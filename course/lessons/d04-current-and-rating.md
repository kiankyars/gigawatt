# Kilowatts do not fill a kilovolt-ampere nameplate

**6. Campus and building power distribution**

Relate real power, power factor, and apparent power to a kVA rating, then work backward from a converter’s DC output, preserving every denominator.

**Driving question:** How do efficiency and power factor change upstream equipment loading?

## Real power, apparent power and a kVA rating

Use the electrical foundations from “Move power with fewer amperes”: RMS values describe effective AC magnitudes; 480 V line-to-line is measured between phases, and √3 connects that voltage convention to total balanced three-phase power. The earlier resistive examples used power factor one. Here the power factor drops below one, and a transformer’s kilovolt-ampere rating becomes the limit to check.

An AC boundary has a second power quantity: apparent power, expressed in kilovolt-amperes (kVA) or megavolt-amperes (MVA). It combines voltage and current magnitudes in the stated system. Power factor (PF) is real power divided by apparent power, so apparent power is real power divided by PF. The difference between kVA and kW is not itself a real-power heat term. However, the associated higher current can increase actual conductor and equipment losses, which require their own accounting.

For balanced three-phase conditions, current is apparent power divided by √3 times the line-to-line RMS voltage. Keep the unit conversion explicit: kVA multiplied by one thousand gives VA. In this lesson the voltage is 480 V line-to-line. The numerical exercise assumes the specified balanced conditions and a given total power factor. It does not infer power factor from an arbitrary phase-angle measurement of a distorted load.

Hold real AC input at 900 kW and balanced three-phase voltage at 480 V line-to-line, behind a transformer with a usable rating of 1,000 kVA. At PF 1, apparent power is 900 kVA and line current is 900,000/(√3 × 480) ≈ 1,083 A, 90 percent of the rating. At PF 0.9 the same 900 kW needs 1,000 kVA, exactly the rating. At PF 0.8 it needs 1,125 kVA and about 1,353 A, 112.5 percent of the rating. Real power is the average power delivered to the load, including its losses. Power factor is the ratio of real to apparent power; conversion efficiency is a different ratio. Because 900 kW and 1,000 kVA measure different things, the smaller number does not rescue the PF 0.8 case. In the lab below, conversion efficiency starts at 1, so the 900 kW is also the real input and PF 0.8 gives 1,125 kVA and 1,353 A; set efficiency to 0.96 and PF to 0.90 for the converter extension.

## The power triangle and the glass of beer

Reactive power describes cyclic energy exchange with electric and magnetic fields. For sinusoidal voltage and current, the three quantities form the power triangle: real power and reactive power are perpendicular sides and apparent power is the hypotenuse, so S² = P² + Q². At 900 kW and PF 0.8, the magnitude of reactive power is 675 kilovolt-amperes reactive (kvar), alongside 1,125 kVA of apparent power. It is not the arithmetic difference between kVA and kW. With distorted waveforms, P and true PF alone do not determine Q.

A glass of beer is a common memory cue for the three quantities. The beer is real power in kW, the average rate at which energy is actually delivered. The foam is reactive power in kvar. The whole glass is apparent power in kVA, and the glass is what the transformer and cables must be sized to hold. The picture fails if the heights are added: 900 kW of beer and 675 kvar of foam need a 1,125 kVA glass, not a 1,575 kVA one, because the two parts combine at right angles.

## Extension: start from a converter’s DC output

A rack-side converter must deliver 900 kW of DC output. That is a different boundary from the 900 kW of real AC input above: conversion has losses, so the AC side supplies more than 900 kW. Define conversion efficiency as output real power divided by input real power. At an assumed 96 percent efficiency, every 0.96 units delivered require one unit at the converter input. To recover the input requirement, divide the output by 0.96. Multiplying by 0.96 would move in the wrong direction and suggest that losses create power.

Begin with 900 kW output and efficiency 0.96. Input real power is 900/0.96 = 937.5 kW. The converter dissipates 37.5 kW at this operating point, found by subtracting output from input. That heat belongs wherever the converter sits. Moving it to another room changes the local cooling account, while its electrical input/output difference remains part of the facility balance.

