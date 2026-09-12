import test from "node:test";
import assert from "node:assert/strict";
import {
  COOLING_EXAMPLE,
  liquidHeatBalance,
  facilityFlowState,
  heatTransportComparison,
  coolingContinuity,
} from "../course/prototypes/cooling-model.js";

const close = (actual, expected) =>
  assert.ok(Math.abs(actual - expected) < 1e-10);

test("100 kW raises 5 kg/s of modeled water by 4.7847 K", () => {
  const result = liquidHeatBalance({ heatKw: 100, flowKgS: 5 });
  close(result.deltaTK, 4.784688995215311);
  close(result.flowKgS * result.specificHeatKjKgK * result.deltaTK, 100);
  close(result.capacityRateKwK, 20.9);
});

test("halving flow doubles the rise while conserving the same heat", () => {
  const baseline = liquidHeatBalance({ heatKw: 100, flowKgS: 5 });
  const reduced = liquidHeatBalance({ heatKw: 100, flowKgS: 2.5 });
  close(reduced.deltaTK, 9.569377990430622);
  close(reduced.deltaTK / baseline.deltaTK, 2);
  for (const flowKgS of [0.5, 1, 2.5, 5, 20]) {
    const balance = liquidHeatBalance({ heatKw: 100, flowKgS });
    close(balance.flowKgS * balance.specificHeatKjKgK * balance.deltaTK, 100);
  }
  close(liquidHeatBalance({ heatKw: 0, flowKgS: 5 }).deltaTK, 0);
});

test("invalid inputs cannot turn stopped flow into an infinite steady temperature", () => {
  for (const flowKgS of [0, -1, NaN, Infinity, "5"])
    assert.throws(
      () => liquidHeatBalance({ heatKw: 100, flowKgS }),
      RangeError,
    );
  for (const heatKw of [-1, NaN, Infinity, "100"])
    assert.throws(() => liquidHeatBalance({ heatKw, flowKgS: 5 }), RangeError);
  for (const specificHeatKjKgK of [0, -1, NaN, Infinity, "4.18"])
    assert.throws(
      () => liquidHeatBalance({ heatKw: 100, flowKgS: 5, specificHeatKjKgK }),
      RangeError,
    );
  assert.equal(COOLING_EXAMPLE.specificHeatKjKgK, 4.18);
});

test("flow interruption identifies the broken path without inventing thermal ride-through", () => {
  const stopped = facilityFlowState(false);
  assert.equal(stopped.steadyHeatPathAvailable, false);
  assert.equal(stopped.rideThroughSeconds, null);
  assert.equal(stopped.transientTemperature, null);
  const restored = facilityFlowState(true);
  assert.equal(restored.steadyHeatPathAvailable, true);
  assert.equal(restored.transientTemperature, null);
  assert.throws(() => facilityFlowState(0), TypeError);
});

test("air and water volume flows carry the same sensible heat at the same rise", () => {
  const m = heatTransportComparison();
  close(m.airLitresPerSecond, 8291.873963515755);
  close(m.waterLitresPerSecond, 2.3923444976076555);
  for (const [flow, density, cp] of [
    [m.airLitresPerSecond, m.airDensityKgM3, m.airSpecificHeatKjKgK],
    [m.waterLitresPerSecond, m.waterDensityKgM3, m.waterSpecificHeatKjKgK],
  ])
    close((flow / 1000) * density * cp * m.deltaTK, m.heatKw);
});

test("N+1 survives one CDU failure but loses delivery through a failed shared facility path", () => {
  const baseline = coolingContinuity();
  assert.equal(baseline.installedEquipmentCount, 3);
  assert.equal(baseline.requiredModules, 2);
  assert.equal(baseline.availableKw, 1800);

  const failedModule = coolingContinuity({ fault: "module" });
  assert.equal(failedModule.paths[0].availableModules, 2);
  assert.equal(failedModule.availableKw, 1200);
  assert.equal(failedModule.marginKw, 200);
  assert.equal(failedModule.supportsLoad, true);

  const failedPath = coolingContinuity({ fault: "shared-path" });
  assert.equal(failedPath.paths[0].healthyModules, 3);
  assert.equal(failedPath.paths[0].availableModules, 0);
  assert.equal(failedPath.availableKw, 0);
  assert.equal(failedPath.selectedPathId, null);
  assert.equal(failedPath.marginKw, -1000);
  assert.equal(failedPath.supportsLoad, false);
});

