# Deliver the campus one usable phase at a time

**4. Siting, grid connection and supply**

Follow a real phased delivery, trace the electricity and fuel connections behind it, compare four supply arrangements, then weigh generation by its duty, its fuel and its date.

**Driving question:** How can a campus obtain usable power by its opening date?

## Begin with a released phase: CoreWeave at Polaris Forge 1

On October 27, 2025, Applied Digital reported the first 50 megawatts (MW) at Polaris Forge 1, in Ellendale, North Dakota, ready for service. Half of the building’s capacity was released while work on the other half continued. Twenty-eight days later, on November 24, the next 50 MW reached the same milestone and completed the first 100 MW building, which is leased to CoreWeave. The campus was fully contracted at 400 MW, and the October release described a possible expansion path to 1 gigawatt (GW). Applied Digital’s October 2025 investor presentation shows Building 1 from the air, below.

A supply decision answers four questions: how much usable capacity, on which date, through which connections, and in which operating states. Power, cooling, network access and finished space all have to reach the same block on the same date. Make the first block independently serviceable and it can go into service while construction continues around it. A cooling connection or network route shared with unfinished work can hold the block back even when its electrical feeder is ready.

Ready for service is a delivery milestone. The information technology (IT) power the tenant draws, the accelerators it installs and the tokens they produce come later, once the workload runs, and each needs its own measurement.

![Page 22 of Applied Digital’s October 2025 investor presentation, titled PF1 Building 1 (100 MW IT load), with two aerial photographs of the building, its rows of outdoor equipment and the construction around it.](../assets/references/applied-digital-polaris-forge-1-building1-october-2025.jpg)

Polaris Forge 1 Building 1 in Applied Digital’s October 2025 investor presentation. The capture days of the two photographs are not stated. [Applied Digital, October 2025 investor presentation, page 22](https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-25-000076/apld_invxfinalpresentati.htm)

## Abilene: one campus, several scopes

Abilene, Texas, is the real campus this course keeps returning to: the original Oracle and OpenAI campus built by Crusoe, followed through its service, construction and cooling. Crusoe describes that original campus as eight buildings and a 1,200 MW plan. Two nearby numbers belong to other scopes. Crusoe’s June 9, 2026 release lists a new 900 MW campus for Microsoft as a separate project, and the 10 GW commitment in OpenAI’s Stargate announcement covers Stargate’s wider US buildout.

Snapshot, September 2026. Oracle reports 75% of total Abilene capacity delivered, with the rest to follow in later quarters, and its aerial photograph below is dated July 15, 2026. Seventy-five percent of the 1,200 MW plan would be 900 MW if Oracle and Crusoe count capacity on the same basis. Oracle leaves that basis undefined and reports no operating megawatts, so 900 MW is a conditional estimate of delivered capacity, separate from any metered load. On March 27, 2026, Crusoe described two of the original buildings as energized and six more planned, an earlier point on the same timeline.

![Oracle aerial photograph of the Abilene campus under a cloudy sky: rows of large data-hall buildings with equipment yards and long covered galleries beside them, and graded construction ground to the right.](../assets/references/distribution-abilene-data-halls.jpg)

Abilene, Texas, in Oracle’s aerial dated July 15, 2026. [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/)

## Fuel arrives by pipe, in stages

A gas turbine is only as useful as the pipe that feeds it. Being near a pipeline gives a site somewhere to connect. Burning gas at scale takes four more things: a lateral (a branch line from the main to the site), the rights of way to build it, metering and pressure regulation at the fence, and enough upstream capacity to hold pressure with every turbine at full output. Each is a construction project with its own schedule, running alongside the turbine order.

Abilene shows the sequence. Energy Transfer began delivering gas to the Oracle data center near Abilene in January 2026, reported a second 14-mile lateral in the area completed by August, and signed a separate agreement with Crusoe for gas facilities to feed about 900 MW of generation. The fuel arrived in stages, as the power did.

Snapshot, August 2026. Sources: Energy Transfer’s fourth-quarter 2025 results, released in February 2026, and its August 2026 investor presentation. The roughly 900 million cubic feet per day (MMcf/day) of gas named in the February release covers three Oracle projects combined.

## A grid connection is studied, then built

Picture two campuses whose supply routes lead back to the same substation, the installation of transformers, switchgear and protection where transmission voltage is stepped down and circuits divide. Before either campus gets service, a connection study checks whether that substation and the lines above it can carry both campuses’ demand at once, together with other customers and the outages the grid must withstand. Sitting next to a transmission line gives a campus a place to connect. Study, upgrades and acceptance turn that place into usable capacity.

Between a large-load request and available service, the utility or grid operator may run studies, sign agreements, build network upgrades, wait for equipment, construct and authorize operation; the names and order of the steps vary by jurisdiction and project. The Electric Reliability Council of Texas (ERCOT), which runs the grid for most of Texas, announced a batch study in June 2026 that assesses several large projects together against the network they would share. A customer’s requested date is an input to that planning; the studies and upgrades determine when the grid can carry the load.

