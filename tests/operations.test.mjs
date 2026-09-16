import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {sampleQuality,heatBalance,readiness,transition,maintenanceState,unavailableUnion,diagnosticEvidence} from '../course/prototypes/operations-model.js';
import {scenes,initialState} from '../course/prototypes/operations-scenes.js';
import {operationsVisual} from '../course/prototypes/operations-visuals.js';
const near=(actual,expected)=>assert.ok(Math.abs(actual-expected)<1e-10,`${actual} ≈ ${expected}`);

test('new delivery does not refresh an old observation, and clock inconsistencies cannot pass',()=>{
 const stale=sampleQuality({observedAt:0,receivedAt:599,now:600});
 assert.equal(stale.age,600);assert.equal(stale.deliveryDelay,599);assert.equal(stale.fresh,false);
 assert.equal(sampleQuality({observedAt:595,receivedAt:599,now:600}).fresh,true);
 assert.equal(sampleQuality({observedAt:540,receivedAt:599,now:600}).fresh,true,'the stated sixty-second limit is inclusive');
 assert.equal(sampleQuality({observedAt:539,receivedAt:599,now:600}).fresh,false);
 assert.equal(sampleQuality({observedAt:610,receivedAt:599,now:600}).quality,'Clock mismatch');
 assert.equal(sampleQuality({observedAt:595,receivedAt:605,now:600}).fresh,false);
 assert.throws(()=>sampleQuality({observedAt:NaN,receivedAt:599,now:600}),RangeError);
});

test('time-aligned row measurements close the heat balance without inventing a cause',()=>{
 near(heatBalance({flow:100,supply:30,returnTemperature:35}).heatMW,2.09);
 near(heatBalance({flow:100,supply:30,returnTemperature:40}).heatMW,4.18);
 near(heatBalance({flow:50,supply:30,returnTemperature:40}).heatMW,2.09);
 near(heatBalance({flow:0}).heatMW,0);
 assert.throws(()=>heatBalance({flow:-1}),RangeError);
 assert.throws(()=>heatBalance({cp:0}),RangeError);
 assert.equal('cause' in heatBalance({flow:50}),false);
});

test('readiness needs fresh physical confirmation beyond command and acknowledgment',()=>{
 const all={command:true,acknowledged:true,flowProven:true,temperatureProven:true,fresh:true};
 assert.equal(readiness(all).available,true);
 for(const key of Object.keys(all))assert.equal(readiness({...all,[key]:false}).available,false,`missing ${key} cannot establish availability`);
 assert.equal(readiness({command:true,acknowledged:true}).acknowledged,true);
 assert.equal(readiness({command:false,acknowledged:true}).acknowledged,false);
});

test('delay and workload admission change the thermal transition without changing final capacity',()=>{
 const two=transition(),three=transition({delayMinutes:3});
 near(two.consumedMWh,1/30);near(two.remainingMWh,1/150);assert.equal(two.withinBudget,true);
 near(three.consumedMWh,.05);assert.equal(three.withinBudget,false);
 assert.equal(transition({delayMinutes:2.4}).withinBudget,true);
 const wait=transition({delayMinutes:3,admit:'ready'});
 assert.equal(wait.consumedMWh,0);assert.equal(wait.waitMinutes,3);
 assert.equal(transition({loadMW:4}).imbalanceMW,0);
 assert.throws(()=>transition({delayMinutes:-1}),RangeError);
 assert.throws(()=>transition({admit:'guess'}),RangeError);
});

test('maintenance evaluates the shared dependency and restoration evidence',()=>{
 assert.equal(maintenanceState().availableMW,6);
 assert.equal(maintenanceState({sharedControl:true}).availableMW,0);
 assert.equal(maintenanceState({configurationMatched:true}).canStart,true);
 assert.equal(maintenanceState({sharedControl:true,configurationMatched:true}).canStart,false);
 const restoration={configurationMatched:true,flowProven:true,restorationChecked:true};
 assert.equal(maintenanceState(restoration).canRestore,true);
 for(const key of Object.keys(restoration))assert.equal(maintenanceState({...restoration,[key]:false}).canRestore,false);
});

test('service time uses the union of clipped impact intervals and never double-counts overlap',()=>{
 const m=unavailableUnion([[0,12],[8,26]]);
 assert.deepEqual(m.merged,[[0,26]]);assert.equal(m.downtime,26);near(m.availability,.9993981481481481);
 const clipped=unavailableUnion([[20,30],[-5,2],[1,4],[3,3],[4,8],[20,25]],{windowStart:0,windowEnd:24});
 assert.deepEqual(clipped.merged,[[0,8],[20,24]]);assert.equal(clipped.downtime,12);assert.equal(clipped.availability,.5);
 assert.equal(unavailableUnion([]).availability,1);
 assert.equal(unavailableUnion([[-10,50000]]).availability,0);
 assert.throws(()=>unavailableUnion([[10,2]]),RangeError);
 assert.throws(()=>unavailableUnion([],{windowStart:1,windowEnd:1}),RangeError);
});

test('diagnostic evidence separates local process, load and configuration',()=>{
 assert.equal(diagnosticEvidence(['plant','pumps']).sufficient,false);
 assert.equal(diagnosticEvidence(['branch','load']).sufficient,false);
 assert.equal(diagnosticEvidence(['branch','load','mapping']).sufficient,true);
 assert.equal(diagnosticEvidence(['branch','load','mapping','plant','pumps']).sufficient,true);
});

function statesFor(scene){
 let states=[{...initialState,evidence:[]}];
 for(const group of scene.controls||[])states=states.flatMap(state=>group.options.map(([value])=>({...state,[group.key]:value})));
 if(scene.id==='diagnosis-check')states=Array.from({length:32},(_,mask)=>({...initialState,evidence:['plant','branch','load','mapping','pumps'].filter((_,index)=>mask&(1<<index))}));
 if(scene.id==='operating-decision')states=[{...initialState},...['restart','hold','plant'].flatMap(diagnosis=>[false,true].map(showDiagnosis=>({...initialState,diagnosis,showDiagnosis})))];
 return states;
}

test('all operational decisions and evidence selections render, with bundled source figures',()=>{
 assert.equal(new Set(scenes.map(scene=>scene.id)).size,scenes.length);
 assert.deepEqual([...new Set(scenes.map(scene=>scene.objective))].sort(),['D14.1','D14.2','D14.3','D14.4','D14.5']);
 const assets=new Set();
 for(const scene of scenes)for(const state of statesFor(scene)){
  const html=operationsVisual(scene.id,state);
  assert.ok(html.length>100,scene.id);assert.doesNotMatch(html,/NaN|undefined|Infinity/,scene.id);
  for(const [,src]of html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g)){
   assert.ok(src.startsWith('../assets/'));
   assert.ok(fs.existsSync(new URL(src,new URL('../course/prototypes/',import.meta.url))),`${scene.id}: missing ${src}`);assets.add(src);
  }
 }
 assert.equal(assets.size,2,'one real facility photo and the publisher control diagram');
 assert.throws(()=>operationsVisual('missing-scene',initialState),/Unknown operations scene/);
});
