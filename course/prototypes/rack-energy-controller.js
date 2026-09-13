import { scenes, initialState, aliases, defaults } from './rack-energy-scenes.js';
import { rackVisual, supplementalVisual, escapeHTML } from './rack-energy-visuals.js';
import { createElectricalVisuals } from '../web/electrical-renderer.js';
import { createPresentationRenderers } from '../web/presentation-renderers.js';
import { acdcConductorModel, acdcWaveModel } from '../web/reader-models.js';
import { presentationLabels } from './teaching-navigation.js';

const $=id=>document.getElementById(id), state={...initialState, revealed:[]};
const fmt=(v,d=0)=>v.toLocaleString('en-US',{maximumFractionDigits:d});
const teaching=new URLSearchParams(location.search).get('teach')==='1';
let index=0;
const current=()=>scenes[index];
const isRevealed=()=>state.revealed.includes(current().id);
const electrical=createElectricalVisuals({acdcWaveModel,getState:()=>state,escapeHTML,fmt});
const sample=createPresentationRenderers({defaults,getState:()=>state,getStep:current,isRevealed,acdcConductorModel,escapeHTML,fmt,assets:'../assets/'});
for(const [i,scene] of scenes.entries())$('scenes').add(new Option(`${i+1} · ${scene.label}`,scene.id));
$('fullscreen').hidden=!teaching;

