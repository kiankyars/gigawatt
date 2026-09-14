# Choose the upgrade that removes the active limit

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d07-bottleneck-model`, then run `uv run gigawatt-expand`.

**9. Compute, memory and the rack · Authored draft**

Derive arithmetic intensity and a roofline bound, then diagnose which resource upgrade changes the operation’s completion time.

**Driving question:** Would this operation benefit from more arithmetic, more memory bandwidth, or less data movement?

## A matrix multiplication explains why reuse matters

For C = A × B, with A shaped M × K and B shaped K × N, there are M × N output elements. Each output combines K products. With the conventional multiply-add accounting, the operation count is approximately 2MKN FLOP: one multiplication plus one addition is two floating-point operations. FLOP counts work; FLOP/s measures its execution rate. This convention lets us connect a named operation to a rate rather than treating an advertised FLOPS number as tokens per second.

One weight tile can contribute to several output elements after being fetched into local storage. If the implementation rereads that tile from HBM for every output, traffic rises. If it reuses the tile locally, more arithmetic occurs per byte crossing HBM. Input shape, tile size, available storage and parallelism determine what reuse is possible. Reuse is the mechanism; a larger batch is only one way an application might expose it.

## Define the two time accounts

Let W be the operation count in FLOP, F the available arithmetic rate in FLOP/s, M the transferred bytes at the selected HBM boundary, and B its bandwidth in bytes/s. The arithmetic time is bounded below by W/F; the memory time by M/B. With ideal overlap, completion cannot be faster than max(W/F, M/B). A fully serial model uses their sum. A real dependency schedule can fall between these accounts or take longer because of additional work.

The model below assigns 200 TFLOP/s to dense BF16 matrix arithmetic with FP32 accumulation and 8 TB/s to HBM traffic. The compute rate is a teaching assumption for this instruction mix, not the peak rating of a GB300. Both rates are held constant to isolate the comparison. If effective rates are measured instead, the workload shape, numerical format, clocks and measurement boundary must remain part of that record.

## Derive the roofline from the time bound

Arithmetic intensity I = W/M is the number of FLOP performed per byte moved across HBM. Dividing work by the idealized elapsed time gives a throughput ceiling of min(F, B × I). On a graph of FLOP/s against FLOP/byte, the bandwidth-limited line rises with I until it meets the horizontal compute ceiling. Their intersection is I = F/B. This graph is called the roofline model.

With 200 × 10¹² FLOP/s and 8 × 10¹² bytes/s, the intersection is 25 FLOP/byte. At 10 FLOP/byte, the bandwidth ceiling is 8 × 10¹² × 10 = 80 TFLOP/s. Above the intersection, adding memory bandwidth does not raise this model’s 200 TFLOP/s compute ceiling. Moving right through better reuse can help a bandwidth-limited operation; raising the wrong ceiling cannot.

## Read numerical formats before comparing compute ratings

A peak rate must name both the operation and numerical format. Dense BF16, FP8 and FP4 matrix arithmetic are different claims; sparse throughput assumes a supported sparsity pattern and an implementation that can exploit it. Multiplying the advertised sparse peak by runtime does not establish that many useful dense operations. Likewise, shrinking tensor precision changes more than capacity: it can change traffic, available instructions and the numerical behavior of the model.

For a purchase comparison, keep the required output quality and workload configuration explicit, then measure the achieved operation or service rate. The roofline is useful for predicting which resource to examine, but insufficient parallelism, irregular access, launch overhead and dependencies can leave execution well below either ceiling. A high arithmetic intensity alone does not guarantee that the GPU is busy.

## Communication can become the exposed dependency

The local HBM model stops at the GPU boundary. If results must be exchanged with peers before the next layer can begin, that exchange enters the critical path. For example, 100 ms of computation followed by 50 ms of unavoidable exchange takes 150 ms. Halving computation reduces the total to 100 ms. The exchange now occupies half the step, so another arithmetic upgrade has a smaller effect unless the communication or dependency schedule also changes.

Return to the course’s outcome: a rack earns useful throughput by completing the required execution graph. Neither installed megawatts nor a sum of chip peaks supplies the missing operation counts, traffic or synchronization schedule. Those measurements establish whether another GPU, more HBM bandwidth, a different kernel, or a better network path is the relevant next change.

## Worked example: A memory-bound operation and two upgrades

- The operation performs 2 × 10¹² FLOP of dense BF16 matrix arithmetic with FP32 accumulation and transfers 160 GB across HBM.
- Its live state fits. Assigned rates are 200 TFLOP/s and 8 TB/s; compute and HBM traffic overlap ideally.
- Upgrades change only one assigned rate; operation count and traffic remain fixed.

1. Account for computation — 2 × 10¹² / (200 × 10¹²) = 0.010 s = 10 ms — The arithmetic account is shorter than the HBM account.
2. Account for HBM traffic — 160 × 10⁹ / (8 × 10¹²) = 0.020 s = 20 ms — With ideal overlap, 20 ms is the active bound.
3. Double the compute rate — max(5 ms, 20 ms) = 20 ms — Faster arithmetic does not shorten the unchanged memory transfer.
4. Double the HBM bandwidth — max(10 ms, 10 ms) = 10 ms — The changed resource removes the active limit until the two accounts meet.

**Result:** For this operation, the bandwidth upgrade changes the bound; the compute upgrade does not. Reducing actual HBM traffic could address the same limit.

**Model boundary:** The assigned compute rate and workload account are original examples. Full overlap gives an optimistic bound; network time, software overhead and contention are outside this account.

## The tradeoff

Choice: Reuse a matrix tile for more arithmetic before replacing it.

Benefit: Increase FLOP per byte transferred from HBM, potentially moving the operation out of the bandwidth-limited regime.

Cost: Consume local storage and possibly alter occupancy or scheduling; validate the whole kernel rather than only its traffic count.

## When the situation changes

Trigger: An optimized kernel reduces HBM traffic but exposes too little concurrent work.

Mechanism: The arithmetic-intensity calculation improves while execution units remain underused.

Response: Compare actual memory traffic, achieved arithmetic rate and dependency timing before attributing the slowdown to hardware capacity.

## Apply the idea

A second operation moves the same 160 GB but performs 40 × 10¹² FLOP at the original rates. Which of the two upgrades should you test first, and what would make the prediction fail?

<details>
<summary>Reveal the worked answer</summary>

The arithmetic account is 200 ms and HBM is 20 ms. Doubling compute reduces the bound to 100 ms; doubling HBM leaves it at 200 ms. Test compute first.

The recommendation changes with the operation, even on unchanged hardware. It could fail if the assumed arithmetic rate cannot be sustained, another dependency dominates, or the upgrade changes the execution plan and traffic. Measure those quantities rather than treating the bound as a benchmark.

</details>

**The idea to keep:** An upgrade helps when it changes a limit on the operation’s critical path.

## Sources and reading boundaries

- [GPU Performance Background User’s Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html) — Compute and memory time bounds, arithmetic intensity and the role of sufficient parallelism; multiply-add counts as two floating-point operations. Read 2026-09-14. GPU structure and performance sections reread. Guide dated February 2023; historical GPU specifications are not used. The 200 TFLOP/s and workload accounts below are original teaching inputs.
- [Matrix Multiplication Background User’s Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) — Matrix dimensions, tiling and operand reuse explain changes in arithmetic intensity. Read 2026-09-14. Public guide reviewed for matrix-operation structure and reuse. Numerical examples below are independently derived; no older hardware throughput is transferred to GB300.
- [NVIDIA — Inside Blackwell Ultra](https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/) — Two dies form one CUDA accelerator; up to 288 GB HBM3e and 8 TB/s per GPU; NVLink 5 bandwidth is 1.8 TB/s bidirectional per GPU. Read 2026-09-14. Authored body and figures inspected, including the actual superchip board. Architecture maxima vary by SKU. The body and endnote conflict on HBM stack wording, so stack count is not taught. No per-GPU C2C bandwidth or performance ratio is inferred for a rack configuration.
