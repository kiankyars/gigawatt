# Count water at the boundary, then ask who can use the heat

**12. Heat rejection, climate and water**

Reconcile tower makeup and blowdown, distinguish withdrawal from consumption, and evaluate heat reuse against an actual receiving load.

**Driving question:** Can a facility improve one resource metric while making another site constraint harder?

## Recirculation is not the same as zero water demand

A cooling loop can circulate the same water repeatedly while still requiring makeup water. In an evaporative rejection system, some water leaves as vapor. Dissolved material does not leave in the same proportion, so the remaining water becomes more concentrated. Blowdown removes some concentrated liquid, and makeup replaces losses. Drift and leakage create additional paths. DOE’s cooling-tower guidance explains these mechanisms and the need to manage concentration within the actual water chemistry.

For a deliberately simple steady balance, ignore drift, leaks and storage changes. Let M be makeup, E evaporation and B blowdown. Water balance gives M = E + B. If makeup dissolved-solids concentration is c and blowdown concentration is Cc, a simplified solids balance gives Mc = BCc, so M = CB. Combining the equations yields B = E/(C − 1). C is the cycles-of-concentration ratio. This algebra is a bookkeeping model, not permission to select a treatment setting.

The distinction matters because a site can reduce blowdown while continuing to evaporate almost the same quantity for a given duty. Increasing the allowable concentration therefore does not eliminate water consumption. Chemistry, corrosion, deposition, biological control and equipment materials constrain the feasible regime. An alternative water supply can change freshwater demand but also introduce treatment, storage and reliability requirements. The source of water belongs in the design brief, not just in a favorable annual total.

## Make the numerator say what it measures

Withdrawal refers to water taken from a source; consumption concerns the portion not returned to the relevant water system in the accounting framework. Water delivered by a utility is also different from a facility directly withdrawing from a river or aquifer. The US Geological Survey distinguishes withdrawal and consumptive-use data because they answer different questions. At a data center, a supply meter alone cannot establish every downstream return flow, basin impact or upstream electricity-related water use.

In our synthetic day, evaporation is 100 cubic metres and cycles of concentration are five. With the simplified assumptions, blowdown is 25 cubic metres and makeup is 125. Suppose the 25 cubic metres are returned to the same accounting basin after suitable treatment, while evaporation is counted as consumption. The site then records 125 cubic metres of intake and 100 of consumption. If that return destination were unknown, the consumption conclusion would require qualification rather than an invented return credit.

Normalize only after stating the time and energy boundary. If IT used 100 MWh that day, intake intensity is 1.25 litres per IT kWh, and consumption intensity is 1 litre per IT kWh. Label each ratio by what it counts. The Green Grid’s water usage effectiveness (WUE), defined in 2011, divides a year of site water use in litres by IT equipment energy in kilowatt-hours. Its site water counts tower evaporation, blowdown and drift together, so it follows the intake side of this ledger. A one-day ratio is still a different quantity from a reported annual WUE. If facility energy is 120 MWh that day, its facility/IT energy ratio is 1.20. This one-day ratio is not an annual PUE report. None of these figures tells us useful training progress, watershed scarcity, water quality or the consequences of an outage in the makeup supply.

Evaporation is also a heat ledger. Turning liquid water into vapor absorbs its latent heat, about 2,430 kJ per kilogram at 30°C in the water tables of the NIST Chemistry WebBook from the US National Institute of Standards and Technology, so evaporating about 1.5 litres carries away 1 kWh. If the tower rejected the day’s 100 MWh of IT heat, its 100 cubic metres of evaporation would account for about 67 MWh, two-thirds of it. The cooling-tower chapter of the handbook from ASHRAE, the American Society of Heating, Refrigerating and Air-Conditioning Engineers, explains where the rest goes. Air passing through a tower gains heat in a latent part, which evaporates water, and a sensible part, which only warms the air, and the sensible share grows as the entering air gets colder. Rejecting all 100 MWh by evaporation alone would take about 150 cubic metres, so the water a tower uses for the same heat changes with the weather.

## Heat reuse needs a customer, a temperature and a clock

A stream of warm coolant is not automatically a useful heat product. The receiving process needs a temperature, flow, delivery pressure, schedule and reliability arrangement. Heat may need another exchanger or a heat pump before it is usable. Distribution requires pipework and pumping, and a backup rejection path may remain necessary when the customer shuts down. A reuse proposal should identify how much heat can actually be transferred across the receiver boundary rather than crediting the full IT load.

Consider a separate synthetic receiving load that can accept 2 MW for six hours, while the data center has 4 MW available continuously. The maximum directly accepted heat over those six hours is 12 MWh, assuming suitable temperatures and no distribution losses. The data center produces 96 MWh over the day, so this arrangement accounts for 12.5 percent of that heat. It leaves 84 MWh requiring another destination. A pipe connection is not evidence of year-round demand.

