import { PRESENTER_PROTOCOL, isPresenterMessage, previewURL } from './presenter-model.js';
import { applyPresenterScroll } from './presenter-bridge.js';
const $ = id => document.getElementById(id);
const audience = window.opener, origin = location.origin, session = location.hash.slice(1);
let current = null, lastSeen = 0, connected = false, headKey = '', previewKey = '';
let editing = false, pendingMirror = null;
let mirrorHTML = '', mirroredSnapshot = null;
const expectedScroll = new WeakMap();
const currentFrame = $('current'), previewFrame = $('preview');
const post = data => {
  if (audience && !audience.closed) audience.postMessage({ protocol: PRESENTER_PROTOCOL, session, ...data }, origin);
};
function status(message) {
  $('connection').hidden = !message;
  $('connection').textContent = message || '';
  connected = !message;
  $('slides').disabled = !connected;
  $('previous').disabled = !connected || !current || current.index === 0;
  $('next').disabled = !connected || !current || (current.index === current.slides.length - 1 && !current.nextChapter);
}
function fit(frame, shell) {
  if (!current) return;
  const scale = Math.min(shell.clientWidth/current.width, shell.clientHeight/current.height);
  frame.style.width = `${current.width}px`; frame.style.height = `${current.height}px`;
  frame.style.transform = `translate(${(shell.clientWidth-current.width*scale)/2}px, ${(shell.clientHeight-current.height*scale)/2}px) scale(${scale})`;
}
function layout() { fit(currentFrame, $('current-shell')); fit(previewFrame, $('next-shell')); }
function navigation(index) { if (connected && current && index >= 0 && index < current.slides.length) post({ type: 'navigate', index }); }
function forward() {
  if (!connected || !current) return;
  if (current.index < current.slides.length-1) navigation(current.index+1);
  else if (current.nextChapter) post({ type: 'next-chapter' });
}
function keydown(event) {
  if (event.altKey || event.metaKey || event.ctrlKey || event.target.closest('button,select,input,textarea,a,[contenteditable]')) return;
  const action = { ArrowRight: forward, PageDown: forward, ' ': forward,
    ArrowLeft: () => navigation(current.index-1), PageUp: () => navigation(current.index-1),
    Home: () => navigation(0), End: () => navigation(current.slides.length-1),
  }[event.key];
  if (action && current && connected) { event.preventDefault(); action(); }
}
function installMirrorEvents(doc) {
  doc.addEventListener('scroll', event => {
    if (!connected || !mirroredSnapshot) return;
    const target = event.target === doc ? doc.defaultView : event.target;
    const node = target === doc.defaultView ? null : target.dataset?.presenterNode;
    if (node === undefined) return;
    const position = target === doc.defaultView
      ? { left: target.scrollX, top: target.scrollY }
      : { left: target.scrollLeft, top: target.scrollTop };
    const expected = expectedScroll.get(target);
    // Applying an audience snapshot also emits scroll events. Do not echo those.
    if (expected && Math.abs(position.left - expected.left) < .5 && Math.abs(position.top - expected.top) < .5) return;
    expectedScroll.set(target, position);
    post({ type: 'action', kind: 'scroll', node, ...position, href: mirroredSnapshot.href });
  }, { capture: true, passive: true });
  // Photos and styles can finish loading after the first position was clamped.
  doc.addEventListener('load', () => {
    if (doc === currentFrame.contentDocument && mirroredSnapshot) restoreScroll(doc, mirroredSnapshot);
  }, true);
  doc.addEventListener('pointerdown', event => {
    if (event.target.matches('input,textarea,select')) editing = true;
  }, true);
  doc.addEventListener('pointerup', finishEditing, true);
  doc.addEventListener('pointercancel', finishEditing, true);
  doc.addEventListener('compositionstart', () => { editing = true; }, true);
  doc.addEventListener('compositionend', finishEditing, true);
  doc.addEventListener('click', event => {
    const target = event.target.closest('[data-presenter-node]');
    if (!target) return;
    const control = target.closest('button,a,input,select,textarea') || target;
    if (control.matches('select,textarea,input:not([type="checkbox"]):not([type="radio"]):not([type="button"]):not([type="submit"])')) return;
    event.preventDefault();
    if (connected) post({ type: 'action', kind: 'click', node: control.dataset.presenterNode });
  }, true);
  for (const kind of ['input', 'change']) doc.addEventListener(kind, event => {
    const control = event.target;
    if (!connected || !control.matches('input,select,textarea') || control.matches('[type="checkbox"],[type="radio"]')) return;
    post({ type: 'action', kind, node: control.dataset.presenterNode, value: control.value, index: control.selectedIndex });
  }, true);
  doc.addEventListener('keydown', keydown);
}
function restoreScroll(doc, snapshot) {
  const restore = (target, position) => {
    if (!applyPresenterScroll(target, position)) return;
    expectedScroll.set(target, target === doc.defaultView
      ? { left: target.scrollX, top: target.scrollY }
      : { left: target.scrollLeft, top: target.scrollTop });
  };
  restore(doc.defaultView, { left: snapshot.scrollX, top: snapshot.scrollY });
  for (const position of snapshot.scrollPositions || []) {
    restore(doc.querySelector(`[data-presenter-node="${position.node}"]`), position);
  }
}
function finishEditing() {
  editing = false;
  if (pendingMirror) {
    const snapshot = pendingMirror;
    pendingMirror = null;
    // Native controls finish their own pointer/change processing first.
    queueMicrotask(() => mirror(snapshot));
  }
}
function mirror(snapshot) {
  if (editing) { pendingMirror = snapshot; return; }
  const doc = currentFrame.contentDocument;
  const key = `${snapshot.href.split('#')[0]}\n${snapshot.styles}`;
  if (headKey !== key || !doc.body) {
    doc.open(); doc.write('<!doctype html><html><head></head><body></body></html>'); doc.close();
    const base = doc.createElement('base'); base.href = snapshot.href; doc.head.append(base);
    doc.head.insertAdjacentHTML('beforeend', snapshot.styles);
    const style = doc.createElement('style');
    style.textContent = '.toolbar,footer.course-slide-navigation{visibility:hidden!important}body{pointer-events:auto}';
    doc.head.append(style); installMirrorEvents(doc); headKey = key; mirrorHTML = '';
  }
  doc.body.className = snapshot.bodyClass;
  // Scrolling changes no HTML. Keep those nodes alive so trackpad momentum and
  // the scrollbar drag survive the audience's acknowledgement.
  if (mirrorHTML !== snapshot.html) {
    const focused = doc.activeElement?.dataset.presenterNode;
    const selection = ['selectionStart','selectionEnd'].map(key => doc.activeElement?.[key]);
    doc.body.innerHTML = snapshot.html;
    mirrorHTML = snapshot.html;
    if (focused) {
      const replacement = doc.querySelector(`[data-presenter-node="${focused}"]`);
      replacement?.focus({ preventScroll: true });
      if (replacement?.setSelectionRange && selection.every(Number.isInteger)) replacement.setSelectionRange(...selection);
    }
  }
  mirroredSnapshot = snapshot;
  restoreScroll(doc, snapshot);
}
function update(snapshot) {
  current = snapshot; lastSeen = Date.now();
  document.title = `Presenter · ${snapshot.title}`;
  // Size the mirror before restoring positions; the default iframe is 300×150.
  layout();
  mirror(snapshot);
  const select = $('slides');
  if (select.options.length !== snapshot.slides.length || snapshot.slides.some((label,index) => select.options[index]?.textContent !== label)) {
    select.replaceChildren(...snapshot.slides.map((label,index) => new Option(label, String(index))));
  }
  select.selectedIndex = snapshot.index;
  $('progress').textContent = `${snapshot.index+1} / ${snapshot.slides.length}`;
  const last = snapshot.index === snapshot.slides.length-1;
  $('next').textContent = last && snapshot.nextChapter ? 'Next chapter →' : '→';
  $('next').setAttribute('aria-label', last && snapshot.nextChapter ? 'Next chapter' : 'Next slide');
  $('end').hidden = !last;
  previewFrame.hidden = last;
  $('next-title').textContent = last ? '' : snapshot.slides[snapshot.index+1];
  if (last) { if (previewKey) { previewFrame.src = 'about:blank'; previewKey = ''; } }
  else {
    const url = previewURL(snapshot.href, snapshot.index+1);
    if (previewKey !== url) { previewFrame.src = url; previewKey = url; }
  }
  layout(); status('');
}
window.addEventListener('message', event => {
  if (!isPresenterMessage(event, audience, origin, session)) return;
  if (event.data.type === 'snapshot') update(event.data);
  else if (event.data.type === 'connected') { lastSeen = Date.now(); if (current) status(''); }
  else if (event.data.type === 'disconnect') status('Waiting for the course window…');
});
$('previous').onclick = () => navigation(current.index-1);
$('next').onclick = forward;
$('slides').onchange = event => navigation(event.target.selectedIndex);
window.addEventListener('keydown', keydown);
window.addEventListener('pointerup', finishEditing, true);
window.addEventListener('pointercancel', finishEditing, true);
window.addEventListener('blur', finishEditing);
window.addEventListener('resize', layout);
window.addEventListener('pagehide', () => post({ type: 'close' }));
new ResizeObserver(layout).observe($('current-shell'));
const hello = () => {
  if (!audience || audience.closed) { status('The course window is closed.'); return; }
  post({ type: 'hello' });
  if (lastSeen && Date.now()-lastSeen > 3500) status('Waiting for the course window…');
};
hello(); window.setInterval(hello, 1000);
