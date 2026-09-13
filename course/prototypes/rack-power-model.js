const positive = (value, label) => {
  if (!Number.isFinite(value) || value <= 0) throw new RangeError(`${label} must be positive`);
};

export function localPower({ watts = 1000, rackVolts = 50, coreVolts = 1, loopMicroOhms = 100 } = {}) {
  for (const [label, value] of Object.entries({ watts, rackVolts, coreVolts, loopMicroOhms })) positive(value, label);
  const rackAmps = watts / rackVolts, coreAmps = watts / coreVolts, resistanceOhms = loopMicroOhms * 1e-6;
  return { rackAmps, coreAmps, lossWatts: coreAmps ** 2 * resistanceOhms, dropVolts: coreAmps * resistanceOhms };
}

export function supplyHandoff({ extraKW = 40, responseSeconds = 0.2 } = {}) {
  positive(extraKW, 'Extra load'); positive(responseSeconds, 'Response time');
  return { energyKJ: extraKW * responseSeconds / 2, peakBufferKW: extraKW, responseSeconds, extraKW };
}

export function bbuShelf({ failedModules = 0, loadKW = 15 } = {}) {
  if (!Number.isInteger(failedModules) || failedModules < 0 || failedModules > 6) throw new RangeError('Failed module count must be 0–6');
  positive(loadKW, 'Load');
  const availableModules = 6 - failedModules, availableKW = availableModules * 3;
  return { availableModules, availableKW, loadKW, deficitKW: Math.max(0, loadKW - availableKW), capacityPass: availableKW >= loadKW, spareKW: availableKW - loadKW };
}

export function burstRecharge({ restSeconds = 10 } = {}) {
  positive(restSeconds, 'Time between bursts');
  const supplyKW = 120, idleLoadKW = 110, burstLoadKW = 160, burstSeconds = 0.2;
  const energyKJ = (burstLoadKW - supplyKW) * burstSeconds;
  const rechargeKW = supplyKW - idleLoadKW, rechargeKJ = Math.min(energyKJ, rechargeKW * restSeconds);
  return { supplyKW, idleLoadKW, burstLoadKW, burstSeconds, energyKJ, rechargeKW, rechargeKJ,
    missingKJ: energyKJ - rechargeKJ, requiredRestSeconds: energyKJ / rechargeKW,
    averageLoadKW: (burstLoadKW * burstSeconds + idleLoadKW * restSeconds) / (burstSeconds + restSeconds) };
}

// Normalized teaching waveforms: fixed average total current, duty ratio 0.30,
// triangular ripple proportional to each phase's average. No component sizing.
export function phaseWaveforms(phases = 4) {
  if (![1, 4].includes(phases)) throw new RangeError('Use one or four phases');
  const duty = 0.3, totalAmps = 1000, samples = 240;
  const phaseCurrent = (time, phase) => {
    const p = (time + phase / phases) % 1;
    const triangle = p < duty ? p / duty : (1 - p) / (1 - duty);
    return totalAmps / phases + (triangle - 0.5) * 400 / phases;
  };
  const curves = Array.from({ length: phases }, (_, phase) => Array.from({ length: samples + 1 }, (_, i) => phaseCurrent(i / samples, phase)));
  const sum = Array.from({ length: samples + 1 }, (_, i) => curves.reduce((a, curve) => a + curve[i], 0));
  return { curves, sum, totalAmps, peakToPeakAmps: Math.max(...sum) - Math.min(...sum) };
}
