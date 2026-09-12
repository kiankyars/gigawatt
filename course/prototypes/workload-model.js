/**
 * Original D02 teaching scenarios, not measurements of any named product.
 * Memory uses decimal GB. Power is at the same system AC boundary throughout;
 * no facility overhead, quality change, network delay or contention is inferred.
 */

function nonnegative(value, name) {
  if (!Number.isFinite(value) || value < 0)
    throw new RangeError(`${name} must be finite and non-negative.`);
  return value;
}

function positive(value, name) {
  nonnegative(value, name);
  if (value === 0) throw new RangeError(`${name} must be positive.`);
  return value;
}

function count(value, name) {
  if (!Number.isSafeInteger(value) || value < 1)
    throw new RangeError(`${name} must be a positive safe integer.`);
  return value;
}

/**
 * Capacity screening only. A multi-device total does not supply a partition.
 * A supplied allocation must account for the complete stated budget; passing it
 * still does not establish implementation feasibility or performance.
 */
export function memoryBudget({
  kind = "inference",
  workspaceGB = kind === "training" ? 64 : 20,
  deviceCount = kind === "training" ? 4 : 1,
  deviceCapacityGB = 80,
  allocationGB,
} = {}) {
  if (!["inference", "training"].includes(kind))
    throw new RangeError("Memory kind must be inference or training.");
  nonnegative(workspaceGB, "Workspace in GB");
  count(deviceCount, "Device count");
  positive(deviceCapacityGB, "Per-device capacity in GB");
  const parametersBillions = 12;
  const bytesPerParameter = kind === "training" ? 16 : 2;
  const stateGB = parametersBillions * bytesPerParameter;
  const reservationGB = kind === "training" ? 0 : 8;
  const totalGB = positive(stateGB + workspaceGB + reservationGB, "Memory budget");
  const aggregateCapacityGB = positive(deviceCount * deviceCapacityGB, "Aggregate capacity");
  const aggregateFits = totalGB <= aggregateCapacityGB;
  if (allocationGB === undefined && deviceCount === 1) allocationGB = [totalGB];
  let deviceFits = null;
  let partitionFits = null;
  if (allocationGB !== undefined) {
    if (!Array.isArray(allocationGB) || allocationGB.length !== deviceCount)
      throw new TypeError("An allocation needs one memory total per device.");
    for (const gb of allocationGB) nonnegative(gb, "Device allocation");
    const allocatedGB = allocationGB.reduce(
      (sum, gb) => nonnegative(sum + nonnegative(gb, "Device allocation"), "Allocated memory"),
      0,
    );
    if (Math.abs(allocatedGB - totalGB) > 1e-9 * Math.max(1, totalGB))
      throw new RangeError("Device allocations must account for the full memory budget.");
    allocationGB = Object.freeze([...allocationGB]);
    deviceFits = Object.freeze(allocationGB.map((gb) => gb <= deviceCapacityGB));
    partitionFits = deviceFits.every(Boolean);
  }
  const fitStatus = !aggregateFits ? "aggregate-fails"
    : partitionFits === null ? "partition-unverified"
      : partitionFits ? "capacity-screen-passes" : "partition-fails";
  return Object.freeze({
    kind, parametersBillions, bytesPerParameter, stateGB, workspaceGB, reservationGB,
    totalGB, deviceCount, deviceCapacityGB, aggregateCapacityGB, aggregateFits,
    aggregateHeadroomGB: aggregateCapacityGB - totalGB,
    allocationGB: allocationGB ?? null, deviceFits, partitionFits, fitStatus,
  });
}

/** Integrate every interval, then divide by accepted output from that interval. */
export function computeObservation({
  computeSeconds = 45,
  idleSeconds = 0,
  waitSeconds = 60 - computeSeconds - idleSeconds,
  computeKW = 60,
  waitKW = 25,
  idleKW = 12,
  acceptedSamplesPerComputeSecond = 1000,
} = {}) {
  for (const [name, value] of Object.entries({
    computeSeconds, waitSeconds, idleSeconds, computeKW, waitKW, idleKW,
    acceptedSamplesPerComputeSecond,
  })) nonnegative(value, name);
  const seconds = positive(computeSeconds + waitSeconds + idleSeconds, "Observation duration");
  let elapsed = 0;
  const phases = [
    { kind: "compute", seconds: computeSeconds, powerKW: computeKW, allocated: true },
    { kind: "wait", seconds: waitSeconds, powerKW: waitKW, allocated: true },
    { kind: "idle", seconds: idleSeconds, powerKW: idleKW, allocated: false },
  ].filter((phase) => phase.seconds > 0).map((phase) => {
    const startSeconds = elapsed;
    elapsed += phase.seconds;
    return Object.freeze({ ...phase, startSeconds, endSeconds: elapsed });
  });
  const energyJ = nonnegative(phases.reduce(
    (total, phase) => total + phase.powerKW * 1000 * phase.seconds, 0,
  ), "Observation energy");
  const acceptedSamples = nonnegative(
    computeSeconds * acceptedSamplesPerComputeSecond, "Accepted samples",
  );
  return Object.freeze({
    seconds, phases: Object.freeze(phases), energyJ, energyKWh: energyJ / 3600000,
    averageKW: nonnegative(energyJ / seconds / 1000, "Average power"), acceptedSamples,
    joulesPerAcceptedSample: acceptedSamples === 0 ? null
      : nonnegative(energyJ / acceptedSamples, "Energy per accepted sample"),
    executionFraction: computeSeconds / seconds,
    allocationFraction: (computeSeconds + waitSeconds) / seconds,
  });
}

