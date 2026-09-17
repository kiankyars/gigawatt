// Original teaching inputs, shared with the three D13 reader lessons.
function nonnegative(value, name) {
  if (!Number.isFinite(value) || value < 0) throw new RangeError(`${name} must be a nonnegative number`);
  return value;
}
export function deliverySchedule({electricalProcurement = 18, coolingProcurement = 10, utilityReady = 16} = {}) {
  [electricalProcurement, coolingProcurement, utilityReady].forEach(value => nonnegative(value, 'Duration'));
  const electrical = 2 + electricalProcurement + 3, cooling = 2 + coolingProcurement + 4;
  const join = Math.max(electrical, cooling, utilityReady);
  return {electrical, cooling, utility: utilityReady, join, finish: join + 4,
    critical: [['electrical', electrical], ['cooling', cooling], ['utility', utilityReady]].filter(([, finish]) => finish === join).map(([name]) => name),
    slack: {electrical: join - electrical, cooling: join - cooling, utility: join - utilityReady}};
}
export function modularSchedule({approvalWeek = 0, factorySlotWeek = 0, factoryWeeks = 6, transportWeeks = 1, siteReady = 8, connectionsWeeks = 2, acceptanceWeeks = 2, siteAssemblyWeeks = 6} = {}) {
  [approvalWeek, factorySlotWeek, factoryWeeks, transportWeeks, siteReady, connectionsWeeks, acceptanceWeeks, siteAssemblyWeeks].forEach(value => nonnegative(value, 'Week'));
  const factoryStart = Math.max(approvalWeek, factorySlotWeek), factoryFinish = factoryStart + factoryWeeks;
  const arrival = factoryFinish + transportWeeks, connectionStart = Math.max(arrival, siteReady);
  const connectionsFinish = connectionStart + connectionsWeeks, finish = connectionsFinish + acceptanceWeeks;
  const siteAssemblyStart = Math.max(siteReady, approvalWeek), siteBuiltFinish = siteAssemblyStart + siteAssemblyWeeks + acceptanceWeeks;
  return {factoryStart, factoryFinish, arrival, connectionStart, connectionsFinish, finish, siteAssemblyStart, siteBuiltFinish, arrivalFloat: Math.max(0, siteReady - arrival), saving: siteBuiltFinish - finish};
}
export function rackInterfaces({rackKW = 200, voltage = 480, powerFactor = 1, deltaT = 10, allowableAmps = 160, allowableFlow = 3, availablePressure = 60} = {}) {
  for (const [name, value] of Object.entries({rackKW, voltage, powerFactor, deltaT})) if (!Number.isFinite(value) || value <= 0) throw new RangeError(`${name} must be positive`);
  const amps = rackKW * 1000 / (Math.sqrt(3) * voltage * powerFactor), flow = rackKW / (4.18 * deltaT);
  const oldFlow = 100 / (4.18 * 10), pressure = 20 * (flow / oldFlow) ** 2;
  return {rackKW, amps, flow, pressure, racks: 20000 / rackKW, racksPerZone: 2000 / rackKW, phaseFlow: 20000 / (4.18 * deltaT), zoneFlow: 2000 / (4.18 * deltaT),
    electricalPass: amps <= allowableAmps, flowPass: flow <= allowableFlow, pressurePass: pressure <= availablePressure,
    // Supplied vendor drawing, never inferred from power alone.
    massPerRackRatio: rackKW === 200 ? 2 : 1, loadPerFootRatio: rackKW === 200 ? 2 : 1};
}
export function releaseHolds({electrical = false, hydraulic = false, geometry = false, logistics = false, controls = false, resources = false} = {}) {
  return {independentSite: true, electricalFabrication: electrical && geometry, hydraulicFabrication: hydraulic && geometry, frameFabrication: geometry, transportPlan: geometry && logistics, configuration: controls, scheduleCommitment: electrical && hydraulic && geometry && logistics && controls && resources, serviceAcceptance: false};
}
export function acceptedPaths({electricalEnd = 80, coolingStart = 21, coolingEnd = 100, networkEnd = 60, rackKW = 200} = {}) {
  const positions = Array.from({length: 100}, (_, i) => {
    const id = i + 1, electrical = id <= electricalEnd, cooling = id >= coolingStart && id <= coolingEnd, network = id <= networkEnd;
    return {id, electrical, cooling, network, accepted: electrical && cooling && network};
  });
  const accepted = positions.filter(position => position.accepted);
  return {positions, accepted, count: accepted.length, envelopeMW: accepted.length * rackKW / 1000};
}

const rackRange = (start, end) => Array.from({length: end - start + 1}, (_, i) => start + i);
function rackIdSet(ids, name) {
  if (!Array.isArray(ids) || ids.some(id => !Number.isInteger(id) || id < 1 || id > 100)) {
    throw new RangeError(`${name} must contain rack IDs from 1 to 100`);
  }
  return new Set(ids);
}
/**
 * Complete paths and passing measured responses must cover the same racks.
 * responsePassedIds contains only results meeting agreed limits and timing.
 */
export function commissionedService({pathAcceptedIds = rackRange(21, 60), responsePassedIds = rackRange(21, 40), responseCommandedIds = rackRange(21, 60), rackKW = 200, otherCriteriaMet = true} = {}) {
  if (!Number.isFinite(rackKW) || rackKW <= 0) throw new RangeError('rackKW must be positive');
  if (typeof otherCriteriaMet !== 'boolean') throw new TypeError('otherCriteriaMet must be boolean');
  const paths = rackIdSet(pathAcceptedIds, 'Accepted paths');
  const passed = rackIdSet(responsePassedIds, 'Passing measured responses');
  const commanded = rackIdSet(responseCommandedIds, 'Commanded responses');
  const positions = rackRange(1, 100).map(id => ({
    id, pathAccepted: paths.has(id), responsePassed: passed.has(id), responseCommanded: commanded.has(id),
    eligible: paths.has(id) && passed.has(id) && otherCriteriaMet,
  }));
  const eligible = positions.filter(position => position.eligible);
  return {positions, eligible, count: eligible.length, envelopeMW: eligible.length * rackKW / 1000,
    awaitingResponseAcceptance: positions.filter(position => position.responseCommanded && !position.responsePassed)};
}
