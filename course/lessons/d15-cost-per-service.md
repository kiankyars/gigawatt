# Compare the service you receive, not the invoice label

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d15-cost-per-service`, then run `uv run gigawatt-expand`.

**D15 · Authored draft · Objectives:** D15.2, D15.3

Build a scoped three-year present-value comparison and show how a stable cost changes meaning when useful output falls.

**Driving question:** How should ownership, energy, timing and useful output enter a defensible cost comparison?

## Choose one decision boundary

A facility owner, tenant and cloud customer pay for different bundles. An electricity bill may be separate in one arrangement and embedded in another service fee. Hardware, staffing, replacement, financing and residual value may lie with different parties. Before comparing prices, define the service, horizon and costs included on both sides. Otherwise, an apparent saving may simply be an omitted obligation or a transfer of responsibility whose price appears elsewhere.

Our synthetic comparison covers the same facilities service for three years and deliberately excludes identical customer compute hardware on both sides. Ownership requires $20 million initially, $3 million of annual non-energy operating cost and $4 million of annual energy cost. It has a stipulated $5 million residual value at the end of year three. A contracted alternative costs $11 million per year and includes that same facilities service and energy. These are invented amounts, not market benchmarks.

The $4 million energy line can be checked separately: 50,000 MWh per year at an assumed $80/MWh equals $4 million. A real tariff can include demand, time variation and other charges; the exercise explicitly uses only a flat energy price. Writing out the quantity and unit price makes the assumption visible and prevents an unexplained annual expense from surviving every later scenario unchanged.

## Put cash flows on the same clock

A payment today and a payment in three years have different present values under a chosen discounting convention. Use PV = future amount/(1 + r)^t. Here r is a stipulated 8 percent annual rate, with recurring payments at year end and no inflation or tax modeling. NIST Handbook 135 explains life-cycle costing, cash-flow timing and discounting. We use the method with original assumptions; the exercise rate is neither a federal requirement nor a recommendation for a real project.

The sum of the three year-end discount factors is approximately 2.5771. Ownership therefore costs 20 + 7 × 2.5771 − 5/(1.08³) = $34.07 million in present value. The contracted alternative costs 11 × 2.5771 = $28.35 million. The residual is subtracted because it is an assumed value recovered at the end, not another expenditure. Omitting it or treating it as cash available at time zero changes the comparison incorrectly.

Financing must match the perspective. This example is an unlevered service-cost comparison with a stipulated discount rate; it does not also insert loan principal and interest payments. A separate financing analysis can model actual funding terms, but adding every financing cash flow to an already inconsistent ownership model can double count or mix perspectives. Likewise, nominal cash flows need a compatible nominal rate, while constant-dollar assumptions need a compatible real treatment. State the convention instead of hiding it in a spreadsheet default.

## The denominator can reverse the story

Cost per installed megawatt describes a capital-intensity boundary. Cost per accelerator-hour describes an equipment-time boundary. Cost per useful result includes what the workload actually produces under a quality and service requirement. None can substitute for another without an explicit conversion model. A powered accelerator that waits for data still contributes to some time denominators while producing little additional useful work.

Suppose a fixed scoped cost buys a stipulated ten million acceptable results over the horizon. If useful output falls by twenty percent while cost remains unchanged, eight million results now share the same cost. Cost per result increases by twenty-five percent because 1/0.8 = 1.25. The equipment count and installed MW did not change. This calculation does not explain the lost output; memory, network, storage, recovery or demand conditions must be investigated through evidence.

A decision should report the assumptions that could change its ranking. Ownership may become preferable with a longer service horizon, a different residual value, different energy exposure or a materially different risk allocation. A service contract may contain minimum commitments, escalation or exit conditions absent from this simple comparison. Those belong in a real evaluation. The lesson’s purpose is to make the arithmetic auditable and the missing terms visible, not to declare one commercial model universally superior.

## Worked example: A three-year facilities-service comparison

- All amounts synthetic, in millions of dollars; the same facilities scope and service requirement apply.
- Ownership: 20 at time zero, 7 at each year end, residual receipt 5 at the end of year three.
- Contract: 11 at each year end, energy included. Rate 8 percent; no taxes, inflation, financing cash flows or performance differences.

1. Recurring present-value factor — 1/1.08 + 1/1.08² + 1/1.08³ = 2.5771 — Every recurring payment uses the same timing convention.
2. Ownership present cost — 20 + 7 × 2.5771 − 5/1.08³ ≈ $34.07 million — Subtract the discounted residual at its actual end date.
3. Contract present cost — 11 × 2.5771 ≈ $28.35 million — The included energy must not be added again.

**Result:** The contracted alternative has about $5.72 million lower present cost for this invented three-year scope and service.

**Model boundary:** This is an educational scenario, not a quote, valuation or investment recommendation. Real risk, terms and resource costs require project-specific evidence.

## The tradeoff

Choice: Own an asset rather than purchase a defined service.

Benefit: Ownership can provide control over use, changes and residual value within the actual legal and operating arrangement.

Cost: It carries capital, maintenance, obsolescence and utilization exposure that a comparison must allocate explicitly.

## When the situation changes

Trigger: A comparison adds electricity to the contract fee even though it is already included, while omitting maintenance from ownership.

Mechanism: Different cost boundaries manufacture a ranking that no consistent service comparison supports.

Response: Reconcile inclusions, timing and obligations before interpreting the numerical result.

## Apply the idea

The contract’s total scoped cost remains fixed, but acceptable output falls from ten million results to eight million. By what percentage does cost per result rise?

<details>
<summary>Reveal the worked answer</summary>

It rises by 25 percent: 10/8 − 1 = 0.25.

Each remaining result bears a larger share of the unchanged cost. A twenty-percent output reduction is not a twenty-percent unit-cost increase because the new denominator is smaller. Before comparing this ratio across workloads, confirm that a result meets the same quality, latency and scope requirement in both cases.

</details>

**The idea to keep:** Keep scope, cash-flow timing and the useful-service denominator consistent. Lower capital cost alone does not establish lower cost per result.

## Sources and reading boundaries

- [NIST Handbook 135, 2025: Life Cycle Costing Manual](https://nvlpubs.nist.gov/nistpubs/hb/2025/NIST.HB.135e2025.pdf) — Chapters 2–4 distinguish study periods, cost categories, cash-flow timing and present-value methods; section 3.2 covers single and recurring payments. Read 2026-09-06. Selected scope, timing and discounting passages inspected. Prices, rate, residual and service assumptions are original; no federal compliance or current-market claim is made.
