# Count the paths, not just the advertised ports

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d08-topology-budget`, then run `uv run gigawatt-expand`.

**10. Networking and interconnects · Authored draft**

Account for a cluster's ports and cables, then trace its connection through the campus boundary to external networks.

**Driving question:** How do topology, physical distance and the campus fiber handoff constrain a communication plan?

## Separate three communication scales

Scale-up communication joins devices within a tightly integrated execution domain, such as the GPUs in a scale-up rack. Scale-out joins nodes or such domains across a cluster. Data-center interconnect (DCI) connects facilities, including buildings on one campus; a wide-area network (WAN) extends communication across more distant sites or provider networks. DCI therefore need not mean long-haul, and scale-up need not end at every rack boundary. These terms describe relationships rather than fixed distances or universal protocols. Identify the participants, synchronization pattern and actual route before assigning a label.

Physical distance establishes a propagation floor that faster serialization cannot remove. Using an illustrative fiber propagation speed of 200,000 kilometers per second, a 100-kilometer route takes at least 0.5 milliseconds one way before switching, queueing or protocol work. A request-response dependency crosses that distance twice. Long bulk transfers may tolerate that delay; many sequential dependent exchanges may not. Route length also differs from straight-line map distance. A WAN proposal needs the actual route and service behavior, not just the names of two cities.

## Locate a real adapter and switch

A network adapter connects the server to an external fabric. The standalone product example is NVIDIA’s ConnectX-7 MCX75310AAS-NEAT: a single OSFP port supports up to 400 Gb/s, with a PCIe Gen 4/5 ×16 host interface. Its board is 68.90 × 167.65 mm. This example identifies the adapter’s function and form; it does not identify the adapter fitted to every GB300 configuration. A 400 Gb/s line rate converts to 50 GB/s before protocol overhead and other constraints.

NVIDIA’s 1U QM9700 switch provides 64 logical 400 Gb/s ports through 32 twin-port OSFP cages. A front-panel opening and a logical port are therefore different counts. Its aggregate is 25.6 Tb/s in one direction; the advertised 51.2 Tb/s sums both directions. Match the direction of the bandwidth number to the traffic being calculated.

## Draw a topology as a graph of constrained resources

Endpoints attach to leaf switches; leaf switches connect through an upper tier such as spines. Each cable consumes a port at each end. A diagram with four uplinks drawn as one thick line still needs four physical links and their associated ports. Specify whether a bandwidth label is per port, per endpoint, the sum of one direction, or a bidirectional aggregate. Dividing an aggregate bidirectional number by a one-way payload is a common way to create an impossibly fast transfer estimate.

Oversubscription compares offered endpoint capacity with capacity available toward the rest of the fabric, under a stated direction and traffic pattern. Four 400 Gb/s downlinks sharing two 400 Gb/s uplinks give a 2:1 ratio at that leaf. This is not a promise that every job runs at half speed. Traffic staying within the leaf may not use uplinks; sparse or staggered transfers may fit easily. The ratio becomes restrictive when simultaneous traffic demands more capacity across the shared cut than the cut can provide.

## Derive bounds from the traffic matrix

A traffic matrix states who sends how much to whom. For every relevant cut in the graph, add the bytes that must cross it and divide by the usable capacity in that direction. Also check endpoint injection and receiving limits. The largest required time across these constraints is a lower bound, assuming the routing can realize the capacities together. Switch internal bandwidth, routing collisions, protocol overhead, retransmission and queueing can make the actual time longer. A bisection is a cut that divides the endpoint set into equal halves. Its capacity is useful only with a declared direction and graph; it does not replace endpoint or other narrower-cut checks.

A balanced fabric does not guarantee balanced traffic. Many senders targeting one receiver create an incast bottleneck even when the rest of the network is idle. A checkpoint burst can collide with dataset reads if they share links. A topology-aware schedule can reduce traffic through a constrained tier by locating communicating workers together, but placement may wait for suitable resources. The correct decision compares the time saved during execution with additional queueing and the effect on other jobs. Network capacity and scheduling policy are therefore parts of the same system.

## Connect the graph to the installation

After the logical calculation, count cables, endpoint ports and switch ports separately. Then add reach, routing space, patching and replacement access. A feasible graph on paper can be difficult to cable if all high-density connections must cross one congested tray. Labels should preserve the relationship between physical port, logical link and scheduled device. That mapping is essential when a technician needs to locate a degraded link without disconnecting a neighboring healthy path.

## Follow the campus connection to a carrier

Trace an external path from the cluster network through border equipment and patch panels to the outside fiber route. The entrance facility brings outside-plant cabling into the building. A meet-me room (MMR) provides an interconnection area for tenant, operator and carrier cabling; a private campus may use a different room arrangement. These are functions to locate, not a universal sequence of separate rooms. Corning's multitenant example connects outside plant, the MMR and customer rack cabling.

At the agreed demarcation point, mark where one party's service responsibility ends and the next begins. In Equinix's example, customers patch their equipment to the operator's demarcation. An intra-facility cable reaches the MMR and a cross-connect completes the physical connection there. That cable alone does not supply Internet transit: identify the actual carrier or private service, endpoint, capacity and acceptance boundary. The site-planning section checks whether the route and construction rights can be delivered; the networking section checks what the resulting connection carries.

## Test routes, not carrier names

Two carrier contracts do not prove two independent physical paths. Map each circuit through its entrance, duct, splice points, bridge crossings and upstream facilities; two fibers in one cable or conduit share that exposure. The FCC's physical-diversity discussion identifies shared cables, conduits and structures as common failure points. Provider diversity and route diversity answer different questions. Verify the route evidence and the surviving service, including border equipment and routing behavior; separate entrances alone do not prove end-to-end independence.

In an original campus example, two 100 Gb/s services share the same bridge. Cutting both bridge cables removes both services, even though the invoices name different carriers. Moving one service to a verified independent crossing removes that particular shared failure. It does not establish automatic failover, enough remaining payload capacity, or independence from every other hazard. This is the external-network counterpart of the shared-bus failure in the UPS lesson.

## Worked example: Four leaves with shared uplinks

- Four leaf switches each connect four endpoints at 400 Gb/s.
- Each leaf has two 400 Gb/s uplinks, one to each of two spine switches. All bandwidth calculations use one direction.
- Four endpoints under one leaf send 32 GB in total to another leaf, with traffic evenly distributed. GB and Gb use decimal units; this model omits overhead and queueing.

1. Count links — 4 × 4 = 16 endpoint cables; 4 × 2 = 8 uplink cables — 24 cables connect the endpoints and the two switch tiers.
2. Count switch ports — Leaves: 16 + 8 = 24; spines: 8 — Each leaf–spine cable consumes a port on both tiers.
3. Find the shared capacity — (4 × 400) / (2 × 400) = 2:1 — A leaf has 1,600 Gb/s toward endpoints but 800 Gb/s toward the spines.
4. Bound the transfer — 800 Gb/s ÷ 8 = 100 GB/s; 32 GB ÷ 100 GB/s = 0.32 s — The sender and receiver uplinks impose the same bound under the supplied balanced traffic pattern.

**Result:** Adding two more uplinks per leaf raises shared capacity to 1,600 Gb/s and reduces this transfer bound to 0.16 s. The endpoint links have not changed.

**Model boundary:** This calculation isolates the shared-link constraint; measured application throughput also includes protocol, routing, queueing and endpoint behavior.

## The tradeoff

Choice: Reduce uplinks for a workload expected to communicate mostly within each leaf.

Benefit: Reduce switch-port, cable and transceiver requirements.

Cost: Cross-leaf bursts and future workload changes can expose the oversubscription; placement flexibility becomes more valuable.

## When the situation changes

Trigger: A job is spread across leaves despite a local communication pattern assumed during design.

Mechanism: Traffic crosses constrained uplinks that the capacity estimate assumed would remain lightly used.

Response: Compare the observed traffic matrix and placement with the design assumptions before concluding that endpoint NICs are slow.

## Apply the idea

The transfer is slow only when its participants occupy separate leaves. Transfers between the same number of endpoints on one leaf remain fast. What should you inspect before replacing their network adapters?

<details>
<summary>Reveal the worked answer</summary>

Inspect uplink utilization, queueing, traffic placement and error counters along the cross-leaf route. A fast local transfer makes the shared fabric a stronger suspect than the endpoint port rate alone.

Changing participant placement changes the route without changing their adapters. Compare that changed route with the symptoms, then test the suspected shared resource.

</details>

**The idea to keep:** An endpoint link rate is only one constraint on a path through a shared network.

## Sources and reading boundaries

- [NVIDIA DGX SuperPOD — Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html) — A concrete reference distinguishes network roles and accounts for leaf/spine cables and ports. Read 2026-09-06. Use the topology concepts only; this lesson’s counts are independently constructed.
- [Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) — Topology-aware allocation can seek to keep jobs within suitable switch groupings. Read 2026-09-06. Current documentation is version-sensitive; no example configuration is offered as production-ready.
- [Corning — Meet-Me-Room to Outside Plant Data Center Solutions](https://www.corning.com/data-center/worldwide/en/home/applications/multi-tenant-data-center/meet-me-room.html) — Connect outside-plant fiber, a meet-me room and customer cabling; DCI can join campus buildings. Read 2026-09-12. Opening MMR/OSP sections reviewed. Multitenant example, not a universal campus layout or security guarantee.
- [Equinix — Customer-Managed Pre-Cabling and Demarcations](https://docs.equinix.com/cross-connect/installation/xc-customer-managed-precabling/) — Separate customer cabling, MMR cross-connects and the demarcation responsibility boundary. Read 2026-09-12. Pre-cabling page and linked Demarcations page reviewed. Product-specific implementation; no fees, availability or universal room arrangement adopted.
- [FCC 25-21 — Physical Diversity, paragraph 63](https://docs.fcc.gov/public/attachments/FCC-25-21A1.pdf) — Shared cables, conduits and structures can defeat physical path diversity. Read 2026-09-12. Paragraphs 62–63 on printed page 26 reviewed. NG911 proposed rulemaking used only for the engineering distinction, not data-center legal requirements.
- [NVIDIA ConnectX-7 adapter card specifications](https://networking-docs.nvidia.com/connectx7hw/specifications) — MCX75310AAS-NEAT adapter: one OSFP port up to 400 Gb/s, PCIe Gen 4/5 ×16, and 68.90 × 167.65 mm dimensions. Read 2026-09-14. Standalone adapter example; do not imply this is the exact GB300 NVL72 tray configuration. Marketing rendering illustrates family, not legible exact SKU.
- [NVIDIA QM97xx hardware introduction](https://networking-docs.nvidia.com/qm97x0hw/introduction) — QM9700: 64 logical 400 Gb/s ports through 32 twin-port OSFP cages in 1U; 25.6 Tb/s one way versus 51.2 Tb/s summed bidirectional bandwidth. Read 2026-09-14. Cages and logical ports differ. One-direction payload calculations cannot use summed bidirectional rate.
- [Equinix Cross Connect demarcations](https://docs.equinix.com/cross-connect/installation/xc-demarcations/) — Physical demarcation points define responsibility for patching between customer equipment and a cross connect. Read 2026-09-14. One colocation arrangement; private campuses can organize rooms differently.
- [Cloud TPU Multislice Overview](https://docs.cloud.google.com/tpu/docs/multislice-introduction) — ICI connects chips within a TPU slice; communication across slices uses the data-center network. Read 2026-09-14. May reuse existing P93 rather than duplicate.
