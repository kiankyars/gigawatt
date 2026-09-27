# Interactivity and total throughput

**3. Workloads and requirements**

Use a GB300 NVL72 and Llama 3.1 70B to connect model state, context and service requirements to infrastructure demand.

**Driving question:** What must the infrastructure deliver for this workload to count as successful?

## Interactivity is output tokens per second per user

Interactivity is the output token rate experienced by one user after a large language model (LLM) starts generating. At 40 tokens per second per user, the average gap between tokens is 25 milliseconds; at 80 it is 12.5 milliseconds. Time to first token measures the separate initial wait. A token may be a whole word or part of a word. Total throughput counts output tokens across the system, so it answers a different question from the rate of an individual answer.

Serving more requests together can increase aggregate throughput while reducing interactivity. Choose the minimum acceptable per-user output rate, then benchmark how much throughput the system delivers while meeting that requirement.

NVIDIA’s August 2026 Figure 2 plots throughput per graphics processing unit (GPU) against interactivity for Qwen3.8-2.4T-A95B on GB300 NVL72, with 8k input and 1k output tokens, TensorRT-LLM, 8-bit floating point (FP8) and multi-token prediction. Set a minimum of 100, 200 or 300 tokens per second per user, and only the part of the curve to its right qualifies. Raising this threshold reduces the throughput available on that curve. It is a separate benchmark case from the Llama 3.1 70B memory ledger.

The plot does not tabulate concurrent users. Do not invent an exact session count or combine peak throughput with peak interactivity from different points. A supported-session answer requires the matching concurrency sweep, with its model, lengths, quality, precision and software fixed.

## Compare training and inference memory together

Training compute is counted in floating-point operations (FLOPs); FLOP/s expresses how fast those operations execute. These quantities describe the computational workload and its execution rate. Model quality still requires evaluation against the intended task. Inference throughput instead counts generated tokens across all users; first-token and inter-token latency describe the response experienced by each user.

Using the rounded class size of 70 billion parameters, inference weights stored in BF16, a 16-bit floating-point format that takes 2 bytes per value, require approximately 70 billion × 2 bytes = 140 decimal gigabytes (GB). A classic mixed-precision Adam training ledger stores 2-byte weights, 2-byte gradients, 4-byte master weights and two 4-byte optimizer moments: 16 bytes per parameter, or approximately 1,120 GB of state. The comparison explains why serving a model and training its parameters can require different distributions of state.

These are partial accounts. Inference also needs each request's key-value (KV) cache, the attention keys and values stored for tokens already processed, and runtime workspace. Training adds activations, communication buffers and other workspace. Precision, optimizer, recomputation, offload and sharding alter the numbers.

## Derive how context changes resident concurrency

Meta’s Llama 3.1 70B definition specifies 80 layers, hidden width 8,192, 64 query heads and eight KV heads. Head dimension is 8,192/64 = 128. With BF16 keys and values, each cached token occupies 2 × 80 × 8 × 128 × 2 = 327,680 bytes, or 320 kibibytes (KiB; 1 KiB is 1,024 bytes). This is model-specific full-context cache accounting; it excludes prefix sharing, block rounding, quantization and other implementation effects.

Choose a 64 gibibyte (GiB) allocation for KV cache, distinct from weights and workspace. At 8,192 cached tokens per request, each uses 2.5 GiB and the pool admits at most 25 requests. At 32,768 tokens, each uses 10 GiB and the pool admits six. The fourfold context increase changes resident concurrency on unchanged hardware. Maintaining 100 such sessions therefore needs at least four versus seventeen equivalent independent pools under this limited model. Those are not GPU counts: parallelism and replication determine which devices own each pool.

This is the facility connection: longer context can change replica requirements, memory traffic, communication and measured power for the same token service. Capacity alone does not predict token speed. A fitting allocation still needs an execution benchmark on the chosen hardware and software.

