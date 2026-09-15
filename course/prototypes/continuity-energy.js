import {
  CAPACITOR_EXAMPLE,
  capacitorEnergyModel,
  capacitorModel,
  recoveryModel,
  recoveryPlan,
} from "./ups-capacitors.js";

const text = (x, y, value, size = 24, color = "ink", anchor = "start", weight = 400) =>
  `<text x="${x}" y="${y}" fill="var(--${color})" font-size="${size}" font-weight="${weight}" text-anchor="${anchor}">${value}</text>`;
const path = (d, color = "ink", width = 2, extra = "") =>
  `<path d="${d}" fill="none" stroke="var(--${color})" stroke-width="${width}" ${extra}/>`;
const dot = (x, y, color = "green") =>
  `<circle cx="${x}" cy="${y}" r="5" fill="var(--${color})"/>`;
const usableEnergyEquation = 'ΔE = ½C(V<tspan baseline-shift="sub" font-size="70%">start</tspan><tspan baseline-shift="baseline">² − V</tspan><tspan baseline-shift="sub" font-size="70%">min</tspan><tspan baseline-shift="baseline">²)</tspan>';
const frame = (title, description, svg, compact, height = 440, compactHeight = 650) => ({
  viewBox: `0 0 ${compact ? 380 : 1180} ${compact ? compactHeight : height}`,
  svg: `<title>${title}</title><desc>${description}</desc><g class="continuity-energy">${svg}</g>`,
});

export function renderCapacitanceDiagram({ compact = false } = {}) {
  const x = compact ? 190 : 300, top = compact ? 68 : 62;
  const plateLeft = x - 53, plateRight = x + 53, bottom = top + 222;
  const plates = `${path(`M${plateLeft} ${top}V${bottom}`, "green", 9)}${path(`M${plateRight} ${top}V${bottom}`, "blue", 9)}
    ${[0, 1, 2, 3].map(i => `${text(plateLeft - 27, top + 30 + i * 55, "+", 31, "green", "middle")}${text(plateRight + 27, top + 30 + i * 55, "−", 31, "blue", "middle")}`).join("")}
    ${text(x - 100, top - 24, "+160 coulombs", compact ? 18 : 23, "green", "middle")}
    ${text(x + 100, top - 24, "−160 coulombs", compact ? 18 : 23, "blue", "middle")}
    ${path(`M${plateLeft} ${bottom + 27}H${plateRight}`, "ink", 2)}
    ${path(`M${plateLeft + 8} ${bottom + 22}l-8 5 8 5 M${plateRight - 8} ${bottom + 22}l8 5 -8 5`, "ink", 2)}
    ${text(x, bottom + 61, "800 V", 29, "ink", "middle")}`;
  const body = compact
    ? `${text(190, 420, "C = 0.20 F", 32, "green", "middle", 600)}${text(190, 458, "0.20 coulomb per volt", 22, "ink", "middle")}
       ${text(190, 525, "Charge = capacitance × voltage", 21, "ink", "middle")}${text(190, 577, "Q = C × V", 35, "ink", "middle")}
       ${text(190, 628, "= 0.20 × 800 = 160 coulombs", 23, "ink", "middle")}`
    : `${text(660, 81, "C = 0.20 F", 40, "green", "start", 600)}${text(660, 129, "0.20 coulomb per volt", 28)}
       ${text(660, 212, "Charge = capacitance × voltage", 26)}${text(660, 274, "Q = C × V", 44)}
       ${text(660, 337, "= 0.20 × 800 = 160 coulombs", 28)}`;
  return {...frame("Capacitance relates charge to voltage", "Capacitance C is measured in farads. One farad means one coulomb of plate charge per volt. Our fixed 0.20 farad capacitor at 800 volts has a charge magnitude Q of 160 coulombs on either plate, with opposite signs. Q equals C times V describes a stored state. Current instead measures charge passing per second, and P equals I times V describes the rate of energy transfer.", plates + body, compact, 420, 670), model: capacitorEnergyModel()};
}

