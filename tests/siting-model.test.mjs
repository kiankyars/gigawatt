import test from "node:test";
import assert from "node:assert/strict";
import {
  readiness,
  matching,
  busBalance,
  islandBudget,
} from "../course/prototypes/siting-model.js";
import { transportBudget } from "../course/prototypes/siting-procurement.js";

const close = (actual, expected, label = "Quantity") =>
  assert.ok(
    Math.abs(actual - expected) <= 1e-9 * Math.max(1, Math.abs(expected)),
    `${label}: ${actual} != ${expected}`,
  );

test("the last accepted dependency controls readiness, not the first power date", () => {
  const a = readiness("A"),
    b = readiness("B");
  assert.ok(a.dates[0] < b.dates[0]);
  assert.ok(a.readyMonth > b.readyMonth);
  assert.equal(a.readyMonth, 22);
  assert.equal(b.readyMonth, 21);
  assert.deepEqual(a.limiting, ["Building"]);
  assert.deepEqual(b.limiting, ["Fiber"]);
  for (const s of [a, b]) {
    assert.ok(s.dates.every((d) => d <= s.readyMonth));
    assert.ok(s.dates.includes(s.readyMonth));
  }
  a.dates[0] = 100;
  assert.equal(
    readiness("A").readyMonth,
    22,
    "A returned array must not mutate the next example",
  );
});

test("daily matching preserves equal totals while retaining both a surplus and a deficit", () => {
  const a = matching();
  assert.equal(a.loadMWh, 10 * 24);
  assert.equal(a.generationMWh, 20 * 12);
  assert.equal(a.surplusMWh, (20 - 10) * 12);
  assert.equal(a.deficitMWh, 10 * 12);
  assert.equal(a.returnedMWh, a.deficitMWh);
  assert.equal(a.energyShortfallMWh, 0);
  assert.equal(a.outputMW * 12, a.returnedMWh);
});

test("round-trip losses cannot return more energy than the captured surplus", () => {
  const a = matching("losses");
  close(a.returnedMWh, a.surplusMWh * 0.9);
  close(a.returnedMWh + a.energyShortfallMWh, a.deficitMWh);
  close(a.requiredChargeMWh * 0.9, a.deficitMWh);
  assert.ok(a.requiredChargeMWh > a.surplusMWh);
  assert.equal(a.energyShortfallMWh, 12);
});

test("an output power limit can fail while stored energy is still sufficient", () => {
  const a = matching("power");
  assert.equal(a.returnedMWh, a.deficitMWh);
  assert.equal(a.energyShortfallMWh, 0);
  assert.equal(a.outputMW, 2);
  assert.equal(a.unsupportedMW, 8);
  assert.equal(a.outputMW + a.unsupportedMW, 10);
  assert.ok(a.outputMW * 12 < a.returnedMWh);
});

test("the customer-bus ledger conserves power across import, balance and proposed export", () => {
  for (const generationMW of [0, 6, 8, 10]) {
    const a = busBalance(generationMW, 8);
    assert.equal(a.gridMW + a.generatorMW, a.loadMW);
    assert.equal(a.loadMW, 8);
  }
  assert.equal(busBalance(6).gridMW, 2);
  assert.equal(busBalance(8).gridMW, 0);
  assert.equal(busBalance(10).gridMW, -2);
  assert.equal(
    busBalance(0).gridMW - 2,
    6,
    "Losing the generator exceeds the stated 2 MW import limit by 6 MW",
  );
});

test("load shedding moves the island constraint from stored energy to fuel duration", () => {
  const eight = islandBudget(8),
    seven = islandBudget(7),
    six = islandBudget(6);
  assert.deepEqual(
    [eight.deficitMW, seven.deficitMW, six.deficitMW],
    [2, 1, 0],
  );
  assert.deepEqual(
    [eight.durationHours, seven.durationHours, six.durationHours],
    [2, 4, 4],
  );
  assert.equal(
    six.batteryHours,
    null,
    "No deficit is distinct from an infinite battery duration",
  );
  for (const a of [eight, seven]) {
    close(a.batteryHours * a.deficitMW, 4);
    assert.ok(a.durationHours <= a.fuelHours);
  }
});

test("island energy cannot rescue a load above the battery output limit", () => {
  const edge = islandBudget(9);
  assert.equal(edge.powerPass, true);
  close(edge.durationHours, 4 / 3);
  const overload = islandBudget(10);
  assert.equal(overload.deficitMW, 4);
  assert.equal(overload.powerPass, false);
  assert.equal(overload.durationHours, 0);
});

test("transport current follows three-phase power conservation and inverse voltage scaling", () => {
  const mv = transportBudget(),
    hv = transportBudget({ voltageKV: 161 });
  for (const a of [mv, hv])
    close((Math.sqrt(3) * a.voltageKV * a.lineCurrentA) / 1000, a.powerMW);
  close(mv.lineCurrentA / hv.lineCurrentA, 161 / 34.5);
  close(mv.lineCurrentA, 3346.9580822587);
  close(hv.lineCurrentA, 717.2053033419788);
});

test("parallel circuits retain total transfer while dividing the current per phase conductor", () => {
  const one = transportBudget();
  for (const circuits of [1, 2, 4]) {
    const a = transportBudget({ circuits });
    close(a.powerPerCircuitMW * circuits, one.powerMW);
    close(a.lineCurrentA * circuits, one.lineCurrentA);
    close(
      (3 * circuits * a.lineCurrentA ** 2) / (3 * one.lineCurrentA ** 2),
      1 / circuits,
      "Fixed-resistance total conductor heating ratio",
    );
  }
  assert.equal(transportBudget({ powerMW: 0 }).lineCurrentA, 0);
});

test("transport budgets reject nonphysical power, voltage and circuit counts", () => {
  for (const powerMW of [-1, NaN, Infinity, "200"])
    assert.throws(() => transportBudget({ powerMW }), RangeError);
  for (const voltageKV of [0, -1, NaN, Infinity, "34.5"])
    assert.throws(() => transportBudget({ voltageKV }), RangeError);
  for (const circuits of [0, -1, 1.5, NaN, Infinity, "2"])
    assert.throws(() => transportBudget({ circuits }), RangeError);
  assert.ok(Object.isFrozen(transportBudget()));
});
