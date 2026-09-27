# GPU rental terms, occupancy and financing

**15. GPU cloud economics**

Compare revenue over the whole fleet, then account for costs and risk.

**Driving question:** When is a long contract preferable to selling capacity at short-term prices?

## One, three or five years

SemiAnalysis tracks rental terms from on-demand through five years. The contract duration determines when a provider must sell the capacity again. A longer agreement can reduce exposure to weak future demand and declining rental prices; it can also lock the provider out of higher prices during a shortage. The customer accepts a payment commitment to secure capacity and negotiate terms. No universal rule forces every longer quote to be cheaper.

The public table for NVIDIA’s H100 GPU illustrates why renewal is a risk rather than a guaranteed price decline. One-year rental ranges were $1.45–1.95 in October 2025, $1.50–2.05 in January 2026 and $2.10–2.70 per GPU-hour in April 2026. These are dated 25th–75th percentile observations, with typical 25 percent prepayment. The public table lists the three- and five-year tenors without numeric quotes.

## The price applies only to the hours that pay

In the worked example, a full-fleet commitment receives $2.50 for every contracted GPU-hour. An uncommitted pool receives $4.00 only for rented hours. At half occupancy the pool’s revenue is only $2.00 per available GPU-hour. This is commercial occupancy: a renter may pay for a GPU that is temporarily idle, so rented hours are not the same as processor utilization.

The break-even rented fraction is 2.50/4.00 = 62.5 percent before differences in cost. At 80 percent the pool earns more; at 50 percent it earns less. This does not forecast future occupancy. It identifies what must be believed about bookings before a high hourly price becomes a better revenue strategy.

## Contracts, costs and the timing of cash

CoreWeave reports using asset-level debt supported by take-or-pay customer contracts. A committed receipt stream helps finance expensive hardware, but delivery, customer credit and operating costs still matter. A signed contract is not cash already collected. Payments to suppliers and lenders can fall due while a facility is being commissioned.

A complete GPU-hour cost includes hardware and network investment, facilities, operations and electricity. Avoid counting both equipment purchases and depreciation as separate cash costs, or mixing loan repayments into an inconsistent operating-cost comparison. Financial statements, cash-flow analysis and a simple operating margin answer different questions.

For the energy example, allocate average whole-site power to each GPU, including cooling and shared equipment: 1 kW while it is rented and 0.2 kW while it is unrented but still powered. Over 100 calendar hours at 80 percent billable occupancy, the 80 rented hours use 80 kWh and the 20 idle hours use 4 kWh. Spreading all 84 kWh over the 80 billed hours gives 1.05 kWh per rented GPU-hour: $0.084 at $80/MWh and $0.168 at $160/MWh. As an extension, if unrented GPUs drew the full 1 kW, the 100 hours would use 100 kWh and each billed hour would carry 100 ÷ 80 = 1.25 kWh: $0.10 at $80/MWh and $0.20 at $160/MWh. In the base case, doubling the tariff adds $0.084 per billed GPU-hour. Under an all-in fixed fee, that unhedged increase reduces provider margin; under an energy reimbursement clause, the specified increase reaches the customer. That is what energy pass-through means.

Core Scientific, which supplies colocation capacity to CoreWeave, gives a real example. Its filing for the second quarter of 2026 states that power is passed through to CoreWeave without markup, so electricity raises its revenue and its cost by the same amount and leaves gross profit unchanged. That is a colocation contract with its own billing unit; CoreWeave’s terms with its own GPU-cloud customers are a separate question.

## Case: NVIDIA backstops unsold cloud capacity

On September 9, 2025, CoreWeave signed a capacity order with NVIDIA worth an initial $6.3 billion. Under it, NVIDIA must buy the covered capacity that CoreWeave leaves unsold to other customers through April 13, 2032, subject to delivery, availability and termination terms. It is a purchase obligation for cloud capacity, separate from any guarantee of CoreWeave’s loans.

NVIDIA’s 2026 program is a separate, broader model for clouds that serve many customers. Its Form 10-Q for the quarter ended July 26, 2026 describes commitments that typically last six years and reports $36 billion of AI-cloud commitments at that date. SemiAnalysis’s July 6, 2026 analysis explains the financing logic: lenders can underwrite a cluster against the contracted fallback revenue while the operator rents to customers on shorter terms. NVIDIA’s commitment shrinks as customers use the capacity.

