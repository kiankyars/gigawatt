# Chapters 8–16: pre-recording audit

Reviewed 19 September 2026: **153 slides across all nine chapters**, their active source code, numerical models, speaker notes and supporting evidence. Baseline `81a700d`; the subsequent cooling-tower-fill clarification in `4f3e1ee` was also inspected. No course slides were edited by this audit.

**Verdict: no major technical or arithmetic error found. Address one evidence gap and three small wording ambiguities before recording. No chapter needs substantial reworking.**

| Priority | Exact location | Finding and smallest correction |
| --- | --- | --- |
| Evidence gap | **9 / 15 — The power stack**, `power-stack-overview`; [scene source](/Users/kian/Developer/gigawatt/course/prototypes/rack-energy-scenes.js:45) | The supplied image asserts **18.3–30 kW per PSU** and **25–40% fewer losses vs. silicon** without identifying products or comparison conditions. These are insufficiently scoped, not proven false. Remove those claims from the recap or attach specific product/comparison sources. Explain that SiC/GaN devices operate **inside converters**, rather than forming another mandatory serial conversion stage. The source caveat currently lives in notes, outside the recording view. |
| Clarification | **15 / 15 — Abilene: plan versus delivery**, `abilene-ledger`; [rendering source](/Users/kian/Developer/gigawatt/course/prototypes/capacity-visuals.js:13) | **75% of capacity delivered** appears in the **Six more buildings** row. Oracle means **total campus capacity**. Change to **Whole campus: 75% of total capacity delivered** or give it a separate row. Continue distinguishing construction completion from customer delivery. [Oracle](https://www.oracle.com/data-centers/) |
| Qualification | **11 / 1 — Why liquid**, `why-liquid`; [title source](/Users/kian/Developer/gigawatt/course/prototypes/cooling-scenes.js:7) | **Why Is Air Cooling Dead?** overstates the conclusion. Suggested title: **Why dense AI racks need liquid cooling**. Air still handles residual heat and other equipment; Lenovo’s GB300 example is approximately 90% liquid / 10% air. Later slides correctly preserve this distinction. [Lenovo](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai#cooling) |
| Qualification | **11 / 12 — CDU approach**, `approach`; [rendering source](/Users/kian/Developer/gigawatt/course/prototypes/cooling-foundations.js:443), also line 425 | Replace **The lower the approach, the better** with **A lower approach gives more coolant-temperature margin**. Achieving it depends on exchanger design and flow, with hydraulic and cost tradeoffs. [Vertiv application guide](https://www.vertiv.com/4945be/globalassets/shared/vertiv-coolchip-cdu-121-application-and-planning-guide-sl-802762.pdf) |

**Recording readability:** the small labels in **9 / 15 (power-stack map)** and **10 / 4 (Microsoft AI Superfactory infographic)** are difficult to read at 1280×720. Enlarge selected regions or simplify the figures if viewers need to read their details. This is a readability issue, not missing content. Chapter 14 / 6’s original Google plot is animated and draws over a four-second loop; its initially empty axes are intentional.

| Chapter | Slides | Main checks and result |
| --- | ---: | --- |
| 8 — Rack power and buffering | 18 | Rack hierarchy, PSU/BBU ratings, 93.05 kW input ledger, voltage drop, VRM waveforms, buffer and recharge arithmetic: consistent. Slide 2 is visibly an analyst forecast; its original publication date remains unknown. |
| 9 — 800 V DC | 15 | 480 V AC / 800 V DC currents, 28% conductor-loss reduction, conversion/isolation paths, Zurich history, protection and 253 kW retrofit requirement: consistent. Graphic caveat above. |
| 10 — Networking | 21 | Port counts, link examples, oversubscription, incast, 0.32 s transfer bound, 1 ms fiber round trip, Meta storage figures: consistent. |
| 11 — Heat capture | 18 | Thermal resistance, water balances, pump intersections, CDU ratings, redundancy and residual-air heat: consistent. Two wording changes above. |
| 12 — Heat rejection | 19 | Separate circuits, wet/dry temperatures, chiller/COP balances, heat reuse and Toronto incident: consistent. |
| 13 — EPC | 14 | Fixed-20 MW rack change, electrical/hydraulic limits, factory/site acceptance and phased delivery: consistent. |
| 14 — Operations | 23 | Row B/C balances, control delays, incident timelines and recovery statistics: consistent. Row C needs 109.81 kg/s, rounded to 110; that alone does not prove safe chip temperatures. |
| 15 — Economics | 15 | Revenue/occupancy, idle electricity, dated rental ranges and NVIDIA commitments: consistent. Abilene denominator clarification above. |
| 16 — Abilene synthesis | 10 | Workloads, bridge/backup role, cooling, manufacturing, company roles and financing boundaries: supported. Keep “greenwashing?” a discussion question; the source does not establish deception or a quantified cost comparison. |

**Validation:** all **80 Python and 303 JavaScript tests** passed, as did course, reader, domain-map and research freshness checks. Inspected every desktop slide; exercised **459 slide/layout combinations** (1280×720 light/dark, 390×844 light) and **59 button interactions**. No runtime errors, failed resources, horizontal page overflow or material visible clipping found. Geometry alerts were checked: intentional image crops and closed assumption panels were not defects. Expanded assumption panels and the Google animation were checked separately.

**Limits:** browser QA used local Chromium, not the actual recording application. Important empirical claims were checked against primary sources where available; this does not independently certify vendor statements. Houdini remains explicitly SemiAnalysis-reported. Supplied analyst graphics retain the evidence limits noted above. No audio or spoken rehearsal was performed.
