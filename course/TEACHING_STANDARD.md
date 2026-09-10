# Lesson and visual authoring standard

Updated **2026-09-10**. This document owns **how to author and check teaching
material**. The [filled-in course template](COURSE_REVIEW.md) owns audience,
scope, companion commitments and production priorities. The [domain map](domain-map.json)
owns objective IDs, prerequisites and sequence. Rehearsal controls belong in
[PRESENTING.md](PRESENTING.md). Do not create another design brief for a new lesson.

## Author the reasoning task

State the engineering purpose before introducing its equation. Teach and assess
every retained objective. Split or merge lessons around the reasoning task;
there is no three-lessons-per-domain quota, fixed scene count or runtime to fill.
A substantial treatment needs a mechanism, independently calculable example,
consequential tradeoff, failure or limiting case, and changed-scenario practice.
The practice must require applying the reasoning rather than copying a result.

Use original explanatory prose. Explain algebra and specialist terms before using
them. Locate equipment and show its job at first use; a glossary or opening
orientation supplements that introduction. Do not paraphrase articles in sequence
or reproduce third-party prose/figures wholesale.

## Edit authored sources, then generate the reading views

The four lesson inputs in `course/expansion/` are
`foundations-power.json`, `racks-compute-heat.json`,
`heat-delivery-operations.json` and `capstones.json`. Each contains a lesson array
or an object with a `lessons` array. Start from an existing lesson in the relevant
file; preserve useful content when adapting the structure.

Each lesson records:

- Stable `id`, `domain`, `title`, `question`, `summary`, `takeaway` and existing
  domain-map `objectives`. Capstone lessons also declare the map's `capstone_id`;
  coverage follows those IDs rather than a hardcoded number of lessons.
- Ordered `sections` with headings and paragraphs, a worked `example` (or
  `worked_example`) with givens, intermediate steps, result and boundary,
  `tradeoff`, `failure`, and `practice` with a question, answer and reasoning.
- `sources` identifying the checked URL, specific supported claim, `reviewed_on`
  date and reading `limits`. Add the reference to `research-sources.json` before
  citing it; the builder resolves its catalog ID.
- `terms` where useful, with a plain definition that disambiguates the physical
  location or accounting boundary. A `visual` declares the authored treatment.

`uv run gigawatt-expand` generates `expanded-course.json`, the HTML reader,
Markdown lessons and manuscript. Edit the JSON inputs rather than those outputs.
The builder validates structure and objective coverage; it does not establish
technical correctness or learner comprehension. Commands and check details live
in [TESTING.md](TESTING.md).

## Declare the presentation's learning contract

A reading lesson is not a presentation sequence. Each authored presentation
declares six fields in a `learning_contract`:

| Field               | What the author must settle                                                     |
| ------------------- | ------------------------------------------------------------------------------- |
| `driving_question`  | The concrete problem the learner will solve                                     |
| `fixed_boundary`    | System, operating state and quantities held constant; any later boundary change |
| `changed_variable`  | What the controlled comparison changes                                          |
| `primary_payoff`    | Why the mechanism matters to the engineering decision                           |
| `misconception`     | The plausible wrong inference the visual must expose                            |
| `transfer_question` | A changed case to reason through before revealing its answer                    |

Assign each scene a `pedagogical_role`: `problem`, `comparison`, `mechanism`,
`architecture`, `balance`, `counterexample` or `transfer`. Begin with the problem,
teach its mechanism and end with transfer. Intermediate scenes depend on the topic.

Keep the audience headline and caption short. Presenter notes should be a few
short bullet points, usually three to five: the mechanism, essential numbers,
important boundary and takeaway. Use phrases the speaker can glance at and
explain in their own words. Put the action or prediction prompt in the separate
cue; keep complete prose and derivations in the student explanation. Include a
provisional rehearsal duration. Preserve stable scene
IDs and replacement aliases. The builder checks these fields, text budgets and
timing totals. The current renderer is specific to the 800 V sample; another
domain needs an authored visual and appropriate model, not only a new JSON title.

