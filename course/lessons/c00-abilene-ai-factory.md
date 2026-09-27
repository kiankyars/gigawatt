# Abilene: putting an AI factory together

**16. Putting an AI Factory Together**

Follow the original Crusoe-built campus for Oracle and OpenAI in Abilene, Texas, from its GB200 workload through gas generation, air-cooled heat rejection and parallel construction to the deals that fund it.

**Driving question:** Why does the Abilene AI factory have this combination of infrastructure, financing and delivery choices?

## One campus, from workload to finance

Abilene, Texas is this course's recurring real campus: the original campus that Crusoe built for Oracle, whose cloud runs OpenAI's training and inference. Construction began in June 2024, and Crusoe reports that the first two buildings were energized within a year. The plan grew to eight buildings and 1.2 GW. Crusoe has also broken ground on a second, 900 MW campus in Abilene for Microsoft; that is a separate project with its own figures. Each choice below answers a requirement set somewhere else in the system, which is why the campus reads best as one machine.

The workload comes first. Crusoe's September 2025 announcement says Oracle began delivering the first NVIDIA GB200 racks in June 2025 and that the first phase was running on Oracle Cloud Infrastructure (OCI); OpenAI reports that it had begun early training and inference there. Each rack sets three requirements for the building: electrical power, heat removal by cold plates plus air for the heat the cold plates miss, and a network fabric that ties the racks together. Working backward sizes the power. In the Chapter 8 rack-power ledger, 72 kW at the processor rails needs 90.26 kW on the rack's DC bus once regulator losses and 12 kW of other rack loads are added, and 93.05 kW at its AC inlet after the power shelf's conversion loss. Those are Chapter 8's example numbers, and the method carries over to Abilene: start from the chips, add each conversion loss and support load, and arrive at the facility's demand.

## Gas generation: bridge first, backup later

Abilene has 350 MW of on-site gas generation. Crusoe's 2025 Impact Report calls the turbines temporary bridge power and long-term backup, and says they replace diesel backup; selective catalytic reduction was added to cut their nitrogen oxide emissions. The same equipment therefore serves a delivery role first and a continuity role later. As bridge power it lets halls operate before the grid alone could supply them, at the cost of a fuel supply, emissions controls and a plant to run.

As backup, the plant's rating has to be compared with the load it would carry. 350 MW is about 29 percent of the 1.2 GW plan, so in a grid outage the plant could carry only part of a fully built campus, and the published sources do not say which loads it would keep running. The worked example compares the rating with the first phase, the full plan and Oracle's delivered share.

![Aerial photograph of the Abilene gas-turbine plant: rows of turbine units with exhaust stacks in the foreground and data-hall buildings behind them on the left.](../assets/references/finale-abilene-turbine-2026.jpg)

Abilene's gas-generation plant beside the data halls, in Oracle's aerial captioned July 15, 2026. [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/)

## Cooling: rejecting heat without evaporating water

The racks' heat must reach the outdoors, and a campus can choose among three routes. Direct dry cooling passes facility water through coils cooled by outdoor air, which works when the air is cool enough relative to the required water temperature. An air-cooled chiller uses refrigeration to make colder water and rejects its heat to outdoor air. A water-cooled chiller paired with a wet cooling tower rejects its heat through the tower, which evaporates water that has to be replaced. Here air-cooled describes the outdoor heat rejection; the GPUs themselves are still cooled by liquid through cold plates.

Crusoe chose air-cooled chillers on a closed loop of facility water, so heat rejection evaporates no water. It estimates about 50,000 gallons per building each year for maintenance and water quality, separate from the initial fill, and says it accepted higher lifecycle and maintenance costs “in the interest of responsible water management.” A wet tower lets a chiller condense at a lower temperature and so can use less compressor electricity, at the price of makeup water, water treatment and tower upkeep. Crusoe publishes no priced alternative or water-price assumptions, so the lifetime cost comparison stays open. Emissions from the on-site gas plant are a separate question from water use.

## Delivery: build in parallel, grow around live work

Crusoe built electrical equipment while the buildings went up. Its Impact Report describes in-house switchgear manufacture and prefabricated electrical skids for Abilene, and its September 14, 2026 release reports more than 2,500 switchboards supplied to Abilene from its Tulsa operations. Factory assembly and site construction proceed at the same time and meet at installation and testing. A factory-complete package still has to match its electrical interfaces and leave room for installation and maintenance before a hall can operate.

The campus also grew around live work. The first phase ran OpenAI workloads while construction continued toward eight buildings joined by an integrated network fabric. Each new phase has to connect its power, cooling and network to shared campus systems while the halls already in service keep running; the general engineering answer is to keep each new interface isolated until its phase is ready. Crusoe targeted the first two buildings for energization in the first half of 2025 and the six additional buildings for mid-2026. Oracle reported 75 percent of Abilene's total capacity delivered as of September 2026, with the rest expected in later quarters. Oracle leaves the basis of that percentage undefined, so converting it into megawatts requires an assumption about that basis.