Abilene’s own grid connection arrived in two steps. Mortenson’s project page for the campus distinguishes the initial 200 MW connection at 138 kilovolts (kV) from the later 1 GW expansion at 345 kV, whose five transformers were all energized by March 10, 2026.

Inside the fence, the staging continues. Electrical equipment can be energized while cooling, control integration, network connections or IT acceptance are still under way. Commissioning checks how a stated scope behaves; operation then shows the service it delivers. A phased campus therefore carries several statuses at once, so track each released block apart from the construction that remains. A project-wide completion percentage, like Oracle’s 75% at Abilene, describes the whole campus, while acceptance is recorded block by block.

## Behind the meter names an electrical boundary

Behind the meter (BTM) means electrically on the customer’s side of a particular utility meter. Draw that meter between the grid and the customer bus, then connect the local generator, the storage and the site’s loads to the customer bus: everything on that side is behind the meter. A real campus can have several meters, so name the one a claim refers to. The electrical drawing settles it; the property line and the equipment’s owner answer other questions.

Four words describe four different things. On-site is a physical location. Behind the meter is an electrical relationship to a named meter. Islanded is a way of operating, disconnected from the wider grid, and off-grid describes a site that runs with no utility connection at all. An off-site power purchase agreement (PPA) is a contract to buy a generator’s output. The generator stays on the far side of the meter, and its energy reaches the campus through the grid, so losing the grid path cuts it off too.

The meter records the net exchange across the boundary. Local generation can shrink imports while the customer load stays the same and the grid stays connected, so a meter reading zero at some moment still describes a grid-connected site. Export works the same way in reverse: a site that exports stays physically tied to the grid, and permission to import is a separate agreement. These distinctions organize the four arrangements that follow.

## Four normal operating arrangements

Grid-supplied. The utility serves normal demand. The site may still have backup generators and an uninterruptible power supply (UPS); those belong to the continuity design. An off-site energy contract changes what the site buys, while the power still arrives over the same feeder.

Grid-parallel. Local generation and grid imports share the load while the site stays connected. The normal import can be much smaller than the import the site needs when a generator trips, so the design needs a plan for that larger number: reserved import capacity, reserve generation, storage or a planned cut in load. Export permission and the fallback states the site supports are settled site by site.

Export-only. Local generation serves the load, and the grid connection carries the surplus out. The agreement allows export only, so every watt the load uses comes from local generation. The site is still electrically connected to the grid. Backup import rights and the ability to survive as an island after a grid disturbance each need their own design and agreement.

Off-grid. The site runs on local resources alone. They carry the full continuing load and set the voltage and frequency themselves, so sustained generation, fast balancing, fuel, reserves and storage limits become one operating problem. Off-grid names the connection, and the resources can be of any kind: gas turbines, for example, or solar with storage sized explicitly for the night.

The four arrangements describe normal supply relationships. A complete design adds backup, switching, grounding, protection, auxiliary loads and storage. Meter location, import and export rights, and island capability are three related questions, and a site can answer each one differently.

## Bridge power can become backup

Crusoe’s 2025 Impact Report, published in May 2026, describes a 350 MW natural-gas plant at Abilene with two jobs: temporary bridge power, and a long-term backup role in place of diesel generators. One plant can therefore serve an early phase before permanent grid delivery arrives and stay on afterward as backup. At 350 MW it is under a third of the original 1.2 GW campus plan, so the backup design still has to name the loads it protects.

Moving from bridge to backup is an engineered change of duty. As bridge power, the plant carries the load in normal operation. As backup, it has to start and pick up the protected load when the grid fails, so its start and transfer behavior, protection settings, maintenance, fuel delivery and operating permissions all have to be designed for the new duty. The report describes the strategy, and each project’s own design sets the switch-over date and the redundancy.

## An island needs energy and a working electrical system

Losing the grid tests two things at once. The first is an energy balance: local generation and storage have to cover the whole protected load for as long as the outage lasts, within their power limits, their stored energy and their fuel. The second is a working electrical system: the site has to transfer to island operation, hold its voltage and frequency stable, and keep a surviving route from each source to the load. The worked example below runs the first test for a grid-parallel site. Its arithmetic gives how long each resource lasts, and the second test needs evidence of its own.

Three habits follow. Size the problem by the protected load on the bus, because the import the meter shows in normal operation is only the gap between that load and local generation. Check a store against both of its limits, its output power and its usable energy. And give each backup source its own fuel: a second generator on the same failed gas connection adds little protection against that failure.

## How simple-cycle and combined-cycle gas turbines make electricity

In a simple-cycle gas turbine, a compressor squeezes incoming air, fuel burns in the compressed air, and the hot gas expands through turbine blades. The turbine’s shaft work drives both the compressor and an electric generator. A starter turns the machine to get it going, and from then on burning fuel supplies all of the shaft work. Engineers model this process as the Brayton cycle. Because the machine draws air from the atmosphere and returns its exhaust there, it is also called open cycle, a name for the air path; how often the machine runs is a separate choice.

