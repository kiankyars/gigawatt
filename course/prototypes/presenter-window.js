import { PRESENTER_PROTOCOL, isPresenterMessage, previewURL } from './presenter-model.js?v=notes-20260919';
import { SPEAKER_NOTES_URL, parseSpeakerNotes, speakerNoteKey, renderSpeakerNotes } from './presenter-notes.js';
const $ = id => document.getElementById(id);
const audience = window.opener, origin = location.origin, session = location.hash.slice(1);
let current = null, lastSeen = 0, connected = false, previewKey = '', exited = false;
const previewFrame = $('preview');
let speakerNotes = new Map(), activeNote = '', renderedNote = '';
function fitPreview() {
  const style = previewFrame.style;
  if ($('workspace').dataset.notes !== 'true') {
    for (const key of ['width','height','left','top','transform']) style[key] = '';
    return;
  }
  const shell = $('next-shell');
  const scale = Math.min(shell.clientWidth / 1280, shell.clientHeight / 720);
  Object.assign(style, {width:'1280px', height:'720px', left:`${(shell.clientWidth - 1280 * scale) / 2}px`, top:`${(shell.clientHeight - 720 * scale) / 2}px`, transform:`scale(${scale})`});
}
function updateNotes() {
  const key = speakerNoteKey(current);
  const html = renderSpeakerNotes(speakerNotes.get(key) || '');
  const hasNotes = !!html;
  $('workspace').dataset.notes = String(hasNotes);
  $('speaker-notes').hidden = !hasNotes;
  $('preview-label').textContent = hasNotes ? 'Current notes + next slide' : 'Up next';
  if (activeNote !== key || renderedNote !== html) {
    $('notes-content').innerHTML = html;
    $('speaker-notes').scrollTop = 0;
  }
  activeNote = key; renderedNote = html;
  fitPreview();
}

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
function navigation(index) {
  if (connected && current && index >= 0 && index < current.slides.length) post({ type: 'navigate', index });
}
function forward() {
  if (!connected || !current) return;
  if (current.index < current.slides.length - 1) navigation(current.index + 1);
  else if (current.nextChapter) post({ type: 'next-chapter' });
}
function keydown(event) {
  if (!connected || !current || event.altKey || event.metaKey || event.ctrlKey
      || event.target.closest('button,select,input,textarea,a,[contenteditable]')) return;
  if (event.target.closest('#speaker-notes') && [' ', 'PageDown', 'PageUp', 'Home', 'End'].includes(event.key)) return;
  const action = {
    ArrowRight: forward, PageDown: forward, ' ': forward,
    ArrowLeft: () => navigation(current.index - 1), PageUp: () => navigation(current.index - 1),
    Home: () => navigation(0), End: () => navigation(current.slides.length - 1),
  }[event.key];
  if (action) { event.preventDefault(); action(); }
}
function update(snapshot) {
  current = snapshot; lastSeen = Date.now();
  updateNotes();
  document.title = `Up next · ${snapshot.title}`;
  $('chapter').textContent = snapshot.title.split(' · ')[0].trim();
  $('chapter').hidden = false;
  const select = $('slides');
  if (select.options.length !== snapshot.slides.length || snapshot.slides.some((label, index) => select.options[index]?.textContent !== label)) {
    select.replaceChildren(...snapshot.slides.map((label, index) => new Option(label, String(index))));
  }
  select.selectedIndex = snapshot.index;
  const last = snapshot.index === snapshot.slides.length - 1;
  $('progress').textContent = last ? 'End of chapter' : `Up next: ${snapshot.index + 2} / ${snapshot.slides.length}`;
  $('next').textContent = last && snapshot.nextChapter ? 'Next chapter →' : '→';
  $('next').setAttribute('aria-label', last && snapshot.nextChapter ? 'Next chapter' : 'Next slide');
  $('end').hidden = !last;
  previewFrame.hidden = last;
  if (last) {
    if (previewKey) { previewFrame.src = 'about:blank'; previewKey = ''; }
  } else {
    const url = previewURL(snapshot.href, snapshot.index + 1);
    if (previewKey !== url) { previewFrame.src = url; previewKey = url; }
  }
  status('');
}
window.addEventListener('message', event => {
  if (exited || !isPresenterMessage(event, audience, origin, session)) return;
  if (event.data.type === 'snapshot') update(event.data);
  else if (event.data.type === 'connected') { lastSeen = Date.now(); if (current) status(''); }
  else if (event.data.type === 'disconnect') status('Waiting for the course window…');
});
$('previous').onclick = () => navigation(current.index - 1);
$('next').onclick = forward;
$('slides').onchange = event => navigation(event.target.selectedIndex);
$('exit-presenter').onclick = () => {
  if (exited) return;
  exited = true;
  window.clearInterval(heartbeat);
  post({ type: 'close' });
  status('Presenter ended. You can close this window.');
  if (audience && !audience.closed) audience.focus();
  window.close();
};
window.addEventListener('keydown', keydown);
window.addEventListener('pagehide', () => post({ type: 'close' }));
const hello = () => {
  if (exited) return;
  if (!audience || audience.closed) { status('The course window is closed.'); return; }
  post({ type: 'hello' });
  if (lastSeen && Date.now() - lastSeen > 3500) status('Waiting for the course window…');
};
hello(); const heartbeat = window.setInterval(hello, 1000);

// Notes are fetched only by this window, never by the audience or preview frame.
fetch(SPEAKER_NOTES_URL, {cache:'no-cache'})
  .then(response => { if (!response.ok) throw new Error('Speaker notes unavailable'); return response.text(); })
  .then(markdown => { if (exited) return; speakerNotes = parseSpeakerNotes(markdown); updateNotes(); })
  .catch(() => { /* Navigation and the full-size preview still work offline. */ });
if (window.ResizeObserver) new window.ResizeObserver(fitPreview).observe($('next-shell'));
window.addEventListener('resize', fitPreview);
