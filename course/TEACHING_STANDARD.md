# Lesson and visual authoring standard

Updated **2026-09-12**. The [course template](COURSE_REVIEW.md) owns audience,
scope and production priorities. The [domain map](domain-map.json) owns objectives,
prerequisites and sequence. This file owns teaching rules; [PRESENTING.md](PRESENTING.md)
owns the rehearsal playbook and controls. Do not create another design brief for
an individual lesson.

## Carry the reasoning across the course

The reviewed UPS, 800 V and cooling sequences establish an approach:
**pose a concrete problem → show the mechanism → change one condition → explain
the consequence**. Select the visual and example that make the particular topic
understandable. The course template records the working goal of at least 300
substantive slides. Individual chapters have no fixed slide count or
three-lessons-per-domain quota; a chapter can span parts of several domains.

Retain material that helps the learner explain, calculate, compare or diagnose
the facility. Cut article-by-article narration, equipment inventories without a
purpose and arithmetic that does not affect the engineering decision. A longer
reference is useful; narrating it does not produce a better lesson.

The [Primer](prototypes/terminology-format.html) aims for about 20 minutes,
subject to rehearsal. It gives a beginner enough vocabulary to follow part of an
expert conversation: electricity, equipment, computing and cooling, attached to
visible objects and concrete examples. Use simple English. Do not label it optional,
include a skip link, refer to other chapters or quote promises about future teaching.
The presenter decides how to introduce it. Keep rehearsal cues, exact per-slide
timings and the Explanation panel out of the primer; preserve supporting detail
in its author notes. Provide a visible Back to course exit throughout the deck.
The primer adds no assessed objective;
teach each concept in context when it becomes useful in the main course.
Keep the N+1 definition and spare-module example; omit the sentence promising a
later surviving-service test. Keep source discussion in the reader. Essential figure attribution may sit beside
a sourced image; it is not an explanation/source popup.

Use numbered descriptive chapter names in the website and presentations, beginning
with **1. Primer**. Stable internal IDs remain for source mapping and existing
links, but are not audience-facing labels.

The public title is **From Watts to Tokens**. The reader is at the site root and
presentations use `/slides/…` addresses. Every slide header has **Back to course**
and **Reading**; no explanation/source dialog or note launcher. Deeper text and
source discussion belong in the reader. Chapter actions use the shared button
style; the directory has no All chapters / Slides available filter.

Every teaching presentation and student exploration view has a visible
**← Back to course** link at the left of its header. It returns to the main
course directory at the site root. A logo or a lesson-specific reading link does not replace
that exit. Keep it available in fullscreen and at narrow widths.

Data center overview remains a broad orientation: preview the equipment, locations and paths
that later sections explain in depth. Briefly naming generation, transmission,
backup, compute, networking and cooling is useful here; each preview needs a
visible role in the same facility journey. Save detailed comparisons for the
section where the learner has the prerequisites.

### Abilene and the recurring case studies

Use the original Crusoe-built Stargate campus in **Abilene, Texas** as the recurring
real facility, just as a named hardware platform anchored the earlier course.
Keep that campus distinct from the adjacent Microsoft development and from
Crusoe/Redwood's solar-and-battery deployment in Sparks, Nevada. Introduce the
reference in the companion and return to it as each physical system is taught.

Carry the same facility through these questions:

| Domains | Return to the campus to ask |
| --- | --- |
| Data center overview through Workloads and requirements | Which boundary and useful service are we describing? Preserve the existing Data center overview slides. |
| Siting, grid connection and supply through Rack power and the 800 V DC transition | Which supply is available, which equipment can be delivered, and where are storage and conversion? |
| Compute, memory and the rack through Storage, orchestration and recovery | What compute, memory, network and storage inputs would establish accepted work? |
| Chip and rack heat capture through Heat rejection, climate and water | How is heat captured, moved and rejected; which water circuit is being counted? |
| Physical site, buildings and safety through Controls, operations and reliability | What must be built, accepted, maintained and recovered for that service to run? |
| Capacity, cost and system decisions | Which dated capacity, output and cost claims can actually enter the ledger? |

Use published Abilene facts only where the source supports the exact building,
date and condition. Otherwise label the mechanism or calculation **illustrative**;
retain stable names and interfaces, and leave unknown as-built quantities unknown.
A reference campus does not require inventing its full one-line or GPU inventory.

