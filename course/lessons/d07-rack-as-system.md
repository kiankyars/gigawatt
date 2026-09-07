# The rack becomes a service boundary

**D07 · Authored draft · Objectives:** D07.1, D07.3, D07.4

Connect tray and rack organization to physical interfaces and failure scope, then distinguish nominal from schedulable capacity.

**Driving question:** How does tighter hardware integration change deployment, maintenance and usable job capacity?

## Distinguish the containers from the communication domain

A server, tray and rack are physical assemblies. A communication domain is the set of devices that can participate under a specified connectivity and software model. The two boundaries may coincide, but they need not. Several independent servers can share one cabinet, while a tightly connected system can span multiple trays. A statement that devices are connected does not imply that each pair has its own dedicated physical wire. Switched connectivity and direct point-to-point wiring are different graphs.

When reading a rack diagram, identify the replaceable assemblies and the dependencies that cross them. A tray may contain processors, memory, network interfaces and local storage. A switch tray may be shared by many compute trays. Power shelves may supply a common bus, and coolant manifolds may serve parallel branches. This creates opportunities to share infrastructure, but also requires a precise account of what happens when a shared component is removed. The smallest replaceable unit, fault domain and scheduled job allocation can all differ.

## Dense hardware changes more than kilowatts per cabinet

A replacement rack can change static weight, rolling installation loads, delivery dimensions, floor anchoring, cable bend space and the clearance needed to remove an assembly. It can also shift heat from room air into a coolant loop while leaving power supplies, networking or other components dependent on air. The electrical inlet, liquid connections, drain or service provisions and management connections must all meet the supplied installation requirements. One acceptable aggregate rack power value cannot answer these separate questions.

The operating team must be able to reach and replace parts without unintentionally disturbing adjacent systems. Ask whether a repair requires draining a branch, isolating a power zone, moving cables or temporarily reducing the communication domain. Consider the recovery path: a replacement component needs compatible firmware, configuration and health validation before it becomes useful. Procurement of a spare is not equivalent to restoration of service. The service plan should name the tools, staff, spares and verification required for the intended repair boundary.

## Convert device inventory into feasible job allocations

Count healthy devices, but also describe how they are connected and which resources a job needs simultaneously. A job may require eight devices in one compatible group, sufficient memory per device, network access and an available software image. A rack with twenty-eight healthy devices might support only three such groups if a failure fragments its topology. The unused devices have not vanished electrically; they are unavailable to that particular allocation. Smaller jobs may still use them.

This creates a scheduling and reliability tradeoff. Large tightly integrated groups may reduce communication cost for some workloads. They can also make partial faults more disruptive when a job cannot shrink or remap around the failure. Flexible partitioning can preserve service for smaller jobs, but it may reduce the maximum group size or change performance. Evaluate the actual customer job mix and software capabilities. The appropriate capacity measure is the number of feasible allocations and their accepted throughput, not a single count of powered processors.

## Accept the system under more than one condition

An acceptance exercise should include normal operation, an agreed degraded condition and restoration. Record which job sizes remain supported, what throughput changes and whether the management plane accurately reports the loss. Repeating a small benchmark on every device individually may miss failures that appear only during collective communication or simultaneous load. Conversely, a whole-rack test can hide one marginal branch if it reports only an average. Combine component checks with a workload exercise that traverses the shared dependencies.

## Worked example: Thirty-two devices, three usable groups

- A synthetic rack contains four independently schedulable groups of eight accelerators.
- An important job requires exactly eight healthy accelerators within one group; this software version cannot combine fragments from different groups.
- Four devices fail in one group; all other devices, power and cooling remain available.

1. Count the healthy devices — 32 − 4 = 28 — This is the physical inventory after the fault.
2. Count feasible large jobs — 3 intact groups × 1 job/group = 3 jobs — The partial fourth group cannot satisfy the stated topology requirement.
3. Compare utilization measures — 28 / 32 = 87.5%; 3 / 4 = 75% — Healthy-device share and large-job-slot availability differ.
4. Identify residual opportunity — 4 healthy devices remain in the affected group — They may support a compatible smaller job if the scheduler and service policy allow it.

**Result:** The rack retains 87.5% of its devices but only 75% of its specified large-job slots.

**Model boundary:** The grouping and failure response are invented to teach allocation constraints; no real product is asserted to behave this way.

## The tradeoff

Choice: Build larger tightly connected job domains.

Benefit: Potentially reduce the communication and coordination burden for workloads that use the full domain.

Cost: Qualification, maintenance and some failure states can affect a larger set of jobs; flexible partitioning must be demonstrated.

## When the situation changes

Trigger: A replaced switch assembly has an incompatible configuration.

Mechanism: Devices pass local health checks, yet the expected communication graph is incomplete or degraded.

Response: Validate the topology, collective behavior and required job sizes after replacement before returning the group to service.

## Apply the idea

The scheduler gains a tested mode that combines the two healthy four-device fragments of two affected groups, at 80% of an intact group’s throughput. How should the capacity report change?

<details>
<summary>Reveal the worked answer</summary>

Report one additional feasible eight-device job slot with a measured degraded-throughput factor of 0.8, plus the unchanged intact-group slots.

The new mode recovers an allocation, but it does not make the fractured topology equivalent to an intact group. The service report should preserve that distinction and state which workloads were tested.

</details>

**The idea to keep:** A system’s useful size is defined by the topology and service it can sustain, including maintenance and failures.

## Sources and reading boundaries

- [NVIDIA DGX SuperPOD — Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html) — A named reference system distinguishes compute, storage and management fabrics and explicit topology groupings. Read 2026-09-06. H100 reference architecture updated November 19, 2025; no component counts or ratios are generalized.
- [Open Rack/SpecsAndDesigns](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) — Physical rack, power and liquid interfaces have separate versioned documents. Read 2026-09-06. An index is a starting point; actual installation and maintenance requirements must come from the supplied equipment.
