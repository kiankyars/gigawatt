# Rehearse the teaching sequences

[Primer](prototypes/terminology-format.html?teach=1)
· [Data center overview](prototypes/orientation-format.html?teach=1)
· [Workloads and requirements](prototypes/workload-format.html?teach=1) · [800 V](teach.html)
· [Siting and generation](prototypes/siting-format.html?teach=1)
· [Rack inlet to chip](prototypes/rack-power-format.html?teach=1)
· [UPS](prototypes/ups-format.html) · [Cooling](prototypes/cooling-format.html?teach=1)

## The next pass

The current edits and technical checks are complete;
these are the next author-review targets.

1. Finish **Chapter 2** by reviewing only its changed slides: the
   [TPU cluster-network example](prototypes/orientation-format.html?teach=1#network-preview),
   the CDU terminology and the capacity title. Its earlier rack-power and rear-busbar
   revisions remain in place.
2. Review the revised **[Chapter 3: Workloads and requirements](prototypes/workload-format.html?teach=1)**
   from its new introduction. Its 18 slides connect one GB300 NVL72 to model
   memory, token service and the power trace that supply design needs.
3. Then continue to **[Chapter 4: Siting, grid connection and supply](prototypes/siting-format.html?teach=1)**,
   the 26-slide draft with gas generation, combined cycle, dispatch and operating-duty economics.

Chapter 3 keeps the conditional staggering example immediately beside its
dependency limitation. Its ending now builds the workload brief; the old two
threshold quizzes are removed. Training/inference, memory and energy comparisons
are shown together, with power over time carrying the electrical explanation.

For each change, send the slide number or URL and the specific confusion. Teach
aloud without recording; notes are optional. The [chapter review tracker](COURSE_REVIEW.md#chapter-review-tracker)
keeps implementation, technical checks, addressed feedback and final acceptance
separate. Mark a chapter accepted only when Kian says its review is finished.
**Do not restart the unchanged Primer.** Its earlier requested revisions are
implemented; a completed final author pass has not been recorded.

The later [Tier comparison](prototypes/ups-format.html#tier-topology) and
[rack inlet to chip](prototypes/rack-power-format.html?teach=1) are new additions
inside previously iterated topics. Review those additions when reaching those
chapters; the earlier UPS and 800 V slides do not need another general pass.

Available decks cover the Primer, overview, workloads, siting, and selected UPS,
rack-power, 800 V and cooling topics. The remaining chapters have reader drafts;
their own presentations still need to be authored. The [catalog](teaching-sequences.json)
owns presentation availability and the tracker owns review status.

## Cooling reference sequence

The **[cooling presentation](prototypes/cooling-format.html)** has fourteen scenes
covering why liquid cooling is useful, CRAH and rack capture methods, the sensible
heat balance, CDU approach, a real CoolIT CHx2000, dry/wet rejection, weather,
chillers, hybrid and economizer modes, and CDU redundancy, independent facility
paths and reduced-power operation after a cooling failure.

**Chip and rack heat capture and Heat rejection, climate and water in the expanded reader are the reference chapters.** They provide
derivations, source discussion and additional detail; the presentation should
teach its selected topics without requiring the audience to open those chapters.
The flow experiment keeps heat load fixed: double coolant flow and watch the
temperature rise halve. The air-versus-water comparison separately explains why
liquid cooling is useful. Further domain detail remains
in [Chip and rack heat capture](index.html#d10-local-thermal-paths) and [Heat rejection, climate and water](index.html#d11-heat-rejection).
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

Open [the UPS sequence](prototypes/ups-format.html). Its 21 scenes cover
selected parts of Continuity, storage and protection: location and form, normal and battery operation, capacitor
buffering, generator handoff, static and maintenance bypass, then N, N+1, N+2,
2N and 2(N+1), then Tier topology, backup-generation requirements, availability
budgets and a dated commercial investment case. Tier is not an uptime percentage:
four nines allows 52.56 minutes in a 365-day year, and Tier I already includes an
engine generator. Generation capacity does not mean continuous on-site generation.

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

The eleven-scene [rack inlet to chip sequence](prototypes/rack-power-format.html?teach=1)
establishes the local power path first: PSU modules, the rear rack busbar,
intermediate conversion, point-of-load regulation, current and finite ripple.
It then connects storage location to the supported load, overlapping buffer/source
response, a specific ORv3 BBU shelf and repeated-burst recharge. The 15 kW BBU
example is a six-module 5+1 configuration, not a battery prescription for NVL72.
Manufacturer cases and original board/buffer models are labeled separately.

Open [the thirteen-scene teaching sequence](teach.html). It covers selected Rack power and the 800 V DC transition
ideas with Data center overview/Campus and building power distribution foundations: closed DC loop, AC power dips, three balanced
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

### Primer opening and case-study use

The primer begins with the circuit and ends with the PUE example. There is no
welcome, roadmap, closing quotation or link to another chapter. Its revised
sequence includes waveform shapes, power factor and UPS types, with concrete
memory, networking and heat examples. Planned cues target about twenty minutes;
rehearsal establishes the actual pace.

Open `prototypes/case-studies.html?teach=1` for the short case treatments. Use each
case in its named domain, invite a prediction before revealing the explanation,
and return to its linked reader lesson for the derivation and source limits.
The accompanying Abilene reference is a dated campus case, not a claim that all
hypothetical equipment values represent the site.
Standalone cases are authored, but their integration into the relevant chapter
presentations is still pending. Before rehearsing a new chapter, use the
[required section handoffs](TEACHING_STANDARD.md#required-section-handoffs) to
check its case, chapter handoff and recurring-campus treatment. Record remaining
work in the [existing production follow-ups](COURSE_REVIEW.md#next-teaching-step).
