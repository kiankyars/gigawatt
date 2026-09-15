# Read a power train as a set of jobs

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d04-read-the-power-train`, then run `uv run gigawatt-expand`.

**6. Campus and building power distribution · Authored draft**

Learn to read a generic single-line diagram by equipment function, then reconcile IT and auxiliary demand against two independent limits.

**Driving question:** What changes, branches, and limits between the campus connection and the rack?

## Follow one line without mistaking it for one wire

A single-line diagram simplifies an electrical system so you can see its connections and major equipment. One drawn line may represent a multiphase circuit, not one physical conductor. Symbols stand for equipment whose ratings and detailed wiring live in other documents. Begin by locating the source boundary, then follow the path to the load. Read branches as separate connected loads or alternative routes, and check the legend before interpreting an unfamiliar symbol.

A transformer changes AC voltage and current while transferring power, with losses. It does not by itself turn AC into DC. Switching equipment establishes or interrupts connections. Protection uses measurements and defined logic to detect conditions requiring isolation, then acts through a suitable interrupting device. Metering reports quantities at a particular point. Switchgear or switchboards can package several of these functions; the enclosure name alone does not tell you the complete protection scheme.

In a generic building path, upstream service supplies transformation and distribution equipment, a UPS where the selected loads require it, and downstream conductors or busway to rack connections. A busway is a distribution assembly using bus conductors rather than a loose synonym for the entire power system. A PDU distributes power to multiple loads and may include other functions in a particular product. Inspect the specified function rather than assuming every device called a PDU has the same voltage conversion or topology.

Mark the auxiliary branches. Pumps, cooling equipment, controls, and building services draw power too. Some may connect through a different continuity path from the main IT load. Their location matters both to the energy account and to the outage account. Moving them off the IT branch does not make their consumption disappear from the facility meter.

## Two limits can leave the same small margin

Consider an original phase-opening scenario. The available facility service is 6.0 MW. The IT branch can deliver 4.8 MW at its output boundary. Actual IT demand is 4.6 MW, declared upstream electrical losses are 0.2 MW, and all other facility demand is 1.0 MW. The facility input is 4.6 + 0.2 + 1.0 = 5.8 MW. There is 0.2 MW of arithmetic service headroom and 0.2 MW of IT-branch headroom, but they exist at different boundaries.

A team proposes another 0.5 MW of IT. The supplied expansion estimate also adds 0.1 MW of auxiliaries and 0.02 MW of electrical losses. The facility requirement becomes 5.8 + 0.5 + 0.1 + 0.02 = 6.42 MW, exceeding the 6.0 MW service. The IT requirement becomes 5.1 MW, exceeding the 4.8 MW branch. Upgrading only the utility service would leave the downstream branch problem unresolved.

Now suppose the service upgrade raises the facility limit to 10 MW, while the IT branch remains unchanged. A large number at the top of the diagram does not travel through a narrower downstream interface by arithmetic permission. The 5.1 MW IT request still fails the stated branch limit. Each segment must carry the load that passes through it, and each limit must be compared with demand at the same electrical boundary.

The loss entries here are supplied scenario estimates, not a constant-loss model valid at every load. A real extension requires an appropriate efficiency and thermal account for its operating point. The example's purpose is to prevent double counting and reveal separate constraints, not to select conductors or equipment from a few real-power totals.

## Read the diagram in a changed operating state

Return to the initial 4.6 MW IT state, but let a hot-weather scenario raise auxiliary demand from 1.0 to 1.4 MW while the supplied 0.2 MW loss estimate stays fixed. Facility input becomes 6.2 MW, exceeding the original 6.0 MW service even though the IT branch still carries only 4.6 MW. A rack-level limit has not changed, yet the wider system can no longer support the same combination of loads within its stated capacity.

This is why a static picture needs an operating condition. A normal-state line can disappear after a fault; an alternate supply can have a different rating; a cooling branch can demand more power in another climate condition. Annotate the chosen state before tracing what survives. A closed loop in the drawing is not evidence that every connection can be closed simultaneously, and an open switching symbol is not a field instruction.

Centralized infrastructure can simplify shared equipment and measurement, but it can also create a dependency serving many downstream loads. Splitting equipment can limit the affected group while adding interfaces and coordination work. You cannot choose between these layouts by counting boxes. Identify the service each box supports, the common elements still present, and the failure or maintenance condition being tested.

A good reading exercise ends with questions, not just labels. Which load does this meter include? Which component changes voltage? Which device can interrupt this circuit under the specified conditions? Where does the cooling pump obtain power? Which upstream limit still binds after a downstream upgrade? Answering those questions makes unfamiliar diagrams readable without pretending that a simplified course drawing is a complete engineered installation.

## Compass: package two electrical jobs together

Siemens and Compass jointly developed the custom modular medium-voltage skid. Siemens supplies the factory-built switchgear-and-transformer package; Compass is the data-center customer, not a Siemens catalog family. Its two functions remain distinct: switchgear makes and protects connections, while the transformer changes AC voltage. The original Siemens photograph shows the switchgear portion. The transformer is not visible in that photograph.

## Compass: co-design the electrical package

Siemens and Compass jointly developed a prefabricated medium-voltage skid that combines switchgear and a transformer. The Chapter 6 lead-in identifies the two electrical jobs and the interfaces agreed when they share a package: voltage and current, protection and physical connections. The following case photograph shows the switchgear portion in the factory; the transformer is not visible.

This case stays with distribution because packaging does not remove the separate switching, protection and voltage-conversion functions. The design, procurement and commissioning chapter can return to the same package for manufacturing strategy, site work, transport, ownership and release evidence. No new schedule-saving or deployment-count claim follows from the drawing.

## Fujitsu: put flexible circuits beside the load

A Starline case study, first published in December 2018, describes an extension to a Fujitsu-managed 3.2 MW data center north of London. Existing racks used cables under a raised floor. The extension adopted 250 A Track Busway overhead so the floor remained available for cooling, with wired or wireless metering options at tap-offs. The electrical consequence is a shared bus with local branch connections. A new branch can be easier to place without creating additional current capacity in the end feed.

## Count current toward the end feed

The slides use a separate row example with balanced 415 V line-to-line AC, power factor one, and a supplied 250 A usable current budget. Three 40 kW racks demand about 167 A at the end feed; four demand 223 A. Each branch remains about 56 A. After each tap, a downstream bus segment carries only the loads beyond it. The interactive fifth-rack state demands about 278 A at the end feed and exceeds the supplied budget. These are teaching inputs, not Fujitsu operating measurements or a conductor-sizing result.

## Trace the path through both transformer stages

The interactive teaching network uses 345 kV at the campus grid connection, 34.5 kV across campus distribution and a 480 V building bus. IT and cooling branch from that bus; the future hall has a separate open medium-voltage feeder. Selecting a load highlights every upstream stage.

The teaching sequence preserves this network while moving into detail: the first repeated overview outlines the medium-voltage switchgear, followed by the switchgear cutaway. The second outlines the 480 V AC connection from the hall transformer into the building bus, followed by the expanded physical-conductor drawing. Returning to the same arrangement keeps each component located in the whole path.

The high-voltage reference follows Abilene’s expansion: Mortenson distinguishes the initial 200 MW / 138 kV connection from the later 1 GW / 345 kV expansion and reports all five expansion transformers energized by March 10, 2026. The Longhorn review drawing filed with TCEQ separately labels an underground Lancium 34.5 kV feed. That December 4, 2024 drawing is marked not for construction. Together these sources support the course’s reference voltages, not a complete as-built 345/34.5 kV ratio for every campus transformer. The hall-level 480 V arrangement remains a teaching example. 34.5 kV is one nominal medium-voltage level, not the definition of the entire MV range.

## Inside the switchgear: sensing, decision and interruption

The slide uses the supplied labeled Siemens NXAirS cutaway, with the breaker, earthing-switch and cable-connection leader endpoints corrected against catalog HA 1702, page 12. The vacuum interrupters sit in the right-hand withdrawable circuit-breaker assembly. The lower-left cable terminations and the adjacent earthing-switch mechanism are different components. The upper-left busbars and upper-right low-voltage controls retain their labels. This product family is rated up to 12 kV and is separate from the 34.5 kV campus example and the Compass 8DJH 36 skid.

A breaker-based feeder assembly separates the power path from its control path. The bus and breaker conduct feeder current. A current transformer supplies a scaled measurement to a protection relay. If the protection criteria are met, the relay commands the breaker to trip. Contacts and an interrupting chamber must then stop the power current. A recorded trip command therefore does not prove successful interruption: continuing fault current can trigger breaker-failure or other backup protection and enlarge the interrupted area. The course diagram is conceptual; actual switching devices, sensors and protection arrangements vary.

## CT and CVT: measuring current and voltage

The current transformer (CT) surrounds or forms part of the phase-current path. Its secondary supplies a scaled current signal to the relay. This is measurement, not delivery of the feeder’s load power to the relay. A voltage transformer (VT) supplies a scaled voltage measurement; MV switchgear can use inductive VTs or voltage sensors.

At a high-voltage connection, a capacitor voltage transformer (CVT) uses a capacitive divider and an electromagnetic unit to obtain the voltage signal. It connects from phase to earth, in parallel with the power circuit. Hitachi’s CPB family covers 72–800 kV and provides a concrete manufacturer reference for the slide’s conceptual 345 kV measurement view; no specific Abilene instrument-transformer model is asserted.

The slide’s CT provides current, its CVT provides voltage, and the relay can use the measurements needed by its protection function. The first three states demonstrate an overcurrent trip using CT current; such a function does not require a CVT. Other functions use voltage as well. The relay sends a separate trip signal to the breaker, whose interrupter must stop the power current. Chapter 7 develops fault zones, grounding and AC/DC interruption; detailed protection settings, instrument-transformer saturation and transient-response studies are beyond this course’s scope.

## Disconnector, breaker and surge arrester are different functions

The illustrated air-insulated disconnector provides an air gap and is not assigned fault-current interruption. A switch-disconnector or breaker-disconnector combines functions only when its ratings provide them. A metal-oxide surge arrester instead responds to overvoltage: its nonlinear resistance falls, allowing surge current to be diverted and limiting insulation stress. It is commonly connected from phase to earth. A surge arrester is not an alternate power source or an isolating switch. The slides distinguish these jobs before Chapter 7 examines fault zones and alternate supply paths.

## Read N, PE and 480Y/277 before following a branch

In 480Y/277 V notation, Y identifies a wye-connected system: 480 V RMS is measured between phases, while 277 V RMS is measured from one phase to neutral. N means neutral; PE means protective earth. Neutral can carry return current for phase-to-neutral loads. Protective earth connects exposed conductive parts into the protective arrangement, rather than being another phase. A single-line diagram compresses the multiphase circuit into a readable path; it is not a count of physical wires.

The paired drawings use the same switchboard-to-rack-PDU circuit: one electrical line on the left, three phase conductors plus neutral and protective earth on the right. Five conductors belong to this chosen example, not every AC circuit. The phase-to-phase voltage is the phase-to-neutral voltage multiplied by √3, so 480Y/277 V is consistent; a 400 V wye system would instead be approximately 400Y/230 V.

## A real transformer operating range is separate from taps

The Primer now shows Schneider Electric’s Phaseo ABL6TS25B, a 250 VA controls transformer. Its datasheet specifies 360–440 V input on the nominal 400 V connection, or 207–253 V on the 230 V connection, with a 47–63 Hz frequency range. Its secondary is rated 24 V AC; that is not a promise of regulated output throughout the input range. The separate ±15 V compensation taps and dielectric test voltage are not the input-voltage limits. These published limits apply to this controls-scale product, not automatically to a medium-voltage hall transformer.

## Transformer taps change the connected turns

A fixed-ratio transformer passes a source-voltage change through to its output. Hammond Power Solutions illustrates 480 V across 80 primary turns and 120 V across 20 secondary turns. With those same turns connected, 504 V at the primary gives 126 V at the secondary. A 504 V tap connects 84 primary turns; the same 20 secondary turns then receive 120 V. The tap changes the ratio by choosing how much of the winding is connected. These are configured connections, not an automatic voltage regulator. The selected equipment determines the allowed connections and procedures.

A separate supplied photograph then shows real winding connections: several bolted terminals are visible on each of three windings, and the supplied red marking identifies one attached lead. The photographed transformer has no provided model or connection schedule; its numerical ratios are not inferred from the earlier Hammond example.

## Where conversion placement is taught

Chapter 6 follows normal AC distribution through switchgear, building branches and row busway. The Primer introduces transformers and a real input range; Chapter 6 teaches taps. Chapter 7 develops continuity and fault response. Chapter 8 owns the rectification-placement, solid-state-transformer and 800 V transition sequence, including the historical Green Zurich-West 380 V DC case. The D04.3 conversion-placement objective is taught there rather than repeated in Chapter 6. Conventional building auxiliaries can still require AC when compatible IT is supplied with DC.

## A PDU name does not specify a transformation ratio

A floor PDU distributes branches and may include an isolation/step-down transformer, metering and protection. A rack PDU distributes an existing supply to outlets. A PSU converts AC to the DC needed by its load. The slide compares these jobs without prescribing universal voltages. As a concrete counterexample to a universal 480-to-208 V claim, Schneider’s Galaxy 1000 kVA PDU accepts 480 V three-phase and supplies 400 or 415 V, according to its May 2026 product article.

## When backup protection widens the interruption

Hall A and Hall B share an incoming breaker and bus, with one outgoing feeder breaker per hall. A fault occurs on Hall A’s feeder. The relay issues a trip, but that feeder breaker fails to interrupt. The exercise asks which load connections upstream backup must disconnect: opening the incoming breaker removes the continuing fault current and also disconnects Hall B, despite no local fault there. A separate healthy feeder does not create an independent upstream supply. Chapter 7 continues from this shared dependency to UPS systems, alternate paths and the cooling loads needed to preserve service.

## Worked example: Opening a phase with two electrical constraints

- Service and IT-branch limits are usable real-power limits supplied for this scenario.
- Auxiliaries exclude IT, and electrical losses are separately supplied estimates.

1. Existing facility demand — 4.6 + 0.2 + 1.0 = 5.8 MW — IT, losses, and auxiliaries are distinct categories.
2. Proposed facility demand — 5.8 + 0.5 + 0.1 + 0.02 = 6.42 MW — Account for the support load and added loss as well as new IT.
3. Service exceedance — 6.42 − 6.0 = 0.42 MW — The requested combination exceeds the upstream limit.
4. IT-branch exceedance — 4.6 + 0.5 − 4.8 = 0.30 MW — The downstream branch also fails, independently of the service upgrade.

**Result:** The extension requires resolving both service and IT-branch constraints.

**Model boundary:** These supplied MW limits are not transformer kVA ratings or an equipment-sizing prescription.

## The tradeoff

Choice: Share a larger distribution component across several load groups.

Benefit: It can consolidate equipment and simplify a common upstream interface.

Cost: The shared element can become a larger common dependency and must be evaluated under maintenance and faults.

## When the situation changes

Trigger: Upgrade only the 6 MW service to 10 MW.

Mechanism: The 4.8 MW downstream branch still cannot deliver the proposed 5.1 MW IT demand.

Response: Trace the complete path and resolve each binding interface.

## Apply the idea

At the original IT demand, auxiliaries rise to 1.4 MW. What limit fails first in the stated ledger?

<details>
<summary>Reveal the worked answer</summary>

The service limit fails: 4.6 + 0.2 + 1.4 = 6.2 MW exceeds 6.0 MW.

The IT branch remains below 4.8 MW. The increased support load matters at the wider facility boundary.

</details>

**The idea to keep:** A power train is a connected set of interfaces and constraints, not a list of equipment names.

## Sources and reading boundaries

- [DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) — A data-center distribution path contains several electrical functions and auxiliary loads. Read 2026-09-06. Read electrical-system sections 6.1–6.3. No historical voltage example or universal efficiency claim from the guide is applied to this synthetic path.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — Phased infrastructure acceptance must preserve the scope of what was tested and handed over. Read 2026-09-06. Read the public ASHRAE framework discussion; the numerical opening plan is original.
- [Siemens — Compass Datacenters integrated MV skid](https://www.siemens.com/en-us/company/insights/compass-datacenters-case-study/) — Integrated MV switchgear and transformer skid; case photograph. Read 2026-09-13. Public project-page text and original product photograph reviewed. The photo shows switchgear in the factory; transformer is not visible. Product name 8DJH 36 is not an asserted operating voltage. No deployment count or quantified saving adopted.
- [Siemens and Compass sign modular electrical solution agreement](https://press.siemens.com/global/en/pressrelease/siemens-and-compass-datacenters-sign-multi-year-custom-electrical-solution-agreement) — Partnership and integrated electrical functions. Read 2026-09-13. December 2024 announcement reviewed. Its planned first deployment and up-to-1,500-unit agreement are not used as installed capacity or completed deliveries.
- [Fujitsu selects Starline Track Busway for data centre expansion](https://starlinepower.com/sites/default/files/files/starline_busway_fujitsu-case-study_US.pdf) — Fujitsu expansion problem and chosen overhead busway. Read 2026-09-13. Both PDF pages read and photographs inspected. Published December 2018; file revised January 2020. Site is described only as north of London. 3.2 MW describes the existing managed facility; no added MW is stated. Case photographs have no capture metadata. Row currents in slides are separate original 415 V examples.
- [Oracle Data Centers: Abilene, Texas](https://www.oracle.com/data-centers/) — Dated recurring-campus photograph only. Read 2026-09-13. Read Abilene location section and matched original July 15, 2026 data-hall aerial. Photograph does not establish one-line topology, voltage, branch ratings or operating demand. Chapter6 does not repeat the delivered-capacity percentage.
- [Schneider Electric — Phaseo ABL6TS25B product datasheet](https://iportal.se.com/Contents/docs/SQD-ABL6TS25B_DATASHEET.PDF) — A named 250 VA controls transformer specifies 360–440 V input limits for its nominal 400 V connection, 207–253 V for its 230 V connection, and 47–63 Hz network frequency limits. The secondary rating is 24 V AC. Read 2026-09-13. PDF page 1 ratings and input limits inspected; page 5 wiring visually inspected and shows separate ±15 V compensation taps. Not a hall or campus MV transformer, not a guarantee of regulated secondary voltage across the input range, and not an insulation withstand rating. Product datasheet dated February 26, 2020; no claim of current delivery or installed campus use.
- [Schneider Electric — Elementary switching devices](https://www.electrical-installation.org/enwiki/Elementary_switching_devices) — Plain disconnector isolation versus switching/interrupting capability; combined devices have separately rated duties. Read 2026-09-13. Full public page reviewed. Conceptual functions only, not operation or installation instructions.
- [Siemens — Vacuum Switching Technology and Components](https://support.industry.siemens.com/cs/attachments/109745538/HG11.01_EN_20190603.pdf) — Metal-oxide surge arresters become conductive during overvoltage and divert surge current, commonly phase to earth. Read 2026-09-13. Public indexed catalog passage on page 30 reviewed; direct PDF open failed. No ratings or internal construction are copied into the conceptual diagram.
- [Siemens — SIPROTEC 7SD610 circuit breaker failure protection](https://support.industry.siemens.com/cs/attachments/109743409/7SD610_Manual_A8_V044100_en.pdf) — A feeder protection relay issues a trip; persistent fault current after the command can require backup interruption by other breakers. Read 2026-09-13. Public indexed section 2.13 reviewed. Course omits timing values, configuration instructions and a specific installed topology.
- [Schneider Electric — Transformer secondary voltage notation](https://acespex.se.com/rpt/prodhelp.php?doc=pms_0044&grp=spex_pms&host=CTW&ndx=21283) — 480Y/277 gives the wye phase-to-phase voltage followed by the phase-to-neutral voltage. Read 2026-09-13. Published short technical entry reviewed. Conductor selection and grounding system are not prescribed.
- [Siemens — NXAirS medium-voltage switchgear HA 1702 sectional illustration](https://cache.industry.siemens.com/dl/files/485/109972485/att_1290488/v1/1702_NXAirS_12kV_Catalogue_EN_final.pdf) — Real panel compartments and original manufacturer sectional illustration. Read 2026-09-14. 2024 A catalog page 12 visually reviewed; original embedded images extracted with transparency. This up-to-12-kV product example is distinct from the 34.5-kV teaching circuit and Compass 8DJH 36 skid.
- [Schneider Electric — Galaxy PDU 1000 kVA distribution voltages](https://blog.se.com/datacenter/2026/05/18/solving-densification-power-distribution-metering-high-performance-computing/) — Floor-PDU output voltage is product-specific: Galaxy 1000 kVA uses 480 V input and 400 or 415 V output. Read 2026-09-14. Official May 18, 2026 product article reviewed. Product configuration example, not universal PDU behavior or an installed-campus voltage claim.
- [Hammond Power Solutions — How Taps Work](https://americas.hammondpowersolutions.com/news/2014/april/how-taps-work) — 480:120 V turns example and 504 V primary tap using 84 primary turns rather than 80. Read 2026-09-14. Instructional turns-ratio example. No claim of automatic regulation or universal transformer operating limits.
- [Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) — Original 200 MW / 138 kV grid connection and later 1 GW / 345 kV expansion; five expansion transformers energized by March 10, 2026. Read 2026-09-14. September 14 recheck: historical energization milestones, not measured IT demand or a complete 345/34.5 kV as-built one-line. October 2026 temporary-transformer replacement remains a stated plan.
- [Longhorn power plant review drawing — Lancium 34.5 kV feed](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) — Project-specific 34.5 kV campus-feed reference. Read 2026-09-14. PDF page 89, drawing 5MECH-00001-GA rev D, reissued December 4, 2024 and marked not for construction. Labels an underground Lancium 34.5 kV feed by others. Does not establish an entire as-built campus transformer ratio.
- [Hitachi Energy — CPB capacitor voltage transformer, 72–800 kV](https://www.hitachienergy.com/products-and-solutions/instrument-transformers/voltage-transformers/cpb-72-800-kv) — HV capacitor voltage transformer, phase-to-ground measurement for protection and metering. Read 2026-09-14. Product family supports the conceptual 345 kV CVT teaching placement; no installed Abilene model is identified.
- [ABB — Protection criteria for medium voltage networks](https://library.e.abb.com/public/76afab5a1dd44f438409aa65c990ed8b/AP_Protection%20criteria%20MV(EN)C-_1VCP000280-01.2017.pdf) — CT/VT scaling and separation of measurement, relay decision and power-current interruption. Read 2026-09-14. Chapter 4, printed pages 11–14: instrument transformers. Teaching diagram omits wiring, CT saturation, relay settings and detailed CVT transient behavior.
