import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {coupledOutage,weatherCapacity,densityRetrofit,stalledJob,phaseAcceptance} from '../course/prototypes/integrated-cases-model.js';
import {scenes,initialState,learningContract,sceneAliases} from '../course/prototypes/integrated-cases-scenes.js';
import {integratedCasesVisual} from '../course/prototypes/integrated-cases-visuals.js';
const near=(actual,expected)=>assert.ok(Math.abs(actual-expected)<1e-9,`${actual} ≈ ${expected}`);

test('outage power, energy and thermal evidence remain separate after either redesign',()=>{
 const base=coupledOutage(),energy=coupledOutage({plan:'energy'}),aux=coupledOutage({plan:'auxiliaries'});
 assert.equal(base.acKWh,540);assert.equal(base.requiredKWh,400);assert.equal(base.reserveKWh,140);near(base.idealMinutes,16.2);
 assert.equal(energy.acKWh,720);near(energy.idealMinutes,21.6);assert.equal(energy.pumpSupplySurvives,false);
 assert.equal(aux.supportedMW,2.2);assert.equal(aux.requiredKWh,440);assert.equal(aux.reserveKWh,100);near(aux.idealMinutes,14.727272727272727);assert.equal(aux.pumpSupplySurvives,true);
 for(const m of [base,energy,aux]){assert.equal(m.electricalPass,true);assert.equal(m.thermalSupport,'unestablished');assert.equal(m.serviceAccepted,false);near(m.requiredKWh+m.reserveKWh,m.acKWh);}
 assert.equal(coupledOutage({inverterMW:1.9}).powerPass,false,'energy inventory cannot repair a power rating');
 assert.equal(coupledOutage({minutes:17}).energyPass,false);
 assert.equal(coupledOutage({minutes:16.2}).energyPass,true);
 assert.equal(coupledOutage({eta:1}).acKWh,600);
});

test('paired weather limits distinguish energy saving, capacity release and accepted paths',()=>{
 const mild=weatherCapacity({weather:'mild'}),hot=weatherCapacity(),saving=weatherCapacity({remedy:'auxiliaries'}),cooling=weatherCapacity({remedy:'cooling'});
 assert.equal(mild.racks,700);assert.equal(hot.racks,550);assert.equal(saving.racks,550);assert.equal(cooling.racks,650);
 assert.equal(saving.electricalMW,85);assert.equal(saving.auxiliaryMW,15);assert.equal(saving.coolingMW,55);
 assert.equal(cooling.electricalMW,75);assert.equal(cooling.coolingMW,65);
 const accepted=weatherCapacity({remedy:'cooling',acceptedRacks:600});
 assert.equal(accepted.racks,600);assert.deepEqual(accepted.binding,['paths']);assert.equal(accepted.capacityMW,60);assert.equal(accepted.facilityMW,83);assert.equal(accepted.demandSupported,true);
 assert.equal(weatherCapacity({remedy:'cooling',acceptedRacks:600,demandMW:61}).demandSupported,false);
 assert.deepEqual(weatherCapacity({acceptedRacks:550}).binding,['cooling','paths']);
 assert.equal(weatherCapacity({acceptedRacks:0}).racks,0);
 assert.equal(weatherCapacity({siteMW:20}).capacityMW,0,'auxiliaries can consume the whole service');
 assert.equal(weatherCapacity({rackKW:120}).racks,458,'only whole supported rack equivalents count');
});

