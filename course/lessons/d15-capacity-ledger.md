# Find the constraint after reconciling the boundaries

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d15-capacity-ledger`, then run `uv run gigawatt-expand`.

**D15 · Authored draft · Objectives:** D15.1

Reconcile facility overhead, non-compute IT, electrical and thermal limits, network scope and accepted service in one synthetic ledger.

**Driving question:** How many rack equivalents can the specified system support, and what would an upgrade actually change?

## A megawatt must belong to a ledger

A utility service limit, downstream electrical rating, cooling duty and installed rack count describe different boundaries. To compare them, define the population and the required state. Our exercise uses identical compute-rack equivalents at 100 kW each, plus a separate 5 MW of non-compute IT. That non-compute IT includes the synthetic shared network and storage electrical load. It belongs inside total IT power, even though it is not assigned to the compute-rack count.

The stipulated facility model is Psite = 1.2 PIT + 5 MW. The load-dependent overhead is 0.2 PIT, and the fixed 5 MW overhead is outside IT. These two different 5 MW terms must not be confused: one is non-compute IT inside PIT; the other is fixed facility overhead outside it. The formula is an invented operating model, not an annual PUE or an observed data-center efficiency. It is useful because each load has an explicit place.

At a 100 MW site limit, total IT power cannot exceed (100 − 5)/1.2 = 79.17 MW. Removing the separate 5 MW non-compute IT leaves about 74.17 MW for compute racks, or 741 whole 100 kW equivalents after rounding down. Other constraints can be lower. A downstream 70 MW IT electrical limit allows only 65 MW for compute, while a stipulated 60 MW thermal limit on total IT heat allows 55 MW.

## Only compare like populations

The synthetic network brief supports six hundred compute-rack equivalents for the specified workload topology. There are seven hundred fifty usable physical positions, and only five hundred twenty positions currently have accepted end-to-end service paths. We explicitly assume these populations are nested and refer to the same positions, with all required reserve and maintenance deductions already included in the stated limits. Without that assumption, the asset-level intersection from the commissioning lesson is necessary.

The reconciled ceilings are therefore 741 from site input, 650 from downstream electrical capacity, 550 from heat removal, 600 from networking, 750 from space and 520 from accepted service. Their minimum is 520. This is an operating envelope under supplied conditions. It is not a measured load, a customer reservation total or a model of useful application output. A workload can demand less power or make poor progress inside the envelope.

Notice that the available electrical service is not the binding constraint. At 520 compute racks, compute power is 52 MW and total IT is 57 MW after adding non-compute IT. The facility model then uses 1.2 × 57 + 5 = 73.4 MW. The unused site capacity cannot be converted directly into more accepted racks. It is headroom at one boundary, while another required condition remains incomplete.

## Removing one bottleneck reveals the next

Complete additional acceptance so that seven hundred positions are available, while leaving physical capacities unchanged. The new minimum is 550, imposed by the thermal boundary. Increase cooling capability from 60 to 70 MW of total IT heat and the thermal compute ceiling becomes 650. Networking now limits the population to 600. The cooling intervention therefore creates fifty additional equivalents after acceptance is expanded, not the full one hundred implied by its ten-megawatt thermal increase.

If network capability later rises to eight hundred equivalents, downstream electrical capacity and cooling both bind at 650. Tied constraints matter: upgrading only one of them does not increase this ceiling while the other remains unchanged. A useful intervention plan records the sequence, prerequisites and cost of the next limiting condition, rather than celebrating every added megawatt as the same increment of service.

Finally, keep capacity and useful output separate. A network upgrade can improve job progress without changing the count of powered racks, and a workload change can reduce required power for the same useful output. An efficiency improvement can also free site capacity that remains unusable because commissioning or another physical interface is limiting. The ledger explains feasibility. To decide whether a change is worthwhile, connect that feasibility to a measured workload and a dated cost model.

## Worked example: One consistent 100 MW scenario

- Synthetic 100 MW site limit with Psite = 1.2 PIT + 5 MW.
- Non-compute IT is a separate 5 MW within PIT; each compute equivalent is 0.1 MW.
- Downstream electrical limit 70 MW IT; cooling limit 60 MW IT heat. Network 600, space 750 and accepted service 520 equivalents. Populations are nested and reserves are already deducted.

1. Site compute ceiling — ((100 − 5)/1.2 − 5)/0.1 = 741.67 → 741 whole equivalents — Subtract fixed facility overhead before conversion, then remove non-compute IT.
2. Downstream and thermal ceilings — (70 − 5)/0.1 = 650; (60 − 5)/0.1 = 550 — Both stated ratings cover total IT, so both include the non-compute IT load.
3. Common feasible population — min(741, 650, 550, 600, 750, 520) = 520 — Every constraint now refers to the same rack-equivalent definition.

**Result:** The current envelope is 520 equivalents. Completing acceptance alone raises it to 550; further gains depend on the next constraints.

**Model boundary:** The overhead relation, thermal accounting and workload equivalence are hypothetical. This is not a site estimate or throughput forecast.

## The tradeoff

Choice: Prioritize an intervention that closes the currently binding service condition.

Benefit: It can produce useful incremental capacity with less stranded upstream headroom.

Cost: The next bottleneck may appear quickly; delivery, workload demand and joint constraints determine how much of the intervention becomes useful.

## When the situation changes

Trigger: A proposal counts all new cooling MW as additional compute MW.

Mechanism: It ignores non-compute IT, the network envelope or the remaining accepted-service boundary.

Response: Reconcile the before-and-after ledger and identify every condition required for the claimed gain.

## Apply the idea

After accepted service reaches 700, cooling reaches 70 MW IT and networking reaches 800 equivalents, what is the ceiling? Would raising only downstream electrical capacity above 70 MW help?

<details>
<summary>Reveal the worked answer</summary>

The ceiling is 650 equivalents, tied between downstream electrical capacity and cooling. Raising only the electrical limit does not change it.

Both boundaries allow 70 − 5 = 65 MW of compute, or 650 equivalents. The unchanged thermal limit remains binding after an electrical-only upgrade. The site, space, network and acceptance ceilings are higher under the stated assumptions, so they do not resolve that tie.

</details>

**The idea to keep:** A capacity minimum is meaningful only after every limit refers to the same population, operating condition and accounting boundary.

## Sources and reading boundaries

- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — The PUE discussion distinguishes facility and IT energy boundaries and describes limitations of comparing operating ratios. Read 2026-09-06. Selected metric-boundary passages inspected. The affine power model and all capacity limits in this lesson are original synthetic inputs, not handbook ratings.
