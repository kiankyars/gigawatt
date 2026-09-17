import {coupledOutage,weatherCapacity,densityRetrofit,phaseAcceptance} from './integrated-cases-model.js';
import {integratedComparison} from './integrated-comparisons.js';
const n=(value,digits=1)=>Number(value.toFixed(digits)).toLocaleString('en-US');
const metric=(value,label,tone='')=>`<div class="i-metric ${tone}"><strong>${value}</strong><span>${label}</span></div>`;
const result=(html,tone='')=>`<div class="i-result ${tone}">${html}</div>`;
const note=html=>`<p class="i-inputs">${html}</p>`;
const svg=(label,body,view='0 0 1120 330')=>`<svg viewBox="${view}" role="img" aria-label="${label}" xmlns="http://www.w3.org/2000/svg"><defs><marker id="i-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10Z" fill="context-stroke"/></marker></defs>${body}</svg>`;
const text=(x,y,label,cls='')=>`<text x="${x}" y="${y}" class="${cls}" text-anchor="middle">${label}</text>`;
const line=(x1,y1,x2,y2,cls='power')=>`<path class="i-wire ${cls}" d="M${x1} ${y1}L${x2} ${y2}" marker-end="url(#i-arrow)"/>`;
const box=(x,y,w,h,label,sub='',cls='')=>`<g class="i-machine ${cls}"><rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9"/>${text(x+w/2,y+h/2-(sub?6:-7),label)}${sub?text(x+w/2,y+h/2+25,sub,'small'):''}</g>`;
const rack=(x,y)=>`<g class="i-rack"><rect x="${x}" y="${y}" width="104" height="138" rx="5"/>${[16,47,78,109].map(d=>`<rect x="${x+12}" y="${y+d}" width="80" height="17" rx="3"/>`).join('')}</g>`;
const stack=(...items)=>`<div class="i-stack">${items.join('')}</div>`;
const metrics=(...items)=>`<div class="i-metrics">${items.join('')}</div>`;
const responsiveDiagram=(wide,narrow)=>`<div class="i-diagram"><div class="i-wide">${wide.replaceAll('i-arrow','i-arrow-wide')}</div><div class="i-narrow">${narrow.replaceAll('i-arrow','i-arrow-narrow')}</div></div>`;

function wholeSystem(close=false){const wide=svg('Electrical energy reaches racks; information supports useful work; rack heat passes through cooling to the outdoors.',
 box(10,103,170,95,'Electricity','watts in')+line(183,150,367,150)+rack(405,80)+rack(526,80)+text(512,253,'Compute + network')+
 box(384,0,256,48,'Information')+line(512,49,512,77,'information')+
 line(632,150,795,150,'information')+box(805,101,300,95,close?'Useful work':'Accepted service',close?'completed, correct work':'under stated conditions')+
 `<path class="i-wire heat" d="M514 270L514 302L907 302" marker-end="url(#i-arrow)"/>`+text(702,284,'Heat → outdoors','heat-label')+
 text(272,118,close?'Available power':'Outage','small')+text(702,122,close?'Working paths':'Network delay','small')+text(250,308,close?'Defined boundary':'Weather · density · handover','small'));
 const narrow=svg('Electricity and data enter compute; useful work leaves on the information path and heat leaves through cooling.',box(84,5,232,70,'Electricity','watts in')+line(200,78,200,113)+rack(148,122)+text(200,291,'Compute + network')+box(5,143,113,83,'Data','inputs')+line(120,185,143,185,'information')+line(200,303,200,337,'information')+box(69,343,262,79,close?'Useful work':'Accepted service','completed, correct work')+`<path class="i-wire heat" d="M260 195H369V493H316" marker-end="url(#i-arrow)"/>`+box(85,455,229,78,'Heat outdoors')+text(200,573,close?'Every path must meet':'Five changes. One system.','small'),'0 0 400 600');
 return responsiveDiagram(wide,narrow);
}

