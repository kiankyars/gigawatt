export const CAPACITOR_EXAMPLE = Object.freeze({
  capacitanceF: 0.2,
  initialV: 800,
  minimumV: 700,
  loadW: 1_000_000,
  rampMs: 10,
});

export function capacitorModel(mode, timeMs) {
  if (
    !["alone", "ramp"].includes(mode) ||
    !Number.isFinite(timeMs) ||
    timeMs < 0 ||
    timeMs > 20
  )
    throw new RangeError(
      "Choose a capacitor scenario and a time between 0 and 20 ms",
    );
  const e = CAPACITOR_EXAMPLE;
  const usableJ = 0.5 * e.capacitanceF * (e.initialV ** 2 - e.minimumV ** 2);
  const cutoffMs = (usableJ / e.loadW) * 1000;
  const elapsedMs = mode === "alone" ? Math.min(timeMs, cutoffMs) : timeMs;
  const t = elapsedMs / 1000;
  const rampS = e.rampMs / 1000;
  const batteryJ =
    mode === "alone"
      ? 0
      : e.loadW * (t <= rampS ? (t * t) / (2 * rampS) : t - rampS / 2);
  const capacitorJ = e.loadW * t - batteryJ;
  const voltageV = Math.sqrt(
    e.initialV ** 2 - (2 * capacitorJ) / e.capacitanceF,
  );
  const supported = mode === "ramp" || timeMs < cutoffMs;
  const batteryW = mode === "ramp" ? e.loadW * Math.min(t / rampS, 1) : 0;
  return {
    usableJ,
    capacitorJ,
    batteryJ,
    voltageV,
    cutoffMs,
    supported,
    batteryW,
    capacitorW: supported ? e.loadW - batteryW : 0,
    loadW: supported ? e.loadW : 0,
  };
}

