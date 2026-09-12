# The longest lead time is not the completion date

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d13-delivery-dependencies`, then run `uv run gigawatt-expand`.

**D13 · Authored draft · Objectives:** D13.1

Build a dependency graph, compare site-built and prefabricated delivery of the same 20 MW phase, and decide which work a late rack change actually delays.

**Driving question:** Which delay actually changes the date when a phase can deliver service?

## Make the endpoint a service condition

A schedule needs a precise finish condition. Equipment delivered, building energized and customer service accepted are different endpoints. Suppose our endpoint is a hypothetical first phase whose electrical, cooling and information paths have passed the specified integrated acceptance. Working backward from that condition exposes the necessary predecessors. It also reveals items that do not belong in the first-phase path, rather than forcing the entire future campus into one opening date.

A dependency is a statement that one activity needs an output from another. Procurement may require approved interfaces, installation may require both a delivered assembly and an available room, and integrated testing may require controls, safe test conditions and completed subsystem checks. Some work runs in parallel. Adding every duration produces an unnecessarily late date; taking only the largest individual duration usually produces an implausibly early one.

The GAO schedule guide explains why a reliable integrated schedule matters to cost and change assessment. Our exercise uses an original small dependency network to demonstrate the calculation. It excludes calendars, resource contention and probability distributions so that the dependency logic remains visible. Those exclusions matter later: a mathematically consistent plan with one specialist assigned to simultaneous tasks may still be impossible to execute.

## Calculate forward, then find the constraint

Start requirements work at week zero and finish after two weeks. The hypothetical electrical package takes eighteen weeks after those requirements, so delivery occurs at week twenty. Its installation then takes three weeks, finishing at week twenty-three. Cooling procurement takes ten weeks after requirements, followed by four weeks of installation, and finishes at week sixteen. Utility work starts at zero and finishes at week sixteen. All durations are exercise inputs, not current supplier lead times.

Integrated controls and acceptance need all three paths and then take four weeks. Their earliest start is the maximum predecessor finish: max(23, 16, 16) = week twenty-three. Acceptance therefore finishes at week twenty-seven. The electrical chain is critical in this deterministic example. Its eighteen-week procurement is the longest single activity, but the service date includes requirements, installation and the final integration work too.

The cooling path finishes seven weeks before it is needed by the final join. Advancing it by four weeks does not change the earliest service date while the electrical path remains unchanged. Delaying it by eight weeks moves its finish to week twenty-four and pushes acceptance to week twenty-eight. Slack is conditional on the rest of the current schedule; it is not a permanent entitlement to delay work without consequence.

## Recalculate after each intervention

An expedited electrical package that arrives four weeks earlier moves its installation finish to week nineteen and acceptance to week twenty-three. That four-week benefit assumes the installation team, room and test resources are also available earlier. If their calendars remain fixed, the purchased acceleration may become waiting time. A commercial promise to shorten one delivery therefore needs to be evaluated against the rest of the route to usable service.

A change can also create a different critical path. If utility readiness slips to week thirty, even the original electrical installation at week twenty-three is no longer controlling the final join. Acceptance now ends at week thirty-four. Expediting the electrical package cannot recover those seven weeks of utility delay. The next useful action would address the actual predecessor or alter the scope of the accepted phase, with any changes reviewed explicitly.

Keep forecasts and evidence separate when updating the network. A reported shipment date is not installation complete; installation complete is not a passed test. Record the status date, remaining work and basis for durations. Compare the current forecast with the approved baseline to understand the change, while resisting the temptation to move dates merely to make a dashboard appear healthy. The purpose of scheduling is to expose consequences early enough to make a meaningful decision.

## EPC responsibility and manufacturing strategy answer different questions

Consider one illustrative 20 MW IT phase divided into ten 2 MW service zones. Initially each zone serves twenty 100 kW racks. Compare assembling its distribution and cooling services in the building with delivering factory-built service modules. Keep the IT duty, required operating conditions and acceptance endpoint fixed. This is an original comparison, not an Abilene construction account or a supplier delivery claim.

EPC means engineering, procurement and construction: it describes the responsibilities assigned in a delivery scope. In this example, the owner contracts one EPC team to coordinate the design, purchase the packages, deliver the site works and integrate the completed systems against the owner’s requirements. Site-built versus prefabricated describes where and how assemblies are made. That same EPC scope can use either strategy or a mixture; a module vendor does not acquire responsibility for the whole facility merely by delivering a tested product. The actual contract must assign the boundaries and acceptance duties.

In the site-built route, factories still manufacture switchgear, cooling equipment and other components. Site trades install supports, assemble distribution and pipework, connect controls and integrate those products in the building. In our prefabricated route, the module factory fits a transportable service frame with electrical distribution, manifolds, internal wiring and controls, and checks the specified internal assemblies before shipment. Site teams still deliver access and foundations, utility and plant connections, unloading and placement, connections between modules and the building, IT rack installation and integrated acceptance. A factory test cannot demonstrate a site connection that did not exist during that test.

## Put the factory and the site on parallel schedule branches

Use a separate controlled schedule for these two routes. Week zero means approved interfaces and available components; upstream equipment lead times have already elapsed equally for both options. All durations are stipulated. Site enabling takes eight weeks. In the site-built route, service assembly then takes six weeks, followed by two weeks of integrated acceptance: 8 + 6 + 2 = week 16. This comparison does not replace the earlier week-27 procurement example.

For the prefabricated route, factory assembly and its internal checks take six weeks while the eight-week site branch runs in parallel. Transport takes one week after the factory release. Setting and site connections take two weeks after both the module arrival and site readiness, then the same two-week integrated acceptance follows: max(6 + 1, 8) + 2 + 2 = week 12. The four-week advance comes from overlapping assembly with site work under these assumptions. It is not a universal percentage saving from modular construction.

A manufacturing release freezes the dimensions, ratings, connection locations, control definitions and drawings that fabrication will consume. It does not freeze every future software or operating choice. Both routes need design control before irreversible work, but cutting a module frame or manufacturing a manifold can commit an interface while the site is still being prepared. An unresolved dimension can stop the factory branch long before it would have stopped site assembly. Release separate packages only where their approved boundaries establish that later decisions cannot invalidate them.

Transport is a real predecessor. Before releasing the module envelope, agree the shipping configuration, dimensions, mass and center of gravity, route clearances and permitted loads, lifting points, access and placement sequence. A module that works electrically and thermally can still require redesign or a different shipment plan. Confirm these inputs for the actual route; the stipulated one-week transport duration is not evidence of access. Protection during shipment and receipt checks belong between the factory record and the site connection record.

## A late rack change consumes interface float

Just before fabrication, the owner changes the phase from 200 × 100 kW to 100 × 200 kW racks. Each 2 MW zone now serves ten racks. The 20 MW IT total remains fixed, but the local electrical, hydraulic and physical interfaces may change. Continue the revised design and supplier reviews, and continue site work whose approved boundaries are demonstrably unaffected. Hold the affected fabrication packages, rack connections and dependent structural or placement work. The next lesson identifies the evidence that releases each hold.

Suppose those required interface approvals arrive together at week 3. Assume no affected factory assembly can start earlier, the factory still has a six-week slot available then, transport remains one week, and independent site work still finishes in week 8. Arrival moves from week 7 to week 10; setting and connections finish in week 12 and integrated acceptance finishes in week 14: max(3 + 6 + 1, 8) + 2 + 2 = 14. The three-week approval delay causes a two-week completion delay because the original delivery branch had one week of float before the site join.

Under the same assumptions, the site-built route can retain week 16 because the revised service interfaces are approved before site assembly starts in week 8. That does not make late changes free: altered purchasing, foundations, equipment lead times or site scope would change the result. Releasing a revised drawing also does not reserve factory labor, test equipment, a truck or a crane. The scheduler must obtain the available manufacturing slot and logistics dates, connect them to the signed release milestones and calculate the current finish. Different packages can have different release dates; do not hide their dependencies behind one unchanged MW figure.

## Worked example: Three paths join before acceptance

- Synthetic durations in continuous weeks, with unconstrained resources and no calendar effects.
- Requirements: 2 weeks. Electrical procurement: 18 weeks after requirements; electrical installation: 3 weeks.
- Cooling procurement: 10 weeks after requirements; cooling installation: 4 weeks. Utility path: 16 weeks from start. Final integration: 4 weeks after all paths.

1. Electrical ready — 2 + 18 + 3 = week 23 — Sequential predecessors accumulate.
2. Cooling and utility ready — Cooling: 2 + 10 + 4 = week 16; utility: week 16 — These paths run in parallel with electrical delivery.
3. Accepted phase — max(23, 16, 16) + 4 = week 27 — The final join waits for every required predecessor.

**Result:** The earliest modeled acceptance is week 27; expediting cooling alone does not advance it.

**Model boundary:** This is neither a supplier lead-time forecast nor a construction commitment. Resource, permit, interface and risk constraints are omitted deliberately.

## The tradeoff

Choice: Freeze module interfaces early enough to assemble services in parallel with site enabling.

Benefit: In the stipulated comparison, overlap moves integrated acceptance from week 16 to week 12.

Cost: The design commits before site assembly would begin; later rack changes can invalidate factory work, consume delivery float or lose a manufacturing slot. Transport and site integration remain necessary.

## When the situation changes

Trigger: A project keeps its factory release and completion dates because the revised rack population still totals 20 MW.

Mechanism: The unchanged aggregate duty hides unapproved branch ratings, manifold connections and support geometry; the factory may build the wrong interfaces or wait for replacements.

Response: Place holds on the affected packages, continue evidenced independent work, assign release owners and recalculate from actual approval, manufacturing, transport and site milestones.

## Apply the idea

For the 20 MW comparison, required rack-change approvals now arrive at week 5. Factory assembly still takes 6 weeks, transport 1, site setting/connections 2 and integrated acceptance 2; independent site work still finishes in week 8. What can continue, when does the modular route finish, and can the site-built route still finish at week 16?

<details>
<summary>Reveal the worked answer</summary>

Independent approved site work can continue. The modular route finishes at max(5 + 6 + 1, 8) + 2 + 2 = week 16. The site-built route can also retain week 16 if all revised inputs and resources are ready before its week-8 assembly start.

Hold only the work whose inputs are unresolved, including any affected supports or embedded connections on the site branch. Electrical, hydraulic and spatial sign-offs release their packages; the scheduler then confirms factory, transport, site and test resources. A five-week approval delay consumes one week of original arrival float and delays modular completion by four weeks. If the rack change alters the supposedly independent site work or component availability, neither finish follows from these assumptions.

</details>

**The idea to keep:** A delivery date belongs to a complete dependency path. Shortening an activity without changing that path may create no earlier service.

## Sources and reading boundaries

- [GAO Schedule Assessment Guide](https://www.gao.gov/products/gao-16-89g) — The guide overview supports integrated schedules, explicit dependencies and the connection between schedule slippage and cost. Read 2026-09-06. Overview and guide structure inspected. The network, durations, slack and interventions are original teaching scenarios, not GAO project examples. The site-built/prefabricated comparison and rack-change release dates are also synthetic; no modular supplier performance is attributed to this guide.
- [WBDG: Commissioning Documents](https://legacy.wbdg.org/building-commissioning/commissioning-documents) — The existing OPR, basis-of-design and review discussion supports connecting project requirements to traceable design and acceptance records. Read 2026-09-06. Selected document-role and design-review passages inspected in the existing source review. The EPC allocation, module scope and release workflow are stipulated teaching choices, not a prescribed contract model or a quotation from WBDG.
