import test from 'node:test';
import assert from 'node:assert/strict';
import {
  workloadBound, roofline, serviceDomains, rackAcceptance,
} from '../course/prototypes/compute-model.js';

const close = (actual, expected) => assert.ok(
  Math.abs(actual - expected) <= Math.max(1e-12, Math.abs(expected) * 1e-12),
  `${actual} versus ${expected}`,
);

test('a 144 GB HBM read at 8 TB/s has an 18 ms transfer lower bound', () => {
  const result = workloadBound({ flops: 0, hbmBytes: 144e9 });
  close(result.memorySeconds, 0.018);
  close(result.overlappedSeconds, 0.018);
  assert.equal(result.bottleneck, 'memory');
});

test('compute and HBM overlap uses the longer interval instead of adding both', () => {
  const result = workloadBound({ flops: 40e12, hbmBytes: 160e9 });
  close(result.computeSeconds, 0.2);
  close(result.memorySeconds, 0.02);
  close(result.overlappedSeconds, 0.2);
  close(result.serialSeconds, 0.22);
  assert.equal(result.arithmeticIntensity, 250);
  assert.equal(result.bottleneck, 'compute');
});

test('more compute cannot shorten a workload whose HBM transfer remains limiting', () => {
  const work = { flops: 2e12, hbmBytes: 160e9 };
  const original = workloadBound(work);
  const fasterMath = workloadBound({ ...work, computeFlopsPerSecond: 400e12 });
  const fasterHBM = workloadBound({ ...work, hbmBytesPerSecond: 16e12 });
  assert.equal(original.bottleneck, 'memory');
  close(fasterMath.overlappedSeconds, original.overlappedSeconds);
  close(fasterHBM.overlappedSeconds, 0.01);
  assert.equal(fasterHBM.bottleneck, 'balanced');
});

test('roofline knee connects bandwidth-limited work to the compute ceiling', () => {
  const low = roofline({ arithmeticIntensity: 10 });
  const knee = roofline({ arithmeticIntensity: 25 });
  const high = roofline({ arithmeticIntensity: 100 });
  assert.equal(knee.kneeFlopsPerByte, 25);
  assert.equal(low.attainableFlopsPerSecond, 80e12);
  assert.equal(low.bottleneck, 'memory');
  assert.equal(knee.bottleneck, 'balanced');
  assert.equal(high.attainableFlopsPerSecond, 200e12);
  assert.equal(high.bottleneck, 'compute');
});

test('roofline and time account agree across workloads and hardware rates', () => {
  for (const flops of [1e12, 4e12, 40e12]) {
    for (const computeFlopsPerSecond of [100e12, 200e12, 400e12]) {
      const work = workloadBound({ flops, hbmBytes: 160e9, computeFlopsPerSecond });
      const bound = roofline({ arithmeticIntensity: work.arithmeticIntensity, computeFlopsPerSecond });
      close(flops / work.overlappedSeconds, bound.attainableFlopsPerSecond);
      assert.equal(work.bottleneck, bound.bottleneck);
    }
  }
});

test('zero memory traffic and idle work do not introduce NaN into the time model', () => {
  const math = workloadBound({ flops: 1e12, hbmBytes: 0 });
  const idle = workloadBound({ flops: 0, hbmBytes: 0 });
  assert.equal(math.bottleneck, 'compute');
  assert.equal(math.arithmeticIntensity, Infinity);
  assert.equal(roofline({ arithmeticIntensity: math.arithmeticIntensity }).attainableFlopsPerSecond, 200e12);
  assert.equal(idle.overlappedSeconds, 0);
  assert.equal(idle.arithmeticIntensity, 0);
  assert.equal(idle.bottleneck, 'idle');
});

test('invalid workload units and rates fail before the slide can show an invented result', () => {
  for (const invalid of [NaN, Infinity, -1]) {
    assert.throws(() => workloadBound({ flops: invalid, hbmBytes: 160e9 }), RangeError);
    assert.throws(() => workloadBound({ flops: 1e12, hbmBytes: invalid }), RangeError);
  }
  assert.throws(() => workloadBound({ flops: 1, hbmBytes: 1, computeFlopsPerSecond: 0 }), RangeError);
  assert.throws(() => workloadBound({ flops: 1, hbmBytes: 1, hbmBytesPerSecond: 0 }), RangeError);
  assert.throws(() => roofline({ arithmeticIntensity: -1 }), RangeError);
  assert.throws(() => roofline({ arithmeticIntensity: NaN }), RangeError);
});

