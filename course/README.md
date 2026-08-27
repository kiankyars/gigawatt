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

Ten segments are `evidence_ready`. Their current claims can be scripted within
the manifest's explicit promotion guards. Sixteen are `research_required` and
are not record-ready for their full learning objective until every listed
blocking question has a validated evidence pack.

The remaining research queue is intentionally concentrated in:

- site installation and configuration evidence for turbine, generator, GSU,
  facility electrical, rack power, CDU, CRAH, and facility-loop equipment;
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

Separate engineering ledgers now support the generic electrical and thermal
roles without promoting them to Abilene. The PPA/accounting boundary, die
energy-balance lesson, and technology supply/return lesson cleared their
research gates. Site-specific installation and configuration claims remain
blocked, and the full thermal replay cannot be promoted above its
research-gated dependencies.

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

Five segments reuse an existing camera state exactly. Twenty-one request a
planned shot or overlay anchored to one of the six validated states. Shot names
and explicit hidden node/edge/copy reveal bundles in this file are requirements;
their approved reusable geometry belongs in `diagram/cameras.yaml` when each act
enters production.

`gigawatt-shots` now compiles all 21 requests into deterministic provisional
frames and a manual review surface at `diagram/planned_shots.html`. The request
inventory is 11 overlays, seven 3D shots, and three 2D shots; their anchors
produce 13 review frames in 2D context and eight in 3D context. The compiler
validates exact topology and hidden reveal bundles and lets the reviewer switch
between each derived frame and its reusable anchor. The requests remain
`planned`: compilation makes them reviewable, not editorially approved or
record-ready.

The review surface contains no timing, script, cadence, autoplay, or automatic
transition contract. Select each shot manually or use the previous/next
controls; the instructor still owns every dwell and explanation.

Run the complete contract with:

```sh
uv run python diagram/generate_s10_two_rack_heat_paths.py
uv run gigawatt-shots
uv run gigawatt-validate
uv run python -m unittest discover -s tests -v
```
