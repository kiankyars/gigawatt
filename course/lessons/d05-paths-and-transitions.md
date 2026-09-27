# Continuity belongs to the complete service

**7. Continuity, storage and protection**

Follow a given electrical and thermal restoration timeline, calculate its energy requirement, and test redundancy under a second unavailable component.

**Driving question:** Which loads remain usable during an interruption, transfer, and maintenance event?

## Follow one timeline across electrical and thermal paths

Begin with a protected system drawing 5 MW for IT, 0.4 MW for circulation pumps, and 0.1 MW for controls. Its total uninterruptible power supply (UPS) output is 5.5 MW. The outdoor heat-rejection plant is on a separately described supply path. At time zero, utility power becomes unavailable. The scenario states that the UPS maintains its connected loads, the generator is ready at 30 seconds, and acceptable generator power reaches the UPS input and outdoor plant at 45 seconds.

The electrical bridge therefore lasts 45 seconds. At 5.5 MW it requires 5.5 × 45/3,600 = 0.06875 MWh, or 68.75 kWh, of usable UPS output energy. If the store has 120 kWh available at that boundary and adequate output power, it passes this energy screen. The claimed continuity still depends on the given transfer behavior actually being valid for the hardware and loads; the arithmetic does not manufacture that behavior.

The thermal timeline continues. Suppose the plant sequence reaches adequate heat rejection only at 90 seconds. Pumps and controls remained powered, but that alone does not prove sufficient heat removal during the interval. Heat may be stored in coolant, equipment, and other material; thermal capacity and temperature margins need their own model. We can identify a 90-second interval requiring thermal evidence without inventing how long the IT can remain within its temperature limits.

After power returns, include restoration and recharge. A store that spent 68.75 kWh cannot immediately promise its original 120 kWh reserve for another event. A successful first transfer and a ready-for-next-event state are different milestones. The system's operating policy must define when full support is again available and what restrictions apply in between.

## Count the capacity that survives the selected event

Now study redundancy separately from the timeline. Redundancy notation counts installed modules against N, the number the load needs. Take a 100 kW protected load and UPS modules that each deliver 50 kW, so N is two modules. N+1 installs three, 150 kW in all: one module can be unavailable and 100 kW remains.

Take one module of that N+1 system out for planned maintenance. The two remaining modules still provide 100 kW. If another module then fails, only 50 kW remains, half the load. N+1 covers one unavailable module, and maintenance plus a failure is two. N+2 installs four modules and covers exactly that pair of events, because two healthy modules still supply 100 kW. In these single-path arrangements every spare shares the same output bus, so a failed common bus stops all of them together. The event being tested must state what is already unavailable, what subsequently fails and what output is required.

2N builds two complete paths, A and B, each with two modules, so either path alone can carry the whole 100 kW. Isolate path A for maintenance and then fail a module on path B, and only 50 kW remains: the load is no longer fully supported. 2(N+1) puts three modules on each path, so with path A isolated and one B module failed, path B still delivers 100 kW. The extra module on each path is what keeps a failure survivable during maintenance.

A second complete path gives a full-capacity alternative route, and its independence is a separate question. If both paths require the same upstream bus, fuel support, control system, or sole cooling interface, that shared dependency may defeat the intended service. Two colors and two power cords cannot prove two independent complete systems.

The load interface matters too. A dual-input device must be able to maintain the required output under the specified surviving-feed condition and transition. Some arrangements share demand across inputs; capacity in normal operation is not automatically the capacity available after one input is lost. The system must demonstrate compatible behavior at the actual required load, not merely show that two connectors exist.

A/B power supply unit (PSU) groups each rated to support a 100 kW load do not force 200 kW into that load. They may share the 100 kW in normal operation; either surviving group must have enough capacity to carry it after the other path is lost. The redundancy comparison counts available capacity, while actual consumption follows the load and conversion losses.

N depends on the load it is counted against. If demand grows from 100 to 150 kW, N becomes three modules, and the three modules installed as N+1 are now exactly N. Growth has consumed the spare without any change to the equipment, so every redundancy label needs its current load written beside it.

