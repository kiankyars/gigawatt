import {
  heatTransportComparison,
  liquidHeatBalance,
  COOLING_EXAMPLE,
} from "./cooling-model.js?v=20260911-cooling2";
const text = (x, y, value, cls = "svg-label", owner = "", anchor = "start") =>
  `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}"${owner ? ` data-label-for="foundation-${owner}"` : ""}>${value}</text>`;
const box = (id, x, y, w, h, cls = "panel") =>
  `<rect id="foundation-${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="10" class="${cls}"/>`;
const path = (d, type = "tech", arrow = false) =>
  `<path d="${d}" class="${type === "air" ? "outline" : type}"${type === "air" ? ' style="stroke:var(--muted);stroke-width:5;stroke-linecap:round;stroke-linejoin:round"' : ""}${arrow ? ` marker-end="url(#${type === "air" ? "foundation-air" : type}-arrow)"` : ""}/>`;
const airMarker = `<defs><marker id="foundation-air-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path d="M0 1 L9 5 L0 9Z" fill="var(--muted)"/></marker></defs>`;

function rack(x, y, w, h) {
  return (
    box("rack", x, y, w, h) +
    [0, 1, 2, 3]
      .map(
        (i) =>
          `<rect x="${x + 14}" y="${y + 37 + (i * (h - 55)) / 4}" width="${w - 28}" height="${(h - 73) / 4}" rx="3" class="face"/>`,
      )
      .join("") +
    text(x + w / 2, y + 25, "Rack", "svg-label", "rack", "middle")
  );
}

function whyLiquid(compact) {
  const m = heatTransportComparison();
  const panel = (air, x, y, w, h) => {
    const id = air ? "air" : "water",
      center = x + w / 2;
    const value = air
      ? Math.round(m.airLitresPerSecond).toLocaleString("en-US")
      : m.waterLitresPerSecond.toFixed(2);
    return (
      box(id, x, y, w, h) +
      text(x + 18, y + 28, air ? "AIR" : "WATER", "svg-tiny", id) +
      text(center, y + 77, `${value} L/s`, "svg-number", id, "middle") +
      text(
        center,
        y + 109,
        air ? "ρ = 1.2 kg/m³" : "ρ = 1,000 kg/m³",
        "svg-small",
        id,
        "middle",
      ) +
      text(
        center,
        y + 130,
        air ? "cₚ = 1.005 kJ/(kg·K)" : "cₚ = 4.18 kJ/(kg·K)",
        "svg-small",
        id,
        "middle",
      )
    );
  };
  if (compact)
    return (
      text(186, 25, "SAME 100 kW · SAME 10 K RISE", "svg-tiny", "", "middle") +
      panel(true, 15, 75, 342, 170) +
      panel(false, 15, 271, 342, 170) +
      text(186, 510, "Q̇ = ṁ cₚ ΔT = ρ V̇ cₚ ΔT", "svg-equation", "", "middle")
    );
  return (
    text(580, 29, "SAME 100 kW · SAME 10 K RISE", "svg-tiny", "", "middle") +
    panel(true, 80, 62, 475, 200) +
    panel(false, 605, 62, 475, 200) +
    text(580, 332, "Q̇ = ṁ cₚ ΔT = ρ V̇ cₚ ΔT", "svg-number", "", "middle")
  );
}

