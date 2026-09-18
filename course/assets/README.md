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

## Chapter 5: parcel, building and service visuals

Five GPT ImageGen illustrations were generated and inspected on 2026-09-12.
[Exact prompts, edits and inspection notes](generated/chapter5-visual-prompts.json)
are retained alongside the PNGs. Each requested generation opportunity is
accounted for in the Chapter 5 entry of [the review tracker](../COURSE_REVIEW.md).

- `site-usable-parcel.png`: connected building pads between a utility easement and drainage.
- `site-flood-access.png`: a campus stays dry while its offsite bridge is flooded.
- `site-neighbor-boundary.png`: plant, acoustic barrier and neighboring homes.
- `site-building-cutaway.png`: data hall, electrical and mechanical rooms, receiving and a service corridor.
- `site-tray-service.png`: a generic tray fully supported at rack height by a material lift.

These illustrate physical relationships. They are not photographs of the named
sites or manufacturer equipment, construction plans, service instructions, or
performance specifications. Code labels were checked against the depicted
objects. The flood truck is on the external bank, facing away from the blocked
crossing. No arriving-vehicle claim is made. The open cutaway is a viewing device,
not an assertion that plant rooms require no partitions.

The separate `references/colossus-1-aerial.jpg` is an actual SpaceXAI photograph
of Colossus 1. Its original URL and hash are in `references/provenance.json`.
Lenovo's actual rack and annotated rear-tray photographs remain publisher-hosted;
P111 and P124 support the 29 kg tray and approximately 1,580 kg rack respectively.

## Chapter 9 compute and memory — 2026-09-14

Two new illustrations were generated with the built-in GPT image tool. Exact
prompts and asset names: [compute-prompts.json](generated/compute-prompts.json).

- [compute-scales.png](generated/compute-scales.png) introduces rack → tray → package. It is a conceptual scale view, not GB300 component placement or tray population.
- [compute-hbm-package.png](generated/compute-hbm-package.png) explains vertical memory stacking and lateral connections on a shared interposer. The cross-section exaggerates layer thickness and connection size; it does not specify a product's die count, HBM stack count, material thickness or pinout. Code leaders identify the memory, logic and interposer; the mobile layout uses full-size HTML labels.

The chapter then uses actual Lenovo/NVIDIA images for the named hardware. Local
originals, publisher URLs, retrieval dates and hashes are in
[reference provenance](references/provenance.json). The single-rack photograph,
enclosed tray, annotated tray and superchip are embedded in the slides. Numerical
and fault diagrams are code-rendered because selections must change the correct
quantities and keep every connection inspectable. No technical timing or product
rating is taken from either generated illustration.


### September 14 site-review assets

- `references/semianalysis-btm-by-state-2026.png` is the unchanged original from the September 10 BTM article. The chart’s August 24 tracker ranks booked onsite generating capacity; it does not count data centers.
- `references/southaven-geography.jpg` is a USGS historical imagery export. `southaven-geography.provenance.json` preserves its exact extent, Census state-boundary vertices transformed into image coordinates and address/permit point sources. Current construction is not inferred from that aerial. The original applicant site plan stays alongside it.

## Chapter 6 manufacturer anatomy — 14 September 2026

`distribution-siemens-nxairs-cutaway.png` and `distribution-siemens-nxairs-front.png`
are original embedded images from Siemens HA 1702 (2024 A), page 12. The cutaway is
shown in Chapter 6 with four compartment callouts and manufacturer attribution.
The product family is NXAirS up to 12 kV, separate from the generic campus circuit
and the Compass skid. Source URL, extraction method and hashes are recorded in
`distribution-siemens-nxairs.provenance.json`.


## Chapter 10 networking — 14 September 2026

- `generated/networking-scopes.png`: GPT-generated spatial overview of rack,
  cluster and external-fiber scales. The exact prompt and inspection record are
  in `generated/networking-scopes.provenance.json`. Native HTML supplies labels;
  the generated equipment is not used to establish a port count or wiring plan.
- `references/networking-connectx7.jpg`: unmodified NVIDIA single-port ConnectX-7
  family rendering. The separately named MCX75310AAS-NEAT specifications come from
  the manufacturer manual, not an inferred board marking in the rendering.
- `references/networking-qm9700-front.png`: original QM9700 front view from its
  hardware manual, with 32 twin-port cages and 64 logical 400 Gb/s ports.
