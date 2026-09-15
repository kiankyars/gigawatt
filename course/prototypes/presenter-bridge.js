import { PRESENTER_PROTOCOL, isPresenterMessage, requestedPreview, slideSelection } from './presenter-model.js';

const SESSION_KEY = 'gigawatt-presenter-session';

/** The original window owns the current slide; the presenter receives only navigation state. */
export function installPresenter(doc = document, win = window) {
  const root = doc.getElementById('viewer') || doc.getElementById('audience');
  if (!root) return;
  // Module-based decks can populate their selector after shared chrome loads.
  // Wait for that renderer to finish before selecting a preview or connecting.
  if (!slideSelection(doc)) {
    const waiting = new win.MutationObserver(() => {
      if (!slideSelection(doc)) return;
      waiting.disconnect();
      installPresenter(doc, win);
    });
    waiting.observe(root, { childList: true, subtree: true });
    return;
  }
  const preview = requestedPreview(win.location.href, win.parent !== win);
  if (preview !== null) {
    doc.documentElement.dataset.presenterPreview = '';
    const select = doc.querySelector('footer.course-slide-navigation select');
    if (select) {
      select.selectedIndex = Math.min(preview, select.options.length - 1);
      select.dispatchEvent(new win.Event('change', { bubbles: true }));
    }
    return;
  }
  if (new URL(win.location.href).searchParams.get('teach') !== '1') return;
  const nav = doc.querySelector('.toolbar nav');
  if (!nav || nav.querySelector('.course-presenter-button')) return;
  const location = new URL(win.location.href);
  if (!['http:', 'https:'].includes(location.protocol)) return;
  const presenterPage = new URL('./presenter.html', import.meta.url);
  let session;
  try { session = win.sessionStorage.getItem(SESSION_KEY); } catch { /* Storage can be disabled. */ }
  session ||= win.crypto.randomUUID();
  let peer = null, ready = false, observer = null, frame = 0, interval = 0, lastSnapshot = '';
  const button = doc.createElement('button');
  button.type = 'button';
  button.className = 'course-presenter-button';
  button.textContent = 'Presenter';
  button.title = 'Show the upcoming slide in a separate window';
  nav.append(button);

  const post = data => {
    if (!peer || peer.closed) return;
    peer.postMessage({ protocol: PRESENTER_PROTOCOL, session, ...data }, location.origin);
  };
  const disconnect = () => {
    ready = false;
    delete doc.documentElement.dataset.presenterActive;
    observer?.disconnect(); observer = null;
    if (frame) win.clearTimeout(frame);
    frame = 0; lastSnapshot = '';
    win.clearInterval(interval); interval = 0;
    button.removeAttribute('aria-expanded');
  };
  function snapshot() {
    frame = 0;
    if (!ready || !peer || peer.closed) { disconnect(); return; }
    const selection = slideSelection(doc);
    if (!selection) return;
    const chapterLink = doc.querySelector('.course-next-chapter:not([hidden])');
    const data = { type: 'snapshot', ...selection, title: doc.title, href: win.location.href,
      nextChapter: chapterLink ? chapterLink.textContent.trim() : null };
    const key = JSON.stringify(data);
    if (key === lastSnapshot) return;
    lastSnapshot = key;
    post(data);
  }
  function schedule() {
    if (!ready || frame) return;
    // Let deck handlers finish changing the selector and next-chapter link.
    frame = win.setTimeout(snapshot, 0);
  }
  function connect() {
    ready = true; lastSnapshot = '';
    doc.documentElement.dataset.presenterActive = '';
    button.setAttribute('aria-expanded', 'true');
    if (!observer) {
      observer = new win.MutationObserver(schedule);
      observer.observe(doc.querySelector('footer.course-slide-navigation'), {
        childList: true, subtree: true, characterData: true, attributes: true,
      });
    }
    if (!interval) interval = win.setInterval(() => { if (!peer || peer.closed) disconnect(); }, 1000);
    snapshot();
  }
  function navigate(index) {
    const select = doc.querySelector('footer.course-slide-navigation select');
    if (!select || !Number.isInteger(index) || index < 0 || index >= select.options.length) return;
    select.selectedIndex = index;
    select.dispatchEvent(new win.Event('change', { bubbles: true }));
    schedule();
  }
  win.addEventListener('message', event => {
    // Reconnect after an audience chapter navigation without opening a second popup.
    if (event.origin === location.origin && event.data?.protocol === PRESENTER_PROTOCOL
        && event.data.session === session && event.data.type === 'hello') {
      try {
        if (event.source?.opener === win && new URL(event.source.location.href).pathname === presenterPage.pathname) {
          peer = event.source;
          if (!ready) connect();
          else post({ type: 'connected' });
        }
      } catch { /* Another origin cannot become this audience's presenter. */ }
    }
    if (!isPresenterMessage(event, peer, location.origin, session)) return;
    const data = event.data;
    if (data.type === 'navigate') navigate(data.index);
    else if (data.type === 'next-chapter') doc.querySelector('.course-next-chapter:not([hidden])')?.click();
    else if (data.type === 'close') disconnect();
  });
  for (const event of ['change', 'click']) root.addEventListener(event, schedule, true);
  win.addEventListener('hashchange', schedule);
  win.addEventListener('pagehide', () => { post({ type: 'disconnect' }); disconnect(); });
  button.addEventListener('click', () => {
    try { win.sessionStorage.setItem(SESSION_KEY, session); } catch { /* Live connection still works. */ }
    if (peer && !peer.closed) { peer.focus(); connect(); return; }
    presenterPage.hash = session;
    peer = win.open(presenterPage.href, `gigawatt-presenter-${session}`, 'popup,width=1440,height=900');
    if (peer) { button.textContent = 'Presenter'; peer.focus(); }
    else { button.textContent = 'Allow presenter popup'; button.title = 'Allow this site to open its presenter window, then try again'; }
  });
}
