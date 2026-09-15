import test from 'node:test';
import assert from 'node:assert/strict';
import { installSlideReadability } from '../course/prototypes/slide-readability.js';

test('diagram text scaling preserves authored sizes and does not compound on redraw', () => {
  let refresh, observed;
  const label = (size, fitted = false) => ({
    size, dataset: {}, properties: {},
    getAttribute() { return this.size; },
    hasAttribute() { return fitted; },
    get style() { return {
      setProperty: (key, value) => { this.properties[key] = value; },
      removeProperty: key => { delete this.properties[key]; },
    }; },
  });
  const labels = [label('24'), label('18px'), label('70%'), label('1.2em'), label('20', true)];
  const content = { querySelectorAll: () => labels };
  installSlideReadability({ querySelector: () => content }, {
    MutationObserver: class {
      constructor(callback) { refresh = callback; }
      observe(target, options) { observed = options; }
    },
  });
  assert.equal(labels[0].properties['--course-label-size'], '24px');
  assert.equal(labels[1].properties['--course-label-size'], '18px');
  for (const item of labels.slice(2)) assert.equal(item.dataset.courseLabelSize, undefined);
  refresh(); refresh();
  assert.equal(labels[0].properties['--course-label-size'], '24px');
  assert.equal(labels[0].size, '24');
  labels[0].size = '30'; refresh();
  assert.equal(labels[0].properties['--course-label-size'], '30px');
  labels[0].size = '80%'; refresh();
  assert.equal(labels[0].dataset.courseLabelSize, undefined);
  assert.equal(labels[0].properties['--course-label-size'], undefined);
  assert.deepEqual(observed.attributeFilter, ['font-size']);
});
