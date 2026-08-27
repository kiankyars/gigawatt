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
unset until editorial review of the completed inventory.

## Evidence readiness

Seven segments are `evidence_ready`. Their current claims can be scripted within
the manifest's explicit promotion guards. Nineteen are `research_required` and
are not record-ready for their full learning objective until every listed
blocking question has a validated evidence pack.

The research queue is intentionally concentrated in:

- turbine, generator, GSU, facility-electrical, VRM, CDU, and CRAH engineering;
- contractual PPA boundaries;
- interconnection chronology, equipment lead times, GPU-load transients, and
  Atlas construction evidence;
- ownership, financing, offtake, operations, and utilization-risk allocation;
- commissioned/current IT power, installed hardware, utilization, MFU,
  workload, and measured throughput for the power-to-tokens close.

Claim bundles use qualified references such as `abilene:rack_platform` rather
than copying values or source IDs. Schema v2 registers multiple evidence
ledgers, distinguishes facts bound to selected topology from explicit overlays,
rejects incompatible assertion/lifecycle pairs, derives mandatory promotion
guards, and keeps research-gated segments fail-closed. The installed-GPU null
retains its stronger `no_evidence_backed_estimate` assertion.

The redline conservatively gates the die energy-balance lesson and the
facility-loop lesson until generic engineering evidence lands. The rack split
stops at its evidenced package boundary, and the full thermal replay cannot be
promoted above its research-gated dependencies.

## Untimed s10 renderer comparison

`pilots/s10_two_rack_heat_paths.yaml` defines four coarse transformations for
the evidence-ready rack split: establish the rack, isolate liquid-cooled
compute, isolate air-cooled auxiliaries, and compare both categories. They are
manual visual selections, not beats. The manifest has no duration, cadence,
runtime, autoplay, or words-to-say contract; the instructor owns the dwell time
on every transformation.

The native Three.js version is generated at
`diagram/s10_two_rack_heat_paths.html`. The isolated ManimCE experiment in
`experiments/manim_s10/` renders the same transformations as independent short
clips. Both consumers validate the exact s10 node/edge boundary and expose the
same source digest. Neither may extend the air category to a CRAH, extend the
liquid path to a CDU, imply an Abilene as-built rack configuration, or encode a
quantitative liquid-versus-air heat split.

The pilot decision is to retain the native SVG/Three.js substrate as the
presenter-controlled course runtime. ManimCE remains an optional renderer for a
specific transition whose precomposed motion materially improves the
explanation; it is not the course player or a pacing system.

Generate and inspect the native pilot with:

```sh
uv run python diagram/generate_s10_two_rack_heat_paths.py
python3 -m http.server --directory diagram 8000
```

Open `http://localhost:8000/s10_two_rack_heat_paths.html`, then advance only
when the explanation calls for a different composition. There is no target
time per state. The ManimCE setup and one-clip render command are documented in
`experiments/manim_s10/README.md`.

## Production shots

Five segments reuse an existing camera state exactly. Twenty-one request a
planned shot or overlay anchored to one of the six validated states. Shot names
and explicit hidden node/edge/copy reveal bundles in this file are requirements;
their geometry belongs in `diagram/cameras.yaml` when each act enters
production. The current player remains a six-state hybrid demonstration until
those 21 shots and the course-sequence compiler are implemented.

Run the complete contract with:

```sh
uv run python diagram/generate_s10_two_rack_heat_paths.py
uv run gigawatt-validate
uv run python -m unittest discover -s tests -v
```
