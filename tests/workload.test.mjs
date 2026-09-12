import test from "node:test";
import assert from "node:assert/strict";
import {
  memoryBudget, computeObservation, utilizationCase, inferenceSchedule,
  WORKLOAD_PHASES, phaseSchedule, transitionRate, evaluateInferenceAcceptance,
} from "../course/prototypes/workload-model.js";

const close = (actual, expected, name = "quantity") => assert.ok(
  Math.abs(actual - expected) <= 1e-9 * Math.max(1, Math.abs(expected)),
  `${name}: expected ${expected}, received ${actual}`,
);

test("the same 12 billion parameters produce distinct declared memory budgets", () => {
  const inference = memoryBudget();
  assert.equal(inference.stateGB, 24);
  assert.equal(inference.totalGB, 52);
  assert.equal(inference.aggregateHeadroomGB, 28);
  assert.equal(inference.fitStatus, "capacity-screen-passes");
  const training = memoryBudget({ kind: "training", deviceCount: 2 });
  assert.equal(training.stateGB, 192);
  assert.equal(training.totalGB, 256);
  assert.equal(training.aggregateCapacityGB, 160);
  assert.equal(training.aggregateFits, false);
  assert.equal(training.fitStatus, "aggregate-fails");
  const four = memoryBudget({ kind: "training", deviceCount: 4 });
  assert.equal(four.aggregateCapacityGB, 320);
  assert.equal(four.aggregateFits, true);
  assert.equal(four.partitionFits, null);
  assert.equal(four.fitStatus, "partition-unverified");
});

test("more workspace can exhaust a single memory pool without changing parameter count", () => {
  for (const [workspaceGB, totalGB, fits] of [[20, 52, true], [44, 76, true], [48, 80, true], [56, 88, false]]) {
    const result = memoryBudget({ workspaceGB });
    assert.equal(result.totalGB, totalGB);
    assert.equal(result.aggregateFits, fits);
    assert.equal(result.partitionFits, fits);
    assert.equal(result.stateGB, 24);
    assert.equal(result.reservationGB, 8);
  }
});

test("equal aggregate memory does not rescue an overflowing per-device partition", () => {
  const even = memoryBudget({ kind: "training", allocationGB: [64, 64, 64, 64] });
  const uneven = memoryBudget({ kind: "training", allocationGB: [96, 64, 64, 32] });
  assert.equal(even.totalGB, uneven.totalGB);
  assert.equal(even.aggregateCapacityGB, uneven.aggregateCapacityGB);
  assert.equal(even.partitionFits, true);
  assert.equal(uneven.aggregateFits, true);
  assert.equal(uneven.partitionFits, false);
  assert.deepEqual(uneven.deviceFits, [false, true, true, true]);
  assert.equal(uneven.fitStatus, "partition-fails");
});

test("memory screening rejects invalid budgets and incomplete allocation accounts", () => {
  assert.throws(() => memoryBudget({ kind: "anything" }), RangeError);
  for (const workspaceGB of [-1, NaN, Infinity, "20"])
    assert.throws(() => memoryBudget({ workspaceGB }), RangeError);
  for (const deviceCount of [0, -1, 2.5, NaN, Infinity, "4"])
    assert.throws(() => memoryBudget({ deviceCount }), RangeError);
  for (const deviceCapacityGB of [0, -1, NaN, Infinity, "80"])
    assert.throws(() => memoryBudget({ deviceCapacityGB }), RangeError);
  for (const allocationGB of [null, {}, [], [64, 64]])
    assert.throws(() => memoryBudget({ kind: "training", allocationGB }), TypeError);
  for (const allocationGB of [[64, 64, 64, 63], [64, 64, 64, -1], [64, 64, 64, NaN], Object.assign(Array(4), { 0: 256 })])
    assert.throws(() => memoryBudget({ kind: "training", allocationGB }), RangeError);
  assert.throws(() => memoryBudget({ deviceCount: 2, deviceCapacityGB: Number.MAX_VALUE }), RangeError);
});

