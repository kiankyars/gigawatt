# GIGAWATT curriculum v2

Status: implemented as the canonical production curriculum. The compiled player
is `diagram/course_v2.html`; the published v1 course remains a byte-preserved
historical comparison and does not supply v2 acceptance evidence.

## Core decision

The course is one system journey taught across multiple explanatory canvases.
The Abilene engineering map remains the evidence-backed case-study topology; it
is no longer required to carry every explanation. Grid and onsite source paths
stay distinct, and the curriculum does not trace one electron or invent an
as-built merge where the evidence is silent.

Each phase teaches the general mechanism first, then maps that mechanism onto
the known Abilene evidence. A redline is therefore an application and evidence
view, not the default lesson surface.

The persistent phase compass is:

`1 Generate -> 2 Transmit -> 3 Campus -> 4 Building -> 5 Compute -> 6 Reject heat`

The opening gigawatt-to-usable-compute funnel and the closing chokepoint,
capital, and usable-compute rereads sit outside the physical phase count. They
frame and synthesize the same six-phase journey.

## Interaction contract

- The presenter owns all dwell time and spoken explanation.
- There is no target duration, autoplay, cadence, or script.
- A teaching visual may have a small number of coarse manual states when the
  conceptual relationship materially changes.
- A state must support a sustained explanation. It is not a micro-animation or
  a timed beat.
- Camera zoom without a new teaching relationship is not a state.
- Evidence and engineering views are available on demand and never replace the
  primary explanatory canvas by default.

## Repeated phase structure

Every physical phase follows the same learner-facing pattern:

1. **Concept:** the problem this phase solves.
2. **Mechanism:** the physical conversion, transport, or control path.
3. **Abilene mapping:** which parts are evidenced at the reference campus and
   which remain unknown.
4. **Consequence:** the constraint handed to the next phase.

This repeated structure is the retention device. The course should not require
the learner to infer the phase boundaries from camera locations.

## Phase 1 — Generate: make electricity

**Anchor question:** Where can an electrical watt come from?

**Objective:** Recognize the major generation families, follow their conversion
chains, and keep physical generation separate from storage, standby power,
behind-the-meter location, and contractual procurement.

The course groups sources by physical conversion rather than presenting a fuel
carousel:

- heat or hot gas -> turbine -> shaft -> generator -> AC;
- moving water or air -> rotor -> generator or power electronics -> AC;
- sunlight -> photovoltaic DC -> inverter -> AC;
- fuel -> electrochemical DC -> power conditioning -> AC;
- charged storage -> discharge conversion -> electricity, explicitly not a
  primary energy source.

Surface examples include gas, coal, nuclear, biomass, geothermal, hydro, wind,
solar PV, fuel cells, batteries, and pumped storage. The grouping is not an
environmental, economic, or reliability ranking.

The Abilene application keeps four evidenced roles separate: physical grid
supply, onsite gas generation, diesel standby generation, and a future-design
BESS. The Microsoft/Constellation nuclear PPA appears only as a generic
comparison between contractual attributes and physical electricity flow; it is
not an Abilene fact and must never be drawn as a dedicated Abilene wire.

**Manual visual states**

1. Major physical conversion families.
2. Convergence on an electrical interface.
3. Generation, storage, standby, location, and contract separated by role.
4. Abilene gas path and its evidence boundary.
5. Phase boundary: once electricity exists, why raise voltage and transmit it?

**Existing material:** retain the supported gas-turbine, generator, and GSU
claims from `s01` and `s02`; fold the physical-versus-contractual lesson from
`s05` into the role comparison.

## Phase 2 — Transmit: move and connect electricity

**Anchor question:** Why can a gigawatt not simply travel down an ordinary
wire?

**Objective:** Explain voltage step-up, long-distance transport, substations,
network behavior, balancing, and the engineering gates between a proposed
large load and energized service.

The generic teaching path is:

`generator or inverter -> step-up transformer -> transmission network -> protection and substation -> campus interface`

The causal opening holds delivered power constant: raising voltage lowers
current, and lower current reduces resistive heating. A second view replaces a
single line with a small network so a contract is not mistaken for a physical
electron route.

Generator interconnection and large-load interconnection are taught as
different processes. FERC Order 2023 concerns generating facilities and
storage seeking transmission interconnection. The current ERCOT large-load
process applies to qualifying large loads; a colocated load and new generator
may need both processes. Rules and thresholds are dated evidence, not timeless
diagram labels.

