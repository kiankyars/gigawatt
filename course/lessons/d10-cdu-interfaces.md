# Two liquid loops exchange heat, not fluid

**11. Chip and rack heat capture**

Label a liquid-to-liquid CDU, distinguish loop rise from approach, and read a real 2 MW CoolIT example against its stated conditions.

**Driving question:** What does a CDU do, and why is loop temperature rise different from approach temperature?

## Draw two closed loops with four temperatures

A liquid-to-liquid coolant distribution unit places a heat exchanger between the technology coolant system, the rack coolant loop serving information technology (IT) equipment, and the facility water system carrying heat toward the plant. In normal operation the liquids remain separated; heat crosses the exchanger surface. The technology side can have its own pumps, controls and fluid requirements. This separation allows the two circuits to have different pressure, chemistry and flow conditions within the equipment’s specifications. It does not make either circuit independent of the other’s thermal performance.

Label technology supply going toward the rack and technology return coming back hot. Separately label facility supply entering the CDU and facility return leaving warmer. A load-side temperature rise is technology return minus technology supply. The approach convention used here is technology supply minus facility supply, matching the Open Compute Project (OCP) CDU paper. These differences connect different points. Calling both of them delta T without a diagram invites a serious reasoning error.

## Follow the rack connections, not just the cabinet

In the GB300 cold-plate example, the CDU supplies technology coolant to rack manifolds. Quick-disconnect connections carry it to the trays and their cold plates; the return manifold takes warmed coolant back to the CDU. Lenovo documents top- and bottom-feed manifold options and in-rack or in-row CDU connections. NVIDIA’s exploded rear view of the DGX GB300 rack, below, labels the liquid-cooling manifolds and their FD83 hose connectors separately from the power bus bar and cable cartridges.

A rear-door heat exchanger is different: its coil takes heat from rack exhaust air. Depending on the installation, the door may use compatible facility water directly or a secondary coolant loop through a CDU. Calling the GB300 cold-plate loop technology coolant is correct for this two-loop architecture; it does not establish that every rear-door water circuit has a CDU.

![Exploded rear view of an NVIDIA DGX GB300 rack labeling the power bus bar, the liquid-cooling manifolds with FD83 hose connectors, cable cartridges, power cable management, rear bezel and seismic bracing.](../assets/references/nvidia-dgx-gb300-rear.png)

NVIDIA DGX GB300 rack, exploded rear view. Two vertical liquid-cooling manifolds with FD83 hose connectors run beside the power bus bar. [NVIDIA DGX GB Rack Scale Systems, hardware guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)

## Finite heat transfer requires a temperature difference

A heat exchanger cannot move a finite heat rate with zero driving temperature difference everywhere unless an unphysical infinite conductance is assumed. A simplified exchanger model uses heat rate equal to UA times an appropriate mean temperature difference, where U represents overall transfer behavior and A the effective area. For the special counterflow example below, both end differences are equal, so their common value is also the log-mean difference. General cases require the appropriate exchanger calculation and performance data.

If facility supply becomes warmer while heat load, flow rates and exchanger performance remain fixed, technology supply generally must rise to preserve the required driving difference. More facility cooling capacity in megawatts does not guarantee that the supply temperature is low enough. Likewise, a large CDU nameplate capacity is meaningful only at its rated fluid, flow and temperature conditions. Compare the required operating point with the supplier’s performance map, including the degraded condition that the service promises to survive.

## Controls manage the interface within physical limits

Controls observe temperature, flow, pressure and fault indications, then adjust the available actuators according to the specified design. A controller can alter pump speed or valve position where provided, but it cannot create unlimited exchanger conductance or make hot facility water behave like cold water. Control response also has a time scale. A rapid workload change can temporarily store heat in equipment and liquid before the next boundary responds. The acceptable excursion depends on the system’s thermal mass, flow and device limits.

Leak management and fluid compatibility belong to this same interface. A compatible fluid in an incompatible seal or mixed-metal circuit can create long-term problems even if initial temperature tests pass. Filters and cleanliness protect narrow passages but introduce pressure drop and maintenance needs. Quick disconnects change the service procedure and hydraulic circuit. The appropriate response to a leak or lost flow must be defined jointly by the IT and facility teams so that electrical shutdown, isolation and restoration preserve the intended safety and service conditions.

## A real row-scale CDU: CoolIT CHx2000

The CHx2000 is a freestanding, row-based liquid-to-liquid CDU serving a group of racks. Follow the hardware functions in order: pumps supply the pressure difference that drives technology coolant through piping, filters and cold plates; the heat exchanger transfers the collected heat into a separate facility circuit; sensors and controls adjust operation and report abnormal conditions. The cabinet needs facility-water connections and service access. It does not reject the heat outdoors itself. CoolIT also sells liquid-to-air CDUs, which transfer collected liquid heat into room air instead: CDU describes a function, not one universal destination for heat.

