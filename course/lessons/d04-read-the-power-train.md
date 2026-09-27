# Read a power train as a set of jobs

**6. Campus and building power distribution**

Learn to read a generic single-line diagram by equipment function, then reconcile information technology (IT) and auxiliary demand against two independent limits.

**Driving question:** What changes, branches, and limits between the campus connection and the rack?

## Follow one line without mistaking it for one wire

A single-line diagram simplifies an electrical system so you can see its connections and major equipment. One drawn line may represent a multiphase circuit, not one physical conductor. Symbols stand for equipment whose ratings and detailed wiring live in other documents. Begin by locating the source boundary, then follow the path to the load. Read branches as separate connected loads or alternative routes, and check the legend before interpreting an unfamiliar symbol.

A transformer changes alternating-current (AC) voltage and current while transferring power, with losses. It does not by itself turn AC into direct current (DC). Switching equipment makes or interrupts connections. Protection uses measurements and defined logic to detect conditions requiring isolation, then acts through a suitable interrupting device. Metering reports quantities at a particular point. Switchgear or switchboards can package several of these functions; the enclosure name alone does not tell you the complete protection scheme.

In a generic building path, upstream service supplies transformation and distribution equipment, an uninterruptible power supply (UPS) where the selected loads require it, and downstream conductors or busway to rack connections. A busway is a distribution assembly using bus conductors rather than a loose synonym for the entire power system. A power distribution unit (PDU) distributes power to multiple loads and may include other functions in a particular product. Inspect the specified function rather than assuming every device called a PDU has the same voltage conversion or topology.

Mark the auxiliary branches. Pumps, cooling equipment, controls, and building services draw power too. Some may connect through a different continuity path from the main IT load. Their location matters both to the energy account and to the outage account. Moving them off the IT branch does not make their consumption disappear from the facility meter.

## Two limits can leave the same small margin

Consider a phase-opening scenario. The available facility service is 6.0 megawatts (MW). The IT branch can deliver 4.8 MW at its output boundary. Actual IT demand is 4.6 MW, declared upstream electrical losses are 0.2 MW, and all other facility demand is 1.0 MW. The facility input is 4.6 + 0.2 + 1.0 = 5.8 MW. There is 0.2 MW of arithmetic service headroom and 0.2 MW of IT-branch headroom, but they exist at different boundaries.

A team proposes another 0.5 MW of IT. The expansion estimate also adds 0.1 MW of auxiliaries and 0.02 MW of electrical losses. The facility requirement becomes 5.8 + 0.5 + 0.1 + 0.02 = 6.42 MW, exceeding the 6.0 MW service. The IT requirement becomes 5.1 MW, exceeding the 4.8 MW branch. Upgrading only the utility service would leave the downstream branch problem unresolved.

Now suppose the service upgrade raises the facility limit to 10 MW, while the IT branch remains unchanged. A large number at the top of the diagram does not travel through a narrower downstream interface by arithmetic permission. The 5.1 MW IT request still fails the stated branch limit. Each segment must carry the load that passes through it, and each limit must be compared with demand at the same electrical boundary.

The loss entries here are estimates for this scenario, not a constant-loss model valid at every load. A real extension requires an appropriate efficiency and thermal account for its operating point. The example's purpose is to prevent double counting and reveal separate constraints, not to select conductors or equipment from a few real-power totals.

## Read the diagram in a changed operating state

Return to the initial 4.6 MW IT state, but let a hot-weather scenario raise auxiliary demand from 1.0 to 1.4 MW while the 0.2 MW loss estimate stays fixed. Facility input becomes 6.2 MW, exceeding the original 6.0 MW service even though the IT branch still carries only 4.6 MW. A rack-level limit has not changed, yet the wider system can no longer support the same combination of loads within its stated capacity.

This is why a static picture needs an operating condition. A normal-state line can disappear after a fault; an alternate supply can have a different rating; a cooling branch can demand more power in another climate condition. Annotate the chosen state before tracing what survives. A closed loop in the drawing is not evidence that every connection can be closed simultaneously, and an open switching symbol is not a field instruction.

