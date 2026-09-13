import test from 'node:test';
import assert from 'node:assert/strict';
import { llamaMemory, sameWorkEnergy, decodeSlots } from '../course/prototypes/workload-model.js';
import { scenes, initialState, legacySceneAliases } from '../course/prototypes/workload-scenes.js';
import { renderWorkload } from '../course/prototypes/workload-visuals.js';

test('named KV geometry preserves bytes, binary capacity and whole-request allocation',()=>{
 const short=llamaMemory(),long=llamaMemory({contextTokens:32768});
 assert.equal(short.weightsGB,140);assert.equal(short.trainingStateGB,1120);
 assert.equal(short.kvBytesPerToken,327680);assert.equal(short.requestGiB,2.5);
 assert.equal(long.requestGiB,10);assert.equal(short.concurrentRequests,25);assert.equal(long.concurrentRequests,6);
 for(const x of[short,long]){assert.ok(x.concurrentRequests*x.requestGiB<=64);assert.ok((x.concurrentRequests+1)*x.requestGiB>64);}
 for(const contextTokens of[0,-1,1.5,NaN,Infinity])assert.throws(()=>llamaMemory({contextTokens}));
});
test('same-work energy uses mean power and total duration with a consistent break-even',()=>{
 const x=sameWorkEnergy();assert.ok(Math.abs(x.energyRatio-1.2)<1e-12);assert.equal(x.breakEvenDurationRatio,1.25);
 assert.equal(sameWorkEnergy({durationRatio:1.25}).energyRatio,1);
 assert.throws(()=>sameWorkEnergy({powerRatio:0}));
});
test('continuous membership preserves each request token count and admits C only in a free slot',()=>{
 for(const policy of[false,true]){
  const x=decodeSlots(policy);for(const job of x.jobs)assert.equal(x.rows.flat().filter(v=>v===job.id).length,job.tokens);
  assert.equal(x.rows.flat().filter(Boolean).length,10);assert.equal(x.rows[0].indexOf('C'),policy?2:5);
  assert.equal(x.rows[1][4],'B');assert.equal(x.stepsToComplete,policy?5:8);
 }
});
test('each retained state renders and retired deep links lead to taught replacement content',()=>{
 const ids=new Set(scenes.map(s=>s.id));assert.equal(ids.size,18);assert.equal(scenes[0].id,'workload-purpose');
 for(const target of Object.values(legacySceneAliases))assert.ok(ids.has(target));
 assert.equal(legacySceneAliases['acceptance-envelope'],'next-brief');
 for(const scene of scenes)for(const compact of[false,true]){
  const states=[initialState,...(scene.controls||[]).flatMap(c=>c.options.map(([value])=>({...initialState,[c.key]:value})))];
  for(const state of states){const r=renderWorkload(scene.id,state,compact);assert.ok(r.description.length>30);assert.ok(r.markup.includes('<text'));assert.doesNotMatch(r.markup,/\bNaN\b|\bInfinity\b/);}
 }
});
