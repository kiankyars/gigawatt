# Fault isolation, grounding and DC interruption

**7. Continuity, storage and protection**

Explain fault detection and selective isolation, distinguish AC and DC interruption, and use a bounded heating example without pretending to choose real protection settings.

**Driving question:** Why can the same breaker arrangement behave differently under another source or grounding scheme?

## Protect a zone without losing the whole system

A fault is an unintended electrical condition, such as an insulation failure that creates a new current path. The system must detect the relevant condition and interrupt or otherwise manage it within the equipment's capabilities. Protection therefore includes a measurement or detection function, a decision about the affected zone, and a suitable action. A circuit-breaker symbol on a drawing represents only part of that chain. Its presence does not show that the complete system will behave selectively.

Selectivity means coordinating protection so that the appropriate downstream device can isolate the affected circuit while unrelated circuits remain supplied, within the stated range of faults and conditions. Imagine three rack groups connected through separate branch devices to one upstream bus. A fault in the middle branch should not unnecessarily remove all three groups if the architecture is intended to preserve the others. However, a fault on the shared bus is a different event; branch devices cannot create a path around that missing common element.

The available fault current changes with the source. A transformer fed from a strong grid limits a short circuit on its secondary mainly by its own impedance. In a worked example from ABB’s 2008 technical paper on transformer substations and short-circuit calculation, an 800 kVA transformer with a 5 percent short-circuit voltage has about 1,155 A of rated current at 400 V and feeds about 23 kA into a three-phase fault on its secondary, 20 times rated, taking the upstream network as infinitely strong. A synchronous generator’s subtransient reactance, about 10 to 20 percent for smooth-rotor machines and 15 to 30 percent for salient-pole machines in the same ABB paper, lets it feed roughly 3 to 10 times rated current at first, and that current then decays. An inverter limits its own output. Schneider Electric’s technical specifications for the Easy UPS 3-Phase Modular give its 50 kW model 73 A of nominal output current at 400 V and an inverter short-circuit current of 160 A for 220 milliseconds, about 2.2 times rated.

Protection works only when the fault current exceeds the trip setting. ABB’s guide to medium-voltage protection states the rule: the protection trip current must always be lower than the minimum short-circuit current at the point of connection. A breaker whose instantaneous trip needs several hundred amperes clears a fault quickly when the transformer-fed bypass supplies it, yet it cannot trip on the 160 A that the inverter alone delivers. A scheme checked only in the normal utility-fed state may therefore fail in another supported state. Schneider’s public coordination guidance distinguishes source conditions for the same reason, so ask which source and topology were evaluated rather than which setting a nominal load current suggests.

## Compare clearing exposure without designing a breaker

Use a deliberately narrow mathematical example. During a fault, assume a fixed 1,000 A flows through a segment with 0.020 ohm resistance until isolation occurs. Resistive heating during that constant-current interval is I²R times duration. If the interval is 20 milliseconds, convert it to 0.020 seconds: 1,000² × 0.020 × 0.020 equals 400 joules. If it lasts 100 milliseconds, the corresponding value is 2,000 joules.

The fivefold duration produces fivefold heating in this fixed-current, fixed-resistance model. The associated I²t quantities are 20,000 and 100,000 ampere-squared seconds. They are useful for seeing the role of time, but they are not complete equipment damage or personnel hazard calculations. Actual fault current changes with time; resistance can change with temperature; stored energy, arcing, device behavior, and thermal limits require additional analysis.

Selectivity introduces another dimension. If the upstream device removes the entire bus quickly, the isolated branch's exposure may be limited but every downstream group loses power. If the intended branch device isolates only the affected group, service to others can continue under the specified disturbance tolerance. The correct design must satisfy protection and continuity requirements together. It is not enough to declare that the smallest clearing time or the fewest tripped devices is always best.

