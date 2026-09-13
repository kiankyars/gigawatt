# Continuity belongs to the complete service

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d05-paths-and-transitions`, then run `uv run gigawatt-expand`.

**7. Continuity, storage and protection · Authored draft**

Follow a supplied electrical/thermal restoration timeline, calculate its energy requirement, and test redundancy under a second unavailable component.

**Driving question:** Which loads remain usable during an interruption, transfer, and maintenance event?

## Follow a supplied timeline across electrical and thermal paths

Begin with a hypothetical protected system drawing 5 MW for IT, 0.4 MW for circulation pumps, and 0.1 MW for controls. Its total UPS output is 5.5 MW. The outdoor heat-rejection plant is on a separately described supply path. At time zero, utility power becomes unavailable. The scenario states that the UPS maintains its connected loads, the generator is ready at 30 seconds, and acceptable generator power reaches the UPS input and outdoor plant at 45 seconds.

The electrical bridge therefore lasts 45 seconds. At 5.5 MW it requires 5.5 × 45/3,600 = 0.06875 MWh, or 68.75 kWh, of usable UPS output energy. If the store has 120 kWh available at that boundary and adequate output power, it passes this energy screen. The claimed continuity still depends on the supplied transfer behavior actually being valid for the hardware and loads; the arithmetic does not manufacture that behavior.

The thermal timeline continues. Suppose the supplied plant sequence reaches adequate heat rejection only at 90 seconds. Pumps and controls remained powered, but that alone does not establish sufficient heat removal during the interval. Heat may be stored in coolant, equipment, and other material; thermal capacity and temperature margins need their own model. We can identify a 90-second interval requiring thermal evidence without inventing how long the IT can remain within its temperature limits.

After power returns, include restoration and recharge. A store that spent 68.75 kWh cannot immediately promise its original 120 kWh reserve for another event. A successful first transfer and a ready-for-next-event state are different milestones. The system's operating policy must define when full support is again available and what restrictions apply in between.

## Count the capacity that survives the selected event

Now study redundancy independently of the timeline. A protected load needs 6 MW. Four identical modules can each deliver 2 MW under the stated conditions. Three modules are necessary to meet the load, so N is three modules and the fourth is the additional module in an N+1 capacity arrangement. All four provide 8 MW installed capacity. Losing one leaves 6 MW, which exactly supports the specified load in this simplified capacity account.

Take one module out for planned maintenance. The three remaining modules still provide 6 MW. If another module then becomes unavailable, only 4 MW remains. N+1 does not mean an unlimited number of failures can be absorbed during maintenance. The event being tested must state what is already unavailable, what subsequently fails, and what output is required. A changing load can also change N; the label depends on the demand being supported.

Compare two separate 6 MW routes, either of which can support the entire 6 MW load. This is a 2N capacity concept at the declared boundary. It can provide a full-capacity alternative route, but independence remains a separate question. If both routes require the same upstream bus, fuel support, control system, or sole cooling interface, that shared dependency may defeat the intended service. Two colors and two power cords cannot prove two independent complete systems.

The load interface matters too. A dual-input device must be able to maintain the required output under the specified surviving-feed condition and transition. Some arrangements share demand across inputs; capacity in normal operation is not automatically the capacity available after one input is lost. The system must demonstrate compatible behavior at the actual required load, not merely show that two connectors exist.

A/B PSU groups each rated to support a 100 kW load do not force 200 kW into that load. They may share the 100 kW in normal operation; either surviving group must have enough capacity to carry it after the other path is lost. The redundancy comparison counts available capacity, while actual consumption follows the load and conversion losses.

## Capacity, maintainability, and fault response answer different questions

Capacity asks whether the remaining equipment can carry the load. Maintainability asks whether selected equipment can be removed from service for planned work while the promised service continues. Fault tolerance asks what happens when a defined unplanned event occurs. These questions overlap but are not identical. A path may have spare capacity but no compatible route around equipment being maintained. A system may tolerate a planned transition while responding differently to an abrupt fault.

Uptime's public Tier descriptions distinguish maintainability and fault-tolerance requirements and include electrical and cooling behavior. This lesson does not assign a Tier to our small diagrams. A certification claim requires the applicable criteria and assessment of the actual infrastructure. The useful transferable skill is to remove a specified element on paper, trace valid routes, and state which additional evidence is needed before asserting continuity.

There is an economic and operating tradeoff in greater path separation. Additional independent equipment can reduce exposure to a common failure and improve maintenance options, but adds cost, footprint, interfaces, and maintenance obligations. If both nominally independent paths share a neglected dependency, that extra investment may not buy the intended behavior. Spend analytical effort on the complete dependency graph before counting the spare modules.

Return to the 45-second electrical bridge and 90-second thermal interval. Passing the UPS energy screen answers one question. Passing the surviving-module capacity screen answers another. Neither proves that cooling is continuously adequate or that a second event is supported before recharge. A strong continuity explanation keeps these answers separate and then combines only the conclusions that the evidence actually supports.

## What each Uptime Tier adds

Uptime Institute tiers describe what the site infrastructure can withstand. Tier I supplies basic power and cooling. Tier II adds spare capacity components. Tier III permits planned maintenance of equipment and distribution paths while IT remains operating. Tier IV adds tolerance of an unplanned infrastructure fault, including continuous cooling. Tier IV has the most demanding infrastructure requirements in this four-level system; the appropriate investment depends on the service the facility must support.

All four Uptime Tiers include an engine generator for extended utility outages. Tier I already includes this backup source, and higher tiers retain it while adding redundancy and fault protection. For Tier III and IV, the generator plant must support critical load without runtime limits in its applicable capacity rating. Fuel supply and operating permissions still limit endurance; the rating does not require the generator to run continuously. This is a requirement of the Uptime classification, not a claim that every data center follows that classification.

Component counts such as N+1 or 2N do not establish a Tier. The complete design and its response to events matter. Tier III proves planned maintenance can occur without shutting down IT; it does not make Tier IV's additional promise about unplanned faults. Neither certification assigns an annual downtime percentage. Uptime removed expected-downtime assignments in 2009.

## Three, four and five nines in published examples

A number of nines needs a named boundary and evidence type. An operator may report a service result, publish a design capability, or promise an SLA. These are useful examples to compare, but they are not a league table of measured site reliability.

**Three nines — Crusoe Spark, Sparks, Nevada.** Crusoe's March 2026 update says its Cloud maintains 99.9% availability using the grid as backup at the Redwood Materials deployment. The microgrid itself reported 99.2% over seven months. Grid backup helps separate the power source's availability from the Cloud service's availability. The release does not give a separate observation window for the 99.9% Cloud figure.

**Four nines — Microsoft Fairwater Atlanta.** In November 2025, Microsoft described this GPU power design as capable of 99.99% availability at the cost of a three-nines design. This is a design claim tied to highly available utility power; Microsoft did not publish a year of measured outages or a site SLA with the announcement.

**Five nines — NTT DATA Vienna 1.** The facility fact sheet advertises 99.999% power uptime in its service level agreement. It also specifies separate A/B UPS systems with 2N redundancy and N+1 diesel generation. The percentage describes the power SLA, not the availability of every application hosted there. The fact sheet does not give the contract's measurement window or exclusions.

For a common mathematical reference, counting every minute of a 365-day year gives 8 h 45 min 36 s of downtime at 99.9%, 52 min 33.6 s at 99.99%, and 5 min 15.36 s at 99.999%. Those durations are annual equivalents, not the stated contract periods or measured performance of these three examples. No verified four-nines primary claim for Abilene was established in this review.

## Fairwater Atlanta: choose backup around the power supply and service

Microsoft chose the Atlanta site for resilient utility power. Its November 2025 description says the GPU fleet can forgo traditional on-site generation, UPS systems and dual-corded distribution, reducing cost and time to market. Microsoft separately describes on-site energy storage for smoothing power fluctuations, so this is not a claim that the campus contains no batteries.

The decision is concrete: how much additional local backup does this GPU service need beyond the reliability available from its utility connection? A different utility supply or a service with a different interruption tolerance can justify a different investment. This Fairwater design is not presented as an Uptime Tier certification. It therefore does not contradict the generator requirement within the four Uptime Tiers.

Microsoft does not supply a quantified capital-cost comparison or a measured annual availability record in that announcement. The case establishes the chosen architecture and the operator's rationale. It does not prove that omitting backup achieves the same result at another site.

## Worked example: An electrical bridge with an unresolved thermal interval

- Protected UPS output is 5.0 + 0.4 + 0.1 = 5.5 MW.
- The supplied electrical transition completes at 45 seconds.
- Usable UPS output energy is 120 kWh; outdoor heat rejection is restored at 90 seconds.

1. Protected demand — 5.0 + 0.4 + 0.1 = 5.5 MW — Include IT, circulation pumps, and controls at the same output boundary.
2. Bridge energy — 5.5 × 45 / 3,600 = 0.06875 MWh — Convert the supplied bridge duration to hours.
3. Remaining energy — 120 − 68.75 = 51.25 kWh — This is the remaining stated output-energy inventory after the first bridge.
4. Maximum constant-load energy interval — 0.120 / 5.5 × 3,600 ≈ 78.55 s — This energy ceiling does not establish thermal continuity or transfer compatibility.

**Result:** The 45-second bridge fits the stated energy inventory; the 90-second thermal interval remains an independent unresolved requirement.

**Model boundary:** All sequence times are hypothetical supplied behavior, not generator or cooling product specifications.

## The tradeoff

Choice: Build greater separation between complete supply routes.

Benefit: A shared dependency can be removed and maintenance options can improve.

Cost: More equipment and interfaces require investment, space, validation, and ongoing maintenance.

## When the situation changes

Trigger: One 2 MW module is maintained and another fails in the four-module, 6 MW example.

Mechanism: Only two modules remain, providing 4 MW rather than the required 6 MW.

Response: State the supported degraded service or add a justified architecture capability; do not call the original N+1 label sufficient.

## Apply the idea

If electrical transfer takes 100 seconds instead of 45, how much UPS output energy is required, and does 120 kWh suffice?

<details>
<summary>Reveal the worked answer</summary>

About 152.78 kWh is needed; 120 kWh is short by 32.78 kWh.

5.5 × 100 / 3,600 MWh equals 0.15278 MWh. The separate thermal and transfer questions still require evidence even if more energy is added.

</details>

**The idea to keep:** A surviving power path needs enough capacity, compatible transfer behavior, and the auxiliaries required to keep the service usable.

## Sources and reading boundaries

- [Tier Classification System](https://uptimeinstitute.com/tiers) — Public Tier descriptions distinguish maintainability and fault tolerance and include continuous cooling requirements at the relevant level. Read 2026-09-06. Read the public overview only; no certification assessment or full topology standard is claimed.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — Critical-load continuity depends on UPS architecture and the surrounding supply system. Read 2026-09-06. Read the public white-paper landing page; all event timings and module capacities are synthetic.
- [Explaining the Uptime Institute’s Tier Classification System (April 2021 Update)](https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/) — Separates the Tier I–IV infrastructure outcomes from measured service availability; explicitly states that expected-downtime assignments were removed in 2009. Supports an original 365-day downtime-allowance example without mapping nines to tiers. Read 2026-09-12. Substantive publisher-indexed text reviewed, including Tier descriptions and the 2009 availability clarification; direct page requests returned 403. The full topology standard was not reviewed. Example outage durations are hypothetical, not reported performance.
- [Tier Classification Myths and Misconceptions](https://uptimeinstitute.com/myths) — Explains that generator plants for Tier III/IV must support the critical load without runtime limitations in their applicable capacity rating, but need not run continuously. Clarifies that utility-feed and component counts do not determine Tier. Read 2026-09-12. Substantive publisher-indexed text reviewed, including the 24 March 2010 generator clarification and 27 August 2009 utility/component-count clarification; direct page requests returned 403. Equipment capability is distinct from fuel endurance, operation permissions and continuous on-site generation.
- [Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) — Teach solar, storage and grid backup at Sparks, Nevada; distinguish microgrid availability from Cloud availability and energy share. Read 2026-09-12. Main release reviewed. Company reports 99.2% microgrid availability over seven months and 99.9% Cloud availability using grid backup, without separately specifying the Cloud measurement window. Expansion to 24 modular data centers is announced, not confirmed complete. These are historical operating claims, repeated in the May impact report, not a September measurement or a site power SLA.
- [Microsoft — Fairwater Atlanta availability and power design](https://blogs.microsoft.com/blog/2025/11/12/infinite-scale-the-architecture-behind-the-azure-ai-superfactory/) — Named Fairwater Atlanta case for four-nines availability at three-nines cost; relate grid reliability and GPU power architecture to backup investment and time to market. Read 2026-09-12. Operator design/capability claim, not an audited annual availability result, SLA, Tier certification or quantified cost comparison. Omits traditional on-site generation, UPS and dual-corded distribution for the GPU fleet; separate on-site energy storage still smooths power fluctuations.
- [NTT DATA — Vienna 1 facility and power SLA](https://services.global.ntt/-/media/ntt/global/insights-and-resources/data-sheets/vienna-1-data-sheet.pdf?rev=9057842951194cb1b9d1cf884282f421) — Named five-nines power SLA example at Vienna 1. Compare the contractual power boundary with Fairwater design availability and Crusoe Cloud service availability. Read 2026-09-12. PDF copyright 2024; exact publication date and contractual measurement window/exclusions not stated. Page 2 advertises 99.999% power uptime availability; this does not establish observed annual uptime or hosted application availability. Page 1 lists 2N UPS A/B and N+1 diesel generation.
