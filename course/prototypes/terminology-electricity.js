/* D00 recognition diagrams. Ideal teaching circuits, not installation layouts. */
const esc = (value) => String(value).replaceAll("&", "&amp;").replaceAll("<", "&lt;");
const text = (x, y, value, size = 22, color = "text", anchor = "middle") =>
  `<text x="${x}" y="${y}" font-size="${size}" text-anchor="${anchor}" fill="var(--${color})">${esc(value)}</text>`;
const path = (d, color = "power", width = 4, extra = "") =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" ${extra}/>`;
const arrow = (d, color = "power", width = 4) =>
  path(d, color, width, `marker-end="url(#primer-${color}-arrow)"`);
const rect = (x, y, w, h, color = "line", fill = "surface", radius = 12) =>
  `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${radius}" fill="var(--${fill})" stroke="var(--${color})" stroke-width="2"/>`;
const dot = (x, y, color = "power") => `<circle cx="${x}" cy="${y}" r="5" fill="var(--${color})"/>`;
const defs = `<defs>${["power", "heat", "data", "muted"].map((color) =>
  `<marker id="primer-${color}-arrow" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="3.4" markerHeight="3.4" orient="auto"><path d="M1 1L9 5L1 9Z" fill="var(--${color})"/></marker>`).join("")}</defs>`;

function circuit(compact, mode = "circuit", state = {}) {
  const left = compact ? 70 : 200, right = compact ? 252 : 820;
  const top = compact ? 180 : 155, bottom = compact ? 420 : 435, cy = (top + bottom) / 2;
  const r = compact ? 35 : 48, lw = compact ? 66 : 104, lh = compact ? 108 : 130;
  const numeric = mode !== "circuit", power = mode === "power", open = !numeric && state.circuit === "open";
  const middle = (left+right)/2, gap = compact ? 27 : 42;
  let out = path(`M${left} ${cy-r}V${top}H${middle-gap}M${middle+gap} ${top}H${right}V${cy-lh/2}`) +
    path(`M${right} ${cy+lh/2}V${bottom}H${left}V${cy+r}`);
  if (numeric) {
    if (mode === "voltage-current") {
      out += `<circle cx="${middle}" cy="${top}" r="${gap}" fill="var(--surface)" stroke="var(--power)" stroke-width="2"/>` + text(middle, top+7, "A", 21, "power");
    } else out += path(`M${middle-gap} ${top}H${middle+gap}`);
  } else {
    out += dot(middle-gap, top) + dot(middle+gap, top);
    out += path(`M${middle-gap} ${top}L${middle+gap-4} ${open ? top-32 : top}`, "power", 3);
  }
  out += `<circle cx="${left}" cy="${cy}" r="${r}" fill="var(--surface)" stroke="var(--power)" stroke-width="3"/>`;
  out += text(left, cy - 10, "+", 25, "power") + text(left, cy + 25, "−", 25, "power");
  out += rect(right-lw/2, cy-lh/2, lw, lh, "power");
  out += text(right, cy+7, power ? "24 W" : numeric ? "6 Ω" : "Load", compact ? 19 : 25);
  if (!open) {
    out += arrow(`M${right} ${top+12}V${cy-lh/2-9}`, "power", 3);
    out += arrow(`M${right-35} ${bottom}H${left+50}`);
  }
  out += text(left, bottom+48, numeric ? "12 V DC source" : "DC source", compact ? 17 : 23);
  if (mode === "circuit") {
    out += text(middle, top-55, open ? "No steady current" : "Conventional current", compact ? 20 : 25, "power");
    out += text(middle, bottom+100, open ? "Open path · I = 0 A" : "Source → load → return", compact ? 20 : 24);
    out += text(middle, bottom+134, open ? "Voltage can remain across the gap" : "Complete loop · ideal DC", compact ? 17 : 19, "muted");
  } else {
    out += text((left+right)/2, mode === "voltage-current" ? top-gap-20 : top-30, "2 A through this path", compact ? 18 : 24, "power");
    if (power) {
      out += text(compact ? 195 : 1010, compact ? 558 : 255, "Power P", 25);
      out += text(compact ? 195 : 1010, compact ? 602 : 306, "P = V × I", 26, "power");
      out += text(compact ? 195 : 1010, compact ? 644 : 350, "12 V × 2 A = 24 W", compact ? 22 : 21);
      out += text(compact ? 195 : 1010, compact ? 680 : 391, "Ideal, steady DC", 17, "muted");
    } else {
      const vx = compact ? 337 : 1030, vtop = cy-lh/2, vbottom = cy+lh/2;
      out += path(`M${right} ${vtop}H${vx}V${cy-27}M${vx} ${cy+27}V${vbottom}H${right}`, "data", 2, 'stroke-dasharray="5 6"');
      out += dot(right, vtop, "data") + dot(right, vbottom, "data");
      out += `<circle cx="${vx}" cy="${cy}" r="${compact ? 27 : 32}" fill="var(--surface)" stroke="var(--data)" stroke-width="2"/>`;
      out += text(vx, cy+5, "12 V", compact ? 17 : 21, "data");
      out += text(compact ? 195 : 850, compact ? 550 : 505, "Voltage V: between two points", compact ? 20 : 24, "data");
      out += text(compact ? 195 : 850, compact ? 592 : 543, "Current I: through a path", compact ? 20 : 24, "power");
      out += text(compact ? 195 : 850, compact ? 642 : 580, "V = volts   ·   A = amperes", compact ? 19 : 21, "muted");
    }
  }
  return out;
}