Centralized infrastructure can simplify shared equipment and measurement, but it can also create a dependency serving many downstream loads. Splitting equipment can limit the affected group while adding interfaces and coordination work. You cannot choose between these layouts by counting boxes. Identify the service each box supports, the common elements still present, and the failure or maintenance condition being tested.

A good reading exercise ends with questions, not just labels. Which load does this meter include? Which component changes voltage? Which device can interrupt this circuit under the specified conditions? Where does the cooling pump obtain power? Which upstream limit still binds after a downstream upgrade? Answering those questions makes unfamiliar diagrams readable without pretending that a simplified course drawing is a complete engineered installation.

## Compass: co-design one electrical package

Siemens and Compass jointly developed a custom prefabricated medium-voltage skid that combines switchgear and a transformer. Siemens supplies the factory-built package; Compass is the data-center customer, not a Siemens catalog family. Sharing a package means agreeing the interfaces between the two jobs: voltage and current, protection and physical connections.

The two functions stay distinct inside one package: switchgear makes and protects connections, while the transformer changes AC voltage. The factory photograph below shows the switchgear portion; the transformer is out of view. The engineering, procurement and construction (EPC) chapter returns to the same package for manufacturing strategy, site work, transport, ownership and release evidence.

![Siemens medium-voltage switchgear for the Compass skid in a factory hall: a row of panel fronts with controls above and cable connections below.](../assets/references/distribution-compass-switchgear.jpg)

