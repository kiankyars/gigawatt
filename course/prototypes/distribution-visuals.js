import { loadFromDc, reservedOutput, phaseLedger, conversionPath, rowBudget, traceLoad } from './distribution-model.js';
import { scenes } from './distribution-scenes.js';

const esc = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const n = (value, digits=1) => value.toLocaleString('en-US',{maximumFractionDigits:digits,minimumFractionDigits:digits});
const ink='var(--text)', power='var(--power)', heat='var(--heat)', muted='var(--muted)', line='var(--line)';
const text = (x,y,lines,size=22,color=ink,anchor='middle') => `<text x="${x}" y="${y}" fill="${color}" font-size="${size}" text-anchor="${anchor}">${(Array.isArray(lines)?lines:[lines]).map((t,i)=>`<tspan x="${x}" dy="${i?size*1.3:0}">${esc(t)}</tspan>`).join('')}</text>`;
const rect = (x,y,w,h,color='var(--surface)',stroke=line) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="${color}" stroke="${stroke}" stroke-width="2"/>`;
const wire = (points,color=power,dash=false) => `<path d="${points}" fill="none" stroke="${color}" stroke-width="5" stroke-linejoin="round" ${dash?'stroke-dasharray="9 7"':''}/>`;
const arrow = (x,y,color=power) => `<path d="M${x-9},${y-6} L${x},${y} L${x-9},${y+6}" fill="none" stroke="${color}" stroke-width="3"/>`;
const box = (x,y,w,h,label,detail='',color=power) => rect(x,y,w,h,'var(--surface)',color)+text(x+w/2,y+(detail?30:h/2+8),label,21)+ (detail?text(x+w/2,y+h-18,detail,16,muted):'');
const svg = (markup, description, width=1120, height=420) => `<svg class="mechanism" viewBox="0 0 ${width} ${height}" role="img" aria-label="${esc(description)}">${markup}</svg>`;
const fact = (value,label,cls='') => `<div class="fact ${cls}"><strong>${value}</strong><span>${label}</span></div>`;
const strip = (...facts) => `<div class="facts">${facts.join('')}</div>`;
const node = (label,detail='',cls='') => `<div class="flow-node ${cls}"><strong>${label}</strong>${detail?`<span>${detail}</span>`:''}</div>`;
const flow = (...nodes) => `<div class="flow">${nodes.join('<span class="flow-arrow" aria-hidden="true">→</span>')}</div>`;
const note = (value,cls='') => `<p class="consequence ${cls}">${value}</p>`;
const inputs = value => `<p class="inputs">${value}</p>`;
const photo = (file,alt,credit,url) => `<figure class="case-photo"><img src="../assets/references/${file}" alt="${esc(alt)}"><figcaption><a href="${url}" target="_blank" rel="noopener">${credit}</a></figcaption></figure>`;
const compassURL='https://www.siemens.com/en-us/company/insights/compass-datacenters-case-study/';
const fujitsuURL='https://starlinepower.com/sites/default/files/files/starline_busway_fujitsu-case-study_US.pdf';
const greenURL='https://library.e.abb.com/public/1afa6036874fd0bb85257d5000710a17/DC%20for%20efficiency.pdf';

function campus(s,m) {
  const active=traceLoad(s.load), on=id=>active.path.includes(id)?power:line;
  if(m){
    let o=wire('M120 60V90',on('campus-bus'))+wire('M120 160V195',on('hall-feeder'))+wire('M120 265V300',on('transformer'));
    o+=box(40,5,220,55,'Campus connection','',on('service'));
    o+=box(40,90,220,70,'MV switchgear','13.8 kV AC',on('campus-bus'));
    o+=box(40,195,220,70,'Hall transformer','13.8 kV → 480 V',on('transformer'));
    o+=box(40,300,220,65,'Building bus','480 V AC',on('building-bus'));
    o+=wire('M120 365V400H60V445',on('row-bus'))+wire('M120 400H260V445',on('pump'));
    o+=box(5,445,150,70,'IT path','Row → rack',on('rack'))+box(195,445,160,70,'Cooling','Drive → pump',on('pump'));
    o+=wire('M260 125H345V205',on('future-feeder'))+wire('M345 205L322 229',on('future-feeder'))+wire('M345 245V262',line)+text(319,290,['Open','future','feeder'],15,muted);
    return svg(o,'The selected load shares upstream campus equipment; IT and cooling branch after the building bus. The future feeder is open.',390,545);
  }
  let o=wire('M180 200H870',on('campus-bus'));
  o+=box(10,160,170,80,'Connection','13.8 kV AC',on('service'));
  o+=box(250,150,180,100,'MV switchgear','Shared campus bus',on('campus-bus'));
  o+=box(500,155,175,90,'Transformer','13.8 kV → 480 V',on('transformer'));
  o+=box(750,160,175,80,'Building bus','480 V AC',on('building-bus'));
  o+=wire('M837 160V65H1010',on('row-bus'))+box(965,25,145,80,'IT path','Row → rack',on('rack'));
  o+=wire('M837 240V330H1010',on('pump'))+box(965,290,145,80,'Cooling','Drive → pump',on('pump'));
  o+=wire('M340 250V340H435',on('future-feeder'))+wire('M435 340L475 309',on('future-feeder'))+wire('M487 340H555',line)+box(555,305,165,75,'Future hall','Feeder open',line);
  o+=text(585,124,'Hall feeder',17,muted);
  return svg(o,'Trace the selected rack, cooling or future-hall path from the 13.8 kV campus supply. Dashed future feeder is open.');
}

function oneLine(m){
  const w=m?390:1120;
  let o=text(w/2,28,'480Y/277 V AC example',23);
  if(m){
    o+=box(80,57,230,60,'Single-line view');o+=wire('M195 117V175');o+=box(80,175,230,55,'Rack branch');
    o+=text(195,272,'Expanded conductors',23);
    ['L1','L2','L3','N','PE'].forEach((v,i)=>{let x=55+i*68; o+=text(x,318,v,18)+wire(`M${x} 340V515`,i<3?power:muted,i===4);});
    o+=text(195,558,['L1–L2: 480 V','L1–N: 277 V','PE: protective earth'],20);
  } else {
    o+=box(35,78,230,70,'Single-line view');o+=wire('M150 148V320')+box(35,320,230,60,'Rack branch');
    o+=text(682,88,'The same circuit has several conductors',23);
    ['L1','L2','L3','N','PE'].forEach((v,i)=>{let x=440+i*130;o+=text(x,132,v,19)+wire(`M${x} 150V300`,i<3?power:muted,i===4);});
    o+=text(685,346,'L1–L2: 480 V      L1–N: 277 V',22)+text(685,382,'PE bonds exposed conductive parts; it is not a load phase.',18,muted);
  }
  return svg(o,'A single-line diagram expands to three phases, neutral and protective earth in the specified 480Y/277 volt system.',w,m?640:420);
}

function switchDiagram(s,m){
 const w=m?390:1120, cy=m?210:205, x1=m?70:405,x2=m?270:715;
 let o=wire(`M${m?20:80} ${cy}H${x1}`,power)+wire(`M${x2} ${cy}H${m?365:1040}`,s.futureClosed?power:line);
 o+=`<circle cx="${x1}" cy="${cy}" r="7" fill="${power}"/><circle cx="${x2}" cy="${cy}" r="7" fill="${power}"/>`;
 o+=wire(`M${x1} ${cy}L${x2} ${s.futureClosed?cy:cy-105}`);
 o+=text(w/2,55,s.futureClosed?'Feeder connected':'Feeder disconnected',26);
 o+=text(m?78:215,cy+72,'13.8 kV AC',20)+text(m?280:910,cy+72,s.futureClosed?'13.8 kV AC':'No supply',20,s.futureClosed?power:muted);
 o+=text(w/2,cy+139,s.futureClosed?'The voltage level stays the same.':'The open contact interrupts this route.',m?18:24);
 return svg(o,'An open or closed teaching feeder changes connectivity without transforming voltage.',w,m?425:420);
}

function transformer(m){
 const w=m?390:1120;
 let o='';
 if(m){
  o+=rect(115,100,160,230,'var(--panel)',muted)+rect(151,138,88,154,'var(--paper)',muted);
  [0,1,2,3,4,5].forEach(i=>{o+=`<ellipse cx="126" cy="${137+i*28}" rx="43" ry="10" fill="none" stroke="${power}" stroke-width="5"/>`;});
  [0,1,2].forEach(i=>{o+=`<ellipse cx="263" cy="${162+i*51}" rx="41" ry="13" fill="none" stroke="${heat}" stroke-width="5"/>`;});
  o+=text(87,53,['AC input','More turns'],20,power)+text(292,53,['AC output','Fewer turns'],20,heat);
  o+=text(195,385,['Changing flux links','the insulated windings.'],22)+text(195,478,['Voltage ratio ≈ turns ratio','Lower voltage → higher current'],20);
 } else {
  o+=rect(380,75,350,230,'var(--panel)',muted)+rect(444,129,222,122,'var(--paper)',muted);
  [0,1,2,3,4,5].forEach(i=>{o+=`<ellipse cx="403" cy="${102+i*34}" rx="64" ry="13" fill="none" stroke="${power}" stroke-width="5"/>`;});
  [0,1,2].forEach(i=>{o+=`<ellipse cx="703" cy="${129+i*60}" rx="64" ry="18" fill="none" stroke="${heat}" stroke-width="5"/>`;});
  o+=text(155,150,['AC input','More winding turns'],24,power)+text(946,150,['AC output','Fewer winding turns'],24,heat);
  o+=text(555,180,['Changing','magnetic flux'],22)+text(555,354,'Voltage ratio ≈ turns ratio',28)+text(555,394,'Power in = power out + core and winding heat',23);
 }
 return svg(o,'A magnetic core links separate windings. Fewer secondary turns lower AC voltage, with corresponding higher current for transferred power.',w,m?555:420);
}

function route(s,m){
 const atHall=s.stepdown==='hall';
 return inputs('2 MW delivered • balanced three-phase • PF 1')+
 flow(node('Campus connection','13.8 kV AC'),...(atHall?[]:[node('Transformer','13.8 kV → 480 V')]),node('450 m campus route',atHall?'13.8 kV · 84 A':'480 V · 2,406 A',atHall?'':'warm'),...(atHall?[node('Transformer','13.8 kV → 480 V')]:[]),node('20 m hall route','480 V · 2,406 A'),node('Hall load','2 MW'))+
 note(atHall?'The long route carries medium voltage; the high-current route is short.':'Stepping down at the entrance makes the long route carry low-voltage current.');
}

function row(s,m){
 const loads=Array(s.rowCount??3).fill(40), r=rowBudget(loads);
 const w=m?390:1120, positions=loads.map((_,i)=>m?45+i*300/(loads.length-1):220+i*800/(loads.length-1));
 let o=wire(`M${m?20:90} 110H${positions.at(-1)}`);
 o+=text(m?195:560,42,`End feed: ${n(r.currentA,0)} A / 250 A usable budget`,m?20:27,r.currentA>250?heat:ink);
 loads.forEach((kw,i)=>{const x=positions[i];o+=wire(`M${x} 110V210`)+rect(x-(m?26:75),210,m?52:150,95)+text(x,247,`Rack ${i+1}`,m?12:22)+text(x,281,'40 kW',m?13:23,power);o+=text(x+(m?23:43),180,`${n(r.branchA[i],0)} A`,m?13:19);if(i<loads.length-1)o+=text((x+positions[i+1])/2,90,`${n(r.segmentsA[i+1],0)} A`,m?12:19,muted);});
 o+=text(w/2,360,s.rowCount===5?'End feed exceeds 250 A; each branch is still 56 A.':'Every shared segment carries its downstream sum.',m?17:25);
 return inputs('Row example • 415 V line-to-line • balanced three-phase • PF 1')+svg(o,'Branch currents add toward the busway end feed. Three racks need 167 amps, four need 223, and five need 278, exceeding the supplied 250 amp budget.',w,400);
}

function phaseBars(s,m){
 const values=s.balanced?[380,380,380]:[460,350,330], w=m?390:1120;
 let o=text(w/2,34,'Each conductor: 400 A usable limit',m?21:27);
 const xs=m?[70,195,320]:[280,560,840], base=330, scale=.5;
 xs.forEach((x,i)=>{const over=values[i]>400;o+=rect(x-(m?33:60),base-values[i]*scale,m?66:120,values[i]*scale,over?heat:power,'none')+text(x,base-values[i]*scale-17,`${values[i]} A`,m?19:26,over?heat:ink)+text(x,370,`Phase ${'ABC'[i]}`,m?18:22);});
 o+=`<path d="M20 130H${w-20}" stroke="${heat}" stroke-width="2" stroke-dasharray="8 6"/>`;
 return inputs('Both allocations average 380 A • phase-to-neutral branch example')+svg(o,'Equal average phase current can hide an overloaded conductor; compare each phase with its own 400 amp limit.',w,405)+note(s.balanced?'All three phases fit the supplied limit.':'Phase A exceeds its limit by 60 A. Total load alone misses it.');
}

function conversion(s){
 const blocks=s.placement==='rack'?[node('Electrical room','AC switchboard'),node('Row route','AC'),node('Rack','AC/DC → DC load')]:s.placement==='row'?[node('Electrical room','AC switchboard'),node('Row sidecar','AC/DC'),node('Short row route','DC', 'warm'),node('Compatible rack','DC input')]:[node('Electrical room','AC/DC'),node('Row route','DC','warm'),node('Compatible rack','DC input')];
 return flow(...blocks)+`<div class="interface-grid"><div><strong>Changes downstream</strong><span>Supply type and voltage<br>Connectors and load input<br>Switching and protection</span></div><div><strong>Still upstream</strong><span>Campus connection<br>Shared feeder and transformer<br>Facility load and loss account</span></div></div>`;
}

function meters(s,m){
 const facility=s.meter==='facility',w=m?390:1120;
 let o='';
 if(m){
  o+=box(85,10,220,75,'Facility meter','5.8 MW',facility?power:line)+wire('M195 85V135H95V185',facility?power:line)+wire('M195 135H300V345',facility?power:line);
  o+=box(5,185,185,75,'Distribution','4.8 MW input',facility?power:line)+wire('M95 260V345',power);
  o+=wire('M190 222H240',heat)+arrow(240,222,heat)+text(250,255,['0.2 MW','heat'],16,heat);
  o+=box(5,345,185,85,'IT output meter','4.6 MW',power)+box(210,345,175,85,'Auxiliaries','1.0 MW',facility?power:line);
  o+=text(195,490,facility?['IT + auxiliaries + losses','are inside this account.']:['IT output excludes the','separately fed auxiliaries.'],21);
 }else{
  o+=box(40,150,215,90,'Facility meter','5.8 MW',facility?power:line)+wire('M255 195H375',facility?power:line)+wire('M375 195V85H480',facility?power:line)+wire('M375 195V330H805',facility?power:line);
  o+=box(480,40,235,90,'Distribution','4.8 MW input',facility?power:line)+wire('M715 85H805',power)+box(805,40,270,90,'IT output meter','4.6 MW',power);
  o+=wire('M597 130V170H700',heat)+arrow(700,170,heat)+text(760,181,'0.2 MW heat',19,heat);
  o+=box(805,285,270,90,'Auxiliaries','1.0 MW',facility?power:line);
  o+=text(600,213,facility?'IT + auxiliaries + losses':'IT output boundary',24,facility?power:muted);
 }
 return svg(o,'The facility meter is upstream of both the IT path and the parallel auxiliary branch. The IT output meter is downstream of electrical losses and excludes auxiliaries.',w,m?545:420);
}

function building(m){
 const w=m?390:1120;
 const labels=[['IT feeder','Continuity block','Row busway','Rack supplies'],['Cooling feeder','Drive and motor','Pump','Moves coolant'],['House feeder','Panelboard','Building services','Lights + controls']];
 let o='';
 if(m){
  o+=box(85,5,220,70,'Transformer','480 V AC')+wire('M195 75V110')+box(85,110,220,75,'Switchboard','Incoming supply → bus');
  o+=wire('M195 185V205H30V582');
  labels.forEach(([a,b,c,d],i)=>{const y=235+i*150;o+=wire(`M30 ${y+47}H65`)+box(65,y,145,95,a.includes(' ')?a.split(' '):a,b)+wire(`M210 ${y+47}H245`)+box(245,y,140,95,c.includes(' ')?c.split(' '):c,d);});
 }else{
  o+=box(140,10,245,85,'Transformer','480 V AC')+wire('M385 52H650')+box(650,10,285,85,'Switchboard','Incoming supply → busbars')+wire('M792 95V145H180V185')+wire('M792 145H940V185')+wire('M560 145V185');
  labels.forEach(([a,b,c,d],i)=>{const x=180+i*380;o+=box(x-155,185,310,80,a,b)+wire(`M${x} 265V315`)+box(x-155,315,310,80,c,d);});
 }
 return svg(o,'The transformer supplies a switchboard bus with three connected outgoing paths: IT through continuity equipment to row busway, cooling through its drive to a pump, and a house panel to controls and lighting.',w,m?655:420);
}

function ledgerCard(d,title){
 return `<div class="ledger"><h2>${title}</h2><div class="ledger-row"><span>IT output</span><strong>${n(d.itMW,2)} MW</strong></div><div class="ledger-row"><span>Auxiliaries</span><strong>${n(d.auxiliaryMW,2)} MW</strong></div><div class="ledger-row"><span>Electrical losses</span><strong>${n(d.lossMW,2)} MW</strong></div><div class="ledger-row total"><span>Facility input</span><strong>${n(d.inputMW,2)} MW</strong></div></div>`;
}
function capacity(d){return `<div class="capacity"><div class="capacity-item ${d.serviceHeadroomMW<0?'over':''}"><span>Service</span><strong>${n(d.inputMW,2)} / ${n(d.serviceMW,1)} MW</strong><span>${d.serviceHeadroomMW<0?'Exceeds by':'Margin'} ${n(Math.abs(d.serviceHeadroomMW),2)} MW</span></div><div class="capacity-item ${d.branchHeadroomMW<0?'over':''}"><span>IT branch</span><strong>${n(d.itMW,2)} / ${n(d.branchMW,1)} MW</strong><span>${d.branchHeadroomMW<0?'Exceeds by':'Margin'} ${n(Math.abs(d.branchHeadroomMW),2)} MW</span></div></div>`;}

export function renderDistribution(id,state={},compact=false){
 const s=state, m=compact, model=loadFromDc({powerFactor:s.powerFactor??.9});
 let markup='';
 switch(id){
 case 'distribution-purpose':
  markup=`<div class="purpose-map">${flow(node('Campus','Available connection'),node('Building','Shared transformer'),node('Row','Feeder and busway'),node('Rack','Required load'))}<div class="opening-question">Where does the next load run out of usable capacity?</div></div>`;break;
 case 'abilene-distribution':markup=`<div class="split">${photo('distribution-abilene-data-halls.jpg','Oracle aerial of data-hall buildings at the original Abilene campus, dated July 15, 2026.','Oracle · Abilene data halls · 15 July 2026','https://www.oracle.com/data-centers/')}<div class="stack">${flow(node('Which hall?','Identify its supply branch'),node('Which loads?','Include cooling and controls'),node('Which limits?','Read every interface on the path'))}</div></div>`;break;
 case 'campus-route': markup=inputs('Campus → building → load • normal supply')+campus(s,m);break;
 case 'one-line':markup=oneLine(m);break;
 case 'feeder-switching':markup=switchDiagram(s,m)+inputs('Unloaded future feeder');break;
 case 'compass-skid':markup=`<div class="split">${photo('distribution-compass-switchgear.jpg','Siemens 8DJH 36 switchgear with three cable terminals visible in the Compass project factory photograph.','Siemens · Compass case photograph',compassURL)}<div class="stack">${flow(node('MV switchgear','Connect, disconnect, measure'),node('Transformer','Change AC voltage'))}${note('One transportable assembly.<br>Two separate electrical jobs.')}<p class="inputs">Compass + Siemens • integrated MV skid<br>Photo: the switchgear portion</p></div></div>`;break;
 case 'transformer':markup=transformer(m);break;
 case 'local-stepdown':markup=route(s,m);break;
 case 'building-branches':markup=building(m);break;
 case 'distribution-units':markup=`<div class="compare"><div><h2>Floor PDU with transformer</h2>${flow(node('480 V AC','Input'),node('Transformer','480 → 208Y/120 V'),node('Branch panel','Breakers + meters'))}</div><div><h2>Rack PDU without transformer</h2>${flow(node('208 V AC','Input'),node('Distribution','Outlets + optional meters'),node('208 V AC','Server power supplies'))}</div></div>`+note('Both distribute power. Only the specified transformer changes voltage.');break;
 case 'fujitsu-busway':markup=`<div class="split">${photo('distribution-fujitsu-outlets.jpg','Blue rack-supply connectors on busway tap-off boxes in Starline’s Fujitsu case study.','Starline / Legrand · Fujitsu case study, 2018',fujitsuURL)}<div class="stack">${strip(fact('250 A','Selected Track Busway product'))}${flow(node('Existing hall','Cables under the floor'),node('Expansion','Overhead busway + tap-off meters'))}${note('Keep the floor air path clear.<br>Place new circuits at the rack.')}</div></div>`;break;
 case 'busway-branches':markup=`<div class="split">${photo('distribution-fujitsu-tapoffs.jpg','Busway tap-off boxes with disconnect handles in the Fujitsu case study.','Starline / Legrand · tap-off photograph',fujitsuURL)}<div class="stack">${flow(node('End feed','Supplies the shared bus'),node('Tap-off','Branch connection + protection'),node('Rack PDU','Supplies server outlets'))}${note('The tap-off connects to the bus.<br>It does not increase the bus rating.')}</div></div>`;break;
 case 'row-growth':markup=row(s,m);break;
 case 'meter-boundary':{
  markup=inputs('Supplied phase demand • IT, auxiliaries and upstream IT-path losses counted separately')+meters(s,m);break;}
 case 'output-to-input':markup=inputs('900 kW DC required • converter efficiency 96%')+flow(node('AC input','900 ÷ 0.96 = 937.5 kW'),node('Converter','96% of input reaches output'),node('DC output','900 kW'))+`<div class="heat-drop">↓ ${fact('37.5 kW','Heat at the converter','warm')}</div>`;break;
 case 'apparent-power':markup=inputs('Same 937.5 kW converter input • total power factor 0.90')+`<div class="equation">S = P ÷ PF</div>`+strip(fact('937.5 kW','Real power'),fact('1,041.7 kVA','Apparent power'))+note('Voltage and current set the apparent-power burden.<br>The kVA − kW difference is not a heat term.');break;
 case 'current-rating':markup=inputs('900 kW DC • 96% conversion • PF 0.90 • balanced 480 V line-to-line RMS')+`<div class="equation">I = S ÷ (√3 × V<sub>LL</sub>)</div>`+strip(fact('1,253 A','AC line current'),fact('1,041.7 kVA','Required input'),fact('1,000 kVA','Usable transformer limit','warm'))+note('The transformer exceeds its supplied limit by 4.2%.','warm');break;
 case 'power-factor':markup=inputs('Fixed: 900 kW DC output • 96% converter efficiency • balanced 480 V AC input')+strip(fact(`${n(model.apparentKVA)} kVA`,'Apparent power'),fact(`${n(model.currentA,0)} A`,'Line current'),fact(`${n(model.lossKW)} kW`,'Converter heat'))+flow(node('Transformer limit','1,000 kVA'),node(model.passes?'Fits this kVA screen':'Exceeds this kVA limit',`${n(model.loading*100)}% loading`,model.passes?'':'warm'))+note('Real input stays at 937.5 kW in this converter model.');break;
 case 'phase-loading':markup=phaseBars(s,m);break;
 case 'thermal-limits':markup=inputs('Balanced three-phase conductor example • 0.020 Ω per phase held fixed')+`<div class="compare heat-compare"><div><h2>200 A</h2><div class="loss-bar" style="--amount:25%"></div><strong>3 × 200² × 0.020 = 2.4 kW</strong></div><div><h2>400 A</h2><div class="loss-bar" style="--amount:100%"></div><strong>3 × 400² × 0.020 = 9.6 kW</strong></div></div>`+note('Twice the current produces four times the conductor heat.')+inputs('Applicable limits also depend on ambient temperature, enclosure and harmonic heating.');break;
 case 'reserve':{const r=reservedOutput({reserve:s.reserve??.2});markup=inputs('1,200 kVA usable equipment limit • PF 0.90 • conversion efficiency 96%')+`<div class="reserve-bar"><span style="width:${(1-(s.reserve??.2))*100}%">${n(r.budgetKVA,0)} kVA for current load</span>${s.reserve?'<span class="held">240 kVA<br>held for expansion</span>':''}</div>`+flow(node('AC budget',`${n(r.budgetKVA,0)} kVA`),node('Real input',`${n(r.inputKW,2)} kW`),node('DC output',`${n(r.outputKW,2)} kW`))+note('A stated expansion reserve is separate from thermal derating and redundancy.');break;}
 case 'conversion-locations':markup=conversion(s);break;
 case 'green-dc':markup=`<div class="split">${photo('distribution-green-zurich-west.jpg','Exterior of Green’s Zurich-West data center from the ABB Review case photograph, including a Green vehicle.','ABB Review 4/2013 · Green Zurich-West',greenURL)}<div class="stack">${strip(fact('1 MW','DC system installed'),fact('May 2012','Expansion opened'))}${flow(node('Central conversion','AC → DC'),node('Compatible HP equipment','DC server and storage inputs'))}${note('The change extended all the way<br>to the IT power interface.')}</div></div>`;break;
 case 'green-path':markup=inputs('Green Zurich-West • ABB technical account, 2013')+flow(node('MV input','16 kV AC'),node('Central unit','1,100 kVA transformer → rectifier'),node('DC distribution','380 V DC in the figure'),node('Compatible IT','DC/DC at the load'))+`<div class="interface-grid"><div><strong>Transformer</strong><span>AC voltage change<br>Magnetic isolation</span></div><div><strong>Rectifier modules</strong><span>AC → DC<br>Controlled DC supply</span></div></div>`+inputs('ABB specifies 400 V open-circuit in the text.');break;
 case 'loss-ledger':{
  const a=conversionPath(1000,[.98,.96]),b=conversionPath(1000,[s.conversionEfficiency??.975,.99]);
  markup=inputs('Same 1,000 kW DC output • stated efficiencies at the compared operating point')+`<div class="compare"><div><h2>AC distribution → rack conversion</h2>${flow(node('98%','Distribution'),node('96%','AC/DC'))}${strip(fact(`${n(a.inputKW)} kW`,'Source input'),fact(`${n(a.lossKW)} kW`,'Total included loss'))}</div><div><h2>Central conversion → DC distribution</h2>${flow(node(`${n((s.conversionEfficiency??.975)*100)}%`,'AC/DC'),node('99%','Distribution'))}${strip(fact(`${n(b.inputKW)} kW`,'Source input'),fact(`${n(b.lossKW)} kW`,'Total included loss'))}</div></div>`+note(b.inputKW<a.inputKW?'Central path uses 26.9 kW less input at these efficiencies.':'The changed converter efficiency reverses the ranking.');break;}
 case 'relocated-heat':markup=inputs('Same converter • 900 kW DC output • 96% efficiency • intervening distribution loss excluded')+`<div class="compare room-compare"><div><h2>Electrical room</h2>${s.moved?node('AC/DC converter','37.5 kW local heat','warm'):node('AC distribution','No converter here')}</div><div><h2>Rack</h2>${s.moved?node('DC load','900 kW input'):node('AC/DC + DC load','37.5 kW converter heat + 900 kW load','warm')}</div></div>`+strip(fact('937.5 kW','Same source input'),fact('37.5 kW','Same converter loss'))+note('The heat-rejection location changes; the loss does not.');break;
 case 'phase-opening':{const d=phaseLedger();markup=inputs('Supplied usable real-power limits • normal phase demand')+`<div class="split">${ledgerCard(d,'Phase demand')}${capacity(d)}</div>`+note('The two 0.2 MW margins belong to different boundaries.');break;}
 case 'hot-weather':{const d=phaseLedger({auxiliaryMW:s.weather==='hot'?1.4:1});markup=inputs('Fixed: IT output 4.6 MW • supplied electrical losses 0.2 MW')+`<div class="split">${ledgerCard(d,'Phase demand')}${capacity(d)}</div>`+note(s.weather==='hot'?'The service exceeds its limit while the IT branch still fits.':'Auxiliaries share the service margin with the IT path.');break;}
 case 'expansion-decision':{
  const d=phaseLedger({itMW:5.1,auxiliaryMW:1.1,lossMW:.22,serviceMW:['service','both'].includes(s.decision)?10:6,branchMW:['branch','both'].includes(s.decision)?5.5:4.8});
  markup=inputs('Existing phase: 4.6 MW IT + 1.0 MW auxiliaries + 0.2 MW losses')+strip(fact('+0.50 MW','New IT'),fact('+0.10 MW','New auxiliaries'),fact('+0.02 MW','Added losses'));
  markup+=s.reveal?capacity(d)+note(d.limits.length?`Hold the extension: ${d.limits.join(' and ')} still exceeds its limit.`:'Both capacity screens pass: 6.42 MW facility input and 5.10 MW IT output.'): `<div class="prediction">Choose the change that supplies the extension.<br>Trace both boundaries before revealing.</div>`;break;}
 case 'distribution-handoff':markup=flow(node('Defined source','Voltage + service limit'),node('Complete path','Connected equipment + ratings'),node('Supported loads','IT + cooling + controls'))+`<div class="opening-question">What changes when one part of this path is unavailable?</div>`;break;
 default:throw new RangeError(`Unknown distribution scene: ${id}`);
 }
 return {markup,description:scenes.find(scene=>scene.id===id).explanation};
}
