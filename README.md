# GIGAWATT

A diagram-led course that follows energy from grid or behind-the-meter
origination to a GPU die, then follows the resulting heat through liquid cooling
to the atmosphere.

Status: **redline-verified v1**. The 2D master is the semantic
engineering map; the 3D scene supplies campus orientation and spatial zooms.
Both use the same 30 node IDs and 34 edge IDs. The complete course inventory
now contains seven acts and 26 evidence-gated segments.

## Current artifacts

- `diagram/master.svg` — evidence-gated conceptual one-line and thermal process
  schematic. It is not an as-built drawing and is not for design/construction.
- `diagram/hybrid.html` — a six-state 2D → 3D → 3D → 3D → 2D overlay → 3D
  vertical slice generated from `master.yaml`, `scene.yaml`, and `cameras.yaml`.
- `diagram/s10_two_rack_heat_paths.html` — an instructor-controlled native
  pilot with four coarse transformations and no timing or automatic advance.
- `experiments/manim_s10/` — an isolated ManimCE renderer for the same s10
  transformations and canonical IDs; generated comparison media is untracked.
- `evidence/abilene.yaml` — 14-source, 48-fact primary-source ledger for the
  original eight-building Abilene Stargate campus.
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
uv run python diagram/generate_s10_two_rack_heat_paths.py
uv run gigawatt-validate
uv run python -m unittest discover -s tests -v
```

To inspect the hybrid player locally:

```sh
python3 -m http.server --directory diagram 8000
```

Then open `http://localhost:8000/hybrid.html` for the spatial substrate or
`http://localhost:8000/s10_two_rack_heat_paths.html` for the manual teaching
pilot. Both players import their pinned Three.js runtime from the network.

## Source-of-truth boundaries

- `evidence/*.yaml`: registered primary-source ledgers and scoped facts.
- `diagram/master.yaml`: topology, lifecycle, copy templates, and fact IDs.
- `diagram/layout.yaml`: 2D placement only.
- `diagram/scene.yaml`: 3D placement only.
- `diagram/cameras.yaml`: reusable camera states plus the current six-state
  vertical-slice demo order; it is not the full course sequence.
- `course/segments.yaml`: canonical course order, learning objectives,
  qualified fact references, production-shot requirements, and narrative
  transitions.
- `course/pilots/*.yaml`: coarse instructor-controlled transformations for
  renderer trials; these are neither course timing nor spoken scripts.
- `src/gigawatt/tokens.py`: shared palette and line system.

The validator fails on unresolved factual copy, duplicate YAML keys, unknown
sources or IDs, mismatched fact/source bindings, incompatible lifecycle
promotion, course-claim promotion, misplaced segment evidence, missing
assertion guards, broken dependencies or narrative transitions, incomplete
course coverage, undeclared hidden-overlay reveals, non-finite production
weights, unsafe reusable-camera focus copy, 2D/3D coverage drift, stale
generated output, or a cooling tower leaking into the Abilene base topology.
