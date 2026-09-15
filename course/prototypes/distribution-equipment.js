import {relayProtection} from './distribution-instruments.js';
const ink='var(--text)', teal='var(--power)', orange='var(--heat)', muted='var(--muted)';
const tx=(x,y,t,size=22,color=ink)=>`<text x="${x}" y="${y}" text-anchor="middle" font-size="${size}" fill="${color}">${t}</text>`;
const ln=(d,color=teal,w=5,dash=false)=>`<path d="${d}" stroke="${color}" stroke-width="${w}" fill="none" stroke-linecap="round" ${dash?'stroke-dasharray="8 7"':''}/>`;
const panel=(x,y,w,h,stroke='var(--line)')=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="var(--surface)" stroke="${stroke}" stroke-width="2"/>`;
export function equipment(id,s,m){
 if(id==='protection-relay')return relayProtection(s,m);
 if(id==='isolation-surge'||id==='surge-protection')return systemProtection(id,m);
 if(id==='phase-loading')return phaseAllocation(s,m);
 if(id==='feeder-diagnosis')return breakerFailure(s,m);
 throw new RangeError(`Unknown equipment scene: ${id}`);
}


const systemSvg=(o,alt,w,h)=>`<svg class="mechanism equipment-system" viewBox="0 0 ${w} ${h}" role="img" aria-label="${alt}">${o}</svg>`;
const dot=(x,y,color=teal,r=5)=>`<circle cx="${x}" cy="${y}" r="${r}" fill="${color}"/>`;
const ground=(x,y,color=orange)=>ln(`M${x} ${y}v16 m-22 0h44 m-15 10h-14 m4 10h6`,color,3);
const contact=(x,y,open,color=teal)=>ln(`M${x-35} ${y}L${x+(open?28:35)} ${y-(open?30:0)}`,color,5)+dot(x-35,y,color)+dot(x+35,y,color);
const contactLeads=(x,y,left,right,color)=>ln(`M${left} ${y}H${x-35} M${x+35} ${y}H${right}`,color,5);
const transformer=(x,y,color=teal)=>`<circle cx="${x-17}" cy="${y}" r="29" fill="var(--paper)" stroke="${color}" stroke-width="3"/><circle cx="${x+17}" cy="${y}" r="29" fill="var(--paper)" stroke="${color}" stroke-width="3"/>`;
const rack=(x,y,color=teal)=>panel(x-35,y,70,83,color)+[16,33,50,67].map(d=>ln(`M${x-23} ${y+d}h46`,color,2)).join('');

function systemProtection(id,m){
 const surge=id==='surge-protection',path=surge?teal:muted;
 const alt=surge?'The supply passes through a closed breaker and disconnector to a transformer and data hall. A surge arrester connects from the phase conductor beside the transformer to earth. The orange transient-current path branches to earth; the arrester is not in series with the load.':'The breaker and disconnector are located in series between the medium-voltage supply and the transformer serving the hall. The breaker is open; a separate open disconnector provides the highlighted air gap. The transformer and hall remain visible on the disconnected side.';
 if(m){
  const x=104;
  let o=tx(104,24,'MV supply',20)+ln(`M${x} 43V87`,teal,6);
  o+=panel(56,87,96,73)+`<g transform="translate(${x} 124) rotate(90)">${contact(0,0,!surge,surge?teal:muted)}</g>`;
  o+=tx(253,117,'Circuit breaker',19)+tx(253,142,surge?'Closed':'Open',16,surge?teal:muted);
  o+=ln(`M${x} 160V202`,path,6)+`<g transform="translate(${x} 237) rotate(90)">${contact(0,0,!surge,surge?teal:orange)}</g>`;
  o+=tx(260,231,'Disconnector',19)+tx(260,256,surge?'Closed':'Air gap',16,surge?teal:orange);
  o+=ln(`M${x} 272V395`,path,6)+`<g transform="translate(${x} 424) rotate(90)">${transformer(0,0,path)}</g>`;
  o+=tx(250,426,'Transformer',20)+ln(`M${x} 470V513`,path,6)+rack(x,513,path)+tx(253,558,'Data hall',20);
  if(surge){
   o+=dot(x,328)+ln(`M${x} 328H254V350`,orange,5)+panel(230,350,48,53,orange)+ln('M235 397L273 356',orange,3)+ground(254,403);
   o+=tx(268,299,'Surge arrester',18,orange)+tx(296,480,'To earth',16,orange);
  }
  return systemSvg(o,alt,390,615);
 }
 let o=tx(86,162,'MV supply',22)+ln('M40 230H198',teal,7);
 o+=panel(198,185,134,90)+contact(265,230,!surge,surge?teal:muted)+contactLeads(265,230,198,332,path)+tx(265,155,'Circuit breaker',22);
 o+=ln('M332 230H455',path,7)+contact(490,230,!surge,surge?teal:orange)+tx(490,155,'Disconnector',22);
 o+=ln('M525 230H729',path,7)+transformer(775,230,path)+tx(775,155,'Transformer',22)+ln('M821 230H994',path,7)+rack(1029,188,path)+tx(1029,155,'Data hall',22);
 if(surge){
  o+=dot(650,230)+ln('M650 230V301',orange,6)+panel(626,301,48,64,orange)+ln('M631 358L669 308',orange,3)+ground(650,365);
  o+=tx(489,323,'Surge arrester',22,orange)+tx(489,351,'Transient path to earth',17,orange);
 }else{
  o+=tx(265,315,'Open',20,muted)+tx(490,315,'Air gap',22,orange);
 }
 return systemSvg(o,alt,1120,440);
}

function phaseAllocation(s,m){
 const counts=s.balanced?[2,2,2]:[4,1,1],w=m?390:1120;
 // Every PSU group terminates on a phase and on the common neutral.
 // The allocation is the changed variable; the same six loads remain connected.
 const alt=`Six single-phase rack PSU groups each draw 20 amps at 277 volts between a phase and neutral. ${s.balanced?'Two groups per phase gives 40, 40 and 40 amps.':'Four groups on L1 and one on each other phase gives 80, 20 and 20 amps; L1 exceeds its 60 amp limit.'} Both arrangements use all six groups.`;
 let next=0,o=tx(w/2,42,'277 V · 20 A per PSU group',m?20:25);
 if(m){
  const groupX=[93,170,247,324];
  counts.forEach((count,i)=>{
   const y=116+i*165,color=count>3?orange:teal;
   o+=tx(30,y+7,`L${i+1}`,20)+ln(`M55 ${y}H370`,color,4)+tx(298,y-18,`${20*count} A / 60 A`,20,color);
   o+=tx(30,y+108,'N',18,muted)+ln(`M55 ${y+101}H370`,muted,3);
   for(let j=0;j<count;j++){
    const x=groupX[j],label=String.fromCharCode(65+next++);
    o+=ln(`M${x} ${y}v28`,color,3)+panel(x-31,y+28,62,50,color)+tx(x,y+59,label,22)+ln(`M${x} ${y+78}v23`,muted,3)+dot(x,y,color,3)+dot(x,y+101,muted,3);
   }
  });
  return systemSvg(o,alt,w,575);
 }
 counts.forEach((count,i)=>{
  const y=124+i*118,color=count>3?orange:teal;
  o+=tx(43,y+8,`L${i+1}`,23)+ln(`M75 ${y}H895`,color,5);
  o+=ln(`M135 ${y+87}H946`,muted,3);
  for(let j=0;j<count;j++){
   const x=230+j*176,label=String.fromCharCode(65+next++);
   o+=ln(`M${x} ${y}v19`,color,3)+panel(x-63,y+19,126,50,color)+tx(x,y+50,`Group ${label}`,21)+ln(`M${x} ${y+69}v18`,muted,3)+dot(x,y,color,4)+dot(x,y+87,muted,4);
  }
  o+=tx(1025,y+17,`${20*count} A`,35,color)+tx(1025,y+48,'60 A limit',18,muted);
 });
 o+=ln('M946 211V447',muted,3)+tx(820,479,'Common neutral',19,muted)+ln('M917 474L942 448',muted,2);
 return systemSvg(o,alt,w,505);
}

function breakerFailure(s,m){
 const backup=s.diagnosisStage==='backup',bus=backup?muted:teal,fault=backup?muted:orange;
 const alt=backup?'The incoming breaker opens after the Hall A feeder breaker fails to interrupt. This removes the fault current and also removes supply to Hall B, which has no local fault. Both halls share the bus downstream of the incoming breaker.':'Hall A has a feeder fault. Its protection relay has issued a trip, but the feeder breaker remains closed and fault current continues. Hall B has no local fault and shares the incoming breaker and common bus. Backup protection can open that incoming breaker.';
 if(m){
  let o=tx(195,25,'Campus supply',21)+ln('M195 44V83',teal,6);
  o+=panel(137,83,116,90)+`<g transform="translate(195 128) rotate(90)">${contact(0,0,backup,backup?muted:orange)+contactLeads(0,0,-45,45,backup?muted:teal)}</g>`;
  o+=tx(72,102,'Incoming',17)+tx(72,125,'breaker',17)+tx(314,132,backup?'Opened':'Closed',19,backup?muted:teal);
  o+=ln('M195 173V215H80 M195 215H310',bus,6)+tx(195,198,'Shared bus',18);
  o+=ln('M80 215V275',fault,6)+ln('M310 215V275',bus,6);
  o+=panel(39,275,82,92,orange)+`<g transform="translate(80 321) rotate(90)">${contact(0,0,false,fault)+contactLeads(0,0,-46,46,fault)}</g>`;
  o+=panel(269,275,82,92)+`<g transform="translate(310 321) rotate(90)">${contact(0,0,false,bus)+contactLeads(0,0,-46,46,bus)}</g>`;
  o+=tx(195,293,'Feeder',18)+tx(195,317,'breakers',18)+tx(80,255,'Failed to open',17,orange);
  o+=ln('M80 367V455',fault,6)+ln('M310 367V455',bus,6);
  o+=ln('M66 393L94 421 M94 393L66 421',orange,4)+tx(195,414,backup?'Fault isolated':'Fault persists',19,orange);
  o+=rack(80,455,muted)+rack(310,455,bus)+tx(80,568,'Hall A',23)+tx(310,568,'Hall B',23)+tx(310,596,backup?'Supply removed':'No local fault',17,backup?orange:muted);
  return systemSvg(o,alt,390,620);
 }
 let o=tx(96,179,'Campus supply',21)+ln('M35 235H200',teal,7);
 o+=panel(200,190,150,90)+contact(275,235,backup,backup?muted:orange)+contactLeads(275,235,200,350,backup?muted:teal)+tx(275,147,'Incoming breaker',23)+tx(275,323,backup?'Opened':'Closed',20,backup?orange:muted);
 o+=ln('M350 235H442 M442 110V380',bus,8)+tx(442,63,'Shared bus',22);
 o+=ln('M442 110H615',fault,7)+panel(615,65,160,90,orange)+contact(695,110,false,fault)+contactLeads(695,110,615,775,fault)+ln('M775 110H946',fault,7);
 o+=tx(695,34,'Hall A feeder breaker',22)+tx(695,195,'Failed to open',22,orange);
 o+=ln('M841 94L871 126 M871 94L841 126',orange,5)+tx(864,175,backup?'Isolated fault':'Fault persists',20,orange);
 o+=rack(981,68,muted)+tx(1036,181,'Hall A',22);
 o+=ln('M442 380H615',bus,7)+panel(615,335,160,90)+contact(695,380,false,bus)+contactLeads(695,380,615,775,bus)+ln('M775 380H946',bus,7);
 o+=tx(695,308,'Hall B feeder breaker',22)+rack(981,338,bus)+tx(1036,451,'Hall B',22);
 o+=tx(864,469,backup?'Supply removed':'No local fault',21,backup?orange:muted);
 if(!backup)o+=tx(745,244,'Trip issued → breaker remained closed',19,orange);
 return systemSvg(o,alt,1120,500);
}