## Capacity, maintainability, and fault response answer different questions

Capacity asks whether the remaining equipment can carry the load. Maintainability asks whether selected equipment can be removed from service for planned work while the promised service continues. Fault tolerance asks what happens when a defined unplanned event occurs. These questions overlap but are not identical. A path may have spare capacity but no compatible route around equipment being maintained. A system may tolerate a planned transition while responding differently to an abrupt fault.

Uptime's public Tier descriptions distinguish maintainability and fault-tolerance requirements and include electrical and cooling behavior. A certification claim requires the applicable criteria and assessment of the actual infrastructure. The useful transferable skill is to remove a specified element on paper, trace valid routes, and state which additional evidence is needed before asserting continuity.

There is an economic and operating tradeoff in greater path separation. Additional independent equipment can reduce exposure to a common failure and improve maintenance options, but adds cost, footprint, interfaces, and maintenance obligations. If both nominally independent paths share a neglected dependency, that extra investment may not buy the intended behavior. Spend analytical effort on the complete dependency graph before counting the spare modules.

Return to the 45-second electrical bridge and 90-second thermal interval. Passing the UPS energy screen answers one question. Passing the surviving-module capacity screen answers another. Neither proves that cooling is continuously adequate or that a second event is supported before recharge. A strong continuity explanation keeps these answers separate and then combines only the conclusions that the evidence actually supports.

## What each Uptime Tier adds

Uptime Institute tiers describe what the site infrastructure can withstand. Tier I supplies basic power and cooling. Tier II adds spare capacity components. Tier III permits planned maintenance of equipment and distribution paths while IT remains operating. Tier IV adds tolerance of an unplanned infrastructure fault, including continuous cooling. Tier IV has the most demanding infrastructure requirements in this four-level system; the appropriate investment depends on the service the facility must support.

All four Uptime Tiers include an engine generator for extended utility outages. Tier I already includes this backup source, and higher tiers retain it while adding redundancy and fault protection. For Tier III and IV, the generator plant must support critical load without runtime limits in its applicable capacity rating. Fuel supply and operating permissions still limit endurance; the rating does not require the generator to run continuously. This is a requirement of the Uptime classification, not a claim that every data center follows that classification.

Component counts such as N+1 or 2N do not decide a Tier. The complete design and its response to events matter. Tier III proves planned maintenance can occur without shutting down IT; it does not make Tier IV's additional promise about unplanned faults. Neither certification assigns an annual downtime percentage. Uptime removed expected-downtime assignments in 2009.

## Three, four and five nines in published examples

A number of nines needs a named boundary and evidence type. An operator may report a service result, publish a design capability, or promise a service level agreement (SLA). These are useful examples to compare, but they are not a league table of measured site reliability.

**Three nines — Crusoe Spark, Sparks, Nevada.** Crusoe's March 2026 update says its Cloud maintains 99.9% availability using the grid as backup at the Redwood Materials deployment. The microgrid itself reported 99.2% over seven months. Grid backup helps separate the power source's availability from the Cloud service's availability. The release does not give a separate observation window for the 99.9% Cloud figure.

**Four nines — Microsoft Fairwater Atlanta.** In November 2025, Microsoft described this graphics processing unit (GPU) power design as capable of 99.99% availability at the cost of a three-nines design. This is a design claim tied to highly available utility power; Microsoft did not publish a year of measured outages or a site SLA with the announcement.

**Five nines — NTT DATA Vienna 1.** The facility fact sheet advertises 99.999% power uptime in its service level agreement. It also specifies separate A/B UPS systems with 2N redundancy and N+1 diesel generation. The percentage describes the power SLA, not the availability of every application hosted there. The fact sheet does not give the contract's measurement window or exclusions.

For a common mathematical reference, counting every minute of a 365-day year gives 8 h 45 min 36 s of downtime at 99.9%, 52 min 33.6 s at 99.99%, and 5 min 15.36 s at 99.999%. Those durations are annual equivalents, not the stated contract periods or measured performance of these three examples.

## Fairwater Atlanta: choose backup around the power supply and service

