# Rehearse the teaching sequences

[Teaching endpoint](teach.html) · [Student exploration](sample.html) · [Written lesson](sample-reading.html)

## Your next feedback pass

1. **[UPS, bypass and redundancy](prototypes/ups-format.html): fifteen scenes,
   part of D05.** Start here to review the latest visual format. Explain each
   diagram aloud and try the failure/maintenance controls.
2. **[AC/DC foundations → 800 V](teach.html): thirteen scenes, the D06 sample
   with D01/D04 foundations.** Check whether the electrical primer makes the
   copper, current and conversion-placement comparisons clear.
3. For either sequence, send the **slide number (or its URL) and what confused you, seemed
   wrong or needed a clearer visual**. Teach without recording; notes are optional.
   We revise these sequences, then carry the settled approach into the next section.

These are reviewable teaching sequences, not finished domains. There is no need to
read the entire course or research library first. When an explanation needs more
depth, use the [UPS storage reference](index.html#d05-storage-power-and-time),
[UPS paths reference](index.html#d05-paths-and-transitions) or
[800 V written lesson](sample-reading.html). The UPS prototype contains newer
bypass and redundancy visuals than those draft reader lessons.

The website follows the device's light/dark setting automatically, including
changes made while the page is open. No website toggle is required.

## UPS, bypass and redundancy prototype

Open [the UPS sequence](prototypes/ups-format.html). Its fifteen scenes move from
the campus into one UPS, trace normal and battery operation, then compare forced
static bypass, external maintenance bypass, N, N+1, N+2, 2N and 2(N+1).
The product slide shows a real freestanding UPS cabinet and distinguishes its external
UPS battery from rack battery backup units (BBUs). The electrical room is the
placement chosen for this layout, not a universal rule.
The same 100 kW load and hypothetical 50 kW modules anchor the comparison.
Remove modules, isolate a route or fail the shared bus; finish by raising demand
to 150 kW without adding equipment. Let the changed paths and surviving capacity
carry the explanation.

Use **Next / →**, **Back / ←**, the scene selector and the diagram's buttons.
Notes are hidden by default. The optional [rehearsal endpoint](prototypes/ups-format.html?rehearse=1)
can open a separate synchronized cue window. The sequence should be teachable
without it. This is a teaching prototype for a dry run; it does not establish that
all of D05 is finished. Bypass drawings show completed functional states,
not an equipment switching procedure.

## Open and control the presentation

| Endpoint              | Use                                                                                                    |
| --------------------- | ------------------------------------------------------------------------------------------------------ |
| `sample.html`         | Default student visuals, prediction/reveal and optional explanations; no instructor controls           |
| `teach.html`          | Teaching visuals with fullscreen and a separate synchronized notes window                              |
| `sample-notes.html`   | Short speaking bullets, action cue and next-step context; open it from teaching mode to pair the windows |
| `sample-reading.html` | Full explanation, derivations and source limits for study or lookup                                    |

Use **Next / →** to advance, **←** to return and **R** to reveal or hide an answer.
Teaching mode adds **P** for notes and **F** for fullscreen. A focused slider uses
arrow keys to change its value. Paired notes synchronize the scene, answer state,
DC voltage and cycle position. All modes share the calculations.
Teaching mode is a presentation choice, not authentication or access control.

## Establish the electrical foundation

Before the copper comparison, teach the four new scenes: the DC closed loop,
one AC cycle, three balanced phases, and line-to-line voltage measurement.
Move the cycle slider to compare current direction with load power. The power band means **100 kW average received power** throughout the circuit examples.
The voltage-measurement slide then isolates the meter probes; L1 and L2 are both
live phases, and L3 is another live phase, not ground.
Single-phase instantaneous power pulses; its average is the comparison anchor.
The primer uses equivalent ideal resistor loads, then adds conductor losses
explicitly in the later comparison.

## Test the revised explanation

Explain each visual in your own words; use the optional speaking cues only if helpful.
The full explanation stays in the student reading view. Ask for a prediction before revealing an
answer, and use these checks to find where the explanation stops being clear:

1. **Copper:** compare three equal copper lengths with two at the same 100 kW
   received. Explain 33.3% less current-carrying copper under equal length,
   cross-section and material assumptions. This is not a qualified cable design.
2. **Current:** 480 V balanced three-phase AC gives about 120.3 A per line;
   800 V two-wire DC gives 125 A per conductor. Introduce line-to-line RMS voltage
   and power factor one. Fewer conductors does not mean lower current in each.
3. **Conductor heat:** at the additional idealization of 10 mΩ effective resistance
   per conductor, sum losses across three AC conductors or two DC conductors.
   The 28% reduction applies to this conductor-heat account, not facility electricity.
4. **Placement:** follow conversion from the rack to a sidecar or upstream power
   room. Identify released rack space and where equipment moved. A nearby sidecar
   still occupies space; moving a converter does not establish a net hall-area saving.
5. **Conversion:** distinguish conductor heating from loss inside the converter.
   Resistance, switching, magnetic components and auxiliaries dissipate power;
   the amount depends on equipment, loading, operating mode and temperature.
   The explicitly illustrative 98% converter needs 102.04 kW input for 100 kW
   output, leaving 2.04 kW as heat. This is not a measured AC/DC architecture advantage.
6. **Transfer:** at `#capacity-check`, double delivered DC power to 200 kW while
   holding 800 V and the conductors unchanged. Predict 250 A and 1.25 kW conductor
   heat: twice the current, four times the heat, unchanged copper by assumption.
   Explain why usable capacity still requires equipment, thermal and voltage-drop limits.

For rack terminology, review [A rack upgrade is an interface negotiation](index.html#d06-rack-migration):
U and usable height, 19-inch mounting, the illustrative 42U allocation, independent
fit/service constraints and OCP OpenU. Do not assume knowing the terms establishes
mechanical or electrical compatibility.

## Record what the dry run changes

Note the scene, the learner's exact question, the missing term or reasoning step,
and the revision needed. Resolve the gap, rehearse again, then ask for the mechanism
and changed-case answer. Mark which claims need technical review separately from
pacing or vocabulary feedback. Electrical protection, thermal/control boundaries
and commissioning still need review before final recording.

The revised format responds to Kian's feedback on excessive text, the separation
of student and teacher controls, the intended **480 V AC versus 800 V DC** premise,
and copper/space being obscured by the energy comparison. The former 150 kW feeder /
160 kW load drawing appeared to show an operating flow despite being intended as
an infeasible request; it has been removed. Its old `#feeder-transfer` link opens
the converter-loss example. Repetitive recording-setup advice is omitted from
the notes.

Use the [teaching standard](TEACHING_STANDARD.md) when revising source material.
[TESTING.md](TESTING.md) records automated and browser verification; those checks
do not replace this rehearsal or establish comprehension and delivery quality.
