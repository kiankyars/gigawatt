# One rack, three paths

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d01-boundaries`, then run `uv run gigawatt-expand`.

**D01 · Authored draft · Objectives:** D01.1, D01.3

Locate white and grey space, trace electricity, heat, and information, then close a facility energy balance without counting any load twice.

**Driving question:** What crosses the boundary of a working data center?

## Start with a place, then trace a connection

Imagine standing in front of a rack: a cabinet holding computing equipment and the hardware that supports it. A server is a computer inside that cabinet; a board connects components inside a server; a package contains one or more semiconductor dies. A row holds several racks, a hall several rows, a building one or more halls, and a campus one or more buildings plus shared infrastructure. These are locations nested inside locations. None of those words specifies a universal power requirement.

Two floor-plan terms help locate those systems. White space is the area housing IT equipment and its immediate support infrastructure. Grey space, also spelled gray space, is the supporting electrical, mechanical, and service area outside the IT hall, such as an electrical room or mechanical gallery. These labels describe areas in a particular layout. They are not equipment categories: a power shelf or a cooling distribution unit can occupy white space when installed with the racks.

Now draw three paths through the same picture. Electrical energy arrives through conductors and conversion equipment. Heat leaves through air, liquid, and heat-transfer equipment. Information arrives, moves between machines, and leaves through communication links. Their arrows mean different things. Coolant circulates around a loop; heat crosses an exchanger between separate loops. Data may travel both ways along a link while electrical energy continues to enter the associated equipment. Giving each arrow a clear meaning prevents an attractive drawing from teaching a false connection.

A boundary is the imaginary line around the equipment you are accounting for. Draw it tightly around a processor and its regulators may lie outside. Draw it around a rack and those regulators, fans, and power supplies may all be inside. Draw it around the facility and cooling pumps and outdoor rejection equipment enter the account. Widening a boundary changes which loads must be counted; it does not physically change their consumption. Always ask where the meter sits relative to that line.

The opening presentation uses NVIDIA’s GB300 NVL72 as a real product anchor. The enterprise reference architecture lists a full-rack requirement of up to 142 kW. That is kilowatts, not watts, and does not specify constant observed consumption or an exact metering plane. A separate teaching case assumes ten racks each draw 142 kW at their AC inputs, adds 80 kW of separate networking/storage and 300 kW of facility support, and obtains 1,800 kW total demand. A hypothetical 2,000 kW supply nameplate is a rating distinct from that demand and from 1,500 kW of IT load. Neither the nameplate nor a subtraction alone establishes usable IT capacity after redundancy, thermal and downstream constraints.

## Close the ledger without throwing computation away

Suppose ten hypothetical racks draw 100 kW each at their inlets. Dedicated network and storage equipment outside those racks draws another 100 kW. The IT total is therefore 1,100 kW. Upstream electrical conversion dissipates 40 kW, cooling machinery draws 160 kW, and other facility equipment draws 20 kW. These are distinct, nonoverlapping categories. Adding them gives 1,320 kW at the facility input. The network equipment counts as IT even though its job is to connect computers rather than execute the main model.

Over a steady interval, nearly all that electrical input ultimately becomes heat. Computing creates valuable results, but those results are not a large competing energy outlet that can be subtracted from the cooling requirement. Our 1,100 kW of IT therefore imposes approximately 1,100 kW of IT heat removal. The remaining electrical loads add heat elsewhere. Exactly where compressor and pump input enters the thermal system depends on the chosen boundary; we need not pretend that all 1,320 kW passes through the rack coolant.

The word approximately matters. Stored electrical energy and warming material can change during a transient, and small energy streams can cross through light or other signals. Our simplified balance assumes those effects are negligible over the chosen steady interval. This is a useful engineering approximation, not an assertion that every joule takes an identical microscopic path. If equipment is warming because heat removal has failed, the missing heat is temporarily accumulating, so the steady-state balance cannot be used unchanged.

## Use the mismatch to find a mistake

A second analyst adds 1,000 kW of rack power, 80 kW of rack power-supply losses, and the 100 kW networking load. The sum is wrong if the 1,000 kW was measured at rack inlets: the supplies already consume their power inside that boundary. Their 80 kW is an internal allocation of the rack total. It becomes an extra term only if the stated 1,000 kW was delivered downstream of the supplies. One changed meter location changes the arithmetic, even though all the equipment names remain identical.

A detailed ledger is more work than one campus number, but it allows a useful question: did an improvement reduce electrical losses, cooling overhead, or the energy required per completed task? Those are different mechanisms. Reducing rack input by 100 kW normally reduces the corresponding heat source, whereas merely moving a converter outside the rack moves a heat-accounting boundary. A visually smaller rack loss does not prove that the facility uses less energy.

Try a location check before claiming a space saving. A converter moves out of the rack into a cabinet beside it. Rack mounting space may be released, but the sidecar still occupies white-space floor area. Move the converter into a separate electrical room and it occupies grey space instead. To claim a smaller facility footprint, compare both layouts, their service access, and their replacement routes. Moving a box across a boundary changes its address; it does not prove that its total space or energy requirement vanished.

Test yourself by removing the cooling power arrow while leaving IT electricity connected. The diagram should not imply continued indefinite operation. The rack remains an active heat source without a complete removal path. The immediate temperature history requires thermal storage, flow, controls, and equipment limits that this ledger does not contain. We can identify the missing dependency without inventing a shutdown time. That habit will carry through every later electrical and thermal comparison.

## Worked example: Account for one hypothetical facility

- All values are simultaneous steady real power.
- Rack inlet totals already include their internal power supplies and fans.
- Dedicated networking/storage lies outside the ten rack totals.

1. Compute-rack input — 10 × 100 kW = 1,000 kW — Multiply the per-rack measured input by the number of identical racks.
2. All IT — 1,000 + 100 = 1,100 kW — Include separately metered networking and storage once.
3. Facility input — 1,100 + 40 + 160 + 20 = 1,320 kW — Add electrical, cooling, and other facility loads at matching boundaries.
4. Four-hour energy — 1,320 kW × 4 h = 5,280 kWh — Holding the stated load constant turns a rate into an energy total.

**Result:** The facility draws 1.32 MW; IT contributes approximately 1.10 MW of heat.

**Model boundary:** The heat figure concerns IT equipment; it is not the duty of a specified outdoor cooling device.

## The tradeoff

Choice: Use subsystem meters instead of a single aggregate total.

Benefit: You can locate changes and avoid overlapping categories.

Cost: More measurement points and careful time alignment are required.

## When the situation changes

Trigger: IT remains powered while its only heat-removal path fails.

Mechanism: Electrical input continues to become heat, so thermal storage grows instead of remaining steady.

Response: Identify the unsupported thermal path and require a thermal model before predicting duration.

## Apply the idea

If 80 kW of the ten racks’ measured input is internal supply loss, should facility power become 1,400 kW? Separately, sketch an IT hall and its supporting electrical room. A rack converter moves to a cabinet beside the rack, then to that room. Label white and grey space at each step. Has either move established lower facility power or a smaller building?

<details>
<summary>Reveal the worked answer</summary>

No. It remains 1,320 kW. The rack and adjacent cabinet occupy white space; the separate electrical room is grey space. Neither move alone establishes lower facility power or a smaller building.

The 80 kW is part of the 1,000 kW rack inlet total. Add it separately only when starting from a downstream power boundary that excludes it. Area labels locate equipment. Placement does not remove its electrical load, and freeing a rack slot does not account for the new cabinet, room, access or cable routes.

</details>

**The idea to keep:** Choose the boundary before adding watts; useful computation does not remove the heat obligation.

## Sources and reading boundaries

- [EIA — Laws of energy](https://www.eia.gov/energyexplained/what-is-energy/laws-of-energy.php) — Energy changes form rather than disappearing; the ledger uses conservation. Read 2026-09-06. Read the public energy-conservation explanation. The campus quantities and deductions are original hypothetical examples.
- [DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) — Data-center accounting separates IT, electrical, and cooling systems. Read 2026-09-06. Read the guide overview and relevant system/metrics material; no named facility configuration or operating measurement is inferred.
- [Leviton — Data center white space and gray space](https://leviton.com/support/literature/newsletters/insider/insideroctober2025/focusedproductoctober2025) — White space houses IT; gray space describes supporting back-of-house infrastructure. Read 2026-09-10. Reviewed the White Space and Gray Space definitions under Leviton Solutions for Data Centers. These are area conventions, not a rule assigning every power or cooling device to one room type.
- [Vertiv — Deploying Liquid Cooling in the Data Center](https://prod.vertiv.cn/4a9616/globalassets/documents/white-papers/liquid-cooling/vertiv-liquidcooling-wp-en-na-sl-71113-web.pdf) — Cooling equipment may occupy white space or a grey-space mechanical gallery; service and replacement need room in either location. Read 2026-09-10. Reviewed Designing Mechanical Space, printed pages 14–15, and the space-use discussion on page 13. No equipment clearance, floor rating, or universal footprint saving is taken from this example.
- [NVIDIA NVL72 AI Factory — System Hardware & Components](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html) — An identified GB300 rack example for distinguishing compute trays, switched in-rack connectivity, external compute and storage networks, management, power shelves and cooling interfaces. Use the component hierarchy rather than treating the rack as a collection of identical GPU power ratings. Opening product example: full GB300 NVL72 rack requiring up to 142 kW; annotated manufacturer image. Read 2026-09-12. The /latest/ URL is mutable. Page inspected as updated May 18, 2026. Marketing performance ratios are workload-dependent and are not adopted. Its bandwidth recommendation block has an unclear per-GPU versus aggregate scope, and scale-out wording for in-rack NVLink needs interpretation against the switched topology. Do not reproduce those as universal specifications; verify exact OEM configuration before any sizing exercise. The 142 kW bullet does not explicitly name its AC/DC measurement plane or workload. The course ledger labels 142 kW at an AC inlet as a hypothetical operating assumption, not a measured NVIDIA result.
