# Selected speaker notes

Use slide titles and links to identify these scenes as numbering changes.

## A three-phase shelf can feed single-phase PSU modules — Chapter 8, slide 6

[Slide](prototypes/rack-energy-format.html?teach=1#psu-input)

“The shelf receives three-phase power, but each PSU module can use a single phase. In this example, there are 480 volts between phases and about 277 volts from each phase to neutral. The shelf spreads those phase-to-neutral connections across its modules.

“Each module converts its AC input to 50-volt DC, and their outputs share the rack bus. So the shelf uses all three phases even though each individual PSU uses only one. Balancing the modules across the phases spreads the input current and smooths their combined power demand. Neutral is separate from protective earth.”

The diagram is the Advanced Energy ORv3 example; it does not establish the PSU wiring of every GB300 rack.

Source: [Advanced Energy ORv3 PSU](https://www.advancedenergy.com/en-us/products/ac-dc-power-supply-units/power-shelves/ocp-compliant/orv3-psu/).

## Should we step down first or rectify first? — Chapter 9, slide 10

[Slide](prototypes/dc-distribution-format.html?teach=1#ac-dc-ledger)

“New higher-voltage SiC devices could make SSTs simpler and more competitive. Their widespread adoption in data centers still has to be demonstrated.”

Source: [Wolfspeed 10 kV SiC announcement](https://www.wolfspeed.com/company/news-events/news/wolfspeed-introduces-industrys-first-commercially-available-10000v-silicon-carbide-power-mosfet/).

## An 800 V DC feeder needs DC-rated protection — Chapter 9, slide 12

[Slide](prototypes/dc-distribution-format.html?teach=1#dc-feeder-protection)

“Both AC and DC circuits need fault protection. With AC, the current naturally crosses zero, helping a breaker extinguish its arc after the contacts open. DC has no periodic natural zero, so the protection must force the current to stop.

“Here, both the rectifier and the charged bus capacitor can feed a short circuit. The cable also stores magnetic energy. The breaker must interrupt that DC fault and withstand the voltage afterward—zero current does not mean zero voltage. Switching off the AC supply alone does not remove the stored energy.”

Source: [ABB DC protection paper](https://library.e.abb.com/public/5cd83dcb95a74dcdb571be5f256e1af8/9AKK108470A9606_en_B_Protection%20Devices%20for%20Direct%20Current%20Applications%20-%20Technical%20Application%20Paper.pdf).

## Microsoft’s ambition for Fairwater — Chapter 10, slide 5

[Slide](prototypes/networking-format.html?teach=1#fairwater-model-scale)

“The distributed networking of Microsoft’s Fairwater sites is designed to enable them to support training models with hundreds of trillions of parameters.”

Microsoft, November 12, 2025. This describes intended capability, not a reported completed training run.

For the dedicated-fiber line: Microsoft describes an AI WAN over dedicated fiber
between its sites. Owning that path helps avoid competition with unrelated
traffic; distance still creates propagation delay. The claim does not establish
that every switch, endpoint and workload is free of bottlenecks.

Source: [Microsoft Fairwater feature](https://news.microsoft.com/source/features/ai/from-wisconsin-to-atlanta-microsoft-connects-datacenters-to-build-its-first-ai-superfactory/).

## Copper for short links; optical fiber for longer runs — Chapter 10, slide 10

[Slide](prototypes/networking-format.html?teach=1#copper-and-light)

“The electronics at each end work with electrical signals. Copper carries that signal along the cable. At high signaling rates, loss and distortion make it harder for the receiver to distinguish the symbols as the cable gets longer. Short passive copper cables keep the connection simple and use very little power.

“With fiber, the transmitting module converts the electrical signal into modulated light. The receiving module detects that light and converts it back into an electrical signal. Both ends do both jobs on a two-way link. These 400G examples span two meters of passive copper, fifty meters of multimode fiber and five hundred meters of single-mode fiber. The cable route and required data rate determine which supported reach you need.”

Source: [NVIDIA LinkX product overview](https://docs.nvidia.com/networking/display/400g100gpam4ovdev/linkx-100g-pam4-product-line-overview), checked September 16, 2026.

## Co-packaged optics shortens the electrical path inside the switch — Chapter 10, slide 11

[Slide](prototypes/networking-format.html?teach=1#optical-packaging)

“Pluggable optics puts conversion at the front panel. CPO moves it beside the switch chip, shortening the electrical path. Both approaches remain in use.”

Sources: [NVIDIA CPO](https://developer.nvidia.com/blog/scaling-ai-factories-with-co-packaged-optics-for-better-power-efficiency/), [Spectrum-6 optical options](https://blogs.nvidia.com/blog/nvidia-spectrum-six-arrives-in-gigascale-ai-factories/).

## Cross-leaf bandwidth is shared by the servers beneath each leaf — Chapter 10, slide 13

[Slide](prototypes/networking-format.html?teach=1#shared-uplinks)

“The full example has sixteen server links, with four servers under each leaf. Here we zoom in on one leaf. Its four 400-gigabit server ports can offer 1,600 gigabits per second, but two 400-gigabit uplinks can carry only 800 toward the other leaves. If all four servers send across that boundary at once, their traffic shares the narrower path. That is the two-to-one ratio.

“Four uplinks raise the shared capacity to 1,600 gigabits per second, matching the four server ports. For the same 32 gigabytes crossing this boundary, the ideal transfer time falls from 0.32 to 0.16 seconds. Traffic staying under the same leaf does not use these uplinks. So the benefit depends on where the communicating servers sit and which traffic actually crosses the boundary.”

Model: [`fabricBudget`](prototypes/networking-model.js), four leaves with four 400 Gb/s server links each; two or four 400 Gb/s uplinks per leaf. The displayed transfer assumes balanced traffic in one direction.

## Four fast senders can overwhelm one receiver port — Chapter 10, slide 15

[Slide](prototypes/networking-format.html?teach=1#incast)

“Four senders can offer 1,600 gigabits per second, but the receiving link carries only 400. Packets accumulate in the switch’s output queue because they arrive faster than that link can drain them. Adding spine bandwidth leaves this final 400-gigabit link unchanged.

“To receive faster, the switch port, cable or optics, and receiving network adapter must all support a higher link rate, and the receiving system must be able to absorb the data. Another option is to spread the traffic across additional receiving links or servers, if the workload can use them. Pacing the senders can control the queue, but it does not increase the link’s capacity.”

Source for supported adapter link rates: [NVIDIA ConnectX-7 specifications](https://networking-docs.nvidia.com/connectx7hw/specifications).

## Meta built large AI clusters with both Ethernet and InfiniBand — Chapter 10, slide 16

[Slide](prototypes/networking-format.html?teach=1#ethernet-infiniband)

“RoCE means RDMA over Converged Ethernet. RDMA is Remote Direct Memory Access:
network adapters transfer data into permitted remote memory without the usual
CPU-managed copying path for each transfer.

“Either fabric still needs several choices to work together. Routing chooses the
paths. Congestion control adjusts sending rates when traffic competes. Collective
software organizes exchanges among participating GPUs. Job placement chooses
which servers run together. Those choices determine how effectively a workload
uses the physical network, and feed back into its capacity and topology.”

Sources: [NVIDIA RoCE documentation](https://docs.nvidia.com/networking-ethernet-software/cumulus-linux/Layer-1-and-Switch-Ports/Quality-of-Service/RDMA-over-Converged-Ethernet-RoCE/), [Meta’s 2024 cluster account](https://engineering.fb.com/2024/03/12/data-center-engineering/building-metas-genai-infrastructure/).

## Meta built storage in tiers to keep GPUs supplied — Chapter 10, slide 21

[Slide](prototypes/networking-format.html?teach=1#meta-rsc)

“This is Meta’s Research SuperCluster, described in January 2022. Its storage has three jobs: 175 petabytes of bulk storage, 46 petabytes of cache for repeated reads, and 10 petabytes of shared file storage. The cache keeps copies of data that will be used again. Meta’s AIRStore also prepares a dataset once so several training runs can reuse it, reducing repeated preparation and transfers between regions.

“The network has to carry those prepared inputs from storage to the GPUs fast enough to keep the work moving. That makes storage part of the facility design: more equipment needs rack space, power, cooling and cable routes. Meta says RSC required changes across all of those systems. The GPU racks in the photograph depend on that entire supply path.”

Source: [Meta’s January 24, 2022 RSC account](https://ai.meta.com/blog/ai-rsc/), storage description and AIRStore sections checked September 16, 2026.
