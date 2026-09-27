# The servers stay powered. The service does not.

**16. Putting an AI Factory Together · Optional practice**

Combine a power budget, an energy budget and a separately supplied cooling path. Identify exactly what the evidence can establish.

**Driving question:** Can this facility sustain useful work through the specified utility interruption?

## Start with a dependency diagram, not a battery runtime

A hall is delivering a steady 2 MW information technology (IT) load, the power drawn by its servers, storage and network equipment, when its utility supply is interrupted. The IT bus has a battery inverter, but the facility-loop pumps are on a different electrical bus. The diagram in the project pack says redundant power; it does not state which auxiliaries share that redundancy. Your first task is to turn that phrase into a list of actual supply paths. Draw the IT bus, its battery path, the rack cooling devices, the facility-loop pumps, the heat-rejection plant and the controllers that coordinate them. Treat an untraced auxiliary as an unresolved dependency until its supply is shown.

The exercise provides a 2.5 MW inverter and 600 kWh of usable stored direct-current (DC) energy. The inverter converts it to alternating current (AC) for the IT bus, and this discharge path is 90% efficient at the stated operating point. The battery energy can therefore support the specified IT power for a bounded duration. Yet those two checks do not establish whether a thermal limit is reached first. The facility-loop pumps lose their supply immediately. Some components may retain electrical power and keep circulating a local loop while the downstream heat path has already stopped. A circulating local loop keeps warming until the path to the outdoor plant runs again.

## Write a timeline whose unknowns stay unknown

At time zero the utility path is lost. Assume, for this exercise only, that the IT inverter transfers without exceeding the IT equipment's allowed interruption. A separately supplied controller remains available and records the pump supply loss. At ten minutes the generator path is available, but an additional two minutes is required by the supplied restoration sequence before the full cooling path can be established. These are synthetic scenario inputs, not recommended switching delays or equipment guarantees. Keep the sequence as evidence to evaluate, not instructions to perform.

You can compare the twelve-minute electrical support requirement with the available energy: the restoration needs 2,000 kW × 0.2 h = 400 kWh of the battery's 540 kWh of AC energy. The heat has a number too. Over the same twelve minutes the racks turn those 400 kWh into heat, and with the facility-loop pumps unpowered that heat accumulates in the hall's coolant and equipment. For scale, 400 kWh is 1,440 megajoules (MJ), enough to warm 10 m³ of water by about 34 K. Whether the hall can absorb it depends on coolant inventory, operating temperatures, effective thermal capacities, flow after the disturbance, device limits and control behavior, so a safe twelve-minute thermal bridge can be calculated only once those are known. The correct engineering answer can therefore contain both a numerical pass and an unresolved service conclusion. Specify the missing measurements and an acceptance test that would resolve them. A decision to reduce workload should follow the actual operating limits and an authorized control sequence, which a battery calculation cannot supply.

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

## When the situation changes

Trigger: A project report substitutes the 16.2-minute battery duration for twelve minutes of service ride-through.

Mechanism: The racks keep turning 2 MW into heat while the facility-loop pumps are unpowered: over the 12-minute restoration that is 2,000 kW × 0.2 h = 400 kWh of heat with no path to the outdoor plant.

Response: Correct the report and require an integrated disturbance test that tracks coolant and device temperatures against their limits through the full 12-minute sequence.

## Apply the idea

A redesign places an additional 0.2 MW of required cooling auxiliaries on the same battery system. All energy and conversion assumptions remain fixed. What are the new power check and ideal duration? What conclusion still needs evidence?

<details>
<summary>Reveal the worked answer</summary>

2.2 MW is below the 2.5 MW inverter rating. Duration is 540/2,200 h = 14.73 minutes, approximately.

The energy margin shrinks because the battery now supports both loads. This can sustain the specified electrical loads for twelve minutes in the simplified model. Whether cooling, controls and IT stay within their actual transient operating limits still needs an integrated test and thermal evidence.

</details>

**The idea to keep:** Electrical ride-through is one dependency of continued service. It is not a prediction of thermal ride-through.

## Sources

- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — ASHRAE · Reviewed 2026-09-06. ASHRAE's AI data-center framework guidance on commissioning and validating integrated facility performance.
