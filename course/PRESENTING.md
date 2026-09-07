# Teaching from the sample

[Open the visual presentation](sample.html) · [Read the lesson](sample-reading.html) · [Presenter notes](sample-notes.html)

The presentation is the screen-share surface. It shows one visual idea at a time.
Explain that idea aloud, ask for a prediction where prompted, then reveal or advance.
Do not scroll through the written lesson while narrating it.

## Recording workflow

1. Open the visual presentation in a browser window. Select **Presenter notes**
   to open a second window with the matching narration and action cues.
2. Share or capture only the visual window or browser tab. Keep notes on another
   display or outside the captured area. Sharing an entire display containing
   both windows would also show the notes.
3. Use **Next** or **→** to advance one visual at a time. **←** goes back.
   The numbered controls jump to a particular visual. **F** toggles fullscreen;
   **P** opens the notes. **R** reveals or hides an answer where applicable.
4. Pause before revealing current, conductor loss, and the final feeder answer.
   After revealing current, the voltage slider lets you vary one input while
   keeping delivered power fixed. Its arrow keys adjust voltage, not the slide.
5. Explain in your own words. Presenter notes contain the argument and model
   boundaries; they are not text for the audience to read along with you.

The two windows synchronize the step, answer visibility and selected voltage.
Open notes with the presentation's button to pair them. A notes page opened
independently has its own **Open visual** link. This uses browser-local messaging;
no account, server, or external service receives the presentation state.

**Read the lesson** opens the complete explanation, solved example, source notes
and practice. Viewers can use that page after the video or study independently.
The 50-lesson reading companion remains a reference manuscript. Only this sample
has an authored presentation sequence so far; the other lessons must be adapted
and rehearsed before they are called ready to record.

## A teaching contract for later lessons

A presentation step earns its place by making a mechanism, comparison or decision
visible. Give it one short headline, a prominent visual, and only the labels and
assumptions needed to interpret that visual. Put derivations, extended explanation,
citations and presenter actions in the notes or reference. Keep essential units
and model boundaries on the shared screen.

Author the sequence deliberately. Do not auto-convert each paragraph into a slide,
shrink the reading page, or reveal bullet lists while reading them aloud. Preserve
spatial positions across comparisons so a moved converter is the thing that changes.
Use code for exact relationships and calculations; illustrative images locate the
equipment without claiming an as-built topology.

The sample's seven steps have a five-minute rehearsal target. That is a planning
assumption, not a measured video duration. Technical comprehension, delivery pacing
and actual recorded legibility still require review.

## Editing

- `course/expansion/sample.json` owns the full written explanation.
- `course/expansion/sample-presentation.json` owns the seven authored beats,
  speaker notes, action cues and timing targets.
- `course/web/presentation.*` owns the visual presentation and notes console.
- `course/web/reader-models.js` supplies the same tested DC arithmetic to both.
- `uv run gigawatt-expand` regenerates `sample.html`, `sample-notes.html`,
  `sample-reading.html` and the full reader.

Preserve the tested calculation and its assumptions across all three surfaces.
Do not silently change a numerical default without reviewing the narration,
reference example and changed-case solution together.
