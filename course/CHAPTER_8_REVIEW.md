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


## Follow-up review: electrical foundations and DC architectures

These numbers refer to the 34-slide version reviewed after the first revision.

| Feedback | Resolution |
| --- | --- |
| Slides 18–19 belong in the primer | Removed those Chapter 8 stops. The primer already teaches the complete DC loop, AC polarity and power, so no duplicate primer slides were added. Old links open the corresponding primer scene. |
| Put slide 20 near the first three-phase/single-line explanation | Moved the current-return and summed-power view directly after Chapter 6’s single-line diagram. The primer retains its simpler introduction. |
| Consider the same move for slide 21 | Moved the 480 V line-to-line measurement immediately after the three-phase view in Chapter 6. Both interactive controls remain. |
| Slide 22 onward is good | Preserved the copper, current, losses and conversion sequence after removing the preceding recap. |
| Is slide 26 AC until the rack? | Yes: the conventional AC baseline converts AC to DC inside the compute rack. The next two diagrams move that conversion into a sidecar, then farther upstream. |
| Add a stacked three-view preview before slide 26 | Added “The three phases of the DC data center revolution,” with the same three architecture drawings stacked top/middle/bottom. The labels identify conversion placement; they do not relabel the conventional baseline as a SemiAnalysis forecast phase. |
| Remove the two Zurich-West explanatory lines on slide 29 | Removed the 400 V open-circuit line and historical-interface footer. Their source explanation remains in the underlying notes. “Open-circuit” means voltage with no load drawing current. |
| Does slide 31 mean AC does not need breakers? | No. Both AC and DC need fault protection. The slide now says DC-rated protection; its notes explain that AC current-zero crossings help an opened breaker extinguish an arc, while DC protection must force interruption without that periodic crossing. |
| Remove slide 33 and its broken/trivial migration question | Removed the exercise from navigation. Its old link opens the closing power-stack slide. The preceding feeder-capacity example remains. |
| Slide 34 is great | Kept the supplied power-stack image as the closing slide. |

## Recording follow-up: falling GPU demand

The new `source-ramp-down` slide immediately follows the rising-load example.
It shows a 40 kW surplus decaying linearly over 0.2 or 0.4 seconds: 4 or 8 kJ
into a bidirectional buffer, with the same 40 kW peak charging requirement.
The graph measures power above the new GPU load. Available charging power,
energy headroom and bus-voltage consequences are part of the explanation.
This closes the downward-power-step follow-up; Chapter 8 now has 32 slides.

## Visual follow-up — 16 September 2026

- Slide 8 now uses the supplied whole-rack power account: 72 kW processor rails,
  a fixed 12 kW parallel branch, and 93.05 kW at the AC inlet. This supersedes
  the earlier processor-only ledger without reintroducing an other-load control.
- Slide 9 separates the current comparison, loop resistance, voltage drop and
  conductor heat into clearly spaced regions. Both resistance settings remain.
- Slide 10 uses the supplied direct/intermediate conversion image. Its green
  panel reads: “Either design can be efficient, depending on the project requirements.”
- A motherboard illustration follows the four-phase VRM interaction. Its
  6/12/18-path layouts replace unsupported budget/gaming/high-end phase ranges:
  advertised power-stage counts can differ from independently controlled phases.
  The original upload is preserved; the displayed derivative was edited with
  the built-in image tool. [Asset provenance and prompts](assets/references/rack-energy-review-figures.provenance.json).

