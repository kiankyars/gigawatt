import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import {capacityLedger,capacityStage,presentValue,costComparison,usefulCost,upgradeScreen} from '../course/prototypes/capacity-model.js';
import {scenes,initialState,sources,learningContract,sceneAliases,resolveSceneId} from '../course/prototypes/capacity-scenes.js';
import {capacityVisual} from '../course/prototypes/capacity-visuals.js';
const near=(actual,expected,tolerance=1e-9)=>assert.ok(Math.abs(actual-expected)<tolerance,`${actual} ≈ ${expected}`);

test('the ledger reconciles shared IT and fixed facility overhead before taking the minimum',()=>{
 const m=capacityLedger();
 assert.deepEqual(m.ceilings.map(item=>item.value),[741,650,550,600,750,520]);
 assert.equal(m.racks,520);assert.deepEqual(m.binding,['accepted']);
 near(m.computeMW,52);near(m.itMW,57);near(m.siteMW,73.4);near(m.headroomMW,26.6);
 assert.equal(m.baseLoadFits,true);
 const max=capacityLedger({electricalMW:100,coolingMW:100,network:1000,space:1000,accepted:1000});
 assert.equal(max.racks,741);assert.ok(max.siteMW<=100);
 assert.ok((max.racks+1)*.1*1.2+5*1.2+5>100,'round down because the next whole rack exceeds the site limit');
});

test('upgrades expose successive and tied constraints instead of adding nominal capacities',()=>{
 assert.deepEqual(['current','acceptance','cooling','network'].map(stage=>capacityStage(stage).racks),[520,550,600,650]);
 assert.deepEqual(capacityStage('network').binding,['electrical','cooling']);
 const p={accepted:700,network:800,coolingMW:70};
 assert.equal(capacityLedger({...p,electricalMW:80}).racks,650);
 assert.equal(capacityLedger({...p,electricalMW:80,coolingMW:80}).racks,700);
 assert.throws(()=>capacityStage('unknown'),RangeError);
});

test('every feasible rack count respects all six limits and monotonic upgrades cannot reduce it',()=>{
 for(const accepted of [0,100,520,550,650,700,800])for(const coolingMW of [5,60,70,80])for(const electricalMW of [5,70,80]){
  const m=capacityLedger({accepted,coolingMW,electricalMW});
  assert.ok(m.ceilings.every(row=>m.racks<=row.value));
  assert.ok(m.itMW<=coolingMW+1e-8);assert.ok(m.itMW<=electricalMW+1e-8);assert.ok(m.siteMW<=100+1e-8);
  assert.ok(capacityLedger({accepted:accepted+1,coolingMW,electricalMW}).racks>=m.racks);
 }
 assert.equal(capacityLedger({siteMW:1}).baseLoadFits,false,'fixed and shared loads may be infeasible even with no compute racks');
 assert.equal(capacityLedger({siteMW:1}).racks,0);
 for(const input of [{rackMW:0},{coolingMW:-1},{accepted:1.5},{network:NaN},{overheadFactor:.9}])assert.throws(()=>capacityLedger(input),RangeError);
});

test('present value puts residual receipts and recurring costs at their stated year ends',()=>{
 const m=costComparison();
 near(m.recurringFactor,1/1.08+1/1.08**2+1/1.08**3);
 near(m.ownPV,34.0705177056343);near(m.contractPV,28.348066859726664);near(m.savingMillions,5.7224508459076375);
 near(m.residualPV,5/1.08**3);assert.equal(m.energyMillions,4);
 near(costComparison({residualMillions:0}).ownPV-m.ownPV,m.residualPV);
 assert.equal(costComparison({rate:0}).ownPV,36);assert.equal(costComparison({rate:0}).contractPV,33);
 assert.equal(presentValue(20,0,.08),20);near(presentValue(-5,3,.08),-m.residualPV);
 for(const options of [{years:0},{years:1.5},{rate:-1},{energyPrice:NaN}])assert.throws(()=>costComparison(options),RangeError);
 assert.throws(()=>presentValue(NaN,1),RangeError);
});

