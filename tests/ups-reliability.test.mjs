import test from "node:test";
import assert from "node:assert/strict";
import { availabilityBudget, availabilityExamples, reliabilityControls, renderReliability } from "../course/prototypes/ups-reliability.js";

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

test("named nines examples preserve their different evidence boundaries", () => {
  assert.deepEqual(availabilityExamples.map(({ nines, boundary, kind }) => [nines, boundary, kind]), [
    [3, "Cloud service", "Operator report"],
    [4, "Site availability", "Design claim"],
    [5, "Power uptime", "Advertised SLA"],
  ]);
  const html = renderReliability("availability-budget", {});
  for (const example of availabilityExamples) {
    assert.match(html, new RegExp(`data-nines="${example.nines}"`));
    assert.ok(html.includes(example.source));
  }
  assert.match(html, /Mathematical reference; actual reporting and contract terms differ/);
  assert.doesNotMatch(html, /One outage|Allowance remaining|Abilene/);
  assert.equal(reliabilityControls("availability-budget", {}), "");
});

test("Tier outcomes stay visible together regardless of legacy selector state", () => {
  const maintenance = renderReliability("tier-topology", { tierEvent: "maintenance" });
  const fault = renderReliability("tier-topology", { tierEvent: "fault" });
  assert.equal(maintenance, fault);
  assert.match(maintenance, /data-tier-outcome="maintenance"/);
  assert.match(maintenance, /data-tier-outcome="fault"/);
  assert.doesNotMatch(maintenance, /Not established|Required outcome/);
  assert.equal(reliabilityControls("tier-topology", {}), "");
});

test("Fairwater evidence remains a GPU-fleet design claim and has no reveal state", () => {
  const before = renderReliability("tier-investment", { tierUpgrade: false });
  const after = renderReliability("tier-investment", { tierUpgrade: true });
  assert.equal(before, after);
  assert.match(before, /data-evidence="design-claim"/);
  assert.match(before, /GPU fleet omits/);
  assert.match(before, /Availability claim ≠ Tier certification/);
  assert.match(before, /microsoft-fairwater-atlanta.jpg/);
  assert.equal(reliabilityControls("tier-investment", {}), "");
});
