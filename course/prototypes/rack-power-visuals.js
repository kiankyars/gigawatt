import { renderSpatial } from './orientation-spatial.js';
import { localPower, supplyHandoff, bbuShelf, burstRecharge, phaseWaveforms } from './rack-power-model.js';
const C = { ink:'var(--text)', muted:'var(--muted)', line:'var(--line)', panel:'var(--panel)', face:'var(--surface)', power:'var(--power)', heat:'var(--heat)', data:'var(--data)', paper:'var(--paper)' };
const esc = v => String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const t = (x,y,s,size=24,color=C.ink,anchor='middle') => `<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${esc(s)}</text>`;
const r = (x,y,w,h,fill=C.panel,stroke=C.line) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="${fill}" stroke="${stroke}"/>`;
const l = (x,y,xx,yy,c=C.power,w=3) => `<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${c}" stroke-width="${w}"/>`;
const arrow = (x,y,xx,yy,c=C.power) => l(x,y,xx,yy,c)+`<path d="M${xx-8} ${yy-5}L${xx} ${yy}L${xx-8} ${yy+5}" transform="rotate(${Math.atan2(yy-y,xx-x)*180/Math.PI} ${xx} ${yy})" fill="none" stroke="${c}" stroke-width="3"/>`;
const box = (x,y,w,h,labels,m=false,color=C.power) => {
 const size=m?20:25, rows=[];
 labels.forEach((label,i)=>{let row='';const limit=Math.floor((w-24)/(size*.55));
  for(const word of label.split(' ')){if(row && row.length+word.length+1>limit){rows.push({text:row,color:i?C.ink:color});row=word;}else row+=(row?' ':'')+word;}
  rows.push({text:row,color:i?C.ink:color});
 });
 const step=Math.min(size+7,(h-20)/rows.length);
 return r(x,y,w,h,C.face,color)+rows.map((row,i)=>t(x+w/2,y+h/2+(i-(rows.length-1)/2)*step+7,row.text,Math.min(size,step/1.15,(w-20)/(row.text.length*.55)),row.color)).join('');
};
const note = (text,m,y=m?645:526) => {
 if(!m || text.length<46) return t(m?195:600,y,text,m?15:19,C.muted);
 const words=text.split(' '), rows=[''];
 for(const word of words){if(rows.at(-1).length+word.length>44)rows.push(word);else rows[rows.length-1]+=(rows.at(-1)?' ':'')+word;}
 return rows.map((row,i)=>t(195,y+i*21,row,15,C.muted)).join('');
};
const result = (value,label,m,y=m?490:420,color=C.power) => t(m?195:600,y,value,m?36:54,color)+t(m?195:600,y+39,label,m?18:24);
const format = v => Number(v.toFixed(3)).toLocaleString('en-US');

