export const learningContract = Object.freeze({
  "driving_question": "What physical place can install, operate and recover the required compute service?",
  "fixed_boundary": "Abilene and original Colossus are distinct dated cases; generic plans are explicitly original teaching diagrams. Lenovo GB300 is the named hardware service example.",
  "changed_variable": "Site exclusions, corridor rights, shared route exposure, service state, storage obstruction and common control command.",
  "primary_payoff": "Turn a supply strategy into a coordinated and maintainable site brief.",
  "misconception": "Gross acres, cabinet footprint or duplicated equipment establish a buildable and recoverable data center.",
  "closing_question": "Which physical interfaces and operating dependencies must the next design team receive with the site brief?"
});
export const initialState = Object.freeze({"land": "gross", "rights": "parcel", "crossing": "open", "fiber": "shared", "service": "installed", "route": "clear", "control": "normal"});
export const scenes = [
  {
    "id": "site-purpose",
    "label": "From land to a working facility",
    "title": "Design the site for installation, operation and recovery.",
    "pedagogical_role": "problem",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Turn the supply strategy into a physical campus. This chapter follows the parcel, the building and the equipment replacement path, then tests which shared physical and control boundaries could interrupt the service.",
      "The deliverable is a buildable site brief: land and connection rights, civil evidence, a coordinated layout, replacement routes and operating boundaries. Concept drawings show mechanisms; they are not construction documents."
    ]
  },
  {
    "id": "greenfield-brownfield",
    "label": "Two starting points",
    "title": "Abilene built a new campus; original Colossus adapted an industrial building.",
    "pedagogical_role": "comparison",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "The original Crusoe-built Abilene campus provides the greenfield reference. Original Colossus occupied the former Electrolux manufacturing facility on Paul Lowery Road in Memphis. This is industrial reuse, not an assertion that the Colossus parcel has a legal brownfield designation or known contamination.",
      "A retained shell may save building work while imposing existing geometry and structural constraints. New construction allows a coordinated arrangement but still needs site and utility infrastructure. Neither label alone proves a faster or cheaper project."
    ]
  },
  {
    "id": "colossus-service",
    "label": "What Colossus could reuse",
    "title": "Original Colossus reused the factory and mains, but still needed a new substation.",
    "pedagogical_role": "architecture",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "MLGW\u2019s historical 2025 update identifies an existing 20-inch water main and 16-inch gas main, with an 8-inch gas tap paid for by xAI. For the first 150 MW of grid service, the utility reported 8 MW through the existing substation and 142 MW through the new substation.",
      "Those are dated utility-service quantities, not a present-day IT meter reading or all sources of site power. The original Paul Lowery Road facility is distinct from the later Tulane Road / Southaven development. The case demonstrates that reuse preserves selected assets; it does not remove the remaining infrastructure work."
    ]
  },
  {
    "id": "usable-land",
    "label": "The usable campus envelope",
    "title": "A parcel\u2019s shape and reserved corridors can matter more than its total acreage.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "A conceptual parcel contains the building pad, outdoor electrical and cooling equipment, access and future construction. Drainage areas, easements and other restrictions reduce the ground available for those uses. Their overlap must be counted only once.",
      "The planning question is whether the required arrangement fits in connected usable space, with the relevant connections and access. An area total does not establish a workable geometry. This original drawing changes only the presence of documented site constraints; it is not a real parcel or a regulatory setback."
    ],
    "controls": [
      {
        "key": "land",
        "label": "Parcel view",
        "options": [
          [
            "gross",
            "Gross parcel"
          ],
          [
            "constraints",
            "Usable envelope"
          ]
        ]
      }
    ]
  },
  {
    "id": "rights-and-routes",
    "label": "Beyond the parcel boundary",
    "title": "Control of the campus parcel does not give you a route for its utilities.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "A utility lateral or fiber extension can cross separately controlled land. The connection route needs suitable construction and operating rights, as well as a service agreement and a feasible delivery plan. The two lines in the drawing describe different questions: physical route and established access.",
      "An option can preserve the choice to buy while investigations proceed, but testing access, timing and extensions depend on its terms. In Texas, surface ownership and mineral ownership can also differ. The actual title and corridor review must resolve the particular parcel; the diagram supplies no legal conclusion."
    ],
    "controls": [
      {
        "key": "rights",
        "label": "Established rights",
        "options": [
          [
            "parcel",
            "Parcel only"
          ],
          [
            "connected",
            "Parcel and corridor"
          ]
        ]
      }
    ]
  },
  {
    "id": "ground-and-foundations",
    "label": "The ground below the slab",
    "title": "The same equipment can require a different foundation on a different parcel.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Geotechnical investigation describes the soil, rock and groundwater conditions relevant to the actual structures. Compressible fill, settlement, groundwater and contamination are different findings with different design consequences. Regional soil mapping can screen questions but does not replace site-specific investigation.",
      "The cross-section is conceptual: one proposed load path meets variable ground. Boreholes represent evidence collection, not a prescribed spacing or depth. Earthwork, ground improvement or a different foundation can change cost and schedule; the engineer determines which solution fits the measured conditions."
    ]
  },
  {
    "id": "outside-flood",
    "label": "A hazard beyond the fence",
    "title": "A dry data hall can lose service when its access road or utility route floods.",
    "pedagogical_role": "counterexample",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Flood assessment must include dependencies outside the building footprint. A shared low bridge can carry the access route or multiple cable routes even when the campus is on higher ground. Local elevations, drainage, hazard maps and the actual utility routes determine exposure.",
      "This synthetic example changes a single shared crossing. It illustrates a common-cause exposure, not the flood risk of Abilene or Memphis. River flooding can isolate communities and damage roads; a dry building alone therefore does not establish continued access or service."
    ],
    "controls": [
      {
        "key": "crossing",
        "label": "Shared crossing",
        "options": [
          [
            "open",
            "Normal"
          ],
          [
            "flood",
            "Flooded"
          ]
        ]
      }
    ]
  },
  {
    "id": "fiber-diversity",
    "label": "Two contracts, one trench",
    "title": "Two fiber carriers share one failure domain when they share the same crossing.",
    "pedagogical_role": "counterexample",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Commercial diversity and physical route diversity are different. Two services can meet in a duct, bridge, building entrance or upstream facility. Confirm route records and the scope of the required independence, not just different carrier names.",
      "The changed arrangement separates the illustrated site approaches. That removes this one shared crossing from the two paths; it does not prove end-to-end network redundancy. Capacity, latency, construction rights and upstream common infrastructure still belong in the network brief."
    ],
    "controls": [
      {
        "key": "fiber",
        "label": "Fiber approach",
        "options": [
          [
            "shared",
            "Shared crossing"
          ],
          [
            "separate",
            "Separate approaches"
          ]
        ]
      }
    ]
  },
  {
    "id": "climate-and-water",
    "label": "The site sets cooling conditions",
    "title": "Water availability and hot-weather capacity must be solved with the cooling design.",
    "pedagogical_role": "comparison",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Dry heat rejection avoids an evaporative process at the depicted rejection stage, but performance depends on outdoor dry-bulb temperature and the equipment selection. Evaporative rejection can approach outdoor wet-bulb temperature while consuming makeup water and requiring water treatment and blowdown arrangements.",
      "This is the site-selection interface, not the full cooling lesson: establish the design-weather conditions, water quantity and quality, discharge obligations and the resulting supported load. A closed IT coolant loop does not by itself mean zero facility water use."
    ]
  },
  {
    "id": "neighbors-and-permits",
    "label": "The campus meets its neighbors",
    "title": "The same generation plan can need a different layout at a different site boundary.",
    "pedagogical_role": "architecture",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Outdoor heat rejection and generation introduce sound, exhaust, access and environmental interfaces. Nearby occupied property, prevailing conditions and applicable permissions can affect equipment arrangement, enclosure, treatment and operating limits.",
      "The drawing marks engineering questions rather than setback distances, permitted emission rates or a compliant design. An air permit, land-use approval and an electrical interconnection answer different questions. Their actual conditions must be reconciled in one site layout."
    ]
  },
  {
    "id": "phased-campus",
    "label": "Keep construction out of live operations",
    "title": "The second phase needs construction access that does not consume the first phase\u2019s service route.",
    "pedagogical_role": "architecture",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Phased delivery leaves an operating facility beside construction. Separate material delivery, laydown, excavation and commissioning activity from the paths the live phase depends on for staffing, maintenance and emergency response.",
      "The concept plan preserves a service route while reserving a different construction approach. This is a spatial interface for the delivery chapter to schedule and own; opening the first building does not establish that the next construction phase can use every adjacent strip of land."
    ]
  },
  {
    "id": "room-layout",
    "label": "White space and supporting rooms",
    "title": "A working hall includes the racks, support rooms and the paths between them.",
    "pedagogical_role": "architecture",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "White space houses IT equipment. Grey space includes supporting electrical and mechanical areas. The distinction describes location and use; it does not decide every cooling or power component\u2019s placement.",
      "The floor plan is a conceptual arrangement with IT rows, separate support rooms, a receiving area and a service corridor. Cabinet positions, pipe/cable routes, fire boundaries and access must be coordinated. The next scenes examine the actual equipment that must enter and be serviced."
    ]
  },
  {
    "id": "gb300-physical",
    "label": "One real rack and tray",
    "title": "Servicing a GB300 rack includes handling 29 kg compute trays.",
    "pedagogical_role": "mechanism",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Lenovo\u2019s GB300 NVL72 product guide, updated 30 August 2026, lists a 600 mm-wide MGX rack and a 29 kg compute tray. The tray is 799 mm deep including its rear water connections. These are manufacturer product quantities; they are not the complete installed rack mass or required aisle dimensions.",
      "The real rack and rear-tray images make the object and its interfaces visible. Service planning follows the tray, connections and handling equipment, not merely the exterior cabinet width. The product guide also calls for a suitable material lift for single-person service."
    ]
  },
  {
    "id": "service-envelope",
    "label": "Make room to perform the service",
    "title": "The space to withdraw a tray and position a lift is part of the equipment layout.",
    "pedagogical_role": "mechanism",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "A rack footprint does not describe the working envelope for a withdrawn tray, lift, person and tools. Lenovo\u2019s GB300 product guide explicitly discusses the Genie GL-8 or an appropriate alternative for service. Its named lift does not establish one universal aisle width.",
      "The top-view drawing is illustrative and has no prescribed clearance dimensions. Switch between installed and service states to reveal the envelope before adding permanent equipment there. Actual service documentation, handling equipment and nearby live systems establish the usable space."
    ],
    "controls": [
      {
        "key": "service",
        "label": "Rack configuration",
        "options": [
          [
            "installed",
            "Installed"
          ],
          [
            "service",
            "Tray service"
          ]
        ]
      }
    ]
  },
  {
    "id": "replacement-route",
    "label": "Follow the object out of the building",
    "title": "The replacement plan must connect the equipment position to the loading dock.",
    "pedagogical_role": "mechanism",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Follow the specified replaceable object through the complete route: withdrawal, turning and staging, doors, floor transitions and the dock. The handling assembly may be wider or heavier than the installed component. A spare does not resolve a blocked restoration route.",
      "This changed-state example blocks the only illustrated route with temporary storage. Removing that storage restores the depicted connection, without proving the dimensions or structural capacity of the route. Every interface still needs the actual equipment envelope and allowed loading."
    ],
    "controls": [
      {
        "key": "route",
        "label": "Replacement route",
        "options": [
          [
            "clear",
            "Clear"
          ],
          [
            "blocked",
            "Storage in corridor"
          ]
        ]
      }
    ]
  },
  {
    "id": "load-path",
    "label": "The floor sees the contact points",
    "title": "A floor\u2019s distributed-load rating does not establish its capacity under a moving wheel.",
    "pedagogical_role": "comparison",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "An installed cabinet transmits force through feet, rails or other supports. Moving equipment uses a different support arrangement and includes its conveyance. Average force over a cabinet footprint is therefore not the same criterion as concentrated load on a wheel or floor panel.",
      "The illustrative mass is 2,200 kg including the moving assembly, giving 21.6 kN of total static weight. Four equally loaded wheels would each carry about 5.4 kN; unequal sharing and motion can increase the maximum. The point is the changed load path, not a pass/fail threshold or structural approval."
    ]
  },
  {
    "id": "space-migration",
    "label": "Rack space and floor space",
    "title": "Moving conversion out of the rack releases mounting space while occupying space elsewhere.",
    "pedagogical_role": "comparison",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "The 800 V transition can change where conversion lives. A sidecar beside a rack can release rack mounting positions while occupying white-space floor area; conversion in a separate support room occupies grey space and changes connections.",
      "The simultaneous sketch tracks the displaced equipment across the same room boundary. To claim a smaller facility, compare complete arrangements including access, support rooms and outdoor plant. Released rack space alone is a useful but narrower result."
    ]
  },
  {
    "id": "fire-and-egress",
    "label": "Design the boundaries together",
    "title": "Fire separation, service access and escape routes must survive the equipment layout.",
    "pedagogical_role": "architecture",
    "reference": "d12-safety-and-control-boundaries",
    "explanation": [
      "Fire protection includes detection, suppression and the building features and operating responses that limit consequences. Electrical rooms, batteries and fuel equipment introduce different hazards; a single generic cabinet label does not establish an appropriate protection scheme.",
      "This conceptual plan marks separate hazard reviews and an escape route. It supplies no code clearances, ratings or suppression selection. The site\u2019s qualified designers and authority having jurisdiction reconcile the actual hazards, building use and equipment with the applicable requirements."
    ]
  },
  {
    "id": "stored-energy",
    "label": "A stopped system can retain energy",
    "title": "Opening one supply path can leave batteries, capacitors or another feed connected.",
    "pedagogical_role": "mechanism",
    "reference": "d12-safety-and-control-boundaries",
    "explanation": [
      "A command to stop equipment and an established safe energy state are different. Electrical storage, alternate feeds and pressurized systems can retain or supply energy after one upstream path is opened. Identify the relevant boundaries before designing access and service.",
      "The visual shows possible sources at a conceptual level; it is not an isolation procedure or instructions for work on energized equipment. The manufacturer and qualified site procedures determine isolation, verification and handling for the actual configuration."
    ]
  },
  {
    "id": "access-boundaries",
    "label": "People and control access",
    "title": "A service visit needs a physical route and a separate scope of control.",
    "pedagogical_role": "architecture",
    "reference": "d12-safety-and-control-boundaries",
    "explanation": [
      "Physical access can be limited to the equipment and route required for the service visit: receiving, a service corridor and the assigned rack row. An IT service role does not automatically need entry to electrical rooms or permission to operate plant controls.",
      "Remote and local control permissions are another boundary. NIST\u2019s OT guidance connects logical and physical access to the safety and availability of the process. The original access map illustrates scopes of access, not a universal staffing model or complete security architecture."
    ]
  },
  {
    "id": "control-boundaries",
    "label": "Operational technology is another boundary",
    "title": "Operational technology can give one controller authority over both cooling trains.",
    "pedagogical_role": "counterexample",
    "reference": "d12-safety-and-control-boundaries",
    "explanation": [
      "Operational technology monitors or changes physical equipment. NIST includes building automation and physical access systems within OT. Distinct pumps or cooling trains can share an administrative account, engineering workstation, network or controller.",
      "The concept diagram reveals a common control dependency, not a specific vendor flaw. Segmentation, least privilege, controlled remote access and tested local behavior address different parts of the risk. A network boundary alone cannot prove that an erroneous command will leave the required service running."
    ],
    "controls": [
      {
        "key": "control",
        "label": "Shared controller",
        "options": [
          [
            "normal",
            "Normal command"
          ],
          [
            "stop",
            "Stop both trains"
          ]
        ]
      }
    ]
  },
  {
    "id": "site-handoff",
    "label": "The site brief becomes a coordinated design",
    "title": "Hand over the site evidence, physical routes and operating boundaries as one design brief.",
    "pedagogical_role": "transfer",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Carry forward the actual land and corridor rights; verified service dates and conditions; civil, structural, flood and environmental evidence; coordinated equipment layouts; and the installed, service and replacement configurations. Link each unresolved interface to its owner and required evidence.",
      "This is the handoff into campus electrical distribution and detailed delivery work. A complete site brief enables those teams to work against the same physical constraints. It does not ask the learner to approve a site by checking a few trivial numeric thresholds."
    ]
  }
];
