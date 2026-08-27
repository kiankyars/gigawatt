# GIGAWATT instructor packet

This packet is teaching territory, not a spoken script. It assigns no
durations, cadence, or automatic visual changes. The presenter decides how
long to remain in each segment and may open the evidence view when the
explanation benefits.

## Run and test

```sh
python3 -m http.server --directory diagram 8000
```

Open `http://localhost:8000/course.html`. Use the segment rail or left/right
arrow keys to move through the course. `Show evidence` (or the E key) opens
the sourced claims, known limits, claim boundaries, and
primary-source links. No state advances on its own.

For a first editorial pass, check whether each opening question naturally
invites the explanation, whether the focused frame remains useful,
whether the evidence boundary is sayable in your own words, and whether the
handoff makes the next segment feel inevitable. Record notes by segment ID.

## Act 1: The missing gigawatt

Establish that announced capacity, energized infrastructure, live workloads, and usable compute are different measures.

### 01. A gigawatt is not a workload `p0_gigawatt_not_workload`

- Opening question: If capacity is announced, how many useful tokens exist?
- Teaching objective: Separate planned, constructed, energized, live, and unknown quantities before following the physical system.
- Visual focus: Gas turbine package, Initial 200 MW / 138 kV station, 1 GW / 345 kV expansion substation, Emergency diesel backup package, Abstract campus MV distribution envelope, GPU die
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **planned grid boundary — planned.**
  - 1200 MW
  - Scope: Original eight-building Abilene campus grid interconnection
  - Boundary: `planned_not_operational` / `planned` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **initial substation rating — confirmed.**
  - 200 MW
  - Scope: Initial Abilene grid path
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **expansion substation rating — confirmed.**
  - 1000 MW
  - Scope: Separate greenfield Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **permitted gas layer — permitted.**
  - 360.5 MW
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **permitted diesel layer — permitted.**
  - 169.9 MW
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-04-24
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645)
- **energized building minimum — confirmed minimum.**
  - 2 buildings
  - Scope: Original eight-building Abilene campus
  - Boundary: `confirmed_minimum` / `energized` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [Crusoe — Crusoe announces new 900 MW AI factory campus in Abilene, Texas, to support Microsoft AI infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure)
- **operational buildings unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Original eight-building Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/)
- **installed gpu no estimate — no evidence backed estimate.**
  - No evidence-backed estimate
  - Scope: Original Abilene campus installed or operational GPU fleet
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts), [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **workloads live by — live by.**
  - 2025-07-22 (ISO-8601 date)
  - Scope: Parts of the original Abilene campus
  - Boundary: `live_by_not_start_date` / `operating` / as of 2025-07-22
  - Sources: [OpenAI — Stargate advances with partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)
- **untyped delivery percentage — reported untyped.**
  - 42 percent
  - Scope: Oracle's Abilene portfolio-page wording
  - Boundary: `reported_untyped` / `delivered_untyped` / as of 2026-08-25
  - Sources: [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/)
- **adjacent project exclusion — excluded scope.**
  - No (boolean)
  - Scope: Adjacent two-building Microsoft AI infrastructure expansion
  - Boundary: `excluded_scope` / `planned` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe announces new 900 MW AI factory campus in Abilene, Texas, to support Microsoft AI infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure)

Red-line warnings:

- **planned to operational.** A planned milestone or capacity is not operational evidence.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **permitted to installed.** A permit does not prove equipment was installed.
- **permitted to commissioned.** A permit does not prove equipment was commissioned.
- **minimum to exact.** A confirmed minimum is not an exact current count.
- **live by to start date.** A live-by disclosure is only an upper date bound, not an exact start date.
- **untyped to capacity.** An untyped delivery percentage does not establish MW, buildings, racks, accelerators, or workload capacity.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.
- **excluded scope addition.** Do not add explicitly excluded assets or capacity to the taught scope.

Handoff: Learn the diagram's claim language before entering the system.

### 02. How to read the machine `p1_read_the_machine`

- Opening question: What does each line style actually let us claim?
- Teaching objective: Read carrier, direction, lifecycle, and evidence posture as separate properties of the master diagram.
- Visual focus: Gas turbine package, Generator, 138 kV slack-span tie, Initial 200 MW / 138 kV station, BESS package, Abstract campus MV distribution envelope, Air-cooled chiller and condenser, Atmosphere
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **energized example — confirmed.**
  - 2026-08-25 (ISO-8601 date)
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **permitted example — permitted.**
  - 10 units
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **future example — future design.**
  - future (status)
  - Scope: BESS shown on the Longhorn power-plant review drawing
  - Boundary: `future_design` / `future_design` / as of 2024-12-04
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **unknown example — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **selected design example — selected design.**
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)

Red-line warnings:

- **permitted to installed.** A permit does not prove equipment was installed.
- **permitted to commissioned.** A permit does not prove equipment was commissioned.
- **future design to operational.** A future design is not installed, commissioned, or operational.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Begin with the first conversion on the behind-the-meter branch.

## Act 2: Origination and interconnection

Distinguish the three physical source branches, their evidence states, and the deliberately abstract campus distribution boundary.

### 03. Fire is not electricity `s01_fire_to_electricity`

