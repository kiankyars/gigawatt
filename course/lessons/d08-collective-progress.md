# A collective makes waiting contagious

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d08-collective-progress`, then run `uv run gigawatt-expand`.

**D08 · Authored draft · Objectives:** D08.1, D08.2, D08.3, D08.5

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

## Worked example: Eight ranks on a fictional ring

- Eight ranks each contribute a 1 GB input buffer.
- Every ring edge sustains 25 GB/s; each of fourteen rounds has 10 microseconds of startup overhead.
- A training step also has 200 ms of computation; no communication overlaps that computation.

1. Calculate sent bytes per rank — 2 × (8 − 1) / 8 × 1 GB = 1.75 GB — Seven reduce-scatter and seven all-gather rounds each send a 0.125 GB chunk.
2. Calculate collective time — 1.75 / 25 s + 14 × 10 microseconds = 70.14 ms — Bandwidth time and stipulated startup time are added.
3. Calculate step time — 200 + 70.14 = 270.14 ms — The collective is fully exposed after computation.
4. Halve available ring bandwidth — 1.75 / 12.5 s + 0.14 ms = 140.14 ms; step = 340.14 ms — A constrained effective ring rate adds 70 ms without changing the compute hardware.

**Result:** The step becomes about 25.9% longer under the stipulated bandwidth degradation, while every accelerator can remain powered and locally healthy.

**Model boundary:** The model uses a single uniform effective ring rate. Real routing, algorithms, overlap and reduction costs must be measured.

## The tradeoff

Choice: Wait for a compact topology placement instead of launching immediately across a wider fabric.

Benefit: Potentially reduce communication time and contention during a long job.

Cost: Increase queueing delay and possibly fragment available resources for other jobs.

## When the situation changes

Trigger: One rank skips a collective after an earlier application exception.

Mechanism: Other ranks wait for a required participant; replacing healthy network hardware would not fix the dependency mismatch.

Response: Correlate rank logs and collective progress, identify the first divergence, and restart from a valid state after correcting the cause.

## Apply the idea

A communication improvement reduces the 70.14 ms collective to 35.07 ms while computation stays at 200 ms. What is the end-to-end speedup?

<details>
<summary>Reveal the worked answer</summary>

270.14 / 235.07 ≈ 1.149, about a 14.9% throughput increase for repeated identical steps.

Only part of the step improves. The communication phase is twice as fast, but the whole dependency chain is not. If the job also has input, checkpoint or queueing overhead, the total-service gain is smaller still.

</details>

**The idea to keep:** Communication is part of the computation’s dependency graph, so local health does not establish global progress.

## Sources and reading boundaries

- [NCCL Collective Operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html) — Defines collective transformations and participation requirements. Read 2026-09-06. Inspected NCCL 2.31.2 documentation; the ring timing model is original and is not asserted to be the library’s chosen implementation.
- [Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) — First-party example of RoCE and InfiniBand clusters and joint network/software/placement tuning. Read 2026-09-06. March 2024 operator report; no reported benchmark ratio is generalized.
