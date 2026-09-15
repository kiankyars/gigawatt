import { traceLoad } from './distribution-model.js';

const ink='var(--text)', power='var(--power)', muted='var(--muted)', line='var(--line)';
const tx=(x,y,value,size=22,color=ink,anchor='middle')=>`<text x="${x}" y="${y}" text-anchor="${anchor}" font-size="${size}" fill="${color}">${value}</text>`;
const wire=(d,color=power,width=5)=>`<path d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"/>`;
const dot=(x,y,color=power)=>`<circle cx="${x}" cy="${y}" r="5" fill="${color}"/>`;
const svg=(body,alt,w,h)=>`<svg class="mechanism distribution-context" viewBox="0 0 ${w} ${h}" role="img" aria-label="${alt}">${body}</svg>`;
const transformer=(x,y,color)=>`<circle cx="${x-17}" cy="${y}" r="30" fill="var(--paper)" stroke="${color}" stroke-width="3"/><circle cx="${x+17}" cy="${y}" r="30" fill="var(--paper)" stroke="${color}" stroke-width="3"/>`;
const cabinet=(x,y,w,h,label,color=power)=>`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" fill="var(--surface)" stroke="${color}" stroke-width="2"/>${tx(x+w/2,y+h/2+8,label,21)}`;

export function campusRoute(s,compact){
 const active=traceLoad(s.load),on=id=>active.path.includes(id)?power:line;
 const alt='A 345 kV grid supply feeds a campus transformer, then 34.5 kV switchgear. A hall transformer steps down again to 480 V, feeding rack and cooling branches. A separate future-hall feeder branches from the medium-voltage bus and is open.';
 if(compact){
  const x=99;let o=tx(x,28,'HV grid',23)+tx(275,28,'345 kV AC',22,power)+wire(`M${x} 46V112`,on('service'));
  o+=`<g transform="translate(${x} 160) rotate(90)">${transformer(0,0,on('campus-transformer'))}</g>`+tx(272,147,'Campus transformer',18)+tx(272,180,'345 → 34.5 kV',20);
  o+=wire(`M${x} 208V270`,on('campus-bus'))+cabinet(15,270,168,60,'MV switchgear',on('campus-bus'))+tx(272,255,'34.5 kV AC',21);
  o+=wire('M183 300H293V340',on('future-feeder'))+dot(293,340,on('future-feeder'))+wire('M293 340L316 368',on('future-feeder'))+dot(293,380,line)+wire('M293 380V405',line)+tx(293,431,'Future hall',21)+tx(293,455,'Feeder open',17,muted);
  o+=wire(`M${x} 330V423`,on('transformer'))+`<g transform="translate(${x} 470) rotate(90)">${transformer(0,0,on('transformer'))}</g>`+tx(272,506,'Hall transformer',19)+tx(272,533,'34.5 kV → 480 V',19);
  o+=wire(`M${x} 517V565`,on('building-bus'))+cabinet(15,565,168,60,'Building bus',on('building-bus'))+tx(271,603,'480 V AC',23);
  o+=wire(`M${x} 625V664H62V704`,on('rack'))+wire(`M${x} 664H284V704`,on('pump'));
  o+=cabinet(4,704,154,57,'Row → rack',on('rack'))+cabinet(203,704,180,57,'Cooling pump',on('pump'));
  return svg(o,alt,390,783);
 }
 let o=tx(67,58,'HV grid',23)+tx(67,90,'345 kV AC',19,power)+wire('M25 145H241',on('service'));
 o+=transformer(288,145,on('campus-transformer'))+tx(288,58,'Campus transformer',21)+tx(288,90,'345 → 34.5 kV',19)+wire('M335 145H462',on('campus-bus'));
 o+=cabinet(462,112,174,66,'MV switchgear',on('campus-bus'))+tx(549,90,'34.5 kV AC',19,power)+wire('M636 145H739',on('transformer'));
 o+=transformer(786,145,on('transformer'))+tx(786,58,'Hall transformer',21)+tx(786,90,'34.5 kV → 480 V',19)+wire('M833 145H966',on('building-bus'));
 o+=cabinet(966,112,144,66,'Building bus',on('building-bus'))+tx(1038,90,'480 V AC',19,power);
 o+=wire('M549 178V265H453',on('future-feeder'))+dot(453,265,on('future-feeder'))+wire('M453 265L412 237',on('future-feeder'))+dot(402,265,line)+wire('M402 265H288V318',line)+cabinet(203,318,170,67,'Future hall',line)+tx(426,308,'Feeder open',19,muted);
 o+=wire('M1038 178V251H772V318',on('rack'))+cabinet(683,318,178,67,'Row → rack',on('rack'));
 o+=wire('M1038 251V318',on('pump'))+cabinet(948,318,172,67,'Cooling pump',on('pump'));
 return svg(o,alt,1140,425);
}