![Oracle aerial of the Abilene campus: rows of data halls, steel framing still exposed in places, long lines of outdoor equipment beside them, and cleared ground on the right where construction continues.](../assets/references/distribution-abilene-data-halls.jpg)

Abilene data halls in Oracle's aerial captioned July 15, 2026. [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/)

## Capital: a hierarchy of deals

Three companies share the operating stack. Crusoe designs, builds and operates the physical campus. Oracle provides the GPU cloud infrastructure, and Crusoe's June 2026 announcement calls the 1.2 GW campus purpose built for Oracle. OpenAI runs training and inference on that infrastructure.

A joint venture sits at the base of the campus's capital stack. In October 2024 Crusoe, Blue Owl-managed funds and Primary Digital Infrastructure announced a $3.4 billion venture for the first phase: 206 MW in two buildings, fully leased long term to a hyperscale tenant the announcement did not name. In May 2025 the same partners announced the second phase, the six additional buildings, of a $15 billion joint venture to fund the 1.2 GW campus. The $15 billion is the venture's size; it is neither a GPU bill nor an amount to add to the earlier $3.4 billion. Blue Owl's funds supply institutional capital, the first phase also drew on construction financing, and Primary Digital co-sponsors the venture and advised on the first-phase transaction. The investors' return rests on the lease: long-term rent and the value of the property. Crusoe keeps the development and operating role, and Primary Digital describes its mission as buying stabilized assets so that developers can recycle capital into their next projects. Each partner's share, cash contribution, fees and target return remain private, so any estimate of a partner's return rests on assumptions.

Keep three budgets apart. The joint venture pays for the physical campus, Oracle pays for the GPU infrastructure it installs, and OpenAI pays Oracle for the compute it uses. Adding the venture's $15 billion to a GPU purchase or to OpenAI's cloud bill would count different layers of one system as a single sum.

## The data center is the machine

Read the campus outward from the rack. The GB200 workload sets requirements for power, cooling and fast connections. Across a hall, those become distribution and cooling systems serving rows of machines. Across the campus, they require substations, outdoor cooling, generation, land and financing. A hardware choice becomes a facility design. The course follows that design both ways: electricity from the site boundary to the chips, and heat from the chips back out.

## Worked example: How far does 350 MW of gas generation reach?

- On-site gas generation: 350 MW (Crusoe 2025 Impact Report).
- First phase: two buildings and 206 MW (Crusoe, October 2024). Full plan: eight buildings and 1,200 MW (Crusoe, March 2025).
- Oracle: 75 percent of total capacity delivered as of September 2026, on a basis it does not define.

1. First phase — 350 / 206 = 1.70 — On ratings alone, the plant is 1.7 times the first phase, so it could bridge that phase before the grid expansion.
2. Full plan — 350 / 1,200 = 0.29 — The plant's rating is about 29% of the planned campus.
3. Delivered share — 0.75 × 1,200 = 900 MW; 350 / 900 = 0.39 — This holds only if Oracle's percentage uses the same basis as the 1.2 GW plan, which Oracle does not say.

**Result:** The plant's rating can cover an early phase but is under a third of the full plan, so as backup it can carry only part of the planned campus unless load is reduced or other supply joins.

**Model boundary:** Ratings only, compared on the bases the sources publish, which they leave undefined (IT or facility, nameplate or available). Generator availability, fuel supply, transfer equipment and the loads a backup must carry are not public, so no Abilene backup design follows from these ratios.

## The tradeoff

Choice: Reject heat with air-cooled chillers instead of wet cooling towers.

Benefit: Heat rejection evaporates no water; Crusoe estimates about 50,000 gallons per building each year for maintenance and water quality, plus the initial fill.

Cost: Crusoe reports higher lifecycle and maintenance costs, and an air-cooled chiller can need more compressor electricity than one rejecting heat through a wet tower.

## Apply the idea

A news summary says Blue Owl paid for Abilene's GPUs. Which layer does the Blue Owl and Primary Digital venture fund, who supplies the GPU infrastructure, and what would you need before calculating any partner's return?

<details>
<summary>Reveal the worked answer</summary>

The venture funds the physical campus that Crusoe builds and operates. Oracle supplies the GPU cloud infrastructure, and OpenAI pays for the compute it uses. A partner's return needs its ownership share, cash contribution, fees and the lease terms, which the announcements do not disclose.

Facility financing, GPU investment and cloud spending are separate layers of the same campus. The lease links the first two: rent from the tenant supports the facility investors' return, while the tenant's hardware and customer contracts sit above it.

</details>

