# Measure complete useful work and diagnose exposed waits

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d02-productive-utilization`, then run `uv run gigawatt-expand`.

**3. Workloads and requirements · Authored draft**

Compare energy at fixed accepted output and align training dependencies with power rather than treating activity or mean kW as a service result.

**Driving question:** Does the power reduction improve energy for the same completed work, and what dependency is consuming the time?

## Keep the completed token workload fixed

Compare two runs that produce the same accepted outputs at the same quality within a common system boundary. Run A averages 100 kW for 10 minutes: 100 × 10/60 = 16.7 kWh. Run B averages 80 kW for 15 minutes: 80 × 15/60 = 20 kWh. B draws less power but takes five minutes longer, so it consumes 20 percent more energy for the same work.

Count waiting, supporting equipment and the complete run at the same meter. Compare these energy totals alongside accepted output and response time. A short GPU compute-phase power sample and rack AC energy over an entire job describe different boundaries.

## Locate the dependency that exposed the wait

A synchronous training step may require collective gradient exchange before its next update can complete. If the required exchange is late, workers remain allocated and powered while dependent computation waits. Allocation is a reservation; useful training progress is an outcome. Communications may overlap arithmetic, so the presence of network traffic does not itself identify a stalled step.

Align collective timings, GPU activity and power, network counters and storage events. Then test a specific hypothesis: an exposed collective, input starvation, checkpoint traffic or another dependency. Merely observing lower GPU utilization cannot identify the root cause, nor can high memory activity be treated as universally maximum power.

## Connect the diagnosis to the facility

Synchronized dependency changes can align the power transitions of many workers. The production H100 example in the next lesson establishes that such variation is observed; the controlled traces explain how it adds at a shared meter. Removing a bottleneck may raise average useful compute and change power demand, so record token or training progress and the electrical trace together.

An inference load balancer places eligible requests on serving replicas. It does not perform the same function as an electrical buffer, and it cannot arbitrarily shift one worker inside a coupled training collective. Software and power remedies must match the actual dependency.

## Worked example: Less mean power, more energy for identical output

- Runs finish the same accepted token workload at the same quality.
- Power is the mean over each entire run at the same meter.
- Run A averages 100 kW for 10 minutes; run B averages 80 kW for 15 minutes.

1. Run A — 100 kW × (10 / 60) h = 16.7 kWh — Ten minutes is one-sixth of an hour.
2. Run B — 80 kW × (15 / 60) h = 20 kWh — The extra five minutes outweighs the reduction in mean power.

**Result:** Run B consumes 20 kWh instead of 16.7 kWh for the same accepted output: 20 percent more energy.

**Model boundary:** A real power-performance curve and quality-controlled benchmark are needed to choose a configuration.

## The tradeoff

Choice: Keep spare serving capacity to absorb incoming requests.

Benefit: Requests can begin sooner during bursts.

Cost: Average allocation can be lower, and idle energy must be included in the service account.

## When the situation changes

Trigger: Count allocated hardware as useful work.

Mechanism: A job retains resources during waits, retries, or failures while the allocation metric stays high.

Response: Inspect synchronized phase and accepted-output traces, then test the suspected bottleneck.

## Apply the idea

A power-capped run draws less mean power but shows longer collective waits. Which measurements would distinguish an energy improvement from a slower, less efficient job?

<details>
<summary>Reveal the worked answer</summary>

Measure whole-run duration and integrated energy, accepted output/quality, and aligned collective and GPU activity traces under both settings.

Mean power alone lacks duration and output. Correlated traces locate an exposed dependency; a controlled comparison tests whether the cap changed it.

</details>

**The idea to keep:** Define utilization by the resource and denominator; measure useful output independently of power.

## Sources and reading boundaries

- [MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) — The public MLPerf power description measures the system AC boundary during the performance measurement. Read 2026-09-06. Read the power-measurement description; this lesson uses its own synthetic traces and does not reproduce benchmark results.
- [NVIDIA — DGX SuperPOD Key Components](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-components.html) — Compute, storage, and communication are distinct cooperating parts of a cluster. Read 2026-09-06. Read the public architecture component page; the lesson makes no claim about a measured H100 utilization profile.
- [Microsoft, OpenAI and NVIDIA — Power Stabilization for AI Training Datacenters](https://arxiv.org/html/2508.14318v1) — Production training power variation motivates the connection from synchronized compute and communication to facility power delivery; compares software smoothing, GPU controls and rack storage. Read 2026-09-12. Read abstract and sections I–II plus IV mitigation descriptions, with figure captions 1 and 5–7. Figure 1 is production DGX-H100 telemetry; figure 5 is a GB200 microbenchmark; figures 6–7 are simulated smoothing/storage results. These are not interchangeable measured deployment claims. Staggered scheduling is a proposed direction rather than evidence that generic independent-job staggering is normal deployed practice. Storage has conversion losses and finite power/energy; do not reuse the paper’s unqualified no-wasted-energy wording.
