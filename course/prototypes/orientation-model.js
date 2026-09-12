/** Original teaching examples; these are not measured facility or product data. */
export const ORIENTATION_PROFILES = Object.freeze({
  variable: Object.freeze([
    Object.freeze({ hours: 8, powerMW: 6 }),
    Object.freeze({ hours: 12, powerMW: 10 }),
    Object.freeze({ hours: 4, powerMW: 4 }),
  ]),
  flat: Object.freeze([Object.freeze({ hours: 24, powerMW: 184 / 24 })]),
});

function finiteNonnegative(value, name) {
  if (!Number.isFinite(value) || value < 0)
    throw new RangeError(`${name} must be finite and non-negative.`);
  return value;
}

function finitePositive(value, name) {
  if (!Number.isFinite(value) || value <= 0)
    throw new RangeError(`${name} must be finite and positive.`);
  return value;
}

/**
 * A single, simultaneous power ledger. Each rack's inlet measurement already
 * includes its internal power-supply losses and fans. Network power is separate
 * IT equipment outside these racks; facility overhead is outside the IT boundary.
 * The power ratio represents PUE only under matching, steady measurement periods.
 */
export function facilityLedger({
  racks = 10,
  rackKW = 100,
  networkKW = 100,
  electricalLossKW = 40,
  coolingKW = 160,
  otherKW = 20,
  rackInternalLossKW = 8,
} = {}) {
  if (!Number.isSafeInteger(racks) || racks < 1)
    throw new RangeError("Rack count must be a positive safe integer.");
  for (const [name, value] of Object.entries({
    rackKW,
    networkKW,
    electricalLossKW,
    coolingKW,
    otherKW,
    rackInternalLossKW,
  }))
    finiteNonnegative(value, name);
  if (rackInternalLossKW > rackKW)
    throw new RangeError(
      "Internal rack losses cannot exceed rack inlet power.",
    );

  const rackTotalKW = finiteNonnegative(racks * rackKW, "Total rack power");
  const itKW = finitePositive(rackTotalKW + networkKW, "Total IT power");
  const overheadKW = finiteNonnegative(
    electricalLossKW + coolingKW + otherKW,
    "Facility overhead",
  );
  const facilityKW = finitePositive(itKW + overheadKW, "Facility power");
  const internalLossTotalKW = finiteNonnegative(
    racks * rackInternalLossKW,
    "Total internal rack losses",
  );
  return Object.freeze({
    rackTotalKW,
    itKW,
    overheadKW,
    facilityKW,
    pue: finitePositive(facilityKW / itKW, "PUE"),
    internalLossTotalKW,
  });
}

/** Piecewise-constant power; duration-weighted energy is distinct from peak MW. */
export function profileSummary(segments) {
  if (!Array.isArray(segments) || segments.length === 0)
    throw new TypeError("A power profile requires at least one time segment.");
  let hours = 0;
  let energyMWh = 0;
  let peakMW = 0;
  for (const segment of segments) {
    if (!segment || typeof segment !== "object")
      throw new TypeError("Each segment needs hours and powerMW.");
    finitePositive(segment.hours, "Segment duration in hours");
    finiteNonnegative(segment.powerMW, "Segment power in MW");
    hours = finitePositive(hours + segment.hours, "Total duration");
    energyMWh = finiteNonnegative(
      energyMWh + segment.hours * segment.powerMW,
      "Total energy in MWh",
    );
    peakMW = Math.max(peakMW, segment.powerMW);
  }
  return Object.freeze({
    hours,
    energyMWh,
    averageMW: finiteNonnegative(energyMWh / hours, "Average power in MW"),
    peakMW,
  });
}

/**
 * Hypothetical useful-work units per hour, not a vendor performance benchmark.
 * All rates describe the same steady interval. kW / (units/hour) = kWh/unit.
 */
export function efficiencyCase({ itKW, overheadKW, usefulUnitsPerHour }) {
  finitePositive(itKW, "IT power in kW");
  finiteNonnegative(overheadKW, "Facility overhead in kW");
  finitePositive(usefulUnitsPerHour, "Useful-work rate in units/hour");
  const facilityKW = finitePositive(itKW + overheadKW, "Facility power");
  return Object.freeze({
    facilityKW,
    pue: finitePositive(facilityKW / itKW, "PUE"),
    energyKWhPerUnit: finitePositive(
      facilityKW / usefulUnitsPerHour,
      "Energy per useful-work unit",
    ),
  });
}
