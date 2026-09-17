import test from 'node:test';
import assert from 'node:assert/strict';
import { PRESENTER_PROTOCOL, previewURL, requestedPreview, isPresenterMessage, slideSelection } from '../course/prototypes/presenter-model.js';
import { installPresenter } from '../course/prototypes/presenter-bridge.js';
import { readFileSync } from 'node:fs';
import vm from 'node:vm';

test('one-slide preview preserves the source and public route without mutating the audience URL', () => {
  for (const path of ['/course/prototypes/workload-format.html', '/gigawatt/slides/workloads.html', '/course/sample.html']) {
    const original = `https://example.test${path}?teach=1#current`;
    const result = new URL(previewURL(original, 3));
    assert.equal(result.pathname, path);
    assert.equal(result.searchParams.get('teach'), '1');
    assert.equal(result.searchParams.get('presenter-preview'), '3');
    assert.equal(result.hash, '#current');
    assert.equal(new URL(original).searchParams.has('presenter-preview'), false);
  }
});

test('preview instructions only operate inside a frame and require a whole valid index', () => {
  const url = 'https://example.test/slides/primer.html';
  assert.equal(requestedPreview(previewURL(url, 0), true), 0);
  assert.equal(requestedPreview(previewURL(url, 12), true), 12);
  assert.equal(requestedPreview(previewURL(url, 12), false), null);
  assert.equal(requestedPreview(url, true), null);
  for (const value of ['-1','1.2','NaN','Infinity','', '0x10', '999999999999999999999']) assert.equal(requestedPreview(`${url}?presenter-preview=${value}`, true), null);
  for (const index of [-1, 1.5, NaN, Infinity, Number.MAX_SAFE_INTEGER + 1]) assert.throws(() => previewURL(url, index));
  assert.throws(() => previewURL('javascript:alert(1)', 1));
});

test('presenter commands require the exact window, origin, session and protocol', () => {
  const peer = {}, origin = 'https://example.test', session = 'session-a';
  const event = { source: peer, origin, data: { protocol: PRESENTER_PROTOCOL, session, type: 'navigate', index: 3 } };
  assert.equal(isPresenterMessage(event, peer, origin, session), true);
  assert.equal(isPresenterMessage({ ...event, source: {} }, peer, origin, session), false);
  assert.equal(isPresenterMessage({ ...event, origin: 'https://other.test' }, peer, origin, session), false);
  assert.equal(isPresenterMessage({ ...event, data: { ...event.data, session: 'another-session' } }, peer, origin, session), false);
  assert.equal(isPresenterMessage({ ...event, data: { ...event.data, protocol: 'another-protocol' } }, peer, origin, session), false);
  assert.equal(isPresenterMessage({ ...event, data: null }, peer, origin, session), false);
  assert.equal(isPresenterMessage(event, null, origin, session), false);
});

test('selection reads the live shared selector, including a replaced UPS selector or adapted numbered steps', () => {
  let select = { selectedIndex: 0, options: [{ textContent: '1 · Opening' }, { textContent: '2 · Mechanism' }] };
  const doc = { querySelector: () => select };
  assert.deepEqual(slideSelection(doc), { index: 0, slides: ['1 · Opening', '2 · Mechanism'] });
  select = { selectedIndex: 1, options: [{ textContent: '1. Question' }, { textContent: '2. Explanation' }] };
  assert.deepEqual(slideSelection(doc), { index: 1, slides: ['1. Question', '2. Explanation'] });
  select = null;
  assert.equal(slideSelection(doc), null);
});

