# Behind the meter and the first usable megawatt

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d03-service-and-siting`, then run `uv run gigawatt-expand`.

**4. Siting, grid connection and supply · Authored draft**

Locate the customer meter, calculate grid import and an islanded supply deficit, then combine those limits with a phased site schedule.

**Driving question:** Can behind-the-meter supply bring a site online sooner and keep its protected load running during an outage?

## A connection is a process, not a single number

A large-load project begins with an intended service requirement and a proposed physical location. The utility or system operator needs enough information to assess how that load connects and behaves. Studies, agreements, network upgrades, equipment delivery, construction, and operational authorization can all stand between the initial request and available service. Their exact names and sequence differ by jurisdiction and project. A generic course diagram must not be mistaken for the current application procedure of a particular utility.

ERCOT's June 2026 announcement of a batch-study approach provides a dated example of why this matters: multiple large projects must be assessed together against the network they would share. The lesson is not to memorize that announcement's process as universal. It is to recognize that requested capacity can interact with other projects and required grid work. A customer's desired date is an input to planning, not evidence that the grid can deliver the requested load on that date.

Inside the property, additional dependencies continue. Electrical equipment can be energized while cooling, control integration, network connections, or IT acceptance remains incomplete. Commissioning checks behavior for the stated scope; operation then supplies evidence of actual service. A phased campus may therefore have several statuses at once. Keep a ledger for each usable block rather than attaching one completion percentage to the entire site.

## Behind the meter describes a boundary, not independence

Behind-the-meter (BTM) generation or storage is electrically on the customer side of the utility meter used for the comparison. Draw that meter between the grid and the customer bus, then connect the local generator, storage, and site loads to the customer bus. Several meters may exist on a real campus, so state which one defines the claim. A property fence, equipment owner, or nearby power plant does not by itself establish this electrical arrangement.

Keep three descriptions separate. On-site describes physical location. Behind the meter describes the electrical relationship to the stated utility meter. Islanded describes operation while disconnected from the wider grid; off-grid can describe a site operated without a utility connection. An off-site power purchase agreement (PPA) is a commercial supply arrangement. It does not move that generator inside the customer boundary or demonstrate that it can supply this campus after the grid path is lost.

Use one original, simplified boundary at Site B. The customer bus supplies 8 MW, including the declared cooling, controls, and downstream losses. A local generator delivers 6 MW net to that bus, and storage is idle. Neglect losses between the meter and this bus. Grid import is 8 − 6 = 2 MW. Over one hour the site uses 8 MWh, supplied by 6 MWh locally and 2 MWh through the meter. Reduced purchased electricity is not an efficiency gain: the site still requires 8 MW, and producing the local 6 MW also consumes its declared fuel or other energy resource.

Now change only local generation to 10 MW with the same 8 MW load and idle storage. The signed grid balance is 8 − 10 = −2 MW: the negative sign describes a proposed 2 MW export. That operating point requires an export-capable, authorized arrangement. If export is unavailable, the proposed state must change, for example through permitted generation reduction or charging within the storage limits. At exactly 8 MW of generation, zero net import would still not tell you whether the grid connection is open.

Finally remove grid support from the original 8 MW load and 6 MW generation case. A suitably designed island must replace the missing 2 MW and maintain a stable supply. The BTM label alone supplies neither function. DOE’s microgrid explanation shows why coordinated controls and equipment matter, and why some local solar systems disconnect during a grid outage. The following duration calculation assumes that an authorized island mode is already established; it does not calculate transfer time or prove seamless continuity.

## Gas turbines turn combustion heat into shaft work

In a simple-cycle gas turbine, air is compressed, fuel burns in that compressed air, and the resulting hot gas expands through turbine blades. Shaft work drives both the compressor and an electric generator. A starter can initially turn the machine; an electric motor is not the continuing source of its output. This gas-turbine process is represented by the Brayton cycle. Open cycle describes intake from the atmosphere and discharge of exhaust; it is not a synonym for peak-only operation.

A combined-cycle plant directs exhaust through a heat recovery steam generator (HRSG). Heat crosses into a separate water/steam circuit; the exhaust gas does not turn into steam. Steam expands through a steam turbine to produce additional shaft work. A condenser rejects heat and returns the steam to liquid, and a pump returns that water to the HRSG. This steam loop is represented by the Rankine cycle. No supplementary firing is assumed in our diagram.

## Compare fuel at equal net output

Take two hypothetical plant options, each delivering 100 MW net electric output. At 40% net efficiency, simple cycle requires 100/0.40 = 250 MW of thermal fuel input. At 60%, combined cycle requires 166.7 MW. The respective remainders are 150 MW and 66.7 MW of unrecovered energy on this simplified lower-heating-value (LHV) balance. Neither percentage is a product rating or a Dania Beach measurement. Keep fuel heating-value convention and net-versus-gross output consistent.

This comparison holds delivered output fixed across two plant options. It does not say that adding a steam cycle to an unchanged gas turbine leaves its total output fixed. Recovering exhaust heat can increase total output from that installation. The added HRSG, steam turbine, condenser, water and cooling systems also add construction, capital, maintenance and operating dependencies. GE Vernova’s 2025 catalog identifies the simpler capital and construction profile of simple cycle alongside its lower efficiency. The real schedule still depends on equipment delivery, fuel, permits and site works.

## A real combined-cycle plant: Dania Beach

GE Vernova’s public case describes two 7HA.03 gas turbines at FPL’s Dania Beach Clean Energy Center near Fort Lauderdale and reports plant output up to 1,260 MW. Its photograph is embedded in the presentation so that the learner can see the physical installation. The reported plant output is not two standalone gas-turbine nameplates added together. This is a grid plant example; no supply relationship to our reference AI campus is asserted.

A separate May 2025 GE Vernova fact sheet lists its 7HA.03 1×1 combined-cycle design at 640 MW net and 63.9% LHV efficiency. It separately lists less than 30 minutes for a rapid-response hot start, a 75 MW/min ramp rate and a 26% minimum load. Conditions are net plant, ISO reference conditions and natural gas fuel. These catalog values are not Dania Beach operating measurements. A cold-start duration cannot be inferred from the hot-start entry.

## Baseload, intermediate duty and peaking are service roles

Baseload is the demand floor present through the stated interval. Intermediate or mid-merit duty covers longer periods above that floor, while peaking duty covers shorter intervals of high demand. EIA describes combined cycle serving base and intermediate loads and simple-cycle turbines commonly supplying peaks. These are typical uses, not exclusive identities. Combined cycle can follow load. Engines, storage and other resources can also provide peaking service.

In the presentation’s hypothetical shared grid, an assumed 100 MW contribution runs throughout the day. Combined cycle serves the next 120 MW and simple-cycle peaking up to 80 MW. Baseline demand peaks at 260 MW. Add a constant 50 MW campus without adding capacity: the peak becomes 310 MW, exceeding the assumed fully available 300 MW by 10 MW. A steady AI load uses headroom during the grid’s hardest hour as well as its quietest hour.

The plot deliberately omits startup and ramp limits, minimum operating output, reserves, outages, network limits and renewable variability. It isolates the hourly capacity account. Starting a machine from its stated thermal condition, increasing the output of a running machine and constructing a new plant are three different timescales. A feasible operational or procurement plan must establish each relevant one, not substitute a single fast-start claim for all three.

## Why simple cycle can win despite burning more fuel

Use a deliberately bounded annual-cost comparison, not a current equipment quote. Both options have 100 MW net capacity and the earlier assumed efficiencies of 40% and 60%. Assign simple cycle $8 million per year in annualized fixed costs and combined cycle $16 million; these supplied totals stand for annualized capital and fixed operating costs. At $20 per MWh of fuel energy on an LHV basis, fuel costs are $50 and $33.33 per MWh of electricity.

Annual cost in this model is fixed cost plus 100 MW × equivalent full-load hours × fuel cost per MWh electric. At 500 hours, the simple-cycle option costs $10.50 million versus $17.67 million. At 7,000 hours, the combined-cycle option costs $39.33 million versus $43.00 million. The crossover is 4,800 equivalent full-load hours: the additional $8 million of fixed cost is then exactly offset by fuel savings. Equivalent full-load hours mean annual MWh divided by the 100 MW rating, not necessarily literal hours spent at maximum output.

The lesson is the change in decision with utilization. Start costs, variable maintenance, emissions prices, part-load performance, downtime and project-specific financing are excluded. Construction speed, delivered fuel, water/cooling and service requirements can reject either option before this cost comparison becomes relevant. Predict the lower-cost option at 500 versus 7,000 hours, then identify what additional evidence would establish that it can actually supply the campus. A generator’s efficiency does not establish islanding, redundancy or customer-service availability.

## Find the last required dependency, then the usable limit

Compare two hypothetical sites for a service that requires power, a finished building, cooling, and fiber. At Site A, the supplied readiness dates are months 18, 22, 21, and 20 respectively. At Site B, they are months 20, 19, 20, and 21. Under the explicit assumption that these dates represent accepted readiness and all other requirements are satisfied, Site A cannot supply the complete service before month 22; Site B cannot before month 21.

The calculation is a maximum, not an average. Averaging Site A's four dates gives 20.25, but there is no useful 20.25-month service if its required building is unavailable until month 22. The maximum identifies the last necessary dependency. These are supplied scenario dates rather than a forecast of an actual project. If the dates are only expected installation dates, additional acceptance and commissioning work must remain on the schedule.

Capacity uses a different operation. Suppose Site B eventually has a 12 MW facility service rating. Return to the 8 MW protected load and 6 MW net generator output at the same customer bus. With the grid available and storage idle, import was 2 MW. In the assumed supported island mode, grid import becomes zero and storage must now supply that same 2 MW deficit. If storage has 4 MWh usable output and a 3 MW output rating at this bus, its power screen passes but its energy lasts only 4/2 = 2 hours. The 12 MW utility service rating contributes nothing while that connection is unavailable.

Add the supplied fuel constraint: the generator can operate for four hours at its assumed 6 MW output before fuel replenishment is required. The battery deficit reaches its limit sooner, after two hours. If the protected load were reduced to 6 MW, the battery deficit would disappear in this steady simplified interval, but generator fuel would still limit duration. This comparison assumes the generator is already stable; starting and transfer behavior require a separate timeline.

## Treat siting requirements as coupled constraints

Land, fiber, climate, water, electrical service, equipment access, and local requirements influence one another. A site with earlier grid availability may need a cooling solution that changes auxiliary power and delivery time. A location with low energy prices may impose a workload latency disadvantage or a difficult expansion path. A single weighted score can be useful for preferences, but it should not average away a hard requirement that the site fails.

Separate requirements into conditions that must pass and tradeoffs among feasible options. If an application needs a maximum network round-trip time, a location outside that envelope may be unsuitable regardless of its lower cost. If a cooling design depends on a water allocation that has not been established, that is unresolved evidence rather than zero cost. List the missing fact and the party or document that could establish it.

On-site supply can reduce grid import for a fixed site load and may help an earlier phase become feasible. In the 8 MW example, a proposed interim 2 MW import limit would cover the normal remainder only while the local 6 MW is available. If that generator stops and storage remains idle, the requested import becomes 8 MW. The proposal must address that changed state through an established supply or load-management plan; the generator nameplate alone has not solved the grid-capacity problem. Fuel, maintenance, controls, emissions, connection requirements, and the generator’s net output under actual conditions remain dependencies.

The final choice should state a complete service envelope: how much load, beginning when, under which normal and degraded conditions, and with which remaining uncertainties. This converts a location comparison into an infrastructure decision. It also identifies where further work has the greatest value: the dependency controlling the delivery date, the capacity limiting accepted load, or the operating condition that breaks the proposed service promise.

## Our recurring campus: Abilene

Abilene, Texas is the recurring real campus reference in this course. We follow the original Crusoe-built Stargate campus across service, construction, cooling and operating evidence. Each real claim retains a source date. Calculators use clearly stated teaching assumptions whenever the public record does not supply matching inputs; their results are not Abilene measurements.

Crusoe’s March 27, 2026 update separates the original campus from a new adjacent Microsoft development. Two original 100 MW buildings were energized; six further buildings were expected by year-end. The adjacent 900 MW development targeted initial energization in mid-2027. Ask which building and which milestone a number describes before combining capacities.

## Worked example: The same 8 MW load before and after grid support is lost

- All readiness dates are supplied accepted-readiness assumptions; the 12 MW service rating is a capacity limit, not the actual load.
- The customer bus supplies 8 MW including stated auxiliaries and downstream losses; losses between this bus and the utility meter are neglected.
- The generator delivers 6 MW net to the bus; storage has 4 MWh usable output and a 3 MW output limit at that bus.
- Grid-connected storage is idle; the island calculation starts after stable, authorized island operation has been established. Startup and transfer are excluded.
- The generator has four hours of fuel at its stated 6 MW output.

1. Site A ready — max(18, 22, 21, 20) = month 22 — The service waits for its last necessary subsystem.
2. Site B ready — max(20, 19, 20, 21) = month 21 — Earlier grid readiness alone does not choose the earlier complete site.
3. Grid-connected import — 8 MW load − 6 MW generation = 2 MW from the grid — The meter sees the remainder; the customer load has not become 2 MW.
4. Supported island — 6 MW generation + 2 MW storage + 0 MW grid = 8 MW load — The same deficit moves from the grid to storage only under the stated island-capability assumption.
5. Storage duration — 4 MWh / 2 MW = 2 h — The 3 MW storage output rating exceeds the 2 MW deficit; usable energy binds first.

**Result:** Site B is ready earlier under the supplied schedule. Its 8 MW load imports 2 MW when grid-connected; the assumed island lasts two hours before usable storage energy is exhausted.

**Model boundary:** These are planning scenarios, not project forecasts, field operating procedures, or proof of local operating authorization.

## The tradeoff

Choice: Add on-site supply to reduce dependence on a particular utility-service condition.

Benefit: It can support a specifically designed alternative supply mode.

Cost: Fuel, controls, maintenance, environmental requirements, and usable capacity introduce additional dependencies.

## When the situation changes

Trigger: Treat the earliest energized subsystem as a completed site.

Mechanism: A later building, cooling, fiber, or acceptance dependency prevents the intended service.

Response: Track complete blocks and keep readiness, commissioning, and observed operation as separate evidence states.

## Apply the idea

In the assumed supported island, the 8 MW load sheds 1 MW. How long can the same generator and storage sustain it? Would an off-site 6 MW PPA alone support that calculation after the grid path is lost?

<details>
<summary>Reveal the worked answer</summary>

Four hours with the stated local generator and storage. An off-site PPA alone does not establish the required island supply.

The remaining 7 MW load needs 1 MW from storage, so 4/1 = 4 h, equal to the supplied generator fuel duration. The calculation assumes the generator can deliver inside this island; a purchase contract does not establish that electrical path. Starting, transfers, and the service consequences of shedding remain separate.

</details>

**The idea to keep:** Behind the meter names an electrical location. Usable capacity, grid exchange, and island operation each need their own demonstrated conditions.

## Sources and reading boundaries

- [ERCOT — Batch Zero large-load connection announcement, June 18, 2026](https://www.ercot.com/news/release/06182026-puct-approves-ercots) — Large-load connection studies consider shared network capacity and required upgrades. Read 2026-09-06. Read the dated June 18, 2026 ERCOT announcement; do not treat its process or thresholds as universal or permanent.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Commissioning and handover can occur in smaller infrastructure blocks with documented acceptance. Read 2026-09-06. Read the public framework discussion; all dates and capacity ledgers here are synthetic.
- [DOE — Islanding a Microgrid](https://www.energy.gov/cmei/femp/articles/islanding-microgrid) — Grid-connected and islanded operation require a coordinated system of sources and loads. Read 2026-09-10. Reviewed the public animation transcript, including coordinated source operation and loss of grid support. The example assumes an established island and does not reproduce its switching sequence or assess a real plant.
- [NARUC — Regulators’ Financial Toolbox: Behind-the-Meter Energy Storage](https://pubs.naruc.org/pub/6233DBE2-B58B-52FF-925E-250DD26DECF9) — Behind-the-meter describes the customer side of the utility meter; it can include resources that exchange power with the grid. Read 2026-09-10. Reviewed the BTM/FTM definition and diagram on printed pages 2–3. The lesson generalizes the electrical-boundary distinction to its stated generator-and-storage example; no tariff benefit or export permission is assumed.
- [DOE — Solar Integration: Distributed Energy Resources and Microgrids Basics](https://www.energy.gov/cmei/systems/solar-integration-distributed-energy-resources-and-microgrids-basics) — Local generation and designed island operation are distinct; many solar systems disconnect during loss of the wider grid. Read 2026-09-10. Reviewed Distributed Energy Resources and Islands and Microgrids. The course does not assume that a data-center generator, inverter, or campus inherits island capability from location or nameplate alone.
- [US EPA — Physical PPA](https://www.epa.gov/green-power-markets/physical-ppa) — A physical PPA is a purchase arrangement that may involve on-site or off-site generation; an off-site project can deliver through the grid. Read 2026-09-10. Reviewed What is a Physical Power Purchase Agreement? and How Do Physical PPAs Work? Contract structure does not establish a dedicated electrical path or island supply for the example.
- [Crusoe — Abilene campus development update](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) — Separate the original Abilene campus from the adjacent Microsoft development; distinguish energized buildings from future capacity. Read 2026-09-12. Main announcement reviewed. Dated company account: two original 100 MW buildings energized; six more expected by end-2026; adjacent 900 MW project targets first energization in mid-2027. These are not September 2026 metered loads.
- [GE Vernova — How a combined-cycle plant produces electricity](https://www.gevernova.com/gas-power/resources/education/combined-cycle-power-plants) — Gas turbine shaft work, exhaust heat recovery in an HRSG, and steam-turbine electricity production. Read 2026-09-12. Read the three mechanism steps. Course paths are conceptual and omit supplementary firing; no site output, net efficiency or startup guarantee follows.
- [EIA — Natural gas generation by technology and region](https://www.eia.gov/todayinenergy/detail.php?id=61444) — Combined-cycle generation serves base and intermediate duty; simple-cycle gas turbines commonly cover shorter peak periods. Read 2026-09-12. Read technology, operating-role and heat-rate sections, published 22 February 2024. Fleet statistics are historical and no universal dispatch order or capacity guarantee is adopted.
- [GE Vernova — 7HA gas-turbine and combined-cycle fact sheet](https://www.gevernova.com/content/dam/gepower-new/global/en_US/downloads/gas-new-site/products/gas-turbines/7ha-fact-sheet-product-specifications.pdf) — 7HA.03 1×1 combined-cycle catalog: 640 MW net, 63.9% LHV efficiency, <30 min rapid-response hot start, 75 MW/min ramp and 26% minimum load. Read 2026-09-12. Complete one-page May 2025 fact sheet reviewed, including net-plant ISO/natural-gas conditions and hot-start footnote. Separate maxima/limits are not assumed simultaneous. No cold-start time or actual campus performance inferred.
- [GE Vernova — First 7HA.03 commercial operation at FPL Dania Beach](https://www.gevernova.com/gas-power/resources/case-studies/first-7ha-florida-power-light) — Reported real plant example: two 7HA.03 gas turbines and up to 1,260 MW at Dania Beach; original manufacturer plant photograph. Read 2026-09-12. Public case text and hero photograph reviewed. No published date shown. Manufacturer-reported plant capacity is not current measured output, and no relationship to a data-center campus is claimed. Marketing emissions and savings claims are not adopted.
- [GE Vernova — 2025 Gas Power Catalog, plant configuration comparison](https://www.gevernova.com/content/dam/gepower-new/global/en_US/downloads/noindexpdf/GEA35241-GE-Vernova-Gas-Power-Catalog.pdf) — Simple-cycle construction and capital simplicity versus combined-cycle efficiency and additional steam-cycle equipment. Read 2026-09-12. Downloaded official PDF and read the plant-configuration comparison on printed page 28. Qualitative manufacturer comparison, not site-specific pricing or guaranteed lead times; numerical annual-cost examples are original assumptions.

## Check your understanding: Can this phase open?

Pause and make a prediction, then compare your reasoning.

A hypothetical project has an energy contract covering its planned annual consumption. Its first phase needs 10 MW at the facility connection, but the available connection is limited to 8 MW. No local generation or storage is included.

**Pause and predict:** Does the energy contract make the full first phase deliverable? Explain the constraint.

<details>
<summary>Compare your reasoning</summary>

No. The stated connection leaves a 2 MW shortfall at the required boundary.

Commercial energy coverage does not increase the physical connection limit. The project needs an evidenced route to more deliverable power or a smaller operating phase. Matching annual energy also says nothing by itself about supply during each operating hour.

</details>

**The next problem:** Power is one site condition. Can the parcel, building, access routes and other services support the same phase?

Continue in **Physical site, buildings and safety**: A rack must fit on its worst day.