The sample's sources are `course/expansion/sample.json` for full teaching prose
and `course/expansion/sample-presentation.json` for the visual sequence.
`course/web/presentation.*` implements the surfaces; `reader-models.js` supplies
shared numerical functions. Keep assumptions and calculations consistent across
student exploration, teaching mode, presenter notes and the written reference.

## Make the mechanism visible

1. Locate the component in the campus → building → rack → board → chip model.
   Preserve names, symbols and interfaces as the view changes.
2. Show the physical comparison. Count conductors, modules, pipes or paths; make
   occupied and released space visible. Show the mechanism behind a percentage.
3. Freeze the baseline and change one stated condition. Keep units, denominator,
   operating/failure state and decisive assumptions beside the visual.
4. Ask for a prediction before revealing a calculation or path trace. Distinguish
   model inputs, calculated outputs and externally measured claims.
5. Close the relevant power, energy, mass-flow, capacity, time or cost account.
   Reconcile interfaces before summing; announce changes in accounting boundary.
6. Apply the reasoning to a changed case. Update the facility artifact and state
   which conclusions still require an equipment rating or additional evidence.

Use exact, code-rendered diagrams for quantities, connections and failure states.
Generated equipment imagery can provide orientation; it must not invent ratings,
electrical connections or quantitative scales. Distinguish physical flows from
commercial and control relationships, and coolant circulation from heat transfer.
Motion must explain a defined change and remain intelligible when paused.

Keep one active visual prominent. Put speaking prompts and action cues in notes, and
derivations and source limits to the reference. Do not auto-convert paragraphs
into slides. The student view is the default; a deliberate teaching endpoint adds
instructor controls. Those modes are presentation choices, not access control.

## Make assumptions and evidence inspectable

A correct equation can still be an incomplete model. Current arithmetic does
not establish total architecture efficiency; a heat balance does not size a pump;
a capacity ceiling does not predict completed workload. Show omitted mechanisms
near the result. State whether each control is a physical design input, simplifying
assumption or schematic comparison, with units, meaningful ranges and justified
precision. Identify essential missing inputs instead of inventing an answer.

Label synthetic values. Keep product specifications, proposed architectures and
observed operation distinct from stable principles and teaching scenarios.
Source records must state what was actually accessible and read, the claim it
supports and its limits. Record disagreements rather than hiding them in an
average. Follow the course's [evidence policy](COURSE_REVIEW.md#evidence-policy)
and the [research workflow](../research/README.md).

For quantitative changes, verify an independently worked example, relevant limits
and invalid inputs. Check diagrams at teaching size, including narrow layouts,
keyboard operation, text alternatives and paused/reduced-motion states. A color
change alone cannot convey an answer. Preserve an understandable reading route
when interaction is unavailable.

## Update the shared facility artifact

Each addition to the functional bill of materials and service-path map records
component/function, location, quantity and unit, operating load, installed and
surviving capacity where relevant, upstream/downstream interfaces, evidence
status and the lesson responsible for the change. Restate configuration and
assumptions when an exercise changes them. A material comparison keeps design
assumptions beside the quantity; the artifact is not a procurement specification.

For example, the 800 V sample's three equal conductor lengths → two is a local
material comparison. Moving rack conversion to a sidecar or power room changes
placement; complete-path energy gets its own account. None of these steps alone
establishes a facility-wide copper, floor-area or energy reduction.

## Revise from the dry run

Teach without recording first. At a hesitation, capture the scene, exact question,
missing term/mechanism/boundary or unsupported claim, and the proposed revision.
After revising, ask the learner to explain the mechanism and solve the changed
case. Record technical review and learner evidence by their actual scope; browser
checks alone do not prove comprehension. The course template maintains production
status and the adaptation backlog so this standard does not become a second plan.
