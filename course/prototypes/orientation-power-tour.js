/* Functional overview diagrams; not wiring layouts or prescribed site topologies. */
const esc = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll('"', "&quot;");
const text = (x, y, value, options = {}) =>
  `<text x="${x}" y="${y}" text-anchor="${options.anchor || "middle"}" font-size="${options.size || 20}" font-weight="${options.weight || 500}" fill="var(--${options.color || "text"})"${options.owner ? ` data-label-for="tour-${options.owner}"` : ""}>${esc(value)}</text>`;
const box = (id, x, y, w, h, options = {}) =>
  `<rect id="tour-${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${options.radius ?? 12}" fill="var(--${options.fill || "surface"})" stroke="var(--${options.color || "line"})" stroke-width="${options.width || 1.5}"${options.dash ? ' stroke-dasharray="7 6"' : ""}/>`;
const wire = (d, options = {}) =>
  `<path d="${d}" fill="none" stroke="var(--${options.color || "power"})" stroke-width="${options.width || 4}" stroke-linejoin="round" stroke-linecap="round"${options.dash ? ' stroke-dasharray="7 6"' : ""}${options.arrow === false ? "" : ' marker-end="url(#tour-arrow)"'}/>`;
const dot = (x, y) => `<circle cx="${x}" cy="${y}" r="5" fill="var(--power)"/>`;
const defs =
  '<defs><marker id="tour-arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="3.3" markerHeight="3.3" orient="auto"><path d="M1 1L9 5L1 9Z" fill="var(--power)"/></marker></defs>';
const artwork = (x, y, width, content) =>
  `<g transform="translate(${x} ${y}) scale(${width / 160})" fill="var(--panel)" stroke="var(--text)" stroke-width="2.5" stroke-linejoin="round" stroke-linecap="round">${content}</g>`;

function thermal(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<path d="M18 123V67H48V50H98V69H141V123Z"/><path d="M108 69V18H121V69M130 69V35H141V69"/><path d="M27 80H45V95H27ZM58 65H86V84H58ZM108 84H129V103H108Z" fill="var(--surface)"/><path d="M57 123V96H91V123M8 124H151"/>',
  );
}
function wind(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<path d="M76 61L70 127H88L82 61"/><path d="M79 51L85 7Q67 9 74 49Z"/><path d="M73 56L30 76Q36 90 78 63Z"/><path d="M85 56L115 88Q124 74 90 50Z"/><circle cx="80" cy="55" r="9" fill="var(--power)" stroke="var(--power)"/><path d="M43 128H114"/>',
  );
}
function solar(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<circle cx="127" cy="22" r="13" stroke="var(--heat)" fill="none"/><path d="M127 1V4M148 22H152M111 6L114 9M143 6L140 9" stroke="var(--heat)"/><path d="M29 49H136L119 103H12Z" fill="var(--surface)"/><path d="M64 49L47 103M100 49L83 103M24 67H130M18 85H124" stroke="var(--power)" stroke-width="2"/><path d="M50 104L47 128M103 104L108 128M33 129H122"/>',
  );
}
function hydro(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<path d="M18 41H71M10 51H71M19 61H71" stroke="var(--data)"/><path d="M76 18H94L119 121H56Z"/><path d="M94 52Q137 61 137 110" fill="none" stroke="var(--power)" stroke-width="5"/><circle cx="135" cy="116" r="12" fill="var(--surface)"/><path d="M135 106V126M125 116H145M10 130Q29 121 46 130T82 130M116 134H154" stroke="var(--power)"/>',
  );
}
function generator(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<rect x="28" y="26" width="109" height="91" rx="12"/><path d="M13 68H28M41 118V130H125V118M113 37V107"/><circle cx="72" cy="71" r="29" fill="var(--surface)"/><path d="M50 72C59 49 65 49 72 72S88 95 96 72" fill="none" stroke="var(--power)" stroke-width="3"/>',
  );
}
function transformer(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<rect x="31" y="34" width="99" height="84" rx="6"/><path d="M49 34V16M76 34V16M109 34V16M43 21H55M70 21H82M103 21H115M20 121H141M42 122V130M119 122V130"/><path d="M57 50C76 50 76 64 57 64C76 64 76 78 57 78C76 78 76 92 57 92C76 92 76 106 57 106M103 50C84 50 84 64 103 64C84 64 84 78 103 78C84 78 84 92 103 92C84 92 84 106 103 106" fill="none" stroke="var(--power)" stroke-width="3"/><path d="M78 47V110M83 47V110"/>',
  );
}
function tower(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<path d="M79 7L112 142M79 7L46 142M64 69H95M58 95H101M53 118H107M45 142L102 95L64 69L86 35M113 142L58 95L95 69L72 35" fill="none"/><path d="M38 37H122M25 61H135M42 37V49M117 37V49M31 61V74M129 61V74M36 143H121"/>',
  );
}
function building(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<path d="M15 123V39H145V123ZM10 34H150"/><path d="M23 30V18H62V30M90 30V18H133V30"/><rect x="33" y="57" width="40" height="66" rx="3" fill="var(--surface)"/><rect x="84" y="57" width="40" height="66" rx="3" fill="var(--surface)"/><path d="M40 71H65M92 71H116M41 86H49M93 86H101M42 109H63M93 109H115" stroke="var(--power)" stroke-width="3"/><path d="M7 128H153"/>',
  );
}
function rack(x, y, width) {
  return artwork(
    x,
    y,
    width,
    '<rect x="34" y="5" width="92" height="136" rx="7"/><path d="M44 16H116V41H44ZM44 47H116V72H44ZM44 78H116V103H44ZM44 109H116V130H44Z" fill="var(--surface)"/><path d="M56 29H97M56 60H97M56 91H97M56 120H97" stroke="var(--power)"/><path d="M27 143H133"/>',
  );
}

