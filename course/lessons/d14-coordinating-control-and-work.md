# The scheduler cannot negotiate with physics after the fact

**14. Controls, operations and reliability**

Separate fast local control, plant-level coordination and workload decisions, then account for the standby start time and any thermal buffer the operating limits allow.

**Driving question:** How should a workload change relate to equipment control and facility operating sequences?

## Three layers answer three different questions

A device controller acts on a local process variable through an actuator. For example, a specified controller may vary a fan or valve to keep a measured condition within its approved operating behavior. A facility sequence coordinates equipment states: which units are enabled, how capacity is staged and what happens under defined changes. A workload scheduler decides when and where jobs run. They may exchange information, but they do not have interchangeable responsibilities.

The US National Institute of Standards and Technology’s description of operational technology includes systems that monitor and change the physical environment. This matters because an apparently simple software request can ultimately influence pressure, temperature or power demand. A scheduler that sees unused accelerators may regard a new job as feasible; a facility sequence may still be bringing required capacity into a ready state. The gap is an interface question, not evidence that either layer should guess the other’s state.

Use explicit signals with understood semantics. Available capacity must specify its boundary, conditions and freshness. Ready must mean a defined physical state, not merely that a start command was sent. Acknowledge, executing and proven available can be different states. When information is missing, the operating policy should say how decisions are constrained. A cheerful green icon does not replace a supported state transition.

## Delays create an energy question as well as a capacity question

Existing work produces 4 MW of heat, and the running cooling removes 5 MW. A new job would add 2 MW, raising the heat input to 6 MW. Standby cooling can raise removal to 7 MW, but its start takes three minutes. If the job starts at once, heat input exceeds removal by 6 − 5 = 1 MW until the standby unit is ready. That heat has to go somewhere: it warms the coolant, the equipment and the room.

Energy is power multiplied by time, so the three-minute gap leaves 1 MW × 3/60 h = 0.05 MWh of heat above removal. No thermal buffer is specified for this site, so nothing allows that heat to accumulate, and the job waits for the standby start. Started at minute three, it meets 7 MW of removal with 1 MW to spare. The installed cooling is the same in both plans; only the order of events differs.

Extension: a site with a stated buffer. Suppose the operating envelope allowed 0.04 MWh of usable thermal buffer. A two-minute standby start would leave 1 MW × 2/60 h = 0.0333 MWh, which fits with 0.0067 MWh to spare. The three-minute start still leaves 0.05 MWh, 0.01 MWh more than the buffer holds. One extra minute turns a fit into a shortfall while the installed cooling stays the same, so capacity, readiness and transition time have to describe the same scenario before a load change is sequenced. A buffer figure covers energy only; local device temperatures, flow distribution and control stability need their own evidence.

## Coordinate before consuming the margin

One possible operating arrangement is to establish the required capacity before admitting the additional workload. Another may allow a documented staged ramp within the supported dynamic envelope. A third may relocate or defer work. These are choices to evaluate through the actual operating requirements. Their costs include waiting time, auxiliary energy, reserve usage and the availability required by the workload.

Overly aggressive reactions can also create interaction between layers. If a workload repeatedly starts and pauses around the same threshold while the plant repeatedly stages equipment, the combined behavior may be undesirable even when each rule appears sensible alone. Time delays, state persistence and different measurements can matter. Engineers set deadbands and controller gains from the real dynamic model and tests, which the simple energy arithmetic leaves out.

After a change, observe whether the intended state was achieved and whether service stayed within its requirement. Preserve the sequence of commands, measured responses and job behavior. If the expected transition does not occur, the record should make the difference visible. That feedback connects commissioning with operation: a new workload or control revision can create behavior not exercised in the original accepted configuration.

## Case: Google checks the optimizer at the local controller

Google’s 2016 system recommended cooling actions that operators then carried out. In its August 2018 account, DeepMind described the next step: an optimizer that controlled the cooling directly under operator supervision, evaluating sensor snapshots every five minutes. Proposed actions had to satisfy operator-defined constraints and pass another check locally before execution. Operators could return control to the existing on-site rules. That is a concrete separation between optimization, local enforcement and human authority; the five-minute interval is not a protective-response deadline.

