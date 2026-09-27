# The same air temperature can create different cooling limits

**12. Heat rejection, climate and water**

Compare dry and wet heat rejection at explicitly labeled temperatures, check cooling electricity against the site ceiling, and distinguish redundant cooling from reduced-power operation after a fault.

**Driving question:** How do dry bulb, wet bulb and exchanger approach determine whether the rack receives cool enough liquid?

## Dry bulb measures the air; wet bulb reveals evaporative opportunity

Dry-bulb temperature is ordinary air temperature, measured with the sensor shaded from radiation and kept dry. A ventilated wet-bulb sensor has a wetted covering. Evaporation cools it below the dry bulb when the air is unsaturated; the two readings meet at saturation. Wetter air offers less evaporative cooling at the same dry-bulb temperature. Wet bulb is an air condition, not the temperature of the water pipe and not a separate outdoor thermometer measuring colder air.

A conventional dry cooler transferring heat from water to outdoor air needs the cooled water to remain warmer than the entering air at finite duty. Evaporative rejection can cool water below that air’s dry-bulb temperature because evaporation carries energy into water vapor. A conventional cooling tower approaches the entering wet-bulb temperature instead. This is why a hot, dry day can support a wet-cooling mode that a similarly hot, humid day cannot.

Neither temperature is a complete equipment rating. Duty also depends on flow, liquid properties, exchanger capability, fouling and the operating mode. The temperatures below are original teaching inputs. A real selection uses the relevant equipment performance data and local design conditions, not these numerical differences as rules of thumb.

## Approach belongs to two named temperature points

For a cooling tower, approach is leaving-water temperature minus entering-air wet bulb. For the dry cooler in our example, we explicitly use leaving-fluid temperature minus entering-air dry bulb. At the liquid-to-liquid CDU, the chip-cooling example uses technology supply, meaning the rack coolant supply, minus facility supply. State the equipment and the two sensor locations every time: approach is not one universal gap that can be copied between all three.

Loop temperature rise compares warm return with cool supply in one circuit. The same circuit can rise by 10 K across its load while its cooler operates at a 3 K or 5 K approach to another temperature. At the tower the inlet-to-outlet drop is called range. Approach can change with load, flow and equipment configuration; a smaller value at one operating point is not a guaranteed value across the operating envelope.

## Trace one 84 kW load through the two outdoor options

Take an 84 kW load carried by water loops at 2 kg/s with heat capacity 4.2 kJ/(kg·K), so each loop rises by 84 ÷ (2 × 4.2) = 10 K. Require technology supply at or below 35°C, and stipulate a 5 K CDU approach. For this comparison only, specify outdoor air at 35°C dry bulb and 22°C wet bulb. In the wet route chosen here, open-tower water is kept separate from the facility loop, so this design includes another heat exchanger. Count that interface when comparing the complete routes.

Dry route: stipulate a 5 K dry-cooler approach at this load. Its 35°C entering air permits a modeled 40°C facility supply. The CDU’s additional 5 K makes technology supply 45°C, above the 35°C requirement. The full steady temperature pairs would be facility 40°C supply / 50°C return and technology 45°C supply / 55°C return. This is a failed temperature screen, not permission to operate the rack at that point.

Wet route: stipulate a 3 K tower approach, so 22°C wet bulb gives 25°C tower outlet water. A separate counterflow exchanger with a stipulated 5 K approach gives 30°C facility supply. The CDU adds its 5 K to give 35°C technology supply. Label every loop: tower 25°C supply / 35°C return; facility 30°C / 40°C; technology 35°C / 45°C. Both ends of each counterflow exchanger retain a 5 K difference. The additional separating exchanger has been counted rather than hidden.

For this temperature comparison, all circulating-water rates are approximated as 2 kg/s; pump heat and the small flow change caused by evaporation are excluded. Every exchanger is stipulated to transfer 84 kW at its stated point. The tower’s water makeup and blowdown need their own ledger. These 3 K and 5 K approaches are example inputs; real values come from equipment performance data. Meeting the temperature screen alone does not establish capacity reserve, control behavior or a complete plant design.

## Change humidity without changing the dry bulb

Now hold dry bulb at 35°C and raise wet bulb from 22°C to 28°C. In the same stipulated fixed-approach screen, the wet route gives 28 + 3 + 5 + 5 = 41°C technology supply. It now fails the 35°C requirement. The dry route is still screened against 35°C dry bulb. The outdoor air thermometer did not change, but the evaporative option lost its useful temperature advantage.

A different exchanger selection, colder weather, a qualified warmer IT inlet, a reduced heat load or mechanical refrigeration could change the answer. An adiabatic dry cooler must count the wet-pad outlet temperature and the coil approach rather than simply substitute wet bulb for dry bulb. No finite pad automatically reaches the inlet wet bulb. A chiller can maintain a colder load circuit by doing work; its condenser must then reject the load heat plus that work.

## Two ceilings must survive the same hot hour

