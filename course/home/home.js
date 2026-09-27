import {presentationLabels} from '../prototypes/teaching-navigation.js';

const mount=document.getElementById('campus-mount');
const views={
  campus:{label:'The whole system',text:'Electricity reaches the racks. Cooling carries their heat back outside.',link:'../prototypes/orientation-format.html?teach=1',cta:'Open the overview'},
  power:{label:'Power',text:'The electrical yard steps grid voltage down before power reaches the building and racks.',link:'../prototypes/distribution-format.html?teach=1',cta:'Explore power distribution'},
  compute:{label:'Compute',text:'Inside the data hall, connected servers turn electrical power into useful computation.',link:'../prototypes/rack-energy-format.html?teach=1',cta:'Look inside the rack'},
  cooling:{label:'Cooling',text:'Heat leaves the processors, travels through cooling loops and reaches the outside air.',link:'../prototypes/cooling-format.html?teach=1',cta:'Follow the heat'}
};
function describeView(key){
 const view=views[key]||views.campus;
 document.getElementById('system-label').textContent=view.label;
 document.getElementById('system-description').textContent=view.text;
 const link=document.getElementById('system-link');link.href=new URL(view.link,import.meta.url);link.textContent=view.cta+' ↗';
 document.querySelectorAll('[data-view]').forEach(b=>b.setAttribute('aria-pressed',String(b.dataset.view===key)));
}
async function chapters(){
 try{
  const catalog=new URL('../teaching-sequences.json',import.meta.url);
  const response=await fetch(catalog);
  if(!response.ok)throw new Error('Course directory unavailable');
  const {presentations}=await response.json();
  // Catalog links are relative to the catalog, and staging rewrites them to the published slide paths.
  const entries=presentations.map(p=>{
   const href=p.chapters[0]?.href;
   if(!href)return {};
   const url=new URL(href,catalog);url.search='';url.hash='';
   return {label:presentationLabels[p.id],href:url.href};
  }).filter(p=>p.label&&p.href);
  const list=document.getElementById('chapter-list');list.replaceChildren();
  for(const {label,href} of entries){
   const numbered=/^\d/.test(label),split=numbered?label.indexOf('. '):-2;const link=document.createElement('a');link.className='chapter-link';link.href=href;
   const number=document.createElement('span');number.className='chapter-number';number.textContent=numbered?label.slice(0,split).padStart(2,'0'):'◆';
   const title=document.createElement('span');title.className='chapter-title';title.textContent=label.slice(split+2);
   const arrow=document.createElement('span');arrow.className='chapter-arrow';arrow.textContent='↗';arrow.setAttribute('aria-hidden','true');
   link.append(number,title,arrow);list.append(link);
  }
  document.getElementById('chapter-count').textContent=`${entries.filter(e=>/^\d/.test(e.label)).length} chapters`;
 }catch{document.getElementById('chapter-count').textContent='Course directory';}
}
chapters();
try{
 const {createCampus}=await import('./campus.js');
 const reduced=matchMedia('(prefers-reduced-motion: reduce)');
 let moving=!reduced.matches,power=true,heat=true;
 const campus=createCampus({mount,onSelect:describeView});
 campus.setMotion(moving);
 mount.dataset.ready='true';
 document.querySelector('.campus-controls').hidden=false;
 document.querySelector('.flow-controls').hidden=false;
 const motion=document.getElementById('motion-toggle');
 const updateMotion=()=>{campus.setMotion(moving);motion.textContent=moving?'Pause motion':'Play motion';motion.setAttribute('aria-pressed',String(!moving));};
 updateMotion();
 document.querySelectorAll('[data-view]').forEach(button=>button.addEventListener('click',()=>{campus.focus(button.dataset.view);describeView(button.dataset.view);}));
 document.getElementById('reset-view').addEventListener('click',()=>{campus.reset();describeView('campus');});
 document.querySelectorAll('[data-flow]').forEach(button=>button.addEventListener('click',()=>{
  if(button.dataset.flow==='power')power=!power;else heat=!heat;
  button.setAttribute('aria-pressed',String(button.dataset.flow==='power'?power:heat));
  campus.setFlow(power&&heat?'all':power?'power':heat?'heat':'none');
 }));
 motion.addEventListener('click',()=>{moving=!moving;updateMotion();});
 reduced.addEventListener('change',event=>{moving=!event.matches;updateMotion();});
 window.addEventListener('pagehide',()=>campus.dispose(),{once:true});
 // A restored history entry needs a fresh renderer after pagehide disposed it.
 window.addEventListener('pageshow',event=>{if(event.persisted)location.reload();});
}catch{
 // The still image loads only when the 3D view cannot start.
 const fallback=document.createElement('img');
 fallback.className='campus-fallback';
 fallback.alt='A cutaway data center with an electrical yard, server racks and cooling equipment.';
 fallback.src=new URL('../assets/campus-cutaway.png',import.meta.url).href;
 mount.prepend(fallback);
 mount.dataset.fallback='true';
 document.getElementById('campus-loading').textContent='The 3D view is unavailable here. The full course is ready below.';
 document.getElementById('campus-help').textContent='Campus overview';
 document.querySelector('.campus-topline>span:last-child').textContent='Overview';
}