A combined-cycle plant sends that hot exhaust through a heat recovery steam generator (HRSG). Heat crosses into a separate water and steam circuit, whose own water becomes the steam while the exhaust stays apart. The steam expands through a steam turbine for more shaft work, a condenser rejects the remaining heat and turns the steam back into water, and a pump returns the water to the HRSG. That steam loop is the Rankine cycle. The description leaves out supplementary firing, in which the HRSG burns extra fuel of its own.

In GE Vernova’s cutaway below, follow the air through the compressor, combustors and turbine to the shaft that turns the generator. In Siemens Energy’s combined-cycle diagram, trace the hot exhaust and the water and steam loop separately through the heat recovery unit, steam turbine and condenser. Its “up to 64%” label is the manufacturer’s maximum efficiency.

![GE Vernova cutaway of a gas turbine driving a generator: air enters the compressor at left, combustors glow orange mid-engine, hot gas passes through the turbine, and a shaft connects to the generator at right.](../assets/references/siting-ge-vernova-gas-turbine-cutaway.jpg)

Gas turbine and generator. The image carries no labels: from the left, compressor, combustors and turbine share one shaft, which turns the generator on the right. [GE Vernova, What Is a Gas Turbine?](https://www.gevernova.com/gas-power/resources/education/what-is-a-gas-turbine)

![Siemens Energy combined-cycle diagram: gas-turbine exhaust flows into a heat recovery unit, steam drives a steam turbine and a second generator, a condenser returns the water, and both generators connect to the grid. A label reads combined cycle efficiency levels of up to 64%.](../assets/references/siting-siemens-energy-combined-cycle.jpg)

Siemens Energy’s combined-cycle principle. The up-to-64% label is the manufacturer’s maximum. [Siemens Energy, Combined Cycle Power Plants](https://www.siemens-energy.com/global/en/home/products-services/product/combined-cycle-power-plants.html)

## Compare fuel at equal output

Compare the two at equal output with round numbers: each plant delivers 100 MW of net electricity, the simple-cycle plant at 40% net efficiency and the combined-cycle plant at 60%. The simple-cycle plant burns 100 ÷ 0.40 = 250 MW of fuel energy and leaves 150 MW unrecovered. The combined-cycle plant burns 100 ÷ 0.60 = 166.7 MW and leaves 66.7 MW. Heat rate states the same comparison per unit of output: 2.5 megawatt-hours (MWh) of fuel for each MWh of electricity against 1.67 MWh.

All of these numbers use the fuel’s lower heating value (LHV), the heat released by burning it when the water vapor formed in combustion leaves uncondensed. The higher heating value (HHV) also counts the heat recovered by condensing that vapor, so it is the larger of the two. The choice changes the denominator of every efficiency and heat rate, so quote fuel prices and efficiencies on the same basis, and keep net and gross output apart for the same reason.

The comparison holds output fixed across two separate plants. Add a steam cycle to an existing gas turbine instead and the output grows, because the recovered exhaust heat drives the extra steam turbine. The price is more plant: the HRSG, steam turbine, condenser, water and cooling systems all add construction, capital, maintenance and operating dependencies. GE Vernova’s 2025 gas power catalog sums up the trade: simple cycle has the simpler capital and construction profile, and combined cycle the higher efficiency. The actual schedule of either still depends on equipment delivery, fuel, permits and site works.

## A real combined-cycle plant: Dania Beach

Florida Power & Light’s (FPL’s) Dania Beach Clean Energy Center, near Fort Lauderdale, puts the mechanism in a real utility plant. Two GE 7HA.03 gas turbines pass their exhaust heat to a steam cycle, and GE Vernova reports up to 1,260 MW for the whole plant, steam cycle included. The model name reads as a code: 7 is the 60 hertz (Hz) family, H stands for high efficiency, A for air-cooled, and .03 is the model version.

GE Vernova’s May 2025 fact sheet gives catalog values for a 7HA.03 combined-cycle block with one gas turbine and one steam turbine, a 1×1 configuration: 640 MW net at 63.9% LHV efficiency, a rapid-response hot start in under 30 minutes, a ramp rate of 75 MW per minute and a minimum load of 26%. The values apply to a net plant burning natural gas at the International Organization for Standardization (ISO) reference conditions. They describe the catalog design, while Dania Beach’s day-to-day performance depends on its own configuration and conditions. The hot-start figure applies to a warm plant; a cold start needs a figure of its own.

## Baseload, intermediate duty and peaking are roles

Grid demand has a floor and a shape. Baseload is the floor, present through the whole interval. Intermediate, or mid-merit, duty covers the long periods above that floor, and peaking duty covers the short intervals of highest demand. The U.S. Energy Information Administration (EIA) describes combined-cycle plants serving base and intermediate load and simple-cycle turbines commonly covering the peaks. Those are typical roles with loose edges: combined cycle can follow load, and engines, storage and other resources also provide peaking service.

Siemens Energy’s conceptual dispatch charts, below, set a conventional supply stack beside a system with much more wind and solar. In the second, the demand left after wind and solar, called the residual load, swings sharply even when total demand changes slowly, and flexible plants have to follow it. A steady artificial intelligence (AI) campus adds demand in the hard hours as well as the easy ones, so what matters for a new campus is the spare generation and transmission in the hardest hours, which its annual energy total leaves hidden.

“Fast” has three meanings, each on its own clock. Building a plant takes as long as its equipment delivery, permits, fuel connection and construction. Starting an existing plant depends on its thermal state, so a start time names the state, as the fact sheet’s hot start does. Changing the output of a running plant depends on its controls and limits, such as the ramp rate and minimum load. A catalog ramp rate belongs to the third clock only. Actual dispatch also depends on reserves, outages, network constraints and fuel availability.

![Two Siemens Energy weekly capacity charts. Left, a conventional fossil-fuel system: a flat base-load block with intermediate and peak load on top. Right, a system with high wind and solar: a lower base-load block and a large, rapidly varying load-following band that fills the gaps between wind and solar output.](../assets/references/siting-siemens-energy-peaker-dispatch.png)

Conceptual weekly dispatch from Siemens Energy, not measured grid data. [Siemens Energy, Peaker Plants](https://www.siemens-energy.com/global/en/home/products-services/product/peaker-plants.html)

## Hours decide the cost, and speed decides the date

Efficiency costs money up front, and fuel savings pay it back over the hours a plant runs. Keep the same two 100 MW plants and give them round annual costs. Capital and fixed operating costs, spread over the years, come to $8 million a year for simple cycle and $16 million for combined cycle. Fuel costs $20 per MWh of fuel energy on the LHV basis, so with the heat rates above, each MWh of electricity needs $50 of fuel from the simple-cycle plant and $33.33 from the combined-cycle plant.

Annual cost is the fixed cost plus 100 MW × equivalent full-load hours × fuel cost per MWh. Equivalent full-load hours are the year’s electricity output divided by the 100 MW rating, so two hours at half output count as one. At 500 hours a year, simple cycle costs $10.50 million against combined cycle’s $17.67 million. At 7,000 hours, combined cycle costs $39.33 million against $43.00 million. The two lines cross at 4,800 hours, where combined cycle’s extra $8 million of fixed cost is exactly repaid by fuel savings of $16.67 per MWh.

A data center runs close to all 8,760 hours of the year, far past the crossover. There the model gives simple cycle $8 million + $43.8 million = $51.8 million against combined cycle’s $16 million + $29.2 million = $45.2 million. On annual cost, combined cycle wins at data-center duty. Simple cycle’s case at a campus is speed to power: the simpler plant can start serving the load sooner.

Price that speed with the same model. At 8,760 hours, simple cycle burns $14.6 million more fuel than combined cycle, and its fixed costs are $8 million lower, so the net penalty for choosing it is $14.6 million − $8 million = $6.6 million a year. If simple cycle opens one month earlier, that month pays for the choice when its contribution, what it earns after the costs of serving it, exceeds $6.6 million plus any premium for the faster build that the $8 million leaves out. Those serving costs include the fuel either plant would burn, so the extra fuel is counted once, inside the $6.6 million. The fuel gap alone would set the bar at $14.6 million; the fixed-cost saving brings it down to $6.6 million.

The model prices one year and leaves out start costs, variable maintenance, emissions prices, part-load performance, downtime and project financing. The fuel gap recurs every year the plant runs, so a longer comparison sets the whole period’s extra fuel, capital, financing, maintenance and availability against the value of the early months. Construction speed, delivered fuel, water, cooling and the service requirement can rule out either plant before cost comes into it. Efficiency is also a separate question from whether the plant can island, provide redundancy or keep the campus in service, which are the continuity questions above.

## Southaven: a simple-cycle plant and the price of speed

xAI’s Colossus 2 data center is on Tulane Road in Memphis, Tennessee. MZX Tech LLC’s generating plant is at 2875 Stanton Road South in Southaven, Mississippi, across the state line. SemiAnalysis’s September 2025 account attributes the cross-border siting to pushback in Tennessee and to Mississippi’s permitting route for temporary turbines, and reports medium-voltage (MV) connections between the sites. Neighboring parcels can answer to different permitting authorities, while the power still crosses between them on a physical connection.

MZX Tech’s January 2026 permit application, prepared by Trinity Consultants as its January 14, 2026 cover email records, proposed 41 simple-cycle turbines with about 1.2 GW of generating nameplate for the site’s own use. The site map and process drawing below come from that application and show the proposal as it stood then. The process drawing connects conditioned gas to the turbines, and the turbines’ electricity to the data center and to battery packs. It was drawn for an air permit, so it carries emissions branches and leaves switching and voltages to the electrical design.

SemiAnalysis’s later procurement account describes imported power modules and medium-voltage delivery used to avoid the long lead times of large transformers. The next lesson, “Move power with fewer amperes”, prices that trade by carrying 200 MW at 34.5 kV and at 161 kV: fewer transformer stages in exchange for more current.

The permission was temporary by design. Mississippi’s July 2025 determination attached mobility and less-than-twelve-month conditions to the turbines’ temporary treatment. On July 30, 2026, SpaceXAI reported an agreement to remove 69 temporary turbines by July 2027 while building permitted permanent generation. A different plant shares the town’s name: the Tennessee Valley Authority’s (TVA’s) Southaven combined-cycle station.

The compute contracts show what earlier capacity can earn. SpaceX’s June 2026 prospectus discloses fees from Anthropic of $1.25 billion a month after a May–June ramp, for compute across Colossus and Colossus II. A separate filing with the Securities and Exchange Commission (SEC) puts Google’s fees at $920 million a month, with reduced ramp fees until the full fees begin in October 2026. Together that is $2.17 billion a month before costs, earned only while the service is delivered under each agreement’s delivery and termination terms. The fees are revenue: SpaceX’s AI segment, which also includes X, Grok, research and development (R&D) and infrastructure, reported $2.561 billion of revenue and a $1.257 billion operating loss in the second quarter of 2026, and the filings give neither contract’s margin nor a megawatt figure that ties the fees to Southaven. SemiAnalysis describes the prices as a premium for large-scale compute available soon and forecasts recovery of the capital expenditure (capex) in under a year; its 3–5 months is the delivery lead time. The $6.6 million bar above belongs to the round-number 100 MW model, and testing any real plant against such a bar takes a contribution margin, which these revenue disclosures leave undisclosed.

![Original MZX Southaven proposed site map with yellow facility boundary and Airbus 2025 imagery credit.](../assets/references/southaven-site-plan.png)

MZX application, January 2026 revision, site map (PDF page 80). The image carries its Airbus imagery credit. Historical proposed facility area. [MZX Tech / Trinity Consultants — site map](https://upload.wikimedia.org/wikipedia/commons/e/e2/MZX_Tech_LLC_Draft_Air_PSD_Construction_Permit.pdf#page=80)

![Original Trinity Consultants process diagram connecting natural gas, turbine generation, data center and battery packs.](../assets/references/southaven-process-plan.png)

Figure 2-1, July 2025, in the January 2026 application (PDF page 13). Air-permit process diagram, including its emissions branches. [MZX Tech / Trinity Consultants — process figure](https://upload.wikimedia.org/wikipedia/commons/e/e2/MZX_Tech_LLC_Draft_Air_PSD_Construction_Permit.pdf#page=13)

## Carry the supply plan into the site decision

Land, fiber, climate, water, electrical service, equipment access and local rules all push on one another. A site with earlier grid availability may need a cooling design that changes its auxiliary power and its delivery date. A location with cheap energy may add network latency to the workload or leave a hard path to expansion. Sort the requirements into conditions a site must pass and tradeoffs among the sites that pass. A weighted score works for the tradeoffs. A hard requirement is a gate, and a site that fails it is out, however well it scores elsewhere.

Treat a missing fact as open, with a name attached. If an application needs a maximum network round-trip time, a location outside it fails however cheap it is. If a cooling design depends on a water allocation that is still pending, record the allocation as unresolved, along with the party or document that could settle it. On-site supply can make an earlier phase possible, and it brings fuel, emissions, cooling, control and maintenance dependencies of its own.

Finish by writing the service envelope: how much load, starting when, under which normal and degraded conditions, and with which uncertainties still open. That turns a comparison of locations into an infrastructure decision, and it points further work where it pays most: at the dependency that sets the delivery date, the capacity that limits accepted load, or the operating condition that would break the service promise.

## Worked example: Ride through a grid outage on local generation and storage

- A grid-parallel customer bus supplies 8 MW, including cooling, controls and downstream losses.
- A stable local generator supplies 6 MW net and holds four hours of fuel at that output.
- Storage holds 4 MWh of usable output energy with a 3 MW output limit at this bus, and is idle while the grid is connected.
- After the grid is lost, authorized and stable island operation is taken as already in place.

1. Normal import — 8 MW − 6 MW = 2 MW — The meter sees 2 MW, while the site remains an 8 MW load.
2. Deficit after grid loss — 8 − 6 = 2 MW, within the 3 MW output limit — Storage has enough output power to replace the lost import.
3. Storage duration — 4 MWh ÷ 2 MW = 2 h — Usable energy divided by the deficit gives the time storage can carry it.
4. Binding limit — min(2 h storage, 4 h fuel) = 2 h — Storage runs out before the generator’s fuel does.
5. Protect 6 MW instead — 6 − 6 = 0 MW deficit, so fuel binds at 4 h — Cutting protected demand to the generator’s output removes the storage deficit and leaves the fuel limit.

**Result:** The site imports 2 MW in normal operation. Islanded, it carries the full 8 MW for two hours, when storage runs out; protecting 6 MW extends that to the generator’s four hours of fuel.

**Model boundary:** All values are hypothetical and are not Abilene equipment specifications. The arithmetic gives durations only; a successful transfer, stable voltage and frequency, a surviving electrical route and an independent fuel supply each need their own evidence.

## When the situation changes

Trigger: Treat the earliest energized subsystem as a completed site.

Mechanism: A later building, cooling, fiber, or acceptance dependency prevents the intended service.

Response: Track complete blocks and keep readiness, commissioning, and observed operation as separate evidence states.

## Apply the idea

A proposed first phase has an energized feeder and installed racks, but its coolant return and network entrance are shared with unfinished later work. What evidence would justify releasing it? Separately, a local gas plant normally cuts grid imports: what must be shown before calling it backup?

<details>
<summary>Reveal the worked answer</summary>

Show accepted cooling and network service for the released block, safe separation from the ongoing work, and the intended operating limits. For backup, show the protected load, starting and transfer behavior, independent surviving paths, fuel, controls and usable capacity.

An energized feeder is one completed dependency. A released phase needs all the required services and supported operating states. A generator’s location and normal output describe normal operation; taking over the load during the failure being considered is a separate duty with its own evidence.

</details>

**The idea to keep:** Plan supply one released phase at a time. Each phase needs energy that can be delivered on its date, a connection that can carry it, and a design for the states it must survive, such as losing the grid.

## Sources

- [ERCOT — Batch Zero large-load connection announcement, June 18, 2026](https://www.ercot.com/news/release/06182026-puct-approves-ercots) — www.ercot.com · Published 2026-06-18 · Reviewed 2026-09-06. Large-load connection studies consider shared network capacity and required upgrades.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — ASHRAE · Reviewed 2026-09-06. Commissioning and handover can occur in smaller infrastructure blocks with documented acceptance.
- [DOE — Islanding a Microgrid](https://www.energy.gov/cmei/femp/articles/islanding-microgrid) — www.energy.gov · Published 2021-10-15 · Reviewed 2026-09-10. Grid-connected and islanded operation require a coordinated system of sources and loads.
- [NARUC — Regulators’ Financial Toolbox: Behind-the-Meter Energy Storage](https://pubs.naruc.org/pub/6233DBE2-B58B-52FF-925E-250DD26DECF9) — pubs.naruc.org · Reviewed 2026-09-10. Behind-the-meter describes the customer side of the utility meter; it can include resources that exchange power with the grid.
- [DOE — Solar Integration: Distributed Energy Resources and Microgrids Basics](https://www.energy.gov/cmei/systems/solar-integration-distributed-energy-resources-and-microgrids-basics) — www.energy.gov · Reviewed 2026-09-10. Local generation and designed island operation are distinct; many solar systems disconnect during loss of the wider grid.
- [US EPA — Physical PPA](https://www.epa.gov/green-power-markets/physical-ppa) — www.epa.gov · Reviewed 2026-09-10. A physical PPA is a purchase arrangement that may involve on-site or off-site generation; an off-site project can deliver through the grid.
- [Crusoe — Abilene campus development update](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) — Crusoe · Published 2026-03-27 · Reviewed 2026-09-12. Historical March 27 milestone separating the original Abilene campus from the adjacent Microsoft development.
- [GE Vernova — How a combined-cycle plant produces electricity](https://www.gevernova.com/gas-power/resources/education/combined-cycle-power-plants) — GE Vernova · Reviewed 2026-09-12. Gas turbine shaft work, exhaust heat recovery in an HRSG, and steam-turbine electricity production.
- [EIA — Natural gas generation by technology and region](https://www.eia.gov/todayinenergy/detail.php?id=61444) — U.S. Energy Information Administration · Published 2024-02-22 · Reviewed 2026-09-12. Combined-cycle generation serves base and intermediate duty; simple-cycle gas turbines commonly cover shorter peak periods.
- [GE Vernova — 7HA gas-turbine and combined-cycle fact sheet](https://www.gevernova.com/content/dam/gepower-new/global/en_US/downloads/gas-new-site/products/gas-turbines/7ha-fact-sheet-product-specifications.pdf) — GE Vernova · Published 2025-05 · Reviewed 2026-09-12. 7HA.03 1×1 combined-cycle catalog: 640 MW net, 63.9% LHV efficiency, <30 min rapid-response hot start, 75 MW/min ramp and 26% minimum load.
- [GE Vernova — First 7HA.03 commercial operation at FPL Dania Beach](https://www.gevernova.com/gas-power/resources/case-studies/first-7ha-florida-power-light) — GE Vernova · Reviewed 2026-09-12. Two 7HA.03 gas turbines and up to 1,260 MW at FPL’s Dania Beach plant, with a manufacturer photograph of the plant.
- [GE Vernova — 2025 Gas Power Catalog, plant configuration comparison](https://www.gevernova.com/content/dam/gepower-new/global/en_US/downloads/noindexpdf/GEA35241-GE-Vernova-Gas-Power-Catalog.pdf) — GE Vernova · Published 2025 · Reviewed 2026-09-12. Simple-cycle construction and capital simplicity versus combined-cycle efficiency and additional steam-cycle equipment.
- [Applied Digital Achieves Ready for Service for Phase 1 at Polaris Forge 1](https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at) — Applied Digital · Published 2025-10-27 · Reviewed 2026-09-16. First 50 MW of the first 100 MW building at Polaris Forge 1 in Ellendale, North Dakota reached ready-for-service on October 27, 2025.
- [Applied Digital Completes Phase II Ready for Service at Polaris Forge 1](https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at) — Applied Digital · Published 2025-11-24 · Reviewed 2026-09-16. Second 50 MW of the first building reached ready-for-service November 24, 2025, bringing that building to 100 MW.
- [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/) — Oracle · Reviewed 2026-09-17. Reports 75% of total Abilene capacity delivered as of September 2026, with aerial photographs dated July 15, 2026.
- [Energy Transfer August 2026 Investor Presentation](https://ir.energytransfer.com/static-files/1cb70dca-abed-4005-95aa-793e3345626c) — Energy Transfer · Published 2026-08 · Reviewed 2026-09-12. Records completion of a second 14-mile Abilene lateral and a separate gas-facilities agreement with Crusoe to support approximately 900 MW of generation.
- [Energy Transfer Reports Fourth Quarter 2025 Results](https://ir.energytransfer.com/node/52241/pdf) — Energy Transfer · Published 2026-02-17 · Reviewed 2026-09-12. Reports that natural-gas delivery to the Oracle data center near Abilene began in January 2026, separately from later expansion agreements.
- [Crusoe 2025 Impact Report](https://media.ffycdn.net/us/crusoe/PL5TuZz5apXB9pVsd3H1.pdf) — Crusoe · Published 2026-05-28 · Reviewed 2026-09-26. Pages 16 and 19 describe a 350 MW natural-gas plant and temporary bridge power with a long-term backup role at Abilene. Page 33 documents the Sparks solar-and-battery case.
- [Combined Cycle Power Plants](https://www.siemens-energy.com/global/en/home/products-services/product/combined-cycle-power-plants.html) — Siemens Energy · Reviewed 2026-09-12. Explains how a combined-cycle plant pairs a gas turbine with a steam cycle, with a full-system diagram and single-shaft and multi-shaft layouts.
- [Peaker Plants](https://www.siemens-energy.com/global/en/home/products-services/product/peaker-plants.html) — Siemens Energy · Reviewed 2026-09-12. Compares conventional generation roles with renewable-driven load following and explains why fast, flexible gas generation is useful.
- [What Is a Gas Turbine?](https://www.gevernova.com/gas-power/resources/education/what-is-a-gas-turbine) — GE Vernova · Reviewed 2026-09-12. Explains the compressor, combustion, turbine and generator of a gas turbine, with a manufacturer cutaway of the machine.
- [Crusoe’s Contracted AI Infrastructure Capacity Approaches 5 Gigawatts Across Data Centers and Cloud](https://www.crusoe.ai/resources/newsroom/crusoes-contracted-ai-infrastructure-capacity-approaches-5-gigawatts-across-data-centers-and-cloud) — Crusoe · Published 2026-06-09 · Reviewed 2026-09-16. Separates the original 1.2 GW Oracle Abilene campus from a distinct 900 MW Microsoft campus.
- [Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) — Mortenson · Reviewed 2026-09-14. Reports five expansion transformers energized by March 10, 2026, and distinguishes the initial substation from the later expansion.
- [MZX Tech LLC — Southaven PSD permit application, January 2026 revision](https://upload.wikimedia.org/wikipedia/commons/e/e2/MZX_Tech_LLC_Draft_Air_PSD_Construction_Permit.pdf) — MZX Tech LLC / Trinity Consultants; public record released by MDEQ, Wikimedia mirror · Published 2026-01-14 · Reviewed 2026-09-12. Original Southaven site and area maps and generating-plant process figure; historical proposed 41 simple-cycle turbines and approximately 1.2 GW.
- [SpaceX — EU prospectus, compute services agreements with Anthropic](https://content.spacex.com/cms-assets/FINAL_Documents%20and%20Updates/SpaceX%20-%20EU%20Prospectus%20%28Approved%20by%20Bafin%29%20-%20June%205%2C%202026.pdf) — Space Exploration Technologies Corp. · Published 2026-06-05 · Reviewed 2026-09-12. Section 4.3.4.5: approximately 325,000 GPUs across Colossus and Colossus II; $1.25B monthly fees through May 2029, with reduced ramp fees and termination provisions.
- [SpaceX — Google Cloud Service Agreement, free writing prospectus](https://www.sec.gov/Archives/edgar/data/1181412/000162828026041150/spacexagreementfwp.htm) — Space Exploration Technologies Corp. / SEC · Published 2026-06-05 · Reviewed 2026-09-12. Approximately 110,000 GPUs and $920M monthly service fees from October 2026, with reduced ramp fees, delivery conditions and 90-day termination rights.
- [SpaceX — second-quarter 2026 Form 10-Q, AI segment results](https://www.sec.gov/Archives/edgar/data/1181412/000162828026052535/spcx-20260630.htm) — Space Exploration Technologies Corp. / SEC · Published 2026-08-04 · Reviewed 2026-09-12. Separates service-fee run rates from reported results: Q2 AI segment $2.561B revenue and $1.257B operating loss; cloud-service revenue timing and customer cancellation exposure.
- [SemiAnalysis — Meta Compute: Everyone Wants To Be A Neocloud](https://newsletter.semianalysis.com/p/meta-compute-everyone-wants-to-be) — SemiAnalysis · Published 2026-07-02 · Reviewed 2026-09-12. Analyst account of premium pricing for near-term large-scale SpaceX compute and why short cancellation rights differentiate these deals.
- [GE Vernova — 7HA gas turbines, model family and specifications](https://www.gevernova.com/gas-power/products/gas-turbines/7ha) — GE Vernova · Reviewed 2026-09-12. Identifies 7HA.03 as a 60 Hz air-cooled H-class gas-turbine model; distinguishes simple-cycle turbine output from complete combined-cycle plant output.
- [U.S. Department of Energy — heating-value glossary](https://www.energy.gov/cmei/fuels/glossary) — U.S. Department of Energy · Reviewed 2026-09-12. Defines lower and higher heating value and the role of condensing combustion water vapor.
- [Applied Digital — October 2025 investor presentation](https://ir.applieddigital.com/sec-filings/all-sec-filings/content/0001144879-25-000076/apld_invxfinalpresentati.htm) — Applied Digital · Published 2025-10 · Reviewed 2026-09-13. Page 22 shows two aerial photographs of Polaris Forge 1 Building 1.
- [GE — How its latest gas turbine could save Florida customers money](https://www.ge.com/news/reports/in-the-money-how-ges-latest-gas-turbine-could-help-save-florida-customers-300-million) — GE · Published 2019-10-03 · Reviewed 2026-09-13. GE naming explanation: H means high efficiency, A means air-cooled. Dania Beach uses a combined-cycle design.
- [GE Vernova — Supporting Vietnam’s energy needs](https://www.gevernova.com/gas-power/resources/articles/2021/supporting-vietnams-energy-needs) — GE Vernova · Published 2021-03-15 · Reviewed 2026-09-13. Distinguishes 7HA for 60 Hz grids from 9HA for 50 Hz grids.
- [SpaceXAI — Greater Memphis site update, July 30, 2026](https://x.ai/memphis/updates) — SpaceXAI · Published 2026-07-30 · Reviewed 2026-09-13. Reports agreement to remove 69 temporary Southaven turbines by July 2027 while building permitted permanent generation.
- [MDEQ — Determination letter on portable gas combustion turbines, July 29, 2025](https://cdn.mississippitoday.org/wp-content/uploads/2025/11/20104011/2025.07.29-MDEQ-Determination-Letter-on-Portable-Gas-Combustion-Turbines-signed.pdf) — Mississippi Department of Environmental Quality · Published 2025-07-29 · Reviewed 2026-09-13. Historical determination includes mobility and less-than-twelve-month conditions for the temporary-turbine treatment.
- [MLGW — 2025 xAI Update](https://www.mlgw.com/images/content/files/pdf/new/xAI%202025%20Update.pdf) — Memphis Light, Gas and Water · Published 2025 · Reviewed 2026-09-13. Locates the Tulane Road Colossus 2 facility near the Tennessee–Mississippi state line.
- [xAI's Colossus 2 - First Gigawatt Datacenter In The World, Unique RL Methodology, Capital Raise](https://newsletter.semianalysis.com/p/xais-colossus-2-first-gigawatt-datacenter) — SemiAnalysis · Published 2025-09-16 · Reviewed 2026-09-13. Cross-border Colossus 2 / Southaven siting and reported MV connection; SemiAnalysis attributes the siting to different temporary-turbine permitting routes.
- [OpenAI: Five new Stargate sites](https://openai.com/index/five-new-stargate-sites/) — openai.com · Reviewed 2026-09-13. The 10 GW commitment concerns Stargate’s wider US buildout, distinct from the Abilene campus plan and current operating load.
- [US Census TIGERweb — Tennessee state boundary and Tulane Road geocode](https://tigerweb.geo.census.gov/arcgis/rest/services/TIGERweb/State_County/MapServer/0) — US Census Bureau · Reviewed 2026-09-14. Places the Tennessee–Mississippi state line between the Tulane Road site in Memphis and the Southaven plant site.
