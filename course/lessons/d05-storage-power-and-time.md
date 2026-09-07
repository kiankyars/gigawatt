# A battery has two limits before it has a runtime

**D05 · Authored draft · Objectives:** D05.1, D05.2

Calculate output energy after usable-capacity and reserve assumptions, screen discharge power separately, and distinguish a UPS role from a generic storage inventory.

**Driving question:** Can the stored energy reach the load at the required rate?

## Separate the energy inventory from the delivery path

A storage system needs both an energy inventory and a way to deliver that energy. The inventory determines how much can be supplied over time. The power-conversion path determines how quickly it can be supplied under the stated conditions. Two systems with the same MWh can therefore support entirely different loads. A large reservoir behind a narrow outlet is a useful analogy only for this distinction; actual batteries and converters have electrical, thermal, control, and protection limits that the analogy does not capture.

Runtime begins by defining usable energy at a particular boundary. A nameplate may describe a stored-energy quantity under stated test conditions. The available energy at the start of an event depends on the actual state, operating limits, aging, temperature, and reserved inventory. Conversion then changes how much reaches the load. If the supplied energy figure is already usable output energy, do not apply the same discharge loss again. The calculation must identify which losses are inside its input.

A UPS is a continuity architecture, not merely a synonym for a battery. Public vendor descriptions distinguish protected-load UPS behavior from conventional site-level storage used for energy management. The differences include connection, controls, response, and purpose. Storage that can discharge for an hour is not thereby proven to provide no-break support to a sensitive load. Conversely, a short-duration UPS may be excellent at its intended bridging job without solving a multi-hour energy shortage.

## Solve one reserve-aware runtime

Consider two hypothetical storage systems. Each begins with a stated 1.0 MWh energy inventory. The scenario permits an 80 percent usable operating window, leaving 0.8 MWh within that window. A policy then reserves 0.2 MWh at the battery-output accounting boundary. The energy available for this event is 0.8 − 0.2 = 0.6 MWh before the specified output conversion loss. This sequence avoids treating the reserve as both a fraction and another unannounced reduction.

Assume the event discharge conversion is 95 percent efficient. Deliverable energy at the protected-load boundary is 0.6 × 0.95 = 0.57 MWh. A constant 6 MW protected load would use that in 0.57/6 = 0.095 hours. Multiply by sixty to obtain 5.7 minutes. The units show why the formula works: MWh divided by MW leaves hours. This is a bounded energy estimate under our assumptions, not a guaranteed product runtime.

System A can deliver 8 MW at the stated output boundary. It passes the 6 MW power screen, so the energy calculation is relevant. System B can deliver only 4 MW. It cannot support the full 6 MW load even though its energy inventory is identical. Calling System B a 5.7-minute solution would confuse a stored quantity with a deliverable service. Its shortfall begins immediately in the simplified steady power screen.

Now add 0.3 MW of cooling and control auxiliaries to the protected scope. Total protected demand becomes 6.3 MW. System A still passes the power screen, but runtime falls to 0.57/6.3 × 60, approximately 5.43 minutes. System B still fails. The arithmetic demonstrates why naming the protected loads matters before sizing storage: preserving servers while omitting the equipment needed to keep them usable can produce a misleading continuity claim.

## Reserve policy has an opportunity cost

The 0.2 MWh reserve is a deliberate operating choice in this example. Removing it would increase event energy to 0.8 × 0.95 = 0.76 MWh and extend the 6 MW estimate to 7.6 minutes. That does not prove the reserve should be removed. It may exist for another event, uncertainty, battery operating policy, or a service obligation. A tradeoff should make the purpose visible so the same energy is not promised to multiple uses at once.

Load shape also matters. For a changing protected demand, calculate energy interval by interval and check the power limit at every relevant interval. A short higher-power phase can fail the power screen while barely changing total energy. A lower sustained phase can fit the converter but exhaust the inventory. Neither the maximum MW nor the total MWh alone describes both problems.

A successful transfer to another supply ends the battery's bridging interval only if the other supply has actually become acceptable to the protected system. Generator start, stabilization, load acceptance, transfer behavior, and auxiliary restoration are system events with their own evidence. No generic runtime formula supplies those timings. Use an explicit timeline and compare the required output energy through that interval with the available energy.

Finally, do not claim complete recovery when the load merely returns to its normal source. The store may be depleted and require recharge before it can support a second event. Recharging competes for electrical capacity and may have its own rate limit. A continuity promise therefore needs the starting state, the supported event, and the restored readiness condition. The next lesson follows that event across electricity and cooling rather than stopping at the battery icon.

## Worked example: Same MWh, different deliverable service

- Starting stated inventory is 1.0 MWh for both systems.
- Usable window is 80%; reserve is 0.2 MWh before 95% output conversion.
- Protected real load is constant at 6 MW.

1. Operating-window energy — 1.0 × 0.80 = 0.8 MWh — Apply the declared usable window once.
2. Event energy before conversion — 0.8 − 0.2 = 0.6 MWh — Subtract the explicitly located reserve.
3. Usable load energy — 0.6 × 0.95 = 0.57 MWh — Conversion loss reduces energy reaching the protected load.
4. Power screen — A: 8 MW ≥ 6 MW; B: 4 MW < 6 MW — Only System A can support the stated full load.
5. Energy-limited duration for A — 0.57 / 6 × 60 = 5.7 minutes — The estimate applies after the power screen passes.

**Result:** System A has a 5.7-minute scenario energy budget; System B fails the full-load power requirement.

**Model boundary:** The example supplies usable-window, reserve, and efficiency inputs; it does not infer battery chemistry behavior or no-break transfer performance.

## The tradeoff

Choice: Reserve more stored energy for a second purpose or uncertainty.

Benefit: The system retains explicitly protected energy for that need.

Cost: Less energy remains available for the current outage interval.

## When the situation changes

Trigger: Use an MWh label to claim support for a load above the converter output rating.

Mechanism: The required delivery rate exceeds the available path even before energy is exhausted.

Response: Check the output MW limit and the complete protected scope before calculating runtime.

## Apply the idea

System A must support 6.3 MW including auxiliaries. How long does 0.57 MWh of usable output last?

<details>
<summary>Reveal the worked answer</summary>

About 5.43 minutes.

0.57/6.3 hours multiplied by 60 gives 5.4286 minutes. Do not multiply by 95 percent again, because that loss was already applied.

</details>

**The idea to keep:** Check deliverable power first; divide only the appropriately defined usable energy by the complete protected load.

## Sources and reading boundaries

- [EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) — Runtime follows energy divided by power when a constant output load is specified. Read 2026-09-06. Read the public power/energy unit definitions. Battery-window and reserve values are original assumptions.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — UPS and conventional behind-the-meter storage have different typical architecture roles. Read 2026-09-06. Read the public landing-page explanation only; the downloadable full white paper and product performance curves were not reviewed.
