# Primer background notes

Author reference for the diagrams. These notes are not displayed in the
presentation and prescribe no slide timings. Evidence and example assumptions
are recorded in [PRIMER_EVIDENCE.md](PRIMER_EVIDENCE.md).

## 1. Source, circuit and load

The source supplies electrical energy. The load receives it, for example to run electronics or produce heat. In this simple steady circuit, current needs a complete path from the source through the load and back. Opening the switch interrupts that path. Voltage can still exist across the open switch. Charge circulates; the load does not consume charge. The arrows represent conventional current, not electron travel speed.

## 2. Volts and amperes

Voltage is electric potential difference: energy per unit charge, measured in volts (V). Current is the rate of charge flow, measured in amperes (A), often called amps. In the example, the resistor has 12 V across it and 2 A through it. Both the outward and return wires carry 2 A. Adding those wire readings would count the same loop current twice. Voltage alone does not tell us the current without knowing the load.

## 3. Resistance and loss

Resistance, measured in ohms (Ω), relates voltage and current in this simple resistor model: V = I × R. With resistance fixed at 6 Ω, 12 V gives 2 A; 24 V gives 4 A. Resistive heating is I²R, so doubling current produces four times the heat at the same resistance. Wires also have resistance. A regulated server is not a fixed resistor; its current can change to maintain delivered power. This example holds resistance fixed.

## 4. Watts

A watt (W) is one joule of energy transferred per second. This is an amount per unit time, not the speed at which energy or an electrical signal travels along a wire. For the steady DC load shown, P = V × I: 12 V × 2 A = 24 W. The load receives 24 joules each second. Voltage and current describe the same receiving boundary.

## 5. Watt-hours and scale

Energy equals power multiplied by time when the power stays constant, or when we use its average over that interval. A 1 kW load running for 2 hours uses 2 kWh. A kilowatt-hour is a unit of energy, not power per hour. The decimal prefixes are k = thousand, M = million and G = billion. Thus 1 MW = 1,000 kW and 1 GW = 1,000 MW. The same prefixes appear on watt-hours. A battery’s kWh rating describes stored energy; its kW limit describes the rate it can supply.

## 6. AC, DC and frequency

The two terminals belong to the resistor drawn below each voltage trace. Voltage is measured at the left terminal relative to the right. In the first DC example, that voltage is constant and positive: current flows from left to right. At the positive AC peak the same is true. At the negative peak the right terminal is at the higher potential, so conventional current flows right to left. At zero voltage this ideal resistor carries zero current. Other loads can shift or reshape current. AC reverses voltage polarity; the first flat DC example establishes unchanged polarity without introducing voltage variation at the same time. Frequency counts full cycles per second in hertz (Hz).

## 7. AC waveform shapes

AC voltage need not be sinusoidal: the sine, square, triangle and sawtooth examples all reverse polarity. Utility voltage is normally approximately sinusoidal. The other shapes are signal and power-electronics examples, not normal utility supply.

## 8. Voltage variation

Nominal voltage is a named reference level. Actual voltage can vary with the source, load and wiring. The controls compare illustrative levels ten percent below and above nominal. The DC level remains positive while changing in magnitude. The AC peak changes in magnitude while its voltage continues to alternate polarity. These two separate 12 V examples use DC level and AC peak, not a mains RMS rating. They do not define safe operating ranges for equipment. A DC voltage may also contain ripple: an AC component superimposed on its DC level. Transformer ratings specify primary voltage and operating conditions, with taps on some products to accommodate supply variation. A fixed-ratio transformer does not automatically regulate its output: changing input voltage changes output voltage. Do not imply every transformer accepts an arbitrary range or operates on steady DC.

## 9. Three-phase AC

Three-phase AC is the predominant form of AC power distribution in data centers, although individual loads can use single-phase AC or DC. In this balanced example, the three phase voltages have equal amplitudes and are staggered by 120 degrees, or one-third of a cycle. Their peaks occur at different times. A quoted AC voltage usually uses RMS: the effective magnitude that produces the same average heating in a resistor as an equal DC voltage. The measurement points still matter: line-to-line voltage is measured between two phase conductors.

