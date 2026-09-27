# Selected speaker notes

## Source, circuit and load — Chapter 1, slide 1

<!-- speaker: primer#circuit -->

The source supplies electrical energy. The load receives it, for example to run electronics or produce heat. Current needs a complete path from the source through the load and back.

Opening the switch breaks that path, but voltage still exists across the open switch. Charge circulates; the load does not use it up.

Sources: evidence and teaching assumptions for every Primer slide are in [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). This is a simple steady circuit. The arrows show conventional current, not how fast electrons travel.

## Volts and amperes — Chapter 1, slide 2

<!-- speaker: primer#voltage-current -->

Voltage is electric potential difference, energy per unit charge, in volts (V). Current is the rate of charge flow, in amperes (A), often called amps. The resistor has 12 V across it and 2 A through it.

The outward and return wires each carry the same 2 A; adding them counts the loop current twice.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). Voltage alone does not give the current; that also depends on the load.

## Resistance and loss — Chapter 1, slide 3

<!-- speaker: primer#resistance -->

Resistance, in ohms (Ω), relates voltage and current in this resistor model: V = I × R. At a fixed 6 Ω, 12 V gives 2 A and 24 V gives 4 A.

Resistive heating is I²R: doubling the current gives four times the heat, 24 W to 96 W.

A regulated server is not a fixed resistor: its current can change to maintain the power it receives.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). Wires also have resistance.

## Watts — Chapter 1, slide 4

<!-- speaker: primer#power -->

A watt (W) is one joule of energy transferred per second: an amount per unit time, not the speed at which energy or a signal travels along a wire.

For this steady direct-current (DC) load, P = V × I: 12 V × 2 A = 24 W, so the load receives 24 joules each second.

Sources: [NIST guide to SI units, W = J/s](https://www.nist.gov/pml/special-publication-811/nist-guide-si-chapter-4-two-classes-si-units-and-si-prefixes). Voltage and current are both measured at the load: across it and through it.

## Watt-hours and scale — Chapter 1, slide 5

<!-- speaker: primer#energy -->

Energy is power multiplied by time, using the average power over that time. A 1 kW load running for 2 hours uses 2 kWh. A kilowatt-hour is energy, not power per hour.

k = thousand, M = million and G = billion, so 1 MW = 1,000 kW and 1 GW = 1,000 MW. A battery’s kWh rating is its stored energy; its kW limit is how fast it can deliver it.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). The same decimal prefixes apply to watt-hours.

## AC, DC and frequency — Chapter 1, slide 6

<!-- speaker: primer#ac-dc -->

Each trace is the voltage at the left terminal of the resistor below it, relative to the right. DC stays positive, so current flows left to right.

Alternating current (AC) reverses polarity. At the positive peak, current flows left to right. At the negative peak the right terminal is higher, so current flows right to left. At the zero crossing this resistor carries no current.

Frequency counts full AC cycles per second, in hertz (Hz).

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). The DC trace is kept flat so that the only new idea here is polarity; a DC level that changes comes later, with voltage variation. Current here means conventional current. The resistor is ideal; other loads can shift or reshape the current.

## AC waveform shapes — Chapter 1, slide 7

<!-- speaker: primer#ac-shapes -->

AC voltage need not be a sine wave: the sine, square, triangle and sawtooth examples all reverse polarity. Utility voltage is normally close to sinusoidal. The other shapes are examples from signals and power electronics, not normal utility supply.

