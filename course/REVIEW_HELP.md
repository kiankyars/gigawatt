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
- The sample had not sufficiently distinguished its 48 V DC versus 800 V DC
  comparison from an AC-versus-DC architecture comparison.
- Rack units were missing from the explicit terminology teaching.

The [teaching endpoint](teach.html) now supports the dry run. The default
[student sample](sample.html) offers the same visual reasoning with optional
explanations and no instructor controls. Presenter notes open from teaching mode.
The [full explanation](sample-reading.html) remains available for reference.

## What to rehearse next

1. Explain why 100 kW delivered at 48 V DC and at 800 V DC requires different
   current. Identify where voltage is measured.
2. Explain the fixed-resistance conductor-loss comparison, then close input =
   delivered power + conductor heat. Nothing is created by the higher voltage.
3. Trace conversion placement across the three functional diagrams.
4. In the final, separately stipulated AC/DC delivery budgets, reveal the
   required inputs. Increase DC conversion loss from 3 kW to 6 kW and explain
   why the total-energy advantage reverses despite lower conductor loss.

The final comparison uses invented losses, not market measurements. It deliberately
shows both a DC advantage and a counterexample. It does not claim a universal
AC/DC winner. The revised premise and ending await another dry run.

For rack units, see [A rack upgrade is an interface negotiation](index.html#d06-rack-migration):
U and usable height, the 19-inch mounting format, an original 42U allocation,
independent fit/service constraints and the distinction from OCP OpenU.

Record the step where the explanation stops being clear, the missing term or
mechanism, and the change needed. Expert review of electrical protection,
thermal/control boundaries and commissioning is still needed before final
recording. No outreach has been sent on Kian's behalf.

[TESTING.md](TESTING.md) records automated and browser verification. Those checks
do not replace the dry run or establish comprehension and delivery quality.
