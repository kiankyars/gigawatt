# Teach the sample

[Teaching endpoint](teach.html) · [Student exploration](sample.html) · [Full written lesson](sample-reading.html)

Kian's planned workflow is to **teach the course without recording first**. The
purpose of that dry run is to find gaps in understanding and make the eventual
recorded explanation smoother. Use the presentation for this pass. A suggestion
to study D04 in the prose reader does not replace the agreed presentation rehearsal.

## Three endpoints

- `course/sample.html` is the default student experience. It has visual steps,
  practice reveals and optional explanations. It has no presenter-notes button,
  teaching fullscreen control, presenter cues or recording instructions.
- `course/teach.html` enables teaching controls and the separate synchronized
  presenter-notes window. Use this endpoint for the unrecorded dry run and later
  for recording.
- `course/sample-notes.html` contains narration, action cues, next-step context
  and the lesson sequence. Open it from the teaching endpoint to pair the windows.
  Repetitive recording-setup instructions have been removed.

`sample-reading.html` preserves the complete reference explanation and source
limits. The two visual modes share calculations and lesson content. Mode selection
is a presentation choice, not an authentication or access-control boundary.

Use Next or **→** to advance, **←** to return and **R** to reveal or hide an answer.
In teaching mode, **P** opens notes and **F** toggles fullscreen. A focused slider
uses its arrow keys to change the input. The presenter window synchronizes the
step, answer visibility, DC voltage and the final conversion-loss control.

## Dry-run pass

Explain each visual in your own words. At a hesitation, note the step and whether
the issue was an undefined term, a missing mechanism, an unclear premise or an
unsupported assumption. Resolve knowledge gaps and revise the visual before
rehearsing it again. These observations are more useful now than a recording setup
checklist or polished delivery of an explanation that is not yet understood.

The revised sample has ten steps. Its purpose is to explain delivering more power
with less distribution copper and more room for compute. First compare **480 V
balanced three-phase AC with 800 V two-wire DC**, holding receiving-end real power
at 100 kW. Three equal copper lengths versus two make the one-third material
reduction visible under equal length, cross-section and material assumptions.
This is not a qualified cable design. Per-conductor current and total heat come
next, with the additional idealization of 10 mΩ effective resistance per conductor.
The architecture sequence marks occupied/released rack space and the destination
of the conversion equipment. A nearby sidecar does not imply net hall-space savings.

The complete-path comparison holds the **final useful DC load** at 100 kW instead. Both
paths begin at the same facility AC supply boundary. Assumed downstream conversion
losses raise the power each feeder delivers, and conductor heat is calculated from
that power. At the default conversion losses, DC requires about 1.144 kWh less
input over one hour. Raising total DC conversion loss from 3 to 6 kW reverses the
result: DC requires about 1.875 kWh more. Keep the boundary change visible; the
preceding 28% conductor-heat reduction is not a fixed whole-path saving.

Finish with `#capacity-check`: keep the 800 V feeder's conductors unchanged and
raise delivered power from 100 to 200 kW. Ask the learner to predict current,
heat and whether capacity is established. Current doubles to 250 A and heat
quadruples to 1.25 kW at fixed resistance; copper is unchanged by assumption.
Operating capacity remains unverified without the equipment and thermal limits.
This ending tests whether the learner can apply the mechanism to growth.

The earlier 150 kW feeder / 160 kW load exercise was an infeasible request, but its
ordinary arrow made it look like an operating flow. It is removed from the sample
ending. The old `#feeder-transfer` link now opens the complete-path loss comparison.

Timing targets are rehearsal prompts, not a recording instruction or measured
runtime. Allow roughly fifteen minutes for explanation, predictions and discussion;
revise these provisional allocations after the dry run. Only
this sample has a complete presentation sequence; the other 50 lessons remain
reading material pending adaptation and dry runs. Recording follows those passes.

## Authoring contract

Show one mechanism, comparison or decision at a time. Keep essential units,
boundaries and assumptions visible. Put extended explanation and source limits
in the student reference, and narration/actions in the presenter notes. Do not
auto-convert paragraphs into slides or use a glossary as a substitute for a
visual introduction to the equipment.

- `course/expansion/sample.json`: full explanation and changed-case practice.
- `course/expansion/sample-presentation.json`: visual sequence, notes, student
  explanations, aliases and rehearsal targets.
- `course/web/presentation.*`: student, teaching and presenter interfaces.
- `course/web/reader-models.js`: shared, tested calculation functions.
- `uv run gigawatt-expand`: generates both visual modes, notes, reading pages
  and the full manuscript.

Preserve the same calculation and assumptions across the three surfaces.
The [course-wide teaching standard](TEACHING_STANDARD.md) defines the reusable
learning contract, the functional BOM and the adaptation plan for all domains.
The builder now checks the contract and teaching roles without imposing the
sample's scene count on future authored sequences.
