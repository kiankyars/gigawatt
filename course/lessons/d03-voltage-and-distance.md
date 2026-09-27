# Move power with fewer amperes

**4. Siting, grid connection and supply**

Start with a closed DC circuit and AC waveforms, explain the three-phase power equation, then compare transport current and conductor heating at a fixed campus load.

**Driving question:** Why does a higher transport voltage reduce one important class of losses?

## Build from a closed DC loop to alternating current

Voltage is an electrical potential difference: energy transferred per unit charge. Current is the rate at which charge passes a point. In a simple direct-current (DC) boundary, their product gives electrical power. A higher voltage can therefore transfer the same power with less current. That observation is the starting point for understanding transport voltage, but it does not by itself choose an installation voltage. Equipment interfaces, insulation, protection, clearances, conversion, and cost still matter.

In a steady DC circuit, voltage keeps one polarity and conventional current travels around a complete source–load–return loop. Both the outgoing and return conductors carry the same current; adding their magnitudes counts one circuit current twice. For an ideal resistive load receiving 100 kW at 800 V DC, each conductor carries 125 A. The introductory circuit has no conductor or converter losses.

Now use a single-phase sinusoidal alternating-current (AC) source and another resistive load, still chosen to receive 100 kW on average. Voltage and current reverse together every half-cycle. Instantaneous power is their product, so the resistor keeps receiving power when both signs reverse. The root-mean-square (RMS) value is the effective value for resistive heating, not the peak: a 480 V RMS sine wave peaks at about 679 V. This single-phase example needs 208.33 A RMS; its received power ranges from zero to 200 kW and averages 100 kW. The equal-power anchor describes the load requirement, not an unchanged resistor.

## Combine three phases without changing the power requirement

Balanced three-phase AC uses three equal phase voltages separated by 120 degrees, or one-third of a cycle. Picture three equal resistive load branches sharing a star point, a wye connection. Each branch averages one-third of the total power. Their staggered instantaneous powers add to a constant 100 kW in this ideal balanced sinusoidal model. Three phases do not mean three times the specified total load.

The signed line currents sum to zero at every instant. Current entering on some phase conductors leaves on the others, so a neutral would carry zero load current in this balanced sinusoidal case. Real unequal loads or nonlinear current waveforms can require a neutral. Protective earth is not the normal load-current return, and a three-conductor model is not a complete installation drawing.

At 480 V line-to-line RMS, each wye branch sees 480/√3 ≈ 277 V RMS from phase to star point. Line-to-line voltage is the difference between two phase voltages separated by 120 degrees, giving the √3 relationship. Add the three branch powers at power factor one: P = 3 × V_phase-to-neutral × I_line = √3 × V_line-to-line × I_line. The 100 kW example therefore uses 120.281 A RMS per line. The 800 V DC example uses 125 A per conductor; average energy delivery remains equal. Each DC conductor carries slightly more current, but the DC circuit needs two conductors where the three-phase circuit needs three. With the same resistance R in every conductor, the DC heat is 2 × 125² × R = 31,250 × R watts and the AC heat is 3 × 120.28² × R ≈ 43,400 × R watts, so the DC circuit makes about 72 percent of the AC circuit’s conductor heat. At 10 milliohms per conductor that is 312.5 W against about 434 W.

## Use the three-phase formula with a named boundary

For a balanced three-phase AC example, real power is P = √3 × VLL × I × PF. VLL is the line-to-line RMS voltage, I is RMS line current, and PF is the real-to-apparent power ratio. The factor √3, approximately 1.732, comes from the relationship among the three phases and the line-to-line voltage convention. Do not insert a phase-to-neutral voltage into this version of the equation. That would mix definitions and produce an incorrect current.

To solve for current, divide both sides by √3 × VLL × PF. The result is I = P/(√3 × VLL × PF). We will use a balanced, sinusoidal, unity-power-factor scenario so the comparison stays narrow. Later lessons add equipment efficiency and apparent-power limits. For now, the purpose is to predict the direction and size of a current change before relying on a calculator.

## Case study: equipment delivery changes the electrical path

In its August 7, 2026 construction analysis, SemiAnalysis describes a procurement workaround in the Southaven/MiniHard buildout discussion: imported power modules and medium-voltage delivery from generation to transformers supplying low voltage, avoiding long-lead switchgear and large power transformers. This is the reported procurement rationale, rather than a claim that every circuit at Colossus uses medium voltage.

