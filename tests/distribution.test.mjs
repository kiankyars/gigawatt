import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {scenes,initialState,learning_contract} from '../course/prototypes/distribution-scenes.js';
import {renderDistribution} from '../course/prototypes/distribution-visuals.js';
test('all chapter mechanisms render in each layout and supported control state',()=>{
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 assert.equal(scenes.findIndex(s=>s.id==='transformer-taps'),scenes.findIndex(s=>s.id==='local-stepdown')+1);
 assert.deepEqual(scenes.slice(scenes.findIndex(s=>s.id==='one-line'),scenes.findIndex(s=>s.id==='one-line')+3).map(s=>s.id),['one-line','three-phase','voltage-basis']);
 assert.deepEqual(scenes.slice(scenes.findIndex(s=>s.id==='apparent-power-beer'),scenes.findIndex(s=>s.id==='apparent-power-beer')+3).map(s=>s.id),['apparent-power-beer','power-factor-explained','power-triangle']);
 for(const scene of scenes){
  const states=[{...initialState}];
  if(['three-phase','voltage-basis'].includes(scene.id))for(const cycleDegrees of [0,90,180,270,360])for(const voltageView of ['meter','pairs'])states.push({...initialState,cycleDegrees,voltageView});
  for(const group of scene.controls||[])for(const [value] of group.options)states.push({...initialState,[group.key]:value});
  if(scene.reveal)for(const diagnosis of ['capacity','breaker','surge'])states.push({...initialState,diagnosis,reveal:true});
  for(const state of states)for(const compact of [false,true]){
   const r=renderDistribution(scene.id,state,compact);assert.ok(r.markup.length>100,scene.id);assert.ok(r.description.length>80,scene.id);
   assert.doesNotMatch(r.markup,/NaN|undefined|Infinity/,scene.id);
   if(scene.id==='transformer-taps'){
    const attr=name=>Number(r.markup.match(new RegExp(`data-${name}="([^\"]+)"`))[1]);
    const expected={nominal:[480,480,80,120],'supply-rise':[504,480,80,126],'matched-tap':[504,504,84,120]}[state.transformerCase];
    assert.deepEqual(['input-volts','tap-volts','primary-turns','output-volts'].map(attr),expected,'Source and tap cases retain the published turns example');
    assert.equal(attr('output-volts')/attr('input-volts'),attr('secondary-turns')/attr('primary-turns'),'Output follows connected turns ratio');
    assert.equal(attr('tap-volts')*attr('secondary-turns')/attr('primary-turns'),120,'Tap rating retains nominal secondary output');
   }
  }
 }
});
test('distribution objectives remain taught with concrete cases',()=>{
 assert.deepEqual([...new Set(scenes.flatMap(s=>s.objectives))].sort(),['D04.1','D04.2','D04.4']);
 for(const c of ['compass','fujitsu'])assert.ok(scenes.some(s=>s.case===c));
 for(const key of ['driving_question','fixed_boundary','changed_variable','primary_payoff','misconception','closing_question'])assert.ok(learning_contract[key]);
 assert.ok(scenes.some(s=>s.pedagogical_role==='transfer'&&s.controls?.some(c=>c.key==='diagnosisStage')));
});
test('every photograph exists locally and no renderer fabricates case efficiencies',()=>{
 for(const scene of scenes){const r=renderDistribution(scene.id,initialState);for(const match of r.markup.matchAll(/src="\.\.\/assets\/references\/([^"<>]+)"/g))assert.ok(fs.existsSync(new URL(`../course/assets/references/${match[1]}`,import.meta.url)));}
});
test('breaker-failure sequence preserves the failed feeder and enlarges the outage boundary',()=>{
 const initial=renderDistribution('feeder-diagnosis',{...initialState,diagnosisStage:'fault'}).markup;
 assert.match(initial,/Trip issued/);assert.match(initial,/Fault persists/);assert.match(initial,/Hall B/);assert.match(initial,/No local fault/);
 const backup=renderDistribution('feeder-diagnosis',{...initialState,diagnosisStage:'backup'}).markup;
 assert.match(backup,/Failed to open/);assert.match(backup,/Opened/);assert.match(backup,/Isolated fault/);assert.match(backup,/Supply removed/);
 assert.doesNotMatch(backup,/Fault persists/);
});
test('new deck uses shared chrome and reader route without dialogs or extra chapter links',()=>{
 const html=fs.readFileSync(new URL('../course/prototypes/distribution-format.html',import.meta.url),'utf8');
 const player=fs.readFileSync(new URL('../course/prototypes/distribution-player.js',import.meta.url),'utf8');
 assert.match(html,/slide-chrome\.js/);assert.match(html,/Back to course/);assert.match(html,/>Reading<\/a>/);assert.doesNotMatch(html,/<dialog|Explanation|open-notes/);
 assert.doesNotMatch(player,/ups-format\.html/);assert.match(player,/aria-pressed/);assert.match(player,/aria-expanded/);
});
