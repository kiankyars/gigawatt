# Two liquid loops exchange heat, not fluid

**D10 · Authored draft · Objectives:** D10.2, D10.3, D10.4

Label a liquid-to-liquid CDU, solve its thermal interfaces and compare cooling choices against a retrofit service brief.

**Driving question:** What does a CDU do, and why is loop temperature rise different from approach temperature?

## Draw two closed loops with four temperatures

A liquid-to-liquid coolant distribution unit places a heat exchanger between the technology coolant system serving IT equipment and the facility water system carrying heat toward the plant. In normal operation the liquids remain separated; heat crosses the exchanger surface. The technology side can have its own pumps, controls and fluid requirements. This separation allows the two circuits to have different pressure, chemistry and flow conditions within the equipment’s specifications. It does not make either circuit independent of the other’s thermal performance.

Label technology supply going toward the rack and technology return coming back hot. Separately label facility supply entering the CDU and facility return leaving warmer. A load-side temperature rise is technology return minus technology supply. The approach convention used here is technology supply minus facility supply, matching the OCP CDU paper. These differences connect different points. Calling both of them delta T without a diagram invites a serious reasoning error.

## Finite heat transfer requires a temperature difference

A heat exchanger cannot move a finite heat rate with zero driving temperature difference everywhere unless an unphysical infinite conductance is assumed. A simplified exchanger model uses heat rate equal to UA times an appropriate mean temperature difference, where U represents overall transfer behavior and A the effective area. For the special counterflow example below, both end differences are equal, so their common value is also the log-mean difference. General cases require the appropriate exchanger calculation and performance data.

If facility supply becomes warmer while heat load, flow rates and exchanger performance remain fixed, technology supply generally must rise to preserve the required driving difference. More facility cooling capacity in megawatts does not guarantee that the supply temperature is low enough. Likewise, a large CDU nameplate capacity is meaningful only at its rated fluid, flow and temperature conditions. Compare the required operating point with the supplier’s performance map, including the degraded condition that the service promises to survive.

## Controls manage the interface within physical limits

Controls observe temperature, flow, pressure and fault indications, then adjust the available actuators according to the specified design. A controller can alter pump speed or valve position where provided, but it cannot create unlimited exchanger conductance or make hot facility water behave like cold water. Control response also has a time scale. A rapid workload change can temporarily store heat in equipment and liquid before the next boundary responds. The acceptable excursion depends on the system’s thermal mass, flow and device limits.

Leak management and fluid compatibility belong to this same interface. A compatible fluid in an incompatible seal or mixed-metal circuit can create long-term problems even if initial temperature tests pass. Filters and cleanliness protect narrow passages but introduce pressure drop and maintenance needs. Quick disconnects change the service procedure and hydraulic circuit. The appropriate response to a leak or lost flow must be defined jointly by the IT and facility teams so that electrical shutdown, isolation and restoration preserve the intended safety and service conditions.

## Choose a capture method against the complete brief

Consider a retrofit with an existing air system, limited floor space, a usable facility water loop and a requirement for routine component replacement. Retained air cooling might require lower density or more air-handling capacity. A rear-door exchanger can move exhaust heat into water while retaining server air paths. Cold plates can remove a declared fraction near the devices but leave residual air loads. Immersion changes the hardware qualification and service workflow more substantially. Evaluate each against actual temperature, fluid, pressure, access, compatibility and maintenance requirements.

The decision cannot be completed by selecting the largest stated cooling capacity. A cold-plate option that captures 85% of a hypothetical 100 kW rack leaves 15 kW for air; that passes a 20 kW residual-air allowance arithmetically. It still needs qualified local temperatures and fluid interfaces. A rear-door option requires its own airflow and water-side operating point. An immersion proposal with unknown component compatibility remains unresolved even if its heat capacity looks ample. Keep the unknowns visible until evidence closes them.

## Worked example: A counterflow CDU with a five-kelvin approach

- A synthetic CDU transfers 84 kW between two water loops, each modeled at 2 kg/s and cp = 4.2 kJ/(kg·K).
- Technology supply/return are 35°C/45°C. Facility supply/return are 30°C/40°C. Pump heat and ambient losses are excluded.
- The exchanger is counterflow and modeled by fixed UA at this operating point.

1. Verify both loop rises — 84 / (2 × 4.2) = 10 K — Each liquid changes by 10 K while traversing its side of the transfer path.
2. Calculate approach — 35 − 30 = 5 K — This compares the two supply temperatures, not supply and return within one loop.
3. Check both exchanger end differences — 45 − 40 = 5 K; 35 − 30 = 5 K — Equal end differences give a 5 K mean driving difference in this special case.
4. Infer the synthetic conductance — UA = 84 / 5 = 16.8 kW/K — This is an illustrative effective conductance, not a real CDU rating.

**Result:** The loop temperature rise is 10 K while the approach is 5 K; both are correct because they compare different temperature points.

**Model boundary:** Real conductance varies with flows, fluids, fouling and exchanger behavior. This idealized example is not equipment selection.

## The tradeoff

Choice: Target a smaller approach at the same heat load.

Benefit: Potentially deliver cooler technology supply for a given facility supply temperature, or permit warmer facility water.

Cost: Require different exchanger performance, area, flow or operating conditions, with effects on cost, pressure drop and service design.

## When the situation changes

Trigger: Facility supply rises from 30°C to 34°C while the load and the example’s fixed-flow exchanger behavior remain unchanged.

Mechanism: Technology supply rises from 35°C to 39°C to preserve the five-kelvin driving difference; the CDU cannot hold its old supply temperature merely by retaining an 84 kW label.

Response: Compare the new temperature with the IT limit, coordinate a qualified load or plant response and verify the actual exchanger operating point.

## Apply the idea

The IT supply limit is 38°C. At 34°C facility supply and 84 kW load, what maximum approach is allowed, and what conductance would the equal-end-difference model require?

<details>
<summary>Reveal the worked answer</summary>

Approach must be at most 4 K. The simplified model requires UA of at least 84 / 4 = 21 kW/K, compared with the original 16.8 kW/K.

That is 25% more effective conductance at the specified equal-flow operating point. It does not prescribe a replacement size: an actual solution could change facility conditions, exchanger design, flow or permitted load, subject to all other interfaces.

</details>

**The idea to keep:** A CDU transfers heat across a finite temperature difference while managing a specified loop; the heat still needs a path out of the building.

## Sources and reading boundaries

- [Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) — Defines approach as technology supply minus facility supply and rates performance with fluid and flow conditions. Read 2026-09-06. Selected thermal, hydraulic, sensing and fluid-service sections reviewed. Synthetic conductance and temperatures are original; no product is qualified.
- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — Air and liquid arrangements must be considered with their environmental and facility interfaces. Read 2026-09-06. Selected public 2023 sections only; specific equipment and later requirements need separate review.
