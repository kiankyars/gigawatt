import {
  ORIENTATION_PROFILES,
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
  `<rect id="${id}" x="${x}" y="${y}" width="${w}" height="${h}" rx="12" fill="${fill}" stroke="${stroke}"/>`;
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
  const m = facilityLedger(),
    whole = state.boundary === "facility";
  const x = compact ? 25 : 100,
    width = compact ? 340 : 960;
  const scale = width / 2000,
    top = compact ? 143 : 178,
    h = compact ? 96 : 100;
  let out = `<g data-facility-kw="${m.facilityKW}" data-meter-kw="${whole ? m.facilityKW : m.itKW}" data-it-kw="${m.itKW}" data-overhead-kw="${m.overheadKW}" data-supply-rating-kw="2000">`;
  out += text(
    x,
    compact ? 42 : 45,
    "10 racks × 142 kW + 80 kW network/storage",
    compact ? 16 : 27,
  );
  out += text(
    x,
    compact ? 73 : 86,
    "Illustrative operating point",
    compact ? 15 : 18,
    "var(--muted)",
  );
  out += text(x, top - 22, "POWER DRAWN", compact ? 15 : 18, "var(--muted)");
  out += rect(
    "load-it",
    x,
    top,
    m.itKW * scale,
    h,
    "var(--power)",
    "var(--power)",
  );
  out += label(
    "load-it",
    x + (m.itKW * scale) / 2,
    top + h / 2 + 7,
    "1,500 kW IT",
    compact ? 24 : 36,
    "var(--paper)",
    "middle",
  );
  out += `<g opacity="${whole ? 1 : 0.28}">${rect("load-support", x + m.itKW * scale, top, m.overheadKW * scale, h, "var(--heat)", "var(--heat)")}</g>`;
  const supportX = x + (m.itKW + m.overheadKW / 2) * scale;
  out += `<path d="M${supportX} ${top + h + 4}V${top + h + 23}" stroke="var(--heat)" stroke-width="2"/>`;
  out += text(
    compact ? x + width : supportX,
    top + h + 46,
    "300 kW support",
    compact ? 17 : 24,
    "var(--heat)",
    compact ? "end" : "middle",
  );
  const supplyY = compact ? 360 : 365;
  out += text(
    x,
    supplyY - 22,
    "SUPPLY NAMEPLATE RATING",
    compact ? 15 : 18,
    "var(--muted)",
  );
  out += rect(
    "supply-rating",
    x,
    supplyY,
    width,
    82,
    "var(--surface)",
    "var(--muted)",
  );
  out += label(
    "supply-rating",
    x + width / 2,
    supplyY + 51,
    "2,000 kW rated",
    compact ? 30 : 36,
    "var(--text)",
    "middle",
  );
  const my = compact ? 510 : 489,
    mh = compact ? 145 : 95;
  out += rect(
    "selected-meter",
    x,
    my,
    width,
    mh,
    "var(--surface)",
    "var(--power)",
  );
  if (compact) {
    out += label(
      "selected-meter",
      x + width / 2,
      my + 36,
      whole ? "WHOLE-FACILITY METER" : "IT-EQUIPMENT METER",
      15,
      "var(--muted)",
      "middle",
    );
    out += label(
      "selected-meter",
      x + width / 2,
      my + 101,
      `${n(whole ? m.facilityKW : m.itKW)} kW`,
      45,
      "var(--power)",
      "middle",
    );
  } else {
    out += label(
      "selected-meter",
      x + 28,
      my + 55,
      whole ? "Whole-facility meter" : "IT-equipment meter",
      25,
    );
    out += label(
      "selected-meter",
      x + width - 28,
      my + 61,
      `${n(whole ? m.facilityKW : m.itKW)} kW`,
      44,
      "var(--power)",
      "end",
    );
  }
  return out + "</g>";
}

