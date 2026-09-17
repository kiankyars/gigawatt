import {coupledOutage,weatherCapacity,stalledJob,phaseAcceptance} from './integrated-cases-model.js';

const number=(value,digits=1)=>Number(value.toFixed(digits)).toLocaleString('en-US');
const footnote=text=>`<p class="ic-footnote">${text}</p>`;
const wrap=(body,boundary)=>`<div class="ic-comparison">${body}${footnote(boundary)}</div>`;
const conclusion=text=>`<p class="ic-conclusion">${text}</p>`;

function outageComparison(){
 const choices=[['existing','Existing design'],['energy','Add 200 kWh'],['auxiliaries','Also power the pumps']];
 return wrap(`<div class="ic-cards">${choices.map(([plan,label])=>{
  const m=coupledOutage({plan});
  return `<section class="ic-card"><h2>${label}</h2><div class="ic-main-value">${number(m.idealMinutes,2)} <span>min</span></div><p class="ic-value-label">ideal electrical duration</p><dl><div><dt>Battery supplies</dt><dd>${number(m.supportedMW)} MW</dd></div><div><dt>Pump supply</dt><dd class="${m.pumpSupplySurvives?'ic-positive':'ic-warning'}">${m.pumpSupplySurvives?'Powered':'Lost'}</dd></div></dl></section>`;
 }).join('')}</div>${conclusion('More battery energy cannot power a pump on a disconnected supply.')}`,
 'Starting storage: 600 kWh usable DC · 90% discharge efficiency · 2.5 MW inverter · pumps add 0.2 MW. All three designs still need evidence of safe temperatures through restoration.');
}

function weatherComparison(){
 const choices=[['none','Hot-day baseline'],['auxiliaries','Save 10 MW of auxiliaries'],['cooling','Add 10 MW of cooling']];
 return wrap(`<div class="ic-cards">${choices.map(([remedy,label])=>{
  const m=weatherCapacity({remedy});
  return `<section class="ic-card"><h2>${label}</h2><div class="ic-main-value">${m.racks} <span>racks</span></div><p class="ic-value-label">supportable at this operating point</p><dl><div><dt>IT electrical budget</dt><dd>${m.electricalMW} MW</dd></div><div><dt>Heat removal</dt><dd class="ic-warning">${m.coolingMW} MW</dd></div></dl></section>`;
 }).join('')}</div>${conclusion('Less auxiliary power saves energy. The cooling upgrade adds racks here.')}`,
 '100 MW service · 900 accepted paths at 100 kW/rack. These are supplied hot-day operating points: the cooling upgrade keeps auxiliary demand at 25 MW.');
}

function networkComparison(){
 const choices=[['none','Existing path'],['endpoint','Double sender'],['fabric','Double fabric']];
 const body=`<table class="ic-table"><caption class="ic-visually-hidden">The smallest payload-rate limit determines the transfer time and complete cycle.</caption><thead><tr><th scope="col">Change</th><th scope="col">Sender</th><th scope="col">Fabric</th><th scope="col">Receiver</th><th scope="col">Full cycle</th></tr></thead><tbody>${choices.map(([upgrade,label])=>{
  const m=stalledJob({upgrade});
  return `<tr><th scope="row">${label}</th>${['sender','fabric','receiver'].map(key=>`<td data-label="${key[0].toUpperCase()+key.slice(1)}"><span class="${m.binding.includes(key)?'ic-rate-binding':''}">${m.rates[key]} <small>GB/s</small></span></td>`).join('')}<td data-label="Full cycle" class="ic-cycle-answer">${m.cycleSeconds} s</td></tr>`;
 }).join('')}</tbody></table><p class="ic-key"><span class="ic-key-swatch"></span>Highlighted rates limit the whole path.</p>${conclusion('The faster sender still waits for the 40 GB/s fabric.')}`;
 return wrap(body,'800 GB payload · 60 s compute + transfer + 10 s other work · no overlap. Rates are supplied achieved payload limits; verify them after the change.');
}

