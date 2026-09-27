# A cool room can contain an overheating chip

**11. Chip and rack heat capture**

Trace heat through local thermal resistances and parallel air/liquid paths, then compare the capture point of different cooling approaches.

**Driving question:** Why do equal rack heat loads create different local cooling problems?

## Name where the cooling happens

A cooling system has several jobs: capture heat at the hardware, transport it through the building, and reject it outdoors. Air cooling, rear-door heat exchangers (RDHX), cold plates and immersion describe capture near the rack. Dry coolers and evaporative towers describe outdoor rejection. A chiller adds refrigeration when the required temperature cannot be maintained by the available passive heat-transfer path. These choices can be combined; they are not competing names for one component.

Water cooler is too ambiguous to identify a data-center architecture. Name the actual equipment: a water-fed cold plate, a chilled-water air handler, a dry fluid cooler, a cooling tower or a water-cooled chiller. In the last term, water-cooled describes the chiller condenser. An air-cooled chiller can still supply chilled water to the building. Always ask which fluid takes heat from which object, then follow it to the next boundary.

## Is air cooling dead?

No, but moving concentrated rack heat through air has practical limits. Carry 100 kW through a 10°C rise: water needs about 2.39 litres per second, while air needs about 8,300 litres per second (8.3 m³/s), roughly 3,500 times the volume. These figures use 1,000 kg/m³ and 4.18 kJ/(kg·K) for water and 1.2 kg/m³ and 1.005 kJ/(kg·K) for air. The equation is the steady-flow sensible-heat balance: Q̇ = ṁ cₚ ΔT = ρ V̇ cₚ ΔT. It relates heat-transfer rate to mass flow, specific heat and fluid temperature rise when the fluid remains in one phase. It is not the boiling/condensation energy balance.

Flow and temperature rise trade against each other. Hold the liquid-path heat at 100 kW and the water inlet at 35°C. At 2.5 kg/s the water rises 100 ÷ (2.5 × 4.18) = 9.57 K and leaves at 44.57°C; doubling the flow to 5 kg/s halves the rise to 4.78 K and the outlet falls to 39.78°C. Those are coolant temperatures, not chip temperatures: the chip sits above the coolant by the temperature difference its local heat path needs.

Lenovo’s GB300 NVL72 guide, updated August 30, 2026, describes approximately 90% liquid and 10% air heat capture at rack level. Cold plates serve the major liquid-cooled components; remaining air-cooled components still need an air path. A GB300 hall therefore needs a coolant distribution unit (CDU) for the liquid heat and air cooling, such as a computer-room air handler (CRAH), for the rest. The proportions depend on the rack implementation and operating conditions.

## Follow temperature through the heat path

In a steady operating state, most electrical energy consumed by computing equipment becomes heat within the facility’s accounting boundary. That energy balance says how much heat must ultimately leave. It does not say that every device is at an acceptable temperature. Heat must cross a sequence of interfaces: from active silicon through its package and thermal interface, then into a heat sink, cold plate or immersion fluid, and onward to another cooling boundary. A restrictive local interface can overheat a device while the room-level heat balance still appears adequate.

A simple thermal-resistance model writes temperature difference as heat flow multiplied by thermal resistance. For example, 100 W crossing a 0.2°C/W path from a GPU to water at 30°C needs a 100 × 0.2 = 20°C difference, so the GPU runs at 50°C. State exactly which two temperatures the resistance connects. Junction-to-case, case-to-fluid and a complete effective path are different quantities. A measurement of coolant inlet temperature is not automatically the local bulk-fluid temperature beside the hottest region. Contact quality, flow distribution and heating along the path can matter. The model is a way to identify required temperature margin, not a substitute for a supplier’s qualified thermal performance map.

## Total heat and heat flux answer different questions