test("A, B and practice C use the complete 60-second energy and accepted-output account", () => {
  const expected = {
    A: { energyJ: 3075000, output: 45000, averageKW: 51.25, intensity: 205 / 3, compute: 45 },
    B: { energyJ: 2550000, output: 30000, averageKW: 42.5, intensity: 85, compute: 30 },
    C: { energyJ: 3250000, output: 50000, averageKW: 325 / 6, intensity: 65, compute: 50 },
  };
  for (const [name, reference] of Object.entries(expected)) {
    const result = utilizationCase(name);
    assert.equal(result.seconds, 60);
    assert.equal(result.energyJ, reference.energyJ);
    assert.equal(result.acceptedSamples, reference.output);
    close(result.energyKWh, reference.energyJ / 3600000);
    close(result.averageKW, reference.averageKW);
    close(result.joulesPerAcceptedSample, reference.intensity);
    assert.equal(result.allocationFraction, 1);
    close(result.executionFraction, reference.compute / 60);
    assert.equal(result.phases[0].startSeconds, 0);
    assert.equal(result.phases.at(-1).endSeconds, 60);
    close(result.energyKWh * 3600, result.averageKW * result.seconds, "Power-energy conservation");
    close(result.joulesPerAcceptedSample * result.acceptedSamples, result.energyJ, "Accepted-output normalization");
  }
  assert.ok(utilizationCase("B").averageKW < utilizationCase("A").averageKW);
  assert.ok(utilizationCase("B").joulesPerAcceptedSample > utilizationCase("A").joulesPerAcceptedSample);
});

test("idle and zero accepted output have an undefined energy-per-result denominator", () => {
  const idle = utilizationCase("idle");
  assert.equal(idle.energyKWh, 0.2);
  assert.equal(idle.energyJ, 720000);
  assert.equal(idle.averageKW, 12);
  assert.equal(idle.allocationFraction, 0);
  assert.equal(idle.executionFraction, 0);
  assert.equal(idle.acceptedSamples, 0);
  assert.equal(idle.joulesPerAcceptedSample, null);
  const unsuccessful = computeObservation({ computeSeconds: 60, acceptedSamplesPerComputeSecond: 0 });
  assert.equal(unsuccessful.allocationFraction, 1);
  assert.equal(unsuccessful.executionFraction, 1);
  assert.equal(unsuccessful.energyKWh, 1);
  assert.equal(unsuccessful.joulesPerAcceptedSample, null);
});

test("observation validation rejects impossible durations, rates and overflow", () => {
  for (const field of ["computeSeconds", "waitSeconds", "idleSeconds", "computeKW", "waitKW", "idleKW", "acceptedSamplesPerComputeSecond"])
    for (const value of [-1, NaN, Infinity, "1"])
      assert.throws(() => computeObservation({ [field]: value }), RangeError);
  assert.throws(() => computeObservation({ computeSeconds: 0, waitSeconds: 0 }), RangeError);
  assert.throws(() => computeObservation({ computeSeconds: 61 }), RangeError);
  assert.throws(() => computeObservation({ computeKW: Number.MAX_VALUE }), RangeError);
  assert.throws(() => utilizationCase("D"), RangeError);
});

test("four arrivals reveal different response times despite one shared batch finish", () => {
  const schedule = inferenceSchedule();
  assert.deepEqual(schedule.arrivalsMs, [0, 6, 12, 18]);
  assert.deepEqual(schedule.requests.map((request) => request.startMs), [18, 18, 18, 18]);
  assert.deepEqual(schedule.requests.map((request) => request.finishMs), [38, 38, 38, 38]);
  assert.deepEqual(schedule.requests.map((request) => request.waitMs), [18, 12, 6, 0]);
  assert.deepEqual(schedule.requests.map((request) => request.latencyMs), [38, 32, 26, 20]);
  assert.equal(schedule.meanLatencyMs, 29);
  assert.equal(schedule.maxLatencyMs, 38);
  assert.equal(schedule.capacityRps, 200);
  close(schedule.arrivalRps, 1000 / 6);
  assert.equal(schedule.overloaded, false);
  close(schedule.sustainableThroughputRps, 1000 / 6);
});

test("an initially short single-request trace hides a queue that grows under sustained arrivals", () => {
  const short = inferenceSchedule({ batchSize: 1 });
  assert.deepEqual(short.requests.map((request) => request.latencyMs), [8, 10, 12, 14]);
  assert.equal(short.capacityRps, 125);
  assert.equal(short.overloaded, true);
  assert.equal(short.sustainableThroughputRps, 125);
  const long = inferenceSchedule({ batchSize: 1, requestCount: 12 });
  assert.equal(long.maxLatencyMs, 30);
  assert.equal(long.requests.at(-1).waitMs, 22);
  const longer = inferenceSchedule({ batchSize: 1, requestCount: 16 });
  assert.equal(longer.maxLatencyMs, 38);
});

test("slower arrivals remove the single queue but make full batches wait longer to gather", () => {
  const single = inferenceSchedule({ batchSize: 1, arrivalIntervalMs: 12, requestCount: 12 });
  assert.equal(single.overloaded, false);
  assert.ok(single.requests.every((request) => request.waitMs === 0 && request.latencyMs === 8));
  const batch = inferenceSchedule({ arrivalIntervalMs: 12 });
  assert.deepEqual(batch.requests.map((request) => request.latencyMs), [56, 44, 32, 20]);
  assert.equal(batch.meanLatencyMs, 38);
  assert.equal(batch.capacityRps, 200);
  close(batch.sustainableThroughputRps, 1000 / 12);
});

