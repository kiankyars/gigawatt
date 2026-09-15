# Feedback audit — 13 September 2026

This audit checks the requests visible in this task against current source and
Git history. Requests made on the other computer are checked against their
repository records; those records do not substitute for the original message.
The prior “everything addressed” claim was too strong. This page foregrounds
exceptions; the coverage list below makes the rest inspectable.

## Chapter 6 final review — 14 September 2026

**Accepted after these edits, as requested.** The deck now has 21 slides;
existing scene links remain stable.

- Slide 8: title now identifies Siemens's switchgear/transformer skids as being
  for Compass **data centers**, verified in Siemens's December 2024 announcement.
- Slide 12: floor PDU caption now says **Distributes to feeders**; removed
  **Transformer optional**. Rack PDU and server PSU panels retained.
- Replaced the switchgear figure with the supplied labeled image. Corrected
  three leader endpoints against Siemens's catalog: breaker, earthing switch
  and cable connection. Supplied originals and edit provenance are retained.
- Added the supplied apparent-power/PF image immediately before former slide
  17. Its arithmetic is correct. Corrected two definitions to distinguish PF
  from conversion efficiency. **Clarification:** the supplied image does not
  depict reactive power; the scene and reader explain its sinusoidal 675 kvar
  relationship without adding another on-slide paragraph.
- Former slide 19, now 20: **Upstream backup opens when the feeder breaker
  fails to open.** The failed feeder breaker stays closed; the separate incoming
  breaker opens and removes both halls' supply.