export function renderCapacitorEnergyDiagram({ compact = false } = {}) {
  const left = compact ? 55 : 100, right = compact ? 334 : 598;
  const top = compact ? 64 : 64, bottom = compact ? 295 : 340;
  const half = (top + bottom) / 2;
  const graph = `<polygon points="${left},${bottom} ${right},${top} ${right},${bottom}" fill="var(--green)" opacity=".15"/>
    ${path(`M${left} ${top - 5}V${bottom}H${right + 10}`, "muted")}
    ${path(`M${left} ${bottom}L${right} ${top}`, "green", 4)}
    ${path(`M${left} ${half}H${right}`, "gold", 2, 'stroke-dasharray="7 6"')}
    ${text(left, top - 24, "Voltage (V)", 22)}
    ${[[top, "800"], [half, "400"], [bottom, "0"]].map(([y, v]) => text(left - 11, y + 7, v, 20, "ink", "end")).join("")}
    ${text(right, bottom + 30, "160", 22, "ink", "middle")}
    ${text(left, bottom + 62, "Charge added (coulombs)", 21)}
    ${text(right - 7, half - 17, "Average: 400 V", compact ? 19 : 23, "gold", "end")}`;
  const equations = compact
    ? `${text(190, 435, "Energy = charge × average voltage", 20, "ink", "middle")}
       ${text(190, 486, "E = 160 × 400 = 64,000 J", 27, "green", "middle", 600)}
       ${text(190, 550, "E = Q × (V / 2)", 28, "ink", "middle")}
       ${text(190, 603, "= (C × V) × (V / 2)", 27, "ink", "middle")}
       ${text(190, 656, "= ½CV²", 35, "green", "middle", 600)}`
    : `${text(700, 92, "Charge × average voltage", 28)}
       ${text(700, 150, "160 × 400 = 64,000 J", 35, "green", "start", 600)}
       ${text(700, 229, "E = Q × (V / 2)", 33)}
       ${text(700, 289, "= (C × V) × (V / 2)", 33)}
       ${text(700, 355, "= ½CV²", 43, "green", "start", 600)}`;
  return {
    ...frame("Why capacitor energy includes one half", "For a fixed capacitance, voltage rises linearly as charge is added. Charging from zero to 800 volts adds 160 coulombs. Equal portions of charge encounter progressively larger voltages, with an average of 400 volts. One volt is one joule per coulomb, so 160 coulombs times 400 volts stores 64,000 joules. This is the area of the voltage-charge triangle. Substitute Q equals C times V into E equals Q times V over two to obtain E equals one half C V squared. The average is over charge added, not over an arbitrary time interval.", graph + equations, compact, 430, 690),
    model: capacitorEnergyModel(),
  };
}

export function renderHoldUpDiagram({ compact = false } = {}) {
  const e = capacitorEnergyModel();
  const cutoff = capacitorModel("alone", 15);
  const left = compact ? 56 : 85, right = compact ? 336 : 575;
  const top = compact ? 89 : 98, bottom = compact ? 290 : 336;
  const x = ms => left + ms / 15 * (right - left);
  const y = voltage => bottom - (voltage - 680) / 140 * (bottom - top);
  const curve = Array.from({ length: 61 }, (_, i) => i / 4)
    .map((ms, i) => `${i ? "L" : "M"}${x(ms)},${y(capacitorModel("alone", ms).voltageV)}`).join(" ");
  const equations = compact
    ? `${text(24, 405, usableEnergyEquation, 25)}${text(24, 450, "= ½ × 0.20 × (800² − 700²)", 23)}${text(24, 506, "= 15,000 J", 33, "green", "start", 600)}${text(24, 575, "t = 15,000 J / 1,000,000 W", 23)}${text(24, 621, "= 15 ms", 33, "green", "start", 600)}${text(24, 680, "49 kJ remains below the cutoff", 21)}`
    : `${text(679, 106, usableEnergyEquation, 30)}${text(679, 157, "= ½ × 0.20 × (800² − 700²)", 26)}${text(679, 223, "= 15,000 J", 41, "green", "start", 600)}${text(679, 300, "t = 15,000 J / 1,000,000 W", 26)}${text(679, 361, "= 15 ms", 41, "green", "start", 600)}`;
  const svg = `${text(compact ? 190 : 590, 31, "C = 0.20 F   ·   load = 1 MW", compact ? 22 : 25, "ink", "middle")}
    ${path(`M${left} ${top}V${bottom}H${right}`, "muted")}
    ${text(left, top - 15, "Bus voltage (V)", 21)}
    ${[700, 800].map(v => `${text(left - 12, y(v) + 7, v, 21, "ink", "end")}${path(`M${left} ${y(v)}H${right}`, v === 700 ? "gold" : "line", 1.5, v === 700 ? 'stroke-dasharray="6 6"' : "")}`).join("")}
    ${path(curve, "green", 4)}${dot(x(15), y(700))}
    ${text(right, y(700) + 25, "Load cutoff", 21, "gold", "end")}
    ${[0, 5, 10, 15].map(ms => text(x(ms), bottom + 29, ms, 20, "ink", "middle")).join("")}
    ${text(right, bottom + 59, "Time without supply (ms)", 20, "ink", "end")}
    ${compact ? "" : text(left, 437, "At 700 V: 49 kJ remains in the capacitor", 21)}
    ${equations}`;
  return {
    ...frame(
      "How long the DC-link capacitor supports a one megawatt load",
      "Capacitance is 0.20 farads. The voltage can fall from 800 to 700 volts before the load shuts down. The useful energy is the difference in stored energy: one half times 0.20 times the difference of the two squared voltages equals fifteen thousand joules. Dividing by one million watts gives fifteen milliseconds. At 700 volts, forty-nine kilojoules remains stored but cannot support this load above its cutoff voltage.",
      svg, compact, 462, 712,
    ),
    model: { ...e, ...cutoff },
  };
}