function cycleRow(model,label){
 const saved=model.baselineSeconds-model.cycleSeconds;
 return `<section class="ic-cycle-row"><div class="ic-row-label"><h2>${label}</h2><strong>${model.cycleSeconds} s</strong></div><div class="ic-cycle-track" aria-label="${model.cycleSeconds} seconds: 60 compute, ${model.communicationSeconds} network and 10 other"><div class="ic-compute" style="--ic-span:60"><span class="ic-segment-label">Compute</span><strong>60 s</strong></div><div class="ic-network" style="--ic-span:${model.communicationSeconds}"><span class="ic-segment-label">Network</span><strong>${model.communicationSeconds} s</strong></div><div class="ic-other" style="--ic-span:10"><span class="ic-segment-label">Other</span><strong>10 s</strong></div>${saved?`<div class="ic-saved" style="--ic-span:${saved}"><span class="ic-segment-label">Saved</span><strong>${saved} s</strong></div>`:''}</div></section>`;
}

function jobConsequence(){
 const before=stalledJob(),after=stalledJob({upgrade:'fabric'});
 return wrap(`${cycleRow(before,'Existing path')}${cycleRow(after,'Fabric bottleneck doubled')}<p class="ic-cycle-legend" aria-hidden="true"><span>Compute</span><span>Network</span><span>Other</span><span>Saved</span></p><div class="ic-throughput"><div><strong>${number(3600/before.cycleSeconds,0)} → ${number(3600/after.cycleSeconds,0)}</strong><span>predicted completed cycles per hour</span></div><div><strong>+${number((after.throughputRatio-1)*100)}%</strong><span>more of the same completed work</span></div></div>`,
 'Same correct work per cycle, with no overlap. Measure the payload rate and complete cycle after the upgrade; check output correctness too.');
}

function stage(label,days,kind=''){
 return `<span class="ic-stage ${kind}" style="--ic-span:${days}"><b>${label}</b><small>${days} ${days===1?'day':'days'}</small></span>`;
}
function scheduleRow(label,end,stages,spare=0){
 return `<section class="ic-schedule-row"><h2>${label}</h2><div class="ic-schedule-track">${stages}${spare?`<i class="ic-schedule-spare" style="--ic-span:${spare}" aria-hidden="true"></i>`:''}</div><strong>Day ${end}</strong></section>`;
}

function phaseSchedule(){
 const normal=phaseAcceptance(),delayed=phaseAcceptance({cTest:'fail'}),afterB=phaseAcceptance({day:6});
 const b=stage('Network work',4)+stage('Test',2,'ic-stage-pass');
 const cStart=stage('Delivery',3)+stage('Fit',1);
 return wrap(`<div class="ic-schedule"><div class="ic-schedule-axis"><span>Day 0</span><span>Day 12</span></div>${scheduleRow('B',normal.bReadyDay,b,6)}${scheduleRow('C · test passes',normal.cReadyDay,cStart+stage('Test',3,'ic-stage-pass'),5)}${scheduleRow('C · test fails',delayed.cReadyDay,cStart+stage('Test fails',3,'ic-stage-fail')+stage('Correct',2,'ic-stage-fail')+stage('Retest',3,'ic-stage-pass'))}</div><div class="ic-schedule-results"><p><strong>${afterB.acceptedRacks} racks</strong><span>after B passes on day 6</span></p><p><strong>800 racks</strong><span>only after C passes: day 7, or day 12 after retest</span></p></div>`,
 'Original teaching schedule: groups proceed independently with qualified teams and resources available. Every opening date depends on a passing test; installed racks alone add no accepted service.');
}

export function integratedComparison(id,state={}){
 switch(id){
  case 'outage-choice':return outageComparison();
  case 'weather-choice':return weatherComparison();
  case 'job-choice':return networkComparison();
  case 'job-consequence':return jobConsequence();
  case 'phase-schedule':return phaseSchedule();
  default:return null;
 }
}
