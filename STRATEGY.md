# STRATEGY — retention primitives for GIGAWATT

*Written 2026-08, reconciled with the completed v1 runtime on 2026-08-27, and
amended for the six-phase v2 redesign on 2026-08-31. Current production status
is recorded at the end.*

## The premise

**Follow one watt.** From grid or behind-the-meter origination to the transistor
gate, and back out as heat to the atmosphere. By the end, "a 1 GW campus" is not a number —
it is a topology: equipment counts, redundancy levels, lead times, construction
sequencing, and the binding constraint.

Scope decisions already made:

- The course does **not** stop at the VRM. Energy in, heat out — the thermal
return path is half the course, not an appendix.
- The neocloud capital stack (who secures land/power, who finances, who owns
GPUs, who bears utilization risk) is **inside** this course, as a re-read of
the master diagram — not a separate business explainer.
- "First principles" was a misnomer. The gap this course fills is the
system + economics + chokepoint view. Physics arrives just-in-time, only when
a piece of equipment demands it.
- The course starts at **generation**, not the transmission corridor. Gas
turbines, nuclear PPAs, behind-the-meter plants are inside — as *one act*,
but physical grid and behind-the-meter paths remain distinct until the
conceptual campus-MV distribution envelope. The exact as-built common-bus
topology remains open.
They share the same gate logic (the watt cannot originate without them),
not a survey of the power industry. Two structural payoffs: the interconnection
queue becomes the cold open rather than backstory, and the figure-eight closes
into a loop — the course opens with heat becoming electricity and ends with
electricity becoming heat. Behind-the-meter is also load-bearing for the
capital-stack read (Crusoe-style generation-first plays need the turbine
introduced as a physical gate first).



## What this course is NOT (the anti-priors)

Chips was a cast drama: charismatic protagonists (TSMC, ASML, Intel), rivalry
framing, scoreboards. Its devices exist to serve characters. This course has a
thin cast — Eaton, Vertiv, Schneider, GE Vernova are vendors encountered at
gates, not protagonists. **The protagonist is the watt; the star is the system.**
Retention machinery is therefore spatial and physical, not character-driven.
Do not import chips devices ritually. What survives from chips is workflow only:
course-as-code, source-linked fact packs, VERIFY discipline, act-by-act
recording, swappable slides for fast-rotting facts.

## The six primitives



### 1. One journey, persistent orientation

*V2 amendment, 2026-08-31:* the original “one diagram, one camera” rule made
the engineering map carry explanations it was not designed to carry. The
course now follows one persistent system journey across multiple explanatory
canvases while grid and onsite sources remain separate branches unless evidence
establishes their merge. A six-phase compass keeps the learner oriented:

`Generate → Transmit → Campus → Building → Compute → Reject heat`

Clean 2D teaching canvases explain causal mechanisms and comparisons. The 3D
scene establishes location, nesting, and scale. The Abilene one-line remains
the evidence-backed case map and poster, but appears after the generic
mechanism is understood rather than serving as every lesson's background.
Powers-of-ten structure still runs from 138/345 kV or generator-terminal MV →
substation yard → electrical room → rack → board → die. The learner keeps one
journey and one phase position without being confined to one drawing.

### 2. The phase input/output journey bar

Progress is not abstract acts. The electrical journey begins on one of three
branches: 138 kV initial grid service, 345 kV expansion grid service, or
generator-terminal MV behind the meter. Those source-side paths remain separate
at the Abilene evidence boundary; the as-built merge is unknown. Generic
teaching canvases then explain campus distribution and the downstream descent
through facility AC → nominal 50–51 VDC at the documented GB200 rack busbar →
core voltage. Exact Abilene campus MV, rack AC input, generator terminal
configuration, and core voltage do not render as invented numbers.

Every piece of equipment is introduced by the conversion, transport, protection,
or control function it performs between a phase input and output. On the thermal
return, the bar follows die heat → technology return → facility return →
air-cooled chiller → atmosphere. Voltage is a state marker, not itself a
conserved quantity.

### 3. The loop, not the line

Act structure is a figure-eight. Descend the voltage ladder to the die; the turn
is the strongest conceptual reversal — *the watt you spent eight segments
delivering is, in the same instant, your enemy* — then ride the heat back out.
Cooling is load-bearing because the structure makes it the second half of one
conserved journey, not a bolted-on topic.

### 4. Three read-throughs of one diagram

Once the diagram is fully lit physically, it is re-read twice:

1. **Chokepoint read.** Where the buildout actually binds: large power
  transformer lead times, interconnection queues, turbine backlogs, switchgear
   and cooling equipment lead times. Quantified, dated, sourced.
2. **Capital-stack read.** Color every box by who owns it, who financed it, who
  operates it, who bears utilization risk. This is where Crusoe, CoreWeave,
   Fluidstack, hyperscalers, developers, and colos stop being synonyms —
   visually, on the same diagram, as different colorings of identical hardware.



### 5. Original evidence

`datacenter_atlas` is the differentiation no competitor has: satellite-tracked
construction timelines, permitting records, real campuses. Chokepoint claims are
illustrated with actual sites and dates, not stock footage.

**Reference campus: Abilene (Lancium / Crusoe / Oracle — Stargate).** Every
site-specific number on the master diagram resolves through registered evidence
ledgers. `evidence/abilene.yaml` owns the base topology: the planned 1.2 GW grid interconnection, separate
200 MW / 138 kV and 1 GW / 345 kV service paths, and permitted gas and diesel
layers. A permit is never promoted into installation or operation. The ledger
also carries explicit nulls for unresolved campus MV, commissioning, building,
and GPU-count questions. Execution, delivery/resilience, commercial, and
compute-method claims remain in separately scoped ledgers. Project Jupiter (2.45 GW BTM fuel
cells) stays in reserve as the behind-the-meter contrast case for the
capital-stack read. GPU load transients
(synchronized training steps swinging tens of MW in milliseconds) are the
seed→payoff thread that ties the die back to the grid and to BESS.