function outagePath(protectedPump=false){const wide=svg('IT is supported by a battery. The facility-loop pump loses power unless its supply is moved to the battery. Heat must still reach outdoor rejection.',
 box(8,32,215,95,'Battery + inverter','2.5 MW')+line(225,80,395,80)+rack(424,15)+text(475,189,'2 MW IT')+
 box(8,220,215,90,protectedPump?'Protected bus':'Utility bus',protectedPump?'0.2 MW cooling':'Supply lost',protectedPump?'':'off')+
 (protectedPump?`<path class="i-wire power" d="M116 128V215" marker-end="url(#i-arrow)"/>`:'')+
 line(225,263,620,263,protectedPump?'power':'broken')+
 box(636,220,200,88,'Facility pump',protectedPump?'Supply survives':'Pump stopped',protectedPump?'':'off')+
 line(531,83,690,83,'heat')+box(702,36,150,94,'Heat loop')+line(858,83,918,83,'heat')+box(929,36,181,94,'Outdoors')+
 `<path class="i-wire heat ${protectedPump?'':'broken'}" d="M737 218V135" marker-end="url(#i-arrow)"/>`+text(948,265,'Flow + limits?','heat-label'));
 const narrow=svg('Battery supports IT. The separate pump bus is lost unless moved to the battery. Thermal support needs observed flow and temperatures.',box(10,15,190,86,'Battery','2.5 MW inverter')+line(203,58,259,58)+rack(271,8)+text(323,177,'2 MW IT')+box(10,222,184,85,protectedPump?'Protected bus':'Utility bus',protectedPump?'0.2 MW cooling':'Supply lost',protectedPump?'':'off')+(protectedPump?line(101,104,101,216):'')+line(196,265,224,265,protectedPump?'power':'broken')+box(229,222,164,85,'Pump',protectedPump?'Powered':'Stopped',protectedPump?'':'off')+`<path class="i-wire heat" d="M323 184V201H205V353" marker-end="url(#i-arrow)"/>`+box(105,360,200,82,'Heat loop','Flow + limits?')+line(205,448,205,489,'heat')+box(105,494,200,78,'Outdoors'),'0 0 400 590');
 return responsiveDiagram(wide,narrow);
}

function limits(m){return `<div class="i-limits">${[['Power for racks',m.electricalMW],['Cooling',m.coolingMW],['Tested rack paths',m.pathMW]].map(([name,value])=>`<div><span>${name}</span><div class="i-limit-track"><i style="width:${Math.min(100,value)}%" class="${value===m.capacityMW?'binding':''}"></i></div><b>${n(value)} MW</b></div>`).join('')}</div>`}
function floorplan(architecture='b',route='blocked'){
 const blocked=architecture==='b'&&route==='blocked';
 const wide=svg('Room plan with a UPS module removal route. A sidecar in the service bay blocks the route; the revised position clears it.',
 `<rect class="i-room" x="35" y="15" width="1050" height="298" rx="8"/>`+
 box(65,44,190,115,'Existing UPS','module exits ↓')+
 `<path class="i-removal ${blocked?'blocked':''}" d="M160 162V265H1055" marker-end="url(#i-arrow)"/>`+
 rack(556,52)+rack(696,52)+text(675,218,'120 kW DC load')+
 (architecture==='b'?box(route==='blocked'?301:860,route==='blocked'?202:57,150,85,'Sidecar','AC → DC',blocked?'off':''):'')+
 text(600,294,blocked?'Removal route blocked':'UPS removal route clear',blocked?'heat-label':'')+
 text(1080,210,'Exit','small')+
 text(387,87,architecture==='a'?'A · conversion':'B · near-load', 'small')+text(387,114,architecture==='a'?'inside rack':'conversion','small'));
 const narrow=svg('Room plan: UPS removal follows the left aisle to the exit; a sidecar in that aisle blocks removal.',`<rect class="i-room" x="5" y="5" width="390" height="490" rx="8"/>`+box(25,30,171,88,'Existing UPS','module exits ↓')+`<path class="i-removal ${blocked?'blocked':''}" d="M107 128V446H357" marker-end="url(#i-arrow)"/>`+rack(248,33)+text(300,203,'120 kW DC')+(architecture==='b'?box(route==='blocked'?24:235,route==='blocked'?238:249,150,85,'Sidecar','AC → DC',blocked?'off':''):'')+text(209,392,blocked?'Removal route blocked':'Removal route clear',blocked?'heat-label':'')+text(357,482,'Exit','small'),'0 0 400 510');
 return responsiveDiagram(wide,narrow);
}

function cycle(seconds,label){const total=60+seconds+10;return `<div class="i-cycle"><div class="i-cycle-label"><b>${label}</b><strong>${total} s</strong></div><div class="i-cycle-track"><span class="compute" style="flex:60">Compute<br><b>60 s</b></span><span class="communicate" style="flex:${seconds}">Network<br><b>${seconds} s</b></span><span class="other" style="flex:10">Other<br><b>10 s</b></span>${total<90?'<span class="saved" style="flex:10">10 s<br>saved</span>':''}</div></div>`}
function groups(m){return `<div class="i-groups">${m.groups.map(group=>`<section class="i-group ${group.accepted?'accepted':'held'}"><div class="i-group-roof"></div><div class="i-group-body"><b>${group.id}</b><div class="i-mini-racks" aria-hidden="true">${Array.from({length:4},()=>'<i></i>').join('')}</div><strong>${group.racks} racks</strong><span>${group.accepted?'Complete paths accepted':group.id==='B'?'Network tests still needed':'Cooling tests still needed'}</span></div></section>`).join('')}</div>`}

function opening(state){
 return `<div class="i-stack i-opening">${note('Illustrative register: 800 installed racks, 100 MW supply, 100 kW per rack.')}${groups(phaseAcceptance())}<button id="opening-reveal" aria-expanded="${Boolean(state.openingReveal)}" aria-controls="opening-answer">${state.openingReveal?'Hide opening decision':'Show opening decision'}</button><div id="opening-answer" class="i-opening-answer" role="status">${state.openingReveal?'<strong>Open A: 300 racks, or 30 MW at this rack duty.</strong><p>B and C need completed tests before their racks can join.</p>':''}</div></div>`;
}