- Opening question: What must happen before fuel can become an electrical watt?
- Teaching objective: Distinguish fuel input, shaft power, and generator output.
- Visual focus: Gas turbine package, Generator
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **gas authorization — permitted.**
  - 10 units
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
  - 360.5 MW
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **turbine generator conversion reference — design reference.**
  - A moving fluid, including combustion gas, pushes turbine blades and rotates the generator rotor shaft.
  - Scope: Generic turbine-generator energy conversion; not an Abilene installation or operating claim
  - Boundary: `design_not_observed` / `design_reference` / as of 2023-10-31
  - Sources: [U.S. Energy Information Administration — How electricity is generated](https://www.eia.gov/energyexplained/electricity/how-electricity-is-generated.php)
  - A generator converts the rotor's mechanical energy to electrical energy.
  - Scope: Generic electromagnetic-generator function; not an Abilene generator output or operating claim
  - Boundary: `design_not_observed` / `design_reference` / as of 2023-10-31
  - Sources: [U.S. Energy Information Administration — How electricity is generated](https://www.eia.gov/energyexplained/electricity/how-electricity-is-generated.php)
- **installed turbine presence — confirmed.**
  - A new onsite power plant was delivered at Crusoe's Abilene data center. (site execution milestone)
  - Scope: Original Abilene campus onsite power plant as a delivered facility; excludes any claim about its installed unit count, commissioned MW, current output, or operating mode.
  - Boundary: `confirmed` / `constructed` / as of 2026-08-27
  - Sources: [Crusoe — An energy first approach to AI](https://www.crusoe.ai/energy)
  - Advanced natural-gas turbines from GE Vernova were installed. (installed equipment family)
  - Scope: Original Abilene campus; manufacturer family and installation only, not installed count, exact model mix, commissioning, output, or availability.
  - Boundary: `confirmed` / `constructed` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **installed turbine configuration unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Exact installed natural-gas-turbine count at the original Abilene campus
  - Boundary: `unverified_null` / `installation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
  - Unknown — not established by the cited evidence
  - Scope: Exact installed turbine model mix at the original Abilene campus
  - Boundary: `unverified_null` / `installation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **operating posture unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Commissioned natural-gas-turbine capacity at the original Abilene campus
  - Boundary: `unverified_null` / `commissioning_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An energy first approach to AI](https://www.crusoe.ai/energy), [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
  - Unknown — not established by the cited evidence
  - Scope: Current output of the original Abilene campus gas-turbine plant
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An energy first approach to AI](https://www.crusoe.ai/energy), [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
  - Unknown — not established by the cited evidence
  - Scope: Current running, standby, testing, unavailable, or other operating posture of the original Abilene campus gas-turbine plant
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)

Red-line warnings:

- **permitted to installed.** A permit does not prove equipment was installed.
- **permitted to commissioned.** A permit does not prove equipment was commissioned.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Follow shaft power into the first electrical state.

### 04. Generator-terminal MV is only the beginning `s02_generator_terminal`

- Opening question: Does a model voltage range reveal the site's configuration?
- Teaching objective: Separate manufacturer range, selected site voltage, step-up function, and the unknown campus connection.
- Visual focus: Generator, Generator step-up package, Abstract campus MV distribution envelope
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **generator authorization — permitted.**
  - 10 units
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **model voltage range — product reference.**
  - 11-13.8 (kV AC)
  - Scope: Solar Titan 350 38 MW generator-set model range
  - Boundary: `model_range_not_site_configured` / `product_documented` / as of 2022-05
  - Sources: [Solar Turbines — Titan 350 38 MW Gas Turbine Generator Set](https://www.solarturbines.com/en_US/solutions/case-studies/titan-350-38mw-gas-turbine-generator-set.html)
- **site voltage unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Exact configured generator terminal voltage at the Longhorn onsite plant
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-25
  - Sources: [Solar Turbines — Titan 350 38 MW Gas Turbine Generator Set](https://www.solarturbines.com/en_US/solutions/case-studies/titan-350-38mw-gas-turbine-generator-set.html), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **campus interface design — design reference.**
  - 34.5 kV
  - Scope: Longhorn generation collection / Lancium underground tie and review-design feeds associated with Buildings 1 and 2
  - Boundary: `design_not_as_built` / `review_design` / as of 2024-12-04
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **campus interface unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **gsu function reference — product reference.**
  - A generator step-up transformer raises generator-level voltage to a suitable higher network voltage.
  - Scope: Generic GSU function; no Abilene terminal voltage, target voltage, ratio, winding connection, or operating state
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Hitachi Energy — Generator Step-up Transformers (GSU)](https://www.hitachienergy.com/us/en/products-and-solutions/transformers/power-transformers/generator-step-up-transformers-gsu)
- **generator gsu protection reference — design reference.**
  - Generator protection addresses internal electrical faults, system faults, and abnormal operating conditions.
  - Scope: Generic synchronous-generator protection scope; no Abilene relay scheme, device, zone, setting, or trip logic
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-06-28
  - Sources: [IEEE Standards Association — IEEE C37.102-2023, IEEE Guide for AC Generator Protection](https://standards.ieee.org/ieee/C37.102/7035/)
  - Power-transformer protection requires engineering of relays and other devices, including consideration of current-transformer behavior, fault clearing, and post-trip re-energization.
  - Scope: Generic power-transformer protection scope; no Abilene GSU protection design or settings
  - Boundary: `design_not_observed` / `design_reference` / as of 2021-06-29
  - Sources: [IEEE Standards Association — IEEE C37.91-2021, IEEE Guide for Protecting Power Transformers](https://standards.ieee.org/ieee/C37.91/5904/)
  - GSU protection functions and current-transformer-defined differential zones must be selected for the application; a reference one-line is not a universal protection design.
  - Scope: Generic lesson from an SEL GSU protection example; not a design recommendation or Abilene protection boundary
  - Boundary: `design_not_observed` / `design_reference` / as of 2015-11-17
  - Sources: [Schweitzer Engineering Laboratories — An SEL Approach to Modifying Transformer Protection for Nuclear Stations](https://selinc.com/api/download/blt62cb31c4b2d7632d/?lang=en-us)
- **site generator configuration boundary — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built ratio, winding connection, grounding, and campus-side target voltage of the generator step-up transformers at Longhorn
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
  - Unknown — not established by the cited evidence
  - Scope: Installed generator and GSU protection devices, CT-defined zones, settings, and trip logic at Longhorn
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)

Red-line warnings:

- **permitted to installed.** A permit does not prove equipment was installed.
- **permitted to commissioned.** A permit does not prove equipment was commissioned.
- **model range to site configuration.** A manufacturer range does not reveal the site's selected setting.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Compare the permitted branch with the first evidenced grid-service path.

### 05. The initial grid-service path `s03_initial_grid_path`

- Opening question: What turns a nearby transmission line into usable site service?
- Teaching objective: Trace the named source, site tie, and initial station without inventing the downstream merge.
- Visual focus: AEP Abilene Northwest source, 138 kV slack-span tie, Initial 200 MW / 138 kV station, Abstract campus MV distribution envelope
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **initial service — confirmed.**
  - AEP Abilene Northwest transmission line
  - Scope: Initial 138 kV Abilene grid path only
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 138 kV
  - Scope: Initial Abilene grid path
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 200 MW
  - Scope: Initial Abilene grid path
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 300 ft
  - Scope: Initial tie between the AEP Abilene Northwest line and the 138 kV substation
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 2026-08-25 (ISO-8601 date)
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **downstream merge unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built merge of the initial 138 kV, expansion 345 kV, and behind-the-meter generation paths at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)

Red-line warnings:

- **substation to it load.** Substation or feeder capacity does not establish current facility load or critical IT load.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Treat the expansion as a separate service path rather than an extension of this one.

### 06. The separate expansion grid-service path `s04_expansion_grid_path`

- Opening question: Why is the expansion not merely a larger version of the initial path?
- Teaching objective: Trace the independent high-voltage corridor, abstract protection envelope, and expansion substation while preserving unknowns.
- Visual focus: Unnamed 345 kV source, 345 kV expansion service, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **expansion service — confirmed.**
  - 345 kV
  - Scope: Separate greenfield Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 1000 MW
  - Scope: Separate greenfield Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 5 main power transformers
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 2026-03-10 (ISO-8601 date)
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **upstream source unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Upstream source line for the separate 345 kV expansion substation
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **downstream merge unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built merge of the initial 138 kV, expansion 345 kV, and behind-the-meter generation paths at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)

Red-line warnings:

- **single path conflation.** Do not identify distinct named, planned, conceptual, or energized paths as one completed physical path.
- **substation to it load.** Substation or feeder capacity does not establish current facility load or critical IT load.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Separate physical delivery from contractual attribution.

### 07. A PPA is not a wire `s05_ppa_not_wire`

- Opening question: Does buying nuclear power place a reactor beside the campus?
- Teaching objective: Distinguish contractual energy attribution from the local physical electron path.
- Visual focus: Nuclear PPA overlay, Unnamed 345 kV source
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **crane microsoft named ppa — contract reference.**
  - Constellation and Microsoft signed a 20-year power purchase agreement supporting the restart of Crane Clean Energy Center; Microsoft will buy energy from the renewed plant to help match the power its PJM data centers use with carbon-free energy. (named contract comparison)
  - Scope: Microsoft-Constellation Crane Clean Energy Center comparison case only; not the Abilene campus and not a dedicated physical delivery path.
  - Boundary: `confirmed_contract` / `contracted` / as of 2024-09-20
  - Sources: [Constellation Energy — Constellation to Launch Crane Clean Energy Center, Restoring Jobs and Carbon-Free Power to The Grid](https://www.constellationenergy.com/news/2024/Constellation-to-Launch-Crane-Clean-Energy-Center-Restoring-Jobs-and-Carbon-Free-Power-to-The-Grid.html)
- **contractual attributes are not physical flow — accounting reference.**
  - Energy attribute instruments are separate from physical grid distribution; contractual relationships allocate generation attributes while consumers receive an untraceable grid mix. (accounting boundary)
  - Scope: General Scope 2 accounting boundary for grid-distributed electricity; it does not determine any site's physical source path or contract eligibility.
  - Boundary: `authoritative_guidance` / `accounting_standard` / as of 2026-08-27
  - Sources: [Greenhouse Gas Protocol — Scope 2 Guidance](https://ghgprotocol.org/sites/default/files/2023-03/Scope%202%20Guidance.pdf)

Red-line warnings:

- **contractual to physical.** A contract or commercial role does not establish physical power flow or asset control.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.

Handoff: Return from contractual origin to the physical campus boundary.

### 08. The campus-MV envelope and resilience claims `s06_campus_mv_envelope`

- Opening question: Where do source, storage, and backup paths actually meet?
- Teaching objective: Preserve the unknown source merge while separating future storage and permitted backup from operating infrastructure.
- Visual focus: Generator step-up package, Initial 200 MW / 138 kV station, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope, BESS package, Emergency diesel backup package
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **campus design reference — design reference.**
  - 34.5 kV
  - Scope: Longhorn generation collection / Lancium underground tie and review-design feeds associated with Buildings 1 and 2
  - Boundary: `design_not_as_built` / `review_design` / as of 2024-12-04
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **campus as built unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **source merge unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built merge of the initial 138 kV, expansion 345 kV, and behind-the-meter generation paths at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **gas authorization — permitted.**
  - 10 units
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **bess future — future design.**
  - future (status)
  - Scope: BESS shown on the Longhorn power-plant review drawing
  - Boundary: `future_design` / `future_design` / as of 2024-12-04
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **bess operation unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: BESS at the original Abilene reference campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **bess connection unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built BESS connection at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **diesel authorization — permitted.**
  - 62 units
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-04-24
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645)
  - 169.9 MW
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-04-24
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645)
- **diesel operation unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `unverified_null` / `installation_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645)
  - Unknown — not established by the cited evidence
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645)
- **diesel connection unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built connection of the authorized emergency and standby diesel system at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645)

Red-line warnings:

- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **future design to operational.** A future design is not installed, commissioned, or operational.
- **permitted to installed.** A permit does not prove equipment was installed.
- **permitted to commissioned.** A permit does not prove equipment was commissioned.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Cross the abstract boundary into one reference building.