**The idea to keep:** A hardware choice becomes a facility design. At Abilene the GB200 workload set the power, cooling and network requirements, and gas generation, air-cooled chillers, factory-built electrical equipment and a lease-backed investment answer them.

## Sources

- [Crusoe — Flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) — Crusoe · Published 2025-09-30 · Reviewed 2026-09-17. Construction began in June 2024, the first two buildings were energized within a year, and Oracle began delivering the first GB200 racks in June 2025; the first phase runs on OCI with early training and inference, within a planned eight-building campus on one integrated network fabric.
- [OpenAI: Five new Stargate sites](https://openai.com/index/five-new-stargate-sites/) — openai.com · Reviewed 2026-09-13. OpenAI says the flagship Abilene campus is running on OCI, that Oracle began delivering the first GB200 racks in June 2025, and that OpenAI has started early training and inference workloads there.
- [Crusoe — Expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) — Crusoe · Published 2025-03-18 · Reviewed 2026-09-17. Plans eight buildings and 1.2 GW, with the first two buildings and more than 200 MW targeted for energization in the first half of 2025 and six more buildings for mid-2026.
- [Crusoe 2025 Impact Report](https://media.ffycdn.net/us/crusoe/PL5TuZz5apXB9pVsd3H1.pdf) — Crusoe · Published 2026-05-28 · Reviewed 2026-09-26. Describes 350 MW of on-site gas generation at Abilene as temporary bridge power and long-term backup that replaces diesel backup, with selective catalytic reduction for nitrogen oxides (printed pp. 16, 19), and in-house switchgear and prefabricated electrical skids for the campus (p. 16).
- [Crusoe — Crusoe Opens Second Tulsa Manufacturing Facility](https://www.crusoe.ai/resources/newsroom/crusoe-opens-second-tulsa-factory-ai-infrastructure) — Crusoe · Published 2026-09-14 · Reviewed 2026-09-26. On September 14, 2026, Crusoe reported that its Tulsa operations had supplied more than 2,500 switchboards to the flagship Abilene site, among electrical equipment that includes medium-voltage switchgear, enclosures, controls and copper busbar.
- [Crusoe — Abilene cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) — Crusoe · Published 2025-08-05 · Reviewed 2026-09-12. Abilene uses closed-loop facility water and air-cooled chillers; Crusoe estimates about 50,000 gallons per building a year for maintenance and water quality and accepted higher lifecycle and maintenance costs to conserve water.
- [Trane — Air vs. Water Cooled Chillers](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html) — Trane · Published 2019-10-31 · Reviewed 2026-09-11. Air-cooled chillers avoid cooling-tower water treatment and tower maintenance; water-cooled systems can use less compressor energy.
- [Crusoe’s Contracted AI Infrastructure Capacity Approaches 5 Gigawatts Across Data Centers and Cloud](https://www.crusoe.ai/resources/newsroom/crusoes-contracted-ai-infrastructure-capacity-approaches-5-gigawatts-across-data-centers-and-cloud) — Crusoe · Published 2026-06-09 · Reviewed 2026-09-16. Crusoe calls the 1.2 GW Abilene campus purpose built for Oracle, among its projects contracted to hyperscale clients, and reports breaking ground on a separate 900 MW Abilene campus for Microsoft.
- [Crusoe — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) — Crusoe · Published 2024-10-15 · Reviewed 2026-09-26. On October 15, 2024, Crusoe, Blue Owl-managed funds and Primary Digital Infrastructure announced a $3.4 billion joint venture that jointly sponsors the first phase: a 206 MW, two-building data center that Crusoe designs, builds and operates, 100 percent leased long term to an unnamed Fortune 100 hyperscale tenant. Primary Digital describes its mission as buying stabilized assets from developers and operators so that they can recycle capital.
- [Crusoe — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter second phase of $15 billion joint venture](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture) — Crusoe · Published 2025-05-21 · Reviewed 2026-09-26. On May 21, 2025, Crusoe, Blue Owl-managed funds and Primary Digital Infrastructure announced the second phase, the six additional buildings, of a $15 billion joint venture to fund the 1.2 GW Abilene campus.
- [Kirkland & Ellis — Kirkland advises Blue Owl funds on JV and financing for development of Abilene data center](https://www.kirkland.com/news/press-release/2025/01/kirkland-ellis-advises-bo-funds-on-jv-and-financing-for-development-of-adc) — Kirkland & Ellis · Published 2025-01-23 · Reviewed 2026-09-26. The $3.4 billion first-phase joint venture closed alongside a $2.3 billion construction loan arranged by JPMorgan Chase, and Primary Digital Infrastructure facilitated and advised on the transaction.
- [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/) — Oracle · Reviewed 2026-09-17. Oracle reports 75 percent of total Abilene capacity delivered as of September 2026, with the rest in later quarters, and publishes campus and turbine-plant aerials captioned July 15, 2026.