function rackPath(s,m) {
 let o='';
 if(m){
  o+=r(20,20,350,400)+t(46,51,'RACK',16,C.muted,'start');
  o+=box(43,85,246,89,['Power shelf','PSUs: AC → DC'],true);
  o+=l(325,127,325,351,C.power,8)+arrow(289,127,322,127);
  o+=box(43,223,246,86,['Compute tray'],true)+arrow(322,266,292,266);
  o+=t(195,377,'Rear busbar · 50–51 V DC',21,C.power);
  o+=arrow(166,310,166,458)+box(34,465,320,128,['Inside the compute tray','Conversion → local VRM → die'],true);
 }else{
  o+=r(40,30,572,441)+t(69,68,'RACK',20,C.muted,'start');
  o+=box(91,108,388,105,['Power shelf','PSUs: AC → DC'],false);
  o+=l(557,160,557,393,C.power,10)+arrow(481,160,553,160);
  o+=box(91,274,388,107,['Compute tray'],false)+arrow(553,327,483,327);
  o+=t(325,431,'Rear busbar · 50–51 V DC',26,C.power);
  o+=arrow(612,327,682,327)+r(697,86,466,385,C.face)+t(929,129,'INSIDE THE COMPUTE TRAY',20,C.muted);
  o+=box(735,173,390,82,['Board conversion'],false)+arrow(930,258,930,288)+box(735,294,390,80,['Point-of-load VRM'],false)+arrow(930,377,930,404)+t(930,440,'Compute die',28,C.power);
 }
 o+=note('Rack voltage: NVIDIA DGX guide · board stages vary',m);
 return o;
}
function psuInput(s,m) {
 let o='';
 if(m){
  o+=t(195,45,'480 V between live phases',23,C.power);
  const xs=[55,155,255], colors=[C.power,C.data,C.heat];
  xs.forEach((x,i)=>{o+=t(x,91,`L${i+1}`,19,colors[i])+l(x,107,x,178,colors[i])+box(x-30,184,76,87,['PSU','277 V'],true,colors[i]);});
  o+=l(338,105,338,164,C.muted)+t(338,89,'N',19,C.muted)+l(78,164,338,164,C.muted);
  xs.forEach(x=>{o+=l(x+23,164,x+23,181,C.muted)+l(x+8,276,x+8,329);});
  o+=l(63,329,263,329)+arrow(163,329,163,382);
  o+=box(25,387,340,94,['Shared rack bus','50 V DC'],true);
  o+=t(195,538,'480 / √3 ≈ 277 V',29,C.power);
  o+=t(195,577,'Phase to neutral at each PSU',18);
  o+=note('Advanced Energy ORv3 example · not wiring guidance',m);
 }else{
  o+=box(30,145,257,160,['Three-phase shelf input','480 V line-to-line'],false);
  o+=box(935,145,235,230,['Shared rack bus','50 V DC'],false);
  const colors=[C.power,C.data,C.heat];
  [0,1,2].forEach(i=>{const yy=75+i*138;o+=t(410,yy+51,`L${i+1}`,23,colors[i])+arrow(434,yy+44,514,yy+44,colors[i])+box(520,yy,275,92,['Single-phase PSU','277 V phase-to-neutral'],false,colors[i])+arrow(799,yy+46,931,yy+46);});
  o+=t(290,471,'480 / √3 ≈ 277 V',30,C.power)+note('Advanced Energy ORv3 example · neutral and protective earth have different roles',m);
 }
 return o;
}
function boardRails(s,m) {
 let o='';
 const a=[['Rack bus','48 V DC'],['Intermediate converter','12 V DC bus'],['Point-of-load VRM','1 V core rail'],['Compute die','Uses the core rail']];
 a.forEach((labels,i)=>{const x=m?48:28+i*298,y=m?30+i*141:178,w=m?294:250,h=m?97:138;
  o+=box(x,y,w,h,labels,m);if(i<3)o+=m?arrow(195,y+h+6,195,y+134):arrow(x+w+4,y+69,x+292,y+69);
 });
 o+=note('Illustrative chain · exact rails depend on the board',m);
 if(!m)o+=t(447,372,'Other loads branch to their own rails',24,C.muted);
 return o;
}
function localCurrent(s,m) {
 const a=localPower({loopMicroOhms:s.resistance});let o='';
 if(m){o+=box(20,40,150,130,['50 V bus','20 A'],true)+arrow(176,105,215,105)+box(221,40,150,130,['1 V core','1,000 A'],true);
  o+=t(195,218,'Same 1 kW · ideal conversion',21);
  o+=box(30,263,330,120,[`${s.resistance} µΩ core-path loop`,`${format(a.dropVolts)} V drop`],true,C.heat);
 }else{o+=box(50,83,325,152,['50 V rack bus','20 A'],false)+arrow(391,159,771,159)+t(585,132,'Same 1 kW · ideal conversion',24)+box(787,83,355,152,['1 V core rail','1,000 A'],false);
  o+=t(600,292,`${s.resistance} µΩ core-path loop → ${format(a.dropVolts)} V drop`,30,C.heat);
 }
 o+=result(`${format(a.lossWatts)} W`,'I²R in the final current path',m,m?467:405,C.heat);
 o+=note('Resistance values are assumptions, not a board design',m);
 return o;
}
function multiphase(s,m) {
 const q=phaseWaveforms(s.phases),x=m?33:90,w=m?324:1020;let o='';
 const color=[C.power,C.data,C.heat,C.muted];
 o+=t(m?195:600,m?44:43,`${s.phases} switching ${s.phases===1?'phase':'phases'} · 1,000 A total average`,m?20:28);
 q.curves.forEach((curve,i)=>{const yy=(m?95:78)+i*(m?61:58),average=1000/s.phases;
  const pts=curve.map((v,j)=>`${x+j/(curve.length-1)*w},${yy-(v-average)/(400/s.phases)*35}`);
  o+=l(x,yy,x+w,yy,C.line,1)+`<polyline data-phase="${i}" points="${pts.join(' ')}" fill="none" stroke="${color[i]}" stroke-width="2.6"/>`;
 });
 const sy=m?431:370,pts=q.sum.map((v,j)=>`${x+j/(q.sum.length-1)*w},${sy-(v-1000)/400*90}`);
 o+=t(x,sy-67,'SUM AT THE LOAD',m?15:19,C.muted,'start')+l(x,sy,x+w,sy,C.line,1)+`<polyline data-phase-sum="${s.phases}" points="${pts.join(' ')}" fill="none" stroke="${C.power}" stroke-width="4"/>`;
 o+=t(m?195:600,m?526:458,`${format(q.peakToPeakAmps)} A peak-to-peak ripple`,m?25:31,C.power);
 o+=note('Normalized currents · 30% duty ratio · residual ripple remains',m);
 return o;
}
function locality(s,m) {
 const colors=[s.location==='facility'?C.power:C.line,s.location==='rack'?C.power:C.line,s.location==='board'?C.power:C.line];let o='';
 if(m){
  o+=r(15,15,360,590,C.panel,colors[0])+t(195,51,'FACILITY',18,C.muted);
  o+=box(37,77,315,75,['UPS battery / BESS'],true,colors[0]);
  o+=r(39,191,310,381,C.face,colors[1])+t(195,225,'RACK',18,C.muted)+box(63,249,264,76,['BBU → rack DC bus'],true,colors[1]);
  o+=r(69,363,250,170,C.panel,colors[2])+t(195,395,'BOARD / PACKAGE',16,C.muted);
  o+=box(87,419,213,76,['Capacitors ↔ chip'],true,colors[2]);
 }else{
  o+=r(22,44,1156,423,C.panel,colors[0])+t(56,83,'FACILITY',19,C.muted,'start')+box(53,175,283,112,['UPS battery / BESS','Broader load boundary'],false,colors[0]);
  o+=r(384,106,758,327,C.face,colors[1])+t(410,141,'RACK',18,C.muted,'start')+box(410,218,280,107,['Rack BBU','Qualified DC bus'],false,colors[1]);
  o+=r(748,164,355,229,C.panel,colors[2])+t(925,204,'BOARD / PACKAGE',18,C.muted)+box(772,245,309,95,['Capacitors ↔ chip'],false,colors[2]);
 }
 const footer={board:'Short local loop · fast current support',rack:'Rack bus support · facility cooling is outside',facility:'Shared upstream support · converters and paths intervene'}[s.location];
 o+=note(footer,m);
 return o;
}
function handoff(s,m){
 const a=supplyHandoff({responseSeconds:s.response}),x=m?45:115,y=m?365:344,w=m?302:985,h=m?212:217;let o='';
 o+=t(m?195:600,m?45:44,'Additional load: 40 kW',m?24:32);
 o+=l(x,y,x+w,y,C.muted,2)+l(x,y,x,y-h-26,C.muted,2);
 o+=`<path d="M${x} ${y-h}H${x+w}L${x} ${y}Z" fill="${C.data}" opacity=".18"/>`;
 o+=l(x,y-h,x+w,y-h,C.heat,4)+l(x,y,x+w,y-h,C.power,4);
 o+=t(x+8,y-h-14,'Load',m?17:23,C.heat,'start')+t(x+w*.62,y-h*.47,'Source ramps',m?17:24,C.power);
 o+=t(x+w*.29,y-h*.68,'Buffer',m?18:27,C.data)+t(x,y+30,'0',m?16:20,C.muted)+t(x+w,y+30,`${s.response} s`,m?16:20,C.muted);
 o+=result(`${a.energyKJ} kJ`,'½ × 40 kW × response time',m,m?485:443);
 o+=note('Area between load and source · initial buffer power 40 kW',m);
 return o;
}
function bbu(s,m){
 const a=bbuShelf({failedModules:s.failed});let o='';
 o+=t(m?195:600,m?47:45,'ORv3 example · six BBU modules',m?23:31);
 const w=m?99:162,h=m?128:190;
 for(let i=0;i<6;i++){const x=m?27+(i%3)*120:46+i*190,y=m?92+Math.floor(i/3)*155:105,failed=i>=6-s.failed;
  o+=box(x,y,w,h,[`BBU ${i+1}`,failed?'Unavailable':'3 kW'],m,failed?C.heat:C.power);
  if(failed)o+=l(x+11,y+12,x+w-11,y+h-12,C.heat,2);
 }
 o+=result(`${a.availableKW} kW available`,a.capacityPass?'15 kW load fits':'15 kW load exceeds surviving capacity',m,m?498:393,a.capacityPass?C.power:C.heat);
 o+=note('Module duration ≥240 s · stated conditions',m,m?590:499);
 o+=note('ORv3 example · not sized for NVL72',m,m?631:531);
 return o;
}
function recharge(s,m){
 const a=burstRecharge({restSeconds:s.rest}),x=m?25:80,w=m?340:1040;let o='';
 const vals=[['Burst',`40 kW × 0.2 s`,`${a.energyKJ} kJ used`],['Recharge',`10 kW × ${s.rest} s`,`${format(a.rechargeKJ)} kJ restored`]];
 vals.forEach((v,i)=>{const yy=m?70+i*192:94,xx=m?25:80+i*550,ww=m?340:490;o+=box(xx,yy,ww,m?137:200,v,m,i?C.power:C.heat);});
 o+=result(a.missingKJ?`${a.missingKJ} kJ lost / cycle`:'Buffer refilled',a.missingKJ?'Average 135 kW > 120 kW source':'Ideal refill needs at least 0.8 seconds',m,m?510:405,a.missingKJ?C.heat:C.power);
 o+=note('120 kW source · 110 kW between bursts · 160 kW during burst',m);
 return o;
}
function transfer(s,m){
 let o=box(m?29:175,m?78:94,m?332:850,m?153:183,['160 kW for 0.2 s','110 kW for 0.2 s','120 kW source cap'],m);
 if(!s.reveal)o+=result('Larger battery?','Predict: longer runtime or indefinite support?',m,m?426:382);
 else{o+=result('135 kW average load','Storage depletes: 15 kW average shortfall',m,m?411:371,C.heat);o+=note('Reduce / shift demand, add supply, or accept finite runtime',m,m?558:499);}
 return o;
}
export function renderRackPower(id,state,compact=false){
 const renderers={'rack-power-path':rackPath,'psu-input':psuInput,'board-rails':boardRails,'local-current':localCurrent,multiphase,'energy-locality':locality,'source-handoff':handoff,'bbu-shelf':bbu,'buffer-recharge':recharge,'rack-transfer':transfer};
 const markup=id==='rear-busbar'?`<g transform="${compact?'translate(11 0) scale(.944)':'translate(55 0) scale(.92)'}">${renderSpatial('rack-boundary',{rackView:'rear'},compact)}</g>`:renderers[id]?.(state,compact);
 if(!markup)throw new Error(`Unknown rack power scene: ${id}`);
 const descriptions={
  'rack-power-path':'PSUs in a rack power shelf convert AC into nominal 50–51 V DC. The vertical rack busbar carries power to trays; board conversion and point-of-load regulation then supply devices.',
  'rear-busbar':'NVIDIA DGX GB300 rear hardware illustration identifies the power busbar behind the trays. It carries nominal 50–51 V DC inside the rack.',
  'psu-input':'The source example uses a 480/277 V wye supply. Each selected single-phase PSU receives phase-to-neutral voltage around 277 V; shared outputs supply a 50 V rack bus. Neutral and protective earth are distinct.',
  'board-rails':'An illustrative 48 V bus feeds a 12 V intermediate converter, then a 1 V point-of-load regulator and compute die. The exact rails and branches vary by board.',
  'local-current':`A 1 kW core receives 1000 A at 1 V. With ${state.resistance} microohms in the final loop, resistive heat is ${format(localPower({loopMicroOhms:state.resistance}).lossWatts)} W.`,
  multiphase:`${state.phases} interleaved converter phases supply a constant 1000 A average. The summed current has ${format(phaseWaveforms(state.phases).peakToPeakAmps)} A peak-to-peak normalized ripple.`,
  'energy-locality':`Selected ${state.location} energy storage. Board capacitors, rack BBU and facility storage connect at different electrical boundaries; path impedance and conversion response matter.`,
  'source-handoff':`The load steps by 40 kW while source power ramps over ${state.response} seconds. The buffer's triangular power deficit requires ${supplyHandoff({responseSeconds:state.response}).energyKJ} kJ.`,
  'bbu-shelf':`${state.failed} BBU modules unavailable: ${bbuShelf({failedModules:state.failed}).availableKW} kW of module capacity remains for a 15 kW load. Runtime and transition conditions must also hold.`,
  'buffer-recharge':`A burst uses 8 kJ. A ${state.rest} second gap replenishes ${burstRecharge({restSeconds:state.rest}).rechargeKJ} kJ with the available 10 kW headroom.`,
  'rack-transfer':state.reveal?'A larger battery delays depletion, but average load 135 kW exceeds source capacity 120 kW. Change the sustained balance.':'Would a larger battery support the supplied repeated burst pattern indefinitely? Predict before revealing.'
 };
 return {markup,description:descriptions[id]};
}
