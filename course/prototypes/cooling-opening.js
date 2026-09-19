// The opening compares physical heat paths. Equipment photography is kept
// intact; the adjacent circuits identify the coolant interfaces explicitly.
const REAR = "../assets/references/nvidia-dgx-gb300-rear.png";
const IMMERSION = "../assets/references/2crsi-single-phase-immersion-user.png";
const COLD_PLATES = "../assets/references/cold-plate-assemblies-user.png";
const ABILENE_HALL = "../assets/references/finale-abilene-coolant-pipes.jpg";

const label = (x, y, value, size = 23, color = "ink", anchor = "middle", weight = 550) =>
  `<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" font-weight="${weight}" style="fill:var(--${color})">${value}</text>`;
const rect = (x, y, w, h, fill = "panel", radius = 12) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="var(--${fill})" stroke="var(--line)" stroke-width="1.5"/>`;
const route = (d, color = "tech", arrow = false, dashed = false, width = 4) =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"${dashed ? ' stroke-dasharray="8 7"' : ""}${arrow ? ` marker-end="url(#opening-${color})"` : ""}/>`;
const markers = `<defs>${["tech", "facility", "heat", "muted"].map(color => `<marker id="opening-${color}" viewBox="0 0 10 10" refX="8.3" refY="5" markerWidth="3.5" markerHeight="3.5" orient="auto"><path d="M0 0L10 5L0 10Z" fill="var(--${color})"/></marker>`).join("")}</defs>`;

function rack(x, y, w, h, liquid = false) {
  let svg = rect(x, y, w, h, "face", 7);
  const trayHeight = (h - 35) / 4;
  for (let i = 0; i < 4; i++) {
    const ty = y + 13 + i * trayHeight;
    svg += rect(x + 12, ty, w - 24, trayHeight - 7, "panel", 3);
    if (liquid) {
      svg += `<rect x="${x + 25}" y="${ty + 5}" width="${w - 50}" height="${trayHeight - 17}" rx="3" fill="var(--tech)" opacity=".18" stroke="var(--tech)" stroke-width="1.4"/>`;
    } else {
      for (let j = 0; j < 5; j++) {
        const vx = x + 23 + j * (w - 50) / 4;
        svg += route(`M${vx} ${ty + 7}v${trayHeight - 21}`, "muted", false, false, 1.4);
      }
    }
  }
  return svg;
}

// Two separate fluid passages, with heat crossing between them.
function exchanger(x, y, gap = 34, height = 45, left = "tech") {
  return route(`M${x - 22} ${y}H${x}V${y + height}H${x - 22}`, left)
    + route(`M${x + gap + 22} ${y}H${x + gap}V${y + height}H${x + gap + 22}`, "facility")
    + route(`M${x + 7} ${y + height / 2}H${x + gap - 8}`, "heat", true, false, 2.7);
}

function comparisonDesktop() {
  const equipment = (y, liquid) => {
    const cabX = 660, cabY = y + 44, cabW = 234, cabH = 176;
    let svg = label(30, y + 13, liquid ? "COLD PLATES" : "AIR COOLING", 19, liquid ? "tech" : "muted", "start", 700)
      + rack(130, y + 48, 134, 168, liquid)
      + label(197, y + 244, liquid ? "Chip cold plates" : "Air-cooled rack", 22)
      + rect(cabX, cabY, cabW, cabH)
      + label(cabX + cabW / 2, cabY + 30, liquid ? "CDU" : "CRAH", 26, liquid ? "tech" : "ink", "middle", 700)
      + label(cabX + cabW / 2, cabY + 57, liquid ? "Coolant distribution" : "Computer room", 18)
      + label(cabX + cabW / 2, cabY + 86, liquid ? "unit" : "air handler", 18)
      + exchanger(761, cabY + 103, 34, 48, liquid ? "tech" : "muted")
      + route(`M${cabX} ${cabY + 103}H739`, liquid ? "tech" : "heat", false, !liquid)
      + route(`M739 ${cabY + 151}H${cabX}`, liquid ? "tech" : "tech", false, !liquid)
      + route(`M817 ${cabY + 103}H1092`, "facility", true)
      + route(`M1092 ${cabY + 151}H817`, "facility", true)
      + label(1009, cabY + 76, "Facility water", 20, "facility")
      + route(`M264 ${cabY + 103}H653`, liquid ? "tech" : "heat", true, !liquid)
      + route(`M660 ${cabY + 151}H272`, "tech", true, !liquid);
    if (liquid) {
      svg += label(453, cabY + 81, "Technology coolant", 23, "tech")
        + label(453, cabY + 178, "To the cold plates", 18, "tech")
        + route(`M239 ${cabY + 21}V${cabY - 14}H438`, "muted", true, true, 3)
        + label(367, cabY - 28, "Remaining air heat", 18, "muted")
        + label(550, cabY - 7, "CRAH / rear door", 18, "muted", "middle", 700);
    } else {
      svg += label(453, cabY + 80, "Warm air", 23, "heat")
        + label(453, cabY + 178, "Cool air", 23, "tech");
    }
    return svg;
  };
  return {
    viewBox: "0 0 1160 580",
    svg: markers
      + equipment(22, false)
      + route("M30 294H1130", "muted", false, false, .7)
      + equipment(326, true),
  };
}

