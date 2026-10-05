# From Watts to Tokens

**A visual course on AI data centers, from electricity to useful computation.**

[Open the course](https://kiankyars.github.io/gigawatt/)

The homepage opens with a scroll-driven voxel tour of one data center (power, compute, cooling, network and operations, each linked to its course chapters; shared with [kiankyars/datacenter](https://github.com/kiankyars/datacenter), see [`course/home/provenance.json`](course/home/provenance.json)), then introduces the course's 16 chapters and its ERCOT and PJM case study. The reader at
[`read.html`](https://kiankyars.github.io/gigawatt/read.html) contains the searchable
lessons, glossary and interactive labs. Its sidebar is the course directory.
Chapters use numbered descriptive names,
starting with **1. Primer**, **2. Data center overview** and **3. Workloads and
requirements**. Each chapter links its reading and its slide deck.

The homepage lives at the site root. Presentations have short addresses
such as `/slides/primer.html`, `/slides/workloads.html` and `/slides/siting.html`.
Use the course directory or current slide URLs; retired routes and slide aliases are not maintained.

## Start with the filled-in template

[COURSE_REVIEW.md](course/COURSE_REVIEW.md) is this course's **filled-in
freeCodeCamp template**. It owns the audience, scope, outcomes, companion design,
production priorities and review gates. Start there when deciding what the
course should become.

The reusable original remains in the YouTube repository:
[course-review-template.md](https://github.com/kiankyars/youtube/blob/main/freecodecamp/course-review-template.md).
The original is a blank format; the filled-in file here holds this course's decisions.

| When changing…                                                  | Edit this owner                                                                                |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Course promise, scope, companion or production status           | [Filled-in template](course/COURSE_REVIEW.md)                                                  |
| Detailed objectives, prerequisites, sequence or capstone briefs | [domain-map.json](course/domain-map.json)                                                      |
| How lessons, visuals, models and evidence should be authored    | [TEACHING_STANDARD.md](course/TEACHING_STANDARD.md)                                            |
| An explanation, worked example, assessment or presentation beat | [Lesson sources](course/README.md)                                                             |
| Which presentations appear in the course sidebar               | [Teaching catalog](course/teaching-sequences.json)                                             |
| Source identity, review scope or domain mapping                 | [research-sources.json](course/research-sources.json); [research workflow](research/README.md) |
| Presenter controls or dry-run procedure                         | [PRESENTING.md](course/PRESENTING.md)                                                          |

The domain map implements the template's scope. Generated Markdown and HTML
are reading views, not additional design authorities. Research notes preserve
evidence; they do not add curriculum requirements. Technical checks live in
[TESTING.md](course/TESTING.md), separately from the template's review decisions.

## Current state

The course begins with the Primer: about 20 minutes of electricity, equipment,
computing and cooling vocabulary, pending rehearsal. It adds no assessed objective.

All 16 numbered chapters and the ERCOT and PJM case study after Chapter 4 have
slide decks. On 20 September 2026 the author reported that Chapters 1–16 are
recorded. The [chapter review tracker](course/COURSE_REVIEW.md#chapter-review-tracker)
gives each deck's slide count and review status. The final chapter, **Putting an
AI Factory Together**, follows one Abilene case across ten slides to connect the
course's engineering and commercial decisions.

The reader has 52 lessons, with teaching and practice mapped to all 65 objectives.
Forty belong to Chapters 2–15 and the case study, and six are further reading on
compute and storage. Chapter 16 has the other six: the Abilene reading, which
follows the chapter's case, and five optional integrated exercises.
The reader also has search, a glossary of 282 terms, a Primer vocabulary page, 15
check-ins (one closing each of Chapters 2–15 and the case study) and interactive
labs of 41 types in 43 lessons. Nineteen lessons embed 40 sourced photographs and
figures; one generated illustration, the campus cutaway, appears in two lessons. Exact
calculations use code; illustrative geometry does not establish equipment ratings.

[COURSE_REVIEW.md](course/COURSE_REVIEW.md#next-teaching-step) owns the remaining
production work: author review of Chapters 14–16, the case study and the slides
added after acceptance, a tagged recorded edition, and the Abilene consistency audit.
[TEACHING_STANDARD.md](course/TEACHING_STANDARD.md#required-section-handoffs)
records the cases and exercises each relevant chapter must carry into its teaching
material, and its [reader style rules](course/TEACHING_STANDARD.md#reader-style-rules)
set the voice of the reader. Authored coverage and passing builds do not establish
comprehension or runtime.

**The encyclopedic survey is an anti-pattern:** articles inform evidence and
questions; they do not automatically earn chapters. The template states the
course's scope and the teaching standard defines the depth each lesson needs.

## Build and verify

Staging publishes PNG and JPEG images over 300 KB as WebP, so it needs the cwebp
encoder (`brew install webp`, or `sudo apt-get install webp`); Pillow with WebP
support also works.

```sh
uv run gigawatt-expand
uv run gigawatt-research build --include-candidates
uv run gigawatt-map
uv run python -m gigawatt.stage_site
uv run python -m http.server 8878 --directory _site
```

Open [the local homepage](http://localhost:8878/) or
[the local reader](http://localhost:8878/read.html). Editable inputs remain grouped in
`course/`; `src/gigawatt/stage_site.py` publishes `homepage.html` at the root,
`index.html` at `read.html`, and presentation sources under `slides/`.
This keeps source ownership separate from
public URLs without maintaining duplicate editable decks. The [source index](course/README.md)
lists each input and its generated outputs.

```sh
uv run gigawatt-build --check
uv run gigawatt-expand --check
uv run gigawatt-map --check
uv run gigawatt-research check --include-candidates
uv run python -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/*.test.mjs
uv run python qa/reader/prose_lint.py --gate slide_refs,residue
git diff --check
```

The Playwright scripts in `tests/browser_*.cjs` default to the staged site on
port 8878, so with the server above running they need no arguments. The
separate Browser checks workflow runs them on each push to `main` without
blocking publication.

GitHub Pages validates and publishes changes to `main` at
[From Watts to Tokens](https://kiankyars.github.io/gigawatt/).
The historical 22-lesson introduction is retired from the published course.
Its source remains in the repository, without publishing its old page or lesson routes. The map's `baseline_coverage` and
`baseline_lessons` fields refer only to that historical introduction; the manuscript reports
[current authored coverage](course/EXPANDED_COURSE.md#objective-to-lesson-coverage).
Earlier `evidence/` ledgers and `diagram/` engineering maps remain dated research
references. Retired course-design documents and experimental players are in Git
history; current guidance is linked from the source index.

Saved publisher text is searchable locally in `research/articles/`, with a capture
index at `research/articles/INDEX.md`. The [research workflow](research/README.md)
explains syncing, importing authorized full exports and checking integrity. The
public source notes record review scope separately from article capture.
