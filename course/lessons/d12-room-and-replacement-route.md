# A rack must fit on its worst day

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d12-room-and-replacement-route`, then run `uv run gigawatt-expand`.

**5. Physical site, buildings and safety · Authored draft**

Separate white and grey space, equipment footprints, service and movement envelopes, and the loads actually applied to a structure.

**Driving question:** Why can a layout that fits every rack still be impossible to maintain?

## Draw three floor plans, not one

A footprint drawing answers a narrow question: can the equipment occupy this position? A service drawing asks whether doors, drawers, cables, hoses and lifting aids can move while nearby equipment remains available. A replacement drawing follows a component from its installed position through turns, thresholds, doors, staging areas and the loading route. These drawings overlap, but none can substitute for the others. The longest or heaviest replaceable object may determine feasibility more than the rack cabinet.

Apply the white/grey distinction from the opening lesson to the actual floor plan. The IT hall is white space; a separate supporting electrical room or mechanical gallery is grey space. A coolant distribution unit can be installed in either area, so its equipment name does not settle the classification. Vertiv’s mechanical-space guidance makes this placement choice explicit and requires room for service and replacement. Count access in the area where the equipment is actually placed.

Consider eight hypothetical racks, each 0.8 m wide and 1.2 m deep. Their combined footprint is 7.68 m². Now give the row a specified 1.5 m front service zone, 1.2 m rear zone and 1 m at each end. Its illustrative planning envelope becomes 8.4 m by 3.9 m, or 32.76 m². Those dimensions are supplied exercise inputs, not code requirements. The difference explains why dividing gross room area by cabinet footprint can overstate a useful layout dramatically.

Not every clearance must be permanently exclusive; some activities can share space at different times. That creates a scheduling and availability condition. If replacing rack A blocks the only access to rack B, the design should state which activity takes priority and whether both services remain supportable. A promise of maintainability is conditional on those actual routes, not just on the electrical single-line diagram.

Consider a converter removed from a rack. Putting it in a sidecar beside the rack can release rack mounting units while consuming white-space floor area and access. Moving it to a separate electrical room consumes grey-space area and may change cable routes. Which option reduces the total building footprint? Neither location alone answers that question. Compare both complete layouts, including the space that can actually be reused and the space newly required. A freed rack slot, a freed hall position, and a smaller building are three different claims.

## A real service object: Lenovo’s GB300 compute tray

Lenovo’s GB300 NVL72 documentation puts the configured rack solution at approximately 1,580 kg, with variation by configuration. Its product guide gives a 600 mm-wide MGX rack and a 29 kg compute tray, 799 mm deep including the rear water connections. These are two different handling jobs: moving a complete rack and replacing a tray. Plan the route, lifting equipment and service access for the object actually being moved.

The guide requires an on-site material lift to permit single-person tray service and names the Genie GL-8 and a ServerLift alternative. A floor plan must therefore accommodate the tray, the selected handling equipment, the technician’s access and the replacement route. The presentation shows the manufacturer’s rack and rear-tray photographs so the water connections and scale are visible. No universal aisle dimension or lifting procedure follows from these product specifications.

## A structure sees forces, locations and combinations

Mass becomes a gravitational force through W = mg. Two thousand kilograms corresponds to about 19.6 kN using g = 9.81 m/s². Dividing that force by a cabinet footprint produces an average pressure, but it does not describe how feet, rails, spreader plates or casters transmit force to a raised floor and structural members. The local load path matters. So do the equipment operating state, attached piping, installation loads and support configuration.

An allowable uniformly distributed floor load is therefore not automatically a permitted wheel load. A moving rack can place substantial force onto a small number of contact points or cross a panel edge. Structural interpretation belongs to the supplied engineering criteria and qualified review. The calculation below deliberately provides a separate wheel limit so that we can make a bounded rejection without pretending that one average number proves the whole building safe.

Increasing rack density can reduce the number of cabinets while increasing weight, cooling connections and the demands on handling equipment. NVIDIA’s H100 deployment guidance illustrates the wider principle: rack and layout choices can change cable lengths and other domains. The course does not turn that particular product configuration into a universal layout. It uses the relationship to ask which interfaces must be recalculated when a cabinet changes.

## Treat the route as a chain of interfaces

Follow the same physical object throughout the journey. Its shipping dimensions may differ from operating dimensions, and temporary handling fixtures may widen it. A door can be wide enough while the turn beyond it is not. A lift can have adequate total capacity while the object’s shape prevents entry. A route may cross a space controlled by a different tenant or become unavailable during another phase of construction. Each is a distinct interface, with an owner and evidence.

For a replacement plan, record the object, mass, orientation, handling assembly, clear envelope, permitted loads and any temporary changes. Then identify dependencies on live services: cable trays overhead, coolant hoses nearby, fire access and the surviving maintenance path. The value of this record is that another person can examine the actual limiting step. A reassuring statement that the route was considered gives them little to verify.

You do not need a complete professional design to discover an incompatibility. If the supplied wheel criterion is 3 kN and the computed static force per wheel is already 5.4 kN, the proposed route fails that stated criterion. Passing it would still not prove adequacy, because unequal load sharing, dynamic effects and structural details remain. This asymmetry is useful: limited evidence can decisively reject a configuration without being sufficient to approve it.

## Worked example: The moving assembly fails where the installed rack passes

- Synthetic installed rack mass 2,000 kg; movement assembly including trolley is 2,200 kg.
- Four wheels are assumed equally loaded for this lower-complexity calculation.
- The specified route limit is 3 kN per wheel; g = 9.81 m/s². No dynamic allowance is included.

1. Installed weight — 2,000 × 9.81 / 1,000 = 19.62 kN — The installed support arrangement must be checked using its own criteria.
2. Moving assembly weight — 2,200 × 9.81 / 1,000 = 21.582 kN — The trolley changes the object that the route must support.
3. Per-wheel static force — 21.582 / 4 = 5.40 kN — Even ideal equal sharing exceeds the supplied 3 kN wheel criterion.

**Result:** Reject this movement configuration against the stated route criterion; investigate a different engineered handling arrangement or route.

**Model boundary:** No floor rating, lifting procedure, structural approval or code clearance is established by this exercise.

## The tradeoff

Choice: Reserve a wider replacement corridor.

Benefit: It can preserve access and reduce interference during equipment exchange.

Cost: It consumes space that cannot simultaneously be sold or assigned to permanently installed cabinets.

## When the situation changes

Trigger: A failed component is too large for the approved exit route.

Mechanism: The electrical spare exists, but restoration depends on a physical movement the layout cannot support.

Response: Escalate the route incompatibility through the qualified facilities and equipment teams; revise the service plan before representing the spare as a complete recovery solution.

## Apply the idea

A floor specification gives an allowable uniformly distributed load, while the replacement route crosses raised-floor panels on a trolley. What is missing from the claim that the route can carry the rack? How does a tray replacement change the object being checked?

<details>
<summary>Reveal the worked answer</summary>

Obtain the relevant concentrated and rolling-load criteria, contact geometry, load sharing and structural route assessment. For tray replacement, check the tray plus its lift, service envelope, rear connections and staging route, rather than the cabinet footprint alone.

A floor-area average does not establish the load at a wheel or panel edge. Equipment dimensions establish size, while the service operation establishes the movement and contact loads. A smaller replaceable component can require a larger temporary envelope once its handling equipment and access are included.

</details>

**The idea to keep:** Check installation, operation and replacement configurations. A free square metre is not necessarily usable rack space.

## Sources and reading boundaries

- [NVIDIA H100 SuperPOD: White Space Infrastructure](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/infrastructure.html) — Rack dimensions and service/layout choices interact with row arrangement and cable length. Read 2026-09-06. Selected white-space planning discussion inspected. The force calculation uses invented masses and limits; the separately identified Lenovo dimensions come from its own product guide.
- [NVIDIA H100 SuperPOD: Planning a Data Center Deployment](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html) — Changes in power density and footprint can affect network layout. Read 2026-09-06. Cross-domain planning discussion inspected; no complete product site plan or compliance assessment is reproduced.
- [Leviton — Data center white space and gray space](https://leviton.com/support/literature/newsletters/insider/insideroctober2025/focusedproductoctober2025) — White space houses IT; gray space describes supporting back-of-house infrastructure. Read 2026-09-10. Reviewed the White Space and Gray Space definitions under Leviton Solutions for Data Centers. These are area conventions, not a rule assigning every power or cooling device to one room type.
- [Vertiv — Deploying Liquid Cooling in the Data Center](https://prod.vertiv.cn/4a9616/globalassets/documents/white-papers/liquid-cooling/vertiv-liquidcooling-wp-en-na-sl-71113-web.pdf) — Cooling equipment may occupy white space or a grey-space mechanical gallery; service and replacement need room in either location. Read 2026-09-10. Reviewed Designing Mechanical Space, printed pages 14–15, and the space-use discussion on page 13. No equipment clearance, floor rating, or universal footprint saving is taken from this example.
- [Lenovo NVIDIA GB300 NVL72 Rack Scale AI Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) — The named service example uses a 600 mm-wide MGX rack, 29 kg compute tray and 799 mm tray depth including water connections; Lenovo identifies suitable lift support for servicing. Read 2026-09-12. Read physical and electrical specifications and Genie Material Lift sections, with rack and rear compute-tray figures. Width and tray mass are product dimensions, not full operating rack mass or service clearance. No universal aisle size, lift configuration, performance or complete design specification is inferred.
- [Lenovo — GB300 NVL72 mechanical specifications](https://pubs.lenovo.com/gb300-nvl72/server_specifications_mechanical) — Rack solution mass is approximately 1,580 kg, depending on configuration. Read 2026-09-12. Full rack solution is distinct from the 185 kg empty MGX rack and 29 kg compute tray in Lenovo Press. Mass is not a floor-pressure, caster-load or handling-assembly specification.
