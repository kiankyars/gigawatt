# Lesson and visual authoring standard

Updated **2026-09-12**. The [course template](COURSE_REVIEW.md) owns audience,
scope and production priorities. The [domain map](domain-map.json) owns objectives,
prerequisites and sequence. This file owns teaching rules; [PRESENTING.md](PRESENTING.md)
owns the rehearsal playbook and controls. Do not create another design brief for
an individual lesson.

## Carry the reasoning across the course

The reviewed UPS, 800 V and D10/D11 cooling sequences establish an approach:
**pose a concrete problem → show the mechanism → change one condition → explain
the consequence**. Select the visual and example that make the particular topic
understandable. The course template records the working goal of at least 300
substantive slides. Individual chapters have no fixed slide count or
three-lessons-per-domain quota; a chapter can span parts of several domains.

Retain material that helps the learner explain, calculate, compare or diagnose
the facility. Cut article-by-article narration, equipment inventories without a
purpose and arithmetic that does not affect the engineering decision. A longer
reference is useful; narrating it does not produce a better lesson.

The opening is a broad orientation: preview the equipment, locations and paths
that later sections explain in depth. Briefly naming generation, transmission,
backup, compute, networking and cooling is useful here; each preview needs a
visible role in the same facility journey. Save detailed comparisons for the
section where the learner has the prerequisites.

Use these rules when adapting each sequence:

1. **Begin with the learner's question.** Give the equipment a job before naming
   its technology. Introduce specialist terms at the object where they matter;
   the glossary is a lookup aid, not a prerequisite lecture.
2. **Locate the mechanism.** Show campus → building → rack → component context,
   physical form and the relevant connections. Embed a real product photograph
   when using a product example. Preserve names and interfaces as the view changes.
   Explain what its components do and attach operating conditions to quoted
   specifications; separately listed maxima need not be achievable together.
3. **Make the diagram teach.** Use one explanatory sentence as the headline,
   one dominant visual, and essential labels, quantities and assumptions beside
   their objects. Remove competing bottom summaries and repeated titles. Put
   exceptions, source discussion and longer derivations in the reference or an
   optional view. An essential reasoning step must remain visible without notes.
   Remove standalone slides that merely repeat an obvious observation or an
   arithmetic identity. Put useful equations where they explain a design choice.
   Introduce their meaning in the teaching sequence; keep the formal model name,
   full term definitions and derivation available in the reference or optional
   explanation. A formula can stand alone on the teaching visual while the
   instructor explains it. Keep assumptions visible when they change the answer.
4. **Control the comparison.** Keep the load, boundary, operating state and
   measurement convention fixed until a change is explicitly introduced. Change
   one condition and show its effect on a path, quantity or constraint. Use a
   prediction/reveal only when there is something worth predicting.
   Judge an experiment by what it explains, not by the complexity of its algebra:
   doubling coolant flow at fixed heat load usefully reveals the smaller
   temperature rise; doubling electrical load without a new consequence adds
   little to the 800 V architecture comparison.
5. **End with the consequence.** Return to the opening problem and explain what
   the comparison establishes. Use a changed case when it tests understanding;
   do not append an unrelated calculation to satisfy a format.
   For a failure, trace the surviving path and capacity, then show the response:
   continued service, reduced service or shutdown. Distinguish a configured
   operating response from automatic component protection and unmodeled timing.

The course remains one linear watts-to-racks journey with the heat path back out.
Use the domain map as a coverage check behind that journey. Author one coherent
section at a time, rehearse it, revise the confusing mechanism, then apply those
improvements to subsequent sections. Do not mechanically convert paragraphs into
slides or call a whole domain finished because one sequence is implemented.

## Keep the physical model honest

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

Use code-rendered diagrams for connections, quantities and failure states.
Generated images can orient the learner, but visual inspection cannot validate
wiring, piping or anatomy. Follow the existing [image role limits](assets/README.md)
and replace misleading details. Source photographs need the correct product,
configuration and provenance. Motion must explain a defined change and remain
intelligible when paused.

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

Teach without recording and without requiring speaker notes. Optional notes are
a few cues, never a script. Capture the exact scene and point of confusion; revise
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
