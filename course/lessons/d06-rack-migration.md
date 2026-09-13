# A rack upgrade is an interface negotiation

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d06-rack-migration`, then run `uv run gigawatt-expand`.

**8. Rack power and the 800 V DC transition · Authored draft**

Test a higher-density rack against electrical, thermal, mechanical and operational constraints before accepting the upgrade path.

**Driving question:** Why can a retrofit reject the architecture that looks best on an empty site?

## Start with a service brief and two inventories

Write the desired service first: a workload, useful-throughput target, availability expectation and date. Then create two inventories. The first describes the existing site: available feeder capacity under the intended redundancy condition, cooling interfaces, physical access, floor support, management network and permitted maintenance windows. The second describes the proposed rack: input range, continuous and transient power, coolant conditions, residual air heat, weight, cabling, service clearances and restart behavior. The project consists of reconciling those inventories, not merely fitting the new cabinet into an old footprint.

A missing value is a project risk to resolve, not a zero. If rack weight is unknown, do not infer it from a photograph. If a supplier specifies cooling capacity without fluid and temperature conditions, the interface is incomplete. If the operator promises a maintenance window but the customer cannot checkpoint within it, the operational interface is incomplete. Identify the owner of each missing specification and the evidence that will close it. This makes the decision reviewable without pretending that a classroom exercise is an engineering approval.

## Read the rack format before counting equipment

For a conventional EIA 19-inch rack, “19-inch” names the nominal equipment mounting format, not the exterior cabinet width. Vertical space is allocated in rack units: 1U = 1.75 inches = 44.45 mm of mounting pitch. A 2U device occupies two such positions. Its actual enclosure dimensions and mounting kit still come from its specification.

A 42U rack offers 42 units of usable mounting height: 42 × 44.45 = 1,866.9 mm, or 73.5 inches. This is not its outside height; the frame, base and other structure add to the overall dimensions. Check the exterior dimensions separately when planning doorways and placement.

Make a small synthetic rack-space ledger: twelve 2U servers occupy 24U, two 1U switches occupy 2U, a stipulated power shelf occupies 4U, and horizontal cable management occupies 2U. Total allocation is 24 + 2 + 4 + 2 = 32U, leaving 42 − 32 = 10U. Those ten free units are space, not permission to add five more servers. Mounting width, usable depth, equipment weight, electrical power, cooling and service clearances must each fit independently. These quantities are a classroom arrangement, not a product bill of materials.

Do not silently substitute OCP OpenU (OU) for EIA U. The reviewed Open Rack V3 base specification defines 48 mm OpenU spacing and separately describes optional 44.45 mm EIA rack-unit support. A label such as 1OU therefore does not mean 1U. Record the actual rack specification, mechanical option and mounting interfaces; an AI rack need not follow the conventional format used in the 42U example.

## Separate steady power from the time response

A feeder can have sufficient average capacity while a load transient still violates a converter’s permitted voltage range. Conversely, a short burst can be buffered locally even when a longer increase cannot be sustained. Plot power against time and label which device responds over each interval. Energy is the area between demand and supply. A 40 kW deficit lasting 0.2 seconds requires 8 kJ delivered to the relevant bus. That arithmetic does not select a battery or capacitor: voltage droop, accessible energy, conversion power, control delay and repetition frequency remain to be established.

For a capacitor model, usable energy between two allowed voltages is one half of capacitance times the difference of their squares. The usable range matters more than total nameplate energy when the load cannot tolerate deep voltage reduction. For a repeated burst, the source must also replenish the buffer between events. A buffer solves a temporary mismatch only while its power and energy limits permit it. It cannot make a permanently overloaded feeder adequate, and recharge can create a new upstream peak.

## Stored energy must be electrically close enough to serve the event

Separate three physical scales. Package and board capacitors provide local transient current at device rails. Rack-bus capacitors and qualified battery backup units (BBUs) support their DC distribution bus. Facility UPS batteries or a battery energy storage system (BESS) act through a larger conversion and distribution path and may serve a broader set of loads. “Closer to compute” is meaningful because impedance, conversion stages and control response sit between stored energy and the load; merely owning more kWh farther away does not remove a fast voltage disturbance at the chip.

Trace the complete forward-and-return path. A changing current creates an inductive voltage term L × di/dt, while resistance produces I × R. Local decoupling shortens the loop that initially supplies a transient. The next regulated stage and its source then take up more load as their controls and power stages respond. These contributions overlap; capacitors do not wait until a fixed timer expires and then hand all power to a battery. An online UPS avoids an output transfer to an inverter that is already running, but its DC-link, battery interface and downstream regulators still have finite dynamics.

For an explicit bus-level model, let demand rise by 40 kW while the upstream converter’s additional contribution rises linearly from zero to 40 kW over 0.2 s. The local buffer supplies the declining difference. Its delivered energy is the triangle ½ × 40 kW × 0.2 s = 4 kJ; a wholly unsupported 40 kW for that interval would instead require 8 kJ. Doubling the stipulated response interval to 0.4 s doubles required energy to 8 kJ while the initial buffer power remains 40 kW. The model excludes resistance, inductance, voltage droop and losses. It separates the energy deficit from the device’s peak power and timing requirements.

A capacitor’s usable energy is ½C(Vinitial² − Vminimum²). It must satisfy both the energy account and the permitted voltage/time response. A BBU needs an adequate discharger, charged cells, protection, coordination and a qualified bus interface. A BESS at the facility can help a grid-side power schedule or longer interruption but does not substitute for local chip decoupling. A rack-only BBU also does not by itself keep facility pumps, cooling or remote switches alive.

## A BBU is not one universal battery per NVL72 rack

BBU can mean an individual module or a whole shelf in informal discussion; identify which. The reviewed ORv3 example has six BBU modules in a shelf with 5+1 redundancy. The OCP module specification calls for 3 kW per module and at least 240 s of discharge under its declared cell-state, temperature and aging conditions. For a 15 kW protected load, five surviving 3 kW modules pass the power screen after one module fails; four supply only 12 kW after two failures. The example establishes an interface-specific capacity calculation, not a BBU count for a 142 kW rack.

The same specification includes a nonzero activation/ramp interval and commanded peak-shaving capability. Whether a deployment uses those functions depends on its configuration and qualification. NVL72 names a compute/NVLink domain; it does not prescribe one BBU module or shelf. Choose the storage architecture using the protected load, discharge power, required duration, voltage compatibility, failure condition and recharge policy. The reviewed NVIDIA rack documentation does not establish a universal BBU-to-NVL72 ratio.

## Repeated bursts must leave time and capacity to recharge

Take an original DC-bus example with a source capped at 120 kW. The rack normally draws 110 kW, then 160 kW for 0.2 s. A qualified buffer supplies the 40 kW gap, delivering 8 kJ. During the 110 kW interval only 10 kW of source headroom remains, so ideal recharge requires 8/10 = 0.8 s. At 10 s between bursts there is time to refill. At only 0.2 s between bursts, the source can replace just 2 kJ and each cycle loses 6 kJ from the buffer.

The rapid pattern also averages (160 × 0.2 + 110 × 0.2)/0.4 = 135 kW, exceeding the 120 kW source indefinitely. Adding storage delays depletion; it cannot fix that sustained energy shortfall. Reduce or reschedule demand, supply more average power, or accept shorter operating duration. Real losses, discharge limits, battery cycling and a reserved backup state of charge narrow the feasible envelope further. Peak shaving and outage reserve therefore compete for the same usable stored energy unless the design explicitly allocates both.

## Brownfield and greenfield optimize different things

On an empty site, the designer can coordinate power rooms, pipe routes, service access and equipment zones before construction. In an occupied building, the same change may require planned outages, temporary capacity and work beside operating systems. Retained assets have both value and constraints. A hybrid power rack may preserve part of the AC system while consuming scarce floor positions. Facility-level DC might offer a cleaner future layout but require a much larger conversion project. The comparison must value time and disruption alongside equipment losses.

Use a decision table whose columns are throughput available by the required date, enabling works, service access, power headroom, cooling headroom and reversibility. Reject a route when a hard requirement cannot be met; score preferences only after that. Then perform a reversal test: identify the smallest plausible change that would alter the choice. If one extra feeder upgrade makes the delayed route attractive, obtain that cost and schedule before declaring a winner. An architecture decision becomes stronger when the team can say what evidence would change it.

## Worked example: A sidecar does not increase feeder capacity

- An existing row has 240 kW available at its AC allocation boundary under the required operating condition.
- Two new compute racks each need 120 kW DC. A shared sidecar is assumed 96% efficient and has 3 kW of additional upstream-fed auxiliaries.
- No simultaneous-load discount is allowed. An alternative reduced setting is 110 kW DC per rack.

1. Test full rack demand — (2 × 120) / 0.96 + 3 = 253 kW — The requested DC output already consumes all nominal AC headroom before losses.
2. Find the shortfall — 253 − 240 = 13 kW — Moving conversion outside the rack does not remove this upstream requirement.
3. Test the reduced setting — (2 × 110) / 0.96 + 3 = 232.167 kW — The lower load leaves about 7.833 kW of modeled electrical headroom.

**Result:** The full setting fails the supplied electrical constraint. The reduced setting passes this one arithmetic screen but still needs workload and interface acceptance.

**Model boundary:** These are synthetic allocations, not conductor ampacities or permission to operate equipment. No real rack power cap or performance response is implied.

## The tradeoff

Choice: Use a staged retrofit with a lower initial rack power setting.

Benefit: Potentially meet an earlier service date while completing enabling work later.

Cost: Useful throughput may fall or become workload-dependent; two qualification cycles and future interruptions may be required.

## When the situation changes

Trigger: The design passes steady-state checks but startup triggers simultaneous charging and compute demand.

Mechanism: The aggregate transient exceeds the agreed input envelope or causes a voltage excursion even though the eventual steady point fits.

Response: Have the responsible engineering teams validate startup sequencing, buffer recharge and load-step behavior against both supplier and site limits.

## Apply the idea

The project can obtain another 20 kW of allocation, but doing so adds six weeks. Its customer needs service in three weeks and accepts a verified lower-throughput mode temporarily. Which route is defensible?

<details>
<summary>Reveal the worked answer</summary>

A staged reduced-load route can be defensible if it passes all interfaces and the customer’s measured service target; schedule the larger allocation as a separate enabling phase.

The full setting would then fit the expanded 260 kW allocation, with only 7 kW of modeled margin, but it misses the initial date. The customer’s acceptance changes the feasible set. Without measured low-power throughput and a qualified migration procedure, even the staged route remains a proposal.

</details>

**The idea to keep:** An upgrade succeeds only when every required interface can support the agreed operating and failure states.

## Sources and reading boundaries

- [Open Rack/SpecsAndDesigns](https://www.opencompute.org/wiki/Open_Rack/SpecsAndDesigns) — Rack, power, connector, battery and manifold interfaces are documented separately with revisions. Read 2026-09-06. Index reviewed; individual component specifications require independent review and qualification.
- [Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) — A hybrid power-rack category can retain upstream AC distribution. Read 2026-09-06. The vendor compatibility statement does not establish the capacity of a particular existing site.
- [Eaton — Rack Basics: Selection, Installation and Cooling](https://tripplite.eaton.com/support/rack-cabinet-basics-selection-installation-cooling) — EIA 19-inch mounting terminology, 1.75-inch rack units, usable U height versus external cabinet height, and separate depth and load considerations. Read 2026-09-08. Reviewed indexed public text under Rack Standards, Rack Units, Height, Width and Depth; direct page retrieval returned 403. Manufacturer explainer, not a review of the full EIA standard. Product-independent classroom allocation is original; no universal AI-rack compatibility or advertised cooling savings are adopted.
- [Open Compute Project — Open Rack V3 Base Specification, revision 1.0](https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf) — Sections 6, 6.1.2 and 6.1.3 distinguish 48 mm OpenU spacing from optional 44.45 mm EIA rack-unit support and allow exterior frame dimensions to vary. Read 2026-09-08. Reviewed the public PDF mechanical sections on printed pages 7, 9 and 11, plus revision table on page 6. Revision 1.0 is the identified reference, not a claim to the latest revision. Electrical, connector and qualification requirements were not audited; the lesson does not infer interchangeability from height alone.
- [OCP — Open Rack V3 48V BBU Module Specification revision 1.4](https://www.opencompute.org/documents/open-rack-v3-bbu-module-spec-1-4-pdf) — A specific modular BBU: 3 kW discharge, at least 240 s under specified conditions, nonzero activation/ramp interval and optional commanded peak-power shaving. Read 2026-09-12. Sections 4.2, 4.3/Table 2, 4.3.3, and parallel-operation references reviewed. Source conditions include at least 3.9 V/cell at the declared threshold and aging/temperature limits. Not a generic modern rack rating, battery chemistry comparison, or NVL72 configuration. The specification includes timing and state conditions; no instant universal handoff is claimed.
- [Analog Devices — Smart Battery Backup for Uninterrupted Energy, Part 4: BBU Shelf Operation](https://www.analog.com/en/resources/analog-dialogue/articles/smart-battery-backup-for-uninterrupted-energy-part4.html) — ORv3 BBU shelf shared-bus architecture, six modules in 5+1 redundancy, monitoring and controlled discharge. Read 2026-09-12. Introduction, BBU Shelf Overview and Shelf System Control read. The 15 kW surviving-capacity calculation combines the six-module arrangement with the separately reviewed OCP 3 kW module requirement. Not a claim that a 15 kW shelf supports a 142 kW NVL72 rack.
- [Texas Instruments — The decoupling capacitor: is it really necessary?](https://e2e.ti.com/blogs_/archives/b/precisionhub/posts/the-decoupling-capacitor-is-it-really-necessary) — Short local current paths and trace inductance explain why device decoupling is separate from distant stored energy. Read 2026-09-12. Authored article and figure descriptions 1–3 inspected. The example is an amplifier circuit, not a GPU benchmark. No suggested component value or layout instructions are imported; rack-level power transients are original stated models.

## Check your understanding: Did moving the converter save energy?

Pause and make a prediction, then compare your reasoning.

A hypothetical redesign moves a converter from each rack to a nearby cabinet. Useful device output, converter efficiency, cable losses and auxiliary demand all remain unchanged.

**Pause and predict:** Did the redesign reduce facility electricity use? Name something it did change.

<details>
<summary>Compare your reasoning</summary>

No energy saving follows from these assumptions. The converter's location and the rack's physical and electrical interfaces changed.

The same output still requires the same total input across the complete path. Conversion heat now occurs outside the rack, and rack space may be released. Shared failure exposure, protection, service access and expansion arrangements need checking at the new location.

</details>

**The next problem:** Now that power reaches the devices, what determines whether those devices spend their time doing useful work?

Continue in **Compute, memory and the rack**: A rack is a path through several memories.
