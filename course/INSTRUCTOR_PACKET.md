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

Presenter-facing teaching focus:

- Kind: `funnel`
- Title: Five stages; PERMITTED is a separate authorization

1. PLANNED — 1.2 GW grid interconnection
   - Claim IDs: `planned_grid_boundary`
2. CONSTRUCTED — 200 MW / 138 kV station; PERMITTED gas/diesel is a separate axis
   - Claim IDs: `initial_substation_rating`, `permitted_gas_layer`, `permitted_diesel_layer`
3. ENERGIZED — 1 GW / 345 kV station and at least two buildings
   - Claim IDs: `expansion_substation_rating`, `energized_building_minimum`
4. LIVE — training and inference within a published date boundary
   - Claim IDs: `workloads_live_by`
5. UNKNOWN — delivered basis, exact operations, and installed GPUs
   - Claim IDs: `untyped_delivery_percentage`, `operational_buildings_unknown`, `installed_gpu_no_estimate`

Validated claim territory:

- **planned grid boundary — planned.**
  - Binding: segment-local, nonphysical teaching overlay
  - 1200 MW
  - Fact: `abilene:planned_grid_interconnection_mw`
  - Basis: Crusoe explicitly describes 1.2 GW as the site's grid interconnection.
  - Scope: Original eight-building Abilene campus grid interconnection
  - Boundary: `planned_not_operational` / `planned` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **initial substation rating — confirmed.**
  - Binding: selected topology ownership
  - 200 MW
  - Fact: `abilene:grid_initial_substation_capacity_mw`
  - Basis: Mortenson identifies the original substation phase as 200 MW.
  - Scope: Initial Abilene grid path
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Topology target: node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 138 kV
  - Fact: `abilene:grid_initial_substation_voltage_kv`
  - Basis: Mortenson identifies the original 200 MW substation as a 138 kV facility.
  - Scope: Initial Abilene grid path
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Topology target: node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **expansion substation rating — confirmed.**
  - Binding: selected topology ownership
  - 1000 MW
  - Fact: `abilene:grid_expansion_substation_capacity_mw`
  - Basis: Mortenson identifies the expansion substation as 1 GW.
  - Scope: Separate greenfield Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 345 kV
  - Fact: `abilene:grid_expansion_substation_voltage_kv`
  - Basis: Mortenson identifies the expansion as a 345 kV greenfield substation.
  - Scope: Separate greenfield Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **permitted gas layer — permitted.**
  - Binding: selected topology ownership
  - 360.5 MW
  - Fact: `abilene:gas_permitted_nameplate_mw`
  - Basis: Five units at 38 MW plus five units at 34.1 MW totals 360.5 MW.
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Topology target: node `gas_turbine` (Gas turbine package; `site_evidenced` / `permitted`)
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-25; Project reviewer dated 2025-01-21; section manager dated 2025-01-22.)
- **permitted diesel layer — permitted.**
  - Binding: selected topology ownership
  - 169.9 MW
  - Fact: `abilene:diesel_permitted_nameplate_mw`
  - Basis: Application class totals are 9 + 9 + 12 + 6 + 7.5 + 48 + 78.4 MW, totaling 169.9 MW across the 62 authorized units.
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-04-24
  - Topology target: node `diesel_backup_package` (Emergency diesel backup package; `site_evidenced` / `permitted`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056) (accessed 2026-08-25; Application supplies the complete engine-class counts and MW totals used to calculate 62 authorized units and 169.9 MW permitted nameplate.), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645) (accessed 2026-08-25; Project received 2025-04-11; reviewer and manager dated 2025-04-24.)
- **energized building minimum — confirmed minimum.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2 buildings
  - Fact: `abilene:buildings_energized_confirmed_min`
  - Basis: Crusoe reported the first two buildings energized and the first phase live; the 2026 Microsoft-expansion release reiterates the two original buildings.
  - Scope: Original eight-building Abilene campus
  - Boundary: `confirmed_minimum` / `energized` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.), [Crusoe — Crusoe announces new 900 MW AI factory campus in Abilene, Texas, to support Microsoft AI infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) (accessed 2026-08-25; Describes a separate adjacent two-building project whose first building was then expected in mid-2027.)
- **operational buildings unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene:operational_buildings_exact`
  - Basis: Primary sources establish a lower bound of two but do not establish the exact current operational count as of the ledger access date.
  - Scope: Original eight-building Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.), [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/) (accessed 2026-08-25; Undated page marked information current January 2026 reports 42 percent of an unspecified total-capacity denominator delivered; the percentage cannot be converted to MW, buildings, IT load, or current load.)
- **installed gpu no estimate — no evidence backed estimate.**
  - Binding: segment-local, nonphysical teaching overlay
  - No evidence-backed estimate
  - Fact: `abilene:installed_gpu_count`
  - Basis: no evidence-backed estimate
  - Scope: Original Abilene campus installed or operational GPU fleet
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.), [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **workloads live by — live by.**
  - Binding: selected topology ownership
  - 2025-07-22 (ISO-8601 date)
  - Fact: `abilene:early_training_inference_live_by`
  - Basis: OpenAI reported on this date that parts of the facility were running and had recently begun early training and inference workloads.
  - Scope: Parts of the original Abilene campus
  - Boundary: `live_by_not_start_date` / `operating` / as of 2025-07-22
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [OpenAI — Stargate advances with partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-25; Reports parts of the Abilene facility running and recent early training and inference workloads; the exact workload start date is not supplied.)
- **untyped delivery percentage — reported untyped.**
  - Binding: segment-local, nonphysical teaching overlay
  - 42 percent
  - Fact: `abilene:oracle_capacity_delivered_percent_untyped`
  - Basis: Oracle reports 42 percent of total capacity delivered without stating the denominator, capacity basis, MW, building count, IT load, or current load.
  - Scope: Oracle's Abilene portfolio-page wording
  - Boundary: `reported_untyped` / `delivered_untyped` / as of 2026-01
  - Sources: [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/) (accessed 2026-08-25; Undated page marked information current January 2026 reports 42 percent of an unspecified total-capacity denominator delivered; the percentage cannot be converted to MW, buildings, IT load, or current load.)
- **adjacent project exclusion — excluded scope.**
  - Binding: segment-local, nonphysical teaching overlay
  - No (boolean)
  - Fact: `abilene:adjacent_microsoft_scope_included`
  - Basis: Crusoe describes this as a separate adjacent 900 MW project with a later delivery schedule; it is excluded from the original eight-building ledger.
  - Scope: Adjacent two-building Microsoft AI infrastructure expansion
  - Boundary: `excluded_scope` / `planned` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe announces new 900 MW AI factory campus in Abilene, Texas, to support Microsoft AI infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) (accessed 2026-08-25; Describes a separate adjacent two-building project whose first building was then expected in mid-2027.)

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

Presenter-facing teaching focus:

- Kind: `layers`
- Title: Four independent visual channels

1. COLOR = carrier, independent of lifecycle
   - Claim IDs: `energized_example`, `permitted_example`, `selected_design_example`
2. DIRECTION = initial 138 kV tie → initial 200 MW / 138 kV station
   - Claim IDs: `energized_example`
3. STROKE = energized, permitted, future-design, or conceptual lifecycle
   - Claim IDs: `energized_example`, `permitted_example`, `future_example`, `unknown_example`, `selected_design_example`
4. POSTURE = claim copy / evidence drawer, not stroke
   - Claim IDs: `energized_example`, `permitted_example`, `future_example`, `unknown_example`, `selected_design_example`

Validated claim territory:

- **energized example — confirmed.**
  - Binding: selected topology ownership
  - 2026-08-25 (ISO-8601 date)
  - Fact: `abilene:grid_initial_service_operational_as_of`
  - Basis: Mortenson's current project page says the initial substation transitioned from de-energized construction into energized, operational service; it does not disclose the exact first-energization date.
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Topology target: node `initial_tie_138` (138 kV slack-span tie; `site_evidenced` / `energized`); node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`); edge `grid138_tie_to_station` (138 kV slack-span tie → Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **permitted example — permitted.**
  - Binding: selected topology ownership
  - 10 units
  - Fact: `abilene:gas_turbine_units_authorized`
  - Basis: Five Solar Titan 350 units plus five GE LM2500 units are authorized.
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Topology target: node `gas_turbine` (Gas turbine package; `site_evidenced` / `permitted`); node `generator` (Generator; `site_evidenced` / `permitted`); edge `btm_fuel_to_shaft` (Gas turbine package → Generator; `site_evidenced` / `permitted`)
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-25; Project reviewer dated 2025-01-21; section manager dated 2025-01-22.)
- **future example — future design.**
  - Binding: selected topology ownership
  - future (status)
  - Fact: `abilene:bess_reference_design_status`
  - Basis: Drawing 5MECH-00001-GA labels the BESS unit as FUTURE.
  - Scope: BESS shown on the Longhorn power-plant review drawing
  - Boundary: `future_design` / `future_design` / as of 2024-12-04
  - Topology target: node `bess_package` (BESS package; `site_evidenced` / `future_design`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **unknown example — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:campus_lpt_secondary_as_built_voltage_kv`
  - Basis: The available review drawing establishes a 34.5 kV Longhorn interface but does not establish the as-built campus LPT ratio or all-building MV voltage.
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Topology target: node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **selected design example — selected design.**
  - Binding: selected topology ownership
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Fact: `abilene:cooling_heat_rejection_posture`
  - Basis: Crusoe describes a selected closed-loop, non-evaporative liquid-cooling system with air-cooled chillers and no water consumed in heat rejection.
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Topology target: node `air_cooled_chiller` (Air-cooled chiller and condenser; `site_evidenced` / `conceptual`); edge `chiller_to_atmosphere` (Air-cooled chiller and condenser → Atmosphere; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)

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
- Visual focus: Gas turbine package, Generator, Generator step-up package
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `layers`
- Title: Conversion path and evidence posture are separate

1. Generic conversion: combustion gas → shaft → generator-terminal electricity
   - Claim IDs: `turbine_generator_conversion_reference`
2. Ten units totaling 360.5 MW remain permit scope
   - Claim IDs: `gas_authorization`
3. Onsite plant and GE Vernova turbine family confirmed installed
   - Claim IDs: `installed_turbine_presence`
4. Installed count, model mix, commissioning, output, and operation remain unknown
   - Claim IDs: `installed_turbine_configuration_unknown`, `operating_posture_unknown`

Validated claim territory:

- **gas authorization — permitted.**
  - Binding: selected topology ownership
  - 10 units
  - Fact: `abilene:gas_turbine_units_authorized`
  - Basis: Five Solar Titan 350 units plus five GE LM2500 units are authorized.
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Topology target: node `gas_turbine` (Gas turbine package; `site_evidenced` / `permitted`); node `generator` (Generator; `site_evidenced` / `permitted`); edge `btm_fuel_to_shaft` (Gas turbine package → Generator; `site_evidenced` / `permitted`)
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-25; Project reviewer dated 2025-01-21; section manager dated 2025-01-22.)
  - 360.5 MW
  - Fact: `abilene:gas_permitted_nameplate_mw`
  - Basis: Five units at 38 MW plus five units at 34.1 MW totals 360.5 MW.
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Topology target: node `gas_turbine` (Gas turbine package; `site_evidenced` / `permitted`)
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-25; Project reviewer dated 2025-01-21; section manager dated 2025-01-22.)
- **turbine generator conversion reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A moving fluid, including combustion gas, pushes turbine blades and rotates the generator rotor shaft.
  - Fact: `electrical_engineering:turbine_fluid_to_rotor_conversion`
  - Basis: EIA separates the moving-fluid turbine stage from the generator stage and explicitly includes combustion gases among the turbine-driving fluids.
  - Scope: Generic turbine-generator energy conversion; not an Abilene installation or operating claim
  - Boundary: `design_not_observed` / `design_reference` / as of 2023-10-31
  - Sources: [U.S. Energy Information Administration — How electricity is generated](https://www.eia.gov/energyexplained/electricity/how-electricity-is-generated.php) (accessed 2026-08-27; EIA marks the page last updated 2023-10-31.)
  - A generator converts the rotor's mechanical energy to electrical energy.
  - Fact: `electrical_engineering:generator_rotor_to_electricity_conversion`
  - Basis: EIA explicitly states that the generator converts the rotor's mechanical or kinetic energy into electrical energy.
  - Scope: Generic electromagnetic-generator function; not an Abilene generator output or operating claim
  - Boundary: `design_not_observed` / `design_reference` / as of 2023-10-31
  - Sources: [U.S. Energy Information Administration — How electricity is generated](https://www.eia.gov/energyexplained/electricity/how-electricity-is-generated.php) (accessed 2026-08-27; EIA marks the page last updated 2023-10-31.)
- **installed turbine presence — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - A new onsite power plant was delivered at Crusoe's Abilene data center. (site execution milestone)
  - Fact: `abilene_execution:onsite_power_plant_delivery_confirmed`
  - Basis: Crusoe's current energy page explicitly says it delivered a new onsite power plant at its Abilene data center.
  - Scope: Original Abilene campus onsite power plant as a delivered facility; excludes any claim about its installed unit count, commissioned MW, current output, or operating mode.
  - Boundary: `confirmed` / `constructed` / as of 2026-08-27
  - Sources: [Crusoe — An energy first approach to AI](https://www.crusoe.ai/energy) (accessed 2026-08-27; Undated current company page. It states that Crusoe delivered a new onsite power plant at its Abilene data center but does not quantify installed units, commissioned capacity, or current output.)
  - Advanced natural-gas turbines from GE Vernova were installed. (installed equipment family)
  - Fact: `abilene_execution:ge_vernovas_gas_turbines_installed`
  - Basis: Crusoe's project-specific engineering account says it strategically installed advanced natural-gas turbines from GE Vernova.
  - Scope: Original Abilene campus; manufacturer family and installation only, not installed count, exact model mix, commissioning, output, or availability.
  - Boundary: `confirmed` / `constructed` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)
- **installed turbine configuration unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:installed_gas_turbine_unit_count`
  - Basis: TCEQ authorizes ten units, while Crusoe confirms only that GE Vernova turbines were installed. Neither source says all ten authorized units or a specific count were installed.
  - Scope: Exact installed natural-gas-turbine count at the original Abilene campus
  - Boundary: `unverified_null` / `installation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-27; Regulatory review authorizes a ten-turbine model mix but does not establish which units were installed, commissioned, or operating.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:installed_gas_turbine_model_mix`
  - Basis: The permit authorizes a Solar and GE model mix; the company installation statement identifies GE Vernova but does not establish the installed Solar count, GE count, or complete installed mix.
  - Scope: Exact installed turbine model mix at the original Abilene campus
  - Boundary: `unverified_null` / `installation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-27; Regulatory review authorizes a ten-turbine model mix but does not establish which units were installed, commissioned, or operating.)
- **operating posture unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:gas_turbine_commissioned_capacity_mw`
  - Basis: Plant delivery and installed-turbine evidence do not quantify completed commissioning; the regulatory review is an authorization, not a commissioning record.
  - Scope: Commissioned natural-gas-turbine capacity at the original Abilene campus
  - Boundary: `unverified_null` / `commissioning_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An energy first approach to AI](https://www.crusoe.ai/energy) (accessed 2026-08-27; Undated current company page. It states that Crusoe delivered a new onsite power plant at its Abilene data center but does not quantify installed units, commissioned capacity, or current output.), [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-27; Regulatory review authorizes a ten-turbine model mix but does not establish which units were installed, commissioned, or operating.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:gas_turbine_current_output_mw`
  - Basis: No reviewed primary source reports a current telemetry value, dispatch interval, or measured output for the installed turbines.
  - Scope: Current output of the original Abilene campus gas-turbine plant
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An energy first approach to AI](https://www.crusoe.ai/energy) (accessed 2026-08-27; Undated current company page. It states that Crusoe delivered a new onsite power plant at its Abilene data center but does not quantify installed units, commissioned capacity, or current output.), [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-27; Regulatory review authorizes a ten-turbine model mix but does not establish which units were installed, commissioned, or operating.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:gas_turbine_current_operating_posture`
  - Basis: Crusoe states the intended ultimate backup role but does not state the plant's present dispatch or availability state.
  - Scope: Current running, standby, testing, unavailable, or other operating posture of the original Abilene campus gas-turbine plant
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)

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

Presenter-facing teaching focus:

- Kind: `comparison`
- Title: Reference voltage is not site configuration

1. Titan 350 model range 11–13.8 kV; selected site voltage unknown
   - Claim IDs: `model_voltage_range`, `site_voltage_unknown`
2. 34.5 kV is a review-design campus-interface reference
   - Claim IDs: `campus_interface_design`
3. Exact generator, GSU, and as-built campus interface remain unknown
   - Claim IDs: `campus_interface_unknown`, `site_generator_configuration_boundary`

Validated claim territory:

