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
function capacity(compact) {
  const cx=compact?195:580;
  let out=text(cx,compact?55:60,'Example load: 100 kW',28,'power')+text(cx,compact?102:103,'Each qualified module: 50 kW',22,'muted');
  const y=compact?205:260,w=compact?88:220,gap=compact?17:65,x=compact?46:185;
  for(let i=0;i<3;i++) out+=box(x+i*(w+gap),y,w,130,i===2?'data':'power')+text(x+i*(w+gap)+w/2,y+57,'50',30,i===2?'data':'power')+text(x+i*(w+gap)+w/2,y+93,'kW',21);
  out+=line(`M${x} ${y+155}v15h${w*2+gap}v-15`,'power')+text(x+(w*2+gap)/2,y+210,'N = 2 required',compact?21:26,'power');
  out+=text(x+2*(w+gap)+w/2,y+179,'+1 spare',compact?17:24,'data');
  if(compact) out+=text(cx,540,'N+1 adds a module',24)+text(cx,600,'The surviving path still matters.',20,'muted');
  else out+=text(cx,550,'N+1 describes provision. We will test surviving service in D05.',25,'muted');
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
  if(compact) return block(45,60,300,'Storage','Saved files and checkpoints','data')+
    line('M140 165V248','data',true)+text(206,208,'Read data',20,'data')+
    block(45,265,300,'Working memory','RAM / HBM: active state','data')+
    line('M195 368V445','data',true)+block(45,465,300,'Processor','Uses the active data')+
    line('M348 510H374V110H353','data',true)+text(195,640,'Checkpoint: save job state',23,'data')+
    text(195,690,'GB = bytes of capacity',22,'muted');
  return block(40,200,270,'Storage','Saved files and checkpoints','data')+block(435,200,290,'Working memory','RAM / HBM: active state','data')+
    block(860,200,250,'Processor','Uses the active data')+line('M314 250H423','data',true)+text(370,190,'Read data',21,'data')+
    line('M730 250H848','data',true)+line('M985 304V430H175V313','data',true)+text(580,472,'Checkpoint: save job state to storage',26,'data')+
    text(580,560,'GB describes capacity. GB/s describes a transfer rate.',25,'muted');
}
function network(compact) {
  const blocks=compact?[[30,80,330],[30,245,330],[30,410,330]]:[[60,165,250],[455,165,250],[850,165,250]];
  let out=''; ['Machine A','Network switch','Machine B'].forEach((n,i)=>{const[x,y,w]=blocks[i];out+=block(x,y,w,n,['Sends data','Forwards traffic','Receives data'][i],'data');if(i<2)out+=compact?line(`M195 ${y+109}V${y+150}`,'data',true):line(`M${x+w+12} ${y+50}H${x+380}`,'data',true)});
  const cx=compact?195:580;
  out+=text(cx,compact?576:370,'Bandwidth: transfer-rate capability',compact?20:28,'data')+text(cx,compact?612:412,'Example unit: gigabits per second (Gb/s)',compact?17:23,'muted');
  out+=text(cx,compact?658:505,'Latency: elapsed time',compact?23:28)+text(cx,compact?694:547,'Example unit: milliseconds (ms)',compact?18:23,'muted');
  return out;
}
function heat(compact) {
  if(compact) return block(45,90,300,'Warmer chip','Temperature in °C','heat')+line('M195 210V373','heat',true)+text(195,286,'Heat-transfer rate',23,'heat')+text(267,338,'in kW',23,'heat')+block(45,405,300,'Cooler coolant','Temperature in °C','power')+text(195,610,'°C: thermal state',23)+text(195,660,'kW: energy transferred per second',19);
  return block(85,170,290,'Warmer chip','Temperature in °C','heat')+block(785,170,290,'Cooler coolant','Temperature in °C','power')+
    line('M390 220H770','heat',true)+text(580,162,'Heat-transfer rate',27,'heat')+text(580,273,'in kW',25,'heat')+
    text(320,440,'°C describes a thermal state',26)+text(825,440,'kW describes a rate',26)+text(580,530,'The later cooling lessons connect temperature, heat load and flow.',24,'muted');
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
  const views={backup:()=>backup(compact),capacity:()=>capacity(compact),hardware:()=>hardware(compact),'memory-storage':()=>memory(compact),network:()=>network(compact),'heat-temperature':()=>heat(compact),cooling:()=>cooling(compact),pue:()=>pue(compact)};
  return defs+(views[id]?.()||'');
}
