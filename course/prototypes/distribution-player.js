import { scenes, initialState, aliases, chapter8Aliases } from './distribution-scenes.js';
import { renderDistribution } from './distribution-visuals.js';
import { presentationLabels } from './teaching-navigation.js';
document.title = `${presentationLabels.distribution || 'Campus and building power distribution'} · From Watts to Tokens`;
const $ = id => document.getElementById(id), state={...initialState};
const teaching=new URLSearchParams(location.search).get('teach')==='1';
let index=0;
$('fullscreen').hidden=!teaching;
for(const [i,s] of scenes.entries()) $('scenes').add(new Option(`${i+1} · ${s.label}`,s.id));
function draw(){const result=renderDistribution(scenes[index].id,state,matchMedia('(max-width:600px)').matches);$('stage').innerHTML=result.markup;$('status').textContent=result.description;}
function controls(){
 $('actions').replaceChildren();
 const scene=scenes[index];
 for(const group of scene.controls||[]){
  const field=document.createElement('fieldset');field.className='choices';
  const legend=document.createElement('legend');legend.textContent=group.label;field.append(legend);
  for(const [value,label] of group.options){const b=document.createElement('button');b.textContent=label;b.dataset.key=group.key;b.dataset.value=String(value);b.setAttribute('aria-pressed',String(state[group.key]===value));b.onclick=()=>{state[group.key]=value;field.querySelectorAll('button').forEach(btn=>btn.setAttribute('aria-pressed',String(btn===b)));draw();};field.append(b);}
  $('actions').append(field);
 }
 if(scene.reveal){const b=document.createElement('button');b.id='reveal';const update=()=>{b.textContent=state[scene.reveal]?'Hide reasoning':'Reveal reasoning';b.setAttribute('aria-expanded',String(state[scene.reveal]));};update();b.onclick=()=>{state[scene.reveal]=!state[scene.reveal];update();draw();};$('actions').append(b);}
}
function render(){const scene=scenes[index];$('title').textContent=scene.title;$('title').classList.toggle('sr-only',Boolean(scene.imageTitle||scene.hideTitle));$('scenes').value=scene.id;$('progress').textContent=`${index+1} / ${scenes.length}`;$('previous').disabled=index===0;$('next').disabled=index===scenes.length-1;$('lesson-reference').href=scene.reference;controls();draw();}
function go(value){index=Math.max(0,Math.min(scenes.length-1,value));history.replaceState(null,'',`#${scenes[index].id}`);render();$('stage').scrollTop=0;window.scrollTo(0,0);}
function fromHash(){const requested=location.hash.slice(1);if(chapter8Aliases[requested]){location.replace("rack-energy-format.html" + location.search + "#" + chapter8Aliases[requested]);return;}const id=aliases[requested]||requested;const found=scenes.findIndex(scene=>scene.id===id);index=found<0?0:found;render();$('stage').scrollTop=0;window.scrollTo(0,0);}
$('scenes').onchange=e=>go(scenes.findIndex(scene=>scene.id===e.target.value));$('previous').onclick=()=>go(index-1);$('next').onclick=()=>go(index+1);
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('viewer').requestFullscreen();}catch{$('fullscreen').textContent='Use browser full screen';}};
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen';});
window.addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||e.target.closest('button,select,input,textarea,a,[contenteditable]'))return;if(e.key==='ArrowRight'){e.preventDefault();go(index+1);}if(e.key==='ArrowLeft'){e.preventDefault();go(index-1);}if(e.key.toLowerCase()==='r'&&$('reveal')){e.preventDefault();$('reveal').click();}if(e.key.toLowerCase()==='f'&&teaching)$('fullscreen').click();});
window.addEventListener('hashchange',fromHash);matchMedia('(max-width:600px)').addEventListener('change',draw);fromHash();
