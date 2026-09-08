# What 800 V changes

**D06 · Authored draft · Objectives:** D06.2, D06.3

Compare 480 V balanced three-phase AC with 800 V two-wire DC at equal received real power. Then hold the final DC load fixed and calculate how conversion placement changes feeder current, heat and required facility input.

**Driving question:** What does higher distribution voltage solve, and what does it leave for the rest of the facility?

## Keep received power and voltage conventions explicit

The intended comparison is 480 V balanced three-phase AC versus 800 V two-wire DC. Both feeders deliver 100 kW of real power at their receiving ends. This first boundary contains only the feeder conductors; conversion and cooling losses are excluded. Later we compare complete delivery paths serving the same final DC load.

For AC, 480 V means line-to-line RMS voltage: measured between two phase conductors, not from one phase to neutral. RMS is the effective value used for resistive-heating calculations, not the waveform peak. Power factor (PF) is real power divided by apparent power. Assume balanced sinusoidal AC with PF = 1, meaning equal phase magnitudes separated by 120 degrees and no reactive power at the receiving boundary.

For DC, 800 V is the voltage between the outgoing and return conductors. Count three current-carrying AC conductors and two DC conductors. Protective earth and any neutral are outside this simplified comparison. The distribution voltage does not mean that an accelerator chip itself operates at 800 V.

NVIDIA explicitly discusses moving from 415 or 480 V three-phase AC distribution to 800 V DC. This makes 480 V AC a relevant representative baseline for the lesson, not a universal facility voltage. The lower DC voltage inside a rack is a different comparison boundary.

## Calculate current before claiming a saving

DC power is P = V × I. Balanced three-phase AC real power is P = √3 × V_line-to-line × I_line × PF. Use watts when calculating current in amperes. At 100,000 W, 480 V AC and PF = 1 give 120.281 A in each AC line. At 800 V DC, each conductor carries 125 A.

DC therefore carries about 3.9% more current per conductor in this stated comparison. Two instead of three is 33% fewer current-carrying conductors, not an automatic reduction in amperes. Adding currents across conductors and calling the sum the feeder current would obscure the different circuit arrangements.

The DC voltage control lets you explore this relationship while keeping the AC reference fixed at 480 V. Increasing DC voltage reduces DC current at the same delivered power. The subsequent worked conductor-loss and energy examples return to 800 V DC.

## Count every conductor when comparing heat

A conductor dissipates I²R as heat; use RMS current for AC. Assume an original teaching value of 10 mΩ, or 0.01 Ω, for each complete conductor from the sending end to the receiving end. This is resistance per conductor, not the total DC loop resistance. Ignore inductive and capacitive effects in this resistive-loss example.

The three AC conductors together dissipate 3 × 120.281² × 0.01 ≈ 434.028 W. The two DC conductors together dissipate 2 × 125² × 0.01 = 312.5 W. The DC-to-AC conductor-loss ratio is 0.72: 28% less conductor heat under these assumptions, despite slightly higher DC current in each conductor.

Keep the denominator visible. This is a reduction in conductor losses, not in per-conductor current or all facility electricity. Changing voltage, power factor or conductor resistance changes the result. Two instead of three conductors means 33% less conductor material only if their lengths, cross-sections and materials remain equal. That arithmetic does not establish a practical cable design; thermal ratings, insulation, protection and other requirements still matter.

## Follow the conversion boundary

A conventional arrangement can bring AC into a compute rack, convert it to DC there, and regulate it again near the devices. A hybrid arrangement retains upstream AC distribution but moves conversion into a nearby power rack or sidecar, then carries higher-voltage DC toward the compute load. A broader facility-DC proposal moves conversion farther upstream. These are different arrangements of equipment and interfaces.

