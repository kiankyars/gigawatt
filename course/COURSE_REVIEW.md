# GIGAWATT — filled-in course review template

Updated **2026-09-10**. **Start here for the course design.** This is the course's
instance of the [freeCodeCamp course review template](https://github.com/kiankyars/youtube/blob/main/freecodecamp/course-review-template.md),
using its [evidence-based improvement system](https://github.com/kiankyars/youtube/blob/main/freecodecamp/improvement-system.md).
The shared template remains in the YouTube repository; this filled-in copy owns
GIGAWATT's learner contract, scope, companion commitments, production priorities
and release decisions.

The [domain map](DOMAIN_MAP.md) owns detailed objectives, prerequisites, sequence
and assessments; edit [its JSON source](domain-map.json). The
[teaching standard](TEACHING_STANDARD.md) owns lesson and visual authoring rules.
[PRESENTING.md](PRESENTING.md) explains the rehearsal controls and procedure.
Those documents implement this design rather than establishing separate course scopes.
Use the domain map to look up the section being prepared; there is no need to
read it end to end.

**Current state:** 50 authored draft lessons cover 65 objective IDs. The thirteen-scene
800 V DC sample and seventeen-scene UPS sequence are implemented teaching prototypes.
A fourteen-scene cooling presentation extends that approach to capture methods,
CDU ratings and approach, weather and outdoor heat rejection.
An eight-scene opening section now teaches selected D01 foundations: facility paths,
measurement boundaries, power and energy, and metrics versus useful work.
These cover selected parts of the curriculum; they do not establish finished domains.
Technical review, learner review, adaptation of the remaining material, recording
and delivery remain pending. Prepare and rehearse one section at a time.

## Learner contract

- **Working title:** GIGAWATT — Modern AI Data Centers: From Watts to Racks and Useful Compute.
- **Intended learner:** A technically curious viewer, software or ML practitioner, or infrastructure analyst who wants to reason about how an AI data center works and evaluate architecture claims. The course does not assume prior facilities engineering experience.
- **What they already know:** Arithmetic, percentages, unit conversion, and how to read a simple graph. Explain any additional algebra and introduce electrical, thermal, and computing vocabulary before relying on it.
- **What they do not yet know:** How grid service becomes usable rack power; how heat reaches the environment; how compute, memory, networking, and storage interact; and how commissioning, failures, maintenance, and delivery constraints determine usable service.
- **What is most likely to confuse, overwhelm, or worry them:** Acronyms introduced before equipment functions; shifting between campus, building, rack, board, and chip boundaries; mixing power with energy or nameplate capacity with operation; treating one vendor architecture as universal; and mistaking a roadmap for an installed system. Dense diagrams must reveal one relationship at a time.
- **What they will be able to do by the end:** Trace electrical, thermal, and information paths; calculate illustrative power, current, energy, heat-flow, and capacity limits; compare architecture choices under stated constraints; diagnose a coupled failure or bottleneck; and separate a supported deployment claim from a scenario or forecast. The final assessment must require these capabilities on an unfamiliar scenario.
- **Scope and explicit exclusions:** Modern AI data centers from grid access through useful compute and operation, with the narrative spine of watts to racks and heat back out. Include siting, delivery, economics, and sustainability where they change infrastructure choices. Explain networking and storage far enough to reason about cluster service. Exclude detailed chip fabrication, exhaustive generator technology surveys, investment recommendations, country-by-country permitting instructions, and professional installation, switching, or certification procedures.
- **Supported platforms or architectural scope, source cut-off, and recording date:** Compare generic architectures and explicitly dated product/site cases; do not promise one universal data-center design. The historical domain baseline began on 2026-09-06. An expanded-course source cut-off and recording date have not been set. Record publication/update and verification dates for each material source before scripting is frozen. Confirm the companion’s supported browser scope before delivery.
- **Provisional runtime and why the outcomes need that time:** Potentially up to roughly ten hours, subject to the validated curriculum and rehearsal. No duration quota: time is earned by explanation, worked examples, comparisons, and learner practice. Avoid the encyclopedic survey: runtime, topics, articles, and named equipment are not success measures. Merge or cut sections that only add facts without improving the learner's reasoning.
- **Public code, notes, or slides:** The [reader](index.html), [manuscript](EXPANDED_COURSE.md), [domain map](DOMAIN_MAP.md), [teaching sample](teach.html) and [research library](../research/README.md) are the current draft resources. The [source index](README.md) identifies what to edit. The [22-lesson introduction](../diagram/index.html) is retained as a historical baseline. Final chapter timestamps, recorded edition and errata links remain pending.

**Explicit anti-pattern: an encyclopedic survey of articles or components.**
The course follows engineering questions and dependencies. More hours, articles,
acronyms or named equipment do not establish comprehensiveness. Merge or cut
material that adds facts without improving the learner's ability to explain,
calculate, compare or diagnose the facility. The video must not become a narration
of the reference library.

### Scope boundaries

Use these boundaries when deciding whether new material belongs in the course.
The domain map decomposes the included scope; a source discovery does not change it.

| Excluded depth                                                                      | Bring a mechanism back when…                                                                                                                      |
| ----------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| Full semiconductor fabrication and device physics                                   | It explains a compute, packaging, electrical or thermal interface. CHIPS owns fabrication depth.                                                  |
| Professional electrical, structural, fire or mechanical design and field procedures | Learners need to recognize a design question, safety interface or requirement for specialist review.                                              |
| A complete generation-technology or electricity-market survey                       | Supply, fuel, connection, dispatch or commercial structure changes data-center deliverability or operation. Behind-the-meter supply belongs here. |
| Supplier rankings, investment recommendations and exhaustive company histories      | A dated case explains an architecture, delivery constraint or measurable tradeoff.                                                                |
| Full GPU programming, model-training and cloud-administration tutorials             | A bounded workload mechanism or experiment explains infrastructure behavior.                                                                      |
| Every enterprise, edge and telecom facility variant                                 | A conventional or retrofit contrast changes an assumption in the central AI-facility model.                                                       |

## Novice pass

- **What feels obvious only because I already know it?** A rack contains computing and support equipment; electrical distribution, coolant circulation and data movement are different systems; more rated MW does not automatically mean more useful computation. AC, DC, voltage, current, power and energy describe different quantities or behaviors.
- **Which term, assumption, or step could lose the learner first?** A full campus one-line or unexplained UPS, CDU, PUE or NVLink acronym. Begin with one rack's obligations and a short system map. Introduce each term when its function becomes useful. An optional opening orientation and skippable references help, but a twenty-minute vocabulary list cannot carry the teaching burden.
- **Does the learner understand why this matters before the details?** Begin with a constraint on useful service and show what a proposed change fixes. For 800 V DC, make conductor copper and conversion-equipment placement visible before calculating current and energy. Do not let an illustrative efficiency result replace the architecture question.
- **What changed after reviewing from the learner's starting point?** The electrical-and-thermal introduction expanded to useful compute, delivery and operations, organized by capabilities rather than source articles. Kian's sample feedback exposed excessive text, an unclear presentation workflow, a misleading power-flow arrow, missing rack-unit vocabulary, and confusion between copper, current and total energy. The revised sample addresses these issues with separate student/teacher endpoints and distinct material, placement and energy comparisons. The latest review removed competing bottom subtitles, clarified the UPS battery and product form factor, simplified the electrical primer, and replaced assumed AC/DC conversion losses with a single explicit efficiency example. Its next dry run should test these revisions.

## Coverage and evidence

The [full manuscript](EXPANDED_COURSE.md) maps all 65 objectives to 45 domain
lessons and five integrated capstones. This establishes **authored coverage**.
The domain map's partial/missing labels describe the **historical 22-lesson
introduction**; they are not a review grade for the expanded manuscript.
The map provides the detailed objectives, assessments and historical lesson
relationships. Current authored lesson-to-objective mappings are generated in
[EXPANDED_COURSE.md](EXPANDED_COURSE.md); do not maintain another curriculum outline here.

| Artifact or capability evidence                           | Current state                                                                                                          | Work before release                                                                  |
| --------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| [Reader and lesson notes](index.html)                     | Drafted explanations, worked examples, tradeoffs, failure cases and changed-scenario answers                           | Complete claim review, learner comprehension checks and final narration              |
| [Five capstones](DOMAIN_MAP.md#proposed-capstones)        | Drafted synthetic briefs and worked solutions; scope belongs to the domain map                                         | Check assumptions and demonstrate transfer across domains                            |
| [800 V DC presentation](teach.html)                       | Twelve authored visual scenes, separate notes, student explanations and shared calculations                               | Rehearse the revised copper/space premise and conversion-placement ending                |
| [UPS, bypass and redundancy](prototypes/ups-format.html) | Sixteen visual scenes with optional notes, power-path changes and surviving-capacity exercises; part of D05 | Dry-run the minimal-text format and report unclear mechanisms or terminology |
| Search, glossary and practice                             | Implemented in the reader                                                                                              | Check findability, first-use vocabulary and learner reasoning                        |
| Numerical models                                          | Eight bounded model types with arithmetic checks                                                                       | Specialist review of physical boundaries and any real-case inputs                    |
| [Illustrations](assets/README.md)                         | Five ImageGen orientation images with preserved prompts; exact engineering labels and calculations rendered separately | Verify final-size legibility and narration                                           |
| [Research library](../research/INDEX.md)                  | Persistent source notes and lesson-specific claims with access/read limits                                             | Resolve unsupported, inaccessible, disputed and date-sensitive claims                |
| Persistent facility artifact, recorded edition and errata | Planned; individual lesson artifacts and source manifests exist                                                        | Connect the course-wide artifact, freeze the video edition and establish corrections |

[TESTING.md](TESTING.md) records the actual scope of build, model and browser
verification. Passing those checks does not establish comprehension, specialist
approval or a successful recording. No complete source-corpus audit is claimed.

**Terminology coverage updated 2026-09-10:**
[D01](index.html#d01-boundaries) now introduces white/grey space;
[D12](index.html#d12-room-and-replacement-route) applies it to equipment placement,
service space and total footprint. [D03](index.html#d03-service-and-siting) explicitly
teaches behind-the-meter location, grid import/export, island capability and
time-to-power constraints. Its original 8 MW load / 6 MW generator case compares
2 MW grid import with 2 MW storage output in an assumed supported island.
These are authored additions within existing objectives, pending learner and
technical review; they do not add domains or standalone lessons.

### Evidence policy

SemiAnalysis is an important discovery and analytical resource, with attribution
at the claim or case it informs. It does not define the scope of the curriculum
or serve as its sole source of truth. Use appropriate primary documentation,
open specifications and standards, operator disclosures, government and academic
work, measurements and independent analysis. Separate stable principles,
synthetic teaching inputs, product specifications, proposals, forecasts and
observed deployments. A vendor roadmap supports what was proposed at that date;
it does not establish a campus's installed configuration or performance.

Record the relevant material actually read, supported claim, version/date,
verification date and limits in the research library and lesson source records.
State disagreements and unknowns. A listed URL or generated note is not evidence
that its full text was read. The public library preserves original research notes
and citations. A separate local Markdown archive retains article text under the
publisher permission reported by Kian on 2026-09-10. It labels public previews and
accepts authorized full exports without promoting capture to technical review.
Use original explanations and diagrams in the course; the article archive is
excluded from the public site. The [research workflow](../research/README.md) owns
ingestion commands and capture-state definitions.

### Companion experience

The companion must help a first-time learner inspect the explanation and a
returning viewer recover the reasoning behind a decision. It has two routes
through the same content:

- **Learn:** follow the watts-to-racks and heat-out sequence, locate the current
  component, predict a change, work an example and apply it. Prerequisite links
  fill a gap without turning the course into a maze of optional detours.
- **Look up:** enter through a term, domain, question, equation, case or source;
  find a concise answer, relevant boundary, visual and worked treatment without
  repeating the entire course.

Student exploration is the default public visual experience. A deliberate
teaching endpoint adds instructor controls and separate presenter notes. The
written reference holds derivations, terminology, source claims and limitations.
All three use the same explanations and numerical models. The sample implements
these surfaces; the full course does not yet have authored presentation sequences.

One persistent campus → building → rack → board → chip model should connect
electrical, thermal and information views. A locator should preserve context
while the active visual answers one question. Keep shared names, symbols and
interfaces consistent. Geometry is illustrative unless supported as an actual
site model; electricity, heat transfer, coolant circulation, data, controls and
commercial relationships require distinguishable conventions.

Build one evolving **functional bill of materials and service-path map** through
the course. It should show what each component does, where it sits, its quantity,
interfaces and relevant installed, operating and surviving capacity. Changes in
lessons update this artifact under stated assumptions. It is an educational
inventory rather than a purchasing specification. A local copper reduction must
not silently become a facility-wide material saving. The persistent interface
remains to be built; the authoring fields belong in the teaching standard.

Indexed lesson notes, a glossary/interface index, bounded calculators,
prediction-and-transfer practice, source notes and integrated cases should link
through stable lesson/objective IDs. Glossary entries need an explanatory
location and first-use lesson, not only an expanded acronym. Calculators must
expose their limits. The five capstone briefs and assessments belong to the
domain map; each exercise must restate its configuration rather than silently
inherit all assumptions from the evolving facility.

At delivery, tag the exact notes, diagrams, models and source snapshot used in the
video. Preserve that recorded edition beside a dated living reference. Corrections
identify the affected lesson/objective and recorded chapter, previous and revised
meaning, evidence and any change in conclusions. Stable links need redirects or
explicit replacements when material moves. Add real timestamps after editing.

The reference must remain useful on a phone and when an interaction is unavailable.
Verify keyboard navigation, visible focus, labeled controls, text alternatives,
contrast, zoom and reduced motion. Avoid encoding meaning in color alone. Test the
densest final recording visuals at 480p and 720p; shrinking a campus schematic
until it fits is not sufficient.

### How the video flows

Teach one linear journey through the [six acts](DOMAIN_MAP.md#proposed-teaching-sequence).
The fifteen domains organize the material behind that journey. Keep returning to
one evolving facility drawing and bill of materials so each addition has a place
and a purpose. The companion lets students revisit, explore and practise independently.

Within each section: **pose a problem → show the mechanism → work an example →
change one condition → explain the result**. Ask brief prediction questions during
the explanation. At a domain boundary, use one short scenario that tests the main
idea, invite viewers to pause, then show the reasoning and connect it to the next
problem. For continuity, that might mean removing a UPS for maintenance and then
losing another unit: what can still run, and why?

Use the existing integrated capstones where several systems meet; longer exercises
can be optional companion practice. The video needs no scoring, mandatory quiz
screen or separate examination after every chapter. This rhythm is the production
approach; the 800 V and UPS prototypes are implemented, while the remaining presenter
sequences still need authorship and dry runs.

### Next teaching step

The reviewed UPS and 800 V sequences establish the teaching approach for the
remaining course. Apply their minimal text, explicit boundaries, visible
mechanisms and controlled comparisons to each new section. Their visual format
is a reference, not a requirement to use electrical-style diagrams everywhere.

The current review is **[D01 — Inside the facility](prototypes/orientation-format.html?teach=1#three-paths)**.
Its eight scenes apply the approach reviewed in UPS, 800 V and cooling: a shared
facility map, white/grey space, rack and facility accounts, heat, energy versus
peak demand, hidden peaks and a PUE/useful-work counterexample. These concepts
are directly taught in the presentation. Source-claim evaluation remains in the
D01 reference; D02's workload brief is the next teaching section to author.

**Teach the new sequence aloud without recording.** Send the scene and the point
that confused you or needed a different visual. The agent fixes that mechanism
and carries the lesson forward. There is no need to review the two earlier
sequences again before work advances, or read all fifty drafts first. The concise
review playbook and optional references are in [PRESENTING.md](PRESENTING.md).

Repeat this process through the domain map's dependency order. Author each
mechanism and example for its topic; converting the existing prose into slides
will not by itself finish the course. Build the facility drawing and bill of
materials as the lessons need them, then assemble the opening orientation from
that shared model. The [BTM source note](../research/sources/SA41.md) remains an
input for deeper supply, island operation, fuel, delivery and grid-transition
teaching within the existing domains. Neither the entire source library nor the
whole presentation must be finished before the next dry run.

## Before recording

- [ ] Teach the section aloud without recording; fix confusing terms and skipped reasoning.
- [ ] Check its technical claims, worked examples and any demonstrated workflow.
- [ ] Check a short capture for readable visuals and clear audio.

## Before delivery

- [ ] Watch the edited video and fix mistakes or missing steps.
- [ ] Check chapter timestamps and public resources; ensure they match the video.
