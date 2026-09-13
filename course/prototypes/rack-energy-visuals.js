import { renderRackPower } from './rack-power-visuals.js';
import { rackLedger, dcPlanes, migrationDecision } from './rack-energy-model.js';
const n=(v,d=2)=>v.toLocaleString('en-US',{maximumFractionDigits:d});
export const escapeHTML=value=>String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const card=(label,value,detail='',extra='')=>`<section class="energy-card ${extra}"><p>${label}</p><strong>${value}</strong>${detail?`<span>${detail}</span>`:''}</section>`;

export function rackVisual(scene,state,compact) {
  const result=renderRackPower(scene.id,state,compact);
  const svg=`<svg class="rack-diagram" viewBox="${compact?'0 0 390 680':'0 0 1200 560'}" role="img" aria-labelledby="rack-title rack-description"><title id="rack-title">${escapeHTML(scene.title)}</title><desc id="rack-description">${escapeHTML(result.description)}</desc>${result.markup}</svg>`;
  return {markup:svg,description:result.description};
}

export function supplementalVisual(scene,s) {
  if(scene.kind==='scales')return `<div class="scales-visual"><div class="scale-labels"><span>Rack bus<small>Distributes power</small></span><span>Board converters<small>Create device rails</small></span><span>Local capacitors<small>Support fast changes</small></span></div><img src="../assets/generated/rack-energy-scales.png" alt="Generic physical scale views: rear rack with copper busbars, a compute board, and capacitors beside a chip package."><p class="scale-question">Keep these local functions as the upstream architecture changes.</p></div>`;
  if(scene.kind==='ledger'){
    const a=rackLedger(s);
    return `<div class="ledger-map"><div class="ledger-inlet">${card('Rack AC inlet',`${n(a.inputKW)} kW`,'All watts entering the rack')}${card('AC → DC shelf','97% efficiency',`${n(a.shelfLossKW)} kW heat`,'heat-card')}</div><div class="ledger-branches"><h2>${n(a.busKW)} kW on the DC bus</h2><div class="ledger-branch"><span class="branch-name">Processor branch</span>${card('Local regulators','92% efficiency',`${n(a.regulatorInputKW)} kW input · ${n(a.regulatorLossKW)} kW heat`)}<span class="flow-arrow" aria-hidden="true">→</span>${card('Processor rails','72 kW','Delivered to devices')}</div><div class="ledger-branch other-branch"><span class="branch-name">Other branch</span>${card('Other bus loads',`${a.auxiliaryKW} kW`,'Hosts, memory, switching and auxiliaries counted at this bus')}</div></div><div class="ledger-equation">${n(a.inputKW)} = 72 + ${a.auxiliaryKW} + ${n(a.regulatorLossKW)} + ${n(a.shelfLossKW)} <span>kW · devices + other loads + regulator heat + shelf heat</span></div></div>`;
  }
  if(scene.kind==='dc-planes'){
    const a=dcPlanes();
    return `<div class="dc-planes"><p class="energy-condition">100 kW at each DC plane · ideal conversion for this current comparison</p><div class="energy-comparison">${card('50 V rack bus',`${n(a.lowAmps)} A`,'100,000 W ÷ 50 V')}${card('800 V distribution',`${a.highAmps} A`,'100,000 W ÷ 800 V')}</div><div class="local-chain"><span>800 V distribution</span><b>→</b><span>Rack / board conversion</span><b>→</b><span>Low-voltage device rails</span></div><p class="energy-condition">Input ranges and conversion stages must match the chosen rack.</p></div>`;
  }
  if(scene.kind==='retrofit'){
    const a=migrationDecision({rackKW:s.rackKW});
    return `<div class="retrofit"><div class="retrofit-path">${card('Existing AC allocation','240 kW','Required operating condition')}${card('Shared sidecar','96% efficiency','3 kW upstream auxiliaries')}${card('Two compute racks',`2 × ${s.rackKW} kW DC`,'Same rack setting')}</div><div class="retrofit-account"><span>Required AC input</span><strong>(2 × ${s.rackKW}) ÷ 0.96 + 3 = ${n(a.inputKW)} kW</strong><p class="${a.powerPass?'pass':'hold'}">${a.powerPass?`${n(a.marginKW)} kW allocation remains`:`${n(-a.marginKW)} kW more than allocated`}</p></div><p class="energy-condition">The sidecar releases rack space. Its losses and auxiliaries still need supply.</p></div>`;
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
