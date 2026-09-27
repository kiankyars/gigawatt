# Inside a GB300 compute tray

**Compute and memory — further reading**

Locate the central processing unit (CPU), graphics processing unit (GPU), high-bandwidth memory (HBM) and rack interconnect in a GB300 NVL72, then distinguish memory capacity from the paths that supply computation.

**Driving question:** Which hardware and data transfers let a powered rack produce tokens?

## Begin with a rack, then open one compute tray

The electrical journey has reached the rack. This lesson follows the hardware that uses that power: processors perform operations, memories hold the operands and execution state, and links carry data between them. The recurring example is NVIDIA’s GB300 NVL72. Its 18 compute trays contain four Blackwell Ultra GPUs and two Grace CPUs each: 72 GPUs and 36 CPUs in one rack. Nine NVLink switch trays connect the GPUs over NVLink, NVIDIA’s direct GPU-to-GPU interconnect. A compute tray runs its own operating-system image; the shared rack fabric connects multiple such systems.

Keep the physical hierarchy visible as the view changes. One Grace Blackwell Ultra superchip combines one Grace CPU with two GPUs; two of those groups occupy a compute tray. A Blackwell Ultra GPU itself contains two compute dies that appear to CUDA, NVIDIA’s GPU programming platform, as one accelerator. Thus a die, a GPU, a superchip, a compute tray and a rack describe different assemblies. Counting the two dies as two schedulable GPUs would double the inventory incorrectly.

## The CPU prepares and coordinates work; the GPU executes parallel kernels

A CPU can run the serving process, prepare inputs, launch GPU kernels and coordinate the application. For a large language model (LLM) request, tokenization turns text into token IDs; software arranges the tensors and chooses the execution plan. Many large arithmetic operations then run on GPU Tensor Cores, which accelerate matrix multiply-accumulate. Other GPU execution units handle work that does not map to those matrix operations. A network interface card (NIC) connects the tray to an external network, and local solid-state storage on the NVMe (Non-Volatile Memory Express) interface can cache data or hold the operating system.

This is a division of responsibilities, not a requirement that every byte be copied through the CPU. The actual software and input/output (I/O) path determine which preparations run on the host and which transfers can bypass intermediate copies. To diagnose a slow rack, identify the operation waiting and the resource supplying it: host preparation, device memory, a peer GPU, or a remote service.

## HBM is attached to the GPU package, close to its compute dies

HBM means high-bandwidth memory. In this GPU family, stacked DRAM (dynamic random-access memory) sits beside the compute dies within the package, with many short parallel connections. The package arrangement provides the wide interface needed to feed the arithmetic units. HBM still stores data outside the compute dies; cache and other on-chip storage can keep reused operands closer. Moving an operand from HBM and reusing it locally are different amounts of traffic at the HBM boundary.

NVIDIA specifies up to 288 GB HBM3e and up to 8 TB/s of HBM bandwidth per Blackwell Ultra GPU. Capacity is a quantity of data; bandwidth is a transfer rate. These are platform specifications. The transfer account below uses 8 TB/s as a ceiling, not an observed sustained rate. A product implementation can differ: Lenovo’s GB300 NVL72 product guide, updated August 30, 2026, lists 7.7 TB/s for its configuration.

## Follow three distinct paths to the arithmetic

For data resident in local HBM, the path is HBM → GPU memory system → execution units. For data resident in CPU memory, the path includes the coherent NVLink-C2C (chip-to-chip) connection between CPU and GPU. For data on a peer GPU, the path includes that peer’s memory and the rack’s NVLink switching fabric. Coherency permits direct addressing across the CPU/GPU boundary; it does not make all physical memory equally fast.

The NVLink 5 figure of 1.8 TB/s per GPU adds the two transfer directions across all of that GPU’s links. It is neither a separate 1.8 TB/s pipe to every peer nor directly comparable with a one-direction transfer measurement. The 72-GPU rack has an advertised aggregate memory bandwidth of up to 576 TB/s because many local HBM interfaces operate in parallel. A single tensor operation does not automatically receive that aggregate rate. Its partitioning and placement determine which interfaces participate.

## Use a transfer account to connect bytes with time

