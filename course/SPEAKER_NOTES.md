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

## Out with the Old, In with the New — Chapter 11, slide 2

“A CRAH is a computer room air handler. Its fans move room air across a chilled-water coil. Heat goes from the air into the water, and cooled air goes back to the room.

“A CDU is a coolant distribution unit. It pumps coolant through the liquid-cooled equipment and controls the coolant supply. In the liquid-to-liquid CDU shown here, a heat exchanger passes that heat into a separate facility-water loop. The two liquids do not mix.

“A rack can need both. Cold plates take heat from selected chips into the CDU loop; storage, power-distribution electronics and other components outside those plates still release heat into air. A CRAH can handle that remaining air load.”

Liquid-to-air CDUs also exist: they reject rack-liquid heat into room air instead of facility water. The diagrams in this comparison use liquid-to-liquid CDUs.

Sources: [DOE FEMP cooling systems](https://www.energy.gov/cmei/femp/cooling-water-efficiency-opportunities-federal-data-centers), [CoolIT CDU architectures](https://www.coolitsystems.com/products-services/data-center-products/cooling-distribution-units/), checked September 16, 2026.

## GB300 rack coolant connections — Chapter 11, slide 3

Follow CDU → supply manifold → tray quick disconnects → cold plates → return manifold. This is technology coolant on the rack side of the liquid-to-liquid CDU. Facility water stays across the exchanger. The NVIDIA rear view shows the manifolds, not a rear-door exhaust coil. The following slide deliberately teaches that different mechanism.

[Lenovo’s current GB300 guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai#cooling) still specifies hybrid liquid/air heat capture. Air cooling remains part of the system; the opening’s “dead?” question motivates the density limit of relying on air alone.

## Immersion and physical cold plates — Chapter 11, slides 5–6

The supplied 2CRSi diagram is single-phase: the dielectric liquid stays liquid as it circulates through the exchanger. Two-phase immersion boils fluid at the hardware and condenses the vapor so liquid returns. The next photograph shows cold-plate assemblies supplied as GB300 context; the precise manufacturer and model are not verified. Explain the visible hardware without calling gold surface patterns hidden coolant channels.

## The chip is warmer than the coolant — Chapter 11, slide 8

“The coolant is at 35 degrees, but heat must travel from the chip through the package, thermal interface and cold plate before it reaches that coolant. Moving heat through that path requires a temperature difference.

“Thermal resistance tells us how large that difference is per watt. At 400 watts, the first path adds 32 degrees: the chip is 67 degrees. The more resistant path adds 48 degrees: the chip is 83 degrees, above our chosen 80-degree limit. Both have the same coolant temperature. A cool inlet alone cannot tell us that the chip is cool enough.”

These are stipulated steady-state junction-to-local-fluid resistances, not measured product specifications. A poor thermal interface or insufficient local flow can worsen the effective path. Model: `deviceTemperature` in [cooling-capture-model.js](prototypes/cooling-capture-model.js).

## The pump and plumbing determine actual flow — Chapter 11, slide 10

“The pump curve shows the pressure the pump can provide at each flow. The circuit curves show the pressure needed to push that flow through the pipes, hoses and cold plates. The actual flow is where available and required pressure meet.

“Adding a restriction makes the circuit demand more pressure at every flow. With the same pump, the intersection moves from 2 litres per second to about 1.41. The same 84 kilowatts is now carried by less water, so the coolant warms by about 14.1 degrees instead of 10.”

Model: `hydraulicPoint` in [cooling-capture-model.js](prototypes/cooling-capture-model.js), using water at 1 kg/L and specific heat 4.2 kJ/(kg·°C). These are teaching curves at one pump speed, not a vendor selection chart. Flow balancing is necessary but can change after commissioning: fouling, a partly closed valve or a new restriction can starve a branch while the total flow looks satisfactory. That point stays in the reading instead of occupying another slide.

Source for filtration/fouling and coolant-path qualification: [OCP cold-plate requirements](https://www.opencompute.org/documents/ocp-acs-liquid-cooling-cold-plate-requirements-pdf), pp. 7, 11–12.

## CDU approach compares two supply temperatures — Chapter 11, slide 11

“Facility water arrives at 30 degrees Celsius. The separate coolant leaving for the chips is at 35 degrees. The difference between those supply temperatures is a five-degree approach. The rack coolant stays warmer so heat can pass into the facility water. This gap is different from how much one fluid warms between its supply and return.”

A temperature **difference** of 5°C equals 5 K; Celsius and kelvin have equal-sized increments. The slide uses °C consistently so the unit does not distract from the two measurement points. This is not a 5 K absolute temperature. Source: [NIST SI temperature units](https://www.nist.gov/pml/special-publication-330/sp-330-section-2).

## CoolIT CHx2000 — Chapter 11, slide 12

The manufacturer separately lists 2 MW at 5°C approach and 2,125 L/min at 35 psi. These are thermal and hydraulic rating points; do not imply that both maxima occur together under unspecified conditions. The visible photo credit remains; this qualification has moved here from the slide footer.

Source: [CoolIT CHx2000](https://www.coolitsystems.com/cdu-product/chx2000/), checked September 16, 2026.

## Retrofit: keep enough air cooling — Chapter 11, slide 16

“The cold plates take 85 kilowatts of this 100-kilowatt rack into liquid. The other 15 kilowatts still goes into room air, which fits the available 20-kilowatt room-air cooling allowance. This gives us a cooling route to develop; we still need to qualify the liquid circuit and access for maintenance.”

## At Abilene, the heat goes to outdoor air — Chapter 12, slide 2

“Follow the heat from the rack through the separate facility-water circuit and the chiller to outdoor air. The water circulates inside the system; the heat leaves it. Crusoe describes this arrangement at Abilene in August 2025. Initial fill and maintenance still need water.”

Keep the dated design account separate from measured operating performance. The later numerical examples are illustrative, not Abilene data.

Source: [Crusoe’s August 5, 2025 Abilene account](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center).

## Wet tower and weather definitions — Chapter 12, slides 3–4

In the open wet tower, water is distributed over fill by nozzles or a distribution deck. Air contacts thin water films or droplets; some evaporates, and cooled water collects in the basin. The air arrow indicates that contact. It is not vapor leaking out of a closed pipe. [DOE component guide](https://www.energy.gov/sites/default/files/2013/10/f3/waterfs_coolingtowers.pdf), pages 1–3.

Dry bulb and wet bulb are two readings of the same air. Wet bulb is lower in unsaturated air and equals dry bulb at saturation. The definition slide uses original teaching wording in a large quotation-style layout, not a verbatim quotation attributed to a publisher. [NWS definitions](https://www.weather.gov/source/zhu/ZHU_Training_Page/definitions/dry_wet_bulb_definition/dry_wet_bulb.html).

## Humid air leaves less room for evaporative cooling — Chapter 12, slide 5

“Both days have the same 35-degree air temperature. A wetted, ventilated sensor cools more in dry air because more evaporation is possible. Switch to humid air: the wet-bulb reading rises from 22 to 28 degrees. That leaves less opportunity to cool water by evaporation.”

Wet bulb describes an air condition. It is not the temperature a tower automatically delivers.

## Dry coolers follow dry bulb; wet towers follow wet bulb — Chapter 12, slide 6

Reveal one interface at a time, following the heat path back from outdoors toward the rack. “Each exchanger needs its own temperature difference. In this example, the wet route reaches the rack at 35 degrees. Now change only the humidity: the same route reaches 41 degrees and no longer meets the rack requirement.”

The fixed gaps belong to this illustrative temperature screen. Flow, return temperatures and the separate 84 kW example remain in the [weather reader](index.html#d11-weather-and-operating-envelope); they need not be calculated aloud.

## When do we need a chiller? — Chapter 12, slide 7

“Refrigeration can keep the load circuit colder while sending heat to a warmer outdoor sink. The compressor needs electricity to do that. Ten megawatts collected plus two megawatts of compressor electricity means twelve megawatts leave the condenser.”

The Chapter 11 CoolIT CHx2000 is a CDU with pumps and a heat exchanger, not a compressor. This slide stays here because it answers the preceding outdoor-temperature problem: refrigeration can deliver colder water when direct heat exchange cannot. This is a separate chiller example, with pumps and fans outside its boundary. On slide 8, introduce whole-plant COP 4 as four units of heat moved per unit of cooling electricity, including pumps and fans. The [reader](index.html#d11-heat-rejection) retains the comparison between equipment and whole-plant COP.

## Economizer mode — Chapter 12, slide 9

- The supplied image shows a functional heat path: when outdoor conditions permit, pumps and fans can carry the cooling duty without the compressor.
- “From racks” and “back to racks” compress the route; a CDU may separate technology coolant and facility water. Follow the heat without treating every arrow as one shared water circuit.

## Hot weather can leave less power for computing — Chapter 12, slide 11

Start at 8 MW computing in cool weather. Ask which part of the power bar will grow before switching to hot weather. “The cooling plant can still remove the heat, but its electricity now takes us beyond the site’s 10 MW supply. Lower computing power until the whole bar fits. Cooling electricity falls too, because there is less heat to move.”

The fitted hot point is 7.68 MW computing, 1.92 MW cooling and 0.4 MW other demand. The algebra stays in the [reader](index.html#d11-weather-and-operating-envelope). On slide 12, keep the proposed 8 MW load fixed to show why an average can hide infeasible hot hours; this is distinct from the reader’s reduced-load daily energy schedule.

## Evaporation leaves dissolved minerals behind — Chapter 12, slide 14

Use the three controls in order. “Some water evaporates and carries heat away. The dissolved minerals remain, so the water becomes more concentrated. Discharge some of that water, then replace both the evaporated water and the discharge. Replacement water brings some minerals too.”

The preceding closed-loop comparison identifies which circuit needs this replacement. Blowdown is the discharge; makeup is the replacement. Concentration ratios and treatment limits remain in the [water reader](index.html#d11-water-and-heat-reuse).

Source: [DOE cooling-tower management](https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management).

## Water taken in and water consumed are different totals — Chapter 12, slide 15

“In this separate example, 125 cubic metres enters, 100 evaporates and 25 leaves as discharge. If that discharge returns to the same basin, the counted consumption is 100. Switch to an unknown destination: the intake meter alone cannot establish that return.”

Keep the water paths visible before discussing any per-kWh metric. The reader retains those calculations and their period and accounting boundaries.

## The customer needs heat only part of the day — Chapter 12, slide 16

“The facility produces heat all day. This customer accepts only part of it, during six hours, and only if its temperature is useful. Close the customer for the day: all the heat still needs an outdoor destination.”

Point to the accepted overlap and the remaining heat. A heat pump can raise delivery temperature but uses electricity. The separate example’s daily energy arithmetic stays in the reader.

## Which plan keeps a complete heat path? — Chapter 12, slide 18

Ask learners to name the surviving heat path and limiting resource before choosing a plan and revealing its explanation. “The tower has no replacement water. The qualified air-cooled alternate can remove enough heat, but keeping full computing power exceeds site electricity. Lower computing power and retain that complete outdoor path.”

The reveal supplies the worked operating point. This synthetic brief assumes the alternate path is qualified; a real transition must also demonstrate flow, temperatures and controls.

## EPC and the late rack change — Chapter 13, slides 1–7

- EPC means engineering, procurement and construction. Commissioning tests the constructed service; it is not the C in the acronym.
- The meme comes before the case. Then establish the unchanged 20 MW IT requirement: 200 racks at 100 kW become 100 racks at 200 kW.
- Electrical, hydraulic and support consequences follow immediately. The phase total can stay fixed while each connection becomes inadequate.
- Electrical example: balanced 480 V three-phase, PF 1. About 120 A becomes 241 A against the original 160 A continuous branch limit.
- Hydraulic example: water, all rack heat to liquid, 10°C rise. Branch flow doubles; the stipulated unchanged hardware needs 80 rather than 20 kPa, exceeding the available 60 kPa.
- The support example separately stipulates twice the rack mass on the same four feet. Power alone does not establish mass. IT duty does not include changing auxiliary power.

## Which delivery should be expedited? — Chapter 13, slides 8–9

- Start a separate schedule case. Electrical installation, cooling installation and utility availability must all reach readiness before integrated testing.
- Compare all four scenarios simultaneously. Earlier cooling does not change the date while switchgear is still last; earlier switchgear can. A late utility connection can become the new controlling path.
- The dates are a teaching dependency model, not a vendor delivery forecast. The full derivation remains in the reader; no fastest-button quiz is needed.

## Prefabrication at different physical scales — Chapter 13, slides 10–13

- Apply E, P and C to the actual electrical plant: coordinated design, ordered package, foundations and placement.
- Off-site assembly can cover an electrical skid or a broader data-hall service assembly. Both allow factory assembly and site construction to overlap; they leave different field connections.
- Houdini: SemiAnalysis reports AWS factory-built data-hall skids and Cupertino Electric participation. The photograph is CEI’s Edgerton factory. It does not identify the pictured equipment as a Houdini unit.
- Siemens–Compass: a jointly developed skid combines 8DJH 36 switchgear with a transformer. The photograph shows the switchgear portion. This case establishes what is assembled, not a universal schedule saving.
- Design freezes, shipping plans and manufacturing dates remain in the reader. The presentation focuses on data-center interfaces and real prefabrication examples.

## Open Compute Project — Chapter 13, slide 14

- OCP publishes shared hardware interface specifications. Open Rack v3 covers rack geometry and 48 V busbar geometry; Universal Quick Disconnect (UQD) specifies coolant-connector mating and performance.
- Two suppliers’ compliant couplings of the same specified interface can mate. That alone does not prove adequate flow or pressure drop for the new rack.
- Return to the 200 kW rack: 4.8 kg/s required versus the example’s existing 3.0 kg/s branch limit. Standardization helps interchangeability; the hydraulic operating point still has to work.
- Sources: [ORv3 revision 1.0](https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf), mechanical and busbar sections; [UQD revision 1.0](https://www.opencompute.org/documents/ocp-universal-quick-disconnect-uqd-specification-rev-1-0-2-pdf), printed pages 4–10. These are the named reference revisions.

## Commission the revised racks — Chapter 13, slides 15–17

- Return explicitly to the same 20 MW rack-change case after the manufacturing examples.
- Factory acceptance covers the tested assembly. Site wiring, piping and control mappings require installed checks before the integrated failure test.
- The alarm identifies A21–A40. The authorized command must reach those same racks; then observe power, temperature and timing against agreed limits.
- The power trace is qualitative. Normal duty, maintenance and recovery tests remain part of complete acceptance, with detail in the reader.


## Which racks can operate now? — Chapter 13, slides 18 and 20

Slide 18 assumes every other acceptance criterion has passed so the learner can isolate the intersection of electrical, cooling and network rack identities. At 200 kW per revised rack, A21–A60 is 40 racks and 8 MW. Extending the cooling coverage to A01 adds 20 eligible racks and gives 12 MW.

The closing exercise changes the evidence: only A21–A40 has a measured failure response that meets the agreed limits and timing. A41–A60 has a command record but no confirmed response. Release the 20 racks in A21–A40, a 4 MW envelope under the stated remaining criteria.

The handover names the released racks, tested topology and configuration revision, including protection settings and control/software versions. Procedures and operating limits must match that evidence. Assign maintenance and isolation responsibilities, and train the operating team. Record excluded racks and each open issue, its operating restriction, decision owner and required evidence or retest. Expanding service requires closing those records.

Detailed derivations and the original separate 100 kW acceptance exercise remain in the [Chapter 13 reader](index.html#d13-commissioning-complete-paths).

## Diagnose Row B — Chapter 14, slides 1–3

- Start with the local chip-temperature alarm and a normal upstream 30°C supply reading.
- Compare complete, time-aligned measurements at the row: before, 100 kg/s and 30→35°C; afterward, 50 kg/s and 30→40°C. Both stabilized states carry 2.09 MW.
- 40°C is the **return**, not a replacement reading for the 30°C inlet. Nonzero flow also rules out a completely disconnected water branch.
- Heat balance: 100 × 4.18 × 5 = 50 × 4.18 × 10 = 2,090 kW. During the intervening temperature rise, heat can accumulate; the displayed balances are stabilized points.
- Lower flow is measured; its cause is not established. A normal plant temperature alone does not identify a valve, pump or local cooling fault.

## Control layers and Google’s AI cooling — Chapter 14, slides 4–7

- Local controllers regulate pumps; plant controls stage equipment; the scheduler admits computing work.
- Google’s **2016** AI advised operators. The **2018** system directly controlled cooling under operator supervision, with an override available.
- The original Google diagram shows prediction and action selection followed by independent local checks. Five minutes is the supervisory cadence, not protective response time.
- On slide 7, existing work produces 4 MW; a new job adds 2 MW. Cooling is 5 MW now and 7 MW after a three-minute startup. Point at the shaded 1 MW deficit if the job starts early, then compare delaying the job.
- The three-minute startup is illustrative. No thermal-buffer allowance is supplied; it does not establish a safe overrun period.

Source: [Google DeepMind, August 2018](https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/).

## Demand response at The Dalles — Chapter 14, slides 8–10

- Establish the grid request first: a 2023 day-ahead pilot with Northern Wasco County PUD.
- Background video processing and translation updates can wait; live user services still operate. These are the operator’s examples, not a claim about pausing arbitrary LLM inference.
- Then use the separate numerical example: a checkpointable 4 MW job needs three running hours above a 20 MW base load. It pauses 14:00–16:00 and finishes at 18:00, ahead of a 20:00 deadline.
- Both job traces use 12 MWh. Demand during the grid event falls from 24 to 20 MW. The diagram assumes no restart penalty and enough later capacity.

Source: [Google Cloud, October 2023](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption).

## Shared maintenance dependency — Chapter 14, slide 11

- Three 3 MW units serve a 5 MW duty; C is under maintenance. A and B can carry 6 MW.
- Toggle the isolation boundary: removing a shared 24 V control supply also disables A and B. Their main electrical feeds need not have failed.
- Keep this here: the commissioning chapter tests the built system; this example shows how maintenance changes the operating topology. More equipment does not eliminate a shared dependency.

## Cloudflare’s failure, correction and retest — Chapter 14, slides 12–15

- November 2023: Portland facility power loss. Dashboard, API and analytics failed; most distributed edge traffic continued.
- High-availability services spanned sites but depended on Kafka/ClickHouse located only at PDX-04. Tests had removed its HA portion, not the entire facility.
- Code Orange expanded capacity and changed failover. The February 2024 whole-facility test exposed another gap that the team subsequently fixed.
- March 26: power lost at 14:58 UTC; APIs/dashboard normal by 15:05 automatically. Analytics recovered later. Seven minutes is this service endpoint, not cold-start time for the facility.

Sources: [November 2023 report](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/), [April 2024 follow-up](https://blog.cloudflare.com/major-data-center-power-failure-again-cloudflare-code-orange-tested/).

## Gmail, London and Llama 3 — Chapter 14, slides 16–20

- **Gmail:** a storage-software bug affected multiple live copies. Offline tape retained an earlier valid state. The story does not involve fixing A and then being reinfected by B.
- **London:** extreme heat and simultaneous redundant-cooling failures forced shutdown of part of one zone. The first London slide establishes the physical event before the recovery timeline.
- The final report gives cooling repair at July 19 14:13 PDT and initial service restoration at July 20 04:28: another 14 h 15 min. Restart sequencing and service-state reconciliation take time; residual issues lasted longer.
- **Llama 3:** 466 interruptions in 54 days, including 47 planned and 419 unexpected. More than 90% effective training time measures useful training against elapsed time, not facility availability.
- The next slide is Meta’s original fleet-maintenance diagram: the purple group leaves service for upgrades and then returns; the maintenance group rotates. It is not an exact layout of the Llama training run. Group size trades spare-capacity cost against interruption frequency.

Sources: [Gmail incident](https://gmail.googleblog.com/2011/02/gmail-back-soon-for-everyone.html), [Google Cloud final report](https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2), [Llama 3 §3.3.4](https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4), [Meta maintenance trains](https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/).

## Knowledge check — Chapter 14, slide 21

- Return to Row B. All heat enters water: 2.09 MW now, plus a proposed 0.70 MW job. Current flow is 50 kg/s, inlet 30°C, return limit 40°C.
- Ask for the total flow needed: 2,790 ÷ (4.18 × 10) = 66.746 kg/s, roughly 67 kg/s. Keep the temperature limit by establishing that flow, freeing 0.70 MW of existing duty, or deferring the new job.
- At unchanged flow, the new duty would require a 43.35°C return. The calculation does not identify why the original flow fell; that diagnosis is still separate.

## Spare site power cannot finish an acceptance test — Chapter 15, slide 2

“The site can receive 100 megawatts, but only 520 rack paths are accepted. At the stated rack duty, computing uses 52 megawatts. Shared network and storage add five. Facility overhead adds another 16.4, taking site input to 73.4 megawatts. The unused 26.6 megawatts cannot complete an acceptance test.”

The two five-megawatt terms belong in different places: shared network and storage are IT; fixed facility overhead is outside IT. The reader retains the full power formula and conversions. These are illustrative operating points, not measured demand or Abilene data.

## Removing one limit reveals the next — Chapter 15, slides 3–4

“First finish more accepted paths. Cooling then limits us to 550 racks. Improve cooling and networking becomes the limit at 600. Improve networking and electrical capacity and cooling tie at 650. Improving only the electrical side of that tie leaves the same cooling limit.”

Ask learners to predict the next limiting bar before each change. These populations are assumed to cover the same nested rack positions. If different systems serve different rack identities, use the intersection method from commissioning. Slide 5 then separates feasible racks from useful work: waiting for data can reduce progress without changing the powered-rack count.

## Who pays for each part of the service? — Chapter 15, slides 6–7

“This is a separate comparison of the same facilities service for three years. Owning it means paying up front, paying annual operating and energy costs, and recovering a residual value at the end. The contract bundles that service and energy into its annual fee. We exclude the identical compute hardware from both options.”

The starting energy price is $80 per megawatt-hour: 50,000 megawatt-hours costs $4 million annually. Change the price and follow the ownership energy bill. The stipulated contract fee remains fixed with energy included. The selected price carries into the timeline and cost-per-result comparison; real pass-throughs and escalation would need their own terms.

## Pay now, pay each year, recover value at the end — Chapter 15, slide 8

Point to the payment dates before comparing totals. “The owner pays twenty million now, pays operations each year and recovers five million at the end. The contract has three annual payments. Discounting expresses later money at the same starting date; it does not change when the payment occurs.”

The selected energy price and discount rate continue through the cost example. At the base $80/MWh and 8 percent, present costs are $34.07 million for ownership and $28.35 million for the contract. At zero discount they are $36 million and $33 million. These are base-case reference values, so do not read them aloud after changing the energy price. Keep the discount-factor derivation in the reader.

## Less accepted output makes the same bill more expensive — Chapter 15, slide 9

“Keep the facilities cost fixed and remove two of the ten blocks of accepted work. Each remaining result now carries a larger share of the bill. Twenty percent less output makes cost per result twenty-five percent higher.”

The cost numerator uses the chosen energy price and discount rate. The denominator is accepted physical results over the same three years, with the same quality requirement for both alternatives. The physical results are not discounted. This comparison does not identify the cause of the lost work.

## Which upgrade buys more extra results per dollar? — Chapter 15, slides 10–11

“Both proposed upgrades have a supplied route to additional accepted work. The network improvement is smaller each hour, but arrives immediately. Cooling adds more each hour once it arrives. Which gives us more extra results per dollar within these three years?”

Ask for a prediction before revealing the result. With cooling arriving after one year, network costs about $2.08 per extra result and cooling costs $2.50. Move cooling to immediate delivery, ask again, then reveal: cooling falls to about $1.67 and wins this screen. Changing the date requires a new prediction; the earlier answer does not carry forward. At half demand both unit costs double, while their ranking stays the same.

This separate intervention brief compares initial capital with incremental accepted output. It excludes ongoing costs, residuals and discounting; do not mix it with the preceding ownership calculation. The [reader](index.html#d15-upgrade-and-evidence) retains the full arithmetic and the conditions for reconsidering the decision.

## Keep Abilene’s dates and projects together — Chapter 15, slides 12–14

“Oracle says seventy-five percent of total capacity was delivered as of September 2026. The photograph shows the physical campus, but it does not define that percentage or tell us the operating IT load. Crusoe’s earlier 1.2-gigawatt campus plan, its first-two-buildings energization report and its early-workloads report describe different states of the same development. We cannot add them together.”

The aerial is captioned July 15, 2026. Crusoe’s June 9, 2026 account separately identifies a 900 MW Microsoft campus nearby. Its two-operational and six-under-construction counts refer to the original Oracle campus at that June date; they are not a current inventory. Oracle’s later percentage cannot be transferred to the Microsoft project.

Sources checked September 16, 2026: [Oracle Abilene account and aerial](https://www.oracle.com/data-centers/), [Crusoe’s March 2025 campus plan](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts), [September 2025 live-campus account](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live), [June 2026 project distinction](https://www.crusoe.ai/resources/newsroom/crusoes-contracted-ai-infrastructure-capacity-approaches-5-gigawatts-across-data-centers-and-cloud).

## Which facts belong, and what must be measured? — Chapter 15, slide 15

First classify the supported claims: planned campus power, reported energized buildings, reported early workloads and a delivered-capacity percentage. Then ask what is missing for the forecast.

“We need the delivery denominator and electrical boundary, the accepted service paths and configuration, measured IT demand and accepted workload results over the same period, and the corresponding costs and obligations. The sources leave those quantities unresolved. Our teaching prices and workload rates cannot fill Abilene’s missing cells.”

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