test('energy is charged once and higher flat tariffs change only the exposed ownership cost',()=>{
 const base=costComparison();
 for(const energyPrice of [80,120,160]){
  const m=costComparison({energyPrice});
  assert.equal(m.energyMillions,50000*energyPrice/1e6);
  near(m.contractPV,base.contractPV);
  near(m.ownPV-base.ownPV,(m.energyMillions-base.energyMillions)*base.recurringFactor);
 }
});

test('fixed present cost divided by lower accepted output raises the unit cost by 25 percent',()=>{
 const m=costComparison();
 for(const costMillions of [m.ownPV,m.contractPV]){
  const full=usefulCost({costMillions,resultsMillions:10}),reduced=usefulCost({costMillions,resultsMillions:8});
  near(reduced.perResult/full.perResult,1.25);
  near(full.perResult*full.resultsMillions,costMillions);
 }
 assert.throws(()=>usefulCost({costMillions:10,resultsMillions:0}),RangeError);
 assert.throws(()=>usefulCost({costMillions:-1}),RangeError);
});

test('delivery time reverses the intervention screen; demand changes realized unit cost',()=>{
 const base=upgradeScreen();
 assert.equal(base.network.results,1920000);assert.equal(base.cooling.results,2400000);
 near(base.network.perResult,25/12);near(base.cooling.perResult,2.5);assert.equal(base.preferred,'network');
 const now=upgradeScreen({coolingDelay:0});assert.equal(now.cooling.results,3600000);near(now.cooling.perResult,5/3);assert.equal(now.preferred,'cooling');
 near(base.equalCostDelay,.6);assert.equal(upgradeScreen({coolingDelay:.6}).preferred,'tie');
 assert.equal(upgradeScreen({coolingDelay:.59}).preferred,'cooling');assert.equal(upgradeScreen({coolingDelay:.61}).preferred,'network');
 for(const coolingDelay of [0,1,2]){
  const all=upgradeScreen({coolingDelay}),half=upgradeScreen({coolingDelay,demand:.5});
  assert.equal(half.preferred,all.preferred);
  for(const key of ['network','cooling']){near(half[key].results,all[key].results/2);near(half[key].perResult,all[key].perResult*2);}
 }
 assert.equal(upgradeScreen({coolingDelay:3}).cooling.perResult,null,'no output yields no finite screening ratio');
 assert.equal(upgradeScreen({demand:0}).preferred,'none');
 for(const options of [{coolingDelay:-1},{demand:1.01},{demand:NaN},{hoursPerYear:0}])assert.throws(()=>upgradeScreen(options),RangeError);
});

function statesFor(scene){
 let states=[{...initialState}];
 for(const group of scene.controls||[])states=states.flatMap(state=>group.options.map(([value])=>({...state,[group.key]:value})));
 if(scene.id==='delivery-window')states=states.flatMap(state=>[state,...['network','cooling'].flatMap(upgradeChoice=>[false,true].map(showUpgrade=>({...state,upgradeChoice,showUpgrade})))]);
 if(['ownership-boundary','cash-flow-timing','cost-per-result'].includes(scene.id))states=states.flatMap(state=>[80,120,160].flatMap(energyPrice=>[0,.08].map(discountRate=>({...state,energyPrice,discountRate}))));
 if(scene.id==='evidence-decision')states=['','plan','operating'].flatMap(evidenceClaim=>['','power','output','cost'].flatMap(evidenceNeed=>[false,true].map(showEvidence=>({...initialState,evidenceClaim,evidenceNeed,showEvidence}))));
 return states;
}

test('all scenes, all independent control combinations and all decision feedback states render',()=>{
 assert.equal(scenes.length,15);assert.equal(new Set(scenes.map(scene=>scene.id)).size,15);
 assert.deepEqual([...new Set(scenes.map(scene=>scene.objective))].sort(),['D15.1','D15.2','D15.3','D15.4','D15.5']);
 assert.equal(Object.keys(learningContract).length,6);
 for(const scene of scenes){
  assert.match(scene.reference,/^d15-/);assert.ok(scene.explanation[0].length>80);
  for(const group of scene.controls||[])assert.ok(group.options.some(([value])=>value===initialState[group.key]));
  for(const state of statesFor(scene)){
   const html=capacityVisual(scene.id,state);assert.ok(html.length>300);assert.doesNotMatch(html,/NaN|undefined|Infinity/);
   assert.doesNotMatch(html,/\b(?:synthetic|illustrative|not a benchmark)\b/,'qualifications belong in metadata, decisive assumptions remain visible');
   for(const [,src]of html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g))assert.ok(fs.existsSync(new URL(src,new URL('../course/prototypes/',import.meta.url))));
  }
 }
 assert.throws(()=>capacityVisual('missing',initialState),/Unknown capacity scene/);
});