## Act 3: Electrical descent to the die

Follow a conceptual facility and rack power train without inventing site-specific voltages or redundancy.

### 09. From campus MV to protected building AC `s07_building_power_train`

- Opening question: Which gates stand between a campus feeder and a rack row?
- Teaching objective: Explain transformation, protected distribution, ride-through, and busway as a conceptual reference chain.
- Visual focus: Abstract campus MV distribution envelope, Unit substation transformer, LV switchgear, UPS, Busway
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **campus input unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **facility distribution product reference — product reference.**
  - A unit substation coordinates primary switchgear, a transformer, and secondary distribution equipment as one system.
  - Scope: Schneider Electric unit-substation product architecture; not an Abilene equipment selection, voltage, rating, or topology
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Schneider Electric — Medium Voltage Unit Substations](https://www.se.com/us/en/product-range/60292-medium-voltage-unit-substations/)
  - Low-voltage switchgear distributes power and protects, controls, and isolates downstream equipment and circuits.
  - Scope: Schneider Electric Power-Zone 4 product function; not an Abilene switchgear selection, rating, lineup, or switch state
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Schneider Electric — Power-Zone 4 Low Voltage Drawout Switchgear](https://www.se.com/us/en/product-range/7288-powerzone-4/)
  - Busway provides enclosed feeder and plug-in sections for facility power distribution.
  - Scope: Schneider Electric I-Line product-family function; not an Abilene route, conductor, rating, tap count, or redundancy path
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Schneider Electric — I-Line Busway](https://www.se.com/us/en/product-range/7550-iline-busway/)
- **ups function reference — design reference.**
  - A UPS protects critical loads with conditioned, no-break power.
  - Scope: Generic large-data-center UPS role; not an Abilene UPS topology, capacity, battery runtime, redundancy, or operating state
  - Boundary: `design_not_observed` / `design_reference` / as of 2026-06-26
  - Sources: [Vertiv — BESS and UPS roles in large data center power architectures](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/)
- **first phase electrical delivery — confirmed.**
  - Essential electrical equipment and switchgear were manufactured in-house, and critical infrastructure was produced and deployed on site to support the first-phase construction schedule. (site execution milestone)
  - Scope: First-phase original Abilene campus equipment deployment; no claim about voltage class, product list, quantity, redundancy, topology, or state.
  - Boundary: `confirmed` / `constructed` / as of 2025-12-22
  - Sources: [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards)
- **building power train configuration unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Site voltages, transformer and switchgear ratings, equipment quantities, redundancy paths, UPS topology, busway layout, and switch states between campus MV and the first-phase rack rows
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards)

Red-line warnings:

- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Follow protected facility AC into the rack.

### 10. Rack AC becomes core voltage `s08_rack_voltage_descent`

- Opening question: How many conversions remain once power reaches the data hall?
- Teaching objective: Separate site AC, the documented rack DC bus, and the deliberately unspecified board-level core voltage.
- Visual focus: Busway, Rack power shelves, Voltage regulator module, GPU die
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **operating family — confirmed.**
  - NVIDIA GB200 (platform family)
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **design platform — design reference.**
  - NVIDIA GB200 NVL72 (platform design reference)
  - Scope: Building-level design reference for the original Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **rack dc product reference — product reference.**
  - 50-51 (VDC)
  - Scope: NVIDIA DGX GB200 rack power-shelf nominal DC busbar output
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **rack ac unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Site-specific AC input to DGX GB200 rack power shelves at Abilene
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-25
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **vrm power delivery reference — product reference.**
  - Voltage regulator modules step down an intermediate-bus output to the voltage required by GPUs and other high-power processors.
  - Scope: Generic AI-server point-of-load architecture; not a GB200 board design, Abilene rack configuration, or numerical core voltage
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Infineon Technologies — Server rack power management](https://www.infineon.com/applications/ai-data-center/data-center-power-solutions/server-rack-power-management)
  - Advanced processors require precise low-voltage, high-current power delivery.
  - Scope: Generic XPU and ASIC power-delivery requirement; no processor-specific rail voltage or current
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Infineon Technologies — Server rack power management](https://www.infineon.com/applications/ai-data-center/data-center-power-solutions/server-rack-power-management)
  - Multiphase DC-to-DC controllers and power stages provide scalable high-current processor-core power with fast transient response.
  - Scope: Texas Instruments multiphase processor-core product architecture; not a selected GPU VRM or Abilene rack design
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Texas Instruments — Multiphase solutions: processor core power](https://www.ti.com/product-category/power-management/multiphase.html)
- **first rack delivery — confirmed.**
  - 2025-06 (ISO-8601 month)
  - Scope: First NVIDIA GB200 rack deliveries to the original Abilene campus
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **operating rack configuration unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Exact operating GB200 rack variant, rack count, populated trays, and power configuration at the original Abilene campus
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
  - Unknown — not established by the cited evidence
  - Scope: Exact board-level processor rail or core voltage for operating Abilene GB200 systems
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: At the die, change from the electrical path to the heat-removal obligation.

## Act 4: Return the heat

Follow the liquid and residual-air paths from the die to the atmosphere with explicit supply and return direction.

### 11. The watt becomes heat `s09_watt_becomes_heat`

- Opening question: Where does electrical energy go after useful computation?
- Teaching objective: Establish the die as both electrical destination and thermal source without asserting a quantitative heat split.
- Visual focus: GPU die, Cold plate
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **operating family — confirmed.**
  - NVIDIA GB200 (platform family)
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **live workload boundary — live by.**
  - 2025-07-22 (ISO-8601 date)
  - Scope: Parts of the original Abilene campus
  - Boundary: `live_by_not_start_date` / `operating` / as of 2025-07-22
  - Sources: [OpenAI — Stargate advances with partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)
- **direct cooling design — design reference.**
  - direct-to-chip liquid cooling (system design)
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **liquid path product reference — product reference.**
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **electrical input to cold plate reference — design reference.**
  - Most electrical power consumed by information-technology equipment becomes heat that cooling systems must remove
  - Scope: Generic ITE energy balance at the equipment and facility boundary; not a per-die heat fraction, useful-compute fraction, or named-site load.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf)
  - A cold plate provides a conductive path from an electronic component to coolant flowing through internal channels
  - Scope: Generic direct-liquid cold-plate function; not evidence of a selected or installed cold-plate design at a named site.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-10-09
  - Sources: [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **live by to start date.** A live-by disclosure is only an upper date bound, not an exact start date.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.

Handoff: Split the rack's heat between liquid-cooled compute and air-cooled auxiliaries.

### 12. One rack, two heat paths `s10_two_rack_heat_paths`

- Opening question: Is a liquid-cooled rack entirely liquid cooled?
- Teaching objective: Separate liquid-cooled compute from residual air-cooled components, ending each branch at its evidenced rack-package boundary.
- Visual focus: GPU die, Air-cooled rack auxiliaries, Cold plate, Rack supply and return headers
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **rack design reference — design reference.**
  - NVIDIA GB200 NVL72 (platform design reference)
  - Scope: Building-level design reference for the original Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
  - direct-to-chip liquid cooling (system design)
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **rack component split — product reference.**
  - networking, storage, and other non-CPU/GPU rack components (component set)
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.

Handoff: Trace the liquid branch's separate supply and return headers.

### 13. Supply and return are different pipes `s11_technology_loop`

- Opening question: Why can the cooling circuit not be drawn as one arrow?
- Teaching objective: Distinguish cold technology supply from heat-carrying technology return.
- Visual focus: Cold plate, Rack supply and return headers, Coolant distribution unit
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **direct cooling design — design reference.**
  - direct-to-chip liquid cooling (system design)
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **manifold product reference — product reference.**
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **technology loop engineering reference — design reference.**
  - Coolant supply flows from the CDU through the rack manifold to IT cold plates; after heat pickup, coolant return flows back through the manifold to the CDU (topology reference)
  - Scope: Generic rack-manifold-distributed Technology Cooling System loop; no temperature, flow, coolant, pressure, or site topology is asserted.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-10-09
  - Sources: [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)
  - A rack manifold distributes coolant from the CDU to IT equipment and back while meeting flow and pressure-drop requirements
  - Scope: Generic rack-manifold function and design parameters; not a flow rate, header arrangement, or control setting for a named system.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-10-09
  - Sources: [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)
  - A liquid-to-liquid CDU uses sensors and controls to regulate coolant flow, pressure, and temperature across its TCS and FWS interfaces
  - Scope: Generic liquid-to-liquid CDU control functions; no control mode, setpoint, sensor count, redundancy, or response is asserted for a named package.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.

Handoff: Follow both headers to the boundary between rack and facility systems.

### 14. The CDU is a boundary, not a magic box `s12_cdu_boundary`

- Opening question: Why use two loops instead of facility water at every cold plate?
- Teaching objective: Explain the conceptual interface without asserting coolant mixing or exact package design.
- Visual focus: Rack supply and return headers, Coolant distribution unit, Closed facility water loop
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **selected loop design — selected design.**
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **direct cooling design — design reference.**
  - direct-to-chip liquid cooling (system design)
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **cdu boundary engineering reference — design reference.**
  - A liquid-to-liquid CDU isolates the Technology Cooling System from the Facility Water System and transfers heat between them through a heat exchanger (topology reference)
  - Scope: Generic liquid-to-liquid CDU boundary; it does not assert coolant mixing, a particular exchanger, or a named-site package design.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)
  - A liquid-to-liquid CDU uses sensors and controls to regulate coolant flow, pressure, and temperature across its TCS and FWS interfaces
  - Scope: Generic liquid-to-liquid CDU control functions; no control mode, setpoint, sensor count, redundancy, or response is asserted for a named package.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)