test("2N serves demand through a surviving full train without adding both trains' ratings", () => {
  const baseline = coolingContinuity({ topology: "2n" });
  assert.equal(baseline.installedEquipmentCount, 4);
  assert.deepEqual(
    baseline.paths.map((p) => p.capacityKw),
    [1200, 1200],
  );
  assert.equal(baseline.availableKw, 1200);
  assert.equal(baseline.fullCapacityPathCount, 2);

  for (const fault of ["module", "shared-path"]) {
    const m = coolingContinuity({ topology: "2n", fault });
    assert.equal(m.availableKw, 1200);
    assert.equal(m.selectedPathId, "B");
    assert.equal(m.fullCapacityPathCount, 1);
    assert.equal(m.supportsLoad, true);
    assert.equal(m.marginKw, 200);
  }
  const lostA = coolingContinuity({ topology: "2n", fault: "shared-path" });
  assert.equal(lostA.paths[0].healthyModules, 2);
  assert.equal(lostA.paths[0].facilityPathAvailable, false);
  assert.equal(lostA.paths[0].capacityKw, 0);
});

test("lower heat demand fits 600 kW of degraded cooling but cannot repair a missing path", () => {
  for (const topology of ["n+1", "2n"]) {
    const full = coolingContinuity({ topology, fault: "double-module" });
    const reduced = coolingContinuity({
      topology,
      fault: "double-module",
      loadMode: "reduced",
    });
    assert.equal(full.availableKw, 600);
    assert.equal(full.supportsLoad, false);
    assert.equal(full.marginKw, -400);
    assert.equal(reduced.availableKw, 600);
    assert.equal(reduced.loadKw, 500);
    assert.equal(reduced.supportsLoad, true);
    assert.equal(reduced.marginKw, 100);
    assert.equal(reduced.requiredModules, 2);
  }
  const isolated = coolingContinuity({
    fault: "shared-path",
    loadMode: "reduced",
  });
  assert.equal(isolated.availableKw, 0);
  assert.equal(isolated.marginKw, -500);
  assert.equal(isolated.supportsLoad, false);

  const compounded = coolingContinuity({
    topology: "2n",
    fault: "double-module",
  });
  assert.equal(compounded.paths[0].facilityPathAvailable, false);
  assert.equal(compounded.paths[0].failedModules, 0);
  assert.equal(compounded.paths[1].failedModules, 1);
  assert.equal(compounded.paths[1].availableModules, 1);
});

test("continuity outcomes preserve installed equipment and never invent transient safety", () => {
  for (const topology of ["n+1", "2n"])
    for (const fault of ["none", "module", "shared-path", "double-module"])
      for (const loadMode of ["full", "reduced"]) {
        const m = coolingContinuity({ topology, fault, loadMode });
        assert.equal(m.installedEquipmentCount, topology === "n+1" ? 3 : 4);
        assert.equal(m.marginKw, m.availableKw - m.loadKw);
        assert.equal(m.supportsLoad, m.marginKw >= 0);
        for (const p of m.paths) {
          assert.equal(p.installedModules, p.healthyModules + p.failedModules);
          assert.ok(p.availableModules <= p.healthyModules);
          if (!p.facilityPathAvailable) assert.equal(p.capacityKw, 0);
        }
        for (const field of [
          "transientTemperature",
          "transferTimeMs",
          "loadReductionTimeMs",
          "rideThroughSeconds",
        ])
          assert.equal(m[field], null);
      }
});

test("unknown cooling topology, fault or load cannot silently turn into a supported state", () => {
  for (const topology of ["N+1", "n+2", "2N", null, 2])
    assert.throws(() => coolingContinuity({ topology }), RangeError);
  for (const fault of ["path", "two-modules", null, true])
    assert.throws(() => coolingContinuity({ fault }), RangeError);
  for (const loadMode of ["throttle", "none", null, 500])
    assert.throws(() => coolingContinuity({ loadMode }), RangeError);
});

test("a later facility outage preserves failed CDU inventory and defeats reduced-load operation", () => {
  const m = coolingContinuity({
    fault: "double-module",
    loadMode: "reduced",
    allPathsLost: true,
  });
  assert.equal(m.paths[0].failedModules, 2);
  assert.equal(m.paths[0].healthyModules, 1);
  assert.equal(m.availableKw, 0);
  assert.equal(m.loadKw, 500);
  assert.equal(m.supportsLoad, false);
  assert.throws(() => coolingContinuity({ allPathsLost: "yes" }), TypeError);
});
