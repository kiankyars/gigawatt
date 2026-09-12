# Primer evidence and teaching assumptions

Reviewed September 12, 2026. This is an author reference; it is not linked from
the primer or included in its teaching flow. The primer explains its concepts
without referring to other chapters.

| Concept | Evidence and scope |
| --- | --- |
| AC polarity and waveform shapes | [Tektronix, Oscilloscope Basics](https://www.tek.com/de/documents/primer/oscilloscope-basics) describes sine, square, triangle and sawtooth waveforms. The diagrams use original bipolar voltage traces. Approximate sinusoidal utility voltage is distinguished from other possible waveforms; unipolar ripple retains its DC polarity. Current reverses with voltage in the expressly stated resistor example. |
| Three-phase distribution | [Eaton, Cabinet and floor-standing PDUs](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/power-distribution-for-it-equipment/power-distribution-unit-faq/cabinet---floor-standing-pdu-solutions.html), opening comparison and phase-type table, describes three-phase distribution for large data centers. The primer identifies it as the usual distribution arrangement, while allowing single-phase and DC loads. It does not claim a measured market share. |
| Power factor | [Schneider Electric, Definition of Power Factor](https://www.electrical-installation.org/enwiki/Definition_of_Power_Factor), publisher-indexed definition, defines active power divided by apparent power. Direct page retrieval timed out. The 8 kW example is original: PF 1 gives 8 kVA; PF 0.8 gives 10 kVA. At fixed voltage and phase arrangement, RMS current is 25% greater. The difference is not 2 kW of heat or converter loss. |
| Offline and online UPS | [Eaton, Types of UPS systems](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/types-of-ups-systems.html) compares standby, line-interactive and online double-conversion paths and typical uses. The primer's two-path comparison is deliberately simplified; it does not imply those are the only topologies. The no-transfer-break statement concerns normal double-conversion operation changing to battery support, not bypass or every fault. |
| Medical example | [Eaton, Powering Healthcare Systems](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/Safeguarding-power-equipment-in-the-healthcare-industry.html) describes online double-conversion protection in healthcare. This supports an example of sensitive medical systems, not a claim that every medical device uses or should use this topology. |
| Model loading | [NVIDIA, GPUDirect Storage Overview](https://docs.nvidia.com/gpudirect-storage/overview-guide/) distinguishes storage, host-memory buffering and direct transfers to GPU memory. The primer illustrates a conventional buffered loading path and explicitly notes that direct paths also exist. No transfer rate, model fit or universal hardware arrangement is inferred. |

The existing electrical, cooling and PUE source records remain in the research
library. The revised diagrams use original illustrative values, not equipment
ratings or measured campus conditions.

- **Network example:** 8 decimal MB = 64 Mb. At ideal payload rates of 100 and
  1,000 Mb/s, serialization takes 640 and 64 ms. With fixed 20 ms first-bit travel
  time, last-bit arrival is 660 and 84 ms. Queueing, overhead and retransmissions
  are excluded.
- **Heat example:** a steady 500 W crosses from a 70 °C chip to a 45 °C cold plate;
  coolant enters at 30 °C and leaves at 35 °C. These stipulated temperatures and
  heat flow illustrate distinct quantities. They are not a prediction from
  temperature alone or a product rating.
- **Pacing:** cue durations are planning estimates. An aloud dry run is still
  required to establish runtime and whether beginners can follow the examples.
