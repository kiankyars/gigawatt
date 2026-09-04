import { renderDiagram } from "./diagrams.js";
import {
  currentThreePhase,
  energyMWh,
  resistiveLossRatio,
  rideThroughMinutes,
  rackCurrent,
  coolantFlow,
  capacityBudget,
} from "./math.js";

const course = JSON.parse(document.getElementById("course-data").textContent);
const lessons = course.lessons;
const byId = new Map(lessons.map((lesson, index) => [lesson.id, index]));
const el = (id) => document.getElementById(id);
const escapeHtml = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const lessonState = new Map();
const checkAnswers = new Map();
let lessonIndex = 0;
let explanationOpen = false;
const defaults = {
  power: 1,
  hours: 1,
  voltage: 138,
  gate: 0,
  equipment: 0,
  outage: false,
  battery: 0.25,
  pathFailed: false,
  fault: false,
  coreV: 1,
  utilization: 60,
  deltaT: 10,
  chiller: 20,
  pue: 1.25,
  cooling: 60,
  network: 900,
  budgetPue: 1.25,
  caseView: 0,
};
const formatValue = (value, digits = 0) =>
  Number(value).toLocaleString("en-US", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });

function currentState() {
  const id = lessons[lessonIndex].id;
  if (!lessonState.has(id)) lessonState.set(id, { ...defaults });
  return lessonState.get(id);
}
function setLesson(index, focus = false) {
  document.querySelectorAll("dialog[open]").forEach((dialog) => dialog.close());
  lessonIndex = Math.max(0, Math.min(lessons.length - 1, index));
  const l = lessons[lessonIndex];
  if (location.hash !== `#${l.id}`) history.pushState(null, "", `#${l.id}`);
  document.title = `${l.title} — GIGAWATT`;
  el("eyebrow").textContent = l.eyebrow;
  el("lesson-title").textContent = l.title;
  el("lesson-body").textContent = l.body;
  el("takeaway").textContent = l.takeaway;
  el("notes").innerHTML =
    `<h2>A closer look</h2>${l.notes.map((p) => `<p>${escapeHtml(p)}</p>`).join("")}`;
  el("notes").hidden = !explanationOpen;
  el("notes-button").setAttribute("aria-expanded", String(explanationOpen));
  el("notes-button").innerHTML =
    `${explanationOpen ? "Close the explanation" : "Read the explanation"} <span aria-hidden="true">${explanationOpen ? "−" : "↗"}</span>`;
  el("chapters")
    .querySelectorAll("button")
    .forEach((button, i) => {
      const active = course.chapters[i].id === l.chapter;
      button.classList.toggle("active", active);
      button.classList.toggle(
        "visited",
        course.chapters.findIndex((c) => c.id === l.chapter) > i,
      );
      if (active) button.setAttribute("aria-current", "step");
      else button.removeAttribute("aria-current");
    });
  const chapterRail = el("chapters");
  const activeChapter = chapterRail.querySelector(".active");
  if (activeChapter && innerWidth <= 760)
    chapterRail.scrollLeft =
      activeChapter.offsetLeft -
      chapterRail.clientWidth / 2 +
      activeChapter.offsetWidth / 2;
  el("progress")
    .querySelectorAll("button")
    .forEach((button, i) => {
      button.classList.toggle("active", i === lessonIndex);
      button.classList.toggle("past", i < lessonIndex);
      if (i === lessonIndex) button.setAttribute("aria-current", "step");
      else button.removeAttribute("aria-current");
    });
  el("lesson-counter").textContent =
    `${String(lessonIndex + 1).padStart(2, "0")} / ${lessons.length}`;
  el("prev").disabled = lessonIndex === 0;
  el("next-label").textContent =
    lessonIndex === lessons.length - 1 ? "Back to start" : "Next lesson";
  el("next").setAttribute(
    "aria-label",
    lessonIndex === lessons.length - 1 ? "Back to first lesson" : "Next lesson",
  );
  renderControls(l.visual);
  updateVisual();
  renderCheck(l);
  if (focus) {
    el("lesson-title").focus({ preventScroll: true });
    window.scrollTo({ top: 0, behavior: "instant" });
  }
}
function fromHash() {
  let hash;
  try {
    hash = decodeURIComponent(location.hash.slice(1));
  } catch {
    hash = "";
  }
  setLesson(byId.get(hash) ?? 0);
}
function updateVisual() {
  const l = lessons[lessonIndex],
    state = currentState(),
    d = renderDiagram(l.visual, { ...state, compact: innerWidth <= 760 });
  el("visual").innerHTML = d.svg;
  el("visual-label").textContent = d.label;
  el("visual-tag").textContent = d.tag ?? "CONCEPTUAL MODEL";
  el("visual-caption").textContent = d.caption;
  const summary = labResult(l.visual, state);
  const output = el("experiment-result");
  if (output) {
    output.textContent = summary;
    output.hidden = !summary;
  }
}
function labResult(id, s) {
  switch (id) {
    case "capacity":
      return [
        "Announced: intended capacity, not operation.",
        "Connected: an electrical connection is established.",
        "Energized: equipment is electrically live.",
        "Commissioned: the required integrated tests are passed.",
        "Loaded: IT equipment is drawing power under workload.",
      ][s.gate];
    case "train":
      return [
        "Transformer: changes voltage.",
        "Switchgear: isolates and protects.",
        "UPS: conditions power and bridges interruptions.",
        "Busway: distributes power toward racks.",
        "Rack: converts AC to DC for its equipment.",
      ][s.equipment];
    case "compute":
      return `${s.utilization}% illustrative scheduled busy time. This is not measured efficiency or a token rate.`;
    case "case":
      return s.caseView === 0
        ? "Use dated evidence to establish each site milestone."
        : "An announced capacity does not establish measured IT load, utilization, or installed GPU count.";
    case "energy":
      return `${formatValue(s.power, 1)} MW × ${s.hours} h = ${formatValue(energyMWh(s.power, s.hours), 1)} MWh.`;
    case "voltage":
      return `${formatValue(currentThreePhase(100, s.voltage))} A per phase · ${formatValue(resistiveLossRatio(s.voltage, 13.8) * 100, 2)}% of the 13.8 kV conductor loss.`;
    case "ride-through":
      return `${s.outage ? "Utility off. UPS carries the load." : "Utility available."} Stored energy supports ${formatValue(rideThroughMinutes(s.battery, 5), 1)} ideal minutes at 5 MW.`;
    case "redundancy":
      return s.pathFailed
        ? "Path A unavailable. Path B supplies the complete load."
        : "Both independent full-capacity paths are available.";
    case "failure":
      return s.fault
        ? "Middle feeder isolated. The two other feeders remain powered."
        : "All three feeders are powered.";
    case "current":
      return `${formatValue(rackCurrent(1, s.coreV))} A at ${s.coreV} V for the same ideal 1 kW load.`;
    case "liquid":
      return `${formatValue(coolantFlow(100, s.deltaT), 2)} kg/s, approximately ${formatValue(coolantFlow(100, s.deltaT) * 60)} L/min of water.`;
    case "rejection":
      return `100 kW absorbed + ${s.chiller} kW work = ${100 + s.chiller} kW rejected.`;
    case "pue":
      return `${formatValue(100 / s.pue, 1)} MW IT + ${formatValue(100 - 100 / s.pue, 1)} MW overhead = 100 MW facility.`;
    case "bottleneck": {
      const b = capacityBudget(
        100,
        s.budgetPue,
        s.cooling,
        100,
        900,
        s.network,
        70,
      );
      return `${b.supportedRacks} rack equivalents · ${b.supportedITMW} MW IT · ${formatValue(b.facilityDrawMW, 1)} MW facility draw. Binding limit: ${b.binding.join(" + ")}.`;
    }
    default:
      return "";
  }
}
function range(key, label, min, max, step, unit, digits = 0) {
  const s = currentState();
  return `<div class="control"><label for="control-${key}">${label}<output id="value-${key}" for="control-${key}">${formatValue(s[key], digits)} ${unit}</output></label><input type="range" id="control-${key}" data-key="${key}" data-digits="${digits}" data-unit="${unit}" min="${min}" max="${max}" step="${step}" value="${s[key]}"></div>`;
}
function choices(key, values) {
  const s = currentState();
  return `<div class="segmented">${values.map(([value, label]) => `<button class="toggle" data-key="${key}" data-value="${value}" aria-pressed="${String(s[key] === value)}">${label}</button>`).join("")}</div>`;
}
function renderControls(id) {
  let html = "";
  switch (id) {
    case "energy":
      html =
        range("power", "Constant power", 0.5, 5, 0.5, "MW", 1) +
        range("hours", "Running time", 1, 24, 1, "h");
      break;
    case "voltage":
      html = range("voltage", "Line-to-line voltage", 13.8, 138, 13.8, "kV", 1);
      break;
    case "capacity":
      html = choices("gate", [
        [0, "Announced"],
        [1, "Connected"],
        [2, "Energized"],
        [3, "Commissioned"],
        [4, "Loaded"],
      ]);
      break;
    case "train":
      html = choices("equipment", [
        [0, "Transformer"],
        [1, "Switchgear"],
        [2, "UPS"],
        [3, "Busway"],
        [4, "Rack"],
      ]);
      break;
    case "ride-through":
      html =
        choices("outage", [
          [false, "Utility on"],
          [true, "Interrupt utility"],
        ]) +
        range("battery", "Usable output energy", 0.05, 0.5, 0.05, "MWh", 2);
      break;
    case "redundancy":
      html = choices("pathFailed", [
        [false, "Both paths available"],
        [true, "Disable path A"],
      ]);
      break;
    case "failure":
      html = choices("fault", [
        [false, "Normal operation"],
        [true, "Fault the middle feeder"],
      ]);
      break;
    case "current":
      html = choices("coreV", [
        [50, "50 V bus"],
        [12, "12 V rail"],
        [1, "1 V near the processor"],
      ]);
      break;
    case "compute":
      html = range(
        "utilization",
        "Illustrative scheduled busy time",
        10,
        100,
        10,
        "%",
      );
      break;
    case "liquid":
      html = range("deltaT", "Coolant temperature rise", 5, 20, 1, "°C");
      break;
    case "rejection":
      html = range("chiller", "Illustrative compressor work", 5, 50, 5, "kW");
      break;
    case "pue":
      html = range(
        "pue",
        "Assumed facility-to-IT ratio",
        1.1,
        1.6,
        0.05,
        "",
        2,
      );
      break;
    case "bottleneck":
      html =
        range("cooling", "Available IT cooling duty", 20, 100, 5, "MW") +
        range("network", "Network-supported racks", 300, 1000, 50, "racks") +
        range(
          "budgetPue",
          "Assumed facility-to-IT ratio",
          1.1,
          1.6,
          0.05,
          "",
          2,
        );
      break;
    case "case":
      html = choices("caseView", [
        [0, "What does this establish?"],
        [1, "What is still unknown?"],
      ]);
      break;
  }
  el("experiment").innerHTML = html
    ? `${html}<output id="experiment-result" class="experiment-result" aria-live="polite" aria-atomic="true"></output><button class="reset" id="reset-experiment">Reset experiment ↺</button>`
    : "";
  el("experiment")
    .querySelectorAll("input")
    .forEach((input) =>
      input.addEventListener("input", () => {
        const key = input.dataset.key;
        currentState()[key] = Number(input.value);
        el(`value-${key}`).textContent =
          `${formatValue(input.value, Number(input.dataset.digits))} ${input.dataset.unit}`;
        updateVisual();
      }),
    );
  el("experiment")
    .querySelectorAll(".toggle")
    .forEach((button) =>
      button.addEventListener("click", () => {
        const raw = button.dataset.value;
        currentState()[button.dataset.key] =
          raw === "true" ? true : raw === "false" ? false : Number(raw);
        el("experiment")
          .querySelectorAll(".toggle")
          .forEach((b) => b.setAttribute("aria-pressed", String(b === button)));
        updateVisual();
      }),
    );
  if (el("reset-experiment"))
    el("reset-experiment").addEventListener("click", () => {
      lessonState.set(lessons[lessonIndex].id, { ...defaults });
      renderControls(id);
      updateVisual();
      el("experiment")
        .querySelector("input, .toggle")
        ?.focus({ preventScroll: true });
    });
}
function renderCheck(l) {
  const box = el("knowledge-check");
  box.hidden = !l.check;
  if (!l.check) {
    box.innerHTML = "";
    return;
  }
  const c = l.check;
  box.innerHTML = `<div class="check-question"><p class="eyebrow">TEST YOUR MENTAL MODEL</p><h2>${escapeHtml(c.question)}</h2></div><div class="check-options">${c.options.map((option, i) => `<button class="answer-button" data-answer="${i}" aria-pressed="false"><span aria-hidden="true">${String.fromCharCode(65 + i)}</span>${escapeHtml(option)}</button>`).join("")}<p id="answer-feedback" class="answer-feedback" aria-live="polite"></p></div>`;
  function answer(i) {
    checkAnswers.set(l.id, i);
    box.querySelectorAll(".answer-button").forEach((b, j) => {
      b.setAttribute("aria-pressed", String(j === i));
      b.classList.toggle("correct", i === c.answer && j === i);
    });
    el("answer-feedback").textContent =
      (i === c.answer ? "Exactly. " : "Try the mechanism again. ") +
      c.explanation;
  }
  box
    .querySelectorAll(".answer-button")
    .forEach((button) =>
      button.addEventListener("click", () =>
        answer(Number(button.dataset.answer)),
      ),
    );
  if (checkAnswers.has(l.id)) answer(checkAnswers.get(l.id));
}
function openSources() {
  const l = lessons[lessonIndex];
  el("source-list").innerHTML =
    `<p class="source-note">${escapeHtml(l.title)}<br>Numerical experiments are simplified teaching scenarios. Primary references support the mechanisms; they do not turn illustrative inputs into site measurements.</p>${l.sources.map((s) => `<a class="source-item" href="${escapeHtml(s.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(s.title)} ↗<small>${escapeHtml(new URL(s.url).hostname)}</small></a>`).join("")}`;
  el("sources-dialog").showModal();
}