test('four concentrated faults and four distributed faults preserve device count but change job capacity', () => {
  const concentrated = serviceDomains({ failedByGroup: [4, 0, 0, 0] });
  const distributed = serviceDomains({ failedByGroup: [1, 1, 1, 1] });
  for (const state of [concentrated, distributed]) {
    assert.equal(state.totalDevices, 32);
    assert.equal(state.healthyDevices, 28);
    assert.equal(state.healthyFraction, 0.875);
    assert.equal(state.allocatedDevices + state.strandedHealthyDevices, state.healthyDevices);
    assert.equal(state.nominalJobs, 4);
  }
  assert.equal(concentrated.runnableJobs, 3);
  assert.equal(concentrated.jobSlotFraction, 0.75);
  assert.equal(concentrated.strandedHealthyDevices, 4);
  assert.equal(distributed.runnableJobs, 0);
  assert.equal(distributed.strandedHealthyDevices, 28);
});

test('smaller compatible jobs can use healthy fragments without pretending they form full groups', () => {
  const fullJobs = serviceDomains({ failedByGroup: [1, 1, 1, 1] });
  const smallerJobs = serviceDomains({ failedByGroup: [1, 1, 1, 1], devicesPerJob: 4 });
  assert.equal(smallerJobs.healthyDevices, fullJobs.healthyDevices);
  assert.equal(smallerJobs.fullHealthyGroups, 0);
  assert.equal(smallerJobs.runnableJobs, 4);
  assert.equal(smallerJobs.strandedHealthyDevices, 12);
});

test('allocation accounting covers all healthy and failed states within each declared group', () => {
  for (let failed = 0; failed <= 8; failed++) {
    const result = serviceDomains({ failedByGroup: [failed, 0, 0, 0] });
    assert.equal(result.failedDevices + result.healthyDevices, result.totalDevices);
    assert.equal(result.runnableJobs, failed === 0 ? 4 : 3);
    assert.ok(result.groups.every(group => group.allocatedDevices <= group.healthyDevices));
  }
  assert.throws(() => serviceDomains({ failedByGroup: [] }), RangeError);
  assert.throws(() => serviceDomains({ failedByGroup: [9] }), RangeError);
  assert.throws(() => serviceDomains({ failedByGroup: [-1] }), RangeError);
  assert.throws(() => serviceDomains({ failedByGroup: [0.5] }), RangeError);
  assert.throws(() => serviceDomains({ devicesPerJob: 16 }), RangeError);
  assert.throws(() => serviceDomains({ devicesPerJob: 0 }), RangeError);
});

test('rack acceptance traces the missing interface instead of equating powered equipment with service', () => {
  assert.equal(rackAcceptance().service, 'full');
  for (const name of ['power', 'coolant', 'fabric', 'software']) {
    const result = rackAcceptance({ [name]: 'unavailable', reducedServiceValidated: true });
    assert.equal(result.canRun, false);
    assert.equal(result.service, 'blocked');
    assert.equal(result.reason, 'missing-input');
    assert.deepEqual(result.blockedBy, [name]);
  }
});

test('limited service requires both available inputs and a validated reduced operating mode', () => {
  const unvalidated = rackAcceptance({ coolant: 'limited', fabric: 'limited' });
  const validated = rackAcceptance({ coolant: 'limited', fabric: 'limited', reducedServiceValidated: true });
  const missing = rackAcceptance({ coolant: 'limited', software: 'unavailable', reducedServiceValidated: true });
  assert.equal(unvalidated.service, 'blocked');
  assert.equal(unvalidated.reason, 'unvalidated-reduced-mode');
  assert.deepEqual(unvalidated.blockedBy, ['coolant', 'fabric']);
  assert.equal(validated.service, 'limited');
  assert.equal(validated.canRun, true);
  assert.deepEqual(validated.blockedBy, []);
  assert.equal(missing.service, 'blocked');
  assert.deepEqual(missing.unavailableInputs, ['software']);
  assert.throws(() => rackAcceptance({ fabric: 'probably-fine' }), RangeError);
  assert.throws(() => rackAcceptance({ reducedServiceValidated: 'yes' }), TypeError);
});
