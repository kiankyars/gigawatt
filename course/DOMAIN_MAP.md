# GIGAWATT — the domain map

<!-- Generated from domain-map.json, research-sources.json and lessons.json. Edit those sources; run uv run gigawatt-map. -->

As of **2026-09-10**. Curriculum objectives and sequence. Authored lesson coverage is reported in EXPANDED_COURSE.md; presentation adaptation and review status are tracked in COURSE_REVIEW.md.

From grid connection to useful compute. Follow the power, close the heat path, operate the system.

[Interactive map](domain-map.html) · [Course review](COURSE_REVIEW.md) · [Source index](../research/INDEX.md) · [Research library](../research/README.md)

## How to read this map

The [filled-in course template](COURSE_REVIEW.md) owns audience, overall scope, exclusions, runtime and production priorities. This map owns the detailed objectives, prerequisites, teaching sequence and capstone briefs within that design.

[Current authored coverage](EXPANDED_COURSE.md#objective-to-lesson-coverage) is generated from the lesson records. Presentation adaptation and review status are tracked in the course template.

## Evidence and historical introduction coverage

Source-to-domain mappings are derived from `research-sources.json` → `sources[].domains`. They identify research connections, not verified support for every objective.

- **partial:** The retained 22-lesson introduction teaches a fragment of this objective. This is a historical reuse label, not the status of the expanded course.
- **missing:** The retained 22-lesson introduction does not substantively teach this objective. See the generated expanded manuscript for current authored coverage.

## System lanes

### Frame the system

Define quantities and the useful work the system must deliver.

- [System boundaries and quantities](#d01)
- [Workloads and the infrastructure brief](#d02)

### Bring power to the racks

Connect, distribute, protect and convert electricity.

- [Siting, grid connection and supply](#d03)
- [Campus and building power distribution](#d04)
- [Continuity, storage and protection](#d05)
- [Rack power and the 800 V DC transition](#d06)

### Turn hardware into useful work

Coordinate compute, memory, networks, storage and jobs.

- [Compute, memory and the rack](#d07)
- [Networking and interconnects](#d08)
- [Storage, orchestration and recovery](#d09)

### Return the heat

Capture heat at the devices and reject it under real site conditions.

- [Chip and rack heat capture](#d10)
- [Heat rejection, climate and water](#d11)

### Build, operate and decide

Make the physical system deliverable, testable, maintainable and economically coherent.

- [Physical site, buildings and safety](#d12)
- [Design, procurement and commissioning](#d13)
- [Controls, operations and reliability](#d14)
- [Capacity, cost and system decisions](#d15)

## Proposed teaching sequence

Topics follow their prerequisites; runtime is not yet allocated.

### A01 — See the system and define the job

[System boundaries and quantities](#d01) → [Workloads and the infrastructure brief](#d02)

Establish the vocabulary, three paths and the workload brief used throughout.

### A02 — Find a site and deliver power

[Siting, grid connection and supply](#d03) → [Physical site, buildings and safety](#d12) → [Campus and building power distribution](#d04)

Make the physical location, utility connection and single-line diagram legible.

### A03 — Keep it running and enter the rack

[Continuity, storage and protection](#d05) → [Rack power and the 800 V DC transition](#d06)

Compare continuity and conversion choices, including 800 V DC, against interfaces and failures.

### A04 — Make the cluster productive

[Compute, memory and the rack](#d07) → [Networking and interconnects](#d08) → [Storage, orchestration and recovery](#d09)

Connect compute, memory, communication, storage and scheduling to useful progress.

### A05 — Close the heat and water balances

[Chip and rack heat capture](#d10) → [Heat rejection, climate and water](#d11)

Follow heat from local device limits to climate-dependent rejection and resource use.

### A06 — Deliver, operate and make decisions

[Design, procurement and commissioning](#d13) → [Controls, operations and reliability](#d14) → [Capacity, cost and system decisions](#d15)

Test complete service paths, operate them, and defend a system decision with uncertainty.

## Domain teaching plans

<a id="d01"></a>

### System boundaries and quantities

**Central question:** What exactly does a megawatt of data-center capacity describe?

Give every later calculation a unit, a boundary, and an operating condition.

**Included scope:**

- Campus, building, hall, row, rack, server, package and die
- White space and grey/gray space as layout conventions; distinguish rack space, data-hall area and support areas
- Power, energy, real/apparent power, efficiency and time
- Nameplate, reserved, commissioned, available, demanded and productive capacity
- Physical flows versus commercial relationships; reference designs versus actual sites

**Prerequisites:** None in this map.

**Learning objectives and assessments:**

#### Learning objective 1

Trace electrical energy, heat, and information through a data center while keeping the accounting boundaries separate.

**Assessment:** Annotate one campus diagram with electrical, heat and information paths; identify white and grey space on its floor plan and explain why those area labels are not energy-accounting boundaries. Explain why useful computation and dissipated heat are not competing energy allocations.

**Historical introduction coverage:** partial. `one-rack` — One campus. Two journeys.; `electrical-to-heat` — The watt becomes heat.; `whole-system` — Follow the power. Close the heat path.

#### Learning objective 2

Convert power and energy across units and time; distinguish a measured load from a capacity rating.

**Assessment:** Calculate an energy total from a stepped load profile and identify what cannot be inferred from a service rating.

**Historical introduction coverage:** partial. `power-and-energy` — A watt is a rate.; `capacity-stages` — Connected is a milestone.

#### Learning objective 3

Define denominators for facility, IT and compute-only metrics and label the time window.

**Assessment:** Reconcile a facility energy ledger with IT energy, overhead and a separately measured workload output.

**Historical introduction coverage:** partial. `facility-overhead` — Budget the whole facility.; `useful-compute` — Watts do not measure useful work.

#### Learning objective 4

Separate physical principles, design specifications, observed deployments, announcements, forecasts and teaching assumptions.

**Assessment:** Classify six supplied claims and state the additional evidence needed to call capacity operational.

**Historical introduction coverage:** partial. `abilene-case` — Read a real headline precisely.; `capacity-stages` — Connected is a milestone.

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
- [P17 — NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) · `page_reviewed` · [local note](../research/sources/P17.md)
- [E22133B3DE1 — EIA — Laws of energy](https://www.eia.gov/energyexplained/what-is-energy/laws-of-energy.php) · `page_reviewed` · [local note](../research/sources/E22133B3DE1.md)
- [E3F4CB1B7FF — DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) · `page_reviewed` · [local note](../research/sources/E3F4CB1B7FF.md)
- [ED20FD8CBCF — EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) · `page_reviewed` · [local note](../research/sources/ED20FD8CBCF.md)
- [EB34D92F523 — OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) · `page_reviewed` · [local note](../research/sources/EB34D92F523.md)
- [EE02276C332 — MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) · `page_reviewed` · [local note](../research/sources/EE02276C332.md)
- [EFB703CFC3D — Schneider Electric — PM2200 total power calculation for accuracy verification](https://productinfo.se.com/pm2200/5afc2b5546e0fb00011e5e9d/PM2200%20series%20User%20Manual/English/BM_PM2200seriesUserManual_0000074170.ditamap.xml/%24/C_VerifyingAccuracy_PowerTotCalcuation_0000034437) · `page_reviewed` · [local note](../research/sources/EFB703CFC3D.md)
- [E7A716A810E — Leviton — Data center white space and gray space](https://leviton.com/support/literature/newsletters/insider/insideroctober2025/focusedproductoctober2025) · `page_reviewed` · [local note](../research/sources/E7A716A810E.md)
- [EFE70308E0A — Vertiv — Deploying Liquid Cooling in the Data Center](https://prod.vertiv.cn/4a9616/globalassets/documents/white-papers/liquid-cooling/vertiv-liquidcooling-wp-en-na-sl-71113-web.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/EFE70308E0A.md)
- [P18 — OpenStax — 20.5 Alternating Current versus Direct Current (College Physics 2e)](https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current) · `page_reviewed` · [local note](../research/sources/P18.md)
- [P61 — The Green Grid — PUE: A Comprehensive Examination of the Metric](https://datacenters.lbl.gov/sites/default/files/WP49-PUE%20A%20Comprehensive%20Examination%20of%20the%20Metric_v6.pdf) · `page_reviewed` · [local note](../research/sources/P61.md)
- [P63 — Google Cloud — Best practices for batch inference on GKE](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/machine-learning/inference/batch-inference) · `page_reviewed` · [local note](../research/sources/P63.md)
- [P64 — NVIDIA DGX GB200/GB300 hardware guide — Power shelves](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html#power-shelves) · `page_reviewed` · [local note](../research/sources/P64.md)
- [P65 — EIA — How electricity is generated](https://www.eia.gov/energyexplained/electricity/how-electricity-is-generated.php) · `public_excerpt_reviewed` · [local note](../research/sources/P65.md)
- [P66 — EIA — Delivery of electricity to consumers](https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php) · `public_excerpt_reviewed` · [local note](../research/sources/P66.md)
- [P67 — OpenStax · Resistance and simple circuits](https://openstax.org/books/college-physics-2e/pages/20-2-ohms-law-resistance-and-simple-circuits) · `page_reviewed` · [local note](../research/sources/P67.md)

<a id="d02"></a>

### Workloads and the infrastructure brief

**Central question:** What useful work must the facility deliver, and on what schedule?

Derive infrastructure requirements from the service or job rather than starting with an equipment inventory.

**Included scope:**

- Training, inference and conventional services as different load and service profiles
- Throughput, latency, availability, memory demand and utilization
- Parallelism, communication, checkpointing and workload-driven power variation
- Design envelopes and uncertainty; avoiding universal watts-to-tokens conversions

**Prerequisites:** [System boundaries and quantities](#d01)

**Learning objectives and assessments:**

#### Learning objective 1

Translate a workload brief into compute, memory, network, storage, power and service requirements.

**Assessment:** Compare two supplied training and inference briefs and explain which requirements need measurement rather than a rack-count estimate.

**Historical introduction coverage:** partial. `useful-compute` — Watts do not measure useful work.

#### Learning objective 2

Distinguish hardware occupancy, power draw and productive utilization.

**Assessment:** Explain three traces in which the same installed hardware produces different useful output; identify idle and waiting intervals.

**Historical introduction coverage:** partial. `useful-compute` — Watts do not measure useful work.

#### Learning objective 3

Explain how batching, parallel execution and synchronized job phases change the infrastructure demand profile.

**Assessment:** Read a supplied job timeline and predict communication, checkpoint and load-transition intervals without assuming a universal waveform.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 4

State an infrastructure design envelope and identify which assumptions a benchmark can and cannot validate.

**Assessment:** Write acceptance criteria for a hypothetical cluster using declared workload, precision, batch, latency and availability conditions.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [P63 — Google Cloud — Best practices for batch inference on GKE](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/machine-learning/inference/batch-inference) · `page_reviewed` · [local note](../research/sources/P63.md)
- [P77 — Google — Supporting power grids with demand response](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption) · `public_excerpt_reviewed` · [local note](../research/sources/P77.md)

<a id="d03"></a>

### Siting, grid connection and supply

**Central question:** Where can the required power actually arrive, and when?

Connect the physical site decision to grid constraints, available infrastructure and the project schedule.

**Included scope:**

- Load connection, utility studies, substations, transmission and distribution interfaces
- Behind-the-meter supply: the customer-side meter boundary, grid import/export, and separately established island capability
- Capacity, energy, fuel, emissions, curtailment and time matching
- Land, fiber, water, climate and local constraints as joint siting inputs

**Prerequisites:** [System boundaries and quantities](#d01), [Workloads and the infrastructure brief](#d02)

**Learning objectives and assessments:**

#### Learning objective 1

Trace a physical supply path and distinguish it from a power purchase agreement or energy attribute claim.

**Assessment:** Draw the metered connection separately from two commercial arrangements; name what each establishes.

**Historical introduction coverage:** partial. `sources-and-grid` — Follow the physical connection.

#### Learning objective 2

Explain voltage, current and conductor loss in a bounded AC or DC comparison.

**Assessment:** Compare two balanced three-phase transfer scenarios with stated power factor and conductor resistance; list excluded losses.

**Historical introduction coverage:** partial. `raise-voltage` — Go farther. Raise the voltage.

#### Learning objective 3

Explain the milestones and constraints between a proposed large load and service available to that load.

**Assessment:** Turn a supplied project timeline into a capacity ledger without treating an application, agreement or energized substation as commissioned IT.

**Historical introduction coverage:** partial. `capacity-stages` — Connected is a milestone.

#### Learning objective 4

Compare utility-only and behind-the-meter supply against energy, capacity, fuel and operating requirements; distinguish customer-side location from island capability.

**Assessment:** Calculate grid import or export for a synthetic on-site supply case, then the islanded power deficit and storage duration. Evaluate fuel and curtailment constraints and record unresolved interconnection and operating requirements.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [E38B3BEAAC1 — NARUC — Regulators’ Financial Toolbox: Behind-the-Meter Energy Storage](https://pubs.naruc.org/pub/6233DBE2-B58B-52FF-925E-250DD26DECF9) · `public_excerpt_reviewed` · [local note](../research/sources/E38B3BEAAC1.md)
- [E0410763323 — DOE — Solar Integration: Distributed Energy Resources and Microgrids Basics](https://www.energy.gov/cmei/systems/solar-integration-distributed-energy-resources-and-microgrids-basics) · `page_reviewed` · [local note](../research/sources/E0410763323.md)
- [SA41 — What is So Hard About Behind-The-Meter Power For Datacenters? Part 1](https://newsletter.semianalysis.com/p/what-is-so-hard-about-behind-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA41.md)
- [P34 — DOE — Beyond Land Leases: Harnessing Data Centers for Tribal Economic Development](https://www.energy.gov/indianenergy/beyond-land-leases-harnessing-data-centers-tribal-economic-development-webinar) · `page_reviewed` · [local note](../research/sources/P34.md)
- [P38 — MLGW — 2025 xAI Update](https://www.mlgw.com/images/content/files/pdf/new/xAI%202025%20Update.pdf) · `page_reviewed` · [local note](../research/sources/P38.md)
- [P39 — Energy Transfer — Q2 2026 investor presentation](https://ir.energytransfer.com/static-files/c29697db-5336-4262-8bf3-3c6e409ccb19) · `public_excerpt_reviewed` · [local note](../research/sources/P39.md)
- [P40 — DOE — CHP Technologies: Gas Turbines](https://betterbuildingssolutioncenter.energy.gov/sites/default/files/attachments/CHP_Gas_Turbines.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/P40.md)
- [P65 — EIA — How electricity is generated](https://www.eia.gov/energyexplained/electricity/how-electricity-is-generated.php) · `public_excerpt_reviewed` · [local note](../research/sources/P65.md)
- [P66 — EIA — Delivery of electricity to consumers](https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php) · `public_excerpt_reviewed` · [local note](../research/sources/P66.md)
- [P73 — Crusoe — Abilene campus development update](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) · `page_reviewed` · [local note](../research/sources/P73.md)
- [P74 — Crusoe — Abilene cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) · `page_reviewed` · [local note](../research/sources/P74.md)
- [P75 — Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) · `page_reviewed` · [local note](../research/sources/P75.md)
- [P76 — Crusoe — 2025 impact report web summary](https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report) · `page_reviewed` · [local note](../research/sources/P76.md)
- [P77 — Google — Supporting power grids with demand response](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption) · `public_excerpt_reviewed` · [local note](../research/sources/P77.md)
- [P78 — MLGW — xAI project quick facts](https://www.mlgw.com/images/content/files/pdf/2024xAI%20and%20MLGW%20Quick%20Facts%201.pdf) · `page_reviewed` · [local note](../research/sources/P78.md)
- [SA42 — SpaceX 10GW in 2027 — construction pace and equipment procurement](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) · `public_excerpt_reviewed` · [local note](../research/sources/SA42.md)

<a id="d04"></a>

### Campus and building power distribution

**Central question:** How does power get from the connection to each load?

Teach electrical topology, equipment roles and rating boundaries before comparing architecture changes.

**Included scope:**

- Single-line diagrams and voltage levels
- Transformers, switchgear, switchboards, busway, cables and distribution units
- Real/apparent power, power factor, efficiency, harmonic and thermal limits
- AC distribution and alternative DC conversion locations
- House loads, IT loads, reserved capacity and expansion phases

**Prerequisites:** [System boundaries and quantities](#d01), [Siting, grid connection and supply](#d03)

**Learning objectives and assessments:**

#### Learning objective 1

Read a generic single-line diagram and explain what each distribution component changes, measures, switches or protects.

**Assessment:** Annotate an unfamiliar generic diagram and identify the loads behind each boundary.

**Historical introduction coverage:** partial. `substation-functions` — Open the substation.; `building-power-train` — Bring the power to the rack.

#### Learning objective 2

Translate load requirements into currents and equipment loading without confusing kW with kVA or nameplate with usable capacity.

**Assessment:** Calculate loading in a stated balanced scenario, including conversion efficiency and a supplied power factor; explain missing design inputs.

**Historical introduction coverage:** partial. `raise-voltage` — Go farther. Raise the voltage.

#### Learning objective 3

Compare centralized and distributed conversion and identify which conductors, equipment and loss boundaries change.

**Assessment:** Mark the changed interfaces on AC, near-rack DC and facility DC reference diagrams without claiming one universal efficiency improvement.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 4

Reconcile IT and auxiliary loads with a downstream electrical capacity budget across project phases.

**Assessment:** Find the binding transformer, feeder or service constraint in a synthetic phase-opening plan.

**Historical introduction coverage:** partial. `capacity-bottleneck` — The smallest limit wins.; `building-power-train` — Bring the power to the rack.

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
- [EFB703CFC3D — Schneider Electric — PM2200 total power calculation for accuracy verification](https://productinfo.se.com/pm2200/5afc2b5546e0fb00011e5e9d/PM2200%20series%20User%20Manual/English/BM_PM2200seriesUserManual_0000074170.ditamap.xml/%24/C_VerifyingAccuracy_PowerTotCalcuation_0000034437) · `page_reviewed` · [local note](../research/sources/EFB703CFC3D.md)
- [EA7B686AF9E — NVIDIA, Partners Drive Next-Gen Efficient Gigawatt AI Factories in Buildup for Vera Rubin](https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin/) · `page_reviewed` · [local note](../research/sources/EA7B686AF9E.md)
- [P18 — OpenStax — 20.5 Alternating Current versus Direct Current (College Physics 2e)](https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current) · `page_reviewed` · [local note](../research/sources/P18.md)
- [P19 — Steven H. Low — Power System Analysis: Analytical tools and structural properties (April 7, 2025 draft)](https://netlab.caltech.edu/assets/book/PSA/Low-PSA-v20250407.pdf) · `page_reviewed` · [local note](../research/sources/P19.md)
- [P20 — Wolfspeed — Powering AI with reliable SiC-based solid-state transformers](https://assets.wolfspeed.com/uploads/2026/03/Wolfspeed_Powering_AI_with_reliable_SiC-based_solid-state_transformers_white_paper.pdf) · `page_reviewed` · [local note](../research/sources/P20.md)
- [P21 — Texas Instruments — TIDA-011012 modular solid-state transformer reference design](https://www.ti.com/tool/TIDA-011012) · `page_reviewed` · [local note](../research/sources/P21.md)
- [P22 — Huber et al. — Comparative Evaluation of MVAC–LVDC SST and Hybrid Transformer Concepts for Future Datacenters (IPEC 2022)](https://www.ams-publications.ee.ethz.ch/uploads/tx_ethpublications/1_IPEC_2022_Final_Huber.pdf) · `page_reviewed` · [local note](../research/sources/P22.md)
- [P23 — Wolfspeed — Introduction of a commercially available 10 kV SiC power MOSFET](https://www.wolfspeed.com/company/news-events/news/wolfspeed-introduces-industrys-first-commercially-available-10000v-silicon-carbide-power-mosfet/) · `page_reviewed` · [local note](../research/sources/P23.md)
- [P24 — Schneider Electric — What is UPS efficiency and how is it calculated?](https://www.se.com/us/en/faqs/FAQ000244215/) · `page_reviewed` · [local note](../research/sources/P24.md)
- [P25 — Texas Instruments — Power Loss in Switching Power Supplies](https://www.ti.com/document-viewer/lit/html/SLUAAL9) · `page_reviewed` · [local note](../research/sources/P25.md)
- [P29 — Eaton — Automatic transfer switch fundamentals](https://www.eaton.com/us/en-us/products/low-voltage-power-distribution-control-systems/automatic-transfer-switches/automatic-transfer-switch-fundamentals.html) · `page_reviewed` · [local note](../research/sources/P29.md)
- [P30 — Schneider Electric — Presence of an Uninterruptible Power Supply (UPS)](https://www.electrical-installation.org/enwiki/Presence_of_an_Uninterruptible_Power_Supply_%28UPS%29) · `page_reviewed` · [local note](../research/sources/P30.md)
- [P33 — Texas Instruments — Basic Calculation of a Buck Converter’s Power Stage](https://www.ti.com/lit/an/slva477b/slva477b.pdf) · `page_reviewed` · [local note](../research/sources/P33.md)
- [P41 — Texas Instruments — TIDA-00349 isolated DC/DC converter](https://www.ti.com/tool/TIDA-00349) · `page_reviewed` · [local note](../research/sources/P41.md)
- [P43 — Hitachi Energy — Core-type transformers](https://www.hitachienergy.com/products-and-solutions/transformers/power-transformers/generator-step-up-transformers-gsu/core-type-transformers) · `page_reviewed` · [local note](../research/sources/P43.md)
- [P44 — Schneider Electric — AA and AA/FA transformer cooling](https://www.se.com/ca/en/faqs/FA102583/) · `page_reviewed` · [local note](../research/sources/P44.md)
- [P45 — Eaton — Medium-voltage solid-state transformer](https://www.eaton.com/us/en-us/catalog/medium-voltage-power-distribution-control-systems/medium-voltage-solid-state-transformer.html) · `page_reviewed` · [local note](../research/sources/P45.md)
- [P54 — OCP — Data Center Facility: Low Voltage Direct Current Power Distribution, v1.0](https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1) · `public_excerpt_reviewed` · [local note](../research/sources/P54.md)
- [P66 — EIA — Delivery of electricity to consumers](https://www.eia.gov/energyexplained/electricity/delivery-to-consumers.php) · `public_excerpt_reviewed` · [local note](../research/sources/P66.md)
- [P67 — OpenStax · Resistance and simple circuits](https://openstax.org/books/college-physics-2e/pages/20-2-ohms-law-resistance-and-simple-circuits) · `page_reviewed` · [local note](../research/sources/P67.md)
- [P68 — Schneider · Definition of power factor](https://www.electrical-installation.org/enwiki/Definition_of_Power_Factor) · `public_excerpt_reviewed` · [local note](../research/sources/P68.md)
- [P69 — Eaton · UPS fundamentals handbook](https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-ups-fundamentals-handbook-anz.pdf) · `page_reviewed` · [local note](../research/sources/P69.md)
- [P78 — MLGW — xAI project quick facts](https://www.mlgw.com/images/content/files/pdf/2024xAI%20and%20MLGW%20Quick%20Facts%201.pdf) · `page_reviewed` · [local note](../research/sources/P78.md)
- [SA42 — SpaceX 10GW in 2027 — construction pace and equipment procurement](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) · `public_excerpt_reviewed` · [local note](../research/sources/SA42.md)

<a id="d05"></a>

### Continuity, storage and protection

**Central question:** What survives a disturbance, and for how long?

Connect backup supply, fault isolation and maintenance to complete operating paths.

**Included scope:**

- UPS, batteries, generators, transfer sequences and load shedding
- Stored energy versus discharge power; transient response versus outage duration
- N, N+1, 2N, common-mode failures and maintainability
- Grounding, fault detection, selective isolation and AC/DC protection concepts
- Electrical and thermal ride-through together

**Prerequisites:** [System boundaries and quantities](#d01), [Campus and building power distribution](#d04)

**Learning objectives and assessments:**

#### Learning objective 1

Calculate bounded stored-energy runtime while checking discharge power and reserve assumptions.

**Assessment:** Compare two storage systems with the same MWh but different MW limits; explain why neither energy alone nor nameplate guarantees ride-through.

**Historical introduction coverage:** partial. `ride-through` — The battery buys time.

#### Learning objective 2

Trace an interruption, transfer and restoration sequence including IT, cooling and controls.

**Assessment:** Predict which loads remain supported at each step of a supplied sequence; identify a missing auxiliary supply.

**Historical introduction coverage:** partial. `ride-through` — The battery buys time.; `redundant-paths` — A second path must be useful.

#### Learning objective 3

Evaluate path independence and surviving capacity during both a fault and planned maintenance.

**Assessment:** Find a common-mode dependency in a two-feed diagram and calculate load support with one path unavailable.

**Historical introduction coverage:** partial. `redundant-paths` — A second path must be useful.; `fault-domains` — Keep one fault from spreading.

#### Learning objective 4

Explain why fault clearing and grounding require topology-specific AC/DC protection design.

**Assessment:** Compare two conceptual isolation sequences and list the protection evidence needed before endorsing either architecture.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [EE53DCAF5E1 — Uptime Institute — Myths and Misconceptions Regarding the Tier Certification System](https://journal.uptimeinstitute.com/myths-and-misconceptions-regarding-the-uptime-institutes-tier-certification-system/) · `public_excerpt_reviewed` · [local note](../research/sources/EE53DCAF5E1.md)
- [EA0B6C5ED33 — Schneider Electric — Comparing UPS System Design Configurations, White Paper 75 Revision 4](https://www.se.com/us/en/download/document/SPD_SADE-5TPL8X_EN/) · `page_reviewed` · [local note](../research/sources/EA0B6C5ED33.md)
- [E836C561209 — Schneider Electric — Why Two Cords Do Not Guarantee Power Redundancy to an IT Device](https://blog.se.com/datacenter/architecture/2014/08/06/two-cords-guarantee-power-redundancy-device/) · `page_reviewed` · [local note](../research/sources/E836C561209.md)
- [E37FE7B98A1 — Schneider Electric — Easy UPS 3-Phase Modular 50–250 kW: UPS Modes](https://productinfo.se.com/easyups3pmodular/990-6537-easy-ups-3-phase-modular-50-250-kw-operation/English/990-6537%20Operation%20Easy%20UPS%203-Phase%20Modular%2050-250%20kW_0001015104.xml/%24/GalaxyPX_UPSModes_0000761714) · `page_reviewed` · [local note](../research/sources/E37FE7B98A1.md)
- [E38B3BEAAC1 — NARUC — Regulators’ Financial Toolbox: Behind-the-Meter Energy Storage](https://pubs.naruc.org/pub/6233DBE2-B58B-52FF-925E-250DD26DECF9) · `public_excerpt_reviewed` · [local note](../research/sources/E38B3BEAAC1.md)
- [E0410763323 — DOE — Solar Integration: Distributed Energy Resources and Microgrids Basics](https://www.energy.gov/cmei/systems/solar-integration-distributed-energy-resources-and-microgrids-basics) · `page_reviewed` · [local note](../research/sources/E0410763323.md)
- [SA41 — What is So Hard About Behind-The-Meter Power For Datacenters? Part 1](https://newsletter.semianalysis.com/p/what-is-so-hard-about-behind-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA41.md)
- [P24 — Schneider Electric — What is UPS efficiency and how is it calculated?](https://www.se.com/us/en/faqs/FAQ000244215/) · `page_reviewed` · [local note](../research/sources/P24.md)
- [P25 — Texas Instruments — Power Loss in Switching Power Supplies](https://www.ti.com/document-viewer/lit/html/SLUAAL9) · `page_reviewed` · [local note](../research/sources/P25.md)
- [P26 — Schneider Electric — Easy UPS 3-Phase Modular physical specifications](https://productinfo.se.com/easyups3pmodular/990-91580-technical-specifications-easy-ups-3-phase-modular/English/990-91580%20Technical%20Specifications%20Easy%20UPS%203-Phase%20Modular50-250%20kW%20UPS_0001011916.xml/%24/PhysicalREF_0000019941) · `page_reviewed` · [local note](../research/sources/P26.md)
- [P27 — Schneider Electric — Easy UPS 3-Phase Modular hardware options](https://productinfo.se.com/easyups3pmodular/990-91580-technical-specifications-easy-ups-3-phase-modular/English/990-91580%20Technical%20Specifications%20Easy%20UPS%203-Phase%20Modular50-250%20kW%20UPS_0001011916.xml/%24/GalaxyPX_HardwareOptions_0000862721) · `page_reviewed` · [local note](../research/sources/P27.md)
- [P28 — Open Compute Project — Open Rack V3 BBU Module Specification 1.4](https://www.opencompute.org/documents/open-rack-v3-bbu-module-spec-1-4-pdf) · `page_reviewed` · [local note](../research/sources/P28.md)
- [P29 — Eaton — Automatic transfer switch fundamentals](https://www.eaton.com/us/en-us/products/low-voltage-power-distribution-control-systems/automatic-transfer-switches/automatic-transfer-switch-fundamentals.html) · `page_reviewed` · [local note](../research/sources/P29.md)
- [P30 — Schneider Electric — Presence of an Uninterruptible Power Supply (UPS)](https://www.electrical-installation.org/enwiki/Presence_of_an_Uninterruptible_Power_Supply_%28UPS%29) · `page_reviewed` · [local note](../research/sources/P30.md)
- [P31 — Eaton — DC-link capacitor modules](https://www.eaton.com/gb/en-gb/products/electronic-components/topics/dc-link-modules.html) · `page_reviewed` · [local note](../research/sources/P31.md)
- [P32 — Eaton — Choosing the optimal UPS topology](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/choosing-the-optimal-ups-topology-.html) · `page_reviewed` · [local note](../research/sources/P32.md)
- [P33 — Texas Instruments — Basic Calculation of a Buck Converter’s Power Stage](https://www.ti.com/lit/an/slva477b/slva477b.pdf) · `page_reviewed` · [local note](../research/sources/P33.md)
- [P41 — Texas Instruments — TIDA-00349 isolated DC/DC converter](https://www.ti.com/tool/TIDA-00349) · `page_reviewed` · [local note](../research/sources/P41.md)
- [P69 — Eaton · UPS fundamentals handbook](https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-ups-fundamentals-handbook-anz.pdf) · `page_reviewed` · [local note](../research/sources/P69.md)
- [P74 — Crusoe — Abilene cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) · `page_reviewed` · [local note](../research/sources/P74.md)
- [P75 — Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) · `page_reviewed` · [local note](../research/sources/P75.md)
- [P76 — Crusoe — 2025 impact report web summary](https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report) · `page_reviewed` · [local note](../research/sources/P76.md)

<a id="d06"></a>

### Rack power and the 800 V DC transition

**Central question:** Where should voltage conversion happen as rack demand changes?

Use 800 V DC as an architecture comparison grounded in current, interfaces and deployment constraints.

**Included scope:**

- Power shelves, rack buses, converters, point-of-load regulation and auxiliary loads
- Conventional AC-to-rack conversion, sidecars and broader facility DC options
- 800 V DC and other specified voltage arrangements; product/version boundaries
- Copper, connectors, busbars, stored energy, service access and space
- Load transients, protection interfaces, brownfield and greenfield choices

**Prerequisites:** [System boundaries and quantities](#d01), [Campus and building power distribution](#d04), [Continuity, storage and protection](#d05)

**Learning objectives and assessments:**

#### Learning objective 1

Trace conversion from rack input to processor rails and distinguish whole-rack power from chip power.

**Assessment:** Label every voltage and power boundary on two supplied rack diagrams and reject a misleading per-GPU TDP calculation.

**Historical introduction coverage:** partial. `rack-conversion` — The rack changes the rules.; `low-voltage-current` — Low voltage. Enormous current.

#### Learning objective 2

Quantify how distribution voltage changes current at fixed DC power without treating conductor loss as total system efficiency.

**Assessment:** Compute currents for a declared 100 kW DC boundary at 50 V and 800 V, then state why this does not size a real conductor or establish an efficiency delta.

**Historical introduction coverage:** partial. `low-voltage-current` — Low voltage. Enormous current.

#### Learning objective 3

Compare near-rack sidecars, rack-level conversion and facility DC as distinct architectures.

**Assessment:** Place conversion, storage, protection and AC/DC boundaries for each; distinguish announced products from proposed future designs.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 4

Evaluate a rack power upgrade against connector, bus, protection, auxiliary and transient interfaces.

**Assessment:** Write an interface checklist for a synthetic higher-density rack migration, with every unknown left explicit.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 5

Explain how retrofit constraints can reverse a seemingly attractive greenfield architecture choice.

**Assessment:** Choose between two supplied migration paths using space, downtime, conversion and maintenance assumptions; show what would change the decision.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [EFB703CFC3D — Schneider Electric — PM2200 total power calculation for accuracy verification](https://productinfo.se.com/pm2200/5afc2b5546e0fb00011e5e9d/PM2200%20series%20User%20Manual/English/BM_PM2200seriesUserManual_0000074170.ditamap.xml/%24/C_VerifyingAccuracy_PowerTotCalcuation_0000034437) · `page_reviewed` · [local note](../research/sources/EFB703CFC3D.md)
- [EA7B686AF9E — NVIDIA, Partners Drive Next-Gen Efficient Gigawatt AI Factories in Buildup for Vera Rubin](https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin/) · `page_reviewed` · [local note](../research/sources/EA7B686AF9E.md)
- [EA0B6C5ED33 — Schneider Electric — Comparing UPS System Design Configurations, White Paper 75 Revision 4](https://www.se.com/us/en/download/document/SPD_SADE-5TPL8X_EN/) · `page_reviewed` · [local note](../research/sources/EA0B6C5ED33.md)
- [E836C561209 — Schneider Electric — Why Two Cords Do Not Guarantee Power Redundancy to an IT Device](https://blog.se.com/datacenter/architecture/2014/08/06/two-cords-guarantee-power-redundancy-device/) · `page_reviewed` · [local note](../research/sources/E836C561209.md)
- [P18 — OpenStax — 20.5 Alternating Current versus Direct Current (College Physics 2e)](https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current) · `page_reviewed` · [local note](../research/sources/P18.md)
- [P19 — Steven H. Low — Power System Analysis: Analytical tools and structural properties (April 7, 2025 draft)](https://netlab.caltech.edu/assets/book/PSA/Low-PSA-v20250407.pdf) · `page_reviewed` · [local note](../research/sources/P19.md)
- [P20 — Wolfspeed — Powering AI with reliable SiC-based solid-state transformers](https://assets.wolfspeed.com/uploads/2026/03/Wolfspeed_Powering_AI_with_reliable_SiC-based_solid-state_transformers_white_paper.pdf) · `page_reviewed` · [local note](../research/sources/P20.md)
- [P21 — Texas Instruments — TIDA-011012 modular solid-state transformer reference design](https://www.ti.com/tool/TIDA-011012) · `page_reviewed` · [local note](../research/sources/P21.md)
- [P22 — Huber et al. — Comparative Evaluation of MVAC–LVDC SST and Hybrid Transformer Concepts for Future Datacenters (IPEC 2022)](https://www.ams-publications.ee.ethz.ch/uploads/tx_ethpublications/1_IPEC_2022_Final_Huber.pdf) · `page_reviewed` · [local note](../research/sources/P22.md)
- [P23 — Wolfspeed — Introduction of a commercially available 10 kV SiC power MOSFET](https://www.wolfspeed.com/company/news-events/news/wolfspeed-introduces-industrys-first-commercially-available-10000v-silicon-carbide-power-mosfet/) · `page_reviewed` · [local note](../research/sources/P23.md)
- [P24 — Schneider Electric — What is UPS efficiency and how is it calculated?](https://www.se.com/us/en/faqs/FAQ000244215/) · `page_reviewed` · [local note](../research/sources/P24.md)
- [P25 — Texas Instruments — Power Loss in Switching Power Supplies](https://www.ti.com/document-viewer/lit/html/SLUAAL9) · `page_reviewed` · [local note](../research/sources/P25.md)
- [P28 — Open Compute Project — Open Rack V3 BBU Module Specification 1.4](https://www.opencompute.org/documents/open-rack-v3-bbu-module-spec-1-4-pdf) · `page_reviewed` · [local note](../research/sources/P28.md)
- [P31 — Eaton — DC-link capacitor modules](https://www.eaton.com/gb/en-gb/products/electronic-components/topics/dc-link-modules.html) · `page_reviewed` · [local note](../research/sources/P31.md)
- [P33 — Texas Instruments — Basic Calculation of a Buck Converter’s Power Stage](https://www.ti.com/lit/an/slva477b/slva477b.pdf) · `page_reviewed` · [local note](../research/sources/P33.md)
- [P43 — Hitachi Energy — Core-type transformers](https://www.hitachienergy.com/products-and-solutions/transformers/power-transformers/generator-step-up-transformers-gsu/core-type-transformers) · `page_reviewed` · [local note](../research/sources/P43.md)
- [P44 — Schneider Electric — AA and AA/FA transformer cooling](https://www.se.com/ca/en/faqs/FA102583/) · `page_reviewed` · [local note](../research/sources/P44.md)
- [P45 — Eaton — Medium-voltage solid-state transformer](https://www.eaton.com/us/en-us/catalog/medium-voltage-power-distribution-control-systems/medium-voltage-solid-state-transformer.html) · `page_reviewed` · [local note](../research/sources/P45.md)
- [P54 — OCP — Data Center Facility: Low Voltage Direct Current Power Distribution, v1.0](https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1) · `public_excerpt_reviewed` · [local note](../research/sources/P54.md)
- [P64 — NVIDIA DGX GB200/GB300 hardware guide — Power shelves](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html#power-shelves) · `page_reviewed` · [local note](../research/sources/P64.md)
- [P67 — OpenStax · Resistance and simple circuits](https://openstax.org/books/college-physics-2e/pages/20-2-ohms-law-resistance-and-simple-circuits) · `page_reviewed` · [local note](../research/sources/P67.md)
- [P69 — Eaton · UPS fundamentals handbook](https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-ups-fundamentals-handbook-anz.pdf) · `page_reviewed` · [local note](../research/sources/P69.md)

<a id="d07"></a>

### Compute, memory and the rack

**Central question:** What inside the rack determines useful performance?

Explain hardware organization only as deeply as needed to connect workload progress with infrastructure choices.

**Included scope:**

- CPU, accelerator, memory, host and accelerator interconnect roles
- Memory capacity and bandwidth, compute throughput and data movement
- Server, tray, rack and scale-up system boundaries
- Packaging and power/thermal density where they affect the facility
- Product specifications, measured performance and workload-dependent limits

**Prerequisites:** [System boundaries and quantities](#d01), [Workloads and the infrastructure brief](#d02)

**Learning objectives and assessments:**

#### Learning objective 1

Locate compute, memory and communication components within a server and rack and explain their roles.

**Assessment:** Trace a simplified data path from storage through host memory to accelerator memory and compute.

**Historical introduction coverage:** partial. `rack-conversion` — The rack changes the rules.

#### Learning objective 2

Distinguish memory-capacity, memory-bandwidth, compute and communication limits.

**Assessment:** Use supplied workload and hardware numbers to identify a plausible bottleneck and state the model's assumptions.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 3

Explain why chip count, advertised FLOPS and installed MW cannot independently establish job throughput.

**Assessment:** Compare two synthetic rack configurations with equal power envelopes but different memory and communication constraints.

**Historical introduction coverage:** partial. `useful-compute` — Watts do not measure useful work.

#### Learning objective 4

Connect server and rack organization to power, cooling, weight and maintenance interfaces.

**Assessment:** Identify the facility interface changes caused by replacing an air-cooled server row with a specified dense rack-scale system.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [P70 — Intel · CPU versus GPU](https://www.intel.com/content/www/us/en/products/docs/processors/cpu-vs-gpu.html) · `page_reviewed` · [local note](../research/sources/P70.md)
- [P71 — Intel · Memory performance in a nutshell](https://www.intel.com/content/www/us/en/developer/articles/technical/memory-performance-in-a-nutshell.html) · `page_reviewed` · [local note](../research/sources/P71.md)

<a id="d08"></a>

### Networking and interconnects

**Central question:** How do many devices make progress as one system?

Teach communication cost and topology as constraints on useful compute and physical deployment.

**Included scope:**

- Scale-up, scale-out and inter-data-center networking
- Latency, bandwidth, bisection capacity, oversubscription and congestion
- Collectives, routing and workload placement
- Ethernet and InfiniBand as architectures with implementation-specific behavior
- Copper, pluggable optics and co-packaged optics; reach, power, cabling and serviceability
- Campus fiber entrances, meet-me rooms, demarcation and carrier connections; physical route diversity

**Prerequisites:** [System boundaries and quantities](#d01), [Workloads and the infrastructure brief](#d02), [Compute, memory and the rack](#d07)

**Learning objectives and assessments:**

#### Learning objective 1

Distinguish scale-up, scale-out and wide-area communication requirements.

**Assessment:** Place communication patterns on a rack, cluster and inter-site map; trace the campus fiber handoff and identify the relevant bottleneck.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 2

Calculate an illustrative topology's endpoint ports, oversubscription and transfer-time lower bounds.

**Assessment:** Compare two small supplied topologies, including units and stated routing assumptions; identify why bandwidth alone does not predict application time.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 3

Explain how congestion, collectives and topology-aware placement affect job progress.

**Assessment:** Predict the effect of a constrained link during a collective and describe a placement or architecture alternative.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 4

Compare interconnect media and packaging choices using reach, bandwidth, power, cooling and replacement boundaries.

**Assessment:** Evaluate copper, pluggable optics and a specified CPO proposal for a declared use case without treating a roadmap as a deployed default.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 5

Trace a network failure or degraded link into workload, cabling and operational consequences.

**Assessment:** Trace a partial fabric failure or shared external fiber route into lost service; distinguish two carriers from two physically independent paths.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [P62 — Corning — Meet-Me-Room to Outside Plant Data Center Solutions](https://www.corning.com/data-center/worldwide/en/home/applications/multi-tenant-data-center/meet-me-room.html) · `page_reviewed` · [local note](../research/sources/P62.md)
- [EA3CEEB6630 — Equinix — Customer-Managed Pre-Cabling and Demarcations](https://docs.equinix.com/cross-connect/installation/xc-customer-managed-precabling/) · `page_reviewed` · [local note](../research/sources/EA3CEEB6630.md)
- [E0F361052D1 — FCC 25-21 — Physical Diversity, paragraph 63](https://docs.fcc.gov/public/attachments/FCC-25-21A1.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/E0F361052D1.md)
- [P71 — Intel · Memory performance in a nutshell](https://www.intel.com/content/www/us/en/developer/articles/technical/memory-performance-in-a-nutshell.html) · `page_reviewed` · [local note](../research/sources/P71.md)

<a id="d09"></a>

### Storage, orchestration and recovery

**Central question:** Can data and jobs reach the hardware, and can useful progress survive failures?

Connect storage and cluster software to the delivery of a usable service.

**Included scope:**

- Local, shared and object storage roles; bandwidth, latency, metadata and durability
- Dataset ingestion, checkpointing and restart paths
- Scheduling, topology-aware placement and resource isolation
- Cluster bring-up, provisioning, observability and tenant/service acceptance
- Recovery objectives, redundancy and backup as different concepts

**Prerequisites:** [System boundaries and quantities](#d01), [Workloads and the infrastructure brief](#d02), [Compute, memory and the rack](#d07), [Networking and interconnects](#d08)

**Learning objectives and assessments:**

#### Learning objective 1

Trace the dataset and checkpoint paths and distinguish capacity, throughput and metadata constraints.

**Assessment:** Calculate an idealized checkpoint transfer time from supplied sizes and effective bandwidth, then identify additional bottlenecks.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 2

Explain how checkpoint frequency, failure behavior and restart time affect completed work.

**Assessment:** Compare two explicit checkpoint policies on a synthetic timeline that includes a failure and recovery.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 3

Explain scheduling, placement, provisioning and isolation as prerequisites for usable cluster capacity.

**Assessment:** Diagnose a scenario in which hardware is healthy but jobs cannot obtain the required topology, software environment or storage access.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 4

Specify a service acceptance exercise that tests end-to-end data access, job launch, useful output and recovery.

**Assessment:** Write a reproducible test plan for a synthetic tenant without reducing acceptance to a device-count or power-on check.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [P63 — Google Cloud — Best practices for batch inference on GKE](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/machine-learning/inference/batch-inference) · `page_reviewed` · [local note](../research/sources/P63.md)
- [P71 — Intel · Memory performance in a nutshell](https://www.intel.com/content/www/us/en/developer/articles/technical/memory-performance-in-a-nutshell.html) · `page_reviewed` · [local note](../research/sources/P71.md)
- [P77 — Google — Supporting power grids with demand response](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption) · `public_excerpt_reviewed` · [local note](../research/sources/P77.md)

<a id="d10"></a>

### Chip and rack heat capture

**Central question:** How does heat leave the devices without exceeding their operating limits?

Connect local thermal constraints with airflow, coolant and rack interfaces.

**Included scope:**

- Heat generation, heat flux, thermal resistance and temperature limits
- Heat sinks, cold plates, rear-door exchangers, immersion and two-phase alternatives
- Residual air paths and containment
- Technology coolant, manifolds, quick disconnects and CDUs
- Flow, pressure drop, approach temperature, material compatibility and leak management

**Prerequisites:** [System boundaries and quantities](#d01), [Compute, memory and the rack](#d07)

**Learning objectives and assessments:**

#### Learning objective 1

Trace parallel air and liquid heat paths and explain why rack power alone does not specify local cooling difficulty.

**Assessment:** Compare two hypothetical devices with the same total heat but different heat flux or thermal resistance.

**Historical introduction coverage:** partial. `electrical-to-heat` — The watt becomes heat.; `residual-air` — This rack still needs air.

#### Learning objective 2

Calculate a single-phase heat-transport flow under stated fluid and temperature assumptions.

**Assessment:** Solve a heat/flow/temperature-rise example and explain why the result alone does not select a pump or cold plate.

**Historical introduction coverage:** partial. `liquid-heat-transport` — Heat needs a moving carrier.

#### Learning objective 3

Explain a CDU's fluid separation, heat-exchange and control functions while distinguishing loop rise from approach temperature.

**Assessment:** Draw two closed loops, label their temperature points and predict the effect of a constrained heat-exchanger interface.

**Historical introduction coverage:** partial. `heat-exchanger` — Heat crosses. Fluids stay apart.

#### Learning objective 4

Compare air, cold-plate, rear-door and immersion approaches against a declared density and service brief.

**Assessment:** Evaluate a synthetic retrofit with residual-air, fluid, pressure, access and maintenance requirements; identify missing compatibility evidence.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [EFE70308E0A — Vertiv — Deploying Liquid Cooling in the Data Center](https://prod.vertiv.cn/4a9616/globalassets/documents/white-papers/liquid-cooling/vertiv-liquidcooling-wp-en-na-sl-71113-web.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/EFE70308E0A.md)
- [P47 — ASHRAE Handbook 2024 — Cooling Towers](https://handbook.ashrae.org/Handbooks/S24/IP/s24_ch40/s24_ch40_ip.aspx) · `page_reviewed` · [local note](../research/sources/P47.md)
- [P49 — Trane — Air vs. Water Cooled Chillers](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html) · `page_reviewed` · [local note](../research/sources/P49.md)
- [P50 — Trane TRACE 3D Plus — Air Cooled Chillers](https://trace3dplus.help.trane.com/air_cooled_chillers.html) · `page_reviewed` · [local note](../research/sources/P50.md)
- [P51 — CoolIT Systems — CHx2000 Row-Based CDU for AI](https://www.coolitsystems.com/cdu-product/chx2000/) · `page_reviewed` · [local note](../research/sources/P51.md)
- [P52 — CoolIT Systems — Cooling Distribution Units](https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/) · `page_reviewed` · [local note](../research/sources/P52.md)
- [P53 — CoolIT Systems — CHx2000 launch announcement, April 15, 2025](https://www.coolitsystems.com/resources/news/coolit-systems-announces-further-breakthroughs-in-row-based-coolant-distribution-unit-performance/) · `page_reviewed` · [local note](../research/sources/P53.md)
- [P55 — NVIDIA System Management Interface — thermal slowdown, shutdown and power limits](https://docs.nvidia.com/deploy/nvidia-smi/index.html) · `page_reviewed` · [local note](../research/sources/P55.md)
- [P56 — Dell PowerEdge event guide — liquid-cooling and temperature-triggered Emergency Power Reduction](https://www.dell.com/support/manuals/en-us/poweredge-xe9780/error_event_message_guide_c/cpwrpower-configuration-event-messages?guid=guid-3683ef35-10cc-4072-b1bb-e0f44ffcc67f&lang=en-us) · `page_reviewed` · [local note](../research/sources/P56.md)
- [P57 — NVIDIA Infra Controller — Leak Detection and Handling](https://docs.nvidia.com/infra-controller/documentation/operations-day-2/leak-detection-handling) · `page_reviewed` · [local note](../research/sources/P57.md)
- [P58 — OCP — Modular Technology Cooling Systems, Revision 1](https://www.opencompute.org/documents/ocp-modular-tcs-rev-1-final-2025-pdf) · `page_reviewed` · [local note](../research/sources/P58.md)
- [P59 — Vertiv — How N+1 redundancy supports continuous data center cooling](https://www.vertiv.com/en-ca/about/news-and-events/articles/educational-articles/how-n1-redundancy-supports-continuous-data-center-cooling/) · `public_excerpt_reviewed` · [local note](../research/sources/P59.md)
- [P60 — NVIDIA — DSX Facilities Infrastructure Reference Design Overview](https://docs.nvidia.com/dsx/facilities-infra/reference-design-overview) · `public_excerpt_reviewed` · [local note](../research/sources/P60.md)
- [P72 — OpenStax · Heat](https://openstax.org/books/college-physics-2e/pages/14-1-heat) · `page_reviewed` · [local note](../research/sources/P72.md)
- [P74 — Crusoe — Abilene cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) · `page_reviewed` · [local note](../research/sources/P74.md)

<a id="d11"></a>

### Heat rejection, climate and water

**Central question:** Where does the heat finally go, and what does moving it consume?

Close the energy and water balances through facility cooling and the outdoor environment.

**Included scope:**

- Facility water loops, pumps, air handlers and thermal storage
- Dry coolers, chillers, towers and economizers as distinct systems
- Refrigeration, COP, load dependence and added compressor heat
- Dry-bulb/wet-bulb conditions, water supply, treatment and consumption
- PUE/WUE boundaries, heat reuse and environmental tradeoffs

**Prerequisites:** [System boundaries and quantities](#d01), [Chip and rack heat capture](#d10)

**Learning objectives and assessments:**

#### Learning objective 1

Distinguish dry cooling, refrigeration, evaporative rejection and economizer operating modes.

**Assessment:** Trace four reference heat paths and identify where electricity and water enter each.

**Historical introduction coverage:** partial. `outdoor-rejection` — Moving heat adds heat.

#### Learning objective 2

Close a declared chiller energy balance and calculate cooling COP with the correct numerator and denominator.

**Assessment:** Given cooling duty and compressor input, calculate COP and condenser heat; place pumps and fans at their stated boundaries.

**Historical introduction coverage:** partial. `outdoor-rejection` — Moving heat adds heat.

#### Learning objective 3

Explain how ambient conditions, supply temperatures and equipment performance constrain capacity and economizer operation.

**Assessment:** Use supplied equipment curves and weather bins to compare two operating modes without applying a universal free-cooling threshold.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 4

Compute energy and water metrics with explicit boundaries and distinguish consumption from withdrawal.

**Assessment:** Compare two scenarios over the same period using stated facility/IT energies and water accounting; explain what PUE and WUE omit.

**Historical introduction coverage:** partial. `facility-overhead` — Budget the whole facility.

#### Learning objective 5

Evaluate cooling architecture or heat reuse against climate, water, electrical capacity and receiving-load constraints.

**Assessment:** Compare a hot-weather and a water-constrained site using a supplied design brief; identify what changes the preferred choice.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [P34 — DOE — Beyond Land Leases: Harnessing Data Centers for Tribal Economic Development](https://www.energy.gov/indianenergy/beyond-land-leases-harnessing-data-centers-tribal-economic-development-webinar) · `page_reviewed` · [local note](../research/sources/P34.md)
- [P46 — National Weather Service — Dry Bulb, Wet Bulb, and Dew Point Temperatures](https://www.weather.gov/source/zhu/ZHU_Training_Page/definitions/dry_wet_bulb_definition/dry_wet_bulb.html) · `page_reviewed` · [local note](../research/sources/P46.md)
- [P47 — ASHRAE Handbook 2024 — Cooling Towers](https://handbook.ashrae.org/Handbooks/S24/IP/s24_ch40/s24_ch40_ip.aspx) · `page_reviewed` · [local note](../research/sources/P47.md)
- [P48 — Vertiv — Optimizing Chilled Water Systems, July 2024](https://www.vertiv.com/495988/globalassets/shared/vertiv-chilled-water-solution-white-paper-sl-18066.pdf) · `page_reviewed` · [local note](../research/sources/P48.md)
- [P49 — Trane — Air vs. Water Cooled Chillers](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html) · `page_reviewed` · [local note](../research/sources/P49.md)
- [P50 — Trane TRACE 3D Plus — Air Cooled Chillers](https://trace3dplus.help.trane.com/air_cooled_chillers.html) · `page_reviewed` · [local note](../research/sources/P50.md)
- [P55 — NVIDIA System Management Interface — thermal slowdown, shutdown and power limits](https://docs.nvidia.com/deploy/nvidia-smi/index.html) · `page_reviewed` · [local note](../research/sources/P55.md)
- [P56 — Dell PowerEdge event guide — liquid-cooling and temperature-triggered Emergency Power Reduction](https://www.dell.com/support/manuals/en-us/poweredge-xe9780/error_event_message_guide_c/cpwrpower-configuration-event-messages?guid=guid-3683ef35-10cc-4072-b1bb-e0f44ffcc67f&lang=en-us) · `page_reviewed` · [local note](../research/sources/P56.md)
- [P57 — NVIDIA Infra Controller — Leak Detection and Handling](https://docs.nvidia.com/infra-controller/documentation/operations-day-2/leak-detection-handling) · `page_reviewed` · [local note](../research/sources/P57.md)
- [P58 — OCP — Modular Technology Cooling Systems, Revision 1](https://www.opencompute.org/documents/ocp-modular-tcs-rev-1-final-2025-pdf) · `page_reviewed` · [local note](../research/sources/P58.md)
- [P59 — Vertiv — How N+1 redundancy supports continuous data center cooling](https://www.vertiv.com/en-ca/about/news-and-events/articles/educational-articles/how-n1-redundancy-supports-continuous-data-center-cooling/) · `public_excerpt_reviewed` · [local note](../research/sources/P59.md)
- [P60 — NVIDIA — DSX Facilities Infrastructure Reference Design Overview](https://docs.nvidia.com/dsx/facilities-infra/reference-design-overview) · `public_excerpt_reviewed` · [local note](../research/sources/P60.md)
- [P72 — OpenStax · Heat](https://openstax.org/books/college-physics-2e/pages/14-1-heat) · `page_reviewed` · [local note](../research/sources/P72.md)
- [P74 — Crusoe — Abilene cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) · `page_reviewed` · [local note](../research/sources/P74.md)

<a id="d12"></a>

### Physical site, buildings and safety

**Central question:** What must the actual place support beyond electrical and thermal ratings?

Make spatial, environmental, access and safety constraints visible before treating a schematic as buildable.

**Included scope:**

- Parcel feasibility, land control, usable acreage, geotechnical and civil conditions; buildings, structural loading and floor layouts
- Site-specific power and gas delivery, cooling/water, fiber routes, easements, title and mineral/surface rights; industrial reuse and contamination
- Flood, seismic, weather and other site hazards as jurisdiction-specific inputs
- Equipment access, lifting, replacement routes, egress and service clearances
- Fire detection/suppression, electrical hazards and battery/fuel arrangements at conceptual level
- Physical security and OT/IT trust boundaries; noise, water and environmental permits

**Prerequisites:** [System boundaries and quantities](#d01), [Siting, grid connection and supply](#d03)

**Learning objectives and assessments:**

#### Learning objective 1

Translate a reference equipment layout into space, weight, access and replacement-route requirements.

**Assessment:** Reject a synthetic layout that fits in area but fails a loading or service-access constraint. Distinguish freed rack units, occupied white/grey space and total facility footprint when equipment moves.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 2

Evaluate whether a parcel can support the required phased campus by checking usable land, utility delivery, site conditions, rights and permissions.

**Assessment:** Compare two hypothetical parcels against one capacity, area and opening-date brief. Identify the binding constraint, distinguish nearby infrastructure from deliverable service, and name the evidence that could change the choice.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 3

Explain how fire, electrical, fluid and stored-energy hazards influence layout and operating boundaries.

**Assessment:** Annotate a conceptual layout with required specialist reviews and separation/access questions without presenting it as a compliant design.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 4

Trace physical and control-system access boundaries and explain why availability depends on controlled changes and access.

**Assessment:** Identify a shared access or control dependency in a supplied facility/tenant interface diagram.

**Historical introduction coverage:** missing. No existing lesson mapped.

**Visual plan: The schematic has to fit somewhere**

- Prediction: Can a higher-density rack reduce rack count while making the existing building harder to use?
- Interaction: Switch a hall between normal operation, equipment replacement and emergency-access views; reveal footprints and clearance envelopes.
- Model boundary: Illustrative envelopes are not code-compliant dimensions. Applicable requirements depend on jurisdiction, equipment and design review.

**Worked example:** Compare two hypothetical parcels using usable acreage, dated services and land-control terms, then fit a rack and replacement route within the selected building using declared dimensions and structural limits.

**Design tradeoff:** A larger or cheaper tract can offer expansion space while losing the first phase to utility delivery, civil conditions or unresolved rights; compact layouts still need access and replacement space.

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
- [E7A716A810E — Leviton — Data center white space and gray space](https://leviton.com/support/literature/newsletters/insider/insideroctober2025/focusedproductoctober2025) · `page_reviewed` · [local note](../research/sources/E7A716A810E.md)
- [EFE70308E0A — Vertiv — Deploying Liquid Cooling in the Data Center](https://prod.vertiv.cn/4a9616/globalassets/documents/white-papers/liquid-cooling/vertiv-liquidcooling-wp-en-na-sl-71113-web.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/EFE70308E0A.md)
- [SA41 — What is So Hard About Behind-The-Meter Power For Datacenters? Part 1](https://newsletter.semianalysis.com/p/what-is-so-hard-about-behind-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA41.md)
- [P34 — DOE — Beyond Land Leases: Harnessing Data Centers for Tribal Economic Development](https://www.energy.gov/indianenergy/beyond-land-leases-harnessing-data-centers-tribal-economic-development-webinar) · `page_reviewed` · [local note](../research/sources/P34.md)
- [P35 — USDA NRCS — Understanding Soil Risks and Hazards](https://www.nrcs.usda.gov/sites/default/files/2023-01/Understanding-Soil-Risks-and-Hazards.pdf) · `page_reviewed` · [local note](../research/sources/P35.md)
- [P36 — Railroad Commission of Texas — Oil and Gas Exploration and Surface Ownership](https://www.rrc.texas.gov/about-us/faqs/oil-gas-faq/oil-gas-exploration-and-surface-ownership/) · `page_reviewed` · [local note](../research/sources/P36.md)
- [P37 — EPA — Eligible Brownfields Planning Activities](https://www.epa.gov/brownfields/eligible-planning-activities) · `page_reviewed` · [local note](../research/sources/P37.md)
- [P38 — MLGW — 2025 xAI Update](https://www.mlgw.com/images/content/files/pdf/new/xAI%202025%20Update.pdf) · `page_reviewed` · [local note](../research/sources/P38.md)
- [P39 — Energy Transfer — Q2 2026 investor presentation](https://ir.energytransfer.com/static-files/c29697db-5336-4262-8bf3-3c6e409ccb19) · `public_excerpt_reviewed` · [local note](../research/sources/P39.md)
- [P40 — DOE — CHP Technologies: Gas Turbines](https://betterbuildingssolutioncenter.energy.gov/sites/default/files/attachments/CHP_Gas_Turbines.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/P40.md)
- [P42 — Cornell Legal Information Institute — Option](https://www.law.cornell.edu/wex/option) · `page_reviewed` · [local note](../research/sources/P42.md)
- [P62 — Corning — Meet-Me-Room to Outside Plant Data Center Solutions](https://www.corning.com/data-center/worldwide/en/home/applications/multi-tenant-data-center/meet-me-room.html) · `page_reviewed` · [local note](../research/sources/P62.md)
- [E0F361052D1 — FCC 25-21 — Physical Diversity, paragraph 63](https://docs.fcc.gov/public/attachments/FCC-25-21A1.pdf) · `public_excerpt_reviewed` · [local note](../research/sources/E0F361052D1.md)
- [P73 — Crusoe — Abilene campus development update](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) · `page_reviewed` · [local note](../research/sources/P73.md)
- [P76 — Crusoe — 2025 impact report web summary](https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report) · `page_reviewed` · [local note](../research/sources/P76.md)
- [P78 — MLGW — xAI project quick facts](https://www.mlgw.com/images/content/files/pdf/2024xAI%20and%20MLGW%20Quick%20Facts%201.pdf) · `page_reviewed` · [local note](../research/sources/P78.md)
- [SA42 — SpaceX 10GW in 2027 — construction pace and equipment procurement](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) · `public_excerpt_reviewed` · [local note](../research/sources/SA42.md)

<a id="d13"></a>

### Design, procurement and commissioning

**Central question:** How does a design become a tested, usable service?

Teach delivery as a chain of interfaces and evidence, not a chronology of announcements.

**Included scope:**

- Requirements, design basis, interface ownership and change control
- Equipment lead times, factory testing, logistics and sequencing
- Construction, installation quality, fluid cleanliness and pre-functional checks
- Functional and integrated systems testing, failure scenarios and acceptance
- Phased handover, as-built records, procedures and operator training

**Prerequisites:** [Siting, grid connection and supply](#d03), [Campus and building power distribution](#d04), [Continuity, storage and protection](#d05), [Storage, orchestration and recovery](#d09), [Chip and rack heat capture](#d10), [Heat rejection, climate and water](#d11), [Physical site, buildings and safety](#d12)

**Learning objectives and assessments:**

#### Learning objective 1

Build a dependency-based delivery plan and distinguish a critical path from the longest equipment lead time.

**Assessment:** Sequence a synthetic project with parallel procurement, utility work, installation and testing; identify which delay changes service availability.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 2

Track interface requirements across vendors and design changes.

**Assessment:** Diagnose a rack/CDU or power/control interface mismatch before equipment shipment and state the acceptance evidence required.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 3

Distinguish installed, energized, individually tested, integrated-tested and service-accepted states.

**Assessment:** Classify supplied milestone evidence and identify which complete electrical, thermal and information paths remain unproven.

**Historical introduction coverage:** partial. `capacity-stages` — Connected is a milestone.; `abilene-case` — Read a real headline precisely.

#### Learning objective 4

Specify an integrated acceptance and handover plan for a phased deployment.

**Assessment:** Propose normal, failure, maintenance and recovery tests, instrumentation, acceptance criteria, records and operator handover for a synthetic phase.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [SA41 — What is So Hard About Behind-The-Meter Power For Datacenters? Part 1](https://newsletter.semianalysis.com/p/what-is-so-hard-about-behind-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA41.md)
- [P34 — DOE — Beyond Land Leases: Harnessing Data Centers for Tribal Economic Development](https://www.energy.gov/indianenergy/beyond-land-leases-harnessing-data-centers-tribal-economic-development-webinar) · `page_reviewed` · [local note](../research/sources/P34.md)
- [P37 — EPA — Eligible Brownfields Planning Activities](https://www.epa.gov/brownfields/eligible-planning-activities) · `page_reviewed` · [local note](../research/sources/P37.md)
- [P38 — MLGW — 2025 xAI Update](https://www.mlgw.com/images/content/files/pdf/new/xAI%202025%20Update.pdf) · `page_reviewed` · [local note](../research/sources/P38.md)
- [P39 — Energy Transfer — Q2 2026 investor presentation](https://ir.energytransfer.com/static-files/c29697db-5336-4262-8bf3-3c6e409ccb19) · `public_excerpt_reviewed` · [local note](../research/sources/P39.md)
- [P55 — NVIDIA System Management Interface — thermal slowdown, shutdown and power limits](https://docs.nvidia.com/deploy/nvidia-smi/index.html) · `page_reviewed` · [local note](../research/sources/P55.md)
- [P56 — Dell PowerEdge event guide — liquid-cooling and temperature-triggered Emergency Power Reduction](https://www.dell.com/support/manuals/en-us/poweredge-xe9780/error_event_message_guide_c/cpwrpower-configuration-event-messages?guid=guid-3683ef35-10cc-4072-b1bb-e0f44ffcc67f&lang=en-us) · `page_reviewed` · [local note](../research/sources/P56.md)
- [P57 — NVIDIA Infra Controller — Leak Detection and Handling](https://docs.nvidia.com/infra-controller/documentation/operations-day-2/leak-detection-handling) · `page_reviewed` · [local note](../research/sources/P57.md)
- [P58 — OCP — Modular Technology Cooling Systems, Revision 1](https://www.opencompute.org/documents/ocp-modular-tcs-rev-1-final-2025-pdf) · `page_reviewed` · [local note](../research/sources/P58.md)
- [P59 — Vertiv — How N+1 redundancy supports continuous data center cooling](https://www.vertiv.com/en-ca/about/news-and-events/articles/educational-articles/how-n1-redundancy-supports-continuous-data-center-cooling/) · `public_excerpt_reviewed` · [local note](../research/sources/P59.md)
- [SA42 — SpaceX 10GW in 2027 — construction pace and equipment procurement](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) · `public_excerpt_reviewed` · [local note](../research/sources/SA42.md)

<a id="d14"></a>

### Controls, operations and reliability

**Central question:** How does the system remain within its limits after handover?

Turn the static design into monitored operation, maintenance and incident recovery.

**Included scope:**

- Electrical, building, cooling and cluster monitoring; meters, sensors and control loops
- Setpoints, sequences, alarms, telemetry quality and control dependencies
- Maintenance, procedures, staffing, change/configuration management and spares
- Failure domains, common causes, service availability and incident learning
- Workload load changes, capacity management, aging and retrofit operations

**Prerequisites:** [Continuity, storage and protection](#d05), [Storage, orchestration and recovery](#d09), [Heat rejection, climate and water](#d11), [Physical site, buildings and safety](#d12), [Design, procurement and commissioning](#d13)

**Learning objectives and assessments:**

#### Learning objective 1

Place sensors and meters so an operator can distinguish an actual constraint from missing or misleading telemetry.

**Assessment:** Diagnose a synthetic thermal alarm using a labeled trend set; state where additional measurements are needed.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 2

Explain the difference between a device controller, a facility sequence and workload scheduling.

**Assessment:** Trace a supplied setpoint or load change through these layers and identify the required coordination and limits.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 3

Evaluate maintainability using a procedure, surviving capacity and real isolation boundaries.

**Assessment:** Walk through a synthetic maintenance plan and identify the shared dependency or restoration step that threatens service.

**Historical introduction coverage:** partial. `redundant-paths` — A second path must be useful.; `fault-domains` — Keep one fault from spreading.

#### Learning objective 4

Distinguish component reliability, topology claims and measured service availability.

**Assessment:** Critique a naive multiplication of component availabilities and specify which correlated failures and repair assumptions are missing.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 5

Convert a failure or capacity incident into an evidence-based recovery and prevention plan.

**Assessment:** Reconstruct a supplied incident timeline, separate observations from hypotheses, and propose a verification step for each corrective action.

**Historical introduction coverage:** missing. No existing lesson mapped.

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
- [EE53DCAF5E1 — Uptime Institute — Myths and Misconceptions Regarding the Tier Certification System](https://journal.uptimeinstitute.com/myths-and-misconceptions-regarding-the-uptime-institutes-tier-certification-system/) · `public_excerpt_reviewed` · [local note](../research/sources/EE53DCAF5E1.md)
- [P75 — Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) · `page_reviewed` · [local note](../research/sources/P75.md)

<a id="d15"></a>

### Capacity, cost and system decisions

**Central question:** Which constraint limits useful service, and which change is worth making?

Combine engineering, delivery and workload models into a bounded decision with explicit uncertainty.

**Included scope:**

- Capacity ledgers, bottlenecks, reserves and phased expansion
- Capital and operating costs, ownership/lease boundaries and commercial commitments
- Energy, hardware utilization, financing assumptions and time to service
- Cost per useful workload outcome versus cost per MW or GPU-hour
- Sensitivity, scenarios, uncertainty, retrofit and retirement

**Prerequisites:** [Workloads and the infrastructure brief](#d02), [Campus and building power distribution](#d04), [Rack power and the 800 V DC transition](#d06), [Networking and interconnects](#d08), [Storage, orchestration and recovery](#d09), [Heat rejection, climate and water](#d11), [Design, procurement and commissioning](#d13), [Controls, operations and reliability](#d14)

**Learning objectives and assessments:**

#### Learning objective 1

Reconcile electrical, thermal, spatial, network and commissioned-service limits using the same boundaries.

**Assessment:** Calculate a synthetic capacity ceiling and identify tied constraints without treating it as measured operating demand.

**Historical introduction coverage:** partial. `capacity-bottleneck` — The smallest limit wins.; `facility-overhead` — Budget the whole facility.

#### Learning objective 2

Build an auditable cost model that separates capital, energy, operations, ownership and financing assumptions.

**Assessment:** Compare two supplied ownership or service models over an explicit horizon with a consistent denominator and utilization scenario.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 3

Explain why cost per MW, per installed accelerator and per useful result answer different questions.

**Assessment:** Recalculate a scenario after changing throughput or utilization while leaving installed capacity constant.

**Historical introduction coverage:** partial. `useful-compute` — Watts do not measure useful work.

#### Learning objective 4

Evaluate an upgrade using sensitivity to delivery date, service output, efficiency and constraints.

**Assessment:** Choose a synthetic power, cooling or network investment and identify the assumptions that reverse its ranking.

**Historical introduction coverage:** missing. No existing lesson mapped.

#### Learning objective 5

Audit a named project's public evidence without filling unknown capacity, topology or economics with generic assumptions.

**Assessment:** Produce a dated case ledger separating announced, designed, permitted, commissioned and observed facts; list unresolved questions.

**Historical introduction coverage:** partial. `abilene-case` — Read a real headline precisely.

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
- [SA41 — What is So Hard About Behind-The-Meter Power For Datacenters? Part 1](https://newsletter.semianalysis.com/p/what-is-so-hard-about-behind-the) · `public_excerpt_reviewed` · [local note](../research/sources/SA41.md)
- [P61 — The Green Grid — PUE: A Comprehensive Examination of the Metric](https://datacenters.lbl.gov/sites/default/files/WP49-PUE%20A%20Comprehensive%20Examination%20of%20the%20Metric_v6.pdf) · `page_reviewed` · [local note](../research/sources/P61.md)
- [P73 — Crusoe — Abilene campus development update](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) · `page_reviewed` · [local note](../research/sources/P73.md)
- [P75 — Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) · `page_reviewed` · [local note](../research/sources/P75.md)

## Paths through the system

### Power → rack

[System boundaries and quantities](#d01) → [Siting, grid connection and supply](#d03) → [Campus and building power distribution](#d04) → [Continuity, storage and protection](#d05) → [Rack power and the 800 V DC transition](#d06) → [Compute, memory and the rack](#d07)

Physical electrical journey. This is a conceptual path, not a universal installed topology.

### Chip → environment

[Compute, memory and the rack](#d07) → [Chip and rack heat capture](#d10) → [Heat rejection, climate and water](#d11)

Thermal journey, including parallel air/liquid paths and auxiliary heat inputs.

### Workload → useful service

[Workloads and the infrastructure brief](#d02) → [Compute, memory and the rack](#d07) → [Networking and interconnects](#d08) → [Storage, orchestration and recovery](#d09) → [Controls, operations and reliability](#d14) → [Capacity, cost and system decisions](#d15)

Information and service dependencies, not a literal packet route.

### Site → service → upgrade

[Workloads and the infrastructure brief](#d02) → [Siting, grid connection and supply](#d03) → [Physical site, buildings and safety](#d12) → [Campus and building power distribution](#d04) → [Design, procurement and commissioning](#d13) → [Controls, operations and reliability](#d14) → [Capacity, cost and system decisions](#d15)

A lifecycle view across domains. Design and procurement iterate; this is not a strict construction schedule.

## Proposed capstones

### C01 — Grid interruption with a thermal dependency

A utility interruption occurs in a hypothetical facility. IT storage support and cooling/control supply paths are specified separately.

Domains: [Campus and building power distribution](#d04), [Continuity, storage and protection](#d05), [Chip and rack heat capture](#d10), [Heat rejection, climate and water](#d11), [Controls, operations and reliability](#d14)

**Deliverable:** An annotated topology, discrete failure timeline, energy and power budgets, and a list of missing thermal evidence.

**Assessment:** Find the unsupported auxiliary path; distinguish what is electrically sustained from what can continue delivering service. Do not invent a thermal ride-through time.

### C02 — Hot weather under a fixed site power limit

Ambient conditions move across supplied cooling performance curves while the site electrical limit remains fixed.

Domains: [System boundaries and quantities](#d01), [Chip and rack heat capture](#d10), [Heat rejection, climate and water](#d11), [Controls, operations and reliability](#d14), [Capacity, cost and system decisions](#d15)

**Deliverable:** A before/after power and heat balance with binding constraints and a stated operating response.

**Assessment:** Account for changed cooling capacity and auxiliary draw separately; explain why an annual PUE is not an instantaneous plant model.

### C03 — A denser rack in an existing building

Compare a higher-density rack migration using the existing AC plant, a sidecar option and a separately specified broader DC alternative.

Domains: [Campus and building power distribution](#d04), [Continuity, storage and protection](#d05), [Rack power and the 800 V DC transition](#d06), [Compute, memory and the rack](#d07), [Chip and rack heat capture](#d10), [Physical site, buildings and safety](#d12), [Design, procurement and commissioning](#d13), [Capacity, cost and system decisions](#d15)

**Deliverable:** Interface matrix, conversion diagrams, current and heat-flow calculations, floor/service-access review, migration sequence and scenario cost comparison.

**Assessment:** Identify retained upstream constraints and new interfaces; separate reference specifications, roadmap claims and hypothetical assumptions.

### C04 — A powered cluster that misses its job target

The hardware has adequate power and cooling, but a synthetic workload suffers fabric congestion and checkpoint stalls.

Domains: [Workloads and the infrastructure brief](#d02), [Compute, memory and the rack](#d07), [Networking and interconnects](#d08), [Storage, orchestration and recovery](#d09), [Controls, operations and reliability](#d14), [Capacity, cost and system decisions](#d15)

**Deliverable:** Work/wait/recovery timeline, a bounded bottleneck calculation, and an experiment that distinguishes competing causes.

**Assessment:** Use evidence to distinguish a communication/storage constraint from a compute shortfall; do not infer output from MW.

### C05 — Open one phase of a campus

An illustrative project has utility service, some installed racks and uneven subsystem completion. A separate named-site exercise uses only dated public evidence.

Domains: [Siting, grid connection and supply](#d03), [Campus and building power distribution](#d04), [Continuity, storage and protection](#d05), [Storage, orchestration and recovery](#d09), [Heat rejection, climate and water](#d11), [Physical site, buildings and safety](#d12), [Design, procurement and commissioning](#d13), [Controls, operations and reliability](#d14), [Capacity, cost and system decisions](#d15)

**Deliverable:** Capacity-state ledger, dependency schedule, integrated acceptance plan and unresolved-evidence list.

**Assessment:** Count only complete, accepted service paths for the synthetic brief; leave the named site's unestablished commissioning and demand values unknown.

## Historical introduction reuse

Every lesson in the retained 22-lesson introduction has a reuse location. These historical mappings do not describe the current authored course or establish completion.

| Introduction lesson | Objectives |
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
