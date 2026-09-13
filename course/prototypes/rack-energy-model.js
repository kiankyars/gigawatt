// Chapter 8 accounts at explicitly declared electrical boundaries.
export function rackLedger({ auxiliaryKW = 12 } = {}) {
  if (!Number.isFinite(auxiliaryKW) || auxiliaryKW < 0) throw new RangeError('Auxiliary power must be nonnegative');
  const processorKW = 72, regulatorEfficiency = 0.92, shelfEfficiency = 0.97;
  const regulatorInputKW = processorKW / regulatorEfficiency;
  const busKW = regulatorInputKW + auxiliaryKW, inputKW = busKW / shelfEfficiency;
  return { processorKW, auxiliaryKW, regulatorEfficiency, shelfEfficiency, regulatorInputKW, busKW, inputKW,
    regulatorLossKW: regulatorInputKW - processorKW, shelfLossKW: inputKW - busKW };
}

export function dcPlanes({ powerKW = 100 } = {}) {
  if (!Number.isFinite(powerKW) || powerKW <= 0) throw new RangeError('Power must be positive');
  return { powerKW, lowAmps: powerKW * 1000 / 50, highAmps: powerKW * 1000 / 800 };
}

export function migrationDecision({ rackKW = 120, allocationKW = 240, deadlineWeeks = 3 } = {}) {
  if (![110,120].includes(rackKW) || ![240,260].includes(allocationKW) || ![3,8].includes(deadlineWeeks)) throw new RangeError('Use the declared migration choices');
  const inputKW = 2 * rackKW / 0.96 + 3, readyWeeks = allocationKW === 260 ? 6 : 2;
  return { inputKW, marginKW: allocationKW - inputKW, readyWeeks, powerPass: inputKW <= allocationKW,
    schedulePass: readyWeeks <= deadlineWeeks, deadlineWeeks, rackKW, allocationKW };
}