## 10. Three-phase power

The straight trace is total instantaneous power, not voltage. For each phase, instantaneous power equals its voltage multiplied by its current. This balanced sinusoidal example uses three equal resistors, with current in phase with voltage. Each phase delivers p = 20 sin²(theta + phase offset) kW: zero to 20 kW, averaging 10 kW. Sum the three phase powers at the same instant. At 0°, they are 0 + 15 + 15 = 30 kW; at 30°, 5 + 20 + 5 = 30 kW; at 60°, 15 + 15 + 0 = 30 kW. Their sum is 30 kW throughout the cycle. No phase is selected or discarded, and the total is not the maximum of the three traces. Each supply voltage remains sinusoidal. Balanced sinusoidal loads can also have constant total power at a common nonzero displacement angle; imbalance and waveform distortion can produce ripple in total power.

## 11. Power factor

Power depends on voltage and current together at each instant: multiply their instantaneous values. With sinusoidal waves in step, energy flows into the load throughout both halves of the cycle. When current shifts behind voltage, there are intervals when their signs differ and energy flows back toward the supply. The same RMS current now transfers less net energy per cycle. The supply voltage has not fallen: delivering the same average power at that voltage requires more RMS current. Here PF 0.8 needs 25% more current than PF 1 to deliver the same 8 kW. That current uses more wiring and supply capacity and increases resistive losses. Power factor quantifies this relationship: real power in kW divided by apparent power in kVA, or kilovolt-amperes. The two cases use 8 and 10 kVA respectively; the difference is not 2 kW of wasted heat. The traces use separate voltage and current scales, held fixed between the cases. For sinusoidal voltage and current, PF equals the cosine of their timing angle. Distorted current can also reduce power factor; electronic power supplies can draw pulses instead of a smooth sine wave. Power factor applies to single-phase and three-phase systems and is distinct from conversion efficiency.

## 12. Conversion equipment

A transformer changes an AC voltage level through magnetic coupling. A rectifier converts AC to DC; an inverter converts DC to AC. A power supply unit (PSU) prepares the electrical output needed by equipment and can contain several stages. A DC–DC converter changes a DC voltage level. A power shelf groups supplies and distributes their output in a rack. These names identify functions, not one mandatory architecture. Real equipment has losses and operating limits.

## 13. UPS, battery and generator

UPS means uninterruptible power supply: a system that supports its protected load when the normal source is interrupted. A battery stores energy and is one possible part of that system. In this online UPS example, its rectifier feeds a DC link and its inverter supplies the load. The battery supports the link during an upstream interruption. A generator can take over the upstream supply after it starts and qualifies. Runtime is finite. Switchgear switches and protects circuits; a breaker can interrupt a circuit. A busbar is a conductor used for distribution, and a rack PDU (power distribution unit) distributes power to equipment.

## 14. Offline and online UPS

An offline or standby UPS normally passes utility AC to the load. When the supply fails, it switches to an inverter powered by the battery, with a brief transfer interval. This topology is common for home computers and desktop equipment. An online double-conversion UPS normally sends power through a rectifier, a DC link and an inverter. Its inverter keeps feeding the load when the battery takes over the DC link, without the normal-to-battery transfer break of a standby UPS. Online systems are often chosen for critical data-center loads and sensitive medical systems. The application determines the suitable topology; medical equipment does not all require the same UPS. These are simplified normal and battery paths: charging details, bypass operation and faults are omitted, and stored runtime is finite.

## 15. Load, rating and redundancy

Load is actual demand. A rating states a component’s capability under specified conditions. Capacity needs a boundary and operating conditions too. In this illustrative system, a 100 kW load requires two 50 kW modules, so N = 2. N+1 adds one spare module. If a module fails, two remain in this simplified capacity screen. Shared paths, controls and cooling can still prevent service. Redundancy is additional provision; availability describes service over a defined period. N+1 alone does not establish availability or a Tier classification.

## 16. Rack, server, CPU and GPU

