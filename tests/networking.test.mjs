import test from 'node:test';
import assert from 'node:assert/strict';
import {fabricBudget,messageTime,communicationTime,propagation} from '../course/prototypes/networking-model.js';
import {scenes,initialState,resolveNetworkingScene} from '../course/prototypes/networking-scenes.js';
import {networkingVisual} from '../course/prototypes/networking-visuals.js';
test('fabric model counts both switch ends of an uplink and uses one-direction cut capacity',()=>{
 const b=fabricBudget();assert.equal(b.endpointCables,16);assert.equal(b.uplinkCables,8);assert.equal(b.cables,24);assert.equal(b.switchPorts,32);assert.equal(b.oversubscription,2);assert.equal(b.transferSeconds,.32);
 const wider=fabricBudget({uplinksPerLeaf:4});assert.equal(wider.transferSeconds,.16);assert.equal(wider.oversubscription,1);
 const excess=fabricBudget({uplinksPerLeaf:8});assert.equal(excess.transferSeconds,.16,'endpoint ports bound further uplink additions');
});
test('message model converts bytes to bits before dividing by gigabits per second',()=>{
 assert.deepEqual(messageTime({bytes:1000}),{serializationUs:.02,totalUs:5.02});
 assert.deepEqual(messageTime({bytes:1e9}),{serializationUs:20000,totalUs:20005});
});
test('only exchange time beyond independent computation delays the step',()=>{
 const b=communicationTime();assert.equal(b.communicationMs,30);assert.equal(b.exposedMs,10);assert.equal(b.communicationStartMs,180);assert.equal(b.overlappedStepMs,210);assert.equal(b.sequentialStepMs,230);
 const slow=communicationTime({communicationMs:60});assert.equal(slow.exposedMs,40);assert.equal(slow.overlappedStepMs,240);assert.equal(slow.sequentialStepMs,260);
 assert.equal(communicationTime({overlapMs:100}).overlappedStepMs,200,'hidden communication cannot shorten the compute interval');
 assert.equal(communicationTime({overlapMs:0}).overlappedStepMs,b.sequentialStepMs);
});
test('collective scope keeps the shared result and timing consequence',()=>{
 const collective=scenes.findIndex(s=>s.id==='all-reduce');assert.equal(scenes[collective+1].id,'collective-time');
 assert.ok(!scenes.some(s=>s.id==='ring-collective'));
 assert.equal(scenes[resolveNetworkingScene('collective-time')].id,'collective-time');
 assert.equal(resolveNetworkingScene('missing-slide'),0);
 assert.ok(!scenes.some(s=>s.id==='tpu-interconnect'));
 const allreduce=networkingVisual('all-reduce',initialState);
 for(const [i,value]of[2,5,7].entries())assert.match(allreduce,new RegExp(`GPU ${i+1}: contribution ${value}`));
 assert.equal((allreduce.match(/combined result 14/g)||[]).length,3);
 for(const communicationMs of[30,60]){
  const html=networkingVisual('collective-time',{...initialState,communicationMs});
  assert.match(html,/200 ms/);assert.match(html,/20 ms of independent work/);
  assert.match(html,new RegExp(`${200+communicationMs} ms`));assert.match(html,new RegExp(`${180+communicationMs} ms`));
  assert.doesNotMatch(html,/ring|1\.5 GB|gradient|reduce.scatter|all.gather/i);
 }
});
test('fiber propagation includes distance in both directions for a reply',()=>{
 assert.deepEqual(propagation(100),{oneWayMs:.5,roundTripMs:1});
 assert.deepEqual(propagation(0),{oneWayMs:0,roundTripMs:0});
});
test('models reject impossible intervals and invalid rates',()=>{
 assert.throws(()=>fabricBudget({uplinksPerLeaf:0}),RangeError);assert.throws(()=>communicationTime({communicationMs:0}),RangeError);assert.throws(()=>communicationTime({overlapMs:201}),RangeError);assert.throws(()=>messageTime({bytes:1,gbps:0}),RangeError);assert.throws(()=>propagation(-1),RangeError);
});
test('all scenes and selectable states produce renderable desktop and compact mechanisms',()=>{
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 for(const scene of scenes){const states=[initialState,...(scene.controls||[]).flatMap(g=>g.options.map(([v])=>({...initialState,[g.key]:v})))];for(const state of states)for(const compact of[false,true]){const html=networkingVisual(scene.id,state,compact);assert.ok(html.length>100);assert.doesNotMatch(html,/NaN|undefined/);}}
});
test('compute migration preserves both requested opening images and distinguishes local memory from networking',()=>{
 assert.equal(scenes[0].id,'networking-purpose');assert.equal(scenes[1].id,'consumer-hardware-meme');assert.equal(scenes[1].imageOnly,true);
 assert.match(networkingVisual('networking-purpose',initialState),/compute-scales\.png/);
 assert.match(networkingVisual('consumer-hardware-meme',initialState),/compute-consumer-hardware-meme\.png/);
 const path=scenes.find(s=>s.id==='packet-path');assert.equal(path.controls,undefined);
 const html=networkingVisual('packet-path',initialState);
 assert.doesNotMatch(html,/muted-path|selected-path/);
 for(const label of ['GPU-local memory','Inside the rack','Across racks'])assert.ok(html.includes(`aria-label="${label}"`));
 assert.doesNotMatch(html,/One GPU package|1 GPU package|[Cc]ompute tray/);assert.match(html,/HBM/);assert.match(html,/NVLink switches/);assert.match(html,/Fabric switches/);
 assert.doesNotMatch(networkingVisual('shared-model',initialState),/Each GPU receives the other part’s result|Exchange through/);
 assert.match(networkingVisual('shared-model',initialState),/GPUs combine the results/);
});