function comparisonCompact() {
  const row = (y, liquid) => {
    let svg = label(18, y + 23, liquid ? "Cold plates" : "Air cooling", 23, liquid ? "tech" : "ink", "start", 700)
      + rack(18, y + 79, 92, 146, liquid)
      + rect(238, y + 79, 163, 146)
      + label(319, y + 105, liquid ? "CDU" : "CRAH", 25, liquid ? "tech" : "ink", "middle", 700)
      + label(319, y + 130, liquid ? "Coolant distribution" : "Computer room", liquid ? 14.5 : 16)
      + label(319, y + 151, liquid ? "unit" : "air handler", 16)
      + exchanger(300, y + 169, 26, 35, liquid ? "tech" : "muted")
      + route(`M110 ${y + 169}H278`, liquid ? "tech" : "heat", true, !liquid, 3)
      + route(`M278 ${y + 204}H115`, "tech", true, !liquid, 3)
      + route(`M348 ${y + 169}H410V${y + 244}H270`, "facility", true, false, 3)
      + route(`M270 ${y + 270}H391V${y + 204}H348`, "facility", true, false, 3)
      + label(328, y + 298, "Facility water", 18, "facility")
      + label(64, y + 252, liquid ? "Cold plates" : "Rack", 17);
    if (liquid) {
      svg += label(173, y + 115, "Technology", 17, "tech")
        + label(173, y + 137, "coolant", 17, "tech")
        + route(`M77 ${y + 79}V${y + 50}H250`, "muted", true, true, 2.7)
        + label(174, y + 74, "Air heat", 15, "muted")
        + label(324, y + 57, "CRAH / rear door", 15, "muted", "middle", 700);
    } else {
      svg += label(172, y + 145, "Warm air", 17, "heat")
        + label(172, y + 237, "Cool air", 17, "tech");
    }
    return svg;
  };
  return {
    viewBox: "0 0 420 680",
    svg: markers + row(0, false)
      + route("M18 330H402", "muted", false, false, .7)
      + row(353, true),
  };
}

function coldPlateDesktop() {
  const svg = markers
    + `<rect x="8" y="30" width="787" height="459" rx="10" fill="white"/>
       <image data-equipment-photo="cold-plate-assemblies" href="${COLD_PLATES}" x="17" y="39" width="769" height="440" preserveAspectRatio="xMidYMid meet"/>`
    + label(402, 526, "Cold-plate assemblies", 24)
    + label(985, 31, "Facility water", 22, "facility")
    + rect(840, 60, 282, 151)
    + label(980, 91, "CDU", 28, "tech", "middle", 700)
    + route("M1128 117H873V134H1128", "facility")
    + route("M1078 134H1118", "facility", true)
    + route("M1118 117H1078", "facility", true)
    + route("M876 210V176H1082V210", "tech")
    + route("M980 168V143", "heat", true, false, 3)
    + route("M876 211V458", "tech")
    + route("M1082 458V211", "tech")
    + route("M876 226V266", "tech", true)
    + route("M1082 266V226", "tech", true)
    + rect(924, 293, 112, 110, "face", 6)
    + label(980, 328, "Tray", 23)
    + `<rect x="946" y="344" width="69" height="38" rx="5" fill="var(--tech)" opacity=".2" stroke="var(--tech)" stroke-width="2"/>`
    + route("M876 363H946", "tech", true)
    + route("M946 363H1015", "tech", false, false, 3)
    + route("M1015 363H1082", "tech", true)
    + `<circle cx="915" cy="363" r="5" fill="var(--face)" stroke="var(--tech)" stroke-width="2"/>
       <circle cx="1045" cy="363" r="5" fill="var(--face)" stroke="var(--tech)" stroke-width="2"/>`
    + label(993, 270, "Quick disconnects", 18)
    + route("M902 281V351H909", "muted", false, false, 1.5)
    + label(980, 436, "Cold plates", 21)
    + label(876, 493, "Supply", 21, "tech")
    + label(1082, 493, "Return", 21, "tech")
    + label(876, 523, "manifold", 21, "tech")
    + label(1082, 523, "manifold", 21, "tech")
    + label(980, 563, "Technology coolant", 23, "tech");
  return { viewBox: "0 0 1160 580", svg };
}

