# GIGAWATT

A diagram-led course that follows energy from grid or behind-the-meter
origination to a GPU die, then follows the resulting heat through liquid cooling
to the atmosphere.

Committed champion status: **record-ready, evidence-bounded v1** at
`9a76191764c9b2d998950069090548439dfc4007`. No working-tree variant is
accepted. Current compiled challenger statuses (`diagram/course_quality.json`):
`labels_only` modeled `pending`, Pareto `pending`, final `pending`;
`annotations_only` modeled `failed`, Pareto `rejected`, final `rejected`;
`combined` modeled `pending`, Pareto `pending`, final `pending`. The `combined`
challenger is the current rendered runtime. Final acceptance is separate from
modeled/Pareto evaluation. Required final-acceptance gate IDs:
`prerequisite_correctness_repairs`,
`historical_frozen_champion_viewport_captures`, `browser`,
`accessibility_snapshot`, `blind_review`. The blind-review gate requires two of
three reviewer preferences. The 2D master is the semantic engineering map; the
3D scene supplies campus orientation and spatial views. Both use the same 30
node IDs and 34 edge IDs. The complete course contains seven acts and 26
presenter-controlled, evidence-ready segments.

## Current artifacts

- `diagram/master.svg` — evidence-gated conceptual one-line and thermal process
  schematic. It is not an as-built drawing and is not for design/construction.
- `diagram/hybrid.html` — a six-state 2D → 3D → 3D → 3D → 2D overlay → 3D
  vertical slice generated from `master.yaml`, `scene.yaml`, and `cameras.yaml`.
- `diagram/s10_two_rack_heat_paths.html` — an instructor-controlled native
  pilot with four coarse transformations and no timing or automatic advance.
- `diagram/planned_shots.html` — a manual review surface for all 21 derived
  planned-shot frames, with shot-versus-anchor comparison and no autoplay.
- `diagram/planned_shots.json` — deterministic shot registry compiled from the
  course, semantic master, 2D layout, 3D scene, and camera anchors.
- `diagram/course.html` — the complete untimed 26-segment presenter runtime,
  with manual section navigation and a claim-first evidence drawer.
- `diagram/course_runtime.json` — deterministic full-course state registry.
- `course/INSTRUCTOR_PACKET.md` — generated teaching territory, claim
  boundaries, source links, and handoffs; it is neither timing nor a script.
- `course/TESTING.md` — the untimed editorial walkthrough and feedback format.
- `diagram/vendor/three/` — the pinned local Three.js 0.170.0 runtime, required
  addons, and upstream MIT license for network-independent playback.
- `evidence/abilene.yaml` — 14-source, 48-fact primary-source ledger for the
  original eight-building Abilene Stargate campus.
- `evidence/abilene_execution.yaml`, `evidence/delivery_resilience.yaml`, and
  `evidence/commercial_compute.yaml` — separately scoped execution,
  delivery/transient, ownership/financing/business-model, and compute-method
  ledgers. Contract/accounting, electrical, and thermal engineering references
  remain isolated in their own ledgers.
- `course/segments.yaml` — canonical act and segment order, camera requirements,
  topology focus, claim-level fact bindings, transitions, and research gates.
- `REDLINE.md` — disposition record for the engineering and legibility review.
- `course/REDLINE.md` — disposition record for course sequencing, claim
  binding, readiness, and production-shot review.

The Abilene overlay distinguishes lifecycle states instead of adding unlike
capacity figures:

- The 200 MW / 138 kV initial station and separate 1 GW / 345 kV expansion
  station are shown as energized; their exact common downstream topology is not
  asserted.
- The 360.5 MW gas fleet and 169.9 MW / 62-unit diesel layer are permits or
  authorizations; installation and commissioning remain unproven.
- BESS is shown only as future design.
- NVIDIA GB200 is the confirmed operating rack family. NVL72 topology and
  nominal 50–51 VDC are retained only as design/product references, and the
  detailed cooling packages remain conceptual rather than as-built claims.
- Exact campus-wide MV, rack AC input, generator terminal configuration,
  operational building count, and installed GPU count remain explicit unknowns.
- Installed GPU count carries the literal result `no evidence-backed estimate`.

## Build and verify

```sh
uv run gigawatt-symbols
uv run gigawatt-layout
uv run gigawatt-scene
uv run gigawatt-shots
uv run gigawatt-course
uv run python diagram/generate_s10_two_rack_heat_paths.py
uv run gigawatt-quality
uv run gigawatt-validate
uv run python -m unittest discover -s tests -v
```

`gigawatt-quality` writes a non-aggregated quality registry for all 26
segments at five protected viewports plus the inspectable dependency graph
from primary sources through viewport evaluations. Its ratchet manifest keeps
the frozen champion, isolated challengers, and still-pending live acceptance
gates explicit.

To inspect the hybrid player locally:

```sh
python3 -m http.server --directory diagram 8000
```

Then open `http://localhost:8000/course.html` for the complete course. Use the
left/right arrows or segment rail to advance and `Show evidence` for sourced
claims, known limits, and primary sources. No state advances automatically.
Open `http://localhost:8000/hybrid.html` for the
spatial substrate or
`http://localhost:8000/s10_two_rack_heat_paths.html` for the manual teaching
pilot. Open `http://localhost:8000/planned_shots.html` to inspect every planned
shot and compare its derived frame with the reusable anchor. All course browser
surfaces load the pinned Three.js runtime locally; no CDN connection is needed.

## Source-of-truth boundaries

- `evidence/*.yaml`: registered primary-source ledgers and scoped facts.
- `diagram/master.yaml`: topology, lifecycle, copy templates, and fact IDs.
- `diagram/layout.yaml`: 2D placement only.
- `diagram/scene.yaml`: 3D placement only.
- `diagram/cameras.yaml`: reusable camera states plus the current six-state
  vertical-slice demo order; it is not the full course sequence.
- `diagram/planned_shots.json` and `.html`: derived review artifacts for the 21
  planned requests; they do not promote those requests to approved cameras.
- `diagram/course_runtime.json` and `course.html`: the complete manual teaching
  package. They package camera requests and evidence but do not change their
  source-of-truth owners.
- `course/segments.yaml`: canonical course order, learning objectives,
  qualified fact references, production-shot requirements, and narrative
  transitions.
- `course/pilots/*.yaml`: coarse instructor-controlled transformations for
  renderer trials; these are neither course timing nor spoken scripts.
- `src/gigawatt/tokens.py`: shared palette and line system.
- `diagram/vendor/three/`: byte-verified Three.js runtime assets; tests pin their
  exact 0.170.0 hashes and license.

All 26 segments in the frozen champion are ready to teach within their validated
evidence boundaries. The current challenger has the same 26-section inventory
but is not a new baseline while live acceptance remains pending. Readiness does
not convert unavailable as-built configuration, private contract terms, current
IT load, utilization, or token throughput into facts; the player shows those
unknowns explicitly.

The validator fails on unresolved factual copy, duplicate YAML keys, unknown
sources or IDs, mismatched fact/source bindings, incompatible lifecycle
promotion, course-claim promotion, misplaced segment evidence, missing
assertion guards, broken dependencies or narrative transitions, incomplete
course coverage, undeclared hidden-overlay reveals, non-finite production
weights, unsafe reusable-camera focus copy, 2D/3D coverage drift, stale
generated output or instructor packet, a derived scenario promoted to a
published method, or a cooling tower leaking into the Abilene base topology.