test('merged scenes retain old navigation links',()=>{
 assert.deepEqual(sceneAliases,{'power-boundaries':'site-headroom','capacity-ledger':'next-constraint','present-cost':'cash-flow-timing','upgrade-decision':'delivery-window'});
 for(const [previous,current]of Object.entries(sceneAliases))assert.equal(resolveSceneId(previous),current);
 for(const scene of scenes)assert.equal(resolveSceneId(scene.id),scene.id);
 assert.equal(resolveSceneId('#present-cost'),'cash-flow-timing');
 assert.equal(resolveSceneId('%70resent-cost'),'cash-flow-timing');
 assert.equal(resolveSceneId('%not-encoded'),scenes[0].id);
 assert.equal(resolveSceneId('missing'),scenes[0].id);
});

test('the delivery prediction withholds the comparison and reveals the current proposal calculation',()=>{
 for(const coolingDelay of[0,1,2])for(const demand of[1,.5])for(const upgradeChoice of['network','cooling']){
  const state={...initialState,coolingDelay,demand,upgradeChoice};
  const hidden=capacityVisual('delivery-window',state);
  assert.doesNotMatch(hidden,/data-upgrade-preferred|class="k-screen-results"|\$\d+\.\d+ \/ result/);
  const shown=capacityVisual('delivery-window',{...state,showUpgrade:true});
  const m=upgradeScreen({coolingDelay,demand});
  assert.match(shown,new RegExp(`data-upgrade-preferred="${m.preferred}"`));
  for(const option of[m.network,m.cooling]){
   assert.ok(shown.includes(`${(option.results/1e6).toFixed(2)}m extra results`));
   assert.ok(shown.includes(`$${option.perResult.toFixed(2)} / result`));
  }
 }
 assert.doesNotMatch(capacityVisual('delivery-window',{...initialState,showUpgrade:true}),/data-upgrade-preferred/,'reveal without a prediction cannot disclose the result');
});

test('the evidence task gates guidance on both selections and distinguishes plans from measured operation',()=>{
 const scene=scenes.find(scene=>scene.id==='evidence-decision');
 for(const state of statesFor(scene)){
  const html=capacityVisual(scene.id,state);
  if(!(state.evidenceClaim&&state.evidenceNeed&&state.showEvidence)){
   assert.doesNotMatch(html,/data-evidence-claim-status|class="k-evidence-feedback"/);
  }else{
   const status=state.evidenceClaim==='plan'?'supported':'unsupported';
   assert.match(html,new RegExp(`data-evidence-claim-status="${status}"`));
   const feedback=html.match(/<p data-evidence-need="[^"]+">([^<]+)<\/p>/)?.[1];assert.ok(feedback);
   if(state.evidenceNeed==='power'){assert.match(feedback,/meter/i);assert.match(feedback,/boundary/i);}
   if(state.evidenceNeed==='output'){assert.match(feedback,/quality/i);assert.match(feedback,/(?:time|deadline)/i);}
   if(state.evidenceNeed==='cost'){assert.match(feedback,/cost/i);assert.match(feedback,/results/i);assert.match(feedback,/horizon/i);}
  }
 }
});

