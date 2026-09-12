# A battery has two limits before it has a runtime

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d05-storage-power-and-time`, then run `uv run gigawatt-expand`.

**7. Continuity, storage and protection · Authored draft**

Calculate output energy after usable-capacity and reserve assumptions, screen discharge power separately, and distinguish a UPS role from a generic storage inventory.

**Driving question:** Can the stored energy reach the load at the required rate?

## Separate the energy inventory from the delivery path

A storage system needs both an energy inventory and a way to deliver that energy. The inventory determines how much can be supplied over time. The power-conversion path determines how quickly it can be supplied under the stated conditions. Two systems with the same MWh can therefore support entirely different loads. A large reservoir behind a narrow outlet is a useful analogy only for this distinction; actual batteries and converters have electrical, thermal, control, and protection limits that the analogy does not capture.

Runtime begins by defining usable energy at a particular boundary. A nameplate may describe a stored-energy quantity under stated test conditions. The available energy at the start of an event depends on the actual state, operating limits, aging, temperature, and reserved inventory. Conversion then changes how much reaches the load. If the supplied energy figure is already usable output energy, do not apply the same discharge loss again. The calculation must identify which losses are inside its input.

A UPS is a continuity architecture, not merely a synonym for a battery. Public vendor descriptions distinguish protected-load UPS behavior from conventional site-level storage used for energy management. The differences include connection, controls, response, and purpose. Storage that can discharge for an hour is not thereby proven to provide no-break support to a sensitive load. Conversely, a short-duration UPS may be excellent at its intended bridging job without solving a multi-hour energy shortage.

## Zero transfer time still needs a fast energy buffer

An online UPS in double-conversion mode already supplies the load through its inverter. Losing the rectifier input does not require switching the load onto a newly started inverter. Zero transfer time describes that output continuity, not instantaneous internal current changes. The battery interface may be a direct DC connection or a controlled DC/DC converter, depending on the equipment; an isolated DC/DC converter may contain a high-frequency transformer.

DC-link capacitors remain useful in online operation. They supply and absorb rapid current differences, smooth switching ripple and support bus voltage while the rectifier or battery path responds. Batteries sustain the longer energy demand. Offline or line-interactive transfer gaps are another reason for load-side hold-up, not the only reason capacitors exist. Capacitors in the UPS DC link and capacitors on a separate rack DC bus occupy different boundaries.

For a separate, hypothetical 800 V rack bus, take an effective 0.20 F capacitance directly across the bus, a constant 1 MW bus load and a 700 V converter shutdown threshold. Assume the converters stay regulated down to that threshold and that no other source contributes. Usable energy is ½ × 0.20 × (800² − 700²) = 15,000 J. Hold-up is 15,000 J / 1,000,000 W = 0.015 s, or 15 ms. At 700 V the bank still stores 49,000 J; that energy is below the permitted operating range. These are chosen teaching values, not specifications of the pictured UPS.

This 15 ms is capacitor-only hold-up, not a UPS transfer time. The load is defined at the DC bus, so do not count downstream converter losses twice; if instead 1 MW were useful downstream output, bus power would include those losses. Once a battery or other source contributes, capacitor energy supplies only the remaining power deficit. More generally, the time integral of P_load − P_source equals the energy withdrawn from the capacitor. The ideal calculation ignores capacitance variation, ESR, wiring resistance and inductance; those affect actual voltage excursions and usable hold-up.

Now allow the battery contribution at that same bus to rise linearly from zero to 1 MW during the first 10 ms. This assumed ramp starts at time zero; it does not wait for the 15 ms capacitor-only limit. The battery supplies 5 kJ and the capacitor supplies the other 5 kJ during those 10 ms. The capacitor deficit is the area of a triangle: ½ × 1 MW × 0.010 s = 5 kJ. Bus voltage reaches √(800² − 2 × 5,000/0.20) = 768.1 V, above the 700 V cutoff.

From 10 ms onward the battery supplies the full 1 MW, so the capacitor no longer loses energy in this ideal model. Its voltage does not automatically return to 800 V: recharge requires power above the ongoing load. The UPS presenter sequence teaches both cases directly in the “Capacitor buffer” scene. Its 10 ms ramp is an assumed comparison, not a measurement of the photographed UPS.

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

## Case study: solar and second-life batteries in Sparks

The solar example is Crusoe and Redwood Materials at Sparks, Nevada. Crusoe’s May 2026 summary specifies 12 MW of solar and 63 MWh of repurposed EV battery capacity. These quantities answer different questions: generation capability and stored energy.

For an original ideal example, assume a full usable 63 MWh store, a constant 3 MW total load, no solar input, no reserve and no conversion loss. Energy alone would last 21 hours. At 6 MW it would last 10.5 hours, only if the delivery path could supply 6 MW. Actual runtime needs usable energy, discharge limits, state of charge, auxiliaries and the weather/load time series. Neither quotient is a measured Sparks runtime.

Crusoe’s March 2026 update reports 99.2% microgrid availability over seven months and 99.9% Cloud availability using grid backup. Pause: does that mean 99.2% of electricity came from solar? No. Availability measures time meeting a service definition; solar share measures energy from a source. An hourly supply ledger is needed to answer the latter. The grid-backup disclosure also prevents describing this operating account as entirely off-grid.

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
- [Eaton — DC-link capacitor modules](https://www.eaton.com/gb/en-gb/products/electronic-components/topics/dc-link-modules.html) — Locate DC-link capacitors between rectifier and inverter; explain voltage buffering, ripple and rapid load transitions. Read 2026-09-11. Reviewed the opening functional explanation and UPS application listing. Listed product values do not specify the course UPS or the hypothetical 0.20 F bus.
- [Eaton — Choosing the optimal UPS topology](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/choosing-the-optimal-ups-topology-.html) — Distinguish zero output transfer time in online double-conversion operation from standby and line-interactive transfers. Read 2026-09-11. Reviewed topology and Online UPS sections. Zero transfer time is not a guarantee of zero internal transient or an equipment-specific battery-interface response time.
- [Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) — Teach solar, storage and grid backup at Sparks, Nevada; distinguish microgrid availability from Cloud availability and energy share. Read 2026-09-12. Main release reviewed. Company reports 99.2% microgrid availability over seven months and 99.9% Cloud availability using grid backup. Expansion to 24 modular data centers is announced, not confirmed complete. Do not carry forward the initial off-grid description as present status.
- [Crusoe — 2025 impact report web summary](https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report) — Names 12 MW of solar and 63 MWh of repurposed EV battery capacity for the Redwood project; describes original Abilene phase as greenfield. Read 2026-09-12. Selected web sections reviewed, not the linked full report. Equipment ratings are not measured continuous output or usable battery energy. Company-wide renewable procurement claims cannot establish hourly matching at every campus.
