# Turn installed hardware into an accepted service

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d09-service-acceptance`, then run `uv run gigawatt-expand`.

**11. Storage, orchestration and recovery · Authored draft**

Connect scheduling, provisioning, isolation and observability to a reproducible end-to-end acceptance exercise.

**Driving question:** What must a tenant demonstrate before the cluster can be called usable?

## Scheduling matches a request to a feasible set

A scheduler receives more than a request for a device count. A job can require memory per device, host memory, CPU resources, compatible software, network locality, storage access and a duration. The available inventory must satisfy those requirements together. A free device in the wrong topology or software pool may not be usable for that job. This is why physical utilization, allocated utilization and useful output should be reported separately: each answers a different question about the service.

Placement can trade queue time for execution time. Keeping communicating workers close can reduce traffic through constrained network tiers, but suitable groups may be occupied. Slurm’s topology guide describes allocation that considers switch groupings; the actual behavior depends on the configured plugin and version. A scheduler also needs trustworthy resource information. If an unhealthy device remains marked available, allocation can succeed while execution fails. If repaired resources remain drained indefinitely, installed capacity stays hidden from users.

## Provisioning and isolation make the allocation real

Provisioning turns selected hardware into a reproducible execution environment. It includes boot and firmware state, drivers, runtime libraries, application images, network configuration and access to the required data. A container image helps capture user-space dependencies but does not by itself standardize every host driver or device interface. Record versions and compatibility rather than assuming that a successful image download proves a working stack. The same job should start from a declared clean state and produce a recognizable result.

Isolation controls what an allocation may consume and access. Resource accounting reports use; enforcement limits it. Slurm’s cgroup documentation distinguishes mechanisms that track processes, collect usage and constrain resources, so enabling telemetry alone should not be mistaken for enforcement. Storage authorization, network separation and management-plane access are additional concerns. An acceptance plan should test the authorized tenant’s intended operations and verify that its agreed resource boundaries are enforced, using a controlled test environment and explicit service expectations.

## Test a chain that ends in correct output

Create a small representative workload with a pinned code revision, environment identifier, input checksum, random-seed policy and expected output condition. Specify the allocation topology, startup deadline, sustained-throughput window and allowable variance before running it. Trace the path from authenticated dataset access through job submission, provisioning, collective communication and durable output. Record stage timing as well as total time. A failure should leave enough evidence to identify which dependency broke, rather than only a final nonzero exit code.

Correctness and performance must both pass. A very fast job that silently reads the wrong dataset or produces incomplete output is not accepted. A correct job that misses the agreed response or throughput target also fails that service requirement. Distinguish cold-start and warm-cache conditions, and state whether other tenants or background services are active. Reproduce a result under the same conditions before comparing it with a changed architecture. A single favorable run is a useful observation, not a complete operating envelope.

## Exercise recovery and return to service

Within an isolated, approved acceptance environment, introduce an agreed non-destructive fault such as terminating one test worker after a completed checkpoint. Observe detection, cleanup, replacement allocation, state restoration and the first correct new output. Compare the result with an uninterrupted control using the declared correctness criteria. Then verify that temporary resources and stale processes are removed. This tests recovery as a service path rather than assuming that a restart command proves progress survived.

The final report should say which service configuration passed, which degraded modes were exercised and which conditions remain untested. Keep raw logs, configuration identifiers, timestamps and output checksums with the report. Power-on counts and electrical capacity remain valuable infrastructure facts, but they are inputs to this acceptance exercise. The accepted output is an executable service commitment tied to workload, environment and recovery behavior.

## Case study: Google shifts flexible work through time

Google’s October 2023 account describes pilots that shifted eligible non-urgent tasks across time and location to reduce demand during grid stress. This complements the Sparks battery case: storage shifts available energy through time; scheduling shifts work and its demand. Neither changes every workload into a flexible job.

Consider an original teaching brief: a video-processing job must finish tomorrow, while an interactive request must respond in 200 ms. A two-hour grid event may allow the video job to move if enough later capacity remains. The same delay would fail the interactive service. Check deadlines, progress retention, placement and the later peak before promising a demand reduction. Moving execution does not automatically reduce its total energy.

## Worked example: Thirty-two free GPUs, no eligible allocation

- A fictional cluster has two topology groups, each containing four nodes with eight GPUs per node.
- A job requires four free nodes within one group and a validated common software image.
- Two nodes are free in each group. Every free node is healthy and has the right image. Cross-group placement is outside the accepted service configuration.

1. Count free hardware — 4 free nodes × 8 GPUs = 32 free GPUs — The physical count equals the requested device count.
2. Check each eligible group — Group A: 2 < 4 nodes; group B: 2 < 4 nodes — Neither group can satisfy the placement constraint.
3. State feasible capacity — Eligible four-node allocations = 0 — The job must wait, change requirements or use a separately validated service mode.

**Result:** The hardware is healthy, powered and sufficiently numerous, yet the requested service cannot launch under its accepted topology.

**Model boundary:** The grouping rule is synthetic; it is not an assertion about a particular scheduler’s default behavior.

## The tradeoff

Choice: Admit smaller flexible jobs while waiting for a large topology-constrained allocation.

Benefit: Use otherwise idle resources and improve service for suitable workloads.

Cost: Without reservations or preemption policy, those jobs can prolong fragmentation and delay the larger job.

## When the situation changes

Trigger: A worker restarts with a different runtime library than the remaining ranks.

Mechanism: Device discovery succeeds, but distributed initialization or execution becomes incompatible and useful output stops.

Response: Compare environment manifests, restore the validated version set and rerun the end-to-end acceptance path before releasing the resources.

## Apply the idea

The owner proposes allowing cross-group placement to launch the waiting job immediately. What evidence is required before treating that as equivalent service?

<details>
<summary>Reveal the worked answer</summary>

Measure correctness, collective behavior, sustained throughput, contention effects and recovery under the cross-group topology using the same pinned workload and output criteria.

Relaxing a constraint creates a new configuration. It may be worthwhile even with lower performance, but the service target and customer acceptance must reflect the measured result. The free-device count cannot establish equivalence.

</details>

**The idea to keep:** A usable cluster launches the right environment on the right topology, produces correct output and restores progress after an agreed fault.

## Sources and reading boundaries

- [Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) — Topology-aware placement considers network groupings when selecting resources. Read 2026-09-06. Plugin, configuration and release determine behavior; synthetic allocation rules are explicit.
- [Control Group in Slurm](https://slurm.schedmd.com/cgroups.html) — Process tracking, accounting and resource confinement have distinct roles. Read 2026-09-06. Current documentation includes version-specific behavior; no live configuration changes are prescribed.
- [NVIDIA DGX SuperPOD — Software](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-software.html) — A reference cluster includes orchestration, system management, libraries and operating-system components. Read 2026-09-06. Vendor reference stack, updated November 19, 2025; it does not certify an arbitrary tenant environment.
- [Google — Supporting power grids with demand response](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption) — Compare storing energy with rescheduling eligible non-urgent work during grid stress. Read 2026-09-12. Publisher-indexed introduction reviewed after direct fetch timed out. Historical pilot description; no claim that every workload can move or that reduced demand necessarily reduces total energy.

## Check your understanding: Which progress comes back?

Pause and make a prediction, then compare your reasoning.

In a hypothetical run, the latest validated, durable checkpoint represents progress through minute 20. A failure occurs at minute 28; no newer checkpoint survives. Restoration takes 3 minutes, and the same work runs at the same rate afterward.

**Pause and predict:** How much completed work must be repeated, and when can the run regain its pre-failure progress?

<details>
<summary>Compare your reasoning</summary>

It repeats 8 minutes of work and regains its minute-28 progress at wall-clock minute 39.

Restoration ends at minute 31. Replaying the 8 minutes after the durable checkpoint then takes until minute 39. The surviving checkpoint preserves earlier progress, but it does not remove restore time or the work completed after its saved state.

</details>

**The next problem:** While the recovered job runs, its hardware keeps producing heat. Can every device transfer that heat into a supported cooling path?

Continue in **Chip and rack heat capture**: A cool room can contain an overheating chip.
