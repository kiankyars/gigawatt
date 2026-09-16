import { renderDCArchitecturePreview } from './rack-dc-preview.js';
import { renderRackBusChoices } from './dc-architecture-review.js';
import { renderRackHardwareAnatomy } from './rack-hardware-anatomy.js';
import { renderCorePath, renderConversionChoices, renderVRMPhases } from './rack-converter-review.js';
import { renderBufferReview } from './rack-buffer-review.js';
import { renderRackPower } from './rack-power-visuals.js';
import { rackLedger, migrationDecision } from './rack-energy-model.js';
import { renderDCProtection } from './rack-energy-protection.js';
const n=(v,d=2)=>v.toLocaleString('en-US',{maximumFractionDigits:d});
export const escapeHTML=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const card=(label,value,detail='',extra='')=>`<section class="energy-card ${extra}"><p>${label}</p><strong>${value}</strong>${detail?`<span>${detail}</span>`:''}</section>`;

export function rackVisual(scene,state,compact) {
  const buffer=renderBufferReview(scene.id,state,compact);
  const updated=buffer || ({'rack-power-path':()=>renderCorePath(),'board-rails':()=>renderConversionChoices(),multiphase:()=>renderVRMPhases(state,compact)}[scene.id]?.());
  if(updated)return {markup:updated,description:scene.explanation.join(' ')};
  const result=renderRackPower(scene.id,state,compact);
  const rackMarkup=result.markup.replace('https://docs.nvidia.com/dgx/dgxgb200-user-guide/_images/hardware-rack-rear-gb300.png','../assets/references/nvidia-dgx-gb300-rear.png');
  const svg=`<svg class="rack-diagram" viewBox="${compact?'0 0 390 680':'0 0 1200 560'}" role="img" aria-labelledby="rack-title rack-description"><title id="rack-title">${escapeHTML(scene.title)}</title><desc id="rack-description">${escapeHTML(result.description)}</desc>${rackMarkup}</svg>`;
  return {markup:svg,description:result.description};
}