function waterBalance(compact, state) {
  const flowKgS = state.flow === 5 ? 5 : 2.5;
  const m = liquidHeatBalance({ heatKw: COOLING_EXAMPLE.heatKw, flowKgS });
  const inletC = 35;
  const outletC = inletC + m.deltaTK;
  const temperature = (x, y, value, label, compact) =>
    text(x, y - (compact ? 26 : 37), label, "svg-small", "", "middle") +
    text(
      x,
      y,
      `${value.toFixed(2)}°C`,
      compact ? "svg-label" : "svg-equation",
      "",
      "middle",
    );
  const output = compact
    ? text(
        186,
        25,
        "SELECTED LIQUID PATH · STEADY STATE",
        "svg-tiny",
        "",
        "middle",
      ) +
      text(186, 73, "100 kW", "svg-number heat-text", "", "middle") +
      path("M186 83 V113", "heat", true) +
      box("pickup", 108, 118, 156, 104) +
      text(186, 147, "Heat pickup", "svg-label", "pickup", "middle") +
      path("M16 187 H356", "tech") +
      path("M51 187 H101", "tech", true) +
      path("M274 187 H348", "tech", true) +
      temperature(51, 162, inletC, "Inlet", true) +
      temperature(319, 162, outletC, "Outlet", true) +
      text(186, 280, `${flowKgS} kg/s`, "svg-number tech-text", "", "middle") +
      text(
        186,
        329,
        `ΔT = ${m.deltaTK.toFixed(2)} K`,
        "svg-number heat-text",
        "",
        "middle",
      ) +
      text(
        186,
        381,
        "Steady-flow sensible-heat balance",
        "svg-label",
        "",
        "middle",
      ) +
      text(186, 418, "Q̇ = ṁ cₚ ΔT", "svg-equation", "", "middle") +
      text(
        186,
        449,
        `100 ÷ (${flowKgS} × 4.18) ≈ ${m.deltaTK.toFixed(2)} K`,
        "svg-label",
        "",
        "middle",
      ) +
      text(24, 488, "Q̇ heat rate · ṁ mass flow", "svg-small") +
      text(24, 511, "cₚ specific heat · ΔT coolant rise", "svg-small") +
      text(
        186,
        552,
        "Water cₚ = 4.18 kJ/(kg·K) · inlet fixed at 35°C",
        "svg-small",
        "",
        "middle",
      )
    : text(
        334,
        29,
        "SELECTED LIQUID PATH · STEADY STATE",
        "svg-tiny",
        "",
        "middle",
      ) +
      text(334, 88, "100 kW", "svg-number heat-text", "", "middle") +
      path("M334 99 V133", "heat", true) +
      box("pickup", 232, 138, 204, 108) +
      text(334, 168, "Heat pickup", "svg-label", "pickup", "middle") +
      path("M59 213 H608", "tech") +
      path("M152 213 H224", "tech", true) +
      path("M446 213 H583", "tech", true) +
      temperature(131, 181, inletC, "Inlet", false) +
      temperature(540, 181, outletC, "Outlet", false) +
      text(
        334,
        306,
        `${flowKgS} kg/s water`,
        "svg-number tech-text",
        "",
        "middle",
      ) +
      text(
        334,
        359,
        `ΔT = ${m.deltaTK.toFixed(2)} K`,
        "svg-number heat-text",
        "",
        "middle",
      ) +
      text(
        334,
        397,
        "Inlet held at 35°C · coolant temperature, not chip temperature",
        "svg-small",
        "",
        "middle",
      ) +
      text(
        869,
        94,
        "Steady-flow sensible-heat balance",
        "svg-label",
        "",
        "middle",
      ) +
      text(869, 151, "Q̇ = ṁ cₚ ΔT", "svg-number", "", "middle") +
      text(
        869,
        200,
        `100 ÷ (${flowKgS} × 4.18) ≈ ${m.deltaTK.toFixed(2)} K`,
        "svg-label",
        "",
        "middle",
      ) +
      text(701, 273, "Q̇ heat rate · ṁ mass flow", "svg-label") +
      text(701, 308, "cₚ specific heat · ΔT coolant rise", "svg-label") +
      text(701, 359, "Water cₚ = 4.18 kJ/(kg·K)", "svg-label");
  return `<g data-flow-kg-s="${flowKgS}" data-inlet-c="${inletC}" data-outlet-c="${outletC}" data-rise-k="${m.deltaTK}" data-heat-kw="${m.heatKw}">${output}</g>`;
}

