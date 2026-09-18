import {deviceTemperature,hydraulicPoint,parallelBranches} from './cooling-capture-model.js';
const n=(v,d=1)=>Number(v.toFixed(d)).toString();
const text=(x,y,s,size=28,color='ink',anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" style="font-size:${size}px;fill:var(--${color})">${s}</text>`;
const box=(x,y,w,h)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="var(--panel)" stroke="var(--line)"/>`;
const path=(d,c='tech')=>`<path d="${d}" fill="none" stroke="var(--${c})" stroke-width="4"/>`;
const card=(x,y,w,title,big,detail='',color='tech')=>box(x,y,w,180)+text(x+w/2,y+38,title,26)+text(x+w/2,y+100,big,45,color)+(detail?text(x+w/2,y+149,detail,23):'');
const control=(key,label,options)=>({key,label,options});
export const captureScenes=[
{id:'local-heat-flux',label:'Heat concentrated on the chip',title:'The same heat can be harder to remove',reference:'d10-local-thermal-paths',kind:'capture-detail',pedagogical_role:'comparison',description:'Two 400 W devices have heat-transfer areas of 4 and 1 square centimetres. Their average heat fluxes are 100 and 400 W per square centimetre. Heat flux is heat transfer rate per unit area, shown here in W/cm². Thermal resistance is the chip-to-coolant temperature difference per watt of heat transfer, in °C/W. Heat flux alone does not establish junction temperature or thermal resistance.'},
{id:'device-temperature',label:'Coolant and chip temperature',title:'Why 35°C coolant can leave a chip above 80°C',reference:'d10-local-thermal-paths',kind:'capture-detail',pedagogical_role:'comparison',description:'Follow the same 400 W of heat from each chip through its cold plate into 35°C local coolant. ΔT means chip temperature minus coolant temperature: ΔT = 400 W × thermal resistance. The lower-resistance path needs ΔT = 32°C, so its chip reaches 67°C; the higher-resistance path needs ΔT = 48°C, so its chip reaches 83°C and exceeds the example 80°C limit. Thermal resistance includes the complete chip-to-coolant path. Heat flux on the preceding slide describes how concentrated the heat is. Smaller area can make that path harder to cool, but area alone does not determine thermal resistance; the two resistance values here are independently specified examples.'},
{id:'pump-operating-point',label:'Flow and pump pressure',title:'The pump and circuit determine the flow',reference:'d10-flow-and-pressure',kind:'capture-detail',pedagogical_role:'mechanism',description:'At fixed pump speed, the descending curve shows pressure available from the pump and the ascending curve shows pressure required by the complete coolant circuit. The example curves are Δp_pump = 160 − 10q² and Δp_circuit = 30q², with q in L/s and pressure in kPa. They meet at 2 L/s and 120 kPa, operating point A. A second circuit curve, Δp = 70q², represents higher resistance such as a partly closed valve. It meets the same pump curve at 1.41 L/s and 140 kPa, operating point B: more resistance reduces flow at unchanged pump speed. Below this flow the pump adds more pressure than the circuit requires; above it the circuit requires more than the pump provides. Pressure means the rise across the pump and the balancing loss around the closed circuit, not absolute coolant pressure. These curves illustrate the mechanism rather than a named CDU rating. See KSB’s Centrifugal Pump Lexicon, Characteristic curve and Operating point.'},
{id:'branch-flow',label:'Total flow can hide a hot branch',title:'Two litres per second can still leave one branch short',reference:'d10-flow-and-pressure',kind:'capture-detail',pedagogical_role:'counterexample',description:'A controller maintains 2 L/s total water flow for two 42 kW branches. A restriction redistributes flow from 1 plus 1 to .5 plus 1.5 L/s. The mixed return remains 45 degrees, while the restricted branch reaches 55 degrees.',controls:[control('branch','Flow split',[['balanced','Balanced'],['restricted','Restricted branch']])]},
{id:'coolant-interfaces',label:'Qualify the complete liquid path',title:'Every wetted part has to work with the coolant',reference:'d10-cdu-interfaces',kind:'capture-detail',pedagogical_role:'architecture',description:'The cold plate, quick disconnects, hoses, filters and CDU share a coolant circuit. Material and fluid compatibility, qualified pressure, cleanliness and leak isolation are interface requirements.'},
{id:'cooling-response',label:'Test the power reduction',title:'Test the power reduction after a cooling failure',reference:'d10-cdu-interfaces',kind:'capture-detail',pedagogical_role:'mechanism',description:'Continue the preceding 1,000 kW liquid-heat example after two CDUs fail, leaving 600 kW cooling. The control system requests a reduction in IT power for the affected racks. Confirm the response through measured power, flow and temperatures. Here the measured heat entering coolant settles at 500 kW, within the 600 kW cooling capacity. The trace is qualitative; it does not prescribe a response time or imply that 500 kW liquid heat equals a 500 kW electrical cap.'},
{id:'cooling-retrofit',label:'A cold-plate retrofit',title:'The remaining 15 kW still needs a cooling path',reference:'d10-cdu-interfaces',kind:'capture-detail',pedagogical_role:'transfer',description:'A 100 kW rack sends 85 kW into cold plates and 15 kW into residual air. That residual heat can use 15 kW of the room’s 20 kW cooling allowance, leaving 5 kW spare, or pass through a rear-door heat exchanger into liquid. The illustrated RDHX captures all 15 kW; only air heat left after the door would use the room allowance.'}
];
function flux(small){
  const w=small?420:1100;let b='';
  for(const [i,area]of [4,1].entries()){
    const cx=small?210:280+i*540,cy=small?140+i*290:225,side=area===4?140:70;
    b+=text(cx,cy-104,'400 W',34,'heat')+`<rect x="${cx-side/2}" y="${cy-side/2}" width="${side}" height="${side}" fill="var(--heatfill)" stroke="var(--heat)" stroke-width="3"/>`+text(cx,cy+110,`${area} cm² → ${400/area} W/cm²`,29);
  }
  if(small){
    return b+text(w/2,580,'Heat flux (W/cm²)',25)
      +text(w/2,611,'Heat transfer rate per unit area',21)
      +text(w/2,666,'Thermal resistance (°C/W)',25)
      +text(w/2,697,'Chip-to-coolant temperature difference per watt',18);
  }
  return b+text(w/2,419,'Heat flux = heat transfer rate ÷ area (W/cm²)',27)
    +text(w/2,469,'Thermal resistance = chip-to-coolant temperature difference ÷ heat rate (°C/W)',24);
}
function temperature(_state,small){
  const w=small?420:1100,fluidC=35,watts=400,limitC=80;
  let b=small?'':`<path d="M550 12V410" stroke="var(--line)"/>`;
  for(const [i,resistance] of [.08,.12].entries()){
    const m=deviceTemperature({fluidC,watts,resistance,limitC}),color=m.passes?'facility':'fault';
    const origin=small?i*317:0,cx=small?148:235+i*550;
    const chipY=origin+(small?58:95),chipW=small?218:270,chipH=small?63:85;
    const plateY=origin+(small?165:250),plateH=small?43:52;
    const waterY=origin+(small?237:338),waterH=small?48:60;
    const bracketX=small?330:438+i*550,top=chipY+chipH/2,bottom=waterY+waterH/2;
    const arrow=(from,to)=>path(`M${cx} ${from}V${to-10}`,'heat')
      +`<path d="M${cx-7} ${to-11}L${cx} ${to}L${cx+7} ${to-11}Z" fill="var(--heat)"/>`;
    b+=text(small?210:275+i*550,origin+(small?28:35),`${i===0?'Lower':'Higher'} resistance · ${resistance}°C/W`,small?22:27)
      +`<rect x="${cx-chipW/2}" y="${chipY}" width="${chipW}" height="${chipH}" rx="9" fill="var(--heatfill)" stroke="var(--${color})" stroke-width="3"/>`
      +text(cx,chipY+(small?42:57),`Chip · ${n(m.junctionC)}°C`,small?29:38,color)
      +arrow(chipY+chipH,plateY)
      +text(cx+(small?50:60),(chipY+chipH+plateY)/2+8,'400 W',small?21:25,'heat','start')
      +`<rect x="${cx-chipW/2}" y="${plateY}" width="${chipW}" height="${plateH}" rx="7" fill="var(--panel)" stroke="var(--tech)" stroke-width="3"/>`
      +text(cx,plateY+(small?29:35),'Cold plate',small?24:29)
      +arrow(plateY+plateH,waterY)
      +`<rect x="${cx-chipW/2}" y="${waterY}" width="${chipW}" height="${waterH}" rx="12" fill="var(--panel)" stroke="var(--tech)" stroke-width="3"/>`
      +text(cx,waterY+(small?32:40),`${fluidC}°C coolant`,small?25:31,'tech')
      +`<path d="M${bracketX-9} ${top}H${bracketX}V${bottom}H${bracketX-9}" fill="none" stroke="var(--${color})" stroke-width="2"/>`
      +text(bracketX+(small?7:12),(top+bottom)/2-12,'ΔT',small?21:24,color,'start')
      +text(bracketX+(small?7:12),(top+bottom)/2+19,`${n(m.junctionC-fluidC)}°C`,small?24:29,color,'start');
  }
  if(small){
    b+=text(w/2,636,`Chip limit: ${limitC}°C`,23)
      +text(w/2,674,'ΔT = T<tspan baseline-shift="sub" font-size="65%">chip</tspan> − T<tspan baseline-shift="sub" font-size="65%">coolant</tspan>',23)
      +text(w/2,706,'ΔT = 400 W × thermal resistance',22);
  }else{
    b+=text(w/2,441,`Chip limit: ${limitC}°C`,26)
      +text(w/2,486,'ΔT = T<tspan baseline-shift="sub" font-size="65%">chip</tspan> − T<tspan baseline-shift="sub" font-size="65%">coolant</tspan> = 400 W × thermal resistance',29);
  }
  return b;
}

function hydraulics(_state,small){
  const w=small?420:1100,left=small?65:110,right=small?385:740,top=small?205:145,bottom=small?530:410;
  const x=q=>left+q/3.2*(right-left),y=p=>bottom-p/200*(bottom-top);
  let b=text(w/2,small?30:28,'Fixed pump speed',small?22:25)
    +text(left,top-26,'Pressure difference (kPa)',small?21:25,'ink','start')
    +path(`M${left} ${top}V${bottom}H${right}`,'muted');
  const curves=[
    ['pump','Pump','tech',q=>160-10*q*q,false],
    ['circuit','Circuit','facility',q=>30*q*q,false],
    ['restricted','Higher resistance','fault',q=>70*q*q,true]
  ];
  curves.forEach(([id,label,color,f,dashed],i)=>{
    const lx=small?45:130+i*320,ly=small?72+i*34:67;
    const dash=dashed?' stroke-dasharray="9 6"':'';
    b+=`<path d="M${lx} ${ly-7}h28" stroke="var(--${color})" stroke-width="4"${dash}/>`+text(lx+39,ly,label,small?21:25,'ink','start');
    const pts=[];for(let step=0;step<=160;step++){const q=step/50,p=f(q);if(p>=0&&p<=200)pts.push(`${x(q)},${y(p)}`);}
    b+=`<polyline data-curve="${id}" points="${pts.join(' ')}" fill="none" stroke="var(--${color})" stroke-width="5"${dash}/>`;
  });
  for(const p of [0,100,200])b+=text(left-12,y(p)+7,p,small?19:23,'muted','end');
  for(const q of [0,1,2,3])b+=text(x(q),bottom+30,q,small?22:25,'muted');
  b+=text((left+right)/2,bottom+68,'Flow (L/s)',small?25:29);
  const points=[['A','Normal circuit',30,'facility'],['B','Higher resistance',70,'fault']];
  points.forEach(([id,label,resistance,color],i)=>{
    const m=hydraulicPoint({resistance}),px=x(m.flowLs),py=y(m.pressureKPa);
    b+=`<path d="M${px} ${py}V${bottom}" fill="none" stroke="var(--${color})" stroke-width="2" stroke-dasharray="4 6"/>`
      +`<circle data-operating-point="${id}" cx="${px}" cy="${py}" r="9" fill="var(--panel)" stroke="var(--${color})" stroke-width="4"/>`
      +text(px+(i?-21:21),py+(i?-15:30),id,small?23:26,color);
    const values=`${n(m.flowLs,2)} L/s · ${n(m.pressureKPa)} kPa`;
    if(small){
      b+=text(44,649+i*46,id,25,color,'start')+text(85,649+i*46,values,26,'ink','start');
    }else{
      b+=text(930,231+i*110,`${id} · ${label}`,25,color)+text(930,271+i*110,values,28);
    }
  });
  return b;
}
function branches(state,small){const m=parallelBranches(state.branch==='restricted'),w=small?420:1100;let b=text(w/2,40,'35°C supply · 42 kW in each branch',small?23:28);for(let i=0;i<2;i++){const x=small?20:35+i*550,y=small?80+i*230:120,cw=small?380:500;b+=card(x,y,cw,`${m.flows[i]} L/s`,`${n(m.returns[i])}°C return`,i===0?'Branch A':'Branch B',m.returns[i]>50?'fault':'tech');}return b+text(w/2,small?625:405,`Total 2 L/s · mixed return ${n(m.mixedReturnC)}°C`,small?25:33)+text(w/2,small?680:465,'Water · 1 kg/L · cp = 4.2 kJ/(kg·K)',small?21:25);}
function interfaces(small){const w=small?420:1100;let b='';const names=['Cold plate','Hoses + connectors','CDU'];for(let i=0;i<3;i++){const x=small?40:25+i*370,y=small?50+i*175:90,cw=small?340:320;b+=box(x,y,cw,110)+text(x+cw/2,y+62,names[i],28)+(i<2?text(small?210:x+345,small?y+146:y+66,small?'↓':'→',37,'tech'):'');}const ys=small?[607,647,687]:[290,350,410];['Fluid + materials','Pressure + cleanliness','Leak detection + isolation'].forEach((v,i)=>b+=text(w/2,ys[i],v,small?26:34));return b;}
function coolingResponse(small){
 const w=small?420:1100,parts=[['Cooling fault','600 kW remains'],['Power reduction','Affected racks'],['Measured response','500 kW into coolant']];
 let b='';
 parts.forEach(([title,detail],i)=>{
  const x=small?30:25+i*370,y=small?15+i*126:25,bw=small?360:310;
  b+=box(x,y,bw,95)+text(x+bw/2,y+35,title,small?24:26)+text(x+bw/2,y+72,detail,small?23:25,i===0?'fault':'tech');
  if(i<2)b+=text(small?210:x+bw+29,small?y+119:y+61,small?'↓':'→',30,'tech');
 });
 const left=small?75:190,right=w-(small?35:65),top=small?440:220,bottom=small?640:415;
 const y=kw=>bottom-kw/1000*(bottom-top),limit=y(600);
 b+=text(w/2,top-30,'Measured heat entering coolant',small?24:28)+path(`M${left} ${top}V${bottom}H${right}`,'muted');
 b+=`<path d="M${left} ${limit}H${right}" fill="none" stroke="var(--facility)" stroke-width="2" stroke-dasharray="7 5"/>`;
 b+=text(left-10,top+7,'1,000',19,'muted','end')+text(left-10,limit+7,'600',19,'facility','end')+text(left-10,bottom+7,'0',19,'muted','end');
 b+=path(`M${left} ${top}H${left+(right-left)*.24}L${left+(right-left)*.56} ${y(500)}H${right}`,'heat');
 b+=text(right,limit-10,'Cooling capacity',small?19:23,'facility','end')+text(right,y(500)+28,'500 kW',small?22:27,'heat','end');
 return b+text(left,top-10,'kW',18,'muted','end')+text(right,bottom+35,'Time →',21,'muted','end');
}
function retrofit(_state,small){
  const w=small?420:1100,cx=w/2,nodeY=190,nodeH=118;
  const coldX=small?107.5:270,airX=small?312.5:825,nodeW=small?185:400;
  const optionY=small?455:435,optionW=small?185:245,roomX=small?107.5:690,doorX=small?312.5:965;
  const arrow=(x,y,color)=>`<path d="M${x-7} ${y-12}L${x} ${y}L${x+7} ${y-12}Z" fill="var(--${color})"/>`;
  let b=box(cx-110,20,220,105)+text(cx,55,'Rack heat',25)+text(cx,105,'100 kW',40,'heat');
  for(const [mid,label,kw,color] of [[coldX,'Cold plates',85,'tech'],[airX,'Residual air',15,'heat']]){
    b+=path(`M${cx} 125V155H${mid}V${nodeY-12}`,color)+arrow(mid,nodeY,color)
      +box(mid-nodeW/2,nodeY,nodeW,nodeH)+text(mid,nodeY+36,label,small?24:29)
      +text(mid,nodeY+91,`${kw} kW`,small?37:45,color);
  }
  b+=path(`M${coldX} ${nodeY+nodeH}V${small?360:500}`,'tech')+arrow(coldX,small?372:512,'tech')
    +text(coldX,small?407:553,'To liquid',small?25:31,'tech');
  const splitY=small?423:383;
  b+=path(`M${airX} ${nodeY+nodeH}V${splitY}M${roomX} ${optionY-12}V${splitY}H${doorX}V${optionY-12}`,'heat')
    +arrow(roomX,optionY,'heat')+arrow(doorX,optionY,'heat')
    +`<rect x="${(roomX+doorX)/2-24}" y="${splitY-14}" width="48" height="28" rx="6" fill="var(--panel)"/>`
    +text((roomX+doorX)/2,splitY+8,'OR',20);
  const roomLeft=roomX-optionW/2,doorLeft=doorX-optionW/2,barW=optionW-28;
  b+=box(roomLeft,optionY,optionW,205)+text(roomX,optionY+34,'Room cooling',small?23:28)
    +text(roomX,optionY+80,'15 kW',small?33:38,'heat')
    +`<rect x="${roomLeft+14}" y="${optionY+99}" width="${barW}" height="24" rx="5" fill="var(--panel)" stroke="var(--line)"/>`
    +`<rect x="${roomLeft+14}" y="${optionY+99}" width="${barW*.75}" height="24" rx="5" fill="var(--heat)" opacity=".4"/>`
    +text(roomX,optionY+154,'20 kW allowance',small?21:25)
    +text(roomX,optionY+187,'5 kW spare',small?21:25,'facility')
    +box(doorLeft,optionY,optionW,205)+text(doorX,optionY+34,'RDHX',small?25:28)
    +`<rect x="${doorX-43}" y="${optionY+55}" width="86" height="57" rx="5" fill="var(--panel)" stroke="var(--tech)" stroke-width="2"/>`
    +path(`M${doorX-28} ${optionY+64}V${optionY+102}H${doorX-10}V${optionY+64}H${doorX+10}V${optionY+102}H${doorX+28}V${optionY+64}`,'tech')
    +path(`M${doorX} ${optionY+112}V${optionY+130}`,'tech')+arrow(doorX,optionY+142,'tech')
    +text(doorX,optionY+174,'15 kW → liquid',small?21:26,'tech');
  return b;
}
export function renderCapture(id,state,compact){switch(id){case'local-heat-flux':return flux(compact);case'device-temperature':return temperature(state,compact);case'pump-operating-point':return hydraulics(state,compact);case'branch-flow':return branches(state,compact);case'coolant-interfaces':return interfaces(compact);case'cooling-response':return coolingResponse(compact);case'cooling-retrofit':return retrofit(state,compact);default:throw new Error(`Unknown capture scene ${id}`);}}