test("every scheduled request is accounted for and one execution instance never overlaps groups", () => {
  for (const batchSize of [1, 4]) for (const arrivalIntervalMs of [1, 6, 8, 12, 20]) {
    const schedule = inferenceSchedule({ batchSize, arrivalIntervalMs, requestCount: 120 });
    assert.equal(schedule.requests.length, 120);
    assert.equal(schedule.batches.length, 120 / batchSize);
    assert.deepEqual(schedule.batches.flatMap((batch) => batch.requestIndices), Array.from({ length: 120 }, (_, index) => index));
    for (const request of schedule.requests) {
      assert.ok(request.startMs >= request.arrivalMs);
      assert.equal(request.finishMs - request.startMs, schedule.executionMs);
      assert.equal(request.latencyMs, request.waitMs + schedule.executionMs);
    }
    for (let index = 1; index < schedule.batches.length; index++)
      assert.ok(schedule.batches[index].startMs >= schedule.batches[index - 1].finishMs);
  }
});

test("inference validation does not invent measurements for unsupported or partial batches", () => {
  for (const batchSize of [0, 2, 3, 5, NaN, "4"])
    assert.throws(() => inferenceSchedule({ batchSize }), RangeError);
  for (const requestCount of [0, -1, 3, 5, 1.5, 100004, Infinity, "4"])
    assert.throws(() => inferenceSchedule({ requestCount }), RangeError);
  for (const arrivalIntervalMs of [0, -1, NaN, Infinity, "6", Number.MAX_VALUE, Number.MIN_VALUE])
    assert.throws(() => inferenceSchedule({ arrivalIntervalMs }), RangeError);
});

test("synchronized jobs expose the 480, 160, 240 kW waveform and 320 kW transition", () => {
  const result = phaseSchedule();
  assert.equal(result.cycleSeconds, 60);
  assert.equal(result.jobCount, 4);
  assert.deepEqual(result.segments.map((segment) => [segment.startSeconds, segment.endSeconds, segment.powerKW]),
    [[0, 30, 480], [30, 45, 160], [45, 60, 240]]);
  assert.equal(result.averageKW, 340);
  assert.equal(result.peakKW, 480);
  assert.equal(result.minKW, 160);
  assert.equal(result.maxTransitionKW, 320);
  close(result.energyKWh, 17 / 3);
  assert.deepEqual(result.transitions.find((transition) => transition.atSeconds === 30),
    { atSeconds: 30, fromKW: 480, toKW: 160, deltaKW: -320 });
  assert.equal(transitionRate(), -160);
});

test("staggering four independent periodic jobs preserves each phase and the cycle energy", () => {
  const result = phaseSchedule({ offsetsSeconds: [0, 15, 30, 45] });
  assert.equal(result.peakKW, 340);
  assert.equal(result.minKW, 340);
  assert.equal(result.averageKW, 340);
  assert.equal(result.maxTransitionKW, 0);
  close(result.energyKWh, 17 / 3);
  for (const segment of result.segments) {
    assert.equal(segment.jobPhases.filter((phase) => phase.kind === "compute").length, 2);
    assert.equal(segment.jobPhases.filter((phase) => phase.kind === "communication").length, 1);
    assert.equal(segment.jobPhases.filter((phase) => phase.kind === "checkpoint").length, 1);
  }
});

test("energy and per-job phase durations survive arbitrary offsets without sampling away transitions", () => {
  for (const offsetsSeconds of [[0], [59.5], [0, 3, 17, 41], [0.25, 15.75, 32.5]]) {
    const result = phaseSchedule({ offsetsSeconds });
    close(result.energyKWh, offsetsSeconds.length * 17 / 12);
    close(result.averageKW, offsetsSeconds.length * 85);
    for (let job = 0; job < offsetsSeconds.length; job++) {
      const durations = { compute: 0, communication: 0, checkpoint: 0 };
      for (const segment of result.segments)
        durations[segment.jobPhases[job].kind] += segment.endSeconds - segment.startSeconds;
      assert.deepEqual(durations, { compute: 30, communication: 15, checkpoint: 15 });
    }
    assert.equal(result.segments[0].startSeconds, 0);
    assert.equal(result.segments.at(-1).endSeconds, 60);
    for (let i = 1; i < result.segments.length; i++)
      assert.equal(result.segments[i - 1].endSeconds, result.segments[i].startSeconds);
  }
});

