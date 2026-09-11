const esc = (value) =>
  String(value).replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const text = (x, y, value, cls = "diagram-detail", anchor = "middle") =>
  `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${esc(value)}</text>`;
const path = (d, active, name) =>
  `<path d="${d}" class="wire ${active ? "active" : ""}" data-path="${name}"/>`;
const contact = (x, y, closed, active, name, rotate = 0) =>
  `<g transform="translate(${x} ${y}) rotate(${rotate})" data-contact="${name}" data-closed="${closed}"><circle cx="-14" cy="0" r="3" fill="var(--muted, #63716b)"/><circle cx="14" cy="0" r="3" fill="var(--muted, #63716b)"/><path d="M-14 0L${closed ? "14 0" : "10 -14"}" class="wire ${active ? "active" : ""}"/></g>`;
const ac = (x, y) =>
  `<circle cx="${x}" cy="${y}" r="36" class="equipment-face"/><path d="M${x - 22} ${y}c8 -28 14 -28 22 0s14 28 22 0" class="symbol"/>`;
const converter = (x, y, inverter = false) =>
  `<g data-component="${inverter ? "inverter" : "rectifier"}"><rect x="${x}" y="${y}" width="112" height="112" rx="5" class="equipment-face inactive"/><path d="M${x + 10} ${y + 102}L${x + 102} ${y + 10}" class="symbol" opacity=".35"/>${text(x + 29, y + 44, inverter ? "⎓" : "~", "diagram-value")}${text(x + 82, y + 88, inverter ? "~" : "⎓", "diagram-value")}</g>`;
const battery = (x, y) =>
  `<g data-component="battery"><rect x="${x}" y="${y}" width="68" height="86" rx="5" class="equipment-face"/>${text(x + 34, y + 35, "+", "diagram-value")}${text(x + 34, y + 72, "−", "diagram-value")}</g>`;
const rack = (x, y, live) =>
  `<g data-component="load"><rect x="${x}" y="${y}" width="78" height="112" rx="5" fill="${live ? "var(--rack-frame, #243e36)" : "var(--inactive-border, #b8beb5)"}"/>${[0, 1, 2].map((i) => `<rect x="${x + 8}" y="${y + 9 + i * 33}" width="62" height="28" rx="2" fill="var(--rack-slot, #edf2e9)"/>`).join("")}</g>`;

export function bypassModel({ mode = "static", sourceAvailable = true } = {}) {
  if (!["static", "maintenance"].includes(mode))
    throw new Error("Unknown bypass mode");
  return {
    mode,
    sourceAvailable,
    loadPowered: sourceAvailable,
    loadKW: sourceAvailable ? 100 : 0,
    upsIsolated: mode === "maintenance",
    batteryCanSupplyLoad: false,
  };
}

