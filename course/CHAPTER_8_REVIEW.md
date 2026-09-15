# Chapter 8 review — 15 September 2026

Slide numbers below refer to the author's review, before the redundant BBU slide
was removed. Scene links stay stable when slide numbers change.

| Feedback | Resolution |
| --- | --- |
| Add the supplied real/reactive-power explanation as a quote slide | Added verbatim in Chapter 6 after the PF comparison image and before the transformer-loading interaction: `power-factor-quote`. |
| Show PSU → VRM → Vcore rail → CPU cores somewhere | Replaced Chapter 8 slide 3 with that explicit path. Vcore is the conductive supply rail, not another converter. This introduces the terms before the later architecture comparison. |
| Consider old slide 17 for that hierarchy | The earlier placement on slide 3 supplies the needed context sooner. The later DC-voltage comparison remains distinct. |
| Remove opening gray subtitles and bottom sentence | Removed all three gray descriptions and the closing sentence. |
| Replace local capacitors with VRM? | Kept them distinct: a VRM is a regulated board converter; capacitors briefly supply or absorb current on its output rail. Both appear in the early path slide. |
| Remove the white square behind the opening image | Removed the white CSS background and blended the image’s light background into the slide; original image pixels preserved. |
| Shorten “point-of-load VRM” | New slide 3 uses “VRM” and shows what it does. |
| Slide 7: remove the other-load variable | Removed the control and parallel branch from this teaching view. It now follows processor supply across the rack, with input equal to useful output plus the two converter losses. |
| Slide 9: V = IR versus P = I²R | Both remain: voltage drop and conductor heat are different consequences of the same current and resistance. The loss is in the low-voltage path, not an inherent cost of a large voltage conversion ratio. |
| Reconsider the order of slides 8 and 9 | High current and the short 1 V path now come first, followed by direct-versus-intermediate conversion. |
| Are present-day racks predominantly direct 51 V → 1 V? | Manufacturer sources establish both architectures, not current GPU-rack market share or an unpublished GB300 board implementation. No dominance claim added. |
| Assess the supplied intermediate-rail image | Not inserted unchanged: it places direct conversion far from the chip, conflating placement with stage count. The replacement diagram keeps the final converter beside the chip in both arrangements. |
| Are two smaller conversions necessarily equally or more efficient? | No. Stage efficiencies multiply; the slide shows 98% × 95% = 93.1%. Compare actual conversion, conductor and thermal losses and response requirements. |
| Identify the multiphase slide as a VRM mechanism | It now explicitly shows switching paths inside one VRM feeding one core rail. Each path contains switches and an inductor. |
| Explain/remove residual ripple, duty ratio and normalized current | Removed these terms from the display. The graph shows individual path currents and combined current directly in amperes. |
| Is multiphase about redundancy? | Current sharing and a steadier sum are the taught mechanisms. Multiple phases alone do not establish N+1 fault tolerance or imply four separate VRMs. |
| Slide 11: remove the three scope buttons | Replaced the selector with one static view of all three scopes. |
| Slide 12: name the buffer | Explicitly a rack BBU with its converter supporting the rack DC bus. It is a separate illustrative system from the following 15 kW product. |
| Slide 12: fix text crossed by the ramp line | Rebuilt the graph with PSU/BBU labels inside their areas and the load statement above the plot. |
| Slide 14: remove unavailable-module buttons, “load fits” and assumptions | Removed the entire redundant capacity slide. Its old `bbu-shelf` link resolves to the hardware slide. |
| Does 6 × 3 kW and a 15 kW rating mean N+1? | That is the arithmetic of the documented ORv3 5+1 example. Delta's pictured product lists those ratings but does not explicitly state N+1 on the reviewed page; its design intent is not inferred from arithmetic alone. |
| Slide 15: use the supplied recharge image | Replaced the slide with the exact supplied image, without another title or controls. |
| What was slide 16 teaching? | It asked whether a larger battery can sustain an average load above the supply limit. That lesson is now already in the supplied recharge image. |
| Replace slide 16 with capacitors/BBU/generator/BESS hierarchy | Replaced it with their electrical connections and supported loads. It is not a fixed timed handoff: generator and BESS can support the facility bus while BBU and capacitors support downstream boundaries. |

Technical basis: [Infineon direct and two-stage converter comparison](https://www.infineon.com/assets/row/public/documents/24/42/infineon-dc-dc-converters-200w-dual-output-48v-pol-single-step-converter-xdpp1100-digital-controller-applicationnotes-en.pdf),
[TI 48 V to 12 V reference design](https://www.ti.com/tool/TIDA-050095),
[TI multiphase regulators](https://www.ti.com/lit/an/slyt449/slyt449.pdf),
[Delta battery shelf](https://www.delta-americas.com/en-US/products/Power-Management/12018),
[Analog Devices ORv3 5+1 example](https://www.analog.com/en/resources/analog-dialogue/articles/smart-battery-backup-for-uninterrupted-energy-part4.html).

This records implementation of the current review through old slide 17; it does
not declare the remaining Chapter 8 slides accepted.
