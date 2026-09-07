# Measure the service, investigate the incident

**D14 · Authored draft · Objectives:** D14.3, D14.4, D14.5

Evaluate maintenance against surviving capacity, calculate a defined service metric and build an evidence-based incident explanation.

**Driving question:** Why do equipment uptime and a redundant topology fail to determine useful-service availability?

## Maintenance consumes a real configuration

Two 3 MW paths do not support a 5 MW load during maintenance of one path if the remaining path can carry only 3 MW. Adding their normal ratings hides the maintenance condition. Three such units might preserve 6 MW after one is removed, but only if their distribution, controls and other dependencies permit the required surviving arrangement. Count the functions available in the actual maintenance state, not the number of equipment symbols.

Uptime Institute distinguishes concurrent maintainability and fault-tolerant infrastructure in its Tier descriptions. Those are topology and performance concepts within a defined framework, not measured uptime percentages that can be assigned to an arbitrary sketch. Its operations criteria also address staffing, maintenance tracking, procedures and incident learning. A design’s intended behavior therefore has to be supported by operating practice and evidence, rather than presumed from installed spares.

A maintenance plan needs a starting configuration, the stated scope of work, surviving service conditions, relevant dependencies and the reviewed restoration condition. Physical access and the possibility of another failure during the work matter too. This lesson evaluates hypothetical capacity and evidence requirements. It does not provide a switching or isolation procedure; actual work requires the applicable qualified process.

## Define what counts as unavailable

A component can remain powered while the service misses its latency or completion requirement. Conversely, one component can be unavailable while the service continues through another path. A service-level indicator makes the chosen observable boundary explicit. For a time-based example, specify which intervals count as unavailable; for a request-based measure, specify which requests and outcomes belong in the denominator. Google’s SRE discussion of service-level objectives emphasizes this measurement contract.

In a synthetic thirty-day observation period there are 43,200 minutes. One service incident covers twelve minutes and another eighteen, with four minutes of overlap. The union of unavailable time is 12 + 18 − 4 = 26 minutes. The time-based availability is (43,200 − 26)/43,200 ≈ 99.9398 percent. Adding the two durations without removing overlap counts the same service outage twice. Counting only a failed component’s power loss may miss the application recovery period.

Probabilistic redundancy formulas require assumptions. If two fully sufficient paths have independent unavailability u, their simultaneous unavailability is u² in that simplified model. Shared power, software, configuration, repair resources or environmental events can invalidate independence. If either path alone lacks the capacity required by the load, even the success condition is different. A neat probability calculation is useful only after the physical and service model has been established.

## An incident explanation separates observation from hypothesis

Consider an original timeline: a configuration changes at 10:00, alarms appear at 10:02, jobs miss their requirement at 10:03, configuration recovery is recorded at 10:11, physical conditions stabilize at 10:16 and service recovery is confirmed at 10:22. This supports a nineteen-minute service-impact interval if the stated criterion failed continuously from 10:03. The time ordering makes the configuration change a hypothesis worth investigating, not proof of the entire causal chain.

Preserve evidence that distinguishes alternatives: the affected configuration and scope, telemetry quality, equipment states, job behavior and the timing of recovery actions. A useful corrective action names a mechanism, an owner and a way to verify the improvement. Rewriting an instruction is different from testing that a common failure path has been removed. Training is different from proving the system now constrains the same erroneous action.

Google’s postmortem guidance emphasizes learning rather than assigning personal blame. In the course, that becomes a practical standard for explanations: describe the conditions that allowed an action or failure to propagate, and specify what evidence would demonstrate prevention or reduced impact. Maintain an honest unresolved section when the cause remains uncertain. A confident but unsupported story can make the next incident harder to diagnose by teaching the organization to look in the wrong place.

## Worked example: A service-time denominator with overlapping incidents

- Synthetic 30-day period: 43,200 minutes.
- Incident A affects the defined service for 12 minutes; incident B for 18 minutes.
- Their service-impact intervals overlap for 4 minutes; no other unavailability occurs.

1. Unavailable union — 12 + 18 − 4 = 26 min — Subtract the shared interval once.
2. Available fraction — (43,200 − 26)/43,200 = 0.999398… — The denominator covers the complete stated observation interval.
3. Percentage — 0.999398… × 100 ≈ 99.9398% — This is a retrospective time-based metric under the exercise definition.

**Result:** The synthetic service availability is about 99.94 percent; the number is not a topology certification or future guarantee.

**Model boundary:** Request success, degraded performance outside the chosen criterion and other periods are not inferred.

## The tradeoff

Choice: Schedule maintenance with explicit surviving capacity and recovery provisions.

Benefit: It can preserve service while limiting deferred equipment work.

Cost: It uses staff, reserve and scheduling flexibility; the required margin depends on the actual service and additional-failure assumptions.

## When the situation changes

Trigger: A shared configuration action changes both nominally independent paths.

Mechanism: Common cause defeats the independence assumed by a component-availability calculation.

Response: Reconstruct the event using verified records and test whether the proposed change actually limits its scope or consequence.

## Apply the idea

In a 60-minute window, ten minutes violate the specified latency objective even though every server remains powered. What is time-based service availability under that criterion?

<details>
<summary>Reveal the worked answer</summary>

50/60 = 83.33 percent for that one-hour window.

Power availability is a different indicator. The service failed its stated latency criterion during ten minutes, so those minutes belong in the unavailable set. This result should not be extrapolated to a month or combined with request-success percentages without reconciling their denominators and observation scopes.

</details>

**The idea to keep:** Reliability claims need a service boundary, dependence assumptions and an operating record. A topology label or component average is not the result.

## Sources and reading boundaries

- [Tier Classification System](https://uptimeinstitute.com/tiers) — Public Tier descriptions distinguish concurrent maintainability and fault tolerance. Read 2026-09-06. Relevant definitions inspected; the lesson neither assigns a Tier nor claims certification for its synthetic arrangements.
- [Management and Operations Guideline](https://uptimeinstitute.com/professional-services/management-operations/mando-criteria) — Maintenance tracking, staffing and incident learning are operational concerns beyond equipment topology. Read 2026-09-06. Selected category descriptions reviewed; no proprietary assessment or complete procedure is reproduced.
- [Google SRE: Service Level Objectives](https://sre.google/sre-book/service-level-objectives/) — Service indicators and objectives need explicitly defined measurements. Read 2026-09-06. Selected metric-boundary discussion reviewed; the availability example is original.
- [Google SRE: Postmortem Culture](https://sre.google/sre-book/postmortem-culture/) — Incident review is intended to support learning and improvement rather than blame. Read 2026-09-06. Selected postmortem principles inspected; timeline and proposed evidence questions are original.