### 6. The gigawatts-to-tokens funnel

The course's thesis, stated as an accounting identity: **announced gigawatts are
not usable compute.** Announced → interconnected → energized → commissioned →
utilized, with dated fractions and lag times at each gate, evidenced by
`datacenter_atlas` (announced-vs-under-construction with satellite timestamps —
the one dataset competitors don't have). The funnel is the cold open ("company X
announced N gigawatts; here is how few tokens exist today — this course explains
every place the watts died") and a re-read overlay on the master diagram, not
new nodes.

**Scope boundary:** the closing segment teaches the power-to-token conversion
recipe — the internals of batching, utilization, and MFU: how a delivered
megawatt becomes tokens, and why identical hardware yields different token
counts. It does not teach serving infrastructure or network topologies — that
is a different course. The figure-eight still closes at the atmosphere.

## Diagram standard (the anti-slop contract)

The failure mode: freehand AI-generated SVGs with invented aesthetics —
gradients, rounded infographic blobs, inconsistent weights. The defense: this
genre already has drafting conventions, so the aesthetic is inherited, not
invented.

- **Symbol library first.** Electrical side uses IEEE/ANSI-inspired one-line
symbols; cooling side uses simplified process-schematic conventions. No diagram is drawn
until the library exists.
- **Design tokens.** One typeface, two line weights, one voltage-keyed color
scale, flat fills only. No gradients, no shadows, no decoration.
- **Composed, not drawn.** Every diagram is generated programmatically from the
symbol library and layout code. Placement lives in `diagram/layout.yaml`;
`uv run gigawatt-layout` composes `diagram/master.svg`. No one-off freehand SVGs.
- **One review gate.** The master diagram gets a hard redline before any zoom
state or lighting state derives from it. The 2026-08-25 disposition is recorded
in `REDLINE.md` and enforced by the project validator.



## Substrate

The native SVG/HTML/Three.js application is the manual course player. Phase
manifests and registered evidence are the source of truth for explanatory
states; `master.yaml` remains the source of truth for the Abilene engineering
map. A teaching state is a coarse, instructor-selected conceptual
transformation, not merely a camera crop and never a timed beat.

Non-spatial evidence appears in an instructor-controlled evidence drawer pinned
to the active teaching state. The production path does not depend on Slidev or
Manim. The same validated manifests generate the recording surface and the
clickable companion, so the two cannot drift into different courses.

### The 3D scene (decided 2026-08-24)

The visual direction is a hybrid, with a split of jobs:

- **2D master diagram** (`diagram/master.svg`) is the engineering map — one-line
  fused with site cross-section, voltage-keyed, the poster. It is how you *read*
  the system: what gates what, at which voltage, in which order.
- **3D scene** (`diagram/hybrid.html`) is how you *see* the campus. It does the
  establishing shot (whole site, orbitable) **and** the spatial zooms (electrical
  room, data hall, rack). A 2D close-up of three symbols in a row is not a
  segment; that job belongs to the 3D camera moving through the building.

Constraints on the 3D stay inside the anti-slop contract: same design tokens
(palette, flat shading, no decoration), same topology (all semantic membership
derives from `master.yaml`; `scene.yaml` contains placement only). It does not replace
the one-line as the source of truth. When a number, vendor, or chokepoint has
to be read, it is annotated on the 2D map.

The six-state demonstration slice is declarative in `cameras.yaml`: 2D system orientation
→ 3D campus establishing → 3D electrical room → 3D data hall/rack → 2D semantic
boundary at the die → 3D thermal return. It proves the hybrid runtime; it is not
the canonical full-course sequence. `course/segments.yaml` retains the frozen v1
sequence; the canonical v2 sequence lives in `course/course_v2.yaml`.

The canonical v2 player reuses three of those validated cameras as optional,
manual spatial anchors: electrical room in Phase 4, data hall and rack in Phase
5, and thermal return in Phase 6. They are available at 900 px and wider, carry
an explicit conceptual/non-as-built boundary, and never replace the 2D teaching
state that owns causal relationships and evidence detail.

## Current production package

- **Canonical v2 course.** `course/CURRICULUM_V2.md` defines the implemented
  six-phase curriculum. Six deterministic, evidence-bound phase renderers feed
  the single manual player at `diagram/course_v2.html`; the engineering map is
  an application layer rather than the default background.

- **Runtime target.** Deliberately unset. `course/segments.yaml` supplies
  relative production weights, but the presenter owns dwell and total length.
- **Full phase inventory.** Complete: Generate, Transmit, Campus, Building,
  Compute, and Reject heat contain 33 coarse manual states, followed by three
  whole-system synthesis lenses.
- **Evidence gate.** Every phase compiles qualified facts and explicit boundaries
  from registered ledgers. Unavailable private site, commercial, utilization,
  and throughput facts remain explicit nulls rather than research placeholders.
- **Production package.** `diagram/course_v2.html`,
  `diagram/course_v2_runtime.json`, and `course/INSTRUCTOR_PACKET_V2.md` are
  generated from the same spine and phase contracts. The player also binds
  `diagram/hybrid.html` and its camera/map/local-runtime dependencies for the
  three manual spatial anchors. `course/TESTING.md` owns the untimed editorial
  walkthrough.
- **Historical comparison.** `diagram/course.html`, its v1 registry and packet,
  and the frozen acceptance corpus remain reconstructable but are not the
  production course or v2 acceptance evidence.
