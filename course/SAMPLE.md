# 800 V DC: less copper, room for compute

Generated reading view. Edit [`course/expansion/sample.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/sample.json), lesson `sample-800v`, then run `uv run gigawatt-expand`.

**D06 · Authored draft · Objectives:** D06.2, D06.3

Learn the electrical foundations, then compare distribution copper and the placement of conversion equipment.

**Driving question:** How can denser racks use less distribution copper and less space for power conversion?

## Start with the constraint on denser racks

The design ambition is to deliver more power using less distribution copper while freeing compute-rack and potentially data-hall space occupied by power-conversion equipment. Copper, equipment placement and energy efficiency are related design questions, but they require different evidence. Begin with material and space; use measured equipment efficiency to evaluate total losses.

To isolate one change, hold average received real power at 100 kW. First learn what voltage, current and three phases mean with ideal resistive teaching loads. Then compare equal received power to make the conductor-material arithmetic legible. Equal power alone does not prove that a new design can simultaneously use less copper and safely serve a larger load.

## Trace a complete DC circuit

A voltage is an electrical potential difference: energy per unit charge. Current measures the rate at which charge passes a point. A source, a load and a complete conducting loop allow current to flow. The load receives electrical energy while charge continues around the circuit; the load does not consume the charge.

In this steady DC model, the source maintains a fixed polarity and 800 V across the load. Conventional current travels from the positive supply connection, through the load, and back through the return conductor. Both conductors carry 125 A as parts of the same loop. Adding their current magnitudes would count the same circuit current twice.

The received power is P = V × I = 800 × 125 = 100,000 W, or 100 kW. It is constant in this model. Direct current need not always have constant magnitude; steady values are the deliberate simplification here. Protective earth is not the normal load-current return.

The waveform primer assumes ideal conductors and no converters. At this boundary, source power equals received power. Later scenes add resistance and conversion losses rather than silently changing this energy balance.

## Separate alternating current from delivered energy

The load is the equipment receiving power. Here it is modeled as an ideal resistance so the waveform arithmetic is transparent. A 480 V single-phase load can be supplied between two phases of a three-phase system; the voltage label alone does not specify the number of phases. This introductory circuit is not the three-phase data-hall feeder used in the later comparison.

Start with one sinusoidal AC source and a resistive load. The voltage changes polarity every half-cycle. The current also reverses, in step with the voltage. With voltage and current referenced consistently at the receiving load, instantaneous power is their product: p(t) = v(t) × i(t). During the negative half-cycle both signs reverse, so the load continues receiving positive power. Alternating current does not imply that this load returns all the delivered energy every half-cycle.

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

L1, L2 and L3 are three live phase conductors. Neither of the two meter connections is ground. In the balanced system, any phase pair measures 480 V RMS: L1–L2, L2–L3 or L3–L1. Voltage uses two measurement points even when the system has three phases. Neutral and protective earth have distinct roles; they are not an unmentioned third phase.

The 480 V label is an RMS value over a cycle, not a constant signed voltage difference. Instantaneous differences obey v12 + v23 + v31 = 0. Their waveforms are shifted in time, so the RMS magnitudes cannot be added as 480 + 480. For example, at one instant phase-to-neutral voltages are about +392, −196 and −196 V: the three signed pair differences are about +588, 0 and −588 V. Each pair still measures 480 V RMS over a full cycle.

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

These are possible architecture choices, not a mandatory sequence for every data center. A real facility may combine AC and DC segments differently.

This is the conventional AC baseline, not SemiAnalysis Phase 1. The later labels refer to the article’s forecast adoption phases, which are unrelated to the three electrical phases of an AC waveform.

In the May 26, 2026 SemiAnalysis forecast, Phase 1 (2026/2027) and Phase 2 (2027/2028) both use near-rack conversion. The important internal distinction is where 800 V is stepped down: a rack shelf in Phase 1 versus on-blade conversion in Phase 2. This drawing groups their shared AC-fed sidecar arrangement; it does not depict identical rack internals. Backup is omitted from these placement drawings: the article discusses DC-coupled batteries and supercapacitors replacing central UPS functions, while also expecting some operators to retain a central UPS. The forecast does not imply one universal backup topology.

SemiAnalysis forecasts Phase 3 for late 2028/2029: conventional step-down followed by a low-voltage AC-to-800 V DC rectifier upstream. Its separate Phase 4 concerns medium-voltage input and SSTs; the heading says after 2029 while its body says early 2029, so no single exact date is adopted for that phase. These are dated forecasts, not confirmed installation dates.

## Close the conductor energy balance

Use the same feeder assumptions: 100 kW received, 480 V balanced three-phase AC at PF = 1 versus 800 V two-wire DC, with 10 mΩ per conductor. The stated voltages are maintained at the receiving end. The sending supply provides enough voltage to cover the resistive drop; treating sending and receiving voltages as identical would silently discard that drop.

The AC source supplies 100 + 0.434028 = 100.434028 kW. The DC source supplies 100 + 0.3125 = 100.3125 kW. Both receiving ends get exactly 100 kW. Every input watt becomes either delivered power or conductor heat in this model.

Over one hour, the DC feeder requires 0.121528 kWh less input, about 0.122 kWh. No energy is created. The invented 10 mΩ resistance makes both feeders low-loss, so a 28% reduction in their small conductor-loss budget is a much smaller percentage of total input energy. This chosen small difference is not a prediction of real 800 V architecture savings. Converter and cooling losses remain outside this balance.

## What determines converter losses?

The supply drawing and the heat calculation have different boundaries. The drawing shows a conventional transformer followed by an electronic AC/DC converter; the heat calculation counts only the electronic converter. A conventional transformer uses windings and a magnetic core, and can cool naturally. Controls and any cooling auxiliaries inside an electronic supply are not a description of a bare transformer.

The first view of slide 9 now traces medium-voltage AC through a conventional transformer into lower-voltage conversion electronics. The heat calculation is a separate view of that converter. Stepping down reduces semiconductor voltage stress. A direct medium-voltage design instead needs higher-rated devices or cascaded voltage-sharing cells and their supporting insulation, protection and controls. The cited SemiAnalysis discussion explicitly acknowledges the stacked-device route; the commercial constraint is not an absolute 10 kV rectification ceiling.

This example isolates one AC/DC power supply: 480 V three-phase AC at its input and 800 V DC at its output. It represents the conversion function moved into a power rack or power room in the following architecture drawings. The supply may contain multiple internal conversion stages. It is not a UPS AC-to-DC-to-AC path or a model of the whole data center.

Before this example’s 480 V AC input, a conventional transformer steps medium-voltage AC down and provides galvanic isolation. Lower AC voltage reduces the voltage stress handled by the following power electronics. The transformer’s own losses are outside the one-power-supply calculation shown here.

The controlled AC/DC supply establishes the 800 V DC output; a simple rectifier is not a voltage-independent route to 800 V. SemiAnalysis’s Phase 3 example uses 415 V AC after conventional step-down. This numerical example retains 480 V AC; neither is a universal required input voltage.

A conventional transformer changes AC voltage; it does not rectify. There is no universal 10 kV ceiling on rectification. Cascaded converter cells can share medium-voltage stress among lower-voltage semiconductors. An SST is an alternative architecture that combines electronic stages with high-frequency isolation, not a prerequisite for an 800 V DC bus. See D04, “Why step down before rectifying?”, for the device-rating distinction.

Conversion changes voltage or electrical form with real components. Current through semiconductor on-resistance, winding resistance and diode drops dissipates power. Switching transitions dissipate energy as current and voltage overlap; repeating those transitions adds average loss. Magnetic cores, controllers, gate drivers and fans also consume power. The balance depends on converter topology, device choices, voltage, load, switching frequency, temperature and operating mode.

Efficiency η is useful output power divided by input power. At a fixed output, P_loss = P_out × (1/η − 1). The slide assumes 98% efficiency solely to demonstrate the calculation: 100/0.98 = 102.0408 kW input, so loss is 2.0408 kW. It is not the efficiency of the pictured UPS or a measured advantage of AC or DC distribution.

To compare architectures, read the actual equipment efficiency curves at the required loading and mode, then sum losses along the complete path. Fewer conversion boxes or lower conductor heat alone does not establish lower total facility input.

## What the architecture comparison establishes

At the same delivered power, the stated equal-geometry comparison uses two current-carrying copper conductors instead of three. Moving AC-to-DC conversion out of the compute rack frees its occupied rack space. A sidecar still occupies nearby hall space; upstream conversion can move that equipment to the power room.

These are the physical changes the lesson set out to explain. Overall hall footprint and facility energy savings require the actual equipment arrangement and losses.

## Compare the three distribution paths side by side

Trace each column from medium-voltage input to the rack. Traditional AC keeps lower-voltage AC distribution through the hall. The DC sidecar retains those upstream stages, then creates an 800 V DC interface near the rack. The third path makes 800 V DC upstream of the hall distribution and busway through a medium-voltage conversion system.

The right-hand column is a direct-medium-voltage design. It differs from the preceding transformer-plus-low-voltage-rectifier example: both can feed an 800 V DC hall. A compact system block does not mean that voltage reduction, isolation, storage, protection or downstream rack DC/DC conversion cease to be necessary functions where the design requires them. The diagram leaves several of these functions out.

Use this drawing to compare conversion placement and AC/DC interfaces. It has no deployment dates and does not prove an efficiency percentage or equipment readiness. Keep the dated SemiAnalysis roadmap separate from these architectural alternatives.

![Three electrical paths. Traditional AC: medium-voltage AC, step-down transformer, AC switchboards, AC PDUs, AC IT racks. DC sidecar: the same upstream AC stages followed by a rack-level AC-to-800-V-DC rectifier and 800-V-DC IT racks. Direct medium-voltage DC: medium-voltage rectifier or solid-state transformer, 800-V-DC distribution, DC busway and DC IT racks. Yellow denotes 10 to 35 kV, blue 400 to 480 V, and green 800 V DC.](assets/references/ocp-ac-sidecar-direct-mvdc.png)

User-supplied figure, attributed to the Open Compute Project; the original publication has not yet been identified. The linked OCP paper provides related LVDC architecture context. The right-hand path depicts direct medium-voltage conversion, not the conventional transformer-plus-low-voltage-rectifier route. These are selected conversion and distribution functions, not complete power or protection designs. [Related OCP LVDC architecture paper](https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1)

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

A power sidecar takes AC-to-DC conversion out of a compute rack but stays beside it in the data hall. Which space is freed, and does this establish a smaller data hall or lower electricity use?

<details>
<summary>Reveal the worked answer</summary>

Space inside the compute rack is freed. The sidecar still needs hall space and service access. Neither a smaller total hall footprint nor lower electricity use follows automatically.

Locate the displaced equipment before counting freed space. Compare actual converter losses at the same useful output before claiming an energy saving.

</details>

**The idea to keep:** Judge copper with explicit geometry, space with explicit equipment placement, and energy with a complete loss balance. An 800 V label alone does not establish usable extra capacity.

## Sources and reading boundaries

- [Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) — Provides context for higher-voltage DC distribution and conversion placement. Numerical loads, voltages, resistance and conversion losses are original teaching assumptions. Conductor heat is calculated from the power each feeder delivers. Read 2026-09-08. August 11, 2026 vendor roadmap. Proposed architecture and availability expectations are distinct from a verified installed deployment.
- [Schneider Electric — PM2200 total power calculation for accuracy verification](https://productinfo.se.com/pm2200/5afc2b5546e0fb00011e5e9d/PM2200%20series%20User%20Manual/English/BM_PM2200seriesUserManual_0000074170.ditamap.xml/%24/C_VerifyingAccuracy_PowerTotCalcuation_0000034437) — Balanced three-phase real power is 3 × line-to-neutral RMS voltage × line current × power factor, equivalent to √3 × line-to-line RMS voltage × line current × power factor. Read 2026-09-08. Balanced three-phase relationship. Numerical loads, voltages, resistance and conversion losses are original teaching assumptions; calculated conductor losses are not equipment specifications.
- [NVIDIA, Partners Drive Next-Gen Efficient Gigawatt AI Factories in Buildup for Vera Rubin](https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin/) — Identifies 415 or 480 V three-phase AC systems as relevant baselines for the proposed transition to 800 V DC. Read 2026-09-08. Used only for baseline relevance. Vendor current, efficiency, copper and deployment claims are not validated by this teaching calculation.
- [NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) — Primary context for copper and rack-space constraints, upstream conversion, and the distinct 54 V rack-distribution boundary. Numerical feeder examples are original teaching calculations. Read 2026-09-09. May 2025 vendor roadmap. Proposed capacity, deployment and savings figures are not field validation; its percentage claims are not used as calculated sample results.
- [OpenStax — 20.5 Alternating Current versus Direct Current (College Physics 2e)](https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current) — Explains AC and DC, sinusoidal peak and RMS values, and average power delivered to a resistive load. The 100 kW comparisons are original teaching models. Read 2026-09-10. The AC primer assumes a sinusoidal source and a resistive load with power factor one; it does not model nonlinear rack power electronics.
- [Steven H. Low — Power System Analysis: Analytical tools and structural properties (April 7, 2025 draft)](https://netlab.caltech.edu/assets/book/PSA/Low-PSA-v20250407.pdf) — Sections 1.2–1.3 develop balanced three-phase circuits, phase-to-line voltage relationships, constant total instantaneous power and zero neutral current under balanced conditions. Read 2026-09-10. April 7, 2025 draft; used for the balanced sinusoidal circuit derivation. No real installation, neutral sizing or protection design follows from the simplified teaching model.
- [Schneider Electric — What is UPS efficiency and how is it calculated?](https://www.se.com/us/en/faqs/FAQ000244215/) — Efficiency is output power divided by input power and varies with operating load. Read 2026-09-11. Uses the general efficiency definition and load dependence; no product efficiency or eConversion claim is adopted.
- [Texas Instruments — Power Loss in Switching Power Supplies](https://www.ti.com/document-viewer/lit/html/SLUAAL9) — Explains transistor conduction and switching losses in switching power supplies. Read 2026-09-11. August 2022 application brief. Mechanisms only, not an efficiency prediction for data-center converters.
- [Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) — Forecast adoption phases: 2026/2027, 2027/2028 and late 2028/2029; distinction between near-rack conversion and upstream low-voltage rectification. Read 2026-09-11. May 26, 2026 analysis. Architecture dates are forecasts. Phase 4 timing is internally inconsistent: heading >2029, body early 2029. The three teaching drawings are a baseline plus grouped Phases 1–2 and Phase 3.
- [Texas Instruments — TIDA-011012 modular solid-state transformer reference design](https://www.ti.com/tool/TIDA-011012) — Explain how input-series converter submodules divide medium-voltage stress across lower-voltage semiconductor devices. Read 2026-09-10. Reviewed overview and feature list. Reference-design architecture, not a deployed data-center system; its stated DC-link voltages are not an 800 V output specification.
- [Huber et al. — Comparative Evaluation of MVAC–LVDC SST and Hybrid Transformer Concepts for Future Datacenters (IPEC 2022)](https://www.ams-publications.ee.ethz.ch/uploads/tx_ethpublications/1_IPEC_2022_Final_Huber.pdf) — Compare transformer-plus-rectifier and SST architectures for 800 V DC; separate system voltage from per-device voltage. Read 2026-09-10. Reviewed Figure 1 and Sections II–IV. The study includes a 13.2 kV cascaded design using 1,200 V devices. Efficiency and density results belong to its 2022 models and are not current universal rankings.
- [Hitachi Energy — Core-type transformers](https://www.hitachienergy.com/products-and-solutions/transformers/power-transformers/generator-step-up-transformers-gsu/core-type-transformers) — Transformer anatomy uses conductive windings and a laminated magnetic steel core. Read 2026-09-11. Product-family anatomy description reviewed. No rating or physical layout is adopted as a universal distribution-transformer specification.
- [Schneider Electric — AA and AA/FA transformer cooling](https://www.se.com/ca/en/faqs/FA102583/) — Natural air convection and added fan cooling are distinct transformer cooling arrangements; fans are not inherent to the transformer function. Read 2026-09-11. FAQ cooling distinctions reviewed. No fan rating, installation requirement or universal capacity threshold is inferred.
- [Eaton — Medium-voltage solid-state transformer](https://www.eaton.com/us/en-us/catalog/medium-voltage-power-distribution-control-systems/medium-voltage-solid-state-transformer.html) — Eaton lists a 2 MW MVSST with 12.47 kV nominal input and 800 V DC output, demonstrating a direct-MV product offering. Read 2026-09-11. Manufacturer product listing reviewed on 2026-09-11. Offered specifications do not establish installed capacity, deployment prevalence, lead time or a measured efficiency advantage.
- [OCP — Data Center Facility: Low Voltage Direct Current Power Distribution, v1.0](https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1) — Context for representative LVDC power-distribution architectures; not a confirmed source for the supplied three-column figure. Read 2026-09-11. Introduction and document metadata inspected. The exact origin of the user-supplied image remains unverified. Do not assign a figure number, mandate this topology, or treat these alternatives as a dated deployment sequence.
