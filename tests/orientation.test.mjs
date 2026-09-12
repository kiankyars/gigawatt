import test from "node:test";
import assert from "node:assert/strict";
import {
  ORIENTATION_PROFILES,
  facilityLedger,
  profileSummary,
  efficiencyCase,
} from "../course/prototypes/orientation-model.js";

const close = (actual, expected) =>
  assert.ok(Math.abs(actual - expected) < 1e-10, `${actual} != ${expected}`);

test("rack inlet, IT and facility boundaries conserve the same incoming power", () => {
  const ledger = facilityLedger();
  assert.deepEqual(ledger, {
    rackTotalKW: 1420,
    itKW: 1500,
    overheadKW: 300,
    facilityKW: 1800,
    pue: 1.2,
    internalLossTotalKW: 0,
  });
  // Looking inside a meter boundary must not create an additional energy load.
  const rackRemainder = ledger.rackTotalKW - ledger.internalLossTotalKW;
  assert.equal(
    rackRemainder + ledger.internalLossTotalKW + 80 + ledger.overheadKW,
    ledger.facilityKW,
  );
});

test("changing the internal-loss breakdown never adds rack power a second time", () => {
  for (const rackInternalLossKW of [0, 8, 25, 100]) {
    const ledger = facilityLedger({ rackInternalLossKW });
    assert.equal(ledger.internalLossTotalKW, 10 * rackInternalLossKW);
    assert.equal(ledger.rackTotalKW, 1420);
    assert.equal(ledger.itKW, 1500);
    assert.equal(ledger.facilityKW, 1800);
    assert.equal(ledger.pue, 1.2);
  }
  const noOverhead = facilityLedger({
    electricalLossKW: 0,
    coolingKW: 0,
    otherKW: 0,
  });
  assert.equal(noOverhead.facilityKW, noOverhead.itKW);
  assert.equal(noOverhead.pue, 1);
});

test("invalid boundaries cannot produce negative loads or a meaningless PUE", () => {
  for (const racks of [0, -1, 1.5, NaN, Infinity, "10"])
    assert.throws(() => facilityLedger({ racks }), RangeError);
  for (const field of [
    "rackKW",
    "networkKW",
    "electricalLossKW",
    "coolingKW",
    "otherKW",
    "rackInternalLossKW",
  ])
    for (const value of [-1, NaN, Infinity, "100", null])
      assert.throws(() => facilityLedger({ [field]: value }), RangeError);
  assert.throws(() => facilityLedger({ rackInternalLossKW: 143 }), RangeError);
  assert.throws(
    () => facilityLedger({ rackKW: 0, networkKW: 0, rackInternalLossKW: 0 }),
    RangeError,
  );
  assert.throws(() => facilityLedger({ rackKW: Number.MAX_VALUE }), RangeError);
});

test("equal 24-hour energy does not imply equal peak power", () => {
  const variable = profileSummary(ORIENTATION_PROFILES.variable);
  const flat = profileSummary(ORIENTATION_PROFILES.flat);
  for (const summary of [variable, flat]) {
    assert.equal(summary.hours, 24);
    close(summary.energyMWh, 144);
    close(summary.averageMW, 6);
  }
  assert.equal(variable.peakMW, 8);
  close(flat.peakMW, 6);
  assert.ok(variable.peakMW > flat.peakMW);
});

test("energy depends on time at each power, not an unweighted mean", () => {
  const profile = [
    { hours: 1, powerMW: 12 },
    { hours: 3, powerMW: 4 },
  ];
  assert.deepEqual(profileSummary(profile), {
    hours: 4,
    energyMWh: 24,
    averageMW: 6,
    peakMW: 12,
  });
  assert.deepEqual(profileSummary([{ hours: 24, powerMW: 0 }]), {
    hours: 24,
    energyMWh: 0,
    averageMW: 0,
    peakMW: 0,
  });
  assert.deepEqual(
    profileSummary([...profile].reverse()),
    profileSummary(profile),
  );
});

test("profiles reject impossible durations, powers and overflowing totals", () => {
  for (const segments of [undefined, null, {}, [], [null]])
    assert.throws(() => profileSummary(segments), TypeError);
  for (const hours of [0, -1, NaN, Infinity, "24"])
    assert.throws(() => profileSummary([{ hours, powerMW: 10 }]), RangeError);
  for (const powerMW of [-1, NaN, Infinity, "10"])
    assert.throws(() => profileSummary([{ hours: 24, powerMW }]), RangeError);
  assert.throws(
    () => profileSummary([{ hours: 24, powerMW: Number.MAX_VALUE }]),
    RangeError,
  );
});

test("reducing facility overhead lowers PUE while the IT energy stays fixed", () => {
  const a = efficiencyCase({
    itKW: 1500,
    overheadKW: 300,
    usefulUnitsPerHour: 100,
  });
  const b = efficiencyCase({
    itKW: 1500,
    overheadKW: 150,
    usefulUnitsPerHour: 100,
  });
  assert.equal(a.facilityKW, 1800);
  assert.equal(b.facilityKW, 1650);
  close(a.pue, 1.2);
  close(b.pue, 1.1);
  assert.equal(a.facilityKW - 300, b.facilityKW - 150);
  assert.equal(a.facilityKW - b.facilityKW, 150);
  assert.equal(a.energyKWhPerUnit, 18);
  assert.equal(b.energyKWhPerUnit, 16.5);
});

test("batch rescheduling keeps fixed load, batch energy and the deadline", () => {
  const fixed = profileSummary([{ hours: 24, powerMW: 4 }]);
  for (const segments of Object.values(ORIENTATION_PROFILES)) {
    const total = profileSummary(segments);
    assert.equal(total.hours, 24);
    assert.equal(total.energyMWh - fixed.energyMWh, 48);
    for (const segment of segments) assert.ok(segment.powerMW >= 4);
  }
  assert.ok(profileSummary(ORIENTATION_PROFILES.variable).peakMW > 6.5);
  assert.ok(profileSummary(ORIENTATION_PROFILES.flat).peakMW < 6.5);
});

test("productive efficiency needs positive measured work and compatible power rates", () => {
  const baseline = { itKW: 1000, overheadKW: 200, usefulUnitsPerHour: 100 };
  for (const field of ["itKW", "usefulUnitsPerHour"])
    for (const value of [0, -1, NaN, Infinity, "100"])
      assert.throws(
        () => efficiencyCase({ ...baseline, [field]: value }),
        RangeError,
      );
  for (const overheadKW of [-1, NaN, Infinity, "200"])
    assert.throws(
      () => efficiencyCase({ ...baseline, overheadKW }),
      RangeError,
    );
  assert.equal(efficiencyCase({ ...baseline, overheadKW: 0 }).pue, 1);
  assert.throws(
    () =>
      efficiencyCase({
        ...baseline,
        itKW: Number.MAX_VALUE,
        overheadKW: Number.MAX_VALUE,
      }),
    RangeError,
  );
});
