# STRATEGY — retention primitives for GIGAWATT

*Written 2026-08. This is a sketch of the design primitives, produced before any
curriculum or slides exist. Nothing here is final; the master-diagram redline and
the chips video's retention data are both upstream of committing.*

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

## What this course is NOT (the anti-priors)

Chips was a cast drama: charismatic protagonists (TSMC, ASML, Intel), rivalry
framing, scoreboards. Its devices exist to serve characters. This course has a
thin cast — Eaton, Vertiv, Schneider, GE Vernova are vendors encountered at
gates, not protagonists. **The protagonist is the watt; the star is the system.**
Retention machinery is therefore spatial and physical, not character-driven.
Do not import chips devices ritually. What survives from chips is workflow only:
course-as-code, source-linked fact packs, VERIFY discipline, act-by-act
recording, swappable slides for fast-rotting facts.

## The five primitives

### 1. One diagram, one camera

The entire course is a single master diagram — a campus one-line diagram fused
with a site cross-section — and every segment is a camera move on it.
Powers-of-ten structure: 500 kV corridor → substation yard → electrical room →
rack → board → die. The viewer never loses spatial position because there is
only one space. The master diagram ships as the poster and (post-video,
optionally) as a clickable companion where every box opens its dossier.

### 2. The conserved quantity as journey bar

Progress is not abstract acts — it is the voltage stepping down on screen:
**500 kV → 34.5 kV → 480 V → 12 V → ~0.8 V.** Every piece of equipment is
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
illustrated with actual sites and dates, not stock footage. GPU load transients
(synchronized training steps swinging tens of MW in milliseconds) are the
seed→payoff thread that ties the die back to the grid and to BESS.

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
  symbol library and layout code. No one-off freehand SVGs.
- **One review gate.** The master diagram gets a hard human redline before any
  zoom state or lighting state derives from it.

## Substrate

Slidev → YouTube video, same as chips: the pipeline is proven and the audience
is there. The format innovation is entirely in the design system above, not the
substrate. The interactive companion diagram is a cheap post-video decision
once the SVG states exist; it must not complicate the build.

## Open questions (deliberately unresolved)

- **Upstream boundary.** Does the course start at the transmission corridor, or
  one step earlier at generation (gas turbines, nuclear PPAs, behind-the-meter
  plants)? Interconnection-queue drama argues for including generation; runtime
  argues against. Not yet decided.
- **Runtime target.** Unset until the segment list exists.
- **Act inventory and segment list.** Deliberately not sketched yet — the master
  diagram should be designed first, and segments derived from its zoom states,
  not the reverse.
- **Chips retention data.** Publishing chips and reading its retention curve
  (especially through the data-center segment) remains the cheapest information
  available before heavy investment here.
