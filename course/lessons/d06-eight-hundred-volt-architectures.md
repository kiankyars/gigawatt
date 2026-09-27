# 800 V is an interface, not an entire architecture

**9. 800 V DC distribution**

Compare a 480 V three-phase feeder with an 800 V DC feeder at the same 100 kW, then place the conversion in the rack, in a sidecar or farther upstream while keeping storage and protection visible.

**Driving question:** How can 800 V DC reduce distribution copper and free compute-rack space?

## Rack power keeps rising

Bank of America’s BofA Global Research forecast charts power capacity per rack across NVIDIA platform generations. It starts from a traditional server rack at 10 to 15 kW, places Grace Blackwell Ultra NVL72 (2025) at about 130 kW and Vera Rubin Ultra NVL576 (2027) at about 640 kW, and ends with Rosa Feynman (2028 and later) above 1.5 MW, nearly 100 times the traditional rack. These are analyst estimates attached to roadmap dates, not measured draw at any site.

At a fixed voltage, current rises with power: I = P ÷ V. A 1.5 MW rack fed at 50 V would need 30,000 A; at 800 V direct current (DC) it needs 1,875 A. Sixteen times the voltage carries the same power with one-sixteenth of the current, and in the same conductor the I²R heat falls by 16² = 256 times. At 50 V the currents are already large. Version 3 of the Open Compute Project (OCP) Open Rack V3 High Power Rack (ORv3 HPR V3) moves the power supplies and backup batteries into a 50 V sidecar power rack, and that design tops out at 300 kW, where its busbars carry 6,000 A. NVIDIA’s May 2025 article gives this growth toward megawatt-scale racks as the reason for 800 V DC distribution. The individual bars remain BofA’s estimates.

## Two conductors instead of three

Compare two feeders that deliver the same power to the same load. Balanced three-phase alternating current (AC) uses three current-carrying conductors; DC uses two. With equal length, cross-section and copper in every conductor, two instead of three is two-thirds of the copper: one-third less in these conductors. Neutral, protective earth, insulation and terminations sit outside that count, so it describes these conductors rather than all the copper in a facility.

The current in each conductor is nearly the same, because the AC formula spreads the power over three lines and measures voltage between two of them: I = P ÷ (√3 × V × power factor) for balanced three-phase AC, against I = P ÷ V for DC. The saving comes from the conductor count, not from a lower current per conductor. Heat follows the count as well. With the same resistance R in every conductor, the AC feeder produces 3I²R and the DC feeder 2I²R.

The lab below compares the two feeders at 100 kW with 10 mΩ per conductor: 480 V three-phase AC carries 120.3 A in each of three conductors and produces 434 W of conductor heat, while 800 V DC carries 125 A in each of two conductors and produces 312.5 W, 28% less. The difference is about 122 W, or 0.12% of the 100 kW delivered, so it is a conductor saving rather than a facility-energy saving. The worked example below takes the same comparison one step at a time.

## 800 V can mean one rail or two

An 800 V label describes one of two arrangements. A single-ended, or monopolar, bus holds one rail at 800 V against a return conductor. A bipolar bus splits the same 800 V into +400 V and −400 V rails around a grounded midpoint, written ±400 V. The load still sees 800 V across its input, so it draws the same current: 125 A at 100 kW, or 1,250 A at 1 MW.

The bipolar form keeps each rail only 400 V from ground. That lets designers use the mature 400 V-class power electronics, capacitors, connectors and fuses built for electric vehicles, the supply chain Google named when it explained its choice of 400 V at OCP’s 2025 summit for Europe, the Middle East and Africa. The price is a third power conductor, the midpoint, which must be routed, terminated and protected along the whole path. The Open Compute Project’s Diablo 400 specification, drafted by Google, Meta and Microsoft in 2025, makes ±400 V its standard configuration and allows single-ended 800 V as a design option. NVIDIA specifies 800 V DC.

Read every voltage label with the conductors it is measured between. Conductor-to-ground stress, fault cases and service interfaces follow from that choice, so a drawing should state it. An AC label needs the same care: 480 V three-phase is measured line to line, and in a 480Y/277 V wye system each phase sits about 277 V from neutral.

## Keep the three architectures separate

Conversion in the rack brings AC distribution to a compute rack, converts it to a lower-voltage DC bus, and regulates power near devices. Conversion in a sidecar retains AC distribution but moves rectification into an adjacent power rack or row unit. A higher-voltage DC connection then reaches compute racks, which contain the required downstream conversion. Conversion farther upstream starts DC distribution in a power room, potentially near the facility electrical boundary. These architectures can share a nominal DC voltage while differing in conductor lengths, maintenance zones, fault exposure and responsibility for stored energy.