function draw(){
  const scene=current(), compact=matchMedia('(max-width:600px)').matches;
  let markup,description=scene.title;
  if(scene.kind==='rack')({markup,description}=rackVisual(scene,state,compact));
  else if(scene.kind==='800v'){
    const kind=scene.sourceKind;
    markup=({'intro':sample.intro,'copper':sample.copper,'current':sample.current,'loss':sample.loss,
      'conversion-loss':sample.conversionViews,'source-figure':sample.sourceFigure}[kind]
      || (['dc-basics','ac-basics','three-phase','voltage-basis'].includes(kind)?()=>electrical.electricalVisual(kind):()=>sample.architecture(kind)))();
  }else markup=supplementalVisual(scene,state);
  $('visual').innerHTML=markup;
  $('scene').dataset.kind=scene.kind;
  $('status').textContent=description;
  bindVisual();
}
function redrawAndFocus(selector, full=false){
  if(full)render();else draw();
  document.querySelector(selector)?.focus({preventScroll:true});
}
function reveal(){
  const scene=current();
  if(scene.kind==='800v'){
    if(!['current','loss','conversion-loss'].includes(scene.sourceKind))return;
    if(scene.sourceKind==='conversion-loss')state.converterView='heat';
    state.revealed=isRevealed()?state.revealed.filter(id=>id!==scene.id):[...state.revealed,scene.id];
  }else if(scene.reveal)state[scene.reveal]=!state[scene.reveal];
  else if(scene.kind==='decision'&&state.decision)state.migrationReveal=!state.migrationReveal;
  else return;
  render();
  ($('reveal')||$('chapter-reveal')||$('scene')).focus({preventScroll:true});
}
function bindVisual(){
  document.querySelectorAll('[data-voltage-view]').forEach(b=>b.onclick=()=>{state.voltageView=b.dataset.voltageView;redrawAndFocus(`[data-voltage-view="${state.voltageView}"]`);});
  document.querySelectorAll('[data-converter-view]').forEach(b=>b.onclick=()=>{state.converterView=b.dataset.converterView;redrawAndFocus(`[data-converter-view="${state.converterView}"]`,true);});
  document.querySelectorAll('[data-decision]').forEach(b=>b.onclick=()=>{state.decision=b.dataset.decision;state.migrationReveal=false;redrawAndFocus(`[data-decision="${state.decision}"]`,true);});
  $('cycle-angle')?.addEventListener('input',e=>{state.cycleDegrees=Number(e.target.value);$('wave-content').innerHTML=electrical.electricalContent(current().sourceKind);$('cycle-value').textContent=`${state.cycleDegrees}° · ${fmt(state.cycleDegrees/360/60*1000,2)} ms`;});
  $('voltage')?.addEventListener('input',e=>{state.volts=Number(e.target.value);$('variable-voltage').textContent=state.volts;$('variable-current').innerHTML=`<div class="metric">${fmt(sample.conductorNumbers(state.volts).dc.amps,1)} <small>A</small></div>`;$('voltage-value').textContent=`${state.volts} V`;$('variable-derivation').textContent=`100,000 W ÷ ${state.volts} V`;});
  $('reset-voltage')?.addEventListener('click',()=>{state.volts=800;redrawAndFocus('#reset-voltage');});
  $('reveal')?.addEventListener('click',reveal);
}
function controls(){
  $('actions').replaceChildren();
  for(const group of current().controls||[]){
    const field=document.createElement('fieldset');field.className='choices';
    const legend=document.createElement('legend');legend.textContent=group.label;field.append(legend);
    for(const [value,label] of group.options){const b=document.createElement('button');b.textContent=label;b.dataset.choice=group.key;b.dataset.value=String(value);b.setAttribute('aria-pressed',String(state[group.key]===value));b.onclick=()=>{state[group.key]=value;if(group.key==='deadlineWeeks')state.migrationReveal=false;redrawAndFocus(`[data-choice="${group.key}"][data-value="${value}"]`,true);};field.append(b);}
    $('actions').append(field);
  }
  if(current().reveal||current().kind==='decision'){
    const b=document.createElement('button');b.id='chapter-reveal';const shown=current().reveal?state[current().reveal]:state.migrationReveal;
    b.textContent=shown?'Hide reasoning':'Reveal reasoning';b.setAttribute('aria-expanded',String(shown));b.disabled=current().kind==='decision'&&!state.decision;b.onclick=reveal;$('actions').append(b);
  }
}
function render(){
  const scene=current();
  $('scene-title').textContent=scene.sourceKind==='conversion-loss'&&state.converterView==='heat'?scene.heat_headline:scene.title;
  document.title=`${presentationLabels['rack-energy']||presentationLabels['rack-800v']||'Rack power and the 800 V DC transition'} · ${scene.title} · From Watts to Tokens`;
  $('lesson-reference').href=`../index.html#${scene.reference}`;
  $('scenes').value=scene.id;$('progress').textContent=`${index+1} / ${scenes.length}`;
  $('previous').disabled=index===0;$('next').disabled=index===scenes.length-1;controls();draw();
}
function go(i){index=Math.max(0,Math.min(scenes.length-1,i));history.replaceState(null,'',`#${current().id}`);render();window.scrollTo({top:0,left:0,behavior:'auto'});}
function fromHash(){const id=aliases[location.hash.slice(1)]||location.hash.slice(1);const found=scenes.findIndex(scene=>scene.id===id);index=found<0?0:found;render();window.scrollTo({top:0,left:0,behavior:'auto'});}
$('scenes').onchange=e=>go(scenes.findIndex(scene=>scene.id===e.target.value));$('previous').onclick=()=>go(index-1);$('next').onclick=()=>go(index+1);
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('viewer').requestFullscreen();}catch{$('status').textContent='Full screen is unavailable in this browser view.';}};
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen';});
window.addEventListener('keydown',e=>{if(e.altKey||e.ctrlKey||e.metaKey||e.target.closest('button,select,input,textarea,a,[contenteditable]'))return;if(['ArrowRight','PageDown'].includes(e.key)){e.preventDefault();go(index+1);}if(['ArrowLeft','PageUp'].includes(e.key)){e.preventDefault();go(index-1);}if(e.key.toLowerCase()==='r')reveal();if(e.key.toLowerCase()==='f'&&teaching)$('fullscreen').click();});
window.addEventListener('hashchange',fromHash);matchMedia('(max-width:600px)').addEventListener('change',draw);fromHash();