There are now 33 slides. The former slide 12 and later slides move forward by one;
all existing scene links remain stable. Redundancy recommendations are recorded
in [the course review](COURSE_REVIEW.md#remaining-course-redundancy-review--16-september-2026).

## Approved redundancy cut — 16 September 2026

Removed the separate rear-busbar stop already taught in Chapter 2. Its old link
opens the rack-anatomy slide, whose notes retain the brief local-bus reminder.
The following supply path still shows the voltage conversion in context.
The chapter is back to 32 slides; the new VRM illustration and all September 16
image/layout changes remain intact.

## Further review — 16 September 2026

- Slides 5 and 15 show different products: AC/DC supplies versus battery backup.
  Kept both and made their titles identify the function.
- Renamed former slide 17 to “Where backup power connects” and placed it
  immediately after the related slide 12.
- Removed the requested grey conductor-loss, Zurich-West device-rail and
  sidecar retrofit captions. The sidecar architecture now names the sidecar.
- Split former slide 23 into consecutive supply-path and converter-loss slides.
  The new loss scene has its own URL and working calculation reveal; the supply
  scene retains its existing URL. The chapter now has 33 slides.
- Recommended, not yet applied: merge the overlapping slides 12/17 using the
  connected-path diagram while retaining UPS context; split rack power/buffering
  from 800 V distribution; put the 50 V/800 V comparison in the latter opening.
  That comparison concerns distribution current, unlike the earlier local 1 V
  path. It also uses a different baseline from the following 480 V AC comparison.

## Chapter split — 16 September 2026

Implemented: Chapter 8 is now **Rack power and buffering** (17 slides); Chapter 9
is **800 V DC distribution** (16 slides). The 50 V/800 V comparison follows the
new DC opening. Old slide fragments route to the correct deck with teaching and
presenter state preserved. Reader ownership and later chapter numbers follow
the same split. The two storage-location/support-path diagrams remain intact;
the proposed merge is one connected diagram with facility/rack/chip groupings,
not two vertically stacked diagrams.

The subsequent September 16 instruction removes bookmark compatibility. The
location and support-path views are now merged into one connected
**Where backup power connects** diagram, with facility, rack and chip groupings.
Chapter 8 now has 16 slides.

## Current Chapter 8 accepted — 16 September 2026

Kian explicitly confirmed satisfaction through Chapter 8. The current 16-slide
**Rack power and buffering** chapter is accepted and verified. The separate
Chapter 9 remains under review; its approved revision moves architecture ahead
of supply equipment and preserves the low-voltage/800 V rack-bus distinction.

## Recording-review slide follow-through — 18 September 2026

The current split is Chapter 8 (rack power and buffering) and Chapter 9 (800 V DC distribution). This checks slide content separately from corrections to the narration.

### Implemented

- Chapter 9, slide 2 (`conductor-copper`): title now reads **One-third less copper in these conductors**. Equal length, cross-section and material remain visible. The three 480 V AC phase conductors are compared with two 800 V DC conductors; this does not establish a reduction in all facility copper. Speaker notes explicitly preserve the 480 V AC baseline throughout the following current and conductor-loss examples.
- Chapter 9, slide 15 (`power-stack-overview`): the previously requested Highest ASP/server label has been removed, and the map now follows the DC architecture comparison.
- Chapter 9, slide 15: the author-approved single contrast edit brightens the secondary text while preserving the layout, wording and attribution. Original and previous teaching images remain in the asset archive.

### Remaining slide recommendations

- **Chapter 8, slide 8 — conductor voltage drop:** show the compensation explicitly: 1.1 V at the regulator minus 0.1 V along the path leaves 1.0 V at the chip. Separate the ideal 50 V × 20 A comparison from the calculation that includes conductor loss; preserving 1 kW at the chip requires additional upstream power once losses are included.
- **Chapter 8, slide 18 — recharge:** identify the depicted pulse as a constant 40 kW shortfall for 0.2 seconds. Its 8 kJ is correct; the earlier ramp example is triangular and uses 4 kJ over 0.2 seconds. This is a change in the power profile, not conflicting arithmetic.
- **Chapter 9, slide 15 — power-stack map:** its separate semiconductor layer can imply a serial conversion stage; explain visually that these devices operate inside PSUs and VRMs. The 18.3–30 kW per-PSU range and 25–40% lower-loss figure need named product/comparison context before being presented as general specifications. Removing the ASP label and improving contrast did not verify the remaining market figures.

The current slides already distinguish rack/tray/board counts, the Clemente intermediate stage, input/output current, summed phase currents, the two rack-power accounting boundaries, 480 V line-to-line versus 277 V phase-to-neutral, PSU and battery products, and forecast versus operating rack capacity. The spoken GDDR5, constant-current, capacitive-voltage-transformer and universal rack-power-limit claims are not reproduced in those teaching diagrams. Camera overlay and excessive zoom are recording issues.
