// The single source for chapter and equipment copy. app.js and world.js derive
// names, labels, colours, counts and server parts from these tables.

const doe = 'https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf';
const ibm = 'https://www.ibm.com/think/topics/data-centers';
const ibmCpu = 'https://www.ibm.com/think/topics/central-processing-unit';
const ibmGpu = 'https://www.ibm.com/think/topics/gpu';
const rack19 = 'https://en.wikipedia.org/wiki/19-inch_rack';
const sprinklers = 'https://en.wikipedia.org/wiki/Fire_sprinkler_system';
const cisco =
  'https://www.cisco.com/c/en/us/products/collateral/switches/nexus-9000-series-switches/white-paper-c11-743245.html';

// `title` lines are joined with line breaks. `items` are listed in the chapter's equipment
// guide; `labels` are the equipment labelled in the 3D view at that stop. `insight` is the
// heading shown above `fact`. Optional: `eyebrow` replaces the numbered label, `enter` adds a
// button to the next chapter, and `links` ([{ label, href }], headed by `linksTitle`) point to
// further material.
export const chapters = [
  {
    id: 'overview',
    name: 'Overview',
    color: '#f7ce46',
    title: ['The cloud is a place.'],
    lead: 'A journey through the machines, energy, and people behind every click.',
    enter: 'Explore the datacenter',
  },
  {
    id: 'power',
    name: 'Power',
    color: '#f7ce46',
    title: ['Nothing happens', 'without power.'],
    lead: 'Before a single bit moves, electricity travels through transformers, switchgear, backup systems, and distribution equipment.',
    guideTitle: 'Power equipment',
    guideLead:
      'Follow the chain from the utility feed to the server. Each stage changes, protects, or backs up the supply.',
    items: ['utility', 'transformer', 'switchgear', 'ats', 'ups', 'generator', 'pdu', 'rack-pdu', 'psu'],
    labels: ['transformer', 'switchgear', 'ups', 'generator', 'pdu', 'ats', 'utility'],
    insight: 'Two time scales',
    fact: 'A UPS can carry the load for seconds to minutes. A standby generator takes several seconds to start and pick up the load, then can run for hours on stored fuel.',
    flow: { id: 'power', noun: 'power' },
  },
  {
    id: 'compute',
    name: 'Compute',
    color: '#75bd64',
    title: ['A world of work.', 'Inside a box.'],
    lead: 'Rows of racks hold the servers. Inside each server: processors, memory, storage, and a connection to the network.',
    guideTitle: 'Compute equipment',
    guideLead: 'Racks are the frames; servers do the work. Open one to see how its parts fit together.',
    items: ['rack', 'server', 'cpu', 'gpu', 'memory', 'storage'],
    labels: ['rack', 'server', 'leaf', 'rack-pdu', 'cold-aisle', 'hot-aisle'],
    insight: 'Busy is efficient',
    fact: 'In enterprise settings, servers average only about 20–40% utilization. Running fewer, busier servers is one of the most effective ways to save energy (DOE, 2024).',
  },
  {
    id: 'cooling',
    name: 'Cooling',
    color: '#41b9ef',
    title: ['The work stays.', 'The heat leaves.'],
    lead: 'Computing turns electricity into heat. Air and liquid carry it out of the servers and back to the environment.',
    guideTitle: 'Cooling equipment',
    guideLead:
      'Almost all the electricity IT equipment uses ends up as heat. Room air and two separate liquid loops carry it outside.',
    items: ['cold-aisle', 'hot-aisle', 'air-handler', 'fans', 'cold-plate', 'cdu', 'facility-loop', 'heat-rejection'],
    labels: ['air-handler', 'cdu', 'facility-loop', 'heat-rejection', 'hot-aisle', 'cold-aisle'],
    insight: 'Cooling has a cost',
    fact: 'ASHRAE recommends server inlet air of about 18–27 °C (64–81 °F). Cooling is also the largest overhead: PUE divides a facility’s total energy by the energy its IT equipment uses. A typical site scores about 1.6; the most efficient get below 1.1 (DOE, 2024).',
    flow: { id: 'cooling', noun: 'heat' },
  },
  {
    id: 'network',
    name: 'Network',
    color: '#ee6252',
    title: ['A conversation', 'between machines.'],
    lead: 'Fiber, switches, and network interfaces connect the servers to each other and the facility to the outside world.',
    guideTitle: 'Network equipment',
    guideLead:
      'Data enters on fiber, crosses a fabric of switches, and reaches each server through its network interface.',
    items: ['fiber', 'switch', 'cable-tray', 'leaf', 'nic'],
    labels: ['fiber', 'switch', 'cable-tray', 'leaf'],
    insight: 'Two kinds of journeys',
    fact: 'North–south traffic travels between the facility and its users. East–west traffic stays inside, moving between servers and storage. Distance still matters: light in fiber covers about 200 km per millisecond, so a user 1,000 km away waits at least 10 ms for a round trip.',
    flow: { id: 'network', noun: 'data' },
  },
  {
    id: 'operations',
    name: 'People',
    color: '#b59cde',
    title: ['It doesn’t run', 'itself.'],
    lead: 'People monitor conditions, maintain the machines, control access, and respond when something goes wrong.',
    guideTitle: 'People and safeguards',
    guideLead:
      'Operators keep watch from a control room, staff the entrances, and plan maintenance so the facility never has to stop.',
    items: ['monitoring', 'technician', 'security', 'fire'],
    labels: ['monitoring', 'technician', 'security', 'fire'],
    insight: 'Resilience is a system',
    fact: 'N is what the load needs. N+1 adds one spare unit; 2N builds two complete, independent paths, often called A and B. Spares only help if no single failure, or planned maintenance, can take out both.',
  },
];

