# From Watts to Tokens — filled-in course review template

Updated **2026-09-12**. **Start here for the course design.** This is the course's
instance of the [freeCodeCamp course review template](https://github.com/kiankyars/youtube/blob/main/freecodecamp/course-review-template.md),
using its [evidence-based improvement system](https://github.com/kiankyars/youtube/blob/main/freecodecamp/improvement-system.md).
The shared template remains in the YouTube repository; this filled-in copy owns
From Watts to Tokens's learner contract, scope, companion commitments, production priorities
and release decisions.

The [domain map](DOMAIN_MAP.md) owns detailed objectives, prerequisites, sequence
and assessments; edit [its JSON source](domain-map.json). The
[teaching standard](TEACHING_STANDARD.md) owns lesson and visual authoring rules.
[PRESENTING.md](PRESENTING.md) explains the rehearsal controls and procedure.
Those documents implement this design rather than establishing separate course scopes.
Use the domain map to look up the section being prepared; there is no need to
read it end to end.

**Current state:** 50 reader lessons map to 65 objective IDs. The course advances
section by section. The Primer, overview, workloads, supply and physical-site
decks are authored; UPS, rack power, 800 V and cooling cover selected later topics.
The table below owns their exact scope and review state. The current revision simplifies Chapter 7’s Tier comparison, adds named availability examples and Fairwater Atlanta, and removes interim labels from the chapter directory. Every deck uses one shared navigation component. Current checks are recorded in [TESTING.md](TESTING.md#tiers-availability-examples-and-directory--2026-09-12). Kian’s review remains separate.

## Latest reliability and directory review — 12 September 2026

This pass covers the four reliability scenes beginning at
[Tier outcomes](prototypes/ups-format.html#tier-topology), plus the shared reader directory.
It does not restart the earlier UPS mechanisms or other chapter reviews.

| Request | Revision |
| --- | --- |
| Explain “not established” and “required outcome”; reduce Tier-slide text | Replace abstract verdicts with named capabilities and a direct maintenance-versus-fault comparison. Tier IV remains the highest of the four infrastructure classes. |
| Clarify why generation appears at Tier I | Show on-site backup generation as a common baseline for Tiers I–IV; higher tiers add resilience requirements. Normal operation of a behind-the-meter plant is a separate choice. |
| Give real three-, four- and five-nines examples | Add publisher examples with their actual service/site/fleet scope and distinguish reported availability from design claims. Do not assign an unverified four-nines rating to Abilene. |
| Find Microsoft's four-nines-at-three-nines-cost example | Microsoft's November 2025 Fairwater Atlanta account identifies the site and its resilient-grid strategy. The capability and cost comparison are Microsoft's claims, not an audited operating record or disclosed cost model. |
| Make the resilience decision concrete | Use the named Fairwater power design to connect a resilience objective to the equipment and cost choice; retain the older phased cloud-facility case in [its source note](../research/sources/P81.md). |
| Remove “Slides available,” “Selected slides,” “Reading” and other interim directory labels | Remove the badges and repeated grouping labels; retain chapter names, destinations and the presenter’s Reading link. |

## Chapter review tracker

This is the single running review status. **Authored** means the material exists;
**checked** refers to recorded technical/build/browser checks;
**feedback addressed** means the requested revisions are implemented;
**accepted** means Kian explicitly finished that chapter’s review. These are separate
facts, not extra approval steps. No whole chapter has explicit final acceptance
recorded yet. Revisit only changed slides or a specific unresolved issue; a new
release does not restart an unchanged chapter’s review.

| Chapter | Authored presentation | Technical checks | Author review / next action |
| --- | --- | --- | --- |
| 1. [Primer](prototypes/terminology-format.html?teach=1) | 21 slides | Latest requested revisions checked; [record](TESTING.md#primer-watts-polarity-and-three-phase-power--2026-09-12) | **Previous feedback addressed; final acceptance unrecorded.** No repeat review assigned. |
| 2. [Data center overview](prototypes/orientation-format.html?teach=1) | 13-slide draft | Prior content pass [checked](TESTING.md#overview-and-workload-review--2026-09-12); shared navigation checked in the current release | **Active review.** Networking, CDU and capacity-title feedback implemented; no general restart. |
| 3. [Workloads and requirements](prototypes/workload-format.html?teach=1) | 18 slides; final visual rebuilt with GPT ImageGen | Previous pass checked; new ending and shared navigation checked in the current release | **Active review.** Revisit the changed final visual, not every resolved slide. |
| 4. [Siting, grid connection and supply](prototypes/siting-format.html?teach=1) | Revised 25-slide draft | Current model, source and native-browser checks recorded in [TESTING.md](TESTING.md#chapters-35-and-root-publication--2026-09-12) | **Feedback addressed.** Review changed generation-to-Southaven ending; preceding cases remain unchanged. |
| 5. [Physical site, buildings and safety](prototypes/site-format.html?teach=1) | Independent agent authored 22-slide draft | Current model, source and native-browser checks recorded in [TESTING.md](TESTING.md#chapters-35-and-root-publication--2026-09-12) | **First author pass pending.** Built from the accumulated teaching rules; no claim of one-shot acceptance. |
| 6. Campus and building power distribution | Reader draft; own deck unbuilt | Reader/build checks only | Presentation not yet assigned for review. |
| 7. [Continuity, storage and protection](prototypes/ups-format.html) | Selected UPS topics, 22 slides | Model/browser checks recorded | **Feedback addressed.** Revised Tier hierarchy, generation baseline, three named availability examples and Fairwater decision; earlier storage/recovery changes remain. **Whole chapter incomplete.** |
| 8. Rack power and the 800 V DC transition | Selected [800 V](teach.html) and [rack-to-chip](prototypes/rack-power-format.html?teach=1) decks | Model/browser checks recorded | 800 V sequence iterated; rack-to-chip addition awaiting review. **Whole chapter incomplete.** |
| 9. Compute, memory and the rack | Reader draft; own deck unbuilt | Reader/build checks only | Presentation not yet assigned for review. |
| 10. Networking and interconnects | Reader draft; own deck unbuilt | Reader/build checks only | Presentation not yet assigned for review. |
| 11. Storage, orchestration and recovery | Reader draft; own deck unbuilt | Reader/build checks only | Presentation not yet assigned for review. |
| 12. [Chip and rack heat capture](prototypes/cooling-format.html?teach=1) | Selected topics in shared cooling deck | Model/browser checks recorded | Cooling sequence iterated; no whole-chapter completion claimed. |
| 13. [Heat rejection, climate and water](prototypes/cooling-format.html?teach=1#rejection) | Selected topics in shared cooling deck | Model/browser checks recorded | Cooling sequence iterated; no whole-chapter completion claimed. |
| 14. Design, procurement and commissioning | Reader draft; own deck unbuilt | Reader/build checks only | Presentation not yet assigned for review. |
| 15. Controls, operations and reliability | Reader draft; own deck unbuilt | Reader/build checks only | Presentation not yet assigned for review. |
| 16. Capacity, cost and system decisions | Reader draft; own deck unbuilt | Reader/build checks only | Presentation not yet assigned for review. |
| 17. Integrated cases | Five reader capstones; final deck unbuilt | Reader/build checks only | Capstone presentation and author review pending. |

Primer completion evidence is the implemented feedback in commits `f3b06f2` and
`e3c5228`, summarized in [the confirmed decisions](FEEDBACK_AUDIT.md) and the
linked test record. This supports “feedback addressed,” not a claim that its
spoken runtime, beginner comprehension or final author acceptance has been observed.

## Current revision: generation, speed and UPS recovery

Review only the changed [Chapter 4 ending](prototypes/siting-format.html?teach=1#dania-cycle) and [Chapter 7 storage/recovery sequence](prototypes/ups-format.html#equipment). Chapter 5 remains ready for its first author pass. Earlier resolved reviews remain closed unless a new issue is identified.

<details>
<summary>Every request from this review and its implemented outcome</summary>

| Request | Implementation |
| --- | --- |
| Identify Dania Beach and 7HA.03 | [Dania Beach](prototypes/siting-format.html?teach=1#dania-cycle) explicitly identifies an FPL utility power station and GE gas-turbine model; actual manufacturer photograph retained. |
| Remove or explain “Other” | Removed the obsolete dispatch renderer containing “Other.” The active Siemens figure names its generation contributions. |
| Give slide 18 a coherent purpose and use GPT ImageGen | [Three meanings of fast](prototypes/siting-format.html?teach=1#generation-flexibility) follows delivery → startup → running output. Actual new GPT ImageGen asset: `assets/generated/generation-timescales.png`; exact prompt and limits saved beside it. |
| Simplify slide 19; define LHV | [Annual cost](prototypes/siting-format.html?teach=1#generation-utilization) shows both curves together. Lower heating value is defined in the reader; unexplained shorthand removed from the visual. |
| Remove awkward comparison/reasoning toggles | Both cost curves and both procurement paths remain visible. No hide/reveal questions in this Chapter 4 revision. |
| Show Southaven plans with direct references | [Original site map](prototypes/siting-format.html?teach=1#southaven-plan) and [process drawing](prototypes/siting-format.html?teach=1#southaven-process), with direct PDF pages 80 and 13. Historical proposed conditions distinguished from September operating status. |
| Show the Google/Anthropic economics and SemiAnalysis payback claim | [Contract fees](prototypes/siting-format.html?teach=1#contract-economics) uses primary filings. $2.17B/month is conditional full-service fees, not profit. Google’s full fees start October 2026. SemiAnalysis’s exact sub-year payback quote is an analyst forecast; 3–5 months is delivery lead time. Actual contract profit and achieved payback are not disclosed. |
| Compare speed with the cost of lower efficiency | [Price the time gained](prototypes/siting-format.html?teach=1#speed-premium) derives $14.6M extra annual fuel for the same illustrative 100 MW. Earlier service must cover that penalty and added build costs. No whole-company contract fees are assigned to this hypothetical plant. |
| Explain the abrupt slide 23 transport comparison | [Campus AC current](prototypes/siting-format.html?teach=1#transport-current) directly follows the transformer procurement choice. Fixed 200 MW transport; no 800 V DC or rack-density change. Separate parallel-circuit arithmetic slide removed. |
| Replace the contrived ending and 8+2 arithmetic | Removed obsolete quiz renderers and reveal states. The ending now compares the delivery decision and carries it into physical site design. Old fragments resolve to relevant replacements. |
| Simplify UPS cabinet description | [Equipment](prototypes/ups-format.html#equipment) shows the verified family rating and dimensions. Family photography does not establish identical internal configurations merely in two colors. |
| Decide whether the generic storage picture earns space | Retained to show the separate external-battery footprint. It is labeled generic and does not imply a product, rating or internal arrangement. |
| Trim normal/outage path labels | Kept equipment functions, path and source state; removed repeated explanatory labels from both diagrams. |
| Motivate capacitance and remove the second ideal-example disclaimer | [Capacitor buffer](prototypes/ups-format.html#capacitors) names capacitance, voltage and cutoff and connects them to the stored-energy equation. Keeps “Ideal DC-bus example.” |
| Demonstrate return to 800 V with battery or generator | New [DC-link recovery](prototypes/ups-format.html#dc-link-recovery) restores the missing 5 kJ using a regulated source’s 100 kW surplus. Recovery time starts when that surplus is available; it is not generator startup time. |
| Add generator supply plus battery charging | [Generator handoff](prototypes/ups-format.html#generator) has four states including generator + recharge. Charging is a configurable supported mode; the “charging omitted” note is removed. |
| Use one reusable navigation component | `slide-navigation.js`, installed by shared `slide-chrome.js`, owns the footer across all decks. Existing chapter state and handlers remain; selector, arrows, count and responsive layout are shared. |
| Remove the misleading full-load PSU caption | Removed it. The reader distinguishes each path’s available rating from actual total draw. Kian’s criticism concerned ambiguous wording, not misunderstanding redundancy. |

The request’s slide numbers were matched by content: the prior published sequence had 23 slides; this revision has 25. No whole-chapter acceptance is inferred from implementation or technical checks.

</details>

## Learner contract

- **Title:** From Watts to Tokens — A visual course on AI data centers. The Python package, command names and GitHub repository slug remain `gigawatt`.
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
| [Workloads and requirements](prototypes/workload-format.html) | Rebuilt 18-scene sequence; current requested edits implemented | Review the revised sequence |
| [800 V DC presentation](teach.html)                       | Thirteen visual scenes with shared calculations; longer explanations and sources stay in the reader                               | Rehearse the revised copper/space premise and conversion-placement ending                |
| [UPS, bypass and redundancy](prototypes/ups-format.html) | 21 visual scenes with power-path changes, surviving-capacity exercises and a separate Tier/availability comparison | Dry-run the minimal-text format and report unclear mechanisms or terminology |
| [Rack inlet to chip](prototypes/rack-power-format.html) | Eleven scenes covering PSU modules, the rear busbar, board regulation, BBUs and storage locality | Dry-run the new mechanisms and repeated-burst prediction |
| [Siting, grid connection and supply](prototypes/siting-format.html) | 23 revised scenes, with phased delivery, four supply configurations and manufacturer turbine/dispatch diagrams | Review after the overview and workloads |
| Search, glossary and practice                             | Implemented in the reader                                                                                              | Check findability, first-use vocabulary and learner reasoning                        |
| Numerical models                                          | Eight bounded model types with arithmetic checks                                                                       | Specialist review of physical boundaries and any real-case inputs                    |
| [Illustrations](assets/README.md)                         | Five existing equipment illustrations plus three new GPT images for the current review; prompts preserved and asset-specific limits recorded | Verify final-size legibility and narration                                           |
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

The reader is published at the site root; presentations use concise `/slides/`
addresses. A teaching route adds fullscreen controls. Every slide header has
**Back to course** and a **Reading** link; explanation/source dialogs and speaker-note
launch buttons are removed from slide views. The reader holds derivations,
terminology, source claims and limitations. Existing links redirect while preserving
their query and slide selection. Editable sources remain grouped by concern in
`course/`; publication paths do not create another editable copy.

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
the explanation. Close with the engineering consequence and a direct connection to the next
chapter. Use a changed scenario only when it advances the reasoning. For continuity,
removing a UPS for maintenance and then losing another unit can reveal a surviving
path; asking whether a displayed number is below a threshold does not earn a slide.

The reading companion now includes fifteen domain check-ins with answer
reveals and transitions. The case-study companion provides short authored teaching
sequences; later domain slide adaptations should integrate those cases in context.

Use the existing integrated capstones where several systems meet; longer exercises
can be optional companion practice. The video needs no scoring, mandatory quiz
screen or separate examination after every chapter. This rhythm is the production
approach; the 800 V and UPS prototypes are implemented, while the remaining presenter
sequences still need authorship and dry runs.

### Next teaching step

#### Current revision — course navigation and Chapters 3–5

Each row records the requested change and its local resolution. **Implemented**
means authored in the working revision; current release validation and final author
acceptance are recorded separately in the chapter tracker.

| Request | Resolution / status |
| --- | --- |
| Rename the course | **From Watts to Tokens** is the public course name. Package, CLI and repository identifiers remain stable. |
| Independent agent starts and finishes Chapter 5 using all accumulated feedback | [Physical site deck](prototypes/site-format.html?teach=1): authored independently around real cases, explicit purpose, minimal text, physical routes and meaningful failures. Current integration checks passed. |
| Remove All chapters / Slides available toggle | Removed. One chapter directory shows reading and available slides. Mobile **Chapters** remains the control that opens that directory. |
| Remove explanation and source UI from all slide views | Shared slide chrome removes those controls and note launchers; **Reading** remains. Current cross-deck integration checks passed. |
| Publish at the root with concise slide URLs | Staging publishes the reader at `/` and decks at `/slides/…`; old `course/prototypes` links redirect with query and hash preserved. Original source ownership remains grouped in `course/`. |
| Replace default-blue underlined chapter check-in links | Chapter actions share designed button styling. Practice stays optional; a useful handoff can replace a quiz. |
| Give Chapter 4 a clear opening purpose | [Opening](prototypes/siting-format.html?teach=1#siting-purpose) establishes delivery date, connections, operating arrangement and generation duty before the cases. |
| Replace trivial readiness arithmetic with CoreWeave phased delivery | [Polaris Forge 1](prototypes/siting-format.html?teach=1#site-ready): Applied Digital reported 50 MW Ready for Service on 27 October 2025, then another 50 MW on 24 November. The contracted campus was 400 MW; the first building was 100 MW. |
| Show a real gas-pipeline connection and locate the Colossus case | [Abilene gas lateral](prototypes/siting-format.html?teach=1#parcel-connections) uses Energy Transfer’s August 2026 update. Original Colossus belongs in [Chapter 5](prototypes/site-format.html?teach=1#colossus-service). No unverified pipe diameter is asserted. |
| Teach BTM generation becoming backup after grid connection | [Bridge to backup](prototypes/siting-format.html?teach=1#bridge-to-backup) uses Crusoe’s stated strategy. Controls, fuel, permitting and supported modes must suit both roles; conversion is not assumed automatic. |
| Replace the four-box grid diagram with a generated spatial visual | [Shared network](prototypes/siting-format.html?teach=1#grid-connection) uses `shared-grid.png`; hypothetical geography explains a common upstream constraint. |
| Motivate the Abilene example and update current status | [Phased campus](prototypes/siting-format.html?teach=1#abilene-phase) follows the release/connection cases. Oracle’s September 2026 statement is separate from the adjacent Microsoft project. |
| Add an Abilene satellite view from September | A publisher aerial dated **15 July 2026** is used with its date visible. No September satellite capture was established; the course does not present this image as one. |
| Refresh March 2026 claims across the repository | Abilene’s active slides, D03 reading and case ledger now use the September Oracle update. Historical events, OCP document revisions and Sparks measurement periods retain their actual dates. The bounded reconciliation and unchanged historical sources are recorded in [TESTING.md](TESTING.md#source-date-reconciliation). |
| Replace the supplied wordy four-configuration image | Original GPT-generated [four-part overview](prototypes/siting-format.html?teach=1#power-configurations) uses grid-supplied, grid-parallel, export-only and off-grid. The supplied image is not reused; source-derived definitions retain their evidence in the reader. |
| Put the configuration overview before four deep dives | The next four slides follow that exact order, with explicit import/local-supply/export/island boundaries. |
| Resolve the unexplained slide 6 and nighttime-battery detour | Old purchase/matching/island fragments are replaced by the configuration sequence. Storage belongs inside the clearly named off-grid discussion, with no invented Crusoe solar scenario. Old slide URLs have aliases. |
| Remove the old trivial slide 12 | The generic fuel-available/fuel-lost toggle is replaced by the actual pipeline-connection case. Generation separately opens with a simple-cycle versus combined-cycle overview and manufacturer diagrams. |
| Clearly introduce simple cycle and CCGT; use manufacturer visuals on the turbine slides | [Generation overview](prototypes/siting-format.html?teach=1#generation-options), [gas turbine](prototypes/siting-format.html?teach=1#gas-shaft) and [CCGT](prototypes/siting-format.html?teach=1#combined-cycle) give the technology a name and purpose. Siemens and GE figures are cited and dominate the relevant slides. |
| Apply the same source-figure approach to dispatch | [Dispatch](prototypes/siting-format.html?teach=1#grid-dispatch) uses Siemens’ illustrative supply profiles; no measured daily forecast is implied. |
| Repair Chapter 3’s final visual and act explicitly on image-generation requests | [Workload handoff](prototypes/workload-format.html?teach=1#next-brief) now uses `workload-handoff.png` with an inspectable schematic power trace. Image requests and the two deliberate code-rendered choices are accounted for below. |

#### Image-request accounting

An image request receives a generated/sourced asset **or a specific recorded
reason for a different visual**. A generic preference against generated diagrams
is not a reason to silently skip a request.

| Request in the course reviews | Action and reason |
| --- | --- |
| Initial request to use GPT ImageGen for teaching visuals across the course | Five existing assets: [campus](assets/campus-cutaway.png), [rack](assets/rack-anatomy.png), [cooling](assets/cooling-cutaway.png), [power](assets/power-equipment.png), [network](assets/network-equipment.png). Their original prompts and asset-specific limits are in [assets](assets/README.md); this does not claim that every remaining chapter is illustrated. |
| Improve AI equipment accuracy and weak flow diagrams | UPS, rack power, 800 V and cooling use checked functional diagrams and named manufacturer views where connections or anatomy matter. Each original generated equipment asset retains its specific allowed role rather than being treated as validated machinery. |
| Optional GPT images for the Chapter 3 training/inference comparison | Kept the two code-rendered panels: the operations and state changes must remain simultaneously legible and inspectable, including the exact distinction between prefill, decode and training updates. This is a local design choice, not a prohibition on generated teaching diagrams. |
| Optional GPT image for same-work energy | Kept the code-scaled comparison table: 80% power × 150% duration = 120% energy must compare directly against the same accepted work. A decorative scene would obscure the scale relationship. |
| GPT image for Chapter 4’s shared-grid slide | Generated [shared-grid.png](assets/generated/shared-grid.png); both campuses visibly depend on the same upstream network. [Prompt](assets/generated/shared-grid-prompt.json). |
| GPT image simplifying the four power configurations | Generated [power-configurations.png](assets/generated/power-configurations.png), with four headings and minimal directional content; the supplied wordy image is not reused. [Prompt record](assets/generated/september-review-prompts.json). |
| Latest request for Chapter 3’s ending and for multiple image requests to be acted on | Generated [workload-handoff.png](assets/generated/workload-handoff.png), plus the two Chapter 4 images above. The power trace and labels remain inspectable overlays. [Prompt record](assets/generated/september-review-prompts.json). |
| Siemens/manufacturer diagrams for simple cycle, CCGT and dispatch | Use actual Siemens/GE diagrams with attribution, as requested; generated reconstructions would lose the named source’s precise mechanism. |
| Real data-hall, GB300 rear busbar, UPS and CoolIT CDU examples | Use manufacturer/operator photographs of the named equipment or site. A generated reconstruction cannot establish its identity or anatomy. |
| User-supplied 800 V architecture, OCP and SST-market figures | Retained as sourced reference figures in their relevant lessons, with provenance and forecast/design limits in [asset records](assets/README.md). |
| Current Abilene satellite/aerial request | Use the dated publisher aerial described above; no AI-generated image is presented as current satellite evidence. |

<details>
<summary>Previous review — Chapters 2 and 3, 12 September 2026</summary>

Each request below has one resolution. The [chapter tracker](#chapter-review-tracker)
records whether the chapter itself is finished; this table tracks the current edits.

| Request | Resolution / status |
| --- | --- |
| Add a Google TPU/OCS/ICI mini-example to overview slide 9 | [Google TPU v4 view](prototypes/orientation-format.html?teach=1#network-preview): actual pod photograph and an original optical-path diagram; 4,096 chips, with multi-data-center networking explicitly distinguished from ICI. |
| Check “cooling” versus “coolant distribution unit” on overview slide 10 | [Cooling preview](prototypes/orientation-format.html?teach=1#cooling-preview) consistently uses **coolant distribution unit**. Sources use both expansions; this is a terminology choice, not a universal correction of manufacturers. |
| Replace the capacity/nameplate/meter title | [Capacity scene](prototypes/orientation-format.html?teach=1#facility-meter): **A 2 MW supply must power the racks and the equipment that supports them.** |
| Replace “64 accelerators” with a named, quantified system | [One GB300 NVL72](prototypes/workload-format.html?teach=1#success-brief): 72 GPUs, Llama 3.1 70B, and a separately chosen token-service target. |
| Add a Chapter 3 introduction explaining the section’s purpose | [New opening](prototypes/workload-format.html?teach=1#workload-purpose): model state → token service → power over time → supply brief. |
| Compare training and inference simultaneously | [Training beside inference](prototypes/workload-format.html?teach=1#model-work); unnecessary mode toggle removed. |
| Improve crude diagrams, including use of generated images when useful | Diagrams rebuilt around simultaneous comparisons and visible dependencies. Actual TPU photography and a published production power trace provide the real examples. |
| Give “Follow the data through the job” an explicit learning outcome | [Stalled training step](prototypes/workload-format.html?teach=1#resource-paths): identify the exchange dependency and the evidence needed to diagnose it. |
| Motivate inference memory and training memory as a comparison | [Same 70B model, two budgets](prototypes/workload-format.html?teach=1#memory-comparison), followed by sourced KV geometry and its context/concurrency consequence. |
| Remove the obvious “each device has its own memory” slide | Removed. [Context capacity](prototypes/workload-format.html?teach=1#context-capacity) now asks how many resident requests fit the stated cache pool. |
| Replace the arbitrary 400 samples/s example | Removed. The opening derives **100 active sessions × 40 output tokens/s = 4,000 output tokens/s**, explicitly a chosen requirement, not measured NVL72 throughput. |
| Fix the obscured waiting-power text and motivate the slide | Replaced by the [training dependency diagram](prototypes/workload-format.html?teach=1#resource-paths) and a separate measured production-power example. |
| Compare energy per result directly instead of toggling cases | [Two complete runs shown together](prototypes/workload-format.html?teach=1#energy-per-result): 80% power × 150% duration = 120% energy for the same accepted token work. |
| Explain whether slide 10 introduces batching, or remove it | The generic batching and queue-threshold sequence is removed; named prefill/decode and continuous-batching mechanisms replace it. |
| Keep continuous batching only with a clear course purpose | [Continuous batching](prototypes/workload-format.html?teach=1#continuous-batching) shows request replacement during decode and connects it to active memory and compute. |
| Connect the job-phase power swings to electrical infrastructure | [Published H100 training trace](prototypes/workload-format.html?teach=1#training-power-evidence) precedes the explicitly hypothetical phase model. Memory traffic is not equated with maximum power. |
| Explain why synchronized load changes matter to power delivery | [Shared supply trace](prototypes/workload-format.html?teach=1#synchronized-jobs) sums coincident loads; [response choices](prototypes/workload-format.html?teach=1#power-response) distinguish scheduling, device control and storage. |
| Retain staggering and the following dependency case, without claiming routine deployment | [Conditional staggering](prototypes/workload-format.html?teach=1#staggering-jobs) retained per the later review; the [next scene](prototypes/workload-format.html?teach=1#independence) shows when coupled workers invalidate the assumption. |
| Prefer the power graph over a mean-only view | [Power over time](prototypes/workload-format.html?teach=1#demand-transition) shows peak and transition speed directly; the mean is supporting context. |
| Remove the old slides 18–19 threshold quizzes | Removed; [the new ending](prototypes/workload-format.html?teach=1#next-brief) carries the defined service and measured power requirements into supply design. |
| Clarify the naming recommendation | Historical recommendation superseded: Kian has now selected **From Watts to Tokens**. |
| Confirm Chapter 1 feedback and keep a chapter-level review tracker | Implemented [above](#chapter-review-tracker). Previous Primer feedback addressed; final acceptance unrecorded. Chapters 2–3 remain under active review. |

</details>

<details>
<summary>Previous implementation ledger — navigation, reliability, rack power and generation</summary>


| Request | Owning section / work | Status |
| --- | --- | --- |
| Make **Back to course** the common header exit in every presentation | Shared presentation template and every standalone deck | Implemented in the shared template and existing decks; a catalog-wide regression check protects the convention |
| Teach the reliability hierarchy and the downtime implied by three/four/five nines | Continuity/reliability; compare Uptime Tiers separately from measured availability | [Four new UPS scenes](prototypes/ups-format.html#tier-topology) and D05 reference; Tier topology is explicitly separate from the downtime calculation |
| Clarify which Tiers require generation, the cost tradeoff and who chooses them | Continuity/reliability | [Generation requirements](prototypes/ups-format.html#tier-generation) and [investment case](prototypes/ups-format.html#tier-investment); Tier I already includes an engine generator; Tier IV is not government-only |
| Clarify **rack supplies** on overview slide 5 | Overview campus power preview | Replaced with **rack power shelves (PSUs)** |
| Identify the rack’s DC busbar voltage and physical location on slide 7 | Overview GB300 anchor | Rear-view control shows NVIDIA's actual annotated figure; nominal **50–51 V DC**, separate from the 800 V hall proposal |
| Teach BBU location, function and sizing; test the one-BBU-per-NVL72 hypothesis | Rack power / continuity cross-reference | [Specific six-module ORv3 BBU shelf](prototypes/rack-power-format.html?teach=1#bbu-shelf) plus D06 reference; no universal one-BBU-per-NVL72 ratio is claimed |
| Teach energy-storage proximity to compute, including fast load changes | Rack power: capacitors, rack batteries and facility storage at explicit boundaries | [Locality](prototypes/rack-power-format.html?teach=1#energy-locality), overlapping source response and repeated-burst/recharge scenes; D06 reference expanded |
| Earlier course-title recommendation | Course title; recommendation without silently renaming the project | Historical naming recommendation superseded by the explicit choice **From Watts to Tokens**. |
| Explain a gas turbine and combined cycle from first principles | Section 4 generation treatment | [Brayton shaft](prototypes/siting-format.html?teach=1#gas-shaft), separate Rankine loop, fuel balance and real Dania Beach plant; D03 reference expanded |
| Explain baseload, intermediate and peak demand, and generator dispatch | Section 4: roles, startup, ramping and the grid supply decision | [Hourly supply stack](prototypes/siting-format.html?teach=1#grid-dispatch) plus the distinction between hot start, running ramp and construction schedule |
| Compare simple cycle and combined cycle economically and operationally | Section 4: efficiency, capital, utilization, construction and delivery constraints | [Fixed-cost/fuel-cost comparison](prototypes/siting-format.html?teach=1#generation-utilization) and changed-duty prediction; numerical costs and crossover explicitly hypothetical |
| Cover and fact-check the complete PSU-to-chip path supplied in the review | Rack power: AC feed, shelf, busbar, board conversion, regulators and die | [Eleven-scene selected D06 sequence](prototypes/rack-power-format.html?teach=1) and expanded D06 reference |
| Distinguish the platform-specific input voltages, intermediate rails, redundancy and ripple behavior | Rack power | Real single-phase ORv3 PSU example, staged DC/DC conversion and finite multiphase ripple; no universal direct-480-V or direct-54-V-to-die claim |
| Split the work into subagents and retain every request | Reliability, rack power and gas-generation agents; root owns navigation and integration | Three independent authoring/source-review assignments completed; requests tracked here |

</details>

Keep these follow-ups open as each section is authored. The
[section handoff checklist](TEACHING_STANDARD.md#required-section-handoffs) identifies
the case scenes to bring into each presentation; update it with the deck and scene
links when integration is complete.

- [ ] **Section endings:** connect every teaching sequence to the next chapter
  through a meaningful consequence, design brief or transfer problem. The fifteen
  reader check-ins remain optional. Workloads now ends with its supply brief and
  a direct Section 4 link; a threshold quiz is not required.
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
- [ ] **Spoken pacing:** establish the Primer’s actual runtime when preparing
  recording. Its previous requested edits are addressed; this reminder does not
  reopen its slide review or block authoring the next chapter.

The reviewed UPS and 800 V sequences establish the teaching approach for the
remaining course. Apply their minimal text, explicit boundaries, visible
mechanisms and controlled comparisons to each new section. Their visual format
is a reference, not a requirement to use electrical-style diagrams everywhere.

The next review is bounded: the changed Chapter 4 ending and Chapter 7 recovery sequence above. Chapter 3’s changed ending and the independently authored [Chapter 5](prototypes/site-format.html?teach=1) remain available for their pending passes. Current technical and visual
checks are recorded in TESTING.md; these changed sections are ready for the next author pass. Do not restart the unchanged Primer, 800 V or cooling passes. For UPS, revisit only the changed storage, generator and recovery scenes; keep their status in the chapter tracker.

Teach the changed material aloud without recording. Send the slide number or URL
and the precise confusion; close that item after the fix, then continue. The
[short playbook](PRESENTING.md#the-next-pass) keeps the next review bounded.

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
