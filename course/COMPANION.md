# GIGAWATT companion

Product and editorial plan, **2026-09-06**. The existing introduction and curriculum map are starting artifacts. The domain atlas and public-metadata research pipeline are implemented starting pieces. This document specifies the learner companion to build; its glossary/search, practice, and edition management remain planned.

## What the companion should do

Help someone understand an AI data center well enough to reason about it, then help them recover that reasoning when a real question arises. The video supplies an explanation with a deliberate sequence. The companion lets the viewer inspect the system, work through a calculation, challenge an assumption, and find the evidence without scrubbing hours of footage.

The course must not become an encyclopedic survey. More hours, topic names, source articles, diagrams, or glossary entries do not establish depth. A substantial section earns its place through a mechanism, worked example, consequential tradeoff, failure or limiting case, and a question that transfers the reasoning. If material only names another product or repeats a fact, merge it into the reference notes or remove it.

The [domain map](DOMAIN_MAP.md) currently organizes 65 objectives into 15 domains and five capstones. Those counts describe the plan, not its quality or completion. Use the objective IDs to connect lessons, examples, sources, and checks, while allowing the learning sequence to cross domains.

## Two ways to use one body of material

| Mode | The learner's question | Intended experience |
| --- | --- | --- |
| **Learn** | “How does this system work, and why is it designed this way?” | Follow the watts-to-racks and heat-out journey, with useful compute as the service being enabled. See the current component on the same system map, learn its mechanism, predict a change, work an example, and apply it before moving on. Prerequisite links explain gaps without creating a maze of optional detours. |
| **Look up** | “What does this term mean, where is this interface, or which assumption changes this result?” | Enter through a term, domain, question, equation, case, or source. Find a concise answer, a labeled visual, the applicable boundary, an example, and links to deeper teaching and evidence. Show prerequisites and date-sensitive limits without making the returning viewer repeat the entire course. |

Both modes use the same explanations and numerical models. Do not maintain a shorter, divergent truth for the video and a conflicting truth in the reference. The learning route controls sequence and progressive disclosure; lookup controls entry and navigation.

## A persistent visual system

Keep one coherent campus → building → rack → board → chip model visible across the course. A small locator shows where the current explanation belongs. Let the learner reveal the electrical, thermal, and information paths separately, then combine them when the question requires it. Shared components and interfaces retain their names, colors, units, and geometry as the view changes.

Use that continuity to make dependencies visible. A denser rack changes more than a number on a label: inspect the electrical interface, conversion stages, cooling duty, and service-access constraints in the same model. An outage follows the surviving power paths and the separately supplied cooling auxiliaries. A congested fabric changes delivered work even when electricity and cooling remain available.

Show one causal comparison at a time. Highlight what changed, what assumptions were held fixed, and which quantities are still unknown. Illustrative geometry is not an as-built site model. Flow arrows distinguish electricity, coolant circulation, heat transfer, and information; commercial agreements and control signals need a different convention. Animation must convey a defined change and remain understandable when paused.

## The reference objects

| Object | What it should contain | How it supports learning |
| --- | --- | --- |
| **Indexed lesson notes** | The driving question, explanation of the mechanism, system location, prerequisites, worked example, tradeoff, failure/limit, takeaway, practice, and sources. Use stable lesson/objective IDs and concise summaries with deeper detail available below. | Reconstruct the argument without relying on a transcript or a long list of disconnected facts. |
| **Glossary and interface index** | Plain-language meaning, first-use lesson, physical location or accounting boundary, units where relevant, and a link to the explanatory visual. Disambiguate overloaded terms such as capacity, efficiency, or redundancy. | Recover a missing prerequisite immediately and distinguish terms that look interchangeable. |
| **Calculators and comparisons** | A small number of teaching models with named inputs, units, assumptions, valid ranges, boundary definitions, equations, and worked defaults. Show the consequence of a controlled change. | Practice reasoning about current, energy, heat flow, and binding constraints without pretending to be a facility design tool. |
| **Changed-scenario practice** | Ask for a prediction before revealing the model result. Give feedback about the mechanism and common wrong reasoning, followed by a changed condition that cannot be answered by copying the worked example. | Test transfer rather than recognition or terminology recall. |
| **Cross-domain capstones** | A complete synthetic brief, an evidence/assumption sheet, an annotated model, intermediate calculations, a worked answer, and unresolved quantities. Connect the five cases in the domain map to their prerequisite lessons. | Integrate electrical, thermal, workload, delivery, and operational reasoning. |
| **Citations and source notes** | The specific claim supported, original author/publisher and URL, publication/version date, date checked, actual access/read status, and important caveats or conflicting evidence. | Let viewers examine why a statement is trusted and where it stops applying. |
| **Corrections and edition history** | A dated correction, affected lesson/objective and recorded chapter when known, previous versus corrected meaning, supporting evidence, and impact on calculations or conclusions. | Keep a recorded explanation usable when a mistake is found or a product/site fact changes. |

Do not make every lesson repeat a large boilerplate form. The elements above are editorial requirements, presented only where they help the learner. A concise definition can link to the complete worked treatment; a calculator should link to the lesson explaining its model.

## Five integrated cases

Use the case briefs and assessments in the [domain map data](domain-map.json) as the authority for their scope:

1. **C01 — Grid interruption with a thermal dependency:** distinguish IT electrical support from continued cooling and controls; do not invent an unsupported thermal ride-through time.
2. **C02 — Hot weather under a fixed site power limit:** account separately for cooling performance and auxiliary electricity, then identify the binding constraint.
3. **C03 — A denser rack in an existing building:** compare specified power architectures, retained interfaces, cooling, floor/service access, and migration constraints.
4. **C04 — A powered cluster that misses its job target:** use workload evidence to distinguish fabric and storage limitations from insufficient compute.
5. **C05 — Open one phase of a campus:** trace complete accepted service paths and keep missing named-site operating evidence unknown.

These are planned exercises. Supplied numerical inputs, independent solutions, visuals, and learner checks must exist before a case is presented as validated. One evolving hypothetical facility can provide continuity, but each exercise must restate its actual configuration and assumptions rather than silently inheriting them.

## Evidence and model limits

Use the [research library](../research/README.md) to pursue questions across primary documentation, open specifications and standards, operator disclosures, academic or government work, measured results, and independent industry analysis. SemiAnalysis is a valuable contributor to this library, not its boundary or final authority. An original equipment manual can support a product interface; a vendor roadmap supports what was proposed at that date; neither alone proves a campus's installed configuration or operating performance.

Keep stable principles, hypothetical teaching scenarios, product specifications, proposed architectures, and observed deployments visibly distinct. When sources disagree, state the disagreement and its scope; do not hide it behind a single confident average. A listed URL is a research lead until its relevant contents have actually been checked. Label partial access and missing full text. The implemented pipeline discovers public sitemap/feed metadata and creates persistent Markdown source notes. It does not download article bodies or establish exhaustive relevance. Educational purpose alone does not authorize whole-article reproduction; use original teaching and citations, with full documents or third-party assets included only where their rights permit.

A correct equation can still form an incomplete model. Current arithmetic does not establish total architecture efficiency; a heat balance does not size a pump; a capacity ceiling does not predict workload output. Put the omitted mechanisms near the result. State whether a control is a real design input, a simplifying assumption, or a schematic comparison. Use justified precision and meaningful ranges. If an essential input is missing, identify what is needed instead of manufacturing a numerical answer. Testing must cover known examples, limiting behavior, and relevant invalid inputs; expert or learner validation must be labeled by its actual scope.

## The recorded edition and the living reference

At delivery, assign a release tag to the exact notes, diagrams, calculations, and source snapshot used by the finished video. Preserve that edition with a prominent link to its corrections. The living reference can then improve, with dates and change notes, while keeping the recorded explanation reproducible and its limitations visible.

Stable lesson and objective links should survive edits. A moved lesson gets a redirect or explicit replacement link. A substantial changed conclusion receives an erratum tied to the affected material; do not silently rewrite a reference in a way that makes the recording seem to say something else. Add video chapter timestamps only after editing and verify them against the final export. Until then, label video links as pending rather than inventing times.

## Readable and usable on a phone

Design dense diagrams for the actual teaching size. Use progressive disclosure, alternative compact compositions, and readable labels instead of shrinking a campus schematic until it fits. Keep the active teaching visual prominent, and test the final recording sample and export at 480p and 720p on a phone.

For the web companion, verify keyboard navigation, visible focus, labeled controls, text alternatives, contrast, zoom, narrow layouts, and reduced motion. A color change alone cannot carry an answer. Long equations and tables need an intelligible compact presentation. Preserve a useful reading path when interaction is unavailable; source links should not require recreating the interactive state to understand the claim.

## Starting artifacts and work still required

| Artifact | Current role | Required before claiming the expanded companion is ready |
| --- | --- | --- |
| [22-lesson curriculum](lessons.json), [existing player](../diagram/index.html), and numerical models | Introductory electrical/thermal foundation with existing interactions and source notes. Prior checks are recorded in [TESTING.md](TESTING.md) for their stated version. | Expand the missing objectives, review reused content, add application assessments, and verify the revised teaching and rendered output. |
| [Domain map data](domain-map.json), [Markdown map](DOMAIN_MAP.md), and [interactive map](domain-map.html) | Planning and navigation for 15 domains, 65 objectives, and five cases; source mappings identify leads. | Reconcile objective coverage with authored lessons and demonstrated capabilities. A planning map alone is not the learning companion. |
| [Research source inventory](research-sources.json), [Markdown library](../research/INDEX.md), and [pipeline](../research/README.md) | Curated source notes plus a persistent public-metadata discovery inventory across source types. | Continue relevance triage, inspect accessible material, link exact claims, and preserve dates, disagreements and limitations. Indexed candidates are not reviewed evidence. |
| Search/glossary, expanded notes, practice, case solutions, and edition/errata views | **Planned.** This document specifies their behavior. | Author, implement, connect, and check them with representative learning and lookup tasks. |
| [Course review](COURSE_REVIEW.md) | The learner contract and open pre-recording, delivery, and post-release checks. | Record actual checks and evidence. Do not close gates because a feature has been specified or code has built successfully. |

The first useful prototype should connect one complete lesson to its locator, notes, glossary terms, bounded example, transfer question, and sources. Test whether a learner can explain the mechanism and whether a returning viewer can find the relevant assumption without replaying the video. Use that evidence to refine the common design before reproducing it across the course. Completion means that the promised capabilities are taught and usable, not that every possible data-center fact has been collected.
