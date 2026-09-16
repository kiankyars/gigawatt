import { scenes as rackScenes, initialState as rackState } from './rack-power-scenes.js';
import { samplePresentation } from './rack-energy-800v-data.js';

const ledger = 'd06-conversion-ledger', migration = 'd06-rack-migration';
const control = (key, label, options) => ({key, label, options});
export const defaults = samplePresentation.defaults;
export const initialState = Object.freeze({...rackState, auxiliaryKW:0, volts:800, cycleDegrees:30,
  voltageView:'meter', converterView:'supply', revealed:[], rackKW:120, allocationKW:240,
  deadlineWeeks:3, decision:'', migrationReveal:false});
export const learningContract = Object.freeze({
  driving_question:'How do rack power supplies, regulators and stored energy keep chip voltage steady?',
  fixed_boundary:'Track power from the rack inlet to processor rails, then the energy exchanged at the rack DC bus.',
  changed_variable:'Local impedance, converter placement, source response or the interval between load bursts.',
  primary_payoff:'Trace the PSU-to-core path, account for inlet watts, and explain how local regulation and buffers handle changing demand.',
  misconception:'A remote power source can respond instantly, or a buffer can support repeated bursts without time and power to recharge.',
  closing_question:'Can the buffer recover before the next burst?'
});
const supplement = [
  {id:'rack-energy-scales', label:'Where conversion belongs', title:'How do we feed the rack while keeping chip voltage steady?', reference:ledger, kind:'scales', pedagogical_role:'problem',
    explanation:['Follow three physical scales: the rack bus distributes power; board converters create the required rails; local regulators and capacitors support the devices. The generated physical context is generic, while the next manufacturer view identifies the actual DGX rack bus.','Trace power from the rack supply through board-level conversion to the chip, then follow the energy buffers that respond as device demand rises and falls.'], boundary:'Rack → board → package · physical context; functional paths are drawn separately.'},
  {id:'rack-inlet-ledger',label:'Account for rack input power',title:'From processor power to rack input power',reference:ledger,kind:'review-figure',imageTitle:true,pedagogical_role:'balance',
    asset:'rack-input-power-account.png',alt:'Power flows from a 93.05 kW rack AC inlet through a 97% efficient shelf to a 90.26 kW DC bus. The bus supplies 12 kW of other loads and 78.26 kW to local regulators. At 92% efficiency, the regulators deliver 72 kW to processor rails. Regulator heat is 6.26 kW and shelf heat is 2.79 kW.',
    explanation:['The supplied rack account works backward from 72 kW at the processor rails. At 92 percent regulator efficiency, their branch needs 78.26 kW. Add 12 kW of other DC-bus loads to get 90.26 kW at the shelf output.','At 97 percent shelf efficiency, the rack inlet supplies 93.05 kW. The balance is 72 + 12 + 6.26 + 2.79 kW, with displayed quantities rounded to two decimals. The 12 kW branch is fixed, not another interactive variable.'],boundary:'72 kW processor rails + 12 kW other bus loads · 92% local regulators · 97% shelf.'},
  {id:'rack-bus-choices',label:'50 V or 800 V inside the rack',title:'Where does the rack step down from 800 V?',reference:'d06-eight-hundred-volt-architectures',kind:'dc-rack-buses',pedagogical_role:'comparison',source_ids:['P05','SA10'],
    explanation:['An 800 V input does not determine the voltage of the vertical bus inside the compute rack. One arrangement converts at the rack entrance and retains a roughly 50 V vertical bus. A second carries 800 V down the rack and places DC/DC conversion closer to the compute trays.','Both arrangements must eventually supply the low voltages required by processors. Tray and board conversion can contain several stages; neither path connects 800 V directly to the processor. The location of the first step-down determines how much of the rack carries high current at low voltage.','The two paths show architecture choices, not two simultaneous buses in every rack. The nominal low-voltage bus may be 48, 50, 51 or 54 V depending on the platform. The sidecar and upstream-power-room arrangements can use different internal rack designs.']},
  {id:'retrofit-power',label:'The sidecar needs upstream power',title:'Can the existing feeder supply the new DC sidecar?',reference:migration,kind:'retrofit',pedagogical_role:'counterexample',
    controls:[control('rackKW','Each of two racks',[[120,'120 kW DC'],[110,'110 kW DC']])],
    explanation:['An existing row has 240 kW allocated under the required operating state. Two 120 kW DC racks require 253 kW upstream when their shared sidecar is 96% efficient and its upstream-fed auxiliaries draw 3 kW.','At 110 kW each, the modeled input becomes 232.17 kW. That passes the supplied steady allocation, but delivered workload service, DC interfaces, protection and startup/recharge remain separate qualifications.'],boundary:'Two equal racks · 96% sidecar efficiency · 3 kW upstream auxiliaries · 240 kW existing allocation.'},

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
  id:'dc-feeder-protection',label:'Protect an 800 V DC feeder',title:'An 800 V DC feeder needs DC-rated protection',
  reference:'d06-eight-hundred-volt-architectures',kind:'dc-protection',pedagogical_role:'mechanism',
  explanation:['AC and DC circuits both need fault protection. In AC, natural current-zero crossings help a breaker extinguish the arc after its contacts open; current crossing zero does not itself disconnect the fault. DC has no periodic natural current zero, so its protection must force current to zero and prevent the arc from restriking.','Once the distribution bus is 800 V DC, its feeders need protection qualified for the DC voltage and available fault current. The rectifier and charged bus capacitor can both feed a downstream short circuit; the cable also stores magnetic energy.','This diagram uses a mechanical DC breaker with an arc chamber. It must interrupt the current, withstand recovery voltage and handle energy released during clearing. Other architectures can use fuses or solid-state protection. Removing the AC supply alone does not establish that the DC circuit is de-energized.'],
  boundary:'Conceptual 800 V DC feeder: rectifier, bus capacitor, cable inductance and mechanical DC breaker.',source_ids:['E1423005C7C','P05']
};
const loadDrop = {
  id:'source-ramp-down',label:'When GPU demand falls',title:'The buffer absorbs the surplus',reference:migration,
  pedagogical_role:'balance',controls:[control('response','PSU power ramp',[[0.2,'0.2 seconds'],[0.4,'0.4 seconds']])],
  explanation:['GPU demand falls by 40 kW, while the PSU shelf takes time to reduce its output. The graph shows source power above the new GPU load, not total rack power. A bidirectional buffer connected to this DC bus absorbs the difference through its controlled converter.',
    'For a linear 0.2-second ramp, the surplus is a triangle: ½ × 40 kW × 0.2 s = 4 kJ. At 0.4 seconds it is 8 kJ. The buffer needs 40 kW of initial charging power in either case, enough available energy capacity, and a response fast enough to keep bus and storage voltages within their limits. The quantities are measured at the DC-bus boundary.',
    'Capacitors absorb the immediate mismatch; a battery helps only through a converter and charging controls designed for this transient. A full or charge-limited buffer cannot absorb the assumed surplus: bus voltage rises unless the source reduces output or another engineered path takes the energy. This example does not assign these charging ratings to the Delta product on the following slide or claim this is the specific GB300 implementation.']
};
const conversionFigure = {kind:'review-figure',imageTitle:true,asset:'rack-direct-intermediate-conversion.png',
  alt:'Direct conversion connects a 51 V rack bus to a local 1 V converter. An intermediate-rail design converts 51 V to 12 V, then to 1 V beside the compute die. Both keep the final high-current path local.',
  figureCaption:'Either design can be efficient, depending on the project requirements.'};
