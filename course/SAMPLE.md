# 800 V DC: less copper, room for compute

Generated reading view. Edit [`course/expansion/sample.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/sample.json), lesson `sample-800v`, then run `uv run gigawatt-expand`.

**D06 · Authored draft · Objectives:** D06.2, D06.3

Keep a 100 kW average-power anchor while building from a closed DC circuit to alternating current, RMS and three phases. Then compare copper quantity, conversion placement and energy losses before testing a higher-load case.

**Driving question:** How can denser racks use less distribution copper and less space for power conversion?

## Start with the constraint on denser racks

The design ambition is to deliver more power using less distribution copper while freeing compute-rack and potentially data-hall space occupied by power-conversion equipment. Copper, equipment placement and energy efficiency are related design questions, but they require different evidence. Begin with material and space; use the energy ledger to test an efficiency claim.

To isolate one change, hold average received real power at 100 kW. First learn what voltage, current and three phases mean with ideal resistive teaching loads. Then compare equal received power to make the conductor-material arithmetic legible. Equal power alone does not prove that a new design can simultaneously use less copper and safely serve a larger load. The closing exercise changes the load and tests that additional claim.

## Trace a complete DC circuit

A voltage is an electrical potential difference: energy per unit charge. Current measures the rate at which charge passes a point. A source, a load and a complete conducting loop allow current to flow. The load receives electrical energy while charge continues around the circuit; the load does not consume the charge.

In this steady DC model, the source maintains a fixed polarity and 800 V across the load. Conventional current travels from the positive supply connection, through the load, and back through the return conductor. Both conductors carry 125 A as parts of the same loop. Adding their current magnitudes would count the same circuit current twice.

The received power is P = V × I = 800 × 125 = 100,000 W, or 100 kW. It is constant in this model. Direct current need not always have constant magnitude; steady values are the deliberate simplification here. Protective earth is not the normal load-current return.

The waveform primer assumes ideal conductors and no converters. At this boundary, source power equals received power. Later scenes add resistance and conversion losses rather than silently changing this energy balance.

## Separate alternating current from delivered energy

Start with one sinusoidal AC source and a resistive load. The voltage changes polarity every half-cycle. The current also reverses, in step with the voltage. With voltage and current referenced consistently at the receiving load, instantaneous power is their product: p(t) = v(t) × i(t). During the negative half-cycle both signs reverse, so the resistor continues receiving positive power. Alternating current does not imply that a resistor returns all the delivered energy every half-cycle.

An AC value must say whether it is a peak or an effective value. RMS means root mean square: square the waveform, average over a cycle, then take the square root. A given RMS current produces the same average heating in the same resistance as that numerical DC current. For a sine wave, peak = √2 × RMS; 480 V RMS therefore has a peak of about 679 V.

Choose this illustrative single-phase load to receive the same 100 kW average power. At 480 V RMS, its current is 100,000/480 = 208.33 A RMS. Voltage and current are sinusoidal and in phase, so power factor is one. Its instantaneous received power is p(θ) = 200 sin²(θ) kW: zero at the waveform crossings, 200 kW at the peaks, and 100 kW averaged over a complete cycle.

The average remains the comparison anchor even though instantaneous power changes. Over one hour at this operating point, the load receives 100 kWh, just as the preceding ideal DC load does. This single-phase case explains the waveform; the data-hall comparison will use balanced three-phase AC. Actual rack power electronics are not resistors and can change current waveforms and power factor.

## Combine three timed AC phases

Three-phase AC uses three sinusoidal phase voltages of equal magnitude, offset from one another by 120 degrees, or one-third of a cycle. For this teaching model, connect three equal resistive load branches at a shared star point, called a wye connection. A phase conductor connects to the other end of each branch.

Keep the total average received power at 100 kW. Each branch averages one-third of that, about 33.3 kW. Its instantaneous power rises and falls between zero and about 66.7 kW. Because the three waveforms are staggered, their instantaneous powers add to a constant 100 kW in this balanced sinusoidal model. A moment of zero voltage on one phase is not a moment of zero total power.

The three signed line currents also add to zero at every instant, but that statement concerns charge flow, not power. Current entering the load through some phase conductors leaves through the others; their roles vary over the cycle. A neutral conductor between the source neutral and load star point would carry zero load current in this ideal balanced case, so the normal load-current circuit can operate with three phase conductors.

Zero neutral current is conditional on this balanced sinusoidal model. Unequal loads and nonlinear current waveforms can require a neutral; protection and grounding requirements also remain. The later copper comparison counts three AC phase conductors under the stated idealization, not every conductor required in every real installation.

The DC, single-phase AC and three-phase AC examples all deliver 100 kW on average. DC is steady in its introductory model, single-phase resistive power pulsates, and the three-phase total is steady under balanced conditions. None of the three phases creates extra energy.

## Read the voltage before calculating current

In the data-hall comparison, 480 V AC means the RMS voltage measured between two phase conductors: line-to-line voltage. It is not the voltage across each branch of the wye teaching load. Each branch sees the phase-to-neutral voltage, measured from its phase conductor to the star point. In a balanced system that RMS value is 480/√3 ≈ 277.1 V.

Line-to-line voltage is the instantaneous difference between two phase voltages. Those equal sine waves are separated by 120 degrees, so the difference has √3 times the magnitude of either phase voltage. This is why the conversion uses √3; treating each branch as a separate 480 V load would mix measurement conventions.

Add the three branch powers. With sinusoidal currents in phase with their respective phase voltages, total real power is P = 3 × V_phase-to-neutral,RMS × I_line,RMS. Substitute V_phase-to-neutral = V_line-to-line/√3 to obtain P = √3 × V_line-to-line,RMS × I_line,RMS. More generally, balanced three-phase real power includes a power-factor multiplier, PF: real power divided by apparent power. The ideal resistive model uses PF = 1.

At 100 kW and 480 V line-to-line RMS, each line carries 100,000/(√3 × 480) = 120.281 A RMS. The corresponding 800 V DC example carries 100,000/800 = 125 A in each of its two conductors. The current magnitudes are close because the AC formula uses three phases and a line-to-line voltage convention. The voltage labels alone do not specify equal circuit arrangements.

The single-phase primer at 480 V RMS used a different arrangement and therefore required 208.33 A RMS for the same average power. It is not the baseline for the copper comparison. From the next scene onward, compare 480 V balanced three-phase AC with 800 V two-wire DC at the same 100 kW receiving-end power; introduce conductor resistance only when calculating heat.

## Fix the data-hall comparison before counting copper

The comparison from here is 480 V balanced three-phase AC versus 800 V two-wire DC. Both feeders deliver 100 kW of real power at their receiving ends. AC uses line-to-line RMS voltage, balanced sinusoidal currents and power factor one. DC voltage is measured between outgoing and return conductors. Conversion and cooling losses are excluded until a later complete-path comparison.

Count three AC phase conductors and two DC conductors under these assumptions. Protective earth and any neutral are outside the material count. Later we explicitly assign resistance per conductor; the ideal waveform demonstrations above contained no conductor loss. The distribution voltage does not mean that an accelerator chip itself operates at 800 V.

NVIDIA explicitly discusses moving from 415 or 480 V three-phase AC distribution to 800 V DC. This makes 480 V AC a relevant representative baseline for the lesson, not a universal facility voltage. The lower DC voltage inside a rack is a different comparison boundary.

## Lay the copper side by side

Give every current-carrying conductor equal length L, cross-sectional area A and copper material. The three-phase AC feeder has three such conductors; the DC feeder has two. Cross-sectional area is the amount of conductor material exposed by a cut across it. Copper volume is conductor count × L × A, and mass is volume times the same copper density.

The DC-to-AC conductor-copper ratio is therefore (2 × L × A)/(3 × L × A) = 2/3. At the stated equal 100 kW delivered load, the DC bundle contains 33.3% less current-carrying copper under these geometry assumptions. That is a material comparison, not a current saving.

Protective earth, any neutral, insulation, terminations and other equipment are excluded. We have not established that the chosen cross-section satisfies ampacity, temperature-rise or voltage-drop limits. Equal effective resistance in the later heat model is an additional idealization; equal geometry alone does not ensure identical AC and DC resistance in service.

## Calculate current without confusing it with copper

DC power is P = V × I. Balanced three-phase AC real power is P = √3 × V_line-to-line × I_line × PF. Use watts when calculating current in amperes. At 100,000 W, 480 V AC and PF = 1 give 120.281 A in each AC line. At 800 V DC, each conductor carries 125 A.

DC therefore carries about 3.9% more current per conductor in this stated comparison. The 33.3% conductor-copper reduction under equal geometry is not an automatic reduction in amperes. Adding currents across conductors and calling the sum the feeder current would obscure the different circuit arrangements.

The DC voltage control lets you explore this relationship while keeping the AC reference fixed at 480 V. Increasing DC voltage reduces DC current at the same delivered power. The subsequent worked conductor-loss and energy examples return to 800 V DC.

## Count every conductor when comparing heat

A conductor dissipates I²R as heat; use RMS current for AC. Add an explicit idealization: each complete conductor has an effective resistance of 10 mΩ, or 0.01 Ω, at the modeled operating point. This is resistance per conductor, not total DC loop resistance. Equal effective AC and DC resistance is specified independently of the earlier equal-copper-geometry assumption; actual AC effects and operating temperatures can change it. Ignore inductive and capacitive effects in this resistive-loss exercise.

The three AC conductors together dissipate 3 × 120.281² × 0.01 ≈ 434.028 W. The two DC conductors together dissipate 2 × 125² × 0.01 = 312.5 W. The DC-to-AC conductor-loss ratio is 0.72: 28% less conductor heat under these assumptions, despite slightly higher DC current in each conductor.

Keep the denominator visible. The 28% figure describes conductor heat; the earlier 33.3% figure describes copper quantity. Neither describes per-conductor current or all facility electricity. Changing voltage, power factor or effective resistance changes the heat result. Thermal ratings, insulation, protection and other requirements still determine practical sizing.

## Free compute space by locating conversion deliberately

A conventional arrangement can bring AC into a compute rack, convert it to DC there, and regulate it again near the devices. A hybrid arrangement retains upstream AC distribution but moves conversion into a nearby power rack or sidecar, then carries higher-voltage DC toward the compute load. A broader facility-DC proposal moves conversion farther upstream. These are different arrangements of equipment and interfaces.

In the sidecar view, locate the existing facility AC. That upstream path still has electrical limits, losses, protection requirements and maintenance dependencies. Moving a converter outside the compute rack can free rack space and move heat elsewhere, but the converter still needs space, cooling and service access. Final voltage reduction near the processor remains necessary. The drawings locate functions; they do not specify a buildable installation.

A power-room conversion arrangement can move selected conversion equipment out of the data hall, whereas a nearby sidecar still uses local space. Neither drawing establishes total facility-footprint savings. NVIDIA separately describes the copper and space constraints of 54 V DC rack distribution; that is a different electrical segment from this lesson’s 480 V AC feeder baseline. Final low-voltage device conversion remains necessary.

## Close the conductor energy balance

Use the same feeder assumptions: 100 kW received, 480 V balanced three-phase AC at PF = 1 versus 800 V two-wire DC, with 10 mΩ per conductor. The stated voltages are maintained at the receiving end. The sending supply provides enough voltage to cover the resistive drop; treating sending and receiving voltages as identical would silently discard that drop.

The AC source supplies 100 + 0.434028 = 100.434028 kW. The DC source supplies 100 + 0.3125 = 100.3125 kW. Both receiving ends get exactly 100 kW. Every input watt becomes either delivered power or conductor heat in this model.

Over one hour, the DC feeder requires 0.121528 kWh less input, about 0.122 kWh. No energy is created. The invented 10 mΩ resistance makes both feeders low-loss, so a 28% reduction in their small conductor-loss budget is a much smaller percentage of total input energy. This chosen small difference is not a prediction of real 800 V architecture savings. Converter and cooling losses remain outside this balance.

## Compare complete delivery paths at the same final load

Now move the fixed 100 kW boundary from each feeder receiving end to the final useful DC load. Both delivery paths begin at the same facility AC supply boundary. A downstream converter needs enough input to supply the useful load and cover its own losses. Its losses therefore increase the power carried by the feeder, which raises current and conductor heat. This boundary change explains why the final conductor losses differ from the preceding conductor-only example.

Keep the same feeder assumptions: 480 V balanced three-phase AC, line-to-line RMS, at power factor one; 800 V two-wire DC; and 10 mΩ per conductor. Assume the AC path has 4 kW of conversion loss, all downstream of the feeder. Its feeder must deliver 104 kW. Assume the DC path has 3 kW total conversion loss by default: a fixed 1 kW upstream rectifier loss and 2 kW downstream DC/DC loss. Its feeder must deliver 102 kW.

Calculate each feeder current from that receiving-end power, then calculate heat across all its conductors. AC conductor heat is 0.469444 kW, giving required facility input of 100 + 4 + 0.469444 = 104.469444 kW. DC conductor heat is 0.325125 kW, giving input of 100 + 1 + 2 + 0.325125 = 103.325125 kW. Over one hour, this DC arrangement requires 1.144319 kWh less input.

Raise total DC conversion loss to 6 kW. Upstream loss remains 1 kW; downstream loss becomes 5 kW. The DC feeder now delivers 105 kW, and its conductor heat rises to 0.344531 kW. Required facility input becomes 106.344531 kW, or 1.875087 kW more than AC. Over one hour it uses 1.875087 kWh more. Break-even total DC conversion loss is about 4.137 kW; the slider brackets it at 4.1 and 4.2 kW.

Conversion losses here are hypothetical watts at the specified operating points, not manufacturer efficiencies. Conductor losses are calculated from the feeder power rather than supplied as independent budgets. Cooling, other losses and voltage compatibility are outside the model. Actual designs need equipment performance, loading, protection, conductor geometry and thermal constraints evaluated together.

This energy counterexample does not undo the separately specified copper comparison or equipment relocation. It shows why an efficiency claim needs its own complete boundary and equipment evidence. Evaluate copper quantity, equipment space and input energy separately before deciding whether a design provides more usable compute power.

## Change the load and test the capacity claim

Return to the conductor-only boundary. Keep the same two DC conductors and 800 V receiving-end voltage, but raise received power from 100 to 200 kW. Predict the current, conductor heat and safe-capacity verdict before calculating. Copper quantity is unchanged because conductor count and geometry are unchanged.

Current rises from 100,000/800 = 125 A to 200,000/800 = 250 A. Holding effective resistance at 0.01 Ω per conductor, heat rises from 2 × 125² × 0.01 = 312.5 W to 2 × 250² × 0.01 = 1,250 W. At fixed voltage and resistance, doubling delivered power doubles current and quadruples conductor heat.

Safe operating capability is unknown. The calculation supplies no ampacity, installation conditions, allowable temperature rise, voltage-drop limits, terminal or protection ratings, converter rating or cooling headroom. Resistance itself varies with temperature in service. Additional usable power must be engineered; a larger number in the power equation is not proof that an unchanged installation can carry it.

The ambition remains more power with less material and more room for compute. The method is to specify the copper geometry, locate the equipment, close the energy balance and test the limiting conditions together. There is no universal savings percentage that replaces those checks.

## Worked example: 100 kW: count copper, then calculate current and heat

- Original synthetic feeders, each delivering 100 kW real power at its receiving end; sending supplies cover resistive voltage drop.
- AC: balanced sinusoidal three-phase, 480 V line-to-line RMS, power factor 1, three current-carrying conductors. DC: 800 V between two current-carrying conductors.
- Equal length, cross-sectional area and copper material for every current-carrying conductor; material count excludes protective earth, any neutral, insulation and terminations.
- Separately assume equal effective resistance of 0.01 Ω per conductor. Conversion and cooling losses are outside the feeder boundary; practical ampacity is not established.

1. DC/AC conductor-copper ratio = (2 × L × A)/(3 × L × A) = 2/3: 33.3% less conductor copper under equal geometry.
2. AC line current = 100,000/(√3 × 480 × 1) = 120.281 A. DC current = 100,000/800 = 125 A.
3. AC conductor heat = 3 × 120.281² × 0.01 ≈ 434.028 W. DC conductor heat = 2 × 125² × 0.01 = 312.5 W.
4. DC-to-AC conductor-loss ratio = 312.5/434.028 = 0.72, or 28% less conductor heat.
5. Input power is about 100.434 kW for AC and 100.313 kW for DC: about 0.122 kWh less DC input over one hour.

**Result:** Under equal geometry, DC uses one-third less current-carrying copper. Under the additional equal-effective-resistance assumption, it produces 28% less conductor heat despite slightly higher current per conductor.

**Model boundary:** Fixed receiving-end power and voltage; equal conductor geometry for material, equal effective resistance for heat. This does not establish ampacity-qualified sizing, complete conversion efficiency, installation cost or whole-facility savings.

## The tradeoff

Choice: Place a converter in a nearby sidecar.

Benefit: Move conversion equipment and some heat out of the compute rack.

Cost: Use space and service capacity elsewhere while retaining the existing upstream AC constraints.

## When the situation changes

Trigger: The new rack-power interface fits, but the room already has a binding cooling limit.

Mechanism: Changing electrical distribution does not automatically add heat-rejection capacity.

Response: Close the electrical and thermal ledgers at the same boundary before claiming more usable racks.

## Apply the idea

An 800 V DC feeder delivers 100 kW through two conductors, each modeled at 10 mΩ. Keep those conductors and receiving-end voltage unchanged, then raise received load to 200 kW. Predict current, conductor heat, copper quantity and whether safe operation has been established.

<details>
<summary>Reveal the worked answer</summary>

Current doubles from 125 to 250 A. Conductor heat rises fourfold from 0.3125 to 1.25 kW under the fixed-resistance model. Copper quantity is unchanged by assumption. Safe operating capability is unknown.

Use I = P/V and total DC conductor heat = 2I²R. Doubling current quadruples heat when R is held fixed. No ampacity, temperature, installation, voltage-drop, terminal, protection, converter or cooling limits were supplied; resistance also varies with temperature in service. The calculation cannot establish usable extra capacity.

</details>

**The idea to keep:** Judge copper with explicit geometry, space with explicit equipment placement, and energy with a complete loss balance. An 800 V label alone does not establish usable extra capacity.

## Sources and reading boundaries

- [Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) — Provides context for higher-voltage DC distribution and conversion placement. Numerical loads, voltages, resistance and conversion losses are original teaching assumptions. Conductor heat is calculated from the power each feeder delivers. Read 2026-09-08. August 11, 2026 vendor roadmap. Proposed architecture and availability expectations are distinct from a verified installed deployment.
- [Schneider Electric — PM2200 total power calculation for accuracy verification](https://productinfo.se.com/pm2200/5afc2b5546e0fb00011e5e9d/PM2200%20series%20User%20Manual/English/BM_PM2200seriesUserManual_0000074170.ditamap.xml/%24/C_VerifyingAccuracy_PowerTotCalcuation_0000034437) — Balanced three-phase real power is 3 × line-to-neutral RMS voltage × line current × power factor, equivalent to √3 × line-to-line RMS voltage × line current × power factor. Read 2026-09-08. Balanced three-phase relationship. Numerical loads, voltages, resistance and conversion losses are original teaching assumptions; calculated conductor losses are not equipment specifications.
- [NVIDIA, Partners Drive Next-Gen Efficient Gigawatt AI Factories in Buildup for Vera Rubin](https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin/) — Identifies 415 or 480 V three-phase AC systems as relevant baselines for the proposed transition to 800 V DC. Read 2026-09-08. Used only for baseline relevance. Vendor current, efficiency, copper and deployment claims are not validated by this teaching calculation.
- [NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) — Primary context for copper and rack-space constraints, upstream conversion, and the distinct 54 V rack-distribution boundary. Numerical feeder examples are original teaching calculations. Read 2026-09-09. May 2025 vendor roadmap. Proposed capacity, deployment and savings figures are not field validation; its percentage claims are not used as calculated sample results.
- [OpenStax — 20.5 Alternating Current versus Direct Current (College Physics 2e)](https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current) — Explains AC and DC, sinusoidal peak and RMS values, and average power delivered to a resistive load. The 100 kW comparisons are original teaching models. Read 2026-09-10. The AC primer assumes a sinusoidal source and a resistive load with power factor one; it does not model nonlinear rack power electronics.
- [Steven H. Low — Power System Analysis: Analytical tools and structural properties (April 7, 2025 draft)](https://netlab.caltech.edu/assets/book/PSA/Low-PSA-v20250407.pdf) — Sections 1.2–1.3 develop balanced three-phase circuits, phase-to-line voltage relationships, constant total instantaneous power and zero neutral current under balanced conditions. Read 2026-09-10. April 7, 2025 draft; used for the balanced sinusoidal circuit derivation. No real installation, neutral sizing or protection design follows from the simplified teaching model.
