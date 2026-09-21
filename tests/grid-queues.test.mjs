import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync,existsSync} from 'node:fs';
import {scenes,sceneAliases} from '../course/prototypes/grid-queues-scenes.js';
import {gridQueuesVisual} from '../course/prototypes/grid-queues-visuals.js';
import {projectOptions,securityFaceAmount,stagedLoad,dominionSnapshot,ercotSnapshot,ercotGroups} from '../course/prototypes/grid-queues-model.js';
import {parseSpeakerNotes} from '../course/prototypes/presenter-notes.js';

test('the opening slide carries only the two operator logos',()=>{
 assert.equal(scenes[0].title,'What does a place in the queue actually buy?');
 const html=gridQueuesVisual('queue-purpose');
 assert.deepEqual([...html.matchAll(/alt="([^"]+)"/g)].map(m=>m[1]),['ERCOT','PJM']);
 assert.equal(html.replace(/<[^>]+>/g,'').trim(),'');
});
test('ERCOT status rows collapse into three groups that account for the whole pipeline',()=>{
 const groups=ercotGroups();
 assert.deepEqual(groups.map(g=>g.gw),[284.3,135.5,55]);
 assert.ok(Math.abs(groups.reduce((sum,g)=>sum+g.gw,0)-ercotSnapshot.totalGW)<0.15,'rounded rows differ from the displayed total by 0.1 GW');
 const html=gridQueuesVisual('ercot-pipeline');
 assert.equal((html.match(/style="flex:/g)||[]).length,3);
 assert.match(html,/5\.9 GW/);assert.match(html,/July 29, 2026/);
 assert.doesNotMatch(html,/phantom|speculative|cancel/i);
});
test('mutually exclusive site requests add to more than the planned deployment, without controls',()=>{
 const m=projectOptions();
 assert.equal(m.requestedMW,3000);assert.equal(m.plannedMW,1000);assert.deepEqual(m.sites,['A','B','C']);
 const html=gridQueuesVisual('site-options');
 assert.equal((html.match(/1 GW request/g)||[]).length,3);
 assert.doesNotMatch(html,/<button|Withdrawn/);
 assert.ok(scenes.every(scene=>!scene.controls),'no slide in this deck is interactive');
});
test('security is computed from MW, labelled as new, and not relabelled a cash fee',()=>{
 assert.equal(securityFaceAmount(1000),50000000);
 assert.equal(securityFaceAmount(100),5000000);
 for(const v of [0,-1,NaN,Infinity])assert.throws(()=>securityFaceAmount(v),RangeError);
 const visual=gridQueuesVisual('commitment-costs');
 assert.match(visual,/security face amount/);assert.match(visual,/effective October 8, 2026/);
 assert.match(visual,/Before SB 6/);assert.match(visual,/No ERCOT-wide amount/);
 assert.doesNotMatch(visual,/\$0|free/i);
});
test('staged local supply never exceeds campus demand or invents more grid access',()=>{
 assert.deepEqual([0,1,2].map(stagedLoad),[100,600,1000]);
 assert.equal(stagedLoad(2)-stagedLoad(1),400);
 assert.throws(()=>stagedLoad(3),RangeError);
 const d=dominionSnapshot;
 assert.ok(Math.abs(d.engineeringGW+d.constructionGW+d.serviceGW-d.totalGW)<1e-9);
 assert.doesNotMatch(gridQueuesVisual('staged-connection'),/grid import limited|does not raise/);
});
test('every scene has a rendered visual, an authored spoken note, and local source images',()=>{
 const notes=parseSpeakerNotes(readFileSync(new URL('../course/SPEAKER_NOTES.md',import.meta.url),'utf8'));
 assert.equal(scenes.length,11);
 assert.equal(new Set(scenes.map(s=>s.id)).size,scenes.length);
 for(const scene of scenes){
  const html=gridQueuesVisual(scene.id);
  assert.ok(html.length>100,scene.id);assert.doesNotMatch(html,/NaN|undefined|Infinity/,scene.id);
  assert.ok(notes.get(`grid-queues#${scene.id}`),scene.id);
  for(const [,src] of html.matchAll(/<img\b[^>]*\bsrc="([^"]+)"/g))assert.ok(existsSync(new URL(src,new URL('../course/prototypes/',import.meta.url))),src);
 }
 assert.throws(()=>gridQueuesVisual('missing'),/Unknown/);
});
test('retired slide anchors resolve to current slides',()=>{
 for(const [old,current] of Object.entries(sceneAliases)){
  assert.ok(scenes.some(s=>s.id===current),current);assert.ok(!scenes.some(s=>s.id===old),old);
 }
});
