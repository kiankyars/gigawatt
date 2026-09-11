const PRESENTATION = JSON.parse(
  document.getElementById("presentation-data").textContent,
);
const STEPS = PRESENTATION.steps;
const DEFAULTS = PRESENTATION.defaults;
const notesMode = document.body.dataset.view === "notes";
const teachingMode = document.body.dataset.view === "teach";
const studentMode = !notesMode && !teachingMode;
const byId = (id) => document.getElementById(id);
const escapeHTML = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const fmt = (value, decimals = 0) =>
  value.toLocaleString("en-US", { maximumFractionDigits: decimals });
let index = Math.max(
  0,
  STEPS.findIndex(
    (step) =>
      step.id ===
      (PRESENTATION.aliases?.[location.hash.slice(1)] ||
        location.hash.slice(1)),
  ),
);
let state = {
  index,
  revealed: [],
  volts: DEFAULTS.comparison_voltage_v,
  cycleDegrees: 30,
};
const session =
  new URLSearchParams(location.search).get("session") || crypto.randomUUID();
const channel =
  !studentMode && typeof BroadcastChannel === "function"
    ? new BroadcastChannel(`gigawatt-sample-${session}`)
    : null;
const role = notesMode ? "notes" : "audience";
const revealKinds = new Set([
  "copper",
  "current",
  "loss",
  "conversion-loss",
  "decision",
]);
const isRevealed = () => state.revealed.includes(STEPS[state.index].id);

