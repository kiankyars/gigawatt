# Teaching illustration assets

Five illustrations were generated with the **built-in GPT ImageGen tool** on
2026-09-06 and copied into this repository. Prompts are preserved in
[generation-prompts.json](generation-prompts.json) and
[additional-prompts.json](additional-prompts.json). The source files are the
original generated PNGs; no manufacturer figure or paid article image was used
as a visual reference.

| Asset | Permitted orientation role | Do not use it to teach |
| --- | --- | --- |
| `campus-cutaway.png` | Locate the electrical area, racks and mechanical yard in a hypothetical campus | Conductor or pipe routes, equipment counts, capacities, or the identity of the yellow cabinet as a UPS |
| `rack-anatomy.png` | Show the relative rack → tray → device scales | Actual rack-unit occupancy, OEM component placement, connector details or coolant paths; the illustrated assembly is invented |
| `cooling-cutaway.png` | Recognize the three equipment groups at a glance | Flow tracing or CDU anatomy; branches and pump connections are ambiguous, including an apparent supply/return cross-connection |
| `power-equipment.png` | Show an overview of electrical equipment categories | UPS internals, battery interconnections or the busway-to-rack interface; none is verified and some interfaces are omitted |
| `network-equipment.png` | Distinguish compute, switching, storage and management equipment | Logical topology, redundancy, cable media or bandwidth; the bundles imply unsupported connections |

Visual inspection after generation checked appearance, not technical accuracy.
The current images have not been validated as equipment anatomy or engineering
layouts. Select them explicitly for orientation; do not automatically attach them
to every lesson in a domain. A caption cannot repair misleading visible plumbing
or connections. Use verified equipment views or authored diagrams for those claims.

Manufacturer and other sourced images also need provenance and a check that the
depicted product, configuration and operating state support the lesson's claim.
For code-rendered diagrams, check connections and flow paths against the stated
model and source; successful rendering or arithmetic tests do not establish
topological correctness. Keep labels accessible and numerical results separate
from illustrative geometry. The generation manifest records image hashes for the
current authored edition.

## Sourced reference images

