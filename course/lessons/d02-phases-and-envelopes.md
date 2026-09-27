# The workload has a rhythm

**3. Workloads and requirements**

Connect request queues and job phases to latency, aggregate power, and the limits of a benchmark-derived design envelope.

**Driving question:** How do batching and synchronized phases change demand without changing installed equipment?

## Prefill and decode use hardware differently

LLM prefill processes the prompt and creates the request’s initial KV cache. Many prompt tokens can be processed together, giving the GPU substantial parallel matrix work: prefill is usually compute-bound. Decode generates tokens successively. At low batch sizes, fetching model weights and cached context can take more time than the arithmetic itself: decode is often memory-bandwidth-bound. Larger batches, long contexts, model design and the hardware can change which resource limits performance. Time to first token includes queueing and prompt processing; time between output tokens concerns the stream after that.

Weight reuse helps explain why prefill is usually compute-bound while low-batch decode is memory-bandwidth-bound. The model’s weights live in the GPU’s high-bandwidth memory (HBM). A matrix operation copies a small block of them, a tile, into much smaller on-chip memory, where one token vector or several can use it before it is replaced. With eight token vectors instead of one, the same tile read supports eight times the arithmetic. Prefill supplies many prompt tokens at once, and batching decode requests supplies several, so both reduce the weight bytes fetched per token. On-chip memory is far smaller than HBM, so this reuse happens one tile at a time rather than by keeping the whole model on the chip.

vLLM describes continuous scheduling of running and waiting requests. When one sequence finishes, the scheduler can admit new work while others continue. Take two batch slots and three requests: A needs two decode steps, B five and C three, and C is already queued. The fixed batch waits for B; the continuous case admits C after A finishes. Each step is one iteration, not an equal wall-clock duration, and the comparison is not a measured speedup. Real admission also depends on prefill work, token budgets and KV capacity.

This matters to facility reasoning because active request membership changes compute and memory demand. Continuous batching is a documented serving mechanism, not a guarantee that rack power stays constant.

These bottlenecks are tendencies. A short prompt may offer too little parallel matrix work to saturate compute. A large decode batch can reuse each loaded weight across enough tokens that matrix multiplication becomes compute-bound, while attention or interconnect traffic may still be limiting. Model, context length, batch size, parallelism and hardware determine the actual bottleneck.

## NVIDIA uses separate racks for prefill and decode

NVIDIA Groq 3 LPX is a rack of 256 Groq language processing unit (LPU) accelerators deployed alongside Vera Rubin NVL72 GPU racks. In NVIDIA’s standard prefill–decode configuration, Rubin processes the prompt and transfers its KV cache once per turn. Groq LPX then uses that cache and model weights held in on-chip static random-access memory (SRAM) to generate the response. Each LPU has 500 megabytes (MB) of SRAM with 150 terabytes per second (TB/s) of bandwidth, 128 GB across the rack, which suits decode's constant weight reads but gives each chip far less capacity than a GPU's HBM. The two phases can therefore use hardware suited to different demands, connected by a cache handoff.

This example pairs Groq with Rubin GPUs. NVIDIA also describes an attention–feed-forward network (FFN) configuration that divides work within decode, plus speculative decoding with a separate draft model. The standard prefill–decode split shows the hardware division most clearly.

## Start with production evidence, then use a controlled trace

Choukse and colleagues from Microsoft, OpenAI and NVIDIA publish production DGX-H100 training power telemetry in Figure 1 of their 2025 paper. They connect synchronized compute and communication phases to power variation visible at larger electrical boundaries. The source figure is normalized, not a GB300 kW rating. Their later storage figures are simulations and their GB200 power-smoothing figure is a microbenchmark; neither is relabeled as production storage evidence.

Now take a simplified 60-second cycle: 30 seconds compute at 120 kW, 15 exchange at 40 kW and 15 save at 60 kW. Its energy is 5,100 kJ and mean power 85 kW. Four coincident copies give 480, 160 and 240 kW at the shared meter, with 340 kW mean. The values show how phases add at a shared meter; a real training job has its own phase lengths.

## Use staggering only when its dependency assumptions hold

