// Keep links to the removed roadmap slides useful without adding navigation stops.
export const sceneAliases = { welcome: 'circuit', ready: 'pue' };

export const scenes = [
  {
    id: 'circuit', label: 'Source, circuit and load', title: 'Current needs a complete loop',
    description: 'A source and load form a complete conducting loop. A switch opens or closes one part of that loop.',
    options: [['closed', 'Closed circuit'], ['open', 'Open circuit']], key: 'circuit', group: 'Circuit',
  },
  {
    id: 'voltage-current', label: 'Volts and amperes', title: 'Voltage drives current around a circuit',
    description: 'A voltmeter compares two circuit points. An ammeter measures current through the loop. A 12 volt source drives 2 amperes through a 6 ohm resistor.',
  },
  {
    id: 'resistance', label: 'Resistance and loss', title: 'Resistance limits current and makes heat',
    description: 'For a fixed 6 ohm resistor, raising the source from 12 to 24 volts raises current from 2 to 4 amperes and resistor heating from 24 to 96 watts.',
    options: [['12', '12 V'], ['24', '24 V']], key: 'resistanceVoltage', group: 'Source voltage',
  },
  {
    id: 'power', label: 'Watts', title: 'Power is energy transferred per second',
    description: 'In a steady DC example, 12 volts times 2 amperes transfers 24 watts, or 24 joules each second, into the load.',
  },
  {
    id: 'energy', label: 'Watt-hours and scale', title: 'Watt-hours add up while a load runs',
    description: 'A constant 1 kilowatt load uses 1 kilowatt-hour in one hour, or 2 kilowatt-hours in two hours. Kilo, mega and giga are factors of one thousand.',
    options: [['1', '1 hour'], ['2', '2 hours']], key: 'hours', group: 'Time running',
  },
  {
    id: 'ac-dc', label: 'AC, DC and frequency', title: 'AC voltage changes polarity',
    description: 'A flat DC voltage keeps the left terminal positive relative to the right and drives current to the right through a resistor. The AC voltage reverses polarity: the positive peak makes the left terminal positive and current flows right; the negative peak makes the right terminal positive and current flows left. At the zero crossing, the terminals have equal voltage and this resistor carries no current.',
    options: [['90', 'Positive peak'], ['180', 'Zero crossing'], ['270', 'Negative peak']], key: 'angle', group: 'AC moment',
  },
  {
    id: 'ac-shapes', label: 'AC waveform shapes', title: 'AC does not have to be a sine wave',
    description: 'Sine, square, sawtooth and triangle voltage waveforms each alternate above and below zero. Utility AC is normally approximately sinusoidal; the other shapes illustrate bipolar AC signals.',
  },
  {
    id: 'voltage-variation', label: 'Voltage variation', title: 'AC and DC supplies can vary in voltage',
    description: 'Two illustrative supplies have nominal levels of 12 volts DC and 12 volts AC peak. Select a level ten percent lower, nominal, or ten percent higher. The DC level changes while staying positive; the AC peak height changes while polarity keeps alternating. Dashed traces mark the nominal levels. Actual supply voltage depends on the source, load and wiring. These example levels are not equipment operating limits.',
    options: [['0.9', '10% lower'], ['1', 'Nominal'], ['1.1', '10% higher']], key: 'supplyLevel', group: 'Supply voltage',
  },
  {
    id: 'three-phase', label: 'Three-phase AC', title: 'Data centers mostly distribute AC in three phases',
    description: 'Three sinusoidal phase voltages are staggered by one-third of a cycle. Three-phase AC is the predominant form of AC power distribution in data centers. RMS describes effective voltage magnitude.',
  },
  {
    id: 'three-phase-power', label: 'Three-phase power', title: 'The three phases add up to steady power',
    description: 'For a balanced sinusoidal supply feeding equal resistive loads, each phase delivers an average of 10 kilowatts and its instantaneous power ranges from zero to 20 kilowatts. The three instantaneous powers add to 30 kilowatts at every moment. The colored traces are each phase’s power, voltage times current; the straight line is their total power, not voltage. Selecting different moments shows the three contributions changing while their sum stays 30 kilowatts.',
    options: [['0', '0°'], ['30', '30°'], ['60', '60°']], key: 'phasePowerAngle', group: 'Moment in cycle',
  },
  {
    id: 'power-factor', label: 'Power factor', title: 'Low power factor means more current for the same power',
    description: 'Compare sinusoidal voltage and current over the same cycle. At power factor one they line up. At power factor 0.8 the current lags the voltage and its amplitude is 25 percent larger. Both examples deliver the same average power of 8 kilowatts at the same RMS supply voltage.',
  },
  {
    id: 'conversion', label: 'Conversion equipment', title: 'Different converters do different jobs',
    description: 'A transformer changes AC voltage, a rectifier converts AC to DC, and an inverter converts DC to AC. A power supply can combine several conversion stages.',
  },
  {
    id: 'backup', label: 'UPS, battery and generator', title: 'A UPS keeps the load powered through an interruption',
    description: 'In one online UPS example, normal AC passes through rectifier and inverter stages. A battery supports the DC link while an upstream generator starts.',
  },
  {
    id: 'ups-types', label: 'Offline and online UPS', title: 'Two ways a UPS handles a power cut',
    description: 'A common supply interruption changes both UPS diagrams. Offline or standby UPS switches from the utility path to its battery-powered inverter. Online double-conversion UPS keeps its inverter supplying the load as the battery supports the DC link.',
    options: [['normal', 'Normal supply'], ['interrupted', 'Supply interrupted']], key: 'upsSupply', group: 'Input supply',
  },
  {
    id: 'capacity', label: 'Load, rating and redundancy', title: 'A 100 kW load needs two 50 kW modules',
    description: 'An illustrative 100 kilowatt load needs two qualified 50 kilowatt modules. N means the required two; N plus one provides a third module.',
  },
  {
    id: 'hardware', label: 'Rack, server, CPU and GPU', title: 'A rack holds computers and their connections',
    description: 'Inside a rack, a compute server contains a CPU, system RAM and a GPU with its own memory. This is the server that will load and run a saved AI model.',
  },
  {
    id: 'memory-storage', label: 'Memory and storage', title: 'The GPU needs the model in its memory',
    description: 'A storage server keeps the saved model. Its data crosses the data-center network to the compute server, enters system RAM, and is copied into GPU memory for the GPU cores to use. The compute server and GPU are the same objects shown inside the rack.',
  },
  {
    id: 'network', label: 'Bandwidth and latency', title: 'The network brings model data to the server',
    description: 'An 8 MB chunk of model data travels from a storage server to a compute server within the data center. Compare ideal payload rates of 10 and 100 Gb/s with the first-bit path latency fixed at 10 microseconds. Receiving the whole chunk takes 6.41 or 0.65 milliseconds respectively.',
    options: [['10000', '10 Gb/s'], ['100000', '100 Gb/s']], key: 'bandwidth', group: 'Network payload rate',
  },
  {
    id: 'heat-temperature', label: 'Heat and temperature', title: 'The running GPU produces heat',
    description: 'The GPU in our compute server now runs the loaded model. In this illustrative steady state, it receives 500 watts of electrical power and transfers 500 watts of heat to a cold plate. The GPU is at 70 degrees Celsius, the cold plate at 45, and coolant warms from 30 to 35.',
  },
  {
    id: 'cooling', label: 'Cold plate, coolant and CDU', title: 'Coolant carries chip heat away',
    description: 'Follow heat from the same GPU and cold plate through the equipment coolant loop to a CDU heat exchanger. Heat crosses into a separate facility loop and reaches the outdoor plant. Pumps circulate the coolant; the two fluids stay separate.',
  },
  {
    id: 'pue', label: 'Facility energy and PUE', title: 'Cooling and power equipment use electricity too',
    description: 'Zoom out from our server to the whole facility. During the same illustrative hour, all IT equipment uses 100 kilowatt-hours and supporting equipment and losses account for another 20. Support includes cooling pumps and fans and power-system losses. PUE equals total facility energy of 120 divided by IT energy of 100, or 1.20.',
  },
];