function airCapture(compact) {
  if (compact) {
    return (
      rack(28, 35, 127, 151) +
      box("crah", 192, 281, 151, 172) +
      text(267, 310, "CRAH", "svg-label", "crah", "middle") +
      text(267, 335, "Computer room", "svg-small", "crah", "middle") +
      text(267, 354, "air handler", "svg-small", "crah", "middle") +
      path("M154 98 H363 V380 H274 V411 H85 V187", "air") +
      path("M188 98 H247", "air", true) +
      path("M85 254 V188", "air", true) +
      text(243, 215, "Warm air", "svg-small") +
      text(31, 276, "Cool air", "svg-small") +
      path("M351 380 H245 V410 H351", "facility") +
      path("M341 380 H309", "facility", true) +
      path("M311 410 H350", "facility", true) +
      path("M273 372 V394", "heat", true) +
      text(192, 486, "Chilled water", "svg-label facility-text") +
      text(
        186,
        551,
        "Chip → heat sink → air → CRAH coil",
        "svg-small",
        "",
        "middle",
      )
    );
  }
  return (
    rack(95, 104, 166, 229) +
    box("crah", 682, 87, 280, 262) +
    text(822, 122, "CRAH", "svg-label", "crah", "middle") +
    text(822, 150, "Computer room air handler", "svg-small", "crah", "middle") +
    path("M262 175 H745 V300 H262", "air") +
    path("M393 175 H474", "air", true) +
    path("M474 300 H393", "air", true) +
    text(400, 151, "Warm air", "svg-label") +
    text(405, 328, "Cool air", "svg-label") +
    path("M1100 230 H782 V281 H1100", "facility") +
    path("M1065 230 H994", "facility", true) +
    path("M992 281 H1070", "facility", true) +
    path("M747 252 H809", "heat", true) +
    text(984, 328, "Chilled water", "svg-label facility-text") +
    text(94, 386, "Chip → heat sink → circulating room air", "svg-small")
  );
}

function coldplateCapture(compact) {
  if (compact) {
    return (
      rack(28, 38, 142, 165) +
      box("cdu", 177, 291, 175, 189) +
      text(264, 321, "CDU", "svg-label", "cdu", "middle") +
      text(264, 344, "Coolant distribution", "svg-small", "cdu", "middle") +
      text(264, 363, "unit", "svg-small", "cdu", "middle") +
      path("M154 158 H173 V384 H221 V439 H130 V187 H154 V158", "tech") +
      path("M173 223 V268", "tech", true) +
      path("M130 360 V312", "tech", true) +
      path("M358 393 H287 V432 H358", "facility") +
      path("M287 393 H323", "facility", true) +
      path("M332 432 H288", "facility", true) +
      path("M225 413 H280", "heat", true) +
      path("M170 88 H332", "air", true) +
      text(211, 116, "Residual air heat", "svg-small") +
      text(29, 248, "Technology", "svg-small tech-text") +
      text(29, 268, "coolant", "svg-small tech-text") +
      text(217, 510, "Facility water", "svg-label facility-text")
    );
  }
  return (
    rack(82, 99, 182, 240) +
    box("cdu", 568, 151, 291, 194) +
    text(712, 181, "CDU", "svg-label", "cdu", "middle") +
    text(712, 205, "Coolant distribution unit", "svg-small", "cdu", "middle") +
    path("M247 250 H630 V310 H247 V250", "tech") +
    path("M386 250 H451", "tech", true) +
    path("M450 310 H387", "tech", true) +
    text(313, 228, "Technology coolant", "svg-label tech-text") +
    path("M1100 242 H779 V307 H1100", "facility") +
    path("M840 242 H952", "facility", true) +
    path("M964 307 H849", "facility", true) +
    path("M637 276 H772", "heat", true) +
    text(938, 346, "Facility water", "svg-label facility-text") +
    path("M264 149 H437", "air", true) +
    text(290, 124, "Residual air heat", "svg-label") +
    text(82, 379, "Chip → cold plate → liquid", "svg-small")
  );
}

