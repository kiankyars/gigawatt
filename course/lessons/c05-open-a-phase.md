# Open one phase, with evidence

**16. Putting an AI Factory Together · Optional practice**

Reconcile installation, energization, integrated testing and service acceptance. Build a dependency schedule without treating announcements as operational measurements.

**Driving question:** Which racks can be counted as accepted service, and what must happen before the next phase opens?

## A campus total can hide incomplete paths

A campus has 1,000 rack locations, 800 installed racks and an energized 100 MW site service. Each rack counts as a 100 kW rack equivalent, so the 800 installed racks come to 80 MW and leave 20 MW of the service for cooling and other auxiliaries, which this exercise assumes is enough. The 1,000 locations measure floor space: filled at 100 kW they would take the whole 100 MW and leave nothing for auxiliaries. On a day when auxiliaries need 25 MW, as in the hot-day case of the weather exercise, the same service carries 750 racks, so the site's power budget belongs in the ledger beside the test results.

The handover register splits the installed racks into three groups. Group A's 300 racks have passed the complete electrical, cooling, network, controls and end-to-end service acceptance package. Group B's 250 racks have passed their electrical tests and the integrated cooling test, but their network interface work and end-to-end acceptance are still open. Group C's 250 racks have passed their electrical tests and completed their network interface work, but their integrated cooling test remains open.

Create separate columns for installed equipment, energized paths, individual tests, integrated tests and service acceptance, then count the subsystem columns. Electrical tests have passed on all 800 racks, the integrated cooling test on 550 (groups A and B) and network interface work on 550 (groups A and C). Taking the smallest column gives 550, but the two 550-rack columns overlap only in group A, so just 300 racks appear in all three. Acceptance counts that intersection: the racks whose every path for the service has passed. The project can report 800 installed racks, and its accepted computing capacity is 300 racks, or 30 MW.

## Distinguish a schedule calculation from a public-site inference

Group B’s remaining network interface work can begin immediately and takes four days. End-to-end acceptance testing then takes two days. Group C needs a replacement cooling component delivered in three days, one day of installation, and three days of integrated cooling testing, with each task depending on the preceding one. Assume the supplied durations hold, groups can proceed independently, and qualified teams and all other resources are available. These assumptions make a small dependency schedule calculable. Actual projects require resource, uncertainty and change-control analysis beyond this exercise.

Apply the same ledger to a named campus using only its dated public record. At Abilene, Crusoe reported the first two buildings energized within a year of the June 2024 construction start, and Oracle reported 75 percent of total capacity delivered as of September 2026. Each statement belongs in its own column: an energization report and a customer-delivery share are milestones, not entries in an acceptance register, and neither says which racks passed integrated testing. Leave Abilene's unreported commissioning state, demand and topology blank. The 300, 250 and 250-rack groups and the six- and seven-day schedules belong to this exercise alone.

## Worked example: Count the intersection and trace the dependencies

- Synthetic groups A/B/C contain 300/250/250 installed racks, each represented by 100 kW. The 100 MW service leaves 20 MW for auxiliaries at the 80 MW of installed racks, which is assumed enough.
- Only A has passed the complete service acceptance package. B has passed electrical and integrated cooling tests; C has passed electrical tests and finished network interface work.
- B: four days of network interface work then two days of end-to-end acceptance testing. C: three days delivery, one day installation, then three days integrated cooling testing.

1. Intersect the subsystem columns: electrical {A, B, C}, integrated cooling {A, B} and network {A, C} share only A. The smallest column holds 550 racks; the intersection holds 300.
2. Accepted service today: 300 × 100 kW = 30 MW of rack-equivalent demand. Installed inventory is separately 800 racks or 80 MW at the stated load.
3. B's acceptance path takes 4 + 2 = 6 days. On successful completion, accepted service becomes 550 racks or 55 MW.
4. C's acceptance path takes 3 + 1 + 3 = 7 days. On successful completion, accepted service becomes 800 racks or 80 MW.
5. The earliest all-group acceptance is day seven under the supplied independent-resource assumptions. The longest single activity is not the same as the longest dependency chain.
6. Every projected increase remains conditional on test success and the stated supply/resource assumptions. A failed test changes the schedule rather than being averaged into an accepted count.

**Result:** The evidence supports 300 accepted racks now, a conditional 550 by day six and a conditional 800 by day seven. Installed, energized and future figures remain separate.

**Model boundary:** Synthetic schedule and acceptance register. No named project's operating state, redundancy certification, installed graphics processing unit (GPU) count or measured demand is inferred.

## The tradeoff

Choice: Open accepted group A while completing groups B and C.

Benefit: 300 racks, 30 MW of rack-equivalent demand, serve from day 0 instead of waiting until day 7 for all 800.

Cost: The network interface work on B and the cooling-component replacement on C happen beside a live group, so isolation, access and change control must keep group A within its accepted conditions.

## When the situation changes

Trigger: An executive summary reports 80 MW live because 800 racks are installed and the site service is energized.

Mechanism: The summary collapses equipment inventory and complete service acceptance into one capacity label.

Response: Replace the single number with the evidence ledger, identify open tests and report conditional future milestones separately.

## Apply the idea

Group C's integrated test fails on day seven. Correction requires two days followed by a three-day retest. B succeeds on day six. Assuming correction starts immediately after the failure, what can be reported on day eight and when could all 800 racks first be accepted?

<details>
<summary>Reveal the worked answer</summary>

On day eight, 550 racks are accepted under the scenario. C can first be accepted on day twelve: day seven plus two correction days plus three retest days.

Failed acceptance does not add usable service, although the hardware remains installed. Group B's successful path is unaffected by assumption; any shared dependency would require revising that independence claim. The day-twelve date remains conditional on successful correction, retest and resource availability.

</details>

**The idea to keep:** Count complete accepted paths for a specified service; maintain a separate ledger for future capacity and unresolved public claims.

## Sources

- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — ASHRAE · Reviewed 2026-09-06. ASHRAE's AI data-center framework guidance on commissioning: testing and handover as steps after installation.
- [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/) — Oracle · Reviewed 2026-09-17. Oracle reports 75 percent of total Abilene capacity delivered as of September 2026, with the rest in later quarters.
- [Crusoe — Flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) — Crusoe · Published 2025-09-30 · Reviewed 2026-09-17. The first two Abilene buildings were energized within a year of the June 2024 construction start.
