# Selected speaker notes

## A three-phase shelf can feed single-phase PSU modules — Chapter 8, slide 6

“The shelf receives three-phase power, but each PSU module can use a single phase. In this example, there are 480 volts between phases and about 277 volts from each phase to neutral. The shelf spreads those phase-to-neutral connections across its modules.

“Each module converts its AC input to 50-volt DC, and their outputs share the rack bus. So the shelf uses all three phases even though each individual PSU uses only one. Balancing the modules across the phases spreads the input current and smooths their combined power demand. Neutral is separate from protective earth.”

The diagram is the Advanced Energy ORv3 example; it does not establish the PSU wiring of every GB300 rack.

Source: [Advanced Energy ORv3 PSU](https://www.advancedenergy.com/en-us/products/ac-dc-power-supply-units/power-shelves/ocp-compliant/orv3-psu/).

## Should we step down first or rectify first? — Chapter 9, slide 10

“New higher-voltage SiC devices could make SSTs simpler and more competitive. Their widespread adoption in data centers still has to be demonstrated.”

Source: [Wolfspeed 10 kV SiC announcement](https://www.wolfspeed.com/company/news-events/news/wolfspeed-introduces-industrys-first-commercially-available-10000v-silicon-carbide-power-mosfet/).

## An 800 V DC feeder needs DC-rated protection — Chapter 9, slide 12

“Both AC and DC circuits need fault protection. With AC, the current naturally crosses zero, helping a breaker extinguish its arc after the contacts open. DC has no periodic natural zero, so the protection must force the current to stop.

“Here, both the rectifier and the charged bus capacitor can feed a short circuit. The cable also stores magnetic energy. The breaker must interrupt that DC fault and withstand the voltage afterward—zero current does not mean zero voltage. Switching off the AC supply alone does not remove the stored energy.”

Source: [ABB DC protection paper](https://library.e.abb.com/public/5cd83dcb95a74dcdb571be5f256e1af8/9AKK108470A9606_en_B_Protection%20Devices%20for%20Direct%20Current%20Applications%20-%20Technical%20Application%20Paper.pdf).

## Microsoft’s ambition for Fairwater — Chapter 10, slide 5

“The distributed networking of Microsoft’s Fairwater sites is designed to enable them to support training models with hundreds of trillions of parameters.”

Microsoft, November 12, 2025. This describes intended capability, not a reported completed training run.

For the dedicated-fiber line: Microsoft describes an AI WAN over dedicated fiber
between its sites. Owning that path helps avoid competition with unrelated
traffic; distance still creates propagation delay. The claim does not establish
that every switch, endpoint and workload is free of bottlenecks.

Source: [Microsoft Fairwater feature](https://news.microsoft.com/source/features/ai/from-wisconsin-to-atlanta-microsoft-connects-datacenters-to-build-its-first-ai-superfactory/).

## Copper for short links; optical fiber for longer runs — Chapter 10, slide 10

“The electronics at each end work with electrical signals. Copper carries that signal along the cable. At high signaling rates, loss and distortion make it harder for the receiver to distinguish the symbols as the cable gets longer. Short passive copper cables keep the connection simple and use very little power.

“With fiber, the transmitting module converts the electrical signal into modulated light. The receiving module detects that light and converts it back into an electrical signal. Both ends do both jobs on a two-way link. These 400G examples span two meters of passive copper, fifty meters of multimode fiber and five hundred meters of single-mode fiber. The cable route and required data rate determine which supported reach you need.”

Source: [NVIDIA LinkX product overview](https://docs.nvidia.com/networking/display/400g100gpam4ovdev/linkx-100g-pam4-product-line-overview), checked September 16, 2026.

## Co-packaged optics shortens the electrical path inside the switch — Chapter 10, slide 11

“Pluggable optics puts conversion at the front panel. CPO moves it beside the switch chip, shortening the electrical path. Both approaches remain in use.”

Sources: [NVIDIA CPO](https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/), [Spectrum-6 optical options](https://blogs.nvidia.com/blog/nvidia-spectrum-six-arrives-in-gigascale-ai-factories/).

## Cross-leaf bandwidth is shared by the servers beneath each leaf — Chapter 10, slide 13

“The full example has sixteen server links, with four servers under each leaf. Here we zoom in on one leaf. Its four 400-gigabit server ports can offer 1,600 gigabits per second, but two 400-gigabit uplinks can carry only 800 toward the other leaves. If all four servers send across that boundary at once, their traffic shares the narrower path. That is the two-to-one ratio.

“Four uplinks raise the shared capacity to 1,600 gigabits per second, matching the four server ports. For the same 32 gigabytes crossing this boundary, the ideal transfer time falls from 0.32 to 0.16 seconds. Traffic staying under the same leaf does not use these uplinks. So the benefit depends on where the communicating servers sit and which traffic actually crosses the boundary.”

Model: [`fabricBudget`](prototypes/networking-model.js), four leaves with four 400 Gb/s server links each; two or four 400 Gb/s uplinks per leaf. The displayed transfer assumes balanced traffic in one direction.

## Four fast senders can overwhelm one receiver port — Chapter 10, slide 15

“Four senders can offer 1,600 gigabits per second, but the receiving link carries only 400. Packets accumulate in the switch’s output queue because they arrive faster than that link can drain them. Adding spine bandwidth leaves this final 400-gigabit link unchanged.

“To receive faster, the switch port, cable or optics, and receiving network adapter must all support a higher link rate, and the receiving system must be able to absorb the data. Another option is to spread the traffic across additional receiving links or servers, if the workload can use them. Pacing the senders can control the queue, but it does not increase the link’s capacity.”

Source for supported adapter link rates: [NVIDIA ConnectX-7 specifications](https://networking-docs.nvidia.com/connectx7hw/specifications).

## Meta built large AI clusters with both Ethernet and InfiniBand — Chapter 10, slide 16

“RoCE means RDMA over Converged Ethernet. RDMA is Remote Direct Memory Access:
network adapters transfer data into permitted remote memory without the usual
CPU-managed copying path for each transfer.

“Either fabric still needs several choices to work together. Routing chooses the
paths. Congestion control adjusts sending rates when traffic competes. Collective
software organizes exchanges among participating GPUs. Job placement chooses
which servers run together. Those choices determine how effectively a workload
uses the physical network, and feed back into its capacity and topology.”

Sources: [NVIDIA RoCE documentation](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/), [Meta’s 2024 cluster account](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/).

## Campus fiber handoff — Chapter 10, slide 18

“Here we follow the connection out of the data center. The border router directs traffic toward outside networks. The patch panel provides an organized place to terminate and connect cables; it does not route the traffic.

“In the meet-me room, the data center’s fiber connects to a carrier’s fiber. A carrier is a company that provides network connectivity. From there, fiber runs through the building entrance and outside ducts into the carrier’s network. The service could be a private connection to another facility or access to the Internet.

“For the facility designer, this means reserving space for the handoff equipment and planning the fiber entrances and routes. Those physical connections must be ready alongside the racks, power and cooling.”

Source: [Equinix Cross Connect documentation](https://docs.equinix.com/cross-connect/), describing physical connections between customers and service providers and building meet-me-room connections.

## Meta built storage in tiers to keep GPUs supplied — Chapter 10, slide 21

“This is Meta’s Research SuperCluster, described in January 2022. Its storage has three jobs: 175 petabytes of bulk storage, 46 petabytes of cache for repeated reads, and 10 petabytes of shared file storage. The cache keeps copies of data that will be used again. Meta’s AIRStore also prepares a dataset once so several training runs can reuse it, reducing repeated preparation and transfers between regions.

“The network has to carry those prepared inputs from storage to the GPUs fast enough to keep the work moving. That makes storage part of the facility design: more equipment needs rack space, power, cooling and cable routes. Meta says RSC required changes across all of those systems. The GPU racks in the photograph depend on that entire supply path.”

Source: [Meta’s January 24, 2022 RSC account](https://ai.meta.com/blog/ai-rsc/), storage description and AIRStore sections checked September 16, 2026.

## CRAH versus CDU — Chapter 11, slide 4

“A CRAH is a computer room air handler. Its fans move room air across a chilled-water coil. Heat goes from the air into the water, and cooled air goes back to the room.

“A CDU is a coolant distribution unit. It pumps coolant through the liquid-cooled equipment and controls the coolant supply. In the liquid-to-liquid CDU shown here, a heat exchanger passes that heat into a separate facility-water loop. The two liquids do not mix.

“A rack can need both. Cold plates take heat from selected chips into the CDU loop; memory, power supplies and other components outside those plates still release heat into air. A CRAH can handle that remaining air load.”

Liquid-to-air CDUs also exist: they reject rack-liquid heat into room air instead of facility water. The diagrams in this comparison use liquid-to-liquid CDUs.

Sources: [DOE FEMP cooling systems](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers), [CoolIT CDU architectures](https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/), checked September 16, 2026.

## The chip is warmer than the coolant — Chapter 11, slide 9

“The coolant is at 35 degrees, but heat must travel from the chip through the package, thermal interface and cold plate before it reaches that coolant. Moving heat through that path requires a temperature difference.

“Thermal resistance tells us how large that difference is per watt. At 400 watts, the first path adds 32 degrees: the chip is 67 degrees. The more resistant path adds 48 degrees: the chip is 83 degrees, above our chosen 80-degree limit. Both have the same coolant temperature. A cool inlet alone cannot tell us that the chip is cool enough.”

These are stipulated steady-state junction-to-local-fluid resistances, not measured product specifications. A poor thermal interface or insufficient local flow can worsen the effective path. Model: `deviceTemperature` in [cooling-capture-model.js](prototypes/cooling-capture-model.js).

## The pump and plumbing determine actual flow — Chapter 11, slide 11

“The pump curve shows the pressure the pump can provide at each flow. The circuit curves show the pressure needed to push that flow through the pipes, hoses and cold plates. The actual flow is where available and required pressure meet.

“Adding a restriction makes the circuit demand more pressure at every flow. With the same pump, the intersection moves from 2 litres per second to about 1.41. The same 84 kilowatts is now carried by less water, so the coolant warms by about 14.1 degrees instead of 10.”

Model: `hydraulicPoint` in [cooling-capture-model.js](prototypes/cooling-capture-model.js), using water at 1 kg/L and specific heat 4.2 kJ/(kg·°C). These are teaching curves at one pump speed, not a vendor selection chart. Flow balancing is necessary but can change after commissioning: fouling, a partly closed valve or a new restriction can starve a branch while the total flow looks satisfactory. That point stays in the reading instead of occupying another slide.

Source for filtration/fouling and coolant-path qualification: [OCP cold-plate requirements](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf), pp. 7, 11–12.

## CDU approach compares two supply temperatures — Chapter 11, slide 12

“Facility water arrives at 30 degrees Celsius. The separate coolant leaving for the chips is at 35 degrees. The difference between those supply temperatures is a five-degree approach. The rack coolant stays warmer so heat can pass into the facility water. This gap is different from how much one fluid warms between its supply and return.”

A temperature **difference** of 5°C equals 5 K; Celsius and kelvin have equal-sized increments. The slide uses °C consistently so the unit does not distract from the two measurement points. This is not a 5 K absolute temperature. Source: [NIST SI temperature units](https://www.nist.gov/pml/special-publication-330/sp-330-section-2).

## CoolIT CHx2000 — Chapter 11, slide 13

The manufacturer separately lists 2 MW at 5°C approach and 2,125 L/min at 35 psi. These are thermal and hydraulic rating points; do not imply that both maxima occur together under unspecified conditions. The visible photo credit remains; this qualification has moved here from the slide footer.

Source: [CoolIT CHx2000](https://www.coolitsystems.com/cdu-product/chx2000/), checked September 16, 2026.

## Retrofit: keep enough air cooling — Chapter 11, slide 17

“The cold plates take 85 kilowatts of this 100-kilowatt rack into liquid. The other 15 kilowatts still goes into room air, which fits the available 20-kilowatt room-air cooling allowance. This gives us a cooling route to develop; we still need to qualify the liquid circuit and access for maintenance.”

## Check the place, time and heat balance — Chapter 14, slides 1–4

“The plant supply can look normal while one row has a problem. Start with measurements at that row. A message delivered now can still contain a ten-minute-old reading; use the sensor’s observation time.

“By slide 4, temperatures have stabilized. All 2.09 megawatts enters this measured water branch. With a ten-degree water rise, the current 50-kilogram-per-second flow accounts for the heat. Combining the old 100-kilogram reading with today’s temperatures would imply twice as much heat. This supports the current measurement; it does not tell us why flow fell.”

The water balance is a stipulated steady-state example. During warming, some energy accumulates in equipment and fluid, so electrical input need not equal instantaneous measured heat removal. Model: [operations-model.js](prototypes/operations-model.js).

## A command is not cooling readiness — Chapter 14, slides 5–8

“Local controls maintain equipment conditions. Plant controls bring capacity into service. The scheduler decides when to add computing work. A reply that says ‘command received’ does not establish that the required flow has arrived.

“Here cooling removes five megawatts while existing work produces four. Adding the job immediately raises heat to six before standby cooling is ready. Waiting keeps the existing work running, then admits the job after measured capacity reaches seven.”

For an optional calculation, a 1 MW deficit lasting three minutes accumulates 50 kWh of heat. This slide supplies no permitted thermal buffer or temperature margin. The reader retains the separate transition-allowance exercise.

The Google case describes the **2018 autonomous system**: the optimizer selected cooling actions every five minutes, with independent local checks and operator exit. That cadence is distinct from protective-control response time. Source: [Google DeepMind](https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/).

## A pause changes timing, not the job’s energy — Chapter 14, slides 9–10

“Both plans need three running hours at four megawatts: twelve megawatt-hours. Pausing during the grid event lowers site power from twenty-four to twenty megawatts during those hours. The job finishes two hours later. A deadline of twenty hundred permits that pause; seventeen hundred does not.”

Assume the job retains progress, with no restart overhead, and 24 MW is available after the event. The adjacent real example is Google’s dated 2023 demand-response pilot with Northern Wasco County PUD; the numerical schedule is illustrative. Source: [Google demand response](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption).

## Check dependencies and command targets — Chapter 14, slides 11–12

“Removing unit C leaves six megawatts for a five-megawatt load. But removing control power shared by A and B stops those units too. The maintenance boundary matters as much as the spare equipment count.

“After a row changes, the physical branch and the control record must agree. Sending the command to the correct row is only the first check. Observe that row’s actual response.”

The shared-supply diagram is a teaching topology, not a switching procedure. The wrong mapping explains the misdirected command; it does not establish the cause of low flow.

## Test the whole dependency chain — Chapter 14, slides 13–14

Pair Cloudflare’s November 2023 failure with its 2024 follow-up. Earlier testing omitted dependencies outside the facility’s high-availability portion. The later seven-minute result refers to API and dashboard operation after the March failure; analytics recovered later. It is not a seven-minute facility restart or universal service-recovery time.

Sources: [November 2023 report](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/), [April 2024 follow-up](https://blog.cloudflare.com/major-data-center-power-failure-again-cloudflare-code-orange-tested/).

## Recovery has different endpoints — Chapter 14, slides 15–17

“A live copy can survive a device failure, but a software error can affect both copies. An earlier valid state gives us another recovery route.” Gmail’s 2011 incident illustrates recovery from offline tape; it does not prescribe tape for every system. Source: [Gmail incident account](https://gmail.googleblog.com/2011/02/gmail-back-soon-for-everyone.html).

For London, the 14 h 15 min interval runs from cooling repair to the initial cloud-service restoration milestone in Google’s final July 29 report. Part of one zone was affected; residual issues lasted longer. Source: [Google Cloud incident](https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2).

Llama’s 466 interruptions include 47 planned events and 419 unexpected events over 54 days. Effective training time measures productive training against elapsed time, not facility availability. The lesson is to preserve progress and make recovery routine. Source: [Llama 3, §3.3.4](https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4).

## What releases the extra work? — Chapter 14, slide 18

Ask the question before revealing the answer. “Correcting the mapping fixes where the command goes. Now show that the right row responds and that its current flow and temperatures meet the new workload’s requirement. Correct configuration alone is not proof of recovered cooling.”

## Racks can stay powered while cooling stops — Chapter 16, slides 2–4

“The battery supports the IT supply, but the pump is on a separate utility-fed circuit. More stored energy extends the electrical duration without reconnecting that pump. Protecting the pump supply uses more battery power, so electrical duration becomes shorter. That change closes one dependency; the integrated outage test still has to show flow, acceptable temperatures and correct application operation.”

The example has 600 kWh usable DC, 90% discharge efficiency, a 2.5 MW inverter and 2 MW IT. Its ideal electrical duration is 16.2 minutes. Adding 200 kWh gives 21.6 minutes; supplying 0.2 MW of cooling auxiliaries instead gives 14.73 minutes. Generator readiness at minute 10 precedes the two-minute restoration sequence. These energy calculations do not establish a permissible interruption of heat removal. The [outage reader](index.html#c01-coupled-outage) retains the energy ledger and test brief.

## An upgrade only helps if it changes the limiting resource — Chapter 16, slides 5–7

“During hot weather, cooling limits this site to 550 racks. Saving auxiliary electricity helps energy use but leaves that cooling limit unchanged. The supplied cooling upgrade raises the limit to 650 racks. Now accept only 600 complete rack paths: those paths become the limit. Finishing more paths makes cooling the limit again.”

The cooling proposal explicitly keeps auxiliaries at 25 MW; this is an illustrative paired operating point. The accepted paths include all required services to the same racks. The workload remains 58 MW, so current site demand remains 58 + 25 = 83 MW when the capacity control changes. Capacity and demand should not be read as interchangeable totals. See the [weather capstone](index.html#c02-weather-capacity).

## A rack can fit while maintenance cannot — Chapter 16, slides 8–10

“Both options deliver 120 kilowatts to the load. Their conversion losses differ, but both remain within the room’s power and cooling limits. The sidecar’s proposed position creates the hold: the UPS module cannot leave through its removal route. Move the sidecar while preserving that route. The electrical losses stay the same.”

A requires 125 kW AC; B requires approximately 126.24 kW. All equipment is inside the same room, so room heat includes every conversion loss. These supplied efficiencies do not establish which architecture is universally better. The [retrofit reader](index.html#c03-density-retrofit) retains the intermediate bus-current calculation and complete acceptance requirements.

## A faster network phase improves only part of the job — Chapter 16, slides 11–13

“The job spends sixty seconds computing, twenty transferring data, and ten on other work. Doubling the sender does nothing while the fabric still limits the path to forty gigabytes per second. Doubling that bottleneck halves the transfer phase. The whole cycle falls from ninety to eighty seconds: forty cycles per hour becomes forty-five.”

The work per cycle stays fixed and phases do not overlap. These are achieved payload rates, not port labels. Check the complete measured cycle and correct output after the change. The old compute-time fraction is intentionally not presented as device utilization or measured useful output. See the [network capstone](index.html#c04-stalled-job).

## A passing test releases the next group — Chapter 16, slides 14–16

Use the Abilene photograph as a physical setting, then explicitly switch to the illustrative 300/250/250-rack register. The photo establishes neither these rack counts nor an acceptance status. Oracle captions it July 15, 2026; the source caption was rechecked during this revision.

“Group A is ready today. Group B needs network work and testing. Group C needs cooling acceptance. A planned test date does not add operating racks. If C’s first test fails, correction and a successful retest move its earliest opening from day seven to day twelve.”

Separate qualified teams and all other required resources are assumed available. Group A remains at 300 racks; after B passes on day six, 550 are accepted. The final 250 join only after C passes. Keep the accepted operating configuration and isolation of live groups intact while construction continues. Source: [Oracle media gallery](https://www.oracle.com/data-centers/); schedule: [phase capstone](index.html#c05-open-a-phase).