function branchDrawing(expanded){
 const w=500;let o=cabinet(100,40,300,65,'480Y/277 V switchboard');
 if(expanded){
  const colors=[power,'var(--heat)','var(--data)',muted,muted];
  ['L1','L2','L3','N','PE'].forEach((v,i)=>{const x=135+i*58;o+=wire(`M${x} 105V292`,colors[i],i===4?3:5)+tx(x,204,v,19,colors[i])+dot(x,105,colors[i])+dot(x,292,colors[i]);});
 }else o+=wire('M250 105V292',power,6)+tx(338,205,'One circuit',20);
 o+=cabinet(100,292,300,65,'Three-phase rack PDU');
 return svg(o,expanded?'The same rack PDU circuit with separate L1, L2, L3, neutral and protective-earth conductors.':'One line represents the circuit from a switchboard to a three-phase rack PDU.',w,386);
}
export function oneLine(){
 return `<div class="branch-comparison"><article><h2>Single-line drawing</h2>${branchDrawing(false)}</article><article><h2>Physical conductors</h2>${branchDrawing(true)}</article></div><div class="voltage-pair"><span><strong>480 V</strong> phase to phase</span><span><strong>277 V</strong> phase to neutral</span></div>`;
}

const manufacturerURL='https://cache.industry.siemens.com/dl/files/485/109972485/att_1290488/v1/1702_NXAirS_12kV_Catalogue_EN_final.pdf';
export function switchgearAnatomy(compact){
 const labels=[['Busbar compartment',.30,.34],['Circuit breaker',.72,.58],['Cable connection',.30,.77],['Protection and controls',.80,.19]];
 let body='';
 if(compact){
  body=`<image href="../assets/references/distribution-siemens-nxairs-cutaway.png" x="0" y="0" width="245" height="355"/>`;
  labels.forEach(([label,x,y],i)=>{body+=`<circle cx="${x*245}" cy="${y*355}" r="14" fill="#086e83"/>`+`<text x="${x*245}" y="${y*355+5}" text-anchor="middle" font-size="16" fill="white">${i+1}</text>`;});
  return `<figure class="manufacturer-figure"><div class="switchgear-mobile">${svg(body,'Original Siemens NXAirS section with numbered busbar, breaker, cable and control compartments.',245,355)}<ol>${labels.map(([label])=>`<li>${label}</li>`).join('')}</ol></div><figcaption><a href="${manufacturerURL}">Siemens NXAirS · up to 12 kV · HA 1702, p. 12</a></figcaption></figure>`;
 }
 const x0=365,y0=0,iw=310,ih=450;
 body=`<rect x="${x0-10}" y="0" width="${iw+20}" height="${ih}" rx="8" fill="#f8f8f3"/><image href="../assets/references/distribution-siemens-nxairs-cutaway.png" x="${x0}" y="${y0}" width="${iw}" height="${ih}"/>`;
 const anchors=[[70,137],[805,284],[70,357],[805,85]];
 labels.forEach(([label,x,y],i)=>{const [lx,ly]=anchors[i],px=x0+x*iw,py=y0+y*ih;body+=wire(`M${px} ${py}H${i===0||i===2?325:720}V${ly-7}H${i===0||i===2?lx+245:lx-15}`,power,2)+dot(px,py)+tx(lx,ly,label,23,ink,'start');});
 return `<figure class="manufacturer-figure">${svg(body,'Original Siemens NXAirS sectional illustration: upper-left busbar compartment, right-side withdrawable breaker, lower cable connection and upper-front protection and controls.',1120,460)}<figcaption><a href="${manufacturerURL}">Siemens NXAirS · up to 12 kV · HA 1702, p. 12</a></figcaption></figure>`;
}
