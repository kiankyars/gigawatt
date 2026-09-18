import {scenes,initialState,sceneAliases} from './heat-rejection-scenes.js';
import {heatRejectionVisual} from './heat-rejection-visuals.js';
import {operatingPoint} from './heat-rejection-model.js';
import {presentationLabels} from './teaching-navigation.js';
const $=id=>document.getElementById(id),state={...initialState};
const teaching=new URLSearchParams(location.search).get('teach')==='1',compact=matchMedia('(max-width:800px)');
let index=0;
for(const [i,scene]of scenes.entries())$('scenes').add(new Option(`${i+1} · ${scene.label}`,scene.id));
$('fullscreen').hidden=!teaching;
function focusAfter(selector){render();document.querySelector(selector)?.focus({preventScroll:true});}
function render(){
 const scene=scenes[index];
 document.title=`${presentationLabels['heat-rejection']||'12. Heat rejection, climate and water'} · ${scene.label}`;
 $('scene').dataset.scene=scene.id;$('scene-title').closest('header').hidden=!!scene.imageOnly;$('scene-title').textContent=scene.title;
 $('visual').innerHTML=heatRejectionVisual(scene.id,state,compact.matches);
 $('lesson-reference').href=`../index.html#${scene.reference}`;
 $('status').textContent=scene.title;$('scenes').value=scene.id;$('progress').textContent=`${index+1} / ${scenes.length}`;
 $('previous').disabled=index===0;$('next').disabled=index===scenes.length-1;
 $('actions').replaceChildren();
 for(const group of scene.controls||[]){
  const fieldset=document.createElement('fieldset');fieldset.className='choices';
  const legend=document.createElement('legend');legend.textContent=group.label;if(group.hideLabel)legend.className='sr-only';fieldset.append(legend);
  for(const [value,label]of group.options){const button=document.createElement('button');button.type='button';button.textContent=label;button.dataset.choice=group.key;button.dataset.value=String(value);button.setAttribute('aria-pressed',String(state[group.key]===value));button.onclick=()=>{state[group.key]=value;focusAfter(`[data-choice="${group.key}"][data-value="${value}"]`);};fieldset.append(button);}
  $('actions').append(fieldset);
 }
 if(scene.id==='approach-outdoors'||scene.id==='approach-wet'){
  const key=scene.id==='approach-wet'?'wetStep':'interfaceStep';
  const waterPhase=(step,selector)=>{
   state[key]=step;focusAfter(selector);
   if(compact.matches)document.querySelector(`[data-water-focus="${['collect','transfer','release','collect'][step]}"]`)?.scrollIntoView({block:'center',behavior:'auto'});
  };
  document.querySelectorAll('[data-water-step]').forEach(button=>button.onclick=()=>waterPhase(Number(button.dataset.waterStep),`[data-water-step="${button.dataset.waterStep}"]`));
  $('approach-next').onclick=()=>waterPhase((state[key]+1)%4,'#approach-next');
 }
 if(scene.id==='hot-hour'){
  const label=document.createElement('label');label.className='h-load-control';label.htmlFor='computing-power';label.textContent='Computing power';
  const slider=document.createElement('input');slider.type='range';slider.id='computing-power';slider.min='4';slider.max='8';slider.step='0.01';slider.value=String(state.requestedITMW);
  const output=document.createElement('output');output.htmlFor='computing-power';output.textContent=`${state.requestedITMW.toFixed(2)} MW`;
  slider.oninput=()=>{state.requestedITMW=Number(slider.value);output.textContent=`${state.requestedITMW.toFixed(2)} MW`;$('visual').innerHTML=heatRejectionVisual(scene.id,state,compact.matches);};
  label.append(slider,output);$('actions').append(label);
  const fit=document.createElement('button');fit.type='button';fit.id='fit-load';fit.textContent='Fit the available power';
  fit.onclick=()=>{state.requestedITMW=Math.min(8,operatingPoint({condition:state.condition}).feasibleMW);focusAfter('#fit-load');};
  $('actions').append(fit);
 }
}
function go(i){index=Math.max(0,Math.min(scenes.length-1,i));history.replaceState(null,'',`#${scenes[index].id}`);render();window.scrollTo({top:0,left:0,behavior:'auto'});}
function fromHash(){let id;try{id=decodeURIComponent(location.hash.slice(1));}catch{id='';}id=sceneAliases[id]||id;const found=scenes.findIndex(scene=>scene.id===id);index=found<0?0:found;render();window.scrollTo({top:0,left:0,behavior:'auto'});}
$('scenes').onchange=event=>go(scenes.findIndex(scene=>scene.id===event.target.value));$('previous').onclick=()=>go(index-1);$('next').onclick=()=>go(index+1);
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('viewer').requestFullscreen();}catch{$('status').textContent='Full screen is unavailable in this browser view.';}};
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen';});
window.addEventListener('keydown',event=>{if(event.altKey||event.ctrlKey||event.metaKey||event.target.closest('button,select,input,textarea,a,[contenteditable]'))return;if(['ArrowRight','PageDown'].includes(event.key)){event.preventDefault();go(index+1);}if(['ArrowLeft','PageUp'].includes(event.key)){event.preventDefault();go(index-1);}if(event.key.toLowerCase()==='f'&&teaching)$('fullscreen').click();});
compact.addEventListener('change',render);window.addEventListener('hashchange',fromHash);fromHash();