**Manual visual states**

1. Same power at lower and higher voltage, with qualitative current and loss.
2. Meshed network and continuous supply-demand balance.
3. Substation protection and transformation as an explicit gate.
4. Generator and large-load interconnection gates side by side.
5. Abilene 138 kV and 345 kV paths as the paired case.
6. Phase boundary: the next problem begins behind the campus boundary.

**Existing material:** combine `s03`, `s04`, and the relevant portion of `s17`
instead of teaching two consecutive route redlines.

## Phase 3 — Campus: distribute and protect

**Anchor question:** Once power reaches the property, how can it serve multiple
buildings without one disturbance becoming a campus-wide failure?

**Objective:** Understand a conceptual campus fan-out, follow the coordinated
protection mechanism that can isolate one disturbed feeder, preserve unknown
source boundaries, and separate the architectural roles of UPS, BESS, and
standby generation.

**Manual visual states**

1. One source -> campus bus -> multiple building feeders.
2. One feeder disturbance -> detect -> interrupt -> isolate, with remaining
   building service explicitly conditional on path independence, selective
   coordination, and available capacity.
3. Multiple sources with an explicitly unknown Abilene merge topology.
4. UPS, BESS, and diesel separated by function and response role.
5. Phase boundary: protected campus distribution becomes a building feeder.

**Existing material:** expand `s06`; integrate the response-role portion of
`s19`. Keep the staged-delivery evidence from `s20` as Abilene context in the
evidence surface rather than using it as the central protection lesson.

## Phase 4 — Building: deliver protected power to the rack

**Anchor question:** What must happen between a campus feeder and a rack
position?

**Objective:** Explain the spatial and functional roles of the unit substation,
switchgear, UPS, distribution path, and busway without presenting a generic
reference architecture as Abilene as-built topology.

Equipment is introduced by verb:

- the transformer changes voltage;
- switchgear distributes power and isolates faults;
- the UPS conditions power and bridges interruptions;
- busway carries power to rack positions.

**Manual visual states**

1. Building cutaway from campus entry to data hall.
2. Functional equipment chain with action labels.
3. Generic protected-path or A/B reference architecture.
4. Fault or maintenance isolation scenario.
5. Abilene mapping limited to the exposed building evidence.
6. Phase boundary: rack-position facility AC becomes the compute input.

**Existing material:** retain the electrical-room spatial anchor and expand
`s07` beyond a labels-only equipment chain.

## Phase 5 — Compute: convert facility power into useful work

**Anchor question:** What must happen before facility AC can switch transistors
and produce useful compute?

**Objective:** Follow the electrical descent through rack, board, and die;
separate facility power from accelerator power; and explain why equal delivered
MW can yield different usable compute.

**Manual visual states**

1. Data hall -> rack -> power shelf -> board -> die.
2. Facility AC -> rack DC -> low-voltage, high-current processor rails.
3. Board-level point-of-load conversion steps rack DC down again.
4. Useful output and upstream demand shown as two views of the same work.
5. Abilene platform facts separated from operating unknowns.
6. Phase boundary: computation is desired output; heat is unavoidable output.

**Existing material:** expand `s08`; move the useful-compute logic from `s24`
into this phase; use the grid-response portion of `s19` as the reverse-direction
payoff; finish with `s09`.

## Phase 6 — Reject heat: return energy to the atmosphere

**Anchor question:** How does heat get from silicon back to the atmosphere?

**Objective:** Follow the liquid and residual-air paths, distinguish technology
and facility loops, understand the CDU and CRAH boundaries, and connect heat
rejection to water accounting.

**Manual visual states**

1. Component or die -> cold plate: heat crosses into technology coolant.
2. Cold plate -> rack manifold -> conditional CDU -> facility liquid loop.
3. Residual-air path runs in parallel and converges at a facility boundary.
4. Facility loop -> heat-rejection terminal -> atmosphere, with four water
   accounts kept separate.
5. Full six-phase journey from Generate through Reject heat.

**Existing material:** retain the evidence and topology in `s09`–`s16`, but
compress the eight redline sections into a smaller number of coherent teaching
transformations. The untimed `s10` pilot remains the interaction precedent.

## Synthesis outside the phase count

After all six physical phases are visible, the course reuses the completed
journey for three questions:

1. Where does delivery actually bind?
2. Who builds, owns, finances, operates, and bears utilization risk at each
   layer?
3. How does announced capacity narrow into usable compute and tokens?

These are overlays on the physical model, not additional physical phases.

## Visual grammar

- **Teaching SVG:** causal mechanisms, comparisons, equations, role separation,
  and coarse transformations.
- **3D scene:** location, nesting, and physical scale.
- **Engineering map:** topology, evidence posture, exact known/unknown boundary,
  and case-study application.
- **Evidence drawer:** claim, scope, source, date, and promotion guard.

A section fails the redesign if its primary visual is only a cropped redline or
if understanding it requires the presenter to invent the missing causal
relationships verbally.

## Evidence contract

- Generic principles live in generic engineering ledgers and cannot be promoted
  into Abilene as-built claims.
- Site facts remain in the Abilene ledgers.
- Commercial instruments remain visually separate from physical power flow.
- Storage always carries both power and energy/duration concepts when a
  numerical comparison is made.
- Generation and large-load interconnection processes are never conflated.
- Fast-changing rules, thresholds, project states, and market quantities carry
  explicit dates.
- A teaching element must bind to at least one validated course claim.

## Production acceptance gate

The Phase 1 pilot established the requirements now applied to every phase and
the compiled player:

- the major generation families are understandable without the Abilene map;
- nuclear, solar PV, fuel cells, storage, PPA, standby, and behind-the-meter are
  not conflated;
- the visual supports several minutes of unscripted explanation per state;
- all state changes are manual and untimed;
- the Abilene redline appears only after the generic mechanism is established;
- every visible factual teaching element resolves to an authoritative source;
- browser review passes at desktop, tablet, short-height, and portrait sizes;
- keyboard and screen-reader structure remain usable.

All six phase manifests and renderers now use this contract. The frozen v1
champion and its acceptance corpus remain historical comparison evidence and
are not reused as v2 acceptance evidence.

## Production implementation architecture

The production v2 course is one compiled manual player, not a collection of
unrelated demo pages. Its source and artifact chain is:

`phase manifests + registered evidence -> validated course registry -> phase renderers -> one course player`

The implementation follows these boundaries:

- Each phase owns a strict YAML manifest containing its anchor question,
  learning objective, coarse manual states, semantic visual objects, Abilene
  case mapping, and qualified fact references.
- A shared compiler validates interaction, evidence, and state coverage. A
  phase-specific renderer may choose different geometry, but it may not weaken
  the common evidence or interaction contract.
- The player owns the persistent six-phase compass, phase and state navigation,
  keyboard behavior, responsive layout, evidence drawer, and source links.
- In Phases 4 through 6 at widths of 900 px and above, the player may manually
  substitute the validated `electrical_room`, `data_hall_rack`, or
  `thermal_return` camera from `diagram/hybrid.html`. The outer shell owns the
  camera title, purpose, conceptual/non-as-built boundary, return control, and
  keyboard behavior; the 2D state remains authoritative for causal and evidence
  detail.
- A renderer owns only the explanatory canvas for one phase. It does not own
  course order, spoken wording, timing, evidence posture, or Abilene topology.
- Desktop may use a semantic SVG when relationships need spatial routing.
  Portrait and short-height layouts may use payload-derived HTML when scaling
  the same SVG would make labels unreadable. Both surfaces must expose the same
  objects, states, claims, and evidence.
- The generated standalone phase pages remain development fixtures. The
  publishable artifact is the compiled v2 course player plus a machine-readable
  registry and an instructor packet generated from the same manifests.

The concrete generated package is `diagram/course_v2.html`,
`diagram/course_v2_runtime.json`, `course/INSTRUCTOR_PACKET_V2.md`, and the six
same-origin phase HTML dependencies named by `course/course_v2.yaml`. Its
supplemental spatial dependency closure is `diagram/hybrid.html`,
`diagram/cameras.yaml`, `diagram/master.svg`,
`diagram/map_watt_heat_handoff.svg`, and the pinned local Three.js modules and
license. The spatial control is absent below 900 px rather than presenting a
cropped or unreadable 3D view.

V2 receives its own acceptance epoch. Passing the v1 ratchet proves that the
historical comparison remains reconstructable; it cannot serve as browser,
accessibility, editorial, or blind-review evidence for the replacement course.