AC current normally crosses zero periodically, which can assist arc extinction under suitable interrupting conditions. This instantaneous current zero is part of an energized waveform: it is not proof of absent voltage or safe isolation. DC lacks a recurring natural current zero of that kind. Its interrupting system must force or achieve current extinction while managing stored circuit energy and the voltage that appears across the open device. AC and DC ratings therefore cannot be exchanged without checking the specified duty.

## Disconnected AC does not remove every energy source

An open AC input can leave a battery connected to the DC link, and a disconnected capacitor can retain charge. In the earlier ideal example, even the 700 V operating cutoff leaves 49 kJ in the capacitor. A converter stopping its load is therefore a different condition from the circuit being de-energized.

Actual safe isolation must account for every source and stored-energy path and verify the resulting absence of voltage under the applicable equipment procedure. A zero crossing, an open-switch icon or a stopped load does not prove that state.

## Grounding changes the fault path, not the laws of electricity

Grounding, also called earthing in many references, describes how source and exposed conductive parts relate to earth and protective conductors. It influences the voltage that can appear on accessible parts, the path taken by fault current, and the detection strategy required. Current does not disappear into an earth symbol. Draw the complete circuit back toward the source, including the impedances that limit current and any relevant capacitive paths.

Standardized earthing families make different choices about the source-to-earth relationship and the connection of exposed conductive parts. An isolated or impedance-referenced source is not simply a system with no protective bonding, nor a guarantee that faults are harmless. First and subsequent insulation faults can have different consequences. The letters IT in an earthing scheme also do not mean information-technology equipment. These distinctions belong in the vocabulary before using a compact grounding symbol as an explanation.

Power electronics can further alter fault detection. A converter may limit sustained fault current while stored capacitors supply a brief initial contribution. A protection scheme based only on a large sustained overcurrent might therefore be inappropriate. ABB's indexed technical discussion highlights that converter and circuit dynamics matter to interruption. This lesson does not translate that observation into device settings; it identifies the evidence a design comparison must supply.

Before endorsing an architecture, ask for its supported source states, grounding arrangement, prospective fault-current behavior, interrupting ratings, coordination evidence, stored-energy paths, and load disturbance tolerance. Ask separately what happens when protection itself or a common control dependency fails. These are conceptual review questions, not instructions to work on energized equipment. A complete answer must come from the engineered installation and its validation.

The worked heating example makes one mechanism visible: changing current or clearing duration can sharply change energy deposited in a resistive path. The three rack groups on one bus supply a different mechanism: where isolation occurs determines which loads lose service. Combine those perspectives without confusing either with a complete safety or reliability certification.

## Bonding and the complete fault loop

A conductive equipment case can become part of the fault circuit. Protective bonding provides a designed return path that lets protection detect and disconnect the fault. The same event has both a shock-protection consequence and an outage boundary; a case may rise in voltage before disconnection, so bonding is not a promise that every fault leaves its voltage at zero.

Protective bonding connects exposed conductive metal to the protective-conductor system. In a TN system, protective conductors connect exposed metal back to the earthed point of the source, so a live-to-case fault returns along the protective earth (PE) conductor to the source, allowing protection to disconnect the circuit. A surge arrester instead limits a transient overvoltage; it does not replace this permanent bonding connection. Loop impedance Z is the combined opposition of the source, outward live conductor and return protective conductor. Fault current is approximately phase-to-neutral voltage divided by Z; a high impedance can limit current enough to delay an overcurrent trip. Other earthing systems can require different detection arrangements.

Now put a severe short circuit on the shared bus itself, before upstream clearing. The breaker contacts remain closed and fault current can still flow, but bus voltage has collapsed below what the groups need to operate. This differs from a branch fault cleared by opening the upstream breaker. Removing the fault supply later would not itself repair the common bus. The groups have lost usable service, which is not proof of absent voltage or a safe circuit.

Opening contacts can leave an arc carrying current. Chapter 9 applies this principle to an 800 V DC feeder: a conventional arc chamber lengthens and cools the arc until current is extinguished, while circuit energy must be managed. Semiconductor and hybrid devices use different mechanisms. The device’s DC voltage and interrupting ratings must match the circuit.

