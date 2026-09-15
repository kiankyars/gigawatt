import { PRESENTER_PROTOCOL, isPresenterMessage, requestedPreview, slideSelection } from './presenter-model.js';

const SESSION_KEY = 'gigawatt-presenter-session';

export function clickPresenterElement(source, win) {
  // SVG links are not HTMLElements and do not implement HTMLElement.click().
  if (source.matches('button, input, a') && typeof source.click === 'function') source.click();
  else source.dispatchEvent(new win.MouseEvent('click', { bubbles: true, cancelable: true, view: win }));
}

export function applyPresenterScroll(target, { left, top }) {
  if (!Number.isFinite(left) || !Number.isFinite(top) || typeof target?.scrollTo !== 'function') return false;
  target.scrollTo({ left, top, behavior: 'instant' });
  return true;
}

/** Audience state stays in the original renderer. The presenter only forwards actions. */
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
    waiting.observe(root, {childList: true, subtree: true});
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
  if (!nav) return;
  const location = new URL(win.location.href);
  if (!['http:', 'https:'].includes(location.protocol)) return;
  const presenterPage = new URL('./presenter.html', import.meta.url);
  let session;
  try { session = win.sessionStorage.getItem(SESSION_KEY); } catch { /* Storage can be disabled. */ }
  session ||= win.crypto.randomUUID();
  let peer = null, ready = false, observer = null, frame = 0, lastSent = 0, interval = 0;
  let nodeCounter = 0, liveNodes = new Map();
  const nodeIds = new WeakMap();
  const button = doc.createElement('button');
  button.type = 'button';
  button.className = 'course-presenter-button';
  button.textContent = 'Presenter';
  button.title = 'Open a separate presenter window';
  nav.append(button);

  const post = data => {
    if (!peer || peer.closed) return;
    peer.postMessage({ protocol: PRESENTER_PROTOCOL, session, ...data }, location.origin);
  };
  const disconnect = () => {
    ready = false;
    observer?.disconnect(); observer = null;
    if (frame) win.clearTimeout(frame);
    frame = 0;
    win.clearInterval(interval); interval = 0;
    button.removeAttribute('aria-expanded');
  };
  function snapshot() {
    frame = 0;
    if (!ready || !peer || peer.closed) { disconnect(); return; }
    const selection = slideSelection(doc);
    if (!selection) return;
    const copy = root.cloneNode(true);
    const sources = [root, ...root.querySelectorAll('*')];
    const copies = [copy, ...copy.querySelectorAll('*')];
    const scrollPositions = [];
    liveNodes = new Map();
    sources.forEach((source, i) => {
      const clone = copies[i];
      const id = nodeIds.get(source) || String(++nodeCounter);
      nodeIds.set(source, id); liveNodes.set(id, source);
      clone.setAttribute('data-presenter-node', id);
      if (source.scrollLeft || source.scrollTop || source.scrollWidth > source.clientWidth || source.scrollHeight > source.clientHeight) {
        scrollPositions.push({ node: id, left: source.scrollLeft, top: source.scrollTop });
      }
      for (const attribute of [...clone.attributes]) if (/^on/i.test(attribute.name)) clone.removeAttribute(attribute.name);
      if (source instanceof win.HTMLInputElement) {
        clone.setAttribute('value', source.value);
        clone.toggleAttribute('checked', source.checked);
      } else if (source instanceof win.HTMLTextAreaElement) clone.textContent = source.value;
      else if (source instanceof win.HTMLSelectElement) {
        [...clone.options].forEach((option, n) => option.toggleAttribute('selected', n === source.selectedIndex));
      } else if (source instanceof win.HTMLCanvasElement) {
        try {
          const image = doc.createElement('img');
          for (const attribute of [...clone.attributes]) image.setAttribute(attribute.name, attribute.value);
          image.src = source.toDataURL(); clone.replaceWith(image);
        } catch { /* External canvas pixels may be unavailable to the browser. */ }
      }
    });
    copy.querySelectorAll('script, iframe, object, embed').forEach(element => element.remove());
    const styles = [...doc.head.querySelectorAll('style, link[rel="stylesheet"], meta[name="color-scheme"]')]
      .map(element => element.outerHTML).join('');
    const chapterLink = doc.querySelector('.course-next-chapter:not([hidden])');
    lastSent = win.performance.now();
    post({ type: 'snapshot', ...selection, title: doc.title, href: win.location.href,
      width: win.innerWidth, height: win.innerHeight, scrollX: win.scrollX, scrollY: win.scrollY,
      html: copy.outerHTML, styles, bodyClass: doc.body.className, scrollPositions,
      nextChapter: chapterLink ? chapterLink.textContent.trim() : null,
    });
  }
  function schedule() {
    if (!ready || frame) return;
    // Coalesce DOM and input changes. A drag stays responsive without copying on every mutation.
    frame = win.setTimeout(snapshot, Math.max(0, 60 - (win.performance.now() - lastSent)));
  }
  function connect() {
    ready = true;
    button.setAttribute('aria-expanded', 'true');
    if (!observer) {
      observer = new win.MutationObserver(schedule);
      observer.observe(root, { childList: true, subtree: true, characterData: true, attributes: true });
    }
    if (!interval) interval = win.setInterval(() => { if (!peer || peer.closed) disconnect(); }, 1000);
    snapshot();
  }
  function navigate(index) {
    const select = doc.querySelector('footer.course-slide-navigation select');
    if (!select || !Number.isInteger(index) || index < 0 || index >= select.options.length) return;
    select.selectedIndex = index;
    select.dispatchEvent(new win.Event('change', { bubbles: true }));
    snapshot();
  }
  function act(action) {
    if (action.kind === 'scroll') {
      // A late scroll event from the previous slide must not move the new one.
      if (action.href !== win.location.href) return;
      const target = action.node === null ? win : liveNodes.get(action.node);
      if (target !== win && (!target?.isConnected || !root.contains(target))) return;
      if (applyPresenterScroll(target, action)) schedule();
      return;
    }
    const source = liveNodes.get(action.node);
    if (!source?.isConnected || !root.contains(source)) return;
    if (action.kind === 'click') {
      clickPresenterElement(source, win);
    } else if (['input', 'change'].includes(action.kind) && source.matches('input, select, textarea')) {
      if (source.matches('select')) {
        if (!Number.isInteger(action.index) || action.index < 0 || action.index >= source.options.length) return;
        source.selectedIndex = action.index;
      } else source.value = String(action.value ?? '');
      source.dispatchEvent(new win.Event(action.kind, { bubbles: true }));
    }
    snapshot();
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
    else if (data.type === 'action') act(data);
    else if (data.type === 'close') disconnect();
    else if (data.type === 'request-snapshot') schedule();
  });
  for (const event of ['input', 'change', 'click']) root.addEventListener(event, schedule, true);
  // Element scroll events do not bubble; capture them from the slide's panels.
  root.addEventListener('scroll', schedule, { capture: true, passive: true });
  for (const event of ['resize', 'hashchange', 'scroll']) win.addEventListener(event, schedule, { passive: true });
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