- **generator authorization — permitted.**
  - Binding: selected topology ownership
  - 10 units
  - Fact: `abilene:gas_turbine_units_authorized`
  - Basis: Five Solar Titan 350 units plus five GE LM2500 units are authorized.
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Topology target: node `generator` (Generator; `site_evidenced` / `permitted`)
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-25; Project reviewer dated 2025-01-21; section manager dated 2025-01-22.)
- **model voltage range — product reference.**
  - Binding: selected topology ownership
  - 11-13.8 (kV AC)
  - Fact: `abilene:generator_terminal_model_voltage_range_kv`
  - Basis: Solar's Titan 350 datasheet specifies selectable generator voltages from 11,000 to 13,800 VAC.
  - Scope: Solar Titan 350 38 MW generator-set model range
  - Boundary: `model_range_not_site_configured` / `product_documented` / as of 2022-05
  - Topology target: node `generator` (Generator; `site_evidenced` / `permitted`); edge `btm_terminal_to_gsu` (Generator → Generator step-up package; `teaching_reference` / `conceptual`)
  - Sources: [Solar Turbines — Titan 350 38 MW Gas Turbine Generator Set](https://www.solarturbines.com/en_US/solutions/case-studies/titan-350-38mw-gas-turbine-generator-set.html) (accessed 2026-08-25; Datasheet code DS350MW38PG/0522/EO.)
- **site voltage unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:generator_terminal_site_voltage_kv`
  - Basis: The manufacturer range does not identify the selected Titan 350 voltage at Abilene and does not establish the LM2500 package terminal voltage.
  - Scope: Exact configured generator terminal voltage at the Longhorn onsite plant
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-25
  - Topology target: node `generator` (Generator; `site_evidenced` / `permitted`); edge `btm_terminal_to_gsu` (Generator → Generator step-up package; `teaching_reference` / `conceptual`)
  - Sources: [Solar Turbines — Titan 350 38 MW Gas Turbine Generator Set](https://www.solarturbines.com/en_US/solutions/case-studies/titan-350-38mw-gas-turbine-generator-set.html) (accessed 2026-08-25; Datasheet code DS350MW38PG/0522/EO.), [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-25; Project reviewer dated 2025-01-21; section manager dated 2025-01-22.)
- **campus interface design — design reference.**
  - Binding: selected topology ownership
  - 34.5 kV
  - Fact: `abilene:campus_mv_reference_design_voltage_kv`
  - Basis: Review drawing 5MECH-00001-GA labels a Lancium 34.5 kV underground feed and 35 kV termination cabinets.
  - Scope: Longhorn generation collection / Lancium underground tie and review-design feeds associated with Buildings 1 and 2
  - Boundary: `design_not_as_built` / `review_design` / as of 2024-12-04
  - Topology target: node `gsu_transformer` (Generator step-up package; `teaching_reference` / `conceptual`); node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `btm_gsu_to_mv` (Generator step-up package → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **campus interface unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:campus_lpt_secondary_as_built_voltage_kv`
  - Basis: The available review drawing establishes a 34.5 kV Longhorn interface but does not establish the as-built campus LPT ratio or all-building MV voltage.
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Topology target: node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `btm_gsu_to_mv` (Generator step-up package → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **gsu function reference — product reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A generator step-up transformer raises generator-level voltage to a suitable higher network voltage.
  - Fact: `electrical_engineering:gsu_generator_to_network_voltage_function`
  - Basis: Hitachi Energy identifies the GSU as the link between a power station and the transmission network and states that it takes generator voltage to a suitable transmission-voltage level. No numerical value is imported.
  - Scope: Generic GSU function; no Abilene terminal voltage, target voltage, ratio, winding connection, or operating state
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Hitachi Energy — Generator Step-up Transformers (GSU)](https://www.hitachienergy.com/us/en/products-and-solutions/transformers/power-transformers/generator-step-up-transformers-gsu) (accessed 2026-08-27; Undated current manufacturer technical page.)
- **generator gsu protection reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Generator protection addresses internal electrical faults, system faults, and abnormal operating conditions.
  - Fact: `electrical_engineering:generator_protection_fault_scope`
  - Basis: IEEE C37.102-2023 defines this scope for applying generator-protection relays, including combustion-turbine generators.
  - Scope: Generic synchronous-generator protection scope; no Abilene relay scheme, device, zone, setting, or trip logic
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-06-28
  - Sources: [IEEE Standards Association — IEEE C37.102-2023, IEEE Guide for AC Generator Protection](https://standards.ieee.org/ieee/C37.102/7035/) (accessed 2026-08-27; Active standard; IEEE records ANSI approval on 2025-03-26.)
  - Power-transformer protection requires engineering of relays and other devices, including consideration of current-transformer behavior, fault clearing, and post-trip re-energization.
  - Fact: `electrical_engineering:transformer_protection_engineering_scope`
  - Basis: IEEE C37.91-2021 covers practical relay and device application, current transformers during system faults, fault clearing, and re-energization.
  - Scope: Generic power-transformer protection scope; no Abilene GSU protection design or settings
  - Boundary: `design_not_observed` / `design_reference` / as of 2021-06-29
  - Sources: [IEEE Standards Association — IEEE C37.91-2021, IEEE Guide for Protecting Power Transformers](https://standards.ieee.org/ieee/C37.91/5904/) (accessed 2026-08-27; Active standard.)
  - GSU protection functions and current-transformer-defined differential zones must be selected for the application; a reference one-line is not a universal protection design.
  - Fact: `electrical_engineering:gsu_protection_zone_application_specificity`
  - Basis: SEL states that the engineer must select functions appropriate to the application and shows that CT availability and location determine whether a differential zone can be bounded by circuit breakers.
  - Scope: Generic lesson from an SEL GSU protection example; not a design recommendation or Abilene protection boundary
  - Boundary: `design_not_observed` / `design_reference` / as of 2015-11-17
  - Sources: [Schweitzer Engineering Laboratories — An SEL Approach to Modifying Transformer Protection for Nuclear Stations](https://selinc.com/api/download/blt62cb31c4b2d7632d/?lang=en-us) (accessed 2026-08-27; SEL white paper LWP0017-01, Date Code 20151117.)
- **site generator configuration boundary — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:gsu_as_built_ratio_and_connection`
  - Basis: The public permit and general-arrangement records do not contain a construction-issued or as-built electrical one-line establishing these fields.
  - Scope: As-built ratio, winding connection, grounding, and campus-side target voltage of the generator step-up transformers at Longhorn
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-27; Regulatory review authorizes a ten-turbine model mix but does not establish which units were installed, commissioned, or operating.), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-27; The cited general-arrangement drawing is marked not for construction and establishes only a review-design 34.5 kV interface, not an as-built GSU ratio, connection, protection scheme, or operating state.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:generator_gsu_protection_as_built`
  - Basis: Neither the air-permit review nor the not-for-construction arrangement drawing discloses an as-built relay one-line, device schedule, zone boundary, or settings file.
  - Scope: Installed generator and GSU protection devices, CT-defined zones, settings, and trip logic at Longhorn
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-27; Regulatory review authorizes a ten-turbine model mix but does not establish which units were installed, commissioned, or operating.), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-27; The cited general-arrangement drawing is marked not for construction and establishes only a review-design 34.5 kV interface, not an as-built GSU ratio, connection, protection scheme, or operating state.)

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
  - Binding: selected topology ownership
  - AEP Abilene Northwest transmission line
  - Fact: `abilene:grid_initial_source_line`
  - Basis: Mortenson ties the initial work to the named AEP line.
  - Scope: Initial 138 kV Abilene grid path only
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Topology target: node `utility_source_138` (AEP Abilene Northwest source; `site_evidenced` / `energized`); edge `grid138_source_to_tie` (AEP Abilene Northwest source → 138 kV slack-span tie; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 138 kV
  - Fact: `abilene:grid_initial_substation_voltage_kv`
  - Basis: Mortenson identifies the original 200 MW substation as a 138 kV facility.
  - Scope: Initial Abilene grid path
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Topology target: node `initial_tie_138` (138 kV slack-span tie; `site_evidenced` / `energized`); node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`); edge `grid138_source_to_tie` (AEP Abilene Northwest source → 138 kV slack-span tie; `site_evidenced` / `energized`); edge `grid138_tie_to_station` (138 kV slack-span tie → Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 200 MW
  - Fact: `abilene:grid_initial_substation_capacity_mw`
  - Basis: Mortenson identifies the original substation phase as 200 MW.
  - Scope: Initial Abilene grid path
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Topology target: node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`); edge `grid138_tie_to_station` (138 kV slack-span tie → Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 300 ft
  - Fact: `abilene:grid_initial_slack_span_length_ft`
  - Basis: Mortenson reports a 300-foot slack span and AEP interconnection work.
  - Scope: Initial tie between the AEP Abilene Northwest line and the 138 kV substation
  - Boundary: `confirmed` / `constructed` / as of 2026-08-25
  - Topology target: node `initial_tie_138` (138 kV slack-span tie; `site_evidenced` / `energized`); edge `grid138_source_to_tie` (AEP Abilene Northwest source → 138 kV slack-span tie; `site_evidenced` / `energized`); edge `grid138_tie_to_station` (138 kV slack-span tie → Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 2026-08-25 (ISO-8601 date)
  - Fact: `abilene:grid_initial_service_operational_as_of`
  - Basis: Mortenson's current project page says the initial substation transitioned from de-energized construction into energized, operational service; it does not disclose the exact first-energization date.
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Topology target: node `utility_source_138` (AEP Abilene Northwest source; `site_evidenced` / `energized`); node `initial_tie_138` (138 kV slack-span tie; `site_evidenced` / `energized`); node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`); edge `grid138_source_to_tie` (AEP Abilene Northwest source → 138 kV slack-span tie; `site_evidenced` / `energized`); edge `grid138_tie_to_station` (138 kV slack-span tie → Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **downstream merge unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:campus_source_merge_as_built_topology`
  - Basis: The reviewed project-delivery page and Longhorn review drawing establish the separate source-side elements but do not establish a shared as-built campus bus, feeder arrangement, switching state, or merge topology.
  - Scope: As-built merge of the initial 138 kV, expansion 345 kV, and behind-the-meter generation paths at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Topology target: node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `grid138_station_to_mv` (Initial 200 MW / 138 kV station → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)

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
  - Binding: selected topology ownership
  - 345 kV
  - Fact: `abilene:grid_expansion_substation_voltage_kv`
  - Basis: Mortenson identifies the expansion as a 345 kV greenfield substation.
  - Scope: Separate greenfield Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `utility_source_345` (Unnamed 345 kV source; `site_evidenced` / `energized`); node `transmission_corridor_345` (345 kV expansion service; `site_evidenced` / `energized`); node `hv_protection_envelope_345` (Abstract 345 kV protection envelope; `site_evidenced` / `energized`); node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`); edge `grid345_source_to_corridor` (Unnamed 345 kV source → 345 kV expansion service; `site_evidenced` / `energized`); edge `grid345_corridor_to_hv` (345 kV expansion service → Abstract 345 kV protection envelope; `site_evidenced` / `energized`); edge `grid345_hv_to_lpt` (Abstract 345 kV protection envelope → 1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 1000 MW
  - Fact: `abilene:grid_expansion_substation_capacity_mw`
  - Basis: Mortenson identifies the expansion substation as 1 GW.
  - Scope: Separate greenfield Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 5 main power transformers
  - Fact: `abilene:grid_expansion_transformers_energized_count`
  - Basis: Mortenson reports all five main power transformers energized by 2026-03-10.
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`); edge `grid345_hv_to_lpt` (Abstract 345 kV protection envelope → 1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 2026-03-10 (ISO-8601 date)
  - Fact: `abilene:grid_expansion_fully_energized_by`
  - Basis: Mortenson reports the fifth and final main power transformer energized on 2026-03-10; three temporary transformers still had planned permanent swaps.
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `utility_source_345` (Unnamed 345 kV source; `site_evidenced` / `energized`); node `transmission_corridor_345` (345 kV expansion service; `site_evidenced` / `energized`); node `hv_protection_envelope_345` (Abstract 345 kV protection envelope; `site_evidenced` / `energized`); node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`); edge `grid345_source_to_corridor` (Unnamed 345 kV source → 345 kV expansion service; `site_evidenced` / `energized`); edge `grid345_corridor_to_hv` (345 kV expansion service → Abstract 345 kV protection envelope; `site_evidenced` / `energized`); edge `grid345_hv_to_lpt` (Abstract 345 kV protection envelope → 1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **upstream source unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene:grid_expansion_upstream_line`
  - Basis: Mortenson does not name the upstream 345 kV line; the AEP Abilene Northwest reference is scoped only to the initial 138 kV path.
  - Scope: Upstream source line for the separate 345 kV expansion substation
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **downstream merge unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:campus_source_merge_as_built_topology`
  - Basis: The reviewed project-delivery page and Longhorn review drawing establish the separate source-side elements but do not establish a shared as-built campus bus, feeder arrangement, switching state, or merge topology.
  - Scope: As-built merge of the initial 138 kV, expansion 345 kV, and behind-the-meter generation paths at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Topology target: node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `grid345_lpt_to_mv` (1 GW / 345 kV expansion substation → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)

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
  - Binding: segment-local, nonphysical teaching overlay
  - Constellation and Microsoft signed a 20-year power purchase agreement supporting the restart of Crane Clean Energy Center; Microsoft will buy energy from the renewed plant to help match the power its PJM data centers use with carbon-free energy. (named contract comparison)
  - Fact: `commercial_energy:crane_microsoft_ppa_contract`
  - Basis: Constellation's announcement identifies the parties, 20-year term, generating asset, PJM context, and matching objective.
  - Scope: Microsoft-Constellation Crane Clean Energy Center comparison case only; not the Abilene campus and not a dedicated physical delivery path.
  - Boundary: `confirmed_contract` / `contracted` / as of 2024-09-20
  - Sources: [Constellation Energy — Constellation to Launch Crane Clean Energy Center, Restoring Jobs and Carbon-Free Power to The Grid](https://www.constellationenergy.com/news/2024/Constellation-to-Launch-Crane-Clean-Energy-Center-Restoring-Jobs-and-Carbon-Free-Power-to-The-Grid.html) (accessed 2026-08-27; Constellation's dated release announces the signed agreement and describes the named generator, buyer, term, grid region, and intended matching use.)
- **contractual attributes are not physical flow — accounting reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Energy attribute instruments are separate from physical grid distribution; contractual relationships allocate generation attributes while consumers receive an untraceable grid mix. (accounting boundary)
  - Fact: `commercial_energy:scope2_contractual_attributes_not_physical_flow`
  - Basis: The Scope 2 Guidance distinguishes the location-based grid-average method from the market-based method derived from qualifying contractual instruments, and expressly separates attributes from physical distribution.
  - Scope: General Scope 2 accounting boundary for grid-distributed electricity; it does not determine any site's physical source path or contract eligibility.
  - Boundary: `authoritative_guidance` / `accounting_standard` / as of 2026-08-27
  - Sources: [Greenhouse Gas Protocol — Scope 2 Guidance](https://ghgprotocol.org/sites/default/files/2023-03/Scope%202%20Guidance.pdf) (accessed 2026-08-27; Current official download of the 2015 guidance, including corrections published through December 2022. A later revision remained in the public consultation process when this source was accessed.)

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
  - Binding: selected topology ownership
  - 34.5 kV
  - Fact: `abilene:campus_mv_reference_design_voltage_kv`
  - Basis: Review drawing 5MECH-00001-GA labels a Lancium 34.5 kV underground feed and 35 kV termination cabinets.
  - Scope: Longhorn generation collection / Lancium underground tie and review-design feeds associated with Buildings 1 and 2
  - Boundary: `design_not_as_built` / `review_design` / as of 2024-12-04
  - Topology target: node `gsu_transformer` (Generator step-up package; `teaching_reference` / `conceptual`); node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `btm_gsu_to_mv` (Generator step-up package → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **campus as built unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:campus_lpt_secondary_as_built_voltage_kv`
  - Basis: The available review drawing establishes a 34.5 kV Longhorn interface but does not establish the as-built campus LPT ratio or all-building MV voltage.
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Topology target: node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `btm_gsu_to_mv` (Generator step-up package → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **source merge unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:campus_source_merge_as_built_topology`
  - Basis: The reviewed project-delivery page and Longhorn review drawing establish the separate source-side elements but do not establish a shared as-built campus bus, feeder arrangement, switching state, or merge topology.
  - Scope: As-built merge of the initial 138 kV, expansion 345 kV, and behind-the-meter generation paths at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Topology target: node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `btm_gsu_to_mv` (Generator step-up package → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `grid138_station_to_mv` (Initial 200 MW / 138 kV station → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`); edge `grid345_lpt_to_mv` (1 GW / 345 kV expansion substation → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.), [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **bess future — future design.**
  - Binding: selected topology ownership
  - future (status)
  - Fact: `abilene:bess_reference_design_status`
  - Basis: Drawing 5MECH-00001-GA labels the BESS unit as FUTURE.
  - Scope: BESS shown on the Longhorn power-plant review drawing
  - Boundary: `future_design` / `future_design` / as of 2024-12-04
  - Topology target: node `bess_package` (BESS package; `site_evidenced` / `future_design`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **bess operation unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:bess_operational_status`
  - Basis: The review drawing does not establish procurement, installation, energization, or operation.
  - Scope: BESS at the original Abilene reference campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Topology target: node `bess_package` (BESS package; `site_evidenced` / `future_design`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **bess connection unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:bess_campus_connection_as_built_topology`
  - Basis: The Longhorn review drawing marks a BESS package as future but does not establish its procurement, installation, energization, or as-built campus connection.
  - Scope: As-built BESS connection at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Topology target: edge `bess_to_mv` (BESS package → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **diesel authorization — permitted.**
  - Binding: selected topology ownership
  - 62 units
  - Fact: `abilene:diesel_units_authorized`
  - Basis: The application engine-class maxima sum to 62 units; the technical review confirms 62 belly tanks and that this authorization is separate from gas generation registration 177263.
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-04-24
  - Topology target: node `diesel_backup_package` (Emergency diesel backup package; `site_evidenced` / `permitted`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056) (accessed 2026-08-25; Application supplies the complete engine-class counts and MW totals used to calculate 62 authorized units and 169.9 MW permitted nameplate.), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645) (accessed 2026-08-25; Project received 2025-04-11; reviewer and manager dated 2025-04-24.)
  - 169.9 MW
  - Fact: `abilene:diesel_permitted_nameplate_mw`
  - Basis: Application class totals are 9 + 9 + 12 + 6 + 7.5 + 48 + 78.4 MW, totaling 169.9 MW across the 62 authorized units.
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-04-24
  - Topology target: node `diesel_backup_package` (Emergency diesel backup package; `site_evidenced` / `permitted`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056) (accessed 2026-08-25; Application supplies the complete engine-class counts and MW totals used to calculate 62 authorized units and 169.9 MW permitted nameplate.), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645) (accessed 2026-08-25; Project received 2025-04-11; reviewer and manager dated 2025-04-24.)
- **diesel operation unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:diesel_units_installed`
  - Basis: The authorization and application do not establish the installed unit count.
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `unverified_null` / `installation_unknown` / as of 2026-08-25
  - Topology target: node `diesel_backup_package` (Emergency diesel backup package; `site_evidenced` / `permitted`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056) (accessed 2026-08-25; Application supplies the complete engine-class counts and MW totals used to calculate 62 authorized units and 169.9 MW permitted nameplate.), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645) (accessed 2026-08-25; Project received 2025-04-11; reviewer and manager dated 2025-04-24.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene:diesel_operational_units`
  - Basis: The authorization and application do not establish the operational unit count.
  - Scope: Longhorn data-center emergency and standby diesel system
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Topology target: node `diesel_backup_package` (Emergency diesel backup package; `site_evidenced` / `permitted`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056) (accessed 2026-08-25; Application supplies the complete engine-class counts and MW totals used to calculate 62 authorized units and 169.9 MW permitted nameplate.), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645) (accessed 2026-08-25; Project received 2025-04-11; reviewer and manager dated 2025-04-24.)
- **diesel connection unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:diesel_campus_connection_as_built_topology`
  - Basis: The permit application and technical review establish authorization but do not establish installation, operation, feeder allocation, switching state, or an as-built campus connection.
  - Scope: As-built connection of the authorized emergency and standby diesel system at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-25
  - Topology target: edge `diesel_to_mv` (Emergency diesel backup package → Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Data Center PBR Revision Application, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8814056) (accessed 2026-08-25; Application supplies the complete engine-class counts and MW totals used to calculate 62 authorized units and 169.9 MW permitted nameplate.), [Texas Commission on Environmental Quality — Permit by Rule Registration Technical Review, Registration 177262](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8811645) (accessed 2026-08-25; Project received 2025-04-11; reviewer and manager dated 2025-04-24.)

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
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:campus_lpt_secondary_as_built_voltage_kv`
  - Basis: The available review drawing establishes a 34.5 kV Longhorn interface but does not establish the as-built campus LPT ratio or all-building MV voltage.
  - Scope: As-built secondary voltage of the 345 kV campus substation across the original campus
  - Boundary: `unverified_null` / `as_built_unknown` / as of 2026-08-25
  - Topology target: node `campus_mv_distribution` (Abstract campus MV distribution envelope; `teaching_reference` / `conceptual`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.), [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **facility distribution product reference — product reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A unit substation coordinates primary switchgear, a transformer, and secondary distribution equipment as one system.
  - Fact: `electrical_engineering:unit_substation_coordinated_assembly_role`
  - Basis: Schneider Electric describes its unit substations as bringing together medium-voltage switchgear, transformers, and secondary switchgear or switchboards, with coordinated components designed to work as one system.
  - Scope: Schneider Electric unit-substation product architecture; not an Abilene equipment selection, voltage, rating, or topology
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Schneider Electric — Medium Voltage Unit Substations](https://www.se.com/us/en/product-range/60292-medium-voltage-unit-substations/) (accessed 2026-08-27; Undated current manufacturer product-range page.)
  - Low-voltage switchgear distributes power and protects, controls, and isolates downstream equipment and circuits.
  - Fact: `electrical_engineering:low_voltage_switchgear_distribution_protection_role`
  - Basis: Schneider Electric describes Power-Zone 4 as electrical-distribution and power-system-protection switchgear that protects, controls, and isolates downstream equipment and processes.
  - Scope: Schneider Electric Power-Zone 4 product function; not an Abilene switchgear selection, rating, lineup, or switch state
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Schneider Electric — Power-Zone 4 Low Voltage Drawout Switchgear](https://www.se.com/us/en/product-range/7288-powerzone-4/) (accessed 2026-08-27; Undated current manufacturer product-range page.)
  - Busway provides enclosed feeder and plug-in sections for facility power distribution.
  - Fact: `electrical_engineering:busway_feeder_and_plugin_distribution_role`
  - Basis: Schneider Electric documents I-Line feeder and plug-in busway lengths, fittings, and plug-in protective units for commercial and industrial power distribution.
  - Scope: Schneider Electric I-Line product-family function; not an Abilene route, conductor, rating, tap count, or redundancy path
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Schneider Electric — I-Line Busway](https://www.se.com/us/en/product-range/7550-iline-busway/) (accessed 2026-08-27; Undated current manufacturer product-range page.)
- **ups function reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A UPS protects critical loads with conditioned, no-break power.
  - Fact: `electrical_engineering:ups_conditioned_no_break_power_role`
  - Basis: Vertiv distinguishes the UPS role of conditioned no-break critical-load power from the site-level energy-management role of a conventional BESS.
  - Scope: Generic large-data-center UPS role; not an Abilene UPS topology, capacity, battery runtime, redundancy, or operating state
  - Boundary: `design_not_observed` / `design_reference` / as of 2026-06-26
  - Sources: [Vertiv — BESS and UPS roles in large data center power architectures](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) (accessed 2026-08-27; Manufacturer page is dated 2026-06-26.)
- **first phase electrical delivery — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - Essential electrical equipment and switchgear were manufactured in-house, and critical infrastructure was produced and deployed on site to support the first-phase construction schedule. (site execution milestone)
  - Fact: `abilene_execution:building_electrical_delivery_scope`
  - Basis: Crusoe's project-delivery release attributes the first-phase schedule to in-house manufacture of electrical equipment and switchgear and says the resulting critical infrastructure was deployed on site.
  - Scope: First-phase original Abilene campus equipment deployment; no claim about voltage class, product list, quantity, redundancy, topology, or state.
  - Boundary: `confirmed` / `constructed` / as of 2025-12-22
  - Sources: [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards) (accessed 2026-08-27; Company project-delivery account describing first-phase electrical equipment and switchgear deployment without publishing an as-built one-line, voltage schedule, redundancy scheme, or switching state.)
- **building power train configuration unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:building_power_train_as_built_configuration`
  - Basis: The company confirms deployment of electrical equipment and switchgear but publishes no as-built one-line, voltage schedule, equipment schedule, redundancy diagram, or operating switching state.
  - Scope: Site voltages, transformer and switchgear ratings, equipment quantities, redundancy paths, UPS topology, busway layout, and switch states between campus MV and the first-phase rack rows
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards) (accessed 2026-08-27; Company project-delivery account describing first-phase electrical equipment and switchgear deployment without publishing an as-built one-line, voltage schedule, redundancy scheme, or switching state.)

Red-line warnings:

- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Follow protected facility AC into the rack.

### 10. Rack AC becomes core voltage `s08_rack_voltage_descent`

- Opening question: Which voltages are site-evidenced, product-documented, or deliberately unknown?
- Teaching objective: Separate site AC, the documented rack DC bus, and the deliberately unspecified board-level core voltage.
- Visual focus: Busway, Rack power shelves, Voltage regulator module, GPU die
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `comparison`
- Title: Product voltage is not site configuration

1. Abilene rack-shelf AC input is unknown
   - Claim IDs: `rack_ac_unknown`
2. DGX GB200 product output is nominal 50–51 VDC
   - Claim IDs: `rack_dc_product_reference`
3. Exact operating rack and core electrical configuration is unknown
   - Claim IDs: `operating_rack_configuration_unknown`

Validated claim territory:

- **operating family — confirmed.**
  - Binding: selected topology ownership
  - NVIDIA GB200 (platform family)
  - Fact: `abilene:rack_platform`
  - Basis: Crusoe reports NVIDIA GB200 racks delivered in June 2025 and early workloads running; it does not identify an operating rack count.
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **design platform — design reference.**
  - Binding: selected topology ownership
  - NVIDIA GB200 NVL72 (platform design reference)
  - Fact: `abilene:rack_platform_nvl72_design_reference`
  - Basis: Crusoe's March expansion release says each building is designed to operate NVIDIA GB200 NVL72 systems; it does not establish installed quantity or the exact operating rack configuration.
  - Scope: Building-level design reference for the original Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `power_shelf` (Rack power shelves; `platform_evidenced` / `conceptual`); edge `busway_to_power_shelf` (Busway → Rack power shelves; `platform_evidenced` / `conceptual`); edge `power_shelf_to_vrm` (Rack power shelves → Voltage regulator module; `platform_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **rack dc product reference — product reference.**
  - Binding: selected topology ownership
  - 50-51 (VDC)
  - Fact: `abilene:rack_power_shelf_output_vdc`
  - Basis: NVIDIA specifies that DGX GB200 power shelves convert AC to nominal 50-51 VDC.
  - Scope: NVIDIA DGX GB200 rack power-shelf nominal DC busbar output
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `power_shelf` (Rack power shelves; `platform_evidenced` / `conceptual`); edge `power_shelf_to_vrm` (Rack power shelves → Voltage regulator module; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
- **rack ac unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:rack_power_shelf_ac_input_voltage_v`
  - Basis: NVIDIA specifies AC input but the cited sources do not establish Abilene's input voltage.
  - Scope: Site-specific AC input to DGX GB200 rack power shelves at Abilene
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-25
  - Topology target: node `power_shelf` (Rack power shelves; `platform_evidenced` / `conceptual`); edge `busway_to_power_shelf` (Busway → Rack power shelves; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
- **vrm power delivery reference — product reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Voltage regulator modules step down an intermediate-bus output to the voltage required by GPUs and other high-power processors.
  - Fact: `electrical_engineering:vrm_intermediate_bus_to_xpu_voltage_role`
  - Basis: Infineon states that intermediate-bus-converter output is stepped down through VRMs to meet the voltage needs of GPUs, TPUs, ASICs, and other accelerators.
  - Scope: Generic AI-server point-of-load architecture; not a GB200 board design, Abilene rack configuration, or numerical core voltage
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Infineon Technologies — Server rack power management](https://www.infineon.com/applications/ai-data-center/data-center-power-solutions/server-rack-power-management) (accessed 2026-08-27; Undated current manufacturer application page.)
  - Advanced processors require precise low-voltage, high-current power delivery.
  - Fact: `electrical_engineering:xpu_low_voltage_high_current_requirement`
  - Basis: Infineon characterizes modern XPU and ASIC power delivery as precise, low-voltage, and high-current, without supplying a universal rail value.
  - Scope: Generic XPU and ASIC power-delivery requirement; no processor-specific rail voltage or current
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Infineon Technologies — Server rack power management](https://www.infineon.com/applications/ai-data-center/data-center-power-solutions/server-rack-power-management) (accessed 2026-08-27; Undated current manufacturer application page.)
  - Multiphase DC-to-DC controllers and power stages provide scalable high-current processor-core power with fast transient response.
  - Fact: `electrical_engineering:multiphase_processor_core_power_role`
  - Basis: Texas Instruments documents multiphase DC-to-DC power for CPU, GPU, SoC, ASIC, and FPGA cores, with current sharing, scalable phase counts, and fast transient response.
  - Scope: Texas Instruments multiphase processor-core product architecture; not a selected GPU VRM or Abilene rack design
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-08-27
  - Sources: [Texas Instruments — Multiphase solutions: processor core power](https://www.ti.com/product-category/power-management/multiphase.html) (accessed 2026-08-27; Undated current manufacturer application page.)
- **first rack delivery — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2025-06 (ISO-8601 month)
  - Fact: `abilene_execution:gb200_first_rack_delivery_month`
  - Basis: Crusoe reports that Oracle began delivering the first NVIDIA GB200 racks in June 2025; the statement does not provide a rack count.
  - Scope: First NVIDIA GB200 rack deliveries to the original Abilene campus
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.)
- **operating rack configuration unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:operating_rack_configuration`
  - Basis: The live-campus release establishes first GB200 deliveries and live workloads but does not publish the installed or operating configuration.
  - Scope: Exact operating GB200 rack variant, rack count, populated trays, and power configuration at the original Abilene campus
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.), [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-27; Current model documentation supports the rack product boundary but does not disclose which supported AC input or exact board-level configuration the Abilene operator selected.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:rack_site_core_voltage`
  - Basis: NVIDIA documents the product boundary while the Abilene execution source does not identify the board operating point selected at the site. The rack-shelf AC-input boundary is recorded separately in the main ledger.
  - Scope: Exact board-level processor rail or core voltage for operating Abilene GB200 systems
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.), [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-27; Current model documentation supports the rack product boundary but does not disclose which supported AC input or exact board-level configuration the Abilene operator selected.)

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

Presenter-facing teaching focus:

- Kind: `sequence`
- Title: Electrical endpoint, thermal source

1. Core-voltage power terminates at the die
   - Claim IDs: `operating_family`, `electrical_input_to_cold_plate_reference`
2. Die heat enters the cold plate; no heat split is inferred
   - Claim IDs: `direct_cooling_design`, `liquid_path_product_reference`, `electrical_input_to_cold_plate_reference`

Validated claim territory:

- **operating family — confirmed.**
  - Binding: selected topology ownership
  - NVIDIA GB200 (platform family)
  - Fact: `abilene:rack_platform`
  - Basis: Crusoe reports NVIDIA GB200 racks delivered in June 2025 and early workloads running; it does not identify an operating rack count.
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **live workload boundary — live by.**
  - Binding: selected topology ownership
  - 2025-07-22 (ISO-8601 date)
  - Fact: `abilene:early_training_inference_live_by`
  - Basis: OpenAI reported on this date that parts of the facility were running and had recently begun early training and inference workloads.
  - Scope: Parts of the original Abilene campus
  - Boundary: `live_by_not_start_date` / `operating` / as of 2025-07-22
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [OpenAI — Stargate advances with partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-25; Reports parts of the Abilene facility running and recent early training and inference workloads; the exact workload start date is not supplied.)
- **direct cooling design — design reference.**
  - Binding: selected topology ownership
  - direct-to-chip liquid cooling (system design)
  - Fact: `abilene:cooling_direct_to_chip_design`
  - Basis: Crusoe's March expansion release says the campus will feature direct-to-chip liquid cooling in a zero-water-evaporation closed loop.
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); edge `die_to_cold_plate_heat` (GPU die → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **liquid path product reference — product reference.**
  - Binding: selected topology ownership
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Fact: `abilene:rack_liquid_cooled_components`
  - Basis: NVIDIA documents liquid flow through rack manifolds and cold plates attached to CPUs and GPUs in DGX GB compute trays.
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); edge `die_to_cold_plate_heat` (GPU die → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
- **electrical input to cold plate reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Most electrical power consumed by information-technology equipment becomes heat that cooling systems must remove
  - Fact: `thermal_engineering:generic_ite_electrical_input_heat`
  - Basis: PNNL states that the majority of electricity consumed by ITE is converted into heat and describes facility heat exchangers transferring that heat away from ITE into coolant loops.
  - Scope: Generic ITE energy balance at the equipment and facility boundary; not a per-die heat fraction, useful-compute fraction, or named-site load.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) (accessed 2026-08-27; PNNL-38817, prepared for the U.S. Department of Energy. The report states that its models are generic and require site-specific technical data before representing a real data center.)
  - A cold plate provides a conductive path from an electronic component to coolant flowing through internal channels
  - Fact: `thermal_engineering:generic_cold_plate_heat_transfer`
  - Basis: OCP defines cold plates as heat exchangers or heat sinks placed on electronics, with internal passages that transfer component heat by conduction to the cooling liquid.
  - Scope: Generic direct-liquid cold-plate function; not evidence of a selected or installed cold-plate design at a named site.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-10-09
  - Sources: [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) (accessed 2026-08-27; Current OCP-hosted requirements document; its revision history records revision 1.0 as first published on 2019-10-09.)

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
  - Binding: selected topology ownership
  - NVIDIA GB200 NVL72 (platform design reference)
  - Fact: `abilene:rack_platform_nvl72_design_reference`
  - Basis: Crusoe's March expansion release says each building is designed to operate NVIDIA GB200 NVL72 systems; it does not establish installed quantity or the exact operating rack configuration.
  - Scope: Building-level design reference for the original Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `rack_air_load` (Air-cooled rack auxiliaries; `platform_evidenced` / `conceptual`); node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
  - direct-to-chip liquid cooling (system design)
  - Fact: `abilene:cooling_direct_to_chip_design`
  - Basis: Crusoe's March expansion release says the campus will feature direct-to-chip liquid cooling in a zero-water-evaporation closed loop.
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `die_to_cold_plate_heat` (GPU die → Cold plate; `platform_evidenced` / `conceptual`); edge `cold_plate_to_manifold_return` (Cold plate → Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `manifold_to_cold_plate_supply` (Rack supply and return headers → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **rack component split — product reference.**
  - Binding: selected topology ownership
  - networking, storage, and other non-CPU/GPU rack components (component set)
  - Fact: `abilene:rack_air_cooled_components`
  - Basis: NVIDIA documents fan air cooling for networking, storage, and other rack components outside the liquid-cooled CPU and GPU path.
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `rack_air_load` (Air-cooled rack auxiliaries; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Fact: `abilene:rack_liquid_cooled_components`
  - Basis: NVIDIA documents liquid flow through rack manifolds and cold plates attached to CPUs and GPUs in DGX GB compute trays.
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `die_to_cold_plate_heat` (GPU die → Cold plate; `platform_evidenced` / `conceptual`); edge `cold_plate_to_manifold_return` (Cold plate → Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `manifold_to_cold_plate_supply` (Rack supply and return headers → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)

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
  - Binding: selected topology ownership
  - direct-to-chip liquid cooling (system design)
  - Fact: `abilene:cooling_direct_to_chip_design`
  - Basis: Crusoe's March expansion release says the campus will feature direct-to-chip liquid cooling in a zero-water-evaporation closed loop.
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `cold_plate_to_manifold_return` (Cold plate → Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `manifold_to_cold_plate_supply` (Rack supply and return headers → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **manifold product reference — product reference.**
  - Binding: selected topology ownership
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Fact: `abilene:rack_liquid_cooled_components`
  - Basis: NVIDIA documents liquid flow through rack manifolds and cold plates attached to CPUs and GPUs in DGX GB compute trays.
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `cold_plate_to_manifold_return` (Cold plate → Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `manifold_to_cold_plate_supply` (Rack supply and return headers → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
- **technology loop engineering reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Coolant supply flows from the CDU through the rack manifold to IT cold plates; after heat pickup, coolant return flows back through the manifold to the CDU (topology reference)
  - Fact: `thermal_engineering:generic_tcs_supply_return_path`
  - Basis: OCP defines the TCS as the loop from the CDU to the rack, through the manifold and IT equipment, and back through the manifold to the CDU; its cold-plate definition establishes component-to-coolant heat transfer.
  - Scope: Generic rack-manifold-distributed Technology Cooling System loop; no temperature, flow, coolant, pressure, or site topology is asserted.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-10-09
  - Sources: [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) (accessed 2026-08-27; Current OCP-hosted requirements document; its revision history records revision 1.0 as first published on 2019-10-09.)
  - A rack manifold distributes coolant from the CDU to IT equipment and back while meeting flow and pressure-drop requirements
  - Fact: `thermal_engineering:generic_rack_manifold_flow_role`
  - Basis: OCP requires the manifold to distribute cooling liquid to and from IT equipment, deliver the required flow at a targeted pressure drop, and provide uniform flow distribution within the rack.
  - Scope: Generic rack-manifold function and design parameters; not a flow rate, header arrangement, or control setting for a named system.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-10-09
  - Sources: [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) (accessed 2026-08-27; Current OCP-hosted requirements document; its revision history records revision 1.0 as first published on 2019-10-09.)
  - A liquid-to-liquid CDU uses sensors and controls to regulate coolant flow, pressure, and temperature across its TCS and FWS interfaces
  - Fact: `thermal_engineering:generic_cdu_control_functions`
  - Basis: OCP identifies flow, pressure, and temperature control as CDU functions and describes sensors and control devices regulating the TCS and FWS sides.
  - Scope: Generic liquid-to-liquid CDU control functions; no control mode, setpoint, sensor count, redundancy, or response is asserted for a named package.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) (accessed 2026-08-27; The document header is dated August 2024 and its version table records the revision 1.0 initial release on 2024-11-01.), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) (accessed 2026-08-27; Current OCP-hosted requirements document; its revision history records revision 1.0 as first published on 2019-10-09.)

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
  - Binding: selected topology ownership
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Fact: `abilene:cooling_heat_rejection_posture`
  - Basis: Crusoe describes a selected closed-loop, non-evaporative liquid-cooling system with air-cooled chillers and no water consumed in heat rejection.
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Topology target: node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **direct cooling design — design reference.**
  - Binding: selected topology ownership
  - direct-to-chip liquid cooling (system design)
  - Fact: `abilene:cooling_direct_to_chip_design`
  - Basis: Crusoe's March expansion release says the campus will feature direct-to-chip liquid cooling in a zero-water-evaporation closed loop.
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`); node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **cdu boundary engineering reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A liquid-to-liquid CDU isolates the Technology Cooling System from the Facility Water System and transfers heat between them through a heat exchanger (topology reference)
  - Fact: `thermal_engineering:generic_cdu_loop_isolation_heat_exchange`
  - Basis: OCP describes the CDU as isolating the IT-side flow network from the facility loop, with heat transfer through a heat exchanger between the heated TCS liquid and the facility-side liquid loop.
  - Scope: Generic liquid-to-liquid CDU boundary; it does not assert coolant mixing, a particular exchanger, or a named-site package design.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) (accessed 2026-08-27; The document header is dated August 2024 and its version table records the revision 1.0 initial release on 2024-11-01.), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) (accessed 2026-08-27; Current OCP-hosted requirements document; its revision history records revision 1.0 as first published on 2019-10-09.)
  - A liquid-to-liquid CDU uses sensors and controls to regulate coolant flow, pressure, and temperature across its TCS and FWS interfaces
  - Fact: `thermal_engineering:generic_cdu_control_functions`
  - Basis: OCP identifies flow, pressure, and temperature control as CDU functions and describes sensors and control devices regulating the TCS and FWS sides.
  - Scope: Generic liquid-to-liquid CDU control functions; no control mode, setpoint, sensor count, redundancy, or response is asserted for a named package.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) (accessed 2026-08-27; The document header is dated August 2024 and its version table records the revision 1.0 initial release on 2024-11-01.), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) (accessed 2026-08-27; Current OCP-hosted requirements document; its revision history records revision 1.0 as first published on 2019-10-09.)
- **cdu site configuration unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:cdu_site_configuration`
  - Basis: The project-specific cooling source describes the facility loop and air-cooled heat rejection but does not name CDUs or disclose their configuration.
  - Scope: Site CDU presence by rack or row, package selection, temperature and flow setpoints, heat-exchanger interface, quantity, and redundancy
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)

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
  - Binding: selected topology ownership
  - networking, storage, and other non-CPU/GPU rack components (component set)
  - Fact: `abilene:rack_air_cooled_components`
  - Basis: NVIDIA documents fan air cooling for networking, storage, and other rack components outside the liquid-cooled CPU and GPU path.
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `rack_air_load` (Air-cooled rack auxiliaries; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
- **selected facility loop — selected design.**
  - Binding: selected topology ownership
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Fact: `abilene:cooling_heat_rejection_posture`
  - Basis: Crusoe describes a selected closed-loop, non-evaporative liquid-cooling system with air-cooled chillers and no water consumed in heat rejection.
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Topology target: node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **parallel air path engineering reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Direct-liquid cooling of IT equipment can coexist with CRAHs that cool the computer-room air (topology reference)
  - Fact: `thermal_engineering:generic_parallel_liquid_air_cooling`
  - Basis: DOE identifies system variants in which CRAHs connected to chilled-water systems cool room air while CDUs cool IT equipment directly.
  - Scope: Generic hybrid data-center cooling arrangement; not evidence that a particular air and liquid branch is installed or operated at Abilene.
  - Boundary: `design_not_observed` / `design_reference` / as of 2019-01-09
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers) (accessed 2026-08-27; Current DOE guidance page with simplified schematics for air-cooled and direct-liquid-cooled data-center heat-removal paths.)
  - Warm IT exhaust air returns to an air handler, where a heat exchanger transfers heat into a coolant loop and conditioned air is supplied back to the data hall (topology reference)
  - Fact: `thermal_engineering:generic_crah_air_heat_removal_path`
  - Basis: DOE describes warm IT air returning to cooling equipment and PNNL describes CRAHs regulating data-hall air while facility heat exchangers transfer ITE heat into coolant loops that pass through outdoor chillers.
  - Scope: Generic CRAH or central-air-handler heat-removal path; not a named-site air path, coil selection, airflow, temperature, humidity, or package count.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers) (accessed 2026-08-27; Current DOE guidance page with simplified schematics for air-cooled and direct-liquid-cooled data-center heat-removal paths.), [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) (accessed 2026-08-27; PNNL-38817, prepared for the U.S. Department of Energy. The report states that its models are generic and require site-specific technical data before representing a real data center.)
  - CRAH airflow can be varied with cooling load and coordinated against common environmental conditions
  - Fact: `thermal_engineering:generic_crah_variable_airflow_control`
  - Basis: DOE recommends variable-speed drives to vary CRAH airflow as cooling load changes and coordinated operation of units serving the same environment.
  - Scope: Generic air-handler control principle; no site setpoint, fan curve, sensor location, or control sequence is asserted.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) (accessed 2026-08-27; Revised July 2024; prepared by NREL authors for DOE FEMP.)
- **residual air site configuration unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:residual_air_site_configuration`
  - Basis: The company describes mixed high-performance cooling and the FWS but does not identify site CRAHs, fan walls, or the as-built residual-air path.
  - Scope: First-phase residual-air path, CRAH or fan-wall selection, package count, airflow direction, redundancy, and facility-loop connection
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.), [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards) (accessed 2026-08-27; Company project-delivery account describing first-phase electrical equipment and switchgear deployment without publishing an as-built one-line, voltage schedule, redundancy scheme, or switching state.)

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
  - Binding: selected topology ownership
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Fact: `abilene:cooling_heat_rejection_posture`
  - Basis: Crusoe describes a selected closed-loop, non-evaporative liquid-cooling system with air-cooled chillers and no water consumed in heat rejection.
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Topology target: node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`); node `air_cooled_chiller` (Air-cooled chiller and condenser; `site_evidenced` / `conceptual`); edge `facility_to_chiller_return` (Closed facility water loop → Air-cooled chiller and condenser; `site_evidenced` / `conceptual`); edge `chiller_to_facility_supply` (Air-cooled chiller and condenser → Closed facility water loop; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **direct cooling design — design reference.**
  - Binding: selected topology ownership
  - direct-to-chip liquid cooling (system design)
  - Fact: `abilene:cooling_direct_to_chip_design`
  - Basis: Crusoe's March expansion release says the campus will feature direct-to-chip liquid cooling in a zero-water-evaporation closed loop.
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **facility loop engineering reference — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Facility coolant loops receive ITE heat through equipment heat exchangers and carry it to plant heat-rejection equipment (topology reference)
  - Fact: `thermal_engineering:generic_facility_loop_heat_transport`
  - Basis: PNNL describes facility heat exchangers transferring heat from ITE into coolant loops that flow through outdoor chillers, while DOE shows heat moving through successive liquid loops to heat-rejection equipment.
  - Scope: Generic facility-loop role; the heat-rejection equipment may vary and no Abilene CDU, CRAH, chiller interface, or operating topology is asserted.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) (accessed 2026-08-27; PNNL-38817, prepared for the U.S. Department of Energy. The report states that its models are generic and require site-specific technical data before representing a real data center.), [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers) (accessed 2026-08-27; Current DOE guidance page with simplified schematics for air-cooled and direct-liquid-cooled data-center heat-removal paths.)
  - Facility cooling control may vary pump flow, differential pressure, and supply-water temperature with load while maintaining required cooling capacity
  - Fact: `thermal_engineering:generic_facility_loop_load_control`
  - Basis: DOE recommends variable-flow pumping, differential-pressure setpoint reset, variable-speed equipment, and supply-temperature control under changing IT loads and ambient conditions while preserving necessary cooling capacity.
  - Scope: Generic chilled-water and facility-loop control options; not an Abilene control sequence, operating setpoint, equipment selection, or measured state.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) (accessed 2026-08-27; Revised July 2024; prepared by NREL authors for DOE FEMP.)
  - A liquid-to-liquid CDU isolates the Technology Cooling System from the Facility Water System and transfers heat between them through a heat exchanger (topology reference)
  - Fact: `thermal_engineering:generic_cdu_loop_isolation_heat_exchange`
  - Basis: OCP describes the CDU as isolating the IT-side flow network from the facility loop, with heat transfer through a heat exchanger between the heated TCS liquid and the facility-side liquid loop.
  - Scope: Generic liquid-to-liquid CDU boundary; it does not assert coolant mixing, a particular exchanger, or a named-site package design.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-11-01
  - Sources: [Open Compute Project Foundation — Liquid to Liquid CDU Test Methodology and Performance Rating, Revision 1.0](https://www.opencompute.org/documents/ocp-wp-l-lcdu-test-methodology-performance-rating-r1-pdf) (accessed 2026-08-27; The document header is dated August 2024 and its version table records the revision 1.0 initial release on 2024-11-01.), [Open Compute Project Foundation — Open Compute Project Liquid Cooling Cold Plate Requirements Document](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf) (accessed 2026-08-27; Current OCP-hosted requirements document; its revision history records revision 1.0 as first published on 2019-10-09.)
  - Warm IT exhaust air returns to an air handler, where a heat exchanger transfers heat into a coolant loop and conditioned air is supplied back to the data hall (topology reference)
  - Fact: `thermal_engineering:generic_crah_air_heat_removal_path`
  - Basis: DOE describes warm IT air returning to cooling equipment and PNNL describes CRAHs regulating data-hall air while facility heat exchangers transfer ITE heat into coolant loops that pass through outdoor chillers.
  - Scope: Generic CRAH or central-air-handler heat-removal path; not a named-site air path, coil selection, airflow, temperature, humidity, or package count.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [U.S. Department of Energy Federal Energy Management Program — Cooling Water Efficiency Opportunities for Federal Data Centers](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers) (accessed 2026-08-27; Current DOE guidance page with simplified schematics for air-cooled and direct-liquid-cooled data-center heat-removal paths.), [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) (accessed 2026-08-27; PNNL-38817, prepared for the U.S. Department of Energy. The report states that its models are generic and require site-specific technical data before representing a real data center.)
- **site facility cooling design — selected design.**
  - Binding: segment-local, nonphysical teaching overlay
  - A true closed-loop Facility Cooling Water System continuously recirculates water and rejects heat through air-cooled chillers. (selected facility-cooling design)
  - Fact: `abilene_execution:facility_cooling_water_system_design`
  - Basis: Crusoe explicitly names the FWS, describes it as a true closed loop, and states that its heat is rejected through air-cooled chillers.
  - Scope: Original eight-building Abilene campus design selection; no CDU, CRAH, temperature, flow, redundancy, quantity, or operating-measurement claim.
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)
  - air-cooled chillers (selected heat-rejection equipment family)
  - Fact: `abilene_execution:facility_heat_rejection_terminal`
  - Basis: Crusoe says the closed-loop facility water rejects heat through air-cooled chillers and does not use water in the heat-rejection process.
  - Scope: Terminal heat-rejection family for the original Abilene FWS; no chiller model, count, capacity, setpoint, or observed operating state.
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)
- **facility cooling interfaces unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:facility_cooling_interfaces_as_built`
  - Basis: The public project source establishes the selected facility-loop and heat-rejection family but does not publish a process-flow diagram or as-built package-interface schedule.
  - Scope: As-built interfaces among rack manifolds, CDUs, residual-air equipment, the FWS, pumps, and air-cooled chillers at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:facility_cooling_operating_measurements`
  - Basis: The source publishes design and anticipated maintenance facts, not telemetry, commissioning readings, package capacities, or current operating measurements.
  - Scope: Current measured operating values for first-phase Abilene cooling loops and heat-rejection equipment
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Resolve why a non-evaporative design still has a water requirement.

### 17. Closed loop does not mean water-free `s15_water_accounting`

- Opening question: What is designed or anticipated here, and what measured consumption remains unknown?
- Teaching objective: Separate design fill and anticipated maintenance from measured operating consumption.
- Visual focus: Initial fill and water treatment, Closed facility water loop, Air-cooled chiller and condenser
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `comparison`
- Title: Design requirement is not measured consumption

1. Initial-fill design is about 1,000,000 gallons per building
   - Claim IDs: `initial_fill_design`
2. Anticipated maintenance is about 50,000 gallons per building per year
   - Claim IDs: `anticipated_maintenance`
3. Measured operating consumption remains unknown
   - Claim IDs: `measured_operating_consumption_unknown`

Validated claim territory:

- **initial fill design — selected design.**
  - Binding: selected topology ownership
  - 1000000 gallons per building
  - Fact: `abilene:cooling_initial_fill_gallons_per_building`
  - Basis: Crusoe reports a design requirement of approximately one million gallons per building.
  - Scope: Design requirement for one building's closed-loop cooling-system initial fill
  - Boundary: `design_selected` / `design_requirement` / as of 2025-08-05
  - Topology target: node `fill_treatment` (Initial fill and water treatment; `site_evidenced` / `conceptual`); edge `fill_to_facility_loop` (Initial fill and water treatment → Closed facility water loop; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **anticipated maintenance — anticipated.**
  - Binding: selected topology ownership
  - 50000 gallons per building per year
  - Fact: `abilene:cooling_annual_maintenance_gallons_per_building`
  - Basis: Crusoe anticipates approximately 50,000 gallons per building per year for maintenance.
  - Scope: Anticipated annual cooling-system maintenance water for each building
  - Boundary: `anticipated_not_observed` / `anticipated_maintenance` / as of 2025-08-05
  - Topology target: node `fill_treatment` (Initial fill and water treatment; `site_evidenced` / `conceptual`); edge `fill_to_facility_loop` (Initial fill and water treatment → Closed facility water loop; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **measured operating consumption unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene:cooling_measured_operating_consumption_gallons`
  - Basis: The cited engineering article reports design fill and anticipated annual maintenance water, not a measured operating-consumption value.
  - Scope: Measured operating water consumption for the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **anticipated to measured.** An anticipated value is not a measured operating result.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Replay the complete return path to its terminal sink.

### 18. The figure-eight closes in the atmosphere `s16_close_atmosphere`

- Opening question: Where is the watt now?
- Teaching objective: Replay every reference heat-transfer gate to the terminal sink without implying an as-built path or physical recirculation.
- Visual focus: GPU die, Air-cooled rack auxiliaries, Cold plate, Rack supply and return headers, Coolant distribution unit, CRAH / fan-wall branch, Closed facility water loop, Air-cooled chiller and condenser, Atmosphere
- Visual state: focused 3D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `parallel`
- Title: Parallel rack paths converge at the facility loop

1. Rack heat splits into direct-to-chip liquid and residual-air paths
   - Claim IDs: `cooling_design`, `rack_component_paths`
2. Liquid path crosses the conceptual CDU interface
   - Claim IDs: `rack_component_paths`, `facility_interface_boundary`
3. Residual-air path crosses the conceptual CRAH interface
   - Claim IDs: `rack_component_paths`, `facility_interface_boundary`
4. Both paths feed the selected-design facility loop, air-cooled plant, and atmosphere
   - Claim IDs: `selected_heat_rejection`, `facility_interface_boundary`

Validated claim territory:

- **operating family — confirmed.**
  - Binding: selected topology ownership
  - NVIDIA GB200 (platform family)
  - Fact: `abilene:rack_platform`
  - Basis: Crusoe reports NVIDIA GB200 racks delivered in June 2025 and early workloads running; it does not identify an operating rack count.
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **cooling design — design reference.**
  - Binding: selected topology ownership
  - direct-to-chip liquid cooling (system design)
  - Fact: `abilene:cooling_direct_to_chip_design`
  - Basis: Crusoe's March expansion release says the campus will feature direct-to-chip liquid cooling in a zero-water-evaporation closed loop.
  - Scope: Design reference for the original eight-building Abilene campus
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-03-18
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`); node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`); edge `die_to_cold_plate_heat` (GPU die → Cold plate; `platform_evidenced` / `conceptual`); edge `cold_plate_to_manifold_return` (Cold plate → Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `manifold_to_cold_plate_supply` (Rack supply and return headers → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **rack component paths — product reference.**
  - Binding: selected topology ownership
  - networking, storage, and other non-CPU/GPU rack components (component set)
  - Fact: `abilene:rack_air_cooled_components`
  - Basis: NVIDIA documents fan air cooling for networking, storage, and other rack components outside the liquid-cooled CPU and GPU path.
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `rack_air_load` (Air-cooled rack auxiliaries; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
  - CPU and GPU cold plates connected through rack liquid-cooling manifolds (component path)
  - Fact: `abilene:rack_liquid_cooled_components`
  - Basis: NVIDIA documents liquid flow through rack manifolds and cold plates attached to CPUs and GPUs in DGX GB compute trays.
  - Scope: NVIDIA DGX GB rack product documentation, not an Abilene as-built observation
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `cold_plate` (Cold plate; `platform_evidenced` / `conceptual`); node `rack_manifold` (Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `die_to_cold_plate_heat` (GPU die → Cold plate; `platform_evidenced` / `conceptual`); edge `cold_plate_to_manifold_return` (Cold plate → Rack supply and return headers; `platform_evidenced` / `conceptual`); edge `manifold_to_cold_plate_supply` (Rack supply and return headers → Cold plate; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
- **selected heat rejection — selected design.**
  - Binding: selected topology ownership
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Fact: `abilene:cooling_heat_rejection_posture`
  - Basis: Crusoe describes a selected closed-loop, non-evaporative liquid-cooling system with air-cooled chillers and no water consumed in heat rejection.
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Topology target: node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`); node `air_cooled_chiller` (Air-cooled chiller and condenser; `site_evidenced` / `conceptual`); edge `facility_to_chiller_return` (Closed facility water loop → Air-cooled chiller and condenser; `site_evidenced` / `conceptual`); edge `chiller_to_facility_supply` (Air-cooled chiller and condenser → Closed facility water loop; `site_evidenced` / `conceptual`); edge `chiller_to_atmosphere` (Air-cooled chiller and condenser → Atmosphere; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **facility interface boundary — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:facility_cooling_interfaces_as_built`
  - Basis: The public project source establishes the selected facility-loop and heat-rejection family but does not publish a process-flow diagram or as-built package-interface schedule.
  - Scope: As-built interfaces among rack manifolds, CDUs, residual-air equipment, the FWS, pumps, and air-cooled chillers at the original campus
  - Boundary: `unverified_null` / `topology_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:cdu_site_configuration`
  - Basis: The project-specific cooling source describes the facility loop and air-cooled heat rejection but does not name CDUs or disclose their configuration.
  - Scope: Site CDU presence by rack or row, package selection, temperature and flow setpoints, heat-exchanger interface, quantity, and redundancy
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:residual_air_site_configuration`
  - Basis: The company describes mixed high-performance cooling and the FWS but does not identify site CRAHs, fan walls, or the as-built residual-air path.
  - Scope: First-phase residual-air path, CRAH or fan-wall selection, package count, airflow direction, redundancy, and facility-loop connection
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-27; Project-specific company account of installed gas turbines and the selected facility-cooling-water and heat-rejection design.), [Crusoe — Crusoe Wins North American Data Center Project of the Year at 2025 Data Center Dynamics Global Awards](https://www.crusoe.ai/resources/newsroom/crusoe-wins-north-american-data-center-project-of-the-year-at-2025-data-center-dynamics-global-awards) (accessed 2026-08-27; Company project-delivery account describing first-phase electrical equipment and switchgear deployment without publishing an as-built one-line, voltage schedule, redundancy scheme, or switching state.)

Red-line warnings:

- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Zoom out from the thermal-return subsystem, then switch to the grid-interconnection schedule.

## Act 5: Chokepoint reread

Identify how interconnection, equipment, commissioning, and load dynamics prevent announced capacity from becoming usable compute.

### 19. Planned capacity becomes a utility delivery schedule `s17_interconnection_schedule`

- Opening question: Which utility construction, energization, and equipment gates stand between planned capacity and service?
- Teaching objective: Separate dated administrative, energization, and planned permanent-equipment gates.
- Visual focus: AEP Abilene Northwest source, 138 kV slack-span tie, Initial 200 MW / 138 kV station, Unnamed 345 kV source, 345 kV expansion service, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `sequence`
- Title: Distinct interconnection gates

1. PLANNED — 1.2 GW grid-interconnection boundary
   - Claim IDs: `planned_grid_boundary`
2. CONFIRMED — initial utility gates energized 2023-06-30
   - Claim IDs: `initial_aep_delivery_gates`
3. REPORTED — line schedule 2025-05-12→2025-11-21; completion/energization unestablished
   - Claim IDs: `expansion_line_schedule`
4. PLANNED — permanent-transformer swaps expected by 2026-10-31
   - Claim IDs: `expansion_permanent_transformer_schedule`
5. UNKNOWN — customer queue/service agreement/capacity/load-ramp administrative record
   - Claim IDs: `private_interconnection_and_load_boundary`

Validated claim territory:

- **planned grid boundary — planned.**
  - Binding: segment-local, nonphysical teaching overlay
  - 1200 MW
  - Fact: `abilene:planned_grid_interconnection_mw`
  - Basis: Crusoe explicitly describes 1.2 GW as the site's grid interconnection.
  - Scope: Original eight-building Abilene campus grid interconnection
  - Boundary: `planned_not_operational` / `planned` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **evidenced service milestones — confirmed.**
  - Binding: selected topology ownership
  - 2026-08-25 (ISO-8601 date)
  - Fact: `abilene:grid_initial_service_operational_as_of`
  - Basis: Mortenson's current project page says the initial substation transitioned from de-energized construction into energized, operational service; it does not disclose the exact first-energization date.
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Topology target: node `utility_source_138` (AEP Abilene Northwest source; `site_evidenced` / `energized`); node `initial_tie_138` (138 kV slack-span tie; `site_evidenced` / `energized`); node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`); edge `grid138_source_to_tie` (AEP Abilene Northwest source → 138 kV slack-span tie; `site_evidenced` / `energized`); edge `grid138_tie_to_station` (138 kV slack-span tie → Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 2026-03-10 (ISO-8601 date)
  - Fact: `abilene:grid_expansion_fully_energized_by`
  - Basis: Mortenson reports the fifth and final main power transformer energized on 2026-03-10; three temporary transformers still had planned permanent swaps.
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `utility_source_345` (Unnamed 345 kV source; `site_evidenced` / `energized`); node `transmission_corridor_345` (345 kV expansion service; `site_evidenced` / `energized`); node `hv_protection_envelope_345` (Abstract 345 kV protection envelope; `site_evidenced` / `energized`); node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`); edge `grid345_source_to_corridor` (Unnamed 345 kV source → 345 kV expansion service; `site_evidenced` / `energized`); edge `grid345_corridor_to_hv` (345 kV expansion service → Abstract 345 kV protection envelope; `site_evidenced` / `energized`); edge `grid345_hv_to_lpt` (Abstract 345 kV protection envelope → 1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **initial aep delivery gates — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - One 138 kV minimum 2000 A, 40 kA breaker; switches; SCADA; Lancium-terminal metering; power-quality metering; telecom equipment; and an overhead exit to a dead-end structure. (utility interconnection project scope)
  - Fact: `abilene_execution:initial_aep_terminal_equipment_scope`
  - Basis: AEP's filed September 2023 construction report lists the equipment scope, project identifier, 2023-06-30 completion and energization, and 99 percent completion in the report.
  - Scope: AEP project T10433134 at Abilene Northwest station for the initial Lancium 138 kV path; not the customer-side campus substation or downstream bus.
  - Boundary: `confirmed` / `energized` / as of 2023-09-24
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF) (accessed 2026-08-27; Utility filing identifies the initial 138 kV terminal and point-of- interconnect projects, their equipment scope, project IDs, construction dates, and 2023-06-30 energization date.)
  - 2023-06-30 (ISO-8601 date)
  - Fact: `abilene_execution:initial_aep_terminal_energized_date`
  - Basis: AEP's filed construction report records both construction completion and energization on 2023-06-30.
  - Scope: AEP project T10433134 at Abilene Northwest 138 kV station
  - Boundary: `confirmed` / `energized` / as of 2023-06-30
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF) (accessed 2026-08-27; Utility filing identifies the initial 138 kV terminal and point-of- interconnect projects, their equipment scope, project IDs, construction dates, and 2023-06-30 energization date.)
  - An underground dead-end point of interconnect between Abilene Northwest 138 kV station and Lancium's 138 kV station for a 200 MW data center. (utility interconnection project scope)
  - Fact: `abilene_execution:initial_aep_poi_scope`
  - Basis: AEP's filed September 2023 construction report supplies the project name, purpose, 0.30-mile circuit field, completion, and energization record.
  - Scope: AEP project T10434308 for the initial grid path; it does not establish the downstream data-center load, campus merge, or present load level.
  - Boundary: `confirmed` / `energized` / as of 2023-09-24
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF) (accessed 2026-08-27; Utility filing identifies the initial 138 kV terminal and point-of- interconnect projects, their equipment scope, project IDs, construction dates, and 2023-06-30 energization date.)
  - 2023-06-30 (ISO-8601 date)
  - Fact: `abilene_execution:initial_aep_poi_energized_date`
  - Basis: AEP's filed construction report records both construction completion and energization on 2023-06-30.
  - Scope: AEP project T10434308, Abilene Northwest-Lancium 138 kV tie line
  - Boundary: `confirmed` / `energized` / as of 2023-06-30
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF) (accessed 2026-08-27; Utility filing identifies the initial 138 kV terminal and point-of- interconnect projects, their equipment scope, project IDs, construction dates, and 2023-06-30 energization date.)
- **expansion line schedule — planned.**
  - Binding: segment-local, nonphysical teaching overlay
  - A 2.40-mile 345 kV transmission-line project from Mulberry Creek 345 kV Station to the Lancium 345 kV point of interconnect. (named utility construction project)
  - Fact: `abilene_execution:expansion_345_named_line_project`
  - Basis: AEP's July 2025 filing names the project and POI, gives its physical scope, and reports two percent completion with the energization field blank.
  - Scope: AEP project T10703126 in the July 2025 report; a named upstream project, not proof that this exact line was later completed or energized.
  - Boundary: `planned_not_operational` / `planned` / as of 2025-07-03
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF) (accessed 2026-08-27; Utility filing names the 2.40-mile Mulberry Creek-Lancium 345 kV line project and POI, records it as two percent complete, and leaves its energization field blank. It is evidence of a construction project, not proof of the later as-built operating source.)
  - 2025-05-12 (ISO-8601 date)
  - Fact: `abilene_execution:expansion_345_line_start_date_as_reported`
  - Basis: The AEP filing's combined estimated-or-actual start-date column records 2025-05-12 and the same row reports two percent completion.
  - Scope: Start-date field for AEP project T10703126 in the July 2025 construction report; the report does not label the field separately as estimated or actual.
  - Boundary: `planned_not_operational` / `planned` / as of 2025-07-03
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF) (accessed 2026-08-27; Utility filing names the 2.40-mile Mulberry Creek-Lancium 345 kV line project and POI, records it as two percent complete, and leaves its energization field blank. It is evidence of a construction project, not proof of the later as-built operating source.)
  - 2025-11-21 (ISO-8601 date)
  - Fact: `abilene_execution:expansion_345_line_finish_date_as_reported`
  - Basis: AEP's filing records 2025-11-21 in the finish-date column while reporting two percent completion and no energization date.
  - Scope: Planned construction-complete field for AEP project T10703126 as of the July 2025 report; not an actual completion or energization date.
  - Boundary: `planned_not_operational` / `planned` / as of 2025-07-03
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF) (accessed 2026-08-27; Utility filing names the 2.40-mile Mulberry Creek-Lancium 345 kV line project and POI, records it as two percent complete, and leaves its energization field blank. It is evidence of a construction project, not proof of the later as-built operating source.)
- **expansion permanent transformer schedule — planned.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2026-10-31 (ISO-8601 month-end bound)
  - Fact: `abilene_execution:expansion_permanent_transformer_swaps_expected_by`
  - Basis: Mortenson's current page says three temporary units were being swapped and all three swapovers were expected by October 2026; this is not a completed milestone.
  - Scope: Planned replacement of three temporary expansion-substation transformers with permanent units
  - Boundary: `planned_not_operational` / `planned` / as of 2026-08-27
  - Sources: [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-27; Undated current EPC-contractor page reporting grid construction and energization milestones through 2026-03-10 plus a then-current October 2026 permanent-transformer swap target.)
- **private interconnection and load boundary — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:site_specific_interconnection_queue_and_contract_record`
  - Basis: AEP and Mortenson disclose physical project execution, while ERCOT states that public large-load status reporting is aggregated because customer information is confidential. The reviewed public records do not supply a customer-specific queue or contract chronology.
  - Scope: Customer-specific queue identifier, study dates, application milestones, executed service agreement, contracted capacity, and load-ramp schedule for the original Abilene campus
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF) (accessed 2026-08-27; Utility filing identifies the initial 138 kV terminal and point-of- interconnect projects, their equipment scope, project IDs, construction dates, and 2023-06-30 energization date.), [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF) (accessed 2026-08-27; Utility filing names the 2.40-mile Mulberry Creek-Lancium 345 kV line project and POI, records it as two percent complete, and leaves its energization field blank. It is evidence of a construction project, not proof of the later as-built operating source.), [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-27; Undated current EPC-contractor page reporting grid construction and energization milestones through 2026-03-10 plus a then-current October 2026 permanent-transformer swap target.), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267) (accessed 2026-08-27; ERCOT records final PUCT approval on 2025-07-31 and explains that customer-owned large-load information is confidential, so the public large-load status report is aggregated rather than customer-specific.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:contracted_grid_service_capacity_mw`
  - Basis: Public utility construction records provide project purposes and equipment ratings, not the customer's confidential executed service quantity or current contract ramp.
  - Scope: Contracted grid-service capacity for the original Abilene campus, separate from substation ratings and the planned 1.2 GW interconnection
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Construction Progress Report, September 2023, Project No. 54468](https://interchange.puc.texas.gov/Documents/54468_276_1332252.PDF) (accessed 2026-08-27; Utility filing identifies the initial 138 kV terminal and point-of- interconnect projects, their equipment scope, project IDs, construction dates, and 2023-06-30 energization date.), [AEP Texas, filed with the Public Utility Commission of Texas — AEP Texas North Division Interim Construction Progress Report, July 2025, Project No. 57477](https://interchange.puc.texas.gov/Documents/57477_194_1516744.PDF) (accessed 2026-08-27; Utility filing names the 2.40-mile Mulberry Creek-Lancium 345 kV line project and POI, records it as two percent complete, and leaves its energization field blank. It is evidence of a construction project, not proof of the later as-built operating source.), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267) (accessed 2026-08-27; ERCOT records final PUCT approval on 2025-07-31 and explains that customer-owned large-load information is confidential, so the public large-load status report is aggregated rather than customer-specific.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:current_total_facility_load_mw`
  - Basis: Energized substations, energized buildings, and live workloads do not disclose current site demand; ERCOT's public large-load reporting is aggregated rather than customer-specific.
  - Scope: Current metered load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.), [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-27; Undated current EPC-contractor page reporting grid construction and energization milestones through 2026-03-10 plus a then-current October 2026 permanent-transformer swap target.), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267) (accessed 2026-08-27; ERCOT records final PUCT approval on 2025-07-31 and explains that customer-owned large-load information is confidential, so the public large-load status report is aggregated rather than customer-specific.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:current_critical_it_load_mw`
  - Basis: The live-campus release establishes operating workloads but publishes no current IT-load telemetry or conversion from facility power to IT power.
  - Scope: Current critical IT load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.)

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

Presenter-facing teaching focus:

- Kind: `comparison`
- Title: Evidence bases are not interchangeable

1. U.S. LPT market example: up to/over 36 months; not an Abilene schedule
   - Claim IDs: `transformer_delivery_exposure`
2. External GE portfolio: ~10 GW available for 2029 delivery; not an Abilene schedule
   - Claim IDs: `turbine_manufacturing_slot`
3. External cooling: XCA first shipped 2026-06; generic acceptance sequence; not Abilene
   - Claim IDs: `cooling_product_availability_example`, `liquid_cooling_acceptance`

Validated claim territory:

- **gas authorization anchor — permitted.**
  - Binding: selected topology ownership
  - 10 units
  - Fact: `abilene:gas_turbine_units_authorized`
  - Basis: Five Solar Titan 350 units plus five GE LM2500 units are authorized.
  - Scope: Longhorn onsite simple-cycle gas generation
  - Boundary: `permitted_not_observed` / `permitted` / as of 2025-01-22
  - Topology target: node `gas_turbine` (Gas turbine package; `site_evidenced` / `permitted`)
  - Sources: [Texas Commission on Environmental Quality — Electric Generating Unit Standard Permit Technical Review, Registration 177263](https://records.tceq.texas.gov/cs/idcplg?IdcService=TCEQ_EXTERNAL_SEARCH_GET_FILE&Rendition=Web&dID=8600163) (accessed 2026-08-25; Project reviewer dated 2025-01-21; section manager dated 2025-01-22.)
- **energized transformer anchor — confirmed.**
  - Binding: selected topology ownership
  - 5 main power transformers
  - Fact: `abilene:grid_expansion_transformers_energized_count`
  - Basis: Mortenson reports all five main power transformers energized by 2026-03-10.
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 2026-03-10 (ISO-8601 date)
  - Fact: `abilene:grid_expansion_fully_energized_by`
  - Basis: Mortenson reports the fifth and final main power transformer energized on 2026-03-10; three temporary transformers still had planned permanent swaps.
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `hv_protection_envelope_345` (Abstract 345 kV protection envelope; `site_evidenced` / `energized`); node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **cooling design anchor — selected design.**
  - Binding: selected topology ownership
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Fact: `abilene:cooling_heat_rejection_posture`
  - Basis: Crusoe describes a selected closed-loop, non-evaporative liquid-cooling system with air-cooled chillers and no water consumed in heat rejection.
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Topology target: node `air_cooled_chiller` (Air-cooled chiller and condenser; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **transformer delivery exposure — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - up to and exceeding 36 (months)
  - Fact: `delivery_resilience:us_large_power_transformer_lead_time_2024`
  - Basis: DOE reports that recent conversations with domestic producers indicated large-power-transformer lead times up to and exceeding 36 months.
  - Scope: U.S. large-power-transformer market observation reported by DOE in July 2024; not a quote, order, or delivery forecast for an Abilene transformer.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy — Large Power Transformer Resilience Report to Congress](https://www.energy.gov/sites/default/files/2024-10/EXEC-2022-001242%20-%20Large%20Power%20Transformer%20Resilience%20Report%20signed%20by%20Secretary%20Granholm%20on%207-10-24.pdf) (accessed 2026-08-27; Report dated July 2024 and signed 2024-07-10.)
  - 12-30 (months)
  - Fact: `delivery_resilience:us_distribution_transformer_lead_time_2023`
  - Basis: DOE reports that distribution-transformer lead times increased from three to six months in 2019 to 12 to 30 months in 2023.
  - Scope: U.S. distribution-transformer market in 2023, the latest data stated on the DOE page; not a unit-substation or campus-transformer delivery quote.
  - Boundary: `design_not_observed` / `design_reference` / as of 2023
  - Sources: [U.S. Department of Energy Office of Electricity — Supply Chain and Market Analysis](https://www.energy.gov/oe/supply-chain-and-market-analysis) (accessed 2026-08-27; Current DOE page; its distribution-transformer lead-time comparison uses 2019 and 2023 data, and it records a working-group webinar on 2026-03-05.)
  - prequalification, bidding, design, manufacture, testing, special transport, delivery, and installation (delivery-stage sequence)
  - Fact: `delivery_resilience:large_power_transformer_delivery_chain`
  - Basis: DOE enumerates manufacturer prequalification, competitive bidding, device design, manufacture, testing, special transportation, delivery, and installation, and notes that the final transport miles can be especially challenging.
  - Scope: Generic large-power-transformer procurement and delivery chain; not a site schedule, contractual critical path, or acceptance record.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07
  - Sources: [U.S. Department of Energy — Large Power Transformer Resilience Report to Congress](https://www.energy.gov/sites/default/files/2024-10/EXEC-2022-001242%20-%20Large%20Power%20Transformer%20Resilience%20Report%20signed%20by%20Secretary%20Granholm%20on%207-10-24.pdf) (accessed 2026-08-27; Report dated July 2024 and signed 2024-07-10.)
- **turbine manufacturing slot — product reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - approximately 10 GW still available for 2029 delivery (GE Vernova portfolio availability)
  - Fact: `delivery_resilience:ge_gas_turbine_delivery_slot_exposure_2025`
  - Basis: GE Vernova stated that approximately 10 GW of supply remained available for 2029 deliveries and expected to be largely sold out of 2030 deliveries by the end of 2026.
  - Scope: GE Vernova gas-turbine portfolio statement on 2025-12-09; not a universal turbine lead time and not an Abilene Titan 350 or LM2500 delivery claim.
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2025-12-09
  - Sources: [GE Vernova — GE Vernova 2025 Investor Update Transcript](https://www.gevernova.com/sites/default/files/gev_webcast_transcript_12092025.pdf) (accessed 2026-08-27; Transcript of the 2025-12-09 investor update.)
- **turbine slot dependency — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A reserved manufacturing slot can precede site permitting and EPC-contract completion (project-delivery relationship)
  - Fact: `delivery_resilience:gas_turbine_slot_can_precede_site_readiness`
  - Basis: GE Vernova described fixed-price 2027-2028 delivery slots backed by deposits while customers were still working through air permits, EPC contracts, and site readiness, with the turbine contract coming first.
  - Scope: GE Vernova's 2024 U.S. AI-load-related slot-reservation portfolio; not a rule for every project and not evidence about Longhorn procurement.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-12-10
  - Sources: [GE Vernova — GE Vernova 2024 Investor Update Transcript](https://www.gevernova.com/sites/default/files/gev_investor_update_transcript_12102024.pdf) (accessed 2026-08-27; Transcript of the 2024-12-10 investor update.)
- **cooling product availability example — product reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2026-06 (first global shipment month)
  - Fact: `delivery_resilience:uniflair_xca_initial_shipping_date`
  - Basis: Schneider Electric's dated release states that the first Uniflair XCA chiller units began shipping globally in June 2026.
  - Scope: Schneider Electric Uniflair XCA 1.3-2.5 MW chiller product family; a launch-availability milestone, not customer lead time or Abilene selection.
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-06-02
  - Sources: [Schneider Electric — Schneider Electric Introduces New Uniflair XCA Chiller Line](https://www.se.com/uk/en/about-us/newsroom/news/press-releases/Schneider-Electric-Introduces-New-Uniflair-XCA-Chiller-Line-Designed-to-Enhance-Energy-Performance-and-Operational-Stability-in-HighDensity-AI-Data-Centers-6a1e894ad8e4a8ed3c04dc8c/) (accessed 2026-08-27; Global manufacturer release published from Rueil-Malmaison, France.)
- **liquid cooling acceptance — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - pre-functional checks, flushing and cleaning validation, hydro and pressure testing, functional performance testing, and integrated testing (commissioning-stage sequence)
  - Fact: `delivery_resilience:liquid_cooling_acceptance_sequence`
  - Basis: Schneider Electric identifies equipment arrival as only one milestone and lists these commissioning stages, including integrated pump- or chiller-failure scenarios and fluid-quality controls.
  - Scope: Generic manufacturer guidance for liquid-cooling projects, written in an India supply-chain context; not an Abilene acceptance plan or record.
  - Boundary: `design_not_observed` / `design_reference` / as of 2026-08-25
  - Sources: [Schneider Electric — Sources, spares, and commissioning liquid cooling in India: The supply-side](https://blog.se.com/datacenter/2026/08/25/sources-spares-and-commissioning-liquid-cooling-in-india-the-supply-side/) (accessed 2026-08-27; Dated manufacturer guidance whose supply-chain context is India; its commissioning sequence is used only as a generic acceptance reference.)

Red-line warnings:

- **permitted to installed.** A permit does not prove equipment was installed.
- **permitted to commissioned.** A permit does not prove equipment was commissioned.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **product to site configuration.** A product specification does not establish the site's selected configuration or operating point.
- **market example to site schedule.** Market lead times and product availability examples do not establish Abilene's schedule or critical path.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.

Handoff: Contrast scoped 36+ month equipment exposure with ~250 ms / <1 s external load behavior.

### 21. Fast load, slow grid `s19_fast_load_slow_grid`

- Opening question: What happens when many accelerators change load together?
- Teaching objective: Connect external synchronized-load observations to generic ride-through architecture while keeping Abilene's transient profile and BESS connection explicit unknowns.
- Visual focus: Unnamed 345 kV source, 345 kV expansion service, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope, BESS package, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `layers`
- Title: Fast event, layered response

1. External NERC example: ~250 ms fastest ramp; transitions <1 s; not Abilene
   - Claim IDs: `synchronized_ai_load_dynamics`
2. Facility ride-through and grid response are different layers
   - Claim IDs: `ride_through_engineering_boundary`, `voltage_sensitive_load_event`, `synchronized_ai_load_dynamics`
3. Abilene transient profile and BESS role remain unknown
   - Claim IDs: `abilene_transient_and_bess_boundary`, `bess_operation_unknown`

Validated claim territory:

- **bess future — future design.**
  - Binding: selected topology ownership
  - future (status)
  - Fact: `abilene:bess_reference_design_status`
  - Basis: Drawing 5MECH-00001-GA labels the BESS unit as FUTURE.
  - Scope: BESS shown on the Longhorn power-plant review drawing
  - Boundary: `future_design` / `future_design` / as of 2024-12-04
  - Topology target: node `bess_package` (BESS package; `site_evidenced` / `future_design`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **bess operation unknown — explicit unknown.**
  - Binding: selected topology ownership
  - Unknown — not established by the cited evidence
  - Fact: `abilene:bess_operational_status`
  - Basis: The review drawing does not establish procurement, installation, energization, or operation.
  - Scope: BESS at the original Abilene reference campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-25
  - Topology target: node `bess_package` (BESS package; `site_evidenced` / `future_design`)
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-25; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION; engineer release is dated 2024-12-05.)
- **operating compute anchor — confirmed.**
  - Binding: selected topology ownership
  - NVIDIA GB200 (platform family)
  - Fact: `abilene:rack_platform`
  - Basis: Crusoe reports NVIDIA GB200 racks delivered in June 2025 and early workloads running; it does not identify an operating rack count.
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **synchronized ai load dynamics — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - less than 1 (second)
  - Fact: `delivery_resilience:ai_training_checkpoint_transition_duration`
  - Basis: NERC reports that the transition between training and checkpoint saving, or the reverse transition, may occur in under one second.
  - Scope: NERC-observed transition between AI training and checkpoint saving in a 50 MW block of a larger 200 MW facility; not an Abilene waveform.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-07
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf) (accessed 2026-08-27; NERC Large Loads Task Force white paper dated July 2025.)
  - 1.9 per unit per second for approximately 250 milliseconds
  - Fact: `delivery_resilience:ai_training_observed_ramp_rate`
  - Basis: NERC reports a 1.9 per-unit-per-second demand change lasting about 250 milliseconds in the fastest ramping period of the observed profile.
  - Scope: Fastest interval in NERC's 50 MW-block AI-training observation; not a universal AI profile, processor specification, or Abilene measurement.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-07
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf) (accessed 2026-08-27; NERC Large Loads Task Force white paper dated July 2025.)
  - Millisecond processor-power variations can correlate during hyperscale parallel AI work and become significant at the site-demand boundary. (load-dynamics relationship)
  - Fact: `delivery_resilience:parallel_ai_load_correlation`
  - Basis: PNNL explains that individual processor demand can vary on millisecond timescales and that parallel computation correlates those variations, making them significant at site level.
  - Scope: Generic grid-level modeling principle for AI training and inference; not an Abilene transient magnitude, frequency, or operating trace.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) (accessed 2026-08-27; PNNL-38817, prepared for the U.S. Department of Energy.)
  - Large power-electronic loads can shift in seconds, faster than conventional generators can ramp (response-time relationship)
  - Fact: `delivery_resilience:large_load_grid_response_mismatch`
  - Basis: NERC states that fast load changes can outpace conventional generator ramping, stress balancing, voltage, and frequency control, and require operators to understand load ramp rates and procure suitable response.
  - Scope: Generic North American bulk-power-system relationship; not a response requirement, reserve product, or measured condition at Abilene.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-07
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf) (accessed 2026-08-27; NERC Large Loads Task Force white paper dated July 2025.)
- **voltage sensitive load event — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - 1500 MW approximate customer-side load reduction
  - Fact: `delivery_resilience:voltage_sag_data_center_load_loss_event`
  - Basis: NERC found that six properly cleared 42-66 millisecond faults coincided with approximately 1,500 MW of customer-side data-center load reduction; operators observed frequency and voltage rise after the load loss.
  - Scope: NERC's 2024 Eastern Interconnection incident involving a concentration of data-center-type load; not Abilene and not an AI-training ramp event.
  - Boundary: `design_not_observed` / `design_reference` / as of 2024-07-10
  - Sources: [North American Electric Reliability Corporation — Incident Review - Considering Simultaneous Voltage-Sensitive Load Reductions](https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_large_load_loss.pdf) (accessed 2026-08-27; NERC Event Analysis incident review published 2025-01-08.)
- **ride through engineering boundary — design reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A battery-backed UPS can assume load for a short grid disturbance or bridge until backup generation starts. (generic ride-through role)
  - Fact: `delivery_resilience:ups_short_duration_ride_through_role`
  - Basis: NERC describes battery-backed centralized and rack UPS systems as taking over during transient voltage disturbances; their batteries are intended for the disturbance interval or until a backup generator starts.
  - Scope: Generic static-UPS behavior described in a NERC incident review; not an Abilene UPS design, setting, capacity, runtime, or transfer sequence.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-01-08
  - Sources: [North American Electric Reliability Corporation — Incident Review - Considering Simultaneous Voltage-Sensitive Load Reductions](https://www.nerc.com/globalassets/our-work/reports/event-reports/incident_review_large_load_loss.pdf) (accessed 2026-08-27; NERC Event Analysis incident review published 2025-01-08.)
  - UPS ride-through depends on OEM capability, protection settings, operating mode, current limiting, synchronism, and output-voltage regulation. (configuration dependency)
  - Fact: `delivery_resilience:ups_ridethrough_depends_on_site_settings`
  - Basis: PNNL explains the UPS battery's DC-link support mechanism and states that more restrictive protection limits vary by site and may be user-set.
  - Scope: Generic double-conversion UPS behavior; no Abilene control or protection setting is inferred.
  - Boundary: `design_not_observed` / `design_reference` / as of 2025-12
  - Sources: [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) (accessed 2026-08-27; PNNL-38817, prepared for the U.S. Department of Energy.)
  - UPS provides conditioned no-break critical-load power; conventional behind-the-meter BESS provides site-level energy management, flexibility, and longer-duration reserve energy. (generic architectural distinction)
  - Fact: `delivery_resilience:ups_and_btm_bess_role_separation`
  - Basis: Vertiv distinguishes series critical-load UPS protection from the site-level energy-management, peak-shaving, and grid-services roles of a conventional behind-the-meter BESS.
  - Scope: Generic large-data-center architecture; not an Abilene equipment function, topology, rating, runtime, dispatch mode, or operating state.
  - Boundary: `design_not_observed` / `design_reference` / as of 2026-06-26
  - Sources: [Vertiv — BESS and UPS roles in large data center power architectures](https://www.vertiv.com/en-us/insights/articles/white-papers/bess-and-ups-roles-in-large-data-center-power-architecture/) (accessed 2026-08-27; Manufacturer technical page dated 2026-06-26.)
- **operating load shaping observations — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - tens of MW, nearly instantaneous ramps, recurring as often as every few seconds (operator-observed load pattern)
  - Fact: `delivery_resilience:google_synchronized_ml_fluctuation_observation`
  - Basis: Google reports tens-of-megawatts cluster-level fluctuations with ramping that could be almost instantaneous and recur every few seconds for long training runs.
  - Scope: Google's batch-synchronous ML workloads on dedicated Google clusters; not a universal GPU behavior or an Abilene operating trace.
  - Boundary: `confirmed` / `operating` / as of 2025-02-11
  - Sources: [Google Cloud — Balance of power: A full-stack approach to power and thermal fluctuations in ML infrastructure](https://cloud.google.com/blog/topics/systems/mitigating-power-and-thermal-fluctuations-in-ml-infrastructure) (accessed 2026-08-27; First-party Google operator report published 2025-02-11.)
  - nearly 50 (percent reduction in fluctuation magnitude in Google's test case)
  - Fact: `delivery_resilience:google_compiler_power_shaping_result`
  - Basis: Google reports that dynamically balancing compute activity around synchronization signatures reduced fluctuation magnitude by nearly 50% with less than one percent performance impact in the test case.
  - Scope: Google's compiler-based TPU workload-shaping test; not a guaranteed result for other hardware, workloads, sites, or the Abilene GB200 platform.
  - Boundary: `confirmed` / `deployed` / as of 2025-02-11
  - Sources: [Google Cloud — Balance of power: A full-stack approach to power and thermal fluctuations in ML infrastructure](https://cloud.google.com/blog/topics/systems/mitigating-power-and-thermal-fluctuations-in-ml-infrastructure) (accessed 2026-08-27; First-party Google operator report published 2025-02-11.)
- **abilene transient and bess boundary — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `delivery_resilience:abilene_bess_function_rating_connection_operation`
  - Basis: The available Longhorn review drawing establishes only a future design placeholder. It does not establish any of these site-specific attributes or lifecycle milestones.
  - Scope: Procurement, function, power and energy ratings, duration, connection, controls, installation, energization, commissioning, and operation of a BESS at the original Abilene reference campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Abilene DC 1, LLC, filed with the Texas Commission on Environmental Quality — Longhorn Power Plant Federal Operating Permit Application 37589](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) (accessed 2026-08-27; General arrangement drawing 5MECH-00001-GA, revision D, re-issued for review 2024-12-04 and marked NOT FOR CONSTRUCTION.)
  - Unknown — not established by the cited evidence
  - Fact: `delivery_resilience:abilene_operating_transient_profile`
  - Basis: The reviewed generic and external operator evidence establishes plausible mechanisms and observed examples, but none is a measurement or disclosed operating trace from Abilene.
  - Scope: Magnitude, ramp rate, periodicity, duration, and grid-facing response of synchronized compute demand at the original Abilene reference campus
  - Boundary: `unverified_null` / `site_configuration_unknown` / as of 2026-08-27
  - Sources: [North American Electric Reliability Corporation — Characteristics and Risks of Emerging Large Loads](https://www.nerc.com/globalassets/who-we-are/standing-committees/rstc/3_doc_white-paper-characteristics-and-risks-of-emerging-large-loads.pdf) (accessed 2026-08-27; NERC Large Loads Task Force white paper dated July 2025.), [Pacific Northwest National Laboratory for the U.S. Department of Energy — Electromagnetic Transient Modeling of Large Data Centers for Grid-Level Studies - Alpha Release](https://www.energy.gov/sites/default/files/2026-01/Data_Center_EMT_Models.pdf) (accessed 2026-08-27; PNNL-38817, prepared for the U.S. Department of Energy.), [Google Cloud — Balance of power: A full-stack approach to power and thermal fluctuations in ML infrastructure](https://cloud.google.com/blog/topics/systems/mitigating-power-and-thermal-fluctuations-in-ml-infrastructure) (accessed 2026-08-27; First-party Google operator report published 2025-02-11.)

Red-line warnings:

- **future design to operational.** A future design is not installed, commissioned, or operational.
- **reverse physical flow.** Do not reverse supply, return, heat, or electrical direction while explaining the diagram.
- **conceptual to as built.** Conceptual geometry is not an as-built connection or equipment configuration.
- **design to as built.** A design or engineering reference is not proof of the site's as-built condition.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **null to zero.** Unknown means not established by the cited evidence; it does not mean zero or absent.

Handoff: Put fast and slow constraints onto the same delivery funnel.

### 22. Build sequence is a staged evidence boundary `s20_build_sequence`

- Opening question: Which delivery stages are evidenced, and where must inference stop?
- Teaching objective: Apply the status funnel without substituting one capacity basis for another.
- Visual focus: Initial 200 MW / 138 kV station, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `funnel`
- Title: Five stages; no capacity-basis substitutions

1. PLANNED — grid interconnection and remaining six buildings
   - Claim IDs: `planned_grid_boundary`, `remaining_buildings_plan`
2. CONSTRUCTED — campus construction started in June 2024
   - Claim IDs: `construction_start`
3. ENERGIZED — grid infrastructure as of evidenced dates; at least two buildings
   - Claim IDs: `infrastructure_milestones`, `energized_minimum`, `first_two_buildings_energized`
4. LIVE — first phase operating and workloads live within dated boundaries
   - Claim IDs: `first_phase_operational`, `live_compute_boundary`
5. UNKNOWN — exact load, accelerators, and delivered basis
   - Claim IDs: `installed_gpu_no_estimate`, `untyped_delivery_boundary`, `current_delivery_boundary`

Validated claim territory:

- **planned grid boundary — planned.**
  - Binding: segment-local, nonphysical teaching overlay
  - 1200 MW
  - Fact: `abilene:planned_grid_interconnection_mw`
  - Basis: Crusoe explicitly describes 1.2 GW as the site's grid interconnection.
  - Scope: Original eight-building Abilene campus grid interconnection
  - Boundary: `planned_not_operational` / `planned` / as of 2025-03-18
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.)
- **infrastructure milestones — confirmed.**
  - Binding: selected topology ownership
  - 2026-08-25 (ISO-8601 date)
  - Fact: `abilene:grid_initial_service_operational_as_of`
  - Basis: Mortenson's current project page says the initial substation transitioned from de-energized construction into energized, operational service; it does not disclose the exact first-energization date.
  - Scope: Initial 200 MW / 138 kV Abilene grid path
  - Boundary: `confirmed` / `operating` / as of 2026-08-25
  - Topology target: node `initial_substation_138` (Initial 200 MW / 138 kV station; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
  - 2026-03-10 (ISO-8601 date)
  - Fact: `abilene:grid_expansion_fully_energized_by`
  - Basis: Mortenson reports the fifth and final main power transformer energized on 2026-03-10; three temporary transformers still had planned permanent swaps.
  - Scope: Separate 345 kV Abilene expansion substation
  - Boundary: `confirmed` / `energized` / as of 2026-03-10
  - Topology target: node `campus_substation_lpt_345` (1 GW / 345 kV expansion substation; `site_evidenced` / `energized`)
  - Sources: [Mortenson — Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-25; Undated current project page reporting milestones through 2026-03-10.)
- **energized minimum — confirmed minimum.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2 buildings
  - Fact: `abilene:buildings_energized_confirmed_min`
  - Basis: Crusoe reported the first two buildings energized and the first phase live; the 2026 Microsoft-expansion release reiterates the two original buildings.
  - Scope: Original eight-building Abilene campus
  - Boundary: `confirmed_minimum` / `energized` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.), [Crusoe — Crusoe announces new 900 MW AI factory campus in Abilene, Texas, to support Microsoft AI infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) (accessed 2026-08-25; Describes a separate adjacent two-building project whose first building was then expected in mid-2027.)
- **installed gpu no estimate — no evidence backed estimate.**
  - Binding: segment-local, nonphysical teaching overlay
  - No evidence-backed estimate
  - Fact: `abilene:installed_gpu_count`
  - Basis: no evidence-backed estimate
  - Scope: Original Abilene campus installed or operational GPU fleet
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.), [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **live compute boundary — live by.**
  - Binding: selected topology ownership
  - 2025-07-22 (ISO-8601 date)
  - Fact: `abilene:early_training_inference_live_by`
  - Basis: OpenAI reported on this date that parts of the facility were running and had recently begun early training and inference workloads.
  - Scope: Parts of the original Abilene campus
  - Boundary: `live_by_not_start_date` / `operating` / as of 2025-07-22
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [OpenAI — Stargate advances with partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-25; Reports parts of the Abilene facility running and recent early training and inference workloads; the exact workload start date is not supplied.)
- **untyped delivery boundary — reported untyped.**
  - Binding: segment-local, nonphysical teaching overlay
  - 42 percent
  - Fact: `abilene:oracle_capacity_delivered_percent_untyped`
  - Basis: Oracle reports 42 percent of total capacity delivered without stating the denominator, capacity basis, MW, building count, IT load, or current load.
  - Scope: Oracle's Abilene portfolio-page wording
  - Boundary: `reported_untyped` / `delivered_untyped` / as of 2026-01
  - Sources: [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/) (accessed 2026-08-25; Undated page marked information current January 2026 reports 42 percent of an unspecified total-capacity denominator delivered; the percentage cannot be converted to MW, buildings, IT load, or current load.)
- **construction start — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2024-06 (ISO-8601 month)
  - Fact: `abilene_execution:campus_construction_start_month`
  - Basis: Crusoe reports that construction of the multi-building campus began in June 2024.
  - Scope: Original Abilene AI data-center campus construction
  - Boundary: `confirmed` / `constructed` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.)
- **first two buildings energized — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2025-09-30 (ISO-8601 date upper bound)
  - Fact: `abilene_execution:first_two_buildings_energized_by`
  - Basis: Crusoe's dated live-campus release says the first two buildings had been energized within a year of the June 2024 construction start; the precise energization date is not supplied, so publication date is the safe bound.
  - Scope: First two buildings of the original Abilene campus
  - Boundary: `confirmed` / `energized` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.)
- **first phase operational — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2025-09-30 (ISO-8601 date upper bound)
  - Fact: `abilene_execution:first_phase_operational_by`
  - Basis: Crusoe's dated release states that the first phase was up and running on OCI by publication; it does not provide the exact first-operational date.
  - Scope: First phase of the original Abilene campus on Oracle Cloud Infrastructure
  - Boundary: `confirmed` / `operating` / as of 2025-09-30
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.)
- **remaining buildings plan — planned.**
  - Binding: segment-local, nonphysical teaching overlay
  - 2026-12-31 (ISO-8601 year-end bound)
  - Fact: `abilene_execution:original_remaining_six_buildings_planned_completion`
  - Basis: Crusoe's March 2026 release explicitly says the original second phase, which adds six buildings, was expected to reach completion by the end of 2026.
  - Scope: Six remaining buildings in the second phase of the original eight-building campus; excludes the adjacent Microsoft campus
  - Boundary: `planned_not_operational` / `planned` / as of 2026-03-27
  - Sources: [Crusoe — Crusoe Announces New 900 MW AI Factory Campus in Abilene, Texas, to Support Microsoft AI Infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) (accessed 2026-08-27; The adjacent Microsoft project itself is excluded. This ledger uses only the release's explicit retrospective statement that the original first two 100 MW buildings were constructed and energized in under one year and its current plan for the original six remaining buildings.)
- **current delivery boundary — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:current_operational_building_count_exact`
  - Basis: Primary sources establish a minimum of two energized buildings and a plan to complete six more by year-end 2026 but do not report an exact current operational count between those bounds.
  - Scope: Exact number of operational buildings in the original eight-building campus as of 2026-08-27
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.), [Crusoe — Crusoe Announces New 900 MW AI Factory Campus in Abilene, Texas, to Support Microsoft AI Infrastructure](https://www.crusoe.ai/resources/newsroom/crusoe-announces-new-900-mw-ai-factory-campus-in-abilene-texas-to-support-microsoft-ai-infrastructure) (accessed 2026-08-27; The adjacent Microsoft project itself is excluded. This ledger uses only the release's explicit retrospective statement that the original first two 100 MW buildings were constructed and energized in under one year and its current plan for the original six remaining buildings.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:current_total_facility_load_mw`
  - Basis: Energized substations, energized buildings, and live workloads do not disclose current site demand; ERCOT's public large-load reporting is aggregated rather than customer-specific.
  - Scope: Current metered load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.), [Mortenson — Abilene AI Data Center and Power Delivery](https://www.mortenson.com/projects/abilene-data-center-development) (accessed 2026-08-27; Undated current EPC-contractor page reporting grid construction and energization milestones through 2026-03-10 plus a then-current October 2026 permanent-transformer swap target.), [Electric Reliability Council of Texas — NPRR1267 Large Load Interconnection Status Report](https://www.ercot.com/mktrules/issues/NPRR1267) (accessed 2026-08-27; ERCOT records final PUCT approval on 2025-07-31 and explains that customer-owned large-load information is confidential, so the public large-load status report is aggregated rather than customer-specific.)
  - Unknown — not established by the cited evidence
  - Fact: `abilene_execution:current_critical_it_load_mw`
  - Basis: The live-campus release establishes operating workloads but publishes no current IT-load telemetry or conversion from facility power to IT power.
  - Scope: Current critical IT load of the original Abilene campus
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-27; Dated release establishing construction start, first-rack delivery, first-phase operation, two-building energization, and live-by workload milestones without disclosing current load or exact rack quantity.)

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
- Visual focus: Gas turbine package, Generator, Generator step-up package, AEP Abilene Northwest source, 138 kV slack-span tie, Initial 200 MW / 138 kV station, Unnamed 345 kV source, 345 kV expansion service, Abstract 345 kV protection envelope, 1 GW / 345 kV expansion substation, Abstract campus MV distribution envelope, BESS package, Emergency diesel backup package, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die, Air-cooled rack auxiliaries, Cold plate, Rack supply and return headers, Coolant distribution unit, CRAH / fan-wall branch, Closed facility water loop, Air-cooled chiller and condenser, Initial fill and water treatment, Atmosphere
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `layers`
- Title: Named roles do not establish asset ownership

1. Program: four funders; SoftBank finance, OpenAI operations
   - Claim IDs: `stargate_responsibility_structure`
2. Announcement: Crusoe owner/developer; Lancium developer role
   - Claim IDs: `abilene_developer_roles`
3. Contract: Crusoe designs, builds, operates phase-one 206 MW
   - Claim IDs: `phase1_delivery_and_operations_contract`
4. Compute: Oracle delivered GB200 racks; OpenAI reported workloads
   - Claim IDs: `operating_compute_roles`
5. Unknown ownership: land, components, IT, phase-one tenant
   - Claim IDs: `legal_ownership_boundary`

Validated claim territory:

- **stargate responsibility structure — reported structure.**
  - Binding: segment-local, nonphysical teaching overlay
  - SoftBank, OpenAI, Oracle, and MGX (named initial equity funders)
  - Fact: `commercial_compute:stargate_initial_equity_funders`
  - Basis: OpenAI and SoftBank explicitly name the four initial equity funders.
  - Scope: Stargate company/program formation; not per-asset Abilene ownership
  - Boundary: `confirmed` / `announced_structure` / as of 2025-01-21
  - Sources: [OpenAI and SoftBank — Announcing The Stargate Project](https://openai.com/index/announcing-the-stargate-project/) (accessed 2026-08-27; Dated formation announcement naming initial equity funders and the lead partners' financial and operational responsibilities at Stargate-program scope.)
  - SoftBank has financial responsibility and OpenAI has operational responsibility as Stargate's lead partners. (program-level responsibility allocation)
  - Fact: `commercial_compute:stargate_lead_responsibility_split`
  - Basis: The formation announcement assigns these responsibilities directly.
  - Scope: Stargate company/program; not ownership or operation of every Abilene asset
  - Boundary: `confirmed` / `announced_structure` / as of 2025-01-21
  - Sources: [OpenAI and SoftBank — Announcing The Stargate Project](https://openai.com/index/announcing-the-stargate-project/) (accessed 2026-08-27; Dated formation announcement naming initial equity funders and the lead partners' financial and operational responsibilities at Stargate-program scope.)
- **abilene developer roles — reported structure.**
  - Binding: segment-local, nonphysical teaching overlay
  - Crusoe would own and develop the initial Abilene data center. (announced project role)
  - Fact: `commercial_compute:abilene_2024_crusoe_owner_developer_announcement`
  - Basis: Crusoe and Lancium state that Crusoe will own and develop the data center.
  - Scope: Initial 200 MW Abilene data-center development as announced in July 2024
  - Boundary: `confirmed` / `announced_structure` / as of 2024-07-18
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center) (accessed 2026-08-27; Dated initial project announcement assigning Crusoe and Lancium roles; later financing disclosures add parties and must be read separately.)
  - Lancium's announced end-to-end role includes land acquisition, power interconnection, site engineering, renewable interconnection, and power orchestration. (announced project role)
  - Fact: `commercial_compute:abilene_lancium_development_role`
  - Basis: Crusoe and Lancium enumerate these functions in the initial release.
  - Scope: Lancium Clean Campus / initial Abilene development
  - Boundary: `confirmed` / `announced_structure` / as of 2024-07-18
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center) (accessed 2026-08-27; Dated initial project announcement assigning Crusoe and Lancium roles; later financing disclosures add parties and must be read separately.)
- **phase1 delivery and operations contract — contract reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Crusoe designs, builds, and operates the 206 MW phase-one data center. (named project role)
  - Fact: `commercial_compute:abilene_phase1_crusoe_delivery_and_operations_role`
  - Basis: The phase-one joint-venture announcement assigns all three functions to Crusoe.
  - Scope: Phase-one 206 MW, 998,000-square-foot Abilene joint-venture asset
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2024-10-15
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.)
- **operating compute roles — confirmed.**
  - Binding: segment-local, nonphysical teaching overlay
  - Oracle delivered the first NVIDIA GB200 racks, and OpenAI reported running early training and inference workloads on operating Abilene capacity. (named compute delivery and workload roles)
  - Fact: `commercial_compute:abilene_compute_activity_roles`
  - Basis: OpenAI states both roles directly in its July 2025 update.
  - Scope: Operating parts of Stargate I at Abilene; not legal title to the equipment
  - Boundary: `confirmed` / `operating` / as of 2025-07-22
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.)
- **legal ownership boundary — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_land_legal_owner`
  - Basis: The named sources describe Lancium's land-acquisition role and subsequent sponsors, but do not establish current legal title to the land.
  - Scope: Land underlying the original eight-building Abilene development
  - Boundary: `unverified_null` / `ownership_unknown` / as of 2026-08-27
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center) (accessed 2026-08-27; Dated initial project announcement assigning Crusoe and Lancium roles; later financing disclosures add parties and must be read separately.), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture) (accessed 2026-08-27; Dated phase-two announcement describing joint sponsorship of six additional buildings; it does not publish a debt-equity waterfall.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_power_asset_ownership_by_component`
  - Basis: The primary commercial disclosures do not provide a current component-by-component legal ownership schedule.
  - Scope: Abilene utility ties, substations, onsite generation, backup generation, storage, campus distribution, and building electrical equipment
  - Boundary: `unverified_null` / `ownership_unknown` / as of 2026-08-27
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center) (accessed 2026-08-27; Dated initial project announcement assigning Crusoe and Lancium roles; later financing disclosures add parties and must be read separately.), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture) (accessed 2026-08-27; Dated phase-two announcement describing joint sponsorship of six additional buildings; it does not publish a debt-equity waterfall.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_it_equipment_legal_owner`
  - Basis: Delivery and operating disclosures do not state which entity holds legal title to the installed IT equipment.
  - Scope: Installed Abilene racks, accelerators, network, and associated IT equipment
  - Boundary: `unverified_null` / `ownership_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_phase1_tenant_identity`
  - Basis: The transaction release calls the tenant a Fortune 100 hyperscaler but does not name it; later statements about Oracle and OpenAI roles do not by themselves establish the lease counterparty.
  - Scope: Phase-one two-building Abilene lease
  - Boundary: `unverified_null` / `counterparty_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.)

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

