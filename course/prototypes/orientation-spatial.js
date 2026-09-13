/* Exact, intentionally simplified spatial diagrams. Flow lines show functional
 * connections, not a wiring, piping or construction layout. */
const escape = (value) =>
  String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll('"', "&quot;");
const rect = (id, x, y, w, h, options = {}) =>
  `<rect id="ori-${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="${options.radius ?? 12}" fill="${options.fill ?? "var(--panel)"}" stroke="${options.stroke ?? "var(--line)"}" stroke-width="${options.width ?? 1.5}"${options.dash ? ' stroke-dasharray="7 6"' : ""}/>`;
const label = (x, y, value, owner, options = {}) =>
  `<text x="${x}" y="${y}" text-anchor="${options.anchor ?? "middle"}" fill="${options.color ?? "var(--text)"}" font-size="${options.size ?? 18}" font-weight="${options.weight ?? 500}"${owner ? ` data-label-for="ori-${owner}"` : ""}>${escape(value)}</text>`;
const line = (d, color, arrow = false, width = 5) =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round"${arrow ? ` marker-end="url(#ori-${color}-arrow)"` : ""}/>`;
const defs = () =>
  `<defs>${["power", "heat", "data"].map((color) => `<marker id="ori-${color}-arrow" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="3.3" markerHeight="3.3" orient="auto-start-reverse"><path d="M1 1 L9 5 L1 9Z" fill="var(--${color})"/></marker>`).join("")}</defs>`;
const route = (name, selected, content) =>
  `<g data-path="${name}" data-selected="${name === selected}" opacity="${name === selected || selected === "all" ? 1 : 0.17}">${content}</g>`;

function cabinet(id, x, y, w, h, name, small = false) {
  const size = small ? 15 : 20;
  if (small && h < 75)
    return (
      rect(id, x, y, w, h, { radius: 7, fill: "var(--surface)" }) +
      (Array.isArray(name)
        ? name
            .map((part, i) =>
              label(x + w / 2, y + 22 + i * 19, part, id, { size: 15 }),
            )
            .join("")
        : label(x + w / 2, y + h / 2 + 5, name, id, { size: 15 }))
    );
  return (
    rect(id, x, y, w, h, { radius: 7, fill: "var(--surface)" }) +
    label(x + w / 2, y + (small ? 22 : 26), name, id, { size }) +
    [0, 1, 2]
      .map(
        (i) =>
          `<path d="M${x + 13} ${y + h - 16 - i * 7}H${x + w - 13}" stroke="var(--line)" stroke-width="2"/>`,
      )
      .join("") +
    `<circle cx="${x + w - 12}" cy="${y + h - 43}" r="2.5" fill="var(--muted)"/>`
  );
}

function rackGroup(compact) {
  const x = compact ? 43 : 373,
    y = compact ? 406 : 225;
  const w = compact ? 204 : 289,
    h = compact ? 210 : 255;
  return (
    rect("racks", x, y, w, h, { fill: "var(--surface)", radius: 10 }) +
    label(x + w / 2, y + 29, "Compute racks", "racks", {
      size: compact ? 17 : 20,
    }) +
    [0, 1, 2]
      .map((i) => {
        const bx = x + (compact ? 11 : 15) + i * (compact ? 61 : 89);
        const by = y + (compact ? 48 : 66),
          bw = compact ? 53 : 76,
          bh = compact ? 143 : 169;
        return (
          rect(`rack-${i}`, bx, by, bw, bh, {
            fill: "var(--panel)",
            radius: 5,
          }) +
          [0, 1, 2, 3, 4]
            .map((slot) => {
              const sy = by + 11 + slot * (compact ? 24 : 28);
              return `<rect x="${bx + 7}" y="${sy}" width="${bw - 14}" height="${compact ? 17 : 20}" rx="2" fill="var(--surface)" stroke="var(--line)"/><circle cx="${bx + bw - 13}" cy="${sy + 8}" r="1.8" fill="var(--muted)"/>`;
            })
            .join("")
        );
      })
      .join("")
  );
}

function cdu(compact, location, named) {
  const hall = location === "hall";
  const x = compact ? (hall ? 267 : 218) : hall ? 692 : 892;
  const y = compact ? (hall ? 493 : 201) : 335;
  const w = compact ? (hall ? 89 : 134) : hall ? 112 : 145;
  const h = compact ? (hall ? 102 : 91) : 105;
  return (
    `<g data-cdu-location="${location}">` +
    rect("cdu", x, y, w, h, {
      fill: "var(--surface)",
      stroke: "var(--heat)",
      width: 2,
    }) +
    (named
      ? label(x + w / 2, y + 26, "CDU", "cdu", {
          size: compact ? 17 : 22,
          weight: 650,
        })
      : ["Cooling", "interface"]
          .map((part, i) =>
            label(
              x + w / 2,
              y + (compact ? 23 : 28) + i * (compact ? 19 : 23),
              part,
              "cdu",
              { size: compact ? 16 : 20, weight: 600 },
            ),
          )
          .join("")) +
    `<g transform="translate(0 ${named ? 0 : compact ? 11 : 17})"><path d="M${x + w / 2 - 16} ${y + 47}h13v25h-13zM${x + w / 2 + 3} ${y + 47}h13v25h-13z" fill="none" stroke="var(--heat)" stroke-width="2"/><path d="M${x + w / 2 - 3} ${y + 50}l6 6-6 6 6 6" fill="none" stroke="var(--muted)" stroke-width="1.5"/></g>` +
    `</g>`
  );
}

function room(id, x, y, w, h, names, space, compact, spaces) {
  const titleY = y + (compact ? 27 : 34);
  return (
    rect(id, x, y, w, h, {
      fill: id === "it-hall" ? "var(--surface)" : "var(--panel)",
      stroke: spaces && id === "it-hall" ? "var(--text)" : "var(--line)",
      width: spaces && id === "it-hall" ? 2.5 : 1.5,
    }) +
    names
      .map((name, index) =>
        label(x + w / 2, titleY + index * 21, name, id, {
          size: compact ? 17 : 20,
          weight: 600,
        }),
      )
      .join("") +
    (spaces
      ? label(x + w / 2, y + h - (compact ? 9 : 18), space, id, {
          size: compact ? 12 : 14,
          weight: 650,
          color: "var(--muted)",
        })
      : "")
  );
}

function floorPlan(state, compact, spaces) {
  const selected = spaces
    ? "all"
    : ["power", "heat", "data"].includes(state.path)
      ? state.path
      : "power";
  const location = spaces && state.cduLocation === "hall" ? "hall" : "gallery";
  const badge = (id, x, y, w, h, text, color) =>
    rect(id, x, y, w, h, { fill: "var(--surface)", radius: 8 }) +
    label(x + w / 2, y + h / 2 + 6, text, id, {
      color: `var(--${color})`,
      size: compact ? 15 : 19,
      weight: 600,
    });
  let out = defs();
  if (compact) {
    out += room(
      "electrical-room",
      18,
      99,
      162,
      219,
      ["Electrical", "room"],
      "GRAY SPACE",
      true,
      spaces,
    );
    out += room(
      "mechanical-gallery",
      199,
      99,
      173,
      219,
      ["Mechanical", "gallery"],
      "GRAY SPACE",
      true,
      spaces,
    );
    out += room(
      "it-hall",
      18,
      340,
      354,
      325,
      ["IT hall"],
      "WHITE SPACE",
      true,
      spaces,
    );
    out += route(
      "power",
      selected,
      line("M96 64V83H29V185H43", "power", true) +
        line("M96 212V230", "power", true) +
        line("M96 284V327H29V492H43", "power", true),
    );
    out += route(
      "data",
      selected,
      `<path d="M145 674V617" fill="none" stroke="var(--data)" stroke-width="5" marker-start="url(#ori-data-arrow)" marker-end="url(#ori-data-arrow)"/>`,
    );
    out += route(
      "heat",
      selected,
      location === "hall"
        ? line("M247 545H267", "heat", true) +
            line("M312 493V332H365V78H285V64", "heat", true)
        : line("M247 545H366V251H352", "heat", true) +
            line("M285 201V177H365V78H285V64", "heat", true),
    );
    out += cabinet("ups", 43, 157, 107, 55, ["Power", "backup"], true);
    out += rect("distribution", 35, 230, 123, 54, {
      fill: "var(--surface)",
      radius: 7,
    });
    out += label(96.5, 262, "Distribution", "distribution", { size: 14 });
    out += rackGroup(true) + cdu(true, location, false);
    out += badge("grid", 31, 24, 130, 40, "Grid", "power");
    out += badge("outdoors", 213, 24, 145, 40, "Heat rejection", "heat");
    out += badge("network", 65, 674, 160, 35, "Network", "data");
  } else {
    out += rect("building", 56, 111, 1048, 434, {
      fill: "var(--surface)",
      radius: 20,
      width: 2,
    });
    out += room(
      "electrical-room",
      75,
      132,
      245,
      390,
      ["Electrical room"],
      "GRAY SPACE",
      false,
      spaces,
    );
    out += room(
      "it-hall",
      340,
      132,
      490,
      390,
      ["IT hall"],
      "WHITE SPACE",
      false,
      spaces,
    );
    out += room(
      "mechanical-gallery",
      850,
      132,
      235,
      390,
      ["Mechanical gallery"],
      "GRAY SPACE",
      false,
      spaces,
    );
    out += route(
      "power",
      selected,
      line("M197 90V115H93V215H197V242", "power", true) +
        line("M197 334V379", "power", true) +
        line("M280 424H350V361H373", "power", true),
    );
    out += route(
      "data",
      selected,
      `<path d="M518 90V225" fill="none" stroke="var(--data)" stroke-width="5" marker-start="url(#ori-data-arrow)" marker-end="url(#ori-data-arrow)"/>`,
    );
    out += route(
      "heat",
      selected,
      location === "hall"
        ? line("M662 390H692", "heat", true) +
            line("M804 390H1064V112H987V90", "heat", true)
        : line("M662 390H892", "heat", true) +
            line("M1037 390H1064V112H987V90", "heat", true),
    );
    out += cabinet("ups", 115, 242, 165, 92, "Power backup");
    out += cabinet("distribution", 115, 379, 165, 90, "Distribution");
    out += rackGroup(false) + cdu(false, location, false);
    out += badge("grid", 112, 40, 170, 50, "Grid", "power");
    out += badge("network", 428, 40, 180, 50, "Network", "data");
    out += badge("outdoors", 892, 40, 190, 50, "Heat rejection", "heat");
  }
  return `<g data-spatial-scene="${spaces ? "white-grey" : "three-paths"}">${out}</g>`;
}

function dataHallPhoto(compact) {
  const source =
    "https://www.gstatic.com/marketing-cms/assets/images/19/43/b476c0984f2da3b2faa1a7f588ce/server-aisles-in-our-new-albany-data-center-building-in-central-ohio.jpg=n-w1086-h814-fcrop64=1,0000202fffffdfea-rw";
  const photo = compact
    ? { x: 14, y: 15, w: 362, h: 204 }
    : { x: 20, y: 12, w: 1120, h: 530 };
  return `<g data-spatial-scene="white-grey" data-space-view="photo">
    <image data-data-hall-image="google-new-albany" href="${source}"
      x="${photo.x}" y="${photo.y}" width="${photo.w}" height="${photo.h}"
      preserveAspectRatio="xMidYMid ${compact ? "meet" : "slice"}"/>
    ${label(
      compact ? 195 : 28,
      compact ? 250 : 576,
      "White space · New Albany, Ohio",
      "",
      {
        anchor: compact ? "middle" : "start",
        size: compact ? 17 : 21,
        weight: 600,
      },
    )}
    ${label(
      compact ? 195 : 1132,
      compact ? 278 : 576,
      "Photograph: Google",
      "",
      {
        anchor: compact ? "middle" : "end",
        size: compact ? 14 : 18,
        color: "var(--muted)",
      },
    )}
  </g>`;
}

function rackBoundary(state, compact) {
  if (state.rackView === "rear") return rackRear(compact);
  const source =
    "https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/_images/nvl72-ai-factory-01.png";
  let out = defs();
  const photo = compact
    ? { x: 80, y: 12, w: 230, h: 292 }
    : { x: 42, y: 18, w: 397, h: 504 };
  out += `<image data-product-image="gb300" href="${source}" x="${photo.x}" y="${photo.y}" width="${photo.w}" height="${photo.h}" preserveAspectRatio="xMidYMid meet"/>`;
  out += label(
    compact ? 195 : 240,
    compact ? 326 : 557,
    "GB300 NVL72 · Image: NVIDIA",
    "",
    { size: compact ? 13 : 17, color: "var(--muted)" },
  );
  const x = compact ? 20 : 495,
    y = compact ? 352 : 48,
    w = compact ? 350 : 610,
    h = compact ? 124 : 175;
  out += rect("rack-requirement", x, y, w, h, {
    fill: "var(--surface)",
    stroke: "var(--power)",
  });
  out += label(x + w / 2, y + 31, "FULL-RACK REQUIREMENT", "rack-requirement", {
    size: compact ? 15 : 20,
    color: "var(--muted)",
  });
  out += `<text x="${x + w / 2}" y="${y + (compact ? 88 : 113)}" text-anchor="middle" font-size="${compact ? 40 : 58}" fill="var(--power)" data-rack-requirement="142">Up to 142 kW</text>`;
  if (!compact)
    out += label(
      x + w / 2,
      y + 148,
      "Published requirement; workload draw varies",
      "rack-requirement",
      { size: 19, color: "var(--muted)" },
    );
  const blocks = compact
    ? [
        [20, 529, 100, 99, ["AC", "supply"]],
        [145, 529, 100, 99, ["PSUs in", "shelves"]],
        [270, 529, 100, 99, ["50–51 V", "DC busbar"]],
      ]
    : [
        [495, 325, 170, 115, ["AC supply"]],
        [715, 325, 170, 115, ["PSUs in", "power shelves"]],
        [935, 325, 170, 115, ["50–51 V DC", "rack busbar"]],
      ];
  blocks.forEach(([bx, by, bw, bh, names], i) => {
    out += rect(`rack-stage-${i}`, bx, by, bw, bh, { fill: "var(--panel)" });
    names.forEach(
      (name, j) =>
        (out += label(
          bx + bw / 2,
          by + (compact ? 40 : names.length > 1 ? 49 : 65) + j * 23,
          name,
          `rack-stage-${i}`,
          { size: compact ? 17 : 22 },
        )),
    );
    if (i < 2)
      out += line(
        `M${bx + bw} ${by + bh / 2} H${blocks[i + 1][0]}`,
        "power",
        true,
        compact ? 3 : 5,
      );
  });
  out += label(
    compact ? 195 : 800,
    compact ? 675 : 495,
    "Inside the rack → compute + switch trays",
    "",
    { size: compact ? 17 : 25 },
  );
  return `<g data-spatial-scene="rack-boundary">${out}</g>`;
}

function rackRear(compact) {
  const source =
    "https://docs.nvidia.com/dgx/dgxgb200-user-guide/_images/hardware-rack-rear-gb300.png";
  let out = defs();
  if (compact) {
    // Enlarge the rear cabinet from NVIDIA's annotated exploded view. The
    // callout terminates at the same power-busbar point as the source arrow.
    out += `<svg x="95" y="12" width="200" height="351" viewBox="975 80 370 650" role="presentation">
      <image data-product-image="gb300" data-rack-view="rear" href="${source}" x="0" y="0" width="1426" height="813"/>
    </svg>`;
    out += line("M195 399V367H105L152 234", "power", true, 3);
    out += label(195, 435, "Rear power busbar", "", { size: 26, weight: 650 });
    out += label(195, 480, "50–51 V DC", "", { size: 34, color: "var(--power)" });
    out += label(195, 515, "Inside this rack", "", { size: 22 });
    out += label(195, 582, "DGX GB300 NVL72", "", { size: 21 });
    out += label(195, 616, "Rear detail · Figure: NVIDIA", "", { size: 16, color: "var(--muted)" });
  } else {
    out += `<rect x="115" y="4" width="930" height="530" rx="8" fill="white"/>
      <image data-product-image="gb300" data-rack-view="rear" href="${source}" x="115" y="4" width="930" height="530" preserveAspectRatio="xMidYMid meet"/>`;
    out += label(28, 580, "50–51 V DC · inside this rack", "", { anchor: "start", size: 25, weight: 600, color: "var(--power)" });
    out += label(1132, 580, "DGX GB300 NVL72 · Figure: NVIDIA", "", { anchor: "end", size: 19, color: "var(--muted)" });
  }
  return `<g data-spatial-scene="rack-boundary" data-rack-detail="rear">${out}</g>`;
}

export function renderSpatial(kind, state = {}, compact = false) {
  if (kind === "three-paths") return floorPlan(state, compact, false);
  if (kind === "white-grey")
    return state.spaceView === "plan"
      ? floorPlan(state, compact, true)
      : dataHallPhoto(compact);
  if (kind === "rack-boundary") return rackBoundary(state, compact);
  throw new Error(`Unknown orientation spatial scene: ${kind}`);
}
