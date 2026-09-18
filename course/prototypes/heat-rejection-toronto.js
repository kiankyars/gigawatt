const enwave = 'https://www.enwave.com/case-studies/enwave-and-toronto-water-tap-into-innovative-energy-source';
const incident = 'https://www.datacenterknowledge.com/outages/toronto-flooding-kos-data-center-cooling-systems';
const operator = 'https://seclists.org/nanog/2013/Jul/130';
const photo = '../assets/references/toronto-151-front-allied.jpg';
const credit = (url, label) => `<p class="t-credit"><a href="${url}" target="_blank" rel="noopener">${label}</a></p>`;
const text = (x,y,label,cls='',anchor='middle') => `<text x="${x}" y="${y}" text-anchor="${anchor}" class="${cls}">${label}</text>`;
const pipe = (d,cls) => `<path d="${d}" class="t-pipe ${cls}"/>`;
const right = (x,y,cls) => `<path d="M${x-8} ${y-7}l8 7-8 7" class="t-direction ${cls}"/>`;
const rack = (x,y,cls='') => `<g class="t-rack ${cls}"><rect x="${x}" y="${y}" width="58" height="112" rx="5"/>${[12,35,58,81].map(a=>`<rect class="t-server" x="${x+8}" y="${y+a}" width="42" height="17" rx="2"/><circle cx="${x+42}" cy="${y+a+8}" r="2"/>`).join('')}</g>`;
function lakeCircuit(compact) {
 if(compact) return `<div class="t-mobile-circuit" role="img" aria-label="Lake Ontario water is treated for drinking, then absorbs heat through a heat exchanger and continues to the drinking-water supply. A separate district loop carries building heat back to this exchanger."><section class="t-potable-route"><h2>Toronto Water</h2><p>Lake Ontario</p><i>↓</i><p>Drinking-water treatment</p><i>↓</i><div class="t-mobile-exchanger">Heat exchanger <b>← Heat</b></div><i>↓</i><p>City drinking water</p></section><section class="t-district-route"><h2>Enwave district loop</h2><div class="t-mobile-loop"><p>Heat exchanger</p><div><span>Cool supply ↓</span><span>↑ Warm return</span></div><p>Downtown buildings</p></div></section></div>`;
 return `<svg class="t-lake-diagram" viewBox="0 0 860 470" role="img" aria-label="Separate potable-water and district cooling paths. Lake Ontario water passes through drinking-water treatment and a heat exchanger before entering the city water supply. The district circuit circulates between buildings and the exchanger.">
 ${text(100,38,'Lake Ontario','t-major')}${text(330,38,'Toronto Water','t-major')}
 <path d="M20 92Q40 80 60 92T100 92T140 92T180 92V252H20Z" class="t-lake"/>
 ${text(100,130,'Deep intake')}
 ${pipe('M75 215H145V170H250','t-potable')}${right(220,170,'t-potable')}
 <rect x="250" y="123" width="135" height="95" rx="8" class="t-equipment"/>
 ${text(317,158,'Drinking-water')}${text(317,187,'treatment')}
 ${pipe('M385 170H440','t-potable')}
 <rect x="440" y="117" width="140" height="232" rx="10" class="t-exchanger"/>
 ${text(510,88,'Heat exchanger','t-major')}
 ${pipe('M440 170H580','t-potable')}${pipe('M580 170H823','t-potable')}${right(800,170,'t-potable')}
 ${text(718,112,'City drinking')}${text(718,139,'water supply')}
 <path d="M470 204H550" class="t-separator"/>
 ${text(510,243,'Heat ↑','t-heat')}
 ${pipe('M747 354H475V300H543','t-warm')}
 ${pipe('M543 300H610V272H747','t-cool')}${right(690,272,'t-cool')}
 <path d="M636 346l-8 8 8 8" class="t-direction t-warm"/>
 <rect x="747" y="235" width="83" height="152" rx="5" class="t-building"/>
 ${[250,280,310,340].map(y=>`<path d="M762 ${y}h19m13 0h20" class="t-building-window"/>`).join('')}
 ${text(788,419,'Downtown')}${text(788,446,'buildings')}
 ${text(665,242,'Cool supply','t-cool-label')}${text(614,390,'Warm return','t-warm-label')}
 ${text(420,445,'Enwave district loop','t-major')}
 </svg>`;
}
function buildingFigure() {
 return `<figure class="t-building-photo"><img src="${photo}" alt="Archival Allied REIT photograph of the brick carrier-hotel building at 151 Front Street West, Toronto, with the CN Tower behind it."><figcaption><strong>151 Front Street West</strong><span>Toronto’s telecom hub</span>${credit(incident,'Photo: Allied REIT / Data Center Knowledge')}</figcaption></figure>`;
}
function outage(compact) {
 const width=compact?360:1050, height=compact?700:425;
 // Mobile puts the two infrastructure dependencies above the same building.
 if(compact) return `<svg class="t-outage-diagram" viewBox="0 0 ${width} ${height}" role="img" aria-label="July 8, 2013: utility power was lost. Building generators supplied electricity, but the external district cooling supply was disrupted.">
 ${text(180,30,'8 July 2013 · Toronto flood','t-date')}
 ${text(100,85,'Utility power')}${pipe('M100 105V150H180V270','t-disabled')}<path d="M89 125l22 22m0-22-22 22" class="t-cross"/>
 ${text(260,85,'Generator')}${pipe('M260 105V270H180V365','t-electric')}${text(270,313,'Running','t-electric-label')}
 <rect x="26" y="365" width="308" height="278" rx="10" class="t-equipment"/>
 ${text(180,400,'151 Front Street','t-major')}${rack(75,441)}${rack(148,441)}${rack(221,441)}
 ${pipe('M65 244V315H93V365','t-disabled')}<path d="M83 335l20 20m0-20-20 20" class="t-cross"/>
 ${text(99,192,'Enwave cooling')}${text(99,222,'Disrupted','t-fault-label')}
 ${text(180,595,'Powered equipment')}${text(180,626,'Losing cooling','t-fault-label')}
 </svg>`;
 return `<svg class="t-outage-diagram" viewBox="0 0 ${width} ${height}" role="img" aria-label="July 8, 2013: building generators continued supplying electricity at 151 Front Street while external district cooling was disrupted.">
 ${text(0,32,'8 July 2013 · Toronto flood','t-date','start')}
 ${text(125,106,'Utility power','t-major')}${pipe('M220 100H650V175','t-disabled')}<path d="M318 85l30 30m0-30-30 30" class="t-cross"/>
 <rect x="55" y="149" width="150" height="78" rx="8" class="t-equipment"/><circle cx="90" cy="188" r="16" class="t-generator"/><path d="M117 175h58m-58 13h58m-58 13h58" class="t-generator-lines"/>
 ${text(130,265,'Building generators','t-major')}${pipe('M205 190H470V175H688','t-electric')}${right(610,175,'t-electric')}
 ${text(490,151,'Electricity continues','t-electric-label')}
 ${text(126,350,'Enwave cooling','t-major')}${pipe('M244 344H688','t-disabled')}<path d="M455 329l30 30m0-30-30 30" class="t-cross"/>
 ${text(484,390,'Cooling disrupted','t-fault-label')}
 <rect x="688" y="94" width="335" height="307" rx="10" class="t-equipment"/>
 ${text(856,137,'151 Front Street','t-major')}${rack(741,204)}${rack(823,204)}${rack(905,204)}
 ${text(856,367,'Heat builds up','t-fault-label')}
 </svg>`;
}
function suites(compact) {
 return `<div class="t-suite-story"><div class="t-suites"><section class="t-suite t-hot-suite"><h2>Hotter suite</h2><div class="t-temperature"><strong>&gt;43°C</strong><span>Cold-side air</span></div><svg viewBox="0 0 260 130" role="img" aria-label="Some equipment shut down in the hotter suite; nonessential systems were stopped.">${rack(26,8,'t-stopped')}${rack(101,8)}${rack(176,8,'t-stopped')}</svg><p>Shut down nonessential systems</p></section><div class="t-move"><span>Move services</span><b aria-hidden="true">${compact?'↓':'→'}</b></div><section class="t-suite t-cool-suite"><h2>Cooler suite</h2><div class="t-recovered">Cooling recovered sooner</div><svg viewBox="0 0 260 130" role="img" aria-label="Services were transferred remotely to the cooler suite.">${rack(26,8)}${rack(101,8)}${rack(176,8)}</svg><p>Receive transferred services</p></section></div>${credit(operator,'Uberflip CTO’s firsthand account · 9 July 2013')}</div>`;
}
export function torontoVisual(id,compact=false) {
 if(id==='toronto-lake-cooling') return `<div class="t-toronto"><div class="t-lake-layout">${buildingFigure()}${lakeCircuit(compact)}</div>${credit(enwave,'Cooling path: Enwave + Toronto Water')}</div>`;
 if(id==='toronto-cooling-outage') return `<div class="t-toronto">${outage(compact)}${credit(incident,'PEER 1 statement reported by Data Center Knowledge · 9 July 2013')}</div>`;
 if(id==='toronto-operator-response') return suites(compact);
 throw new RangeError(`Unknown Toronto scene: ${id}`);
}
