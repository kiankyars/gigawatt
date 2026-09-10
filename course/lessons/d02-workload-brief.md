# Design for a job, not a rack count

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d02-workload-brief`, then run `uv run gigawatt-expand`.

**D02 · Authored draft · Objectives:** D02.1, D02.4

Turn contrasting training and inference requests into explicit compute, memory, communication, storage, and service requirements.

**Driving question:** What must the infrastructure deliver for this workload to count as successful?

## A request for accelerators leaves the problem undefined

A team asks for 64 accelerators. Before deciding what building infrastructure they need, ask what those accelerators must accomplish. One team may want to complete a training experiment before a deadline. Another may need to answer interactive requests within a latency target while traffic varies. Training changes model parameters by processing examples and updating state. Inference uses a configured model to produce outputs. Both can occupy similar equipment, yet their service requirements can differ substantially.

An infrastructure brief makes those requirements explicit. Name the model and implementation, numerical representation, input sizes, output or quality criterion, expected concurrency, and measurement period. For training, define the accepted progress or completed workload, not merely how long a process runs. For inference, define successful requests, response-time requirements, and the traffic pattern. A tokens-per-second number without input/output lengths and latency conditions can hide a very different service.

Translate the brief into several interacting resources. Parameters and working state need memory; arithmetic needs processors; distributed work exchanges data; input and checkpoints use storage; all equipment needs electrical and thermal capacity. The resource list alone is insufficient. Ask how much of each resource the job needs at each phase, what can overlap, and what happens if one arrives late. The measured training step or request timeline connects the software requirement to the physical system.

## Build a bounded memory and throughput estimate

Use a hypothetical model with 12 billion parameters. Suppose inference stores each parameter in two bytes: the weights occupy 24 billion bytes, or 24 decimal GB. The selected workload additionally needs an assumed 20 GB for cache and temporary workspace, plus an 8 GB reservation. That produces a 52 GB memory budget. These extra quantities are inputs supplied by our hypothetical measurement, not universal multipliers. A different context length or batching policy can change them.

For a separate training configuration of the same parameter count, assume the supplied accounting is 16 bytes per parameter across weights, gradients, master weights, and optimizer state. That gives 192 GB. Add an assumed 64 GB of peak activations and working memory to reach 256 GB. Two devices with 80 GB each provide only 160 GB of aggregate capacity, so even a perfect partition cannot fit this stated budget. Four provide 320 GB in aggregate, which passes the first arithmetic screen.

Passing that screen does not establish that the workload fits or runs efficiently. The implementation must partition the state so no device exceeds its own capacity, preserve necessary buffers, and communicate intermediate information. Four separate 80 GB pools are not automatically one unrestricted 320 GB pool. Conversely, techniques that change state representation or recomputation may reduce memory at the expense of arithmetic, communication, or complexity. Keep those changes explicit instead of quietly altering the original brief.

Now suppose a supplied benchmark reports 400 accepted training samples per second for a particular eight-device configuration. If the same performance is sustained for 20 hours, the arithmetic is 400 × 20 × 3,600 = 28.8 million samples. That is a conditional throughput estimate. It does not prove convergence, because progress per example and the stopping criterion are separate parts of the experiment. It also does not predict a 64-device result by multiplying by eight without a scaling measurement.

## Write acceptance criteria that survive a demonstration

A useful acceptance statement might say: the specified inference service must process at least 120 accepted requests per second under the supplied arrival trace, with a declared percentile of end-to-end response times below the agreed limit. It must use the named model quality and input/output distributions, within a specified system power envelope. State which failures or maintenance conditions are included. The actual numbers are application choices; the form prevents a fast demonstration from silently changing the test.

For training, specify a complete job or validated progress target and its completion deadline, including input staging, checkpoint overhead, expected recoveries, and final output handling. Separate sustained service from a best short interval. A fast kernel benchmark verifies that kernel on its tested configuration. It does not establish storage recovery behavior, production tail latency, or cooling capacity during the hottest allowed condition. Benchmarks become valuable when their scope matches a question rather than being asked to certify the whole facility.

There is a consequential choice between buying headroom and narrowing the supported workload envelope. Larger memory and additional infrastructure may accommodate broader future demands, but capacity held in reserve costs money and still requires compatible interfaces. Narrowing the brief can produce a more efficient system for a specific job, yet a later workload change may force a redesign. Record uncertainty as an explicit range or scenario, so the team can decide where flexibility is worth paying for.

When someone converts site megawatts straight into tokens, this brief is the missing bridge. Electricity establishes a resource budget. A declared workload model and measurements establish how the system turns that budget into accepted service. Neither substitutes for the other. The correct answer to an underspecified brief is a short list of measurements or decisions that would make it solvable.

## Worked example: Two memory envelopes for one parameter count

- Decimal GB means one billion bytes.
- All per-parameter and workspace values are hypothetical inputs.
- Device capacity is 80 GB; no unlisted memory overhead is assumed in the screening calculation.

1. Inference weights — 12 × 10^9 parameters × 2 bytes = 24 GB — Parameter count multiplied by bytes per parameter gives storage.
2. Inference total — 24 + 20 + 8 = 52 GB — Add measured/assumed workspace and the declared reservation.
3. Training state — 12 × 10^9 × 16 bytes = 192 GB — The supplied training representation keeps more state than the inference weights.
4. Training peak — 192 + 64 = 256 GB — Two devices provide 160 GB and fail this aggregate screen; four provide 320 GB but still require a valid partition.

**Result:** The same model count produces different memory requirements under different workloads.

**Model boundary:** These are hypothetical state budgets, not measured requirements for a named model or a guarantee of multi-device fit.

## The tradeoff

Choice: Reserve capacity for a broader workload envelope.

Benefit: Future inputs, concurrency, or implementations may fit without replacing the system.

Cost: Additional capacity costs money and can remain unused; aggregate capacity still needs a workable partition.

## When the situation changes

Trigger: Accept a short compute benchmark as proof of production service.

Mechanism: The test excludes queueing, data movement, recovery, or the required workload distribution.

Response: Match acceptance conditions to the actual service and measure the missing phases.

## Apply the idea

If inference workspace rises from 20 to 44 GB while the other assumptions stay fixed, does the 80 GB device pass the arithmetic screen?

<details>
<summary>Reveal the worked answer</summary>

Yes: 24 + 44 + 8 = 76 GB, leaving 4 GB beyond the stated budget.

This is only a capacity screen. Unmodeled overhead, implementation allocation, and workload performance still need measurement.

</details>

**The idea to keep:** Start with accepted work and its constraints; hardware quantities follow from a measured workload model.

## Sources and reading boundaries

- [NVIDIA — DGX SuperPOD Key Components](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-components.html) — A documented AI cluster architecture includes compute, management, networking, and storage components. Read 2026-09-06. Read the public component and design-requirement page for the H100 reference architecture; no product count or performance is copied into the hypothetical brief.
- [MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) — Benchmark results depend on a declared workload scenario and measurement conditions. Read 2026-09-06. Read the public scenario and power-measurement descriptions; no named system performance is asserted.
