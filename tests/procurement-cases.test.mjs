import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {deliverySchedule,modularSchedule,rackInterfaces,releaseHolds,acceptedPaths} from '../course/prototypes/procurement-model.js';
import {scenes,initialState,resolveProcurementScene} from '../course/prototypes/procurement-cases-scenes.js';
import {procurementVisual} from '../course/prototypes/procurement-visuals.js';

const near=(actual,expected,message)=>assert.ok(Math.abs(actual-expected)<1e-9,message||`${actual} ≈ ${expected}`);
const evidenceKeys=['electrical','hydraulic','geometry','logistics','controls','resources'];
const allEvidence=Object.fromEntries(evidenceKeys.map(key=>[key,true]));

test('delivery gains and delays matter only when they move the dependency join',()=>{
 const baseline=deliverySchedule();
 assert.equal(baseline.finish,27);
 assert.deepEqual(baseline.critical,['electrical']);
 assert.equal(baseline.slack.cooling,7);
 assert.equal(deliverySchedule({coolingProcurement:6}).finish,27,'faster cooling adds float without advancing acceptance');
 assert.equal(deliverySchedule({electricalProcurement:14}).finish,23);
 const coolingLate=deliverySchedule({coolingProcurement:18});
 assert.equal(coolingLate.finish,28);
 assert.deepEqual(coolingLate.critical,['cooling']);
 const utilityLate=deliverySchedule({utilityReady:30});
 assert.equal(utilityLate.finish,34);
 assert.deepEqual(utilityLate.critical,['utility']);
 assert.deepEqual(deliverySchedule({coolingProcurement:17}).critical,['electrical','cooling'],'equal finishes create two critical paths');
});

test('prefabrication uses overlap but waits for both design approval and a factory slot',()=>{
 const baseline=modularSchedule();
 assert.equal(baseline.finish,12);
 assert.equal(baseline.siteBuiltFinish,16);
 assert.equal(baseline.arrivalFloat,1);
 assert.equal(modularSchedule({approvalWeek:1}).finish,12,'one week of approval delay consumes arrival float');
 const approvalLate=modularSchedule({approvalWeek:3});
 assert.equal(approvalLate.factoryStart,3);
 assert.equal(approvalLate.finish,14);
 assert.equal(approvalLate.siteBuiltFinish,16);
 assert.equal(modularSchedule({approvalWeek:5}).finish,16);
 const slotLate=modularSchedule({approvalWeek:3,factorySlotWeek:7});
 assert.equal(slotLate.factoryStart,7,'approved design alone does not provide factory capacity');
 assert.equal(slotLate.finish,18);
 assert.equal(slotLate.saving,-2,'prefab can finish later than site assembly');
 const approvalAfterSlot=modularSchedule({approvalWeek:9,factorySlotWeek:7});
 assert.equal(approvalAfterSlot.factoryStart,9,'an available slot does not waive design approval');
 assert.equal(approvalAfterSlot.siteAssemblyStart,9);
 assert.equal(approvalAfterSlot.siteBuiltFinish,17);
 for(const [factoryWeeks,finish]of[[6,12],[9,14],[12,17]])assert.equal(modularSchedule({factoryWeeks}).finish,finish);
});

test('doubling rack density preserves phase capacity but exceeds electrical, flow and pressure limits',()=>{
 const before=rackInterfaces({rackKW:100}),after=rackInterfaces({rackKW:200});
 assert.equal(before.racks,200);assert.equal(after.racks,100);
 assert.equal(before.racksPerZone,20);assert.equal(after.racksPerZone,10);
 assert.equal(before.rackKW*before.racks,20000);
 assert.equal(after.rackKW*after.racks,20000);
 assert.equal(before.phaseFlow,after.phaseFlow);
 near(before.amps,120.28130608117204);
 near(after.amps,240.56261216234408);
 assert.equal(before.electricalPass,true);assert.equal(after.electricalPass,false);
 near(before.flow,2.3923444976076556);
 near(after.flow,4.784688995215311);
 assert.equal(before.flowPass,true);assert.equal(after.flowPass,false);
 near(before.flow*before.racks,before.phaseFlow);
 near(after.flow*after.racks,after.phaseFlow);
 assert.equal(before.pressure,20);assert.equal(after.pressure,80);
 assert.equal(before.pressurePass,true);assert.equal(after.pressurePass,false);
 const flowOnlyUpgrade=rackInterfaces({rackKW:200,allowableFlow:5});
 assert.equal(flowOnlyUpgrade.flowPass,true);
 assert.equal(flowOnlyUpgrade.pressurePass,false,'a flow rating does not establish adequate available pressure');
 assert.equal(after.massPerRackRatio,2);assert.equal(after.loadPerFootRatio,2);
 assert.equal(before.racksPerZone*before.massPerRackRatio,after.racksPerZone*after.massPerRackRatio,'unchanged zone mass does not establish local support adequacy');
});

