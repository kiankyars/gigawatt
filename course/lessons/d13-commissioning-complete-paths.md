# Commission the intersection, not the inventory

**13. EPC**

Distinguish installation and subsystem tests from integrated acceptance, then count overlapping accepted rack paths rather than adding milestone totals.

**Driving question:** When do installed components become a tested service path?

## Every milestone answers a different question

Installed equipment is physically present in its intended arrangement. Energized equipment has an electrical state, but that does not establish its full behavior. A component test checks a specified item under declared conditions. A subsystem functional test examines the function of a connected system. Integrated testing asks whether multiple systems work together across the intended scenarios. Service acceptance adds the project’s end-to-end requirements and the evidence the owner requires before using the phase.

Industry practice numbers the testing stages as commissioning levels L1 to L5. L1, the factory witness test, proves each skid or module as a standalone unit at the manufacturer; this is the factory acceptance test (FAT), which checks internal wiring, piping and controls before shipment. L2 verifies delivery and installation on site: the unit is received, set, anchored and inspected. L3 energizes and starts each system on its own, and L4 runs functional performance tests on each system.

L5, integrated systems testing (IST), runs every system together on site under simulated failures, such as losing the A-side supply, an uninterruptible power supply (UPS) transfer, a pump failover and a black-building start. Some frameworks add a Level 0 design review in front. Everything from L2 onward happens on site, because the utility feed, generators and batteries that the tests exercise meet only there.

The AI data-center commissioning framework from ASHRAE, the American Society of Heating, Refrigerating and Air-Conditioning Engineers, describes staged validation from factory and installation checks through functional and integrated performance. Those labels are useful orientation, but a stage or level name is not the test record. A project can use different organization while still needing explicit criteria, observed results and resolution of issues. Ask what was actually exercised, at what load, with which instrumentation, and what remained outside the test scope.

A synthetic test load can establish important facilities behavior without reproducing a full application. An application test can demonstrate job progress without exercising every facility failure case. Both may be necessary. The important distinction is between what a test stresses and what someone later claims it proves. Do not let a successful demonstration at one boundary become evidence for untested behavior at another.

## The same racks must have complete paths

Continue the 20 MW phase after its rack change: one hundred positions, A01 through A100, each for a 200 kW rack. Electrical acceptance covers A01–A80. Cooling acceptance covers A21–A100. Network acceptance covers A01–A60. Taking the minimum of the three counts gives sixty, but that result is wrong: only A21–A60 are present in all three sets. Their intersection contains forty positions. The counts alone concealed that different parts of the hall had been tested.

This distinction is especially important in phased construction. A completed cooling loop can serve a different block from an energized electrical section. The topology and identity of the accepted paths determine what can be combined. A generic capacity minimum is valid only when its constraints have been reconciled to the same population and boundaries. Otherwise, even correct arithmetic produces an unsupported available-capacity claim.

At 200 kW per position, the forty complete positions give an accepted envelope of 40 × 200 kW = 8 MW of the phase’s 20 MW. Extending cooling acceptance to A01–A100 closes the gap at A01–A20: sixty positions, A01–A60, then have all three acceptances, and the envelope grows to 12 MW. An accepted envelope states the conditions under which service was demonstrated and is permitted. The load the racks actually draw and the training throughput they deliver need their own measurements.

## Acceptance includes the ability to operate afterward

A proposed integrated test matrix should cover the required normal behavior, specified failures, maintenance configurations and restoration. For each conceptual scenario, state the starting configuration, observable requirement, measurement points and criteria for stopping or accepting the exercise. Qualified engineers write and run the project’s actual tests; reviewing the matrix finds the evidence that is still missing.

Handover should preserve the configuration that was tested. Updated topology, equipment identifiers, control versions, unresolved issues, operating documentation and training connect the observed result to future operation. If a critical setting changes afterward, the old result may no longer support the same claim. WBDG treats commissioning records as information for ongoing operations, which ties each piece of evidence to a phase and a configuration.

An unresolved issue needs an explicit disposition. Some issues prevent the stated service condition; others may be accepted with a defined limitation and owner decision. A list of open items is more informative than a single percentage complete when it identifies which paths and claims are affected. Before expanding a phase, recalculate the overlap and inspect shared systems whose configuration changes. The next building can affect the first even when their milestone trackers are separate.

Applied Digital’s Polaris Forge 1 in Ellendale, North Dakota, leased to CoreWeave, delivered its first building in two steps: the first 50 MW reached ready-for-service on October 27, 2025, and the second 50 MW on November 24, 2025. Connecting the second phase had to preserve the infrastructure already serving the first. The two releases record the milestones, so a reviewer of such an expansion asks which switchgear, cooling headers and controls the phases share, and how each connection was tested with the first phase live.

## Worked example: Why min(80, 80, 60) is not enough

- The revised 20 MW phase: rack positions A01–A100 at 200 kW each.
- Electrical acceptance: A01–A80; cooling acceptance: A21–A100; network acceptance: A01–A60.
- All other acceptance criteria are met for the intersecting positions.

1. Electrical ∩ cooling — A21–A80 = 60 positions — Both physical requirements apply to these same positions.
2. Add network acceptance — A21–A80 ∩ A01–A60 = A21–A60 = 40 positions — Only the overlap carries the complete evidence set.
3. Accepted envelope — 40 × 200 kW = 8,000 kW = 8 MW — This is accepted capacity, not operating demand.
4. Extend cooling to A01–A100 — A01–A80 ∩ A01–A60 = A01–A60 = 60 positions; 60 × 200 kW = 12 MW — Network acceptance now lies inside both other sets, so here the intersection equals the smallest count.