## A gap is not yet an interrupted current

Follow a breaker’s contacts through three states. First, touching contacts complete a conducting circuit. Next, the contacts separate, but hot ionized gas can bridge the gap and carry current. Finally, the arc is extinguished and the gap no longer conducts. The circuit current is then zero while the source remains energized and voltage can appear across the open contacts.

In the last two states the contacts sit in the same positions; what changes is whether the gap contains a conducting arc. AC current zero crossings can help extinguish an arc; DC interruption must achieve current extinction without that recurring natural zero. Neither an interrupted load current nor this simple sequence proves that every part of real equipment is de-energized.

## Worked example: A fixed-current fault heating comparison

- Fault current is held at 1,000 A solely for this illustration.
- The segment resistance is constant at 0.020 Ω.
- The example excludes arcs, capacitor energy, changing current, and equipment damage thresholds.

1. Convert time — 20 ms = 0.020 s; 100 ms = 0.100 s — Energy calculations require a consistent time unit.
2. Short interval heating — 1,000² × 0.020 × 0.020 = 400 J — I²R gives watts, then multiplication by seconds gives joules.
3. Long interval heating — 1,000² × 0.020 × 0.100 = 2,000 J — At fixed current and resistance, energy scales directly with duration.
4. Exposure ratio — 2,000 / 400 = 5 — Five times the interval gives five times the modeled resistive heating.

**Result:** Clearing duration matters strongly, but the calculation does not select a protective device or define a safe operating procedure.

**Model boundary:** Only a stated constant-current resistive segment is modeled; actual fault and interruption behavior requires topology-specific engineering.

## The tradeoff

Choice: Coordinate isolation to preserve unaffected branches.

Benefit: A local fault can be confined to its intended zone under the validated conditions.

Cost: Coordination must remain valid across source states and equipment limits; a shared-bus fault still affects the common dependency.

## When the situation changes

Trigger: Reuse a protection claim after changing from utility AC supply to a different converter-fed or DC topology.

Mechanism: Fault waveforms, current limits, interruption conditions, or grounding paths may no longer match the earlier evidence.

Response: Require protection and coordination evidence for the new topology and supported states before claiming equivalence.

## Apply the idea

At 2,000 A for 10 ms through the same 0.020 Ω segment, what is the modeled heating?

<details>
<summary>Reveal the worked answer</summary>

800 J, twice the 400 J result for 1,000 A over 20 ms.

Doubling current multiplies I² by four; halving time divides by two. Net heating doubles: 2,000² × 0.020 × 0.010 = 800 J.

</details>

**The idea to keep:** Protection must match the actual sources, fault paths, stored energy, earthing arrangement, and loads that need to remain supported.

## Sources

