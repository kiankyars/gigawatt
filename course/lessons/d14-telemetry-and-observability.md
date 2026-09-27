# A believable number can describe the wrong thing

**14. Controls, operations and reliability**

Place measurements at physical boundaries, align their times and use conservation checks to discriminate between competing explanations.

**Driving question:** How do we distinguish a real cooling constraint from a measurement problem?

## Give every measurement a location and a meaning

A temperature value needs a physical location. A supply temperature before a mixing junction is not necessarily the temperature reaching a rack; a return value from one branch may not describe the entire loop. A power value needs an electrical boundary. A flow value needs to say whether it is measured, commanded or inferred. Without these labels, combining individually plausible numbers can produce a calculation that corresponds to no actual piece of the system.

Time is equally important. One meter may report an instantaneous sample, another a minute average, and a third its most recent successful value. A plot that places them at the same horizontal position can imply a relationship their acquisition times do not support. Preserve the observation timestamp, the reporting timestamp and the aggregation interval where they differ. A missing measurement should remain missing instead of being interpreted as zero or silently held forever.

Google’s discussion of monitoring in site reliability engineering (SRE) distinguishes observations of internal behavior from observations of externally experienced service. The same distinction helps facilities reasoning. A pump’s reported running state is an internal status; adequate flow at the required interface is a process observation; successful useful work is a service observation. Each can disagree with another without being contradictory, because they measure different parts of the causal chain.

## Use a balance to ask a sharper question

Row B’s twenty racks draw 2.09 MW, and all of that heat enters the row’s water branch. Before the fault the branch carries 100 kg/s from a 30°C supply to a 35°C return. Taking the specific heat of water as 4.18 kJ/(kg·K), the balance is Q = 100 × 4.18 × 5 = 2,090 kW, and the hottest measured chip runs at 70°C against an 80°C operating limit. Then the flow halves to 50 kg/s while the supply stays at 30°C.

At the old 5 K rise, 50 kg/s carries only 50 × 4.18 × 5 = 1,045 kW, half the heat arriving. The other half accumulates in the coolant, the cold plates and the chips, and temperatures climb until the return reaches 40°C. There the 10 K rise carries the full load again: 50 × 4.18 × 10 = 2,090 kW. The water balance closes at both operating points.

The chips tell a different story. At the new equilibrium the hottest measured chip reads 85°C, above its 80°C limit, while the plant dashboard still shows a normal 30°C supply. The water balance describes the water, so it cannot show this. Chip temperature is a separate measurement, and the dashboard has to show it beside the plant readings.

A closed balance says the heat is leaving; it does not say why the flow fell. A valve position, pump speed, pressure difference or blockage hypothesis each needs its own evidence. Conservation is a strong consistency check, and the diagnosis still comes from measurements that separate one cause from another.

Extension: the same numbers from a stale reading. Suppose the flow display had frozen at 100 kg/s when the real flow halved. Multiplying the frozen 100 kg/s by the new 10 K rise reports 100 × 4.18 × 10 = 4,180 kW, as if the racks had doubled their heat output. Several explanations fit that number: the heat input really changed, the flow reading is stale, the temperature sensors do not enclose the intended load, or heat is moving into or out of stored material during a transient. An independent, time-aligned flow measurement of 50 kg/s and an electrical load still at 2.09 MW separate them, and the balance closes at 2,090 kW. Without that observation, picking the stale-flow explanation because it fits the story would be a guess.

## Design monitoring around decisions

A useful sensor arrangement begins with the decisions operators need to make. To determine whether a heat exchanger is meeting its role, instrument the appropriate entering and leaving conditions on the relevant loops. To distinguish excessive electrical load from reduced thermal capacity, align power and process measurements. To understand service impact, inspect job throughput or latency at the same time. Adding many sensors without an explanatory model can increase uncertainty rather than reduce it.

Alarm design should also distinguish a symptom from an actionable condition. A single brief spike, a sustained excursion and stale data may require different interpretation. Set thresholds, delays and severity from the site’s operating requirements and evidence. Document what an alarm means and what additional information supports the approved response. Otherwise, repeated ambiguous alarms train people to ignore signals that may eventually matter.

Keep the diagnostic record reproducible. Preserve raw samples when available, transformations, units, sensor identity, known quality issues and the time range used for the calculation. An incident graph should separate observed values from inferred quantities and hypotheses. When a sensor is corrected, retain the reason rather than rewriting history as though the earlier false reading never existed. That record lets future operators distinguish a recurring physical problem from a recurring measurement failure.

## Worked example: Row B’s water balance closes while its hottest chip overheats

- Row B: twenty racks draw 2.09 MW, all of it transferred to the row’s water branch; water cp = 4.18 kJ/(kg·K).
- Before the flow drop: 100 kg/s, 30°C supply, 35°C return, hottest measured chip 70°C. At the later equilibrium: 50 kg/s, 30°C supply, 40°C return, hottest measured chip 85°C. The chip operating limit is 80°C.
- Chip temperatures are measurements, not results of the water balance. No settling time is given.

1. Before the flow drop — 100 × 4.18 × 5 = 2,090 kW — At equilibrium the water removes all the heat the racks produce.
2. Just after the flow halves — 50 × 4.18 × 5 = 1,045 kW — Removal falls to half the input, so heat accumulates and temperatures rise.
3. New equilibrium — 50 × 4.18 × 10 = 2,090 kW — The larger rise restores removal to the full load at a hotter operating point.
4. Chip check — 85°C > 80°C limit — The balance closes, and the chip is over its limit while the supply water reads a normal 30°C.

**Result:** Row B’s water removes all 2.09 MW at both equilibria, yet its hottest chip runs 5 K over the limit. The next step is local evidence for why the row’s flow fell.

**Model boundary:** The chip temperatures and the 80°C limit are scenario inputs, not a rating for a named graphics processing unit (GPU). The water balance gives neither chip temperature nor how long the transition takes.

## When the situation changes

Trigger: A communication failure freezes a flow value without a visible quality flag.

Mechanism: The frozen 100 kg/s is combined with a current 10 K rise, so the dashboard reports 4.18 MW for a loop that still removes 2.09 MW.

## Apply the idea

You observe a doubled temperature difference and unchanged displayed flow, but have no independent flow or aligned power data. Can you conclude that flow halved?

<details>
<summary>Reveal the worked answer</summary>

No. Halved flow is one hypothesis, not an established diagnosis.

Changed heat input, temperature-sensor error, different measurement boundaries and transient storage can also alter the calculated relationship. State the missing observations: synchronized load measurements, actual flow at the same interface, sensor location/quality and the relevant time behavior. The appropriate next step is an evidence check, not a guessed operational adjustment.

</details>

**The idea to keep:** An alarm is evidence of a reported condition. A diagnosis requires consistent measurements that distinguish its possible causes.

## Sources

- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — sre.google · Reviewed 2026-09-06. The monitoring discussion distinguishes internal and external observations and separates symptoms from causes.
