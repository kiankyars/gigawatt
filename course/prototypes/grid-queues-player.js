import {scenes,sceneAliases} from './grid-queues-scenes.js';
import {gridQueuesVisual} from './grid-queues-visuals.js';
import {presentationLabels} from './teaching-navigation.js';
const $=id=>document.getElementById(id);
const teaching=new URLSearchParams(location.search).get('teach')==='1';
let index=0;
for(const [i,scene]of scenes.entries())$('scenes').add(new Option(`${i+1} · ${scene.label}`,scene.id));
$('fullscreen').hidden=!teaching;
function render(){
 const scene=scenes[index];
 document.title=`${presentationLabels['grid-queues']||'17. ERCOT and PJM: the race to connect'} · ${scene.label}`;
 $('scene').dataset.scene=scene.id;$('scene-title').textContent=scene.title;
 $('visual').innerHTML=gridQueuesVisual(scene.id);
 $('lesson-reference').href=`../index.html#${scene.reference}`;
 $('status').textContent=scene.title;$('scenes').value=scene.id;$('progress').textContent=`${index+1} / ${scenes.length}`;
 $('previous').disabled=index===0;$('next').disabled=index===scenes.length-1;
}
function go(i){index=Math.max(0,Math.min(scenes.length-1,i));history.replaceState(null,'',`#${scenes[index].id}`);render();window.scrollTo({top:0,left:0,behavior:'auto'});}
function fromHash(){const id=location.hash.slice(1),found=scenes.findIndex(scene=>scene.id===(sceneAliases[id]||id));index=found<0?0:found;render();window.scrollTo({top:0,left:0,behavior:'auto'});}
$('scenes').onchange=event=>go(scenes.findIndex(scene=>scene.id===event.target.value));$('previous').onclick=()=>go(index-1);$('next').onclick=()=>go(index+1);
$('fullscreen').onclick=async()=>{try{if(document.fullscreenElement)await document.exitFullscreen();else await $('viewer').requestFullscreen();}catch{$('status').textContent='Full screen is unavailable in this browser view.';}};
document.addEventListener('fullscreenchange',()=>{$('fullscreen').textContent=document.fullscreenElement?'Exit full screen':'Full screen';});
window.addEventListener('keydown',event=>{if(event.altKey||event.ctrlKey||event.metaKey||event.target.closest('button,select,input,textarea,a,[contenteditable]'))return;if(['ArrowRight','PageDown'].includes(event.key)){event.preventDefault();go(index+1);}if(['ArrowLeft','PageUp'].includes(event.key)){event.preventDefault();go(index-1);}if(event.key.toLowerCase()==='f'&&teaching)$('fullscreen').click();});
window.addEventListener('hashchange',fromHash);fromHash();