- **cdu site configuration unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Site CDU presence by rack or row, package selection, temperature and flow setpoints, heat-exchanger interface, quantity, and redundancy
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)

Red-line warnings:

- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Recover the rack heat that never entered a cold plate.

### 15. Residual air takes a parallel route `s13_residual_air_branch`

- Opening question: Where does heat from networking, storage, and other auxiliaries go?
- Teaching objective: Use the reference CRAH branch as a parallel cooling path without claiming it is Abilene's as-built residual-air configuration.
- Visual focus: Air-cooled rack auxiliaries, CRAH / fan-wall branch, Closed facility water loop
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **air cooled components — product reference.**
  - networking, storage, and other non-CPU/GPU rack components (component set)
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **selected facility loop — selected design.**
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **parallel air path engineering reference — design reference.**
  - Direct-liquid cooling of IT equipment can coexist with CRAHs that cool the computer-room air (topology reference)
  - Scope: Generic hybrid data-center cooling arrangement; not evidence that a particular air and liquid branch is installed or operated at Abilene.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-01-09
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers)
  - Warm IT exhaust air returns to an air handler, where a heat exchanger transfers heat into a coolant loop and conditioned air is supplied back to the data hall (topology reference)
  - Scope: Generic CRAH or central-air-handler heat-removal path; not a named-site air path, coil selection, airflow, temperature, humidity, or package count.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers), [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf)
  - CRAH airflow can be varied with cooling load and coordinated against common environmental conditions
  - Scope: Generic air-handler control principle; no site setpoint, fan curve, sensor location, or control sequence is asserted.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf)
- **residual air site configuration unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: First-phase residual-air path, CRAH or fan-wall selection, package count, airflow direction, redundancy, and facility-loop connection
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards)

Red-line warnings:

- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Rejoin the liquid and air branches at the facility loop.

### 16. The facility loop carries heat to the plant `s14_facility_heat_rejection`

- Opening question: Which equipment still gates heat after it leaves the data hall?
- Teaching objective: Follow facility return and restored supply through the selected air-cooled heat-rejection design.
- Visual focus: Coolant distribution unit, CRAH / fan-wall branch, Closed facility water loop, Air-cooled chiller and condenser
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **selected heat rejection — selected design.**
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **direct cooling design — design reference.**
  - direct-to-chip liquid cooling (system design)
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **facility loop engineering reference — design reference.**
  - Facility coolant loops receive ITE heat through equipment heat exchangers and carry it to plant heat-rejection equipment (topology reference)
  - Scope: Generic facility-loop role; the heat-rejection equipment may vary and no Abilene CDU, CRAH, chiller interface, or operating topology is asserted.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf), [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers)
  - Facility cooling control may vary pump flow, differential pressure, and supply-water temperature with load while maintaining required cooling capacity
  - Scope: Generic chilled-water and facility-loop control options; not an Abilene control sequence, operating setpoint, equipment selection, or measured state.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf)
  - A liquid-to-liquid CDU isolates the Technology Cooling System from the Facility Water System and transfers heat between them through a heat exchanger (topology reference)
  - Scope: Generic liquid-to-liquid CDU boundary; it does not assert coolant mixing, a particular exchanger, or a named-site package design.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf)
  - Warm IT exhaust air returns to an air handler, where a heat exchanger transfers heat into a coolant loop and conditioned air is supplied back to the data hall (topology reference)
  - Scope: Generic CRAH or central-air-handler heat-removal path; not a named-site air path, coil selection, airflow, temperature, humidity, or package count.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers), [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf)
- **site facility cooling design — selected design.**
  - A true closed-loop Facility Cooling Water System continuously recirculates water and rejects heat through air-cooled chillers. (selected facility-cooling design)
  - Scope: Original eight-building Abilene campus design selection; no CDU, CRAH, temperature, flow, redundancy, quantity, or operating-measurement claim.
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
  - air-cooled chillers (selected heat-rejection equipment family)
  - Scope: Terminal heat-rejection family for the original Abilene FWS; no chiller model, count, capacity, setpoint, or observed operating state.
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **facility cooling interfaces unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built interfaces among rack manifolds, CDUs, residual-air equipment, the FWS, pumps, and air-cooled chillers at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
  - Unknown — not established by the cited evidence
  - Scope: Current measured operating values for first-phase Abilene cooling loops and heat-rejection equipment
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Resolve why a non-evaporative design still has a water requirement.

### 17. Closed loop does not mean water-free `s15_water_accounting`

- Opening question: How can non-evaporative heat rejection still require water?
- Teaching objective: Separate design fill and anticipated maintenance from measured operating consumption.
- Visual focus: Initial fill and water treatment, Closed facility water loop, Air-cooled chiller and condenser
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **initial fill design — selected design.**
  - 1000000 gallons per building
  - Scope: Design requirement for one building's closed-loop cooling-system initial fill
  - Boundary: `design_selected` / `design_requirement` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **anticipated maintenance — anticipated.**
  - 50000 gallons per building per year
  - Scope: Anticipated annual cooling-system maintenance water for each building
  - Boundary: `anticipated_not_observed` / `anticipated_maintenance` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **anticipated to measured.** An anticipated value is not a measured operating result.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.

Handoff: Replay the complete return path to its terminal sink.

### 18. The figure-eight closes in the atmosphere `s16_close_atmosphere`

- Opening question: Where is the watt now?
- Teaching objective: Replay every reference heat-transfer gate to the terminal sink without implying an as-built path or physical recirculation.
- Visual focus: GPU die, Air-cooled rack auxiliaries, Cold plate, Rack supply and return headers, Coolant distribution unit, CRAH / fan-wall branch, Closed facility water loop, Air-cooled chiller and condenser, Initial fill and water treatment, Atmosphere
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **operating family — confirmed.**
  - NVIDIA GB200 (platform family)
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **cooling design — design reference.**
  - direct-to-chip liquid cooling (system design)
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **rack component paths — product reference.**
  - networking, storage, and other non-CPU/GPU rack components (component set)
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **selected heat rejection — selected design.**
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **facility interface boundary — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: As-built interfaces among rack manifolds, CDUs, residual-air equipment, the FWS, pumps, and air-cooled chillers at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
  - Unknown — not established by the cited evidence
  - Scope: Site CDU presence by rack or row, package selection, temperature and flow setpoints, heat-exchanger interface, quantity, and redundancy
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
  - Unknown — not established by the cited evidence
  - Scope: First-phase residual-air path, CRAH or fan-wall selection, package count, airflow direction, redundancy, and facility-loop connection
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Reread the same physical path as a construction schedule.

## Act 5: Chokepoint reread

Identify how interconnection, equipment, commissioning, and load dynamics prevent announced capacity from becoming usable compute.

### 19. The interconnection queue is a physical schedule `s17_interconnection_schedule`

