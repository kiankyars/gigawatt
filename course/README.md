# Course source index

Start with the [filled-in freeCodeCamp template](COURSE_REVIEW.md) for course
design and production status. This page only identifies editable inputs and
build outputs. [TEACHING_STANDARD.md](TEACHING_STANDARD.md) defines the authoring
contract; [PRESENTING.md](PRESENTING.md) explains the dry-run controls.

[Open the course](index.html) or its [Slides available view](index.html?view=slides).
The sidebar combines reading and teaching material under numbered descriptive
chapters, beginning with **1. Primer**. It identifies chapters with no slides and
marks decks that teach selected topics rather than the whole chapter.

| Editable input                                                                                                   | Generated reading or teaching output                                                                  | Build command                                         |
| ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `expansion/foundations-power.json`, `racks-compute-heat.json`, `heat-delivery-operations.json`, `capstones.json` | `index.html`, `expanded-course.json`, `lessons/*.md`, `EXPANDED_COURSE.md`, `expansion-manifest.json` | `uv run gigawatt-expand`                              |
| `expansion/sample.json`                                                                                          | `sample-reading.html`, `SAMPLE.md`                                                                    | `uv run gigawatt-expand`                              |
| `expansion/sample-presentation.json`, `web/presentation.*`                                                       | `sample.html`, `teach.html`, `sample-notes.html`                                                      | `uv run gigawatt-expand`                              |
| `web/reader.*`, `web/reader-models.js`, `assets/`                                                                | Reader layout, exact calculations and equipment illustrations                                         | `uv run gigawatt-expand`                              |
| `teaching-sequences.json`, chapter order from `domain-map.json`                                                 | Chapter/deck directory in `index.html` and `expanded-course.json`; shared slide labels in `prototypes/teaching-navigation.js` | `uv run gigawatt-expand`                |
| `domain-map.json`, `web/domain-map.html`; source connections from `research-sources.json`                        | `DOMAIN_MAP.md`, `domain-map.html`                                                                    | `uv run gigawatt-map`                                 |
| `research-sources.json`, `../research/discovery.json`                                                            | Source-note metadata and `../research/INDEX.md`; original note bodies are preserved                   | `uv run gigawatt-research build --include-candidates` |

Edit the inputs and regenerate. Add `--check` to verify freshness without writing.
When adding a presentation, register its title, chapter placements, links and
coverage (`chapter` or `selected`) in `teaching-sequences.json`, then regenerate.
The catalog drives slide discovery and shared numbering; it is not a review or
completion tracker. Follow-ups belong in
[COURSE_REVIEW.md](COURSE_REVIEW.md#next-teaching-step), and required case and
exercise handoffs belong in
[TEACHING_STANDARD.md](TEACHING_STANDARD.md#required-section-handoffs).

The authored sequences in `prototypes/` are served directly: `ups-format.html`
and its mechanism modules, and `cooling-format.html` with `cooling-model.js`, `cooling-foundations.js`,
`cooling-rejection.js`, `cooling-cdu.js` and `cooling-continuity.js`.
Edit those files directly; their numerical tests and browser checks verify the
prototype, while the matching reader lessons retain the longer explanations.
The [Primer](prototypes/terminology-format.html) has teaching mode at `prototypes/terminology-format.html?teach=1`.
Edit `prototypes/terminology-format.html` (embedded presentation shell and styles),
`prototypes/terminology-scenes.js` (scene content and explanations) and
`prototypes/terminology-visuals.js` and `prototypes/terminology-electricity.js`
(diagrams) directly. Its 19 slides have 20:05 of planned cues, pending rehearsal.
They attach vocabulary to examples so a beginner can follow part of an expert
conversation. [Evidence and assumptions](PRIMER_EVIDENCE.md) are kept outside the slides.

The following Data center overview sequence is `prototypes/orientation-format.html`, with spatial
diagrams in `orientation-spatial.js`, quantity diagrams in
`orientation-quantities.js` and shared calculations in `orientation-model.js`.
The broad power and compute tours are in `orientation-power-tour.js` and
`orientation-compute-tour.js`.
Its thirteen scenes remain intact. The workload sequence follows in `prototypes/workload-format.html`,
with authored scenes in `workload-scenes.js`, diagrams in `workload-visuals.js`,
and shared calculations in `workload-model.js`. Its 19 scenes teach the workload
brief, memory budgets, useful output, request timing and job-demand envelopes.
The primer and workload sequence are ready for an aloud dry run.
The manifest reports generated counts and image hashes; the template records
what has actually been reviewed. Source notes and generated lessons each serve
a different reading purpose and do not own course design.

## Retired introduction and research

`lessons.json` and `web/course.*`, `web/diagrams.js`, `web/math.js` own the
historical 22-lesson introduction at `../diagram/index.html`, generated with
`uv run gigawatt-build`. These files are retained as local source and curriculum
history. Site staging replaces the published introduction with a redirect to the
current reader and maps its old lesson hashes to relevant current lessons.
It has no active course entry or live deck. Its coverage labels are historical
reuse information, not current teaching status or Primer coverage.

The source ledgers in `../evidence/` and earlier engineering maps in `../diagram/`
are dated references. Inspect and cite underlying evidence when reusing a claim.
[TESTING.md](TESTING.md) records verification procedures and their limits.

## Recurring campus and case studies

Abilene, Texas—the original Crusoe-built Stargate campus—is the recurring real
campus reference. The adjacent Microsoft development is a separate project.
Public facts retain their source dates; illustrative calculations are labelled
as assumptions and do not become Abilene operating measurements.

[Case-study slides](prototypes/case-studies.html?teach=1) teach the land comparison,
original Colossus reuse, the SemiAnalysis equipment-procurement workaround,
Crusoe/Redwood solar and batteries in Sparks, Abilene cooling, and Google's
flexible scheduling. Each includes a prediction and worked explanation. Their
longer treatments live in the relevant reader lessons. Standalone case scenes do
not count as integration into a chapter's teaching material: use the
[required section handoffs](TEACHING_STANDARD.md#required-section-handoffs) when
building each deck, and record its integrated scene there.

`domain-checkins.json` owns one short check-in for each of the fifteen domains.
The expanded-course builder attaches it to that domain's final lesson and
preserves the scenario, answer and transition in the reader and Markdown.