DeepMind measured the result as cooling energy per unit of cooling delivered, in kilowatts per ton of cooling, against the historical baseline before AI control. Over nine months the improvement grew from about 12 percent to about 30 percent. That compares cooling energy for the same cooling output, which is a smaller quantity than the whole site’s electricity.

For our campus discussion, ask which measurements authorize a change, where an instruction can be rejected, and how the operator verifies the resulting state. The historical Google case supplies a control pattern, not an as-built Abilene implementation.

## Case: a staging sequence decides when the next chiller starts

Johnson Controls publishes a Metasys application note for a Guideline 36 chilled-water plant. Its sequence starts the next chiller stage when the running chillers stay above a part-load threshold: 80 percent for stages made only of positive-displacement chillers, and 90 percent when the current and next stages include constant-speed centrifugal chillers. Thresholds for variable-speed centrifugal chillers change with lift, the sequence also checks time and trend conditions, and temperature and pressure failsafes can stage up on their own.

These thresholds decide when adding a chiller is efficient. The reserve a data center keeps comes from three separate questions: the demand to serve, including its ramp; the capacity that can actually reach the load in the current weather, flow and failure case; and how long new equipment takes to start compared with the thermal storage that can bridge the gap. Spare heat-removal capacity in megawatts is usable capacity minus demand. Stored cold buys time instead.

## Case: Intel stored chilled water to cover a power outage

Intel IT’s September 2007 white paper describes two 24,000-US-gallon tanks of water held at 42°F (5.6°C), connected to a chilled-water system that supplies 55°F (12.8°C) water. The tanks were sized to keep cooling for seven minutes beyond the five minutes of full-load runtime on the uninterruptible power supply (UPS): twelve minutes in all. During a 2006 outage, lightly loaded servers ran for more than fifteen minutes; the stored water kept cooling throughout and removed residual heat afterward. Pumps and air-handler fans ran on backed-up power, which made the stored cooling usable.

Intel’s tanks are a physical thermal buffer of the kind the worked example lacks. For scale, the 0.05 MWh that the three-minute start would leave unremoved is the heat that warms about 8.6 tonnes of water by 5 K. A buffer covers a transition of known length, while steady heat removal still has to come from running equipment.

## Case: Google defers flexible work during grid events

In October 2023, Google described how it lowers data-center demand when a grid operator forecasts a local supply constraint. The notice reaches Google’s computing planning system, which sets hour-by-hour limits on non-urgent work at the affected sites for the duration of the event and lets that work run afterward, or on another grid when feasible. Google’s examples of work that can wait are YouTube video processing and adding new words to Google Translate, while Search, Maps and YouTube stay available. Google gives no megawatt figure for the reduction. Its local utility, the Northern Wasco County People’s Utility District (PUD), reports a day-ahead pilot with Google’s facilities in The Dalles, Oregon.

A checkpointable 4 MW batch job shows the arithmetic. It needs three running hours on top of a steady 20 MW, a grid event runs from 14:00 to 16:00, and the job must finish by 20:00. Started at 13:00 and run straight through, it finishes at 16:00 and holds the site at 24 MW for the whole event. Paused for the event, it runs from 13:00 to 14:00 and from 16:00 to 18:00: the same 12 MWh of work, 20 MW during the event, and a finish two hours before the deadline. The pause costs nothing only if the job keeps its progress, restarts without penalty and finds capacity afterward.

## Worked example: A three-minute start with no specified buffer

- Existing work produces 4 MW of heat; the new job adds 2 MW, so heat input would rise to 6 MW.
- Running cooling removes 5 MW. Standby cooling raises removal to 7 MW after a three-minute start.
- No thermal buffer is specified, so heat may not accumulate above removal.

1. Imbalance if the job starts now — 6 − 5 = 1 MW — Heat the running plant cannot remove accumulates in the coolant and equipment.
2. Heat left over the start — 1 MW × 3/60 h = 0.05 MWh — Power multiplied by duration gives the accumulated energy.
3. Allowed accumulation — 0 MWh < 0.05 MWh — With no buffer specified, starting at once has no allowance to draw on.
4. Start at minute three — 6 MW ≤ 7 MW — Once standby cooling is proven ready, the job runs with 1 MW of removal to spare.