- Opening question: What lies between a request for power and an energized feeder?
- Teaching objective: Separate dated administrative, energization, and planned permanent-equipment gates.
- Visual focus: AEP Abilene Northwest source, 138 kV slack-span tie, Initial 200 MW / 138 kV station, Unnamed 345 kV source, 345 kV expansion service, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **planned grid boundary — planned.**
  - 1200 MW
  - Scope: Original eight-building Abilene campus grid interconnection
  - Boundary: `planned_not_operational` / `planned` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **evidenced service milestones — confirmed.**
  - 2026-08-25 (ISO-8601 date)
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 2026-03-10 (ISO-8601 date)
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **initial aep delivery gates — confirmed.**
  - One 138 kV minimum 2000 A, 40 kA breaker; switches; SCADA; Lancium-terminal metering; power-quality metering; telecom equipment; and an overhead exit to a dead-end structure. (utility interconnection project scope)
  - Scope: AEP project T10433134 at Abilene Northwest station for the initial Lancium 138 kV path; not the customer-side campus substation or downstream bus.
  - Boundary: `confirmed` / `energized` / as of 2023-09-24
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF)
  - 2023-06-30 (ISO-8601 date)
  - Scope: AEP project T10433134 at Abilene Northwest 138 kV station
  - Boundary: `confirmed` / `energized` / as of 2023-06-30
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF)
  - An underground dead-end point of interconnect between Abilene Northwest 138 kV station and Lancium's 138 kV station for a 200 MW data center. (utility interconnection project scope)
  - Scope: AEP project T10434308 for the initial grid path; it does not establish the downstream data-center load, campus merge, or present load level.
  - Boundary: `confirmed` / `energized` / as of 2023-09-24
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF)
  - 2023-06-30 (ISO-8601 date)
  - Scope: AEP project T10434308, Abilene Northwest-Lancium 138 kV tie line
  - Boundary: `confirmed` / `energized` / as of 2023-06-30
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF)
- **expansion line schedule — planned.**
  - A 2.40-mile 345 kV transmission-line project from Mulberry Creek 345 kV Station to the Lancium 345 kV point of interconnect. (named utility construction project)
  - Scope: AEP project T10703126 in the July 2025 report; a named upstream project, not proof that this exact line was later completed or energized.
  - Boundary: `planned_not_operational` / `planned` / as of 2025-07-03
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF)
  - 2025-05-12 (ISO-8601 date)
  - Scope: Start-date field for AEP project T10703126 in the July 2025 construction report; the report does not label the field separately as estimated or actual.
  - Boundary: `planned_not_operational` / `planned` / as of 2025-07-03
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF)
  - 2025-11-21 (ISO-8601 date)
  - Scope: Planned construction-complete field for AEP project T10703126 as of the July 2025 report; not an actual completion or energization date.
  - Boundary: `planned_not_operational` / `planned` / as of 2025-07-03
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF)
- **expansion permanent transformer schedule — planned.**
  - 2026-10-31 (ISO-8601 month-end bound)
  - Scope: Planned replacement of three temporary expansion-substation transformers with permanent units
  - Boundary: `planned_not_operational` / `planned` / as of 2026-08-27
  - Sources: [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development)
- **private interconnection and load boundary — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Customer-specific queue identifier, study dates, application milestones, executed service agreement, contracted capacity, and load-ramp schedule for the original Abilene campus
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF), [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF), [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267)
  - Unknown — not established by the cited evidence
  - Scope: Contracted grid-service capacity for the original Abilene campus, separate from substation ratings and the planned 1.2 GW interconnection
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF), [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267)
  - Unknown — not established by the cited evidence
  - Scope: Current metered load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267)
  - Unknown — not established by the cited evidence
  - Scope: Current critical IT load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)

Red-line warnings:

- **planned to operational.** A planned milestone or capacity is not operational evidence.
- **single path conflation.** Do not identify distinct named, planned, conceptual, or energized paths as one completed physical path.
- **substation to it load.** Substation or feeder capacity does not establish current facility load or critical IT load.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Ask which package classes can constrain delivery without assigning Abilene's critical path.

### 20. Equipment delivery can become a schedule constraint `s18_long_lead_equipment`

