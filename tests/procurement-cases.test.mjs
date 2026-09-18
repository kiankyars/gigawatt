import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {deliverySchedule,modularSchedule,rackInterfaces,releaseHolds,acceptedPaths,commissionedService} from '../course/prototypes/procurement-model.js';
import {scenes,sceneAliases,initialState,resolveProcurementScene} from '../course/prototypes/procurement-cases-scenes.js';
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
 assert.equal(baseline.count,40);assert.equal(baseline.envelopeMW,8);
 assert.deepEqual(baseline.accepted.map(p=>p.id),Array.from({length:40},(_,i)=>i+21));
 const separateCounts=['electrical','cooling','network'].map(key=>baseline.positions.filter(p=>p[key]).length);
 assert.deepEqual(separateCounts,[80,80,60]);
 assert.notEqual(baseline.count,Math.min(...separateCounts));
 const extended=acceptedPaths({coolingStart:1});
 assert.equal(extended.count,60);assert.equal(extended.envelopeMW,12);
 assert.deepEqual(extended.accepted.map(p=>p.id),Array.from({length:60},(_,i)=>i+1));
 const disjoint=acceptedPaths({electricalEnd:50,coolingStart:51,networkEnd:50});
 assert.equal(disjoint.count,0,'three separately accepted 50-rack systems can have no complete path');
 assert.equal(disjoint.envelopeMW,0);
 assert.equal(acceptedPaths({rackKW:100}).envelopeMW,4,'the reader calculation can still select its declared rack duty');
});

