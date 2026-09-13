# Measure complete useful work and diagnose exposed waits

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d02-productive-utilization`, then run `uv run gigawatt-expand`.

**3. Workloads and requirements · Authored draft**

Compare energy at fixed accepted output and align training dependencies with power rather than treating activity or mean kW as a service result.

**Driving question:** Does the power reduction improve energy for the same completed work, and what dependency is consuming the time?

## Keep the completed token workload fixed

Compare two runs that produce the same accepted outputs at the same quality within a common system boundary. Normalize run A’s whole-run mean power, duration and energy to one. If B uses 80 percent of the power for 150 percent of the duration, E_B/E_A = 0.8 × 1.5 = 1.2. It consumes 20 percent more energy for the same useful workload. This relative example teaches the tradeoff without inventing a hardware token-throughput result.

At 80 percent power, the break-even runtime is 1/0.8 = 1.25 times as long. A real power cap or serving policy might lie on either side; measure it. Include waiting, supporting equipment and the complete interval at the same meter. Do not compare a GPU compute-phase sample with rack AC energy over an entire job.

## Locate the dependency that exposed the wait

A synchronous training step may require collective gradient exchange before its next update can complete. If the required exchange is late, workers remain allocated and powered while dependent computation waits. Allocation is a reservation; useful training progress is an outcome. Communications may overlap arithmetic, so the presence of network traffic does not itself identify a stalled step.

Align collective timings, GPU activity and power, network counters and storage events. Then test a specific hypothesis: an exposed collective, input starvation, checkpoint traffic or another dependency. Merely observing lower GPU utilization cannot identify the root cause, nor can high memory activity be treated as universally maximum power.

## Connect the diagnosis to the facility

Synchronized dependency changes can align the power transitions of many workers. The production H100 example in the next lesson establishes that such variation is observed; the controlled traces explain how it adds at a shared meter. Removing a bottleneck may raise average useful compute and change power demand, so record token or training progress and the electrical trace together.

An inference load balancer places eligible requests on serving replicas. It does not perform the same function as an electrical buffer, and it cannot arbitrarily shift one worker inside a coupled training collective. Software and power remedies must match the actual dependency.

## Worked example: Less mean power, more energy for identical output

- Runs finish the same accepted token workload at the same quality.
- Power is the mean over each entire run at the same meter.
- Ratios are original teaching inputs, not a product benchmark.

1. Reference A — E_A = P_A × t_A — Count the whole run.
2. Changed run B — E_B = 0.8 P_A × 1.5 t_A = 1.2 E_A — The duration increase outweighs the reduction in mean power.
3. Break-even runtime — t_B / t_A = 1 / 0.8 = 1.25 — At this power ratio, duration must grow by less than 25 percent for energy to fall.

**Result:** B consumes 20 percent more energy for the same accepted output.

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
