import { renderElectricity } from './terminology-electricity.js';

const text = (x,y,value,size=24,color='text',anchor='middle') => `<text x="${x}" y="${y}" font-size="${size}" fill="var(--${color})" text-anchor="${anchor}">${value}</text>`;
const line = (d,color='power',arrow=false) => `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" ${arrow ? `marker-end="url(#term-${color})"` : ''}/>`;
const box = (x,y,w,h,color='line') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="var(--surface)" stroke="var(--${color})" stroke-width="2"/>`;
const defs = `<defs>${['power','heat','data','muted'].map(c=>`<marker id="term-${c}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M1 1L9 5L1 9Z" fill="var(--${c})"/></marker>`).join('')}</defs>`;
function block(x,y,w,title,subtitle,color='power',h=100) {
  return box(x,y,w,h,color)+text(x+w/2,y+40,title,24,color)+text(x+w/2,y+73,subtitle,19);
}
function backup(compact) {
  if(compact) return text(195,45,'One online UPS example',23,'muted')+
    block(40,80,310,'Utility / generator','Normal / alternate AC supply')+line('M195 182V220H248V283','power',true)+
    box(25,240,340,310,'power')+text(80,273,'UPS',25,'power')+
    block(150,295,195,'Rectifier','AC to DC','power',85)+
    line('M248 382V434','power',true)+text(300,424,'DC link',17,'power')+
    box(40,369,100,70,'data')+text(90,398,'Battery',20,'data')+text(90,423,'Energy',17)+
    line('M144 404H237','data',true)+block(150,445,195,'Inverter','DC to AC','power',85)+
    line('M248 534V570H195V582','power',true)+block(70,592,250,'Protected load','Receives AC output');
  return text(580,65,'One online UPS example',25,'muted')+
    block(25,250,235,'Utility / generator','Upstream AC supply')+
    box(310,170,540,225,'power')+text(580,210,'Uninterruptible power supply (UPS)',25,'power')+
    block(340,250,210,'Rectifier','AC to DC')+block(610,250,210,'Inverter','DC to AC')+
    line('M263 300H327','power',true)+line('M554 300H598','power',true)+line('M824 300H900','power',true)+
    block(915,250,225,'Protected load','Receives AC output')+
    block(470,440,220,'Battery','Stored energy','data')+line('M580 437V313','data',true)+text(658,420,'DC link support',20,'data');
}
function upsTypes(compact,state) {
  const interrupted=state.upsSupply==='interrupted';
  const flow=(d,active,color='power')=>active?line(d,color,true):`<path d="${d}" fill="none" stroke="var(--line)" stroke-width="3" stroke-dasharray="6 7"/>`;
  const unit=(x,y,w,name,active=true,color='power')=>box(x,y,w,56,active?color:'line')+text(x+w/2,y+35,name,compact?18:23,active?color:'muted');
  let out='';
  if(compact) {
    out+=text(195,33,'Offline / standby UPS',25)+text(195,66,'Common for desktop PCs',19,'muted');
    out+=unit(22,115,96,'Utility',!interrupted)+unit(280,115,90,'Load');
    out+=flow('M122 143H237',!interrupted)+flow('M258 143H274',true);
    out+=line(interrupted?'M258 143L237 177':'M258 143H237','power');
    out+=text(195,104,'Switch',17,'muted');
    out+=unit(24,213,103,'Battery',interrupted,'data')+unit(165,213,108,'Inverter',interrupted,'data');
    out+=flow('M132 241H159',interrupted,'data')+flow('M278 241H325V177H237',interrupted,'data');
    out+=text(195,302,interrupted?'Brief transfer, then battery power':'Utility feeds the load directly',19,interrupted?'data':'power');
    out+=line('M20 340H370','muted');
    out+=text(195,381,'Online double-conversion UPS',23)+text(195,414,'Data centers / sensitive medical systems',16,'muted');
    out+=text(71,451,interrupted?'Input lost':'Utility AC',17,interrupted?'muted':'power');
    out+=flow('M71 459V475',!interrupted);
    out+=unit(22,485,102,'Rectifier',!interrupted)+unit(171,485,100,'Inverter')+unit(297,485,74,'Load');
    out+=flow('M129 513H141',!interrupted)+flow('M146 513H165',true)+flow('M277 513H290',true);
    out+=unit(42,593,106,'Battery',interrupted,'data')+flow('M153 621H160V551H144V516',interrupted,'data');
    out+=text(146,472,'DC link',16,'power');
    out+=text(195,690,'Inverter keeps supplying the load',20,'power');
  } else {
    out+=text(60,40,'Offline / standby UPS',27,'text','start')+text(1100,40,'Common for desktop PCs',23,'muted','end');
    out+=unit(65,95,180,'Utility',!interrupted)+unit(905,95,190,'Load');
    out+=flow('M251 123H741',!interrupted)+flow('M792 123H897',true);
    out+=line(interrupted?'M792 123L748 171':'M792 123H741','power');
    out+=text(771,87,'Transfer switch',21,'muted');
    out+=unit(310,200,180,'Battery',interrupted,'data')+unit(570,200,190,'Inverter',interrupted,'data');
    out+=flow('M496 228H562',interrupted,'data')+flow('M766 228H860V171H748',interrupted,'data');
    out+=text(485,166,interrupted?'Brief transfer, then battery power':'Utility feeds the load directly',23,interrupted?'data':'power');
    out+=line('M40 284H1120','muted');
    out+=text(60,330,'Online double-conversion UPS',27,'text','start')+text(1100,330,'Data centers / sensitive medical systems',21,'muted','end');
    out+=unit(65,379,180,'Utility',!interrupted)+unit(330,379,180,'Rectifier',!interrupted)+unit(650,379,190,'Inverter')+unit(925,379,170,'Load');
    out+=flow('M251 407H321',!interrupted)+flow('M516 407H571',!interrupted)+flow('M579 407H642',true)+flow('M846 407H917',true);
    out+=unit(430,491,190,'Battery',interrupted,'data')+flow('M625 519H637V456H575V412',interrupted,'data');
    out+=text(575,365,'DC link',21,'power');
    out+=text(869,529,'Inverter keeps supplying the load',23,'power');
  }
  return `<g data-ups-supply="${interrupted?'interrupted':'normal'}" data-standby-path="${interrupted?'battery-inverter-switch':'utility-switch'}" data-online-path="${interrupted?'battery-dclink-inverter':'utility-rectifier-dclink-inverter'}">${out}</g>`;
}
function capacity(compact) {
  const cx=compact?195:580;
  let out=text(cx,compact?55:60,'Example load: 100 kW',28,'power')+text(cx,compact?102:103,'Each qualified module: 50 kW',22,'muted');
  const y=compact?205:260,w=compact?88:220,gap=compact?17:65,x=compact?46:185;
  for(let i=0;i<3;i++) out+=box(x+i*(w+gap),y,w,130,i===2?'data':'power')+text(x+i*(w+gap)+w/2,y+57,'50',30,i===2?'data':'power')+text(x+i*(w+gap)+w/2,y+93,'kW',21);
  out+=line(`M${x} ${y+155}v15h${w*2+gap}v-15`,'power')+text(x+(w*2+gap)/2,y+210,'N = 2 required',compact?21:26,'power');
  out+=text(x+2*(w+gap)+w/2,y+179,'+1 spare',compact?17:24,'data');
  return out;
}
function hardware(compact) {
  if(compact) return box(15,25,360,665)+text(37,61,'Rack',22,'muted','start')+
    box(30,90,330,535,'power')+text(50,127,'Compute server',24,'power','start')+
    block(55,152,280,'CPU','Runs the system','power',88)+
    box(55,264,280,72,'data')+text(195,309,'System RAM',24,'data')+
    box(55,371,280,226,'power')+text(75,408,'GPU',25,'power','start')+
    box(75,429,240,60,'data')+text(195,467,'GPU memory',23,'data')+
    box(75,516,240,60,'power')+text(195,554,'GPU cores',23,'power');
  return box(70,25,1020,535)+text(95,65,'Rack',24,'muted','start')+
    box(95,95,970,415,'power')+text(120,138,'Compute server',28,'power','start')+
    block(125,262,220,'CPU','Runs the system','power',100)+
    box(390,262,220,100,'data')+text(500,321,'System RAM',26,'data')+
    box(675,177,360,284,'power')+text(700,222,'GPU',28,'power','start')+
    box(705,252,300,74,'data')+text(855,298,'GPU memory',27,'data')+
    box(705,357,300,74,'power')+text(855,403,'GPU cores',27,'power');
}
function memory(compact) {
  let out;
  if(compact) out=box(25,210,340,482,'power')+text(45,247,'Compute server',24,'power','start')+
    box(55,407,280,258,'power')+text(75,442,'GPU',25,'power','start')+
    block(75,25,240,'Storage server','Saved model file','data',90)+
    line('M195 120V184H340V313H332','data',true)+text(216,168,'Network',20,'data','start')+
    box(70,278,250,70,'data')+text(195,321,'System RAM',23,'data')+
    line('M195 352V448','data',true)+text(223,382,'Copy',19,'data','start')+
    box(75,460,240,65,'data')+text(195,500,'GPU memory',23,'data')+
    line('M195 530V571','data',true)+
    box(75,582,240,60,'power')+text(195,620,'GPU cores',23,'power');
  else out=box(375,95,760,415,'power')+text(400,138,'Compute server',28,'power','start')+
    box(695,177,405,284,'power')+text(720,222,'GPU',28,'power','start')+
    block(25,210,215,'Storage server','Saved model file','data',100)+
    line('M245 260H393','data',true)+text(318,230,'Network',22,'data')+
    box(405,220,215,90,'data')+text(512,275,'System RAM',26,'data')+
    line('M625 265H717','data',true)+text(659,236,'Copy',20,'data')+
    box(730,240,335,74,'data')+text(897,286,'GPU memory',27,'data')+
    line('M897 319V349','data',true)+
    box(730,360,335,74,'power')+text(897,406,'GPU cores',27,'power');
  return `<g data-loading-path="storage-ram-gpu-memory-gpu-cores" data-storage-location="network-storage-server">${out}</g>`;
}
function network(compact,state) {
  const rate=Number(state.bandwidth)===100000?100000:10000,payloadMb=8*8,travel=0.01;
  const sending=payloadMb/rate*1000,arrival=travel+sending;
  const x=compact?35:140,w=compact?320:880,y=compact?309:269;
  const scale=w/6.41,delayWidth=travel*scale,sendWidth=sending*scale;
  let out=text(compact?195:580,compact?42:45,'8 MB chunk = 64 megabits',compact?22:29,'data');
  if(compact) out+=box(20,87,151,90,'data')+text(95,124,'Storage',22,'data')+text(95,153,'server',21,'data')+
    box(219,87,151,90,'power')+text(294,124,'Compute',22,'power')+text(294,153,'server',21,'power')+
    line('M177 132H211','data',true)+text(195,214,'Data-center network',22,'data')+
    text(195,254,`${rate/1000} Gb/s payload rate`,23,'data');
  else out+=box(100,90,255,95,'data')+text(227,146,'Storage server',27,'data')+
    box(805,90,255,95,'power')+text(932,146,'Compute server',27,'power')+
    line('M363 139H795','data',true)+text(580,116,'Data-center network',24,'data')+
    text(580,175,`${rate/1000} Gb/s payload rate`,24,'data');
  out+=text(compact?195:580,compact?291:242,'Illustrative transfer · no queues or overhead',compact?16:21,'muted');
  out+=`<rect x="${x}" y="${y}" width="${delayWidth}" height="56" fill="var(--heat)"/><rect x="${x+delayWidth}" y="${y}" width="${sendWidth}" height="56" fill="var(--data)"/>`;
  out+=line(`M${x} ${y+67}H${x+w}`,'muted');
  [0,3.2,6.4].forEach(n=>{out+=text(x+n*scale,y+97,`${n} ms`,compact?16:21,'muted',n===0?'start':n===6.4?'end':'middle')});
  const cx=compact?195:580;
  out+=text(cx,compact?464:421,`${sending} ms to send all the bits`,compact?25:29,'data')+
    text(cx,compact?506:463,'10 μs first-bit latency at either rate',compact?20:25,'heat')+
    text(cx,compact?586:535,`All 8 MB arrive in ${arrival.toFixed(2)} ms`,compact?25:34,'data');
  return `<g data-payload-mb="8" data-rate-mbps="${rate}" data-travel-ms="${travel}" data-sending-ms="${sending}" data-arrival-ms="${arrival}" data-sender="storage-server" data-receiver="compute-server">${out}</g>`;
}
function heat(compact) {
  if(compact) return `<g data-heat-watts="500" data-chip-celsius="70" data-plate-celsius="45" data-inlet-celsius="30" data-outlet-celsius="35">`+
    text(195,33,'Compute server',22,'power')+
    box(40,57,310,558,'power')+
    text(195,89,'500 W electrical input',20,'power')+line('M195 95V112','power',true)+
    box(65,120,260,155,'power')+text(88,156,'GPU',25,'power','start')+
    text(195,203,'Running the model',22,'power')+text(195,241,'70 °C',28,'heat')+
    line('M195 280V347','heat',true)+text(282,310,'500 W',26,'heat')+text(282,339,'Heat',19,'heat')+
    block(65,365,260,'Cold plate','45 °C','heat',105)+
    line('M25 563V423H56','power',true)+line('M332 423H365V563','data',true)+
    text(91,595,'30 °C in',22,'power')+text(299,595,'35 °C out',22,'data')+
    text(195,662,'Illustrative steady operation',19,'muted')+'</g>';
  return `<g data-heat-watts="500" data-chip-celsius="70" data-plate-celsius="45" data-inlet-celsius="30" data-outlet-celsius="35">`+
    box(325,30,510,475,'power')+text(350,71,'Compute server',26,'power','start')+
    box(415,100,330,145,'power')+text(440,140,'GPU',28,'power','start')+
    text(580,180,'Running the model',25,'power')+text(580,219,'70 °C',29,'heat')+
    text(170,147,'Electrical input',24,'power')+text(170,183,'500 W',28,'power')+line('M270 178H404','power',true)+
    line('M580 250V348','heat',true)+text(685,297,'500 W',30,'heat')+text(685,331,'Heat',22,'heat')+
    block(380,365,400,'Cold plate','45 °C','heat',110)+
    line('M145 458V420H368','power',true)+line('M792 420H1015V458','data',true)+
    text(145,507,'Coolant in: 30 °C',23,'power')+text(1015,507,'Coolant out: 35 °C',23,'data')+
    text(580,561,'Illustrative steady operation',23,'muted')+'</g>';
}
function cooling(compact) {
  if(compact) return text(195,31,'Equipment coolant loop',23,'power')+
    box(40,61,120,64,'power')+text(100,102,'GPU',24,'power')+line('M100 130V174','heat',true)+
    line('M100 194V286H306V194H100','power')+
    box(30,183,140,70,'heat')+text(100,227,'Cold plate',23,'heat')+
    box(256,173,100,102,'power')+text(306,215,'CDU',23,'power')+text(306,247,'side A',18)+
    line('M177 194H245','power',true)+line('M232 286H176','power',true)+
    `<circle cx="208" cy="286" r="19" fill="var(--surface)" stroke="var(--power)" stroke-width="2"/>`+
    line('M215 277L201 286L215 295','power')+text(208,327,'Pump',19,'power')+
    line('M306 291V420','heat',true)+text(125,365,'Heat crosses',23,'heat')+text(125,398,'Fluids stay apart',19)+
    line('M100 455V591H306V455H100','data')+
    box(256,430,100,112,'data')+text(306,474,'CDU',23,'data')+text(306,507,'side B',18)+
    block(25,445,165,'Outdoor plant','Fans reject heat','data',98)+
    line('M225 591H164','data',true)+text(195,640,'Facility coolant loop',23,'data');
  return text(280,42,'Equipment coolant loop',27,'power')+text(880,42,'Facility coolant loop',27,'data')+
    box(65,82,210,77,'power')+text(170,130,'GPU',28,'power')+line('M170 164V238','heat',true)+
    line('M170 260V420H495V260H170','power')+line('M665 260V420H1040V260H665','data')+
    box(55,250,230,90,'heat')+text(170,305,'Cold plate',27,'heat')+
    box(450,230,90,160,'power')+box(620,230,90,160,'data')+
    text(580,150,'CDU heat exchanger',26)+line('M546 310H609','heat',true)+
    text(580,480,'Heat crosses',24,'heat')+text(580,518,'Fluids stay apart',22)+
    block(930,250,220,'Outdoor plant','Fans reject heat','data')+
    line('M300 260H359','power',true)+line('M350 420H285','power',true)+
    `<circle cx="370" cy="420" r="23" fill="var(--surface)" stroke="var(--power)" stroke-width="2"/>`+
    line('M379 408L360 420L379 432','power')+text(370,469,'Pump',23,'power')+
    line('M800 420H865','data',true)+line('M865 260H800','data',true);
}
function pue(compact) {
  const x=compact?30:120,y=compact?190:215,w=compact?330:920,h=compact?145:145,it=w*5/6;
  let out=text(compact?195:580,compact?37:48,'Whole facility · one-hour example',compact?20:26,'muted');
  if(compact) out+=text(167,148,'Computers · storage · network',18,'power');
  else out+=text(x+it/2,142,'Computers · storage · network',25,'power')+
    text(x+it+(w-it)/2,110,'Pumps · fans',24,'heat')+
    text(x+it+(w-it)/2,147,'Power losses',24,'heat')+
    text(x+it+(w-it)/2,184,'Support',25,'heat');
  out+=`<rect x="${x}" y="${y}" width="${it}" height="${h}" rx="6" fill="var(--power)"/><rect x="${x+it}" y="${y}" width="${w-it}" height="${h}" rx="6" fill="var(--heat)"/>`;
  out+=text(x+it/2,y+65,'IT',compact?27:32,'paper')+text(x+it/2,y+110,'100 kWh',compact?25:32,'paper');
  out+=text(x+it+(w-it)/2,y+72,'20',compact?19:30,'paper')+text(x+it+(w-it)/2,y+112,'kWh',compact?17:25,'paper');
  if(compact) out+=line('M332 340V367H195V382','heat')+text(195,413,'Support',25,'heat')+
    text(195,449,'Pumps · fans · power losses',20,'heat');
  out+=text(compact?195:580,compact?526:431,'Facility total = 120 kWh',compact?26:32)+
    text(compact?195:580,compact?592:493,'Power usage effectiveness',compact?23:26,'power')+
    text(compact?195:580,compact?640:543,'PUE = 120 ÷ 100 = 1.20',compact?27:36,'power');
  return out;
}
export function renderTerminology(id,state={},compact=false) {
  const electricity=renderElectricity(id,state,compact);
  if(electricity) return electricity;
  const views={backup:()=>backup(compact),'ups-types':()=>upsTypes(compact,state),capacity:()=>capacity(compact),hardware:()=>hardware(compact),'memory-storage':()=>memory(compact),network:()=>network(compact,state),'heat-temperature':()=>heat(compact),cooling:()=>cooling(compact),pue:()=>pue(compact)};
  return defs+(views[id]?.()||'');
}
