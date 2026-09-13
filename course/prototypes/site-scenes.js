import { operationsScenes } from "./site-operations.js";
export const learningContract = Object.freeze({
  driving_question:
    "What physical place can install, operate and recover the required compute service?",
  fixed_boundary:
    "Abilene and Colossus 1 are distinct dated cases; generic plans are explicitly original teaching diagrams. Lenovo GB300 is the named hardware service example.",
  changed_variable:
    "Paired physical arrangements; one shared controller switches both cooling trains between running and stopped.",
  primary_payoff:
    "Turn a supply strategy into a coordinated and maintainable site brief.",
  misconception:
    "Gross acres, cabinet footprint or duplicated equipment establish a buildable and recoverable data center.",
  closing_question:
    "Which shared control dependency remains after the cooling equipment is duplicated?",
});
export const initialState = Object.freeze({ control: "normal" });
export const scenes = [
  {
    id: "site-purpose",
    label: "From parcel to rack",
    title: "Turn a parcel into a place you can build, operate and repair.",
    pedagogical_role: "problem",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "Turn the supply strategy into a physical campus. This chapter follows the parcel, the building and the equipment replacement path, then tests which shared physical and control boundaries could interrupt the service.",
      "The deliverable is a buildable site brief: land and connection rights, civil evidence, a coordinated layout, replacement routes and operating boundaries. Concept drawings show mechanisms; they are not construction documents.",
    ],
  },
  {
    id: "greenfield-brownfield",
    label: "Abilene and Colossus 1",
    title: "Abilene built a new campus; Colossus 1 reused a factory.",
    pedagogical_role: "comparison",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "The original Crusoe-built Abilene campus provides the greenfield reference. Colossus 1 occupied the former Electrolux manufacturing facility on Paul Lowery Road in Memphis. This is industrial reuse, not an assertion that the Colossus parcel has a legal brownfield designation or known contamination.",
      "A retained shell may save building work while imposing existing geometry and structural constraints. New construction allows a coordinated arrangement but still needs site and utility infrastructure. Neither label alone proves a faster or cheaper project.",
    ],
  },
  {
    id: "colossus-service",
    label: "What the factory could reuse",
    title: "Colossus 1 inherited utility mains, but needed more grid capacity.",
    pedagogical_role: "architecture",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "MLGW’s historical 2025 update identifies an existing 20-inch water main and 16-inch gas main, with an 8-inch gas tap paid for by xAI. For the first 150 MW of grid service, the utility reported 8 MW through the existing substation and 142 MW through the new substation.",
      "Those are dated utility-service quantities, not a present-day IT meter reading or all sources of site power. The original Paul Lowery Road facility is distinct from the later Tulane Road / Southaven development. The case demonstrates that reuse preserves selected assets; it does not remove the remaining infrastructure work.",
    ],
  },
  {
    id: "usable-land",
    label: "Fit the whole campus",
    title: "Utility corridors and drainage shape the space available to build.",
    pedagogical_role: "mechanism",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "A conceptual parcel contains the building pad, outdoor electrical and cooling equipment, access and future construction. Drainage areas, easements and other restrictions reduce the ground available for those uses. Their overlap must be counted only once.",
      "The planning question is whether the required arrangement fits in connected usable space, with the relevant connections and access. An area total does not establish a workable geometry. This original drawing changes only the presence of documented site constraints; it is not a real parcel or a regulatory setback.",
    ],
  },
  {
    id: "rights-and-routes",
    label: "Texas: surface and mineral rights",
    title: "Buying Texas land may leave mineral rights with another owner.",
    pedagogical_role: "mechanism",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "Texas recognizes separate surface and mineral estates. A surface purchase can therefore leave the minerals with another owner. The Railroad Commission explains that the mineral estate is generally dominant: reasonably necessary use of the surface can include roads, wells and pipelines. Deeds, leases, ordinances and the accommodation doctrine can limit that use.",
      "This Texas case explains why title investigation must extend below the proposed buildings. It does not assert a mineral dispute at Abilene. Investigate severed estates, existing leases and surface-use agreements alongside the easements needed for power, fuel, water and fiber. Owning the campus parcel also does not create rights across someone else’s land.",
    ],
  },
  {
    id: "ground-and-foundations",
    label: "Carry the load into the ground",
    title: "Weak ground can force foundations below the surface layers.",
    pedagogical_role: "mechanism",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "Geotechnical investigation describes the soil, rock and groundwater conditions relevant to the actual structures. Compressible fill, settlement, groundwater and contamination are different findings with different design consequences. Regional soil mapping can screen questions but does not replace site-specific investigation.",
      "The cross-section is conceptual: one proposed load path meets variable ground. Boreholes represent evidence collection, not a prescribed spacing or depth. Earthwork, ground improvement or a different foundation can change cost and schedule; the engineer determines which solution fits the measured conditions.",
    ],
  },
  {
    id: "outside-flood",
    label: "Access beyond the fence",
    title: "A flooded bridge can isolate a campus on dry ground.",
    pedagogical_role: "counterexample",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "Flood assessment must include dependencies outside the building footprint. A shared low bridge can carry the access route or multiple cable routes even when the campus is on higher ground. Local elevations, drainage, hazard maps and the actual utility routes determine exposure.",
      "This synthetic example changes a single shared crossing. It illustrates a common-cause exposure, not the flood risk of Abilene or Memphis. River flooding can isolate communities and damage roads; a dry building alone therefore does not establish continued access or service.",
    ],
  },
  {
    id: "fiber-diversity",
    label: "Independent fiber approaches",
    title: "Separate fiber entrances remove a shared point of failure.",
    pedagogical_role: "counterexample",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "Physical route diversity is an established design practice. QTS describes its operating Suwanee campus with diverse fiber entrances and redundant campus conduits. Its January 2023 article separately describes four entrances in a planned DC2 refresh; the slide uses the established campus claim rather than treating the announced refresh as completed.",
      "The paired route sketches are illustrative, not a map of QTS. One illustrates two cables sharing an entrance, while the other has separate approaches. Separation removes the pictured shared exposure; it does not prove end-to-end independence. Circuits may still meet in an upstream bridge, duct or facility. Zayo’s March 2026 announcement of four diverse routes under construction for QTS Cambois is an additional AI-campus example.",
    ],
  },
  {
    id: "climate-and-water",
    label: "Two AI cooling designs",
    title:
      "Abilene rejects heat without evaporation; Colossus 1 also uses cooling towers.",
    pedagogical_role: "comparison",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "Crusoe describes Abilene’s outdoor heat rejection as non-evaporative air-cooled chillers. This is a named AI-factory example, not a claim that all Texas facilities must use dry cooling or that Abilene relies only on passive dry coolers. Its liquid loops carry heat inside the system without establishing an evaporative process outdoors.",
      "Colossus 1 provides the comparison: TDEC identifies xAI Colossus as a user of evaporative cooling in its 2025 reclaimed-water proposal. FAS’s original May 2026 imagery analysis identifies both cooling towers and air-cooled chillers. The proposal does not prove the reclaimed-water plant is operational. Dry rejection depends on outdoor dry-bulb temperature; evaporative rejection uses the wet-bulb boundary and consumes makeup water. Actual equipment capacity remains conditional on its rated operating conditions.",
    ],
  },
  {
    id: "neighbors-and-permits",
    label: "Design around the neighbors",
    title:
      "Plant placement and acoustic barriers control how sound reaches neighbors.",
    pedagogical_role: "architecture",
    reference: "d12-hazards-and-site-evidence",
    explanation: [
      "Outdoor heat rejection and generation introduce sound, exhaust, access and environmental interfaces. Nearby occupied property, prevailing conditions and applicable permissions can affect equipment arrangement, enclosure, treatment and operating limits.",
      "The drawing marks engineering questions rather than setback distances, permitted emission rates or a compliant design. An air permit, land-use approval and an electrical interconnection answer different questions. Their actual conditions must be reconciled in one site layout.",
    ],
  },
  {
    id: "phased-campus",
    label: "CoreWeave: opening in phases",
    title:
      "Polaris Forge 1 opened its first phase while the next was being completed.",
    pedagogical_role: "architecture",
    reference: "d12-room-and-replacement-route",
    explanation: [
      "This is the Applied Digital Polaris Forge 1 campus in Ellendale, North Dakota, leased to CoreWeave. Applied Digital reported the first 50 MW ready for service on October 27, 2025 and another 50 MW on November 24, completing its first 100 MW building. These are ready-for-service milestones, not measured IT power.",
      "Chapter 4 uses the same case to explain the value of earlier service. Here the physical consequence is the focus: staff, equipment replacements and emergency access must coexist with delivery trucks, excavation and commissioning for later work. The site paths are a generic planning illustration, not the disclosed Polaris Forge construction layout.",
    ],
  },
  {
    id: "room-layout",
    label: "Inside the building",
    title:
      "Equipment rooms and service corridors belong in the layout from the start.",
    pedagogical_role: "architecture",
    reference: "d12-room-and-replacement-route",
    explanation: [
      "White space houses IT equipment. Grey space includes supporting electrical and mechanical areas. The distinction describes location and use; it does not decide every cooling or power component’s placement.",
      "The floor plan is a conceptual arrangement with IT rows, separate support rooms, a receiving area and a service corridor. Cabinet positions, pipe/cable routes, fire boundaries and access must be coordinated. The next scenes examine the actual equipment that must enter and be serviced.",
    ],
  },
  {
    id: "gb300-physical",
    label: "The rack and its serviceable parts",
    title:
      "Moving a rack and replacing a tray require separate handling plans.",
    pedagogical_role: "mechanism",
    reference: "d12-room-and-replacement-route",
    explanation: [
      "Lenovo’s GB300 NVL72 mechanical specification lists the complete rack solution at approximately 1,580 kg, depending on configuration. This is distinct from an empty rack frame. Its August 30, 2026 product guide lists the compute tray at 29 kg; both images show actual Lenovo products.",
      "The manufacturer mass informs the handling and structural design, but it is not a caster-load or floor-pressure rating. Loads pass through the actual feet, casters and handling equipment. Lenovo calls for a suitable material lift for single-person compute-tray service. Those interfaces motivate the following service and replacement scenes.",
    ],
  },
  ...operationsScenes,
];
