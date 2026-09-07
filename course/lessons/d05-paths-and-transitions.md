# Continuity belongs to the complete service

**D05 · Authored draft · Objectives:** D05.2, D05.3

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

## Capacity, maintainability, and fault response answer different questions

Capacity asks whether the remaining equipment can carry the load. Maintainability asks whether selected equipment can be removed from service for planned work while the promised service continues. Fault tolerance asks what happens when a defined unplanned event occurs. These questions overlap but are not identical. A path may have spare capacity but no compatible route around equipment being maintained. A system may tolerate a planned transition while responding differently to an abrupt fault.

Uptime's public Tier descriptions distinguish maintainability and fault-tolerance requirements and include electrical and cooling behavior. This lesson does not assign a Tier to our small diagrams. A certification claim requires the applicable criteria and assessment of the actual infrastructure. The useful transferable skill is to remove a specified element on paper, trace valid routes, and state which additional evidence is needed before asserting continuity.

There is an economic and operating tradeoff in greater path separation. Additional independent equipment can reduce exposure to a common failure and improve maintenance options, but adds cost, footprint, interfaces, and maintenance obligations. If both nominally independent paths share a neglected dependency, that extra investment may not buy the intended behavior. Spend analytical effort on the complete dependency graph before counting the spare modules.

Return to the 45-second electrical bridge and 90-second thermal interval. Passing the UPS energy screen answers one question. Passing the surviving-module capacity screen answers another. Neither proves that cooling is continuously adequate or that a second event is supported before recharge. A strong continuity explanation keeps these answers separate and then combines only the conclusions that the evidence actually supports.

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
