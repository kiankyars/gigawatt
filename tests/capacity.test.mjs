import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {rentalRevenue,electricityPerBilledHour,h100Ranges} from '../course/prototypes/capacity-model.js';
import {scenes,initialState,sceneAliases,resolveSceneId} from '../course/prototypes/capacity-scenes.js';
import {capacityVisual} from '../course/prototypes/capacity-visuals.js';
const near=(a,b)=>assert.ok(Math.abs(a-b)<1e-8);
test('billable occupancy changes merchant revenue but not the committed obligation',()=>{
 const base=rentalRevenue();assert.equal(base.availableHours,8970240);assert.equal(base.committed,22425600);assert.equal(base.market,17940480);near(base.breakEven,.625);
 near(rentalRevenue({occupancy:.625}).market,base.committed);assert.equal(rentalRevenue({occupancy:.8}).market,28704768);
 for(const occupancy of[0,.2,.5,.625,.8,1]){const m=rentalRevenue({occupancy});near(m.billedHours,m.availableHours*occupancy);assert.equal(m.committed,base.committed);}
 assert.equal(rentalRevenue({occupancy:0}).market,0);
 assert.equal(rentalRevenue({marketRate:2}).breakEven,1.25,'a lower merchant price cannot equal a fully paid higher commitment even at full occupancy');
 for(const input of[{gpus:1.5},{gpus:0},{hours:NaN},{occupancy:-.1},{occupancy:1.1},{marketRate:0}])assert.throws(()=>rentalRevenue(input),RangeError);
});
test('energy divides calendar-hour consumption by rented hours without dropping idle consumption',()=>{
 near(electricityPerBilledHour(),.084);near(electricityPerBilledHour({tariffPerMWh:160}),.168);near(electricityPerBilledHour({occupancy:.4}),.104);
 near(electricityPerBilledHour({occupancy:1}),.08);
 near(electricityPerBilledHour({idleSiteKWPerGPU:0}),.08);
 near(electricityPerBilledHour({idleSiteKWPerGPU:1}),.1);
 assert.throws(()=>electricityPerBilledHour({idleSiteKWPerGPU:-1}),RangeError);
 assert.throws(()=>electricityPerBilledHour({occupancy:0}),RangeError);assert.throws(()=>electricityPerBilledHour({occupancy:1.1}),RangeError);
});
test('market series carries explicit historical observation periods and ranges',()=>{
 assert.deepEqual(h100Ranges.map(p=>[p.period,p.low,p.high]),[['Oct 2025',1.45,1.95],['Jan 2026',1.5,2.05],['Apr 2026',2.1,2.7]]);
 assert.match(capacityVisual('rental-market',initialState),/Oct 2025/);
 assert.match(capacityVisual('rental-market',initialState),/Apr 2026/);
});
test('new scenes have a coherent business scope and all source assets exist',()=>{
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);assert.equal(scenes.length,18);
 assert.deepEqual([...new Set(scenes.map(s=>s.objective))].sort(),['D15.1','D15.2','D15.3','D15.4','D15.5']);
 for(const scene of scenes)for(const occupancy of[.5,.625,.8]){
  const html=capacityVisual(scene.id,{occupancy});assert.doesNotMatch(html,/undefined|NaN|Infinity/);
  for(const[,src]of html.matchAll(/<img[^>]+src="([^"]+)"/g))assert.ok(fs.existsSync(new URL(src,new URL('../course/prototypes/',import.meta.url))));
 }
 assert.throws(()=>capacityVisual('missing',initialState));
 const all=scenes.map(s=>capacityVisual(s.id,initialState)).join('');assert.doesNotMatch(all,/accepted paths|cost per accepted result|Spare site power/i);
});
test('retired bookmarks lead to the corresponding new business topic',()=>{
 for(const[before,after]of Object.entries(sceneAliases)){assert.equal(resolveSceneId('#'+before),after);assert.ok(scenes.some(s=>s.id===after));}
 assert.equal(resolveSceneId('%bad'),scenes[0].id);
});
test('Abilene schedule comparison distinguishes the forecast milestone from reported delivery',()=>{
 const html=capacityVisual('abilene-ledger',initialState);assert.match(html,/1H 2025/);assert.match(html,/mid-2026/);assert.match(html,/75%/);assert.match(html,/Construction complete mid-2026/);assert.match(html,/capacity delivered/);
 assert.doesNotMatch(html,/900 MW|Microsoft|accepted results/);
});
test('player keeps exactly one occupancy button selected and preserves it through navigation',()=>{
 class Element{constructor(){this.children=[];this.dataset={};this.attributes={};}append(...v){this.children.push(...v);}add(v){this.children.push(v);}replaceChildren(){this.children=[];}setAttribute(k,v){this.attributes[k]=v;}focus(){}}
 const elements=new Map(['scenes','fullscreen','scene','scene-title','visual','lesson-reference','status','progress','previous','next','actions','viewer'].map(id=>[id,new Element()]));
 const events={},location={hash:'#billable-occupancy',search:'?teach=1'};
 const document={getElementById:id=>elements.get(id),createElement:()=>new Element(),querySelector:()=>null,addEventListener(){}};
 vm.runInNewContext(fs.readFileSync(new URL('../course/prototypes/capacity-player.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,''),{document,window:{addEventListener:(k,v)=>events[k]=v,scrollTo(){}},location,history:{replaceState(_a,_b,h){location.hash=h;}},URLSearchParams,Option:class{},scenes,initialState,resolveSceneId,capacityVisual,presentationLabels:{}});
 const buttons=()=>elements.get('actions').children.flatMap(g=>g.children).filter(x=>x.type==='button');
 buttons().find(b=>b.dataset.value==='0.8').onclick();assert.equal(buttons().filter(b=>b.attributes['aria-pressed']==='true').length,1);assert.match(elements.get('visual').innerHTML,/28.70/);
 location.hash='#contract-tenor';events.hashchange();location.hash='#billable-occupancy';events.hashchange();assert.match(elements.get('visual').innerHTML,/28.70/);
});