Heat flux is heat flow per area. Two devices each produce 400 W. Through four square centimeters that averages 100 W/cm²; through one square centimeter it averages 400 W/cm², four times as concentrated. The total heat is the same, but in the second device it must leave through a quarter of the area. Heat flux alone does not set a temperature without the geometry and thermal path, but it explains why total rack kilowatts alone cannot rank cooling difficulty. Within one package, local hotspots can be more demanding than the area average.

The temperature limit matters too. A device that tolerates a higher operating temperature has a different allowable path resistance at the same heat and coolant temperature. Reducing coolant temperature can create more margin, but it may increase the work required farther upstream or introduce condensation constraints. Improving the local interface can also create margin. Evaluate those options with the complete thermal and energy system in view. The most effective intervention depends on where the limiting temperature difference actually occurs.

## Compare where each method captures heat

An air-cooled heat sink transfers heat into a moving air stream. Containment and air management help prevent heated exhaust from mixing back into device inlets, but adequate room cooling cannot compensate for insufficient flow through a particular server. A rear-door heat exchanger captures heat from rack exhaust air into a liquid circuit. The server still needs a functioning internal air path, and the added exchanger must be compatible with its airflow and service requirements.

Room air must then pass its heat onward. A computer-room air handler (CRAH) uses a chilled-water coil: room air gives heat to the water, which returns to the cooling plant. A computer-room air conditioner (CRAC) uses a compressor-driven refrigerant circuit, often called direct expansion (DX). Its condenser still needs an air or water heat-rejection path. Perimeter, in-row and overhead describe placement and air delivery, not new ways to eliminate heat.

A cold plate captures heat near selected components and transfers it to the rack coolant loop, also called the technology coolant system. Components outside that liquid path can still reject heat to air, so a liquid-cooled rack may retain a substantial residual-air requirement. Immersion places qualified hardware in a compatible dielectric fluid. Single-phase systems transport sensible heat as the liquid warms; two-phase approaches use boiling and condensation as part of the transfer process. Fluid compatibility, component qualification, vapor or liquid containment and service procedures depend on the actual design. These approaches cannot be ranked from the word liquid alone.

## Close parallel heat paths without erasing local limits

Draw liquid-captured heat and residual air heat as separate arrows whose sum matches the defined rack heat load. Include auxiliaries consistently. If a 100 kW rack transfers 85 kW into a cold-plate loop and 15 kW to room air, the air system still needs to manage that 15 kW at the right locations. A failed fan can harm an air-cooled component while the liquid supply remains normal. Likewise, a blocked cold-plate branch can cause local throttling even if the room is comfortable and the CDU’s aggregate load is below its rating.

## Cold plates and immersion up close

A cold-plate assembly brings coolant through tubes, hoses and couplings to a metal plate mounted on each high-power package. Heat crosses the package, the thermal interface and the plate metal before entering the contained coolant.

2CRSi’s single-phase immersion system, below, pumps dielectric liquid from the tank through a coolant-to-water heat exchanger and back while the liquid stays liquid. The water side then carries the heat to a chilled-water loop, an evaporative cooling tower or a dry cooler. In two-phase immersion, a suitable fluid boils at the electronics, vapor reaches a cooled condenser, and liquid returns to the bath. The words single-phase and two-phase refer to the fluid’s physical state; they do not describe the facility electrical supply.

![2CRSi single-phase immersion diagram: server racks stand in a tank of dielectric liquid; a coolant pump sends warm liquid to a coolant-to-water heat exchanger and cooled liquid returns to the tank. The water side connects to a chilled-water loop, an evaporative cooling tower or a dry cooler.](../assets/references/2crsi-single-phase-immersion-user.png)

