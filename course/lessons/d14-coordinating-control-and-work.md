# The scheduler cannot negotiate with physics after the fact

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d14-coordinating-control-and-work`, then run `uv run gigawatt-expand`.

**15. Controls, operations and reliability · Authored draft**

Separate fast local control, plant-level coordination and workload decisions, then account for a stipulated delay and thermal-energy buffer.

**Driving question:** How should a workload change relate to equipment control and facility operating sequences?

## Three layers answer three different questions

A device controller acts on a local process variable through an actuator. For example, a specified controller may vary a fan or valve to keep a measured condition within its approved operating behavior. A facility sequence coordinates equipment states: which units are enabled, how capacity is staged and what happens under defined changes. A workload scheduler decides when and where jobs run. They may exchange information, but they do not have interchangeable responsibilities.

NIST’s description of operational technology includes systems that monitor and change the physical environment. This matters because an apparently simple software request can ultimately influence pressure, temperature or power demand. A scheduler that sees unused accelerators may regard a new job as feasible; a facility sequence may still be bringing required capacity into a ready state. The gap is an interface question, not evidence that either layer should guess the other’s state.

Use explicit signals with understood semantics. Available capacity must specify its boundary, conditions and freshness. Ready must mean a defined physical state, not merely that a start command was sent. Acknowledge, executing and proven available can be different states. When information is missing, the operating policy should say how decisions are constrained. A cheerful green icon does not replace a supported state transition.

## Delays create an energy question as well as a capacity question

Consider a synthetic cooling system with 5 MW of currently available heat removal. A proposed workload raises heat input from 4 MW to 6 MW. A standby unit can add the required capacity, but the stipulated transition takes two minutes. During those two minutes, the heat imbalance is 1 MW if the active unit provides 5 MW. That mismatch must go somewhere: it accumulates in the modeled system, is handled by another stated path, or causes operating limits to be exceeded.

For this exercise alone, assume a validated usable thermal-energy buffer of 0.04 MWh over the permitted operating envelope. The two-minute mismatch requires 1 MW × 2/60 h = 0.0333 MWh. It fits that supplied scalar energy budget. The calculation does not prove local device temperatures, flow distribution or control stability, because a single buffer value does not describe them. Real authorization would need the full relevant operating evidence.

If the standby transition takes three minutes instead, the mismatch requires 0.05 MWh and exceeds the stipulated budget. A one-minute delay changes the result even though the eventual installed cooling capacity is unchanged. This is why a steady nameplate total is insufficient for sequencing a load change. Capacity, readiness and transition behavior must describe the same scenario.

## Coordinate before consuming the margin

One possible operating arrangement is to establish the required capacity before admitting the additional workload. Another may allow a documented staged ramp within the supported dynamic envelope. A third may relocate or defer work. These are choices to evaluate through the actual operating requirements; the lesson does not prescribe a field control sequence. Their costs include waiting time, auxiliary energy, reserve usage and the availability required by the workload.

Overly aggressive reactions can also create interaction between layers. If a workload repeatedly starts and pauses around the same threshold while the plant repeatedly stages equipment, the combined behavior may be undesirable even when each rule appears sensible alone. Time delays, state persistence and different measurements can matter. Engineers use the real dynamic model and tests to establish suitable logic. We do not select a universal deadband or controller gain from the simple energy arithmetic.

After a change, observe whether the intended state was achieved and whether service stayed within its requirement. Preserve the sequence of commands, measured responses and job behavior. If the expected transition does not occur, the record should make the difference visible. That feedback connects commissioning with operation: a new workload or control revision can create behavior not exercised in the original accepted configuration.

## Worked example: A two-minute transition consumes most of the stated buffer

- Synthetic step to 6 MW heat input; active removal is 5 MW.
- Standby readiness delay is exactly two minutes in the base case.
- A separately stipulated usable buffer is 0.04 MWh, and all other operating conditions are assumed met for this arithmetic check.

1. Temporary imbalance — 6 − 5 = 1 MW — Only heat not removed by the active capacity draws on the buffer.
2. Two-minute energy — 1 MW × 2/60 h = 0.0333 MWh — Power multiplied by duration gives accumulated energy.
3. Remaining scalar margin — 0.04 − 0.0333 = 0.0067 MWh — Only one-sixth of the original energy allowance remains in the model.

**Result:** The base transition fits the supplied energy budget; a three-minute transition does not.

**Model boundary:** The buffer is a hypothetical validated input, not a heat-capacity estimate or an asserted safe ride-through time for real equipment.

## The tradeoff

Choice: Prove extra physical capacity ready before admitting a job.

Benefit: It can avoid depending on an uncertain transition while the new load is already present.

Cost: It may delay useful work or operate auxiliary equipment before it is needed; the service brief determines whether that cost is worthwhile.

## When the situation changes

Trigger: The scheduler treats a standby start command as proven available cooling capacity.

Mechanism: The job arrives during a transition whose duration or result is not yet established.

Response: Apply the approved coordination policy, distinguish commanded from measured readiness and investigate the mismatch with time-aligned evidence.

## Apply the idea

The workload rises to 5.5 MW instead of 6 MW, while standby readiness takes three minutes. How much buffer energy is required?

<details>
<summary>Reveal the worked answer</summary>

(5.5 − 5) MW × 3/60 h = 0.025 MWh, below the supplied 0.04 MWh scalar budget.

The smaller half-megawatt mismatch more than compensates for the longer delay in this particular energy check. It still does not certify temperatures or dynamics. The result illustrates why a supported load envelope should specify ramp or step size and timing rather than only a final MW total.

</details>

**The idea to keep:** Each control layer has a different objective and timescale. A load decision must respect the state the physical system can actually support.

## Sources and reading boundaries

- [NIST SP 800-82 Revision 3: OT Security](https://csrc.nist.gov/pubs/sp/800/82/r3/final) — OT includes physical-process monitoring and control and must account for reliability and performance needs. Read 2026-09-06. Abstract scope reviewed; no detailed control tuning or security configuration is inferred. All timing and buffer values are original stipulated inputs.
- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — Monitoring should connect system behavior with externally visible service. Read 2026-09-06. Selected conceptual discussion reviewed; the plant/scheduler scenario is an original cross-domain teaching example.
