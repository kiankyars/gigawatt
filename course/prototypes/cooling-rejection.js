/** Original explanatory schematics; dimensions are illustrative, not construction drawings. */
const esc = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
const label = (x, y, value, size = 17, color = "ink", extra = "") =>
  `<text x="${x}" y="${y}" fill="var(--${color})" style="fill:var(--${color});font-size:${size}px;font-weight:${size >= 17 ? 650 : 450}" ${extra}>${esc(value)}</text>`;
const centered = (x, y, value, size = 17, color = "ink", owner = "") =>
  label(
    x,
    y,
    value,
    size,
    color,
    `text-anchor="middle"${owner ? ` data-label-for="${owner}"` : ""}`,
  );
const rect = (id, x, y, w, h, fill = "panel", extra = "") =>
  `<rect id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="10" fill="var(--${fill})" stroke="var(--line)" stroke-width="1.5" ${extra}/>`;
const path = (d, color = "facility", arrow = false, width = 4, extra = "") =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${arrow ? `marker-end="url(#reject-${color})"` : ""} ${extra}/>`;
const definitions = `<defs>${["facility", "tech", "heat", "muted", "ink"].map((color) => `<marker id="reject-${color}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="3.5" markerHeight="3.5" orient="auto-start-reverse"><path d="M0 1 L9 5 L0 9 Z" fill="var(--${color})"/></marker>`).join("")}</defs>`;
const fan = (x, y, r = 24) =>
  `<g><circle cx="${x}" cy="${y}" r="${r}" fill="var(--paper)" stroke="var(--muted)" stroke-width="1.6"/>${[0, 120, 240].map((a) => `<path d="M${x} ${y} Q${x + r} ${y - r} ${x + r / 3} ${y + 2} Z" fill="var(--muted)" transform="rotate(${a} ${x} ${y})"/>`).join("")}<circle cx="${x}" cy="${y}" r="3" fill="var(--ink)"/></g>`;
const coil = (x, y, w, h, color = "facility") => {
  let d = `M${x} ${y}`;
  for (let i = 0; i < 5; i++)
    d += ` H${i % 2 === 0 ? x + w : x} ${i < 4 ? `V${y + ((i + 1) * h) / 4}` : ""}`;
  return (
    Array.from({ length: 8 }, (_, i) =>
      path(`M${x + (i * w) / 7} ${y - 7} V${y + h + 7}`, "line", false, 1.4),
    ).join("") + path(d, color, false, 4)
  );
};

function rejection(compact) {
  if (compact) return compactRejection();
  const dry =
    rect("dry-panel", 22, 12, 544, 392) +
    centered(294, 47, "Dry cooler", 23, "ink", "dry-panel") +
    rect("dry-coil-case", 248, 102, 162, 212, "face") +
    coil(272, 134, 105, 144) +
    label(74, 102, "Closed liquid loop", 15, "facility") +
    path("M104 159 H272 V134", "facility") +
    path("M148 159 H204", "facility", true) +
    path("M377 278 H442 V339 H104 V269", "facility") +
    path("M255 339 H195", "facility", true) +
    rect("dry-heat-source", 48, 165, 113, 100) +
    centered(104, 207, "Heat", 17, "ink", "dry-heat-source") +
    centered(104, 231, "collected", 15, "ink", "dry-heat-source") +
    path("M104 159 V165", "facility") +
    path("M104 265 V269", "facility") +
    path("M220 204 H272", "muted", true, 3) +
    path("M377 204 H525", "heat", true, 4) +
    fan(449, 204, 23) +
    centered(470, 150, "Air", 16) +
    centered(294, 378, "Water stays inside the coil.", 17, "ink", "dry-panel");
  const wet =
    rect("wet-panel", 590, 12, 548, 392) +
    centered(864, 47, "Wet cooling tower", 23, "ink", "wet-panel") +
    rect("tower-case", 839, 118, 181, 204, "face") +
    label(619, 102, "Tower-water loop", 15, "facility") +
    path("M670 165 H864 V149 H982", "facility") +
    path("M723 165 H783", "facility", true) +
    Array.from({ length: 6 }, (_, i) =>
      path(`M${865 + i * 23} 158 V201`, "facility", true, 1.8),
    ).join("") +
    Array.from({ length: 4 }, (_, i) =>
      path(`M855 ${210 + i * 20} h146`, "line", false, 2),
    ).join("") +
    `<path d="M849 289 H1010 V311 H849 Z" fill="var(--facility)" opacity=".2"/>` +
    path("M850 298 H670 V270", "facility") +
    path("M784 298 H724", "facility", true) +
    rect("tower-load", 614, 173, 112, 96) +
    centered(670, 211, "Heat", 17, "ink", "tower-load") +
    centered(670, 235, "collected", 15, "ink", "tower-load") +
    path("M670 165 V173", "facility") +
    path("M929 144 V83", "heat", true, 4) +
    centered(929, 68, "Heat + water vapor", 13, "heat") +
    path("M1062 237 H1011", "muted", true, 2.5) +
    label(1070, 241, "Air", 13) +
    path("M1064 298 H1021", "facility", true, 3) +
    centered(1074, 276, "Makeup", 13, "facility") +
    path("M999 313 V342 H1081", "facility", true, 2.5) +
    centered(1066, 364, "Blowdown", 12, "facility") +
    centered(
      852,
      378,
      "Most water returns to the loop.",
      17,
      "ink",
      "wet-panel",
    );
  return dry + wet;
}
function compactRejection() {
  const dry =
    rect("dry-panel", 12, 4, 348, 272) +
    label(28, 32, "Dry cooler", 22) +
    rect("dry-coil-case", 160, 64, 108, 158, "face") +
    coil(177, 83, 73, 117) +
    path("M64 92 H177 V83", "facility") +
    path("M84 92 H126", "facility", true, 3) +
    path("M250 200 H284 V230 H64 V198", "facility") +
    path("M142 230 H103", "facility", true, 3) +
    rect("dry-heat-source", 24, 118, 81, 70) +
    centered(64, 148, "Heat", 14, "ink", "dry-heat-source") +
    centered(64, 169, "collected", 13, "ink", "dry-heat-source") +
    path("M64 92 V118", "facility") +
    path("M64 188 V198", "facility") +
    path("M131 148 H176", "muted", true, 2.5) +
    path("M251 148 H338", "heat", true, 3) +
    fan(290, 148, 19) +
    label(278, 104, "Air", 13) +
    centered(186, 257, "No intentional evaporation", 15, "ink", "dry-panel");
  const wet =
    rect("wet-panel", 12, 289, 348, 285) +
    label(28, 318, "Wet cooling tower", 22) +
    rect("tower-case", 163, 365, 135, 137, "face") +
    path("M66 382 H179 V381 H284", "facility") +
    path("M99 382 H138", "facility", true, 3) +
    Array.from({ length: 5 }, (_, i) =>
      path(`M${179 + i * 25} 390 V429`, "facility", true, 1.5),
    ).join("") +
    Array.from({ length: 3 }, (_, i) =>
      path(`M175 ${439 + i * 14} H286`, "line", false, 1.5),
    ).join("") +
    `<path d="M170 481 H291 V495 H170 Z" fill="var(--facility)" opacity=".2"/>` +
    path("M174 490 H65 V478", "facility") +
    path("M132 490 H102", "facility", true, 3) +
    rect("tower-load", 24, 410, 83, 67) +
    centered(65, 438, "Heat", 14, "ink", "tower-load") +
    centered(65, 458, "collected", 13, "ink", "tower-load") +
    path("M65 382 V410", "facility") +
    path("M233 375 V350", "heat", true, 3) +
    centered(228, 342, "Heat + water vapor", 12, "heat") +
    path("M342 433 H298", "muted", true, 2.3) +
    label(330, 417, "Air", 12) +
    path("M338 490 H299", "facility", true, 2.5) +
    centered(321, 470, "Makeup", 11, "facility") +
    path("M278 500 V520 H327", "facility", true, 2) +
    centered(280, 539, "Blowdown", 11, "facility") +
    label(27, 565, "Most water recirculates.", 15);
  return dry + wet;
}

function thermometer(x, y, reading, wet, compact) {
  const h = compact ? 172 : 202;
  const t = compact ? 5 : 6;
  const liquidY = y + h - 28 - (reading - 15) * t;
  const bulbY = y + h - 13;
  return (
    `<rect x="${x - 12}" y="${y}" width="24" height="${h - 15}" rx="12" fill="var(--paper)" stroke="var(--ink)" stroke-width="2"/>` +
    `<circle cx="${x}" cy="${bulbY}" r="23" fill="var(--paper)" stroke="var(--ink)" stroke-width="2"/>` +
    path(`M${x} ${liquidY} V${bulbY}`, wet ? "tech" : "heat", false, 9) +
    `<circle cx="${x}" cy="${bulbY}" r="14" fill="var(--${wet ? "tech" : "heat"})"/>` +
    Array.from({ length: 5 }, (_, i) =>
      path(`M${x + 17} ${y + 19 + i * 27} h10`, "muted", false, 1.4),
    ).join("") +
    (wet
      ? `<path d="M${x - 26} ${bulbY - 13} Q${x - 36} ${bulbY + 33} ${x + 24} ${bulbY + 27} V${bulbY - 14}" fill="none" stroke="var(--tech)" stroke-width="2" stroke-dasharray="3 3"/>`
      : "") +
    path(`M${x - 73} ${y + 80} H${x - 29}`, "muted", true, 2) +
    path(`M${x + 38} ${y + 80} H${x + 81}`, "muted", true, 2)
  );
}
function weather(compact, state) {
  const wb = state.humidity === "humid" ? 28 : 22;
  if (compact)
    return (
      rect("weather-panel", 12, 6, 348, 467) +
      centered(101, 39, "Dry bulb", 21) +
      centered(272, 39, "Wet bulb", 21) +
      thermometer(100, 80, 35, false, true) +
      thermometer(267, 80, wb, true, true) +
      centered(100, 301, "35°C", 35, "heat") +
      centered(267, 301, `${wb}°C`, 35, "tech") +
      centered(100, 330, "Dry sensor", 14) +
      centered(267, 330, "Wetted wick", 14) +
      centered(
        186,
        371,
        "Both shaded and ventilated",
        14,
        "muted",
        "weather-panel",
      ) +
      path("M65 399 H308", "line", false, 1.3) +
      centered(
        186,
        434,
        `Dry − wet bulb = ${35 - wb} K`,
        21,
        "ink",
        "weather-panel",
      ) +
      centered(186, 502, "Higher humidity → less evaporation", 15) +
      centered(186, 528, "At saturation: wet bulb = dry bulb", 13, "muted")
    );
  return (
    rect("weather-panel", 32, 15, 1096, 386) +
    centered(251, 56, "Dry-bulb temperature", 24) +
    centered(775, 56, "Wet-bulb temperature", 24) +
    thermometer(184, 104, 35, false, false) +
    thermometer(690, 104, wb, true, false) +
    label(280, 198, "35°C", 48, "heat") +
    label(280, 231, "Dry sensor", 17) +
    label(794, 198, `${wb}°C`, 48, "tech") +
    label(794, 231, "Wetted wick", 17) +
    label(794, 258, "Evaporation cools the sensor.", 14, "muted") +
    centered(263, 356, "Shaded · ventilated", 14, "muted") +
    centered(780, 356, "Shaded · ventilated", 14, "muted") +
    path("M549 76 V318", "line", false, 1.5) +
    centered(
      580,
      386,
      `Dry − wet bulb = ${35 - wb} K  ·  At saturation, the two readings meet.`,
      17,
      "ink",
      "weather-panel",
    )
  );
}

function temperatureNode(
  id,
  x,
  y,
  w,
  value,
  lines,
  color = "ink",
  compact = false,
) {
  const h = compact ? 103 : 120;
  return (
    rect(id, x, y, w, h, "paper") +
    centered(
      x + w / 2,
      y + (compact ? 35 : 45),
      `${value}°C`,
      compact ? 25 : 34,
      color,
      id,
    ) +
    lines
      .map((line, i) =>
        centered(
          x + w / 2,
          y + (compact ? 64 : 79) + i * 19,
          line,
          compact ? 12 : 14,
          "muted",
          id,
        ),
      )
      .join("")
  );
}
function gap(x1, x2, y, name, kelvin, compact) {
  return (
    path(`M${x1} ${y} H${x2}`, "muted", true, compact ? 2.5 : 3) +
    centered((x1 + x2) / 2, y - 16, `+${kelvin} K`, compact ? 12 : 17, "heat") +
    (compact
      ? ""
      : name === "Separator"
        ? centered((x1 + x2) / 2, y + 22, "Heat", 12) +
          centered((x1 + x2) / 2, y + 38, "exchanger", 12)
        : centered((x1 + x2) / 2, y + 27, name, 13))
  );
}
function approach(compact, state) {
  const wb = state.humidity === "humid" ? 28 : 22;
  const wet = wb + 13;
  if (compact) {
    const dryY = 61,
      wetY = 279;
    return (
      label(20, 25, "84 kW · stipulated approaches", 13, "muted") +
      label(20, 50, "Dry route", 18) +
      temperatureNode(
        "dry-air",
        15,
        dryY,
        89,
        35,
        ["Dry bulb"],
        "muted",
        true,
      ) +
      temperatureNode(
        "dry-facility",
        142,
        dryY,
        89,
        40,
        ["Facility", "supply"],
        "facility",
        true,
      ) +
      temperatureNode(
        "dry-technology",
        269,
        dryY,
        89,
        45,
        ["Technology", "supply"],
        "fault",
        true,
      ) +
      gap(107, 138, dryY + 62, "", 5, true) +
      gap(234, 265, dryY + 62, "", 5, true) +
      centered(123, 186, "Dry cooler", 12) +
      centered(250, 186, "CDU", 12) +
      label(20, 227, "Wet route · separate tower loop", 17) +
      temperatureNode(
        "wet-air",
        15,
        wetY,
        73,
        wb,
        ["Wet bulb"],
        "muted",
        true,
      ) +
      temperatureNode(
        "wet-tower",
        107,
        wetY,
        73,
        wb + 3,
        ["Tower", "water"],
        "facility",
        true,
      ) +
      temperatureNode(
        "wet-facility",
        199,
        wetY,
        73,
        wb + 8,
        ["Facility", "supply"],
        "facility",
        true,
      ) +
      temperatureNode(
        "wet-technology",
        291,
        wetY,
        73,
        wet,
        ["Technology", "supply"],
        wet <= 35 ? "facility" : "fault",
        true,
      ) +
      gap(89, 103, wetY + 64, "", 3, true) +
      gap(181, 195, wetY + 64, "", 5, true) +
      gap(273, 287, wetY + 64, "", 5, true) +
      centered(97, 258, "Tower", 11) +
      centered(189, 251, "Heat", 11) +
      centered(189, 265, "exchanger", 11) +
      centered(281, 258, "CDU", 11) +
      rect("approach-limit", 17, 421, 338, 90) +
      centered(
        186,
        450,
        "Required technology supply ≤35°C",
        16,
        "ink",
        "approach-limit",
      ) +
      centered(
        186,
        483,
        wet <= 35
          ? "Dry fails · wet meets the limit"
          : "Both routes fail the temperature limit",
        16,
        wet <= 35 ? "facility" : "fault",
        "approach-limit",
      ) +
      centered(
        186,
        545,
        "The wet route here keeps tower water separate.",
        13,
        "muted",
      )
    );
  }
  const dryY = 47,
    wetY = 219;
  return (
    label(
      24,
      25,
      "84 kW example · fixed approaches are teaching inputs",
      13,
      "muted",
    ) +
    label(24, 82, "Dry", 22) +
    temperatureNode("dry-air", 114, dryY, 168, 35, ["Outdoor", "dry bulb"]) +
    temperatureNode(
      "dry-facility",
      428,
      dryY,
      168,
      40,
      ["Facility", "supply"],
      "facility",
    ) +
    temperatureNode(
      "dry-technology",
      742,
      dryY,
      168,
      45,
      ["Technology", "supply"],
      "fault",
    ) +
    gap(289, 419, dryY + 58, "Dry cooler", 5, false) +
    gap(603, 733, dryY + 58, "CDU", 5, false) +
    label(956, 107, "45°C > 35°C", 24, "fault") +
    label(956, 136, "Fails the limit", 14, "fault") +
    label(24, 252, "Wet", 22) +
    temperatureNode("wet-air", 114, wetY, 150, wb, ["Outdoor", "wet bulb"]) +
    temperatureNode(
      "wet-tower",
      334,
      wetY,
      150,
      wb + 3,
      ["Tower", "outlet water"],
      "facility",
    ) +
    temperatureNode(
      "wet-facility",
      554,
      wetY,
      150,
      wb + 8,
      ["Facility", "supply"],
      "facility",
    ) +
    temperatureNode(
      "wet-technology",
      774,
      wetY,
      150,
      wet,
      ["Technology", "supply"],
      wet <= 35 ? "facility" : "fault",
    ) +
    gap(271, 325, wetY + 58, "Tower", 3, false) +
    gap(491, 545, wetY + 58, "Separator", 5, false) +
    gap(711, 765, wetY + 58, "CDU", 5, false) +
    label(
      956,
      279,
      `${wet}°C ${wet <= 35 ? "≤" : ">"} 35°C`,
      24,
      wet <= 35 ? "facility" : "fault",
    ) +
    label(
      956,
      308,
      wet <= 35 ? "Meets the limit" : "Fails the limit",
      14,
      wet <= 35 ? "facility" : "fault",
    ) +
    centered(
      581,
      390,
      "The wet route here includes a separate tower-to-facility heat exchanger.",
      17,
    )
  );
}

function adiabatic(compact) {
  if (compact)
    return (
      rect("pad-case", 52, 100, 268, 105, "face") +
      centered(186, 143, "Wetted pad", 21, "tech", "pad-case") +
      centered(186, 171, "Some feed water evaporates", 14, "ink", "pad-case") +
      label(28, 30, "Outdoor air", 19) +
      path("M185 42 V92", "muted", true, 3) +
      path("M349 152 H324", "tech", true, 3) +
      label(272, 86, "Water feed", 12, "tech") +
      path("M185 211 V269", "muted", true, 3) +
      label(205, 243, "Cooler, wetter air", 13) +
      rect("adiabatic-coil-case", 69, 280, 234, 153, "face") +
      coil(95, 308, 181, 91) +
      path("M30 308 H95", "facility", true, 3) +
      path("M276 399 H337", "facility", true, 3) +
      label(27, 462, "Closed liquid", 14, "facility") +
      label(27, 484, "circuit", 14, "facility") +
      path("M185 435 V513", "heat", true, 3) +
      label(205, 515, "Warm air", 14, "heat")
    );
  return (
    label(35, 85, "Outdoor air", 19) +
    path("M41 193 H234", "muted", true, 4) +
    rect("pad-case", 243, 104, 186, 200, "face") +
    Array.from({ length: 7 }, (_, i) =>
      path(`M${260 + i * 25} 125 V281`, "tech", false, 1.6),
    ).join("") +
    centered(336, 78, "Wetted pad", 21) +
    path("M190 127 H236", "tech", true, 3) +
    label(95, 131, "Water feed", 14, "tech") +
    path("M436 194 H607", "muted", true, 4) +
    centered(522, 163, "Cooler, wetter air", 15) +
    rect("adiabatic-coil-case", 616, 104, 236, 200, "face") +
    coil(651, 131, 167, 145) +
    centered(734, 78, "Dry coil", 21) +
    path("M573 131 H651", "facility", true, 3) +
    path("M818 276 H889", "facility", true, 3) +
    label(617, 348, "Process liquid stays inside the coil.", 17, "facility") +
    path("M856 194 H1115", "heat", true, 4) +
    fan(979, 194, 30) +
    label(988, 151, "Warm air", 17, "heat") +
    centered(336, 342, "Some feed water evaporates.", 16)
  );
}
function chiller(compact, water) {
  const sink = water ? "Condenser water" : "Outdoor air";
  if (compact)
    return (
      label(20, 26, water ? "Water-cooled chiller" : "Air-cooled chiller", 23) +
      rect("chiller-boundary", 17, 115, 338, 289, "panel") +
      rect("chiller-evaporator", 41, 137, 290, 80, "face") +
      centered(186, 170, "Evaporator", 20, "ink", "chiller-evaporator") +
      centered(
        186,
        196,
        "Chilled-water circuit",
        14,
        "tech",
        "chiller-evaporator",
      ) +
      path("M186 68 V130", "heat", true, 3) +
      centered(186, 52, "100 kW collected heat", 17, "heat") +
      path("M186 224 V298", "heat", true, 4) +
      label(213, 251, "Refrigerant", 13) +
      path("M25 268 H177", "ink", true, 3) +
      label(29, 226, "Compressor", 13) +
      label(29, 248, "20 kW work", 13) +
      rect("chiller-condenser", 41, 305, 290, 76, "face") +
      centered(186, 338, "Condenser", 20, "ink", "chiller-condenser") +
      centered(
        186,
        363,
        sink,
        14,
        water ? "facility" : "muted",
        "chiller-condenser",
      ) +
      path("M186 386 V445", "heat", true, 4) +
      centered(186, 472, "120 kW rejected", 25, "heat") +
      centered(
        186,
        506,
        water ? "Water circuit → cooling tower" : "Fins + fans → outdoor air",
        17,
      ) +
      centered(
        186,
        551,
        "Synthetic steady heat balance; auxiliaries omitted",
        11,
        "muted",
      )
    );
  return (
    rect("chiller-boundary", 256, 78, 598, 267, "panel") +
    label(
      278,
      108,
      water ? "WATER-COOLED CHILLER" : "AIR-COOLED CHILLER",
      15,
      "muted",
    ) +
    rect("chiller-evaporator", 284, 167, 216, 119, "face") +
    centered(392, 210, "Evaporator", 23, "ink", "chiller-evaporator") +
    centered(
      392,
      242,
      "Chilled-water circuit",
      15,
      "tech",
      "chiller-evaporator",
    ) +
    rect("chiller-condenser", 612, 167, 214, 119, "face") +
    centered(719, 210, "Condenser", 23, "ink", "chiller-condenser") +
    centered(
      719,
      242,
      sink,
      15,
      water ? "facility" : "muted",
      "chiller-condenser",
    ) +
    path("M46 226 H276", "heat", true, 4) +
    label(42, 168, "100 kW", 30, "heat") +
    label(42, 193, "Collected heat", 15) +
    path("M507 228 H604", "heat", true, 4) +
    centered(555, 277, "Refrigerant", 14) +
    path("M555 92 V218", "ink", true, 3) +
    centered(554, 43, "20 kW compressor work", 18) +
    path("M831 226 H1099", "heat", true, 4) +
    label(888, 169, "120 kW", 30, "heat") +
    label(888, 194, "Rejected heat", 15) +
    label(879, 283, water ? "Water circuit → tower" : "Fins + fans → air", 17) +
    centered(
      580,
      388,
      "Hypothetical steady state · other auxiliaries excluded",
      13,
      "muted",
    )
  );
}
function economizer(compact) {
  if (compact)
    return (
      rect("economizer-load", 27, 20, 160, 112) +
      centered(107, 52, "Facility heat", 20, "ink", "economizer-load") +
      centered(107, 78, "Closed water loop", 13, "ink", "economizer-load") +
      rect("economizer-hx", 185, 205, 160, 135, "face") +
      centered(264, 174, "Economizer", 20) +
      centered(264, 196, "exchanger", 16) +
      `<rect x="208" y="222" width="28" height="95" rx="5" fill="var(--tech)" opacity=".12"/><rect x="278" y="222" width="28" height="95" rx="5" fill="var(--facility)" opacity=".12"/>` +
      rect("economizer-cooler", 27, 411, 160, 103, "face") +
      centered(107, 440, "Outdoor cooler", 17, "ink", "economizer-cooler") +
      centered(
        107,
        463,
        "Cool-enough weather",
        12,
        "ink",
        "economizer-cooler",
      ) +
      path("M142 100 H172 V230 H222 V300 H142 V100", "tech") +
      path("M172 153 V191", "tech", true, 3) +
      path("M291 230 H329 V499 H142 V475 H291 V230", "facility") +
      path("M329 364 V399", "facility", true, 3) +
      path("M236 263 H278", "heat", true, 3) +
      path("M98 106 H132", "heat", true, 3) +
      path("M139 487 H79", "heat", true, 3) +
      label(27, 258, "Compressor", 14, "muted") +
      label(27, 283, "off", 23, "muted") +
      centered(186, 552, "Pumps and fans still consume electricity.", 14)
    );
  return (
    rect("economizer-load", 32, 118, 211, 173) +
    centered(137, 160, "Facility heat", 23, "ink", "economizer-load") +
    rect("economizer-hx", 450, 97, 259, 213, "face") +
    centered(579, 132, "Economizer exchanger", 20, "ink", "economizer-hx") +
    `<rect x="505" y="154" width="48" height="143" rx="7" fill="var(--tech)" opacity=".12"/><rect x="607" y="154" width="48" height="143" rx="7" fill="var(--facility)" opacity=".12"/>` +
    rect("economizer-cooler", 910, 109, 215, 211, "face") +
    centered(1017, 88, "Outdoor cooler", 22) +
    path("M191 265 V185 H529 V265 H191", "tech") +
    path("M292 185 H351", "tech", true, 3) +
    path("M358 265 H300", "tech", true, 3) +
    path("M631 185 H900 V169 H952", "facility") +
    path("M756 185 H817", "facility", true, 3) +
    coil(952, 169, 50, 102) +
    path("M1002 271 H1020 V290 H631 V185", "facility") +
    path("M817 290 H756", "facility", true, 3) +
    path("M553 207 H607", "heat", true, 3) +
    path("M553 250 H607", "heat", true, 3) +
    path("M105 225 H182", "heat", true, 3) +
    fan(1072, 219, 25) +
    path("M1004 218 H1120", "heat", true, 3) +
    centered(137, 316, "Closed water loop", 14, "tech") +
    centered(1017, 344, "Cool-enough weather", 14) +
    label(688, 385, "Pumps and fans still consume electricity.", 17)
  );
}

/**
 * State contract:
 * weather / approach-outdoors: humidity='dry'|'humid' (35°C dry bulb, 22/28°C wet bulb).
 * plant-options: plant='adiabatic'|'air-chiller'|'water-chiller'|'economizer'.
 */
export function renderRejection(kind, compact, state = {}) {
  let drawing;
  if (kind === "rejection") drawing = rejection(compact);
  else if (kind === "weather") drawing = weather(compact, state);
  else if (kind === "approach-outdoors") drawing = approach(compact, state);
  else if (kind === "plant-options") {
    if (state.plant === "air-chiller") drawing = chiller(compact, false);
    else if (state.plant === "water-chiller") drawing = chiller(compact, true);
    else if (state.plant === "economizer") drawing = economizer(compact);
    else drawing = adiabatic(compact);
  } else throw new RangeError(`Unknown rejection scene: ${kind}`);
  return definitions + drawing;
}
