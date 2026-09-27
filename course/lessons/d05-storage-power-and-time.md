# Battery power, stored energy and runtime

**7. Continuity, storage and protection**

Calculate output energy using one declared usable-energy window, screen discharge power separately, and distinguish an uninterruptible power supply (UPS) role from a generic storage inventory.

**Driving question:** Can the stored energy reach the load at the required rate?

## Separate the energy inventory from the delivery path

A storage system needs both an energy inventory and a way to deliver that energy. The inventory determines how much can be supplied over time. The power-conversion path determines how quickly it can be supplied under the stated conditions. Two systems with the same megawatt-hours (MWh) can therefore support entirely different loads. A large reservoir behind a narrow outlet is a useful analogy only for this distinction; actual batteries and converters have electrical, thermal, control, and protection limits that the analogy does not capture.

Runtime begins by defining usable energy at a particular boundary. A nameplate may describe a stored-energy quantity under stated test conditions. The available energy at the start of an event depends on the actual state, operating limits, aging, temperature, and reserved inventory. Conversion then changes how much reaches the load. If the given energy figure is already usable output energy, do not apply the same discharge loss again. The calculation must identify which losses are inside its input.

A UPS is a continuity architecture, not merely a synonym for a battery. Public vendor descriptions distinguish protected-load UPS behavior from conventional site-level storage used for energy management. The differences include connection, controls, response, and purpose. Storage that can discharge for an hour is not thereby proven to provide no-break support to a sensitive load. Conversely, a short-duration UPS may be excellent at its intended bridging job without solving a multi-hour energy shortage.

## The UPS and its external batteries

Schneider’s Easy UPS 3-Phase Modular family includes 50–250 kW external-battery models in black and white finishes. The common cabinet is 1,991 mm high, 600 mm wide and 850 mm deep. Its power modules, bypass, control electronics and battery interface belong to the UPS; the main battery inventory is in external cabinets. DC means direct current. A rack battery backup unit (BBU) supplies a local DC power plane; it is distinct from facility UPS batteries. The DC/DC interface is a controlled conversion stage, not simply a cable connector.

![Two Schneider Electric Easy UPS 3-Phase Modular cabinets, one black and one white, each with a small display near the top of a perforated front door.](../assets/references/schneider-easy-ups-3phase-modular.jpg)

