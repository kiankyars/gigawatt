import {
  currentThreePhase,
  resistiveLossRatio,
  energyMWh,
  rideThroughMinutes,
  rackCurrent,
  coolantFlow,
  capacityBudget,
} from "./math.js";

// prettier-ignore
export const VISUAL_IDS = [
  "campus",
  "energy",
  "grid",
  "voltage",
  "substation",
  "capacity",
  "train",
  "ride-through",
  "redundancy",
  "failure",
  "rack",
  "current",
  "compute",
  "heat",
  "liquid",
  "cdu",
  "air",
  "rejection",
  "pue",
  "bottleneck",
  "case",
  "synthesis"
];
const C = {
  power: "#ffc875",
  cold: "#75d8e7",
  hot: "#f08383",
  ink: "#dbe7ee",
  muted: "#9eb3c1",
  green: "#93dbb0",
  violet: "#bab0f3",
};
const fmt = (n, d = 0) =>
  Number(n).toLocaleString("en-US", {
    maximumFractionDigits: d,
    minimumFractionDigits: d,
  });
function txt(x, y, s, cls = "", color = "", anchor = "start") {
  return `<text x="${x}" y="${y}" class="diagram-text ${cls}"${color ? ` fill="${color}" style="fill:${color}"` : ""} text-anchor="${anchor}">${s}</text>`;
}
function line(d, c = C.power, w = 3, extra = "") {
  return `<path d="${d}" fill="none" stroke="${c}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
}
function rect(x, y, w, h, fill = "#203545", stroke = "#547084", r = 3) {
  return `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${fill}" stroke="${stroke}"/>`;
}
function dot(x, y, c = C.power, r = 5) {
  return `<circle cx="${x}" cy="${y}" r="${r}" fill="${c}"/>`;
}
function arrow(d, c = C.power, w = 3) {
  return line(d, c, w, `marker-end="url(#a-${c.slice(1)})"`);
}
function metric(x, y, n, unit, label, c = C.power) {
  return (
    txt(x, y, n, "diagram-number", c) +
    txt(x, y + 28, unit, "diagram-small", c) +
    txt(x, y + 60, label, "diagram-small")
  );
}
function chip(x, y, w = 100, h = 95) {
  let p = "";
  for (let i = 10; i < w; i += 12)
    p += line(`M${x + i} ${y - 9}v9 M${x + i} ${y + h}v9`, "#628294", 2);
  for (let i = 10; i < h; i += 12)
    p += line(`M${x - 9} ${y + i}h9 M${x + w} ${y + i}h9`, "#628294", 2);
  return (
    p +
    rect(x, y, w, h, "#1a3242", "#87a4b4") +
    rect(x + 12, y + 12, w - 24, h - 24, "#365963", C.cold) +
    line(`M${x + 20} ${y + 20}h${w - 40}v${h - 40}h-${w - 40}Z`, "#87d2ce", 0.6)
  );
}
function server(x, y, w = 110, h = 30, lit = true) {
  return (
    rect(x, y, w, h, "#213b4b", "#58768a", 1) +
    line(`M${x + 12} ${y + 9}h${w - 40}m-${w - 40} 7h${w - 40}`, "#7f9cad", 1) +
    dot(x + w - 12, y + 12, lit ? C.green : "#617280", 2.5)
  );
}
function rack(x, y, w = 110, h = 220, lit = true) {
  let a = rect(x, y, w, h, "#132938", "#728e9f", 2);
  for (let i = 0; i < 6; i++)
    a += server(x + 8, y + 14 + (i * (h - 28)) / 6, w - 16, (h - 40) / 6, lit);
  return (
    a +
    line(`M${x + 9} ${y + h + 4}v7 M${x + w - 9} ${y + h + 4}v7`, "#567789", 5)
  );
}
function cube(
  x,
  y,
  w,
  d,
  h,
  colors = ["#365769", "#233f51", "#192f41"],
  stroke = "#638294",
) {
  const p = [
      [x, y],
      [x + w, y + w * 0.38],
      [x + w - d, y + w * 0.38 + d * 0.5],
      [x - d, y + d * 0.5],
    ],
    t = p.map(([a, b]) => [a, b - h]);
  const poly = (pts, fill) =>
    `<polygon points="${pts.map((a) => a.join(",")).join(" ")}" fill="${fill}" stroke="${stroke}" stroke-width="1"/>`;
  return (
    poly([p[0], p[1], t[1], t[0]], colors[1]) +
    poly([p[1], p[2], t[2], t[1]], colors[2]) +
    poly(t, colors[0])
  );
}
function pylon(x, y, s = 1) {
  return `<g transform="translate(${x} ${y}) scale(${s})">${line("M-26 0 0-150 26 0 M-20-32H20 M-15-64H15 M-10-96H10 M-6-120H6 M-20-32 15-64-10-96 6-120 M20-32-15-64 10-96-6-120 M-50-99H50 M-37-126H37 M0-150-37-126-50-99 M0-150 37-126 50-99", "#a2b8c4", 2)}${[-45, -30, 30, 45].map((a) => line(`M${a} -99v12`, "#849dae", 3)).join("")}</g>`;
}
function transformer(x, y, s = 1) {
  return `<g transform="translate(${x} ${y}) scale(${s})">${cube(0, 0, 85, 45, 80)}${Array.from({ length: 8 }, (_, i) => line(`M${-35 + i * 7} ${-10 + i * 2.7}v-54`, "#9cb4c1", 2)).join("")}${[0, 27, 54].map((a) => line(`M${a} ${-77 + a * 0.38}v-24`, "#dbdfe0", 5)).join("")}</g>`;
}
function fan(x, y, r = 23) {
  return `<g>${`<circle cx="${x}" cy="${y}" r="${r}" stroke="#8dafbd" fill="#183142"/>`}${[0, 120, 240].map((a) => `<path d="M${x} ${y}q-${r} -${r} ${r * 0.1} -${r * 0.83}q${r * 0.55} ${r * 0.25} -${r * 0.1} ${r * 0.83}" fill="#6a8b9b" transform="rotate(${a} ${x} ${y})"/>`).join("")}${dot(x, y, "#c9dade", 4)}</g>`;
}
function sv(title, body) {
  const markers = Object.values(C)
    .map(
      (c) =>
        `<marker id="a-${c.slice(1)}" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 1 8 5 0 9" fill="none" stroke="${c}" stroke-width="1.5"/></marker>`,
    )
    .join("");
  return `<svg viewBox="0 0 900 545" role="img" aria-label="${title}" xmlns="http://www.w3.org/2000/svg"><defs>${markers}<pattern id="dots" width="26" height="26" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".65" fill="#9db8ca" opacity=".12"/></pattern></defs><rect width="900" height="545" fill="url(#dots)"/><g class="subtle-enter">${body}</g></svg>`;
}

