import { scenes as rackScenes, initialState as rackState } from './rack-power-scenes.js';
import { samplePresentation } from './rack-energy-800v-data.js';

const ledger = 'd06-conversion-ledger', migration = 'd06-rack-migration';
const control = (key, label, options) => ({key, label, options});
export const defaults = samplePresentation.defaults;
export const aliases = Object.freeze({...samplePresentation.aliases,'green-dc':'green-zurich-west','green-path':'green-zurich-west'});
export const initialState = Object.freeze({...rackState, auxiliaryKW:12, volts:800, cycleDegrees:30,
  voltageView:'meter', converterView:'supply', revealed:[], rackKW:120, allocationKW:240,
  deadlineWeeks:3, decision:'', migrationReveal:false});
export const learningContract = Object.freeze({
  driving_question:'Where should power conversion and stored energy connect as the rack changes?',
  fixed_boundary:'Keep each declared load and electrical boundary fixed: local rails, 100 kW conductor comparison, then the two-rack retrofit.',
  changed_variable:'Local impedance, source response, recharge interval, distribution voltage, conversion location or retrofit constraint.',
  primary_payoff:'Trace the rack-to-chip path, account for all inlet watts, and choose an architecture whose power and service interfaces can be qualified.',
  misconception:'An 800 V distribution bus powers a chip directly, fewer conductors establish total efficiency, or a sidecar increases feeder capacity.',
  closing_question:'Which retrofit can meet the service date, and what evidence must release its remaining interface holds?'
});
const supplement = [
  {id:'rack-energy-scales', label:'Where conversion belongs', title:'How do we feed the rack while keeping chip voltage steady?', reference:ledger, kind:'scales', pedagogical_role:'problem',
    explanation:['Follow three physical scales: the rack bus distributes power; board converters create the required rails; local regulators and capacitors support the devices. The generated physical context is generic, while the next manufacturer view identifies the actual DGX rack bus.','The chapter first traces the local requirements, then moves conversion outward to compare 800 V architectures and an occupied-building retrofit.'], boundary:'Rack → board → package · physical context; functional paths are drawn separately.'},
  {id:'rack-inlet-ledger',label:'Account for every inlet watt',title:'From processor power to rack input power',reference:ledger,kind:'ledger',pedagogical_role:'balance',
    controls:[control('auxiliaryKW','Other DC-bus loads',[[12,'12 kW'],[18,'18 kW']])],
    explanation:['The original reader example fixes processor rails at 72 kW, regulator efficiency at 92%, and shelf efficiency at 97%. Other loads branch directly from the shelf bus. Work backward through series converters and add parallel branches.','Increasing the other branch by 6 kW adds 6 / 0.97 = 6.186 kW at the inlet. It never passes through the processor regulators. The inlet is not the sum of processor ratings.'],boundary:'72 kW processor rails · 92% local regulation · 97% shelf efficiency · other loads at DC bus.'},
  {id:'dc-voltage-planes',label:'Separate the voltage planes',title:'Higher distribution voltage lowers current; the chip still needs local conversion.',reference:ledger,kind:'dc-planes',pedagogical_role:'comparison',
    explanation:['At 100 kW DC, a 50 V plane carries 2,000 A while an 800 V plane carries 125 A. These are two receiving-end voltage choices at equal power, not the current at each stage of a lossy real rack.','The coming AC/DC comparison asks a different question: three 480 V AC line conductors versus two 800 V DC conductors. Keep those conductor and measurement conventions explicit.'],boundary:'Same 100 kW at each declared DC plane · I = P / V · converter loss excluded from this current comparison.'},
  {id:'retrofit-power',label:'The sidecar needs upstream power',title:'Can the existing feeder supply the new DC sidecar?',reference:migration,kind:'retrofit',pedagogical_role:'counterexample',
    controls:[control('rackKW','Each of two racks',[[120,'120 kW DC'],[110,'110 kW DC']])],
    explanation:['An existing row has 240 kW allocated under the required operating state. Two 120 kW DC racks require 253 kW upstream when their shared sidecar is 96% efficient and its upstream-fed auxiliaries draw 3 kW.','At 110 kW each, the modeled input becomes 232.17 kW. That passes the supplied steady allocation, but delivered workload service, DC interfaces, protection and startup/recharge remain separate qualifications.'],boundary:'Two equal racks · 96% sidecar efficiency · 3 kW upstream auxiliaries · 240 kW existing allocation.'},
  {id:'migration-decision',label:'Choose and qualify the retrofit',title:'Choose a migration that meets both the power allocation and the service date.',reference:migration,kind:'decision',pedagogical_role:'transfer',
    controls:[control('deadlineWeeks','Service deadline',[[3,'Three weeks'],[8,'Eight weeks']])],
    explanation:['Choose a route before revealing its consequences. Existing allocation is 240 kW and a staged retrofit is ready in two weeks. A 20 kW increase takes six weeks. The customer accepts a measured lower-throughput mode temporarily. These are original classroom inputs, not an Abilene construction schedule.','For a three-week deadline, reduced demand can fit the power account and date, conditional on actual accepted service and interfaces. The full setting with the existing feeder fails power. More allocation fits full demand but misses the early date. At eight weeks the larger allocation becomes a feasible candidate.','The release evidence is a qualified 800 V converter-to-rack interface and DC protection; startup, load-step and recharge tests within the input envelope; protected cooling and network dependencies; service access and measured workload acceptance. A greenfield layout can reserve converter zones and DC paths before construction. An occupied building has retained equipment and a live service deadline.'],boundary:'Two racks · 96% sidecar · 3 kW auxiliaries · 240/260 kW allocation · 2/6-week readiness · temporary reduced service accepted.'}
];
const greenCase = {
  id:'green-zurich-west',label:'Zurich-West: DC in 2012',title:'Zurich-West moved rectification upstream in 2012.',
  reference:'d06-eight-hundred-volt-architectures',kind:'green-case',pedagogical_role:'architecture',
  boundary:'Historical Green Zurich-West expansion · 1 MW DC system · 380 V DC distribution; 400 V open-circuit in ABB’s technical text.',
  explanation:['ABB and Green opened this 1 MW DC installation in May 2012, with compatible HP servers and storage. The existing exterior photograph identifies the site; it does not depict the electrical equipment. This case is a historical 380 V deployment, separate from the later 800 V architectures.',
    'Inside the central rectifier package, a 1,100 kVA dry transformer steps down the 16 kV AC supply before rectifier modules convert AC to DC. Local DC/DC conversion still supplies the devices. The system diagram labels the distribution 380 V DC; ABB specifies 400 V open-circuit in the text. Moving rectification upstream did not remove the transformer function or the need for compatible IT inputs.'],
  source_ids:['P153','P154']
};
const reviewFigures = [
  {id:'rack-density-roadmap',label:'Rack power keeps rising',title:'Rack power keeps rising',reference:ledger,kind:'review-figure',pedagogical_role:'motivation',
    asset:'rack-density-roadmap.png',
    alt:'BofA Global Research forecast of rack power capacity, from a traditional 10–15 kW server rack toward more than 1.5 MW in the Feynman era. The supplied chart includes NVIDIA platform names, roadmap dates and an estimates attribution.',
    explanation:['This user-supplied BofA Global Research forecast motivates the physical power-delivery challenge before the chapter opens the rack. It forecasts rack capacity; it does not measure operating draw at Abilene. Keep the chart’s original estimate language and roadmap dates attached to the figure.','NVIDIA’s May 2025 technical article independently describes the transition from 54 V rack distribution toward 800 V DC for MW-scale racks. It supports the architectural motivation, not every product date or bar in this analyst chart.'],
    boundary:'Supplied BofA roadmap forecast; original report publication date not provided.',source_ids:['P05']},
  {id:'power-stack-overview',label:'The power stack, from grid to chip',title:'The power stack, from grid to chip',reference:ledger,kind:'review-figure',pedagogical_role:'recap',
    asset:'power-stack-overview.png',
    alt:'Data Gravity / Wing, May 2026 industry map: grid and substation infrastructure; data-center power distribution and UPS; rack-level power supplies; SiC and GaN power semiconductors; point-of-load and chip-level voltage regulation; ending at the NVIDIA GPU die.',
    explanation:['The supplied industry map closes the chapter by joining the grid, building, rack and chip perspectives. Follow the functions from the top to the GPU die after the class has seen the actual conversion choices and retrofit constraints.','Power semiconductors are technologies inside power converters, not necessarily a separate serial conversion stage. The chart’s companies, highlights and market metrics remain the source’s dated industry overview, not measured plant performance or a bill of materials for this course.'],
    boundary:'User-supplied industry map, labeled Data Gravity / Wing · May 2026.'}
];
const dcProtection = {
  id:'dc-feeder-protection',label:'Protect an 800 V DC feeder',title:'Interrupting a fault on an 800 V DC rack feeder',
  reference:'d06-eight-hundred-volt-architectures',kind:'dc-protection',pedagogical_role:'mechanism',
  explanation:['Once the distribution bus is 800 V DC, its feeders need protection qualified for the DC voltage and available fault current. The rectifier and charged bus capacitor can both feed a downstream short circuit; the cable also stores magnetic energy.','This diagram uses a mechanical DC breaker with an arc chamber. It must interrupt the current, withstand recovery voltage and handle energy released during clearing. Other architectures can use fuses or solid-state protection. Removing the AC supply alone does not establish that the DC circuit is de-energized.'],
  boundary:'Conceptual 800 V DC feeder: rectifier, bus capacitor, cable inductance and mechanical DC breaker.',source_ids:['E1423005C7C','P05']
};
const rack = rackScenes.map(scene=>({...scene,kind:'rack'}));
const ledgerIndex = rack.findIndex(scene => scene.id === 'board-rails');
const local = [supplement[0],reviewFigures[0],...rack.slice(0,ledgerIndex), supplement[1],...rack.slice(ledgerIndex)];
const electrical = samplePresentation.steps.map(step=>({...step,label:step.title,title:step.headline,reference:'d06-eight-hundred-volt-architectures',sourceKind:step.kind,kind:'800v'}));
// Preserve both reviewed sequences and every old scene ID in the shared selector.
const transition = electrical.flatMap(scene=>scene.id==='ocp-power-architectures'?[greenCase,scene]:[scene]);
export const scenes = Object.freeze([...local,supplement[2],...transition,dcProtection,...supplement.slice(3),reviewFigures[1]]);
