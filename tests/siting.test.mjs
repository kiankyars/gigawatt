import test from 'node:test';
import assert from 'node:assert/strict';
import { scenes, initialState } from '../course/prototypes/siting-scenes.js';
import { renderSiting } from '../course/prototypes/siting-visuals.js';

test('every authored state renders with an accessible account at both layout sizes',()=>{
 assert.equal(scenes.length,26);
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 for(const scene of scenes){
  const states=[initialState];
  for(const c of scene.controls||[])for(const [v] of c.options)states.push({...initialState,[c.key]:v});
  if(scene.reveal)states.push({...initialState,[scene.reveal]:true});
  for(const state of states)for(const compact of [false,true]){
   const a=renderSiting(scene.id,state,compact);
   assert.ok(a.description.length>30,scene.id);
   assert.doesNotMatch(a.markup,/undefined|NaN|Infinity/,scene.id);
  }
 }
});
