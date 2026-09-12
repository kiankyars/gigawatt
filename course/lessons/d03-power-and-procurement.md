# A contract is not a cable

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d03-power-and-procurement`, then run `uv run gigawatt-expand`.

**Siting, grid connection and supply · Authored draft**

Separate the shared grid, commercial arrangements, and time-matched supply, then calculate the storage a matching claim leaves out.

**Driving question:** How do energy purchases relate to the physical supply that keeps a rack running?

## Draw two relationships without confusing their arrows

A data center connects electrically through an arrangement of conductors, substations, switches, protection, and upstream grid infrastructure. Those connections determine possible physical power paths. A commercial agreement describes purchases, prices, delivery obligations, or environmental attributes. It may be associated with generation somewhere on that grid, but the agreement is not an extra feeder into the building. Draw it with a different line style so it cannot be mistaken for a redundant electrical route.

EPA distinguishes a physical power purchase agreement, involving delivery or title to electricity under its arrangement, from a financial PPA that does not deliver electricity to the buyer. That distinction matters, but neither label alone establishes a dedicated generator-to-campus wire or uninterrupted supply. The actual location, contractual structure, utility arrangements, and physical connection still matter. This course uses the distinction to interpret claims, not to give procurement advice for a particular jurisdiction.

Environmental attributes require their own account. An attribute associated with a quantity of generation addresses the characteristic being claimed for that generation. It does not increase a cable's current limit or make a generator produce during an interval when it is unavailable. Keep the physical service, commercial energy, and attribute ledgers connected by explicit references, while preserving the different questions each can answer. That is more informative than coloring one grid wire green.

## Equal daily totals can hide a half-day gap

Consider a hypothetical facility drawing 10 MW for 24 hours. Its energy demand is 240 MWh. A separately described generation profile produces 20 MW for twelve hours and zero for twelve hours, also totaling 240 MWh. The matching annual or daily totals are equal. The profiles are not. During the generating interval, production exceeds this load by 10 MW. During the zero-production interval, the load exceeds production by 10 MW.

The time-matching surplus and deficit are each 10 MW × 12 h = 120 MWh. These are differences between two stated profiles, not a claim about the site's metered import and export. If the generator is elsewhere under a PPA, the campus may still physically import from the shared grid throughout the day. A physical meter reading depends on the actual electrical arrangement, not simply on subtracting contractual generation from campus demand.

Suppose we now construct a separate idealized system in which a battery can capture the entire surplus and later support the full 10 MW deficit. With perfect efficiency, it needs 120 MWh of usable output energy and at least 10 MW of output power. These are separate requirements. It also needs a compatible charge path, charge capability, controls, and an actual connection to the protected load. A 120 MWh store with a 2 MW output limit cannot supply the missing 10 MW service.

Real losses change the matching arithmetic. Assume a hypothetical 90 percent round-trip efficiency: 120 MWh put into storage returns only 108 MWh. That leaves 12 MWh of the later demand uncovered. Supplying the full 120 MWh from this storage would require 120/0.90 = 133.3 MWh of charging energy, more than the original 120 MWh surplus. Equal production and demand totals therefore cannot close this particular time-shifting balance once losses are included.

## Choose which uncertainty you are solving

A long-term energy agreement can address a commercial objective while leaving the site's connection schedule unresolved. Additional physical service can expand usable power while leaving energy cost or sourcing objectives unresolved. Storage can shift energy in time while leaving a protection or transfer problem unresolved. Each is valuable when matched to the requirement it can actually satisfy. The mistake is allowing one solution's label to stand in for the entire system.

Consider an outage during the nonproducing interval. If the hypothetical storage is connected only through an unavailable common bus, its energy inventory does not create an alternative path to the racks. If it is designed to support the relevant loads, the available duration still depends on its state of charge and discharge conditions at that moment. A system that has already used its energy for another purpose may have less reserve for an outage. Reserve policy is therefore a real tradeoff, not a free capacity multiplier.

For an on-site supply comparison, add fuel and operating constraints where relevant. A machine's output rating does not establish how long fuel can be supplied, whether it can operate independently of the grid, or what supporting equipment stays available. A photovoltaic installation is not automatically an island-capable microgrid simply because it sits on the same property. DOE's islanding description treats sources and loads as a coordinated system, with the required behavior at disconnection and reconnection.

When evaluating a supply claim, produce three small drawings or ledgers: the physical path, the commercial/attribute relationships, and the time-resolved energy balance. Then name what each leaves unresolved. This makes the claim actionable. Instead of arguing vaguely about whether a campus has enough power, you can ask whether the missing piece is a connection, deliverable capacity, a particular interval's energy, or the controls and reserve required to survive a disruption.

## Worked example: Matching 240 MWh does not provide every hour

- Facility load is a constant 10 MW for 24 h.
- Generation is 20 MW for 12 h and zero for 12 h.
- The storage exercise is a separately specified hypothetical physical arrangement.

1. Load energy — 10 × 24 = 240 MWh — This is the demand profile area.
2. Generation energy — 20 × 12 = 240 MWh — Equal area does not imply equal height at every time.
3. Night deficit — 10 × 12 = 120 MWh — This energy must come from another source or stored energy.
4. Storage losses — 120 × 0.90 = 108 MWh returned — The original surplus falls 12 MWh short after the assumed round-trip loss.

**Result:** Perfect time shifting needs 120 MWh usable output and 10 MW output capability; 90 percent round-trip efficiency requires extra charging energy.

**Model boundary:** Profile differences are not necessarily actual campus meter imports/exports under an off-site contract.

## The tradeoff

Choice: Use stored energy for normal time shifting as well as outage reserve.

Benefit: The same equipment may support more than one economic or operating objective.

Cost: Energy committed to one use can reduce the reserve available for another unless the policy explicitly preserves it.

## When the situation changes

Trigger: Assume a commercial energy purchase creates a surviving power path.

Mechanism: An agreement does not bypass an unavailable conductor, bus, or conversion interface.

Response: Inspect the physical topology and the state-dependent energy/power budget.

## Apply the idea

If the usable storage output is 80 MWh and its output rating is 12 MW, how long can it cover the 10 MW deficit?

<details>
<summary>Reveal the worked answer</summary>

Eight hours, leaving four hours of the twelve-hour deficit unsupported.

Twelve MW exceeds the required 10 MW, but 80/10 = 8 hours. More inverter power does not create additional stored energy.

</details>

**The idea to keep:** Purchased energy and continuous physical service answer different questions; trace and quantify each separately.

## Sources and reading boundaries

- [US EPA — Physical PPA](https://www.epa.gov/green-power-markets/physical-ppa) — Physical and financial PPAs differ in whether electricity is physically delivered or title is conveyed under the arrangement. Read 2026-09-06. Read the public EPA distinctions; contractual eligibility and local legal requirements are outside this lesson.
- [DOE — Islanding a Microgrid](https://www.energy.gov/cmei/femp/articles/islanding-microgrid) — Islanding requires coordinated operation of sources and loads within an electrical boundary. Read 2026-09-06. Read the public DOE explanation; no particular on-site plant or local interconnection permission is established.
