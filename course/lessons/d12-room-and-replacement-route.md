# A rack must fit on its worst day

**D12 · Authored draft · Objectives:** D12.1

Separate equipment footprints from service and movement envelopes, and distinguish average loading from the loads actually applied to a structure.

**Driving question:** Why can a layout that fits every rack still be impossible to maintain?

## Draw three floor plans, not one

A footprint drawing answers a narrow question: can the equipment occupy this position? A service drawing asks whether doors, drawers, cables, hoses and lifting aids can move while nearby equipment remains available. A replacement drawing follows a component from its installed position through turns, thresholds, doors, staging areas and the loading route. These drawings overlap, but none can substitute for the others. The longest or heaviest replaceable object may determine feasibility more than the rack cabinet.

Consider eight hypothetical racks, each 0.8 m wide and 1.2 m deep. Their combined footprint is 7.68 m². Now give the row a specified 1.5 m front service zone, 1.2 m rear zone and 1 m at each end. Its illustrative planning envelope becomes 8.4 m by 3.9 m, or 32.76 m². Those dimensions are supplied exercise inputs, not code requirements. The difference explains why dividing gross room area by cabinet footprint can overstate a useful layout dramatically.

Not every clearance must be permanently exclusive; some activities can share space at different times. That creates a scheduling and availability condition. If replacing rack A blocks the only access to rack B, the design should state which activity takes priority and whether both services remain supportable. A promise of maintainability is conditional on those actual routes, not just on the electrical single-line diagram.

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

The same 2,200 kg assembly uses six equally loaded wheels. Does it now satisfy the stated 3 kN limit?

<details>
<summary>Reveal the worked answer</summary>

No. The static average is 21.582/6 = 3.60 kN per wheel.

Six contacts reduce the average but still exceed the supplied criterion. Real uneven contact may produce a larger maximum. Merely increasing wheel count does not constitute a validated handling design; the revised assembly and route would need their own reviewed loading assumptions.

</details>

**The idea to keep:** Check installation, operation and replacement configurations. A free square metre is not necessarily usable rack space.

## Sources and reading boundaries

- [NVIDIA H100 SuperPOD: White Space Infrastructure](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/infrastructure.html) — Rack dimensions and service/layout choices interact with row arrangement and cable length. Read 2026-09-06. Selected white-space planning discussion inspected. All dimensions, masses and force limits in this lesson are invented inputs, not NVIDIA specifications.
- [NVIDIA H100 SuperPOD: Planning a Data Center Deployment](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html) — Changes in power density and footprint can affect network layout. Read 2026-09-06. Cross-domain planning discussion inspected; no complete product site plan or compliance assessment is reproduced.