function audienceFixture({ preview = null, populated = true } = {}) {
  const handlers = new Map(), pending = new Map(), intervals = new Map(), observers = [], messages = [];
  let timer = 0, button, currentSelect = { selectedIndex: 0, options: [{ textContent: '1 · Opening' }, { textContent: '2 · Mechanism' }], dispatchEvent() {} };
  if (!populated) currentSelect.options = [];
  const root = { addEventListener() {}, cloneNode() { throw new Error('The upcoming-slide window must not copy audience DOM'); } };
  const footer = {}, head = {};
  const nav = { querySelector: () => button || null, append: element => { button = element; } };
  const doc = {
    title: 'Example chapter', documentElement: { dataset: {} },
    getElementById: id => id === 'viewer' ? root : null,
    querySelector: selector => selector === '.toolbar nav' ? nav
      : selector === 'footer.course-slide-navigation select' ? currentSelect
      : selector === 'footer.course-slide-navigation' ? footer
      : selector === 'head' ? head : null,
    createElement: () => ({
      addEventListener(type, handler) { this[type] = handler; },
      setAttribute() {}, removeAttribute() {},
    }),
  };
  const win = {
    location: new URL(`https://example.test/slides/workloads.html?teach=1${preview === null ? '' : `&presenter-preview=${preview}`}#opening`),
    sessionStorage: { getItem: () => 'test-session', setItem() {} },
    crypto: { randomUUID: () => 'test-session' },
    Event: class { constructor(type, options) { this.type = type; Object.assign(this, options); } },
    MutationObserver: class {
      constructor(callback) { this.callback = callback; observers.push(this); }
      observe(target) { this.target = target; }
      disconnect() { this.disconnected = true; }
    },
    addEventListener: (type, handler) => handlers.set(type, handler),
    setTimeout: callback => { pending.set(++timer, callback); return timer; },
    clearTimeout: id => pending.delete(id),
    setInterval: callback => { intervals.set(++timer, callback); return timer; },
    clearInterval: id => intervals.delete(id),
  };
  win.parent = preview === null ? win : {};
  const peer = { opener: win, closed: false, focus() {}, postMessage: data => messages.push(data) };
  win.open = href => { peer.location = new URL(href); return peer; };
  const send = data => handlers.get('message')?.({ origin: win.location.origin, source: peer,
    data: { protocol: PRESENTER_PROTOCOL, session: 'test-session', ...data } });
  const flush = () => { const callbacks = [...pending.values()]; pending.clear(); callbacks.forEach(callback => callback()); };
  return { doc, win, peer, messages, handlers, observers, intervals, head, send, flush,
    get button() { return button; }, get select() { return currentSelect; },
    set select(value) { currentSelect = value; },
  };
}

test('audience bridge sends navigation metadata, forwards navigation and reconnects without copying slide DOM', () => {
  const fixture = audienceFixture();
  installPresenter(fixture.doc, fixture.win);
  fixture.button.click(); fixture.send({ type: 'hello' });
  let snapshot = fixture.messages.at(-1);
  assert.deepEqual(Object.keys(snapshot).sort(), ['protocol','session','type','index','slides','title','href','nextChapter'].sort());
  assert.equal(snapshot.index, 0);
  let changes = 0;
  fixture.select.dispatchEvent = event => { if (event.type === 'change') changes++; };
  fixture.send({ type: 'navigate', index: 1 }); fixture.flush();
  assert.equal(fixture.select.selectedIndex, 1);
  assert.equal(changes, 1);
  assert.equal(fixture.messages.at(-1).index, 1);
  for (const index of [-1, 2, 1.5, '0']) fixture.send({ type: 'navigate', index });
  fixture.flush();
  assert.equal(changes, 1, 'invalid navigation must not change the audience');
  const count = fixture.messages.length;
  fixture.observers.at(-1).callback(); fixture.flush();
  assert.equal(fixture.messages.length, count, 'unchanged navigation state should not produce repeated snapshots');
  fixture.send({ type: 'close' });
  fixture.select = { selectedIndex: 0, options: [{ textContent: '1 · Replacement selector' }], dispatchEvent() {} };
  fixture.send({ type: 'hello' });
  snapshot = fixture.messages.at(-1);
  assert.equal(snapshot.index, 0);
  assert.deepEqual(snapshot.slides, ['1 · Replacement selector']);
});

test('presenter hides audience chrome only while connected and restores it on either close path', () => {
  const fixture = audienceFixture();
  const data = fixture.doc.documentElement.dataset;
  installPresenter(fixture.doc, fixture.win);
  assert.equal(data.presenterActive, undefined);
  fixture.button.click();
  assert.equal(data.presenterActive, undefined, 'opening alone is not a successful connection');
  fixture.send({ type: 'hello' });
  assert.equal(data.presenterActive, '');
  fixture.send({ type: 'close' });
  assert.equal(data.presenterActive, undefined);
  assert.equal(fixture.intervals.size, 0);
  fixture.send({ type: 'hello' });
  assert.equal(data.presenterActive, '', 'reconnection hides chrome again');
  fixture.peer.closed = true;
  for (const tick of fixture.intervals.values()) tick();
  assert.equal(data.presenterActive, undefined, 'window.closed restores chrome even without a close message');
  assert.equal(fixture.intervals.size, 0);
});

