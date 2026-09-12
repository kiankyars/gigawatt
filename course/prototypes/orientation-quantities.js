import {
  facilityLedger,
  profileSummary,
  efficiencyCase,
} from "./orientation-model.js";

const n = (value, digits = 0) =>
  value.toLocaleString("en-US", {
    maximumFractionDigits: digits,
    minimumFractionDigits: digits,
  });
const text = (
  x,
  y,
  value,
  size = 22,
  fill = "var(--text)",
  anchor = "start",
  extra = "",
) =>
  `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" text-anchor="${anchor}" ${extra}>${value}</text>`;
const rect = (id, x, y, w, h, fill = "var(--panel)", stroke = "var(--line)") =>
  `<rect id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="${fill}" stroke="${stroke}"/>`;
const label = (
  id,
  x,
  y,
  value,
  size = 22,
  fill = "var(--text)",
  anchor = "start",
) => text(x, y, value, size, fill, anchor, `data-label-for="${id}"`);

function ledger(state, compact) {
  const f = facilityLedger(),
    whole = state.boundary === "facility";
  const rows = [
    ["10 racks × 100 kW", f.rackTotalKW, "var(--power)", true],
    ["Network + storage", 100, "var(--data)", true],
    ["Electrical losses", 40, "var(--heat)", false],
    ["Cooling machinery", 160, "var(--heat)", false],
    ["Other facility loads", 20, "var(--heat)", false],
  ];
  const x = compact ? 15 : 55,
    w = compact ? 360 : 680,
    h = compact ? 67 : 78,
    gap = compact ? 10 : 13,
    top = compact ? 25 : 66;
  let out = `<g data-facility-kw="${f.facilityKW}" data-meter-kw="${whole ? f.facilityKW : f.itKW}">`;
  rows.forEach(([name, value, color, it], i) => {
    const y = top + i * (h + gap),
      active = whole || it,
      id = `ledger-${i}`;
    out += `<g opacity="${active ? 1 : 0.35}">${rect(id, x, y, w, h)}<rect x="${x}" y="${y + 13}" width="5" height="${h - 26}" rx="2" fill="${color}"/>`;
    out += label(id, x + 18, y + h / 2 + 7, name, compact ? 17 : 25);
    out +=
      label(
        id,
        x + w - 18,
        y + h / 2 + 7,
        `${n(value)} kW`,
        compact ? 18 : 27,
        color,
        "end",
      ) + "</g>";
  });
  const mx = compact ? 15 : 790,
    my = compact ? 445 : 155,
    mw = compact ? 360 : 310;
  out += rect("meter-total", mx, my, mw, 165, "var(--surface)", "var(--power)");
  out += label(
    "meter-total",
    mx + mw / 2,
    my + 35,
    whole ? "FACILITY INPUT" : "IT INPUT",
    16,
    "var(--muted)",
    "middle",
  );
  out += label(
    "meter-total",
    mx + mw / 2,
    my + 102,
    `${n(whole ? f.facilityKW : f.itKW)} kW`,
    compact ? 44 : 43,
    "var(--text)",
    "middle",
  );
  out += label(
    "meter-total",
    mx + mw / 2,
    my + 137,
    whole ? "IT + supporting systems" : "Racks + network + storage",
    16,
    "var(--muted)",
    "middle",
  );
  return out + "</g>";
}

function heat(compact) {
  const f = facilityLedger();
  const cards = compact
    ? [
        [15, 55, 220, 135, "IT equipment", f.itKW],
        [15, 305, 220, 135, "Supporting systems", f.overheadKW],
      ]
    : [
        [80, 90, 435, 155, "IT equipment", f.itKW],
        [80, 325, 435, 155, "Supporting systems", f.overheadKW],
      ];
  let out = `<g data-heat-kw="${f.facilityKW}">`;
  cards.forEach(([x, y, w, h, name, kw], i) => {
    const id = `heat-equipment-${i}`;
    out += rect(id, x, y, w, h);
    out += label(id, x + 18, y + 32, name, compact ? 18 : 26);
    if (compact) {
      out += label(id, x + 18, y + 79, `${n(kw)} kW`, 28, "var(--power)");
      out += label(id, x + 18, y + 108, "electrical input", 16, "var(--muted)");
      out += `<path d="M235 ${y + 70} H350 ${i === 0 ? "V545" : ""}" stroke="var(--heat)" stroke-width="4" fill="none"/>`;
      out += `<path d="M266 ${y + 64} L276 ${y + 70} L266 ${y + 76}" stroke="var(--heat)" stroke-width="2.5" fill="none"/>`;
      out += text(292, y + 24, `≈ ${n(kw)} kW`, 16, "var(--heat)", "middle");
      out += text(292, y + 47, "heat", 15, "var(--heat)", "middle");
      if (i === 1)
        out += `<path d="M343 534 L350 544 L357 534" stroke="var(--heat)" stroke-width="3" fill="none"/>`;
    } else {
      out += label(
        id,
        x + 22,
        y + 83,
        `${n(kw)} kW electrical input`,
        26,
        "var(--power)",
      );
      out += `<path d="M515 ${y + 78} H809" stroke="var(--heat)" stroke-width="7"/><path d="M798 ${y + 70} L810 ${y + 78} L798 ${y + 86}" fill="none" stroke="var(--heat)" stroke-width="3"/>`;
      out += text(
        645,
        y + 55,
        `≈ ${n(kw)} kW heat`,
        22,
        "var(--heat)",
        "middle",
      );
    }
  });
  const x = compact ? 15 : 810,
    y = compact ? 545 : 150,
    w = compact ? 360 : 300,
    h = compact ? 115 : 270;
  out += rect("environment", x, y, w, h, "var(--surface)", "var(--heat)");
  out += label(
    "environment",
    x + w / 2,
    y + (compact ? 32 : 55),
    "TO THE ENVIRONMENT",
    compact ? 16 : 18,
    "var(--muted)",
    "middle",
  );
  out += label(
    "environment",
    x + w / 2,
    y + (compact ? 78 : 139),
    `≈ ${n(f.facilityKW)} kW`,
    compact ? 37 : 36,
    "var(--heat)",
    "middle",
  );
  if (!compact)
    out += label(
      "environment",
      x + w / 2,
      y + 193,
      "Across all heat paths",
      18,
      "var(--muted)",
      "middle",
    );
  out += text(
    compact ? 195 : 580,
    compact ? 704 : 565,
    "Steady operation · negligible energy accumulation",
    compact ? 13 : 19,
    "var(--muted)",
    "middle",
  );
  return out + "</g>";
}