**Result:** Hold the job until standby cooling is ready at minute three. Starting at once would leave 0.05 MWh of heat with no buffer specified to absorb it.

**Model boundary:** Energy arithmetic only, and the three-minute delay is an example rather than a vendor startup specification. Temperatures, rates of change and control behavior during the transition need their own evidence.

## The tradeoff

Choice: Prove extra physical capacity ready before admitting a job.

Benefit: No heat accumulates above removal. In the worked example, starting at once would leave 0.05 MWh over the three-minute start, with no buffer specified to absorb it.

Cost: The job starts three minutes later, and the plant then runs 7 MW of removal for 6 MW of heat.

## When the situation changes

Trigger: The scheduler treats a standby start command as proven available cooling capacity.

Mechanism: The job arrives during a transition whose duration or result is not yet established.

## Apply the idea

The new job adds 1.5 MW instead of 2 MW, so heat input rises to 5.5 MW; standby cooling still takes three minutes. How much heat accumulates if the job starts at once? Can it start before minute three with no specified buffer, and would the extension’s 0.04 MWh buffer hold it?

<details>
<summary>Reveal the worked answer</summary>

(5.5 − 5) MW × 3/60 h = 0.025 MWh. With no buffer specified the job still waits until minute three; a 0.04 MWh buffer would hold it with 0.015 MWh to spare.

Halving the imbalance halves the accumulated heat, but any accumulation exceeds a zero allowance. A supported load envelope therefore states the step size, its timing and the buffer it may use, not only a final megawatt total. The energy check still says nothing about temperatures or dynamics.

</details>

**The idea to keep:** Each control layer has a different objective and timescale. A load decision must respect the state the physical system can actually support.

## Sources

- [NIST SP 800-82 Revision 3: OT Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final) — csrc.nist.gov · Published 2023-09-28 · Reviewed 2026-09-06. OT includes physical-process monitoring and control and must account for reliability and performance needs.
- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — sre.google · Reviewed 2026-09-06. Monitoring should connect system behavior with externally visible service.
- [Google DeepMind — Safety-first AI for autonomous data centre cooling and industrial control](https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/) — Google DeepMind · Published 2018-08-17 · Reviewed 2026-09-17. Every five minutes, a supervisory AI evaluates sensor snapshots and proposed cooling actions. Low-confidence actions are excluded. The cloud evaluates operator-defined constraints; the local system independently checks instructions before implementation. Operators can exit to existing on-site rules.
- [Google — Supporting power grids with demand response](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption) — Google · Published 2023-10-03 · Reviewed 2026-09-14. Google sets hour-by-hour limits on non-urgent work during forecast grid events and runs it later or elsewhere; Northern Wasco County PUD reports a day-ahead pilot at The Dalles, Oregon.
- [Johnson Controls — Metasys Chilled-Water Plant for Guideline 36 Application Note: Stage-up part-load ratio (SPLRUP)](https://docs.johnsoncontrols.com/bas/r/Metasys/en-US/Chilled-Water-Plant-for-Guideline-36-Application-Note/1.0/Chiller-sequence-of-operations/Chiller-and-waterside-economizer-staging-determination-5.20.1-15/Stage-Up-Part-Load-Ratio-SPLRUP) — Johnson Controls · Reviewed 2026-09-26. The next chiller stage starts above 80 percent part load for positive-displacement stages and 90 percent when constant-speed centrifugal chillers are involved; variable-speed thresholds vary with lift, and failsafes can stage up on their own.
- [Intel IT — Thermal storage system provides emergency data center cooling, September 2007](https://www.intel.com/content/dam/doc/white-paper/intel-it-thermal-storage-system-provides-emergency-data-center-cooling-paper.pdf) — Intel · Published 2007-09 · Reviewed 2026-09-26. Two 24,000-US-gallon tanks at 42°F were sized to cool for seven minutes beyond five minutes of UPS runtime and carried a 2006 outage, with pumps and air-handler fans on backed-up power.
