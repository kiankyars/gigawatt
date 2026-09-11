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
  const voltageTop = compact ? 280 : 232,
    voltageBottom = compact ? 405 : 350;
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
  const metricsX = compact ? 28 : 930;
  const metricsY = compact ? 495 : 83;
  const metrics = compact
    ? `${text(metricsX, metricsY, "Capacitor energy", "cb-label")}${text(350, metricsY, ramp ? "5 kJ" : "15 kJ", "cb-value", "end")}${text(metricsX, metricsY + 42, "Lowest bus voltage", "cb-label")}${text(350, metricsY + 42, ramp ? "768.1 V" : "700 V", "cb-value", "end")}${text(28, metricsY + 82, ramp ? "Battery covers the load by 10 ms." : "Load shuts down at 15 ms.", "cb-label")}${text(28, metricsY + 108, ramp ? "Recharging needs surplus power." : "49 kJ remains below the usable limit.", "cb-detail")}`
    : `${text(metricsX, metricsY, "CAPACITOR ENERGY", "cb-detail")}${text(metricsX, metricsY + 44, ramp ? "5 kJ" : "15 kJ", "cb-big")}${text(metricsX, metricsY + 110, "LOWEST BUS VOLTAGE", "cb-detail")}${text(metricsX, metricsY + 153, ramp ? "768.1 V" : "700 V", "cb-big")}${text(metricsX, metricsY + 217, ramp ? "Battery carries 1 MW" : "Load shuts down", "cb-label")}${text(metricsX, metricsY + 246, ramp ? "from 10 ms onward." : "at 15 ms.", "cb-label")}${text(metricsX, metricsY + 299, ramp ? "No recharge modeled." : "49 kJ still stored.", "cb-detail")}`;
  const svg = `<title>Capacitors cover the power deficit while battery power rises</title><desc>Separate hypothetical DC-bus example: one megawatt, 0.20 farads, 800 to 700 volts. ${ramp ? "Assumed battery power rises from zero to one megawatt over ten milliseconds. Capacitors supply five kilojoules, so voltage falls to 768.1 volts and then stays there without recharge." : "Without another source, fifteen kilojoules supports the full load for fifteen milliseconds, when the 700 volt shutdown threshold is reached. The trace stops at that threshold."}</desc>
  <rect x="${left}" y="${powerTop - 30}" width="16" height="12" fill="var(--gold)"/>${text(left + 24, powerTop - 19, "Capacitor", "cb-detail")}
  <rect x="${left + 155}" y="${powerTop - 30}" width="16" height="12" fill="var(--green)"/>${text(left + 179, powerTop - 19, "Battery", "cb-detail")}
  <polygon points="${capacitorArea}" fill="var(--gold)" opacity=".65"/>
  ${ramp ? `<polygon points="${batteryArea}" fill="var(--green)" opacity=".7"/>` : `<rect x="${x(15)}" y="${powerTop}" width="${x(20) - x(15)}" height="${powerBottom - powerTop}" fill="var(--muted)" opacity=".1"/>`}
  <path d="M${left} ${powerTop}H${right}" stroke="var(--ink)" stroke-dasharray="6 6" fill="none"/>
  <path d="M${left} ${powerTop}V${powerBottom}H${right} M${left} ${voltageTop}V${voltageBottom}H${right}" fill="none" stroke="var(--muted)"/>
  ${text(left - 8, powerTop + 6, "1", "cb-tick", "end")}${text(left - 8, powerBottom + 5, "0", "cb-tick", "end")}${text(left - 8, powerTop - 20, "MW", "cb-detail", "end")}
  ${text(left, voltageTop - 15, "Bus voltage", "cb-label")}
  ${[700, 800].map((v) => `${text(left - 8, vy(v) + 6, v, "cb-tick", "end")}<line x1="${left}" x2="${right}" y1="${vy(v)}" y2="${vy(v)}" stroke="var(--line)"/>`).join("")}
  <path d="M${left} ${vy(700)}H${right}" stroke="var(--gold)" stroke-dasharray="6 6" fill="none"/>
  <path d="${voltagePath}" stroke="var(--green)" stroke-width="4" fill="none"/>
  <circle cx="${x(last)}" cy="${vy(result.voltageV)}" r="5" fill="var(--green)"/>
  ${ticks}${text(right, powerBottom + 47, "Time after supply loss (ms)", "cb-detail", "end")}${text(right, voltageBottom + 47, "Time after supply loss (ms)", "cb-detail", "end")}
  ${metrics}`;
  return { svg, viewBox: `0 0 ${W} ${compact ? 640 : 430}`, model: result };
}
