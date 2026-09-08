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

The revised sample has eight steps. It first compares **48 V DC with 800 V DC**
at the receiving end of a fixed load. It then closes the conductor energy balance
using an invented loop resistance. Finally, a separate hypothetical loss budget
compares complete AC-distributed and DC-distributed arrangements serving the same
final DC load. The distinction is stated explicitly in the visuals and notes.

The earlier 150 kW feeder / 160 kW load exercise was an infeasible request, but its
ordinary arrow made it look like an operating flow. It is removed from the sample
ending. The old `#feeder-transfer` link now opens the complete-path loss comparison.

Timing targets are rehearsal prompts, not a recording instruction or measured
runtime. The revised sequence targets about six minutes before discussion. Only
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
