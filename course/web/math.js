function mathFinite(value, name, minimum = 0, exclusive = false) {
  if (
    !Number.isFinite(value) ||
    (exclusive ? value <= minimum : value < minimum)
  ) {
    throw new RangeError(
      `${name} must be finite and ${exclusive ? "greater than" : "at least"} ${minimum}.`,
    );
  }
  return value;
}

function mathFraction(value, name) {
  mathFinite(value, name, 0, true);
  if (value > 1) throw new RangeError(`${name} cannot exceed 1.`);
  return value;
}

function mathSlots(value, name) {
  if (!Number.isSafeInteger(value) || value < 0) {
    throw new RangeError(`${name} must be a nonnegative safe integer.`);
  }
  return value;
}

function mathRackLimit(powerMW, rackKW) {
  const ratio = mathFinite((powerMW * 1000) / rackKW, "Rack limit");
  // Preserve an exact rack boundary when unit conversion introduces roundoff.
  const nearest = Math.round(ratio);
  const tolerance = 4 * Number.EPSILON * Math.max(1, ratio);
  return mathSlots(
    Math.abs(ratio - nearest) <= tolerance ? nearest : Math.floor(ratio),
    "Rack limit",
  );
}

export function currentThreePhase(powerMW, voltageKV, powerFactor = 1) {
  mathFinite(powerMW, "Power");
  mathFinite(voltageKV, "Line-to-line voltage", 0, true);
  mathFraction(powerFactor, "Power factor");
  return mathFinite(
    ((powerMW / voltageKV) * 1000) / Math.sqrt(3) / powerFactor,
    "Current",
  );
}

export function resistiveLossRatio(voltageKV, referenceKV = 138) {
  mathFinite(voltageKV, "Voltage", 0, true);
  mathFinite(referenceKV, "Reference voltage", 0, true);
  return mathFinite((referenceKV / voltageKV) ** 2, "Loss ratio");
}

export function energyMWh(powerMW, hours) {
  mathFinite(powerMW, "Power");
  mathFinite(hours, "Duration");
  return mathFinite(powerMW * hours, "Energy");
}

export function rideThroughMinutes(energyMWh, powerMW, efficiency = 1) {
  mathFinite(energyMWh, "Usable stored energy");
  mathFinite(powerMW, "Load power", 0, true);
  mathFraction(efficiency, "Discharge efficiency");
  return mathFinite((energyMWh / powerMW) * efficiency * 60, "Runtime");
}

export function rackCurrent(powerKW, voltageV) {
  mathFinite(powerKW, "DC power");
  mathFinite(voltageV, "DC voltage", 0, true);
  return mathFinite((powerKW / voltageV) * 1000, "DC current");
}

export function coolantFlow(powerKW, deltaT, cp = 4.18) {
  mathFinite(powerKW, "Heat load");
  mathFinite(deltaT, "Coolant temperature rise", 0, true);
  mathFinite(cp, "Specific heat capacity", 0, true);
  return mathFinite(powerKW / deltaT / cp, "Mass flow");
}

export function capacityBudget(
  facilityMW,
  pue,
  coolingMW,
  rackKW,
  rackSlots,
  networkRacks,
  electricalMW = Infinity,
) {
  mathFinite(facilityMW, "Facility power budget");
  mathFinite(pue, "Assumed facility-to-IT ratio", 1);
  mathFinite(coolingMW, "Available IT heat-removal capacity");
  mathFinite(rackKW, "Rack power", 0, true);
  mathSlots(rackSlots, "Physical rack slots");
  mathSlots(networkRacks, "Network-supported rack count");
  const itBudgetMW = facilityMW / pue;
  const limits = {
    power: mathRackLimit(itBudgetMW, rackKW),
    cooling: mathRackLimit(coolingMW, rackKW),
    space: rackSlots,
    network: networkRacks,
  };
  if (electricalMW !== Infinity) {
    mathFinite(electricalMW, "Downstream electrical IT capacity");
    limits.electrical = mathRackLimit(electricalMW, rackKW);
  }
  const supportedRacks = Math.min(...Object.values(limits));
  const supportedITMW = mathFinite(
    (supportedRacks * rackKW) / 1000,
    "Supported IT power",
  );
  return {
    itBudgetMW,
    supportedRacks,
    supportedITMW,
    facilityDrawMW: mathFinite(supportedITMW * pue, "Scenario facility draw"),
    binding: Object.keys(limits).filter(
      (key) => limits[key] === supportedRacks,
    ),
    limits,
  };
}