test('audience tab stays neutral while private presenter metadata follows slides and restores on exit', () => {
  const fixture = audienceFixture();
  const opening = '10. Networking · Opening';
  fixture.doc.title = opening;
  installPresenter(fixture.doc, fixture.win);
  fixture.button.click();
  assert.equal(fixture.doc.title, opening, 'opening alone must not change the tab title');
  fixture.send({ type: 'hello' });
  assert.equal(fixture.doc.title, 'From Watts to Tokens');
  assert.equal(fixture.messages.at(-1).title, opening);
  const titleObserver = fixture.observers.find(observer => observer.target === fixture.head);
  assert.ok(titleObserver);
  fixture.doc.title = '10. Networking · Campus fiber';
  titleObserver.callback(); fixture.flush();
  assert.equal(fixture.doc.title, 'From Watts to Tokens');
  assert.equal(fixture.messages.at(-1).title, '10. Networking · Campus fiber');
  const messageCount = fixture.messages.length;
  titleObserver.callback(); fixture.flush();
  assert.equal(fixture.messages.length, messageCount, 'neutral-title mutations must not produce loops');
  fixture.send({ type: 'close' });
  assert.equal(fixture.doc.title, '10. Networking · Campus fiber');
  assert.equal(titleObserver.disconnected, true);
  fixture.send({ type: 'hello' });
  assert.equal(fixture.doc.title, 'From Watts to Tokens');
  fixture.doc.title = '10. Networking · Distance';
  fixture.peer.closed = true;
  for (const tick of fixture.intervals.values()) tick();
  assert.equal(fixture.doc.title, '10. Networking · Distance', 'closing before a title callback preserves the latest renderer title');
});

test('blocked presenter popup leaves audience controls available', () => {
  const fixture = audienceFixture();
  fixture.win.open = () => null;
  installPresenter(fixture.doc, fixture.win);
  fixture.button.click();
  assert.equal(fixture.doc.documentElement.dataset.presenterActive, undefined);
  assert.equal(fixture.button.textContent, 'Allow presenter popup');
});

test('preview initialization waits for module decks to populate the live selector', () => {
  const fixture = audienceFixture({ preview: 5, populated: false });
  installPresenter(fixture.doc, fixture.win);
  assert.equal(fixture.button, undefined);
  assert.equal(fixture.observers.length, 1);
  let changed = false;
  fixture.select = { selectedIndex: 0, options: [{ textContent: '1 · Opening' }, { textContent: '2 · Mechanism' }], dispatchEvent: () => { changed = true; } };
  fixture.observers[0].callback();
  assert.equal(fixture.observers[0].disconnected, true);
  assert.equal(fixture.doc.documentElement.dataset.presenterPreview, '');
  assert.equal(fixture.select.selectedIndex, 1, 'preview index clamps to the deck rather than selecting a missing slide');
  assert.equal(changed, true);
  assert.equal(fixture.button, undefined, 'the upcoming slide must not launch another presenter');
});

test('separate presenter displays the upcoming slide and its controls advance the audience', () => {
  const messages = [], handlers = new Map();
  const elements = Object.fromEntries(['preview','connection','slides','previous','next','progress','end','exit-presenter','chapter'].map(id => [id, {
    hidden: false, options: [], setAttribute(name, value) { this[name] = value; },
    replaceChildren(...options) { this.options = options; },
  }]));
  const audience = { closed: false, focus() {}, postMessage: data => messages.push(data) };
  const context = {
    document: { getElementById: id => elements[id] },
    window: { opener: audience, addEventListener: (type, handler) => handlers.set(type, handler), setInterval() {}, clearInterval() {}, close() {} },
    location: { origin: 'https://example.test', hash: '#test-session' },
    Option: function (text, value) { this.textContent = text; this.value = value; },
    PRESENTER_PROTOCOL, isPresenterMessage, previewURL,
  };
  const source = readFileSync(new URL('../course/prototypes/presenter-window.js', import.meta.url), 'utf8').replace(/^import .*;\n/, '');
  vm.runInNewContext(source, context);
  const receive = data => handlers.get('message')({ source: audience, origin: context.location.origin,
    data: { protocol: PRESENTER_PROTOCOL, session: 'test-session', ...data } });
  const state = { type: 'snapshot', title: '3. Workloads and requirements · Opening · From Watts to Tokens', href: 'https://example.test/slides/workloads.html?teach=1#opening',
    index: 0, slides: ['1 · Opening', '2 · Mechanism', '3 · Close'], nextChapter: null };
  receive(state);
  assert.equal(new URL(elements.preview.src).searchParams.get('presenter-preview'), '1');
  assert.equal(elements.progress.textContent, 'Up next: 2 / 3');
  assert.equal(elements.chapter.textContent, '3. Workloads and requirements');
  assert.equal(elements.chapter.hidden, false);
  assert.equal(elements.slides.selectedIndex, 0, 'the selector identifies the audience slide, not the preview');
  elements.next.onclick();
  assert.equal(messages.at(-1).type, 'navigate'); assert.equal(messages.at(-1).index, 1);
  receive({ ...state, index: 1 });
  assert.equal(new URL(elements.preview.src).searchParams.get('presenter-preview'), '2');
  receive({ ...state, index: 2, nextChapter: 'Next chapter →' });
  assert.equal(elements.preview.hidden, true); assert.equal(elements.preview.src, 'about:blank');
  assert.equal(elements.end.hidden, false); assert.equal(elements.next.disabled, false);
  elements.next.onclick(); assert.equal(messages.at(-1).type, 'next-chapter');
  receive({ ...state, index: 2 });
  assert.equal(elements.next.disabled, true);
  receive({ type: 'disconnect' });
  assert.equal(elements.slides.disabled, true);
  receive({ ...state, title: '4. Siting, grid connection and supply · From Watts to Tokens', href: 'https://example.test/slides/siting.html?teach=1', index: 0 });
  assert.equal(elements.chapter.textContent, '4. Siting, grid connection and supply', 'the label follows the audience across chapter navigation');
});

