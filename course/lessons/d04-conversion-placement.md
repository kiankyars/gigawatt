# Moving a converter moves an interface

**6. Campus and building power distribution**

Compare two complete paths at the same delivered boundary, allocate their losses, and test how centralization changes failure and expansion exposure.

**Driving question:** How should centralized and distributed conversion be compared fairly?

## Compare functions before naming the winning architecture

Electrical power changes form and voltage at several places between a utility connection and a processor. A transformer changes AC voltage. A rectifier converts AC to DC. An inverter converts DC to AC. A DC converter changes a DC voltage level. Actual products can package these functions together with controls, storage interfaces, and protection. Counting the boxes in a simplified drawing can therefore conceal what conversion really occurs.

In a distributed arrangement, conversion may sit near each load or rack. In a centralized arrangement, a larger conversion stage may serve several downstream loads. Those labels describe placement and grouping, not an automatic efficiency ranking. The important comparison is which conductors carry which voltage and waveform, where conversion losses occur, what protection and storage interfaces change, and which equipment is shared. Chapter 9 develops specific 800 V DC proposals; here we set out how to judge a comparison.

Choose a common endpoint. If one architecture is measured at the rack AC inlet and another at a downstream DC bus, their reported input powers are not directly comparable. Draw both paths from the same upstream boundary to the same useful electrical output. Include every different stage between them. Any unchanged stages beyond the endpoint can be excluded only if the exclusion is stated consistently for both alternatives.

## A DC/DC converter can contain a transformer, but it is not one

A transformer transfers energy through a changing magnetic field. It does not take steady DC on its own and continuously deliver a different DC voltage. A DC/DC converter is the complete circuit that changes DC voltage or regulates a DC output.

A non-isolated buck converter lowers voltage using a controlled switch, an inductor and filtering capacitors; it needs no transformer. In an isolated DC/DC converter, switches turn the DC input into a changing waveform, a transformer transfers energy and provides isolation, and rectification plus filtering produces the DC output. The transformer is one component inside that converter.

UPS designs differ at the battery interface: some connect batteries directly to the DC link, while others use a controlled converter. Neither arrangement justifies an assumption of zero internal transient or a universal battery-start delay.

## Why step down before rectifying?

A conventional transformer has conductive windings around a magnetic core, commonly laminated steel. Alternating current creates changing magnetic flux; the changing flux induces voltage in another winding. Electronic switching and a permanent magnet are not required for that function. Some transformers cool by natural convection; larger designs may add fans. Cooling equipment is distinct from the core-and-windings mechanism.

A conventional route is medium-voltage AC → isolation and step-down transformer → controlled AC/DC converter → 800 V DC. The transformer reduces the voltage seen by the electronics and supplies isolation. The controlled converter sets the required DC output; a plain rectifier alone does not turn 13.8 kV AC into an isolated 800 V bus.

This is a semiconductor and system-design tradeoff. A compact direct-MV converter needs devices that withstand higher voltage or multiple switches/cells that share it, with added isolation, control and protection demands. Commercial availability of higher-voltage silicon carbide (SiC) devices can reduce that complexity. SemiAnalysis itself acknowledges conventional MV rectification using series-stacked silicon devices, so its point about device scarcity is not a universal 10 kV system limit.

Rectifying at medium voltage is possible. The design must manage device blocking voltage, AC peaks, transients, insulation and voltage sharing. Cascaded converter cells can divide the input voltage, so each semiconductor need not withstand the full system voltage. A solid-state transformer (SST) combines electronic conversion with an internal high-frequency isolation transformer. It is one way to build the interface; 800 V DC distribution also works with conventional transformers and rectifiers.

Keep the units and product claim precise: 10 kV = 10,000 V. Wolfspeed announced a commercially available 10 kV SiC power metal-oxide-semiconductor field-effect transistor (MOSFET) in March 2026. That is a device-category announcement, not a ceiling on rectifiable system voltage. A 2022 ETH/Delta/Paderborn study already described a 13.2 kV cascaded SST using 1,200 V devices.

The conventional path uses mature transformer and low-voltage power-electronic technologies. Direct medium-voltage conversion for 800 V data centers is a developing alternative, not an unavailable one. In September 2026, Eaton listed a 2 MW medium-voltage solid-state transformer (MVSST) with 12.47 kV nominal input and 800 V DC output. A product offering does not show widespread deployment, delivery time or universal economic superiority.

