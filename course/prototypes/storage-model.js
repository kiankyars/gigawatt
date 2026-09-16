const positive=(value,label)=>{if(!Number.isFinite(value)||value<=0)throw new RangeError(`${label} must be positive.`);return value;};
const nonnegative=(value,label)=>{if(!Number.isFinite(value)||value<0)throw new RangeError(`${label} must be nonnegative.`);return value;};
const integer=(value,label)=>{positive(value,label);if(!Number.isInteger(value))throw new RangeError(`${label} must be an integer.`);return value;};

export function inputPipeline({sourceGBps=16,networkGBps=24,hostGBps=8,demandGBps=12}={}){
 for(const [k,v]of Object.entries({sourceGBps,networkGBps,hostGBps,demandGBps}))positive(v,k);
 const stages=[{id:'source',rate:sourceGBps},{id:'network',rate:networkGBps},{id:'host',rate:hostGBps}],supplyGBps=Math.min(...stages.map(s=>s.rate));
 return {stages,supplyGBps,deliveredGBps:Math.min(supplyGBps,demandGBps),activeFraction:Math.min(1,supplyGBps/demandGBps),bottlenecks:stages.filter(s=>s.rate===supplyGBps).map(s=>s.id)};
}
export function checkpointTransfer({payloadGB=512,sourceGBps=16,networkGBps=24,backendGBps=20,shards=4096,metadataOps=1024,commitSeconds=2}={}){
 for(const [k,v]of Object.entries({payloadGB,sourceGBps,networkGBps,backendGBps,metadataOps}))positive(v,k);integer(shards,'shards');nonnegative(commitSeconds,'commitSeconds');
 const payloadGBps=Math.min(sourceGBps,networkGBps,backendGBps),payloadSeconds=payloadGB/payloadGBps,metadataSeconds=shards/metadataOps;
 return {payloadGBps,payloadSeconds,metadataSeconds,commitSeconds,totalSeconds:metadataSeconds+payloadSeconds+commitSeconds};
}
export function checkpointCommit({shards=[42,42,42,42],requiredVersion=42,durable=true,published=false,previousVersion=41}={}){
 integer(requiredVersion,'requiredVersion');integer(previousVersion,'previousVersion');if(!Array.isArray(shards)||shards.length===0)throw new RangeError('Checkpoint shards are required.');
 if(shards.some(v=>v!==null&&(!Number.isInteger(v)||v<=0)))throw new RangeError('Shard versions must be positive integers or missing.');
 const coherent=shards.every(v=>v===requiredVersion),canPublish=coherent&&durable,recoverable=published&&canPublish;
 return {coherent,canPublish,recoverable,recoveryVersion:recoverable?requiredVersion:previousVersion};
}
export function asyncQueue({intervalSeconds=30,writeSeconds=64,checkpointGB=512,attempts=4,maxOutstanding=2}={}){
 for(const [k,v]of Object.entries({intervalSeconds,writeSeconds,checkpointGB}))positive(v,k);integer(attempts,'attempts');integer(maxOutstanding,'maxOutstanding');
 const saves=[];for(let i=0;i<attempts;i++){const requested=i*intervalSeconds;const released=i>=maxOutstanding?saves[i-maxOutstanding].end:0;const admitted=Math.max(requested,released),start=Math.max(admitted,saves.at(-1)?.end||0);saves.push({requested,admitted,start,end:start+writeSeconds,pauseSeconds:admitted-requested});}
 const peakOutstanding=Math.max(...saves.map(event=>saves.filter(s=>s.admitted<=event.admitted&&s.end>event.admitted).length));
 return {saves,productionGBps:checkpointGB/intervalSeconds,persistenceGBps:checkpointGB/writeSeconds,stagedCapacityGB:maxOutstanding*checkpointGB,maxStagedGB:peakOutstanding*checkpointGB,backpressured:saves.some(s=>s.pauseSeconds>0)};
}
export function checkpointTimeline({targetMinutes=60,intervalMinutes=20,saveMinutes=2,failureMinute=35,recoveryMinutes=5}={}){
 for(const [k,v]of Object.entries({targetMinutes,intervalMinutes,saveMinutes}))positive(v,k);nonnegative(recoveryMinutes,'recoveryMinutes');if(failureMinute!==null)nonnegative(failureMinute,'failureMinute');
 let time=0,progress=0,preserved=0,failed=false,lostMinutes=0;const segments=[];
 const append=(kind,duration)=>{if(duration>0){segments.push({kind,start:time,end:time+duration,duration});time+=duration;}};
 const fail=()=>{lostMinutes=progress-preserved;for(let i=segments.length-1;i>=0;i--){if(segments[i].kind==='save'&&segments[i].complete)break;if(segments[i].kind==='work')segments[i].kind='lost';}progress=preserved;failed=true;append('recovery',recoveryMinutes);};
 if(failureMinute===0)fail();
 while(progress<targetMinutes){
  const work=Math.min(intervalMinutes-(progress-preserved),targetMinutes-progress);
  if(!failed&&failureMinute!==null&&failureMinute>=time&&failureMinute<time+work){const partial=failureMinute-time;append('work',partial);progress+=partial;fail();continue;}
  append('work',work);progress+=work;if(progress>=targetMinutes)break;
  if(!failed&&failureMinute!==null&&failureMinute>=time&&failureMinute<time+saveMinutes){append('save',failureMinute-time);fail();continue;}
  append('save',saveMinutes);segments.at(-1).complete=true;preserved=progress;
 }
 return {segments,finishMinute:time,lostMinutes,failed,preservedAtFailure:failed?targetMinutes-segments.filter(s=>s.kind==='work'&&s.start>=failureMinute).reduce((a,s)=>a+s.duration,0):null,saveMinutes:segments.filter(s=>s.kind==='save').reduce((a,s)=>a+s.duration,0),recoveryMinutes:failed?recoveryMinutes:0,usefulMinutes:targetMinutes};
}
export function recoveryEnergy(timeline,{workMW=1,saveMW=.8,recoveryMW=.4}={}){
 for(const[k,v]of Object.entries({workMW,saveMW,recoveryMW}))nonnegative(v,k);
 const ledger={usefulMWh:0,lostMWh:0,saveMWh:0,recoveryMWh:0};
 for(const segment of timeline.segments){const key={work:'usefulMWh',lost:'lostMWh',save:'saveMWh',recovery:'recoveryMWh'}[segment.kind];if(!key)throw new RangeError('Unknown timeline interval.');ledger[key]+=segment.duration/60*({work:workMW,lost:workMW,save:saveMW,recovery:recoveryMW}[segment.kind]);}
 return {...ledger,totalMWh:Object.values(ledger).reduce((a,b)=>a+b,0)};
}
export function eligibleGroups({groups=[[true,true,false,false],[true,true,false,false]],nodesRequired=4,gpusPerNode=8}={}){
 integer(nodesRequired,'nodesRequired');integer(gpusPerNode,'gpusPerNode');if(!Array.isArray(groups)||!groups.length||groups.some(g=>!Array.isArray(g)||g.some(v=>typeof v!=='boolean')))throw new RangeError('Groups must contain node availability.');
 const freeByGroup=groups.map(g=>g.filter(Boolean).length);return {freeByGroup,freeGPUs:freeByGroup.reduce((a,b)=>a+b,0)*gpusPerNode,eligible:freeByGroup.map((n,i)=>n>=nodesRequired?i:null).filter(i=>i!==null)};
}
export function localityRecovery({checkpointGB=512,localGBps=32,remoteGBps=8,waitSeconds=30,setupSeconds=12}={}){
 for(const[k,v]of Object.entries({checkpointGB,localGBps,remoteGBps}))positive(v,k);nonnegative(waitSeconds,'waitSeconds');nonnegative(setupSeconds,'setupSeconds');
 return {localReadSeconds:checkpointGB/localGBps,remoteReadSeconds:checkpointGB/remoteGBps,localReadySeconds:waitSeconds+setupSeconds+checkpointGB/localGBps,remoteReadySeconds:setupSeconds+checkpointGB/remoteGBps};
}
export function flexibleSchedule({deadlineHour=20,eventStart=14,eventEnd=16,workHours=3,startHour=13,shift=true,baseMW=20,jobMW=4}={}){
 for(const[k,v]of Object.entries({workHours,baseMW,jobMW}))positive(v,k);for(const[k,v]of Object.entries({deadlineHour,eventStart,eventEnd,startHour}))nonnegative(v,k);if(eventEnd<=eventStart||eventStart<startHour)throw new RangeError('Grid event must follow the scheduling start.');
 const first=Math.min(workHours,eventStart-startHour),remaining=workHours-first;
 const segments=shift&&remaining>0?[{start:startHour,end:startHour+first},{start:eventEnd,end:eventEnd+remaining}].filter(s=>s.end>s.start):[{start:startHour,end:startHour+workHours}];
 const finishHour=segments.at(-1).end,eventOverlapHours=segments.reduce((a,s)=>a+Math.max(0,Math.min(s.end,eventEnd)-Math.max(s.start,eventStart)),0);
 return {segments,finishHour,meetsDeadline:finishHour<=deadlineHour,eventOverlapHours,eventPeakMW:baseMW+(eventOverlapHours>0?jobMW:0),laterPeakMW:baseMW+(segments.some(s=>s.end>eventEnd)?jobMW:0),jobMWh:workHours*jobMW,slackHours:deadlineHour-finishHour};
}
export const recoveryChoices={
 newest:{correct:false,text:'Checkpoint 43 is incomplete. Faster allocation cannot make that state complete.'},
 split:{correct:false,text:'Checkpoint 42 is usable, but two nodes in each group do not meet the four-node placement requirement.'},
 restore:{correct:true,text:'Reserve all four nodes in Group A, load complete checkpoint 42, validate the shared environment, then check the first correct new output.'},
 cache:{correct:false,text:'The failed node and its local copy are unavailable. A fast local write did not create an independent, complete recovery point.'},
};
