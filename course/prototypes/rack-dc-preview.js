import { createPresentationRenderers } from '../web/presentation-renderers.js';
import { samplePresentation } from './rack-energy-800v-data.js';

const escapeHTML = value => String(value).replace(/[&<>"']/g, character => ({
  '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;',
}[character]));

const architectures = [
  {
    id: 'conversion-in-rack',
    label: 'Rack conversion',
    description: 'AC reaches the compute rack. The rack converts AC to DC, then regulates the device voltage.',
  },
  {
    id: 'conversion-in-sidecar',
    label: 'Hall sidecar',
    description: 'A separate power rack in the hall converts AC to 800 V DC. The compute rack regulates the device voltage.',
  },
  {
    id: 'conversion-farther-upstream',
    label: 'Upstream conversion',
    description: 'AC to DC conversion moves to the upstream power room. The hall distributes 800 V DC and the compute rack regulates the device voltage.',
  },
];

/** The same three drawings used on the following full-size architecture slides. */
export function renderDCArchitecturePreview() {
  return `<div class="dc-architecture-preview">${architectures.map(({ id, label, description }, index) => {
    const step = samplePresentation.steps.find(candidate => candidate.id === id);
    const renderer = createPresentationRenderers({
      defaults: samplePresentation.defaults,
      getState: () => ({}),
      getStep: () => step,
      isRevealed: () => false,
      escapeHTML,
      fmt: value => String(value),
    });
    return `<figure class="dc-architecture-preview-row">
      <figcaption><span aria-hidden="true">${index + 1}</span>${label}</figcaption>
      <div class="dc-architecture-preview-drawing" role="img" aria-label="${escapeHTML(description)}">
        <div aria-hidden="true">${renderer.architecture(step.kind)}</div>
      </div>
    </figure>`;
  }).join('')}</div>`;
}