Consider a site with 10 MW of available electrical input. Its non-cooling overhead is 0.4 MW. In our synthetic model, cooling input equals IT heat divided by a stated plant COP; that ratio includes every cooling electrical load used in this exercise. We assume IT heat equals IT power at the modeled evaporator boundary. Writing PIT for IT power, the site inequality is PIT + PIT/COP + 0.4 ≤ 10 MW. This accounting avoids applying a yearly efficiency average to a particular hour.

In the cool condition the plant COP is eight and available thermal duty is 9 MW. In the hot condition the plant COP is four and thermal duty is 8.5 MW. At a proposed 8 MW IT load, the hot plant can remove the heat, but it consumes 2 MW doing so. The complete site then requires 10.4 MW. Thermal capacity alone says yes; the electrical balance says no. Reducing the IT load to 7.68 MW satisfies the hot electrical limit before the thermal ceiling is reached.

The result is a coupled constraint, not a penalty that can be assigned twice. First calculate feasible IT power from the electrical balance, then compare that result with available thermal duty and every other relevant ceiling. If a real performance curve changes COP with load, this simple division is no longer exact. Solve the electrical and thermal conditions together using the supplied load-dependent values rather than holding a favorable COP constant while changing its operating point.

## A cooling fault changes the available operating envelope

Cooling redundancy asks which complete heat-removal path survives a specified failure. An extra CDU pump can preserve circulation after that pump fails; it does not duplicate the shared heat exchanger, electrical feed, header or outdoor plant. Apply the N+1 and 2N redundancy reasoning from the uninterruptible power supply (UPS) lesson to the actual cooling boundary, at the required flow and temperatures. The Open Compute Project's modular cooling guidance connects loop boundaries with electrical failure scope and treats additional CDU capacity as useful when it serves a defined redundancy or maintenance requirement.

Power reduction is another response, with a different outcome: less heat is generated and less computing work may be delivered. NVIDIA separates temperature-triggered clock reduction on a graphics processing unit (GPU) from a configured power ceiling. A GPU cap is not automatically a cap on the complete rack. Coordinated controls can act on facility signals before waiting for chip protection: Dell's event guide explicitly describes liquid-cooling alerts triggering Emergency Power Reduction by throttling or shutdown. Such integration must be configured and its response demonstrated.

Return to the chip-cooling chapter’s fault example: suppose this liquid path captures 1,000 kW but its surviving route is stipulated to support only 600 kW at the permitted temperatures. If 1,000 kW continues entering while only 600 kW leaves, stored thermal energy rises at 400 kJ/s. Reducing captured heat to 500 kW brings demand below that stated capability. This is a candidate reduced-service state; the capacity screen alone does not establish chip temperatures, branch flow, control response or the performance delivered to users.

Complete loss of useful circulation needs a different analysis. The steady-flow heat equation cannot give a safe operating power or time-to-overheat when flow is zero. Liquid and metal may buffer energy temporarily, but thermal protection does not guarantee continued service. A leak can also require isolation and shutdown even while some cooling remains. NVIDIA's rack-management documentation separates the building management system (BMS), which isolates a leaking rack by cutting its power and closing its coolant valve, from supervisory handling. Restore a validated heat path or follow the specified protective response; an arbitrary power cap does not repair the fault.

## A useful weather model retains timing

An annual climate average hides the duration and coincidence of demanding conditions. A plant may face high ambient temperature when workloads are also heavy, or water restrictions may eliminate a mode assumed available by the energy calculation. For an estimate, divide a supplied time trace into operating bins and integrate the corresponding input. If switching, hysteresis or thermal storage matters, preserve the sequence instead of treating bins as interchangeable hours.

Take a twelve-hour cool period followed by twelve hot hours. In the cool bin the electrical ceiling is (10 − 0.4)/(1 + 1/8) = 8.53 MW, below the 9 MW thermal limit, so the proposed 8 MW of IT runs with 0.53 MW to spare. In the hot bin the site runs at its 7.68 MW ceiling. Both loads are dispatch choices, not measured application demand. The resulting IT energy is 188.16 MWh; cooling uses 35.04 MWh; non-cooling overhead adds 9.6 MWh. Their sum is 232.8 MWh. The reduction in IT work cannot be quantified without a workload model.

An economizer, thermal store or higher supply temperature might alter this result. Each proposal must say which equation or constraint it changes and what additional resource it consumes. A heat-reuse customer is similarly conditional: it must accept the available temperature and heat at the required times. A receiving building that needs little summer heat does not remove the obligation to reject a summer data-center load.

## Worked example: A complete hot-hour power balance

- All values are synthetic, with constant COP within each declared bin.
- Site limit 10 MW; non-cooling overhead 0.4 MW. Cool COP 8 and thermal limit 9 MW; hot COP 4 and thermal limit 8.5 MW.
- IT power becomes the modeled cooling duty; cooling input includes all plant auxiliaries.

1. Proposed hot load — 8 + 8/4 + 0.4 = 10.4 MW — Eight megawatts fits the thermal envelope but exceeds the site electrical limit.
2. Electrical IT ceiling — PIT ≤ (10 − 0.4)/(1 + 1/4) = 7.68 MW — Rearrange the full power budget instead of subtracting a cooling load calculated at a different IT load.
3. Check thermal ceiling — min(7.68, 8.5) = 7.68 MW — The electrical budget is binding for this hot condition.

