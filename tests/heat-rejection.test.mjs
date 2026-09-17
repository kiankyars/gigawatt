import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {chillerBalance,operatingPoint,weatherDay,towerLedger,heatReuse,decisionFeedback} from '../course/prototypes/heat-rejection-model.js';
import {scenes,sceneAliases,initialState} from '../course/prototypes/heat-rejection-scenes.js';
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
 assert.equal(scenes[1].id,'abilene-cooling');
 assert.deepEqual(sceneAliases,{'two-ceilings':'hot-hour','reuse-interface':'heat-reuse'});
});
test('every scene and documented control state produces finite desktop and phone content',()=>{
 for(const scene of scenes){const states=[{...initialState}];for(const c of scene.controls||[])for(const [value]of c.options)states.push({...initialState,[c.key]:value});
  if(scene.id==='hot-hour')for(const condition of ['cool','hot'])for(const requestedITMW of [4,7.68,8])states.push({...initialState,condition,requestedITMW});
  if(scene.id==='approach-outdoors')for(const humidity of ['dry','humid'])for(const interfaceStep of [0,1,2,3])states.push({...initialState,humidity,interfaceStep});
  for(const state of states)for(const compact of [false,true]){const html=heatRejectionVisual(scene.id,state,compact);assert.ok(html.length>100);assert.doesNotMatch(html,/\b(?:undefined|NaN|Infinity)\b/);}
 }
});
test('hot-hour visual follows the requested load and retains both adequacy screens',()=>{
 const proposed=heatRejectionVisual('hot-hour',{...initialState,condition:'hot',requestedITMW:8});
 const fitted=heatRejectionVisual('hot-hour',{...initialState,condition:'hot',requestedITMW:7.68});
 assert.match(proposed,/10\.4\s*\/\s*10 MW/);assert.match(fitted,/10\s*\/\s*10 MW/);
 assert.match(fitted,/7\.68/);assert.match(fitted,/1\.92/);assert.doesNotMatch(fitted,/10\.4\s*\/\s*10 MW/);
});
test('temperature ladders reveal one interface at a time and humidity changes the final limit',()=>{
 for(const interfaceStep of [0,1,2,3]){
  const html=heatRejectionVisual('approach-outdoors',{...initialState,interfaceStep});
  const shown=[...html.matchAll(/data-approach-step="(\d+)"/g)].map(match=>Number(match[1]));
  assert.equal(shown.length,Math.min(interfaceStep+1,3)+interfaceStep+1);
  assert.ok(shown.every(step=>step<=interfaceStep));
  assert.equal([...html.matchAll(/class="h-temperature-stage h-unrevealed" aria-hidden="true"/g)].length,7-shown.length);
 }
 const dry=heatRejectionVisual('approach-outdoors',{...initialState,humidity:'dry',interfaceStep:3});
 const humid=heatRejectionVisual('approach-outdoors',{...initialState,humidity:'humid',interfaceStep:3});
 assert.match(dry,/data-approach-step="3">[\s\S]*?h-pass[^>]*><b>35°C/);
 assert.match(humid,/data-approach-step="3">[\s\S]*?h-fail[^>]*><b>41°C/);
});
test('water accounting keeps missing return evidence unresolved',()=>{
 const unknown=heatRejectionVisual('water-metrics',{...initialState,returnKnown:false});
 const known=heatRejectionVisual('water-metrics',{...initialState,returnKnown:true});
 assert.match(unknown,/unresolved/i);assert.doesNotMatch(known,/unresolved/i);
 for(const mineralStage of ['evaporate','purge','refill']){
  const visual=heatRejectionVisual('water-ledger',{...initialState,mineralStage});
  assert.doesNotMatch(visual,/C\s*=|B\s*=|C\s*[−-]\s*1|concentration ratio/i);
 }
 assert.notEqual(heatRejectionVisual('water-ledger',{...initialState,mineralStage:'evaporate'}),heatRejectionVisual('water-ledger',{...initialState,mineralStage:'purge'}));
});
test('closing decision feedback diagnoses both wrong paths and keeps the answer behind reveal',()=>{
 assert.equal(decisionFeedback('reduce').correct,true);assert.equal(decisionFeedback('full').correct,false);assert.equal(decisionFeedback('tower').correct,false);
 const hidden=heatRejectionVisual('heat-rejection-check',{...initialState,choice:'reduce'},false);assert.doesNotMatch(hidden,/Both limits pass|7\.68|1\.92/);assert.match(hidden,/data-plan="reduce" aria-pressed="true"/);
 const revealed=heatRejectionVisual('heat-rejection-check',{...initialState,choice:'reduce',revealed:true},false);assert.match(revealed,/Both limits pass/);assert.match(revealed,/1\.92/);assert.doesNotMatch(revealed,/data-plan=/);
});
test('chapter uses shared presenter chrome and the local attributed Abilene photo',()=>{
 const html=readFileSync(new URL('../course/prototypes/heat-rejection-format.html',import.meta.url),'utf8');assert.match(html,/src="slide-chrome.js"/);assert.match(html,/id="scenes"/);assert.match(html,/id="lesson-reference"/);
 const visual=heatRejectionVisual('abilene-cooling',initialState);assert.match(visual,/distribution-abilene-data-halls\.jpg/);assert.match(visual,/August 2025/);assert.match(visual,/crusoe\.ai/);
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
 Object.defineProperty(elements.get('visual'),'innerHTML',{get(){return this.html;},set(html){this.html=html;inline=[];for(const [,attrs]of html.matchAll(/<(?:button|input)\b([^>]*)>/g)){const element=new Element();for(const [,key,value]of attrs.matchAll(/([\w-]+)="([^"]*)"/g)){element.setAttribute(key,value);if(['id','type','value','min','max','step'].includes(key))element[key]=value;}inline.push(element);}}});
 const descendants=element=>element.children.flatMap(child=>[child,...descendants(child)]);
 const actions=()=>descendants(elements.get('actions'));
 const buttons=()=>actions().filter(element=>element.type==='button');
 const listeners={},location={hash,search:'?teach=1'};
 const document={getElementById:id=>elements.get(id)||[...inline,...actions()].find(element=>element.id===id||element.getAttribute('id')===id),createElement:()=>new Element(),querySelector:()=>null,querySelectorAll:selector=>{const attr=selector.slice(1,-1);return inline.filter(element=>element.getAttribute(attr)!==undefined);},addEventListener(){}};
 const window={addEventListener:(name,fn)=>{listeners[name]=fn;},scrollTo(){}};
 const source=readFileSync(new URL('../course/prototypes/heat-rejection-player.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
 vm.runInNewContext(source,{document,window,location,history:{replaceState(_state,_title,hash){location.hash=hash;}},matchMedia:()=>({matches:false,addEventListener(){}}),URLSearchParams,Option:class{constructor(label,value){this.label=label;this.value=value;}},scenes,sceneAliases,initialState,heatRejectionVisual,operatingPoint,presentationLabels:{'heat-rejection':'12. Heat rejection, climate and water'}});
 return {elements,document,go(id){location.hash=`#${id}`;listeners.hashchange();},click(key,value){const button=buttons().find(button=>button.dataset.choice===key&&button.dataset.value===String(value));assert.ok(button,`${key}=${value}`);button.onclick();},press(id){const button=document.getElementById(id);assert.ok(button,id);(button.onclick||button.listeners.click)();},input(id,value){const input=document.getElementById(id);assert.ok(input,id);input.value=String(value);const handle=input.oninput||input.listeners.input;assert.equal(typeof handle,'function');handle({target:input,currentTarget:input});}};
}

test('actual player connects weather and IT load controls and preserves them across navigation',()=>{
 const player=playerAt('#hot-hour'),html=()=>player.elements.get('visual').innerHTML;
 assert.match(html(),/9\.4\s*\/\s*10 MW/);
 const slider=player.document.getElementById('computing-power');assert.ok(slider);assert.equal(Number(slider.min),4);assert.equal(Number(slider.max),8);assert.equal(Number(slider.step),.01);
 player.click('condition','hot');assert.match(html(),/10\.4\s*\/\s*10 MW/);
 player.input('computing-power',7.68);assert.match(html(),/10\s*\/\s*10 MW/);assert.match(html(),/1\.92/);
 player.go('water-ledger');player.click('mineralStage','purge');player.go('hot-hour');assert.equal(Number(player.document.getElementById('computing-power').value),7.68);assert.match(html(),/10\s*\/\s*10 MW/);
 player.input('computing-power',8);player.press('fit-load');assert.equal(Number(player.document.getElementById('computing-power').value),7.68);assert.match(html(),/10\s*\/\s*10 MW/);
 player.click('condition','cool');player.press('fit-load');assert.equal(Number(player.document.getElementById('computing-power').value),8);assert.match(html(),/9\.4\s*\/\s*10 MW/);
 player.go('two-ceilings');assert.equal(player.elements.get('scene').dataset.scene,'hot-hour');
 player.go('reuse-interface');assert.equal(player.elements.get('scene').dataset.scene,'heat-reuse');
});
test('actual player advances and restarts the temperature reveal while retaining humidity',()=>{
 const player=playerAt('#approach-outdoors'),html=()=>player.elements.get('visual').innerHTML;
 assert.doesNotMatch(html(),/data-approach-step="[123]"/);
 for(const step of [1,2,3]){player.press('approach-next');assert.match(html(),new RegExp(`data-approach-step="${step}"`));}
 player.click('humidity','humid');assert.match(html(),/data-approach-step="3">[\s\S]*?h-fail[^>]*><b>41°C/);
 player.press('approach-next');assert.doesNotMatch(html(),/data-approach-step="[123]"/);assert.match(html(),/<b>28°C<\/b>/);
});