test('retrofit closes both conversion boundaries without treating a low current as a release',()=>{
 const a=densityRetrofit({architecture:'a'}),b=densityRetrofit({architecture:'b'}),clear=densityRetrofit({architecture:'b',route:'clear'});
 near(a.aInputKW,125);near(b.bInputKW,120/(.97*.98));near(b.intermediateKW,120/.98);near(b.amps,(120/.98)*1000/800);
 near(b.sidecarLossKW+b.nearLossKW+120,b.bInputKW);near(b.aLossKW+120,b.aInputKW);near(b.roomHeatKW,b.inputKW);
 assert.equal(a.releaseCandidate,true);assert.equal(b.electricalPass,true);assert.equal(b.thermalPass,true);assert.equal(b.accessPass,false);assert.equal(b.releaseCandidate,false);
 assert.equal(clear.releaseCandidate,true);assert.equal(clear.roomHeatKW,b.roomHeatKW);assert.equal(clear.inputKW,b.inputKW);
 assert.equal(densityRetrofit({architecture:'b',route:'clear',roomCoolingKW:125}).releaseCandidate,false,'a clear route cannot close a heat limit');
 assert.equal(densityRetrofit({volts:400}).bInputKW,b.bInputKW);near(densityRetrofit({volts:400}).amps,2*b.amps);
});

test('network intervention must change the physical path bottleneck before serial progress improves',()=>{
 const base=stalledJob(),endpoint=stalledJob({upgrade:'endpoint'}),fabric=stalledJob({upgrade:'fabric'});
 assert.equal(base.communicationSeconds,20);assert.equal(base.cycleSeconds,90);near(base.computeShare,2/3);
 assert.equal(endpoint.rates.sender,160);assert.equal(endpoint.achievedGBps,40);assert.equal(endpoint.cycleSeconds,90);assert.deepEqual(endpoint.binding,['fabric']);
 assert.equal(fabric.achievedGBps,80);assert.equal(fabric.communicationSeconds,10);assert.equal(fabric.cycleSeconds,80);near(fabric.throughputRatio,1.125);
 assert.deepEqual(fabric.binding,['sender','fabric','receiver']);
 const receiver=stalledJob({upgrade:'fabric',receiverGBps:50});assert.equal(receiver.achievedGBps,50);assert.equal(receiver.communicationSeconds,16);assert.equal(receiver.cycleSeconds,86);
 for(const m of [base,endpoint,fabric,receiver])near(m.communicationSeconds*m.achievedGBps,800);
});

test('opening scope counts successful groups and a failed cooling test adds no accepted service',()=>{
 assert.equal(phaseAcceptance().acceptedRacks,300);assert.equal(phaseAcceptance().acceptedMW,30);
 assert.equal(phaseAcceptance({open:'ab'}).canOpen,false);assert.equal(phaseAcceptance({open:'all'}).canOpen,false);
 assert.equal(phaseAcceptance({day:5.99}).acceptedRacks,300);assert.equal(phaseAcceptance({day:6}).acceptedRacks,550);assert.equal(phaseAcceptance({day:7}).acceptedRacks,800);
 assert.equal(phaseAcceptance({day:8,cTest:'fail'}).acceptedRacks,550);
 assert.equal(phaseAcceptance({day:11.99,cTest:'fail'}).acceptedRacks,550);assert.equal(phaseAcceptance({day:12,cTest:'fail'}).acceptedRacks,800);
 assert.equal(phaseAcceptance({day:12,cTest:'fail',cRetestPass:false}).acceptedRacks,550,'a planned retest date does not establish a passing result');
 assert.equal(phaseAcceptance({day:12,bPass:false,cTest:'fail',cRetestPass:false}).acceptedRacks,300);
 for(const day of [0,6,7,8,12])for(const cTest of ['pass','fail']){
  const m=phaseAcceptance({day,cTest});assert.equal(m.installedRacks,800);assert.equal(m.installedMW,80);assert.equal(m.acceptedRacks,m.groups.filter(g=>g.accepted).reduce((s,g)=>s+g.racks,0));
 }
});

