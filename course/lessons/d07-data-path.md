# A rack is a path through several memories

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d07-data-path`, then run `uv run gigawatt-expand`.

**D07 · Authored draft · Objectives:** D07.1, D07.2

Follow bytes through storage, host processing, accelerator memory, execution and communication, and distinguish movement from ownership.

**Driving question:** What must happen between a stored dataset and a completed accelerator operation?

## Trace one batch before drawing a whole cluster

Start with a dataset record in durable storage. A process identifies the record, obtains permission to read it, retrieves its bytes and interprets its format. The host CPU may decode, tokenize, transform or assemble those bytes into a batch. Host memory holds intermediate state. A transfer places the required tensors in accelerator-accessible memory, kernels operate on them, and results feed another kernel, a communication operation or a stored output. This deliberately simple path is a reasoning tool. Some implementations bypass intermediate copies, but their control and correctness responsibilities still exist.

The CPU is not merely a smaller accelerator. It may run the operating system, launch work, prepare data, coordinate communications and execute parts of the application that do not map efficiently to parallel kernels. The accelerator combines execution units with a hierarchy of memories and caches. A NIC connects the node to an external fabric; an accelerator interconnect connects participating devices within a specified system. A storage device holds data across power cycles according to its guarantees. Each component solves a different part of the journey.

## Capacity, locality and copies are different questions

Memory capacity asks whether the required live state fits. Bandwidth asks how quickly bytes cross an interface. Latency asks how long an individual request waits for completion. A workload may fit comfortably while spending most of its time moving data. It may also have ample nominal bandwidth but issue too little concurrent work to use it. Write the working set as weights, temporary state, input/output buffers and any cached history needed by the algorithm. Do not compare model-file size alone with memory capacity and conclude that execution will fit.

Locality changes which link is used. A value already in a nearby cache may avoid a trip to device memory; a local dataset cache may avoid a remote storage transfer. Caching helps only when data is reused and remains valid. A first pass can still be slow, and a new workload can evict useful state. Distinguish a copy from a view or reference: the software may expose a convenient address while the physical bytes remain across a limited interconnect. Apparent memory unification does not erase bandwidth or ownership rules.

## Turn the data path into a pipeline model

If preparation, transfer and execution run strictly one after another, their times add. If separate batches can use those stages concurrently, steady-state batch spacing is bounded by the slowest stage, after the pipeline fills. That improvement requires enough buffers and independent resources. A CPU preparing the next batch may contend with checkpoint staging; a transfer may share a link with communication. Therefore perfect overlap is an optimistic model, not a default property of an architecture.

The distinction between throughput and latency becomes visible here. A pipeline can complete a batch every 40 milliseconds even though each individual batch takes longer from entry to exit. The first result still waits for every required stage. For an interactive request with a tight response deadline, that end-to-end delay may matter more than steady-state batch throughput. For a long offline job, the spacing between completed batches may dominate. The correct infrastructure brief names both the output being counted and the timing condition under which it must arrive.

## Read a real rack without importing its marketing

The NVL72 reference page provides a concrete example of compute trays, switched interconnects, separate networking roles, local storage and management. Use that hierarchy to ask where the bytes travel. The numerical exercise below is entirely fictional. It does not inherit the page’s performance ratios or its ambiguous bandwidth aggregation. A reference architecture is most useful when it reveals interfaces that a simplified sketch accidentally omitted.

## Worked example: Three stages, two execution policies

- Each synthetic batch takes 30 ms of host preparation, 20 ms of transfer and 40 ms of accelerator execution.
- Ten batches are processed; startup overhead outside these stages is zero.
- For the pipelined case, stages have independent resources, sufficient buffers and no interference.

1. Process batches serially — 10 × (30 + 20 + 40) = 900 ms — Each batch waits until the preceding batch completes every stage.
2. Fill the pipeline — 30 + 20 + 40 = 90 ms — The first batch still crosses all three stages.
3. Complete the remaining batches — 9 × max(30, 20, 40) = 360 ms — After filling, the bottleneck stage determines batch spacing.
4. Compare total duration — 90 + 360 = 450 ms — Ideal overlap halves this ten-batch duration.

**Result:** The same components deliver different throughput because the schedule changes. The first-batch latency remains 90 ms in this model.

**Model boundary:** Real overlap depends on implementation, buffer capacity, shared links and contention; this is not a benchmark of a named platform.

## The tradeoff

Choice: Allocate more buffering to overlap host work, transfer and accelerator execution.

Benefit: Reduce idle gaps and approach the slowest-stage throughput bound.

Cost: Consume memory, complicate lifetime management and potentially increase queued work and response latency.

## When the situation changes

Trigger: A new dataset takes 70 ms per batch to decode on the host.

Mechanism: Host preparation becomes the bottleneck; faster accelerator arithmetic cannot fill the resulting input gaps.

Response: Measure stage timing, then investigate preparation parallelism, data representation or caching while preserving equivalent input semantics.

## Apply the idea

With the 70 ms preparation stage, 20 ms transfer and 40 ms execution, what is the ideal duration for ten pipelined batches? Would halving accelerator execution time restore the original 450 ms result?

<details>
<summary>Reveal the worked answer</summary>

Duration is 130 + 9 × 70 = 760 ms. Halving execution to 20 ms gives 110 + 630 = 740 ms, still far from 450 ms.

The dominant repeated interval is now host preparation. Faster execution shortens only the fill/drain contribution because it was already shorter than the bottleneck stage.

</details>

**The idea to keep:** A powerful arithmetic engine contributes only when the data, software and synchronization it needs arrive in time.

## Sources and reading boundaries

- [GPU Performance Background User’s Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html) — A GPU combines execution resources and a memory hierarchy; achieved performance depends on workload behavior. Read 2026-09-06. Use conceptual structure only; dated product examples and throughput tables are not applied.
- [NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) — The component hierarchy distinguishes compute, switching, networking, local storage and management. Read 2026-09-06. Inspected May 18, 2026 page revision; no universal power or bandwidth numbers inferred.
