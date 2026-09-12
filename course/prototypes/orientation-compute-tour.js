const esc = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll('"', "&quot;");
const box = (id, x, y, width, height, options = {}) =>
  `<rect id="tour-${id}" x="${x}" y="${y}" width="${width}" height="${height}" rx="${options.radius ?? 12}" fill="${options.fill ?? "var(--surface)"}" stroke="${options.stroke ?? "var(--line)"}" stroke-width="${options.weight ?? 1.5}"${options.dash ? ' stroke-dasharray="6 6"' : ""}/>`;
const text = (x, y, value, owner, options = {}) =>
  `<text x="${x}" y="${y}" text-anchor="${options.anchor ?? "middle"}" fill="var(--${options.color ?? "text"})" font-size="${options.size ?? 19}" font-weight="${options.weight ?? 500}"${owner ? ` data-label-for="tour-${owner}"` : ""}>${esc(value)}</text>`;
const path = (d, color = "data", options = {}) =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${options.width ?? 3}" stroke-linecap="round" stroke-linejoin="round"${options.dash ? ' stroke-dasharray="5 6"' : ""}${options.arrow ? ` marker-end="url(#tour-${color}-arrow)"` : ""}/>`;
const defs = () =>
  `<defs>${["power", "heat", "data", "muted"].map((color) => `<marker id="tour-${color}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.2" markerHeight="3.2" orient="auto-start-reverse"><path d="M1 1L9 5L1 9Z" fill="var(--${color})"/></marker>`).join("")}</defs>`;

function chip(x, y, size, selected = false) {
  const inset = size * 0.2;
  return (
    `<rect x="${x}" y="${y}" width="${size}" height="${size}" rx="${size * 0.08}" fill="var(--panel)" stroke="var(--${selected ? "data" : "muted"})" stroke-width="${selected ? 2.5 : 1.5}"/>` +
    `<rect x="${x + inset}" y="${y + inset}" width="${size - 2 * inset}" height="${size - 2 * inset}" rx="3" fill="var(--surface)" stroke="var(--${selected ? "data" : "line"})"/>` +
    [0.3, 0.5, 0.7]
      .map((at) =>
        path(
          `M${x - 5} ${y + at * size}h5M${x + size} ${y + at * size}h5M${x + at * size} ${y - 5}v5M${x + at * size} ${y + size}v5`,
          selected ? "data" : "muted",
          { width: 1.5 },
        ),
      )
      .join("")
  );
}

function tray(x, y, width, height, selected = false) {
  const s = Math.min(height * 0.43, width * 0.25);
  return (
    `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="5" fill="var(--panel)" stroke="var(--${selected ? "data" : "muted"})" stroke-width="${selected ? 2.5 : 1.5}"/>` +
    path(
      `M${x + 12} ${y + height - 12}H${x + width - 12}M${x + width * 0.49} ${y + 12}V${y + height - 12}`,
      "line",
      { width: 2 },
    ) +
    chip(x + width * 0.18, y + height * 0.25, s, true) +
    `<rect x="${x + width * 0.68}" y="${y + height * 0.19}" width="${width * 0.16}" height="${height * 0.62}" rx="2" fill="var(--surface)" stroke="var(--line)"/>`
  );
}

function rack(x, y, width, height, selected = false, highlightTray = false) {
  const gap = height * 0.05;
  const trayHeight = (height - 5 * gap) / 4;
  return (
    `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="5" fill="var(--panel)" stroke="var(--${selected ? "data" : "muted"})" stroke-width="${selected ? 2.5 : 1.5}"/>` +
    [0, 1, 2, 3]
      .map((i) => {
        const sy = y + gap + i * (trayHeight + gap);
        return `<rect x="${x + width * 0.13}" y="${sy}" width="${width * 0.74}" height="${trayHeight}" rx="2" fill="var(--surface)" stroke="var(--${highlightTray && i === 1 ? "data" : "line"})" stroke-width="${highlightTray && i === 1 ? 2.5 : 1}"/><path d="M${x + width * 0.2} ${sy + trayHeight * 0.35}h${width * 0.42}m${-width * 0.42} ${trayHeight * 0.26}h${width * 0.42}" stroke="var(--line)"/><circle cx="${x + width * 0.77}" cy="${sy + trayHeight * 0.5}" r="${width * 0.025}" fill="var(--data)"/>`;
      })
      .join("")
  );
}

function switchIcon(x, y, width, height) {
  return (
    `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="4" fill="var(--surface)" stroke="var(--data)" stroke-width="2"/>` +
    [0, 1, 2, 3]
      .map(
        (i) =>
          `<rect x="${x + width * (0.13 + i * 0.19)}" y="${y + height * 0.34}" width="${width * 0.1}" height="${height * 0.32}" fill="var(--data)" opacity="0.65"/>`,
      )
      .join("")
  );
}

function computeScale(compact) {
  const names = ["Chip", "Compute tray", "Rack", "Cluster"];
  if (compact) {
    let out = "";
    names.forEach((name, i) => {
      const y = 18 + i * 175;
      out += box(`scale-${i}`, 20, y, 350, 153);
      out += text(256, y + 73, name, `scale-${i}`, { size: 22, weight: 650 });
      if (i === 0) out += chip(64, y + 38, 75, true);
      if (i === 1) out += tray(37, y + 41, 144, 73);
      if (i === 2) out += rack(74, y + 17, 65, 120, false, true);
      if (i === 3) {
        out += [0, 1, 2]
          .map((j) => rack(37 + j * 49, y + 22, 40, 78, j === 0))
          .join("");
        out += path(`M57 ${y + 100}v12h98v-12M106 ${y + 100}v24`, "data", {
          width: 2,
        });
        out += switchIcon(80, y + 123, 52, 15);
        out += text(256, y + 99, "Networked racks", `scale-${i}`, {
          size: 14,
          color: "data",
        });
      }
      if (i < 3)
        out += path(`M195 ${y + 156}v13`, "muted", { width: 2, arrow: true });
    });
    return out;
  }
  let out = "";
  names.forEach((name, i) => {
    const x = 22 + i * 290;
    out += box(`scale-${i}`, x, 65, 248, 463);
    out += text(x + 124, 112, name, `scale-${i}`, { size: 26, weight: 650 });
    if (i === 0) out += chip(x + 52, 239, 144, true);
    if (i === 1) out += tray(x + 24, 236, 200, 134);
    if (i === 2) out += rack(x + 64, 169, 120, 294, false, true);
    if (i === 3) {
      out += [0, 1, 2]
        .map((j) => rack(x + 19 + j * 74, 222, 61, 172, j === 0))
        .join("");
      out += path(`M${x + 49} 394v35h148v-35M${x + 123} 394v51`, "data");
      out += switchIcon(x + 89, 446, 69, 25);
      out += text(x + 124, 502, "Networked racks", `scale-${i}`, {
        size: 18,
        color: "data",
      });
    }
    if (i < 3)
      out += path(`M${x + 254} 296h28`, "muted", { width: 2.5, arrow: true });
  });
  return out;
}

function storage(x, y, width, height) {
  return (
    `<path d="M${x} ${y + 9}v${height - 18}a${width / 2} 9 0 0 0 ${width} 0V${y + 9}" fill="var(--panel)" stroke="var(--muted)" stroke-width="1.5"/>` +
    `<ellipse cx="${x + width / 2}" cy="${y + 9}" rx="${width / 2}" ry="9" fill="var(--surface)" stroke="var(--muted)" stroke-width="1.5"/>` +
    path(
      `M${x} ${y + height * 0.45}a${width / 2} 9 0 0 0 ${width} 0M${x} ${y + height * 0.7}a${width / 2} 9 0 0 0 ${width} 0`,
      "line",
      { width: 1.5 },
    )
  );
}

function internalRack(x, y, width, height) {
  const size = width * 0.21;
  const left = x + width * 0.16;
  const right = x + width * 0.63;
  const top = y + height * 0.22;
  const bottom = y + height * 0.6;
  return (
    `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="7" fill="var(--panel)" stroke="var(--muted)" stroke-width="1.5"/>` +
    path(
      `M${left + size / 2} ${top + size / 2}H${right + size / 2}V${bottom + size / 2}H${left + size / 2}Z`,
      "data",
    ) +
    [
      chip(left, top, size),
      chip(right, top, size),
      chip(left, bottom, size),
      chip(right, bottom, size),
    ].join("")
  );
}

function networkPreview(compact) {
  if (compact) {
    let out = box("network-campus", 14, 16, 362, 458);
    out += text(195, 45, "Inside the campus", "network-campus", {
      size: 18,
      color: "muted",
    });
    out += internalRack(33, 85, 136, 168);
    out += text(101, 75, "Scale-up", "network-campus", {
      size: 19,
      weight: 650,
    });
    out += text(101, 277, "Within a rack", "network-campus", { size: 14 });
    out += text(286, 75, "Scale-out", "network-campus", {
      size: 19,
      weight: 650,
    });
    out += rack(214, 104, 55, 115) + rack(304, 104, 55, 115);
    out += path("M241 219v17h91v-17M286 236v12", "data");
    out += switchIcon(258, 247, 56, 20);
    out += text(286, 290, "Across racks", "network-campus", { size: 14 });
    out += path("M169 85L214 104M169 253L214 219", "muted", {
      width: 1.5,
      dash: true,
    });
    out += path(
      "M241 219v12h-36v94h144v-68h-35M193 325h12M193 325v34h71",
      "data",
      {
        width: 2,
        dash: true,
      },
    );
    out += switchIcon(162, 348, 63, 22);
    out += storage(268, 339, 64, 54);
    out += text(157, 404, "Storage network", "network-campus", { size: 18 });
    out += text(300, 417, "Storage", "network-campus", { size: 14 });
    out += path("M347 219h17v227H195v44", "data", { width: 2.5 });
    out += box("network-handoff", 83, 490, 224, 61, { stroke: "var(--data)" });
    out += text(195, 515, "Campus edge", "network-handoff", {
      size: 19,
      weight: 650,
    });
    out += text(195, 537, "Carrier handoff", "network-handoff", { size: 14 });
    out += path("M195 551v38", "data", { width: 3 });
    out += box("network-wan", 47, 589, 296, 91, { fill: "var(--panel)" });
    out += text(195, 624, "Carrier / wide-area network", "network-wan", {
      size: 18,
      weight: 650,
    });
    out += text(195, 653, "Other sites and users", "network-wan", { size: 16 });
    return out;
  }
  let out = box("network-campus", 20, 40, 818, 515);
  out += text(52, 79, "Inside the campus", "network-campus", {
    size: 20,
    color: "muted",
    anchor: "start",
  });
  out += text(174, 133, "Scale-up", "network-campus", {
    size: 24,
    weight: 650,
  });
  out += internalRack(80, 153, 188, 235);
  out += text(174, 416, "Within a rack", "network-campus", { size: 18 });
  out += text(465, 133, "Scale-out", "network-campus", {
    size: 24,
    weight: 650,
  });
  out +=
    rack(340, 168, 76, 175) + rack(448, 168, 76, 175) + rack(556, 168, 76, 175);
  out += path("M378 343v32h216v-32M486 343v48", "data");
  out += switchIcon(448, 391, 77, 29);
  out += text(486, 448, "Across racks", "network-campus", { size: 18 });
  out += path("M268 153L340 168M268 388L340 343", "muted", {
    width: 1.5,
    dash: true,
  });
  out += storage(713, 178, 78, 96);
  out += text(752, 308, "Storage", "network-campus", { size: 19 });
  out += path("M791 223h20v135H486V343M594 343v15M378 343v15", "data", {
    width: 2,
    dash: true,
  });
  out += switchIcon(715, 346, 74, 25);
  out += text(722, 404, "Storage", "network-campus", { size: 18 });
  out += text(722, 428, "network", "network-campus", { size: 18 });
  out += path("M525 405h83v92h61", "data", { width: 3 });
  out += box("network-handoff", 669, 458, 147, 77, { stroke: "var(--data)" });
  out += text(742.5, 488, "Campus edge", "network-handoff", {
    size: 18,
    weight: 650,
  });
  out += text(742.5, 514, "Carrier handoff", "network-handoff", { size: 15 });
  out += path("M816 497h156V379", "data", { width: 4 });
  out += text(975, 101, "Outside the campus", null, {
    size: 19,
    color: "muted",
  });
  out += box("network-wan", 882, 189, 252, 190, { fill: "var(--panel)" });
  out += text(1008, 236, "Carrier /", "network-wan", { size: 23, weight: 650 });
  out += text(1008, 269, "wide-area network", "network-wan", {
    size: 23,
    weight: 650,
  });
  out += text(1008, 326, "Other sites and users", "network-wan", { size: 18 });
  return out;
}

function fan(cx, cy, radius) {
  return `<circle cx="${cx}" cy="${cy}" r="${radius}" fill="var(--surface)" stroke="var(--muted)" stroke-width="1.5"/>${[0, 120, 240].map((angle) => `<path transform="rotate(${angle} ${cx} ${cy})" d="M${cx} ${cy}q${-radius * 0.1} ${-radius * 0.95} ${radius * 0.55} ${-radius * 0.55}q${radius * 0.4} ${radius * 0.55} ${-radius * 0.55} ${radius * 0.55}" fill="var(--muted)" opacity="0.65"/>`).join("")}<circle cx="${cx}" cy="${cy}" r="${radius * 0.16}" fill="var(--text)"/>`;
}

function coolingPreview(compact) {
  if (compact) {
    let out = box("cooling-rack", 74, 18, 242, 135);
    out += text(195, 48, "Chips and cold plates", "cooling-rack", {
      size: 19,
      weight: 650,
    });
    out += chip(127, 68, 40) + chip(224, 68, 40);
    out += path("M146 109v10M244 109v10", "heat", { width: 3, arrow: true });
    out += path("M110 153v-26h170v26", "power", { width: 6 });
    out += text(195, 218, "Technology", null, { size: 20 });
    out += text(195, 245, "coolant", null, { size: 20 });
    out += box("cooling-cdu", 70, 288, 250, 159);
    out += text(195, 309, "Cooling distribution unit", "cooling-cdu", {
      size: 17,
      weight: 650,
    });
    out += text(195, 329, "CDU · heat exchanger", "cooling-cdu", { size: 14 });
    out += path("M280 153V270H345V337H280", "heat", { width: 5, arrow: true });
    out += path("M110 337H45V270H110V158", "power", { width: 5, arrow: true });
    out += path("M110 565V470H45V412H110", "power", { width: 5, arrow: true });
    out += path("M280 412H345V470H280V560", "heat", { width: 5, arrow: true });
    out += path("M110 337h170", "heat", { width: 10 });
    out += path("M110 412h170", "power", { width: 10 });
    out += path("M90 374h210", "line", { width: 3 });
    out += path("M172 351v43M218 351v43", "heat", { width: 3, arrow: true });
    out += text(195, 440, "Separate fluid circuits", "cooling-cdu", {
      size: 14,
      color: "muted",
    });
    out += text(195, 508, "Facility", null, { size: 20 });
    out += text(195, 535, "coolant", null, { size: 20 });
    out += box("cooling-outdoor", 72, 565, 246, 110);
    out += text(195, 590, "Outdoor", "cooling-outdoor", {
      size: 18,
      weight: 650,
    });
    out += text(195, 614, "heat rejection", "cooling-outdoor", {
      size: 18,
      weight: 650,
    });
    out += path("M110 565v70h170v-70", "power", { width: 4 });
    out += path("M280 565v28", "heat", { width: 4 });
    out += fan(145, 648, 16) + fan(245, 648, 16);
    out += path("M195 677v15", "heat", { width: 4, arrow: true });
    out += text(195, 716, "Atmosphere", null, { size: 17, color: "heat" });
    return out;
  }
  let out = box("cooling-rack", 35, 172, 221, 305);
  out += text(145.5, 210, "Compute rack", "cooling-rack", {
    size: 24,
    weight: 650,
  });
  out += chip(63, 258, 56) + chip(63, 358, 56);
  out += path("M123 286h36M123 386h36", "heat", { width: 4, arrow: true });
  out += path("M255 392H191V263h64", "power", { width: 8 });
  out += text(146, 451, "Chips → cold plates", "cooling-rack", { size: 17 });
  out += text(371, 167, "Technology coolant", null, { size: 21, weight: 600 });
  out += path("M256 263H492", "heat", { width: 6, arrow: true });
  out += path("M492 392H263", "power", { width: 6, arrow: true });
  out += box("cooling-cdu", 490, 170, 215, 307);
  out += text(597.5, 205, "Cooling distribution unit", "cooling-cdu", {
    size: 16,
    weight: 650,
  });
  out += text(597.5, 236, "CDU · heat exchanger", "cooling-cdu", { size: 18 });
  out += path("M492 263h58v129h-58", "heat", { width: 9 });
  out += path("M705 392h-62V263h62", "power", { width: 9 });
  out += path("M595 253v154", "line", { width: 3 });
  out += path("M566 301h61M566 355h61", "heat", { width: 3, arrow: true });
  out += text(597.5, 452, "Separate fluid circuits", "cooling-cdu", {
    size: 15,
    color: "muted",
  });
  out += text(818, 167, "Facility coolant", null, { size: 21, weight: 600 });
  out += path("M705 263H927", "heat", { width: 6, arrow: true });
  out += path("M927 392H714", "power", { width: 6, arrow: true });
  out += box("cooling-outdoor", 927, 170, 199, 307);
  out += text(1026.5, 208, "Outdoor", "cooling-outdoor", {
    size: 22,
    weight: 650,
  });
  out += text(1026.5, 236, "heat rejection", "cooling-outdoor", {
    size: 22,
    weight: 650,
  });
  out += fan(986, 333, 28) + fan(1065, 333, 28);
  out += path("M928 263h177v129H928", "power", { width: 4 });
  out += path("M928 263h177v52", "heat", { width: 4 });
  out += path("M995 169V139M1058 169V139", "heat", { width: 4, arrow: true });
  out += text(1026.5, 119, "Atmosphere", null, { size: 22, color: "heat" });
  out += path("M372 540h39", "power", { width: 5 });
  out += text(422, 546, "Cooler supply", null, { size: 18, anchor: "start" });
  out += path("M610 540h39", "heat", { width: 5 });
  out += text(660, 546, "Warmer return", null, { size: 18, anchor: "start" });
  return out;
}

export function renderComputeTour(id, state = {}, compact = false) {
  const renderers = {
    "compute-scale": computeScale,
    "network-preview": networkPreview,
    "cooling-preview": coolingPreview,
  };
  if (!renderers[id]) return "";
  return `${defs()}<g data-tour-scene="${id}">${renderers[id](compact)}</g>`;
}
