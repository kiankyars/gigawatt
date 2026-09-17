import {maintenanceState} from './operations-model.js';
import {operationsComparison} from './operations-comparisons.js';

const arrow='<span class="o-arrow" aria-hidden="true">→</span>';
const card=(title,body,cls='')=>`<section class="o-card ${cls}"><h2>${title}</h2><p>${body}</p></section>`;
const result=(value,label,cls='')=>`<div class="o-result ${cls}"><strong>${value}</strong><span>${label}</span></div>`;
const rack=()=>'<div class="o-rack" aria-hidden="true"><i></i><i></i><i></i><i></i></div>';
const credit=(label,url)=>`<p class="o-credit"><a href="${url}" target="_blank" rel="noreferrer">${label}</a></p>`;
const photo=(asset,alt,caption,url)=>`<figure class="o-photo"><img src="../assets/references/${asset}" alt="${alt}"><figcaption><a href="${url}" target="_blank" rel="noreferrer">${caption}</a></figcaption></figure>`;
const deepmind='https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/';

function boundaries(){
  return `<div class="o-stack"><div class="o-loop">
    <section class="o-plant"><h2>Cooling plant</h2><div class="o-plant-icon" aria-hidden="true"><i></i><i></i></div><div class="o-tag">Supply 30°C<small>Upstream measurement</small></div></section>
    <div class="o-pipes"><div class="o-supply">Supply →</div><div class="o-tag positive"><b>Measure here</b><small>Row-branch flow + temperatures</small></div><div class="o-return">← Return</div></div>
    <section class="o-rack-zone"><h2>Row B</h2>${rack()}<div class="o-tag warning">Chips getting hotter</div></section>
    </div><div class="o-two o-local-readings">${card('At the water branch','Flow + supply and return temperatures')}${card('At the racks','Electrical power + chip temperatures')}</div></div>`;
}

function readiness(){
  return `<div class="o-stack"><div class="o-status-chain">
    ${card('1. Request','“Start the standby unit.”')}${arrow}
    ${card('2. Reply','“Command received.”')}${arrow}
    ${card('3. Physical proof','Current flow and temperature meet the requirement.','positive')}
    </div><div class="o-readiness-verdict"><span>Messages confirm communication.</span><strong>Measurements confirm cooling.</strong></div></div>`;
}

function admission(){
  // Both plans use the same load, cooling capacity and three-minute readiness time.
  const profile=(wait)=>`<section class="o-admission-case ${wait?'positive':''}"><h2>${wait?'Wait for measured readiness':'Start on the command'}</h2>
    <div class="o-phase"><span>During the 3-minute start</span><strong>${wait?4:6} MW heat</strong><b>5 MW cooling</b><em>${wait?'Existing work continues':'1 MW excess heat accumulates'}</em></div>
    <div class="o-phase o-after"><span>After cooling is proven ready</span><strong>6 MW heat</strong><b>7 MW cooling</b></div></section>`;
  return `<div class="o-stack"><p class="o-given">Existing work: 4 MW · with the new job: 6 MW · standby adds 2 MW cooling</p><div class="o-two o-admission">${profile(false)}${profile(true)}</div><p class="o-key">Enough cooling after startup does not establish enough cooling during startup.</p></div>`;
}

function maintenance(state){
  const m=maintenanceState({sharedControl:state.sharedControl});
  return `<div class="o-stack"><div class="o-control-supply ${state.sharedControl?'off':''}">Shared 24 V control supply <b>${state.sharedControl?'ISOLATED':'AVAILABLE'}</b></div>
    <div class="o-branch-lines" aria-hidden="true"><span>↓</span><span>↓</span><span>↓</span></div><div class="o-three">
    ${card('Unit A · 3 MW',state.sharedControl?'Control power lost':'Operating',state.sharedControl?'warning':'positive')}
    ${card('Unit B · 3 MW',state.sharedControl?'Control power lost':'Operating',state.sharedControl?'warning':'positive')}
    ${card('Unit C · 3 MW','Under maintenance','warning')}</div>
    <div class="o-two o-maintenance-result">${result('5 MW','Heat to remove')}${result(`${m.availableMW} MW`,'Cooling that can operate',m.capacityMeetsLoad?'':'warning')}</div></div>`;
}

function cloudflareFailure(){
  return `<div class="o-stack"><p class="o-case-date">Cloudflare · Portland · November 2023</p><div class="o-two o-failure-boundaries">
    ${card('Previously tested','Loss of the high-availability cluster’s part of the facility.')}
    ${card('What actually failed','The entire facility, including dependencies outside that cluster.','warning')}
    </div><div class="o-two o-outcomes">${result('Mostly continued','Distributed edge traffic')}${result('Disrupted','Dashboard, API and analytics','warning')}</div>
    ${credit('Cloudflare · November 2023 incident report','https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/')}</div>`;
}

function cloudflareRetest(){
  return `<div class="o-stack"><p class="o-case-date">Cloudflare · follow-up after the November 2023 outage</p><div class="o-status-chain">
    ${card('Improve','Add capacity and repair failover.')}${arrow}${card('Test','Remove a whole facility in February 2024.')}${arrow}${card('Real repeat','Another power failure on March 26.','warning')}
    </div><div class="o-two o-outcomes">${result('7 minutes','API + dashboard normal; no human intervention')}${card('Later that day','Analytics recovered separately.')}</div>
    ${credit('Cloudflare · April 2024 follow-up report','https://blog.cloudflare.com/major-data-center-power-failure-again-cloudflare-code-orange-tested/')}</div>`;
}

