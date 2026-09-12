# Rehearse the teaching sequences

[Opening section](prototypes/orientation-format.html?teach=1) · [800 V](teach.html)
· [UPS](prototypes/ups-format.html) · [Cooling](prototypes/cooling-format.html?teach=1)

## The next pass

The next dry run is **[D01 — Data center overview](prototypes/orientation-format.html?teach=1#three-paths)**.
Its thirteen scenes tour the three paths, white/gray space, generation,
transmission, campus distribution, backup power, GB300 hardware, chip-to-cluster
scale, network and cooling paths, then rating, LLM batch scheduling and PUE.
It applies the approach reviewed in UPS, 800 V and cooling.
The [student route](prototypes/orientation-format.html) has the same diagrams and
experiments; each scene's explanation and sources open on demand.

1. Teach the new sequence aloud without recording. Let the visual carry the
   explanation; notes are optional.
2. Send the slide number or URL and the exact point that confused you, seemed
   wrong or needed a clearer picture.
3. We revise that section, then continue through the domain map's dependencies.
   The domains track coverage; they do not impose fifteen identical slide decks.

This is the opening teaching section, not all of D01/D02. Source-claim evaluation
remains in the D01 reference; D02's workload brief and service requirements are
the next teaching section to build. No need to reread the three reviewed sequences
or the entire manuscript before this pass.

D08's written networking section covers copper, fiber, pluggable and co-packaged
optics, scale-up/scale-out, plus campus entrances, meet-me rooms, carrier handoff,
DCI/WAN and shared-route risks. Its teaching sequence remains to be authored.

## Cooling reference sequence

The **[cooling presentation](prototypes/cooling-format.html)** has fourteen scenes
covering why liquid cooling is useful, CRAH and rack capture methods, the sensible
heat balance, CDU approach, a real CoolIT CHx2000, dry/wet rejection, weather,
chillers, hybrid and economizer modes, and CDU redundancy, independent facility
paths and reduced-power operation after a cooling failure.

**D10 and D11 in the expanded reader are the reference chapters.** They provide
derivations, source discussion and additional detail; the presentation should
teach its selected topics without requiring the audience to open those chapters.
The flow experiment keeps heat load fixed: double coolant flow and watch the
temperature rise halve. The air-versus-water comparison separately explains why
liquid cooling is useful. Further domain detail remains
in [D10](index.html#d10-local-thermal-paths) and [D11](index.html#d11-heat-rejection).
[The revised ending](prototypes/cooling-format.html?teach=1#lost-flow) starts with
spare CDUs, then independent facility paths, then the load reduction that can fit
remaining cooling capacity. Its kW values are hypothetical qualified operating
points, not manufacturer ratings or a prediction of safe response time.
This expanded presentation is ready for a dry run, not a completed course release.

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

Open [the thirteen-scene teaching sequence](teach.html). It covers selected D06
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