Whether reuse is preferable depends on the counterfactual and the constraints. Does it replace a receiving building’s fuel use, add electricity for a heat pump, or displace another low-emission source? Is the benefit delivered during the same hours that the data center needs rejection? Keep energy, water and emissions ledgers separate. The decisive comparison is a specified service arrangement against an alternative, with the assumptions that could reverse the answer visible.

## Case study: Abilene closes the coolant loop, then rejects heat to air

Crusoe’s August 2025 Abilene description specifies closed-loop facility water and air-cooled chillers for non-evaporative heat rejection. It separately accounts for initial fill and maintenance water. This dated design description is our recurring campus example, not an audited annual water balance.

Follow the mechanism: fluid circulates inside the system, heat crosses the chiller interfaces, and outdoor air receives the rejected heat. Closed-loop describes the fluid path. Non-evaporative describes the rejection process. Neither term means zero compressor work, zero maintenance water or unlimited capacity on a hot day.

Pause: would replacing the air-cooled rejection arrangement with an evaporative tower leave the water ledger unchanged merely because the equipment coolant loop stays closed? No. The equipment loop may still recirculate, while a separate tower circuit needs makeup water. Identify each circuit before applying a water-use claim to the whole campus.

## Case study: a Toronto carrier hotel kept power but lost cooling

Enwave’s district cooling system in downtown Toronto starts with cold water drawn from deep in Lake Ontario. Toronto Water treats that water for drinking. On its way into the city supply, it passes through heat exchangers at the John Street Pumping Station and absorbs heat from a separate district-cooling circuit. That circuit recirculates through downtown buildings, including the carrier hotel at 151 Front Street West, a building where many network operators interconnect, and returns to John Street to be cooled again. Lake water never reaches a server rack: the drinking-water flow and the district loop exchange heat without mixing.

On July 8, 2013, heavy rain flooded Hydro One’s Richview and Manby transmission stations and caused widespread outages across the Toronto area. Data Center Knowledge quoted PEER 1 the next day: the 151 Front Street West building transferred to generator power, while its external chilled-water provider also had power problems, so cooling fell. The same report said Enwave supplied an emergency chiller, which gave some relief until the system was restored.

Erik Levinson, chief technology officer of the tenant Uberflip, described the response on July 9 in a message to the North American Network Operators’ Group (NANOG) mailing list. One suite recovered sooner than another. In the hotter suite, cold-side cabinet air rose above 43°C and some equipment shut down automatically. Operators remotely stopped redundant and nonessential systems, moved some services to the cooler suite, and restored equipment once temperatures returned to normal. His account covers roughly 18:45 to 01:15.

The lake still held cold water. The weak link was the equipment that delivered the cooling, and it depended on the provider’s power supply rather than on the building’s generators. Backup generation protects only the loads connected to it. For each heat-removal path, list the services it needs, such as water supply, pumps and controls, and the power source behind each one.

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

Benefit: It removes evaporation from the site water ledger, which is 100 of the 125 m³ taken in each day in the worked example.

Cost: Dry rejection is limited by the dry bulb. In the weather lesson’s 84 kW example, 35°C air gives 45°C technology supply through the dry cooler against 35°C through the tower route at 22°C wet bulb, so on that day the dry route needs a chiller, a warmer qualified inlet or a lower load.

## When the situation changes

Trigger: A summer water restriction removes a tower mode assumed available in the design case.

Mechanism: A resource constraint changes the feasible heat path even while the electrical service remains intact.

## Apply the idea

Keep evaporation at 100 m³/day but use C = 3. What are makeup and intake intensity? Does evaporation decrease?

<details>
<summary>Reveal the worked answer</summary>

Blowdown is 50 m³/day, makeup is 150 m³/day and intake intensity is 1.50 L/kWh. Evaporation remains 100 m³/day by assumption.

Lower concentration requires more blowdown in this model. It increases intake by 25 m³/day without changing the stipulated evaporative heat-rejection requirement. The calculation does not establish which concentration is chemically feasible, and no treatment recommendation follows from choosing the lower numerical intake.

</details>

**The idea to keep:** Water, electricity and recovered heat have different boundaries and timing. Report them separately before deciding which architecture is preferable.

## Sources

