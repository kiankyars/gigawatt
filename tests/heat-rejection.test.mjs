import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import {chillerBalance,operatingPoint,weatherDay,towerLedger,heatReuse,decisionFeedback} from '../course/prototypes/heat-rejection-model.js';
import {scenes,initialState} from '../course/prototypes/heat-rejection-scenes.js';
import {heatRejectionVisual} from '../course/prototypes/heat-rejection-visuals.js';
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} != ${b}`);
test('chiller balances separate compressor COP from plant COP',()=>{
 const m=chillerBalance();close(m.condenserMW,12);close(m.compressorCOP,5);close(m.plantCOP,4);close(m.plantInputMW,2.5);
 assert.throws(()=>chillerBalance({compressorMW:0}),RangeError);
});
test('hot-hour thermal adequacy does not imply electrical adequacy',()=>{
 const hot=operatingPoint();assert.equal(hot.thermalFits,true);assert.equal(hot.electricalFits,false);close(hot.totalMW,10.4);close(hot.feasibleMW,7.68);
 const fitted=operatingPoint({requestedITMW:hot.feasibleMW});close(fitted.totalMW,10);close(fitted.coolingMW,1.92);assert.ok(fitted.thermalFits&&fitted.electricalFits);
 const cool=operatingPoint({condition:'cool'});close(cool.totalMW,9.4);close(cool.electricalMW,9.6/1.125);assert.ok(cool.thermalFits&&cool.electricalFits);
});
test('weather bins integrate the dispatched power without averaging away the peak',()=>{
 const m=weatherDay();close(m.itMWh,188.16);close(m.coolingMWh,35.04);close(m.otherMWh,9.6);close(m.facilityMWh,232.8);
 for(const bin of m.bins){const p=operatingPoint({condition:bin.condition,requestedITMW:bin.itMW});assert.ok(p.electricalFits&&p.thermalFits);}
});
test('tower balances conserve water and solids as concentration changes',()=>{
 for(const cycles of [3,5]){const m=towerLedger({cycles});close(m.makeupM3,m.evaporationM3+m.blowdownM3);close(m.makeupM3,cycles*m.blowdownM3);close(m.evaporationM3,100);}
 const m=towerLedger();close(m.blowdownM3,25);close(m.makeupM3,125);close(m.intakeLitresPerKWh,1.25);close(m.consumptionLitresPerKWh,1);close(m.energyRatio,1.2);
 close(towerLedger({cycles:3}).makeupM3,150);assert.equal(towerLedger({returnKnown:false}).consumptionM3,null);assert.equal(towerLedger({returnKnown:false}).consumptionLitresPerKWh,null);
 assert.throws(()=>towerLedger({cycles:1}),RangeError);
});
test('heat reuse is limited by receiver power and hours',()=>{
 const m=heatReuse();close(m.acceptedMWh,12);close(m.generatedMWh,96);close(m.remainingMWh,84);close(m.acceptedFraction,.125);
 const closed=heatReuse({receiverHours:0});close(closed.acceptedMWh,0);close(closed.remainingMWh,96);
 close(heatReuse({receiverMW:9,receiverHours:24}).acceptedMWh,96);assert.throws(()=>heatReuse({receiverHours:25}),RangeError);
});
test('chapter covers all D11 objectives and preserves original outdoor deep links',()=>{
 assert.equal(scenes.length,18);assert.equal(new Set(scenes.map(s=>s.id)).size,18);
 for(const id of ['rejection','weather','approach-outdoors','plant-options'])assert.ok(scenes.some(s=>s.id===id));
 for(let i=1;i<=5;i++)assert.ok(scenes.some(s=>s.objective===`D11.${i}`));
 assert.equal(scenes.at(-1).pedagogical_role,'transfer');assert.ok(scenes.find(s=>s.id==='abilene-cooling').sources[0].includes('crusoe.ai'));
});
test('every scene and documented control state produces finite desktop and phone content',()=>{
 for(const scene of scenes){const states=[{...initialState}];for(const c of scene.controls||[])for(const [value]of c.options)states.push({...initialState,[c.key]:value});
  for(const state of states)for(const compact of [false,true]){const html=heatRejectionVisual(scene.id,state,compact);assert.ok(html.length>100);assert.doesNotMatch(html,/\b(?:undefined|NaN|Infinity)\b/);}
 }
});
test('closing decision feedback diagnoses both wrong paths and keeps the answer behind reveal',()=>{
 assert.equal(decisionFeedback('reduce').correct,true);assert.equal(decisionFeedback('full').correct,false);assert.equal(decisionFeedback('tower').correct,false);
 const hidden=heatRejectionVisual('heat-rejection-check',{...initialState,choice:'reduce'},false);assert.doesNotMatch(hidden,/Both limits pass/);assert.match(hidden,/data-plan="reduce" aria-pressed="true"/);
 const revealed=heatRejectionVisual('heat-rejection-check',{...initialState,choice:'reduce',revealed:true},false);assert.match(revealed,/Both limits pass/);assert.match(revealed,/1\.92/);assert.doesNotMatch(revealed,/data-plan=/);
});
test('chapter uses shared presenter chrome and the local attributed Abilene photo',()=>{
 const html=readFileSync(new URL('../course/prototypes/heat-rejection-format.html',import.meta.url),'utf8');assert.match(html,/src="slide-chrome.js"/);assert.match(html,/id="scenes"/);assert.match(html,/id="lesson-reference"/);
 const visual=heatRejectionVisual('abilene-cooling',initialState);assert.match(visual,/distribution-abilene-data-halls\.jpg/);assert.match(visual,/August 2025/);assert.match(visual,/crusoe\.ai/);
});