test('Exit presenter restores audience chrome without changing slides or reconnecting from delayed callbacks', () => {
  const fixture = audienceFixture();
  const handlers = new Map(), intervals = new Map(), commands = [];
  let timer = 0, focusCalls = 0, closeCalls = 0;
  const elements = Object.fromEntries(['preview','connection','slides','previous','next','progress','end','exit-presenter','chapter'].map(id => [id, {
    hidden: false, options: [], setAttribute(name, value) { this[name] = value; },
    replaceChildren(...options) { this.options = options; },
  }]));
  fixture.win.focus = () => { focusCalls++; };
  fixture.win.postMessage = data => { commands.push(data); fixture.send(data); };
  const receive = data => handlers.get('message')?.({ source: fixture.win, origin: fixture.win.location.origin, data });
  fixture.peer.postMessage = data => { fixture.messages.push(data); receive(data); };
  const context = {
    document: { getElementById: id => elements[id] },
    window: {
      opener: fixture.win,
      addEventListener: (type, handler) => handlers.set(type, handler),
      setInterval: callback => { intervals.set(++timer, callback); return timer; },
      clearInterval: id => intervals.delete(id),
      // Keep the simulated window alive so delayed callbacks can still run after a close request.
      close: () => { closeCalls++; },
    },
    location: { origin: fixture.win.location.origin, hash: '#test-session' },
    Option: function (text, value) { this.textContent = text; this.value = value; },
    PRESENTER_PROTOCOL, isPresenterMessage, previewURL,
  };
  installPresenter(fixture.doc, fixture.win);
  fixture.button.click();
  const source = readFileSync(new URL('../course/prototypes/presenter-window.js', import.meta.url), 'utf8').replace(/^import .*;\n/, '');
  vm.runInNewContext(source, context);
  assert.equal(fixture.doc.documentElement.dataset.presenterActive, '');
  assert.equal(elements.slides.disabled, false);
  assert.equal(intervals.size, 1);
  const pendingHeartbeat = [...intervals.values()][0];
  const pendingSnapshot = fixture.messages.find(message => message.type === 'snapshot');
  const currentIndex = fixture.select.selectedIndex;
  const currentURL = fixture.win.location.href;

  elements['exit-presenter'].onclick();

  assert.equal(commands.at(-1).type, 'close');
  assert.equal(fixture.doc.documentElement.dataset.presenterActive, undefined);
  assert.equal(fixture.intervals.size, 0);
  assert.equal(intervals.size, 0, 'the presenter heartbeat must stop');
  assert.equal(focusCalls, 1);
  assert.equal(closeCalls, 1);
  assert.equal(fixture.select.selectedIndex, currentIndex);
  assert.equal(fixture.win.location.href, currentURL);
  for (const id of ['slides','previous','next']) assert.equal(elements[id].disabled, true);

  const commandCount = commands.length;
  pendingHeartbeat();
  receive(pendingSnapshot);
  receive({ protocol: PRESENTER_PROTOCOL, session: 'test-session', type: 'connected' });
  elements.next.onclick();
  assert.equal(commands.length, commandCount, 'delayed callbacks must not send hello or navigate after exit');
  assert.equal(fixture.doc.documentElement.dataset.presenterActive, undefined);
  assert.equal(elements.slides.disabled, true, 'a late snapshot must not re-enable presenter navigation');
  assert.equal(fixture.select.selectedIndex, currentIndex);
});