export function integratedCasesVisual(id,state={}){
 const comparison=integratedComparison(id,state);
 if(comparison!==null)return comparison;
 switch(id){
  case 'five-decisions':return stack(wholeSystem(),result('Five cases connect the facility to the work it can deliver.'));
  case 'outage-brief':return stack(outagePath(),metrics(metric('16.2 min','ideal electrical duration'),metric('12 min','planned restoration sequence'),metric('Unknown','time before temperatures exceed limits','warning')),note('2 MW IT; controls stay powered. Generator ready at minute 10, then 2 minutes to restore cooling.'));
  case 'outage-evidence':return stack(`<div class="i-test-path"><section><div class="i-symbol">↯</div><h2>Pump supply</h2><p>The pump stays powered<br>and measured flow continues.</p></section><span>→</span><section><div class="i-symbol heat">≈</div><h2>Temperatures</h2><p>Coolant and chips stay<br>within the required limits.</p></section><span>→</span><section><div class="i-symbol">✓</div><h2>Completed work</h2><p>The application keeps<br>producing correct results.</p></section></div>`,result('Test through the outage and restoration, with defined stopping conditions.'));
  case 'weather-brief':{const mild=weatherCapacity({weather:'mild'}),hot=weatherCapacity();return stack(`<div class="i-weather-pair"><section><h2>Mild weather</h2>${limits(mild)}${metric('700 racks','70 MW rack capacity')}</section><section><h2>Hot weather</h2>${limits(hot)}${metric('550 racks','55 MW rack capacity','warning')}</section></div>`,note('100 MW supply, 100 kW per rack. Auxiliary demand rises from 15 to 25 MW; rack inlet requirement stays fixed.'));}
  case 'weather-paths':{const m=weatherCapacity({remedy:'cooling',acceptedRacks:state.acceptedRacks??600,demandMW:58});return stack(limits(m),metrics(metric(`${m.capacityMW} MW`,'rack capacity'),metric('58 MW','actual rack demand'),metric('83 MW','total site demand')),note('Demand stays at 58 MW + 25 MW auxiliaries. Accepted paths include power, cooling and network to the same racks.'));}
  case 'density-brief':return stack(floorplan(),metrics(metric('120 kW','DC load in either option'),metric('160 kW','AC feeder limit'),metric('140 kW','room cooling limit')),result('A keeps conversion inside the rack. B adds the sidecar shown in the removal route.'));
  case 'density-ledger':return stack(`<div class="i-density-pair"><section><h2>A · inside the rack</h2><div class="i-density-flow"><strong>125 kW AC</strong><span>96% conversion</span><strong>120 kW DC</strong></div>${metric('5 kW','conversion loss')}</section><section><h2>B · sidecar + near-load stage</h2><div class="i-density-flow"><strong>126.24 kW AC</strong><span>97% × 98% conversion</span><strong>120 kW DC</strong></div>${metric('6.24 kW','conversion loss','warning')}</section></div>`,result('Both fit the power and cooling limits. B still needs a clear maintenance route.'),note('All conversion equipment is inside the room: AC input also becomes room heat. Efficiencies are supplied for this example.'));
  case 'density-route':{const m=densityRetrofit({architecture:'b',route:state.route??'blocked'});return stack(floorplan('b',state.route??'blocked'),metrics(metric('126.24 kW','power draw and room heat stay the same'),metric(m.accessPass?'Route clear':'Route blocked','UPS module removal',m.accessPass?'':'warning')),note('Clearing access resolves this layout issue. Equipment connections and the changeover still need acceptance.'));}
  case 'job-brief':return stack(cycle(20,'One complete cycle'),metrics(metric('800 GB','data to transfer'),metric('40 GB/s','achieved transfer rate'),metric('20 seconds','800 ÷ 40')),note('Same work in each cycle. Compute, transfer and other work happen one after another.'));
  case 'phase-brief':return `<div class="i-campus"><figure><img src="../assets/references/distribution-abilene-data-halls.jpg" alt="Aerial of data halls and outdoor equipment at the original Abilene campus"><figcaption><a href="https://www.oracle.com/data-centers/" target="_blank" rel="noopener noreferrer">Oracle · Abilene data halls · 15 July 2026</a></figcaption></figure><div><h2>Return to Abilene</h2><p>Which halls have the services and test results needed to open?</p><div class="i-case-boundary"><b>Next: an illustrative handover register</b><span>The rack counts and dates are teaching inputs, not Abilene operating data.</span></div></div></div>`;
  case 'phase-choice':return opening(state);
  case 'watts-to-work':return stack(wholeSystem(true),result('Capacity makes work possible. Measure the completed work itself.'));
  default:throw new Error(`Unknown integrated case scene: ${id}`);
 }
}