Sources: [Tektronix, Oscilloscope Basics](https://www.tek.com/de/documents/primer/oscilloscope-basics).

## Voltage variation — Chapter 1, slide 8

<!-- speaker: primer#voltage-variation -->

Nominal voltage is a named reference level. Actual voltage varies with the source, the load and the wiring. The buttons compare levels 10% below and above nominal.

The DC level changes size and stays positive. The AC peak changes size while its polarity keeps alternating. These are teaching values, not safe operating ranges for equipment.

Sources: [Rohde & Schwarz, Testing AC/DC Converters, pp. 26–30](https://scdn.rohde-schwarz.com/ur/pws/dl_downloads/dl_application/application_notes/1sl387/1SL387_2e_TestingACDC_Converters.pdf). These are two separate 12 V examples: a DC level and an AC peak. Mains AC is usually quoted as a root-mean-square (RMS) value instead of a peak. A DC voltage can also carry ripple: an AC component on top of its DC level.

## Three-phase AC — Chapter 1, slide 9

<!-- speaker: primer#three-phase -->

Three-phase AC is the predominant form of AC power distribution in data centers, although individual loads can use single-phase AC or DC. The three phase voltages are staggered by 120 degrees, one-third of a cycle, so their peaks occur at different times.

A rack spreads its single-phase power supply unit (PSU) loads across the phases. Each PSU uses two current-carrying conductors: phase and neutral, or two phases.

Sources: [Eaton, Cabinet and floor-standing PDUs](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/power-distribution-for-it-equipment/power-distribution-unit-faq/cabinet---floor-standing-pdu-solutions.html). In this balanced example the three phase voltages have equal amplitudes. Each PSU connects according to its input rating. A quoted AC voltage is usually its RMS value: the effective magnitude that gives the same average heating in a resistor as an equal DC voltage. These traces are measured to neutral; line-to-line voltage is measured between two phase conductors.

## Three-phase power — Chapter 1, slide 10

<!-- speaker: primer#three-phase-power -->

The straight trace is total instantaneous power, not voltage. Each phase’s power is its voltage times its current: here 20 sin²(θ + phase offset) kW, from zero to 20 kW, averaging 10 kW.

Add the three at the same instant: 0 + 15 + 15 at 0°, 5 + 20 + 5 at 30°, 15 + 15 + 0 at 60°. Each sum is 30 kW: the total of all three phases, not the largest trace.

Sources: [Introduction to Electrical Power Engineering, Power and Energy](https://pb.ee.pw.edu.pl/pb/iepe/chapter/power-and-energy/). This balanced example uses three equal resistors, so each current is in phase with its voltage, and each supply voltage stays sinusoidal. Balanced sinusoidal loads also keep a constant total when every phase’s current lags its voltage by the same angle. Imbalance and waveform distortion can make the total ripple.

## Power factor — Chapter 1, slide 11

<!-- speaker: primer#power-factor -->

Power at each instant is voltage times current. When current lags voltage, their signs differ for part of the cycle and energy flows back toward the supply.

The voltage has not fallen, yet the same 8 kW takes 25% more current at power factor (PF) 0.8 than at PF 1. That current uses wiring and supply capacity and adds resistive loss.

PF is real power in kW divided by apparent power in kVA, kilovolt-amperes: 8 kW ÷ 8 kVA = 1 and 8 kW ÷ 10 kVA = 0.8. The extra 2 kVA is not 2 kW of wasted heat.

Sources: [Schneider Electric, Understanding True Power Factor](https://blog.se.com/energy-management-energy-efficiency/2020/02/20/distortion-displacement-and-the-truth-understanding-true-power-factor/). With the waves in step, energy flows in through both halves of the cycle. When current lags, the same RMS current transfers less net energy per cycle, so the same average power at the same supply voltage needs more RMS current. The voltage and current traces have separate scales, fixed between the two cases. For sinusoidal voltage and current, PF equals the cosine of the angle between them. Distorted current can also lower power factor: electronic power supplies can draw pulses instead of a smooth sine wave. Power factor applies to single-phase and three-phase systems and is separate from conversion efficiency.

## Conversion equipment — Chapter 1, slide 12

<!-- speaker: primer#conversion -->

A transformer changes an AC voltage level through magnetic coupling. A rectifier converts AC to DC; an inverter converts DC to AC. A DC–DC converter changes a DC voltage level.

A PSU prepares the electrical output that equipment needs and can contain several stages. A power shelf groups power supplies and distributes their output within a rack.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). These names identify functions, not one required architecture. Real equipment has losses and operating limits.

## Transformer input range — Chapter 1, slide 13

<!-- speaker: primer#transformer-operating-range -->

A real transformer’s rating specifies its input. Schneider Electric’s Phaseo ABL6TS25B is rated 250 volt-amperes (VA): 400 V AC nominal input, 24 V AC output rating. On the 400 V connection the manufacturer permits 360 to 440 V, 10% either side.

The turns ratio is fixed, so the transformer does not regulate: the output moves with the input. 24 V is the rating, not a constant output.

Sources: P159, [Schneider Electric Phaseo ABL6TS25B datasheet](https://iportal.se.com/Contents/docs/SQD-ABL6TS25B_DATASHEET.PDF), page 1: ratings, input limits and the photograph; [Schneider Electric, transformer taps and input voltage](https://www.se.com/us/en/faqs/FA120846/). The fixed turns ratio applies on a given connection. The 230 V connection has its own range, 207 to 253 V, and the supply frequency must be 47 to 63 Hz. A transformer works on AC, and each one’s permitted input depends on its rating and connection. This one is a small controls transformer, not one of the large transformers that supply a data hall.

## UPS, battery and generator — Chapter 1, slide 14

<!-- speaker: primer#backup -->

A UPS, or uninterruptible power supply, keeps its protected load supplied when the normal source is interrupted. A battery stores energy; it is one possible part of that system.

In this online UPS, the rectifier feeds a DC link and the inverter supplies the load. The battery supports the link during an upstream interruption; a generator can take over upstream after it starts and qualifies. Runtime is finite.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). Related terms: switchgear switches and protects circuits, and a breaker can interrupt a circuit. A busbar is a conductor used for distribution, and a rack power distribution unit (PDU) distributes power to the equipment in a rack.

## Offline and online UPS — Chapter 1, slide 15

<!-- speaker: primer#ups-types -->

An offline, or standby, UPS normally passes utility AC straight to the load. When the supply fails, it switches to a battery-powered inverter after a brief transfer.

An online double-conversion UPS normally runs power through a rectifier, a DC link and an inverter. When the battery takes over the DC link, the inverter keeps feeding the load with no transfer break.

Offline designs are common for home computers and desktop equipment; online systems are often chosen for critical data-center loads and sensitive medical systems.

Sources: [Eaton, Types of UPS systems](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/types-of-ups-systems.html), [Eaton, Powering Healthcare Systems](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/Safeguarding-power-equipment-in-the-healthcare-industry.html). The application decides which design suits; medical equipment does not all need the same UPS. These are simplified normal and battery paths: charging, bypass operation and faults are left out, and stored runtime is finite.

## Load, rating and redundancy — Chapter 1, slide 16

<!-- speaker: primer#capacity -->

Load is actual demand. A rating states a component’s capability under specified conditions. Here a 100 kW load needs two 50 kW modules, so N = 2. N+1 adds one spare module: if a module fails, two remain.

Shared paths, controls and cooling can still stop the service. Redundancy is extra provision; availability describes service over a defined period.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). Capacity also needs a boundary and operating conditions. The system is illustrative, and this is a simplified capacity check. N+1 alone does not establish availability or an Uptime Institute Tier classification.

## Rack, server, CPU and GPU — Chapter 1, slide 17

<!-- speaker: primer#hardware -->

A rack is a frame for mounting equipment. In this compute server, the central processing unit (CPU) coordinates work, system random-access memory (RAM) holds active data, and the graphics processing unit (GPU) does the parallel numerical work used to run many AI models.

The GPU has its own memory beside its cores. Our model’s saved data has to reach that memory before the GPU can run it.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). A cluster is a coordinated collection of connected machines. This simplified server is an example, not a particular vendor’s configuration.

## Memory and storage — Chapter 1, slide 18

<!-- speaker: primer#memory-storage -->

Storage keeps data when power is off; working memory holds data while the computer runs. Our saved model is on a storage server elsewhere in the data center.

Follow the loading path: across the network into the compute server’s system RAM, then copied into GPU memory, where the GPU cores use it. Memory capacity, measured in GB, sets how much model data can fit.

Sources: [NVIDIA, GPUDirect Storage Overview](https://docs.nvidia.com/gpudirect-storage/overview-guide/). Many accelerators use high-bandwidth memory (HBM). This example uses a buffered loading path; direct storage-to-GPU paths also exist. The boxes are separate memories, not one automatically shared pool.

## Bandwidth and latency — Chapter 1, slide 19

<!-- speaker: primer#network -->

Bandwidth is how much data the path carries per second. Latency is how long a defined event takes: here the first bit arrives after 10 microseconds, or 0.01 ms, at either rate.

The 8 MB chunk is 64 megabits, because one byte (B) is eight bits (b). At 10 Gb/s, sending takes 6.4 ms and the last bit arrives at 6.41 ms. At 100 Gb/s, sending takes 0.64 ms and the last bit arrives at 0.65 ms.

More bandwidth shortens the transfer; the first-bit latency stays the same.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). Both endpoints, a storage server and a compute server, are in the same data center. The chunk is part of the model, not the whole model; megabytes here are decimal and the rates are ideal payload rates. These are teaching assumptions, not measured performance or a product specification. The data is already in the sender’s buffer; storage reads, host-memory copies, queues, protocol overhead and retransmissions are outside this simplified account.

## Heat and temperature — Chapter 1, slide 20

<!-- speaker: primer#heat-temperature -->

The running GPU turns the electrical energy it uses into heat that must leave the chip: 500 W in, 500 W out through the cold plate, or 500 joules each second.

Temperature tells us how hot a place is: GPU 70 °C, cold plate 45 °C, coolant in at 30 °C and out at 35 °C. A temperature alone does not give the heat-transfer rate; that also depends on the thermal path.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). This is a simplified steady state; other heat paths and changes in stored energy are negligible. The heat-transfer rate also depends on operating conditions. The values are illustrative, not GPU or cooling-product ratings.