function resistance(compact, state) {
  const volts = Number(state.resistanceVoltage) === 24 ? 24 : 12, amps = volts/6, watts = amps*amps*6;
  const left = compact ? 65 : 200, right = compact ? 290 : 760, top = compact ? 145 : 125, bottom = compact ? 405 : 435;
  const cy = (top+bottom)/2;
  let out = text(compact ? 195 : 580, compact ? 52 : 49, "Fixed resistor: R = 6 Ω", 25);
  out += path(`M${left} ${cy-35}V${top}H${right}V${cy-55}M${right} ${cy+55}V${bottom}H${left}V${cy+35}`);
  out += `<circle cx="${left}" cy="${cy}" r="35" fill="var(--surface)" stroke="var(--power)" stroke-width="3"/>`;
  out += text(left, cy-8, "+", 24, "power") + text(left, cy+25, "−", 24, "power");
  out += text(left, bottom+43, `${volts} V DC`, compact ? 20 : 24, "power");
  out += arrow(`M${left+55} ${top}H${right-40}`) + text((left+right)/2, top-26, `${amps} A`, 25, "power");
  out += arrow(`M${right-35} ${bottom}H${left+55}`);
  out += rect(right-42, cy-55, 84, 110, "heat") + text(right, cy+8, "6 Ω", 24, "heat");
  out += Array.from({length: amps === 2 ? 1 : 4}, (_, i) => {
    const yy = cy+(i-(amps === 2 ? 0 : 1.5))*22;
    return compact ? arrow(`M${right-49} ${yy}H${right-120}`, "heat", 3) : arrow(`M${right+49} ${yy}H${right+140}`, "heat", 3);
  }).join("");
  if (compact) {
    out += text(195, 526, `I = ${volts} V ÷ 6 Ω = ${amps} A`, 24, "power");
    out += text(195, 582, `P = ${amps}² × 6 = ${watts} W`, 26, "heat");
    out += text(195, 627, "Resistor heating · I²R", 21, "heat");
    out += text(195, 676, "Ideal source and wires", 18, "muted");
  } else {
    out += text(964, 331, `${watts} W of heat`, 26, "heat");
    out += text(355, 522, `I = ${volts} V ÷ 6 Ω = ${amps} A`, 26, "power");
    out += text(840, 522, `P = ${amps}² × 6 = ${watts} W`, 26, "heat");
    out += text(580, 576, "Ideal source and wires · resistor heating is I²R", 21, "muted");
  }
  return `<g data-volts="${volts}" data-amps="${amps}" data-heat-watts="${watts}">${out}</g>`;
}