**Result:** The feasible hot-bin IT ceiling is 7.68 MW in this model.

**Model boundary:** No real climate, product curve or control stability is represented. Other site constraints may reduce the feasible load further.

## The tradeoff

Choice: Retain compressor capacity for unfavorable outdoor conditions.

Benefit: It can widen the temperature envelope in which the required cooling duty is achievable.

Cost: Its electricity counts against the same site limit. In the hot hour at COP 4, cooling 8 MW of IT draws 2 MW, and the site needs 10.4 MW against its 10 MW supply.

## When the situation changes

Trigger: An annual PUE is used to authorize a high-load hot-weather operating point.

Mechanism: The average conceals a higher cooling demand during the constrained hour.

Response: Recompute the constrained hour with its own COP. At COP 4 the 10 MW site supports at most (10 − 0.4)/(1 + 1/4) = 7.68 MW of IT.

## Apply the idea

A revised synthetic hot mode has COP 5 but only 7.5 MW thermal capacity. What now limits IT under the same 10 MW site limit and 0.4 MW overhead?

<details>
<summary>Reveal the worked answer</summary>

The electrical ceiling is 9.6/1.2 = 8 MW, but thermal capacity limits IT to 7.5 MW.

Better COP frees electrical headroom, but it does not repair the separate heat-removal ceiling. At 7.5 MW IT, site input is 7.5 + 1.5 + 0.4 = 9.4 MW. The unused 0.6 MW cannot support additional IT without increasing the thermal capability or changing the stated conditions.

</details>

**The idea to keep:** Follow the temperature difference at every interface. Dry bulb, wet bulb, loop rise and approach answer different questions.

## Sources

- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — ASHRAE · Published 2023 · Reviewed 2026-09-11. Data-center cooling choices depend on outdoor environmental conditions and on the system they serve.
- [Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) — U.S. Department of Energy, Federal Energy Management Program · Published 2024-07-26 · Reviewed 2026-09-06. The overview identifies environmental conditions, cooling and heat recovery as connected design subjects.
- [National Weather Service — Dry Bulb, Wet Bulb, and Dew Point Temperatures](https://www.weather.gov/source/zhu/ZHU_Training_Page/definitions/dry_wet_bulb_definition/dry_wet_bulb.html) — National Weather Service · Reviewed 2026-09-17. Dry-bulb and ventilated wet-bulb measurement definitions; evaporation lowers wet-bulb temperature in unsaturated air, with equality at saturation.
- [ASHRAE Handbook 2024 — Cooling Towers](https://handbook.ashrae.org/Handbooks/S24/IP/s24_ch40/s24_ch40_ip.aspx) — ASHRAE · Published 2024 · Reviewed 2026-09-26. Tower range compares entering and leaving water; tower approach compares leaving water with entering-air wet bulb. Performance depends on the stated heat load, flow and air conditions; closed-circuit towers separate process liquid from spray water.
- [Vertiv — Optimizing Chilled Water Systems, July 2024](https://www.vertiv.com/495988/globalassets/shared/vertiv-chilled-water-solution-white-paper-sl-18066.pdf) — Vertiv · Published 2024-07 · Reviewed 2026-09-11. Adiabatic systems precool entering air through wet pads ahead of the coils; their water use depends on when the controls enable wet operation.
- [NVIDIA System Management Interface — thermal slowdown, shutdown and power limits](https://docs.nvidia.com/deploy/nvidia-smi/index.html) — NVIDIA · Reviewed 2026-09-11. nvidia-smi reports temperature-triggered clock reduction, shutdown temperature thresholds and configured power limits as separate quantities.
- [Dell PowerEdge event guide — liquid-cooling and temperature-triggered Emergency Power Reduction](https://www.dell.com/support/manuals/en-us/poweredge-xe9780/error_event_message_guide_c/cpwrpower-configuration-event-messages?guid=guid-3683ef35-10cc-4072-b1bb-e0f44ffcc67f&lang=en-us) — Dell Technologies · Reviewed 2026-09-11. CPWR0139 identifies liquid-cooling-alert-triggered power throttling or shutdown; CPWR0050 and CPWR0131 describe temperature-triggered group EPR. CPWR0026 and CPWR0177 document failed action paths.
- [NVIDIA Infra Controller — Leak Detection and Handling](https://docs.nvidia.com/infra-controller/documentation/operations-day-2/leak-detection-handling) — NVIDIA · Reviewed 2026-09-11. Separates BMS electrical and liquid isolation from infrastructure-management handling of critical, severe and general leaks, and lists the integration each requires.
- [OCP — Modular Technology Cooling Systems, Revision 1](https://www.opencompute.org/documents/ocp-modular-tcs-rev-1-final-2025-pdf) — Open Compute Project · Reviewed 2026-09-11. Sections 3.7–3.8 connect electrical and cooling boundaries, redundancy/maintainability, and branch flow; Appendix A and the service-level framework discuss failure scope and response expectations.
