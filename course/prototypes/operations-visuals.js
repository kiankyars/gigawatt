import {maintenanceState} from './operations-model.js';
import {caseStoryVisual} from './operations-case-stories.js';
import {operationsComparison} from './operations-comparisons.js';

const arrow='<span class="o-arrow" aria-hidden="true">→</span>';
const card=(title,body,cls='')=>`<section class="o-card ${cls}"><h2>${title}</h2><p>${body}</p></section>`;
const result=(value,label,cls='')=>`<div class="o-result ${cls}"><strong>${value}</strong><span>${label}</span></div>`;
const rack=()=>'<div class="o-rack" aria-hidden="true"><i></i><i></i><i></i><i></i></div>';
const credit=(label,url)=>`<p class="o-credit"><a href="${url}" target="_blank" rel="noreferrer">${label}</a></p>`;
const photo=(asset,alt,caption,url)=>`<figure class="o-photo"><img src="../assets/references/${asset}" alt="${alt}"><figcaption><a href="${url}" target="_blank" rel="noreferrer">${caption}</a></figcaption></figure>`;

function admission(){
 const plot=wait=>`<section class="o-admission-plot"><h2>${wait?'Start the job at minute 3':'Start the job immediately'}</h2><svg viewBox="0 0 500 255" role="img" aria-label="${wait?'Waiting keeps heat within cooling capacity':'Starting early exceeds cooling by 1 MW for three minutes'}"><text x="10" y="22">MW</text>${[4,5,6,7].map(n=>`<path d="M50 ${235-n*27}H462" class="oa-grid"/><text x="38" y="${241-n*27}" text-anchor="end">${n}</text>`).join('')}${wait?'':'<rect x="50" y="73" width="206" height="27" fill="var(--warning-surface)"/>'}<path d="M50 100 H256 V46 H462" class="oa-cooling"/><path d="${wait?'M50 127 H256 V73 H462':'M50 73 H462'}" class="oa-load"/><path d="M256 30 V200" class="oa-marker"/><text x="50" y="226">0</text><text x="256" y="226" text-anchor="middle">3</text><text x="462" y="226" text-anchor="end">6 min</text><text x="268" y="24">Standby ready</text></svg><p>${wait?'4 MW → 6 MW after cooling starts':'1 MW excess heat for three minutes'}</p></section>`;
 return `<div class="o-stack"><div class="oa-legend"><span class="oa-load-key">Heat: 4 MW existing + 2 MW new job</span><span class="oa-cool-key">Cooling: 5 MW → 7 MW</span></div><div class="o-two">${plot(false)}${plot(true)}</div></div>`;
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

function replication(){
 return `<div class="o-stack"><p class="o-case-date">Gmail · February 2011 · storage-software update</p><div class="o-gmail-story"><section class="o-gmail-online"><h2>Live copies</h2><div class="o-copy-row"><span class="warning">Copy A</span><span class="warning">Copy B</span></div><p>The same software bug deletes mail from several copies.</p></section><span class="o-arrow">←</span><section class="o-gmail-tape"><h2>Offline tape</h2><strong>Earlier valid data</strong><p>Restore affected mail<br>over hours</p></section></div>${credit('Google · Gmail incident, February 2011','https://gmail.googleblog.com/2011/02/gmail-back-soon-for-everyone.html')}</div>`;
}

function llama(){
  return `<div class="o-stack"><p class="o-case-date">Meta · Llama 3 pre-training · 54-day snapshot</p><div class="o-two o-outcomes">${result('466','Job interruptions: 47 planned + 419 unexpected')}${result('&gt;90%','Effective training time')}</div>
    <div class="o-status-chain">${card('Detect','Identify the interruption.')}${arrow}${card('Recover','Restart and restore progress.')}${arrow}${card('Continue','Resume productive training.','positive')}</div>
    <p class="o-key">Only three incidents required significant manual intervention.</p>
    ${credit('Meta · The Llama 3 Herd of Models · §3.3.4','https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4')}</div>`;
}

function decision(state){
 return `<div class="o-stack o-decision"><div class="o-decision-givens"><section><h2>Row B</h2><strong>2.09 MW</strong><span>+0.70 MW proposed job</span></section><section><h2>Measured water path</h2><strong>50 kg/s · 30°C in</strong><span>Return limit: 40°C</span></section></div><p class="o-decision-equation">Q̇ = ṁ cₚ ΔT <span>cₚ = 4.18 kJ/(kg·°C)</span></p><p class="o-decision-question">How much flow would the extra job need?</p><button id="decision-reveal" aria-expanded="${Boolean(state.showDecision)}" aria-controls="decision-answer">${state.showDecision?'Hide calculation':'Show calculation'}</button><div id="decision-answer" class="o-decision-answer" role="status">${state.showDecision?'<strong>2,790 ÷ (4.18 × 10) = 66.75 kg/s</strong><p>About 67 kg/s total—or free 0.70 MW by moving existing work.</p>':''}</div></div>`;
}

export function operationsVisual(id,state={}){
  const story=caseStoryVisual(id);
  if(story!==null)return story;
  const comparison=operationsComparison(id,state);
  if(comparison!==null)return comparison;
  switch(id){
    case 'operations-purpose':return `<div class="o-opening"><section><div class="o-screen"><span>PLANT SUPPLY</span><b>30°C</b><small>Last observation 10:00</small><i>● Normal</i></div><h2>The plant dashboard</h2></section><div class="o-question">?</div><section>${rack()}<h2>Row B · 10:10</h2><p class="o-hot">Chip temperatures rising</p></section></div>`;
    case 'control-layers':return `<div class="o-three o-control-layers">${card('Local pump controls','Adjust pump speed to maintain the pressure or flow target.')}${card('Plant controls','Start another cooling unit and confirm it is ready.')}${card('Workload scheduler','Start, delay or move computing work.')}</div>`;
    case 'admit-work':return admission();
    case 'maintenance-scope':return maintenance(state);
    case 'replication-and-backup':return replication();
    case 'llama-recovery':return llama();
    case 'llama-maintenance':return `<div class="o-stack o-meta-maintenance">${photo('operations-meta-maintenance-train.jpg','Original Meta diagram: one maintenance group returns to compute service as the maintenance train advances to the next group.','Meta · maintenance trains · June 2024','https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/')}<p class="o-key">Purple: under maintenance · teal: available for compute</p></div>`;
    case 'operating-decision':return decision(state);
    default:throw new Error(`Unknown operations scene: ${id}`);
  }
}
