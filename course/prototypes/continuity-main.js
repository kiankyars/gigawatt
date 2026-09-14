import {
  continuityScenes as scenes,
  resolveContinuityScene,
} from "./continuity-scenes.js";
import { renderContinuityVisual, esc } from "./continuity-visuals.js";
import { renderOnlineUPS } from "./continuity-online.js";
import { renderCapacitorEnergyDiagram, renderHoldUpDiagram, renderBatteryRampDiagram, renderRecoveryComparison } from "./continuity-energy.js";
import { renderGeneratorDiagram } from "./ups-generator.js";
import { renderBypassDiagram } from "./ups-bypass.js";
import { redundancyModel, renderRedundancy } from "./ups-redundancy.js";
import { renderReliability } from "./ups-reliability.js";

const $ = (id) => document.getElementById(id);
let index = resolveContinuityScene(location.hash.slice(1));
const fresh = () => ({
  outage: true,
  supplyAvailable: true,
  recoverySource: "battery",
  generatorStage: "waiting",
  maintenance: ["capacity-n2", "two-n-plus-one"].includes(scenes[index].id),
  fault: scenes[index].id === "capacity-n2",
  busFault: scenes[index].id === "shared-bus",
  loadKW: 100,
  isolation: "branch",
  arcStage: "arc",
  serviceStage: "bridge",
  protectedControls: false,
  serviceReveal: false,
});
let state = fresh();
const button = (key, label, value = undefined) =>
  `<button data-key="${key}" ${value === undefined ? "" : `data-value="${value}"`} aria-pressed="${value === undefined ? Boolean(state[key]) : String(state[key]) === String(value)}">${label}</button>`;
const choices = (key, options) =>
  options.map(([value, label]) => button(key, label, value)).join("");
