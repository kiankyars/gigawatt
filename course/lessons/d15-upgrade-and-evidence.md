# Choose the intervention, then audit the claim

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d15-upgrade-and-evidence`, then run `uv run gigawatt-expand`.

**D15 · Authored draft · Objectives:** D15.4, D15.5

Compare original intervention scenarios with different delivery dates, then audit a dated Stargate announcement without converting planned capacity into measured operation.

**Driving question:** Which improvement delivers useful results within the horizon, and which public statements actually support the project model?

## An intervention needs a causal route to useful output

An upgrade should name the limiting condition it changes and the service that benefits. A network intervention can reduce waiting without increasing available electrical MW. A cooling intervention can permit a higher physical load while leaving storage or commissioning as a separate constraint. Before assigning an economic benefit, confirm that the revised configuration, workload and accepted paths support the additional useful output. Removing a local bottleneck does not by itself establish the end-to-end gain.

Our synthetic brief stipulates that two alternatives have already passed those feasibility checks for the same workload and output-quality requirement. The network option costs $4 million and immediately adds eighty acceptable results per operating hour. The cooling option costs $6 million, arrives one year later and then adds one hundred fifty results per operating hour. There are eight thousand usable hours per year and a three-year evaluation horizon. These are supplied scenario outcomes, not watts-to-tokens conversions.

The timing is consequential. The immediate network option produces 80 × 8,000 × 3 = 1.92 million additional results. The delayed cooling option produces 150 × 8,000 × 2 = 2.40 million. Dividing initial cost by these increments gives about $2.08 and $2.50 per additional result respectively. This is a narrow capital-per-increment screening ratio: energy, discounting, recurring cost, risk and residual value are excluded explicitly, so it is not a complete investment decision.

## Sensitivity should find the assumption that reverses the answer

If the cooling option becomes available immediately, its increment rises to 3.60 million results and its screening ratio falls to about $1.67. The ranking reverses without changing its equipment performance or initial cost. Delivery time was the decisive assumption. The GAO schedule guide makes the broader connection between schedule and cost assessment; this original example also connects schedule with the time available to deliver useful service.

Actual use is another condition. An added capacity envelope does not guarantee customers, jobs or data that can occupy it productively. If only half of the stipulated incremental results are demanded, dividing by the full capacity output understates realized unit cost. Similarly, an intervention that shifts quality or latency cannot be compared using an unchanged result label without checking the service contract. Scenario comparisons should change one assumption at a time before exploring combinations.

The decision record should state the current choice, supporting evidence and condition for reconsideration. Physical necessity may survive every scenario while the preferred delivery option changes with demand. Explain which uncertain inputs govern the decision rather than presenting a large spreadsheet without an argument.

## A named project requires a different evidence ledger

Now leave the synthetic brief entirely. OpenAI’s article dated September 23, 2025, with a later October update on the page, describes a broader Stargate plan and says early workloads had begun at the Abilene campus. The same article describes nearly 7 GW as planned capacity across multiple projects. Those are different claims with different subjects and statuses. The presence of an operational statement about one campus cannot convert the entire announced program into operating capacity.

A useful ledger records the entity, quantity, unit, status, boundary, source date and exact claim supported. For this article, one row can record the publisher’s statement about early Abilene workloads. Another can record the planned program total. A third can record a potential expansion as potential, not additive operating inventory. The page alone does not establish current metered demand, full commissioned MW, detailed topology, economics or the configuration of every building. Those cells stay unresolved.

Treat this as a dated document audit, not an assertion about September 2026 operating conditions. A present-day claim would require refreshed evidence. Likewise, several partners repeating one joint announcement do not necessarily provide independent confirmation. Trace original records where available, preserve changes and contradictions, and distinguish a publisher statement from independently observed measurements. The course becomes a useful reference when its reasoning remains inspectable even where the public evidence stops.

## Worked example: Delivery timing changes the screening ranking

- Entirely synthetic alternatives serving the same acceptable-result definition.
- Network: $4m, available immediately, +80 results/hour. Cooling: $6m, available after one year, +150 results/hour.
- Three-year horizon; 8,000 usable hours/year; every incremental result is demanded. This screening excludes recurring costs, discounting and residuals.

1. Network increment — 80 × 8,000 × 3 = 1,920,000 results — Immediate delivery uses the full modeled horizon.
2. Delayed cooling increment — 150 × 8,000 × 2 = 2,400,000 results — The first year contributes no incremental cooling-enabled output.
3. Capital per incremental result — $4m/1.92m ≈ $2.08; $6m/2.40m = $2.50 — The ratio compares only the stated initial expenditure with the stated incremental output.
4. Immediate cooling alternative — $6m/(150 × 8,000 × 3) ≈ $1.67/result — Changing delivery alone reverses this limited screening ranking.

**Result:** The immediate network option wins the base screening ratio; immediate cooling would win the revised one. A full decision needs the excluded costs and risks.

**Model boundary:** None of these prices or output rates describes Stargate or any named product. The document audit is separate from the numerical scenario.

## The tradeoff

Choice: Choose earlier service with a smaller steady output increment.

Benefit: It may deliver more value within a short or time-sensitive opportunity than a later, larger technical improvement.

Cost: Longer horizons, recurring costs, uncertainty or a changed service requirement can reverse the preference.

## When the situation changes

Trigger: A planned program total is inserted as operating capacity in the upgrade model.

Mechanism: Different sites, dates and status categories are collapsed into a quantity the evidence does not establish.

Response: Rebuild the ledger by entity and state; leave unverified commissioning, demand and throughput values blank rather than substituting generic assumptions.

## Apply the idea

A dated announcement states that early jobs are running at one campus and separately lists a multi-site planned MW total. What operating MW value can you assign to the entire program from those statements alone?

<details>
<summary>Reveal the worked answer</summary>

No quantitative operating-MW total for the entire program is established by those statements alone.

The first statement supports a publisher-reported instance of operation at a named campus and date. The second supports a plan across a different population. Neither specifies the measured or commissioned aggregate now in service. Record both claims with their boundaries, identify the missing site-level evidence and avoid adding overlapping phases or treating planned capacity as observed demand.

</details>

**The idea to keep:** A decision connects constraints, useful output, time and evidence. Keep synthetic calculations separate from what a named source actually establishes.

## Sources and reading boundaries

- [GAO Schedule Assessment Guide](https://www.gao.gov/products/gao-16-89g) — The guide overview connects schedule credibility and slippage with program cost assessment. Read 2026-09-06. Overview reviewed. The intervention prices, rates, horizon and screening ratios are original and are not project forecasts.
- [OpenAI: Five new Stargate sites](https://openai.com/index/five-new-stargate-sites/) — The article distinguishes a multi-site planned capacity total from its statement about early workloads at Abilene. Read 2026-09-06. Main article and visible October 22, 2025 update inspected on September 6, 2026. This lesson audits the dated statements; it does not establish current operating MW, complete topology or site economics.

## D15 domain check-in: Which upgrade changes the ceiling?

Optional: pause and make a prediction, then compare your reasoning. You can continue whenever you are ready.

For the same hypothetical rack population and operating condition, electrical capacity supports 12 racks, cooling 8, networking 10 and accepted service 9. Option A raises electrical capacity to 16; option B raises cooling capacity to 11. Assume the other limits stay fixed.

**Pause and predict:** What ceiling follows from each option, and is that enough to choose an investment?

<details>
<summary>Compare your reasoning</summary>

Option A leaves the ceiling at 8 racks. Option B raises it to 9, where accepted service becomes the limit. This alone does not settle the investment decision.

Take the minimum across limits with matching boundaries: min(16, 8, 10, 9) = 8 and min(12, 11, 10, 9) = 9. Then compare delivery dates, costs and useful output from the added service. A capacity ceiling is neither measured demand nor a guaranteed business result.

</details>

**The next problem:** Take the whole chain into an integrated case: can you defend a decision while keeping its assumptions, evidence and unresolved constraints visible?

Continue in **the integrated cases**: The servers stay powered. The service does not..
