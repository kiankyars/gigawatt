# GIGAWATT — the domain map

<!-- Generated from domain-map.json, research-sources.json and lessons.json. Edit those sources; run uv run gigawatt-map. -->

As of **2026-09-06**. Planning baseline; expanded lessons, visuals and assessments are not yet implemented or reviewed.

From grid connection to useful compute. Follow the power, close the heat path, operate the system.

[Interactive map](domain-map.html) · [Course review](COURSE_REVIEW.md) · [Source index](../research/INDEX.md) · [Research library](../research/README.md)

## Teaching contract

**Scope:** Modern AI data-center infrastructure, including conventional facilities and retrofit alternatives needed to explain engineering choices. System understanding and bounded quantitative decisions, not professional design qualification.

**Audience:** Technically curious learners with arithmetic, percentages, unit conversion, simple graph reading and general computer literacy. No prior data-center, electrical, cooling or networking vocabulary is assumed. Explain additional algebra before relying on it; introduce specialized mathematics and professional practice only to the depth needed for the stated outcomes.

**Runtime:** A substantial single course, potentially up to ten hours. Runtime is unallocated until section prototypes and learner rehearsals establish the depth each objective needs; this map is not a ten-hour script.

## Evidence and baseline coverage

Source mappings identify research leads for domains, not verified support for every proposed claim or objective. The seed corpus is not exhaustive. Verify particular claims at lesson authoring, follow original references, retain dates and assumptions, and record contradictions rather than averaging them away.

Source-to-domain mappings are derived from `research-sources.json` → `sources[].domains`. They identify research connections, not verified support for every objective.

- **partial:** The current player teaches a useful fragment of this objective. It still needs expansion, an application assessment and review.
- **missing:** The current player does not substantively teach this objective. Related mentions or source links do not count as teaching.
- **complete:** Reserved for a scripted, implemented and reviewed objective with an application assessment. No objective is marked complete in this planning baseline.

**Anti-pattern:** The encyclopedic survey: naming every component, paraphrasing every article, animating an inventory or increasing runtime without teaching a mechanism, worked example, consequential tradeoff, failure or limiting case, and transfer to a changed situation.


## System lanes

### Frame the system

Define quantities and the useful work the system must deliver.

