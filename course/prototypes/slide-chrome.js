// Presentation controls shared by every chapter. Source notes remain in the reader.
import { installSlideNavigation } from './slide-navigation.js';
import { installPresenter } from './presenter-bridge.js';
import { installSlideReadability } from './slide-readability.js';

function installSlideChrome() {
  installSlideNavigation();
  installSlideReadability();
  const toolbar = document.querySelector('.toolbar');
  if (!toolbar) return;
  const nav = toolbar.querySelector('nav');
  const sourceLink = document.querySelector('#lesson-reference')
    || document.querySelector('dialog#reading a[href*="index.html#"], dialog#reading a[href*="read.html#"]')
    || document.querySelector('dialog#reading a[href*="sample-reading.html"]');
  let reading = nav?.querySelector('a.reading-link, a[data-course-reading], a[href*="sample-reading.html"], a[href*="index.html"], a[href*="read.html"]');
  // Decks without their own reading link name a reader target here. The Primer
  // has no lessons, so its reading is the reader's Primer vocabulary view.
  // Published decks drop "-format", so both names map to the same target.
  const deck = location.pathname.split('/').pop().replace(/(?:-format)?\.html$/, '');
  const references = {
    'case-studies': 'd12-hazards-and-site-evidence',
    terminology: 'primer-vocabulary',
    primer: 'primer-vocabulary',
  };
  // Without a target, a bare reader link would open an unrelated first lesson.
  if (!reading && nav && (sourceLink || references[deck])) {
    reading = document.createElement('a');
    reading.dataset.courseReading = '';
    reading.textContent = 'Reading';
    const target = new URL('../index.html', import.meta.url);
    target.hash = references[deck] || '';
    reading.href = sourceLink?.href || target.href;
    nav.prepend(reading);
  }
  if (reading) {
    reading.dataset.courseReading = '';
    reading.textContent = 'Reading';
  }
  if (reading && sourceLink && reading !== sourceLink) {
    const sync = () => { reading.href = sourceLink.href; };
    sync();
    new MutationObserver(sync).observe(sourceLink, {attributes: true, attributeFilter: ['href']});
  }
  const courseLink = toolbar.querySelector('.back-to-course, .course-link, .brand');
  if (courseLink) courseLink.href = new URL('../homepage.html', import.meta.url).href;
  // These buttons have initialized their former handlers by DOMContentLoaded.
  // Retain the hidden data targets used by legacy renderers while removing their UI.
  for (const id of ['explain', 'evidence', 'open-notes']) document.getElementById(id)?.remove();
  for (const node of document.querySelectorAll('dialog#reading, #student-context')) {
    node.hidden = true;
    node.inert = true;
    node.setAttribute('aria-hidden', 'true');
  }
  installPresenter();
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', installSlideChrome, {once: true});
} else installSlideChrome();
