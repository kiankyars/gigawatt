// Course-specific copy for the homepage's voxel data center. The shared module in
// ./datacenter/ is an unmodified copy of github.com/kiankyars/datacenter (see
// provenance.json); this file adapts its copy to the course before app.js renders.
import { chapters, equipment } from './datacenter/content.js';
import { presentationLabels } from '../prototypes/teaching-navigation.js';

// Each link is a literal path so site staging can rewrite it to the published slide address.
const decks = {
  primer: '../prototypes/terminology-format.html?teach=1',
  overview: '../prototypes/orientation-format.html?teach=1',
  workloads: '../prototypes/workload-format.html?teach=1',
  distribution: '../prototypes/distribution-format.html?teach=1',
  continuity: '../prototypes/continuity-format.html?teach=1',
  'rack-energy': '../prototypes/rack-energy-format.html?teach=1',
  networking: '../prototypes/networking-format.html?teach=1',
  cooling: '../prototypes/cooling-format.html?teach=1',
  'heat-rejection': '../prototypes/heat-rejection-format.html?teach=1',
  operations: '../prototypes/operations-format.html?teach=1',
};
const deck = (id, label = presentationLabels[id]) => ({ label, href: new URL(decks[id], import.meta.url).href });

const byId = Object.fromEntries(chapters.map((c) => [c.id, c]));
Object.assign(byId.overview, {
  eyebrow: 'A VISUAL COURSE ON AI INFRASTRUCTURE',
  title: ['Inside an AI', 'data center.'],
  lead: 'Explore the power, computing and cooling systems that make AI possible.',
  enter: 'Explore the data center',
  linksTitle: 'Start the course',
  links: [
    deck('primer', `Start with ${presentationLabels.primer}`),
    deck('overview'),
    { label: 'All chapters', href: '#chapters' },
  ],
});
const related = {
  power: ['distribution', 'continuity'],
  compute: ['workloads', 'rack-energy'],
  cooling: ['cooling', 'heat-rejection'],
  network: ['networking'],
  operations: ['operations'],
};
for (const [chapter, ids] of Object.entries(related)) {
  Object.assign(byId[chapter], { linksTitle: 'In the course', links: ids.map((id) => deck(id)) });
}

// The course writes "data center" as two words.
const spell = (text) => text.replace(/\bDatacenter\b/g, 'Data center').replace(/\bdatacenter\b/g, 'data center');
for (const record of [...chapters, ...Object.values(equipment)]) {
  for (const [key, value] of Object.entries(record)) {
    if (typeof value === 'string') record[key] = spell(value);
  }
}
// The teaching standard keeps generic "not live data" caveats off teaching visuals.
equipment.monitoring.insight = equipment.monitoring.insight.replace(/\s*This world shows no live readings\.$/, '');