Switchgear portion of the jointly developed Compass skid, in the factory. The transformer is out of view. [Siemens, Compass Datacenters case study](https://www.siemens.com/en-us/company/insights/compass-datacenters-case-study/)

## Fujitsu: put flexible circuits beside the load

A Starline case study, first published in December 2018, describes an extension to a Fujitsu-managed 3.2 MW data center north of London. Existing racks used cables under a raised floor. The extension adopted 250 A Track Busway overhead so the floor remained available for cooling, with wired or wireless metering options at tap-offs. The electrical consequence is a shared bus with local branch connections. A new branch can be easier to place without creating additional current capacity in the end feed.

## Count current toward the end feed

Take a separate row example with balanced 415 V line-to-line AC, power factor one, and a 250 A usable current budget at the end feed. Three 40 kW racks demand about 167 A at the end feed; four demand 223 A. Each branch remains about 56 A. After each tap, a downstream bus segment carries only the loads beyond it. A fifth rack raises the end-feed current to about 278 A, over the budget. These currents are not Fujitsu operating measurements or a conductor-sizing result.

## Trace the path through both transformer stages

Take a reference network with 345 kV at the campus grid connection, 34.5 kV across campus distribution and a 480 V building bus. IT and cooling branch from that bus; the future hall has a separate open medium-voltage feeder. Every load traces back through each upstream stage.

Two parts of this network deserve a closer look: the medium-voltage switchgear, and the 480 V AC connection from the hall transformer into the building bus. The next sections take each in turn.

The high-voltage reference follows Abilene’s expansion: Mortenson distinguishes the initial 200 MW / 138 kV connection from the later 1 gigawatt (GW) / 345 kV expansion and reports all five expansion transformers energized by March 10, 2026. The Longhorn review drawing filed with the Texas Commission on Environmental Quality (TCEQ) separately labels an underground Lancium 34.5 kV feed. That December 4, 2024 drawing is marked not for construction. Together these sources support the reference voltages used here, not a complete as-built 345/34.5 kV ratio for every campus transformer. The hall-level 480 V bus belongs to the reference network rather than to these sources. 34.5 kV is one nominal medium-voltage (MV) level, not the definition of the entire MV range.

## Inside the switchgear: sensing, decision and interruption

Siemens’s sectional drawing of one NXAirS panel, from catalog HA 1702, page 12, shows how the parts are arranged; it appears below. The withdrawable circuit breaker fills the middle of the panel, and the brown upright pole just right of the central frame houses a vacuum interrupter. The busbars sit in their own compartment at upper left, under a yellow pressure-relief duct, and the low-voltage controls sit in a cabinet at upper right. The cable terminations at lower left and the earthing switch beside them are different components. This product family is rated up to 12 kV and is separate from the 34.5 kV campus example and the Compass 8DJH 36 skid.

A breaker-based feeder assembly separates the power path from its control path. The bus and breaker conduct feeder current. A current transformer supplies a scaled measurement to a protection relay. If the protection criteria are met, the relay commands the breaker to trip. Contacts and an interrupting chamber must then stop the power current. A recorded trip command therefore does not prove successful interruption: continuing fault current can trigger breaker-failure or other backup protection and enlarge the interrupted area. Actual switching devices, sensors and protection arrangements vary by design.

![Unlabeled section drawing of a Siemens NXAirS circuit-breaker panel: a yellow pressure-relief duct across the top, the busbar compartment below it at upper left, a gray low-voltage cabinet at upper right, the withdrawable circuit breaker with a brown vacuum-interrupter pole in the middle, and a red current transformer above brown cable connections and a ribbed insulator at lower left.](../assets/references/distribution-siemens-nxairs-cutaway.png)

Section through one Siemens NXAirS circuit-breaker panel, rated up to 12 kV. The catalog’s numbered callouts are not part of this image. [Siemens, NXAirS catalog HA 1702, page 12](https://cache.industry.siemens.com/dl/files/485/109972485/att_1290488/v1/1702_NXAirS_12kV_Catalogue_EN_final.pdf#page=12)

## CT and CVT: measuring current and voltage

The current transformer (CT) surrounds or forms part of the phase-current path. Its secondary supplies a scaled current signal to the relay. This is measurement, not delivery of the feeder’s load power to the relay. A voltage transformer (VT) supplies a scaled voltage measurement; MV switchgear can use inductive VTs or voltage sensors.

At a high-voltage connection, a capacitor voltage transformer (CVT) uses a capacitive divider and an electromagnetic unit to obtain the voltage signal. It connects from phase to earth, in parallel with the power circuit. Hitachi Energy’s CPB family, for example, covers 72–800 kV, a range that includes this network’s 345 kV connection.

Here the CT provides current and the CVT provides voltage, and the relay uses the measurements its protection function needs. An overcurrent trip uses CT current alone and needs no CVT. Other functions use voltage as well. The relay sends a separate trip signal to the breaker, whose interrupter must stop the power current. Chapter 7 develops fault zones, grounding and AC/DC interruption; detailed protection settings, instrument-transformer saturation and transient response need their own engineering studies.

## Disconnector, breaker and surge arrester are different functions

An air-insulated disconnector provides an isolating air gap and is not assigned fault-current interruption. A switch-disconnector or breaker-disconnector combines functions only when its ratings provide them. A metal-oxide surge arrester instead responds to overvoltage: its nonlinear resistance falls, allowing surge current to be diverted and limiting insulation stress. It is commonly connected from phase to earth. A surge arrester is not an alternate power source or an isolating switch. Chapter 7 builds on these three jobs when it examines fault zones and alternate supply paths.

## Read N, PE and 480Y/277 before following a branch

In 480Y/277 V notation, Y identifies a wye-connected system: 480 V root-mean-square (RMS) is measured between phases, while 277 V RMS is measured from one phase to neutral. N means neutral; PE means protective earth. Neutral can carry return current for phase-to-neutral loads. Protective earth connects exposed conductive parts into the protective arrangement, rather than being another phase. A single-line diagram compresses the multiphase circuit into a readable path; it is not a count of physical wires.

Draw one switchboard-to-rack-PDU circuit twice: once as a single line, and once as its physical conductors, three phases plus neutral and protective earth. Five conductors belong to this example, not every AC circuit. The phase-to-phase voltage is the phase-to-neutral voltage multiplied by √3, so 480Y/277 V is consistent; a 400 V wye system would instead be approximately 400Y/230 V.

## A real transformer operating range is separate from taps

Schneider Electric’s Phaseo ABL6TS25B is a 250 volt-ampere (VA) controls transformer. Its datasheet specifies 360–440 V input on the nominal 400 V connection, or 207–253 V on the 230 V connection, with a 47–63 Hz frequency range. Its secondary is rated 24 V AC; that is not a promise of regulated output throughout the input range. The separate ±15 V compensation taps and dielectric test voltage are not the input-voltage limits. These published limits apply to this controls-scale product, not automatically to a medium-voltage hall transformer.

## Transformer taps change the connected turns

A fixed-ratio transformer passes a source-voltage change through to its output. Hammond Power Solutions illustrates 480 V across 80 primary turns and 120 V across 20 secondary turns. With those same turns connected, 504 V at the primary gives 126 V at the secondary. A 504 V tap connects 84 primary turns; the same 20 secondary turns then receive 120 V. The tap changes the ratio by choosing how much of the winding is connected. These are configured connections, not an automatic voltage regulator. The selected equipment determines the allowed connections and procedures.

## Where conversion placement comes next

This chapter follows normal AC distribution through switchgear, building branches and row busway, with the transformer taps along the way. Chapter 7 develops continuity and fault response. Where rectification happens, including solid-state transformers and the move to 800 V DC, is the subject of “Moving a converter moves an interface”, the last lesson of this chapter, and of Chapter 9, which includes the historical Green Zurich-West 380 V DC case. Conventional building auxiliaries can still require AC when compatible IT is supplied with DC.

## A PDU name does not specify a transformation ratio

A floor PDU distributes branches and may include an isolation/step-down transformer, metering and protection. A rack PDU distributes an existing supply to outlets. A power supply unit (PSU) converts AC to the DC needed by its load. Their voltages vary by product: Schneider’s Galaxy PDU, rated 1,000 kilovolt-amperes (kVA), accepts 480 V three-phase and supplies 400 or 415 V, according to its May 2026 product article.

## When backup protection widens the interruption

Hall A and Hall B share an incoming breaker and bus, with one outgoing feeder breaker per hall. A fault occurs on Hall A’s feeder. The relay issues a trip, but that feeder breaker fails to interrupt. Upstream backup protection must then clear the fault: opening the incoming breaker removes the continuing fault current and also disconnects Hall B, despite no local fault there. A separate healthy feeder does not create an independent upstream supply. Chapter 7 continues from this shared dependency to UPS systems, alternate paths and the cooling loads needed to preserve service.

## Worked example: Opening a phase with two electrical constraints

- Service and IT-branch limits are usable real-power limits given for this scenario.
- Auxiliaries exclude IT, and electrical losses are separately given estimates.

1. Existing facility demand — 4.6 + 0.2 + 1.0 = 5.8 MW — IT, losses, and auxiliaries are distinct categories.
2. Proposed facility demand — 5.8 + 0.5 + 0.1 + 0.02 = 6.42 MW — Account for the support load and added loss as well as new IT.
3. Service exceedance — 6.42 − 6.0 = 0.42 MW — The requested combination exceeds the upstream limit.
4. IT-branch exceedance — 4.6 + 0.5 − 4.8 = 0.30 MW — The downstream branch also fails, independently of the service upgrade.

**Result:** The extension requires resolving both service and IT-branch constraints.

**Model boundary:** These MW limits are not transformer kVA ratings or an equipment-sizing prescription.

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

## Sources

- [DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) — www.energy.gov · Published 2024-07 · Reviewed 2026-09-06. A data-center distribution path contains several electrical functions and auxiliary loads.
- [Commissioning & Performance Validation | AI Data Center Energy Performance Framework](https://www.ashrae.org/technical-resources/ai-data-center-framework/commissioning-performance-validation) — ASHRAE · Reviewed 2026-09-06. Phased infrastructure acceptance must preserve the scope of what was tested and handed over.
- [Siemens — Compass Datacenters integrated MV skid](https://www.siemens.com/en-us/company/insights/compass-datacenters-case-study/) — Siemens · Reviewed 2026-09-15. Siemens and Compass’s integrated medium-voltage switchgear and transformer skid, with a factory photograph.
- [Siemens and Compass sign modular electrical solution agreement](https://press.siemens.com/global/en/pressrelease/siemens-and-compass-datacenters-sign-multi-year-custom-electrical-solution-agreement) — Siemens · Published 2024-12-04 · Reviewed 2026-09-17. Partnership and integrated electrical functions.
- [Fujitsu selects Starline Track Busway for data centre expansion](https://starlinepower.com/sites/default/files/files/starline_busway_fujitsu-case-study_US.pdf) — Starline / Legrand · Published 2018-12 · Reviewed 2026-09-13. Fujitsu expansion problem and chosen overhead busway.
- [Schneider Electric — Phaseo ABL6TS25B product datasheet](https://iportal.se.com/Contents/docs/SQD-ABL6TS25B_DATASHEET.PDF) — Schneider Electric · Published 2020-02-26 · Reviewed 2026-09-13. A named 250 VA controls transformer specifies 360–440 V input limits for its nominal 400 V connection, 207–253 V for its 230 V connection, and 47–63 Hz network frequency limits. The secondary rating is 24 V AC.
- [Schneider Electric — Elementary switching devices](https://www.electrical-installation.org/enwiki/Elementary_switching_devices) — Schneider Electric · Reviewed 2026-09-13. Plain disconnector isolation versus switching/interrupting capability; combined devices have separately rated duties.
- [Siemens — Vacuum Switching Technology and Components](https://support.industry.siemens.com/cs/attachments/109745538/HG11.01_EN_20190603.pdf) — Siemens · Reviewed 2026-09-13. Metal-oxide surge arresters become conductive during overvoltage and divert surge current, commonly phase to earth.
- [Siemens — SIPROTEC 7SD610 circuit breaker failure protection](https://support.industry.siemens.com/cs/attachments/109743409/7SD610_Manual_A8_V044100_en.pdf) — Siemens · Reviewed 2026-09-13. A feeder protection relay issues a trip; persistent fault current after the command can require backup interruption by other breakers.
- [PDHonline — Standard AC System Voltages (600 V and Less), course E427](https://www.pdhonline.com/courses/e427/e427content.pdf) — PDH Online (David A. Snyder, PE) · Reviewed 2026-09-26. 480Y/277 gives the wye phase-to-phase voltage followed by the phase-to-neutral voltage.
- [Siemens — NXAirS medium-voltage switchgear HA 1702 sectional illustration](https://cache.industry.siemens.com/dl/files/485/109972485/att_1290488/v1/1702_NXAirS_12kV_Catalogue_EN_final.pdf) — Siemens · Published 2024 · Reviewed 2026-09-26. Page 12 shows an NXAirS circuit-breaker panel in section and names its busbar, switching-device, connection and low-voltage compartments, vacuum interrupters, current transformer, cable connection and earthing switch.
- [Schneider Electric — Galaxy PDU 1000 kVA distribution voltages](https://blog.se.com/datacenter/2026/05/18/solving-densification-power-distribution-metering-high-performance-computing/) — Schneider Electric · Published 2026-05-18 · Reviewed 2026-09-14. Floor-PDU output voltage is product-specific: Galaxy 1000 kVA uses 480 V input and 400 or 415 V output.
- [Hammond Power Solutions — How Taps Work](https://americas.hammondpowersolutions.com/news/2014/april/how-taps-work) — Hammond Power Solutions · Published 2014-04-02 · Reviewed 2026-09-14. 480:120 V turns example and 504 V primary tap using 84 primary turns rather than 80.
- [Abilene Data Center Development](https://www.mortenson.com/projects/abilene-data-center-development) — Mortenson · Reviewed 2026-09-14. Original 200 MW / 138 kV grid connection and later 1 GW / 345 kV expansion; five expansion transformers energized by March 10, 2026.
- [Longhorn power plant review drawing — Lancium 34.5 kV feed](https://www.tceq.texas.gov/assets/public/permitting/air/reports/applications/37589-tc.pdf) — Abilene DC 1 / Campos, filed with TCEQ · Reviewed 2026-09-14. Project-specific 34.5 kV campus-feed reference.
- [Hitachi Energy — CPB capacitor voltage transformer, 72–800 kV](https://www.hitachienergy.com/products-and-solutions/instrument-transformers/voltage-transformers/cpb-72-800-kv) — Hitachi Energy · Reviewed 2026-09-14. HV capacitor voltage transformer, phase-to-ground measurement for protection and metering.
- [ABB — Protection criteria for medium voltage networks](https://library.e.abb.com/public/76afab5a1dd44f438409aa65c990ed8b/AP_Protection%20criteria%20MV(EN)C-_1VCP000280-01.2017.pdf) — ABB · Published 2017 · Reviewed 2026-09-26. CT/VT scaling and separation of measurement, relay decision and power-current interruption.
