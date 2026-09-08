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
  dcConversionKW: DEFAULTS.dc_conversion_kw,
};
const session =
  new URLSearchParams(location.search).get("session") || crypto.randomUUID();
const channel =
  !studentMode && typeof BroadcastChannel === "function"
    ? new BroadcastChannel(`gigawatt-sample-${session}`)
    : null;
const role = notesMode ? "notes" : "audience";
const revealKinds = new Set(["current", "loss", "energy", "paths"]);
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
    value.volts >= 48 &&
    value.volts <= 800 &&
    Number.isFinite(value.dcConversionKW) &&
    value.dcConversionKW >= 1 &&
    value.dcConversionKW <= 7
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
  return `<div class="hero"><div class="hero-copy"><span class="chip">ONE DC DISTRIBUTION SEGMENT</span><div class="hero-number">100<small> kW</small></div><p>Power arriving<br>at the load</p></div><img src="assets/power-equipment.png" width="1672" height="941" alt="Illustrative conversion equipment beside a compute rack; not a wiring diagram or an equipment rating." /></div>`;
}
function current() {
  const dc = dcModel(DEFAULTS.power_kw, state.volts);
  const shown = isRevealed();
  return `<div class="model"><div class="model-top"><span class="chip">DELIVERED POWER · ${DEFAULTS.power_kw} kW</span><span class="formula">I = P ÷ V</span></div><div class="comparison"><div class="metric-card"><p class="metric-label">${DEFAULTS.reference_voltage_v} V DC</p>${metric(shown ? fmt(dc.referenceAmps) : "?", "A")}<p class="metric-sub">${shown ? `${fmt(DEFAULTS.power_kw * 1000)} W ÷ ${DEFAULTS.reference_voltage_v} V` : "Reference segment"}</p></div><div class="metric-card changed"><p class="metric-label"><span id="variable-voltage">${state.volts}</span> V DC</p><div id="variable-current">${metric(shown ? fmt(dc.amps, 1) : "?", "A")}</div><p class="metric-sub" id="variable-derivation">${shown ? `${fmt(DEFAULTS.power_kw * 1000)} W ÷ ${state.volts} V` : "Same delivered power"}</p></div></div>${shown ? `<div class="control-line"><label for="voltage">Try another voltage</label><input id="voltage" type="range" min="48" max="800" step="1" value="${state.volts}" /><output id="voltage-value" for="voltage">${state.volts} V</output><button id="reset-voltage">800 V</button></div>` : `<div class="control-line"><button class="reveal" id="reveal">Reveal the currents</button></div>`}</div>`;
}
function loss() {
  const shown = isRevealed(),
    ratio =
      dcModel(DEFAULTS.power_kw, DEFAULTS.comparison_voltage_v).lossRatio * 100;
  return `<div class="model"><div class="model-top"><span class="chip">CONDUCTOR LOSS · RESISTANCE HELD FIXED</span><span class="formula">P<sub>loss</sub> = I²R</span></div><div class="comparison"><div class="metric-card"><p class="metric-label">48 V reference</p>${metric("100", "%")}<p class="metric-sub">Original conductor loss</p><div class="loss-track"><div class="loss-bar" style="width:100%"></div></div></div><div class="metric-card changed"><p class="metric-label">800 V comparison</p>${metric(shown ? fmt(ratio, 2) : "?", "%")}<p class="metric-sub">Of the original conductor loss</p><div class="loss-track">${shown ? `<div class="loss-bar" style="width:${ratio}%"></div>` : ""}</div></div></div>${shown ? `<p class="bridge">This conductor ≠ the whole facility</p>` : `<div class="control-line"><button class="reveal" id="reveal">Reveal the loss comparison</button></div>`}</div>`;
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
    adjacent = unit("Broader DC path");
    rack = regulator + arrow + chip;
  }
  const observation = {
    ac: "Conversion occupies space in the compute rack.",
    sidecar: "The sidecar still needs power, cooling and service access.",
    facility: "A longer DC path means more interfaces to coordinate.",
  }[kind];
  return `<div class="architecture"><div class="path"><section class="zone ${kind === "facility" ? "active" : ""}"><h2 class="zone-title">Upstream facility</h2><div class="zone-body">${facility}</div></section><section class="zone ${kind === "sidecar" ? "active" : ""}"><h2 class="zone-title">${kind === "sidecar" ? "Nearby power rack / sidecar" : "Distribution space"}</h2><div class="zone-body">${adjacent}</div></section><section class="zone rack ${kind === "ac" ? "active" : ""}"><h2 class="zone-title">Compute rack</h2><div class="zone-body">${rack}</div></section></div><p class="path-label">${kind === "ac" ? "AC toward the rack" : kind === "sidecar" ? "AC to the sidecar → 800 V DC toward the rack" : "AC conversion upstream → DC across the facility"}</p><p class="boundary-line">${observation}</p></div>`;
}
function ledgerCard(title, rows, inputKW, shown, changed = false) {
  return `<section class="ledger-card ${changed ? "changed" : ""}"><h2>${title}</h2><dl>${rows.map(([label, value]) => `<div><dt>${label}</dt><dd>${value} <small>kW</small></dd></div>`).join("")}</dl><div class="ledger-total"><span>Required input</span><strong>${shown ? fmt(inputKW, 3) : "?"} <small>kW</small></strong></div></section>`;
}
function energy() {
  const low = dcConductorModel(
    DEFAULTS.power_kw,
    48,
    DEFAULTS.loop_ohms,
    DEFAULTS.hours,
  );
  const high = dcConductorModel(
    DEFAULTS.power_kw,
    800,
    DEFAULTS.loop_ohms,
    DEFAULTS.hours,
  );
  const shown = isRevealed();
  return `<div class="energy-ledger"><div class="model-top"><span class="chip">DC SEGMENT · 100 kW DELIVERED</span><span class="ledger-formula">Input = delivered power + heat</span></div><div class="comparison">${ledgerCard(
    "48 V DC at the load",
    [
      ["Delivered power", "100"],
      ["Conductor heat", fmt(low.lossKW, 3)],
    ],
    low.inputKW,
    shown,
  )}${ledgerCard(
    "800 V DC at the load",
    [
      ["Delivered power", "100"],
      ["Conductor heat", fmt(high.lossKW, 3)],
    ],
    high.inputKW,
    shown,
    true,
  )}</div><div class="ledger-result">${shown ? `<strong>${fmt(low.inputKWh - high.inputKWh, 3)} kWh less input over 1 h</strong><span>Same useful output. Less energy dissipated as heat.</span>` : `<button id="reveal">Reveal the required input</button>`}</div></div>`;
}
function pathNumbers() {
  return {
    ac: deliveryPathModel(
      DEFAULTS.power_kw,
      DEFAULTS.ac_conversion_kw,
      DEFAULTS.ac_conductor_kw,
      DEFAULTS.hours,
    ),
    dc: deliveryPathModel(
      DEFAULTS.power_kw,
      state.dcConversionKW,
      DEFAULTS.dc_conductor_kw,
      DEFAULTS.hours,
    ),
  };
}
function pathResult(ac, dc) {
  const difference = ac.inputKWh - dc.inputKWh;
  return Math.abs(difference) < 1e-9
    ? "Same input energy over 1 h"
    : `DC uses ${fmt(Math.abs(difference), 1)} kWh ${difference > 0 ? "less" : "more"} input over 1 h`;
}
function paths() {
  const { ac, dc } = pathNumbers(),
    shown = isRevealed();
  return `<div class="energy-ledger"><div class="model-top"><span class="chip">HYPOTHETICAL LOSSES · 100 kW FINAL DC LOAD</span><span class="ledger-formula">Input = load + all path losses</span></div><div class="comparison">${ledgerCard(
    "AC-distributed path",
    [
      ["Final DC load", "100"],
      ["Conductors", fmt(DEFAULTS.ac_conductor_kw)],
      ["All conversion", fmt(DEFAULTS.ac_conversion_kw)],
    ],
    ac.inputKW,
    shown,
  )}<div id="dc-path-card">${ledgerCard(
    "DC-distributed path",
    [
      ["Final DC load", "100"],
      ["Conductors", fmt(DEFAULTS.dc_conductor_kw, 1)],
      ["All conversion", fmt(state.dcConversionKW, 1)],
    ],
    dc.inputKW,
    shown,
    true,
  )}</div></div>${shown ? `<div class="control-line"><label for="dc-conversion">DC conversion loss</label><input id="dc-conversion" type="range" min="1" max="7" step="0.1" value="${state.dcConversionKW}" /><output id="dc-conversion-value" for="dc-conversion">${fmt(state.dcConversionKW, 1)} kW</output><button id="dc-loss-reset">Reset</button></div><div class="ledger-result"><strong id="path-result">${pathResult(ac, dc)}</strong></div>` : `<div class="ledger-result"><button id="reveal">Reveal both input budgets</button></div>`}</div>`;
}
function renderNotes() {
  const step = STEPS[state.index];
  byId("notes-title").textContent = PRESENTATION.title;
  byId("notes-position").textContent =
    `VISUAL ${state.index + 1} OF ${STEPS.length} · ~${step.duration_seconds} SECONDS PLANNED`;
  byId("notes-headline").textContent = step.headline;
  byId("notes-cue").textContent = step.cue;
  byId("narration").innerHTML = step.notes
    .map((p) => `<p>${escapeHTML(p)}</p>`)
    .join("");
  if (step.kind === "current" && isRevealed())
    byId("narration").insertAdjacentHTML(
      "afterbegin",
      `<p class="cue">Live comparison: ${state.volts} V · ${fmt(dcModel(DEFAULTS.power_kw, state.volts).amps, 1)} A</p>`,
    );
  if (step.kind === "paths" && isRevealed()) {
    const { ac, dc } = pathNumbers();
    byId("narration").insertAdjacentHTML(
      "afterbegin",
      `<p class="cue">Live DC conversion loss: ${fmt(state.dcConversionKW, 1)} kW. ${pathResult(ac, dc)}.</p>`,
    );
  }
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
  byId("dc-conversion")?.addEventListener("input", (event) => {
    state.dcConversionKW = Number(event.target.value);
    const { ac, dc } = pathNumbers();
    byId("dc-path-card").innerHTML = ledgerCard(
      "DC-distributed path",
      [
        ["Final DC load", "100"],
        ["Conductors", fmt(DEFAULTS.dc_conductor_kw, 1)],
        ["All conversion", fmt(state.dcConversionKW, 1)],
      ],
      dc.inputKW,
      true,
      true,
    );
    byId("dc-conversion-value").textContent =
      `${fmt(state.dcConversionKW, 1)} kW`;
    byId("path-result").textContent = pathResult(ac, dc);
    publish();
  });
  byId("dc-loss-reset")?.addEventListener("click", () =>
    change({ dcConversionKW: DEFAULTS.dc_conversion_kw }),
  );
  byId("reveal")?.addEventListener("click", reveal);
  byId("voltage")?.addEventListener("input", (event) => {
    state.volts = Number(event.target.value);
    byId("variable-voltage").textContent = state.volts;
    byId("variable-current").innerHTML = metric(
      fmt(dcModel(DEFAULTS.power_kw, state.volts).amps, 1),
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
    `800 V DC / ${String(state.index + 1).padStart(2, "0")} · ${step.title}`;
  byId("scene-title").textContent = step.headline;
  byId("caption").textContent = step.caption;
  byId("visual").innerHTML = (
    { intro, current, loss, energy, paths }[step.kind] ||
    (() => architecture(step.kind))
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
