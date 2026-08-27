# Course production redline — disposition

Review date: 2026-08-27
Artifacts: `course/segments.yaml` and `course/pilots/s10_two_rack_heat_paths.yaml`
Posture: complete course inventory and production contract; not a finished
script, full-course player, or claim that every segment is record-ready.

## Release verdict

The seven-act, 26-segment inventory is approved to advance as a fail-closed
production contract. Seven segments are evidence-ready. Nineteen remain
research-gated and cannot be promoted by prose, camera work, or conceptual
diagram status.

## Blocking redlines

1. **Unknown voltage used as unknown topology — resolved.** Separate null facts
   now record the unverified campus source merge and BESS and diesel connection
   topologies. The 345 kV station secondary-voltage null is used only for
   voltage or ratio claims.
2. **Single-ledger course schema — resolved.** Schema v2 registers evidence
   ledgers and uses qualified fact references. The Abilene ledger remains the
   master-diagram ledger; future engineering, comparison, capital, and compute
   ledgers can be added without polluting its campus scope.
3. **Fail-open claim placement — resolved.** Every claim declares `topology` or
   `overlay` binding. Topology facts must belong to selected nodes or edges;
   overlays cannot bypass a fact already bound elsewhere in the master.
4. **Lifecycle and promotion ambiguity — resolved.** Assertions validate both
   lifecycle and posture. Mandatory promotion guards are derived from each
   assertion, and the installed-GPU null retains the literal
   `no evidence-backed estimate` boundary.
5. **Thermal readiness overstatement — resolved.** The die energy-balance and
   facility-loop lessons are gated pending engineering sources. The rack split
   ends at the evidenced rack-package boundary. The full thermal replay depends
   on the preceding thermal dossiers and cannot become ready first.
6. **Hidden contractual overlay without reveal semantics — resolved.** Planned
   PPA and ownership/model shots explicitly enumerate the hidden nodes, edges,
   and master-owned copy they must reveal as one bundle. Existing shots may not
   reveal hidden topology or labels.
7. **Two sequence owners — resolved by scope.** `course/segments.yaml` owns the
   canonical 26-segment order. `diagram/cameras.yaml` owns reusable camera states
   and the current six-state demonstration order only. The full-course compiler
   remains future production work.
8. **Semantic objective review — manual gate retained.** A validator cannot
   prove the truth of free-form pedagogical prose. This redline reviewed each
   objective against its claim bundle, selected topology, and blockers; factual
   narration and on-screen copy must still be generated from validated claims,
   not improvised from the objective text.
9. **s10 pacing, scope, and renderer choice — resolved.** The native pilot
   consumes one four-transformation manifest. Transformations advance only on
   instructor action and carry no editorial timing or spoken-script fields. The
   view stops at the four-node, three-edge rack-package boundary, preserves
   distinct liquid supply and return, and gives the air-cooled category no
   invented downstream edge. The ManimCE comparison failed the visual quality
   bar and is retained only as a rejected experiment, not a production option.

## Acceptance checks

- Complete coverage of every base-visible master node and edge.
- Canonical next-segment transitions and backward-only dependency references.
- Exact existing-camera focus and explicit node/edge/copy reveal bundles for
  planned shots.
- Reusable cameras reject unknown or base-hidden focus copy.
- Qualified multi-ledger fact resolution and topology/overlay locality.
- Assertion posture/lifecycle compatibility and required promotion guards.
- Research blockers reject empty and placeholder entries.
- Finite positive weights with an exact declared total.
- Explicit readiness regression checks for the initial grid path and full
  thermal replay.
- Exact s10 pilot scope, absence of timing fields and automatic advance,
  deterministic native output, and manual browser QA.

Runtime and packaging remain editorial choices. They do not block engineering,
evidence-pack, camera, or instructor-note work.
