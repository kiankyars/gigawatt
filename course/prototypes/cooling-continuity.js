import { coolingContinuity } from "./cooling-model.js?v=20260911-continuity4";

const label = (x, y, value, cls = "svg-label", owner = "", anchor = "middle") =>
  `<text x="${x}" y="${y}" text-anchor="${anchor}" class="${cls}"${owner ? ` data-label-for="continuity-${owner}"` : ""}>${value}</text>`;
const box = (id, x, y, w, h, failed = false) =>
  `<rect id="continuity-${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="10" class="panel"${failed ? ' style="stroke:var(--fault);stroke-dasharray:5 4;fill:var(--paper)"' : ""}/>`;
const route = (d, active = true, arrow = false) =>
  `<path d="${d}" fill="none" stroke="var(--${active ? "heat" : "muted"})" stroke-width="${active ? 4 : 2}"${active ? "" : ' stroke-dasharray="6 5"'}${arrow && active ? ' marker-end="url(#heat-arrow)"' : ""}/>`;
const fmt = (n) => n.toLocaleString("en-US");
function capacity(m, compact) {
  const text = `${fmt(m.availableKw)} kW ${m.supportsLoad ? "≥" : "<"} ${fmt(m.loadKw)} kW`;
  return (
    label(
      compact ? 186 : 580,
      compact ? 520 : 385,
      text,
      `svg-number ${m.supportsLoad ? "facility-text" : "fault-text"}`,
    ) +
    label(
      compact ? 186 : 580,
      compact ? 550 : 412,
      "Available cooling vs. heat load",
      "svg-small",
    )
  );
}
function redundancyComparison(compact) {
  const base = coolingContinuity({ topology: "n+1", fault: "none" });
  const moduleKw = base.moduleKw;
  const n = base.requiredModules;
  const cards = [
    { id: "n", name: "N", count: n, title: "The CDUs needed for the load", result: "No spare CDU" },
    { id: "n-plus-one", name: "N+1", count: n + 1, title: "One extra CDU", result: "Lose one CDU → two remain" },
    { id: "two-n", name: "2N", count: n * 2, title: "Two complete cooling trains", result: "Either train can carry the load" },
  ];
  let out = label(compact ? 186 : 580, 25, `${fmt(base.fullLoadKw)} kW heat · ${moduleKw} kW per CDU`, "svg-small");
  cards.forEach((card, index) => {
    const x = compact ? 18 : 20 + index * 380;
    const y = compact ? 55 + index * 164 : 63;
    const w = compact ? 336 : 360;
    const h = compact ? (index === 2 ? 185 : 152) : 316;
    const cx = x + w / 2;
    out += `<g data-redundancy-case="${card.id}" data-installed-cdus="${card.count}" data-required-cdus="${n}">`;
    out += box(card.id, x, y, w, h);
    if (compact) {
      out += label(x + 20, y + 39, card.name, "svg-number", card.id, "start");
      if (index < 2) {
        out += label(x + 128, y + 33, index ? "One extra CDU" : "Two CDUs needed", "svg-label", card.id, "start");
        const moduleW = 62, gap = 10;
        const rowX = cx - (card.count * moduleW + (card.count - 1) * gap) / 2;
        for (let i = 0; i < card.count; i++) {
          const mx = rowX + i * (moduleW + gap);
          const id = `${card.id}-cdu${i}`;
          out += box(id, mx, y + 59, moduleW, 42);
          out += label(mx + moduleW / 2, y + 85, `${moduleKw}`, "svg-label", id);
        }
        out += label(cx, y + 127, card.result, "svg-small", card.id);
        if (index === 1)
          out += label(cx, y + 146, "Facility path is still shared", "svg-small", card.id);
      } else {
        out += label(x + 116, y + 33, "Two complete trains", "svg-label", card.id, "start");
        ["A", "B"].forEach((train, i) => {
          const id = `${card.id}-train${train}`, ty = y + 53 + i * 50;
          out += box(id, x + 15, ty, w - 30, 40);
          out += label(cx, ty + 25, `${train} · 2 CDUs + its own facility path`, "svg-small", id);
        });
        out += label(cx, y + 170, card.result, "svg-small", card.id);
      }
    } else {
      out += label(cx, y + 48, card.name, "svg-number", card.id);
      out += label(cx, y + 87, card.title, "svg-label", card.id);
      if (index < 2) {
        const moduleW = 76, gap = 14;
        const rowX = cx - (card.count * moduleW + (card.count - 1) * gap) / 2;
        for (let i = 0; i < card.count; i++) {
          const mx = rowX + i * (moduleW + gap);
          const id = `${card.id}-cdu${i}`;
          out += box(id, mx, y + 132, moduleW, 67);
          out += label(mx + moduleW / 2, y + 159, "CDU", "svg-small", id);
          out += label(mx + moduleW / 2, y + 184, `${moduleKw} kW`, "svg-label", id);
        }
        out += label(cx, y + 249, card.result, "svg-label", card.id);
        if (index === 1)
          out += label(cx, y + 282, "Facility path is still shared", "svg-small", card.id);
      } else {
        ["A", "B"].forEach((train, i) => {
          const id = `${card.id}-train${train}`, ty = y + 118 + i * 65;
          out += box(id, x + 20, ty, w - 40, 53);
          out += label(cx, ty + 23, `Train ${train} · 2 CDUs`, "svg-label", id);
          out += label(cx, ty + 43, "Own facility loop, plant, power + controls", "svg-small", id);
        });
        out += label(cx, y + 282, card.result, "svg-small", card.id);
      }
    }
    out += "</g>";
  });
  return `<g data-continuity-diagram data-cooling-comparison="redundancy" data-cooling-load="${base.fullLoadKw}" data-cdu-capacity="${moduleKw}">${out}</g>`;
}
function independentPaths(compact, m) {
  let out = label(
    compact ? 186 : 580,
    25,
    "2N · EACH TRAIN CAN CARRY 1,000 kW",
    "svg-tiny",
  );
  if (compact) {
    out +=
      box("load", 89, 51, 194, 66) +
      label(186, 78, "Shared load interface", "svg-small", "load") +
      label(186, 103, "1,000 kW", "svg-label", "load");
    out += route("M186 117 V141 M97 141 H275", true);
    m.paths.forEach((p, i) => {
      const x = 15 + i * 178,
        cx = x + 82,
        active = p.id === m.selectedPathId;
      out += route(`M${cx} 141 V176 M${cx} 427 V474`, active, true);
      out += box(`train${p.id}`, x, 176, 164, 251, !p.facilityPathAvailable);
      out += label(cx, 204, `Train ${p.id}`, "svg-label", `train${p.id}`);
      out += label(cx, 234, "2 × 600 kW CDUs", "svg-small", `train${p.id}`);
      out += label(cx, 268, "Facility loop", "svg-label", `train${p.id}`);
      out += label(cx, 293, "Outdoor plant", "svg-label", `train${p.id}`);
      out += label(cx, 318, "Power + controls", "svg-small", `train${p.id}`);
      out += label(
        cx,
        365,
        p.facilityPathAvailable ? "1,200 kW" : "Unavailable",
        p.facilityPathAvailable
          ? "svg-label facility-text"
          : "svg-label fault-text",
        `train${p.id}`,
      );
      out += label(
        cx,
        396,
        active
          ? "Serving load"
          : p.facilityPathAvailable
            ? "Ready"
            : "Isolated",
        "svg-small",
        `train${p.id}`,
      );
    });
  } else {
    out +=
      box("load", 30, 151, 180, 103) +
      label(120, 182, "Shared load interface", "svg-small", "load") +
      label(120, 220, "1,000 kW", "svg-label", "load");
    out += route("M210 202 H277 M277 107 V293", true);
    m.paths.forEach((p, i) => {
      const y = 46 + i * 186,
        cy = y + 61,
        active = p.id === m.selectedPathId;
      out += route(`M277 ${cy} H330 M1060 ${cy} H1121`, active, true);
      out += box(`train${p.id}`, 330, y, 730, 122, !p.facilityPathAvailable);
      out += label(
        355,
        y + 30,
        `TRAIN ${p.id}`,
        "svg-tiny",
        `train${p.id}`,
        "start",
      );
      out += label(490, y + 66, "2 × 600 kW CDUs", "svg-label", `train${p.id}`);
      out += label(
        742,
        y + 59,
        "Facility loop + outdoor plant",
        "svg-label",
        `train${p.id}`,
      );
      out += label(
        742,
        y + 87,
        "Independent power and controls",
        "svg-small",
        `train${p.id}`,
      );
      out += label(
        974,
        y + 63,
        p.facilityPathAvailable ? "1,200 kW" : "Unavailable",
        p.facilityPathAvailable
          ? "svg-label facility-text"
          : "svg-label fault-text",
        `train${p.id}`,
      );
      out += label(
        974,
        y + 91,
        active
          ? "Serving load"
          : p.facilityPathAvailable
            ? "Ready"
            : "Isolated",
        "svg-small",
        `train${p.id}`,
      );
    });
  }
  return out + capacity(m, compact);
}
function reducedPower(compact) {
  const cases = ["full", "reduced"].map((loadMode) => coolingContinuity({
    topology: "n+1", fault: "double-module", loadMode,
  }));
  let out = label(compact ? 186 : 580, 25, "Two CDUs fail → 600 kW cooling remains", "svg-small");
  cases.forEach((m, index) => {
    const id = `power-${m.loadMode}`;
    const x = compact ? 18 : 30 + index * 570;
    const y = compact ? 58 + index * 230 : 66;
    const w = compact ? 336 : 530;
    const h = compact ? 210 : 278;
    const cx = x + w / 2;
    const bx = x + 28, by = y + (compact ? 85 : 113), bw = w - 56;
    const limitX = bx + bw * m.availableKw / m.fullLoadKw;
    const excessKw = Math.max(0, m.loadKw - m.availableKw);
    out += `<g data-load-case="${m.loadMode}" data-case-heat="${m.loadKw}" data-case-capacity="${m.availableKw}" data-case-margin="${m.marginKw}" data-case-supported="${m.supportsLoad}">`;
    out += box(id, x, y, w, h);
    out += label(cx, y + 33, index ? "Reduced load" : "Original load", "svg-label", id);
    out += label(cx, y + (compact ? 65 : 82), `${fmt(m.loadKw)} kW heat`, compact ? "svg-label heat-text" : "svg-number heat-text", id);
    out += `<rect x="${bx}" y="${by}" width="${bw}" height="27" rx="5" fill="var(--muted)" opacity="0.12"/>`;
    out += `<rect x="${bx}" y="${by}" width="${bw * m.loadKw / m.fullLoadKw}" height="27" rx="5" fill="var(--heat)"/>`;
    out += `<path d="M${limitX} ${by - 8} V${by + 40}" stroke="var(--facility)" stroke-width="3" stroke-dasharray="5 3"/>`;
    out += label(limitX, by + 59, "600 kW capacity", "svg-small facility-text", id);
    out += label(cx, y + (compact ? 188 : 236), excessKw ? `${fmt(excessKw)} kW excess heat` : `${fmt(m.marginKw)} kW cooling margin`, `svg-label ${excessKw ? "fault-text" : "facility-text"}`, id);
    out += "</g>";
  });
  out += label(compact ? 186 : 580, compact ? 548 : 395, compact ? "An IT power cap reduces heat." : "A configured IT power cap lowers the heat entering the coolant.", "svg-small");
  return `<g data-continuity-diagram data-cooling-comparison="derating" data-full-load="${cases[0].loadKw}" data-reduced-load="${cases[1].loadKw}" data-remaining-cooling="${cases[0].availableKw}">${out}</g>`;
}

export function renderContinuity(kind, compact, state = {}) {
  if (kind === "redundancy") return redundancyComparison(compact);
  if (kind === "derating") return reducedPower(compact);
  const m = coolingContinuity({
    topology: "2n",
    fault: state.pathFault || "shared-path",
    loadMode: "full",
  });
  return `<g data-continuity-diagram data-cooling-capacity="${m.availableKw}" data-cooling-load="${m.loadKw}" data-cooling-margin="${m.marginKw}" data-cooling-topology="${m.topology}" data-cooling-fault="${m.fault}" data-supported="${m.supportsLoad}">${independentPaths(compact, m)}</g>`;
}
