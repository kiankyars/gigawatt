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

// Ideal source and resistive load: voltage and current are in phase. This
// model excludes conversion losses, conductor losses, harmonics and imbalance.
// Three-phase voltages are phase-to-neutral in a balanced wye equivalent;
// the neutral current is zero, so the neutral need not be a load conductor.
export function acdcWaveModel(
  kind,
  angleDegrees,
  loadKW = 100,
  dcV = 800,
  lineV = 480,
) {
  if (!["dc-basics", "ac-basics", "three-phase", "voltage-basis"].includes(kind))
    throw new RangeError("Unknown AC/DC waveform kind");
  if (!Number.isFinite(angleDegrees))
    throw new RangeError("Phase angle must be finite");
  if (!Number.isFinite(loadKW) || loadKW < 0)
    throw new RangeError("Average load power must be nonnegative and finite");
  positive(dcV, "DC pair voltage");
  positive(lineV, "AC RMS voltage");

  const isDC = kind === "dc-basics";
  const isThreePhase = kind === "three-phase" || kind === "voltage-basis";
  const phaseVoltageRMSV = isDC
    ? dcV
    : isThreePhase
      ? lineV / Math.sqrt(3)
      : lineV;
  const rmsCurrentA =
    (loadKW * 1000) / ((isThreePhase ? 3 : 1) * phaseVoltageRMSV);
  const peakV = phaseVoltageRMSV * (isDC ? 1 : Math.SQRT2);
  const peakA = rmsCurrentA * (isDC ? 1 : Math.SQRT2);
  const offsets = isThreePhase
    ? [["A", 0], ["B", -120], ["C", 120]]
    : [[isDC ? "DC" : "AC", 0]];
  const phases = offsets.map(([label, offset]) => {
    const wave = isDC
      ? 1
      : Math.sin((((angleDegrees % 360) + offset) * Math.PI) / 180);
    const voltageV = peakV * wave;
    const currentA = peakA * wave;
    return {
      label,
      voltageV,
      currentA,
      powerKW: (voltageV * currentA) / 1000,
      rmsVoltageV: phaseVoltageRMSV,
      rmsCurrentA,
      peakV,
      peakA,
    };
  });
  return {
    kind,
    angleDegrees,
    averageKW: loadKW,
    instantKW: phases.reduce((sum, phase) => sum + phase.powerKW, 0),
    currentSumA: phases.reduce((sum, phase) => sum + phase.currentA, 0),
    lineVoltageRMSV: isDC ? dcV : lineV,
    phaseVoltageRMSV,
    lineABVoltageV: isThreePhase
      ? phases[0].voltageV - phases[1].voltageV
      : phases[0].voltageV,
    phases,
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

export function dcConductorModel(loadKW, loadVolts, loopOhms, hours) {
  positive(loadKW, "Delivered power");
  positive(loadVolts, "Receiving-end voltage");
  positive(hours, "Duration");
  if (!Number.isFinite(loopOhms) || loopOhms < 0)
    throw new RangeError("Loop resistance must be nonnegative and finite");
  const amps = (loadKW * 1000) / loadVolts;
  const lossKW = (amps * amps * loopOhms) / 1000;
  const inputKW = loadKW + lossKW;
  return {
    amps,
    lossKW,
    inputKW,
    sendingVolts: loadVolts + amps * loopOhms,
    deliveredKWh: loadKW * hours,
    lossKWh: lossKW * hours,
    inputKWh: inputKW * hours,
  };
}
export function acdcConductorModel(
  loadKW,
  acVolts,
  dcVolts,
  powerFactor,
  conductorOhms,
  hours,
) {
  positive(loadKW, "Delivered real power");
  positive(acVolts, "Receiving-end AC line-to-line RMS voltage");
  positive(dcVolts, "Receiving-end DC pair voltage");
  positive(hours, "Duration");
  if (!Number.isFinite(powerFactor) || powerFactor <= 0 || powerFactor > 1)
    throw new RangeError("Power factor must lie in (0, 1]");
  if (!Number.isFinite(conductorOhms) || conductorOhms < 0)
    throw new RangeError(
      "Resistance per conductor must be nonnegative and finite",
    );
  function segment(amps, conductors) {
    const lossKW = (conductors * amps ** 2 * conductorOhms) / 1000;
    return {
      amps,
      conductors,
      lossKW,
      inputKW: loadKW + lossKW,
      deliveredKWh: loadKW * hours,
      lossKWh: lossKW * hours,
      inputKWh: (loadKW + lossKW) * hours,
    };
  }
  const ac = segment(
    (loadKW * 1000) / (Math.sqrt(3) * acVolts * powerFactor),
    3,
  );
  const dc = segment((loadKW * 1000) / dcVolts, 2);
  return { ac, dc, lossRatio: (2 * dc.amps ** 2) / (3 * ac.amps ** 2) };
}
export function deliveryPathModel(
  loadKW,
  conversionLossKW,
  conductorLossKW,
  hours,
) {
  positive(loadKW, "Delivered power");
  positive(hours, "Duration");
  if (
    ![conversionLossKW, conductorLossKW].every(
      (v) => Number.isFinite(v) && v >= 0,
    )
  )
    throw new RangeError("Stipulated losses must be nonnegative and finite");
  const lossKW = conversionLossKW + conductorLossKW;
  return {
    lossKW,
    inputKW: loadKW + lossKW,
    inputKWh: (loadKW + lossKW) * hours,
    efficiency: loadKW / (loadKW + lossKW),
  };
}
export function acdcDeliveryModel(
  loadKW,
  acVolts,
  dcVolts,
  powerFactor,
  conductorOhms,
  hours,
  acConversionKW,
  dcConversionKW,
  dcUpstreamConversionKW,
) {
  if (
    ![acConversionKW, dcConversionKW, dcUpstreamConversionKW].every(
      (v) => Number.isFinite(v) && v >= 0,
    ) ||
    dcUpstreamConversionKW > dcConversionKW
  )
    throw new RangeError(
      "Conversion losses must be nonnegative with upstream loss within the DC total",
    );
  const dcDownstreamKW = dcConversionKW - dcUpstreamConversionKW;
  const acFeederKW = loadKW + acConversionKW;
  const dcFeederKW = loadKW + dcDownstreamKW;
  const ac = acdcConductorModel(
    acFeederKW,
    acVolts,
    dcVolts,
    powerFactor,
    conductorOhms,
    hours,
  ).ac;
  const dc = acdcConductorModel(
    dcFeederKW,
    acVolts,
    dcVolts,
    powerFactor,
    conductorOhms,
    hours,
  ).dc;
  return {
    ac: {
      ...deliveryPathModel(loadKW, acConversionKW, ac.lossKW, hours),
      conductorLossKW: ac.lossKW,
      amps: ac.amps,
      feederKW: acFeederKW,
    },
    dc: {
      ...deliveryPathModel(loadKW, dcConversionKW, dc.lossKW, hours),
      conductorLossKW: dc.lossKW,
      amps: dc.amps,
      feederKW: dcFeederKW,
    },
    dcDownstreamKW,
  };
}
