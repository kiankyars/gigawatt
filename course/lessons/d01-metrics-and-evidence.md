# Attach a denominator and a date

**2. Data center overview**

Reconcile facility and IT metrics, then separate engineering laws, scenarios, product specifications, and operating evidence.

**Driving question:** What does an efficiency or capacity claim actually establish?

## A ratio answers the question in its denominator

Suppose a facility meter records 1,800 kilowatt-hours (kWh) over one hour, while matching IT meters record 1,500 kWh, including networking and storage. The ratio of facility to IT energy is 1,800 divided by 1,500, or 1.20. The overhead is 300 kWh. Relative to IT, that overhead is 300/1,500 = 20 percent; relative to total facility energy, it is 300/1,800 ≈ 16.7 percent. Both percentages are correct. Their denominators differ, so their meanings differ.

That ratio of facility energy to IT energy over the same interval is the facility’s power usage effectiveness (PUE) for that hour. Formal PUE reporting defines measurement categories and periods, and a published figure normally follows those rules, so label a one-hour or one-day ratio with its interval and keep it apart from an annual report. An energy ratio over any period also differs from the instantaneous power ratio at a hot afternoon peak or during an outage, and an annual summary cannot supply an unmeasured plant operating curve.

Now add service. Assume that hour completes 600 accepted jobs under a fixed workload definition. It uses 1,800 kWh divided by 600 jobs, or 3.0 kWh per completed job at the facility boundary. Using IT energy instead gives 2.5 kWh per job. These are different useful measurements. A compute-only submeter might give another value. State whether the job count includes failures, retries, and jobs that missed their deadline; otherwise the denominator can improve on paper while users receive a worse service.

## Compare outcomes without changing the test

Start by isolating facility overhead. Hold the installed IT, the completed workload and the hour’s IT energy at 1,500 kWh. Reduce supporting-system energy from 300 to 150 kWh: facility energy falls from 1,800 to 1,650 kWh, PUE for the hour falls from 1.20 to 1.10, and facility energy per job falls from 3.0 to 2.75 kWh. IT capacity and actual IT energy both stay fixed, and they remain distinct quantities. The overhead reduction is an assumed input. In the lab below, the same facility runs for a whole day: 36 MWh of IT energy, 7.2 MWh of overhead and 14,400 accepted jobs give PUE 1.2 and 3 kWh per job, and cutting overhead to 3.6 MWh gives PUE 1.1 and 2.75 kWh per job.

Fair comparisons require matching conditions. A faster or lower-energy run at a different model quality, precision, input length, batch size, or failure policy is not automatically an improvement for the original service. Record the changed condition and decide whether it is acceptable. The same discipline applies to a site case: a source-side connection rating and a rack count collected months apart cannot be combined as though they were simultaneous measurements of one commissioned configuration.

## Extension: a higher ratio can mean less energy per job

Run the baseline facility for a full day. Day A uses 36 MWh of IT energy and 7.2 MWh of overhead, 43.2 MWh in all, and completes 14,400 accepted jobs at 3.0 kWh each. Day B completes the same 14,400 jobs with 30 MWh of IT energy while overhead stays at 7.2 MWh. Day B’s ratio rises to 37.2/30 = 1.24, yet it uses 37.2 MWh, about 2.58 kWh per job and 14 percent less energy for the same useful work. Judging only by the overhead ratio would punish the better total-energy result.

Reverse the experiment. Add an unnecessary 6 MWh of IT consumption to Day A without changing useful output or facility overhead. The ratio falls to 49.2/42 ≈ 1.17 because the denominator grows, even though total electricity use increases. Overhead metrics still earn their place; pair each one with the outcome it cannot measure. Facility overhead, workload efficiency, resource use and availability are separate questions, and a dashboard should keep them separate rather than compressing them into one score. In the lab, set IT energy to 30 MWh to see Day B.

## Sort evidence before drawing a conclusion

Classify six example statements. First, energy is conserved: that is a physical principle, with the chosen boundary determining the bookkeeping. Second, the ledger in “One rack, three paths” assumes each of ten GB300 racks draws 142 kW: that is a teaching input. Third, a manufacturer's document rates a product at a specified voltage and load: that is a product specification under its stated conditions. Fourth, an operator reports that a particular building began a named workload on a particular date: that is a dated operating claim, whose scope is limited by the evidence given.

