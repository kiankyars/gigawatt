// D00 is optional first exposure. These seconds are a rehearsal plan, not measured runtime.
export const sources = {
  circuits: { title: 'OpenStax · Resistance and simple circuits', url: 'https://openstax.org/books/college-physics-2e/pages/20-2-ohms-law-resistance-and-simple-circuits', reviewed_on: '2026-09-12', limits: 'Explanatory section through conservation of energy reviewed. Simple source, resistor and closed circuit only.' },
  electricity: { title: 'EIA · Measuring electricity', url: 'https://www.eia.gov/energyexplained/electricity/measuring-electricity.php', reviewed_on: '2026-09-12', limits: 'Watt, decimal prefixes and watt-hour definitions reviewed. Examples here are original.' },
  ac: { title: 'OpenStax · Alternating current versus direct current', url: 'https://openstax.org/books/college-physics-2e/pages/20-5-alternating-current-versus-direct-current', reviewed_on: '2026-09-12', limits: 'AC/DC definitions and RMS relationships for sinusoidal resistive examples reviewed. Real converter currents may have other shapes.' },
  phases: { title: 'P19 · Three-phase source and reading limits', url: '../../research/sources/P19.md', reviewed_on: '2026-09-10', limits: 'Selected basic-concept material in sections 1.2–1.3 of Steven Low’s draft notes. Ideal balanced sinusoidal relationships only.' },
  pf: { title: 'Schneider · Definition of power factor', url: 'https://www.electrical-installation.org/enwiki/Definition_of_Power_Factor', reviewed_on: '2026-09-12', limits: 'Publisher-indexed active/apparent-power definition reviewed. Direct page opening failed. No installation guidance used.' },
  ups: { title: 'Eaton · UPS fundamentals handbook', url: 'https://www.eaton.com/content/dam/eaton/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/eaton-ups-fundamentals-handbook-anz.pdf', reviewed_on: '2026-09-12', limits: 'Introduction, topology material on printed page 28 and rectifier glossary on page 46 reviewed. General functions only, without sizing or product claims.' },
  hardware: { title: 'Intel · CPU versus GPU', url: 'https://www.intel.com/content/www/us/en/products/docs/processors/cpu-vs-gpu.html', reviewed_on: '2026-09-12', limits: 'CPU/GPU definitions and comparison sections reviewed. No performance or superiority claim adopted.' },
  memory: { title: 'Intel · Memory performance in a nutshell', url: 'https://www.intel.com/content/www/us/en/developer/articles/technical/memory-performance-in-a-nutshell.html', reviewed_on: '2026-09-12', limits: 'Persistence, latency and bandwidth explanations reviewed. Historical component numbers excluded.' },
  heat: { title: 'OpenStax · Heat', url: 'https://openstax.org/books/college-physics-2e/pages/14-1-heat', reviewed_on: '2026-09-12', limits: 'Introductory definition of heat as energy transfer due to a temperature difference reviewed.' },
  cdu: { title: 'CoolIT · Coolant distribution units', url: 'https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/', reviewed_on: '2026-09-12', limits: 'Portfolio, selection and loop-separation FAQ reviewed. Liquid-to-liquid example only; liquid-to-air CDUs also exist.' },
  pue: { title: 'The Green Grid · PUE: A comprehensive examination', url: 'https://datacenters.lbl.gov/sites/default/files/WP49-PUE%20A%20Comprehensive%20Examination%20of%20the%20Metric_v6.pdf', reviewed_on: '2026-09-12', limits: 'Printed pages 8–12 on definitions and productivity limitations reviewed. Historical metric guidance, not a standards compliance review.' },
};

// Keep links to the removed roadmap slides useful without adding navigation stops.
export const sceneAliases = { welcome: 'circuit', ready: 'pue' };