- [DOE FEMP: Cooling Tower Management](https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management) — www.energy.gov · Reviewed 2026-09-06. Cooling towers lose water to evaporation and blowdown, makeup replaces it, and dissolved solids concentrate as water evaporates.
- [USGS National Water Availability Assessment Data Companion](https://waterdata.usgs.gov/blog/nwdc-overview/) — waterdata.usgs.gov · Published 2026-03-11 · Reviewed 2026-09-06. The water-use discussion distinguishes withdrawals from consumptive use.
- [Crusoe — Abilene cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) — Crusoe · Published 2025-08-05 · Reviewed 2026-09-12. Abilene provides a recurring example of grid supply, backup and closed-loop cooling with air-cooled heat rejection.
- [ASHRAE Handbook 2024 — Cooling Towers](https://handbook.ashrae.org/Handbooks/S24/IP/s24_ch40/s24_ch40_ip.aspx) — ASHRAE · Published 2024 · Reviewed 2026-09-26. Air passing through a tower absorbs heat in a sensible part and a latent part. Only the latent part evaporates water, and the sensible part grows as the entering air gets colder, so the average evaporation over a season falls below the design rate.
- [Enwave — Enwave and Toronto Water tap into innovative energy source](https://www.enwave.com/case-studies/enwave-and-toronto-water-tap-into-innovative-energy-source) — Enwave Energy Corporation · Reviewed 2026-09-26. Lake Ontario water treated for drinking passes heat exchangers at the John Street Pumping Station, which chill a separate district-cooling loop serving downtown Toronto buildings.
- [Hydro One — Power outages due to heavy rains, July 8, 2013](https://www.newswire.ca/news-releases/hydro-one-power-outages-due-to-heavy-rains-512697891.html) — Hydro One Inc., via Cision Newswire · Published 2013-07-08 · Reviewed 2026-09-26. Heavy rain flooded the Richview and Manby transmission stations and caused widespread outages in Brampton, Toronto and Mississauga.
- [Data Center Knowledge — Toronto Flooding KOs Data Center Cooling Systems, July 9, 2013](https://www.datacenterknowledge.com/outages/toronto-flooding-kos-data-center-cooling-systems) — Data Center Knowledge (Rich Miller) · Published 2013-07-09 · Reviewed 2026-09-26. PEER 1 said 151 Front Street moved to generator power while its chill-loop provider's power problems cut cooling; the article reports that Enwave supplied an emergency chiller for relief until the system was restored.
- [Erik Levinson (Uberflip) — What to expect after a cooling failure, NANOG mailing list, July 9, 2013](https://seclists.org/nanog/2013/Jul/130) — NANOG mailing list archive (seclists.org) · Published 2013-07-09 · Reviewed 2026-09-26. A tenant's firsthand account of the hotter suite passing 43°C on the cold side, automatic shutdowns, remote load shedding and transfers, from about 18:45 to 01:15.
- [NIST Chemistry WebBook — Saturation properties for water](https://webbook.nist.gov/cgi/fluid.cgi?Action=Load&ID=C7732185&Type=SatP&Digits=5&THigh=35&TLow=20&TInc=5&RefState=DEF&TUnit=C&PUnit=MPa&DUnit=kg%2Fm3&HUnit=kJ%2Fkg&WUnit=m%2Fs&VisUnit=uPa*s&STUnit=N%2Fm) — US National Institute of Standards and Technology (NIST Standard Reference Database 69) · Reviewed 2026-09-26. At 30°C the vapor and liquid enthalpies, 2,555.5 and 125.73 kJ/kg, give a latent heat of about 2,430 kJ/kg.
- [The Green Grid — White Paper #35: Water Usage Effectiveness (WUE): A Green Grid Data Center Sustainability Metric](https://www.thegreengrid.org/system/files/store/WUE_v1.pdf) — The Green Grid (editor Michael Patterson, Intel) · Published 2011-03-01 · Reviewed 2026-09-26. Site WUE divides annual site water usage by IT equipment energy, in L/kWh; site water includes humidification and tower evaporation, blowdown and drift, while off-site water for energy production belongs to WUEsource.

## Check your understanding: What reaches the condenser?

Pause and make a prediction, then compare your reasoning.

A hypothetical chiller removes 1.0 MW from its evaporator loop while its compressor consumes 0.2 MW. Ignore other heat transfers and exclude pumps and fans from this stated balance.

**Pause and predict:** How much heat must its condenser reject, and what is the cooling COP at this boundary?

<details>
<summary>Compare your reasoning</summary>

The condenser rejects 1.2 MW, and cooling COP is 1.0 / 0.2 = 5.

The condenser receives the cooling duty plus compressor work: 1.0 + 0.2 MW. Cooling COP uses the evaporator duty as its numerator. This balance does not establish outdoor equipment capacity under a given climate, or account for the excluded pumps and fans.

</details>

**The next problem:** We have traced the power, work and heat paths. What evidence proves that the delivered equipment can operate as one complete service?

Continue in **13. EPC**: The longest lead time is not the completion date.
