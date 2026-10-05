import { chapters, equipment, flowCaptions, flowDescriptions, serverParts, sources } from './content.js';

const LAST = chapters.length - 1;
const pad = (n) => String(n).padStart(2, '0');
const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));
const $ = (selector) => document.querySelector(selector);
const esc = (text) =>
  String(text).replace(/[&<>"]/g, (ch) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[ch]);
const reducedQuery = matchMedia('(prefers-reduced-motion: reduce)');

const els = {
  track: $('#scroll-track'),
  nav: $('#chapter-nav'),
  story: $('#story'),
  copy: $('#chapter-copy'),
  caption: $('#flow-caption'),
  count: $('#stop-count'),
  prev: $('#previous'),
  next: $('#next'),
  progress: $('#progress-fill'),
  detail: $('#equipment-dialog'),
  detailContent: $('#equipment-content'),
  about: $('#about-dialog'),
  menuToggle: $('#menu-toggle'),
  motion: $('#motion-button'),
  announcer: $('#announcer'),
  world: $('#world'),
  hotspots: $('#hotspots'),
  tooltip: $('#world-tooltip'),
  loading: $('#world-loading'),
  fallback: $('.world-fallback'),
};
const baseTitle = document.title;

let current = 0; // the chapter whose copy is on screen
let currentEquipment = null;
let activeFlow = null;
let paused = reducedQuery.matches;
let motionChosen = false; // once the reader toggles motion, OS changes no longer override it
let pending = null; // destination of an in-flight go(), so rapid presses accumulate
let pendingAt = 0;
let opener = null;
let restoreFocusOnClose = true;
let lastProgress = 0;
let lastSize = [innerWidth, innerHeight];
const coverReasons = new Set();

// Until three.js has loaded, the UI drives a stand-in with the same interface.
let world = {
  journey() {},
  select() {},
  clearFocus() {},
  flow() {},
  reset() {},
  orbitBy() {},
  pause() {},
  setReducedMotion() {},
  setSafeRect() {},
  cover() {},
  isSettled: () => true,
};

// ── Journey geometry ──────────────────────────────────────────────────────────
// Progress is measured across #scroll-track, so the page may continue after it.
function journeyRange() {
  const top = els.track.getBoundingClientRect().top + scrollY;
  return { top, max: els.track.offsetHeight - innerHeight };
}
function scrollToChapter(i, behavior) {
  const { top, max } = journeyRange();
  if (max > 0) scrollTo({ top: top + (max * i) / LAST, behavior });
}
function pastJourney() {
  const { top, max } = journeyRange();
  return max > 0 && scrollY > top + max + 2;
}
function layoutSnapPoints() {
  const { max } = journeyRange();
  els.track.querySelectorAll('.snap').forEach((el, i) => {
    el.style.top = `${Math.max(0, (max * i) / LAST)}px`;
  });
}

function setCover(reason, on) {
  if (on) coverReasons.add(reason);
  else coverReasons.delete(reason);
  world.cover(coverReasons.size > 0);
}

function go(i) {
  i = clamp(i, 0, LAST);
  pending = i;
  pendingAt = performance.now();
  restoreFocusOnClose = false;
  closeDetail();
  closeMenu();
  scrollToChapter(i, reducedQuery.matches ? 'instant' : 'smooth');
}
const base = () => (pending !== null && performance.now() - pendingAt < 1200 ? pending : current);
const clearPending = () => {
  pending = null;
};

let scrollFrame = 0;
function onScroll() {
  scrollFrame = 0;
  const { top, max } = journeyRange();
  if (!(max > 0)) return;
  const progress = clamp(((scrollY - top) / max) * LAST, 0, LAST);
  lastProgress = progress;
  world.journey(progress);
  els.progress.style.transform = `scaleY(${progress / LAST})`;
  if (pending !== null && Math.abs(progress - pending) < 0.02) pending = null;
  const past = scrollY > top + max + 2;
  if (past !== document.body.classList.contains('past-journey')) {
    document.body.classList.toggle('past-journey', past);
    setCover('past', past);
    if (past) {
      closeMenu();
      // Past the journey, the address and title belong to the page again, so a reload
      // keeps the reader where they are rather than jumping back to the last chapter.
      if (parseHash()) {
        history.replaceState(history.state, '', location.pathname + location.search);
        history.scrollRestoration = 'auto';
      }
      document.title = baseTitle;
    } else updateHash();
  }
  if (els.detail.open) return; // the chapter holds still while the drawer is open
  enterChapter(Math.round(progress));
}
addEventListener(
  'scroll',
  () => {
    if (!scrollFrame) scrollFrame = requestAnimationFrame(onScroll);
  },
  { passive: true },
);
addEventListener('scrollend', clearPending);
addEventListener('wheel', clearPending, { passive: true });
addEventListener(
  'touchstart',
  (e) => {
    if (!e.target.closest?.('button, a, [role="button"]')) clearPending();
  },
  { passive: true },
);

// The track scales with the viewport, so a real resize keeps the reader's progress
// instead of letting the old scroll offset land in another chapter.
addEventListener('resize', () => {
  const [w, h] = lastSize;
  if (innerWidth !== w || Math.abs(innerHeight - h) > 120) {
    lastSize = [innerWidth, innerHeight];
    if (!document.body.classList.contains('past-journey')) {
      const { top, max } = journeyRange();
      if (max > 0) scrollTo({ top: top + (lastProgress / LAST) * max, behavior: 'instant' });
    }
  }
  layoutSnapPoints();
  updateSafeRect();
  onScroll();
});

function enterChapter(i) {
  if (i === current) return;
  current = i;
  closeMenu();
  if (activeFlow) {
    activeFlow = null;
    world.flow(null);
  }
  world.reset(); // ease any orbit back to the authored framing
  render();
  announceChapter();
  updateHash();
}

// ── Chapter copy ──────────────────────────────────────────────────────────────
function copyFor(c, i) {
  const eyebrow = i === 0 ? 'A JOURNEY INSIDE' : `${pad(i + 1)} / ${c.name.toUpperCase()}`;
  const arrow = '<span aria-hidden="true">→</span>';
  const actions = [];
  if (c.id === 'compute') actions.push(`<button id="open-server" type="button">Open a server ${arrow}</button>`);
  actions.push(
    `<button id="open-guide" type="button">${i === 0 ? 'See the five systems' : c.id === 'compute' ? 'Equipment guide' : 'Explore the equipment'} ${arrow}</button>`,
  );
  if (c.flow) {
    actions.push(
      `<button id="trace" type="button" aria-pressed="false" data-flow="${c.flow.id}">Follow the ${esc(c.flow.noun)}</button>`,
    );
  }
  // Optional links to further material, such as a course's chapters, set in content.js.
  const links = c.links?.length
    ? `<div class="chapter-links"><p class="eyebrow">${esc((c.linksTitle || 'Go deeper').toUpperCase())}</p>${c.links
        .map((link) => `<a href="${esc(link.href)}">${esc(link.label)} ${arrow}</a>`)
        .join('')}</div>`
    : '';
  return `<p class="eyebrow">${esc(c.eyebrow || eyebrow)}</p>
    <h1 id="chapter-title" tabindex="-1">${c.title.map(esc).join('<br>')}</h1>
    <p class="lead">${esc(c.lead)}</p>
    ${c.enter && i < LAST ? `<button class="enter-button" id="enter" type="button">${esc(c.enter)} <span aria-hidden="true">↓</span></button>` : ''}
    <div class="chapter-actions">${actions.join('')}</div>
    ${links}
    ${i === 0 ? '<p class="page-scroll-hint">SCROLL TO TRAVEL THROUGH THE WORLD</p>' : ''}`;
}

function render() {
  const c = chapters[current];
  document.documentElement.style.setProperty('--accent', c.color);
  document.body.dataset.chapter = c.id;
  els.nav.querySelectorAll('button').forEach((b, i) => {
    if (i === current) b.setAttribute('aria-current', 'step');
    else b.removeAttribute('aria-current');
  });
  els.count.textContent = `${pad(current + 1)} / ${pad(chapters.length)}`;
  els.prev.setAttribute('aria-disabled', String(current === 0));
  els.next.setAttribute('aria-disabled', String(current === LAST));
  // Rebuilding the copy must not drop keyboard focus: keep it on the same control,
  // or on the new heading.
  const focused = els.copy.contains(document.activeElement) ? document.activeElement.id : null;
  els.copy.innerHTML = copyFor(c, current);
  syncFlowUI();
  if (focused !== null)
    (els.copy.querySelector(`#${focused || 'none'}`) || els.copy.querySelector('h1')).focus({ preventScroll: true });
  updateSafeRect();
}

els.copy.addEventListener('click', (e) => {
  const button = e.target.closest('button');
  if (!button) return;
  if (button.id === 'enter') go(current + 1);
  else if (button.id === 'open-server') select('server');
  else if (button.id === 'open-guide') openGuide(current);
  else if (button.id === 'trace') setFlow(activeFlow === button.dataset.flow ? null : button.dataset.flow);
});

// ── Flows ─────────────────────────────────────────────────────────────────────
function syncFlowUI() {
  const trace = els.copy.querySelector('#trace');
  if (trace) trace.setAttribute('aria-pressed', String(activeFlow === trace.dataset.flow));
  els.caption.textContent = activeFlow ? flowCaptions[activeFlow] : '';
}
function setFlow(id) {
  activeFlow = id || null;
  world.flow(activeFlow);
  syncFlowUI();
  announce(activeFlow ? flowDescriptions[activeFlow] : 'Path hidden.');
  updateSafeRect();
}

// ── Announcements ─────────────────────────────────────────────────────────────
function announce(text) {
  els.announcer.textContent = '';
  requestAnimationFrame(() => {
    els.announcer.textContent = text;
  });
}
let announceTimer = 0;
function announceChapter() {
  clearTimeout(announceTimer);
  announceTimer = setTimeout(() => {
    const c = chapters[current];
    announce(`Chapter ${current + 1} of ${chapters.length}, ${c.name}: ${c.title.join(' ')}`);
  }, 300);
}

// ── Equipment drawer ──────────────────────────────────────────────────────────
// The drawer is non-modal, so the 3D view beside or above it stays live: parts can be
// picked, labels clicked and the model orbited while it is open.
function openDrawer() {
  closeMenu();
  if (!els.detail.open) {
    opener = document.activeElement && document.activeElement !== document.body ? document.activeElement : null;
    els.detail.show();
  }
  restoreFocusOnClose = true;
  els.detail.scrollTop = 0;
  els.detailContent.querySelector('h2').focus({ preventScroll: true });
  updateSafeRect();
}

function closeDetail() {
  if (!els.detail.open) return;
  els.detail.close();
  currentEquipment = null;
  world.clearFocus();
  updateSafeRect();
  updateHash();
}

els.detail.addEventListener('close', () => {
  if (els.detail.open) return; // reopened before this event arrived
  currentEquipment = null;
  world.clearFocus();
  updateSafeRect();
  updateHash();
  if (restoreFocusOnClose) {
    const target = opener?.isConnected && opener.offsetParent !== null ? opener : els.copy.querySelector('#open-guide');
    (target || els.story).focus({ preventScroll: true });
  }
  opener = null;
  restoreFocusOnClose = true;
});

function openGuide(i = current) {
  const c = chapters[i];
  const list = c.items
    .map((id) => {
      const label = equipment[id]?.name || chapters.find((ch) => ch.id === id)?.name;
      return `<button type="button" data-equipment="${id}">${esc(label)}<span aria-hidden="true">→</span></button>`;
    })
    .join('');
  els.detailContent.innerHTML = `<p class="eyebrow">${esc(c.name.toUpperCase())}</p>
    <h2 id="equipment-title" tabindex="-1">${esc(c.guideTitle)}</h2>
    <p>${esc(c.guideLead)}</p>
    <div class="equipment-list">${list}</div>
    <p class="eyebrow">${esc(c.insight.toUpperCase())}</p>
    <p class="detail-insight">${esc(c.fact)}</p>`;
  if (currentEquipment) {
    currentEquipment = null;
    world.clearFocus();
  }
  openDrawer();
  updateHash();
}

function select(id) {
  if (!Object.hasOwn(equipment, id)) {
    // Chapter-level pads, chapter labels and overview list items.
    const i = chapters.findIndex((c) => c.id === id);
    if (i < 0) return;
    if (i !== current) return go(i);
    return id === 'compute' ? select('server') : openGuide(i);
  }
  const e = equipment[id];
  const ci = chapters.findIndex((c) => c.id === e.chapter);
  const chapter = chapters[ci];
  currentEquipment = id;
  if (activeFlow) setFlow(null);
  world.select(id);
  const parts = serverParts.includes(id) ? serverParts.filter((k) => k !== id) : [];
  const partList = parts.length
    ? `<p class="eyebrow">${id === 'server' ? 'ITS PARTS' : 'MORE IN THIS SERVER'}</p><div class="equipment-list">${parts
        .map(
          (k) =>
            `<button type="button" data-equipment="${k}">${k === 'server' ? 'Whole server' : esc(equipment[k].name)}<span aria-hidden="true">→</span></button>`,
        )
        .join('')}</div>`
    : '';
  const source = e.source
    ? `<a class="source-link" href="${esc(e.source)}" target="_blank" rel="noreferrer">Read the source<span class="visually-hidden"> (opens in a new tab)</span> <span aria-hidden="true">↗</span></a>`
    : '';
  els.detailContent.innerHTML = `<button class="back-equipment" type="button" data-guide="${ci}"><span aria-hidden="true">←</span> ${esc(chapter.guideTitle)}</button>
    <p class="eyebrow">${esc(chapter.name.toUpperCase())} / LOOK CLOSER</p>
    <h2 id="equipment-title" tabindex="-1">${esc(e.name)}</h2>
    <p>${esc(e.description)}</p>
    <p class="equipment-path">${esc(e.path)}</p>
    <p class="eyebrow">GOOD TO KNOW</p>
    <p class="detail-insight">${esc(e.insight)}</p>
    ${partList}${source}`;
  openDrawer();
  updateHash();
}

els.detailContent.addEventListener('click', (e) => {
  const item = e.target.closest('[data-equipment]');
  if (item) return select(item.dataset.equipment);
  const back = e.target.closest('.back-equipment');
  if (back) openGuide(Number(back.dataset.guide));
});
els.detail.querySelector('.close-dialog').addEventListener('click', closeDetail);

// ── About dialog (modal) ──────────────────────────────────────────────────────
// A backdrop press closes it only when both the press and release land outside the
// panel without a drag, so text selection and stray taps cannot dismiss it.
let backdropDown = null;
const outsideAbout = (e) => {
  const r = els.about.getBoundingClientRect();
  return e.clientX < r.left || e.clientX > r.right || e.clientY < r.top || e.clientY > r.bottom;
};
els.about.addEventListener('pointerdown', (e) => {
  backdropDown = e.target === els.about && outsideAbout(e) ? { x: e.clientX, y: e.clientY } : null;
});
els.about.addEventListener('click', (e) => {
  if (
    backdropDown &&
    e.target === els.about &&
    outsideAbout(e) &&
    Math.hypot(e.clientX - backdropDown.x, e.clientY - backdropDown.y) < 6
  ) {
    els.about.close();
  }
  backdropDown = null;
});
els.about.querySelector('.close-dialog').addEventListener('click', () => els.about.close());
els.about.addEventListener('close', () => setCover('about', false));
$('#about-button')?.addEventListener('click', () => {
  closeMenu();
  closeDetail();
  els.about.showModal();
  setCover('about', els.about.getBoundingClientRect().width >= innerWidth - 1);
});

// ── Navigation controls ───────────────────────────────────────────────────────
function setMenu(open) {
  els.nav.classList.toggle('open', open);
  els.menuToggle.setAttribute('aria-expanded', String(open));
  els.menuToggle.querySelector('span').textContent = open ? '−' : '+';
  updateSafeRect();
}
function closeMenu() {
  if (!els.nav.classList.contains('open')) return;
  const focusInside = els.nav.contains(document.activeElement);
  setMenu(false);
  if (focusInside) els.menuToggle.focus({ preventScroll: true });
}
els.menuToggle.addEventListener('click', () => setMenu(!els.nav.classList.contains('open')));
document.addEventListener('pointerdown', (e) => {
  if (els.nav.classList.contains('open') && !els.nav.contains(e.target) && !els.menuToggle.contains(e.target))
    closeMenu();
});
els.nav.addEventListener('click', (e) => {
  const b = e.target.closest('[data-chapter]');
  if (b) go(Number(b.dataset.chapter));
});
els.prev.addEventListener('click', () => {
  if (els.prev.getAttribute('aria-disabled') !== 'true') go(base() - 1);
});
els.next.addEventListener('click', () => {
  if (els.next.getAttribute('aria-disabled') !== 'true') go(base() + 1);
});
// A host page may leave out the home button or the camera controls.
$('#home')?.addEventListener('click', () => go(0));
$('#reset-camera')?.addEventListener('click', () => world.reset());
$('#rotate-left')?.addEventListener('click', () => world.orbitBy(-0.35));
$('#rotate-right')?.addEventListener('click', () => world.orbitBy(0.35));

function updateMotion() {
  els.motion.textContent = paused ? 'Play motion' : 'Pause motion';
  world.pause(paused);
}
els.motion.addEventListener('click', () => {
  paused = !paused;
  motionChosen = true;
  updateMotion();
});
reducedQuery.addEventListener('change', (e) => {
  world.setReducedMotion(e.matches);
  if (!motionChosen) {
    paused = e.matches;
    updateMotion();
  }
});

document.addEventListener('keydown', (e) => {
  if (e.key === 'Escape') {
    if (els.about.open) return; // the modal handles its own Escape
    if (els.nav.classList.contains('open')) {
      closeMenu();
      els.menuToggle.focus({ preventScroll: true });
      e.preventDefault();
    } else if (els.detail.open) {
      closeDetail();
      e.preventDefault();
    }
    return;
  }
  if (e.defaultPrevented || e.ctrlKey || e.metaKey || e.altKey) return;
  if (els.about.open || els.detail.open || pastJourney()) return;
  const editable =
    'input, select, textarea, [contenteditable]:not([contenteditable="false"]), [role="textbox"], [role="combobox"], [role="listbox"], [role="slider"]';
  if (e.target.closest?.(editable)) return;
  const interactive = e.target.closest?.('button, a');
  let to = null;
  if (/^[1-9]$/.test(e.key) && Number(e.key) <= chapters.length) to = Number(e.key) - 1;
  else if (['ArrowDown', 'ArrowRight', 'PageDown'].includes(e.key) || (e.key === ' ' && !e.shiftKey && !interactive))
    to = base() + 1;
  else if (['ArrowUp', 'ArrowLeft', 'PageUp'].includes(e.key) || (e.key === ' ' && e.shiftKey && !interactive))
    to = base() - 1;
  // Past either end, the key keeps its native behaviour (for example, scrolling on to
  // content after the journey).
  if (to === null || to < 0 || to > LAST) return;
  e.preventDefault();
  go(to);
});

// ── Layout handed to the world ────────────────────────────────────────────────
// The camera centres the subject in the screen area not covered by the copy, the
// chapter list or the drawer. Hotspots outside that area are hidden.
let safeFrame = 0;
function updateSafeRect() {
  cancelAnimationFrame(safeFrame);
  safeFrame = requestAnimationFrame(() => {
    const W = innerWidth;
    const H = innerHeight;
    const rect = (el) => {
      if (!el || getComputedStyle(el).display === 'none') return null;
      const r = el.getBoundingClientRect();
      return r.width && r.height ? r : null;
    };
    const drawer = els.detail.open ? rect(els.detail) : null;
    const copy = rect(els.story);
    const nav = rect(els.nav);
    let l = 0;
    let r = W;
    let t = Math.min(120, H * 0.15);
    let b = H - 40;
    let side = false;
    const occupied = drawer || copy;
    if (occupied) {
      if (occupied.left > W * 0.35) {
        r = occupied.left - 24;
        side = true;
      } else b = occupied.top - 12;
    }
    if (!drawer && nav && nav.right < W * 0.3) l = nav.right + 24;
    if (r - l < 160) [l, r] = [0, W];
    if (b - t < 140) [t, b] = [0, H];
    world.setSafeRect({ l, r, t, b, side });
  });
}
const layoutObserver = new ResizeObserver(updateSafeRect);
layoutObserver.observe(els.story);
layoutObserver.observe(els.detail);
document.fonts?.ready.then(updateSafeRect);

// ── Addresses ─────────────────────────────────────────────────────────────────
// The address bar mirrors the chapter and open equipment (#power, #power/ups), so a
// view can be shared. Hashes that belong to the host page are left alone.
function parseHash(hash = location.hash) {
  let raw;
  try {
    raw = decodeURIComponent(hash.slice(1));
  } catch {
    return null;
  }
  const [chapterId, equipmentId] = raw.split('/');
  const i = chapters.findIndex((c) => c.id === chapterId);
  return i < 0 ? null : { i, equipmentId: Object.hasOwn(equipment, equipmentId) ? equipmentId : null };
}
function updateHash() {
  if (document.body.classList.contains('past-journey')) return;
  const c = chapters[current];
  document.title = current ? `${c.name} · ${baseTitle}` : baseTitle;
  if (location.hash && !parseHash()) return;
  const hash = currentEquipment
    ? `#${equipment[currentEquipment].chapter}/${currentEquipment}`
    : current
      ? `#${c.id}`
      : '';
  if (location.hash !== hash) history.replaceState(history.state, '', hash || location.pathname + location.search);
}
function applyHash() {
  const target = parseHash();
  if (!target) return false;
  restoreFocusOnClose = false;
  closeDetail();
  scrollToChapter(target.i, 'instant');
  onScroll();
  if (target.equipmentId) select(target.equipmentId);
  return true;
}
addEventListener('hashchange', applyHash);
document.querySelector('.skip-link[href="#story"]')?.addEventListener('click', (e) => {
  e.preventDefault();
  els.story.focus();
});

// ── WebMCP ────────────────────────────────────────────────────────────────────
// The tool goes through the same functions as the visible controls.
function registerTool() {
  if (!document.modelContext?.registerTool) return;
  const flowChapter = Object.fromEntries(chapters.filter((c) => c.flow).map((c) => [c.flow.id, c.id]));
  const flows = [...Object.keys(flowChapter), 'none'];
  const lifecycle = new AbortController();
  const tool = {
    name: 'explore_datacenter',
    title: 'Explore the datacenter',
    description:
      'Travel to a datacenter chapter, inspect equipment, or trace power, heat, and data in the visible world.',
    inputSchema: {
      type: 'object',
      properties: {
        chapter: { type: 'string', enum: chapters.map((c) => c.id) },
        equipment: { type: 'string', enum: Object.keys(equipment) },
        flow: { type: 'string', enum: flows },
      },
      additionalProperties: false,
    },
    annotations: { readOnlyHint: false, untrustedContentHint: false },
    execute(input) {
      if (!input || typeof input !== 'object' || Array.isArray(input)) throw Error('Invalid options');
      if (Object.keys(input).some((k) => !['chapter', 'equipment', 'flow'].includes(k))) throw Error('Invalid options');
      if (input.chapter !== undefined && !chapters.some((c) => c.id === input.chapter)) throw Error('Unknown chapter');
      if (input.equipment !== undefined && !Object.hasOwn(equipment, input.equipment)) throw Error('Unknown equipment');
      if (input.flow !== undefined && !flows.includes(input.flow)) throw Error('Unknown flow');
      const traced = input.flow && input.flow !== 'none';
      if (input.equipment && traced) throw Error('Choose equipment or a flow');
      const chapterId =
        input.chapter ??
        (input.equipment ? equipment[input.equipment].chapter : traced ? flowChapter[input.flow] : undefined);
      if (input.equipment && equipment[input.equipment].chapter !== chapterId)
        throw Error('Equipment does not belong to this chapter');
      if (traced && flowChapter[input.flow] !== chapterId)
        throw Error(`That flow belongs to the ${flowChapter[input.flow]} chapter`);
      if (chapterId !== undefined) {
        restoreFocusOnClose = false;
        closeDetail();
        const i = chapters.findIndex((c) => c.id === chapterId);
        scrollToChapter(i, 'instant');
        onScroll();
        enterChapter(i);
      }
      if (input.equipment) select(input.equipment);
      if (input.flow !== undefined) setFlow(traced ? input.flow : null);
      return {
        chapter: chapters[current].id,
        equipment: currentEquipment,
        flow: activeFlow,
        title: currentEquipment ? equipment[currentEquipment].name : chapters[current].name,
        graphicsAvailable: document.body.dataset.world === 'ready',
      };
    },
  };
  try {
    Promise.resolve(document.modelContext.registerTool(tool, { signal: lifecycle.signal })).catch(() => {});
  } catch {
    // Registration is optional.
  }
  addEventListener('pagehide', () => lifecycle.abort(), { once: true });
}

// ── 3D world ──────────────────────────────────────────────────────────────────
// Loaded lazily: copy, navigation and controls work before (and without) WebGL.
function loadWorld() {
  const options = {
    onSelect: select,
    onEmptyClick: () => closeDetail(),
    onReady: () => worldState('ready'),
    onHotspotHidden: () => els.story.focus({ preventScroll: true }),
    hotspotLayer: els.hotspots,
    tooltip: els.tooltip,
    chapterIds: chapters.map((c) => c.id),
    chapterLabels: Object.fromEntries(
      chapters.slice(1).map((c, i) => [c.id, `${pad(i + 2)} / ${c.name.toUpperCase()}`]),
    ),
    itemLabels: Object.fromEntries(Object.entries(equipment).map(([id, e]) => [id, e.label])),
    itemChapter: Object.fromEntries(Object.entries(equipment).map(([id, e]) => [id, e.chapter])),
    colors: Object.fromEntries(chapters.map((c) => [c.id, c.color])),
    names: {
      ...Object.fromEntries(chapters.map((c) => [c.id, c.name])),
      ...Object.fromEntries(Object.entries(equipment).map(([id, e]) => [id, e.name])),
    },
    serverParts,
  };
  import('./world.js')
    .then(({ createWorld }) => {
      const created = createWorld(els.world, options);
      if (!created) throw new Error('WebGL is unavailable');
      world = created;
      world.setReducedMotion(reducedQuery.matches);
      world.pause(paused);
      world.cover(coverReasons.size > 0);
      updateSafeRect();
      onScroll();
      if (currentEquipment) world.select(currentEquipment);
      else if (activeFlow) world.flow(activeFlow);
    })
    .catch((error) => {
      console.error(error);
      els.fallback.hidden = false;
      worldState('fallback');
    });
}

// Host pages can listen for 'datacenter:world' to react when the 3D view is ready or unavailable.
function worldState(state) {
  els.loading?.remove();
  document.body.dataset.world = state;
  document.dispatchEvent(new CustomEvent('datacenter:world', { detail: state }));
}

// ── Start ─────────────────────────────────────────────────────────────────────
els.nav.innerHTML = chapters
  .map((c, i) => `<button type="button" data-chapter="${i}"><span>${pad(i + 1)}</span>${esc(c.name)}</button>`)
  .join('');
els.track.innerHTML = chapters.map(() => '<i class="snap"></i>').join('');
$('#source-list').innerHTML =
  '<p class="eyebrow">FURTHER READING</p>' +
  sources
    .map(
      (s) =>
        `<p><a href="${esc(s.url)}" target="_blank" rel="noreferrer">${esc(s.title)}<span class="visually-hidden"> (opens in a new tab)</span> <span aria-hidden="true">↗</span></a></p>`,
    )
    .join('');
registerTool();
render();
updateMotion();
for (const el of document.querySelectorAll('[data-needs-script]')) el.hidden = false;
layoutSnapPoints();
if (parseHash()) history.scrollRestoration = 'manual';
if (!applyHash()) onScroll();
loadWorld();

// A small hook for automated checks: whether the camera has settled after a change.
window.datacenter = { isSettled: () => world.isSettled() };
