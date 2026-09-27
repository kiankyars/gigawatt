# Flow arithmetic is only the first pump question

**11. Chip and rack heat capture**

Derive a single-phase flow requirement, then add pressure drop, pump operating point and branch maldistribution.

**Driving question:** How much liquid transports the heat, and can that flow reach every required branch?

## Start from the heat balance

The chips in a liquid-cooled rack pass their heat through cold plates into coolant, which carries it to a coolant distribution unit (CDU). Three questions decide whether that works. How much coolant does the heat need? Can the pump push that much through the installed circuit? Does every branch get its share? The first takes one line of arithmetic. The other two decide whether each chip receives the flow the arithmetic asks for.

For a single-phase liquid whose specific heat capacity, cp, stays roughly constant, each kilogram absorbs cp times its temperature rise, ΔT. Multiply by the mass flow rate, ṁ, and you have the heat-transfer rate: Q̇ = ṁ × cp × ΔT. With heat in kilowatts and cp in kilojoules per kilogram-kelvin, mass flow comes out in kilograms per second, and the liquid's density turns that into litres. Keep heat rate and liquid flow apart by their units, kilowatts for one and litres per second for the other, even where a drawing labels both Q.

For water, at about 1 kg/L and 4.2 kJ/(kg·K), the balance reduces to a rule of thumb: a 10 K rise needs 60 ÷ (4.2 × 10) = 1.43 L/min of water for every kilowatt of heat. Halve the allowed rise to 5 K and the rule doubles to 2.86 L/min per kW.

The temperature rise is the liquid's outlet temperature minus its inlet temperature across the load, a separate number from the supply temperature and from a heat exchanger's approach temperature. Flow and rise trade against each other: in the previous lesson’s 100 kW case, doubling the flow from 2.5 to 5 kg/s halved the rise from 9.57 K to 4.78 K. A larger rise saves flow but warms the return and everything along the load path, while a smaller rise asks more of the pumps. The equipment's thermal requirements and the complete system design set the acceptable range.

## Ask what pressure difference produces that flow

A pump makes coolant circulate by supplying a pressure difference that pushes it through the circuit's restrictions: pipes, hoses, valves, filters, connectors and cold plates. The circuit needs more pressure the faster the liquid flows, and the pump adds less pressure the more flow it delivers. Its maximum free-flow figure, the flow at zero added pressure, is the one point on its curve that the installed circuit never reaches. Plot both curves against flow and they cross at the hydraulic operating point: the flow the loop actually gets, and the point to choose a pump by.

Resistance moves the operating point. A partly closed valve or a clogging filter makes the circuit curve steeper, so at unchanged pump speed the two curves meet at a higher pressure and a lower flow. The worked example puts numbers on both points, and in the lab below, raising the circuit coefficient k from 30 to 70 moves the loop from one to the other. The pump is still running and adding more pressure, yet less coolant circulates. Check flow as well as pressure, because the equipment needs enough coolant to carry its heat away.

In a circuit dominated by friction, pressure drop grows roughly with the square of flow over a working range. Hydraulic power is pressure difference times volume flow, so it grows with the cube of flow. On a circuit that needs 120 kPa at 2 L/s, halving the flow to 1 L/s cuts the pressure to 30 kPa and the hydraulic power from 240 W to 30 W, one-eighth. The pump affinity laws give the matching rule for a centrifugal pump changing speed on such a circuit: flow follows speed, pressure follows speed squared, and power follows speed cubed. The cube is the price of a small temperature rise: doubling the flow to halve the rise, as in that 100 kW case, takes four times the pressure and eight times the hydraulic power.

The square law is an approximation. Real pump and circuit curves, fluid viscosity, controls and component limits decide the actual operating point. A glycol mixture has its own density, heat capacity and viscosity, so a water calculation carries over only after those are checked at the intended conditions. Treat the fluid's identity as part of the interface specification.

## Parallel branches can hide a local shortage

A manifold divides the total flow among parallel branches by their hydraulic resistance and the pressure difference across them, whatever heat each carries. A partly blocked filter, a restrictive connector or a moved valve can starve one branch while its neighbours take the difference, and the total at the CDU stays the same. Take 2 L/s of water at 35°C feeding two 42 kW branches. Balanced at 1 L/s each, both return at 45°C. Restrict one branch to 0.5 L/s and the other takes 1.5 L/s: the starved branch returns at 55°C and its neighbour at 41.7°C.

Now mix the two returns. The flow-weighted average is still 45°C, the balanced value, while one branch runs 10 K hotter than design. A single rack-average return temperature cannot see that fault. Local device temperatures, branch flow or the differential pressure across each branch can. Which of them a loop needs depends on the failure modes it must catch and how fast it must respond. Its flow ledger lists every branch as well as the total.

## Include pump energy and qualification boundaries

Pump electricity ends up as heat. The motor and fluid boundaries decide where: the share assigned to the liquid adds to the heat the next exchanger must transfer, and any share that leaves to room air needs its own path in the ledger. A first flow calculation often leaves this small term out to isolate the main mechanism. The final engineering ledger states whether it is in.

A qualified loop also needs compatible wetted materials, fluid chemistry, cleanliness and service procedures. More flow cures a hydraulic shortage. It leaves poor thermal contact at a cold plate exactly as it was, and it can push a component past its allowed pressure, velocity or pumping envelope. Use the manufacturer's pump and system curves and the component limits to tell a hydraulic shortage from a local heat-transfer defect before changing the operating point.

