const phaseColors = [
  "var(--phase-one)",
  "var(--phase-two)",
  "var(--phase-three)",
];

function waveView(angle) {
  const dc = acdcWaveModel("dc-basics", angle);
  const ac = acdcWaveModel("ac-basics", angle);
  const three = acdcWaveModel("three-phase", angle);
  return {
    dcVoltage: dc.phases[0].voltageV,
    dcCurrent: dc.phases[0].currentA,
    dcPower: dc.instantKW,
    singleVoltage: ac.phases[0].voltageV,
    singleCurrent: ac.phases[0].currentA,
    singlePower: ac.instantKW,
    phaseCurrents: three.phases.map((p) => p.currentA),
    phasePowers: three.phases.map((p) => p.powerKW),
    phaseVoltage1: three.phases[0].voltageV,
    phaseVoltage2: three.phases[1].voltageV,
    phaseVoltage3: three.phases[2].voltageV,
    threePower: three.instantKW,
    lineVoltage: three.lineABVoltageV,
  };
}

function electricalPlot(
  title,
  series,
  low,
  high,
  unit,
  angle = state.cycleDegrees,
) {
  const left = 56,
    right = 594,
    top = 10,
    bottom = 60;
  const x = (degrees) => left + ((right - left) * degrees) / 360;
  const y = (value) => bottom - ((bottom - top) * (value - low)) / (high - low);
  const ticks = [...new Set([low, 0, (low + high) / 2, high])].filter(
    (v) => v >= low && v <= high,
  );
  const paths = series
    .map((s) => {
      const d = Array.from(
        { length: 121 },
        (_, n) =>
          `${n ? "L" : "M"}${x(n * 3).toFixed(2)},${y(s.value(n * 3)).toFixed(2)}`,
      ).join(" ");
      return `<path d="${d}" fill="none" stroke="${s.color}" stroke-width="${s.width || 2.5}" ${s.dash ? 'stroke-dasharray="6 4"' : ""}/><circle cx="${x(angle)}" cy="${y(s.value(angle))}" r="4.5" fill="${s.color}" stroke="var(--paper)" stroke-width="1.5"/>`;
    })
    .join("");
  return `<section class="electrical-plot"><h3>${title} <small>${unit}</small></h3><svg viewBox="0 0 620 90" role="img" aria-label="${escapeHTML(title)} over one cycle; dashed vertical marker shows ${angle} degrees within the 60 Hz reference interval.">${ticks.map((v) => `<line x1="${left}" x2="${right}" y1="${y(v)}" y2="${y(v)}" stroke="var(--line)"/><text x="${left - 8}" y="${y(v) + 4}" text-anchor="end">${fmt(v)}</text>`).join("")}<line x1="${x(angle)}" x2="${x(angle)}" y1="${top}" y2="${bottom}" stroke="var(--muted)" stroke-dasharray="3 5"/>${paths}${[0, 90, 180, 270, 360].map((d) => `<text x="${x(d)}" y="82" text-anchor="middle">${fmt((d / 360 / 60) * 1000, 1)} ms</text>`).join("")}</svg><div class="wave-key">${series.map((s) => `<span style="--wave-color:${s.color}">${s.label}</span>`).join("")}</div></section>`;
}

function directionArrow(x, y, current, color = "var(--phase-one)") {
  if (Math.abs(current) < 0.01)
    return `<circle cx="${x}" cy="${y}" r="5" fill="${color}"/><text x="${x}" y="${y - 18}" text-anchor="middle">0 A</text>`;
  const right = current > 0;
  return `<path d="M${x + (right ? -22 : 22)},${y} H${x + (right ? 22 : -22)} m${right ? -9 : 9},-7 l${right ? 9 : -9},7 l${right ? -9 : 9},7" fill="none" stroke="${color}" stroke-width="4"/><text x="${x}" y="${y - 18}" text-anchor="middle">${fmt(Math.abs(current), 1)} A</text>`;
}

function circuitLoop(dc, instant) {
  const current = dc ? 125 : instant.singleCurrent;
  const volts = dc ? 800 : instant.singleVoltage;
  const power = dc ? 100 : instant.singlePower;
  const polarity =
    volts < -0.01 ? ["−", "+"] : volts > 0.01 ? ["+", "−"] : ["0", "0"];
  return `<svg class="current-circuit" viewBox="0 0 470 290" role="img" aria-label="Arrows show instantaneous conventional current. Closed two-conductor circuit. Conventional current ${current < 0 ? "reverses" : "leaves the positive source terminal and returns through the other conductor"}. The ideal resistive load absorbs ${fmt(power, 1)} kilowatts."><rect class="circuit-box" x="20" y="56" width="94" height="186" rx="12"/><rect class="circuit-box load" x="346" y="56" width="104" height="186" rx="12"/><path class="circuit-wire" d="M114 82H346 M114 216H346"/><text x="67" y="144" text-anchor="middle">${dc ? "DC" : "AC"}</text><text x="67" y="167" text-anchor="middle" class="svg-small">source</text><text x="97" y="89">${polarity[0]}</text><text x="97" y="222">${polarity[1]}</text><text x="398" y="136" text-anchor="middle">Load</text><text x="398" y="187" text-anchor="middle" class="svg-value">${fmt(power, 1)} kW</text>${directionArrow(226, 82, current)}${directionArrow(226, 216, -current)}<text x="230" y="278" text-anchor="middle" class="svg-small">${dc ? "800 V across the load" : "Polarity reverses · " + fmt(volts, 1) + " V now"}</text></svg>`;
}