- [Schneider Electric — Coordination between circuit-breakers](https://www.electrical-installation.org/enwiki/Coordination_between_circuit-breakers) — www.electrical-installation.org · Reviewed 2026-09-06. Protection selectivity depends on fault conditions and the available supply source.
- [ABB — Protection Devices for Direct Current Applications](https://library.e.abb.com/public/5cd83dcb95a74dcdb571be5f256e1af8/9AKK108470A9606_en_B_Protection%20Devices%20for%20Direct%20Current%20Applications%20-%20Technical%20Application%20Paper.pdf) — library.e.abb.com · Reviewed 2026-09-06. DC interruption and converter-fed fault behavior depend on circuit dynamics and device capabilities.
- [Schneider Electric — Definition of standardised earthing schemes](https://www.electrical-installation.org/enwiki/Definition_of_standardised_earthing_schemes) — www.electrical-installation.org · Reviewed 2026-09-06. Earthing schemes distinguish the source-earth relationship from exposed-part protective connections.
- [OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) — openstax.org · Published 2016-10-06 · Reviewed 2026-09-06. The fixed-current resistive energy example follows I²R multiplied by time.
- [Schneider Electric — TN system: Principle](https://www.electrical-installation.org/enwiki/TN_system_-_Principle) — Schneider Electric · Reviewed 2026-09-13. In the TN arrangement, exposed conductive parts connect by protective conductors to the earthed source point; fault current returns through that loop.
- [ABB — Protection Devices for Direct Current Applications, 2025 technical paper](https://library.e.abb.com/public/4b22f4bae7e5424d9bf87039c3c1d0ba/9AKK108470A2501_Technical%20Application%20Paper_Protection%20Devices%20for%20Direct%20Current%20Applications.pdf) — ABB · Published 2025 · Reviewed 2026-09-13. Explains DC arc formation and conventional interruption, which must drive current to zero while managing circuit energy, alongside semiconductor, resonant and hybrid methods.
- [Schneider Electric — Elementary switching devices](https://www.electrical-installation.org/enwiki/Elementary_switching_devices) — Schneider Electric · Reviewed 2026-09-13. Distinguishes disconnection for isolation from load switching and fault interruption.
- [OpenStax — Energy Stored in Capacitors](https://openstax.org/books/college-physics-2e/pages/19-7-energy-stored-in-capacitors) — OpenStax, Rice University · Published 2022-07-13 · Reviewed 2026-09-14. A charged capacitor retains electrical energy even when the external supply is disconnected.
- [ABB — Protection criteria for medium voltage networks](https://library.e.abb.com/public/76afab5a1dd44f438409aa65c990ed8b/AP_Protection%20criteria%20MV(EN)C-_1VCP000280-01.2017.pdf) — ABB · Published 2017 · Reviewed 2026-09-26. The protection trip current must always be lower than the minimum short-circuit current at the point of connection; a relay set above the available fault current does not protect the plant.
- [Schneider Electric — Easy UPS 3-Phase Modular specifications](https://productinfo.se.com/easyups3pmodular/viewer?docidentity=REF_Specifications-B929255A&lang=en&extension=xml&manualidentity=TechnicalSpecificationsEasyUPS3-Pha-BC29F805) — Schneider Electric · Reviewed 2026-09-26. The 50 kW configuration’s nominal output current is 73 A at 400 V, and its inverter output short-circuit current is 160 A for 220 ms.
- [ABB — Technical Application Papers No. 2: MV/LV transformer substations, theory and examples of short-circuit calculation (February 2008)](https://library.e.abb.com/public/2c522f583c884a4fbdf3968e1fdf1481/1SDC007101G0202.pdf) — ABB · Published 2008-02 · Reviewed 2026-09-26. An 800 kVA transformer with 5% short-circuit voltage has about 1,155 A of rated current at 400 V and feeds about 23 kA into a three-phase secondary fault, about 20 times rated; generator subtransient reactances are about 10–20% (smooth rotor) and 15–30% (salient pole).

## Check your understanding: Maintenance, then another loss

Pause and make a prediction, then compare your reasoning.

Three hypothetical UPS modules can each deliver 1 MW to a common output serving 1.8 MW, including all protected auxiliaries. One module is isolated for maintenance; another then fails. Assume the surviving output path remains connected and has enough stored energy for the required bridge interval.

**Pause and predict:** Can the full load remain supported? Explain which limit matters now.

<details>
<summary>Compare your reasoning</summary>

No. Only 1 MW remains available for a 1.8 MW load, leaving a 0.8 MW power shortfall.

With one module unavailable, the two remaining modules supplied 2 MW. Losing another removes that margin and more. Enough stored energy cannot overcome an output-power limit; preserving a smaller service would require a pre-established way to reduce the supported load.

</details>

**The next problem:** Carry those power, energy and failure boundaries into the rack. Where do its watts go between the inlet and the chips, and what covers a sudden step in its load?

Continue in **8. Rack power and buffering**: Follow the watts through the rack.
