import { renderGeneration, generationScenes } from './siting-generation.js';
import { readiness, matching, busBalance, islandBudget } from './siting-model.js';
import { renderProcurement } from './siting-procurement.js';
const C={ink:'var(--text)',muted:'var(--muted)',line:'var(--line)',face:'var(--surface)',panel:'var(--panel)',power:'var(--power)',heat:'var(--heat)',data:'var(--data)',paper:'var(--paper)'};
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const t=(x,y,v,size=24,color=C.ink,anchor='start')=>`<text x="${x}" y="${y}" font-size="${size}" fill="${color}" text-anchor="${anchor}">${esc(v)}</text>`;
const rect=(x,y,w,h,fill=C.face,stroke=C.line)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="${fill}" stroke="${stroke}" stroke-width="2"/>`;
const line=(x,y,x2,y2,color=C.line,width=3,dash='')=>`<path d="M${x} ${y}L${x2} ${y2}" fill="none" stroke="${color}" stroke-width="${width}" ${dash?'stroke-dasharray="'+dash+'"':''}/>`;
const arrow=(x,y,x2,y2,c=C.power,dash='')=>{const a=Math.atan2(y2-y,x2-x),d=10;return line(x,y,x2,y2,c,4,dash)+`<path d="M${x2-d*Math.cos(a-.45)} ${y2-d*Math.sin(a-.45)}L${x2} ${y2}L${x2-d*Math.cos(a+.45)} ${y2-d*Math.sin(a+.45)}" fill="none" stroke="${c}" stroke-width="3"/>`;};
function box(x,y,w,h,label,sub='',color=C.power){return rect(x,y,w,h,C.face,color)+t(x+w/2,y+h/2+(sub?-6:8),label,w<220?21:26,C.ink,'middle')+(sub?t(x+w/2,y+h/2+24,sub,w<220?16:19,C.muted,'middle'):'');}
function scope(m,label){
 if(!m||label.length<53)return t(m?195:560,m?653:518,label,m?13:16,C.muted,'middle');
 const words=label.split(' '),rows=[''];for(const word of words){const i=rows.length-1;if((rows[i]+' '+word).length>51)rows.push(word);else rows[i]+=(rows[i]?' ':'')+word;}
 return rows.map((row,i)=>t(195,637+i*19,row,13,C.muted,'middle')).join('');
}
const result=(markup,description,attrs='')=>({markup:`<g ${attrs}>${markup}</g>`,description});

function siteReady(s,m){
 const a=readiness(s.site),x=m?36:150,w=m?310:830,y=m?165:152,step=m?85:75,labels=['Power','Building','Cooling','Fiber'];let o=t(m?195:560,m?85:73,`Site ${s.site}`,m?35:43,C.ink,'middle');
 const scale=w/24;
 labels.forEach((label,i)=>{const yy=y+i*step;o+=t(x,yy-12,label,m?18:20,C.muted)+rect(x,yy,24*scale,24,C.panel,C.panel)+rect(x,yy,a.dates[i]*scale,24,C.power,C.power)+t(x+a.dates[i]*scale-8,yy+19,`${a.dates[i]}`,16,C.paper,'end');});
 o+=t(m?195:560,m?560:471,s.readinessReveal?`Complete service: month ${a.readyMonth}`:'Predict the first usable month.',m?24:31,s.readinessReveal?C.power:C.ink,'middle');
 o+=scope(m,'Supplied accepted-readiness dates · months from the same start');
 return result(o,`Site ${s.site}: ${labels.map((v,i)=>v+' month '+a.dates[i]).join(', ')}. ${s.readinessReveal?`All required services ready at month ${a.readyMonth}; ${a.limiting.join(' and ')} binds.`:'Predict before revealing the usable month.'}`,`data-ready-month="${a.readyMonth}"`);
}
function parcel(s,m){
 const routes=[['power','Substation','Capacity + connection'],['fuel','Gas network','Pressure + capacity'],['fiber','Fiber route','Connectivity + rights']];let o='';
 if(m){o+=rect(40,340,310,235,C.panel)+t(195,372,'PROPOSED PARCEL',16,C.muted,'middle')+box(86,414,218,102,'Data center','Phase to be supplied');routes.forEach(([k,a,b],i)=>{const yy=38+i*91,c=s.corridor===k?C.power:C.line;o+=box(40,yy,242,67,a,'',c)+arrow(293,yy+34,330,yy+34,c);if(s.corridor===k)o+=line(330,yy+34,330,399,c,4)+arrow(330,399,280,414,c);});}
 else {o+=rect(608,72,430,375,C.panel)+t(823,112,'PROPOSED PARCEL',18,C.muted,'middle')+box(692,212,270,119,'Data center','Phase to be supplied');routes.forEach(([k,a,b],i)=>{const yy=65+i*143,c=s.corridor===k?C.power:C.line;o+=box(60,yy,280,88,a,'',c)+line(352,yy+44,650,yy+44,c,3);if(s.corridor===k)o+=line(650,yy+44,650,271,c,4)+arrow(650,271,685,271,c)+t(490,yy+20,'Route + rights',19,c,'middle');});}
 const selected=routes.find(r=>r[0]===s.corridor);o+=t(m?195:560,m?608:483,selected[2],m?23:29,C.power,'middle');
 return result(o,`${selected[1]} connects through a required corridor. Verify ${selected[2].toLowerCase()}, plus rights to connect and cross the intervening route. Other site feasibility requirements remain.`);
}
function chain(m,items){let o='';const w=m?310:240,h=m?82:115;items.forEach(([a,b],i)=>{const x=m?40:30+i*278,y=m?50+i*140:175;o+=box(x,y,w,h,a,b);if(i<items.length-1)o+=m?arrow(195,y+h+6,195,y+128):arrow(x+w+6,y+57,x+267,y+57);});return o;}
function connection(m){return result(chain(m,[['Load request','MW + behavior + site'],['Network studies','Shared constraints'],['Required works','Equipment + construction'],['Accepted service','Defined operating scope']])+scope(m,'Illustrative dependencies · jurisdiction-specific process'), 'A load request leads to shared-network studies, required equipment and construction, then accepted service. The chain is conceptual; names, order and timing vary by jurisdiction.');}
function abilene(m){
 const items=[['Original campus','First two buildings','2 × 100 MW','Energized'],['Original campus','Six further buildings','End of 2026','Expected'],['Adjacent Microsoft','Separate development','Mid-2027','Initial energization targeted']];let o='';
 items.forEach(([a,b,c,d],i)=>{const x=m?30:30+i*370,y=m?44+i*185:105,w=m?330:340,h=m?164:296;o+=rect(x,y,w,h)+t(x+20,y+31,a,18,C.muted)+t(x+20,y+65,b,m?22:24)+t(x+20,y+(m?105:154),c,m?30:39,i===0?C.power:C.data)+t(x+20,y+(m?140:237),d,m?16:18,C.muted);});
 o+=scope(m,'Crusoe · 27 March 2026 · milestones, not measured AI output');
 return result(o,'Crusoe reported two 100 MW buildings energized at the original Abilene campus, six further buildings expected by year-end 2026, and a separate adjacent Microsoft project targeting initial energization in mid-2027. These are dated statements.');
}
function contractPath(s,m){
 const up=s.grid==='connected';let o='';
 if(m){o+=box(75,45,240,91,'Off-site generator')+arrow(195,144,195,246)+box(75,255,240,90,'Shared grid')+arrow(195,353,195,461,up?C.power:C.line)+box(75,470,240,100,'Campus',up?'Grid path available':'Grid path unavailable',up?C.power:C.heat)+line(45,90,45,522,C.data,3,'9 7')+line(45,90,70,90,C.data,3,'9 7')+arrow(45,522,71,522,C.data,'9 7')+t(33,213,'PPA',17,C.data);if(!up)o+=t(195,421,'×',43,C.heat,'middle');}
 else{o+=box(40,180,260,115,'Off-site generator')+arrow(310,237,420,237)+box(430,180,260,115,'Shared grid')+arrow(700,237,810,237,up?C.power:C.line)+box(820,180,260,115,'Campus','',up?C.power:C.heat)+line(170,170,170,82,C.data,3,'9 7')+line(170,82,950,82,C.data,3,'9 7')+arrow(950,82,950,170,C.data,'9 7')+t(560,58,'Financial PPA · commercial relationship',22,C.data,'middle')+t(950,355,up?'Grid path available':'Grid path unavailable',23,up?C.power:C.heat,'middle');if(!up)o+=t(755,251,'×',44,C.heat,'middle');}
 return result(o+scope(m,'Solid: physical power path · dashed: contract'),`An off-site financial PPA links the generator and campus commercially. The physical path passes through the shared grid and is ${up?'available':'unavailable at the campus connection'}. A contract supplies no independent feeder.`);
}
function hourly(m){
 const x=m?48:120,y=m?140:95,w=m?300:890,h=m?215:255;let o=t(m?195:560,m?70:42,'20 MW × 12 h = 10 MW × 24 h',m?23:31,C.ink,'middle');
 o+=rect(x,y,w/2,h/2,C.data,C.data)+rect(x,y+h/2,w/2,h/2,C.panel,C.panel)+rect(x+w/2,y+h/2,w/2,h/2,C.heat,C.heat)+line(x,y+h/2,x+w,y+h/2,C.power,4);
 o+=t(x-10,y+6,'20',16,C.muted,'end')+t(x-10,y+h/2+6,'10',16,C.power,'end')+t(x-10,y+h+6,'0',16,C.muted,'end')+t(x,y-16,'MW',16,C.muted);
 [0,12,24].forEach((v,i)=>o+=t(x+i*w/2,y+h+29,`${v} h`,16,C.muted,i===0?'start':i===2?'end':'middle'));
 o+=`<path d="M${x} ${y}H${x+w/2}V${y+h}H${x+w}" fill="none" stroke="${C.data}" stroke-width="4"/>`;
 o+=t(x+w/4,y+h*.25+6,'+120 MWh',m?19:29,C.paper,'middle')+t(x+w*.75,y+h*.75+6,'−120 MWh',m?19:29,C.paper,'middle');
 const yy=m?444:420;o+=t(m?40:120,yy,'Generation: 20 MW, then 0',m?19:22,C.data)+t(m?40:620,m?481:yy,'Load: constant 10 MW',m?19:22,C.power)+scope(m,'Profile surplus and deficit · each profile totals 240 MWh');
 return result(o,'Both daily totals are 240 MWh. During the first 12 hours, generation exceeds load by 10 MW, a 120 MWh surplus. During the other 12 hours, load exceeds generation by 10 MW, a 120 MWh deficit. Colored areas are differences between profiles, not campus meter readings.');
}
function storage(s,m){
 const a=matching(s.storage),items=[['Charge energy','Captured surplus','120 MWh'],['Usable output','After round-trip loss',`${a.returnedMWh} MWh`],['Output capability','Required: 10 MW',`${a.outputMW} MW`]];let o='';
 items.forEach(([a,b,c],i)=>{const x=m?35:40+i*365,y=m?45+i*159:106,w=m?320:310;o+=rect(x,y,w,m?135:232)+t(x+20,y+31,a,19,C.muted)+t(x+20,y+(m?85:115),c,m?36:47,i===2&&s.storage==='power'?C.heat:C.power)+t(x+20,y+(m?113:177),b,m?16:19,C.muted);});
 const message=s.storage==='losses'?'12 MWh energy shortfall':s.storage==='power'?'8 MW unsupported load':'10 MW for the full 12 hours';
 o+=t(m?195:560,m?574:424,message,m?24:32,s.storage==='ideal'?C.power:C.heat,'middle');
 return result(o+scope(m,'Original storage assumptions · no outage reserve included'),`${a.returnedMWh} MWh returns from 120 MWh charging energy. Output limit is ${a.outputMW} MW. ${message}.`, `data-returned-mwh="${a.returnedMWh}" data-output-mw="${a.outputMW}"`);
}
function bus(s,m,kind){
 const island=kind==='island-boundary',supported=s.island==='supported';
 const g=kind==='import-contingency'?(s.generator==='running'?6:0):island?6:s.generation;
 const a=busBalance(g),grid=island?0:a.gridMW,storage=island&&supported?2:0;
 let o='';const y=m?255:215,x=m?195:560;
 if(m){o+=rect(23,160,344,410,C.panel)+t(195,190,'CUSTOMER SIDE',16,C.muted,'middle')+box(78,26,234,73,'Grid',island?'Disconnected':grid<0?'Proposed export':`${grid} MW import`);o+=line(195,106,195,255,island?C.line:C.power,4)+rect(169,118,52,32,C.face)+t(195,140,'M',18,C.ink,'middle')+t(250,141,'Meter',16,C.muted);if(island)o+=t(225,225,'×',28,C.heat);o+=line(59,y,330,y,C.power,5)+box(44,321,150,88,'Generator',`${g} MW net`,g?C.power:C.line)+arrow(119,312,119,y+5,g?C.power:C.line);o+=box(216,321,131,88,'Storage',`${storage} MW`,storage?C.power:C.line);o+=storage?arrow(281,314,281,y+5):line(281,314,281,y+5,C.line,3);o+=arrow(195,y+7,195,457)+box(80,466,230,79,'Site load','8 MW');}
 else{o+=rect(355,69,727,386,C.panel)+t(1060,100,'CUSTOMER SIDE',17,C.muted,'end')+box(30,177,218,105,'Grid',island?'Disconnected':grid<0?'Proposed export':`${grid} MW import`);o+=line(258,y+15,418,y+15,island?C.line:C.power,4)+rect(305,y-9,42,46,C.face)+t(326,y+22,'M',19,C.ink,'middle')+t(326,y-22,'Meter',16,C.muted,'middle');if(island)o+=t(282,y+27,'×',38,C.heat);o+=line(418,y+15,868,y+15,C.power,5)+box(425,84,235,89,'Generator',`${g} MW net`,g?C.power:C.line)+arrow(542,180,542,y+10,g?C.power:C.line)+box(425,328,235,89,'Storage',`${storage} MW`,storage?C.power:C.line);o+=storage?arrow(542,320,542,y+20):line(542,320,542,y+20,C.line,3);o+=arrow(869,y+15,884,y+15)+box(893,177,165,105,'Site load','8 MW');}
 let message=island?(supported?'6 MW generation + 2 MW storage':'2 MW gap · support not established'):kind==='import-contingency'?(g?'Required import: 2 MW · limit: 2 MW':'Required import: 8 MW · limit: 2 MW'):grid<0?'2 MW export requires an allowed route':grid===0?'Zero exchange · connection still closed':`${g} MW local + ${grid} MW grid = 8 MW`;
 o+=t(m?195:560,m?609:492,message,m?17:24,((island&&!supported)||(kind==='import-contingency'&&!g)||grid<0)?C.heat:C.power,'middle');
 return result(o,`At the customer bus: 8 MW load, ${g} MW net local generation, ${storage} MW storage, ${grid} MW ${kind==='import-contingency'?'required grid import':'signed grid exchange'}. ${message}. The meter is at the utility connection.`,`data-grid-mw="${grid}" data-generation-mw="${g}" data-storage-mw="${storage}"`);
}
function duration(s,m){
 const a=islandBudget(s.protectedLoad);let o=t(m?195:560,m?75:66,`${a.loadMW} − 6 = ${a.deficitMW} MW from storage`,m?24:35,C.ink,'middle');
 const items=[['Battery energy','4 MWh usable',a.batteryHours===null?'No deficit':`${a.batteryHours} hours`],['Generator fuel','At 6 MW net output','4 hours']];
 items.forEach(([label,sub,v],i)=>{const x=m?35:110+i*510,y=m?133+i*185:138,w=m?320:400;o+=rect(x,y,w,m?159:222)+t(x+23,y+36,label,23)+t(x+23,y+(m?91:111),v,m?40:50,C.power)+t(x+23,y+(m?135:183),sub,m?18:20,C.muted);});
 o+=t(m?195:560,m?560:432,`Supported interval: ${a.durationHours} hours`,m?25:34,C.heat,'middle')+scope(m,'Battery output limit 3 MW · stable supported island assumed');
 return result(o,`For ${a.loadMW} MW supported load and 6 MW generation the battery deficit is ${a.deficitMW} MW. ${a.batteryHours===null?'No battery discharge is needed':`Its 4 MWh lasts ${a.batteryHours} hours`}. Generator fuel lasts 4 hours. The limiting interval is ${a.durationHours} hours.`,`data-deficit-mw="${a.deficitMW}" data-duration-hours="${a.durationHours}"`);
}
function fuel(s,m){let o=chain(m,[['Gas network','Available supply'],['Site connection','Capacity + pressure'],['Generation plant',s.fuel==='available'?'Net electrical output':'Fuel route interrupted'],['Customer bus','Loads + auxiliaries']]);if(s.fuel==='interrupted'){o+=m?t(195,310,'×',45,C.heat,'middle'):t(570,232,'×',51,C.heat,'middle');}return result(o+scope(m,'Fuel inventory and interruption duration are not modeled'),'Fuel must reach the plant through a capable site connection. '+(s.fuel==='available'?'The conceptual route is available.':'The route is interrupted; generator duration cannot be inferred without fuel inventory and operating conditions.'));}
function brief(m){let o='';const rows=[['Load boundary','8 MW at the customer bus'],['Accepted readiness','Month 21 · Site B assumptions'],['Normal supply','6 MW local + 2 MW grid'],['Supported island','2 hours · stated battery and fuel']];rows.forEach(([a,b],i)=>{const x=m?35:110,y=m?90+i*132:93+i*105;o+=t(x,y,a,m?18:20,C.muted)+t(x,y+40,b,m?21:30)+line(x,y+64,m?355:1010,y+64);});return result(o,rows.map(r=>r.join(': ')).join('. ')+'. A supplied teaching envelope, not a real campus measurement.');}
function phaseCheck(s,m){let o=chain(m,[['Energy contract','Annual total covered'],['Physical connection','8 MW available'],['Proposed phase','10 MW required']]);
 o+=t(m?195:560,m?552:422,s.checkReveal?'2 MW physical shortfall':'Predict: can the full phase open?',m?23:32,s.checkReveal?C.heat:C.ink,'middle');
 if(s.checkReveal)o+=t(m?195:560,m?596:470,'Next: parcel, buildings and access',m?18:23,C.muted,'middle');
 return result(o,`Annual energy contract, 8 MW physical connection, 10 MW required, no local generation or storage. ${s.checkReveal?'No: a 2 MW shortfall prevents the full phase. Next test the parcel, building and access routes.':'Predict before revealing.'}`);
}
export function renderSiting(id,state,compact=false){
 const m=compact;
 if(generationScenes.some(scene=>scene.id===id))return renderGeneration(id,state,m);
 if(['procurement-route','transport-current','parallel-circuits','procurement-decision'].includes(id))return renderProcurement(id,state,m);
 const renders={'site-ready':()=>siteReady(state,m),'parcel-connections':()=>parcel(state,m),'grid-connection':()=>connection(m),'abilene-phase':()=>abilene(m),'purchased-energy':()=>contractPath(state,m),'hourly-match':()=>hourly(m),'storage-match':()=>storage(state,m),'btm-import':()=>bus(state,m,id),'import-contingency':()=>bus(state,m,id),'island-boundary':()=>bus(state,m,id),'island-duration':()=>duration(state,m),'fuel-delivery':()=>fuel(state,m),'supply-brief':()=>brief(m),'phase-check':()=>phaseCheck(state,m)};
 if(!renders[id])throw new Error(`Unknown siting scene: ${id}`);
 return renders[id]();
}