Suppose an operation must read 144 GB across one GPU’s HBM interface. At an 8 TB/s transfer ceiling, the read alone requires at least 144 × 10⁹ / (8 × 10¹²) = 0.018 seconds, or 18 ms. GB and TB here use decimal powers of ten, as in the International System of Units (SI). Increasing memory capacity while leaving the traffic and bandwidth unchanged does not lower that bound. Reducing the traffic through reuse, or increasing bandwidth, can.

The 144 GB account is chosen to isolate one mechanism; it is not a model checkpoint or one token’s measured traffic. A generated token requires an execution graph, including arithmetic, cache activity and often communication. Converting the 18 ms into a token rate would require establishing how often this transfer occurs and which other dependencies remain. Capacity comes first when a placement cannot fit; transfer time becomes the next question once that placement is feasible.

## Worked example: What can an 8 TB/s HBM interface tell us?

- One operation reads 144 GB from local HBM; all numbers use SI bytes.
- The transfer-rate ceiling is 8 TB/s; the read is not already served by cache.
- We isolate HBM traffic before adding arithmetic and communication.

1. Count bytes at the chosen interface — 144 GB = 144 × 10⁹ bytes — Count actual HBM reads, not every logical reuse of the data.
2. Divide traffic by bandwidth — 144 × 10⁹ / (8 × 10¹²) = 0.018 s = 18 ms — This is the minimum read duration under the stated ceiling.
3. Test a capacity-only upgrade — 144 GB / 8 TB/s = 18 ms — Additional capacity can enable a larger resident working set but does not change this fixed read.
4. Test eliminating half the HBM traffic — 72 GB / 8 TB/s = 9 ms — The improvement requires actual reuse or removal of transfers at this boundary.

**Result:** The useful performance question is how many bytes cross which interface, not merely how many bytes the rack can store.

**Model boundary:** NVIDIA gives the up-to-8-TB/s platform figure. The 144 GB traffic account is assumed for the example; these are transfer bounds, not token rates.

## When the situation changes

Trigger: A deployment fits its state by moving frequently read tensors from HBM to CPU memory.

Mechanism: The address remains accessible, but repeated accesses now traverse the CPU/GPU path.

Response: Identify the tensors and measured traffic crossing that path, then compare placement, reuse and partitioning options.

## Apply the idea

A workload fits in HBM but spends most of its time repeatedly reading the same weights from it. Which evidence would make local reuse a better candidate than buying a larger memory capacity?

<details>
<summary>Reveal the worked answer</summary>

Show that the working set already fits and that the implementation rereads weights across the HBM interface when it could reuse them in faster local storage.

A larger capacity removes no transfer by itself. A changed kernel or execution grouping must reduce measured HBM traffic without changing the required output or exceeding available local storage.

</details>

**The idea to keep:** Where a tensor resides determines which memory or interconnect must supply it to the GPU.

## Sources

- [NVIDIA DGX GB Rack Scale Systems — Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html#power-shelves) — NVIDIA · Reviewed 2026-09-17. DGX GB300 rack, compute-tray, rear-interface and switch-tray organization.
- [NVIDIA GB300 NVL72 — Specifications](https://www.nvidia.com/en-us/data-center/gb300-nvl72/) — NVIDIA · Reviewed 2026-09-14. The named platform contains 72 GPUs and 36 CPUs; advertised rack GPU memory bandwidth is up to 576 TB/s in aggregate.
- [NVIDIA — Inside Blackwell Ultra](https://developer.nvidia.com/blog/inside-nvidia-blackwell-ultra-the-chip-powering-the-ai-factory-era/) — NVIDIA · Published 2025-08-22 · Reviewed 2026-09-14. Two dies form one CUDA accelerator; up to 288 GB HBM3e and 8 TB/s per GPU; NVLink 5 bandwidth is 1.8 TB/s bidirectional per GPU.
- [NVIDIA — Memory management on hardware-coherent platforms](https://developer.nvidia.com/blog/understanding-memory-management-on-hardware-coherent-platforms/) — NVIDIA · Published 2025-10-14 · Reviewed 2026-09-14. GB300 CPU and GPU memory can be directly addressed across NVLink-C2C while retaining different physical locations and management behavior.
- [Lenovo NVIDIA GB300 NVL72 Rack Scale AI Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) — Lenovo Press · Published 2026-08-30 · Reviewed 2026-09-17. Lenovo’s GB300 NVL72 configuration lists 7.7 TB/s of GPU memory bandwidth.
