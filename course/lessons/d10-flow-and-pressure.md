# Flow arithmetic is only the first pump question

**D10 · Authored draft · Objectives:** D10.1, D10.2

Derive a single-phase flow requirement, then add pressure drop, pump operating point and branch maldistribution.

**Driving question:** How much liquid transports the heat, and can that flow reach every required branch?

## Derive the heat-transport equation

For a single-phase liquid with approximately constant specific heat, each kilogram absorbs cp times its temperature rise in energy. Multiplying by mass flow rate gives heat-transfer rate: Qdot = mdot × cp × delta T. Keep heat rate distinct from liquid flow, even when a drawing uses the same letter Q for both. If heat is in kilowatts and cp in kilojoules per kilogram-kelvin, mass flow comes out in kilograms per second. Convert to volume flow only after specifying density.

The temperature rise is the difference between the liquid leaving and entering the load. It is not the absolute supply temperature, nor the approach temperature across a heat exchanger. A larger allowed rise reduces required mass flow for the same heat, but warms the return and changes temperatures along the load path. A smaller rise needs more flow and can increase hydraulic demand. The acceptable range must come from the equipment’s thermal requirements and the complete system design.

## Ask what pressure difference produces that flow

A pump supplies pressure difference that drives liquid through restrictions. Pipes, hoses, valves, filters, connectors and cold plates all contribute pressure drop. A pump has a relationship between flow and available pressure; the system has a relationship between flow and required pressure. Their intersection gives an operating point under the stated conditions. Selecting a pump from a maximum free-flow number ignores the pressure required by the installed circuit.

For a simplified friction-dominated circuit, pressure drop can be approximated as proportional to the square of flow over a limited range. Hydraulic power is pressure difference times volume flow. With that approximation, changing flow can have a strong effect on pumping demand. Actual pump and system curves, fluid viscosity, controls and component limits still govern. A glycol mixture cannot inherit a water calculation without checking its density, heat capacity and viscosity at the intended conditions. Treat fluid identity as part of the interface, not a cosmetic label.

## Parallel branches can hide a local shortage

A manifold divides total flow among branches according to their hydraulic resistances and available pressure difference. Equal branch heat does not guarantee equal branch flow. A partly blocked filter, a connector restriction or a changed valve position can reduce one branch’s flow while another receives more. Aggregate flow at the CDU can look acceptable even as a device on the restricted branch approaches its thermal limit. This is why the flow ledger must identify branches as well as totals.

Temperature sensing helps reveal the consequence, but a mixed return temperature can hide the hottest stream. If one branch leaves at a high temperature and mixes with cooler liquid from other branches, the average may remain within a broad alarm threshold. Local device temperatures, branch flow or differential-pressure information can therefore be more diagnostic than one rack-average reading. The right sensor set depends on the failure modes and response time the system must manage.

## Include pump energy and qualification boundaries

Electrical power consumed by pumping eventually appears as heat somewhere within the wider system, but its allocation depends on the motor and fluid boundaries. If all pump input is assigned to the liquid in a simplified balance, add it to the heat that the next exchanger must transfer. If part leaves to room air, track that path separately. The first flow calculation often neglects this small term to isolate the main mechanism; the final engineering ledger should state whether it has been included.

A qualified loop also needs compatible wetted materials, fluid chemistry, cleanliness and service procedures. More flow is not a universal response to every temperature problem: it may exceed a component’s allowed pressure, velocity or pumping envelope while leaving poor thermal contact unresolved. Use the supplied curves and limits to distinguish a hydraulic shortage from a local heat-transfer defect before changing an operating point.

## Worked example: Heat balance meets two synthetic curves

- The loop captures 84 kW into single-phase water modeled with cp = 4.2 kJ/(kg·K) and density = 1 kg/L.
- The desired load-side temperature rise is 10 K. Pump heat is excluded from this first transport calculation.
- With volume flow q in L/s, the invented pump curve is delta p = 160 − 10q² kPa and system curve is delta p = 30q² kPa. Overall pump efficiency is assumed 60%.

1. Find required mass and volume flow — 84 / (4.2 × 10) = 2 kg/s = 2 L/s = 120 L/min — The specified fluid properties allow the mass-to-volume conversion.
2. Find the hydraulic operating point — 160 − 10q² = 30q²; q = 2 L/s — The two invented curves intersect at the required flow.
3. Find operating pressure difference — 30 × 2² = 120 kPa — The pump must supply this pressure difference across the declared circuit.
4. Calculate pump power — 120,000 Pa × 0.002 m³/s = 240 W hydraulic; 240 / 0.60 = 400 W electrical — Consistent SI units convert pressure times volume flow into watts.

**Result:** The synthetic pump and system deliver the heat-balance flow at 120 kPa with 400 W of modeled input.

**Model boundary:** These curves do not select real equipment. Fluid-property variation, branch balance, transient behavior, pressure limits and redundancy remain outside the example.

## The tradeoff

Choice: Allow a larger liquid temperature rise to reduce required flow.

Benefit: Potentially reduce hydraulic demand and the burden on piping and pumping.

Cost: Increase downstream fluid temperatures and potentially reduce device thermal margin; actual pump operation must be recalculated.

## When the situation changes

Trigger: One of four equal 21 kW branches receives only 0.25 L/s instead of 0.5 L/s.

Mechanism: Its modeled temperature rise doubles from 10 K to 20 K even if other branches remain normal.

Response: Use local temperature and hydraulic evidence to identify the restricted branch and follow the qualified isolation and restoration procedure.

## Apply the idea

If the entire 400 W pump input enters the liquid upstream of the exchanger, what heat must the exchanger reject and what is the overall temperature rise at 2 kg/s?

<details>
<summary>Reveal the worked answer</summary>

The exchanger transfers 84.4 kW, and the corresponding overall rise is 84.4 / (2 × 4.2) ≈ 10.048 K.

The small difference does not invalidate the first-pass calculation, but explicitly closing it prevents pump energy from disappearing between boundaries. A different motor-to-air heat allocation would require a separate air-path term.

</details>

**The idea to keep:** Heat capacity sets an energy-transport requirement; the hydraulic network determines the flow actually delivered.

## Sources and reading boundaries

- [Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) — CDU evaluation includes thermal conditions, technology-loop pressure head and facility-loop flow impedance. Read 2026-09-06. Selected performance and fluid-service sections reviewed; supplied synthetic pump curves are not extracted from the paper. Front matter has inconsistent date labels.
- [Open Compute Project — Cold Plate workstream](https://www.opencompute.org/wiki/Cooling_Environments/Cold_Plate) — The workstream separates cold-plate, loop, fluid and connector requirements. Read 2026-09-06. Index reviewed; linked loop-requirement PDF did not load during this pass and is not treated as audited.
