# Measure the service, investigate the incident

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d14-maintenance-and-service-reliability`, then run `uv run gigawatt-expand`.

**14. Controls, operations and reliability · Authored draft**

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

## Case: Cloudflare tested less than the failure removed

Cloudflare’s November 2023 account identifies a gap between testing the high-availability portion of PDX-04 and losing the entire PDX-04 facility. Some application dependencies existed only at the failed site. Edge traffic continued, while control-plane and analytics services were disrupted. A useful test record therefore names the removed facility functions and the user-facing service that was observed, rather than merely recording that failover passed.

## Case: A repeated failure tests the corrective work

Cloudflare subsequently added capacity, changed failover behavior and tested a full-facility cut. During the March 26, 2024 power failure, APIs and dashboards were operating normally seven minutes after power loss, without manual intervention. Analytics recovered later. The comparison shows why corrective actions need a defined verification endpoint: API recovery, analytics recovery and a complete facility cold start measure different outcomes.

## Case: Cooling recovery is not service recovery

Google’s final July 2022 europe-west2 incident summary separates a cooling repair at 14:13 PDT on July 19 from initial cloud-service restoration at 04:28 PDT on July 20: another 14 hours 15 minutes. Some residual recovery continued beyond that milestone. The response also briefly widened the disruption through a routing change that avoided three zones rather than the affected one.

When reviewing such an incident, distinguish the physical repair, configuration scope and application restart dependencies. An operating plan must verify the service after the infrastructure returns, and an incident timeline must retain the remaining exceptions.

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
- [Cloudflare — Post mortem on the Cloudflare Control Plane and Analytics Outage](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/) — A November 2, 2023 facility power failure disrupted control-plane and analytics services. Cloudflare reports undiscovered facility dependencies and a test scope that covered the high-availability portion of PDX-04 rather than the entire PDX-04 facility. Most control-plane service returned at the disaster-recovery facility at 17:57 UTC on November 2. Read 2026-09-16. Use Cloudflare’s own application, monitoring and test-scope observations. Its reconstruction of the utility/generator chain expressly includes unconfirmed hypotheses; do not present the DSG program or grid-maintenance causation as established. The article’s opening has 11:43/11:44 start-time variation, so avoid minute-exact before/after ratios. General network traffic was not equivalent to the affected control-plane service.
- [Cloudflare — Major data center power failure (again): Cloudflare Code Orange tested](https://blog.cloudflare.com/major-data-center-power-failure-again-cloudflare-code-orange-tested/) — After capacity expansion and failover changes, Cloudflare ran a facility cut test in February 2024. A March 26 power failure began at 14:58 UTC; APIs and dashboards operated normally by 15:05 without human intervention. Analytics required longer recovery. Read 2026-09-16. Compare the defined API/dashboard endpoint; do not say every service recovered in seven minutes. The article reports approximately 72 versus 10 hours for facility cold starts, a different endpoint from API availability. Breaker-setting causation is a reported initial assessment, not an independently verified final RCA. PDX01 is the same facility discussed in the November account using the earlier PDX-04 name.
- [Google Cloud — July 2022 europe-west2 cooling incident report](https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2) — During extreme heat, simultaneous cooling failures affected part of europe-west2-a on July 19, 2022. The final report’s summary gives shutdown at 10:05 PDT, cooling repair at 14:13, and initial cloud-service restoration at 04:28 PDT July 20. Recovery work therefore continued for 14 hours 15 minutes after cooling returned. An incorrect routing change initially avoided all three zones rather than the affected zone. Read 2026-09-16. Use the final July 29 summary, not the superseded July 21 preliminary timings. These are reported milestone endpoints, not a uniform downtime for every customer; small residual issues required longer recovery. The per-product detail includes additional dates beyond the summary, so do not equate its aggregate endpoint with every final manual cleanup. No public London-site photograph is identified here; the DeepMind photo must not be labeled as this outage site.

## Check your understanding: One reassuring number

Pause and make a prediction, then compare your reasoning.

A hypothetical rack reports high device temperatures while the plant's displayed supply temperature looks normal. The plant reading is ten minutes old, and there is no current measurement of flow through the affected rack branch.

**Pause and predict:** Does the normal plant reading establish that rack cooling is adequate? Identify the next evidence you need.

<details>
<summary>Compare your reasoning</summary>

No. Obtain time-aligned measurements at the affected rack's thermal and flow boundaries before choosing a cause.

A stale upstream temperature cannot establish current local flow or heat transfer. Current branch flow, supply and return temperatures, device temperatures and load history can help distinguish restricted flow, a changed load and faulty telemetry. The alarm alone does not select among them.

</details>

**The next problem:** Measurements reveal the constraint. Which intervention changes usable service enough to justify its cost and delivery time?

Continue in **Capacity, cost and system decisions**: Find the constraint after reconciling the boundaries.