test('fabrication approvals remain coupled to geometry and never establish service acceptance',()=>{
 const dutyApproved=releaseHolds({electrical:true,hydraulic:true});
 assert.equal(dutyApproved.independentSite,true);
 assert.equal(dutyApproved.electricalFabrication,false);
 assert.equal(dutyApproved.hydraulicFabrication,false);
 assert.equal(dutyApproved.frameFabrication,false);
 const electricalAndGeometry=releaseHolds({electrical:true,geometry:true});
 assert.equal(electricalAndGeometry.electricalFabrication,true);
 assert.equal(electricalAndGeometry.hydraulicFabrication,false);
 assert.equal(electricalAndGeometry.frameFabrication,true);
 assert.equal(releaseHolds({logistics:true}).transportPlan,false);
 assert.equal(releaseHolds({logistics:true,geometry:true}).transportPlan,true);
 assert.equal(releaseHolds(allEvidence).scheduleCommitment,true);
 for(const key of evidenceKeys)assert.equal(releaseHolds({...allEvidence,[key]:false}).scheduleCommitment,false,`the service date still needs ${key} evidence`);
 for(let mask=0;mask<2**evidenceKeys.length;mask++){
  const evidence=Object.fromEntries(evidenceKeys.map((key,index)=>[key,Boolean(mask&(1<<index))]));
  assert.equal(releaseHolds(evidence).serviceAcceptance,false,'approval evidence does not replace an integrated test');
 }
});

test('accepted capacity is the intersection of named racks, not the smallest subsystem count',()=>{
 const baseline=acceptedPaths();
 assert.equal(baseline.count,40);assert.equal(baseline.envelopeMW,4);
 assert.deepEqual(baseline.accepted.map(p=>p.id),Array.from({length:40},(_,i)=>i+21));
 const separateCounts=['electrical','cooling','network'].map(key=>baseline.positions.filter(p=>p[key]).length);
 assert.deepEqual(separateCounts,[80,80,60]);
 assert.notEqual(baseline.count,Math.min(...separateCounts));
 const extended=acceptedPaths({coolingStart:1});
 assert.equal(extended.count,60);assert.equal(extended.envelopeMW,6);
 assert.deepEqual(extended.accepted.map(p=>p.id),Array.from({length:60},(_,i)=>i+1));
 const disjoint=acceptedPaths({electricalEnd:50,coolingStart:51,networkEnd:50});
 assert.equal(disjoint.count,0,'three separately accepted 50-rack systems can have no complete path');
 assert.equal(disjoint.envelopeMW,0);
});

test('schedule and interface calculations reject invalid durations and denominators',()=>{
 for(const value of[-1,NaN,Infinity]){
  assert.throws(()=>deliverySchedule({utilityReady:value}),RangeError);
  assert.throws(()=>modularSchedule({factorySlotWeek:value}),RangeError);
 }
 for(const key of['rackKW','voltage','powerFactor','deltaT'])assert.throws(()=>rackInterfaces({[key]:0}),RangeError);
});

function statesFor(scene){
 let states=[{...initialState}];
 for(const group of scene.controls||[])states=states.flatMap(state=>group.options.map(([value])=>({...state,[group.key]:value})));
 if(scene.id==='release-holds')states=Array.from({length:64},(_,mask)=>({...initialState,...Object.fromEntries(evidenceKeys.map((key,index)=>[key,Boolean(mask&(1<<index))]))}));
 if(scene.id==='release-decision')states=[{...initialState},...['all','independent','stop'].flatMap(diagnosis=>[false,true].map(showDiagnosis=>({...initialState,diagnosis,showDiagnosis})))];
 return states;
}

test('every procurement scene and control state renders with existing photographs',()=>{
 assert.equal(new Set(scenes.map(scene=>scene.id)).size,scenes.length);
 assert.deepEqual([...new Set(scenes.map(scene=>scene.objective))].sort(),['D13.1','D13.2','D13.3','D13.4']);
 const assets=new Set();
 for(const scene of scenes)for(const state of statesFor(scene)){
  const html=procurementVisual(scene.id,state);
  assert.ok(html.length>100,scene.id);
  assert.doesNotMatch(html,/NaN|undefined|Infinity/,scene.id);
  for(const [,src]of html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g)){
   assert.ok(src.startsWith('../assets/'),`${scene.id}: photograph must be bundled`);
   const url=new URL(src,new URL('../course/prototypes/',import.meta.url));
   assert.ok(fs.existsSync(url),`${scene.id}: missing ${src}`);
   assets.add(src);
  }
 }
 assert.ok(assets.size>=2,'the chapter retains multiple real case-study photographs');
 assert.throws(()=>procurementVisual('missing-scene',initialState),/Unknown procurement scene/);
});

test('procurement navigation resolves current scenes',()=>{
 assert.ok(!scenes.some(scene=>scene.id==='polaris-phases'));
 assert.equal(resolveProcurementScene('polaris-phases'),0);
 assert.equal(scenes[resolveProcurementScene('release-decision')].id,'release-decision');
 assert.equal(resolveProcurementScene('unknown'),0);
});
