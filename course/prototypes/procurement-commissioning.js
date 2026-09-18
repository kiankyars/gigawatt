import {acceptedPaths} from './procurement-model.js';

const arrow = '<span class="pc-arrow" aria-hidden="true">→</span>';
const strip = text => `<div class="p-strip pc-strip">${text}</div>`;
const note = text => `<p class="p-condition pc-note">${text}</p>`;
const rackIcon = '<span class="pc-rack-icon" aria-hidden="true"><i></i><i></i><i></i><i></i></span>';
const coolingIcon = '<span class="pc-cooling-icon" aria-hidden="true"><i></i><b>×</b><i></i></span>';

function responseTrace(measured) {
  return `<div class="pc-response-trace ${measured ? 'pc-measured' : 'pc-pending'}">
    <svg viewBox="0 0 260 112" role="img" aria-label="${measured ? 'Qualitative power versus time: measured power falls after the command; compare with agreed criteria.' : 'Qualitative power versus time: reduction was requested; an observed response is still missing.'}">
      <path class="pc-trace-axis" d="M32 20 V88 H248" />
      <path class="pc-trace-before" d="M33 34 H105" />
      <path class="pc-trace-command" d="M106 20 V90" />
      ${measured ? '<path class="pc-trace-after" d="M106 34 H125 L145 72 H245" />' : '<path class="pc-trace-missing" d="M112 34 H245" /><text x="178" y="71" text-anchor="middle">Awaiting measurement</text>'}
      <text x="7" y="12">Power</text><text x="248" y="106" text-anchor="end">Time</text>
      <text x="106" y="106" text-anchor="middle">Command</text>
    </svg>
    <span>${measured ? 'Qualitative trend · no calibrated scale' : 'No measured power response yet'}</span>
  </div>`;
}

function responsePath({phase = 'measured', measured = false} = {}) {
  const commanded = phase !== 'fault';
  const observed = phase === 'measured' && measured;
  return `<div class="pc-response-path">
    <section class="pc-response-step pc-fault"><span class="pc-step-number">1 · Physical event</span>${coolingIcon}<h2>Cooling path fails</h2><p>Identify the affected<br><b>A21–A40 racks</b>.</p></section>
    ${arrow}
    <section class="pc-response-step ${commanded ? 'pc-active' : 'pc-not-yet'}"><span class="pc-step-number">2 · Correct target</span>${rackIcon}<h2>${commanded ? 'Reduction commanded' : 'Command not sent yet'}</h2><p>${commanded ? 'The authorized command reaches <b>A21–A40</b>.' : 'The mapped rack group must receive the action.'}</p></section>
    ${arrow}
    <section class="pc-response-step ${observed ? 'pc-observed' : 'pc-not-yet'}"><span class="pc-step-number">3 · Observed outcome</span>${phase === 'fault' ? '<div class="pc-awaiting">No response evidence</div>' : responseTrace(observed)}<h2>${observed ? 'Power reduction measured' : 'Response unconfirmed'}</h2><p>${observed ? 'Check the record against the agreed acceptance criteria.' : 'Sending a request does not establish the response.'}</p></section>
  </div>`;
}

function controls(state) {
  const measured = state.action === 'confirmed';
  return `<div class="p-stack pc-stack" data-action="${measured ? 'confirmed' : 'unconfirmed'}">
    ${responsePath({measured})}
    ${strip(measured ? 'The measured result closes the command loop.' : 'Follow the fault all the way to the observed rack response.')}
    ${note('After the rack change, verify the physical branch, sensor and command target refer to the same new rack group.')}
  </div>`;
}

function factoryAcceptance() {
  const rows = [
    ['Internal wiring and protection', 'Field cables and protection coordination'],
    ['Internal piping and leak tests', 'Field joints and measured flow'],
    ['Controller logic with simulated signals', 'Real sensors and equipment response'],
  ];
  return `<div class="pc-scope-table pc-factory-table" role="table" aria-label="Factory tests and remaining site tests">
      <div class="pc-scope-heading" role="row"><h2 role="columnheader">Tested in the factory</h2><h2 role="columnheader">Checked at the site</h2></div>
      ${rows.map(([factory, site]) => `<div class="pc-scope-row" role="row"><div class="pc-factory-cell" role="cell">${factory}</div><div role="cell">${site}</div></div>`).join('')}
    </div>
  `;
}

