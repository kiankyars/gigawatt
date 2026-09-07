# Course review

Planning review updated **2026-09-06**, instantiated from the [freeCodeCamp course review template](https://github.com/kiankyars/youtube/blob/main/freecodecamp/course-review-template.md) and its [evidence-based improvement system](https://github.com/kiankyars/youtube/blob/main/freecodecamp/improvement-system.md). The expanded course now has 50 authored lessons, five solved capstones, five ImageGen illustrations and eight interactive model types. This is a draft review, not a completed recording review. All release gates remain open.

## Learner contract

- **Working title:** GIGAWATT — Modern AI Data Centers: From Watts to Racks and Useful Compute.
- **Intended learner:** A technically curious viewer, software or ML practitioner, or infrastructure analyst who wants to reason about how an AI data center works and evaluate architecture claims. The course does not assume prior facilities engineering experience.
- **What they already know:** Arithmetic, percentages, unit conversion, and how to read a simple graph. Explain any additional algebra and introduce electrical, thermal, and computing vocabulary before relying on it.
- **What they do not yet know:** How grid service becomes usable rack power; how heat reaches the environment; how compute, memory, networking, and storage interact; and how commissioning, failures, maintenance, and delivery constraints determine usable service.
- **What is most likely to confuse, overwhelm, or worry them:** Acronyms introduced before equipment functions; shifting between campus, building, rack, board, and chip boundaries; mixing power with energy or nameplate capacity with operation; treating one vendor architecture as universal; and mistaking a roadmap for an installed system. Dense diagrams must reveal one relationship at a time.
- **What they will be able to do by the end:** Trace electrical, thermal, and information paths; calculate illustrative power, current, energy, heat-flow, and capacity limits; compare architecture choices under stated constraints; diagnose a coupled failure or bottleneck; and separate a supported deployment claim from a scenario or forecast. The final assessment must require these capabilities on an unfamiliar scenario.
- **Scope and explicit exclusions:** Modern AI data centers from grid access through useful compute and operation, with the narrative spine of watts to racks and heat back out. Include siting, delivery, economics, and sustainability where they change infrastructure choices. Explain networking and storage far enough to reason about cluster service. Exclude detailed chip fabrication, exhaustive generator technology surveys, investment recommendations, country-by-country permitting instructions, and professional installation, switching, or certification procedures.
- **Supported platforms or architectural scope, source cut-off, and recording date:** Compare generic architectures and explicitly dated product/site cases; do not promise one universal data-center design. The planning date is 2026-09-06. An expanded-course source cut-off and recording date have not been set. Record publication/update and verification dates for each material source before scripting is frozen. The existing interactive course is a browser artifact; confirm its supported browser scope before publishing expanded interactions.
- **Provisional runtime and why the outcomes need that time:** Potentially up to roughly ten hours, subject to the validated curriculum and rehearsal. No duration quota: time is earned by explanation, worked examples, comparisons, and learner practice. Avoid the encyclopedic survey: runtime, topics, articles, and named equipment are not success measures. Merge or cut sections that only add facts without improving the learner's reasoning.
- **Public code, notes, or slides:** The [current 22-lesson curriculum](lessons.json) and [rendered introduction](../diagram/index.html) are the starting material. The [domain map](DOMAIN_MAP.md) and [interactive map](domain-map.html) define the expansion; the [course README](README.md) identifies editable sources. The [companion plan](COMPANION.md) specifies a guided learning path and a searchable reference built around the same visual system. The [research library](../research/README.md) covers evidence from multiple publishers and primary sources. Final video resource links, chapter timestamps, and the errata location must be verified at delivery.

## Novice pass

- **What feels obvious only because I already know it?** That a rack is a collection of computing and support equipment; that electrical distribution, coolant circulation, and data movement are different systems; that increasing a site's rated MW does not automatically add useful computation; and that AC, DC, voltage, current, power, and energy name different quantities or behaviors. Introduce these before presenting detailed architectures.
- **Which term, assumption, or step could lose the learner first?** Starting with a full campus one-line or an acronym such as UPS, CDU, PUE, or NVLink without showing the component's job. Begin with one rack's obligations and a short vocabulary map. Define a term at first use, including the boundary and units where relevant.
- **Does the learner understand why this matters before the details?** Every domain should begin with a concrete question: what prevents this rack or cluster from delivering its intended service, what would changing this component fix, and what would it leave unresolved? Introduce 800 V DC through the current and distribution problem, then compare the interfaces and tradeoffs of the alternatives.
- **What changed after this planning pass?** The proposed scope now extends beyond the existing electrical-and-thermal introduction to useful compute, delivery, and operations. Coverage is organized by learner capabilities and domain interfaces, with article mapping as supporting research. The planned sequence includes cross-domain failure cases and changed-scenario questions. The expanded lessons and visual reader are now authored. A final recording script and learner rehearsal remain pending. Kian’s first sample feedback identified text crowding and an unclear recording workflow. The revised 800 V sample separates visual presentation, speaker notes and reading material; it awaits another review.

## Coverage and evidence

The [full manuscript](EXPANDED_COURSE.md) now maps all 65 objectives to authored
lessons and transfer practice. The [visual reader](index.html) contains 45 domain
lessons plus five integrated capstones. This is authored coverage, not evidence
of learner mastery or external engineering review. The [domain map](DOMAIN_MAP.md)
retains partial/missing labels against the historical 22-lesson introduction.

Every lesson includes explanatory sections, a solved example with assumptions
and intermediate steps, a tradeoff, a failure or limit, a transfer question and
answer, and specific source claims with reading limits. Roughly 51,000 words
provide substantial teaching material; they do not establish a ten-hour runtime.

| Domain | Authored entry lesson | Status |
| --- | --- | --- |
| D01 — System boundaries and quantities | [One rack, three paths](lessons/d01-boundaries.md) | Three lessons drafted; review pending |
| D02 — Workloads and the infrastructure brief | [Design for a job, not a rack count](lessons/d02-workload-brief.md) | Three lessons drafted; review pending |
| D03 — Siting, grid connection and supply | [A contract is not a cable](lessons/d03-power-and-procurement.md) | Three lessons drafted; review pending |
| D12 — Physical site, buildings and safety | [A rack must fit on its worst day](lessons/d12-room-and-replacement-route.md) | Three lessons drafted; review pending |
| D04 — Campus and building power distribution | [Read a power train as a set of jobs](lessons/d04-read-the-power-train.md) | Three lessons drafted; review pending |
| D05 — Continuity, storage and protection | [A battery has two limits before it has a runtime](lessons/d05-storage-power-and-time.md) | Three lessons drafted; review pending |
| D06 — Rack power and the 800 V DC transition | [Follow the watts through the rack](lessons/d06-conversion-ledger.md) | Three lessons drafted; review pending |
| D07 — Compute, memory and the rack | [A rack is a path through several memories](lessons/d07-data-path.md) | Three lessons drafted; review pending |
| D08 — Networking and interconnects | [Count the paths, not just the advertised ports](lessons/d08-topology-budget.md) | Three lessons drafted; review pending |
| D09 — Storage, orchestration and recovery | [Storage is a traffic and state system](lessons/d09-storage-paths.md) | Three lessons drafted; review pending |
| D10 — Chip and rack heat capture | [A cool room can contain an overheating chip](lessons/d10-local-thermal-paths.md) | Three lessons drafted; review pending |
| D11 — Heat rejection, climate and water | [The heat does not disappear at the chiller](lessons/d11-heat-rejection.md) | Three lessons drafted; review pending |
| D13 — Design, procurement and commissioning | [The longest lead time is not the completion date](lessons/d13-delivery-dependencies.md) | Three lessons drafted; review pending |
| D14 — Controls, operations and reliability | [A believable number can describe the wrong thing](lessons/d14-telemetry-and-observability.md) | Three lessons drafted; review pending |
| D15 — Capacity, cost and system decisions | [Find the constraint after reconciling the boundaries](lessons/d15-capacity-ledger.md) | Three lessons drafted; review pending |

The five capstones have supplied synthetic briefs, solved numerical examples,
tradeoffs, failures and changed-scenario answers. Named-site public evidence is
kept separate from those invented inputs. No final recording, external expert
review, demonstrated learner comprehension or complete source-corpus audit is claimed.

**Source policy.** The curriculum is organized by domain. Authored lessons now record checked primary-source passages or accessible excerpts, their specific claims and reading limits. Before recording, review the complete claim set and obtain specialist checks for protection, thermal/control and commissioning assumptions. SemiAnalysis is an important discovery and analytical resource, with explicit attribution at the claim or case it informs; it is not the sole source of truth or the boundary of the research library. Include relevant equipment documentation, standards and open specifications, operator evidence, research, government material, measurements, and other independent analysis. Record what was actually accessible and read, the supported claim, the document version/date, and the check date. Label forecasts, disputed claims, and missing evidence. Acknowledge sources in the video and repository; attribution alone does not establish permission to reuse third-party prose or figures. Prefer original explanations and diagrams, recording any permission needed for reused assets. The [research pipeline](../research/README.md) now discovers public metadata and generates local Markdown notes while preserving original research annotations. It does not collect whole articles. A mapped source is not a claim that its full text has been retrieved or audited.

**Companion commitment.** Implement the [companion plan](COMPANION.md) as two views of the same curriculum: a guided path for learning and fast lookup for returning viewers. Keep the persistent campus/rack model, indexed lesson notes, glossary, bounded calculators, changed-scenario practice, claim-level citations, and versioned errata connected by stable IDs. Freeze the companion edition used in the video while allowing a clearly dated living reference to improve. The reader now implements lesson search, a 137-term glossary, eight numerical model types, answer reveals and source boundaries. The complete versioned video/errata experience remains pending. Add real video timestamps only after the recording is edited.

**Visual teaching model.** Reuse one consistent campus → building → rack → board → chip map, with connected power, heat, and information views. Distinguish coolant circulation from heat transfer, and physical connections from commercial or control relationships. Each visual must answer one question, show relevant units/boundaries/assumptions, and explain what changes under a controlled comparison or failure. Use motion when it conveys a defined behavior, with a clear paused state and an equivalent textual explanation. A visually impressive result still needs readable labels and correct causal relationships.

**Validation available so far.** The [testing record](TESTING.md) distinguishes
the prior introduction review from the expanded reader's model, build and
browser checks. Kian’s initial feedback identified too much text and an unclear
recording workflow. The [sample](sample.html) now uses seven visual steps with
separate presenter notes and a reading companion. Rehearsal and review of this
revised format remain pending; see [REVIEW_HELP.md](REVIEW_HELP.md).
External specialist review, final narration, recording settings and export
legibility remain open.

## Pre-recording gates

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

| Review | Main evidence | Fix this release | Change the next course | New permanent gate |
| --- | --- | --- | --- | --- |
| 24 hours — planned | Inspect comments about prerequisites, first-use vocabulary, missing resources, and phone legibility; examine retention at cited timestamps if available. | Verify and correct consequential technical errors or broken resources; add a dated erratum where needed. No observed issue yet. | Record repeated confusion in the opening/system map. No audience result yet. | Apply the improvement system's severe-issue or corroboration rule; none proposed from nonexistent feedback. |
| 7 days — planned | Group substantive comments by domain and misunderstanding; compare repeated reports with retention and transfer-question responses where available. | Recheck disputed calculations, architecture labels, and time-sensitive deployment claims before correcting them. | Revise explanatory order, pacing, or chapter navigation where evidence supports it. | Record the evidence and scope before adopting a new gate. |
| 30 days — planned | Review unresolved issues, repeated misconceptions, resource use, source drift, and whether learners can reason across domains. | Publish verified corrections and dated reference updates with links to affected chapters. | Decide which depth gaps warrant a new edition or focused supplement; do not treat requests alone as proof of a broken learner contract. | Preserve the learner-first process; avoid adding gates for isolated preferences without corroboration. |

Follow the [improvement system](https://github.com/kiankyars/youtube/blob/main/freecodecamp/improvement-system.md): one evidenced correctness, security, accessibility, or reproducibility failure can justify a permanent gate; taste changes require independent corroboration or matching retention evidence. Keep the evidence separate from the action and state when analytics or learner results are unavailable.
