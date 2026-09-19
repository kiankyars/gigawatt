# Feedback audit — updated 18 September 2026

**Latest author acceptance — 17 September 2026:** Kian stated, “I approve up to chapters 13 at this point.”
Chapters 1–13 are accepted in the current numbering; Chapters 14–16 remain unaccepted.
The [chapter review tracker](COURSE_REVIEW.md#chapter-review-tracker) records this decision.
Earlier audit findings and separate research or enhancement follow-ups remain below.

This audit checks the requests visible in this task against current source and
Git history. Requests made on the other computer are checked against their
repository records; those records do not substitute for the original message.
The prior “everything addressed” claim was too strong. This page foregrounds
exceptions; the coverage list below makes the rest inspectable.

## Abilene course finale — 18 September 2026

Kian approved replacing the five separate hypothetical cases with a connected
final chapter and explicitly selected Abilene. **Putting an AI Factory Together**
is a nine-slide synthesis of the customer, equipment, facility, delivery and
commercial decisions. It is ready for author review, not author-accepted.

The former hot-weather comparison could make installed GPUs appear to vanish
when the supportable operating load fell; the standalone cooling-bottleneck
exercise repeated earlier teaching. Those views and the final rack-selection
and schedule-arithmetic quizzes are removed from the presentation. The five
C01–C05 reader exercises and their numerical models remain optional practice.
The stable deck route is unchanged, and retired slide fragments redirect into
the new sequence. No extra review of unchanged Chapters 1–13 is required.


## Current completion audit — 17 September 2026

An unqualified “everything in the conversation is complete” is **not established**.
This pass independently checked current Chapter 11–16 scene definitions and renderers
against the visible review requests. Chapter 11–12 served files were also checked
against source. Earlier chapter acceptance is preserved; it is not a new request-by-request
audit of all earlier work.

| Scope | Verified result | Remaining issue |
|---|---|---|
| Chapter 11 requested edits | Image placement, residual-air/RDHX path, immersion image, heat-flux/resistance definitions, ΔT, pump comparison, approach note, CDU labels, redundancy wording/default and merged failure response are implemented. | No missing explicit edit found. Latest follow-up restores the higher-resistance circuit curve alongside the fixed-speed pump and normal circuit: operating points are 2 L/s, 120 kPa and approximately 1.41 L/s, 140 kPa. More restriction reduces flow on the same pump; equations and explanation remain in the speaker notes. |
| Chapter 12 requested edits | Opening and captions, wet/dry definition, physical circuit walkthroughs, temperature-limit clarification, economizer order, COP comparison, removals, water/heat-reuse changes, meme and latest reorder are implemented. | Audit found that the moved closed-loop slide still defaulted to air and silently introduced a chiller. **Corrected:** it now opens on the wet-tower path and uses the preceding exchanger-only example. |
| Chapter 13 requested edits | EPC opening, contiguous rack-change case, supplied full-page prefab and Open Rack figures, three-row factory/site table, merged cooling test relocation, final quiz removal and reused CoreWeave photographs/milestones are implemented. | The retained rack-coverage intersection is still a possible editorial weak point; the specifically rejected closing quiz is removed. |
| Chapters 14–15 requested changes | Chapter 14 now makes the Row B chip-temperature violation explicit, keeps all four Google control diagrams together, adds the original cooling-performance plot, merges demand-response workload names and scheduling graphs, and removes the duplicate shared-maintenance slide. Requested case context, control-layer image, Meta figure, rental terms, bare metal/managed distinction, energy reimbursement and Abilene plan/delivery comparison remain present. | Current audit is source-based; it does not establish a new author acceptance of these chapters or a completed browser/test pass for the latest changes. |
| Whole-course removal of trivial exercises | Many explicitly rejected exercises are gone. The 18 September Chapter 16 revision removes `phase-choice` and `phase-schedule` from the presentation and replaces the five-case deck with one nine-slide Abilene synthesis. | Chapter 16 is rebuilt for author review; this closes those specific editorial gaps, not an unqualified whole-course completeness claim. |
| Earlier commitments | Transformer range, manufacturer PSU/BBU photographs and rack load-drop example exist. | The persistent inventory companion was removed from scope by Kian on 19 September. Sparks current load and exact inference concurrency remain unresolved evidence items. |
| Communication and status | This audit identifies actual content and distinguishes local preview from publication. | The adiabatic question was initially acted on without a clear answer; it has now been answered. Earlier audit rows contained stale completion states, corrected below. |

The subagent-process concern was waived by Kian on 17 September; it is not an open
content task. The current review runs on localhost 8877. No new public deployment
is implied. The chapter acceptance record remains in [COURSE_REVIEW.md](COURSE_REVIEW.md#chapter-review-tracker).

## Chapter 6 overview sequence and image review — 15 September 2026

All requests from this pass are implemented:

- Original slide 2 is preserved. New slide 3 outlines its MV switchgear; slide 4
  opens the switchgear. Slide 5 returns to the overview and outlines the 480 V
  conductor and building bus; slide 6 expands the physical conductors.
- Compass remains in Chapter 6, with a new co-design lead-in immediately before
  the factory case. Manufacturing, logistics and ownership are explicitly
  handed to the procurement/commissioning chapter in TEACHING_STANDARD.md.
- The supplied tap photograph has its own slide after the unchanged interactive
  turns-ratio example.
- Evaluated all four PF images; selected the clean two-column supplied image.
  The other two new figures incorrectly label reactive power as 225 or 450 kvar
  and visually imply scalar addition of P and Q. The sinusoidal value here is
  675 kvar. The previous image is correct but denser; it remains in the repository.

No unresolved instruction from this pass. New slide numbers reflect four added
slides; existing scene hashes are stable. Image provenance records the comparison.

## Chapter 7 review and Chapter 8 figures — 15 September 2026

The requested recovery derivation, storage arithmetic correction, stored-energy
isolation explanation, simpler fault/contact controls, two closing checks and
Microsoft quotation are implemented. The 800 V feeder is now in Chapter 8;
its old link redirects there. The supplied rack-density chart is Chapter 8 slide
2, and the power-stack image is its final recap. Chapter 5 now has separate
Meta Prometheus tents and Amazon Houdini factory-assembly cases, both with real
photographs. The user confirmed those identities and authorized the Chapter 6
single-line title change.

**Remaining uncertainty:** no current commissioned Sparks IT nameplate was
found. The revised example uses the reported **1 MW pilot from 2025**, with its
date visible; the current-load research item remains in [the tracker](COURSE_REVIEW.md).
The supplied BofA and Data Gravity/Wing figures retain their original attribution;
their publication URLs and individual forecast/market annotations were not verified.

**Clarifications incorporated:** the battery's 80% usable window is applied once;
AC current zero crossings help interrupt an arc but do not establish safe
isolation; generator startup and transfer can restore a failed-inverter bypass
supply but cannot bridge the interruption. Grounding remains because the metal
case needs a fault-current return path for automatic disconnection.

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

## Earlier commitments reconciled — 17 September 2026

| Feedback | Current finding and next action |
| --- | --- |
| Evolving functional bill of materials and service-path companion | **Removed from scope — 19 September 2026.** Kian confirmed this bill-of-materials companion is unnecessary. It was not built and is no longer an outstanding deliverable. |
| Teach **interactivity** as the central inference metric | **Missed in the previous release.** The fixed 4,000-token/s budget was arbitrary and slide 3 did not teach interactivity. Revised slide 3 defines tokens/s/user; the next slide reads NVIDIA’s actual GB300 throughput/interactivity curve. Exact supported-session selection remains **open** because this source has no concurrency table; a fixed total divided by user speed is not an adequate substitute. |
| Active check-in in every domain | **Later explicit removals take precedence.** Do not restore the rejected Chapter 3, 12 or 13 checks to satisfy a quota. Record meaningful exercises or closing examples by chapter. Chapter 16 now closes with one Abilene synthesis rather than a pattern-matching quiz; the original exercises remain optional reader practice. |
| Teach D13 site-built versus prefab/modular; fixed 20 MW late rack change | **Implemented in current Chapter 13.** The 14-scene EPC presentation includes the fixed-20-MW rack change, electrical/hydraulic/support consequences, supplied prefab figure, Houdini/Compass cases, OCP interfaces, factory/site testing and phased CoreWeave delivery. Rejected trivial schedule and release quizzes are removed. |
| Teach Crusoe’s solar/battery case in context | **Integrated.** `continuity-format.html#sparks-storage` includes the site photograph, 12 MW solar / 63 MWh battery account and 5.25-hour conditional calculation; the nines scene retains the separate availability claim. |
| Other requested cases in their relevant chapters | **Implemented at current destinations:** Google demand response and its deadline example in Chapter 14; Abilene plan versus reported delivery in Chapter 15; Abilene cooling in Chapter 12. These are separate from Colossus brownfield and Southaven procurement. The old “pending integration” statements were stale. |
| Abilene as the recurring campus throughout | Policy and several cases are implemented. A whole-course consistency pass is still open; no complete as-built campus model is claimed. |
| Approximately 20-minute primer | Slides exist; actual spoken runtime and beginner comprehension have not been established. No precise rehearsal cues are being restored. |
| Remove repeated disclaimer/subtitle clutter everywhere | The latest sweep removed many visible footers. **Not certified exhaustive.** Further cleanup must distinguish generic disclaimers from useful example inputs, figure credits and named-project status. “Ideal example” was explicitly permitted by the author and is not itself a missed removal. |
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
  recharge. The later `source-ramp-down` example now covers a sudden downward step and source surplus; its completion is recorded in COURSE_REVIEW.md.

## Chapter 11 opening review — 17 September 2026

- Reviewed the updated repository before edits: 49 commits since the previous baseline, 16 current chapters, Chapters 1–9 accepted, and the new shared presenter/notes system preserved.
- Opening uses “Why Is Air Cooling Dead?” and names the fundamental heat transfer equation. The combined comparison answers the rhetorical title by retaining residual air cooling.
- Former slides 2–3 become the stacked “Old with the New”; the separate CRAH/CDU explanation is folded into it. Current Lenovo GB300 documentation supports the retained hybrid path.
- New “How does the coolant enter the rack?” uses the existing NVIDIA rear view and labels technology coolant from the CDU. The distinct rear-door exhaust exchanger remains immediately after it; its facility-water example was not universally incorrect.
- Supplied 2CRSi single-phase image replaces the immersion illustration; a short phase comparison distinguishes liquid circulation from boiling/condensation.
- Supplied cold-plate photograph replaces the invented internal view. Exact manufacturer/model remains unverified, recorded in asset provenance rather than cluttering the slide.
- Downstream Chapter 11 scenes and shared navigation remain. Review and notes numbering now follow 16 scenes. This is not a whole-chapter approval.

## Chapter 12 opening review — 17 September 2026

- Opening titled “The Heat Still Has to Leave the Site”; only Collect → Carry → Release remains beneath it.
- Wet/dry comparison titled “Do you want your cooling wet or dry, sir?” Requested lower explanatory lines removed. Nozzle distribution, fill and direct air-water contact explain open-tower evaporation.
- Definition slide inserted before humidity example, using large quotation-style typography and original teaching wording. Wet-bulb is lower in unsaturated air and equal at saturation; it is not the pipe-water temperature.
- Removed the generic real-coolers temperature-gap line. Temperature comparison now distinguishes equipment names from the two air measurements and identifies each reference temperature.
- Chiller remains in Chapter 12 after the outdoor-temperature constraint. The Chapter 11 CoolIT CHx2000 is a liquid-to-liquid CDU, not a compressor, so adjoining the two without this distinction would reinforce the confusion.
- Removed the repeated higher-COP explanation. Updated notes and current tracker for the inserted slide; neither chapter is marked accepted.

## Chapter 13 EPC review through former slide 14 — 17 September 2026

| Request | Implemented result |
|---|---|
| Consistent chapter name and plain opening | EPC in the menu and reader; opening contains only Engineering, Procurement and Construction (EPC). Commissioning remains content, not the C in EPC. |
| Meme before the example | Meme moved to slide 2, ahead of the short 20 MW case brief. |
| Introduce the rack change and keep its consequences together | Slides 3–7: brief, before/after rack layout, electrical branch, hydraulic branch and concentrated support loads. The former slide 14 no longer appears as a disconnected return to the case. |
| Explain the new schedule case; remove fastest-button quiz | New case brief followed by four simultaneously visible dependency scenarios. The point is which purchase can change the opening date, not finding the lowest displayed number. |
| Make EPC concrete and give prefabrication proper treatment | Electrical-plant responsibilities, parallel factory/site assembly, analyst-reported AWS Houdini and verified Siemens–Compass physical package. Prefabrication is not confined to a definition slide. |
| Remove Houdini photograph caveat | Removed the visible caveat; neutral CEI credit and accurate provenance remain. |
| Remove trivial week arithmetic and generic pre-manufacture/shipping advice | Active factory-week, approval-delay, manufacturing-release, transport and approval-checklist slides removed; detail remains in the reader. |
| Reconsider the Compass “connect the part” slide | Retained its real photograph and package scope; removed the generic joint/handoff lecture. |
| Introduce OCP without a four-tab wall of text | One physical UQD interface example: shared mating interface versus the changed rack’s flow requirement. Named ORv3/UQD reference revisions and source notes added. |
| Correct Chapter 11 comparison title | “Out with the Old, In with the New”. |
| Replace Chapter 12 economizer slide with supplied image | Original PNG installed unchanged, with only its embedded title visible. |

The revised deck contains 20 slides. Commissioning and acceptance remain after the prefabrication examples. This revision addresses the author’s review through former slide 14; it does not imply acceptance of the remaining material.

## Chapter 14 full review — 17 September 2026

| Request | Implemented result |
|---|---|
| Keep the immediate case-study opening; remove repeated slide 2 | Opening retained. Local measurements show flow 100→50 kg/s and return 35→40°C, with inlet 30°C and heat 2.09 MW unchanged. Latest follow-up also supplies the hottest chip at 70→85°C against a stipulated 80°C limit. |
| Explain why old and fresh temperature were identical; clarify 40°C | Removed the standalone same-value timestamp exercise. Complete before/after sets identify inlet versus return and feed the following heat balance. |
| Keep control layers | Retained after the Google cooling case and before workload admission. The added performance plot makes this slide 7. |
| Google cooling needs context then flow | Three slides now distinguish 2016 recommendations from 2018 autonomous control, show all four original control diagrams together, then present the supplied original cooling-performance GIF. Operator override is explicit. |
| Remove generic command-is-not-proof slide | Removed; the necessary startup constraint is taught by simultaneous heat/cooling time traces. |
| Make standby cooling admission intuitive | Compare immediate versus delayed job start, showing the three-minute 1 MW deficit visually. |
| Google demand response needs context; old slide 10 is ugly | Two slides: The Dalles pilot, then concise workload names and both scheduling graphs together. The 20 MW base load and 4 MW job are labeled illustrative. The separate deadline slide is removed. |
| Keep shared isolation; consider chapter ownership | Initially retained as operational maintenance; the latest request removes it because shared-control dependence duplicates the redundancy chapter. |
| Remove generic wrong-command slide | Removed; prior EPC mapping coverage remains. |
| Cloudflare needs a concise start-to-finish story | Four slides: outage and affected services, single-facility dependencies, corrective changes/full-facility test, repeat outage and defined recovery endpoint. |
| Verify Gmail interpretation | Corrected: a software update affected multiple live copies; offline tape preserved recoverable mail. Not fixed copy A being reinfected by B. |
| London needs context | Added physical event/affected-zone context before the dated cooling-versus-service restoration timeline. |
| Keep Llama and add a real Meta figure | Existing recovery snapshot retained; a second slide uses Meta's original maintenance-train diagram with its separate fleet scope recorded. |
| Knowledge check lacks numbers and has verbose reveal | Supplied power, added job, flow, inlet, return limit and heat capacity. The 66.75 kg/s result is only the water-balance minimum; the existing 85°C chip-temperature violation must also be resolved before new work starts. |

The initial revision had 21 slides. The latest follow-up below produces 20 slides. This record reflects feedback implementation, not author acceptance.

## Cooling, supplied slides and GPU cloud economics — 17 September 2026

| Request | Result |
|---|---|
| Replace three control layers and prefab figures | Supplied full-slide images installed in Chapters 14 and 13; duplicate headings hidden. |
| Clarify Chapter 11 slides 3–5 | Latest placement: slide 3 combines the cold-plate photograph with its coolant-flow diagram; slide 4 (formerly 5) pairs the GB300 rear manifolds with the separately labeled RDHX mechanism. The standalone coolant-entry slide is removed. |
| Correct the assumption that residual air always uses CRAHs | Generic comparison now offers CRAH or RDHX. Crusoe's supplied pages do not establish an Abilene-wide absence of CRAHs or the proposed exact residual-heat percentage. |
| Simplify Chapter 11 slide 8 | Replaced several controls and dense copy with simultaneous 400 W / 35°C examples and one thermal-resistance equation. |
| Explain Chapter 16 | Five original engineering scenarios: outage, hot weather, rack retrofit, network bottleneck and phased opening. They are not five documented company incidents. |
| Remove Chapter 15's obvious or redundant capacity exercises | Rebuilt the chapter around what GPU clouds sell and who bears price, occupancy, delivery and operating risk. |
| Teach spot, one-, three- and five-year GPU rentals | Distinguishes interruptible Spot from market terminology, shows contract timelines and dated SemiAnalysis H100 rental ranges. |
| Teach bare metal versus managed services | Contrasts customer-operated and managed serving; bare metal can include Kubernetes and managed Slurm. |
| Explain energy pass-through | Contrasts fixed all-in fees with contractual energy reimbursement; calculates electricity per rented GPU-hour. |
| Replace cost-per-accepted-result provider framing | Uses committed versus rented GPU-hours and billable occupancy; internal cost per token/run remains a separate customer metric. |
| Compare Abilene plans to progress | Original target and reported-delivery table; adjacent Microsoft project removed. Unlike milestones are identified without inventing a delay. |

Chapter 15 now has 12 slides, including the hardware-price meme relocated from EPC. Implementation and technical checks do not establish author acceptance.

## Chapters 11–13 local review — 17 September 2026

| Request | Result |
|---|---|
| Chapter 11: clarify thermal path and relate it to heat flux | Retain the visual comparison; show chip-to-coolant temperature difference explicitly and keep concise definitions beside the heat-flux example. |
| Explain the pump chart | Initial pump/system intersection explanation was superseded by the later request: one fixed-speed pump curve with two flow rates and no clean/restricted comparison. |
| Remove approach, CDU and redundancy captions | Removed the specified supporting labels; cooling redundancy gets a literal title and both A/B paths are initially available. |
| Account for rear-door heat capture in the retrofit | Residual 15 kW takes either a room-air path or an RDHX-to-liquid path; do not charge captured door heat against room cooling. |
| Chapter 12: physically follow dry and wet cooling | Separate dry/wet slides walk through collection, transfer, outdoor rejection and return. |
| Explain condenser heat and reorder economizer | 10 MW collected plus 2 MW compressor electricity becomes 12 MW outdoors; economizer immediately follows. |
| Clarify adiabatic equipment and weather-dependent COP | Wet pads precool air before a sealed coil; compare COP 8 cool weather with COP 4 hot weather explicitly. |
| Remove averages, water metrics and numerical final check | All three removed from the active presentation; detailed reading/model remains. |
| Simplify closed-loop water and water accounting | Keep the toggled diagrams, remove the outdoor-arrangement heading, put tower water balance immediately after wet/dry equipment. |
| Heat reuse and operating dependencies | Data center generates heat all day; a separate factory needs it for six hours. Dry rejection needs electricity; wet towers also need ongoing water. |
| Chapter 13: explain 20 and 80 kPa | Both are pressure differences across the same connection at different flows, not pressures at the CDU versus rack. |
| Remove trivial schedule pair and reuse EPC slide as opening | EPC responsibilities becomes slide 1; the separate schedule brief/comparison is removed. |
| Make prefab image fill the slide and add Downloads rack figure | Full-page prefab image; original Open Rack figure follows the retained OCP coupling example, whose three upper category labels are removed. |
| Simplify factory acceptance | Title plus a three-row, two-column factory/site table. |
| Merge repeated control/test examples after cooling derating | One measured cooling-failure response now directly follows Chapter 11's reduction in rack heat. |
| Clarify shared readiness and remove final matching quiz | Plain readiness title retained; final pattern-matching quiz removed. |
| Reuse the earlier CoreWeave phase example | Original campus photographs and 27 October / 24 November 2025 delivery milestones return, motivating the next 50 MW connection beside the first live phase. |

Revisions are available on the local server. Implementation and technical checks do not imply author acceptance.

### Chapter 11/12 wording follow-up

- Chapter 11 slide 7 defines heat flux and thermal resistance without changing its comparison; slide 8 uses ΔT explicitly for the chip-to-coolant difference.
- Chapter 11 slide 10 now has one fixed-speed pump curve and two flow rates. The title describes available pump pressure, avoiding a general claim that faster flow always lowers pressure.
- Chapter 11 approach slide includes the requested small note, “The lower the approach, the better.”
- Chapter 12 wet-/dry-bulb definition subtitle now reads “Think of it like sweating!”
- Outdoor path captions specify rack **coolant** supply and its 35°C maximum. The 35°C outdoor air plus two 5°C approach differences gives 45°C inlet coolant; 35°C is a stipulated inlet limit, not a chip-temperature limit.

### Chapter 12 order and hot-weather image

Moved `closed-loop-water` immediately after `approach-wet`, making it slide 9. The following chiller, economizer and COP material remains together. Restored the original hot-day data-centres cartoon as a small corner image on `hot-hour` (now slide 14), without obscuring its equation or electricity comparison. The adiabatic cooler explanation distinguishes evaporating pad water to precool air from exposing circulating tower water directly to air; the earlier question had been acted on but not clearly answered to the author.

### Pump operating-point follow-up — 17 September 2026

The author subsequently asked to restore how actual flow is determined, then explicitly requested the higher-resistance system curve. Chapter 11 slide 10 now has three curves: the fixed-speed pump Δp = 160 − 10q², the normal circuit Δp = 30q² and the higher-resistance circuit Δp = 70q², with q in L/s and Δp in kPa. The normal circuit meets the pump at 2 L/s and 120 kPa; the higher-resistance circuit meets it at √2 ≈ 1.41 L/s and 140 kPa. More restriction therefore reduces flow on the same pump. This supersedes the earlier pump-only and single-circuit versions. Visible text stays sparse, with the equations and fuller explanation in the speaker notes.

### Live review follow-up — 17 September 2026

- Chapter 13 final phase slide: exact requested title, “Connect the next 50 MW while keeping the first 50 MW online.” The official investor-presentation photographs now have equal photo-only viewports, side by side above the milestones, stacked evenly on mobile.
- Chapter 14 slide 2: removed the bottom subtitle; preserved measurements. Slide 3 explanation and speaker notes distinguish equal heat removal from acceptable chip temperature. The later follow-up adds explicit 70→85°C chip measurements against an 80°C limit.
- Chapter 14 control-layers image: moved after the Google cooling case and before workload admission. It was slide 6 at this review; the later performance-plot insertion makes it slide 7.
- Chapter 12 adiabatic assist: selected the clearer of the two supplied Downloads images, retained the original bitmap, and replaced the diagram body. Placed immediately after the dry-cooler walkthrough: dry route → optional wetted-pad assist → wet tower → closed-loop comparison.

### Hardware-price meme placement — 17 September 2026

Moved the supplied meme out of EPC and into Chapter 15 immediately after GPU financing and before the GPU-hour cost breakdown (slide 9). This concerns component purchase prices, not rental rates. Chapter 13 now begins EPC → rack-change case without an interruption. The old EPC meme bookmark redirects to its new chapter.

### Chapter 14 thermal diagnosis and Google figures follow-up — 17 September 2026

| Request | Implemented result |
|---|---|
| Explain why the row is failing when both water balances remove 2.09 MW | Slides 1–3 now show hottest-chip measurements of 70→85°C against a stipulated 80°C operating limit. These are scenario inputs, not a GPU rating or values derived from the water balance. Immediately after flow falls from 100 to 50 kg/s, an unchanged 5°C water rise would remove only 1.045 MW, so heat accumulates. The later 10°C rise restores the full heat balance at a measured chip temperature above the limit. |
| Put all original Google control diagrams together | `google-cooling-flow`, slide 5, shows all four original diagrams in order: sensor snapshot, prediction, action selection and independent local verification. |
| Add the supplied original performance plot after the control flow | New `google-cooling-performance`, slide 6, uses the original GIF. The reported approximately 12%→30% reduction over nine months concerns cooling energy per unit of cooling against the historical baseline, not total facility electricity. |
| Retain the control-layers image after the Google case | `control-layers` is slide 7; workload admission follows on slide 8. |
| Merge the deadline graphs into the Google workload slide | `google-demand-response-workloads`, slide 10, combines concise Google workload names with both scheduling graphs. The 20 MW base load, 4 MW job and deadline are illustrative teaching assumptions, not disclosed Google measurements. The standalone deadline scene is removed. |
| Remove the repeated shared-control maintenance example | `maintenance-scope` is removed from the active sequence because this dependency is already covered in the redundancy chapter. Cloudflare now follows demand response directly. |
| Keep the closing calculation consistent with the chip alarm | Slide 19 identifies 66.75 kg/s as the water-balance minimum only. Admission also requires resolving the existing chip overtemperature and measuring chips below the stipulated limit. |

The active source sequence contains 19 slides: Row B 1–3; Google cooling 4–6; control layers 7; workload admission 8; demand response 9–10; Cloudflare 11–14; London 15–16; Llama 3 and maintenance 17–18; knowledge check 19. Speaker notes follow this sequence. This entry records source changes; it does not claim completed browser checks, tests, publication or author acceptance.

### Cloudflare and London review follow-up — 17 September 2026

Cloudflare’s opening now shows only the disrupted dashboard, API and analytics. The next title explicitly identifies a single point of failure. The correction and successful retest slides are preserved. The Gmail backup case is removed from this presentation and remains in the storage reading. Google’s original London incident report was inspected and contains no incident photos or diagrams. Latest local test/browser validation is recorded in TESTING.md.

### Meta figure and closing verdict — 17 September 2026

Added the supplied maintenance-cost graph beside Meta’s train diagram on `llama-maintenance`, preserving the supplied image bytes and removing the purple/teal subtitle. The closing knowledge check now explicitly answers “No—the new job must wait,” shows the existing chip-temperature violation in its givens, and requires sufficient flow plus acceptable chip temperature before admission.

### Heat accumulation and plant-controls focus — 17 September 2026

Chapter 14 slide 3 replaces the disconnected endpoint calculations with aligned heat-rate and chip-temperature traces. Heat accumulates while removal falls short of generation; the later equality stops further warming at an already excessive temperature. The trace has no claimed settling duration. Arbitrary clock labels were removed from the opening measurements. A duplicate control-layer slide highlights only plant controls before the standby-start example; the original overview remains unchanged. Chapter 14 now has 20 slides.


### Google and Cloudflare layout restoration — 17 September 2026

The author rejected the compressed Google workload labels. Restored the original large Keep serving / Defer eligible background work panels, with the scheduling graphs returned to their own following slide. This supersedes the earlier request to merge them. Restored Cloudflare’s original Core services card, date and source; removed only the unaffected Global edge network card. The chapter now contains 21 scenes.


### Rebuild the Chapter 14 closing exercise — 17 September 2026

Replaced the already-overheating Row B exercise with a separate, healthy Row C. The site has 3 MW of spare electrical and central cooling capacity, but the row’s measured flow and return-temperature limit allow only 2.09 MW more heat. The proposed 2.50 MW workload therefore tests local versus site headroom, rather than asking the learner to reject a workload because an existing chip alarm gives away the answer. The reveal states the decision and calculates local headroom; speaker notes explain the approximately 110 kg/s total-flow requirement and operational verification.

### Merge Cloudflare’s outage and dependency slides — 17 September 2026

Merged former Chapter 14 slides 13 and 14 into `cloudflare-pdx`, retaining the outage date, Core services card for the disrupted dashboard, API and analytics, and the three-site dependency diagram. The title identifies the single point of failure. `hidden-dependency` now aliases this combined scene. The correction and retest remain separate slides; Chapter 14 now has 20 scenes, with Cloudflare on slides 13–15 and the closing exercise on slide 20. This records the merge without changing whole-chapter acceptance.


### Cooling reserve and Google’s incident quotation — 18 September 2026

Clarified that slide 9’s 1 MW headroom is a teaching assumption. Added manufacturer stage-up thresholds and an Intel IT thermal-storage case immediately after that example, distinguishing continuous capacity from stored thermal energy. The Intel figure is extracted directly from the primary paper. Added the author’s exact Google root-cause quotation in the established quotation format immediately before the London shutdown mechanism. Added explanatory notes distinguishing a hotter steady state from a longer heat-removal interval and identifying the unchanged inlet versus warmer return. Chapter 14 now has 23 slides; Chapter 14 acceptance remains pending.


### Chapter 15 opening terminology and contract-chart search — 18 September 2026

Removed the internal-cost sentence from slide 2. Slide 3 now defines bare metal and distinguishes hardware architecture from software-management responsibility, verified against CoreWeave’s own product pages. Slide 4 defines Spot in the title, keeps the three rental offers and removes the redundant market-price subtitle. Interpreted the request for “Chapter 12 slide 5” as Chapter 15’s contract-term comparison because its one-/three-/five-year context is unambiguous. Searched the public SemiAnalysis dashboard and published GPU rental-index launch article: they track the full term structure, but publish the H100 one-year index publicly and reserve full-term data for institutional subscribers. Retained the duration diagram rather than fabricate an unavailable same-GPU, same-date comparison. Mobile footer now flows after content instead of covering it.


### Chapter 15 NVIDIA backstops and powered idle capacity — 18 September 2026

Moved the supplied hardware-price meme to the opening. Removed “dated observations, not September quotes” from the market source caption and the construction-versus-delivery subtitle from the final Abilene slide; historical dates and milestone distinctions remain in the data and notes. Financing now leads into three NVIDIA backstop slides, sourced to SemiAnalysis and corroborated by CoreWeave/NVIDIA SEC disclosures. Chapter 15 now has 15 scenes. The electricity example explicitly includes both rented and unrented-but-powered hours: 80 kWh + 4 kWh divided by 80 rented hours. Rented hours are not assumed to mean 100% GPU compute utilization; example power is a whole-site allocation per GPU. Author review remains pending.


### Chapter 8 conversion comparison — 19 September 2026

Renamed `board-rails` to the author’s requested “All roads lead to Rome.” in the scene metadata and teaching image. Removed the green bottom caption panel and its overlaid sentence after the author’s follow-up. The direct and intermediate conversion diagrams, speaker notes and existing bookmark remain intact. Original supplied image preserved; derivative and edit prompts recorded in the figure provenance.


### Chapter 8 PSU input photographs — 19 September 2026

Kept `psu-input` as its own slide. Replaced the left text box with the primer’s existing three-phase waveform, the three PSU rectangles with the existing Advanced Energy module photograph, and the DC-bus box with NVIDIA’s rear rack image. The busbar is highlighted at the manufacturer’s callout location. Removed the standalone sentence title, square-root calculation and phase-to-neutral footer; retained concise voltage labels and manufacturer credits. Speaker notes identify the images as examples of the functions rather than a matched installed equipment set. The slide order and existing bookmark remain unchanged.


### Chapter 8 phase connections and busbar annotation — 19 September 2026

Removed the unrelated seismic-bracing annotation from the rear-rack image used by `psu-input`; the busbar arrow remains, and the original manufacturer image is preserved. Connected each colored AC waveform to its corresponding L1/L2/L3 PSU path. The waveform has the same 120-degree phase separation, with its displayed cycle starting at a different point so the connectors can reach their PSU rows without crossings. Mobile uses the same phase-to-module mapping.

### Cooling-tower fill speaker note — 19 September 2026

Added the requested definition to the Chapter 12 wet-tower speaker notes and scene explanation: fill spreads water into thin films or droplets to maximize the water surface exposed to air per unit volume. Linked the DOE cooling-tower component guide. The projected diagram is unchanged.

### Adiabatic boost image and cooling circuits — 19 September 2026

Added the supplied nitrous-boost image alongside the existing adiabatic-assist diagram. Recorded the analogy and the dry-cooler versus refrigerant distinction in speaker notes and review questions 24, 26 and 28, including the optional four-circuit arrangement and the 10 + 2 = 12 MW compressor balance. Checked the existing three-control-layer image for review question 37: it already identifies flow/pressure, bringing cooling units on and moving/delaying compute, so no duplicate captions were added.

### Llama 3 slide simplification — 19 September 2026

Simplified Chapter 14 `llama-recovery` into two metric columns. Removed the generic Detect → Recover → Continue boxes and preserved all visible numbers: 54 days, 466 interruptions, 47 planned, 419 unexpected, more than 90% effective training time and three incidents requiring significant manual intervention. The existing hardware statistic remains in the speaker explanation. Verified desktop, mobile and light/dark layouts; navigation and slide order are unchanged.

### Chapter 15 serving choices and customer examples — 19 September 2026

Retitled slide 4 “There are two ways to skin the cat.” Replaced the responsibility matrix with two simple serving stacks and removed the bare-metal footer. Added slide 5, `service-examples`, with Anthropic–CoreWeave cloud capacity and Cursor–Fireworks managed Fast Apply inference, using company marks. The public Anthropic agreement does not disclose a bare-metal purchase or the detailed serving split; that limit and the distinction between a hypervisor and container orchestration are recorded in scene explanations, speaker notes and review question 46. All existing slide bookmarks remain. Desktop/mobile and light/dark layouts verified; Chapter 15 now has 16 slides.

### Chapter 15 occupancy and electricity simplification — 19 September 2026

Removed the occupancy slide’s entire annual-revenue/billable-occupancy subtitle; its distinction stays in the speaker notes. Reworked `gpu-hour-cost` using the sparse two-column treatment from the Llama 3 slide: rented and powered-idle energy on the left, 1.05 kWh per billed GPU-hour and both electricity prices on the right. Preserved every calculation input and result.

### Chapter 15 NVIDIA money-machine image — 19 September 2026

Inserted the supplied image unchanged, without an added title, immediately before `nvidia-coreweave-backstop`. Preserved the embedded Bloomberg attribution and recorded asset provenance. Image-only scenes now share the same header handling. Existing bookmarks are unchanged.

### Chapter 15 delay quotation and Abilene table — 19 September 2026

Added an exact-title SemiAnalysis quotation slide immediately before `abilene-ledger`, with the June 18, 2026 article linked at the bottom. Removed the table’s smaller gray source/date labels and folded them into the three source links. March 2025 identifies the original plan; September 2025 identifies the first-phase report; September 2026 identifies Oracle’s delivery update. Preserved the table’s milestone comparison and all existing bookmarks. Chapter 15 now has 18 slides.

Independent source review also clarified that Oracle’s 75% delivery figure covers total campus capacity, not just the six-building expansion; the comparison now states that scope explicitly.

### Cooling margin, adiabatic reveal and circuit clarification — 19 September 2026

Condensed the operating-margin inputs on Chapter 14’s `chiller-staging` slide into three bullets: demand, usable capacity and response time. The explanation distinguishes spare MW from stored thermal energy and preserves the manufacturer’s 80%/90% efficiency-staging thresholds. Chapter 12 now separates the nitrous-boost image into a title-free transition between the dry-cooler temperature example and the adiabatic-assist diagram. Added a small water/glycol label to the non-numerical dry-cooler path. Updated review question 26 and speaker notes to distinguish a condenser-water loop from an optional waterside economizer, and to explain purpose-built compressor-off refrigerant circulation.

### Electricity pass-through and delay artwork — 19 September 2026

Confirmed that electricity reimbursement was already in the reader, review question 49 and speaker notes. Added a sparse follow-up slide after `gpu-hour-cost` contrasting a fixed all-in price with electricity pass-through, retaining the preceding $0.084/GPU-hour increase. A dated Core Scientific filing grounds the separate colocation example: power is passed through to CoreWeave without markup. Added the supplied SemiAnalysis artwork unchanged to `datacenter-delay-quote`, preserving the exact title and source link. Chapter 15 now has 19 slides. Speaker notes clarify that the existing compressor-rest image depicts water-side free cooling. `REVIEW_QUESTIONS.md` remains unchanged pending the user’s requested retirement confirmation.

### Independent recording-audit follow-through — 19 September 2026

Checked all four findings against the current source. Qualified the Chapter 11 CDU caption to “A lower approach gives more coolant-temperature margin,” with exchanger/flow/cost tradeoffs in the notes. The Abilene table already identifies 75% as total campus capacity; no additional change was needed. Retained the air-cooling title and Chapter 9 power-stack graphic at the author’s direction. The latter's small labels and insufficiently scoped source claims remain known limitations.

Verified the Microsoft Superfactory infographic's readability issue at 1280×720. Kept its full overview and added Campus scale / Inside the data hall detail views through existing shared controls, enlarging the original callouts by about 2.3× without changing the source image. Checked all three views in light/dark at 1280×720 and 390×844, including mobile scrolling and control access; the slide count and bookmark remain unchanged. The Chapter 14 Google plot's initially blank axes are intentional in its four-second animation. The independent audit document and `REVIEW_QUESTIONS.md` were left unchanged.

### Simplify electricity pass-through — 19 September 2026

Reduced `electricity-pass-through` to two choices under the existing question: fixed all-in price / provider absorbs the increase, and electricity pass-through / customer pays the increase. Removed the repeated calculation and company example from the projected slide; source context and assumptions remain in the scene explanation and speaker notes. Verified 1280×720 and 390×844 in light/dark themes, with no clipping or browser errors. The author also approved retiring `REVIEW_QUESTIONS.md` after reading the final three clarifications; its existing URL and reference content remain available with a retirement notice.

### Compatible cooling layouts — 19 September 2026

Added `cooling-layouts` immediately after the compressor-rest illustration, as Chapter 12 slide 14 of 21. One shared IT-coolant / CDU / facility-water heat path leads into three families: no chiller, air-cooled chiller and water-cooled chiller. Both dry-cooler and wet-tower routes are represented; the latter retains separation from the closed facility loop. The additional condenser-water circuit is distinct from an optional economizer bypass. A short line separates compressor-off operation from layout choice; equipment compatibility, refrigerant-side free cooling and the heat-versus-fluid distinction are explained in the notes. Trane and Vertiv provide the source evidence. Updated speaker-note numbering and checked 720p and mobile in light/dark themes. Existing slide bookmarks and the chapter's closing dependency slide remain intact.
