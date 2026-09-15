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
 return `<figure class="manufacturer-figure supplied-switchgear"><div class="teaching-art"><img src="../assets/generated/distribution-nxairs-labeled.png" alt="Labeled Siemens NXAirS section: busbars at upper left, low-voltage controls at upper right, vacuum circuit breaker in the right-hand withdrawable compartment, and earthing switch and cable connections below."></div><figcaption><a href="${manufacturerURL}#page=12">Siemens NXAirS · up to 12 kV · adapted labels checked against HA 1702, p. 12</a></figcaption></figure>`;
}
