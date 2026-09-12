import test from "node:test";
import assert from "node:assert/strict";
import {
  COOLING_EXAMPLE,
  liquidHeatBalance,
  facilityFlowState,
  heatTransportComparison,
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
