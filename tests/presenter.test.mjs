import test from 'node:test';
import assert from 'node:assert/strict';
import { PRESENTER_PROTOCOL, previewURL, requestedPreview, isPresenterMessage, slideSelection } from '../course/prototypes/presenter-model.js';
import { applyPresenterScroll, clickPresenterElement } from '../course/prototypes/presenter-bridge.js';

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

test('presenter activates SVG links without requiring HTMLElement.click', () => {
  const events = [];
  const win = { MouseEvent: class { constructor(type, options) { this.type = type; Object.assign(this, options); } } };
  const svgLink = { matches: () => true, dispatchEvent: event => events.push(event) };
  assert.doesNotThrow(() => clickPresenterElement(svgLink, win));
  assert.equal(events.length, 1);
  assert.equal(events[0].type, 'click');
  assert.equal(events[0].bubbles, true);
  assert.equal(events[0].cancelable, true);
  assert.equal(events[0].view, win);
  let nativeClicks = 0;
  clickPresenterElement({ matches: () => true, click: () => { nativeClicks++; } }, win);
  assert.equal(nativeClicks, 1, 'HTML controls retain their native activation behavior');
});

test('presenter restores both axes including zero without smooth-scroll feedback', () => {
  const positions = [];
  const target = { scrollTo: position => positions.push(position) };
  assert.equal(applyPresenterScroll(target, { left: 380, top: 125 }), true);
  assert.equal(applyPresenterScroll(target, { left: 0, top: 0 }), true);
  assert.deepEqual(positions, [
    { left: 380, top: 125, behavior: 'instant' },
    { left: 0, top: 0, behavior: 'instant' },
  ]);
  for (const position of [{ left: NaN, top: 0 }, { left: 0, top: Infinity }, { left: '10', top: 0 }]) {
    assert.equal(applyPresenterScroll(target, position), false);
  }
  assert.equal(applyPresenterScroll(null, { left: 0, top: 0 }), false);
  assert.equal(positions.length, 2, 'invalid messages must not move the audience');
});
