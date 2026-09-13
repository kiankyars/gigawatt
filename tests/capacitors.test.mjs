import test from "node:test";
import assert from "node:assert/strict";
import { capacitorModel } from "../course/prototypes/ups-capacitors.js";
const near = (actual, expected) =>
  assert.ok(
    Math.abs(actual - expected) < 1e-6,
    `${actual} differs from ${expected}`,
  );
test("capacitor-only support reaches the chosen voltage threshold before energy is exhausted", () => {
  const m = capacitorModel("alone", 15);
  near(m.usableJ, 15000);
  near(m.capacitorJ, 15000);
  near(m.voltageV, 700);
  near(0.5 * 0.2 * m.voltageV ** 2, 49000);
  assert.equal(m.supported, false);
  assert.equal(capacitorModel("alone", 14.9).supported, true);
  const later = capacitorModel("alone", 20);
  near(later.capacitorJ, 15000);
  near(later.loadW, 0);
});
test("battery contribution overlaps capacitor discharge from the beginning of the assumed ramp", () => {
  const midway = capacitorModel("ramp", 5);
  near(midway.batteryW, 500000);
  near(midway.capacitorW, 500000);
  near(midway.batteryJ, 1250);
  near(midway.capacitorJ, 3750);
  const complete = capacitorModel("ramp", 10);
  near(complete.capacitorJ, 5000);
  near(complete.batteryJ, 5000);
  near(complete.voltageV, 768.1145747868608);
  near(complete.capacitorW, 0);
  near(complete.batteryW, 1000000);
  const later = capacitorModel("ramp", 20);
  near(later.voltageV, complete.voltageV);
  near(later.batteryJ, 15000);
});
test("energy and instantaneous power balance hold throughout both scenarios", () => {
  for (const mode of ["alone", "ramp"])
    for (let ms = 0; ms <= 20; ms += 0.1) {
      const m = capacitorModel(mode, ms);
      near(
        m.capacitorJ + m.batteryJ,
        1000 * (mode === "alone" ? Math.min(ms, 15) : ms),
      );
      near(m.capacitorJ, 0.5 * 0.2 * (800 ** 2 - m.voltageV ** 2));
      near(m.batteryW + m.capacitorW, m.loadW);
    }
});
test("unsupported mode and time inputs fail explicitly", () => {
  for (const [mode, ms] of [
    ["unknown", 0],
    ["alone", -1],
    ["ramp", 21],
    ["alone", NaN],
  ])
    assert.throws(() => capacitorModel(mode, ms), RangeError);
});

test("recovery returns the missing capacitor energy and then stops charging", async () => {
  const { recoveryModel } = await import("../course/prototypes/ups-capacitors.js");
  const initial = capacitorModel("ramp", 10);
  for (let ms = 0; ms <= 100; ms += 0.25) {
    const m = recoveryModel(ms);
    near(m.sourceW, m.loadW + m.capacitorChargeW);
    near(m.recoveredJ, 0.5 * 0.2 * (m.voltageV ** 2 - initial.voltageV ** 2));
    near(m.recoveredJ, Math.min(5000, 100 * ms));
    assert.ok(m.voltageV <= 800 + 1e-8);
  }
  near(recoveryModel(50).voltageV, 800);
  near(recoveryModel(50).sourceW, 1000000);
  near(recoveryModel(50).capacitorChargeW, 0);
  near(recoveryModel(25).capacitorChargeW, 100000);
  near(recoveryModel(25).voltageV, Math.sqrt(615000));
});
test("matching the load cannot recover voltage; less headroom takes longer", async () => {
  const { recoveryModel } = await import("../course/prototypes/ups-capacitors.js");
  const noSurplus = recoveryModel(10000, 0);
  near(noSurplus.voltageV, capacitorModel("ramp", 10).voltageV);
  near(noSurplus.recoveredJ, 0);
  assert.equal(noSurplus.settled, false);
  near(recoveryModel(50, 50000).recoveredJ, 2500);
  near(recoveryModel(100, 50000).voltageV, 800);
  near(recoveryModel(50, 50000).recoveryMs, 100);
  for (const args of [[-1], [NaN], [0, -1], [0, Infinity]])
    assert.throws(() => recoveryModel(...args), RangeError);
});
