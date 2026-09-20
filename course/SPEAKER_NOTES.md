# Selected speaker notes

## Inside a liquid-cooled data hall — Chapter 2, slide 10

<!-- speaker: overview#abilene-data-hall -->

Overhead pipes connect to flexible hoses along the rack rows. Liquid cooling needs this physical distribution system alongside the computers. The photograph does not reveal each fluid boundary or the location of a CDU.

Sources: [Oracle Abilene media kit](https://www.oracle.com/news/resources/abilene-campus/).

## The power triangle — Chapter 6, slide 25

<!-- speaker: distribution#power-triangle -->

Reactive power is energy exchanged with electric or magnetic fields; 675 kvar is not 675 kW of waste heat. Real and reactive power are perpendicular components: √(900² + 675²) = 1,125 kVA. Power factor is 900 / 1,125 = 0.80.

This triangle assumes sinusoidal voltage and current. Harmonics can also lower true power factor, so PF 0.80 alone does not establish 675 kvar.

Sources: [Schneider power triangle](https://www.electrical-installation.org/enwiki/Definition_of_reactive_power), [harmonic distortion and power factor](https://www.electrical-installation.org/enwiki/Harmonic_distortion_indicators_-_Power_factor).

## Inside a GB300 compute rack — Chapter 8, slide 3

<!-- speaker: rack-energy#rack-hardware-anatomy -->

“If you want to learn more about this chip, watch my chips course.”

The chokes are inductors in parallel switching branches, not separate complete VRMs. Several branches can feed one voltage rail. Counting 24 chokes does not establish 24 VRMs; an exact count needs the board’s circuit information. **Phases** are parallel branches; **stages** are successive conversions.

Sources: [TI: multiphase buck converters](https://www.ti.com/lit/an/slyt449/slyt449.pdf).

## From three-phase AC to the rack busbar — Chapter 8, slide 6

<!-- speaker: rack-energy#psu-input -->

The shelf distributes its three phases across single-phase PSU modules. Here each phase-to-neutral connection is about 277 V, while phase-to-phase voltage is 480 V. Their 50 V DC outputs share the rack bus. Balanced loading uses all three phases and smooths their combined demand. Neutral is separate from protective earth.

The three module photographs represent one branch per phase, not the full shelf population. They do not identify the PSU model installed in the pictured NVIDIA rack.

Sources: [Advanced Energy ORv3 PSU](https://www.advancedenergy.com/en-us/products/ac-dc-power-supply-units/power-shelves/ocp-compliant/orv3-psu/).

## Meta's GB300 power board — Chapter 8, slide 10

<!-- speaker: rack-energy#clemente-power-board -->

Meta’s Clemente tray implements the intermediate rail: the NVIDIA-designed board converts nominal 51 V to 12 V, then local regulators supply the processors. The specification permits 46–52 V at the input; its 48/50 V terminology refers to the same rack supply. The board illustration is conceptual, and the specification does not disclose the final core voltage or phase count.

Sources: [Meta / OCP Clemente specification](https://www.opencompute.org/documents/clemente-compute-tray-ocp-specification-final-pdf).

## How the VRM phases switch — Chapter 8, slide 12

<!-- speaker: rack-energy#vrm-switching -->

The switches make voltage pulses; the inductors produce currents that rise and fall. With both branches switching together, their sum swings from 34 to 46 A. Staggering them by half a period narrows it to 38–42 A, with the same 40 A average. The smaller ripple repeats each cycle. The capacitor supplies or absorbs the remaining mismatch while feedback regulates voltage.

These are two phases inside one regulator, not facility AC phases. This example uses 12 V input, 3 V output and a 25% duty cycle. Lower voltage allows higher current at the same ideal power; real conversion losses require extra input power.

Sources: [Texas Instruments, Benefits of a multiphase buck converter](https://www.ti.com/lit/an/slyt449/slyt449.pdf).

## Should we step down first or rectify first? — Chapter 9, slide 10

<!-- speaker: dc-distribution#ac-dc-ledger -->

“New higher-voltage SiC devices could make SSTs simpler and more competitive. Their widespread adoption in data centers still has to be demonstrated.”

Sources: [Wolfspeed 10 kV SiC announcement](https://www.wolfspeed.com/company/news-events/news/wolfspeed-introduces-industrys-first-commercially-available-10000v-silicon-carbide-power-mosfet/).

## An 800 V DC feeder needs DC-rated protection — Chapter 9, slide 12

<!-- speaker: dc-distribution#dc-feeder-protection -->

Both AC and DC need fault protection. AC’s natural current zeros help extinguish the arc after a breaker opens. DC protection must create that interruption.

The rectifier and charged capacitor can both feed a short circuit, and the cable stores magnetic energy. After interrupting current, the breaker still has to withstand voltage. Turning off the AC supply does not remove the stored energy.

Sources: [ABB DC protection paper](https://library.e.abb.com/public/5cd83dcb95a74dcdb571be5f256e1af8/9AKK108470A9606_en_B_Protection%20Devices%20for%20Direct%20Current%20Applications%20-%20Technical%20Application%20Paper.pdf).

## Inside an AI Superfactory — Chapter 10, slide 4

<!-- speaker: networking#microsoft-ai-superfactory -->

The campus view connects the backbone, power infrastructure and GPU halls. The data-hall detail connects cooling and cable length to the network topology. These are parts of the same physical design.

Sources: [Microsoft Fairwater feature](https://news.microsoft.com/source/features/ai/from-wisconsin-to-atlanta-microsoft-connects-datacenters-to-build-its-first-ai-superfactory/).

## Microsoft’s ambition for Fairwater — Chapter 10, slide 5

<!-- speaker: networking#fairwater-model-scale -->

“The distributed networking of Microsoft’s Fairwater sites is designed to enable them to support training models with hundreds of trillions of parameters.”

Microsoft described that ambition in November 2025, not a completed training run. Dedicated fiber avoids sharing the path with unrelated traffic; it does not remove propagation delay or bottlenecks at the endpoints.

Sources: [Microsoft Fairwater feature](https://news.microsoft.com/source/features/ai/from-wisconsin-to-atlanta-microsoft-connects-datacenters-to-build-its-first-ai-superfactory/).

## Leaf–spine is common, not universal — Chapter 10, slide 10

<!-- speaker: networking#leaf-spine -->

NVIDIA LinkX 400G cables connect switches, network adapters (NICs), and DPUs in AI data centers.

Sources: [NVIDIA LinkX product overview](https://docs.nvidia.com/networking/display/400g100gpam4ovdev/LinkX-100G-PAM4-Product-Line-Overview).

## Copper for short links; optical fiber for longer runs — Chapter 10, slide 11

<!-- speaker: networking#copper-and-light -->

Longer copper runs lose and distort high-speed electrical signals. Short passive copper links stay simple and use little power. Fiber uses modules at both ends to convert electricity to light and back.

These 400G examples reach 2 m over passive copper, 50 m over multimode fiber and 500 m over single-mode fiber. Select the supported reach for the required data rate and actual cable route.

Sources: [NVIDIA LinkX product overview](https://docs.nvidia.com/networking/display/400g100gpam4ovdev/linkx-100g-pam4-product-line-overview).

## Co-packaged optics shortens the electrical path inside the switch — Chapter 10, slide 12

<!-- speaker: networking#optical-packaging -->

Pluggable optics puts electrical-to-optical conversion at the front panel. CPO moves it beside the switch chip, shortening the electrical path. Both approaches remain in use.

Sources: [NVIDIA CPO](https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/), [Spectrum-6 optical options](https://blogs.nvidia.com/blog/nvidia-spectrum-six-arrives-in-gigascale-ai-factories/).

## Cross-leaf bandwidth is shared by the servers beneath each leaf — Chapter 10, slide 13

<!-- speaker: networking#shared-uplinks -->

Four 400 Gb/s server ports can offer 1,600 Gb/s, but two 400 Gb/s uplinks carry only 800. That is 2:1 oversubscription across this boundary.

Four uplinks match the server-port capacity. For 256 Gb of balanced one-way traffic, the minimum transfer time falls from 0.32 seconds to 0.16. Bandwidth is an upper limit on throughput; dividing the data size by that rate gives a lower limit on time. Overhead and congestion can make the transfer take longer. Traffic staying under the same leaf does not use these uplinks.

Sources: [`fabricBudget`](prototypes/networking-model.js).

## Incast — Chapter 10, slide 14

<!-- speaker: networking#incast -->

Incast is many senders converging on one receiver. When their combined traffic exceeds the receiving link’s capacity, packets queue at the switch output. This is the same capacity principle as the previous slide, applied to the receiver’s link.

Sources: [NVIDIA ConnectX-7 specifications](https://networking-docs.nvidia.com/connectx7hw/specifications).

## Meta built large AI clusters with both Ethernet and InfiniBand — Chapter 10, slide 16

<!-- speaker: networking#ethernet-infiniband -->

RoCE is RDMA over Converged Ethernet. RDMA lets adapters transfer data into permitted remote memory without the usual CPU-managed copying for each transfer.

Either fabric needs coordinated routing, congestion control, collective software and job placement. Those choices determine how well the workload uses the installed network.

Sources: [NVIDIA RoCE documentation](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/), [Meta’s 2024 cluster account](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/).

## Campus fiber handoff — Chapter 10, slide 18

<!-- speaker: networking#campus-fiber -->

The router directs traffic; the patch panel organizes physical connections. In the meet-me room, the data center’s fiber connects to a carrier—a company providing network service. That service may be a private intersite link or Internet connectivity.

The facility needs space for this handoff and planned fiber entrances and ducts, ready alongside power and cooling.

Sources: [Equinix Cross Connect documentation](https://docs.equinix.com/cross-connect/).

## The slowest server sets the pace — Chapter 10, slide 20

<!-- speaker: networking#network-diagnosis -->

These are transfer completion times from the same start, not ping latencies. The next step needs all four results, so the first three servers wait for server 4 to finish at 50 ms. Speeding up the first three alone will not shorten that wait. Unrelated work can still proceed.

## Meta built storage in tiers to keep GPUs supplied — Chapter 10, slide 21

<!-- speaker: networking#meta-rsc -->

Meta’s January 2022 RSC account separates bulk storage, cache and shared file storage. AIRStore prepares datasets once for reuse across training runs, reducing repeated preparation and transfers.

Keeping GPUs supplied therefore requires storage equipment and network capacity, with their own rack space, power, cooling and cable routes.

Sources: [Meta’s January 24, 2022 RSC account](https://ai.meta.com/blog/ai-rsc/).

## Out with the Old, In with the New — Chapter 11, slide 2

<!-- speaker: cooling#capture-options -->

A CRAH moves room air across a chilled-water coil. A liquid-to-liquid CDU pumps coolant through the equipment and transfers heat into separate facility water; the liquids do not mix.

A rack can need both: cold plates collect selected chip heat, while other components still heat the air. Liquid-to-air CDUs also exist, but the diagram here uses a liquid-to-liquid CDU.

Sources: [DOE FEMP cooling systems](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers), [CoolIT CDU architectures](https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/).

## How does coolant reach the cold plates? — Chapter 11, slide 3

<!-- speaker: cooling#cold-plate -->

Rack-side coolant passes through the manifold, tray connections and cold plates, then returns to the CDU. Facility water stays on the other side of the CDU’s heat exchanger.

## Liquid cooling inside Abilene — Chapter 11, slide 4

<!-- speaker: cooling#abilene-coolant-distribution -->

This scales the cold-plate path up to a row: overhead pipes and hoses distribute coolant to many racks. The photograph alone does not identify each fluid boundary or a hidden CDU.

Sources: [Oracle Abilene media kit](https://www.oracle.com/news/resources/abilene-campus/).

## Rear-door heat capture — Chapter 11, slide 5

<!-- speaker: cooling#capture-rear-door -->

Cold plates can leave some heat in the rack’s exhaust air. An RDHX captures that heat into liquid; room-air handlers are another option. The NVIDIA coolant manifold pictured alongside is not itself a rear-door exhaust coil. The Abilene evidence does not establish one residual-air arrangement across every hall.

Sources: [Lenovo’s GB300 guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai#cooling).

## Immersion — Chapter 11, slides 6–7

<!-- speaker: cooling#capture-immersion -->

Single-phase immersion fluid stays liquid while carrying heat to an exchanger. Two-phase immersion boils at the hardware and condenses so the liquid can return.

<!-- speaker: cooling#immersion-hardware -->

This photograph shows immersion hardware. Its operator and fluid were not supplied, so the photograph does not establish which immersion process it uses.

## Heat flux — Chapter 11, slide 8

<!-- speaker: cooling#local-heat-flux -->

Both devices produce 400 W. Over 4 cm² that is 100 W/cm²; over 1 cm² it is 400 W/cm². The total heat is unchanged, but it must leave through a smaller area.

## Thermal resistance — Chapter 11, slide 9

<!-- speaker: cooling#thermal-resistance-example -->

At 100 W and 0.2°C/W, the chip needs a 20°C gap above the water: 100 × 0.2 = 20. With 30°C water, that gives a 50°C chip. This is the chip-to-water gap, not the water’s supply-to-return rise.

## Chip temperature — Chapter 11, slide 10

<!-- speaker: cooling#device-temperature -->

At 400 W, a 0.08°C/W thermal resistance needs a 32°C chip-to-water gap; 0.12°C/W needs 48°C. With the same 35°C coolant, the chips reach 67°C and 83°C.

Heat flux alone does not determine these temperatures. The resistance describes the complete specified heat-transfer path; these two values are separate example inputs.

Sources: [cooling-capture-model.js](prototypes/cooling-capture-model.js).

## Coolant flow — Chapter 11, slide 11

<!-- speaker: cooling#water-balance -->

The same heat can leave in more water with a smaller temperature rise. At fixed heat duty and heat capacity, doubling mass flow halves the supply-to-return rise.

## Coolant flow and the pump curve — Chapter 11, slide 12

<!-- speaker: cooling#pump-operating-point -->

The previous slide showed why coolant flow matters. This graph shows what determines how much flow we actually get.

The horizontal axis is flow, in litres per second. The vertical axis is the pressure difference the pump adds to drive coolant around the loop. We’re keeping the pump speed fixed.

The downward-sloping line shows what the pump can provide. At this speed, it can produce a larger pressure difference at low flow, and a smaller one at high flow.

The upward-sloping line shows what the cooling circuit requires. Pushing more coolant through the pipes, valves and cold plates takes a larger pressure difference.

Where those two lines meet is where the system settles. That’s the operating point. At point A, the pump provides the pressure the circuit needs to sustain two litres per second: 120 kilopascals.

Now imagine a valve is partly closed, or a filter starts to clog. Getting the same flow through that restriction would require more pressure. That gives us the steeper, dashed line. The pump speed hasn’t changed, so the pump curve stays where it is.

The new intersection is point B. Flow falls to about 1.4 litres per second, while the pressure difference rises to 140 kilopascals.

The pump is still running, and it’s producing a larger pressure difference, but less coolant is circulating. That’s why we need to check flow as well as pressure: the equipment still needs enough coolant to carry its heat away.

Sources: [Grundfos — How does one read a pump curve?](https://www.grundfos.com/solutions/support/faq/how-does-one-read-a-pump-curve-of-a-heating-pump), [Hydraulic Institute — Combined pump and system curves](https://datatool.pumps.org/pump-fundamentals/combined.html), [KSB characteristic curves](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/characteristic-curve-1117926).

## CDU approach compares two supply temperatures — Chapter 11, slide 13

<!-- speaker: cooling#approach -->

Facility water enters at 30°C; separate rack coolant leaves toward the chips at 35°C. Their 5°C difference is the CDU approach, not one fluid’s supply-to-return rise.

A smaller approach leaves more temperature margin, but may require more exchanger area, flow, pumping or cost. A 5°C temperature difference equals 5 K.

Sources: [Vertiv CDU 121 application guide, thermal performance at 3°C, 5°C and 7°C approach](https://www.vertiv.com/490d59/globalassets/shared/vertiv-coolchip-cdu-121-application-and-planning-guide-sl-802762.pdf), [NIST SI temperature units](https://www.nist.gov/pml/special-publication-330/sp-330-section-2).

## CoolIT CHx2000 — Chapter 11, slide 14

<!-- speaker: cooling#coolit-cdu -->

The manufacturer’s 2 MW at 5°C approach and 2,125 L/min at 35 psi are separate thermal and hydraulic specifications. This CDU contains pumps and a heat exchanger, not a refrigeration compressor.

Sources: [CoolIT CHx2000](https://www.coolitsystems.com/cdu-product/chx2000/).

## Cooling redundancy and response — Chapter 11, slides 15–18

<!-- speaker: cooling#lost-flow -->

Spare CDU capacity only helps racks that remain connected to it. Trace the coolant path as well as the equipment count.

<!-- speaker: cooling#independent-cooling-paths -->

Each A/B train can carry the load, but follow the connections after one train is lost to establish which racks still receive coolant.

<!-- speaker: cooling#cooling-derating -->

Two failures leave 600 kW of cooling against 1,000 kW entering the coolant. Reducing that heat load to 500 kW restores a 100 kW margin.

<!-- speaker: cooling#cooling-response -->

Test the response by commanding the affected racks and measuring actual power, flow and temperature. A power-cap command is not itself proof of reduced liquid heat. This qualitative trace does not establish a safe response time.

## Retrofit and residual air heat — Chapter 11, slide 19

<!-- speaker: cooling#cooling-retrofit -->

The cold plates collect 85 kW, leaving 15 kW in air. That uses 15 kW of the room’s 20 kW allowance, or a suitable rear-door exchanger can move it into liquid. The example assumes the door captures all of that remaining 15 kW.

## At Abilene, the heat goes to outdoor air — Chapter 12, slide 2

<!-- speaker: heat-rejection#abilene-cooling -->

Heat passes from rack coolant into separate facility water and then outdoor air. Crusoe describes non-evaporative heat rejection: water circulates rather than evaporating to carry away heat. Initial fill and maintenance still require water.

Sources: [Crusoe’s August 5, 2025 Abilene account](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center).

## Wet and dry equipment; tower water balance — Chapter 12, slides 3–4

<!-- speaker: heat-rejection#rejection -->

In an open wet tower, water spreads over fill and contacts moving air. Some evaporates; the cooled water collects below. A dry cooler transfers heat through a sealed coil wall.

<!-- speaker: heat-rejection#water-ledger -->

Evaporation leaves dissolved minerals behind. Blowdown removes concentrated water; makeup replaces evaporation and discharge. Makeup describes the water’s role, not its source or treatment quality.

Sources: [DOE component guide](https://www.energy.gov/sites/default/files/2013/10/f3/waterfs_coolingtowers.pdf), [DOE cooling-tower management](https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management).

## Wet bulb and dry bulb — Chapter 12, slides 5–6

<!-- speaker: heat-rejection#bulb-definitions -->

Dry bulb is ordinary air temperature. A wetted, ventilated sensor cools by evaporation: wet bulb is lower in unsaturated air and equal at saturation.

<!-- speaker: heat-rejection#weather -->

Higher humidity raises wet bulb even at the same dry-bulb temperature. That leaves less temperature difference for evaporative cooling. Dry coolers follow dry bulb; evaporative towers can approach wet bulb.

Sources: [NWS definitions](https://www.weather.gov/source/zhu/ZHU_Training_Page/definitions/dry_wet_bulb_definition/dry_wet_bulb.html).

## Follow the outdoor coolant paths — Chapter 12, slides 7 and 10

<!-- speaker: heat-rejection#approach-outdoors -->

Every exchanger needs a temperature difference. With 35°C outdoor air and a 5°C dry-cooler approach, facility water reaches 40°C. Another 5°C across the CDU gives 45°C rack coolant—above this example’s 35°C coolant limit. That limit is for coolant, not the chip.

<!-- speaker: heat-rejection#approach-wet -->

Fill spreads water into thin films or droplets, creating more surface for contact with air. Tower water can evaporate; separate facility and rack loops stay on their respective sides of the exchangers. Follow heat across those interfaces, not one fluid through every component.

Sources: [DOE cooling-tower component guide](https://www.energy.gov/sites/default/files/2013/10/f3/waterfs_coolingtowers.pdf).

## A cooling boost — Chapter 12, slide 8

<!-- speaker: heat-rejection#adiabatic-boost -->

“The dry path cannot reach the required coolant temperature here. Can we give it a boost?”

## Adiabatic assist — Chapter 12, slide 9

<!-- speaker: heat-rejection#adiabatic-assist -->

Evaporation cools the incoming air before it reaches the sealed water/glycol coil. Unlike an open tower, the process fluid itself does not contact the air. The assist consumes water while operating, even though that process loop is closed. It can run continuously when water and suitable conditions are available.

## Closed-loop water — Chapter 12, slide 11

<!-- speaker: heat-rejection#closed-loop-water -->

A separating exchanger keeps facility water closed while tower water contacts air and evaporates. A sealed outdoor dry-cooler loop may use water/glycol for freeze protection; that does not prescribe the fluid inside the rack. Neither route shown here uses refrigeration.

## Chiller and economizer — Chapter 12, slides 12–13

<!-- speaker: heat-rejection#chiller-balance -->

The compressor adds energy: 10 MW collected plus 2 MW of compressor electricity means 12 MW rejected outdoors, before pump and fan loads.

Facility water heats a separate refrigerant circuit. Its condenser sends heat to air, or into another water circuit. The extra circuit changes the heat path; it does not automatically provide a redundant route.

<!-- speaker: heat-rejection#plant-options -->

Water-side free cooling bypasses refrigeration through a suitable outdoor heat-transfer path. Refrigerant-side free cooling instead circulates refrigerant without the compressor. Both need compatible equipment and suitable weather. The supplied image shows water-side free cooling; its fluid is water.

Sources: [review question 26](REVIEW_QUESTIONS.md#26-can-a-closed-rack-loop-use-a-wet-tower-could-open-tower-water-go-all-the-way-to-the-cdu), [Trane free cooling](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/glossary/free-cooling.html), [Vertiv EconoPhase](https://www.vertiv.com/en-us/products-catalog/thermal-management/room-cooling/econophase-pumped-refrigerant-economizer/).

## What connects after the facility loop? — Chapter 12, slide 14

<!-- speaker: heat-rejection#cooling-layouts -->

The rack coolant and facility water remain separate at the CDU. These arrows follow heat, not one fluid.

- Without a chiller, facility heat goes to a dry cooler or through an exchanger into a wet-tower circuit.
- An air-cooled chiller rejects refrigerant heat directly to outdoor air.
- A water-cooled chiller transfers refrigerant heat into condenser water, which carries it to outdoor equipment.

The condenser is that last interface, not another CDU. Economizing is a separate feature that avoids compressor work when conditions permit.

Sources: [Trane chiller types](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/glossary/chillers.html), [Trane free cooling](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/glossary/free-cooling.html).

## Cooling COP — Chapter 12, slide 15

<!-- speaker: heat-rejection#cooling-cop -->

COP compares heat moved with electricity consumed. Include the same equipment in the electricity boundary when comparing two COP values.

## Hot weather needs more cooling electricity — Chapter 12, slide 16

<!-- speaker: heat-rejection#hot-hour -->

For 8 MW of computing, COP 8 needs 1 MW of cooling electricity; COP 4 needs 2 MW. Add 0.4 MW of other demand and the site moves from 9.4 to 10.4 MW, exceeding its 10 MW limit. Enough heat-removal capacity does not guarantee enough electrical capacity.

## Heat reuse — Chapter 12, slide 17

<!-- speaker: heat-rejection#heat-reuse -->

The data center produces 4 MW all day, but the factory wants only 2 MW for six hours—or none when closed. Unused heat still needs another rejection path.

## Toronto's deep lake cooling — Chapter 12, slides 18–20

<!-- speaker: heat-rejection#toronto-lake-cooling -->

Lake Ontario water enters Toronto’s drinking-water system. At John Street, exchangers transfer heat from the separate district loop into that potable flow. Lake water does not circulate through server racks.

<!-- speaker: heat-rejection#toronto-cooling-outage -->

During the July 2013 flood, PEER1 said the building’s generators worked while its external cooling provider had power problems. Electricity could reach the racks while their heat-removal path was disrupted. The source does not identify the exact failed pump.

<!-- speaker: heat-rejection#toronto-operator-response -->

Uberflip’s CTO reported cold-side cabinet air above 43°C, thermal shutdowns, deliberate shutdown of nonessential machines and service transfers. PEER1 reported partial relief from an emergency chiller. The lake still held cold water; the equipment needed to deliver that cooling was the dependency.

Sources: [Enwave / Toronto Water](https://www.enwave.com/case-studies/enwave-and-toronto-water-tap-into-innovative-energy-source), [Hydro One, July 8, 2013](https://www.newswire.ca/news-releases/hydro-one-power-outages-due-to-heavy-rains-512697891.html), [contemporary PEER1 account](https://www.datacenterknowledge.com/outages/toronto-flooding-kos-data-center-cooling-systems), [Uberflip CTO's July 9 report](https://seclists.org/nanog/2013/Jul/130).

## Operating dependencies — Chapter 12, slide 21

<!-- speaker: heat-rejection#water-restriction -->

Dry rejection needs electricity. A wet tower needs electricity and ongoing water. Initial fill is separate from that operating water demand.

## EPC and the late rack change — Chapter 13, slides 1–6

<!-- speaker: procurement-cases#epc-and-prefab -->

EPC means engineering, procurement and construction. It defines project responsibilities; prefabrication is a manufacturing strategy. Commissioning is not the C in EPC.

<!-- speaker: procurement-cases#rack-case-brief -->

The design changes just before fabrication. Decide what can continue, what must wait, and what evidence releases each hold.

<!-- speaker: procurement-cases#rack-change -->

Each picture shows one 2 MW zone: twenty 100 kW racks become ten 200 kW racks. The data center has ten such zones, so total demand stays at 20 MW. Keeping the total unchanged does not preserve the branch connections, coolant flow or floor loads.

<!-- speaker: procurement-cases#electrical-interface -->

At balanced 480 V three-phase and PF 1, 100 kW needs about 120 A; 200 kW needs 241 A. The existing 160 A branch cannot serve the new rack.

<!-- speaker: procurement-cases#hydraulic-interface -->

At a 10°C water rise, flow doubles from 2.39 to 4.78 kg/s. With this branch’s quadratic pressure-flow relation, required pressure difference quadruples from 20 to 80 kPa. These are inlet-to-outlet differences at two flows.

<!-- speaker: procurement-cases#spatial-interface -->

This example also doubles rack mass on the same four feet, concentrating the support load. That is a separate hardware assumption: twice the electrical power does not by itself imply twice the mass.

## Prefabrication at different scales — Chapter 13, slides 7–9

<!-- speaker: procurement-cases#factory-and-site -->

Factory assembly can overlap site construction. The schedules meet at delivery and installation, so interfaces need to be fixed before fabrication.

<!-- speaker: procurement-cases#aws-houdini-prefab -->

The Houdini account describes AWS data-hall skids and Cupertino Electric’s participation. The photograph shows CEI’s Edgerton factory; it does not identify a pictured unit as Houdini equipment.

<!-- speaker: procurement-cases#compass-package -->

Siemens and Compass jointly developed the switchgear-and-transformer skid. The photograph shows its switchgear portion. Combining equipment changes the assembly scope; it does not establish a universal schedule saving.

## Open Compute Project — Chapter 13, slides 10–11

<!-- speaker: procurement-cases#interface-owner -->

A standard can make connectors compatible without making the branch large enough. Matching UQD interfaces can mate, but this rack needs 4.8 kg/s against a 3.0 kg/s branch limit.

<!-- speaker: procurement-cases#ocp-rack-example -->

Open Rack consolidates power supplies at rack level instead of putting a PSU in each server. This supplied image illustrates that interface choice; it is not identified as a GB300 product.

Sources: [ORv3 revision 1.0](https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf), [UQD revision 1.0](https://www.opencompute.org/documents/ocp-universal-quick-disconnect-uqd-specification-rev-1-0-2-pdf).

## Factory and site acceptance — Chapter 13, slide 12

<!-- speaker: procurement-cases#factory-acceptance -->

Factory tests check internal wiring, piping and controller logic before shipment. Site tests still need to prove field connections and the response of the installed equipment. Prefabrication moves some troubleshooting earlier.

## Which racks are ready? — Chapter 13, slide 13

<!-- speaker: procurement-cases#accepted-paths -->

Only A21–A60 have all three services: 40 racks, or 8 MW. Extending cooling to A01 increases that intersection to 60 racks and 12 MW. Total equipment capacity is useful only where the completed paths overlap.

## Connect the next phase beside live service — Chapter 13, slide 14

<!-- speaker: procurement-cases#phase-boundary -->

Applied Digital reported the first 50 MW ready for service on October 27, 2025, and another 50 MW on November 24. Connecting the next phase must preserve service to the first. The reports do not disclose the exact shared topology.

Sources: [first 50 MW](https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at), [second 50 MW](https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at).

## Diagnose Row B — Chapter 14, slides 1–3

<!-- speaker: operations#operations-purpose -->

The supply water is normal, but the hottest chip is at 85°C against this example’s 80°C limit. A plant reading alone does not prove adequate cooling at the chip.

<!-- speaker: operations#measurement-boundaries -->

Flow halved from 100 to 50 kg/s. Supply stayed at 30°C, while return rose from 35 to 40°C. Both stabilized states carry 2.09 MW: 100 × 4.18 × 5 = 50 × 4.18 × 10. That water balance does not calculate chip temperature or identify the cause of the lower flow.

<!-- speaker: operations#heat-balance -->

Immediately after flow falls, the old 5°C water rise carries only 1.045 MW. Heat accumulates and temperatures rise. Later, the 10°C water rise carries the full 2.09 MW again, but the measured chip remains too hot.

The larger chip-to-water temperature gap drives heat through the less effective cooling path. This gap differs from the water’s inlet-to-return rise. The trace illustrates the transition; it does not calculate the 85°C endpoint or an elapsed time.

Sources: [CoolIT’s cold-plate thermal-resistance versus flow graph](https://www.coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf).

## Google’s AI cooling and control layers — Chapter 14, slides 4–9

<!-- speaker: operations#google-cooling -->

Google’s 2016 AI advised operators. By 2018, the system directly controlled cooling under operator supervision, with an override available.

<!-- speaker: operations#google-cooling-flow -->

Sensors feed predictions; the optimizer selects an action within constraints; local checks verify it before execution. The five-minute supervisory loop is not the protective response time.

<!-- speaker: operations#google-cooling-performance -->

Over nine months, cooling energy per unit of cooling improved from about 12% to about 30% below the historical pre-AI baseline. This is trailing twelve-month cooling performance, not a 30% reduction in total site electricity.

<!-- speaker: operations#control-layers -->

Local controllers regulate equipment, plant controls stage capacity, and the scheduler decides when work starts. They act at different boundaries and timescales.

<!-- speaker: operations#plant-controls-focus -->

Starting standby equipment is a plant-level decision. The scheduler still needs to know when that extra capacity is actually available.

<!-- speaker: operations#admit-work -->

Existing work produces 4 MW; the new job adds 2 MW. Cooling can remove 5 MW now and 7 MW after startup. Starting early creates a 1 MW deficit. No thermal-buffer allowance is given, so the three-minute startup does not establish a safe overrun period.

Sources: [Google DeepMind, August 2018](https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/).

## Cooling reserve and staging — Chapter 14, slides 10–11

<!-- speaker: operations#chiller-staging -->

Capacity margin, redundancy after failure and stored cooling answer different questions. This Metasys sequence uses 80% or 90% stage-up thresholds for specified chiller types; time, trend and failsafe conditions also matter. Those thresholds are not guaranteed reserve margins.

Set the margin from expected demand, usable capacity under the required conditions, and the time needed to bring more equipment online.

<!-- speaker: operations#intel-cooling-reserve -->

Intel’s two 24,000-US-gallon tanks held water at 42°F, or 5.6°C. The design covered five minutes of full-load UPS runtime plus seven extra minutes of cooling. In the actual event, lightly loaded servers ran over fifteen minutes and the tanks maintained cooling. Backed-up pumps and fans made the stored cooling usable.

Sources: [Johnson Controls staging threshold](https://docs.johnsoncontrols.com/bas/r/Metasys/en-US/Chilled-Water-Plant-for-Guideline-36-Application-Note/1.0/Chiller-sequence-of-operations/Chiller-and-waterside-economizer-staging-determination-5.20.1-15/Stage-Up-Part-Load-Ratio-SPLRUP), [stage-up conditions](https://docs.johnsoncontrols.com/bas/r/Metasys/en-US/Chilled-Water-Plant-for-Guideline-36-Application-Note/1.0/Chiller-sequence-of-operations/Chiller-and-waterside-economizer-staging-determination-5.20.1-15/Stage-up-efficiency-condition), [Intel IT thermal storage](https://www.intel.com/content/dam/doc/white-paper/intel-it-thermal-storage-system-provides-emergency-data-center-cooling-paper.pdf), [Schneider reserve-cooling guidance](https://blog.se.com/datacenter/2013/02/11/4-tips-for-keeping-your-it-equipment-cool-during-when-the-power-goes-out/).

## Demand response at The Dalles — Chapter 14, slides 12–14

<!-- speaker: operations#google-demand-response -->

In the 2023 Northern Wasco County PUD pilot, the utility requested a day-ahead reduction during busy grid hours.

<!-- speaker: operations#google-demand-response-workloads -->

Video processing and Translate updates could wait while Search, Maps and video playback continued. Those are Google’s examples, not a claim that arbitrary interactive requests can be paused.

<!-- speaker: operations#deadline-scheduling -->

Pausing the 4 MW job from 14:00 to 16:00 shifts completion from 16:00 to 18:00, before its 20:00 deadline. Both schedules use 12 MWh, but event demand falls from 24 to 20 MW. This example assumes restart without penalty and sufficient later capacity.

Sources: [Google Cloud, October 2023](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption).

## Cloudflare’s failure, correction and retest — Chapter 14, slides 15–17

<!-- speaker: operations#cloudflare-pdx -->

The November 2023 Portland power loss disrupted dashboard, API and analytics services. Multi-site services still depended on Kafka and ClickHouse at PDX-04. Earlier tests removed only its HA portion, not the whole facility.

<!-- speaker: operations#cloudflare-facility-test -->

Code Orange added capacity and changed failover. A February 2024 whole-facility test revealed another gap, which the team then corrected.

<!-- speaker: operations#cloudflare-retest -->

On March 26, power failed at 14:58 UTC; APIs and dashboards recovered automatically by 15:05. Analytics took longer. Seven minutes describes those service endpoints, not the facility’s cold-start time.

Sources: [November 2023 report](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/), [April 2024 follow-up](https://blog.cloudflare.com/major-data-center-power-failure-again-cloudflare-code-orange-tested/).

## London and Llama 3 — Chapter 14, slides 18–22

<!-- speaker: operations#london-cooling-quote -->

This is Google’s own root-cause account from its July 29, 2022 final report.

<!-- speaker: operations#london-recovery -->

Extreme heat and simultaneous failures of redundant cooling forced shutdown of part of one London zone.

<!-- speaker: operations#london-recovery-timeline -->

Cooling repair was recorded at July 19, 14:13 PDT; initial service restoration at July 20, 04:28—another 14 hours 15 minutes. Restart sequencing and service-state reconciliation continued after cooling returned.

<!-- speaker: operations#llama-recovery -->

Llama 3 had 466 interruptions in 54 days: 47 planned and 419 unexpected. More than 90% effective training time compares useful training with elapsed time; it is not facility availability.

<!-- speaker: operations#llama-maintenance -->

Smaller maintenance groups cause more frequent training interruptions. Larger groups remove more capacity at once. The curve shows that trade-off without establishing a numerical optimum.

Sources: [Google Cloud final report](https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2), [Llama 3 §3.3.4](https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4), [Meta maintenance trains](https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/).

## Knowledge check — Chapter 14, slide 23

<!-- speaker: operations#operating-decision -->

The site has spare power and cooling, but Row C has only 2.09 MW of water-side headroom: 100 × 4.18 × (40 − 35) ÷ 1,000. The extra 2.50 MW does not fit at the current flow.

Total heat would be 4.59 MW. Holding return to 40°C requires 4,590 ÷ (4.18 × 10) = 109.81 kg/s, rounded to 110. At 100 kg/s, return reaches 40.98°C.

Establish sufficient local flow or place some work elsewhere. The calculation assumes all added heat enters this water branch; it does not prove the installed equipment can deliver that flow safely.

## GPU cloud economics — Chapter 15

<!-- speaker: capacity#hardware-prices-meme -->

This concerns consumer hardware prices and availability, not GPU rental rates.

<!-- speaker: capacity#capacity-purpose -->

Committed capacity can give a provider predictable revenue, while the customer still has to turn that compute into useful work.

<!-- speaker: capacity#what-is-sold -->

The provider’s capacity invoice differs from a lab’s internal cost per token or training run. Bare metal means dedicated physical hardware without a hypervisor; it can still run Kubernetes and managed software.

<!-- speaker: capacity#service-boundary -->

The choice is who operates inference. Your team can run the serving stack on CoreWeave infrastructure, or CoreWeave can run it through Dedicated Inference. You supply the model and application in both.

<!-- speaker: capacity#service-examples -->

Anthropic’s announced CoreWeave agreement supplies capacity for Claude, but does not disclose the serving responsibilities. For the managed example, Cursor trained Fast Apply and Fireworks deployed and served it through its API. That account concerns Fast Apply, not every Cursor model.

<!-- speaker: capacity#rental-products -->

Cloud Spot rents spare capacity that can be reclaimed. AWS adjusts its price gradually, not on every instantaneous market movement.

<!-- speaker: capacity#contract-tenor -->

Longer commitments exchange future repricing opportunities for more predictable revenue. Delivery and customer credit risks remain.

<!-- speaker: capacity#rental-market -->

These are dated H100 price ranges. Use the changing prices to consider what happens when a rental contract renews.

<!-- speaker: capacity#billable-occupancy -->

$2.50 / $4.00 = 62.5%: the higher-rate pool needs that share of rented hours to match full-fleet commitment revenue before costs. Rented hours differ from GPU compute utilization.

<!-- speaker: capacity#contract-financing -->

Lenders fund hardware; customer payments support debt service. Contracts allocate delivery, credit and operating risk rather than eliminating it.

<!-- speaker: capacity#nvidia-money-machine -->

The arrows distinguish investment, hardware/software purchases and services. The valuations are a historical snapshot.

<!-- speaker: capacity#nvidia-coreweave-backstop -->

CoreWeave’s initial September 2025 agreement covered $6.3 billion of capacity. Keep that specific contract separate from the later backstop program.

<!-- speaker: capacity#nvidia-backstop-financing -->

NVIDIA’s July 2026 filing describes typically six-year support for cloud capacity, allowing providers to offer shorter customer rentals. It is not an unconditional guarantee of the provider’s debts.

<!-- speaker: capacity#nvidia-backstop-risk -->

The $36 billion figure is a dated aggregate commitment, not a realized loss. Buying unused capacity provides a revenue floor while leaving NVIDIA exposed if customers do not fill it.

<!-- speaker: capacity#gpu-hour-cost -->

Idle GPUs can still consume power. Here 80 rented hours at 1 kW plus 20 idle hours at 0.2 kW use 84 kWh. Spread across 80 billed hours, that is 1.05 kWh per billed GPU-hour.

At $80/MWh it costs $0.084; at $160/MWh, $0.168. These are assumed site allocations, not device specifications. Rented time does not mean continuous maximum-power computing.

<!-- speaker: capacity#electricity-pass-through -->

The extra $0.084 per billed GPU-hour reduces provider margin under a fixed fee, or reaches the customer under full reimbursement. Core Scientific’s colocation agreement passes power costs to CoreWeave without markup. That does not establish CoreWeave’s GPU-cloud customer terms.

<!-- speaker: capacity#abilene-roles -->

Crusoe builds the facility, Oracle supplies cloud capacity and OpenAI runs workloads. Their responsibilities sit at different points in the delivery chain.

<!-- speaker: capacity#datacenter-delay-quote -->

“For one concrete case, let’s compare Abilene’s original plan with its reported delivery.”

The article challenges aggregate delay headlines, not the existence of individual delays.

<!-- speaker: capacity#abilene-ledger -->

Compare each target with the corresponding reported milestone. Energization, construction completion and delivered capacity are different events; mismatched milestones cannot establish an exact schedule slip.

Sources: [Anthropic–CoreWeave agreement](https://www.coreweave.com/news/coreweave-announces-multi-year-agreement-with-anthropic), [Cursor–Fireworks case](https://fireworks.ai/blog/cursor), [idle-system power model](https://docs.nvidia.com/datacenter/dps/versions/latest/guides/reference/apis/v1/devices.html), [Core Scientific Q2 2026 filing, Electricity Costs](https://www.sec.gov/Archives/edgar/data/1839341/000183934126000014/core-20260630.htm), [SemiAnalysis’s June 18, 2026 article](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter).

## Putting an AI Factory Together — Chapter 16

<!-- speaker: integrated-cases#abilene-factory -->

This is the original Oracle/OpenAI campus in July 2026. Keep the neighboring Microsoft development separate.

<!-- speaker: integrated-cases#abilene-workload -->

Work backward from processor demand through conversion losses, other rack loads and facility support. The earlier example starts with 72 kW at processor rails, adds 12 kW of other rack loads, and needs 90.26 kW on the DC bus and 93.05 kW at the AC inlet. These are teaching values, not Abilene ratings.

Components outside the cold plates still release heat into air. Public sources do not establish the residual-air equipment in every Abilene hall.

<!-- speaker: integrated-cases#abilene-power -->

Crusoe describes 350 MW of gas generation as temporary bridge power and long-term backup. The same equipment serves a delivery role first and a continuity role later; its rating does not establish backup coverage for the entire planned campus.

<!-- speaker: integrated-cases#abilene-cooling-choice -->

Compare direct dry cooling, air-cooled refrigeration and water-cooled refrigeration with a wet tower before revealing the site’s choice. Air-cooled describes the outdoor condenser; the GPU cold plates still use liquid. These are architectural alternatives, not a disclosed procurement shortlist.

<!-- speaker: integrated-cases#abilene-heat -->

Crusoe chose air-cooled chillers to avoid evaporative water use. Water conservation can be commercially attractive too. Gas emissions are a separate issue and do not disprove that water-saving claim.

Crusoe reports higher lifecycle and maintenance costs, but gives no priced alternative or water-price assumptions. Compare equipment, electricity, water availability, treatment and upkeep before claiming a universal cost winner. The title poses a question; it does not establish deception.

<!-- speaker: integrated-cases#abilene-parallel-build -->

Crusoe’s September 2026 release reports more than 2,500 switchboards supplied from Tulsa to Abilene. Factory assembly and site construction could proceed in parallel before installation and testing. The current factory photo does not establish that the newly opened second plant supplied the first 2025 phase.

<!-- speaker: integrated-cases#abilene-capital -->

Crusoe builds and operates the campus; Oracle supplies GPU cloud infrastructure; OpenAI uses the capacity. Blue Owl-managed funds provide institutional project capital, with Primary Digital as investment and co-sponsorship partner.

The facility’s rent and property value support the investment. Ownership shares, contributions, fees and returns are undisclosed. Keep facility financing separate from Oracle’s GPU purchases and OpenAI’s compute bill.

<!-- speaker: integrated-cases#abilene-live-expansion -->

Early workloads ran while construction continued. The next power, cooling and network connections had to preserve service to the live phase. The diagram illustrates that requirement, not an as-built switching procedure.

<!-- speaker: integrated-cases#abilene-system -->

“Start at the rack. The GB200 workload sets requirements for power, cooling and fast connections. Across a hall, those become distribution and cooling systems serving rows of machines. Across the campus, they require substations, outdoor cooling, generation, land and financing. A hardware choice becomes a facility design.”

<!-- speaker: integrated-cases#watts-to-work -->

“We started with electricity at the site boundary. You can now follow it all the way to computation, and follow the heat back out. That is the physical system behind every token.”

Sources: [ChatGPT prompt](CHAPTER_16_CLOSING_IMAGE_PROMPT.md), [original Abilene evidence](../research/abilene-finale-evidence-2026-09-18.md), [revision evidence and photographs](../research/finale-review-evidence-2026-09-18.md), [Crusoe cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), [Trane maintenance comparison](https://www.trane.com/commercial/north-america/canada/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html), [Crusoe’s initial venture](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), [Kirkland’s account of Blue Owl and Primary Digital’s roles](https://www.kirkland.com/news/press-release/2025/01/kirkland-ellis-advises-bo-funds-on-jv-and-financing-for-development-of-adc).

## Queue purpose — Chapter 17, slide 1

<!-- speaker: grid-queues#queue-purpose -->

A connection request starts with a place, an amount of power, and a desired date. It asks the utility and grid operator to work out what serving that load would require. The result may involve studies, new equipment, construction, and limits on how the site operates. ERCOT and PJM face the same basic question, but their processes differ. We will follow what each milestone actually establishes, from an early request to a computing campus that can use its power.

Source: P235 — [FERC, June 18, 2026, existing PJM processes, pp. 19–21](https://www.ferc.gov/sites/default/files/2026-06/EL26-67-000.pdf); E21653C0173 — [ERCOT Batch Zero announcement](https://www.ercot.com/news/release/06182026-puct-approves-ercots).

## Two queues — Chapter 17, slide 2

<!-- speaker: grid-queues#two-queues -->

Start by checking which side of the network a request belongs to. A generator proposes to supply power. A data center asks to consume it. In August 2026, PJM reported 715 generation projects totaling 201.5 gigawatts of nameplate capacity qualified for study. That is a supply pipeline, not waiting data centers. Some load-related transmission requests can share PJM’s New Services Queue, so the label alone is not enough. We need the request type and the actual study status.

Source: P234 — [PJM, August 3, 2026](https://insidelines.pjm.com/over-700-new-generation-projects-accepted-into-first-cycle-of-reformed-interconnection-process/); P235 — [FERC, pp. 19–21](https://www.ferc.gov/sites/default/files/2026-06/EL26-67-000.pdf).

## ERCOT pipeline — Chapter 17, slide 3

<!-- speaker: grid-queues#ercot-pipeline -->

This is ERCOT’s June 2026 snapshot of large-load requests through 2033. The total reaches 474.7 gigawatts, but 284.3 gigawatts sits in the no-studies-submitted category. The observed energized segment is 5.9 gigawatts. Even that number needs its definition: it adds non-simultaneous peak consumption, rather than measuring everything at one instant. The chart compares stages of maturity. It does not show that the difference has been cancelled, and the future-year totals should not be added together.

Source: P227 — [ERCOT July 29 presentation, slide 6](https://www.ercot.com/files/docs/2026/07/29/ERCOT-Senate-July-29-Panel-1-Assessing-The-Grid.pdf#page=6); P228 — [ERCOT status definitions](https://www.ercot.com/files/docs/2026/04/16/ERCOT-Monthly-Operational-Overview-March-2026.pdf).

## Site options — Chapter 17, slide 4

<!-- speaker: grid-queues#site-options -->

Imagine one business that wants to deploy a gigawatt of computing. It explores three possible sites and requests a gigawatt at each. There are now three gigawatts of requests, but the business intends to choose just one site. Early engineering can be inexpensive compared with a campus, which makes preserving options useful. The challenge is to identify when those options become separate, credible commitments. This is an illustrative example, not an estimate of ERCOT’s duplicate requests. Texas now requires disclosure of materially overlapping requests.

Source: P229 — [Texas SB 6, PURA 37.0561(d)](https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00006F.htm). The one-business, three-site example is hypothetical.

## SemiAnalysis comparison — Chapter 17, slide 5

<!-- speaker: grid-queues#ercot-analyst -->

SemiAnalysis makes that concern concrete with its own comparison. ERCOT’s April 2026 requests totaled about 410 gigawatts, including roughly 357 gigawatts of data centers. The publisher places those requests beside 45.4 gigawatts in its tracked buildout through the end of 2030. This is an analyst’s classification using different coverage and horizons. It is useful evidence to examine, but it is not an ERCOT finding that every untracked megawatt is duplicated, fraudulent, or cancelled.

Source: SA33 — [SemiAnalysis, June 18, 2026, public ERCOT comparison](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter).

## Commitment costs — Chapter 17, slide 6

<!-- speaker: grid-queues#commitment-costs -->

Texas adopted these rules on September 18, with effect from October 8. The study fee is $100,000, and unused amounts return after the study. Intermediate-agreement security is a separate $50,000 per megawatt. For a gigawatt, that is a $50 million face amount of financial assurance, not necessarily $50 million spent in cash. The later standard agreement can require more security if allocated system upgrades cost more. These commitments make an application materially different from an early expression of interest. As of September 20, the newly adopted rule is not yet effective.

Source: P230 — [PUCT final rule, printed pp. 234–235 and 251–252](https://interchange.puc.texas.gov/Documents/58481_218_1684656.PDF#page=35); P236 — [effective-date acknowledgment, p. 3](https://interchange.puc.texas.gov/Documents/58481_219_1684678.PDF#page=3).

## Batch Zero — Chapter 17, slide 7

<!-- speaker: grid-queues#batch-zero -->

Batch Zero is another filter. ERCOT reported about 205 gigawatts preliminarily eligible using its July 28 snapshot. Eligibility gets a project into a study process; it does not authorize that load to switch on. In September, ERCOT was still requesting documents to verify conditionally included projects. The July eligibility numbers also cover a different population from the June pipeline. We cannot subtract one from the other and call the remainder cancelled. Each figure answers a different question.

Source: P231 — [ERCOT August 19 presentation, slide 3](https://www.ercot.com/files/docs/2026/08/19/ERCOTPanel1DataCenters.pdf#page=3); P232 — [September 9 verification notice](https://www.ercot.com/services/comm/mkt_notices/M-A090926-01).

## Dominion contracts — Chapter 17, slide 8

<!-- speaker: grid-queues#dominion-contracts -->

Dominion gives us a clear utility example inside PJM. An engineering authorization comes with a $250,000 deposit and a study typically lasting nine to twelve months. That study identifies infrastructure, estimated cost, and an estimated energization date. A construction authorization then reserves capacity and creates construction and cancellation obligations. The electric service agreement establishes the contracted service and its terms. These are progressively stronger commitments. They are Dominion’s process, not universal PJM rules, and an estimated energization date is still an estimate.

Source: P233 — [Dominion January 6, 2026 letter, p. 2](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/dominion-documentation.pdf#page=2).

## Dominion demand — Chapter 17, slide 9

<!-- speaker: grid-queues#dominion-demand -->

Now read Dominion’s headline carefully. Its July 2025 contract snapshot totaled 47 gigawatts: 30.1 in engineering authorizations, 7.1 in construction authorizations, and 9.8 in electric service agreements. The same letter reports a four-gigawatt coincident data-center peak in 2025. Contracted capacity and simultaneous demand are different measurements. Customers ramp their use, and the contracts represent different stages. These bars should make us more precise about the headline; they do not show that forty-three gigawatts was cancelled.

Source: P233 — [Dominion January 6, 2026 letter, pp. 1–3](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/dominion-documentation.pdf).

## Forecast filter — Chapter 17, slide 10

<!-- speaker: grid-queues#forecast-filter -->

A planner still has to decide what belongs in the demand forecast. This historical ERCOT figure compares 208 gigawatts submitted for 2030 with an adjusted forecast of 138 gigawatts. It covers the whole system, not only data centers. Adjusting a forecast means choosing assumptions about which loads arrive and when they ramp. It does not mean energizing those loads, and this 2025 forecast adjustment is not a rule for discounting every request today.

Source: SA32 — [SemiAnalysis, March 3, 2026, ERCOT-credited 2025 forecast figure](https://newsletter.semianalysis.com/p/are-ai-datacenters-increasing-electric).

## Staged connection — Chapter 17, slide 11

<!-- speaker: grid-queues#staged-connection -->

This ERCOT workshop illustration has a thousand-megawatt load, a hundred-megawatt grid withdrawal limit, and two five-hundred-megawatt onsite generators. Grid power alone supports at most a hundred megawatts. One generator raises the simple power bound to six hundred. Both can cover the pictured thousand-megawatt load. But the import limit remains. If one generator is lost at full load, at least four hundred megawatts falls out of this balance and demand may need prompt reduction. Actual ramp and stability limits can be tighter. This explains a mechanism, not an approved project schedule.

Source: P237 — [ERCOT May 4, 2026 workshop, slide 38](https://www.ercot.com/files/docs/2026/05/04/ERCOT_Batch_Study_Workshop_8_20260504.pptx); SA07 — [SemiAnalysis reproduction](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw).

## Connection terms — Chapter 17, slide 12

<!-- speaker: grid-queues#connection-terms -->

The useful result of the connection process is a service arrangement we can build and operate around. It gives us a confirmed import limit, a supported ramp with dates, clear responsibility for construction, and operating conditions that describe what happens when supply is constrained. A gigawatt requested tells us the ambition. These terms tell us which phase can actually open. That is how we compare two sites or two connection offers: by the usable service they can deliver to the computing plan.

Source: Synthesis from P229/P230 commitments, P233 utility service stages, and P237 operating example; [Dominion service definitions](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/dominion-documentation.pdf) and [ERCOT staged mechanism](https://www.ercot.com/files/docs/2026/05/04/ERCOT_Batch_Study_Workshop_8_20260504.pptx).
