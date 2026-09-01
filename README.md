# GIGAWATT

A diagram-led course that follows energy from grid or behind-the-meter
origination to a GPU die, then follows the resulting heat through liquid cooling
to the atmosphere.

The canonical course is the manual six-phase v2 player at
`diagram/course_v2.html`:

`Generate -> Transmit -> Campus -> Building -> Compute -> Reject heat`

It uses explanatory canvases for mechanisms, the Abilene engineering map for
case application and evidence boundaries, and one persistent phase compass.
GitHub Pages publishes this player at the project site root together with its
six phase renderers. The byte-preserved v1 comparison remains available at
`/gigawatt/v1.html`.

Historical v1 comparison status: **record-ready, evidence-bounded v1** at
`0856a93b78181bec3945168632d141595575800c`. No working-tree variant is
accepted. The current evidence epoch starts unresolved. Current compiled challenger statuses
(`diagram/course_quality.json`):
`labels_only` modeled `pending`, Pareto `pending`, final `pending`;
`annotations_only` modeled `failed`, Pareto `rejected`, final `rejected`;
`combined` modeled `pending`, Pareto `pending`, final `pending`. The `combined`
challenger is the current rendered runtime. Frozen champion
`0856a93b78181bec3945168632d141595575800c` is the immutable accepted snapshot;
the next epoch starts with fresh, unresolved evidence. Final acceptance is
separate from modeled/Pareto evaluation. Required final-acceptance gate IDs:
`prerequisite_correctness_repairs`,
`historical_frozen_champion_viewport_captures`, `browser`,
`accessibility_snapshot`, `blind_review`. The blind-review gate requires two of
three reviewer preferences. The prior epoch's three-of-three candidate
preference and its complete acceptance corpus remain preserved in the frozen
commit and its Git ancestry; they are not reused as current-epoch evidence. The
2D master is the semantic engineering map; the 3D scene supplies campus
orientation and spatial views. Both use the same 30 node IDs and 34 edge IDs.
The frozen v1 course contains seven acts and 26 presenter-controlled,
evidence-ready segments.

## Canonical six-phase course

V2 is the production teaching surface. It follows one six-phase engineering
journey through a branching power-and-heat service chain:

`Generate -> Transmit -> Campus -> Building -> Compute -> Reject heat`

`course/CURRICULUM_V2.md` owns the curriculum contract. Generic explanatory
canvases teach each mechanism before the Abilene engineering map is used as the
case and evidence layer. All six source-bound phase renderers compile into one
responsive player with 33 coarse manual states and no timing, autoplay, or
spoken-script contract. The standalone phase pages remain development fixtures;
`diagram/course_v2.html` is the canonical runtime. Grid and onsite source paths
remain distinct unless evidence establishes a merge; the course does not imply
one traced electron path through every phase.

## Current artifacts

- `diagram/master.svg` — evidence-gated conceptual one-line and thermal process
  schematic. It is not an as-built drawing and is not for design/construction.
- `diagram/hybrid.html` — a six-state 2D → 3D → 3D → 3D → 2D overlay → 3D
  vertical slice generated from `master.yaml`, `scene.yaml`, and `cameras.yaml`.
- `diagram/s10_two_rack_heat_paths.html` — an instructor-controlled native
  pilot with four coarse transformations and no timing or automatic advance.
- `diagram/phase1_generation.html` through `diagram/phase6_heat.html` — the six
  evidence-bound explanatory canvases loaded by the canonical player.
- `diagram/course_v2.html` — the canonical six-phase manual course player.
- `diagram/course_v2_runtime.json` — the deterministic v2 course registry.
- `course/INSTRUCTOR_PACKET_V2.md` — generated teaching territory, evidence
  boundaries, state instructions, and phase transitions for v2.
- `diagram/planned_shots.html` — a manual review surface for all 21 derived
  planned-shot frames, with shot-versus-anchor comparison and no autoplay.
- `diagram/planned_shots.json` — deterministic shot registry compiled from the
  course, semantic master, 2D layout, 3D scene, and camera anchors.