function controls(scene) {
  if (scene.id === "outage")
    return button(
      "outage",
      state.outage ? "Restore utility" : "Remove utility",
    );
  if (scene.id === "dc-link-recovery")
    return choices("recoverySource", [
      ["battery", "Battery converter"],
      ["rectifier", "Generator + rectifier"],
    ]);
  if (scene.id === "generator")
    return choices("generatorStage", [
      ["utility", "Utility supplying"],
      ["waiting", "Generator starting"],
      ["generator", "Generator accepted"],
      ["recharge", "Generator + recharge"],
    ]);
  if (scene.mode)
    return button(
      "supplyAvailable",
      state.supplyAvailable ? "Lose bypass source" : "Restore bypass source",
    );
  if (scene.id === "shared-bus")
    return button(
      "busFault",
      state.busFault ? "Restore shared bus" : "Fail shared bus",
    );
  if (scene.id === "load-growth")
    return button(
      "loadKW",
      state.loadKW === 100 ? "Raise demand to 150 kW" : "Return to 100 kW",
      state.loadKW === 100 ? 150 : 100,
    );
  if (scene.redundancy)
    return (
      (scene.id === "capacity-n"
        ? ""
        : button(
            "maintenance",
            state.maintenance
              ? "Return maintained equipment"
              : scene.redundancy.startsWith("two_")
                ? "Isolate path A"
                : "Maintain one module",
          )) +
      button(
        "fault",
        state.fault
          ? "Restore failed module"
          : scene.redundancy.startsWith("two_")
            ? "Fail a B module"
            : "Fail one module",
      )
    );
  if (scene.id === "fault-isolation")
    return choices("isolation", [
      ["branch", "Branch fault · selective isolation"],
      ["upstream", "Branch fault · upstream trips"],
      ["bus", "Bus fault · before clearing"],
      ["bus-cleared", "Bus fault · cleared"],
    ]);
  if (scene.id === "ac-dc-interruption") return choices("arcStage", [["closed", "Contacts closed"], ["arc", "Contacts separating"], ["cleared", "Current interrupted"]]);
  if (scene.id === "service-check")
    return (
      (state.serviceReveal
        ? choices("serviceStage", [
            ["bridge", "Battery bridge"],
            ["generator", "Generator accepted"],
            ["recovery", "Cooling restarting"],
          ]) +
          button(
            "protectedControls",
            state.protectedControls
              ? "Return controls to utility"
              : "Add UPS feed to controls",
          )
        : "") +
      button(
        "serviceReveal",
        state.serviceReveal ? "Discuss" : "Show answer",
      )
    );
  return "";
}
function ups(scene, compact) {
  let result,
    context = "";
  if (["normal", "outage"].includes(scene.id)) {
    result = renderOnlineUPS(scene.id === "outage" && state.outage, compact);
    context =
      scene.id === "outage"
        ? "The inverter continues supplying the 100 kW load."
        : "100 kW protected AC load";
  } else if (scene.id === "capacitor-energy") {
    result = renderCapacitorEnergyDiagram({ compact });
  } else if (scene.id === "capacitors") {
    result = renderHoldUpDiagram({ compact });
  } else if (scene.id === "battery-ramp") {
    result = renderBatteryRampDiagram({ compact });
  } else if (scene.id === "dc-link-recovery") {
    result = renderRecoveryComparison(state.recoverySource, { compact });
  } else if (scene.id === "generator") {
    result = renderGeneratorDiagram({ stage: state.generatorStage, compact });
    context =
      state.generatorStage === "recharge"
        ? "Source capacity covers <strong>100 kW load + UPS losses + charging</strong>."
        : "100 kW protected block · source switchgear feeds the UPS input";
  } else if (scene.mode) {
    result = renderBypassDiagram({
      mode: scene.mode,
      sourceAvailable: state.supplyAvailable,
      compact,
    });
    context = state.supplyAvailable
      ? scene.mode === "static"
        ? "Forced bypass: the inverter is unavailable."
        : "External bypass supplies the load while UPS input, output and battery paths are isolated."
      : "Bypass source lost → no surviving route to this load";
  } else if (scene.redundancy) {
    const model = redundancyModel({ kind: scene.redundancy, ...state });
    return `<div class="ups-visual"><div id="redundancy-view">${renderRedundancy(model, { compact })}</div><p class="ups-context"><strong>${model.label} · ${state.loadKW} kW load demand</strong> · 50 kW usable output per module</p></div>`;
  }
  return `<div class="ups-visual"><svg id="circuit" viewBox="${result.viewBox}" role="img">${result.svg}</svg>${context ? `<p class="ups-context">${context}</p>` : ""}</div>`;
}
function render() {
  const scene = scenes[index],
    compact = matchMedia("(max-width:799px)").matches;
  document.title = `7. Continuity, storage and protection · ${scene.label} · From Watts to Tokens`;
  $("title").textContent = scene.title;
  $("lesson-reference").href = `../index.html#${scene.reading}`;
  $("stage").dataset.scene = scene.id;
  $("stage").innerHTML = scene.ups
    ? ups(scene, compact)
    : scene.reliability
      ? `<div id="reliability">${renderReliability(scene.id, state)}</div>`
      : renderContinuityVisual(scene, state, compact);
  $("actions").innerHTML = controls(scene);
  $("actions")
    .querySelectorAll("button")
    .forEach(
      (b) =>
        (b.onclick = () => {
          const { key, value } = b.dataset;
          state[key] =
            value === undefined
              ? !state[key]
              : key === "loadKW"
                ? Number(value)
                : value;
          render();
          const controls = [...$("actions").querySelectorAll("button")];
          const replacement =
            controls.find(
              (control) =>
                control.dataset.key === key && control.dataset.value === value,
            ) || controls.find((control) => control.dataset.key === key);
          replacement?.focus({ preventScroll: true });
        }),
    );
  $("scenes").innerHTML = scenes
    .map(
      (s, i) =>
        `<option value="${i}" ${i === index ? "selected" : ""}>${i + 1}. ${esc(s.label)}</option>`,
    )
    .join("");
  $("progress").textContent = `${index + 1} / ${scenes.length}`;
  $("previous").disabled = index === 0;
  $("next").disabled = index === scenes.length - 1;
  history.replaceState(null, "", `#${scene.id}`);
}
function go(i) {
  index = Math.max(0, Math.min(scenes.length - 1, i));
  state = fresh();
  render();
  window.scrollTo(0, 0);
}
$("scenes").onchange = (e) => go(Number(e.target.value));
$("previous").onclick = () => go(index - 1);
$("next").onclick = () => go(index + 1);
$("fullscreen").onclick = () =>
  document.fullscreenElement
    ? document.exitFullscreen()
    : document.documentElement.requestFullscreen();
window.addEventListener("hashchange", () =>
  go(resolveContinuityScene(location.hash.slice(1))),
);
document.addEventListener("keydown", (e) => {
  if (
    e.altKey ||
    e.metaKey ||
    e.ctrlKey ||
    /INPUT|TEXTAREA|SELECT/.test(e.target.tagName)
  )
    return;
  if (["ArrowRight", "PageDown", "ArrowLeft", "PageUp"].includes(e.key)) {
    e.preventDefault();
    go(index + (["ArrowRight", "PageDown"].includes(e.key) ? 1 : -1));
  }
  if (e.key === "Home") {
    e.preventDefault();
    go(0);
  }
  if (e.key === "End") {
    e.preventDefault();
    go(scenes.length - 1);
  }
});
matchMedia("(max-width:799px)").addEventListener("change", render);
render();
