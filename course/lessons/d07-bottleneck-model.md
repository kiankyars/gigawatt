# Find the limit before buying more arithmetic

**D07 · Authored draft · Objectives:** D07.2, D07.3

Apply a small performance model, then test its assumptions against capacity and the job’s critical path.

**Driving question:** Is a workload constrained by memory capacity, memory bandwidth, compute or communication?

## Use four different tests

Begin with feasibility: does the required live state fit in the memory accessible under the chosen execution plan? This is a capacity test, not a speed test. If it fails, the plan must change by partitioning state, recomputing intermediates, offloading data or changing the workload. Each option changes traffic and possibly numerical behavior. Once the plan fits, count the operations it performs and bytes it moves across a specified memory interface. Then count communication on the critical path between participating devices.

FLOPS is an execution rate for specified operations and numerical formats. Bytes per second is a movement rate across a specified interface. Neither is a generic unit of job progress. A comparison must hold the algorithm, precision, correctness target, batch policy and output definition constant enough to be meaningful. Installed megawatts only constrain an electrical envelope. They do not reveal how much of that envelope feeds arithmetic that advances the requested result, or how much time the equipment spends waiting.

## Derive a useful lower bound

Let W be the required floating-point operations, F the available execution rate, M the bytes transferred from the chosen memory boundary and B its bandwidth. Execution takes at least W/F; memory transfer takes at least M/B. If those activities can overlap ideally, elapsed time is at least their maximum. If they must occur serially, the sum is a more appropriate model. Arithmetic intensity W/M expresses how much calculation occurs per byte moved. Comparing it with F/B suggests which resource limits the idealized case.

The model is valuable because its assumptions are visible. It does not include all kernel launch delays, instruction dependencies, irregular access, insufficient parallelism or inter-device synchronization. It also requires the correct traffic count. Counting each mathematical input once can underestimate bytes if the implementation rereads it repeatedly; counting all logical accesses as device-memory transfers can overestimate bytes if cache reuse is effective. Use the model to formulate a measurement question, then use profiling to check the actual boundary and traffic.

## Equal power can hide very different useful capacity

Imagine two synthetic rack configurations with equal electrical input limits. Rack A provides twice as much nominal arithmetic as B, but B provides twice the effective memory bandwidth for the chosen workload. A bandwidth-heavy job can favor B even though A has the more impressive FLOPS total. A compute-heavy job can favor A. Neither result ranks the racks universally. It establishes a workload-dependent comparison that can be revisited when model size, batch size or parallelization changes.

Communication introduces another limit. If a step needs 50 milliseconds of unavoidable synchronization after 100 milliseconds of computation, doubling compute speed gives a 100-millisecond step, not a 75-millisecond step. The unchanged portion becomes a larger share of elapsed time. Overlap can reduce that penalty only where dependencies permit it. This is why faster devices can increase the value of a better network or storage path: they shorten one phase until an older waiting phase becomes exposed. A balanced system is balanced for a particular workload, not for every imaginable application.

## Measure the output that matters

For training, count progress under a fixed convergence or validation objective rather than treating every arithmetic operation as equally useful. For inference, specify request mix, output length, quality and latency constraints before comparing completed tokens. A change that increases batch throughput while violating response deadlines may reduce accepted service. Keep energy per accepted output separate from peak power. An experiment should report both the electrical boundary and the conditions under which the output was counted.

## Worked example: A fictional kernel and two resource upgrades

- A kernel performs 120 trillion operations and moves 3 trillion bytes across the specified device-memory boundary.
- The synthetic device provides 300 trillion operations per second and 2 trillion bytes per second.
- The 100 GB live working set fits in 128 GB of usable memory; computation and memory traffic overlap ideally.

1. Check arithmetic time — 120 / 300 = 0.4 s — Operation units cancel consistently.
2. Check memory time — 3 / 2 = 1.5 s — Memory traffic sets the larger idealized time.
3. Compare resource ratios — 120 / 3 = 40 operations/byte; 300 / 2 = 150 operations/byte — The workload provides too little arithmetic per transferred byte to reach this device’s compute ceiling.
4. Test upgrades — Double compute: max(0.2, 1.5) = 1.5 s; double bandwidth: max(0.4, 0.75) = 0.75 s — Only the bandwidth upgrade changes the active bound in this model.

**Result:** The predicted limit is memory bandwidth, after capacity feasibility has been established.

**Model boundary:** All numbers are synthetic. This optimistic bound excludes software, caching details, communication and contention.

## The tradeoff

Choice: Increase batch size to reuse data across more arithmetic.

Benefit: Potentially increase arithmetic intensity and reduce movement per output.

Cost: Increase live memory demand and possibly queueing delay; training or serving semantics must remain acceptable.

## When the situation changes

Trigger: An optimization reduces arithmetic time but increases temporary state beyond 128 GB.

Mechanism: The previously feasible memory plan fails or begins offloading over a slower interface.

Response: Recompute the live-state and traffic ledger together; do not celebrate a faster isolated kernel until the full job remains feasible.

## Apply the idea

A second implementation performs the same 120 trillion operations but moves only 0.6 trillion bytes, with the original device. What is its bound, and which resource is now active?

<details>
<summary>Reveal the worked answer</summary>

Memory time becomes 0.3 s, so the idealized bound is max(0.4, 0.3) = 0.4 s, with computation active.

Reducing traffic can be more valuable than buying additional arithmetic. The improvement depends on actually eliminating transfers at the measured boundary, while retaining correct output and sufficient parallelism.

</details>

**The idea to keep:** The useful comparison is work divided by the time needed to obtain its inputs, execute it and exchange its results.

## Sources and reading boundaries

- [GPU Performance Background User’s Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html) — Arithmetic intensity offers a first-order compute-versus-memory model whose assumptions require profiling. Read 2026-09-06. The lesson derives its own examples; historical NVIDIA device values are not used.
- [Matrix Multiplication Background User’s Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) — Matrix shape and reuse can alter arithmetic intensity and the active performance limit. Read 2026-09-06. A guide to particular operations, not a universal model of end-to-end AI job performance.