export function renderBypassDiagram(options = {}) {
  const model = bypassModel(options),
    compact = Boolean(options.compact),
    maintenance = model.upsIsolated,
    live = model.loadPowered;
  let svg = "";
  if (!compact) {
    svg += `<rect x="240" y="36" width="654" height="400" rx="18" class="ups-enclosure"/>${text(270, 67, maintenance ? "UPS · ISOLATED" : "UPS", "diagram-kicker", "start")}`;
    svg +=
      path("M131 188H180", live, "source-to-branch") +
      path("M180 188H206", false, "utility-input") +
      contact(220, 188, !maintenance, false, "ups-input") +
      path("M234 188H314", false, "rectifier-input");
    svg +=
      path("M426 188H568H710", false, "dc-link") +
      path("M822 188H830", false, "inverter-output") +
      contact(844, 188, false, false, "inverter-unavailable") +
      path("M858 188H926", !maintenance && live, "ups-output") +
      contact(
        940,
        188,
        !maintenance,
        !maintenance && live,
        "ups-output-isolation",
      ) +
      path("M954 188H1026", live, "load-input");
    svg +=
      path("M180 188V86H206", !maintenance && live, "bypass-source") +
      contact(220, 86, !maintenance, !maintenance && live, "bypass-input") +
      path("M234 86H554", !maintenance && live, "static-in") +
      contact(568, 86, !maintenance, !maintenance && live, "static-switch") +
      path("M582 86H866V188", !maintenance && live, "static-out");
    svg += text(568, 62, "Static bypass", "diagram-detail");
    if (maintenance) {
      svg +=
        path("M180 188V-7H554", live, "maintenance-in") +
        contact(568, -7, true, live, "external-maintenance") +
        path("M582 -7H990V188", live, "maintenance-out");
      svg += text(568, -24, "External maintenance bypass", "diagram-detail");
    }
    svg +=
      path("M129 354H206", false, "battery-cabinet") +
      contact(220, 354, !maintenance, false, "battery-disconnect") +
      path("M234 354H383", false, "battery-input") +
      path("M553 354H568V188", false, "battery-interface");
    svg +=
      ac(91, 188) +
      text(91, 120, "Source AC", "diagram-label") +
      text(
        91,
        252,
        live ? "Available" : "Unavailable",
        live ? "ready-label" : "unavailable-label",
      );
    svg +=
      converter(314, 132) +
      text(370, 111, "Rectifier", "diagram-label") +
      converter(710, 132, true) +
      text(766, 111, "Inverter", "diagram-label") +
      text(568, 168, "DC link");
    svg += text(
      766,
      272,
      maintenance ? "Disconnected" : "Unavailable",
      "unavailable-label",
    );
    svg += battery(61, 311) + text(95, 426, "Battery", "diagram-label");
    svg += `<rect x="383" y="327" width="170" height="54" rx="7" class="equipment-face inactive"/>${text(468, 360, "Battery interface")}`;
    svg +=
      rack(1026, 132, live) +
      text(1065, 111, "Load", "diagram-label") +
      text(1065, 288, live ? "100 kW" : "No supply", "diagram-value") +
      text(
        1065,
        316,
        live ? "Powered via bypass" : "100 kW demand",
        live ? "ready-label" : "unavailable-label",
      );
    if (!maintenance)
      svg += text(700, 372, "Battery cannot reach the load", "diagram-detail");
  } else {
    svg += `<rect x="20" y="130" width="306" height="440" rx="16" class="ups-enclosure"/>${text(36, 152, maintenance ? "UPS · ISOLATED" : "UPS", "diagram-kicker", "start")}`;
    svg +=
      ac(105, 45) +
      text(60, 106, "AC source") +
      path("M105 81V95", live, "source-to-branch") +
      path("M105 95V146", false, "utility-input") +
      contact(105, 160, !maintenance, false, "ups-input", 90) +
      path("M105 174V195", false, "rectifier-input");
    svg +=
      converter(49, 195) +
      text(175, 228, "Rectifier", "diagram-detail", "start");
    svg +=
      path("M105 307V370", false, "dc-link") +
      text(68, 344, "DC link", "diagram-kicker");
    svg +=
      converter(49, 370, true) +
      text(175, 416, "Inverter", "diagram-detail", "start") +
      text(
        175,
        442,
        maintenance ? "Disconnected" : "Unavailable",
        "unavailable-label",
        "start",
      );
    svg +=
      path("M105 482V496", false, "inverter-output") +
      contact(105, 510, false, false, "inverter-unavailable", 90) +
      path("M105 524V568", !maintenance && live, "ups-output") +
      contact(
        105,
        582,
        !maintenance,
        !maintenance && live,
        "ups-output-isolation",
        90,
      ) +
      path("M105 596V632", live, "load-input");
    svg +=
      path("M105 95H170V-7H304V146", !maintenance && live, "bypass-source") +
      contact(
        304,
        160,
        !maintenance,
        !maintenance && live,
        "bypass-input",
        90,
      ) +
      path("M304 174V281", !maintenance && live, "static-in") +
      contact(
        304,
        295,
        !maintenance,
        !maintenance && live,
        "static-switch",
        90,
      ) +
      path("M304 309V540H105", !maintenance && live, "static-out");
    svg += text(339, 180, "Static") + text(339, 202, "bypass");
    if (maintenance) {
      svg +=
        path("M105 95H170V-7H380V281", live, "maintenance-in") +
        contact(380, 295, true, live, "external-maintenance", 90) +
        path("M380 309V614H105", live, "maintenance-out");
      svg += `<text x="366" y="436" class="diagram-detail" text-anchor="middle" transform="rotate(-90 366 436)">External bypass</text>`;
    }
    svg += battery(219, 9) + text(254, 117, "Battery");
    svg +=
      path("M253 95V230", false, "battery-cabinet") +
      contact(253, 244, !maintenance, false, "battery-disconnect", 90) +
      path("M253 258V315", false, "battery-input") +
      `<rect x="200" y="315" width="99" height="43" rx="5" class="equipment-face inactive"/>${text(250, 342, "Interface")}` +
      path("M200 337H105", false, "battery-interface");
    svg +=
      rack(66, 632, live) +
      text(176, 657, "Load", "diagram-label", "start") +
      text(176, 693, live ? "100 kW" : "No supply", "diagram-value", "start") +
      text(
        176,
        721,
        live ? "Via bypass" : "100 kW demand",
        live ? "ready-label" : "unavailable-label",
        "start",
      );
  }
  return {
    model,
    viewBox: compact ? "0 -20 410 775" : "0 -45 1200 540",
    svg: `<title id="circuit-title">${maintenance ? "External maintenance bypass; UPS isolated" : "Forced static bypass; inverter unavailable"}. ${live ? "Bypass source supplies the 100 kW load." : "Bypass source lost; no source can supply the load."}</title><desc>Conceptual completed operating state. Contacts depict functional isolation, not a switching procedure or a particular product wiring diagram. Battery backup unavailable in these declared modes.</desc>${svg}`,
  };
}
