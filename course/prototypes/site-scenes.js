export const learningContract = Object.freeze({
  "driving_question": "What physical place can install, operate and recover the required compute service?",
  "fixed_boundary": "Abilene and Colossus 1 are distinct dated cases; generic plans are explicitly original teaching diagrams. Lenovo GB300 is the named hardware service example.",
  "changed_variable": "Physical arrangements and the service boundary for a power module versus a compute tray.",
  "primary_payoff": "Turn a supply strategy into a coordinated and maintainable site brief.",
  "misconception": "Gross acres, cabinet footprint or duplicated equipment establish a buildable and recoverable data center.",
  "closing_question": "What must be verified to replace a component while preserving the rest of the service?"
});
export const initialState = Object.freeze({ serviceAnswer: "hidden" });
export const scenes = [
  {
    "id": "site-purpose",
    "label": "From parcel to rack",
    "title": "Turn a parcel into a place you can build, operate and repair.",
    "pedagogical_role": "problem",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Turn the supply strategy into a physical campus. This chapter follows the parcel, the building and the equipment replacement path, then tests which shared physical and control boundaries could interrupt the service.",
      "The deliverable is a buildable site brief: land and connection rights, civil evidence, a coordinated layout, replacement routes and operating boundaries. Concept drawings show mechanisms; they are not construction documents."
    ]
  },
  {
    "id": "greenfield-brownfield",
    "label": "Abilene and Colossus 1",
    "title": "Abilene built a new campus; Colossus 1 reused a factory.",
    "pedagogical_role": "comparison",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "The original Crusoe-built Abilene campus provides the greenfield reference. Colossus 1 occupied the former Electrolux manufacturing facility on Paul Lowery Road in Memphis. This is industrial reuse, not an assertion that the Colossus parcel has a legal brownfield designation or known contamination.",
      "A retained shell may save building work while imposing existing geometry and structural constraints. New construction allows a coordinated arrangement but still needs site and utility infrastructure. Neither label alone proves a faster or cheaper project."
    ]
  },
  {
    "id": "colossus-service",
    "label": "What the factory could reuse",
    "title": "Colossus 1 inherited utility mains, but needed more grid capacity.",
    "pedagogical_role": "architecture",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "MLGW’s historical 2025 update identifies an existing 20-inch water main and 16-inch gas main, with an 8-inch gas tap paid for by xAI. For the first 150 MW of grid service, the utility reported 8 MW through the existing substation and 142 MW through the new substation.",
      "Those are dated utility-service quantities, not a present-day IT meter reading or all sources of site power. The original Paul Lowery Road facility is distinct from the later Tulane Road / Southaven development. The case demonstrates that reuse preserves selected assets; it does not remove the remaining infrastructure work."
    ]
  },
  {
    "id": "usable-land",
    "label": "Fit the whole campus",
    "title": "Utility corridors and drainage shape the space available to build.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "A conceptual parcel contains the building pad, outdoor electrical and cooling equipment, access and future construction. Drainage areas, easements and other restrictions reduce the ground available for those uses. Their overlap must be counted only once.",
      "The planning question is whether the required arrangement fits in connected usable space, with the relevant connections and access. An area total does not establish a workable geometry. This original drawing changes only the presence of documented site constraints; it is not a real parcel or a regulatory setback."
    ]
  },
  {
    "id": "rights-and-routes",
    "label": "Texas: surface and mineral rights",
    "title": "Buying Texas land may leave mineral rights with another owner.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Texas recognizes separate surface and mineral estates. A surface purchase can therefore leave the minerals with another owner. The Railroad Commission explains that the mineral estate is generally dominant: reasonably necessary use of the surface can include roads, wells and pipelines. Deeds, leases, ordinances and the accommodation doctrine can limit that use.",
      "The required outcome is enforceable rights compatible with the campus, not necessarily ownership of every mineral interest. Relevant mineral owners and existing lessees may agree to surface restrictions or waivers, or agreed drilling and access areas can shape the layout. Purchasing minerals does not automatically rewrite an existing lease. Title investigation must identify the parties whose rights actually affect the site."
    ]
  },
  {
    "id": "mineral-project",
    "label": "TCDC: land secured, waiver pending",
    "title": "A land purchase does not settle an operator’s surface rights.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "New Era’s August 14, 2026 issuer update said all 493 acres for Texas Critical Data Centers near Odessa had been secured, with one final surface waiver pending from a leasehold operator. It also reported removal of 22 abandoned pipelines across 12 rights-of-way. These are distinct site-development milestones.",
      "The release establishes an outstanding agreement, not a quantified mineral-caused delay. Another actual contract, Fermi’s May 2025 Project Matador ground lease, made a surface waiver a commencement condition unless the tenant waived it. Its later filing reports commencement in September 2025 after conditions were satisfied or waived. Agreements can resolve surface use without buying every mineral interest."
    ]
  },
  {
    "id": "mineral-accommodation",
    "label": "Getty v. Jones: conflicting surface uses",
    "title": "An oil well and an irrigation system needed the same space.",
    "pedagogical_role": "case-study",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "In Getty Oil v. Jones (Texas Supreme Court, 1971), an established irrigation system needed seven feet of clearance while Getty’s pumpjacks reached 17 and 34 feet. Other operators showed lower-profile or recessed alternatives. The court held that reasonable mineral use can require accommodating an existing surface use where reasonable mineral-development alternatives are available and the surface owner has no reasonable alternative for continuing that existing use.",
      "The court affirmed a remand; this was not a universal order to bury equipment. It is a farming judgment, not a data-center lawsuit. Its lesson for a proposed campus is that dominance of the mineral estate has limits, but a fact-dependent doctrine does not pre-approve a new building layout. Resolve express deeds, leases and surface agreements before relying on litigation."
    ]
  },
  {
    "id": "ground-and-foundations",
    "label": "ADA Docklands: building on fill",
    "title": "At ADA’s London site, the buildings and utilities needed different support.",
    "pedagogical_role": "case-study",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Menard’s account of ADA Infrastructure’s London Docklands campus identifies up to six metres of fill above soft alluvium, plus buried foundations, tanks and timber piles. Continuous-flight-auger (CFA) piles support the buildings. About 7,000 Bi-Modulus ground-improvement columns treated 40,000 square metres of external areas and utility infrastructure.",
      "The upper stone sections of those columns could clash with utilities, so utility invert levels had to be coordinated with the treatment. Remediation also affected the work sequence. The actual site photograph shows drilling rigs. The case links ground evidence to the buildings, external utility routes and construction sequence; the 7,000 columns are not the building piles."
    ]
  },
  {
    "id": "outside-flood",
    "label": "Equinix HO1 during Harvey",
    "title": "Equinix stayed online while flooding blocked customer access.",
    "pedagogical_role": "case-study",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "On August 28, 2017, Equinix told Data Center Knowledge that HO1 in Houston remained staffed and operating without interruption, while flooding had closed surrounding streets and made the site inaccessible to customers. That is a documented offsite-access consequence, without inventing a bridge failure.",
      "Equinix’s subsequent employee account describes water entering its Houston data center and staff staying for days, pumping it out while maintaining power. Continued IT service therefore depended on people already on site as well as equipment. This is not a dry-campus story, and no unrelated Houston flood photograph is presented as the HO1 access route."
    ]
  },
  {
    "id": "qts-suwanee",
    "label": "Meet QTS Suwanee",
    "title": "QTS Suwanee houses customers’ equipment north of Atlanta.",
    "pedagogical_role": "case-study",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "QTS operates a 53-acre colocation campus in Suwanee, Georgia. Its two data-center buildings are at 300 and 120 Satellite Boulevard NW. The visual uses the operator’s actual campus plan. Customers place IT equipment in such facilities and connect it to their networks through physical fiber routes.",
      "QTS’s January 2023 article described diverse campus fiber entrances and separately proposed four entrances for DC2. Its current campus page describes redundant campus conduits as in progress. These are dated statements with different scopes, so the following teaching sketches do not certify completion of the whole campus conduit system."
    ]
  },
  {
    "id": "fiber-diversity",
    "label": "Independent fiber approaches",
    "title": "Separate fiber entrances remove a shared point of failure.",
    "pedagogical_role": "counterexample",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "QTS’s January 2023 Suwanee article describes diverse fiber entrances and separately proposes four entrances for DC2. Its current page still describes redundant campus conduits as in progress. Entrance separation is the design mechanism taught here; no undisclosed QTS route plan or completed end-to-end redundancy is asserted.",
      "The paired route sketches are illustrative, not a map of QTS. One illustrates two cables sharing an entrance, while the other has separate approaches. Separation removes the pictured shared exposure; it does not prove end-to-end independence. Circuits may still meet in an upstream bridge, duct or facility. Zayo’s March 2026 announcement of four diverse routes under construction for QTS Cambois is an additional AI-campus example."
    ]
  },
  {
    "id": "climate-and-water",
    "label": "Two AI cooling designs",
    "title": "Abilene rejects heat without evaporation; Colossus 1 also uses cooling towers.",
    "pedagogical_role": "comparison",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Crusoe describes Abilene’s outdoor heat rejection as non-evaporative air-cooled chillers. This is a named AI-factory example, not a claim that all Texas facilities must use dry cooling or that Abilene relies only on passive dry coolers. Its liquid loops carry heat inside the system without establishing an evaporative process outdoors.",
      "Colossus 1 provides the comparison: TDEC identifies xAI Colossus as a user of evaporative cooling in its 2025 reclaimed-water proposal. FAS’s original May 2026 imagery analysis identifies both cooling towers and air-cooled chillers. The proposal does not prove the reclaimed-water plant is operational. Dry rejection depends on outdoor dry-bulb temperature; evaporative rejection uses the wet-bulb boundary and consumes makeup water. Actual equipment capacity remains conditional on its rated operating conditions."
    ]
  },
  {
    "id": "neighbors-and-permits",
    "label": "Rogers Toronto: screen the chillers",
    "title": "Rogers screened its rooftop chillers from neighboring homes.",
    "pedagogical_role": "case-study",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Parklane’s account of the Rogers headquarters data-center retrofit in Toronto describes rooftop chillers opposite residences and a 15-foot acoustic screen. Sixteen factory-built wall sections were installed in one ten-hour day. With little staging space, the sections were lifted from delivery trucks onto precisely positioned columns.",
      "The photograph shows the actual screen. A barrier interrupts direct sound propagation, while sound can still diffract around its edges; height, placement and construction matter. The open top must also support the chillers’ airflow. Parklane reports meeting the noise requirements, but no measured decibel reduction is supplied here."
    ]
  },
  {
    "id": "gb300-physical",
    "label": "The rack and its serviceable parts",
    "title": "Moving a rack and replacing a tray require separate handling plans.",
    "pedagogical_role": "mechanism",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Lenovo’s GB300 NVL72 mechanical specification lists the complete rack solution at approximately 1,580 kg, depending on configuration. This is distinct from an empty rack frame. Its August 30, 2026 product guide lists the compute tray at 29 kg; both images show actual Lenovo products.",
      "The manufacturer mass informs the handling and structural design, but it is not a caster-load or floor-pressure rating. Loads pass through the actual feet, casters and handling equipment. Lenovo calls for a suitable material lift for single-person compute-tray service. Those interfaces motivate the following service and replacement scenes."
    ]
  },
  {
    "id": "service-envelope",
    "label": "Withdraw and support the tray",
    "title": "Reserve space for the tray, lift and technician.",
    "pedagogical_role": "mechanism",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "The previous slide identified the Lenovo GB300 rack and its 29 kg compute tray. Now follow the service movement: support the tray at working height and leave room for the handling equipment and technician. Lenovo’s product guide identifies a Genie GL-8 or appropriate alternative for single-person service. The space reserved for this work is larger than the installed rack footprint.",
      "The generated illustration depicts that physical relationship, not the exact anatomy or approved removal procedure of a Lenovo tray or Genie lift. Actual service instructions determine the supported handling method, required disconnections and clearances. A service envelope belongs in the layout before adjacent equipment is fixed in place."
    ]
  },
  {
    "id": "hot-swap",
    "label": "Replace a module while the rack runs",
    "title": "Hot-swap power modules can keep the rest of the rack running.",
    "pedagogical_role": "mechanism",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Lenovo’s GB300 NVL72 power shelf contains six 5.5 kW hot-swappable power-supply modules. Hot-swappable means a designated component can be replaced while the containing system remains energized and operating, subject to the supported configuration and service procedure. The remaining qualified power supplies must be able to carry the load during replacement.",
      "A field-replaceable unit is not automatically hot-swappable. Lenovo’s compute-tray removal instructions require that tray to be powered off and disconnected before removal. Its workload must stop or move; that does not itself require shutting down every rack component. Both jobs still need physical access and an appropriate service envelope."
    ]
  },
  {
    "id": "replacement-route",
    "label": "Fit the equipment around the turn",
    "title": "The replacement route must fit the equipment through every turn.",
    "pedagogical_role": "mechanism",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Continue the same equipment movement from its working position toward receiving. A door can be wide enough for straight passage while the approach leaves insufficient room to turn the supported assembly. The complete handling envelope includes the equipment and its conveyance; the route therefore needs a swept-path check, not just the width of each opening.",
      "The plan is an original geometric teaching illustration, not the layout of either named campus. The amber region marks the turn that needs dimensional verification. Equipment size, permitted orientation, door openings, floor transitions and loading conditions determine the actual route. There is no arbitrary corridor-width rule or invented pass/fail dimension."
    ]
  },
  {
    "id": "load-path",
    "label": "Trace the load into the floor",
    "title": "A floor must support concentrated loads wherever equipment travels.",
    "pedagogical_role": "comparison",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Lenovo lists approximately 1,580 kg for its complete GB300 rack solution, depending on configuration. That mass is not a floor-pressure specification. Installed feet or rails and the contacts of a moving handling assembly transfer forces into a slab, panel or other floor structure in different ways.",
      "The visual compares those contact patterns without assuming that rack transport is permitted on a particular trolley or that four wheels share load equally. A structural check follows the actual equipment and handling instructions across the complete route, including local contact loads, transitions, loading dock and any raised-floor panels. A distributed floor-load rating alone cannot establish the capacity of each local contact along that route."
    ]
  },
  {
    "id": "fire-and-egress",
    "label": "Separate hazards from escape routes",
    "title": "A plant-room incident should not block the data hall’s escape route.",
    "pedagogical_role": "architecture",
    "reference": "d12-safety-and-control-boundaries",
    "explanation": [
      "Place the service and escape routes in the plan alongside electrical equipment, batteries and the compute hall. The drawing gives the data hall a route to an exterior exit that does not pass through the depicted battery room. It locates the design question physically: a room arrangement can couple a hazardous event to the route people need to leave.",
      "This is a design objective, not a compliant evacuation plan. Occupancy, travel distances, number of exits, fire ratings, detection, suppression, battery chemistry and the applicable requirements determine the real design. Those details belong to the site’s fire-protection review. The conceptual plan does not establish a universal rule that every battery installation occupies a separate room."
    ]
  },
  {
    "id": "service-check",
    "label": "Check the replacement plan",
    "title": "Which replacement can happen while the rack keeps running?",
    "pedagogical_role": "check-in",
    "reference": "d12-room-and-replacement-route",
    "explanation": [
      "Ask learners to separate two maintenance jobs on a production GB300 rack: replacing a designated hot-swap power module and replacing a compute tray. Before showing the answer, identify the service boundary, the required evidence and the route the part and handling equipment will take.",
      "A supported PSU hot-swap with sufficient remaining qualified supply capacity can preserve rack power. A compute tray requires its workload to move or stop and the tray to power down. For physical removal, verify the tray-and-lift envelope at turns and openings, plus concentrated loads along the route. A nominally wide door alone establishes none of the other conditions."
    ],
    "controls": [
      {
        "key": "serviceAnswer",
        "label": "Replacement plan",
        "options": [
          [
            "hidden",
            "Discuss"
          ],
          [
            "shown",
            "Show reasoning"
          ]
        ]
      }
    ]
  }
];
