# 800 V is an interface, not an entire architecture

**D06 · Authored draft · Objectives:** D06.2, D06.3, D06.4

Compare three declared architectures while preserving their conversion, storage and protection interfaces.

**Driving question:** What changes when conversion sits in the rack, beside the rack, or at the facility boundary?

## Keep the three drawings separate

Architecture A brings AC distribution to a compute rack, converts it to a lower-voltage DC bus, and regulates power near devices. Architecture B retains AC distribution but moves rectification into an adjacent power rack or row unit. A higher-voltage DC connection then reaches compute racks, which contain the required downstream conversion. Architecture C begins DC distribution farther upstream, potentially near the facility electrical boundary. These drawings can share a nominal DC voltage while differing in conductor lengths, maintenance zones, fault exposure and responsibility for stored energy.

The comparison becomes useful when unchanged equipment stays visible. In B, the upstream AC feeder still carries the aggregate load delivered to the row, plus conversion losses. In C, a longer portion of the facility becomes a DC distribution system and must be designed accordingly. Neither sketch determines how many storage modules, isolation stages or protective devices are required. Draw those as explicit blocks with interfaces rather than assuming that central rectification automatically replaces every UPS function.

## Read a roadmap as a dated design proposal

NVIDIA’s May 2025 account described a facility-level 800 VDC concept and linked full-scale production to 2027 systems. Its August 11, 2026 update separately described a hybrid power rack expected in the second half of 2026, a row power center expected in 2027, and a broader DC power block. These are vendor descriptions and availability expectations as published. They establish proposed architecture categories, not evidence that a named site has accepted an operating installation or achieved a claimed efficiency.

When a diagram says 800 V, ask between which conductors it is measured. A two-conductor 800 V differential and a bipolar arrangement described relative to a midpoint cannot be substituted silently. Their conductor-to-ground stress, fault cases and service interfaces depend on the actual grounding arrangement. The teaching diagram should show the specified convention without inventing it. Similarly, an AC voltage label needs a declared phase configuration and line-to-line or line-to-neutral meaning. A DC current comparison must not be casually reused as a three-phase AC feeder calculation.

## Compare a chain, not the number of boxes

Fewer conversion stages can be attractive, but stage count is not an efficiency measurement. A larger converter at low load may behave differently from several smaller modules loaded near their intended operating range. Redundancy, thermal conditions, auxiliary power and standby behavior can also change the result. Create a table of stage efficiencies for each architecture at the same delivered load. Multiply efficiencies only along one energy path, add branch loads where they join, and allocate auxiliary consumption to its real location.

The physical interfaces deserve equal attention. A rack input specification must cover steady demand, peak demand, permitted voltage variation and the response to a sudden load change. The downstream equipment and upstream supply must agree on startup sequencing, fault isolation and shutdown behavior. A higher voltage reduces current at fixed power, but stored electrical energy and fault interruption remain separate engineering questions. The course comparison asks which functions moved and which must be revalidated. It does not instruct a learner to select protective equipment from a nominal voltage alone.

## Worked example: Two deliberately simplified conversion chains

- Both paths deliver exactly 100 kW at the same final DC load boundary.
- Path A has assumed efficiencies of 98%, 97% and 95%; path B has 98.5% and 96%.
- Auxiliary loads, conductors and redundancy effects are excluded equally to isolate the series-conversion calculation.

1. Compute path A efficiency — 0.98 × 0.97 × 0.95 = 0.90307 — The three serial stages deliver 90.307% of their input to the declared output.
2. Compute path B efficiency — 0.985 × 0.96 = 0.9456 — Two assumed stages deliver 94.56%.
3. Compare inputs — 100 / 0.90307 = 110.733 kW; 100 / 0.9456 = 105.753 kW — At equal output, the input difference is about 4.980 kW.
4. State the comparison correctly — (110.733 − 105.753) / 110.733 ≈ 4.50% — This is a reduction in modeled input relative to A, not the percentage-point difference between efficiencies.

**Result:** Path B uses about 4.50% less input in this constructed example. That conclusion follows from the assigned efficiencies, not from the label 800 V.

**Model boundary:** No values represent measured NVIDIA hardware, and omitted parallel loads would change an end-to-end result.

## The tradeoff

Choice: Extend DC distribution farther toward the facility boundary.

Benefit: Allow conversion and distribution to be reconsidered together instead of preserving every existing stage.

Cost: Expand the scope of protection, grounding, maintenance, controls and equipment qualification that must be coordinated.

## When the situation changes

Trigger: A team treats a hybrid sidecar as a facility-wide DC conversion.

Mechanism: The drawing hides retained AC constraints and incorrectly attributes all upstream losses and UPS functions to equipment that has not changed.

Response: Mark every retained and replaced block, then compare the same electrical endpoints under a documented operating state.

## Apply the idea

Path B requires an additional constant 6 kW auxiliary load supplied at the upstream boundary. Does it still use less input than A in this example?

<details>
<summary>Reveal the worked answer</summary>

No. B becomes 111.753 kW, about 1.020 kW above A.

The unmodeled auxiliary reverses the arithmetic result. This does not show that a real high-voltage design has such a load. It demonstrates why architecture claims require an inclusive boundary and measured auxiliary behavior.

</details>

**The idea to keep:** Specify where 800 V begins and ends, what remains AC, and which claims are roadmap statements.

## Sources and reading boundaries

- [NVIDIA 800 VDC Architecture Will Power the Next Generation of AI Factories](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/) — May 2025 facility DC concept, conversion placement and forward-looking 2027 timing. Read 2026-09-06. Vendor roadmap; projected savings and reliability claims are not adopted as measured results.
- [Why Scaling AI Compute Performance Requires a New Power Architecture](https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/) — August 2026 distinction between hybrid power rack, row power center and facility DC power block. Read 2026-09-06. Published availability expectations are not proof of installation, acceptance or site compatibility.
