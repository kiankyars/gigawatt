/* Pure visual factory shared by the original sample and consolidated Chapter 8. */
export function createPresentationRenderers({ defaults: DEFAULTS, getState, getStep, isRevealed, acdcConductorModel, escapeHTML, fmt, assets = "assets/" }) {
function metric(value, unit) { return `<div class="metric">${value} <small>${unit}</small></div>`; }
function intro() {
  const label=getStep()?.introLabel || '480 V three-phase AC ↔ 800 V DC';
  return `<div class="hero"><div class="hero-copy"><span class="chip">${escapeHTML(label)}</span><div class="hero-number">100<small> kW</small></div><span class="hero-goal">Same power delivered to the load</span></div><img src="${assets}power-equipment.png" width="1672" height="941" alt="Concept illustration of conversion equipment beside a compute rack." /></div>`;
}
function conductorNumbers(volts = DEFAULTS.comparison_voltage_v) {
  return acdcConductorModel(
    DEFAULTS.power_kw,
    DEFAULTS.reference_voltage_v,
    volts,
    DEFAULTS.power_factor,
    DEFAULTS.conductor_ohms,
    DEFAULTS.hours,
  );
}
function conductors(labels) {
  return `<div class="conductor-lines" aria-label="${labels.length} current-carrying conductors">${labels.map((label) => `<div><span>${label}</span><i></i></div>`).join("")}</div>`;
}
function copper() {
  function bundle(supply, labels) {
    return `<div class="copper-bundle" data-supply="${supply}" aria-label="${labels.length} copper conductors of equal length and cross-section">${labels.map((label) => `<div class="copper-row"><span>${label}</span><i class="copper-bar" aria-hidden="true"></i></div>`).join("")}${supply === "dc" ? '<div class="copper-row copper-removed" aria-label="One fewer conductor"><span>−1</span><i aria-hidden="true"></i></div>' : ""}</div>`;
  }
  return `<div class="model copper-model"><div class="model-top"><span class="chip">SAME 100 kW DELIVERED</span><span class="ledger-formula">Equal length, cross-section and material</span></div><div class="comparison"><section class="metric-card"><p class="metric-label">480 V three-phase AC</p>${bundle("ac", ["L1", "L2", "L3"])}<p class="copper-quantity"><strong>3</strong> equal copper lengths</p></section><section class="metric-card changed"><p class="metric-label">800 V DC</p>${bundle("dc", ["+", "−"])}<p class="copper-quantity"><strong>2</strong> equal copper lengths</p></section></div></div>`;
}
function current() {
  const { ac, dc } = conductorNumbers(getState().volts);
  const shown = isRevealed();
  return `<div class="model"><div class="model-top"><span class="chip">${DEFAULTS.power_kw} kW REAL POWER · AC PF = ${DEFAULTS.power_factor}</span><span class="ledger-formula">Current in each conductor</span></div><div class="comparison"><div class="metric-card"><p class="metric-label">${DEFAULTS.reference_voltage_v} V three-phase AC</p>${metric(shown ? fmt(ac.amps, 1) : "?", "A")}<p class="metric-sub">RMS · I = P / (√3 × V<sub>LL</sub> × PF)</p>${conductors(["L1", "L2", "L3"])}</div><div class="metric-card changed"><p class="metric-label"><span id="variable-voltage">${getState().volts}</span> V DC</p><div id="variable-current">${metric(shown ? fmt(dc.amps, 1) : "?", "A")}</div><p class="metric-sub" id="variable-derivation">${shown ? `${fmt(DEFAULTS.power_kw * 1000)} W ÷ ${getState().volts} V` : "I = P / V"}</p>${conductors(["+", "−"])}</div></div>${shown ? `<div class="control-line"><label for="voltage">Try another DC voltage</label><input id="voltage" type="range" min="400" max="1000" step="1" value="${getState().volts}" /><output id="voltage-value" for="voltage">${getState().volts} V</output><button id="reset-voltage">800 V</button></div>` : `<div class="control-line"><button class="reveal" id="reveal">Reveal the currents</button></div>`}</div>`;
}
function loss() {
  const shown = isRevealed(),
    { ac, dc, lossRatio } = conductorNumbers();
  return `<div class="model"><div class="model-top"><span class="chip">100 kW delivered · PF = 1</span><span class="ledger-formula">10 mΩ per conductor</span></div><div class="comparison"><section class="metric-card"><p class="metric-label">480 V three-phase AC</p>${metric(fmt(ac.lossKW * 1000), "W heat")}<p class="metric-sub">P<sub>heat</sub> = 3 I<sub>RMS</sub>²R<br>3 × 120.3² × 0.01</p><div class="loss-track"><div class="loss-bar" style="width:100%"></div></div></section><section class="metric-card changed"><p class="metric-label">800 V DC</p>${metric(shown ? fmt(dc.lossKW * 1000, 1) : "?", "W heat")}<p class="metric-sub">P<sub>heat</sub> = 2 I²R<br>2 × 125² × 0.01</p><div class="loss-track">${shown ? `<div class="loss-bar" style="width:${lossRatio * 100}%"></div>` : ""}</div></section></div>${shown ? `<p class="comparison-result"><strong>${fmt((ac.lossKW - dc.lossKW) * 1000)} W less heat</strong></p>` : `<div class="control-line"><button class="reveal" id="reveal">Calculate DC conductor heat</button></div>`}</div>`;
}
function unit(label, style = "", detail = "") {
  return `<div class="unit ${style}">${label}${detail ? `<small>${detail}</small>` : ""}</div>`;
}
function architecture(kind) {
  const converter = unit("AC → DC", "converter", "conversion");
  const regulator = unit("DC → DC", "converter", "device regulation");
  const chip = unit("Compute", "chip-unit", "low device voltage");
  const arrow = '<span class="wire" aria-hidden="true">→</span>';
  let facility, adjacent, rack;
  if (kind === "ac") {
    facility = unit("Facility AC");
    adjacent = unit("AC path");
    rack = converter + arrow + regulator + arrow + chip;
  }
  if (kind === "sidecar") {
    facility = unit("Facility AC");
    adjacent = converter + arrow + unit("800 V DC");
    rack = regulator + arrow + chip;
  }
  if (kind === "facility") {
    facility = converter;
    adjacent = unit("800 V DC", "", "hall distribution");
    rack = regulator + arrow + chip;
  }
  const space = `<div class="rack-space ${kind === "ac" ? "occupied" : "released"}"><span>AC/DC equipment space</span><strong>${kind === "ac" ? "Occupied" : "Freed"}</strong></div>`;
  const step = getStep();
  const roadmap = `<div class="roadmap-context"><span class="chip">${escapeHTML(step.roadmap_label)}</span>${kind === "ac" ? "" : '<a href="https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part" target="_blank" rel="noopener">SemiAnalysis forecast · May 2026</a>'}</div>`;
  return `<div class="architecture">${roadmap}<div class="path"><section class="zone ${kind === "facility" ? "active" : ""}"><h2 class="zone-title">Upstream power room</h2><div class="zone-body">${facility}</div></section><section class="zone ${kind === "sidecar" ? "active" : ""}"><h2 class="zone-title">${kind === "sidecar" ? "Power rack (sidecar)" : "Hall distribution"}</h2><div class="zone-body">${adjacent}</div></section><section class="zone rack ${kind === "ac" ? "active" : ""}"><h2 class="zone-title">Compute rack</h2><div class="zone-body">${rack}</div>${space}</section></div></div>`;
}
function conversionViews() {
  const tabs = `<div class="conversion-views">${[
    ["supply", "Supply path"],
    ["heat", "Converter losses"],
  ]
    .map(
      ([view, label]) =>
        `<button data-converter-view="${view}" aria-pressed="${getState().converterView === view}">${label}</button>`,
    )
    .join("")}</div>`;
  return tabs + (getState().converterView === "heat" ? conversionLoss() : conversionSupply());
}
function conversionSupply() {
  return `<div class="stepdown-example"><div class="stepdown-path"><section><p class="metric-label">Incoming supply</p><strong>Medium-voltage AC</strong><span>13.8 kV example</span></section><b aria-hidden="true">→</b><section><p class="metric-label">Transformer</p><strong>13.8 kV → 480 V AC</strong><span>Step-down + isolation</span></section><b aria-hidden="true">→</b><section class="stepdown-electronics"><p class="metric-label">Controlled converter</p><strong>480 V AC → 800 V DC</strong><span>Rectification + regulation</span></section></div></div>`;
}

function conversionLoss() {
  const output = DEFAULTS.power_kw,
    efficiency = DEFAULTS.converter_efficiency;
  const input = output / efficiency,
    loss = input - output,
    shown = isRevealed();
  return `<div class="converter-example"><div class="model-top"><span class="chip">One AC/DC power supply · 98% efficiency assumed</span></div><div class="converter-flow"><div class="power-port"><span>480 V three-phase AC input</span><strong>${shown ? fmt(input, 2) : "?"}<small> kW</small></strong></div><span class="conversion-arrow" aria-hidden="true">→</span><div class="converter-box"><strong>Electronic AC/DC converter</strong><span>Useful output ÷ input = 98%</span></div><span class="conversion-arrow" aria-hidden="true">→</span><div class="power-port"><span>800 V DC output</span><strong>100<small> kW</small></strong></div><div class="converter-heat"><span aria-hidden="true">↓</span><strong>${shown ? fmt(loss, 2) : "?"} kW <small>converter heat</small></strong></div></div><div class="loss-causes"><span>Current heats components</span><span>Switching dissipates energy</span><span>Magnetic cores heat up</span></div>${shown ? '<div class="equation-block">100 ÷ 0.98 − 100 = <strong>2.04 kW</strong></div>' : '<div class="control-line"><button class="reveal" id="reveal">Calculate the lost power</button></div>'}</div>`;
}
function sourceFigure() {
  const figure = getStep().figure;
  const asset = `${assets}${figure.asset}`;
  return `<figure class="source-figure"><a class="source-image" href="${escapeHTML(asset)}" target="_blank" rel="noopener" aria-label="Open diagram at full size"><img src="${escapeHTML(asset)}" alt="${escapeHTML(figure.alt)}"></a><figcaption><span>${escapeHTML(figure.credit)}</span><a href="${escapeHTML(figure.source_url)}" target="_blank" rel="noopener">${escapeHTML(figure.source_title)}</a><a href="${escapeHTML(asset)}" target="_blank" rel="noopener">Open full size ↗</a></figcaption></figure>`;
}

return { intro, copper, current, loss, architecture, conversionViews, conversionSupply, conversionLoss, sourceFigure, conductorNumbers };
}