el("chapters").innerHTML = course.chapters
  .map(
    (c, i) =>
      `<button class="chapter" data-chapter="${escapeHtml(c.id)}"><span class="chapter-number">${String(i + 1).padStart(2, "0")}</span><span>${escapeHtml(c.title)}</span></button>`,
  )
  .join("");
el("chapters")
  .querySelectorAll("button")
  .forEach((button) =>
    button.addEventListener("click", () =>
      setLesson(
        lessons.findIndex((l) => l.chapter === button.dataset.chapter),
        true,
      ),
    ),
  );
el("progress").innerHTML = lessons
  .map(
    (l, i) =>
      `<button aria-label="Lesson ${i + 1}: ${escapeHtml(l.title)}" title="${escapeHtml(l.title)}"></button>`,
  )
  .join("");
el("progress")
  .querySelectorAll("button")
  .forEach((button, i) =>
    button.addEventListener("click", () => setLesson(i, true)),
  );
el("contents-list").innerHTML = course.chapters
  .map(
    (c) =>
      `<section class="contents-chapter"><h3>${escapeHtml(c.kicker)} / ${escapeHtml(c.title)}</h3>${lessons.map((l, i) => (l.chapter === c.id ? `<button data-index="${i}"><span>${String(i + 1).padStart(2, "0")}</span>${escapeHtml(l.title)}</button>` : "")).join("")}</section>`,
  )
  .join("");
