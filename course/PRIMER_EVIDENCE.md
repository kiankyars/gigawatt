# Primer evidence and teaching assumptions

Reviewed September 12, 2026. This is an author reference; it is not linked from
the primer or included in its teaching flow. The primer explains its concepts
without referring to other chapters.

| Concept | Evidence and scope |
| --- | --- |
| AC polarity and waveform shapes | [Tektronix, Oscilloscope Basics](https://www.tek.com/de/documents/primer/oscilloscope-basics) describes sine, square, triangle and sawtooth waveforms. The diagrams use original bipolar voltage traces. Approximate sinusoidal utility voltage is distinguished from other possible waveforms; unipolar ripple retains its DC polarity. Current reverses with voltage in the expressly stated resistor example. |
| Three-phase distribution | [Eaton, Cabinet and floor-standing PDUs](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/power-distribution-for-it-equipment/power-distribution-unit-faq/cabinet---floor-standing-pdu-solutions.html), opening comparison and phase-type table, describes three-phase distribution for large data centers. The primer identifies it as the usual distribution arrangement, while allowing single-phase and DC loads. It does not claim a measured market share. |
| Power factor | [Schneider Electric, Understanding True Power Factor](https://blog.se.com/energy-management-energy-efficiency/2020/02/20/distortion-displacement-and-the-truth-understanding-true-power-factor/) explains displacement between voltage and current, distortion from nonlinear loads, and real/apparent power. The diagram compares original single-phase sinusoidal examples at the same RMS voltage and 8 kW delivered. PF 1 has zero lag and relative RMS current 1; PF 0.8 has a lag of arccos(0.8) and relative RMS current 1.25. Voltage and current have separate plot scales, each held fixed across cases. The supply voltage has not fallen. The explanation introduces instantaneous voltage times current before the ratio. Distorted current can also lower true PF; phase displacement is not its only cause. |
| Offline and online UPS | [Eaton, Types of UPS systems](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/types-of-ups-systems.html) compares standby, line-interactive and online double-conversion paths and typical uses. The primer's two-path comparison is deliberately simplified; it does not imply those are the only topologies. The no-transfer-break statement concerns normal double-conversion operation changing to battery support, not bypass or every fault. |
| Medical example | [Eaton, Powering Healthcare Systems](https://www.eaton.com/us/en-us/products/backup-power-ups-surge-it-power-distribution/backup-power-ups/Safeguarding-power-equipment-in-the-healthcare-industry.html) describes online double-conversion protection in healthcare. This supports an example of sensitive medical systems, not a claim that every medical device uses or should use this topology. |
| Model loading | [NVIDIA, GPUDirect Storage Overview](https://docs.nvidia.com/gpudirect-storage/overview-guide/) distinguishes storage, host-memory buffering and direct transfers to GPU memory. The primer illustrates a conventional buffered loading path and explicitly notes that direct paths also exist. No transfer rate, model fit or universal hardware arrangement is inferred. |

The existing electrical, cooling and PUE source records remain in the research
library. The revised diagrams use original illustrative values, not equipment
ratings or measured campus conditions.

- **Model-loading sequence:** the same compute server and GPU recur from the
  rack view through memory, network and heat capture. A separate storage server
  supplies model data through the data-center network into host RAM, then GPU
  memory. The network timing covers only one chunk already buffered for sending,
  not disk reading or the complete model load.
- **Network example:** 8 decimal MB = 64 Mb. At ideal payload rates of 10 and
  100 Gb/s, serialization takes 6.4 and 0.64 ms. With fixed illustrative 10 µs
  first-bit path latency, last-bit arrival is 6.41 and 0.65 ms. This is a path
  between storage and compute servers within the data center, not a WAN example
  or measured equipment performance. Storage reads, host copies, queueing,
  protocol overhead and retransmissions are outside the calculation.
- **Heat example:** the running GPU receives 500 W of electrical power and, in
  this simplified steady state, transfers 500 W to its cold plate. Other paths
  and changes in stored energy are negligible. Heat crosses from the 70 °C GPU
  to a 45 °C cold plate;
  coolant enters at 30 °C and leaves at 35 °C. These stipulated temperatures and
  heat flow illustrate distinct quantities. They are not a prediction from
  temperature alone or a product rating.
- **Facility account:** PUE zooms out to all IT and its support equipment. The
  100 kWh IT plus 20 kWh support example is explicitly a new facility account,
  not energy attributed to the single 500 W GPU. Pumps and fans connect this
  account to the cooling diagram. The useful-computation distinction stays in
  [author background notes](PRIMER_NOTES.md); the unexplained bottom caption is removed.
- **Pacing:** exact slide timings and rehearsal cues have been removed. About
  twenty minutes remains the authoring target, to be assessed by teaching the
  material aloud and observing whether beginners follow it.
