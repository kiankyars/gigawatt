// Primer scene timings are a rehearsal plan, not measured runtime.
// Keep links to the removed roadmap slides useful without adding navigation stops.
export const sceneAliases = { welcome: 'circuit', ready: 'pue' };

export const scenes = [
  {
    id: 'circuit', label: 'Source, circuit and load', title: 'Current needs a complete loop', seconds: 75,
    description: 'A source and load form a complete conducting loop. A switch opens or closes one part of that loop.',
    options: [['closed', 'Closed circuit'], ['open', 'Open circuit']], key: 'circuit', group: 'Circuit',
    explanation: 'The source supplies electrical energy. The load receives it, for example to run electronics or produce heat. In this simple steady circuit, current needs a complete path from the source through the load and back. Opening the switch interrupts that path. Voltage can still exist across the open switch. Charge circulates; the load does not consume charge. The arrows represent conventional current, not electron travel speed.',
  },
  {
    id: 'voltage-current', label: 'Volts and amperes', title: 'Voltage drives current around a circuit', seconds: 75,
    description: 'A voltmeter compares two circuit points. An ammeter measures current through the loop. A 12 volt source drives 2 amperes through a 6 ohm resistor.',
    explanation: 'Voltage is electric potential difference: energy per unit charge, measured in volts (V). Current is the rate of charge flow, measured in amperes (A), often called amps. In the example, the resistor has 12 V across it and 2 A through it. Both the outward and return wires carry 2 A. Adding those wire readings would count the same loop current twice. Voltage alone does not tell us the current without knowing the load.',
  },
  {
    id: 'resistance', label: 'Resistance and loss', title: 'Resistance limits current and makes heat', seconds: 60,
    description: 'For a fixed 6 ohm resistor, raising the source from 12 to 24 volts raises current from 2 to 4 amperes and resistor heating from 24 to 96 watts.',
    options: [['12', '12 V'], ['24', '24 V']], key: 'resistanceVoltage', group: 'Source voltage',
    explanation: 'Resistance, measured in ohms (Ω), relates voltage and current in this simple resistor model: V = I × R. With resistance fixed at 6 Ω, 12 V gives 2 A; 24 V gives 4 A. Resistive heating is I²R, so doubling current produces four times the heat at the same resistance. Wires also have resistance. A regulated server is not a fixed resistor; its current can change to maintain delivered power. This example holds resistance fixed.',
  },
  {
    id: 'power', label: 'Watts', title: 'Watts tell us how fast energy moves', seconds: 50,
    description: 'In a steady DC example, 12 volts times 2 amperes transfers 24 watts, or 24 joules each second, into the load.',
    explanation: 'A watt (W) is one joule of energy transferred each second. For the steady DC load shown, P = V × I: 12 V × 2 A = 24 W. The voltage and current must describe the same receiving boundary. A watt describes how fast energy is being transferred, not how long the device runs.',
  },
  {
    id: 'energy', label: 'Watt-hours and scale', title: 'Watt-hours add up while a load runs', seconds: 60,
    description: 'A constant 1 kilowatt load uses 1 kilowatt-hour in one hour, or 2 kilowatt-hours in two hours. Kilo, mega and giga are factors of one thousand.',
    options: [['1', '1 hour'], ['2', '2 hours']], key: 'hours', group: 'Time running',
    explanation: 'Energy equals power multiplied by time when the power stays constant, or when we use its average over that interval. A 1 kW load running for 2 hours uses 2 kWh. A kilowatt-hour is a unit of energy, not power per hour. The decimal prefixes are k = thousand, M = million and G = billion. Thus 1 MW = 1,000 kW and 1 GW = 1,000 MW. The same prefixes appear on watt-hours. A battery’s kWh rating describes stored energy; its kW limit describes the rate it can supply.',
  },
  {
    id: 'ac-dc', label: 'AC, DC and frequency', title: 'AC voltage changes polarity', seconds: 75,
    description: 'The voltage between points A and B changes polarity in AC. For a resistor, current reverses too. A rippled DC voltage varies but stays on one side of zero.',
    options: [['90', 'First half-cycle'], ['180', 'Zero crossing'], ['270', 'Second half-cycle']], key: 'angle', group: 'AC moment',
    explanation: 'Voltage polarity tells us which of two points is at the higher electric potential. In this AC example, point A alternates between positive and negative relative to B. Current direction is a separate quantity: through a resistor, current reverses when the voltage polarity reverses. Other loads can shift or reshape the current. DC voltage keeps its polarity and DC current keeps its direction, although their magnitudes can vary. Ripple that never reverses the total voltage polarity does not make that total waveform bipolar AC. Frequency counts full cycles per second in hertz (Hz); 60 Hz means 60 cycles per second.',
  },
  {
    id: 'ac-shapes', label: 'AC waveform shapes', title: 'AC does not have to be a sine wave', seconds: 45,
    description: 'Sine, square, sawtooth and triangle voltage waveforms each alternate above and below zero. Utility AC is normally approximately sinusoidal; the other shapes illustrate bipolar AC signals.',
    explanation: 'AC describes alternation, not one mandatory waveform shape. Each voltage waveform shown changes polarity between the same two measurement points. A sine wave changes smoothly, a square wave switches between levels, a sawtooth ramps and resets, and a triangle or zigzag ramps both ways. Utility supplies are normally approximately sinusoidal. These other shapes are examples from signals and power electronics, not a claim about normal utility supply. A DC waveform can have ripple while keeping the same polarity.',
  },
  {
    id: 'three-phase', label: 'Three-phase AC', title: 'Data centers mostly distribute AC in three phases', seconds: 60,
    description: 'Three sinusoidal phase voltages are staggered by one-third of a cycle. Three-phase AC is the predominant form of AC power distribution in data centers. RMS describes effective voltage magnitude.',
    explanation: 'Three-phase AC is the predominant form of AC power distribution in data centers, although individual loads can use single-phase AC or DC. In this balanced example, the three phase voltages have equal amplitudes and are staggered by 120 degrees, or one-third of a cycle. Their peaks occur at different times. A quoted AC voltage usually uses RMS: the effective magnitude that produces the same average heating in a resistor as an equal DC voltage. The measurement points still matter: line-to-line voltage is measured between two phase conductors.',
  },
  {
    id: 'power-factor', label: 'Power factor', title: 'Low power factor means more current for the same power', seconds: 75,
    description: 'Two loads each receive 8 kilowatts of real power. At power factor one the apparent power is 8 kVA; at power factor 0.8 it is 10 kVA. At the same voltage and phase arrangement, the second load needs 25 percent more RMS current.',
    explanation: 'Why might a supply be rated in both kW and kVA? Real power, in kW, measures average energy transfer. Apparent power, in kVA, reflects voltage and RMS current together. Power factor is their ratio: kW divided by kVA. The same 8 kW at PF 1 needs 8 kVA; at PF 0.8 it needs 10 kVA. With voltage and phase arrangement fixed, that means 25% more RMS current for the same real power, using more of the supply and wiring capacity. The difference is not 2 kW of wasted energy: power factor is not conversion efficiency. This concept applies to both single-phase and three-phase AC. Phase shift and distorted current waveforms can both reduce power factor.',
  },
  {
    id: 'conversion', label: 'Conversion equipment', title: 'Different converters do different jobs', seconds: 60,
    description: 'A transformer changes AC voltage, a rectifier converts AC to DC, and an inverter converts DC to AC. A power supply can combine several conversion stages.',
    explanation: 'A transformer changes an AC voltage level through magnetic coupling. A rectifier converts AC to DC; an inverter converts DC to AC. A power supply unit (PSU) prepares the electrical output needed by equipment and can contain several stages. A DC–DC converter changes a DC voltage level. A power shelf groups supplies and distributes their output in a rack. These names identify functions, not one mandatory architecture. Real equipment has losses and operating limits.',
  },
  {
    id: 'backup', label: 'UPS, battery and generator', title: 'A UPS keeps the load powered through an interruption', seconds: 60,
    description: 'In one online UPS example, normal AC passes through rectifier and inverter stages. A battery supports the DC link while an upstream generator starts.',
    explanation: 'UPS means uninterruptible power supply: a system that supports its protected load when the normal source is interrupted. A battery stores energy and is one possible part of that system. In this online UPS example, its rectifier feeds a DC link and its inverter supplies the load. The battery supports the link during an upstream interruption. A generator can take over the upstream supply after it starts and qualifies. Runtime is finite. Switchgear switches and protects circuits; a breaker can interrupt a circuit. A busbar is a conductor used for distribution, and a rack PDU (power distribution unit) distributes power to equipment.',
  },
  {
    id: 'ups-types', label: 'Offline and online UPS', title: 'Two ways a UPS handles a power cut', seconds: 90,
    description: 'A common supply interruption changes both UPS diagrams. Offline or standby UPS switches from the utility path to its battery-powered inverter. Online double-conversion UPS keeps its inverter supplying the load as the battery supports the DC link.',
    options: [['normal', 'Normal supply'], ['interrupted', 'Supply interrupted']], key: 'upsSupply', group: 'Input supply',
    explanation: 'An offline or standby UPS normally passes utility AC to the load. When the supply fails, it switches to an inverter powered by the battery, with a brief transfer interval. This topology is common for home computers and desktop equipment. An online double-conversion UPS normally sends power through a rectifier, a DC link and an inverter. Its inverter keeps feeding the load when the battery takes over the DC link, without the normal-to-battery transfer break of a standby UPS. Online systems are often chosen for critical data-center loads and sensitive medical systems. The application determines the suitable topology; medical equipment does not all require the same UPS. These are simplified normal and battery paths: charging details, bypass operation and faults are omitted, and stored runtime is finite.',
  },
  {
    id: 'capacity', label: 'Load, rating and redundancy', title: 'A 100 kW load needs two 50 kW modules', seconds: 60,
    description: 'An illustrative 100 kilowatt load needs two qualified 50 kilowatt modules. N means the required two; N plus one provides a third module.',
    explanation: 'Load is actual demand. A rating states a component’s capability under specified conditions. Capacity needs a boundary and operating conditions too. In this illustrative system, a 100 kW load requires two 50 kW modules, so N = 2. N+1 adds one spare module. If a module fails, two remain in this simplified capacity screen. Shared paths, controls and cooling can still prevent service. Redundancy is additional provision; availability describes service over a defined period. N+1 alone does not establish availability or a Tier classification.',
  },
  {
    id: 'hardware', label: 'Rack, server, CPU and GPU', title: 'A rack holds computers and their connections', seconds: 60,
    description: 'A rack contains a server or compute tray; that system contains CPU, GPU and working memory. Connected machines can form a cluster.',
    explanation: 'A rack is a frame for mounting equipment. A server or compute tray combines processors, working memory and connections into a system. CPU means central processing unit; GPU means graphics processing unit. Both compute, with different architectures and workload strengths. GPUs also perform the parallel numerical work used in many AI systems. A cluster is a coordinated collection of connected machines. IT means information technology and includes computing, networking and storage equipment. These generic boxes do not specify a particular vendor configuration.',
  },
  {
    id: 'memory-storage', label: 'Memory and storage', title: 'A saved model must move into working memory to run', seconds: 60,
    description: 'A saved model is read from storage into system RAM, then copied into GPU working memory in this common loading example. GPU cores use the model held in that memory.',
    explanation: 'Imagine starting a model that was saved as a file. Storage keeps that file when the computer is off. In the loading path shown, the system reads the file into RAM, then copies the needed model data into the GPU’s working memory. GPU cores use that data while running the model. RAM means random-access memory; HBM means high-bandwidth memory, used by many accelerators. This is one common loading path; direct storage-to-GPU paths also exist. Capacity in GB tells us how much fits, while GB/s tells us how fast data moves. The GPU must have access to the memory containing the data it needs; adding memory elsewhere does not automatically make it one shared pool.',
  },
  {
    id: 'network', label: 'Bandwidth and latency', title: 'A faster link sends the same file sooner', seconds: 60,
    description: 'The same 8 MB payload crosses either a 100 Mb/s or 1,000 Mb/s link. First-bit travel time remains 20 milliseconds; the faster link finishes sending the payload sooner. This ideal example excludes queueing, overhead and losses.',
    options: [['100', '100 Mb/s'], ['1000', '1,000 Mb/s']], key: 'bandwidth', group: 'Link payload rate',
    explanation: 'Bandwidth asks how much data a link can carry per second. Latency asks how long a defined event takes. Here the payload is 8 MB, or 64 megabits, and the path takes 20 ms for the first bit to travel. At an ideal payload rate of 100 Mb/s, sending all the bits takes 640 ms; the last bit arrives after 660 ms. At 1,000 Mb/s, sending takes 64 ms and the last bit arrives after 84 ms. More bandwidth helps the large payload finish sooner, while the first-bit travel time stays 20 ms. Real paths also add queueing, protocol overhead and possible retransmissions. Lowercase b means bits; uppercase B means bytes, with eight bits per byte.',
  },
  {
    id: 'heat-temperature', label: 'Heat and temperature', title: 'How hot is the chip? How fast is heat leaving?', seconds: 60,
    description: 'In an illustrative steady thermal path, a chip is at 70 degrees Celsius, its cold plate at 45 degrees Celsius, and coolant warms from 30 to 35 degrees Celsius. The heat-transfer rate from chip to cold plate is 500 watts.',
    explanation: 'Temperature answers how hot a particular place is; here it is measured in degrees Celsius. Heat is energy crossing from a warmer place to a cooler one. Heat-transfer rate answers how much energy crosses each second. In this illustrative steady example, the chip is at 70 °C and the cold plate is at 45 °C, with 500 W of heat crossing between them. That is 500 joules each second, not a temperature. Coolant enters at 30 °C and leaves at 35 °C as it carries the heat away. These temperatures and heat rate describe different dimensions of the same path. Their values depend on cooling conditions and thermal resistance; they are not product ratings.',
  },
  {
    id: 'cooling', label: 'Cold plate, coolant and CDU', title: 'Coolant carries chip heat away', seconds: 60,
    description: 'An equipment coolant loop passes through a cold plate and a CDU heat exchanger. A separate facility loop receives heat and carries it toward the outdoor plant.',
    explanation: 'A cold plate is a heat exchanger attached to a hot component. Coolant flows through it and carries heat away. CDU means coolant distribution unit. In this liquid-to-liquid example, its heat exchanger transfers heat between an equipment loop and a separate facility loop without mixing the fluids. Pumps circulate coolant, and the outdoor plant rejects the heat. Liquid-to-air CDUs also exist. A chiller uses refrigeration to cool fluid; a dry cooler transfers heat to outdoor air.',
  },
  {
    id: 'pue', label: 'Efficiency and PUE', title: 'PUE counts the energy beyond the IT equipment', seconds: 60,
    description: 'An illustrative one-hour facility account contains 100 kilowatt-hours of IT energy and 20 kilowatt-hours of support energy. PUE equals 120 divided by 100, or 1.20.',
    explanation: 'Power usage effectiveness (PUE) is total facility energy divided by IT equipment energy over the same interval. The numerator already includes IT. In the example, IT uses 100 kWh and support uses 20 kWh, so PUE = 120/100 = 1.20. PUE is a ratio, not a percentage or a measure of useful computation. Conversion efficiency instead compares useful output energy with input energy for a specified device or process. This one-hour example is not an annual PUE measurement.',
  },
];
