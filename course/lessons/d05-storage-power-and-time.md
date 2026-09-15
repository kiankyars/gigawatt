# Battery power, stored energy and runtime

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d05-storage-power-and-time`, then run `uv run gigawatt-expand`.

**7. Continuity, storage and protection · Authored draft**

Calculate output energy using one declared usable-energy window, screen discharge power separately, and distinguish a UPS role from a generic storage inventory.

**Driving question:** Can the stored energy reach the load at the required rate?

## Separate the energy inventory from the delivery path

A storage system needs both an energy inventory and a way to deliver that energy. The inventory determines how much can be supplied over time. The power-conversion path determines how quickly it can be supplied under the stated conditions. Two systems with the same MWh can therefore support entirely different loads. A large reservoir behind a narrow outlet is a useful analogy only for this distinction; actual batteries and converters have electrical, thermal, control, and protection limits that the analogy does not capture.

Runtime begins by defining usable energy at a particular boundary. A nameplate may describe a stored-energy quantity under stated test conditions. The available energy at the start of an event depends on the actual state, operating limits, aging, temperature, and reserved inventory. Conversion then changes how much reaches the load. If the supplied energy figure is already usable output energy, do not apply the same discharge loss again. The calculation must identify which losses are inside its input.

A UPS is a continuity architecture, not merely a synonym for a battery. Public vendor descriptions distinguish protected-load UPS behavior from conventional site-level storage used for energy management. The differences include connection, controls, response, and purpose. Storage that can discharge for an hour is not thereby proven to provide no-break support to a sensitive load. Conversely, a short-duration UPS may be excellent at its intended bridging job without solving a multi-hour energy shortage.

## The UPS and its external batteries

Schneider’s Easy UPS 3-Phase Modular family includes 50–250 kW external-battery models in black and white finishes. The common cabinet is 1,991 mm high, 600 mm wide and 850 mm deep. Its power modules, bypass, control electronics and battery interface belong to the UPS; the main battery inventory is in external cabinets. The family photo does not establish the exact module count or switch configuration of either cabinet. DC means direct current. A rack BBU supplies a local DC power plane; it is distinct from facility UPS batteries. The DC/DC interface is a controlled conversion stage, not simply a cable connector.

## Zero transfer time still needs a fast energy buffer

An online UPS in double-conversion mode already supplies the load through its inverter. Losing the rectifier input does not require switching the load onto a newly started inverter. Zero transfer time describes that output continuity, not instantaneous internal current changes. The battery interface may be a direct DC connection or a controlled DC/DC converter, depending on the equipment; an isolated DC/DC converter may contain a high-frequency transformer.

DC-link capacitors remain useful in online operation. They supply and absorb rapid current differences, smooth switching ripple and support bus voltage while the rectifier or battery path responds. Batteries sustain the longer energy demand. Offline or line-interactive transfer gaps are another reason for load-side hold-up, not the only reason capacitors exist. Capacitors in the UPS DC link and capacitors on a separate rack DC bus occupy different boundaries.

Capacitance relates plate charge to voltage: Q = C × V. Here Q is charge measured in coulombs, C is capacitance measured in farads, and V is voltage. One farad means one coulomb per volt. Our 0.20 F capacitor at 800 V therefore has a charge magnitude of 0.20 × 800 = 160 coulombs on each plate, with opposite signs. This is a stored state. Current I measures charge passing per second; P = I × V describes the rate of energy transfer. It cannot replace the capacitance equation.

For fixed capacitance, adding equal amounts of charge raises voltage by equal amounts. Charging from zero to 800 V therefore gives an average of 400 V over the charge added. Each volt is one joule per coulomb: 160 coulombs × 400 V = 64,000 joules stored. Equivalently, the voltage-versus-charge plot has a triangular area E = Q × (V/2). Substituting Q = C × V gives E = (C × V) × (V/2) = ½CV². No calculus is needed. The average is taken over charge increments, not over an arbitrary charging time. Stored energy is not necessarily the total energy consumed by the charging circuit.

For a separate, hypothetical 800 V rack bus, take an effective 0.20 F capacitance directly across the bus, a constant 1 MW bus load and a 700 V converter shutdown threshold. Assume the converters stay regulated down to that threshold and that no other source contributes. Usable energy is ½ × 0.20 × (800² − 700²) = 15,000 J. Hold-up is 15,000 J / 1,000,000 W = 0.015 s, or 15 ms. At 700 V the bank still stores 49,000 J; that energy is below the permitted operating range. These are chosen teaching values, not specifications of the pictured UPS.

This 15 ms is capacitor-only hold-up, not a UPS transfer time. The load is defined at the DC bus, so do not count downstream converter losses twice; if instead 1 MW were useful downstream output, bus power would include those losses. Once a battery or other source contributes, capacitor energy supplies only the remaining power deficit. The area between the load-power and source-power curves measures the energy supplied by the capacitor. The ideal calculation ignores capacitance variation, ESR, wiring resistance and inductance; those affect actual voltage excursions and usable hold-up.

Now allow the battery contribution at that same bus to rise linearly from zero to 1 MW during the first 10 ms. This assumed ramp starts at time zero; it does not wait for the 15 ms capacitor-only limit. The battery supplies 5 kJ and the capacitor supplies the other 5 kJ during those 10 ms. The capacitor deficit is the area of a triangle: ½ × 1 MW × 0.010 s = 5 kJ. Bus voltage reaches √(800² − 2 × 5,000/0.20) = 768.1 V, above the 700 V cutoff.

From 10 ms onward the battery supplies the full 1 MW, so capacitor energy stops falling in this ideal model. The DC link remains at 768.1 V until a source returns the missing 5 kJ. The capacitor scene teaches this initial response; the following recovery scene closes the energy account.

## Restore the DC link, then recharge the battery

Matching the load arrests the DC-link voltage decline. Restoring its setpoint requires replacing the capacitor energy already released. A regulated battery DC/DC interface can increase delivered current before the generator is ready. Once acceptable AC is available, the rectifier can regulate the link instead. Battery terminal voltage and link voltage need not be equal; directly connected battery architectures behave differently.

Write the energy account before reading the recovery graph. The missing energy is E_missing = ½C(V_target² − V_initial²). With constant source and load power at the same DC bus, surplus power is P_extra = P_source − P_load, so recovery time t = E_missing / P_extra when P_extra is positive. Joules divided by watts gives seconds. Equivalently, choosing a recovery time requires P_source = P_load + E_missing/t. A source that only matches the load provides no surplus for recovery.

Continue from 768.1 V with 5 kJ missing and a constant 1 MW load. At 1.05 MW source output, the 50 kW surplus replaces 5 kJ in 100 ms. At 1.10 MW, the 100 kW surplus restores the same energy in 50 ms. Supplying only 1.00 MW leaves no recharge power. The voltage controller reduces output to the load requirement at 800 V. These times describe recovery after surplus power is available, independently of generator startup.

The voltage curve follows the same account: V(t) = √(V_initial² + 2P_extra t/C) until it reaches the target. For the unrounded initial state, stored energy rises from 59 kJ to 64 kJ. Constant surplus power therefore raises energy linearly while voltage follows a square-root curve. These curves assume constant capacitance and neglect losses; the displayed 768.1 V is rounded. The graph begins when the stipulated surplus is available, not at generator-start command.

Recharging the UPS battery is a separate energy account from restoring the DC-link capacitors. Generator and rectifier capacity must cover the load, allowed battery charging and losses. Schneider’s illustrated Easy UPS family can configure detected genset supply with charging disabled or enabled. The presentation therefore shows both generator-only supply and generator supply plus battery recharge.

## Apply one usable-energy window, then conversion loss

Consider two hypothetical storage systems. Each begins with a stated 1.0 MWh energy inventory. The scenario permits an 80 percent usable operating window: 1.0 × 0.80 = 0.80 MWh before the specified output conversion loss. This one window already excludes the unavailable 20 percent. Do not subtract that same unavailable slice again as a separate reserve. Any additional reserve would need a distinct purpose and an explicitly stated accounting boundary; none is added here.

Assume event discharge conversion is 95 percent efficient. Deliverable energy at the protected-load boundary is 1.0 × 0.80 × 0.95 = 0.76 MWh. A constant 6 MW protected load uses that in 0.76/6 hours, or 0.76/6 × 60 = 7.6 minutes. MWh divided by MW leaves hours. This is an energy estimate under the supplied assumptions, not a guaranteed product runtime.

System A can deliver 8 MW at the stated output boundary. It passes the 6 MW power screen, so the energy calculation is relevant. System B can deliver only 4 MW. It cannot support the full 6 MW load even though its energy inventory is identical. Calling System B a 7.6-minute solution would confuse stored energy with deliverable service. Its shortfall begins immediately in the simplified steady power screen.

Now add 0.3 MW of cooling and control auxiliaries to the protected scope. Total protected demand becomes 6.3 MW. System A still passes the power screen, but runtime falls to 0.76/6.3 × 60 = 7.238 minutes, approximately 7.24 minutes. System B still fails. Preserving servers while omitting the equipment needed to keep them usable can produce a misleading continuity claim.

## Reserve policy has an opportunity cost

A usable-energy window can reflect operating limits and reserved inventory. State what it includes before allocating energy to another purpose. Retaining a separate reserve can support another event, uncertainty or a service obligation, but it reduces the energy available now. The 80 percent window in this example is applied once; neither its excluded 20 percent nor the 5 percent conversion loss is deducted twice.

Load shape also matters. For a changing protected demand, calculate energy interval by interval and check the power limit at every relevant interval. A short higher-power phase can fail the power screen while barely changing total energy. A lower sustained phase can fit the converter but exhaust the inventory. Neither the maximum MW nor the total MWh alone describes both problems.

A successful transfer to another supply ends the battery's bridging interval only if the other supply has actually become acceptable to the protected system. Generator start, stabilization, load acceptance, transfer behavior, and auxiliary restoration are system events with their own evidence. No generic runtime formula supplies those timings. Use an explicit timeline and compare the required output energy through that interval with the available energy.

Finally, do not claim complete recovery when the load merely returns to its normal source. The store may be depleted and require recharge before it can support a second event. Recharging competes for electrical capacity and may have its own rate limit. A continuity promise therefore needs the starting state, the supported event, and the restored readiness condition. The next lesson follows that event across electricity and cooling rather than stopping at the battery icon.

## Case study: solar and second-life batteries in Sparks

The solar example is Crusoe and Redwood Materials at Sparks, Nevada. Redwood’s 2 April 2026 introduction to Redwood Energy and Crusoe’s May 2026 impact-report summary specify 12 MW of solar and 63 MWh of repurposed EV battery capacity. These quantities describe generation capability and stored energy. Neither is a statement of current IT demand, total-site nameplate load or battery discharge power.

A host-published interview dated 27 July 2025 attributes a 1 MW initial deployment to Forrest Carroll, who worked in Crusoe Energy & Infrastructure Development. This is a dated participant account of the pilot’s scale. The transcript does not specify whether 1 MW is IT power or total facility load, and it is not an equipment nameplate. Later expansion announcements do not establish a verified current load denominator.

Crusoe’s March 2026 update reports 99.2% microgrid availability over seven months and 99.9% Cloud availability using grid backup. Pause: does that mean 99.2% of electricity came from solar? No. Availability measures time meeting a service definition; solar share measures energy from a source. An hourly supply ledger is needed to answer the latter. The grid-backup disclosure also prevents describing this operating account as entirely off-grid. These are historical company-reported operating figures, not a September 2026 measurement interval or a current service guarantee. The May 2026 impact report repeats the case without establishing a new measurement period.

## Compare stored energy with the reported 1 MW pilot

Use the historical reported pilot scale for an explicitly ideal comparison: 63 MWh / 1 MW = 63 hours, or 2.625 days. This is a gross energy-to-reported-load ratio, not measured or guaranteed autonomy. It assumes the whole stated inventory reaches a constant 1 MW load and that the delivery path can supply it. The 12 MW solar nameplate is not the load denominator.

Actual runtime requires usable delivered battery energy divided by the total battery-fed load, with a separate output-power check. Starting state of charge, operating window, reserves, conversion losses, auxiliaries and concurrent generation matter. If the reported 1 MW describes IT alone, cooling and electrical overhead increase the battery-fed demand. As of this 15 September 2026 review, the current expanded installation’s verified IT/nameplate load, full-site load and qualified battery discharge MW remain unknown; the pilot comparison does not fill those gaps.

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

## The tradeoff

Choice: Reserve more stored energy for a second purpose or uncertainty.

Benefit: The system retains explicitly protected energy for that need.

Cost: Less energy remains available for the current outage interval.

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

## Sources and reading boundaries

- [EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) — Runtime follows energy divided by power when a constant output load is specified. Read 2026-09-06. Read the public power/energy unit definitions. Battery-window and reserve values are original assumptions.
- [Vertiv — BESS and UPS roles in large data center power architecture](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) — UPS and conventional behind-the-meter storage have different typical architecture roles. Read 2026-09-06. Read the public landing-page explanation only; the downloadable full white paper and product performance curves were not reviewed.
- [Eaton — DC-link capacitor modules](https://www.eaton.com/gb/en-gb/products/electronic-components/topics/dc-link-modules.html) — Locate DC-link capacitors between rectifier and inverter; explain voltage buffering, ripple and rapid load transitions. Read 2026-09-11. Reviewed the opening functional explanation and UPS application listing. Listed product values do not specify the course UPS or the hypothetical 0.20 F bus.
- [Eaton — Choosing the optimal UPS topology](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/choosing-the-optimal-ups-topology-.html) — Distinguish zero output transfer time in online double-conversion operation from standby and line-interactive transfers. Read 2026-09-11. Reviewed topology and Online UPS sections. Zero transfer time is not a guarantee of zero internal transient or an equipment-specific battery-interface response time.
- [Crusoe and Redwood — Sparks microgrid update](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density) — Teach solar, storage and grid backup at Sparks, Nevada; distinguish microgrid availability from Cloud availability and energy share. Read 2026-09-12. Main release reviewed. Company reports 99.2% microgrid availability over seven months and 99.9% Cloud availability using grid backup. Expansion to 24 modular data centers is announced, not confirmed complete. Do not carry forward the initial off-grid description as present status.
- [Crusoe — 2025 impact report web summary](https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report) — Names 12 MW of solar and 63 MWh of repurposed EV battery capacity for the Redwood project; describes original Abilene phase as greenfield. Read 2026-09-12. Selected web sections reviewed, not the linked full report. Equipment ratings are not measured continuous output or usable battery energy. Company-wide renewable procurement claims cannot establish hourly matching at every campus.
- [Crusoe 2025 Impact Report](https://media.ffycdn.net/us/crusoe/PL5TuZz5apXB9pVsd3H1.pdf) — Page 33 repeats the Sparks solar, storage and availability case. Read 2026-09-12. Report launched May 28, 2026 at https://www.crusoe.ai/resources/blog/crusoes-2025-impact-report . Operator-reported case, not independent commissioning evidence. Do not imply 350 MW backs up the full 1.2 GW campus. Repeated Sparks availability figures are not a newly measured September interval.
- [Schneider Electric — Easy UPS 3-Phase Modular: Configure the Input Contacts](https://productinfo.se.com/easyups3pmodular/990-6537-easy-ups-3-phase-modular-50-250-kw-operation/English/990-6537%20Operation%20Easy%20UPS%203-Phase%20Modular%2050-250%20kW_0001015104.xml/%24/GalaxyPX_ConfiguretheInputContacts_0000761997) — The detected-genset function can set battery charge power to 0% or 100%. Generator-supplied battery charging is configurable; it is not necessarily enabled in every installation. Read 2026-09-12. Public manufacturer's input-contact configuration page read. No claim about generator capacity, start time or charging rate for an actual installation.
- [Eaton — 93E UPS Generation 3 installation and operation manual, 164000301 Rev. 04](https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-93e-ups/eaton-93e-ups-20kva-30kva-generation-3-manual-p-164000301.pdf) — Printed pages 56–59 describe regulated rectifier output and a buck/boost battery converter. When acceptable AC returns, the rectifier resumes supplying the inverter and the battery can recharge. Read 2026-09-12. Operating-mode sections on PDF pages 67–70 reviewed. This is an Eaton topology example, not a specification for the illustrated Schneider UPS or the ideal 800 V, 0.20 F teaching bus and its assumed response times.
- [Redwood Materials — Redwood and Crusoe expand compute to 7x scale](https://www.redwoodmaterials.com/news/redwood-and-crusoe-expand-compute-to-7x-scale/) — Identify the publisher-provided aerial photograph of the Sparks battery and modular data-center deployment. Read 2026-09-13. Article and linked aerial inspected. Expansion is announced. The photo does not establish completed expanded capacity or the battery discharge rating; retain the Crusoe impact report for the specific solar-power label.
- [Schneider Electric — Easy UPS 3-Phase Modular model list](https://productinfo.se.com/easyups3pmodular/viewer?docidentity=ModelList-1A71D03C&extension=xml&lang=en&manualidentity=TechnicalSpecificationsEasyUPS3-Pha-BC29F805) — Named 50–250 kW external-battery models and black/white finish options. Read 2026-09-13. Official model list read. One-switch and four-switch versions exist; the family photograph does not identify the exact model or fitted modules.
- [Schneider Electric — Easy UPS 3-Phase Modular physical specifications](https://productinfo.se.com/easyups3pmodular/990-91580-technical-specifications-easy-ups-3-phase-modular/English/990-91580%20Technical%20Specifications%20Easy%20UPS%203-Phase%20Modular50-250%20kW%20UPS_0001011916.xml/%24/PhysicalREF_0000019941) — Cabinet dimensions and floor footprint for the product shown in the UPS teaching sequence. Read 2026-09-11. Selected dimensions reviewed: 1,991 mm high, 600 mm wide and 850 mm deep. Does not identify the installed rating or internal arrangement of either cabinet in the product-family photo.
- [Redwood Materials — Introduction to Redwood Energy](https://www.redwoodmaterials.com/resources/unlocking-affordable-energy-storage-at-scale-an-introduction-to-redwood-energy/) — Proven at Scale case identifies a 12 MW solar array and 63 MWh repurposed-battery inventory at the Nevada campus; distinguish these from IT load and battery discharge power. Read 2026-09-15. Full page reviewed, especially Proven at Scale: The Crusoe Project. Four modular data centers and expansion to 24 do not establish current commissioned electrical load. No exact IT/full-site nameplate, qualified battery output MW, usable delivered energy or guaranteed autonomy is given.
- [OpenStax — Energy Stored in Capacitors](https://openstax.org/books/college-physics-2e/pages/19-7-energy-stored-in-capacitors) — Explain stored capacitor energy using average voltage over charge, then substitute Q = CV. Read 2026-09-14. Algebraic derivation and equations 19.74–19.76 reviewed. The course uses its own figures and chosen 0.20 F, 800 V numerical example.
- [Luca Pedretti — From Electrons to Intelligence: How Crusoe Powers AI with Modular, 24/7 Energy](https://lucapedretti850786.substack.com/p/c0b) — Host-published interview attributes a 1 MW initial Sparks deployment to Crusoe participant Forrest Carroll; supports a clearly dated pilot-scale energy comparison. Read 2026-09-15. Written interview reviewed; audio not checked. The 1 MW statement is participant testimony, not an equipment nameplate, and does not specify IT versus total facility power. It does not describe the current expanded load or battery output rating. Dividing 63 MWh by this reported pilot scale gives an ideal 63-hour ratio, not measured or guaranteed runtime.
- [Pexapark — Podcast catalogue, Episode 19 with Forrest Carroll of Crusoe](https://pexapark.com/podcast/) — Corroborate the Crusoe interview’s host, guest, topic and Episode 19 date of 24 July 2025. Read 2026-09-15. Episode 19 catalogue entry reviewed. The catalogue date differs from the host’s 27 July written-post date. The catalogue establishes identity, not the 1 MW statement; source P198 supplies the written participant account. Audio not checked.