function generation(compact) {
  const sources = [
    { label: "Thermal", draw: thermal },
    { label: "Wind", draw: wind },
    { label: "Solar", draw: solar },
    { label: "Hydro", draw: hydro },
  ];
  let content = "";
  if (compact) {
    const positions = [
      [42, 32],
      [220, 32],
      [42, 226],
      [220, 226],
    ];
    for (let i = 0; i < sources.length; i++) {
      const [x, y] = positions[i];
      content += sources[i].draw(x, y, 128);
      content += text(x + 64, y + 130, sources[i].label, { size: 20 });
    }
    content +=
      wire("M106 177V195H195V430", { arrow: false }) +
      wire("M284 177V195H195", { arrow: false });
    content +=
      wire("M106 372V410H195", { arrow: false }) +
      wire("M284 372V410H195", { arrow: false });
    content += dot(195, 195) + dot(195, 410) + wire("M195 430V471");
    content +=
      tower(130, 479, 130) +
      text(195, 647, "Electricity grid", { size: 25, weight: 600 });
  } else {
    const centers = [166, 442, 718, 994];
    sources.forEach((source, i) => {
      const x = centers[i];
      content +=
        source.draw(x - 80, 83, 160) + text(x, 261, source.label, { size: 24 });
      content += wire(`M${x} 284V346`, { arrow: false });
    });
    content +=
      wire("M166 346H994", { arrow: false }) +
      dot(580, 346) +
      wire("M580 346V395");
    content +=
      tower(528, 405, 104) +
      text(580, 543, "Electricity grid", { size: 28, weight: 600 });
  }
  return content;
}

