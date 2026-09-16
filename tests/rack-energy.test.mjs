import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';
import { rackLedger, dcPlanes, migrationDecision } from '../course/prototypes/rack-energy-model.js';
import { scenes, initialState, aliases, sceneRedirects, defaults } from '../course/prototypes/rack-energy-scenes.js';
import { scenes as oldRackScenes } from '../course/prototypes/rack-power-scenes.js';
import { acdcConductorModel, acdcWaveModel } from '../course/web/reader-models.js';
import { createElectricalVisuals } from '../course/web/electrical-renderer.js';
import { createPresentationRenderers } from '../course/web/presentation-renderers.js';
import { rackVisual, supplementalVisual, escapeHTML } from '../course/prototypes/rack-energy-visuals.js';
const close=(actual,expected)=>assert.ok(Math.abs(actual-expected)<1e-8,`${actual} versus ${expected}`);

test('legacy sample initializes its shared visual factory after the reveal state exists',()=>{
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
test('chapter sequence preserves architecture order and routes retired foundations to earlier chapters',()=>{
  const sample=JSON.parse(readFileSync(new URL('../course/expansion/sample-presentation.json',import.meta.url)));
  assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
  for(const sequence of [oldRackScenes,sample.steps]){
    let previous=-1;for(const s of sequence.filter(s=>!sceneRedirects[s.id]&&!aliases[s.id]&&s.id!=='rack-transfer')){const index=scenes.findIndex(c=>c.id===s.id);assert.ok(index>previous,s.id);previous=index;}
  }
  for(const [alias,target] of Object.entries(sample.aliases))assert.equal(aliases[alias],target);
  assert.equal(aliases['rear-busbar'],'rack-hardware-anatomy');assert.ok(!scenes.some(s=>s.id==='rear-busbar'));
  assert.equal(aliases['green-dc'],'green-zurich-west');assert.equal(aliases['green-path'],'green-zurich-west');
  for(const target of Object.values(aliases))assert.ok(scenes.some(s=>s.id===target));
  assert.deepEqual(sceneRedirects, {
    'dc-circuit':{file:'terminology-format.html',scene:'circuit'},
    'ac-cycle':{file:'terminology-format.html',scene:'ac-dc'},
    'three-phase':{file:'distribution-format.html',scene:'three-phase'},
    'voltage-basis':{file:'distribution-format.html',scene:'voltage-basis'}
  });
  for(const id of Object.keys(sceneRedirects))assert.ok(!scenes.some(s=>s.id===id));
  const preview=scenes.findIndex(s=>s.id==='dc-architecture-preview');
  assert.equal(scenes[preview+1].id,'conversion-in-rack');
  assert.equal(aliases['migration-decision'],'power-stack-overview');
  const locality=scenes.findIndex(s=>s.id==='energy-locality');
  assert.equal(scenes[locality+1].id,'rack-transfer');
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

test('supply path and converter heat are separate slides with independent reveal behavior',()=>{
  const index=scenes.findIndex(scene=>scene.id==='ac-dc-ledger');
  assert.equal(scenes[index].sourceKind,'conversion-supply');
  assert.equal(scenes[index+1].id,'ac-dc-converter-loss');
  let revealed=false;
  const sample=createPresentationRenderers({defaults,getState:()=>({...initialState,converterView:'heat'}),getStep:()=>scenes[index],isRevealed:()=>revealed,acdcConductorModel,escapeHTML,fmt:(v,d=0)=>v.toLocaleString('en-US',{maximumFractionDigits:d})});
  const supply=sample.conversionSupply();
  assert.match(supply,/13.8 kV → 480 V AC/);
  assert.doesNotMatch(supply,/data-converter-view|Calculate the lost power/);
  assert.match(sample.conversionLoss(),/Calculate the lost power/);
  revealed=true;
  assert.match(sample.conversionLoss(),/102.04/);
  assert.match(sample.conversionLoss(),/2.04 kW/);
  assert.doesNotMatch(sample.conversionLoss(),/data-converter-view/);
});
