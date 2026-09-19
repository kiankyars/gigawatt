export const learningContract = Object.freeze({driving_question:'Can the complete liquid path keep the chips within their temperature limit?',fixed_boundary:'Each local thermal, hydraulic and retrofit example declares its heat load and flow boundary.',changed_variable:'Thermal resistance, flow restriction or available cooling path.',primary_payoff:'Trace heat and coolant from chip to CDU and identify the limiting interface.',misconception:'Cool supply, enough total flow or spare equipment alone proves adequate cooling.',closing_question:'Which retrofit can handle both chip heat and the residual air load?'});
import {captureScenes} from './cooling-capture.js';
const existing=[
  {
    "id": "why-liquid",
    "label": "Why liquid",
    "title": "Why Is Air Cooling Dead?",
    "kind": "why-liquid",
    "description": "Compare approximate water and air volumetric heat capacity at a declared teaching point. This motivates compact heat transport without claiming that liquid alone establishes chip temperatures.",
    "reference": "d10-local-thermal-paths"
  },
  {
    "id": "capture-options",
    "label": "Air and liquid cooling",
    "title": "Out with the Old, In with the New",
    "kind": "capture-comparison",
    "description": "Top: rack heat enters room air, then a computer room air handler (CRAH) transfers it to chilled water. Bottom: cold plates move chip heat through technology coolant to a liquid-to-liquid coolant distribution unit (CDU), which transfers it into separate facility water. Residual air heat needs a separate path, which can be a CRAH or rear-door exchanger depending on the design. This is a generic comparison, not an Abilene floor plan.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "capture-rear-door", "label": "Rear-door heat exchanger",
    "title": "A rear-door exchanger cools the exhaust air",
    "kind": "rear-door-comparison",
    "description": "Left: NVIDIA’s DGX GB300 rear-assembly diagram identifies the coolant manifolds serving chip cold plates. Right: a separate rear-door exchanger schematic shows the residual air heat of a cold-plate-cooled rack crossing a water coil. The photographed GB300 manifolds are not a rear-door heat exchanger. Depending on the installation, the door receives compatible facility water or a separate coolant loop through a CDU.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "capture-immersion", "label": "Immersion cooling",
    "title": "What the heck is immersion cooling and why are there two types?",
    "kind": "immersion-photo",
    "description": "The supplied 2CRSi diagram shows single-phase immersion: electrically insulating liquid circulates around the electronics, then through a coolant-to-water heat exchanger. It stays liquid. In two-phase immersion, the fluid boils at the hardware, vapor condenses at a cooled surface, and liquid returns to the bath. The diagram depicts the single-phase path; the two captions distinguish the mechanisms.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "immersion-hardware",
    "label": "Inside an immersion tank",
    "title": "Inside an immersion tank",
    "kind": "immersion-hardware",
    "description": "The supplied photograph shows server assemblies immersed in liquid. Use it to connect the preceding fluid-loop diagram to physical equipment. The photograph's operator, coolant and operating conditions were not supplied.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "cold-plate",
    "label": "Cold-plate hardware",
    "title": "How does coolant reach the cold plates?",
    "kind": "coldplate-photo",
    "description": "The supplied photograph shows copper cold-plate assemblies, tubes, hoses and couplings. Beside it, a functional circuit follows technology coolant from the CDU through a supply manifold and tray quick disconnects into cold plates, then back through the return manifold. Separate facility water removes heat across the CDU exchanger. The user supplied the photograph as GB300 context; its maker and exact model remain unverified. No visible surface pattern is identified as an internal coolant channel.",
    "reference": "d10-local-thermal-paths"
  },
  {
    "id": "abilene-coolant-distribution",
    "label": "Liquid cooling at Abilene",
    "title": "Liquid cooling inside Abilene",
    "kind": "abilene-photo",
    "description": "We have followed coolant through one cold plate. Here is the physical distribution across a row: overhead pipes, flexible hoses and connections at the racks. Next, we follow the heat that still leaves through the air. Oracle's Abilene campus photograph connects the component diagram to real equipment; it does not identify hidden loop boundaries or establish which visible equipment is a CDU or rear-door exchanger.",
    "reference": "d10-cdu-interfaces",
    "sources": ["https://www.oracle.com/news/resources/abilene-campus/"],
    "pedagogical_role": "case-study"
  },
  {
    "id": "water-balance",
    "label": "Flow and temperature rise",
    "title": "More flow means less temperature rise",
    "kind": "water-balance",
    "description": "Predict the effect of doubling flow, then compare. Hold the selected liquid-path heat pickup at 100 kilowatts and water inlet at 35 degrees Celsius. Doubling mass flow from 2.5 to 5 kilograms per second halves its steady temperature rise from 9.57 to 4.78 degrees Celsius. The outlet falls from 44.57 to 39.78 degrees Celsius; these are coolant, not chip, temperatures.",
    "reference": "d10-local-thermal-paths"
  },
  {
    "id": "approach",
    "label": "CDU approach",
    "title": "CDU approach is the gap between the two supply temperatures",
    "kind": "approach",
    "description": "Facility water enters the CDU at 30 degrees Celsius. The separate rack coolant leaves for the chips at 35 degrees Celsius. The supply-temperature difference is a 5 degree Celsius CDU approach. Heat crosses the exchanger from warmer rack coolant to cooler facility water without the fluids mixing. This is a temperature difference, not a chip temperature or a loop return-minus-supply rise. A difference of 5 degrees Celsius equals 5 kelvin. At the same facility inlet temperature and heat duty, a lower approach gives more margin to the rack-coolant temperature limit. Achieving it depends on exchanger design and flow; added exchanger size, pumping demand and cost can offset the temperature benefit.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "coolit-cdu",
    "label": "CoolIT CHx2000",
    "title": "Inside a CoolIT CHx2000",
    "kind": "cdu",
    "description": "Official product photographs show a row-scale liquid-to-liquid CDU. Manufacturer-listed 2 MW at 5°C approach and 2125 L/min at 35 psi are separately stated thermal and hydraulic points.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "lost-flow",
    "label": "N, N+1 and 2N",
    "title": "Redundancy Applied to Coolant Distribution",
    "kind": "redundancy",
    "description": "For 1,000 kW of liquid heat with each CDU qualified for 600 kW at the operating conditions, N is two CDUs. N+1 installs three: one can fail while two still carry the load. 2N duplicates the complete required cooling train: two CDUs plus facility cooling, power and controls on each side. An extra CDU alone does not duplicate shared upstream dependencies.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "independent-cooling-paths",
    "label": "A/B cooling",
    "title": "2N: either cooling train can carry the load",
    "kind": "independent-paths",
    "description": "Two independent upstream trains each contain two 600 kW CDU modules and a sufficient facility loop, outdoor plant, power and controls. A compatible transfer serves the selected 1,000 kW demand through one train. The displayed capacity is that of one surviving train, not their sum. The shared load-side interface remains outside the duplicated scope; this is not a claim that a whole site is fault tolerant.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "cooling-derating",
    "label": "Reduce power",
    "title": "Reduce power to fit the cooling that remains",
    "kind": "derating",
    "description": "Two cases share the same remaining 600 kW cooling capacity after two CDU failures, with the facility path available. A 1,000 kW liquid heat load exceeds capacity by 400 kW. A coordinated reduction to 500 kW leaves 100 kW cooling margin. Configured power reduction differs from local temperature-triggered throttling. No electrical cap value, application-throughput ratio or safe response time is inferred.",
    "reference": "d10-cdu-interfaces"
  }
];
const byId=new Map([...existing,...captureScenes].map(s=>[s.id,s]));
export const scenes=["why-liquid","capture-options","cold-plate","abilene-coolant-distribution","capture-rear-door","capture-immersion","immersion-hardware","local-heat-flux","device-temperature","water-balance","pump-operating-point","approach","coolit-cdu","lost-flow","independent-cooling-paths","cooling-derating","cooling-response","cooling-retrofit"].map(id=>byId.get(id));
// Preserve useful destinations for bookmarks to the removed standalone slides.
export const sceneAliases={"rack-coolant-entry":"cold-plate","heat-path":"capture-options","capture-coldplates":"capture-options","crah-cdu":"capture-options","branch-flow":"pump-operating-point","coolant-interfaces":"cooling-retrofit"};
