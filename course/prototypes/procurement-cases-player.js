import {scenes,initialState,resolveProcurementScene} from './procurement-cases-scenes.js';
import {procurementVisual} from './procurement-visuals.js';
import {presentationLabels} from './teaching-navigation.js';
const $=id=>document.getElementById(id),state={...initialState};
const teaching=new URLSearchParams(location.search).get('teach')==='1';
let index=0;
for(const [i,scene]of scenes.entries())$('scenes').add(new Option(`${i+1} · ${scene.label}`,scene.id));
$('fullscreen').hidden=!teaching;
function focusAfter(selector){render();document.querySelector(selector)?.focus({preventScroll:true});}
function render(){
 const scene=scenes[index];
 document.title=`${presentationLabels['procurement-cases']||'14. Design, procurement and commissioning'} · ${scene.label}`;
 $('scene').dataset.scene=scene.id;$('scene-title').textContent=scene.title;
 $('visual').innerHTML=procurementVisual(scene.id,state);
 $('lesson-reference').href=`../index.html#${scene.reference}`;
 $('status').textContent=scene.title;$('scenes').value=scene.id;$('progress').textContent=`${index+1} / ${scenes.length}`;
 $('previous').disabled=index===0;$('next').disabled=index===scenes.length-1;
 $('actions').replaceChildren();
 for(const group of scene.controls||[]){
  const fieldset=document.createElement('fieldset');fieldset.className='choices';
  const legend=document.createElement('legend');legend.textContent=group.label;fieldset.append(legend);
  for(const [value,label]of group.options){const button=document.createElement('button');button.type='button';button.textContent=label;button.dataset.choice=group.key;button.dataset.value=value;button.setAttribute('aria-pressed',String(state[group.key]===value));button.onclick=()=>{state[group.key]=value;focusAfter(`[data-choice="${group.key}"][data-value="${value}"]`);};fieldset.append(button);}
  $('actions').append(fieldset);
 }
 document.querySelectorAll('[data-evidence]').forEach(button=>button.onclick=()=>{const key=button.dataset.evidence;state[key]=!state[key];focusAfter(`[data-evidence="${key}"]`);});
 document.querySelectorAll('[data-diagnosis]').forEach(button=>button.onclick=()=>{state.diagnosis=button.dataset.diagnosis;state.showDiagnosis=false;focusAfter(`[data-diagnosis="${state.diagnosis}"]`);});
 $('diagnosis-reveal')?.addEventListener('click',()=>{state.showDiagnosis=!state.showDiagnosis;focusAfter('#diagnosis-reveal');});
}
function go(i){index=Math.max(0,Math.min(scenes.length-1,i));history.replaceState(null,'',`#${scenes[index].id}`);render();window.scrollTo({top:0,left:0,behavior:'auto'});}
function fromHash(){index=resolveProcurementScene(location.hash.slice(1));if(location.hash&&location.hash.slice(1)!==scenes[index].id)history.replaceState(null,'',`#${scenes[index].id}`);render();window.scrollTo({top:0,left:0,behavior:'auto'});}
$('scenes').onchange=event=>go(scenes.findIndex(scene=>scene.id===event.target.value));$('previous').onclick=()=>go(index-1);$('next').onclick=()=>go(index+1);
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('viewer').requestFullscreen();}catch{$('status').textContent='Full screen is unavailable in this browser view.';}};
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen';});
window.addEventListener('keydown',event=>{if(event.altKey||event.ctrlKey||event.metaKey||event.target.closest('button,select,input,textarea,a,[contenteditable]'))return;if(['ArrowRight','PageDown'].includes(event.key)){event.preventDefault();go(index+1);}if(['ArrowLeft','PageUp'].includes(event.key)){event.preventDefault();go(index-1);}if(event.key.toLowerCase()==='f'&&teaching)$('fullscreen').click();});
window.addEventListener('hashchange',fromHash);fromHash();