Presenter-facing teaching focus:

- Kind: `layers`
- Title: Public structure, private earning gates

1. Published phase-one financing and lease structure
   - Claim IDs: `phase1_financing_and_lease`
2. Published phase-two joint-venture structure
   - Claim IDs: `phase2_joint_venture`
3. Equipment finance, acceptance, rent, and utilization terms remain unknown
   - Claim IDs: `undisclosed_capital_and_risk_terms`

Validated claim territory:

- **phase1 financing and lease — contract reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - A $3.4 billion fully funded forward takeout, with funds managed by Blue Owl's Real Estate platform and Primary Digital Infrastructure jointly sponsoring the 206 MW data center designed, built, and operated by Crusoe. (named transaction structure)
  - Fact: `commercial_compute:abilene_phase1_financing_structure`
  - Basis: The parties disclose the amount, structure, sponsors, asset scope, and operator.
  - Scope: Phase-one 206 MW Abilene joint venture only
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2024-10-15
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.)
  - The phase-one two-building project was 100 percent long-term leased to an unnamed Fortune 100 hyperscale tenant. (named lease posture)
  - Fact: `commercial_compute:abilene_phase1_lease_structure`
  - Basis: The joint-venture release states the occupancy and tenant category directly.
  - Scope: Phase-one Abilene data center only
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2024-10-15
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.)
- **phase2 joint venture — contract reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Crusoe, funds managed by Blue Owl's Real Assets platform, and Primary Digital Infrastructure jointly sponsor construction of six additional buildings under the second phase of a $15 billion joint venture. (named transaction structure)
  - Fact: `commercial_compute:abilene_phase2_financing_structure`
  - Basis: The phase-two release states the amount, parties, and construction scope.
  - Scope: Six-building phase-two Abilene expansion
  - Boundary: `confirmed_contract` / `contracted_structure` / as of 2025-05-21
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture) (accessed 2026-08-27; Dated phase-two announcement describing joint sponsorship of six additional buildings; it does not publish a debt-equity waterfall.)
- **undisclosed capital and risk terms — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_phase1_lease_term_years`
  - Basis: The release says long-term but does not publish the lease duration.
  - Scope: Phase-one Abilene tenant lease
  - Boundary: `unverified_null` / `contract_term_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_capital_stack_waterfall`
  - Basis: The releases publish headline joint-venture amounts and sponsors but not debt-equity proportions, security, priority, guarantees, or distribution waterfalls.
  - Scope: Original eight-building Abilene development and its phase-specific joint ventures
  - Boundary: `unverified_null` / `financing_terms_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture) (accessed 2026-08-27; Dated phase-two announcement describing joint sponsorship of six additional buildings; it does not publish a debt-equity waterfall.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_rent_commencement_and_acceptance_terms`
  - Basis: Public releases do not disclose rent commencement, delivery acceptance, service-credit, termination, or performance-guarantee terms.
  - Scope: Phase-one and phase-two Abilene leases and customer arrangements
  - Boundary: `unverified_null` / `contract_term_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital, and Primary Digital Infrastructure enter second phase of $15 billion joint venture to fund AI data center in Abilene, Texas](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture) (accessed 2026-08-27; Dated phase-two announcement describing joint sponsorship of six additional buildings; it does not publish a debt-equity waterfall.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_it_equipment_financing_terms`
  - Basis: The cited Abilene disclosures do not publish equipment purchase, lease, collateral, vendor-finance, or ownership terms.
  - Scope: Abilene accelerators, racks, networking, and associated IT equipment
  - Boundary: `unverified_null` / `financing_terms_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_utilization_risk_allocation`
  - Basis: A fully leased facility does not establish who bears workload-utilization, accelerator-idle-time, or token-demand risk, and the public transaction disclosures do not provide those terms.
  - Scope: Abilene facility occupancy and compute utilization
  - Boundary: `unverified_null` / `contract_term_unknown` / as of 2026-08-27
  - Sources: [Crusoe, Blue Owl Capital, and Primary Digital Infrastructure — Crusoe, Blue Owl Capital and Primary Digital Infrastructure enter $3.4 billion joint venture for AI data center development](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) (accessed 2026-08-27; Dated phase-one transaction announcement describing the forward takeout, sponsors, Crusoe operating role, and the anonymous long-term tenant.), [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.)

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

Presenter-facing teaching focus:

- Kind: `comparison`
- Title: Same machine, different risk allocation

1. Developer: Crusoe owner/developer announcement; Lancium development functions
   - Claim IDs: `developer_role_comparison`
2. Colo: Equinix operates space and power; customers place IT; facility tenure varies
   - Claim IDs: `colocation_comparison`
3. Neocloud: leased space, equipment commitments, and utilization-linked contract risk
   - Claim IDs: `neocloud_operating_comparison`, `neocloud_contract_risk_comparison`
4. Hyperscaler: Microsoft owns or leases facilities and aggregates cloud demand
   - Claim IDs: `hyperscale_cloud_comparison`

Validated claim territory:

- **developer role comparison — reported structure.**
  - Binding: segment-local, nonphysical teaching overlay
  - Crusoe would own and develop the initial Abilene data center. (announced project role)
  - Fact: `commercial_compute:abilene_2024_crusoe_owner_developer_announcement`
  - Basis: Crusoe and Lancium state that Crusoe will own and develop the data center.
  - Scope: Initial 200 MW Abilene data-center development as announced in July 2024
  - Boundary: `confirmed` / `announced_structure` / as of 2024-07-18
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center) (accessed 2026-08-27; Dated initial project announcement assigning Crusoe and Lancium roles; later financing disclosures add parties and must be read separately.)
  - Lancium's announced end-to-end role includes land acquisition, power interconnection, site engineering, renewable interconnection, and power orchestration. (announced project role)
  - Fact: `commercial_compute:abilene_lancium_development_role`
  - Basis: Crusoe and Lancium enumerate these functions in the initial release.
  - Scope: Lancium Clean Campus / initial Abilene development
  - Boundary: `confirmed` / `announced_structure` / as of 2024-07-18
  - Sources: [Crusoe and Lancium — Crusoe to build initial 200 MW AI data center with plans to expand at 1.2 GW Lancium Clean Campus](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center) (accessed 2026-08-27; Dated initial project announcement assigning Crusoe and Lancium roles; later financing disclosures add parties and must be read separately.)
- **colocation comparison — business model reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Equinix's IBX colocation offering supplies secure data-center space and power for customers' IT infrastructure, typically bills from space and power consumption under fixed-duration contracts, and generates monthly recurring revenue; contracts are generally one to five years. (named business-model comparison)
  - Fact: `commercial_compute:equinix_colocation_comparison`
  - Basis: Equinix describes its offering, billing basis, and typical contract duration.
  - Scope: Equinix IBX colocation as reported for 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [Equinix, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1101239/000110123926000032/eqix-20251231.htm) (accessed 2026-08-27; Signed 2026-02-11; used only as named colocation and hyperscale-colocation comparison evidence.)
  - Equinix operates the IBX facility environment while customers colocate their IT equipment; Equinix owns some IBX facilities and leases others, and landlord control of base infrastructure varies by lease. (named asset and operating boundary)
  - Fact: `commercial_compute:equinix_asset_and_operating_boundary`
  - Basis: The filing distinguishes customer equipment, Equinix operations, and mixed facility tenure.
  - Scope: Equinix IBX portfolio as reported for 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [Equinix, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1101239/000110123926000032/eqix-20251231.htm) (accessed 2026-08-27; Signed 2026-02-11; used only as named colocation and hyperscale-colocation comparison evidence.)
- **neocloud operating comparison — business model reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - CoreWeave primarily finances infrastructure development with asset-level debt supported by take-or-pay customer contracts, supplemented by corporate equity and debt; it also offers pay-as-you-go access. (named business-model comparison)
  - Fact: `commercial_compute:coreweave_ai_cloud_contract_and_financing_comparison`
  - Basis: CoreWeave states its financing and customer-contract mix directly.
  - Scope: CoreWeave AI cloud as reported for 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [CoreWeave, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) (accessed 2026-08-27; Signed 2026-03-02; used only as a named AI-cloud comparison case, not as evidence for Abilene's contracts or assets.)
  - CoreWeave leases or licenses third-party data-center space and does not control operation of those facilities; under certain separate lease arrangements it must procure and install lessee-owned equipment. (named asset and operating boundary)
  - Fact: `commercial_compute:coreweave_facility_and_equipment_boundary_comparison`
  - Basis: The filing distinguishes facility control from separate lessee-owned asset commitments.
  - Scope: CoreWeave portfolio and disclosed commitments as of 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-12-31
  - Sources: [CoreWeave, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) (accessed 2026-08-27; Signed 2026-03-02; used only as a named AI-cloud comparison case, not as evidence for Abilene's contracts or assets.)
- **neocloud contract risk comparison — contract reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - CoreWeave committed contracts typically require payment regardless of utilization, while on-demand arrangements permit usage reductions with limited notice; multi-year fixed-capacity facility leases can leave CoreWeave paying for capacity that customers do not use and pay for. (named risk-allocation comparison)
  - Fact: `commercial_compute:coreweave_capacity_and_utilization_risk_comparison`
  - Basis: The filing states these payment and capacity-mismatch exposures directly.
  - Scope: CoreWeave contracts and facility leases as reported for 2025; not Abilene
  - Boundary: `confirmed_contract` / `operating_business_model` / as of 2025-12-31
  - Sources: [CoreWeave, Inc., filed with the U.S. Securities and Exchange Commission — Annual Report on Form 10-K for the year ended December 31, 2025](https://www.sec.gov/Archives/edgar/data/1769628/000176962826000104/crwv-20251231.htm) (accessed 2026-08-27; Signed 2026-03-02; used only as a named AI-cloud comparison case, not as evidence for Abilene's contracts or assets.)
- **hyperscale cloud comparison — business model reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Microsoft operates data centers, owns and leases facilities, invests in data centers and computer systems, and sells Azure and other cloud services; aggregating diverse demand is part of its stated utilization economics. (named business-model comparison)
  - Fact: `commercial_compute:microsoft_hyperscale_cloud_comparison`
  - Basis: Microsoft's annual report describes its operating footprint, owned and leased facilities, capital investment, cloud revenue, and economies of scale.
  - Scope: Microsoft hyperscale cloud as reported for fiscal 2025; not Abilene
  - Boundary: `confirmed` / `operating_business_model` / as of 2025-06-30
  - Sources: [Microsoft Corporation — 2025 Annual Report](https://www.microsoft.com/investor/reports/ar25/index.html) (accessed 2026-08-27; Microsoft's official annual-report rendering of its fiscal-2025 Form 10-K; used only as a named hyperscale-cloud comparison case.)

Red-line warnings:

- **contractual to physical.** A contract or commercial role does not establish physical power flow or asset control.
- **site scope transfer.** A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.
- **capacity basis substitution.** Do not substitute one capacity, power, energy, or compute basis for another.
- **announced to operational.** An announced structure or role does not prove current operation.

Handoff: Return to the opening question with the physical conversion path and no-estimate stop rule visible.

## Act 7: From delivered power to usable compute

Teach an assumption-bound conversion recipe without inventing an Abilene token estimate.

### 26. From delivered megawatts to tokens `s24_megawatts_to_tokens`

- Opening question: Given delivered power, how many useful tokens result?
- Teaching objective: Keep power-rate and energy-yield routes dimensionally separate, require matching hardware and workload measurements, and preserve the no-estimate boundary for the reference campus.
- Visual focus: Abstract campus MV distribution envelope, Unit substation transformer, LV switchgear, UPS, Busway, Rack power shelves, Voltage regulator module, GPU die, Cold plate, Rack supply and return headers, Coolant distribution unit, Closed facility water loop, Air-cooled chiller and condenser, Atmosphere
- Visual state: focused 2D view; evidence panel on demand.
- Evidence posture: **evidence ready**

Presenter-facing teaching focus:

- Kind: `routes`
- Title: Scenario unit cancellation; no Abilene values

1. Inference rate: W_facility×W_IT/W_facility×W_accel/W_IT×tokens/J=tokens/s
   - Claim IDs: `facility_to_it_scenario_step`, `inference_published_boundaries`, `inference_scenario_step`, `complete_scenario_recipe`
2. Energy yield: J_facility×J_IT/J_facility×J_accel/J_IT×tokens/J=tokens
   - Claim IDs: `pue_accounting_boundary`, `facility_to_it_scenario_step`, `inference_scenario_step`, `complete_scenario_recipe`
3. Training: active peak matmul FLOP/s × same-system measured MFU ÷ model FLOP/token = tokens/s
   - Claim IDs: `training_published_method`, `training_scenario_step`, `complete_scenario_recipe`
4. Missing site input means no Abilene estimate
   - Claim IDs: `site_power_no_estimates`, `site_compute_no_estimates`, `site_workload_configuration_unknown`

Validated claim territory:

- **current installed gpu no estimate — no evidence backed estimate.**
  - Binding: segment-local, nonphysical teaching overlay
  - No evidence-backed estimate
  - Fact: `abilene:installed_gpu_count`
  - Basis: no evidence-backed estimate
  - Scope: Original Abilene campus installed or operational GPU fleet
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-25
  - Sources: [Crusoe — Crusoe expands AI data center campus in Abilene to 1.2 gigawatts](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts) (accessed 2026-08-25; Reports an eight-building design, a planned 1.2 GW grid interconnection, and an up-to-50,000-GPU design ceiling per building.), [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **untyped delivery boundary — reported untyped.**
  - Binding: segment-local, nonphysical teaching overlay
  - 42 percent
  - Fact: `abilene:oracle_capacity_delivered_percent_untyped`
  - Basis: Oracle reports 42 percent of total capacity delivered without stating the denominator, capacity basis, MW, building count, IT load, or current load.
  - Scope: Oracle's Abilene portfolio-page wording
  - Boundary: `reported_untyped` / `delivered_untyped` / as of 2026-01
  - Sources: [Oracle — AI Data Centers - Investing in Communities, Powering the Future](https://www.oracle.com/data-centers/) (accessed 2026-08-25; Undated page marked information current January 2026 reports 42 percent of an unspecified total-capacity denominator delivered; the percentage cannot be converted to MW, buildings, IT load, or current load.)
- **operating platform anchor — confirmed.**
  - Binding: selected topology ownership
  - NVIDIA GB200 (platform family)
  - Fact: `abilene:rack_platform`
  - Basis: Crusoe reports NVIDIA GB200 racks delivered in June 2025 and early workloads running; it does not identify an operating rack count.
  - Scope: Operationally supported first-phase rack-platform family at the original Abilene campus; family identity only, not rack, tray, or GPU quantity
  - Boundary: `confirmed` / `deployed` / as of 2025-09-30
  - Topology target: node `die` (GPU die; `platform_evidenced` / `operational_confirmed`)
  - Sources: [Crusoe — Crusoe announces flagship Abilene data center is live](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) (accessed 2026-08-25; Reports the first phase live and the first two buildings energized.)
- **rack power product reference — product reference.**
  - Binding: selected topology ownership
  - 50-51 (VDC)
  - Fact: `abilene:rack_power_shelf_output_vdc`
  - Basis: NVIDIA specifies that DGX GB200 power shelves convert AC to nominal 50-51 VDC.
  - Scope: NVIDIA DGX GB200 rack power-shelf nominal DC busbar output
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Topology target: node `power_shelf` (Rack power shelves; `platform_evidenced` / `conceptual`); edge `power_shelf_to_vrm` (Rack power shelves → Voltage regulator module; `platform_evidenced` / `conceptual`)
  - Sources: [NVIDIA — DGX GB200 Hardware Overview](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-25; Documentation last updated 2026-03-03.)
- **selected heat rejection — selected design.**
  - Binding: selected topology ownership
  - closed-loop, non-evaporative; air-cooled chillers (system design)
  - Fact: `abilene:cooling_heat_rejection_posture`
  - Basis: Crusoe describes a selected closed-loop, non-evaporative liquid-cooling system with air-cooled chillers and no water consumed in heat rejection.
  - Scope: Selected cooling and heat-rejection design for the original Abilene campus
  - Boundary: `design_selected` / `selected_design` / as of 2025-08-05
  - Topology target: node `facility_loop` (Closed facility water loop; `site_evidenced` / `conceptual`); node `air_cooled_chiller` (Air-cooled chiller and condenser; `site_evidenced` / `conceptual`); edge `facility_to_chiller_return` (Closed facility water loop → Air-cooled chiller and condenser; `site_evidenced` / `conceptual`); edge `chiller_to_atmosphere` (Air-cooled chiller and condenser → Atmosphere; `site_evidenced` / `conceptual`)
  - Sources: [Crusoe — An inside look at the Abilene AI data center](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) (accessed 2026-08-25; Describes the project-specific closed-loop, non-evaporative liquid-cooling selection, air-cooled heat rejection, initial fill requirement, and anticipated annual maintenance water.)
- **pue accounting boundary — method reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - PUE is total data-center energy consumption over a continuous 12-month period divided by IT-equipment energy consumption over the same period; IT equipment includes equipment used to store, process, and transport data. (authoritative energy-accounting definition)
  - Fact: `commercial_compute:pue_energy_boundary`
  - Basis: The standard defines the numerator, denominator, period, and IT-equipment boundary.
  - Scope: ISO/IEC 30134-2:2026 PUE; not an Abilene measurement
  - Boundary: `authoritative_guidance` / `accounting_standard` / as of 2026-01-16
  - Sources: [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen) (accessed 2026-08-27; Current second edition defining PUE over a continuous 12-month energy boundary and distinguishing designed, interim, and partial derivatives.)
- **facility to it scenario step — derived scenario reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - For a matching continuous 12-month boundary, scenario IT energy equals scenario total data-center energy divided by scenario PUE. An average-power route instead requires direct IT-power metering or a boundary-matched interim or partial PUE over the same averaging interval; annual PUE must not be silently treated as a point-in-time operating ratio. (scenario calculation rule)
  - Fact: `commercial_compute:facility_energy_to_it_energy_recipe`
  - Basis: Algebra from the ISO PUE definition, with the standard's period and boundary preserved.
  - Scope: Energy-accounting step in a hypothetical scenario; not an Abilene estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen) (accessed 2026-08-27; Current second edition defining PUE over a continuous 12-month energy boundary and distinguishing designed, interim, and partial derivatives.)
- **rack compute product reference — product reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - One NVIDIA DGX GB NVL72 rack contains 72 GPUs across 18 compute trays and has approximate rack power consumption of 120 kW. (manufacturer product configuration)
  - Fact: `commercial_compute:dgx_gb_nvl72_product_reference`
  - Basis: NVIDIA specifies the rack composition and approximate rack consumption.
  - Scope: NVIDIA DGX GB rack-scale product documentation; not Abilene installed quantity or draw
  - Boundary: `confirmed_model_spec` / `product_documented` / as of 2026-03-03
  - Sources: [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-27; Documentation last updated 2026-03-03.)
- **training published method — method reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Model FLOPs utilization is observed training throughput in tokens per second divided by the theoretical maximum token throughput of the same system operating at peak FLOPs, counting the model-required forward and backward operations rather than implementation-dependent rematerialization. (training-efficiency definition)
  - Fact: `commercial_compute:training_mfu_definition`
  - Basis: The PaLM authors define MFU and distinguish it from hardware FLOPs utilization.
  - Scope: Training-system analysis in the PaLM paper; not inference utilization or Abilene MFU
  - Boundary: `authoritative_guidance` / `published_method` / as of 2022-10-05
  - Sources: [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311) (accessed 2026-08-27; Version 5 defines model FLOPs utilization and gives the dense decoder-only training FLOPs-per-token calculation used here.)
  - For the PaLM paper's dense decoder-only training boundary, theoretical FLOPs per token are 6N plus 12LHQT, where N is parameter count and L, H, Q, and T are layers, attention heads, head dimension, and sequence length. (published training-method boundary)
  - Fact: `commercial_compute:dense_decoder_training_flops_per_token_method`
  - Basis: The PaLM appendix publishes the FLOPs-per-token and MFU equations.
  - Scope: Dense decoder-only training under the PaLM counting convention; not a general inference formula and not an Abilene estimate
  - Boundary: `authoritative_guidance` / `published_method` / as of 2022-10-05
  - Sources: [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311) (accessed 2026-08-27; Version 5 defines model FLOPs utilization and gives the dense decoder-only training FLOPs-per-token calculation used here.)
- **training scenario step — derived scenario reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Scenario training tokens per second equal exact active aggregate peak matmul FLOP/s times MFU measured for the same model and system, divided by the model's FLOPs-per-token term. Supply active hardware quantity and applicable per-device performance explicitly. If the route begins from accelerator power, reconcile the selected inventory's measured power to that same power boundary. Apply a separate fleet active-duty factor only when MFU is conditional on active execution. (derived training scenario rule)
  - Fact: `commercial_compute:dense_decoder_training_tokens_recipe`
  - Basis: Derived application of the PaLM FLOPs-per-token and MFU equations with explicit hardware, power, and activity boundaries.
  - Scope: Dense decoder-only training under the PaLM counting convention; not a general inference formula and not an Abilene estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311) (accessed 2026-08-27; Version 5 defines model FLOPs utilization and gives the dense decoder-only training FLOPs-per-token calculation used here.), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-27; Documentation last updated 2026-03-03.)
- **inference published boundaries — method reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Triton dynamic batching combines requests and typically increases throughput; batch size and queue delay are configured per model and can trade increased latency for throughput. (runtime performance dependency)
  - Fact: `commercial_compute:inference_batching_dependency`
  - Basis: NVIDIA documents the behavior and recommends measuring latency and throughput while tuning.
  - Scope: NVIDIA Triton inference serving; not an Abilene runtime configuration
  - Boundary: `authoritative_guidance` / `product_documented` / as of 2026-08-27
  - Sources: [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html) (accessed 2026-08-27; Versioned official runtime documentation; used to establish that batching configuration changes throughput and latency.)
  - A defensible inference-throughput result names the model, dataset or workload, quality target, scenario, system under test, and latency constraints. MLPerf separates Offline measured throughput from Server maximum supported throughput under benchmark-specific latency limits and records time to first token and time per output token for LLMs. (benchmark measurement boundary)
  - Fact: `commercial_compute:inference_measurement_boundary`
  - Basis: MLCommons defines distinct scenarios, metrics, quality gates, and LLM latency measures.
  - Scope: MLPerf Inference methodology; not an Abilene benchmark result
  - Boundary: `authoritative_guidance` / `benchmark_method` / as of 2026-08-27
  - Sources: [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc) (accessed 2026-08-27; Living official rules at the access date; used for measurement-boundary requirements, not as a performance result for any Abilene system.)
- **inference scenario step — derived scenario reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Use measured tokens per joule for the exact model, weights or quantization, hardware, software, batch and concurrency policy, input/output-length distribution, quality target, and latency boundary, so matching accelerator watts times tokens per joule yields tokens per second. Alternatively, scale exact-system measured tokens per second only by a matching system count and measured scale-efficiency factor, with matching measured power as a consistency check. Facility MW or product peak FLOPs alone do not establish inference tokens per second. (scenario calculation rule)
  - Fact: `commercial_compute:inference_tokens_recipe`
  - Basis: NVIDIA documents batching-dependent latency/throughput and MLCommons requires workload-, system-, quality-, scenario-, and latency-specific measurement.
  - Scope: Hypothetical inference scenario; not an Abilene estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html) (accessed 2026-08-27; Versioned official runtime documentation; used to establish that batching configuration changes throughput and latency.), [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc) (accessed 2026-08-27; Living official rules at the access date; used for measurement-boundary requirements, not as a performance result for any Abilene system.)
- **complete scenario recipe — derived scenario reference.**
  - Binding: segment-local, nonphysical teaching overlay
  - Choose one output and one common averaging interval. For a power-rate route, start with measured average facility power over that interval; obtain matching average IT power from direct metering or a boundary-matched interim or partial PUE, then obtain accelerator power from direct metering or a measured IT-power share. For training, supply exact active hardware quantity, applicable aggregate peak matmul FLOP/s, and MFU measured for the same model and system; divide aggregate peak FLOP/s times MFU by model FLOPs per token. Apply a separate fleet active-duty factor only when MFU is conditional on active execution, and reconcile the inventory's measured power with accelerator power. For inference, multiply matching accelerator watts by tokens per joule measured for the exact model, weights or quantization, hardware, software, batching, input/output distribution, quality, and latency boundary; or scale exact-system tokens per second with matching system count and measured scale efficiency. For an energy-yield route, start with facility energy over the interval, derive matching IT energy, then use measured accelerator-energy share and matching tokens per joule, or integrate the rate route over the same interval, to produce token count. Annual PUE is valid only for its matching annual boundary. Propagate ranges and stop with no estimate when any required site input is unavailable. (assumption-driven scenario recipe)
  - Fact: `commercial_compute:mw_to_tokens_scenario_recipe`
  - Basis: The recipe preserves ISO energy boundaries, NVIDIA product/runtime distinctions, the PaLM training-MFU definition, and MLPerf measurement constraints without substituting product nameplate for observed operation.
  - Scope: General teaching recipe; produces no Abilene token estimate
  - Boundary: `derived_from_authoritative_sources` / `derived_scenario_method` / as of 2026-08-27
  - Sources: [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen) (accessed 2026-08-27; Current second edition defining PUE over a continuous 12-month energy boundary and distinguishing designed, interim, and partial derivatives.), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-27; Documentation last updated 2026-03-03.), [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html) (accessed 2026-08-27; Versioned official runtime documentation; used to establish that batching configuration changes throughput and latency.), [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311) (accessed 2026-08-27; Version 5 defines model FLOPs utilization and gives the dense decoder-only training FLOPs-per-token calculation used here.), [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc) (accessed 2026-08-27; Living official rules at the access date; used for measurement-boundary requirements, not as a performance result for any Abilene system.)
- **site power no estimates — no evidence backed estimate.**
  - Binding: segment-local, nonphysical teaching overlay
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_current_facility_power_mw`
  - Basis: no evidence-backed estimate
  - Scope: Current operating total-facility power for the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.)
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_current_it_power_mw`
  - Basis: no evidence-backed estimate
  - Scope: Current operating IT-equipment power for the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.)
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_current_pue`
  - Basis: no evidence-backed estimate
  - Scope: Measured current PUE, iPUE, or pPUE for the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.), [International Organization for Standardization and International Electrotechnical Commission — ISO/IEC 30134-2:2026 Information technology - Data centres key performance indicators - Part 2: Power usage effectiveness (PUE)](https://www.iso.org/obp/ui?_escaped_fragment_=iso%3Astd%3Aiso-iec%3A30134%3A-2%3Aed-2%3Av1%3Aen) (accessed 2026-08-27; Current second edition defining PUE over a continuous 12-month energy boundary and distinguishing designed, interim, and partial derivatives.)
- **site compute no estimates — no evidence backed estimate.**
  - Binding: segment-local, nonphysical teaching overlay
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_installed_accelerator_count`
  - Basis: no evidence-backed estimate
  - Scope: Installed or operational accelerator fleet at the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-27; Documentation last updated 2026-03-03.)
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_usable_accelerator_power_mw`
  - Basis: no evidence-backed estimate
  - Scope: Usable accelerator power at the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.), [NVIDIA — DGX Grace Blackwell Rack Scale Systems User Guide - Hardware](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html) (accessed 2026-08-27; Documentation last updated 2026-03-03.)
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_accelerator_power_share`
  - Basis: no evidence-backed estimate
  - Scope: Accelerator share of current Abilene IT-equipment power
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.)
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_accelerator_active_utilization`
  - Basis: no evidence-backed estimate
  - Scope: Time- and fleet-weighted active accelerator utilization at Abilene
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.)
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_training_mfu`
  - Basis: no evidence-backed estimate
  - Scope: Any training workload running at Abilene
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Google Research authors via arXiv — PaLM: Scaling Language Modeling with Pathways](https://arxiv.org/abs/2204.02311) (accessed 2026-08-27; Version 5 defines model FLOPs utilization and gives the dense decoder-only training FLOPs-per-token calculation used here.)
  - No evidence-backed estimate
  - Fact: `commercial_compute:abilene_measured_token_throughput`
  - Basis: no evidence-backed estimate
  - Scope: Any training or inference workload at the original Abilene campus
  - Boundary: `no_evidence_backed_estimate` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [Oracle — Abilene, Texas Data Center](https://www.oracle.com/data-centers/abilene/) (accessed 2026-08-27; Undated page marked information current as of January 2026; it describes live workloads and campus characteristics but not current measured load or accelerator inventory.), [MLCommons — MLPerf Inference Rules](https://github.com/mlcommons/inference_policies/blob/master/inference_rules.adoc) (accessed 2026-08-27; Living official rules at the access date; used for measurement-boundary requirements, not as a performance result for any Abilene system.)
- **site workload configuration unknown — explicit unknown.**
  - Binding: segment-local, nonphysical teaching overlay
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_model_and_workload_configuration`
  - Basis: Public disclosures say early training and inference workloads were running but do not name the model architecture, parameter count, context length, precision, quantization, or input/output distribution.
  - Scope: Abilene training and inference workloads
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.)
  - Unknown — not established by the cited evidence
  - Fact: `commercial_compute:abilene_inference_batching_configuration`
  - Basis: Public disclosures do not publish batch size, concurrency, queue delay, latency service level, software stack, or scale efficiency.
  - Scope: Abilene inference workloads
  - Boundary: `unverified_null` / `operation_unknown` / as of 2026-08-27
  - Sources: [OpenAI — Stargate advances with 4.5 GW partnership with Oracle](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) (accessed 2026-08-27; Dated disclosure that Oracle delivered the first NVIDIA GB200 racks and OpenAI had begun early training and inference workloads at Abilene.), [NVIDIA — Triton Inference Server 2.59.1 - Batchers](https://docs.nvidia.com/deeplearning/triton-inference-server/archives/triton-inference-server-2591/user-guide/docs/user_guide/batcher.html) (accessed 2026-08-27; Versioned official runtime documentation; used to establish that batching configuration changes throughput and latency.)

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
