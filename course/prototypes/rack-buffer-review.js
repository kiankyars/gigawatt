import { supplyHandoff } from './rack-power-model.js';

const C={ink:'var(--text)',muted:'var(--muted)',line:'var(--line)',panel:'var(--panel)',surface:'var(--surface)',power:'var(--power)',battery:'var(--data)',heat:'var(--heat)'};
const text=(x,y,value,size=24,color=C.ink,anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${value}</text>`;
const line=(x,y,xx,yy,color=C.power,width=3)=>`<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${color}" stroke-width="${width}"/>`;
const rect=(x,y,w,h,color=C.line,fill=C.surface)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" stroke="${color}" fill="${fill}"/>`;
const arrow=(x,y,xx,yy,color=C.power)=>line(x,y,xx,yy,color)+`<path d="M${xx-8} ${yy-5}L${xx} ${yy}L${xx-8} ${yy+5}" transform="rotate(${Math.atan2(yy-y,xx-x)*180/Math.PI} ${xx} ${yy})" fill="none" stroke="${color}" stroke-width="3"/>`;
const box=(x,y,w,h,title,detail='',color=C.power,compact=false)=>rect(x,y,w,h,color)+text(x+w/2,y+h/2+(detail?-5:8),title,compact?19:25,color)+(detail?text(x+w/2,y+h/2+25,detail,compact?15:19):'');
const svg=(content,compact,label)=>`<svg class="buffer-review-diagram" viewBox="${compact?'0 0 390 680':'0 0 1200 560'}" role="img" aria-label="${label}">${content}</svg>`;

function locality(compact){
 let out='';
 if(compact){
  out+=rect(13,16,364,619,C.power,C.panel)+text(195,55,'FACILITY',18,C.muted);
  out+=box(38,82,314,84,'UPS batteries / BESS','Upstream power system',C.power,true);
  out+=rect(39,208,312,392,C.battery)+text(195,248,'RACK',18,C.muted);
  out+=box(62,277,266,84,'Rack BBU','Rack DC bus',C.battery,true);
  out+=rect(66,401,258,165,C.heat,C.panel)+text(195,434,'BOARD / PACKAGE',16,C.muted);
  out+=box(84,457,222,81,'Capacitors','Beside the chips',C.heat,true);
 }else{
  out+=rect(22,45,1156,437,C.power,C.panel)+text(58,88,'FACILITY',20,C.muted,'start');
  out+=box(52,203,284,123,'UPS batteries / BESS','Upstream power system');
  out+=rect(380,120,765,323,C.battery)+text(410,163,'RACK',20,C.muted,'start');
  out+=box(408,245,286,123,'Rack BBU','Rack DC bus',C.battery);
  out+=rect(747,193,357,210,C.heat,C.panel)+text(925,236,'BOARD / PACKAGE',19,C.muted);
  out+=box(774,266,305,103,'Capacitors','Beside the chips',C.heat);
 }
 return svg(out,compact,'Facility UPS batteries or BESS connect upstream. A rack BBU connects to the rack DC bus. Capacitors sit close to the chips.');
}

function handoff(state,compact){
 const response=state.response===0.4?0.4:0.2;
 const {energyKJ}=supplyHandoff({responseSeconds:response});
 let out='';
 if(compact){
  out+=box(12,21,104,76,'PSUs','AC → DC',C.power,true)+arrow(118,59,140,59);
  out+=box(145,21,100,76,'Rack','DC bus',C.ink,true);
  out+=arrow(272,59,251,59,C.battery)+box(278,21,100,76,'BBU','Battery',C.battery,true);
 }else{
  out+=box(225,19,220,74,'PSUs','AC → DC')+arrow(451,56,491,56);
  out+=box(497,19,210,74,'Rack DC bus','',C.ink);
  out+=arrow(755,56,715,56,C.battery)+box(761,19,220,74,'BBU','Rack battery',C.battery);
 }
 const x=compact?48:115,y=compact?408:367,w=compact?297:970,h=compact?222:209;
 out+=line(x,y,x+w,y,C.muted,2)+line(x,y,x,y-h-14,C.muted,2);
 out+=`<path d="M${x} ${y-h}H${x+w}L${x} ${y}Z" fill="${C.battery}" opacity=".17"/>`;
 out+=`<path d="M${x} ${y}H${x+w}V${y-h}Z" fill="${C.power}" opacity=".09"/>`;
 out+=line(x,y-h,x+w,y-h,C.heat,4)+line(x,y,x+w,y-h,C.power,4);
 out+=text(x,y-h-25,'Load rises by 40 kW',compact?21:29,C.heat,'start');
 out+=text(x+w*.23,y-h*.72,'BBU',compact?22:30,C.battery);
 out+=text(x+w*.72,y-h*.22,'PSUs',compact?22:30,C.power);
 out+=text(x-14,y+7,'0',compact?16:21,C.muted,'end');
 out+=text(x,y+32,'0 s',compact?17:22,C.muted)+text(x+w,y+32,`${response} s`,compact?17:22,C.muted);
 if(compact){
  out+=text(195,510,`${energyKJ} kJ from the BBU`,30,C.battery);
  out+=text(195,553,`½ × 40 kW × ${response} s`,24);
 }else{
  out+=text(600,468,`${energyKJ} kJ from the BBU`,42,C.battery);
  out+=text(600,510,`½ × 40 kW × ${response} s`,27);
 }
 return svg(out,compact,`A rack BBU supplies the difference as PSU power rises to meet an extra 40 kilowatts of load over ${response} seconds. The shaded triangular energy deficit is ${energyKJ} kilojoules.`);
}

function hierarchy(compact){
 let out='';
 if(compact){
  out+=box(15,12,168,87,'Generator','After startup',C.power,true);
  out+=box(207,12,168,87,'Site BESS','Battery + inverter',C.battery,true);
  out+=line(99,102,99,138)+line(291,102,291,138,C.battery)+line(99,138,291,138)+arrow(195,138,195,164);
  out+=box(92,169,206,72,'Facility AC bus','',C.power,true)+arrow(195,245,195,268);
  out+=box(92,274,206,72,'Rack PSUs','',C.power,true)+arrow(195,350,195,378);
  out+=box(17,388,112,80,'BBU','Rack battery',C.battery,true)+arrow(132,427,158,427,C.battery);
  out+=box(164,388,210,80,'Rack DC bus','',C.power,true)+arrow(270,472,270,503);
  out+=box(164,509,210,72,'VRM → chip','',C.power,true);
  out+=box(17,509,112,95,'Capacitors','Near the chip',C.heat,true)+arrow(132,546,158,546,C.heat);
  out+=text(195,654,'Connection determines the loads supported.',16,C.muted);
 }else{
  out+=box(22,73,199,100,'Generator','After startup');
  out+=box(255,73,223,100,'Site BESS','Battery + inverter',C.battery);
  out+=line(122,177,122,228)+line(367,177,367,228,C.battery)+line(122,228,367,228)+arrow(210,228,210,306);
  out+=box(87,313,245,100,'Facility AC bus');
  out+=arrow(336,364,390,364)+box(397,313,204,100,'Rack PSUs');
  out+=arrow(605,364,659,364)+box(666,313,219,100,'Rack DC bus');
  out+=box(666,73,219,100,'BBU','Rack battery',C.battery)+arrow(776,178,776,306,C.battery);
  out+=arrow(889,364,943,364)+box(950,313,228,100,'VRM → chip');
  out+=box(950,73,228,100,'Capacitors','Near the chip',C.heat)+arrow(1064,178,1064,306,C.heat);
  out+=text(600,490,'Connection determines the loads supported.',24,C.muted);
 }
 return svg(out,compact,'An example of support at different electrical boundaries. A generator after startup and a site BESS through its inverter supply a facility AC bus. Rack PSUs convert AC to DC. A rack BBU supports that DC bus. Capacitors support local device rails near the chip. These sources do not form a fixed sequence.');
}

export function renderBufferReview(id,state={},compact=false){
 if(id==='energy-locality')return locality(compact);
 if(id==='source-handoff')return handoff(state,compact);
 if(id==='rack-transfer')return hierarchy(compact);
 if(id==='buffer-recharge')return '<figure class="buffer-review-figure"><img src="../assets/references/rack-recharge-between-bursts.png" alt="Recharge between bursts. An eight-kilojoule burst uses 40 kilowatts for 0.2 seconds. With 10 kilowatts of surplus, a one-second quiet interval allows recovery; a half-second interval provides only five kilojoules, leaving the buffer short. Energy equals power times time."></figure>';
 return null;
}