function powerChart(state, compact, shortInterval = false) {
  const alternate = shortInterval
    ? state.trace === "spike"
    : state.schedule === "flat";
  const segments = shortInterval
    ? alternate
      ? [
          { hours: 1 / 60, powerMW: 12 },
          { hours: 4 / 60, powerMW: 7 },
        ]
      : [{ hours: 5 / 60, powerMW: 8 }]
    : alternate
      ? [{ hours: 24, powerMW: 184 / 24 }]
      : [
          { hours: 8, powerMW: 6 },
          { hours: 12, powerMW: 10 },
          { hours: 4, powerMW: 4 },
        ];
  const m = profileSummary(segments),
    limit = shortInterval ? 10 : 8;
  const left = compact ? 53 : 95,
    top = compact ? 65 : 65,
    width = compact ? 310 : 955,
    height = compact ? 300 : 315;
  const maxY = 14,
    maxX = shortInterval ? 5 : 24;
  const px = (v) => left + (v / maxX) * width,
    py = (v) => top + height - (v / maxY) * height;
  let out = `<g data-energy-mwh="${m.energyMWh}" data-peak-mw="${m.peakMW}" data-average-mw="${m.averageMW}">`;
  [0, 4, 8, 12].forEach((value) => {
    out +=
      `<path d="M${left} ${py(value)} H${left + width}" stroke="var(--line)"/>` +
      text(left - 12, py(value) + 5, value, 16, "var(--muted)", "end");
  });
  out += text(left - 10, top - 24, "MW", 17, "var(--muted)", "end");
  let elapsed = 0,
    points = `M${left} ${py(0)}`;
  for (const segment of segments) {
    const span = segment.hours * (shortInterval ? 60 : 1);
    points += ` L${px(elapsed)} ${py(segment.powerMW)} L${px(elapsed + span)} ${py(segment.powerMW)}`;
    elapsed += span;
  }
  out += `<path d="${points} L${px(maxX)} ${py(0)} Z" fill="var(--power)" fill-opacity="0.18" stroke="var(--power)" stroke-width="3"/>`;
  if (!shortInterval) {
    let start = 0;
    for (const segment of segments) {
      const center = px(start + segment.hours / 2);
      const labelPower = segment.powerMW * (alternate ? 0.32 : 0.5);
      const energy = n(segment.powerMW * segment.hours);
      if (compact) {
        out += text(
          center,
          py(labelPower),
          energy,
          18,
          "var(--power)",
          "middle",
        );
        out += text(
          center,
          py(labelPower) + 21,
          "MWh",
          13,
          "var(--power)",
          "middle",
        );
      } else {
        out += text(
          center,
          py(labelPower) + 7,
          `${energy} MWh`,
          23,
          "var(--power)",
          "middle",
        );
      }
      start += segment.hours;
    }
    out += text(
      compact ? 195 : 580,
      compact ? 434 : 446,
      "Energy = power × time",
      compact ? 17 : 23,
      "var(--text)",
      "middle",
    );
  }
  out += `<path d="M${left} ${py(limit)} H${left + width}" stroke="var(--heat)" stroke-width="2" stroke-dasharray="7 6"/>`;
  out += text(
    left + width - 5,
    py(limit) - 10,
    `${limit} MW supply limit`,
    compact ? 15 : 19,
    "var(--heat)",
    "end",
  );
  (shortInterval ? [0, 1, 5] : [0, 8, 20, 24]).forEach(
    (value) =>
      (out += text(
        px(value),
        top + height + 28,
        value,
        17,
        "var(--muted)",
        "middle",
      )),
  );
  out += text(
    left + width,
    top + height + 58,
    shortInterval ? "minutes" : "hours",
    17,
    "var(--muted)",
    "end",
  );
  if (shortInterval) {
    out += `<path d="M${left} ${py(8)} H${left + width}" stroke="var(--data)" stroke-width="2" stroke-dasharray="3 5"/>`;
    out += text(
      left + width - 5,
      py(8) - 11,
      "8 MW average",
      compact ? 15 : 19,
      "var(--data)",
      "end",
    );
  }
  const cards = shortInterval
    ? [
        ["5-MINUTE ENERGY", `${n(m.energyMWh * 1000, 1)} kWh`],
        ["ACTUAL PEAK", `${n(m.peakMW, 0)} MW`],
      ]
    : [
        ["DAILY ENERGY", `${n(m.energyMWh)} MWh`],
        ["PEAK DEMAND", `${n(m.peakMW, alternate ? 2 : 0)} MW`],
      ];
  cards.forEach(([heading, value], i) => {
    const x = compact ? 15 + i * 187 : 135 + i * 475,
      y = compact ? 455 : 475,
      w = compact ? 173 : 415,
      h = compact ? 118 : 100,
      id = `chart-metric-${i}`;
    out += rect(id, x, y, w, h);
    out += label(
      id,
      x + w / 2,
      y + 29,
      heading,
      compact ? 12 : 15,
      "var(--muted)",
      "middle",
    );
    out += label(
      id,
      x + w / 2,
      y + 76,
      value,
      compact ? 29 : 39,
      i ? "var(--text)" : "var(--power)",
      "middle",
    );
  });
  return out + "</g>";
}