In the sidecar view, locate the existing facility AC. That upstream path still has electrical limits, losses, protection requirements and maintenance dependencies. Moving a converter outside the compute rack can free rack space and move heat elsewhere, but the converter still needs space, cooling and service access. Final voltage reduction near the processor remains necessary. The drawings locate functions; they do not specify a buildable installation.

## Close the conductor energy balance

Use the same feeder assumptions: 100 kW received, 480 V balanced three-phase AC at PF = 1 versus 800 V two-wire DC, with 10 mΩ per conductor. The stated voltages are maintained at the receiving end. The sending supply provides enough voltage to cover the resistive drop; treating sending and receiving voltages as identical would silently discard that drop.

The AC source supplies 100 + 0.434028 = 100.434028 kW. The DC source supplies 100 + 0.3125 = 100.3125 kW. Both receiving ends get exactly 100 kW. Every input watt becomes either delivered power or conductor heat in this model.

Over one hour, the DC feeder requires 0.121528 kWh less input, about 0.122 kWh. No energy is created. A 28% reduction in this small conductor-loss budget is a much smaller percentage of total input energy. Converter and cooling losses remain outside this balance.

## Compare complete delivery paths at the same final load

Now move the fixed 100 kW boundary from each feeder receiving end to the final useful DC load. Both delivery paths begin at the same facility AC supply boundary. A downstream converter needs enough input to supply the useful load and cover its own losses. Its losses therefore increase the power carried by the feeder, which raises current and conductor heat. This boundary change explains why the final conductor losses differ from the preceding conductor-only example.

Keep the same feeder assumptions: 480 V balanced three-phase AC, line-to-line RMS, at power factor one; 800 V two-wire DC; and 10 mΩ per conductor. Assume the AC path has 4 kW of conversion loss, all downstream of the feeder. Its feeder must deliver 104 kW. Assume the DC path has 3 kW total conversion loss by default: a fixed 1 kW upstream rectifier loss and 2 kW downstream DC/DC loss. Its feeder must deliver 102 kW.

Calculate each feeder current from that receiving-end power, then calculate heat across all its conductors. AC conductor heat is 0.469444 kW, giving required facility input of 100 + 4 + 0.469444 = 104.469444 kW. DC conductor heat is 0.325125 kW, giving input of 100 + 1 + 2 + 0.325125 = 103.325125 kW. Over one hour, this DC arrangement requires 1.144319 kWh less input.

Raise total DC conversion loss to 6 kW. Upstream loss remains 1 kW; downstream loss becomes 5 kW. The DC feeder now delivers 105 kW, and its conductor heat rises to 0.344531 kW. Required facility input becomes 106.344531 kW, or 1.875087 kW more than AC. Over one hour it uses 1.875087 kWh more. Break-even total DC conversion loss is about 4.137 kW; the slider brackets it at 4.1 and 4.2 kW.

Conversion losses here are hypothetical watts at the specified operating points, not manufacturer efficiencies. Conductor losses are calculated from the feeder power rather than supplied as independent budgets. Cooling, other losses and voltage compatibility are outside the model. Actual designs need equipment performance, loading, protection, conductor geometry and thermal constraints evaluated together.

For dense racks, 480 V AC versus 800 V DC distribution is a question about where conversion belongs and which delivery constraints it changes. Moving conversion can alter rack space, service access, conductor requirements and heat location. An input-energy advantage must follow from the complete balance; the preceding 28% conductor-loss reduction is not a fixed whole-path or facility saving.

## Worked example: 100 kW through 480 V three-phase AC or 800 V DC

- Original synthetic feeders, each delivering 100 kW real power at its receiving end; sending supplies cover resistive voltage drop.
- AC: balanced sinusoidal three-phase, 480 V line-to-line RMS, power factor 1, three current-carrying conductors. DC: 800 V between two current-carrying conductors.
- Each conductor has 0.01 Ω resistance; protective earth and any neutral excluded. Conversion and cooling losses are outside the feeder boundary.

