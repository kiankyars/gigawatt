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
  voltageView: "meter",
  converterView: "supply",
};
const session =
  new URLSearchParams(location.search).get("session") || crypto.randomUUID();
const channel =
  !studentMode && typeof BroadcastChannel === "function"
    ? new BroadcastChannel(`gigawatt-sample-${session}`)
    : null;
const role = notesMode ? "notes" : "audience";
const revealKinds = new Set(["current", "loss", "conversion-loss"]);
const isRevealed = () => state.revealed.includes(STEPS[state.index].id);
const { intro, copper, current, loss, architecture, conversionViews, sourceFigure, conductorNumbers } = createPresentationRenderers({ defaults: DEFAULTS, getState: () => state, getStep: () => STEPS[state.index], isRevealed, acdcConductorModel, escapeHTML, fmt });

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
    value.cycleDegrees <= 360 &&
    ["meter", "pairs"].includes(value.voltageView) &&
    ["supply", "heat"].includes(value.converterView)
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
    ...(step.kind === "conversion-loss" ? { converterView: "heat" } : {}),
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
    "End of sample. Return to the copper and equipment-placement question.";
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
  document.querySelectorAll("[data-converter-view]").forEach((button) =>
    button.addEventListener("click", () => {
      change({ converterView: button.dataset.converterView });
      document
        .querySelector(`[data-converter-view="${state.converterView}"]`)
        .focus({ preventScroll: true });
    }),
  );
  document.querySelectorAll("[data-voltage-view]").forEach((button) => {
    button.addEventListener("click", () => {
      change({ voltageView: button.dataset.voltageView });
      document
        .querySelector(`[data-voltage-view="${state.voltageView}"]`)
        .focus({ preventScroll: true });
    });
  });
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
  document.title = `${notesMode ? "Presenter notes · " : ""}${presentationLabels['rack-800v']} · ${step.title} · From Watts to Tokens`;
  renderSteps();
  if (notesMode) {
    renderNotes();
    return;
  }
  const focus = document.activeElement?.id;
  byId("chapter").textContent =
    `${presentationLabels['rack-800v']} · ${state.index + 1} / ${STEPS.length}`;
  byId("scene-title").textContent =
    step.kind === "conversion-loss" && state.converterView === "heat"
      ? step.heat_headline
      : step.headline;
  byId("visual").innerHTML = (
    {
      intro,
      copper,
      current,
      loss,
      "conversion-loss": conversionViews,
      "source-figure": sourceFigure,
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