The backstop moves risk between the parties. The operator gains a revenue floor that can support debt, and SemiAnalysis describes it sharing some revenue above that floor with NVIDIA; a floor alone does not ensure an attractive return on equity. NVIDIA’s filing warns that weaker demand could leave it buying capacity it cannot use or resell. The $36 billion is a commitment rather than a loss or cash spent, and it excludes NVIDIA’s separately disclosed hardware-supply and property-lease obligations.

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

Cost: The provider cannot reprice during the term. The one-year H100 range rose from $1.45–1.95 per GPU-hour in October 2025 to $2.10–2.70 in April 2026; a provider that signed at the October range kept that rate while the market rose. Customer-credit and delivery exposure continue for the whole term.

## When the situation changes

Trigger: A model applies a high advertised price to every installed GPU-hour.

Mechanism: It assumes every hour is sold. At $4.00 and 50 percent occupancy, the pool earns $2.00 per available GPU-hour, not $4.00.

Response: Apply billable occupancy and distinguish revenue from profit.

## Apply the idea

If a pool bills $4/GPU-hour but rents 50% of its hours, what full-fleet committed rate produces the same revenue?

<details>
<summary>Reveal the worked answer</summary>

$2 per GPU-hour, before cost differences.

Only half the available hours earn the $4 rate. The comparison needs the same fleet and time interval.

</details>

**The idea to keep:** Compare revenue over the whole fleet, then account for costs and risk.

## Sources

- [SemiAnalysis GPU rental pricing index](https://gpu-index.semianalysis.com/) — SemiAnalysis · Reviewed 2026-09-17. One-, three- and five-year tenors and dated H100 one-year ranges.
- [CoreWeave 2025 annual report](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) — CoreWeave · Reviewed 2026-09-17. Capacity contracts, revenue mix and asset-level financing.
- [Nvidia GPU Debt Backstop Unleashes the AI Project Trinity: Capital, Offtake and Datacenters](https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes) — SemiAnalysis · Published 2026-07-06 · Reviewed 2026-09-06. Explains how an NVIDIA capacity backstop lets lenders finance a cluster against contracted fallback revenue while the operator rents on shorter terms.
- [CoreWeave — Form 8-K, NVIDIA capacity order, September 2025](https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm) — CoreWeave · Published 2025-09-15 · Reviewed 2026-09-26. A September 9, 2025 order with an initial value of $6.3 billion obliges NVIDIA to buy residual unsold capacity through April 13, 2032, subject to delivery, availability and termination terms.
- [NVIDIA — Form 10-Q for the quarter ended July 26, 2026](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm) — NVIDIA · Published 2026-08-26 · Reviewed 2026-09-26. AI-cloud capacity commitments, typically six years long, totaled $36 billion at July 26, 2026 and shrink as others use the capacity; weaker demand could leave NVIDIA unable to use or resell it.
- [Core Scientific — Form 10-Q for the quarter ended June 30, 2026](https://www.sec.gov/Archives/edgar/data/1839341/000183934126000014/core-20260630.htm) — Core Scientific · Published 2026-07-28 · Reviewed 2026-09-26. Colocation power costs are passed through to CoreWeave without markup, so power prices move revenue and cost equally.
- [NVIDIA — NVIDIA Unlocks AI Compute at Scale, Inviting Partners to Power the AI Infrastructure Buildout](https://blogs.nvidia.com/blog/nvidia-unlocks-ai-compute-at-scale-capital-partners-to-power-ai-infrastructure-buildout/) — NVIDIA (Colette Kress and Raj Mirpuri) · Published 2026-07-01 · Reviewed 2026-09-26. NVIDIA’s July 2026 program with AI clouds serving many customers uses a revenue-sharing and credit-support model: the clouds sell NVIDIA-powered cloud services, and NVIDIA earns product revenue and a share of cloud revenue on the supported capacity.
- [Nvidia’s Backstop Universe – Heads I Win, Tails Who Loses?](https://newsletter.semianalysis.com/p/nvidias-backstop-universe-heads-i) — SemiAnalysis · Published 2026-09-11 · Reviewed 2026-09-26. Under the AI Cloud Partner program NVIDIA floors the cloud’s revenue at a level set to repay lenders and takes a share of revenue above that floor; the $36 billion of AI-cloud agreements first appeared in NVIDIA’s August 26, 2026 quarterly report.
