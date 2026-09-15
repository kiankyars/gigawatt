# Present From Watts to Tokens

## The next pass

The current pass is [Chapter 5, slides 14–20](prototypes/site-format.html?teach=1#service-envelope). This section was rebuilt around handling, replacement access, floor loads and failure boundaries. Then revisit the changed earlier cases as needed; the [review tracker](COURSE_REVIEW.md#chapter-5-physical-design-rebuild--2026-09-12) accounts for each request.

The preceding changes remain available at:

1. [Chapter 4: generation through the delivery decision](prototypes/siting-format.html?teach=1#dania-cycle): clarified plant example, new GPT figure, cost curves, Southaven plans and supported compute economics.
2. [Chapter 7: continuity, storage and protection](prototypes/continuity-format.html?teach=1#equipment): simpler labels, capacitor support, generator charging and restoration of DC-link voltage.

Chapter 5’s first-pass feedback is implemented; your acceptance is still pending. Continue any unresolved Chapter 2 or 3 items at their specific slides; do not restart the unchanged Primer, 800 V or cooling sequence.
The [chapter tracker](COURSE_REVIEW.md#chapter-review-tracker) separates implemented
changes, technical checks and your final acceptance.

Teach aloud without recording. When a slide leaves you explaining around an
unclear picture, send its URL and the precise confusion. Revise that mechanism,
then continue. There is no mandatory quiz or approval checklist between chapters.

## Open and present

The published reader is at the [site root](https://kiankyars.github.io/gigawatt/).
Open a chapter’s slides from the one chapter directory. The header provides
**Back to course**, **Reading** and, in teaching mode, **Full screen**.
Explanation/source dialogs and note-launch buttons are removed from slide views;
the written lesson holds definitions, derivations and sources.

**Presenter** opens a separate window showing only the upcoming slide, filling
that window. Put it on your second monitor and record the original course
window, which shows the current slide. There is no duplicate current slide,
thumbnail overlay, timer or notes panel. The upcoming slide shows its starting
state; interact with the current slide in the original window.

The presenter's small footer controls the original window: its selector names
the current audience slide, while “Up next” gives the number of the slide shown
on the second monitor. Either window's navigation advances both views. In the
presenter window, arrow keys, Page Up / Page Down and Space navigate; Home / End
select the first or last audience slide. Focused controls keep their own keyboard
behavior. At the last slide, the presenter shows “End of chapter” and offers the
next chapter when available. Closing the presenter leaves the audience unchanged;
**Presenter** opens it again. If the browser blocks the popup, allow popups for
this site and click the button again.

Use **Next / →**, **Back / ←**, the short slide selector and diagram controls.
Where a meaningful prediction has a reveal, use its button; the 800 V sequence
also supports **R**. **F** enters fullscreen in decks that support it. A focused
slider uses arrow keys to change its value. The site follows the device’s light
or dark appearance. Press Escape to leave fullscreen.

Clean public routes include `/slides/primer.html`, `/slides/workloads.html`,
`/slides/siting.html`, `/slides/site-design.html`, `/slides/continuity.html` and
`/slides/rack-energy.html`. The old UPS, rack-power and 800 V routes redirect to
the corresponding chapter and retain their query and scene fragment.
Existing `course/prototypes` links redirect while preserving the selected slide
and teaching mode. Editable sources remain grouped in the repository; public
URLs are mapped during staging.

## The teaching rhythm

A chapter gives the learner a question, shows the mechanism and works through a
consequence. Show both cases together when the comparison is the lesson. Use a
control to reveal a change in behavior. Close with what the next design decision
needs; a substantive prediction is useful when it tests the mechanism, while a
threshold-check quiz is not required.

The slides carry the main facts and visual reasoning. Explain the rest in your
own words. The [teaching standard](TEACHING_STANDARD.md) records the accumulated
feedback, and the [source index](README.md) identifies the editable inputs.

[TESTING.md](TESTING.md) records which technical and browser checks actually ran.
Passing them establishes behavior and legibility under those checks; rehearsal
establishes whether the sequence teaches clearly.