## Worked example: One pump curve, two circuits

- The loop captures 84 kW into single-phase water with cp = 4.2 kJ/(kg·K), rounded from 4.18, and density 1 kg/L. The desired temperature rise is 10 K, and pump heat is left out.
- At fixed pump speed the pump curve is Δp = 160 − 10q² kPa and the circuit curve is Δp = 30q² kPa, with volume flow q in L/s. A partly closed valve raises the circuit curve to Δp = 70q² kPa.
- Overall pump efficiency is 60%.

1. Find the required flow — 84 ÷ (4.2 × 10) = 2 kg/s = 2 L/s = 120 L/min — The fluid density converts mass flow into volume flow.
2. Find operating point A — 160 − 10q² = 30q²; q = 2 L/s; Δp = 30 × 2² = 120 kPa — Pump and circuit agree at exactly the flow the heat balance needs.
3. Calculate pump power at A — 120,000 Pa × 0.002 m³/s = 240 W hydraulic; 240 ÷ 0.60 = 400 W electrical — In the International System of Units (SI), pascals times cubic metres per second give watts.
4. Partly close a valve: operating point B — 160 − 10q² = 70q²; q = √2 ≈ 1.41 L/s; Δp = 70 × 2 = 140 kPa — The pump supplies more pressure but moves less coolant.
5. Find the new temperature rise — 84 ÷ (√2 × 4.2) ≈ 14.1 K — The same heat in less water raises the coolant temperature 4.1 K more.

**Result:** At point A the pump delivers the 2 L/s that a 10 K rise needs, at 120 kPa and 400 W of input. The partly closed valve moves the loop to point B, 1.41 L/s at 140 kPa, and the coolant now rises 14.1 K.

**Model boundary:** The curves illustrate the mechanism and describe no real pump or CDU. Fluid-property variation, branch balance, transients, pressure limits and redundancy are outside the example.

## The tradeoff

Choice: Allow a larger liquid temperature rise to reduce required flow.

Benefit: Reduce hydraulic demand and the burden on piping and pumping: at 84 kW, doubling the allowed rise from 10 K to 20 K halves the required flow from 2 kg/s to 1 kg/s.

Cost: Downstream fluid runs warmer and device thermal margin can shrink. The pump's operating point has to be recalculated for the new flow.

## When the situation changes

Trigger: One of four equal 21 kW branches receives 0.25 L/s instead of its 0.5 L/s.

Mechanism: Its temperature rise doubles from 10 K to 20 K, whatever the other three branches do.

Response: Find the restricted branch from local temperatures and branch flow or pressure readings, then follow the qualified isolation and restoration procedure.

## Apply the idea

If the entire 400 W pump input enters the liquid upstream of the exchanger, what heat must the exchanger reject and what is the overall temperature rise at 2 kg/s?

<details>
<summary>Reveal the worked answer</summary>

The exchanger transfers 84.4 kW, and the overall rise is 84.4 ÷ (2 × 4.2) ≈ 10.048 K.

The difference is 0.048 K, small enough that the first-pass calculation stands. Closing it explicitly keeps pump energy from disappearing between boundaries. If part of the motor's heat went to room air instead, that share would need its own air-path term.

</details>

**The idea to keep:** The heat balance sets the flow the heat needs. The pump, the circuit and each branch decide the flow every load actually gets.

## Sources

- [Liquid to Liquid CDU Test Methodology and Performance Rating — Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) — Open Compute Project · Reviewed 2026-09-06. CDU evaluation includes thermal conditions, technology-loop pressure head and facility-loop flow impedance.
- [Open Compute Project — Cold Plate workstream](https://www.opencompute.org/wiki/Cooling_Environments/Cold_Plate) — www.opencompute.org · Reviewed 2026-09-06. The workstream separates cold-plate, loop, fluid and connector requirements.
- [U.S. DOE and Hydraulic Institute — Improving Pumping System Performance: A Sourcebook for Industry, 2nd ed., May 2006](https://www.energy.gov/sites/prod/files/2014/05/f16/pump.pdf) — U.S. Department of Energy and Hydraulic Institute · Published 2006-05 · Reviewed 2026-09-26. The affinity laws tie pump flow, pressure and speed; friction head rises roughly with flow squared, so doubling the flow quadruples it.
- [Grundfos — How does one read a pump curve of a heating pump?](https://www.grundfos.com/solutions/support/faq/how-does-one-read-a-pump-curve-of-a-heating-pump) — Grundfos · Reviewed 2026-09-26. A pump curve plots delivery head against flow, so higher flow means lower head; the duty point is where the system curve crosses the pump curve.
- [Hydraulic Institute — Pump System Operating Point (combined pump and system curves)](https://datatool.pumps.org/pump-fundamentals/combined.html) — Hydraulic Institute · Reviewed 2026-09-26. The system curve combines static head with friction losses that rise with flow, and the operating point is where it crosses the pump curve. Closing a valve steepens the system curve; changing pump speed shifts the pump curve by the affinity laws.
- [KSB — Characteristic curve (centrifugal pump lexicon)](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/characteristic-curve-1117926) — KSB · Reviewed 2026-09-26. A centrifugal pump’s characteristic curves plot head, power input, efficiency and net positive suction head (NPSH) required against flow.
