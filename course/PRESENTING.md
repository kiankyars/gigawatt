# Rehearse the teaching sequences

[800 V teaching view](teach.html) · [Student exploration](sample.html) · [Written lesson](sample-reading.html)

## The next pass

The reviewed **UPS** and **800 V** sequences now establish the direction for the
rest of the course. Keep reporting specific confusing scenes, but there is no
need to reread both sequences before work advances.

Next is **[cooling: from chip to outdoor air](prototypes/cooling-format.html)**,
a new teaching draft spanning selected D10/D11 concepts. It follows heat through
the cold plate, two isolated liquid loops and outdoor rejection, then changes
flow to show the consequence. This tests the approach on a different physical
mechanism rather than copying the electrical diagrams.

1. Teach the new sequence aloud without recording. Let the visual carry the
   explanation; notes are optional.
2. Send the slide number or URL and the exact point that confused you, seemed
   wrong or needed a clearer picture.
3. We revise that section, then continue through the domain map's dependencies.
   The domains track coverage; they do not impose fifteen identical slide decks.

The expanded reader is reference material, not a script to narrate or a reading
assignment before each review. If cooling needs more background, use
[the CDU explanation](index.html#d10-cdu-interfaces) and
[heat rejection](index.html#d11-heat-rejection). The cooling sequence does not yet
cover all of D10 or D11. A sequence can be ready for feedback while its broader
domain remains unfinished.

## What carries into every chapter

Use the [teaching standard](TEACHING_STANDARD.md): a concrete question, a visible
mechanism, one controlled change and its engineering consequence. Keep one clear
headline and essential object labels. Put deeper explanations in the reference,
not below the diagram. The facility context stays recognizable as the topic
changes. Each next sequence needs its own model and visual; paragraph-to-slide
conversion is not the production method.

## UPS, bypass and redundancy

Open [the UPS sequence](prototypes/ups-format.html). Its seventeen scenes cover
selected parts of D05: location and form, normal and battery operation, capacitor
buffering, generator handoff, static and maintenance bypass, then N, N+1, N+2,
2N and 2(N+1).

Use the diagram controls to remove modules, isolate paths or lose a shared bus.
The path and capacity comparisons use a 100 kW load and hypothetical 50 kW
modules; the final changed case raises demand to 150 kW without adding equipment.
These functional states are not equipment switching instructions.

The capacitor scene declares a separate 1 MW DC-bus model: 0.20 F, initially
800 V, with shutdown at 700 V. **Capacitor only** reaches that threshold after
15 ms. In the **assumed 10 ms battery ramp**, battery power rises from time zero
and the capacitor covers the overlapping deficit. Neither is a timing specification
for the illustrated UPS product.

Use **Next / →**, **Back / ←**, the short-label selector and diagram buttons.
The optional [rehearsal endpoint](prototypes/ups-format.html?rehearse=1) opens a
synchronized cue window. No notes are required for the main teaching route.

## AC/DC foundations and 800 V

Open [the twelve-scene teaching sequence](teach.html). It covers selected D06
ideas with D01/D04 foundations: closed DC loop, AC power dips, three balanced
phases, line-to-line voltage, copper and current, then conversion placement.

The comparisons retain **100 kW received power** unless the scene explicitly
changes the boundary. At power factor one, 480 V balanced three-phase AC needs
about 120.3 A per line; 800 V two-wire DC needs 125 A per conductor. Equal copper
length and cross-section are a material comparison, not a qualified cable design.
The 28% conductor-heat reduction additionally assumes 10 mΩ per conductor; it is
not a facility-efficiency claim.

On the voltage scene, **Why not 960 V?** shows three 480 V RMS pair measurements.
Their signed instantaneous differences sum to zero. All three phase conductors
are live; the third is not ground.

**Slide 9 — Supply path** shows conventional voltage reduction before the
controlled AC/DC converter. The point is the maturity and practicality of
step-down plus lower-voltage conversion. Direct medium-voltage conversion is
possible but changes the semiconductor, insulation and control problem.
**Converter losses** is optional and belongs to the controlled AC/DC supply,
not the upstream transformer or UPS double-conversion path. The assumed 98%
efficiency gives 102.04 kW in, 100 kW out and 2.04 kW heat.

Finish by tracing which copper is removed, where the converter moves and what
rack space is released. The staged dates are SemiAnalysis's May 2026 forecast,
not a claim that all data centers follow that schedule. A sidecar still occupies
space; rack space released is not automatically net hall area saved.

## Views and controls

| View                  | Purpose                                                    |
| --------------------- | ---------------------------------------------------------- |
| `sample.html`         | Student visuals with exploration and optional explanation  |
| `teach.html`          | The same visuals with fullscreen and optional paired notes |
| `sample-notes.html`   | Brief cues; open from teaching mode to synchronize         |
| `sample-reading.html` | Full explanation, derivations and sources                  |

Use **Next / →**, **←** and **R** for reveal. Teaching mode adds **P** for notes and
**F** for fullscreen. A focused slider uses arrow keys to change its value.
Paired notes share the scene and interactive state. The website automatically
follows the device's light/dark setting, including changes while it is open.

[TESTING.md](TESTING.md) records browser and numerical checks. Those checks support
a working visual; the dry run reveals whether it teaches clearly.
