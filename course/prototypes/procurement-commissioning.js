import {acceptedPaths, commissionedService} from './procurement-model.js';

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
    ['Cable', 'Internal wiring → module terminals', 'Field cable → correct rack branch', 'Connections + protection settings'],
    ['Pipe', 'Internal manifold → module flanges', 'Field pipe → correct rack branch', 'Fluid + leak integrity + measured flow'],
    ['Controls', 'Controller → factory test setup', 'Actual sensor → correct rack group', 'Point mapping + observed action'],
  ];
  return `<div class="p-stack pc-stack">
    <div class="pc-scope-table" role="table" aria-label="Factory scope and installed checks">
      <div class="pc-scope-heading" role="row"><span role="columnheader">Connection</span><h2 role="columnheader">Factory test scope</h2><h2 role="columnheader">Installed checks at the site</h2></div>
      ${rows.map(([label, factory, installed, check]) => `<div class="pc-scope-row" role="row"><b role="rowheader">${label}</b><div class="pc-factory-cell" role="cell"><span>${factory}</span></div><div role="cell"><strong>${installed}</strong><span>${check}</span></div></div>`).join('')}
    </div>
    ${strip('Test the assembly. Check its field connections. Then test the joined service.')}
    ${note('Record the tested revision, conditions and results. A shipment release covers its declared factory scope.')}
  </div>`;
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
  return `<div class="p-stack pc-stack">
    <div class="p-shared-plant">Shared upstream plant + controls</div>
    <div class="p-phase-links" aria-hidden="true"><span>↓</span><span>↓</span></div>
    <div class="p-two pc-phase-pair"><section class="p-card positive"><h2>Phase A · operating</h2><p>Keep its tested service within the accepted limits.</p></section><section class="p-card warning"><h2>Phase B · construction</h2><p>Its connection changes the shared system.</p></section></div>
    <div class="pc-phase-checks"><b>Before connecting B</b><span>Agree isolation ownership</span><span>Check shared capacity</span><span>Retest affected functions</span></div>
    ${note('A previous acceptance record applies to the configuration that was tested.')}
  </div>`;
}

function releaseDecision(state) {
  const m = commissionedService();
  const selected = ['all', 'proven', 'wait'].includes(state.diagnosis) ? state.diagnosis : '';
  const reveal = Boolean(state.showDiagnosis && selected);
  const responses = {
    all: 'A41–A60 has a command record but no measured failure response. Forty complete paths do not yet establish forty racks eligible for service.',
    proven: `Release A21–A40: ${m.count} racks × 200 kW = ${m.envelopeMW} MW. Those same racks have complete paths and a measured response that meets the agreed limits and timing.`,
    wait: `A21–A40 already meets every stated criterion. Its ${m.count} racks can enter service within the tested configuration and limits.`,
  };
  return `<div class="pc-release">
    <section class="pc-release-evidence"><div class="pc-release-context"><span>Same 100 revised racks · 200 kW each</span><h2>Now inspect the failure-response records</h2></div><div class="pc-evidence-row"><b>A21–A60 · 40 racks</b><span>All three service paths accepted</span></div><div class="pc-evidence-row pc-evidence-measured"><b>A21–A40 · 20 racks</b><span>Measured response meets agreed limits and timing</span></div><div class="pc-evidence-row pc-evidence-pending"><b>A41–A60 · 20 racks</b><span>Command sent; response unconfirmed</span></div><p>All other acceptance criteria are met.<br>Other racks lack a complete accepted path.</p></section>
    <section class="pc-release-answer"><h2>Which racks can enter service?</h2><div class="p-answer-options pc-answer-options">${[['all', 'A21–A60 · all 40 with complete paths'], ['proven', 'A21–A40 · only the 20 with a passing response'], ['wait', 'None · wait for all 100 racks']].map(([value, label]) => `<button type="button" data-diagnosis="${value}" aria-pressed="${selected === value}">${label}</button>`).join('')}</div><button type="button" id="diagnosis-reveal" class="p-reveal" ${selected ? '' : 'disabled'} aria-expanded="${reveal}">${reveal ? 'Hide reasoning' : 'Check the decision'}</button><div class="pc-release-feedback ${reveal ? selected === 'proven' ? 'pc-correct' : 'pc-recheck' : ''}" role="status"${reveal ? ` data-release-eligible="${m.count}" data-release-mw="${m.envelopeMW}"` : ''}>${reveal ? `<p>${responses[selected]}</p><p class="pc-handover">Handover: name the released racks, tested configuration and operating limits. Record excluded racks and the evidence still required.</p>` : ''}</div></section>
  </div>`;
}

export function procurementCommissioningVisual(id, state = {}) {
  switch (id) {
    case 'controls-interface': return controls(state);
    case 'factory-acceptance': return factoryAcceptance();
    case 'integrated-tests': return integratedTest(state);
    case 'accepted-paths': return accepted(state);
    case 'phase-boundary': return phaseBoundary();
    case 'release-decision': return releaseDecision(state);
    default: return null;
  }
}