export function renderCapacitorDiagram(mode, { compact = false } = {}) {
  const ramp = mode === "ramp";
  const result = capacitorModel(mode, 20);
  const W = compact ? 380 : 1180;
  const left = compact ? 55 : 90;
  const right = compact ? 355 : 850;
  const powerTop = compact ? 75 : 48,
    powerBottom = compact ? 205 : 166;
  const voltageTop = compact ? 310 : 232,
    voltageBottom = compact ? 435 : 350;
  const x = (t) => left + (t / 20) * (right - left);
  const py = (p) => powerBottom - (p / 1e6) * (powerBottom - powerTop);
  const vy = (v) =>
    voltageBottom - ((v - 680) / 120) * (voltageBottom - voltageTop);
  const last = ramp ? 20 : 15;
  const text = (xx, yy, value, cls = "cb-label", anchor = "start") =>
    `<text x="${xx}" y="${yy}" class="${cls}" text-anchor="${anchor}">${value}</text>`;
  const batteryAt = (t) => (ramp ? Math.min(t / 10, 1) * 1e6 : 0);
  const samples = Array.from({ length: last * 4 + 1 }, (_, i) => i / 4);
  const points = samples.map((t) => `${x(t)},${py(batteryAt(t))}`).join(" ");
  const batteryArea = `${x(0)},${powerBottom} ${points} ${x(last)},${powerBottom}`;
  const capacitorArea = `${x(0)},${py(1e6)} ${x(last)},${py(1e6)} ${samples
    .slice()
    .reverse()
    .map((t) => `${x(t)},${py(batteryAt(t))}`)
    .join(" ")}`;
  const voltagePath = samples
    .map(
      (t, i) =>
        `${i ? "L" : "M"}${x(t)},${vy(capacitorModel(mode, t).voltageV)}`,
    )
    .join(" ");
  const ticks = [0, 5, 10, 15, 20]
    .map(
      (t) =>
        `${text(x(t), powerBottom + 24, t, "cb-tick", "middle")}${text(x(t), voltageBottom + 24, t, "cb-tick", "middle")}`,
    )
    .join("");
  const metricsX = compact ? 28 : 905;
  const metricsY = compact ? 525 : 83;
  const metrics = compact
    ? `${text(metricsX, metricsY, "Capacitor energy", "cb-label")}${text(350, metricsY, ramp ? "5 kJ" : "15 kJ", "cb-value", "end")}${text(metricsX, metricsY + 42, "Lowest bus voltage", "cb-label")}${text(350, metricsY + 42, ramp ? "768.1 V" : "700 V", "cb-value", "end")}${text(28, metricsY + 82, ramp ? "Battery covers the load by 10 ms." : "Load shuts down at 15 ms.", "cb-label")}${text(28, metricsY + 108, ramp ? "½ × 1 MW × 10 ms = 5 kJ" : "½C(800² − 700²) = 15 kJ", "cb-detail")}`
    : `${text(metricsX, metricsY, "CAPACITOR ENERGY", "cb-detail")}${text(metricsX, metricsY + 53, ramp ? "5 kJ" : "15 kJ", "cb-big")}${text(metricsX, metricsY + 110, "LOWEST BUS VOLTAGE", "cb-detail")}${text(metricsX, metricsY + 162, ramp ? "768.1 V" : "700 V", "cb-big")}${text(metricsX, metricsY + 217, ramp ? "Battery carries 1 MW" : "Load shuts down", "cb-label")}${text(metricsX, metricsY + 246, ramp ? "from 10 ms onward." : "at 15 ms.", "cb-label")}${text(metricsX, metricsY + 299, ramp ? "½ × 1 MW × 10 ms = 5 kJ" : "½C(800² − 700²) = 15 kJ", "cb-detail")}`;
  const svg = `<title>Capacitors cover the power deficit while battery power rises</title><desc>Separate hypothetical DC-bus example: one megawatt, 0.20 farads, 800 to 700 volts. ${ramp ? "Assumed battery power rises from zero to one megawatt over ten milliseconds. Capacitors supply five kilojoules, so voltage falls to 768.1 volts and then stays there without recharge." : "Without another source, fifteen kilojoules supports the full load for fifteen milliseconds, when the 700 volt shutdown threshold is reached. The trace stops at that threshold."}</desc>
  <rect x="${left}" y="${powerTop - 30}" width="16" height="12" fill="var(--gold)"/>${text(left + 24, powerTop - 19, "Capacitor", "cb-detail")}
  <rect x="${left + 155}" y="${powerTop - 30}" width="16" height="12" fill="var(--green)"/>${text(left + 179, powerTop - 19, "Battery", "cb-detail")}
  <polygon points="${capacitorArea}" fill="var(--gold)" opacity=".65"/>
  ${ramp ? `<polygon points="${batteryArea}" fill="var(--green)" opacity=".7"/>` : `<rect x="${x(15)}" y="${powerTop}" width="${x(20) - x(15)}" height="${powerBottom - powerTop}" fill="var(--muted)" opacity=".1"/>`}
  <path d="M${left} ${powerTop}H${right}" stroke="var(--ink)" stroke-dasharray="6 6" fill="none"/>
  <path d="M${left} ${powerTop}V${powerBottom}H${right} M${left} ${voltageTop}V${voltageBottom}H${right}" fill="none" stroke="var(--muted)"/>
  ${text(left - 8, powerTop + 6, "1", "cb-tick", "end")}${text(left - 8, powerBottom + 5, "0", "cb-tick", "end")}${text(left - 8, powerTop - 20, "MW", "cb-detail", "end")}
  ${text(left, voltageTop - 15, "Bus voltage (V)", "cb-label")}
  ${[700, 800].map((v) => `${text(left - 8, vy(v) + 6, v, "cb-tick", "end")}<line x1="${left}" x2="${right}" y1="${vy(v)}" y2="${vy(v)}" stroke="var(--line)"/>`).join("")}
  <path d="M${left} ${vy(700)}H${right}" stroke="var(--gold)" stroke-dasharray="6 6" fill="none"/>
  <path d="${voltagePath}" stroke="var(--green)" stroke-width="4" fill="none"/>
  <circle cx="${x(last)}" cy="${vy(result.voltageV)}" r="5" fill="var(--green)"/>
  ${text(right, vy(700) - 7, "Shutdown threshold", "cb-detail", "end")}
  ${ticks}${text(right, powerBottom + 47, "Time after supply loss (ms)", "cb-detail", "end")}${text(right, voltageBottom + 47, "Time after supply loss (ms)", "cb-detail", "end")}
  ${metrics}`;
  return { svg, viewBox: `0 0 ${W} ${compact ? 665 : 430}`, model: result };
}

/** Recovery begins after the assumed ramp, when an available converter has headroom.
 * Powers are measured at the DC link; upstream conversion loss is outside this account.
 */
export function recoveryModel(timeMs, surplusW = 100_000) {
  if (!Number.isFinite(timeMs) || timeMs < 0 || !Number.isFinite(surplusW) || surplusW < 0)
    throw new RangeError("Recovery time and surplus power must be finite and nonnegative");
  const e = CAPACITOR_EXAMPLE;
  const previous = capacitorModel("ramp", e.rampMs);
  const missingJ = previous.capacitorJ;
  const recoveredJ = Math.min(missingJ, surplusW * timeMs / 1000);
  const recoveryMs = surplusW > 0 ? missingJ / surplusW * 1000 : Infinity;
  const capacitorChargeW = timeMs < recoveryMs ? surplusW : 0;
  return {
    initialV: previous.voltageV,
    voltageV: Math.sqrt(previous.voltageV ** 2 + 2 * recoveredJ / e.capacitanceF),
    missingJ,
    recoveredJ,
    recoveryMs,
    capacitorChargeW,
    sourceW: e.loadW + capacitorChargeW,
    loadW: e.loadW,
    settled: timeMs >= recoveryMs,
  };
}

