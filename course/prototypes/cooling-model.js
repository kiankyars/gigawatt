/** An ideal steady-state heat balance for one selected liquid path. */
export const COOLING_EXAMPLE = Object.freeze({
  heatKw: 100,
  specificHeatKjKgK: 4.18,
  normalFlowKgS: 5,
  reducedFlowKgS: 2.5,
});

export function liquidHeatBalance({
  heatKw,
  flowKgS,
  specificHeatKjKgK = COOLING_EXAMPLE.specificHeatKjKgK,
}) {
  if (!Number.isFinite(heatKw) || heatKw < 0)
    throw new RangeError("Heat must be a finite non-negative rate in kW.");
  if (!Number.isFinite(flowKgS) || flowKgS <= 0)
    throw new RangeError(
      "Steady transport requires a positive mass flow in kg/s.",
    );
  if (!Number.isFinite(specificHeatKjKgK) || specificHeatKjKgK <= 0)
    throw new RangeError("Specific heat must be positive and finite.");
  const capacityRateKwK = flowKgS * specificHeatKjKgK;
  return Object.freeze({
    heatKw,
    flowKgS,
    specificHeatKjKgK,
    capacityRateKwK,
    deltaTK: heatKw / capacityRateKwK,
  });
}

/** No temperature/time prediction is possible from a steady energy balance alone. */
export function facilityFlowState(available) {
  if (typeof available !== "boolean")
    throw new TypeError("Facility-flow availability must be a boolean.");
  return Object.freeze({
    facilityFlowAvailable: available,
    steadyHeatPathAvailable: available,
    transientTemperature: null,
    rideThroughSeconds: null,
  });
}

export function heatTransportComparison() {
  const heatKw = 100,
    deltaTK = 10;
  const airDensityKgM3 = 1.2,
    waterDensityKgM3 = 1000;
  const airSpecificHeatKjKgK = 1.005;
  const waterSpecificHeatKjKgK = COOLING_EXAMPLE.specificHeatKjKgK;
  return Object.freeze({
    heatKw,
    deltaTK,
    airDensityKgM3,
    waterDensityKgM3,
    airSpecificHeatKjKgK,
    waterSpecificHeatKjKgK,
    airLitresPerSecond:
      (heatKw / (airDensityKgM3 * airSpecificHeatKjKgK * deltaTK)) * 1000,
    waterLitresPerSecond:
      (heatKw / (waterDensityKgM3 * waterSpecificHeatKjKgK * deltaTK)) * 1000,
  });
}