test('Abilene statements retain dates, distinct projects and the unknown operating boundary',()=>{
 const ledger=capacityVisual('abilene-ledger',initialState),campus=capacityVisual('abilene-campus',initialState),scope=capacityVisual('separate-campuses',initialState);
 for(const text of ['18 Mar 2025','30 Sep 2025','Sep 2026','Planned campus','Energized','Workloads running','Delivered'])assert.ok(ledger.includes(text),text);
 for(const url of [sources.plan,sources.live,sources.oracle])assert.ok(ledger.includes(url));
 assert.match(campus,/distribution-abilene-data-halls.jpg/);assert.match(campus,/15 July 2026/);
 assert.match(scope,/9 June 2026/);assert.match(scope,/1.2 GW project/);assert.match(scope,/900 MW project/);assert.match(scope,/Oracle/);assert.match(scope,/Microsoft/);
 assert.match(ledger,/Accepted service MW · metered IT demand · accepted results/);
 const entry=JSON.parse(fs.readFileSync(new URL('../course/assets/references/provenance.json',import.meta.url))).find(item=>item.file==='distribution-abilene-data-halls.jpg');
 assert.ok(entry);assert.equal(entry.publisher,'Oracle');assert.match(entry.sha256,/^[a-f0-9]{64}$/);
 assert.ok(scenes.find(scene=>scene.id==='cash-flow-timing').sources.includes(sources.nist));
 assert.ok(scenes.find(scene=>scene.id==='delivery-window').sources.includes(sources.gao));
});

