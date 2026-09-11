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
  return `<svg class="current-circuit" viewBox="0 0 470 290" role="img" aria-label="Arrows show instantaneous conventional current. Closed two-conductor circuit. Conventional current ${current < 0 ? "reverses" : "leaves the positive source terminal and returns through the other conductor"}. The resistor absorbs ${fmt(power, 1)} kilowatts."><rect class="circuit-box" x="20" y="56" width="94" height="186" rx="12"/><rect class="circuit-box load" x="346" y="56" width="104" height="186" rx="12"/><path class="circuit-wire" d="M114 82H346 M114 216H346"/><text x="67" y="144" text-anchor="middle">${dc ? "DC" : "AC"}</text><text x="67" y="167" text-anchor="middle" class="svg-small">source</text><text x="97" y="89">${polarity[0]}</text><text x="97" y="222">${polarity[1]}</text><text x="398" y="136" text-anchor="middle">Load</text><text x="398" y="159" text-anchor="middle" class="svg-small">resistor</text><text x="398" y="187" text-anchor="middle" class="svg-value">${fmt(power, 1)} kW</text>${directionArrow(226, 82, current)}${directionArrow(226, 216, -current)}${power > 0.01 ? '<path d="M153 143H306 l-12 -8 m12 8 l-12 8" stroke="var(--amber)" stroke-width="5" fill="none"/>' : '<line x1="153" y1="143" x2="306" y2="143" stroke="var(--line)" stroke-dasharray="4 6"/>'}<text x="230" y="173" text-anchor="middle" class="svg-small">${power < 0.01 ? "Zero power at this instant" : "Energy absorbed by load"}</text><text x="230" y="278" text-anchor="middle" class="svg-small">${dc ? "Fixed polarity · 800 V" : "Polarity reverses · " + fmt(volts, 1) + " V now"}</text></svg>`;
}

