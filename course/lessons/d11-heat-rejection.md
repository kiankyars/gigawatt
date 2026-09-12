# The heat does not disappear at the chiller

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d11-heat-rejection`, then run `uv run gigawatt-expand`.

**D11 · Authored draft · Objectives:** D11.1, D11.2

Separate rack heat capture from outdoor dry, wet and hybrid rejection; distinguish air- and water-cooled chillers, then close the heat and work balance.

**Driving question:** What reaches the environment after cooling equipment has moved the IT heat?

## Follow the heat before naming the equipment

D10 collected heat at an air stream, rear-door exchanger, cold plate or immersion bath. Here the question is how that heat leaves the site. A dry cooler moves warm liquid through a coil while outdoor air passes over it. The streams stay separate and the liquid cools without intentional evaporation. Dry describes outdoor rejection: water can still circulate through the building. The relevant air temperature is the dry bulb, introduced and compared with wet bulb in the next lesson.

Wet cooling uses evaporation. In an open cooling tower, some circulating water evaporates as air contacts it; the remaining water cools and returns to collect more heat. A closed-circuit evaporative cooler instead keeps process liquid inside a coil while separate spray water evaporates outside it. Neither arrangement implies that rack coolant is sprayed into the air. Identify the water circuit that consumes makeup water; D11’s water ledger follows that circuit.

Hybrid equipment combines dry and evaporative operation. One adiabatic arrangement precools entering air through wetted pads before that air reaches a dry coil. The process liquid remains inside the coil, while the precooling step consumes water. Humidity limits the evaporative benefit, and the controller can enable wet operation only under selected conditions. A wet pad is not a compressor, and adding one does not guarantee the required temperature on every day.

A chiller uses refrigeration to transfer heat from its colder evaporator to its warmer condenser. Air-cooled means the condenser rejects to air; water-cooled means it rejects to a separate water circuit. That water circuit commonly leads to a tower, though the supplied design must identify its actual final sink. Both types can deliver chilled water to the same load. Thus liquid cooling at the rack does not determine the chiller type or prove that outdoor rejection consumes evaporative water.

An economizer is an operating arrangement that uses favorable outdoor conditions to reduce or avoid compressor operation. An airside arrangement can use outdoor air to cool the room; a waterside arrangement can transfer heat through a cooler or tower path. Pumps, fans, filtration and controls still require resources. Mark each heat-transfer interface, electrical input and water intake on the same drawing before comparing modes.

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
- [ASHRAE Handbook 2024 — Cooling Towers](https://handbook.ashrae.org/Handbooks/S24/IP/s24_ch40/s24_ch40_ip.aspx) — Tower range compares entering and leaving water; tower approach compares leaving water with entering-air wet bulb. Performance depends on the stated heat load, flow and air conditions; closed-circuit towers separate process liquid from spray water. Read 2026-09-11. Selected mechanism, terminology, closed-circuit and performance-curve sections reviewed. No handbook example approach, capacity or water-saving percentage is adopted as a universal design value.
- [Vertiv — Optimizing Chilled Water Systems, July 2024](https://www.vertiv.com/495988/globalassets/shared/vertiv-chilled-water-solution-white-paper-sl-18066.pdf) — The Adiabatic System section explains evaporative air precooling through wet pads ahead of coils and control-dependent water use. Read 2026-09-11. Selected text on printed pages 6–7 reviewed. The claim of no additional energy cost and the simulated energy/WUE savings are not adopted; fans, pumps and controls retain their declared electricity boundary.
- [Trane — Air vs. Water Cooled Chillers](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html) — Air-cooled and water-cooled classify the condenser heat-rejection arrangement. The discussed water-cooled configuration uses condenser water and a cooling tower; compressor work depends on operating conditions. Read 2026-09-11. Mechanism and comparison sections reviewed. The tower-based configuration is one arrangement, not proof every water-cooled chiller must use an evaporative tower; no generic lifespan or efficiency advantage is adopted.
- [Trane TRACE 3D Plus — Air Cooled Chillers](https://trace3dplus.help.trane.com/air_cooled_chillers.html) — An air-cooled chiller can make chilled water while its condenser rejects heat to air, resolving the ambiguity between load coolant and condenser cooling medium. Read 2026-09-11. Opening definition reviewed. No software performance curve is reused or extrapolated.
