# Choose where electricity becomes light

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d08-copper-light-service`, then run `uv run gigawatt-expand`.

**Networking and interconnects · Authored draft**

Compare media and optical packaging at the link level, then include their effects on switch cooling, cabling and repair.

**Driving question:** How should reach, power and replacement boundaries shape the choice between copper, pluggable optics and CPO?

## Start with the required link, not the fashionable package

A link has two endpoints, a required payload rate, a physical route and an acceptable error behavior. Its media choice must satisfy those conditions under the intended environment. Copper carries an electrical signal along the route; optical fiber carries modulated light after electro-optical conversion. Copper can be attractive for sufficiently short qualified connections, while increasing rate and distance can make electrical loss and signal conditioning harder. There is no universal distance at which every copper design stops and every optical design begins: specify the actual interface and approved cable.

A pluggable optical transceiver places the electrical-to-optical boundary in a replaceable module attached to a host port. The signal still travels electrically between the switching silicon and that module. Co-packaged optics moves optical engines close to the switching silicon, shortening that electrical portion. External laser arrangements, fiber connections and serviceable subassemblies vary by design. CPO names a packaging approach, not a guarantee that every optical component is inseparable or that every repair requires replacing an entire switch.

## Compare complete and equal power boundaries

NVIDIA’s August 2025 photonics description uses shorter electrical paths as a motivation for CPO and describes then-proposed switch platforms. That is a useful mechanism to study. Its advertised savings and reliability ratios are not adopted here as universal field measurements. A comparison must state the included elements: host electrical interfaces, retimers or signal processing where present, optical engines, lasers and any additional cooling. If one number includes both ends of a link and another includes only the switch end, the apparent saving is not meaningful.

Power is also not energy per completed job. A lower-power network that slows an important collective can keep the much larger compute system running longer. Conversely, a somewhat higher-power network can reduce total job energy if it improves accepted throughput enough. Hold the workload, topology, payload rate and availability condition constant when comparing link hardware. Then separately test the application effect. Keep a component power budget for thermal design and an end-to-end energy ledger for useful service.

## Serviceability is a design requirement with a topology

The relevant maintenance question is what must be isolated, reached and replaced after a specified fault. A front-panel module can offer a convenient replacement boundary, but dense cabling may make access difficult. More integrated optics can change the set of replaceable assemblies and require a different spare strategy. Neither arrangement is automatically more reliable merely because it contains fewer visible boxes. Failure rates, shared dependencies, detection quality and restoration time all matter.

Consider a single optical engine serving several logical links. Its failure may affect more than one endpoint, depending on the design. Consider a removable module with one marginal connection: it may produce intermittent errors rather than a clean link-down event. The software can experience retries or a degraded route while the hardware inventory still looks complete. Acceptance should exercise the intended link rates and communication patterns, and operations should connect error telemetry to physical cable and component identities.

## Treat cabling and cooling as part of the network

Fiber routes require handling, cleaning, bend control, labeling and accessible connection points according to the supplied hardware requirements. Copper routes impose their own bend, weight and reach constraints. Dense optical and switching equipment also dissipates heat at a specific location; a switch may have a liquid interface even when its neighboring networking equipment uses air. Moving optical conversion inward can change where heat must be captured. The installation review should therefore connect the logical network graph to cable routes, cooling interfaces and the actual replacement procedure.

## Worked example: A synthetic optical power comparison

- Compare 64 equivalent links at the same payload capability; each link has two counted endpoints.
- Design A assigns 20 W per endpoint to the included optical subsystem.
- Design B assigns 8 W per endpoint plus a shared 160 W laser subsystem and 100 W of incremental cooling electricity. Everything else is held equal.

1. Count optical endpoints — 64 × 2 = 128 endpoints — Counting only one side would understate a full-link comparison.
2. Calculate design A — 128 × 20 = 2,560 W — The stated A boundary has no extra shared load in this constructed example.
3. Calculate design B — 128 × 8 + 160 + 100 = 1,284 W — Include the shared and cooling terms instead of comparing only engine power.
4. Compare at the stated boundary — 2,560 − 1,284 = 1,276 W — The difference is 49.8% of A’s included subsystem power.

**Result:** B uses 1.276 kW less within this hypothetical equal-service boundary. It does not establish the saving of an actual CPO product or whole data center.

**Model boundary:** All wattages are invented. Real comparisons require product-specific optical budgets, load conditions and replacement architectures.

## The tradeoff

Choice: Move optical engines closer to the switch silicon.

Benefit: Potentially reduce electrical-path loss and the power needed to sustain high-rate signaling.

Cost: Change packaging, thermal integration, supply-chain dependencies and the set of components that can be serviced independently.

## When the situation changes

Trigger: A marginal link remains up but repeatedly corrects or retries traffic.

Mechanism: Usable payload bandwidth or latency consistency degrades, extending communication phases before a simple device-count monitor flags a failure.

Response: Correlate physical-link error counters and workload timing; isolate the affected path using the qualified operating procedure and verify performance after repair.

## Apply the idea

Suppose design B causes a 1 MW compute workload to run one extra minute while saving 1.276 kW throughout a one-hour baseline job. Could the link-power saving offset that extra compute energy?

<details>
<summary>Reveal the worked answer</summary>

Extra compute energy is about 16.67 kWh. A uses 2.56 kWh of the compared network subsystem in 60 minutes; B uses 1.284 × 61/60 = 1.3054 kWh. The network saving is only about 1.255 kWh.

The longer compute duration overwhelms the smaller network energy saving. The scenario is synthetic and does not assert that CPO slows workloads; it demonstrates why each design must be compared over the time needed to complete the same useful output.

</details>

**The idea to keep:** Moving optical conversion changes the electrical path and service boundary; it does not remove the need for a complete link budget and operating plan.

## Sources and reading boundaries

- [Scaling AI Factories with Co-Packaged Optics for Better Power Efficiency](https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/) — Describes moving optical conversion nearer switch silicon and the associated electrical-path mechanism. Read 2026-09-06. August 18, 2025 vendor account; availability and benefit claims are dated proposals, not universal deployment evidence.
- [NVIDIA Optical Transceivers and Cables](https://www.nvidia.com/en-us/networking/interconnect/) — Provides distinct interconnect product categories whose compatibility must be checked at the actual interface. Read 2026-09-06. Product catalog and marketing page; no power, reach or reliability rating is adopted without its specific datasheet.

## Check your understanding: Healthy devices, waiting job

Pause and make a prediction, then compare your reasoning.

A hypothetical synchronized training step cannot finish until every participant completes its required exchange. One shared fabric link becomes congested, although every accelerator remains healthy.

**Pause and predict:** Can the job slow down without losing any accelerators? Trace the dependency.

<details>
<summary>Compare your reasoning</summary>

Yes. Delayed communication can hold up the exchange that the entire step needs before it can advance.

Healthy endpoints do not establish a healthy end-to-end communication path. Follow the affected traffic through shared links and the collective's dependencies. Placement or path changes might help, but only if they relieve the actual constrained route.

</details>

**The next problem:** The cluster also needs durable data and recoverable progress. What survives when an interruption stops the job?

Continue in **Storage, orchestration and recovery**: Storage is a traffic and state system.