export function supplementalVisual(scene,s,compact=false) {
  if(scene.kind==='dc-rack-buses')return renderRackBusChoices();
  if(scene.kind==='hardware-anatomy')return renderRackHardwareAnatomy();
  if(scene.kind==='dc-preview')return renderDCArchitecturePreview();
  if(scene.kind==='review-figure')return scene.figureCaption
    ? `<figure class="review-figure"><svg viewBox="0 0 1672 941" role="img" aria-labelledby="review-title review-description"><title id="review-title">${escapeHTML(scene.title)}</title><desc id="review-description">${escapeHTML(scene.alt)} ${escapeHTML(scene.figureCaption)}</desc><image href="../assets/references/${escapeHTML(scene.asset)}" width="1672" height="941"/><text x="836" y="849" text-anchor="middle" font-family="Georgia,serif" font-size="33" fill="#10223b">${escapeHTML(scene.figureCaption)}</text></svg></figure>`
    : `<figure class="review-figure"><img src="../assets/references/${escapeHTML(scene.asset)}" alt="${escapeHTML(scene.alt)}"></figure>`;
  if(scene.kind==='dc-protection')return renderDCProtection(compact);
  if(scene.kind==='scales')return `<div class="scales-visual"><div class="scale-labels"><span>Rack bus</span><span>Board converters / VRMs</span><span>Local capacitors</span></div><img src="../assets/generated/rack-energy-scales.png" alt="Generic physical scale views: rear rack with copper busbars, a compute board, and capacitors beside a chip package."></div>`;
  if(scene.kind==='green-case')return `<div class="green-case"><figure class="green-site"><img src="../assets/references/distribution-green-zurich-west.jpg" alt="Exterior of Green’s Zurich-West data center, photographed in the ABB Review case study."><figcaption><a href="https://library.e.abb.com/public/1afa6036874fd0bb85257d5000710a17/DC%20for%20efficiency.pdf" target="_blank" rel="noopener">Green Zurich-West · ABB Review 4/2013</a></figcaption></figure><div class="green-system"><p class="green-date"><strong>May 2012</strong><span>1 MW DC system</span></p><p class="green-inlet">16 kV AC input <span aria-hidden="true">↓</span></p><section class="green-conversion"><h2>Central conversion unit</h2><div class="green-stages"><div><strong>Transformer</strong><span>1,100 kVA · AC step-down</span></div><b aria-hidden="true">→</b><div><strong>Rectifier modules</strong><span>AC → DC</span></div></div></section><div class="green-dc-bus"><span aria-hidden="true">↓</span><strong>380 V DC distribution</strong></div><div class="green-load"><span aria-hidden="true">↓</span><strong>Compatible HP servers and storage</strong></div></div></div>`;
  if(scene.kind==='ledger'){
    const a=rackLedger({auxiliaryKW:0});
    return `<div class="processor-ledger">${card('AC into this supply path',`${n(a.inputKW)} kW`)}<b>→</b>${card('PSU stage','97%',`${n(a.shelfLossKW)} kW heat`,'heat-card')}<b>→</b>${card('VRM stage','92%',`${n(a.regulatorLossKW)} kW heat`,'heat-card')}<b>→</b>${card('Processor rails','72 kW')}<p>${n(a.inputKW)} kW in = 72 kW to processor rails + ${n(a.regulatorLossKW+a.shelfLossKW)} kW heat</p></div>`;
  }
  if(scene.kind==='retrofit'){
    const a=migrationDecision({rackKW:s.rackKW});
    return `<div class="retrofit"><div class="retrofit-path">${card('Existing AC allocation','240 kW','Required operating condition')}${card('Shared sidecar','96% efficiency','3 kW upstream auxiliaries')}${card('Two compute racks',`2 × ${s.rackKW} kW DC`,'Same rack setting')}</div><div class="retrofit-account"><span>Required AC input</span><strong>(2 × ${s.rackKW}) ÷ 0.96 + 3 = ${n(a.inputKW)} kW</strong><p class="${a.powerPass?'pass':'hold'}">${a.powerPass?`${n(a.marginKW)} kW allocation remains`:`${n(-a.marginKW)} kW more than allocated`}</p></div></div>`;
  }
  if(scene.kind==='decision'){
    const options=[['full','Full racks now',120,240],['staged','Reduced racks first',110,240],['upgrade','Increase allocation',120,260]];
    const choices=options.map(([key,label,rackKW,allocationKW])=>{
      const a=migrationDecision({rackKW,allocationKW,deadlineWeeks:s.deadlineWeeks});
      const selected=s.decision===key;
      return `<button class="migration-option" data-decision="${key}" aria-pressed="${selected}"><span>${label}</span><strong>2 × ${rackKW} kW DC</strong><small>${allocationKW} kW AC allocation · ready week ${a.readyWeeks}</small>${s.migrationReveal?`<em>${n(a.inputKW)} kW AC input</em><span class="decision-verdict ${a.powerPass&&a.schedulePass?'pass':'hold'}">${!a.powerPass?'Power shortfall':!a.schedulePass?'Misses the service date':'Power and date fit'}</span>`:''}</button>`;
    }).join('');
    return `<div class="migration-check"><p class="energy-condition">Service in ${s.deadlineWeeks} weeks · customer accepts verified reduced throughput temporarily</p><div class="migration-options">${choices}</div>${s.migrationReveal?`<div class="release-evidence"><h2>${s.deadlineWeeks===3?'Reduced racks first can meet the early date.':'The larger allocation now becomes a feasible candidate.'}</h2><p>Release the route only with evidence for:</p><div><span>800 V input, connectors and DC protection</span><span>Startup, bursts and recharge within the input envelope</span><span>Cooling, network, service access and accepted workload</span></div></div>`:`<p class="decision-prompt">Choose a route, then reveal which constraints still need evidence.</p>`}</div>`;
  }
  throw new Error(`Unknown Chapter 8 scene: ${scene.id}`);
}