- Opening question: Which box can delay an otherwise ready campus?
- Teaching objective: Contrast dated procurement, availability, and acceptance evidence across transformers, turbines, and cooling while keeping their non-equivalent bases separate.
- Visual focus: Gas turbine package, Generator step-up package, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Unit substation transformer, LV switchgear, UPS, Coolant distribution unit, Air-cooled chiller and condenser
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **gas authorization anchor — permitted.**
  - 10 units
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163)
- **energized transformer anchor — confirmed.**
  - 5 main power transformers
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 2026-03-10 (ISO-8601 date)
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **cooling design anchor — selected design.**
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **transformer delivery exposure — design reference.**
  - up to and exceeding 36 (months)
  - Scope: U.S. large-power-transformer market observation reported by DOE in July 2024; not a quote, order, or delivery forecast for an Abilene transformer.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy — Large Power Transformer Resilience Report to Congress](https://www.energy.gov/sites/default/files/2024-10/EXEC-2022-001242%20-%20Large%20Power%20Transformer%20Resilience%20Report%20signed%20by%20Secretary%20Granholm%20on%207-10-24.pdf)
  - 12-30 (months)
  - Scope: U.S. distribution-transformer market in 2023, the latest data stated on the DOE page; not a unit-substation or campus-transformer delivery quote.
  - Boundary: `design_not_observed` / `design_reference` / as of 2023
  - Sources: [U.S. Department of Energy Office of Electricity — Supply Chain and Market Analysis](https://www.energy.gov/oe/supply-chain-and-market-analysis)
  - prequalification, bidding, design, manufacture, testing, special transport, delivery, and installation (delivery-stage sequence)
  - Scope: Generic large-power-transformer procurement and delivery chain; not a site schedule, contractual critical path, or acceptance record.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy — Large Power Transformer Resilience Report to Congress](https://www.energy.gov/sites/default/files/2024-10/EXEC-2022-001242%20-%20Large%20Power%20Transformer%20Resilience%20Report%20signed%20by%20Secretary%20Granholm%20on%207-10-24.pdf)
- **turbine manufacturing slot — product reference.**
  - approximately 10 GW still available for 2029 delivery (GE Vernova portfolio availability)
  - Scope: GE Vernova gas-turbine portfolio statement on 2025-12-09; not a universal turbine lead time and not an Abilene Titan 350 or LM2500 delivery claim.
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2025-12-09
  - Sources: [GE Vernova — GE Vernova 2025 Investor Update Transcript](https://www.gevernova.com/sites/default/files/gev_webcast_transcript_12092025.pdf)
- **turbine slot dependency — design reference.**
  - A reserved manufacturing slot can precede site permitting and EPC-contract completion (project-delivery relationship)
  - Scope: GE Vernova's 2024 U.S. AI-load-related slot-reservation portfolio; not a rule for every project and not evidence about Longhorn procurement.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-12-10
  - Sources: [GE Vernova — GE Vernova 2024 Investor Update Transcript](https://www.gevernova.com/sites/default/files/gev_investor_update_transcript_12102024.pdf)
- **cooling product availability example — product reference.**
  - 2026-06 (first global shipment month)
  - Scope: Schneider Electric Uniflair XCA 1.3-2.5 MW chiller product family; a launch-availability milestone, not customer lead time or Abilene selection.
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-06-02
  - Sources: [Schneider Electric — Schneider Electric Introduces New Uniflair XCA Chiller Line](https://www.se.com/uk/en/about-us/newsroom/news/press-releases/Schneider-Electric-Introduces-New-Uniflair-XCA-Chiller-Line-Designed-to-Enhance-Energy-Performance-and-Operational-Stability-in-HighDensity-AI-Data-Centers-6a1e894ad8e4a8ed3c04dc8c/)
- **liquid cooling acceptance — design reference.**
  - pre-functional checks, flushing and cleaning validation, hydro and pressure testing, functional performance testing, and integrated testing (commissioning-stage sequence)
  - Scope: Generic manufacturer guidance for liquid-cooling projects, written in an India supply-chain context; not an Abilene acceptance plan or record.
  - Boundary: `design_not_observed` / `design_reference` / as of 2026-08-25
  - Sources: [Schneider Electric — Sources, spares, and commissioning liquid cooling in India: The supply-side](https://blog.se.com/datacenter/2026/08/25/sources-spares-and-commissioning-liquid-cooling-in-india-the-supply-side/)

Red-line warnings:

- **permitted to installed.** A permit does not prove equipment was installed.
- **permitted to commissioned.** A permit does not prove equipment was commissioned.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **market example to site schedule.** Market lead times and product availability examples do not establish Abilene's schedule or critical path.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.

Handoff: Contrast multi-year construction with millisecond load behavior.

### 21. Fast load, slow grid `s19_fast_load_slow_grid`

- Opening question: What happens when many accelerators change load together?
- Teaching objective: Connect external synchronized-load observations to generic ride-through architecture while keeping Abilene's transient profile and BESS connection explicit unknowns.
- Visual focus: Unnamed 345 kV source, 345 kV expansion service, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope, BESS package, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **bess future — future design.**
  - future (status)
  - Scope: BESS shown on the Longhorn power-plant review drawing
  - Boundary: `future_design` / `future_design` / as of 2024-12-04
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **bess operation unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: BESS at the original Abilene reference campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
- **operating compute anchor — confirmed.**
  - NVIDIA GB200 (platform family)
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **synchronized ai load dynamics — design reference.**
  - less than 1 (second)
  - Scope: NERC-observed transition between AI training and checkpoint saving in a 50 MW block of a larger 200 MW facility; not an Abilene waveform.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-07
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf)
  - 1.9 per unit per second for approximately 250 milliseconds
  - Scope: Fastest interval in NERC's 50 MW-block AI-training observation; not a universal AI profile, processor specification, or Abilene measurement.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-07
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf)
  - Millisecond processor-power variations can correlate during hyperscale parallel AI work and become significant at the site-demand boundary. (load-dynamics relationship)
  - Scope: Generic grid-level modeling principle for AI training and inference; not an Abilene transient magnitude, frequency, or operating trace.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf)
  - Large power-electronic loads can shift in seconds, faster than conventional generators can ramp (response-time relationship)
  - Scope: Generic North American bulk-power-system relationship; not a response requirement, reserve product, or measured condition at Abilene.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-07
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf)
- **voltage sensitive load event — design reference.**
  - 1500 MW approximate customer-side load reduction
  - Scope: NERC's 2024 Eastern Interconnection incident involving a concentration of data-center-type load; not Abilene and not an AI-training ramp event.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07-10
  - Sources: [North American Electric Reliability Corporation — Incident Review - Considering Simultaneous Voltage-Sensitive Load Reductions](https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_large_load_loss.pdf)
- **ride through engineering boundary — design reference.**
  - A battery-backed UPS can assume load for a short grid disturbance or bridge until backup generation starts. (generic ride-through role)
  - Scope: Generic static-UPS behavior described in a NERC incident review; not an Abilene UPS design, setting, capacity, runtime, or transfer sequence.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-01-08
  - Sources: [North American Electric Reliability Corporation — Incident Review - Considering Simultaneous Voltage-Sensitive Load Reductions](https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_large_load_loss.pdf)
  - UPS ride-through depends on OEM capability, protection settings, operating mode, current limiting, synchronism, and output-voltage regulation. (configuration dependency)
  - Scope: Generic double-conversion UPS behavior; no Abilene control or protection setting is inferred.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf)
  - UPS provides conditioned no-break critical-load power; conventional behind-the-meter BESS provides site-level energy management, flexibility, and longer-duration reserve energy. (generic architectural distinction)
  - Scope: Generic large-data-center architecture; not an Abilene equipment function, topology, rating, runtime, dispatch mode, or operating state.
  - Boundary: `design_not_observed` / `design_reference` / as of 2026-06-26
  - Sources: [Vertiv — BESS and UPS roles in large data center power architectures](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/)
- **operating load shaping observations — confirmed.**
  - tens of MW, nearly instantaneous ramps, recurring as often as every few seconds (operator-observed load pattern)
  - Scope: Google's batch-synchronous ML workloads on dedicated Google clusters; not a universal GPU behavior or an Abilene operating trace.
  - Boundary: `confirmed` / `operating` / as of 2025-02-11
  - Sources: [Google Cloud — Balance of power: A full-stack approach to power and thermal fluctuations in ML infrastructure](https://cloud.google.com/blog/topics/systems/mitigating-power-and-thermal-fluctuations-in-ml-infrastructure)
  - nearly 50 (percent reduction in fluctuation magnitude in Google's test case)
  - Scope: Google's compiler-based TPU workload-shaping test; not a guaranteed result for other hardware, workloads, sites, or the Abilene GB200 platform.
  - Boundary: `confirmed` / `deployed` / as of 2025-02-11
  - Sources: [Google Cloud — Balance of power: A full-stack approach to power and thermal fluctuations in ML infrastructure](https://cloud.google.com/blog/topics/systems/mitigating-power-and-thermal-fluctuations-in-ml-infrastructure)
- **abilene transient and bess boundary — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Procurement, function, power and energy ratings, duration, connection, controls, installation, energization, commissioning, and operation of a BESS at the original Abilene reference campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf)
  - Unknown — not established by the cited evidence
  - Scope: Magnitude, ramp rate, periodicity, duration, and grid-facing response of synchronized compute demand at the original Abilene reference campus
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf), [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf), [Google Cloud — Balance of power: A full-stack approach to power and thermal fluctuations in ML infrastructure](https://cloud.google.com/blog/topics/systems/mitigating-power-and-thermal-fluctuations-in-ml-infrastructure)

Red-line warnings:

- **future design to operational.** A future design is not installed, commissioned, or operational.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Put fast and slow constraints onto the same delivery funnel.

### 22. The build sequence is the binding constraint `s20_build_sequence`

- Opening question: At which gate did the announced capacity stop?
- Teaching objective: Apply the status funnel without substituting one capacity basis for another.
- Visual focus: Initial 200 MW / 138 kV station, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **planned grid boundary — planned.**
  - 1200 MW
  - Scope: Original eight-building Abilene campus grid interconnection
  - Boundary: `planned_not_operational` / `planned` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts)
- **infrastructure milestones — confirmed.**
  - 2026-08-25 (ISO-8601 date)
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
  - 2026-03-10 (ISO-8601 date)
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development)
- **energized minimum — confirmed minimum.**
  - 2 buildings
  - Scope: Original eight-building Abilene campus
  - Boundary: `confirmed_minimum` / `energized` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [Crusoe — Crusoe announces new 900 MW AI factory campus in Abilene, Texas, to support Microsoft AI infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure)
- **installed gpu no estimate — no evidence backed estimate.**
  - No evidence-backed estimate
  - Scope: Original Abilene campus installed or operational GPU fleet
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts), [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **live compute boundary — live by.**
  - 2025-07-22 (ISO-8601 date)
  - Scope: Parts of the original Abilene campus
  - Boundary: `live_by_not_start_date` / `operating` / as of 2025-07-22
  - Sources: [OpenAI — Stargate advances with partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)
- **untyped delivery boundary — reported untyped.**
  - 42 percent
  - Scope: Oracle's Abilene portfolio-page wording
  - Boundary: `reported_untyped` / `delivered_untyped` / as of 2026-08-25
  - Sources: [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/)
- **dated construction and operation sequence — confirmed.**
  - 2024-06 (ISO-8601 month)
  - Scope: Original Abilene AI data-center campus construction
  - Boundary: `confirmed` / `constructed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
  - 2025-09-30 (ISO-8601 date upper bound)
  - Scope: First two buildings of the original Abilene campus
  - Boundary: `confirmed` / `energized` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
  - 2025-09-30 (ISO-8601 date upper bound)
  - Scope: First phase of the original Abilene campus on Oracle Cloud Infrastructure
  - Boundary: `confirmed` / `operating` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **remaining buildings plan — planned.**
  - 2026-12-31 (ISO-8601 year-end bound)
  - Scope: Six remaining buildings in the second phase of the original eight-building campus; excludes the adjacent Microsoft campus
  - Boundary: `planned_not_operational` / `planned` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe Announces New 900 MW AI Factory Campus in Abilene, Texas, to Support Microsoft AI Infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure)
- **current delivery boundary — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Exact number of operational buildings in the original eight-building campus as of 2026-08-27
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [Crusoe — Crusoe Announces New 900 MW AI Factory Campus in Abilene, Texas, to Support Microsoft AI Infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure)
  - Unknown — not established by the cited evidence
  - Scope: Current metered load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267)
  - Unknown — not established by the cited evidence
  - Scope: Current critical IT load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)

Red-line warnings:

- **planned to operational.** A planned milestone or capacity is not operational evidence.
- **minimum to exact.** A confirmed minimum is not an exact current count.
- **untyped to capacity.** An untyped delivery percentage does not establish MW, buildings, racks, accelerators, or workload capacity.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **substation to it load.** Substation or feeder capacity does not establish current facility load or critical IT load.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.
- **live by to start date.** A live-by disclosure is only an upper date bound, not an exact start date.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.

Handoff: Reread the same gates by ownership rather than engineering function.

## Act 6: Capital-stack reread

Separate ownership, financing, operation, offtake, and utilization risk across the same physical topology.

### 23. Same hardware, different commercial roles `s21_capital_ownership`

- Opening question: Which roles are publicly named, and which asset-level owners remain unknown?
- Teaching objective: Distinguish named program, project, phase, and operating roles without assigning them to every highlighted asset.
- Visual focus: Gas turbine package, Generator, Generator step-up package, AEP Abilene Northwest source, 138 kV slack-span tie, Initial 200 MW / 138 kV station, Unnamed 345 kV source, 345 kV expansion service, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Nuclear PPA overlay, Abstract campus MV distribution envelope, BESS package, Emergency diesel backup package, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die, Air-cooled rack auxiliaries, Cold plate, Rack supply and return headers, Coolant distribution unit, CRAH / fan-wall branch, Closed facility water loop, Air-cooled chiller and condenser, Initial fill and water treatment, Atmosphere
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **stargate responsibility structure — reported structure.**
  - SoftBank, OpenAI, Oracle, and MGX (named initial equity funders)
  - Scope: Stargate company/program formation; not per-asset Abilene ownership
  - Boundary: `confirmed` / `announced_structure` / as of 2025-01-21
  - Sources: [OpenAI and SoftBank — Announcing The Stargate Project](https://openai.com/index/announcing-the-stargate-project/)
  - SoftBank has financial responsibility and OpenAI has operational responsibility as Stargate's lead partners. (program-level responsibility allocation)
  - Scope: Stargate company/program; not ownership or operation of every Abilene asset
  - Boundary: `confirmed` / `announced_structure` / as of 2025-01-21
  - Sources: [OpenAI and SoftBank — Announcing The Stargate Project](https://openai.com/index/announcing-the-stargate-project/)
- **abilene developer roles — reported structure.**
  - Crusoe would own and develop the initial Abilene data center. (announced project role)
  - Scope: Initial 200 MW Abilene data-center development as announced in July 2024
  - Boundary: `confirmed` / `announced_structure` / as of 2024-07-18
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center)
  - Lancium's announced end-to-end role includes land acquisition, power interconnection, site engineering, renewable interconnection, and power orchestration. (announced project role)
  - Scope: Lancium Clean Campus / initial Abilene development
  - Boundary: `confirmed` / `announced_structure` / as of 2024-07-18
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center)
- **phase1 delivery and operations contract — contract reference.**
  - Crusoe designs, builds, and operates the 206 MW phase-one data center. (named project role)
  - Scope: Phase-one 206 MW, 998,000-square-foot Abilene joint-venture asset
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2024-10-15
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture)
- **operating compute roles — confirmed.**
  - Oracle delivered the first NVIDIA GB200 racks, and OpenAI reported running early training and inference workloads on operating Abilene capacity. (named compute delivery and workload roles)
  - Scope: Operating parts of Stargate I at Abilene; not legal title to the equipment
  - Boundary: `confirmed` / `operating` / as of 2025-07-22
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)
- **legal ownership boundary — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Land underlying the original eight-building Abilene development
  - Boundary: `unverified_null` / `ownership_unknown` / as of 2026-08-27
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture)
  - Unknown — not established by the cited evidence
  - Scope: Abilene utility ties, substations, onsite generation, backup generation, storage, campus distribution, and building electrical equipment
  - Boundary: `unverified_null` / `ownership_unknown` / as of 2026-08-27
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture)
  - Unknown — not established by the cited evidence
  - Scope: Installed Abilene racks, accelerators, network, and associated IT equipment
  - Boundary: `unverified_null` / `ownership_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)
  - Unknown — not established by the cited evidence
  - Scope: Phase-one two-building Abilene lease
  - Boundary: `unverified_null` / `counterparty_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)

Red-line warnings:

- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **named role to asset assignment.** Do not apply program, project, phase, or operating-part roles to every highlighted asset; their published scopes remain distinct.
- **contractual to physical.** A contract or commercial role does not establish physical power flow or asset control.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **announced to operational.** An announced structure or role does not prove current operation.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Follow the timing of cash outlays and revenue eligibility across those roles.

### 24. Who pays before the first token? `s22_capital_risk`

- Opening question: What facility-level financing and lease structure is public, and which per-box capital and earning gates remain undisclosed?
- Teaching objective: Separate disclosed project financing from undisclosed equipment finance, acceptance, rent, and utilization terms without allocating them by node.
- Visual focus: Gas turbine package, Generator step-up package, Initial 200 MW / 138 kV station, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, GPU die, Coolant distribution unit, Air-cooled chiller and condenser
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **phase1 financing and lease — contract reference.**
  - A $3.4 billion fully funded forward takeout, with funds managed by Blue Owl's Real Estate platform and Primary Digital Infrastructure jointly sponsoring the 206 MW data center designed, built, and operated by Crusoe. (named transaction structure)
  - Scope: Phase-one 206 MW Abilene joint venture only
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2024-10-15
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture)
  - The phase-one two-building project was 100 percent long-term leased to an unnamed Fortune 100 hyperscale tenant. (named lease posture)
  - Scope: Phase-one Abilene data center only
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2024-10-15
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture)
- **phase2 joint venture — contract reference.**
  - Crusoe, funds managed by Blue Owl's Real Assets platform, and Primary Digital Infrastructure jointly sponsor construction of six additional buildings under the second phase of a $15 billion joint venture. (named transaction structure)
  - Scope: Six-building phase-two Abilene expansion
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2025-05-21
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture)
- **undisclosed capital and risk terms — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Phase-one Abilene tenant lease
  - Boundary: `unverified_null` / `contract_term_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture)
  - Unknown — not established by the cited evidence
  - Scope: Original eight-building Abilene development and its phase-specific joint ventures
  - Boundary: `unverified_null` / `financing_terms_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture)
  - Unknown — not established by the cited evidence
  - Scope: Phase-one and phase-two Abilene leases and customer arrangements
  - Boundary: `unverified_null` / `contract_term_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture)
  - Unknown — not established by the cited evidence
  - Scope: Abilene accelerators, racks, networking, and associated IT equipment
  - Boundary: `unverified_null` / `financing_terms_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)
  - Unknown — not established by the cited evidence
  - Scope: Abilene facility occupancy and compute utilization
  - Boundary: `unverified_null` / `contract_term_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)