const vrmPhaseCounts = {id:'vrm-phase-counts',label:'VRM phase counts',title:'Motherboards use different numbers of VRM phases',reference:ledger,kind:'review-figure',imageTitle:true,pedagogical_role:'example',
  asset:'vrm-phase-counts-illustrative.png',alt:'Illustrative motherboard layouts with 6, 12 and 18 independent VRM paths sharing current to the CPU. Interleaving reduces ripple; component and control quality also matter.',
  explanation:['The motherboard illustration extends the preceding four-path VRM example to larger implementations. These are converter paths feeding the processor, not the electrical phases of the facility supply.','The phase counts are illustrative layouts, not product specifications or price tiers. A motherboard’s advertised power-stage count can differ from its independently controlled phase count; controller timing and component ratings determine the actual behavior.']};
const rack = rackScenes.filter(scene=>scene.id!=='rear-busbar').flatMap(scene=>scene.id==='source-handoff'?[scene,loadDrop]:scene.id==='multiphase'?[scene,vrmPhaseCounts]:[scene]).map(scene=>({...scene,kind:scene.kind||'rack',...(scene.id==='board-rails'?conversionFigure:{})}));
const hardwareAnatomy = {id:'rack-hardware-anatomy',label:'Inside the GB300 rack',title:'Inside a GB300 compute rack',reference:ledger,kind:'hardware-anatomy',pedagogical_role:'architecture',source_ids:['P111','P64','P173'],explanation:['A GB300 NVL72 rack holds 18 compute trays. Each tray contains two Grace Blackwell Ultra superchips; each superchip pairs one Grace CPU with two Blackwell Ultra GPUs. Follow the physical nesting before following the rack power path. Recall the rear nominal 50–51 V DC bus shown in the overview; the following supply-path diagram puts that local voltage in context.','The manufacturer photographs show a Lenovo GB300 rack, an NVIDIA DGX GB300 tray and the NVIDIA superchip board. They illustrate the shared platform hierarchy; the tray photograph is not a claim about a particular Lenovo service part.']};
const ledgerIndex = rack.findIndex(scene => scene.id === 'local-current');
const local = [supplement[0],reviewFigures[0],hardwareAnatomy,...rack.slice(0,ledgerIndex), supplement[1],...rack.slice(ledgerIndex)];
const electrical = samplePresentation.steps.filter(step=>!['dc-circuit','ac-cycle','three-phase','voltage-basis'].includes(step.id)).flatMap(step=>{
  const scene={...step,label:step.title,title:step.headline,reference:'d06-eight-hundred-volt-architectures',sourceKind:step.kind,kind:'800v'};
  if(step.id==='one-load')return [{...scene,introLabel:'Power distribution',introGoal:'Comparing AC to DC in the data hall',explanation:['Keep the load at 100 kW while asking where power conversion belongs and how the distribution voltage changes conductor current.','Compare a 480 V three-phase AC feeder with an 800 V DC feeder at the same delivered power. Then follow where conversion moves and where the rack steps down to its device voltages.','Follow the resulting conversion choices from the compute rack to a sidecar and farther upstream, then check whether an existing feeder can supply a retrofit.']}];
  if(step.id==='conversion-in-sidecar')return [{...scene,label:'Conversion in a sidecar',title:'A sidecar converts AC to DC beside the compute rack.'}];
  if(step.id!=='ac-dc-ledger')return [scene];
  return [{...scene,label:'Producing the 800 V DC supply',title:'How do we produce the 800 V DC supply?',sourceKind:'conversion-supply',
    explanation:['The preceding architecture views locate AC/DC conversion in a sidecar or power room. This diagram opens that supply path: a conventional transformer first steps medium-voltage AC down to lower-voltage AC, then a controlled electronic supply rectifies and regulates it to 800 V DC.','Stepping down first lets conventional transformer equipment handle the medium-voltage insulation and isolation, while the electronic supply operates at a lower input voltage. Rectifying at medium voltage is also possible, but requires a different converter architecture and insulation, protection and control design.','The transformer changes AC voltage; it does not rectify. The controlled converter establishes the 800 V DC output. A simple unregulated rectifier fed from 480 V AC does not automatically produce this regulated output.','The voltage labels are one supply example: 13.8 kV AC to 480 V AC to 800 V DC. Other projects use different incoming and intermediate voltages. This drawing explains the equipment functions; it does not require every DC hall to follow the same topology.']}];
});
const dcPreview = {id:'dc-architecture-preview',label:'Three DC architecture views',title:'The three phases of the DC data center revolution',reference:'d06-eight-hundred-volt-architectures',kind:'dc-preview',pedagogical_role:'overview',explanation:['Preview the next three drawings from top to bottom: AC-to-DC conversion inside the compute rack, in a nearby power rack, and farther upstream. Keep the placement of conversion in view as each drawing is enlarged.','Here phases names the three architecture views in this lesson, not the three electrical phases of AC or a required deployment sequence. The conventional AC baseline is not SemiAnalysis Phase 1; the sidecar view groups that forecast’s first two adoption phases.']};
const dcChanges = {id:'dc-architecture-changes',label:'AC hall versus DC hall',title:'What changes when the hall distributes DC?',reference:'d06-eight-hundred-volt-architectures',kind:'dc-changes',pedagogical_role:'comparison',source_ids:['P05'],
  explanation:['The comparison is between conventional AC distribution to the rack and an architecture that rectifies upstream and distributes 800 V DC through the hall. A sidecar is a separate transition option: the hall remains AC-fed up to the sidecar.','The AC/DC conversion function already exists in the conventional rack supply. Moving it upstream replaces that rack function; it does not add an entirely new rectification requirement. DC-input racks still need DC/DC conversion and device regulation.','Conversion equipment moved out of compute racks frees compute-rack space but occupies space and needs cooling elsewhere. DC distribution requires appropriate DC-rated switching and protection, and backup equipment must connect through interfaces designed for the new power path. Backup is adapted rather than assumed to disappear.','Assess efficiency across the complete power path at the required load and operating mode, including conductors, converters, storage interfaces and auxiliaries. Reduced conductor heat and relocated conversion can offer benefits, but one isolated converter efficiency cannot establish the net advantage.']};