## Cold plate, coolant and CDU — Chapter 1, slide 21

<!-- speaker: primer#cooling -->

A cold plate is a heat exchanger attached to the chip. Coolant flows through it and carries the heat to a coolant distribution unit (CDU).

The CDU transfers that heat into a separate facility loop without mixing the two fluids, and that loop carries it to the outdoor plant. Pumps circulate the coolant; pumps and fans need electricity too.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). This is a liquid-to-liquid example; liquid-to-air CDUs also exist. Outdoor equipment rejects the heat: a chiller uses refrigeration to cool fluid, and a dry cooler transfers heat to outdoor air. The diagram follows the GPU’s liquid cooling path; other equipment may still need air cooling.

## Facility energy and PUE — Chapter 1, slide 22

<!-- speaker: primer#pue -->

Now count the whole facility for one hour. Information technology (IT) equipment, all servers, networking and storage, uses 100 kWh. Cooling, power-system losses and other support add 20 kWh: 120 kWh in total.

Power usage effectiveness (PUE) is total facility energy divided by IT energy: 120 ÷ 100 = 1.20. It describes facility overhead, not how much computation the IT equipment performed.

Sources: [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md). The GPU needs electricity to compute, and its cooling system needs electricity to move heat. The hour is illustrative. The numerator already includes IT, and both measurements cover the same interval. This is a new facility-wide example, not the consumption of our single 500 W GPU. One illustrative hour does not establish an annual PUE.

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

