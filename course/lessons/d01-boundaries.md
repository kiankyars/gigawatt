# One rack, three paths

**2. Data center overview**

Locate white and gray space, trace electricity, heat and information, then close a facility energy balance that counts each load once.

**Driving question:** What crosses the boundary of a working data center?

## Start with a place

Imagine standing in front of a rack: a cabinet holding computing equipment and the hardware that supports it. A server is a computer inside that cabinet, a board connects the components inside a server, and a package holds one or more semiconductor dies. Step outward and a row holds several racks, a hall several rows, a building one or more halls, and a campus one or more buildings plus the infrastructure they share. These words name places nested inside places. Power belongs to the equipment installed in them, so each rack, row and hall needs its own number.

Two floor-plan terms locate the systems that support the racks. White space is the area housing information technology (IT) equipment and its immediate support infrastructure. Gray space, also spelled grey space, is the supporting electrical, mechanical and service area outside the IT hall, such as an electrical room or a mechanical gallery. The labels describe the floor, and equipment takes the label of the room it stands in: a power shelf or a coolant distribution unit (CDU) installed with the racks sits in white space. Google’s photograph below, of server aisles in its data center at New Albany, Ohio, shows white space: racks and their cabling line one side of the aisle, with piping and cable trays overhead.

![A Google data hall in New Albany, Ohio: server racks with dense blue and green cabling on the left, gray cabinets and control panels beside them, orange-tagged pipes and cable trays overhead, and yellow safety posts along a long, brightly lit aisle.](../assets/references/overview-google-new-albany-aisles.webp)

