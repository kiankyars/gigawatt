import test from 'node:test';
import assert from 'node:assert/strict';
import {inputPipeline,checkpointTransfer,checkpointCommit,asyncQueue,checkpointTimeline,recoveryEnergy,eligibleGroups,localityRecovery,flexibleSchedule,recoveryChoices} from '../course/prototypes/storage-model.js';
const close=(a,b)=>assert.ok(Math.abs(a-b)<1e-9,`${a} ≠ ${b}`);

test('the input path uses its slowest stage and caps supply at job demand',()=>{
 const baseline=inputPipeline();assert.deepEqual(baseline.bottlenecks,['host']);assert.equal(baseline.deliveredGBps,8);close(baseline.activeFraction,2/3);
 const fasterHost=inputPipeline({hostGBps:20});assert.deepEqual(fasterHost.bottlenecks,['source']);assert.equal(fasterHost.supplyGBps,16);assert.equal(fasterHost.deliveredGBps,12);assert.equal(fasterHost.activeFraction,1);
 assert.equal(inputPipeline({networkGBps:48}).deliveredGBps,8,'a faster network does not relieve host preparation');
});
test('checkpoint timing includes serialized metadata and commit after the overlapping bulk bottleneck',()=>{
 assert.deepEqual(checkpointTransfer(),{payloadGBps:16,payloadSeconds:32,metadataSeconds:4,commitSeconds:2,totalSeconds:38});
 const sourceUpgrade=checkpointTransfer({sourceGBps:32});assert.equal(sourceUpgrade.payloadGBps,20);assert.equal(sourceUpgrade.totalSeconds,31.6);
 const moreShards=checkpointTransfer({shards:65536});assert.equal(moreShards.metadataSeconds,64);assert.equal(moreShards.payloadSeconds,32);assert.equal(moreShards.totalSeconds,98);
 assert.equal(checkpointTransfer({networkGBps:48}).totalSeconds,38);
});
test('a recovery point advances only after all shards agree, persistence is reached and publication succeeds',()=>{
 for(const params of[{shards:[42,42,42,null],published:true},{shards:[42,42,42,43],published:true},{durable:false,published:true},{published:false}]){
  assert.equal(checkpointCommit(params).recoveryVersion,41);assert.equal(checkpointCommit(params).recoverable,false);
 }
 const ready=checkpointCommit();assert.equal(ready.canPublish,true);assert.equal(ready.recoverable,false);
 const committed=checkpointCommit({published:true});assert.equal(committed.recoveryVersion,42);assert.equal(committed.recoverable,true);
});
test('asynchronous saves obey the serial writer and bounded snapshot memory',()=>{
 const q=asyncQueue();assert.deepEqual(q.saves.map(s=>[s.requested,s.admitted,s.end]),[[0,0,64],[30,30,128],[60,64,192],[90,128,256]]);assert.equal(q.backpressured,true);assert.equal(q.maxStagedGB,1024);
 const spaced=asyncQueue({intervalSeconds:90});assert.equal(spaced.backpressured,false);assert.equal(spaced.maxStagedGB,512);assert.equal(spaced.stagedCapacityGB,1024);
 for(const limit of[1,2,3]){const run=asyncQueue({intervalSeconds:10,attempts:10,maxOutstanding:limit});for(const event of run.saves){const active=run.saves.filter(s=>s.admitted<=event.admitted&&s.end>event.admitted);assert.ok(active.length<=limit);assert.ok(event.start>=event.admitted);assert.ok(event.admitted>=event.requested);}assert.ok(run.maxStagedGB<=run.stagedCapacityGB);}
});
test('checkpoint policies change preserved progress across failure positions and retain a no-failure cost',()=>{
 const early20=checkpointTimeline(),early40=checkpointTimeline({intervalMinutes:40});
 assert.equal(early20.finishMinute,82);assert.equal(early20.lostMinutes,13);assert.equal(early20.preservedAtFailure,20);
 assert.equal(early40.finishMinute,102);assert.equal(early40.lostMinutes,35);assert.equal(early40.preservedAtFailure,0);
 for(const intervalMinutes of[20,40]){const later=checkpointTimeline({intervalMinutes,failureMinute:55});assert.equal(later.finishMinute,80);assert.equal(later.preservedAtFailure,40);}
 assert.equal(checkpointTimeline({failureMinute:null}).finishMinute,64);assert.equal(checkpointTimeline({intervalMinutes:40,failureMinute:null}).finishMinute,62);
 const interruptedSave=checkpointTimeline({failureMinute:21});assert.equal(interruptedSave.preservedAtFailure,0);assert.equal(interruptedSave.lostMinutes,20);
 assert.equal(checkpointTimeline({failureMinute:22}).preservedAtFailure,20,'a completed save remains recoverable at the next work boundary');
});
test('timeline accounts conserve elapsed time and never count lost computation as accepted work',()=>{
 for(const intervalMinutes of[10,20,40,60])for(const failureMinute of[0,20,21,22,35,42,44,55,60,64,100,null]){
  const t=checkpointTimeline({intervalMinutes,failureMinute});let end=0;for(const s of t.segments){close(s.start,end);assert.ok(s.duration>0);end=s.end;}close(end,t.finishMinute);
  close(t.segments.filter(s=>s.kind==='work').reduce((a,s)=>a+s.duration,0),60);
  close(t.segments.filter(s=>s.kind==='lost').reduce((a,s)=>a+s.duration,0),t.lostMinutes);
  close(t.finishMinute,60+t.lostMinutes+t.saveMinutes+t.recoveryMinutes);
 }
});
test('energy integrates each phase at the declared power and holds accepted computation equal',()=>{
 const a=recoveryEnergy(checkpointTimeline()),b=recoveryEnergy(checkpointTimeline({intervalMinutes:40}));close(a.usefulMWh,1);close(b.usefulMWh,1);close(a.lostMWh,13/60);close(b.lostMWh,35/60);close(a.totalMWh,1.3033333333333332);close(b.totalMWh,1.6433333333333333);
 close(a.totalMWh,a.usefulMWh+a.lostMWh+a.saveMWh+a.recoveryMWh);
 const off=recoveryEnergy(checkpointTimeline(),{workMW:0,saveMW:0,recoveryMW:0});assert.equal(off.totalMWh,0);
});
test('placement requires a complete eligible group, not the same aggregate free count',()=>{
 const fragmented=eligibleGroups();assert.equal(fragmented.freeGPUs,32);assert.deepEqual(fragmented.eligible,[]);
 const together=eligibleGroups({groups:[[true,true,true,true],[false,false,false,false]]});assert.equal(together.freeGPUs,32);assert.deepEqual(together.eligible,[0]);
 assert.deepEqual(eligibleGroups({nodesRequired:2}).eligible,[0,1]);
});
test('locality saves read time but the queue can reverse the preferred recovery path',()=>{
 const short=localityRecovery();assert.equal(short.localReadSeconds,16);assert.equal(short.remoteReadSeconds,64);assert.equal(short.localReadySeconds,58);assert.equal(short.remoteReadySeconds,76);
 const long=localityRecovery({waitSeconds:90});assert.equal(long.localReadySeconds,118);assert.equal(long.remoteReadySeconds,76);assert.ok(long.localReadySeconds>long.remoteReadySeconds);
});
test('scheduling honors service deadlines and conserves job energy while moving the power peak',()=>{
 const shifted=flexibleSchedule();assert.equal(shifted.finishHour,18);assert.equal(shifted.eventPeakMW,20);assert.equal(shifted.laterPeakMW,24);assert.equal(shifted.meetsDeadline,true);assert.equal(shifted.jobMWh,12);assert.equal(shifted.eventOverlapHours,0);
 const early=flexibleSchedule({deadlineHour:17});assert.equal(early.meetsDeadline,false);assert.equal(early.slackHours,-1);
 const continuous=flexibleSchedule({shift:false});assert.equal(continuous.finishHour,16);assert.equal(continuous.eventPeakMW,24);assert.equal(continuous.laterPeakMW,20);assert.equal(continuous.jobMWh,shifted.jobMWh);
 for(const run of[shifted,continuous])close(run.segments.reduce((a,s)=>a+s.end-s.start,0),3);
});
test('models reject impossible rates, state and scheduling inputs',()=>{
 for(const fn of[()=>inputPipeline({hostGBps:0}),()=>checkpointTransfer({shards:1.5}),()=>checkpointCommit({shards:[]}),()=>checkpointCommit({shards:[0]}),()=>asyncQueue({maxOutstanding:0}),()=>checkpointTimeline({intervalMinutes:0}),()=>checkpointTimeline({failureMinute:-1}),()=>recoveryEnergy(checkpointTimeline(),{recoveryMW:-1}),()=>eligibleGroups({groups:[[1,0]]}),()=>localityRecovery({waitSeconds:-1}),()=>flexibleSchedule({eventEnd:14}),()=>flexibleSchedule({workHours:NaN})])assert.throws(fn,RangeError);
});
