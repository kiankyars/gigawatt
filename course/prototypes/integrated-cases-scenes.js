export const learningContract = Object.freeze({
  "driving_question": "What can this facility actually deliver after one condition changes?",
  "fixed_boundary": "Five supplied engineering cases, with complete electrical, heat and information paths.",
  "changed_variable": "An outage, weather, rack architecture, a network bottleneck and acceptance evidence.",
  "primary_payoff": "Compare an intervention, explain its consequence and identify the evidence needed to release service.",
  "misconception": "A component rating or installed total establishes useful service.",
  "closing_question": "Can power, heat, information and acceptance reach the same useful work?"
});

export const initialState = {acceptedRacks:600,route:'blocked',openingReveal:false};

export const scenes = [
  {
    "id": "five-decisions",
    "label": "Five connected decisions",
    "title": "What can this facility actually deliver?",
    "reference": "c01-coupled-outage",
    "case_id": null,
    "objective": "integration",
    "pedagogical_role": "problem",
    "explanation": [
      "This closing chapter assumes the preceding physical mechanisms. In five original cases, choose what changes, predict the consequence, and require evidence of useful service."
    ]
  },
  {
    "id": "outage-brief",
    "label": "1 · Coupled outage",
    "title": "The racks stay powered, but the cooling pump stops",
    "reference": "c01-coupled-outage",
    "case_id": "C01",
    "objective": "C01",
    "pedagogical_role": "problem",
    "explanation": [
      "2 MW IT survives the electrical transfer. The existing battery provides 16.2 minutes of ideal electrical duration; generator readiness is at minute ten and the planned cooling restoration sequence ends at minute twelve. The pump loses its separate utility supply. Electrical duration cannot establish how long temperatures remain acceptable without flow. The underlying example has 600 kWh usable DC, 90% discharge efficiency and a 2.5 MW inverter; controls stay powered."
    ]
  },
  {
    "id": "outage-choice",
    "label": "1 · Choose the redesign",
    "title": "More battery energy leaves the pump without power",
    "reference": "c01-coupled-outage",
    "case_id": "C01",
    "objective": "C01",
    "pedagogical_role": "transfer",
    "explanation": [
      "The three alternatives are visible together. Existing design: 16.2 minutes electrical duration and an unpowered pump. Adding 200 kWh extends duration to 21.6 minutes but leaves the pump off. Protecting the 0.2 MW cooling supply keeps the pump powered but reduces ideal duration to 14.73 minutes. All fit the 2.5 MW inverter. None establishes thermal survival without flow, temperature and service evidence."
    ]
  },
  {
    "id": "outage-evidence",
    "label": "1 · Release with evidence",
    "title": "The outage test must show that cooling and work continue",
    "reference": "c01-coupled-outage",
    "case_id": "C01",
    "objective": "C01",
    "pedagogical_role": "mechanism",
    "explanation": [
      "A project-specific integrated disturbance test must establish the auxiliary supply and observed flow, coolant and device temperatures against limits, and correct service through restoration. Define acceptance and stop criteria in advance. Thermal mass, initial conditions and control response are required; this slide is an acceptance brief, not a switching procedure."
    ]
  },
  {
    "id": "weather-brief",
    "label": "2 · Hot-weather capacity",
    "title": "Hot weather reduces the number of racks we can support",
    "reference": "c02-weather-capacity",
    "case_id": "C02",
    "objective": "C02",
    "pedagogical_role": "problem",
    "explanation": [
      "100 MW service. Mild weather: fixed 15 MW auxiliary demand and 70 MW heat removal at the IT boundary. Hot: fixed 25 MW auxiliaries and 55 MW heat removal. 900 accepted rack paths at 100 kW each. Same required IT inlet conditions; the exercise uses supplied paired operating points."
    ]
  },
  {
    "id": "weather-choice",
    "label": "2 · Choose an investment",
    "title": "Only the cooling upgrade adds rack capacity here",
    "reference": "c02-weather-capacity",
    "case_id": "C02",
    "objective": "C02",
    "pedagogical_role": "transfer",
    "explanation": [
      "Under the hot operating point, saving 10 MW of auxiliaries leaves capacity at 550 racks. Adding 10 MW of heat removal, at the supplied unchanged 25 MW auxiliaries, raises it to 650. The first can save energy; capital and operating costs are needed to compare economic value."
    ]
  },
  {
    "id": "weather-paths",
    "label": "2 · The limit moves",
    "title": "New cooling can outpace the racks ready to use it",
    "reference": "c02-weather-capacity",
    "case_id": "C02",
    "objective": "C02",
    "pedagogical_role": "mechanism",
    "explanation": [
      "Cooling is 65 MW and fixed auxiliary demand is 25 MW. With 600 complete accepted 100 kW rack paths, capacity is 60 MW. With 900 paths, cooling limits capacity to 65 MW. These paths include the required power, cooling and network services to the same racks. Actual demand is held at 58 MW in both states, so total site demand remains 83 MW. Available capacity and current demand are different quantities."
    ],
    "controls": [
      {
        "key": "acceptedRacks",
        "label": "Racks with all required services accepted",
        "options": [
          [
            600,
            "600 racks"
          ],
          [
            900,
            "900 racks"
          ]
        ]
      }
    ]
  },
  {
    "id": "density-brief",
    "label": "3 · Density retrofit",
    "title": "Both options fit the load. One blocks maintenance",
    "reference": "c03-density-retrofit",
    "case_id": "C03",
    "objective": "C03",
    "pedagogical_role": "problem",
    "explanation": [
      "Both architectures supply the same 120 kW final DC load within a 160 kW feeder limit and 140 kW whole-room cooling limit. A converts inside the rack at 96% efficiency and leaves access clear. B uses a 97% sidecar plus 98% near-load stage, and the proposed sidecar blocks the only UPS module removal route. A passes these supplied checks; B needs a layout change. Full electrical, thermal and migration acceptance is still required."
    ]
  },
  {
    "id": "density-ledger",
    "label": "3 · Close the same boundary",
    "title": "Both supply 120 kW, but their losses differ",
    "reference": "c03-density-retrofit",
    "case_id": "C03",
    "objective": "C03",
    "pedagogical_role": "mechanism",
    "explanation": [
      "A needs 125 kW AC to deliver 120 kW DC: 5 kW is conversion loss. B needs 126.24 kW AC: 6.24 kW is loss. All equipment and losses are inside the same room cooling boundary, so total room heat equals AC input in each case. The reader retains the intermediate 122.45 kW, 800 V and 153.06 A calculations. These are stipulated efficiencies, not a general ranking of architectures."
    ]
  },
  {
    "id": "density-route",
    "label": "3 · Test the revised drawing",
    "title": "Moving the sidecar clears the UPS removal route",
    "reference": "c03-density-retrofit",
    "case_id": "C03",
    "objective": "C03",
    "pedagogical_role": "transfer",
    "explanation": [
      "A revised drawing keeps the sidecar inside the same room but places it clear of the UPS replacement route. Show the actual swept removal path and preserve working clearance. B retains 126.236 kW input and room heat. Route clearance closes this specific hold; coordinated electrical, thermal and migration acceptance still applies."
    ],
    "controls": [
      {
        "key": "route",
        "label": "Sidecar position",
        "options": [
          [
            "blocked",
            "In the removal route"
          ],
          [
            "clear",
            "Moved clear"
          ]
        ]
      }
    ]
  },
  {
    "id": "job-brief",
    "label": "4 · Stalled job",
    "title": "The network adds 20 seconds to each job cycle",
    "reference": "c04-stalled-job",
    "case_id": "C04",
    "objective": "C04",
    "pedagogical_role": "problem",
    "explanation": [
      "One cycle completes fixed work in three serial phases: 60 seconds compute, 800 GB communication at 40 GB/s taking 20 seconds, and 10 seconds other work. Total: 90 seconds. Phases do not overlap. The compute-time fraction is not a measurement of output or device utilization."
    ]
  },
  {
    "id": "job-choice",
    "label": "4 · Upgrade the path",
    "title": "A faster sender leaves the network bottleneck in place",
    "reference": "c04-stalled-job",
    "case_id": "C04",
    "objective": "C04",
    "pedagogical_role": "transfer",
    "explanation": [
      "The supplied path supports 80 GB/s at sender and receiver, but 40 GB/s at the fabric bottleneck. Doubling sender capacity to 160 leaves 40 GB/s end to end. Doubling the bottleneck to 80 gives 10 seconds communication and an 80-second cycle. Rates are achieved payload-rate limits for this case, not named product ratings."
    ]
  },
  {
    "id": "job-consequence",
    "label": "4 · Predict useful progress",
    "title": "Shorter transfers allow 45 cycles per hour instead of 40",
    "reference": "c04-stalled-job",
    "case_id": "C04",
    "objective": "C04",
    "pedagogical_role": "mechanism",
    "explanation": [
      "The same correct work takes 90 seconds before the fabric upgrade and 80 seconds afterward. This is 40 versus 45 completed cycles per hour, a 12.5% throughput increase. Compute remains 60 seconds and other work remains 10; communication falls from 20 to 10. Verify achieved end-to-end payload rate and the complete application trace. A negotiated link rate alone does not establish this result."
    ]
  },
  {
    "id": "phase-brief",
    "label": "5 · Open a campus phase",
    "title": "Which part of this campus could open first?",
    "reference": "c05-open-a-phase",
    "case_id": "C05",
    "objective": "C05",
    "pedagogical_role": "problem",
    "explanation": [
      "Return to the original Crusoe-built Abilene campus as the physical setting for the handover question. Oracle captions this bundled aerial July 15 2026. No operating capacity or internal acceptance status is inferred from the image. The following 300/250/250-rack register and durations are original teaching inputs, not Abilene figures."
    ],
    "sources": [
      "https://www.oracle.com/data-centers/"
    ]
  },
  {
    "id": "phase-choice",
    "label": "5 · Choose the opening scope",
    "title": "800 racks are installed. Which group can open today?",
    "reference": "c05-open-a-phase",
    "case_id": "C05",
    "objective": "C05",
    "pedagogical_role": "transfer",
    "explanation": [
      "All three groups are visible. A has 300 accepted complete rack paths. B has 250 racks awaiting network work and acceptance. C has 250 awaiting integrated cooling acceptance. Reveal confirms A alone can open now: 30 MW at the stipulated 100 kW rack duty. Installed inventory and the 100 MW energized service do not release B or C. These are illustrative inputs, not Abilene operating data."
    ]
  },
  {
    "id": "phase-schedule",
    "label": "5 · Trace the next opening",
    "title": "A failed cooling test delays the final 250 racks",
    "reference": "c05-open-a-phase",
    "case_id": "C05",
    "objective": "C05",
    "pedagogical_role": "mechanism",
    "explanation": [
      "Both test outcomes are visible. A provides 300 racks today. B adds 250 after four days interface work and two days testing, if it passes. C adds 250 after three days delivery, one installation and three testing, if it passes on day seven. If that test fails, two days correction and three days retesting make day twelve the earliest opening, conditional on a successful retest. Preserve the accepted configuration and isolation of operating groups while work continues. All other resources are assumed available."
    ]
  },
  {
    "id": "watts-to-work",
    "label": "From watts to useful work",
    "title": "Completed work depends on the whole facility",
    "reference": "c05-open-a-phase",
    "case_id": null,
    "objective": "integration",
    "pedagogical_role": "transfer",
    "explanation": [
      "Electricity and information must reach the computing equipment, and heat must reach the outdoors. Count capacity at the accepted rack boundary and measure completed correct work at the application. The five cases show how a change in one dependency can affect that complete route."
    ]
  }
];

export const sceneAliases = {
  "outage-timeline": "outage-brief",
  "weather-demand": "weather-paths",
  "density-choice": "density-brief",
  "job-evidence": "job-consequence",
  "phase-handover": "phase-schedule"
};