function threePhaseCircuit(instant) {
  return `<svg class="current-circuit" viewBox="0 0 470 290" role="img" aria-label="Arrows show instantaneous conventional current. Three conductors connect a balanced source and wye-connected resistive load. Signed line currents sum to zero; other lines carry the return current."><rect class="circuit-box" x="10" y="24" width="88" height="212" rx="12"/><text x="54" y="123" text-anchor="middle">AC</text><text x="54" y="146" text-anchor="middle" class="svg-small">source</text><rect class="circuit-box load" x="318" y="24" width="142" height="212" rx="12"/><text x="391" y="45" text-anchor="middle" class="svg-small">Balanced load</text>${instant.phaseCurrents
    .map((amps, n) => {
      const y = 75 + n * 65;
      return `<text x="108" y="${y + 22}" fill="${phaseColors[n]}" class="svg-small">L${n + 1}</text><path d="M98 ${y}H332" stroke="${phaseColors[n]}" stroke-width="3" fill="none"/>${directionArrow(215, y, amps, phaseColors[n])}<rect x="333" y="${y - 8}" width="36" height="16" fill="var(--paper)" stroke="${phaseColors[n]}" stroke-width="2"/><path d="M369 ${y}H429V140" stroke="${phaseColors[n]}" stroke-width="2" fill="none"/>`;
    })
    .join(
      "",
    )}<circle cx="429" cy="140" r="5" fill="var(--ink)"/><text x="235" y="267" text-anchor="middle" class="svg-small">i₁ + i₂ + i₃ = ${fmt(Math.abs(instant.phaseCurrents.reduce((a, b) => a + b, 0)) < 0.01 ? 0 : instant.phaseCurrents.reduce((a, b) => a + b, 0), 1)} A</text></svg>`;
}