The comparison becomes useful when unchanged equipment stays visible. With a sidecar, the upstream AC feeder still carries the aggregate load delivered to the row, plus conversion losses. With conversion farther upstream, a longer portion of the facility becomes a DC distribution system and must be designed accordingly. Neither arrangement determines how many storage modules, isolation stages or protective devices are required. Draw those as explicit blocks with interfaces rather than assuming that central rectification automatically replaces every uninterruptible power supply (UPS) function.

## Where the rack steps down from 800 V

An 800 V supply at the rack inlet does not require one specific voltage on the vertical rack bus. One design converts 800 V to roughly 50 V at the rack entrance, then distributes that lower voltage vertically to the trays. Rack documents give that low-voltage bus as 48, 50, 51 or 54 V depending on the platform and specification; all of them name one class of roughly 50 V rack bus, not separate conversion steps. Another carries 800 V along the vertical bus and steps it down near the trays. Both still need local conversion and regulation to supply processor rails; 800 V does not feed a processor directly.

The comparison is about how far the higher voltage travels before step-down. Retaining a roughly 50 V vertical bus is one option, not an invariant of DC-input racks. SemiAnalysis’s May 2026 forecast distinguishes rack-shelf conversion from on-blade conversion; NVIDIA’s architecture also shows downstream 54 V/12 V and core conversion. Actual nominal rail voltages and the number of conversion stages depend on the platform.

For a hall that distributes 800 V DC, rectification moves upstream and rack inputs use DC/DC conversion. The AC/DC function already existed inside conventional AC-fed rack supplies. Compute-rack space can be released, while the relocated equipment still occupies space and needs cooling elsewhere. DC protection and backup interfaces must match the new path. Compare efficiency across the complete chain at the required operating load rather than treating one converter as a new penalty.

## Should we step down first or rectify first?

The established transformer-plus-converter path first steps medium-voltage AC down with a conventional transformer, then uses controlled lower-voltage electronics to rectify and regulate an 800 V DC output. That choice draws on established transformer and converter equipment. It is not a physical requirement to lower AC voltage before rectification.

A modular solid-state transformer (SST) can reverse that order: rectify the medium-voltage input, then use high-frequency isolated DC/DC conversion to obtain the lower DC output. Semiconductor switching creates the alternating waveform for the internal high-frequency transformer. The transformer itself does not operate on steady DC. Series-connected modules can share input-voltage stress across lower-voltage devices.

SSTs are an available architecture option. Eaton lists a 2 MW medium-voltage SST with a 12.47 kV input and 800 V DC output. Texas Instruments’ modular reference design illustrates the electronic and isolation functions, with its own different ratings. Choosing between the paths involves available equipment, qualification, serviceability, protection and complete-path efficiency; an SST is not required merely because a hall distributes 800 V DC.

## Zurich-West: centralized DC in 2012

ABB and Green opened a 1 MW DC system for the Zurich-West expansion in May 2012. Compatible HP servers and storage accepted its 380 V DC supply. This is a built historical example of upstream rectification; its interface is separate from the later 800 V designs.

ABB’s technical account places a 1,100 kilovolt-ampere (kVA) dry transformer inside the central rectifier unit. It steps down the 16 kV AC input before rectifier modules perform AC/DC conversion. Downstream DC/DC conversion still supplies device rails. ABB labels the distribution 380 V DC and specifies 400 V open-circuit. The package name “rectifier” does not remove the transformer function. Neither its conversion placement nor this historical installation establishes a universal efficiency gain.

![Exterior of Green’s Zurich-West data center in the ABB Review case photograph.](../assets/references/distribution-green-zurich-west.jpg)

