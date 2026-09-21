import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';
import {nextChapterLink} from '../course/prototypes/slide-navigation.js';
import {presentationRoutes} from '../course/prototypes/teaching-navigation.js';

const course = new URL('../course/', import.meta.url);
const catalog = JSON.parse(await readFile(new URL('teaching-sequences.json', course), 'utf8'));
const decks = new Set(catalog.presentations.flatMap(p => p.chapters.map(c => c.href.split(/[?#]/)[0])));
decks.add('sample.html');
decks.add('prototypes/case-studies.html');

test('every published slide deck provides the common navigation component contract', async () => {
  for (const path of decks) {
    const html = await readFile(new URL(path, course), 'utf8');
    assert.match(html, /<script\b[^>]*src="(?:prototypes\/)?slide-chrome\.js"/, path);
    assert.match(html, /<link\b[^>]*href="(?:\.\.\/)?assets\/slide-chrome\.css"/, path);
    const footer = [...html.matchAll(/<footer\b[^>]*>([\s\S]*?)<\/footer>/g)]
      .map(match => match[1]).find(markup => /id="(?:previous|back)"/.test(markup));
    assert.ok(footer, `${path}: a footer contains the previous control`);
    assert.equal([...footer.matchAll(/id="(?:previous|back)"/g)].length, 1, path);
    assert.equal([...footer.matchAll(/id="next"/g)].length, 1, path);
    assert.match(footer, /<(?:select|nav)\b[^>]*id="(?:scenes|sequence|steps)"/, path);
  }
});

test('the generated 800 V template retains the same shared navigation imports', async () => {
  const template = await readFile(new URL('web/presentation.html', course), 'utf8');
  assert.match(template, /src="prototypes\/slide-chrome\.js"/);
  assert.match(template, /href="assets\/slide-chrome\.css"/);
  const chrome = await readFile(new URL('prototypes/slide-chrome.js', course), 'utf8');
  assert.match(chrome, /import \{ installSlideNavigation \} from '\.\/slide-navigation\.js'/);
});

test('source decks advance in curriculum order while retaining teaching mode', () => {
  const module = 'http://localhost:8765/course/prototypes/slide-navigation.js';
  const link = nextChapterLink('http://localhost:8765/course/prototypes/siting-format.html?teach=1#last', presentationRoutes, module);
  assert.equal(link.number, undefined, 'the case study after siting is unnumbered');
  assert.equal(link.href, 'http://localhost:8765/course/prototypes/grid-queues-format.html?teach=1');
  const site = nextChapterLink(link.href, presentationRoutes, module);
  assert.equal(site.number, 5);
  assert.equal(site.href, 'http://localhost:8765/course/prototypes/site-format.html?teach=1');
});

test('student exploration stays outside teaching mode and transient parameters do not leak', () => {
  const module = 'https://example.test/course/prototypes/slide-navigation.js';
  const link = nextChapterLink('https://example.test/course/prototypes/continuity-format.html?debug=1#service-check', presentationRoutes, module);
  assert.equal(link.href, 'https://example.test/course/prototypes/rack-energy-format.html');
  const off = nextChapterLink('https://example.test/course/prototypes/continuity-format.html?teach=0', presentationRoutes, module);
  assert.equal(new URL(off.href).search, '?teach=0');
});

test('outdoor cooling continues to the delivery chapter', () => {
  const module = 'http://localhost/course/prototypes/slide-navigation.js';
  const link = nextChapterLink('http://localhost/course/prototypes/heat-rejection-format.html?teach=1#rejection', presentationRoutes, module);
  assert.equal(link.number, 13);
  assert.equal(link.kind, 'slides');
  assert.equal(link.href, 'http://localhost/course/prototypes/procurement-cases-format.html?teach=1');
});

test('delivery, operations, capacity and capstone remain a continuous slide sequence', () => {
  const module = 'http://localhost/course/prototypes/slide-navigation.js';
  const link = nextChapterLink('http://localhost/course/prototypes/procurement-cases-format.html?teach=1#aws-houdini-prefab', presentationRoutes, module);
  assert.equal(link.number, 14);
  assert.equal(link.kind, 'slides');
  assert.equal(link.href, 'http://localhost/course/prototypes/operations-format.html?teach=1');
  const next = nextChapterLink(link.href, presentationRoutes, module);
  assert.equal(next.number, 15);
  assert.equal(next.kind, 'slides');
  assert.equal(next.href, 'http://localhost/course/prototypes/capacity-format.html?teach=1');
  const last = nextChapterLink(next.href, presentationRoutes, module);
  assert.equal(last.number, 16);
  assert.equal(last.href, 'http://localhost/course/prototypes/integrated-cases-format.html?teach=1');
  assert.equal(nextChapterLink(last.href, presentationRoutes, module), null);
});

test('networking advances directly to cooling after storage retirement', () => {
  const module = 'http://localhost/course/prototypes/slide-navigation.js';
  const cooling = nextChapterLink('http://localhost/course/prototypes/networking-format.html?teach=1#meta-rsc', presentationRoutes, module);
  assert.equal(cooling.number, 11);
  assert.equal(cooling.kind, 'slides');
  assert.equal(cooling.href, 'http://localhost/course/prototypes/cooling-format.html?teach=1');
  assert.ok(!presentationRoutes.some(route=>route.path.includes('storage-format')));
});

test('rack power advances to DC distribution, then networking', () => {
  const module = 'http://localhost/course/prototypes/slide-navigation.js';
  const link = nextChapterLink('http://localhost/course/prototypes/rack-energy-format.html?teach=1#buffer-recharge', presentationRoutes, module);
  assert.equal(link.number, 9);
  assert.equal(link.kind, 'slides');
  assert.equal(link.href, 'http://localhost/course/prototypes/dc-distribution-format.html?teach=1');
  const next = nextChapterLink(link.href, presentationRoutes, module);
  assert.equal(next.number, 10);
  assert.equal(next.href, 'http://localhost/course/prototypes/networking-format.html?teach=1');
});

test('chip heat capture continues into outdoor cooling', () => {
  const module = 'http://localhost/course/prototypes/slide-navigation.js';
  const link = nextChapterLink('http://localhost/course/prototypes/cooling-format.html#cooling-retrofit', presentationRoutes, module);
  assert.equal(link.number, 12);
  assert.equal(link.kind, 'slides');
});

test('published routes resolve under a repository prefix and preserve the next entry fragment', () => {
  const routes = [{path:'one.html', next:{number:2, title:'Two', href:'two.html?teach=1#start', kind:'slides'}}];
  const link = nextChapterLink('https://example.test/gigawatt/slides/one.html?teach=1#last', routes, 'https://example.test/gigawatt/slides/slide-navigation.js');
  assert.equal(link.href, 'https://example.test/gigawatt/slides/two.html?teach=1#start');
});

test('standalone scenes, another origin and a terminal presentation have no false handoff', () => {
  const module = 'https://example.test/slides/slide-navigation.js';
  const routes = [{path:'final.html', next:null}];
  assert.equal(nextChapterLink('https://example.test/slides/final.html', routes, module), null);
  assert.equal(nextChapterLink('https://example.test/slides/case-studies.html', routes, module), null);
  assert.equal(nextChapterLink('https://other.test/slides/final.html', routes, module), null);
});
