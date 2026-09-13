export const initialState=Object.freeze({"genCycle": "simple", "genCampus": 0, "genStart": "hot", "genHours": 500, "genChoiceHours": 7000, "genChoiceReveal": false, "site": "A", "readinessReveal": false, "corridor": "power", "grid": "connected", "storage": "ideal", "generation": 6, "generator": "running", "island": "unsupported", "protectedLoad": 8, "fuel": "available", "route": "mv", "voltage": 34.5, "circuits": 1, "decisionReveal": false, "checkReveal": false});
export const scenes=[
  {
    "id": "siting-purpose",
    "label": "What must this site deliver?",
    "title": "Choose a site that can supply each phase on its required date.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Chapter purpose · delivery, connection, operating configuration and generation duty.",
    "explanation": [
      "This chapter connects the workload brief to physical supply: when usable capacity can arrive, which routes carry electricity and fuel, and which operating arrangement supports the load. We start with actual phased delivery before comparing grid and local generation.",
      "Then follow fuel through a gas turbine and a combined-cycle plant. Compare generation duty and procurement choices before handing a defined supply arrangement to the parcel and building design in Chapter 5."
    ]
  },
  {
    "id": "site-ready",
    "label": "CoreWeave: phased delivery",
    "title": "CoreWeave received the first 50 MW before the full 100 MW building was ready.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Applied Digital · 27 October and 24 November 2025 · Ready for Service milestones.",
    "explanation": [
      "Applied Digital reported Ready for Service for the first 50 MW at Polaris Forge 1 in Ellendale, North Dakota on October 27, 2025. On November 24 it reported the second 50 MW, completing the first 100 MW building leased to CoreWeave. The contracted campus was 400 MW; possible future expansion is a different claim.",
      "The useful lesson is to make a phase independently serviceable. Its power, cooling, network, access and testing must support that released scope while construction continues elsewhere. These releases establish delivery milestones, not measured IT draw, accepted token throughput or a quantified benefit from an invented delay scenario."
    ]
  },
  {
    "id": "parcel-connections",
    "label": "Abilene: gas has a route",
    "title": "Abilene’s on-site generation required a new gas connection.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Energy Transfer · August 2026 update · 14-mile lateral; no diameter claim.",
    "explanation": [
      "Energy Transfer’s August 2026 presentation reports completion of a second 14-mile natural-gas lateral to the Abilene data-center area. Separately, its February report says deliveries to the Oracle data center began in January. A supply strategy has become a physical connection, not just a nearby pipeline on a map.",
      "The lateral, its delivery capacity and pressure, the generation plant and their connection rights all matter. Do not infer the pipe diameter or a complete route from this account. The original Oracle campus and a separate Crusoe agreement for an adjacent development remain different records."
    ]
  },
  {
    "id": "grid-connection",
    "label": "Why loads need joint study",
    "title": "Two campuses can compete for capacity in the same upstream network.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Generated conceptual geography · ERCOT Batch Zero is a dated process example.",
    "explanation": [
      "Follow the two campus routes back to the shared substation. A connection study evaluates the upstream system that must carry their simultaneous demand, including other customers and supported contingencies. Being next to a transmission line does not reserve its spare capacity.",
      "ERCOT’s June 2026 Batch Zero announcement describes coordinated study of large loads against shared infrastructure. The illustration is a hypothetical geography, not ERCOT topology or a particular campus one-line. Study, upgrades and acceptance connect the requested service to a usable phase."
    ]
  },
  {
    "id": "abilene-phase",
    "label": "Abilene: current delivery",
    "title": "Abilene shows how a campus opens while later phases are still being built.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Oracle · status September 2026 · publisher aerial 15 July 2026.",
    "explanation": [
      "Our recurring example is the original Crusoe-built Oracle/OpenAI campus in Abilene. Oracle’s location page reports 75 percent of total capacity delivered as of September 2026, with the remainder in subsequent quarters. Its displayed aerial photograph is dated July 15, 2026.",
      "Use the current delivery statement for current status. The page does not give a denominator that licenses turning 75 percent into a new megawatt count, nor does delivered capacity establish metered IT power or useful output. The adjacent Microsoft campus is a separate project. No September satellite capture was established."
    ]
  },
  {
    "id": "power-configurations",
    "label": "Four operating arrangements",
    "title": "Distinguish grid imports, local supply and an electrical island.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Original four-configuration teaching figure · normal operation; backup omitted.",
    "explanation": [
      "These four simplified arrangements organize the next four slides. Grid-supplied uses utility delivery for normal demand. Grid-parallel combines local generation with permitted imports. Export-only supplies the site locally while permitting surplus export but no imports to serve the load. Off-grid has no operating grid tie.",
      "The directions describe the permitted supply relationship, not installation wiring or an exhaustive industry taxonomy. Export-only remains electrically grid-connected. Backup, storage, auxiliary and protection details are omitted here and must be specified separately."
    ]
  },
  {
    "id": "config-grid-supplied",
    "label": "1 · Grid-supplied",
    "title": "Grid-supplied operation depends on a physical utility connection.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Normal utility supply · backup omitted from this overview.",
    "explanation": [
      "Normal electrical demand comes through the utility connection. An off-site energy contract can address price or sourcing, but it does not add an independent feeder. Start with the actual point of delivery and the service it can support.",
      "Backup generation and UPS arrangements are separate parts of the continuity design. A purchase agreement or a claim of annual clean-energy matching does not establish outage support. This configuration does not mean that backup equipment is absent."
    ]
  },
  {
    "id": "config-grid-parallel",
    "label": "2 · Grid-parallel",
    "title": "Grid-parallel generation changes imports without disconnecting the site.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Connected operation · import and export rights are site-specific.",
    "explanation": [
      "The grid and local plant share the task of supplying the customer load. The meter records net exchange; zero imports at one moment need not mean the breaker is open. If local generation stops, the required import can rise sharply.",
      "The reserved import capacity and supported fallback matter as much as the normal energy balance. Export requires the relevant agreement and equipment capability. A behind-the-meter location alone does not establish permission to export or ability to island."
    ]
  },
  {
    "id": "config-export-only",
    "label": "3 · Export-only",
    "title": "An export-only site is grid-connected without imports available to serve its load.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "No grid imports to serve load · permitted surplus export · not an electrical island.",
    "explanation": [
      "Local generation serves the data center and may export the surplus through the allowed grid connection. The no-import constraint concerns supply rights or configuration, not the absence of an electrical tie.",
      "Grid disturbance behavior still needs a protection and operating design. The plant may need to disconnect; surviving as an island requires established controls and capacity. Neither export permission nor netting of flows creates backup import rights."
    ]
  },
  {
    "id": "config-off-grid",
    "label": "4 · Off-grid",
    "title": "Off-grid operation must balance the full load with local resources.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Isolated operation · local generation and balancing must both be established.",
    "explanation": [
      "There is no operating grid tie to absorb a deficit or surplus. The local system must establish voltage and frequency, support the full continuing load and remain within its fuel, storage, thermal and equipment limits.",
      "Generation can provide sustained energy while a suitably connected buffer responds to a fast mismatch. Battery discharge power and usable energy are separate limits. We are not assuming a solar plant, night-time operation, or a particular transfer time. The detailed storage lesson develops that response."
    ]
  },
  {
    "id": "bridge-to-backup",
    "label": "Bridge power becomes backup",
    "title": "Crusoe uses gas turbines as bridge power and long-term backup.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Crusoe impact report · May 2026 · strategy, not a universal automatic conversion.",
    "explanation": [
      "Crusoe’s 2025 impact report, published May 2026, describes natural-gas turbines as temporary bridge power and replacement for diesel backup. The strategy can let a campus operate before permanent grid delivery is available, then retain the plant for backup duty.",
      "The change of role is engineered, not automatic. The later arrangement must meet its starting, transfer, protection, redundancy, fuel, maintenance and operating-permission requirements. A prime-power rating alone does not establish successful backup performance."
    ]
  },
  {
    "id": "generation-options",
    "label": "Simple cycle versus combined cycle",
    "title": "A combined-cycle plant adds a steam cycle to a gas turbine.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Gas-turbine cycle and combined gas/steam cycle · OEM diagrams follow.",
    "explanation": [
      "A simple-cycle gas turbine compresses air, burns fuel and expands the hot gas to produce shaft work. Exhaust then leaves the cycle. A combined-cycle plant sends that exhaust through a heat-recovery steam generator to supply an additional steam turbine.",
      "The additional steam system can increase electrical output from a given fuel input, but adds equipment, cooling and operating constraints. First follow each mechanism in the manufacturer drawings; then compare the service the plant must provide. Simple cycle is the term, rather than single-cycle combined cycle."
    ]
  },
  {
    "id": "gas-shaft",
    "label": "What turns the generator?",
    "title": "How does a simple-cycle gas turbine drive its generator?",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Conceptual open-cycle gas turbine · steady operation, after startup.",
    "explanation": [
      "Air enters a compressor, fuel burns in the compressed air, and the hot gas expands through turbine blades. The turbine supplies shaft work to both the compressor and the electric generator. This gas-turbine process is modeled by the Brayton cycle. A starter may initially turn the shaft; a continuously powered electric motor is not the fuel-to-electricity mechanism.",
      "Open cycle, or simple-cycle gas turbine, describes the gas leaving through the exhaust without a second steam power cycle. Peaking is an operating role. Gas turbines can do other jobs, and peaking power can also come from engines, storage or other resources."
    ]
  },
  {
    "id": "combined-cycle",
    "label": "Recover the exhaust heat",
    "title": "How does a combined-cycle gas turbine plant work?",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Siemens Energy original principle diagram · its 64% label is the vendor example, not a universal efficiency.",
    "explanation": [
      "A heat recovery steam generator, or HRSG, transfers heat from the gas-turbine exhaust into a separate pressurized water/steam circuit. Steam expands through a steam turbine, which drives a generator. A condenser removes remaining heat and returns steam to liquid; a pump returns that water to the HRSG. This steam power loop is modeled by the Rankine cycle.",
      "The exhaust gas does not become the steam. Combining the gas and steam cycles recovers energy that a simple-cycle plant would otherwise reject. It also adds the HRSG, steam turbine, condenser, cooling and water systems. Those additions affect capital, space, construction, maintenance and startup requirements. The combined-cycle plant still rejects heat."
    ]
  },
  {
    "id": "dania-cycle",
    "label": "See the actual plant",
    "title": "Dania Beach’s combined cycle includes two gas turbines.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "GE Vernova’s Dania Beach case · reported plant output up to 1,260 MW · source reviewed 12 September 2026.",
    "explanation": [
      "The manufacturer’s photograph places this mechanism in a real utility plant: FPL’s Dania Beach Clean Energy Center near Fort Lauderdale. GE Vernova reports two 7HA.03 gas turbines and plant output up to 1,260 MW. That number describes the reported plant, not two standalone turbine nameplates added together.",
      "This is a grid-generation example, not an asserted supply contract or electrical connection to our course campus. Do not infer this site’s instantaneous output, operating efficiency or allocation to data centers from its published capacity."
    ]
  },
  {
    "id": "grid-dispatch",
    "label": "Supply each hour",
    "title": "Peaking plants cover the residual load left by the rest of the grid.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Siemens Energy illustrative dispatch profiles · no measured hourly forecast.",
    "explanation": [
      "Baseload is the demand floor; mid-merit and peaking describe operating duties above that floor. The Siemens diagram contrasts conventional dispatch with a system containing more variable renewable output. The residual load, not the gross daily demand alone, determines which flexible resources must run.",
      "Simple-cycle gas turbines can be valuable when short operating intervals, rapid response and lower installed complexity dominate fuel efficiency. Combined-cycle plants can also follow load. Unit commitment, startup, minimum output, reserves, fuel and network constraints shape actual dispatch. These illustrative curves are not a prediction for a named grid."
    ]
  },
  {
    "id": "generation-flexibility",
    "label": "Combined cycle can follow load",
    "title": "A hot-start rating does not tell you the cold-start time.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "GE 7HA.03, 1×1 combined-cycle catalog · May 2025 · net plant, ISO conditions, natural gas.",
    "controls": [
      {
        "key": "genStart",
        "label": "Initial condition",
        "options": [
          [
            "hot",
            "Hot plant"
          ],
          [
            "cold",
            "Cold plant"
          ]
        ]
      }
    ],
    "explanation": [
      "The May 2025 GE Vernova fact sheet lists a 7HA.03 1×1 combined-cycle plant at 640 MW net, with a rapid-response hot start below 30 minutes, a 75 MW/minute ramp rate and a 26% minimum-load entry. These are separate catalog characteristics; the hot-start number cannot be reused for a cold plant, and the ramp rate is not a promise of instantaneous service from zero.",
      "Combined cycle can follow load and serve intermediate duty. Simple cycle often has a simpler installation and can suit short-notice operation, but startup depends on the actual machine and thermal state. Building a plant, starting an available plant and changing its running output are three different clocks. Equipment procurement, permits, fuel supply and civil work can dominate either construction schedule."
    ]
  },
  {
    "id": "generation-utilization",
    "label": "When does efficiency repay?",
    "title": "More running hours can repay the extra steam-cycle equipment.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Hypothetical 100 MW options · annualized fixed cost $8M / $16M · fuel $20/MWh thermal, LHV.",
    "controls": [
      {
        "key": "genHours",
        "label": "Equivalent full-load hours per year",
        "options": [
          [
            500,
            "500 h"
          ],
          [
            4800,
            "4,800 h"
          ],
          [
            7000,
            "7,000 h"
          ]
        ]
      }
    ],
    "explanation": [
      "This separate hypothetical comparison assumes efficiencies of 40% for simple cycle and 60% for combined cycle, with annualized fixed costs of $8 million and $16 million respectively. At a fuel price of $20 per MWh thermal on the same LHV basis, variable fuel costs are $50 and $33.33 per MWh electric. Equal output capability does not imply equal annual cost.",
      "At 500 equivalent full-load hours, simple cycle costs $10.5 million against $17.67 million. At 7,000 hours, combined cycle costs $39.33 million against $43 million. The crossover is 4,800 hours in this model. These are original assumptions, not market quotations or an investment recommendation. Start costs, variable maintenance, emissions costs, part-load efficiency, downtime and project-specific financing are excluded."
    ]
  },
  {
    "id": "procurement-route",
    "label": "Southaven procurement",
    "title": "Equipment lead times can change the power route.",
    "reference": "../index.html#d03-voltage-and-distance",
    "boundary": "SemiAnalysis · 7 August 2026 · reported Southaven/MiniHard context, conceptual paths.",
    "controls": [
      {
        "key": "route",
        "label": "Conceptual delivery route",
        "options": [
          [
            "hv",
            "Step up, then down"
          ],
          [
            "mv",
            "Local medium voltage"
          ]
        ]
      }
    ],
    "explanation": [
      "SemiAnalysis’s construction analysis describes imported power modules and medium-voltage delivery from generation to low-voltage transformers as a way to bypass long-lead switchgear and large power transformers in the Southaven/MiniHard buildout discussion. This is the reported procurement rationale.",
      "The drawing compares conceptual paths. It is not an as-built one-line, an assertion about every circuit at Colossus, or evidence that all transformers and switchgear disappear. Next, isolate the current cost of choosing a lower transport voltage at the same power."
    ]
  },
  {
    "id": "transport-current",
    "label": "Voltage and current",
    "title": "Lower transport voltage requires more current for the same power.",
    "reference": "../index.html#d03-voltage-and-distance",
    "boundary": "Hypothetical 200 MW receiving boundary · balanced three-phase · line-to-line RMS voltage · PF = 1.",
    "controls": [
      {
        "key": "voltage",
        "label": "Transport voltage",
        "options": [
          [
            34.5,
            "34.5 kV"
          ],
          [
            161,
            "161 kV"
          ]
        ]
      }
    ],
    "explanation": [
      "Using I = P / (√3 × VLL × PF), 200 MW corresponds to about 3.35 kA at 34.5 kV and 717 A at 161 kV. The current ratio is about 4.67. Power at the receiving boundary remains fixed.",
      "These numerical voltages and load are original comparison inputs, not Southaven site specifications. Current is per line, or an equivalent aggregate before circuit splitting, not the sum of three conductor magnitudes. Equipment ratings, circuit count and losses remain separate design questions."
    ]
  },
  {
    "id": "parallel-circuits",
    "label": "Divide the transfer",
    "title": "Parallel circuits spread the current across more conductors.",
    "reference": "../index.html#d03-voltage-and-distance",
    "boundary": "Hypothetical 200 MW at 34.5 kV · equal sharing · each circuit has three phase conductors.",
    "controls": [
      {
        "key": "circuits",
        "label": "Complete three-phase circuits",
        "options": [
          [
            1,
            "One"
          ],
          [
            2,
            "Two"
          ],
          [
            4,
            "Four"
          ]
        ]
      }
    ],
    "explanation": [
      "Dividing the same transfer equally across more complete circuits lowers current per circuit, while increasing the number of phase conductor paths. Four equal circuits each carry about 837 A per line in this model. Actual sharing depends on the engineered arrangement.",
      "At unchanged resistance per conductor, total conductor heating follows 3 × n × (Iaggregate/n)² × R. This isolated result excludes reactive, thermal, protection and conversion behavior; it neither specifies conductor sizing nor estimates real site losses."
    ]
  },
  {
    "id": "procurement-decision",
    "label": "Choose the tradeoff",
    "title": "Earlier equipment must still meet the electrical requirement.",
    "reference": "../index.html#d03-voltage-and-distance",
    "boundary": "Reported procurement rationale paired with bounded teaching models.",
    "reveal": "decisionReveal",
    "explanation": [
      "Before revealing, name one delivery dependency the alternative can avoid and one electrical consequence that still has to be resolved. Lower voltage increases required current at fixed transfer; more circuits or conductor area can change the outcome.",
      "A proposal earns earlier useful work only if the equipment, protection, physical routes and commissioned service actually meet the load requirement. The 4.67 current ratio is not a site efficiency prediction, and supplier availability alone is not a finished campus."
    ]
  },
  {
    "id": "supply-brief",
    "label": "Next: build the site",
    "title": "Carry the supply arrangement into the physical site design.",
    "reference": "../index.html#d03-service-and-siting",
    "boundary": "Supply-to-site handoff · no threshold quiz.",
    "explanation": [
      "Carry the accepted delivery phase, electrical connection, fuel route and supported normal and failure states into Chapter 5. They determine what must fit on the parcel, which access and utility rights are needed and what must remain maintainable.",
      "The next chapter evaluates usable land, retained structures, equipment space, replacement routes and physical failure domains. A released phase must be usable and supportable while the rest of the campus changes."
    ]
  }
];
export const legacySceneAliases=Object.freeze({
  "purchased-energy": "config-grid-supplied",
  "hourly-match": "config-off-grid",
  "storage-match": "config-off-grid",
  "btm-import": "config-grid-parallel",
  "import-contingency": "config-grid-parallel",
  "island-boundary": "config-off-grid",
  "island-duration": "config-off-grid",
  "fuel-delivery": "parcel-connections",
  "generation-fuel": "combined-cycle",
  "generation-choice": "generation-utilization",
  "phase-check": "supply-brief"
});
