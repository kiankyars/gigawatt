# What 800 V changes

**D06 · Authored draft · Objectives:** D06.2, D06.3

Compare 48 V DC with 800 V DC at equal delivered power, close the conductor energy balance, then compare complete AC-distributed and DC-distributed paths using explicit hypothetical losses.

**Driving question:** What does higher distribution voltage solve, and what does it leave for the rest of the facility?

## Keep the useful load fixed

The first comparison is 48 V DC versus 800 V DC. Both values are receiving-end voltages across the same stated DC load boundary. It does not compare an AC waveform with a DC waveform. AC and DC arrangements are compared separately below using a complete, explicitly hypothetical loss budget.

Start with a hypothetical load receiving 100 kilowatts of direct-current power. A watt is a rate of energy transfer. Voltage describes energy transferred per unit charge; current describes charge flowing per second. At this DC boundary, power equals voltage multiplied by current: P = V × I. To find current, divide the required power by the voltage. We are holding the load fixed so that changing one variable has an interpretable consequence.

One hundred kilowatts is 100,000 watts. At 48 volts, the current is 100,000/48, or about 2,083 amperes. At 800 volts, it is 125 amperes. The power has not fallen. Each unit of charge now transfers more energy, so less charge has to flow each second to deliver the same power. This calculation describes the selected distribution segment; it does not mean that an accelerator chip operates at 800 volts.

## Follow the conversion boundary

A conventional arrangement can bring AC into a compute rack, convert it to DC there, and regulate it again near the devices. A hybrid arrangement retains upstream AC distribution but moves conversion into a nearby power rack or sidecar, then carries higher-voltage DC toward the compute load. A broader facility-DC proposal moves conversion farther upstream. These are different arrangements of equipment and interfaces, not three names for one replacement component.

Use the architecture buttons below. In the sidecar view, locate the words existing facility AC. The upstream path is still there. It still has its electrical limits, losses, protection requirements and maintenance dependencies. Moving a converter outside the compute rack can free rack space and move heat into another location. That converter still needs a place, a power supply, cooling and access. The final voltage reduction near the processor also remains necessary.

## Ask what the current comparison actually proves

Conductor heating is I²R: current squared times resistance. If we deliberately hold the conductor resistance fixed, the 800-volt current is 48/800 of the 48-volt current. Squaring that ratio gives 0.0036. The calculated conductor loss is therefore 0.36 percent of the reference loss. This is a useful mechanism to understand. It is not a measured whole-facility energy saving.

A real comparison must also account for converter efficiency, cable geometry, insulation, connectors, fault clearing, grounding, load transients and service access. Changing the conductor size changes resistance, so it changes the comparison. Changing conversion stages changes other losses. Before moving the voltage control, predict that current will fall. Before recommending an architecture, identify which complete project constraint it would actually relieve.

## Close the conductor energy balance

Assume a 1 mΩ complete conductor loop, equal in both cases. Maintain 100 kW at the load end at either 48 V DC or 800 V DC. The source voltage covers the additional conductor drop.

The source supplies the load plus conductor heat: about 104.340 kW in the 48 V case and 100.016 kW in the 800 V case. Over one hour, the latter requires about 4.325 kWh less input. No energy is created.

This is still a DC-versus-DC conductor comparison. Converter and cooling losses are excluded.

At 48 V, I = 2,083.333 A and I²R = 4.340278 kW. At 800 V, I = 125 A and I²R = 0.015625 kW. Required sending voltages are about 50.083 V and 800.125 V respectively. Specifying receiving-end voltage is essential: silently treating 48 V as both the sending and receiving voltage would ignore the drop.

## Compare AC and DC arrangements at the same final load

Compare complete delivery paths serving the same 100 kW final DC load. The loss figures here are invented at this operating point. Both paths include their total conversion losses.

At the defaults, AC needs 100 + 1 + 4 = 105 kW and DC needs 100 + 0.1 + 3 = 103.1 kW. Over one hour, the DC arrangement uses 1.9 kWh less input.

Raise DC conversion loss to 6 kW: DC input becomes 106.1 kW and exceeds AC input. The advantage depends on the whole loss budget, not the AC/DC label alone.

The total conversion-loss input includes every converter within the selected delivery path; it is not an efficiency assumed for one unnamed device. Fixed losses here are supplied scenario values at one load point. Neither the 1 mΩ loop of the earlier example nor its losses carry into this separate comparison. Cooling and other facility overhead are outside both budgets.

## Worked example: The same power at two stated DC voltages

- Original synthetic 100 kW DC load; equal delivered power at the compared segment.
- 48 V and 800 V both mean conductor-to-return voltage; conductor resistance is held equal only for the loss-ratio comparison.

1. At 48 V: I = 100,000/48 = 2,083.3 A.
2. At 800 V: I = 100,000/800 = 125 A.
3. At fixed resistance: loss ratio = (125/2,083.3)² = 0.0036, or 0.36%.

**Result:** The higher-voltage segment carries less current. No total architecture efficiency or installed facility capacity has yet been calculated.

**Model boundary:** Ideal DC comparison, with no converter, protection, insulation, thermal-rating or cost model. The architecture selector and current controls deliberately answer separate questions.

## The tradeoff

Choice: Place a converter in a nearby sidecar.

Benefit: Move conversion equipment and some heat out of the compute rack.

Cost: Use space and service capacity elsewhere while retaining the existing upstream AC constraints.

## When the situation changes

Trigger: The new rack-power interface fits, but the room already has a binding cooling limit.

Mechanism: Changing electrical distribution does not automatically add heat-rejection capacity.

Response: Close the electrical and thermal ledgers at the same boundary before claiming more usable racks.

## Apply the idea

Keep the AC path at 1 kW conductor loss plus 4 kW total conversion loss. The DC path has 0.1 kW conductor loss, but its total conversion loss rises to 6 kW. Both supply a 100 kW final DC load for one hour. Which needs more input energy, and by how much?

<details>
<summary>Reveal the worked answer</summary>

AC needs 105 kWh. DC needs 106.1 kWh. DC uses 1.1 kWh more input energy in this hypothetical comparison.

Add all path losses to the same delivered load before multiplying by the common duration. The DC conductor loss is lower, but the conversion loss is sufficiently higher to reverse the total-energy advantage.

</details>

**The idea to keep:** Higher voltage can reduce conductor loss. Lower whole-path energy input depends on all losses at equal useful output; energy is conserved.

## Sources and reading boundaries

- [Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) — Provides context for higher-voltage DC distribution and conversion placement. All voltages, loads, loop resistance and loss budgets used in calculations are explicitly original teaching assumptions. Read 2026-09-08. August 11, 2026 vendor roadmap. Proposed architecture and availability expectations are distinct from a verified installed deployment.
