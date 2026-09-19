import test from 'node:test';
import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
import vm from 'node:vm';
import {SPEAKER_NOTES_URL,parseSpeakerNotes,speakerNoteKey,renderSpeakerNotes} from '../course/prototypes/presenter-notes.js';
import {PRESENTER_PROTOCOL,isPresenterMessage,previewURL,currentSceneId} from '../course/prototypes/presenter-model.js';

const sample='## First\n<!-- speaker: rack-energy#first -->\nRead **this** first.\n\nSources: [TI](https://example.test)\n\n## Last\n<!-- speaker: rack-energy#last -->\nClosing notes.\n';
test('notes markers survive reordered headings and isolate separate scripts within a group',()=>{
  const notes=parseSpeakerNotes(`${sample}\n## Group\n<!-- speaker: cooling#a cooling#b -->\nShared note.\n<!-- speaker: cooling#c -->\nSeparate note.\n## Unmapped\nNot a note.`);
  assert.equal(notes.size,5);
  assert.equal(notes.get('cooling#a'),notes.get('cooling#b'));
  assert.equal(notes.get('cooling#c'),'Separate note.');
  assert.throws(()=>parseSpeakerNotes(`${sample}\n<!-- speaker: rack-energy#first -->\nDuplicate`),/Duplicate/);
  assert.throws(()=>parseSpeakerNotes('<!-- speaker: ../bad -->\nText'),/Invalid/);
  assert.equal(parseSpeakerNotes('<!-- speaker: cooling#empty -->\n\n').size,0);
});
test('notes follow the current stable scene on source and published routes',()=>{
  for(const [source,published,deck] of [['orientation-format','overview','overview'],['rack-energy-format','rack-energy','rack-energy'],['site-format','site-design','site-design'],['dc-distribution-format','dc-distribution','dc-distribution']]){
    for(const path of [`/course/prototypes/${source}.html`,`/gigawatt/slides/${published}.html`]){
      assert.equal(speakerNoteKey({href:`https://example.test${path}?teach=1#old-alias`,sceneId:'current'}),`${deck}#current`);
      assert.equal(speakerNoteKey({href:`https://example.test${path}#current`}),`${deck}#current`);
    }
  }
  assert.equal(speakerNoteKey({href:'https://example.test/slides/cooling.html'}),'');
  const select={selectedIndex:0,options:[{value:'current'}]};
  const doc={querySelector:s=>s.includes('select')?select:null};
  assert.equal(currentSceneId(doc,'https://example.test/'),'current','first slide need not have a hash');
  doc.querySelector=s=>s==='[data-scene]'?{dataset:{scene:'resolved'}}:select;
  assert.equal(currentSceneId(doc,'https://example.test/#old-alias'),'resolved');
});
test('reading view retains emphasis, hides source clutter and never renders raw HTML or links',()=>{
  const html=renderSpeakerNotes('Read **this** [explanation](https://example.test).\n\n<script>bad()</script>\n\nSources: [TI](https://example.test)\n\n- One\n- Two');
  assert.match(html,/<strong>this<\/strong> explanation/);
  assert.match(html,/&lt;script&gt;/);
  assert.match(html,/<ul><li>One<\/li><li>Two<\/li><\/ul>/);
  assert.doesNotMatch(html,/<script|<a\b|https:|Sources:/);
  assert.equal(renderSpeakerNotes('Sources: reference'),'');
});
test('every authored note targets a current slide',async()=>{
  const notes=parseSpeakerNotes(readFileSync(new URL('../course/SPEAKER_NOTES.md',import.meta.url),'utf8'));
  const decks=new Map();
  for(const deck of ['distribution','rack-energy','networking','cooling','heat-rejection','procurement-cases','operations','capacity','integrated-cases']){
    const mod=await import(`../course/prototypes/${deck}-scenes.js`);
    decks.set(deck,new Set(mod.scenes.map(s=>s.id)));
    if(deck==='rack-energy')decks.set('dc-distribution',new Set(mod.dcScenes.map(s=>s.id)));
  }
  const overview=readFileSync(new URL('../course/prototypes/orientation-format.html',import.meta.url),'utf8');
  decks.set('overview',new Set([...overview.matchAll(/id:\s*["']([a-z0-9-]+)["']/g)].map(m=>m[1])));
  assert.ok(notes.size>0);
  for(const [key,body] of notes){const [deck,id]=key.split('#');assert.ok(decks.get(deck)?.has(id),key);assert.ok(renderSpeakerNotes(body),key);}
});

function presenterFixture(){
  let resolveFetch,rejectFetch;
  const loaded=new Promise((resolve,reject)=>{resolveFetch=resolve;rejectFetch=reject;});
  const messages=[],handlers=new Map();
  const ids=['preview','connection','slides','previous','next','progress','end','exit-presenter','chapter','workspace','speaker-notes','notes-content','next-shell','preview-label'];
  const elements=Object.fromEntries(ids.map(id=>[id,{hidden:false,options:[],dataset:{},style:{},innerHTML:'',scrollTop:0,clientWidth:640,clientHeight:600,setAttribute(k,v){this[k]=v;},replaceChildren(...options){this.options=options;}}]));
  const audience={closed:false,focus(){},postMessage:m=>messages.push(m)};
  const context={document:{getElementById:id=>elements[id]},window:{opener:audience,addEventListener:(k,v)=>handlers.set(k,v),setInterval(){},clearInterval(){},close(){}},location:{origin:'https://example.test',hash:'#session'},Option:function(text,value){this.textContent=text;this.value=value;},PRESENTER_PROTOCOL,isPresenterMessage,previewURL,SPEAKER_NOTES_URL,parseSpeakerNotes,speakerNoteKey,renderSpeakerNotes,fetch:()=>loaded};
  const source=readFileSync(new URL('../course/prototypes/presenter-window.js',import.meta.url),'utf8').replace(/^import .*;\n/gm,'');
  vm.runInNewContext(source,context);
  const state={type:'snapshot',title:'8. Rack power · From Watts to Tokens',href:'https://example.test/slides/rack-energy.html?teach=1',index:0,sceneId:'first',slides:['1 · First','2 · No notes','3 · Last'],nextChapter:null};
  const send=(patch={})=>handlers.get('message')({source:audience,origin:context.location.origin,data:{protocol:PRESENTER_PROTOCOL,session:'session',...state,...patch}});
  const settle=()=>new Promise(resolve=>setImmediate(resolve));
  return {elements,messages,handlers,send,settle,resolveFetch:()=>resolveFetch({ok:true,text:()=>sample}),rejectFetch};
}
test('only current-slide notes trigger equal panels; empty slides restore normal preview and scrolling',async()=>{
  const f=presenterFixture(),e=f.elements;
  f.send();f.resolveFetch();await f.settle();
  assert.equal(e.workspace.dataset.notes,'true');assert.equal(e['speaker-notes'].hidden,false);
  assert.match(e['notes-content'].innerHTML,/Read <strong>this/);
  assert.equal(new URL(e.preview.src).searchParams.get('presenter-preview'),'1');
  assert.equal(e.preview.style.width,'1280px','split preview keeps desktop slide layout');
  e['speaker-notes'].scrollTop=80;f.send();assert.equal(e['speaker-notes'].scrollTop,80);
  f.send({index:1,sceneId:'unnoted'});
  assert.equal(e.workspace.dataset.notes,'false');assert.equal(e['speaker-notes'].hidden,true);
  assert.equal(e['notes-content'].innerHTML,'');assert.equal(e.preview.style.width,'');
  assert.equal(new URL(e.preview.src).searchParams.get('presenter-preview'),'2','next-slide notes must not appear early');
  f.send({index:2,sceneId:'last',nextChapter:'Next chapter →'});
  assert.equal(e.workspace.dataset.notes,'true');assert.match(e['notes-content'].innerHTML,/Closing/);
  assert.equal(e.end.hidden,false);assert.equal(e.preview.hidden,true);assert.equal(e.next.disabled,false);
  f.send({index:2,sceneId:'last'});assert.equal(e.next.disabled,true);
  f.send({href:'https://example.test/slides/cooling.html',sceneId:'opening'});
  assert.equal(e.workspace.dataset.notes,'false');assert.equal(e['notes-content'].innerHTML,'');
});
test('late notes resolve against latest navigation, fail safely, and do not render after exit',async()=>{
  const f=presenterFixture();f.send();f.send({index:2,sceneId:'last'});f.resolveFetch();await f.settle();
  assert.match(f.elements['notes-content'].innerHTML,/Closing/);assert.doesNotMatch(f.elements['notes-content'].innerHTML,/Read/);
  const failed=presenterFixture();failed.send();failed.rejectFetch(new Error('offline'));await failed.settle();
  assert.equal(failed.elements.workspace.dataset.notes,'false');assert.equal(failed.elements.next.disabled,false);
  const exited=presenterFixture();exited.send();exited.elements['exit-presenter'].onclick();exited.resolveFetch();await exited.settle();
  assert.equal(exited.elements['notes-content'].innerHTML,'');assert.equal(exited.elements.next.disabled,true);
});
test('page keys can scroll focused notes without advancing the audience',async()=>{
  const f=presenterFixture();f.send();f.resolveFetch();await f.settle();const count=f.messages.length;
  f.handlers.get('keydown')({key:'PageDown',target:{closest:s=>s==='#speaker-notes'},preventDefault(){assert.fail('notes scrolling should remain native');}});
  assert.equal(f.messages.length,count);
});
