import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../course/web/reader.js', import.meta.url), 'utf8');
const directory = source.slice(source.indexOf('function renderContents()'), source.indexOf('function renderGlossary('));

test('chapter directory exposes existing destinations without draft-state classification', () => {
  const lessons = [
    {id:'one', domain:'D01', title:'One lesson'},
    {id:'two', domain:'D02', title:'Another lesson'},
    {id:'reference', domain:'D07', title:'GPU performance depth'},
  ];
  const nodes = Object.fromEntries(['search','lesson-count','search-status','contents'].map(id => [id, {
    value:'', textContent:'', innerHTML:'', querySelectorAll:() => [],
  }]));
  const context = {
    CHAPTERS:[
      {id:'D01-part', number:1, title:'A chapter with slides', lesson_ids:['one'], presentations:[{id:'deck', title:'A topic', coverage:'selected', href:'prototypes/example.html'}]},
      {id:'D02', number:2, title:'A chapter with lessons', lesson_ids:['two'], presentations:[]},
      {id:'case', title:'Case study — an unnumbered deck', additional:true, lesson_ids:[], presentations:[]},
    ],
    LESSONS:lessons, byLesson:new Map(lessons.map((lesson,index) => [lesson.id,index])),
    current:0, lookupMode:false, $:id => nodes[id],
    esc:value => String(value), chapterName:chapter => chapter.number ? `${chapter.number}. ${chapter.title}` : chapter.title,
    renderGlossary:() => {},
  };
  context.READING_GROUPS = [...context.CHAPTERS, {
    id:'D07', title:'Compute and memory — further reading', lesson_ids:['reference'], presentations:[],
  }];
  context.chapterByLesson = new Map(context.READING_GROUPS.flatMap(chapter => chapter.lesson_ids.map(id => [id, chapter])));
  vm.runInNewContext(`${directory}\nrenderContents();`, context);
  const html = nodes.contents.innerHTML;
  assert.equal((html.match(/class="slides-link"/g) || []).length,1);
  assert.match(html, /href="prototypes\/example.html"/);
  assert.match(html, /data-lesson="one"/);
  assert.match(html, /data-chapter="D01-part" open/);
  assert.match(html, /data-lesson="two"/);
  assert.doesNotMatch(html, /Slides available|Selected slides|Selected topics|reading-label|chapter-status|not yet available/);
  assert.match(html, /2\. A chapter with lessons/);
  assert.match(html, /data-lesson="reference"/);
  assert.match(html, /Compute and memory — further reading/);
  assert.doesNotMatch(html, /undefined|NaN/);
  assert.match(html, /Case study — an unnumbered deck/);
  assert.equal(nodes['lesson-count'].textContent, '2 chapters', 'unnumbered case studies are not counted as chapters');
});
