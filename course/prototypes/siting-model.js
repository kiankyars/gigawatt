export function readiness(site) {
  const dates = site === 'A' ? [18, 22, 21, 20] : [20, 19, 20, 21];
  const readyMonth = Math.max(...dates);
  return { dates, readyMonth, limiting: ['Power', 'Building', 'Cooling', 'Fiber'].filter((_, i) => dates[i] === readyMonth) };
}

export function matching(mode = 'ideal') {
  const efficiency = mode === 'losses' ? 0.9 : 1;
  const outputMW = mode === 'power' ? 2 : 10;
  const returnedMWh = 120 * efficiency;
  return { loadMWh: 240, generationMWh: 240, surplusMWh: 120, deficitMWh: 120,
    returnedMWh, outputMW, energyShortfallMWh: 120 - returnedMWh,
    unsupportedMW: Math.max(0, 10 - outputMW), requiredChargeMWh: 120 / efficiency };
}

export function busBalance(generatorMW = 6, loadMW = 8) {
  return { loadMW, generatorMW, gridMW: loadMW - generatorMW };
}

export function islandBudget(loadMW = 8) {
  const deficitMW = Math.max(0, loadMW - 6);
  const batteryHours = deficitMW === 0 ? null : 4 / deficitMW;
  const powerPass = deficitMW <= 3;
  const durationHours = powerPass ? Math.min(batteryHours ?? 4, 4) : 0;
  return { loadMW, deficitMW, batteryHours, powerPass, fuelHours: 4, durationHours };
}
