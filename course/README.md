# From Watts to Tokens — source index

Start with the [filled-in freeCodeCamp template](COURSE_REVIEW.md) for course
design and production status. This page only identifies editable inputs and
build outputs. [TEACHING_STANDARD.md](TEACHING_STANDARD.md) defines the authoring
contract; [PRESENTING.md](PRESENTING.md) explains the dry-run controls.

[Review questions and answers](REVIEW_QUESTIONS.md) collects the conceptual
clarifications from the September 17–18 walkthroughs in one searchable reference.

[Open the course](index.html).
The sidebar combines reading and teaching material under numbered descriptive
chapters, beginning with **1. Primer**. All 16 numbered chapters and the unnumbered ERCOT and PJM case study have
complete authored slide decks; the review tracker records which the author has accepted.

| Editable input                                                                                                   | Generated reading or teaching output                                                                  | Build command                                         |
| ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `expansion/foundations-power.json`, `racks-compute-heat.json`, `heat-delivery-operations.json`, `capstones.json`, `grid-queues.json` | `index.html`, `expanded-course.json`, `lessons/*.md`, `EXPANDED_COURSE.md`, `expansion-manifest.json` | `uv run gigawatt-expand`                              |
| `expansion/sample.json`                                                                                          | `sample-reading.html`, `SAMPLE.md` (local only; not published)                                         | `uv run gigawatt-expand`                              |
| `expansion/sample-presentation.json`, `web/presentation.*`                                                       | `sample.html`, `teach.html`, `sample-notes.html` (local only; not published); `prototypes/rack-energy-800v-data.js`, which supplies Chapter 9’s 800 V scenes | `uv run gigawatt-expand`                              |
| `web/reader.*`, `web/reader-models.js`, `assets/`                                                                | Reader layout, exact calculations and equipment illustrations                                         | `uv run gigawatt-expand`                              |
| `teaching-sequences.json`, chapter order from `domain-map.json`                                                 | Chapter/deck directory in `index.html` and `expanded-course.json`; shared slide labels in `prototypes/teaching-navigation.js` | `uv run gigawatt-expand`                |
| `domain-map.json`, `web/domain-map.html`; source connections from `research-sources.json`                        | `DOMAIN_MAP.md`, `domain-map.html`                                                                    | `uv run gigawatt-map`                                 |
| `research-sources.json`, `../research/discovery.json`                                                            | Source-note metadata and `../research/INDEX.md`; original note bodies are preserved                   | `uv run gigawatt-research build --include-candidates` |

