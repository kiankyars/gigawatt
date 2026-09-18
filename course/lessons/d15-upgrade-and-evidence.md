# Abilene: commercial roles and delivery

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d15-upgrade-and-evidence`, then run `uv run gigawatt-expand`.

**15. GPU cloud economics · Authored draft**

Compare the original target with a dated report of the same milestone.

**Driving question:** How did the public delivery reports compare with the announced plan?

## Separate the commercial layers

The original Abilene campus links Crusoe’s facility development, Oracle’s cloud infrastructure and OpenAI’s workloads. A megawatt of facility capacity and a GPU cluster available to a customer are different deliverables. The public first-phase report establishes operating OCI and early workloads; it does not disclose every private ownership, financing or service agreement.

This case remains about the Oracle/OpenAI campus. The neighboring Microsoft project is not required to explain these milestones and is omitted from the presentation. The photograph supplies site context; it does not independently establish the status of every hall.

## First phase: target and reported event

On March 18, 2025, Crusoe targeted energization of the first two buildings for the first half of 2025. Its September 30 report says they were energized within a year of construction starting in June 2024, with the first NVIDIA GB200 racks arriving in June 2025. That report also describes early training and inference workloads. Its publication in September does not mean energization occurred in September.

The first-phase accounts are broadly consistent with the stated half-year energization target. They do not provide a detailed daily commissioning log or the exact start of every customer service obligation. Do not substitute the press-release date for the event date.

## Expansion: construction and customer delivery

The March 2025 expansion announcement targeted completion of six additional buildings in mid-2026. Oracle’s September 2026 update says 75 percent of capacity had been delivered, with the remainder expected in following quarters. That provides a useful comparison with the original ambition, but it changes the milestone from construction completion to customer delivery.

These reports do not support calculating a precise schedule slip. Nor does the percentage establish operating IT demand: its delivery denominator is not defined well enough to multiply it by the campus’s announced 1.2 GW. The relevant commercial question is which contracted capacity was available on which date. Answering it requires the agreed delivery milestone and the corresponding completion record.

## Worked example: Read the date of the event, not just the announcement

- Crusoe plan published March 18, 2025; first two buildings targeted for energization in 1H 2025.
- September 30, 2025 report states energization within one year of June 2024 and first racks in June 2025.

1. Match the milestone — Energization → energization — Compare the same first-phase event.
2. Locate the event — By roughly June 2025, reported in September — Do not use publication date as the completion date.
3. Separate the expansion — Mid-2026 construction target versus September customer-delivery share — The two descriptions require another record before calculating delay.

**Result:** First-phase reporting is consistent with the half-year target; the expansion comparison is not a precise lateness calculation.

**Model boundary:** Only the original Oracle/OpenAI campus and named public records are included.

## The tradeoff

Choice: Use phased customer delivery.

Benefit: Completed portions can begin serving demand.

Cost: Later phases retain construction, commissioning and contractual delivery exposure.

## When the situation changes

Trigger: An analyst treats construction completion and delivered customer capacity as the same milestone.

Mechanism: A supposed schedule variance compares different events.

Response: Match scope and milestone before calculating a delay.

## Apply the idea

Does Oracle’s 75% capacity-delivery statement prove that 900 MW of IT demand was operating?

<details>
<summary>Reveal the worked answer</summary>

No. It does not define the matched power boundary or delivered-capacity denominator.

The 1.2 GW plan and a delivered share do not together supply a metered IT load.

</details>

**The idea to keep:** Compare the original target with a dated report of the same milestone.

## Sources and reading boundaries

- [Crusoe — Expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) — March 2025 first-phase energization and six-building construction targets. Read 2026-09-17. Keep construction, energization and customer delivery distinct.
- [Crusoe — Flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) — September 2025 report of first-phase energization and OCI workloads. Read 2026-09-17. Publication date differs from the reported energization and first rack-delivery dates.
- [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/) — September 2026 Abilene update reports 75 percent of capacity delivered. Read 2026-09-17. Delivery denominator and construction milestone are not matched; no inferred operating MW.

## Check your understanding: A high rate or a full commitment?

Pause and make a prediction, then compare your reasoning.

The same 1,024 GPUs can be fully committed at $2.50 per GPU-hour or rented at $4.00 per booked hour. Expected billable occupancy of the pool is between 50% and 80%.

**Pause and predict:** At what occupancy is annual revenue equal, and what does the comparison leave out?

<details>
<summary>Compare your reasoning</summary>

62.5% billable occupancy. Costs, delivery, customer credit and financing remain to be compared.

Equate $4 × occupancy to $2.50. The pool earns less at 50% and more at 80%. Billable occupancy means paid rental hours, not GPU compute utilization; a committed customer can pay while the GPU is idle.

</details>

**The next problem:** Bring the physical and commercial decisions together at Abilene; use the five reader exercises for optional practice.

Continue in **the integrated cases**: The servers stay powered. The service does not..
