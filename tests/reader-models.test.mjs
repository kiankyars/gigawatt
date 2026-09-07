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
