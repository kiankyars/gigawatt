import { equipment } from './distribution-equipment.js';
import { rowBudget, traceLoad } from './distribution-model.js';
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
  let o=text(w/2,28,'480Y/277 V: Y means wye',23);
  if(m){
    o+=box(80,57,230,60,'Single-line view');o+=wire('M195 117V175');o+=box(80,175,230,55,'Rack branch');
    o+=text(195,272,'Expanded conductors',23);
    ['L1','L2','L3','N','PE'].forEach((v,i)=>{let x=55+i*68; o+=text(x,318,v,18)+wire(`M${x} 340V515`,i<3?power:muted,i===4);});
    o+=text(195,558,['480 V: phase to phase','277 V: phase to neutral','N = neutral','PE = protective earth'],20);
  } else {
    o+=box(35,78,230,70,'Single-line view');o+=wire('M150 148V320')+box(35,320,230,60,'Rack branch');
    o+=text(682,88,'The same circuit has several conductors',23);
    ['L1','L2','L3','N','PE'].forEach((v,i)=>{let x=440+i*130;o+=text(x,132,v,19)+wire(`M${x} 150V300`,i<3?power:muted,i===4);});
    o+=text(685,346,'480 V: phase to phase     277 V: phase to neutral',22)+text(685,382,'N = neutral     PE = protective earth',18,muted);
  }
  return svg(o,'A single-line diagram expands to three phases, neutral and protective earth in the specified 480Y/277 volt system.',w,m?640:420);
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

function building(m){
 const w=m?390:1120;
 const labels=[['IT feeder','Continuity block','Row busway','Rack PSUs'],['Cooling feeder','Drive and motor','Pump','Moves coolant'],['House feeder','Panelboard','Building services','Lights + controls']];
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

export function renderDistribution(id,state={},compact=false){
 const m=compact,s=state;
 const art=(file,alt)=>`<figure class="teaching-art"><img src="../assets/generated/${file}.png" alt="${esc(alt)}"></figure>`;
 let markup='';
 switch(id){
 case 'distribution-purpose':markup=art('distribution-campus-to-rack','Campus connection → building transformer → overhead row busway → rack load.');break;
 case 'abilene-distribution':markup=photo('distribution-abilene-data-halls.jpg','Oracle aerial of Abilene data halls.','Oracle · Abilene · 15 July 2026','https://www.oracle.com/data-centers/');break;
 case 'campus-route':markup=campus(s,m);break;
 case 'one-line':markup=oneLine(m);break;
 case 'switchgear-anatomy':case 'protection-relay':case 'isolation-surge':case 'phase-loading':case 'feeder-diagnosis':markup=equipment(id,s,m);break;
 case 'compass-skid':markup=`<div class="split">${photo('distribution-compass-switchgear.jpg','Factory view of the Siemens switchgear used in the Compass integrated medium-voltage skid case.','Siemens · Compass project',compassURL)}<div class="package-comparison"><div><h2>Separate equipment</h2><p>Switchgear + transformer</p><span>Site connections between assemblies</span></div><div><h2>Integrated skid</h2><p>Same two functions</p><span>Packaged for transport and site installation</span></div></div></div>`;break;
 case 'local-stepdown':markup=art('distribution-transformer-location','Two balanced 2 MW, PF 1 routes: early step-down carries 2,406 A over 470 m; step-down beside the hall carries 84 A at 13.8 kV over 450 m and 2,406 A at 480 V over the final 20 m. Losses neglected.');break;
 case 'building-branches':markup=building(m);break;
 case 'distribution-units':markup=art('distribution-pdu-psu','Illustrative equipment: a transformer-equipped floor PDU changes 480 V AC to 208 V AC and distributes branches; a rack PDU distributes 208 V AC to outlets; a server PSU converts 208 V AC to 12 V DC.');break;
 case 'busway-branches':markup=`<div class="split">${photo('distribution-fujitsu-tapoffs.jpg','A busway tap-off enclosure with branch connectors in the Fujitsu case.','Starline / Legrand · tap-off',fujitsuURL)}<div class="stack">${flow(node('End feed','Power enters busway'),node('Tap-off box','Connects a protected branch'),node('Cable to rack','Rack PDU or power shelf'))}</div></div>`;break;
 case 'fujitsu-busway':markup=`<div class="split">${photo('distribution-fujitsu-outlets.jpg','Overhead busway branch outlets in the Fujitsu case study.','Starline / Legrand · Fujitsu · 2018',fujitsuURL)}<div class="case-points"><strong>250 A Track Busway</strong><p>New branches near changing rack loads</p><p>Metering at each tap-off</p><p>Underfloor cooling path stays clear</p></div></div>`;break;
 case 'row-growth':markup=row(s,m);break;
 case 'power-factor':{const pf=s.powerFactor??1,p=900,kva=p/pf,amps=kva*1000/(Math.sqrt(3)*480);markup=inputs('900 kW real AC input · balanced 480 V line-to-line · illustrative 1,000 kVA transformer')+`<div class="equation">S = P / PF</div>`+strip(fact('900 kW','Real input'),fact(`${n(kva,0)} kVA`,'Transformer loading',kva>1000?'warm':''),fact(`${n(amps,0)} A`,'Line current'))+`<div class="rating-track"><span style="width:${Math.min(kva/1200*100,100)}%"></span><i style="left:83.333%"></i></div><p class="inputs">1,000 kVA rating · I = S / (√3 × V<sub>LL</sub>)</p>`;break;}
 case 'distribution-handoff':markup=art('distribution-interruption','An open common feeder interrupts the path to a switchboard and both its compute-rack and cooling/control branches.');break;
 default:throw new RangeError(`Unknown distribution scene: ${id}`);
 }
 return {markup,description:scenes.find(scene=>scene.id===id).explanation};
}
