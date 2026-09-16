import { supplyHandoff } from './rack-power-model.js';

const C={ink:'var(--text)',muted:'var(--muted)',line:'var(--line)',panel:'var(--panel)',surface:'var(--surface)',power:'var(--power)',battery:'var(--data)',heat:'var(--heat)'};
const text=(x,y,value,size=24,color=C.ink,anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${value}</text>`;
const line=(x,y,xx,yy,color=C.power,width=3)=>`<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${color}" stroke-width="${width}"/>`;
const rect=(x,y,w,h,color=C.line,fill=C.surface)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" stroke="${color}" fill="${fill}"/>`;
const arrow=(x,y,xx,yy,color=C.power)=>line(x,y,xx,yy,color)+`<path d="M${xx-8} ${yy-5}L${xx} ${yy}L${xx-8} ${yy+5}" transform="rotate(${Math.atan2(yy-y,xx-x)*180/Math.PI} ${xx} ${yy})" fill="none" stroke="${color}" stroke-width="3"/>`;
const box=(x,y,w,h,title,detail='',color=C.power,compact=false)=>rect(x,y,w,h,color)+text(x+w/2,y+h/2+(detail?-5:8),title,compact?19:25,color)+(detail?text(x+w/2,y+h/2+25,detail,compact?15:19):'');
const svg=(content,compact,label)=>`<svg class="buffer-review-diagram" viewBox="${compact?'0 0 390 680':'0 0 1200 560'}" role="img" aria-label="${label}">${content}</svg>`;

const energyNode=(id,x,y,w,h,rows,color=C.power)=>`<g data-power-node="${id}">${rect(x,y,w,h,color)}${rows.map((row,i)=>text(x+w/2,y+h/2+(i-(rows.length-1)/2)*24+7,row,i?17:22,i?C.muted:color)).join('')}</g>`;
const connection=(from,to,content)=>`<g data-power-from="${from}" data-power-to="${to}">${content}</g>`;
const junction=(x,y,color=C.power)=>`<circle cx="${x}" cy="${y}" r="5" fill="${color}"/>`;

export function renderEnergyConnections(compact=false){
 let out='';
 if(compact){
  out+=`<g data-power-group="facility">${rect(5,5,380,1040,C.power,C.panel)}${text(25,36,'FACILITY',17,C.muted,'start')}</g>`;
  out+=`<g data-power-group="rack">${rect(26,518,340,499,C.battery)}${text(45,548,'RACK',17,C.muted,'start')}</g>`;
  out+=`<g data-power-group="chip">${rect(47,781,300,215,C.heat,C.panel)}${text(64,812,'CHIP / LOCAL SUPPLY',16,C.muted,'start')}</g>`;
  out+=energyNode('generator',25,62,158,74,['Generator','After connection']);
  out+=energyNode('bess',209,62,157,74,['Site BESS','Battery + inverter'],C.battery);
  out+=connection('generator','facility-ac',line(104,137,104,166)+line(104,166,282,166)+arrow(282,166,282,197));
  out+=connection('bess','facility-ac',arrow(287,137,287,197,C.battery));
  out+=text(70,235,'Grid',22)+connection('grid','facility-ac',arrow(104,227,203,227));
  out+=energyNode('facility-ac',209,201,153,65,['Facility AC bus']);
  out+=connection('facility-ac','ups-rectifier',arrow(282,270,282,297));
  out+=energyNode('ups-rectifier',214,302,139,65,['UPS rectifier','AC → DC']);
  out+=connection('ups-rectifier','ups-dc-link',line(282,369,282,409));
  out+=energyNode('ups-battery',32,374,160,75,['UPS batteries'],C.battery);
  out+=connection('ups-battery','ups-dc-link',arrow(196,410,277,410,C.battery))+junction(282,410);
  out+=text(237,393,'DC link',15,C.muted);
  out+=connection('ups-dc-link','ups-inverter',arrow(282,414,282,441));
  out+=energyNode('ups-inverter',214,446,139,63,['UPS inverter','DC → AC']);
  out+=connection('ups-inverter','rack-psu',arrow(282,513,282,580));
  out+=text(123,571,'Protected AC',17,C.muted);
  out+=energyNode('rack-psu',215,585,138,65,['Rack PSU','AC → DC']);
  out+=connection('rack-psu','rack-dc',line(283,654,283,719));
  out+=energyNode('rack-bbu',43,683,159,76,['Rack BBU','Battery + DC/DC'],C.battery);
  out+=connection('rack-bbu','rack-dc',arrow(206,721,278,721,C.battery))+junction(283,721);
  out+=text(190,671,'Rack DC bus',17,C.muted,'end');
  out+=connection('rack-dc','vrm',arrow(283,725,283,827));
  out+=energyNode('vrm',235,832,96,61,['VRM']);
  out+=connection('vrm','chip-rail',line(283,897,283,927));
  out+=energyNode('capacitors',65,884,143,69,['Capacitors','Near the chip'],C.heat);
  out+=connection('capacitors','chip-rail',arrow(212,928,278,928,C.heat))+junction(283,928,C.heat);
  out+=connection('chip-rail','chip',arrow(283,932,283,944));
  out+=text(341,917,'Core rail',15,C.muted,'end');
  out+=energyNode('chip',235,949,96,34,['Chip']);
 }else{
  out+=`<g data-power-group="facility">${rect(12,18,1256,536,C.power,C.panel)}${text(39,57,'FACILITY',21,C.muted,'start')}</g>`;
  out+=`<g data-power-group="rack">${rect(710,160,532,365,C.battery)}${text(733,196,'RACK',21,C.muted,'start')}</g>`;
  out+=`<g data-power-group="chip">${rect(982,265,238,235,C.heat,C.panel)}${text(1101,299,'CHIP / LOCAL SUPPLY',17,C.muted)}</g>`;
  out+=energyNode('generator',40,93,194,86,['Generator','After connection']);
  out+=energyNode('bess',260,93,210,86,['Site BESS','Battery + inverter'],C.battery);
  out+=connection('generator','facility-ac',line(137,184,137,253)+line(137,253,224,253)+arrow(224,253,224,387));
  out+=connection('bess','facility-ac',line(365,184,365,253,C.battery)+line(365,253,224,253,C.battery));
  out+=text(73,405,'Grid',22)+connection('grid','facility-ac',arrow(95,430,173,430));
  out+=energyNode('facility-ac',179,392,100,75,['AC bus']);
  out+=connection('facility-ac','ups-rectifier',arrow(283,430,316,430));
  out+=energyNode('ups-rectifier',322,392,125,75,['Rectifier','AC → DC']);
  out+=text(385,361,'UPS',23,C.muted);
  out+=connection('ups-rectifier','ups-dc-link',line(451,430,491,430));
  out+=energyNode('ups-battery',482,192,195,82,['UPS batteries'],C.battery);
  out+=connection('ups-battery','ups-dc-link',line(580,279,580,320,C.battery)+line(580,320,491,320,C.battery)+arrow(491,320,491,425,C.battery))+junction(491,430);
  out+=text(491,477,'DC link',17,C.muted);
  out+=connection('ups-dc-link','ups-inverter',arrow(496,430,526,430));
  out+=energyNode('ups-inverter',532,392,125,75,['Inverter','DC → AC']);
  out+=connection('ups-inverter','rack-psu',arrow(661,430,730,430));
  out+=text(694,373,'Protected',16,C.muted)+text(694,395,'AC',16,C.muted);
  out+=energyNode('rack-psu',736,392,119,75,['Rack PSU','AC → DC']);
  out+=connection('rack-psu','rack-dc',line(859,430,914,430));
  out+=energyNode('rack-bbu',770,229,194,86,['Rack BBU','Battery + DC/DC'],C.battery);
  out+=connection('rack-bbu','rack-dc',line(867,319,867,348,C.battery)+line(867,348,914,348,C.battery)+arrow(914,348,914,425,C.battery))+junction(914,430);
  out+=text(914,477,'Rack DC bus',17,C.muted);
  out+=connection('rack-dc','vrm',arrow(919,430,994,430));
  out+=energyNode('vrm',1000,392,84,75,['VRM']);
  out+=connection('vrm','chip-rail',line(1088,430,1111,430));
  out+=energyNode('capacitors',997,317,207,55,['Local capacitors'],C.heat);
  out+=connection('capacitors','chip-rail',arrow(1111,376,1111,425,C.heat))+junction(1111,430,C.heat);
  out+=connection('chip-rail','chip',arrow(1116,430,1131,430));
  out+=energyNode('chip',1137,392,70,75,['Chip']);
  out+=text(1111,487,'Core rail',17,C.muted);
 }
 return `<svg class="buffer-review-diagram energy-connections" viewBox="${compact?'0 0 390 1055':'0 0 1280 570'}" role="img" aria-labelledby="energy-connections-title energy-connections-description"><title id="energy-connections-title">Where backup power connects</title><desc id="energy-connections-description">One connected electrical path inside facility, rack and chip groupings. Grid, connected generator and BESS inverter supply facility AC. The UPS rectifier and batteries supply its DC link; the inverter supplies protected AC to the rack PSU. Rack BBU and PSU support the rack DC bus. The VRM supplies the chip rail, where nearby capacitors support brief current changes. Source contributions can overlap.</desc>${out}</svg>`;
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

function rampDown(state,compact){
 const response=state.response===0.4?0.4:0.2;
 const {energyKJ,peakBufferKW}=supplyHandoff({responseSeconds:response});
 let out='';
 if(compact){
  out+=box(12,20,93,75,'PSUs','',C.power,true)+arrow(109,57,132,57);
  out+=box(138,20,93,75,'DC bus','',C.ink,true)+arrow(235,57,258,57,C.battery);
  out+=box(264,20,114,75,'Buffer','Battery + DC/DC',C.battery,true);
  out+=text(195,130,'Bidirectional converter charges the battery',16,C.battery);
 }else{
  out+=box(160,19,210,74,'PSUs')+arrow(376,56,436,56);
  out+=box(442,19,210,74,'Rack DC bus','',C.ink)+arrow(658,56,718,56,C.battery);
  out+=box(724,19,330,74,'Bidirectional buffer','Battery + converter',C.battery);
 }
 const x=compact?58:140,y=compact?420:370,w=compact?285:945,h=compact?206:204;
 out+=text(compact?195:600,compact?176:137,'Power above the new GPU load',compact?19:25);
 out+=line(x,y,x+w,y,C.muted,2)+line(x,y,x,y-h-10,C.muted,2);
 out+=`<path d="M${x} ${y-h}L${x+w} ${y}H${x}Z" fill="${C.battery}" opacity=".18"/>`;
 out+=line(x,y-h,x+w,y,C.power,4);
 out+=text(x-12,y-h+6,'40 kW',compact?15:21,C.power,'end')+text(x-12,y+6,'0',compact?16:21,C.muted,'end');
 out+=text(x+w*.69,y-h*.8,'PSUs ramp down',compact?17:25,C.power);
 out+=text(x+w*.25,y-h*.27,'Into the buffer',compact?17:27,C.battery);
 out+=text(x,y+31,'0 s',compact?17:22,C.muted)+text(x+w,y+31,`${response} s`,compact?17:22,C.muted);
 out+=text(compact?195:600,compact?505:457,`${energyKJ} kJ to absorb`,compact?32:42,C.battery);
 out+=text(compact?195:600,compact?545:499,`${peakBufferKW} kW peak charging · ${energyKJ} kJ of room`,compact?20:26);
 out+=text(compact?195:600,compact?607:547,'Full or charge-limited → bus voltage rises',compact?17:22,C.heat);
 return svg(out,compact,`GPU demand drops by 40 kilowatts. Source power above the new load ramps from 40 kilowatts to zero over ${response} seconds. The shaded surplus is ${energyKJ} kilojoules absorbed by a battery through a bidirectional converter. Peak charging power is 40 kilowatts. A full or charge-limited buffer lets bus voltage rise unless another path handles the surplus.`);
}


export function renderBufferReview(id,state={},compact=false){
 if(id==='energy-locality')return renderEnergyConnections(compact);
 if(id==='source-handoff')return handoff(state,compact);
 if(id==='source-ramp-down')return rampDown(state,compact);
 if(id==='buffer-recharge')return '<figure class="buffer-review-figure"><img src="../assets/references/rack-recharge-between-bursts.png" alt="Recharge between bursts. An eight-kilojoule burst uses 40 kilowatts for 0.2 seconds. With 10 kilowatts of surplus, a one-second quiet interval allows recovery; a half-second interval provides only five kilojoules, leaving the buffer short. Energy equals power times time."></figure>';
 return null;
}
