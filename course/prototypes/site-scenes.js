import { rapidBuildScenes } from "./rapid-build-cases.js";

// Keep shared Chapter 5 case links useful after moving modular construction.
export function siteSceneRedirect(locationHref, moduleHref = import.meta.url) {
  const current = new URL(locationHref);
  if (current.hash !== "#aws-houdini-prefab") return null;
  const destination = new URL("./procurement-cases-format.html", moduleHref);
  destination.search = current.search;
  destination.hash = current.hash;
  return destination.href;
}

export const learningContract = Object.freeze({
  "driving_question": "What physical place can install, operate and recover the required compute service?",
  "fixed_boundary": "Abilene and Colossus 1 are distinct dated cases; generic plans are explicitly original teaching diagrams. Lenovo GB300 is the named hardware service example.",
  "changed_variable": "Physical arrangements and the service boundary for a power module versus a compute tray.",
  "primary_payoff": "Turn a supply strategy into a coordinated and maintainable site brief.",
  "misconception": "Gross acres, cabinet footprint or duplicated equipment establish a buildable and recoverable data center.",
  "closing_question": "How can a new hall be built without cutting the live hall’s access and fiber?"
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
  ...rapidBuildScenes.filter(scene => scene.id === "meta-prometheus-tents"),
  {
    "id": "usable-land",
    "label": "Fit the whole campus",
    "title": "Utility corridors and drainage shape the space available to build.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "A conceptual parcel contains the building pad, outdoor electrical and cooling equipment, access and future construction. Drainage here means managing rainwater from roofs, roads and equipment yards; a closed cooling loop does not remove that need. Drainage areas, easements and other restrictions reduce the ground available for those uses. Their overlap must be counted only once.",
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
    "title": "Texas projects must secure land and the rights to use it.",
    "pedagogical_role": "mechanism",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "New Era’s August 14, 2026 issuer update said all 493 acres for Texas Critical Data Centers near Odessa had been secured, with one final surface waiver pending from a leasehold operator. It also reported removal of 22 abandoned pipelines across 12 rights-of-way. These are distinct site-development milestones.",
      "The release establishes an outstanding agreement, not a quantified mineral-caused delay. Another actual contract, Fermi’s May 2025 Project Matador ground lease, made a surface waiver a commencement condition unless the tenant waived it. Its later filing reports commencement in September 2025 after conditions were satisfied or waived. Agreements can resolve surface use without buying every mineral interest.",
      "SemiAnalysis’s September 10, 2026 article reproduces its August 24 BTM Tracker chart: about 17 GW of booked onsite generation belongs to named Texas sites, the largest named-state total. Another 29 GW has no site chosen. The chart ranks generating nameplate ordered for data centers, excluding batteries; it does not rank operating data-center count, IT capacity or completed construction. The chart supplies the scale context, while New Era supplies a separate concrete surface-rights example."
    ]
  },
  {
    "id": "docklands-context",
    "label": "ADA Docklands: the setting",
    "title": "ADA’s new London campus starts on old industrial ground.",
    "pedagogical_role": "context",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "ADA Infrastructure’s Docklands campus is in East London’s Royal Docks. Its June 2024 planning announcement described three planned data-center buildings. The image is the developer’s proposed campus visualization, not a photograph of completed construction.",
      "Menard’s project account identifies the site’s previous docklands use and buried foundations, tanks and timber piles. A new aboveground campus therefore inherits old conditions below it. The following engineering slide keeps the actual groundworks photograph and distinguishes the support required by buildings from that required by external utilities."
    ],
    "sources": [
      "https://adainfrastructure.com/en-US/insights/news/ada-infrastructure-approved-to-develop-210-mw-data-center-campus-in-east-londons-royal-docks",
      "https://menard.co.uk/soil-expert-portfolio/london-silvertown-project-olympus-data-centre/"
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
    "id": "harvey-context",
    "label": "Houston: Hurricane Harvey",
    "title": "Harvey’s slow passage brought days of flooding to Houston.",
    "pedagogical_role": "context",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Hurricane Harvey made landfall on the Texas coast on August 25, 2017. Slow storm movement kept rain bands over southeastern Texas. The National Weather Service records rapid flash flooding across Harris County during the night of August 26–27, followed by more heavy rain on August 29–30 that worsened the existing floods.",
      "The actual August 28 Houston-area road photograph is credited to TxDOT by NWS Houston/Galveston. It establishes the regional access emergency, not the location or condition of Equinix HO1. The next slide uses a separate contemporaneous operator statement and later staff account to explain that facility’s continuity and access experience."
    ],
    "sources": [
      "https://www.weather.gov/hgx/hurricaneharvey"
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
    "id": "fiber-diversity",
    "label": "QTS Suwanee: separate fiber entrances",
    "title": "QTS Suwanee DC1 uses three separate fiber entrances.",
    "pedagogical_role": "counterexample",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "The original QTS campus plan establishes the two-building setting in Suwanee, Georgia. QTS’s DC1 facility sheet identifies three diverse underground fiber entry laterals. The side-by-side sketches compare a shared building entry with three separated entries, matching the documented DC1 topology count without inventing the precise route geometry. The shared-entry layout is a counterexample, not QTS’s layout.",
      "QTS’s January 2023 expansion account separately proposed four diverse entrances for DC2. Three DC1 entrances and four proposed DC2 entrances describe different buildings. The actual campus plan does not disclose surveyed cable alignments. Physical entrance diversity removes a local shared exposure; it does not certify end-to-end independence of carrier networks."
    ]
  },
  {
    "id": "climate-and-water",
    "label": "Two AI cooling designs",
    "title": "Local climate and water supply shape the cooling design.",
    "pedagogical_role": "comparison",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "Crusoe describes Abilene’s outdoor heat rejection as non-evaporative air-cooled chillers. This is a named AI-factory example, not a claim that all Texas facilities must use dry cooling or that Abilene relies only on passive dry coolers. Its liquid loops carry heat inside the system without establishing an evaporative process outdoors.",
      "Colossus 1 provides the comparison: TDEC identifies xAI Colossus as a user of evaporative cooling in its 2025 reclaimed-water proposal. FAS’s original May 2026 imagery analysis identifies both cooling towers and air-cooled chillers. The proposal does not prove the reclaimed-water plant is operational. Dry rejection depends on outdoor dry-bulb temperature; evaporative rejection uses the wet-bulb boundary and consumes makeup water. Actual equipment capacity remains conditional on its rated operating conditions.",
      "This is the site-selection preview. The Chip and rack heat capture / Heat rejection, climate and water sequence teaches chillers, cooling towers, dry-bulb and wet-bulb temperatures and water balance in depth. Makeup water means water added to replace evaporation, blowdown and other losses. It describes the water’s role, not its quality: a suitable source can be potable water, reclaimed wastewater or another treated supply."
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
    "id": "service-check",
    "label": "Knowledge check: expand a live campus",
    "title": "Plan Hall B without interrupting Hall A.",
    "pedagogical_role": "check-in",
    "reference": "d12-hazards-and-site-evidence",
    "explanation": [
      "A live Hall A uses an access road and a duct carrying both fiber services. The proposed excavation for Hall B cuts across both. Ask learners what must move before digging begins, then reveal the replacement routes and a short construction sequence.",
      "Build the alternative access road and replacement fiber while the original routes stay in service. Test the new connection, switch the live service and access onto the replacements, then start excavation. Moving only the road leaves the shared fiber exposure; moving only fiber leaves Hall A without access. This check focuses on route geometry and continuity during construction; land agreements are covered earlier in the chapter."
    ],
    "controls": [
      {
        "key": "serviceAnswer",
        "label": "Expansion plan",
        "options": [
          [
            "hidden",
            "Show the problem"
          ],
          [
            "shown",
            "Show one sequence"
          ]
        ]
      }
    ]
  }
];
