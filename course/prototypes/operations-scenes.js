export const learningContract = Object.freeze({
  driving_question: 'The row is hot: what should we measure, change and verify?',
  fixed_boundary: 'Row B for diagnosis; separately declared loads for readiness, scheduling and maintenance.',
  changed_variable: 'Measurement quality, workload deadline or maintenance isolation.',
  primary_payoff: 'Use local evidence to act, then prove that the required service has recovered.',
  misconception: 'A green dashboard or accepted command proves the equipment is doing its job.',
  closing_question: 'What evidence releases more work onto the hot row?'
});

export const initialState = {deadline:20,sharedControl:false,showDecision:false};

export const scenes = [
  {
    "id": "operations-purpose",
    "label": "Controls, operations and reliability",
    "title": "The racks are hot. The dashboard is green.",
    "reference": "d14-telemetry-and-observability",
    "objective": "D14.1",
    "pedagogical_role": "problem",
    "explanation": [
      "The opening alarm concerns rack row B while the reassuring value is a ten-minute-old plant supply temperature. Location and measurement time decide whether observations describe the same condition. Rack row B contains twenty racks; its current electrical heat input totals 2.09 MW."
    ]
  },
  {
    "id": "measurement-boundaries",
    "label": "Plant versus row",
    "title": "Check the row that is hot",
    "reference": "d14-telemetry-and-observability",
    "objective": "D14.1",
    "pedagogical_role": "mechanism",
    "explanation": [
      "An upstream plant temperature does not establish flow or chip temperature at Row B. Observe current row-branch flow and supply/return temperatures together with row electrical input and chip temperature. The opening alarm is local; the measurement must cover that same place."
    ]
  },
  {
    "id": "measurement-time",
    "label": "Measurement time",
    "title": "A fresh delivery can contain an old reading",
    "reference": "d14-telemetry-and-observability",
    "objective": "D14.1",
    "pedagogical_role": "mechanism",
    "explanation": [
      "At 10:10:00, the plant value was observed at 10:00:00 but delivered at 10:09:59. For this exercise the freshness requirement is at most sixty seconds. Compare with a new sample observed at 10:09:55."
    ]
  },
  {
    "id": "heat-balance",
    "label": "Cross-check the flow",
    "title": "Which flow reading matches the heat being removed?",
    "reference": "d14-telemetry-and-observability",
    "objective": "D14.1",
    "pedagogical_role": "mechanism",
    "explanation": [
      "After temperatures stabilize, Row B has 2.09 MW electrical heat input and all of this heat enters the measured water branch. Current supply and return are 30 and 40°C. The old displayed flow of 100 kg/s implies 4.18 MW; the independent current measurement of 50 kg/s implies 2.09 MW. Water specific heat is 4.18 kJ/(kg·°C). The balance supports the current flow measurement; it does not identify the cause of reduced flow."
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
  {
    "id": "google-cooling",
    "label": "Google: AI and local controls",
    "title": "Google checks AI cooling actions before applying them",
    "reference": "d14-coordinating-control-and-work",
    "objective": "D14.2",
    "pedagogical_role": "case-study",
    "explanation": [
      "Google DeepMind reported in August 2018 that its supervisory AI proposed cooling actions every five minutes. It excluded low-confidence actions and applied operator-defined constraints. Local controls checked instructions independently. Operators could leave autonomous mode for existing rules. Five minutes is the optimization cadence, not protective response latency. The real facility photo does not identify an exact campus."
    ],
    "sources": [
      "https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/"
    ]
  },
  {
    "id": "prove-readiness",
    "label": "Request, reply, physical proof",
    "title": "A start command does not prove that cooling is ready",
    "reference": "d14-coordinating-control-and-work",
    "objective": "D14.2",
    "pedagogical_role": "mechanism",
    "explanation": [
      "A request tells a standby unit to start. An acknowledgment says its controller received the command. Only fresh physical feedback showing the required flow and temperature establishes cooling readiness in this example. The three stages are visible together; they are not three alternative definitions of readiness."
    ]
  },
  {
    "id": "admit-work",
    "label": "Cooling before new work",
    "title": "Wait for cooling before adding the new workload",
    "reference": "d14-coordinating-control-and-work",
    "objective": "D14.2",
    "pedagogical_role": "mechanism",
    "explanation": [
      "The existing load produces 4 MW of heat, and cooling can remove 5 MW. New work would bring heat to 6 MW. A standby unit raises removal to 7 MW after three minutes, once physically proven ready. Starting new work immediately leaves a 1 MW heat-removal deficit during the delay; waiting holds heat at 4 MW until the 7 MW capacity is ready. Immediate admission requires a separately established transition allowance and local limits; this slide does not establish a safe delay."
    ]
  },
  {
    "id": "google-demand-response",
    "label": "Google demand response",
    "title": "Google deferred work to help the grid",
    "reference": "d14-coordinating-control-and-work",
    "objective": "D14.2",
    "pedagogical_role": "case-study",
    "explanation": [
      "Google’s October 2023 account describes a day-ahead demand-response pilot with Northern Wasco County PUD at The Dalles, Oregon. A grid event notice prompts hourly limits on non-urgent work, which can be rescheduled after the event or moved to another grid when feasible."
    ],
    "sources": [
      "https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption"
    ]
  },
  {
    "id": "deadline-scheduling",
    "label": "Shift work within its deadline",
    "title": "Both plans finish the job. Does the deadline allow the pause?",
    "reference": "d14-coordinating-control-and-work",
    "objective": "D14.2",
    "pedagogical_role": "balance",
    "explanation": [
      "A 4 MW job needs three hours of execution above a 20 MW base load, starting at 13:00. Retaining its progress across a 14:00–16:00 grid event moves completion from 16:00 to 18:00 without changing its 12 MWh of execution energy. The plan needs sufficient deadline slack and available capacity after the event."
    ],
    "controls": [
      {
        "key": "deadline",
        "label": "Deadline",
        "options": [
          [
            20,
            "20:00"
          ],
          [
            17,
            "17:00"
          ]
        ]
      }
    ]
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
  {
    "id": "configuration-mapping",
    "label": "Check the command target",
    "title": "A command to the wrong row cannot protect the hot row",
    "reference": "d14-maintenance-and-service-reliability",
    "objective": "D14.3",
    "pedagogical_role": "mechanism",
    "explanation": [
      "After a row reconfiguration, row B (B01–B20) is on branch C2; the old configuration maps C2 to row A (A01–A20). Verify as-built IDs, sensor points and action targets before restoring automatic control."
    ]
  },
  {
    "id": "cloudflare-pdx",
    "label": "Cloudflare: the missing test",
    "title": "Cloudflare had tested only part of the failed facility",
    "reference": "d14-maintenance-and-service-reliability",
    "objective": "D14.4",
    "pedagogical_role": "case-study",
    "explanation": [
      "Cloudflare’s November 2023 postmortem describes previously undiscovered facility dependencies: earlier tests at PDX-04 covered its high-availability portion, not the entire facility. The high-availability cluster spanned three sites; the other two facilities had been removed in previous tests. Edge network traffic mostly continued while dashboard, API and analytics were disrupted. This is a test-scope and service-boundary case; uncertain reconstruction of the power-failure cause is omitted."
    ],
    "sources": [
      "https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/"
    ]
  },
  {
    "id": "cloudflare-retest",
    "label": "Cloudflare: changes and retest",
    "title": "Cloudflare fixed the gaps and tested a full facility loss",
    "reference": "d14-maintenance-and-service-reliability",
    "objective": "D14.5",
    "pedagogical_role": "case-study",
    "explanation": [
      "After capacity expansion and failover changes, Cloudflare ran a facility cut test in February 2024. On March 26, a repeat facility power failure began at 14:58 UTC; APIs and dashboards operated normally by 15:05 without human intervention. Analytics recovered later that day. The seven-minute endpoint is not all-service or facility cold-start recovery."
    ],
    "sources": [
      "https://blog.cloudflare.com/major-data-center-power-failure-again-cloudflare-code-orange-tested/"
    ]
  },
  {
    "id": "replication-and-backup",
    "label": "Replicas versus backups",
    "title": "A second live copy can repeat the same mistake",
    "reference": "d14-maintenance-and-service-reliability",
    "objective": "D14.4",
    "pedagogical_role": "case-study",
    "explanation": [
      "A live replica can remain available if one device fails. A bad write or software fault can affect both live copies, so recovery also needs an earlier valid state. Gmail’s February 2011 storage software bug affected replicated copies; offline tape preserved data, and restoring it took hours. Both failure cases are shown together."
    ],
    "sources": [
      "https://gmail.googleblog.com/2011/02/gmail-back-soon-for-everyone.html"
    ]
  },
  {
    "id": "london-recovery",
    "label": "Repair versus service recovery",
    "title": "Cooling was repaired before cloud service recovered",
    "reference": "d14-maintenance-and-service-reliability",
    "objective": "D14.4",
    "pedagogical_role": "case-study",
    "explanation": [
      "Google Cloud final July 29 2022 incident summary for europe-west2: July 19 10:05 PDT servers powered down, cooling repaired at 14:13, initial cloud-service restoration milestone July 20 04:28. That is 14 hours 15 minutes after cooling repair. Residual issues lasted longer. These are reported milestones, not uniform customer downtime. The mitigation routing change initially avoided all three zones rather than only the affected zone."
    ],
    "sources": [
      "https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2"
    ]
  },
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
    "id": "operating-decision",
    "label": "Make the operating decision",
    "title": "What must be proven before more work can start?",
    "reference": "d14-maintenance-and-service-reliability",
    "objective": "D14.5",
    "pedagogical_role": "transfer",
    "explanation": [
      "The three supplied findings are unchanged row electrical input, half the branch flow and a load-reduction command aimed at the wrong row after maintenance. The cause of low flow remains unproven. Keep extra work restricted under the approved policy while the team verifies the physical cause and corrects the mapping. Release new work only after fresh local flow, temperatures and the actual response of the correct row demonstrate the required service. A configuration change or acknowledgment alone does not prove recovery."
    ]
  }
];

// Keep bookmarks useful when a standalone explanation is folded into another slide.
export const sceneAliases = {
  "diagnostic-observations": "heat-balance",
  "google-verification": "google-cooling",
  "control-delay": "admit-work",
  "return-to-service": "operating-decision",
  "common-cause": "maintenance-scope",
  "overlap-outages": "london-recovery",
  "causal-evidence": "operating-decision",
  "diagnosis-check": "operating-decision"
};
