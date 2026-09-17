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
test('the chapter retains facility mechanisms and removes repeated software explanations without aliases',()=>{
 const removed=['message-time','all-reduce','collective-time','fabric-failure','storage-handoff'];
 assert.equal(scenes.length,21);
 for(const id of removed){assert.ok(!scenes.some(scene=>scene.id===id));assert.equal(resolveNetworkingScene(id),0);assert.throws(()=>networkingVisual(id,initialState),/No networking visual/);}
 assert.equal(scenes.at(-1).id,'meta-rsc');
 const incast=scenes.findIndex(scene=>scene.id==='incast');assert.equal(scenes[incast-1].id,'traffic-placement');assert.equal(scenes[incast+1].id,'ethernet-infiniband');
 const placement=scenes.find(scene=>scene.id==='traffic-placement');assert.deepEqual(placement.controls[0].options,[['remote','Across two leaves'],['local','Under one leaf']]);assert.notEqual(placement.controls[0].label,'Place the communicating servers');
 assert.match(networkingVisual('incast',initialState),/1,600 Gb\/s arriving/);assert.match(networkingVisual('incast',initialState),/400 Gb\/s →/);assert.match(networkingVisual('incast',initialState),/receiving link stays at 400 Gb\/s/);
});
test('the network choice explains the full system and the distance example isolates propagation',()=>{
 const fabrics=networkingVisual('ethernet-infiniband',initialState);
 assert.match(fabrics,/RDMA over Converged Ethernet/);assert.match(fabrics,/remote direct memory access/);
 for(const label of ['Routing','Congestion control','Collective software','Job placement'])assert.ok(fabrics.includes(label),label);
 assert.equal((fabrics.match(/24,576 H100 GPUs/g)||[]).length,2);
 const distance=networkingVisual('distance-latency',initialState);
 assert.match(distance,/100 km fiber route/);assert.match(distance,/Request · 0.5 ms/);assert.match(distance,/Reply · 0.5 ms/);assert.match(distance,/>1 ms</);assert.match(distance,/propagation alone/);
 assert.doesNotMatch(distance,/Multislice|Amdahl|Bulk data|Dependent exchanges/);
});
test('the diagnosis reveals evidence by selecting one of two physical links',()=>{
 const unrevealed=networkingVisual('network-diagnosis',initialState);
 assert.match(unrevealed,/>20 ms</);assert.match(unrevealed,/>50 ms</);
 assert.match(unrevealed,/Cable just moved/);assert.match(unrevealed,/Same transfer from each server/);
 assert.doesNotMatch(unrevealed,/Errors rose after the move|diagnosis-reveal/);
 for(const [diagnosis,finding]of [['link','Errors rose after the move'],['uplink','Capacity is available']]){
  const chosen=networkingVisual('network-diagnosis',{...initialState,diagnosis});assert.match(chosen,new RegExp(`data-diagnosis="${diagnosis}" aria-pressed="true"`));assert.ok(chosen.includes(finding));
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
 for(const scene of scenes){let states=[initialState];for(const group of scene.controls||[])states=states.flatMap(state=>group.options.map(([value])=>({...state,[group.key]:value})));if(scene.id==='network-diagnosis')states=['','link','uplink'].map(diagnosis=>({...initialState,diagnosis}));for(const state of states)for(const compact of[false,true]){const html=networkingVisual(scene.id,state,compact);assert.ok(html.length>100,scene.id);assert.doesNotMatch(html,/NaN|undefined/,scene.id);}}
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