function usefulWork(state, compact) {
  const extra = state.efficiency === "extra",
    it = extra ? 1200 : 1000;
  const m = efficiencyCase({
    itKW: it,
    overheadKW: 200,
    usefulUnitsPerHour: 100,
  });
  const x = compact ? 20 : 85,
    w = compact ? 350 : 990,
    scale = w / 1600,
    y = compact ? 150 : 160;
  let out = `<g data-pue="${m.pue}" data-energy-per-job="${m.energyKWhPerUnit}">`;
  out += text(
    compact ? 195 : 580,
    compact ? 53 : 55,
    "100 identical jobs completed in one hour",
    compact ? 19 : 28,
    "var(--data)",
    "middle",
  );
  out += text(
    x,
    y - 22,
    "FACILITY ENERGY OVER THAT HOUR",
    compact ? 13 : 16,
    "var(--muted)",
  );
  out += `<rect x="${x}" y="${y}" width="${it * scale}" height="80" rx="8" fill="var(--power)" fill-opacity="0.2"/><rect x="${x + it * scale}" y="${y}" width="${200 * scale}" height="80" rx="8" fill="var(--heat)" fill-opacity="0.35"/>`;
  out += text(
    x + (it * scale) / 2,
    y + 48,
    `${n(it)} kWh IT`,
    compact ? 19 : 30,
    "var(--text)",
    "middle",
  );
  out += text(
    x + it * scale + 100 * scale,
    y + 116,
    "200 kWh",
    compact ? 16 : 22,
    "var(--heat)",
    "middle",
  );
  out += text(
    x + it * scale + 100 * scale,
    y + 141,
    "overhead",
    compact ? 13 : 17,
    "var(--muted)",
    "middle",
  );
  const cards = [
    ["PUE", n(m.pue, 2), "Facility energy ÷ IT energy"],
    [
      "ENERGY / COMPLETED JOB",
      `${n(m.energyKWhPerUnit)} kWh`,
      "Same completed work",
    ],
  ];
  cards.forEach(([heading, value, detail], i) => {
    const cx = compact ? 15 : 85 + i * 530,
      cy = compact ? 350 + i * 162 : 370,
      cw = compact ? 360 : 460,
      ch = 145,
      id = `efficiency-${i}`;
    out += rect(id, cx, cy, cw, ch);
    out += label(
      id,
      cx + cw / 2,
      cy + 31,
      heading,
      compact ? 14 : 17,
      "var(--muted)",
      "middle",
    );
    out += label(
      id,
      cx + cw / 2,
      cy + 87,
      value,
      45,
      i ? "var(--heat)" : "var(--power)",
      "middle",
    );
    out += label(
      id,
      cx + cw / 2,
      cy + 122,
      detail,
      compact ? 16 : 19,
      "var(--muted)",
      "middle",
    );
  });
  out += text(
    compact ? 195 : 580,
    compact ? 707 : 565,
    "PUE = power usage effectiveness",
    compact ? 16 : 21,
    "var(--muted)",
    "middle",
  );
  return out + "</g>";
}

export function renderQuantities(kind, state, compact = false) {
  if (kind === "facility-meter") return ledger(state, compact);
  if (kind === "heat-account") return heat(compact);
  if (kind === "power-energy") return powerChart(state, compact);
  if (kind === "meter-average") return powerChart(state, compact, true);
  if (kind === "useful-work") return usefulWork(state, compact);
  throw new RangeError(`Unknown quantity scene: ${kind}`);
}