function playerAt(hash){
 class Element{
  constructor(){this.children=[];this.dataset={};this.attributes={};this.listeners={};}
  append(...children){this.children.push(...children);}add(child){this.children.push(child);}replaceChildren(...children){this.children=children;}
  setAttribute(key,value){this.attributes[key]=value;}getAttribute(key){return this.attributes[key];}focus(){}addEventListener(name,fn){this.listeners[name]=fn;}
 }
 const elements=new Map(['scenes','fullscreen','scene','scene-title','visual','lesson-reference','status','progress','previous','next','actions','viewer'].map(id=>[id,new Element()]));
 let inline=[];
 Object.defineProperty(elements.get('visual'),'innerHTML',{get(){return this.html;},set(html){this.html=html;inline=[];for(const [,attrs,label]of html.matchAll(/<button\b([^>]*)>([\s\S]*?)<\/button>/g)){const button=new Element();button.label=label;for(const [,key,value]of attrs.matchAll(/([\w-]+)="([^"]*)"/g))button.setAttribute(key,value);inline.push(button);}}});
 const listeners={},location={hash,search:'?teach=1'};
 const buttons=()=>elements.get('actions').children.flatMap(group=>group.children).filter(element=>element.type==='button');
 const document={getElementById:id=>elements.get(id)||inline.find(button=>button.getAttribute('id')===id),createElement:()=>new Element(),querySelector:()=>null,querySelectorAll:selector=>{const attr=selector.match(/\[([^\]]+)\]/)?.[1];return inline.filter(button=>button.getAttribute(attr)!==undefined);},addEventListener(){}};
 const window={addEventListener:(name,fn)=>{listeners[name]=fn;},scrollTo(){}};
 const source=fs.readFileSync(new URL('../course/prototypes/capacity-player.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
 vm.runInNewContext(source,{document,window,location,history:{replaceState(_state,_title,hash){location.hash=hash;}},URLSearchParams,Option:class{constructor(label,value){this.label=label;this.value=value;}},scenes,initialState,sceneAliases,resolveSceneId,capacityVisual,presentationLabels:{capacity:'15. Capacity, cost and system decisions'}});
 return {elements,buttons,document,go(id){location.hash=`#${id}`;listeners.hashchange();},click(key,value){const button=buttons().find(button=>button.dataset.choice===key&&button.dataset.value===String(value));assert.ok(button,`${key}=${value}`);button.onclick();},choose(attr,value){const button=inline.find(button=>button.getAttribute(`data-${attr}`)===value);assert.ok(button);button.onclick();},reveal(id){document.getElementById(id).listeners.click();}};
}

test('the player preserves cost assumptions across the cash-flow and accepted-output views',()=>{
 const player=playerAt('#energy-exposure'),html=()=>player.elements.get('visual').innerHTML;
 player.click('energyPrice',160);
 player.go('ownership-boundary');assert.match(html(),/\$8(?:\.00)?m/);
 player.go('cash-flow-timing');player.click('discountRate',0);assert.match(html(),/\$48\.0m/);assert.match(html(),/\$33\.0m/);
 player.go('cost-per-result');player.click('outputMillions',8);assert.match(html(),/\$6\.00\/result/);assert.match(html(),/\$4\.13\/result/);
 player.go('cash-flow-timing');player.click('discountRate',.08);
 const m=costComparison({energyPrice:160,rate:.08});
 player.go('cost-per-result');assert.ok(html().includes(`$${(m.ownPV/8).toFixed(2)}/result`));assert.ok(html().includes(`$${(m.contractPV/8).toFixed(2)}/result`));
 player.go('ownership-boundary');assert.match(html(),/\$8(?:\.00)?m/);
});

test('the player clears stale predictions when delivery or demand changes and preserves other controls',()=>{
 const player=playerAt('#delivery-window'),html=()=>player.elements.get('visual').innerHTML;
 const selected=key=>player.buttons().filter(button=>button.dataset.choice===key&&button.attributes['aria-pressed']==='true').map(button=>button.dataset.value);
 const hidden=()=>{assert.doesNotMatch(html(),/data-upgrade-preferred|data-upgrade-choice="[^"]+" aria-pressed="true"/);};
 hidden();assert.deepEqual(selected('coolingDelay'),['1']);assert.deepEqual(selected('demand'),['1']);
 player.choose('upgrade-choice','network');player.reveal('upgrade-reveal');assert.match(html(),/data-upgrade-preferred="network"/);
 player.click('coolingDelay',0);hidden();assert.deepEqual(selected('demand'),['1']);
 player.choose('upgrade-choice','cooling');player.reveal('upgrade-reveal');assert.match(html(),/data-upgrade-preferred="cooling"/);
 player.click('demand',.5);hidden();assert.deepEqual(selected('coolingDelay'),['0']);
 player.choose('upgrade-choice','cooling');player.reveal('upgrade-reveal');assert.match(html(),/\$3\.33 \/ result/);
 player.go('tied-constraints');player.click('tieUpgrade','electrical');assert.match(html(),/650 racks/);player.click('tieUpgrade','both');assert.match(html(),/700 racks/);
 player.go('upgrade-decision');assert.equal(player.elements.get('scene').dataset.scene,'delivery-window');assert.match(html(),/data-upgrade-preferred="cooling"/);
 assert.deepEqual(selected('coolingDelay'),['0']);assert.deepEqual(selected('demand'),['0.5']);
 player.choose('upgrade-choice','network');assert.doesNotMatch(html(),/data-upgrade-preferred/);player.reveal('upgrade-reveal');assert.match(html(),/data-upgrade-preferred="cooling"/);
 for(const [previous,current]of Object.entries(sceneAliases)){player.go(previous);assert.equal(player.elements.get('scene').dataset.scene,current);}
 assert.match(player.document.title,/^15\. Capacity, cost and system decisions/);
});

test('the player requires both evidence selections and updates the feedback for each changed selection',()=>{
 const player=playerAt('#evidence-decision'),html=()=>player.elements.get('visual').innerHTML;
 player.choose('evidence-claim','plan');assert.match(html(),/id="evidence-reveal"[^>]*disabled/);assert.doesNotMatch(html(),/data-evidence-claim-status/);
 player.choose('evidence-need','power');player.reveal('evidence-reveal');assert.match(html(),/data-evidence-claim-status="supported"/);
 player.choose('evidence-claim','operating');assert.doesNotMatch(html(),/data-evidence-claim-status/);player.reveal('evidence-reveal');assert.match(html(),/data-evidence-claim-status="unsupported"/);
 for(const need of['output','cost']){player.choose('evidence-need',need);assert.doesNotMatch(html(),/data-evidence-claim-status/);player.reveal('evidence-reveal');assert.match(html(),new RegExp(`<p data-evidence-need="${need}">`));}
 player.choose('evidence-claim','plan');assert.doesNotMatch(html(),/data-evidence-claim-status/);player.reveal('evidence-reveal');
 player.go('abilene-ledger');player.go('evidence-decision');assert.match(html(),/data-evidence-claim-status="supported"/);assert.match(html(),/<p data-evidence-need="cost">/);
});
