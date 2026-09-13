# The workload has a rhythm

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d02-phases-and-envelopes`, then run `uv run gigawatt-expand`.

**3. Workloads and requirements · Authored draft**

Connect request queues and job phases to latency, aggregate power, and the limits of a benchmark-derived design envelope.

**Driving question:** How do batching and synchronized phases change demand without changing installed equipment?

## Teach prefill, decode and continuous batching directly

LLM prefill processes the prompt and creates initial request state. Decode extends the sequence over successive iterations. Time to first token includes queueing and prompt processing; time between output tokens concerns the stream after that. Prefill often offers more parallel matrix work, while low-batch decode can be memory-bandwidth constrained. This varies with model, hardware and batch; the phase name does not specify a fixed power draw.

vLLM describes continuous scheduling of running and waiting requests. When one sequence finishes, the scheduler can admit new work while others continue. Our two-slot illustration has A needing two decode steps, B five, and C three. C is already queued. The fixed batch waits for B; the continuous case admits C after A finishes. The cells represent iterations, not equal wall-clock durations or a measured speedup. Real admission also depends on prefill work, token budgets and KV capacity.

This matters to facility reasoning because active request membership changes compute and memory demand. Continuous batching is a documented serving mechanism, not a guarantee that rack power stays constant.

## Start with production evidence, then use a controlled trace

Choukse and colleagues from Microsoft, OpenAI and NVIDIA publish production DGX-H100 training power telemetry in Figure 1 of their 2025 paper. They connect synchronized compute and communication phases to power variation visible at larger electrical boundaries. The source figure is normalized, not a GB300 kW rating. Their later storage figures are simulations and their GB200 power-smoothing figure is a microbenchmark; neither is relabeled as production storage evidence.

The following 60-second teaching cycle is original and deliberately simplified: 30 seconds compute at 120 kW, 15 exchange at 40 kW and 15 save at 60 kW. Its energy is 5,100 kJ and mean power 85 kW. Four coincident copies give 480, 160 and 240 kW at the shared meter, with 340 kW mean. These values explain addition and timing, rather than claiming a particular training job has these phase lengths.

## Use staggering only when its dependency assumptions hold

If four independent periodic jobs can shift by 0, 15, 30 and 45 seconds without extra waiting, contention or missed deadlines, two compute while one exchanges and one saves: 340 kW throughout the ideal cycle. Their energy remains 5.667 kWh. This is a conditional scheduling thought experiment, not an assertion that production AI clusters routinely use these offsets.

Workers inside one synchronous job are a different case. Delaying a participant may force the others to wait at a collective, violating the unchanged-duration assumption. Keep the staggering and dependency slides together. The lesson is to identify which scheduling freedom actually exists before proposing it as a power remedy.

## Read the trace to choose a response

Read peak power, change magnitude, transition duration, repetition and energy at the intended meter. In a separate assumed transition, 480 to 160 kW over two seconds is a 160 kW/s decrease; over 0.2 seconds it is 1,600 kW/s. The same two plateaus can require a very different response. These ramp examples do not silently change the energy of the ideal stepwise cycle.

Schedulers change eligible workload timing. Supported GPU power controls change device behavior, potentially affecting runtime or energy. Storage changes source-facing power within its conversion, charge, discharge and usable-energy limits. Choose among them using workload dependencies and electrical timescales. A request load balancer does not provide stored energy, and a buffer cannot sustain an average power deficit indefinitely.

## End with the engineering handoff

The presentation ends with a workload brief rather than arithmetic threshold quizzes. Carry model and hardware identity, software/precision, prompt/output lengths, active sessions, token delivery, first-token targets and quality. Add a measured power trace, complete-run energy and recovery cases at a declared boundary. This supports the next siting/supply decision; unknown rack throughput and electrical behavior remain unknown.

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

Choice: Admit new inference requests during ongoing decode rather than waiting for a fixed batch to finish.

Benefit: Released execution/cache capacity may serve queued work sooner.

Cost: Admission and prefill still consume resources; memory occupancy, latency, quality and power need measurement.

## When the situation changes

Trigger: Assume a smooth average remains smooth during synchronized job transitions.

Mechanism: Several jobs change phase together, creating a large aggregate step.

Response: Use a time-resolved workload envelope and test controls/scheduling against the relevant transitions.

## Apply the idea

A distributed training workload has acceptable average power but large synchronized transitions. What evidence would distinguish scheduling freedom from a need for local buffering or device controls?

<details>
<summary>Reveal the worked answer</summary>

Inspect the dependency graph and deadlines, measure coincident power at the shared boundary with relevant time resolution, and test qualified controls or buffers against peak power, transition speed, usable energy and recharge.

A flatter hypothetical sum does not prove jobs can be shifted. A mean does not reveal transition duration, and a buffer cannot remove a sustained energy deficit.

</details>

**The idea to keep:** The timing of work matters alongside its total amount; a mean load does not define a demand envelope.

## Sources and reading boundaries

- [NVIDIA Triton — Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html) — Dynamic batching can combine requests and introduce a configurable waiting interval. Read 2026-09-06. Read the public dynamic-batcher and delayed-batching sections. All timings and throughput numbers in this lesson are hypothetical.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — Synchronized AI load changes motivate coordination across power-system levels. Read 2026-09-06. Read the public white-paper landing page only, not the downloadable full white paper; no universal measured waveform is asserted.
- [vLLM — Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) — Prefill and decode, key/value-cache allocation, continuous scheduling of new and running requests, serving load balancing, and latency/throughput measurement. Read 2026-09-12. Read the engine initialization, scheduler and forward-pass sections, disaggregated prefill/decode overview, serving/load-balancer description and metric definitions. The article describes V1 at commit 42172ad from August 2025; it is not a claim about every inference engine. Prefill often has high arithmetic intensity and decode often has a bandwidth constraint, with workload/batch/hardware-dependent exceptions. No published speedup is generalized to the course case.
- [Microsoft, OpenAI and NVIDIA — Power Stabilization for AI Training Datacenters](https://arxiv.org/html/2508.14318v1) — Production training power variation motivates the connection from synchronized compute and communication to facility power delivery; compares software smoothing, GPU controls and rack storage. Read 2026-09-12. Read abstract and sections I–II plus IV mitigation descriptions, with figure captions 1 and 5–7. Figure 1 is production DGX-H100 telemetry; figure 5 is a GB200 microbenchmark; figures 6–7 are simulated smoothing/storage results. These are not interchangeable measured deployment claims. Staggered scheduling is a proposed direction rather than evidence that generic independent-job staggering is normal deployed practice. Storage has conversion losses and finite power/energy; do not reuse the paper’s unqualified no-wasted-energy wording.

## Check your understanding: Same hardware, different service

Pause and make a prediction, then compare your reasoning.

Two hypothetical inference services have the same accelerator count and average IT demand. One meets its response-time target; the other builds a queue whenever requests arrive in bursts.

**Pause and predict:** Would you give them the same usable-service rating? Name the missing evidence.

<details>
<summary>Compare your reasoning</summary>

No. Equal hardware and average demand do not establish equal output within the response-time target.

Compare accepted responses under the same arrival pattern, quality requirement and latency target, including the slow end of the response-time distribution. Then measure the load phases and simultaneous peaks needed to deliver that service. A mean demand alone does not define its infrastructure envelope.

</details>

**The next problem:** Once the workload has an explicit demand envelope, where can the required power actually be delivered?

Continue in **Siting, grid connection and supply**: A contract is not a cable.
