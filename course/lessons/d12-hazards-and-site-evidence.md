# The site boundary does not stop the hazard

Generated reading view. Edit [`course/expansion/heat-delivery-operations.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/heat-delivery-operations.json), lesson `d12-hazards-and-site-evidence`, then run `uv run gigawatt-expand`.

**D12 · Authored draft · Objectives:** D12.2

Connect hazards to exposed assets and service dependencies, then use explicit hypothetical probabilities without turning them into a site forecast.

**Driving question:** What evidence distinguishes an attractive parcel from a deliverable and resilient location?

## A hazard becomes a service problem through an exposed path

A hazard describes a potentially damaging condition. Exposure identifies the equipment, people and infrastructure that can encounter it. Vulnerability concerns how that exposed system responds. Consequence asks what happens to the intended service. These are different questions. A flood near the parcel may spare the data hall while disabling the access road, utility substation or fuel delivery route. Conversely, evidence of a regional hazard does not prove that a particular protected installation will fail.

National Weather Service material identifies several flood mechanisms, including intense rainfall and river overflow. USGS explains that seismic hazard assessment considers faults, wave propagation and local near-surface conditions. Those references establish why a single generic city label is insufficient. They do not provide the parcel’s elevations, drainage capacity, soil response, equipment anchorage or operating plan. An actual site assessment must identify which local documents and specialists resolve those missing details.

Draw the facility’s dependencies outside the fence. Trace electrical supply, water, telecommunications, road access and shared emergency resources. Two routes that appear independent on a building drawing may share the same bridge, trench or regional constraint. The question is not simply how many providers have contracts; it is which physical failure or operating restriction can affect them together. Keep uncertainty visible when that topology is unavailable.

## A risk register should lead to a decision

A useful site register connects each question to an owner, evidence, consequence and decision. For example: could stormwater isolate the service yard; which civil survey and drainage model address it; who reviews the result; and what layout or project decision changes if the result is unfavorable? A generic list of weather words can look comprehensive without answering any of these questions. The register earns its place when a missing fact has a clear route to resolution.

Permitting is another dependency graph. Air emissions, noise, water abstraction, discharge, construction, land use and fire arrangements can involve different authorities and conditions. Their relevance depends on the jurisdiction and proposed equipment. A generator purchase order does not itself demonstrate permission to operate it in the contemplated way. Equally, a permit for one phase cannot silently be treated as authorization for a larger future layout.

Compare alternatives at the same stage of knowledge. One parcel with documented problems may be more understandable than another with an empty folder. Absence of reported issues is not evidence that the same investigations were performed. Record whether an item is observed, modeled, required, unresolved or excluded by the actual scope. Do not convert those states into equally certain numbers simply to complete a scoring spreadsheet.

## Probability arithmetic helps only when the assumptions survive

Imagine a synthetic hazard with a 2 percent annual occurrence probability. Conditional on that hazard, the modeled facility has a 25 percent probability of a service interruption lasting ten hours. Under this deliberately simple one-event model, expected interruption time is 0.02 × 0.25 × 10 = 0.05 hours per year. That is a long-run mathematical expectation under the supplied assumptions, not a forecast that this facility will lose three minutes every year.

An expected value can conceal the shape of the consequence. A rare ten-hour event and frequent brief interruptions can have the same average while producing different workload recovery, contractual and safety consequences. The independence assumptions also matter. If a hazard simultaneously damages power, communications and roads, multiplying their individual availabilities as though unrelated understates the shared cause. A proposed intervention should identify which conditional probability or consequence it changes.

A site decision therefore combines quantitative scenarios with unresolved evidence and feasibility conditions. Recalculate when the design changes or a more informative local study appears. Keep the base date and model scope attached to the result. A score that survives only because old assumptions were never revisited is a poor reference for procurement, commissioning or operation.

## Worked example: A conditional risk calculation, not a site prediction

- Entirely synthetic: annual hazard probability 0.02.
- Conditional service-interruption probability 0.25 and conditional downtime 10 hours.
- This simplified model excludes multiple events, changing climate and other causes of interruption.

1. Annual interruption probability from this modeled cause — 0.02 × 0.25 = 0.005 — The hazard must occur and produce the specified service consequence.
2. Expected downtime — 0.005 × 10 h = 0.05 h/year — The average is 3 minutes/year across hypothetical repetitions, not a scheduled annual outage.
3. Improved conditional resilience — 0.02 × 0.10 × 10 h = 0.02 h/year — A stated change to conditional vulnerability reduces this modeled contribution, without proving total site risk.

**Result:** The intervention reduces the modeled contribution by 0.03 expected hours/year, subject to every stated assumption.

**Model boundary:** The probabilities are not assigned to any real location, and no site selection or insurance result follows.

## The tradeoff

Choice: Add a second access or supply route.

Benefit: It may reduce consequences from a failure specific to one route.

Cost: Its value depends on physical separation, shared hazards, permissions, upkeep and availability when needed.

## When the situation changes

Trigger: Both nominally separate service routes cross the same vulnerable off-site interface.

Mechanism: One external event defeats the assumed independence.

Response: Update the dependency model and obtain route-specific evidence before crediting the redundancy.

## Apply the idea

A second synthetic design reduces interruption probability after the hazard to 0.10, but repair takes 30 hours because access is harder. Is its expected downtime lower than the original 0.05 h/year?

<details>
<summary>Reveal the worked answer</summary>

No. Expected downtime is 0.02 × 0.10 × 30 = 0.06 h/year.

The design experiences fewer modeled interruptions but each lasts longer. The average worsens slightly, and its consequence distribution also changes. A preference still requires service requirements and other considerations; neither the lower event probability nor this one expected-value metric settles the entire decision.

</details>

**The idea to keep:** A site comparison needs local evidence and consequence paths. A hazard score or map color cannot establish facility performance.

## Sources and reading boundaries

- [National Weather Service: Flood Related Hazards](https://www.weather.gov/safety/flood-hazards) — Flood mechanisms differ and can affect low-lying and urban infrastructure through rainfall and overflow. Read 2026-09-06. Public hazard descriptions inspected; no local elevation, flood probability or engineering requirement is inferred.
- [USGS: What is seismic hazard?](https://www.usgs.gov/faqs/what-seismic-hazard-what-a-seismic-hazard-map-and-how-are-they-used) — Seismic hazard maps incorporate fault, propagation and near-surface site information. Read 2026-09-06. FAQ reviewed; it is not a parcel assessment or a code-specific structural design input.