function threePhaseCircuit(instant) {
  return `<svg class="current-circuit" viewBox="0 0 470 290" role="img" aria-label="Arrows show instantaneous conventional current. Three conductors connect a balanced source and wye resistor load. Signed line currents sum to zero; other lines carry the return current."><rect class="circuit-box" x="10" y="24" width="88" height="212" rx="12"/><text x="54" y="123" text-anchor="middle">AC</text><text x="54" y="146" text-anchor="middle" class="svg-small">source</text><rect class="circuit-box load" x="318" y="24" width="142" height="212" rx="12"/><text x="391" y="45" text-anchor="middle" class="svg-small">Balanced load</text>${instant.phaseCurrents
    .map((amps, n) => {
      const y = 75 + n * 65;
      return `<text x="108" y="${y + 22}" fill="${phaseColors[n]}" class="svg-small">L${n + 1}</text><path d="M98 ${y}H332" stroke="${phaseColors[n]}" stroke-width="3" fill="none"/>${directionArrow(215, y, amps, phaseColors[n])}<rect x="333" y="${y - 8}" width="36" height="16" fill="var(--paper)" stroke="${phaseColors[n]}" stroke-width="2"/><path d="M369 ${y}H429V140" stroke="${phaseColors[n]}" stroke-width="2" fill="none"/>`;
    })
    .join(
      "",
    )}<circle cx="429" cy="140" r="5" fill="var(--ink)"/><text x="235" y="267" text-anchor="middle" class="svg-small">i₁ + i₂ + i₃ = ${fmt(Math.abs(instant.phaseCurrents.reduce((a, b) => a + b, 0)) < 0.01 ? 0 : instant.phaseCurrents.reduce((a, b) => a + b, 0), 1)} A · no neutral current</text></svg>`;
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
  if (kind === "voltage-basis") {
    return `<div class="electrical-grid"><div class="voltage-reference"><span class="eyebrow">SAME BALANCED WYE SYSTEM</span><div class="voltage-pair"><strong>277<small> V RMS</small></strong><span>one phase → star point</span></div><div class="voltage-pair"><strong>480<small> V RMS</small></strong><span>phase → another phase</span></div><p class="voltage-identity">480 = √3 × 277.1</p><p class="electrical-guard">RMS: the DC value giving equal resistor heating.<br>A sine wave’s peak is √2 × RMS.</p></div><div class="electrical-charts">${electricalPlot("Two phase voltages", [make("L1 to star", phaseColors[0], "phaseVoltage1"), make("L2 to star", phaseColors[1], "phaseVoltage2", true)], -400, 400, "V")}${electricalPlot("Subtract at the same instant", [make("L1 − L2", "var(--ink)", "lineVoltage")], -700, 700, "V")}<p class="wave-result">480 V RMS between lines → 679 V peak</p></div></div><p class="electrical-footer"><strong>P = 3 × V<sub>phase</sub> × I = √3 × V<sub>line-to-line</sub> × I</strong><span>Balanced sine waves · power factor 1</span></p>`;
  }
  const dc = kind === "dc-basics",
    three = kind === "three-phase";
  let charts;
  if (three) {
    charts =
      electricalPlot(
        "Current in each line",
        [0, 1, 2].map((n) => ({
          label: `L${n + 1} · ${n * 120}° offset`,
          color: phaseColors[n],
          dash: n === 1,
          value: (d) => waveView(d).phaseCurrents[n],
        })),
        -180,
        180,
        "A",
      ) +
      electricalPlot(
        "Power adds across the three loads",
        [
          ...Array.from({ length: 3 }, (_, n) => ({
            label: `Phase ${n + 1}`,
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
        200,
        "kW",
      );
  } else {
    charts =
      electricalPlot(
        "Voltage polarity",
        [
          make(
            dc ? "DC voltage" : "AC voltage",
            phaseColors[0],
            dc ? "dcVoltage" : "singleVoltage",
          ),
        ],
        -800,
        800,
        "V",
      ) +
      electricalPlot(
        "Conventional current",
        [
          make(
            dc ? "DC current" : "AC current",
            phaseColors[0],
            dc ? "dcCurrent" : "singleCurrent",
          ),
        ],
        -300,
        300,
        "A",
      ) +
      electricalPlot(
        "Power absorbed: p(t) = v(t) × i(t)",
        [make("Load power", "var(--ink)", dc ? "dcPower" : "singlePower")],
        0,
        200,
        "kW",
      );
  }
  return `<div class="electrical-grid"><div class="electrical-circuit-panel"><p class="eyebrow">INSTANTANEOUS CURRENT · FOLLOW THE ARROWS</p>${three ? threePhaseCircuit(now) : circuitLoop(dc, now)}<p class="circuit-reading">${three ? "Three phases, one-third of a cycle apart." : dc ? "Charge follows one direction around a closed loop." : "Current and voltage reverse together in this resistor."}</p><div class="wave-result">${three ? "100 kW total at every instant" : dc ? "100 kW at every instant" : `${fmt(now.singlePower, 1)} kW now · 100 kW average`}</div><p class="electrical-guard">${three ? "Return current uses the other phases. Unbalanced or harmonic loads may need a neutral." : dc ? "Current = charge per second. Voltage = energy per unit charge." : "Negative voltage × negative current = positive load power."}</p></div><div class="electrical-charts">${charts}</div></div><p class="electrical-footer">${three ? "120.3 A RMS per line · 480 V RMS between lines" : dc ? "800 V DC × 125 A = 100 kW" : "480 V RMS × 208.3 A RMS = 100 kW average"}<span>${three ? "Balanced sinusoidal wye load · PF = 1" : "Equivalent resistor load · ideal conductors"}</span></p>`;
}

function electricalVisual(kind) {
  const scrub = kind !== "dc-basics";
  return `<div class="electrical-model"><div class="energy-band"><strong>100 kW average at the load</strong><span>Same hour → 100 kWh received</span></div><div id="wave-content">${electricalContent(kind)}</div>${scrub ? `<div class="cycle-control"><label for="cycle-angle">Time · 60 Hz example (60 cycles/s)</label><input type="range" id="cycle-angle" min="0" max="360" step="1" value="${state.cycleDegrees}"/><output id="cycle-value" for="cycle-angle">${state.cycleDegrees}° · ${fmt((state.cycleDegrees / 360 / 60) * 1000, 2)} ms</output></div>` : ""}</div>`;
}
