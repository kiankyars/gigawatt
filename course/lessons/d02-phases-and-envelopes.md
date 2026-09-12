# The workload has a rhythm

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d02-phases-and-envelopes`, then run `uv run gigawatt-expand`.

**D02 · Authored draft · Objectives:** D02.3, D02.4, D02.1

Connect request queues and job phases to latency, aggregate power, and the limits of a benchmark-derived design envelope.

**Driving question:** How do batching and synchronized phases change demand without changing installed equipment?

## A batch trades waiting for a different execution shape

An inference request can begin immediately or wait briefly so the server can process several requests together. A batch is that group of inputs executed together under the implementation's rules. Combining requests can improve throughput by changing how overhead and hardware work are shared. It can also add queueing delay. NVIDIA Triton's public documentation describes dynamic batching and a configurable delay limit; it does not promise that every model benefits or that a particular delay is safe for every service.

Use an original toy measurement: one request takes 8 milliseconds to execute, while a batch of four takes 20 milliseconds. With a permanently full queue, sequential single-request execution produces 1/0.008 = 125 requests per second. Full batches produce 4/0.020 = 200 requests per second. The batched path has higher throughput under those assumed measurements, but each batch still requires 20 milliseconds of execution after its requests have been gathered. Throughput is not the same quantity as one request's response time.

Suppose requests arrive every 6 milliseconds and a batch begins when four have arrived. They arrive at 0, 6, 12, and 18 milliseconds. Starting at 18 and finishing at 38 means the first request experiences 38 milliseconds from arrival to completion, while the fourth experiences 20. Their average is 29 milliseconds. This controlled example excludes network and other queueing delays. It exposes the mechanism: waiting to form the group changes different users' latency by different amounts.

At one arrival every six milliseconds, the incoming rate is about 166.7 requests per second. That already exceeds the assumed single-request execution capacity of 125 requests per second. Removing batch-gathering delay therefore does not solve the sustained service with one execution instance: its queue would grow. The comparison must satisfy both the arrival-rate requirement and the response-time requirement, rather than improving one while silently failing the other.

## Shared phase timing changes the aggregate trace

Now turn from serving requests to four independent hypothetical jobs. Each job's sixty-second cycle contains thirty seconds of compute at 120 kW, fifteen seconds of communication at 40 kW, and fifteen seconds of checkpointing at 60 kW. Those are scenario inputs, not a universal training waveform. One job uses 120 × 30 + 40 × 15 + 60 × 15 = 5,100 kW-seconds per cycle, so its average is 85 kW. Four jobs average 340 kW.

If all four begin each phase together, aggregate power is 480 kW during compute, 160 kW during communication, and 240 kW during checkpointing. If independent jobs can instead be offset by fifteen seconds, the idealized system always has two computing, one communicating, and one checkpointing. Aggregate power then stays at 2 × 120 + 40 + 60 = 340 kW. Cycle energy is unchanged because each job spends the same time in each state.

The condition of independence is essential. Participants in one distributed training job may need to reach a communication point together. Arbitrarily delaying one participant can make the others wait and change both completion time and the power profile. Even independent jobs may contend for the same fabric or storage. Our perfect staggering result is a controlled scheduling illustration, not a promise that a production cluster can achieve a flat trace without side effects.

The original synchronized step from 480 to 160 kW is a 320 kW change. If that transition occurs over two seconds in a supplied trace, its average rate of change over those two seconds is 160 kW per second downward. A five-minute average would not reveal that rate. Electrical equipment and controls encounter behavior on multiple timescales, so a facility brief must include the time resolution relevant to the particular question.

## Specify the envelope a test must actually explore

A workload design envelope combines several conditions: input sizes, concurrency, execution settings, traffic or phase timing, minimum accepted throughput, latency or deadline, and electrical/thermal limits. It also says which degraded states are supported. Write these down before running the demonstration. Otherwise, a test can succeed because its queue was permanently full, its input was unusually small, or its measurement omitted the difficult startup and recovery intervals.

For the toy inference example, a requirement below 30 milliseconds for every request would reject the four-request gathering behavior because the first request takes 38 milliseconds. The higher 200 requests/s full-queue throughput does not override the response-time requirement. A different batch limit, a shorter gathering delay, more execution instances, or a changed requirement might be appropriate. Each changes a stated mechanism, and each needs a new measurement under the intended arrival pattern.

For the job example, record both the 340 kW average and the synchronized phase values. If the proposed scheduling policy depends on staggering, verify that it preserves accepted work and remains effective when jobs start, finish, checkpoint, or recover at unexpected times. A power cap may reduce a peak while extending the job; a storage schedule may smooth writes while increasing recovery exposure. Those consequences belong in the decision, not in a footnote after the power graph.

A good benchmark narrows uncertainty. It can verify the tested implementation's response under declared conditions. It cannot by itself validate untested input distributions, multi-day failure behavior, or every operating state of the facility. Describe the boundary of what was tested, then select the next scenario most likely to challenge the design. That is how a workload measurement becomes a useful infrastructure requirement.

## Worked example: Synchronized versus staggered independent jobs

- Four identical, independent jobs each repeat a 60-second cycle.
- Per job: 30 s at 120 kW, 15 s at 40 kW, and 15 s at 60 kW.
- Staggering causes no extra waiting or resource contention in this model.

1. One-job average — (120 × 30 + 40 × 15 + 60 × 15) / 60 = 85 kW — Weight each power by its time fraction.
2. Four-job energy — 4 × 5,100 / 3,600 = 5.667 kWh per cycle — The same individual phase durations imply the same aggregate energy.
3. Synchronized maximum — 4 × 120 = 480 kW — All jobs occupy the high-power phase simultaneously.
4. Ideal staggered power — 2 × 120 + 40 + 60 = 340 kW — A fifteen-second offset maintains this composition of phases.

**Result:** The ideal staggering lowers the peak from 480 to 340 kW while preserving cycle energy.

**Model boundary:** This result requires independent jobs and excludes contention; it cannot be imposed on synchronized workers without analysis.

## The tradeoff

Choice: Delay requests to form larger batches.

Benefit: The measured execution can produce more requests per second.

Cost: Gathering and execution delay may violate the service latency requirement.

## When the situation changes

Trigger: Assume a smooth average remains smooth during synchronized job transitions.

Mechanism: Several jobs change phase together, creating a large aggregate step.

Response: Use a time-resolved workload envelope and test controls/scheduling against the relevant transitions.

## Apply the idea

In the four-request example, what are the four response times, and does every request meet a 30 ms target?

<details>
<summary>Reveal the worked answer</summary>

38, 32, 26, and 20 ms; the first two miss the target.

Average response time is 29 ms, yet an average below 30 ms does not mean every request meets a 30 ms requirement.

</details>

**The idea to keep:** The timing of work matters alongside its total amount; a mean load does not define a demand envelope.

## Sources and reading boundaries

- [NVIDIA Triton — Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html) — Dynamic batching can combine requests and introduce a configurable waiting interval. Read 2026-09-06. Read the public dynamic-batcher and delayed-batching sections. All timings and throughput numbers in this lesson are hypothetical.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — Synchronized AI load changes motivate coordination across power-system levels. Read 2026-09-06. Read the public white-paper landing page only, not the downloadable full white paper; no universal measured waveform is asserted.

## D02 domain check-in: Same hardware, different service

Optional: pause and make a prediction, then compare your reasoning. You can continue whenever you are ready.

Two hypothetical inference services have the same accelerator count and average IT demand. One meets its response-time target; the other builds a queue whenever requests arrive in bursts.

**Pause and predict:** Would you give them the same usable-service rating? Name the missing evidence.

<details>
<summary>Compare your reasoning</summary>

No. Equal hardware and average demand do not establish equal output within the response-time target.

Compare accepted responses under the same arrival pattern, quality requirement and latency target, including the slow end of the response-time distribution. Then measure the load phases and simultaneous peaks needed to deliver that service. A mean demand alone does not define its infrastructure envelope.

</details>

**The next problem:** Once the workload has an explicit demand envelope, where can the required power actually be delivered?

Continue in **D03**: A contract is not a cable.