- `references/networking-google-ocs.jpg`: original Google diagram of optical
  paths and MEMS mirrors. Monitor illumination and data light remain separately
  labeled in the source image.
- Original URLs and retrieval records for the three manufacturer figures are
  in `references/networking-primary-provenance.json`. Product/figure credits
  remain beside the images; detailed source interpretation is in the reader.

The topology, ring states, packet paths and timing comparisons are authored
HTML/SVG because their exact connections, quantities and interactive states
carry the explanation.

## Chapter 11 storage and recovery — 14 September 2026

- `references/storage-meta-rsc.jpg`: original Meta Research SuperCluster data-hall
  photograph published in January 2022. Its equipment is not identified as the
  later Llama 3 training cluster. Storage-tier quantities come from the RSC
  description, not from counting equipment in the photograph.
- `references/storage-google-dalles-repair.jpg`: Google's photograph of a
  technician replacing a motherboard at The Dalles, Oregon. Hardware repair
  provides context for the separate application recovery path.

Both retain their original bytes. Source URLs, captions, dimensions and
SHA-256 hashes are in `references/storage-primary-provenance.json`. Capture dates
are not established. Publisher credits remain beside the figures. The pipeline,
checkpoint versions, recovery timelines and scheduling comparisons are rendered
in HTML/SVG because their exact state and quantities carry the explanation.

### Chapter 3 opening image — 14 September 2026

`references/jensen-huang-tokens-per-watt.png` is the user-supplied Jensen Huang screenshot. The original bytes, watermark and complete frame are preserved, with no added visible caption. The adjacent provenance JSON records the attachment name, dimensions and hash; its original event/date were not supplied.

### Chapter 3 KV-cache and batching images — 14 September 2026

`references/deepseek-kv-cache.png` is the user's supplied KV-cache chart, converted
from TIFF to PNG for browser display. It matches the KV panel of Figure 1 in the
DeepSeek V4 technical report ([P193](../../research/sources/P193.md)). Its comparison
is separate from the Llama BF16 calculation beside it.

`generated/batching-bus.png` is a simple city-bus visual cue, made with the built-in
image-generation tool and inspected before integration above the batching diagrams.
Both adjacent provenance JSON files record hashes; the bus record includes the
complete generation prompt.

## Chapter 11 supplied cooling figures — 17 September 2026

`references/2crsi-single-phase-immersion-user.png` and `references/cold-plate-assemblies-user.png` preserve the supplied PNG bytes. The first matches [2CRSi’s single-phase schematic](https://2crsi.com/single-phase-immersion-cooling), with its logo retained; two-phase behavior is explained separately. The second was supplied as GB300 context, but its maker and exact model remain unverified. It is captioned “Cold-plate assemblies,” with no invented attribution or hidden-channel annotation. Hashes and usage limits are in `references/provenance.json`. The existing NVIDIA GB300 rear view is reused to locate coolant manifolds.

## Supplied economizer illustration — 17 September 2026

`references/economizer-mode-user.png` replaces Chapter 12’s economizer slide unchanged. Its embedded title is the sole visible heading. The diagram summarizes heat transfer; “from racks” and “back to racks” do not assert that facility water and technology coolant share one circuit.

### Chapter 14 maintenance diagram — September 17, 2026

`references/operations-meta-maintenance-train.jpg` is the original Meta maintenance-train illustration from its June 12, 2024 engineering account. Publisher bytes are unchanged; source, scope and SHA-256 are recorded in `references/operations-primary-provenance.json`.

## Supplied control and prefab slides — 17 September 2026

`references/three-control-layers-user.png` replaces Chapter 14's control-layers diagram using the supplied PNG unchanged. `references/prefab-factory-site-user.png` replaces Chapter 13's factory-and-site slide, converted from the supplied TIFF for browser display. Each image carries its own title; the HTML heading is hidden to prevent duplication. These are explanatory illustrations, not photographs of identified equipment.

`references/immersion-tank-user.png` is the user-supplied immersion photograph, preserved unchanged and placed immediately after the single-/two-phase explanation. Its operator and fluid were not supplied.

## Supplied Open Rack example — 17 September 2026

`references/ocp-rack-basics-user.png` preserves the image supplied through Downloads as `The-open-Compute-Project-Basics_Figure-3.png`. It follows the OCP coupling example in Chapter 13. The original publisher and rack generation have not been established; the slide does not identify it as a GB300 rack. Original bytes and SHA-256 are recorded in `references/provenance.json`.