function powerChart(state, compact) {
  const flat = state.schedule === "flat";
  const m = profileSummary(
    flat ? ORIENTATION_PROFILES.flat : ORIENTATION_PROFILES.variable,
  );
  const left = compact ? 50 : 100,
    width = compact ? 315 : 960;
  const top = compact ? 160 : 130,
    height = compact ? 285 : 270;
  const px = (hour) => left + (hour / 24) * width;
  const py = (power) => top + height - (power / 9.5) * height;
  let out = `<g data-energy-mwh="${m.energyMWh}" data-peak-mw="${m.peakMW}" data-average-mw="${m.averageMW}" data-fixed-mw="4" data-batch-energy-mwh="48" data-deadline-hour="24">`;
  out += text(
    compact ? 195 : 580,
    compact ? 42 : 38,
    "LLM batch evaluations",
    compact ? 23 : 28,
    "var(--data)",
    "middle",
  );
  out += text(
    compact ? 195 : 580,
    compact ? 73 : 74,
    "Ready 00:00 · Due 24:00",
    compact ? 18 : 23,
    "var(--muted)",
    "middle",
  );
  [0, 4, 8].forEach((value) => {
    out += `<path d="M${left} ${py(value)}H${left + width}" stroke="var(--line)"/>`;
    out += text(left - 12, py(value) + 5, value, 16, "var(--muted)", "end");
  });
  out += text(left - 9, top - 20, "MW", 16, "var(--muted)", "end");
  out += `<rect id="fixed-demand" x="${left}" y="${py(4)}" width="${width}" height="${py(0) - py(4)}" fill="var(--power)" fill-opacity="0.2" stroke="var(--power)"/>`;
  if (compact) {
    out += label(
      "fixed-demand",
      left + width / 2,
      py(2) - 6,
      "Live inference + overhead",
      18,
      "var(--power)",
      "middle",
    );
    out += label(
      "fixed-demand",
      left + width / 2,
      py(2) + 24,
      "4 MW · stays on",
      20,
      "var(--power)",
      "middle",
    );
  } else
    out += label(
      "fixed-demand",
      left + width / 2,
      py(2) + 8,
      "Live inference + overhead · 4 MW",
      26,
      "var(--power)",
      "middle",
    );
  const bx = px(flat ? 0 : 12),
    bw = width * (flat ? 1 : 0.5),
    batchMW = flat ? 2 : 4;
  out += `<rect id="batch-demand" x="${bx}" y="${py(4 + batchMW)}" width="${bw}" height="${py(4) - py(4 + batchMW)}" fill="var(--data)" fill-opacity="0.22" stroke="var(--data)"/>`;
  out += label(
    "batch-demand",
    bx + bw / 2,
    py(4 + batchMW / 2) + (compact ? 10 : 17),
    `Batch: +${batchMW} MW`,
    compact ? 16 : 24,
    "var(--data)",
    "middle",
  );
  out += `<path d="M${left} ${py(6.5)}H${left + width}" stroke="var(--heat)" stroke-width="2" stroke-dasharray="7 6"/>`;
  out += text(
    left + (compact ? 3 : 8),
    py(6.5) - 10,
    "6.5 MW supply limit",
    compact ? 15 : 20,
    "var(--heat)",
  );
  for (const hour of [0, 12, 24])
    out += text(
      px(hour),
      top + height + 29,
      `${String(hour).padStart(2, "0")}:00`,
      compact ? 15 : 18,
      "var(--muted)",
      hour === 0 ? "start" : hour === 24 ? "end" : "middle",
    );
  out += text(
    compact ? 195 : 580,
    compact ? 517 : 464,
    "Energy = average power × time",
    compact ? 21 : 26,
    "var(--text)",
    "middle",
  );
  const cards = [
    ["DAILY ENERGY", `${n(m.energyMWh)} MWh`],
    ["PEAK DEMAND", `${n(m.peakMW)} MW`],
  ];
  cards.forEach(([heading, value], i) => {
    const x = compact ? 20 + i * 180 : 100 + i * 500,
      y = compact ? 555 : 499;
    const w = compact ? 170 : 460,
      h = compact ? 115 : 88,
      id = `demand-metric-${i}`;
    out += rect(id, x, y, w, h);
    out += label(
      id,
      x + w / 2,
      y + 26,
      heading,
      compact ? 12 : 15,
      "var(--muted)",
      "middle",
    );
    out += label(
      id,
      x + w / 2,
      y + (compact ? 79 : 76),
      value,
      compact ? 30 : 38,
      i ? "var(--text)" : "var(--power)",
      "middle",
    );
  });
  return out + "</g>";
}

