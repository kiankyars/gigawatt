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
function transformer(x,y,size,color=C.power){
 return `<circle cx="${x-size*.22}" cy="${y}" r="${size*.31}" fill="none" stroke="${color}" stroke-width="2.5"/><circle cx="${x+size*.22}" cy="${y}" r="${size*.31}" fill="none" stroke="${color}" stroke-width="2.5"/>`;
}
function equipment(x,y,w,h,label,kind,color=C.power,small=false){
 let out=rect(x,y,w,h,C.surface,color);
 if(kind==='generator')out+=`<circle cx="${x+w/2}" cy="${y+31}" r="19" fill="none" stroke="${color}" stroke-width="2.5"/>`+text(x+w/2,y+38,'G',23,color,'middle');
 if(kind==='transformer')out+=transformer(x+w/2,y+31,54,color);
 if(kind==='load')for(let i=0;i<3;i++)out+=rect(x+w/2-26,y+13+i*13,52,10,C.panel,color,2);
 out+=lines(x+w/2,y+(small&&h<100?64:72),Array.isArray(label)?label:[label],small?16:20,C.text,'middle',small?20:24);
 return out;
}
function route(s,m){
 const mv=s.route==='mv';let out='';
 if(m){
  out+=text(24,35,mv?'Local medium-voltage path':'High-voltage transport path',21,C.power);
  const x=25,w=143,h=101;
  out+=equipment(x,67,w,h,'Generation','generator',C.power,true);
  if(mv){
   out+=line(96,173,96,333,C.power,4)+text(118,230,'MV delivery',20,C.power)+text(118,259,'No large HV',16,C.muted)+text(118,281,'transformer stages',16,C.muted);
   out+=equipment(x,338,w,h,['Step down','to low voltage'],'transformer',C.power,true)+arrow(96,444,96,473)+equipment(x,480,w,100,'Load','load',C.power,true);
   out+=text(190,386,'Retained',17,C.power);
  }else{
   out=text(24,35,'High-voltage transport path',21,C.power);
   const block=(y,label,kind,color=C.power)=>equipment(25,y,143,93,label,kind,color,true);
   out+=block(54,'Generation','generator')+arrow(96,153,96,169)+block(177,'Step up','transformer',C.heat);
   out+=line(168,223,245,223,C.power,3)+line(245,223,245,349,C.power,3)+arrow(245,349,178,349)+lines(268,269,['HV','route'],19,C.power);
   out+=block(306,'Step down','transformer',C.heat)+arrow(96,405,96,422)+block(429,['Load-side','LV supply'],'transformer')+arrow(96,528,96,545)+block(552,'Load','load');
   out+=lines(190,452,['Low-voltage','supply remains'],16,C.muted);

  }
  if(mv)out+=lines(25,625,['Conceptual paths · SemiAnalysis','Southaven / MiniHard, Aug 2026'],15,C.muted);
 }else{
  out+=text(32,36,'Conceptual paths · reported procurement rationale',18,C.muted)+text(1088,36,'SemiAnalysis · Aug 2026',18,C.muted,'end');
  const draw=(isMV,y)=>{
   const active=isMV===mv,stroke=active?C.power:C.line;
   let row=rect(24,y-19,1072,189,active?C.panel:C.surface,stroke,12,active?'stroke-width="2"':'');
   row+=text(43,y+7,isMV?'LOCAL MV DELIVERY':'HV TRANSPORT',16,active?C.power:C.muted);
   row+=equipment(47,y+24,132,112,'Generation','generator',stroke);
   if(isMV){
    row+=arrow(189,y+78,722,y+78,stroke)+text(455,y+57,'MV route',24,active?C.power:C.muted,'middle');
    row+=text(455,y+117,'Large HV transformer stages bypassed',20,C.muted,'middle');
    row+=equipment(734,y+24,157,112,['Step down','to low voltage'],'transformer',stroke)+arrow(902,y+78,929,y+78,stroke)+equipment(940,y+24,132,112,'Load','load',stroke);
   }else{
    row+=arrow(189,y+78,222,y+78,stroke)+equipment(234,y+24,149,112,'Step up','transformer',active?C.heat:C.line)+arrow(396,y+78,550,y+78,stroke)+text(473,y+56,'HV route',23,active?C.power:C.muted,'middle');
    row+=equipment(563,y+24,150,112,'Step down','transformer',active?C.heat:C.line)+arrow(725,y+78,746,y+78,stroke)+equipment(758,y+24,150,112,['Load-side','LV supply'],'transformer',stroke)+arrow(919,y+78,931,y+78,stroke)+equipment(941,y+24,131,112,'Load','load',stroke);
   }
   return row;
  };
  out+=draw(false,90)+draw(true,326);
  out+=text(640,283,'Large-transformer delivery dependencies',18,C.heat,'middle');
  out+=line(308,263,638,263,C.heat,2)+line(308,253,308,263,C.heat,2)+line(638,253,638,263,C.heat,2);
 }
 return meta('procurement-route','Conceptual high-voltage and medium-voltage delivery paths',`Selected ${mv?'local MV':'HV transport'} path. SemiAnalysis reports imported power modules and medium-voltage delivery to low-voltage transformers in the Southaven/MiniHard procurement discussion. These original functional paths are not an as-built site drawing. Bypassing large high-voltage transformer stages does not remove the load-side low-voltage supply or the need for switching and protection.`,out,`data-route="${mv?'mv':'hv'}"`);
}
function current(s,m){
 const v=Number(s.voltage??34.5),selected=transportBudget({voltageKV:v}),mv=transportBudget(),hv=transportBudget({voltageKV:161});let out='';
 if(m){
  out+=text(195,56,'200 MW received',30,C.power,'middle')+text(195,89,'Balanced three-phase · PF = 1',17,C.muted,'middle');
  [mv,hv].forEach((a,i)=>{
   const y=143+i*174,active=a.voltageKV===v,w=300*a.lineCurrentA/mv.lineCurrentA;
   out+=text(35,y,`${a.voltageKV} kV`,27,active?C.power:C.muted)+text(350,y,'line-to-line RMS',15,C.muted,'end');
   out+=rect(35,y+23,300,45,C.surface,C.line,0)+rect(35,y+23,w,45,active?C.power:C.muted,active?C.power:C.muted,0);
   out+=text(35,y+107,`${number(a.lineCurrentA)} A / phase conductor`,24,active?C.power:C.muted);
  });
  out+=text(195,525,'I = P / (√3 × VLL × PF)',25,C.text,'middle');
  out+=text(195,573,`200,000 kW / (√3 × ${v} kV)`,21,C.muted,'middle')+text(195,620,`= ${number(selected.lineCurrentA)} A`,34,C.power,'middle');
 }else{
  out+=text(38,46,'200 MW received',29,C.power)+text(1080,46,'Balanced three-phase · PF = 1',21,C.muted,'end');
  out+=text(280,109,'RMS current in each phase conductor',21,C.muted);
  [mv,hv].forEach((a,i)=>{
   const y=148+i*126,active=a.voltageKV===v,w=600*a.lineCurrentA/mv.lineCurrentA;
   out+=text(48,y+41,`${a.voltageKV} kV`,34,active?C.power:C.muted)+text(48,y+72,'line-to-line RMS',17,C.muted);
   out+=rect(280,y,600,59,C.surface,C.line,0)+rect(280,y,w,59,active?C.power:C.muted,active?C.power:C.muted,0);
   out+=text(1080,y+40,`${number(a.lineCurrentA)} A`,38,active?C.power:C.muted,'end');
  });
  out+=text(560,432,'I = P / (√3 × VLL × PF)',38,C.text,'middle');
  out+=text(560,488,`200,000 kW / (√3 × ${v} kV × 1) = ${number(selected.lineCurrentA)} A`,29,C.power,'middle');
 }
 return meta('transport-current','Line current at two transport voltages',`Original hypothetical comparison, not xAI design values: 200 MW received at balanced three-phase power factor one. At 34.5 kV line-to-line RMS the RMS line current is ${mv.lineCurrentA} amperes. At 161 kV it is ${hv.lineCurrentA} amperes. The selected value is ${v} kV. Neither value is a sum of the three phase-current magnitudes.`,out,`data-voltage-kv="${v}" data-line-current-a="${selected.lineCurrentA}" data-power-mw="200"`);
}
function parallel(s,m){
 const count=Number(s.circuits??1),a=transportBudget({circuits:count});let out='';
 if(m){
  out+=text(195,43,'200 MW · 34.5 kV · PF = 1',23,C.power,'middle');
  out+=rect(27,84,336,63,C.panel,C.power)+text(195,125,'Source bus',24,C.text,'middle');
  const xs=count===1?[195]:Array.from({length:count},(_,i)=>57+i*276/(count-1)),top=192,bottom=398;
  xs.forEach((x,i)=>{
   out+=line(x,147,x,top-10,C.power,3)+line(x-6,top,x-6,bottom,C.power,2)+line(x,top,x,bottom,C.power,2)+line(x+6,top,x+6,bottom,C.power,2)+line(x,bottom+10,x,441,C.power,3);
   out+=rect(x-25,260,50,47,C.surface,C.line,6)+text(x,290,`C${i+1}`,20,C.power,'middle');
  });
  out+=rect(27,441,336,64,C.panel,C.power)+text(195,482,'Receiving bus · 200 MW',23,C.text,'middle');
  out+=text(195,549,`${a.powerPerCircuitMW} MW per circuit`,26,C.text,'middle')+text(195,597,`${number(a.lineCurrentA)} A per phase conductor`,24,C.power,'middle');
  out+=text(195,643,'Each C is a complete three-phase circuit.',17,C.muted,'middle');
 }else{
  out+=text(40,42,'200 MW received · 34.5 kV line-to-line · PF = 1',25,C.power);
  out+=rect(45,116,160,276,C.surface,C.power)+lines(125,241,['Source','bus'],25,C.text,'middle');
  out+=rect(894,116,183,276,C.surface,C.power)+lines(985,235,['Receiving','bus'],25,C.text,'middle')+text(985,311,'200 MW',29,C.power,'middle');
  const ys=count===1?[254]:Array.from({length:count},(_,i)=>150+i*210/(count-1));
  ys.forEach((y,i)=>{
   out+=line(205,y,267,y,C.power,3)+line(823,y,894,y,C.power,3);
   [-6,0,6].forEach(d=>out+=line(267,y+d,823,y+d,C.power,2));
   out+=rect(369,y-22,353,44,C.surface,C.line,7)+text(545,y+7,`Circuit ${i+1} · ${a.powerPerCircuitMW} MW · ${number(a.lineCurrentA)} A / line`,21,C.power,'middle');
  });
  out+=text(560,466,'Each path is a complete three-phase circuit.',24,C.text,'middle')+text(560,510,`I per line = 200,000 / (${count} × √3 × 34.5) = ${number(a.lineCurrentA)} A`,26,C.power,'middle');
 }
 return meta('parallel-circuits','Share the transfer among equally loaded three-phase circuits',`${count} equally loaded parallel three-phase circuit${count===1?'':'s'} deliver a total 200 MW at 34.5 kV line-to-line RMS and power factor one. Each circuit carries ${a.powerPerCircuitMW} MW and each of its phase conductors carries ${a.lineCurrentA} A RMS. Extra circuits add equipment, conductors and protection interfaces. This functional diagram specifies neither wiring nor redundant capacity and makes no total loss or cost comparison.`,out,`data-circuits="${count}" data-power-per-circuit-mw="${a.powerPerCircuitMW}" data-line-current-a="${a.lineCurrentA}" data-power-mw="200"`);
}
function decision(s,m){
 let out='';
 if(!s.decisionReveal){
  if(m){
   out+=text(27,91,'The local MV route',26,C.power);
   out+=text(27,174,'What can it avoid?',28,C.text)+lines(27,215,['Name one delivery dependency.'],20,C.muted)+line(27,271,363,271,C.line,2,'stroke-dasharray="6 6"');
   out+=text(27,374,'What must still work?',28,C.text)+lines(27,415,['Name one electrical requirement.'],20,C.muted)+line(27,471,363,471,C.line,2,'stroke-dasharray="6 6"');
  }else{
   out+=text(47,77,'The local MV route',30,C.power);
   out+=text(47,211,'What can it avoid?',36,C.text)+text(47,261,'Name one delivery dependency.',25,C.muted)+line(47,321,515,321,C.line,2,'stroke-dasharray="6 6"');
   out+=text(613,211,'What must still work?',36,C.text)+text(613,261,'Name one electrical requirement.',25,C.muted)+line(613,321,1080,321,C.line,2,'stroke-dasharray="6 6"');
  }
  return meta('procurement-decision','Predict the procurement tradeoff','Before revealing, name one delivery dependency that local medium-voltage delivery can avoid, and one electrical requirement the alternative must still satisfy.',out,'data-decision-revealed="false"');
 }

 const rows=[['Large transformers','Equipment delivery date',C.heat],['MV delivery','Circuit and conductor capacity',C.power],['Complete route','Switching, protection and commissioning',C.data]];
 if(m){
  rows.forEach(([a,b,c],i)=>{
   const y=65+i*168;
   out+=text(29,y,a,27,c)+arrow(29,y+28,64,y+28,c)+lines(82,y+34,b==='Switching, protection and commissioning'?['Switching, protection','and commissioning']:b==='Circuit and conductor capacity'?['Circuit and','conductor capacity']:[b],22,C.text);
   out+=line(29,y+109,361,y+109);
  });
  out+=lines(195,605,['Compare the date when the','whole route can serve the load.'],23,C.power,'middle');
 }else{
  rows.forEach(([a,b,c],i)=>{
   const y=94+i*128;
   out+=text(62,y,a,31,c)+arrow(370,y-9,482,y-9,c)+text(515,y,b,29,C.text)+line(62,y+42,1060,y+42);
  });
  out+=text(560,488,'Compare the date when the whole route can serve the load.',31,C.power,'middle');
 }
 return meta('procurement-decision','A procurement workaround changes the complete delivery decision','Removing a large-transformer procurement dependency can bring an alternative route forward. Medium-voltage delivery still needs adequate circuits and conductors, switching, protection and commissioning. Compare when a complete engineered route can actually serve the required load; an earlier equipment shipment is not yet usable campus power.',out,'data-decision-revealed="true"');
}
export function renderProcurement(id,state={},compact=false){
 if(id==='procurement-route')return route(state,compact);
 if(id==='transport-current')return current(state,compact);
 if(id==='parallel-circuits')return parallel(state,compact);
 if(id==='procurement-decision')return decision(state,compact);
 return null;
}
