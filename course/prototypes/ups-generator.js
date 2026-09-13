const text = (x, y, value, cls = "diagram-detail") =>
  `<text x="${x}" y="${y}" text-anchor="middle" class="${cls}">${value}</text>`;
const wire = (d, active, id) =>
  `<path d="${d}" class="wire ${active ? "active" : ""}" data-path="${id}"/>`;
const contact = (d, active, id) =>
  `<path d="${d}" class="wire ${active ? "active" : ""}" data-contact="${id}" data-closed="${active}"/>`;
const dot = (x, y) => `<circle cx="${x}" cy="${y}" r="5" class="connection"/>`;
const box = (x, y, w, h, active = true) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="7" class="equipment-face ${active ? "" : "inactive"}"/>`;
const source = (x, y, title, active, radius) =>
  `<circle cx="${x}" cy="${y}" r="${radius}" class="equipment-face ${active ? "" : "inactive"}"/><path d="M${x - 17} ${y}c6 -22 11 -22 17 0s11 22 17 0" class="symbol"/>${text(x, y - radius - 14, title, "generator-label")}`;

export function generatorModel(stage = "waiting") {
  if (!["utility", "waiting", "generator", "recharge"].includes(stage))
    throw new Error("Unknown generator stage");
  return {
    stage,
    utilityConnected: stage === "utility",
    generatorConnected: stage === "generator" || stage === "recharge",
    batterySupplying: stage === "waiting",
    batteryCharging: stage === "recharge",
    rectifierPowered: stage !== "waiting",
    loadKW: 100,
  };
}

export function renderGeneratorDiagram({
  stage = "waiting",
  compact = false,
} = {}) {
  const m = generatorModel(stage);
  const u = m.utilityConnected,
    g = m.generatorConnected,
    b = m.batterySupplying,
    c = m.batteryCharging;
  const generatorStatus = g
    ? "Accepted AC source"
    : stage === "waiting"
      ? "Starting · disconnected"
      : "Standby";
  const title = u
    ? "Utility power feeds the source transfer switchgear, rectifier, DC link, inverter and 100 kW load. Generator is disconnected."
    : b
      ? "Utility has failed and the generator is starting, disconnected. Both source contacts are open. The UPS battery feeds the DC link and inverter to maintain 100 kW."
      : c
        ? "Utility remains unavailable. Generator power feeds the rectifier, DC link and inverter for the 100 kW load, and the battery converter recharges the battery. Source demand includes load, recharge and UPS losses. Charging is enabled in this configuration."
        : "Utility remains unavailable. Accepted generator power feeds the source transfer switchgear, rectifier, DC link, inverter and 100 kW load. Battery charging is disabled in this configuration.";
  let svg;
  if (!compact) {
    svg = `<rect x="400" y="90" width="510" height="260" rx="18" class="ups-enclosure"/>${text(655, 118, "UPS · DOUBLE CONVERSION", "diagram-kicker")}`;
    svg +=
      box(215, 177, 160, 110) +
      text(295, 158, "Source transfer", "generator-label");
    svg +=
      wire("M126 116H185V212H245", u, "utility-input") +
      wire("M126 330H185V252H245", g, "generator-input");
    svg +=
      contact(u ? "M245 212L300 232" : "M245 212L280 194", u, "utility") +
      contact(g ? "M245 252L300 232" : "M245 252L280 274", g, "generator");
    svg +=
      wire("M300 232H445", !b, "transfer-to-rectifier") +
      wire("M555 232H630", !b, "rectifier-output") +
      wire("M630 232H745", true, "dc-link") +
      wire("M855 232H1015", true, "inverter-output");
    svg += wire("M520 397H630V232", b || c, c ? "dc-link-to-battery" : "battery-to-dc-link") + dot(630, 232);
    svg += box(568, 265, 124, 72, b || c) + text(630, 294, "Battery", "generator-small") + text(630, 320, "DC/DC", "generator-label");
    if (b || c) svg += `<path d="${c ? "M624 350l6 10 6 -10" : "M624 360l6 -10 6 10"}" class="symbol"/><path d="${c ? "M543 391l-10 6 10 6" : "M533 391l10 6 -10 6"}" class="symbol"/>`;
    svg +=
      source(90, 116, "Utility", u, 36) +
      text(90, 171, u ? "Supplying" : "Unavailable", "generator-small");
    svg +=
      source(90, 330, "Generator", g, 36) +
      text(104, 388, generatorStatus, "generator-small");
    svg +=
      box(445, 177, 110, 110, !b) +
      text(500, 158, "Rectifier", "generator-label") +
      text(500, 239, "AC → DC", "generator-label");
    svg += text(650, 204, "DC link", "generator-label");
    svg +=
      box(745, 177, 110, 110) +
      text(800, 158, "Inverter", "generator-label") +
      text(800, 239, "DC → AC", "generator-label");
    svg +=
      box(420, 365, 100, 65, b || c) +
      text(470, 405, "+  −", "diagram-label") +
      text(470, 454, "UPS battery", "generator-label") +
      text(800, 391, b ? "Discharging" : c ? "Charging" : "Ready", "generator-small");
    svg +=
      box(1015, 177, 110, 110) +
      text(1070, 217, "Racks", "generator-label") +
      text(1070, 251, "100 kW", "diagram-label");
  } else {
    svg = `<rect x="88" y="263" width="248" height="259" rx="14" class="ups-enclosure"/>${text(290, 286, "UPS", "diagram-kicker")}`;
    svg +=
      box(125, 146, 140, 88) +
      text(195, 132, "Source transfer", "generator-label");
    svg +=
      wire("M72 86V169H147", u, "utility-input") +
      wire("M303 86V210H243", g, "generator-input");
    svg +=
      contact(u ? "M147 169L195 196" : "M147 169L167 153", u, "utility") +
      contact(g ? "M243 210L195 196" : "M243 210L222 225", g, "generator");
    svg +=
      wire("M195 196V295", !b, "transfer-to-rectifier") +
      wire("M195 355V394", !b, "rectifier-output") +
      wire("M195 394V435", true, "dc-link") +
      wire("M195 495V558", true, "inverter-output");
    svg += wire("M77 371H112V394H195", b || c, c ? "dc-link-to-battery" : "battery-to-dc-link") + dot(195, 394);
    svg += box(93, 353, 65, 62, b || c) + text(125, 390, "DC/DC", "generator-small");
    if (b || c) svg += `<path d="${c ? "M177 388l-8 6 8 6" : "M169 388l8 6 -8 6"}" class="symbol"/>`;
    svg += source(72, 60, "Utility", u, 26);
    svg += source(303, 60, "Generator", g, 26);
    svg +=
      box(155, 295, 80, 60, !b) +
      text(195, 318, "Rectifier", "generator-small") +
      text(195, 343, "AC → DC", "generator-label");
    svg += text(245, 402, "DC link", "generator-small");
    svg +=
      box(155, 435, 80, 60) +
      text(195, 458, "Inverter", "generator-small") +
      text(195, 483, "DC → AC", "generator-label");
    svg +=
      box(7, 341, 70, 60, b || c) +
      text(42, 378, "+  −", "generator-label") +
      text(47, 440, "UPS battery", "generator-small") +
      text(47, 463, b ? "Discharging" : c ? "Charging" : "Ready", "generator-small");
    svg +=
      box(150, 558, 90, 62) +
      text(195, 582, "Racks", "generator-label") +
      text(195, 608, "100 kW", "generator-label");
  }
  return {
    viewBox: compact ? "0 0 380 635" : "0 0 1160 475",
    svg: `<title>${title}</title><g data-generator-stage="${stage}">${svg}</g>`,
    model: m,
  };
}
