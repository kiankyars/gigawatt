# A believable number can describe the wrong thing

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d14-telemetry-and-observability`, then run `uv run gigawatt-expand`.

**D14 · Authored draft · Objectives:** D14.1

Place measurements at physical boundaries, align their times and use conservation checks to discriminate between competing explanations.

**Driving question:** How do we distinguish a real cooling constraint from a measurement problem?

## Give every measurement a location and a meaning

A temperature value needs a physical location. A supply temperature before a mixing junction is not necessarily the temperature reaching a rack; a return value from one branch may not describe the entire loop. A power value needs an electrical boundary. A flow value needs to say whether it is measured, commanded or inferred. Without these labels, combining individually plausible numbers can produce a calculation that corresponds to no actual piece of the system.

Time is equally important. One meter may report an instantaneous sample, another a minute average, and a third its most recent successful value. A plot that places them at the same horizontal position can imply a relationship their acquisition times do not support. Preserve the observation timestamp, the reporting timestamp and the aggregation interval where they differ. A missing measurement should remain missing instead of being interpreted as zero or silently held forever.

Google’s SRE monitoring discussion distinguishes observations of internal behavior from observations of externally experienced service. The same distinction helps facilities reasoning. A pump’s reported running state is an internal status; adequate flow at the required interface is a process observation; successful useful work is a service observation. Each can disagree with another without being contradictory, because they measure different parts of the causal chain.

## Use a balance to ask a sharper question

Our hypothetical loop removes a steady 2.09 MW. At 100 kg/s and a stipulated specific heat of 4.18 kJ/(kg·K), a 5 K temperature rise gives Q = 100 × 4.18 × 5 = 2,090 kW. Now the displayed temperature rise becomes 10 K while the flow screen still shows 100 kg/s. The same calculation reports 4.18 MW. Does that prove the computers doubled their heat output? No: the calculation depends on whether the measurements represent the same flow and interval.

Several explanations remain possible. Actual heat input may have changed; the flow reading may be stale; temperature locations may not enclose the intended load; or heat may be accumulating or leaving stored material during a transient. A good diagnosis proposes an observation that separates these cases. In the supplied scenario, an independent time-aligned measurement establishes that actual flow fell to 50 kg/s while electrical heat input stayed at 2.09 MW. That evidence closes the balance at the larger temperature rise.

The independent observation is essential. Without it, choosing the stale-flow explanation simply because it fits the story would be guessing. Even after the balance closes, the reason for reduced flow remains a separate question. A valve position, pump speed, pressure difference or blockage hypothesis needs relevant evidence. Conservation is a powerful consistency check, but it is not a magic sensor that identifies every mechanism from one alarm.

## Design monitoring around decisions

A useful sensor arrangement begins with the decisions operators need to make. To determine whether a heat exchanger is meeting its role, instrument the appropriate entering and leaving conditions on the relevant loops. To distinguish excessive electrical load from reduced thermal capacity, align power and process measurements. To understand service impact, inspect job throughput or latency at the same time. Adding many sensors without an explanatory model can increase uncertainty rather than reduce it.

Alarm design should also distinguish a symptom from an actionable condition. A single brief spike, a sustained excursion and stale data may require different interpretation. Choose thresholds, delays and severity through the actual operating requirements and evidence; this course does not invent universal temperature or alarm values. Document what an alarm means and what additional information supports the approved response. Otherwise, repeated ambiguous alarms train people to ignore signals that may eventually matter.

Keep the diagnostic record reproducible. Preserve raw samples when available, transformations, units, sensor identity, known quality issues and the time range used for the calculation. An incident graph should separate observed values from inferred quantities and hypotheses. When a sensor is corrected, retain the reason rather than rewriting history as though the earlier false reading never existed. That record lets future operators distinguish a recurring physical problem from a recurring measurement failure.

## Worked example: One stale flow value doubles the apparent heat

- Synthetic steady loop with cp = 4.18 kJ/(kg·K).
- Initial actual flow 100 kg/s and temperature rise 5 K.
- Later independent measurements show actual flow 50 kg/s and rise 10 K; the original flow display is stale at 100 kg/s.

1. Initial consistent duty — 100 × 4.18 × 5 = 2,090 kW — The three quantities refer to the same loop and interval.
2. Misleading display-based duty — 100 × 4.18 × 10 = 4,180 kW — The stale value creates an apparent doubling.
3. Correct time-aligned duty — 50 × 4.18 × 10 = 2,090 kW — The independent observation establishes the reduced flow and restores the balance.

**Result:** The apparent heat increase was a measurement-combination error; the actual flow reduction still needs its own cause analysis.

**Model boundary:** The diagnostic outcome is stipulated for the synthetic trace. It is not a universal inference from a higher return temperature.

## The tradeoff

Choice: Add independent process and service observations.

Benefit: They can distinguish sensor faults from actual constraints and reveal whether a component issue affects useful work.

Cost: Sensors, calibration, timestamps, data retention and interpretation create ongoing operational work; more points alone do not establish observability.

## When the situation changes

Trigger: A communication failure freezes a flow value without a visible quality flag.

Mechanism: A valid-looking old number is combined with current temperatures, producing a false heat calculation.

Response: Identify data age and quality, compare independent evidence and restore a trustworthy measurement path through the approved operating process.

## Apply the idea

You observe a doubled temperature difference and unchanged displayed flow, but have no independent flow or aligned power data. Can you conclude that flow halved?

<details>
<summary>Reveal the worked answer</summary>

No. Halved flow is one hypothesis, not an established diagnosis.

Changed heat input, temperature-sensor error, different measurement boundaries and transient storage can also alter the calculated relationship. State the missing observations: synchronized load measurements, actual flow at the same interface, sensor location/quality and the relevant time behavior. The appropriate next step is an evidence check, not a guessed operational adjustment.

</details>

**The idea to keep:** An alarm is evidence of a reported condition. A diagnosis requires consistent measurements that distinguish its possible causes.

## Sources and reading boundaries

- [Google SRE: Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) — The monitoring discussion distinguishes internal and external observations and separates symptoms from causes. Read 2026-09-06. Selected monitoring principles inspected; this lesson’s thermal trace, numerical diagnostic and sensor placement examples are original.
