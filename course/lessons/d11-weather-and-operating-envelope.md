# The same air temperature can create different cooling limits

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d11-weather-and-operating-envelope`, then run `uv run gigawatt-expand`.

**D11 · Authored draft · Objectives:** D11.1, D11.3, D11.5

Compare dry and wet heat rejection at explicitly labeled temperatures, then check cooling electricity against the site power ceiling.

**Driving question:** How do dry bulb, wet bulb and exchanger approach determine whether the rack receives cool enough liquid?

## Dry bulb measures the air; wet bulb reveals evaporative opportunity

Dry-bulb temperature is ordinary air temperature, measured with the sensor shaded from radiation and kept dry. A ventilated wet-bulb sensor has a wetted covering. Evaporation cools it below the dry bulb when the air is unsaturated; the two readings meet at saturation. Wetter air offers less evaporative cooling at the same dry-bulb temperature. Wet bulb is an air condition, not the temperature of the water pipe and not a separate outdoor thermometer measuring colder air.

A conventional dry cooler transferring heat from water to outdoor air needs the cooled water to remain warmer than the entering air at finite duty. Evaporative rejection can cool water below that air’s dry-bulb temperature because evaporation carries energy into water vapor. A conventional cooling tower approaches the entering wet-bulb temperature instead. This is why a hot, dry day can support a wet-cooling mode that a similarly hot, humid day cannot.

Neither temperature is a complete equipment rating. Duty also depends on flow, liquid properties, exchanger capability, fouling and the operating mode. The temperatures below are original teaching inputs. A real selection uses the relevant equipment performance data and local design conditions, not these numerical differences as rules of thumb.

## Approach belongs to two named temperature points

For a cooling tower, approach is leaving-water temperature minus entering-air wet bulb. For the dry cooler in our example, we explicitly use leaving-fluid temperature minus entering-air dry bulb. At the liquid-to-liquid CDU, D10 uses technology supply minus facility supply. State the equipment and the two sensor locations every time: approach is not one universal gap that can be copied between all three.

Loop temperature rise compares warm return with cool supply in one circuit. The same circuit can rise by 10 K across its load while its cooler operates at a 3 K or 5 K approach to another temperature. At the tower the inlet-to-outlet drop is called range. Approach can change with load, flow and equipment configuration; a smaller value at one operating point is not a guaranteed value across the operating envelope.

## Trace one 84 kW load through the two outdoor options

Reuse D10’s synthetic 84 kW load and 2 kg/s water loops with heat capacity 4.2 kJ/(kg·K), giving a 10 K temperature rise. Require technology supply at or below 35°C, and stipulate a 5 K CDU approach. For this comparison only, specify outdoor air at 35°C dry bulb and 22°C wet bulb. In the wet route chosen here, open-tower water is kept separate from the facility loop, so this design includes another heat exchanger. Count that interface when comparing the complete routes.

Dry route: stipulate a 5 K dry-cooler approach at this load. Its 35°C entering air permits a modeled 40°C facility supply. The CDU’s additional 5 K makes technology supply 45°C, above the 35°C requirement. The full steady temperature pairs would be facility 40°C supply / 50°C return and technology 45°C supply / 55°C return. This is a failed temperature screen, not permission to operate the rack at that point.

Wet route: stipulate a 3 K tower approach, so 22°C wet bulb gives 25°C tower outlet water. A separate counterflow exchanger with a stipulated 5 K approach gives 30°C facility supply. The CDU adds its 5 K to give 35°C technology supply. Label every loop: tower 25°C supply / 35°C return; facility 30°C / 40°C; technology 35°C / 45°C. Both ends of each counterflow exchanger retain a 5 K difference. The additional separating exchanger has been counted rather than hidden.

For this temperature comparison, all circulating-water rates are approximated as 2 kg/s; pump heat and the small flow change caused by evaporation are excluded. Every exchanger is stipulated to transfer 84 kW at its stated point. The tower’s water makeup and blowdown need their own ledger. These 3 K and 5 K approaches are invented inputs, not standard equipment performance. Meeting the temperature screen alone does not establish capacity reserve, control behavior or a complete plant design.

## Change humidity without changing the dry bulb

Now hold dry bulb at 35°C and raise wet bulb from 22°C to 28°C. In the same stipulated fixed-approach screen, the wet route gives 28 + 3 + 5 + 5 = 41°C technology supply. It now fails the 35°C requirement. The dry route is still screened against 35°C dry bulb. The outdoor air thermometer did not change, but the evaporative option lost its useful temperature advantage.

A different exchanger selection, colder weather, a qualified warmer IT inlet, a reduced heat load or mechanical refrigeration could change the answer. An adiabatic dry cooler must count the wet-pad outlet temperature and the coil approach rather than simply substitute wet bulb for dry bulb. No finite pad automatically reaches the inlet wet bulb. A chiller can maintain a colder load circuit by doing work; its condenser must then reject the load heat plus that work.

## Two ceilings must survive the same hot hour

Consider a site with 10 MW of available electrical input. Its non-cooling overhead is 0.4 MW. In our synthetic model, cooling input equals IT heat divided by a stated plant COP; that ratio includes every cooling electrical load used in this exercise. We assume IT heat equals IT power at the modeled evaporator boundary. The site inequality is therefore PIT + PIT/COP + 0.4 ≤ 10 MW. This accounting avoids applying a yearly efficiency average to a particular hour.

In the cool condition the plant COP is eight and available thermal duty is 9 MW. In the hot condition the plant COP is four and thermal duty is 8.5 MW. At a proposed 8 MW IT load, the hot plant can remove the heat, but it consumes 2 MW doing so. The complete site then requires 10.4 MW. Thermal capacity alone says yes; the electrical balance says no. Reducing the IT load to 7.68 MW satisfies the hot electrical limit before the thermal ceiling is reached.

The result is a coupled constraint, not a penalty that can be assigned twice. First calculate feasible IT power from the electrical balance, then compare that result with available thermal duty and every other relevant ceiling. If a real performance curve changes COP with load, this simple division is no longer exact. Solve the electrical and thermal conditions together using the supplied load-dependent values rather than holding a favorable COP constant while changing its operating point.

## A useful weather model retains timing

An annual climate average hides the duration and coincidence of demanding conditions. A plant may face high ambient temperature when workloads are also heavy, or water restrictions may eliminate a mode assumed available by the energy calculation. For an estimate, divide a supplied time trace into operating bins and integrate the corresponding input. If switching, hysteresis or thermal storage matters, preserve the sequence instead of treating bins as interchangeable hours.

For a twelve-hour cool period followed by twelve hot hours, the synthetic site can sustain 8 MW IT in the cool bin and 7.68 MW in the hot bin. That is a capacity-limited dispatch assumption, not measured application demand. The resulting IT energy is 188.16 MWh; cooling uses 35.04 MWh; non-cooling overhead adds 9.6 MWh. Their sum is 232.8 MWh. The reduction in IT work cannot be quantified without a workload model.

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

Cost: Its electricity, capital, maintenance and rejection duty must be included, even if it operates infrequently.

## When the situation changes

Trigger: An annual PUE is used to authorize a high-load hot-weather operating point.

Mechanism: The average conceals a higher cooling demand during the constrained hour.

Response: Reconcile time-aligned load, ambient and equipment performance, then compare feasible operating responses within validated limits.

## Apply the idea

A revised synthetic hot mode has COP 5 but only 7.5 MW thermal capacity. What now limits IT under the same 10 MW site limit and 0.4 MW overhead?

<details>
<summary>Reveal the worked answer</summary>

The electrical ceiling is 9.6/1.2 = 8 MW, but thermal capacity limits IT to 7.5 MW.

Better COP frees electrical headroom, but it does not repair the separate heat-removal ceiling. At 7.5 MW IT, site input is 7.5 + 1.5 + 0.4 = 9.4 MW. The unused 0.6 MW cannot support additional IT without increasing the thermal capability or changing the stated conditions.

</details>

**The idea to keep:** Follow the temperature difference at every interface. Dry bulb, wet bulb, loop rise and approach answer different questions.

## Sources and reading boundaries

- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — Selected discussion supports the dependence of cooling choices on environmental and system conditions. Read 2026-09-06. No equipment curve or universal economizer threshold is taken from this chapter; all operating-bin numbers are original hypothetical inputs.
- [Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) — The overview identifies environmental conditions, cooling and heat recovery as connected design subjects. Read 2026-09-06. Landing-page scope reviewed; no claim to have audited every linked design recommendation. Synthetic energy calculations are independent.
- [National Weather Service — Dry Bulb, Wet Bulb, and Dew Point Temperatures](https://www.weather.gov/source/zhu/ZHU_Training_Page/definitions/dry_wet_bulb_definition/dry_wet_bulb.html) — Dry-bulb and ventilated wet-bulb measurement definitions; evaporation lowers wet-bulb temperature in unsaturated air, with equality at saturation. Read 2026-09-11. Definitions reviewed. The lesson supplies its own paired weather values; they are not a weather observation, equipment rating or heat-stress threshold.
- [ASHRAE Handbook 2024 — Cooling Towers](https://handbook.ashrae.org/Handbooks/S24/IP/s24_ch40/s24_ch40_ip.aspx) — Tower range compares entering and leaving water; tower approach compares leaving water with entering-air wet bulb. Performance depends on the stated heat load, flow and air conditions; closed-circuit towers separate process liquid from spray water. Read 2026-09-11. Selected mechanism, terminology, closed-circuit and performance-curve sections reviewed. No handbook example approach, capacity or water-saving percentage is adopted as a universal design value.
- [Vertiv — Optimizing Chilled Water Systems, July 2024](https://www.vertiv.com/495988/globalassets/shared/vertiv-chilled-water-solution-white-paper-sl-18066.pdf) — The Adiabatic System section explains evaporative air precooling through wet pads ahead of coils and control-dependent water use. Read 2026-09-11. Selected text on printed pages 6–7 reviewed. The claim of no additional energy cost and the simulated energy/WUE savings are not adopted; fans, pumps and controls retain their declared electricity boundary.