// Captions for "Follow the …"; colours match the paths drawn in world.js.
export const flowCaptions = {
  power:
    'PALE YELLOW: UTILITY → TRANSFORMER → SWITCHGEAR → UPS → BUSWAY → RACK · DIM LINE: STANDBY GENERATOR VIA TRANSFER SWITCH',
  cooling: 'ORANGE: HEAT, CARRIED BY WARM RETURN · BLUE: COOLED SUPPLY · THE TWO LIQUID LOOPS SWAP HEAT INSIDE THE CDU',
  network: 'RED: USER TRAFFIC IN AND OUT (NORTH–SOUTH) · PINK: SERVER TO SERVER THROUGH THE SPINE (EAST–WEST)',
};

// Spoken versions of the captions, without arrows or colour shorthand.
export const flowDescriptions = {
  power:
    'Showing the power path: utility, transformer, switchgear, UPS, busway, rack. A dim line marks the standby generator.',
  cooling:
    'Showing the heat path: warm return lines carry heat out, cooled supply lines come back, and the two liquid loops swap heat in the CDU.',
  network:
    'Showing data paths: user traffic in and out of the building, and server-to-server traffic through the spine.',
};

// `label` is the short in-world label; `name` is the full title used in the drawer.
export const equipment = {
  utility: {
    chapter: 'power',
    name: 'Utility feed',
    label: 'UTILITY FEED',
    description: 'High-voltage transmission lines bring electricity from the grid to the site’s transformer yard.',
    path: 'Power plants → grid → transmission line → transformer',
    insight: 'Everything downstream depends on this connection, which is why the site also plans for it to fail.',
  },
  transformer: {
    chapter: 'power',
    name: 'Transformer',
    label: 'TRANSFORMER',
    description:
      'Uses magnetic coupling to change alternating-current voltage. Here, incoming utility power steps down before distribution through the facility.',
    path: 'Utility → transformer → switchgear',
    insight: 'Voltage is changed in stages. The exact levels depend on the electrical design.',
    source: doe,
  },
  switchgear: {
    chapter: 'power',
    name: 'Switchgear',
    label: 'SWITCHGEAR',
    description:
      'Switches and circuit breakers route electricity, isolate equipment, and interrupt fault currents. A transfer switch beside it can move the load to the standby generator.',
    path: 'Transformer → switchgear → UPS',
    insight:
      'Isolation lets a section be disconnected for a fault or planned work. Alternate routes must be designed to carry the remaining load.',
    source: doe,
  },
  ats: {
    chapter: 'power',
    name: 'Transfer switch',
    label: 'TRANSFER SWITCH',
    description:
      'Moves the load from the utility supply to the standby generator when the utility fails, and back again when it returns.',
    path: 'Utility or generator → transfer switch → UPS',
    insight: 'The UPS carries the load through the seconds the generator needs to start and the switch needs to move.',
  },
  ups: {
    chapter: 'power',
    name: 'UPS & batteries',
    label: 'UPS',
    description:
      'An uninterruptible power supply uses stored energy to keep its connected equipment running during a supply interruption.',
    path: 'Switchgear → UPS → IT distribution',
    insight:
      'Ride-through is finite: seconds to minutes, depending on stored energy and load. It covers the gap while the standby generator starts.',
    source: doe,
  },
  generator: {
    chapter: 'power',
    name: 'Standby generator',
    label: 'GENERATOR',
    description:
      'An engine drives an electrical generator. When the utility supply fails, a transfer switch connects this alternate supply.',
    path: 'Generator → transfer switch → UPS → loads',
    insight:
      'This is a parallel supply branch, not a stage electricity must always pass through. Fuel and maintenance limit how long it can run.',
    source: doe,
  },
  pdu: {
    chapter: 'power',
    name: 'Power distribution',
    label: 'BUSWAY',
    description:
      'Distribution panels, overhead busways, and rack power strips carry electricity from the facility supply to the individual server power supplies.',
    path: 'UPS → busway → rack PDU → server power supply',
    insight:
      'This is the last hop before the server. Many servers have two power supplies, one on each of two separate paths, so either path can fail or be serviced without the server stopping.',
    source: ibm,
  },
  'rack-pdu': {
    chapter: 'power',
    name: 'Rack power strip',
    label: 'RACK PDU',
    description:
      'A vertical strip of outlets in the rack feeds each server’s power supplies. Racks often carry two strips, one for each power path.',
    path: 'Busway → rack PDU → server power supplies',
    insight: 'Many rack PDUs meter each outlet, so operators can see how much power every server draws.',
    source: ibm,
  },
  psu: {
    chapter: 'power',
    name: 'Server power supply',
    label: 'PSU',
    description:
      'Converts alternating current from the rack power strip into the low-voltage direct current that the server’s boards use.',
    path: 'Rack PDU → power supply → motherboard',
    insight:
      'Each conversion loses some energy as heat, so efficient power supplies cut both the electricity bill and the cooling load.',
    source: doe,
  },
  rack: {
    chapter: 'compute',
    name: 'Server rack',
    label: 'RACK',
    description:
      'A standard frame whose rails hold equipment 19 inches (48 cm) wide. Servers, switches, and power strips stack in rack units (1U = 1.75 in); a common rack holds 42U.',
    path: 'Data hall → row → rack → server',
    insight:
      'Racks are budgeted in kilowatts. Dense AI racks now exceed 100 kW each (DOE, 2024), which pushes cooling toward liquid.',
    source: rack19,
  },
  server: {
    chapter: 'compute',
    name: 'Inside a server',
    label: 'SERVERS',
    description:
      'A server is a computer built to provide a service. This open chassis shows processors, memory, storage, power supplies, fans, and network interfaces.',
    path: 'Request → network interface → processor ↔ memory / storage',
    insight:
      'Every online service runs on machines like this. The parts follow the work: this is an accelerated AI server, but many servers have no GPU at all.',
    source: ibm,
  },
  cpu: {
    chapter: 'compute',
    name: 'CPU',
    label: 'CPU',
    description:
      'The central processor runs instructions and coordinates the operating system and applications. It accesses active data through the memory system.',
    path: 'Instructions + data → CPU → results',
    insight:
      'Clock speed alone does not determine useful work. Memory access, software, and the workload all influence performance.',
    source: ibmCpu,
  },
  gpu: {
    chapter: 'compute',
    name: 'GPU / accelerator',
    label: 'GPU',
    description:
      'Thousands of parallel execution units work on suitable computations at once, such as the matrix operations used by AI models. In this server, cold plates carry the GPUs’ heat into liquid.',
    path: 'Data → parallel computation → results',
    insight:
      'A GPU accelerates workloads that suit it. It still needs data, memory, power, cooling, and supporting software.',
    source: ibmGpu,
  },
  memory: {
    chapter: 'compute',
    name: 'Working memory',
    label: 'RAM',
    description:
      'RAM holds instructions and data being used by the processors. Ordinary DRAM loses its contents when power is removed.',
    path: 'Storage → RAM ↔ processor',
    insight:
      'Capacity determines how much working data fits nearby. Bandwidth determines how fast it can be delivered.',
    source: ibmCpu,
  },
  storage: {
    chapter: 'compute',
    name: 'Persistent storage',
    label: 'STORAGE',
    description:
      'Solid-state drives and hard drives retain data without continuous power. A server may use local drives or reach shared storage over the network.',
    path: 'Application ↔ local drives or shared storage',
    insight:
      'Persistent does not mean indestructible. Storage systems still need protection against failure and data loss.',
    source: ibm,
  },
  'air-handler': {
    chapter: 'cooling',
    name: 'Air handler',
    label: 'AIR HANDLER',
    description:
      'Fans move cooled air into the cold aisles. Warm air from the hot aisle returns across a cooling coil, which transfers its heat into another cooling circuit.',
    path: 'Cold aisle → servers → hot aisle → cooling coil',
    insight:
      'Rack fronts face each other across a cold aisle (blue) and exhaust into a shared hot aisle (orange), so cold supply and hot return don’t mix.',
    source: doe,
  },
  'cold-aisle': {
    chapter: 'cooling',
    name: 'Cold aisle',
    label: 'COLD AISLE',
    description:
      'Rack fronts face each other across the cold aisle, where cooled air arrives and the servers draw it in.',
    path: 'Air handler → cold aisle → server intakes',
    insight:
      'Keeping cold supply and hot exhaust apart, sometimes with doors and roofs over an aisle, lets the cooling run warmer and use less energy.',
    source: doe,
  },
  'hot-aisle': {
    chapter: 'cooling',
    name: 'Hot aisle',
    label: 'HOT AISLE',
    description:
      'Rack backs share the hot aisle, which collects the servers’ warm exhaust and returns it to the air handler.',
    path: 'Server exhausts → hot aisle → air handler',
    insight:
      'If hot exhaust leaks back into the cold aisle, servers breathe warmer air and the cooling has to work harder.',
    source: doe,
  },
  fans: {
    chapter: 'cooling',
    name: 'Server fans',
    label: 'FANS',
    description:
      'Fans pull cool air in at the front of the server and push warm air out of the back, across the parts the liquid loop does not reach.',
    path: 'Cold aisle → fans → components → hot aisle',
    insight: 'Even a liquid-cooled server needs airflow for its memory, storage, and power supplies.',
    source: doe,
  },
  'cold-plate': {
    chapter: 'cooling',
    name: 'Cold plate',
    label: 'COLD PLATES',
    description:
      'A thermally conductive plate sits against a chip. Coolant flowing through channels inside the plate carries the chip’s heat away. Here, cold plates sit on the three GPUs.',
    path: 'Cool supply → cold plate on chip → warm return → CDU',
    insight:
      'The coolant stays inside a sealed circuit. In this design, it does not flow freely over the electronic components.',
    source: doe,
  },
  cdu: {
    chapter: 'cooling',
    name: 'Coolant distribution unit',
    label: 'CDU',
    description:
      'A CDU circulates and controls coolant for IT equipment. Its heat exchanger transfers heat between the IT loop and the facility loop.',
    path: 'IT coolant → heat exchanger → facility coolant',
    insight: 'The two fluids exchange heat without mixing. A CDU is an interface, not the final destination for heat.',
    source: doe,
  },
  'facility-loop': {
    chapter: 'cooling',
    name: 'Facility water loop',
    label: 'FACILITY WATER',
    description:
      'Pipes carry warm water from the CDUs out to the dry coolers and bring cooled water back. This loop never touches the IT coolant; the two exchange heat inside the CDU.',
    path: 'CDU → warm water → dry coolers → cooled water → CDU',
    insight: 'The warmer this water can run, the more of the year outdoor air alone can cool it, without chillers.',
    source: doe,
  },
  'heat-rejection': {
    chapter: 'cooling',
    name: 'Outdoor heat rejection',
    label: 'DRY COOLERS',
    description:
      'The outdoor plant ultimately transfers heat to the environment. This model depicts fan-assisted dry coolers, which suit warm-water liquid cooling.',
    path: 'Facility loop → outdoor equipment → environment',
    insight:
      'A dry cooler blows outdoor air across a sealed coil and uses almost no water, but struggles on hot days. A cooling tower evaporates water, which cools better but consumes it. A chiller runs a refrigeration cycle to make water colder than the outside air, at an energy cost. Many sites combine them, trading energy use against water use.',
    source: doe,
  },
  fiber: {
    chapter: 'network',
    name: 'Fiber entrance',
    label: 'FIBER',
    description:
      'Optical fiber links the building to carriers and other facilities, often landing in a meet-me room where networks interconnect. Routers at the network boundary direct traffic onward.',
    path: 'Outside network ↔ fiber entrance ↔ border routers',
    insight:
      'This model has two separate fiber entrances. Diverse routes help only if they avoid the same failure: two cables in one trench can be cut together.',
  },
  switch: {
    chapter: 'network',
    name: 'Spine & border switches',
    label: 'SPINE',
    description:
      'Switches forward traffic toward its destination. In a leaf-spine fabric, the leaf switch at the top of each rack connects up to spine switches like these, which link every leaf. Border switches connect the fabric to the outside.',
    path: 'Server → leaf → spine → leaf → another server',
    insight:
      'Links have finite capacity. Leaf-spine fabrics can be oversubscribed; topology alone does not guarantee unlimited bandwidth.',
    source: cisco,
  },
  'cable-tray': {
    chapter: 'network',
    name: 'Cable trays',
    label: 'CABLE TRAYS',
    description:
      'Overhead trays carry fiber and copper cables between the racks and out to the spine switches, kept apart from the power busways.',
    path: 'Server → leaf switch → cable tray → spine',
    insight: 'Tidy cabling keeps airflow clear and makes it possible to trace and replace a single link.',
    source: doe,
  },
  leaf: {
    chapter: 'network',
    name: 'Top-of-rack switch',
    label: 'LEAF SWITCH',
    description:
      'The top unit of each rack is a leaf switch. Every server in the rack plugs into it, and it connects up to the spine.',
    path: 'Server → leaf (top of rack) → spine',
    insight: 'Traffic between two servers in the same rack never leaves it; traffic between racks crosses the spine.',
    source: cisco,
  },
  nic: {
    chapter: 'network',
    name: 'Network interface',
    label: 'NIC',
    description: 'A network interface connects the server to the fabric, sending and receiving data through its ports.',
    path: 'Processor / memory ↔ interface ↔ leaf switch',
    insight: 'The interface is one stage in the journey. Software and other links can limit end-to-end throughput.',
    source: cisco,
  },
  monitoring: {
    chapter: 'operations',
    name: 'Monitoring & operators',
    label: 'CONTROL ROOM',
    description:
      'Sensors report conditions such as temperature and electrical load. Operators use these signals to investigate problems and plan maintenance.',
    path: 'Sensors → monitoring → operator → action',
    insight:
      'Operators often spot trouble in the data before anything fails: a rising inlet temperature or a circuit near its limit. This world shows no live readings.',
    source: ibm,
  },
  technician: {
    chapter: 'operations',
    name: 'Technicians',
    label: 'TECHNICIAN',
    description:
      'On-site staff replace failed parts, install new equipment, and carry out planned maintenance around the clock.',
    path: 'Alert or work order → technician → repair → back in service',
    insight:
      'Much of the work is planned: parts are replaced on a schedule, and one path is taken offline while its twin carries the load.',
  },
  security: {
    chapter: 'operations',
    name: 'Physical access',
    label: 'ACCESS GATE',
    description:
      'Checkpoints, credentials, and controlled doors restrict entry to the facility and sensitive equipment areas.',
    path: 'Identity check → authorized zone → recorded access',
    insight:
      'Physical access controls complement software permissions and cybersecurity. Neither layer replaces the other.',
    source: ibm,
  },
  fire: {
    chapter: 'operations',
    name: 'Fire detection & suppression',
    label: 'FIRE PANEL',
    description:
      'Detectors raise the alarm early. Sprinklers here are often pre-action systems: their pipes stay dry until a detector trips, so a damaged pipe cannot flood the equipment. Some rooms use a clean-agent gas instead of water.',
    path: 'Detection → alarm → planned response',
    insight: 'Regular inspection and trained response are part of protection, alongside the equipment itself.',
    source: sprinklers,
  },
};

// Parts drawn inside the open server chassis, in the order the drawer lists them.
export const serverParts = ['server', 'cpu', 'gpu', 'memory', 'storage', 'nic', 'cold-plate', 'psu', 'fans'];

export const sources = [
  { title: 'NREL for U.S. DOE · Best Practices Guide for Energy-Efficient Data Center Design (2024)', url: doe },
  { title: 'IBM · What is a data center?', url: ibm },
  { title: 'IBM · What is a central processing unit (CPU)?', url: ibmCpu },
  { title: 'IBM · What is a GPU?', url: ibmGpu },
  { title: 'Cisco · Massively Scalable Data Center Network Fabric Design (white paper, 2024)', url: cisco },
  { title: 'Wikipedia · 19-inch rack', url: rack19 },
  { title: 'Wikipedia · Fire sprinkler system', url: sprinklers },
];
