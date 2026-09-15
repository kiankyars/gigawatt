import { renderBypassDiagram } from './ups-bypass.js';
const frac = (top, bottom) => `<span class="fraction"><span>${top}</span><span>${bottom}</span></span>`;
export function renderRecoveryTime() {
 return `<div class="recovery-derivation" aria-label="Recovery time equals energy to replace divided by source power minus load power. The capacitor is missing five kilojoules."><div class="derivation-row">t = ${frac('Energy to replace', 'Source power − Load power')} = ${frac('½C(V<sub>target</sub>² − V<sub>initial</sub>²)', 'P<sub>source</sub> − P<sub>load</sub>')}</div><div class="derivation-row"><span class="math-term">½C(V<sub>target</sub>² − V<sub>initial</sub>²)</span><span class="math-term">= 64 kJ − 59 kJ = <strong>5 kJ</strong></span></div><div class="derivation-row"><span class="math-term">P<sub>extra</sub> = P<sub>source</sub> − P<sub>load</sub></span></div><div class="derivation-result">Recovery time = ${frac('5 kJ', 'Extra power')}</div><p>Constant positive surplus at the DC bus</p></div>`;
}
export function renderStoredEnergyIsolation() {
 return `<figure class="isolation-supplied-image"><img src="../assets/references/continuity-ac-dc-isolation-updated.png" alt="AC off. DC still live. The AC input to a UPS rectifier is disconnected, while a battery and converter remain connected to the DC bus and its capacitor remains charged. The added DC disconnect separates the load side, which is shown de-energized after discharge, from the still-live battery and capacitor section."></figure>`;
}
export function renderBypassCheck(state={},compact=false) {
 const answered=Boolean(state.bypassAnswer);
 const result=renderBypassDiagram({mode:'static',sourceAvailable:!answered,compact});
 return `<div class="bypass-exercise"><p class="service-scenario">The inverter has failed. Static bypass carries the load. Now utility power fails.</p><div class="ups-visual"><svg viewBox="${result.viewBox}" role="img" aria-label="A failed inverter blocks the battery path. The static bypass depends on its AC source.">${result.svg}</svg></div>${answered?`<div class="service-prompt">${state.bypassAnswer==='yes'?'No—the battery path still needs the failed inverter.':'Correct. The failed inverter blocks the battery path.'} A generator can restore bypass power after startup and transfer; it does not bridge this interruption.</div>`:'<p class="bypass-question">Will the load stay powered without interruption?</p>'}</div>`;
}

export function renderRedundancyMemes() {
 return `<div class="redundancy-memes"><figure><img src="../assets/references/continuity-datacentres-cartoon.png" alt="Cartoon: a man drinking water is told, Take it easy buddy. Think of the data centres."></figure><figure><img src="../assets/references/continuity-redundancy-meme.png" alt="Austin Powers: I see you don’t have enough redundancy in your data center. I also like to live dangerously."></figure></div>`;
}
