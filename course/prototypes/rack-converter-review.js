import { phaseWaveforms } from './rack-power-model.js';

export function renderCorePath() {
  return `<div class="core-path"><div class="core-flow"><section><h2>PSU</h2><p>AC → 51 V DC</p></section><b>→</b><section><h2>VRM</h2><p>Makes and regulates the core voltage</p></section><b>→</b><section class="core-rail"><h2>Vcore rail</h2><p>The copper path carrying ~1 V</p></section><b>→</b><section><h2>CPU cores</h2></section></div><div class="core-support"><strong>Local capacitors</strong><span>Connect to the rail beside the chip</span></div></div>`;
}

export function renderConversionChoices() {
  return `<div class="converter-choices"><section><h2>Direct conversion</h2><div class="converter-route"><span class="route-input">51 V</span><span class="route-wire">51 V distribution</span><div class="near-chip"><span class="route-converter">VRM<br><strong>51 V → 1 V</strong></span><span class="short-rail">1 V</span><span class="route-chip">Cores</span></div></div></section><section><h2>With an intermediate rail</h2><div class="converter-route"><span class="route-input">51 V</span><span class="route-converter">Bus converter<br><strong>51 V → 12 V</strong></span><span class="route-wire">12 V distribution</span><div class="near-chip"><span class="route-converter">VRM<br><strong>12 V → 1 V</strong></span><span class="short-rail">1 V</span><span class="route-chip">Cores</span></div></div></section><p class="conversion-principle">Keep the 1 V path short in either design.</p><p class="conversion-efficiency">Two-stage efficiency multiplies: <strong>98% × 95% = 93.1%</strong></p></div>`;
}

export function renderVRMPhases(state = {}, compact = false) {
  const count = state.phases || 4, model = phaseWaveforms(count);
  const W = compact ? 380 : 1120, left = compact ? 42 : 85, right = W - 18;
  const colors = ['var(--teal)', 'var(--amber)', 'var(--phase-three)', 'var(--ink)'];
  const line = (curve,x,y,w,h,min,max) => curve.map((v,i)=>`${i?'L':'M'}${(x+i/(curve.length-1)*w).toFixed(2)} ${(y+h-(v-min)/(max-min)*h).toFixed(2)}`).join(' ');
  const cellW = (right-left)/count, rowY = 48, rowH = compact ? 102 : 135;
  const perPath = model.totalAmps/count;
  const paths = model.curves.map((curve,i)=>`<g><text x="${left+cellW*(i+.5)}" y="${rowY-10}" text-anchor="middle" fill="${colors[i]}" font-size="${compact?14:20}">Path ${i+1}</text><rect x="${left+i*cellW+5}" y="${rowY}" width="${cellW-10}" height="${rowH}" rx="8" fill="var(--surface-soft)"/><path d="${line(curve,left+i*cellW+12,rowY+16,cellW-24,rowH-32,perPath*.75,perPath*1.25)}" fill="none" stroke="${colors[i]}" stroke-width="3"/></g>`).join('');
  const graphY = compact?264:302, graphH=130;
  const ticks = [800,1000,1200].map(v=>{const y=graphY+graphH-(v-780)/440*graphH;return `<path d="M${left} ${y}H${right}" stroke="var(--line)" stroke-dasharray="4 5"/><text x="${left-8}" y="${y+5}" text-anchor="end" font-size="${compact?12:18}" fill="var(--muted)">${v}</text>`;}).join('');
  return `<div class="vrm-phase-view"><div class="vrm-context">One VRM · ${count===1?'one switching path':'four switching paths'} · one core rail<small>Each path has switches and an inductor.</small></div><svg viewBox="0 0 ${W} ${compact?450:492}" role="img" aria-label="${count} switching paths inside one VRM. Their inductor currents combine to an average of 1,000 amperes; staggered paths make the combined current steadier.">${paths}<text x="${W/2}" y="${rowY+rowH+30}" text-anchor="middle" font-size="${compact?15:22}" fill="var(--muted)">Current from each path</text><text x="${W/2}" y="${graphY-25}" text-anchor="middle" font-size="${compact?18:25}" fill="var(--ink)">Combined current into the core rail (A)</text>${ticks}<path d="${line(model.sum,left,graphY,right-left,graphH,780,1220)}" fill="none" stroke="var(--teal)" stroke-width="4"/><text x="${right}" y="${graphY+graphH+25}" text-anchor="end" font-size="${compact?14:18}" fill="var(--muted)">Time →</text></svg><p class="vrm-summary">${count===1?'One path carries all the current.':'The paths take turns increasing and decreasing current.'}</p></div>`;
}
