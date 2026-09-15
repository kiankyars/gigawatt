// Scale authored SVG labels independently of the diagram's coordinates and paths.
export function installSlideReadability(doc = document, win = window) {
  const content = doc.querySelector('#viewer > main, #audience > main');
  if (!content) return;
  const update = () => {
    for (const label of content.querySelectorAll('svg text[font-size], svg tspan[font-size]')) {
      const value = label.getAttribute('font-size');
      // Preserve relative units and any explicitly fitted text.
      if (!/^\d*\.?\d+(?:px)?$/.test(value) || label.hasAttribute('textLength')) {
        delete label.dataset.courseLabelSize;
        label.style.removeProperty('--course-label-size');
        continue;
      }
      const size = `${parseFloat(value)}px`;
      if (label.dataset.courseLabelSize === size) continue;
      label.dataset.courseLabelSize = size;
      label.style.setProperty('--course-label-size', size);
    }
  };
  update();
  new win.MutationObserver(update).observe(content, {
    childList: true, subtree: true, attributes: true, attributeFilter: ['font-size'],
  });
}
