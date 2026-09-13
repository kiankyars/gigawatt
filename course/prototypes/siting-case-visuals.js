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
 return result(o,'Follow delivery phases, connection arrangements and generation duty. The generated geography is a conceptual teaching world, not a real campus.');
}
function release(m){
 let o=t(m?195:560,m?38:35,'POLARIS FORGE 1 · ELLENDALE, NORTH DAKOTA',m?12:19,C.muted,'middle');
 const phases=[['27 OCT 2025','50 MW','Phase I ready for service'],['24 NOV 2025','+50 MW','First 100 MW building complete']];
 phases.forEach(([a,b,c],i)=>{const x=m?27:70+i*560,y=m?90+i*240:122;o+=t(x,y,a,m?20:28)+t(x,y+80,b,m?61:78,C.power)+t(x,y+127,c,m?18:25);if(i===0)o+=m?line(27,294,363,294):line(560,105,560,386);});
 o+=note(m,'Applied Digital · Ready for Service announcements', 'https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at');
 return result(o,'Applied Digital reported the first 50 MW ready for service for CoreWeave on October 27, 2025, and the second 50 MW on November 24. This completed the first 100 MW building at the 400 MW contracted Polaris Forge 1 campus. It is a released-service milestone, not measured IT demand.');
}
function fuel(m){
 let o=img(sitingImages.gas,m?12:20,m?20:10,m?366:750,m?280:425);
 const x=m?25:810,y=m?360:101;
 o+=t(x,y,'14-mile lateral',m?36:35,C.power)+t(x,y+46,'Additional route · August',m?20:20)+t(x,y+80,'Oracle delivery · Jan 2026',m?18:19)+t(x,y+145,'Capacity · pressure · rights',m?19:20,C.muted);
 o+=note(m,'Energy Transfer · August 2026 | Oracle photo · 15 July 2026','https://ir.energytransfer.com/static-files/1cb70dca-abed-4005-95aa-793e3345626c');
 return result(o,'Oracle’s July 15, 2026 photograph shows the Abilene turbine plant. Energy Transfer reports a completed second 14-mile gas lateral in its August update. Separately, it reports deliveries to the Oracle data center beginning in January 2026. No pipe diameter or as-built route is asserted.');
}
function shared(m){
 const o=img(sitingImages.shared,m?8:12,m?83:0,m?374:1096,m?421:484)+t(m?195:560,m?41:36,'SHARED SUBSTATION',m?18:21,C.ink,'middle')+t(m?95:280,m?543:499,'Campus A',m?21:24,C.ink,'middle')+t(m?294:850,m?543:499,'Campus B',m?21:24,C.ink,'middle')+t(m?195:560,m?601:530,'Study coincident demand and upstream constraints.',m?14:18,C.muted,'middle');
 return result(o,'The two illustrative campus feeds meet at a shared upstream substation. Capacity studies account for coincident demand, existing customers and supported contingencies. Generated geography, not a real site or installation drawing.');
}
function abilene(m){
 let o=img(sitingImages.aerial,m?9:15,m?22:12,m?372:805,m?315:440);
 const x=m?26:844,y=m?402:155;
 o+=t(x,y,'75%',m?68:75,C.power)+t(x,y+43,'capacity delivered',m?24:24)+t(x,y+84,'September 2026',m?22:23)+note(m,'Oracle · September status | Aerial · 15 July 2026',oracle);
 return result(o,'Oracle reports 75 percent of total Abilene capacity delivered as of September 2026. Its publisher aerial is dated July 15, 2026. The status page does not establish a denominator for a new MW total or measured IT output. The adjacent Microsoft project remains separate.');
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
 const data=id==='gas-shaft'?{image:sitingImages.turbine,credit:'GE Vernova · gas turbine and generator cutaway',url:'https://www.gevernova.com/gas-power/resources/education/what-is-a-gas-turbine',desc:'Original GE Vernova gas-turbine and generator cutaway. Air compression, combustion and hot-gas expansion produce shaft work for the compressor and generator; the exhaust can then feed heat recovery in a combined-cycle plant.'}:id==='combined-cycle'?{image:sitingImages.combined,credit:'Siemens Energy · combined-cycle principle',url:siemens,desc:'Original Siemens Energy combined-cycle diagram: gas-turbine exhaust enters a heat recovery steam generator; a separate water and steam loop drives the steam turbine and condenser. Both generators supply electricity. The diagram’s 64 percent label is a manufacturer example, not a universal plant efficiency.'}:{image:sitingImages.dispatch,credit:'Siemens Energy · illustrative generation dispatch',url:'https://www.siemens-energy.com/global/en/home/products-services/product/peaker-plants.html',desc:'Original Siemens Energy diagram compares conventional dispatch with higher renewable penetration. Flexible peaking resources supply residual demand left by the other contributions. Qualitative illustration, not recorded or forecast operating values.'};
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
function southaven(id,m){
 const site=id==='southaven-plan';
 const image=site?'../assets/references/southaven-site-plan.png':'../assets/references/southaven-process-plan.png';
 let o=img(image,m?6:12,m?15:0,m?378:site?760:1096,m?480:site?500:500);
 if(site){const x=m?22:820,y=m?535:146;
  o+=t(x,y,'41 simple-cycle turbines',m?23:22)+t(x,y+47,'≈1.2 GW nameplate',m?27:27,C.power)+t(x,y+88,'Proposed · January 2026',m?19:20,C.muted);
 }
 o+=note(m,site?'MZX application · site map · PDF p. 80 ↗':'Trinity Consultants · process figure · PDF p. 13 ↗',southavenPermit+(site?'#page=80':'#page=13'));
 return result(o,site?'Original Southaven MZX site map from its January 2026 air-permit application, retaining Airbus 2025 imagery credit. The proposed facility included 41 simple-cycle turbines and approximately 1.2 GW nameplate. Historical proposal, not a current as-built survey.':'Original Trinity Consultants process flow diagram dated July 2025, reproduced in the January 2026 MZX application. Natural gas conditioning feeds turbines, which supply the data center and battery packs. Emissions branches are shown for the permit. This is not an electrical one-line or completion evidence.');
}
export function renderSitingCase(id,state,m=false){
 const renderers={'southaven-plan':()=>southaven(id,m),'southaven-process':()=>southaven(id,m),'siting-purpose':()=>purpose(m),'site-ready':()=>release(m),'parcel-connections':()=>fuel(m),'grid-connection':()=>shared(m),'abilene-phase':()=>abilene(m),'power-configurations':()=>quadrant(m),'bridge-to-backup':()=>bridge(m),'generation-options':()=>options(m),'gas-shaft':()=>manufacturer(id,m),'combined-cycle':()=>manufacturer(id,m),'grid-dispatch':()=>manufacturer(id,m),'supply-brief':()=>handoff(m)};
 if(id.startsWith('config-'))return config(id,m);
 return renderers[id]?.()??null;
}
