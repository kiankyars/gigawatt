import {
  storageModel,
  isolationModel,
  serviceModel,
} from "./continuity-model.js";
export const esc = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll('"', "&quot;");
const text = (x, y, value, cls = "s-label", anchor = "middle") =>
  `<text x="${x}" y="${y}" text-anchor="${anchor}" class="${cls}">${value}</text>`;
const box = (x, y, w, h, lines, active = true) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="9" class="s-node"/>${lines.map((line, i) => text(x + w / 2, y + h / 2 + (i - (lines.length - 1) / 2) * 27 + 7, line, i ? "s-small" : "s-label")).join("")}${active ? "" : `<path d="M${x + 8} ${y + 8}L${x + w - 8} ${y + h - 8}" stroke="var(--red)" stroke-width="3"/>`}`;
const path = (d, active = true) =>
  `<path d="${d}" class="s-wire ${active ? "" : "s-off"}"/>`;
const dot = (x, y) => `<circle cx="${x}" cy="${y}" r="5" fill="var(--green)"/>`;
const wrap = (body, label, compact = false, height = 480) =>
  `<svg class="visual" viewBox="0 0 ${compact ? 380 : 1180} ${height}" role="img" aria-label="${esc(label)}">${body}</svg>`;
const photo = (src, alt, name, credit) =>
  `<figure class="product"><img src="../assets/references/${src}" alt="${alt}"><h2>${name}</h2><figcaption>${credit}</figcaption></figure>`;

function equipment(compact) {
  const batteryDrawing = compact
    ? box(10, 20, 140, 135, ["Batteries"]) +
      text(80, 63, "+  −", "s-label") +
      path("M150 88H200") +
      box(200, 40, 170, 95, ["UPS DC link", "Interface"])
    : box(95, 30, 190, 190, ["+  −", "External batteries"]) +
      path("M285 125H410") +
      box(410, 65, 280, 120, ["UPS DC link", "Battery interface"]);
  return `<div class="pair">${photo("schneider-easy-ups-3phase-modular.jpg", "Schneider Easy UPS 3-Phase Modular product-family photograph showing UPS cabinets.", "Facility AC UPS", "Schneider Electric · Easy UPS 3-Phase Modular")}<div class="battery-location">${wrap(batteryDrawing, "A separate battery cabinet connects to the UPS DC link through its battery interface.", compact, compact ? 175 : 250).replace("0 0 1180 250", "0 0 740 250")}<p>Electrical room: UPS + external batteries<br>Rack BBU: local DC backup<br>Campus BESS: a larger storage system</p><div class="source-credit">BBU = battery backup unit · BESS = battery energy storage system</div></div></div>`;
}
function storage() {
  return `<div class="storage-energy">1.0 MWh × 80% usable window − 0.2 MWh reserve <span>→ 95% conversion →</span><strong>0.57 MWh to load</strong></div><div class="comparison">${[
    8, 4,
  ]
    .map((p) => {
      const m = storageModel(p);
      return `<article><h2>${p} MW output limit</h2><div class="large">6 MW demand</div><div class="loadbar"><span style="width:${(p / 8) * 100}%"></span><i style="left:75%"></i></div><div class="status ${m.canSupport ? "" : "fail"}">${m.canSupport ? "5.7 minutes at 6 MW" : "Full load cannot be supplied"}</div><div class="details">${m.canSupport ? "Power screen passes.<br>0.57 MWh ÷ 6 MW × 60" : "More duration cannot repair<br>a 2 MW power shortfall."}</div></article>`;
    })
    .join("")}</div>`;
}
function sparks(compact) {
  const drawing = compact
    ? box(10, 15, 170, 95, ["Solar", "12 MW"]) +
      box(200, 15, 170, 95, ["Battery inventory", "63 MWh"]) +
      path("M95 110V160H190V205 M285 110V160H190") +
      box(95, 205, 190, 90, ["Crusoe Spark", "Compute load"]) +
      path("M190 360V295") +
      text(190, 395, "Grid backup", "s-label")
    : box(10, 30, 235, 105, ["Solar", "12 MW"]) +
      box(305, 30, 260, 105, ["Battery inventory", "63 MWh"]) +
      path("M125 135V225H280V295 M435 135V225H280") +
      box(145, 295, 275, 100, ["Crusoe Spark", "Compute load"]) +
      path("M280 475V395") +
      text(280, 513, "Grid backup", "s-label");
  return `<div class="sparks"><figure><img src="../assets/references/continuity-sparks-site.png" alt="Redwood Materials aerial photograph of its battery arrays and Crusoe Spark units at the Sparks deployment."><figcaption class="source-credit">Sparks, Nevada · photograph: Redwood Materials</figcaption></figure><svg class="visual" viewBox="0 0 ${compact ? "380 430" : "590 550"}" role="img" aria-label="The Sparks source reports 12 MW solar and 63 MWh battery inventory with grid backup. Battery discharge power and usable energy are not given here.">${drawing}</svg></div><div class="boundary"><span>Night coverage needs <strong>load + usable MWh + discharge MW</strong></span><span>63 MWh ÷ 12 MW cannot establish that duration.</span></div>`;
}
function faultIsolation(state, compact) {
  const m = isolationModel(state.isolation || "branch"),
    W = compact ? 380 : 1180;
  const xs = compact ? [65, 190, 315] : [260, 590, 920];
  const busY = compact ? 175 : 165,
    breakerY = compact ? 235 : 235,
    rackY = compact ? 355 : 335;
  let body =
    box(W / 2 - 90, 10, 180, 68, ["Upstream supply"]) +
    path(`M${W / 2} 78V108`, m.upstream) +
    `<path d="M${W / 2} 108l${m.upstream ? 0 : 24} 30" stroke="${m.upstream ? "var(--green)" : "var(--red)"}" stroke-width="4"/>` +
    path(`M${W / 2} 138V${busY} M${xs[0]} ${busY}H${xs[2]}`, m.upstream);
  xs.forEach((x, i) => {
    body +=
      dot(x, busY) +
      path(`M${x} ${busY}V${breakerY}`, m.healthy[i]) +
      `<path d="M${x} ${breakerY}l${m.branchContactsClosed[i] ? 0 : 25} 35" stroke="${!m.branchContactsClosed[i] ? "var(--red)" : m.healthy[i] ? "var(--green)" : "var(--inactive-wire)"}" stroke-width="4"/>` +
      path(`M${x} ${breakerY + 35}V${rackY}`, m.healthy[i]) +
      box(x - (compact ? 51 : 100), rackY, compact ? 102 : 200, 80, [
        `Group ${"ABC"[i]}`,
        m.healthy[i]
          ? "Supplied"
          : m.branchContactsClosed[i]
            ? "No supply"
            : "Isolated",
      ]);
  });
  body += text(
    W / 2 + (compact ? 55 : 115),
    m.fault === "bus" ? busY - 12 : breakerY + 65,
    "⚡ Fault",
    "s-gold",
  );
  return `<div class="fault-steps"><span>Detect abnormal current</span><span>Identify protected zone</span><span>Interrupt the matching path</span></div>${wrap(body, `Fault on ${m.fault === "bus" ? "shared bus" : "branch B"}; isolation state ${m.zone}; ${m.healthy.filter(Boolean).length} healthy load groups remain supplied.`, compact, compact ? 460 : 450)}<div class="boundary"><span>Check coordination under utility, generator and converter supply.</span></div>`;
}
function grounding(compact) {
  const body = compact
    ? `<circle cx="70" cy="220" r="35" class="s-node"/><path d="M49 220c7-22 14-22 21 0s14 22 21 0" fill="none" stroke="var(--green)" stroke-width="3"/>` +
      text(145, 160, "Source", "s-small") +
      box(225, 145, 140, 185, ["Metal case"]) +
      path("M70 185V65H295V167") +
      `<path d="M295 167l-10 20h16l-6 21" fill="none" stroke="var(--gold)" stroke-width="4"/>` +
      path("M295 208H365V410H70V255") +
      dot(70, 410) +
      text(89, 100, "L", "s-small") +
      text(87, 291, "N", "s-small") +
      text(180, 392, "Protective conductor (PE)", "s-small") +
      path("M70 410V453 M46 453H94 M54 464H86 M62 475H78") +
      text(220, 474, "Source-earth bond", "s-small")
    : `<circle cx="120" cy="230" r="48" class="s-node"/><path d="M91 230c10-32 19-32 29 0s19 32 29 0" fill="none" stroke="var(--green)" stroke-width="3"/>` +
      text(270, 163, "Source winding", "s-label") +
      box(820, 155, 280, 210, []) +
      text(965, 337, "Exposed metal case", "s-label") +
      path("M120 182V60H960V183") +
      `<path d="M960 183l-15 25h24l-9 25" fill="none" stroke="var(--gold)" stroke-width="5"/>` +
      path("M960 233V290H1100V400H120V278") +
      dot(120, 400) +
      text(145, 100, "L", "s-label") +
      text(145, 318, "N", "s-label") +
      text(575, 380, "Protective conductor (PE)", "s-label") +
      text(1035, 200, "Fault", "s-small") +
      path("M120 400V445 M89 445H151 M99 457H141 M109 469H131") +
      text(285, 465, "Source-earth bond", "s-small");
  return `<div class="boundary"><span>Source referenced to earth · separate protective conductor (TN-S)</span></div>${wrap(body, "Conceptual TN-S fault loop: source line terminal, insulation fault at metal case, protective conductor returning to source neutral. The earth connection does not replace the return circuit.", compact, compact ? 505 : 495)}<div class="boundary"><span>Loop impedance determines fault current; detection must match the grounding scheme.</span></div>`;
}
function interruption() {
  const graph = (ac) => {
    const points = Array.from(
      { length: 121 },
      (_, i) =>
        `${30 + i * 3.6},${ac ? 120 - Math.sin((i / 120) * 4 * Math.PI) * 70 : 60}`,
    ).join(" ");
    return `<svg viewBox="0 0 490 245" role="img" aria-label="${ac ? "AC current crosses zero periodically." : "DC current has no recurring natural zero crossing."}"><path d="M30 25V205H470 M30 120H470" stroke="var(--line)" fill="none"/><polyline points="${points}" stroke="var(--green)" stroke-width="4" fill="none"/><text x="15" y="126" text-anchor="middle" fill="var(--muted)" font-size="17">0</text><text x="465" y="235" text-anchor="end" fill="var(--muted)" font-size="17">Time</text><text x="35" y="18" fill="var(--muted)" font-size="17">Current</text></svg>`;
  };
  return `<div class="wave-compare"><article><h2>AC circuit</h2>${graph(true)}<p>Periodic current zeros can assist interruption.<br>The gap must withstand the recovering voltage.</p></article><article><h2>DC circuit</h2>${graph(false)}<p>The device must force current to zero.<br>Inductors and capacitors can keep feeding the fault.</p></article></div><div class="boundary"><span>Match the device’s <strong>AC/DC duty, voltage and fault-current rating</strong></span></div>`;
}
function service(state) {
  const m = serviceModel({
    stage: state.serviceStage || "bridge",
    protectedControls: state.protectedControls,
  });
  const track = (name, condition, label) =>
    `<div class="track"><strong>${name}</strong><span class="state ${condition === "pending" ? "pending" : condition ? "" : "failed"}">${label}</span></div>`;
  return `<div class="service-check"><div class="flow-strip"><div><strong>IT</strong>UPS → racks<br>Power bridge passes</div><div><strong>Pumps</strong>Generator-backed<br>Wait for transfer</div><div><strong>Controls</strong>${state.protectedControls ? "UPS-backed" : "Utility-only feed"}<br>Loss trips service interlock</div><div><strong>Heat rejection</strong>Restarts after power<br>Thermal margin unknown</div></div>${state.serviceReveal ? "" : `<p class="question">During the outage, identify the missing path. Then decide what evidence is still needed after it is repaired.</p>`}${state.serviceReveal ? `<div class="service-tracks">${track("IT power", true, "Energized throughout")}${track("Cooling controls", m.controls, m.controls ? "Powered" : "Lost → service interlock stops the workload")}${track("Pumps", m.pumps, m.pumps ? "Powered" : "Awaiting accepted generator")}${track("Heat rejection", m.heatRejection ? "pending" : false, m.heatRejection ? "Operating state still needs thermal evidence" : "Restart pending")}</div><div class="answer">${!m.controls ? "The rack can have voltage while the cooling-control interlock requires a stop." : m.stage === "normal" ? "All specified paths are present in normal operation." : "Restoring control power repairs one dependency. Demonstrate temperature margin through pump transfer and heat-rejection restart before claiming continued service."}</div>` : '<div class="service-note">Configured scenario: a cooling-control power loss stops the workload. No thermal ride-through duration is supplied.</div>'}</div>`;
}

export function renderContinuityVisual(scene, state, compact) {
  return (
    {
      campus: () =>
        `<div class="continuity-opening"><img src="../assets/generated/continuity-electrical-room.png" alt="Electrical support room beside a data hall; UPS cabinets and separate battery storage maintain the protected rack supply."><div class="opening-jobs"><span>Keep AC output alive</span><span>Bridge to another source</span><span>Keep cooling and controls available</span></div></div>`,
      equipment: () => equipment(compact),
      "storage-limits": storage,
      "sparks-storage": () => sparks(compact),
      "fault-isolation": () => faultIsolation(state, compact),
      grounding: () => grounding(compact),
      "ac-dc-interruption": interruption,
      "service-check": () => service(state),
    }[scene.id]?.() || ""
  );
}
