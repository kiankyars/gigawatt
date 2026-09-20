import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {scenes,initialState} from '../course/prototypes/grid-queues-scenes.js';
import {gridQueuesVisual} from '../course/prototypes/grid-queues-visuals.js';
import {projectOptions,securityFaceAmount,stagedLoad,dominionSnapshot} from '../course/prototypes/grid-queues-model.js';
import {parseSpeakerNotes} from '../course/prototypes/presenter-notes.js';

test('choosing among mutually exclusive sites removes requests without cancelling the deployment',()=>{
 const exploring=projectOptions(),selected=projectOptions(true);
 assert.equal(exploring.requestedMW,3000);assert.equal(selected.requestedMW,1000);
 assert.equal(exploring.plannedMW,selected.plannedMW);assert.deepEqual(selected.activeSites,['B']);
 const html=gridQueuesVisual('site-options',{siteChoice:'selected'});
 assert.equal((html.match(/Withdrawn/g)||[]).length,2);
 assert.equal((html.match(/1 GW request/g)||[]).length,1);
});
test('security is computed from MW without being relabelled a cash fee',()=>{
 assert.equal(securityFaceAmount(1000),50000000);
 assert.equal(securityFaceAmount(100),5000000);
 for(const v of [0,-1,NaN,Infinity])assert.throws(()=>securityFaceAmount(v),RangeError);
 const visual=gridQueuesVisual('commitment-costs');
 assert.match(visual,/security face amount/);assert.match(visual,/effective October 8, 2026/);
});
test('staged local supply never exceeds campus demand or invents more grid access',()=>{
 assert.deepEqual([0,1,2].map(stagedLoad),[100,600,1000]);
 assert.equal(stagedLoad(2)-stagedLoad(1),400);
 assert.throws(()=>stagedLoad(3),RangeError);
 assert.equal(dominionSnapshot.engineeringGW+dominionSnapshot.constructionGW+dominionSnapshot.serviceGW,dominionSnapshot.totalGW);
});
test('every scene has a rendered visual, an authored spoken note, and local source images',()=>{
 const notes=parseSpeakerNotes(readFileSync(new URL('../course/SPEAKER_NOTES.md',import.meta.url),'utf8'));
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 for(const scene of scenes){
  const html=gridQueuesVisual(scene.id,initialState);
  assert.ok(html.length>100,scene.id);assert.doesNotMatch(html,/NaN|undefined|Infinity/,scene.id);
  assert.ok(notes.get(`grid-queues#${scene.id}`),scene.id);
  for(const [,src] of html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g))assert.ok(existsSync(new URL(src,new URL('../course/prototypes/',import.meta.url))),src);
 }
 assert.throws(()=>gridQueuesVisual('missing'),/Unknown/);
});