Easy UPS 3-Phase Modular in its two finishes. The photograph does not identify the model or the fitted modules. [Schneider Electric, Easy UPS 3-Phase Modular model list](https://productinfo.se.com/easyups3pmodular/viewer?docidentity=ModelList-1A71D03C&extension=xml&lang=en&manualidentity=TechnicalSpecificationsEasyUPS3-Pha-BC29F805)

## Zero transfer time still needs a fast energy buffer

An online UPS in double-conversion mode already supplies the load through its inverter. Losing the rectifier input does not require switching the load onto a newly started inverter. Zero transfer time describes that output continuity, not instantaneous internal current changes. The battery interface may be a direct DC connection or a controlled DC/DC converter, depending on the equipment; an isolated DC/DC converter may contain a high-frequency transformer.

DC-link capacitors remain useful in online operation. They supply and absorb rapid current differences, smooth switching ripple and support bus voltage while the rectifier or battery path responds. Batteries sustain the longer energy demand. Offline or line-interactive transfer gaps are another reason for load-side hold-up, not the only reason capacitors exist. Capacitors in the UPS DC link and capacitors on a separate rack DC bus occupy different boundaries.

Follow one UPS DC link through an outage. The link runs at 800 V with an effective 0.20 farad (F) of capacitance across it, and the inverter draws a constant 1 megawatt (MW) from it. Capacitance relates plate charge to voltage: Q = C × V. Here Q is charge measured in coulombs, C is capacitance measured in farads, and V is voltage. One farad means one coulomb per volt. The 0.20 F link capacitance at 800 V therefore holds a charge magnitude of 0.20 × 800 = 160 coulombs on each plate, with opposite signs. This is a stored state. Current I measures charge passing per second; P = I × V describes the rate of energy transfer. It cannot replace the capacitance equation.

For fixed capacitance, adding equal amounts of charge raises voltage by equal amounts. Charging from zero to 800 V therefore gives an average of 400 V over the charge added. Each volt is one joule per coulomb: 160 coulombs × 400 V = 64,000 joules stored. Equivalently, the voltage-versus-charge plot has a triangular area E = Q × (V/2). Substituting Q = C × V gives E = (C × V) × (V/2) = ½CV². No calculus is needed. The average is taken over charge increments, not over an arbitrary charging time. Stored energy is not necessarily the total energy consumed by the charging circuit.

Now remove the rectifier’s AC input. Let the inverter stay regulated down to a 700 V shutdown threshold, and at first let no other source contribute. Usable energy is ½ × 0.20 × (800² − 700²) = 15,000 J. Hold-up is 15,000 J / 1,000,000 W = 0.015 s, or 15 ms. At 700 V the bank still stores 49,000 J; that energy is below the permitted operating range.

This 15 ms is capacitor-only hold-up, not a UPS transfer time. The load is defined at the DC link, so do not count the inverter’s losses twice; if instead 1 MW were the inverter’s AC output, link power would include those losses. Once a battery or other source contributes, capacitor energy supplies only the remaining power deficit. The area between the load-power and source-power curves measures the energy supplied by the capacitor. The ideal calculation ignores capacitance variation, equivalent series resistance (ESR), wiring resistance and inductance; those affect actual voltage excursions and usable hold-up.

Now allow the battery contribution into that same link to rise linearly from zero to 1 MW during the first 10 ms. This assumed ramp starts at time zero; it does not wait for the 15 ms capacitor-only limit. The battery supplies 5 kJ and the capacitor supplies the other 5 kJ during those 10 ms. The capacitor deficit is the area of a triangle: ½ × 1 MW × 0.010 s = 5 kJ. Link voltage reaches √(800² − 2 × 5,000/0.20) = 768.1 V, above the 700 V cutoff.

From 10 ms onward the battery supplies the full 1 MW, so capacitor energy stops falling in this ideal model. The DC link remains at 768.1 V until a source returns the missing 5 kJ. The next section closes the energy account.

## Restore the DC link, then recharge the battery

Matching the load arrests the DC-link voltage decline. Restoring its setpoint requires replacing the capacitor energy already released. A regulated battery DC/DC interface can increase delivered current before the generator is ready. Once acceptable alternating current (AC) is available, the rectifier can regulate the link instead. Battery terminal voltage and link voltage need not be equal; directly connected battery architectures behave differently.

Write the energy account first. The missing energy is E_missing = ½C(V_target² − V_initial²). With constant source and load power at the same DC link, surplus power is P_extra = P_source − P_load, so recovery time t = E_missing / P_extra when P_extra is positive. Joules divided by watts gives seconds. Equivalently, choosing a recovery time requires P_source = P_load + E_missing/t. A source that only matches the load provides no surplus for recovery.

Continue from 768.1 V with 5 kJ missing and a constant 1 MW load. At 1.05 MW source output, the 50 kW surplus replaces 5 kJ in 100 ms. At 1.10 MW, the 100 kW surplus restores the same energy in 50 ms. Supplying only 1.00 MW leaves no recharge power. The voltage controller reduces output to the load requirement at 800 V. These times describe recovery after surplus power is available, independently of generator startup.

The voltage curve follows the same account: V(t) = √(V_initial² + 2P_extra t/C) until it reaches the target. For the unrounded initial state, stored energy rises from 59 kJ to 64 kJ. Constant surplus power therefore raises energy linearly while voltage follows a square-root curve. These curves assume constant capacitance and neglect losses; 768.1 V is rounded. The recovery clock starts when the stated surplus is available, not at the generator-start command.

Recharging the UPS battery is a separate energy account from restoring the DC-link capacitors. Generator and rectifier capacity must cover the load, allowed battery charging and losses. When Schneider’s Easy UPS detects a generator supply, it can be configured to disable or enable battery charging. The generator may therefore carry the load alone, or the load plus battery recharge.

## Apply one usable-energy window, then conversion loss

Consider two storage systems. Each begins with a stated 1.0 MWh energy inventory. The scenario permits an 80 percent usable operating window: 1.0 × 0.80 = 0.80 MWh before the specified output conversion loss. This one window already excludes the unavailable 20 percent. Do not subtract that same unavailable slice again as a separate reserve. Any additional reserve would need a distinct purpose and an explicitly stated accounting boundary; none is added here.

Assume event discharge conversion is 95 percent efficient. Deliverable energy at the protected-load boundary is 1.0 × 0.80 × 0.95 = 0.76 MWh. A constant 6 MW protected load uses that in 0.76/6 hours, or 0.76/6 × 60 = 7.6 minutes. MWh divided by MW leaves hours. This is an energy estimate under the given assumptions, not a guaranteed product runtime.

System A can deliver 8 MW at the stated output boundary. It passes the 6 MW power screen, so the energy calculation is relevant. System B can deliver only 4 MW. It cannot support the full 6 MW load even though its energy inventory is identical. Calling System B a 7.6-minute solution would confuse stored energy with deliverable service. Its shortfall begins immediately in the simplified steady power screen.

Now add 0.3 MW of cooling and control auxiliaries to the protected scope. Total protected demand becomes 6.3 MW. System A still passes the power screen, but runtime falls to 0.76/6.3 × 60 = 7.238 minutes, approximately 7.24 minutes. System B still fails. Preserving servers while omitting the equipment needed to keep them usable can produce a misleading continuity claim.

## Reserve policy has an opportunity cost

A usable-energy window can reflect operating limits and reserved inventory. State what it includes before allocating energy to another purpose. Retaining a separate reserve can support another event, uncertainty or a service obligation, but it reduces the energy available now. The 80 percent window in this example is applied once; neither its excluded 20 percent nor the 5 percent conversion loss is deducted twice.

Load shape also matters. For a changing protected demand, calculate energy interval by interval and check the power limit at every relevant interval. A short higher-power phase can fail the power screen while barely changing total energy. A lower sustained phase can fit the converter but exhaust the inventory. Neither the maximum MW nor the total MWh alone describes both problems.

A successful transfer to another supply ends the battery's bridging interval only if the other supply has actually become acceptable to the protected system. Generator start, stabilization, load acceptance, transfer behavior, and auxiliary restoration are system events with their own evidence. No generic runtime formula supplies those timings. Use an explicit timeline and compare the required output energy through that interval with the available energy.

Finally, do not claim complete recovery when the load merely returns to its normal source. The store may be depleted and require recharge before it can support a second event. Recharging competes for electrical capacity and may have its own rate limit. A continuity promise therefore needs the starting state, the supported event, and the restored readiness condition. The next lesson follows that event across electricity and cooling rather than stopping at the battery icon.

## Case study: solar and second-life batteries in Sparks

The solar example is Crusoe and Redwood Materials at Sparks, Nevada. Redwood’s 2 April 2026 introduction to Redwood Energy and Crusoe’s May 2026 impact-report summary specify 12 MW of solar and 63 MWh of repurposed electric-vehicle (EV) battery capacity. These quantities describe generation capability and stored energy. Neither is a statement of current information technology (IT) demand, total-site nameplate load or battery discharge power.

A host-published interview dated 27 July 2025 attributes a 1 MW initial deployment to Forrest Carroll, who worked in Crusoe Energy & Infrastructure Development. This is a dated participant account of the pilot’s scale. The transcript does not specify whether 1 MW is IT power or total facility load, and it is not an equipment nameplate. Later expansion announcements report no measured load to divide by.

Crusoe’s March 2026 update reports 99.2% microgrid availability over seven months and 99.9% Cloud availability using grid backup. Pause: does that mean 99.2% of electricity came from solar? No. Availability measures time meeting a service definition; solar share measures energy from a source. An hourly supply ledger is needed to answer the latter. The grid-backup disclosure also prevents describing this operating account as entirely off-grid. These are historical company-reported operating figures, not a September 2026 measurement interval or a current service guarantee. The May 2026 impact report repeats the case without giving a new measurement period.

## Compare stored energy with the reported 1 MW pilot

Use the historical reported pilot scale for an explicitly ideal comparison: 63 MWh / 1 MW = 63 hours, or 2.625 days. This is a gross energy-to-reported-load ratio, not measured or guaranteed autonomy. It assumes the whole stated inventory reaches a constant 1 MW load and that the delivery path can supply it. The 12 MW solar nameplate is not the load denominator.

Actual runtime requires usable delivered battery energy divided by the total battery-fed load, with a separate output-power check. Starting state of charge, operating window, reserves, conversion losses, auxiliaries and concurrent generation matter. If the reported 1 MW describes IT alone, cooling and electrical overhead increase the battery-fed demand. The sources cited here give no IT load, full-site load or battery discharge power for the expanded installation, so the 1 MW pilot ratio cannot describe it.

## Worked example: Same MWh, different deliverable service

- Starting stated inventory is 1.0 MWh for both systems.
- One 80% usable-energy window is followed by 95% output conversion; no additional reserve is deducted.
- Protected real load is constant at 6 MW.

1. Operating-window energy — 1.0 × 0.80 = 0.80 MWh — Apply the declared usable window once; its excluded slice is already unavailable.
2. Usable load energy — 0.80 × 0.95 = 0.76 MWh — Apply the specified conversion loss once at the protected-load boundary.
3. Power screen — A: 8 MW ≥ 6 MW; B: 4 MW < 6 MW — Only System A can support the stated full load.
4. Energy-limited duration for A — 0.76 / 6 × 60 = 7.6 minutes — The estimate applies after the power screen passes.

**Result:** System A has a 7.6-minute scenario energy budget; System B fails the full-load power requirement.

**Model boundary:** The example supplies the usable window and conversion efficiency. It does not infer battery chemistry behavior, output ratings at other conditions or no-break transfer performance.

## When the situation changes

Trigger: Use an MWh label to claim support for a load above the converter output rating.

Mechanism: The required delivery rate exceeds the available path even before energy is exhausted.

Response: Check the output MW limit and the complete protected scope before calculating runtime.

## Apply the idea

System A must support 6.3 MW including auxiliaries. How long does 0.76 MWh of usable output last?

<details>
<summary>Reveal the worked answer</summary>

About 7.24 minutes.

0.76/6.3 hours multiplied by 60 gives 7.2381 minutes. Do not apply the 80 percent window or 95 percent conversion efficiency again.

</details>

**The idea to keep:** Check deliverable power first; divide only the appropriately defined usable energy by the complete protected load.

## Sources

- [EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) — www.eia.gov · Reviewed 2026-09-06. Runtime follows energy divided by power when a constant output load is specified.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — www.vertiv.com · Reviewed 2026-09-06. UPS and conventional behind-the-meter storage have different typical architecture roles.
- [Eaton — DC-link capacitor modules](https://www.eaton.com/gb/en-gb/products/electronic-components/topics/dc-link-modules.html) — Eaton · Reviewed 2026-09-11. DC-link capacitors sit between rectifier and inverter, stabilizing bus voltage, smoothing ripple and supporting rapid load transitions.
- [Eaton — Choosing the optimal UPS topology](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/choosing-the-optimal-ups-topology-.html) — Eaton · Reviewed 2026-09-11. In online double-conversion operation the inverter supplies the load continuously, giving zero output transfer time, unlike standby and line-interactive designs.
- [Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) — Crusoe · Published 2026-03-24 · Reviewed 2026-09-12. The Sparks, Nevada microgrid combines solar, storage and grid backup; the March 2026 release reports 99.2% microgrid availability over seven months separately from 99.9% Crusoe Cloud availability.
- [Crusoe — 2025 impact report web summary](https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report) — Crusoe · Published 2026-05-28 · Reviewed 2026-09-12. Names 12 MW of solar and 63 MWh of repurposed EV battery capacity for the Redwood project; describes original Abilene phase as greenfield.
- [Crusoe 2025 Impact Report](https://media.ffycdn.net/us/crusoe/PL5TuZz5apXB9pVsd3H1.pdf) — Crusoe · Published 2026-05-28 · Reviewed 2026-09-26. Page 33 repeats the Sparks solar, storage and availability case.
- [Schneider Electric — Easy UPS 3-Phase Modular: Configure the Input Contacts](https://productinfo.se.com/easyups3pmodular/990-6537-easy-ups-3-phase-modular-50-250-kw-operation/English/990-6537%20Operation%20Easy%20UPS%203-Phase%20Modular%2050-250%20kW_0001015104.xml/%24/GalaxyPX_ConfiguretheInputContacts_0000761997) — Schneider Electric · Reviewed 2026-09-12. The detected-genset function can set battery charge power to 0% or 100%. Generator-supplied battery charging is configurable; it is not necessarily enabled in every installation.
- [Eaton — 93E UPS Generation 3 installation and operation manual, 164000301 Rev. 04](https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-93e-ups/eaton-93e-ups-20kva-30kva-generation-3-manual-p-164000301.pdf) — Eaton · Reviewed 2026-09-12. Printed pages 56–59 describe regulated rectifier output and a buck/boost battery converter. When acceptable AC returns, the rectifier resumes supplying the inverter and the battery can recharge.
- [Redwood Materials — Redwood and Crusoe expand compute to 7x scale](https://www.redwoodmaterials.com/news/redwood-and-crusoe-expand-compute-to-7x-scale/) — Redwood Materials · Published 2026-03-24 · Reviewed 2026-09-13. Announces a sevenfold expansion of Crusoe’s computing at Sparks, with an aerial photograph of the battery and modular data-center deployment.
- [Schneider Electric — Easy UPS 3-Phase Modular model list](https://productinfo.se.com/easyups3pmodular/viewer?docidentity=ModelList-1A71D03C&extension=xml&lang=en&manualidentity=TechnicalSpecificationsEasyUPS3-Pha-BC29F805) — Schneider Electric · Reviewed 2026-09-13. Named 50–250 kW external-battery models and black/white finish options.
- [Schneider Electric — Easy UPS 3-Phase Modular physical specifications](https://productinfo.se.com/easyups3pmodular/990-91580-technical-specifications-easy-ups-3-phase-modular/English/990-91580%20Technical%20Specifications%20Easy%20UPS%203-Phase%20Modular50-250%20kW%20UPS_0001011916.xml/%24/PhysicalREF_0000019941) — Schneider Electric · Reviewed 2026-09-26. Cabinet dimensions of the Easy UPS 3-Phase Modular: 1,991 mm high, 600 mm wide and 850 mm deep.
- [Redwood Materials — Introduction to Redwood Energy](https://www.redwoodmaterials.com/resources/unlocking-affordable-energy-storage-at-scale-an-introduction-to-redwood-energy/) — Redwood Materials · Published 2026-04-02 · Reviewed 2026-09-15. Its Proven at Scale case gives a 12 MW solar array and 63 MWh of repurposed batteries at the Nevada campus.
- [OpenStax — Energy Stored in Capacitors](https://openstax.org/books/college-physics-2e/pages/19-7-energy-stored-in-capacitors) — OpenStax, Rice University · Published 2022-07-13 · Reviewed 2026-09-14. Derives stored capacitor energy from the average voltage over the added charge and Q = CV.
- [Luca Pedretti — From Electrons to Intelligence: How Crusoe Powers AI with Modular, 24/7 Energy](https://lucapedretti850786.substack.com/p/c0b) — Luca Pedretti / The Pexapark Podcast · Published 2025-07-27 · Reviewed 2026-09-15. Host-published interview attributes a 1 MW initial Sparks deployment to Crusoe participant Forrest Carroll.
- [Pexapark — Podcast catalogue, Episode 19 with Forrest Carroll of Crusoe](https://pexapark.com/podcast/) — Pexapark · Published 2025-07-24 · Reviewed 2026-09-15. Lists Episode 19, with Forrest Carroll of Crusoe, dated 24 July 2025.
