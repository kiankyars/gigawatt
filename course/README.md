# Course source index

Start with the [filled-in freeCodeCamp template](COURSE_REVIEW.md) for course
design and production status. This page only identifies editable inputs and
build outputs. [TEACHING_STANDARD.md](TEACHING_STANDARD.md) defines the authoring
contract; [PRESENTING.md](PRESENTING.md) explains the dry-run controls.

| Editable input                                                                                                   | Generated reading or teaching output                                                                  | Build command                                         |
| ---------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `expansion/foundations-power.json`, `racks-compute-heat.json`, `heat-delivery-operations.json`, `capstones.json` | `index.html`, `expanded-course.json`, `lessons/*.md`, `EXPANDED_COURSE.md`, `expansion-manifest.json` | `uv run gigawatt-expand`                              |
| `expansion/sample.json`                                                                                          | `sample-reading.html`, `SAMPLE.md`                                                                    | `uv run gigawatt-expand`                              |
| `expansion/sample-presentation.json`, `web/presentation.*`                                                       | `sample.html`, `teach.html`, `sample-notes.html`                                                      | `uv run gigawatt-expand`                              |
| `web/reader.*`, `web/reader-models.js`, `assets/`                                                                | Reader layout, exact calculations and equipment illustrations                                         | `uv run gigawatt-expand`                              |
| `domain-map.json`, `web/domain-map.html`; source connections from `research-sources.json`                        | `DOMAIN_MAP.md`, `domain-map.html`                                                                    | `uv run gigawatt-map`                                 |
| `research-sources.json`, `../research/discovery.json`                                                            | Source-note metadata and `../research/INDEX.md`; original note bodies are preserved                   | `uv run gigawatt-research build --include-candidates` |

Edit the inputs and regenerate. Add `--check` to verify freshness without writing.
The authored sequences in `prototypes/` are served directly: `ups-format.html`
and its mechanism modules, and `cooling-format.html` with `cooling-model.js`.
Edit those files directly; their numerical tests and browser checks verify the
prototype, while the matching reader lessons retain the longer explanations.
The manifest reports generated counts and image hashes; the template records
what has actually been reviewed. Source notes and generated lessons each serve
a different reading purpose and do not own course design.

## Retained introduction and research

`lessons.json` and `web/course.*`, `web/diagrams.js`, `web/math.js` own the
historical 22-lesson introduction at `../diagram/index.html`, generated with
`uv run gigawatt-build`. Its coverage labels are historical reuse information.
It is not the expanded course's curriculum authority.

The source ledgers in `../evidence/` and earlier engineering maps in `../diagram/`
are dated references. Inspect and cite underlying evidence when reusing a claim.
[TESTING.md](TESTING.md) records verification procedures and their limits.
