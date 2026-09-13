import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

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
