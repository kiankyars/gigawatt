# Present From Watts to Tokens

## Current chapter boundary

The former Chapter 8 is now **8. Rack power and buffering** and
**9. 800 V DC distribution**. Existing recordings and dated notes referring to
the old Chapter 8 cover both. The former standalone Storage and recovery chapter is now folded into Networking
and Operations. Cooling follows Chapter 10 directly; later chapters are numbered
11–16. Use current chapter links from the directory.

Selected narration is in [Speaker notes](SPEAKER_NOTES.md).

## Recording in batches

Kian confirmed Chapters 1–8 verified on **15 September 2026**. The recording plan
is two parts: begin directly with the Primer and continue through Chapter 8,
including the completed buffering follow-up below. Then resume the chapter-by-chapter
refinement loop for the remaining course before recording the second part.
Their acceptance is recorded in the [chapter tracker](COURSE_REVIEW.md#chapter-review-tracker).

Before the first take, make a short capture using the actual microphone and
recording layout: check a dense diagram, one interactive control and the separate
presenter window. Review the result at normal size and a small playback size.
Play a 20–30-second sample of a dense slide on a phone at normal size: the
smallest labels and numbers must remain readable in the recorded video.
Record only the current-slide window; keep the upcoming-slide window off the
captured display. Rehearse the section aloud to catch any missing spoken steps.

Record the spoken course introduction last, once the actual length and full
course content are known. Keep it separate from the Primer. State the audience,
what the learner will be able to explain, the broad journey and the companion
link. Introduce the Primer as first exposure to vocabulary, then begin its circuit
example. The site’s **Glossary** button and search lead back to full explanations;
show one lookup instead of reading the glossary aloud.

For each batch, record the Git revision and actual capture date in the recording
notes. The first preparation baseline is `5d9553a`; this does not claim a recording
has occurred. Preserve the batch’s slide version while later material changes.
Use explicit dates when narrating project milestones and forecasts.

The Chapter 8 buffering follow-up is complete: slide 14 shows a sudden GPU load
drop and the bidirectional buffer absorbing excess source power during ramp-down.
The rising and falling load examples now sit together before the battery hardware
and recharge slides. The [production follow-up](COURSE_REVIEW.md#next-teaching-step)
is closed; this recording content gap is resolved.

## The next pass

Prepare only the section being recorded. The template’s short checks are a
spoken rehearsal, checked claims/examples/workflow, and a readable capture with
clear audio. Complete later chapters, final timestamps and the recorded-edition
publication at their own production stage. The full evolving equipment inventory
is still a planned companion feature; introduce the existing reader, glossary,
slides and examples in the opening.

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
The original window's header and bottom slide navigation hide while the presenter
is connected and return when it closes, without moving the slide content.
The separate upcoming-slide window keeps its bottom navigation controls and a
small header with **Exit presenter**. That button closes the presenter window,
returns focus to the original window and restores its header and navigation
without changing the current slide.

The presenter's small footer controls the original window: its selector names
the current audience slide, while “Up next” gives the number of the slide shown
on the second monitor. Use the presenter controls or the current slide's keyboard
shortcuts to advance both views. In the
presenter window, arrow keys, Page Up / Page Down and Space navigate; Home / End
select the first or last audience slide. Focused controls keep their own keyboard
behavior. At the last slide, the presenter shows “End of chapter” and offers the
next chapter when available. Closing the presenter leaves the audience unchanged;
**Presenter** opens it again. If the browser blocks the popup, allow popups for
this site and click the button again.

Desktop slide margins use 2% of the viewport (16–36 px), with 12 px above the
content. Shared diagram labels are 6% larger; titles retain their authored sizes
so extra wrapping does not shrink the diagrams. Captions inside photographs or
supplied figures retain their original proportions.

Use **Next / →**, **Back / ←**, the short slide selector and diagram controls.
Where a meaningful prediction has a reveal, use its button; the 800 V sequence
also supports **R**. **F** enters fullscreen in decks that support it. A focused
slider uses arrow keys to change its value. The site follows the device’s light
or dark appearance. Press Escape to leave fullscreen.

Clean public routes include `/slides/primer.html`, `/slides/workloads.html`,
`/slides/siting.html`, `/slides/site-design.html`, `/slides/continuity.html` and
`/slides/rack-energy.html` and `/slides/dc-distribution.html`. Use the course
directory or these current URLs; retired URLs and slide aliases have been removed.
Editable sources remain grouped in the repository; public URLs are mapped during
staging.

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
