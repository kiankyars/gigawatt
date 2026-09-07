# Move power with fewer amperes

**D03 · Authored draft · Objectives:** D03.2

Derive a balanced three-phase current comparison, calculate conductor heating, and identify what the comparison cannot decide.

**Driving question:** Why does a higher transport voltage reduce one important class of losses?

## Voltage and current perform different jobs

Voltage is an electrical potential difference: energy transferred per unit charge. Current is the rate at which charge passes a point. In a simple DC boundary, their product gives electrical power. A higher voltage can therefore transfer the same power with less current. That observation is the starting point for understanding transport voltage, but it does not by itself choose an installation voltage. Equipment interfaces, insulation, protection, clearances, conversion, and cost still matter.

For a balanced three-phase AC example, real power is P = √3 × VLL × I × PF. VLL is the line-to-line RMS voltage, I is RMS line current, and PF is the real-to-apparent power ratio. The factor √3, approximately 1.732, comes from the relationship among the three phases and the line-to-line voltage convention. Do not insert a phase-to-neutral voltage into this version of the equation. That would mix definitions and produce an incorrect current.

To solve for current, divide both sides by √3 × VLL × PF. The result is I = P/(√3 × VLL × PF). We will use a balanced, sinusoidal, unity-power-factor scenario so the comparison stays narrow. Later lessons add equipment efficiency and apparent-power limits. For now, the purpose is to predict the direction and size of a current change before relying on a calculator.

## Work through a two-voltage transport comparison

Deliver a hypothetical 10 MW to a receiving boundary at either 10 kV or 20 kV line-to-line, with PF = 1. At 10 kV, current is 10,000,000/(1.732 × 10,000), approximately 577.4 A. At 20 kV it is approximately 288.7 A. Doubling voltage has halved current because the delivered real power and power factor are held fixed. We have not claimed that the same piece of equipment can simply be operated at either voltage.

Assume each of the three phase conductors has 0.10 ohm resistance at the operating condition being compared. Resistive heating is I²R per conductor. Across three equal conductors it is 3I²R. The lower-voltage case loses 3 × 577.4² × 0.10, approximately 100,000 W, or 100 kW. The higher-voltage case loses approximately 25 kW. Halving current quarters this particular loss because the current is squared.

The difference is 75 kW. If both cases remained at their stated load for eight hours, the conductor-energy difference would be 75 kW × 8 h = 600 kWh. This isolates one mechanism. It excludes transformer losses, converter losses, reactive effects beyond the stated power factor, additional auxiliaries, and any change in conductor design. It is not a total-system efficiency prediction or a construction specification.

Check the electrical accounting. We specified 10 MW delivered at the receiving boundary, so the sending source must cover that plus the modeled conductor heating. In this simplified comparison it supplies 10.100 MW in the first case and 10.025 MW in the second. If a diagram labels both ends 10 MW while also showing positive losses, the numbers do not balance. A clear diagram makes the receiving and sending boundaries visible.

## Test which assumptions make the result hold

Change the power factor to 0.80 while keeping delivered real power and voltage fixed. Current rises by 1/0.80 = 1.25. Conductor heating rises by 1.25 squared, or 1.5625. At 10 kV with the same resistance, the loss becomes 156.25 kW. Power factor has increased the current needed to deliver the same real power. It has not changed the stated 10 MW into 12.5 MW of real load.

Now change the conductor rather than the voltage. If the higher-voltage design uses a different resistance, the loss ratio becomes the current-squared ratio multiplied by the resistance ratio. A resistance twice as large would turn the earlier quarter-loss result into half the loss. You cannot keep saying one quarter after changing the assumption that produced it. This is why a comparison should display its fixed inputs next to the visual.

Higher transport voltage brings a real tradeoff. It can reduce current and conductor burden for a given transfer, but requires appropriate equipment and insulation interfaces and may change conversion placement. If a higher-voltage route needs an additional conversion stage, its losses belong in a whole-path comparison. The correct choice depends on the complete architecture, not only the elegant inverse-square relationship.

A useful failure test is to ask what happens if the required load doubles while the transport voltage and conductor remain unchanged. Current doubles and conductor heating becomes four times as large in the simplified model. Temperature-dependent resistance and equipment operating limits can make the actual response more complicated. The model gives an early warning about scaling, while the engineering design still requires the missing thermal, protection, and installation information.

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
