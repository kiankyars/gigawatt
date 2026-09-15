# A rack’s repair boundary changes its usable job capacity

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d07-rack-as-system`, then run `uv run gigawatt-expand`.

**Compute and memory — further reading · Authored draft**

Connect the GB300 physical interfaces to service work, then use a controlled failure-placement example to distinguish healthy devices from feasible jobs.

**Driving question:** What happens to useful work when a tray or shared rack interface becomes unavailable?

## Separate the physical assembly from the job allocation

In the GB300 NVL72, four GPUs share a compute tray with CPUs and other components. Each GPU connects through the NVLink switch fabric to peers in the rack. A compute tray, a 72-GPU communication domain and an application’s tensor-parallel group are therefore different boundaries. A job may use a subset of the rack or span multiple racks, depending on its software and communication needs.

This distinction matters during service. Removing a tray removes its local components from availability. The jobs affected depend on which of those components they use, what shared dependencies were disturbed and whether the software can remap or restart. It does not follow that every GPU in the rack physically fails when one tray is unavailable, or that every job can continue unchanged.

## The rack must meet several facility interfaces at once

Rack integration concentrates power, heat and service work. The electrical inlet must supply the intended load; coolant connections must serve the cold plates; airflow must still remove heat from air-cooled parts; and the network and management interfaces must be accessible. A power allocation alone establishes none of the hydraulic, spatial or software conditions. For the recurring Abilene campus, published capacity milestones do not establish a specific GB300 rack inventory or those as-built interfaces.

Lenovo’s named compute tray weighs 29 kg and combines liquid-cooled high-power components with air-cooled supporting parts. Its removal procedure calls for tray power-off, disconnection and appropriate lifting and coolant-service equipment. The teaching consequence is a larger service operation than replacing a single hot-swappable PSU. Detailed clearances, floor loads and handling belong to the physical-site lesson; here the question is which job resources disappear during the repair.

## Failure placement can matter more than the device total

Use an independent teaching system with four groups of eight GPUs. A large job needs eight healthy GPUs in one group, and the configured scheduler cannot combine fragments from different groups. Hold four GPU failures constant. If all four occur in one group, three groups remain intact. If one occurs in each group, none remains intact. Both states contain 28 healthy GPUs, yet they support different numbers of the specified large job.

The healthy fragments remain useful for compatible smaller jobs. With one failure in each group, each group has seven healthy GPUs; a four-GPU job fits once per group, leaving three devices in each for other compatible work. “Unavailable capacity” is therefore always relative to a workload and allocation policy. This controlled grouping is not an assertion that an NVL72 has four eight-GPU fault domains.

## Recovery depends on software as well as the spare

A tightly coupled job may need checkpoint recovery, spare substitution or reconfiguration after a device interruption. NVIDIA’s July 2026 discussion of nonuniform tensor parallelism separates those existing recovery approaches from an experimental scheme that reshards work around missing GPUs. Automatic shrinkage is a software capability to establish, not a property implied by the presence of NVLink.

After physical repair, compatible firmware and configuration must restore the expected topology. Component health checks can pass while a job still encounters a wrong partition or impaired communication path. Returning the group to useful service requires exercising the dependencies used by that workload. Record both whether a placement can run and whether its output meets the expected service condition.

## Diagnose the required service rather than an average

Consider a rack with power, coolant and individual GPU checks all ready, but its required NVLink fabric unavailable. The specified multi-GPU job remains blocked. If a tested reduced mode can use a smaller working group, it may provide a limited service; merely observing that some GPUs respond does not establish that mode. The decision is whether to repair the missing path, use a qualified alternative placement, or wait. The Networking and interconnects chapter follows those communication paths beyond this rack.

## Worked example: Four failures, two placement outcomes

- The teaching system has four independent groups of eight GPUs.
- The large job needs eight healthy GPUs in one group; this configuration cannot combine fragments across groups.
- Four GPUs are unavailable. All other required inputs remain ready. Only failure placement changes.

1. Concentrate the failures — Healthy GPUs per group: 4, 8, 8, 8 — Three groups can each host one large job; the partial group can serve compatible smaller work.
2. Disperse the failures — Healthy GPUs per group: 7, 7, 7, 7 — No group meets the eight-GPU placement requirement.
3. Compare the service result — 28 healthy GPUs in either case; 3 versus 0 large-job slots — The device total hides the location of the missing resources.
4. Change the job requirement — Four-GPU jobs in the dispersed case: 1 per group = 4 jobs — Four smaller jobs occupy 16 GPUs; 12 healthy GPUs remain for other compatible allocations.

**Result:** The workload and placement rule determine usable job capacity. Failure location is part of that account.

**Model boundary:** This four-group scheduling example is original. It does not specify GB300 partition sizes or imply that one unavailable GPU always stops a real rack-wide job.

## The tradeoff

Choice: Use a larger tightly coupled GPU group for one application.

Benefit: Keep more of its communication within a fast scale-up fabric.

Cost: Its useful operation depends on a larger set of participating devices; recovery and repartitioning support affect the outcome of partial faults.

## When the situation changes

Trigger: A replacement tray passes local checks but has not joined the intended NVLink partition.

Mechanism: The hardware inventory is restored while the application’s required communication path remains incomplete.

Response: Verify configuration and the intended multi-GPU workload before counting the group as restored service.

## Apply the idea

The dispersed-failure system must run an eight-GPU job. Would adding one spare GPU anywhere recover a slot, or does placement matter? What else would you verify before promising throughput?

<details>
<summary>Reveal the worked answer</summary>

A spare must be connected and qualified within one affected group so that group again provides eight healthy GPUs. An unrelated ninth group or an unqualified attachment does not satisfy the stated rule.

Restoring one valid group recovers allocation feasibility. Compatible firmware, topology and application behavior still determine whether that slot delivers the required throughput; the spare’s presence alone is not a completed recovery.

</details>

**The idea to keep:** A capacity report needs the job’s placement requirements and recovery behavior, as well as a healthy-device count.

## Sources and reading boundaries

- [NVIDIA DGX GB Rack Scale Systems — Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html#power-shelves) — DGX GB300 rack, compute-tray, rear-interface and switch-tray organization. Read 2026-09-14. Identified GB300 figures and hardware sections inspected. The shared guide also contains GB200-specific NIC and approximate power text; those quantities are not carried into this lesson.
- [Lenovo NVIDIA GB300 NVL72 Rack Scale AI Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) — Named rack and compute-tray components, hybrid cooling, 29 kg tray, service spares and CPU memory configuration. Read 2026-09-14. August 30, 2026 guide inspected. Lenovo lists 7.7 TB/s GPU memory bandwidth for its configuration, separate from NVIDIA’s up-to-8-TB/s platform figure. This lesson does not combine those into a measured hardware claim.
- [Lenovo — Remove a GB300 compute tray from the rack](https://pubs.lenovo.com/gb300-nvl72/remove_compute_tray) — Compute-tray removal requires power-off and disconnection, with appropriate lifting and coolant-service provisions. Read 2026-09-14. Manufacturer removal procedure inspected. Used to explain the service boundary, not to assert that every tray fault shuts down the rack or to reproduce a maintenance procedure.
- [NVIDIA DGX GB Rack Scale Systems — System Health Check](https://docs.nvidia.com/dgx/dgxgb200-user-guide/health-check.html) — NVSM checks component health and can stress the system under load. Read 2026-09-14. Public page reviewed. Application qualification after a repair is the course’s operational reasoning, not a complete vendor acceptance procedure.
- [NVIDIA — Nonuniform Tensor Parallelism and training goodput](https://developer.nvidia.com/blog/enhancing-goodput-in-large-scale-llm-training-with-nonuniform-tensor-parallelism/) — A device interruption can affect a tightly coupled job; recovery depends on checkpointing, spare substitution or supported adaptation. Read 2026-09-14. July 6, 2026 authored article reviewed. Nonuniform Tensor Parallelism and associated power boosting are described as experimental. The four-group allocation exercise is original and is not NVL72 fault behavior.
