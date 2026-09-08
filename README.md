# GIGAWATT

**From watts to racks, useful compute, and operation.**

[Read the course](course/index.html) · [Explore the 800 V sample](course/sample.html) · [Teach](course/teach.html)
· [Domain atlas](course/domain-map.html) · [Research library](research/INDEX.md)

GIGAWATT is an authored draft of a visual reference course on modern AI data
centers. Its 50 lessons cover 15 connected domains and five integrated cases:
grid interruption, hot-weather capacity, a dense-rack retrofit, a stalled job,
and phased service acceptance. Each lesson includes developed explanations,
a solved example, a tradeoff, a failure or limit, and changed-scenario practice.
All 65 domain objectives have authored teaching and practice mappings.

The reader combines five original GPT ImageGen equipment illustrations with
eight kinds of numerical interaction, searchable lessons, a 140-term glossary,
source reading boundaries, and worked-answer reveals. Exact calculations are
rendered in code; illustrative equipment geometry never establishes a rating
or a buildable design. The [22-lesson introduction](diagram/index.html) remains
available for its compact SVG experiments.

**The encyclopedic survey is an anti-pattern.** Articles inform questions and
evidence; they do not earn chapters automatically. Runtime is determined by
explanation, practice and rehearsal. The roughly 51,000 words in this draft do
not establish a recorded duration, learner comprehension or engineering review.

## Teach, present, and read

The [student sample](course/sample.html) offers visual steps and optional
explanations. The separate [teaching endpoint](course/teach.html) enables presenter
controls and synchronized notes. Kian will teach an unrecorded dry run first to
identify gaps, then refine the explanation before recording. The eight-step
sample now distinguishes a DC voltage comparison from a complete AC/DC loss
budget. [Dry-run workflow](course/PRESENTING.md).

The 50-lesson reader is the study/reference companion. Only the sample currently
has a deliberately authored presentation sequence; the remaining lessons need
that adaptation and rehearsal before recording.

## Run and edit

```sh
uv run gigawatt-expand
uv run gigawatt-research build --include-candidates
uv run gigawatt-map
python3 -m http.server 8765
```

Open [the local reader](http://localhost:8765/course/index.html). Its styles,
lesson data and code are embedded; the five PNG illustrations are local assets.
No account or remote runtime dependency is needed to read or use the models.

- `course/expansion/` contains editable lesson records and the review sample.
- `course/web/reader.*` and `reader-models.js` contain the reader and exact models.
- `course/web/presentation.*` contains the visual sample and separate notes console.
- `course/assets/` contains generated illustrations, their prompts and limits.
- `gigawatt-expand` generates the reader, standalone Markdown lessons, the full
  manuscript, glossary, objective mapping and an edition manifest.
- `course/research-sources.json` owns source identity and domain mappings;
  each authored lesson also records the specific claim and reading boundary.
- `course/domain-map.json` owns the learner capabilities and prerequisite order.
- [COURSE_REVIEW.md](course/COURSE_REVIEW.md) owns the production review.

Generated files are not editing targets. The old `course/lessons.json` and
`course/web/course.*` continue to own the compact introduction, built with
`gigawatt-build`. The domain atlas's partial/missing labels describe that
historical introductory baseline, not the new authored coverage.

## Verify and publish

```sh
uv run gigawatt-build --check
uv run gigawatt-expand --check
uv run gigawatt-map --check
uv run gigawatt-research check --include-candidates
uv run python -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/*.test.mjs
git diff --check
```

[TESTING.md](course/TESTING.md) records browser and model checks, including what
they do not establish. GitHub Pages validates generated artifacts and publishes
the reader, sample, local assets, introduction and reference documents when
`main` changes. Old introductory lesson hashes retain their route.

External engineering review, learner rehearsal, the recorded script and final
video legibility remain pending. The [first sample review](course/REVIEW_HELP.md)
identified text crowding and an unclear recording workflow; the revised format
awaits further review. No expert or learner sign-off is implied.
The public course is [GIGAWATT](https://kiankyars.github.io/gigawatt/).

The research library includes SemiAnalysis and primary references. It stores
original notes, claims and citations, with access limitations recorded; it does
not collect whole copyrighted articles or treat any publisher as final truth.
Earlier ledgers and engineering maps remain in `evidence/` and `diagram/` as
dated references. Retired experimental players remain in Git history.
