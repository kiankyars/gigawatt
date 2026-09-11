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

`references/provenance.json` records publisher URLs, retrieval dates and file
hashes. The two supplied 800 V DC diagrams are embedded, with source-specific
limits, in D04's conversion-placement lesson. They are architecture proposals,
not validated installation drawings. The recovered SemiAnalysis JPEG matches
the missing attachment's image UUID; the supplied NVIDIA/Wolfspeed PNG is unchanged.

The Schneider Easy UPS product-family photograph is an official external view.
Its two pictured cabinets do not establish a UPS/battery pairing or redundancy
configuration; use the manufacturer's documentation for those relationships.
