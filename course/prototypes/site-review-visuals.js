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
 return `<svg class="expansion-plan" viewBox="0 0 1000 430" role="img" aria-label="${shown?'Sequence: secure northern corridor rights, open alternate access, install and test replacement fiber, then transfer service before excavation':'Hall B excavation would cut the live hall access and the duct carrying both fiber services. The north corridor needs a surface-use agreement.'}">
 <rect x="28" y="24" width="944" height="380" rx="10" fill="var(--surface)" stroke="var(--line)" stroke-width="2"/>
 <path d="M48 60H944V117H48Z" fill="var(--panel)"/>${text(500,96,shown?'1 · Secure corridor rights':'Surface-use agreement unresolved','middle')}
 <path d="M892 280H325V220" fill="none" stroke="var(--line)" stroke-width="36"/>${text(825,333,'Site entry')}
 
 <rect x="230" y="140" width="190" height="80" rx="5" fill="var(--power)"/> <text x="325" y="188" fill="var(--paper)" text-anchor="middle" font-family="system-ui" font-size="24">Hall A · live</text>
 <path d="M525 164H785V311H525Z" fill="var(--heat)" fill-opacity=".13" stroke="var(--heat)" stroke-width="3" stroke-dasharray="8 5"/>${text(655,194,'Hall B','middle')}${text(655,221,'Excavation','middle')}
 <path d="M940 239H404V220M940 250H393V220" fill="none" stroke="var(--data)" stroke-width="4"/>
 ${shown?`<path d="M900 280V125H455V280H325V220" fill="none" stroke="var(--power)" stroke-width="9"/><path d="M935 240V111H440V155H420" fill="none" stroke="var(--data)" stroke-width="5"/>${text(525,156,'2 · Access + tested fiber')}${text(535,373,'3 · Transfer, then excavate')}`:`<circle cx="565" cy="257" r="48" fill="none" stroke="var(--heat)" stroke-width="3"/>${text(290,373,'Both fiber services share this duct')}`}
 </svg>`;
}
function expansionMobile(shown){
 return `<svg class="expansion-plan" viewBox="0 0 390 530" role="img" aria-label="Hall B excavation crosses the access and fiber paths to live Hall A; a corridor to the left needs surface rights.">
 <rect x="8" y="12" width="372" height="505" rx="10" fill="var(--surface)" stroke="var(--line)"/>
 <rect x="115" y="52" width="230" height="85" rx="6" fill="var(--power)"/><text x="230" y="102" text-anchor="middle" fill="var(--paper)" font-size="24">Hall A · live</text>
 <path d="M270 470V137" stroke="var(--line)" stroke-width="26"/>
 <path d="M237 470V137M228 470V137" stroke="var(--data)" stroke-width="4"/>
 <rect x="155" y="232" width="185" height="140" fill="var(--heat)" fill-opacity=".13" stroke="var(--heat)" stroke-width="3" stroke-dasharray="7 5"/>
 ${text(247,273,'Hall B','middle')}${text(247,302,'Excavation','middle')}${text(273,499,'Site entry','middle')}
 <path d="M50 480V110H115" fill="none" stroke="var(--power)" stroke-width="${shown?9:3}" stroke-dasharray="${shown?'none':'6 5'}"/>
 ${shown?'<path d="M220 469H67V126H115" fill="none" stroke="var(--data)" stroke-width="4"/>':''}
 <text transform="translate(31 398) rotate(-90)" font-size="18" fill="var(--text)">${shown?'1 · Rights → 2 · Access + tested fiber':'Alternative corridor · rights unresolved'}</text>
 ${shown?text(190,35,'3 · Transfer before excavation','middle'):''}
 </svg>`;
}
export function renderSiteReview(id,state,compact=false){
 if(id==='fiber-diversity') return result(`<div class="fiber-case"><figure class="fiber-campus"><img src="../assets/references/qts-suwanee-campus.png" alt="QTS's campus plan of its two Suwanee buildings"><figcaption>QTS Suwanee · campus plan</figcaption></figure><div class="fiber-options"><article><h2>Shared entry</h2><span>Counterexample</span>${entrances(true)}</article><article><h2>Three entrances</h2><span>QTS DC1 · topology sketch</span>${entrances(false)}</article></div></div>`, 'The original campus plan establishes the two-building QTS Suwanee setting. A shared entry counterexample is compared with three separated entry laterals as documented for DC1. Sketches show topology, not surveyed cable routes. DC2’s proposed four entrances are a separate building specification.');
 if(id==='service-check'){
  const shown=state.serviceAnswer==='shown';
  return result(`<div class="expansion-check">${expansionPlan(shown,compact)}<p class="expansion-prompt"${shown?' hidden':''}>${shown?'Keep the original connections until their replacements are working.':'What must be working before excavation starts?'}</p></div>`,shown?'Resolve the northern corridor rights, open alternate access, install and test replacement fiber, then transfer service before excavation. If rights cannot be secured, change the layout or schedule.':'Hall A is live. Hall B excavation crosses the operating access road and a shared fiber duct. A northern alternative needs a surface-use agreement. Propose a construction sequence that preserves the live service.');
 }
 return null;
}
