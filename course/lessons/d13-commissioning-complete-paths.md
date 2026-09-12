# Commission the intersection, not the inventory

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d13-commissioning-complete-paths`, then run `uv run gigawatt-expand`.

**D13 · Authored draft · Objectives:** D13.3, D13.4

Distinguish installation and subsystem tests from integrated acceptance, then count overlapping accepted rack paths rather than adding milestone totals.

**Driving question:** When do installed components become a tested service path?

## Every milestone answers a different question

Installed equipment is physically present in its intended arrangement. Energized equipment has an electrical state, but that does not establish its full behavior. A component test checks a specified item under declared conditions. A subsystem functional test examines the function of a connected system. Integrated testing asks whether multiple systems work together across the intended scenarios. Service acceptance adds the project’s end-to-end requirements and the evidence the owner requires before using the phase.

ASHRAE’s AI commissioning framework describes staged validation from factory and installation checks through functional and integrated performance. Those labels are useful orientation, but a stage name is not the test record. A project can use different organization while still needing explicit criteria, observed results and resolution of issues. Ask what was actually exercised, at what load, with which instrumentation, and what remained outside the test scope.

A synthetic test load can establish important facilities behavior without reproducing a full application. An application test can demonstrate job progress without exercising every facility failure case. Both may be necessary. The important distinction is between what a test stresses and what someone later claims it proves. Do not let a successful demonstration at one boundary become evidence for untested behavior at another.

## The same racks must have complete paths

Imagine one hundred named rack positions, A01 through A100. The recorded electrical acceptance covers A01–A80. Cooling acceptance covers A21–A100. Network acceptance covers A01–A60. Taking the minimum of the three counts gives sixty, but that result is wrong: only A21–A60 are present in all three sets. Their intersection contains forty positions. The counts alone concealed that different parts of the hall had been tested.

This distinction is especially important in phased construction. A completed cooling loop can serve a different block from an energized electrical section. The topology and identity of the accepted paths determine what can be combined. A generic capacity minimum is valid only when its constraints have been reconciled to the same population and boundaries. Otherwise, even correct arithmetic produces an unsupported available-capacity claim.

If the synthetic brief assigns 100 kW per accepted rack position, forty complete positions correspond to a 4 MW envelope for that stated population. They do not prove a 4 MW measured load or a particular training throughput. Evidence of acceptance establishes the permitted and demonstrated conditions of service; observation of present demand and useful output requires additional measurements.

## Acceptance includes the ability to operate afterward

A proposed integrated test matrix should cover the required normal behavior, specified failures, maintenance configurations and restoration. For each conceptual scenario, state the starting configuration, observable requirement, measurement points and criteria for stopping or accepting the exercise. Real tests need project-specific engineering and qualified execution. The learner’s task is to identify what evidence is missing, not to improvise an outage procedure on operating equipment.

Handover should preserve the configuration that was tested. Updated topology, equipment identifiers, control versions, unresolved issues, operating documentation and training connect the observed result to future operation. If a critical setting changes afterward, the old result may no longer support the same claim. WBDG treats commissioning records as information used in ongoing operations; the course uses that principle to make evidence traceable to a phase and configuration.

An unresolved issue needs an explicit disposition. Some issues prevent the stated service condition; others may be accepted with a defined limitation and owner decision. A list of open items is more informative than a single percentage complete when it identifies which paths and claims are affected. Before expanding a phase, recalculate the overlap and inspect shared systems whose configuration changes. The next building can affect the first even when their milestone trackers are separate.

## Worked example: Why min(80, 80, 60) is not enough

- Synthetic named rack population A01–A100.
- Electrical acceptance: A01–A80; cooling acceptance: A21–A100; network acceptance: A01–A60.
- All other criteria are assumed met for the intersecting positions, and the exercise assigns 100 kW per position.

1. Electrical ∩ cooling — A21–A80 = 60 positions — Both physical requirements apply to these same positions.
2. Add network acceptance — A21–A80 ∩ A01–A60 = A21–A60 = 40 positions — Only the overlap carries the complete evidence set.
3. Declared envelope — 40 × 100 kW = 4,000 kW = 4 MW — This expresses the exercise’s accepted capacity envelope, not its operating demand.

**Result:** Forty complete rack paths are evidenced under the stated assumptions; a minimum of aggregate counts would overstate them.

**Model boundary:** No real project commissioning status, permitted load or application throughput is established.

## The tradeoff

Choice: Hand over smaller accepted phases.

Benefit: It can expose interface problems earlier and permit useful service before all future equipment is finished.

Cost: Shared systems, boundaries, configuration control and the separation of construction from live operation become more demanding.

## When the situation changes

Trigger: Individually successful cooling and electrical tests apply to different blocks of the hall.

Mechanism: The project combines their totals without confirming that the same rack paths satisfy both.

Response: Reconcile asset identities, topology and test scope, then state the accepted intersection and remaining gaps.

## Apply the idea

Cooling evidence is extended to A01–A100, while electrical and network scopes remain unchanged. How many paths are now complete?

<details>
<summary>Reveal the worked answer</summary>

A01–A60 now satisfy all three sets: 60 positions, corresponding to 6 MW only under the same 100 kW-per-position assumption.

The added cooling evidence closes the missing condition for A01–A20. Positions A61–A80 still lack network acceptance, and A81–A100 also lack electrical acceptance. Extending one subsystem’s scope does not advance every part of the phase equally.

</details>

**The idea to keep:** Usable service requires the same path to satisfy every necessary condition. Separate subsystem counts do not establish that intersection.

## Sources and reading boundaries

- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — The staged commissioning and integrated-systems discussion distinguishes component checks from coupled validation. Read 2026-09-06. Selected commissioning-stage and handover discussion inspected; project procedures, pass criteria and synthetic rack sets are original.
- [WBDG: Commissioning Documents](https://legacy.wbdg.org/building-commissioning/commissioning-documents) — Commissioning records and systems documentation support continued operation and maintenance. Read 2026-09-06. Selected documentation purpose reviewed; this is not a claim to have applied a complete ASHRAE standard or GSA acceptance process.

## D13 domain check-in: Count the same accepted paths

Optional: pause and make a prediction, then compare your reasoning. You can continue whenever you are ready.

A hypothetical phase contains rack positions A, B, C and D. Power acceptance covers A, B and C; cooling acceptance covers B, C and D; network acceptance covers A, B, C and D. No end-to-end workload or recovery test has run.

**Pause and predict:** How many positions share the three accepted subsystem paths? How many have demonstrated service acceptance?

<details>
<summary>Compare your reasoning</summary>

Two positions, B and C, share all three subsystem acceptances. None has yet demonstrated end-to-end service acceptance.

Separate totals of three, three and four do not identify a common set of three. Take the intersection first, then test the agreed workload, failure behavior and recovery on complete paths. A subsystem pass is evidence for its own scope.

</details>

**The next problem:** After acceptance, how will operators notice when those same paths change, degrade or become unavailable for maintenance?

Continue in **D14**: A believable number can describe the wrong thing.
