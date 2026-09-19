import {renderRejection} from './cooling-rejection.js';
import {chillerBalance, operatingPoint, heatReuse} from './heat-rejection-model.js';
import {outdoorWaterVisual} from './heat-rejection-outdoor.js';
import {torontoVisual} from './heat-rejection-toronto.js';
const n = (value, digits = 2) => Number(value.toFixed(digits)).toLocaleString('en-US');
const arrow = '<span class="h-arrow" aria-hidden="true">→</span>';
const stat = (value, label, extra = '') => `<div class="h-stat ${extra}"><strong>${value}</strong><span>${label}</span></div>`;
const node = (title, detail = '', extra = '') => `<div class="h-node ${extra}"><b>${title}</b>${detail ? `<span>${detail}</span>` : ''}</div>`;
const strip = text => `<p class="h-strip">${text}</p>`;
const stack = content => `<div class="h-stack">${content}</div>`;
const input = text => `<p class="h-input">${text}</p>`;
const route = (middle, sink, detail = '') => `<div class="h-route" aria-label="Heat path from rack through outdoor plant"><span>Rack heat</span>${arrow}<span>Facility water</span>${arrow}<span>${middle}</span>${arrow}<span>${sink}</span></div>${detail ? input(detail) : ''}`;
const panel = (title, body, extra = '') => `<section class="h-panel ${extra}"><h2>${title}</h2>${body}</section>`;
const legacy = (id, state, compact, label) => `<div class="h-legacy"><svg role="img" aria-label="${label}" viewBox="${compact ? '0 0 372 580' : '0 0 1160 420'}">${renderRejection(id, compact, state)}</svg></div>`;
function powerBar(p) {
  return `<div class="h-power"><div class="h-power-header"><span>Site electricity</span><b class="${p.electricalFits ? '' : 'h-warning'}">${n(p.totalMW)} / 10 MW</b></div><div class="h-power-track" role="img" aria-label="Computing ${n(p.requestedITMW)}, cooling ${n(p.coolingMW)}, other 0.4 MW: ${n(p.totalMW)} MW against a 10 MW limit"><span class="h-it" style="width:${p.requestedITMW / 11 * 100}%"></span><span class="h-cooling" style="width:${p.coolingMW / 11 * 100}%"></span><span class="h-other" style="width:${p.otherMW / 11 * 100}%"></span><i style="left:${10 / 11 * 100}%"><em>10 MW limit</em></i></div><div class="h-legend"><span><i class="h-it"></i>Computing ${n(p.requestedITMW)} MW</span><span><i class="h-cooling"></i>Cooling ${n(p.coolingMW)} MW</span><span><i class="h-other"></i>Other 0.4 MW</span></div></div>`;
}
function reuseChart(hours, compact) {
  const width = compact ? 520 : 920, left = compact ? 65 : 90, plotWidth = compact ? 420 : 790, top = 55, height = 190, bottom = top + height;
  const acceptedWidth = plotWidth * hours / 24;
  return `<svg class="h-reuse-plot" role="img" aria-label="The data center runs all 24 hours and produces 4 MW of heat continuously. ${hours ? `The neighboring factory, a separate heat customer, uses 2 MW for ${hours} hours.` : 'The neighboring factory needs no heat today.'} All remaining heat goes outdoors." viewBox="0 0 ${width} 300"><text x="${left + plotWidth / 2}" y="28" text-anchor="middle">Data center: 4 MW all day</text><rect x="${left}" y="${top}" width="${plotWidth}" height="${height}" class="h-reuse-available"/><rect x="${left}" y="${top + height / 2}" width="${acceptedWidth}" height="${height / 2}" class="h-reuse-accepted"/><path d="M${left} ${top}V${bottom}H${left + plotWidth}" class="h-chart-axis"/><path d="M${left} ${top + height / 2}H${left + plotWidth}" class="h-chart-grid"/><text x="${left - 15}" y="${top + 8}" text-anchor="end">4 MW</text><text x="${left - 15}" y="${top + height / 2 + 8}" text-anchor="end">2 MW</text><text x="${left - 15}" y="${bottom + 6}" text-anchor="end">0</text>${[0, 6, 12, 24].map(t => `<text x="${left + plotWidth * t / 24}" y="${bottom + 35}" text-anchor="${t === 0 ? 'start' : t === 24 ? 'end' : 'middle'}">${t} h</text>`).join('')}<text x="${left + plotWidth * .56}" y="${top + 62}" text-anchor="middle">Heat released outdoors</text>${hours ? `<text class="h-chart-light" x="${left + acceptedWidth / 2}" y="${bottom - 52}" text-anchor="middle">2 MW<tspan x="${left + acceptedWidth / 2}" dy="28">reused</tspan></text>` : ''}</svg>`;
}
export function heatRejectionVisual(id, state, compact = false) {
  if (id.startsWith('toronto-')) return torontoVisual(id, compact);
  if (id === 'heat-rejection-purpose') return `<div class="h-flow">${node('Collect','Chips warm rack coolant','h-water')}${arrow}${node('Carry','A separate facility loop','h-water')}${arrow}${node('Release','Outdoor equipment transfers heat','h-outdoors')}</div>`;
  if (id === 'abilene-cooling') return `<div class="h-case"><figure><img src="../assets/references/distribution-abilene-data-halls.jpg" alt="Oracle aerial photograph of the original Abilene data-center campus and its data halls."><figcaption><a href="https://www.oracle.com/data-centers/" target="_blank" rel="noopener">Oracle · Abilene aerial · July 15, 2026</a></figcaption></figure><div class="h-case-copy"><p class="h-date">Crusoe design account · August 2025</p><div class="h-vertical">${node('Facility water','Circulates and carries heat')}${arrow}${node('Air-cooled chiller','Uses electricity to move heat')}${arrow}${node('Outdoor air','Receives the heat')}</div><p class="h-credit"><a href="https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center" target="_blank" rel="noopener">Non-evaporative rejection. Fill and maintenance still use water.</a></p></div></div>`;
  if (id === 'rejection') return legacy('rejection', state, compact, 'Dry coil and evaporative tower heat and water paths');
  if (id === 'bulb-definitions') return `<div class="h-definition"><blockquote><p><strong>Dry-bulb temperature</strong> is the air temperature measured with a dry, shaded thermometer.</p><p><strong>Wet-bulb temperature</strong> is measured with a thermometer covered in a water-soaked cloth and exposed to airflow. Evaporation cools it.</p></blockquote><p class="h-saturation">Think of it like sweating!</p></div>`;
  if (id === 'weather') {
    const humid = state.humidity === 'humid', wet = humid ? 28 : 22;
    return stack(`<div class="h-two">${panel('Ordinary air temperature', `${stat('35°C','Dry bulb')}<div class="h-thermometer"><span style="height:87.5%"></span></div>`)}${panel('Temperature of a wetted sensor', `${stat(`${wet}°C`,'Wet bulb')}<div class="h-thermometer h-wet"><span style="height:${wet / 40 * 100}%"></span></div>`)}</div><p class="h-cause">${humid ? 'Less water evaporates. The wetted sensor stays warmer.' : 'Water evaporates into dry air. The wetted sensor cools more.'}</p>`);
  }
  if (id === 'approach-outdoors' || id === 'approach-wet') return outdoorWaterVisual(id,state,compact);
  if (id === 'chiller-balance') {
    const m = chillerBalance();
    return stack(`<div class="h-chiller" aria-label="10 MW of computing heat plus 2 MW of compressor power equals 12 MW of heat released outdoors.">${stat(`${n(m.dutyMW)} MW`,'Heat from computing')}${arrow}<div class="h-machine"><div class="h-work">+ ${n(m.compressorMW)} MW <span>Compressor electricity</span><span>Also becomes heat ↓</span></div>${node('Chiller','Refrigeration lowers the supply temperature')}</div>${arrow}${stat(`${n(m.condenserMW)} MW`,'Computing heat + compressor heat','h-warm')}</div>${strip('Without a compressor, outdoor cooling can still remove all 10 MW—if temperatures and capacity allow.')}`);
  }
  if (id === 'cooling-cop') return stack(`${input('Whole cooling plant · pumps and fans included')}<div class="h-cop-picture"><div><div class="h-energy-blocks h-electricity"><i></i></div><p>1 unit of electricity</p></div>${arrow}<div><div class="h-energy-blocks">${'<i></i>'.repeat(4)}</div><p>4 units of heat moved</p></div></div><div class="h-cop-caption">Coefficient of performance: <b>COP 4</b></div>`);
  if (id === 'plant-options') return '<figure class="h-supplied-slide"><img src="../assets/references/economizer-mode-user.png" alt="Cool weather can let the compressor rest: warm water transfers heat to outdoor air and returns cool; economizer mode keeps fans and pumps on while the compressor is off."></figure>';
  if (id === 'adiabatic-boost') return `<figure class="h-supplied-slide"><img src="../assets/references/adiabatic-nitrous-boost-user.png" alt="A driver presses a nitrous-boost button in a racing game: an analogy for adding cooling assistance when needed."></figure>`;
  if (id === 'adiabatic-assist') return `<figure class="h-supplied-slide"><img src="../assets/references/adiabatic-wetted-pad-user.png" alt="Adiabatic assist: makeup water wets a pad and evaporates, precooling incoming air. The cooler air passes over a dry coil and leaves warmer; coolant stays inside the tubes."></figure>`;
  if (id === 'hot-hour') {
    const p = operatingPoint({condition:state.condition, requestedITMW:state.requestedITMW});
    const weather = state.condition === 'cool' ? 'Cool' : 'Hot';
    const balance = stack(`${input('Illustrative whole-plant COP · includes pumps and fans')}<div class="h-cop-equation" role="group" aria-label="${weather} weather: ${n(p.requestedITMW)} MW of computing heat divided by COP ${n(p.cop)} requires ${n(p.coolingMW)} MW of cooling electricity.">${stat(`${n(p.requestedITMW)} MW`, 'Computing heat')}<span class="h-cop-operator" aria-hidden="true">÷</span>${stat(n(p.cop), `${weather}-weather COP`)}<span class="h-cop-operator" aria-hidden="true">=</span>${stat(`${n(p.coolingMW)} MW`, 'Cooling electricity', 'h-warm')}</div>${powerBar(p)}<div class="h-capacity-line"><span class="${p.thermalFits ? 'h-pass-text' : 'h-warning'}">Heat removal: ${n(p.requestedITMW)} of ${n(p.thermalMW)} MW</span><b class="${p.electricalFits ? 'h-pass-text' : 'h-warning'}">${p.electricalFits ? 'Both limits fit' : 'Electricity exceeds the limit'}</b></div>`);
    return `<div class="h-hot-hour">${balance}<figure class="h-hot-day-meme"><a href="../assets/references/continuity-datacentres-cartoon.png" target="_blank" rel="noopener" aria-label="Open full-size hot-day cartoon"><img src="../assets/references/continuity-datacentres-cartoon.png" alt="A man drinks water on a hot day. Another says: Take it easy buddy. Think of the data centres."></a></figure></div>`;
  }
  if (id === 'closed-loop-water') {
    const tower = state.closedSink === 'tower';
    return `<div class="h-flow">${node('Closed rack loop','Coolant recirculates','h-water')}${arrow}${node('Closed facility loop',tower ? 'Heat crosses a separating exchanger' : 'Water / glycol stays in the coil','h-water')}${arrow}${node(tower ? 'Evaporatively cooled tower' : 'Dry cooler', tower ? 'Tower water contacts air and evaporates' : 'Outdoor air receives the heat','h-outdoors')}</div>`;
  }
  if (id === 'water-ledger') {
    const stage = state.mineralStage, refill = stage === 'refill', purge = stage === 'purge';
    const dots = Array.from({length:refill ? 7 : purge ? 4 : 10},(_,i)=>`<i style="left:${12+(i*23)%77}%;bottom:${12+(i*17)%48}%"></i>`).join('');
    return stack(`<div class="h-minerals" data-mineral-stage="${stage}"><div class="h-water-event">${refill ? 'Fresh makeup water enters ↓' : purge ? 'Some concentrated water is discharged ↓' : 'Water evaporates and carries heat upward ↑'}</div><div class="h-basin"><div class="h-basin-water" style="height:${refill ? 78 : purge ? 19.2 : 48}%">${dots}</div><span>Dissolved minerals</span></div><p>${refill ? 'Replacement water restores the level and dilutes the remaining minerals.' : purge ? 'This discharge is called blowdown. It removes some of the minerals.' : 'The minerals remain as the water level falls. Their concentration rises.'}</p></div>`);
  }
  if (id === 'heat-reuse') {
    const m = heatReuse({receiverHours:state.receiverHours});
    return stack(`${input(m.acceptedMWh ? 'Example: a neighboring factory needs 2 MW of heat for a 6-hour process.' : 'Example: the neighboring factory needs no heat today.')}${reuseChart(state.receiverHours, compact)}${strip(m.acceptedMWh ? 'The factory uses half the heat for 6 hours. Outdoor equipment removes the rest.' : 'The data center still produces 4 MW, all day. Outdoor equipment removes all of it.')}`);
  }
  if (id === 'water-restriction') return stack(`${input('Operating dependencies · initial fill excluded')}<div class="h-two">${panel('Dry, non-evaporative cooling','<p class="h-cause">Electricity</p>')}${panel('Wet cooling tower','<p class="h-cause">Electricity and water</p>')}</div>`);
  throw new RangeError(`Unknown heat-rejection scene: ${id}`);
}
