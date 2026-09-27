# A rack must fit on its worst day

**5. Physical site, buildings and safety**

Separate white and gray space, equipment footprints, service and movement envelopes, and the loads actually applied to a structure.

**Driving question:** Why can a layout that fits every rack still be impossible to maintain?

## Draw three floor plans, not one

A footprint drawing answers a narrow question: can the equipment occupy this position? A service drawing asks whether doors, drawers, cables, hoses and lifting aids can move while nearby equipment remains available. A replacement drawing follows a component from its installed position through turns, thresholds, doors, staging areas and the loading route. These drawings overlap, but none can substitute for the others. The longest or heaviest replaceable object may determine feasibility more than the rack cabinet.

Apply the white/gray distinction from the opening lesson to the actual floor plan. The IT hall is white space; a separate supporting electrical room or mechanical gallery is gray space. A coolant distribution unit can be installed in either area, so its equipment name does not settle the classification. Vertiv’s mechanical-space guidance makes this placement choice explicit and requires room for service and replacement. Count access in the area where the equipment is actually placed.

Consider eight hypothetical racks, each 0.8 m wide and 1.2 m deep. Their combined footprint is 7.68 m². Now give the row a specified 1.5 m front service zone, 1.2 m rear zone and 1 m at each end. Its illustrative planning envelope becomes 8.4 m by 3.9 m, or 32.76 m². Those dimensions are supplied exercise inputs, not code requirements. The difference explains why dividing gross room area by cabinet footprint can overstate a useful layout dramatically.

Not every clearance must be permanently exclusive; some activities can share space at different times. That creates a scheduling and availability condition. If replacing rack A blocks the only access to rack B, the design should state which activity takes priority and whether both services remain supportable. A promise of maintainability is conditional on those actual routes, not just on the electrical single-line diagram.

Consider a converter removed from a rack. Putting it in a sidecar beside the rack can release rack mounting units while consuming white-space floor area and access. Moving it to a separate electrical room consumes gray-space area and may change cable routes. Which option reduces the total building footprint? Neither location alone answers that question. Compare both complete layouts, including the space that can actually be reused and the space newly required. A freed rack slot, a freed hall position, and a smaller building are three different claims.

## A real service object: Lenovo’s GB300 compute tray

Lenovo’s GB300 NVL72 documentation puts the configured rack solution at approximately 1,580 kg, with variation by configuration. Its product guide gives a 600 mm-wide MGX rack and a 29 kg compute tray, 799 mm deep including the rear water connections. These are two different handling jobs: moving a complete rack and replacing a tray. Plan the route, lifting equipment and service access for the object actually being moved.

The guide requires an on-site material lift to permit single-person tray service and names the Genie GL-8 and a ServerLift alternative. A floor plan must therefore accommodate the tray, the selected handling equipment, the technician’s access and the replacement route. The rear of each tray carries a water outlet and a water inlet quick disconnect at its two ends and a busbar clip in the middle, so removing a tray disconnects two coolant connections and its power connection. No universal aisle dimension or lifting procedure follows from these product specifications.

![Rear of a Lenovo GB300 compute tray: the water outlet quick disconnect at the left end, the busbar clip in the middle and the water inlet quick disconnect at the right end.](../assets/references/site-lenovo-gb300-compute-tray-rear.png)

Rear of a GB300 compute tray. Lenovo labels the water outlet and inlet quick disconnects (QD) and the busbar clip. [Lenovo — GB300 NVL72 Rack Scale AI Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai)

## A structure sees forces, locations and combinations

Mass becomes a gravitational force through W = mg. Lenovo’s complete GB300 NVL72 rack, at about 1,580 kg, weighs 1,580 × 9.81 = 15,500 N, or about 15.5 kN, using g = 9.81 m/s². Dividing that force by a cabinet footprint produces an average pressure, but it does not describe how feet, rails, spreader plates or casters transmit force to a raised floor and structural members. The local load path matters. So do the equipment operating state, attached piping, installation loads and support configuration.

An allowable uniformly distributed floor load is therefore not automatically a permitted wheel load. A moving rack can place substantial force onto a small number of contact points or cross a panel edge. Structural interpretation belongs to the supplied engineering criteria and qualified review. The worked example below therefore gives the route its own wheel limit. That limit is enough to reject a route; approving one takes the full structural review.

Increasing rack density can reduce the number of cabinets while increasing weight, cooling connections and the demands on handling equipment. NVIDIA’s H100 deployment guidance illustrates the wider principle: rack and layout choices can change cable lengths and other domains. Treat that product configuration as one example, and ask which interfaces must be recalculated when a cabinet changes.

## Treat the route as a chain of interfaces

Follow the same physical object throughout the journey. Its shipping dimensions may differ from operating dimensions, and temporary handling fixtures may widen it. A door can be wide enough while the turn beyond it is not. A lift can have adequate total capacity while the object’s shape prevents entry. A route may cross a space controlled by a different tenant or become unavailable during another phase of construction. Each is a distinct interface, with an owner and evidence.

For a replacement plan, record the object, mass, orientation, handling assembly, clear envelope, permitted loads and any temporary changes. Then identify dependencies on live services: cable trays overhead, coolant hoses nearby, fire access and the surviving maintenance path. The value of this record is that another person can examine the actual limiting step. A reassuring statement that the route was considered gives them little to verify.

You do not need a complete professional design to discover an incompatibility. Suppose the handling assembly rolls on four wheels and the route allows 3 kN per wheel. Shared among four wheels, the rack’s 15.5 kN averages about 3.9 kN per wheel. However unevenly the wheels share the load, at least one of them carries the average or more, so at least one exceeds 3 kN and the route fails. A trolley only adds weight. A pass would need more evidence: the actual load sharing, dynamic effects and structural details. This asymmetry is useful: limited evidence can reject a configuration decisively without being enough to approve it.

