import test from 'node:test';
import assert from 'node:assert/strict';
import { llamaMemory, sameWorkEnergy, interactivityMetrics, decodeSlots } from '../course/prototypes/workload-model.js';
import { scenes, initialState } from '../course/prototypes/workload-scenes.js';
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
 const x=sameWorkEnergy();assert.equal(x.runA.minutes,10);assert.equal(x.runB.minutes,15);assert.equal(x.runA.powerKW,100);assert.equal(x.runB.powerKW,80);assert.equal(x.runB.energyKWh,20);assert.equal(x.runB.energyKWh/x.runA.energyKWh,1.2);assert.ok(Math.abs(x.energyRatio-1.2)<1e-12);assert.equal(x.breakEvenDurationRatio,1.25);
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
test('each workload state renders',()=>{
 const ids=new Set(scenes.map(s=>s.id));assert.equal(ids.size,18);assert.equal(scenes[0].id,'workload-purpose');
 for(const scene of scenes)for(const compact of[false,true]){
  const states=[initialState,...(scene.controls||[]).flatMap(c=>c.options.map(([value])=>({...initialState,[c.key]:value})))];
  for(const state of states){const r=renderWorkload(scene.id,state,compact);assert.ok(r.description.length>30);assert.match(r.markup,/<(?:text|image)\b/);assert.doesNotMatch(r.markup,/\bNaN\b|\bInfinity\b/);}
 }
});

test('weight reuse follows prefill/decode and changes vectors without adding weight loads',()=>{
 const index=scenes.findIndex(s=>s.id==='operand-reuse');
 assert.equal(scenes[index-1].id,'prefill-decode');
 for(const compact of[false,true])for(const reuseTokens of[1,8]){
  const {markup,description}=renderWorkload('operand-reuse',{...initialState,reuseTokens},compact);
  assert.equal((markup.match(/data-token-vector=/g)||[]).length,reuseTokens);
  assert.equal((markup.match(/data-weight-tile=/g)||[]).length,2);
  assert.equal((markup.match(/Load once/g)||[]).length,1);
  assert.match(description,/GPU memory, or HBM/);
  assert.match(description,/on-chip memory/);
 }
});

test('interactivity is per-user generation speed, separate from capacity',()=>{
 for(const rate of [20,40,80]){
  const x=interactivityMetrics({tokensPerSecond:rate});assert.equal(x.millisecondsPerToken,1000/rate);
  assert.equal(x.tokensPerSecond,rate);
 }
 for(const rate of [0,-1,NaN,Infinity])assert.throws(()=>interactivityMetrics({tokensPerSecond:rate}));
 assert.equal(scenes[2].id,'interactivity');
});
test('staggered teaching state preserves cycle energy and lowers the coincident peak',()=>{
 for(const compact of [false,true]){
  const sync=renderWorkload('synchronized-jobs',initialState,compact).markup;
  const staggered=renderWorkload('staggering-jobs',initialState,compact).markup;
  const attr=(html,name)=>Number(html.match(new RegExp('data-'+name+'="([^" ]+)"'))[1]);
  assert.equal(attr(sync,'peak-kw'),480);assert.equal(attr(staggered,'peak-kw'),340);
  assert.equal(attr(sync,'energy-kwh'),attr(staggered,'energy-kwh'));
  assert.equal(attr(sync,'average-kw'),attr(staggered,'average-kw'));
 }
});