/** C is the 50-second practice case; the no-assignment case is named idle. */
export function utilizationCase(name = "A") {
  const cases = {
    A: { computeSeconds: 45 },
    B: { computeSeconds: 30 },
    C: { computeSeconds: 50 },
    idle: { computeSeconds: 0, waitSeconds: 0, idleSeconds: 60 },
  };
  if (!Object.hasOwn(cases, name))
    throw new RangeError("Utilization case must be A, B, C or idle.");
  return computeObservation(cases[name]);
}

/**
 * One non-preemptive execution instance, FIFO arrivals from an initially empty
 * queue. Full groups only: no timing for partial batches has been supplied.
 * Execution is 8 ms for one request and 20 ms for four, independent of arrivals.
 * A finite trace's latency is separate from stability under sustained arrivals.
 */
export function inferenceSchedule({
  batchSize = 4,
  arrivalIntervalMs = 6,
  requestCount = 4,
} = {}) {
  if (![1, 4].includes(batchSize))
    throw new RangeError("Only the supplied batch sizes 1 and 4 have execution timings.");
  positive(arrivalIntervalMs, "Arrival interval in ms");
  count(requestCount, "Request count");
  if (requestCount > 100000 || requestCount % batchSize !== 0)
    throw new RangeError("Use at most 100000 requests and a whole number of full batches.");
  const executionMs = batchSize === 1 ? 8 : 20;
  const arrivalsMs = Array.from({ length: requestCount }, (_, i) =>
    nonnegative(i * arrivalIntervalMs, "Arrival time"));
  const requests = [];
  const batches = [];
  let availableMs = 0;
  for (let first = 0; first < requestCount; first += batchSize) {
    const startMs = Math.max(availableMs, arrivalsMs[first + batchSize - 1]);
    const finishMs = positive(startMs + executionMs, "Completion time");
    const requestIndices = [];
    for (let index = first; index < first + batchSize; index++) {
      requestIndices.push(index);
      requests.push(Object.freeze({
        index, arrivalMs: arrivalsMs[index], startMs, finishMs,
        waitMs: startMs - arrivalsMs[index], latencyMs: finishMs - arrivalsMs[index],
      }));
    }
    batches.push(Object.freeze({
      startMs, finishMs, requestIndices: Object.freeze(requestIndices),
    }));
    availableMs = finishMs;
  }
  const capacityRps = batchSize * 1000 / executionMs;
  const arrivalRps = positive(1000 / arrivalIntervalMs, "Arrival rate");
  return Object.freeze({
    batchSize, executionMs, arrivalIntervalMs, requestCount,
    arrivalsMs: Object.freeze(arrivalsMs), requests: Object.freeze(requests),
    batches: Object.freeze(batches), capacityRps, arrivalRps,
    overloaded: arrivalRps > capacityRps,
    sustainableThroughputRps: Math.min(arrivalRps, capacityRps),
    meanLatencyMs: nonnegative(requests.reduce((sum, request) =>
      sum + request.latencyMs / requestCount, 0), "Mean latency"),
    maxLatencyMs: requests.reduce((max, request) => Math.max(max, request.latencyMs), 0),
    finishMs: availableMs,
  });
}

export const WORKLOAD_PHASES = Object.freeze([
  Object.freeze({ kind: "compute", seconds: 30, powerKW: 120 }),
  Object.freeze({ kind: "communication", seconds: 15, powerKW: 40 }),
  Object.freeze({ kind: "checkpoint", seconds: 15, powerKW: 60 }),
]);

/**
 * Periodic steady operation, including jobs already running at t=0. Offsetting
 * independent jobs preserves their cycle time and energy; startup, coupled
 * workers, shared-resource contention and ramp shapes are outside this account.
 */