function validState(value) {
  return (
    value &&
    Number.isInteger(value.index) &&
    value.index >= 0 &&
    value.index < STEPS.length &&
    Array.isArray(value.revealed) &&
    value.revealed.every((id) => STEPS.some((s) => s.id === id)) &&
    Number.isFinite(value.volts) &&
    value.volts >= 400 &&
    value.volts <= 1000 &&
    Number.isFinite(value.cycleDegrees) &&
    value.cycleDegrees >= 0 &&
    value.cycleDegrees <= 360
  );
}
function publish() {
  channel?.postMessage({ type: "state", role, state });
}
function change(patch, announce = true) {
  state = { ...state, ...patch };
  history.replaceState(null, "", `#${STEPS[state.index].id}`);
  render();
  if (announce) publish();
}
function move(delta) {
  change({
    index: Math.max(0, Math.min(STEPS.length - 1, state.index + delta)),
  });
}
function reveal() {
  const step = STEPS[state.index];
  if (!revealKinds.has(step.kind)) return;
  change({
    revealed: isRevealed()
      ? state.revealed.filter((id) => id !== step.id)
      : [...state.revealed, step.id],
  });
}
function renderSteps() {
  const buttons = STEPS.map(
    (s, i) =>
      `<button data-step="${i}" ${i === state.index ? 'aria-current="step"' : ""} aria-label="${i + 1}. ${escapeHTML(s.title)}">${i + 1}</button>`,
  ).join("");
  byId("steps").innerHTML = buttons;
  byId("notes-outline").innerHTML = STEPS.map(
    (s, i) =>
      `<button data-step="${i}" ${i === state.index ? 'aria-current="step"' : ""}>${i + 1}. ${escapeHTML(s.title)}</button>`,
  ).join("");
  document
    .querySelectorAll("[data-step]")
    .forEach((b) =>
      b.addEventListener("click", () =>
        change({ index: Number(b.dataset.step) }),
      ),
    );
}
function metric(value, unit) {
  return `<div class="metric">${value} <small>${unit}</small></div>`;
}
function intro() {
  return `<div class="hero"><div class="hero-copy"><span class="chip">480 V three-phase AC ↔ 800 V DC</span><div class="hero-number">100<small> kW</small></div><span class="hero-goal">Same power delivered to the load</span></div><img src="assets/power-equipment.png" width="1672" height="941" alt="Concept illustration of conversion equipment beside a compute rack." /></div>`;
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
  const shown = isRevealed();
  const { ac, dc } = conductorNumbers();
  const ratio = dc.conductors / ac.conductors;
  function bundle(supply, labels) {
    return `<div class="copper-bundle" data-supply="${supply}" aria-label="${labels.length} copper conductors of equal length and cross-section">${labels.map((label) => `<div class="copper-row"><span>${label}</span><i class="copper-bar" aria-hidden="true"></i></div>`).join("")}${supply === "dc" ? '<div class="copper-row copper-removed" aria-label="One fewer conductor"><span>−1</span><i aria-hidden="true"></i></div>' : ""}</div>`;
  }
  return `<div class="model copper-model"><div class="model-top"><span class="chip">SAME 100 kW DELIVERED</span><span class="ledger-formula">Copper volume = count × length × area</span></div><div class="comparison"><section class="metric-card"><p class="metric-label">480 V three-phase AC</p>${bundle("ac", ["L1", "L2", "L3"])}<p class="copper-quantity"><strong>3</strong> equal copper lengths</p></section><section class="metric-card changed"><p class="metric-label">800 V DC</p>${bundle("dc", ["+", "−"])}<p class="copper-quantity"><strong>2</strong> equal copper lengths</p></section></div>${shown ? `<div class="copper-result"><strong>${fmt((1 - ratio) * 100, 1)}% less conductor copper</strong><span>Equal length, cross-section and material. Current comes next.</span></div>` : '<div class="control-line"><button id="reveal" class="reveal">How much copper is removed?</button></div>'}</div>`;
}
function current() {
  const { ac, dc } = conductorNumbers(state.volts);
  const shown = isRevealed();
  return `<div class="model"><div class="model-top"><span class="chip">${DEFAULTS.power_kw} kW REAL POWER · AC PF = ${DEFAULTS.power_factor}</span><span class="ledger-formula">Current in each conductor</span></div><div class="comparison"><div class="metric-card"><p class="metric-label">${DEFAULTS.reference_voltage_v} V three-phase AC</p>${metric(shown ? fmt(ac.amps, 1) : "?", "A")}<p class="metric-sub">RMS · I = P / (√3 × V<sub>LL</sub> × PF)</p>${conductors(["L1", "L2", "L3"])}</div><div class="metric-card changed"><p class="metric-label"><span id="variable-voltage">${state.volts}</span> V DC</p><div id="variable-current">${metric(shown ? fmt(dc.amps, 1) : "?", "A")}</div><p class="metric-sub" id="variable-derivation">${shown ? `${fmt(DEFAULTS.power_kw * 1000)} W ÷ ${state.volts} V` : "I = P / V"}</p>${conductors(["+", "−"])}</div></div>${shown ? `<div class="control-line"><label for="voltage">Try another DC voltage</label><input id="voltage" type="range" min="400" max="1000" step="1" value="${state.volts}" /><output id="voltage-value" for="voltage">${state.volts} V</output><button id="reset-voltage">800 V</button></div>` : `<div class="control-line"><button class="reveal" id="reveal">Reveal the currents</button></div>`}</div>`;
}
function loss() {
  const shown = isRevealed(),
    { ac, dc, lossRatio } = conductorNumbers();
  return `<div class="model"><div class="model-top"><span class="chip">100 kW delivered · PF = 1</span><span class="ledger-formula">10 mΩ per conductor</span></div><div class="comparison"><section class="metric-card"><p class="metric-label">480 V three-phase AC</p>${metric(fmt(ac.lossKW * 1000), "W heat")}<p class="metric-sub">3 × 120.3² × 0.01</p><div class="loss-track"><div class="loss-bar" style="width:100%"></div></div></section><section class="metric-card changed"><p class="metric-label">800 V DC</p>${metric(shown ? fmt(dc.lossKW * 1000, 1) : "?", "W heat")}<p class="metric-sub">2 × 125² × 0.01</p><div class="loss-track">${shown ? `<div class="loss-bar" style="width:${lossRatio * 100}%"></div>` : ""}</div></section></div>${shown ? `<p class="comparison-result"><strong>${fmt((ac.lossKW - dc.lossKW) * 1000)} W less heat</strong><span>About 0.12% of the 100 kW delivered · conductors only</span></p>` : `<div class="control-line"><button class="reveal" id="reveal">Calculate DC conductor heat</button></div>`}</div>`;
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
  return `<div class="architecture"><div class="path"><section class="zone ${kind === "facility" ? "active" : ""}"><h2 class="zone-title">Upstream power room</h2><div class="zone-body">${facility}</div></section><section class="zone ${kind === "sidecar" ? "active" : ""}"><h2 class="zone-title">${kind === "sidecar" ? "Power rack in the hall" : "Hall distribution"}</h2><div class="zone-body">${adjacent}</div></section><section class="zone rack ${kind === "ac" ? "active" : ""}"><h2 class="zone-title">Compute rack</h2><div class="zone-body">${rack}</div>${space}</section></div></div>`;
}
function conversionLoss() {
  const output = DEFAULTS.power_kw,
    efficiency = DEFAULTS.converter_efficiency;
  const input = output / efficiency,
    loss = input - output,
    shown = isRevealed();
  return `<div class="converter-example"><div class="model-top"><span class="chip">Illustration · 98% efficiency at this load</span></div><div class="converter-flow"><div class="power-port"><span>Input</span><strong>${shown ? fmt(input, 2) : "?"}<small> kW</small></strong></div><span class="conversion-arrow" aria-hidden="true">→</span><div class="converter-box"><strong>Power converter</strong><span>Useful output ÷ input = 98%</span></div><span class="conversion-arrow" aria-hidden="true">→</span><div class="power-port"><span>Useful output</span><strong>100<small> kW</small></strong></div><div class="converter-heat"><span aria-hidden="true">↓</span><strong>${shown ? fmt(loss, 2) : "?"} kW <small>converter heat</small></strong></div></div><div class="loss-causes"><span>Resistance heats conductors</span><span>Switching dissipates energy</span><span>Magnetic cores heat up</span><span>Controls &amp; fans draw power</span></div>${shown ? '<div class="equation-block">100 ÷ 0.98 − 100 = <strong>2.04 kW</strong></div>' : '<div class="control-line"><button class="reveal" id="reveal">Calculate the lost power</button></div>'}</div>`;
}
function decision() {
  const shown = isRevealed(),
    base = conductorNumbers().dc;
  const grown = dcConductorModel(
    DEFAULTS.power_kw * 2,
    DEFAULTS.comparison_voltage_v,
    2 * DEFAULTS.conductor_ohms,
    DEFAULTS.hours,
  );
  function caseCard(label, power, amps, heat, changed) {
    return `<section class="metric-card ${changed ? "changed" : ""}"><p class="metric-label">${label}</p>${metric(fmt(power), "kW to load")}<div class="growth-equation">${fmt(power * 1000)} W ÷ 800 V<br>= <strong>${changed && !shown ? "?" : fmt(amps)} A</strong> per conductor</div><p class="metric-sub">Conductor heat: ${changed && !shown ? "?" : fmt(heat * 1000, 1)} W</p></section>`;
  }
  return `<div class="model capacity-model"><div class="model-top"><span class="chip">Same two conductors · 800 V at the load · 10 mΩ each</span></div><div class="comparison">${caseCard("Original load", DEFAULTS.power_kw, base.amps, base.lossKW, false)}${caseCard("Double the load", DEFAULTS.power_kw * 2, grown.amps, grown.lossKW, true)}</div>${shown ? '<p class="comparison-result"><span>Current rating, temperature and voltage drop still limit usable capacity.</span></p>' : '<div class="control-line"><button id="reveal" class="reveal">Calculate the new current</button></div>'}</div>`;
}
function renderNotes() {
  const step = STEPS[state.index];
  byId("notes-title").textContent = PRESENTATION.title;
  byId("notes-position").textContent =
    `VISUAL ${state.index + 1} OF ${STEPS.length} · ~${step.duration_seconds} SECONDS PLANNED`;
  byId("notes-headline").textContent = step.headline;
  byId("notes-cue").textContent = step.cue;
  byId("narration").innerHTML = `<ul class="speaker-points">${step.notes
    .map((point) => `<li>${escapeHTML(point)}</li>`)
    .join("")}</ul>`;
  if (["ac-basics", "three-phase"].includes(step.kind)) {
    const now = acdcWaveModel(step.kind, state.cycleDegrees);
    byId("narration").insertAdjacentHTML(
      "afterbegin",
      `<p class="cue" id="notes-cycle">Cycle: ${state.cycleDegrees}° · ${fmt(now.instantKW, 1)} kW received now · 100 kW average.</p>`,
    );
  }
  if (step.kind === "current" && isRevealed())
    byId("narration").insertAdjacentHTML(
      "afterbegin",
      `<p class="cue">Live DC comparison: ${state.volts} V · ${fmt(conductorNumbers(state.volts).dc.amps, 1)} A. AC stays at 480 V · ${fmt(conductorNumbers().ac.amps, 1)} A RMS</p>`,
    );
  byId("notes-next").textContent =
    STEPS[state.index + 1]?.headline ||
    "End of sample. Discuss the learner’s reasoning.";
  byId("notes-previous").disabled = state.index === 0;
  byId("notes-next-button").disabled = state.index === STEPS.length - 1;
  byId("notes-reveal").hidden = !revealKinds.has(step.kind);
  byId("notes-reveal").textContent = isRevealed()
    ? "Hide answer"
    : "Reveal answer";
  byId("audience-link").href =
    `teach.html?session=${encodeURIComponent(session)}#${step.id}`;
}
function bindVisual() {
  byId("cycle-angle")?.addEventListener("input", (event) => {
    state.cycleDegrees = Number(event.target.value);
    byId("wave-content").innerHTML = electricalContent(STEPS[state.index].kind);
    byId("cycle-value").textContent =
      `${state.cycleDegrees}° · ${fmt((state.cycleDegrees / 360 / 60) * 1000, 2)} ms`;
    publish();
  });
  byId("reveal")?.addEventListener("click", reveal);
  byId("voltage")?.addEventListener("input", (event) => {
    state.volts = Number(event.target.value);
    byId("variable-voltage").textContent = state.volts;
    byId("variable-current").innerHTML = metric(
      fmt(conductorNumbers(state.volts).dc.amps, 1),
      "A",
    );
    byId("voltage-value").textContent = `${state.volts} V`;
    byId("variable-derivation").textContent =
      `${fmt(DEFAULTS.power_kw * 1000)} W ÷ ${state.volts} V`;
    publish();
  });
  byId("reset-voltage")?.addEventListener("click", () =>
    change({ volts: DEFAULTS.comparison_voltage_v }),
  );
}
function render() {
  const step = STEPS[state.index];
  document.title = `${notesMode ? "Presenter notes · " : ""}${step.title} — GIGAWATT`;
  renderSteps();
  if (notesMode) {
    renderNotes();
    return;
  }
  const focus = document.activeElement?.id;
  byId("chapter").textContent =
    `800 V DC · ${state.index + 1} / ${STEPS.length}`;
  byId("scene-title").textContent = step.headline;
  byId("visual").innerHTML = (
    {
      intro,
      copper,
      current,
      loss,
      "conversion-loss": conversionLoss,
      decision,
      "dc-basics": () => electricalVisual("dc-basics"),
      "ac-basics": () => electricalVisual("ac-basics"),
      "three-phase": () => electricalVisual("three-phase"),
      "voltage-basis": () => electricalVisual("voltage-basis"),
    }[step.kind] || (() => architecture(step.kind))
  )();
  byId("previous").disabled = state.index === 0;
  byId("next").disabled = state.index === STEPS.length - 1;
  byId("next").innerHTML =
    state.index === STEPS.length - 1
      ? "<span>End of sample</span> ✓"
      : "<span>Next</span> →";
  if (studentMode)
    byId("student-explanation").innerHTML = step.explanation
      .map((p) => `<p>${escapeHTML(p)}</p>`)
      .join("");
  bindVisual();
  if (focus === "reveal") byId("scene").focus({ preventScroll: true });
}
byId("view-label").textContent = studentMode
  ? "800 V DC · EXPLORE"
  : "800 V DC · TEACH";