Extension: a heavier rack on a trolley. A 2,000 kg rack on a trolley that brings the moving assembly to 2,200 kg weighs 2,200 × 9.81 = 21.58 kN, so even perfectly equal sharing puts 5.40 kN on each of four wheels. The trolley changes the object the route must carry, which is why the check follows the handling assembly rather than the installed rack.

## Case study: Replace a module while the rack runs

Lenovo’s GB300 NVL72 power shelf contains six 5.5 kW hot-swappable power supply unit (PSU) modules. Hot-swappable means a designated component can be replaced while the containing system remains energized and operating, subject to the supported configuration and service procedure. The remaining qualified power supplies must be able to carry the load during replacement.

A field-replaceable unit is not automatically hot-swappable. Lenovo’s compute-tray removal instructions require that tray to be powered off and disconnected before removal. Its workload must stop or move; that does not itself require shutting down every rack component. Both jobs still need physical access and an appropriate service envelope.

## Worked example: A 1,580 kg rack fails a 3 kN wheel limit whatever the load sharing

- Lenovo lists the complete GB300 NVL72 rack at approximately 1,580 kg, depending on configuration.
- The handling assembly rolls on four wheels and the route allows 3 kN per wheel; g = 9.81 m/s², with no dynamic allowance.
- Nothing is assumed about how the four wheels share the load.

1. Rack weight — 1,580 × 9.81 / 1,000 = 15.50 kN — Mass becomes force through W = mg. A trolley or handling fixture adds its own weight on top.
2. Average per wheel — 1,580 × 9.81 / 4,000 = 3.87 kN — This is what each wheel would carry if the four shared the load equally.
3. Most heavily loaded wheel — maximum ≥ average = 3.87 kN > 3 kN — However the load is shared, at least one wheel carries the average or more.

**Result:** The route fails its 3 kN wheel limit for this rack whatever the load sharing, and a trolley only adds weight. Choose a different handling arrangement or route.

**Model boundary:** The four-wheel arrangement and the 3 kN limit are exercise inputs, not Lenovo handling data or a floor rating. A route that passed would still need the actual load sharing, dynamic effects and a structural review.

## The tradeoff

Choice: Reserve a wider replacement corridor.

Benefit: Trays and lifts can reach one rack while its neighbours keep running.

Cost: The corridor takes floor that cannot hold cabinets. Eight racks occupy 7.68 m², but the example row’s service envelope is 32.76 m²; the other 25.08 m² stays clear.

## When the situation changes

Trigger: A failed component is too large for the approved exit route.

Mechanism: The electrical spare exists, but restoration depends on a physical movement the layout cannot support.

## Apply the idea

A floor specification gives an allowable uniformly distributed load, while the replacement route crosses raised-floor panels on a trolley. What is missing from the claim that the route can carry the rack? How does a tray replacement change the object being checked?

<details>
<summary>Reveal the worked answer</summary>

Obtain the relevant concentrated and rolling-load criteria, contact geometry, load sharing and structural route assessment. For tray replacement, check the tray plus its lift, service envelope, rear connections and staging route, rather than the cabinet footprint alone.

A floor-area average does not establish the load at a wheel or panel edge. Equipment dimensions establish size, while the service operation establishes the movement and contact loads. A smaller replaceable component can require a larger temporary envelope once its handling equipment and access are included.

</details>

**The idea to keep:** Check installation, operation and replacement configurations. A free square metre is not necessarily usable rack space.

## Sources

- [NVIDIA H100 SuperPOD: White Space Infrastructure](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/infrastructure.html) — docs.nvidia.com · Reviewed 2026-09-06. Rack dimensions and service/layout choices interact with row arrangement and cable length.
- [NVIDIA H100 SuperPOD: Planning a Data Center Deployment](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html) — docs.nvidia.com · Reviewed 2026-09-16. Changes in power density and footprint can affect network layout.
- [Leviton — Data center white space and gray space](https://leviton.com/support/literature/newsletters/insider/insideroctober2025/focusedproductoctober2025) — leviton.com · Published 2025-10 · Reviewed 2026-09-10. White space houses IT; gray space describes supporting back-of-house infrastructure.
- [Vertiv — Deploying Liquid Cooling in the Data Center](https://prod.vertiv.cn/4a9616/globalassets/documents/white-papers/liquid-cooling/vertiv-liquidcooling-wp-en-na-sl-71113-web.pdf) — prod.vertiv.cn · Published 2023 · Reviewed 2026-09-10. Cooling equipment may occupy white space or a gray-space mechanical gallery; service and replacement need room in either location.
- [Lenovo NVIDIA GB300 NVL72 Rack Scale AI Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) — Lenovo Press · Published 2026-08-30 · Reviewed 2026-09-17. The named service example uses a 600 mm-wide MGX rack, 29 kg compute tray and 799 mm tray depth including water connections; Lenovo identifies suitable lift support for servicing.
- [Lenovo — GB300 NVL72 mechanical specifications](https://pubs.lenovo.com/gb300-nvl72/server_specifications_mechanical) — Lenovo · Reviewed 2026-09-12. Rack solution mass is approximately 1,580 kg, depending on configuration.
- [Lenovo — Remove a GB300 compute tray from the rack](https://pubs.lenovo.com/gb300-nvl72/remove_compute_tray) — Lenovo · Reviewed 2026-09-14. Requires compute-tray power-off and disconnection before removal; distinguishes tray service from hot-swappable PSU modules.
