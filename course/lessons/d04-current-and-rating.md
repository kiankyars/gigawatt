# Kilowatts do not fill a kilovolt-ampere nameplate

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d04-current-and-rating`, then run `uv run gigawatt-expand`.

**6. Campus and building power distribution · Authored draft**

Move backward from a required DC output through conversion efficiency, apparent power, and three-phase current, preserving every denominator.

**Driving question:** How do efficiency and power factor change upstream equipment loading?

## Start at the load and work toward the source

Use the electrical foundations from “Move power with fewer amperes”: RMS values describe effective AC magnitudes; 480 V line-to-line is measured between phases, and √3 connects that voltage convention to total balanced three-phase power. The earlier resistive examples used power factor one. Here we deliberately change the model to a converter with specified efficiency and a supplied power factor below one, and name its 900 kW DC output boundary before working upstream.

A rack-side system needs 900 kW of DC output. The upstream AC equipment does not supply only 900 kW if conversion has losses. Define conversion efficiency as output real power divided by input real power. At an assumed 96 percent efficiency, every 0.96 units delivered require one unit at the converter input. To recover the input requirement, divide the output by 0.96. Multiplying by 0.96 would move in the wrong direction and suggest that losses create power.

The AC boundary introduces another quantity: apparent power, expressed in kVA or MVA. It combines voltage and current magnitudes in the stated system. Power factor is real power divided by apparent power. A supplied power factor of 0.90 means that 0.90 kW of real input accompanies each kVA at that operating point. Therefore apparent power is real power divided by 0.90. The difference between kVA and kW is not itself a real-power heat term. However, the associated higher current can increase actual conductor and equipment losses, which require their own accounting.

For balanced three-phase conditions, current is apparent power divided by √3 times the line-to-line RMS voltage. Keep the unit conversion explicit: kVA multiplied by one thousand gives VA. In this lesson the voltage is 480 V line-to-line. The numerical exercise assumes the specified balanced conditions and a supplied total power factor. It does not infer power factor from an arbitrary phase-angle measurement of a distorted load.

## Calculate the rating screen step by step

Begin with 900 kW output and efficiency 0.96. Input real power is 900/0.96 = 937.5 kW. The converter dissipates 37.5 kW at this operating point, found by subtracting output from input. That heat belongs wherever the converter sits. Moving it to another room changes the local cooling account, while its electrical input/output difference remains part of the facility balance.

Next divide 937.5 kW by PF 0.90. Apparent power is approximately 1,041.7 kVA. At 480 V, current is 1,041,667/(√3 × 480), approximately 1,253 A. A hypothetical transformer with a usable 1,000 kVA limit fails this simple apparent-power screen: the requested load is about 104.2 percent of that limit. The fact that 937.5 kW is less than 1,000 does not rescue it; those numbers have different units and describe different constraints.

If the supplied power factor improves to 0.99 while output and efficiency remain unchanged, apparent power becomes about 947.0 kVA. The arithmetic screen now fits beneath 1,000 kVA. Real input power is still 937.5 kW and converter heat is still 37.5 kW in the stated model. This isolates the distinction between reducing a current/apparent-power burden and reducing conversion loss.

The screen is necessary but not sufficient. Equipment limits also depend on operating temperature, load waveform, installation, voltage conditions, and the rating's defined duty. Harmonic currents can matter to heating and equipment performance. An aggregate average can conceal unequal phase loading. The short calculation identifies a plainly inconsistent proposal; it does not substitute for the additional studies needed to endorse a real installation.

## Do not multiply allowances without naming them

Suppose the planning policy reserves twenty percent of a 1.2 MVA usable rating. The remaining apparent-power budget is 1.2 × 0.80 = 0.96 MVA. At PF 0.90 that supports 0.864 MW real input. At efficiency 0.96 it supports 0.82944 MW, or 829.44 kW, of the defined DC output. Each factor applies to a different question: reservation, AC power factor, and conversion efficiency. Combining them is valid only because their boundaries and meanings have been stated.

A reserve policy is not automatically a physical derating, and a physical derating is not automatically redundancy. Derating changes the applicable equipment capability under a condition. Reservation holds some otherwise usable capability for a purpose such as uncertainty or expansion. Redundancy asks what remains available after a selected element is unavailable. Treating all three as one unexplained safety factor makes it impossible to tell whether capacity has been counted twice or not at all.

There is a tradeoff between a larger equipment rating and tighter control of the workload envelope. More rated capacity can create room for growth and operating variation, but may increase cost, footprint, and low-load losses. Tighter limits can use existing equipment efficiently but constrain the accepted workload or require enforceable power management. Neither choice can be assessed from an average utilization percentage alone.

Finally, keep the quantities visible on the diagram. Write 900 kW DC at the output, 937.5 kW real and 1,041.7 kVA at the input, and 1,253 A next to the specified 480 V circuit. The labels show why each number exists. If a subsequent lesson changes the converter, voltage, or power factor, you can update the affected terms without rebuilding the entire explanation from vague notions of electrical capacity.

## Place the high-current route deliberately

The chapter keeps a balanced 2 MW load at power factor one and compares a 450 m campus route followed by a 20 m hall route. At 34.5 kV, line current is about 33.5 A; at 480 V it is about 2,406 A, excluding losses for this current comparison. Moving the transformer beside the hall keeps the long route at medium voltage. This changes cable and equipment requirements; actual loss requires the resistance and operating conditions of the selected conductors.

## Check phases and heat before treating a rating as usable

A 380 A average can mean three 380 A phases or a 460/350/330 A allocation. With a supplied 400 A per-conductor usable limit, the unequal case exceeds the phase-A limit. The simple average hides that constraint. For a separate balanced conductor example with resistance fixed at 0.020 ohm per phase, loss is 3 I²R: 2.4 kW at 200 A and 9.6 kW at 400 A. Actual temperature also depends on ambient conditions and enclosure. Harmonic current can increase RMS burden and transformer losses, so the waveform belongs in the thermal assessment.

## Equal phase voltages do not enforce equal phase currents

Equinix’s rack installation guidelines explicitly ask for balanced connections across the three phases of a rack PDU. In the teaching example six single-phase PSU groups each draw 20 A at 277 V phase-to-neutral. Two groups on each phase give 40/40/40 A; a four/one/one assignment gives 80/20/20 A. The total load stays fixed but L1 exceeds the stipulated 60 A phase limit. A balanced electromagnetic source does not automatically reassign connected loads. Neutral current depends on the vector sum and waveform content; nonlinear load harmonics require a separate check.

The reduced power-factor example holds real AC input at 900 kW and voltage at 480 V line-to-line. S = P/PF gives 900 kVA at PF 1, 1,000 kVA at PF 0.9 and 1,125 kVA at PF 0.8. The illustrative transformer is rated 1,000 kVA. This teaches how current uses equipment capacity without reintroducing a converter-loss calculation. Power factor and conversion efficiency are distinct.

## Read the power-factor comparison

The comparison before the interactive slide keeps real power at 900 kW and balanced three-phase voltage at 480 V line-to-line. PF 1 gives 900 kVA and 1,083 A; PF 0.8 gives 1,125 kVA and 1,353 A. Those loads use 90% and 112.5% of the 1,000 kVA transformer rating; the selected two-column image displays 112.5% directly. Real power is average power delivered to the load, including its losses. Power factor is the ratio of real to apparent power; it is not conversion efficiency.

Reactive power describes cyclic energy exchange with electric and magnetic fields. For sinusoidal voltage and current, S² = P² + Q². At 900 kW and PF 0.8, the magnitude of reactive power is 675 kvar, alongside 1,125 kVA of apparent power. It is not the arithmetic difference between kVA and kW. With distorted waveforms, P and true PF alone do not determine Q.

## Worked example: A 900 kW output behind a 1 MVA limit

- DC output is 900 kW.
- Conversion efficiency is 0.96 and input PF is 0.90.
- The AC input is balanced three-phase at 480 V line-to-line RMS.

1. Input real power — 900 / 0.96 = 937.5 kW — Divide by efficiency because input must exceed output.
2. Converter heat — 937.5 − 900 = 37.5 kW — The input/output difference is the stated conversion loss.
3. Apparent power — 937.5 / 0.90 = 1,041.67 kVA — Power factor relates real power to apparent power.
4. Line current — 1,041,667 / (√3 × 480) ≈ 1,253 A — Use VA and volts to obtain amperes.
5. Rating screen — 1,041.67 / 1,000 = 104.17% — The hypothetical 1,000 kVA usable limit is exceeded.

**Result:** The proposal fails the apparent-power screen despite real input below 1,000 kW.

**Model boundary:** No cable, breaker, transformer thermal, harmonics, or installation design is established by this arithmetic alone.

## The tradeoff

Choice: Increase equipment capacity rather than tighten the supported load envelope.

Benefit: Additional capacity can accommodate growth or uncertainty.

Cost: Cost, footprint, and operating efficiency need their own assessment.

## When the situation changes

Trigger: Compare 937.5 kW directly with a 1,000 kVA rating.

Mechanism: The comparison ignores the stated power factor and therefore understates apparent-power loading.

Response: Convert quantities at matching boundaries before comparing with a rating.

## Apply the idea

With PF 0.99 and the same 900 kW output and 96% efficiency, what apparent power is required?

<details>
<summary>Reveal the worked answer</summary>

Approximately 946.97 kVA.

Input real power remains 937.5 kW. Dividing by 0.99 gives 946.97 kVA; this passes only the stated apparent-power screen.

</details>

**The idea to keep:** Output power, input real power, apparent power, and current are different quantities that must be reconciled at their own boundaries.

## Sources and reading boundaries

- [Schneider Electric — Installed apparent power](https://www.electrical-installation.org/enwiki/Installed_apparent_power_(kVA)) — The public guide relates output power, efficiency, power factor, apparent power, and balanced three-phase current. Read 2026-09-06. Read the formula and variable definitions. Nonlinear-load and installation behavior require additional evidence; the example values are hypothetical.
- [Schneider Electric — Choice of transformer rating](https://www.electrical-installation.org/enwiki/Choice_of_transformer_rating) — Transformer rating selection considers apparent-power loading and installation constraints. Read 2026-09-06. Read the public rating discussion, not a site-specific selection study; no listed product rating is used.
- [Schneider Electric — Effects of harmonics: increased losses](https://www.electrical-installation.org/enwiki/Effects_of_harmonics_-_Increased_losses) — Harmonic heating and transformer-loss mechanism; excerpt scope recorded. Read 2026-09-13. Public indexed excerpt reviewed; direct page returned 503. No harmonic derating factor or real equipment rating is inferred. The 3 I²R comparison uses original fixed-resistance teaching inputs.
- [Equinix — Customer Installation Guidelines, phase balancing](https://docs.equinix.com/assets/files/Customer-Installation-Guidelines-EN-5d94e7d67671467cab7d7c9877ef5229.pdf) — Rack PDU load allocation should balance connections across all three phases; figure 14 compares balanced and unbalanced racks. Read 2026-09-13. Public indexed page 19 and figure description reviewed. Six groups at 20 A and a 60 A limit are an original teaching example, not Equinix ratings.
- [Schneider · Definition of power factor](https://www.electrical-installation.org/enwiki/Definition_of_Power_Factor) — Define real power, apparent power and PF = P/S independently of conversion efficiency. Read 2026-09-14. Definitions reviewed. The 900 kW, 480 V and 1,000 kVA comparison is a course example, not equipment performance data.
- [Schneider Electric — Definition of reactive power](https://www.electrical-installation.org/enwiki/Definition_of_reactive_power) — Sinusoidal power triangle and balanced three-phase P, Q and S relationships. Read 2026-09-14. S² = P² + Q² and displacement PF interpretation assume sinusoidal voltage and current. Do not infer Q from true PF alone under harmonic distortion.