function campusScene(s, final = false) {
  let b = "";
  b += `<path d="M74 297 450 139 829 320 454 498Z" fill="#172c3b" stroke="#38556a"/>`;
  for (let i = 0; i < 7; i++)
    b += line(
      `M${106 + i * 49} ${283 - i * 21}l378 181`,
      "#6b8ea0",
      0.65,
      'opacity=".18"',
    );
  b += line("M74 297 450 478 829 320", "#55778a", 1);
  b += pylon(172, 277, 0.82) + pylon(264, 235, 0.6);
  b += line(
    "M135 194Q180 223 237 175 M209 194Q230 200 291 175",
    "#708b9d",
    1.2,
  );
  b += transformer(305, 333, 0.82) + transformer(375, 304, 0.57);
  b += cube(468, 399, 239, 127, 105, ["#233e50", "#1b3344", "#142c3d"]);
  // Open roof, inner floor and a pair of visible rack rows.
  b += `<polygon points="${[
    [447, 307],
    [641, 381],
    [733, 335],
    [539, 260],
  ]
    .map((p) => p.join(","))
    .join(" ")}" fill="#203b4c" stroke="#7694a4"/>`;
  for (let row = 0; row < 2; row++)
    for (let i = 0; i < 5; i++) {
      const x = 477 + i * 34 + row * 46,
        y = 324 + i * 13 - row * 23;
      b += cube(x, y, 24, 17, 58, ["#5d7f8c", "#314f5f", "#203c4d"]);
      for (let j = 0; j < 5; j++)
        b += line(`M${x + 3} ${y - 9 - j * 8}l17 6`, "#88b4bb", 1);
    }
  b += cube(648, 221, 127, 49, 48, ["#3e5d6b", "#2a4555", "#1f3748"]);
  b += fan(677, 181, 16) + fan(719, 197, 16);
  b +=
    arrow("M199 275 230 290 275 308", C.power, 4) +
    arrow("M352 356 405 381 454 358", C.power, 4);
  b += arrow("M591 286 637 261 696 282 745 257 745 218", C.hot, 4);
  b += arrow("M668 239 625 219 557 251 557 284", C.cold, 3);
  b += arrow("M686 165v-35", C.hot, 2) + arrow("M725 180v-37", C.hot, 2);
  b +=
    line("M187 140V101H80", "#698697", 1) +
    txt(80, 81, "01 / GRID", "diagram-small", C.power);
  b +=
    line("M306 361 264 405H87", "#698697", 1) +
    txt(87, 432, "02 / SUBSTATION", "diagram-small", C.power);
  b +=
    line("M610 393v65h167", "#698697", 1) +
    txt(617, 483, "03 / RACKS", "diagram-small", C.ink);
  b +=
    line("M741 167 788 116h35", "#698697", 1) +
    txt(602, 86, "04 / HEAT OUT", "diagram-small", C.hot);
  b += txt(
    450,
    40,
    final
      ? "A WORKING RACK IS A SYSTEM OUTCOME"
      : "ELECTRICITY IN. COMPUTATION. HEAT OUT.",
    "diagram-tiny",
    C.muted,
    "middle",
  );
  return {
    body: b,
    caption:
      "An illustrative campus, with an open roof to reveal the racks. Gold carries electricity; blue and coral trace cooling supply and heat removal.",
    label: final ? "22 / THE WHOLE SYSTEM" : "01 / ONE CAMPUS, TWO JOURNEYS",
  };
}
function energyScene(s) {
  const p = s.power ?? 1,
    h = s.hours ?? 1;
  let b = txt(
    74,
    69,
    "POWER IS THE HEIGHT. ENERGY IS THE AREA.",
    "diagram-tiny",
  );
  b += line("M105 129V410H800", "#7a94a5", 1.5);
  const top = 410 - (p / 5) * 230,
    right = 105 + (h / 24) * 695;
  b +=
    `<path d="M105 410V${top}H${right}V410Z" fill="#ffc875" fill-opacity=".19"/>` +
    line(`M105 ${top}H${right}`, C.power, 3) +
    line(`M${right} ${top}V410`, C.power, 1, 'stroke-dasharray="4 6"');
  b +=
    txt(105, 451, "0 h", "diagram-small") +
    txt(800, 451, "24 h", "diagram-small", "", "end") +
    txt(105, 113, "MW", "diagram-small");
  b += metric(
    405,
    186,
    fmt(energyMWh(p, h), 1),
    "MWh of energy",
    `${fmt(p, 1)} MW × ${h} hours`,
  );
  b += txt(
    74,
    505,
    "A 1 MW load running for 1 hour uses 1 MWh.",
    "diagram-small",
  );
  return {
    body: b,
    label: "02 / RATE × TIME",
    tag: "IDEALIZED CONSTANT LOAD",
    caption:
      "The height is power (MW); width is time (hours). The shaded area is energy (MWh). Move either slider to change the area.",
  };
}
function gridScene(s) {
  let b = txt(
    62,
    56,
    "A CONTRACT AND A WIRE DO DIFFERENT JOBS.",
    "diagram-tiny",
  );
  b +=
    `<circle cx="153" cy="252" r="58" fill="#223b4a" stroke="#8ca8b8" stroke-width="2"/>` +
    line("M118 252q17-37 35 0t35 0", C.power, 3) +
    line("M108 211H215", C.power, 3);
  b +=
    rect(267, 184, 226, 110) +
    txt(380, 226, "Shared grid", "", "", "middle") +
    txt(380, 255, "Many sources · many loads", "diagram-small", "", "middle");
  b += rack(669, 184, 100, 166) + arrow("M211 230H263") + arrow("M497 230H660");
  b +=
    rect(305, 360, 150, 92, "#262b43", "#8d84b3") +
    line("M329 386h100m-100 15h78m-78 15h92", C.violet, 1.5) +
    txt(380, 479, "Energy contract", "diagram-small", C.violet, "middle");
  b += line(
    "M160 309V406H300 M459 406H716V364",
    C.violet,
    2,
    'stroke-dasharray="6 7"',
  );
  b +=
    txt(152, 327, "Generation", "diagram-small", "", "middle") +
    txt(719, 163, "Data center", "diagram-small", "", "middle");
  b +=
    txt(62, 104, "Physical delivery", "", C.power) +
    txt(558, 104, "Commercial accounting", "", C.violet);
  return {
    body: b,
    label: "03 / SOURCES & DELIVERY",
    caption:
      "The solid line is the physical electricity network. The dashed line represents a contract. Onsite generation still needs its own equipment, fuel, permissions, and operating limits.",
  };
}
function voltageScene(s) {
  const v = s.voltage ?? 138,
    i = currentThreePhase(100, v),
    ratio = resistiveLossRatio(v, 13.8);
  let b = "";
  b += pylon(184, 316, 1.1) + pylon(695, 316, 1.1);
  b += line(
    "M136 203Q430 304 647 203 M151 203Q430 274 662 203 M218 203Q430 242 729 203",
    C.power,
    Math.max(1.5, (5 * 13.8) / v),
  );
  b += txt(448, 103, "100 MW DELIVERED", "diagram-tiny", C.muted, "middle");
  b += txt(448, 165, `${fmt(v, 1)} kV`, "diagram-number", C.power, "middle");
  b += metric(122, 406, fmt(i), "amps per phase", "I = P / (√3 × V × PF)");
  b += metric(
    534,
    406,
    `${fmt(ratio * 100, ratio < 0.01 ? 2 : 1)}%`,
    "relative conductor loss",
    "Compared with 13.8 kV",
    C.hot,
  );
  return {
    body: b,
    label: "04 / THE VOLTAGE EXPERIMENT",
    tag: "BALANCED 3-PHASE · PF = 1",
    caption:
      "Fixed 100 MW, balanced three-phase AC, power factor 1, and unchanged conductor resistance. Raising voltage 10× lowers current 10× and I²R loss 100×. It does not create power.",
  };
}
function substationScene(s) {
  let b = txt(
    65,
    62,
    "CHANGE VOLTAGE. CONTROL WHERE POWER CAN FLOW.",
    "diagram-tiny",
  );
  b += pylon(155, 290, 1) + transformer(417, 329, 1.3);
  b += cube(633, 323, 64, 36, 136) + cube(704, 352, 64, 36, 136);
  b += arrow("M186 267 290 309 336 286") + arrow("M471 352 567 390 618 365");
  b +=
    line("M421 165v-45h90", "#6e8b9e", 1) +
    txt(526, 125, "Transformer", "", C.power) +
    txt(526, 152, "Changes voltage", "diagram-small");
  b +=
    line("M736 223v-57h63", "#6e8b9e", 1) +
    txt(663, 141, "Switchgear", "", C.ink);
  b +=
    txt(100, 396, "HIGH VOLTAGE", "diagram-tiny", C.power) +
    txt(568, 438, "PROTECTED BUILDING FEEDERS", "diagram-tiny", C.power);
  b += txt(
    75,
    501,
    "A transformer changes voltage; breakers isolate faults. Neither makes electrical energy.",
    "diagram-small",
  );
  return {
    body: b,
    label: "05 / THE CAMPUS THRESHOLD",
    caption:
      "Conceptual equipment arrangement. Actual campus voltage, protection, grounding, redundancy, and feeder topology are site-specific engineering choices.",
  };
}
function capacityScene(s) {
  const step = s.gate ?? 0,
    names = ["Announced", "Connected", "Energized", "Commissioned", "Loaded"];
  let b = txt(65, 69, "CAPACITY HAS A LIFECYCLE.", "diagram-tiny");
  for (let i = 0; i < 5; i++) {
    const x = 66 + i * 164,
      active = i <= step;
    b += rect(
      x,
      192,
      138,
      176,
      active ? "#2e423e" : "#1b303f",
      active ? C.green : "#465f72",
    );
    b += txt(
      x + 18,
      231,
      String(i + 1).padStart(2, "0"),
      "diagram-small",
      active ? C.green : C.muted,
    );
    b += txt(x + 18, 280, names[i], "diagram-small", active ? C.ink : C.muted);
    b += txt(
      x + 18,
      337,
      i === step ? "YOU ARE HERE" : i < step ? "PASSED" : "NEXT GATE",
      "diagram-tiny",
      active ? C.green : C.muted,
    );
    if (i < 4)
      b += arrow(`M${x + 145} 279h11`, i < step ? C.green : "#546f81", 1.5);
  }
  const desc = [
    "A plan describes an intended outcome.",
    "The electrical connection has been established.",
    "Equipment is electrically live.",
    "Systems have passed their required integrated tests.",
    "IT equipment is drawing power under workload.",
  ];
  b += txt(66, 126, "These milestones answer different questions.", "");
  b += txt(66, 439, desc[step], "", C.green);
  return {
    body: b,
    label: "06 / FROM PROMISE TO SERVICE",
    tag: "SIMPLIFIED MILESTONES",
    caption:
      "Select a milestone. A later stage requires additional evidence; a permit, lease, interconnection agreement, or energized substation does not prove running racks. Track one selected path: other buildings may be at different stages.",
  };
}
function trainScene(s) {
  const a = s.equipment ?? 0,
    names = ["Transformer", "Switchgear", "UPS", "Busway", "Rack"],
    verbs = [
      "Changes voltage",
      "Isolates and protects",
      "Conditions + bridges",
      "Distributes power",
      "Converts AC to DC",
    ];
  let b = txt(
    62,
    64,
    "LEARN EACH BOX BY THE PROBLEM IT SOLVES.",
    "diagram-tiny",
  );
  for (let i = 0; i < 5; i++) {
    const x = 62 + i * 164,
      c = a === i ? C.power : "#657f90";
    if (i === 0) b += transformer(x + 45, 323, 0.75);
    else if (i === 4) b += rack(x + 18, 170, 105, 182);
    else {
      b += rect(x + 12, 190, 112, 162, a === i ? "#3d3b2d" : "#213847", c);
      if (i === 1) b += line(`M${x + 68} 215v32m0 36v32m0-32 21-25`, c, 3);
      if (i === 2) {
        b +=
          rect(x + 35, 239, 65, 41, "none", c) +
          txt(x + 48, 267, "~ → ~", "diagram-small", c);
      }
      if (i === 3)
        for (let k = 0; k < 4; k++)
          b += line(`M${x + 32} ${220 + k * 27}h72`, c, 4);
    }
    b += txt(
      x + 64,
      396,
      names[i],
      "diagram-small",
      a === i ? C.power : C.muted,
      "middle",
    );
    if (i < 4) b += arrow(`M${x + 135} 284h25`, C.power, 2);
  }
  b += txt(450, 471, verbs[a], "", C.power, "middle");
  return {
    body: b,
    label: "07 / INSIDE THE ELECTRICAL ROOM",
    caption:
      "A conceptual protected power path. UPS placement, bypass, alternate feeds, and maintenance arrangements vary. Select equipment to connect its name to its function.",
  };
}
function rideScene(s) {
  const off = s.outage ?? false,
    e = s.battery ?? 0.25,
    p = 5,
    t = rideThroughMinutes(e, p);
  let b = txt(62, 65, "STORED ENERGY BUYS TIME.", "diagram-tiny");
  b += pylon(153, 312, 0.93) + rack(693, 165, 110, 211, !off || e > 0);
  b +=
    rect(356, 221, 174, 100, "#203b45", off ? C.power : "#587d89") +
    rect(370, 236, 143, 69, "#19313e", C.power) +
    rect(530, 251, 12, 39, C.power, C.power);
  const cells = Math.round((e / 0.5) * 8);
  for (let j = 0; j < 8; j++)
    b += rect(
      379 + j * 16,
      246,
      11,
      49,
      j < cells ? C.power : "#2c404c",
      "none",
      1,
    );
  b += arrow("M203 269H344", off ? "#546a7a" : C.power, 3);
  if (off) b += line("M260 252l25 33m0-33-25 33", C.hot, 3);
  b += arrow("M548 269H681", C.power, 4);
  b +=
    txt(
      152,
      359,
      off ? "Utility lost" : "Utility available",
      "diagram-small",
      off ? C.hot : C.green,
      "middle",
    ) +
    txt(444, 359, "UPS + stored energy", "diagram-small", "", "middle") +
    txt(748, 415, "5 MW load", "diagram-small", C.power, "middle");
  b += metric(
    100,
    447,
    fmt(t, 1),
    "minutes of ideal runtime",
    `${fmt(e, 2)} MWh usable output energy ÷ 5 MW`,
  );
  return {
    body: b,
    label: "08 / RIDE THROUGH AN INTERRUPTION",
    tag: "IDEAL ENERGY LIMIT",
    caption:
      "Use the outage switch, then change stored energy. Real runtime also depends on UPS power rating, battery condition, discharge limits, and transfer behavior. Backup must become available before stored energy runs out.",
  };
}
function redundancyScene(s) {
  const failed = s.pathFailed ?? false;
  let b = txt(64, 66, "REDUNDANCY IS ABOUT A SURVIVING PATH.", "diagram-tiny");
  b += rack(694, 185, 116, 199, true);
  for (let j = 0; j < 2; j++) {
    const y = 178 + j * 177,
      c = j === 0 && failed ? C.hot : j === 1 && failed ? C.green : C.power;
    b +=
      rect(96, y, 156, 88, "#203746", c) +
      txt(
        174,
        y + 36,
        `PATH ${j === 0 ? "A" : "B"}`,
        "diagram-small",
        c,
        "middle",
      ) +
      txt(174, y + 64, "100% of load", "diagram-small", "", "middle");
    b += arrow(
      `M258 ${y + 44}H526V${y + 44 + (j === 0 ? 35 : -35)}H679`,
      j === 0 && failed ? "#4e6273" : c,
      3,
    );
    if (j === 0 && failed)
      b += line(`M367 ${y + 27}l29 34m0-34-29 34`, C.hot, 3);
  }
  b += txt(
    94,
    449,
    failed
      ? "Path B must carry the full load after A fails."
      : "Both paths are available. Each is rated for the full load.",
    "",
    failed ? C.green : C.ink,
  );
  b += txt(
    94,
    488,
    "A generic dual-fed design; actual transfers depend on the load and architecture.",
    "diagram-small",
  );
  return {
    body: b,
    label: "09 / WHAT SURVIVES A FAILURE?",
    tag: "ILLUSTRATIVE 2N POWER PATHS",
    caption:
      "Disable path A. Duplicating boxes helps only if the other path has enough capacity and avoids the same failure. Two full paths support one load; their ratings are not additive sellable capacity.",
  };
}
function failureScene(s) {
  const trip = s.fault ?? false;
  let b = txt(
    62,
    62,
    "ISOLATE THE FAULT. KEEP THE OTHER LOADS ALIVE.",
    "diagram-tiny",
  );
  b +=
    line("M148 153H752", C.power, 5) +
    txt(450, 125, "SHARED SUPPLY BUS", "diagram-tiny", C.power, "middle");
  for (let j = 0; j < 3; j++) {
    const x = 192 + j * 258,
      c = trip && j === 1 ? C.hot : C.power;
    b +=
      line(`M${x} 154v60`, c, 3) +
      line(`M${x} 262v43`, trip && j === 1 ? "#425a6b" : c, 3) +
      rect(x - 23, 216, 46, 43, "#172e3d", c) +
      line(
        `M${x} 223v6m0 17v5m0-5 ${trip && j === 1 ? "15-13" : "0-13"}`,
        c,
        2,
      ) +
      rack(x - 56, 310, 112, 137, !(trip && j === 1));
    if (trip && j === 1)
      b += txt(x, 486, "ISOLATED", "diagram-small", C.hot, "middle");
    else b += txt(x, 486, "POWERED", "diagram-small", C.green, "middle");
  }
  return {
    body: b,
    label: "10 / SELECTIVE PROTECTION",
    caption:
      "A simplified selective-trip example. Fault location, fault current, device ratings, and coordinated settings determine which device opens. This diagram assumes branch-level selectivity.",
  };
}
function rackScene(s) {
  let b = txt(
    65,
    62,
    "THE RACK IS AN ELECTRICAL SYSTEM IN MINIATURE.",
    "diagram-tiny",
  );
  b += rack(133, 144, 190, 286);
  b += rect(150, 165, 155, 47, "#443e2d", C.power);
  b += txt(228, 195, "POWER SHELF", "diagram-small", C.power, "middle");
  b +=
    arrow("M73 189H130", C.power, 3) +
    txt(63, 160, "AC", "diagram-small", C.power);
  b +=
    line("M319 230H382V152H526", C.power, 2) +
    txt(447, 124, "DC bus", "diagram-small", C.power, "middle");
  b +=
    rect(398, 285, 142, 126, "#264234", "#7ba591") +
    rect(429, 325, 81, 43, "#4c6442", C.power) +
    txt(469, 353, "VRM", "", C.power, "middle");
  b +=
    arrow("M530 160H602V270H544", C.power, 3) +
    arrow("M545 349H655", C.power, 4) +
    chip(681, 300, 118, 101);
  b +=
    txt(228, 474, "RACK", "diagram-tiny", C.muted, "middle") +
    txt(469, 451, "BOARD REGULATOR", "diagram-tiny", C.muted, "middle") +
    txt(740, 451, "PROCESSOR", "diagram-tiny", C.muted, "middle");
  b += txt(677, 251, "Low-voltage rails", "diagram-small", C.power);
  return {
    body: b,
    label: "11 / AC TO SILICON",
    caption:
      "Conceptual rack path: power supplies rectify AC, a rack or board bus distributes DC, and local voltage regulators feed the processor. Bus architecture and voltage vary by platform.",
  };
}
function currentScene(s) {
  const v = s.coreV ?? 1,
    i = rackCurrent(1, v);
  let b = txt(
    65,
    65,
    "SAME POWER. LOWER VOLTAGE. MUCH MORE CURRENT.",
    "diagram-tiny",
  );
  b +=
    rect(90, 211, 170, 135, "#243c45", "#6b8a9c") +
    txt(175, 269, "1,000 W", "", "", "middle") +
    txt(175, 300, "ideal load power", "diagram-small", "", "middle");
  b +=
    chip(634, 205, 144, 141) +
    arrow("M270 276H612", C.power, 2 + 10 * Math.sqrt(i / 1000));
  b += txt(
    446,
    222,
    `${fmt(v, v < 2 ? 1 : 0)} V`,
    "diagram-number",
    C.power,
    "middle",
  );
  b += txt(446, 336, `${fmt(i)} A`, "", C.power, "middle");
  b +=
    txt(95, 433, "50 V → 20 A", "", C.muted) +
    txt(508, 433, "1 V → 1,000 A", "", C.power);
  b += txt(
    95,
    485,
    "P = V × I     ·     Local regulators keep the huge-current path short.",
    "diagram-small",
  );
  return {
    body: b,
    label: "12 / WHY REGULATION MOVES CLOSE TO THE CHIP",
    tag: "IDEALIZED 1 kW LOAD",
    caption:
      "Change voltage for an ideal constant 1 kW DC load. This isolates P = VI; it is not a proposed rack-wide 1 V bus, and real converters have losses and multiple processor rails. Line thickness is qualitative.",
  };
}
function computeScene(s) {
  const util = s.utilization ?? 60;
  let b = txt(
    65,
    62,
    "POWER ENABLES COMPUTATION. IT DOES NOT MEASURE IT.",
    "diagram-tiny",
  );
  b += chip(108, 197, 185, 165);
  b +=
    arrow("M54 279H87", C.power, 4) +
    arrow("M199 367v58", C.hot, 4) +
    txt(195, 469, "HEAT", "diagram-tiny", C.hot, "middle");
  b += txt(352, 142, "AN ILLUSTRATIVE WORKLOAD TRACE", "diagram-tiny");
  const busy = Math.round(util / 10);
  for (let r = 0; r < 4; r++)
    for (let j = 0; j < 10; j++)
      b += rect(
        355 + j * 43,
        187 + r * 44,
        32,
        29,
        j < busy ? C.violet : "#233747",
        j < busy ? "#cec3fa" : "#435e70",
        2,
      );
  b += txt(
    356,
    412,
    `${util}% scheduled busy time in this illustration`,
    "",
    C.violet,
  );
  b += txt(
    356,
    461,
    "Model · precision · memory · network · batching",
    "diagram-small",
  );
  b += line("M301 267H337", C.violet, 2, 'stroke-dasharray="4 6"');
  return {
    body: b,
    label: "13 / FROM POWER TO USEFUL WORK",
    tag: "CONCEPTUAL SCHEDULING TRACE",
    caption:
      "Purple blocks show illustrative busy intervals, not measured efficiency. No token rate can be inferred from these blocks or from a megawatt rating. Electrical power still becomes heat while the computation happens.",
  };
}
function heatScene(s) {
  let b = txt(
    62,
    62,
    "THE ELECTRICAL BUDGET BECOMES A THERMAL DUTY.",
    "diagram-tiny",
  );
  b +=
    rack(390, 149, 146, 259) +
    arrow("M75 270H360", C.power, 18) +
    arrow("M568 270H821", C.hot, 18);
  b +=
    txt(200, 210, "100 kW", "diagram-number", C.power, "middle") +
    txt(200, 340, "ELECTRICITY", "diagram-tiny", C.power, "middle");
  b +=
    txt(699, 210, "≈100 kW", "diagram-number", C.hot, "middle") +
    txt(699, 340, "HEAT", "diagram-tiny", C.hot, "middle");
  b += txt(
    464,
    448,
    "Information processing occurs inside the rack.",
    "",
    C.ink,
    "middle",
  );
  b += txt(
    464,
    487,
    "It does not remove a large fraction of the electrical energy.",
    "diagram-small",
    C.muted,
    "middle",
  );
  return {
    body: b,
    label: "14 / TURN THE JOURNEY AROUND",
    tag: "STEADY STATE · RACK BOUNDARY",
    caption:
      "Nearly all rack electrical input ultimately becomes heat. At steady state, heat must leave at approximately the electrical input rate; thermal storage only buys time.",
  };
}
function liquidScene(s) {
  const dt = s.deltaT ?? 10,
    flow = coolantFlow(100, dt);
  let b = txt(64, 61, "THE WATER CARRIES HEAT AWAY.", "diagram-tiny");
  b += chip(122, 192, 182, 152) + rect(110, 185, 206, 168, "#365e6e55", C.cold);
  b += line("M120 211h163v29H139v28h144v29H138v27h162", C.cold, 7);
  b +=
    arrow("M67 214H112", C.cold, 6) + arrow("M303 326H383V226H473", C.hot, 6);
  b += metric(
    525,
    220,
    fmt(flow, 2),
    "kg/s of water",
    `≈ ${fmt(flow * 60)} L/min`,
    C.cold,
  );
  b +=
    txt(523, 355, `ΔT = ${dt}°C`, "", C.hot) +
    txt(523, 390, "100 kW transferred into water", "diagram-small");
  b +=
    txt(73, 448, "Q̇ = ṁ × cₚ × ΔT", "", C.cold) +
    txt(
      73,
      491,
      "Half the temperature rise needs twice the flow.",
      "diagram-small",
    );
  return {
    body: b,
    label: "15 / THE COOLANT EXPERIMENT",
    tag: "IDEAL WATER HEAT BALANCE",
    caption:
      "Assume 100 kW captured by pure water, cp = 4.18 kJ/(kg·K), density ≈ 1 kg/L. Actual coolant mixtures, pressure drop, pump limits, and allowable component temperatures constrain a design.",
  };
}
function cduScene(s) {
  let b = txt(
    65,
    60,
    "HEAT CROSSES. THE TWO FLUIDS STAY SEPARATE.",
    "diagram-tiny",
  );
  b += rack(79, 210, 101, 168) + rect(354, 151, 192, 265, "#213d4a", "#83a2b4");
  for (let j = 0; j < 10; j++)
    b += line(`M${382 + j * 13} 186v189`, j % 2 === 0 ? C.cold : C.hot, 5);
  b += arrow("M183 243H368", C.hot, 4) + arrow("M370 352H184", C.cold, 4);
  b +=
    arrow("M533 210H751V266", C.hot, 4) + arrow("M752 344V374H533", C.cold, 4);
  b +=
    rect(682, 268, 136, 74, "#203847", "#82a2b6") +
    txt(750, 311, "Facility loop", "diagram-small", "", "middle");
  b +=
    txt(127, 168, "RACK LOOP", "diagram-tiny", C.cold, "middle") +
    txt(450, 118, "HEAT EXCHANGER", "diagram-tiny", C.ink, "middle");
  b +=
    arrow("M408 287H494", C.hot, 3) +
    txt(450, 448, "HEAT →", "diagram-small", C.hot, "middle");
  b += txt(
    62,
    502,
    "A liquid-to-liquid CDU also manages circulation and operating conditions.",
    "diagram-small",
  );
  return {
    body: b,
    label: "16 / THE CDU BOUNDARY",
    caption:
      "One common liquid-to-liquid arrangement. Alternate CDU architectures exist. The heat exchanger separates water quality and pressure regimes; it transfers heat without mixing the two loops.",
  };
}
function airScene(s) {
  let b = txt(63, 61, "THIS HYBRID RACK HAS TWO HEAT PATHS.", "diagram-tiny");
  b +=
    rack(198, 169, 153, 229) + rect(597, 171, 151, 227, "#253d4c", "#7392a6");
  b += fan(671, 236, 39) + fan(671, 333, 39);
  b +=
    line("M613 282h118m-118 8h118", C.cold, 2) +
    arrow("M749 286H812V230", C.hot, 2) +
    txt(796, 206, "Heat onward", "diagram-small", C.hot, "middle");
  b +=
    arrow("M672 407V452H274V404", C.cold, 5) + arrow("M354 231H584", C.hot, 5);
  b +=
    arrow("M441 129H111V255H200", C.cold, 4) +
    arrow("M352 335H443V160", C.hot, 4);
  b += txt(445, 107, "LIQUID PATH", "diagram-tiny", C.cold, "middle");
  b +=
    txt(470, 212, "Warm room air", "diagram-small", C.hot, "middle") +
    txt(480, 489, "Cooled air returns", "diagram-small", C.cold, "middle");
  b +=
    txt(274, 149, "RACK", "diagram-tiny", C.ink, "middle") +
    txt(671, 149, "AIR HANDLER", "diagram-tiny", C.ink, "middle");
  return {
    body: b,
    label: "17 / TWO HEAT PATHS",
    caption:
      "A qualitative split with no implied percentage. Liquid-cooled components send heat to coolant; remaining components send heat to room air. Fans circulate the air; the air-handler coil transfers its heat onward. Both duties must reach a rejection system.",
  };
}
function rejectionScene(s) {
  const w = s.chiller ?? 20;
  let b = txt(61, 61, "MOVING HEAT CAN ADD MORE HEAT.", "diagram-tiny");
  b +=
    rect(362, 187, 196, 158, "#233d4d", "#7fa0b1") +
    fan(414, 265, 33) +
    fan(506, 265, 33);
  b +=
    arrow("M66 275H346", C.hot, 11) + arrow("M574 275H831", C.hot, 11 + w / 10);
  b += arrow("M460 104V174", C.power, 4);
  b +=
    txt(83, 222, "100 kW", "", C.hot) +
    txt(83, 321, "heat absorbed", "diagram-small");
  b +=
    txt(639, 222, `${100 + w} kW`, "", C.hot) +
    txt(639, 321, "heat rejected", "diagram-small");
  b += txt(512, 132, `${w} kW work in`, "diagram-small", C.power);
  b += txt(460, 400, "Q̇ rejected = Q̇ absorbed + Ẇ input", "", C.ink, "middle");
  b += txt(
    460,
    465,
    "Outdoor conditions and supply temperature change the work required.",
    "diagram-small",
    C.muted,
    "middle",
  );
  return {
    body: b,
    label: "18 / THE LAST HOP TO THE ENVIRONMENT",
    tag: "ILLUSTRATIVE CHILLER BALANCE",
    caption:
      "Energy balance for a chiller, using illustrative compressor work. Fans and pumps add their own loads at the appropriate system boundary. Economizers can reduce compressor use when conditions permit.",
  };
}
function pueScene(s) {
  const p = s.pue ?? 1.25,
    it = 100 / p,
    over = 100 - it;
  let b = txt(61, 61, "FIRST DRAW THE ACCOUNTING BOUNDARY.", "diagram-tiny");
  const w = 727,
    wi = w / p;
  b +=
    rect(86, 167, w, 109, "#513d36", C.hot) +
    rect(86, 167, wi, 109, "#335451", C.green, 0);
  b +=
    txt(111, 210, `${fmt(it, 1)} MW`, "", C.green) +
    txt(111, 247, "IT load", "diagram-small");
  if (over > 8)
    b +=
      txt(86 + wi + (w - wi) / 2, 213, `${fmt(over, 1)}`, "", C.hot, "middle") +
      txt(
        86 + wi + (w - wi) / 2,
        247,
        "overhead MW",
        "diagram-small",
        C.hot,
        "middle",
      );
  b +=
    line("M86 144v-14h727v14", "#879faa", 1) +
    txt(450, 108, "100 MW total facility input", "", C.ink, "middle");
  b += metric(
    90,
    381,
    fmt(p, 2),
    "assumed PUE",
    "100 MW facility ÷ IT MW",
    C.ink,
  );
  b += metric(
    535,
    381,
    fmt(it, 1),
    "MW available to IT",
    "Steady-load illustration",
    C.green,
  );
  return {
    body: b,
    label: "19 / FACILITY POWER ≠ IT POWER",
    tag: "ASSUMED STEADY-LOAD EXAMPLE",
    caption:
      "Formal PUE compares total facility and IT energy over the same continuous 12 months. Shorter periods use interim PUE. Here a fixed assumed ratio translates a steady 100 MW facility budget. It is not a measured site PUE or a guarantee at every load.",
  };
}
function bottleneckScene(s) {
  const cooling = s.cooling ?? 60,
    network = s.network ?? 900,
    pue = s.budgetPue ?? 1.25;
  const bgt = capacityBudget(100, pue, cooling, 100, 900, network, 70);
  let b = txt(
    63,
    60,
    "THE SMALLEST SUPPORTED LOAD SETS THE CEILING.",
    "diagram-tiny",
  );
  const bars = [
    ["Power / PUE", bgt.limits.power, C.power, "power"],
    ["Electrical train", bgt.limits.electrical, C.power, "electrical"],
    ["Cooling", bgt.limits.cooling, C.cold, "cooling"],
    ["Rack positions", 900, C.muted, "space"],
    ["Network limit", network, C.violet, "network"],
  ];
  bars.forEach(([label, n, c, key], j) => {
    const y = 129 + j * 66;
    b += txt(64, y + 17, label, "diagram-small");
    b += rect(
      246,
      y,
      Math.max(1, (Math.min(n, 1100) / 1100) * 438),
      24,
      bgt.binding.includes(key) ? c : `${c}44`,
      "none",
      1,
    );
    b += txt(712, y + 19, fmt(n), "diagram-small", c);
    if (bgt.binding.includes(key))
      b += txt(773, y + 18, "LIMIT", "diagram-tiny", c);
  });
  b += txt(
    450,
    503,
    `${fmt(bgt.supportedRacks)} rack equivalents × 100 kW = ${fmt(bgt.supportedITMW)} MW IT`,
    "",
    C.green,
    "middle",
  );
  return {
    body: b,
    label: "20 / THE CAPACITY LAB",
    tag: "SYNTHETIC DESIGN EXERCISE",
    caption:
      "100 MW facility, assumed PUE, 70 MW downstream electrical capacity, adjustable IT cooling duty, 900 rack positions, and adjustable network limit. Identical 100 kW rack-equivalent loads. This ceiling does not prove commissioned or utilized capacity.",
  };
}
function caseScene(s) {
  const tab = s.caseView ?? 0;
  let b = txt(62, 61, "A REAL CAMPUS. A CAREFUL READING.", "diagram-tiny");
  b +=
    pylon(152, 312, 0.87) +
    transformer(375, 320, 0.98) +
    rack(683, 171, 120, 222, false);
  b +=
    arrow("M200 272H306", C.power, 3) +
    line("M454 287H665", "#8095a4", 2, 'stroke-dasharray="5 8"');
  b +=
    txt(150, 380, "Grid service", "diagram-small", C.power, "middle") +
    txt(386, 380, "Substations", "diagram-small", C.power, "middle") +
    txt(745, 438, "Measured IT load?", "diagram-small", C.ink, "middle");
  b += txt(551, 275, "?", "diagram-number", C.muted, "middle");
  b +=
    rect(75, 89, 720, 53, "#273847", "#496276") +
    txt(
      97,
      122,
      tab === 0
        ? "Dated site evidence establishes individual milestones."
        : "A capacity headline does not establish installed GPU count.",
      "diagram-small",
      tab === 0 ? C.green : C.hot,
    );
  b += txt(
    66,
    495,
    "ABILENE / A HISTORICAL SOURCE-READING EXERCISE",
    "diagram-tiny",
  );
  return {
    body: b,
    label: "21 / READ A CAMPUS ANNOUNCEMENT",
    tag: "HISTORICAL CASE · SEE SOURCES",
    caption:
      "Use the Abilene sources to distinguish interconnection, equipment, commissioning, and actual IT operation. The course makes no current campus-wide power, installed GPU count, utilization, or tokens-per-second estimate.",
  };
}

