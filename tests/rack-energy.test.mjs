import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { rackLedger, dcPlanes, migrationDecision } from '../course/prototypes/rack-energy-model.js';
import { scenes as rackScenes, dcScenes, allScenes as scenes, initialState, defaults, decks, resolveRackEnergyScene } from '../course/prototypes/rack-energy-scenes.js';
import { acdcConductorModel, acdcWaveModel } from '../course/web/reader-models.js';
import { createElectricalVisuals } from '../course/web/electrical-renderer.js';
import { createPresentationRenderers } from '../course/web/presentation-renderers.js';
import { renderEnergyConnections } from '../course/prototypes/rack-buffer-review.js';
import { rackVisual, supplementalVisual, escapeHTML } from '../course/prototypes/rack-energy-visuals.js';
const close=(actual,expected)=>assert.ok(Math.abs(actual-expected)<1e-8,`${actual} versus ${expected}`);

test('shared sample initializes its shared visual factory after the reveal state exists',()=>{
  const data=readFileSync(new URL('../course/expansion/sample-presentation.json',import.meta.url),'utf8');
  const script=readFileSync(new URL('../course/web/presentation.js',import.meta.url),'utf8').split('function validState')[0];
  assert.doesNotThrow(()=>vm.runInNewContext(script,{
    document:{getElementById:()=>({textContent:data}),body:{dataset:{view:'teach'}}},
    location:{hash:'',search:''},URLSearchParams,crypto:{randomUUID:()=> 'test'},
    createPresentationRenderers,acdcConductorModel
  }));
});

test('the rack account conserves energy and the changed parallel branch skips processor regulators',()=>{
  const a=rackLedger(),b=rackLedger({auxiliaryKW:18});
  close(a.inputKW,a.processorKW+a.auxiliaryKW+a.regulatorLossKW+a.shelfLossKW);
  close(b.inputKW-a.inputKW,6/0.97);
  close(a.regulatorLossKW,b.regulatorLossKW);
  assert.throws(()=>rackLedger({auxiliaryKW:-1}),RangeError);
});
test('DC comparison holds receiving-end power fixed at both planes',()=>{
  const a=dcPlanes();assert.equal(a.lowAmps,2000);assert.equal(a.highAmps,125);
  assert.equal(a.lowAmps*50,a.highAmps*800);
});
test('retrofit choice changes with deadline while the electrical account remains fixed',()=>{
  const full=migrationDecision(),reduced=migrationDecision({rackKW:110}),late=migrationDecision({allocationKW:260}),later=migrationDecision({allocationKW:260,deadlineWeeks:8});
  assert.equal(full.inputKW,253);assert.equal(full.powerPass,false);
  close(reduced.inputKW,232.16666666666669);assert.equal(reduced.powerPass,true);assert.equal(reduced.schedulePass,true);
  assert.equal(late.powerPass,true);assert.equal(late.schedulePass,false);
  assert.equal(later.schedulePass,true);assert.equal(later.inputKW,late.inputKW);
  assert.throws(()=>migrationDecision({rackKW:100}),RangeError);
});
test('chapter sequence motivates architecture and follows both directions of changing load',()=>{
  assert.equal(new Set(scenes.map(scene=>scene.id)).size,scenes.length);
  const preview=scenes.findIndex(s=>s.id==='dc-architecture-preview');
  assert.equal(scenes[preview+1].id,'conversion-in-rack');
  const rise=scenes.findIndex(s=>s.id==='source-handoff');
  assert.equal(scenes[rise+1].id,'source-ramp-down');
  assert.equal(scenes[rise+2].id,'bbu-hardware');
});
test('a slower downward ramp doubles stored energy without changing peak charging power',()=>{
  const scene=scenes.find(s=>s.id==='source-ramp-down');
  for(const compact of [false,true])for(const [response,energy] of [[0.2,4],[0.4,8]]){
    const html=rackVisual(scene,{...initialState,response},compact).markup;
    assert.ok(html.includes(`${energy} kJ to absorb`));
    assert.ok(html.includes(`40 kW peak charging · ${energy} kJ of room`));
    assert.ok(html.includes('Power above the new GPU load'));
    assert.ok(html.includes('Full or charge-limited'));
  }
});
test('shared renderers cover all scenes and changed states without missing quantities',()=>{
  let state={...initialState},scene;
  const common={getState:()=>state,escapeHTML,fmt:(v,d=0)=>v.toLocaleString('en-US',{maximumFractionDigits:d})};
  const sample=createPresentationRenderers({...common,defaults,getStep:()=>scene,isRevealed:()=>true,acdcConductorModel});
  const electrical=createElectricalVisuals({...common,acdcWaveModel});
  for(const changed of [{},{resistance:10,phases:1,location:'rack',response:0.4,failed:2,rest:0.2,reveal:true,auxiliaryKW:18,volts:400,cycleDegrees:270,voltageView:'pairs',converterView:'heat',rackKW:110,deadlineWeeks:8,decision:'upgrade',migrationReveal:true}]){
    state={...initialState,...changed};
    for(scene of scenes){
      let html;
      if(scene.kind==='rack')for(const compact of [false,true]){html=rackVisual(scene,state,compact).markup;assert.doesNotMatch(html,/undefined|NaN/,scene.id);}
      else if(scene.kind==='800v')html=({intro:sample.intro,copper:sample.copper,current:sample.current,loss:sample.loss,'conversion-supply':sample.conversionSupply,'converter-heat':sample.conversionLoss,'source-figure':sample.sourceFigure}[scene.sourceKind]||(['dc-basics','ac-basics','three-phase','voltage-basis'].includes(scene.sourceKind)?()=>electrical.electricalVisual(scene.sourceKind):()=>sample.architecture(scene.sourceKind)))();
      else html=supplementalVisual(scene,state);
      assert.ok(html.length>100,scene.id);assert.doesNotMatch(html,/undefined|NaN/,scene.id);
    }
  }
});