Next divide 937.5 kW by a power factor of 0.90. Apparent power is approximately 1,041.7 kVA. At 480 V, current is 1,041,667/(√3 × 480), approximately 1,253 A, about 104.2 percent of the same 1,000 kVA rating. At PF 0.90 the 900 kW of real input above exactly filled that rating; the converter’s 37.5 kW of loss pushes this case over it. The fact that 937.5 kW is less than 1,000 does not rescue it; those numbers have different units and describe different constraints.

If the power factor improves to 0.99 while output and efficiency remain unchanged, apparent power becomes about 947.0 kVA. The arithmetic screen now fits beneath 1,000 kVA. Real input power is still 937.5 kW and converter heat is still 37.5 kW in the stated model. This isolates the distinction between reducing a current/apparent-power burden and reducing conversion loss.

The screen is necessary but not sufficient. Equipment limits also depend on operating temperature, load waveform, installation, voltage conditions, and the rating's defined duty. Harmonic currents can matter to heating and equipment performance. An aggregate average can conceal unequal phase loading. The short calculation identifies a plainly inconsistent proposal; it does not substitute for the additional studies needed to endorse a real installation.

## Do not multiply allowances without naming them

Suppose the planning policy reserves twenty percent of a 1.2 MVA usable rating. The remaining apparent-power budget is 1.2 × 0.80 = 0.96 MVA. At PF 0.90 that supports 0.864 MW real input. At efficiency 0.96 it supports 0.82944 MW, or 829.44 kW, of the defined DC output. Each factor applies to a different question: reservation, AC power factor, and conversion efficiency. Combining them is valid only because their boundaries and meanings have been stated.

A reserve policy is not automatically a physical derating, and a physical derating is not automatically redundancy. Derating changes the applicable equipment capability under a condition. Reservation holds some otherwise usable capability for a purpose such as uncertainty or expansion. Redundancy asks what remains available after a selected element is unavailable. Treating all three as one unexplained safety factor makes it impossible to tell whether capacity has been counted twice or not at all.

There is a tradeoff between a larger equipment rating and tighter control of the workload envelope. More rated capacity can create room for growth and operating variation, but may increase cost, footprint, and low-load losses. Tighter limits can use existing equipment efficiently but constrain the accepted workload or require enforceable power management. Neither choice can be assessed from an average utilization percentage alone.

Finally, keep the quantities visible on your diagram. Write 900 kW DC at the output, 937.5 kW real and 1,041.7 kVA at the input, and 1,253 A next to the specified 480 V circuit. The labels show why each number exists. If a subsequent lesson changes the converter, voltage, or power factor, you can update the affected terms without rebuilding the entire explanation from vague notions of electrical capacity.

## Place the high-current route deliberately

Take a balanced 2 MW load at power factor one, fed over a 450 m campus route followed by a 20 m hall route. At 34.5 kV, line current is about 33.5 A; at 480 V it is about 2,406 A, excluding losses for this current comparison. Moving the transformer beside the hall keeps the long route at medium voltage. This changes cable and equipment requirements; actual loss requires the resistance and operating conditions of the selected conductors.

## Check phases and heat before treating a rating as usable

A 380 A average can mean three 380 A phases or a 460/350/330 A allocation. With a 400 A per-conductor usable limit, the unequal case exceeds the phase-A limit. The simple average hides that constraint. For a separate balanced conductor example with resistance fixed at 0.020 ohm per phase, loss is 3 I²R: 2.4 kW at 200 A and 9.6 kW at 400 A. Actual temperature also depends on ambient conditions and enclosure. Harmonic current can increase RMS burden and transformer losses, so the waveform belongs in the thermal assessment.

## Equal phase voltages do not enforce equal phase currents

