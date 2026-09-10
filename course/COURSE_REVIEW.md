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

**Current state:** 50 authored draft lessons cover 65 objective IDs. The ten-scene
800 V DC sample is the only complete presentation prototype. Technical review,
learner review, adaptation of the remaining material, recording and delivery
remain pending. No release gate below is complete.

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
- **What changed after reviewing from the learner's starting point?** The electrical-and-thermal introduction expanded to useful compute, delivery and operations, organized by capabilities rather than source articles. Kian's sample feedback exposed excessive text, an unclear presentation workflow, a misleading power-flow arrow, missing rack-unit vocabulary, and confusion between copper, current and total energy. The revised sample addresses these issues with separate student/teacher endpoints and distinct material, placement and energy comparisons. Its next dry run must establish whether those explanations work.

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
| [800 V DC presentation](teach.html)                       | Ten authored visual scenes, separate notes, student explanations and shared calculations                               | Rehearse the revised copper/space premise and final capacity question                |
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

### Production priorities and presentation backlog

Kian will **teach without recording first** to expose knowledge gaps and improve
flow. The [rehearsal guide](PRESENTING.md) contains the operating instructions and
questions to test. The sample's fifteen-minute allowance is provisional, not a
measured runtime or a target to fill.

1. Rehearse the revised 800 V sample: conductor copper, equipment placement,
   current, complete energy balance and the changed-load capacity limit.
2. Resolve D05's documented redundancy gaps. The
   [coverage audit](../research/redundancy-coverage-review.md) calls for N, N+1,
   N+2, 2N and 2(N+1), UPS normal/battery/bypass paths, single-corded interfaces,
   and maintenance plus a fault. Test surviving capacity and path independence
   before treating that capability as reviewed.
3. Use the [new BTM deep-dive source note](../research/sources/SA41.md) to deepen
   the existing D03/D05/D12/D13/D15 treatments: connection arrangements, fuel and
   project delivery, island operating behavior and the later transition to grid
   service. The current import/island budget is an introduction, not complete
   coverage of BTM execution. Verify consequential claims with primary sources
   and add changed-case assessments before calling that coverage complete.
4. Build the opening orientation and persistent facility artifact. Introduce
   equipment and terms at first use; connect behind-the-meter and physical-space
   teaching to the relevant boundaries.
5. Adapt the remaining material in dependency order, revising lesson divisions
   around the reasoning task. Kian's familiarity with generation or campus
   distribution can accelerate preparation; it does not establish teaching quality.

The table below is a **planned presentation backlog**, not another set of
curriculum objectives. The domain map owns detailed objectives and sequence.
Each proposed visual still needs authorship and a dry run; merge or replace these
treatments where rehearsal supports a better explanation.

| Domain                         | Presentation treatment to develop                                                 | Changed case / facility-artifact update                              |
| ------------------------------ | --------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| D01 Quantities and boundaries  | Trace one rack's inputs, useful service and losses                                | Move the measurement boundary; reconcile kW and kWh                  |
| D02 Workload brief             | Turn workload demand into continuous and transient requirements                   | Change duty cycle; update the load brief                             |
| D03 Grid and supply            | Show energization dependencies, meter boundary and grid-connected/islanded supply | Delay a dependency or lose grid supply; revise usable capacity/date  |
| D04 Distribution               | Trace voltage, current and capacity along a power path                            | Change feeder demand; update distribution interfaces                 |
| D05 Continuity                 | Trace UPS states and distinguish spare modules from independent routes            | Maintenance plus a fault; update surviving capacity                  |
| D06 Rack power                 | Count copper, locate conversion and close the energy account                      | Double rack demand; identify the unverified capacity limit           |
| D07 Compute and memory         | Follow a workload through memory and compute limits                               | Change arithmetic intensity; locate the limiting resource            |
| D08 Networks                   | Show ports, links and traffic on one topology                                     | Remove a link or change traffic; update usable throughput            |
| D09 Storage and recovery       | Follow a write, checkpoint and restart                                            | Lose a component; distinguish stored, durable and recoverable state  |
| D10 Heat capture               | Trace chip → cold plate → fluid, including residual air heat                      | Increase rack duty; update cooling interfaces                        |
| D11 Heat rejection             | Close the outdoor heat account at stated ambient conditions                       | Change weather or water availability; update the operating envelope  |
| D12 Physical site              | Overlay equipment, white/grey space, access and service routes                    | Replace the largest component; test clearances and dependencies      |
| D13 Delivery and commissioning | Trace the critical path and accepted service paths                                | Delay an unaccepted subsystem; revise usable capacity                |
| D14 Operations                 | Trace measurements, controls, failure and restoration                             | Introduce misleading telemetry or maintenance; revise service status |
| D15 System decisions           | Combine electrical, cooling and accepted-path constraints                         | Move the binding constraint; update capacity and cost                |
| Integrated capstones           | Reuse the accumulated facility model                                              | Solve unfamiliar coupled cases without new unexplained concepts      |

## Pre-recording gates

Check a gate only after recording what passed, when and where its evidence is.
Planned work stays unchecked; an inapplicable subcase gets an explicit reason.

