import { scenes } from './siting-scenes.js';
export const generationInitialState = Object.freeze({});
export const generationScenes = scenes.filter(scene => ['dania-cycle', 'generation-flexibility', 'generation-utilization'].includes(scene.id));

export function generationBalance(cycle){
 if(!['simple','combined'].includes(cycle))throw new RangeError('Unknown power cycle');
 const efficiency=cycle==='simple'?.4:.6,netMW=100,fuelMW=netMW/efficiency;
 return {efficiency,netMW,fuelMW,remainderMW:fuelMW-netMW};
}
const dailyDemand=Object.freeze([130,120,110,100,100,110,130,160,185,205,220,230,240,250,260,260,250,245,230,215,195,175,155,140]);
export function dispatchDay(campusMW=0){
 if(!Number.isFinite(campusMW)||campusMW<0)throw new RangeError('Campus load must be finite and nonnegative');
 return dailyDemand.map((baselineMW,hour)=>{const demandMW=baselineMW+campusMW,baseMW=100,combinedMW=Math.min(120,demandMW-baseMW),peakerMW=Math.min(80,Math.max(0,demandMW-baseMW-combinedMW)),shortfallMW=demandMW-baseMW-combinedMW-peakerMW;return{hour,demandMW,baseMW,combinedMW,peakerMW,shortfallMW};});
}
export function generationCosts(hours){
 if(!Number.isFinite(hours)||hours<0||hours>8760)throw new RangeError('Hours must be between 0 and 8760');
 const simpleFuelPerMWh=20/.4,combinedFuelPerMWh=20/.6,simpleFixed=8e6,combinedFixed=16e6;
 const simpleTotal=simpleFixed+100*hours*simpleFuelPerMWh,combinedTotal=combinedFixed+100*hours*combinedFuelPerMWh;
 return {hours,simpleTotal,combinedTotal,simpleFixed,combinedFixed,simpleFuelPerMWh,combinedFuelPerMWh,crossoverHours:(combinedFixed-simpleFixed)/(100*(simpleFuelPerMWh-combinedFuelPerMWh)),winner:Math.abs(simpleTotal-combinedTotal)<.01?'equal':simpleTotal<combinedTotal?'simple':'combined'};
}
const C={ink:'var(--text)',muted:'var(--muted)',line:'var(--line)',power:'var(--power)',heat:'var(--heat)',paper:'var(--paper)'};
const esc=s=>String(s).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const t=(x,y,v,z=24,c=C.ink,a='start')=>`<text x="${x}" y="${y}" font-size="${z}" fill="${c}" text-anchor="${a}">${esc(v)}</text>`;
const line=(x,y,xx,yy,c=C.line,w=2,dash='')=>`<path d="M${x} ${y}L${xx} ${yy}" fill="none" stroke="${c}" stroke-width="${w}" stroke-dasharray="${dash}"/>`;
const img=(src,x,y,w,h)=>`<image href="${src}" x="${x}" y="${y}" width="${w}" height="${h}" preserveAspectRatio="xMidYMid meet"/>`;
const result=(markup,description)=>({markup,description});
const daniaPhoto='https://www.gevernova.com/content/dam/gepower-new/global/en_US/images/gas-new-site/resources/case-studies/first-7ha-florida-power-light/first-7ha-florida-power-light-hero.png';
function dania(m){
 const x=m?24:764, y=m?357:104;
 const o=img(daniaPhoto,m?8:12,8,m?374:715,m?310:447)
  +t(x,y,'FPL utility power station',m?25:26)
  +t(x,y+57,'2 × GE 7HA.03',m?32:33,C.power)
  +t(x,y+93,'Gas-turbine model',m?21:22,C.muted)
  +t(x,y+163,'Up to 1,260 MW',m?31:31,C.power)
  +t(x,y+199,'Combined plant output',m?21:22,C.muted)
  +`<a href="https://www.gevernova.com/gas-power/resources/case-studies/first-7ha-florida-power-light" target="_blank" rel="noopener">${t(m?195:560,m?655:523,'GE Vernova · Dania Beach, Florida',m?15:18,C.muted,'middle')}</a>`;
 return result(o,'FPL’s Dania Beach Clean Energy Center is a utility power station in Florida, not a data center. GE 7HA.03 identifies the gas-turbine model. GE reports two such turbines and combined plant output up to 1,260 MW. The image is the manufacturer’s real plant photograph.');
}
function flexibility(m){
 const src='../assets/generated/generation-timescales.png';
 let o;
 if(m){
  const labels=[['Delivery','Equipment','and construction'],['Startup','Stopped to','generating'],['Ramping','Adjust the','running output']];
  o=labels.map(([name,a,b],i)=>{const q=i*557.333,y=10+i*211;return `<svg x="8" y="${y}" width="165" height="190" viewBox="${q} 170 557.333 540" preserveAspectRatio="xMidYMid meet"><defs><clipPath id="plant-crop-${i}"><rect x="${q}" y="170" width="557.333" height="540"/></clipPath></defs><g clip-path="url(#plant-crop-${i})">${img(src,0,0,1672,941)}</g></svg>`+t(193,y+55,name,26)+t(193,y+94,a,17,C.muted)+t(193,y+120,b,17,C.muted);}).join('');
 } else o=img(src,16,0,1088,520);
 return result(o,'Follow the same conceptual plant from delivery and construction, to startup, to changing its running output. Delivery depends on equipment and construction; startup depends on the machine’s initial state; ramp rate describes changes once generating. GPT-generated conceptual illustration, not an OEM layout or measured output trace. GE’s separate hot-start and ramp specifications are in the reading.');
}
function costs(m){
 const x=m?52:93,y=m?415:425,w=m?302:680,h=m?280:325;
 const xx=hours=>x+hours/8000*w, yy=cost=>y-cost/1e6/50*h;
 let o=t(x,m?43:39,'Annual cost · $ million',m?23:26);
 if(m)o+=t(x,78,'Simple cycle · 40%',19,C.heat)+t(x,104,'Combined cycle · 60%',19,C.power);
 [0,10,20,30,40,50].forEach(v=>o+=line(x,y-v/50*h,x+w,y-v/50*h,C.line,1)+t(x-9,y-v/50*h+5,v,m?13:17,C.muted,'end'));
 [0,2000,4000,6000,8000].forEach(v=>o+=t(xx(v),y+27,v.toLocaleString(),m?12:17,C.muted,'middle'));
 for(const [key,c] of [['simpleTotal',C.heat],['combinedTotal',C.power]]){
  o+=line(xx(0),yy(generationCosts(0)[key]),xx(8000),yy(generationCosts(8000)[key]),c,m?4:5);
 }
 const cross=generationCosts(4800);
 o+=line(xx(4800),yy(cross.simpleTotal),xx(4800),y,C.muted,1.5,'5 5')
  +`<circle cx="${xx(4800)}" cy="${yy(cross.simpleTotal)}" r="6" fill="${C.ink}"/>`
  +t(xx(4800)-8,yy(cross.simpleTotal)-(m?27:30),'4,800 h',m?19:25,C.ink,'end');
 if(!m)o+=t(802,yy(generationCosts(8000).simpleTotal)+6,'Simple cycle · 40%',24,C.heat)
  +t(802,yy(generationCosts(8000).combinedTotal)+6,'Combined cycle · 60%',24,C.power);
 o+=t(x+w/2,y+59,'Full-load hours per year',m?19:23,C.muted,'middle');
 if(m)o+=t(24,541,'Illustrative 100 MW plants',21)+t(24,580,'Fuel: $20 / MWh of fuel energy',17,C.muted)+t(24,614,'Annual fixed cost: $8M / $16M',17,C.muted);
 else o+=t(560,529,'Illustrative 100 MW · fuel $20/MWh · annual fixed cost $8M / $16M',18,C.muted,'middle');
 return result(o,'Compare both complete annual-cost curves at once. Hypothetical 100 MW simple cycle uses 40 percent efficiency and $8 million annualized fixed cost; combined cycle uses 60 percent and $16 million. At $20 per MWh of fuel energy, variable fuel cost is $50 versus $33.33 per MWh electric. Both cost $32 million at 4,800 full-load hours. Fewer hours favor lower fixed cost; more favor fuel savings. Fuel and efficiency use the same lower-heating-value basis, defined in the reader.');
}
export function renderGeneration(id,state,compact=false){
 const renders={'dania-cycle':dania,'generation-flexibility':flexibility,'generation-utilization':costs};
 if(!renders[id])throw new RangeError(`Unknown generation scene: ${id}`);
 return renders[id](compact);
}