export function renderRecoveryDiagram(source = "battery", { compact = false } = {}) {
  if (!["battery", "rectifier"].includes(source)) throw new RangeError("Unknown recovery source");
  const m = recoveryModel(60);
  const text = (x, y, value, cls = "cb-label", anchor = "start") =>
    `<text x="${x}" y="${y}" class="${cls}" text-anchor="${anchor}">${value}</text>`;
  const wire = (d, dashed = false) => `<path d="${d}" fill="none" stroke="var(--green)" stroke-width="3" ${dashed ? 'stroke-dasharray="5 5"' : ''}/>`;
  const box = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" class="equipment-face"/>`;
  const title = source === "battery" ? "Battery converter" : "Generator rectifier";
  const name = source === "battery" ? "Battery" : "Accepted generator";
  const left = compact ? 65 : 590, right = compact ? 354 : 1135;
  const top = compact ? 400 : 105, bottom = compact ? 530 : 288;
  const x = (ms) => left + ms / 60 * (right - left);
  const y = (v) => bottom - (v - 760) / 50 * (bottom - top);
  const samples = Array.from({ length: 121 }, (_, i) => i / 2);
  const curve = samples.map((ms, i) => `${i ? "L" : "M"}${x(ms)},${y(recoveryModel(ms).voltageV)}`).join(" ");
  const body = compact
    ? `${text(190, 29, name, "cb-label", "middle")}${wire("M190 41V59")}${box(120, 59, 140, 66)}${text(190, 100, source === "battery" ? "DC/DC" : "AC → DC", "cb-value", "middle")}${wire("M190 125V185H306 M190 185H75V242")}${text(211, 157, "1.10 MW", "cb-label")}${box(270, 165, 91, 84)}${text(315, 195, "Bus load", "cb-detail", "middle")}${text(315, 228, "1 MW", "cb-value", "middle")}${text(112, 222, "+100 kW", "cb-label")}${wire("M48 242H102 M48 254H102 M75 254V276")}${text(75, 303, "+5 kJ", "cb-value", "middle")}${text(190, 350, "Voltage control returns the missing energy", "cb-detail", "middle")}`
    : `${text(228, 44, name, "cb-label", "middle")}${wire("M228 59V91")}${box(151, 91, 154, 76)}${text(228, 138, source === "battery" ? "DC/DC" : "AC → DC", "cb-value", "middle")}${wire("M228 167V231H407 M228 231H87V311")}${text(208, 203, "1.10 MW", "cb-value", "end")}${box(384, 203, 126, 95)}${text(447, 236, "Bus load", "cb-label", "middle")}${text(447, 273, "1 MW", "cb-value", "middle")}${text(167, 281, "+100 kW", "cb-label", "middle")}${wire("M57 311H117 M57 325H117 M87 325V345")}${text(87, 380, "+5 kJ", "cb-value", "middle")}${wire("M228 231V361H269V167", true)}${text(354, 385, "Voltage control", "cb-detail", "middle")}`;
  const graph = `${text(left, top - 27, "DC-link voltage (V)", "cb-label")}
    ${wire(`M${left} ${top}V${bottom}H${right}`)}
    ${[768.1, 800].map(v => `${text(left - 9, y(v) + 5, v, "cb-detail", "end")}<path d="M${left} ${y(v)}H${right}" stroke="var(--line)" fill="none" ${v === 800 ? 'stroke-dasharray="6 6"' : ''}/>`).join("")}
    <path d="${curve}" fill="none" stroke="var(--green)" stroke-width="4"/>
    ${[0, 25, 50].map(ms => text(x(ms), bottom + 25, ms, "cb-detail", "middle")).join("")}
    ${text(right, bottom + 52, "Time since recovery begins (ms)", "cb-detail", "end")}
    ${text(x(50), y(800) - 20, "800 V target", "cb-label", "middle")}
    ${text(compact ? 190 : 865, compact ? 625 : 388, "+100 kW × 50 ms = +5 kJ", "cb-value", "middle")}
    ${text(compact ? 190 : 865, compact ? 657 : 422, "At 800 V: source returns to 1 MW", "cb-detail", "middle")}`;
  return {
    viewBox: compact ? "0 0 380 680" : "0 0 1180 455",
    svg: `<title>${title} restores the capacitor energy</title><desc>Ideal separate DC-bus example, continuing from 768.1 volts after five kilojoules were released. An already available ${title.toLowerCase()} delivers 1.10 megawatts at the bus while the load draws one megawatt. The extra 100 kilowatts restores five kilojoules in fifty milliseconds. At 800 volts its controller reduces source power to one megawatt. This is recovery time after power is available, not generator startup time.</desc><g data-recovery-source="${source}">${body}${graph}</g>`,
    model: m,
  };
}
