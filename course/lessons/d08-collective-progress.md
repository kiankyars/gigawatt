# A collective makes waiting contagious

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d08-collective-progress`, then run `uv run gigawatt-expand`.

**9. Networking and interconnects · Authored draft**

Walk through a ring all-reduce, then connect synchronization, congestion and placement to the job timeline.

**Driving question:** How can one constrained participant delay a job running on many healthy accelerators?

## Understand the result before choosing an algorithm

An all-reduce combines corresponding values from participating workers and returns the combined result to each worker. For example, three workers holding 2, 5 and 7 can all receive 14 after a sum reduction. An all-gather instead distributes each worker’s distinct contribution to everyone; an all-to-all sends different pieces to different destinations. Their names identify data transformations, not one mandatory topology. A library can implement a transformation with different algorithms depending on message size, topology and available hardware.

The workers must agree on the operation they are participating in. NCCL’s collective documentation requires compatible participation, counts and data types and warns that mismatches can hang, crash or corrupt execution. This is a software correctness condition distinct from link capacity. A job that stops during communication may have a missing or mismatched participant rather than a damaged cable. Diagnosis must examine both communication progress and the execution history that led each rank to that point.

## Derive one ring rather than memorizing a formula

For a simplified ring all-reduce with N workers, divide each worker’s input buffer into N equal chunks. During a reduce-scatter phase, workers pass and combine chunks for N minus one rounds. At its end, each worker holds one final reduced chunk. During an all-gather phase, another N minus one rounds circulate the completed chunks until everyone holds the full reduced buffer. In this model, each worker sends one chunk in each round, giving total sent bytes of 2(N−1)S/N for an input buffer of size S.

If every ring edge sustains bandwidth B, the transfer component is that byte count divided by B. Add an assumed per-round startup cost alpha for 2(N−1) rounds. This model neglects reduction execution, protocol overhead and interference, and assumes that sends can proceed concurrently around the ring. It is a teaching model of one algorithm. It is not a prediction that a library will choose a ring or that every real all-reduce reaches the resulting time.

## Place the communication on the job’s critical path

If a step cannot begin its next computation until the collective finishes, collective delay extends the step directly. If some independent computation can overlap, only the exposed portion extends the critical path. The distinction matters when evaluating a network upgrade. Halving a communication phase does not halve a job whose time is mostly spent elsewhere. Conversely, a phase that seems small on one device can dominate at scale if it repeatedly waits for a slow participant.

Congestion makes available bandwidth time-dependent. Several flows can share an output queue, and one worker can receive less than its nominal link rate. A degraded link can also shift traffic onto remaining paths. The collective may then wait for the slowest required transfer even while most devices report no local error. Look for distributions of completion time, retransmissions or congestion indicators and rank-level timing. An average utilization metric can hide the worker that determines the finish line.

## Select a fabric as an operating system decision

Ethernet and InfiniBand are families of technologies and implementations, not universal performance rankings. Meta’s March 2024 report describes separate large clusters using RoCE and InfiniBand and explains that routing, collective software and topology-aware scheduling required joint tuning. That case supports testing the full system. It does not prove equal performance for every workload or make operational expertise irrelevant. A useful comparison names the hardware, protocol configuration, topology, software version, message distribution and failure conditions being tested.

## Optical circuit switching in Google TPU v4

Google’s TPU v4 paper describes 4,096 TPU chips in 64 racks. Each rack contains a 64-chip electrical 4 × 4 × 4 block. Forty-eight optical circuit switches connect these blocks through reconfigurable light paths. An optical circuit switch establishes a connection between fiber endpoints; it does not inspect and forward each packet like a packet switch. Reconfiguration can connect available blocks for a workload and avoid unavailable portions of the machine.

This is the TPU v4 inter-chip network. Google’s Multislice documentation separately distinguishes ICI inside a slice from communication over the data-center network between slices. A wide-area route requires another distance and service budget; the presence of optical switches does not remove propagation delay.

## Diagnose a link that stays connected

The closing slide changes the evidence: after a cable move, one worker arrives late, its port reports rising retries, and other uplinks retain spare capacity. Trace that worker’s adapter, cable, connectors and switch port before adding general fabric bandwidth. Correlate the link counters with rank timing, localize the affected segment and verify the collective after the repair. A connected link can deliver poor payload service, so link-up status alone does not resolve the diagnosis.

## Worked example: Four workers perform a ring all-reduce

- Four workers each contribute a 1 GB buffer, split into four 0.25 GB chunks.
- Each ring edge sustains 50 GB/s of payload. The bandwidth model omits per-round startup and reduction work.
- Compute takes 200 ms; compare exchange entirely afterward with 20 ms of communication overlapping independent compute.

1. Reduce then distribute — 3 reduce-scatter rounds + 3 all-gather rounds = 6 rounds — After reduction, each worker holds one complete chunk; distribution gives every worker all complete chunks.
2. Count transmitted bytes — 6 × 0.25 GB = 1.5 GB per worker — Each ring edge carries one chunk per round.
3. Find communication time — 1.5 GB ÷ 50 GB/s = 30 ms — All ring edges operate concurrently at the stipulated payload rate.
4. Place it on the critical path — Without overlap: 200 + 30 = 230 ms; with overlap: 200 + (30 − 20) = 210 ms — Only the 10 ms remaining after the compute interval extends the overlapped step.

**Result:** At 25 GB/s, communication takes 60 ms. With the same 20 ms overlap, step time becomes 240 ms. Faster networking changes exposed communication, not the fixed 200 ms of compute.

**Model boundary:** The uniform ring is a teaching model; actual collective algorithms and achievable overlap depend on the workload and fabric.

## The tradeoff

Choice: Wait for a compact topology placement instead of launching immediately across a wider fabric.

Benefit: Potentially reduce communication time and contention during a long job.

Cost: Increase queueing delay and possibly fragment available resources for other jobs.

## When the situation changes

Trigger: One rank skips a collective after an earlier application exception.

Mechanism: Other ranks wait for a required participant; replacing healthy network hardware would not fix the dependency mismatch.

Response: Correlate rank logs and collective progress, identify the first divergence, and restart from a valid state after correcting the cause.

## Apply the idea

GPU compute stays at 200 ms. Collective time rises from 30 to 60 ms, and counters show output queueing on a shared uplink while link errors remain unchanged. Would you start with faster GPUs, fabric traffic placement, or extra model memory?

<details>
<summary>Reveal the worked answer</summary>

Start with fabric traffic placement and the shared uplink. Inspect which traffic crosses it and whether competing transfers can be separated; verify the result with the same job.

The observed change is exposed communication. More GPU arithmetic throughput or model memory does not directly remove the measured output queue.

</details>

**The idea to keep:** Communication is part of the computation’s dependency graph, so local health does not establish global progress.

## Sources and reading boundaries

- [NCCL Collective Operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html) — Defines collective transformations and participation requirements. Read 2026-09-14. Inspected NCCL 2.31.2 documentation; the ring timing model is original and is not asserted to be the library’s chosen implementation.
- [Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) — First-party example of RoCE and InfiniBand clusters and joint network/software/placement tuning. Read 2026-09-14. March 2024 operator report; no reported benchmark ratio is generalized.
- [TPU v4: An Optically Reconfigurable Supercomputer for Machine Learning](https://arxiv.org/abs/2304.01433) — TPU v4: 4,096 chips in 64 racks, 64 chips in each electrical 4 × 4 × 4 block, and 48 optical circuit switches connecting the blocks. Read 2026-09-14. TPUv4 architecture, not every TPU generation; ICI optical circuits are not automatically long-haul WAN.