Single-phase immersion: the dielectric liquid circulates without boiling and hands its heat to a water loop. [2CRSi, single-phase immersion cooling](https://2crsi.com/single-phase-immersion-cooling)

## Worked example: Equal heat, unequal chip temperature

- Two chips each dissipate 400 W at steady state.
- Both are cooled by the same 35°C local coolant. Chip A’s path has an effective thermal resistance of 0.08 K/W; chip B’s has 0.12 K/W.
- Both chips have an 80°C maximum junction temperature; the junction is the hottest point inside the chip. The effective resistance connects that junction to the coolant.

1. Predict chip A’s temperature — 35 + 400 × 0.08 = 67°C — A has 13 K of margin to the limit.
2. Predict chip B’s temperature — 35 + 400 × 0.12 = 83°C — B exceeds the limit despite producing the same total heat.
3. Find the required resistance bound — (80 − 35) / 400 = 0.1125 K/W — The complete effective path must be no worse than this value in the stated model.

**Result:** The same heat and coolant temperature produce different outcomes because the local thermal paths differ: chip A reaches 67°C and chip B 83°C, above its 80°C limit.

**Model boundary:** The resistances and temperature limit are invented; this calculation cannot qualify a processor, cold plate or mounting procedure.

## The tradeoff

Choice: Capture more heat directly with cold plates.

Benefit: Reduce the fraction that must travel through the room-air path and potentially improve local heat removal: a 100 kW rack that sends 85 kW into cold plates leaves 15 kW for air.

Cost: Add fluid interfaces, material and leak qualification, branch-flow requirements and a different maintenance procedure.

## When the situation changes

Trigger: A cold plate has poor thermal contact after maintenance.

Mechanism: Effective local resistance increases while total coolant flow and rack electrical demand remain near normal.

Response: Correlate device temperatures with the qualified local operating model, remove the affected equipment from the agreed service state and have the responsible team verify the interface.

## Apply the idea

For chip B, lowering the coolant temperature to 30°C gives what junction temperature? Does that automatically make the better facility design?

<details>
<summary>Reveal the worked answer</summary>

30 + 400 × 0.12 = 78°C, so it passes the 80°C limit. It does not automatically make the better facility design.

Lower supply temperature may require additional upstream cooling work or condensation management. Improving the local path could preserve warmer facility operation. Compare qualified alternatives across both the device constraint and the wider energy and service boundaries.

</details>

**The idea to keep:** Heat quantity sets transport demand; heat concentration, resistance and temperature limits determine whether the device can operate.

## Sources

- [ASHRAE — Emergence and Expansion of Liquid Cooling in Mainstream Data Centers](https://www.ashrae.org/file%20library/technical%20resources/bookstore/emergence-and-expansion-of-liquid-cooling-in-mainstream-data-centers_wp.pdf) — www.ashrae.org · Published 2021 · Reviewed 2026-09-06. Thermal resistance connects device temperature, cooling-medium temperature and device heat; local requirements can drive cooling changes.
- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — ASHRAE · Published 2023 · Reviewed 2026-09-11. Provides context for air and liquid heat paths, CRAH chilled-water coils, CRAC compressorized circuits, and equipment-specific environmental requirements.
- [Trane TRACE 3D Plus — Air Cooled Chillers](https://trace3dplus.help.trane.com/air_cooled_chillers.html) — Trane · Reviewed 2026-09-11. An air-cooled chiller can make chilled water while its condenser rejects heat to air, resolving the ambiguity between load coolant and condenser cooling medium.
- [Lenovo NVIDIA GB300 NVL72 Rack Scale AI Product Guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai) — Lenovo Press · Published 2026-08-30 · Reviewed 2026-09-17. GB300 NVL72 rack heat capture is about 90% liquid and 10% air, with residual air-cooled components.
- [2CRSi — Single-phase immersion cooling](https://2crsi.com/single-phase-immersion-cooling) — 2CRSi · Reviewed 2026-09-17. In 2CRSi’s single-phase immersion system, dielectric liquid circulates through the tank and a separate coolant-to-water heat exchanger.
- [2CRSi — Two-phase immersion cooling](https://2crsi.com/two-phase-immersion-cooling) — 2CRSi · Reviewed 2026-09-17. Phase-change mechanism compared with single-phase immersion.