Green Zurich-West · ABB Review 4/2013. The exterior identifies the facility; the electrical path comes from the technical account. [ABB Review — DC for efficiency](https://library.e.abb.com/public/1afa6036874fd0bb85257d5000710a17/DC%20for%20efficiency.pdf)

## Compare the three distribution paths side by side

Trace each column from medium-voltage input to the rack. Traditional AC keeps lower-voltage AC distribution through the hall. The DC sidecar retains those upstream stages, then creates an 800 V DC interface near the rack. The third path makes 800 V DC upstream of the hall distribution and busway through a medium-voltage conversion system.

The right-hand column is a direct-medium-voltage design. It differs from the preceding transformer-plus-low-voltage-rectifier example: both can feed an 800 V DC hall. A compact system block does not mean that voltage reduction, isolation, storage, protection or downstream rack DC/DC conversion cease to be necessary functions where the design requires them. The diagram leaves several of these functions out.

Use this drawing to compare conversion placement and AC/DC interfaces. It has no deployment dates and does not prove an efficiency percentage or equipment readiness. Keep the dated SemiAnalysis roadmap separate from these architectural alternatives.

![Three electrical paths. Traditional AC: medium-voltage AC, step-down transformer, AC switchboards, AC PDUs, AC IT racks. DC sidecar: the same upstream AC stages followed by a rack-level AC-to-800-V-DC rectifier and 800-V-DC IT racks. Direct medium-voltage DC: medium-voltage rectifier or solid-state transformer, 800-V-DC distribution, DC busway and DC IT racks. Yellow denotes 10 to 35 kV, blue 400 to 480 V, and green 800 V DC.](../assets/references/ocp-ac-sidecar-direct-mvdc.png)

Three paths to 800 V DC racks, attributed to the Open Compute Project: traditional AC, a DC sidecar, and direct medium-voltage conversion. Each column shows selected conversion and distribution functions, not a complete power or protection design. The linked OCP white paper describes related low-voltage DC architectures. [OCP low-voltage DC power-distribution white paper](https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1)

## Read a roadmap as a dated design proposal

NVIDIA’s May 2025 account described a facility-level 800 V DC concept and linked full-scale production to 2027 systems. Its August 11, 2026 update separately described a hybrid power rack expected in the second half of 2026, a row power center expected in 2027, and a broader DC power block. These are vendor descriptions and availability expectations as published. They establish proposed architecture categories, not evidence that a named site has accepted an operating installation or achieved a claimed efficiency.

## Snapshot: SemiAnalysis’s four-phase forecast, May 2026

SemiAnalysis’s May 26, 2026 forecast divides the move to 800 V DC into four phases. Phase 1 (2026/2027) retrofits the white space: a row-level power rack converts AC to 800 V DC, and a power shelf inside the compute rack converts 800 V to about 50 V before the trays. Phase 2 (2027/2028) keeps the row-level power rack, but the 800 V bus runs to each compute blade, where an on-blade power module steps it down to 50 V. Phase 3 (late 2028/2029) moves a central rectifier into the gray space or outdoors, converting 415 V AC to 800 V DC for the whole hall. Phase 4 replaces the low-voltage transformer and rectifier with a solid-state transformer that converts medium voltage directly to 800 V DC. The article’s heading dates Phase 4 after 2029, while its text does not expect SST adoption at scale until early 2029, so this phase has no single forecast date.

These are forecast dates attached to architecture categories. The three architectures above describe where conversion sits, and the phases add the forecaster’s timing: the sidecar covers Phases 1 and 2, and conversion farther upstream covers Phase 3. Conversion in the rack is today’s AC baseline, not Phase 1.

## The 800 V feeder still needs DC fault interruption

Picture an 800 V DC feeder running from a rectifier and its charged bus capacitor through a cable to a DC breaker, with a short circuit downstream. The rectifier and the capacitor can both feed the fault, and the cable’s inductance stores magnetic energy, so the breaker needs a DC voltage rating, fault-current interruption and a way to absorb that stored energy. When a fault develops, opening contacts may draw an arc that continues carrying current. In a conventional mechanical breaker with an arc chamber, the arc is lengthened and cooled to drive current to extinction. DC has no periodic natural current zero; the breaker must manage the actual source, circuit energy and voltage across the open contacts.

This is one interruption mechanism, not a universal description of solid-state or hybrid breakers. Converter current limiting and capacitor discharge can change the fault waveform. Isolation of a feeder also does not prove every downstream store is discharged. The example therefore connects the higher-voltage interface to circuit-specific protection, grounding and stored-energy boundaries without selecting a device or prescribing an operating procedure.

## Compare a chain, not the number of boxes

Fewer conversion stages can be attractive, but stage count is not an efficiency measurement. A larger converter at low load may behave differently from several smaller modules loaded near their intended operating range. Redundancy, thermal conditions, auxiliary power and standby behavior can also change the result. Create a table of stage efficiencies for each architecture at the same delivered load. Multiply efficiencies only along one energy path, add branch loads where they join, and allocate auxiliary consumption to its real location.

Two conversion chains make the point. Path A runs through three stages at 98%, 97% and 95%, and path B through two at 98.5% and 96%, both delivering 100 kW to the same DC load. A’s stages multiply to 0.98 × 0.97 × 0.95 = 90.307%, so it needs 100 ÷ 0.90307 = 110.733 kW of input; B’s multiply to 94.56% and need 105.753 kW. B uses 4.980 kW less, about 4.50% of A’s input. Now add a constant 6 kW auxiliary load at B’s upstream boundary: B needs 111.753 kW, about 1.02 kW more than A. The ranking turns on what the boundary includes, not on the number of stages or the label 800 V.

Conversion losses also dwarf the conductor saving. A single AC-to-DC supply at 98% efficiency delivering 100 kW draws 100 ÷ 0.98 = 102.04 kW and turns 2.04 kW into heat, about 17 times the 122 W the DC feeder saves in its conductors, so an energy comparison between architectures has to follow efficiency along the whole conversion path.

The physical interfaces deserve equal attention. A rack input specification must cover steady demand, peak demand, permitted voltage variation and the response to a sudden load change. The downstream equipment and upstream supply must agree on startup sequencing, fault isolation and shutdown behavior. A higher voltage reduces current at fixed power, but stored electrical energy and fault interruption remain separate engineering questions. For each architecture, list which functions moved and which must be revalidated; a nominal voltage alone does not select the protective equipment.

## Optional market context — SST demand forecast

The model connects future facility adoption to equipment spending using an assumed $1.25 million of SST content per MW. Both adoption and equipment pricing can change; medium-voltage rectifiers compete for part of this opportunity. An 800 V DC interface does not require an SST.

![SemiAnalysis forecast chart for 2026–2030. Gold SST revenue bars label $2.2 billion in 2028, $20.1 billion in 2029 and $32.4 billion in 2030. A blue line uses a separate axis for incremental facility-level GW.](../assets/references/semianalysis-sst-market-forecast-2026-2030.png)

FORECAST · SemiAnalysis, 26 May 2026. Gold: modeled SST revenue ($B). Blue: incremental facility-level GW. These are projections, not observed revenue or deployed capacity. [SemiAnalysis Industrials Model — SST market opportunity](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part)

## Worked example: One 100 kW load, two feeders

- Both feeders deliver 100 kW of real power to the same load.
- The AC feeder is balanced three-phase at 480 V line to line with a power factor of 1, on three current-carrying conductors. The DC feeder holds 800 V across two conductors.
- Every conductor has the same length, cross-section and a resistance of 10 mΩ. Neutral and protective earth are not counted.

1. Count the copper — 2 conductors ÷ 3 conductors = 2/3 — The DC feeder uses one-third less copper in these conductors.
2. Find the AC line current — 100,000 ÷ (√3 × 480 × 1) = 120.28 A — Each of the three lines carries this root-mean-square (RMS) current.
3. Find the DC current — 100,000 ÷ 800 = 125 A — Each of the two conductors carries slightly more current than an AC line.
4. Add the conductor heat — AC: 3 × 120.28² × 0.01 = 434.0 W; DC: 2 × 125² × 0.01 = 312.5 W — Each feeder’s heat is its conductor count times I²R.
5. Compare the heat — 312.5 ÷ 434.0 = 0.72; 434.0 − 312.5 = 121.5 W — The DC feeder produces 28% less conductor heat; the 121.5 W saved is 0.12% of the 100 kW delivered.

**Result:** At the same delivered power, the 800 V DC feeder uses one-third less conductor copper and produces 28% less conductor heat, although each of its conductors carries slightly more current.

**Model boundary:** Equal resistance per conductor is a modeling assumption. Converters, protection, cable sizing and the rest of the facility’s copper are outside this feeder comparison.

## When the situation changes

Trigger: A team treats a hybrid sidecar as a facility-wide DC conversion.

Mechanism: Their drawing hides the AC distribution that the sidecar keeps upstream and wrongly attributes all upstream losses and UPS functions to equipment that has not changed.

Response: Mark every retained and replaced block, then compare the same electrical endpoints under a documented operating state.

## Apply the idea

The AC load draws current at a power factor of 0.9 instead of 1, still receiving 100 kW. Recompute the AC line current and conductor heat. How does the DC feeder’s heat compare now?

<details>
<summary>Reveal the worked answer</summary>

The AC line current becomes 100,000 ÷ (√3 × 480 × 0.9) = 133.6 A, and three conductors at 10 mΩ each turn 535.8 W into heat. The DC feeder still produces 312.5 W, now 58% of the AC heat, or 42% less.

Below a power factor of 1, the AC feeder needs more RMS current to deliver the same real power, and conductor heat grows with the square of that current. The copper count is unchanged, so the DC feeder still uses two-thirds of the copper. Set the lab’s power factor to 0.9 to check the result.

</details>

**The idea to keep:** Specify where 800 V begins and ends, what remains AC, and which claims are roadmap statements.

## Sources

- [NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) — NVIDIA · Published 2025-05-20 · Reviewed 2026-09-06. May 2025 facility DC concept for megawatt-scale racks, conversion placement and forward-looking 2027 timing.
- [Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) — NVIDIA · Published 2026-08-11 · Reviewed 2026-09-06. August 2026 distinction between hybrid power rack, row power center and facility DC power block.
- [Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) — SemiAnalysis · Published 2026-05-26 · Reviewed 2026-09-11. May 2026 forecast of four phases: row-level power racks with rack-shelf (Phase 1, 2026/2027) or on-blade (Phase 2, 2027/2028) step-down, a central 415 V AC rectifier (Phase 3, late 2028/2029) and medium-voltage SSTs (Phase 4, dated after 2029 in its heading and early 2029 in its text); 800 V DC as single-ended 800 V or bipolar ±400 V, with the OCP Diablo 400 specification standardizing ±400 V; 6,000 A at 300 kW in the 50 V ORv3 HPR V3 sidecar; an SST market forecast that assumes $1.25 million of SST content per MW.
- [OCP — Data Center Facility: Low Voltage Direct Current Power Distribution, v1.0](https://www.opencompute.org/documents/dcf-power-distribution-lvdc-white-paper-version-1-0-final-pdf-1) — Open Compute Project · Published 2026-03-30 · Reviewed 2026-09-11. Describes representative low-voltage DC power-distribution architectures for data-center facilities.
- [ABB Review 4/2013 — DC for efficiency](https://library.e.abb.com/public/1afa6036874fd0bb85257d5000710a17/DC%20for%20efficiency.pdf) — ABB · Published 2013 · Reviewed 2026-09-13. Zurich-West: a 1,100 kVA dry transformer inside the central rectifier unit steps 16 kV AC down before rectification to 380 V DC distribution.
- [ABB and Green open Zurich-West DC data-center expansion](https://new.abb.com/news/detail/12816/worlds-most-powerful-dc-data-center-online) — ABB · Published 2012-05-30 · Reviewed 2026-09-13. Opening date, installation scale and compatible HP IT.
- [ABB — Protection Devices for Direct Current Applications](https://library.e.abb.com/public/5cd83dcb95a74dcdb571be5f256e1af8/9AKK108470A9606_en_B_Protection%20Devices%20for%20Direct%20Current%20Applications%20-%20Technical%20Application%20Paper.pdf) — library.e.abb.com · Reviewed 2026-09-06. DC interruption and converter-fed fault behavior depend on circuit dynamics and device capabilities.
- [ABB — Protection Devices for Direct Current Applications, 2025 technical paper](https://library.e.abb.com/public/4b22f4bae7e5424d9bf87039c3c1d0ba/9AKK108470A2501_Technical%20Application%20Paper_Protection%20Devices%20for%20Direct%20Current%20Applications.pdf) — ABB · Published 2025 · Reviewed 2026-09-13. Explains arc formation and conventional arc-chamber interruption in DC breakers, and distinguishes semiconductor, resonant and hybrid interruption methods.
- [Texas Instruments — TIDA-011012 modular solid-state transformer reference design](https://www.ti.com/tool/TIDA-011012) — Texas Instruments · Published 2026-06-04 · Reviewed 2026-09-16. Modular rectification and high-frequency isolated DC/DC conversion explain an SST supply path.
- [Eaton — Medium-voltage solid-state transformer](https://www.eaton.com/us/en-us/catalog/medium-voltage-power-distribution-control-systems/medium-voltage-solid-state-transformer.html) — Eaton · Reviewed 2026-09-16. Eaton’s 2 MW medium-voltage SST is listed with a 12.47 kV input and 800 V DC output.

## Check your understanding: Did moving the converter save energy?

Pause and make a prediction, then compare your reasoning.

A hypothetical redesign moves a converter from each rack to a nearby cabinet. Useful device output, converter efficiency, cable losses and auxiliary demand all remain unchanged.

**Pause and predict:** Did the redesign reduce facility electricity use? Name something it did change.

<details>
<summary>Compare your reasoning</summary>

No energy saving follows from these assumptions. The converter's location and the rack's physical and electrical interfaces changed.

The same output still requires the same total input across the complete path. Conversion heat now occurs outside the rack, and rack space may be released. Shared failure exposure, protection, service access and expansion arrangements need checking at the new location.

</details>

**The next problem:** Power now reaches the devices. How do those devices exchange data within a rack and across the cluster?

Continue in **10. Networking and interconnects**: Count the paths, not just the advertised ports.