1. AC line current = 100,000/(√3 × 480 × 1) = 120.281 A. DC current = 100,000/800 = 125 A.
2. AC conductor heat = 3 × 120.281² × 0.01 ≈ 434.028 W. DC conductor heat = 2 × 125² × 0.01 = 312.5 W.
3. DC-to-AC conductor-loss ratio = 312.5/434.028 = 0.72, or 28% less conductor heat.
4. Input power is about 100.434 kW for AC and 100.313 kW for DC: about 0.122 kWh less DC input over one hour.

**Result:** The DC case has fewer current-carrying conductors and lower total conductor heat under these assumptions, with slightly higher current in each conductor.

**Model boundary:** A resistive feeder comparison at fixed receiving-end power and voltage. It does not calculate complete conversion losses, thermal ratings, installation cost or whole-facility savings.

## The tradeoff

Choice: Place a converter in a nearby sidecar.

Benefit: Move conversion equipment and some heat out of the compute rack.

Cost: Use space and service capacity elsewhere while retaining the existing upstream AC constraints.

## When the situation changes

Trigger: The new rack-power interface fits, but the room already has a binding cooling limit.

Mechanism: Changing electrical distribution does not automatically add heat-rejection capacity.

Response: Close the electrical and thermal ledgers at the same boundary before claiming more usable racks.

## Apply the idea

Both paths serve the same final 100 kW DC load. The 480 V three-phase AC feeder has 4 kW downstream conversion loss. The 800 V two-wire DC path has 6 kW total conversion loss: 1 kW upstream and 5 kW downstream. With 10 mΩ per conductor, AC power factor 1 and a one-hour duration, which path needs more input energy? Include the effect of downstream losses on conductor current.

<details>
<summary>Reveal the worked answer</summary>

AC needs about 104.469 kWh. DC needs about 106.345 kWh. DC uses about 1.875 kWh more input energy in this hypothetical comparison.

The AC feeder delivers 104 kW and dissipates about 0.469444 kW across three conductors. The DC feeder delivers 105 kW and dissipates about 0.344531 kW across two conductors. Add all conversion and conductor losses to the final 100 kW load, then multiply by one hour. Lower DC conductor heat does not offset its higher assumed conversion loss.

</details>

**The idea to keep:** Fewer conductors do not automatically mean less current. Conductor heat depends on voltage, current and resistance; whole-path energy input depends on all losses at equal useful output.

## Sources and reading boundaries

- [Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) — Provides context for higher-voltage DC distribution and conversion placement. Numerical loads, voltages, resistance and conversion losses are original teaching assumptions. Conductor heat is calculated from the power each feeder delivers. Read 2026-09-08. August 11, 2026 vendor roadmap. Proposed architecture and availability expectations are distinct from a verified installed deployment.
- [Schneider Electric — PM2200 total power calculation for accuracy verification](https://productinfo.se.com/pm2200/5afc2b5546e0fb00011e5e9d/PM2200%20series%20User%20Manual/English/BM_PM2200seriesUserManual_0000074170.ditamap.xml/%24/C_VerifyingAccuracy_PowerTotCalcuation_0000034437) — Balanced three-phase real power is 3 × line-to-neutral RMS voltage × line current × power factor, equivalent to √3 × line-to-line RMS voltage × line current × power factor. Read 2026-09-08. Balanced three-phase relationship. Numerical loads, voltages, resistance and conversion losses are original teaching assumptions; calculated conductor losses are not equipment specifications.
- [NVIDIA, Partners Drive Next-Gen Efficient Gigawatt AI Factories in Buildup for Vera Rubin](https://blogs.nvidia.com/blog/gigawatt-ai-factories-ocp-vera-rubin/) — Identifies 415 or 480 V three-phase AC systems as relevant baselines for the proposed transition to 800 V DC. Read 2026-09-08. Used only for baseline relevance. Vendor current, efficiency, copper and deployment claims are not validated by this teaching calculation.
