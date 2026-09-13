# Interactivity and total throughput

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d02-workload-brief`, then run `uv run gigawatt-expand`.

**3. Workloads and requirements · Authored draft**

Use a GB300 NVL72 and Llama 3.1 70B to connect model state, context and service requirements to infrastructure demand.

**Driving question:** What must the infrastructure deliver for this workload to count as successful?

## Interactivity is output tokens per second per user

Interactivity is the output token rate experienced by one user after generation starts. At 40 tokens per second per user, the average gap between tokens is 25 milliseconds; at 80 it is 12.5 milliseconds. Time to first token measures the separate initial wait. A token may be a whole word or part of a word. Total throughput counts output tokens across the system, so it answers a different question from the rate of an individual answer.

Serving more requests together can increase aggregate throughput while reducing interactivity. Choose the minimum acceptable per-user output rate, then benchmark how much throughput the system delivers while meeting that requirement.

NVIDIA’s August 2026 Qwen3.8-2.4T-A95B curve on GB300 NVL72 shows throughput per GPU against interactivity. The original image identifies 8k input / 1k output, TensorRT-LLM, FP8 and multi-token prediction. Select a minimum of 100, 200 or 300 tokens per second per user and inspect only the part of the curve to its right. Raising this threshold reduces available throughput on that curve. It is a separate benchmark case from the Llama 3.1 70B memory ledger.

The plot does not tabulate concurrent users. Do not invent an exact session count or combine peak throughput with peak interactivity from different points. A supported-session answer requires the matching concurrency sweep, with its model, lengths, quality, precision and software fixed.

## Compare training and inference memory together

Using the rounded class size of 70 billion parameters, BF16 inference weights require approximately 70 billion × 2 bytes = 140 decimal GB. A classic mixed-precision Adam training ledger stores 2-byte weights, 2-byte gradients, 4-byte master weights and two 4-byte optimizer moments: 16 bytes per parameter, or approximately 1,120 GB of state. The comparison explains why serving a model and training its parameters can require different distributions of state.

These are partial accounts. Inference also needs request KV cache and runtime workspace. Training adds activations, communication buffers and other workspace. Precision, optimizer, recomputation, offload and sharding alter the numbers. The older isolated 80 GB device example did not identify real hardware or establish this connection clearly; the presentation now compares named model uses directly rather than implying an H100 installation.

## Derive how context changes resident concurrency

Meta’s Llama 3.1 70B definition specifies 80 layers, hidden width 8,192, 64 query heads and eight KV heads. Head dimension is 8,192/64 = 128. With BF16 keys and values, each cached token occupies 2 × 80 × 8 × 128 × 2 = 327,680 bytes, or 320 KiB. This is model-specific full-context cache accounting; it excludes prefix sharing, block rounding, quantization and other implementation effects.

Choose a 64 GiB allocation for KV cache, distinct from weights and workspace. At 8,192 cached tokens per request, each uses 2.5 GiB and the pool admits at most 25 requests. At 32,768 tokens, each uses 10 GiB and the pool admits six. The fourfold context increase changes resident concurrency on unchanged hardware. Maintaining 100 such sessions therefore needs at least four versus seventeen equivalent independent pools under this limited model. Those are not GPU counts: parallelism and replication determine which devices own each pool.

This is the facility connection: longer context can change replica requirements, memory traffic, communication and measured power for the same token service. Capacity alone does not predict token speed. A fitting allocation still needs an execution benchmark on the chosen hardware and software.

## Carry a workload brief into design

Do not derive actual tokens per second by dividing a GPU peak-FLOPS number by one approximate operation count. Precision, sustained utilization, attention work, memory bandwidth, interconnects, batching and software all matter. State a service requirement first, then benchmark the intended workload and measure power at its actual electrical boundary.

Record complete-run energy, peak demand, transition duration and recovery behavior together with token delivery and response times. Those become inputs to siting, source capacity, cooling, protection and buffering decisions. A rack inventory and an average kW figure leave important parts of that brief unmeasured.

## Worked example: How context changes a fixed KV-cache pool

- Llama 3.1 70B geometry; BF16 KV entries.
- 64 GiB is a chosen cache allocation, excluding weights and workspace.
- Equal full contexts; no prefix sharing, block rounding or cache quantization.

1. Per-token state — 2 × 80 × 8 × 128 × 2 = 327,680 bytes = 320 KiB — K and V × layers × KV heads × head dimension × bytes per element.
2. 8,192-token context — 8,192 × 320 KiB = 2.5 GiB; floor(64 / 2.5) = 25 requests — Each complete active request occupies its context state.
3. 32,768-token context — 32,768 × 320 KiB = 10 GiB; floor(64 / 10) = 6 requests — Longer contexts reduce resident concurrency without changing the cache allocation.

**Result:** The same pool holds 25 or six complete contexts; this changes the service capacity problem.

**Model boundary:** Memory capacity is not throughput. Pool count is not GPU count; actual runtime allocations need measurement.

## The tradeoff

Choice: Reserve capacity for a broader workload envelope.

Benefit: Future inputs, concurrency, or implementations may fit without replacing the system.

Cost: Additional capacity costs money and can remain unused; aggregate capacity still needs a workable partition.

## When the situation changes

Trigger: Accept a short compute benchmark as proof of production service.

Mechanism: The test excludes queueing, data movement, recovery, or the required workload distribution.

Response: Match acceptance conditions to the actual service and measure the missing phases.

## Apply the idea

A customer keeps the same active-session count but increases context from 8,192 to 32,768 tokens. What must be revisited before promising unchanged token speed and power?

<details>
<summary>Reveal the worked answer</summary>

Revisit cache allocation and request admission, then benchmark the intended parallelism/replicas and token latency at the new lengths.

The fixed pool admits fewer full contexts. Adding capacity or distributing the model changes power and communication; neither arithmetic memory fit nor a peak-FLOPS rating supplies the missing performance measurement.

</details>

**The idea to keep:** Start with accepted work and its constraints; hardware quantities follow from a measured workload model.

## Sources and reading boundaries

- [NVIDIA — DGX SuperPOD Key Components](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-components.html) — A documented AI cluster architecture includes compute, management, networking, and storage components. Read 2026-09-06. Read the public component and design-requirement page for the H100 reference architecture; no product count or performance is copied into the hypothetical brief.
- [MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) — Benchmark results depend on a declared workload scenario and measurement conditions. Read 2026-09-06. Read the public scenario and power-measurement descriptions; no named system performance is asserted.
- [Meta — Llama model SKU architecture definitions](https://github.com/meta-llama/llama-models/blob/main/models/sku_list.py) — Named Llama 3.1 70B architecture for original parameter-storage and KV-cache calculations: hidden width 8,192, 80 layers, 64 query heads and 8 key/value heads. Read 2026-09-12. The llama3_1_base_models definition was inspected in the public GitHub source and its raw file. Head dimension 128 is derived from 8,192/64. The 70B parameter count is rounded model-class notation, not an exact counted checkpoint size. The gated Hugging Face config returned 401 and was not read. This source establishes architecture, not GB300 throughput or deployment performance.
- [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/html/1910.02054) — Derive a declared mixed-precision Adam example: two bytes each for weights and gradients, four for a master weight, eight for the two optimizer moments, giving 16 bytes per parameter before activations and buffers. Read 2026-09-12. Read sections 2.1, 3.1–3.2 and model-state partitioning formulas. This is a classic FP16/FP32 Adam accounting example, not a universal 2026 training-memory requirement. BF16 arrangements, gradient accumulation precision, optimizer choices, quantization, offload and sharding alter the budget. Using rounded 70 billion parameters gives about 1.12 TB across model states, not an asserted minimum GPU count or throughput.
- [NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) — The GB300 NVL72 rack contains 72 Blackwell Ultra GPUs. Read 2026-09-12. Hardware identity and count only; actual inference throughput depends on the serving workload and configuration.
- [NVIDIA AIPerf — Metrics Reference](https://docs.nvidia.com/aiperf/reference/ai-perf-metrics-reference) — Per-user generation throughput and the reciprocal inter-token interval; distinguish total throughput and TTFT. Read 2026-09-13. Reviewed output-token-throughput-per-user and streaming metric definitions. Does not establish a capacity for a named GPU.
- [NVIDIA — Qwen3.8 throughput and interactivity on GB300 NVL72](https://developer.nvidia.com/blog/serve-qwen3-8-2-4t-a95b-a-2-4t-parameter-model-with-configurable-reasoning-on-nvidia-gb300-nvl72/) — Original Figure 2 shows the throughput/interactivity tradeoff with the hardware, model and workload conditions printed in the figure. Read 2026-09-13. Publisher benchmark curve, not our measurement. 8k/1k, TensorRT-LLM, FP8 and MTP read from the original figure. No tabulated concurrency or exact curve samples provided; do not infer supported sessions.
