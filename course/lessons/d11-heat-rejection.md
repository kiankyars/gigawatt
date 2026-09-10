# The heat does not disappear at the chiller

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d11-heat-rejection`, then run `uv run gigawatt-expand`.

**D11 · Authored draft · Objectives:** D11.1, D11.2

Trace dry, evaporative, refrigerated and economizer paths, then close the energy balance around the equipment actually being measured.

**Driving question:** What reaches the environment after cooling equipment has moved the IT heat?

## Four paths, four different jobs

Picture a rack drawing steady electrical power. Its cooling system collects heat, but collection is only the beginning of a route to an external sink. A dry cooler passes a fluid through a heat exchanger exposed to outdoor air. Heat crosses the exchanger wall; the air and circulating fluid normally remain separate. Fans and pumps help the transfer. Calling this arrangement dry describes the rejection mechanism, not the absence of liquid inside the building.

An evaporative tower instead uses evaporation as an important route for transferring heat to the atmosphere. The tower water may be on a separate loop from the clean coolant near the computers. A refrigeration machine adds another function: it uses work to move heat from a colder side to a warmer side. Its condenser can ultimately reject through air or water. Consequently, tower, chiller and liquid cooling are not mutually exclusive descriptions of an entire facility.

An economizer is an operating arrangement that exploits favorable outside conditions to reduce or avoid compressor cooling. It still needs a complete heat path. Depending on the design, that path can exchange heat through outdoor air or a separate water circuit. Fans, pumps, filtration and controls do not disappear when compressors stop. In your sketch, mark the heat-transfer interfaces first, then add electrical inputs and any water crossing the site boundary. That order prevents equipment names from substituting for an explanation.

## COP is a ratio at a stated boundary

Cooling coefficient of performance is cooling delivered divided by the corresponding work input, expressed in consistent units. A cooling duty of 10 MW with 2 MW of compressor input has a compressor-boundary COP of five. That is not an electrical conversion efficiency of 500 percent. The machine is moving heat already present at its evaporator, and work is helping drive that transfer. DOE defines COP in terms of useful cooling or heating effect relative to work input; which mode and equipment boundary matter.

For our idealized steady chiller, the condenser receives both the evaporator heat and the compressor work: Qcond = Qevap + Wcomp. If a condenser rating is compared only with the IT load, the compressor contribution can be omitted accidentally. Conversely, adding all site overhead to the evaporator and then adding it again at the condenser double counts energy. Follow the actual location where each motor, pump or conversion loss becomes heat, rather than putting every auxiliary in one convenient box.

A broader plant COP includes the chosen pumps and fans in its electrical denominator. It is usually a different number from the chiller COP. Neither ratio by itself is PUE: PUE relates total facility energy to IT energy over a stated interval. If a dashboard displays a high COP, ask which meters produced the numerator and denominator, how their intervals were aligned, and whether the reported load and input were simultaneous. The ratio is meaningful only after those questions have answers.

## Why a correct balance can still be an incomplete design

A steady energy balance answers how much heat must leave; it does not tell us what temperatures, pressures, flows or equipment will achieve the transfer. Ten megawatts can be collected at different coolant temperatures, and the same outdoor equipment can behave differently across those conditions. The useful design question is whether the entire transfer chain can satisfy the required device inlet conditions at the declared load and ambient condition.

Time adds another boundary. Immediately after a load increase, heat can accumulate in metal, coolant and air. The instantaneous external rejection rate therefore need not equal the instantaneous electrical draw. To predict temperature rise, we would need stored thermal energy, effective heat capacities, mixing, transport delays and control behavior. This lesson deliberately calculates an established steady operating point. It does not turn an omitted thermal model into a guessed ride-through time.

The practical habit is to annotate every arrow with both a physical meaning and an accounting boundary. A fluid arrow represents moving material; a heat arrow represents energy crossing an interface. A wire feeding a fan brings electricity that eventually joins a heat path. Once these are distinct, a changed architecture becomes easier to compare: identify which interfaces moved, which electrical inputs changed, and which outdoor duty remains to be served.

## Worked example: One load, two COP boundaries

- Synthetic steady operating point; all rates in MW.
- The evaporator receives 10 MW. Compressor input is 2 MW.
- A separate 0.5 MW of pumps and fans lies outside the chiller electrical boundary. This exercise places its dissipation outside the evaporator load.

1. Chiller COP — 10 MW / 2 MW = 5 — Only compressor input is included in this declared equipment ratio.
2. Condenser duty — 10 MW + 2 MW = 12 MW — Compressor work joins the extracted heat on the hot side.
3. Plant COP — 10 MW / (2 + 0.5) MW = 4 — The same useful cooling is divided by a larger, explicitly defined electrical input.
4. Ultimate heat addition — 10 + 2 + 0.5 = 12.5 MW — All listed energy eventually reaches the environment, although not necessarily through one condenser.

**Result:** The chiller COP is 5, plant COP is 4, and the condenser itself rejects 12 MW under the stated placement of auxiliaries.

**Model boundary:** No equipment sizing, temperature lift, transient response or certified efficiency is inferred.

## The tradeoff

Choice: Move toward warmer coolant where device limits permit.

Benefit: A smaller temperature lift or wider economizer opportunity may reduce cooling work.

Cost: Device operating envelopes, exchanger approaches and control margins must still be satisfied; this direction is not a quantified saving without performance evidence.

## When the situation changes

Trigger: The design review sizes outdoor rejection at the evaporator duty alone.

Mechanism: Compressor heat has been omitted, leaving the selected operating point unsupported.

Response: Reconcile each input at its actual boundary and compare the resulting duty with specified performance at the required temperatures.

## Apply the idea

The same evaporator duty is 10 MW, but compressor input rises to 2.5 MW and the other auxiliaries stay at 0.5 MW. Find chiller COP, plant COP and condenser duty.

<details>
<summary>Reveal the worked answer</summary>

Chiller COP = 4; plant COP = 10/3 ≈ 3.33; condenser duty = 12.5 MW.

More compressor work lowers both ratios while increasing hot-side rejection. The outdoor condenser receives 10 + 2.5 MW, not 13 MW, because the separate auxiliary dissipation was explicitly placed outside that condenser boundary. Ultimate environmental heat from all listed inputs is 13 MW.

</details>

**The idea to keep:** Cooling moves a heat load and often adds another one. State the boundary before calculating COP or rejection duty.

## Sources and reading boundaries

- [Incorporate Minimum Efficiency Requirements for Heating and Cooling Products into Federal Acquisition Documents](https://www.energy.gov/cmei/femp/incorporate-minimum-efficiency-requirements-heating-and-cooling-products-federal) — COP definition in the heat-pump table notes; cooling effect divided by work in identical units. Read 2026-09-06. Definition and rating-boundary notes inspected; no listed efficiency threshold is used as a data-center design requirement.
- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — Cooling-system and economizer discussion supports distinguishing heat-path arrangements. Read 2026-09-06. Selected cooling discussion inspected; this lesson supplies original simplified schematics and does not reproduce handbook figures or equipment ratings.