export function phaseSchedule({ offsetsSeconds = [0, 0, 0, 0] } = {}) {
  if (!Array.isArray(offsetsSeconds) || offsetsSeconds.length === 0)
    throw new TypeError("Supply at least one independent job offset.");
  const cycleSeconds = 60;
  for (const offset of offsetsSeconds) {
    nonnegative(offset, "Job offset");
    if (offset >= cycleSeconds)
      throw new RangeError("Offsets must be inside the 60-second cycle.");
  }
  const modulo = (time) => (time % cycleSeconds + cycleSeconds) % cycleSeconds;
  const boundaries = [...new Set([0, cycleSeconds, ...offsetsSeconds.flatMap((offset) =>
    [0, 30, 45].map((boundary) => modulo(offset + boundary)),
  )])].sort((a, b) => a - b);
  const segments = boundaries.slice(0, -1).map((startSeconds, i) => {
    const endSeconds = boundaries[i + 1];
    const jobPhases = offsetsSeconds.map((offset) => {
      const time = modulo((startSeconds + endSeconds) / 2 - offset);
      return WORKLOAD_PHASES[time < 30 ? 0 : time < 45 ? 1 : 2];
    });
    return Object.freeze({
      startSeconds, endSeconds, jobPhases: Object.freeze(jobPhases),
      powerKW: positive(jobPhases.reduce((sum, phase) => sum + phase.powerKW, 0), "Aggregate power"),
    });
  });
  const energyKWh = positive(segments.reduce((sum, segment) =>
    sum + segment.powerKW * (segment.endSeconds - segment.startSeconds) / 3600, 0,
  ), "Cycle energy");
  const transitions = segments.map((segment, index) => Object.freeze({
    atSeconds: segment.startSeconds,
    fromKW: segments[(index + segments.length - 1) % segments.length].powerKW,
    toKW: segment.powerKW,
    deltaKW: segment.powerKW - segments[(index + segments.length - 1) % segments.length].powerKW,
  }));
  return Object.freeze({
    cycleSeconds, jobCount: offsetsSeconds.length,
    offsetsSeconds: Object.freeze([...offsetsSeconds]), segments: Object.freeze(segments),
    transitions: Object.freeze(transitions), energyKWh,
    averageKW: energyKWh * 3600 / cycleSeconds,
    peakKW: segments.reduce((max, segment) => Math.max(max, segment.powerKW), 0),
    minKW: segments.reduce((min, segment) => Math.min(min, segment.powerKW), Infinity),
    maxTransitionKW: transitions.reduce((max, transition) => Math.max(max, Math.abs(transition.deltaKW)), 0),
  });
}

/** A separate measured transition interval is required to calculate a ramp. */
export function transitionRate({ fromKW = 480, toKW = 160, durationSeconds = 2 } = {}) {
  nonnegative(fromKW, "Initial power");
  nonnegative(toKW, "Final power");
  positive(durationSeconds, "Transition duration");
  return nonnegative(Math.abs(toKW - fromKW) / durationSeconds, "Ramp magnitude")
    * Math.sign(toKW - fromKW);
}

/**
 * Numerical checks for this toy trace, never overall production acceptance.
 * The latency limit is inclusive and applies to every request (not the mean).
 * Insufficient offered traffic cannot demonstrate the requested service rate.
 */
export function evaluateInferenceAcceptance({
  schedule = inferenceSchedule(), latencyLimitMs = 30, minThroughputRps = 120,
} = {}) {
  positive(latencyLimitMs, "Every-request latency limit");
  nonnegative(minThroughputRps, "Minimum accepted request rate");
  if (!schedule || !Array.isArray(schedule.requests) || schedule.requests.length === 0)
    throw new TypeError("Acceptance requires a non-empty inference schedule.");
  positive(schedule.capacityRps, "Supplied execution capacity");
  positive(schedule.arrivalRps, "Supplied arrival rate");
  const missedRequestIndices = [];
  for (const [index, request] of schedule.requests.entries()) {
    if (!request) throw new TypeError("Every request needs a latency.");
    nonnegative(request.latencyMs, "Request latency");
    if (request.latencyMs > latencyLimitMs) missedRequestIndices.push(index);
  }
  const meetsLatency = missedRequestIndices.length === 0;
  const meetsThroughputCapacity = schedule.capacityRps >= minThroughputRps;
  const meetsArrivalRate = schedule.arrivalRps <= schedule.capacityRps;
  const sufficientOfferedLoad = schedule.arrivalRps >= minThroughputRps;
  return Object.freeze({
    latencyLimitMs, minThroughputRps, meetsLatency, meetsThroughputCapacity,
    meetsArrivalRate, sufficientOfferedLoad,
    missedRequestIndices: Object.freeze(missedRequestIndices),
    numericalPass: meetsLatency && meetsThroughputCapacity && meetsArrivalRate && sufficientOfferedLoad,
    unverifiedConditions: Object.freeze([
      "Model quality, precision and input/output distributions",
      "End-to-end network and other service delays",
      "Measured system power and electrical/thermal limits",
      "Availability, failures, maintenance and recovery",
    ]),
  });
}