White space: server aisles in Google’s data center at New Albany, Ohio. The capture date is not stated. [Google Data Centers, photo gallery](https://www.datacenters.google/discover-more/photo-gallery/)

## Trace three paths through one rack

Now draw three paths through the same picture. Electrical energy arrives through conductors and conversion equipment. Heat leaves through air, liquid and heat-transfer equipment. Information arrives, moves between machines and leaves through communication links. The three arrows mean different things. Coolant circulates around a loop and comes back, while heat crosses an exchanger from one loop into the next. Data can travel both ways along a link, while electrical energy keeps flowing into the equipment. Give each arrow one meaning, and the drawing shows how the parts really connect.

NVIDIA’s GB300 NVL72 gives the lesson a real rack. Its enterprise reference architecture lists a full-rack requirement of up to 142 kilowatts (kW). That is a published ceiling for planning, the most the rack should need, and the facility in this lesson takes it as each rack’s draw at its alternating-current (AC) input.

The same rack shows that the information path has boundaries of its own. A GB300 NVL72 holds 72 Blackwell Ultra graphics processing units (GPUs) in 18 compute trays, and nine NVLink switch trays connect every GPU to every other GPU in the rack, so all 72 can work as one multi-GPU unit. That group is a scale-up domain. A separate scale-out network connects racks to one another, storage traffic travels on a network of its own, and at the campus edge a carrier takes traffic to other sites and users. Each network has its own bandwidth budget and physical reach, so where a job is placed decides which of its exchanges stay on the rack fabric and which cross the cluster.

## Draw the boundary, then close the ledger

A boundary is the imaginary line around the equipment you are accounting for. Draw it tightly around a processor and its voltage regulators may lie outside. Draw it around a rack and those regulators, the fans and the power supplies may all be inside. Draw it around the facility and the cooling pumps and outdoor heat-rejection equipment join the account. Widening the boundary changes which loads you count, while every load keeps drawing exactly what it drew before. So always ask where the meter sits relative to the line.

Now fill in a facility. Ten GB300 racks draw 142 kW each at their AC inputs. Networking and storage equipment outside those racks, on its own meters, draws another 80 kW, and it counts as IT load alongside the computers. Behind the IT sit three facility loads: 40 kW lost in upstream electrical conversion, 240 kW for the cooling machinery and 20 kW for other facility equipment, 300 kW of overhead in all. Each load sits in exactly one category, so the categories add without overlap. The worked example below does the sums: 1,500 kW of IT and 1,800 kW at the facility input.

Compare that demand with a supply whose nameplate is 2,000 kW. The nameplate is a rating, and the 1,800 kW is the load drawn through it. Treat the gap between them as headroom at that one rating: redundancy requirements, cooling and downstream electrical limits can each run out before it does. The whole facility shares the nameplate, too. Its 300 kW of overhead flows through the same supply as the 1,500 kW of IT.

Over a steady interval, nearly all of that electrical input ends up as heat. Computing produces valuable results, yet the results themselves carry away a negligible share of the energy, so the electrical input sets the cooling requirement. The 1,500 kW of IT therefore means about 1,500 kW of heat to remove from the IT equipment. The other 300 kW turns into heat as well, in the electrical rooms, the cooling plant and elsewhere in the building, and the boundary you draw decides where the compressor and pump power enters the thermal account.

The word “about” matters. During a transient, stored electrical energy can rise or fall, the equipment’s own material can warm up or cool down, and a little energy leaves as light and signals. Over a steady interval those effects are small, which makes the balance a sound engineering approximation. It holds while heat is removed as fast as it is made.

## Use the ledger to catch mistakes

Double counting is the usual mistake, and the meter’s position decides what counts twice. Each 142 kW is measured at a rack’s AC input, so everything that runs inside the rack is already in it: the GPUs, the fans, and the power supplies together with their conversion losses. Start instead from a meter downstream of those supplies, which misses their losses, and the losses become a line of their own. One move of the meter changes the arithmetic, while every piece of equipment keeps its name.

A line-by-line ledger takes more work than one campus number, and it earns that work back the first time someone claims a saving. Ask which line moved: electrical losses, cooling overhead, or energy per finished task. Cut the racks’ input by 100 kW and there is 100 kW less heat to remove. Move a converter out of the rack into the room next door and the rack’s number falls by the converter’s loss, while the facility’s total stays exactly where it was. The loss has changed address.

Now remove the cooling power arrow and leave the IT electricity connected. The racks keep turning 1,500 kW into heat with the removal path gone, so the heat accumulates and the equipment warms. How fast it warms, and how long it can keep running, depends on thermal storage, coolant flow, controls and equipment limits, which the thermal lessons model. The ledger’s job is to expose the missing dependency. Naming the dependency before estimating a time is a habit that carries through every later electrical and thermal comparison.

## Worked example: Ten GB300 racks behind a 2 MW supply

- Each of ten GB300 NVL72 racks draws its published 142 kW upper requirement at its AC input; this operating point is assumed, not measured.
- Rack input totals already include their internal power supplies and fans.
- Separately metered networking and storage lie outside the ten rack totals.
- All values are simultaneous steady real power; the 2,000 kW supply nameplate is a rating.

1. Compute-rack input — 10 × 142 kW = 1,420 kW — Multiply the per-rack input by the number of identical racks.
2. All IT — 1,420 + 80 = 1,500 kW — Include separately metered networking and storage once.
3. Facility input — 1,500 + 40 + 240 + 20 = 1,800 kW — Add electrical losses, cooling, and other facility loads at matching boundaries.
4. Margin at the supply — 2,000 − 1,800 = 200 kW — This is arithmetic margin at one rating, not usable IT capacity.
5. Four-hour energy — 1,800 kW × 4 h = 7,200 kWh — Holding the load constant turns a rate into an energy total.

**Result:** The facility draws 1.8 megawatts (MW) against a 2 MW nameplate; IT contributes approximately 1.5 MW of heat.

**Model boundary:** The heat figure concerns IT equipment; it is not the duty of a specified outdoor cooling device, and the 200 kW margin ignores redundancy and downstream limits.

## The tradeoff

Choice: Meter each subsystem as well as the facility total.

Benefit: Each line of the ledger gets its own reading, so a claimed saving shows up on the line that moved: rack input, electrical losses or cooling.

Cost: More meters, and their readings must cover the same interval before they can be added.

## When the situation changes

Trigger: IT stays powered while its only heat-removal path fails.

Mechanism: Electrical input keeps turning into heat, which now accumulates in the equipment and its coolant, so temperatures rise.

Response: Name the lost heat path, then use a thermal model of storage, flow and equipment limits before predicting how long operation can continue.

## Apply the idea

If 70 kW of the ten racks’ measured input is internal supply loss, should facility power become 1,870 kW? Separately, sketch an IT hall and its supporting electrical room. A rack converter moves to a cabinet beside the rack, then to that room. Label white and gray space at each step. Does either move show lower facility power or a smaller building?

<details>
<summary>Reveal the worked answer</summary>

No. It remains 1,800 kW. The rack and the adjacent cabinet occupy white space; the separate electrical room is gray space. Neither move by itself shows lower facility power or a smaller building.

The 70 kW is already part of the 1,420 kW rack input. It becomes a separate line only when the ledger starts from a meter downstream of the supplies. Area labels locate equipment, and the equipment draws the same power wherever it stands. A freed rack slot is one gain; the new cabinet or room, its service access and its cable and replacement routes are costs that a footprint claim must also count.

</details>

**The idea to keep:** Choose the boundary before adding watts, and count each load once. Nearly all the power the IT equipment draws, computation included, comes back out as heat.

## Sources

- [EIA — Laws of energy](https://www.eia.gov/energyexplained/what-is-energy/laws-of-energy.php) — www.eia.gov · Reviewed 2026-09-06. Energy changes form rather than disappearing; the ledger uses conservation.
- [DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) — www.energy.gov · Published 2024-07 · Reviewed 2026-09-06. Data-center accounting separates IT, electrical, and cooling systems.
- [Leviton — Data center white space and gray space](https://leviton.com/support/literature/newsletters/insider/insideroctober2025/focusedproductoctober2025) — leviton.com · Published 2025-10 · Reviewed 2026-09-10. White space houses IT; gray space describes supporting back-of-house infrastructure.
- [Vertiv — Deploying Liquid Cooling in the Data Center](https://prod.vertiv.cn/4a9616/globalassets/documents/white-papers/liquid-cooling/vertiv-liquidcooling-wp-en-na-sl-71113-web.pdf) — prod.vertiv.cn · Published 2023 · Reviewed 2026-09-10. Cooling equipment may occupy white space or a grey-space mechanical gallery; service and replacement need room in either location.
- [NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) — NVIDIA · Reviewed 2026-09-12. Describes the GB300 NVL72 rack’s compute trays, in-rack switched connectivity, external compute and storage networks, management, power shelves and cooling interfaces, with a full-rack requirement of up to 142 kW.
- [Google Data Centers — Photo gallery](https://www.datacenters.google/discover-more/photo-gallery/) — Google · Reviewed 2026-09-26. Google’s photograph of server aisles in its New Albany, Ohio data center shows a data hall’s white space.