Compare two conceptual paths. One raises generation voltage for transmission and later steps it down again. The other distributes locally at medium voltage before stepping down for the load. Removing the large-transformer stages can remove a delivery dependency, but current, conductor quantity, protection, distance and losses still constrain the alternative. The actual circuit count, ratings and procurement dates require project records.

Comparing the two paths at equal power shows what the lower-voltage route trades away: more current for the same delivered power. Extra current may require more parallel feeders, conductor area and switchgear. The comparison concerns campus AC transport and is separate from the 800 V DC rack and hall comparison in Chapter 9.

## Work through a 200 MW transport comparison

Take a 200 MW receiving boundary supplied at either 34.5 kV or 161 kV line-to-line, balanced, with PF = 1. At 34.5 kV, current is 200,000,000/(1.732 × 34,500), approximately 3,347 A, or 3.35 kA. At 161 kV it is approximately 717 A. The current ratio is 161/34.5 ≈ 4.67, because the delivered real power and power factor are held fixed. These currents are per line, or an aggregate before the current is split across parallel circuits. Neither voltage comes from the Southaven permit figures, which give no circuit counts or losses either, and each voltage needs equipment rated for it.

Resistive heating, also called Joule heating, is I²R per conductor, so three equal phase paths lose 3I²R. Give each phase path the same equivalent resistance of 0.01 ohm. The 34.5 kV route loses 3 × 3,347² × 0.01, approximately 336 kW; the 161 kV route loses about 15.4 kW. Squaring the 4.67 current ratio gives about 21.8 times the heat at the lower voltage. A real 34.5 kV design would split its current across parallel circuits or larger conductors, which lowers the resistance, so these figures estimate no site’s losses.

The difference is about 321 kW. Held for eight hours, it is about 2,565 kWh of conductor heat. This isolates one mechanism. It excludes transformer losses, converter losses, reactive effects beyond the stated power factor, additional auxiliaries, and any change in conductor design, so it is a comparison of one loss rather than a total-system efficiency prediction.

Check the electrical accounting. We specified 200 MW delivered at the receiving boundary, so the sending source must cover that plus the modeled conductor heating: about 200.336 MW in the first case and 200.015 MW in the second. If a diagram labels both ends 200 MW while also showing positive losses, the numbers do not balance. A clear diagram makes the receiving and sending boundaries visible.

## Test which assumptions make the result hold

Change the power factor to 0.80 while keeping delivered real power and voltage fixed. Current rises by 1/0.80 = 1.25, to about 4,184 A at 34.5 kV. Conductor heating rises by 1.25 squared, or 1.5625, to about 525 kW at the same resistance. Power factor has increased the current needed to deliver the same real power. The stated 200 MW of real load is still 200 MW.

Distance enters through resistance. A conductor’s resistance is proportional to its length and inversely proportional to its cross-sectional area, R = ρL/A, where ρ is the resistivity of the metal. Double the route length with the same conductor and R doubles, so at the same current the I²R heat doubles too. The current saved by a higher voltage therefore saves more heat the longer the route it travels.

Now change the conductor rather than the voltage. If the higher-voltage route has a different resistance, because it is longer or uses a thinner conductor, the loss ratio becomes the current-squared ratio multiplied by the resistance ratio. Twice the resistance at 161 kV halves the 21.8-fold advantage to about 10.9. You cannot keep quoting the first ratio after changing the assumption that produced it. This is why a comparison should show its fixed inputs next to its result.

Higher transport voltage brings a real tradeoff. It can reduce current and conductor burden for a given transfer, but requires appropriate equipment and insulation interfaces and may change conversion placement. If a higher-voltage route needs an additional conversion stage, its losses belong in a whole-path comparison. The correct choice depends on the complete architecture, not only the elegant inverse-square relationship.

A useful failure test is to ask what happens if the required load doubles while the transport voltage and conductor remain unchanged. Current doubles and conductor heating becomes four times as large in the simplified model. Temperature-dependent resistance and equipment operating limits can make the actual response more complicated. The model gives an early warning about scaling, while the engineering design still requires the missing thermal, protection, and installation information.

## Extension: ten megawatts on a campus feeder