The overview and rack-power sequence embed NVIDIA's annotated **DGX GB300 rear
hardware figure**, inspected 2026-09-12, from the
[GB rack hardware guide](https://docs.nvidia.com/dgx/dgxgb200-user-guide/hardware.html#power-shelves).
The [publisher-hosted image](https://docs.nvidia.com/dgx/dgxgb200-user-guide/_images/hardware-rack-rear-gb300.png)
identifies the power busbar, cooling manifolds and NVLink cable cartridges.
The narrow composition enlarges the cabinet and points to the same busbar
location; it does not invent hidden components. The guide's **nominal 50–51 V DC**
bus description is kept separate from its approximate combined-guide power
example and from the enterprise GB300 up-to-142-kW requirement. This figure
does not establish an OEM-independent BBU configuration or board regulator design.

Section 4 embeds GE Vernova's photograph of **Dania Beach Clean Energy Center**,
inspected 2026-09-12, from its
[FPL case study](https://www.gevernova.com/gas-power/resources/case-studies/first-7ha-florida-power-light).
The publisher-hosted image shows a real combined-cycle plant; the adjacent
two-7HA.03 and up-to-1,260-MW labels are manufacturer-reported plant claims.
No claim is made that the plant supplies the course's campus or operated at that
output when photographed. The diagram and cost/fuel models remain separate
original teaching examples. Neither publisher image is AI-generated.

The overview's second slide opens on Google's photograph of server aisles at
its **New Albany, Ohio** campus, credited on the slide. Source:
[Google Data Centers photo gallery — Central Ohio](https://www.datacenters.google/discover-more/photo-gallery/),
inspected 2026-09-12. The image is embedded from the
[publisher's image CDN](https://www.gstatic.com/marketing-cms/assets/images/19/43/b476c0984f2da3b2faa1a7f588ce/server-aisles-in-our-new-albany-data-center-building-in-central-ohio.jpg=n-w1086-h814-fcrop64=1,0000202fffffdfea-rw),
not copied into this repository. Desktop presentation crops it to the available
wide frame; phone presentation contains the full publisher-served image. It is
a visual reference for equipment racks, aisles and overhead infrastructure—not
a universal data-hall layout, a GB300 installation, or evidence of an identified
cooling component. The selectable white/gray-space floor plan is a separate
teaching schematic, not a plan of Google's building.

`references/provenance.json` records publisher URLs, retrieval dates and file
hashes. The two supplied 800 V DC diagrams are embedded, with source-specific
limits, in D04's conversion-placement lesson. They are architecture proposals,
not validated installation drawings. The recovered SemiAnalysis JPEG matches
the missing attachment's image UUID; the supplied NVIDIA/Wolfspeed PNG is unchanged.

The Schneider Easy UPS product-family photograph is an official external view.
Its two pictured cabinets do not establish a UPS/battery pairing or redundancy
configuration; use the manufacturer's documentation for those relationships.

The user-supplied three-column AC / DC sidecar / direct-MV-DC figure is embedded
in the 800 V teaching sequence and D06 reference. Its attribution to OCP is from
the user; the exact publication is still unverified. The linked OCP LVDC paper
is related context. The PNG is unchanged; these alternatives carry no adoption
dates and do not specify complete protection or storage arrangements.

The overview's TPU view embeds Google's photograph of **eight Cloud TPU v4
racks**, one eighth of a 4,096-chip pod. Source: [Google Cloud — TPU v4](https://cloud.google.com/blog/topics/systems/tpu-v4-enables-performance-energy-and-co2e-efficiency-gains),
reviewed 2026-09-12. The publisher-hosted photograph is unchanged. Its adjacent
64 × 64-chip block diagram explains logical grouping and optical connections;
it does not reproduce cable routing or imply that pod ICI is a wide-area fabric.

The workload sequence embeds **Figure 1 from Choukse et al., Power Stabilization
for AI Training Datacenters (2025)**, [paper and source figure](https://arxiv.org/html/2508.14318v1),
reviewed 2026-09-12. This is normalized production DGX-H100 training telemetry,
embedded unchanged from arXiv with authors and figure number on the slide. The
article is licensed CC BY-NC-SA 4.0. Later traces are separate original teaching
models; they are not reconstructed measurements or GB300 performance claims.


## September review: requested GPT figures

Three additional figures were generated with the built-in **GPT ImageGen** tool
on 2026-09-12. The unmodified PNG outputs are in `generated/`; exact prompts are
in `generated/september-review-prompts.json` and `generated/shared-grid-prompt.json`.
The request-by-request accounting is in `COURSE_REVIEW.md`.

| Asset | Teaching use | Accuracy boundary |
| --- | --- | --- |
| `generated/workload-handoff.png` | Chapter 3 closes on a rack, power measurement, and supply equipment | Generic exteriors, not GB300 anatomy. The code-overlay trace is schematic, not measured telemetry. |
| `generated/power-configurations.png` | Chapter 4 introduces four normal-supply arrangements, then enlarges each quadrant | Arrows were visually checked for grid imports, local supply and export direction. Backup, protection, switching and grounding are omitted. Not an installation drawing. |
| `generated/shared-grid.png` | Chapter 4 shows two campus feeds meeting at one upstream substation | Original invented geography; no real-site route, capacity, equipment count or electrical topology is asserted. |

The supplied SemiAnalysis configuration image was not used as a generation
reference or embedded. The original figure uses the four conventional supply
categories. Electrical explanations are cross-checked against the primary
references in the research catalog.

Chapter 4 uses publisher-hosted **GE Vernova gas-turbine/generator anatomy** and
**Siemens Energy combined-cycle and dispatch diagrams**, inspected 2026-09-12:

- [GE Vernova: What is a gas turbine?](https://www.gevernova.com/gas-power/resources/education/what-is-a-gas-turbine)
- [Siemens Energy: Combined-cycle power plants](https://www.siemens-energy.com/global/en/home/products-services/product/combined-cycle-power-plants.html)
- [Siemens Energy: Peaker plants](https://www.siemens-energy.com/global/en/home/products-services/product/peaker-plants.html)

These are actual manufacturer figures, not generated equipment internals.
The added GE component labels identify the visible stages. The Siemens 64%
efficiency annotation is a vendor example, not a universal combined-cycle rating;
its dispatch chart is qualitative, not measured or forecast data.

Oracle's Abilene media comes from its [data-centers page](https://www.oracle.com/data-centers/).
The aerial and turbine-plant photographs are captioned **15 July 2026**;
Oracle's **September 2026** capacity status is a separate claim. The course does
not relabel the photographs as September satellite captures or infer a new MW
total from Oracle's percentage. Chapter 5 additionally embeds actual Lenovo
rack and compute-tray views from the [GB300 NVL72 product guide](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai),
updated 2026-08-30. They show this product's service geometry, not a universal
rack configuration or full rack operating mass.
