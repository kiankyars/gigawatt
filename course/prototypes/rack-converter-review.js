import { phaseWaveforms } from './rack-power-model.js';

export function renderCorePath() {
  return `<div class="core-path"><div class="core-flow"><section><h2>PSU</h2><p>AC → 51 V DC</p></section><b>→</b><section><h2>VRM</h2><p>Makes and regulates the core voltage</p></section><b>→</b><section class="core-rail"><h2>Vcore rail</h2><p>The copper path carrying ~1 V</p></section><b>→</b><section><h2>CPU cores</h2></section></div><div class="core-support"><strong>Local capacitors</strong><span>Connect to the rail beside the chip</span></div></div>`;
}

export function renderConversionChoices() {
  return `<div class="converter-choices"><section><h2>Direct conversion</h2><div class="converter-route"><span class="route-input">51 V</span><span class="route-wire">51 V distribution</span><div class="near-chip"><span class="route-converter">VRM<br><strong>51 V → 1 V</strong></span><span class="short-rail">1 V</span><span class="route-chip">Cores</span></div></div></section><section><h2>With an intermediate rail</h2><div class="converter-route"><span class="route-input">51 V</span><span class="route-converter">Bus converter<br><strong>51 V → 12 V</strong></span><span class="route-wire">12 V distribution</span><div class="near-chip"><span class="route-converter">VRM<br><strong>12 V → 1 V</strong></span><span class="short-rail">1 V</span><span class="route-chip">Cores</span></div></div></section><p class="conversion-principle">Keep the 1 V path short in either design.</p><p class="conversion-efficiency">Two-stage efficiency multiplies: <strong>98% × 95% = 93.1%</strong></p></div>`;
}

export function renderVRMPhases() {
  const left = 82, right = 462, width = right - left;
  const colors = ['var(--teal)', 'var(--amber)', 'var(--phase-three)', 'var(--ink)'];
  const line = (curve, y, height, min, max) => curve.map((v, i) =>
    `${i ? 'L' : 'M'}${(left + i / (curve.length - 1) * width).toFixed(2)} ${(y + height - (v - min) / (max - min) * height).toFixed(2)}`
  ).join(' ');
  const panel = count => {
    const model = phaseWaveforms(count), perPath = model.totalAmps / count;
    const paths = model.curves.map((curve, i) =>
      `<path d="${line(curve, 50, 104, perPath * .75, perPath * 1.25)}" fill="none" stroke="${colors[i]}" stroke-width="3"/>`
    ).join('');
    const ticks = [800, 1000, 1200].map(value => {
      const y = 248 + 112 - (value - 780) / 440 * 112;
      return `<path d="M${left} ${y}H${right}" stroke="var(--line)" stroke-dasharray="4 5"/><text x="${left - 12}" y="${y + 6}" text-anchor="end" font-size="19" fill="var(--muted)">${value.toLocaleString('en-US')}</text>`;
    }).join('');
    return `<section class="vrm-phase-panel" aria-label="${count === 1 ? 'One phase' : 'Four phases'} inside one VRM"><h2>${count === 1 ? 'One phase' : 'Four phases'}</h2><svg viewBox="0 0 480 404" role="img" aria-label="${count === 1 ? 'One path carries an average of 1,000 amperes.' : 'Four staggered paths each carry an average of 250 amperes.'} The lower plot shows their total current on the same 800 to 1,200 ampere scale in both examples."><text x="${left}" y="24" font-size="21" fill="var(--muted)">${perPath.toLocaleString('en-US')} A average per path</text><path d="M${left} 102H${right}" stroke="var(--line)" stroke-dasharray="4 5"/>${paths}<path d="M272 175v23m-6-6 6 6 6-6" fill="none" stroke="var(--muted)" stroke-width="2"/><text x="${left}" y="231" font-size="23" fill="var(--ink)">Total into the rail (A)</text>${ticks}<path d="${line(model.sum, 248, 112, 780, 1220)}" fill="none" stroke="var(--teal)" stroke-width="4"/><text x="${right}" y="395" text-anchor="end" font-size="19" fill="var(--muted)">Time →</text></svg></section>`;
  };
  return `<div class="vrm-phase-comparison">${panel(1)}${panel(4)}</div>`;
}
