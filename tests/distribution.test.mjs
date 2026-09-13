import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import {scenes,initialState,learning_contract} from '../course/prototypes/distribution-scenes.js';
import {renderDistribution} from '../course/prototypes/distribution-visuals.js';
test('all chapter mechanisms render in each layout and supported control state',()=>{
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 for(const scene of scenes){
  const states=[{...initialState}];
  for(const group of scene.controls||[])for(const [value] of group.options)states.push({...initialState,[group.key]:value});
  if(scene.reveal)for(const decision of ['service','branch','both'])states.push({...initialState,decision,reveal:true});
  for(const state of states)for(const compact of [false,true]){
   const r=renderDistribution(scene.id,state,compact);assert.ok(r.markup.length>100,scene.id);assert.ok(r.description.length>80,scene.id);
   assert.doesNotMatch(r.markup,/NaN|undefined|Infinity/,scene.id);
  }
 }
});
test('all four D04 objectives and three primary-source cases have authored scenes',()=>{
 assert.deepEqual([...new Set(scenes.flatMap(s=>s.objectives))].sort(),['D04.1','D04.2','D04.3','D04.4']);
 for(const c of ['compass','fujitsu','green'])assert.ok(scenes.some(s=>s.case===c));
 for(const key of ['driving_question','fixed_boundary','changed_variable','primary_payoff','misconception','closing_question'])assert.ok(learning_contract[key]);
 assert.ok(scenes.some(s=>s.pedagogical_role==='transfer'&&s.reveal));
});
test('every photograph exists locally and no renderer fabricates case efficiencies',()=>{
 for(const scene of scenes){const r=renderDistribution(scene.id,initialState);for(const match of r.markup.matchAll(/src="\.\.\/assets\/references\/([^"<>]+)"/g))assert.ok(fs.existsSync(new URL(`../course/assets/references/${match[1]}`,import.meta.url)));}
 const green=renderDistribution('green-path',initialState).markup;assert.match(green,/16 kV AC/);assert.match(green,/1,100 kVA/);assert.match(green,/400 V open-circuit/);
});
test('check-in reveals the surviving constraint for each proposed intervention',()=>{
 assert.doesNotMatch(renderDistribution('expansion-decision',{...initialState,reveal:false}).markup,/Hold the extension/);
 assert.match(renderDistribution('expansion-decision',{...initialState,reveal:true,decision:'service'}).markup,/Hold the extension: IT branch/);
 assert.match(renderDistribution('expansion-decision',{...initialState,reveal:true,decision:'branch'}).markup,/Hold the extension: service/);
 assert.match(renderDistribution('expansion-decision',{...initialState,reveal:true,decision:'both'}).markup,/Both capacity screens pass/);
});
test('new deck uses shared chrome and reader route without dialogs or extra chapter links',()=>{
 const html=fs.readFileSync(new URL('../course/prototypes/distribution-format.html',import.meta.url),'utf8');
 const player=fs.readFileSync(new URL('../course/prototypes/distribution-player.js',import.meta.url),'utf8');
 assert.match(html,/slide-chrome\.js/);assert.match(html,/Back to course/);assert.match(html,/>Reading<\/a>/);assert.doesNotMatch(html,/<dialog|Explanation|open-notes/);
 assert.doesNotMatch(player,/ups-format\.html/);assert.match(player,/aria-pressed/);assert.match(player,/aria-expanded/);
});