function energy(compact, state) {
  const hours = Number(state.hours) === 1 ? 1 : 2;
  const x = compact ? 38 : 180, w = compact ? 314 : 800, y = compact ? 166 : 170;
  let out = text(compact ? 195 : 580, compact ? 48 : 57, "Energy = power × time", 26);
  out += text(compact ? 195 : 580, compact ? 92 : 105, `Constant 1 kW load for ${hours} ${hours === 1 ? "hour" : "hours"}`, compact ? 20 : 24, "power");
  out += rect(x, y, w, compact ? 165 : 170, "line", "surface", 0);
  out += rect(x, y, w*hours/2, compact ? 165 : 170, "power", "panel", 0);
  out += path(`M${x+w/2} ${y}V${y+(compact ? 165 : 170)}`, "line", 2, 'stroke-dasharray="5 6"');
  out += text(x+w/4, y+94, "1 kWh", compact ? 24 : 26, "power");
  if (hours === 2) out += text(x+3*w/4, y+94, "1 kWh", compact ? 24 : 26, "power");
  [0, 1, 2].forEach((h) => { out += text(x+h*w/2, y+207, `${h} h`, compact ? 19 : 23, "muted"); });
  out += text(compact ? 195 : 580, compact ? 430 : 450, `1 kW × ${hours} h = ${hours} kWh`, 26, "power");
  if (compact) {
    out += text(195, 511, "kilo (k) = 1,000", 21) + text(195, 552, "mega (M) = 1,000,000", 21) + text(195, 593, "giga (G) = 1,000,000,000", 21);
    out += text(195, 655, "kW is power · kWh is energy", 20, "muted");
  } else {
    out += text(260, 534, "k = 1,000", 23) + text(580, 534, "M = 1,000,000", 23) + text(940, 534, "G = 1,000,000,000", 23);
  }
  return `<g data-hours="${hours}" data-energy-kwh="${hours}">${out}</g>`;
}

const wave = (x, mid, width, amplitude, phase = 0, cycles = 2) =>
  Array.from({length: 181}, (_, i) => `${i ? "L" : "M"}${(x+width*i/180).toFixed(2)} ${(mid-amplitude*Math.sin(i/180*Math.PI*2*cycles+phase)).toFixed(2)}`).join("");
function axes(x, mid, width, amplitude, compact) {
  return path(`M${x} ${mid-amplitude-16}V${mid+amplitude+16}`, "line", 2) +
    arrow(`M${x} ${mid}H${x+width+8}`, "muted", 2) +
    text(x-11, mid+6, "0", 17, "muted") +
    text(x+width, mid+amplitude+44, "time →", compact ? 17 : 19, "muted", "end");
}
function acdc(compact, state) {
  const angle = [90,180,270].includes(Number(state.angle)) ? Number(state.angle) : 90;
  let out = "";
  ["DC", "AC"].forEach((kind, i) => {
    const x = compact ? 52 : 135+i*550, width = compact ? 280 : 380;
    const mid = compact ? 205+i*295 : 298, amp = compact ? 60 : 92;
    out += text(x+width/2, mid-amp-61, kind === "DC" ? "Direct current (DC)" : "Alternating current (AC)", compact ? 23 : 26);
    out += text(x, mid-amp-25, "current", 18, "muted", "start") + axes(x, mid, width, amp, compact);
    out += kind === "DC" ? path(`M${x} ${mid-amp*.70}H${x+width}`, "power", 4) : path(wave(x, mid, width, amp), "data", 4);
    if (kind === "AC") {
      const sampleX = x+width*angle/720, sampleY = mid-amp*Math.sin(angle*Math.PI/180);
      out += path(`M${sampleX} ${mid-amp-8}V${mid+amp+8}`, "data", 2, 'stroke-dasharray="4 5"') + dot(sampleX, sampleY, "data");
    }
    out += text(x+width/2, mid+amp+82, kind === "DC" ? "Constant, one direction" : angle === 90 ? "Positive current →" : angle === 270 ? "← Negative current" : "Zero current at this instant", compact ? 19 : 23, kind === "DC" ? "power" : "data");
    if (kind === "AC") out += text(x+width/2, mid+amp+118, "60 Hz = 60 cycles each second", compact ? 18 : 21, "muted");
  });
  return `<g data-phase-angle="${angle}" data-ac-current-sign="${angle === 90 ? 1 : angle === 270 ? -1 : 0}">${out}</g>`;
}