If four independent periodic jobs can shift by 0, 15, 30 and 45 seconds without extra waiting, contention or missed deadlines, two compute while one exchanges and one saves: 340 kW throughout the ideal cycle. Their energy remains 5.667 kWh. This is a conditional scheduling thought experiment, not an assertion that production artificial intelligence (AI) clusters routinely use these offsets.

Workers inside one synchronous job are a different case. Delaying a participant may force the others to wait at a collective, violating the unchanged-duration assumption. The lesson is to identify which scheduling freedom actually exists before proposing it as a power remedy.

## Read the trace to choose a response

Read peak power, change magnitude, transition duration, repetition and energy at the intended meter. In a separate assumed transition, 480 to 160 kW over two seconds is a 160 kW/s decrease; over 0.2 seconds it is 1,600 kW/s. The same two plateaus can require a very different response. These ramp examples do not silently change the energy of the ideal stepwise cycle.

Schedulers change eligible workload timing. Supported GPU power controls change device behavior, potentially affecting runtime or energy. Storage changes source-facing power within its conversion, charge, discharge and usable-energy limits. Choose among them using workload dependencies and electrical timescales. A request load balancer does not provide stored energy, and a buffer cannot sustain an average power deficit indefinitely.

## End with the engineering handoff

End with a workload brief. Carry model and hardware identity, software/precision, prompt/output lengths, active sessions, token delivery, first-token targets and quality. Add a measured power trace, complete-run energy and recovery cases at a declared boundary. This supports the next siting/supply decision; unknown rack throughput and electrical behavior remain unknown.

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

## Sources

- [NVIDIA Triton — Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html) — docs.nvidia.com · Reviewed 2026-09-06. Dynamic batching can combine requests and introduce a configurable waiting interval.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — www.vertiv.com · Reviewed 2026-09-06. Argues that synchronized AI load changes call for coordination across power-system levels.
- [vLLM — Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) — vLLM · Published 2025-09-05 · Reviewed 2026-09-14. Describes prefill and decode, key/value-cache allocation, continuous scheduling of new and running requests, serving load balancing, and latency and throughput measurement.
- [Microsoft, OpenAI and NVIDIA — Power Stabilization for AI Training Datacenters](https://arxiv.org/html/2508.14318v1) — Microsoft, OpenAI and NVIDIA authors / arXiv · Published 2025-08-20 · Reviewed 2026-09-12. Reports production training power swings that follow synchronized compute and communication phases, and compares software smoothing, GPU power controls and rack-level energy storage.
- [NVIDIA — Inside NVIDIA Groq 3 LPX](https://developer.nvidia.com/blog/inside-nvidia-groq-3-lpx-the-low-latency-inference-accelerator-for-the-nvidia-vera-rubin-platform/) — NVIDIA · Published 2026-03-16 · Reviewed 2026-09-26. LPX is a separate rack-scale system with 256 Groq LPU accelerators, deployed alongside Vera Rubin NVL72; each LPU has 500 MB of on-chip SRAM as its primary working storage, with 150 TB/s of on-chip memory bandwidth.
- [NVIDIA — How Groq 3 LPX Unlocks Ultrafast Interactivity at Long Context](https://developer.nvidia.com/blog/how-nvidia-groq-3-lpx-unlocks-ultrafast-interactivity-at-long-context-on-nvidia-vera-rubin/) — NVIDIA · Published 2026-08-24 · Reviewed 2026-09-26. Standard prefill–decode disaggregation: Vera Rubin NVL72 runs prefill and hands off the KV cache once per turn; Groq 3 LPX runs the entire decode step using that cache and SRAM-resident weights, with 128 GB of SRAM across its 256 LPUs.
- [NVIDIA — What Is Disaggregated Serving?](https://www.nvidia.com/en-gb/glossary/disaggregated-serving/) — NVIDIA · Reviewed 2026-09-13. Explains compute-heavy prompt processing and memory-bandwidth-heavy token generation, dedicated hardware for each phase, and the required KV-cache transfer.
- [Groq — What is a Language Processing Unit?](https://groq.com/blog/the-groq-lpu-explained) — Groq · Published 2025-03-07 · Reviewed 2026-09-26. Groq expands LPU as Language Processing Unit, its inference processor, built around deterministic execution and memory on the same chip as compute.

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

Continue in **4. Siting, grid connection and supply**: Deliver the campus one usable phase at a time.
