# Expanded lesson source

Each author owns one JSON file containing a `lessons` array and an optional
`sources` array for additional primary references. The first integration adapts
minor schema differences rather than discarding authored content.

Each lesson should have a stable `id`, `domain` (D01–D15), `title`, `question`,
`objectives` (existing objective IDs), `summary`, and `sections`: an ordered list
of `{heading, paragraphs}` with original explanatory prose. Include an explicit
worked example (`{title, givens, steps, result, boundary}`), tradeoff and failure
or limiting case, and transfer practice (`{question, answer, explanation}`).
Provide a `takeaway`, `source_ids`, and glossary terms where useful.

The generator normalizes source authoring into `course/expanded-course.json`,
readable Markdown lessons and an accessible HTML reader. This is an authored
draft, not a claim of external expert review, a tested recording, or a fixed
ten-hour runtime. Explain algebra and specialist terminology before using them.

Teach and assess every retained domain objective. Split or merge lessons around
the reasoning task; the current three-per-domain grouping is not a quota.
An example must be independently calculable; a failure must change
a stated condition; practice must apply the reasoning to a new case. Original
synthetic values must be labeled as such. No article-by-article paraphrase and
no wholesale reproduction of third-party prose or figures.

## Presentation authoring

A reading lesson is not a presentation sequence. `sample-presentation.json`
owns ten deliberately authored beats for the 800 V sample. Each beat has a
short audience headline/caption and separate speaker notes, action cue and
rehearsal timing target. Each also has a student explanation.
Student view is the default; teaching mode is explicitly selected by endpoint. Essential units and model assumptions remain visible.
Do not auto-generate slides from paragraphs or put the narration on screen.
The sample uses the same tested AC/DC arithmetic as the reader. Declare the
six-field `learning_contract` and each scene's `pedagogical_role` described in
[TEACHING_STANDARD.md](../TEACHING_STANDARD.md). Start with an engineering problem,
make the primary benefit visible, and finish with changed-case transfer. See
[PRESENTING.md](../PRESENTING.md) for the dry-run workflow.
