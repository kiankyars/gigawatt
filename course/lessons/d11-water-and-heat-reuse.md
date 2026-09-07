# Count water at the boundary, then ask who can use the heat

**D11 · Authored draft · Objectives:** D11.4, D11.5

Reconcile tower makeup and blowdown, distinguish withdrawal from consumption, and evaluate heat reuse against an actual receiving load.

**Driving question:** Can a facility improve one resource metric while making another site constraint harder?

## Recirculation is not the same as zero water demand

A cooling loop can circulate the same water repeatedly while still requiring makeup water. In an evaporative rejection system, some water leaves as vapor. Dissolved material does not leave in the same proportion, so the remaining water becomes more concentrated. Blowdown removes some concentrated liquid, and makeup replaces losses. Drift and leakage create additional paths. DOE’s cooling-tower guidance explains these mechanisms and the need to manage concentration within the actual water chemistry.

For a deliberately simple steady balance, ignore drift, leaks and storage changes. Let M be makeup, E evaporation and B blowdown. Water balance gives M = E + B. If makeup dissolved-solids concentration is c and blowdown concentration is Cc, a simplified solids balance gives Mc = BCc, so M = CB. Combining the equations yields B = E/(C − 1). C is the cycles-of-concentration ratio. This algebra is a bookkeeping model, not permission to select a treatment setting.

The distinction matters because a site can reduce blowdown while continuing to evaporate almost the same quantity for a given duty. Increasing the allowable concentration therefore does not eliminate water consumption. Chemistry, corrosion, deposition, biological control and equipment materials constrain the feasible regime. An alternative water supply can change freshwater demand but also introduce treatment, storage and reliability requirements. The source of water belongs in the design brief, not just in a favorable annual total.

## Make the numerator say what it measures

Withdrawal refers to water taken from a source; consumption concerns the portion not returned to the relevant water system in the accounting framework. Water delivered by a utility is also different from a facility directly withdrawing from a river or aquifer. USGS distinguishes withdrawal and consumptive-use data because they answer different questions. At a data center, a supply meter alone cannot establish every downstream return flow, basin impact or upstream electricity-related water use.

In our synthetic day, evaporation is 100 cubic metres and cycles of concentration are five. With the simplified assumptions, blowdown is 25 cubic metres and makeup is 125. Suppose the 25 cubic metres are returned to the same accounting basin after suitable treatment, while evaporation is counted as consumption. The site then records 125 cubic metres of intake and 100 of consumption. If that return destination were unknown, the consumption conclusion would require qualification rather than an invented return credit.

Normalize only after stating the time and energy boundary. If IT used 100 MWh that day, intake intensity is 1.25 litres per IT kWh, and consumption intensity is 1 litre per IT kWh. Explicitly label these ratios rather than casually assigning an unspecified WUE label. If facility energy is 120 MWh that day, its facility/IT energy ratio is 1.20. This one-day ratio is not an annual PUE report. None of these figures tells us useful training progress, watershed scarcity, water quality or the consequences of an outage in the makeup supply.

## Heat reuse needs a customer, a temperature and a clock

A stream of warm coolant is not automatically a useful heat product. The receiving process needs a temperature, flow, delivery pressure, schedule and reliability arrangement. Heat may need another exchanger or a heat pump before it is usable. Distribution requires pipework and pumping, and a backup rejection path may remain necessary when the customer shuts down. A reuse proposal should identify how much heat can actually be transferred across the receiver boundary rather than crediting the full IT load.

Consider a separate synthetic receiving load that can accept 2 MW for six hours, while the data center has 4 MW available continuously. The maximum directly accepted heat over those six hours is 12 MWh, assuming suitable temperatures and no distribution losses. The data center produces 96 MWh over the day, so this arrangement accounts for 12.5 percent of that heat. It leaves 84 MWh requiring another destination. A pipe connection is not evidence of year-round demand.

Whether reuse is preferable depends on the counterfactual and the constraints. Does it replace a receiving building’s fuel use, add electricity for a heat pump, or displace another low-emission source? Is the benefit delivered during the same hours that the data center needs rejection? Keep energy, water and emissions ledgers separate. The decisive comparison is a specified service arrangement against an alternative, with the assumptions that could reverse the answer visible.

## Worked example: A synthetic tower water ledger

- One day; E = 100 m³/day, concentration ratio C = 5.
- Negligible drift, leaks and storage change; dissolved solids leave through blowdown.
- IT electricity is 100 MWh/day. Blowdown is assumed returned to the same accounting basin after appropriate treatment.

1. Blowdown — B = 100/(5 − 1) = 25 m³/day — Solve the water and simplified solids balances together.
2. Makeup — M = 100 + 25 = 125 m³/day — This is the measured intake requirement under the assumptions.
3. Intake intensity — 125,000 L / 100,000 kWh = 1.25 L/kWh — Both numerator and denominator cover the same day.
4. Consumption intensity — 100,000 L / 100,000 kWh = 1.00 L/kWh — This conclusion depends on the specified return-flow accounting.

**Result:** Intake and consumption differ even though both are associated with the same cooling system.

**Model boundary:** This is not a water-treatment prescription, site WUE certification, or watershed impact assessment.

## The tradeoff

Choice: Select a dry-rejection alternative for a water-constrained brief.

Benefit: It can reduce direct evaporative water demand at the site.

Cost: The alternative still needs evidenced thermal capacity, fan/compressor electricity, footprint and high-ambient performance; indirect resource effects remain separate.

## When the situation changes

Trigger: A summer water restriction removes a tower mode assumed available in the design case.

Mechanism: A resource constraint changes the feasible heat path even while the electrical service remains intact.

Response: Evaluate the specified alternate rejection mode and permitted workload response; do not assume nameplate cooling survives the restriction.

## Apply the idea

Keep evaporation at 100 m³/day but use C = 3. What are makeup and intake intensity? Does evaporation decrease?

<details>
<summary>Reveal the worked answer</summary>

Blowdown is 50 m³/day, makeup is 150 m³/day and intake intensity is 1.50 L/kWh. Evaporation remains 100 m³/day by assumption.

Lower concentration requires more blowdown in this model. It increases intake by 25 m³/day without changing the stipulated evaporative heat-rejection requirement. The calculation does not establish which concentration is chemically feasible, and no treatment recommendation follows from choosing the lower numerical intake.

</details>

**The idea to keep:** Water, electricity and recovered heat have different boundaries and timing. Report them separately before deciding which architecture is preferable.

## Sources and reading boundaries

- [DOE FEMP: Cooling Tower Management](https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management) — Evaporation, blowdown, makeup and concentration mechanisms support the simplified conservation example. Read 2026-09-06. Overview and water-balance discussion inspected; no chemical dosing, operating limit or treatment procedure is reproduced.
- [USGS National Water Availability Assessment Data Companion](https://waterdata.usgs.gov/blog/nwdc-overview/) — The water-use discussion distinguishes withdrawals from consumptive use. Read 2026-09-06. Selected definitions inspected; the lesson’s hypothetical return-flow assumption is not an observation about a real basin.