Equinix’s rack installation guidelines explicitly ask for balanced connections across the three phases of a rack PDU. Take six single-phase PSU groups that each draw 20 A at 277 V phase-to-neutral. Two groups on each phase give 40/40/40 A; a four/one/one assignment gives 80/20/20 A. The total load stays fixed but L1 exceeds a 60 A phase limit. A balanced electromagnetic source does not automatically reassign connected loads. Neutral current depends on the vector sum and waveform content; nonlinear load harmonics require a separate check.

## Worked example: 900 kW of real input behind a 1,000 kVA rating

- Real AC input is 900 kW at both power factors.
- The input is balanced three-phase at 480 V line-to-line RMS.
- The transformer’s usable rating is 1,000 kVA.

1. Apparent power at PF 1 — 900 / 1.0 = 900 kVA — Apparent power is real power divided by power factor.
2. Line current at PF 1 — 900,000 / (√3 × 480) ≈ 1,083 A — Use VA and line-to-line volts to obtain amperes.
3. Apparent power at PF 0.8 — 900 / 0.8 = 1,125 kVA — The same real power needs more apparent power.
4. Line current at PF 0.8 — 1,125,000 / (√3 × 480) ≈ 1,353 A — Current rises in step with apparent power.
5. Rating screen — 900 / 1,000 = 90%; 1,125 / 1,000 = 112.5% — The rating fits at PF 1 and is exceeded at PF 0.8.

**Result:** The same 900 kW passes the 1,000 kVA screen at PF 1 and fails it at PF 0.8, where reactive power is 675 kvar.

**Model boundary:** No converter efficiency is applied. Cable, breaker, transformer thermal, harmonic, and installation checks are separate.

## When the situation changes

Trigger: Compare 900 kW of real input directly with a 1,000 kVA rating.

Mechanism: The comparison ignores the stated power factor and therefore understates apparent-power loading.

Response: Convert quantities at matching boundaries before comparing with a rating.

## Apply the idea

At what power factor does the same 900 kW of real input exactly fill the 1,000 kVA rating, and what line current flows then at 480 V?

<details>
<summary>Reveal the worked answer</summary>

At PF 0.9, with about 1,203 A per line.

900 kW divided by 1,000 kVA is 0.9. Then 1,000,000 VA divided by √3 × 480 V gives about 1,203 A. Any lower power factor pushes the same load past the rating.

</details>

**The idea to keep:** Output power, input real power, apparent power, and current are different quantities that must be reconciled at their own boundaries.

## Sources

- [Schneider Electric — Installed apparent power](https://www.electrical-installation.org/enwiki/Installed_apparent_power_(kVA)) — www.electrical-installation.org · Reviewed 2026-09-06. The public guide relates output power, efficiency, power factor, apparent power, and balanced three-phase current.
- [Schneider Electric — Choice of transformer rating](https://www.electrical-installation.org/enwiki/Choice_of_transformer_rating) — www.electrical-installation.org · Reviewed 2026-09-06. Transformer rating selection considers apparent-power loading and installation constraints.
- [Schneider Electric — Effects of harmonics: increased losses](https://www.electrical-installation.org/enwiki/Effects_of_harmonics_-_Increased_losses) — Schneider Electric · Reviewed 2026-09-13. Harmonic currents increase heating and transformer losses.
- [Equinix — Customer Installation Guidelines, phase balancing](https://web.archive.org/web/20250708155531/https://docs.equinix.com/assets/files/Customer-Installation-Guidelines-EN-5d94e7d67671467cab7d7c9877ef5229.pdf) — Equinix · Published 2024 · Reviewed 2026-09-26. Rack PDU load allocation should balance connections across all three phases; figure 14 compares balanced and unbalanced racks.
- [Schneider · Definition of power factor](https://www.electrical-installation.org/enwiki/Definition_of_Power_Factor) — Schneider Electric · Reviewed 2026-09-14. Defines real power, apparent power and power factor PF = P/S, independently of conversion efficiency.
- [Schneider Electric — Definition of reactive power](https://www.electrical-installation.org/enwiki/Definition_of_reactive_power) — Schneider Electric · Reviewed 2026-09-14. Sinusoidal power triangle and balanced three-phase P, Q and S relationships.