Microsoft chose the Atlanta site for resilient utility power. Its November 2025 description says the GPU fleet can forgo traditional on-site generation, UPS systems and dual-corded distribution, reducing cost and time to market. The same article discusses on-site energy storage for smoothing power fluctuations; the passage does not provide a complete installed-equipment inventory.

The decision is concrete: how much additional local backup does this GPU service need beyond the reliability available from its utility connection? A different utility supply or a service with a different interruption tolerance can justify a different investment. This Fairwater design is not presented as an Uptime Tier certification. It therefore does not contradict the generator requirement within the four Uptime Tiers.

Microsoft does not supply a quantified capital-cost comparison or a measured annual availability record in that announcement. The case shows the chosen architecture and the operator's rationale. It does not prove that omitting backup achieves the same result at another site.

## Microsoft on power oscillations

> We have also worked with our industry partners to codevelop power-management solutions to mitigate power oscillations created by large scale jobs, a growing challenge in maintaining grid stability as AI demand scales. This includes a software-driven solution that introduces supplementary workloads during periods of reduced activity, a hardware-driven solution where the GPUs enforce their own power thresholds and an on-site energy storage solution to further mask power fluctuations without utilizing excess power.

Scott Guthrie, Microsoft, 12 November 2025, in “Infinite scale: The architecture behind the Azure AI superfactory.” The passage appears in the Fairwater design discussion immediately after the Atlanta power paragraph. It describes three power-management approaches; it does not show that all three were commissioned at Atlanta or deployed throughout Azure. The final phrase is Microsoft’s wording; real energy storage still has conversion losses.

## Trace a powered rack with a failed service dependency

Take a separate qualitative scenario: utility power fails, and the generator starts and supplies the cooling plant. Compute racks have UPS and generator support; pumps and heat rejection have generator support; cooling controls have only utility power. The remaining dependency is the unpowered cooling controls. In this case the workload cannot continue merely because its racks still receive electricity.

A protected supply for the controls addresses that missing path. Cooling restart behavior and thermal margin still need checking. This short check gives no transfer times or thermal ride-through duration; the earlier numerical timeline is a separate, explicitly assumed example.

## Check bypass after an inverter failure

Suppose the inverter has failed and forced static bypass supplies the load from utility AC. The battery is charged, but its route to the AC load still requires the failed inverter. If the utility source now fails, neither the inverter path nor the bypass source can supply the load. The load therefore does not ride through in this scenario.

A generator may restore acceptable bypass power after startup and transfer; it does not bridge the intervening interruption. This check assumes no other operating supply path. It also differs from a requested bypass mode with a healthy inverter: Schneider’s Easy UPS manual distinguishes those operating states, so the word bypass alone does not tell you the available battery support.

## Maintenance bypass takes the whole UPS out of the path

Static bypass is an electronic path inside the UPS. Maintenance bypass is a separate, manually closed route that carries the load around the UPS so the UPS can be isolated and serviced. In Schneider Electric’s Easy UPS 3-Phase Modular manual, closing the external maintenance bypass disconnect lets service and replacement be performed on the entire UPS, while the load receives unconditioned power straight from the bypass source.

That access costs the stored-energy protection. The same manual states that the batteries are not available as an alternate power source in maintenance bypass. A 100 kW load fed this way therefore drops if the bypass source is lost, because no surviving route remains. A second complete path, as in 2N, lets one UPS be isolated for maintenance while the other keeps battery-backed support for the load.

## Worked example: An electrical bridge with an unresolved thermal interval

- Protected UPS output is 5.0 + 0.4 + 0.1 = 5.5 MW.
- The given electrical transition completes at 45 seconds.
- Usable UPS output energy is 120 kWh; outdoor heat rejection is restored at 90 seconds.

1. Protected demand — 5.0 + 0.4 + 0.1 = 5.5 MW — Include IT, circulation pumps, and controls at the same output boundary.
2. Bridge energy — 5.5 × 45 / 3,600 = 0.06875 MWh — Convert the given bridge duration to hours.
3. Remaining energy — 120 − 68.75 = 51.25 kWh — This is the remaining stated output-energy inventory after the first bridge.
4. Maximum constant-load energy interval — 0.120 / 5.5 × 3,600 ≈ 78.55 s — This energy ceiling does not prove thermal continuity or transfer compatibility.

