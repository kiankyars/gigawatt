const C={text:'var(--text)',muted:'var(--muted)',line:'var(--line)',panel:'var(--panel)',surface:'var(--surface)',power:'var(--power)',heat:'var(--heat)',data:'var(--data)'};
const esc=v=>String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const text=(x,y,value,size=22,color=C.text,anchor='start',extra='')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}" ${extra}>${esc(value)}</text>`;
const lines=(x,y,values,size=22,color=C.text,anchor='start',gap=size*1.3)=>values.map((value,i)=>text(x,y+i*gap,value,size,color,anchor)).join('');
const rect=(x,y,w,h,fill=C.panel,stroke=C.line,rx=10,extra='')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}" stroke="${stroke}" ${extra}/>`;
const line=(x,y,xx,yy,color=C.line,width=2,extra='')=>`<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${color}" stroke-width="${width}" ${extra}/>`;
const arrow=(x,y,xx,yy,color=C.power)=>line(x,y,xx,yy,color,3)+`<path d="M-8 -6L0 0L-8 6" transform="translate(${xx} ${yy}) rotate(${Math.atan2(yy-y,xx-x)*180/Math.PI})" fill="none" stroke="${color}" stroke-width="3"/>`;
const number=v=>v.toLocaleString('en-US',{maximumFractionDigits:0});
const meta=(id,title,description,markup,attrs='')=>({markup:`<g data-procurement-scene="${id}" ${attrs}><title>${esc(title)}</title>${markup}</g>`,description});

export function transportBudget({powerMW=200,voltageKV=34.5,circuits=1}={}){
 if(!Number.isFinite(powerMW)||powerMW<0||!Number.isFinite(voltageKV)||voltageKV<=0||!Number.isInteger(circuits)||circuits<1)throw new RangeError('Use finite power ≥ 0, voltage > 0 and an integer circuit count ≥ 1.');
 const powerPerCircuitMW=powerMW/circuits;
 const lineCurrentA=powerPerCircuitMW*1000/(Math.sqrt(3)*voltageKV);
 return Object.freeze({powerMW,voltageKV,circuits,powerPerCircuitMW,lineCurrentA});
}
function transformer(x,y,color=C.power){
 return `<circle cx="${x-10}" cy="${y}" r="20" fill="var(--paper)" stroke="${color}" stroke-width="3"/><circle cx="${x+10}" cy="${y}" r="20" fill="none" stroke="${color}" stroke-width="3"/>`;
}
function generator(x,y){return `<circle cx="${x}" cy="${y}" r="25" fill="var(--paper)" stroke="${C.power}" stroke-width="3"/>`+text(x,y+8,'G',24,C.power,'middle');}
function campus(x,y){return rect(x-29,y-25,58,50,C.surface,C.power,2)+[-12,0,12].map(d=>line(x-18,y+d,x+18,y+d,C.power,3)).join('');}
function route(s,m){
 let out='';
 if(m){
  out+=text(95,35,'HV transport',21,C.heat,'middle')+text(292,35,'Local MV',21,C.power,'middle');
  for(const x of [95,292])out+=arrow(x,123,x,557,C.power)+generator(x,92)+campus(x,590);
  out+=transformer(95,190,C.heat)+text(130,197,'Step up',16,C.heat)
   +text(130,292,'HV',17,C.muted)+transformer(95,352,C.heat)+lines(130,346,['Step','down'],16,C.heat);
  for(const x of [95,292])out+=transformer(x,474)+rect(x-58,507,116,24,'var(--paper)','none',0)+text(x,525,'Local LV supply',15,C.power,'middle');
  out+=rect(241,292,102,27,'var(--paper)','none',0)+text(292,312,'MV feeder',18,C.power,'middle')+text(195,655,'Conceptual AC routes · not an as-built one-line',13,C.muted,'middle');
 }else{
  const row=(y,hv)=>{
   let a=text(40,y-84,hv?'HIGH-VOLTAGE TRANSPORT':'LOCAL MEDIUM-VOLTAGE DELIVERY',19,hv?C.heat:C.power)
    +arrow(128,y,1005,y)+generator(95,y)+text(95,y+59,'Gas plant',22,C.text,'middle')
    +transformer(850,y)+text(850,y+59,'Local LV supply',22,C.text,'middle')
    +campus(1040,y)+text(1040,y+59,'Campus',22,C.text,'middle');
   if(hv)a+=transformer(305,y,C.heat)+text(305,y+59,'Step up',22,C.heat,'middle')
    +transformer(650,y,C.heat)+text(650,y+59,'Step down',22,C.heat,'middle')+text(477,y-27,'HV feeder',23,C.muted,'middle');
   else a+=text(477,y-27,'MV feeder',25,C.power,'middle');
   return a;
  };
  out+=row(155,true)+row(397,false)+text(560,285,'Large-transformer delivery dependencies',22,C.heat,'middle')
   +text(560,529,'Conceptual AC routes · SemiAnalysis’s Southaven procurement account, August 2026',17,C.muted,'middle');
 }
 return meta('procurement-route','Two AC routes from local generation to the campus','Both conceptual AC paths remain visible. The high-voltage path adds large step-up and step-down transformer stages. Local medium-voltage delivery bypasses those stages, retaining the local low-voltage supply. SemiAnalysis reports this procurement rationale for Southaven; the permit maps do not establish these exact electrical routes. Switching and protection are outside this functional sketch.',out);
}
function current(s,m){
 const mv=transportBudget(),hv=transportBudget({voltageKV:161});
 let out=text(m?195:40,m?42:42,'200 MW from plant to campus',m?24:29,C.power,m?'middle':'start');
 out+=text(m?195:1080,m?76:42,'Illustrative · three-phase AC · PF = 1',m?15:19,C.muted,m?'middle':'end');
 [mv,hv].forEach((a,i)=>{
  const y=(m?153:148)+i*(m?185:140),x=m?32:278,w=m?317:570,bar=w*a.lineCurrentA/mv.lineCurrentA;
  out+=text(m?32:45,y+(m?0:34),`${a.voltageKV} kV`,m?27:34,C.text)
   +rect(x,y+(m?24:0),bar,m?48:59,i===0?C.heat:C.power,i===0?C.heat:C.power,0)
   +text(m?32:1080,y+(m?111:39),`${number(a.lineCurrentA)} A per line`,m?24:31,i===0?C.heat:C.power,m?'start':'end');
 });
 out+=text(m?195:560,m?553:435,'I = P / (√3 × VLL × PF)',m?24:35,C.text,'middle');
 out+=text(m?195:560,m?601:492,'4.67× current at the lower voltage',m?20:26,C.heat,'middle');
 out+=text(m?195:560,m?651:531,'Extra current can require more parallel feeders.',m?15:19,C.muted,'middle');
 return meta('transport-current','The electrical consequence of avoiding the high-voltage transport stage','The previous procurement choice concerns campus AC transport, not 800 V DC or rack power density. Hold a hypothetical receiving boundary at 200 MW. At 34.5 kV line-to-line, current is 3,347 amperes per line; at 161 kV it is 717 amperes. The 4.67-fold current ratio can require more parallel feeders or conductor area. These are comparison inputs, not Southaven specifications or measured losses.',out,`data-power-mw="200" data-mv-current-a="${mv.lineCurrentA}" data-hv-current-a="${hv.lineCurrentA}"`);
}
export function renderProcurement(id,state={},compact=false){
 if(id==='procurement-route')return route(state,compact);
 if(id==='transport-current')return current(state,compact);
 return null;
}