byId("open-notes").hidden = !teachingMode;
byId("fullscreen").hidden = !teachingMode;
byId("student-context").hidden = !studentMode;
byId("audience").hidden = notesMode;
byId("presenter").hidden = !notesMode;
byId("previous").addEventListener("click", () => move(-1));
byId("next").addEventListener("click", () => move(1));
byId("notes-previous").addEventListener("click", () => move(-1));
byId("notes-next-button").addEventListener("click", () => move(1));
byId("notes-reveal").addEventListener("click", reveal);
byId("open-notes").addEventListener("click", () => {
  const win = window.open(
    `sample-notes.html?session=${encodeURIComponent(session)}#${STEPS[state.index].id}`,
    `gigawatt-notes-${session}`,
    "popup,width=1120,height=850",
  );
  if (!win)
    byId("notice").textContent =
      "The notes window was blocked. Allow this popup, then select Presenter notes again.";
});
byId("fullscreen").addEventListener("click", async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await document.documentElement.requestFullscreen();
  } catch {
    byId("notice").textContent =
      "Fullscreen is unavailable here. Open this page in a standalone browser window.";
  }
});
document.addEventListener("fullscreenchange", () => {
  byId("fullscreen").setAttribute(
    "aria-label",
    document.fullscreenElement ? "Exit fullscreen" : "Enter fullscreen",
  );
  byId("fullscreen").innerHTML =
    `⛶ <span>${document.fullscreenElement ? "Exit fullscreen" : "Fullscreen"}</span>`;
});
document.addEventListener("keydown", (event) => {
  if (
    event.altKey ||
    event.ctrlKey ||
    event.metaKey ||
    /INPUT|TEXTAREA|SELECT/.test(event.target.tagName)
  )
    return;
  if (event.key === "ArrowRight" || event.key === "PageDown") {
    event.preventDefault();
    move(1);
  }
  if (event.key === "ArrowLeft" || event.key === "PageUp") {
    event.preventDefault();
    move(-1);
  }
  if (event.key.toLowerCase() === "r") reveal();
  if (event.key.toLowerCase() === "p" && teachingMode)
    byId("open-notes").click();
  if (event.key.toLowerCase() === "f" && teachingMode)
    byId("fullscreen").click();
});
window.addEventListener("hashchange", () => {
  const selected = STEPS.findIndex(
    (s) =>
      s.id ===
      (PRESENTATION.aliases?.[location.hash.slice(1)] ||
        location.hash.slice(1)),
  );
  if (selected >= 0) change({ index: selected });
});
if (channel) {
  channel.addEventListener("message", ({ data }) => {
    if (!data || data.role === role) return;
    if (notesMode)
      byId("connection").textContent =
        "Connected to the visual window. Navigation and reveals stay in sync.";
    if (data.type === "hello") publish();
    if (data.type === "state" && validState(data.state))
      change(data.state, false);
  });
  channel.postMessage({ type: "hello", role });
}
byId("connection").textContent = channel
  ? "Open the visual window to connect. These notes also work on their own."
  : "Live synchronization is unavailable in this browser. Advance each window separately.";
render();
