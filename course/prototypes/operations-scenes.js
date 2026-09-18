import {caseStoryScenes} from './operations-case-stories.js';
import {reserveScenes} from './operations-reserve.js';
export const learningContract = Object.freeze({
  driving_question: 'The row is hot: what should we measure, change and verify?',
  fixed_boundary: 'Row B for diagnosis; separately declared loads for readiness, scheduling and maintenance.',
  changed_variable: 'Local flow, workload timing, maintenance scope and recovery path.',
  primary_payoff: 'Use local evidence to act, then prove that the required service has recovered.',
  misconception: 'Normal plant readings and duplicated equipment establish service resilience.',
  closing_question: 'Does spare plant capacity let a healthy row take another 2.50 MW?'
});

export const initialState = {showDecision:false};

export const scenes = [
  {
  "id": "operations-purpose",
  "label": "Controls, operations and reliability",
  "title": "Row B’s chips exceed 80°C despite a normal coolant supply.",
  "reference": "d14-telemetry-and-observability",
  "objective": "D14.1",
  "pedagogical_role": "problem",
  "explanation": [
    "Original teaching scenario: twenty racks draw 2.09 MW. The plant supply dashboard reads 30°C, but the hottest measured chip in Row B reaches 85°C against a stipulated 80°C operating limit. The normal upstream temperature does not establish safe chip temperature. The measured before/after points follow; chip readings and the operating limit are scenario inputs, not temperatures derived from the water heat balance or a named GPU rating."
  ]
},
  {
  "id": "measurement-boundaries",
  "label": "What changed at Row B?",
  "title": "Row B still gets 30°C water, but only half the flow.",
  "reference": "d14-telemetry-and-observability",
  "objective": "D14.1",
  "pedagogical_role": "mechanism",
  "explanation": [
    "Compare two stabilized operating points at the same 2.09 MW heat input, all transferred to the measured water branch. Before the flow drop, the row had 100 kg/s, 30°C inlet and 35°C return. At the later equilibrium, it has 50 kg/s, 30°C inlet and 40°C return. The hottest measured chip rises from 70°C to 85°C, above this scenario’s 80°C operating limit. The problem is the chip-temperature violation, not lower flow by itself. Each column is a complete set of row measurements. The return is warmer than the supply at each point. No settling duration is specified."
  ]
},
  {
  "id": "heat-balance",
  "label": "Explain the warmer return",
  "title": "Lower flow can leave chips too hot after temperatures stabilize.",
  "reference": "d14-telemetry-and-observability",
  "objective": "D14.1",
  "pedagogical_role": "mechanism",
  "explanation": [
    "Before the flow drop, the row is at equilibrium: 2.09 MW enters and 2.09 MW leaves through the measured water branch, with the hottest chip at 70°C. When flow falls from 100 to 50 kg/s, heat removal initially falls below heat input. The difference accumulates in the row, raising temperatures. A larger water temperature rise then restores heat removal to the full 2.09 MW at a hotter equilibrium, where the measured chip reaches 85°C and exceeds the scenario’s 80°C limit. The endpoint water balances are 100 × 4.18 × 5 = 2,090 kW and 50 × 4.18 × 10 = 2,090 kW. The transition is qualitative: no thermal mass or settling duration is supplied. Chip temperature is a separate measurement, not calculated from the water balance."
  ]
},
  ...caseStoryScenes.filter(scene=>scene.storyGroup==='google-cooling'),
  {
  "id": "control-layers",
  "label": "Who controls what?",
  "title": "Pump controls, plant controls and the scheduler have different jobs",
  "reference": "d14-coordinating-control-and-work",
  "objective": "D14.2",
  "pedagogical_role": "mechanism",
  "explanation": [
    "Local pump controls adjust pump speed to maintain a measured target. Plant controls start or stop cooling units and confirm their readiness. The workload scheduler decides when computing starts. These functions exchange measurements, available capacity and load requests."
  ]
},
  {
  "id": "plant-controls-focus",
  "label": "Plant controls start standby cooling",
  "title": "Plant controls bring standby cooling online.",
  "reference": "d14-coordinating-control-and-work",
  "objective": "D14.2",
  "pedagogical_role": "mechanism",
  "explanation": [
    "The highlighted plant-controls layer brings standby cooling online and confirms that it is ready. In the following example, the workload scheduler holds the new job until that cooling is available."
  ]
},
  {
  "id": "admit-work",
  "label": "A job waits for cooling",
  "title": "The new job needs cooling that takes three minutes to start.",
  "reference": "d14-coordinating-control-and-work",
  "objective": "D14.2",
  "pedagogical_role": "mechanism",
  "explanation": [
    "Existing work produces 4 MW of heat. The new job adds 2 MW. Available heat removal is 5 MW until standby cooling completes its three-minute start, then 7 MW. Compare starting the job immediately with starting at minute three. The early case accumulates 1 MW × 3/60 h = 0.05 MWh of heat above removal; no permitted thermal buffer is specified. The delay is an example, not a vendor startup specification."
  ]
},
  ...reserveScenes,
  ...caseStoryScenes.filter(scene=>scene.storyGroup==='google-demand-response'),
  {
  "id": "deadline-scheduling",
  "label": "Defer one flexible job",
  "title": "Pause the flexible job during the grid event; finish it afterward.",
  "reference": "d14-coordinating-control-and-work",
  "objective": "D14.2",
  "pedagogical_role": "balance",
  "explanation": ["An illustrative checkpointable 4 MW batch job needs three running hours above a fixed 20 MW base load. A grid event lasts 14:00–16:00. Uninterrupted execution runs 13:00–16:00; pausing runs 13:00–14:00 and 16:00–18:00. Both consume 12 MWh of job energy. A 20:00 deadline allows the shift. Assume retained progress, no restart overhead and available later capacity. These are teaching assumptions, not Google’s pilot measurements."]
},
  ...caseStoryScenes.filter(scene=>scene.storyGroup==='cloudflare'),
  ...caseStoryScenes.filter(scene=>scene.storyGroup==='london'),
  {
  "id": "llama-recovery",
  "label": "Recovery keeps training productive",
  "title": "Llama 3 kept making progress by recovering from interruptions",
  "reference": "d14-maintenance-and-service-reliability",
  "objective": "D14.4",
  "pedagogical_role": "case-study",
  "explanation": [
    "Meta reports 466 interruptions in a 54-day Llama 3 training snapshot: 47 planned and 419 unexpected. About 78% of unexpected interruptions involved confirmed or suspected hardware issues. Automation handled all but three incidents requiring significant manual intervention; reduced startup and checkpoint overhead helped keep effective training time above 90%."
  ],
  "sources": [
    "https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4"
  ]
},
  {
  "id": "llama-maintenance",
  "label": "Meta: planned maintenance",
  "title": "Meta upgrades one maintenance group at a time.",
  "reference": "d14-maintenance-and-service-reliability",
  "objective": "D14.4",
  "pedagogical_role": "case-study",
  "explanation": [
    "The preceding Llama 3 snapshot includes 47 planned interruptions. In a separate June 2024 engineering article, Meta describes maintenance trains: a bounded group leaves service for upgrades, then returns while the next group is serviced. The original Meta train illustration shows the rotation; the supplied original cost graph shows the sizing trade-off. Smaller maintenance domains cause more interruptions, while larger domains temporarily remove more compute capacity. The U-shaped curve is qualitative and does not specify a numeric optimum. It is a fleet-maintenance mechanism, not the measured allocation of the 54-day Llama 3 snapshot."
  ],
  "sources": [
    "https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/"
  ]
},
  {
  "id": "operating-decision",
  "label": "Knowledge check",
  "title": "Knowledge Check: Can Row C take another 2.50 MW?",
  "reference": "d14-maintenance-and-service-reliability",
  "objective": "D14.5",
  "pedagogical_role": "transfer",
  "explanation": [
    "New scenario: Row C is operating normally, including acceptable chip temperatures; this is not the earlier faulty Row B. The row draws 2.09 MW, all transferred to its water branch, at 100 kg/s with 30°C supply and 35°C return. A new workload adds 2.50 MW of electrical load and heat to this same branch. Electrical capacity and the cooling plant each have 3 MW spare, so neither rules out the job. The local row return must remain at or below 40°C. Its water-side heat-transfer headroom at the present flow is only 100 × 4.18 × (40−35) = 2,090 kW, or 2.09 MW. Answer: not at the current row flow. The proposed total is 4.59 MW, requiring 4,590/(4.18×10) = 109.81 kg/s, rounded up to 110 kg/s. At unchanged flow the required return would be 40.98°C. Increasing proven row flow or assigning some of the workload to another row resolves the local capacity mismatch; central spare capacity alone does not. The 110 kg/s value is a water-balance requirement, not a predicted chip temperature or an assertion that the installed pump, piping or cold plates support that flow. Their operating range and chip temperatures must be checked during a staged load increase. No equipment is already overheating in the starting state."
  ]
}
];

export const sceneAliases = {
  "cloudflare-hidden-dependency": "cloudflare-pdx",
  "replication-and-backup": "london-recovery",
  "maintenance-scope": "cloudflare-pdx",
  "diagnostic-observations": "heat-balance",
  "google-verification": "google-cooling-flow",
  "control-delay": "admit-work",
  "return-to-service": "operating-decision",
  "common-cause": "cloudflare-pdx",
  "overlap-outages": "london-recovery",
  "causal-evidence": "operating-decision",
  "diagnosis-check": "operating-decision",
  "measurement-time": "measurement-boundaries",
  "prove-readiness": "admit-work",
  "configuration-mapping": "cloudflare-pdx"
};