test('DC architecture motivates the supply equipment and preserves both rack-bus choices',()=>{
  const ids=dcScenes.map(scene=>scene.id);
  assert.ok(!ids.includes('dc-voltage-planes'));
  assert.ok(!ids.includes('ac-dc-converter-loss'));
  const supplyIndex=ids.indexOf('ac-dc-ledger');
  for(const id of ['conversion-in-rack','conversion-in-sidecar','conversion-farther-upstream','rack-bus-choices'])assert.ok(ids.indexOf(id)<supplyIndex,id);
  assert.equal(ids[supplyIndex+1],'green-zurich-west');
  assert.ok(!ids.includes('dc-architecture-changes'));
  assert.ok(ids.includes('ocp-power-architectures'));
  const busScene=dcScenes.find(s=>s.id==='rack-bus-choices');
  for(const compact of [false,true]){
    const buses=supplementalVisual(busScene,initialState,compact);
    assert.match(buses,/50 V/);
    assert.match(buses,/800 V/);
    assert.doesNotMatch(buses,/2,000 A|125 A/);
  }
  const supply=supplementalVisual(dcScenes[supplyIndex],initialState);
  assert.match(supply,/Step down first/);
  assert.match(supply,/Rectify first/);
  assert.match(supply,/solid-state transformer/);
  assert.match(supply,/high-frequency transformer/);
  assert.match(supply,/Rectify \+ regulate/);
  assert.doesNotMatch(supply,/data-converter-view|Calculate the lost power/);
});


test('rack power and DC distribution separate rack behavior from DC distribution',()=>{
  assert.equal(rackScenes.length,16);
  assert.equal(dcScenes.length,15);
  assert.equal(rackScenes.at(-1).id,'buffer-recharge');
  assert.deepEqual(dcScenes.slice(0,2).map(scene=>scene.id),['one-load','conductor-copper']);
  assert.equal(dcScenes.at(-1).id,'power-stack-overview');
  assert.equal(scenes.length,new Set(scenes.map(scene=>scene.id)).size);
  assert.ok(rackScenes.some(scene=>scene.id==='energy-locality'));
  assert.ok(!rackScenes.some(scene=>scene.id==='rack-transfer'));
  assert.ok(!rackScenes.some(scene=>scene.id==='dc-feeder-protection'));
  assert.ok(dcScenes.some(scene=>scene.id==='dc-feeder-protection'));
  for(const [deckId,deck] of Object.entries(decks)){
    const html=readFileSync(new URL(`../course/prototypes/${deck.file}`,import.meta.url),'utf8');
    assert.ok(html.includes(`data-presentation="${deckId}"`));
    assert.match(html,/src="rack-energy-controller.js"/);
    assert.ok(html.includes(deck.title));
  }
});

test('each deck resolves only its own current slide hashes',()=>{
  for(const [deckId,deck] of Object.entries(decks))for(const [index,scene] of deck.scenes.entries()){
    assert.equal(resolveRackEnergyScene(`#${scene.id}`,deckId),index);
    assert.equal(resolveRackEnergyScene(scene.id.replace(/-/g,'%2D'),deckId),index);
  }
  for(const hash of ['','#unknown','#%E0%A4%A','#__proto__'])for(const deckId of Object.keys(decks)){
    assert.equal(resolveRackEnergyScene(hash,deckId),0);
  }
  assert.equal(resolveRackEnergyScene('#conversion-in-sidecar','rack-energy'),0);
  assert.equal(resolveRackEnergyScene('#buffer-recharge','dc-distribution'),0);
});

test('the DC opening names the data-hall comparison without changing the sample opening',()=>{
  let scene=dcScenes[0];
  const renderer=createPresentationRenderers({defaults,getState:()=>initialState,getStep:()=>scene,isRevealed:()=>false,acdcConductorModel,escapeHTML,fmt:String});
  assert.match(renderer.intro(),/Power distribution/);
  assert.match(renderer.intro(),/Comparing AC to DC in the data hall/);
  assert.doesNotMatch(renderer.intro(),/480 V three-phase AC/);
  scene={};
  assert.match(renderer.intro(),/480 V three-phase AC ↔ 800 V DC/);
});


test('the merged energy diagram traces every buffer to the electrical boundary it supports',()=>{
  const expectedNodes=['generator','bess','facility-ac','ups-rectifier','ups-battery','ups-inverter','rack-psu','rack-bbu','vrm','capacitors','chip'];
  const expectedEdges=[['ups-battery','ups-dc-link'],['ups-dc-link','ups-inverter'],['ups-inverter','rack-psu'],['rack-psu','rack-dc'],['rack-dc','vrm'],['vrm','chip-rail'],['chip-rail','chip'],['rack-bbu','rack-dc'],['capacitors','chip-rail']];
  for(const compact of [false,true]){
    const html=renderEnergyConnections(compact);
    assert.equal((html.match(/<svg\b/g)||[]).length,1);
    for(const group of ['facility','rack','chip'])assert.ok(html.includes(`data-power-group="${group}"`));
    for(const node of expectedNodes)assert.ok(html.includes(`data-power-node="${node}"`),node);
    for(const [from,to] of expectedEdges)assert.ok(html.includes(`data-power-from="${from}" data-power-to="${to}"`),`${from} → ${to}`);
    assert.doesNotMatch(html,/undefined|NaN/);
  }
});