function integratedTest(state) {
  const phase = ['fault', 'command', 'measured'].includes(state.testPhase) ? state.testPhase : 'fault';
  const status = {
    fault: 'The cooling fault identifies the racks that need a response.',
    command: 'The command is on record. The outcome still needs measurement.',
    measured: 'Accept the response only when measured power, timing and temperatures meet the agreed criteria.',
  };
  return `<div class="p-stack pc-stack" data-test-phase="${phase}">
    <div class="pc-test-brief"><b>One agreed cooling-failure test</b><span>Same revised 200 kW racks · A21–A40</span></div>
    ${responsePath({phase, measured: phase === 'measured'})}
    ${strip(status[phase])}
    ${note('Before testing, agree measurement points, numerical limits, response time, stop criteria and who can act.')}
  </div>`;
}

function accepted(state) {
  const coolingStart = state.coolingStart === 1 ? 1 : 21;
  const m = acceptedPaths({coolingStart, rackKW: 200});
  const row = (label, start, end, cls) => `<div class="p-acceptance-lane"><b>${label}</b><div>${[1,21,41,61,81].map(from => `<span class="${from >= start && from + 19 <= end ? cls : ''}">A${String(from).padStart(2, '0')}–${String(from + 19).padStart(2, '0')}</span>`).join('')}</div></div>`;
  const range = coolingStart === 21 ? 'A21–A60' : 'A01–A60';
  return `<div class="p-stack pc-stack">
    ${note('Same revised phase · 100 racks × 200 kW = 20 MW')}
    <div class="p-acceptance-map pc-acceptance-map">${row('Electrical', 1, 80, 'power')}${row('Cooling', coolingStart, 100, 'water')}${row('Network', 1, 60, 'network')}${row('All three', coolingStart, 60, 'complete')}</div>
    <div class="pc-accepted-result"><strong>${m.count} racks · ${m.envelopeMW} MW</strong><span>${range} · 200 kW each</span></div>
    ${strip(coolingStart === 21 ? 'The records overlap at A21–A60. Count those same rack identities.' : 'New cooling evidence adds A01–A20 to the complete paths.')}
    ${note('All other acceptance criteria are met for this comparison.')}
  </div>`;
}

function phaseBoundary() {
  // Two equal-aspect photographic viewports, wholly inside the source photos.
  // The bundled source is a flattened investor slide; keep its text and borders out.
  const image = '../assets/references/applied-digital-polaris-forge-1-building1-october-2025.jpg';
  const crop = (viewBox, label) => `<svg viewBox="${viewBox}" role="img" aria-label="${label}" preserveAspectRatio="xMidYMid meet"><image href="${image}" x="0" y="0" width="1368" height="829" /></svg>`;
  return `<div class="pc-polaris-phase">
    <figure class="pc-polaris-photos"><div class="pc-polaris-gallery">${crop('225 175 770 275', 'Polaris Forge 1 Building 1 and surrounding infrastructure, from Applied Digital’s October 2025 presentation')}${crop('60 480 700 250', 'A second aerial view of Polaris Forge 1 Building 1 from the same October 2025 presentation')}</div><figcaption><a href="https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-25-000076/apld_invxfinalpresentati.htm" target="_blank" rel="noreferrer">Applied Digital · October 2025 presentation, p. 22 · two views of Building 1</a></figcaption></figure>
    <div class="pc-polaris-milestones"><div class="pc-polaris-location"><h2>Polaris Forge 1 · Ellendale</h2><p>Applied Digital · leased to CoreWeave</p></div>
      <div class="p-phase-milestone"><time datetime="2025-10-27">27 Oct 2025</time><strong>50 MW</strong><span>Phase I ready for service</span></div>
      <div class="p-phase-milestone"><time datetime="2025-11-24">24 Nov 2025</time><strong>+50 MW</strong><span>First 100 MW building complete</span></div>
    </div>
  </div>`;
}

export function procurementCommissioningVisual(id, state = {}) {
  switch (id) {
    case 'controls-interface': return controls(state);
    case 'factory-acceptance': return factoryAcceptance();
    case 'integrated-tests': return integratedTest(state);
    case 'accepted-paths': return accepted(state);
    case 'phase-boundary': return phaseBoundary();
    default: return null;
  }
}
