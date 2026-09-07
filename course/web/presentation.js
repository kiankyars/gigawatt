const PRESENTATION = JSON.parse(
  document.getElementById("presentation-data").textContent,
);
const STEPS = PRESENTATION.steps;
const DEFAULTS = PRESENTATION.defaults;
const notesMode = location.pathname.endsWith("sample-notes.html");
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
  STEPS.findIndex((step) => `#${step.id}` === location.hash),
);
let state = { index, revealed: [], volts: DEFAULTS.comparison_voltage_v };
const session =
  new URLSearchParams(location.search).get("session") || crypto.randomUUID();
const channel =
  typeof BroadcastChannel === "function"
    ? new BroadcastChannel(`gigawatt-sample-${session}`)
    : null;
const role = notesMode ? "notes" : "audience";
const revealKinds = new Set(["current", "loss", "transfer"]);
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
    value.volts <= 800
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
function transfer() {
  const shown = isRevealed(),
    amps = dcModel(
      DEFAULTS.transfer_power_kw,
      DEFAULTS.transfer_voltage_v,
    ).amps;
  return `<div class="transfer"><div class="transfer-path"><div class="metric-card"><p class="metric-label">Upstream feeder limit</p>${metric(DEFAULTS.transfer_feeder_kw, "kW")}</div><div class="transfer-arrow" aria-hidden="true">→</div><div class="metric-card changed"><p class="metric-label">Downstream DC load</p>${metric(DEFAULTS.transfer_power_kw, "kW")}<p class="metric-sub">at ${DEFAULTS.transfer_voltage_v} V · ${shown ? `${fmt(amps)} A` : "What current?"}</p></div></div><div class="answer-strip">${shown ? `<b>${fmt(amps)} A · No</b><p>${DEFAULTS.transfer_feeder_kw} kW cannot supply ${DEFAULTS.transfer_power_kw} kW, even before losses.</p>` : `<button id="reveal">Reveal current + feeder answer</button>`}</div></div>`;
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
    `sample.html?session=${encodeURIComponent(session)}#${step.id}`;
}
function bindVisual() {
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
    { intro, current, loss, transfer }[step.kind] ||
    (() => architecture(step.kind))
  )();
  byId("previous").disabled = state.index === 0;
  byId("next").disabled = state.index === STEPS.length - 1;
  byId("next").innerHTML =
    state.index === STEPS.length - 1 ? "End of sample" : "<span>Next</span> →";
  bindVisual();
  if (focus === "reveal") byId("scene").focus({ preventScroll: true });
}
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
  byId("workflow").hidden = Boolean(document.fullscreenElement);
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
  if (event.key.toLowerCase() === "p" && !notesMode) byId("open-notes").click();
  if (event.key.toLowerCase() === "f" && !notesMode) byId("fullscreen").click();
});
window.addEventListener("hashchange", () => {
  const selected = STEPS.findIndex((s) => `#${s.id}` === location.hash);
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
