# Move power with fewer amperes

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d03-voltage-and-distance`, then run `uv run gigawatt-expand`.

**4. Siting, grid connection and supply · Authored draft**

Start with a closed DC circuit and AC waveforms, explain the three-phase power equation, then compare transport current and conductor heating at a fixed campus load.

**Driving question:** Why does a higher transport voltage reduce one important class of losses?

## Build from a closed DC loop to alternating current

Voltage is an electrical potential difference: energy transferred per unit charge. Current is the rate at which charge passes a point. In a simple DC boundary, their product gives electrical power. A higher voltage can therefore transfer the same power with less current. That observation is the starting point for understanding transport voltage, but it does not by itself choose an installation voltage. Equipment interfaces, insulation, protection, clearances, conversion, and cost still matter.

In a steady DC circuit, voltage keeps one polarity and conventional current travels around a complete source–load–return loop. Both the outgoing and return conductors carry the same current; adding their magnitudes counts one circuit current twice. For an ideal resistive load receiving 100 kW at 800 V DC, each conductor carries 125 A. The introductory circuit has no conductor or converter losses.

Now use a single-phase sinusoidal AC source and another resistive load, still chosen to receive 100 kW on average. Voltage and current reverse together every half-cycle. Instantaneous power is their product, so the resistor keeps receiving power when both signs reverse. RMS is the effective value for resistive heating, not the peak: a 480 V RMS sine wave peaks at about 679 V. This single-phase example needs 208.33 A RMS; its received power ranges from zero to 200 kW and averages 100 kW. The equal-power anchor describes the load requirement, not an unchanged resistor.

## Combine three phases without changing the power requirement

Balanced three-phase AC uses three equal phase voltages separated by 120 degrees, or one-third of a cycle. Picture three equal resistive load branches sharing a star point, a wye connection. Each branch averages one-third of the total power. Their staggered instantaneous powers add to a constant 100 kW in this ideal balanced sinusoidal model. Three phases do not mean three times the specified total load.

The signed line currents sum to zero at every instant. Current entering on some phase conductors leaves on the others, so a neutral would carry zero load current in this balanced sinusoidal case. Real unequal loads or nonlinear current waveforms can require a neutral. Protective earth is not the normal load-current return, and a three-conductor teaching model is not a complete installation drawing.

At 480 V line-to-line RMS, each wye branch sees 480/√3 ≈ 277 V RMS from phase to star point. Line-to-line voltage is the difference between two phase voltages separated by 120 degrees, giving the √3 relationship. Add the three branch powers at power factor one: P = 3 × V_phase-to-neutral × I_line = √3 × V_line-to-line × I_line. The 100 kW example therefore uses 120.281 A RMS per line. The 800 V DC example uses 125 A per conductor; average energy delivery remains equal. The visual 800 V sample develops this circuit and waveform sequence before its copper comparison.

## Use the three-phase formula with a named boundary

For a balanced three-phase AC example, real power is P = √3 × VLL × I × PF. VLL is the line-to-line RMS voltage, I is RMS line current, and PF is the real-to-apparent power ratio. The factor √3, approximately 1.732, comes from the relationship among the three phases and the line-to-line voltage convention. Do not insert a phase-to-neutral voltage into this version of the equation. That would mix definitions and produce an incorrect current.

To solve for current, divide both sides by √3 × VLL × PF. The result is I = P/(√3 × VLL × PF). We will use a balanced, sinusoidal, unity-power-factor scenario so the comparison stays narrow. Later lessons add equipment efficiency and apparent-power limits. For now, the purpose is to predict the direction and size of a current change before relying on a calculator.

## Work through a two-voltage transport comparison

Now increase the example load explicitly from the 100 kW electrical primer to a hypothetical 10 MW campus receiving boundary. Deliver that same 10 MW at either 10 kV or 20 kV line-to-line, with PF = 1. At 10 kV, current is 10,000,000/(1.732 × 10,000), approximately 577.4 A. At 20 kV it is approximately 288.7 A. Doubling voltage has halved current because the delivered real power and power factor are held fixed. We have not claimed that the same piece of equipment can simply be operated at either voltage.

Assume each of the three phase conductors has 0.10 ohm resistance at the operating condition being compared. Resistive heating is I²R per conductor. Across three equal conductors it is 3I²R. The lower-voltage case loses 3 × 577.4² × 0.10, approximately 100,000 W, or 100 kW. The higher-voltage case loses approximately 25 kW. Halving current quarters this particular loss because the current is squared.

The difference is 75 kW. If both cases remained at their stated load for eight hours, the conductor-energy difference would be 75 kW × 8 h = 600 kWh. This isolates one mechanism. It excludes transformer losses, converter losses, reactive effects beyond the stated power factor, additional auxiliaries, and any change in conductor design. It is not a total-system efficiency prediction or a construction specification.

Check the electrical accounting. We specified 10 MW delivered at the receiving boundary, so the sending source must cover that plus the modeled conductor heating. In this simplified comparison it supplies 10.100 MW in the first case and 10.025 MW in the second. If a diagram labels both ends 10 MW while also showing positive losses, the numbers do not balance. A clear diagram makes the receiving and sending boundaries visible.

## Test which assumptions make the result hold

Change the power factor to 0.80 while keeping delivered real power and voltage fixed. Current rises by 1/0.80 = 1.25. Conductor heating rises by 1.25 squared, or 1.5625. At 10 kV with the same resistance, the loss becomes 156.25 kW. Power factor has increased the current needed to deliver the same real power. It has not changed the stated 10 MW into 12.5 MW of real load.

Now change the conductor rather than the voltage. If the higher-voltage design uses a different resistance, the loss ratio becomes the current-squared ratio multiplied by the resistance ratio. A resistance twice as large would turn the earlier quarter-loss result into half the loss. You cannot keep saying one quarter after changing the assumption that produced it. This is why a comparison should display its fixed inputs next to the visual.

Higher transport voltage brings a real tradeoff. It can reduce current and conductor burden for a given transfer, but requires appropriate equipment and insulation interfaces and may change conversion placement. If a higher-voltage route needs an additional conversion stage, its losses belong in a whole-path comparison. The correct choice depends on the complete architecture, not only the elegant inverse-square relationship.

A useful failure test is to ask what happens if the required load doubles while the transport voltage and conductor remain unchanged. Current doubles and conductor heating becomes four times as large in the simplified model. Temperature-dependent resistance and equipment operating limits can make the actual response more complicated. The model gives an early warning about scaling, while the engineering design still requires the missing thermal, protection, and installation information.

## Case study: equipment delivery changes the electrical path

In its August 7, 2026 construction analysis, SemiAnalysis describes a procurement workaround in the Southaven/MiniHard buildout discussion: imported power modules and medium-voltage delivery from generation to transformers supplying low voltage, avoiding long-lead switchgear and large power transformers. This is the reported procurement rationale, rather than a claim that every circuit at Colossus uses medium voltage.

Compare two conceptual paths. One raises generation voltage for transmission and later steps it down again. The other distributes locally at medium voltage before stepping down for the load. Removing the large-transformer stages can remove a delivery dependency, but current, conductor quantity, protection, distance and losses still constrain the alternative. The actual circuit count, ratings and procurement dates require project records.

Pause: for the same balanced three-phase 200 MW transfer at power factor 1, compare 34.5 kV with 161 kV. These are hypothetical voltages, not xAI site specifications. Using I = P/(√3 V), aggregate line current is about 3.35 kA versus 0.717 kA, a 4.67-fold change. At the same equivalent resistance, I²R loss changes about 21.8-fold. A real design can add parallel circuits or conductor area, so this does not estimate xAI losses. The decision is whether a deliverable alternative earns enough earlier useful work to justify its other costs.

## Worked example: Ten megawatts at two AC voltages

- Balanced sinusoidal three-phase load with PF = 1.
- Receiving real power is 10 MW in both cases.
- Each phase conductor has 0.10 Ω resistance at the stated condition.

1. 10 kV current — 10,000,000 / (√3 × 10,000) = 577.35 A — Use line-to-line RMS voltage.
2. 20 kV current — 10,000,000 / (√3 × 20,000) = 288.68 A — At fixed real power, doubling voltage halves current.
3. 10 kV conductor loss — 3 × 577.35² × 0.10 = 100,000 W — Account for all three equal phase conductors.
4. 20 kV conductor loss — 3 × 288.68² × 0.10 = 25,000 W — Current squared makes this one quarter of the first loss.

**Result:** The modeled conductor losses are 100 kW and 25 kW, a 75 kW difference.

**Model boundary:** No transformer, switchgear, converter, installation, or total architecture efficiency claim follows from this isolated resistance model.

## The tradeoff

Choice: Increase transport voltage.

Benefit: Required current and resistive conductor heating can fall for the same delivered power.

Cost: Voltage-compatible equipment, insulation, conversion, and protection must be considered as part of the full architecture.

## When the situation changes

Trigger: Double load without changing the conductor path.

Mechanism: Current doubles and the modeled I²R heating quadruples.

Response: Recalculate the complete operating envelope instead of extrapolating a nameplate or linear loss assumption.

## Apply the idea

At 20 kV, double each conductor resistance from 0.10 to 0.20 Ω. Is loss still one quarter of the 10 kV, 0.10 Ω case?

<details>
<summary>Reveal the worked answer</summary>

No. It becomes 50 kW, or one half of the original 100 kW loss.

The current-squared ratio is one quarter; multiplying by a resistance ratio of two produces one half.

</details>

**The idea to keep:** At fixed real power and power factor, higher voltage reduces current; the conductor-loss benefit depends on the resistance being compared.

## Sources and reading boundaries

- [Schneider Electric — Installed apparent power](https://www.electrical-installation.org/enwiki/Installed_apparent_power_(kVA)) — Balanced three-phase apparent power and line current use line-to-line voltage and the √3 factor. Read 2026-09-06. Read the public equation and variable definitions; this scenario assumes sinusoidal balanced conditions and does not reproduce equipment selection tables.
- [OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) — Resistive heating follows I²R under the stated resistor model. Read 2026-09-06. Read the electrical-power equations; conductor resistance and all numerical values are original assumptions.
- [OpenStax — 20.5 Alternating Current versus Direct Current (College Physics 2e)](https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current) — Explains AC and DC, sinusoidal peak and RMS values, and average power delivered to a resistive load. The 100 kW comparisons are original teaching models. Read 2026-09-10. The AC primer assumes a sinusoidal source and a resistive load with power factor one; it does not model nonlinear rack power electronics.
- [Steven H. Low — Power System Analysis: Analytical tools and structural properties (April 7, 2025 draft)](https://netlab.caltech.edu/assets/book/PSA/Low-PSA-v20250407.pdf) — Sections 1.2–1.3 develop balanced three-phase circuits, phase-to-line voltage relationships, constant total instantaneous power and zero neutral current under balanced conditions. Read 2026-09-10. April 7, 2025 draft; used for the balanced sinusoidal circuit derivation. No real installation, neutral sizing or protection design follows from the simplified teaching model.
- [SpaceX 10GW in 2027 — construction pace and equipment procurement](https://newsletter.semianalysis.com/p/spacex-10gw-in-2027-why-its-real) — Reported speed-versus-efficiency tradeoff: power modules and medium-voltage generation-to-distribution path bypass long-lead switchgear and large power transformers. Read 2026-09-12. Public construction-pace section reviewed, especially the paragraph immediately following MiniHard. Attribution is SemiAnalysis research in the Southaven/MiniHard buildout context; not an as-built one-line for every Colossus site. No market, revenue or 2027 capacity forecast adopted. Do not rewrite this as all site equipment operating at MV.
