# STRATEGY — retention primitives for GIGAWATT

*Written 2026-08. This is a sketch of the design primitives, produced before any curriculum or slides exist. Nothing here is final.*

## The premise

**Follow one watt.** From the transmission corridor to the transistor gate, and
back out as heat to the atmosphere. By the end, "a 1 GW campus" is not a number —
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
entered through the same gate logic (the watt cannot originate without them),
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



### 1. One diagram, one camera

The entire course is a single master diagram — a campus one-line diagram fused
with a site cross-section — and every segment is a camera move on it.
Powers-of-ten structure: 345 kV corridor → substation yard → electrical room →
rack → board → die. The viewer never loses spatial position because there is
only one space. The master diagram ships as the poster and (post-video,
optionally) as a clickable companion where every box opens its dossier.

### 2. The conserved quantity as journey bar

Progress is not abstract acts — it is the voltage stepping down on screen,
after one ascent at origination:
**~20 kV (generator) → 345 kV → 34.5 kV → 480 V → 54 V → ~0.8 V.**
Every piece of equipment is
introduced as *the thing that gets you from this voltage to that one* — the
watt cannot proceed without it. This structurally kills the listicle: no box
appears except at the moment it gates the journey. On the return path the bar
inverts to temperature/heat flux: die → cold plate → CDU → chilled water loop →
tower/dry cooler → atmosphere.

### 3. The loop, not the line

Act structure is a figure-eight. Descend the voltage ladder to the die; the turn
is the single strongest beat available — *the watt you spent eight segments
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
number on the master diagram is pinned to this site: 1.2 GW ERCOT grid
connection, 200 MW + 1 GW substation ladder, GE Vernova turbines on site, and
the deepest evidence package in the atlas (curated record, municipal permitting,
two satellite-change retains, Jun 2024 → Jun 2026 chronology). Details and open
VERIFY items live in `diagram/master.yaml`. Project Jupiter (2.45 GW BTM fuel
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

- **Symbol library first.** Electrical side uses IEEE 315 / ANSI one-line
symbols; cooling side uses simplified P&ID conventions. No diagram is drawn
until the library exists.
- **Design tokens.** One typeface, two line weights, one voltage-keyed color
scale, flat fills only. No gradients, no shadows, no decoration.
- **Composed, not drawn.** Every diagram is generated programmatically from the
symbol library and layout code. Placement lives in `diagram/layout.yaml`;
`uv run gigawatt-layout` composes `diagram/master.svg`. No one-off freehand SVGs.
- **One review gate.** The master diagram gets a hard human redline before any
zoom state or lighting state derives from it.



## Substrate

The diagram is the substrate; Slidev is demoted to a camera player. The master
SVG — with stable IDs on every box, edge, and label — is the single source of
truth. A "slide" is a declarative camera state: viewport, lit set, overlays.
The deck is a sequence of camera states with animated transitions between them.
This inverts the chips workflow: there, slides were the artifact; here, slides
are derived views of the diagram.

Slidev stays because the recording pipeline is proven and a chunk of the
evidence is non-spatial (satellite timelines, lead-time charts, tables). That
material appears as overlays pinned to the diagram location it belongs to —
the camera never cuts away to a naked slide.

Consequence: the interactive companion is no longer a post-video decision. It
is the same camera states with a click handler, so it falls out of the build
for free.

### The 3D scene (decided 2026-08-24)

The visual direction is a hybrid, with a split of jobs:

- **2D master diagram** (`diagram/master.svg`) is the engineering map — one-line
  fused with site cross-section, voltage-keyed, the poster. It is how you *read*
  the system: what gates what, at which voltage, in which order.
- **3D scene** (`diagram/mock_3d.html`) is how you *see* the campus. It does the
  establishing shot (whole site, orbitable) **and** the spatial zooms (electrical
  room, data hall, rack). A 2D close-up of three symbols in a row is not a
  segment; that job belongs to the 3D camera moving through the building.

Constraints on the 3D stay inside the anti-slop contract: same design tokens
(palette, flat shading, no decoration), same topology (geometry must derive from
`master.yaml` before it ships, not hand-placed coordinates). It does not replace
the one-line as the source of truth. When a number, vendor, or chokepoint has
to be read, it is annotated on the 2D map.

The 2D electrical-room camera (three nodes on a line) was a substrate proof
and is not the teaching close-up.

## Open questions (deliberately unresolved)

- **Runtime target.** Unset until the segment list exists.
- **Act inventory and segment list.** Deliberately not sketched yet — the master  
diagram should be designed first, and segments derived from its zoom states,  
not the reverse.

