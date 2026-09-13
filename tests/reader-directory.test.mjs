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
  ];
  const nodes = Object.fromEntries(['search','lesson-count','search-status','contents'].map(id => [id, {
    value:'', textContent:'', innerHTML:'', querySelectorAll:() => [],
  }]));
  const context = {
    CHAPTERS:[
      {id:'D01', number:1, title:'A chapter with slides', lesson_ids:['one'], presentations:[{id:'deck', title:'A topic', coverage:'selected', href:'prototypes/example.html'}]},
      {id:'D02', number:2, title:'A chapter with lessons', lesson_ids:['two'], presentations:[]},
    ],
    LESSONS:lessons, byLesson:new Map(lessons.map((lesson,index) => [lesson.id,index])),
    current:0, lookupMode:false, $:id => nodes[id],
    esc:value => String(value), chapterName:chapter => `${chapter.number}. ${chapter.title}`,
    renderGlossary:() => {},
  };
  vm.runInNewContext(`${directory}\nrenderContents();`, context);
  const html = nodes.contents.innerHTML;
  assert.equal((html.match(/class="slides-link"/g) || []).length,1);
  assert.match(html, /href="prototypes\/example.html"/);
  assert.match(html, /data-lesson="one"/);
  assert.match(html, /data-lesson="two"/);
  assert.doesNotMatch(html, /Slides available|Selected slides|Selected topics|reading-label|chapter-status|not yet available/);
  assert.match(html, /2\. A chapter with lessons/);
});
