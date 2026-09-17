export const learningContract = Object.freeze({driving_question:'Can the complete liquid path keep the chips within their temperature limit?',fixed_boundary:'Each local thermal, hydraulic and retrofit example declares its heat load and flow boundary.',changed_variable:'Thermal resistance, flow restriction or available cooling path.',primary_payoff:'Trace heat and coolant from chip to CDU and identify the limiting interface.',misconception:'Cool supply, enough total flow or spare equipment alone proves adequate cooling.',closing_question:'Which retrofit can handle both chip heat and the residual air load?'});
import {captureScenes} from './cooling-capture.js';
const existing=[
  {
    "id": "why-liquid",
    "label": "Why liquid",
    "title": "Why use liquid cooling?",
    "kind": "why-liquid",
    "description": "Compare approximate water and air volumetric heat capacity at a declared teaching point. This motivates compact heat transport without claiming that liquid alone establishes chip temperatures.",
    "reference": "d10-local-thermal-paths"
  },
  {
    "id": "heat-path",
    "label": "Complete heat path",
    "title": "Follow the heat out of the rack",
    "kind": "route",
    "description": "A liquid-to-liquid coolant distribution unit transfers heat from the rack loop into a separate facility loop. Facility water carries heat to outdoor rejection. The fluids do not mix.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "capture-options",
    "label": "Air cooling / CRAH",
    "title": "Air carries rack heat to a CRAH",
    "kind": "capture-options",
    "capture": "air",
    "description": "A computer room air handler (CRAH) uses fans to move warm room air over a chilled-water coil and returns cooled air to the room. Heat passes from air into water; the two do not mix.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "capture-coldplates", "label": "Cold plates + air",
    "title": "Cold plates carry chip heat directly into liquid",
    "kind": "capture-options", "capture": "coldplate",
    "description": "Cold plates take heat directly from selected chips into a pumped coolant loop. A liquid-to-liquid CDU transfers that heat into separate facility water. Components outside the cold-plate path still release heat to room air and need air cooling.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "crah-cdu", "label": "CRAH versus CDU",
    "title": "A CRAH cools air; a CDU serves the rack coolant loop",
    "kind": "crah-cdu",
    "description": "CRAH means computer room air handler: fans circulate room air across a chilled-water coil. CDU means coolant distribution unit: pumps circulate rack coolant and controls regulate its supply. In the liquid-to-liquid CDU shown here, a heat exchanger transfers heat to separate facility water without mixing the fluids. A cold-plate installation can use both: CDU for chip heat, CRAH for residual air heat. Liquid-to-air CDUs also exist.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "capture-rear-door", "label": "Rear-door heat exchanger",
    "title": "A cooled rear door captures heat from rack exhaust",
    "kind": "capture-options", "capture": "rear-door",
    "description": "Server fans move air through the rack and the rear-door water coil. Heat moves from chips to air, then into water at the door. The depicted arrangement uses compatible facility water; other installations place a CDU between the door and facility loop.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "capture-immersion", "label": "Immersion cooling",
    "title": "Immersion puts the electronics in dielectric liquid",
    "kind": "capture-options", "capture": "immersion",
    "description": "Qualified electronics sit in electrically insulating liquid. Single-phase liquid warms without boiling; two-phase liquid boils and the vapor condenses at a cooled surface. Both methods need a downstream path to reject the captured heat.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "cold-plate",
    "label": "Inside a cold plate",
    "title": "Inside a cold plate",
    "kind": "plate",
    "description": "Processor heat crosses the package, thermal interface and plate metal into coolant channels. The coolant does not contact the silicon junction.",
    "reference": "d10-local-thermal-paths"
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
    "description": "Facility water enters the CDU at 30 degrees Celsius. The separate rack coolant leaves for the chips at 35 degrees Celsius. The supply-temperature difference is a 5 degree Celsius CDU approach. Heat crosses the exchanger from warmer rack coolant to cooler facility water without the fluids mixing. This is a temperature difference, not a chip temperature or a loop return-minus-supply rise. A difference of 5 degrees Celsius equals 5 kelvin.",
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
    "title": "N is enough capacity; N+1 adds a spare; 2N duplicates the system",
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
export const scenes=["why-liquid","capture-options","capture-coldplates","crah-cdu","capture-rear-door","capture-immersion","cold-plate","local-heat-flux","device-temperature","water-balance","pump-operating-point","approach","coolit-cdu","lost-flow","independent-cooling-paths","cooling-derating","cooling-retrofit"].map(id=>byId.get(id));
// Preserve useful destinations for bookmarks to the removed standalone slides.
export const sceneAliases={"heat-path":"crah-cdu","branch-flow":"pump-operating-point","coolant-interfaces":"cooling-retrofit"};
