import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const source = await readFile(
  new URL("../course/web/math.js", import.meta.url),
  "utf8",
);
const math = await import(
  `data:text/javascript;base64,${Buffer.from(source).toString("base64")}`
);
const close = (actual, expected) =>
  assert.ok(
    Math.abs(actual - expected) <= 1e-10 * Math.max(1, Math.abs(expected)),
    `${actual} != ${expected}`,
  );

test("three-phase current uses line-to-line RMS voltage, power factor, and MW/kV units", () => {
  close(math.currentThreePhase(100, 138), 418.3697602823375);
  close(math.currentThreePhase(100, 13.8), 4183.697602823375);
  close(
    math.currentThreePhase(100, 138, 0.8),
    math.currentThreePhase(100, 138) / 0.8,
  );
  assert.equal(math.currentThreePhase(0, 138), 0);
  close(math.resistiveLossRatio(13.8), 100);
  close(math.resistiveLossRatio(276), 0.25);
});

test("energy and ride-through distinguish power, energy, and discharge efficiency", () => {
  assert.equal(math.energyMWh(100, 24), 2400);
  assert.equal(math.energyMWh(120 / 1000, 24), 2.88);
  close(math.rideThroughMinutes(5, 100), 3);
  close(math.rideThroughMinutes(5, 100, 0.9), 2.7);
  assert.equal(math.rideThroughMinutes(0, 100), 0);
});

test("DC current and liquid heat balance have explicit conversion boundaries", () => {
  assert.equal(math.rackCurrent(120, 50), 2400);
  assert.equal(math.rackCurrent(0.8, 0.8), 1000);
  close(math.coolantFlow(100, 10), 2.3923444976076556);
  close(math.coolantFlow(100, 5), 2 * math.coolantFlow(100, 10));
  close(math.coolantFlow(100, 10, 2), 5);
  assert.equal(math.coolantFlow(0, 10), 0);
});

test("canonical capacity case binds at cooling despite ample site service", () => {
  const budget = math.capacityBudget(100, 1.25, 60, 100, 900, 1000, 70);
  assert.equal(budget.itBudgetMW, 80);
  assert.equal(budget.supportedRacks, 600);
  assert.equal(budget.supportedITMW, 60);
  assert.equal(budget.facilityDrawMW, 75);
  assert.deepEqual(budget.limits, {
    power: 800,
    cooling: 600,
    space: 900,
    network: 1000,
    electrical: 700,
  });
  assert.deepEqual(budget.binding, ["cooling"]);
});

test("rack counts are whole racks, preserve decimal boundaries, and expose tied constraints", () => {
  assert.equal(math.capacityBudget(1, 1.25, 1, 120, 99, 99).supportedRacks, 6);
  assert.equal(math.capacityBudget(0.299, 1, 1, 100, 99, 99).supportedRacks, 2);
  assert.equal(math.capacityBudget(0.29, 1, 1, 10, 99, 99).supportedRacks, 29);
  assert.deepEqual(math.capacityBudget(1, 1, 1, 100, 10, 10).binding, [
    "power",
    "cooling",
    "space",
    "network",
  ]);
  assert.deepEqual(math.capacityBudget(1, 1, 1, 100, 99, 3).binding, [
    "network",
  ]);
  assert.deepEqual(math.capacityBudget(1, 1, 1, 100, 4, 99).binding, ["space"]);
  assert.deepEqual(math.capacityBudget(1, 1, 1, 100, 99, 99, 0.5).binding, [
    "electrical",
  ]);
  assert.deepEqual(math.capacityBudget(0, 1.25, 0, 100, 0, 0), {
    itBudgetMW: 0,
    supportedRacks: 0,
    supportedITMW: 0,
    facilityDrawMW: 0,
    limits: { power: 0, cooling: 0, space: 0, network: 0 },
    binding: ["power", "cooling", "space", "network"],
  });
});

test("invalid denominators, nonfinite values, invalid ratios, and impossible slots fail explicitly", () => {
  const invalidCalls = [
    () => math.currentThreePhase(100, 0),
    () => math.currentThreePhase(100, 138, 0),
    () => math.currentThreePhase(100, 138, 1.01),
    () => math.currentThreePhase(NaN, 138),
    () => math.resistiveLossRatio(0),
    () => math.resistiveLossRatio(138, Infinity),
    () => math.energyMWh(-1, 10),
    () => math.energyMWh(1, Infinity),
    () => math.energyMWh(Number.MAX_VALUE, 2),
    () => math.rideThroughMinutes(5, 0),
    () => math.rideThroughMinutes(5, 100, 1.1),
    () => math.rackCurrent(120, 0),
    () => math.coolantFlow(100, 0),
    () => math.coolantFlow(100, 10, 0),
    () => math.capacityBudget(100, 0.9, 60, 100, 900, 1000),
    () => math.capacityBudget(100, 1.25, -1, 100, 900, 1000),
    () => math.capacityBudget(100, 1.25, 60, 0, 900, 1000),
    () => math.capacityBudget(100, 1.25, 60, 100, 900.5, 1000),
    () => math.capacityBudget(100, 1.25, 60, 100, 900, -1),
    () => math.capacityBudget(100, 1.25, 60, 100, 900, 1000, NaN),
  ];
  for (const call of invalidCalls) assert.throws(call, RangeError);
});
