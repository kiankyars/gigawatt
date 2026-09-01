# Course inventory

`course_v2.yaml` is the canonical course spine. It orders six system phases,
their input/output boundaries, renderer artifacts, and the closing synthesis. The
compiled production player is `../diagram/course_v2.html`.

`segments.yaml` remains the frozen v1 comparison order: seven acts and 26
segments built on the validated master diagram and six camera anchors. It is no
longer the production course sequence.

## Canonical six-phase v2 course

`CURRICULUM_V2.md` defines one engineering journey across six explanatory
phases:

`Generate -> Transmit -> Campus -> Building -> Compute -> Reject heat`

The v2 policy is “one journey, multiple explanatory canvases.” Clean teaching
views establish causal mechanisms first; the Abilene redline is then used for
the case mapping and exact known/unknown boundary. Manual states represent
coarse conceptual changes, never target durations, autoplay, micro-beats, or a
spoken script. Grid and onsite generation remain branching source paths; the
spine does not assert one traced carrier or an evidenced downstream merge where
the site record is silent.

Each phase has a strict manifest under `pilots/` and a deterministic standalone
renderer under `../diagram/`. Build the six renderers before the unified player:

```sh
uv run python diagram/generate_phase1_generation.py
uv run python diagram/generate_phase2_transmission.py
uv run python diagram/generate_phase3_campus.py
uv run python diagram/generate_phase4_building.py
uv run python diagram/generate_phase5_compute.py
uv run python diagram/generate_phase6_heat.py
uv run python diagram/generate_course_v2.py
python3 -m http.server --directory diagram 8000
```

Open `http://localhost:8000/course_v2.html`. The persistent phase compass keeps
the learner oriented while the state rail changes only coarse explanatory
relationships. The six standalone phase pages are development fixtures loaded
by the compiled player, not separate course chapters.

The production package is `../diagram/course_v2.html`,
`../diagram/course_v2_runtime.json`, and `INSTRUCTOR_PACKET_V2.md`. GitHub Pages
publishes the player at the site root, its six phase dependencies beside it, the
optional `../diagram/hybrid.html` spatial surface with its master-map and local
Three.js assets, and the byte-preserved v1 comparison at
`/gigawatt/v1.html`. The player
offers validated conceptual 3D anchors only in Phases 4 through 6 and only at
900 px and wider; the 2D states remain the causal and evidence-owning surfaces.

The inventory owns pedagogy only:

- act and segment order;
- opening questions and learning objectives;
- master node and edge focus;
- existing camera anchors and requested production shots;
- claim-level fact bindings, promotion guards, and research blockers;
- narrative transitions and relative production weight.

It does not own factual values, sources, topology, lifecycle, coordinates, or
camera geometry. Those remain in registered `evidence/*.yaml` ledgers,
`diagram/master.yaml`, and `diagram/cameras.yaml`.

## Frozen v1 structure

| Act | Segments | Purpose |
| --- | ---: | --- |
| The missing gigawatt | 2 | Establish the lifecycle and evidence grammar. |
| Origination and interconnection | 6 | Separate the three source branches and campus boundary. |
| Electrical descent to the die | 2 | Follow the conceptual building and rack power train. |
| Return the heat | 8 | Complete the near-symmetric thermal half of the figure-eight. |
| Chokepoint reread | 4 | Reinterpret the same equipment as schedule and commissioning gates. |
| Capital-stack reread | 3 | Recolor the topology by ownership, financing, and utilization risk. |
| From delivered power to usable compute | 1 | Close with an assumption-bound conversion recipe. |

The physical electrical sequence and thermal-return sequence carry nearly equal
relative weight. The weights are not minutes: runtime remains deliberately
unset because the presenter owns the dwell and total course length.

## Frozen v1 evidence readiness

All 26 segments are `evidence_ready`. Their current claims can be taught within
the manifest's explicit promotion guards. Readiness means the learning
objective is supported by authoritative claim territory and an explicit
boundary; it does not require private as-built or commercial facts to exist.

Unavailable site values remain course content rather than silent gaps:

- generator terminal voltage, GSU configuration and protection settings;
- building/rack electrical configuration and detailed CDU/CRAH interfaces;
- current operational building count, facility load, and critical IT load;
- legal asset ownership and undisclosed financing or risk-allocation terms;
- installed accelerator count, utilization, MFU, workload configuration, and
  measured token throughput.

Claim bundles use qualified references such as `abilene:rack_platform` rather
than copying values or source IDs. Schema v2 registers multiple evidence
ledgers, distinguishes facts bound to selected topology from explicit overlays,
rejects incompatible assertion/lifecycle pairs, derives mandatory promotion
guards, and keeps research-gated segments fail-closed. The installed-GPU null
retains its stronger `no_evidence_backed_estimate` assertion.

Published methods and project-authored scenario logic are separate assertion
classes. The MW-to-token close keeps power-rate and energy-yield routes on a
common interval, requires an explicit hardware/power/workload bridge, and stops
without a site estimate when an Abilene input is unavailable.

Separate engineering ledgers support generic electrical and thermal roles
without promoting them to Abilene. Execution, delivery/resilience, and
commercial/compute ledgers add dated primary evidence while preserving every
site-specific null. This lets the complete thermal replay, chokepoint reread,
capital reread, and MW-to-token recipe become teachable without invented facts.

## Canonical untimed v2 runtime

