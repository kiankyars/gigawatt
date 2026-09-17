import {caseStoryScenes} from './operations-case-stories.js';
export const learningContract = Object.freeze({
  driving_question: 'The row is hot: what should we measure, change and verify?',
  fixed_boundary: 'Row B for diagnosis; separately declared loads for readiness, scheduling and maintenance.',
  changed_variable: 'Local flow, workload timing, maintenance scope and recovery path.',
  primary_payoff: 'Use local evidence to act, then prove that the required service has recovered.',
  misconception: 'Normal plant readings and duplicated equipment establish service resilience.',
  closing_question: 'Can the measured cooling path carry another 0.70 MW?'
});

export const initialState = {sharedControl:false,showDecision:false};

export const scenes = [
  {
  "id": "operations-purpose",
  "label": "Controls, operations and reliability",
  "title": "The racks are hot. The dashboard is green.",
  "reference": "d14-telemetry-and-observability",
  "objective": "D14.1",
  "pedagogical_role": "problem",
  "explanation": [
    "The opening contrasts the plant supply dashboard with a local alarm at Row B. Row B has twenty racks drawing 2.09 MW. A normal upstream temperature does not measure local coolant flow. The following before/after measurements identify a reduced-flow condition; they do not establish its cause."
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
    "Compare two stabilized operating points at the same 2.09 MW heat input, all transferred to the measured water branch. At 10:00 the row had 100 kg/s, 30°C inlet and 35°C return. At 10:10 it has 50 kg/s, 30°C inlet and 40°C return. The chip-temperature alarm arose during the transition. The timestamps belong to complete sets of row measurements, not two samples of the same temperature. The return is warmer than the supply at each point."
  ]
},
  {
  "id": "heat-balance",
  "label": "Explain the warmer return",
  "title": "Half the water flow carries the heat with twice the temperature rise.",
  "reference": "d14-telemetry-and-observability",
  "objective": "D14.1",
  "pedagogical_role": "mechanism",
  "explanation": [
    "At the same 2.09 MW heat input, Q = mass flow × water heat capacity × water temperature rise. 100 × 4.18 × 5 = 2,090 kW; 50 × 4.18 × 10 = 2,090 kW. These are two stabilized points. Do not pair old flow with new temperatures. Normal supply temperature alone does not rule out inadequate local cooling."
  ]
},
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
  ...caseStoryScenes.filter(scene=>scene.storyGroup==='google-cooling'),
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
  ...caseStoryScenes.filter(scene=>scene.storyGroup==='google-demand-response'),
  {
  "id": "deadline-scheduling",
  "label": "Defer one flexible job",
  "title": "Pause the flexible job during the grid event; finish it afterward.",
  "reference": "d14-coordinating-control-and-work",
  "objective": "D14.2",
  "pedagogical_role": "balance",
  "explanation": [
    "An illustrative checkpointable 4 MW batch job needs three running hours above a fixed 20 MW base load. A grid event lasts 14:00–16:00. Uninterrupted execution runs 13:00–16:00; pausing runs 13:00–14:00 and 16:00–18:00. Both consume 12 MWh of job energy. A 20:00 deadline allows the shift; a 17:00 deadline does not. Assume retained progress, no restart overhead and available later capacity. These numbers do not describe Google’s pilot."
  ],
  "controls": []
},
  {
  "id": "maintenance-scope",
  "label": "Maintenance and shared controls",
  "title": "Isolating one unit can also stop the units you need",
  "reference": "d14-maintenance-and-service-reliability",
  "objective": "D14.3",
  "pedagogical_role": "mechanism",
  "explanation": [
    "Original topology: 5 MW duty; two operating 3 MW units plus a third 3 MW unit under maintenance. The chosen isolation either removes only C or also a shared 24 V control supply required by A and B. We evaluate scope, not a switching procedure."
  ],
  "controls": [
    {
      "key": "sharedControl",
      "label": "Isolate",
      "options": [
        [
          false,
          "Unit C only"
        ],
        [
          true,
          "C + shared control supply"
        ]
      ]
    }
  ]
},
  ...caseStoryScenes.filter(scene=>scene.storyGroup==='cloudflare'),
  {
  "id": "replication-and-backup",
  "label": "Replicas versus backups",
  "title": "Gmail recovered from tape after a bug affected its live copies.",
  "reference": "d14-maintenance-and-service-reliability",
  "objective": "D14.4",
  "pedagogical_role": "case-study",
  "explanation": [
    "Google’s February 2011 report attributes the incident to a storage software update that affected several live data copies. It does not describe fixing copy A and then being reinfected by copy B. Multiple live copies protect against some hardware failures; an earlier offline backup preserved data through this software fault. Google stopped the rollout and reverted the software, then restored affected mail from tape."
  ],
  "sources": [
    "https://gmail.googleblog.com/2011/02/gmail-back-soon-for-everyone.html"
  ]
},
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
    "The preceding Llama 3 snapshot includes 47 planned interruptions. In a separate June 2024 engineering article, Meta describes maintenance trains: a bounded group leaves service for upgrades, then returns while the next group is serviced. This original Meta illustration depicts that rotation. Maintenance-domain sizing trades reserved capacity against training interruptions. It is a fleet-maintenance mechanism, not the measured allocation of the 54-day Llama 3 snapshot."
  ],
  "sources": [
    "https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/"
  ]
},
  {
  "id": "operating-decision",
  "label": "Knowledge check",
  "title": "Knowledge Check: Can Row B take another 0.70 MW?",
  "reference": "d14-maintenance-and-service-reliability",
  "objective": "D14.5",
  "pedagogical_role": "transfer",
  "explanation": [
    "Return to Row B at 2.09 MW. Supply is 30°C, measured flow is 50 kg/s and the allowed return is at most 40°C. All heat enters water with cp 4.18 kJ/(kg·°C); use a stabilized balance. The current water path can remove 2.09 MW at that temperature limit. A new 0.70 MW job raises duty to 2.79 MW and needs 2,790/(4.18×10) = 66.746 kg/s. At unchanged flow its required return is 43.35°C. Keep the limit by establishing at least 66.75 kg/s at the stipulated conditions, removing 0.70 MW of existing duty, or deferring the new job. This answers the stated thermal balance; the cause of the original flow reduction remains to be diagnosed."
  ]
}
];

export const sceneAliases = {
  "diagnostic-observations": "heat-balance",
  "google-verification": "google-cooling-flow",
  "control-delay": "admit-work",
  "return-to-service": "operating-decision",
  "common-cause": "maintenance-scope",
  "overlap-outages": "london-recovery",
  "causal-evidence": "operating-decision",
  "diagnosis-check": "operating-decision",
  "measurement-time": "measurement-boundaries",
  "prove-readiness": "admit-work",
  "configuration-mapping": "maintenance-scope"
};
