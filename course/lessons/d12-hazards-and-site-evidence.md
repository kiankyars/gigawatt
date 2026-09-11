# Choose a site that can deliver the first phase

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d12-hazards-and-site-evidence`, then run `uv run gigawatt-expand`.

**D12 · Authored draft · Objectives:** D12.2

Compare two parcels by usable area, utility delivery, cooling, fiber, land rights and permissions. Follow the constraint that prevents opening, rather than choosing the largest tract.

**Driving question:** Which parcel can support the required campus, with usable land and services ready on time?

## Start with a campus requirement, not a land listing

In this original example, the first phase needs 60 MW delivered at the customer bus, including the stated campus auxiliaries, a 40-acre campus envelope, two physically separate fiber routes, and opening by month 24. The campus envelope includes the buildings, electrical and cooling plant, access and service areas. It is a supplied layout requirement, not an acres-per-megawatt rule. Compare every parcel against that same brief.

A parcel’s price and acreage cannot establish whether that campus can be built. A utility line may be nearby without available capacity. A large tract may lose useful area to drainage or existing rights of way. A land option may expire before the project can resolve its conditions. Keep each unresolved fact visible; a weighted score cannot compensate for a condition that prevents the first phase.

## Confirm the power and fuel that can reach the site

Obtain the capacity, delivery point, required upgrades, operating restrictions and date from the actual utility process. A substation rating is not a commitment to supply that amount to this customer. D03 develops the electrical service boundary; here the question is whether the proposed parcel can obtain that service on the project schedule.

An on-site gas plant replaces some electrical dependencies with fuel dependencies. Establish required gas volume and pressure, supply and transportation terms, curtailment conditions, and the tap, metering, lateral and any compression needed to connect. Confirm who builds them, when, and across whose land. DOE’s gas-turbine guidance explains why insufficient pressure can require a fuel-gas compressor. Owning a generator and seeing a gas pipeline on a map do not answer those questions.

## Draw the land that the campus can actually use

Parcel A has 100 gross acres. The example excludes 25 acres for drainage and flood constraints and a separate, nonoverlapping 15 acres of easements, leaving 60 usable acres. Parcel B has 72 gross acres, with 12 acres of drainage exclusion and 8 separate easement acres, leaving 52. Both exceed the supplied 40-acre campus envelope. Real exclusion polygons can overlap; calculate their union rather than subtracting the same ground twice.

The supplied area screen assumes a contiguous envelope with suitable access. It does not establish foundation design. A topographic survey, grading and drainage plan, geotechnical investigation, equipment routes and expansion layout resolve different questions. USDA warns that regional soil surveys are not site-specific evaluations and do not test for toxic spills. A flood can also disable an off-site substation, bridge or fuel route while leaving the building dry: trace the dependency beyond the fence.

## Match cooling and fiber to the actual design

For cooling, establish the available water source, allocation, quality and discharge conditions against the chosen heat-rejection design and local weather. A recirculating loop can still need makeup water; dry cooling instead changes the equipment and hot-weather operating requirements. D11 owns those heat and water calculations. Here, retain the resulting capacity and readiness conditions in the site comparison.

For communications, verify capacity, route length, delivery dates, site entrances and the rights to construct each route. Two carrier contracts can share a trench or bridge. In this example, two physically separate routes are a stated requirement; Parcel B’s second route arriving in month 23 is the last supplied prerequisite. Its first route arriving earlier does not satisfy both paths.

## Secure the parcel and the rights across it

Purchase, lease and option arrangements give different rights for different periods. Check the actual terms for investigations, access, assignment, closing conditions and extensions, then compare their dates with the utility and permit work. Review title exceptions, recorded easements and the additional routes needed to bring power, gas, fiber and water to the campus. A line crossing another owner’s property needs its own established right; control of the main parcel does not supply it.

In Texas, the surface and mineral estates can have different owners. The Railroad Commission explains that mineral development can carry rights to reasonably necessary surface use, subject to applicable limits. A surface purchase alone therefore does not settle potential mineral-development conflicts. The example assumes Parcel B’s required rights are resolved through month 26. Parcel A’s option ends in month 18 with no agreed extension; that is unresolved control, not a date that can silently slide to month 30.

## Check permitted uses, neighbors and what the old site leaves behind

Identify the approvals and conditions for this layout: land use, air emissions, noise, water, drainage, construction and fire access. Equipment intended for continuous generation can raise different questions from standby equipment. Nearby homes, schools and other sensitive uses affect the actual siting conversation. A permit for one phase does not establish approval for the later campus.

Industrial reuse may offer roads, utility connections and a building, while also carrying obsolete equipment or contamination. EPA distinguishes historical and site-condition review from sampling and cleanup planning. Establish what can remain, what must be removed, and any restrictions on the intended use. An apparently empty contamination folder is not equivalent to completed investigation.

## Two real connections show why the delivery details matter

MLGW’s 2025 xAI update describes the Paul Lowery Road campus in the former Electrolux facility: an existing 16-inch gas main served the site, and xAI paid for an 8-inch tap. The same dated update describes additional gas capacity at the separate Tulane Road site as still under study. Infrastructure reuse, a funded connection and a pending service study are three different states. This historical record does not establish either site’s September 2026 capacity.

Energy Transfer’s Q2 2026 presentation reports an agreement to construct gas-delivery facilities for Crusoe’s Abilene expansion. It verifies an infrastructure agreement, not completed service. A separate slide bullet about a completed Abilene lateral does not identify that lateral as the Crusoe project. Neither case supports casually saying that an AI company built a regional pipeline.

## Worked example: The smaller parcel meets the opening brief

- Original hypothetical brief: 60 MW net at the customer bus, including auxiliaries; 40 contiguous usable acres; two physically separate fiber routes; opening by month 24.
- Parcel A: 100 gross acres minus 25 drainage/flood acres and 15 nonoverlapping easement acres. Parcel B: 72 minus 12 and 8 respectively. Layout fit, soil suitability and access within the remaining envelope are supplied assumptions.
- Accepted-readiness months for power, civil works, cooling/water, two fiber routes and permits: A = 30, 20, 20, 21, 22; B = 22, 21, 20, 23, 21. These are teaching inputs, not project forecasts.
- A’s land option ends in month 18 without an agreed extension; its proposed gas bridge has no established volume, pressure or lateral rights. B’s required land and service rights are resolved through month 26; its permitted first phase does not rely on gas generation.
- All other prerequisites, including the supplied Phase I/II findings and any required remediation, are assumed resolved for B. The model screens stated conditions; it is not engineering or legal approval.

1. Usable area — A: 100 − 25 − 15 = 60 ac; B: 72 − 12 − 8 = 52 ac — Both fit the supplied 40-acre envelope. The larger acreage is not the deciding constraint.
2. Earliest service date — A: max(30, 20, 20, 21, 22) = month 30; B: max(22, 21, 20, 23, 21) = month 23 — A misses the month-24 brief. B waits for its second fiber route.
3. Control and fuel — A: option ends at 18 < 30; gas bridge unresolved. B: control through 26 > 23 — A needs a new land agreement and evidence for any alternative supply. The proposed gas plant cannot be credited as available power.
4. First-phase selection — B: 52 ≥ 40 ac; 60 MW; month 23 ≤ 24 — B passes the declared screen with 12 acres outside the initial envelope. That remainder is not proven future MW.

**Result:** Select Parcel B for the supplied brief. Parcel A’s extra land does not resolve its later power date or expired land-control assumption.

**Model boundary:** Area exclusions are disjoint and dimensions schematic. Dates represent supplied accepted readiness. No actual site, contract, water allocation, gas capacity, permit or construction program is approved by this example.

## The tradeoff

Choice: Favor a smaller parcel whose first-phase services and rights are established.

Benefit: It can meet the stated opening date without relying on unresolved supply or land extensions.

Cost: Less remaining land may constrain expansion; future capacity still needs its own layout and service evidence.

## When the situation changes

Trigger: Two nominal fiber providers share the only bridge into the site, or the required independent route slips.

Mechanism: The network requirement fails even though the campus buildings and power are ready.

Response: Verify the physical routes and delivery obligation; revise the opening plan or the service requirement explicitly.

## Apply the idea

Parcel B’s second fiber route is delayed from month 23 to month 28. Its land-control period still ends in month 26. Does the parcel still meet the brief?

<details>
<summary>Reveal the worked answer</summary>

No. Earliest readiness becomes month 28, after both the month-24 opening deadline and the month-26 control period.

A replacement route or changed service requirement would need explicit acceptance. A land extension would solve only the control problem, not the month-24 deadline. Neither change can be assumed from the original parcel choice.

</details>

**The idea to keep:** Nearby infrastructure and gross acreage are starting points. A site needs usable space, enforceable rights and services that meet the same capacity and date.

## Sources and reading boundaries

- [National Weather Service: Flood Related Hazards](https://www.weather.gov/safety/flood-hazards) — Flood mechanisms differ and can affect low-lying and urban infrastructure through rainfall and overflow. Read 2026-09-06. Public hazard descriptions inspected; no local elevation, flood probability or engineering requirement is inferred.
- [USGS: What is seismic hazard?](https://www.usgs.gov/faqs/what-seismic-hazard-what-a-seismic-hazard-map-and-how-are-they-used) — Seismic hazard maps incorporate fault, propagation and near-surface site information. Read 2026-09-06. FAQ reviewed; it is not a parcel assessment or a code-specific structural design input.
- [DOE — Beyond Land Leases: Harnessing Data Centers for Tribal Economic Development](https://www.energy.gov/indianenergy/beyond-land-leases-harnessing-data-centers-tribal-economic-development-webinar) — DOE speakers connect land, power access, water and cooling choices, fiber, roads, local impacts and development timing. Read 2026-09-11. Reviewed introductory transcript, especially the siting discussion. Speaker-specific projects and claimed performance are not adopted as general data-center facts.
- [USDA NRCS — Understanding Soil Risks and Hazards](https://www.nrcs.usda.gov/sites/default/files/2023-01/Understanding-Soil-Risks-and-Hazards.pdf) — Soil-survey limitations distinguish regional screening from parcel-specific investigation and contamination testing. Read 2026-09-11. Reviewed introduction and Limitations of Soil Surveys, not every hazard chapter. No parcel conditions or geotechnical design values are established.
- [Railroad Commission of Texas — Oil and Gas Exploration and Surface Ownership](https://www.rrc.texas.gov/about-us/faqs/oil-gas-faq/oil-gas-exploration-and-surface-ownership/) — Texas surface and mineral estates can be separately owned; mineral development can entail reasonably necessary surface use subject to applicable limits. Read 2026-09-11. Texas-specific general guidance. It neither determines the title of a particular parcel nor prescribes the rights needed for a data-center transaction.
- [EPA — Eligible Brownfields Planning Activities](https://www.epa.gov/brownfields/eligible-planning-activities) — Phase I environmental assessment examines site history and conditions; Phase II can investigate contamination; cleanup planning depends on intended reuse. Read 2026-09-11. Reviewed planning and assessment descriptions. Funding eligibility and liability protections are not inferred for any teaching parcel.
- [MLGW — 2025 xAI Update](https://www.mlgw.com/images/content/files/pdf/new/xAI%202025%20Update.pdf) — The Paul Lowery Road site reused the Electrolux facility and an existing 16-inch gas main; xAI paid for an 8-inch tap. The update separately describes a pending gas-capacity study at Tulane Road. Read 2026-09-11. Historical 2025 utility update, not September 2026 operating status. The tap is not evidence that xAI built a regional gas pipeline; the two sites and their service states must remain distinct.
- [Energy Transfer — Q2 2026 investor presentation](https://ir.energytransfer.com/static-files/c29697db-5336-4262-8bf3-3c6e409ccb19) — Printed slide 3 reports a Q2 2026 agreement to construct gas-delivery facilities for Crusoe’s Abilene campus expansion. Read 2026-09-11. Primary search-extracted slide text reviewed; full PDF fetch returned HTTP 403. An agreement is not operational completion. A separate bullet about a completed 14-mile Abilene lateral is not attributed to Crusoe without explicit linkage.
- [DOE — CHP Technologies: Gas Turbines](https://betterbuildingssolutioncenter.energy.gov/sites/default/files/attachments/CHP_Gas_Turbines.pdf) — The fuel-supply discussion explains that insufficient site gas pressure requires a fuel-gas compressor. Read 2026-09-11. Primary searchable PDF excerpt reviewed; full fetch returned HTTP 502. No generic pressure, efficiency or cost is adopted as an actual data-center turbine specification.