function coldPlateCompact() {
  const svg = markers
    + label(210, 24, "Cold-plate assemblies", 23)
    + `<rect x="5" y="45" width="410" height="237" rx="9" fill="white"/>
       <image data-equipment-photo="cold-plate-assemblies" href="${COLD_PLATES}" x="10" y="49" width="400" height="228" preserveAspectRatio="xMidYMid meet"/>`
    + rect(142, 316, 203, 123)
    + label(245, 344, "CDU", 27, "tech", "middle", 700)
    + label(75, 326, "Facility", 19, "facility")
    + label(75, 350, "water", 19, "facility")
    + route("M31 372H224V399H31", "facility")
    + route("M42 372H103", "facility", true)
    + route("M103 399H42", "facility", true)
    + route("M267 371V420H181V486H80V643", "tech")
    + route("M340 643V460H315V371H267", "tech")
    + route("M258 389H235", "heat", true, false, 2.5)
    + route("M80 502V539", "tech", true)
    + route("M340 539V502", "tech", true)
    + rect(148, 527, 125, 103, "face", 7)
    + label(211, 556, "Tray", 21)
    + `<rect x="174" y="574" width="74" height="35" rx="5" fill="var(--tech)" opacity=".2" stroke="var(--tech)" stroke-width="2"/>`
    + route("M80 592H174", "tech", true)
    + route("M174 592H248", "tech", false, false, 3)
    + route("M248 592H340", "tech", true)
    + `<circle cx="136" cy="592" r="5" fill="var(--face)" stroke="var(--tech)" stroke-width="2"/>
       <circle cx="285" cy="592" r="5" fill="var(--face)" stroke="var(--tech)" stroke-width="2"/>`
    + label(262, 504, "Quick disconnects", 18)
    + route("M164 512H136V582", "muted", false, false, 1.5)
    + label(210, 657, "Cold plates", 19)
    + label(80, 678, "Supply", 21, "tech")
    + label(340, 678, "Return", 21, "tech")
    + label(80, 708, "manifold", 21, "tech")
    + label(340, 708, "manifold", 21, "tech")
    + label(210, 749, "Technology coolant", 23, "tech");
  return { viewBox: "0 0 420 770", svg };
}

function immersion(compact) {
  if (compact) {
    return {
      viewBox: "0 0 420 595",
      svg: label(210, 29, "Single-phase circuit", 24)
        + `<rect x="4" y="52" width="412" height="235" rx="9" fill="white"/>
           <image data-source-figure="2crsi-single-phase" href="${IMMERSION}" x="10" y="58" width="400" height="223" preserveAspectRatio="xMidYMid meet"/>`
        + label(210, 359, "Single-phase", 27, "tech", "middle", 700)
        + label(210, 398, "Liquid stays liquid", 24)
        + route("M50 443H370", "muted", false, false, .7)
        + label(210, 502, "Two-phase", 27, "heat", "middle", 700)
        + label(210, 541, "Boils, then condenses", 24),
    };
  }
  return {
    viewBox: "0 0 1160 510",
    svg: `<rect x="10" y="12" width="882" height="484" rx="12" fill="white"/>
         <image data-source-figure="2crsi-single-phase" href="${IMMERSION}" x="19" y="20" width="864" height="468" preserveAspectRatio="xMidYMid meet"/>`
      + label(1028, 139, "Single-phase", 25, "tech", "middle", 700)
      + label(1028, 175, "Liquid stays liquid", 20)
      + label(1028, 208, "Shown here", 18, "muted")
      + route("M927 269H1132", "muted", false, false, .7)
      + label(1028, 333, "Two-phase", 25, "heat", "middle", 700)
      + label(1028, 369, "Boils, then condenses", 19),
  };
}

