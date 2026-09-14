import test from "node:test";
import assert from "node:assert/strict";
import {
  capacitorEnergyModel,
  capacitorModel,
  recoveryModel,
  recoveryPlan,
} from "../course/prototypes/ups-capacitors.js";
import {
  renderCapacitorEnergyDiagram,
  renderHoldUpDiagram,
  renderBatteryRampDiagram,
  renderRecoveryComparison,
} from "../course/prototypes/continuity-energy.js";

const near = (actual, expected) =>
  assert.ok(Math.abs(actual - expected) < 1e-6, `${actual} differs from ${expected}`);

test("charge-voltage area gives the stored and usable capacitor energy", () => {
  const m = capacitorEnergyModel();
  near(m.initialChargeC, 160);
  near(m.remainingChargeC, 140);
  near(m.initialJ, 64000);
  near(m.remainingJ, 49000);
  near(m.usableJ, 15000);
  const trapezoidJ = (m.initialV + m.minimumV) / 2 * (m.initialChargeC - m.remainingChargeC);
  near(m.usableJ, trapezoidJ);
  const full = capacitorEnergyModel({ minimumV: 0 });
  near(full.usableJ, full.initialJ);
  near(capacitorEnergyModel({ minimumV: 800 }).usableJ, 0);
  for (const invalid of [{ capacitanceF: 0 }, { minimumV: 801 }, { initialV: NaN }, { minimumV: -1 }])
    assert.throws(() => capacitorEnergyModel(invalid), RangeError);
});

test("the ten millisecond power deficit triangle determines the resulting voltage", () => {
  const m = capacitorModel("ramp", 10);
  const rectangleJ = 1_000_000 * 0.010;
  const triangleJ = rectangleJ / 2;
  near(m.capacitorJ, triangleJ);
  near(m.batteryJ, rectangleJ - triangleJ);
  near(m.voltageV ** 2, 800 ** 2 - 2 * triangleJ / .20);
  near(m.voltageV, 768.1145747868608);
});

test("the chosen recovery duration determines surplus and total source power", () => {
  for (const [ms, surplus, total] of [[50, 100000, 1100000], [100, 50000, 1050000], [250, 20000, 1020000]]) {
    const p = recoveryPlan(ms);
    near(p.missingJ, 5000);
    near(p.surplusW, surplus);
    near(p.sourceW, total);
    near(recoveryModel(ms / 2, p.surplusW).recoveredJ, 2500);
    near(recoveryModel(ms, p.surplusW).voltageV, 800);
    near(recoveryModel(ms, p.surplusW).sourceW, 1000000);
  }
  near(recoveryModel(1000, 0).recoveredJ, 0);
  assert.equal(recoveryModel(1000, 0).recoveryMs, Infinity);
  for (const invalid of [0, -1, Infinity, NaN]) assert.throws(() => recoveryPlan(invalid), RangeError);
});

test("both source interfaces preserve the same capacitor recovery energy account", () => {
  for (const compact of [false, true]) {
    for (const render of [renderCapacitorEnergyDiagram, renderHoldUpDiagram, renderBatteryRampDiagram]) {
      const result = render({ compact });
      assert.match(result.viewBox, compact ? /^0 0 380 / : /^0 0 1180 /);
      assert.doesNotMatch(result.svg, /NaN|undefined/);
      assert.match(result.svg, /<title>/);
    }
    const battery = renderRecoveryComparison("battery", { compact });
    const generator = renderRecoveryComparison("rectifier", { compact });
    assert.deepEqual(battery.model, generator.model);
    near(battery.model.missingJ, 5000);
    assert.match(battery.svg, /Battery → DC\/DC/);
    assert.match(generator.svg, /Running generator → rectifier/);
    for (const label of ["1.00 MW", "1.05 MW", "1.10 MW", "100 ms", "50 ms", "No recovery"])
      assert.ok(battery.svg.includes(label));
  }
});