function rearDoorCapture(compact) {
  const x = compact ? 40 : 105,
    y = compact ? 76 : 107;
  const w = compact ? 132 : 194,
    h = compact ? 191 : 228;
  const dx = x + w + 10;
  let out = rack(x, y, w, h) + box("door", dx, y, 38, h);
  out += Array.from(
    { length: 7 },
    (_, i) =>
      `<path d="M${dx + 7} ${y + 20 + (i * (h - 40)) / 6} h24" class="outline"/>`,
  ).join("");
  if (compact)
    return (
      out +
      text(43, 45, "Rear-door heat exchanger", "svg-label") +
      path(`M15 ${y + 93} H${dx + 2}`, "air", true) +
      path(`M${dx + 42} ${y + 93} H350`, "air", true) +
      path(`M${dx + 19} ${y + 14} H350`, "facility", true) +
      path(`M350 ${y + h - 12} H${dx + 19} V${y + 14}`, "facility") +
      path(`M329 ${y + h - 12} H271`, "facility", true) +
      text(40, 297, "Rack air crosses the coil.", "svg-small") +
      text(44, 413, "Facility water carries heat away.", "svg-small") +
      path(`M${dx + 17} ${y + 110} V${y + 145}`, "heat", true)
    );
  return (
    out +
    text(330, 79, "Rear-door heat exchanger", "svg-label") +
    path(`M40 ${y + 111} H${dx + 2}`, "air", true) +
    path(`M${dx + 42} ${y + 111} H643`, "air", true) +
    path(`M${dx + 19} ${y + 19} H943`, "facility", true) +
    path(`M944 ${y + h - 18} H${dx + 19}`, "facility", true) +
    path(`M${dx + 19} ${y + h - 18} V${y + 19}`, "facility") +
    text(706, 176, "Facility water", "svg-label facility-text") +
    text(430, 259, "Air passes through the water-cooled door.", "svg-label") +
    path(`M${dx + 1} ${y + 111} H${dx + 31}`, "heat", true)
  );
}

function immersionCapture(compact) {
  const x = compact ? 24 : 73,
    y = compact ? 54 : 80,
    w = compact ? 324 : 498,
    h = compact ? 235 : 249;
  let out =
    box("bath", x, y, w, h) +
    text(x + 20, y + 31, "Immersion bath", "svg-label", "bath");
  out += `<rect x="${x + 9}" y="${y + 69}" width="${w - 18}" height="${h - 78}" rx="5" fill="var(--tech)" opacity="0.13"/>`;
  out += [0, 1, 2, 3]
    .map(
      (i) =>
        `<rect x="${x + 29 + (i * (w - 81)) / 4}" y="${y + 107}" width="${(w - 125) / 4}" height="${h - 141}" rx="4" class="face"/>`,
    )
    .join("");
  out += text(
    x + 20,
    y + 93,
    "Electronics in dielectric liquid",
    "svg-small",
    "bath",
  );
  if (compact)
    return (
      out +
      box("single", 24, 333, 324, 79) +
      text(43, 360, "Single-phase", "svg-label", "single") +
      text(43, 388, "Liquid warms without boiling.", "svg-small", "single") +
      box("two", 24, 432, 324, 99) +
      text(43, 462, "Two-phase", "svg-label", "two") +
      text(43, 491, "Liquid boils; vapor condenses", "svg-small", "two") +
      text(43, 511, "at a cooled surface.", "svg-small", "two")
    );
  return (
    out +
    path("M238 263 V204", "heat", true) +
    path("M442 263 V204", "heat", true) +
    box("single", 697, 77, 389, 111) +
    text(722, 112, "Single-phase", "svg-label", "single") +
    text(722, 151, "Liquid warms without boiling.", "svg-label", "single") +
    box("two", 697, 216, 389, 134) +
    text(722, 252, "Two-phase", "svg-label", "two") +
    text(722, 288, "Liquid boils; vapor condenses", "svg-label", "two") +
    text(722, 318, "at a cooled surface.", "svg-label", "two")
  );
}