function transmission(compact) {
  if (compact) {
    return (
      generator(33, 18, 120) +
      text(262, 76, "Generator", { size: 22 }) +
      wire("M93 131V175") +
      transformer(33, 181, 120) +
      text(259, 217, "Step up", { size: 22, weight: 600 }) +
      text(259, 245, "Raise voltage", { size: 17, color: "muted" }) +
      wire("M93 290V331") +
      tower(30, 340, 126) +
      text(263, 385, "Transmission", { size: 21, weight: 600 }) +
      text(263, 413, "High voltage", { size: 17, color: "power" }) +
      wire("M93 459V504") +
      transformer(33, 515, 120) +
      text(263, 550, "Step down", { size: 22, weight: 600 }) +
      text(263, 578, "Lower voltage", { size: 17, color: "muted" }) +
      text(195, 671, "Receiving substation", { size: 23, weight: 600 })
    );
  }
  let content =
    generator(36, 216, 156) +
    transformer(267, 216, 156) +
    transformer(944, 216, 156);
  content += wire("M193 285H272") + wire("M426 285H474");
  content += tower(487, 143, 180) + tower(705, 143, 180);
  content +=
    '<path d="M473 224Q581 247 690 224T906 224M473 243Q581 267 690 243T906 243M473 262Q581 286 690 262T906 262" fill="none" stroke="var(--power)" stroke-width="3"/>';
  content += wire("M906 285H951");
  content += text(114, 395, "Generator", { size: 23 });
  content +=
    text(345, 395, "Step up", { size: 25, weight: 600 }) +
    text(345, 428, "Raise voltage", { size: 19, color: "muted" });
  content += text(690, 395, "High-voltage transmission", {
    size: 23,
    weight: 600,
  });
  content +=
    text(1022, 395, "Step down", { size: 25, weight: 600 }) +
    text(1022, 428, "Lower voltage", { size: 19, color: "muted" });
  content += text(224, 114, "POWER PLANT", {
    size: 17,
    color: "muted",
    weight: 650,
  });
  content +=
    text(1022, 114, "RECEIVING", { size: 17, color: "muted", weight: 650 }) +
    text(1022, 138, "SUBSTATION", { size: 17, color: "muted", weight: 650 });
  return content;
}

function campus(compact) {
  if (compact) {
    let content = box("campus", 14, 174, 362, 518, {
      fill: "panel",
      dash: true,
    });
    content += text(195, 204, "ILLUSTRATIVE CAMPUS", {
      size: 14,
      color: "muted",
      owner: "campus",
      weight: 650,
    });
    content +=
      tower(22, 17, 107) + text(244, 80, "Utility connection", { size: 22 });
    content += wire("M76 120V215") + transformer(23, 221, 107);
    content +=
      text(245, 255, "Campus", { size: 21 }) +
      text(245, 283, "substation", { size: 21 });
    content += wire("M76 310V409");
    content +=
      generator(244, 318, 86) +
      text(281, 418, "On-site generation", { size: 16 }) +
      text(281, 439, "Optional", { size: 14, color: "muted" });
    content += wire("M250 355H76", { dash: true }) + dot(76, 355);
    content +=
      building(23, 413, 107) +
      text(246, 475, "Building distribution", { size: 18 });
    content +=
      wire("M76 501V547") +
      rack(23, 554, 107) +
      text(244, 613, "Rack supplies", { size: 22 });
    return content;
  }
  let content = box("campus", 226, 77, 907, 486, { fill: "panel", dash: true });
  content += text(261, 111, "ILLUSTRATIVE CAMPUS", {
    size: 16,
    anchor: "start",
    color: "muted",
    owner: "campus",
    weight: 650,
  });
  content +=
    tower(33, 198, 155) +
    transformer(273, 217, 155) +
    building(595, 217, 155) +
    rack(934, 195, 155);
  content += wire("M180 281H273") + wire("M428 281H595") + wire("M750 281H966");
  content +=
    text(110, 380, "Utility", { size: 24 }) +
    text(110, 410, "connection", { size: 24 });
  content +=
    text(350, 380, "Campus", { size: 24 }) +
    text(350, 410, "substation", { size: 24 });
  content += text(673, 380, "Building distribution", { size: 24 });
  content += text(1012, 380, "Rack supplies", { size: 24 });
  content +=
    generator(435, 426, 103) +
    wire("M486 442V281", { dash: true }) +
    dot(486, 281);
  content += text(571, 479, "Optional on-site generation", {
    size: 20,
    anchor: "start",
  });
  return content;
}