export const scenes = [
  {
    id: 'circuit', label: 'Source, circuit and load', title: 'A simple circuit has a source, a load and a return path', seconds: 90,
    description: 'A source and load form a complete conducting loop. A switch opens or closes one part of that loop.',
    options: [['closed', 'Closed circuit'], ['open', 'Open circuit']], key: 'circuit', group: 'Circuit',
    explanation: 'Allow about twenty minutes for this optional primer. You do not need to memorize these terms: we will explain them again when we reach the system that uses them. If they are familiar already, skip straight to D01. The source supplies electrical energy. The load receives it, for example to run electronics or produce heat. In this simple steady circuit, current needs a complete path from the source through the load and back. Opening the switch interrupts that path. Voltage can still exist across the open switch. Charge circulates; the load does not consume charge. The arrows represent conventional current, not electron travel speed.',
    returns: 'D04 explains the electrical path. D06 follows conversion into the rack.', reference: 'd03-voltage-and-distance', sources: ['circuits'],
  },
  {
    id: 'voltage-current', label: 'Volts and amperes', title: 'Voltage is measured across two points; current flows through a path', seconds: 90,
    description: 'A voltmeter compares two circuit points. An ammeter measures current through the loop. A 12 volt source drives 2 amperes through a 6 ohm resistor.',
    explanation: 'Voltage is electric potential difference: energy per unit charge, measured in volts (V). Current is the rate of charge flow, measured in amperes (A), often called amps. In the example, the resistor has 12 V across it and 2 A through it. Both the outward and return wires carry 2 A. Adding those wire readings would count the same loop current twice. Voltage alone does not tell us the current without knowing the load.',
    returns: 'D04 and the 800 V section revisit voltage, current and measurement points.', reference: 'd03-voltage-and-distance', sources: ['circuits'],
  },
  {
    id: 'resistance', label: 'Resistance and loss', title: 'Resistance affects current and produces heat', seconds: 60,
    description: 'For a fixed 6 ohm resistor, raising the source from 12 to 24 volts raises current from 2 to 4 amperes and resistor heating from 24 to 96 watts.',
    options: [['12', '12 V'], ['24', '24 V']], key: 'resistanceVoltage', group: 'Source voltage',
    explanation: 'Resistance, measured in ohms (Ω), relates voltage and current in this simple resistor model: V = I × R. With resistance fixed at 6 Ω, 12 V gives 2 A; 24 V gives 4 A. Resistive heating is I²R, so doubling current produces four times the heat at the same resistance. Wires also have resistance. A regulated server is not a fixed resistor: later comparisons can instead hold delivered power fixed. We will state which condition is held fixed.',
    returns: 'D03 and D06 compare conductor losses under a stated load.', reference: 'd03-voltage-and-distance', sources: ['circuits'],
  },
  {
    id: 'power', label: 'Watts', title: 'Power is the rate of energy transfer', seconds: 75,
    description: 'In a steady DC example, 12 volts times 2 amperes transfers 24 watts, or 24 joules each second, into the load.',
    explanation: 'A watt (W) is one joule of energy transferred each second. For the steady DC load shown, P = V × I: 12 V × 2 A = 24 W. The voltage and current must describe the same receiving boundary. A watt describes how fast energy is being transferred, not how long the device runs. AC circuits need additional measurement conventions, which we will introduce again before using their equations.',
    returns: 'D01 uses power to describe actual loads. D04 develops AC power.', reference: 'd01-power-over-time', sources: ['electricity', 'ac'],
  },
  {
    id: 'energy', label: 'Watt-hours and scale', title: 'Energy accumulates while a load runs', seconds: 75,
    description: 'A constant 1 kilowatt load uses 1 kilowatt-hour in one hour, or 2 kilowatt-hours in two hours. Kilo, mega and giga are factors of one thousand.',
    options: [['1', '1 hour'], ['2', '2 hours']], key: 'hours', group: 'Time running',
    explanation: 'Energy equals power multiplied by time when the power stays constant, or when we use its average over that interval. A 1 kW load running for 2 hours uses 2 kWh. A kilowatt-hour is a unit of energy, not power per hour. The decimal prefixes are k = thousand, M = million and G = billion. Thus 1 MW = 1,000 kW and 1 GW = 1,000 MW. The same prefixes appear on watt-hours. A battery’s kWh rating describes stored energy; its kW limit describes the rate it can supply.',
    returns: 'D01 compares power with energy. D05 applies both to storage.', reference: 'd01-power-over-time', sources: ['electricity'],
  },
  {
    id: 'ac-dc', label: 'AC, DC and frequency', title: 'AC reverses direction; DC keeps one direction', seconds: 90,
    description: 'Two current-versus-time plots show constant DC and sinusoidal AC. Moving a phase control reveals positive, zero and negative AC current.',
    options: [['90', 'First half-cycle'], ['180', 'Zero crossing'], ['270', 'Second half-cycle']], key: 'angle', group: 'AC moment',
    explanation: 'Direct current (DC) keeps one direction, although its magnitude can vary. Our simple DC trace is constant. Alternating current (AC) changes direction periodically. The positive and negative signs refer to a chosen direction, not useful versus wasted electricity. Frequency counts complete cycles per second in hertz (Hz). A 60 Hz supply completes 60 cycles per second. In a simple AC resistor, voltage and current reverse together, and the resistor still receives energy in both halves of the cycle.',
    returns: 'D04 and the 800 V section explain waveforms and conversion in context.', reference: 'd03-voltage-and-distance', sources: ['ac'],
  },
  {
    id: 'three-phase', label: 'Three phase, RMS and power factor', title: 'Three-phase AC has three staggered waveforms', seconds: 60,
    description: 'Three equal sine waves are shifted by one-third of a cycle. RMS and power factor are introduced as labels used in later AC calculations.',
    explanation: 'In this balanced sinusoidal example, the three phases have equal amplitudes and are separated by 120 degrees, or one-third of a cycle. A quoted AC voltage often uses RMS, a measure of effective magnitude rather than peak or signed average. Specify which two points the voltage is between, such as line-to-line. Power factor (PF) is real power divided by apparent power: kW divided by kVA. It is not converter efficiency. This slide is first exposure to these labels; the later electrical section will build the relationships before calculating with them.',
    returns: 'D04 introduces RMS, line-to-line voltage, kVA and PF before using them.', reference: 'd04-current-and-rating', sources: ['ac', 'phases', 'pf'],
  },
  {
    id: 'conversion', label: 'Conversion equipment', title: 'Conversion equipment changes the electrical supply', seconds: 75,
    description: 'A transformer changes AC voltage, a rectifier converts AC to DC, and an inverter converts DC to AC. A power supply can combine several conversion stages.',
    explanation: 'A transformer changes an AC voltage level through magnetic coupling. A rectifier converts AC to DC; an inverter converts DC to AC. A power supply unit (PSU) prepares the electrical output needed by equipment and can contain several stages. A DC–DC converter changes a DC voltage level. A power shelf groups supplies and distributes their output in a rack. These names identify functions, not one mandatory architecture. Real equipment has losses and operating limits.',
    returns: 'D04 and D06 explain where each stage sits and why it is needed.', reference: 'd04-conversion-placement', sources: ['ups'],
  },
  {
    id: 'backup', label: 'UPS, battery and generator', title: 'A UPS and its stored energy bridge an interruption', seconds: 75,
    description: 'In one online UPS example, normal AC passes through rectifier and inverter stages. A battery supports the DC link while an upstream generator starts.',
    explanation: 'UPS means uninterruptible power supply: a system that supports its protected load when the normal source is interrupted. A battery stores energy and is one possible part of that system. In this online UPS example, its rectifier feeds a DC link and its inverter supplies the load. The battery supports the link during an upstream interruption. A generator can take over the upstream supply after it starts and qualifies. Runtime is finite. Switchgear switches and protects circuits; a breaker can interrupt a circuit. A busbar is a conductor used for distribution, and a rack PDU (power distribution unit) distributes power to equipment. We will locate and explain each item again.',
    returns: 'D04 introduces distribution and protection. D05 teaches UPS operating states.', reference: 'd05-paths-and-transitions', sources: ['ups'],
  },
  {
    id: 'capacity', label: 'Load, rating and redundancy', title: 'A load is demand; a rating states capability under conditions', seconds: 60,
    description: 'An illustrative 100 kilowatt load needs two qualified 50 kilowatt modules. N means the required two; N plus one provides a third module.',
    explanation: 'Load is actual demand. A rating states a component’s capability under specified conditions. Capacity needs a boundary and operating conditions too. In this illustrative system, a 100 kW load requires two 50 kW modules, so N = 2. N+1 adds one spare module. If a module fails, two remain in this simplified capacity screen. Shared paths, controls and cooling can still prevent service. Redundancy is additional provision; availability describes service over a defined period. N+1 alone does not establish availability or a Tier classification.',
    returns: 'D01 separates rating and load. D05 tests surviving paths and capacity.', reference: 'd05-paths-and-transitions', sources: ['ups'],
  },
  {
    id: 'hardware', label: 'Rack, server, CPU and GPU', title: 'A rack holds systems that contain processors and memory', seconds: 60,
    description: 'A rack contains a server or compute tray; that system contains CPU, GPU and working memory. Connected machines can form a cluster.',
    explanation: 'A rack is a frame for mounting equipment. A server or compute tray combines processors, working memory and connections into a system. CPU means central processing unit; GPU means graphics processing unit. Both compute, with different architectures and workload strengths. GPUs also perform the parallel numerical work used in many AI systems. A cluster is a coordinated collection of connected machines. IT means information technology and includes computing, networking and storage equipment. These generic boxes do not specify a particular vendor configuration.',
    returns: 'D01 tours a rack. D07 develops compute and memory.', reference: 'd07-rack-as-system', sources: ['hardware'],
  },
  {
    id: 'memory-storage', label: 'Memory and storage', title: 'Working memory holds active state; storage keeps saved data', seconds: 60,
    description: 'Saved data moves from storage to working memory for processing. A checkpoint writes saved job state back to storage for later recovery.',
    explanation: 'Working memory holds the data and state a processor is using. RAM means random-access memory; HBM means high-bandwidth memory, a memory technology used near many accelerators. Storage retains datasets, files and checkpoints. A checkpoint saves enough job state to support recovery according to the application’s design. GB describes a quantity of bytes, while GB/s describes a transfer rate. We will state decimal GB versus binary GiB when calculating capacity. More aggregate memory does not automatically make all of it accessible as one pool.',
    returns: 'D02 builds a memory budget. D07 and D09 explain access and checkpoints.', reference: 'd02-workload-brief', sources: ['memory'],
  },
  {
    id: 'network', label: 'Bandwidth and latency', title: 'Bandwidth describes a rate; latency describes a delay', seconds: 60,
    description: 'A network switch connects two machines. Bandwidth is labelled in gigabits per second, while response latency spans a timeline measured in milliseconds.',
    explanation: 'A network moves information between machines. A switch forwards traffic between connected ports. Bandwidth describes a transfer-rate capability; measured throughput is the rate actually achieved under conditions. Latency is elapsed time for a defined event, such as sending data or receiving a response. A network path can have high bandwidth and still have noticeable latency. Lowercase b means bits; uppercase B means bytes, with eight bits per byte. Application throughput may instead count accepted requests per second. D02 will show why throughput and response time must both meet the workload’s needs.',
    returns: 'D02 compares request throughput with latency. D08 develops network paths.', reference: 'd08-topology-budget', sources: ['memory'],
  },
  {
    id: 'heat-temperature', label: 'Heat and temperature', title: 'Temperature and heat-transfer rate describe different quantities', seconds: 60,
    description: 'Heat transfers from a warmer chip to cooler coolant. Temperature labels use degrees Celsius, while the heat-transfer-rate arrow uses kilowatts.',
    explanation: 'Temperature describes a thermal state, measured here in degrees Celsius (°C). Heat is energy transferred because of a temperature difference. Heat-transfer rate is measured in watts or kilowatts. Most electrical energy entering IT equipment ultimately becomes heat that the facility must reject. A coolant can carry more heat at the same temperature rise if enough additional flow is provided; temperature alone does not tell us the heat load. This is a vocabulary preview, not a cooling design calculation.',
    returns: 'D10 introduces the heat balance and coolant-flow experiment.', reference: 'd10-local-thermal-paths', sources: ['heat'],
  },
  {
    id: 'cooling', label: 'Cold plate, coolant and CDU', title: 'A cold plate transfers chip heat into moving coolant', seconds: 60,
    description: 'An equipment coolant loop passes through a cold plate and a CDU heat exchanger. A separate facility loop receives heat and carries it toward the outdoor plant.',
    explanation: 'A cold plate is a heat exchanger attached to a hot component. Coolant flows through it and carries heat away. CDU means coolant distribution unit. In this liquid-to-liquid example, its heat exchanger transfers heat between an equipment loop and a separate facility loop without mixing the fluids. Pumps circulate coolant, and the outdoor plant rejects the heat. Liquid-to-air CDUs also exist. A chiller uses refrigeration to cool fluid; a dry cooler transfers heat to outdoor air. The later cooling sequence explains when each mechanism is useful.',
    returns: 'D10 and D11 trace capture, coolant loops and heat rejection.', reference: 'd10-cdu-interfaces', sources: ['cdu', 'heat'],
  },
  {
    id: 'pue', label: 'Efficiency and PUE', title: 'PUE compares facility energy with IT energy', seconds: 60,
    description: 'An illustrative one-hour facility account contains 100 kilowatt-hours of IT energy and 20 kilowatt-hours of support energy. PUE equals 120 divided by 100, or 1.20.',
    explanation: 'Power usage effectiveness (PUE) is total facility energy divided by IT equipment energy over the same interval. The numerator already includes IT. In the example, IT uses 100 kWh and support uses 20 kWh, so PUE = 120/100 = 1.20. PUE is a ratio, not a percentage or a measure of useful computation. Conversion efficiency instead compares useful output energy with input energy for a specified device or process. We will always state what is counted. This one-hour example is not an annual PUE measurement.',
    returns: 'D01 revisits PUE. D02 measures useful work separately.', reference: 'd01-metrics-and-evidence', sources: ['pue'],
  },
];
