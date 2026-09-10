# Count the paths, not just the advertised ports

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d08-topology-budget`, then run `uv run gigawatt-expand`.

**D08 · Authored draft · Objectives:** D08.1, D08.2

Build a small fabric, account for every port and cable, and calculate lower bounds with explicit traffic assumptions.

**Driving question:** How do endpoint bandwidth, oversubscription and physical distance constrain a communication plan?

## Separate three communication scales

Scale-up communication joins devices within a tightly integrated execution domain. Scale-out joins nodes or such domains across a cluster. Wide-area communication crosses a larger geographic and operational boundary. These terms describe relationships rather than fixed distances or universal protocols. Identify the participants, synchronization pattern and actual route before assigning a label. A geographically distributed job may use all three kinds of communication during one step, each with different bandwidth, latency and failure implications.

Physical distance establishes a propagation floor that faster serialization cannot remove. Using an illustrative fiber propagation speed of 200,000 kilometers per second, a 100-kilometer route takes at least 0.5 milliseconds one way before switching, queueing or protocol work. A request-response dependency crosses that distance twice. Long bulk transfers may tolerate that delay; many sequential dependent exchanges may not. Route length also differs from straight-line map distance. A WAN proposal needs the actual route and service behavior, not just the names of two cities.

## Draw a topology as a graph of constrained resources

Endpoints attach to leaf switches; leaf switches connect through an upper tier such as spines. Each cable consumes a port at each end. A diagram with four uplinks drawn as one thick line still needs four physical links and their associated ports. Specify whether a bandwidth label is per port, per endpoint, the sum of one direction, or a bidirectional aggregate. Dividing an aggregate bidirectional number by a one-way payload is a common way to create an impossibly fast transfer estimate.

Oversubscription compares offered endpoint capacity with capacity available toward the rest of the fabric, under a stated direction and traffic pattern. Eight 100 Gb/s downlinks sharing four 100 Gb/s uplinks give a 2:1 ratio at that leaf. This is not a promise that every job runs at half speed. Traffic staying within the leaf may not use uplinks; sparse or staggered transfers may fit easily. The ratio becomes restrictive when simultaneous traffic demands more capacity across the shared cut than the cut can provide.

## Derive bounds from the traffic matrix

A traffic matrix states who sends how much to whom. For every relevant cut in the graph, add the bytes that must cross it and divide by the usable capacity in that direction. Also check endpoint injection and receiving limits. The largest required time across these constraints is a lower bound, assuming the routing can realize the capacities together. Switch internal bandwidth, routing collisions, protocol overhead, retransmission and queueing can make the actual time longer. A bisection is a cut that divides the endpoint set into equal halves. Its capacity is useful only with a declared direction and graph; it does not replace endpoint or other narrower-cut checks.

A balanced fabric does not guarantee balanced traffic. Many senders targeting one receiver create an incast bottleneck even when the rest of the network is idle. A checkpoint burst can collide with dataset reads if they share links. A topology-aware schedule can reduce traffic through a constrained tier by locating communicating workers together, but placement may wait for suitable resources. The correct decision compares the time saved during execution with additional queueing and the effect on other jobs. Network capacity and scheduling policy are therefore parts of the same system.

## Connect the graph to the installation

After the logical calculation, count cables, endpoint ports and switch ports separately. Then add reach, routing space, patching and replacement access. A feasible graph on paper can be difficult to cable if all high-density connections must cross one congested tray. Labels should preserve the relationship between physical port, logical link and scheduled device. That mapping is essential when a technician needs to locate a degraded link without disconnecting a neighboring healthy path.

## Worked example: A four-leaf synthetic fabric

- Four leaf switches each connect eight endpoints at 100 Gb/s, one port per endpoint.
- Each leaf has four 100 Gb/s uplinks, one to each of four spine switches. Links are full duplex; all calculations below use one direction.
- Eight endpoints on one leaf send a total of 64 GB to endpoints on another leaf, evenly balanced. GB and Gb use decimal units; switching and routing are otherwise ideal.

1. Count endpoints and links — 4 × 8 = 32 endpoint links; 4 × 4 = 16 leaf-spine links — There are 48 cables in this logical design, before any management connections.
2. Count occupied switch ports — Leaves: 32 + 16 = 48; spines: 16 — A fabric cable consumes a port on both tiers, while an endpoint cable consumes one switch port and one NIC port.
3. Calculate oversubscription — (8 × 100) / (4 × 100) = 2:1 — Each leaf can inject 800 Gb/s from endpoints toward 400 Gb/s of uplinks.
4. Bound transfer time — 400 Gb/s / 8 = 50 GB/s; 64 / 50 = 1.28 s — The transmitting and receiving leaf uplinks impose the same aggregate bound under balanced routing.

**Result:** The transfer cannot finish in less than 1.28 seconds under the supplied model, despite the endpoints collectively offering twice that uplink rate.

**Model boundary:** This is a topology exercise, not an Ethernet or InfiniBand benchmark. Effective payload rate and real routing require measurement.

## The tradeoff

Choice: Reduce uplinks for a workload expected to communicate mostly within each leaf.

Benefit: Reduce switch-port, cable and transceiver requirements.

Cost: Cross-leaf bursts and future workload changes can expose the oversubscription; placement flexibility becomes more valuable.

## When the situation changes

Trigger: A job is spread across leaves despite a local communication pattern assumed during design.

Mechanism: Traffic crosses constrained uplinks that the capacity estimate assumed would remain lightly used.

Response: Compare the observed traffic matrix and placement with the design assumptions before concluding that endpoint NICs are slow.

## Apply the idea

One uplink on the sending leaf fails and traffic is perfectly balanced over the remaining three. What is the new lower bound for the same 64 GB transfer?

<details>
<summary>Reveal the worked answer</summary>

300 Gb/s equals 37.5 GB/s, so the bound is 64 / 37.5 ≈ 1.707 seconds.

The sending cut is now narrower than the receiving cut. Powered endpoints and healthy receiving links cannot overcome the missing capacity on the required path.

</details>

**The idea to keep:** An endpoint link rate is only one constraint on a path through a shared network.

## Sources and reading boundaries

- [NVIDIA DGX SuperPOD — Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html) — A concrete reference distinguishes network roles and accounts for leaf/spine cables and ports. Read 2026-09-06. Use the topology concepts only; this lesson’s counts are independently constructed.
- [Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) — Topology-aware allocation can seek to keep jobs within suitable switch groupings. Read 2026-09-06. Current documentation is version-sensitive; no example configuration is offered as production-ready.
