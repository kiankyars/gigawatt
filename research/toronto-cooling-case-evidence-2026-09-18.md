# Toronto district cooling case — source and teaching record

Reviewed September 18, 2026. Chapter 12 gains three scenes immediately after `water-restriction`: `toronto-lake-cooling`, `toronto-cooling-outage`, `toronto-operator-response`. The existing sixteen scenes and aliases remain.

## Evidence

- **Physical system:** [Enwave / Toronto Water](https://www.enwave.com/case-studies/enwave-and-toronto-water-tap-into-innovative-energy-source) describes cold lake intake, drinking-water treatment, and heat exchangers at John Street. The potable flow absorbs heat from a separate recirculating district cooling circuit before continuing into the city supply. This source describes the architecture; its present-day scale and resilience claims are not assigned to the 2013 system.
- **Flood context:** [Hydro One’s July 8, 2013 release](https://www.newswire.ca/news-releases/hydro-one-power-outages-due-to-heavy-rains-512697891.html) documents severe flooding at Richview and Manby transmission stations and regional outages. It does not establish a particular electrical feeder from either station to Enwave or 151 Front. The slides do not draw one.
- **Building power and cooling:** [Data Center Knowledge, July 9, 2013](https://www.datacenterknowledge.com/outages/toronto-flooding-kos-data-center-cooling-systems) reproduces PEER 1’s statement that the building transferred to generators while its external chill-loop provider’s power problems affected cooling. It identifies Enwave deep lake cooling and reports an emergency chiller. PEER 1’s original forum link is no longer relied on as independently available. This is a contemporary secondary report carrying an attributed operator statement.
- **Tenant response:** [Uberflip CTO Erik Levinson’s July 9, 2013 NANOG message](https://seclists.org/nanog/2013/Jul/130) is the firsthand basis for the hotter/cooler suite comparison, automatic equipment shutdowns, remote shutdown of redundant/nonessential systems, service transfers and the reported temperature above 43°C. That temperature describes cold-side cabinet air in the hotter suite, not coolant, silicon or a building-wide reading. The event interval in this account is approximately 18:45–01:15; no universal tenant outage duration is inferred.

## Slide treatment

1. The archival 151 Front Street photograph establishes a specific building. A native vector drawing separately traces Toronto Water’s one-way potable supply and Enwave’s returning district circuit, with heat crossing the exchanger. The mobile layout retains the two distinct water paths with larger labels.
2. A single building receives two different services. Electricity remains available through building generators; district cooling is impaired. The display does not locate a specific failed pump or imply that the lake ran out of water.
3. A conceptual pair of suites communicates the operator response. Rack silhouettes are visual placeholders, not a count or floor plan. The warmer-suite air temperature is explicitly labeled. No claim is made that all services or tenants remained online.

Native diagrams were chosen because separated physical paths and failure boundaries must stay legible, editable and accurate across themes and screen sizes. The real building photograph supplies visual context; no generated picture is presented as incident evidence.

## Asset

`course/assets/references/toronto-151-front-allied.jpg` is the unchanged 470 × 351 photograph credited to Allied REIT in the contemporary article. It is deliberately a small context figure. Its adjacent provenance JSON records the source URL, date, dimensions and hash.

## Speaker notes handoff

The full explanations are stored with the three scene records in `heat-rejection-scenes.js`. Emphasize the separation between potable water and district water; then distinguish on-site backup electricity from an externally supplied cooling service. Finish with the tenant’s actual response, keeping the reported air temperature specific to its hotter suite. The case is evidence that electrical backup alone did not protect every heat-removal dependency, not an argument that district cooling always lacks redundancy.

## Verification

- `node --test tests/heat-rejection.test.mjs`: 13 tests passed, including all 19 scenes, phone/desktop render variants, source-bookmark aliases and existing controls.
- Playwright exercised all three new scenes at 1440 × 900 and 390 × 844 in light and dark mode: no horizontal overflow, unloaded images, footer overlap or JavaScript errors. Every scene was visually inspected at desktop and phone sizes; the mobile power line was extended to physically meet the building and its label moved clear of the line.
- Additional 1280 × 720 render check: all three scenes fit before the shared footer. Final scene retains the shared next-chapter button.
- `git diff --check` passed. QA used an isolated source server on port 8878, leaving the main staged website untouched.