function component(id, x, y, w, h, names, size = 17) {
  const gap = size + 5;
  return (
    box(id, x, y, w, h, { color: "power", radius: 8 }) +
    names
      .map((name, i) =>
        text(
          x + w / 2,
          y + h / 2 + size * 0.35 + (i - (names.length - 1) / 2) * gap,
          name,
          { size, owner: id },
        ),
      )
      .join("")
  );
}

function continuity(compact) {
  if (compact) {
    let content = tower(32, 10, 90) + generator(259, 18, 90);
    content +=
      text(77, 111, "Utility", { size: 19 }) +
      text(304, 117, "Generator", { size: 19 });
    content += wire("M77 127V150H152V170") + wire("M304 132V150H238V170");
    content += component(
      "selection",
      105,
      171,
      180,
      70,
      ["Source selection", "utility OR generator"],
      16,
    );
    content += box("ups", 20, 274, 350, 291, {
      fill: "panel",
      color: "power",
      width: 2,
    });
    content += text(195, 306, "Uninterruptible power supply (UPS)", {
      size: 16,
      owner: "ups",
      weight: 650,
      color: "power",
    });
    content += wire("M195 241V258H70V345");
    content += component("rectifier", 44, 345, 107, 62, ["Rectifier"], 17);
    content += component("inverter", 239, 345, 107, 62, ["Inverter"], 17);
    content += wire("M151 376H239") + dot(195, 376);
    content += text(195, 345, "DC link", { size: 16, color: "power" });
    content +=
      component("battery-interface", 148, 424, 94, 36, ["DC/DC"], 17) +
      wire("M195 424V381");
    content +=
      component("battery", 137, 492, 116, 47, ["Battery"], 18) +
      wire("M195 492V460");
    content += wire("M293 407V587H128V598");
    content += rack(78, 599, 100) + text(258, 651, "IT load", { size: 22 });
    return content;
  }
  let content = tower(55, 89, 138) + generator(55, 370, 138);
  content +=
    text(124, 255, "Utility", { size: 25 }) +
    text(124, 531, "Backup generator", { size: 23 });
  content += wire("M193 166H357V261") + wire("M193 434H357V359");
  content += component(
    "selection",
    250,
    262,
    214,
    96,
    ["Source selection", "utility OR generator"],
    18,
  );
  content += box("ups", 508, 117, 421, 410, {
    fill: "panel",
    color: "power",
    width: 2,
  });
  content += text(719, 158, "Uninterruptible power supply (UPS)", {
    size: 21,
    owner: "ups",
    color: "power",
    weight: 650,
  });
  content +=
    wire("M464 310H546") +
    component("rectifier", 546, 270, 119, 80, ["Rectifier"], 21);
  content +=
    component("inverter", 772, 270, 119, 80, ["Inverter"], 21) +
    wire("M665 310H772") +
    dot(719, 310);
  content += text(719, 253, "DC link", { size: 19, color: "power" });
  content +=
    component("battery-interface", 670, 371, 98, 42, ["DC/DC"], 20) +
    wire("M719 371V315");
  content +=
    component("battery", 653, 455, 132, 47, ["Battery"], 22) +
    wire("M719 455V413");
  content +=
    wire("M891 310H1007") +
    rack(972, 247, 138) +
    text(1041, 418, "IT load", { size: 25 });
  return content;
}

export function renderPowerTour(id, _state = {}, compact = false) {
  const renderers = {
    generation,
    transmission,
    "campus-power": campus,
    "continuity-preview": continuity,
  };
  const render = renderers[id];
  if (!render) return "";
  return `<g data-tour-scene="${id}">${defs}${render(compact)}</g>`;
}
