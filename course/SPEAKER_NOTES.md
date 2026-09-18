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

## Cold plates and rear-door heat capture — Chapter 11, slides 3–4

Follow CDU → supply manifold → tray quick disconnects → cold plates → return manifold. This is technology coolant on the rack side of a liquid-to-liquid CDU. Facility water stays across the exchanger. Slide 3 combines the supplied cold-plate assemblies and coolant route. Slide 4 places the NVIDIA rear-manifold view beside the separate RDHX mechanism. The NVIDIA manifold is not itself a rear-door exhaust coil.

A liquid-cooled rack can still put heat into its exhaust air. An RDHX captures that residual air heat into liquid; room-air handlers are another arrangement. [Lenovo’s GB300 guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai#cooling) specifies hybrid liquid/air heat capture. The supplied Abilene sources do not establish that every residual heat path at the campus uses the same equipment.

## Immersion — Chapter 11, slides 5–6

The supplied 2CRSi diagram is single-phase: the dielectric liquid stays liquid as it circulates through the exchanger. Two-phase immersion boils fluid at the hardware and condenses the vapor so liquid returns. The following supplied photograph shows actual immersion hardware; its operator and fluid were not supplied.

## Heat flux and thermal resistance — Chapter 11, slides 7–8

Heat flux is heat-transfer rate per unit area. Both devices generate 400 W; spread over 4 cm² that is 100 W/cm², while 1 cm² produces 400 W/cm². This compares the concentration of heat, not the total heat duty.

Thermal resistance is the temperature difference required per watt along a specified heat-transfer path. Here it covers the chip-to-local-coolant path, in °C/W. The chip is warmer than the coolant: ΔT = T_chip − T_coolant = 400 W × thermal resistance. At 0.08°C/W the gap is 32°C and the chip reaches 67°C; at 0.12°C/W it is 48°C and the chip reaches 83°C. Both coolant temperatures are 35°C. This is a spatial temperature difference, not a time-dependent temperature decrease.

Smaller area can make heat removal harder, but heat flux alone does not establish thermal resistance or chip temperature. The two resistance values are independent stipulated examples. Model: `deviceTemperature` in [cooling-capture-model.js](prototypes/cooling-capture-model.js).

## Coolant flow and the pump curve — Chapter 11, slides 9–10

The steady-flow sensible heat balance relates carried heat to mass flow, heat capacity and supply-to-return temperature rise. Doubling flow halves that rise at fixed heat duty.

The descending curve shows the pressure difference the pump can add at each flow, at fixed rotational speed. The two ascending curves show the pressure difference needed to circulate water through the normal circuit and through the same circuit with greater resistance. Actual steady flow is where the pump curve meets the applicable circuit curve: 2 L/s and 120 kPa for the normal circuit, or approximately 1.41 L/s and 140 kPa with higher resistance.

Below an intersection the pump has more pressure available than that circuit requires, so flow increases. Above it the circuit needs more pressure than the pump provides, so flow decreases. The curves are Δp_pump = 160 − 10q², Δp_normal = 30q² and Δp_higher-resistance = 70q², with q in L/s and Δp in kPa. Equating pump and circuit pressure differences gives q = 2 L/s for the normal circuit and q = √2 ≈ 1.41 L/s for the higher-resistance circuit. They illustrate a complete closed circulation path; they are not absolute pressure readings or a named CDU's rating.

More restriction reduces flow on the same fixed-speed pump: the operating point moves left and upward along its curve. At a given flow the higher-resistance circuit needs more pressure difference. More flow through either unchanged circuit also requires a larger pressure difference, even though the pump curve slopes downward. Keep the slide's visible labels sparse; use these notes for the equations and explanation. Chapter 13 illustrates the plumbing requirement with the approximate quadratic relation. Source: [KSB characteristic curves](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/characteristic-curve-1117926).

## CDU approach compares two supply temperatures — Chapter 11, slide 11

Facility water arrives at 30°C; separate coolant leaves for the chips at 35°C. Their difference is a 5°C approach. A smaller approach brings the technology coolant closer to the facility-water temperature. This differs from one fluid's supply-to-return rise. Achieving a smaller approach at a given heat duty depends on exchanger size, flow and operating conditions.

A temperature difference of 5°C equals 5 K. Source: [NIST SI temperature units](https://www.nist.gov/pml/special-publication-330/sp-330-section-2).

## CoolIT CHx2000 — Chapter 11, slide 12

The manufacturer separately lists 2 MW at 5°C approach and 2,125 L/min at 35 psi. These are separately specified thermal and hydraulic points. The CHx2000 is a liquid-to-liquid CDU with pumps and a heat exchanger, not a refrigeration compressor. Source: [CoolIT CHx2000](https://www.coolitsystems.com/cdu-product/chx2000/).

## Cooling redundancy and response — Chapter 11, slides 13–16

Distinguish spare CDU capacity from an independently supplied coolant path. The A/B example initially has both paths available. Losing a path reveals which racks retain cooling.

The derating example starts with 1,000 kW entering coolant; two CDU failures leave 600 kW of cooling. Reducing the load to 500 kW leaves 100 kW margin. The following merged commissioning example tests that response: command the affected racks, then measure actual power, flow and temperature. Its trace is qualitative and does not establish a safe response time. Liquid heat is not automatically identical to the commanded electrical power cap.

## Retrofit and residual air heat — Chapter 11, slide 17

The cold plates collect 85 kW of a 100 kW rack's heat; 15 kW remains in air. That heat can use 15 kW of a 20 kW room-air allowance, or be captured by a suitable RDHX and sent into liquid. Only air heat escaping the rear door contributes to the room's remaining duty. The diagram assumes the door captures the illustrated 15 kW.

## At Abilene, the heat goes to outdoor air — Chapter 12, slide 2

Follow the heat from rack coolant through separate facility water and outdoor equipment. Crusoe describes non-evaporative heat rejection; circulating water is not itself consumed to carry away the heat. Initial fill and maintenance still need water. The later numerical examples are separate teaching cases.

Source: [Crusoe’s August 5, 2025 Abilene account](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center).

## Wet and dry equipment; tower water balance — Chapter 12, slides 3–4

In an open wet tower, nozzles or a distribution deck spread water over fill. Air contacts films or droplets; some water evaporates and cooled water collects in a basin. It is not vapor escaping through holes in a closed pipe. [DOE component guide](https://www.energy.gov/sites/default/files/2013/10/f3/waterfs_coolingtowers.pdf), pages 1–3.

Evaporation leaves dissolved minerals behind. Blowdown removes some concentrated water; makeup replaces evaporation and discharge. Makeup describes the water's purpose, not a specific source or treatment quality. [DOE cooling-tower management](https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management).

## Wet bulb and dry bulb — Chapter 12, slides 5–6

These are two measurements of the same air. Dry bulb is the ordinary air temperature. A wetted, ventilated sensor cools by evaporation; wet bulb is lower in unsaturated air and equal at saturation. The definition slide uses original teaching wording. [NWS definitions](https://www.weather.gov/source/zhu/ZHU_Training_Page/definitions/dry_wet_bulb_definition/dry_wet_bulb.html).

Humidity changes wet bulb even when dry bulb stays fixed. Equipment names and air measurements are separate: dry coolers follow dry bulb; evaporative towers can approach wet bulb.

## Follow the outdoor coolant paths — Chapter 12, slides 7 and 9

Step through collection, transfer, rejection and return on each physical diagram. The separate CDU loops remain distinct. The dry coil transfers heat through its wall to outdoor air; the wet tower exposes tower water to moving air. Each heat-transfer interface needs a temperature difference. On the dry route, 35°C outdoor air plus a 5°C dry-cooler approach yields 40°C facility water; the 5°C CDU approach yields 45°C rack coolant. The example assumes a maximum rack-coolant inlet of 35°C, not a 35°C chip temperature. These values illustrate the interfaces rather than a particular site's performance.

## Adiabatic assist — Chapter 12, slide 8

Wetted pads or spray cool incoming air by evaporation before it crosses a sealed process-fluid coil. That distinguishes the illustrated adiabatic cooler from an open tower, where tower water directly contacts air. The assist consumes water even though the process loop is closed.

## Closed-loop water — Chapter 12, slide 10

This continues the preceding wet-tower example, with that route initially selected. A separating exchanger keeps facility water closed while tower water contacts outdoor air and evaporates. Switch to the dry cooler to revisit the preceding sealed-coil route. Neither diagram here includes refrigeration; the next slide introduces the chiller. Direct open tower water can serve other qualified heat-exchanger arrangements; water quality and the actual equipment interfaces determine suitability.

## Chiller, economizer and COP — Chapter 12, slides 11–13

The compressor adds energy to the heat being moved. Ten megawatts collected plus two megawatts of compressor electricity becomes twelve megawatts outdoors. Pumps and fans are outside this particular compressor balance. It does not mean that direct outdoor cooling must remove less than 10 MW: when weather and equipment capacity permit, it can remove the entire load without a compressor.

The supplied economizer image follows immediately. It summarizes a functional heat path; “from racks” and “back to racks” do not mean every water circuit is shared. The COP slide then relates heat moved to cooling electricity. Keep the equipment boundary consistent when comparing COP values.

## Hot weather needs more cooling electricity — Chapter 12, slide 14

At 8 MW computing, the example's COP 8 in cool weather means 1 MW cooling electricity; COP 4 in hot weather means 2 MW. With 0.4 MW other demand, total draw rises from 9.4 to 10.4 MW against a 10 MW site limit. The controls illustrate that electricity constraint independently of heat-removal capacity. COP values are example operating points, not a universal cold/hot rule.

## Heat reuse — Chapter 12, slide 15

The heat-reuse chart keeps the data center at 4 MW all day. A neighboring factory needs 2 MW for six hours or is closed that day. It is the heat customer's demand that changes, not the data center's operating hours. Remaining heat still needs another rejection path.

## Operating dependencies — Chapter 12, slide 16

Dry, non-evaporative rejection needs electricity. A wet cooling tower needs electricity and ongoing water. Initial fill is outside this comparison.

## EPC and the late rack change — Chapter 13, slides 1–6

EPC means engineering, procurement and construction. The opening connects those responsibilities to electrical plant; commissioning is not the C in EPC. The rack-change case follows the opening directly.

A 20 MW IT phase changes from 200 racks at 100 kW to 100 racks at 200 kW. Electrical, hydraulic and support consequences follow together. At balanced 480 V three-phase, PF 1, a branch rises from about 120 A to 241 A against its existing 160 A continuous limit.

At a 10°C water rise, rack flow doubles from 2.39 to 4.78 kg/s. The unchanged branch's stipulated quadratic pressure-flow relation requires 80 rather than 20 kPa differential. These are inlet-to-outlet differences at two flows, not pressure readings at the CDU and rack. The separate support example stipulates twice the mass on the same four feet; power alone does not determine mass.

## Prefabrication at different scales — Chapter 13, slides 7–9

The supplied full-page image shows factory and site work proceeding in parallel. Houdini then introduces analyst-reported AWS data-hall skids and Cupertino Electric participation. The photograph is CEI's Edgerton factory; its pictured equipment is not identified as a Houdini unit.

Siemens–Compass uses a jointly developed skid combining 8DJH 36 switchgear and a transformer. The photograph shows the switchgear portion. These examples establish the assembled scope without assigning a universal schedule saving.

## Open Compute Project — Chapter 13, slides 10–11

OCP publishes shared equipment interfaces. UQD-compliant couplings of the same specified interface can mate; that alone does not establish sufficient flow for the new rack. The example needs 4.8 kg/s against an existing 3.0 kg/s branch limit. The following user-supplied Open Rack image compares server-level PSUs with consolidated rack-level PSUs; it is not identified as a GB300 product.

Sources: [ORv3 revision 1.0](https://www.opencompute.org/documents/open-rack-base-specification-version-3-pdf), mechanical and busbar sections; [UQD revision 1.0](https://www.opencompute.org/documents/ocp-universal-quick-disconnect-uqd-specification-rev-1-0-2-pdf), printed pages 4–10.

## Factory and site acceptance — Chapter 13, slide 12

Factory tests cover internal wiring, piping and controller logic before shipment. Site tests cover field connections and real installed equipment response. The three-row table shows how prefabrication shifts troubleshooting earlier while leaving necessary site checks. The merged cooling-failure example now follows Chapter 11's cooling derating.

## Which racks are ready? — Chapter 13, slide 13

Electrical readiness covers A01–A80, cooling A21–A100 and networking A01–A60. Their intersection is A21–A60: 40 racks, or 8 MW at 200 kW per rack. Extending cooling to A01 yields 60 racks and 12 MW. This isolates shared coverage while assuming the remaining acceptance criteria are met. The repeated closing matching quiz is removed.

## Connect the next phase beside live service — Chapter 13, slide 14

Return to the earlier Polaris Forge 1 photographs and dates. Applied Digital reported 50 MW ready for service for CoreWeave on October 27, 2025, and a further 50 MW on November 24. Phased delivery means the next connection must preserve the infrastructure serving the first phase. The public milestones do not identify a particular shared topology or claim that a fault occurred.

Sources: [first 50 MW](https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at), [second 50 MW](https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at).

## Diagnose Row B — Chapter 14, slides 1–3

- Start with the hottest measured chip at 85°C, above the scenario’s stipulated 80°C operating limit, despite a normal upstream 30°C supply reading.
- Compare complete, time-aligned measurements at the row: before, 100 kg/s and 30→35°C water, with the hottest chip at 70°C; afterward, 50 kg/s and 30→40°C water, with the hottest chip at 85°C. Both stabilized states carry 2.09 MW. These chip readings and the 80°C limit are scenario inputs, not a named GPU’s rating or temperatures derived from the water balance.
- 40°C is the **return**, not a replacement reading for the 30°C inlet. Nonzero flow also rules out a completely disconnected water branch.
- Heat balance: 100 × 4.18 × 5 = 50 × 4.18 × 10 = 2,090 kW. Immediately after flow falls, an unchanged 5°C water rise would remove only 50 × 4.18 × 5 = 1,045 kW. Heat initially accumulates; the later 10°C rise restores the full 2.09 MW balance.
- The later balance removes all the heat at an unacceptable measured chip temperature. Halving flow alone would not establish failure; the 85°C chip reading against the 80°C limit does. Lower flow can increase cold-plate thermal resistance and coolant warming, requiring hotter chips to transfer the same heat. The water balance alone does not calculate chip temperature. See [CoolIT’s cold-plate thermal-resistance versus flow graph](https://www.coolitsystems.com/wp-content/uploads/2024/05/Split-Flow-Technology-CoolIT-Tech-Brief.pdf).
- Slide 3 now shows the transition explicitly: heat removal briefly falls below generation, stored heat increases, and the chip warms until heat removal catches up. At the later balance the temperature stops rising; it has not returned to a safe value. The larger chip-to-coolant temperature difference drives the required heat through the less effective cooling path. The drawn time course is qualitative: no elapsed seconds or thermal mass is specified, and it does not calculate the 85°C endpoint.
- The chip-to-coolant temperature difference is distinct from the water inlet-to-return rise. The 30°C inlet is maintained by upstream cooling; return water rises from 35°C to 40°C. At the later equilibrium, heat removal again matches generation per second. During the transition some energy remains stored in the warmer equipment; this is not the same energy removed over a longer time.
- Lower flow is measured; its cause is not established. A normal plant temperature alone does not identify a valve, pump or local cooling fault.

## Google’s AI cooling and control layers — Chapter 14, slides 4–9

- Show Google’s cooling context, control flow and performance on slides 4–6. Then use the three-control-layer image on slide 7 to organize the example then highlight plant controls on slide 8 before workload admission on slide 9.
- Local controllers regulate pumps; plant controls stage equipment; the scheduler admits computing work.
- Google’s **2016** AI advised operators. The **2018** system directly controlled cooling under operator supervision, with an override available.
- Slide 5 keeps all four original Google diagrams together: read sensors → predict outcomes → select an action within constraints → verify locally and act. Five minutes is the supervisory cadence, not protective response time.
- Slide 6 preserves the supplied original performance GIF. Cooling energy per unit of cooling improved from about 12% to about 30% below the historical pre-AI baseline over nine months. The plot tracks trailing twelve-month performance and training examples; it does not claim a 30% reduction in total facility electricity.
- On slide 9, existing work produces 4 MW; a new job adds 2 MW. Cooling is 5 MW now and 7 MW after a three-minute startup. Point at the shaded 1 MW deficit if the job starts early, then compare delaying the job.
- The three-minute startup is illustrative. No thermal-buffer allowance is supplied; it does not establish a safe overrun period.

Source: [Google DeepMind, August 2018](https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/).

## Cooling reserve and staging — Chapter 14, slides 10–11

- The preceding 1 MW spare capacity is an illustrative choice, not a universal margin. Capacity reserve (MW), redundancy after an equipment failure and thermal storage (energy, with a finite duration) answer different questions.
- Johnson Controls’ Metasys sequence uses an 80% stage-up threshold for all-positive-displacement stages and 90% when constant-speed centrifugal chillers govern the stated condition. Variable-speed centrifugal thresholds vary with operating lift. Time, trend and failsafe conditions also apply; the graph shows thresholds, not an assured 10–20% reserve or a rule for every data center.
- Intel’s historical case used two 24,000-US-gallon tanks at 42°F (5.6°C). The twelve-minute design interval comes from five minutes of full-load UPS runtime plus seven extra minutes of cooling. In the actual late-2006 event, lightly loaded servers ran over fifteen minutes and the tanks maintained cooling, then absorbed residual heat. Backed-up pumps and fans made the stored cooling usable.
- Spare capacity after restart also permits removal of heat accumulated during an interruption. A site chooses its operating margin around credible load changes, starting time, equipment performance at the current weather, local delivery limits and required failure tolerance.

Sources: [Johnson Controls staging threshold](https://docs.johnsoncontrols.com/bas/r/Metasys/en-US/Chilled-Water-Plant-for-Guideline-36-Application-Note/1.0/Chiller-sequence-of-operations/Chiller-and-waterside-economizer-staging-determination-5.20.1-15/Stage-Up-Part-Load-Ratio-SPLRUP), [stage-up conditions](https://docs.johnsoncontrols.com/bas/r/Metasys/en-US/Chilled-Water-Plant-for-Guideline-36-Application-Note/1.0/Chiller-sequence-of-operations/Chiller-and-waterside-economizer-staging-determination-5.20.1-15/Stage-up-efficiency-condition), [Intel IT thermal storage](https://www.intel.com/content/dam/doc/white-paper/intel-it-thermal-storage-system-provides-emergency-data-center-cooling-paper.pdf), [Schneider reserve-cooling guidance](https://blog.se.com/datacenter/2013/02/11/4-tips-for-keeping-your-it-equipment-cool-during-when-the-power-goes-out/).

## Demand response at The Dalles — Chapter 14, slides 12–14

- Establish the grid request first: a 2023 day-ahead pilot with Northern Wasco County PUD.
- YouTube video processing and Google Translate updates can wait; Search, Maps and video playback still operate. These are the operator’s examples, not a claim about pausing arbitrary LLM inference.
- Slide 13 restores the large “Keep serving” and “Defer eligible background work” panels. Slide 14 separately shows both scheduling graphs. Its 20 MW base load and checkpointable 4 MW job are explicitly illustrative, not Google measurements. The job needs three running hours; pausing 14:00–16:00 moves completion from 16:00 to 18:00, ahead of a 20:00 deadline.
- Both job traces use 12 MWh. Demand during the grid event falls from 24 to 20 MW. The diagram assumes no restart penalty and enough later capacity.

Source: [Google Cloud, October 2023](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption).

## Cloudflare’s failure, correction and retest — Chapter 14, slides 15–17

- Slide 15 combines the outage date and Core services card with the three-site dependency diagram, identifying the single point of failure.
- November 2023: Portland facility power loss. Dashboard, API and analytics failed. Focus on the affected services.
- High-availability services spanned sites but depended on Kafka/ClickHouse located only at PDX-04. Tests had removed its HA portion, not the entire facility.
- Code Orange expanded capacity and changed failover. The February 2024 whole-facility test exposed another gap that the team subsequently fixed.
- March 26: power lost at 14:58 UTC; APIs/dashboard normal by 15:05 automatically. Analytics recovered later. Seven minutes is this service endpoint, not cold-start time for the facility.

Sources: [November 2023 report](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/), [April 2024 follow-up](https://blog.cloudflare.com/major-data-center-power-failure-again-cloudflare-code-orange-tested/).

## London and Llama 3 — Chapter 14, slides 18–22

- Slide 18 presents the author-supplied verbatim Root Cause quote from Google’s July 29, 2022 final report before the incident mechanism on slide 19.
- **London:** extreme heat and simultaneous redundant-cooling failures forced shutdown of part of one zone. The first London slide establishes the physical event before the recovery timeline.
- The final report gives cooling repair at July 19 14:13 PDT and initial service restoration at July 20 04:28: another 14 h 15 min. Restart sequencing and service-state reconciliation take time; residual issues lasted longer.
- **Llama 3:** 466 interruptions in 54 days, including 47 planned and 419 unexpected. More than 90% effective training time measures useful training against elapsed time, not facility availability.
- The next slide pairs Meta’s original maintenance-train diagram with the supplied maintenance-cost graph. Smaller domains mean more training interruptions; larger domains take more compute capacity out of service. The U-shaped graph illustrates that trade-off without a numerical optimum.

Sources: [Google Cloud final report](https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2), [Llama 3 §3.3.4](https://arxiv.org/html/2407.21783v3#S3.SS3.SSS4), [Meta maintenance trains](https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/).

## Knowledge check — Chapter 14, slide 23

- This is a new, healthy Row C, not the earlier faulty Row B. It transfers 2.09 MW into water at 100 kg/s, 30°C supply and 35°C return; chips are operating within their limits.
- A new workload adds 2.50 MW to the same water branch. Electrical capacity and the cooling plant each have 3 MW spare. The decision concerns whether that spare capacity can serve this row at its current flow.
- The row return limit is 40°C. Remaining water-side capacity is 100 × 4.18 × (40 − 35) ÷ 1,000 = 2.09 MW. **Not at the current row flow:** the proposed addition exceeds this local headroom even though the site has enough spare power and cooling.
- Total heat would be 4.59 MW. At 30°C supply and a 40°C maximum return, the water-balance requirement is 4,590 ÷ (4.18 × 10) = 109.81 kg/s, rounded up to 110 kg/s. At the unchanged 100 kg/s the return would instead be 40.98°C.
- The operating decision is to establish sufficient row flow or assign some workload elsewhere. The calculated flow is not proof that the installed pump, piping or cold plates support it; verify the operating range and chip temperatures during a staged load increase. All proposed load heat is assumed to enter this measured water branch.

## GPU cloud economics — Chapter 15

- **Opening meme:** The supplied hardware-price meme opens the chapter. It concerns component purchase prices, not GPU rental rates.
- **Products and responsibilities:** Start the commercial explanation with CoreWeave's committed-revenue share. Separate the provider's capacity invoice from a lab's internal cost per token or training run. Bare metal describes dedicated physical hardware without a hypervisor. The customer or provider can operate software on that hardware: CoreWeave explicitly runs Kubernetes on bare metal. The removed internal-cost line meant a lab's own cost accounting, which can include its allocated GPU bill and other costs; it did not mean only salaries or only costs outside the cloud invoice.
- **Rental terms and prices:** Define cloud Spot as spare capacity rented at the current price, subject to reclamation; AWS changes its prices gradually, not on every instantaneous market movement. Walk through one-, three- and five-year commitments. The H100 ranges retain their historical dates on the chart; use them to show renewal exposure.
- **Billable occupancy:** Compare full-fleet commitment with the uncommitted rental pool. $2.50 / $4.00 = 62.5% rented hours gives equal revenue before costs. Rented hours and GPU compute utilization are different quantities.
- **Financing:** Customer payments support the provider's debt service; lenders fund hardware. Delivery, credit and operating risks remain with the contract parties.
- **NVIDIA backstops:** Three slides follow financing: CoreWeave’s September 2025 $6.3 billion initial agreement; the typical six-year support described in NVIDIA’s July 2026 filing; and the exposure from unused capacity. Keep CoreWeave’s specific agreement distinct from the later program structure. The $36 billion is a dated aggregate commitment, not a loss. The backing concerns contracted cloud capacity, not an unconditional guarantee of each operator’s debts. SemiAnalysis’s September article motivates the revenue-floor / shared-upside tradeoff; official filings confirm the purchase commitments and risks.
- **Electricity:** Unrented GPUs can remain powered. Idle power depends on the hardware and operating policy; it is not universally zero or equal to busy power. In this example the average site allocation is 1 kW while rented and 0.2 kW while idle. Over 100 hours: 80 × 1 + 20 × 0.2 = 84 kWh. All 84 kWh must be covered by 80 rented hours, giving 1.05 kWh per billed hour. At $80/MWh this costs $0.084 per rented GPU-hour; at $160/MWh it costs $0.168. Rented does not mean continuously computing at maximum power. Under a fixed all-in fee the provider bears an unhedged energy-price change; reimbursement transfers the specified expense to the customer. Hardware, facilities and operations remain in the cost base. NVIDIA's [idle-system power model](https://docs.nvidia.com/datacenter/dps/versions/latest/guides/reference/apis/v1/devices.html) supports nonzero idle consumption; the course's assumed powers are not device specifications.
- **Abilene:** Crusoe builds the facility, Oracle supplies cloud capacity, OpenAI runs workloads. Compare the original two-building energization target with the later report, then the expansion construction target with Oracle's delivered-capacity report. Different milestones do not establish an exact schedule slip; that distinction stays in the notes rather than a slide subtitle.

## Putting an AI Factory Together — Chapter 16

1. **Abilene.** Return to the original Oracle/OpenAI campus. The aerial is dated July 2026. Follow one physical site through the decisions that shaped it; keep the neighboring Microsoft development separate.
2. **The workload.** OpenAI’s early training and inference ran on Oracle infrastructure. Show how the actual cluster creates electrical, cooling and fabric requirements. The Oracle media-kit image documents the hall; equipment models are established by the separate deployment announcement, not read off the photograph.
3. **Bridge power and backup.** Toggle the gas plant’s role. Earlier power can change the start of service; later the equipment can protect continuity. Fuel supply, controls, emissions equipment and maintenance remain part of that choice. The stated gas rating does not establish backup coverage for the full campus.
4. **Heat and water.** Trace rack-side heat into the facility loop and out through air-cooled chillers. The refrigerant transports heat across the chiller; water and refrigerant do not mix. Condenser fans and the compressor need power. The public description does not establish which residual-air device appears in every hall.
5. **A hot afternoon.** Both sides show the same installed racks and the same IT load. At a fixed cooling duty and coolant target, higher outdoor dry-bulb generally requires higher refrigerant condensing temperature and pressure, increasing compressor work. The bars show direction, not measured proportions. If the plant or electrical limit is reached, the sustainable IT load can fall while hardware inventory stays unchanged. We do not assign Abilene a made-up derating curve.
6. **Parallel construction.** Manufacturing and site works converge at installation and testing. Equipment interfaces, delivery access and later replacement access still shape the project. Do not treat the sketch as an identified installed skid model or a measured schedule saving.
7. **Capital.** Distinguish physical-facility funding from a GPU purchase and from the tenant’s cloud invoice. The venture announcement and initial long-term lease connect customer demand to construction finance. They do not disclose the campus’s revenue, profit or exact customer rates.
8. **Live expansion.** Early workloads and further construction coexisted. Carry the operating phase’s power, cooling and network boundaries into a new connection. The graphic expresses the design problem, not a disclosed switching procedure or topology. The old rack-matching exercise is no longer presented.
9. **From Watts to Tokens.** Trace each path on the same diagram. Electricity feeds the racks and cooling equipment. Information crosses the GPU fabric into training or inference. Heat leaves through the cooling plant, together with its electrical input. The campus’s MW rating alone cannot establish tokens per second; model, precision, batching and service targets still matter.

Primary claims, dates and asset provenance: [Abilene evidence ledger](../research/abilene-finale-evidence-2026-09-18.md). The five original numerical exercises remain optional reading; their inputs are not Abilene measurements.
