function positive(value, name) {
  if (!Number.isFinite(value) || value <= 0)
    throw new RangeError(`${name} must be positive and finite`);
  return value;
}
export function dcModel(kw, volts) {
  positive(kw, "Power");
  positive(volts, "Voltage");
  return {
    amps: (kw * 1000) / volts,
    referenceAmps: (kw * 1000) / 48,
    lossRatio: (48 / volts) ** 2,
  };
}
export function thermalModel(kw, deltaT, auxiliaryKW) {
  positive(kw, "Heat duty");
  positive(deltaT, "Temperature rise");
  if (!Number.isFinite(auxiliaryKW) || auxiliaryKW < 0)
    throw new RangeError("Auxiliary input must be nonnegative");
  return {
    kgPerSecond: kw / (4.18 * deltaT),
    litersPerMinute: (kw / (4.18 * deltaT)) * 60,
    rejectedKW: kw + auxiliaryKW,
  };
}
export function transferModel(gigabytes, gbps, efficiency) {
  positive(gigabytes, "Payload");
  positive(gbps, "Link rate");
  if (!Number.isFinite(efficiency) || efficiency <= 0 || efficiency > 1)
    throw new RangeError("Efficiency must lie in (0, 1]");
  const GBps = (gbps / 8) * efficiency;
  return { GBps, seconds: gigabytes / GBps };
}
export function rooflineModel(intensity, bandwidthTBps, peakTFLOPS) {
  positive(intensity, "Arithmetic intensity");
  positive(bandwidthTBps, "Bandwidth");
  positive(peakTFLOPS, "Peak compute");
  const memoryCeiling = intensity * bandwidthTBps;
  return {
    memoryCeiling,
    ceiling: Math.min(memoryCeiling, peakTFLOPS),
    binding:
      memoryCeiling < peakTFLOPS
        ? "memory bandwidth"
        : memoryCeiling > peakTFLOPS
          ? "compute"
          : "both ceilings",
  };
}
export function continuityModel(
  kwh,
  efficiency,
  loadKW,
  inverterKW,
  auxiliarySupported,
) {
  positive(kwh, "Stored energy");
  positive(loadKW, "Load");
  positive(inverterKW, "Inverter rating");
  if (!Number.isFinite(efficiency) || efficiency <= 0 || efficiency > 1)
    throw new RangeError("Efficiency must lie in (0, 1]");
  return {
    powerSufficient: inverterKW >= loadKW,
    electricalMinutes:
      inverterKW >= loadKW ? ((kwh * efficiency) / loadKW) * 60 : 0,
    auxiliarySupported: Boolean(auxiliarySupported),
  };
}
export function checkpointModel(checkpointSeconds, intervalSeconds, mttfHours) {
  positive(checkpointSeconds, "Checkpoint duration");
  positive(intervalSeconds, "Interval");
  positive(mttfHours, "MTTF");
  const mttfSeconds = mttfHours * 3600;
  return {
    checkpointFraction: checkpointSeconds / intervalSeconds,
    recomputeFraction: intervalSeconds / (2 * mttfSeconds),
    optimumSeconds: Math.sqrt(2 * checkpointSeconds * mttfSeconds),
  };
}
export function capacityModel(
  siteMW,
  overheadMW,
  coolingMW,
  rackKW,
  acceptedRacks,
) {
  positive(siteMW, "Site limit");
  positive(rackKW, "Rack load");
  if (
    ![overheadMW, coolingMW, acceptedRacks].every(
      (v) => Number.isFinite(v) && v >= 0,
    ) ||
    overheadMW > siteMW ||
    !Number.isInteger(acceptedRacks)
  )
    throw new RangeError("Capacity inputs are outside the stated domain");
  const powerMW = siteMW - overheadMW,
    acceptedMW = (acceptedRacks * rackKW) / 1000;
  const limit = Math.min(powerMW, coolingMW, acceptedMW);
  return {
    racks: Math.floor((limit * 1000) / rackKW + 1e-9),
    powerMW,
    acceptedMW,
    binding: [
      ["electrical budget", powerMW],
      ["cooling", coolingMW],
      ["accepted rack paths", acceptedMW],
    ]
      .filter(([, v]) => Math.abs(v - limit) < 1e-9)
      .map(([name]) => name),
  };
}
