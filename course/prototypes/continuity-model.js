export function storageModel(powerMW = 8, loadMW = 6) {
  if (![powerMW, loadMW].every((x) => Number.isFinite(x) && x > 0))
    throw new RangeError("Positive power required.");
  const deliveredMWh = (1 * 0.8 - 0.2) * 0.95;
  return {
    powerMW,
    loadMW,
    deliveredMWh,
    canSupport: powerMW >= loadMW,
    runtimeMinutes: powerMW >= loadMW ? (deliveredMWh / loadMW) * 60 : null,
  };
}
export function isolationModel(zone = "branch") {
  if (!["branch", "upstream", "bus", "bus-cleared"].includes(zone))
    throw new RangeError("Unknown isolation state.");
  return {
    zone,
    healthy: zone === "branch" ? [true, false, true] : [false, false, false],
    branchContactsClosed:
      zone === "branch" ? [true, false, true] : [true, true, true],
    upstream: ["branch", "bus"].includes(zone),
    fault: zone.startsWith("bus") ? "bus" : "B",
  };
}
export function serviceModel({
  stage = "bridge",
  protectedControls = false,
} = {}) {
  if (!["normal", "bridge", "generator", "recovery"].includes(stage))
    throw new RangeError("Unknown service stage.");
  const utility = stage === "normal",
    generator = ["generator", "recovery"].includes(stage);
  const controls = utility || protectedControls;
  return {
    stage,
    utility,
    generator,
    itPower: true,
    controls,
    pumps: utility || generator,
    heatRejection: utility || stage === "recovery",
    thermalEvidenceNeeded: stage !== "normal",
    service: !controls
      ? "controlled stop"
      : stage === "normal"
        ? "operating"
        : "thermal margin required",
  };
}