- [ ] I reviewed every expanded section from the learner's starting point, using the domain map to identify hidden prerequisites and unexplained jumps; the final script records the resulting changes.
- [ ] The opening states the intended learner, arithmetic/graph prerequisites, achievable outcomes, scope limits, and a short system map before detailed architecture.
- [ ] Essential vocabulary is introduced before it carries explanatory weight; the glossary and first-use order are checked against the complete script.
- [ ] For any software or setup workflow, the complete workflow passes from a fresh environment with supported browsers/platforms/versions stated. Building and operating the course interactions must be checked; learner account setup is currently not part of the course, so account-specific steps are N/A unless a demo adds them.
- [ ] For any added software/setup demo, accounts, costs, permissions, security consequences, limitations, and likely drift are explained before setup. Current account/installation requirements are N/A because the planned learner experience is viewing the course and browser-based examples; revisit this if the scope changes.
- [ ] Material technical claims, calculations, architecture comparisons, source links, and recommendations are verified against appropriate primary evidence, with source and check dates recorded and forecasts/disagreements labeled.
- [ ] Every promised capability has a worked example and a changed-scenario question; the map's remaining coverage gaps are resolved or explicitly excluded from the learner contract.
- [ ] Each substantial section earns its place through a mechanism, worked example, tradeoff, failure or limiting case, and transfer question. The script follows connected problems rather than an article-by-article or component-by-component survey; cut repetitions and runtime padding.
- [ ] Quantitative and visual models pass independent example and limiting-case checks for units, boundaries, assumptions, and failures; diagrams remain correct and explanatory when paused.
- [ ] A dense five-minute section is rehearsed with an intended learner who can explain what happened, why it matters, and what comes next. Start with the electrical architecture comparison or coupled outage case. If no reviewer is available, document a deliberate novice pass and its limitations.
- [ ] Technical review addresses the highest-risk cross-domain claims, especially electrical protection/continuity, cooling operating envelopes, and the useful-compute model; record reviewer scope or the independent evidence used, without claiming unperformed expert validation.
- [ ] A 60-second sample of the densest final diagrams passes phone viewing at 480p and 720p using the final capture settings. The visual fills the frame, labels need no zoom, and narration explains mechanisms rather than reading text.

## Pre-delivery gates

- [ ] Review the first and last two minutes, every cut within a calculation, and transitions between diagrams or applications for bloopers, skipped reasoning, stale labels, and unexplained terms.
- [ ] The final export passes the phone-legibility test, including the densest comparison and system diagram; captions and narration preserve important units and vocabulary.
- [ ] The description and pinned comment link durable course notes, the navigable domain map, chapter timestamps, prerequisites, source/version dates, limitations, acknowledgments, and an errata location; verify every public link.
- [ ] The companion's learning and lookup routes work on a phone, connect lessons to their practice and evidence, and identify the recorded edition versus subsequent corrections. Search, calculators, and source availability are described only to the extent actually implemented and checked.
- [ ] The final course delivers the integrated worked case and a changed-scenario assessment, with a complete explanation of the answer and its assumptions.
- [ ] Course visuals, source notes, and the public artifact match the recorded version; use the applicable checks in [TESTING.md](TESTING.md) and inspect changed content after deployment. A passed build alone does not close the teaching or recording gates.

## Post-release review

Review comments and retention at 24 hours, 7 days, and 30 days after the expanded video is published. Publication and review dates are not yet scheduled. The table records planned reviews, not audience evidence already collected.

| Review             | Main evidence                                                                                                                                            | Fix this release                                                                                                                | Change the next course                                                                                                                  | New permanent gate                                                                                          |
| ------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| 24 hours — planned | Inspect comments about prerequisites, first-use vocabulary, missing resources, and phone legibility; examine retention at cited timestamps if available. | Verify and correct consequential technical errors or broken resources; add a dated erratum where needed. No observed issue yet. | Record repeated confusion in the opening/system map. No audience result yet.                                                            | Apply the improvement system's severe-issue or corroboration rule; none proposed from nonexistent feedback. |
| 7 days — planned   | Group substantive comments by domain and misunderstanding; compare repeated reports with retention and transfer-question responses where available.      | Recheck disputed calculations, architecture labels, and time-sensitive deployment claims before correcting them.                | Revise explanatory order, pacing, or chapter navigation where evidence supports it.                                                     | Record the evidence and scope before adopting a new gate.                                                   |
| 30 days — planned  | Review unresolved issues, repeated misconceptions, resource use, source drift, and whether learners can reason across domains.                           | Publish verified corrections and dated reference updates with links to affected chapters.                                       | Decide which depth gaps warrant a new edition or focused supplement; do not treat requests alone as proof of a broken learner contract. | Preserve the learner-first process; avoid adding gates for isolated preferences without corroboration.      |

Follow the [improvement system](https://github.com/kiankyars/youtube/blob/main/freecodecamp/improvement-system.md): one evidenced correctness, security, accessibility, or reproducibility failure can justify a permanent gate; taste changes require independent corroboration or matching retention evidence. Keep the evidence separate from the action and state when analytics or learner results are unavailable.