function voltageMeasurement() {
  return `<div class="voltage-measurement"><svg viewBox="0 0 900 455" role="img" aria-labelledby="meter-title"><title id="meter-title">Voltmeter probes connect to live phase L1 and live phase L2. They measure 480 volts RMS. L3 is also live and is not ground.</title>${[80, 300, 390].map((y, n) => `<text x="36" y="${y + 8}" class="meter-line-label">L${n + 1} · live</text><path d="M180 ${y}H860" fill="none" stroke="${phaseColors[n]}" stroke-width="5"/>`).join("")}<circle cx="450" cy="80" r="7" fill="var(--phase-one)"/><path d="M450 80V135" fill="none" stroke="var(--phase-one)" stroke-width="4"/><circle cx="560" cy="300" r="7" fill="var(--phase-two)"/><path d="M560 245V300" fill="none" stroke="var(--phase-two)" stroke-width="4"/><rect x="385" y="135" width="240" height="110" rx="14" fill="var(--circuit-load)" stroke="var(--strong-line)" stroke-width="2"/><text x="505" y="183" text-anchor="middle" class="meter-number">480 V</text><text x="505" y="220" text-anchor="middle">RMS · L1 to L2</text><text x="785" y="165" text-anchor="middle" class="meter-note">Voltmeter</text></svg><p class="phase-measurement-note">All three phases are live. Protective earth is separate.</p></div>`;
}
function pairVoltages(angle) {
  const v = waveView(angle);
  return [
    v.phaseVoltage1 - v.phaseVoltage2,
    v.phaseVoltage2 - v.phaseVoltage3,
    v.phaseVoltage3 - v.phaseVoltage1,
  ];
}
function pairVoltageComparison() {
  const names = ["L1 − L2", "L2 − L3", "L3 − L1"],
    values = pairVoltages(state.cycleDegrees),
    x = (angle) => 65 + (angle / 360) * 660,
    y = (voltage) => 140 - (voltage / 700) * 110;
  const curves = names
    .map((name, i) => {
      const path = Array.from(
        { length: 121 },
        (_, n) =>
          `${n ? "L" : "M"}${x(n * 3).toFixed(2)} ${y(pairVoltages(n * 3)[i]).toFixed(2)}`,
      ).join(" ");
      return `<path d="${path}" fill="none" stroke="${phaseColors[i]}" stroke-width="4" ${i === 1 ? 'stroke-dasharray="9 7"' : ""}/><circle cx="${x(state.cycleDegrees)}" cy="${y(values[i])}" r="6" fill="${phaseColors[i]}" stroke="var(--paper)" stroke-width="2"/>`;
    })
    .join("");
  const signed = (value) =>
    Math.abs(value) < 0.05
      ? "0"
      : `${value > 0 ? "+" : "−"}${fmt(Math.abs(value), 1)}`;
  return `<div class="pair-comparison"><div class="pair-readings">${names.map((name, i) => `<div style="--pair-color:${phaseColors[i]}"><span>${name}</span><strong>480 <small>V RMS</small></strong><span data-pair-voltage="${i}">${signed(values[i])} V now</span></div>`).join("")}</div><svg class="pair-waveform" viewBox="0 0 780 285" role="img" aria-label="Three pair-voltage waveforms have the same RMS magnitude and different timing. Their signed instantaneous values sum to zero.">${[-680, 0, 680].map((v) => `<line x1="65" y1="${y(v)}" x2="725" y2="${y(v)}" stroke="var(--line)"/><text x="55" y="${y(v) + 6}" text-anchor="end">${v}</text>`).join("")}<line x1="${x(state.cycleDegrees)}" x2="${x(state.cycleDegrees)}" y1="25" y2="253" stroke="var(--muted)" stroke-dasharray="4 6"/>${curves}<text x="65" y="280">0</text><text x="725" y="280" text-anchor="end">One cycle</text></svg><p class="pair-identity">${values.map(signed).join(" + ").replaceAll("+ −", "− ").replaceAll("+ +", "+ ")} ≈ 0 V <span>Signed voltages now</span></p><p class="pair-principle">480 V is an RMS magnitude, not a fixed +480 V step.</p></div>`;
}
function electricalContent(kind) {
  const now = waveView(state.cycleDegrees);
  const make = (label, color, key, dash = false, width = 2.5) => ({
    label,
    color,
    value: (degrees) => waveView(degrees)[key],
    dash,
    width,
  });
  if (kind === "voltage-basis")
    return state.voltageView === "pairs"
      ? pairVoltageComparison()
      : voltageMeasurement();
  if (kind === "dc-basics") {
    return `<div class="dc-essential">${circuitLoop(true, now)}<div class="equation-block"><span>P = V × I</span><strong>800 V × 125 A = 100 kW</strong></div></div>`;
  }
  const three = kind === "three-phase";
  const charts = three
    ? electricalPlot(
        "Current in each phase",
        [0, 1, 2].map((n) => ({
          label: `L${n + 1}`,
          color: phaseColors[n],
          dash: n === 1,
          value: (d) => waveView(d).phaseCurrents[n],
        })),
        -180,
        180,
        "A",
      ) +
      electricalPlot(
        "Three phase powers add",
        [
          ...Array.from({ length: 3 }, (_, n) => ({
            label: `L${n + 1}`,
            color: phaseColors[n],
            width: 2,
            value: (d) => waveView(d).phasePowers[n],
          })),
          {
            label: "Total",
            color: "var(--ink)",
            width: 4,
            value: (d) => waveView(d).threePower,
          },
        ],
        0,
        120,
        "kW",
      )
    : electricalPlot(
        "Voltage reverses",
        [make("Voltage", phaseColors[0], "singleVoltage")],
        -800,
        800,
        "V",
      ) +
      electricalPlot(
        "Load power dips to zero",
        [
          make("Instantaneous power", phaseColors[0], "singlePower"),
          {
            label: "100 kW average",
            color: "var(--muted)",
            value: () => 100,
            dash: true,
          },
        ],
        0,
        200,
        "kW",
      );
  const result = three
    ? "100 kW total at every instant"
    : `${fmt(now.singleVoltage, 1)} V × ${fmt(now.singleCurrent, 1)} A = ${fmt(now.singlePower, 1)} kW now`;
  return `<div class="electrical-grid"><div class="electrical-circuit-panel">${three ? threePhaseCircuit(now) : circuitLoop(false, now)}<div class="wave-result">${result}</div></div><div class="electrical-charts">${charts}</div></div>`;
}
function electricalVisual(kind) {
  const scrub =
    ["ac-basics", "three-phase"].includes(kind) ||
    (kind === "voltage-basis" && state.voltageView === "pairs");
  const condition =
    kind === "dc-basics"
      ? "800 V DC · ideal wires"
      : kind === "ac-basics"
        ? "480 V RMS · single-phase model · resistive load"
        : kind === "three-phase"
          ? "480 V three-phase · balanced resistive load · PF = 1"
          : "Balanced 480 V three-phase system";
  return `<div class="electrical-model"><div class="energy-band"><strong>${kind === "voltage-basis" ? condition : "100 kW average at the load"}</strong>${kind === "voltage-basis" ? "" : `<span>${condition}</span>`}</div>${kind === "voltage-basis" ? `<div class="voltage-view-controls"><button data-voltage-view="meter" aria-pressed="${state.voltageView === "meter"}">Meter connections</button><button data-voltage-view="pairs" aria-pressed="${state.voltageView === "pairs"}">Why not 960 V?</button></div>` : ""}<div id="wave-content">${electricalContent(kind)}</div>${scrub ? `<div class="cycle-control"><label for="cycle-angle">One AC cycle · 60 Hz</label><input type="range" id="cycle-angle" min="0" max="360" step="1" value="${state.cycleDegrees}"/><output id="cycle-value" for="cycle-angle">${state.cycleDegrees}°</output></div>` : ""}</div>`;
}
