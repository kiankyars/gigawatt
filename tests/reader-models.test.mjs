import test from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
const source = readFileSync(
  new URL("../course/web/reader-models.js", import.meta.url),
  "utf8",
);
const m = await import(
  `data:text/javascript;base64,${Buffer.from(source).toString("base64")}`
);
const close = (a, b, t = 1e-9) =>
  assert.ok(Math.abs(a - b) < t, `${a} != ${b}`);
test("DC comparison uses the stated output and equal-resistance boundary", () => {
  const v48 = m.dcModel(100, 48),
    v800 = m.dcModel(100, 800);
  close(v48.amps, 2083.3333333333335);
  close(v800.amps, 125);
  close(v800.lossRatio, 0.0036);
  close(v800.amps * 800, v48.amps * 48);
});
test("Water flow and rejected heat close independent energy balances", () => {
  const x = m.thermalModel(100, 10, 20);
  close(x.kgPerSecond * 4.18 * 10, 100);
  close(x.litersPerMinute, x.kgPerSecond * 60);
  close(x.rejectedKW, 120);
  close(m.thermalModel(100, 20, 0).kgPerSecond, x.kgPerSecond / 2);
});
test("Network transfer distinguishes bits from bytes and achieved from nominal rate", () => {
  const x = m.transferModel(100, 400, 0.8);
  close(x.GBps, 40);
  close(x.seconds, 2.5);
  close(m.transferModel(100, 800, 0.8).seconds, 1.25);
});
test("Roofline changes binding ceiling at the independently solved crossover", () => {
  assert.equal(m.rooflineModel(50, 2, 500).binding, "memory bandwidth");
  close(m.rooflineModel(50, 2, 500).ceiling, 100);
  assert.equal(m.rooflineModel(250, 2, 500).binding, "both ceilings");
  assert.equal(m.rooflineModel(300, 2, 500).binding, "compute");
});
test("Electrical ride-through cannot substitute for auxiliary support", () => {
  const x = m.continuityModel(600, 0.9, 2000, 2500, false);
  close(x.electricalMinutes, 16.2);
  assert.equal(x.auxiliarySupported, false);
  assert.equal(
    m.continuityModel(600, 0.9, 2000, 1500, true).powerSufficient,
    false,
  );
  close(
    m.continuityModel(600, 0.9, 2200, 2500, true).electricalMinutes,
    14.727272727272727,
  );
});
test("Checkpoint model minimum balances its two approximate terms", () => {
  const x = m.checkpointModel(30, 900, 10);
  close(x.checkpointFraction, 1 / 30);
  close(x.recomputeFraction, 0.0125);
  const optimum = m.checkpointModel(30, x.optimumSeconds, 10);
  close(optimum.checkpointFraction, optimum.recomputeFraction);
});
test("Capacity follows whole accepted service paths and reports tied limits", () => {
  assert.equal(m.capacityModel(100, 15, 70, 100, 900).racks, 700);
  assert.equal(m.capacityModel(100, 25, 55, 100, 900).racks, 550);
  const x = m.capacityModel(100, 25, 65, 100, 600);
  assert.equal(x.racks, 600);
  assert.deepEqual(x.binding, ["accepted rack paths"]);
  assert.deepEqual(m.capacityModel(100, 40, 60, 100, 600).binding, [
    "electrical budget",
    "cooling",
    "accepted rack paths",
  ]);
  assert.equal(m.capacityModel(1, 0, 0.999, 100, 20).racks, 9);
});
test("Invalid and nonfinite inputs fail instead of producing plausible outputs", () => {
  for (const f of [
    () => m.dcModel(100, 0),
    () => m.thermalModel(100, 0, 0),
    () => m.transferModel(10, 400, 1.1),
    () => m.rooflineModel(NaN, 2, 500),
    () => m.continuityModel(100, 0, 100, 100, true),
    () => m.checkpointModel(30, 0, 10),
    () => m.capacityModel(100, 110, 60, 100, 900),
    () => m.capacityModel(100, 20, 60, 100, 1.5),
  ])
    assert.throws(f, RangeError);
});

