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
  const x=compact?25:130,w=compact?340:900;
  let out=box(x,55,w,compact?600:500,'line')+text(x+25,95,'RACK',22,'muted','start');
  out+=box(x+20,120,w-40,compact?455:340,'power')+text(x+40,162,'Server / compute tray',compact?22:28,'power','start');
  const chips=[['CPU','General-purpose work'],['GPU','Parallel numerical work'],['Memory','Active data and state']];
  chips.forEach(([a,b],i)=>{const bx=compact?65:190+i*270,by=compact?195+i*115:255,bw=compact?260:240;out+=block(bx,by,bw,a,b,i===2?'data':'power',95)});
  out+=text(compact?195:580,compact?618:510,'Connected machines form a cluster',compact?19:25);
  return out;
}
function memory(compact) {
  const stages = [
    ['Storage', 'Saved model file'],
    ['System RAM', 'Holds the loaded data'],
    ['GPU memory', 'Holds the model for use'],
    ['GPU cores', 'Run the model'],
  ];
  let out='';
  stages.forEach(([name,job],i)=>{
    const x=compact?50:35+i*290,y=compact?55+i*153:190,w=compact?290:220;
    out+=block(x,y,w,name,job,'data',95);
    if(i<3) {
      out+=compact?line(`M195 ${y+101}V${y+140}`,'data',true):line(`M${x+w+8} ${y+47}H${x+277}`,'data',true);
      out+=text(compact?260:x+255,compact?y+129:y+12,['Read','Copy','Use'][i],18,'data');
    }
  });
  if(compact)out+=text(195,674,'One common model-loading path',19,'muted');
  else out+=text(145,335,'Keeps files when off',20,'muted')+text(580,435,'One common model-loading path',22,'muted');
  return `<g data-loading-path="storage-ram-gpu-memory-gpu-cores">${out}</g>`;
}
function network(compact,state) {
  const rate=Number(state.bandwidth)===1000?1000:100,payloadMb=8*8,travel=20;
  const sending=payloadMb/rate*1000,arrival=travel+sending;
  const x=compact?42:170,w=compact?300:880,y=compact?255:220;
  const scale=w/660,delayWidth=travel*scale,sendWidth=sending*scale;
  let out=text(compact?195:580,compact?50:60,'Same payload: 8 MB = 64 megabits',compact?20:27,'data');
  out+=block(compact?35:100,compact?90:95,compact?125:235,'Sender','Sends the bits','data',85)+
    block(compact?230:825,compact?90:95,compact?125:235,'Receiver','Gets the bits','data',85)+
    line(compact?'M165 131H224':'M344 138H814','data',true)+
    text(compact?195:580,compact?215:193,'Last bit arrives after:',compact?23:24);
  out+=`<rect x="${x}" y="${y}" width="${delayWidth}" height="56" fill="var(--heat)"/><rect x="${x+delayWidth}" y="${y}" width="${sendWidth}" height="56" fill="var(--data)"/>`;
  out+=line(`M${x} ${y+67}H${x+w}`,'muted');
  [0,330,660].forEach(n=>{out+=text(x+n*scale,y+96,`${n} ms`,compact?16:21,'muted')});
  const cx=compact?195:580;
  out+=text(cx,compact?414:389,`${travel} ms travel + ${sending} ms sending`,compact?22:28)+
    text(cx,compact?467:445,`= ${arrival} ms to receive the whole payload`,compact?19:27,'data');
  out+=text(cx,compact?542:512,'First bit: 20 ms at either link rate',compact?20:23,'heat');
  if(compact)out+=text(cx,615,'Ideal payload rate · no queues,',18,'muted')+text(cx,644,'overhead or retransmissions',18,'muted');
  else out+=text(cx,566,'Ideal payload rate · no queues, overhead or retransmissions',20,'muted');
  return `<g data-payload-mb="8" data-rate-mbps="${rate}" data-travel-ms="${travel}" data-sending-ms="${sending}" data-arrival-ms="${arrival}">${out}</g>`;
}
function heat(compact) {
  if(compact) return `<g data-heat-watts="500" data-chip-celsius="70" data-plate-celsius="45" data-inlet-celsius="30" data-outlet-celsius="35">`+
    block(65,55,260,'Chip','70 °C','heat',95)+
    line('M195 155V297','heat',true)+text(284,222,'500 W',26,'heat')+
    text(195,267,'Heat into the cold plate',19,'heat')+
    block(45,315,300,'Cold plate','45 °C','heat',105)+
    line('M48 500V400H83','power',true)+line('M307 400H345V500','data',true)+
    text(86,546,'30 °C in',23,'power')+text(295,546,'35 °C out',23,'data')+
    text(195,680,'Illustrative steady temperatures and heat rate',16,'muted')+'</g>';
  return `<g data-heat-watts="500" data-chip-celsius="70" data-plate-celsius="45" data-inlet-celsius="30" data-outlet-celsius="35">`+
    block(440,65,280,'Chip','70 °C','heat',95)+
    line('M580 165V295','heat',true)+text(690,235,'500 W',30,'heat')+
    block(365,315,430,'Cold plate','45 °C','heat',110)+
    line('M160 478V370H350','power',true)+line('M809 370H1000V478','data',true)+
    text(160,526,'Coolant in: 30 °C',25,'power')+text(1000,526,'Coolant out: 35 °C',25,'data')+
    text(580,573,'Illustrative steady temperatures and heat-transfer rate',21,'muted')+'</g>';
}
function cooling(compact) {
  if(compact) return text(195,45,'Equipment coolant loop',23,'power')+
    line('M65 120V255H325V120H65','power')+block(28,125,130,'Cold plate','Chip heat','heat',95)+box(243,120,104,125,'power')+text(295,158,'CDU',21,'power')+text(295,191,'side A',18)+
    line('M175 120H224','power',true)+line('M215 255H165','power',true)+
    line('M295 259V392','heat',true)+text(133,319,'Heat crosses',23,'heat')+text(126,351,'Fluids stay apart',19)+
    line('M65 425V565H325V425H65','data')+box(243,425,104,125,'data')+text(295,464,'CDU',21,'data')+text(295,497,'side B',18)+block(28,439,165,'Outdoor plant','Heat rejection','data',95)+
    line('M225 565H175','data',true)+text(195,625,'Facility coolant loop',23,'data')+text(195,685,'Liquid-to-liquid CDU example',20,'muted');
  return text(280,75,'Equipment coolant loop',27,'power')+text(880,75,'Facility coolant loop',27,'data')+
    line('M125 210V420H495V210H125','power')+line('M665 210V420H1035V210H665','data')+
    block(35,250,205,'Cold plate','Receives chip heat','heat')+box(450,230,90,160,'power')+box(620,230,90,160,'data')+
    text(580,157,'CDU heat exchanger',26)+line('M545 310H609','heat',true)+text(580,470,'Heat crosses',24,'heat')+
    text(580,511,'Fluids stay apart',22)+block(935,250,210,'Outdoor plant','Rejects heat','data')+
    line('M285 210H350','power',true)+line('M350 420H285','power',true)+line('M800 420H865','data',true)+line('M865 210H800','data',true)+
    text(580,580,'Liquid-to-liquid CDU example',22,'muted');
}
function pue(compact) {
  const x=compact?30:120,y=compact?190:200,w=compact?330:920,h=compact?160:180,it=w*5/6;
  let out=text(compact?195:580,compact?56:65,'Same illustrative one-hour interval',compact?20:25,'muted');
  out+=`<rect x="${x}" y="${y}" width="${it}" height="${h}" rx="6" fill="var(--power)"/><rect x="${x+it}" y="${y}" width="${w-it}" height="${h}" rx="6" fill="var(--heat)"/>`;
  out+=text(x+it/2,y+65,'IT',compact?27:32,'paper')+text(x+it/2,y+110,'100 kWh',compact?25:32,'paper');
  out+=text(x+it+(w-it)/2,y+72,'20',compact?19:30,'paper')+text(x+it+(w-it)/2,y+112,'kWh',compact?17:25,'paper');
  out+=text(compact?195:x+it+(w-it)/2,compact?411:166,'Support',compact?23:22,'heat');
  out+=text(compact?195:580,compact?476:460,'Facility total = 120 kWh',compact?26:32)+text(compact?195:580,compact?549:528,'PUE = 120 ÷ 100 = 1.20',compact?27:36,'power');
  out+=text(compact?195:580,compact?650:585,'Useful work is measured separately.',compact?21:24,'muted');
  return out;
}
export function renderTerminology(id,state={},compact=false) {
  const electricity=renderElectricity(id,state,compact);
  if(electricity) return electricity;
  const views={backup:()=>backup(compact),'ups-types':()=>upsTypes(compact,state),capacity:()=>capacity(compact),hardware:()=>hardware(compact),'memory-storage':()=>memory(compact),network:()=>network(compact,state),'heat-temperature':()=>heat(compact),cooling:()=>cooling(compact),pue:()=>pue(compact)};
  return defs+(views[id]?.()||'');
}