export function renderBatteryRampDiagram({ compact = false } = {}) {
  const model = capacitorModel("ramp", CAPACITOR_EXAMPLE.rampMs);
  const left = compact ? 52 : 84, right = compact ? 336 : 581;
  const top = compact ? 76 : 70, bottom = compact ? 251 : 235;
  const x = ms => left + ms / 20 * (right - left);
  const powerY = p => bottom - p / 1e6 * (bottom - top);
  const vTop = compact ? 553 : 313, vBottom = compact ? 654 : 393;
  const vy = v => vBottom - (v - 760) / 45 * (vBottom - vTop);
  const voltage = Array.from({ length: 81 }, (_, i) => i / 4)
    .map((ms, i) => `${i ? "L" : "M"}${x(ms)},${vy(capacitorModel("ramp", ms).voltageV)}`).join(" ");
  const equations = compact
    ? `${text(25, 341, "Capacitor deficit = triangle area", 22)}${text(25, 388, "ΔE = ½ × 1 MW × 10 ms", 25)}${text(25, 435, "= 5 kJ", 33, "gold", "start", 600)}${text(25, 498, "V² = 800² − 2 × 5,000 / 0.20", 23)}${text(25, 733, "V = 768.1 V", 31, "green", "start", 600)}${text(25, 778, "After 10 ms: battery = load", 23)}`
    : `${text(691, 87, "Capacitor deficit = triangle area", 24)}${text(691, 143, "ΔE = ½ × 1 MW × 10 ms", 30)}${text(691, 208, "= 5 kJ", 43, "gold", "start", 600)}${text(691, 282, "½C(800² − V²) = 5,000 J", 28)}${text(691, 336, "V² = 800² − 2 × 5,000 / 0.20", 26)}${text(691, 399, "V = 768.1 V", 39, "green", "start", 600)}`;
  const svg = `${text(left, top - 29, "Power (MW)", 22)}
    <polygon points="${x(0)},${top} ${x(10)},${top} ${x(0)},${bottom}" fill="var(--gold)" opacity=".4"/>
    <polygon points="${x(0)},${bottom} ${x(10)},${top} ${x(20)},${top} ${x(20)},${bottom}" fill="var(--green)" opacity=".17"/>
    ${path(`M${left} ${top}V${bottom}H${right}`, "muted")}
    ${path(`M${left} ${top}H${right}`, "ink", 1.5, 'stroke-dasharray="6 6"')}
    ${path(`M${x(0)} ${bottom}L${x(10)} ${top}H${x(20)}`, "green", 4)}
    ${text(left - 12, top + 7, "1", 22, "ink", "end")}${text(left - 12, bottom + 7, "0", 22, "ink", "end")}
    ${text(x(20), top - 15, "1 MW load", 21, "ink", "end")}
    ${text(x(1), top + 34, "Capacitor", compact ? 18 : 22, "gold")}
    ${text(x(13), bottom - 34, "Battery", compact ? 20 : 24, "green", "middle")}
    ${[0, 10, 20].map(ms => text(x(ms), bottom + 30, `${ms}${ms === 20 ? " ms" : ""}`, 21, "ink", "middle")).join("")}
    ${text(left, vTop - 17, "Bus voltage (V)", 21)}
    ${path(`M${left} ${vTop}V${vBottom}H${right}`, "muted")}
    ${text(left - 11, vy(800) + 6, "800", 19, "ink", "end")}
    ${path(voltage, "green", 4)}${dot(x(10), vy(model.voltageV))}
    ${text(right, vy(model.voltageV) - 14, "768.1", 22, "green", "end")}
    ${[0, 10, 20].map(ms => text(x(ms), vBottom + 28, `${ms}${ms === 20 ? " ms" : ""}`, 20, "ink", "middle")).join("")}
    ${compact ? "" : text(691, 453, "After 10 ms: battery power equals load power", 22)}
    ${equations}`;
  return {
    ...frame(
      "A ten millisecond battery ramp uses five kilojoules",
      "Battery power rises linearly from zero to one megawatt during ten milliseconds. The capacitor supplies the difference between the flat load line and the rising battery line. The triangular deficit area is one half times one megawatt times ten milliseconds, or five kilojoules. Solving one half C times the difference of squared voltages equals five thousand joules gives 768.1 volts. After ten milliseconds the battery matches the load, so there is no further capacitor discharge and no recharge yet.",
      svg, compact, 478, 814,
    ),
    model,
  };
}

