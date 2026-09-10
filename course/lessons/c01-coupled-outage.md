# The servers stay powered. The service does not.

Generated reading view. Edit [`course/expansion/capstones.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/capstones.json), lesson `c01-coupled-outage`, then run `uv run gigawatt-expand`.

**capstone · Authored draft · Objectives:** D05.1, D05.2, D05.3, D14.5

Combine a power budget, an energy budget and a separately supplied cooling path. Identify exactly what the evidence can establish.

**Driving question:** Can this facility sustain useful work through the specified utility interruption?

## Start with a dependency diagram, not a battery runtime

A hypothetical hall is delivering a steady 2 MW IT load when its utility supply is interrupted. The IT bus has a battery inverter, but the facility-loop pumps are on a different electrical bus. The diagram in the project pack says redundant power; it does not state which auxiliaries share that redundancy. Your first task is to turn that phrase into a list of actual supply paths. Draw the IT bus, its battery path, the rack cooling devices, the facility-loop pumps, the heat-rejection plant and the controllers that coordinate them. An untraced auxiliary is an unresolved dependency, not an assumed survivor.

The exercise provides a 2.5 MW inverter and 600 kWh of usable stored DC energy before conversion. The discharge path is 90% efficient at the stated operating point. The battery energy can therefore support the specified IT power for a bounded duration. Yet those two checks do not establish whether a thermal limit is reached first. The facility-loop pumps lose their supply immediately. Some components may retain electrical power and keep circulating a local loop while the downstream heat path has already stopped. Sustaining one loop is not equivalent to rejecting heat to the environment.

## Write a timeline whose unknowns stay unknown

At time zero the utility path is lost. Assume, for this exercise only, that the IT inverter transfers without exceeding the IT equipment's allowed interruption. A separately supplied controller remains available and records the pump supply loss. At ten minutes the generator path is available, but an additional two minutes is required by the supplied restoration sequence before the full cooling path can be established. These are synthetic scenario inputs, not recommended switching delays or equipment guarantees. Keep the sequence as evidence to evaluate, not instructions to perform.

You can compare the twelve-minute electrical support requirement with the available energy. You cannot calculate a safe twelve-minute thermal bridge without coolant inventory, operating temperatures, effective thermal capacities, flow after the disturbance, device limits and control behavior. The correct engineering answer can therefore contain both a numerical pass and an unresolved service conclusion. Specify the missing measurements and an acceptance test that would resolve them. A decision to reduce workload should follow the actual operating limits and an authorized control sequence; this course does not invent one from a battery calculation.

## Worked example: Two passes do not establish service continuity

- Synthetic constant 2 MW IT load; no load shedding in the numerical calculation.
- 2.5 MW inverter, 600 kWh usable DC storage, 90% discharge-path efficiency.
- Cooling pumps lose power; the full restoration sequence takes 12 minutes. Thermal storage and limits are unspecified.

1. Check instantaneous power — 2.5 MW ≥ 2 MW — The stipulated inverter can supply the IT load at this operating point.
2. Convert stored energy to usable AC energy — 600 kWh × 0.90 = 540 kWh — Apply the stated discharge efficiency once.
3. Calculate ideal electrical duration — 540 kWh / 2,000 kW = 0.27 h = 16.2 min — Power and energy are checked at consistent boundaries.
4. Budget the restoration interval — 2,000 kW × (12/60) h = 400 kWh AC — The electrical inventory has 140 kWh AC remaining under the supplied assumptions.
5. State the service conclusion — Electrical support passes; thermal support is unestablished — The missing heat path prevents a justified claim of twelve minutes of useful operation.

**Result:** The IT electrical path has 16.2 ideal minutes, but the available data do not establish continued service for the twelve-minute restoration sequence.

**Model boundary:** No thermal transient, battery ageing, inverter overload curve, protective coordination or actual transfer performance is inferred.

## The tradeoff

Choice: Add electrical support for the missing cooling auxiliaries.

Benefit: Remove one dependency that previously failed immediately.

Cost: The supported load and usable energy budget change, and all downstream heat-path and control dependencies still require testing.

## When the situation changes

Trigger: A project report substitutes calculated battery duration for service ride-through.

Mechanism: IT power remains available while an unprotected auxiliary breaks heat removal.

Response: Correct the report, identify sensor and supply boundaries, and require an integrated disturbance test with explicit acceptance limits.

## Apply the idea

A redesign places an additional 0.2 MW of required cooling auxiliaries on the same battery system. All energy and conversion assumptions remain fixed. What are the new power check and ideal duration? What conclusion still needs evidence?

<details>
<summary>Reveal the worked answer</summary>

2.2 MW is below the 2.5 MW inverter rating. Duration is 540/2,200 h = 14.73 minutes, approximately.

The energy margin shrinks because the battery now supports both loads. This can sustain the specified electrical loads for twelve minutes in the simplified model. Whether cooling, controls and IT stay within their actual transient operating limits still needs an integrated test and thermal evidence.

</details>

**The idea to keep:** Electrical ride-through is one dependency of continued service. It is not a prediction of thermal ride-through.

## Sources and reading boundaries

- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Commissioning provides the context for testing integrated facility behavior; the numerical case is original. Read 2026-09-06. Public framework guidance. Referenced standards and project-specific acceptance procedures were not reviewed; no field procedure is prescribed.