- `diagram/course.html`, `diagram/course_runtime.json`, and
  `course/INSTRUCTOR_PACKET.md` — the frozen v1 comparison package.
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
uv run python diagram/generate_phase1_generation.py
uv run python diagram/generate_phase2_transmission.py
uv run python diagram/generate_phase3_campus.py
uv run python diagram/generate_phase4_building.py
uv run python diagram/generate_phase5_compute.py
uv run python diagram/generate_phase6_heat.py
uv run python diagram/generate_course_v2.py
uv run gigawatt-quality
uv run gigawatt-validate
uv run python -m unittest discover -s tests -v
```

`gigawatt-quality` writes a non-aggregated quality registry for all 26
segments at five protected viewports plus the inspectable dependency graph
from primary sources through viewport evaluations. Its ratchet manifest keeps
the frozen champion, isolated challengers, candidate-bound acceptance evidence,
and promotion eligibility explicit.

To inspect the canonical course locally:

```sh
python3 -m http.server --directory diagram 8000
```

Open `http://localhost:8000/course_v2.html`. Use the phase compass for the six
engineering problems, the state rail for coarse explanatory transformations,
and the evidence drawer for scoped claims and primary sources. No state advances
automatically. In Phases 4 through 6, `3D spatial anchor` manually opens the
validated electrical-room, rack, or thermal-return camera at widths of 900 px
and above; `Return to 2D teaching` restores the causal view. These anchors are
conceptual spatial references, not Abilene as-built claims. Open
`http://localhost:8000/course.html` only for the frozen v1 comparison.
`s10_two_rack_heat_paths.html` and `planned_shots.html` remain development and
review surfaces. The v2 teaching canvases are self-contained; its optional 3D
mode and the archived v1 load the pinned Three.js runtime locally rather than
from a CDN.

## Source-of-truth boundaries

- `evidence/*.yaml`: registered primary-source ledgers and scoped facts.
- `diagram/master.yaml`: topology, lifecycle, copy templates, and fact IDs.
- `diagram/layout.yaml`: 2D placement only.
- `diagram/scene.yaml`: 3D placement only.
- `diagram/cameras.yaml`: reusable camera states plus the current six-state
  vertical-slice demo order; it is not the full course sequence.
- `diagram/planned_shots.json` and `.html`: derived review artifacts for the 21
  planned requests; they do not promote those requests to approved cameras.
- `course/course_v2.yaml`: canonical v2 phase order, questions, phase inputs and
  outputs, renderer paths, and closing synthesis.
- `course/pilots/*.yaml`: source manifests for the six coarse
  instructor-controlled phase surfaces; these are neither course timing nor
  spoken scripts.
- `diagram/course_v2_runtime.json`, `course_v2.html`, and
  `course/INSTRUCTOR_PACKET_V2.md`: generated v2 package compiled from the spine,
  phase manifests, rendered phase payloads, and registered evidence.
- `course/segments.yaml`, `diagram/course_runtime.json`, and `course.html`: the
  frozen v1 order and generated comparison runtime.
- `src/gigawatt/tokens.py`: shared palette and line system.
- `diagram/vendor/three/`: byte-verified Three.js runtime assets; tests pin their
  exact 0.170.0 hashes and license.

All 26 segments in the frozen champion are ready to teach within their validated
evidence boundaries. The current working tree has the same 26-section runtime,
but its next-epoch challenger records remain pending until they receive fresh
acceptance evidence. Readiness does not convert unavailable as-built
configuration, private contract terms, current IT load, utilization, or token
throughput into facts; the player shows those unknowns explicitly.

The validator fails on unresolved factual copy, duplicate YAML keys, unknown
sources or IDs, mismatched fact/source bindings, incompatible lifecycle
promotion, course-claim promotion, misplaced segment evidence, missing
assertion guards, broken dependencies or narrative transitions, incomplete
course coverage, undeclared hidden-overlay reveals, non-finite production
weights, unsafe reusable-camera focus copy, 2D/3D coverage drift, stale
generated output or instructor packet, a derived scenario promoted to a
published method, or a cooling tower leaking into the Abilene base topology.
