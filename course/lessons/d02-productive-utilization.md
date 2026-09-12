# Busy, powered, and productive are different

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d02-productive-utilization`, then run `uv run gigawatt-expand`.

**Workloads and the infrastructure brief · Authored draft**

Read allocation, execution, waiting, power, and accepted output as separate traces instead of treating one utilization percentage as the answer.

**Driving question:** Why can lower average power accompany worse energy per useful result?

## Choose what your utilization number measures

A scheduler can allocate every accelerator to a job while that job waits for storage. From the scheduler's perspective, the devices are occupied. From the user's perspective, useful progress may have stopped. Meanwhile the equipment still consumes electricity. These are not contradictory observations; they describe different quantities. Allocation tells us who has reserved the resource. A hardware activity counter describes some measured device behavior. Productive utilization asks how much useful service the available system delivers.

Be careful with the word occupancy. In this lesson, allocation occupancy means the fraction of accelerators assigned to a workload. Some programming tools use occupancy for a much narrower hardware scheduling concept. A shared word does not make those metrics interchangeable. Always attach the numerator, denominator, and interval: allocated device-seconds divided by available device-seconds, active execution time divided by observation time, or accepted output divided by a stated reference capability.

Even useful execution needs an outcome definition. Repeating a failed job can keep devices active and consume energy without increasing accepted completed work. Communication can be essential to progress, so time outside arithmetic kernels is not automatically waste. The diagnostic question is whether that time is necessary for this workload, avoidable under another configuration, or evidence of a fault. A timeline with phase labels is more informative than a single percentage stripped of context.

## Compare two complete one-minute observations

Take a hypothetical system observed for sixty seconds. During compute phases it draws 60 kW and produces 1,000 accepted samples per second. During waiting phases it draws 25 kW and produces no accepted samples. Case A spends 45 seconds computing and 15 seconds waiting. The accepted output is 45,000 samples. Energy is power multiplied by time in each state: (60 × 45 + 25 × 15) divided by 3,600 equals approximately 0.854 kWh.

Case B spends 30 seconds computing and 30 seconds waiting. It produces 30,000 samples and uses (60 × 30 + 25 × 30)/3,600, or approximately 0.708 kWh. Its average power is lower: 42.5 kW instead of 51.25 kW. That does not make it more efficient for the accepted service. Convert each energy total to joules by multiplying kWh by 3.6 million, then divide by output. Case A uses about 68.3 joules per sample; Case B uses 85 joules per sample.

Why does the less active system use more energy per accepted result? Each minute includes time spent drawing power while producing no new accepted samples. Case B spreads that waiting energy across fewer results. This is a property of the declared scenario, not a universal claim that every system should run at maximum power. A different operating point might reduce compute power enough to improve energy per sample. The measurements must settle that comparison under the same service conditions.

Now consider a third minute in which no job is assigned and the system draws 12 kW while producing zero output. The energy is 0.2 kWh. Energy per accepted sample is undefined because the denominator is zero. Reporting zero would suggest perfect efficiency, while reporting an arbitrary giant number would hide the mathematical issue. Report idle energy and the absence of accepted output directly.

## Use the traces to select the next experiment

If allocation remains high while compute phases shrink and storage waits grow, adding more accelerators may simply create more waiting clients. A useful next experiment changes the suspected constraint: pre-stage the same inputs, vary checkpoint timing, or compare runs with measured storage service. The goal is to distinguish competing explanations while preserving the workload definition. Changing several knobs at once may improve performance but make the cause impossible to identify.

A utilization target can also conflict with responsiveness. An inference service may intentionally keep spare capacity so arriving requests do not join a long queue. Filling every available execution slot can raise throughput while harming tail latency. The unoccupied interval is then part of the service design rather than an obvious inefficiency. Decide which tradeoff is acceptable using the response-time and traffic requirements in the workload brief.

For training, distinguish a fast step from a fast completed job. A configuration might execute arithmetic more quickly but save larger checkpoints, recover more slowly, or repeat more work after failures. Productive utilization over the whole job includes those consequences. The same lesson applies to availability: equipment that is powered and responds to a health check can still fail to deliver the intended user service.

Collect synchronized traces of allocation, relevant device activity, workload phases, system power, and accepted output. Compare changes on a common clock before assigning causality. Correlation between a power drop and lower progress narrows the question, but does not identify the failing subsystem by itself. The most useful conclusion states both what the evidence supports and the controlled measurement that would resolve the remaining uncertainty.

## Worked example: Lower power, higher energy per accepted sample

- All power is measured at the same system AC boundary.
- Compute produces 1,000 accepted samples/s at 60 kW.
- Waiting produces no accepted samples at 25 kW.

1. Case A energy — (60 × 45 + 25 × 15) / 3,600 = 0.8542 kWh — Power in kW times seconds is converted to kWh by dividing by seconds per hour.
2. Case A output — 45 × 1,000 = 45,000 samples — Only the declared compute interval contributes output.
3. Case B energy — (60 × 30 + 25 × 30) / 3,600 = 0.7083 kWh — Less compute reduces total minute energy.
4. Normalize by service — A: 3,075,000 / 45,000 = 68.3 J/sample; B: 2,550,000 / 30,000 = 85 J/sample — Energy per result includes waiting energy.

**Result:** Case B draws less average power but uses about 24.4 percent more energy per accepted sample.

**Model boundary:** No GPU product, quality change, or facility-overhead behavior is represented.

## The tradeoff

Choice: Keep spare serving capacity to absorb incoming requests.

Benefit: Requests can begin sooner during bursts.

Cost: Average allocation can be lower, and idle energy must be included in the service account.

## When the situation changes

Trigger: Count allocated hardware as useful work.

Mechanism: A job retains resources during waits, retries, or failures while the allocation metric stays high.

Response: Inspect synchronized phase and accepted-output traces, then test the suspected bottleneck.

## Apply the idea

Case C computes for 50 seconds and waits for 10 seconds under the same power/output assumptions. What is its energy per sample?

<details>
<summary>Reveal the worked answer</summary>

65 J per accepted sample.

Energy is 60,000 × 50 + 25,000 × 10 = 3,250,000 J. Output is 50,000 samples. Dividing gives 65 J/sample.

</details>

**The idea to keep:** Define utilization by the resource and denominator; measure useful output independently of power.

## Sources and reading boundaries

- [MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) — The public MLPerf power description measures the system AC boundary during the performance measurement. Read 2026-09-06. Read the power-measurement description; this lesson uses its own synthetic traces and does not reproduce benchmark results.
- [NVIDIA — DGX SuperPOD Key Components](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-components.html) — Compute, storage, and communication are distinct cooperating parts of a cluster. Read 2026-09-06. Read the public architecture component page; the lesson makes no claim about a measured H100 utilization profile.
