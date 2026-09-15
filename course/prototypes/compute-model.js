// Compute reference models: SI quantities and configured job boundaries.

function positive(value, name) {
  if (!Number.isFinite(value) || value <= 0) throw new RangeError(`${name} must be finite and positive`);
  return value;
}

function nonnegative(value, name) {
  if (!Number.isFinite(value) || value < 0) throw new RangeError(`${name} must be finite and nonnegative`);
  return value;
}

function positiveInteger(value, name) {
  if (!Number.isSafeInteger(value) || value <= 0) throw new RangeError(`${name} must be a positive safe integer`);
  return value;
}

/**
 * Lower bound when the specified compute and HBM transfers overlap completely.
 * Rates are effective rates for this operation, not interchangeable nameplate peaks.
 * No network, launch, synchronization or other work is included in the account.
 */
export function workloadBound({
  flops,
  hbmBytes,
  computeFlopsPerSecond = 200e12,
  hbmBytesPerSecond = 8e12,
} = {}) {
  nonnegative(flops, 'Work in FLOPs');
  nonnegative(hbmBytes, 'HBM bytes transferred');
  positive(computeFlopsPerSecond, 'Compute rate in FLOP/s');
  positive(hbmBytesPerSecond, 'HBM rate in bytes/s');
  const computeSeconds = flops / computeFlopsPerSecond;
  const memorySeconds = hbmBytes / hbmBytesPerSecond;
  const overlappedSeconds = Math.max(computeSeconds, memorySeconds);
  const serialSeconds = computeSeconds + memorySeconds;
  const arithmeticIntensity = hbmBytes === 0 ? (flops === 0 ? 0 : Infinity) : flops / hbmBytes;
  const bottleneck = overlappedSeconds === 0 ? 'idle'
    : computeSeconds === memorySeconds ? 'balanced'
      : computeSeconds > memorySeconds ? 'compute' : 'memory';
  return {
    flops, hbmBytes, computeFlopsPerSecond, hbmBytesPerSecond,
    computeSeconds, memorySeconds, overlappedSeconds, serialSeconds,
    arithmeticIntensity, bottleneck,
  };
}

/** Arithmetic intensity counts work per byte transferred from HBM. */
export function roofline({
  arithmeticIntensity,
  computeFlopsPerSecond = 200e12,
  hbmBytesPerSecond = 8e12,
} = {}) {
  // Infinity represents work with no accounted HBM transfer.
  if (arithmeticIntensity !== Infinity) nonnegative(arithmeticIntensity, 'Arithmetic intensity in FLOP/byte');
  positive(computeFlopsPerSecond, 'Compute rate in FLOP/s');
  positive(hbmBytesPerSecond, 'HBM rate in bytes/s');
  const kneeFlopsPerByte = computeFlopsPerSecond / hbmBytesPerSecond;
  const bandwidthCeilingFlopsPerSecond = hbmBytesPerSecond * arithmeticIntensity;
  const attainableFlopsPerSecond = Math.min(computeFlopsPerSecond, bandwidthCeilingFlopsPerSecond);
  const bottleneck = arithmeticIntensity === kneeFlopsPerByte ? 'balanced'
    : arithmeticIntensity < kneeFlopsPerByte ? 'memory' : 'compute';
  return {
    arithmeticIntensity, computeFlopsPerSecond, hbmBytesPerSecond,
    kneeFlopsPerByte, bandwidthCeilingFlopsPerSecond,
    attainableFlopsPerSecond, bottleneck,
  };
}

/**
 * Configured independent allocation groups. Each job fits wholly in one group;
 * healthy fragments cannot be combined across groups in this scheduling mode.
 * Within a group, any healthy devices can form the declared fixed-size job.
 * This is a scheduling configuration, not a hardware claim about NVL72 faults.
 */
export function serviceDomains({
  devicesPerGroup = 8,
  failedByGroup = [4, 0, 0, 0],
  devicesPerJob = 8,
} = {}) {
  positiveInteger(devicesPerGroup, 'Devices per group');
  positiveInteger(devicesPerJob, 'Devices per job');
  if (devicesPerJob > devicesPerGroup) throw new RangeError('The specified job must fit within one allocation group');
  if (!Array.isArray(failedByGroup) || failedByGroup.length === 0) throw new RangeError('Supply at least one allocation group');
  const groups = failedByGroup.map((failedDevices, index) => {
    if (!Number.isSafeInteger(failedDevices) || failedDevices < 0 || failedDevices > devicesPerGroup) {
      throw new RangeError('Failed devices must be a whole number within each group');
    }
    const healthyDevices = devicesPerGroup - failedDevices;
    const runnableJobs = Math.floor(healthyDevices / devicesPerJob);
    const allocatedDevices = runnableJobs * devicesPerJob;
    return {
      index, totalDevices: devicesPerGroup, failedDevices, healthyDevices,
      runnableJobs, allocatedDevices,
      strandedHealthyDevices: healthyDevices - allocatedDevices,
      fullyHealthy: failedDevices === 0,
    };
  });
  const totalDevices = groups.length * devicesPerGroup;
  const healthyDevices = groups.reduce((sum, group) => sum + group.healthyDevices, 0);
  const failedDevices = totalDevices - healthyDevices;
  const runnableJobs = groups.reduce((sum, group) => sum + group.runnableJobs, 0);
  const nominalJobs = groups.length * Math.floor(devicesPerGroup / devicesPerJob);
  const allocatedDevices = runnableJobs * devicesPerJob;
  return {
    devicesPerGroup, devicesPerJob, groups, totalDevices, failedDevices, healthyDevices,
    healthyFraction: healthyDevices / totalDevices,
    nominalJobs, runnableJobs, jobSlotFraction: runnableJobs / nominalJobs,
    fullHealthyGroups: groups.filter(group => group.fullyHealthy).length,
    allocatedDevices, strandedHealthyDevices: healthyDevices - allocatedDevices,
  };
}

/**
 * Service acceptance for a specified job and its required interfaces.
 * A reduced operating mode must be validated before limited inputs enable service.
 * Output is a readiness decision, not a throughput prediction or protection model.
 */
export function rackAcceptance({
  power = 'ready',
  coolant = 'ready',
  fabric = 'ready',
  software = 'ready',
  reducedServiceValidated = false,
} = {}) {
  const inputs = { power, coolant, fabric, software };
  for (const [name, status] of Object.entries(inputs)) {
    if (!['ready', 'limited', 'unavailable'].includes(status)) {
      throw new RangeError(`${name} must be ready, limited or unavailable`);
    }
  }
  if (typeof reducedServiceValidated !== 'boolean') throw new TypeError('Reduced service validation must be true or false');
  const unavailableInputs = Object.keys(inputs).filter(name => inputs[name] === 'unavailable');
  const limitedInputs = Object.keys(inputs).filter(name => inputs[name] === 'limited');
  const service = unavailableInputs.length ? 'blocked'
    : limitedInputs.length ? (reducedServiceValidated ? 'limited' : 'blocked') : 'full';
  const reason = unavailableInputs.length ? 'missing-input'
    : limitedInputs.length ? (reducedServiceValidated ? 'validated-reduced-mode' : 'unvalidated-reduced-mode') : 'all-inputs-ready';
  const blockedBy = unavailableInputs.length ? unavailableInputs
    : (limitedInputs.length && !reducedServiceValidated ? limitedInputs : []);
  return {
    inputs, reducedServiceValidated, unavailableInputs, limitedInputs,
    service, canRun: service !== 'blocked', blockedBy, reason,
  };
}