test('models reject impossible efficiencies, invalid boundaries and unknown cases',()=>{
 for(const value of [NaN,Infinity,-1]){
  assert.throws(()=>coupledOutage({minutes:value}),RangeError);assert.throws(()=>weatherCapacity({acceptedRacks:value}),RangeError);assert.throws(()=>phaseAcceptance({day:value}),RangeError);
 }
 for(const eta of [0,1.01,NaN]){assert.throws(()=>coupledOutage({eta}),RangeError);assert.throws(()=>densityRetrofit({etaNear:eta}),RangeError);}
 assert.throws(()=>weatherCapacity({acceptedRacks:4.5}),RangeError);
 assert.throws(()=>stalledJob({fabricGBps:0}),RangeError);assert.throws(()=>densityRetrofit({volts:0}),RangeError);
 for(const [fn,options]of [[coupledOutage,{plan:'guess'}],[weatherCapacity,{weather:'guess'}],[densityRetrofit,{route:'guess'}],[stalledJob,{upgrade:'guess'}],[phaseAcceptance,{cTest:'guess'}]])assert.throws(()=>fn(options),RangeError);
});

function statesFor(scene){
 let states=[{...initialState}];
 for(const group of scene.controls||[])states=states.flatMap(state=>group.options.map(([value])=>({...state,[group.key]:value})));
 if(scene.id==='phase-choice')states=[false,true].map(openingReveal=>({...initialState,openingReveal}));
 return states;
}

test('all five cases keep their problem and decision with valid sources in every offered state',()=>{
 assert.equal(scenes.length,17);assert.equal(new Set(scenes.map(s=>s.id)).size,17);assert.ok(learningContract.primary_payoff);
 for(const id of ['C01','C02','C03','C04','C05']){const group=scenes.filter(s=>s.case_id===id);assert.equal(group.length,3,id);assert.equal(group[0].pedagogical_role,'problem');assert.ok(group.some(s=>s.pedagogical_role==='transfer'));}
 const assets=new Set(),references=new Set(JSON.parse(fs.readFileSync(new URL('../course/expansion/capstones.json',import.meta.url),'utf8')).map(item=>item.id));
 for(const scene of scenes){
  assert.ok(references.has(scene.reference),scene.id);
  for(const group of scene.controls||[])assert.ok(group.options.some(([value])=>value===initialState[group.key]));
  for(const state of statesFor(scene)){
   const html=integratedCasesVisual(scene.id,state);assert.ok(html.length>150,scene.id);assert.doesNotMatch(html,/NaN|undefined|Infinity/,scene.id);assert.doesNotMatch(html,/checkpoint/i,scene.id);
   for(const [,src]of html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g)){assert.ok(src.startsWith('../assets/'));assert.ok(fs.existsSync(new URL(src,new URL('../course/prototypes/',import.meta.url))));assets.add(src);}
   for(const source of scene.sources||[])assert.ok(html.includes(source));
  }
 }
 assert.deepEqual([...assets],['../assets/references/distribution-abilene-data-halls.jpg']);
 assert.throws(()=>integratedCasesVisual('missing',initialState),/Unknown integrated case scene/);
});

test('comparisons show alternatives together and retain the limits on their conclusions',()=>{
 assert.deepEqual(scenes.filter(s=>s.controls?.length).map(s=>s.id),['weather-paths','density-route']);
 for(const id of ['outage-choice','weather-choice','job-choice','job-consequence','phase-schedule'])assert.doesNotMatch(integratedCasesVisual(id,initialState),/<button/);
 const outage=integratedCasesVisual('outage-choice',initialState);for(const text of ['16.2','21.6','14.73','Powered','Lost','temperatures'])assert.ok(outage.includes(text),text);
 const weather=integratedCasesVisual('weather-choice',initialState);assert.equal((weather.match(/550 <span>racks/g)||[]).length,2);assert.match(weather,/650 <span>racks/);assert.match(weather,/auxiliary demand at 25 MW/);
 const job=integratedCasesVisual('job-consequence',initialState);for(const text of ['40 → 45','+12.5%','60 s','20 s','10 s','correctness'])assert.ok(job.includes(text),text);
 const schedule=integratedCasesVisual('phase-schedule',initialState);for(const text of ['test passes','test fails','Day 7','Day 12','passing test'])assert.ok(schedule.includes(text),text);
});

