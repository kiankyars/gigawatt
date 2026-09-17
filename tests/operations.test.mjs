import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {sampleQuality,heatBalance,readiness,transition,maintenanceState,unavailableUnion,diagnosticEvidence,flexibleSchedule} from '../course/prototypes/operations-model.js';
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

test('workload shifting meets the selected deadline while conserving execution and energy',()=>{
 const shifted=flexibleSchedule(),continuous=flexibleSchedule({shift:false});
 assert.deepEqual(shifted.segments,[{start:13,end:14},{start:16,end:18}]);
 assert.equal(shifted.finishHour,18);assert.equal(shifted.eventPeakMW,20);assert.equal(shifted.laterPeakMW,24);assert.equal(shifted.eventOverlapHours,0);
 assert.equal(shifted.meetsDeadline,true);assert.equal(shifted.slackHours,2);
 assert.equal(continuous.finishHour,16);assert.equal(continuous.eventPeakMW,24);assert.equal(continuous.laterPeakMW,20);assert.equal(continuous.eventOverlapHours,2);
 assert.equal(flexibleSchedule({deadlineHour:17}).meetsDeadline,false);
 assert.equal(flexibleSchedule({deadlineHour:17}).slackHours,-1);
 assert.equal(flexibleSchedule({deadlineHour:18}).meetsDeadline,true,'completion at the deadline is valid');
 for(const run of [shifted,continuous]){near(run.jobMWh,12);near(run.segments.reduce((sum,segment)=>sum+segment.end-segment.start,0),3);}
 assert.deepEqual(flexibleSchedule({workHours:1}).segments,[{start:13,end:14}],'a job complete before the event needs no restart');
 assert.deepEqual(flexibleSchedule({startHour:14}).segments,[{start:16,end:19}],'an event at job start does not leave an empty segment');
 for(const options of [{eventEnd:14},{eventStart:12},{workHours:NaN},{jobMW:0},{deadlineHour:-1}])assert.throws(()=>flexibleSchedule(options),RangeError);
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
 assert.equal(assets.size,3,'two real facility photos and the publisher control diagram');
 assert.throws(()=>operationsVisual('missing-scene',initialState),/Unknown operations scene/);
});

test('the four migrated scenes have operations references, real sources and the intended sequence',()=>{
 const ids=scenes.map(scene=>scene.id);
 assert.equal(scenes.length,26);
 assert.deepEqual(ids.slice(ids.indexOf('admit-work'),ids.indexOf('admit-work')+3),['admit-work','google-demand-response','deadline-scheduling']);
 assert.deepEqual(ids.slice(ids.indexOf('common-cause'),ids.indexOf('common-cause')+4),['common-cause','replication-and-backup','london-recovery','llama-recovery']);
 for(const id of ['google-demand-response','deadline-scheduling','replication-and-backup','llama-recovery']){
  const scene=scenes.find(item=>item.id===id);
  assert.match(scene.reference,/^d14-/);
  for(const group of scene.controls||[])assert.ok(group.options.some(([value])=>value===initialState[group.key]),`${id}: ${group.key} has an active initial choice`);
  if(id!=='deadline-scheduling')for(const source of scene.sources)assert.ok(operationsVisual(id,initialState).includes(source),`${id}: source credit preserved`);
 }
 for(const file of ['operations-visuals.js','operations-model.js','operations-player.js','operations-scenes.js']){
  const source=fs.readFileSync(new URL(`../course/prototypes/${file}`,import.meta.url),'utf8');
  assert.doesNotMatch(source,/from\s+['"][^'"]*storage[^'"]*['"]/,`${file}: no dependency on the retired deck`);
 }
 assert.match(operationsVisual('llama-recovery',initialState),/confirmed or suspected hardware issues/);
 assert.match(operationsVisual('llama-recovery',initialState),/Automated diagnosis/);
 assert.match(operationsVisual('replication-and-backup',{...initialState,replicaFault:'write'}),/Bad write copied/);
});

function operationsPlayerAt(hash){
 class Element{
  constructor(){this.children=[];this.dataset={};this.attributes={};}
  append(...children){this.children.push(...children);}
  add(child){this.children.push(child);}
  replaceChildren(...children){this.children=children;}
  setAttribute(key,value){this.attributes[key]=value;}
  focus(){}
 }
 const elements=new Map(['scenes','fullscreen','scene','scene-title','visual','lesson-reference','status','progress','previous','next','actions','viewer'].map(id=>[id,new Element()]));
 const listeners={},location={hash,search:''};
 const buttons=()=>elements.get('actions').children.flatMap(group=>group.children).filter(element=>element.type==='button');
 const document={getElementById:id=>elements.get(id),createElement:()=>new Element(),querySelector:()=>null,querySelectorAll:()=>[],addEventListener(){}};
 const window={addEventListener:(name,fn)=>{listeners[name]=fn;},scrollTo(){}};
 const source=fs.readFileSync(new URL('../course/prototypes/operations-player.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
 vm.runInNewContext(source,{document,window,location,history:{replaceState(_state,_title,hash){location.hash=hash;}},URLSearchParams,Option:class{constructor(label,value){this.label=label;this.value=value;}},scenes,initialState,operationsVisual,presentationLabels:{operations:'14. Controls, operations and reliability'}});
 return {elements,buttons,document,go(id){location.hash=`#${id}`;listeners.hashchange();},click(key,value){const button=buttons().find(button=>button.dataset.choice===key&&button.dataset.value===String(value));assert.ok(button,`${key}=${value}`);button.onclick();}};
}

test('the actual operations player keeps deadline and replica controls synchronized across navigation',()=>{
 const player=operationsPlayerAt('#deadline-scheduling');
 const selected=key=>player.buttons().filter(button=>button.dataset.choice===key&&button.attributes['aria-pressed']==='true').map(button=>button.dataset.value);
 const html=()=>player.elements.get('visual').innerHTML;
 assert.deepEqual(selected('shift'),['true']);assert.deepEqual(selected('deadline'),['20']);
 assert.match(html(),/finishes at 18:00, and meets its deadline/);
 assert.equal(player.elements.get('progress').textContent,'13 / 26');
 player.click('deadline',17);assert.deepEqual(selected('deadline'),['17']);assert.match(html(),/misses its deadline/);assert.match(html(),/<strong>18:00<\/strong>/);
 player.click('shift',false);assert.deepEqual(selected('shift'),['false']);assert.match(html(),/finishes at 16:00, and meets its deadline/);assert.match(html(),/<strong>24 MW<\/strong>/);
 player.go('replication-and-backup');assert.deepEqual(selected('replicaFault'),['device']);assert.match(html(),/Valid data available/);
 player.click('replicaFault','write');assert.deepEqual(selected('replicaFault'),['write']);assert.match(html(),/Bad write copied/);assert.match(html(),/Earlier valid version/);
 player.go('deadline-scheduling');assert.deepEqual(selected('shift'),['false']);assert.deepEqual(selected('deadline'),['17']);
 player.click('deadline',20);player.click('shift',true);assert.match(html(),/finishes at 18:00, and meets its deadline/);assert.match(html(),/<strong>12 MWh<\/strong>/);
 assert.match(player.document.title,/^14\. Controls, operations and reliability/);
});
