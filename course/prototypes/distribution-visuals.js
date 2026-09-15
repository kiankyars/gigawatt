import { equipment } from './distribution-equipment.js';
import { rowBudget, transformerVoltage } from './distribution-model.js';
import { campusRoute, oneLine, switchgearAnatomy } from './distribution-context.js';
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

function transformerTaps(state, compact) {
 const {inputVolts,primaryTurns,secondaryTurns,tapVolts,outputVolts}=transformerVoltage(state.transformerCase);
 const cx=compact?195:560, px=compact?144:465, sx=compact?246:655;
 const top=compact?207:115, step=compact?22:25;
 const coil=(x,direction,color)=>wire(`M${x} ${top}${Array.from({length:4},()=>`c${direction*27} 0 ${direction*27} ${step} 0 ${step}`).join('')}`,color);
 let o='';
 if(compact){
  o+=text(100,40,'AC input',22,power)+text(290,40,'AC output',22,'var(--data)');
  o+=text(100,84,`${inputVolts} V`,32,power)+text(290,84,`${outputVolts} V`,32,'var(--data)');
  o+=rect(72,148,246,235)+text(cx,183,'Transformer',23);
  o+=wire(`M100 100V${top}H${px}`,power)+wire(`M${sx} ${top}H290V104`,'var(--data)');
  o+=wire(`M${px} ${top+4*step}H105V317`,power)+wire(`M${sx} ${top+4*step}H285V317`,'var(--data)');
  o+=wire('M190 201V302M200 201V302',muted);
  o+=text(119,343,`${primaryTurns} turns`,21,power)+text(272,343,'20 turns',21,'var(--data)');
 }else{
  o+=text(180,145,'AC input',26,power)+text(940,145,'AC output',26,'var(--data)');
  o+=text(180,197,`${inputVolts} V`,40,power)+text(940,197,`${outputVolts} V`,40,'var(--data)');
  o+=rect(360,35,400,240)+text(cx,75,'Transformer',28);
  o+=wire(`M275 183H405V${top}H${px}`,power)+wire(`M${sx} ${top}H715V183H845`,'var(--data)');
  o+=wire(`M${px} ${top+4*step}H410V237`,power)+wire(`M${sx} ${top+4*step}H710V237`,'var(--data)');
  o+=wire('M555 105V218M565 105V218',muted);
  o+=text(460,256,`${primaryTurns} turns`,23,power)+text(660,256,'20 turns',23,'var(--data)');
 }
 o+=coil(px,1,power)+coil(sx,-1,'var(--data)');
 o+=text(cx,compact?441:332,`${inputVolts} V × ${secondaryTurns} / ${primaryTurns} = ${outputVolts} V`,compact?25:32);
 o+=text(cx,compact?502:391,state.transformerCase==='matched-tap'?'More primary turns restore 120 V.':'Same turns: output follows input.',compact?19:24,muted);
 return svg(`<g data-input-volts="${inputVolts}" data-primary-turns="${primaryTurns}" data-secondary-turns="${secondaryTurns}" data-tap-volts="${tapVolts}" data-output-volts="${outputVolts}">${o}</g>`,'A transformer tap changes connected primary turns. With 20 secondary turns, 80 primary turns give 120 volts from 480 volts and 126 volts from 504 volts. Connecting 84 primary turns gives 120 volts from 504 volts.',compact?390:1120,compact?550:420);
}

function coDesign(compact) {
 const w=compact?390:1120;
 let o='';
 if(compact){
  o+=box(8,10,168,92,'Compass','Site requirements')+box(214,10,168,92,'Siemens','Equipment design');
  o+=wire('M176 56H214',muted)+wire('M92 102V133H296V102',muted)+wire('M195 133V174',muted);
  o+=rect(20,174,350,297,'var(--panel)',power)+text(195,213,'One factory-built skid',25,power);
  o+=box(64,239,262,81,'MV switchgear','Switch + protect')+wire('M195 320V348');
  o+=box(64,348,262,81,'Transformer','Change voltage');
 }else{
  o+=box(190,5,260,85,'Compass','Site requirements')+box(670,5,260,85,'Siemens','Equipment design');
  o+=wire('M450 47H670',muted)+text(560,28,'Co-design',20,muted)+wire('M560 47V129',muted);
  o+=rect(175,129,770,233,'var(--panel)',power)+text(560,169,'One factory-built skid',28,power);
  o+=box(235,207,285,95,'MV switchgear','Switch + protect')+wire('M520 254H600')+arrow(587,254)+box(600,207,285,95,'Transformer','Change voltage');
 }
 return svg(o,'Compass site requirements and Siemens equipment design meet in one factory-built skid. Switchgear switches and protects; the transformer changes voltage.',w,compact?485:380);
}