test("Receiving-end DC voltage closes both power and energy balances", () => {
  const low = m.dcConductorModel(100, 48, 0.001, 1);
  const high = m.dcConductorModel(100, 800, 0.001, 1);
  close(low.lossKW, 4.340277777777778);
  close(high.lossKW, 0.015625);
  close(low.sendingVolts, 50.083333333333336);
  close(high.sendingVolts, 800.125);
  close(low.inputKW, 104.34027777777777);
  close(high.inputKW, 100.015625);
  close(low.inputKWh - high.inputKWh, 4.3246527777777715);
  for (const x of [low, high]) {
    close(x.inputKW, (x.amps * x.sendingVolts) / 1000);
    close(x.inputKWh, x.deliveredKWh + x.lossKWh);
  }
  close(m.dcConductorModel(100, 800, 0.001, 2).inputKWh, 2 * high.inputKWh);
  close(m.dcConductorModel(100, 48, 0, 1).inputKW, 100);
});
test("Whole-path losses can reverse the AC versus DC energy result", () => {
  const ac = m.deliveryPathModel(100, 4, 1, 1);
  const dc = m.deliveryPathModel(100, 3, 0.1, 1);
  const changed = m.deliveryPathModel(100, 6, 0.1, 1);
  close(ac.inputKW, 105);
  close(dc.inputKW, 103.1);
  close(ac.inputKWh - dc.inputKWh, 1.9);
  close(changed.inputKWh - ac.inputKWh, 1.1);
  close(m.deliveryPathModel(100, 4.9, 0.1, 1).inputKW, ac.inputKW);
  close(m.deliveryPathModel(100, 0, 0, 2).inputKWh, 200);
  assert.ok(ac.efficiency < 1 && dc.efficiency < 1);
});
test("480 V three-phase AC and 800 V DC separate current from total conductor heat", () => {
  const { ac, dc, lossRatio } = m.acdcConductorModel(100, 480, 800, 1, 0.01, 1);
  close(ac.amps, 120.28130608117205);
  close(dc.amps, 125);
  assert.ok(dc.amps > ac.amps);
  close(ac.lossKW, 0.4340277777777778);
  close(dc.lossKW, 0.3125);
  close(lossRatio, 0.72);
  close(ac.inputKWh - dc.inputKWh, 0.1215277777777778);
  for (const x of [ac, dc]) close(x.inputKWh, x.deliveredKWh + x.lossKWh);
  close(ac.amps * (480 / Math.sqrt(3)) * 3, 100000);
  close(dc.amps * 800, 100000);
});
test("Equal numerical voltage, power factor and conductor resistance alter the comparison", () => {
  const sameVoltage = m.acdcConductorModel(100, 480, 480, 1, 0.01, 1);
  close(sameVoltage.dc.amps / sameVoltage.ac.amps, Math.sqrt(3));
  close(sameVoltage.lossRatio, 2);
  const lowerPF = m.acdcConductorModel(100, 480, 800, 0.8, 0.01, 2);
  close(lowerPF.ac.amps, 150.35163260146505);
  close(lowerPF.lossRatio, 0.4608);
  close(lowerPF.dc.inputKWh, 200.625);
  const zeroR = m.acdcConductorModel(100, 480, 800, 1, 0, 1);
  close(zeroR.ac.inputKW, 100);
  close(zeroR.dc.inputKW, 100);
});
test("The AC/DC comparison rejects invalid electrical assumptions", () => {
  for (const args of [
    [100, 0, 800, 1, 0.01, 1],
    [100, 480, NaN, 1, 0.01, 1],
    [100, 480, 800, 0, 0.01, 1],
    [100, 480, 800, 1.1, 0.01, 1],
    [100, 480, 800, 1, -1, 1],
    [100, 480, 800, 1, Infinity, 1],
    [100, 480, 800, 1, 0.01, 0],
  ])
    assert.throws(() => m.acdcConductorModel(...args), RangeError);
});
test("Complete paths include conversion in feeder loading at the correct position", () => {
  const run = (dcLoss) =>
    m.acdcDeliveryModel(100, 480, 800, 1, 0.01, 1, 4, dcLoss, 1);
  const { ac, dc } = run(3);
  close(ac.feederKW, 104);
  close(dc.feederKW, 102);
  close(ac.conductorLossKW, 0.46944444444444444);
  close(dc.conductorLossKW, 0.325125);
  close(ac.inputKW, 104.46944444444445);
  close(dc.inputKW, 103.325125);
  close(ac.inputKWh - dc.inputKWh, 1.1443194444444487);
  const reversed = run(6).dc;
  close(reversed.feederKW, 105);
  close(reversed.inputKW, 106.34453125);
  assert.ok(reversed.inputKW > ac.inputKW);
  assert.ok(reversed.conductorLossKW < ac.conductorLossKW);
  close(run(4.137030473976019).dc.inputKW, ac.inputKW);
  for (const x of [ac, dc, reversed]) close(x.inputKW, 100 + x.lossKW);
  const shifted = m.acdcDeliveryModel(100, 480, 800, 1, 0.01, 1, 4, 3, 3);
  close(shifted.dc.feederKW, 100);
  close(shifted.dc.conductorLossKW, 0.3125);
  assert.throws(
    () => m.acdcDeliveryModel(100, 480, 800, 1, 0.01, 1, 4, 2, 3),
    RangeError,
  );
});
test("Energy ledgers reject invalid resistance, time and loss budgets", () => {
  for (const fn of [
    () => m.dcConductorModel(100, 0, 0.001, 1),
    () => m.dcConductorModel(100, 800, -1, 1),
    () => m.dcConductorModel(100, 800, Infinity, 1),
    () => m.dcConductorModel(100, 800, 0.001, 0),
    () => m.deliveryPathModel(100, -1, 0.1, 1),
    () => m.deliveryPathModel(100, 3, NaN, 1),
    () => m.deliveryPathModel(100, 3, 0.1, 0),
  ])
    assert.throws(fn, RangeError);
});