function playerAt(hash){
 class Element{constructor(){this.children=[];this.dataset={};this.attributes={};this.listeners={};}append(...children){this.children.push(...children);}add(child){this.children.push(child);}replaceChildren(...children){this.children=children;}setAttribute(key,value){this.attributes[key]=value;}addEventListener(type,fn){this.listeners[type]=fn;}focus(){}}
 const elements=new Map(['scenes','fullscreen','scene','scene-title','visual','lesson-reference','status','progress','previous','next','actions','viewer','opening-reveal'].map(id=>[id,new Element()]));
 const listeners={},location={hash,search:'?teach=1'};
 const buttons=()=>elements.get('actions').children.flatMap(group=>group.children).filter(element=>element.type==='button');
 const document={getElementById:id=>id==='opening-reveal'&&!elements.get('visual').innerHTML?.includes('id="opening-reveal"')?undefined:elements.get(id),createElement:()=>new Element(),querySelector:()=>null,addEventListener(){}};
 const window={addEventListener:(name,fn)=>{listeners[name]=fn;},scrollTo(){}};
 const source=fs.readFileSync(new URL('../course/prototypes/integrated-cases-player.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
 vm.runInNewContext(source,{document,window,location,history:{replaceState(_state,_title,hash){location.hash=hash;}},URLSearchParams,Option:class{constructor(label,value){this.label=label;this.value=value;}},scenes,initialState,sceneAliases,integratedCasesVisual,presentationLabels:{'integrated-cases':'16. Integrated cases'}});
 return {elements,document,go(id){location.hash=`#${id}`;listeners.hashchange();},click(key,value){const b=buttons().find(button=>button.dataset.choice===key&&button.dataset.value===String(value));assert.ok(b,`${key}=${value}`);b.onclick();},reveal(){elements.get('opening-reveal').listeners.click();}};
}

test('actual player changes acceptance and access without changing independent loads',()=>{
 const p=playerAt('#weather-paths'),html=()=>p.elements.get('visual').innerHTML;
 assert.match(html(),/60 MW/);assert.match(html(),/58 MW/);assert.match(html(),/83 MW/);
 p.click('acceptedRacks',900);assert.match(html(),/65 MW/);assert.match(html(),/58 MW/);assert.match(html(),/83 MW/);
 p.go('density-route');assert.match(html(),/Route blocked/);p.click('route','clear');assert.match(html(),/Route clear/);assert.match(html(),/126.24 kW/);
 p.go('weather-paths');assert.match(html(),/65 MW/);p.click('acceptedRacks',600);assert.match(html(),/60 MW/);
 p.go('density-route');assert.match(html(),/Route clear/);
 p.go('phase-choice');assert.doesNotMatch(html(),/Open A: 300 racks/);p.reveal();assert.match(html(),/Open A: 300 racks/);assert.match(html(),/aria-expanded="true"/);p.reveal();assert.doesNotMatch(html(),/Open A: 300 racks/);
});

test('all retired bookmarks reach their retained explanation and navigation stays complete',()=>{
 const p=playerAt('#outage-timeline');assert.equal(p.elements.get('scene').dataset.scene,'outage-brief');
 for(const [old,current]of Object.entries(sceneAliases)){p.go(old);assert.equal(p.elements.get('scene').dataset.scene,current);}
 p.go('watts-to-work');assert.equal(p.elements.get('next').disabled,true);assert.equal(p.elements.get('progress').textContent,'17 / 17');assert.match(p.document.title,/^16\. Integrated cases/);
 p.go('unknown');assert.equal(p.elements.get('previous').disabled,true);assert.equal(p.elements.get('progress').textContent,'1 / 17');
});