Red-line warnings:

- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **facility financing to component allocation.** Do not allocate facility-level finance, acceptance, rent, or utilization terms to individual equipment; those terms remain undisclosed.
- **contractual to physical.** A contract or commercial role does not establish physical power flow or asset control.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Compare how different business models reallocate those same risks.

### 25. Business models recolor the same machine `s23_business_models`

- Opening question: What changes between developer, colo, neocloud, and hyperscaler models?
- Teaching objective: Compare contractual and risk allocations without changing physical topology.
- Visual focus: Nuclear PPA overlay, Unnamed 345 kV source, Gas turbine package, Abstract campus MV distribution envelope, Rack power shelves, GPU die
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **colocation comparison — business model reference.**
  - Equinix's IBX colocation offering supplies secure data-center space and power for customers' IT infrastructure, typically bills from space and power consumption under fixed-duration contracts, and generates monthly recurring revenue; contracts are generally one to five years. (named business-model comparison)
  - Scope: Equinix IBX colocation as reported for 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [Equinix, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1101239/000110123926000032/eqix-20251231.htm)
  - Equinix operates the IBX facility environment while customers colocate their IT equipment; Equinix owns some IBX facilities and leases others, and landlord control of base infrastructure varies by lease. (named asset and operating boundary)
  - Scope: Equinix IBX portfolio as reported for 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [Equinix, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1101239/000110123926000032/eqix-20251231.htm)
- **neocloud operating comparison — business model reference.**
  - CoreWeave primarily finances infrastructure development with asset-level debt supported by take-or-pay customer contracts, supplemented by corporate equity and debt; it also offers pay-as-you-go access. (named business-model comparison)
  - Scope: CoreWeave AI cloud as reported for 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [CoreWeave, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm)
  - CoreWeave leases or licenses third-party data-center space and does not control operation of those facilities; under certain separate lease arrangements it must procure and install lessee-owned equipment. (named asset and operating boundary)
  - Scope: CoreWeave portfolio and disclosed commitments as of 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [CoreWeave, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm)
- **neocloud contract risk comparison — contract reference.**
  - CoreWeave committed contracts typically require payment regardless of utilization, while on-demand arrangements permit usage reductions with limited notice; multi-year fixed-capacity facility leases can leave CoreWeave paying for capacity that customers do not use and pay for. (named risk-allocation comparison)
  - Scope: CoreWeave contracts and facility leases as reported for 2025; not Abilene
  - Boundary: `confirmed_contract` / `operating_business_model` / as of 2025-12-31
  - Sources: [CoreWeave, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm)
