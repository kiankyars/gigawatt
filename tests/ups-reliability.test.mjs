import test from "node:test";
import assert from "node:assert/strict";
import { availabilityBudget, renderReliability } from "../course/prototypes/ups-reliability.js";

test("annual availability allowance closes a 365-day service account", () => {
  for (const [nines, minutes] of [[3, 525.6], [4, 52.56], [5, 5.256]]) {
    const model = availabilityBudget(nines);
    assert.ok(Math.abs(model.allowedMinutes - minutes) < 1e-9);
    assert.ok(Math.abs(model.remainingMinutes + 45 - minutes) < 1e-9);
  }
  assert.ok(Math.abs(availabilityBudget(4).usedPercent - 85.61643835616438) < 1e-9);
  assert.equal(availabilityBudget(4).withinBudget, true);
  assert.equal(availabilityBudget(5).withinBudget, false);
});

test("allowance changes with the observation window and exact boundary", () => {
  const thirtyDays = availabilityBudget(4, 0, 30);
  assert.ok(Math.abs(thirtyDays.allowedMinutes - 4.32) < 1e-9);
  assert.equal(availabilityBudget(4, thirtyDays.allowedMinutes, 30).withinBudget, true);
  assert.equal(availabilityBudget(4, thirtyDays.allowedMinutes + 0.001, 30).withinBudget, false);
  for (const args of [[2], [4, -1], [4, Infinity], [4, 1, 0], [4, 1, NaN]])
    assert.throws(() => availabilityBudget(...args), RangeError);
});

test("selected Tier outcomes distinguish planned maintenance from a fault", () => {
  const maintenance = renderReliability("tier-topology", { tierEvent: "maintenance" });
  const fault = renderReliability("tier-topology", { tierEvent: "fault" });
  assert.equal((maintenance.match(/data-meets-event="true"/g) || []).length, 2);
  assert.equal((fault.match(/data-meets-event="true"/g) || []).length, 1);
  assert.match(maintenance, /data-reliability-value="maintenance" aria-pressed="true"/);
  assert.match(fault, /data-reliability-value="fault" aria-pressed="true"/);
});