**Result:** Forty complete rack paths give 8 MW, where the minimum of the counts would have claimed sixty and 12 MW. Extending cooling acceptance to A01 raises the complete paths to sixty and the envelope to 12 MW.

**Model boundary:** The acceptance ranges and rack power are exercise inputs, not a real project’s commissioning status, permitted load or application throughput.

## When the situation changes

Trigger: Individually successful cooling and electrical tests apply to different blocks of the hall.

Mechanism: The project combines their totals without confirming that the same rack paths satisfy both.

Response: Reconcile asset identities, topology and test scope, then state the accepted intersection and remaining gaps.

## Apply the idea

Start again from electrical A01–A80, cooling A21–A100 and network A01–A60. This time the network team extends its acceptance to A01–A100 instead. How many paths are now complete, and what envelope do they give at 200 kW per position?

<details>
<summary>Reveal the worked answer</summary>

Sixty paths, A21–A80, for 12 MW. The minimum of the counts, min(80, 80, 100) = 80, would claim 16 MW.

A01–A20 still lack cooling acceptance and A81–A100 still lack electrical acceptance, so the new network work completes only A61–A80. The count matches the cooling extension’s sixty, but the racks differ: A21–A80 here against A01–A60 there. A handover has to name the positions, not only their number.

</details>

**The idea to keep:** Usable service requires the same path to satisfy every necessary condition. Separate subsystem counts do not establish that intersection.

## Sources

- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — ASHRAE · Reviewed 2026-09-06. The staged commissioning and integrated-systems discussion distinguishes component checks from coupled validation.
- [WBDG: Commissioning Documents](https://legacy.wbdg.org/building-commissioning/commissioning-documents) — legacy.wbdg.org · Reviewed 2026-09-06. Commissioning records and systems documentation support continued operation and maintenance.
- [The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) — SemiAnalysis · Published 2026-07-29 · Reviewed 2026-09-26. Lists commissioning levels L1 (factory witness test) through L5 (integrated systems testing), with work from L2 onward on site.
- [Applied Digital Achieves Ready for Service for Phase 1 at Polaris Forge 1](https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at) — Applied Digital · Published 2025-10-27 · Reviewed 2026-09-16. The first 50 MW of Polaris Forge 1’s first building reached ready-for-service on October 27, 2025.
- [Applied Digital Completes Phase II Ready for Service at Polaris Forge 1](https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at) — Applied Digital · Published 2025-11-24 · Reviewed 2026-09-16. The second 50 MW of the first building reached ready-for-service on November 24, 2025, bringing it to 100 MW.

## Check your understanding: 20 MW stays; what can the factory release?

Pause and make a prediction, then compare your reasoning.

Just before fabrication, the illustrative phase changes from 200 × 100 kW to 100 × 200 kW racks. Each old rack branch permits 160 A and 3.0 kg/s. Use balanced 480 V AC at PF 1; assign all IT heat to water with cp = 4.18 kJ/(kg·K) and a maximum 10 K rise. The new vendor drawing also doubles rack mass on the same four feet. Independent site work remains approved.

**Pause and predict:** What can proceed, what must be held, and what evidence releases each hold? Address electrical, hydraulic, spatial and scheduling constraints. Does a successful factory test establish site service acceptance?

<details>
<summary>Compare your reasoning</summary>

Continue the approved independent site work and redesign. Hold the affected branches, manifold and supports, shipment/placement and any unsupported completion-date promise. The revised rack needs about 240.6 A and 4.78 kg/s, beyond the old limits; the stipulated load per foot doubles. Factory approval alone cannot establish service acceptance.

Electrical: the design lead must approve the revised rack inputs, branch/connector ratings, one-line and protection/failure review. Halving the number of branches does not double each remaining branch’s allowable current.

Hydraulic: the mechanical lead must demonstrate the revised flow at allowed temperatures and pressures with actual pump/component curves, piping and balancing provisions. The phase still needs about 478.5 kg/s in this model, but each rack needs twice its former flow. Constant total flow does not establish adequate branch pressure.

Spatial: the structural/layout leads need coordinated dimensions, local support loads, access and connection locations. Fewer racks with twice the stipulated mass leave total zone mass unchanged while doubling each occupied position’s load. Logistics separately needs the actual shipping envelope, mass, lifting and route/placement plan.

Scheduling: the EPC interface manager records each approved boundary and the scheduler confirms components, factory slot, transport, site and test resources. With all required approvals at week 3, factory work 6 weeks, transport 1, site ready in week 8, connections 2 and acceptance 2, the finish is max(3 + 6 + 1, 8) + 2 + 2 = week 14. Approval dates alone do not reserve those resources.

Acceptance: controls owners must remap alarms and actions to the new racks, and the commissioning lead must revise the tests. Factory evidence covers its tested scope; completed site connections and integrated workload/failure/recovery evidence are still required. No service path has been demonstrated merely because a module can ship.

</details>

**The next problem:** After those revised paths pass acceptance, which measurements, configuration records and maintenance responsibilities will keep their operating limits visible?

Continue in **14. Controls, operations and reliability**: A believable number can describe the wrong thing.
