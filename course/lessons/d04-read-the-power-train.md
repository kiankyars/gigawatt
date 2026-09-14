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

Siemens and Compass co-developed a medium-voltage skid containing switchgear and a transformer. The factory package makes a repeatable interface, while its electrical functions remain distinct: switchgear connects and isolates circuits; the transformer changes AC voltage. The project photograph shows the switchgear portion. Neither the 8DJH 36 family name nor the skid exterior supplies the operating voltage and usable rating of an installed campus path.

## Fujitsu: put flexible circuits beside the load

A Starline case study, first published in December 2018, describes an extension to a Fujitsu-managed 3.2 MW data center north of London. Existing racks used cables under a raised floor. The extension adopted 250 A Track Busway overhead so the floor remained available for cooling, with wired or wireless metering options at tap-offs. The electrical consequence is a shared bus with local branch connections. A new branch can be easier to place without creating additional current capacity in the end feed.

## Count current toward the end feed

The slides use a separate row example with balanced 415 V line-to-line AC, power factor one, and a supplied 250 A usable current budget. Three 40 kW racks demand about 167 A at the end feed; four demand 223 A. Each branch remains about 56 A. After each tap, a downstream bus segment carries only the loads beyond it. The interactive fifth-rack state demands about 278 A at the end feed and exceeds the supplied budget. These are teaching inputs, not Fujitsu operating measurements or a conductor-sizing result.

## Return to Abilene with the right evidence

Oracle’s July 15, 2026 data-hall aerial locates the recurring original Abilene campus. Use a building in that image to pose the distribution question: which feeder, transformer, bus and branch supplies its IT and supporting equipment? The image cannot answer its one-line topology, voltage or ratings. The following campus model therefore supplies explicit 13.8 kV and 480 V interfaces to practice tracing a complete load path.

## Inside the switchgear: sensing, decision and interruption

A breaker-based feeder assembly separates the power path from its control path. The bus and breaker conduct feeder current. A current transformer supplies a scaled measurement to a protection relay. If the protection criteria are met, the relay commands the breaker to trip. Contacts and an interrupting chamber must then stop the power current. A recorded trip command therefore does not prove successful interruption: continuing fault current can trigger breaker-failure or other backup protection and enlarge the interrupted area. The course diagram is conceptual; actual switching devices, sensors and protection arrangements vary.

## Disconnector, breaker and surge arrester are different functions

A plain disconnector provides an isolation gap and is not assigned fault-current interruption. A switch-disconnector or breaker-disconnector combines functions only when its ratings provide them. A metal-oxide surge arrester instead responds to overvoltage: its nonlinear resistance falls, allowing surge current to be diverted and limiting insulation stress. It is commonly connected from phase to earth. A surge arrester is not an alternate power source or an isolating switch. The slides distinguish these jobs before Chapter 7 examines fault zones and alternate supply paths.

## Read N, PE and 480Y/277 before following a branch

In 480Y/277 V notation, Y identifies a wye-connected system: 480 V RMS is measured between phases, while 277 V RMS is measured from one phase to neutral. N means neutral; PE means protective earth. Neutral can carry return current for phase-to-neutral loads. Protective earth connects exposed conductive parts into the protective arrangement, rather than being another phase. A single-line diagram compresses the multiphase circuit into a readable path; it is not a count of physical wires.

## A real transformer operating range is separate from taps

The Primer now shows Schneider Electric’s Phaseo ABL6TS25B, a 250 VA controls transformer. Its datasheet specifies 360–440 V input on the nominal 400 V connection, or 207–253 V on the 230 V connection, with a 47–63 Hz frequency range. Its secondary is rated 24 V AC; that is not a promise of regulated output throughout the input range. The separate ±15 V compensation taps and dielectric test voltage are not the input-voltage limits. These published limits apply to this controls-scale product, not automatically to a medium-voltage hall transformer.

## Where conversion placement is taught

Chapter 6 follows normal AC distribution through switchgear, building branches and row busway. The Primer teaches the transformer ratio, taps and a real input range. Chapter 7 develops continuity and fault response. Chapter 8 owns the rectification-placement, solid-state-transformer and 800 V transition sequence, including the historical Green Zurich-West 380 V DC case. The D04.3 conversion-placement objective is taught there rather than repeated in Chapter 6. Conventional building auxiliaries can still require AC when compatible IT is supplied with DC.

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