## An 800 V DC battery rack beside the compute rack — Chapter 9, slide 9

<!-- speaker: dc-distribution#dc-battery-rack -->

Here, medium-voltage AC is converted to 800 V DC upstream of the racks. The adjacent battery rack routes that DC supply onward to the compute rack through its distribution shelves. Battery shelves shave demand peaks, while capacitor shelves buffer faster power swings. The 800 kW rating and Kyber–Rubin Ultra name belong to this proposal.

Sources: [SemiAnalysis: Inside the 800VDC Revolution, Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part).

## Should we step down first or rectify first? — Chapter 9, slide 11

<!-- speaker: dc-distribution#ac-dc-ledger -->

“New higher-voltage silicon carbide (SiC) devices could make solid-state transformers (SSTs) simpler and more competitive. Their widespread adoption in data centers still has to be demonstrated.”

Sources: [Wolfspeed 10 kV SiC announcement](https://www.wolfspeed.com/company/news-events/news/wolfspeed-introduces-industrys-first-commercially-available-10000v-silicon-carbide-power-mosfet/).

## An 800 V DC feeder needs DC-rated protection — Chapter 9, slide 13

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

Cold plates can leave some heat in the rack’s exhaust air. A rear-door heat exchanger (RDHX) captures that heat into liquid; room-air handlers are another option. The NVIDIA coolant manifold pictured alongside is not itself a rear-door exhaust coil. The Abilene evidence does not establish one residual-air arrangement across every hall.

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

The cold plates collect 85 kW, leaving 15 kW in air. That uses 15 kW of the room’s 20 kW allowance, or a suitable rear-door heat exchanger (RDHX) can move it into liquid. The example assumes the door captures all of that remaining 15 kW.

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

Uberflip’s CTO reported cold-side cabinet air above 43°C, thermal shutdowns, deliberate shutdown of nonessential machines and service transfers. Data Center Knowledge reported that Enwave supplied an emergency chiller, which gave some relief until the system was restored. The lake still held cold water; the equipment needed to deliver that cooling was the dependency.

Sources: P242 [Enwave / Toronto Water](https://www.enwave.com/case-studies/enwave-and-toronto-water-tap-into-innovative-energy-source), P243 [Hydro One, July 8, 2013](https://www.newswire.ca/news-releases/hydro-one-power-outages-due-to-heavy-rains-512697891.html), P244 [Data Center Knowledge, July 9, 2013: PEER1’s statement and the reporter’s emergency-chiller account](https://www.datacenterknowledge.com/outages/toronto-flooding-kos-data-center-cooling-systems), P245 [Uberflip CTO's July 9 report](https://seclists.org/nanog/2013/Jul/130).

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

Sources: P255 [CoolIT Split-Flow tech brief, May 8, 2024, Figure 2: cold-plate thermal resistance versus flow, archived April 19, 2025](https://web.archive.org/web/20250419054125/https://www.coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf).

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

In the 2023 Northern Wasco County People’s Utility District (PUD) pilot, the utility requested a day-ahead reduction during busy grid hours.

<!-- speaker: operations#google-demand-response-workloads -->

Video processing and Translate updates could wait while Search, Maps and video playback continued. Those are Google’s examples, not a claim that arbitrary interactive requests can be paused.

<!-- speaker: operations#deadline-scheduling -->

Pausing the 4 MW job from 14:00 to 16:00 shifts completion from 16:00 to 18:00, before its 20:00 deadline. Both schedules use 12 MWh, but event demand falls from 24 to 20 MW. This example assumes restart without penalty and sufficient later capacity.

Sources: [Google Cloud, October 2023](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption).

## Cloudflare’s failure, correction and retest — Chapter 14, slides 15–17

<!-- speaker: operations#cloudflare-pdx -->

The November 2023 Portland power loss disrupted dashboard, API and analytics services. Multi-site services still depended on Kafka and ClickHouse at PDX-04. Earlier tests removed only its high-availability (HA) portion, not the whole facility.

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

The choice is who operates inference. Your team can run the serving stack itself on CoreWeave Kubernetes Service (CKS), an option CoreWeave calls Inference on CKS, or CoreWeave can run it through Dedicated Inference. You supply the model and application in both.

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

NVIDIA’s Form 10-Q for the quarter ended July 26, 2026 describes typically six-year support for cloud capacity, allowing providers to offer shorter customer rentals. It is not an unconditional guarantee of the provider’s debts.

<!-- speaker: capacity#nvidia-backstop-risk -->

The $36 billion figure is NVIDIA’s aggregate commitment as of July 26, 2026, not a realized loss. Buying unused capacity provides a revenue floor while leaving NVIDIA exposed if customers do not fill it.

<!-- speaker: capacity#gpu-hour-cost -->

Idle GPUs can still consume power. Here 80 rented hours at 1 kW plus 20 idle hours at 0.2 kW use 84 kWh. Spread across 80 billed hours, that is 1.05 kWh per billed GPU-hour.

At $80/MWh it costs $0.084; at $160/MWh, $0.168. These are assumed site allocations, not device specifications. Rented time does not mean continuous maximum-power computing.

<!-- speaker: capacity#electricity-pass-through -->

The extra $0.084 per billed GPU-hour reduces provider margin under a fixed fee, or reaches the customer under full reimbursement. Core Scientific’s colocation agreement passes power costs to CoreWeave without markup. That does not establish CoreWeave’s GPU-cloud customer terms.

<!-- speaker: capacity#abilene-roles -->

Crusoe builds the facility, Oracle supplies cloud capacity through Oracle Cloud Infrastructure (OCI) and OpenAI runs workloads. Their responsibilities sit at different points in the delivery chain.

<!-- speaker: capacity#datacenter-delay-quote -->

“For one concrete case, let’s compare Abilene’s original plan with its reported delivery.”

The article challenges aggregate delay headlines, not the existence of individual delays.

<!-- speaker: capacity#abilene-ledger -->

Compare each target with the corresponding reported milestone. Energization, construction completion and delivered capacity are different events; mismatched milestones cannot establish an exact schedule slip.

Sources: P222 [CoreWeave Dedicated Inference and Inference on CKS](https://www.coreweave.com/products/dedicated-inference), P253 [Anthropic–CoreWeave agreement](https://www.coreweave.com/news/coreweave-announces-multi-year-agreement-with-anthropic), P254 [Cursor–Fireworks case](https://fireworks.ai/blog/cursor), P250 [CoreWeave Form 8-K, September 15, 2025, the $6.3 billion NVIDIA order](https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm), P251 [NVIDIA Form 10-Q for the quarter ended July 26, 2026, commitments typically six years, $36 billion](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm), SA35 [SemiAnalysis, July 6, 2026, GPU debt backstop](https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes), SA44 [SemiAnalysis, September 11, 2026, Nvidia’s Backstop Universe](https://newsletter.semianalysis.com/p/nvidias-backstop-universe-heads-i), [idle-system power model](https://docs.nvidia.com/datacenter/dps/versions/latest/guides/reference/apis/v1/devices.html), P252 [Core Scientific Q2 2026 filing, Electricity Costs](https://www.sec.gov/Archives/edgar/data/1839341/000183934126000014/core-20260630.htm), SA33 [SemiAnalysis’s June 18, 2026 article](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter).

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

Sources: [ChatGPT prompt](CHAPTER_16_CLOSING_IMAGE_PROMPT.md), [original Abilene evidence](../research/abilene-finale-evidence-2026-09-18.md), [revision evidence and photographs](../research/finale-review-evidence-2026-09-18.md), P74 [Crusoe cooling design](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center), P49 [Trane maintenance comparison](https://www.trane.com/commercial/north-america/us/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html), P267 [Crusoe’s initial venture](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture), P268 [Crusoe’s May 21, 2025 second phase of the $15 billion venture](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture), P269 [Kirkland’s account of Blue Owl and Primary Digital’s roles](https://www.kirkland.com/news/press-release/2025/01/kirkland-ellis-advises-bo-funds-on-jv-and-financing-for-development-of-adc), P270 [Crusoe, September 14, 2026: second Tulsa facility and more than 2,500 switchboards for Abilene](https://www.crusoe.ai/resources/newsroom/crusoe-opens-second-tulsa-factory-ai-infrastructure).

## Queue purpose — ERCOT and PJM case study, slide 1

<!-- speaker: grid-queues#queue-purpose -->

Chapter 4 ended ready to build the site. Before we do, a detour: how two real grids decide who connects.

Request = study with the utility and grid operator. ERCOT, the Electric Reliability Council of Texas, is the grid for most of Texas. PJM Interconnection runs it for 13 eastern states and Washington, D.C.

Source: P235 — [FERC, June 18, 2026, existing PJM processes, pp. 19–21](https://www.ferc.gov/sites/default/files/2026-06/EL26-67-000.pdf); E21653C0173 — [ERCOT Batch Zero announcement](https://www.ercot.com/news/release/06182026-puct-approves-ercots). Logos: [asset provenance](assets/references/grid-queues-logos.provenance.json).

## Chips need power — ERCOT and PJM case study, slide 2

<!-- speaker: grid-queues#chips-need-power -->

Hardware cannot power itself. Nadella, BG2 podcast, October 2025: chips in inventory he can’t plug in.

Source: P238 — [BG2 podcast, October 31, 2025, at 18:29](https://www.youtube.com/watch?v=Gnl833wXRz0&t=1109s); P239 — [Microsoft FY26 Q1 earnings call, October 29, 2025](https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q1). One company’s dated statement; his constraint includes building construction as well as the utility connection.

## ERCOT pipeline — ERCOT and PJM case study, slide 3

<!-- speaker: grid-queues#ercot-pipeline -->

ERCOT: 474.7 GW of large-load requests. Its tracked pipeline, as of June 2026; load requested by 2033. 284 GW: no study submitted to ERCOT, or reviewed and not approved. 136 GW: under review. 55 GW: study approved or further. 5.9 GW operating = each site’s peak, added up. Not a cancellation rate. If asked: the groups add to 474.8, not 474.7, because ERCOT’s rows are rounded.

Source: P227 — [ERCOT July 29 presentation, slide 6](https://www.ercot.com/files/docs/2026/07/29/ERCOT-Senate-July-29-Panel-1-Assessing-The-Grid.pdf#page=6); P228 — [ERCOT status definitions](https://www.ercot.com/files/docs/2026/04/16/ERCOT-Monthly-Operational-Overview-March-2026.pdf). The third group adds ERCOT’s rows 9.9 + 36.0 + 3.2 + 5.9 GW. The three groups sum to 474.8 GW (284.3 + 135.5 + 55.0) against the title’s 474.7 because ERCOT’s six rows are rounded. ERCOT’s monthly overviews for the same summer report slightly different totals; keep this deck’s date with its numbers.

## Site options — ERCOT and PJM case study, slide 4

<!-- speaker: grid-queues#site-options -->

One 1 GW project, three candidate sites = 3 GW of requests. Pick one; two requests vanish, nothing cancelled. Hypothetical. Texas Senate Bill 6 (SB 6, 2025) requires disclosure of overlapping requests.

Source: P229 — [Texas SB 6, PURA 37.0561(d)](https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00006F.htm). The one-business, three-site example is hypothetical.

## SemiAnalysis comparison — ERCOT and PJM case study, slide 5

<!-- speaker: grid-queues#ercot-analyst -->

SemiAnalysis: 410 GW requested in April 2026, about 357 GW data centers, versus 45.4 GW in its tracked buildout through 2030. Analyst classification, not an ERCOT finding.

Source: SA33 — [SemiAnalysis, June 18, 2026, public ERCOT comparison](https://newsletter.semianalysis.com/p/stop-saying-half-of-2026-us-datacenter).

## Commitment costs — ERCOT and PJM case study, slide 6

<!-- speaker: grid-queues#commitment-costs -->

New, not always like this. Before Texas Senate Bill 6 (SB 6), signed June 2025: no ERCOT-wide amount; each utility set its own terms. The Public Utility Commission of Texas (PUCT) adopted the rule on September 18, 2026. From October 8, 2026, requests of 75 MW or more: $100,000 study fee plus $50,000 per MW security, before ERCOT studies it. 1 GW = $50 million face amount; guarantee or letter of credit counts.

Source: P230 — [PUCT final rule, printed pp. 234–235 and 251–252](https://interchange.puc.texas.gov/Documents/58481_218_1684656.PDF#page=35); P236 — [effective-date acknowledgment, p. 3](https://interchange.puc.texas.gov/Documents/58481_219_1684678.PDF#page=3); P229 — [Texas SB 6](https://capitol.texas.gov/tlodocs/89R/billtext/html/SB00006F.htm); [PGRR145](https://www.ercot.com/mktrules/issues/PGRR145). Utility practice before SB 6 is from utility comments summarized in the PUCT adoption order; no source lists the amounts each utility charged.

## Dominion in PJM — ERCOT and PJM case study, slide 7

<!-- speaker: grid-queues#dominion-in-pjm -->

Dominion is not PJM. PJM = grid operator, 13 states and D.C., owns no lines. Dominion = the main utility in one of PJM’s 21 zones; Northern Virginia’s data centers. Data centers sign with the utility. Texas parallel: ERCOT and Oncor. As of mid-2026, PJM has no central large-load queue, so we read Dominion’s contracts.

Source: [PJM at a Glance](https://www.pjm.com/-/media/DotCom/about-pjm/newsroom/fact-sheets/pjm-at-a-glance.pdf): others own the lines; P240 — [PJM Transmission Zones map](https://www.pjm.com/-/media/DotCom/about-pjm/pjm-zones.pdf); P233 — [Dominion January 6, 2026 letter](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/dominion-documentation.pdf). [FERC, June 18, 2026, pp. 20–23](https://www.ferc.gov/sites/default/files/2026-06/EL26-67-000.pdf): load interconnection requests go to the transmission owners. Cooperatives in the zone, such as NOVEC, report their own data-center load to PJM.

## Dominion contracts — ERCOT and PJM case study, slide 8

<!-- speaker: grid-queues#dominion-contracts -->

Three stages. Engineering study: $250,000 deposit, 9–12 months, no obligation to build. Construction: customer repays spent costs if it leaves. Service agreement: pays whether or not it takes service. July 2026: 53.8 GW, of which 32.4 GW is studies. 2025 data-center peak: about 4 GW. Contracts are not demand.

Source: P241 — [Dominion Energy Q2 2026 earnings slides, July 31, 2026, slide 5](https://s2.q4cdn.com/510812146/files/doc_financials/2026/q2/2026-07-31-DE-IR-2Q-2026-earnings-call-slides-vTCII.pdf#page=5); P233 — [Dominion January 6, 2026 letter, pp. 1–3](https://www.pjm.com/-/media/DotCom/planning/res-adeq/load-forecast/dominion-documentation.pdf): deposit, study duration, 2025 coincident peak, and the July 2025 snapshot of 47 GW, which the reading keeps as the earlier point beside July 2026. The slide’s SELOA is the letter’s ELOA.

## Forecast filter — ERCOT and PJM case study, slide 9

<!-- speaker: grid-queues#forecast-filter -->

ERCOT 2025 forecast for 2030: 208 GW submitted, 138 GW adjusted. Whole system, not only data centers. A forecast is not energization.

Source: SA32 — [SemiAnalysis, March 3, 2026, ERCOT-credited 2025 forecast figure](https://newsletter.semianalysis.com/p/are-ai-datacenters-increasing-electric).

## Staged connection — ERCOT and PJM case study, slide 10

<!-- speaker: grid-queues#staged-connection -->

ERCOT illustration: 1,000 MW load, 100 MW grid limit, two 500 MW generators. 100, then 600, then 1,000 MW. The import limit stays; lose a generator and load must drop.

Source: P237 — [ERCOT May 4, 2026 workshop, slide 38](https://www.ercot.com/files/docs/2026/05/04/ERCOT_Batch_Study_Workshop_8_20260504.pptx); SA07 — [SemiAnalysis reproduction](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw).

## Behind-the-meter gap — ERCOT and PJM case study, slide 11

<!-- speaker: grid-queues#btm-gap -->

SemiAnalysis forecast, capacity added per year, in GW. Orange: spare grid capacity, gone after 2027. Green: new grid supply. Blue: the gap, met behind the meter; about 43 of 54 GW in 2028. Modeled gap, not contracted plants. A queue place buys a study and an import limit, not power on your schedule.

Back to our project. Chapter 5 takes the supply strategy to the parcel and turns it into a place we can build, operate and repair.

Source: SA07 — [SemiAnalysis, June 25, 2026, public figure](https://newsletter.semianalysis.com/p/us-grid-constraints-towards-40gw). Annual net additions in GW; the figure’s title says MW.
