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

export function coolingContinuity({
  topology = "n+1",
  fault = "none",
  loadMode = "full",
  allPathsLost = false,
} = {}) {
  if (!["n+1", "2n"].includes(topology))
    throw new RangeError("Cooling topology must be n+1 or 2n.");
  if (!["none", "module", "shared-path", "double-module"].includes(fault))
    throw new RangeError("Unknown cooling fault.");
  if (!["full", "reduced"].includes(loadMode))
    throw new RangeError("Cooling load mode must be full or reduced.");
  if (typeof allPathsLost !== "boolean")
    throw new TypeError("All-path loss must be a boolean.");

  const moduleKw = 600;
  const fullLoadKw = 1000;
  const loadKw = loadMode === "full" ? fullLoadKw : 500;
  const requiredModules = 2;
  const path = (id, installedModules, failedModules, facilityPathAvailable) => {
    facilityPathAvailable = facilityPathAvailable && !allPathsLost;
    const healthyModules = installedModules - failedModules;
    const availableModules = facilityPathAvailable ? healthyModules : 0;
    const capacityKw = availableModules * moduleKw;
    return Object.freeze({
      id,
      installedModules,
      failedModules,
      healthyModules,
      facilityPathAvailable,
      availableModules,
      capacityKw,
      supportsFullLoad: capacityKw >= fullLoadKw,
    });
  };
  const furtherFailure = fault === "double-module";
  const paths = Object.freeze(
    topology === "n+1"
      ? [
          path(
            "A",
            3,
            furtherFailure ? 2 : fault === "module" ? 1 : 0,
            fault !== "shared-path",
          ),
        ]
      : [
          path(
            "A",
            2,
            fault === "module" ? 1 : 0,
            fault !== "shared-path" && !furtherFailure,
          ),
          path("B", 2, furtherFailure ? 1 : 0, true),
        ],
  );

  // The 2N case transfers this demand to one train; it does not combine A and B.
  const availableKw = Math.max(...paths.map((p) => p.capacityKw));
  const selectedPathId =
    paths.find((p) => p.capacityKw === availableKw && availableKw > 0)?.id ??
    null;
  const faultDescription = {
    none: "No modeled failure.",
    module: "One CDU module in path A is unavailable.",
    "shared-path":
      topology === "n+1"
        ? "The shared facility path is unavailable."
        : "Facility path A is unavailable; path B is independent.",
    "double-module":
      topology === "n+1"
        ? "Two CDU modules in the shared path are unavailable."
        : "Facility path A and one CDU module in path B are unavailable.",
  }[fault];
  return Object.freeze({
    topology,
    fault,
    faultDescription:
      faultDescription +
      (allPathsLost ? " All facility paths are also unavailable." : ""),
    allPathsLost,
    loadMode,
    moduleKw,
    fullLoadKw,
    requiredModules,
    equipmentType: "CDU modules",
    installedEquipmentCount: paths.reduce(
      (sum, p) => sum + p.installedModules,
      0,
    ),
    paths,
    capacityPolicy:
      topology === "n+1"
        ? "parallel-modules-on-shared-path"
        : "one-surviving-train-without-summing-A-and-B",
    selectedPathId,
    fullCapacityPathCount: paths.filter((p) => p.supportsFullLoad).length,
    availableKw,
    loadKw,
    marginKw: availableKw - loadKw,
    supportsLoad: availableKw >= loadKw,
    compatibleIsolationAssumed: true,
    compatibleTransferAssumed: topology === "2n",
    transientTemperature: null,
    transferTimeMs: null,
    loadReductionTimeMs: null,
    rideThroughSeconds: null,
  });
}
