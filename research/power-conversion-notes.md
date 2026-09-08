Condensed from Kian's September 6–8 Google AI research capture. Power-focused reference for D03/D04/D06, not a proposal for more chapters. Repetition and unsupported numerical claims are excluded; original questions are retained where they improve the explanation.

## Solid-state transformers: the useful mechanism

**If DC has no frequency, what is switching?** A representative DC-output SST path is:

Grid AC → rectifier/DC link → switching bridge → high-frequency isolation transformer → rectifier/DC output.

The bridge creates an alternating waveform across the transformer. The input or output can be DC even though this internal stage is not. Add an output inverter only when AC output is required. An SST still contains magnetics; higher-frequency operation can reduce their size. [Infineon: operating principle](https://www.infineon.com/product-information/solid-state-transformer-how-to-optimize-systems-with-sic-power-modules).

**Why accept more electronics?** Potential gains are compact magnetic isolation, controlled conversion, and suitable interfaces to DC loads or storage. More stages also mean losses and engineering tradeoffs: compare complete systems at the same delivered-power boundary, not box count or “DC is inherently better.” Grid-disturbance handling has operating limits; it is not a promise of perfect output under every fault. The same [Infineon explanation](https://www.infineon.com/product-information/solid-state-transformer-how-to-optimize-systems-with-sic-power-modules) explicitly acknowledges conversion losses.

**Does this replace backup power?** Conversion does not create reserve energy. Storage and coordinated protection still need specifying, even if integrated into one product. DC compatibility also does not mean batteries or solar can be connected without appropriate interfaces. [Infineon: grid-to-core power functions](https://www.infineon.com/applications/ai-data-center/data-center-power-solutions).

Teaching use: answer those three questions alongside the existing [conversion-placement lesson](../course/lessons/d04-conversion-placement.md). No new lesson or presentation sequence has been added.

## AC and HVDC: keep the whole-path comparison

- Ordinary transformers made AC voltage changes economical: higher transmission voltage reduces current and resistive heating for a given delivered power.
- An HVDC link connects to AC systems through AC/DC and DC/AC converter terminals. Their cost and losses belong in the comparison.
- Skin effect raises AC conductor resistance. Cable capacitance creates charging current that consumes current-carrying capacity and contributes to resistive heating. Reactive energy exchange is not itself all dissipated as heat. Steady DC avoids repetitive charging and skin effect, not ordinary conductor or converter losses.
- Cables' charging-current constraint can favor HVDC at shorter distances than overhead transmission. There is no universal crossover distance: capacity, voltage, cable/route design, compensation, and costs matter.

[EIA-commissioned HVDC technical report](https://www.eia.gov/analysis/studies/electricity/hvdctransmission/pdf/transmission.pdf): selected history, converter, advantages, economics, and glossary passages reviewed; not a full-report review. These points support D03, rather than expanding the course into transmission-system design.

## One insulation distinction

Insulation resistance concerns leakage under applied voltage. Dielectric strength concerns the electric field at breakdown, commonly expressed as voltage per material thickness. High resistance does not establish that a component can withstand an arbitrary voltage. [FDA electrical-component definitions](https://www.fda.gov/inspections-compliance-enforcement-and-criminal-investigations/inspection-technical-guides/capacitor).

## Networking reference only — outside the power teaching insert

Distinguish a network's role (scale-up/out), switching tier (L1/L2 in a specified design), and physical medium (copper/optics). They are not interchangeable labels. GB300 NVL72 has a switched in-rack NVLink L1 domain and a separate scale-out network; do not generalize its hardware counts to other generations. [NVIDIA architecture](https://docs.nvidia.com/enterprise-reference-architectures/nvl72-ai-factory/latest/components.html).

Copper/optics choice depends on qualified reach, rate, power, routing, and serviceability—not a universal one-metre rule. Reuse the existing [media-choice lesson](../course/lessons/d08-copper-light-service.md), which records its primary-source boundaries. The original question about **what engineering changes produced NVLink's generation-to-generation bandwidth increase remains unanswered**; this compression does not pretend otherwise.
