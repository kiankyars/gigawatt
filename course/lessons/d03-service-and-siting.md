# The first usable megawatt has dependencies

**D03 · Authored draft · Objectives:** D03.3, D03.4

Evaluate a phased site schedule and an islanded supply budget without confusing available land, connection approval, or generation nameplates with usable service.

**Driving question:** Which site can deliver the required service, and what happens when supply is constrained?

## A connection is a process, not a single number

A large-load project begins with an intended service requirement and a proposed physical location. The utility or system operator needs enough information to assess how that load connects and behaves. Studies, agreements, network upgrades, equipment delivery, construction, and operational authorization can all stand between the initial request and available service. Their exact names and sequence differ by jurisdiction and project. A generic course diagram must not be mistaken for the current application procedure of a particular utility.

ERCOT's June 2026 announcement of a batch-study approach provides a dated example of why this matters: multiple large projects must be assessed together against the network they would share. The lesson is not to memorize that announcement's process as universal. It is to recognize that requested capacity can interact with other projects and required grid work. A customer's desired date is an input to planning, not evidence that the grid can deliver the requested load on that date.

Inside the property, additional dependencies continue. Electrical equipment can be energized while cooling, control integration, network connections, or IT acceptance remains incomplete. Commissioning checks behavior for the stated scope; operation then supplies evidence of actual service. A phased campus may therefore have several statuses at once. Keep a ledger for each usable block rather than attaching one completion percentage to the entire site.

## Find the last required dependency, then the usable limit

Compare two hypothetical sites for a service that requires power, a finished building, cooling, and fiber. At Site A, the supplied readiness dates are months 18, 22, 21, and 20 respectively. At Site B, they are months 20, 19, 20, and 21. Under the explicit assumption that these dates represent accepted readiness and all other requirements are satisfied, Site A cannot supply the complete service before month 22; Site B cannot before month 21.

The calculation is a maximum, not an average. Averaging Site A's four dates gives 20.25, but there is no useful 20.25-month service if its required building is unavailable until month 22. The maximum identifies the last necessary dependency. These are supplied scenario dates rather than a forecast of an actual project. If the dates are only expected installation dates, additional acceptance and commissioning work must remain on the schedule.

Capacity uses a different operation. Suppose Site B eventually has 12 MW of facility service, but the supported island mode is defined around an 8 MW protected load, including all declared auxiliaries. An available on-site generator supplies 6 MW in that mode. Storage must supply the remaining 2 MW. If it has 4 MWh usable output and a 3 MW output rating, the power screen passes but energy lasts only 4/2 = 2 hours. The utility service rating does not extend that islanded duration.

Add the supplied fuel constraint: the generator can operate for four hours at its assumed 6 MW output before fuel replenishment is required. The battery deficit reaches its limit sooner, after two hours. If the protected load were reduced to 6 MW, the battery deficit would disappear in this steady simplified interval, but generator fuel would still limit duration. This comparison assumes the generator is already stable; starting and transfer behavior require a separate timeline.

## Treat siting requirements as coupled constraints

Land, fiber, climate, water, electrical service, equipment access, and local requirements influence one another. A site with earlier grid availability may need a cooling solution that changes auxiliary power and delivery time. A location with low energy prices may impose a workload latency disadvantage or a difficult expansion path. A single weighted score can be useful for preferences, but it should not average away a hard requirement that the site fails.

Separate requirements into conditions that must pass and tradeoffs among feasible options. If an application needs a maximum network round-trip time, a location outside that envelope may be unsuitable regardless of its lower cost. If a cooling design depends on a water allocation that has not been established, that is unresolved evidence rather than zero cost. List the missing fact and the party or document that could establish it.

On-site supply can provide a different option set, but it adds its own fuel, maintenance, control, emissions, connection, and operating questions. A behind-the-meter generator does not automatically grant permission or technical ability to isolate from the grid. A generation nameplate does not establish its usable output under every ambient condition or with required reserve. The conceptual comparison asks what each option must demonstrate, without supplying field procedures or jurisdiction-specific legal conclusions.

The final choice should state a complete service envelope: how much load, beginning when, under which normal and degraded conditions, and with which remaining uncertainties. This converts a location comparison into an infrastructure decision. It also identifies where further work has the greatest value: the dependency controlling the delivery date, the capacity limiting accepted load, or the operating condition that breaks the proposed service promise.

## Worked example: Schedule and island capacity are different constraints

- All readiness dates are supplied accepted-readiness assumptions.
- The 8 MW island load includes its stated cooling and control auxiliaries.
- The generator is already operating at 6 MW; startup is excluded.

1. Site A ready — max(18, 22, 21, 20) = month 22 — The service waits for its last necessary subsystem.
2. Site B ready — max(20, 19, 20, 21) = month 21 — Earlier grid readiness alone does not choose the earlier complete site.
3. Island deficit — 8 MW load − 6 MW generation = 2 MW — Storage must cover the difference at the same electrical boundary.
4. Storage duration — 4 MWh / 2 MW = 2 h — The 3 MW storage output rating exceeds the 2 MW deficit; usable energy binds first.

**Result:** Site B is earlier under the supplied schedule; its stated island support lasts two hours before the storage deficit is exhausted.

**Model boundary:** These are planning scenarios, not project forecasts, field operating procedures, or proof of local operating authorization.

## The tradeoff

Choice: Add on-site supply to reduce dependence on a particular utility-service condition.

Benefit: It can support a specifically designed alternative supply mode.

Cost: Fuel, controls, maintenance, environmental requirements, and usable capacity introduce additional dependencies.

## When the situation changes

Trigger: Treat the earliest energized subsystem as a completed site.

Mechanism: A later building, cooling, fiber, or acceptance dependency prevents the intended service.

Response: Track complete blocks and keep readiness, commissioning, and observed operation as separate evidence states.

## Apply the idea

The 8 MW island load can temporarily shed 1 MW. With the same 6 MW generator and 4 MWh storage, how long does the energy balance last?

<details>
<summary>Reveal the worked answer</summary>

Four hours, with both battery energy and the stated generator fuel duration reaching their limits.

The remaining 7 MW load needs 1 MW from storage, so 4/1 = 4 h. This steady result still excludes starting, transfers, and the consequences of shedding that workload.

</details>

**The idea to keep:** Usable service requires every necessary path and permission in the stated operating condition; the last dependency and the smallest capacity both matter.

## Sources and reading boundaries

- [ERCOT — Batch Zero large-load connection announcement, June 18, 2026](https://www.ercot.com/news/release/06182026-puct-approves-ercots) — Large-load connection studies consider shared network capacity and required upgrades. Read 2026-09-06. Read the dated June 18, 2026 ERCOT announcement; do not treat its process or thresholds as universal or permanent.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Commissioning and handover can occur in smaller infrastructure blocks with documented acceptance. Read 2026-09-06. Read the public framework discussion; all dates and capacity ledgers here are synthetic.
- [DOE — Islanding a Microgrid](https://www.energy.gov/cmei/femp/articles/islanding-microgrid) — Grid-connected and islanded operation require a coordinated system of sources and loads. Read 2026-09-06. Read the public DOE explanation; no specific generation or fuel system was assessed.