Prefix caching reuses stored keys and values for initial tokens that requests have in common, such as a shared system prompt. It does not mean that unrelated contexts can share arbitrary KV state. The calculation above counts each request independently; sharing an identical prefix can reduce that allocation.

DeepSeek’s V4 technical report shows another way to change the budget: compressed attention. Its Figure 1, below, compares V4-Pro and V4-Flash with V3.2 as sequence length grows. At about one million tokens of context, accumulated KV cache is 9.5 times smaller for V4-Pro and 13.7 times smaller for V4-Flash than for V3.2. Its architecture and KV storage formats differ from Llama 3.1 70B, so the preceding 320 KiB-per-token factor does not describe those curves.

![DeepSeek chart of accumulated KV cache in gigabytes against sequence length up to 1,024K tokens. The V3.2 line rises toward 50 GB; arrows mark V4-Pro as 9.5 times smaller and V4-Flash as 13.7 times smaller.](../assets/references/deepseek-kv-cache.png)

DeepSeek V4 technical report, Figure 1, KV-cache panel. Compressed attention and mixed KV precision make these curves a different model from the Llama 3.1 70B calculation above. [DeepSeek V4 technical report, Figure 1](https://arxiv.org/html/2606.19348v1)

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

## Sources

- [NVIDIA — DGX SuperPOD Key Components](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-components.html) — docs.nvidia.com · Reviewed 2026-09-16. A documented AI cluster architecture includes compute, management, networking, and storage components.
- [MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) — mlcommons.org · Reviewed 2026-09-06. Benchmark results depend on a declared workload scenario and measurement conditions.
- [Meta — Llama model SKU architecture definitions](https://github.com/meta-llama/llama-models/blob/main/models/sku_list.py) — Meta · Reviewed 2026-09-12. Llama 3.1 70B architecture: hidden width 8,192, 80 layers, 64 query heads and 8 key/value heads.
- [ZeRO: Memory Optimizations Toward Training Trillion Parameter Models](https://arxiv.org/html/1910.02054) — Microsoft Research authors / arXiv · Published 2019-10-04 · Reviewed 2026-09-12. Mixed-precision Adam training keeps two bytes each for weights and gradients, four for a master copy of the weights and eight for the two optimizer moments: 16 bytes per parameter before activations and buffers.
- [NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) — NVIDIA · Reviewed 2026-09-12. The GB300 NVL72 rack contains 72 Blackwell Ultra GPUs.
- [NVIDIA AIPerf — Metrics Reference](https://docs.nvidia.com/aiperf/reference/ai-perf-metrics-reference) — NVIDIA · Reviewed 2026-09-13. Defines per-user output token throughput as the reciprocal of inter-token latency, separately from total throughput and time to first token (TTFT).
- [NVIDIA — Qwen3.8 throughput and interactivity on GB300 NVL72](https://developer.nvidia.com/blog/serve-qwen3-8-2-4t-a95b-a-2-4t-parameter-model-with-configurable-reasoning-on-nvidia-gb300-nvl72/) — NVIDIA · Published 2026-08-12 · Reviewed 2026-09-13. Figure 2 plots throughput per GPU against per-user interactivity for Qwen3.8-2.4T-A95B on GB300 NVL72 at 8k input and 1k output tokens, with TensorRT-LLM, FP8 and multi-token prediction.
- [DeepSeek-V4: Towards Highly Efficient Million-Token Context Intelligence](https://arxiv.org/html/2606.19348v1) — DeepSeek-AI · Published 2026-04-26 · Reviewed 2026-09-14. Figure 1 and section 2.3.4 compare accumulated KV-cache state for V3.2, V4-Pro and V4-Flash.
- [vLLM — Inside vLLM: Anatomy of a High-Throughput LLM Inference System](https://vllm.ai/blog/2025-09-05-anatomy-of-vllm) — vLLM · Published 2025-09-05 · Reviewed 2026-09-14. KV blocks for identical token prefixes can be reused across requests.
