// Presentation controls shared by every chapter. Source notes remain in the reader.
function installSlideChrome() {
  const toolbar = document.querySelector('.toolbar');
  if (!toolbar) return;
  const nav = toolbar.querySelector('nav');
  const sourceLink = document.querySelector('#lesson-reference')
    || document.querySelector('dialog#reading a[href*="index.html#"]')
    || document.querySelector('dialog#reading a[href*="sample-reading.html"]');
  let reading = nav?.querySelector('a.reading-link, a[data-course-reading], a[href*="sample-reading.html"], a[href*="index.html"]');
  if (!reading && nav) {
    reading = document.createElement('a');
    reading.dataset.courseReading = '';
    reading.textContent = 'Reading';
    const exit = toolbar.querySelector('a[href*="index.html"]');
    const fallback = exit ? new URL(exit.href) : new URL('../index.html', location.href);
    fallback.search = '';
    const deck = location.pathname.split('/').pop().replace(/(?:-format)?\.html$/, '');
    const references = {ups: 'd05-storage-power-and-time', 'rack-power': 'd06-conversion-ledger', 'case-studies': 'd12-hazards-and-site-evidence'};
    if (references[deck]) fallback.hash = references[deck];
    reading.href = sourceLink?.href || fallback.href;
    nav.prepend(reading);
  }
  if (reading) reading.dataset.courseReading = '';
  if (reading && sourceLink && reading !== sourceLink) {
    const sync = () => { reading.href = sourceLink.href; };
    sync();
    new MutationObserver(sync).observe(sourceLink, {attributes: true, attributeFilter: ['href']});
  }
  // These buttons have initialized their former handlers by DOMContentLoaded.
  // Retain the hidden data targets used by legacy renderers while removing their UI.
  for (const id of ['explain', 'evidence', 'open-notes']) document.getElementById(id)?.remove();
  for (const node of document.querySelectorAll('dialog#reading, #student-context')) {
    node.hidden = true;
    node.inert = true;
    node.setAttribute('aria-hidden', 'true');
  }
}
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', installSlideChrome, {once: true});
} else installSlideChrome();