Edit the inputs and regenerate. Add `--check` to verify freshness without writing.
Published decks load `web/presentation.css`, `web/presentation-renderers.js`,
`web/electrical-renderer.js` and `web/reader-models.js` directly, so edits to them
change recorded slides.
When adding a presentation, register its title, chapter placements, links and
coverage (`chapter` or `selected`) in `teaching-sequences.json`, then regenerate.
The catalog drives slide discovery and shared numbering; it is not a review or
completion tracker. `domain-map.json` also lists `reference_domains`: these retain
their reading and objective IDs but sit outside numbered chapters. The former
Compute deck is retired; its useful slides live within workloads, rack power,
networking and operations. Follow-ups belong in
[COURSE_REVIEW.md](COURSE_REVIEW.md#next-teaching-step), and required case and
exercise handoffs belong in
[TEACHING_STANDARD.md](TEACHING_STANDARD.md#required-section-handoffs).

The authored sequences in `prototypes/` are source files, published at clean
`/slides/…` routes by `src/gigawatt/stage_site.py`: `continuity-format.html`
and its mechanism modules, and `cooling-format.html` with `cooling-model.js`, `cooling-foundations.js`,
`cooling-capture.js`, `cooling-cdu.js` and `cooling-continuity.js`.
Chapter 12 uses `heat-rejection-format.html` and its scene, player, model and visual
modules, reusing the outdoor mechanisms in `cooling-rejection.js`. The final two
decks use the same structure under `capacity-*` and `integrated-cases-*`.
Chapter 15, **GPU cloud economics**, has 19 slides. It opens with the supplied
hardware-price meme, then covers capacity products and customers, rental terms
and prices, occupancy, financing, NVIDIA's backstop agreements, idle electricity
and its pass-through, and Abilene's plan against its reported delivery.
Chapter 16, **Putting an AI Factory Together**, uses ten slides to follow one
Abilene case through the connected facility and commercial decisions. In
`expansion/capstones.json`, the Abilene companion lesson (`c00-abilene-ai-factory`)
opens the chapter's reading and follows the same case. The five original
engineering exercises come after it as optional reading and practice; their
numerical models are separate from the final deck.
Edit those files directly; their numerical tests and browser checks verify the
presentation, while the matching reader lessons retain the longer explanations.
The [Primer](prototypes/terminology-format.html) publishes at `/slides/primer.html?teach=1`.
Edit `prototypes/terminology-format.html` (embedded presentation shell and styles),
`prototypes/terminology-scenes.js` (headlines and accessible descriptions) and
`prototypes/terminology-visuals.js` and `prototypes/terminology-electricity.js`
(diagrams) directly. Its 22 slides target roughly twenty minutes, without per-slide timing cues.
They attach vocabulary to examples so a beginner can follow part of an expert
conversation. Their notes are the [Chapter 1 section](SPEAKER_NOTES.md#source-circuit-and-load--chapter-1-slide-1)
of `SPEAKER_NOTES.md`, and [evidence and assumptions](PRIMER_EVIDENCE.md) are
kept outside the slides.

The following Data center overview sequence is `prototypes/orientation-format.html`, with spatial
diagrams in `orientation-spatial.js`, quantity diagrams in
`orientation-quantities.js` and shared calculations in `orientation-model.js`.
The broad power and compute tours are in `orientation-power-tour.js` and
`orientation-compute-tour.js`.
Its 14 slides remain intact. The workload sequence follows in `prototypes/workload-format.html`,
with authored scenes in `workload-scenes.js`, diagrams in `workload-visuals.js`,
and shared calculations in `workload-model.js`. Its 18 scenes connect a named
GB300 NVL72 and Llama 3.1 70B to training/inference memory, KV-cache capacity,
prefill/decode, continuous batching, complete-run energy and time-resolved power.
A published H100 training trace is distinct from the original timing model.
Conditional staggering remains beside its dependency limitation; the closing
workload brief replaces the old threshold quizzes. The
[chapter review tracker](COURSE_REVIEW.md#chapter-review-tracker) records validation
and author-review status; the unchanged Primer is not assigned another general pass.
Chapter 4 uses `siting-format.html`, `siting-scenes.js`, `siting-visuals.js` and
`siting-generation.js`; Chapter 5 uses `site-format.html`, `site-scenes.js`,
`site-visuals.js` and `site-model.js`. The two decks have 25 and 20 slides.
Shared presentation chrome is in
`prototypes/slide-chrome.js` and `assets/slide-chrome.css`.

Chapter 13 uses `procurement-cases-format.html`, `procurement-cases-scenes.js`,
`procurement-visuals.js`, `procurement-commissioning.js`, `procurement-model.js`,
`procurement-cases-player.js` and the shared `rapid-build-cases.js`. Its 14 slides
separate EPC responsibilities from prefabrication, follow the fixed-20 MW rack
change through its electrical, coolant and support interfaces, then cover factory
and site work, Houdini, the Siemens/Compass skid, Open Compute Project interfaces,
factory acceptance and complete accepted paths. The deck ends on the Polaris
Forge 1 phase boundary: connecting the next 50 MW while the first 50 MW stays
online. Retired fragments resolve through `sceneAliases`; the hardware-price
meme moved to Chapter 15, and its old bookmark opens there through `sceneRedirects`.

Chapter 14 uses `operations-format.html` with `operations-scenes.js`,
`operations-model.js`, `operations-visuals.js`, `operations-comparisons.js`,
`operations-case-stories.js`, `operations-reserve.js`, `operations-player.js` and
their stylesheets. Its 23 slides diagnose a hot row from before/after measurements,
separate pump controls, plant controls and the scheduler, then follow Google's
autonomous cooling and demand response, Cloudflare's Portland outages, Google's
London cooling failure and Meta's Llama 3 recovery. The knowledge check asks
whether a healthy row can take another 2.50 MW. The longer case accounts live in
the D14 reader lessons.

The new GPT visuals are in `assets/generated/`, with prompt JSON alongside them.
The [image-request ledger](COURSE_REVIEW.md#image-request-accounting) records what
was generated and why a few precise comparisons deliberately remain code-rendered.

The manifest reports generated counts and image hashes; the template records
what has actually been reviewed. Source notes and generated lessons each serve
a different reading purpose and do not own course design.

## Retired introduction and research

`lessons.json` and `web/course.*`, `web/diagrams.js`, `web/math.js` own the
historical 22-lesson introduction at `../diagram/index.html`, generated with
`uv run gigawatt-build`. These files are retained as local source and curriculum
history. The historical introduction is excluded from publication.
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
Colossus 1 reuse, the SemiAnalysis equipment-procurement workaround,
Crusoe/Redwood solar and batteries in Sparks, Abilene cooling, and Google's
flexible scheduling. Each retains a case question and worked explanation in its reference. Their
longer treatments live in the relevant reader lessons. Standalone case scenes do
not count as integration into a chapter's teaching material: use the
[required section handoffs](TEACHING_STANDARD.md#required-section-handoffs) when
building each deck, and record its integrated scene there.

`domain-checkins.json` owns the reader's 15 optional check-ins, keyed by chapter:
one closing each of Chapters 2 to 15 (Chapters 8 and 9 use `D06` and `D06-DC`)
and one closing the case study (`grid-queues`). The Primer and Chapter 16 have
none. Each
record names its `chapter` and `next_chapter`. The expanded-course builder
attaches the check-in to that chapter's final lesson, checks that `next_chapter`
is the chapter of the next lesson in course order, and preserves the scenario,
answer and transition in the reader and Markdown.

## Rack-power chapter split

The directory exposes separate [Rack power and buffering](prototypes/rack-energy-format.html?teach=1)
and [800 V DC distribution](prototypes/dc-distribution-format.html?teach=1) decks.
`teaching-sequences.json` partitions domain D06's reading into Chapters 8 and 9
without changing its objective IDs. Later chapter numbers follow automatically.
Each chapter has its own slide selector and canonical URL. Retired URLs and
slide aliases are not published.

## ERCOT and PJM case-study chapter

The unnumbered **Case study — ERCOT and PJM: the race to connect** sits after
Chapter 4 (siting) and before Chapter 5; recorded Chapters 1–16 keep their numbers. Its 11 static slides distinguish
requests, studies, financial commitments, forecasts and actual demand, and end
on the gap that campuses fill with their own generation. Three public
SemiAnalysis figures, PJM's zone map and Dominion's contract chart remain
intact apart from recorded crops; the dense staged-energization figure is
redrawn for the slides and preserved in the reader. Every slide has narration
in `SPEAKER_NOTES.md`.

Edit `prototypes/grid-queues-*`, `expansion/grid-queues.json` and the matching
source records. The catalog’s `additional_chapters` assigns the D03 lesson
`d03-interconnection-queues` to the unnumbered case study after Chapter 4 without
renumbering Chapters 1–16. Chapter 4’s check-in bridges to the case study
(`next_chapter: "grid-queues"`), and the case study’s own check-in bridges to
Chapter 5.
The September 18 Texas rule is identified as adopted, effective October 8; the
queue snapshots retain their own dates. The author's first review on
September 21 is implemented; acceptance of the revised chapter remains pending.