test('service release intersects complete paths with passing measured response and excludes unaccepted evidence',()=>{
 const baseline=commissionedService();
 assert.equal(baseline.count,20);assert.equal(baseline.envelopeMW,4);
 assert.deepEqual(baseline.eligible.map(rack=>rack.id),Array.from({length:20},(_,i)=>i+21));
 assert.deepEqual(baseline.awaitingResponseAcceptance.map(rack=>rack.id),Array.from({length:20},(_,i)=>i+41));
 assert.ok(baseline.awaitingResponseAcceptance.every(rack=>rack.pathAccepted&&!rack.eligible),'a complete service path and a command do not demonstrate failure response');
 assert.equal(commissionedService({responsePassedIds:[]}).count,0);
 assert.equal(commissionedService({pathAcceptedIds:[21,22],responsePassedIds:[22,23]}).count,1,'records must name the same racks');
 assert.deepEqual(commissionedService({pathAcceptedIds:[21,21],responsePassedIds:[21,21]}).eligible.map(rack=>rack.id),[21],'duplicate records do not create extra capacity');
 assert.equal(commissionedService({otherCriteriaMet:false}).count,0,'this partial evidence does not waive remaining acceptance criteria');
 assert.equal(commissionedService({responseCommandedIds:[]}).count,20,'a passing measured response is not invalidated by omitting a redundant command record');
 for(const value of[0,-200,NaN,Infinity])assert.throws(()=>commissionedService({rackKW:value}),RangeError);
 for(const key of['pathAcceptedIds','responsePassedIds','responseCommandedIds'])for(const value of[[0],[101],[21.5],null])assert.throws(()=>commissionedService({[key]:value}),RangeError);
 assert.throws(()=>commissionedService({otherCriteriaMet:'yes'}),TypeError);
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
 return states;
}

test('every procurement scene and control state renders with existing photographs',()=>{
 assert.equal(new Set(scenes.map(scene=>scene.id)).size,scenes.length);
 assert.equal(scenes[0].id,'epc-and-prefab','the EPC responsibilities open the chapter');
 assert.deepEqual(scenes.slice(1,6).map(scene=>scene.id),['rack-case-brief','rack-change','electrical-interface','hydraulic-interface','spatial-interface'],'keep the rack-change case and its consequences together');
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
 assert.equal(scenes.at(-1).id,'phase-boundary');
 for(const retired of['release-decision','controls-interface','integrated-tests'])assert.ok(!scenes.some(scene=>scene.id===retired),`${retired} is no longer an active procurement slide`);
 assert.equal(resolveProcurementScene('unknown'),0);
 for(const [oldId,currentId]of Object.entries(sceneAliases))assert.equal(scenes[resolveProcurementScene(oldId)].id,currentId);
 for(const id of['aws-houdini-prefab','compass-package'])assert.equal(scenes[resolveProcurementScene(id)].id,id);
});

test('electrical and hydraulic comparisons keep both rack duties visible without a rack-duty toggle',()=>{
 for(const id of['electrical-interface','hydraulic-interface']){
  const scene=scenes.find(scene=>scene.id===id);
  assert.ok(!(scene.controls||[]).some(control=>control.key==='rackKW'));
  const before=procurementVisual(id,{...initialState,rackKW:100});
  const after=procurementVisual(id,{...initialState,rackKW:200});
  assert.equal(before,after,'a stale rack-duty state cannot hide half of the comparison');
  if(id==='electrical-interface'){assert.match(after,/100 kW/);assert.match(after,/200 kW/);}
  else{for(const rackKW of[100,200]){const m=rackInterfaces({rackKW});assert.ok(after.includes(`${m.flow.toFixed(1)} kg/s`));assert.ok(after.includes(`${m.pressure} kPa`));}}
 }
});

test('accepted-path visuals show the overlap for the revised rack duty',()=>{
 assert.match(procurementVisual('accepted-paths',{...initialState,coolingStart:21}),/40 racks · 8 MW/);
 assert.match(procurementVisual('accepted-paths',{...initialState,coolingStart:1}),/60 racks · 12 MW/);
});

function playerAt(hash){
 class Element{
  constructor(){this.children=[];this.dataset={};this.attributes={};this.listeners={};}
  append(...children){this.children.push(...children);}add(child){this.children.push(child);}replaceChildren(...children){this.children=children;}
  setAttribute(key,value){this.attributes[key]=String(value);if(key.startsWith('data-'))this.dataset[key.slice(5).replace(/-([a-z])/g,(_,c)=>c.toUpperCase())]=String(value);}
  getAttribute(key){return this.attributes[key];}focus(){}addEventListener(name,fn){this.listeners[name]=fn;}closest(){return this.header||(this.header=new Element());}
 }
 const elements=new Map(['scenes','fullscreen','scene','scene-title','visual','lesson-reference','status','progress','previous','next','actions','viewer'].map(id=>[id,new Element()]));
 let inline=[];
 Object.defineProperty(elements.get('visual'),'innerHTML',{get(){return this.html;},set(html){this.html=html;inline=[];for(const [,attrs]of html.matchAll(/<button\b([^>]*)>/g)){const button=new Element();for(const [,key,value]of attrs.matchAll(/([\w-]+)="([^"]*)"/g))button.setAttribute(key,value);inline.push(button);}}});
 const descendants=element=>element.children.flatMap(child=>[child,...descendants(child)]);
 const buttons=()=>descendants(elements.get('actions')).filter(element=>element.type==='button');
 const listeners={},location={hash,search:'?teach=1',replace(url){this.redirect=url;}};
 const document={getElementById:id=>elements.get(id)||inline.find(button=>button.getAttribute('id')===id),createElement:()=>new Element(),querySelector:()=>null,querySelectorAll:selector=>{const attr=selector.slice(1,-1);return inline.filter(element=>element.getAttribute(attr)!==undefined);},addEventListener(){}};
 const window={addEventListener:(name,fn)=>{listeners[name]=fn;},scrollTo(){}};
 const source=fs.readFileSync(new URL('../course/prototypes/procurement-cases-player.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
 vm.runInNewContext(source,{document,window,location,history:{replaceState(_state,_title,hash){location.hash=hash;}},URLSearchParams,Option:class{constructor(label,value){this.label=label;this.value=value;}},scenes,initialState,resolveProcurementScene,procurementVisual,presentationLabels:{'procurement-cases':'13. EPC'}});
 return {elements,document,location,go(id){location.hash=`#${id}`;listeners.hashchange();},click(key,value){const button=buttons().find(button=>button.dataset.choice===key&&String(button.dataset.value)===String(value));assert.ok(button,`${key}=${value}`);button.onclick();}};
}

test('actual player preserves the selected cooling extent across chapter navigation',()=>{
 const player=playerAt('#accepted-paths'),html=()=>player.elements.get('visual').innerHTML;
 assert.match(html(),/40 racks · 8 MW/);
 player.click('coolingStart',1);assert.match(html(),/60 racks · 12 MW/);
 player.go('phase-boundary');assert.equal(player.elements.get('scene').dataset.scene,'phase-boundary');
 assert.equal(player.elements.get('next').disabled,true,'the phased-delivery case closes the chapter');
 player.go('accepted-paths');assert.match(html(),/60 racks · 12 MW/);
 player.click('coolingStart',21);assert.match(html(),/40 racks · 8 MW/);
 player.go('site-checks');assert.equal(player.elements.get('scene').dataset.scene,'factory-acceptance');
 player.go('release-decision');assert.equal(player.elements.get('scene').dataset.scene,'phase-boundary');
 player.go('handover-records');assert.equal(player.elements.get('scene').dataset.scene,'phase-boundary');
});

test('old cooling-failure bookmarks redirect to the combined cooling lesson',()=>{
 for(const id of['controls-interface','integrated-tests','service-requirements']){
  const player=playerAt(`#${id}`);
  assert.equal(player.location.redirect,'./cooling-format.html?teach=1#cooling-response');
  assert.equal(player.elements.get('visual').innerHTML,undefined,'the obsolete procurement scene is not drawn before redirecting');
 }
});