function threePhase(compact) {
  const x = compact ? 46 : 120, width = compact ? 300 : 930;
  let out = "";
  const amps = compact ? 39 : 90;
  const phases = [0, -2*Math.PI/3, -4*Math.PI/3];
  if (compact) {
    ["A", "B", "C"].forEach((label, i) => {
      const mid = 117+i*148, color = ["power", "data", "heat"][i];
      out += text(x, mid-57, `Phase ${label}`, 20, color, "start");
      out += axes(x, mid, width, amps, true) + path(wave(x, mid, width, amps, phases[i], 1), color, 3);
    });
    out += text(195, 547, "Equal sine waves · 120° apart", 21);
    out += text(195, 593, "RMS: effective AC magnitude", 19, "muted");
    out += text(195, 629, "Power factor (PF) = kW ÷ kVA", 20);
    out += text(195, 677, "Phase voltages · common reference", 17, "muted");
  } else {
    const mid = 265;
    out += axes(x, mid, width, amps, false);
    phases.forEach((phase, i) => {
      const color = ["power", "data", "heat"][i];
      out += path(wave(x, mid, width, amps, phase, 1), color, 4);
      out += path(`M${275+i*280} 72H${315+i*280}`, color, 4) + text(330+i*280, 79, `Phase ${["A", "B", "C"][i]}`, 23, color, "start");
    });
    out += text(580, 434, "Equal sine waves · 120° apart", 26);
    out += text(580, 483, "RMS: effective AC magnitude · Power factor (PF) = kW ÷ kVA", 25);
    out += text(580, 526, "Phase voltages share one reference", 22, "muted");
  }
  return out;
}

function acSymbol(x, y, width, color = "power") {
  return path(wave(x, y, width, 10, 0, 1.5), color, 3);
}
function dcSymbol(x, y, width) {
  return path(`M${x} ${y-5}H${x+width}`, "power", 3) + path(`M${x} ${y+5}H${x+width}`, "power", 2, 'stroke-dasharray="5 5"');
}
function conversion(compact) {
  const rows = [
    ["Transformer", "AC", "AC", "Changes AC voltage"],
    ["Rectifier", "AC", "DC", "AC → DC"],
    ["Inverter", "DC", "AC", "DC → AC"],
    ["Power supply (PSU)", "AC", "DC", "Regulated DC for electronics"],
  ];
  let out = "";
  rows.forEach(([name, input, output, job], i) => {
    const y = compact ? 64+i*165 : 68+i*139;
    if (compact) {
      out += text(195, y, name, 23);
      out += rect(120, y+20, 150, 65, "power");
      if (i === 0) {
        out += path(`M153 ${y+33}c18 0 18 12 0 12c18 0 18 12 0 12c18 0 18 12 0 12M237 ${y+33}c-18 0 -18 12 0 12c-18 0 -18 12 0 12c-18 0 -18 12 0 12M192 ${y+29}v46M198 ${y+29}v46`, "power", 2);
      } else out += text(195, y+61, i === 3 ? "AC/DC example" : `${input} → ${output}`, 18, "power");
      out += text(54, y+34, input, 18) + text(336, y+34, output, 18);
      out += arrow(`M70 ${y+54}H112`, "power", 3) + arrow(`M278 ${y+54}H320`, "power", 3);
      out += text(195, y+119, job, 19, "muted");
    } else {
      out += text(70, y+37, name, 24, "text", "start");
      out += text(400, y+7, input, 20, "muted");
      out += (input === "AC" ? acSymbol(371, y+40, 58) : dcSymbol(371, y+40, 58));
      out += arrow(`M446 ${y+40}H491`, "power", 3);
      out += rect(505, y+7, 170, 65, "power");
      if (i === 0) out += path(`M547 ${y+22}c18 0 18 12 0 12c18 0 18 12 0 12c18 0 18 12 0 12M633 ${y+22}c-18 0 -18 12 0 12c-18 0 -18 12 0 12c-18 0 -18 12 0 12M587 ${y+17}v46M593 ${y+17}v46`, "power", 2);
      else out += text(590, y+49, i === 3 ? "AC/DC example" : `${input} → ${output}`, 21, "power");
      out += arrow(`M689 ${y+40}H734`, "power", 3);
      out += text(780, y+7, output, 20, "muted");
      out += (output === "AC" ? acSymbol(751, y+40, 58) : dcSymbol(751, y+40, 58));
      out += text(850, y+47, job, 21, "muted", "start");
    }
  });
  return out;
}

export function renderElectricity(id, state = {}, compact = false) {
  const renderers = {
    circuit: () => circuit(compact, "circuit", state),
    "voltage-current": () => circuit(compact, "voltage-current"),
    resistance: () => resistance(compact, state),
    power: () => circuit(compact, "power"),
    energy: () => energy(compact, state),
    "ac-dc": () => acdc(compact, state),
    "three-phase": () => threePhase(compact),
    conversion: () => conversion(compact),
  };
  return renderers[id] ? `<g data-electricity-scene="${id}">${defs}${renderers[id]()}</g>` : "";
}
