# Rehearse the teaching sample

[Teaching endpoint](teach.html) · [Student exploration](sample.html) · [Written lesson](sample-reading.html)

Teach **without recording first** to find gaps in understanding and improve flow.
The ten-scene 800 V sample is the current presentation prototype. Allow roughly
fifteen minutes for explanation, predictions and discussion, then revise that
provisional allowance from the dry run. The remaining reading lessons need their
own authored visuals and rehearsal; current production priorities are in the
[filled-in course template](COURSE_REVIEW.md#next-teaching-step).

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
DC voltage and final conversion-loss control. All modes share the calculations.
Teaching mode is a presentation choice, not authentication or access control.

## Test the revised explanation

Glance at the speaking bullets, then explain each visual in your own words.
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
5. **Complete path:** explicitly move the fixed 100 kW boundary to the final useful
   DC load. Both alternatives start at the same facility AC supply. Downstream
   conversion losses raise feeder power and its calculated heat. At the illustrative
   defaults, DC uses about 1.144 kWh less input over one hour. Raising total DC
   conversion loss from 3 to 6 kW makes DC use about 1.875 kWh more. These assumed
   losses are not manufacturer efficiencies; cooling and other losses are excluded.
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
the complete-path comparison. Repetitive recording-setup advice is omitted from
the notes.

Use the [teaching standard](TEACHING_STANDARD.md) when revising source material.
[TESTING.md](TESTING.md) records automated and browser verification; those checks
do not replace this rehearsal or establish comprehension and delivery quality.