// The manufacturer rear view shows manifolds, not a rear-door exchanger.
// Pair the two mechanisms without identifying the photograph as the latter.
function rearDoorCircuit() {
  const x = 44, y = 132, w = 140, h = 214, doorX = 198;
  return rack(x, y, w, h)
    + rect(doorX, y, 38, h, "face", 5)
    + Array.from({ length: 9 }, (_, i) =>
      route(`M${doorX + 7} ${y + 17 + i * 22}h24`, "facility", false, false, 2.6)).join("")
    + label(306, 147, "Warm", 21, "heat")
    + label(306, 175, "rack air", 21, "heat")
    + route("M156 202H205", "heat", true, false, 5)
    + route("M240 241H354", "tech", true, false, 5)
    + label(306, 276, "Cooled air", 21, "tech")
    + route("M342 381H217V339", "facility", true)
    + route("M217 139V67H342", "facility", true)
    + label(291, 45, "Warm coolant", 20, "facility")
    + label(306, 418, "Coolant supply", 20, "facility")
    + label(217, 474, "Air → coil → coolant", 24);
}

function rearDoorComparison(compact) {
  if (compact) {
    return {
      viewBox: "0 0 420 865",
      svg: markers
        + label(210, 28, "GB300 coolant manifolds", 25, "tech", "middle", 700)
        + `<rect x="5" y="48" width="410" height="238" rx="10" fill="white"/>
           <image data-equipment-photo="gb300-rear" href="${REAR}" x="10" y="53" width="400" height="228" preserveAspectRatio="xMidYMid meet"/>`
        + route("M18 319H402", "muted", false, false, .7)
        + label(210, 365, "Rear-door heat exchanger", 25, "facility", "middle", 700)
        + `<g transform="translate(0 378)">${rearDoorCircuit()}</g>`,
    };
  }
  return {
    viewBox: "0 0 1160 555",
    svg: markers
      + label(369, 31, "GB300 coolant manifolds", 27, "tech", "middle", 700)
      + `<rect x="8" y="73" width="725" height="413" rx="10" fill="white"/>
         <image data-equipment-photo="gb300-rear" href="${REAR}" x="15" y="80" width="711" height="399" preserveAspectRatio="xMidYMid meet"/>`
      + route("M758 15V532", "muted", false, false, .7)
      + label(957, 31, "Rear-door heat exchanger", 25, "facility", "middle", 700)
      + `<g transform="translate(770 55)">${rearDoorCircuit()}</g>`,
  };
}

function abilenePhoto(compact) {
  const width = compact ? 420 : 1160;
  const photoHeight = width * 9 / 16;
  const creditY = photoHeight + (compact ? 28 : 32);
  return {
    viewBox: `0 0 ${width} ${creditY + 12}`,
    svg: `<image data-equipment-photo="abilene-coolant-distribution" href="${ABILENE_HALL}" x="0" y="0" width="${width}" height="${photoHeight}" preserveAspectRatio="xMidYMid meet"/>`
      + `<a href="https://www.oracle.com/news/resources/abilene-campus/" target="_blank" rel="noopener noreferrer" aria-label="Photograph: Oracle Abilene campus media kit">${label(width / 2, creditY, "Photograph: Oracle · Abilene campus", compact ? 16 : 22, "ink", "middle", 400)}</a>`,
  };
}

export function renderCoolingOpening(scene, compact = false) {
  switch (scene.kind) {
    case "capture-comparison": return compact ? comparisonCompact() : comparisonDesktop();
    case "rear-door-comparison": return rearDoorComparison(compact);
    case "immersion-photo": return immersion(compact);
    case "immersion-hardware": return {viewBox:"0 0 1160 653",svg:'<image data-equipment-photo="immersion-tank" href="../assets/references/immersion-tank-user.png" x="0" y="0" width="1160" height="653" preserveAspectRatio="xMidYMid meet"/>'};
    case "coldplate-photo": return compact ? coldPlateCompact() : coldPlateDesktop();
    case "abilene-photo": return abilenePhoto(compact);
    default: return null;
  }
}