function approach(compact) {
  if (compact) {
    let out =
      text(186, 25, "HYPOTHETICAL 84 kW CDU", "svg-tiny", "", "middle") +
      box("hx", 122, 109, 128, 221) +
      text(186, 140, "CDU", "svg-label", "hx", "middle");
    out +=
      path("M38 173 H151 V290 H38", "tech") +
      path("M55 173 H112", "tech", true) +
      path("M111 290 H50", "tech", true) +
      path("M334 290 H221 V173 H334", "facility") +
      path("M321 290 H263", "facility", true) +
      path("M263 173 H320", "facility", true) +
      path("M164 216 H207", "heat", true) +
      path("M164 259 H207", "heat", true);
    out +=
      text(29, 78, "Technology", "svg-label tech-text") +
      text(254, 78, "Facility", "svg-label facility-text") +
      text(33, 155, "45°C", "svg-label tech-text") +
      text(284, 155, "40°C", "svg-label facility-text") +
      text(33, 322, "35°C", "svg-label tech-text") +
      text(284, 322, "30°C", "svg-label facility-text") +
      text(34, 361, "Loop ΔT: 10 K", "svg-small tech-text") +
      text(244, 361, "Loop ΔT: 10 K", "svg-small facility-text") +
      text(186, 414, "CDU approach: 35 − 30 = 5 K", "svg-label", "", "middle") +
      text(
        186,
        451,
        "Technology supply − facility supply",
        "svg-small",
        "",
        "middle",
      ) +
      text(186, 512, "84 kW = 2 kg/s × 4.2 × 10 K", "svg-label", "", "middle") +
      text(
        186,
        545,
        "Both water paths: 2 kg/s · cₚ = 4.2 kJ/(kg·K)",
        "svg-small",
        "",
        "middle",
      );
    return out;
  }
  let out =
    text(
      580,
      28,
      "HYPOTHETICAL 84 kW CDU · COUNTERFLOW",
      "svg-tiny",
      "",
      "middle",
    ) +
    box("hx", 469, 70, 223, 219) +
    text(580, 101, "CDU heat exchanger", "svg-label", "hx", "middle");
  out +=
    path("M111 137 H521 V258 H111", "tech") +
    path("M194 137 H339", "tech", true) +
    path("M340 258 H195", "tech", true) +
    path("M1048 258 H640 V137 H1048", "facility") +
    path("M982 258 H829", "facility", true) +
    path("M827 137 H981", "facility", true) +
    path("M538 176 H624", "heat", true) +
    path("M538 223 H624", "heat", true);
  out +=
    text(112, 90, "Technology loop", "svg-label tech-text") +
    text(851, 90, "Facility loop", "svg-label facility-text") +
    text(302, 120, "45°C return", "svg-label tech-text") +
    text(776, 120, "40°C return", "svg-label facility-text") +
    text(302, 287, "35°C supply", "svg-label tech-text") +
    text(776, 287, "30°C supply", "svg-label facility-text") +
    text(112, 205, "Loop ΔT: 10 K", "svg-label tech-text") +
    text(899, 205, "Loop ΔT: 10 K", "svg-label facility-text") +
    text(580, 335, "CDU approach: 35 − 30 = 5 K", "svg-label", "", "middle") +
    text(
      580,
      359,
      "Technology supply − facility supply",
      "svg-small",
      "",
      "middle",
    ) +
    text(
      580,
      404,
      "84 kW = 2 kg/s × 4.2 kJ/(kg·K) × 10 K · each water loop carries 2 kg/s",
      "svg-label",
      "",
      "middle",
    );
  return out;
}

export function renderFoundation(kind, compact, state = {}) {
  if (kind === "why-liquid") return airMarker + whyLiquid(compact);
  if (kind === "water-balance") return waterBalance(compact, state);
  if (kind === "approach") return airMarker + approach(compact);
  if (kind === "capture-options") {
    const renderers = {
      air: airCapture,
      coldplate: coldplateCapture,
      "rear-door": rearDoorCapture,
      immersion: immersionCapture,
    };
    return airMarker + (renderers[state.capture] || airCapture)(compact);
  }
  throw new RangeError(`Unknown cooling foundation: ${kind}`);
}
