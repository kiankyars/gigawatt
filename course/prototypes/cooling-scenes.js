export const learningContract = Object.freeze({driving_question:'Can the complete liquid path keep the chips within their temperature limit?',fixed_boundary:'Each local thermal, hydraulic and retrofit example declares its heat load and flow boundary.',changed_variable:'Thermal resistance, flow restriction, branch balance or available cooling path.',primary_payoff:'Trace heat and coolant from chip to CDU and identify the limiting interface.',misconception:'Cool supply, enough total flow or spare equipment alone proves adequate cooling.',closing_question:'Which retrofit can handle both chip heat and the residual air load?'});
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
    "label": "Air and liquid paths",
    "title": "Four ways to capture rack heat",
    "kind": "capture-options",
    "description": "Compare CRAH air cooling, cold plates with residual air cooling, rear-door heat exchangers and immersion. A CRAH transfers room-air heat into chilled water.",
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
    "description": "Hold the selected liquid-path heat pickup at 100 kilowatts and water inlet at 35 degrees Celsius. Doubling mass flow from 2.5 to 5 kilograms per second halves its steady temperature rise from 9.57 to 4.78 kelvin. The outlet falls from 44.57 to 39.78 degrees Celsius; these are coolant, not chip, temperatures.",
    "reference": "d10-local-thermal-paths"
  },
  {
    "id": "approach",
    "label": "CDU approach",
    "title": "The two loops need a temperature gap",
    "kind": "approach",
    "description": "Name the separate technology and facility supply temperatures at the CDU. Their difference is CDU approach; return minus supply in one loop is loop temperature rise.",
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
    "label": "Spare CDUs",
    "title": "A spare CDU still needs a working heat path",
    "kind": "redundancy",
    "description": "A hypothetical 1,000 kW selected liquid heat load needs two 600 kW CDUs. Three installed units give N+1 at that duty. One isolated CDU failure leaves 1,200 kW, while loss of the shared facility path defeats all three. Qualified capacities, compatible isolation, sufficient flow and the remaining plant are assumed; no transfer or survival time is calculated.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "independent-cooling-paths",
    "label": "A/B cooling",
    "title": "Keep a second cooling path available",
    "kind": "independent-paths",
    "description": "Two independent upstream trains each contain two 600 kW CDU modules and a sufficient facility loop, outdoor plant, power and controls. A compatible transfer serves the selected 1,000 kW demand through one train. The displayed capacity is that of one surviving train, not their sum. The shared load-side interface remains outside the duplicated scope; this is not a claim that a whole site is fault tolerant.",
    "reference": "d10-cdu-interfaces"
  },
  {
    "id": "cooling-derating",
    "label": "Reduce power",
    "title": "Reduce power to fit the cooling that remains",
    "kind": "derating",
    "description": "After two CDU failures, one qualified 600 kW unit remains. A coordinated operating response is assumed to reduce the selected liquid heat load from 1,000 to 500 kW. At the modeled conditions, 400 kW of excess heat becomes 100 kW of cooling margin. Configured power reduction differs from local temperature-triggered throttling. No electrical cap value, application-throughput ratio or safe response time is inferred. Losing the remaining facility path removes this sustained operating option.",
    "reference": "d10-cdu-interfaces"
  }
];
const byId=new Map([...existing,...captureScenes].map(s=>[s.id,s]));
export const scenes=["why-liquid","heat-path","capture-options","cold-plate","local-heat-flux","device-temperature","water-balance","pump-operating-point","branch-flow","approach","coolit-cdu","coolant-interfaces","lost-flow","independent-cooling-paths","cooling-derating","cooling-retrofit"].map(id=>byId.get(id));
