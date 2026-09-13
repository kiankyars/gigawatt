# Feedback audit — 13 September 2026

This audit checks the requests visible in this task against current source and
Git history. Requests made on the other computer are checked against their
repository records; those records do not substitute for the original message.
The prior “everything addressed” claim was too strong. This page foregrounds
exceptions; the coverage list below makes the rest inspectable.

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
and product-photo gap listed below. Historical Chapter 3 rows have been reconciled
with their replacements. This source audit does not establish fresh visual QA,
whole-course completeness or author acceptance. Chapters 4–5 remain with their
current authoring agent. Kian clarified that Chapters 6 and 7 must remain separate.
The Astra / Ultra agent is building a Chapter 6 deck and a separate Chapter 7 deck;
the latter retains `tier-investment`. Kian confirmed that the two existing decks to
consolidate belong to **Chapter 8: rack-to-chip and 800 V DC**. Combine those into
one Chapter 8 presentation while preserving the reviewed mechanisms. Chapter 8
must not be merged into Chapters 6 or 7.

## Missing, partial or uncertain

| Feedback | Current finding and next action |
| --- | --- |
| Evolving functional bill of materials and service-path companion | **Unbuilt.** The commitment existed only in COURSE_REVIEW.md prose. Build the persistent component inventory and connect it to the facility map and lesson changes; isolated diagrams do not fulfill this request. |
| Named rack hardware shown as real equipment | **Teaching-standard gap.** The Advanced Energy ORv3 PSU and six-module BBU shelf have functional drawings, but no product photograph in those scenes. Add a verified product/specification image appropriate to each example; retain the drawings for the mechanism. This follows the general product-example rule, rather than a separately recorded photo request for those two products. |
| Teach **interactivity** as the central inference metric | **Missed in the previous release.** The fixed 4,000-token/s budget was arbitrary and slide 3 did not teach interactivity. Revised slide 3 defines tokens/s/user; the next slide reads NVIDIA’s actual GB300 throughput/interactivity curve. Exact supported-session selection remains **open** because this source has no concurrency table; a fixed total divided by user speed is not an adequate substitute. |
| Active check-in in every domain | **Not complete in the teaching material.** Fifteen reader checks exist. Latest clarification: make an active check-in the default in each domain; use a strong example only if no worthwhile check can be made. Chapter 3 now includes a more-throughput/slower-answers check; audit the remaining decks and record any specific exception. |
| Teach D13 site-built versus prefab/modular; fixed 20 MW late rack change | **Reader complete; deck unbuilt.** The reader covers EPC duties, factory/site work, parallel schedules, design freezes, transport and interface owners; the exercise covers electrical, hydraulic, spatial and schedule holds and release evidence. Chapter 14 in the numbered course still needs its own teaching sequence. |
| Teach Crusoe’s solar/battery case in context | **Partial.** Sparks has standalone solar/battery teaching and appears in the UPS availability examples. The actual 12 MW solar / 63 MWh battery mechanism is not yet integrated into the continuity/storage deck. |
| Other requested cases in their relevant chapters | Google flexible scheduling and Abilene’s capacity ledger remain pending integration. Abilene cooling appears in the physical-site deck, but not yet in the cooling deck. These are separate from already integrated Colossus brownfield and Southaven procurement cases. |
| Abilene as the recurring campus throughout | Policy and several cases are implemented. A whole-course consistency pass is still open; no complete as-built campus model is claimed. |
| Approximately 20-minute primer | Slides exist; actual spoken runtime and beginner comprehension have not been established. No precise rehearsal cues are being restored. |
| Remove repeated disclaimer/subtitle clutter everywhere | The latest sweep removed many visible footers. **Not certified exhaustive:** UPS still uses “Ideal DC-bus example”; other notes use similar boilerplate. Further cleanup must distinguish generic disclaimers from inputs, figure credits and named-project status. |
| Transformer input-range explanation | **Partial; previous completion claim corrected.** `transformer-taps` explains output change at a fixed ratio and a matched tap. It does not yet identify a real unit and its permissible input-voltage range. Add the manufacturer's rating, tap options and operating limits without treating tap range as guaranteed regulation or tolerance. |
| Simplify access to available presentations | Directory and duplicate footer were consolidated. The two rack-power decks still had identical visible “Open slides” labels; corrected to their distinct titles. The old audit’s “Slides available filter” claim was stale: a later recorded request deliberately removed that filter. |
| Requested Astro 6 Ultra agents and Chrome-for-Testing removal | Earlier audit records both as completed. Current code/Git alone cannot freshly establish the historical agent configuration or the notification state on the original Mac. Built-in-browser-only testing remains the rule; this audit is not a new malware scan of that other computer. |

These open production tasks are also owned by [Course review](COURSE_REVIEW.md#next-teaching-step)
and the [case handoffs](TEACHING_STANDARD.md#required-section-handoffs).

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
  equipment's permissible operating range remains open as recorded above.
- **Check-ins:** latest instruction supersedes the earlier broad permission to
  substitute closing examples. Default to one meaningful active check per domain.

## Other requests checked

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