- **hyperscale cloud comparison — business model reference.**
  - Microsoft operates data centers, owns and leases facilities, invests in data centers and computer systems, and sells Azure and other cloud services; aggregating diverse demand is part of its stated utilization economics. (named business-model comparison)
  - Scope: Microsoft hyperscale cloud as reported for fiscal 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-06-30
  - Sources: [Microsoft Corporation — 2025 Annual Report](https://www.microsoft.com/investor/reports/ar25/index.html)

Red-line warnings:

- **contractual to physical.** A contract or commercial role does not establish physical power flow or asset control.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.

Handoff: Return to the opening question with every physical and economic gate visible.

## Act 7: From delivered power to usable compute

Teach an assumption-bound conversion recipe without inventing an Abilene token estimate.

### 26. From delivered megawatts to tokens `s24_megawatts_to_tokens`

- Opening question: Given delivered power, how many useful tokens result?
- Teaching objective: Keep power-rate and energy-yield routes dimensionally separate, require matching hardware and workload measurements, and preserve the no-estimate boundary for the reference campus.
- Visual focus: Abstract campus MV distribution envelope, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die, Cold plate, Rack supply and return headers, Coolant distribution unit, Closed facility water loop, Air-cooled chiller and condenser, Atmosphere
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Validated claim territory:

- **current installed gpu no estimate — no evidence backed estimate.**
  - No evidence-backed estimate
  - Scope: Original Abilene campus installed or operational GPU fleet
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts), [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **untyped delivery boundary — reported untyped.**
  - 42 percent
  - Scope: Oracle's Abilene portfolio-page wording
  - Boundary: `reported_untyped` / `delivered_untyped` / as of 2026-08-25
  - Sources: [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/)
- **operating platform anchor — confirmed.**
  - NVIDIA GB200 (platform family)
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live)
- **rack power product reference — product reference.**
  - 50-51 (VDC)
  - Scope: NVIDIA DGX GB200 rack power-shelf nominal DC busbar output
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **selected heat rejection — selected design.**
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
- **pue accounting boundary — method reference.**
  - PUE is total data-center energy consumption over a continuous 12-month period divided by IT-equipment energy consumption over the same period; IT equipment includes equipment used to store, process, and transport data. (authoritative energy-accounting definition)
  - Scope: ISO/IEC 30134-2:2026 PUE; not an Abilene measurement
  - Boundary: `authoritative_guidance` / `accounting_standard` / as of 2026-01-16
  - Sources: [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen)
- **facility to it scenario step — derived scenario reference.**
  - For a matching continuous 12-month boundary, scenario IT energy equals scenario total data-center energy divided by scenario PUE. An average-power route instead requires direct IT-power metering or a boundary-matched interim or partial PUE over the same averaging interval; annual PUE must not be silently treated as a point-in-time operating ratio. (scenario calculation rule)
  - Scope: Energy-accounting step in a hypothetical scenario; not an Abilene estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen)
- **rack compute product reference — product reference.**
  - One NVIDIA DGX GB NVL72 rack contains 72 GPUs across 18 compute trays and has approximate rack power consumption of 120 kW. (manufacturer product configuration)
  - Scope: NVIDIA DGX GB rack-scale product documentation; not Abilene installed quantity or draw
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **training published method — method reference.**
  - Model FLOPs utilization is observed training throughput in tokens per second divided by the theoretical maximum token throughput of the same system operating at peak FLOPs, counting the model-required forward and backward operations rather than implementation-dependent rematerialization. (training-efficiency definition)
  - Scope: Training-system analysis in the PaLM paper; not inference utilization or Abilene MFU
  - Boundary: `authoritative_guidance` / `published_method` / as of 2022-10-05
  - Sources: [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311)
  - For the PaLM paper's dense decoder-only training boundary, theoretical FLOPs per token are 6N plus 12LHQT, where N is parameter count and L, H, Q, and T are layers, attention heads, head dimension, and sequence length. (published training-method boundary)
  - Scope: Dense decoder-only training under the PaLM counting convention; not a general inference formula and not an Abilene estimate
  - Boundary: `authoritative_guidance` / `published_method` / as of 2022-10-05
  - Sources: [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311)
- **training scenario step — derived scenario reference.**
  - Scenario training tokens per second equal exact active aggregate peak matmul FLOP/s times MFU measured for the same model and system, divided by the model's FLOPs-per-token term. Supply active hardware quantity and applicable per-device performance explicitly. If the route begins from accelerator power, reconcile the selected inventory's measured power to that same power boundary. Apply a separate fleet active-duty factor only when MFU is conditional on active execution. (derived training scenario rule)
  - Scope: Dense decoder-only training under the PaLM counting convention; not a general inference formula and not an Abilene estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
- **inference published boundaries — method reference.**
  - Triton dynamic batching combines requests and typically increases throughput; batch size and queue delay are configured per model and can trade increased latency for throughput. (runtime performance dependency)
  - Scope: NVIDIA Triton inference serving; not an Abilene runtime configuration
  - Boundary: `authoritative_guidance` / `product_documented` / as of 2026-08-27
  - Sources: [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html)
  - A defensible inference-throughput result names the model, dataset or workload, quality target, scenario, system under test, and latency constraints. MLPerf separates Offline measured throughput from Server maximum supported throughput under benchmark-specific latency limits and records time to first token and time per output token for LLMs. (benchmark measurement boundary)
  - Scope: MLPerf Inference methodology; not an Abilene benchmark result
  - Boundary: `authoritative_guidance` / `benchmark_method` / as of 2026-08-27
  - Sources: [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)
- **inference scenario step — derived scenario reference.**
  - Use measured tokens per joule for the exact model, weights or quantization, hardware, software, batch and concurrency policy, input/output-length distribution, quality target, and latency boundary, so matching accelerator watts times tokens per joule yields tokens per second. Alternatively, scale exact-system measured tokens per second only by a matching system count and measured scale-efficiency factor, with matching measured power as a consistency check. Facility MW or product peak FLOPs alone do not establish inference tokens per second. (scenario calculation rule)
  - Scope: Hypothetical inference scenario; not an Abilene estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html), [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)
- **complete scenario recipe — derived scenario reference.**
  - Choose one output and one common averaging interval. For a power-rate route, start with measured average facility power over that interval; obtain matching average IT power from direct metering or a boundary-matched interim or partial PUE, then obtain accelerator power from direct metering or a measured IT-power share. For training, supply exact active hardware quantity, applicable aggregate peak matmul FLOP/s, and MFU measured for the same model and system; divide aggregate peak FLOP/s times MFU by model FLOPs per token. Apply a separate fleet active-duty factor only when MFU is conditional on active execution, and reconcile the inventory's measured power with accelerator power. For inference, multiply matching accelerator watts by tokens per joule measured for the exact model, weights or quantization, hardware, software, batching, input/output distribution, quality, and latency boundary; or scale exact-system tokens per second with matching system count and measured scale efficiency. For an energy-yield route, start with facility energy over the interval, derive matching IT energy, then use measured accelerator-energy share and matching tokens per joule, or integrate the rate route over the same interval, to produce token count. Annual PUE is valid only for its matching annual boundary. Propagate ranges and stop with no estimate when any required site input is unavailable. (assumption-driven scenario recipe)
  - Scope: General teaching recipe; produces no Abilene token estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html), [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html), [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311), [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)
- **site power no estimates — no evidence backed estimate.**
  - No evidence-backed estimate
  - Scope: Current operating total-facility power for the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/)
  - No evidence-backed estimate
  - Scope: Current operating IT-equipment power for the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/)
  - No evidence-backed estimate
  - Scope: Measured current PUE, iPUE, or pPUE for the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/), [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen)
- **site compute no estimates — no evidence backed estimate.**
  - No evidence-backed estimate
  - Scope: Installed or operational accelerator fleet at the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
  - No evidence-backed estimate
  - Scope: Usable accelerator power at the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html)
  - No evidence-backed estimate
  - Scope: Accelerator share of current Abilene IT-equipment power
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/)
  - No evidence-backed estimate
  - Scope: Time- and fleet-weighted active accelerator utilization at Abilene
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/)
  - No evidence-backed estimate
  - Scope: Any training workload running at Abilene
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311)
  - No evidence-backed estimate
  - Scope: Any training or inference workload at the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/), [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc)
- **site workload configuration unknown — explicit unknown.**
  - Unknown — not established by the cited evidence
  - Scope: Abilene training and inference workloads
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/)
  - Unknown — not established by the cited evidence
  - Scope: Abilene inference workloads
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/), [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html)

Red-line warnings:

- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **design ceiling to installed.** A design ceiling does not establish installed or operating quantity.
- **untyped to capacity.** An untyped delivery percentage does not establish MW, buildings, racks, accelerators, or workload capacity.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **energy power time basis.** Keep power rates and energy totals on one explicit, matching averaging interval.
- **power to compute bridge.** Do not convert power to compute without matching hardware quantity, measured power, workload efficiency, and system boundaries.
- **scenario to site estimate.** A derived scenario is not a site estimate; missing site inputs must stop the calculation.

Close: Return to the opening question and state which conversions are evidenced, assumed, or still unknown.