A rack is a frame for mounting equipment. Look inside this compute server: the CPU coordinates work, system RAM holds active data, and the GPU performs the parallel numerical work used to run many AI models. CPU means central processing unit; GPU means graphics processing unit. The GPU has memory close to its processing cores. Before those cores can run our model, its saved data has to reach that memory. A cluster is a coordinated collection of connected machines. IT means information technology and includes computing, networking and storage equipment. This simplified server is an example, not a particular vendor configuration.

## 17. Memory and storage

We want the GPU inside our compute server to run a saved model. The file is on a storage server elsewhere in the data center. Storage preserves the file when power is off; working memory holds data while the computer runs. Follow the loading path: the model data crosses the network into the compute server’s system RAM, then is copied into GPU memory. The GPU cores use the data there to compute. RAM means random-access memory; HBM means high-bandwidth memory, used by many accelerators. This example uses a buffered loading path; direct storage-to-GPU paths also exist. Memory capacity, measured in GB, determines how much model data can fit. The separate boxes are not one automatically shared pool of memory.

## 18. Bandwidth and latency

Zoom in on the network connection carrying model data to our compute server. The endpoints are a storage server and a compute server in the same data center. Bandwidth describes how much data the path can carry per second. Latency describes how long a defined event takes. Here the first bit reaches the receiving endpoint after an illustrative 10 microseconds, or 0.01 ms, at either selected rate. The payload is an 8 MB chunk of the model, not the entire model. One byte contains eight bits, so 8 decimal MB contains 64 megabits. Sending that chunk at an ideal payload rate of 10 Gb/s takes 6.4 ms; the last bit arrives at 6.41 ms. At 100 Gb/s, sending takes 0.64 ms and arrival takes 0.65 ms. More bandwidth shortens the transfer without changing the stipulated first-bit latency. These are teaching assumptions, not measured performance or a product specification. The data is ready in the sender’s buffer; storage reads, host-memory copies, queues, protocol overhead and retransmissions are outside this simplified network account. Lowercase b means bits; uppercase B means bytes.

## 19. Heat and temperature

The model has reached GPU memory and the GPU is computing. The electrical energy it uses becomes heat that must leave the chip. This simplified steady state accounts for 500 W of electrical input and 500 W leaving through the cold plate, with negligible other paths or stored-energy change. Watts tell us how fast energy moves: 500 joules each second. Temperature tells us how hot a particular location is: the GPU is at 70 °C and the cold plate at 45 °C. Coolant flows through the plate, entering at 30 °C and leaving at 35 °C as it carries the heat away. A temperature alone does not tell us the heat-transfer rate; that also depends on the thermal path and operating conditions. The values are illustrative, not GPU or cooling-product ratings.

## 20. Cold plate, coolant and CDU

Follow the heat leaving our GPU. A cold plate is a heat exchanger attached to the chip. Coolant flows through it and carries heat to a coolant distribution unit, or CDU. In this liquid-to-liquid example, the CDU transfers heat into a separate facility loop without mixing the two fluids. That loop carries the heat to the outdoor plant. Pumps circulate the coolant; outdoor equipment rejects the heat. Pumps and fans need electricity too. A chiller uses refrigeration to cool fluid; a dry cooler transfers heat to outdoor air. Liquid-to-air CDUs also exist. This diagram follows the GPU’s liquid cooling path; other equipment may also require air cooling.

## 21. Facility energy and PUE

The GPU needs electricity to compute, and its cooling system needs electricity to move heat. Now count the whole facility for one illustrative hour, including all servers, networking and storage. IT equipment uses 100 kWh. Cooling, power-system losses and other support account for another 20 kWh. The facility therefore uses 120 kWh in total. Power usage effectiveness, or PUE, compares that total with the IT energy: 120 divided by 100 gives 1.20. The numerator already includes IT, and both measurements cover the same interval. This is a new facility-wide example, not the consumption of our single 500 W GPU. PUE describes facility overhead; it does not measure how much computation the IT performed. The illustrative hour does not establish annual PUE.
