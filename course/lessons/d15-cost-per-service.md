# GPU rental terms, occupancy and financing

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d15-cost-per-service`, then run `uv run gigawatt-expand`.

**15. GPU cloud economics · Authored draft**

Compare revenue over the whole fleet, then account for costs and risk.

**Driving question:** When is a long contract preferable to selling capacity at short-term prices?

## One, three or five years

SemiAnalysis tracks rental terms from on-demand through five years. The contract duration determines when a provider must sell the capacity again. A longer agreement can reduce exposure to weak future demand and declining rental prices; it can also lock the provider out of higher prices during a shortage. The customer accepts a payment commitment to secure capacity and negotiate terms. No universal rule forces every longer quote to be cheaper.

The public H100 table illustrates why renewal is a risk rather than a guaranteed price decline. One-year rental ranges were $1.45–1.95 in October 2025, $1.50–2.05 in January 2026 and $2.10–2.70 per GPU-hour in April 2026. These are dated 25th–75th percentile observations, with typical 25 percent prepayment, not September spot quotes. Missing public three- and five-year numeric quotes are not filled with invented estimates.

## The price applies only to the hours that pay

In the worked example, a full-fleet commitment receives $2.50 for every contracted GPU-hour. An uncommitted pool receives $4.00 only for rented hours. At half occupancy the pool’s revenue is only $2.00 per available GPU-hour. This is commercial occupancy: a renter may pay for a GPU that is temporarily idle, so rented hours are not the same as processor utilization.

The break-even rented fraction is 2.50/4.00 = 62.5 percent before differences in cost. At 80 percent the pool earns more; at 50 percent it earns less. This does not forecast future occupancy. It identifies what must be believed about bookings before a high hourly price becomes a better revenue strategy.

## Contracts and costs sit on both sides of the balance sheet

CoreWeave reports using asset-level debt supported by take-or-pay customer contracts. A committed receipt stream helps finance expensive hardware, but delivery, customer credit and operating costs still matter. A signed contract is not cash already collected. Payments to suppliers and lenders can fall due while a facility is being commissioned.

A complete GPU-hour cost includes hardware and network investment, facilities, operations and electricity. Avoid counting both equipment purchases and depreciation as separate cash costs, or mixing loan repayments into an inconsistent operating-cost comparison. Financial statements, cash-flow analysis and a simple operating margin answer different questions.

For the energy example, allocate 1 kW of average whole-site demand to each installed GPU over all hours, including cooling and shared equipment. At $80/MWh and 80 percent billable occupancy, energy costs $0.10 per rented GPU-hour. Doubling the tariff makes that $0.20 at the same average load. Under an all-in fixed fee, an unhedged increase reduces provider margin; under an energy reimbursement clause, the specified increase reaches the customer. That is what energy pass-through means.

## Worked example: A higher rate with fewer rented hours

- 1,024 GPUs over 8,760 hours. Same service scope; rates are original example inputs.
- Committed: $2.50/GPU-hour for the full fleet. Pool: $4.00/rented GPU-hour at 50% occupancy.

1. Available hours — 1,024 × 8,760 = 8,970,240 GPU-hours — Count the entire fleet over the same interval.
2. Committed revenue — 8,970,240 × $2.50 = $22,425,600 — The commitment pays independently of actual use.
3. Pool revenue — 8,970,240 × 0.50 × $4.00 = $17,940,480 — Unrented hours earn no rental revenue.
4. Equal revenue — Occupancy = $2.50/$4.00 = 62.5% — Costs and risk can still change the preferred strategy.

**Result:** The higher-priced pool earns less at 50% occupancy, and more at 80%.

**Model boundary:** Annual revenue before costs; delivery and collectability are assumed. These are not CoreWeave price quotes.

## The tradeoff

Choice: Commit the fleet for a longer term.

Benefit: More visible receipts and fewer renewal gaps.

Cost: Reduced repricing flexibility and continuing customer-credit and delivery exposure.

## When the situation changes

Trigger: A model applies a high advertised price to every installed GPU-hour.

Mechanism: It assumes every hour is sold.

Response: Apply billable occupancy and distinguish revenue from profit.

## Apply the idea

If a pool bills $4/GPU-hour but rents 50% of its hours, what full-fleet committed rate produces the same revenue?

<details>
<summary>Reveal the worked answer</summary>

$2 per GPU-hour, before cost differences.

Only half the available hours earn the $4 rate. The comparison needs the same fleet and time interval.

</details>

**The idea to keep:** Compare revenue over the whole fleet, then account for costs and risk.

## Sources and reading boundaries

- [SemiAnalysis GPU rental pricing index](https://gpu-index.semianalysis.com/) — One-, three- and five-year tenors and dated H100 one-year ranges. Read 2026-09-17. Only visible public observations used. October 2025, January and April 2026 ranges are historical, not September quotes; missing tenors left blank.
- [CoreWeave 2025 annual report](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) — Capacity contracts, revenue mix and asset-level financing. Read 2026-09-17. Fiscal 2025 observations; these are not claims about every provider or every private contract.