Fifth, a developer announces a future campus capacity: that shows a stated intention, not installed equipment. Sixth, an analyst predicts a future architecture's market share: that is a forecast, not a measurement. A credible author can produce several of these evidence types in one article. Authority does not make the types interchangeable. Preserve the distinction in notes and diagrams so a forecast never quietly becomes the assumed as-built configuration of a real facility.

To call additional capacity operational, ask which complete service path has been shown to work. The answer may require connection status, installed and accepted electrical equipment, cooling at the applicable conditions, configured IT, and actual workload evidence. Different questions need different documents. Commissioning reports show tested behavior within their scope, while months of productive utilization need operating records. One building may be operating while the rest of the campus is still in construction.

The practical payoff is precision rather than skepticism for its own sake. You can calculate confidently when the scenario supplies the necessary inputs, and you can stop cleanly when a real claim does not. Mark the missing fact and the evidence that would resolve it. That produces a useful question for an operator or source author instead of a spurious decimal produced by multiplying unrelated headline numbers.

## Worked example: Lower overhead at the same IT energy

- Installed IT, completed work and IT energy stay fixed at 1,500 kWh over one hour.
- Supporting-system energy falls from 300 to 150 kWh; the reduction is assumed.
- The hour completes 600 identical accepted jobs.
- The ratio covers one hour; it is not an annual PUE report.

1. Baseline facility energy — 1,500 + 300 = 1,800 kWh — Facility energy is IT energy plus overhead over the same hour.
2. Baseline PUE — 1,800 / 1,500 = 1.20 — Facility energy is the numerator and IT energy the denominator.
3. Lower overhead — 1,500 + 150 = 1,650 kWh; 1,650 / 1,500 = 1.10 — Only the numerator changes, because IT energy is held fixed.
4. Energy per job — 1,800 / 600 = 3.0 kWh → 1,650 / 600 = 2.75 kWh — With the work fixed, the overhead saving also shows up per completed job.

**Result:** PUE falls from 1.20 to 1.10 and facility energy per job from 3.0 to 2.75 kWh, while IT energy stays at 1,500 kWh.

**Model boundary:** This comparison holds IT energy, workload definition, completion count, and the one-hour window fixed; it says nothing about how efficiently the IT equipment did the work.

## The tradeoff

Choice: Optimize an overhead metric alone.

Benefit: It highlights facility energy outside IT and helps track that category.

Cost: It cannot show computing productivity and can move opposite to total energy per useful result.

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

## Sources

- [DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) — www.energy.gov · Published 2024-07 · Reviewed 2026-09-06. Facility efficiency metrics require defined IT and facility boundaries.
- [MLCommons — MLPerf Inference: Datacenter](https://mlcommons.org/benchmarks/inference-datacenter/) — mlcommons.org · Reviewed 2026-09-06. Benchmark energy/performance comparisons declare workload scenarios and measurement boundaries.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — ASHRAE · Reviewed 2026-09-06. Commissioning and documented performance validation have a defined scope and evidentiary role.
- [The Green Grid — PUE: A Comprehensive Examination of the Metric](https://datacenters.lbl.gov/sites/default/files/WP49-PUE%20A%20Comprehensive%20Examination%20of%20the%20Metric_v6.pdf) — The Green Grid · Published 2012-10-02 · Reviewed 2026-09-11. PUE compares facility energy with IT equipment energy and cannot by itself establish useful-work efficiency.
- [The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters) — SemiAnalysis · Published 2026-07-29 · Reviewed 2026-09-26. Describes the commissioning ladder L1 to L5: factory witness test, delivery and installation verification, pre-functional start-up, functional performance testing and integrated systems testing under simulated failures.

## Check your understanding: What does the meter establish?

Pause and make a prediction, then compare your reasoning.

A hypothetical campus records 12 MWh at the facility meter and 10 MWh at its IT meters during the same hour. An analyst adds them and reports 22 MW of useful compute.

**Pause and predict:** Correct the total and explain what these readings leave unknown.

<details>
<summary>Compare your reasoning</summary>

The facility averaged 12 MW, including the IT load. These readings do not measure useful compute output.

The IT boundary sits inside the facility boundary, so adding the two readings counts the IT energy twice. Over this hour, the facility used 2 MWh beyond the IT load and its energy ratio was 12 / 10 = 1.2. Neither that ratio nor the electrical demand tells us how much accepted work the campus completed.

</details>

**The next problem:** We can now account for the watts. What job must those watts support, and what counts as a successful result?

Continue in **3. Workloads and requirements**: Interactivity and total throughput.