el("contents-list")
  .querySelectorAll("button")
  .forEach((b) =>
    b.addEventListener("click", () => {
      el("contents-dialog").close();
      setLesson(Number(b.dataset.index), true);
    }),
  );
el("contents-button").addEventListener("click", () =>
  el("contents-dialog").showModal(),
);
document
  .querySelectorAll(".dialog-close")
  .forEach((b) =>
    b.addEventListener("click", () => b.closest("dialog").close()),
  );
document.querySelectorAll("dialog").forEach((dialog) =>
  dialog.addEventListener("click", (event) => {
    if (event.target === dialog) {
      const bounds = dialog.getBoundingClientRect();
      if (
        event.clientX < bounds.left ||
        event.clientX > bounds.right ||
        event.clientY < bounds.top ||
        event.clientY > bounds.bottom
      )
        dialog.close();
    }
  }),
);
el("sources-button").addEventListener("click", openSources);
el("notes-button").addEventListener("click", () => {
  explanationOpen = !explanationOpen;
  el("notes").hidden = !explanationOpen;
  el("notes-button").setAttribute("aria-expanded", String(explanationOpen));
  el("notes-button").innerHTML =
    `${explanationOpen ? "Close the explanation" : "Read the explanation"} <span aria-hidden="true">${explanationOpen ? "−" : "↗"}</span>`;
});
el("prev").addEventListener("click", () => setLesson(lessonIndex - 1, true));
el("next").addEventListener("click", () =>
  setLesson(lessonIndex === lessons.length - 1 ? 0 : lessonIndex + 1, true),
);
el("fullscreen").hidden = !document.fullscreenEnabled;
el("fullscreen").addEventListener("click", async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await document.documentElement.requestFullscreen();
  } catch {
    el("fullscreen").hidden = true;
  }
});
document.addEventListener("fullscreenchange", () =>
  el("fullscreen").setAttribute(
    "aria-label",
    document.fullscreenElement ? "Exit fullscreen" : "Enter fullscreen",
  ),
);
document.addEventListener("keydown", (event) => {
  if (
    event.altKey ||
    event.ctrlKey ||
    event.metaKey ||
    event.shiftKey ||
    document.querySelector("dialog[open]")
  )
    return;
  if (event.target.closest("input,select,textarea,[contenteditable=true]"))
    return;
  if (event.key === "ArrowRight" && lessonIndex < lessons.length - 1) {
    event.preventDefault();
    setLesson(lessonIndex + 1, true);
  }
  if (event.key === "ArrowLeft" && lessonIndex > 0) {
    event.preventDefault();
    setLesson(lessonIndex - 1, true);
  }
});
document.querySelector(".skip").addEventListener("click", (event) => {
  event.preventDefault();
  el("lesson-title").focus();
});
window
  .matchMedia("(max-width: 760px)")
  .addEventListener("change", updateVisual);
window.addEventListener("popstate", fromHash);
window.addEventListener("hashchange", fromHash);
fromHash();
