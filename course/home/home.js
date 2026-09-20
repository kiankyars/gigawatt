import {presentationLabels} from '../prototypes/teaching-navigation.js';

const root=new URL('../',import.meta.url);
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
  const response=await fetch(new URL('../teaching-sequences.json',import.meta.url));
  if(!response.ok)throw new Error('Course directory unavailable');
  const {presentations}=await response.json();
  const slideNames={
   'terminology-format.html':'primer.html','orientation-format.html':'overview.html',
   'workload-format.html':'workloads.html','siting-format.html':'siting.html',
   'site-format.html':'site-design.html','distribution-format.html':'distribution.html',
   'continuity-format.html':'continuity.html','rack-energy-format.html':'rack-energy.html',
   'dc-distribution-format.html':'dc-distribution.html','networking-format.html':'networking.html',
   'cooling-format.html':'cooling.html','heat-rejection-format.html':'heat-rejection.html',
   'procurement-cases-format.html':'procurement-cases.html','operations-format.html':'operations.html',
   'capacity-format.html':'capacity.html','integrated-cases-format.html':'integrated-cases.html',
   'grid-queues-format.html':'grid-queues.html'
  };
  const entries=presentations.map(p=>{
   const source=p.chapters[0]?.href?.split('?')[0].split('/').pop();
   return {label:presentationLabels[p.id],href:`slides/${slideNames[source]||source}`};
  }).filter(p=>p.label&&p.href!=='slides/undefined');
  const list=document.getElementById('chapter-list');list.replaceChildren();
  for(const {label,href} of entries){
   const split=label.indexOf('. ');const link=document.createElement('a');link.className='chapter-link';link.href=new URL(href,root);
   const number=document.createElement('span');number.className='chapter-number';number.textContent=label.slice(0,split).padStart(2,'0');
   const title=document.createElement('span');title.className='chapter-title';title.textContent=label.slice(split+2);
   const arrow=document.createElement('span');arrow.className='chapter-arrow';arrow.textContent='↗';arrow.setAttribute('aria-hidden','true');
   link.append(number,title,arrow);list.append(link);
  }
  document.getElementById('chapter-count').textContent=`${entries.length} chapters`;
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
 mount.dataset.fallback='true';
 document.getElementById('campus-loading').textContent='The 3D view is unavailable here. The full course is ready below.';
 document.getElementById('campus-help').textContent='Campus overview';
 document.querySelector('.campus-topline>span:last-child').textContent='Overview';
}