function usefulWork(state, compact) {
  const lower = state.efficiency === "lower",
    overhead = lower ? 150 : 300;
  const m = efficiencyCase({
    itKW: 1500,
    overheadKW: overhead,
    usefulUnitsPerHour: 100,
  });
  const x = compact ? 40 : 140,
    barW = compact ? 133 : 290;
  const bottom = compact ? 414 : 444,
    scale = compact ? 300 / 2000 : 360 / 2000;
  const itTop = bottom - 1500 * scale,
    top = itTop - overhead * scale;
  let out = `<g data-pue="${m.pue}" data-facility-energy-kwh="${m.facilityKW}" data-it-energy-kwh="1500" data-overhead-energy-kwh="${overhead}" data-energy-per-job="${m.energyKWhPerUnit}">`;
  out += text(
    compact ? 195 : 580,
    39,
    "ENERGY OVER THE SAME ONE-HOUR INTERVAL",
    compact ? 13 : 20,
    "var(--muted)",
    "middle",
  );
  out += `<rect id="pue-it" x="${x}" y="${itTop}" width="${barW}" height="${1500 * scale}" rx="8" fill="var(--power)" fill-opacity="0.22" stroke="var(--power)"/>`;
  out += label(
    "pue-it",
    x + barW / 2,
    itTop + (1500 * scale) / 2 - 9,
    "IT",
    compact ? 20 : 26,
    "var(--power)",
    "middle",
  );
  out += label(
    "pue-it",
    x + barW / 2,
    itTop + (1500 * scale) / 2 + 28,
    "1,500 kWh",
    compact ? 22 : 33,
    "var(--power)",
    "middle",
  );
  out += `<rect id="pue-overhead" x="${x}" y="${top}" width="${barW}" height="${overhead * scale}" fill="var(--heat)" fill-opacity="0.4" stroke="var(--heat)"/>`;
  const lx = x + barW + (compact ? 21 : 39),
    ly = top + (overhead * scale) / 2;
  out += `<path d="M${x + barW} ${ly}h${compact ? 14 : 30}" stroke="var(--heat)" stroke-width="2"/>`;
  out += text(lx, ly + 6, `${overhead} kWh`, compact ? 22 : 30, "var(--heat)");
  out += text(
    lx,
    ly + 32,
    "supporting systems",
    compact ? 14 : 20,
    "var(--muted)",
  );
  out += text(
    x + barW / 2,
    bottom + 38,
    `${n(m.facilityKW)} kWh total`,
    compact ? 22 : 29,
    "var(--text)",
    "middle",
  );
  if (compact) {
    out += text(
      195,
      511,
      "PUE = facility energy ÷ IT energy",
      19,
      "var(--text)",
      "middle",
    );
    out += text(
      195,
      556,
      `${n(m.facilityKW)} ÷ 1,500`,
      29,
      "var(--muted)",
      "middle",
    );
    out += text(195, 639, n(m.pue, 2), 70, "var(--power)", "middle");
    out += text(
      195,
      695,
      "PUE: power usage effectiveness",
      16,
      "var(--muted)",
      "middle",
    );
  } else {
    out += text(
      815,
      245,
      "PUE = facility energy ÷ IT energy",
      27,
      "var(--text)",
      "middle",
    );
    out += text(
      815,
      307,
      `${n(m.facilityKW)} ÷ 1,500`,
      38,
      "var(--muted)",
      "middle",
    );
    out += text(815, 416, n(m.pue, 2), 100, "var(--power)", "middle");
    out += text(
      815,
      480,
      "Power usage effectiveness",
      23,
      "var(--muted)",
      "middle",
    );
  }
  return out + "</g>";
}

export function renderQuantities(kind, state, compact = false) {
  if (kind === "facility-meter") return ledger(state, compact);
  if (kind === "power-energy") return powerChart(state, compact);
  if (kind === "useful-work") return usefulWork(state, compact);
  throw new RangeError(`Unknown quantity scene: ${kind}`);
}
