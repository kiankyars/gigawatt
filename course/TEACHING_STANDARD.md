# From a reading lesson to a teaching sequence

Updated 2026-09-09 after the 800 V DC dry-run feedback. This is the course-wide
authoring standard and adaptation plan. The 800 V sample implements the first
revision; the remaining 50 reading lessons have not been converted or rehearsed.

## Start with the engineering purpose

State the useful outcome before introducing its equation. For 800 V DC, the
purpose is to deliver more power using less distribution copper and release space
occupied by power equipment. A fixed 100 kW comparison isolates the material
benefit; it does not prove that an unchanged feeder can serve any future rack.

Each sequence declares six fields in a `learning_contract`:

| Field | What the author must settle |
| --- | --- |
| `driving_question` | The concrete problem the learner will solve. |
| `fixed_boundary` | The system, operating state and quantities held constant; any later boundary change. |
| `changed_variable` | What the controlled comparison changes. |
| `primary_payoff` | Why the mechanism matters to the engineering decision. |
| `misconception` | The plausible wrong inference the visual must expose. |
| `transfer_question` | A changed case the learner must reason through before seeing its answer. |

Assign each scene a `pedagogical_role`: `problem`, `comparison`, `mechanism`,
`architecture`, `balance`, `counterexample` or `transfer`. Begin with the problem,
teach its mechanism, and end with transfer. The number and order of intermediate
scenes depend on the topic. There is no eight-slide rule, three-lessons-per-domain
quota or runtime target to fill.

The builder checks these declarations, headline/caption text budgets, separate
notes and explanations, duration totals and stable-link aliases. It cannot judge
whether the explanation teaches well. The current renderer's scenes still serve
the 800 V sample; adapting another domain requires an authored visual and any
appropriate model, not merely a different JSON title.

## Make the reasoning visible

1. Locate the component and show its job before naming specialist terms. Reuse
   campus → building → rack → board → chip boundaries and consistent symbols.
2. Show the physical comparison. Count wires, modules, pipes or paths; make
   occupied and released space visible. A percentage alone hides its mechanism.
3. Freeze the baseline and change one stated condition. Keep units, denominator,
   normal/failure state and decisive assumptions beside the visual.
4. Ask for a prediction, then reveal the calculation or path trace. Distinguish
   model inputs, calculated outputs and externally measured claims.
5. Close the relevant account: power, energy, mass flow, capacity, time or cost.
   Reconcile interfaces before summing. A new boundary gets an explicit transition.
6. Apply the reasoning to a changed case and update the shared facility artifact.
   Record what is established and what still needs an equipment rating or evidence.

Use exact, code-native diagrams for quantities, connections and failure states.
Use generated equipment imagery for orientation where it helps; it must not
invent an electrical connection, equipment rating or quantitative scale. Motion
must remain understandable when paused. Explain the same mechanism in the
student reference and keep the calculation shared across surfaces.

## Keep the three surfaces distinct

- **Student exploration:** sparse visuals, prediction/reveal and optional explanation.
- **Teaching endpoint:** the same visuals with instructor controls; no narration wall.
- **Private notes and written reference:** notes contain spoken reasoning and action
  cues; the reference holds derivations, terminology, source claims and limitations.

Introduce vocabulary at its first useful application. An optional opening
orientation can identify recurring equipment and units; a 20-minute list of
definitions cannot replace those introductions. Add glossary links for later lookup.

## Build one facility artifact through the course

The companion should accumulate a functional bill of materials and service-path
map. Each addition records component/function, location, quantity and unit,
operating load, installed and surviving capacity where relevant, upstream/downstream
interfaces, evidence status and the lesson that changed it. A material comparison
records the design assumptions beside the quantity. It is an educational inventory,
not a purchase-ready equipment specification.

For the sample, the local update is three equal conductor lengths → two, rack
AC/DC conversion → a stated sidecar or power-room location, and a separate energy
account. Do not turn 33.3% less illustrative conductor copper into a facility-wide
BOM reduction. The persistent cross-course BOM interface remains to be built.

## Adapt the whole curriculum deliberately

Every row below needs an authored sequence and a dry run; these are proposals,
not claims that new presentations exist. Preserve existing useful research and
worked examples, but merge or split lessons around the reasoning task.

| Domain | Visual mechanism to teach | Changed case / facility-artifact update |
| --- | --- | --- |
| D01 Quantities and boundaries | Trace one rack's input, useful output and losses | Move a measurement boundary; reconcile kW and kWh |
| D02 Workload brief | Convert workload demand into continuous and transient requirements | Change duty cycle; update the load brief |
| D03 Grid and supply | Trace the energization dependencies of one site | Delay one dependency; revise available capacity/date |
| D04 Distribution | Follow voltage, current and capacity along one power path | Change feeder demand; update distribution interfaces |
| D05 Continuity | Trace UPS normal/battery/bypass paths and spare units versus independent routes | Maintenance plus a fault; update surviving capacity |
| D06 Rack power | Count copper and locate conversion, then close the energy account | Double rack demand; identify the unverified capacity limit |
| D07 Compute and memory | Follow one workload through its memory and compute limits | Change arithmetic intensity; identify the limiting resource |
| D08 Networks | Count ports, links and traffic across a visible topology | Remove a link or change traffic; update usable throughput |
| D09 Storage and recovery | Follow a write, checkpoint and restart through dependencies | Lose a component; distinguish stored, durable and recoverable state |
| D10 Heat capture | Trace chip → cold plate → fluid, including residual air heat | Increase rack duty; update flow and cooling interfaces |
| D11 Heat rejection | Close the outdoor heat account at stated ambient conditions | Change weather or water availability; update the operating envelope |
| D12 Physical site | Overlay equipment, access and service routes | Replace the largest component; test clearances and dependencies |
| D13 Delivery and commissioning | Trace the critical path and accepted complete service path | One delayed/unaccepted subsystem; revise usable capacity |
| D14 Operations | Trace measurements and controls through a failure and restoration | Misleading telemetry or maintenance state; revise service status |
| D15 System decisions | Combine electrical, cooling and accepted-path constraints | Move the binding constraint; update capacity and cost |
| Five capstones | Reuse the accumulated facility model | Solve an unfamiliar coupled case without adding unexplained concepts |

Production order: rehearse the revised 800 V sample, implement D05's documented
redundancy gaps, then build the opening orientation and functional BOM. Continue
through dependent domains in the course map. Familiarity with generation or
campus distribution can accelerate Kian's preparation; it does not establish
that those sections already teach effectively.

## Use dry-run evidence to revise

Teach without recording first. At each hesitation, capture the scene, the exact
question, the missing term/mechanism/boundary or unsupported claim, and the revision.
After the change, ask the learner to explain the mechanism and solve the changed
case. A browser pass proves layout and interaction; it does not prove comprehension.

The sample's feedback establishes the changes to test across the course: less
on-screen text, clear student/teacher endpoints, correctly stated comparison
boundaries, visible material and space benefits, and a meaningful final application.
Adopt these as the working standard now; refine them after rehearsal instead of
automatically copying the sample's exact scenes into 50 lessons.

**Anti-pattern:** an encyclopedic survey of articles, acronyms or equipment.
Every retained section must improve a learner's ability to explain, calculate,
compare or diagnose the facility. Coverage is demonstrated by that capability,
not by word count, duration or the number of mapped sources.