- [D01 — System boundaries and quantities](#d01)
- [D02 — Workloads and the infrastructure brief](#d02)

### Bring power to the racks

Connect, distribute, protect and convert electricity.

- [D03 — Siting, grid connection and supply](#d03)
- [D04 — Campus and building power distribution](#d04)
- [D05 — Continuity, storage and protection](#d05)
- [D06 — Rack power and the 800 V DC transition](#d06)

### Turn hardware into useful work

Coordinate compute, memory, networks, storage and jobs.

- [D07 — Compute, memory and the rack](#d07)
- [D08 — Networking and interconnects](#d08)
- [D09 — Storage, orchestration and recovery](#d09)

### Return the heat

Capture heat at the devices and reject it under real site conditions.

- [D10 — Chip and rack heat capture](#d10)
- [D11 — Heat rejection, climate and water](#d11)

### Build, operate and decide

Make the physical system deliverable, testable, maintainable and economically coherent.

- [D12 — Physical site, buildings and safety](#d12)
- [D13 — Design, procurement and commissioning](#d13)
- [D14 — Controls, operations and reliability](#d14)
- [D15 — Capacity, cost and system decisions](#d15)

## Proposed teaching sequence

Domain IDs are stable references, not chapter numbers. This sequence respects prerequisites; runtime is not yet allocated.

### A01 — See the system and define the job

[D01](#d01) → [D02](#d02)

Establish the vocabulary, three paths and the workload brief used throughout.

### A02 — Find a site and deliver power

[D03](#d03) → [D12](#d12) → [D04](#d04)

Make the physical location, utility connection and single-line diagram legible.

### A03 — Keep it running and enter the rack

[D05](#d05) → [D06](#d06)

Compare continuity and conversion choices, including 800 V DC, against interfaces and failures.

### A04 — Make the cluster productive

[D07](#d07) → [D08](#d08) → [D09](#d09)

Connect compute, memory, communication, storage and scheduling to useful progress.

### A05 — Close the heat and water balances

[D10](#d10) → [D11](#d11)

Follow heat from local device limits to climate-dependent rejection and resource use.

### A06 — Deliver, operate and make decisions

[D13](#d13) → [D14](#d14) → [D15](#d15)

Test complete service paths, operate them, and defend a system decision with uncertainty.

## Domain teaching plans

<a id="d01"></a>

### D01 — System boundaries and quantities

**Central question:** What exactly does a megawatt of data-center capacity describe?

Give every later calculation a unit, a boundary, and an operating condition.

**Included scope:**

- Campus, building, hall, row, rack, server, package and die
- Power, energy, real/apparent power, efficiency and time
- Nameplate, reserved, commissioned, available, demanded and productive capacity
- Physical flows versus commercial relationships; reference designs versus actual sites

**Prerequisites:** None in this map.

**Learning objectives and assessments:**

#### D01.1

Trace electrical energy, heat, and information through a data center while keeping the accounting boundaries separate.

**Assessment:** Annotate one campus diagram with three paths and explain why useful computation and dissipated heat are not competing energy allocations.

**Existing baseline:** partial. `one-rack` — One campus. Two journeys.; `electrical-to-heat` — The watt becomes heat.; `whole-system` — Follow the power. Close the heat path.

#### D01.2

Convert power and energy across units and time; distinguish a measured load from a capacity rating.

**Assessment:** Calculate an energy total from a stepped load profile and identify what cannot be inferred from a service rating.

**Existing baseline:** partial. `power-and-energy` — A watt is a rate.; `capacity-stages` — Connected is a milestone.

#### D01.3

Define denominators for facility, IT and compute-only metrics and label the time window.

**Assessment:** Reconcile a facility energy ledger with IT energy, overhead and a separately measured workload output.

**Existing baseline:** partial. `facility-overhead` — Budget the whole facility.; `useful-compute` — Watts do not measure useful work.

#### D01.4

Separate physical principles, design specifications, observed deployments, announcements, forecasts and teaching assumptions.

**Assessment:** Classify six supplied claims and state the additional evidence needed to call capacity operational.

**Existing baseline:** partial. `abilene-case` — Read a real headline precisely.; `capacity-stages` — Connected is a milestone.

**Visual plan: One campus, three paths**

- Prediction: Which quantities change when the accounting boundary moves from the utility meter to IT equipment?
- Interaction: Select power, heat or information, then zoom campus → rack → chip while retaining the enclosing boundary.
- Model boundary: Arrows show connectivity and direction. Their animation does not represent physical propagation speed.

**Worked example:** Use a synthetic 24-hour load trace to compare MW, MWh and separately specified capacity; label all measurement points.

**Design tradeoff:** A simple system model is easier to reason with; omitted loads and changing boundaries can invalidate its conclusion.

**Failure or maintenance scenario:** A capacity headline combines planned expansion with an existing phase. Identify the double count before doing arithmetic.

**Research connections:**

- [P01 — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) · `page_reviewed` · [local note](../research/sources/P01.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P07 — ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) · `page_reviewed` · [local note](../research/sources/P07.md)
- [P09 — The Datacenter as a Computer: designing warehouse-scale machines](https://research.google/pubs/the-datacenter-as-a-computer-designing-warehouse-scale-machines/) · `public_excerpt_reviewed` · [local note](../research/sources/P09.md)
- [P10 — Incorporate Minimum Efficiency Requirements for Heating and Cooling Products into Federal Acquisition Documents](https://www.energy.gov/cmei/femp/incorporate-minimum-efficiency-requirements-heating-and-cooling-products-federal) · `page_reviewed` · [local note](../research/sources/P10.md)
- [SA14 — AI Datacenter Energy Dilemma - Race for AI Datacenter Space](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race) · `public_excerpt_reviewed` · [local note](../research/sources/SA14.md)
- [SA31 — From Tokens to Burgers: A Water Footprint Face-Off](https://newsletter.semianalysis.com/p/from-tokens-to-burgers-a-water-footprint) · `public_excerpt_reviewed` · [local note](../research/sources/SA31.md)
- [SA33 — Stop Saying Half of 2026 US Datacenter Capacity Is Canceled](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA33.md)
- [SA37 — xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA37.md)
- [SA39 — OpenAI Stargate Joint Venture Demystified | Microsoft Sore Loser, Does Softbank Have The Capital?, Texas GigaCampus, Winners & Losers](https://newsletter.semianalysis.com/p/openai-stargate-joint-venture-demystified) · `public_excerpt_reviewed` · [local note](../research/sources/SA39.md)
- [E22133B3DE1 — EIA — Laws of energy](https://www.eia.gov/energyexplained/what-is-energy/laws-of-energy.php) · `page_reviewed` · [local note](../research/sources/E22133B3DE1.md)
- [E3F4CB1B7FF — DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) · `page_reviewed` · [local note](../research/sources/E3F4CB1B7FF.md)
- [ED20FD8CBCF — EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) · `page_reviewed` · [local note](../research/sources/ED20FD8CBCF.md)
- [EB34D92F523 — OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) · `page_reviewed` · [local note](../research/sources/EB34D92F523.md)
- [EE02276C332 — MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) · `page_reviewed` · [local note](../research/sources/EE02276C332.md)

<a id="d02"></a>

### D02 — Workloads and the infrastructure brief

**Central question:** What useful work must the facility deliver, and on what schedule?

Derive infrastructure requirements from the service or job rather than starting with an equipment inventory.

**Included scope:**

- Training, inference and conventional services as different load and service profiles
- Throughput, latency, availability, memory demand and utilization
- Parallelism, communication, checkpointing and workload-driven power variation
- Design envelopes and uncertainty; avoiding universal watts-to-tokens conversions

**Prerequisites:** [D01 — System boundaries and quantities](#d01)

**Learning objectives and assessments:**

#### D02.1

Translate a workload brief into compute, memory, network, storage, power and service requirements.

**Assessment:** Compare two supplied training and inference briefs and explain which requirements need measurement rather than a rack-count estimate.

**Existing baseline:** partial. `useful-compute` — Watts do not measure useful work.

#### D02.2

Distinguish hardware occupancy, power draw and productive utilization.

**Assessment:** Explain three traces in which the same installed hardware produces different useful output; identify idle and waiting intervals.

**Existing baseline:** partial. `useful-compute` — Watts do not measure useful work.

#### D02.3

Explain how batching, parallel execution and synchronized job phases change the infrastructure demand profile.

**Assessment:** Read a supplied job timeline and predict communication, checkpoint and load-transition intervals without assuming a universal waveform.

**Existing baseline:** missing. No existing lesson mapped.

#### D02.4

State an infrastructure design envelope and identify which assumptions a benchmark can and cannot validate.

**Assessment:** Write acceptance criteria for a hypothetical cluster using declared workload, precision, batch, latency and availability conditions.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: From job timeline to demand**

- Prediction: Does a higher average GPU power draw necessarily imply higher useful throughput?
- Interaction: Switch between labeled training, interactive inference and batch inference scenarios; align work, communication and power traces.
- Model boundary: Traces are illustrative until tied to an identified measurement, workload and hardware configuration.

**Worked example:** Compare a compute-limited and communication-limited synthetic job at identical installed power capacity; calculate elapsed time and useful work per energy.

**Design tradeoff:** Provisioning for peaks, pooling resources and accepting queueing produce different cost and service outcomes.

**Failure or maintenance scenario:** A new workload meets the average MW budget but violates a latency or transient requirement.

**Research connections:**

- [SA03 — 100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) · `public_excerpt_reviewed` · [local note](../research/sources/SA03.md)
- [SA04 — Multi-Datacenter Training: OpenAI’s Ambitious Plan To Beat Google’s Infrastructure](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) · `public_excerpt_reviewed` · [local note](../research/sources/SA04.md)
- [SA09 — How Much Do GPU Clusters Really Cost?](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost) · `public_excerpt_reviewed` · [local note](../research/sources/SA09.md)
- [P07 — ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) · `page_reviewed` · [local note](../research/sources/P07.md)
- [P08 — Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) · `page_reviewed` · [local note](../research/sources/P08.md)
- [P09 — The Datacenter as a Computer: designing warehouse-scale machines](https://research.google/pubs/the-datacenter-as-a-computer-designing-warehouse-scale-machines/) · `public_excerpt_reviewed` · [local note](../research/sources/P09.md)
- [SA11 — AI Training Load Fluctuations at Gigawatt-scale - Risk of Power Grid Blackout?](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout) · `public_excerpt_reviewed` · [local note](../research/sources/SA11.md)
- [SA18 — GPU Cloud Economics Explained – The Hidden Truth](https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA18.md)
- [SA20 — H100 vs GB200 NVL72 Training Benchmarks - Power, TCO, and Reliability Analysis, Software Improvement Over Time](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks) · `public_excerpt_reviewed` · [local note](../research/sources/SA20.md)
- [SA21 — The Memory Wall: Past, Present, and Future of DRAM](https://newsletter.semianalysis.com/p/the-memory-wall) · `public_excerpt_reviewed` · [local note](../research/sources/SA21.md)
- [SA22 — Scaling the Memory Wall: The Rise and Roadmap of HBM](https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm) · `public_excerpt_reviewed` · [local note](../research/sources/SA22.md)
- [SA23 — CPUs are Back: The Datacenter CPU Landscape in 2026](https://newsletter.semianalysis.com/p/cpus-are-back-the-datacenter-cpu) · `public_excerpt_reviewed` · [local note](../research/sources/SA23.md)
- [SA25 — TPUv7: Google Takes a Swing at the King](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA25.md)
- [SA26 — AWS Trainium3 Deep Dive | A Potential Challenger Approaching](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential) · `public_excerpt_reviewed` · [local note](../research/sources/SA26.md)
- [SA27 — RL Systems Mind the Gap: Matching Trainer and Generator Throughput](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching) · `public_excerpt_reviewed` · [local note](../research/sources/SA27.md)
- [SA30 — Meta’s Infrastructure Team Needs A Culture Reset](https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a) · `public_excerpt_reviewed` · [local note](../research/sources/SA30.md)
- [SA36 — Microsoft's AI Strategy Deconstructed - From Energy to Tokens](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed) · `public_excerpt_reviewed` · [local note](../research/sources/SA36.md)
- [SA40 — Google AI Infrastructure Supremacy: Systems Matter More Than Microarchitecture](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy) · `public_excerpt_reviewed` · [local note](../research/sources/SA40.md)
- [P13 — Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) · `page_reviewed` · [local note](../research/sources/P13.md)
- [EE02276C332 — MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) · `page_reviewed` · [local note](../research/sources/EE02276C332.md)
- [E23909D618E — NVIDIA — DGX SuperPOD Key Components](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-superpod-components.html) · `page_reviewed` · [local note](../research/sources/E23909D618E.md)
- [E2C35A11B05 — NVIDIA Triton — Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/user_guide/batcher.html) · `page_reviewed` · [local note](../research/sources/E2C35A11B05.md)
- [E0814EDF226 — Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) · `page_reviewed` · [local note](../research/sources/E0814EDF226.md)

<a id="d03"></a>

### D03 — Siting, grid connection and supply

**Central question:** Where can the required power actually arrive, and when?

Connect the physical site decision to grid constraints, available infrastructure and the project schedule.

**Included scope:**

- Load connection, utility studies, substations, transmission and distribution interfaces
- Generation and behind-the-meter supply where they affect delivery, dispatch or resilience
- Capacity, energy, fuel, emissions, curtailment and time matching
- Land, fiber, water, climate and local constraints as joint siting inputs

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D02 — Workloads and the infrastructure brief](#d02)

**Learning objectives and assessments:**

#### D03.1

Trace a physical supply path and distinguish it from a power purchase agreement or energy attribute claim.

**Assessment:** Draw the metered connection separately from two commercial arrangements; name what each establishes.

**Existing baseline:** partial. `sources-and-grid` — Follow the physical connection.

#### D03.2

Explain voltage, current and conductor loss in a bounded AC or DC comparison.

**Assessment:** Compare two balanced three-phase transfer scenarios with stated power factor and conductor resistance; list excluded losses.

**Existing baseline:** partial. `raise-voltage` — Go farther. Raise the voltage.

#### D03.3

Explain the milestones and constraints between a proposed large load and service available to that load.

**Assessment:** Turn a supplied project timeline into a capacity ledger without treating an application, agreement or energized substation as commissioned IT.

**Existing baseline:** partial. `capacity-stages` — Connected is a milestone.

#### D03.4

Compare utility-only and on-site supply options against energy, capacity, fuel, grid and operating requirements.

**Assessment:** Evaluate a synthetic siting brief with outage, fuel-delivery and curtailment constraints; record unresolved utility and local requirements.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Two maps: electrons and agreements**

- Prediction: Which contractual change increases physically deliverable power at the meter?
- Interaction: Overlay the physical connection, commercial contracts and project milestones on the same site comparison.
- Model boundary: A contract is not an electrical edge. Grid rules, interconnection terms and permits require a named jurisdiction and date.

**Worked example:** Compare two hypothetical sites with different delivery dates, service limits, climate and fiber reach; keep ratings, costs and operating assumptions explicit.

**Design tradeoff:** Earlier on-site supply may trade schedule advantage against fuel, emissions, operating complexity and future grid integration.

**Failure or maintenance scenario:** Supply is available in aggregate but a transmission constraint or fuel interruption prevents the promised operating profile.

**Research connections:**

- [SA04 — Multi-Datacenter Training: OpenAI’s Ambitious Plan To Beat Google’s Infrastructure](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) · `public_excerpt_reviewed` · [local note](../research/sources/SA04.md)
- [SA07 — US Grid Constraints: Towards 40GW+ of Behind-The-Meter Datacenter by 2028?](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw) · `public_excerpt_reviewed` · [local note](../research/sources/SA07.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P12 — Large Loads Action Plan](https://www.nerc.com/initiatives/large-loads-action-plan) · `public_excerpt_reviewed` · [local note](../research/sources/P12.md)
- [SA11 — AI Training Load Fluctuations at Gigawatt-scale - Risk of Power Grid Blackout?](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout) · `public_excerpt_reviewed` · [local note](../research/sources/SA11.md)
- [SA12 — How AI Labs Are Solving the Power Crisis: The Onsite Gas Deep Dive](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power) · `public_excerpt_reviewed` · [local note](../research/sources/SA12.md)
- [SA14 — AI Datacenter Energy Dilemma - Race for AI Datacenter Space](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race) · `public_excerpt_reviewed` · [local note](../research/sources/SA14.md)
- [SA31 — From Tokens to Burgers: A Water Footprint Face-Off](https://newsletter.semianalysis.com/p/from-tokens-to-burgers-a-water-footprint) · `public_excerpt_reviewed` · [local note](../research/sources/SA31.md)
- [SA32 — Are AI Datacenters Increasing Electric Bills for American Households?](https://newsletter.semianalysis.com/p/are-ai-datacenters-increasing-electric) · `public_excerpt_reviewed` · [local note](../research/sources/SA32.md)
- [SA33 — Stop Saying Half of 2026 US Datacenter Capacity Is Canceled](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA33.md)
- [SA34 — $12B of US ratepayers' money wasted on a modeling mistake and PJM wants to do it again](https://newsletter.semianalysis.com/p/12b-of-us-ratepayers-money-wasted) · `public_excerpt_reviewed` · [local note](../research/sources/SA34.md)
- [SA35 — Nvidia GPU Debt Backstop Unleashes the AI Project Trinity: Capital, Offtake and Datacenters](https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes) · `public_excerpt_reviewed` · [local note](../research/sources/SA35.md)
- [SA36 — Microsoft's AI Strategy Deconstructed - From Energy to Tokens](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed) · `public_excerpt_reviewed` · [local note](../research/sources/SA36.md)
- [SA37 — xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA37.md)
- [SA38 — How Oracle Is Winning the AI Compute Market](https://newsletter.semianalysis.com/p/how-oracle-is-winning-the-ai-compute-market) · `public_excerpt_reviewed` · [local note](../research/sources/SA38.md)
- [SA39 — OpenAI Stargate Joint Venture Demystified | Microsoft Sore Loser, Does Softbank Have The Capital?, Texas GigaCampus, Winners & Losers](https://newsletter.semianalysis.com/p/openai-stargate-joint-venture-demystified) · `public_excerpt_reviewed` · [local note](../research/sources/SA39.md)
- [EB34D92F523 — OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) · `page_reviewed` · [local note](../research/sources/EB34D92F523.md)
- [ED8255C2875 — US EPA — Physical PPA](https://www.epa.gov/green-power-markets/physical-ppa) · `page_reviewed` · [local note](../research/sources/ED8255C2875.md)
- [E61807424F1 — DOE — Islanding a Microgrid](https://www.energy.gov/cmei/femp/articles/islanding-microgrid) · `page_reviewed` · [local note](../research/sources/E61807424F1.md)
- [E45AB7B1BC1 — Schneider Electric — Installed apparent power](https://www.electrical-installation.org/enwiki/Installed_apparent_power_(kVA)) · `page_reviewed` · [local note](../research/sources/E45AB7B1BC1.md)
- [E21653C0173 — ERCOT — Batch Zero large-load connection announcement, June 18, 2026](https://www.ercot.com/news/release/06182026-puct-approves-ercots) · `page_reviewed` · [local note](../research/sources/E21653C0173.md)

<a id="d04"></a>

### D04 — Campus and building power distribution

**Central question:** How does power get from the connection to each load?

Teach electrical topology, equipment roles and rating boundaries before comparing architecture changes.

**Included scope:**

- Single-line diagrams and voltage levels
- Transformers, switchgear, switchboards, busway, cables and distribution units
- Real/apparent power, power factor, efficiency, harmonic and thermal limits
- AC distribution and alternative DC conversion locations
- House loads, IT loads, reserved capacity and expansion phases

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D03 — Siting, grid connection and supply](#d03)

**Learning objectives and assessments:**

#### D04.1

Read a generic single-line diagram and explain what each distribution component changes, measures, switches or protects.

**Assessment:** Annotate an unfamiliar generic diagram and identify the loads behind each boundary.

**Existing baseline:** partial. `substation-functions` — Open the substation.; `building-power-train` — Bring the power to the rack.

#### D04.2

Translate load requirements into currents and equipment loading without confusing kW with kVA or nameplate with usable capacity.

**Assessment:** Calculate loading in a stated balanced scenario, including conversion efficiency and a supplied power factor; explain missing design inputs.

**Existing baseline:** partial. `raise-voltage` — Go farther. Raise the voltage.

#### D04.3

Compare centralized and distributed conversion and identify which conductors, equipment and loss boundaries change.

**Assessment:** Mark the changed interfaces on AC, near-rack DC and facility DC reference diagrams without claiming one universal efficiency improvement.

**Existing baseline:** missing. No existing lesson mapped.

#### D04.4

Reconcile IT and auxiliary loads with a downstream electrical capacity budget across project phases.

**Assessment:** Find the binding transformer, feeder or service constraint in a synthetic phase-opening plan.

**Existing baseline:** partial. `capacity-bottleneck` — The smallest limit wins.; `building-power-train` — Bring the power to the rack.

**Visual plan: A living single-line diagram**

- Prediction: Which current changes when conversion moves upstream, and which upstream current may remain essentially unchanged?
- Interaction: Select a load to trace its upstream path; switch between conversion placements and display currents at labeled boundaries.
- Model boundary: A teaching topology is not an as-built design, a protection study or a conductor sizing tool.

**Worked example:** Work through one assumed facility-to-rack power budget, including conversion losses and separately reserved auxiliary loads.

**Design tradeoff:** Centralization can change conversion count, serviceability and fault scope; actual benefits depend on the selected topology and operating point.

**Failure or maintenance scenario:** A row can fit physically while exceeding a feeder's available rating after required reserves.

**Research connections:**

- [SA01 — Datacenter Anatomy Part 1: Electrical Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical) · `public_excerpt_reviewed` · [local note](../research/sources/SA01.md)
- [SA10 — Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) · `public_excerpt_reviewed` · [local note](../research/sources/SA10.md)
- [P01 — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) · `page_reviewed` · [local note](../research/sources/P01.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P04 — Tier Classification System](https://uptimeinstitute.com/tiers) · `page_reviewed` · [local note](../research/sources/P04.md)
- [P05 — NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) · `page_reviewed` · [local note](../research/sources/P05.md)
- [SA14 — AI Datacenter Energy Dilemma - Race for AI Datacenter Space](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race) · `public_excerpt_reviewed` · [local note](../research/sources/SA14.md)
- [SA29 — The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) · `public_excerpt_reviewed` · [local note](../research/sources/SA29.md)
- [P16 — Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) · `page_reviewed` · [local note](../research/sources/P16.md)
- [E3F4CB1B7FF — DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) · `page_reviewed` · [local note](../research/sources/E3F4CB1B7FF.md)
- [E45AB7B1BC1 — Schneider Electric — Installed apparent power](https://www.electrical-installation.org/enwiki/Installed_apparent_power_(kVA)) · `page_reviewed` · [local note](../research/sources/E45AB7B1BC1.md)
- [EBFFD23506A — Schneider Electric — Choice of transformer rating](https://www.electrical-installation.org/enwiki/Choice_of_transformer_rating) · `page_reviewed` · [local note](../research/sources/EBFFD23506A.md)

<a id="d05"></a>

### D05 — Continuity, storage and protection

**Central question:** What survives a disturbance, and for how long?

Connect backup supply, fault isolation and maintenance to complete operating paths.

**Included scope:**

- UPS, batteries, generators, transfer sequences and load shedding
- Stored energy versus discharge power; transient response versus outage duration
- N, N+1, 2N, common-mode failures and maintainability
- Grounding, fault detection, selective isolation and AC/DC protection concepts
- Electrical and thermal ride-through together

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D04 — Campus and building power distribution](#d04)

**Learning objectives and assessments:**

#### D05.1

Calculate bounded stored-energy runtime while checking discharge power and reserve assumptions.

**Assessment:** Compare two storage systems with the same MWh but different MW limits; explain why neither energy alone nor nameplate guarantees ride-through.

**Existing baseline:** partial. `ride-through` — The battery buys time.

#### D05.2

Trace an interruption, transfer and restoration sequence including IT, cooling and controls.

**Assessment:** Predict which loads remain supported at each step of a supplied sequence; identify a missing auxiliary supply.

**Existing baseline:** partial. `ride-through` — The battery buys time.; `redundant-paths` — A second path must be useful.

#### D05.3

Evaluate path independence and surviving capacity during both a fault and planned maintenance.

**Assessment:** Find a common-mode dependency in a two-feed diagram and calculate load support with one path unavailable.

**Existing baseline:** partial. `redundant-paths` — A second path must be useful.; `fault-domains` — Keep one fault from spreading.

#### D05.4

Explain why fault clearing and grounding require topology-specific AC/DC protection design.

**Assessment:** Compare two conceptual isolation sequences and list the protection evidence needed before endorsing either architecture.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Failure timeline and surviving paths**

- Prediction: Can the rack remain energized while the overall service still becomes unavailable?
- Interaction: Inject an outage or isolate equipment; run a discrete sequence with separate electrical, thermal and control availability tracks.
- Model boundary: Timing and reliability values are declared scenarios, not device guarantees or a Tier certification.

**Worked example:** Calculate a storage energy budget and a surviving-path power budget separately, then test whether both support the same required interval.

**Design tradeoff:** More redundant equipment may improve maintainability but can add shared controls, switching complexity and underutilized capacity.

**Failure or maintenance scenario:** A successful electrical transfer leaves cooling controls unavailable; determine the missing evidence for thermal ride-through.

**Research connections:**

- [SA01 — Datacenter Anatomy Part 1: Electrical Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical) · `public_excerpt_reviewed` · [local note](../research/sources/SA01.md)
- [SA07 — US Grid Constraints: Towards 40GW+ of Behind-The-Meter Datacenter by 2028?](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw) · `public_excerpt_reviewed` · [local note](../research/sources/SA07.md)
- [SA10 — Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) · `public_excerpt_reviewed` · [local note](../research/sources/SA10.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P03 — Management and Operations Guideline](https://uptimeinstitute.com/professional-services/management-operations/mando-criteria) · `page_reviewed` · [local note](../research/sources/P03.md)
- [P04 — Tier Classification System](https://uptimeinstitute.com/tiers) · `page_reviewed` · [local note](../research/sources/P04.md)
- [P05 — NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) · `page_reviewed` · [local note](../research/sources/P05.md)
- [P06 — Open Rack/SpecsAndDesigns](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) · `page_reviewed` · [local note](../research/sources/P06.md)
- [P11 — NFPA 75: Standard for the Fire Protection of Information Technology Equipment](https://www.nfpa.org/codes-and-standards/nfpa-75-standard-development/75) · `candidate_not_reviewed` · [local note](../research/sources/P11.md)
- [P12 — Large Loads Action Plan](https://www.nerc.com/initiatives/large-loads-action-plan) · `public_excerpt_reviewed` · [local note](../research/sources/P12.md)
- [SA11 — AI Training Load Fluctuations at Gigawatt-scale - Risk of Power Grid Blackout?](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout) · `public_excerpt_reviewed` · [local note](../research/sources/SA11.md)
- [SA12 — How AI Labs Are Solving the Power Crisis: The Onsite Gas Deep Dive](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power) · `public_excerpt_reviewed` · [local note](../research/sources/SA12.md)
- [SA37 — xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA37.md)
- [P16 — Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) · `page_reviewed` · [local note](../research/sources/P16.md)
- [ED20FD8CBCF — EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) · `page_reviewed` · [local note](../research/sources/ED20FD8CBCF.md)
- [EB34D92F523 — OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) · `page_reviewed` · [local note](../research/sources/EB34D92F523.md)
- [E0814EDF226 — Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) · `page_reviewed` · [local note](../research/sources/E0814EDF226.md)
- [E9FFEE6828F — Schneider Electric — Coordination between circuit-breakers](https://www.electrical-installation.org/enwiki/Coordination_between_circuit-breakers) · `page_reviewed` · [local note](../research/sources/E9FFEE6828F.md)
- [E1423005C7C — ABB — Protection Devices for Direct Current Applications](https://library.e.abb.com/public/5cd83dcb95a74dcdb571be5f256e1af8/9AKK108470A9606_en_B_Protection%20Devices%20for%20Direct%20Current%20Applications%20-%20Technical%20Application%20Paper.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/E1423005C7C.md)
- [E2A3F76B3F9 — Schneider Electric — Definition of standardised earthing schemes](https://www.electrical-installation.org/enwiki/Definition_of_standardised_earthing_schemes) · `public_excerpt_reviewed` · [local note](../research/sources/E2A3F76B3F9.md)

<a id="d06"></a>

### D06 — Rack power and the 800 V DC transition

**Central question:** Where should voltage conversion happen as rack demand changes?

Use 800 V DC as an architecture comparison grounded in current, interfaces and deployment constraints.

**Included scope:**

- Power shelves, rack buses, converters, point-of-load regulation and auxiliary loads
- Conventional AC-to-rack conversion, sidecars and broader facility DC options
- 800 V DC and other specified voltage arrangements; product/version boundaries
- Copper, connectors, busbars, stored energy, service access and space
- Load transients, protection interfaces, brownfield and greenfield choices

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D04 — Campus and building power distribution](#d04), [D05 — Continuity, storage and protection](#d05)

**Learning objectives and assessments:**

#### D06.1

Trace conversion from rack input to processor rails and distinguish whole-rack power from chip power.

**Assessment:** Label every voltage and power boundary on two supplied rack diagrams and reject a misleading per-GPU TDP calculation.

**Existing baseline:** partial. `rack-conversion` — The rack changes the rules.; `low-voltage-current` — Low voltage. Enormous current.

#### D06.2

Quantify how distribution voltage changes current at fixed DC power without treating conductor loss as total system efficiency.

**Assessment:** Compute currents for a declared 100 kW DC boundary at 50 V and 800 V, then state why this does not size a real conductor or establish an efficiency delta.

**Existing baseline:** partial. `low-voltage-current` — Low voltage. Enormous current.

#### D06.3

Compare near-rack sidecars, rack-level conversion and facility DC as distinct architectures.

**Assessment:** Place conversion, storage, protection and AC/DC boundaries for each; distinguish announced products from proposed future designs.

**Existing baseline:** missing. No existing lesson mapped.

#### D06.4

Evaluate a rack power upgrade against connector, bus, protection, auxiliary and transient interfaces.

**Assessment:** Write an interface checklist for a synthetic higher-density rack migration, with every unknown left explicit.

**Existing baseline:** missing. No existing lesson mapped.

#### D06.5

Explain how retrofit constraints can reverse a seemingly attractive greenfield architecture choice.

**Assessment:** Choose between two supplied migration paths using space, downtime, conversion and maintenance assumptions; show what would change the decision.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Move the conversion boundary**

- Prediction: Which constraints move, which remain, and where does a new protection or service interface appear?
- Interaction: Morph a shared diagram between existing AC, sidecar and broader DC reference architectures; keep unchanged equipment visually anchored.
- Model boundary: Use dated, identified reference architectures. Single-ended and bipolar voltage labels cannot be silently interchanged; benefits require stated comparisons.

**Worked example:** At a hypothetical 100 kW DC boundary, compare 50 V and 800 V currents; separately account for each assumed conversion stage and its load-dependent efficiency.

**Design tradeoff:** Higher distribution voltage changes current and packaging constraints while introducing different conversion, insulation, protection and service requirements.

**Failure or maintenance scenario:** A proposed sidecar upgrade clears rack space but does not solve an upstream AC feeder limit.

**Research connections:**

- [SA01 — Datacenter Anatomy Part 1: Electrical Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical) · `public_excerpt_reviewed` · [local note](../research/sources/SA01.md)
- [SA10 — Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) · `public_excerpt_reviewed` · [local note](../research/sources/SA10.md)
- [P05 — NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) · `page_reviewed` · [local note](../research/sources/P05.md)
- [P06 — Open Rack/SpecsAndDesigns](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) · `page_reviewed` · [local note](../research/sources/P06.md)
- [SA17 — Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition) · `public_excerpt_reviewed` · [local note](../research/sources/SA17.md)
- [SA19 — GB200 Hardware Architecture - Component Supply Chain & BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) · `public_excerpt_reviewed` · [local note](../research/sources/SA19.md)
- [SA24 — Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) · `public_excerpt_reviewed` · [local note](../research/sources/SA24.md)
- [P16 — Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) · `page_reviewed` · [local note](../research/sources/P16.md)
- [P17 — NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) · `page_reviewed` · [local note](../research/sources/P17.md)
- [E960EB5ED2E — Eaton — Rack Basics: Selection, Installation and Cooling](https://tripplite.eaton.com/support/rack-cabinet-basics-selection-installation-cooling) · `public_excerpt_reviewed` · [local note](../research/sources/E960EB5ED2E.md)
- [E8D4F19907B — Open Compute Project — Open Rack V3 Base Specification, revision 1.0](https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf) · `page_reviewed` · [local note](../research/sources/E8D4F19907B.md)

<a id="d07"></a>

### D07 — Compute, memory and the rack

**Central question:** What inside the rack determines useful performance?

Explain hardware organization only as deeply as needed to connect workload progress with infrastructure choices.

**Included scope:**

- CPU, accelerator, memory, host and accelerator interconnect roles
- Memory capacity and bandwidth, compute throughput and data movement
- Server, tray, rack and scale-up system boundaries
- Packaging and power/thermal density where they affect the facility
- Product specifications, measured performance and workload-dependent limits

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D02 — Workloads and the infrastructure brief](#d02)

**Learning objectives and assessments:**

#### D07.1

Locate compute, memory and communication components within a server and rack and explain their roles.

**Assessment:** Trace a simplified data path from storage through host memory to accelerator memory and compute.

**Existing baseline:** partial. `rack-conversion` — The rack changes the rules.

#### D07.2

Distinguish memory-capacity, memory-bandwidth, compute and communication limits.

**Assessment:** Use supplied workload and hardware numbers to identify a plausible bottleneck and state the model's assumptions.

**Existing baseline:** missing. No existing lesson mapped.

#### D07.3

Explain why chip count, advertised FLOPS and installed MW cannot independently establish job throughput.

**Assessment:** Compare two synthetic rack configurations with equal power envelopes but different memory and communication constraints.

**Existing baseline:** partial. `useful-compute` — Watts do not measure useful work.

#### D07.4

Connect server and rack organization to power, cooling, weight and maintenance interfaces.

**Assessment:** Identify the facility interface changes caused by replacing an air-cooled server row with a specified dense rack-scale system.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: A rack as a data path**

- Prediction: Which upgrade helps a workload that is waiting on memory rather than arithmetic?
- Interaction: Zoom rack → tray → package; highlight storage transfers, memory access, compute and scale-up communication with consistent boundaries.
- Model boundary: Use product-specific diagrams only with versions and sources. The generic data path is deliberately simplified.

**Worked example:** Apply a supplied compute/bandwidth model to two workloads, then explain which unmodeled communication or software effects could reduce throughput.

**Design tradeoff:** More tightly integrated systems can change performance and data movement while constraining service granularity and upgrade choices.

**Failure or maintenance scenario:** A failed component changes the usable topology and job capacity even though facility electrical capacity is unchanged.

**Research connections:**

- [SA03 — 100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) · `public_excerpt_reviewed` · [local note](../research/sources/SA03.md)
- [SA05 — AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) · `public_excerpt_reviewed` · [local note](../research/sources/SA05.md)
- [SA06 — Co-Packaged Optics (CPO) Book – Scaling with Light for the Next Wave of Interconnect](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling) · `public_excerpt_reviewed` · [local note](../research/sources/SA06.md)
- [SA10 — Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) · `public_excerpt_reviewed` · [local note](../research/sources/SA10.md)
- [P05 — NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) · `page_reviewed` · [local note](../research/sources/P05.md)
- [P06 — Open Rack/SpecsAndDesigns](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) · `page_reviewed` · [local note](../research/sources/P06.md)
- [P08 — Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) · `page_reviewed` · [local note](../research/sources/P08.md)
- [P09 — The Datacenter as a Computer: designing warehouse-scale machines](https://research.google/pubs/the-datacenter-as-a-computer-designing-warehouse-scale-machines/) · `public_excerpt_reviewed` · [local note](../research/sources/P09.md)
- [SA13 — Nvidia’s Optical Boogeyman – NVL72, Infiniband Scale Out, 800G & 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) · `public_excerpt_reviewed` · [local note](../research/sources/SA13.md)
- [SA17 — Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition) · `public_excerpt_reviewed` · [local note](../research/sources/SA17.md)
- [SA19 — GB200 Hardware Architecture - Component Supply Chain & BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) · `public_excerpt_reviewed` · [local note](../research/sources/SA19.md)
- [SA20 — H100 vs GB200 NVL72 Training Benchmarks - Power, TCO, and Reliability Analysis, Software Improvement Over Time](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks) · `public_excerpt_reviewed` · [local note](../research/sources/SA20.md)
- [SA21 — The Memory Wall: Past, Present, and Future of DRAM](https://newsletter.semianalysis.com/p/the-memory-wall) · `public_excerpt_reviewed` · [local note](../research/sources/SA21.md)
- [SA22 — Scaling the Memory Wall: The Rise and Roadmap of HBM](https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm) · `public_excerpt_reviewed` · [local note](../research/sources/SA22.md)
- [SA23 — CPUs are Back: The Datacenter CPU Landscape in 2026](https://newsletter.semianalysis.com/p/cpus-are-back-the-datacenter-cpu) · `public_excerpt_reviewed` · [local note](../research/sources/SA23.md)
- [SA24 — Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) · `public_excerpt_reviewed` · [local note](../research/sources/SA24.md)
- [SA25 — TPUv7: Google Takes a Swing at the King](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA25.md)
- [SA26 — AWS Trainium3 Deep Dive | A Potential Challenger Approaching](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential) · `public_excerpt_reviewed` · [local note](../research/sources/SA26.md)
- [SA27 — RL Systems Mind the Gap: Matching Trainer and Generator Throughput](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching) · `public_excerpt_reviewed` · [local note](../research/sources/SA27.md)
- [SA40 — Google AI Infrastructure Supremacy: Systems Matter More Than Microarchitecture](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy) · `public_excerpt_reviewed` · [local note](../research/sources/SA40.md)
- [P13 — Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) · `page_reviewed` · [local note](../research/sources/P13.md)
- [P14 — NVIDIA DGX SuperPOD: Next Generation Scalable Infrastructure for AI Leadership Reference Architecture Featuring NVIDIA DGX H100](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/) · `page_reviewed` · [local note](../research/sources/P14.md)
- [P17 — NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) · `page_reviewed` · [local note](../research/sources/P17.md)
- [EB973B565B7 — GPU Performance Background User’s Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-gpu-background/index.html) · `page_reviewed` · [local note](../research/sources/EB973B565B7.md)
- [E134D3535CB — Matrix Multiplication Background User’s Guide](https://docs.nvidia.com/deeplearning/performance/dl-performance-matrix-multiplication/index.html) · `page_reviewed` · [local note](../research/sources/E134D3535CB.md)
- [E4ABDC02D45 — NVIDIA DGX SuperPOD — Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html) · `page_reviewed` · [local note](../research/sources/E4ABDC02D45.md)

<a id="d08"></a>

### D08 — Networking and interconnects

**Central question:** How do many devices make progress as one system?

Teach communication cost and topology as constraints on useful compute and physical deployment.

**Included scope:**

- Scale-up, scale-out and inter-data-center networking
- Latency, bandwidth, bisection capacity, oversubscription and congestion
- Collectives, routing and workload placement
- Ethernet and InfiniBand as architectures with implementation-specific behavior
- Copper, pluggable optics and co-packaged optics; reach, power, cabling and serviceability

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D02 — Workloads and the infrastructure brief](#d02), [D07 — Compute, memory and the rack](#d07)

**Learning objectives and assessments:**

#### D08.1

Distinguish scale-up, scale-out and wide-area communication requirements.

**Assessment:** Place three communication patterns on a rack, cluster and regional map and identify the relevant bottleneck.

**Existing baseline:** missing. No existing lesson mapped.

#### D08.2

Calculate an illustrative topology's endpoint ports, oversubscription and transfer-time lower bounds.

**Assessment:** Compare two small supplied topologies, including units and stated routing assumptions; identify why bandwidth alone does not predict application time.

**Existing baseline:** missing. No existing lesson mapped.

#### D08.3

Explain how congestion, collectives and topology-aware placement affect job progress.

**Assessment:** Predict the effect of a constrained link during a collective and describe a placement or architecture alternative.

**Existing baseline:** missing. No existing lesson mapped.

#### D08.4

Compare interconnect media and packaging choices using reach, bandwidth, power, cooling and replacement boundaries.

**Assessment:** Evaluate copper, pluggable optics and a specified CPO proposal for a declared use case without treating a roadmap as a deployed default.

**Existing baseline:** missing. No existing lesson mapped.

#### D08.5

Trace a network failure or degraded link into workload, cabling and operational consequences.

**Assessment:** Explain why a powered and cooled cluster can miss its useful-throughput acceptance target after a partial fabric failure.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Watch a collective cross the fabric**

- Prediction: Does doubling a single link's bandwidth halve the whole job time?
- Interaction: Advance a small collective step by step; change topology, oversubscription or a failed link and compare work/wait timelines.
- Model boundary: A simplified communication model is not a benchmark. Keep routing, concurrency, protocol overhead and failure assumptions visible.

**Worked example:** Calculate ports and idealized transfer bounds for a small fabric, then add explicitly modeled communication phases to a job timeline.

**Design tradeoff:** Bandwidth density, reach, power and serviceability pull in different directions; network selection depends on workload and operating capability.

**Failure or maintenance scenario:** A partial fabric degradation increases job waiting while aggregate device health appears normal.

**Research connections:**

- [SA03 — 100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) · `public_excerpt_reviewed` · [local note](../research/sources/SA03.md)
- [SA04 — Multi-Datacenter Training: OpenAI’s Ambitious Plan To Beat Google’s Infrastructure](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) · `public_excerpt_reviewed` · [local note](../research/sources/SA04.md)
- [SA05 — AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) · `public_excerpt_reviewed` · [local note](../research/sources/SA05.md)
- [SA06 — Co-Packaged Optics (CPO) Book – Scaling with Light for the Next Wave of Interconnect](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling) · `public_excerpt_reviewed` · [local note](../research/sources/SA06.md)
- [SA08 — ClusterMAX™ 2.0: The Industry Standard GPU Cloud Rating System](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) · `public_excerpt_reviewed` · [local note](../research/sources/SA08.md)
- [P08 — Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) · `page_reviewed` · [local note](../research/sources/P08.md)
- [P09 — The Datacenter as a Computer: designing warehouse-scale machines](https://research.google/pubs/the-datacenter-as-a-computer-designing-warehouse-scale-machines/) · `public_excerpt_reviewed` · [local note](../research/sources/P09.md)
- [SA13 — Nvidia’s Optical Boogeyman – NVL72, Infiniband Scale Out, 800G & 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) · `public_excerpt_reviewed` · [local note](../research/sources/SA13.md)
- [SA15 — The New AI Networks | Ultra Ethernet UEC | UALink vs Broadcom Scale Up Ethernet SUE](https://newsletter.semianalysis.com/p/the-new-ai-networks-ultra-ethernet-uec-ualink-vs-broadcom-scale-up-ethernet-sue) · `public_excerpt_reviewed` · [local note](../research/sources/SA15.md)
- [SA16 — Google OCS Apollo: The &gt;$3 Billion Game-Changer in Datacenter Networking](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game) · `public_excerpt_reviewed` · [local note](../research/sources/SA16.md)
- [SA19 — GB200 Hardware Architecture - Component Supply Chain & BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) · `public_excerpt_reviewed` · [local note](../research/sources/SA19.md)
- [SA24 — Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) · `public_excerpt_reviewed` · [local note](../research/sources/SA24.md)
- [SA25 — TPUv7: Google Takes a Swing at the King](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA25.md)
- [SA26 — AWS Trainium3 Deep Dive | A Potential Challenger Approaching](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential) · `public_excerpt_reviewed` · [local note](../research/sources/SA26.md)
- [SA40 — Google AI Infrastructure Supremacy: Systems Matter More Than Microarchitecture](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy) · `public_excerpt_reviewed` · [local note](../research/sources/SA40.md)
- [P13 — Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) · `page_reviewed` · [local note](../research/sources/P13.md)
- [P14 — NVIDIA DGX SuperPOD: Next Generation Scalable Infrastructure for AI Leadership Reference Architecture Featuring NVIDIA DGX H100](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/) · `page_reviewed` · [local note](../research/sources/P14.md)
- [P17 — NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) · `page_reviewed` · [local note](../research/sources/P17.md)
- [E4ABDC02D45 — NVIDIA DGX SuperPOD — Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html) · `page_reviewed` · [local note](../research/sources/E4ABDC02D45.md)
- [EB0CA366091 — NCCL Collective Operations](https://docs.nvidia.com/deeplearning/nccl/user-guide/docs/usage/collectives.html) · `page_reviewed` · [local note](../research/sources/EB0CA366091.md)
- [E80C73CE756 — Scaling AI Factories with Co-Packaged Optics for Better Power Efficiency](https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/) · `page_reviewed` · [local note](../research/sources/E80C73CE756.md)
- [E9ACF1B58FE — NVIDIA Optical Transceivers and Cables](https://www.nvidia.com/en-us/networking/interconnect/) · `page_reviewed` · [local note](../research/sources/E9ACF1B58FE.md)

<a id="d09"></a>

### D09 — Storage, orchestration and recovery

**Central question:** Can data and jobs reach the hardware, and can useful progress survive failures?

Connect storage and cluster software to the delivery of a usable service.

**Included scope:**

- Local, shared and object storage roles; bandwidth, latency, metadata and durability
- Dataset ingestion, checkpointing and restart paths
- Scheduling, topology-aware placement and resource isolation
- Cluster bring-up, provisioning, observability and tenant/service acceptance
- Recovery objectives, redundancy and backup as different concepts

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D02 — Workloads and the infrastructure brief](#d02), [D07 — Compute, memory and the rack](#d07), [D08 — Networking and interconnects](#d08)

**Learning objectives and assessments:**

#### D09.1

Trace the dataset and checkpoint paths and distinguish capacity, throughput and metadata constraints.

**Assessment:** Calculate an idealized checkpoint transfer time from supplied sizes and effective bandwidth, then identify additional bottlenecks.

**Existing baseline:** missing. No existing lesson mapped.

#### D09.2

Explain how checkpoint frequency, failure behavior and restart time affect completed work.

**Assessment:** Compare two explicit checkpoint policies on a synthetic timeline that includes a failure and recovery.

**Existing baseline:** missing. No existing lesson mapped.

#### D09.3

Explain scheduling, placement, provisioning and isolation as prerequisites for usable cluster capacity.

**Assessment:** Diagnose a scenario in which hardware is healthy but jobs cannot obtain the required topology, software environment or storage access.

**Existing baseline:** missing. No existing lesson mapped.

#### D09.4

Specify a service acceptance exercise that tests end-to-end data access, job launch, useful output and recovery.

**Assessment:** Write a reproducible test plan for a synthetic tenant without reducing acceptance to a device-count or power-on check.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Progress survives—or starts again**

- Prediction: Can a faster checkpoint policy consume enough resources to slow normal progress?
- Interaction: Run the same job with two checkpoint/restart policies; show useful work, storage traffic, saved state and lost progress.
- Model boundary: Do not assume independent failures or constant restart time without labeling them; RAID/replication and backup are distinct.

**Worked example:** Reconcile checkpoint size, sustained storage throughput and recovery time for a provided scenario; account separately for lost and recomputed work.

**Design tradeoff:** More frequent checkpoints can reduce lost progress but consume storage, network and execution resources.

**Failure or maintenance scenario:** A storage or orchestration failure makes otherwise available GPUs unusable or prevents a clean restart.

**Research connections:**

- [SA03 — 100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) · `public_excerpt_reviewed` · [local note](../research/sources/SA03.md)
- [SA04 — Multi-Datacenter Training: OpenAI’s Ambitious Plan To Beat Google’s Infrastructure](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) · `public_excerpt_reviewed` · [local note](../research/sources/SA04.md)
- [SA05 — AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) · `public_excerpt_reviewed` · [local note](../research/sources/SA05.md)
- [SA08 — ClusterMAX™ 2.0: The Industry Standard GPU Cloud Rating System](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) · `public_excerpt_reviewed` · [local note](../research/sources/SA08.md)
- [SA09 — How Much Do GPU Clusters Really Cost?](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost) · `public_excerpt_reviewed` · [local note](../research/sources/SA09.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P08 — Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) · `page_reviewed` · [local note](../research/sources/P08.md)
- [P09 — The Datacenter as a Computer: designing warehouse-scale machines](https://research.google/pubs/the-datacenter-as-a-computer-designing-warehouse-scale-machines/) · `public_excerpt_reviewed` · [local note](../research/sources/P09.md)
- [SA15 — The New AI Networks | Ultra Ethernet UEC | UALink vs Broadcom Scale Up Ethernet SUE](https://newsletter.semianalysis.com/p/the-new-ai-networks-ultra-ethernet-uec-ualink-vs-broadcom-scale-up-ethernet-sue) · `public_excerpt_reviewed` · [local note](../research/sources/SA15.md)
- [SA18 — GPU Cloud Economics Explained – The Hidden Truth](https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA18.md)
- [SA20 — H100 vs GB200 NVL72 Training Benchmarks - Power, TCO, and Reliability Analysis, Software Improvement Over Time](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks) · `public_excerpt_reviewed` · [local note](../research/sources/SA20.md)
- [SA22 — Scaling the Memory Wall: The Rise and Roadmap of HBM](https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm) · `public_excerpt_reviewed` · [local note](../research/sources/SA22.md)
- [SA23 — CPUs are Back: The Datacenter CPU Landscape in 2026](https://newsletter.semianalysis.com/p/cpus-are-back-the-datacenter-cpu) · `public_excerpt_reviewed` · [local note](../research/sources/SA23.md)
- [SA25 — TPUv7: Google Takes a Swing at the King](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA25.md)
- [SA26 — AWS Trainium3 Deep Dive | A Potential Challenger Approaching](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential) · `public_excerpt_reviewed` · [local note](../research/sources/SA26.md)
- [SA27 — RL Systems Mind the Gap: Matching Trainer and Generator Throughput](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching) · `public_excerpt_reviewed` · [local note](../research/sources/SA27.md)
- [SA28 — Most Neoclouds Suck At Security](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security) · `public_excerpt_reviewed` · [local note](../research/sources/SA28.md)
- [SA38 — How Oracle Is Winning the AI Compute Market](https://newsletter.semianalysis.com/p/how-oracle-is-winning-the-ai-compute-market) · `public_excerpt_reviewed` · [local note](../research/sources/SA38.md)
- [SA40 — Google AI Infrastructure Supremacy: Systems Matter More Than Microarchitecture](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy) · `public_excerpt_reviewed` · [local note](../research/sources/SA40.md)
- [P13 — Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) · `page_reviewed` · [local note](../research/sources/P13.md)
- [P14 — NVIDIA DGX SuperPOD: Next Generation Scalable Infrastructure for AI Leadership Reference Architecture Featuring NVIDIA DGX H100](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/) · `page_reviewed` · [local note](../research/sources/P14.md)
- [P17 — NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) · `page_reviewed` · [local note](../research/sources/P17.md)
- [E4D40417934 — NVIDIA DGX SuperPOD — Storage Architecture](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/storage-architecture.html) · `page_reviewed` · [local note](../research/sources/E4D40417934.md)
- [E284D853C6B — PyTorch Distributed Checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html) · `public_excerpt_reviewed` · [local note](../research/sources/E284D853C6B.md)
- [E2E0C218DA7 — Asynchronous Saving with Distributed Checkpoint](https://docs.pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html) · `page_reviewed` · [local note](../research/sources/E2E0C218DA7.md)
- [EE0FC346C72 — Control Group in Slurm](https://slurm.schedmd.com/cgroups.html) · `page_reviewed` · [local note](../research/sources/EE0FC346C72.md)
- [E0CDE775C43 — NVIDIA DGX SuperPOD — Software](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/dgx-software.html) · `page_reviewed` · [local note](../research/sources/E0CDE775C43.md)

<a id="d10"></a>

### D10 — Chip and rack heat capture

**Central question:** How does heat leave the devices without exceeding their operating limits?

Connect local thermal constraints with airflow, coolant and rack interfaces.

**Included scope:**

- Heat generation, heat flux, thermal resistance and temperature limits
- Heat sinks, cold plates, rear-door exchangers, immersion and two-phase alternatives
- Residual air paths and containment
- Technology coolant, manifolds, quick disconnects and CDUs
- Flow, pressure drop, approach temperature, material compatibility and leak management

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D07 — Compute, memory and the rack](#d07)

**Learning objectives and assessments:**

#### D10.1

Trace parallel air and liquid heat paths and explain why rack power alone does not specify local cooling difficulty.

**Assessment:** Compare two hypothetical devices with the same total heat but different heat flux or thermal resistance.

**Existing baseline:** partial. `electrical-to-heat` — The watt becomes heat.; `residual-air` — This rack still needs air.

#### D10.2

Calculate a single-phase heat-transport flow under stated fluid and temperature assumptions.

**Assessment:** Solve a heat/flow/temperature-rise example and explain why the result alone does not select a pump or cold plate.

**Existing baseline:** partial. `liquid-heat-transport` — Heat needs a moving carrier.

#### D10.3

Explain a CDU's fluid separation, heat-exchange and control functions while distinguishing loop rise from approach temperature.

**Assessment:** Draw two closed loops, label their temperature points and predict the effect of a constrained heat-exchanger interface.

**Existing baseline:** partial. `heat-exchanger` — Heat crosses. Fluids stay apart.

#### D10.4

Compare air, cold-plate, rear-door and immersion approaches against a declared density and service brief.

**Assessment:** Evaluate a synthetic retrofit with residual-air, fluid, pressure, access and maintenance requirements; identify missing compatibility evidence.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Two fluids, one heat transfer**

- Prediction: Does increasing loop temperature rise imply the same change in heat-exchanger approach temperature?
- Interaction: Follow heat from die through parallel air/liquid routes; vary flow and supply temperature within a declared model.
- Model boundary: Fluid properties and operating limits must be specified. Flow arithmetic is not a hydraulic or equipment selection model.

**Worked example:** Calculate water flow for a declared steady heat load, then examine a supplied pressure-drop curve and a separate heat-exchanger approach constraint.

**Design tradeoff:** Capturing heat closer to its source can support density while changing plumbing, materials, controls and service procedures.

**Failure or maintenance scenario:** A blocked branch or failed pump creates a local thermal limit that a facility-wide MW heat balance cannot reveal.

**Research connections:**

- [SA02 — Datacenter Anatomy Part 2 – Cooling Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems) · `public_excerpt_reviewed` · [local note](../research/sources/SA02.md)
- [P01 — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) · `page_reviewed` · [local note](../research/sources/P01.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P04 — Tier Classification System](https://uptimeinstitute.com/tiers) · `page_reviewed` · [local note](../research/sources/P04.md)
- [P06 — Open Rack/SpecsAndDesigns](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) · `page_reviewed` · [local note](../research/sources/P06.md)
- [P07 — ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) · `page_reviewed` · [local note](../research/sources/P07.md)
- [P10 — Incorporate Minimum Efficiency Requirements for Heating and Cooling Products into Federal Acquisition Documents](https://www.energy.gov/cmei/femp/incorporate-minimum-efficiency-requirements-heating-and-cooling-products-federal) · `page_reviewed` · [local note](../research/sources/P10.md)
- [SA14 — AI Datacenter Energy Dilemma - Race for AI Datacenter Space](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race) · `public_excerpt_reviewed` · [local note](../research/sources/SA14.md)
- [SA17 — Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition) · `public_excerpt_reviewed` · [local note](../research/sources/SA17.md)
- [SA19 — GB200 Hardware Architecture - Component Supply Chain & BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) · `public_excerpt_reviewed` · [local note](../research/sources/SA19.md)
- [SA24 — Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) · `public_excerpt_reviewed` · [local note](../research/sources/SA24.md)
- [SA29 — The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) · `public_excerpt_reviewed` · [local note](../research/sources/SA29.md)
- [SA37 — xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA37.md)
- [P15 — Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) · `public_excerpt_reviewed` · [local note](../research/sources/P15.md)
- [P17 — NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) · `page_reviewed` · [local note](../research/sources/P17.md)
- [E709C9E5196 — ASHRAE — Emergence and Expansion of Liquid Cooling in Mainstream Data Centers](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf) · `page_reviewed` · [local note](../research/sources/E709C9E5196.md)
- [EE136EB8E02 — Open Compute Project — Cold Plate workstream](https://www.opencompute.org/wiki/Cooling_Environments/Cold_Plate) · `public_excerpt_reviewed` · [local note](../research/sources/EE136EB8E02.md)

<a id="d11"></a>

### D11 — Heat rejection, climate and water

**Central question:** Where does the heat finally go, and what does moving it consume?

Close the energy and water balances through facility cooling and the outdoor environment.

**Included scope:**

- Facility water loops, pumps, air handlers and thermal storage
- Dry coolers, chillers, towers and economizers as distinct systems
- Refrigeration, COP, load dependence and added compressor heat
- Dry-bulb/wet-bulb conditions, water supply, treatment and consumption
- PUE/WUE boundaries, heat reuse and environmental tradeoffs

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D10 — Chip and rack heat capture](#d10)

**Learning objectives and assessments:**

#### D11.1

Distinguish dry cooling, refrigeration, evaporative rejection and economizer operating modes.

**Assessment:** Trace four reference heat paths and identify where electricity and water enter each.

**Existing baseline:** partial. `outdoor-rejection` — Moving heat adds heat.

#### D11.2

Close a declared chiller energy balance and calculate cooling COP with the correct numerator and denominator.

**Assessment:** Given cooling duty and compressor input, calculate COP and condenser heat; place pumps and fans at their stated boundaries.

**Existing baseline:** partial. `outdoor-rejection` — Moving heat adds heat.

#### D11.3

Explain how ambient conditions, supply temperatures and equipment performance constrain capacity and economizer operation.

**Assessment:** Use supplied equipment curves and weather bins to compare two operating modes without applying a universal free-cooling threshold.

**Existing baseline:** missing. No existing lesson mapped.

#### D11.4

Compute energy and water metrics with explicit boundaries and distinguish consumption from withdrawal.

**Assessment:** Compare two scenarios over the same period using stated facility/IT energies and water accounting; explain what PUE and WUE omit.

**Existing baseline:** partial. `facility-overhead` — Budget the whole facility.

#### D11.5

Evaluate cooling architecture or heat reuse against climate, water, electrical capacity and receiving-load constraints.

**Assessment:** Compare a hot-weather and a water-constrained site using a supplied design brief; identify what changes the preferred choice.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: The heat balance meets the weather**

- Prediction: Under a fixed site electrical limit, can hotter weather constrain IT twice: through cooling capacity and auxiliary demand?
- Interaction: Sweep a labeled ambient condition through supplied performance curves; watch available cooling, plant power and water use together.
- Model boundary: COP and equipment curves need rating conditions. Water use depends on system and accounting boundary, not the label liquid cooling.

**Worked example:** Use a synthetic chiller performance table and hourly weather bins to estimate cooling electricity; keep the separate water model's assumptions explicit.

**Design tradeoff:** Temperature, water, energy, space and heat-reuse opportunities create site-specific choices rather than a universal best cooling system.

**Failure or maintenance scenario:** A heatwave or water restriction invalidates a nominal cooling rating used in the electrical capacity plan.

**Research connections:**

- [SA02 — Datacenter Anatomy Part 2 – Cooling Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems) · `public_excerpt_reviewed` · [local note](../research/sources/SA02.md)
- [P01 — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) · `page_reviewed` · [local note](../research/sources/P01.md)
- [P07 — ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) · `page_reviewed` · [local note](../research/sources/P07.md)
- [P10 — Incorporate Minimum Efficiency Requirements for Heating and Cooling Products into Federal Acquisition Documents](https://www.energy.gov/cmei/femp/incorporate-minimum-efficiency-requirements-heating-and-cooling-products-federal) · `page_reviewed` · [local note](../research/sources/P10.md)
- [SA12 — How AI Labs Are Solving the Power Crisis: The Onsite Gas Deep Dive](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power) · `public_excerpt_reviewed` · [local note](../research/sources/SA12.md)
- [SA31 — From Tokens to Burgers: A Water Footprint Face-Off](https://newsletter.semianalysis.com/p/from-tokens-to-burgers-a-water-footprint) · `public_excerpt_reviewed` · [local note](../research/sources/SA31.md)
- [P15 — Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) · `public_excerpt_reviewed` · [local note](../research/sources/P15.md)
- [E89E077D5C1 — DOE FEMP: Cooling Tower Management](https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management) · `page_reviewed` · [local note](../research/sources/E89E077D5C1.md)
- [E6DF2655A78 — USGS National Water Availability Assessment Data Companion](https://waterdata.usgs.gov/blog/nwdc-overview/) · `page_reviewed` · [local note](../research/sources/E6DF2655A78.md)

<a id="d12"></a>

### D12 — Physical site, buildings and safety

**Central question:** What must the actual place support beyond electrical and thermal ratings?

Make spatial, environmental, access and safety constraints visible before treating a schematic as buildable.

**Included scope:**

- Land, geotechnical and civil interfaces; buildings, structural loading and floor layouts
- Flood, seismic, weather and other site hazards as jurisdiction-specific inputs
- Equipment access, lifting, replacement routes, egress and service clearances
- Fire detection/suppression, electrical hazards and battery/fuel arrangements at conceptual level
- Physical security and OT/IT trust boundaries; noise, water and environmental permits

**Prerequisites:** [D01 — System boundaries and quantities](#d01), [D03 — Siting, grid connection and supply](#d03)

**Learning objectives and assessments:**

#### D12.1

Translate a reference equipment layout into space, weight, access and replacement-route requirements.

**Assessment:** Reject a synthetic rack/plant layout that fits in area but fails a supplied loading or service-access constraint.

**Existing baseline:** missing. No existing lesson mapped.

#### D12.2

Identify site hazards and permitting interfaces that require location-specific evidence.

**Assessment:** Build a siting risk register for two hypothetical locations and distinguish generic questions from verified local requirements.

**Existing baseline:** missing. No existing lesson mapped.

#### D12.3

Explain how fire, electrical, fluid and stored-energy hazards influence layout and operating boundaries.

**Assessment:** Annotate a conceptual layout with required specialist reviews and separation/access questions without presenting it as a compliant design.

**Existing baseline:** missing. No existing lesson mapped.

#### D12.4

Trace physical and control-system access boundaries and explain why availability depends on controlled changes and access.

**Assessment:** Identify a shared access or control dependency in a supplied facility/tenant interface diagram.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: The schematic has to fit somewhere**

- Prediction: Can a higher-density rack reduce rack count while making the existing building harder to use?
- Interaction: Switch a hall between normal operation, equipment replacement and emergency-access views; reveal footprints and clearance envelopes.
- Model boundary: Illustrative envelopes are not code-compliant dimensions. Applicable requirements depend on jurisdiction, equipment and design review.

**Worked example:** Fit a hypothetical rack and replacement route into a supplied floor plan using declared dimensions and structural limits.

**Design tradeoff:** Density and compactness must be weighed against access, hazard separation, replacement logistics and expansion space.

**Failure or maintenance scenario:** A component cannot be replaced while maintaining the planned service path, despite adequate spare electrical capacity.

**Research connections:**

- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P06 — Open Rack/SpecsAndDesigns](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) · `page_reviewed` · [local note](../research/sources/P06.md)
- [P07 — ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) · `page_reviewed` · [local note](../research/sources/P07.md)
- [P11 — NFPA 75: Standard for the Fire Protection of Information Technology Equipment](https://www.nfpa.org/codes-and-standards/nfpa-75-standard-development/75) · `candidate_not_reviewed` · [local note](../research/sources/P11.md)
- [SA29 — The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) · `public_excerpt_reviewed` · [local note](../research/sources/SA29.md)
- [P16 — Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) · `page_reviewed` · [local note](../research/sources/P16.md)
- [EDDF63EA993 — NVIDIA H100 SuperPOD: White Space Infrastructure](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/infrastructure.html) · `page_reviewed` · [local note](../research/sources/EDDF63EA993.md)
- [E320A75F233 — NVIDIA H100 SuperPOD: Planning a Data Center Deployment](https://docs.nvidia.com/dgx-superpod/design-guides/dgx-superpod-data-center-design-h100/latest/planning.html) · `page_reviewed` · [local note](../research/sources/E320A75F233.md)
- [E2848C36FE7 — National Weather Service: Flood Related Hazards](https://www.weather.gov/safety/flood-hazards) · `page_reviewed` · [local note](../research/sources/E2848C36FE7.md)
- [E95181BB427 — USGS: What is seismic hazard?](https://www.usgs.gov/faqs/what-seismic-hazard-what-a-seismic-hazard-map-and-how-are-they-used) · `page_reviewed` · [local note](../research/sources/E95181BB427.md)
- [E013A66FA9A — NIST SP 800-82 Revision 3: OT Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final) · `public_excerpt_reviewed` · [local note](../research/sources/E013A66FA9A.md)
- [EDEEDB16DDE — OSHA 1910.333: Electrical work practices](https://www.osha.gov/laws-regs/regulations/standardnumber/1910/1910.333) · `public_excerpt_reviewed` · [local note](../research/sources/EDEEDB16DDE.md)

<a id="d13"></a>

### D13 — Design, procurement and commissioning

**Central question:** How does a design become a tested, usable service?

Teach delivery as a chain of interfaces and evidence, not a chronology of announcements.

**Included scope:**

- Requirements, design basis, interface ownership and change control
- Equipment lead times, factory testing, logistics and sequencing
- Construction, installation quality, fluid cleanliness and pre-functional checks
- Functional and integrated systems testing, failure scenarios and acceptance
- Phased handover, as-built records, procedures and operator training

**Prerequisites:** [D03 — Siting, grid connection and supply](#d03), [D04 — Campus and building power distribution](#d04), [D05 — Continuity, storage and protection](#d05), [D09 — Storage, orchestration and recovery](#d09), [D10 — Chip and rack heat capture](#d10), [D11 — Heat rejection, climate and water](#d11), [D12 — Physical site, buildings and safety](#d12)

**Learning objectives and assessments:**

#### D13.1

Build a dependency-based delivery plan and distinguish a critical path from the longest equipment lead time.

**Assessment:** Sequence a synthetic project with parallel procurement, utility work, installation and testing; identify which delay changes service availability.

**Existing baseline:** missing. No existing lesson mapped.

#### D13.2

Track interface requirements across vendors and design changes.

**Assessment:** Diagnose a rack/CDU or power/control interface mismatch before equipment shipment and state the acceptance evidence required.

**Existing baseline:** missing. No existing lesson mapped.

#### D13.3

Distinguish installed, energized, individually tested, integrated-tested and service-accepted states.

**Assessment:** Classify supplied milestone evidence and identify which complete electrical, thermal and information paths remain unproven.

**Existing baseline:** partial. `capacity-stages` — Connected is a milestone.; `abilene-case` — Read a real headline precisely.

#### D13.4

Specify an integrated acceptance and handover plan for a phased deployment.

**Assessment:** Propose normal, failure, maintenance and recovery tests, instrumentation, acceptance criteria, records and operator handover for a synthetic phase.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Only complete paths count**

- Prediction: Can the utility milestone be complete while the usable-capacity milestone remains unchanged?
- Interaction: Advance independent delivery milestones across power, cooling, network and controls; reveal when a complete tested service path exists.
- Model boundary: Testing requirements and acceptance conditions must be tied to a project brief. Timeline bars do not prove operating status.

**Worked example:** Find the earliest service-ready date in a supplied dependency graph, then recalculate after a converter or cooling-control delivery delay.

**Design tradeoff:** Standardization and early ordering can accelerate delivery while limiting later changes; phased openings add interface and acceptance complexity.

**Failure or maintenance scenario:** Individually successful subsystem tests miss a coupled failure during an integrated utility-loss test.

**Research connections:**

- [SA01 — Datacenter Anatomy Part 1: Electrical Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical) · `public_excerpt_reviewed` · [local note](../research/sources/SA01.md)
- [SA05 — AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) · `public_excerpt_reviewed` · [local note](../research/sources/SA05.md)
- [SA07 — US Grid Constraints: Towards 40GW+ of Behind-The-Meter Datacenter by 2028?](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw) · `public_excerpt_reviewed` · [local note](../research/sources/SA07.md)
- [SA10 — Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) · `public_excerpt_reviewed` · [local note](../research/sources/SA10.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P03 — Management and Operations Guideline](https://uptimeinstitute.com/professional-services/management-operations/mando-criteria) · `page_reviewed` · [local note](../research/sources/P03.md)
- [P04 — Tier Classification System](https://uptimeinstitute.com/tiers) · `page_reviewed` · [local note](../research/sources/P04.md)
- [P11 — NFPA 75: Standard for the Fire Protection of Information Technology Equipment](https://www.nfpa.org/codes-and-standards/nfpa-75-standard-development/75) · `candidate_not_reviewed` · [local note](../research/sources/P11.md)
- [P12 — Large Loads Action Plan](https://www.nerc.com/initiatives/large-loads-action-plan) · `public_excerpt_reviewed` · [local note](../research/sources/P12.md)
- [SA12 — How AI Labs Are Solving the Power Crisis: The Onsite Gas Deep Dive](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power) · `public_excerpt_reviewed` · [local note](../research/sources/SA12.md)
- [SA14 — AI Datacenter Energy Dilemma - Race for AI Datacenter Space](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race) · `public_excerpt_reviewed` · [local note](../research/sources/SA14.md)
- [SA19 — GB200 Hardware Architecture - Component Supply Chain & BOM](https://newsletter.semianalysis.com/p/gb200-hardware-architecture-and-component) · `public_excerpt_reviewed` · [local note](../research/sources/SA19.md)
- [SA24 — Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) · `public_excerpt_reviewed` · [local note](../research/sources/SA24.md)
- [SA29 — The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) · `public_excerpt_reviewed` · [local note](../research/sources/SA29.md)
- [SA30 — Meta’s Infrastructure Team Needs A Culture Reset](https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a) · `public_excerpt_reviewed` · [local note](../research/sources/SA30.md)
- [SA33 — Stop Saying Half of 2026 US Datacenter Capacity Is Canceled](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA33.md)
- [SA35 — Nvidia GPU Debt Backstop Unleashes the AI Project Trinity: Capital, Offtake and Datacenters](https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes) · `public_excerpt_reviewed` · [local note](../research/sources/SA35.md)
- [SA36 — Microsoft's AI Strategy Deconstructed - From Energy to Tokens](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed) · `public_excerpt_reviewed` · [local note](../research/sources/SA36.md)
- [SA37 — xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA37.md)
- [SA38 — How Oracle Is Winning the AI Compute Market](https://newsletter.semianalysis.com/p/how-oracle-is-winning-the-ai-compute-market) · `public_excerpt_reviewed` · [local note](../research/sources/SA38.md)
- [SA39 — OpenAI Stargate Joint Venture Demystified | Microsoft Sore Loser, Does Softbank Have The Capital?, Texas GigaCampus, Winners & Losers](https://newsletter.semianalysis.com/p/openai-stargate-joint-venture-demystified) · `public_excerpt_reviewed` · [local note](../research/sources/SA39.md)
- [P14 — NVIDIA DGX SuperPOD: Next Generation Scalable Infrastructure for AI Leadership Reference Architecture Featuring NVIDIA DGX H100](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/) · `page_reviewed` · [local note](../research/sources/P14.md)
- [P15 — Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) · `public_excerpt_reviewed` · [local note](../research/sources/P15.md)
- [P16 — Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) · `page_reviewed` · [local note](../research/sources/P16.md)
- [E50E0F856B0 — GAO Schedule Assessment Guide](https://www.gao.gov/products/gao-16-89g) · `page_reviewed` · [local note](../research/sources/E50E0F856B0.md)
- [ECB7071035F — WBDG: Commissioning Documents](https://legacy.wbdg.org/building-commissioning/commissioning-documents) · `page_reviewed` · [local note](../research/sources/ECB7071035F.md)

<a id="d14"></a>

### D14 — Controls, operations and reliability

**Central question:** How does the system remain within its limits after handover?

Turn the static design into monitored operation, maintenance and incident recovery.

**Included scope:**

- Electrical, building, cooling and cluster monitoring; meters, sensors and control loops
- Setpoints, sequences, alarms, telemetry quality and control dependencies
- Maintenance, procedures, staffing, change/configuration management and spares
- Failure domains, common causes, service availability and incident learning
- Workload load changes, capacity management, aging and retrofit operations

**Prerequisites:** [D05 — Continuity, storage and protection](#d05), [D09 — Storage, orchestration and recovery](#d09), [D11 — Heat rejection, climate and water](#d11), [D12 — Physical site, buildings and safety](#d12), [D13 — Design, procurement and commissioning](#d13)

**Learning objectives and assessments:**

#### D14.1

Place sensors and meters so an operator can distinguish an actual constraint from missing or misleading telemetry.

**Assessment:** Diagnose a synthetic thermal alarm using a labeled trend set; state where additional measurements are needed.

**Existing baseline:** missing. No existing lesson mapped.

#### D14.2

Explain the difference between a device controller, a facility sequence and workload scheduling.

**Assessment:** Trace a supplied setpoint or load change through these layers and identify the required coordination and limits.

**Existing baseline:** missing. No existing lesson mapped.

#### D14.3

Evaluate maintainability using a procedure, surviving capacity and real isolation boundaries.

**Assessment:** Walk through a synthetic maintenance plan and identify the shared dependency or restoration step that threatens service.

**Existing baseline:** partial. `redundant-paths` — A second path must be useful.; `fault-domains` — Keep one fault from spreading.

#### D14.4

Distinguish component reliability, topology claims and measured service availability.

**Assessment:** Critique a naive multiplication of component availabilities and specify which correlated failures and repair assumptions are missing.

**Existing baseline:** missing. No existing lesson mapped.

#### D14.5

Convert a failure or capacity incident into an evidence-based recovery and prevention plan.

**Assessment:** Reconstruct a supplied incident timeline, separate observations from hypotheses, and propose a verification step for each corrective action.

**Existing baseline:** missing. No existing lesson mapped.

**Visual plan: Operate the same campus**

- Prediction: Which alarm is a symptom, and what observation would discriminate between two plausible causes?
- Interaction: Move from topology to aligned telemetry and an incident timeline; select a maintenance action or workload change and trace dependencies.
- Model boundary: Synthetic telemetry is labeled. A simplified control model cannot establish stability, safety or field performance.

**Worked example:** Use a synthetic availability and incident log to calculate service downtime and identify the difference between equipment uptime and completed work.

**Design tradeoff:** Aggressive utilization or efficiency setpoints may reduce margin; the operational choice depends on measured behavior and service requirements.

**Failure or maintenance scenario:** A shared control or configuration change disables nominally independent equipment paths.

**Research connections:**

- [SA03 — 100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing](https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network) · `public_excerpt_reviewed` · [local note](../research/sources/SA03.md)
- [SA05 — AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) · `public_excerpt_reviewed` · [local note](../research/sources/SA05.md)
- [SA06 — Co-Packaged Optics (CPO) Book – Scaling with Light for the Next Wave of Interconnect](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling) · `public_excerpt_reviewed` · [local note](../research/sources/SA06.md)
- [SA08 — ClusterMAX™ 2.0: The Industry Standard GPU Cloud Rating System](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) · `public_excerpt_reviewed` · [local note](../research/sources/SA08.md)
- [SA09 — How Much Do GPU Clusters Really Cost?](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost) · `public_excerpt_reviewed` · [local note](../research/sources/SA09.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P03 — Management and Operations Guideline](https://uptimeinstitute.com/professional-services/management-operations/mando-criteria) · `page_reviewed` · [local note](../research/sources/P03.md)
- [P04 — Tier Classification System](https://uptimeinstitute.com/tiers) · `page_reviewed` · [local note](../research/sources/P04.md)
- [P07 — ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) · `page_reviewed` · [local note](../research/sources/P07.md)
- [P08 — Building Meta’s GenAI Infrastructure](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/) · `page_reviewed` · [local note](../research/sources/P08.md)
- [P09 — The Datacenter as a Computer: designing warehouse-scale machines](https://research.google/pubs/the-datacenter-as-a-computer-designing-warehouse-scale-machines/) · `public_excerpt_reviewed` · [local note](../research/sources/P09.md)
- [P12 — Large Loads Action Plan](https://www.nerc.com/initiatives/large-loads-action-plan) · `public_excerpt_reviewed` · [local note](../research/sources/P12.md)
- [SA11 — AI Training Load Fluctuations at Gigawatt-scale - Risk of Power Grid Blackout?](https://newsletter.semianalysis.com/p/ai-training-load-fluctuations-at-gigawatt-scale-risk-of-power-grid-blackout) · `public_excerpt_reviewed` · [local note](../research/sources/SA11.md)
- [SA15 — The New AI Networks | Ultra Ethernet UEC | UALink vs Broadcom Scale Up Ethernet SUE](https://newsletter.semianalysis.com/p/the-new-ai-networks-ultra-ethernet-uec-ualink-vs-broadcom-scale-up-ethernet-sue) · `public_excerpt_reviewed` · [local note](../research/sources/SA15.md)
- [SA16 — Google OCS Apollo: The &gt;$3 Billion Game-Changer in Datacenter Networking](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game) · `public_excerpt_reviewed` · [local note](../research/sources/SA16.md)
- [SA18 — GPU Cloud Economics Explained – The Hidden Truth](https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA18.md)
- [SA20 — H100 vs GB200 NVL72 Training Benchmarks - Power, TCO, and Reliability Analysis, Software Improvement Over Time](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks) · `public_excerpt_reviewed` · [local note](../research/sources/SA20.md)
- [SA27 — RL Systems Mind the Gap: Matching Trainer and Generator Throughput](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching) · `public_excerpt_reviewed` · [local note](../research/sources/SA27.md)
- [SA28 — Most Neoclouds Suck At Security](https://newsletter.semianalysis.com/p/most-neoclouds-suck-at-security) · `public_excerpt_reviewed` · [local note](../research/sources/SA28.md)
- [SA30 — Meta’s Infrastructure Team Needs A Culture Reset](https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a) · `public_excerpt_reviewed` · [local note](../research/sources/SA30.md)
- [SA38 — How Oracle Is Winning the AI Compute Market](https://newsletter.semianalysis.com/p/how-oracle-is-winning-the-ai-compute-market) · `public_excerpt_reviewed` · [local note](../research/sources/SA38.md)
- [P13 — Slurm Workload Manager — Topology Guide](https://slurm.schedmd.com/topology.html) · `page_reviewed` · [local note](../research/sources/P13.md)
- [P14 — NVIDIA DGX SuperPOD: Next Generation Scalable Infrastructure for AI Leadership Reference Architecture Featuring NVIDIA DGX H100](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/) · `page_reviewed` · [local note](../research/sources/P14.md)
- [P15 — Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) · `public_excerpt_reviewed` · [local note](../research/sources/P15.md)
- [P17 — NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) · `page_reviewed` · [local note](../research/sources/P17.md)
- [E013A66FA9A — NIST SP 800-82 Revision 3: OT Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final) · `public_excerpt_reviewed` · [local note](../research/sources/E013A66FA9A.md)
- [E71B82C307F — Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) · `page_reviewed` · [local note](../research/sources/E71B82C307F.md)
- [E7B9A3E66DB — Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) · `page_reviewed` · [local note](../research/sources/E7B9A3E66DB.md)
- [E571B75F6E0 — Google SRE: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) · `page_reviewed` · [local note](../research/sources/E571B75F6E0.md)

<a id="d15"></a>

### D15 — Capacity, cost and system decisions

**Central question:** Which constraint limits useful service, and which change is worth making?

Combine engineering, delivery and workload models into a bounded decision with explicit uncertainty.

**Included scope:**

- Capacity ledgers, bottlenecks, reserves and phased expansion
- Capital and operating costs, ownership/lease boundaries and commercial commitments
- Energy, hardware utilization, financing assumptions and time to service
- Cost per useful workload outcome versus cost per MW or GPU-hour
- Sensitivity, scenarios, uncertainty, retrofit and retirement

**Prerequisites:** [D02 — Workloads and the infrastructure brief](#d02), [D04 — Campus and building power distribution](#d04), [D06 — Rack power and the 800 V DC transition](#d06), [D08 — Networking and interconnects](#d08), [D09 — Storage, orchestration and recovery](#d09), [D11 — Heat rejection, climate and water](#d11), [D13 — Design, procurement and commissioning](#d13), [D14 — Controls, operations and reliability](#d14)

**Learning objectives and assessments:**

#### D15.1

Reconcile electrical, thermal, spatial, network and commissioned-service limits using the same boundaries.

**Assessment:** Calculate a synthetic capacity ceiling and identify tied constraints without treating it as measured operating demand.

**Existing baseline:** partial. `capacity-bottleneck` — The smallest limit wins.; `facility-overhead` — Budget the whole facility.

#### D15.2

Build an auditable cost model that separates capital, energy, operations, ownership and financing assumptions.

**Assessment:** Compare two supplied ownership or service models over an explicit horizon with a consistent denominator and utilization scenario.

**Existing baseline:** missing. No existing lesson mapped.

#### D15.3

Explain why cost per MW, per installed accelerator and per useful result answer different questions.

**Assessment:** Recalculate a scenario after changing throughput or utilization while leaving installed capacity constant.

**Existing baseline:** partial. `useful-compute` — Watts do not measure useful work.

#### D15.4

Evaluate an upgrade using sensitivity to delivery date, service output, efficiency and constraints.

**Assessment:** Choose a synthetic power, cooling or network investment and identify the assumptions that reverse its ranking.

**Existing baseline:** missing. No existing lesson mapped.

#### D15.5

Audit a named project's public evidence without filling unknown capacity, topology or economics with generic assumptions.

**Assessment:** Produce a dated case ledger separating announced, designed, permitted, commissioned and observed facts; list unresolved questions.

**Existing baseline:** partial. `abilene-case` — Read a real headline precisely.

**Visual plan: Find the constraint, then change it**

- Prediction: Does removing the current bottleneck necessarily increase delivered useful work or improve cost per result?
- Interaction: Compare a base case and one intervention across capacity, time, cost and useful output; display assumptions beside the result.
- Model boundary: A scenario is not a valuation, site estimate or throughput forecast. Do not add overlapping capacity stages or count shared loads twice.

**Worked example:** Extend the existing 100 MW teaching scenario with separate non-compute IT, commissioning, workload and delivery assumptions; compare two interventions.

**Design tradeoff:** Lowest capital cost, earliest service, highest efficiency and best useful-output economics may select different designs.

**Failure or maintenance scenario:** A technically successful upgrade leaves a separate delivery, network or workload constraint binding.

**Research connections:**

- [SA01 — Datacenter Anatomy Part 1: Electrical Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-1-electrical) · `public_excerpt_reviewed` · [local note](../research/sources/SA01.md)
- [SA02 — Datacenter Anatomy Part 2 – Cooling Systems](https://newsletter.semianalysis.com/p/datacenter-anatomy-part-2-cooling-systems) · `public_excerpt_reviewed` · [local note](../research/sources/SA02.md)
- [SA04 — Multi-Datacenter Training: OpenAI’s Ambitious Plan To Beat Google’s Infrastructure](https://newsletter.semianalysis.com/p/multi-datacenter-training-openais) · `public_excerpt_reviewed` · [local note](../research/sources/SA04.md)
- [SA05 — AI Neocloud Playbook and Anatomy](https://newsletter.semianalysis.com/p/ai-neocloud-playbook-and-anatomy) · `public_excerpt_reviewed` · [local note](../research/sources/SA05.md)
- [SA06 — Co-Packaged Optics (CPO) Book – Scaling with Light for the Next Wave of Interconnect](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling) · `public_excerpt_reviewed` · [local note](../research/sources/SA06.md)
- [SA07 — US Grid Constraints: Towards 40GW+ of Behind-The-Meter Datacenter by 2028?](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw) · `public_excerpt_reviewed` · [local note](../research/sources/SA07.md)
- [SA08 — ClusterMAX™ 2.0: The Industry Standard GPU Cloud Rating System](https://newsletter.semianalysis.com/p/clustermax-20-the-industry-standard) · `public_excerpt_reviewed` · [local note](../research/sources/SA08.md)
- [SA09 — How Much Do GPU Clusters Really Cost?](https://newsletter.semianalysis.com/p/how-much-do-gpu-clusters-really-cost) · `public_excerpt_reviewed` · [local note](../research/sources/SA09.md)
- [SA10 — Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) · `public_excerpt_reviewed` · [local note](../research/sources/SA10.md)
- [P01 — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) · `page_reviewed` · [local note](../research/sources/P01.md)
- [P02 — Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) · `page_reviewed` · [local note](../research/sources/P02.md)
- [P05 — NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) · `page_reviewed` · [local note](../research/sources/P05.md)
- [P07 — ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) · `page_reviewed` · [local note](../research/sources/P07.md)
- [P09 — The Datacenter as a Computer: designing warehouse-scale machines](https://research.google/pubs/the-datacenter-as-a-computer-designing-warehouse-scale-machines/) · `public_excerpt_reviewed` · [local note](../research/sources/P09.md)
- [P10 — Incorporate Minimum Efficiency Requirements for Heating and Cooling Products into Federal Acquisition Documents](https://www.energy.gov/cmei/femp/incorporate-minimum-efficiency-requirements-heating-and-cooling-products-federal) · `page_reviewed` · [local note](../research/sources/P10.md)
- [SA12 — How AI Labs Are Solving the Power Crisis: The Onsite Gas Deep Dive](https://newsletter.semianalysis.com/p/how-ai-labs-are-solving-the-power) · `public_excerpt_reviewed` · [local note](../research/sources/SA12.md)
- [SA13 — Nvidia’s Optical Boogeyman – NVL72, Infiniband Scale Out, 800G & 1.6T Ramp](https://newsletter.semianalysis.com/p/nvidias-optical-boogeyman-nvl72-infiniband) · `public_excerpt_reviewed` · [local note](../research/sources/SA13.md)
- [SA14 — AI Datacenter Energy Dilemma - Race for AI Datacenter Space](https://newsletter.semianalysis.com/p/ai-datacenter-energy-dilemma-race) · `public_excerpt_reviewed` · [local note](../research/sources/SA14.md)
- [SA16 — Google OCS Apollo: The &gt;$3 Billion Game-Changer in Datacenter Networking](https://newsletter.semianalysis.com/p/google-apollo-the-3-billion-game) · `public_excerpt_reviewed` · [local note](../research/sources/SA16.md)
- [SA17 — Energizing AI: Power Delivery Competition Heats Up Vicor, MPS, Delta, ADI, Renesas, Infineon](https://newsletter.semianalysis.com/p/energizing-ai-power-delivery-competition) · `public_excerpt_reviewed` · [local note](../research/sources/SA17.md)
- [SA18 — GPU Cloud Economics Explained – The Hidden Truth](https://newsletter.semianalysis.com/p/gpu-cloud-economics-explained-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA18.md)
- [SA20 — H100 vs GB200 NVL72 Training Benchmarks - Power, TCO, and Reliability Analysis, Software Improvement Over Time](https://newsletter.semianalysis.com/p/h100-vs-gb200-nvl72-training-benchmarks) · `public_excerpt_reviewed` · [local note](../research/sources/SA20.md)
- [SA21 — The Memory Wall: Past, Present, and Future of DRAM](https://newsletter.semianalysis.com/p/the-memory-wall) · `public_excerpt_reviewed` · [local note](../research/sources/SA21.md)
- [SA22 — Scaling the Memory Wall: The Rise and Roadmap of HBM](https://newsletter.semianalysis.com/p/scaling-the-memory-wall-the-rise-and-roadmap-of-hbm) · `public_excerpt_reviewed` · [local note](../research/sources/SA22.md)
- [SA23 — CPUs are Back: The Datacenter CPU Landscape in 2026](https://newsletter.semianalysis.com/p/cpus-are-back-the-datacenter-cpu) · `public_excerpt_reviewed` · [local note](../research/sources/SA23.md)
- [SA24 — Vera Rubin – Extreme Co-Design: An Evolution from Grace Blackwell Oberon](https://newsletter.semianalysis.com/p/vera-rubin-extreme-co-design-an-evolution) · `public_excerpt_reviewed` · [local note](../research/sources/SA24.md)
- [SA25 — TPUv7: Google Takes a Swing at the King](https://newsletter.semianalysis.com/p/tpuv7-google-takes-a-swing-at-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA25.md)
- [SA26 — AWS Trainium3 Deep Dive | A Potential Challenger Approaching](https://newsletter.semianalysis.com/p/aws-trainium3-deep-dive-a-potential) · `public_excerpt_reviewed` · [local note](../research/sources/SA26.md)
- [SA27 — RL Systems Mind the Gap: Matching Trainer and Generator Throughput](https://newsletter.semianalysis.com/p/rl-systems-mind-the-gap-matching) · `public_excerpt_reviewed` · [local note](../research/sources/SA27.md)
- [SA29 — The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) · `public_excerpt_reviewed` · [local note](../research/sources/SA29.md)
- [SA30 — Meta’s Infrastructure Team Needs A Culture Reset](https://newsletter.semianalysis.com/p/metas-infrastructure-team-needs-a) · `public_excerpt_reviewed` · [local note](../research/sources/SA30.md)
- [SA31 — From Tokens to Burgers: A Water Footprint Face-Off](https://newsletter.semianalysis.com/p/from-tokens-to-burgers-a-water-footprint) · `public_excerpt_reviewed` · [local note](../research/sources/SA31.md)
- [SA32 — Are AI Datacenters Increasing Electric Bills for American Households?](https://newsletter.semianalysis.com/p/are-ai-datacenters-increasing-electric) · `public_excerpt_reviewed` · [local note](../research/sources/SA32.md)
- [SA33 — Stop Saying Half of 2026 US Datacenter Capacity Is Canceled](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA33.md)
- [SA34 — $12B of US ratepayers' money wasted on a modeling mistake and PJM wants to do it again](https://newsletter.semianalysis.com/p/12b-of-us-ratepayers-money-wasted) · `public_excerpt_reviewed` · [local note](../research/sources/SA34.md)
- [SA35 — Nvidia GPU Debt Backstop Unleashes the AI Project Trinity: Capital, Offtake and Datacenters](https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes) · `public_excerpt_reviewed` · [local note](../research/sources/SA35.md)
- [SA36 — Microsoft's AI Strategy Deconstructed - From Energy to Tokens](https://newsletter.semianalysis.com/p/microsofts-ai-strategy-deconstructed) · `public_excerpt_reviewed` · [local note](../research/sources/SA36.md)
- [SA37 — xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) · `public_excerpt_reviewed` · [local note](../research/sources/SA37.md)
- [SA38 — How Oracle Is Winning the AI Compute Market](https://newsletter.semianalysis.com/p/how-oracle-is-winning-the-ai-compute-market) · `public_excerpt_reviewed` · [local note](../research/sources/SA38.md)
- [SA39 — OpenAI Stargate Joint Venture Demystified | Microsoft Sore Loser, Does Softbank Have The Capital?, Texas GigaCampus, Winners & Losers](https://newsletter.semianalysis.com/p/openai-stargate-joint-venture-demystified) · `public_excerpt_reviewed` · [local note](../research/sources/SA39.md)
- [SA40 — Google AI Infrastructure Supremacy: Systems Matter More Than Microarchitecture](https://newsletter.semianalysis.com/p/google-ai-infrastructure-supremacy) · `public_excerpt_reviewed` · [local note](../research/sources/SA40.md)
- [P16 — Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) · `page_reviewed` · [local note](../research/sources/P16.md)
- [E50E0F856B0 — GAO Schedule Assessment Guide](https://www.gao.gov/products/gao-16-89g) · `page_reviewed` · [local note](../research/sources/E50E0F856B0.md)
- [EEFB073374C — NIST Handbook 135, 2025: Life Cycle Costing Manual](https://nvlpubs.nist.gov/nistpubs/hb/2025/NIST.HB.135e2025.pdf) · `page_reviewed` · [local note](../research/sources/EEFB073374C.md)
- [E775A7D4E10 — OpenAI: Five new Stargate sites](https://openai.com/index/five-new-stargate-sites/) · `page_reviewed` · [local note](../research/sources/E775A7D4E10.md)

## Paths through the system

### Power → rack

[D01](#d01) → [D03](#d03) → [D04](#d04) → [D05](#d05) → [D06](#d06) → [D07](#d07)

Physical electrical journey. This is a conceptual path, not a universal installed topology.

### Chip → environment

[D07](#d07) → [D10](#d10) → [D11](#d11)

Thermal journey, including parallel air/liquid paths and auxiliary heat inputs.

### Workload → useful service

[D02](#d02) → [D07](#d07) → [D08](#d08) → [D09](#d09) → [D14](#d14) → [D15](#d15)

Information and service dependencies, not a literal packet route.

### Site → service → upgrade

[D02](#d02) → [D03](#d03) → [D12](#d12) → [D04](#d04) → [D13](#d13) → [D14](#d14) → [D15](#d15)

A lifecycle view across domains. Design and procurement iterate; this is not a strict construction schedule.

## Proposed capstones

### C01 — Grid interruption with a thermal dependency

A utility interruption occurs in a hypothetical facility. IT storage support and cooling/control supply paths are specified separately.

Domains: [D04](#d04), [D05](#d05), [D10](#d10), [D11](#d11), [D14](#d14)

**Deliverable:** An annotated topology, discrete failure timeline, energy and power budgets, and a list of missing thermal evidence.

**Assessment:** Find the unsupported auxiliary path; distinguish what is electrically sustained from what can continue delivering service. Do not invent a thermal ride-through time.

### C02 — Hot weather under a fixed site power limit

Ambient conditions move across supplied cooling performance curves while the site electrical limit remains fixed.

Domains: [D01](#d01), [D10](#d10), [D11](#d11), [D14](#d14), [D15](#d15)

**Deliverable:** A before/after power and heat balance with binding constraints and a stated operating response.

**Assessment:** Account for changed cooling capacity and auxiliary draw separately; explain why an annual PUE is not an instantaneous plant model.

### C03 — A denser rack in an existing building

Compare a higher-density rack migration using the existing AC plant, a sidecar option and a separately specified broader DC alternative.

Domains: [D04](#d04), [D05](#d05), [D06](#d06), [D07](#d07), [D10](#d10), [D12](#d12), [D13](#d13), [D15](#d15)

**Deliverable:** Interface matrix, conversion diagrams, current and heat-flow calculations, floor/service-access review, migration sequence and scenario cost comparison.

**Assessment:** Identify retained upstream constraints and new interfaces; separate reference specifications, roadmap claims and hypothetical assumptions.

### C04 — A powered cluster that misses its job target

The hardware has adequate power and cooling, but a synthetic workload suffers fabric congestion and checkpoint stalls.

Domains: [D02](#d02), [D07](#d07), [D08](#d08), [D09](#d09), [D14](#d14), [D15](#d15)

**Deliverable:** Work/wait/recovery timeline, a bounded bottleneck calculation, and an experiment that distinguishes competing causes.

**Assessment:** Use evidence to distinguish a communication/storage constraint from a compute shortfall; do not infer output from MW.

### C05 — Open one phase of a campus

An illustrative project has utility service, some installed racks and uneven subsystem completion. A separate named-site exercise uses only dated public evidence.

Domains: [D03](#d03), [D04](#d04), [D05](#d05), [D09](#d09), [D11](#d11), [D12](#d12), [D13](#d13), [D14](#d14), [D15](#d15)

**Deliverable:** Capacity-state ledger, dependency schedule, integrated acceptance plan and unresolved-evidence list.

**Assessment:** Count only complete, accepted service paths for the synthetic brief; leave the named site's unestablished commissioning and demand values unknown.

## Existing lesson migration

Every current lesson has a proposed reuse location. These are introductory foundations, not completion evidence for the expanded course.

| Current lesson | Proposed objectives |
| --- | --- |
| `one-rack` — One campus. Two journeys. | D01.1 |
| `power-and-energy` — A watt is a rate. | D01.2 |
| `sources-and-grid` — Follow the physical connection. | D03.1 |
| `raise-voltage` — Go farther. Raise the voltage. | D03.2, D04.2 |
| `substation-functions` — Open the substation. | D04.1 |
| `capacity-stages` — Connected is a milestone. | D01.2, D01.4, D03.3, D13.3 |
| `building-power-train` — Bring the power to the rack. | D04.1, D04.4 |
| `ride-through` — The battery buys time. | D05.1, D05.2 |
| `redundant-paths` — A second path must be useful. | D05.2, D05.3, D14.3 |
| `fault-domains` — Keep one fault from spreading. | D05.3, D14.3 |
| `rack-conversion` — The rack changes the rules. | D06.1, D07.1 |
| `low-voltage-current` — Low voltage. Enormous current. | D06.1, D06.2 |
| `useful-compute` — Watts do not measure useful work. | D01.3, D02.1, D02.2, D07.3, D15.3 |
| `electrical-to-heat` — The watt becomes heat. | D01.1, D10.1 |
| `liquid-heat-transport` — Heat needs a moving carrier. | D10.2 |
| `heat-exchanger` — Heat crosses. Fluids stay apart. | D10.3 |
| `residual-air` — This rack still needs air. | D10.1 |
| `outdoor-rejection` — Moving heat adds heat. | D11.1, D11.2 |
| `facility-overhead` — Budget the whole facility. | D01.3, D11.4, D15.1 |
| `capacity-bottleneck` — The smallest limit wins. | D04.4, D15.1 |
| `abilene-case` — Read a real headline precisely. | D01.4, D13.3, D15.5 |
| `whole-system` — Follow the power. Close the heat path. | D01.1 |

## Deliberate exclusions and re-entry conditions

### Full semiconductor manufacturing and transistor/device physics

CHIPS and specialist material own fabrication depth. Here packaging, devices and memory matter where they change rack and facility requirements.

**Reconsider when:** Include a mechanism when it is necessary to explain a compute, electrical or thermal interface.

### Detailed electrical, structural, fire or mechanical design qualification

This course teaches interpretation and bounded reasoning, not stamped designs, field switching procedures or jurisdiction-wide compliance.

**Reconsider when:** Teach the relevant design question and point to dated local requirements and qualified review; do not omit safety interfaces.

### A complete generation-technology or electricity-market survey

Depth is limited to the supply, fuel, interconnection, emissions and commercial distinctions needed for data-center decisions.

**Reconsider when:** Include a supply option when it materially changes deliverability, operating behavior or project economics.

### Supplier rankings, investment recommendations and exhaustive company histories

The curriculum is organized around capabilities and decisions. Company detail is a dated example, not the organizing principle.

**Reconsider when:** Use a sourced case when it explains a specific architecture, delivery constraint or measurable tradeoff.

### Full GPU programming, model training and cloud administration tutorials

Workload and software mechanisms are included to explain infrastructure behavior; implementing every software layer would be a separate course.

**Reconsider when:** Include a small reproducible experiment when it tests an infrastructure learning objective.

### Every enterprise/edge/telecom facility variant

Modern AI facilities are the center. Conventional and retrofit configurations are taught where they establish prerequisites or meaningful alternatives.

**Reconsider when:** Include a contrasting case when it changes an assumption in the central model.

## Production priorities

1. Prototype one electrical architecture comparison, one thermal model and one network/recovery scenario before allocating runtime.
2. Review prerequisites and first-use vocabulary against the six-act sequence; domain IDs are stable reference IDs, not chapter numbers.
3. Expand the seed source catalog into a dated article inventory; record access/review status, domain mappings, duplicates, exclusions and unresolved primary evidence.
4. At lesson authoring, map each objective to exact claims, citations, original visual assets and an application assessment. A domain-level source link is not sufficient.
5. Obtain separate electrical/facilities and cluster/network technical reviews, then rehearse dense sections with intended learners.
6. Publish the long-form recording with navigable text, source dates, glossary, calculators and an errata location; maintain the companion when implementations change.
