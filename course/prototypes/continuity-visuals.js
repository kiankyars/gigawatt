import { renderGrounding, renderInterruption, renderDCProtection } from "./continuity-protection.js";
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

function equipment() {
  return `<div class="equipment-specs"><figure class="product"><img src="../assets/references/schneider-easy-ups-3phase-modular.jpg" alt="Black and white cabinets from Schneider Electric’s Easy UPS 3-Phase Modular family."><figcaption>Schneider Electric · Easy UPS 3-Phase Modular</figcaption></figure><article><h2>50–250 kW</h2><p class="equipment-dimensions">1.991 m H × 0.600 m W × 0.850 m D</p><p>Black and white cabinet finishes</p><div class="equipment-function"><strong>Inside the UPS</strong><p>Rectifier · DC link · inverter<br>Battery interface · static bypass<br>Controls and cooling</p></div><div class="equipment-function"><strong>Batteries: external cabinets</strong><p>Connected to the UPS battery interface</p></div></article></div><div class="equipment-locations"><span><strong>Facility UPS</strong>Electrical support room</span><span><strong>Rack battery backup unit (BBU)</strong>Direct current backup at the rack</span></div>`;
}
function storage() {
  return `<div class="storage-energy">1.0 MWh × 80% usable window − 0.2 MWh reserve <span>→ 95% conversion →</span><strong>0.57 MWh to load</strong></div><div class="comparison">${[
    8, 4,
  ]
    .map((p) => {
      const m = storageModel(p);
      return `<article><h2>${p} MW output limit</h2><div class="large">6 MW demand</div><div class="loadbar"><span style="width:${(p / 8) * 100}%"></span><i style="left:75%"></i></div><div class="status ${m.canSupport ? "" : "fail"}">${m.canSupport ? "5.7 minutes at 6 MW" : "Full load cannot be supplied"}</div><div class="details">${m.canSupport ? "0.57 MWh ÷ 6 MW × 60" : "2 MW of demand remains unsupported."}</div></article>`;
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
  return `<div class="sparks"><figure><img src="../assets/references/continuity-sparks-site.png" alt="Redwood Materials aerial photograph of its battery arrays and Crusoe Spark units at the Sparks deployment."><figcaption class="source-credit">Sparks, Nevada · photograph: Redwood Materials</figcaption></figure><svg class="visual" viewBox="0 0 ${compact ? "380 430" : "590 550"}" role="img" aria-label="The Sparks source reports 12 MW solar and 63 MWh battery inventory with grid backup. Battery discharge power and usable energy are not given here.">${drawing}</svg></div><div class="sparks-calculation"><span>At a constant 12 MW load, using 63 MWh</span><strong>63 MWh ÷ 12 MW = 5.25 hours</strong><span>The site’s 12 MW figure is its solar-array rating.</span></div>`;
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
  return `${wrap(body, `Fault on ${m.fault === "bus" ? "shared bus" : "branch B"}; isolation state ${m.zone}; ${m.healthy.filter(Boolean).length} healthy load groups remain supplied.`, compact, compact ? 460 : 450)}<div class="boundary">${m.zone === "bus" ? "Fault present · upstream contacts still closed" : m.zone === "bus-cleared" ? "Upstream breaker clears the fault; the shared bus remains unavailable." : ""}</div>`;
}
function service(state) {
  const m = serviceModel({stage: state.serviceStage || "bridge", protectedControls: state.protectedControls});
  const rows = [
    ["Compute racks", "UPS", true, "Powered"],
    ["Cooling controls", state.protectedControls ? "UPS" : "Utility only", m.controls, m.controls ? "Powered" : "Off → workload interlock stops compute"],
    ["Cooling pumps", "Generator-backed", m.pumps, m.pumps ? "Powered" : "Waiting for generator"],
    ["Heat rejection", "Restarts after transfer", m.heatRejection, m.heatRejection ? "Available" : "Restart pending"],
  ];
  return `<div class="service-exercise"><p class="service-scenario">Utility power fails. The rack UPS works, and the generator starts successfully.</p><div class="service-matrix"><div class="service-matrix-head"><span>Equipment</span><span>Power source</span>${state.serviceReveal ? '<span>After the outage</span>' : ''}</div>${rows.map(([name,source,ok,result])=>`<div class="service-matrix-row"><strong>${name}</strong><span>${source}</span>${state.serviceReveal ? `<span class="service-result ${ok ? 'ok' : 'lost'}">${result}</span>` : ''}</div>`).join('')}</div><div class="service-prompt">${!state.serviceReveal ? 'What still stops the workload, and which power path would you change?' : !m.controls ? 'Put the cooling controls on a protected supply.' : m.stage === 'normal' ? 'All four systems have power.' : 'Controls now stay on. Next, check the temperature rise while pumps and heat rejection restart.'}</div></div>`;
}

export function renderContinuityVisual(scene, state, compact) {
  return (
    {
      campus: () =>
        `<div class="continuity-opening"><img src="../assets/generated/continuity-electrical-room.png" alt="Electrical support room beside a data hall; UPS cabinets and separate battery storage maintain the protected rack supply."></div>`,
      equipment: () => equipment(compact),
      "storage-limits": storage,
      "sparks-storage": () => sparks(compact),
      "fault-isolation": () => faultIsolation(state, compact),
      grounding: () => renderGrounding(compact),
      "ac-dc-interruption": () => renderInterruption(state.arcStage || "arc"),
      "dc-feeder-protection": () => renderDCProtection(compact),
      "service-check": () => service(state),
    }[scene.id]?.() || ""
  );
}
