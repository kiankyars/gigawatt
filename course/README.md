# Course inventory

`segments.yaml` is the canonical course order. It contains seven acts and 26
segments built on the validated master diagram and six camera anchors.

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

## Current structure

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

## Evidence readiness

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

## Complete untimed runtime

`diagram/course.html` packages all 26 segments in canonical order. Every change
is manual. The presenter may move between the focused frame, its reusable
context, and the evidence panel, but none of those transformations is required
or timed. `course/INSTRUCTOR_PACKET.md` carries the same opening questions,
objectives, claim boundaries, primary-source links, plain-language promotion
warnings, and handoffs in a printable form. The evidence drawer is keyboard
contained while closed and restores focus when dismissed. `course/TESTING.md`
defines the editorial walkthrough.

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
derived frames for the complete course runtime without promoting them into
reusable cameras.

The review surface contains no timing, script, cadence, autoplay, or automatic
transition contract. Select each shot manually or use the previous/next
controls; the instructor still owns every dwell and explanation.

Run the complete contract with:

```sh
uv run python diagram/generate_s10_two_rack_heat_paths.py
uv run gigawatt-shots
uv run gigawatt-course
uv run gigawatt-validate
uv run python -m unittest discover -s tests -v
```
