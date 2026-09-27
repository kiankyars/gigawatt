import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import vm from 'node:vm';

const source = await readFile(new URL('../course/web/reader.js', import.meta.url), 'utf8');
const directory = source.slice(source.indexOf('function renderContents()'), source.indexOf('function renderGlossary('));

test('chapter directory exposes existing destinations without draft-state classification', () => {
  const lessons = [
    {id:'one', domain:'D01', title:'One lesson'},
    {id:'two', domain:'D02', title:'Another lesson', optional:true},
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
  assert.equal((html.match(/Optional practice/g) || []).length, 1, 'only the optional lesson is labelled');
  assert.doesNotMatch(html, /Slides available|Selected slides|Selected topics|reading-label|chapter-status|not yet available/);
  assert.match(html, /2\. A chapter with lessons/);
  assert.match(html, /data-lesson="reference"/);
  assert.match(html, /Compute and memory — further reading/);
  assert.doesNotMatch(html, /undefined|NaN/);
  assert.match(html, /Case study — an unnumbered deck/);
  assert.equal(nodes['lesson-count'].textContent, '2 chapters', 'unnumbered case studies are not counted as chapters');
});

test('sidebar search matches the words a reader sees, not field names', () => {
  const search = source.slice(source.indexOf('// Search the words a reader can see'), source.indexOf('function presentationLinks('));
  const context = {asList:(value) => Array.isArray(value) ? value : value ? [value] : []};
  const lessonSearchText = vm.runInNewContext(`${search}\nlessonSearchText;`, context);
  const lesson = {
    id:'one', title:'Voltage and distance', summary:'Higher voltage moves power with fewer amperes.',
    question:'Why raise the voltage?', sections:[{heading:'Current', paragraphs:['Loss scales with current squared.']}],
    worked_example:{title:'Two feeders', givens:['10 MW'], steps:['577 A'], result:'75 kW less loss', boundary:'Model boundary'},
    tradeoff:['Insulation costs more.'], failure:[], practice:{question:'Try 30 kV.', answer:'192 A', explanation:['Divide.']},
    takeaway:'Voltage trades current for insulation.', source_notes:[{id:'P01', claim:'Read 2026-09-12'}], domain:'D03',
  };
  const text = lessonSearchText(lesson);
  for (const word of ['voltage', '577 a', 'insulation', '192 a', 'loss scales']) assert.ok(text.includes(word), word);
  for (const word of ['tradeoff', 'worked', 'practice', 'explanation', 'domain', 'read 2026']) assert.ok(!text.includes(word), word);
  assert.equal(lessonSearchText(lesson), text, 'built once per lesson');
  assert.match(source, /matching \$\{visible\.length === 1 \? "chapter" : "chapters"\}/);
});

// A stand-in for the few DOM nodes the reader's render functions touch. Each id
// gets one plain object, so a test can read what a function wrote to it.
function fakeDom(values = {}) {
  const nodes = new Map();
  const node = (id) => {
    if (!nodes.has(id)) nodes.set(id, {
      id, hidden:false, disabled:false, textContent:'', innerHTML:'', value:values[id] ?? '', src:'', alt:'',
      classList:{toggle() {}, add() {}, remove() {}}, closest:(selector) => node(`${id} ${selector}`),
      before() {}, replaceChildren() {}, removeAttribute() {}, addEventListener() {},
      querySelectorAll:() => [], querySelector:() => null,
    });
    return nodes.get(id);
  };
  return node;
}
const esc = (value) => String(value ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'})[c]);
const asList = (value) => Array.isArray(value) ? value : value ? [value] : [];
const prose = (value) => asList(value).map((p) => `<p>${esc(p)}</p>`).join('');
const slice = (start, end) => source.slice(source.indexOf(start), source.indexOf(end, source.indexOf(start)));

test('sources render as a bibliography with dates and claims, never author limits', () => {
  const $ = fakeDom();
  const context = {
    $, esc,
    sourcesById:new Map([['E1', {id:'E1', title:'Electric Power Monthly', url:'https://www.eia.gov/electricity/monthly/', publisher:'EIA', published_on:'2025-01-02', reviewed_on:'2026-09-06', review_status:'page_reviewed'}]]),
  };
  vm.runInNewContext(`${slice('function renderSources(l)', 'function renderDomainCheckin(')}\nrenderSources(lesson);`, {
    ...context,
    lesson:{source_notes:[
      {id:'E1', claim:'Monthly retail sales by sector.', limits:'Author note: PDF fetch returned HTTP 403.'},
      {id:'E1', claim:'Average retail price by state.', limits:'Do not quote the preliminary month.'},
      {id:'missing', claim:'A source outside the catalog.'},
    ]},
  });
  const html = $('evidence').innerHTML;
  assert.match(html, /EIA · Published 2025-01-02 · Reviewed 2026-09-06/);
  assert.match(html, /Monthly retail sales by sector\./);
  assert.match(html, /Average retail price by state\./);
  assert.match(html, /1 source</, 'two claims on one source list the source once');
  assert.doesNotMatch(html, /HTTP 403|Do not quote|review_status|page_reviewed|A source outside the catalog/);
});

test('check-ins continue by the next label and keep drafts per chapter', () => {
  const $ = fakeDom();
  const checkin = (chapter) => ({
    chapter, title:'Where does the power go?', scenario:['A 10 MW hall.'], prompt:'Predict the loss.',
    answer:'About 1%.', explanation:['Current squared.'], bridge:['Next, the room.'],
    next_lesson:'d06-conversion-ledger', next_domain:'D06', next_label:'8. Rack Power',
  });
  const context = {
    $, esc, prose, drafts:new Map(), checkinDrafts:new Map(), current:0, go() {},
    topicTitle:() => 'the next chapter',
    LESSONS:[{id:'d05-protection-and-fault-domains', domain_checkin:checkin('D06')}],
  };
  vm.runInNewContext(`${slice('function saveDrafts()', 'function go(')}\n${slice('function renderDomainCheckin(', 'function renderParcelComparison(')}`, context);
  $('checkin-response').value = 'My prediction for Chapter 8';
  context.saveDrafts();
  context.renderDomainCheckin(checkin('D06'));
  assert.match($('domain-checkin').innerHTML, /id="checkin-continue">Continue to 8\. Rack Power →<\/a>/);
  assert.equal($('checkin-response').value, 'My prediction for Chapter 8', 'the same chapter restores its draft');
  context.renderDomainCheckin(checkin('D06-DC'));
  assert.equal($('checkin-response').value, '', 'another chapter in the same domain starts empty');
  context.renderDomainCheckin({...checkin('D07'), next_label:undefined});
  assert.match($('domain-checkin').innerHTML, /Continue to the next chapter →/);
  context.renderDomainCheckin(null);
  assert.equal($('domain-checkin').hidden, true);
});

test('the lesson footer names the next chapter and optional lessons carry a label', () => {
  const lesson = (id, extra = {}) => ({
    id, domain:'D01', title:id, summary:'', question:'', takeaway:'', objectives:[],
    sections:[{heading:'One', paragraphs:['Text.']}],
    worked_example:{title:'Example', givens:[], steps:[], result:''}, practice:{question:'', answer:'', explanation:[]},
    source_notes:[], ...extra,
  });
  const LESSONS = [lesson('a1'), lesson('a2'), lesson('b1'), lesson('c1', {optional:true}), lesson('r1')];
  const CHAPTERS = [
    {id:'A', number:4, title:'Power Delivery', lesson_ids:['a1', 'a2'], presentations:[]},
    {id:'case', title:'Case study: ERCOT and PJM', lesson_ids:['b1'], presentations:[]},
    {id:'C', number:16, title:'Putting an AI Factory Together', lesson_ids:['c1'], presentations:[]},
  ];
  const REFERENCE_GROUPS = [{id:'R', title:'Compute and memory, further reading', lesson_ids:['r1'], presentations:[]}];
  const chapterByLesson = new Map([...CHAPTERS, ...REFERENCE_GROUPS].flatMap((c) => c.lesson_ids.map((id) => [id, c])));
  const labels = LESSONS.map((_, current) => {
    const $ = fakeDom();
    vm.runInNewContext(`${slice('function renderLesson()', '// Sources render as a bibliography')}\nrenderLesson();`, {
      $, esc, prose, asList, LESSONS, current, REFERENCE_GROUPS, chapterByLesson,
      chapterName:(chapter) => chapter.number ? `${chapter.number}. ${chapter.title}` : chapter.title,
      domainById:new Map(), DATA:{domains:[]}, CASE_STUDY_LINKS:{}, drafts:new Map(), document:{title:''},
      artFor:() => null, presentationLinks:() => '', referenceFigures:() => '',
      renderSources() {}, renderDomainCheckin() {}, renderLab() {}, renderParcelComparison() {},
    });
    return [$('next').textContent, $('optional-label').hidden];
  });
  assert.deepEqual(labels.map(([next]) => next), [
    'Next lesson →',
    'Continue to Case study: ERCOT and PJM →',
    'Continue to 16. Putting an AI Factory Together →',
    'Further reading →',
    'Back to start ↻',
  ]);
  assert.deepEqual(labels.map(([, hidden]) => hidden), [true, true, true, false, true], 'only the optional lesson shows its label');
});

test('the glossary shows an empty state that hands the query to lesson search', () => {
  const $ = fakeDom({'glossary-filter':'  token '});
  const context = {
    $, esc, go() {}, renderContents() {}, openRail() {},
    DATA:{glossary:[{term:'Kilovolt-ampere (kVA)', definition:'Apparent power in thousands of volt-amperes.', lesson:'d04-current-and-rating'}]},
  };
  vm.runInNewContext(`${slice('function renderGlossary()', 'function renderPrimer(')}\nrenderGlossary();`, context);
  assert.match($('glossary').innerHTML, /No glossary entry for “token”/);
  assert.match($('glossary').innerHTML, /data-search-lessons/);
  assert.doesNotMatch($('glossary').innerHTML, /glossary-card/);
  $('glossary-filter').value = 'kva';
  context.renderGlossary();
  assert.match($('glossary').innerHTML, /class="glossary-card"><h2>Kilovolt-ampere \(kVA\)<\/h2>/);
});
