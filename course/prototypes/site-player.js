import { scenes, initialState, siteSceneRedirect } from "./site-scenes.js";
import { renderSite } from "./site-visuals.js";
import { operationsAliases } from "./site-operations.js";
const $ = (id) => document.getElementById(id),
  state = { ...initialState };
const teaching =
  new URLSearchParams(location.search).get("teach") === "1";
$("fullscreen").hidden = !teaching;
let index = 0;
for (const [i, s] of scenes.entries())
  $("scenes").add(new Option(`${i + 1} · ${s.label}`, s.id));
function draw() {
  const scene = scenes[index],
    compact = matchMedia("(max-width:600px)").matches,
    { markup, description } = renderSite(scene.id, state, compact);
  $("scene-content").innerHTML = markup;
  $("status").textContent = description;
}
function controls() {
  $("actions").replaceChildren();
  for (const group of scenes[index].controls || []) {
    const field = document.createElement("fieldset");
    field.className = "choices";
    const legend = document.createElement("legend");
    legend.textContent = group.label;
    field.append(legend);
    for (const [value, label] of group.options) {
      const b = document.createElement("button");
      b.textContent = label;
      b.dataset.key = group.key;
      b.dataset.value = String(value);
      b.setAttribute("aria-pressed", String(state[group.key] === value));
      b.onclick = () => {
        state[group.key] = value;
        field
          .querySelectorAll("button")
          .forEach((button) =>
            button.setAttribute("aria-pressed", String(button === b)),
          );
        draw();
      };
      field.append(b);
    }
    $("actions").append(field);
  }

}
function render() {
  const s = scenes[index];
  $("title").textContent = s.title;
  $("scenes").value = s.id;
  $("progress").textContent = `${index + 1} / ${scenes.length}`;
  $("previous").disabled = index === 0;
  $("next").disabled = index === scenes.length - 1;
  $("lesson-reference").href = "../index.html#" + s.reference;
  controls();
  draw();
}
function go(i) {
  index = Math.max(0, Math.min(scenes.length - 1, i));
  history.replaceState(null, "", `#${scenes[index].id}`);
  render();
}
function fromHash() {
  const redirect = siteSceneRedirect(location.href);
  if (redirect) {
    location.replace(redirect);
    return;
  }
  const target =
      operationsAliases[location.hash.slice(1)] || location.hash.slice(1),
    i = scenes.findIndex((s) => s.id === target);
  index = i < 0 ? 0 : i;
  render();
}
$("scenes").onchange = (e) =>
  go(scenes.findIndex((s) => s.id === e.target.value));
$("previous").onclick = () => go(index - 1);
$("next").onclick = () => go(index + 1);
$("fullscreen").onclick = async () => {
  try {
    if (document.fullscreenElement) await document.exitFullscreen();
    else await $("viewer").requestFullscreen();
  } catch {
    $("fullscreen").textContent = "Use browser full screen";
  }
};
document.addEventListener("fullscreenchange", () => {
  $("fullscreen").textContent = document.fullscreenElement
    ? "Exit full screen"
    : "Full screen";
});
window.addEventListener("keydown", (e) => {
  if (
    e.altKey ||
    e.ctrlKey ||
    e.metaKey ||
    e.target.closest("button,select,input,textarea,a,[contenteditable]")
  )
    return;
  if (e.key === "ArrowRight") {
    e.preventDefault();
    go(index + 1);
  }
  if (e.key === "ArrowLeft") {
    e.preventDefault();
    go(index - 1);
  }
  if (e.key.toLowerCase() === "f" && teaching) $("fullscreen").click();
});
window.addEventListener("hashchange", fromHash);
matchMedia("(max-width:600px)").addEventListener("change", draw);
fromHash();