## Read the architecture drawings from the same boundaries

In the first drawing, compare which AC conversion and distribution functions are grouped into the future 800 V DC interface. The single “medium voltage rectifier or solid-state transformer” block is a system abstraction: voltage reduction, isolation, controls and protection still need an implementation. The drawing’s “Today” and “Future” are the publisher’s conceptual alternatives, not a claim that all facilities follow either path.

![NVIDIA conceptual comparison of AC distribution through UPS and PDUs with future 800 V DC distribution, reproduced in a Wolfspeed paper.](../assets/references/nvidia-800vdc-wolfspeed-user-figure.png)

NVIDIA architecture comparison, reproduced as Figure 1 in Wolfspeed’s March 2026 paper. The 480 V and 415 V labels belong to this example; storage and conversion details are condensed. [Wolfspeed, Figure 1, PDF page 3](https://assets.wolfspeed.com/uploads/2026/03/Wolfspeed_Powering_AI_with_reliable_SiC-based_solid-state_transformers_white_paper.pdf)

![SemiAnalysis concept with upstream conversion from medium-voltage AC to 800 V DC, a battery rack with distribution, battery and capacitor shelves, and an 800-V compute rack.](../assets/references/semianalysis-800vdc-architecture.jpeg)

SemiAnalysis battery-rack concept. Upstream rectification does not remove downstream energy storage or distribution. The 800 kW and Kyber/Rubin Ultra labels are source-specific proposal labels, not validated course equipment ratings. “DC/DC distribution” here does not imply a voltage step-down. [SemiAnalysis — Inside the 800VDC Revolution, Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part)

## A complete two-stage loss calculation

Take a scenario delivering 1 MW at the same rack-side DC boundary. Path A distributes AC with an assumed 98 percent path efficiency, then converts near the rack at 96 percent efficiency. Work backward from the 1 MW output. The rack converter needs 1/0.96 = 1.041667 MW input. The upstream AC distribution needs 1.041667/0.98 = 1.062925 MW. Total modeled loss is therefore approximately 62.925 kW.

Allocate that loss to its location. The near-rack converter dissipates 41.667 kW. The preceding distribution dissipates about 21.259 kW. Together they match the source-to-output difference, allowing for rounding. If a drawing moves the converter outside the rack boundary, the rack's apparent heat burden falls by the relocated amount, but the facility still has to supply and reject that loss unless the converter's actual performance changes.

Path B converts centrally at an assumed 97.5 percent efficiency and then distributes DC with an assumed 99 percent efficiency to the same endpoint. The downstream distribution requires 1/0.99 = 1.010101 MW input. The central converter requires 1.010101/0.975 = 1.036001 MW. Total modeled loss is about 36.001 kW: 10.101 kW in the distribution and 25.900 kW in the central converter. Under these assumptions, Path B needs approximately 26.924 kW less source power.

This is an arithmetic result for two specified models, not evidence that DC universally saves that percentage. The efficiencies are hypothetical operating-point values, including only the stated stages. Different loading, voltage, conductor resistance, standby requirements, or equipment could reverse the outcome. Indeed, if Path B's conversion efficiency were 94 percent instead of 97.5 percent, its source requirement would rise to about 1.074575 MW, exceeding Path A.

## An efficient path must also fit the service

Centralization can remove equipment from individual racks or simplify a shared conversion interface. It can also put more loads behind a common component. If a shared converter is unavailable, which loads retain an independent compatible path? Does the replacement route have enough usable output, and do the connected loads tolerate the transition? A more efficient normal-state diagram is not automatically a better continuity design.

Distributed conversion can support incremental growth because conversion capacity can be added close to a new load group. It can also multiply maintenance points and impose packaging or service-access constraints near racks. Central equipment may be purchased before the full load arrives, so its partial-load and standby behavior matter during early phases. Compare the actual anticipated operating points, rather than assigning one full-load efficiency to every year of the campus plan.

A brownfield migration adds another constraint: equipment already installed has interfaces and limits. A new downstream architecture may retain the existing upstream transformer, service, or feeder. That retained equipment can continue to bind even if a conversion stage becomes smaller. Ask which components are reused, which are replaced, and which must temporarily coexist during migration. A lower eventual loss does not remove the need for a compatible transition plan.

Finish the comparison with a table of interfaces and a balanced loss ledger. Each path should identify its input and output type, voltage boundaries, losses, shared dependencies, and supported maintenance/failure states. Mark uncertain efficiency values as uncertain. That combination lets you ask whether a proposed change is worthwhile under the actual service brief, instead of being persuaded by a shorter line of boxes or a striking rack photograph.

## Zurich-West: centralized DC required compatible loads

ABB and Green opened the Zurich-West DC expansion in May 2012. A 1 MW DC system served the 1,100 square metre extension, using DC-capable HP servers and storage. It is a historical built case of changing the downstream supply interface.

ABB Review’s technical account identifies 16 kV AC at the input and a 1,100 kVA dry transformer inside the central rectifier package. Rectifier modules perform AC/DC conversion after the transformer changes voltage. Figure 2 labels the downstream supply 380 V DC; the text specifies 400 V open-circuit. Preserve that operating-condition distinction. The example shows actual conversion placement, without adopting ABB’s promotional percentage savings as a general comparison.

## Worked example: Two routes to the same 1 MW DC output

- All efficiencies are hypothetical values at the compared operating point.
- Path A: AC distribution 0.98, then near-rack conversion 0.96.
- Path B: central conversion 0.975, then DC distribution 0.99.

1. Path A input — 1 / (0.98 × 0.96) = 1.062925 MW — Overall efficiency is the product because output from one stage becomes input to the next.
2. Path A total loss — 1.062925 − 1 = 0.062925 MW — The common 1 MW output is subtracted once.
3. Path B input — 1 / (0.975 × 0.99) = 1.036001 MW — Work backward through both included stages.
4. Difference — 1.062925 − 1.036001 = 0.026924 MW — The stated models differ by approximately 26.9 kW of source input.

**Result:** Path B wins this specified operating-point calculation; neither the placement label nor DC alone decides the result.

**Model boundary:** Unchanged downstream silicon conversion and unspecified auxiliaries are outside both paths; real equipment curves and topology must be checked separately.

## When the situation changes

Trigger: Compare one architecture at an AC inlet with another at a downstream DC output.

Mechanism: Different included conversions make the reported powers incomparable.

Response: Redraw both from a common source boundary to a common delivered endpoint.

## Apply the idea

If Path B conversion efficiency falls to 0.94 while distribution remains 0.99, which path uses less source power?

<details>
<summary>Reveal the worked answer</summary>

Path A: 1.062925 MW versus Path B: 1/(0.94 × 0.99) = 1.074575 MW.

The altered assumption reverses the ranking. Path B now needs about 11.65 kW more input than Path A for the same output.

</details>

**The idea to keep:** Compare complete paths under matching conditions; moving a loss outside the rack does not eliminate it.

## Sources

- [DOE — Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/sites/default/files/2024-07/best-practice-guide-data-center-design_0.pdf) — www.energy.gov · Published 2024-07 · Reviewed 2026-09-06. Conversion stages and distribution placement affect electrical losses and operating efficiency.
- [Schneider Electric — Choice of transformer rating](https://www.electrical-installation.org/enwiki/Choice_of_transformer_rating) — www.electrical-installation.org · Reviewed 2026-09-06. Initial and future loading and installation conditions matter to upstream equipment selection.
- [Wolfspeed — Powering AI with reliable SiC-based solid-state transformers](https://assets.wolfspeed.com/uploads/2026/03/Wolfspeed_Powering_AI_with_reliable_SiC-based_solid-state_transformers_white_paper.pdf) — Wolfspeed · Published 2026-03-06 · Reviewed 2026-09-26. Reproduces NVIDIA’s comparison of AC distribution with 800 V DC distribution as Figure 1 and describes SiC-based solid-state transformers; states that its 10 kV SiC MOSFET operates above 10,000 Hz, while 6,500 V silicon IGBTs are generally limited to a few hundred hertz.
- [Texas Instruments — TIDA-011012 modular solid-state transformer reference design](https://www.ti.com/tool/TIDA-011012) — Texas Instruments · Published 2026-06-04 · Reviewed 2026-09-16. Explains how input-series converter submodules divide medium-voltage stress across lower-voltage semiconductor devices.
- [Huber et al. — Comparative Evaluation of MVAC–LVDC SST and Hybrid Transformer Concepts for Future Datacenters (IPEC 2022)](https://www.ams-publications.ee.ethz.ch/uploads/tx_ethpublications/1_IPEC_2022_Final_Huber.pdf) — ETH Zurich, Delta Electronics and Paderborn University · Published 2022-05 · Reviewed 2026-09-10. Compares transformer-plus-rectifier and solid-state transformer (SST) architectures for 800 V DC, including a 13.2 kV cascaded design built from 1,200 V devices.
- [Wolfspeed — Introduction of a commercially available 10 kV SiC power MOSFET](https://www.wolfspeed.com/company/news-events/news/wolfspeed-introduces-industrys-first-commercially-available-10000v-silicon-carbide-power-mosfet/) — Wolfspeed · Published 2026-03-05 · Reviewed 2026-09-10. Announces a commercially available 10 kV silicon carbide (SiC) power MOSFET, on March 5, 2026.
- [Inside the 800VDC Revolution – Part 1](https://newsletter.semianalysis.com/p/inside-the-800vdc-revolution-part) — SemiAnalysis · Published 2026-05-26 · Reviewed 2026-09-11. Proposes 800 V DC architectures with upstream medium-voltage rectification and a separate battery rack for storage and distribution.
- [Texas Instruments — Basic Calculation of a Buck Converter’s Power Stage](https://www.ti.com/lit/an/slva477b/slva477b.pdf) — Texas Instruments · Published 2011-12 · Reviewed 2026-09-11. Figure 1 shows a buck converter made from switching, inductance and capacitance without a transformer.
- [Texas Instruments — TIDA-00349 isolated DC/DC converter](https://www.ti.com/tool/TIDA-00349) — Texas Instruments · Reviewed 2026-09-11. Shows an isolated DC/DC converter built from a primary half-bridge, a transformer and secondary rectification.
- [Hitachi Energy — Core-type transformers](https://www.hitachienergy.com/products-and-solutions/transformers/power-transformers/generator-step-up-transformers-gsu/core-type-transformers) — Hitachi Energy · Reviewed 2026-09-11. Transformer anatomy uses conductive windings and a laminated magnetic steel core.
- [Schneider Electric — AA and AA/FA transformer cooling](https://www.se.com/ca/en/faqs/FA102583/) — Schneider Electric · Reviewed 2026-09-11. Natural air convection and added fan cooling are distinct transformer cooling arrangements; fans are not inherent to the transformer function.
- [Eaton — Medium-voltage solid-state transformer](https://www.eaton.com/us/en-us/catalog/medium-voltage-power-distribution-control-systems/medium-voltage-solid-state-transformer.html) — Eaton · Reviewed 2026-09-16. Eaton lists a 2 MW MVSST with 12.47 kV nominal input and 800 V DC output, demonstrating a direct-MV product offering.
- [ABB Review 4/2013 — DC for efficiency](https://library.e.abb.com/public/1afa6036874fd0bb85257d5000710a17/DC%20for%20efficiency.pdf) — ABB · Published 2013 · Reviewed 2026-09-13. Case transformer, rectifier and DC distribution interfaces.
- [ABB and Green open Zurich-West DC data-center expansion](https://new.abb.com/news/detail/12816/worlds-most-powerful-dc-data-center-online) — ABB · Published 2012-05-30 · Reviewed 2026-09-13. Opening date, installation scale and compatible HP IT.

## Check your understanding: Which rating stops the load?

Pause and make a prediction, then compare your reasoning.

At a hypothetical AC interface, a load needs 900 kW at power factor 0.9. The upstream transformer is rated 1,000 kVA, while a downstream device at the same voltage is limited to 950 kVA. Ignore losses and other constraints for this screen.

**Pause and predict:** Does this path pass the stated capacity screen? Show the comparison.

<details>
<summary>Compare your reasoning</summary>

No. The load requires 900 / 0.9 = 1,000 kVA, exceeding the downstream 950 kVA limit.

The transformer reaches its stated rating, but every element of the path must carry the load. Comparing 900 kW directly with a kVA rating would hide the constraint. Passing this arithmetic screen would still leave installation and operating conditions to verify.

</details>

**The next problem:** A path that carries normal demand is only the start. What happens when supply is interrupted or equipment is unavailable?

Continue in **7. Continuity, storage and protection**: Battery power, stored energy and runtime.
