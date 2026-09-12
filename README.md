# GIGAWATT

**From watts to racks, useful compute, and operation.**

[Open the course](course/index.html) · [Slides available](course/index.html?view=slides)

The sidebar is the course directory. Chapters use numbered descriptive names,
starting with **1. Primer**, **2. Data center overview** and **3. Workloads and
requirements**. Each chapter shows its reading and available slides. Choose
**Slides available** to see only chapters with teaching material; selected-topic
sequences are labelled so they do not imply a complete chapter deck.

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

The expanded reader contains 50 authored lessons across 15 domains, including
five integrated cases, with teaching and practice mapped to all 65 objectives.
It includes searchable text, a glossary, eight numerical model types and five
original GPT ImageGen equipment illustrations. Exact calculations use code;
illustrative geometry does not establish equipment ratings.

The sidebar reports which chapters have slides and whether they cover the chapter
or selected topics. [COURSE_REVIEW.md](course/COURSE_REVIEW.md#next-teaching-step)
owns the remaining production work, including check-in connections, case and
delivery slides, consistent use of Abilene, and teaching rehearsals.
[TEACHING_STANDARD.md](course/TEACHING_STANDARD.md#required-section-handoffs)
records the cases and exercises each relevant chapter must carry into its teaching
material. Authored coverage and passing builds do not establish comprehension or runtime.

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
The historical 22-lesson introduction is retired from the published course.
Its source remains in the repository; its old page and lesson links redirect to
relevant lessons in the current reader. The map's `baseline_coverage` and
`baseline_lessons` fields refer only to that historical introduction; the manuscript reports
[current authored coverage](course/EXPANDED_COURSE.md#objective-to-lesson-coverage).
Earlier `evidence/` ledgers and `diagram/` engineering maps remain dated research
references. Retired course-design documents and experimental players are in Git
history; their published document paths point to the consolidated guidance.

Saved publisher text is searchable locally in `research/articles/`, with a capture
index at `research/articles/INDEX.md`. The [research workflow](research/README.md)
explains syncing, importing authorized full exports and checking integrity. The
public source notes record review scope separately from article capture.