In September 2026, CoolIT’s product page listed 2,000 kW of cooling at a 5°C approach. The 2 MW is heat-transfer capacity, not electrical consumption and not a promise at every water temperature. In the CDU convention used here, a 5 K approach means that 30°C facility supply could correspond to 35°C technology supply at the applicable rated conditions. Those temperatures are illustrative; they are not a complete CHx2000 operating point. The rack-loop temperature rise is a different measurement, found from the sensible-heat balance using the actual load, coolant properties and flow.

Read the remaining specifications independently. The same page listed 2,125 L/min at 35 psi, a hydraulic operating point: useful flow must still be delivered against the loop’s resistance. It also listed 12.24 kW of electrical consumption without tying that figure to the same thermal and hydraulic condition. Do not divide these numbers to claim a measured system efficiency. Its April 2025 launch description identifies 25-micron filtration and serviceable pumps, filters and sensors. Filters keep contaminants away from narrow passages; accumulated debris raises resistance and creates a maintenance requirement. Match any installation to the current manufacturer selection data, including fluid, temperature, pressure and degraded-operation requirements.

## Count surviving cooling paths, not just spare cabinets

Redundancy can be built into pumps and power supplies inside a CDU, across a group of CDUs, or through facility pumps, chillers, heat rejection, piping, power and controls. These are different failure boundaries. NVIDIA’s DSX reference describes N+1 CDU groups with shared piping in mechanical galleries. That is a concrete example of group redundancy; it does not establish two independent facility-water paths.

In this example, a selected liquid heat load is 1,000 kW and each CDU is qualified for 600 kW at the stated fluid conditions. N is therefore two CDUs at the design duty, and three installed units give N+1. An independently isolated unit failure leaves 1,200 kW. The sum is usable only if the surviving branches, headers, pumps and outdoor plant can deliver the required conditions. Loss of their shared facility path defeats the heat-removal route despite healthy CDU cabinets. Spare units do not repair a failed common control panel or a leak in a shared manifold.

A separate 2N example has two upstream trains, each with two 600 kW CDU modules and independent facility-water, outdoor rejection, power and control paths. The model transfers the selected 1,000 kW demand to one compatible surviving train, so its displayed capacity is the larger surviving train capacity rather than A+B. The downstream load interface remains shared. A fault in that shared interface is outside the failure survived by this example; a 2N label at one boundary does not establish whole-campus fault tolerance.

If two of the three CDUs in the first example fail, 600 kW remains. A coordinated IT response is assumed to reduce heat entering that liquid path from 1,000 to 500 kW, leaving 100 kW of thermal capacity margin. This is a comparison of operating points, not a prediction that a controller can react before a temperature limit is reached. A real policy has to account for the hardware’s power scope, heat capture fraction, local flow and temperature limits, and confirmed achieved power. The heat-rejection section develops the distinction between that planned reduction, local thermal protection, and shutdown or isolation when no compatible cooling path remains.

## Choose a capture method against the complete brief

Consider a retrofit with an existing air system, limited floor space, a usable facility water loop and a requirement for routine component replacement. Retained air cooling might require lower density or more air-handling capacity. A rear-door exchanger can move exhaust heat into water while retaining server air paths. Cold plates can remove a declared fraction near the devices but leave residual air loads. Immersion changes the hardware qualification and service workflow more substantially. Evaluate each against actual temperature, fluid, pressure, access, compatibility and maintenance requirements.

The decision cannot be completed by selecting the largest stated cooling capacity. A cold-plate option that captures 85% of a 100 kW rack leaves 15 kW for air; that passes a 20 kW residual-air allowance arithmetically, with 5 kW to spare. It still needs qualified local temperatures and fluid interfaces. Adding a rear-door heat exchanger (RDHX) that captures all 15 kW would leave the room allowance untouched, because only air heat that passes the door counts against it; the door then needs its own airflow and water-side operating point. An immersion proposal with unknown component compatibility remains unresolved even if its heat capacity looks ample. Keep the unknowns visible until evidence closes them.

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

## Sources

