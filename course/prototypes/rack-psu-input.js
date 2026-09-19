import { renderElectricity } from './terminology-electricity.js';
import { rackProducts } from './rack-power-products.js';

const phases = ['power', 'data', 'heat'];
const psu = rackProducts['psu-hardware'];
const module = psu.items[0];
const text = (x, y, label, size = 26, color = 'text') =>
  `<text x="${x}" y="${y}" text-anchor="middle" font-size="${size}" fill="var(--${color})">${label}</text>`;
const line = (d, color = 'power', arrow = false) =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="3" stroke-linejoin="round" ${arrow ? 'marker-end="url(#psu-input-arrow)"' : ''}/>`;
const phaseOriginDegrees = 120;

function waveform(x, y, width, height) {
  return `<svg x="${x}" y="${y}" width="${width}" height="${height}" viewBox="95 165 990 225" preserveAspectRatio="none" overflow="hidden" aria-hidden="true" data-reused-figure="primer-three-phase">${renderElectricity('three-phase', { phaseOriginDegrees }, false)}</svg>`;
}

function waveformEnd(x, y, width, height, phase) {
  const angle = (phaseOriginDegrees - phase*120)*Math.PI/180;
  return [x + (1050-95)*width/990, y + (279-90*Math.sin(angle)-165)*height/225];
}

function phaseMapping(start, targetY, endX, phase, compact) {
  const [x, y] = start;
  const bendX = compact ? 205 : 408;
  const controlX = compact ? 188 : 374;
  return `<g data-phase-mapping="L${phase + 1}"><title>Color mapping from phase L${phase + 1} to its PSU input; the connector is not part of the time waveform.</title>
    ${line(`M${x} ${y}C${controlX} ${y} ${controlX} ${targetY} ${bendX} ${targetY}H${endX}`, phases[phase], true)}
    <circle cx="${x}" cy="${y}" r="4" fill="var(--${phases[phase]})"/>
  </g>`;
}

function modulePhoto(x, y, width, height, phase) {
  return `<g data-psu-phase="L${phase + 1}">
    <rect x="${x}" y="${y}" width="${width}" height="${height}" rx="8" fill="white" stroke="var(--${phases[phase]})" stroke-width="2"/>
    <svg x="${x + 8}" y="${y + 6}" width="${width - 16}" height="${height - 12}" viewBox="${module.crop}" overflow="hidden">
      <image href="../assets/references/${module.file}" width="${module.width}" height="${module.height}"/>
    </svg>
  </g>`;
}

function rackPhoto(x, y, width, height) {
  return `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="8" fill="white"/>
    <svg x="${x}" y="${y}" width="${width}" height="${height}" viewBox="998 112 318 558" overflow="hidden" data-rack-detail="rear">
    <image href="../assets/references/nvidia-dgx-gb300-rear-power-only.png" width="1426" height="813"/>
      <circle cx="1080" cy="485" r="18" fill="none" stroke="var(--power)" stroke-width="5"/>
    </svg>`;
}

export function renderPSUInput(state, compact) {
  let out = `<defs><marker id="psu-input-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="3.5" markerHeight="3.5" orient="auto-start-reverse"><path d="M1 1L9 5L1 9" fill="none" stroke="context-stroke" stroke-width="2"/></marker></defs>`;
  if (compact) {
    out += text(195, 28, 'Three-phase AC', 26);
    out += waveform(15, 116, 160, 160);
    out += text(93, 307, '480 V', 21, 'power');
    [0, 1, 2].forEach(i => {
      const y = 52 + i * 105;
      out += text(213, y + 23, `L${i + 1}`, 20, phases[i]);
      out += phaseMapping(waveformEnd(15, 116, 160, 160, i), y + 36, 233, i, true);
      out += modulePhoto(241, y, 130, 72, i);
      out += line(`M376 ${y + 36}H383`);
    });
    out += line('M383 88V343H195');
    out += text(195, 370, 'PSUs · 277 V AC → 50 V DC', 19);
    out += line('M195 384V405', 'power', true);
    out += rackPhoto(210, 405, 138, 240);
    out += text(94, 477, 'Rack busbar', 20);
    out += text(94, 509, '50 V DC', 24, 'power');
    out += line('M94 527V566H246', 'power', true);
    out += `<a href="${psu.source}" target="_blank" rel="noopener">${text(103, 666, 'Advanced Energy', 13, 'muted')}</a>`;
    out += `<a href="https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html" target="_blank" rel="noopener">${text(291, 666, 'NVIDIA · DGX GB300', 13, 'muted')}</a>`;
  } else {
    out += text(192, 45, 'Three-phase AC', 29);
    out += text(616, 45, 'PSU modules', 29);
    out += text(1039, 45, 'Rear rack busbar', 29);
    out += waveform(25, 185, 332, 187);
    out += text(192, 423, '480 V', 29, 'power');
    out += text(616, 83, '277 V AC → 50 V DC', 22);
    [0, 1, 2].forEach(i => {
      const y = 103 + i * 139;
      out += text(424, y + 35, `L${i + 1}`, 23, phases[i]);
      out += phaseMapping(waveformEnd(25, 185, 332, 187, i), y + 58, 483, i, false);
      out += modulePhoto(491, y, 250, 116, i);
      out += line(`M746 ${y + 58}H817`);
    });
    out += line('M817 161V439');
    out += line('M817 300H914', 'power', true);
    out += text(860, 271, '50 V DC', 21, 'power');
    out += rackPhoto(927, 83, 246, 420);
    out += `<a href="${psu.source}" target="_blank" rel="noopener">${text(616, 540, 'Advanced Energy · ORv3', 16, 'muted')}</a>`;
    out += `<a href="https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html" target="_blank" rel="noopener">${text(1039, 540, 'NVIDIA · DGX GB300', 16, 'muted')}</a>`;
  }
  return `<g data-psu-input="hardware">${out}</g>`;
}
