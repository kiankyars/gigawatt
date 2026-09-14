const positive = (value, name) => {
  if (!Number.isFinite(value) || value <= 0) throw new RangeError(`${name} must be positive`);
  return value;
};
const fraction = (value, name) => {
  positive(value, name);
  if (value > 1) throw new RangeError(`${name} must not exceed one`);
  return value;
};
const nonnegative = (value, name) => {
  if (!Number.isFinite(value) || value < 0) throw new RangeError(`${name} must be nonnegative`);
  return value;
};

// kW at a DC output; balanced AC line-to-line RMS volts at the input.
export function loadFromDc({ outputKW = 900, efficiency = .96, powerFactor = .9, voltageLL = 480, limitKVA = 1000 } = {}) {
  positive(outputKW, 'outputKW'); fraction(efficiency, 'efficiency'); fraction(powerFactor, 'powerFactor');
  positive(voltageLL, 'voltageLL'); positive(limitKVA, 'limitKVA');
  const inputKW = outputKW / efficiency;
  const apparentKVA = inputKW / powerFactor;
  return { outputKW, inputKW, lossKW: inputKW - outputKW, apparentKVA,
    currentA: apparentKVA * 1000 / (Math.sqrt(3) * voltageLL),
    loading: apparentKVA / limitKVA, passes: apparentKVA <= limitKVA };
}

export function reservedOutput({ ratingKVA = 1200, reserve = .2, powerFactor = .9, efficiency = .96 } = {}) {
  positive(ratingKVA, 'ratingKVA'); nonnegative(reserve, 'reserve');
  if (reserve >= 1) throw new RangeError('reserve must be below one');
  fraction(powerFactor, 'powerFactor'); fraction(efficiency, 'efficiency');
  const budgetKVA = ratingKVA * (1 - reserve);
  return { budgetKVA, reservedKVA: ratingKVA - budgetKVA, inputKW: budgetKVA * powerFactor, outputKW: budgetKVA * powerFactor * efficiency };
}

export function phaseLedger({ itMW = 4.6, auxiliaryMW = 1, lossMW = .2, serviceMW = 6, branchMW = 4.8 } = {}) {
  for (const [key, value] of Object.entries({itMW, auxiliaryMW, lossMW})) nonnegative(value, key);
  positive(serviceMW, 'serviceMW'); positive(branchMW, 'branchMW');
  const inputMW = itMW + auxiliaryMW + lossMW;
  return { inputMW, itMW, auxiliaryMW, lossMW, serviceMW, branchMW,
    serviceHeadroomMW: serviceMW - inputMW, branchHeadroomMW: branchMW - itMW,
    limits: [inputMW > serviceMW && 'service', itMW > branchMW && 'IT branch'].filter(Boolean) };
}

export function conversionPath(outputKW, efficiencies) {
  positive(outputKW, 'outputKW');
  if (!Array.isArray(efficiencies) || !efficiencies.length) throw new RangeError('At least one stage is required');
  let required = outputKW;
  const stages = [];
  for (let i = efficiencies.length - 1; i >= 0; i--) {
    fraction(efficiencies[i], 'efficiency');
    const inputKW = required / efficiencies[i];
    stages.unshift({ inputKW, outputKW: required, lossKW: inputKW - required });
    required = inputKW;
  }
  return { inputKW: required, outputKW, lossKW: required - outputKW, stages };
}

export function rowBudget(loadsKW, { voltageLL = 415, powerFactor = 1, budgetA = 250 } = {}) {
  if (!Array.isArray(loadsKW) || !loadsKW.length) throw new RangeError('At least one branch is required');
  loadsKW.forEach(load => nonnegative(load, 'loadKW'));
  positive(voltageLL, 'voltageLL'); fraction(powerFactor, 'powerFactor'); positive(budgetA, 'budgetA');
  const current = kw => kw * 1000 / (Math.sqrt(3) * voltageLL * powerFactor);
  return { totalKW: loadsKW.reduce((a,b) => a+b, 0), branchA: loadsKW.map(current),
    segmentsA: loadsKW.map((_, i) => current(loadsKW.slice(i).reduce((a,b) => a+b,0))),
    currentA: current(loadsKW.reduce((a,b) => a+b,0)), capacityKW: budgetA * Math.sqrt(3) * voltageLL * powerFactor / 1000 };
}

export const topology = Object.freeze({
  row: ['high-voltage-grid','campus-transformer','service','campus-bus','hall-feeder','transformer','building-bus','it-feeder','row-bus','rack'],
  cooling: ['high-voltage-grid','campus-transformer','service','campus-bus','hall-feeder','transformer','building-bus','cooling-feeder','pump'],
  future: ['high-voltage-grid','campus-transformer','service','campus-bus','future-feeder','future-hall'],
});
export function traceLoad(load, { futureClosed = false } = {}) {
  if (!Object.hasOwn(topology,load)) throw new RangeError(`Unknown load: ${load}`);
  return { path: [...topology[load]], energized: load !== 'future' || futureClosed,
    stopsAt: load === 'future' && !futureClosed ? 'future-feeder' : null };
}
