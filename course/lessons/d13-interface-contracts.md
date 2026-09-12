# Two adequate products can form an inadequate system

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d13-interface-contracts`, then run `uv run gigawatt-expand`.

**D13 · Authored draft · Objectives:** D13.2

Keep a 20 MW IT duty fixed, test the changed electrical, hydraulic and spatial interfaces, and assign the evidence needed to release fabrication and schedule holds.

**Driving question:** What can proceed when 200 × 100 kW racks become 100 × 200 kW just before fabrication?

## Start with the required behavior, not the catalog number

An owner requirement describes what the intended service must do. A design basis explains how the proposed arrangement will accomplish it. The WBDG commissioning-document guidance distinguishes these roles and connects them to reviewed records. In a data-center project, that distinction prevents a vendor selection from quietly redefining the service: an available component is not automatically an adequate response to the original workload, availability or operating envelope.

An interface contract should specify what crosses a boundary and under which conditions. For cooling, this includes temperatures, flow, pressure behavior, fluid compatibility and the division of control responsibility. For power, it includes the relevant electrical characteristics and protection assumptions. For information, it includes the meaning, units, timing and authority of exchanged signals. Physical connectors are only one part of compatibility; a connection can mate while the expected behavior remains impossible.

The contract also needs ownership. Who provides the requirement, who demonstrates it, who reviews the demonstration, and what happens when one side changes? A vague shared responsibility can leave both suppliers assuming the other side provides a necessary sensor or control function. Turning the interface into an explicit record exposes these gaps while the project can still change drawings or procurement terms.

## The same 20 MW puts twice the demand through each rack connection

Continue the delivery comparison: ten service zones each carry 2 MW, changing from twenty 100 kW racks to ten 200 kW racks per zone just before fabrication. Hold the IT load, voltage, power factor and cooling temperatures fixed. These are synthetic equipment and operating assumptions, not product ratings or an Abilene design. The 20 MW is IT power, so it does not establish unchanged total facility demand if cooling pumps, conversion losses or other support loads change.

For the electrical check, use balanced 480 V three-phase AC and power factor 1 at the rack input. Model one supply path carrying the entire rack load: I = P/(√3 × V × PF). A 100 kW rack draws about 120.3 A; a 200 kW rack draws about 240.6 A. The existing complete branch has a stipulated allowable continuous operating current of 160 A under these conditions. It passes the original calculation and fails the revised one. Halving the branch count does not give each remaining conductor, tap, connector or protective device twice its rating. With redundant feeds, the revised design must also establish the current and protection of each surviving path after a specified failure; normal sharing cannot be presumed to solve it.

For the thermal check, assign all IT heat to a single-phase water circuit and ignore auxiliary heat in this illustrative balance. At a maximum 10 K rise and cp = 4.18 kJ/(kg·K), each rack needs 100/(4.18 × 10) = 2.39 kg/s before the change and 200/(4.18 × 10) = 4.78 kg/s after it. The phase total stays about 478.5 kg/s and each 2 MW zone stays about 47.8 kg/s. Yet the old rack branch has a stipulated 3.0 kg/s flow limit, so it fails the new requirement. At 10 K it can carry only 125.4 kW. A CDU or header’s aggregate thermal rating cannot release this branch.

Flow also needs pressure. For a separate check of the reused branch hardware, stipulate a 20 kPa drop at the original flow, an approximately quadratic pressure-flow relationship over this range, and only 60 kPa available across that same hardware. Doubling flow would require about 4 × 20 = 80 kPa, beyond the available pressure. This approximation tests the old hardware; it is not a prediction for a redesigned rack or all parts of the loop. The hydraulic review needs the actual pump and system curves, remaining rack/exchanger losses, balancing behavior and pressure limits. Do not turn a constant total flow into an assumption of constant required pump head.

## Fewer racks do not establish smaller or lighter infrastructure

A rack count is not a floor plan. Obtain the revised cabinet dimensions, service and removal clearances, connector locations, hose routes, cable bends, access to isolation devices and network connection schedule. Ten new racks may require a different arrangement within a zone; the former twenty takeoffs do not automatically line up with ten higher-duty connections. Deleting half the floor area or cutting off alternate manifold branches before this review would commit unverified geometry.

To make the structural consequence concrete, stipulate that the revised vendor drawing specifies twice the installed mass on the same four support feet, with equal static sharing for this comparison. That mass change is an exercise input, not something inferred from doubling kW. Total rack mass per 2 MW zone remains constant because there are half as many racks, but each occupied rack position and each foot carries twice the original load. The structural designer must check the local floor or module frame, anchorage, installation and replacement route; a whole-zone weight total cannot establish those conditions.

The logistics lead and module supplier also need the actual shipping configuration. Our service modules receive IT racks on-site, so the doubled installed rack mass is not automatically a doubled shipping payload. Changed buswork, manifolds or frame design can still alter module mass, lifting loads, center of gravity or dimensions. Release the revised module envelope only when the agreed transport route, clearances, load limits, handling and placement sequence fit that configuration. Module joints need tolerances and accessible connections as well as nominal dimensions.

## Give every module boundary one accountable integration owner

For this exercise, the EPC interface manager owns closure of every connection between the module and the facility. The owner’s requirements representative approves changes to required service; the electrical, mechanical and structural design leads approve their technical interfaces. The module supplier owns its internal assemblies and terminal/flange drawings, and the site contractor owns the external connections and installation records. The commissioning lead defines and witnesses the agreed evidence across the joined systems. Write these duties into the interface register, with one accountable integration owner, drawing revisions and release status for each boundary. Supplier approval of its own end is not closure of the joint.

At the module’s incoming electrical terminals, name the upstream and internal design owners, voltage, load and failure envelope, current and fault-duty limits, protection assumptions and termination geometry. At the coolant flanges, name the facility-loop and module-loop owners, temperatures, flow and pressure envelope, fluid specification, connection locations and isolation duties. At the base and module joints, name the structure and installation owners, datum coordinates, tolerances, support reactions and access. At the controls gateway, name the alarm and command owners, units, timestamps, rack/branch addresses, loss-of-communication behavior and authority to request or enforce load reduction.

The rack change requires new identifiers as well as new hardware: old cooling alarms, power circuits and shutdown groups must map to the intended new racks. The EPC interface manager resolves a cross-boundary conflict and records acceptance by both technical sides; the commissioning lead later verifies that the physical installation and configured behavior match that record. A vendor factory test can release shipment for its specified scope. It cannot release integrated service acceptance for the completed site.

## Acceptance criteria make a requirement observable

A requirement such as sufficient cooling is too vague to test. A stronger record identifies a declared heat load, inlet conditions, measurement locations, allowable behavior, duration and response to specified changes. Each acceptance condition should connect to recorded evidence. If temperature sensors are placed on different sides of a heat exchanger, their difference may not mean the quantity assumed in the flow calculation. The metering plan is therefore part of the interface agreement.

Control semantics deserve the same precision. State whether a reported flow is commanded, measured or inferred; whether an alarm denotes a warning or a protective action; and whether a value is instantaneous or averaged. Specify how stale or unavailable data is represented. A display that silently reuses its last good value can make a stopped communication path look like an unusually stable process. That is an interface failure even though the physical equipment has not changed.

A cooling-fault response is also an interface to demonstrate: identify the sensor, affected rack or branch, action authority, power-cap scope, and confirmation that the action occurred. Distinguish a warning, requested reduction, enforced reduction and shutdown. Dell documents failed Emergency Power Reduction actions when a target is unreachable or rejects shutdown. NVIDIA's rack leak integration requires explicit BMS connectivity and configuration. A cooling alarm on a dashboard alone therefore does not establish an operating protection path.

When a revision arrives, compare it with the recorded interface before accepting the substitution. A lighter rack may alter center of gravity; a new CDU may change connection pressure; a software release may rename a signal or change its range. Record the affected requirements, retests and downstream documents. A disciplined change record saves time because it tells the project exactly what to re-examine instead of reopening every design question or assuming nothing consequential changed.

## Release work with evidence, package by package

Proceed with impact analysis, revised drawings, supplier data requests and schedule updates. Site access, earthworks or upstream orders can continue only for packages whose responsible designer has recorded that the changed racks do not alter their approved inputs. For an upstream electrical or cooling package, that record must check operating and failure loads, auxiliary demand, temperatures and interfaces; “still 20 MW” is insufficient. Hold affected embedded services, foundations or common supports too if their geometry or loads remain unresolved.

Electrical hold — Stop fabrication or installation of the affected rack distribution, taps, cables and terminations. The electrical design lead releases it with the revised rack input specification, one-line and branch schedule; verified allowable operating current, equipment/connector ratings and derating; fault-duty and protection review, including required failure states; and coordinated terminal drawings accepted by the module supplier and site electrical contractor. The old 160 A branch cannot receive a 240.6 A duty through a paperwork-only release.

Hydraulic hold — Stop affected manifold takeoffs, rack hoses, connections and any changed CDU/pump selection. The mechanical design lead releases it with the approved rack thermal and coolant envelope, selected components that support 4.78 kg/s at the allowed temperatures, a pressure/flow calculation using actual component and pump curves, balancing and control provisions, and a coordinated piping diagram. A claimed 20 MW plant rating does not discharge the 3.0 kg/s branch limit or the 80 kPa versus 60 kPa pressure mismatch.

Spatial and logistics hold — Stop cutting affected frames and penetrations, fixing supports or foundations, and releasing the revised module for shipment or placement. The structural and layout leads release fabrication using vendor dimensional and mass drawings, coordinated clearances and routes, checked local support loads, anchorage and connection tolerances. The logistics lead separately releases movement against the confirmed as-shipped dimensions, mass, center of gravity, lifting and route/placement plan. A layout approval is not evidence that a truck or crane can deliver that configuration.

Controls and acceptance hold — Hold the changed alarm, circuit and rack-address mappings and any claim that the original test evidence covers the revision. Controls owners provide an approved signal and cause/action matrix for the new rack groups; the commissioning lead updates factory and site test scopes, instrumentation and criteria. Release fabrication or configuration on those approved inputs, release shipment on the specified factory records, and release service only after the required site and integrated tests close the affected issues. Tests at the former rack duty do not demonstrate the new duty.

Schedule hold — Hold an unconditional factory-start or service-date commitment until the EPC scheduler has the signed package releases, revised component availability, a confirmed factory slot, transport and placement resources, site readiness and test resources in one dependency network. For the prior example with all required approvals at week 3, those confirmations support week 14. If the frame can safely begin earlier under its own approved interfaces, model that split explicitly; if a manufacturing slot is lost, use the replacement slot rather than pretending the six-week clock started at drawing approval.

## Worked example: Release a revised 20 MW phase, one interface at a time

- Ten 2 MW zones: 200 × 100 kW racks become 100 × 200 kW. IT duty stays 20 MW; facility auxiliary loads require separate review.
- Balanced 480 V three-phase rack input, PF = 1, one supply path carrying the full rack duty. Old branch allowable continuous current: 160 A.
- All IT heat enters water; cp = 4.18 kJ/(kg·K), maximum rise 10 K, old branch flow limit 3.0 kg/s. For the reused branch hardware alone, Δp ∝ flow², with 20 kPa at old flow and 60 kPa available.
- The new rack has twice the stipulated installed mass on the same four support feet; equal static sharing is assumed. IT racks are installed after module shipment.
- Required approvals arrive at week 3. Confirmed factory work takes 6 weeks, transport 1, independent site work finishes at week 8, site connections take 2 and integrated acceptance takes 2.

1. Electrical branch — 100,000/(√3 × 480) = 120.3 A; 200,000/(√3 × 480) = 240.6 A > 160 A — Hold the affected distribution until a revised rated and protected path is approved.
2. Hydraulic branch — 100/(4.18 × 10) = 2.39 kg/s; 200/(4.18 × 10) = 4.78 kg/s > 3.0 kg/s; 20 × 2² = 80 kPa > 60 kPa — Hold the branch/manifold design; unchanged total heat and flow do not establish local transport capacity or sufficient pressure.
3. Local support — Half as many racks × twice the mass = same zone mass; mass per occupied rack and load per foot both double — Hold affected supports until the local structural and layout review passes. Check the shipping configuration separately.
4. Dependency join — max(3 + 6 + 1, 8) + 2 + 2 = week 14 — Independent site work continues; the factory waits for the required releases. Confirmed resources make the assumed durations usable.

**Result:** Neither unchanged MW nor unchanged total coolant flow releases the affected interfaces. Continue demonstrably independent work; release changed packages only on their named evidence. The modeled acceptance moves from week 12 to week 14.

**Model boundary:** This is an original design-review exercise, not an equipment selection, structural calculation or construction commitment. Real product curves, support details, failure states, factory slots and integrated test records must replace the assumptions.

## The tradeoff

Choice: Release independent module packages while the revised rack interfaces are being resolved.

Benefit: Unaffected site and factory work can preserve useful overlap.

Cost: A supposedly independent frame, penetration or manifold can embed an unresolved interface. The design owner must establish that independence before fabrication, and the schedule must retain the remaining joins.

## When the situation changes

Trigger: The factory deletes alternate 100 kW rack connections and labels the remaining ten positions in each zone 200 kW.

Mechanism: The surviving 160 A and 3.0 kg/s branches cannot support the new duty; local support loads, connector positions and control mappings are also unverified.

Response: Hold the affected fabrication, record the interface owners and obtain revised electrical, hydraulic, spatial and control evidence before release. Recompute manufacturing, transport and integrated acceptance dates.

## Apply the idea

The rack change remains 200 × 100 kW → 100 × 200 kW. The electrical lead has approved replacement branches for the revised normal and failure duties; the mechanical lead has approved the new hydraulic operating points. The revised mass/layout drawing and transport plan are still missing, and no replacement factory slot is confirmed. Which work can proceed, what stays held, and what evidence is still needed?

<details>
<summary>Reveal the worked answer</summary>

Release the approved electrical and hydraulic packages only to the extent that their fabrication does not consume unresolved geometry or common supports. Continue independently released site work and design coordination. Hold affected frames, support locations, penetrations, shipment/placement and an unconditional completion-date commitment.

Electrical and hydraulic adequacy cannot locate connectors or establish floor reactions, access or transport fit. The structural/layout leads must approve the vendor dimensions, twice-per-position loads, routes, tolerances and connection locations; logistics must approve the actual shipping and placement configuration. The EPC interface manager closes the joints with both suppliers, controls owners remap the new rack groups, and the commissioning lead defines revised tests. The scheduler then needs a confirmed factory slot, component readiness, transport/site resources and the resulting dependency dates. Factory records release only their specified scope; site and integrated evidence remain necessary for service acceptance.

</details>

**The idea to keep:** The same MW total can require different branches, manifolds and supports. Release each affected package against a checked interface and an accountable owner.

## Sources and reading boundaries

- [WBDG: Commissioning Documents](https://legacy.wbdg.org/building-commissioning/commissioning-documents) — The OPR, basis-of-design and review discussion supports requirements ownership and traceable acceptance documentation. Read 2026-09-06. Selected document-role and design-review passages inspected; no standard text or complete acceptance procedure is reproduced. The module responsibility register and hold/release decisions are original teaching allocations.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Design-phase feedback and early monitoring/control coordination are relevant to interface validation. Read 2026-09-06. Selected highlights reviewed. All rack, module, current, flow, pressure, mass and schedule values here are synthetic, not ASHRAE ratings. Existing source review is reused; no new external review is implied.
- [Dell PowerEdge event guide — liquid-cooling and temperature-triggered Emergency Power Reduction](https://www.dell.com/support/manuals/en-us/poweredge-xe9780/error_event_message_guide_c/cpwrpower-configuration-event-messages?guid=guid-3683ef35-10cc-4072-b1bb-e0f44ffcc67f&lang=en-us) — CPWR0139 identifies liquid-cooling-alert-triggered power throttling or shutdown; CPWR0050 and CPWR0131 describe temperature-triggered group EPR. CPWR0026 and CPWR0177 document failed action paths. Read 2026-09-11. Selected event definitions reviewed, not a tested installation or universal implementation. Feature support, licensing, communications and target response matter; no reaction time or achieved cooling protection is inferred.
- [NVIDIA Infra Controller — Leak Detection and Handling](https://docs.nvidia.com/infra-controller/documentation/operations-day-2/leak-detection-handling) — The current capability and critical/severe/general leak sections distinguish BMS electrical/liquid isolation from infrastructure-management handling and identify integration prerequisites. Read 2026-09-11. Current capability sections reviewed. Future API-customizable policies and broader lifecycle coverage are not treated as delivered features. This is a specific rack-management implementation, not a universal leak procedure.
