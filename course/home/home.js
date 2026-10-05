// Homepage entry: course copy first, then the shared voxel data center, then the
// course directory below it.
import './course.js';
import './datacenter/app.js';
import {presentationLabels} from '../prototypes/teaching-navigation.js';

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

// Without WebGL, the campus still image stands in for the 3D world. It is only
// requested in that case.
function showStill(){
 if(document.querySelector('.campus-fallback'))return;
 const still=document.createElement('img');
 still.className='campus-fallback';
 still.alt='A cutaway data center with an electrical yard, server racks and cooling equipment.';
 still.src=new URL('../assets/campus-cutaway.png',import.meta.url).href;
 document.getElementById('world').prepend(still);
}
if(document.body.dataset.world==='fallback')showStill();
document.addEventListener('datacenter:world',event=>{if(event.detail==='fallback')showStill();});
