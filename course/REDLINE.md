# Course production redline — disposition

Review date: 2026-08-27
Artifacts: `course/segments.yaml`, `course/pilots/s10_two_rack_heat_paths.yaml`,
`diagram/planned_shots.json`, `diagram/planned_shots.html`,
`diagram/course_runtime.json`, `diagram/course.html`, and
`course/INSTRUCTOR_PACKET.md`
Posture: complete evidence-bounded course runtime and instructor package; not a
spoken script, timed edit, as-built drawing, or site-performance estimate.

## Release verdict

The seven-act, 26-segment course is approved as record-ready within its explicit
evidence boundaries. All 26 segments are evidence-ready. Private as-built,
commercial, operating-load, utilization, and throughput fields remain null or
`no evidence-backed estimate`; readiness does not promote those facts.

## Blocking redlines

1. **Unknown voltage used as unknown topology — resolved.** Separate null facts
   now record the unverified campus source merge and BESS and diesel connection
   topologies. The 345 kV station secondary-voltage null is used only for
   voltage or ratio claims.
2. **Single-ledger course schema — resolved.** Schema v2 registers evidence
   ledgers and uses qualified fact references. The Abilene ledger remains the
   master-diagram ledger; execution, commercial, delivery/resilience, compute,
   and generic engineering ledgers remain separately scoped without polluting
   the campus evidence boundary.
3. **Fail-open claim placement — resolved.** Every claim declares `topology` or
   `overlay` binding. Topology facts must belong to selected nodes or edges;
   overlays cannot bypass a fact already bound elsewhere in the master.
4. **Lifecycle and promotion ambiguity — resolved.** Assertions validate both
   lifecycle and posture. Mandatory promotion guards are derived from each
   assertion, and the installed-GPU null retains the literal
   `no evidence-backed estimate` boundary.
5. **Thermal readiness overstatement — resolved.** Generic engineering sources
   support the die energy balance and technology-loop direction. Site-specific
   design evidence supports the closed facility loop and air-cooled terminal,
   while CDU, CRAH, and internal interface configurations remain explicit nulls.
   The full replay is ready because it teaches that boundary; it does not claim
   a public as-built internal topology.
6. **Hidden contractual overlay without reveal semantics — resolved.** Planned
   PPA and ownership/model shots explicitly enumerate the hidden nodes, edges,
   and master-owned copy they must reveal as one bundle. Existing shots may not
   reveal hidden topology or labels.
7. **Two sequence owners — resolved by scope.** `course/segments.yaml` owns the
   canonical 26-segment order. `diagram/cameras.yaml` owns reusable camera states
   and the current six-state demonstration order only. The planned-shot compiler
   derives its 21-review-frame order from the course and does not create a second
   sequence owner.
8. **Semantic objective review — manual gate retained.** A validator cannot
   prove the truth of free-form pedagogical prose. This redline reviewed each
   objective against its claim bundle, selected topology, and boundaries; factual
   narration and on-screen copy must still be generated from validated claims,
   not improvised from the objective text.
9. **s10 pacing, scope, and renderer choice — resolved.** The native pilot
   consumes one four-transformation manifest. Transformations advance only on
   instructor action and carry no editorial timing or spoken-script fields. The
   view stops at the four-node, three-edge rack-package boundary, preserves
   distinct liquid supply and return, and gives the air-cooled category no
   invented downstream edge. The ManimCE comparison failed the visual quality
   bar and is retained only as a rejected experiment, not a production option.
10. **Planned-shot implementation without editorial overreach — resolved.** All
    21 planned requests compile into deterministic derived 2D/3D frames with
    exact semantic focus and reveal bundles. Navigation and anchor comparison are
    manual. Browser QA approved the derived frames for the complete runtime; the
    requests remain outside the reusable-camera library, which is a geometry
    ownership distinction rather than an evidence or recording gate.
11. **Full-course runtime and packet — resolved.** The generated 26-segment
    player exposes opening question, objective, focus, context, evidence status,
    claim values, primary-source links, and handoff. Every transformation is
    presenter-controlled. The instructor packet mirrors that territory without
    durations, cadence, or words-to-say instructions.
12. **Cross-ledger semantic overreach — resolved.** The final adversarial pass
    added explicit installed-turbine, CDU, CRAH, interconnection-path, permanent-
    transformer, substation-to-load, and conceptual-to-as-built boundaries;
    duplicate voltage, rack-input, building-count, and live-by claims were
    removed from the teaching bundles.
13. **Schedule and storage overclaim — resolved.** Equipment availability is
    taught as heterogeneous market, procurement, and acceptance evidence rather
    than Abilene's critical path. The transient segment no longer highlights the
    conceptual BESS connection and keeps both the site transient profile and
    connection explicit unknowns.
14. **Scenario method promotion — resolved.** Source-published methods remain
    `method_reference`; project synthesis is a separate
    `derived_scenario_reference`. The MW-to-token recipe now separates power-rate
    and energy-yield routes, reconciles hardware quantity with power, requires
    matching workload efficiency, and stops when a site input is unavailable.
15. **Instructor-facing redlines — resolved.** Every validated promotion guard
    is rendered as a plain-language warning in both the evidence drawer and the
    instructor packet. Named-role and facility-financing facts cannot be read as
    per-node assignments merely because the full topology is highlighted.
16. **Recording reliability and keyboard containment — resolved.** Exact
    Three.js 0.170.0 modules and license are vendored locally, startup failure is
    visible, embedded JSON is script-safe, the evidence drawer is inert while
    hidden, focus is restored on close, and drawer scroll resets by segment.

## Acceptance checks

- Complete coverage of every base-visible master node and edge.
- Canonical next-segment transitions and backward-only dependency references.
- Exact existing-camera focus and explicit node/edge/copy reveal bundles for
  planned shots.
- Reusable cameras reject unknown or base-hidden focus copy.
- Qualified multi-ledger fact resolution and topology/overlay locality.
- Assertion posture/lifecycle compatibility and required promotion guards.
- Research-gated regressions still require concrete blockers; evidence-ready
  segments reject blockers and empty claim bundles.
- Finite positive weights with an exact declared total.
- Explicit readiness regression checks for the initial grid path and full
  thermal replay.
- Exact s10 pilot scope, absence of timing fields and automatic advance,
  deterministic native output, and manual browser QA.
- Exact 21-shot registry coverage, deterministic derived framing, hidden
  reveal integrity, absence of timing or autoplay, and manual browser QA.
- Exact 26-segment runtime coverage, deterministic instructor-packet generation,
  manual focus/context/evidence controls, and browser QA across every state.
- Exact local Three.js hashes, zero CDN imports, visible startup failure, and
  network-independent 2D/3D playback.
- Separate published-method and derived-scenario assertions with mandatory
  time-basis, power-to-compute, and scenario-to-site guards.

The package is ready for an instructor walkthrough and recording rehearsal.
Course length and dwell remain presenter-owned editorial choices.
