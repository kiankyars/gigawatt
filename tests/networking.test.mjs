import test from 'node:test';
import assert from 'node:assert/strict';
import {fabricBudget,messageTime,ringTime,propagation,ringChunkState} from '../course/prototypes/networking-model.js';
import {scenes,initialState} from '../course/prototypes/networking-scenes.js';
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
test('ring sends six quarter-buffers and overlaps only independent compute',()=>{
 const b=ringTime();assert.equal(b.rounds,6);assert.equal(b.sentGB,1.5);assert.equal(b.communicationMs,30);assert.equal(b.overlappedStepMs,210);assert.equal(b.sequentialStepMs,230);
 const slow=ringTime({bandwidthGBps:25});assert.equal(slow.communicationMs,60);assert.equal(slow.overlappedStepMs,240);assert.equal(slow.sequentialStepMs,260);
 assert.equal(ringTime({overlapMs:100}).overlappedStepMs,200);
});
test('ring phase endpoints preserve one reduced owner before distribution',()=>{
 assert.equal(ringChunkState(0).flat().filter(c=>c.kind==='partial').length,16);
 assert.equal(ringChunkState(3).flat().filter(c=>c.kind==='complete').length,4);
 for(const rank of ringChunkState(3))assert.equal(rank.filter(c=>c.kind==='complete').length,1);
 assert.equal(ringChunkState(6).flat().filter(c=>c.kind==='complete').length,16);
});
test('fiber propagation includes distance in both directions for a reply',()=>{
 assert.deepEqual(propagation(100),{oneWayMs:.5,roundTripMs:1});
 assert.deepEqual(propagation(0),{oneWayMs:0,roundTripMs:0});
});
test('models reject impossible intervals and invalid rates',()=>{
 assert.throws(()=>fabricBudget({uplinksPerLeaf:0}),RangeError);assert.throws(()=>ringTime({ranks:1}),RangeError);assert.throws(()=>ringTime({overlapMs:201}),RangeError);assert.throws(()=>messageTime({bytes:1,gbps:0}),RangeError);assert.throws(()=>propagation(-1),RangeError);
});
test('all scenes and selectable states produce renderable desktop and compact mechanisms',()=>{
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 for(const scene of scenes){const states=[initialState,...(scene.controls||[]).flatMap(g=>g.options.map(([v])=>({...initialState,[g.key]:v})))];for(const state of states)for(const compact of[false,true]){const html=networkingVisual(scene.id,state,compact);assert.ok(html.length>100);assert.doesNotMatch(html,/NaN|undefined/);}}
});
test('compute migration preserves both requested opening images and distinguishes local memory from networking',()=>{
 assert.equal(scenes[0].id,'networking-purpose');assert.equal(scenes[1].id,'consumer-hardware-meme');assert.equal(scenes[1].imageOnly,true);
 assert.match(networkingVisual('networking-purpose',initialState),/compute-scales\.png/);
 assert.match(networkingVisual('consumer-hardware-meme',initialState),/compute-consumer-hardware-meme\.png/);
 const path=scenes.find(s=>s.id==='packet-path');assert.deepEqual(path.controls[0].options.map(([value])=>value),['local','rack','cluster']);
 const labels={local:'GPU-local memory',rack:'Inside the rack',cluster:'Across racks'};
 for(const transfer of Object.keys(labels)){
  const html=networkingVisual('packet-path',{...initialState,transfer});
  assert.equal((html.match(/class="selected-path"/g)||[]).length,1);
  assert.ok(html.includes(`aria-label="${labels[transfer]} — selected"`));
  assert.match(html,/One GPU package/);assert.match(html,/HBM/);assert.match(html,/NVLink switches/);assert.match(html,/Fabric switches/);
 }
 assert.match(networkingVisual('shared-model',initialState),/Each GPU receives the other part’s result/);
 assert.match(networkingVisual('shared-model',initialState),/GPUs combine the results/);
});