Teach contrasting cases within their relevant systems: original Colossus for
brownfield reuse; SemiAnalysis's Southaven/MiniHard procurement account for
speed versus electrical efficiency; Sparks for solar, battery energy and backup;
Abilene for non-evaporative rejection; Google for scheduling flexible demand.
Each case needs a concrete choice, a mechanism and an engineering consequence.
Use a prediction and reveal when the changed condition tests useful reasoning. Keep source interpretation out of the
main visual unless it changes the engineering conclusion. Primer remains first
exposure to terms; detailed cases belong in the domains.

The reader implements one optional check-in at each domain boundary.
Use those scenarios in presentations when they test a meaningful mechanism;
a concrete design brief can provide the bridge to the next chapter instead.
Do not force a quiz or answer reveal into every ending.

### Required section handoffs

Use the cases below when they teach the section’s engineering question, and
record their integrated location in the last column. A new case can replace one
whose consequence is already taught; do not add a detour solely to satisfy the table. These cases already have reader treatments and standalone teaching
scenes; **none of those establishes integration into the relevant chapter deck**.
The open production tasks remain in [the course review](COURSE_REVIEW.md#next-teaching-step).

| Section | Case and teaching consequence | Existing standalone scenes | Chapter integration |
| --- | --- | --- | --- |
| Siting, grid connection and supply (`d03`) | SemiAnalysis's Southaven/MiniHard procurement workaround: equipment lead time versus the consequences of MV distribution | [Procurement](prototypes/case-studies.html?teach=1#procurement), [current comparison](prototypes/case-studies.html?teach=1#current) | Integrated in Section 4: [route](prototypes/siting-format.html?teach=1#procurement-route), [current](prototypes/siting-format.html?teach=1#transport-current), [circuits](prototypes/siting-format.html?teach=1#parallel-circuits), [decision](prototypes/siting-format.html?teach=1#procurement-decision); authored draft |
| Continuity, storage and protection (`d05`) | Crusoe/Redwood in Sparks: solar power, battery energy, discharge power and grid backup | [Solar and battery](prototypes/case-studies.html?teach=1#sparks), [availability](prototypes/case-studies.html?teach=1#availability) | Pending |
| Storage, orchestration and recovery (`d09`) | Google flexible scheduling: which work can move without missing its service requirement? | [Demand response](prototypes/case-studies.html?teach=1#demand-response) | Pending |
| Heat rejection, climate and water (`d11`) | Abilene cooling: closed coolant loops, outdoor heat rejection and the boundary of water-use claims | [Abilene cooling](prototypes/case-studies.html?teach=1#abilene-cooling) | Pending; existing cooling deck does not yet integrate this case |
| Physical site, buildings and safety (`d12`) | Greenfield versus brownfield, using Abilene and original Colossus; factory reuse still required new power infrastructure | [Land comparison](prototypes/case-studies.html?teach=1#land), [original Colossus](prototypes/case-studies.html?teach=1#colossus) | Integrated in Chapter 5: [greenfield/brownfield](prototypes/site-format.html?teach=1#greenfield-brownfield) and [Colossus](prototypes/site-format.html?teach=1#colossus-service); current checks recorded in [TESTING.md](TESTING.md) |
| Capacity, cost and system decisions (`d15`) | Abilene's dated capacity milestones: distinguish the original campus, adjacent project, energized capacity and useful output | [Capacity ledger](prototypes/case-studies.html?teach=1#abilene-ledger) | Pending |

For **Design, procurement and commissioning (`d13`)**, adapt the existing reader
comparison into slides: EPC responsibilities versus manufacturing strategy; factory
and site work; parallel schedules; design freezes; transport; and ownership of
module interfaces. Hold 20 MW constant while 200 × 100 kW racks become 100 × 200 kW
just before fabrication. Require the learner to decide what proceeds, what is held
and which electrical, hydraulic, spatial and schedule evidence releases each hold.
Close with the interface consequences or a meaningful changed-design problem;
the reader’s boundary check is available without forcing it into the slides.

At every section handoff, verify the next chapter is reachable, check any Abilene
claim against its dated source and update the chapter's
presentation status. A reader draft, standalone case and integrated deck are
different completion states.
Register each deck in [the teaching catalog](teaching-sequences.json) so it appears
in the single chapter directory. Classify whether it teaches the chapter
or selected topics; a partial sequence must not imply a complete chapter deck.
Chapter numbers are generated from the curriculum teaching order; do not maintain a separate numbering list.

### Build the teaching sequence

Use these rules when adapting each sequence:

1. **Begin with the learner's question.** Give the equipment a job before naming
   its technology. Open a substantive chapter with its purpose and the decision
   its mechanisms will support. Introduce specialist terms at the object where
   they matter; the glossary is a lookup aid, not a prerequisite lecture.
2. **Locate the mechanism.** Show campus → building → rack → component context,
   physical form and the relevant connections. Embed a real product photograph
   when using a product example. Preserve names and interfaces as the view changes.
   Anchor hardware examples in a named platform and a stated quantity. Explain
   what its components do and attach operating conditions to quoted
   specifications; separately listed maxima need not be achievable together.
3. **Make the diagram teach.** Use one explanatory sentence as the headline,
   one dominant visual, and essential labels, quantities and assumptions beside
   their objects. Remove competing bottom summaries and repeated titles. Put
   exceptions, source discussion and longer derivations in the reference or an
   written reference. An essential reasoning step must remain visible without notes.
   Remove standalone slides that merely repeat an obvious observation or an
   arithmetic identity. Put useful equations where they explain a design choice.
   Introduce their meaning in the teaching sequence; keep the formal model name,
   full term definitions and derivation available in the written reference. A formula can stand alone on the teaching visual while the
   instructor explains it. Keep assumptions visible when they change the answer.
4. **Control the comparison.** Keep the load, boundary, operating state and
   measurement convention fixed until a change is explicitly introduced. Show
   direct comparisons simultaneously when both fit: training beside inference,
   or complete runs beside their energy account. Use a toggle when it reveals a
   mechanism or a controlled change, not merely to hide the other case. Change
   one condition and show its effect on a path, quantity or constraint. Use a
   prediction/reveal only when there is something worth predicting.
   Judge an experiment by what it explains, not by the complexity of its algebra:
   doubling coolant flow at fixed heat load usefully reveals the smaller
   temperature rise; doubling electrical load without a new consequence adds
   little to the 800 V architecture comparison.
5. **End with the consequence.** Return to the opening problem and explain what
   the comparison establishes. Use a changed case when it tests understanding;
   do not append an unrelated calculation to satisfy a format. Remove quizzes
   that only ask whether a number crosses a displayed threshold; a concrete
   design brief or meaningful prediction can close the chapter instead.
   For a failure, trace the surviving path and capacity, then show the response:
   continued service, reduced service or shutdown. Distinguish a configured
   operating response from automatic component protection and unmodeled timing.

The course remains one linear watts-to-racks journey with the heat path back out.
Use the domain map as a coverage check behind that journey. Author one coherent
section at a time, rehearse it, revise the confusing mechanism, then apply those
improvements to subsequent sections. Do not mechanically convert paragraphs into
slides or call a whole domain finished because one sequence is implemented.

## Keep the physical model honest

State whether each number is a sourced specification, an operating measurement,
a chosen service requirement or an original teaching assumption. Derive the
result from visible inputs. A chosen token target is not a hardware benchmark;
a useful conditional scheduling example is not evidence of routine deployment.
Retain its dependency limitation beside it. When equipment must respond to a
changing load, show power against time; the average cannot stand in for the peak
or transition speed.

A correct equation can answer the wrong question. Current does not establish
facility efficiency; energy capacity does not establish discharge power; total
coolant flow does not establish adequate flow through every branch. Name the
account being calculated and show assumptions at the result.

- Separate physical flows from control and commercial relationships. Distinguish
  coolant circulation from heat crossing an exchanger. A shared diagram color
  must not suggest that isolated fluid loops mix.
- Distinguish a component from its containing system: a transformer may be part
  of a converter; a battery is not the entire UPS. Attribute losses and functions
  to the actual component shown.
- Distinguish physics, teaching assumptions, product ratings, proposed designs
  and observed operation. Commercial maturity is not a physical impossibility;
  one semiconductor's voltage rating is not a complete converter's rating.
- Explain electrical measurement conventions before using them: closed DC loop,
  AC reversal, RMS and balanced three-phase paths. Keep received average power
  explicit when waveforms change. Introduce new thermal and computing quantities
  with the same care.
- Check relevant conservation accounts, limits and failure states independently.
  A capacitor reaching a shutdown voltage is not empty; a schematic state is not
  an operating procedure; a nameplate rating is not surviving service capacity.

Choose the visual that teaches the mechanism: a GPT-generated illustration,
manufacturer diagram, real photograph, code-rendered comparison or a combination.
When the user asks for image generation, produce the asset or record a specific,
local reason for another visual in the existing review tracker. Do not silently
skip it or invoke a general ban on generated mathematical/technical diagrams.
A useful combination is generated physical context with inspectable labels,
curves or states overlaid in code. Verify each arrow, label, unit, connection and
operating state against the intended model; appearance alone proves none of them.
Existing [asset-specific limits](assets/README.md) describe those particular images,
not a prohibition on future generated teaching visuals. Prefer the actual named
product/site photograph or manufacturer diagram when identity and anatomy are
part of the lesson. Motion must explain a defined change and remain intelligible
when paused.

## Author in the existing sources

The four lesson inputs in `course/expansion/` are `foundations-power.json`,
`racks-compute-heat.json`, `heat-delivery-operations.json` and `capstones.json`.
Edit the relevant lesson there, preserving its stable ID and domain-map objective
IDs. Each lesson records its question, explanation, worked example, tradeoff,
limiting case, practice, terms where needed and authored visual. Capstones retain
the map's `capstone_id`.

Add checked sources to `research-sources.json` and record the specific supported
claim, `reviewed_on` date and reading limits in the lesson. Describe what was
actually accessible and read; retain disagreements rather than hiding them in an
average. Use original explanatory prose. Follow the [research workflow](../research/README.md).

`uv run gigawatt-expand` generates the reader, Markdown lessons and manuscript.
Do not edit those outputs. The builder establishes structural coverage, not
technical correctness or comprehension. [TESTING.md](TESTING.md) holds commands
and verification results.

A presentation needs its own authored mechanism and model. For JSON-backed
presentations, retain the six `learning_contract` fields: `driving_question`,
`fixed_boundary`, `changed_variable`, `primary_payoff`, `misconception` and
`closing_question`. Scenes retain a `pedagogical_role`: `problem`, `comparison`,
`mechanism`, `architecture`, `balance`, `counterexample` or `transfer`. These fields
make the reasoning inspectable; they do not require a scene for every role.

The 800 V sample uses `sample.json` for the reading explanation and
`sample-presentation.json` for scenes, with `course/web/presentation.*` and
`electrical-visuals.js` rendering the visuals. `reader-models.js` holds shared
calculations. The UPS prototype uses `course/prototypes/ups-format.html` and its
separate mechanism modules. The cooling prototype uses
`course/prototypes/cooling-format.html`, its mechanism modules and
`cooling-model.js`. Preserve stable scene IDs and replacement aliases; keep
student, teaching and reference calculations consistent.

## Rehearse and check the section

Teach without recording and without requiring speaker notes. Any private notes remain outside the slide view and contain a few cues, never a script. Capture the exact scene and point of confusion; revise
that diagram, term or reasoning step and try again. A reader lesson, an implemented
presentation and a rehearsed explanation are distinct states.
When handing over a section, identify what is actually taught in its slides and
what remains only in the reference, so the reviewer knows what they are reviewing.

Verify quantitative examples and invalid inputs. Inspect the actual teaching
viewport in light and dark mode, at narrow widths and with keyboard navigation.
Check labels against their own objects, not just the canvas edge: text must fit
inside its box or have an unambiguous leader. Inspect arrow origins and endpoints
for the physical meaning they imply, including every revealed or fault state.
Give independent variables separate labeled control groups. Selected states must
stay visible, match the diagram and survive changes to the other controls. Check
repeated selections, restoration, keyboard use and touch as well as the first click.
Keep visible focus, text alternatives, sufficient contrast, paused/reduced-motion
states and an understandable reading route when interaction is unavailable. Color
alone cannot convey the answer. Browser checks do not establish comprehension.

Extend the shared facility drawing, functional bill of materials and service-path
model as each section develops: component, job, location, interfaces and relevant installed,
operating and surviving capacity. State the configuration when it changes.
A local material saving does not become a facility-wide saving by implication,
and the educational inventory is not a procurement specification.
