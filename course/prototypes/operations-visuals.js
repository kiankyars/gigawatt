import {caseStoryVisual} from './operations-case-stories.js';
import {operationsComparison} from './operations-comparisons.js';
import {heatBalance} from './operations-model.js';
import {reserveVisual} from './operations-reserve.js';

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



function llama(){
  return `<div class="o-stack"><p class="o-case-date">Meta · Llama 3 pre-training · 54-day snapshot</p><div class="o-two o-outcomes">${result('466','Job interruptions: 47 planned + 419 unexpected')}${result('&gt;90%','Effective training time')}</div>
    <div class="o-status-chain">${card('Detect','Identify the interruption.')}${arrow}${card('Recover','Restart and restore progress.')}${arrow}${card('Continue','Resume productive training.','positive')}</div>
    <p class="o-key">Only three incidents required significant manual intervention.</p>
    ${credit('Meta · The Llama 3 Herd of Models · §3.3.4','https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4')}</div>`;
}

function decision(state){
 const current=heatBalance({flow:100,supply:30,returnTemperature:35}).heatMW;
 const maximum=heatBalance({flow:100,supply:30,returnTemperature:40}).heatMW;
 const headroom=(maximum-current).toFixed(2);
 const requiredFlow=Math.ceil((current+2.5)*1000/(4.18*(40-30)));
 return `<div class="o-stack o-decision"><div class="o-decision-givens"><section><h2>Row C · operating normally</h2><strong>${current.toFixed(2)} MW → water</strong><span>100 kg/s · 30°C in → 35°C out</span><span>Maximum return: 40°C</span></section><section><h2>Proposed workload</h2><strong>+2.50 MW</strong><span>Electrical headroom: 3 MW</span><span>Cooling-plant headroom: 3 MW</span></section></div><p class="o-decision-equation">Q̇ = ṁ cₚ ΔT <span>cₚ = 4.18 kJ/(kg·°C)</span></p><button id="decision-reveal" aria-expanded="${Boolean(state.showDecision)}" aria-controls="decision-answer">${state.showDecision?'Hide answer':'Show answer'}</button><div id="decision-answer" class="o-decision-answer" role="status">${state.showDecision?`<strong class="o-decision-no">Not at the current row flow.</strong><span>Row headroom: 100 × 4.18 × (40 − 35) ÷ 1,000 = <b>${headroom} MW</b></span><p>The added load needs ≈${requiredFlow} kg/s total row flow.</p>`:''}</div></div>`;
}

export function operationsVisual(id,state={}){
  const reserve=reserveVisual(id);
  if(reserve!==null)return reserve;
  const story=caseStoryVisual(id);
  if(story!==null)return story;
  const comparison=operationsComparison(id,state);
  if(comparison!==null)return comparison;
  switch(id){
    case 'operations-purpose':return `<div class="o-opening"><section><div class="o-screen"><span>PLANT SUPPLY</span><b>30°C</b><i>● Normal</i></div><h2>The plant dashboard</h2></section><div class="o-question">?</div><section>${rack()}<h2>Row B</h2><p class="o-hot">Chip: 85°C · limit: 80°C</p></section></div>`;
    case 'control-layers':return '<figure class="o-supplied-slide"><img src="../assets/references/three-control-layers-user.png" alt="Three control layers: local pump controls hold flow or pressure; plant controls bring cooling units on; the workload scheduler moves or delays compute."></figure>';
    case 'plant-controls-focus':return '<figure class="o-supplied-slide o-plant-focus"><a href="../assets/references/three-control-layers-user.png" target="_blank" rel="noopener" aria-label="Open original full-size control-layer diagram"><img src="../assets/references/three-control-layers-user.png" alt="Plant controls highlighted in the three-layer diagram: bring cooling units on. Local pump controls hold flow or pressure; the workload scheduler moves or delays compute."><svg viewBox="0 0 1672 941" aria-hidden="true" focusable="false"><rect x="600" y="314" width="477" height="508" rx="23"/></svg></a></figure>';
    case 'admit-work':return admission();
    case 'llama-recovery':return llama();
    case 'llama-maintenance':return `<div class="o-meta-maintenance"><div class="o-meta-figures"><figure><a href="../assets/references/operations-meta-maintenance-train.jpg" target="_blank" rel="noopener" aria-label="Open full-size Meta maintenance-train diagram"><img src="../assets/references/operations-meta-maintenance-train.jpg" alt="Original Meta diagram: one maintenance group returns to compute service as the maintenance train advances to the next group."></a></figure><figure><a href="../assets/references/operations-meta-maintenance-cost.webp" target="_blank" rel="noopener" aria-label="Open full-size Meta maintenance-cost graph"><img src="../assets/references/operations-meta-maintenance-cost.webp" alt="Meta’s qualitative maintenance-cost graph: smaller maintenance domains cause more interruptions; larger domains take more compute capacity out of service."></a></figure></div>${credit('Meta · maintenance trains and domain size · June 2024','https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/')}</div>`;
    case 'operating-decision':return decision(state);
    default:throw new Error(`Unknown operations scene: ${id}`);
  }
}