function replication(){
  return `<div class="o-stack"><div class="o-two o-replica-cases">
    <section class="o-card"><h2>One device fails</h2><div class="o-copy-row"><span class="warning">Copy A ✕</span><span class="o-arrow" aria-hidden="true">│</span><span class="positive">Copy B ✓</span></div><p>The other live copy can serve data.</p></section>
    <section class="o-card"><h2>A bad write reaches both</h2><div class="o-copy-row"><span class="warning">Bad data A</span>${arrow}<span class="warning">Bad data B</span></div><p>Recover an earlier valid version.</p></section>
    </div><div class="o-gmail-case"><b>Gmail · 2011</b><span>A storage software bug affected replicated copies. Offline tape preserved the data; recovery took hours.</span></div>
    ${credit('Google · Gmail incident, February 2011','https://gmail.googleblog.com/2011/02/gmail-back-soon-for-everyone.html')}</div>`;
}

function london(){
  return `<div class="o-stack"><p class="o-case-date">Google Cloud · London · July 2022</p><ol class="o-recovery-timeline">
    <li><b>Cooling failure</b><span>Part of one zone powered down.</span></li>
    <li><b>Cooling repaired</b><span>Service recovery continues.</span></li>
    <li class="positive"><b>14 h 15 min later</b><span>Initial cloud-service restoration milestone.</span></li>
    </ol><p class="o-key">Repair the facility, then restore the computing service.</p>
    ${credit('Google Cloud · final July 29 report · residual issues lasted longer','https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2')}</div>`;
}

function llama(){
  return `<div class="o-stack"><p class="o-case-date">Meta · Llama 3 pre-training · 54-day snapshot</p><div class="o-two o-outcomes">${result('466','Job interruptions: 47 planned + 419 unexpected')}${result('&gt;90%','Effective training time')}</div>
    <div class="o-status-chain">${card('Detect','Identify the interruption.')}${arrow}${card('Recover','Restart and restore progress.')}${arrow}${card('Continue','Resume productive training.','positive')}</div>
    <p class="o-key">Only three incidents required significant manual intervention.</p>
    ${credit('Meta · The Llama 3 Herd of Models · §3.3.4','https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4')}</div>`;
}

function decision(state){
  return `<div class="o-stack o-decision"><div class="o-three">
    ${card('Power','Row input is still 2.09 MW.')}${card('Cooling','Measured branch flow has halved.','warning')}${card('Before correction','The hot row was B; the command targeted A.','warning')}
    </div><p class="o-decision-question">The mapping is corrected. Can the new workload start now?</p>
    <button id="decision-reveal" aria-expanded="${Boolean(state.showDecision)}" aria-controls="decision-answer">${state.showDecision?'Hide release condition':'Show release condition'}</button>
    <div id="decision-answer" class="o-decision-answer" role="status">${state.showDecision?'<strong>Hold the extra work until local cooling is proven.</strong><p>Verify the correct row responds and its current flow and temperatures meet the requirement.</p><small>The mapping error explains a wrong-row response. It does not yet explain why flow fell.</small>':''}</div></div>`;
}

export function operationsVisual(id,state={}){
  const comparison=operationsComparison(id,state);
  if(comparison!==null)return comparison;
  switch(id){
    case 'operations-purpose':return `<div class="o-opening"><section><div class="o-screen"><span>PLANT SUPPLY</span><b>30°C</b><small>Last observation 10:00</small><i>● Normal</i></div><h2>The plant dashboard</h2></section><div class="o-question">?</div><section>${rack()}<h2>Row B · 10:10</h2><p class="o-hot">Chip temperatures rising</p></section></div>`;
    case 'measurement-boundaries':return boundaries();
    case 'control-layers':return `<div class="o-three o-control-layers">${card('Local pump controls','Adjust pump speed to maintain the pressure or flow target.')}${card('Plant controls','Start another cooling unit and confirm it is ready.')}${card('Workload scheduler','Start, delay or move computing work.')}</div>`;
    case 'google-cooling':return `<div class="o-case">${photo('operations-google-cooling-facility.jpg','Google data-center cooling infrastructure.','Google DeepMind · August 2018',deepmind)}<div class="o-case-copy"><div class="o-case-step"><b>AI selects an action</b><span>Choose within operator-defined limits.</span></div><div class="o-case-step"><b>Local controls check it</b><span>Apply only within local constraints.</span></div><div class="o-case-step"><b>Equipment responds</b><span>Operators can exit AI control.</span></div></div></div>`;
    case 'prove-readiness':return readiness();
    case 'admit-work':return admission();
    case 'google-demand-response':return `<div class="o-case">${photo('storage-google-dalles-repair.jpg','A Google technician replaces a motherboard at The Dalles data center.','Google · The Dalles facility operations','https://www.datacenters.google/discover-more/photo-gallery/')}<div class="o-case-copy"><h2>The Dalles, Oregon</h2><p>2023 pilot with Northern Wasco County PUD</p><div class="o-case-step"><b>Grid event notice</b><span>Identify the constrained hours.</span></div><div class="o-case-step"><b>Defer non-urgent work</b><span>Use later capacity and deadline slack.</span></div>${credit('Google Cloud · October 2023','https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption')}</div></div>`;
    case 'maintenance-scope':return maintenance(state);
    case 'cloudflare-pdx':return cloudflareFailure();
    case 'cloudflare-retest':return cloudflareRetest();
    case 'replication-and-backup':return replication();
    case 'london-recovery':return london();
    case 'llama-recovery':return llama();
    case 'operating-decision':return decision(state);
    default:throw new Error(`Unknown operations scene: ${id}`);
  }
}