function compactDiagram(id, state, result) {
  let b = "";
  if (id === "bottleneck") {
    const budget = capacityBudget(
      100,
      state.budgetPue,
      state.cooling,
      100,
      900,
      state.network,
      70,
    );
    const rows = [
      ["Facility / PUE", budget.limits.power, C.power, "power"],
      ["Electrical train", 700, C.power, "electrical"],
      ["Cooling", budget.limits.cooling, C.cold, "cooling"],
      ["Rack positions", 900, C.muted, "space"],
      ["Network", state.network, C.violet, "network"],
    ];
    rows.forEach(([name, n, color, key], j) => {
      const y = 63 + j * 85;
      b +=
        txt(40, y, name, "", color) + txt(555, y, String(n), "", color, "end");
      b +=
        rect(40, y + 18, 515, 16, "#253b4b", "none") +
        rect(40, y + 18, (n / 1100) * 515, 16, color, "none");
      if (budget.binding.includes(key))
        b += txt(555, y + 57, "BINDING LIMIT", "diagram-tiny", color, "end");
    });
    b += txt(
      300,
      546,
      `${budget.supportedRacks} rack equivalents`,
      "diagram-number",
      C.green,
      "middle",
    );
  } else if (id === "voltage") {
    const i = currentThreePhase(100, state.voltage);
    b += txt(
      300,
      63,
      "100 MW · THREE-PHASE · PF 1",
      "diagram-small",
      C.muted,
      "middle",
    );
    b += txt(
      300,
      150,
      `${fmt(state.voltage, 1)} kV`,
      "diagram-number",
      C.power,
      "middle",
    );
    b +=
      pylon(120, 333, 0.9) +
      pylon(480, 333, 0.9) +
      line("M80 244Q300 330 440 244 M160 244Q330 292 520 244", C.power, 3);
    b +=
      txt(60, 418, fmt(i), "diagram-number", C.power) +
      txt(60, 457, "amps / phase", "diagram-small");
    b +=
      txt(
        355,
        418,
        `${fmt(resistiveLossRatio(state.voltage, 13.8) * 100, 1)}%`,
        "diagram-number",
        C.hot,
      ) + txt(355, 457, "relative loss", "diagram-small");
    b += txt(
      300,
      529,
      "Reference: 13.8 kV, same resistance",
      "diagram-small",
      C.muted,
      "middle",
    );
  } else if (id === "liquid") {
    b +=
      chip(64, 154, 186, 162) +
      line("M65 169h167v32H88v33h144v33H88v32h160", C.cold, 8) +
      arrow("M27 169h34", C.cold, 5) +
      arrow("M252 298h66v-75h33", C.hot, 5);
    b +=
      txt(
        447,
        239,
        fmt(coolantFlow(100, state.deltaT), 2),
        "diagram-number",
        C.cold,
        "middle",
      ) + txt(447, 282, "kg/s water", "diagram-small", C.cold, "middle");
    b +=
      txt(
        300,
        75,
        "100 kW INTO THE WATER",
        "diagram-small",
        C.muted,
        "middle",
      ) +
      txt(
        300,
        410,
        `Temperature rise: ${state.deltaT}°C`,
        "",
        C.hot,
        "middle",
      ) +
      txt(300, 491, "Q̇ = ṁ × cₚ × ΔT", "", C.cold, "middle");
  } else if (id === "pue") {
    const it = 100 / state.pue;
    b += txt(
      300,
      77,
      "100 MW FACILITY BUDGET",
      "diagram-small",
      C.muted,
      "middle",
    );
    b +=
      rect(48, 140, 504, 110, "#724d47", C.hot) +
      rect(48, 140, 504 / state.pue, 110, "#456e62", C.green);
    b += txt(67, 203, "IT", "", C.green);
    b +=
      txt(60, 362, fmt(it, 1), "diagram-number", C.green) +
      txt(60, 403, "MW IT", "diagram-small", C.green);
    b +=
      txt(362, 362, fmt(100 - it, 1), "diagram-number", C.hot) +
      txt(362, 403, "MW overhead", "diagram-small", C.hot);
    b += txt(
      300,
      498,
      `Assumed ratio: ${fmt(state.pue, 2)}`,
      "",
      C.muted,
      "middle",
    );
  } else if (id === "energy") {
    b += txt(55, 66, "POWER × TIME = ENERGY", "diagram-small");
    b += line("M65 153V402H547", C.muted, 2);
    const y = 402 - (state.power / 5) * 210,
      x = 65 + (state.hours / 24) * 482;
    b +=
      `<path d="M65 402V${y}H${x}V402Z" fill="#ffc87544"/>` +
      line(`M65 ${y}H${x}`, C.power, 3);
    b +=
      txt(547, 439, "24 hours", "diagram-small", C.muted, "end") +
      txt(65, 439, "0", "diagram-small");
    b += txt(
      300,
      521,
      `${fmt(energyMWh(state.power, state.hours), 1)} MWh`,
      "diagram-number",
      C.power,
      "middle",
    );
  } else if (id === "heat") {
    b += txt(
      300,
      74,
      "STEADY STATE · RACK BOUNDARY",
      "diagram-small",
      C.muted,
      "middle",
    );
    b +=
      rack(229, 176, 142, 220) +
      arrow("M39 286H207", C.power, 10) +
      arrow("M393 286H561", C.hot, 10);
    b +=
      txt(120, 149, "100 kW", "", C.power, "middle") +
      txt(480, 149, "≈100 kW", "", C.hot, "middle");
    b +=
      txt(120, 447, "Electricity", "diagram-small", C.power, "middle") +
      txt(480, 447, "Heat", "diagram-small", C.hot, "middle");
    b += txt(
      300,
      521,
      "Computation happens inside.",
      "diagram-small",
      C.muted,
      "middle",
    );
  } else if (id === "current") {
    const i = rackCurrent(1, state.coreV);
    b +=
      txt(
        300,
        71,
        "SAME IDEAL 1 kW DC LOAD",
        "diagram-small",
        C.muted,
        "middle",
      ) + chip(390, 190, 133, 136);
    b +=
      rect(66, 204, 111, 105, "#293f48", C.muted) +
      arrow("M188 256H370", C.power, 4 + 20 * Math.sqrt(i / 1000));
    b += txt(275, 172, `${state.coreV} V`, "diagram-number", C.power, "middle");
    b +=
      txt(300, 431, `${fmt(i)} A`, "diagram-number", C.power, "middle") +
      txt(300, 497, "I = P / V", "", C.muted, "middle");
  } else return result;
  return { ...result, body: b, compact: true };
}

export function renderDiagram(id, state = {}) {
  const scenes = {
    campus: campusScene,
    energy: energyScene,
    grid: gridScene,
    voltage: voltageScene,
    substation: substationScene,
    capacity: capacityScene,
    train: trainScene,
    "ride-through": rideScene,
    redundancy: redundancyScene,
    failure: failureScene,
    rack: rackScene,
    current: currentScene,
    compute: computeScene,
    heat: heatScene,
    liquid: liquidScene,
    cdu: cduScene,
    air: airScene,
    rejection: rejectionScene,
    pue: pueScene,
    bottleneck: bottleneckScene,
    case: caseScene,
    synthesis: (s) => campusScene(s, true),
  };
  if (!scenes[id]) throw new Error(`Unknown visual: ${id}`);
  const original = scenes[id](state);
  const result = state.compact ? compactDiagram(id, state, original) : original;
  const svg = sv(result.label, result.body);
  return {
    ...result,
    svg: result.compact
      ? svg.replace(
          'viewBox="0 0 900 545"',
          'class="compact-diagram" viewBox="0 0 600 580"',
        )
      : svg,
  };
}
