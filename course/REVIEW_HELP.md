# Review the teaching sample

Kian's first feedback on 2026-09-06 identified too much text and an unclear
teaching workflow. The revised presentation was directionally useful. Subsequent
feedback on 2026-09-08 established the following:

- The first teaching pass will be an **unrecorded dry run** to identify knowledge
  gaps and improve the eventual recorded delivery.
- Repetitive recording-setup advice does not belong in the presenter notes.
- The default student experience should not display instructor controls.
- The 150 kW feeder / 160 kW load drawing looked like a real operating transfer,
  although it was intended as an impossible requested load.
- Kian clarified that the intended comparison was 480 V AC versus 800 V DC.
  The earlier 48 V DC premise was a misunderstanding and has been replaced.
- Rack units were missing from the explicit terminology teaching.
- The later copper/space discussion showed that energy savings had become the
  sample's apparent purpose. The 2026-09-09 revision makes copper and equipment
  placement visible first, with efficiency treated as a separate comparison.

The [teaching endpoint](teach.html) now supports the dry run. The default
[student sample](sample.html) offers the same visual reasoning with optional
explanations and no instructor controls. Presenter notes open from teaching mode.
The [full explanation](sample-reading.html) remains available for reference.

## What to rehearse next

1. Count three equal copper lengths versus two at the same 100 kW received.
   Explain the one-third material reduction and its equal-geometry assumption.
2. Compare current at 100 kW received: 480 V balanced three-phase AC gives
   about 120.3 A per line, while 800 V DC gives 125 A per conductor. Explain
   line-to-line RMS voltage and the power-factor-one assumption.
3. With 10 mΩ per conductor, add heat across three AC conductors or two DC
   conductors. Explain why 28% less conductor heat is neither less current
   per conductor nor a 28% reduction in facility electricity.
4. Trace conversion placement across the three functional diagrams. Identify
   released rack space and where the equipment moved; distinguish sidecar space
   from conversion located outside the hall.
5. In the complete-path comparison, move the fixed 100 kW boundary to the final useful
   DC load. Explain why downstream conversion losses increase feeder power and
   conductor heat. Reveal the required inputs, then raise total DC conversion
   loss from 3 to 6 kW and explain the reversal.
6. At `#capacity-check`, predict what doubling delivered DC power changes at
   fixed voltage and conductor geometry. Explain twice the current, four times
   the modeled heat, and why usable capacity still needs equipment evidence.

The complete-path model assumes conversion losses and calculates conductor heat from the
power each feeder must deliver. Both paths begin at the same facility AC supply
boundary. At the defaults, DC requires about 1.144 kWh less input over one hour;
with 6 kW total DC conversion loss, it requires about 1.875 kWh more. Cooling,
other losses and voltage compatibility are excluded. These are teaching
assumptions, not manufacturer efficiencies or a universal AC/DC ranking.
The revised premise and ending await another dry run.

Use [TEACHING_STANDARD.md](TEACHING_STANDARD.md) to carry successful changes into
other domains. Record comprehension evidence before claiming the format works
throughout the course; the other lessons still need their own authored visuals.

For rack units, see [A rack upgrade is an interface negotiation](index.html#d06-rack-migration):
U and usable height, the 19-inch mounting format, an original 42U allocation,
independent fit/service constraints and the distinction from OCP OpenU.

Record the step where the explanation stops being clear, the missing term or
mechanism, and the change needed. Expert review of electrical protection,
thermal/control boundaries and commissioning is still needed before final
recording. No outreach has been sent on Kian's behalf.

[TESTING.md](TESTING.md) records automated and browser verification. Those checks
do not replace the dry run or establish comprehension and delivery quality.