No unresolved content instruction in this pass. Fresh browser interaction and
whole-page layout QA remains a technical follow-up; source, arithmetic,
diagram/image and automated checks are recorded in [TESTING.md](TESTING.md#chapter-6-final-review--2026-09-14).

## Chapter 6 voltages and instrument transformers — 14 September 2026

- Campus path now uses **345 kV → 34.5 kV → 480 V**. Mortenson identifies
  Abilene's 345 kV expansion separately from its initial 138 kV phase; the
  Longhorn review drawing labels a 34.5 kV Lancium feed. These support the
  voltage references, not a complete as-built transformer schedule. The 480 V
  building stage is a teaching example. Updated the transformer-location image,
  current calculation and reader consistently: 2 MW at 34.5 kV gives 33.5 A.
- Slide 5 now names the **current transformer (CT)** and adds a fourth view,
  **CT + CVT at 345 kV**, with current and voltage measurements feeding the relay.
  The CVT branches from phase to earth. It is an HV teaching example, not a claim
  about installed Abilene equipment or a CVT requirement on each MV feeder.
- Slide 6 now says **Air gap**. The component introductions belong to Chapter 6
  slides 4–7, not Chapter 5. Chapter 6's feeder-failure example and Chapter 7's
  fault isolation, grounding and interruption sequence extend that teaching.
  CT/CVT roles are now introduced; detailed instrument sizing, saturation and
  transient response are outside the current teaching scope.

All requested edits in this pass are implemented. **Verification follow-up:**
operate the new slide 5 view in the built-in browser when its control tool is
available again. Desktop/phone SVG renders and automated checks are recorded in
[TESTING.md](TESTING.md#chapter-6-abilene-voltages-and-instrument-transformers--2026-09-14).
Chapter acceptance was subsequently recorded in the final review above.

## Chapter 5 drainage and expansion check — 14 September 2026

- Slides 1–4: positive review; preserved the visuals. Slide 4's notes now
  distinguish stormwater drainage from the closed cooling loop.
- Slide 5: removed “Deeds · mineral leases · surface-use agreements” at the bottom.
- Slide 10: rechecked Equinix's own employee account. Staff did pump water out
  while keeping power on; the existing claim needs no correction.
- Slide 19: removed the land-rights condition, shaded corridor strip and outer
  panel. The problem now shows only the live hall, excavation and existing road
  and fiber. The reveal adds alternative routes and three steps: build, test and
  switch, then excavate. “Copyright rights” was a misreading/dictation of
  “corridor rights”—permission to use the route's land.

No new unresolved instruction from this pass. Whole-chapter acceptance remains pending.

## Chapter 4 final review and Chapter 3 opener — 14 September 2026

Chapter 3's original MODEL STATE / SERVING USERS / ELECTRICAL DEMAND text is
restored on slide 1 alongside the supplied Jensen Huang image; 17 slides remain.
Chapter 4 is **accepted after the requested changes**:

- Simplified WHEN and WHAT; preserved HOW. “Generation duty” means everyday
  supply, peaks or backup. Energy Transfer is the company, now labeled as the
  gas supplier to Oracle.
- Moved Abilene's delivery slide immediately after CoreWeave's delivery slide.
  The later slide numbers and all existing hashes remain stable.
- Removed slide 6's subtitle and slides 7–10's extra headings and captions;
  enlarged the four configuration images and retained their two key lines.
- Dania Beach displays **up to 1.26 GW**; removed the model-rating sentence.
  Retitled the single-cycle, three meanings of fast and xAI procurement slides.
  Removed the parallel-feeder sentence from the current comparison.

The 40% / 60% question was withdrawn once Kian identified fuel efficiency;
that calculation remains unchanged. “Grid type” was dictation for **grid tie**.
The xAI procurement account remains sourced to Southaven/MiniHard; it is not
new evidence about the original Electrolux conversion. No implementation ambiguity
remains from this pass. Existing research follow-ups remain in the tracker.

## Chapter 6 follow-up review — 14 September 2026

| Request | Implemented |
| --- | --- |
| Abilene photograph adds no teaching value | Removed the standalone slide; its old URL opens the complete campus path. |
| Trace the load through high-voltage AC | Added the two-stage campus path. The later Abilene-reference review updates its values to 345 kV grid → campus transformer → 34.5 kV switchgear → hall transformer → 480 V building branches. |
| Explain the single-line convention through an example; trim N/PE prose | The same switchboard-to-rack-PDU circuit appears as one line and five separate conductors. Removed the explanatory legend. Kept the correct **480Y/277 V**, rather than the requested inconsistent 400Y/277 V. |
| Use real manufacturer switchgear anatomy | Original Siemens NXAirS section with four compartment callouts; up-to-12-kV family identified separately from the campus model. |
| Teach disconnectors and surge arresters in context | Two full source-to-hall circuit views: series isolation gap, then parallel arrester-to-earth path. |
| State who supplies the Compass package | Visible title identifies Siemens as supplier and Compass as customer/co-developer. |
| Stop implying every floor PDU converts 480 V to 208 V | GPT image edit removes fixed voltages; floor transformer is optional. Reader adds Schneider's 480-to-400/415 V counterexample. |
| Introduce busway before tap-offs | New GPT-generated overhead busway illustration precedes the actual tap-off close-up. |
| Remove gray power-factor subtitles | Kept the transformer rating, equation and live quantities; removed the gray assumptions paragraphs from the slide. |
| Motivate single-phase PSU allocations | Shows six labeled PSU groups connected between phases and neutral. Controls say “Spread across phases” and “Crowded onto L1.” |
| Replace the failed-interruption slide | Two halls share an incoming breaker. Operate upstream backup after a feeder breaker fails and observe the affected load paths. Removed the multiple-choice/reasoning interface. |
| Clarify the Chapter 7 segue | Final title explicitly introduces continuity for racks and cooling; shared footer advances to Chapter 7. |

The revised deck has **19 slides**. Implementation and technical checks are complete;
author acceptance remains pending. This record covers the visible follow-up request,
not unseen feedback from another task or computer.

## Fairwater slide and independent request check

The requested **four-nines availability at three-nines cost** case already has
its own [Fairwater Atlanta slide](prototypes/ups-format.html?teach=1#tier-investment).
It shows Microsoft's campus photograph, the availability/cost claim and the
traditional GPU backup equipment Microsoft says it can omit. The slide was added
in `79a5ec6`; it is not merely a source note. Microsoft's original
[November 2025 article](https://blogs.microsoft.com/blog/2025/11/12/infinite-scale-the-architecture-behind-the-azure-ai-superfactory/)
was rechecked on 13 September. This is Microsoft's design-capability claim;
the article supplies no measured annual outage record or quantified cost model.
The live `/slides/ups.html?teach=1#tier-investment` page was also checked in the
built-in browser: Fairwater is slide **21 of 22**, with the comparison visible
without opening notes or following a source link.

An independent source audit checked earlier requests against active scene
definitions, renderers, source notes and the tables in COURSE_REVIEW.md. It found
the missing transformer operating-range treatment, unbuilt companion inventory
and a product-photo gap, now closed by the additions recorded below. Historical Chapter 3 rows have been reconciled
with their replacements. This source audit does not establish fresh visual QA,
whole-course completeness or author acceptance. Chapters 4–5 remain with their
current authoring agent. Kian clarified that Chapters 6, 7 and 8 must remain
separate. **Ownership is split:** the Chapter 5 task owns the separate Chapter 6
deck; the other Astra / Ultra assignment focuses on Chapters 7 and 8. Chapter 7 retains
`tier-investment`. For Chapter 8, append **rack-to-chip then 800 V DC** into one
presentation. They are distinct sequences, not duplicated content; preserve both
sets of slides and unify navigation rather than deleting or rewriting them.

## Missing, partial or uncertain

| Feedback | Current finding and next action |
| --- | --- |
| Evolving functional bill of materials and service-path companion | **Unbuilt.** The commitment existed only in COURSE_REVIEW.md prose. Build the persistent component inventory and connect it to the facility map and lesson changes; isolated diagrams do not fulfill this request. |
| Teach **interactivity** as the central inference metric | **Missed in the previous release.** The fixed 4,000-token/s budget was arbitrary and slide 3 did not teach interactivity. Revised slide 3 defines tokens/s/user; the next slide reads NVIDIA’s actual GB300 throughput/interactivity curve. Exact supported-session selection remains **open** because this source has no concurrency table; a fixed total divided by user speed is not an adequate substitute. |
| Active check-in in every domain | **Not complete in the teaching material.** Fifteen reader checks exist. Latest clarification: make an active check-in the default in each domain; use a strong example only if no worthwhile check can be made. Chapters 3, 5 and 6 now include service, replacement-plan and distribution-capacity checks; audit the remaining decks and record any specific exception. |
| Teach D13 site-built versus prefab/modular; fixed 20 MW late rack change | **Reader complete; deck unbuilt.** The reader covers EPC duties, factory/site work, parallel schedules, design freezes, transport and interface owners; the exercise covers electrical, hydraulic, spatial and schedule holds and release evidence. Chapter 14 in the numbered course still needs its own teaching sequence. |
| Teach Crusoe’s solar/battery case in context | **Integrated.** `continuity-format.html#sparks-storage` includes the site photograph, 12 MW solar / 63 MWh battery account and 5.25-hour conditional calculation; the nines scene retains the separate availability claim. |
| Other requested cases in their relevant chapters | Google flexible scheduling is integrated in Chapter 11 at `google-demand-response` and `deadline-scheduling`. Abilene’s capacity ledger remains pending integration. Abilene cooling appears in the physical-site deck, but not yet in the cooling deck. These are separate from already integrated Colossus brownfield and Southaven procurement cases. |
| Abilene as the recurring campus throughout | Policy and several cases are implemented. A whole-course consistency pass is still open; no complete as-built campus model is claimed. |
| Approximately 20-minute primer | Slides exist; actual spoken runtime and beginner comprehension have not been established. No precise rehearsal cues are being restored. |
| Remove repeated disclaimer/subtitle clutter everywhere | The latest sweep removed many visible footers. **Not certified exhaustive:** UPS still uses “Ideal DC-bus example”; other notes use similar boilerplate. Further cleanup must distinguish generic disclaimers from inputs, figure credits and named-project status. |
| Transformer input-range explanation | **Implemented.** Primer `transformer-operating-range` follows the tap mechanism with Schneider Phaseo ABL6TS25B: 250 VA controls transformer, 360–440 V on its 400 V connection, 47–63 Hz (P159). Published input limits remain distinct from compensation taps, output regulation and dielectric tests. |
| Simplify access to available presentations | Directory and duplicate footer were consolidated. The two rack-power decks still had identical visible “Open slides” labels; corrected to their distinct titles. The old audit’s “Slides available filter” claim was stale: a later recorded request deliberately removed that filter. |
| Requested Astro 6 Ultra agents and Chrome-for-Testing removal | Earlier audit records both as completed. Current code/Git alone cannot freshly establish the historical agent configuration or the notification state on the original Mac. Built-in-browser-only testing remains the rule; this audit is not a new malware scan of that other computer. |

These open production tasks are also owned by [Course review](COURSE_REVIEW.md#next-teaching-step)
and the [case handoffs](TEACHING_STANDARD.md#required-section-handoffs).

## Chapter 6 assignment

A separate GPT-6 Astra / Ultra agent authored Chapter 6 with three source-backed
case studies, real photographs and an active capacity check-in. It has its own
numbered course-directory entry. Chapter 7 and Chapter 8 remain separate.

## Latest Chapter 5 review

Implemented the requested replacements and removals in the 20-scene deck,
including QTS **Suwanee**, Georgia, and the hot-swap follow-up. The liked opening
three scenes and rack/tray handling examples remain unchanged.

Only two research limits remain: no verified data-center redesign or quantified
delay specifically caused by severed mineral rights, and no verified flooded-bridge
case or HO1 flood photograph. TCDC's dated surface-waiver milestone and Equinix's
actual Harvey access interruption supply the concrete examples instead. Getty's
judgment is explicitly an agricultural case. No clarification is needed for
“Sawani”: the existing campus was QTS Suwanee.

## Latest Chapter 4 review

All six comments are implemented: October-published CoreWeave aerials, explicit
Energy Transfer-to-Oracle gas delivery, Campus A/B layout, Abilene capacity scope,
Dania Beach cycle/model labels and Southaven’s state-line explanation.

Two evidence limits remain: the aerials’ exact capture days are unknown, and
Oracle’s September percentage does not define current operating MW. The slide
shows 900 MW only as 75% of the separately reported 1,200 MW plan, conditional
on the same capacity basis. The 10 GW commitment is for the wider Stargate buildout.

## Wording and identity questions consolidated

- **Interactivity:** now explicitly tokens per second per user during generation.
  Initial waiting time is TTFT, a separate metric. The earlier arithmetic edit
  failed to teach the intended concept; this was our miss, not poor dictation.
- **Chapter/slide numbers:** Chapter 3 originally had 18 slides; later edits shifted
  positions. Requests are matched by quoted content and stable scene IDs, not by
  carrying old numbers forward. Interactivity is now deliberately slide 3.
- **Abbeleen → Abilene, Texas**; original **Colossus** means the former Electrolux
  factory in Memphis, Tennessee. Southaven/MiniHard, Mississippi, owns the
  SemiAnalysis high-voltage-procurement account. These identities were clarified.
- **Crusoe solar:** Crusoe/Redwood in Sparks, Nevada, distinct from Abilene.
- **“Rock chips” → Groq LPUs**. NVIDIA’s LPX partner is Vera Rubin, not Blackwell;
  they are separate racks. The selected prefill/decode split is sourced.
- **“S+1” → N+1:** retain the definition and spare-module example; remove only the
  sentence promising a surviving-service test in a later chapter.
- **Primer “references”:** remove promises about later chapters; this did not mean
  banning citations. Explanation duplicates and precise rehearsal cues are removed.
- **Power factor:** hold supply voltage fixed; misaligned voltage/current can
  require more current for equal real power. Three-phase power is the simultaneous
  sum, not a selector that follows the highest voltage wave.
- **Transformer range:** fixed-ratio and tap mechanisms are implemented. The
  equipment's published operating range now follows the tap mechanism in the Primer.
- **Check-ins:** latest instruction supersedes the earlier broad permission to
  substitute closing examples. Default to one meaningful active check per domain.

## Other requests checked

- **PSU and BBU product photographs:** added dedicated `psu-hardware` and
  `bbu-hardware` scenes before their mechanism slides. Four unchanged manufacturer
  images show the Advanced Energy ORv3 PSU/power shelf and Delta BBU/battery shelf.
  Source notes and image hashes are recorded. Delta's 15 kW system rating remains
  distinct from the following ORv3 sum-of-module-capacity model. This closes the
  photo gap found in the audit; it does not certify the whole rack-power chapter.
- **Primer purpose and naming:** separate from historical introduction; substantive
  first circuit slide; no optional label, “Skip to D01,” future-chapter promises,
  closing reassurance quotation or empty final slide. Numbered descriptive titles
  start at 1. Primer; technical IDs and old URLs remain stable.
- **Primer electricity:** watts means energy per second; heat label moved below
  arrows; initially flat DC; polarity and visible terminals; square/sawtooth/triangle
  follow-up; voltage variation separate; predominant three-phase stated; total
  three-phase power summed; dedicated waveform-motivated PF slide.
- **Primer equipment and flow:** transformer/rectifier/inverter/PSU and UPS retained;
  online/offline follow-up includes familiar applications; N+1 retained. The same
  server/model connects hardware, memory, intra-data-center networking, running
  GPU heat, cold plate and CDU. PUE’s unwanted “useful work” footer is gone.
  One stale watts sentence in author notes was found and corrected during this audit.
- **Course/navigation:** greenfield/brownfield and Colossus are in Chapter 5;
  SemiAnalysis’s procurement rationale is in Chapter 4. Historical introduction
  redirects; duplicate footer retired; chapter directory exposes available decks;
  Back to course is visible; workload-to-overview detour removed; slides have no
  Explanation/source-dialog launchers. Reader and teaching material are distinct.
- **Latest workload pass:** obvious GPU-count sentence and redundant training title
  removed; slides 4–6 memory arithmetic verified; prefill/decode bottlenecks taught;
  LPX image and handoff added; continuous-batching transition improved and wall-clock
  caveat removed; energy uses 10/15 minutes without break-even caption; power-trace
  caveats removed; staggering fixed 15 seconds; three flagged ending scenes retired;
  preferred final visual retained. Interactivity was the significant missed item
  and is separately accounted for above.
- **Publication:** the previous revision was pushed and its live files verified.
  This revision’s local validation is recorded in [Testing](TESTING.md). Push and
  live verification are reported with the release; technical checks do not mean
  the creator accepted the teaching quality.

## Chapter 6 review — 13 September 2026

Every original slide number below refers to the reviewed 30-slide release. Revised Chapter 6 has 18 slides; stable removed-scene links resolve to their replacement or Chapter 8.

| Original slides / request | Disposition |
| --- | --- |
| 1: generated opening | New GPT image: campus connection → building transformer → row busway → rack. |
| 2–3: keep case and explain named equipment | Abilene photograph and branching campus path retained; new switchgear anatomy and relay/breaker sequence provide the missing mechanism. |
| 4: N, PE, 480Y/277 | Visible definitions: neutral, protective earth, wye, phase-to-phase and phase-to-neutral voltage. Removed the criticized PE sentence. |
| 5: redundant open/closed switch | Removed; replaced with sensor → relay command → breaker interruption, including a failed-interruption check. |
| 6: motivate Compass skid | Compare separate equipment/site connections with one transportable package; do not claim two racks become one rack. |
| 7: transformers and SST | Generic turns-ratio repetition removed. Primer owns ratio/taps and the real controls-transformer input range; Chapter 8 owns SST and rectification architecture. |
| 8: overflowing transformer-location diagram; four attachments | Replaced with GPT two-route image. First attachment has correct arithmetic; other versions contain contradictory recommendations/current labels and were not used unchanged. |
| 9: AC auxiliaries | Retained building branch diagram here to establish the AC load paths before Chapter 8 changes the IT supply architecture. |
| 10: PDU/PSU distinction and generated figure | New GPT comparison: transformer-equipped floor PDU, AC rack PDU, AC/DC server PSU. Generic illustrative equipment, not manufacturer photographs. |
| 11–12: overhead circuits and tap-off introduction | Tap-off mechanism now precedes Fujitsu case. Circuits means protected rack-supply branches, not PSUs. Benefits: adaptable branches, local metering, unobstructed floor cooling route. |
| 13 and 21: tap-off/growth consolidation | Retain one interactive shared-bus current example; remove separate reserve-percentage slide. |
| 14–15: meter and backward loss arithmetic | Remove repeated standalone slides; reference accounting remains in reader and earlier/later appropriate chapters. |
| 16–18: power factor | One fixed-900-kW example shows kVA and conductor current as PF changes. kVA retained because it is the transformer-rating unit; converter efficiency arithmetic removed. |
| 19: phase overload | Rebuilt around six visible single-phase PSU groups and their phase-to-neutral connections. Equinix P163 confirms phase balancing is a real rack-installation concern. |
| 20: repeated current/heat equation | Removed standalone slide. Correction: conductor heat is I²R; voltage drop is IR; real DC power is VI. |
| 22–26: repeated DC/conversion sequence | Cut duplicates; preserve unique Green Zurich-West case in Chapter 8 (`green-zurich-west`), including historical 380 V / open-circuit 400 V distinction. |
| 27–29: repeated threshold comparisons | Removed. New check asks why a trip command with continuing fault current indicates failed interruption and what broader outage backup protection can cause. |
| 30: generated transition | New GPT figure shows common-feeder interruption affecting racks and cooling/controls. |
| Device deep dives | Chapter 6: switchgear assembly, sensors, relay, breaker, disconnector, surge arrester and distribution. Chapter 7: fault domains, grounding, continuity. Chapter 8: rack conversion, SST and 800 V. Hardware-operating/design calculations beyond those declared examples are not claimed complete. |


## Chapter 5 context and ending — 13 September 2026

- Original slides 8 and 9 each become context → engineering pairs: Docklands
  setting/groundworks at 8–9, Harvey context/HO1 response at 10–11. Both liked
  engineering slides are preserved. New images are credited primary-source assets.
- Original slide 19 becomes an interactive comparison of two exit-route layouts:
  one blocked corridor removes both shared routes but leaves the independent
  alternative connected. New position 21; `fire-and-egress` link retained.
- Original slide 20 now has two concise cards. Show reasoning replaces the
  questions with answers; it does not add another wall of text. New position 22;
  `service-check` link retained.
- The user's reference to Chapter 15 was interpreted as Chapter 5 because the
  active deck and the two described slides match its original positions 19–20.
- Sources P165–P167 are in the existing library and reading. No claim of a
  photographed HO1 access route, completed ADA construction or compliant egress
  design is made. Author acceptance remains pending.

## Chapter 7 review — 14 September 2026

The active deck is `continuity-format.html` (public `/slides/continuity.html`).
This pass implements the author's latest numbered review; scene hashes remain stable
where a scene was revised. Thirty scenes now include four new teaching steps.

| Request | Disposition |
| --- | --- |
| Literal chapter title; remove opening bottom prose | `campus` has **Continuity, storage and protection** and its establishing image only. |
| Restore UPS dimensions, rating, identify pictured cabinets | `equipment`: Schneider 50–250 kW; 1.991 m H × 0.600 m W × 0.850 m D. Black/white finishes of the same family; exact photo configurations remain unidentified in research notes. P26 and P168 checked. |
| Explain local DC; external batteries; UPS contents | `equipment` spells out direct current backup at the rack, separate external batteries, rectifier/link/inverter, battery interface, bypass, controls and cooling. The battery interface is explained as conversion/control, not a simple connector, in the reader. |
| Derive capacitor formula before substituting; remove garbled expression | New `capacitor-energy` derives E = ½CV² from the voltage–charge area. `capacitors` calculates usable 15 kJ and 15 ms with visible inputs. |
| Derive the 10 ms ramp | New `battery-ramp`: triangle area = 5 kJ; rearranging the energy equation gives 768.1 V. No postponed battery handoff. |
| Motivate 1.10 MW versus 1.05 MW | `dc-link-recovery` compares both with 1.00 MW simultaneously. Extra power = missing 5 kJ / recovery time; 50 kW gives 100 ms, 100 kW gives 50 ms. |
| Clarify storage output limit | `storage-limits` fixes demand at 6 MW and compares 8/4 MW delivery limits with the same usable energy. Shortfall and supported duration remain separate. |
| Replace solar/battery slogan; calculate 63/12 | `sparks-storage` uses a plain site title and shows **5.25 hours at a constant 12 MW load using 63 MWh**. The diagram labels 12 MW as solar. This ratio is not a minimum site runtime because solar rating is not a verified maximum served load. P169 added. |
| Remove abstract protection steps | Removed Detect/Identify/Interrupt strip from `fault-isolation`. |
| Shared bus fails even with upstream contacts closed | `fault-isolation` now shows fault before clearing and after upstream clearing. Both lose all load groups; clearing removes supply to the fault without repairing the bus. |
| Define bonding/impedance; distinguish arrester; remove TN-S subtitle | `grounding` draws the complete return loop and defines protective bonding, PE and loop impedance at use. Arrester distinction is directly explained in the reader; old subtitle removed. |
| AC/DC interruption example; 800 V relevance; remove ending prose | `ac-dc-interruption` compares contacts closed, separating with an arc, and current interrupted. New `dc-feeder-protection` applies conventional arc-chamber interruption to an 800 V feeder, cable inductance, capacitor and fault. ABB P170 supports mechanism. |
| Introduce Tier pyramid first | New `tier-overview` precedes Tier outcomes. Original accessible pyramid from Uptime definitions: no official pyramid found; third-party pyramids tying tiers to fixed percentages were rejected. |
| Remove mathematical-reference section and repeated disclaimers | Removed availability mathematical-reference footer, old capacitor/recovery contexts and recurring generic caveats from the revised material. Inputs and essential figure credits remain. Source limitations stay in research/reader. |
| Put Tier/availability distinction only with nines | Nines slide: “These times do not directly correspond to a Tier.” Fairwater certification footer removed. |
| Confirm Fairwater utility-resilience interpretation | Microsoft primary article confirms four-nines capability at three-nines cost, with GPU-fleet generators/UPS/dual-corded distribution omitted. Does not imply every campus load has no backup. |
| Mundane closing title; clear scenario/discussion/answer | `service-check`: **Chapter 7 knowledge check**. One high-contrast scenario, an equipment/supply table, and a single question. Answer replaces question; repaired controls lead to the cooling-restart consequence. |
| Audit other slogans, especially upcoming material | Checked active scene titles and boundary subtitles. Chapter 8 rack-to-chip opening, locality, recharge, rack-input account and sidecar titles made direct; repeated model disclaimers trimmed while relevant quantities remain. This is not acceptance of unbuilt chapters. |

Validation and publication evidence are recorded in TESTING.md. This is feedback
implemented, not a claim of final author acceptance.

## Chapter 9 creation — 14 September 2026

Request: create the highest-quality Chapter 9 presentation while applying the accumulated course feedback.

| Inherited requirement | Implemented location |
| --- | --- |
| One coherent section with a literal chapter opening | `compute-purpose`; rack → tray → GPU/memory → performance → job recovery |
| Real equipment on the slide | `rack`, `tray`, `superchip`, `rack-interfaces`, `tray-repair`; byte-preserved manufacturer assets |
| Actually use GPT ImageGen and inspect the result | Two new workspace assets with saved prompts; scale illustration and HBM cutaway. Product identity uses manufacturer pictures. |
| First principles before the numbers | `capacity-bandwidth`, `weight-read`, `operand-reuse`, `peak-flops`, `operation-bounds`; FLOP definition precedes rate calculations |
| Sparse labels, no speaker scripts or source popup | One header; essential diagram labels; supporting prose/citations in the three D07 reader lessons |
| A controlled comparison and useful interaction | `roofline`; simultaneous concentrated/dispersed fault layouts with 8-GPU and 4-GPU allocation modes |
| Avoid invented performance and failure guarantees | Product maxima are separate from stated operation rates; 18 ms is a memory-read bound; allocation groups have explicit job rules |
| Meaningful active check-in | `diagnose-upgrade` chooses between compute throughput, HBM rate and HBM capacity for the same supplied kernel |
| Shared controls, device theme, mobile layout | Existing `slide-chrome.js` / `slide-navigation.js`; first/last/selector controls and automatic device colors; narrower diagrams reflow |
| One owner for review state | Chapter 9 row in COURSE_REVIEW.md; technical checks do not mark Kian's review accepted |

The source review found different NVIDIA/Lenovo memory-bandwidth values and a
conflicting HBM-stack endnote. The deck uses NVIDIA's up-to-8-TB/s platform figure,
omits a fixed stack count and does not treat aggregate coherent memory as one
uniform-bandwidth pool. The visual pass corrected the initial roofline axis/path
mismatch, the NVSwitch enclosure boundary, the weight-vector dimensions and the
interposer callout before publication.


## Chapters 4–5 review and shared handoff — 14 September 2026

| Request | Resolution |
| --- | --- |
| Clarify MZX and put the state boundary on the actual site slide | `southaven-plan` combines Census-registered geographic context and original permit plan. MZX is the applicant; Trinity Consultants is the consultant. The separate border slide is removed; its hash redirects. |
| Remove Odessa subtitle; judge Getty relevance | Subtitle removed. Getty remains in the reading as background to surface rights, with no standalone presentation detour. |
| Add SemiAnalysis’s Texas chart beside Odessa | Original chart embedded unchanged. Its 17 GW is booked onsite generation at named Texas sites, not a count of data centers; 29 GW without a chosen site remains visible. |
| Merge QTS context and entrance diagrams | One slide contains the original campus plan and shared-entry counterexample beside three-entry DC1 topology. DC2’s four proposed entrances are distinct in the reader. Exact cable geometry is not invented. |
| Clarify cooling’s role and makeup water | Chapter 5 is the siting preview. Title links design to climate/water; replacement-water meaning is explained in the reader and slide label. The cooling sequence retains the deeper mechanisms. |
| Remove hot-swap conclusions and exit-corridor slide | Both repeated conclusions removed; egress slide removed and old hash redirects to the new check. |
| Better knowledge check | Live Hall A, Hall B excavation and an unresolved alternate corridor: sequence rights, alternate access and tested fiber, transfer, then excavation. |
| Automatic final-slide chapter jump | Shared footer uses generated teaching-catalog order. Bespoke workload/siting/continuity links removed. No chapter skips when slides are missing: the next chapter’s reading opens. |

Visual and behavior validation is recorded in TESTING.md. These are revisions awaiting author review, not a claim of acceptance.


## Chapter 7 capacitance follow-up — 14 September 2026

| Request | Resolution |
| --- | --- |
| Clarify Q = CV and its difference from P = IV | New `capacitance` scene introduces C = 0.20 F as 0.20 coulomb per volt, then shows Q = 0.20 × 800 = 160 coulombs. The reader distinguishes stored charge from charge per second and stored energy from power. |
| Explain substitution into E = QV/2 without calculus | `capacitor-energy` shows voltage rising linearly with charge: average 400 V, 160 coulombs × 400 V = 64 kJ, then E = Q × V/2 = (C × V) × V/2 = ½CV². No derivatives, differentials or integrals. |
| Start the next unmade chapter | Chapter 10, Networking and interconnects, assigned to an independent agent. Chapter 9 already has its own checked deck. Completion state belongs in the existing tracker. |
| Recall chapters both improved and reviewed | Refreshed the single chapter tracker in COURSE_REVIEW.md. Feedback/revisions exist for Chapters 1–8 and the selected Chapter 12–13 cooling sequence; Chapter 9 awaits first author review. Final whole-chapter acceptance is not inferred. |

The exact graph is code-rendered because the teaching depends on its slope,
triangle area and readable algebra. Existing generated spatial illustrations
are retained. OpenStax College Physics 2e §19.7 supports the algebraic derivation.


## Chapter 10 creation — 14 September 2026

The next previously unbuilt chapter is **Networking and interconnects (D08)**.
An independent authoring agent and source-review agent produced its 22-scene
presentation. Chapter 9 already existed; it was not rebuilt.

- Scope: network adapter and switch → copper/optical reach and CPO → shared
  fabric capacity → collectives and exposed communication → Meta fabrics and
  Google TPU v4 optical circuits → campus carrier handoff → link diagnosis.
- GPT ImageGen produced the spatial opening. Actual NVIDIA adapter/switch images
  and Google’s optical diagram provide the product/mechanism examples. Exact
  graphs, topology paths and state changes use authored HTML/SVG.
- The three D08 reader lessons now support the specific four-worker ring and
  sixteen-endpoint fabric examples. Six new primary references P182–P187 join
  the existing Meta, Google and NCCL sources without duplicate records.
- Common header/footer, device theme and automatic Chapter 9 → Chapter 10 →
  Chapter 11 handoff are registered through the existing teaching catalog.
- Review state stays in COURSE_REVIEW.md. Authored and checked is not author
  acceptance, and the older reviewed material does not need a general restart.

## Chapter 11 authoring — 14 September 2026

- Inspected upstream through `7377eef` before choosing the next missing chapter.
  Chapters 1–10 remain available for Kian's review; their slide content was not
  revised as part of this chapter.
- Authored a complete storage, orchestration and recovery sequence with explicit
  dataset/cache/checkpoint roles, metadata and payload constraints, coherent
  commits, asynchronous saves, recovery placement and tenant acceptance.
- Integrated the previously pending Google flexible-scheduling case, including
  the deadline and later-capacity consequences of a two-hour grid event.
- Named cases use original operator evidence: Meta RSC storage, Llama 3 recovery,
  Google's 2011 Gmail backup incident and its 2023 demand-response account.
  Real RSC and Google facility photographs have source records.
- The active diagnosis combines saved-state validity and feasible placement;
  correct output and full recovery time remain the acceptance criteria.
- The course directory and shared next-chapter navigation now reach Chapter 11.
  It leads to the existing Chapter 12 cooling material. Chapter 12 remains the
  next incomplete full-chapter deck.

Implementation checks are recorded in TESTING.md. First author review is pending;
this release does not establish spoken runtime or beginner comprehension.

## Chapters 1–3 review — 14 September 2026

Chapters 1–2 are accepted after these requested edits. Chapter 3 slides 1–6 are reviewed; review continues from slide 7.

- Primer: removed the entire two-terminal voltage subtitle; three-phase loads and single-phase PSU inputs clarified; tap teaching moved to Chapter 6; simpler voltage-range example follows the converter introduction. Added “(AC)” to power factor, removed the extra UPS example label, shortened the UPS comparison to “Online vs. Offline UPS” and removed duplicate link rates and the overhead disclaimer.
- Overview: identifies Gemini 1.0 Ultra as the largest model in Google’s original 2023 family; states that OCS mirror reconfiguration can bypass faulty interconnects.
- Workloads: supplied Jensen Huang image on slide 1 without new visible text; training compute labeled FLOPs; aggregate throughput separated from per-user latency. Removed the two subordinate interactivity statements and the two curve-reading text blocks. Slides 5–6 retained.
- Dictation resolved by context: “Jensen Wong” is Jensen Huang; “turning the power” identifies the primer’s model-data/network slide by its 10/100 Gb/s controls.
- The presenter request means a **separate presenter window**, confirmed explicitly; it must keep the next-slide preview off the audience page.

## Chapter 3 final review — 14 September 2026

Chapter 3 is accepted after the requested revisions; it now has 17 slides.
The former slide 18 remains the closing slide, now numbered 17.

- Presenter now shows only the upcoming slide across the separate window, for
  the second monitor. The original window shows the current slide.
- Slide 6 keeps only “Excludes block overhead” beneath its calculation.
  “Cache sharing” meant prefix caching; the reader now defines it explicitly.
- Slide 7 includes the supplied DeepSeek chart, checked against the original
  report and identified separately from the Llama calculation.
- Slide 8 retains “usually/often”: short prompts and large decode batches can
  change the limiting resource. The reader explains why.
- Slide 10 is titled “Batching,” with the generated bus above the diagrams.
  Slide 11 is titled “Interactivity isn’t the only important metric.”
- Slides 14–16 lose the redundant vertical-axis labels; slide 16 also loses
  “Independent jobs · phase durations unchanged.”
- The repetitive knowledge check is removed. Its old link resolves to the
  retained closing slide. The wording “remove it, then keep it” was understood
  as “remove it rather than keep it,” consistent with the stated objection.
- Chapter 8 already covers local capacitors/rack batteries, burst discharge and
  recharge. A sudden downward-step/source-surplus example is still missing and
  is recorded explicitly in COURSE_REVIEW.md's follow-up list.