The same arithmetic works at the scale of one campus feeder. Deliver 10 MW at either 10 kV or 20 kV line-to-line with PF = 1: current is about 577.4 A at 10 kV and 288.7 A at 20 kV, so doubling the voltage halves the current. With 0.10 ohm per phase conductor, the losses are 3 × 577.4² × 0.10 ≈ 100 kW and about 25 kW, a 75 kW difference, and the sending source supplies 10.100 MW or 10.025 MW. Halving the current quarters this loss because the current is squared. In the lab below, set 10 MW, 10 kV, 20 kV and 0.10 Ω to reproduce it.

## Worked example: Two hundred megawatts at 34.5 kV and 161 kV

- Balanced sinusoidal three-phase load with PF = 1.
- Receiving real power is 200 MW in both cases; currents are per line, before any split into parallel circuits.
- Each phase path has the same 0.01 Ω equivalent resistance at the stated condition.

1. 34.5 kV current — 200,000,000 / (√3 × 34,500) ≈ 3,347 A — Use line-to-line RMS voltage.
2. 161 kV current — 200,000,000 / (√3 × 161,000) ≈ 717 A — At fixed real power, current is inversely proportional to voltage.
3. Current ratio — 161 / 34.5 ≈ 4.67 — The lower-voltage route carries about 4.67 times the current.
4. 34.5 kV conductor heat — 3 × 3,347² × 0.01 ≈ 336 kW — Account for all three equal phase paths.
5. 161 kV conductor heat — 3 × 717² × 0.01 ≈ 15.4 kW — Squaring the 4.67 current ratio gives about 21.8 times less heat.

**Result:** The 34.5 kV route carries about 3.35 kA against 717 A and, at equal resistance, makes about 336 kW of conductor heat against 15.4 kW.

**Model boundary:** No transformer, switchgear, circuit count, installation, or site loss follows from this isolated resistance model; the voltages are comparison inputs, not Southaven specifications.

## When the situation changes

Trigger: Double load without changing the conductor path.

Mechanism: Current doubles and the modeled I²R heating quadruples.

Response: Recalculate the complete operating envelope instead of extrapolating a nameplate or linear loss assumption.

## Apply the idea

Suppose the 161 kV route is three times as long as the 34.5 kV route and uses the same conductor, so each of its phase paths has 0.03 Ω. Does it still make less conductor heat than the 34.5 kV route at 0.01 Ω?

<details>
<summary>Reveal the worked answer</summary>

Yes. It makes about 46.3 kW against 336 kW, about 7.3 times less instead of 21.8 times.

Tripling the length triples R, so the 161 kV heat triples from about 15.4 to about 46.3 kW. The 21.8-fold current-squared advantage divided by the resistance ratio of 3 leaves about 7.3.

</details>

**The idea to keep:** At fixed real power and power factor, higher voltage reduces current; the conductor-loss benefit depends on the resistance being compared.

## Sources

- [Schneider Electric — Installed apparent power](https://www.electrical-installation.org/enwiki/Installed_apparent_power_(kVA)) — www.electrical-installation.org · Reviewed 2026-09-06. Balanced three-phase apparent power and line current use line-to-line voltage and the √3 factor.
- [OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) — openstax.org · Published 2016-10-06 · Reviewed 2026-09-06. Resistive heating follows I²R under the stated resistor model.
- [OpenStax — 20.5 Alternating Current versus Direct Current (College Physics 2e)](https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current) — OpenStax, Rice University · Published 2022-07-13 · Reviewed 2026-09-10. Explains AC and DC, sinusoidal peak and RMS values, and average power delivered to a resistive load.
- [Steven H. Low — Power System Analysis: Analytical tools and structural properties (April 7, 2025 draft)](https://netlab.caltech.edu/assets/book/PSA/Low-PSA-v20250407.pdf) — Steven H. Low, California Institute of Technology · Reviewed 2026-09-10. Sections 1.2–1.3 develop balanced three-phase circuits, phase-to-line voltage relationships, constant total instantaneous power and zero neutral current under balanced conditions.
- [SpaceX 10GW in 2027 — construction pace and equipment procurement](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) — SemiAnalysis · Published 2026-08-07 · Reviewed 2026-09-12. Reported speed-versus-efficiency tradeoff: power modules and medium-voltage generation-to-distribution path bypass long-lead switchgear and large power transformers.
- [OpenStax — College Physics 2e, 20.3 Resistance and Resistivity](https://openstax.org/books/college-physics-2e/pages/20-3-resistance-and-resistivity) — OpenStax, Rice University · Reviewed 2026-09-26. Resistance is proportional to conductor length and inversely proportional to cross-sectional area, R = ρL/A.