test("phase offsets and ramp intervals require valid physical inputs", () => {
  for (const offsetsSeconds of [null, {}, []])
    assert.throws(() => phaseSchedule({ offsetsSeconds }), TypeError);
  for (const offsetsSeconds of [[-1], [60], [Infinity], [NaN], ["0"]])
    assert.throws(() => phaseSchedule({ offsetsSeconds }), RangeError);
  for (const durationSeconds of [0, -1, NaN, Infinity, "2", Number.MIN_VALUE])
    assert.throws(() => transitionRate({ durationSeconds }), RangeError);
  assert.throws(() => transitionRate({ fromKW: -1 }), RangeError);
  assert.throws(() => transitionRate({ toKW: NaN }), RangeError);
  assert.equal(transitionRate({ fromKW: 160, toKW: 480 }), 160);
  assert.equal(transitionRate({ fromKW: 340, toKW: 340 }), 0);
});

test("acceptance checks every latency, offered traffic and capacity independently", () => {
  const batch = evaluateInferenceAcceptance();
  assert.equal(batch.meetsThroughputCapacity, true);
  assert.equal(batch.meetsArrivalRate, true);
  assert.equal(batch.meetsLatency, false);
  assert.deepEqual(batch.missedRequestIndices, [0, 1]);
  assert.equal(batch.numericalPass, false);
  const single = evaluateInferenceAcceptance({ schedule: inferenceSchedule({ batchSize: 1 }) });
  assert.equal(single.meetsLatency, true);
  assert.equal(single.meetsThroughputCapacity, true);
  assert.equal(single.meetsArrivalRate, false);
  assert.equal(single.numericalPass, false);
  const sparse = evaluateInferenceAcceptance({ schedule: inferenceSchedule({ batchSize: 1, arrivalIntervalMs: 12 }) });
  assert.equal(sparse.meetsLatency, true);
  assert.equal(sparse.meetsArrivalRate, true);
  assert.equal(sparse.sufficientOfferedLoad, false);
  assert.equal(sparse.numericalPass, false);
  const relaxed = evaluateInferenceAcceptance({ latencyLimitMs: 38 });
  assert.equal(relaxed.meetsLatency, true);
  assert.equal(relaxed.numericalPass, true);
  assert.equal(relaxed.unverifiedConditions.length, 4);
  assert.equal(evaluateInferenceAcceptance({ latencyLimitMs: 37.99 }).meetsLatency, false);
  assert.equal(evaluateInferenceAcceptance({ latencyLimitMs: 40, minThroughputRps: 201 }).meetsThroughputCapacity, false);
});

test("acceptance rejects missing or nonphysical measurements", () => {
  for (const schedule of [null, {}, { requests: [] }])
    assert.throws(() => evaluateInferenceAcceptance({ schedule }), TypeError);
  for (const latencyLimitMs of [0, -1, NaN, Infinity, "30"])
    assert.throws(() => evaluateInferenceAcceptance({ latencyLimitMs }), RangeError);
  for (const minThroughputRps of [-1, NaN, Infinity, "120"])
    assert.throws(() => evaluateInferenceAcceptance({ minThroughputRps }), RangeError);
  for (const requests of [[null], Array(2)])
    assert.throws(() => evaluateInferenceAcceptance({ schedule: { ...inferenceSchedule(), requests } }), TypeError);
  assert.throws(() => evaluateInferenceAcceptance({ schedule: {
    ...inferenceSchedule(), requests: [{ latencyMs: NaN }],
  } }), RangeError);
});

test("returned scenario state cannot mutate shared constants or caller-owned inputs", () => {
  const allocationGB = [64, 64, 64, 64];
  const budget = memoryBudget({ kind: "training", allocationGB });
  const offsetsSeconds = [0, 15, 30, 45];
  const phases = phaseSchedule({ offsetsSeconds });
  assert.notEqual(budget.allocationGB, allocationGB);
  assert.notEqual(phases.offsetsSeconds, offsetsSeconds);
  assert.deepEqual(allocationGB, [64, 64, 64, 64]);
  assert.deepEqual(offsetsSeconds, [0, 15, 30, 45]);
  assert.throws(() => { budget.allocationGB[0] = 0; }, TypeError);
  assert.throws(() => { WORKLOAD_PHASES[0].powerKW = 0; }, TypeError);
  assert.throws(() => { phases.segments[0].jobPhases[0].seconds = 0; }, TypeError);
  assert.throws(() => { inferenceSchedule().requests[0].latencyMs = 0; }, TypeError);
  assert.throws(() => { utilizationCase().phases[0].powerKW = 0; }, TypeError);
});