`diagram/course_v2.html` packages the six phases and 33 coarse manual states in
one player. The outer shell owns the opening journey, phase compass, phase
input/output boundary ribbon, state navigation, evidence drawer, keyboard
behavior, and closing synthesis. Every phase renderer supplies only its
explanatory canvas. No timing, autoplay, cadence, or spoken script is encoded.

`course/INSTRUCTOR_PACKET_V2.md` is generated from the same compiled registry.
It carries teaching territory, state instructions, evidence boundaries, source
links, and phase transitions without prescribing the instructor's wording or
dwell time.
`course/TESTING.md` defines the v2 editorial walkthrough.

## Frozen v1 runtime

`diagram/course.html` packages all 26 segments in canonical order. Every change
is manual. The presenter advances between focused course sections and may open
the evidence panel on demand; neither action is timed. The generic context/focus
zoom was removed because it changed camera geometry without adding teaching
content. `course/INSTRUCTOR_PACKET.md` carries the same opening questions,
objectives, claim boundaries, primary-source links, plain-language promotion
warnings, and transitions in a printable form. The evidence drawer is keyboard
contained while closed and restores focus when dismissed.

The player, planned-shot review, hybrid substrate, and native pilot load the
pinned Three.js 0.170.0 modules from `diagram/vendor/three/`; recording does not
depend on a CDN.

## Untimed s10 native pilot

`pilots/s10_two_rack_heat_paths.yaml` defines four coarse transformations for
the evidence-ready rack split: establish the rack, isolate liquid-cooled
compute, isolate air-cooled auxiliaries, and compare both categories. They are
manual visual selections, not beats. The manifest has no duration, cadence,
runtime, autoplay, or words-to-say contract; the instructor owns the dwell time
on every transformation.

The native Three.js version is generated at
`diagram/s10_two_rack_heat_paths.html`. It validates the exact s10 node/edge
boundary. It may not extend the air category to a CRAH, extend the liquid path
to a CDU, imply an Abilene as-built rack configuration, or encode a
quantitative liquid-versus-air heat split.

The pilot decision is to use the native SVG/Three.js substrate as the
presenter-controlled course runtime and not pursue ManimCE. Visual review found
that the generated Manim clips read as generic vector rendering rather than
purpose-built explanatory animation. Reaching the desired quality would
require bespoke design and choreography that does not justify a second
renderer for this course. The spike remains in `experiments/manim_s10/` only as
an evaluation record and is outside the production and validation path.

Generate and inspect the native pilot with:

```sh
uv run python diagram/generate_s10_two_rack_heat_paths.py
python3 -m http.server --directory diagram 8000
```

Open `http://localhost:8000/s10_two_rack_heat_paths.html`, then advance only
when the explanation calls for a different composition. There is no target
time per state.

## Production shots

Five segments reuse an existing camera state exactly. Twenty-one use a
deterministically derived shot or overlay anchored to one of the six validated
states. Shot names and explicit hidden node/edge/copy reveal bundles in this
file are requirements. Their source requests remain `planned` because they are
not promoted into the small reusable-camera library; that geometry-ownership
status is separate from segment evidence and recording readiness.

`gigawatt-shots` compiles all 21 requests into deterministic derived
frames and a manual review surface at `diagram/planned_shots.html`. The request
inventory is 11 overlays, seven 3D shots, and three 2D shots; their anchors
produce 13 review frames in 2D context and eight in 3D context. The compiler
validates exact topology and hidden reveal bundles and lets the reviewer switch
between each derived frame and its reusable anchor. Browser QA approved all 21
derived frames in frozen champion
`0856a93b78181bec3945168632d141595575800c` without promoting them into reusable
cameras. That historical result is not browser evidence for the current
working-tree challengers.

No working-tree variant is accepted. The current evidence epoch starts
unresolved. Current compiled challenger statuses
(`diagram/course_quality.json`): `labels_only` modeled `pending`, Pareto
`pending`, final `pending`; `annotations_only` modeled `failed`, Pareto
`rejected`, final `rejected`; `combined` modeled `pending`, Pareto `pending`,
final `pending`. The `combined` challenger is the current rendered runtime.
Frozen champion `0856a93b78181bec3945168632d141595575800c` is the immutable
accepted snapshot; the next epoch starts with fresh, unresolved evidence. Final
acceptance is separate from modeled/Pareto evaluation. Required
final-acceptance gate IDs: `prerequisite_correctness_repairs`,
`historical_frozen_champion_viewport_captures`, `browser`,
`accessibility_snapshot`, `blind_review`. The blind-review gate requires two of
three reviewer preferences. The prior epoch's three-of-three candidate
preference, 10 typed reports, 13 reviewed occupancy PNGs, and raw comparison
corpus remain preserved in the frozen commit and its Git ancestry; they are not
reused as current-epoch evidence.

The review surface contains no timing, script, cadence, autoplay, or automatic
transition contract. Select each shot manually or use the previous/next
controls; the instructor still owns every dwell and explanation.

Run the complete contract with:

```sh
uv run python diagram/generate_s10_two_rack_heat_paths.py
uv run gigawatt-shots
uv run gigawatt-course
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

The quality compiler writes `diagram/course_quality.json` and
`diagram/course_dependency_graph.json`. It preserves per-dimension and
per-viewport vectors rather than collapsing them into a weighted average;
modeled/Pareto eligibility cannot satisfy any separate final-acceptance gate.