export function renderRecoveryComparison(source = "battery", { compact = false } = {}) {
  if (!["battery", "rectifier"].includes(source)) throw new RangeError("Unknown recovery source");
  const sourceLabel = source === "battery" ? "Battery → DC/DC" : "Running generator → rectifier";
  const cases = [
    { label: "1.00 MW", surplusW: 0, color: "muted", duration: "No recovery" },
    { label: "1.05 MW", ...recoveryPlan(100), color: "gold", duration: "100 ms" },
    { label: "1.10 MW", ...recoveryPlan(50), color: "green", duration: "50 ms" },
  ];
  const left = compact ? 63 : 90, right = compact ? 331 : 594;
  const top = compact ? 139 : 126, bottom = compact ? 321 : 339;
  const x = ms => left + ms / 120 * (right - left);
  const y = v => bottom - (v - 763) / 42 * (bottom - top);
  const graph = `${text(left, top - 19, "Bus voltage (V)", 21)}
    ${path(`M${left} ${top}V${bottom}H${right}`, "muted")}
    ${[768.1, 800].map(v => `${text(left - 10, y(v) + 7, v, 20, "ink", "end")}${path(`M${left} ${y(v)}H${right}`, "line", 1.5, 'stroke-dasharray="6 6"')}`).join("")}
    ${cases.map(c => path(Array.from({ length: 121 }, (_, ms) => `${ms ? "L" : "M"}${x(ms)},${y(recoveryModel(ms, c.surplusW).voltageV)}`).join(" "), c.color, 4, c.surplusW === 0 ? 'stroke-dasharray="7 5"' : "")).join("")}
    ${[50, 100].map(ms => `${dot(x(ms), y(800), ms === 50 ? "green" : "gold")}${text(x(ms), bottom + 28, ms, 20, "ink", "middle")}`).join("")}
    ${text(left, bottom + 28, "0", 20, "ink", "middle")}
    ${text(right, bottom + 57, "Recovery time (ms)", 21, "ink", "end")}`;
  const comparison = compact
    ? cases.map((c, i) => {
      const yy = 460 + i * 77;
      return `${path(`M26 ${yy - 27}H352`, "line", 1)}${text(28, yy, c.label, 25, c.color, "start", 600)}${text(352, yy, c.duration, 25, c.color, "end", 600)}${text(28, yy + 29, `${c.surplusW / 1000} kW to capacitor`, 20)}`;
    }).join("")
    : `<g>${text(695, 132, "At the bus", 21)}${text(916, 132, "Surplus", 21, "ink", "middle")}${text(1145, 132, "Recovery", 21, "ink", "end")}
    ${cases.map((c, i) => {
      const yy = 185 + i * 67;
      return `${path(`M682 ${yy - 30}H1156`, "line", 1)}${text(695, yy, c.label, 27, c.color, "start", 600)}${text(916, yy, `${c.surplusW / 1000} kW`, 25, c.color, "middle")}${text(1145, yy, c.duration, 25, c.color, "end")}`;
    }).join("")}</g>`;
  const equations = compact
    ? `${text(26, 791, "At 800 V: reduce source to 1 MW", 22)}`
    : `${text(695, 443, "At 800 V: reduce source to 1 MW", 24)}`;
  const svg = `${text(compact ? 190 : 590, 31, sourceLabel, compact ? 22 : 27, "ink", "middle")}
    ${text(compact ? 190 : 590, 71, "1 MW load   ·   5 kJ to restore", compact ? 23 : 27, "ink", "middle")}
    ${graph}${comparison}${equations}`;
  return {
    ...frame(
      "Recovery power determines how quickly the DC link returns to 800 volts",
      "The load still draws one megawatt and the capacitor is missing five kilojoules. A source delivering one megawatt leaves no surplus and holds 768.1 volts. Restoring five kilojoules in one hundred milliseconds requires fifty kilowatts extra, giving 1.05 megawatts total. Restoring it in fifty milliseconds requires one hundred kilowatts extra, giving 1.10 megawatts total. Either an available battery DC/DC converter or generator-fed rectifier can supply this power. Voltage control reduces the capacitor-charging contribution to zero at 800 volts, leaving one megawatt for the load.",
      svg, compact, 472, 826,
    ),
    model: { cases, initialV: recoveryModel(0).voltageV, missingJ: recoveryModel(0).missingJ },
  };
}