const dcSteps = Object.fromEntries([...electrical,dcPreview,supplement[2],dcChanges,greenCase,dcProtection,supplement[3],reviewFigures[1]].map(scene=>[scene.id,scene]));
export const scenes = Object.freeze(local);
export const dcScenes = Object.freeze([
  'one-load','conductor-copper','current-prediction','conductor-loss',
  'dc-architecture-preview','conversion-in-rack','conversion-in-sidecar','conversion-farther-upstream',
  'rack-bus-choices','ac-dc-ledger','dc-architecture-changes',
  'green-zurich-west','ocp-power-architectures','dc-feeder-protection','retrofit-power','power-stack-overview'
].map(id=>dcSteps[id]));
export const allScenes = Object.freeze([...scenes,...dcScenes]);
export const dcLearningContract = Object.freeze({
  driving_question:'How can 800 V DC reduce distribution copper and free compute-rack space?',
  fixed_boundary:'100 kW received by the load in each conductor comparison; a separate two-rack retrofit has a 240 kW upstream allocation.',
  changed_variable:'Distribution voltage, conductor arrangement, conversion location or rack power.',
  primary_payoff:'Distinguish conductor savings from whole-system efficiency, trace each conversion boundary, and check the power needed by a sidecar.',
  misconception:'Higher DC voltage supplies the chip directly, fewer conductors establish total efficiency, or a sidecar increases feeder capacity.',
  closing_question:'Where does conversion happen, and what power and protection does that arrangement still need?'
});
export const decks = Object.freeze({
  'rack-energy':Object.freeze({scenes,title:'Rack power and buffering',file:'rack-energy-format.html',fallbackNumber:8}),
  'dc-distribution':Object.freeze({scenes:dcScenes,title:'800 V DC distribution',file:'dc-distribution-format.html',fallbackNumber:9})
});

export function resolveRackEnergyScene(hash, deckId='rack-energy') {
  let id=String(hash||'').replace(/^#/, '');
  try { id=decodeURIComponent(id); } catch { id=''; }
  return Math.max(0,decks[deckId].scenes.findIndex(scene=>scene.id===id));
}