- [Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) — Open Compute Project · Reviewed 2026-09-06. Defines approach as technology supply minus facility supply and rates performance with fluid and flow conditions.
- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — ASHRAE · Published 2023 · Reviewed 2026-09-11. The ASHRAE data-center chapter treats air and liquid cooling arrangements together with their environmental and facility interfaces.
- [CoolIT Systems — CHx2000 Row-Based CDU for AI](https://www.coolitsystems.com/cdu-product/chx2000/) — CoolIT Systems · Reviewed 2026-09-11. CHx2000 row-based liquid-to-liquid CDU: 2,000 kW at a 5°C approach, 2,125 L/min at 35 psi and 12.24 kW of listed electrical consumption.
- [CoolIT Systems — Cooling Distribution Units](https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/) — CoolIT Systems · Reviewed 2026-09-11. CDU pumping, temperature-control and heat-transfer functions; distinction between liquid-to-liquid and liquid-to-air equipment.
- [CoolIT Systems — CHx2000 launch announcement, April 15, 2025](https://www.coolitsystems.com/resources/news/coolit-systems-announces-further-breakthroughs-in-row-based-coolant-distribution-unit-performance/) — CoolIT Systems · Published 2025-04-15 · Reviewed 2026-09-11. Dated identification of integrated filtration and service access for pumps, filters and sensors.
- [NVIDIA System Management Interface — thermal slowdown, shutdown and power limits](https://docs.nvidia.com/deploy/nvidia-smi/index.html) — NVIDIA · Reviewed 2026-09-11. The Clock Event Reasons, Temperature, GPU Power Readings and Module Power Readings sections distinguish temperature-triggered clock reduction, shutdown thresholds and configured power ceilings.
- [Dell PowerEdge event guide — liquid-cooling and temperature-triggered Emergency Power Reduction](https://www.dell.com/support/manuals/en-us/poweredge-xe9780/error_event_message_guide_c/cpwrpower-configuration-event-messages?guid=guid-3683ef35-10cc-4072-b1bb-e0f44ffcc67f&lang=en-us) — Dell Technologies · Reviewed 2026-09-11. CPWR0139 identifies liquid-cooling-alert-triggered power throttling or shutdown; CPWR0050 and CPWR0131 describe temperature-triggered group EPR. CPWR0026 and CPWR0177 document failed action paths.
- [OCP — Modular Technology Cooling Systems, Revision 1](https://www.opencompute.org/documents/ocp-modular-tcs-rev-1-final-2025-pdf) — Open Compute Project · Reviewed 2026-09-11. Sections 3.7–3.8 connect electrical and cooling boundaries, redundancy/maintainability, and branch flow; Appendix A and the service-level framework discuss failure scope and response expectations.
- [Vertiv — How N+1 redundancy supports continuous data center cooling](https://www.vertiv.com/en-ca/about/news-and-events/articles/educational-articles/how-n1-redundancy-supports-continuous-data-center-cooling/) — Vertiv · Published 2025-08-12 · Reviewed 2026-09-11. Defines cooling N, N+1 and 2N and distinguishes redundant units from shared power, water and control dependencies.
- [NVIDIA — DSX Facilities Infrastructure Reference Design Overview](https://docs.nvidia.com/dsx/facilities-infra/reference-design-overview) — NVIDIA · Published 2026-08-19 · Reviewed 2026-09-11. The mechanical-gallery CDU section specifies N+1 CDU groups with shared piping and separates the technical and facility-water loops.
- [NVIDIA DGX GB Rack Scale Systems — Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html#power-shelves) — NVIDIA · Reviewed 2026-09-17. Annotated GB300 rear hardware figure identifies cooling manifolds and liquid interfaces.
- [Lenovo NVIDIA GB300 NVL72 Rack Scale AI Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) — Lenovo Press · Published 2026-08-30 · Reviewed 2026-09-17. CDU inlet/return hoses, tray quick connections and top/bottom-feed rack manifolds.
- [Motivair — ChilledDoor rear-door heat exchanger](https://www.motivaircorp.com/products/chilleddoor/) — Motivair · Reviewed 2026-09-17. A rear-door exchanger can circulate compatible facility water through its coil.

## Check your understanding: The liquid loop is not the whole rack

Pause and make a prediction, then compare your reasoning.

A hypothetical 100 kW rack transfers 80 kW into its liquid loop and 20 kW into room air. Its liquid loop remains available, but the room's air-cooling path becomes unavailable.

**Pause and predict:** Can you claim the rack can keep running at 100 kW? Explain the remaining heat obligation.

<details>
<summary>Compare your reasoning</summary>

No. The 20 kW released to air still needs a working heat-removal path.

Adequate liquid capacity does not establish cooling for components whose heat enters the air. Without another demonstrated path, the supplied facts do not support continued full-load operation. Thermal limits and any allowable ride-through require additional evidence.

</details>

**The next problem:** Heat captured from the rack has only started its journey. How does it finally reach the outdoor environment?

Continue in **12. Heat rejection, climate and water**: The heat does not disappear at the chiller.