**Result:** The 45-second bridge fits the stated energy inventory; the 90-second thermal interval remains an independent unresolved requirement.

**Model boundary:** All sequence times are assumed behavior, not generator or cooling product specifications.

## When the situation changes

Trigger: One module of the three-module N+1 system is maintained, and another then fails.

Mechanism: Only one 50 kW module remains, half the 100 kW load.

Response: State the supported degraded service, or add capacity such as N+2 or 2(N+1), which covers maintenance plus a failure.

## Apply the idea

If electrical transfer takes 100 seconds instead of 45, how much UPS output energy is required, and does 120 kWh suffice?

<details>
<summary>Reveal the worked answer</summary>

About 152.78 kWh is needed; 120 kWh is short by 32.78 kWh.

5.5 × 100 / 3,600 MWh equals 0.15278 MWh. The separate thermal and transfer questions still require evidence even if more energy is added.

</details>

**The idea to keep:** A surviving power path needs enough capacity, compatible transfer behavior, and the auxiliaries required to keep the service usable.

## Sources

- [Tier Classification System](https://uptimeinstitute.com/tiers) — Uptime Institute · Reviewed 2026-09-06. Public Tier descriptions distinguish maintainability and fault tolerance and include continuous cooling requirements at the relevant level.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — www.vertiv.com · Reviewed 2026-09-06. Critical-load continuity depends on UPS architecture and the surrounding supply system.
- [Explaining the Uptime Institute’s Tier Classification System (April 2021 Update)](https://journal.uptimeinstitute.com/explaining-uptime-institutes-tier-classification-system/) — Uptime Institute · Published 2014-09-30 · Reviewed 2026-09-12. Separates the Tier I–IV infrastructure outcomes from measured service availability; explicitly states that expected-downtime assignments were removed in 2009.
- [Tier Classification Myths and Misconceptions](https://uptimeinstitute.com/myths) — Uptime Institute · Reviewed 2026-09-12. Explains that generator plants for Tier III/IV must support the critical load without runtime limitations in their applicable capacity rating, but need not run continuously. Clarifies that utility-feed and component counts do not determine Tier.
- [Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) — Crusoe · Published 2026-03-24 · Reviewed 2026-09-12. The Sparks, Nevada microgrid combines solar, storage and grid backup; the March 2026 release reports 99.2% microgrid availability over seven months separately from 99.9% Crusoe Cloud availability.
- [Microsoft — Fairwater Atlanta availability and power design](https://blogs.microsoft.com/blog/2025/11/12/infinite-scale-the-architecture-behind-the-azure-ai-superfactory/) — Microsoft · Published 2025-11-12 · Reviewed 2026-09-16. Microsoft’s rationale for Fairwater Atlanta’s availability and backup design, including supplementary workloads, GPU power thresholds and on-site storage for power oscillations.
- [NTT DATA — Vienna 1 facility and power SLA](https://services.global.ntt/-/media/ntt/global/insights-and-resources/data-sheets/vienna-1-data-sheet.pdf?rev=9057842951194cb1b9d1cf884282f421) — NTT DATA · Published 2024 · Reviewed 2026-09-12. The Vienna 1 fact sheet advertises 99.999% power uptime under its service-level agreement, with 2N A/B UPS systems and N+1 diesel generation.
- [Schneider Electric — Easy UPS 3-Phase Modular 50–250 kW: UPS Modes](https://productinfo.se.com/easyups3pmodular/990-6537-easy-ups-3-phase-modular-50-250-kw-operation/English/990-6537%20Operation%20Easy%20UPS%203-Phase%20Modular%2050-250%20kW_0001015104.xml/%24/GalaxyPX_UPSModes_0000761714) — Schneider Electric · Reviewed 2026-09-26. Distinguishes requested static bypass, forced static bypass and internal and external maintenance bypass. Batteries are not available as an alternate source in forced static bypass or maintenance bypass, and external maintenance bypass permits service on the entire UPS while the load receives unconditioned bypass power.
