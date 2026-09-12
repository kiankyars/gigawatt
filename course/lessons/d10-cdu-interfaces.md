# Two liquid loops exchange heat, not fluid

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d10-cdu-interfaces`, then run `uv run gigawatt-expand`.

**D10 · Authored draft · Objectives:** D10.2, D10.3, D10.4

Label a liquid-to-liquid CDU, distinguish loop rise from approach, and read a real 2 MW CoolIT example against its stated conditions.

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

## A real row-scale CDU: CoolIT CHx2000

The CHx2000 is a freestanding, row-based liquid-to-liquid CDU serving a group of racks. Follow the hardware functions in order: pumps supply the pressure difference that drives technology coolant through piping, filters and cold plates; the heat exchanger transfers the collected heat into a separate facility circuit; sensors and controls adjust operation and report abnormal conditions. The cabinet needs facility-water connections and service access. It does not reject the heat outdoors itself. CoolIT also sells liquid-to-air CDUs, which transfer collected liquid heat into room air instead: CDU describes a function, not one universal destination for heat.

CoolIT’s current product page lists 2,000 kW of cooling at a 5°C approach. The 2 MW is heat-transfer capacity, not electrical consumption and not a promise at every water temperature. In the CDU convention used here, a 5 K approach means that 30°C facility supply could correspond to 35°C technology supply at the applicable rated conditions. Those temperatures are illustrative; they are not a complete CHx2000 operating point. The rack-loop temperature rise is a different measurement, found from the sensible-heat balance using the actual load, coolant properties and flow.

Read the remaining specifications independently. The current page lists 2,125 L/min at 35 psi, a hydraulic operating point: useful flow must still be delivered against the loop’s resistance. It also lists 12.24 kW electrical consumption without tying that figure to the same thermal and hydraulic condition. Do not divide these numbers to claim a measured system efficiency. Its April 2025 launch description identifies 25-micron filtration and serviceable pumps, filters and sensors. Filters keep contaminants away from narrow passages; accumulated debris raises resistance and creates a maintenance requirement. Match any installation to the current manufacturer selection data, including fluid, temperature, pressure and degraded-operation requirements.

## Count surviving cooling paths, not just spare cabinets

Redundancy can be built into pumps and power supplies inside a CDU, across a group of CDUs, or through facility pumps, chillers, heat rejection, piping, power and controls. These are different failure boundaries. NVIDIA’s DSX reference describes N+1 CDU groups with shared piping in mechanical galleries. That is a concrete example of group redundancy; it does not establish two independent facility-water paths. The current CoolIT CHx2000 page is not used to assign an N+1 pump arrangement.

In the original teaching example, a selected liquid heat load is 1,000 kW and each CDU is qualified for 600 kW at the stated fluid conditions. N is therefore two CDUs at the design duty, and three installed units give N+1. An independently isolated unit failure leaves 1,200 kW. The sum is usable only if the surviving branches, headers, pumps and outdoor plant can deliver the required conditions. Loss of their shared facility path defeats the heat-removal route despite healthy CDU cabinets. Spare units do not repair a failed common control panel or a leak in a shared manifold.

A separate 2N example has two upstream trains, each with two 600 kW CDU modules and independent facility-water, outdoor rejection, power and control paths. The model transfers the selected 1,000 kW demand to one compatible surviving train, so its displayed capacity is the larger surviving train capacity rather than A+B. The downstream load interface remains shared. A fault in that shared interface is outside the failure survived by this example; a 2N label at one boundary does not establish whole-campus fault tolerance.

If two of the three CDUs in the first example fail, 600 kW remains. A coordinated IT response is assumed to reduce heat entering that liquid path from 1,000 to 500 kW, leaving 100 kW of thermal capacity margin. This is a comparison of operating points, not a prediction that a controller can react before a temperature limit is reached. A real policy has to account for the hardware’s power scope, heat capture fraction, local flow and temperature limits, and confirmed achieved power. D11 develops the distinction between that planned reduction, local thermal protection, and shutdown or isolation when no compatible cooling path remains.

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
- [CoolIT Systems — CHx2000 Row-Based CDU for AI](https://www.coolitsystems.com/cdu-product/chx2000/) — Official product type, current thermal and hydraulic claims, listed electrical consumption, and manufacturer photographs. Read 2026-09-11. The separately listed thermal, hydraulic and electrical figures do not establish one simultaneous operating point. Vendor superiority, rack-count, availability and factory-test claims are not adopted. The mutable page differs from older product collateral.
- [CoolIT Systems — Cooling Distribution Units](https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/) — CDU pumping, temperature-control and heat-transfer functions; distinction between liquid-to-liquid and liquid-to-air equipment. Read 2026-09-11. Portfolio mechanism descriptions only; product capacity does not establish suitability for a particular facility.
- [CoolIT Systems — CHx2000 launch announcement, April 15, 2025](https://www.coolitsystems.com/resources/news/coolit-systems-announces-further-breakthroughs-in-row-based-coolant-distribution-unit-performance/) — Dated identification of integrated filtration and service access for pumps, filters and sensors. Read 2026-09-11. 2025 product description. Comparative performance, availability and footprint-density claims are not reused as current specifications. Current procurement needs current selection data.
- [NVIDIA System Management Interface — thermal slowdown, shutdown and power limits](https://docs.nvidia.com/deploy/nvidia-smi/index.html) — The Clock Event Reasons, Temperature, GPU Power Readings and Module Power Readings sections distinguish temperature-triggered clock reduction, shutdown thresholds and configured power ceilings. Read 2026-09-11. Selected definitions reviewed. Support and limits vary by device. This does not specify liquid-cooling fault response time, safe operation without flow, or a universal cap-to-performance relationship.
- [Dell PowerEdge event guide — liquid-cooling and temperature-triggered Emergency Power Reduction](https://www.dell.com/support/manuals/en-us/poweredge-xe9780/error_event_message_guide_c/cpwrpower-configuration-event-messages?guid=guid-3683ef35-10cc-4072-b1bb-e0f44ffcc67f&lang=en-us) — CPWR0139 identifies liquid-cooling-alert-triggered power throttling or shutdown; CPWR0050 and CPWR0131 describe temperature-triggered group EPR. CPWR0026 and CPWR0177 document failed action paths. Read 2026-09-11. Selected event definitions reviewed, not a tested installation or universal implementation. Feature support, licensing, communications and target response matter; no reaction time or achieved cooling protection is inferred.
- [OCP — Modular Technology Cooling Systems, Revision 1](https://www.opencompute.org/documents/ocp-modular-tcs-rev-1-final-2025-pdf) — Sections 3.7–3.8 connect electrical and cooling boundaries, redundancy/maintainability, and branch flow; Appendix A and the service-level framework discuss failure scope and response expectations. Read 2026-09-11. Selected sections reviewed. The course does not adopt universal flow rules, numerical reliability estimates, or the document's inconsistently written energy/flow units. Synthetic examples are original.
- [Vertiv — How N+1 redundancy supports continuous data center cooling](https://www.vertiv.com/en-ca/about/news-and-events/articles/educational-articles/how-n1-redundancy-supports-continuous-data-center-cooling/) — Define cooling N, N+1 and 2N and distinguish redundant units from shared power, water and control dependencies. Read 2026-09-11. Definitions and shared-dependency discussion reviewed. No prevalence, Tier mapping or blanket continuity guarantee adopted; capacity and connectivity require a particular design and operating conditions.
- [NVIDIA — DSX Facilities Infrastructure Reference Design Overview](https://docs.nvidia.com/dsx/facilities-infra/reference-design-overview) — The mechanical-gallery CDU section specifies N+1 CDU groups with shared piping and separates the technical and facility-water loops. Read 2026-09-11. Selected CDU and gallery sections reviewed in mutable HTML. One reference design does not prove site deployment, independent facility-water paths or the ratings and response time of the synthetic course example.
