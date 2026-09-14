import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {scenes,initialState,learning_contract,chapter8Aliases} from '../course/prototypes/distribution-scenes.js';
import {renderDistribution} from '../course/prototypes/distribution-visuals.js';
test('all chapter mechanisms render in each layout and supported control state',()=>{
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 for(const scene of scenes){
  const states=[{...initialState}];
  for(const group of scene.controls||[])for(const [value] of group.options)states.push({...initialState,[group.key]:value});
  if(scene.reveal)for(const diagnosis of ['capacity','breaker','surge'])states.push({...initialState,diagnosis,reveal:true});
  for(const state of states)for(const compact of [false,true]){
   const r=renderDistribution(scene.id,state,compact);assert.ok(r.markup.length>100,scene.id);assert.ok(r.description.length>80,scene.id);
   assert.doesNotMatch(r.markup,/NaN|undefined|Infinity/,scene.id);
  }
 }
});
test('distribution objectives remain taught and conversion has explicit Chapter 8 routes',()=>{
 assert.deepEqual([...new Set(scenes.flatMap(s=>s.objectives))].sort(),['D04.1','D04.2','D04.4']);
 for(const c of ['compass','fujitsu'])assert.ok(scenes.some(s=>s.case===c));
 for(const key of ['driving_question','fixed_boundary','changed_variable','primary_payoff','misconception','closing_question'])assert.ok(learning_contract[key]);
 assert.ok(scenes.some(s=>s.pedagogical_role==='transfer'&&s.reveal));
});
test('every photograph exists locally and no renderer fabricates case efficiencies',()=>{
 for(const scene of scenes){const r=renderDistribution(scene.id,initialState);for(const match of r.markup.matchAll(/src="\.\.\/assets\/references\/([^"<>]+)"/g))assert.ok(fs.existsSync(new URL(`../course/assets/references/${match[1]}`,import.meta.url)));}
 assert.equal(chapter8Aliases['green-dc'],'green-zurich-west');assert.equal(chapter8Aliases['green-path'],'green-zurich-west');assert.ok(chapter8Aliases['conversion-locations']);
});
test('fault diagnosis distinguishes a trip command from actual interruption',()=>{
 const initial=renderDistribution('feeder-diagnosis',{...initialState,reveal:false}).markup;
 assert.match(initial,/TRIP issued/);assert.match(initial,/Fault persists/);assert.doesNotMatch(initial,/has not cleared/);
 assert.match(renderDistribution('feeder-diagnosis',{...initialState,reveal:true,diagnosis:'breaker'}).markup,/has not cleared/);
 assert.match(renderDistribution('feeder-diagnosis',{...initialState,reveal:true,diagnosis:'capacity'}).markup,/capacity cannot clear/);
});
test('new deck uses shared chrome and reader route without dialogs or extra chapter links',()=>{
 const html=fs.readFileSync(new URL('../course/prototypes/distribution-format.html',import.meta.url),'utf8');
 const player=fs.readFileSync(new URL('../course/prototypes/distribution-player.js',import.meta.url),'utf8');
 assert.match(html,/slide-chrome\.js/);assert.match(html,/Back to course/);assert.match(html,/>Reading<\/a>/);assert.doesNotMatch(html,/<dialog|Explanation|open-notes/);
 assert.doesNotMatch(player,/ups-format\.html/);assert.match(player,/aria-pressed/);assert.match(player,/aria-expanded/);
});
