# The powered cluster that keeps waiting

Generated reading view. Edit [`course/expansion/capstones.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/capstones.json), lesson `c04-stalled-job`, then run `uv run gigawatt-expand`.

**Integrated practice · Authored draft**

Build a serial job timeline from supplied measurements, compare two proposed improvements, and test recovery rather than relying on GPU occupancy.

**Driving question:** Which measurement would distinguish a fabric limit from a storage or compute limit?

## Name what the job is waiting for

A hypothetical distributed job repeats a cycle containing 60 seconds of useful compute, a 20-second communication phase, and a 10-second blocking checkpoint pause. The supplied trace shows no overlap between these phases. A dashboard reports that the devices remain allocated for the entire cycle, but allocation alone cannot tell you how much useful work completes. Some waiting may also involve active instructions, so a generic hardware busy counter is not a substitute for the application trace. Use the actual job boundary and a declared definition of useful progress.

The communication phase moves a supplied 800 GB payload across one measured bottleneck at an effective 40 GB/s. The checkpoint writes 200 GB at an effective 20 GB/s. These decimal units and achieved rates are scenario measurements, not peak port specifications. The numbers are deliberately consistent with the phase durations. A real collective can have multiple rounds, aggregation and synchronization effects; do not apply one-payload division to an unidentified collective algorithm. This capstone provides the transfer model so its calculation can be checked.

## Make a falsifiable improvement prediction

Proposal N doubles the achieved communication rate while leaving computation and storage unchanged. Proposal S doubles the checkpoint write rate with the rest unchanged. Since the supplied trace is serial, calculate each phase separately and add the times. Predict a new cycle duration before running the experiment. If observed completion does not improve as predicted, examine whether the achieved rate changed at the bottleneck, whether another segment expanded, whether synchronization moved the critical path, or whether the original no-overlap assumption was wrong.

A complete recovery exercise goes beyond write speed. After a checkpoint is committed, the job must find compatible state, read it, restore execution and produce valid progress. A checkpoint that is fast but unrecoverable is not a successful service. Record the application version, checkpoint identifier, storage path, restart duration and output check. Compare ordinary completion time with time lost during failures over an appropriate interval. Power and cooling adequacy remain prerequisites; they do not establish these information and software paths.

## Worked example: Compare two bottleneck interventions

- Synthetic serial cycle: 60 s useful compute, 800 GB communication, 200 GB blocking checkpoint.
- Achieved payload rates: 40 GB/s communication and 20 GB/s checkpoint writing; no overlap or restart in the baseline cycle.
- Both proposals affect only their named rate.

1. Baseline communication is 800/40 = 20 s; checkpoint write is 200/20 = 10 s.
2. Baseline cycle duration is 60 + 20 + 10 = 90 s. Useful-compute share is 60/90 = 66.7%.
3. N gives 800/80 = 10 s communication, hence an 80 s cycle and 90/80 = 1.125 times the baseline cycle throughput.
4. S gives 200/40 = 5 s checkpoint write, hence an 85 s cycle and 90/85 ≈ 1.059 times the baseline cycle throughput.
5. If both independently hold, the cycle becomes 60 + 10 + 5 = 75 s, or 1.20 times baseline throughput. Neither rate doubling doubles useful throughput.

**Result:** Under this serial trace, the network proposal saves ten seconds per cycle and the storage proposal saves five. Validate the achieved rates and the changed cycle in an experiment.

**Model boundary:** The model excludes overlap, collective details, startup overhead and failure recovery from ordinary cycle time. No rack power, advertised FLOPS or generic GPU utilization value is converted into job output.

## The tradeoff

Choice: Invest in the larger measured time reduction first.

Benefit: The predicted gain is tied to a named bottleneck and can be checked against a trace.

Cost: Acquisition, disruption, scaling and recovery behavior may differ; the biggest speed improvement is not automatically the best economic choice.

## When the situation changes

Trigger: The communication rate doubles but job duration barely changes.

Mechanism: The assumed bottleneck may not be on the job's critical path, or another shared resource may now dominate.

Response: Collect aligned compute, communication, storage and synchronization traces, then compare the observed intervals with the prediction.

## Apply the idea

A revised implementation overlaps 8 seconds of the baseline 10-second checkpoint pause with computation. Communication remains serial at 20 seconds. What is the new cycle duration? Would doubling checkpoint write rate still save five seconds?

<details>
<summary>Reveal the worked answer</summary>

The cycle is 60 + 20 + (10 − 8) = 82 seconds. A five-second write can fit entirely inside the available eight-second overlap window, reducing the cycle only to 80 seconds.

The visible critical-path checkpoint cost is two seconds. Faster storage saves only exposed time, provided the same overlap window and compute behavior really hold. A phase's total duration and its contribution to end-to-end completion are different quantities.

</details>

**The idea to keep:** A job's critical path is a time budget. Improve the segment that governs completion and measure whether the expected gain appears.

## Sources and reading boundaries

- [Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) — Provides scheduling-topology context; all payloads, phase times and interventions are original synthetic scenarios. Read 2026-09-06. Selected topology documentation, not a pinned-release workload benchmark. Scheduling topology does not by itself specify packet routing or achieved communication rate.
