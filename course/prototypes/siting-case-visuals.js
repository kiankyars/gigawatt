const C={ink:'var(--text)',muted:'var(--muted)',line:'var(--line)',power:'var(--power)',heat:'var(--heat)',panel:'var(--panel)'};
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;');
const t=(x,y,v,z=24,c=C.ink,a='start')=>`<text x="${x}" y="${y}" font-size="${z}" fill="${c}" text-anchor="${a}">${esc(v)}</text>`;
const line=(x,y,xx,yy,c=C.line,w=2)=>`<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${c}" stroke-width="${w}"/>`;
const img=(src,x,y,w,h)=>`<image href="${src}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet"/>`;
const note=(m,text,url)=>`<a href="${url}" target="_blank" rel="noopener noreferrer">${t(m?195:560,m?660:529,text,m?12:16,C.muted,'middle')}</a>`;
const result=(markup,description)=>({markup,description});
export const sitingImages=Object.freeze({
 configurations:'../assets/generated/power-configurations.png',
 shared:'../assets/generated/shared-grid.png',
 aerial:'https://www.oracle.com/cmsng/img/0cb07dd3d128f06e666f776839f78314.jpg',
 gas:'https://www.oracle.com/cmsng/img/02aee384550de51f446469fe8e200aec.jpg',
 turbine:'https://thinglink-data-prod.s3.eu-west-1.amazonaws.com/scene/1814018245611487718/7e60a467e2481d4d92a28c9aeb08f043/image.jpg',
 combined:'https://assets.siemens-energy.com/dam/8ba91ba1-10b1-4e51-8254-b25b015e547f/CombinedCyclePrinciple__Complex-jpg_Original%20file.jpg',
 dispatch:'https://assets.siemens-energy.com/dam/fda3bd2f-e5ab-48e4-ad5b-b2c800bd8224/peaker-plant-load-diagram-3-png_Original%20file.png',
});
const oracle='https://www.oracle.com/data-centers/';
const siemens='https://www.siemens-energy.com/global/en/home/products-services/product/combined-cycle-power-plants.html';
function purpose(m){
 let o=img(sitingImages.shared,m?12:390,m?84:8,m?366:720,m?320:455);
 [['WHEN','Release a usable phase'],['HOW','Connect grid and local supply'],['WHAT','Choose the generation duty']].forEach(([a,b],i)=>{const y=m?445+i*62:94+i*145;o+=t(m?23:25,y,a,m?13:18,C.muted)+t(m?98:25,m?y:y+47,b,m?18:27);});
 return result(o,'Follow delivery phases, connection arrangements and generation duty. The drawing shows a conceptual campus and its connections.');
}
function release(m){
 const image='../assets/references/applied-digital-polaris-forge-1-building1-october-2025.jpg';
 const crop=(x,y,w,h,box)=>`<svg x="${x}" y="${y}" width="${w}" height="${h}" viewBox="${box}" overflow="hidden">${img(image,0,0,1368,829)}</svg>`;
 let o=t(m?195:375,m?32:29,'Polaris Forge 1 · Ellendale',m?16:22,C.ink,'middle');
 o+=t(m?195:375,m?54:49,'Both photos: October 2025 presentation',m?13:16,C.muted,'middle');
 o+=crop(m?12:16,m?75:68,m?366:710,m?83:162,'50 170 1252 285');
 o+=crop(m?12:16,m?180:250,m?366:710,m?131:255,'49 472 724 260');
 const phases=[['27 OCT 2025','50 MW','Phase I ready for service'],['24 NOV 2025','+50 MW','First 100 MW building complete']];
 phases.forEach(([a,b,c],i)=>{const x=m?27:774,y=m?352+i*137:102+i*234;o+=t(x,y,a,m?20:25)+t(x,y+(m?53:78),b,m?44:64,C.power)+t(x,y+(m?89:119),c,m?18:21);});
 o+=note(m,'Applied Digital · October 2025 investor presentation, p. 22', 'https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-25-000076/apld_invxfinalpresentati.htm');
 return result(o,'Two genuine aerial photographs of Polaris Forge 1 Building 1 from Applied Digital’s October 2025 investor presentation. Exact photograph capture dates are not given. The company separately reported 50 MW ready for service for CoreWeave on October 27 and another 50 MW on November 24, completing the first 100 MW building at the 400 MW contracted campus.');
}
function fuel(m){
 let o=img(sitingImages.gas,m?12:20,m?20:10,m?366:750,m?280:425);
 const x=m?25:800,y=m?355:92;
 o+=t(x,y,'14-mile gas lateral',m?31:29,C.power)+t(x,y+43,'Second route · Aug 2026',m?20:20);
 o+=t(x,y+119,'Energy Transfer',m?25:28)+t(x,y+156,'supplies gas to Oracle',m?23:25)+t(x,y+193,'Deliveries began Jan 2026',m?19:20,C.muted);
 o+=note(m,'Energy Transfer · 2026 updates | Oracle photo · 15 July 2026','https://ir.energytransfer.com/static-files/1cb70dca-abed-4005-95aa-793e3345626c');
 return result(o,'Energy Transfer supplies natural gas to Oracle’s Abilene data center. Deliveries began in January 2026; its August update reports a completed second 14-mile lateral in the Abilene area. Oracle is the customer receiving gas. Oracle’s plant photograph is dated July 15, 2026.');
}
function shared(m){
 const badge=(x,y,label,w,z)=>`<rect x="${x-w/2}" y="${y-29}" width="${w}" height="42" rx="7" fill="var(--paper)" stroke="var(--line)"/>${t(x,y,label,z,C.ink,'middle')}`;
 let o=img(sitingImages.shared,m?0:115,m?151:20,m?390:890,m?219.5:501);
 if(m){
  o+=line(195,108,195,204,C.ink,2)+badge(195,91,'Shared substation',218,22);
  o+=line(88,356,88,300,C.ink,2)+badge(88,388,'Campus A',135,22);
  o+=line(302,356,302,300,C.ink,2)+badge(302,388,'Campus B',135,22);
 }else{
  o+=line(560,76,560,151,C.ink,2)+badge(560,58,'Shared substation',266,27);
  o+=line(315,477,315,411,C.ink,2)+badge(315,506,'Campus A',174,27);
  o+=line(805,477,805,411,C.ink,2)+badge(805,506,'Campus B',174,27);
 }
 return result(o,'Campus A and Campus B each have a feed back to the same shared upstream substation. Labels point to the substation and the two campuses. Capacity studies account for their simultaneous demand and the other loads on that network.');
}
function abilene(m){
 let o=img(sitingImages.aerial,m?9:10,m?13:10,m?372:660,m?236:371);
 const x=m?26:717;
 const entries=[['1,200 MW','Original Abilene campus plan'],['75%','Oracle: capacity delivered · Sep 2026'],['900 MW','Implied only on that 1,200 MW basis']];
 entries.forEach(([value,label],i)=>{const y=m?290+i*91:75+i*144;o+=t(x,y,value,m?35:49,C.power)+t(x,y+(m?31:38),label,m?17:21);});
 o+=t(m?26:717,m?571:443,'Current operating MW not reported',m?17:20,C.muted);
 o+=t(m?195:345,m?620:449,'10 GW = Stargate’s wider US target',m?18:25,C.ink,'middle');
 o+=note(m,'Crusoe + Oracle | Aerial · 15 July 2026',oracle);
 return result(o,'The original Oracle/OpenAI Abilene campus has a published 1,200 MW plan across eight buildings. Oracle reports 75% of capacity delivered in September 2026. Multiplying that percentage by the 1,200 MW plan gives 900 MW only if both sources use the same capacity basis; Oracle does not specify that basis or report current operating MW. The 10 GW commitment concerns Stargate sites across the United States, not Abilene alone. The adjacent Microsoft project is separate.');
}
function quadrant(m){return result(img(sitingImages.configurations,m?5:100,m?78:0,m?380:920,m?500:510)+t(m?195:560,m?615:529,'Normal supply directions · backup omitted',m?15:17,C.muted,'middle'),'Four original configurations: grid supplies normal load; grid-parallel local generation and imports; local supply with export-only grid tie; off-grid local supply without an operating grid connection. The four following slides develop each arrangement.');}
function config(id,m){
 const cases={
  'config-grid-supplied':{q:0,a:'Utility supplies normal demand',b:'Backup is a separate design',detail:'An energy contract does not add a feeder.'},
  'config-grid-parallel':{q:1,a:'Local output + permitted imports',b:'Reserve import capacity matters',detail:'A generator outage can increase required imports.'},
  'config-export-only':{q:2,a:'Local supply + surplus exports',b:'No imports to serve the load',detail:'Grid-connected does not mean grid-backed.'},
  'config-off-grid':{q:3,a:'No operating grid tie',b:'Local energy + fast balancing',detail:'Generation and buffering serve different timescales.'},
 };
 const c=cases[id],qx=c.q%2*836,qy=Math.floor(c.q/2)*470;
 let o=`<svg x="${m?10:0}" y="${m?100:35}" width="${m?370:665}" height="${(m?370:665)*470/836}" viewBox="${qx} ${qy} 836 470" overflow="hidden">${img(sitingImages.configurations,0,0,1672,941)}</svg>`;
 const x=m?26:713,y=m?426:171;
 o+=t(x,y,c.a,m?21:25,C.power)+t(x,y+61,c.b,m?20:25)+t(m?195:560,m?604:498,c.detail,m?13:21,C.muted,'middle');
 return result(o,`${c.a}. ${c.b}. ${c.detail} Original conceptual supply directions; not complete switching, grounding, storage or protection diagrams.`);
}
function bridge(m){
 let o=img(sitingImages.gas,m?12:20,m?30:0,m?366:1080,m?295:355);
 [['BEFORE GRID DELIVERY','Bridge supply'],['AFTER GRID DELIVERY','Backup duty']].forEach(([a,b],i)=>{const x=m?25:105+i*595,y=m?400+i*102:411;o+=t(x,y,a,m?15:18,C.muted)+t(x,y+39,b,m?28:32,C.power);});
 o+=note(m,'Crusoe · 2025 impact report, published May 2026','https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report');
 return result(o,'Crusoe describes gas turbines as temporary bridge power and replacement for diesel backup. After grid service arrives their duty can change, subject to engineered start, transfer, protection, fuel and maintenance requirements. The Oracle plant photograph is dated July 15, 2026.');
}
function options(m){
 let o='';
 [['SIMPLE CYCLE','Gas turbine',sitingImages.turbine],['COMBINED CYCLE','Gas turbine + steam cycle',sitingImages.combined]].forEach(([a,b,src],i)=>{const x=m?18:15+i*560,y=m?17+i*322:33;o+=t(x,y+22,a,m?22:26)+t(x,y+61,b,m?18:22,C.muted)+img(src,x,y+83,m?354:535,m?205:327);});
 o+=note(m,'GE Vernova gas turbine | Siemens Energy combined cycle',siemens);
 return result(o,'Simple cycle uses the gas turbine. Combined cycle adds exhaust heat recovery and a separate steam power cycle. Original GE Vernova cutaway and Siemens Energy principle diagram establish the mechanisms, examined next.');
}
function manufacturer(id,m){
 const data=id==='gas-shaft'?{image:sitingImages.turbine,credit:'GE Vernova · gas turbine and generator cutaway',url:'https://www.gevernova.com/gas-power/resources/education/what-is-a-gas-turbine',desc:'Original GE Vernova gas-turbine and generator cutaway. Air compression, combustion and hot-gas expansion produce shaft work for the compressor and generator; the exhaust can then feed heat recovery in a combined-cycle plant.'}:id==='combined-cycle'?{image:sitingImages.combined,credit:'Siemens Energy · combined-cycle principle',url:siemens,desc:'Original Siemens Energy combined-cycle diagram: gas-turbine exhaust enters a heat recovery steam generator; a separate water and steam loop drives the steam turbine and condenser. Both generators supply electricity. The diagram’s 64 percent label is a manufacturer example, not a universal plant efficiency.'}:{image:sitingImages.dispatch,credit:'Siemens Energy · generation dispatch',url:'https://www.siemens-energy.com/global/en/home/products-services/product/peaker-plants.html',desc:'Original Siemens Energy diagram compares conventional dispatch with higher renewable penetration. Flexible peaking resources supply residual demand left by the other contributions.'};
 let visual=img(data.image,m?4:8,m?70:4,m?382:1104,m?535:503);
 if(id==='gas-shaft'){
  const labels=[['Compressor',140,98,155,144],['Combustor',347,85,357,150],['Turbine',510,103,492,166],['Generator',907,448,907,382]];
  let art=img(data.image,0,0,1200,532);
  labels.forEach(([name,x,y,xx,yy])=>{art+=t(x,y,name,24,'#f4f3ee','middle')+line(x,y+(y<200?9:-25),xx,yy,'#a3d6d9',2);});
  visual=`<svg x="${m?6:8}" y="${m?60:4}" width="${m?378:1104}" height="${m?525:503}" viewBox="0 0 1200 532" preserveAspectRatio="xMidYMid meet">${art}</svg>`;
 }
 if(id==='grid-dispatch'){
  const crop=(x,y,w,h,box)=>`<svg x="${x}" y="${y}" width="${w}" height="${h}" viewBox="${box}" preserveAspectRatio="xMidYMid meet">${img(data.image,0,0,2048,1152)}</svg>`;
  visual=m?crop(8,5,374,314,'90 160 935 840')+crop(8,333,374,314,'1010 160 935 840'):crop(8,4,1104,503,'80 150 1870 850');
 }
 return result(visual+note(m,data.credit,data.url),data.desc);
}
function handoff(m){
 let o=img(sitingImages.shared,m?10:135,m?38:4,m?370:850,m?400:445);
 [['Released phase',m?24:100],['Connection routes',m?24:441],['Operating states',m?24:818]].forEach(([a,x],i)=>o+=t(x,m?491+i*58:502,a,m?24:26));
 return result(o,'Carry the released supply phase, connection routes and supported operating states into physical site design: usable land, equipment space, access, replacement paths and failure boundaries.');
}
const southavenPermit='https://upload.wikimedia.org/wikipedia/commons/e/e2/MZX_Tech_LLC_Draft_Air_PSD_Construction_Permit.pdf';
function geography(m){
 const marker=(x,y,name,labelY)=>`<circle cx="${x}" cy="${y}" r="15" fill="#ffd16f" stroke="#102027" stroke-width="6"/><path d="M${x} ${y}L85 ${labelY}" stroke="#fff" stroke-width="4"/><rect x="24" y="${labelY-30}" width="445" height="57" rx="8" fill="#102027ed"/><text x="43" y="${labelY+9}" fill="#fff" font-size="34">${name}</text>`;
 const content=`<image href="../assets/references/southaven-geography.jpg" width="1100" height="1400"/><path d="M-98.82,611.72L9.51,611.61L139.74,611.47L530.95,610.9L552.06,610.9L594.07,610.83L944.72,610.47L1054.26,610.33L1165.25,610.55" fill="none" stroke="#102027" stroke-width="14"/><path d="M-98.82,611.72L9.51,611.61L139.74,611.47L530.95,610.9L552.06,610.9L594.07,610.83L944.72,610.47L1054.26,610.33L1165.25,610.55" fill="none" stroke="#ffd16f" stroke-width="7"/>${marker(533.08,452.02,'Colossus 2 · site',330)}${marker(630.63,989.09,'Power plant · Southaven',1250)}<rect x="35" y="505" width="260" height="48" rx="7" fill="#102027ed"/><text x="53" y="540" fill="#fff" font-size="32">TENNESSEE</text><rect x="35" y="655" width="275" height="48" rx="7" fill="#102027ed"/><text x="53" y="690" fill="#fff" font-size="32">MISSISSIPPI</text>`;
 let o=`<svg x="${m?12:55}" y="${m?0:0}" width="${m?366:470}" height="${m?410:505}" viewBox="0 220 1100 1180" preserveAspectRatio="xMidYMid meet" style="overflow:hidden">${content}</svg>`;
 o+=t(m?195:275,m?429:502,'Historical aerial · site locations',m?12:15,C.muted,'middle');
 if(m){o+=img('../assets/references/southaven-site-plan.png',245,446,135,130);o+=t(20,491,'41 turbines',22,C.power)+t(20,525,'≈1.2 GW',26,C.power)+t(195,606,'Proposed · January 2026',18,C.muted,'middle');}
 else{o+=img('../assets/references/southaven-site-plan.png',550,35,555,370);o+=t(827,445,'41 turbines · ≈1.2 GW',26,C.power,'middle')+t(827,480,'Proposed · January 2026',19,C.muted,'middle');}
 return o;
}
function southaven(id,m){
 const site=id==='southaven-plan';
 let o=site?geography(m):img('../assets/references/southaven-process-plan.png',m?6:12,m?15:0,m?378:1096,m?480:500);
 o+=note(m,site?'USGS · Census boundary · MZX permit plan ↗':'Trinity Consultants · process figure · PDF p. 13 ↗',southavenPermit+(site?'#page=80':'#page=13'));
 return result(o,site?'Colossus 2 is in Memphis, Tennessee; the Southaven power plant is in Mississippi. The state line comes from Census TIGERweb geometry, registered to the returned USGS imagery extent. Markers use the Census street-address point and the permit coordinates. The original permit plan is shown alongside. MZX Tech LLC is the applicant, Trinity Consultants the consulting firm. The January 2026 plan proposed 41 simple-cycle turbines and about 1.2 GW nameplate.':'Original Trinity Consultants process flow diagram dated July 2025, reproduced in the January 2026 MZX application. Natural gas conditioning feeds turbines, which supply the data center and battery packs. Emissions branches are shown for the permit. This is not an electrical one-line or completion evidence.');
}
export function renderSitingCase(id,state,m=false){
 const renderers={'southaven-plan':()=>southaven(id,m),'southaven-process':()=>southaven(id,m),'siting-purpose':()=>purpose(m),'site-ready':()=>release(m),'parcel-connections':()=>fuel(m),'grid-connection':()=>shared(m),'abilene-phase':()=>abilene(m),'power-configurations':()=>quadrant(m),'bridge-to-backup':()=>bridge(m),'generation-options':()=>options(m),'gas-shaft':()=>manufacturer(id,m),'combined-cycle':()=>manufacturer(id,m),'grid-dispatch':()=>manufacturer(id,m),'supply-brief':()=>handoff(m)};
 if(id.startsWith('config-'))return config(id,m);
 return renderers[id]?.()??null;
}
