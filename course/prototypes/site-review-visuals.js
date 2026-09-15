const result = (markup, description) => ({ markup, description, format: 'html' });
const text=(x,y,words,anchor='start')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" fill="var(--text)" font-family="system-ui" font-size="21">${words}</text>`;
function entrances(shared) {
 const routes=shared
 ? '<path d="M35 65H90V173H180M35 270H105V189H180M430 310H120V205H180"/>'
 : '<path d="M35 65H100V140H180M440 60H370V105H315M435 295H400V260H320"/>';
 return `<svg viewBox="0 0 480 340" role="img" aria-label="${shared?'Counterexample: three routes converge at one building entrance':'QTS DC1 topology sketch: three separated building entry laterals'}"><rect x="180" y="105" width="140" height="155" rx="5" fill="var(--panel)" stroke="var(--text)" stroke-width="2"/><path d="M200 129H297M200 157H297M200 185H297M200 213H297M200 241H297" stroke="var(--line)" stroke-width="10"/><g fill="none" stroke="var(--data)" stroke-width="5" stroke-linejoin="round">${routes}</g>${shared?'<circle cx="174" cy="189" r="32" fill="none" stroke="var(--heat)" stroke-width="3" stroke-dasharray="5 4"/>':'<g fill="var(--power)"><circle cx="180" cy="140" r="7"/><circle cx="315" cy="105" r="7"/><circle cx="320" cy="260" r="7"/></g>'}</svg>`;
}
function expansionPlan(shown, compact){
 if(compact) return expansionMobile(shown);
 return `<svg class="expansion-plan" viewBox="0 0 1000 385" role="img" aria-label="${shown?'New access road and fiber bypass the Hall B excavation and reconnect to live Hall A.':'Hall B excavation crosses the access road and the duct carrying both fiber services to live Hall A.'}">
 <path d="M915 285H280V205" fill="none" stroke="var(--line)" stroke-width="28"/>
 <path d="M945 249H370V205M945 260H359V205" fill="none" stroke="var(--data)" stroke-width="4"/>
 <rect x="180" y="120" width="250" height="85" rx="5" fill="var(--power)"/><text x="305" y="171" fill="var(--paper)" text-anchor="middle" font-family="system-ui" font-size="25">Hall A · live</text>
 <rect x="535" y="164" width="260" height="163" rx="5" fill="none" stroke="var(--heat)" stroke-width="3" stroke-dasharray="8 5"/>
 ${text(665,194,'Hall B excavation','middle')}${text(230,332,'Access road')}${text(430,228,'Fiber duct')}${text(868,332,'Site entry')}
 ${shown?`<path d="M915 285V77H280V120" fill="none" stroke="var(--line)" stroke-width="28"/><path d="M915 285V77H280V120" fill="none" stroke="var(--power)" stroke-width="4"/>
 <path d="M945 249V35H460V154H430M945 260H956V24H449V143H430" fill="none" stroke="var(--data)" stroke-width="4"/>`:''}
 </svg>`;
}
function expansionMobile(shown){
 return `<svg class="expansion-plan" viewBox="0 0 390 480" role="img" aria-label="${shown?'New access road and fiber run to the left of the Hall B excavation.':'Hall B excavation crosses the access road and fiber duct to live Hall A.'}">
 <path d="M290 432V119" stroke="var(--line)" stroke-width="26"/>
 <path d="M237 432V119M228 432V119" stroke="var(--data)" stroke-width="4"/>
 <rect x="115" y="34" width="245" height="85" rx="6" fill="var(--power)"/><text x="237" y="85" text-anchor="middle" fill="var(--paper)" font-size="24">Hall A · live</text>
 <rect x="105" y="215" width="247" height="135" fill="none" stroke="var(--heat)" stroke-width="3" stroke-dasharray="7 5"/>
 ${text(159,253,'Hall B','middle')}${text(159,282,'excavation','middle')}${text(287,463,'Site entry','middle')}
 <text x="215" y="185" text-anchor="end" font-size="17" fill="var(--data)">Fiber duct</text><path d="M220 179H230" stroke="var(--data)"/>
 <text x="310" y="390" font-size="17" fill="var(--text)"><tspan>Access </tspan><tspan x="310" dy="22">road</tspan></text>
 ${shown?'<path d="M290 432H60V77H115" fill="none" stroke="var(--line)" stroke-width="26"/><path d="M290 432H60V77H115" fill="none" stroke="var(--power)" stroke-width="4"/><path d="M237 432V419H88V102H115M228 432V410H97V111H115" fill="none" stroke="var(--data)" stroke-width="4"/>':''}
 </svg>`;
}
export function renderSiteReview(id,state,compact=false){
 if(id==='fiber-diversity') return result(`<div class="fiber-case"><figure class="fiber-campus"><img src="../assets/references/qts-suwanee-campus.png" alt="QTS's campus plan of its two Suwanee buildings"><figcaption>QTS Suwanee · campus plan</figcaption></figure><div class="fiber-options"><article><h2>Shared entry</h2><span>Counterexample</span>${entrances(true)}</article><article><h2>Three entrances</h2><span>QTS DC1 · topology sketch</span>${entrances(false)}</article></div></div>`, 'The original campus plan establishes the two-building QTS Suwanee setting. A shared entry counterexample is compared with three separated entry laterals as documented for DC1. Sketches show topology, not surveyed cable routes. DC2’s proposed four entrances are a separate building specification.');
 if(id==='service-check'){
  const shown=state.serviceAnswer==='shown';
  const followup=shown?'<ol class="expansion-steps"><li>Build the new road and fiber</li><li>Test and switch to them</li><li>Start excavation</li></ol>':'<p class="expansion-prompt">What must move before digging starts?</p>';
  return result(`<div class="expansion-check">${expansionPlan(shown,compact)}${followup}</div>`,shown?'Build the alternative access road and replacement fiber while the original routes stay in service. Test the replacement connection and transfer service, then start the excavation. Both the road and fiber must bypass the work.':'Hall A is live. Hall B excavation crosses its access road and the duct carrying both fiber services. What must move before digging starts?');
 }
 return null;
}