export function renderDistribution(id,state={},compact=false){
 const m=compact,s=state;
 const art=(file,alt)=>`<figure class="teaching-art"><img src="../assets/generated/${file}.png" alt="${esc(alt)}"></figure>`;
 let markup='';
 switch(id){
 case 'distribution-purpose':markup=art('distribution-campus-to-rack','Campus connection → building transformer → overhead row busway → rack load.');break;
 case 'campus-route':markup=campusRoute(s,m);break;
 case 'campus-switchgear-focus':markup=campusRoute(s,m,'switchgear');break;
 case 'campus-three-phase-focus':markup=campusRoute(s,m,'three-phase');break;
 case 'one-line':markup=oneLine(m);break;
 case 'switchgear-anatomy':markup=switchgearAnatomy(m);break;
 case 'protection-relay':case 'isolation-surge':case 'surge-protection':case 'phase-loading':case 'feeder-diagnosis':markup=equipment(id,s,m);break;
 case 'compass-co-design':markup=coDesign(m);break;
 case 'compass-skid':markup=`<div class="split">${photo('distribution-compass-switchgear.jpg','Original factory view of Siemens switchgear for the jointly developed Compass MV skid.','Siemens × Compass · factory switchgear',compassURL)}<div class="package-comparison"><div><h2>Custom factory-built skid</h2><p>MV switchgear + transformer</p></div><div><h2>Co-developed with Compass</h2><p>Manufactured by Siemens</p></div></div></div>`;break;
 case 'local-stepdown':markup=art('distribution-transformer-location','Two balanced 2 MW, PF 1 routes: early step-down carries 2,406 A over 470 m; step-down beside the hall carries 33.5 A at 34.5 kV over 450 m and 2,406 A at 480 V over the final 20 m. Losses neglected.');break;
 case 'transformer-taps':markup=transformerTaps(s,m);break;
 case 'transformer-taps-photo':markup=`<figure class="teaching-art transformer-tap-photo"><img src="../assets/references/distribution-transformer-taps-photo.png" alt="Three transformer windings with multiple bolted tap terminals. The supplied red circle and arrow mark one attached winding lead."></figure>`;break;
 case 'building-branches':markup=building(m);break;
 case 'distribution-units':markup=art('distribution-pdu-psu','Floor PDU distributes to feeders; rack PDU distributes AC to outlets; server PSU converts AC to DC.');break;
 case 'busway-introduction':markup=art('distribution-busway','An enclosed overhead busway has one end feed and a shared conductor housing above three racks. Tap-off boxes connect individual rack cables to the busway.');break;
 case 'busway-branches':markup=`<div class="split">${photo('distribution-fujitsu-tapoffs.jpg','A busway tap-off enclosure with branch connectors in the Fujitsu case.','Starline / Legrand · tap-off',fujitsuURL)}<div class="stack">${flow(node('End feed','Power enters busway'),node('Tap-off box','Connects a protected branch'),node('Cable to rack','Rack PDU or power shelf'))}</div></div>`;break;
 case 'fujitsu-busway':markup=`<div class="split">${photo('distribution-fujitsu-outlets.jpg','Overhead busway branch outlets in the Fujitsu case study.','Starline / Legrand · Fujitsu · 2018',fujitsuURL)}<div class="case-points"><strong>250 A Track Busway</strong><p>New branches near changing rack loads</p><p>Metering at each tap-off</p><p>Underfloor cooling path stays clear</p></div></div>`;break;
 case 'row-growth':markup=row(s,m);break;
 case 'apparent-power-beer':markup=`<figure class="pf-beer-image"><img src="../assets/references/distribution-apparent-power-beer.png" alt="How is apparent power like a pint of beer? The beer is labeled active power in kW, its foam reactive power in kvar, and a bracket around both apparent power in kVA."></figure>`;break;
 case 'power-factor-explained':markup=`<figure class="teaching-art"><img src="../assets/references/distribution-power-factor-comparison.png" alt="At 900 kW real power and 480 V balanced three-phase, PF 1 needs 900 kVA and 1,083 A, loading a 1,000 kVA transformer to 90 percent. PF 0.8 needs 1,125 kVA and 1,353 A, loading the same transformer to 112.5 percent."></figure>`;break;
 case 'power-factor':{const pf=s.powerFactor??1,p=900,kva=p/pf,amps=kva*1000/(Math.sqrt(3)*480);markup=`<div class="pf-rating"><strong>1,000 kVA</strong><span>Transformer rating</span></div><div class="equation">S = P / PF</div>`+strip(fact('900 kW','Real input'),fact(`${n(kva,0)} kVA`,'Transformer loading',kva>1000?'warm':''),fact(`${n(amps,0)} A`,'Current at 480 V'))+`<div class="rating-track"><span style="width:${Math.min(kva/1200*100,100)}%"></span><i style="left:83.333%"></i></div>`;break;}
 case 'distribution-handoff':markup=art('distribution-interruption','An open common feeder interrupts the path to a switchboard and both its compute-rack and cooling/control branches.');break;
 default:throw new RangeError(`Unknown distribution scene: ${id}`);
 }
 return {markup,description:scenes.find(scene=>scene.id===id).explanation};
}
