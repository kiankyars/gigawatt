import {scenes,initialState,resolveNetworkingScene} from './networking-scenes.js';
import {networkingVisual} from './networking-visuals.js';
import {presentationLabels} from './teaching-navigation.js';
const $=id=>document.getElementById(id),state={...initialState};
const teaching=new URLSearchParams(location.search).get('teach')==='1';
let index=0;
for(const [i,s]of scenes.entries())$('scenes').add(new Option(`${i+1} · ${s.label}`,s.id));
$('fullscreen').hidden=!teaching;
function focusAfter(selector){render();document.querySelector(selector)?.focus({preventScroll:true});}
function render(){
 const s=scenes[index];$('scene-title').textContent=s.title;$('scene').dataset.scene=s.id;$('scene-title').closest('header').hidden=!!s.imageOnly;
 document.title=`${presentationLabels.networking||'10. Networking and interconnects'} · ${s.label}`;
 $('lesson-reference').href=`../index.html#${s.reference}`;
 $('visual').innerHTML=networkingVisual(s.id,state,matchMedia('(max-width:600px)').matches);
 $('status').textContent=s.title;$('scenes').value=s.id;$('progress').textContent=`${index+1} / ${scenes.length}`;
 $('previous').disabled=index===0;$('next').disabled=index===scenes.length-1;
 $('actions').replaceChildren();
 for(const g of s.controls||[]){const f=document.createElement('fieldset');f.className='choices';const l=document.createElement('legend');l.textContent=g.label;f.append(l);for(const [value,label]of g.options){const b=document.createElement('button');b.textContent=label;b.dataset.choice=g.key;b.dataset.value=value;b.setAttribute('aria-pressed',String(state[g.key]===value));b.onclick=()=>{state[g.key]=value;focusAfter(`[data-choice="${g.key}"][data-value="${value}"]`);};f.append(b);}$('actions').append(f);}
}
function go(i){index=Math.max(0,Math.min(scenes.length-1,i));history.replaceState(null,'',`#${scenes[index].id}`);render();window.scrollTo({top:0,left:0,behavior:'auto'});}
function fromHash(){index=resolveNetworkingScene(location.hash.slice(1));if(location.hash&&location.hash.slice(1)!==scenes[index].id)history.replaceState(null,'',`#${scenes[index].id}`);render();window.scrollTo({top:0,left:0,behavior:'auto'});}
$('scenes').onchange=e=>go(scenes.findIndex(s=>s.id===e.target.value));$('previous').onclick=()=>go(index-1);$('next').onclick=()=>go(index+1);
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('viewer').requestFullscreen();}catch{$('status').textContent='Full screen is unavailable in this browser view.';}};
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen';});
window.addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||e.target.closest('button,select,input,textarea,a,[contenteditable]'))return;if(['ArrowRight','PageDown'].includes(e.key)){e.preventDefault();go(index+1);}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(index-1);}if(e.key.toLowerCase()==='f'&&teaching)$('fullscreen').click();});
window.addEventListener('hashchange',fromHash);matchMedia('(max-width:600px)').addEventListener('change',render);fromHash();
