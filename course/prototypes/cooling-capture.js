import {deviceTemperature,hydraulicPoint,parallelBranches} from './cooling-capture-model.js';
const n=(v,d=1)=>Number(v.toFixed(d)).toString();
const text=(x,y,s,size=28,color='ink',anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" style="font-size:${size}px;fill:var(--${color})">${s}</text>`;
const box=(x,y,w,h)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="var(--panel)" stroke="var(--line)"/>`;
const path=(d,c='tech')=>`<path d="${d}" fill="none" stroke="var(--${c})" stroke-width="4"/>`;
const card=(x,y,w,title,big,detail='',color='tech')=>box(x,y,w,180)+text(x+w/2,y+38,title,26)+text(x+w/2,y+100,big,45,color)+(detail?text(x+w/2,y+149,detail,23):'');
const control=(key,label,options)=>({key,label,options});
export const captureScenes=[
{id:'local-heat-flux',label:'Heat concentrated on the chip',title:'The same heat can be harder to remove',reference:'d10-local-thermal-paths',kind:'capture-detail',pedagogical_role:'comparison',description:'Two 400 W devices have heat-transfer areas of 4 and 1 square centimetres. Their average heat fluxes are 100 and 400 W per square centimetre; neither value by itself establishes junction temperature.'},
{id:'device-temperature',label:'Coolant and chip temperature',title:'The chip is hotter than the coolant',reference:'d10-local-thermal-paths',kind:'capture-detail',pedagogical_role:'comparison',description:'Chip temperature equals local coolant temperature plus the temperature rise through the heat-transfer path. Thermal resistance is the temperature rise needed for each watt of heat. Both examples hold heat at 400 W and local coolant at 35°C: 0.08°C/W adds 32°C for a 67°C chip; 0.12°C/W adds 48°C for an 83°C chip. The example chip limit is 80°C.'},
{id:'pump-operating-point',label:'Flow needs pressure',title:'More restriction means less coolant flow',reference:'d10-flow-and-pressure',kind:'capture-detail',pedagogical_role:'mechanism',description:'At the same pump speed, the pump curve shows available pressure and each circuit curve shows required pressure. The pump and circuit curves cross at the actual flow. Both circuits are visible: the clean circuit crosses at 2 L/s and an added restriction moves the crossing left to 1.41 L/s. With q in L/s, the example curves are 160 − 10q² kPa for the pump, 30q² for the clean circuit and 70q² for the restricted circuit.'},
{id:'branch-flow',label:'Total flow can hide a hot branch',title:'Two litres per second can still leave one branch short',reference:'d10-flow-and-pressure',kind:'capture-detail',pedagogical_role:'counterexample',description:'A controller maintains 2 L/s total water flow for two 42 kW branches. A restriction redistributes flow from 1 plus 1 to .5 plus 1.5 L/s. The mixed return remains 45 degrees, while the restricted branch reaches 55 degrees.',controls:[control('branch','Flow split',[['balanced','Balanced'],['restricted','Restricted branch']])]},
{id:'coolant-interfaces',label:'Qualify the complete liquid path',title:'Every wetted part has to work with the coolant',reference:'d10-cdu-interfaces',kind:'capture-detail',pedagogical_role:'architecture',description:'The cold plate, quick disconnects, hoses, filters and CDU share a coolant circuit. Material and fluid compatibility, qualified pressure, cleanliness and leak isolation are interface requirements.'},
{id:'cooling-retrofit',label:'A cold-plate retrofit',title:'The remaining air heat fits this room',reference:'d10-cdu-interfaces',kind:'capture-detail',pedagogical_role:'transfer',description:'A fixed worked example: a 100 kW rack sends 85 kW into cold plates and 15 kW into room air. The remaining 15 kW fits the existing 20 kW room-air allowance, leaving 5 kW spare. The liquid path must carry the other 85 kW; meeting the air allowance alone does not establish liquid-loop capacity or qualification.'}
];
function flux(small){const w=small?420:1100;let b='';for(const [i,area]of [4,1].entries()){const cx=small?210:280+i*540,cy=small?140+i*290:225,side=area===4?140:70;b+=text(cx,cy-104,'400 W',34,'heat')+`<rect x="${cx-side/2}" y="${cy-side/2}" width="${side}" height="${side}" fill="var(--heatfill)" stroke="var(--heat)" stroke-width="3"/>`+text(cx,cy+110,`${area} cm² → ${400/area} W/cm²`,29);}return b+text(w/2,small?685:468,'Heat flux = heat ÷ area',29);}
function temperature(_state,small){
  const w=small?420:1100;
  let b=text(w/2,32,'400 W per chip · local coolant 35°C',small?22:28);
  const definition=small?['Thermal resistance: how much hotter','the chip must be for each watt of heat.']:['Thermal resistance: how much hotter the chip must be for each watt of heat.'];
  definition.forEach((line,i)=>b+=text(w/2,(small?70:78)+i*27,line,small?21:25));
  for(const [i,r] of [.08,.12].entries()){
    const x=small?20:35+i*550,y=small?120+i*255:112,cw=small?380:500,ch=small?235:290;
    const m=deviceTemperature({fluidC:35,resistance:r}),rise=m.junctionC-35,color=m.passes?'facility':'fault';
    b+=box(x,y,cw,ch)+text(x+cw/2,y+35,i===0?'Easier path for heat':'Harder path for heat',small?25:28)
      +text(x+cw/2,y+75,`${r}°C/W × 400 W = ${rise}°C rise`,small?23:27)
      +text(x+cw/2,y+(small?115:130),'Coolant + temperature rise = chip',small?20:25)
      +text(x+cw/2,y+(small?160:190),`35°C + ${rise}°C = ${n(m.junctionC)}°C`,small?31:40,color)
      +text(x+cw/2,y+(small?205:250),`${n(Math.abs(m.marginK))}°C ${m.passes?'below':'above'} the 80°C limit`,small?23:27,color);
  }
  const conclusion=small?['The same coolant can produce','different chip temperatures.']:['The harder heat-transfer path makes the chip hotter, even with the same coolant.'];
  conclusion.forEach((line,i)=>b+=text(w/2,(small?657:459)+i*28,line,small?24:27));
  return b;
}
function hydraulics(_state,small){
  const w=small?420:1100,left=small?62:80,right=small?390:680,top=small?160:125,bottom=small?398:361;
  const x=q=>left+q/2.6*(right-left),y=p=>bottom-p/200*(bottom-top);
  const curves=[{label:'Pump: pressure available',color:'tech',f:q=>160-10*q*q},
    {label:'Clean circuit: pressure needed',color:'facility',f:q=>30*q*q},
    {label:'Restricted circuit: pressure needed',color:'fault',f:q=>70*q*q,dash:true}];
  let b=text(w/2,35,'Same pump speed in both cases',small?22:27);
  curves.forEach((curve,i)=>{
    const lx=small?18:28+i*358,ly=small?55+i*28:61;
    b+=`<path d="M${lx} ${ly-6}h30" fill="none" stroke="var(--${curve.color})" stroke-width="4"${curve.dash?' stroke-dasharray="8 5"':''}/>`
      +text(lx+40,ly,curve.label,18,'ink','start');
  });
  b+=path(`M${left} ${top}V${bottom}H${right}`,'muted')+text(left,top-17,'kPa',19);
  for(const p of [0,100,200])b+=text(left-10,y(p)+7,p,19,'muted','end');
  for(const q of [0,1,2])b+=text(x(q),bottom+26,q,20,'muted');
  b+=text((left+right)/2,bottom+57,'Flow (L/s)',small?22:24);
  for(const curve of curves){
    const pts=[];
    for(let step=0;step<=260;step++){
      const q=step/100,p=curve.f(q);
      if(p>=0&&p<=200)pts.push(`${x(q)},${y(p)}`);
    }
    b+=`<polyline data-curve="${curve.color==='tech'?'pump':curve.dash?'restricted':'clean'}" points="${pts.join(' ')}" fill="none" stroke="var(--${curve.color})" stroke-width="4"${curve.dash?' stroke-dasharray="8 5"':''}/>`;
  }
  for(const [i,resistance] of [30,70].entries()){
    const m=hydraulicPoint({resistance}),color=i===0?'facility':'fault',point=i===0?'A':'B',px=x(m.flowLs),py=y(m.pressureKPa);
    b+=`<path d="M${px} ${py}V${bottom}" fill="none" stroke="var(--${color})" stroke-width="2" stroke-dasharray="3 5"/>`
      +`<circle cx="${px}" cy="${py}" r="8" fill="var(--panel)" stroke="var(--${color})" stroke-width="4"/>`
      +text(px+(i===0?16:-17),py+(i===0?25:-20),point,24,color);
    const cx=small?15+i*205:740,cy=small?480:100+i*155,cw=small?185:325;
    b+=box(cx,cy,cw,small?110:130)+text(cx+cw/2,cy+32,`${point} · ${i===0?'Clean':'Restricted'}`,small?23:26)
      +text(cx+cw/2,cy+(small?79:90),`${n(m.flowLs,2)} L/s`,small?33:42,color);
  }
  const lines=small?['At each crossing, pump pressure','equals the circuit’s pressure need.','Restriction moves it left: less flow.']:['At each crossing, pump pressure equals the circuit’s pressure need.','Adding a restriction moves the crossing left: less coolant flow.'];
  lines.forEach((line,i)=>b+=text(w/2,(small?637:450)+i*(small?28:32),line,small?22:26));
  return b;
}
function branches(state,small){const m=parallelBranches(state.branch==='restricted'),w=small?420:1100;let b=text(w/2,40,'35°C supply · 42 kW in each branch',small?23:28);for(let i=0;i<2;i++){const x=small?20:35+i*550,y=small?80+i*230:120,cw=small?380:500;b+=card(x,y,cw,`${m.flows[i]} L/s`,`${n(m.returns[i])}°C return`,i===0?'Branch A':'Branch B',m.returns[i]>50?'fault':'tech');}return b+text(w/2,small?625:405,`Total 2 L/s · mixed return ${n(m.mixedReturnC)}°C`,small?25:33)+text(w/2,small?680:465,'Water · 1 kg/L · cp = 4.2 kJ/(kg·K)',small?21:25);}
function interfaces(small){const w=small?420:1100;let b='';const names=['Cold plate','Hoses + connectors','CDU'];for(let i=0;i<3;i++){const x=small?40:25+i*370,y=small?50+i*175:90,cw=small?340:320;b+=box(x,y,cw,110)+text(x+cw/2,y+62,names[i],28)+(i<2?text(small?210:x+345,small?y+146:y+66,small?'↓':'→',37,'tech'):'');}const ys=small?[607,647,687]:[290,350,410];['Fluid + materials','Pressure + cleanliness','Leak detection + isolation'].forEach((v,i)=>b+=text(w/2,ys[i],v,small?26:34));return b;}
function retrofit(_state,small){
  const w=small?420:1100,cx=w/2;
  let b=text(cx,34,'Cold plates capture 85% of rack heat',small?23:30)
    +box(cx-110,65,220,115)+text(cx,103,'Rack heat',26)+text(cx,156,'100 kW',42,'heat');
  for(let i=0;i<2;i++){
    const bx=small?15+i*205:60+i*530,by=small?245:250,bw=small?185:450,mid=bx+bw/2,color=i===0?'tech':'heat';
    b+=path(`M${cx} 180V210H${mid}V${by-12}`,color)
      +`<path d="M${mid-7} ${by-12}L${mid} ${by}L${mid+7} ${by-12}Z" fill="var(--${color})"/>`
      +box(bx,by,bw,small?190:165)+text(mid,by+35,i===0?'Cold plates':'Room air',small?25:29)
      +text(mid,by+92,i===0?'85 kW':'15 kW',small?39:45,color);
    const detail=i===0?(small?['Liquid system','carries this heat']:['Liquid system carries this heat']):(small?['Fans cool the','remaining parts']:['Fans cool the remaining parts']);
    detail.forEach((line,j)=>b+=text(mid,by+(small?135:139)+j*27,line,small?20:25));
  }
  const barX=small?30:230,barY=small?527:489,barW=small?360:640,barH=40;
  b+=text(cx,barY-24,'Room cooling: 20 kW capacity',small?25:30)
    +`<rect x="${barX}" y="${barY}" width="${barW}" height="${barH}" rx="8" fill="var(--panel)" stroke="var(--line)"/>`
    +`<rect x="${barX}" y="${barY}" width="${barW*.75}" height="${barH}" rx="8" fill="var(--facility)" opacity=".2"/>`
    +text(barX+barW*.375,barY+27,'15 kW used',small?20:24,'facility')
    +text(barX+barW*.875,barY+27,small?'5 kW':'5 kW spare',small?20:24)
    +text(cx,small?614:579,'15 kW fits the 20 kW air allowance.',small?23:29,'facility')
    +text(cx,small?667:626,'Size the liquid path for the other 85 kW.',small?22:27);
  return b;
}
export function renderCapture(id,state,compact){switch(id){case'local-heat-flux':return flux(compact);case'device-temperature':return temperature(state,compact);case'pump-operating-point':return hydraulics(state,compact);case'branch-flow':return branches(state,compact);case'coolant-interfaces':return interfaces(compact);case'cooling-retrofit':return retrofit(state,compact);default:throw new Error(`Unknown capture scene ${id}`);}}
