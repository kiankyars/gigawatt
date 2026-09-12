# Open one phase, with evidence

Generated reading view. Edit [`course/expansion/capstones.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/capstones.json), lesson `c05-open-a-phase`, then run `uv run gigawatt-expand`.

**Integrated practice · Authored draft**

Reconcile installation, energization, integrated testing and service acceptance. Build a dependency schedule without treating announcements as operational measurements.

**Driving question:** Which racks can be counted as accepted service, and what must happen before the next phase opens?

## A campus total can hide incomplete paths

A hypothetical campus has 1,000 rack locations, 800 installed racks and an energized 100 MW site service. None of those totals alone identifies an accepted service path. The supplied handover register splits the installed racks into three groups: A contains 300 racks whose electrical, cooling, network, storage, controls and workload recovery tests have passed; B contains 250 racks with electrical and cooling tests complete but storage acceptance still open; C contains 250 racks whose integrated cooling test remains open. Every group uses a specified 100 kW rack-equivalent load for this exercise.

Create separate columns for installed equipment, energized paths, individual tests, integrated tests and service acceptance. Do not combine the highest count from each subsystem as if those counts referred to the same racks. Even equal totals can describe disjoint groups. Acceptance requires the intersection of compatible paths for the particular service. The hypothetical evidence explicitly establishes that intersection only for group A. The project can report its larger installed inventory, but it should not rename that inventory as accepted computing capacity.

## Distinguish a schedule calculation from a public-site inference

Group B's remaining storage interface work can begin immediately and takes four days. Recovery testing then takes two days. Group C needs a replacement cooling component delivered in three days, one day of installation, and three days of integrated testing, with each task depending on the preceding one. Assume the supplied durations hold, groups can proceed independently, and qualified teams and all other resources are available. These assumptions make a small dependency schedule calculable. Actual projects require resource, uncertainty and change-control analysis beyond this exercise.

For a named campus, perform a different task: open its dated public records and classify the statements they actually support. A reported building opening, utility agreement or equipment order is not evidence of the internal acceptance register used here. If a relevant public source does not report commissioning state, demand, topology or workload output, leave those entries unknown. The worked exercise teaches how to reason when inputs are supplied; it does not authorize filling missing real-site evidence with the synthetic numbers. An auditable reference distinguishes these two modes every time it uses a real project name.

## Worked example: Count the intersection and trace the dependencies

- Synthetic groups A/B/C contain 300/250/250 installed racks, each represented by 100 kW.
- Only A has passed the complete service acceptance package. All other site-wide constraints are adequate for the calculated groups.
- B: four days of interface work then two days of recovery testing. C: three days delivery, one day installation, then three days integrated testing.

1. Accepted service today: 300 × 100 kW = 30 MW of rack-equivalent demand. Installed inventory is separately 800 racks or 80 MW at the stated load.
2. B's acceptance path takes 4 + 2 = 6 days. On successful completion, accepted service becomes 550 racks or 55 MW.
3. C's acceptance path takes 3 + 1 + 3 = 7 days. On successful completion, accepted service becomes 800 racks or 80 MW.
4. The earliest all-group acceptance is day seven under the supplied independent-resource assumptions. The longest single activity is not the same as the longest dependency chain.
5. Every projected increase remains conditional on test success and the stated supply/resource assumptions. A failed test changes the schedule rather than being averaged into an accepted count.

**Result:** The evidence supports 300 accepted racks now, a conditional 550 by day six and a conditional 800 by day seven. Installed, energized and future figures remain separate.

**Model boundary:** Synthetic schedule and acceptance register. No named project's operating state, redundancy certification, installed GPU count or measured demand is inferred.

## The tradeoff

Choice: Open accepted group A while completing the other phases.

Benefit: Begin delivering a bounded service before the entire installed inventory is accepted.

Cost: Shared-system work, isolation, access and change control must preserve the live group's accepted conditions.

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

## Sources and reading boundaries

- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Commissioning context for distinguishing testing and handover from installation; the register and schedule are original teaching inputs. Read 2026-09-06. Public framework guidance. Referenced standards and project-specific acceptance procedures were not reviewed; no field procedure is prescribed.
