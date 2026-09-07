# Course source

The [expanded visual reader](index.html) now contains 50 authored lessons and
five integrated cases across all 65 domain objectives. [EXPANDED_COURSE.md](EXPANDED_COURSE.md)
is the full manuscript and coverage index. Editable records live in `expansion/`;
`gigawatt-expand` generates the reader, Markdown lessons, glossary and manifest.
The [800 V sample](sample.html) now provides seven visual steps for screen sharing,
separate presenter notes and a [reading view](sample-reading.html). See the
[recording workflow](PRESENTING.md). The remaining lessons are reading material
pending presentation adaptation; the revised sample awaits further review.

The reader uses `web/reader.html`, `reader.css`, `reader.js`, and
`reader-models.js`, with GPT ImageGen illustrations in `assets/`. The
manifest records image hashes; prompt files record how the assets were made.
Run `uv run gigawatt-expand --check` to check generated freshness.

The expansion is defined by [COURSE_REVIEW.md](COURSE_REVIEW.md), instantiated
from the freeCodeCamp template, and the [domain map](DOMAIN_MAP.md).
[COMPANION.md](COMPANION.md) defines the reference experience, while the
[research library](../research/README.md) retains source notes and discovery results.
The encyclopedic survey is an explicit anti-pattern: coverage requires a taught
capability, a worked example and an application assessment.

`domain-map.json` is the editable map; `research-sources.json` is the curated
source catalog. `uv run gigawatt-map` validates their relationships and generates
`DOMAIN_MAP.md` and the standalone `domain-map.html` atlas. Use `--check` to verify
freshness. Domain-level source links are research leads, not claim-level approval.

`lessons.json` is the current 22-lesson introductory curriculum. It contains the
title, chapter list, and
ordered lessons. Each lesson specifies a stable ID, chapter, visual ID, short
explanation, takeaway, longer notes, and sources. Optional checks include a
question, options, a zero-based answer index, and an explanation.

`web/` contains the HTML template, CSS, native SVG visuals, engineering math,
and navigation code. The visual registry in `diagrams.js` is the authority for
the visual IDs used by lessons. `gigawatt-build` embeds all of these inputs into
`../diagram/index.html`; edit the inputs and regenerate the page.

```sh
uv run gigawatt-build
uv run gigawatt-build --check
```

The core journey is rack requirements, grid delivery, electrical continuity,
silicon, cooling, and whole-system limits. Lessons build one physical model.
Keep examples and questions useful to that journey, with explicit numerical
assumptions and a clear separation between generic principles and dated site
claims.

The source ledgers under `../evidence/` are retained research references. They
do not automatically establish a lesson's correctness or current project state;
inspect and cite the underlying source when reusing a claim.

`TESTING.md` covers release checks and the visual walkthrough. Retired players
and experimental curricula remain available through Git history.
