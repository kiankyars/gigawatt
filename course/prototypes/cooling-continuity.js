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
function cdu(id, x, y, w, failed) {
  return (
    box(id, x, y, w, 72, failed) +
    label(x + w / 2, y + 25, id.replace("cdu", "CDU "), "svg-small", id) +
    label(
      x + w / 2,
      y + 51,
      failed ? "Isolated" : "600 kW",
      failed ? "svg-label fault-text" : "svg-label",
      id,
    )
  );
}
function spareCDUs(compact, m) {
  const p = m.paths[0];
  const available = p.facilityPathAvailable;
  let out = label(
    compact ? 186 : 580,
    26,
    "N = 2 CDUs · 3 INSTALLED = N+1",
    "svg-tiny",
  );
  if (compact) {
    out +=
      box("load", 93, 53, 186, 72) +
      label(186, 80, "Selected heat load", "svg-small", "load") +
      label(186, 108, "1,000 kW", "svg-label", "load");
    out += route("M186 125 V157 M66 157 H306 M186 308 V342", available);
    for (let i = 0; i < 3; i++) {
      const x = 15 + i * 120,
        failed = i < p.failedModules;
      out += route(
        `M${x + 51} 157 V193 M${x + 51} 265 V308`,
        available && !failed,
        true,
      );
      out += cdu(`cdu${i + 1}`, x, 193, 102, failed);
    }
    out += route("M66 308 H306", available);
    out +=
      box("facility", 38, 342, 296, 88, !available) +
      label(186, 369, "Shared facility path", "svg-label", "facility") +
      label(
        186,
        394,
        available ? "Pumps + outdoor heat rejection" : "Unavailable",
        available ? "svg-small" : "svg-label fault-text",
        "facility",
      ) +
      label(186, 416, "Shared power and controls", "svg-small", "facility");
    out += route("M186 430 V468", available, true);
  } else {
    out +=
      box("load", 30, 146, 170, 116) +
      label(115, 182, "Selected heat load", "svg-small", "load") +
      label(115, 224, "1,000 kW", "svg-label", "load");
    out += route("M200 204 H270 M270 100 V308 M620 100 V308", available);
    out += route("M620 204 H739", available, true);
    for (let i = 0; i < 3; i++) {
      const y = 64 + i * 104,
        failed = i < p.failedModules;
      out += route(
        `M270 ${y + 36} H355 M525 ${y + 36} H620`,
        available && !failed,
        true,
      );
      out += cdu(`cdu${i + 1}`, 355, y, 170, failed);
    }
    out +=
      box("facility", 739, 144, 300, 120, !available) +
      label(889, 174, "Shared facility path", "svg-label", "facility") +
      label(
        889,
        203,
        available ? "Pumps + outdoor heat rejection" : "Unavailable",
        available ? "svg-small" : "svg-label fault-text",
        "facility",
      ) +
      label(889, 234, "Shared power and controls", "svg-small", "facility");
    out += route("M1039 204 H1120", available, true);
  }
  return out + capacity(m, compact);
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
function reducedPower(compact, m) {
  const removed = Math.min(m.availableKw, m.loadKw);
  const accumulating = Math.max(0, m.loadKw - removed);
  const result =
    m.availableKw === 0
      ? "No sustained heat-removal path"
      : accumulating > 0
        ? `Heat accumulates at ${fmt(accumulating)} kW`
        : `${fmt(m.marginKw)} kW cooling margin`;
  const color = m.supportsLoad ? "facility-text" : "fault-text";
  let out =
    label(
      compact ? 186 : 580,
      25,
      "Cooling alert → configured power cap",
      "svg-small",
    ) +
    label(
      compact ? 186 : 580,
      49,
      "Chip temperature → thermal protection",
      "svg-small",
    );
  if (compact) {
    out +=
      label(186, 85, "Heat into liquid path", "svg-small") +
      label(186, 130, `${fmt(m.loadKw)} kW`, "svg-number heat-text") +
      route("M186 150 V197", true, true);
    out +=
      box("balance", 28, 198, 316, 123) +
      label(186, 228, "Remaining cooling path", "svg-label", "balance") +
      label(
        186,
        267,
        `${fmt(m.availableKw)} kW available`,
        `svg-label ${color}`,
        "balance",
      ) +
      label(
        186,
        297,
        m.availableKw
          ? "One of three CDUs remains"
          : "Facility flow unavailable",
        "svg-small",
        "balance",
      );
    out +=
      route("M186 321 V351", removed > 0, true) +
      label(186, 405, `${fmt(removed)} kW`, "svg-number facility-text") +
      label(186, 433, "Heat removed in this model", "svg-small");
    out +=
      label(186, 481, result, `svg-label ${color}`) +
      label(
        186,
        520,
        "Heat rates only; no time-to-overheat model.",
        "svg-small",
      ) +
      label(186, 546, "Reduced heat is assumed, not automatic.", "svg-small");
  } else {
    out +=
      label(167, 134, "Heat into liquid path", "svg-small") +
      label(167, 182, `${fmt(m.loadKw)} kW`, "svg-number heat-text");
    out += route("M85 220 H406", true, true);
    out +=
      box("balance", 407, 116, 342, 162) +
      label(578, 152, "Remaining cooling path", "svg-label", "balance") +
      label(
        578,
        199,
        `${fmt(m.availableKw)} kW available`,
        `svg-label ${color}`,
        "balance",
      ) +
      label(
        578,
        238,
        m.availableKw
          ? "One of three CDUs remains"
          : "Facility flow unavailable",
        "svg-small",
        "balance",
      );
    out +=
      route("M749 220 H1090", removed > 0, true) +
      label(950, 134, "Heat removed in this model", "svg-small") +
      label(950, 182, `${fmt(removed)} kW`, "svg-number facility-text");
    out +=
      label(580, 332, result, `svg-number ${color}`) +
      label(
        580,
        392,
        "Reduced heat is an assumed coordinated action; transition time and safe temperatures are not predicted.",
        "svg-small",
      );
  }
  return out;
}

export function renderContinuity(kind, compact, state = {}) {
  const topology = kind === "independent-paths" ? "2n" : "n+1";
  const fault =
    kind === "derating"
      ? "double-module"
      : kind === "independent-paths"
        ? state.pathFault || "shared-path"
        : state.cduFault || "module";
  const m = coolingContinuity({
    topology,
    fault,
    loadMode: kind === "derating" ? state.loadMode || "full" : "full",
    allPathsLost: kind === "derating" && Boolean(state.deratingPathLost),
  });
  const content =
    kind === "derating"
      ? reducedPower(compact, m)
      : kind === "independent-paths"
        ? independentPaths(compact, m)
        : spareCDUs(compact, m);
  return `<g data-cooling-capacity="${m.availableKw}" data-cooling-load="${m.loadKw}" data-cooling-margin="${m.marginKw}" data-cooling-topology="${m.topology}" data-cooling-fault="${m.fault}" data-supported="${m.supportsLoad}">${content}</g>`;
}
