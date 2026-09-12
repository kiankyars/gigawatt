# Attach a denominator and a date

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d01-metrics-and-evidence`, then run `uv run gigawatt-expand`.

**D01 · Authored draft · Objectives:** D01.3, D01.4

Reconcile facility and IT metrics, then separate engineering laws, scenarios, product specifications, and operating evidence.

**Driving question:** What does an efficiency or capacity claim actually establish?

## A ratio answers the question in its denominator

Suppose a facility meter records 240 MWh over a day. Matching IT meters record 192 MWh, including networking and storage. The ratio of facility to IT energy is 240 divided by 192, or 1.25. The overhead is 48 MWh. Relative to IT, that overhead is 48/192 = 25 percent; relative to total facility energy, it is 48/240 = 20 percent. Both percentages are correct. Their denominators differ, so their meanings differ.

For this lesson call 1.25 the observed daily facility-to-IT energy ratio. Do not silently present a one-day exercise as a compliant annual PUE report. Formal reporting rules define measurement categories and periods, and those requirements must be followed when claiming the metric. More fundamentally, an energy ratio over any period is not automatically the instantaneous power ratio at a hot afternoon peak or during an outage. An annual summary cannot supply an unmeasured plant operating curve.

Now add service. Assume the same system completes 96,000 successful jobs under a fixed workload definition that day. It uses 240,000 kWh divided by 96,000 jobs, or 2.5 kWh per completed job at the facility boundary. Using IT energy instead gives 2 kWh per job. These are different useful measurements. A compute-only submeter might give another value. State whether the job count includes failures, retries, and jobs that missed their deadline; otherwise the denominator can improve on paper while users receive a worse service.

## Compare outcomes without changing the test

Consider two hypothetical days with the same accepted workload and completion count. Day A uses 240 MWh facility energy and 192 MWh IT energy. Day B uses 228 MWh facility energy and 180 MWh IT energy. Day B has a slightly larger facility-to-IT ratio: 228/180 is about 1.267. Yet it uses less total energy for the same useful work. Its overhead remains 48 MWh while IT energy falls. Judging only by the overhead ratio would punish the better total-energy result.

Reverse the experiment. Add an unnecessary 20 MWh of IT consumption without changing useful output or facility overhead. The ratio falls because the denominator grows, even though total electricity use increases. This is not a reason to abandon overhead metrics. It is a reason to pair each metric with the outcome it cannot measure. Facility overhead, workload efficiency, resource use, and availability are separate questions. A dashboard should keep them separate rather than compressing them into one score.

The opening presentation uses a separate one-hour version of this counterexample: 100 identical jobs meet the same quality requirements in both cases. With 1,000 kWh of IT energy and 200 kWh overhead, facility energy is 1,200 kWh, PUE for the illustrative interval is 1.20, and energy per job is 12 kWh. Increase IT energy to 1,200 kWh while keeping overhead and completed work fixed: the facility uses 1,400 kWh, PUE falls to about 1.17, and energy per job rises to 14 kWh. The unchanged overhead is an assumption, and this one-hour calculation is not an annual PUE report.

Fair comparisons require matching conditions. A faster or lower-energy run at a different model quality, precision, input length, batch size, or failure policy is not automatically an improvement for the original service. Record the changed condition and decide whether it is acceptable. The same discipline applies to a site case: a source-side connection rating and a rack count collected months apart cannot be combined as though they were simultaneous measurements of one commissioned configuration.

## Sort evidence before drawing a conclusion

Classify six example statements. First, energy is conserved: that is a physical principle, with the chosen boundary determining the bookkeeping. Second, this exercise assumes each rack draws 100 kW: that is a teaching input. Third, a manufacturer's document rates a product at a specified voltage and load: that is a product specification under its stated conditions. Fourth, an operator reports that a particular building began a named workload on a particular date: that is a dated operating claim, whose scope is limited by the evidence supplied.

Fifth, a developer announces a future campus capacity: that establishes a stated intention, not installed equipment. Sixth, an analyst predicts a future architecture's market share: that is a forecast, not a measurement. A credible author can produce several of these evidence types in one article. Authority does not make the types interchangeable. Preserve the distinction in notes and diagrams so a forecast never quietly becomes the assumed as-built configuration of a real facility.

To call additional capacity operational, ask what complete service path has been established. The answer may require connection status, installed and accepted electrical equipment, cooling at the applicable conditions, configured IT, and actual workload evidence. Different questions need different documents. Commissioning reports establish tested behavior within their scope; they do not by themselves establish months of productive utilization. One building may be operating while the rest of the campus is still in construction.

The practical payoff is precision rather than skepticism for its own sake. You can calculate confidently when the scenario supplies the necessary inputs, and you can stop cleanly when a real claim does not. Mark the missing fact and the evidence that would resolve it. That produces a useful question for an operator or source author instead of a spurious decimal produced by multiplying unrelated headline numbers.

## Worked example: An overhead ratio can rise while energy per job improves

- Both days complete 96,000 identical accepted jobs.
- Facility and IT energy use matching daily intervals.
- The exercise is not an annual PUE report.

1. Day A ratio — 240 / 192 = 1.25 — Facility energy is the numerator and IT energy the denominator.
2. Day B ratio — 228 / 180 = 1.267 — Fixed 48 MWh overhead occupies a larger share of the reduced IT total.
3. Day A service energy — 240,000 / 96,000 = 2.50 kWh/job — Convert MWh to kWh before dividing.
4. Day B service energy — 228,000 / 96,000 = 2.375 kWh/job — The same accepted service uses five percent less facility energy.

**Result:** Day B improves energy per job despite a higher overhead ratio.

**Model boundary:** This comparison holds service quality, workload definition, completion count, and time window fixed.

## The tradeoff

Choice: Optimize an overhead metric alone.

Benefit: It highlights facility energy outside IT and helps track that category.

Cost: It cannot establish computing productivity and can move opposite to total energy per useful result.

## When the situation changes

Trigger: Combine an announced connection with an unrelated rack specification to report operating compute.

Mechanism: The calculation supplies missing deployment, configuration, and utilization facts without evidence.

Response: Label the output as a conditional scenario or leave the operating quantity unknown.

## Apply the idea

A facility uses 150 MWh while IT uses 120 MWh. Is its 30 MWh overhead 20 percent or 25 percent?

<details>
<summary>Reveal the worked answer</summary>

It is 20 percent of facility energy and 25 percent of IT energy.

Thirty divided by 150 is 0.20; thirty divided by 120 is 0.25. Neither ratio says how many useful jobs the site completed.

</details>

**The idea to keep:** A useful claim has a defined boundary, time window, evidence type, and limit on what follows from it.

## Sources and reading boundaries

- [DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) — Facility efficiency metrics require defined IT and facility boundaries. Read 2026-09-06. Read relevant metrics discussion; this lesson intentionally uses daily ratios rather than claiming standards-compliant annual PUE.
- [MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) — Benchmark energy/performance comparisons declare workload scenarios and measurement boundaries. Read 2026-09-06. Read the public benchmark and power-measurement descriptions, not every result or implementation.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Commissioning and documented performance validation have a defined scope and evidentiary role. Read 2026-09-06. Read the public framework discussion; no project report or full paid standard was reviewed.
- [The Green Grid — PUE: A Comprehensive Examination of the Metric](https://datacenters.lbl.gov/sites/default/files/WP49-PUE%20A%20Comprehensive%20Examination%20of%20the%20Metric_v6.pdf) — PUE compares facility energy with IT equipment energy and cannot by itself establish useful-work efficiency. Read 2026-09-11. Reviewed printed pages 8–9, 14–22 and 34. Original one-hour counterexample; no current standards compliance or measured annual PUE is claimed.
