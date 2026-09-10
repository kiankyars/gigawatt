# GIGAWATT

**From watts to racks, useful compute, and operation.**

[Read the course](course/index.html) · [Explore the 800 V sample](course/sample.html)
· [Teach](course/teach.html) · [Domain atlas](course/domain-map.html)
· [Research library](research/INDEX.md)

## Start with the filled-in template

[COURSE_REVIEW.md](course/COURSE_REVIEW.md) is this course's **filled-in
freeCodeCamp template**. It owns the audience, scope, outcomes, companion design,
production priorities and review gates. Start there when deciding what the
course should become.

The reusable original remains in the YouTube repository:
[course-review-template.md](https://github.com/kiankyars/youtube/blob/main/freecodecamp/course-review-template.md).
The original is a blank format; the filled-in file here holds GIGAWATT's decisions.

| When changing…                                                  | Edit this owner                                                                                |
| --------------------------------------------------------------- | ---------------------------------------------------------------------------------------------- |
| Course promise, scope, companion or production status           | [Filled-in template](course/COURSE_REVIEW.md)                                                  |
| Detailed objectives, prerequisites, sequence or capstone briefs | [domain-map.json](course/domain-map.json)                                                      |
| How lessons, visuals, models and evidence should be authored    | [TEACHING_STANDARD.md](course/TEACHING_STANDARD.md)                                            |
| An explanation, worked example, assessment or presentation beat | [Lesson sources](course/README.md)                                                             |
| Source identity, review scope or domain mapping                 | [research-sources.json](course/research-sources.json); [research workflow](research/README.md) |
| Presenter controls or dry-run procedure                         | [PRESENTING.md](course/PRESENTING.md)                                                          |

The domain map implements the template's scope. Generated Markdown and HTML
are reading views, not additional design authorities. Research notes preserve
evidence; they do not add curriculum requirements. Technical checks live in
[TESTING.md](course/TESTING.md), separately from the template's review decisions.

## Current state

The expanded reader contains 50 authored lessons across 15 domains, including
five integrated cases, with teaching and practice mapped to all 65 objectives.
It includes searchable text, a glossary, eight numerical model types and five
original GPT ImageGen equipment illustrations. Exact calculations use code;
illustrative geometry does not establish equipment ratings.

The ten-step 480 V AC / 800 V DC sample has separate student, teaching and
presenter-note views. It makes copper and conversion placement visible, then
compares current, losses and a changed load. The full-course presentation
adaptation, external engineering review and learner dry runs remain pending.
Authored coverage and passing builds do not establish comprehension or runtime.

**The encyclopedic survey is an anti-pattern:** articles inform evidence and
questions; they do not automatically earn chapters. The template states the
course's scope and the teaching standard defines the depth each lesson needs.

## Build and verify

```sh
uv run gigawatt-expand
uv run gigawatt-research build --include-candidates
uv run gigawatt-map
uv run python -m http.server 8765
```

Open [the local reader](http://localhost:8765/course/index.html). Editable inputs
and their outputs are listed in the [source index](course/README.md).

```sh
uv run gigawatt-build --check
uv run gigawatt-expand --check
uv run gigawatt-map --check
uv run gigawatt-research check --include-candidates
uv run python -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/*.test.mjs
git diff --check
```

GitHub Pages validates and publishes changes to `main` at
[GIGAWATT](https://kiankyars.github.io/gigawatt/).
The [retained 22-lesson introduction](diagram/index.html) and old lesson hashes
remain accessible. The map's `baseline_coverage` and `baseline_lessons` fields
refer only to that historical introduction; the expanded manuscript reports
[current authored coverage](course/EXPANDED_COURSE.md#objective-to-lesson-coverage).
Earlier `evidence/` ledgers and `diagram/` engineering maps remain dated research
references. Retired course-design documents and experimental players are in Git
history; their published document paths point to the consolidated guidance.

Saved publisher text is searchable locally in `research/articles/`, with a capture
index at `research/articles/INDEX.md`. The [research workflow](research/README.md)
explains syncing, importing authorized full exports and checking integrity. The
public source notes record review scope separately from article capture.
