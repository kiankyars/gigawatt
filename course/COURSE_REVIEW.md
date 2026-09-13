# GIGAWATT — filled-in course review template

Updated **2026-09-12**. **Start here for the course design.** This is the course's
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
A separate [Primer](prototypes/terminology-format.html) introduces
electricity basics and recurring terminology before the core course. Its 21 slides
have a 20-minute target that remains provisional until rehearsal.
The thirteen-scene Data center overview remains intact: it tours generation, transmission, campus power, backup,
GB300 hardware, compute, networks and cooling before introducing load, energy and PUE.
The new [Workloads and requirements presentation](prototypes/workload-format.html) has 19 scenes covering
workload requirements, memory, useful output, batching, latency and job-demand
envelopes. Its examples and controls are implemented, pending an aloud dry run.
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
- **Provisional runtime and why the outcomes need that time:** Aim for at least 300 substantive teaching slides across the 15 domains, with roughly ten hours as a provisional course length. At 300 slides, ten hours averages two minutes per slide, including spoken explanation and demonstrations. This is an authoring target, not a finished storyboard; actual runtime follows dry runs. Keep slides concise and earn length through mechanisms, worked examples and learner practice. Avoid the encyclopedic survey: runtime, topics, articles, and named equipment are not success measures. Merge or cut sections that only add facts without improving the learner's reasoning.
- **Public code, notes, or slides:** The [reader](index.html), [manuscript](EXPANDED_COURSE.md), [domain map](DOMAIN_MAP.md), [teaching sample](teach.html) and [research library](../research/README.md) are the current draft resources. The [source index](README.md) identifies what to edit. The historical 22-lesson introduction is retired from the published course; its source remains in the repository as a baseline. Final chapter timestamps, recorded edition and errata links remain pending.

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
- **Which term, assumption, or step could lose the learner first?** A full campus one-line or unexplained UPS, CDU, PUE or NVLink acronym. The Primer gives first exposure to electricity basics and recurring terminology through visible relationships. Keep the primer self-contained and tie each term to a concrete example. Reintroduce each term when its function becomes useful; Primer requires neither memorization nor mastery before Data center overview.
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
| [Primer](prototypes/terminology-format.html) | Primer before the data center overview; approximately 20-minute target, pending rehearsal | Rehearse pacing and check that first exposure reduces unfamiliarity without implying mastery |
| [Reader and lesson notes](index.html)                     | Drafted explanations, worked examples, tradeoffs, failure cases and changed-scenario answers                           | Complete claim review, learner comprehension checks and final narration              |
| [Five capstones](DOMAIN_MAP.md#proposed-capstones)        | Drafted synthetic briefs and worked solutions; scope belongs to the domain map                                         | Check assumptions and demonstrate transfer across domains                            |
| [Workloads and requirements](prototypes/workload-format.html) | 19 authored scenes covering its three reader lessons, with numerical comparisons and changed cases | Rehearse explanations, timing and transfer; complete technical and learner review |
| [800 V DC presentation](teach.html)                       | Thirteen authored visual scenes, separate notes, student explanations and shared calculations                               | Rehearse the revised copper/space premise and conversion-placement ending                |
| [UPS, bypass and redundancy](prototypes/ups-format.html) | Seventeen visual scenes with optional notes, power-path changes and surviving-capacity exercises; part of Continuity, storage and protection | Dry-run the minimal-text format and report unclear mechanisms or terminology |
| Search, glossary and practice                             | Implemented in the reader                                                                                              | Check findability, first-use vocabulary and learner reasoning                        |
| Numerical models                                          | Eight bounded model types with arithmetic checks                                                                       | Specialist review of physical boundaries and any real-case inputs                    |
| [Illustrations](assets/README.md)                         | Five ImageGen orientation images with preserved prompts; exact engineering labels and calculations rendered separately | Verify final-size legibility and narration                                           |
| [Research library](../research/INDEX.md)                  | Persistent source notes and lesson-specific claims with access/read limits                                             | Resolve unsupported, inaccessible, disputed and date-sensitive claims                |
| Persistent facility artifact, recorded edition and errata | Planned; individual lesson artifacts and source manifests exist                                                        | Connect the course-wide artifact, freeze the video edition and establish corrections |

[TESTING.md](TESTING.md) records the actual scope of build, model and browser
verification. Passing those checks does not establish comprehension, specialist
approval or a successful recording. No complete source-corpus audit is claimed.

**Terminology coverage updated 2026-09-10:**
[Data center overview](index.html#d01-boundaries) now introduces white/grey space;
[Physical site, buildings and safety](index.html#d12-room-and-replacement-route) applies it to equipment placement,
service space and total footprint. [Siting, grid connection and supply](index.html#d03-service-and-siting) explicitly
teaches behind-the-meter location, grid import/export, island capability and
time-to-power constraints. Its original 8 MW load / 6 MW generator case compares
2 MW grid import with 2 MW storage output in an assumed supported island.
These are authored additions within existing objectives, pending learner and
technical review; they do not add domains or standalone lessons.

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

The original Crusoe-built Stargate campus in **Abilene, Texas** is the recurring
real campus reference. Keep the adjacent Microsoft project separate, retain dates
on site claims, and label synthetic calculations as illustrative. Contrasting
cases teach industrial reuse (original Colossus), procurement-driven electrical
choices (SemiAnalysis’s Southaven/MiniHard account), solar and storage
(Crusoe/Redwood in Sparks), and demand flexibility (Google).

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
The **Primer** comes first,
followed by the existing **Data center overview**. Primer introduces names and
basic relationships so a later explanation is not the learner's first encounter.
It is a prelude to the fifteen domains, not a sixteenth required domain, a new
set of assessed objectives, or the historical 22-lesson introduction. The presenter decides how to introduce it; the slides contain no skip prompt.
The fifteen domains organize the material behind the main journey. Keep returning to
one evolving facility drawing and bill of materials so each addition has a place
and a purpose. The companion lets students revisit, explore and practise independently.

Within each section: **pose a problem → show the mechanism → work an example →
change one condition → explain the result**. Ask brief prediction questions during
the explanation. At a domain boundary, use one short scenario that tests the main
idea, invite viewers to pause, then show the reasoning and connect it to the next
problem. For continuity, that might mean removing a UPS for maintenance and then
losing another unit: what can still run, and why?

The reading companion now includes fifteen domain check-ins with answer
reveals and transitions. The case-study companion provides short authored teaching
sequences; later domain slide adaptations should integrate those cases in context.

Use the existing integrated capstones where several systems meet; longer exercises
can be optional companion practice. The video needs no scoring, mandatory quiz
screen or separate examination after every chapter. This rhythm is the production
approach; the 800 V and UPS prototypes are implemented, while the remaining presenter
sequences still need authorship and dry runs.

### Next teaching step

Keep these follow-ups open as each section is authored. The
[section handoff checklist](TEACHING_STANDARD.md#required-section-handoffs) identifies
the case scenes to bring into each presentation; update it with the deck and scene
links when integration is complete.

- [ ] **Domain check-ins:** connect every applicable teaching sequence to its
  authored check-in, with a prediction pause, answer reveal and next-section
  transition. All fifteen exist in the reader; only the overview and workloads
  presentations currently link directly to theirs.
- [ ] **Delivery exercise and case integration:** turn the site-built versus
  prefabricated/modular comparison and the fixed-20 MW rack-density change into
  a teaching sequence. Preserve electrical, hydraulic, spatial and scheduling
  reasoning, with an owner and release evidence for each hold. Integrate the six
  required case treatments listed in the section handoff checklist; standalone
  case slides and reader coverage do not complete this task.
- [ ] **Recurring campus:** audit every lesson and presentation for consistent
  use of the original Crusoe-built Stargate campus in **Abilene, Texas**. Keep
  dated site facts, illustrative examples, the adjacent Microsoft project and
  other case-study sites distinct; record the checked sections before closing.
- [ ] **Primer rehearsal:** teach all twenty-one slides aloud with a beginner,
  record the actual runtime against the approximately 20-minute target, and test
  whether they can follow part of an expert conversation. Revise the specific
  unfamiliar terms or missing reasoning; browser checks do not establish this.

The reviewed UPS and 800 V sequences establish the teaching approach for the
remaining course. Apply their minimal text, explicit boundaries, visible
mechanisms and controlled comparisons to each new section. Their visual format
is a reference, not a requirement to use electrical-style diagrams everywhere.

The next dry run is **[Primer](prototypes/terminology-format.html?teach=1)**.
Check its approximately 20-minute target, whether the diagrams give each term a
meaningful first exposure, and whether beginners can follow part of a technical conversation. Do not test recall as an entry requirement.

**[Data center overview](prototypes/orientation-format.html?teach=1#three-paths)** remains as authored.
Its thirteen scenes give a broad first tour: facility rooms, generation and
transmission, campus distribution and backup, a GB300 rack, chip-to-cluster scale,
network and cooling paths, then rating, demand and fixed-IT PUE comparisons. These concepts
are directly taught in the presentation. Source-claim evaluation remains in the
Data center overview reference. Workloads and requirements now has a 19-scene teaching sequence across its three written
lessons; Siting, grid connection and supply is the next core teaching section to author after the Workloads and requirements dry run.

**Teach the new sequence aloud without recording.** Send the scene and the point
that confused you or needed a different visual. The agent fixes that mechanism
and carries the lesson forward. There is no need to review the two earlier
sequences again before work advances, or read all fifty drafts first. The concise
review playbook and optional references are in [PRESENTING.md](PRESENTING.md).

Repeat this process through the domain map's dependency order. Author each
mechanism and example for its topic; converting the existing prose into slides
will not by itself finish the course. Build the facility drawing and bill of
materials as the lessons need them, keeping the primer and data center overview
consistent with that shared model. The [BTM source note](../research/sources/SA41.md) remains an
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

### Design, procurement and commissioning delivery comparison — 12 September 2026

The scheduling and interface lessons now share one synthetic 20 MW comparison:
site-built services versus factory-built service modules under the same EPC
scope. The late change from 200 × 100 kW to 100 × 200 kW racks drives electrical,
hydraulic, spatial, controls, transport and schedule holds. Each hold identifies
its owner and release evidence. The Design, procurement and commissioning boundary check revisits the same choice;
factory release remains distinct from integrated site acceptance.
