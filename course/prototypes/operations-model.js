// Original teaching scenarios. Times are seconds unless a name states otherwise.
function finite(value,name){if(!Number.isFinite(value))throw new RangeError(`${name} must be finite`);return value;}
function nonnegative(value,name){finite(value,name);if(value<0)throw new RangeError(`${name} must be nonnegative`);return value;}
export function sampleQuality({observedAt,receivedAt,now,maxAge=60}){
 for(const [name,value]of Object.entries({observedAt,receivedAt,now,maxAge}))nonnegative(value,name);
 const age=now-observedAt,deliveryDelay=receivedAt-observedAt;
 const ordered=observedAt<=receivedAt&&receivedAt<=now;
 return {age,deliveryDelay,ordered,fresh:ordered&&age<=maxAge,quality:!ordered?'Clock mismatch':age>maxAge?'Stale':'Current'};
}
export function heatBalance({flow=100,supply=30,returnTemperature=40,cp=4.18}={}){
 nonnegative(flow,'Flow');finite(supply,'Supply temperature');finite(returnTemperature,'Return temperature');
 if(!(cp>0&&Number.isFinite(cp)))throw new RangeError('Specific heat must be positive');
 return {deltaT:returnTemperature-supply,heatMW:flow*cp*(returnTemperature-supply)/1000};
}
export function readiness({command=false,acknowledged=false,flowProven=false,temperatureProven=false,fresh=true}={}){
 return {requested:command,acknowledged:command&&acknowledged,available:command&&acknowledged&&flowProven&&temperatureProven&&fresh};
}
export function transition({loadMW=6,removalMW=5,delayMinutes=2,allowanceMWh=.04,admit='now'}={}){
 for(const [name,value]of Object.entries({loadMW,removalMW,delayMinutes,allowanceMWh}))nonnegative(value,name);
 if(!['now','ready'].includes(admit))throw new RangeError('Unknown admission policy');
 const imbalanceMW=admit==='ready'?0:Math.max(0,loadMW-removalMW);
 const consumedMWh=imbalanceMW*delayMinutes/60;
 return {imbalanceMW,consumedMWh,remainingMWh:allowanceMWh-consumedMWh,withinBudget:consumedMWh<=allowanceMWh,waitMinutes:admit==='ready'?delayMinutes:0};
}
export function maintenanceState({sharedControl=false,configurationMatched=false,flowProven=false,restorationChecked=false}={}){
 const availableMW=sharedControl?0:6;
 return {availableMW,capacityMeetsLoad:availableMW>=5,canStart:availableMW>=5&&configurationMatched,canRestore:!sharedControl&&configurationMatched&&flowProven&&restorationChecked};
}
export function unavailableUnion(intervals,{windowStart=0,windowEnd=43200}={}){
 finite(windowStart,'Window start');finite(windowEnd,'Window end');if(windowEnd<=windowStart)throw new RangeError('Observation window must have positive duration');
 const clipped=intervals.map(([start,end])=>{finite(start,'Interval start');finite(end,'Interval end');if(end<start)throw new RangeError('Interval ends before it starts');return [Math.max(start,windowStart),Math.min(end,windowEnd)];}).filter(([start,end])=>end>start).sort((a,b)=>a[0]-b[0]);
 const merged=[];for(const [start,end]of clipped){const last=merged.at(-1);if(last&&start<=last[1])last[1]=Math.max(last[1],end);else merged.push([start,end]);}
 const downtime=merged.reduce((sum,[start,end])=>sum+end-start,0),duration=windowEnd-windowStart;
 return {merged,downtime,duration,availability:1-downtime/duration};
}
export function diagnosticEvidence(selected=[]){const set=new Set(selected);return {local: set.has('branch'),load:set.has('load'),configuration:set.has('mapping'),sufficient:set.has('branch')&&set.has('load')&&set.has('mapping')};}
