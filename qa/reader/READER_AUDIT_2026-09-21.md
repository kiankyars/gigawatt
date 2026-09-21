# Reader audit — 21 September 2026

Scope: the 51 reader lessons, glossary, source lists and check-ins generated from
`course/expansion/*.json` (about 102,000 published words, of which 54,755 are
body prose). Slides and the recorded video are treated as frozen and correct.
This file lives under `qa/` because `stage_site.py` publishes every
`course/*.md` to the live site.

Re-run the measurements at any time with `python3 qa/reader/prose_lint.py`.

## Verdict

The reader does not have the usual AI-slop problem. It has a rarer one.

The filler vocabulary people scan for is absent: zero uses of *delve, crucial,
pivotal, leverage, robust, landscape* in 55,000 words, and eight em-dashes. The
arithmetic is code-checked and the facts are sourced. Someone already scrubbed
the obvious tells.

What remains is **audit voice**. The text was written to survive a fact-check
rather than to teach. Half of all paragraphs end on a negation, usually the
denial of a claim nobody made. A learner who has never heard of a 12-inch pipe
is told that no 12-inch pipe was verified. The reader has become the place where
every caveat removed from the slides was stored, and its prose has taken the
shape of that ledger.

The underlying material is good: accurate, well-sequenced inside most lessons,
and built on worked numbers. The fix is mostly subtraction and re-voicing, plus
realignment with the recorded video. It does not need new research.

## Measurements

Baseline: eight Wikipedia engineering articles (data center, UPS, combined
cycle, roofline model, power transmission, cooling tower, transformer, circuit
breaker), 43,166 words of human-edited technical prose. It is a rough yardstick;
the gaps are large enough that the choice of baseline does not matter.

| Signal | Reader body | Human baseline | Ratio |
|---|--:|--:|--:|
| Sentences containing a negation | 23.1% | 7.7% | 3× |
| **Paragraphs whose last sentence is a negation** | **48.5%** | **9.4%** | **5×** |
| "establish*" per 10,000 words | 22.5 | 2.1 | 10× |
| Semicolons per 1,000 words | 6.3 | 1.2 | 5× |
| Sentence length, mean (std. dev.) | 15.5 (6.2) | 21.9 (10.2) | flat rhythm |
| Generic slop words (*delve, crucial, leverage…*) | 0 | n/a | none |

The pattern is uniform across all five source files (41–52% of paragraphs end on
a negation in each), so this is one systemic voice, not a few bad lessons.
50 of 51 lessons exceed the lint budgets; the single pass is
`d10-flow-and-pressure`.

Other counts:

- **40 sentences in 20 lessons** point at a slide or image the reader cannot
  see ("The slide shows…", "The presentation uses…"). Listed in Appendix A.
- **Review and fact-check notes sit in teaching prose** ("October is still
  future as of this September 12 review."; "This replaces the separate
  schematic border slide."). Listed in Appendix B.
- **357 source annotations carry about 15,000 words** of notes. 65% of their
  `limits` text is a verbatim copy of the research catalog's `caution` field,
  which is a note to the author. 31 contain instructions such as "add
  restrained overlay labels or explain orally" or "full PDF fetch returned
  HTTP 403". Listed in Appendix C.
- **About a quarter of lessons open with a concrete situation.** The rest open
  with a definition, which wastes unusually good titles ("A contract is not a
  cable", "A collective makes waiting contagious", "A rack must fit on its
  worst day").
- **Depth is uneven:** `d03-service-and-siting` has 3,610 body words in 18
  sections with 40 sources; the three GPU-economics lessons have 309–430.
- **Cross-lesson copy-paste is negligible** (four shared seven-word runs in the
  whole corpus). Padding by repetition is not a problem here.

## Root cause

Three mechanisms, all fixable at the source.

1. **The authoring standard routes every caveat into the reader.**
   `TEACHING_STANDARD.md` says it five ways: "Put exceptions, source discussion
   and longer derivations in the reader", "Keep source discussion in the
   reader", "record its provenance in the reader", and so on. The same document
   bans generic disclaimers on slides. The problem was noticed and fixed on the
   slide side by moving it to the reader side.
2. **The standard is written in the voice it produces.** "Current does not
   establish facility efficiency; energy capacity does not establish discharge
   power; total coolant flow does not establish adequate flow through every
   branch." Any agent that reads this before writing a lesson imitates the
   cadence. The style guide is the style exemplar.
3. **The pipeline copies author notes into learner text.** The "12-inch pipe"
   sentence began as a caution in `research/sources/P103.md`, was copied to
   `research-sources.json`, then into the lesson's source `limits`, then
   promoted into a body paragraph. The builder also *requires* non-empty
   `tradeoff`, `failure`, `example.boundary` and per-source `limits` on every
   lesson, so those slots get filled even when there is nothing to say.

The important consequence: negation is the course's best teaching device when
it targets a real misconception. "A megawatt is not a megawatt-hour." "The heat
does not disappear at the chiller." Spending it on every paragraph buries the
warnings that matter under ones that do not.

## What to keep

- **The arithmetic.** Every number in every body, worked example, failure field
  and practice answer across all 51 lessons was independently re-derived
  during this audit. No arithmetic error was found. The defects listed under
  "Content defects" are wording, consistency and reasoning, not calculation.
- The titles and driving questions.
- The homepage copy ("Electricity reaches the racks. Cooling carries their heat
  back outside."). It is already in the voice the reader needs.
- The check-ins ("It fits until replacement day"): concrete, short, well built.
- The glossary's definitions, which are tight (mean 14 words, 8% negated).
- The recurring Abilene thread, which appears in 13 lessons.
- Passages that already have the target voice. Examples:
  - `d01-power-over-time`: "That display could come from a constant 8 MW draw.
    It could also come from one minute at 12 MW followed by four minutes at
    7 MW… These traces are indistinguishable to the average yet impose
    different peak demands."
  - `d10-local-thermal-paths`: "A failed fan can harm an air-cooled component
    while the liquid supply remains normal. Likewise, a blocked cold-plate
    branch can cause local throttling even if the room is comfortable and the
    CDU's aggregate load is below its rating."
  - `d03-voltage-and-distance`: "Halving current quarters this particular loss
    because the current is squared."

The rewrite target is not a foreign style. It is the corpus's own best fifth.

## The deeper cost: the voice removed signal as well as adding noise

Six reviewers read all 51 lessons in full. Working independently, each one came
back with the same observation in different words: "the lessons pose ML
questions and refuse ML answers"; "calibration values are withheld, so look-up
fails"; "no real transceiver wattage appears, in a course about watts".

A writer trained never to overclaim stops claiming. The measurable result:

| In 54,755 words of body prose | Count |
|---|--:|
| "universal", always as a disclaimer | 36 |
| "typically", "usually", "in practice" | 4 |
| "rule of thumb" or any equivalent | 0 |

Rules of thumb, named laws and standard terms are what an expert carries around
and what a learner most wants to take away. The reader describes them without
naming them, which also defeats search:

- **Never named in any lesson body:** REC, virtual PPA, hourly matching,
  $/MMBtu, Amdahl's law, error budget, NEC/NFPA, Young/Daly checkpoint interval,
  MFU, goodput, TCO, load factor, capacity factor, C-rate, RPO/RTO, ATS/STS,
  commissioning levels L1–L5, FAT, SAT, IST. Instead of "REC" the reader says
  "An attribute associated with a quantity of generation addresses the
  characteristic being claimed for that generation."
- **Results never stated as a rule:** water cooling needs about 1.43 L/min per
  kW at a 10 K rise (the flow lesson computes 120 L/min for 84 kW and stops);
  pump power rises with the cube of flow ("can have a strong effect"); about
  1.5 L of water evaporates per kWh of heat rejected (absent, so the 100 m³/day
  in the water lesson arrives from nowhere).
- **Motivating comparisons missing:** the 800 V lesson never says that 1 MW is
  20,000 A at 50 V and 1,250 A at 800 V. The scale-up/scale-out lessons never
  put 900 GB/s of NVLink beside a 50 GB/s NIC. The protection lesson
  illustrates a fault with 1,000 A when the next chapter's *normal* rack load is
  2,000 A, and gives no kA-scale figure.
- **Core acronyms are never spelled out in a lesson.** GPU (79 uses), UPS (31),
  CPU (12), PUE (8), PDU (7), LLM (4), BMS and WUE are never expanded in any
  lesson body. PDU, LLM, BMS, WUE and COP have no glossary entry either. EPC and
  BBU are used a chapter or more before the lesson that expands them. The
  learner contract lists unexplained acronyms as the first confusion risk.

So the rewrite has two halves. Take out the denials nobody needed. Put back the
numbers, names and rules of thumb the denials displaced.

## Structure

The same four patterns recur in every group of lessons.

1. **A clean core, then slide captions in deck order.** Lessons grew one
   section at a time as slides were added. `d04-read-the-power-train` is a
   complete three-section lesson followed by fourteen sections that follow the
   deck (busway → 345 kV → switchgear → CVT → 480Y/277 → controls transformer →
   taps → PDU), which breaks the lesson's own rule to follow the path to the
   load. 22 of 51 lessons need regrouping by argument. This is mostly
   re-sorting existing material.
2. **The numbers are told two to four times.** Half of all distinctive
   worked-example numbers (140 of 281) already appear in the body, and in 20
   lessons the "worked example" is mostly a recap. 40% of practice-answer
   numbers are printed in the body before the question is asked. The rack-change
   case is computed four times across Chapter 13. The capstones get this right:
   the body sets up, the example computes, the practice changes a condition.
   Copy that pattern everywhere.
3. **Template slots filled because the builder demands them.** `tradeoff` and
   `failure` are required, so they get entries like "Cost: Cost, footprint, and
   operating efficiency need their own assessment." Most "Response" fields
   reduce to *verify, identify, compare, reconcile*. Where a field has numbers
   it works well (`d10-flow-and-pressure`: one of four branches drops to
   0.25 L/s and its rise doubles to 20 K). Three takeaways repeat their summary
   verbatim.
4. **Chapter checks sit after the source list and test a different lesson.**
   The check attached to `d05-protection` tests redundancy; the one on
   `d14-maintenance` tests telemetry; the one on `d04-conversion-placement`
   tests kVA.

Also: "original" is used corpus-wide to mean "invented by us" ("In this
original example"), which collides with its ordinary sense ("one week of
original arrival float", "the original Crusoe-built campus"). "Supplied",
"stated" and "declared" behave the same way.

### Proposed splits and merges

| Lesson | Proposal |
|---|---|
| `d03-service-and-siting` (3,610 words, 18 sections, 40 sources) | Four lessons. **1. Usable power arrives one phase at a time** (Polaris, connection process, Abilene, siting constraints; the current title, takeaway and check fit only this). **2. Behind the meter: four ways to connect a campus** (BTM, four arrangements, bridge power, fuel; the island calculation becomes the worked example). **3. Simple cycle versus combined cycle** (mechanisms, LHV, Dania Beach, duty roles; 250 vs 166.7 MW as the worked example; add heat rate). **4. Paying for speed: the Southaven bet** (crossover and fuel penalty made adjacent; merge the two Southaven map sections; contract fees cut to a paragraph). |
| `d12-hazards-and-site-evidence` (19 sections, 32 sources) | Three lessons: **Screen a parcel against the first-phase brief**; **Controlling the parcel is not controlling the surface** (options, easements, mineral estates, permits); **What the ground, the flood and the last owner leave behind** (greenfield/brownfield, Colossus 1, fill, Harvey). Move the heat-rejection paragraphs to `d11-water`. |
| `d11-weather-and-operating-envelope` | Three topics: the temperature stack, hot-hour ceilings, cooling-fault response. The third repeats `d10-cdu-interfaces` with the same 1,000/600/500 kW numbers. Merge both into one lesson, *Which cooling path survives the fault?* |
| `d05-storage-power-and-time` + `d06-rack-migration` | Capacitor and DC-link physics is ~40% of `d05-storage` and most of `d06-rack-migration`, yet is in neither title. Pull both into one **Buffers by time scale** lesson. Leave runtime and retrofit as their own lessons. |
| `d05-paths-and-transitions` | The argument ends after section 3. Split off **Tiers, nines and Fairwater** as a look-up lesson. |
| `d02-*` (three lessons) | `d02-productive-utilization` (310 words) never defines utilization and duplicates its neighbours: merge. `d02-phases` is inference serving plus training power rhythm: split. `d02-workload-brief` never shows the brief: add it as one table. |
| `d03-voltage-and-distance` | Split the AC / three-phase primer (which `d04` depends on) from the transport comparison. Say that resistance scales with length; at present "distance" is never taught. |
| `d08-topology-budget` | Split fabric budget from campus fibre, meet-me rooms and route diversity. |
| `d13-delivery-dependencies` | Critical-path network and prefab-versus-site-built are two lessons joined by a slide insert. |
| `d04-conversion-placement`, `d06-eight-hundred-volt-architectures` | Move the MV-to-800 V hardware block out of the loss-accounting lesson into the 800 V chapter. Map the three naming schemes (Architecture A/B/C; AC/sidecar/direct MV; rack/row/block) onto each other. Open with why 800 V. |
| `d15-*` (309–430 words each) | Too thin to stand beside their neighbours. Build an actual cost per GPU-hour (energy turns out to be about 4% of a $2.50 GPU-hour, which is the punchline). Move `d15-upgrade-and-evidence` to Chapter 16 as the Abilene companion. |

## Content defects

None of these is an arithmetic error. Items marked ✔ were re-checked against the
lesson text by the lead reviewer.

**Reasoning**

- ✔ `d03-service-and-siting`, "Why simple cycle can win despite burning more
  fuel". The model's crossover is 4,800 hours. A data center runs near 8,760,
  where the same model gives simple cycle $51.8M against combined cycle $45.2M.
  The lesson never says its own cost model rejects simple cycle for this duty.
  The real argument, speed to power, arrives three sections later.
- ✔ Same lesson, "Price the operating penalty": it "continues the original
  comparison" but drops that model's $8M fixed-cost advantage. The net annual
  penalty is $6.6M, not $14.6M.
- ✔ `d06-eight-hundred-volt-architectures` never states why 800 V, and its
  worked example repeats `d04-conversion-placement`'s series-efficiency
  exercise, conceding the result follows "not from the label 800 V".
- ✔ `d05-protection-and-fault-domains` uses a 1,000 A illustrative fault with no
  realistic magnitude. It never gives the numbers that answer its own driving
  question: a transformer feeds a fault at roughly 15–20× rated current, a
  generator several times, an inverter 1–3×, which is why a breaker that trips
  on utility supply may not trip on UPS supply.
- `d03-voltage-and-distance`, titled "Move power with fewer amperes", lands on
  800 V DC = 125 A against 480 V three-phase = 120.3 A and moves on. The
  resolution (two conductors against three) is left to a slide.
- `d13-commissioning-complete-paths`: the practice cannot detect the error the
  lesson teaches, because the new intersection (60) equals the naive minimum.
- `d07-bottleneck-model`: the assumed 200 TFLOP/s puts the roofline ridge at
  25 FLOP/byte. Advertised Blackwell-class rates are PFLOP/s-scale, which would
  put the ridge in the hundreds, so the number a reader remembers is about an
  order of magnitude low. 2MKN is derived and never applied to a real matrix
  multiply (BF16 matrix–vector decode is near 1 FLOP/byte; a 4096² matrix–matrix
  product is near 10³, and that contrast is the lesson).
- `d02-productive-utilization`: the practice frames an 80 kW / 15 min run as
  power capping. Moderate GPU power caps usually *save* energy, so a learner may
  take away the opposite of field experience. Say the numbers are contrived or
  show both outcomes.

**Consistency**

- ✔ `d13-delivery-dependencies`: "those seven weeks of utility delay". The
  utility slipped 14 weeks; acceptance slipped seven after float absorbed the
  rest.
- ✔ `d04-read-the-power-train` says conversion placement is "taught there
  [Chapter 9] rather than repeated in Chapter 6", while
  `d04-conversion-placement` sits in Chapter 6 and teaches it.
- ✔ `d11-heat-rejection`: "The tower/dry-cooler temperature comparison therefore
  comes before the chiller balance in this chapter." False in reader order.
- ✔ `d08-copper-light-service`: body says 50 m multimode; its source note says
  30 m.
- ✔ `d07-bottleneck-model`: M and B name matrix dimensions, then bytes and
  bandwidth two paragraphs later.
- ✔ `d01-metrics-and-evidence` forbids calling a short-interval ratio PUE, then
  calls a one-hour ratio "the interval PUE".
- ✔ `d10-local-thermal-paths`: "about 8,292 litres per second at the stated
  densities and heat capacities". The values are never stated, and four figures
  is false precision. Say about 8.3 m³/s, roughly 3,500 times water's volume.
- `d05-storage-power-and-time`: the capacitor example sits on "a separate,
  hypothetical 800 V rack bus", then becomes "the DC link" restored by a UPS
  rectifier. The capacitor is also used two paragraphs before it is introduced.
- `d06-*`: the rack bus is 50–51 V, 48 V, "roughly 50 V" and 54 V in different
  lessons with nothing saying these are one 48 V-class bus. ±400 V is never
  written.
- `d11-weather`: "can sustain 8 MW IT in the cool bin" against the lesson's own
  inequality, which gives 8.53 MW.
- `d12-safety-and-control-boundaries`: the takeaway opens "Independent power
  equipment"; the scenario is two cooling trains.
- `c05-open-a-phase`: 1,000 locations × 100 kW on a 100 MW service leaves
  nothing for auxiliaries, straight after `c02` taught 100 − 25 = 75 MW.
- `d15-cost-per-service`: the heading "both sides of the balance sheet" covers
  revenue, cost and cash timing, which are not balance-sheet items.
  `d15-upgrade-and-evidence` has a typo: "The service does not..".

**Not verified by this audit.** Dated 2026 claims (SpaceX and Oracle filings,
rental-price ranges, "over 98 percent", "75 percent delivered") were not checked
against their sources. The research pipeline owns that.

## Reader versus recorded video

The video is frozen, so where the two disagree the reader has to move. Two
reviewers compared every deck's scenes, models and headline numbers with the
lessons its "Reading" links open. (Each scene's `reference` field decides where
that link lands, which also reveals lessons no slide points to.)

| Ch. | Deck | Alignment | Sharpest mismatch |
|--:|---|---|---|
| 2 | Data center overview | **Divergent** | Deck: ten 142 kW racks + 80 + 300 = 1,800 kW against a 2,000 kW nameplate; 144 MWh day; PUE 1.20 → 1.10. Reader: ten 100 kW racks → 1,320 kW; a 184 MWh day; a 1.25 "facility-to-IT energy ratio". All three sibling lessons use a different facility from the video, each with one bridge paragraph patched in. |
| 3 | Workloads | Aligned | All three worked examples match the deck. The weight-tile reuse slide gets one sentence. |
| 4 | Siting | Partial | Deck: 200 MW at 34.5 kV = 3.35 kA against 161 kV = 717 A. Reader's worked example: 10 MW at 10 and 20 kV. `d03-power-and-procurement` is referenced by no slide, and its solar example conflicts with the deck's "We are not assuming a solar plant". |
| 5 | Physical site | Partial | Deck: Lenovo GB300 rack at 1,580 kg, explicitly no equal-wheel-load assumption. Reader: 2,000/2,200 kg on four equal wheels. Meta's Prometheus tents are in the deck and in no d12 lesson. `d12-safety-and-control-boundaries` is referenced by no slide. |
| 6 | Distribution | Partial | The same 900 kW / 1,000 kVA example means different things. Deck: 900 kW real input at PF 0.8 → 1,125 kVA, 1,353 A, 112.5%. Reader: 900 kW DC output ÷ 0.96 at PF 0.90 → 1,041.67 kVA, 1,253 A, 104.17%. The lesson now contains both without drawing the contrast. The deck's beer-glass analogy is in no lesson. |
| 7 | Continuity | Partial | Deck teaches redundancy on a 100 kW load with 50 kW modules growing to 150 kW. Reader uses 6 MW with 2 MW modules. "Maintenance bypass", "N+2" and "2(N+1)" are on slides and in no lesson. |
| 8 | Rack power | Partial | The ledger matches. Meta's Clemente board (51 → 12 V) and the VRM ripple numbers (34–46 A against 38–42 A) are narrated and in no lesson. Several sections sit under the other chapter's lesson. |
| 9 | 800 V DC | **Divergent** | The deck's headline numbers, "one-third less copper", 434 W against 312.5 W and "28% less heat", appear in no lesson. The Reading link offers a 4.50% efficiency chain that the deck says its drawings do not establish. Deck naming is "in rack / sidecar / farther upstream" and Phases 1–3; the reader says "Architecture A/B/C". |
| 10 | Networking | Partial | `d08-topology-budget` matches. The deck's straggler slide (workers ready at 20/20/20/50 ms, so "all four ready at 50 ms") is the picture the lesson title "A collective makes waiting contagious" promises, but the lesson's example is a ring all-reduce at 30 ms. The 24,576-GPU slide has no mapped reading. |
| 11 | Chip and rack heat capture | Partial | Deck: 400 W over 4 cm² and 1 cm² → 100 and 400 W/cm²; reader: 16 cm² and 4 cm² → 25 and 100 W/cm². Deck: 100 kW, cp 4.18, 2.5 → 5 kg/s; reader: 84 kW, cp 4.2, 2 kg/s, and that 84 kW case then runs through two more lessons. Deck says "rack coolant loop" and "chip"; reader says "technology supply" and "junction". |
| 12 | Heat rejection | Aligned | Every shared number matches (the deck's model was built from the reader). The Toronto deep-lake cooling case, slides 18–21, is in no lesson. |
| 13 | EPC | Partial | ✔ Same rack sets, different answer. Deck: the overlap A21–A60 is "40 racks, or 8 MW", extending to "60 racks and 12 MW" (200 kW racks). Reader: "40 × 100 kW = 4,000 kW = 4 MW", then 6 MW. Deck says "FAT"; reader says "vendor factory test". The week-27 critical-path material belongs to retired slides. |
| 14 | Operations | Partial | ✔ Deck: cooling completes a "three-minute start" and "no permitted thermal buffer is specified". Reader: "two minutes" and a 0.04 MWh buffer. The deck's Row B is a real flow loss with a chip over its limit; the reader reuses the numbers as a stale sensor value. The Dalles and Llama 3 slides link to d14 lessons that contain neither; the matching text sits in the unmapped `d09` lessons. Metasys, Intel tanks and Row C are in no lesson. |
| 15 | GPU cloud economics | Partial | ✔ Deck: 80 h at 1 kW plus 20 h at 0.2 kW = 84 kWh → $0.084 and $0.168 per GPU-hour. Reader: 1 kW over all hours → $0.10 and $0.20. The three NVIDIA-backstop slides, Anthropic/Cursor–Fireworks and Core Scientific have no reading. Lesson ids still name the retired deck. |
| 16 | Putting an AI Factory Together | **Divergent** | The deck's driving question is "Why does the Abilene AI factory have this combination of infrastructure, financing and delivery choices?" and it follows that one real campus through generation role, cooling, the Blue Owl / Primary Digital capital stack and phased delivery. Its Reading link opens five unrelated hypothetical drills (`c01`–`c05`: a 2 MW hall, a 100 MW site, a one-rack room, a job, a 100 MW campus) with no landing note. The course's synthesis chapter has no reading, and the capital-stack slide has no reader text anywhere. Fix: write one Abilene companion lesson (start from `d15-upgrade-and-evidence`), and relabel `c01`–`c05` as optional practice. |
| 17 | ERCOT and PJM | Aligned with the committed deck | Partial against the uncommitted working-tree deck, which now says Dominion holds 53.8 GW of contracts where the reader says 47 GW. Which version was recorded could not be determined. Resolve this when that session commits. |

The two further-reading domains: roofline (`d07`) is taught in no deck. HBM,
checkpoints, Google's flexible scheduling and Meta's RSC *are* taught, inside
the workload, networking and operations decks, so the `d09` lessons hold the
reading for several Chapter 14 slides while being mapped to no chapter.

Terminology also differs: the decks say "coolant distribution unit" and "gray
space"; the reader uses "cooling distribution unit" half the time and "grey
space". Follow the decks.

**What to do.** For each chapter marked Divergent or Partial, make the deck's
running example the lesson's worked example, using the deck's numbers, and
delete the bridge paragraphs. Keep a reader-only example only where it teaches
something the deck does not, and introduce it as an extension ("the video used
10 racks at 142 kW; here is the same ledger when…"). Give every slide case that
has no reading a short treatment, and decide what to do with the lessons no
slide references: keep them as clearly labelled further reading, or fold them
into a lesson that is referenced.

## The plan

Ordered by value for effort, and by dependency. Phases 1 and 2 need no taste
decisions and could be done this week.

### Phase 1 — Stop publishing author notes (about half a day, code only)

1. Render sources as a bibliography: title, publisher, date, one-line claim.
   Stop rendering `limits` in `reader.js` and in the Markdown builder. This
   removes about 9,100 words of author notes from the learner's view in one
   commit and loses nothing, since `research/sources/*.md` keeps the full
   record and the reader already links to it. Then hand-edit the 31 entries in
   Appendix C whose `claim` text contains instructions.
2. Make `tradeoff` and `failure` optional in `build_expanded.py`. Keep them
   where they carry numbers; delete the rest rather than rewrite them.
3. Drop the "Generated reading view. Edit … then run …" banner and the
   "Authored draft" label from `lessons/*.md`. Those files are published.
4. Trim the disclaimer captions hard-coded in `reader.js` (14 strings, some
   shown under every lesson's mechanism cards).
5. Narrow `stage_site.py`. It publishes every `course/*.md` and
   `research/*.md`, so `FEEDBACK_AUDIT.md`, `COURSE_REVIEW.md`,
   `SPEAKER_NOTES.md` and `TESTING.md` are served from the course site root.
6. Replace the reader-related parts of `TEACHING_STANDARD.md` with the ten
   rules below, so the next agent to read it imitates the right voice.

### Phase 2 — Purge what the reader cannot see (about a day)

Work through Appendices A and B. For each slide or image reference choose one
of three fixes: embed the figure with a caption (the `figures` field already
exists and is used nine times), replace the sentence with two or three values
read off the figure, or cut it. Deleting alone is often the wrong fix: several
of these sentences say what an unseen figure is *not* and withhold what it
shows. Fix the defects in the Consistency list at the same time.

### Phase 3 — Realign with the recorded video

See "Reader versus recorded video". The video is frozen, so where the two
disagree the reader moves.

### Phase 4 — Re-voice from your own narration (the large one)

The cure for AI voice is a human one, and you have ten hours of it. Transcribe
the recorded video. For each lesson, use the transcript for order, emphasis and
phrasing, and the existing lesson for facts, numbers and sources. The reader
becomes what you said in the video, tightened, plus the derivations, practice
and sources the video had no time for. That also guarantees alignment.

Sequence it to avoid trading one tic for another:

1. Pilot three lessons by hand, or edit agent drafts heavily: one LIGHT, one
   HEAVY, one RESTRUCTURE. Suggested: `d10-flow-and-pressure`, `d01-boundaries`,
   `d03-service-and-siting`.
2. Freeze those three as the exemplars. Every later rewrite prompt includes
   them. Exemplars steer a model far more reliably than rules do, which is how
   the current standard produced the current voice.
3. Batch the rest in chapter order, since early chapters get the most readers.
4. Add back the missing signal as you go: expand each acronym at first use,
   name the standard term, state the rule of thumb, give the real number.
5. Turn on `prose_lint.py --check` in CI once the corpus is under budget, so
   later edits cannot drift back.

### Phase 5 — Restructure the outliers

Use the split table above, starting with `d03-service-and-siting` and
`d12-hazards-and-site-evidence`. Apply "one place carries the numbers"
everywhere. Move each chapter check above the sources and make it test its own
lesson.

### Phase 6 — Rebuild the glossary around what people look up

- Add the industry core that is used in lessons but undefined: token, PDU,
  switchgear, substation, 2N, redundancy, circuit breaker, relay, NVLink,
  scale-up and scale-out, KV cache, prefill, decode, training, inference,
  latency, utilization, cold plate, cooling tower, rear-door heat exchanger,
  immersion, manifold, ΔT, leaf and spine, commissioning (with L1–L5),
  COP, WUE, LLM, BMS, MW against MWh. A course called *From Watts to Tokens*
  has no glossary entry for "token".
- Demote about 40 course-coined process terms (Acceptance register, Authority
  boundary, Durability boundary, Interface register, Operating evidence,
  Denominator, Range, Workspace…) to the lessons that use them, or mark them as
  course terms.
- Merge the six duplicates (Approach temperature, Brownfield, Critical path,
  Service envelope, Gas lateral, Acceptance criterion). The builder silently
  keeps the first definition and drops the second; make it fail instead.
- Give each entry two sentences: what it is, and why it matters in a data
  center. Group by system (electrical, cooling, compute, network, delivery,
  commercial) as well as A–Z. 229 cards in one alphabetical grid is hard to
  browse.
- The Primer has no reading. A one-page "Primer vocabulary" that links its 21
  slides' terms into the glossary would give beginners a landing place.

### Phase 7 — When the video is published

Add a "Watch: chapter N, mm:ss" link to each lesson and glossary entry, tag the
recorded edition as `COURSE_REVIEW.md` already plans, and keep dated snapshot
boxes on a refresh schedule.

## Reader style rules

These replace the reader-related parts of `TEACHING_STANDARD.md`. They are
written the way the reader should sound.

1. **Teach first.** Say what is true and how it works. Add a qualification only
   when it would change what the learner does.
2. **Every "not" must pass the misconception test.** Would a smart newcomer
   really believe the thing being denied, and would believing it change a
   decision? If yes, keep the sentence and make it the point of the paragraph.
   If no, delete it. "PUE is not a measure of useful computation" passes. "The
   name does not encode the turbine's megawatt output" fails.
3. **One scope note per example.** The *Model boundary* line under each worked
   example already says the numbers are invented. Body paragraphs never repeat
   it, so "hypothetical", "illustrative", "supplied" and "original teaching
   input" leave the prose.
4. **Dated facts go in snapshot boxes:** claim, as-of date, source. The prose
   around them stays evergreen and the boxes can be refreshed without touching
   the explanation.
5. **The reader never mentions the slides, the deck, a review, or its own
   production.** If an image matters, embed it with a caption. If it does not,
   drop the reference.
6. **Open with the situation the title promises.** The definition comes second,
   attached to the object it describes.
7. **End each paragraph on the consequence,** stated positively.
8. **Plain verbs.** *Show, prove, tell, give, set* for "establish". *Given* for
   "supplied", "stated" and "declared".
9. **Sources are a bibliography:** author, title, date, one line on what the
   source supports. Review notes stay in `research/`.
10. **Vary the rhythm.** Let a long sentence carry a mechanism through its
    steps, then land the point with a short one.

## Before and after

Every fact in the "after" versions is already in the lesson. Nothing was
researched or added.

**A body paragraph** (`d01-boundaries`)

> *Before.* A detailed ledger is more work than one campus number, but it allows
> a useful question: did an improvement reduce electrical losses, cooling
> overhead, or the energy required per completed task? Those are different
> mechanisms. Reducing rack input by 100 kW normally reduces the corresponding
> heat source, whereas merely moving a converter outside the rack moves a
> heat-accounting boundary. A visually smaller rack loss does not prove that the
> facility uses less energy.

> *After.* A line-by-line ledger takes more work than one campus number, and it
> earns that work back the first time someone claims a saving. Ask which line
> moved: electrical losses, cooling overhead, or energy per finished task. Cut a
> rack's input by 100 kW and there is 100 kW less heat to remove. Move a
> converter out of the rack into the room next door and the rack's number falls
> by the converter's loss, while the facility's total stays exactly where it
> was. The loss has changed address.

**A dated case** (`d03-service-and-siting`, "Fuel reaches a site…", 174 words → 134 plus a 23-word snapshot line)

> *Before.* …A nearby pipeline is a possible connection point, not a promise of
> service. … These statements establish different pieces of the buildout; the
> presentation does not justify equating every lateral with the same project
> scope. No 12-inch pipe diameter was verified for this case. Likewise, the
> roughly 900 MMcf/day in the February release refers to three Oracle projects
> in aggregate, not the Abilene campus alone. The useful lesson is to establish
> a specific delivery route and commitment before converting regional gas
> abundance into an assumption about campus power.

> *After.* A gas turbine is only as useful as the pipe that feeds it. Being near
> a pipeline gives a site somewhere to connect. Burning gas at scale takes four
> more things: a lateral (a branch line from the main to the site), the rights
> of way to build it, metering and pressure regulation at the fence, and enough
> upstream capacity to hold pressure with every turbine at full output. Each is
> a construction project with its own schedule, running alongside the turbine
> order.
>
> Abilene shows the sequence. Energy Transfer began delivering gas to the campus
> in January 2026, completed a second 14-mile lateral in the area by August, and
> signed a separate agreement with Crusoe for gas facilities to feed about
> 900 MW of generation. The fuel arrived in stages, as the power did.
>
> **Snapshot, August 2026.** Energy Transfer Q4 2025 results and August 2026
> investor presentation. The release's ~900 MMcf/day figure covers three Oracle
> projects combined.

**A source entry** (`d03-service-and-siting`)

> *Before.* GE Vernova — What Is a Gas Turbine? — Explains compressor,
> combustion, turbine and generator; embedded original cutaway provides a real
> manufacturer visual for the simple-cycle mechanism. Read 2026-09-12. Cutaway
> is an explanatory rendering, not a photograph of a particular data-center
> installation. The image is unlabelled; add restrained overlay labels or
> explain orally.

> *After.* GE Vernova, *What is a gas turbine?* Compressor, combustor, turbine
> and generator, with a cutaway. Accessed 12 September 2026.

**A lesson opening** (`d10-local-thermal-paths`, "A cool room can contain an overheating chip"; a sketch to be checked against the lesson)

> *Before.* A cooling system has several jobs: capture heat at the hardware,
> transport it through the building, and reject it outdoors.

> *After.* The hall thermostat reads 22 °C. Inside one rack, a GPU is throttling
> at its temperature limit. Both readings are correct, and the gap between them
> is this lesson: heat has to be captured at the chip before the building can do
> anything with it.

**A missing glossary entry**

> **Token.** The unit of text a language model reads and writes, about
> three-quarters of an English word. Serving speed is quoted in tokens per
> second and price in dollars per million tokens, which is why the course ends
> there: tokens are what the data center finally produces. *First used in 3.1,
> Interactivity and total throughput.*

## Per-lesson verdicts

**LIGHT** (9): sound, line-edit for voice. **HEAVY** (20): content right, rewrite
paragraph by paragraph. **RESTRUCTURE** (22): regroup, split or merge; mostly
re-sorting material that already exists. Ordered by video chapter; "ref." marks
the two further-reading domains that have no deck.

| Ch. | Lesson | Verdict | Body words | ¶ end on negation | Slide refs | What it needs |
|--:|---|---|--:|--:|--:|---|
| 2 | `d01-boundaries` | HEAVY | 1,008 | 67% | 1 | Sound ledger. The GB300 paragraph is residue carrying a second, competing facility. Practice repeats the body. |
| 2 | `d01-metrics-and-evidence` | HEAVY | 863 | 45% | 1 | Spell out PUE, fix the "interval PUE" contradiction, turn the First-to-Sixth evidence list into a table. |
| 2 | `d01-power-over-time` | LIGHT | 846 | 64% |  | Clearest lesson in its group. Dedupe the worked example. |
| 3 | `d02-phases-and-envelopes` | RESTRUCTURE | 791 | 46% | 2 | Inference serving and training power rhythm are two lessons. "Envelope" is never defined in the body. |
| 3 | `d02-productive-utilization` | RESTRUCTURE | 310 | 33% |  | Never defines utilization. Duplicates its neighbours. Merge. |
| 3 | `d02-workload-brief` | RESTRUCTURE | 796 | 21% | 3 | Title, id and worked example are three topics. The brief itself is never shown. |
| 4 | `d03-power-and-procurement` | HEAVY | 830 | 64% |  | Numbers right. Core example labelled optional. REC, virtual PPA and hourly matching never named. |
| 4 | `d03-service-and-siting` | RESTRUCTURE | 3,610 | 58% | 10 | Four lessons in one. See split table and the simple-cycle reasoning gap. |
| 4 | `d03-voltage-and-distance` | RESTRUCTURE | 1,434 | 50% |  | Split the AC primer from the transport comparison. Teach that resistance grows with length. |
| 5 | `d12-hazards-and-site-evidence` | RESTRUCTURE | 2,451 | 62% | 2 | Eight method sections then eight cases in slide order. Split in three. |
| 5 | `d12-room-and-replacement-route` | LIGHT | 1,057 | 13% | 1 | Best of its group. Merge the two Lenovo sections. Do the floor-loading division it sets up. |
| 5 | `d12-safety-and-control-boundaries` | HEAVY | 723 | 50% |  | Abstract throughout. Make the two-train scenario the worked example. Name a concrete hazard. |
| 6 | `d04-conversion-placement` | RESTRUCTURE | 1,454 | 43% |  | Fair-comparison core is sound. The MV-to-800 V hardware block belongs in the 800 V chapter. |
| 6 | `d04-current-and-rating` | HEAVY | 1,371 | 39% | 1 | Core derivation is excellent. Back half is captions. Reactive power is defined in the last paragraph. |
| 6 | `d04-read-the-power-train` | RESTRUCTURE | 2,470 | 44% | 6 | A clean three-section lesson plus fourteen slide-ordered captions. |
| 7 | `d05-paths-and-transitions` | RESTRUCTURE | 1,912 | 57% |  | Argument ends after section 3. Split off Tiers, nines and Fairwater. |
| 7 | `d05-protection-and-fault-domains` | HEAVY | 1,402 | 55% | 1 | Correct but abstract. Needs realistic fault currents and a worked example on selectivity. |
| 7 | `d05-storage-power-and-time` | RESTRUCTURE | 2,252 | 57% | 1 | Three lessons interleaved. The hook arrives after 17 paragraphs. Practice answer printed in body. |
| 8 | `d06-conversion-ledger` | LIGHT | 1,343 | 53% |  | Best of its group. Delete the unseen-image section and strip hedges. |
| 8 | `d06-rack-migration` | RESTRUCTURE | 1,801 | 57% | 2 | Retrofit and buffering are separate lessons. Examples told two or three times. |
| 9 | `d06-eight-hundred-volt-architectures` | RESTRUCTURE | 1,393 | 57% |  | Never says why 800 V. Three unmapped naming schemes. Borrowed worked example. |
| 10 | `d08-collective-progress` | HEAVY | 736 | 30% |  | Strongest core. Show one slow edge stalling all workers, which is what the title promises. |
| 10 | `d08-copper-light-service` | HEAVY | 683 | 50% | 1 | "All wattages are invented" in a course about watts. Reconcile 50 m and 30 m. |
| 10 | `d08-topology-budget` | RESTRUCTURE | 1,446 | 25% | 2 | Split fabric budget from campus fibre and route diversity. |
| 11 | `d10-cdu-interfaces` | RESTRUCTURE | 1,431 | 41% |  | Strong core. Move the redundancy and capture-method sections out. |
| 11 | `d10-flow-and-pressure` | LIGHT | 609 | 12% |  | Tightest lesson in the corpus. Add the cube law and the 1.43 L/min per kW rule. |
| 11 | `d10-local-thermal-paths` | HEAVY | 1,065 | 43% |  | Physics right. Two of seven sections are caption residue. Hook buried. |
| 12 | `d11-heat-rejection` | HEAVY | 1,024 | 36% |  | COP treatment sound. Merge the bolted-on tower section. Cut the false ordering sentence. |
| 12 | `d11-water-and-heat-reuse` | LIGHT | 833 | 75% |  | Sound. Add the latent-heat link and define WUE. |
| 12 | `d11-weather-and-operating-envelope` | RESTRUCTURE | 1,600 | 71% |  | Three lessons in one. Worked example contradicts the title. |
| 13 | `d13-commissioning-complete-paths` | HEAVY | 597 | 22% |  | Strong core. Fix the practice. Map the six milestones onto L1–L5. |
| 13 | `d13-delivery-dependencies` | RESTRUCTURE | 1,607 | 45% |  | Two lessons joined by a slide insert. Example and practice cover different halves. |
| 13 | `d13-interface-contracts` | RESTRUCTURE | 2,085 | 68% |  | Best technical content in its group. Lead with the case. Cut the duplicate example. |
| 14 | `d14-coordinating-control-and-work` | LIGHT | 720 | 64% |  | Sound. Give the 0.04 MWh buffer a physical picture (about 7 t of water warming 5 K). |
| 14 | `d14-maintenance-and-service-reliability` | RESTRUCTURE | 844 | 46% |  | Three topics and three cases in slide order. Test the SLI against an SLO. |
| 14 | `d14-telemetry-and-observability` | LIGHT | 664 | 44% |  | Sound and concrete. Trim duplication. |
| 15 | `d15-capacity-ledger` | HEAVY | 331 | 17% |  | Correct but thin. Vacuous example and fields. |
| 15 | `d15-cost-per-service` | HEAVY | 430 | 43% |  | Revenue half excellent. Cost and financing half asserted, not taught. |
| 15 | `d15-upgrade-and-evidence` | RESTRUCTURE | 309 | 67% | 1 | Residue-laden. Belongs in Chapter 16 as the Abilene companion. |
| 16 | `c01-coupled-outage` | HEAVY | 376 | 100% |  | Give the thermal half numbers (2 MW × 12 min = 0.4 MWh of heat). Fewer disclaimers. |
| 16 | `c02-weather-capacity` | LIGHT | 337 | 25% |  | Clean binding-constraint drill. |
| 16 | `c03-density-retrofit` | HEAVY | 348 | 50% |  | Orphan "current ratio". Slide and NVIDIA residue. |
| 16 | `c04-stalled-job` | LIGHT | 327 | 25% |  | Best capstone. Name Amdahl's law. |
| 16 | `c05-open-a-phase` | HEAVY | 386 | 50% | 1 | Delete the Abilene paragraph. Make the reader derive the intersection. |
| 17 | `d03-interconnection-queues` | HEAVY | 1,025 | 50% |  | Facts and order sound. Prose mostly says what numbers do not mean. PUCT, SB 6, Batch Zero undefined. |
| ref. | `d07-bottleneck-model` | HEAVY | 690 | 30% |  | Math right. Fix the M/B symbol collision. Apply 2MKN to a real matrix multiply. |
| ref. | `d07-data-path` | HEAVY | 742 | 20% | 1 | Quantify all three paths. Connect 18 ms to a token rate. Drop the stale opener. |
| ref. | `d07-rack-as-system` | RESTRUCTURE | 596 | 44% |  | Example duplicates its own section and d09-service-acceptance. Rebuild around a tray pull. |
| ref. | `d09-checkpoint-timeline` | HEAVY | 843 | 50% | 1 | Best of D09. Lead with 419 interruptions in 54 days. Add Young/Daly and RPO/RTO. |
| ref. | `d09-service-acceptance` | RESTRUCTURE | 980 | 42% | 1 | Demand-response orphan. Trivial example. Promote the allocation-wait comparison. |
| ref. | `d09-storage-paths` | RESTRUCTURE | 974 | 18% | 1 | Merge "Teaching model" into the worked example. Stop printing the practice answer. |

Full metrics for any lesson: `python3 qa/reader/prose_lint.py`, and
`--list <lesson-id>` to print every flagged sentence.

## Appendix A — Sentences that reference slides or images the reader cannot see

**`d01-boundaries`**
- The opening presentation uses NVIDIA’s GB300 NVL72 as a real product anchor.

**`d01-metrics-and-evidence`**
- The opening presentation first isolates facility overhead.

**`d02-workload-brief`**
- The original image identifies 8k input / 1k output, TensorRT-LLM, FP8 and multi-token prediction.
- The older isolated 80 GB device example did not identify real hardware or establish this connection clearly; the presentation now compares named model uses directly rather than implying an H100 installation.
- The DeepSeek V4 technical-report chart on the slide shows another way to change the budget: compressed attention.

**`d02-phases-and-envelopes`**
- The presentation uses the standard prefill–decode split to make the hardware division clear.
- The presentation ends with a workload brief rather than arithmetic threshold quizzes.

**`d03-service-and-siting`**
- Two genuine Building 1 aerials from Applied Digital’s October 2025 investor presentation appear beside the handover milestones.
- These statements establish different pieces of the buildout; the presentation does not justify equating every lateral with the same project scope.
- Oracle’s photograph shown in the presentation is an aerial dated July 15, 2026.
- The presentation uses GE Vernova’s original gas-turbine and generator cutaway, then Siemens Energy’s combined-cycle principle diagram.
- Follow the compressor, combustor, turbine and generator in the first image.
- The manufacturer diagram is a simplified mechanism drawing; its up-to-64% label is an illustrative vendor maximum, not a universal operating efficiency.
- The manufacturer graphic illustrates operating roles rather than measured grid data.
- The campus AC transport penalty on the preceding slide is a different mechanism from gas-turbine thermal efficiency.
- The slide places Census state-boundary geometry over a wider USGS historical aerial, alongside the original permit plan.
- This replaces the separate schematic border slide.

**`d04-read-the-power-train`**
- The slides use a separate row example with balanced 415 V line-to-line AC, power factor one, and a supplied 250 A usable current budget.
- The slide uses the supplied labeled Siemens NXAirS cutaway, with the breaker, earthing-switch and cable-connection leader endpoints corrected against catalog HA 1702, page 12.
- Hitachi’s CPB family covers 72–800 kV and provides a concrete manufacturer reference for the slide’s conceptual 345 kV measurement view; no specific Abilene instrument-transformer model is asserted.
- The slide’s CT provides current, its CVT provides voltage, and the relay can use the measurements needed by its protection function.
- The slides distinguish these jobs before Chapter 7 examines fault zones and alternate supply paths.
- The slide compares these jobs without prescribing universal voltages.

**`d04-current-and-rating`**
- The comparison before the interactive slide keeps real power at 900 kW and balanced three-phase voltage at 480 V line-to-line.

**`d05-storage-power-and-time`**
- The presentation therefore shows both generator-only supply and generator supply plus battery recharge.

**`d05-protection-and-fault-domains`**
- The device’s DC voltage and interrupting ratings must match the circuit; the animation supplies no product rating or clearing-time claim.

**`d06-rack-migration`**
- The product photographs in the presentation show Delta’s removable 3 kW BBU and its six-module, 15 kW Battery Backup System.
- The supplied recharge slide uses an 8 kJ burst followed by 10 kW of available recharge power.

**`d07-data-path`**
- The presentation uses 8 TB/s as the ceiling of a controlled transfer account, not as an observed sustained rate.

**`d08-topology-budget`**
- The slide’s NVLink example shows communication within a scale-up domain.
- The slide shows one path through the network, while the complete reference fabric provides many links and alternative paths.

**`d08-copper-light-service`**
- The deck compares three supported reaches in NVIDIA’s 400G LinkX product family: a 2 m passive copper cable, 50 m multimode optics and 500 m single-mode DR4 optics.

**`d09-storage-paths`**
- The article’s 16 TB/s figure was a phase-two target, so the slides do not treat it as a demonstrated rate.

**`d09-checkpoint-timeline`**
- The slides compare the energy spent repeating computation at 1 MW.

**`d09-service-acceptance`**
- Google does not provide a measured megawatt saving for the slide exercise.

**`d12-room-and-replacement-route`**
- The presentation shows the manufacturer’s rack and rear-tray photographs so the water connections and scale are visible.

**`d12-hazards-and-site-evidence`**
- A separate slide bullet about a completed Abilene lateral does not identify that lateral as the Crusoe project.
- The consolidated slide shows the original campus plan beside a shared-entry counterexample and a three-entry topology sketch.

**`d15-upgrade-and-evidence`**
- The neighboring Microsoft project is not required to explain these milestones and is omitted from the presentation.

**`c05-open-a-phase`**
- The slide sequence uses an Oracle data-hall aerial identified as Abilene and dated July 15, 2026.


## Appendix B — Review and fact-check residue in body prose

**`d02-workload-brief`**
- The older isolated 80 GB device example did not identify real hardware or establish this connection clearly; the presentation now compares named model uses directly rather than implying an H100 installation.

**`d03-service-and-siting`**
- No 12-inch pipe diameter was verified for this case.
- The conditional full-service sum is $2.17 billion per month before costs; October is still future as of this September 12 review.
- This replaces the separate schematic border slide.

**`d05-storage-power-and-time`**
- As of this 15 September 2026 review, the current expanded installation’s verified IT/nameplate load, full-site load and qualified battery discharge MW remain unknown; the pilot comparison does not fill those gaps.

**`d05-paths-and-transitions`**
- No verified four-nines primary claim for Abilene was established in this review.

**`d06-eight-hundred-volt-architectures`**
- The course comparison asks which functions moved and which must be revalidated.

**`d08-copper-light-service`**
- Its advertised savings and reliability ratios are not adopted here as universal field measurements.

**`d13-interface-contracts`**
- Deleting half the floor area or cutting off alternate manifold branches before this review would commit unverified geometry.

**`d15-cost-per-service`**
- Missing public three- and five-year numeric quotes are not filled with invented estimates.

**`d15-upgrade-and-evidence`**
- The neighboring Microsoft project is not required to explain these milestones and is omitted from the presentation.


## Appendix C — Source annotations containing instructions or retrieval notes

**`d01-boundaries`**
- *NVIDIA NVL72 AI Factory — System Hardware & Components* — “…d storage networks, management, power shelves and cooling interfaces. Use the component hierarchy rather than treating the rack as a collection of identical GPU power ratings. Opening pro…”

**`d03-voltage-and-distance`**
- *SpaceX 10GW in 2027 — construction pace and equipment procurement* — “…Colossus site. No market, revenue or 2027 capacity forecast adopted. Do not rewrite this as all site equipment operating at MV.…”

**`d03-service-and-siting`**
- *Applied Digital — Applied Digital Achieves Ready for Service for Phase* — “…llendale, North Dakota reached ready-for-service on October 27, 2025. Use as an actual phased handover example. Operator announcement of ready-for-service capacity, not measured draw or…”
- *Energy Transfer — Energy Transfer August 2026 Investor Presentation* — “…behind a campus. August presentation; some statements are forecasts. Do not equate the 14-mile lateral with the exact Crusoe 900 MW agreement without explicit support. A 12-inch pipe di…”
- *Crusoe — Crusoe 2025 Impact Report* — “…ort . Operator-reported case, not independent commissioning evidence. Do not imply 350 MW backs up the full 1.2 GW campus. Repeated Sparks availability figures are not a newly measured S…”
- *Siemens Energy — Combined Cycle Power Plants* — “…ginal full-system diagram, plus single-shaft and multi-shaft layouts. Appropriate for a diagram-dominant CCGT lesson. Manufacturer illustrations simplify auxiliaries. The displayed up-to-64% figu…”
- *Siemens Energy — Peaker Plants* — “…Supplies a strong diagram comparing conventional generation roles with renewable-driven load following, and explains why fast f…”
- *GE Vernova — What Is a Gas Turbine?* — “…ph of a particular data-center installation. The image is unlabelled; add restrained overlay labels or explain orally.…”
- *Mortenson — Abilene Data Center Development* — “…lestone and a planned October 2026 temporary-transformer replacement. Preserve event dates and forecast status; no later completion was established.…”
- *GE Vernova — 7HA gas turbines, model family and specifications* — “…ly and public simple-cycle table with ISO and natural-gas conditions. Do not mix its 430 MW simple-cycle output or 21-minute hot start with the separate 640 MW 1×1 combined-cycle catalog…”
- *Applied Digital — October 2025 investor presentation* — “…ober presentation date; exact photograph capture days unknown. Photos must not be labeled as Oct 27 or Nov 24 captures.…”
- *MDEQ — Determination letter on portable gas combustion turbines, July * — “…ine treatment. Indexed primary text reviewed; full PDF fetch returned HTTP 403. Does not establish indefinite or current permission.…”

**`d04-current-and-rating`**
- *Schneider Electric — Definition of reactive power* — “…displacement PF interpretation assume sinusoidal voltage and current. Do not infer Q from true PF alone under harmonic distortion.…”

**`d04-conversion-placement`**
- *DOE — Best Practices Guide for Energy-Efficient Data Center Design* — “…ct electrical losses and operating efficiency. Read sections 6.1–6.3. Do not reuse the guide’s historical comparison as evidence for present architecture-wide savings; all efficiencies h…”

**`d05-storage-power-and-time`**
- *Crusoe and Redwood — Sparks microgrid update* — “…sion to 24 modular data centers is announced, not confirmed complete. Do not carry forward the initial off-grid description as present status.…”
- *Crusoe — 2025 Impact Report* — “…ort . Operator-reported case, not independent commissioning evidence. Do not imply 350 MW backs up the full 1.2 GW campus. Repeated Sparks availability figures are not a newly measured S…”

**`d06-eight-hundred-volt-architectures`**
- *OCP — Data Center Facility: Low Voltage Direct Current Power Distribut* — “…Introduction and document metadata inspected. The exact origin of the user-supplied image remains unverified. Do not assign a figure number, mandate this topology, or treat these alternatives a…”

**`d06-rack-migration`**
- *Delta Electronics — 3 kW BBU and 15 kW Battery Backup System* — “…ears of service, with 0–40°C operating range. The 15 kW system rating must not be replaced by the sum of six 3 kW module ratings. Product photos do not identify equipment installed in an N…”

**`d08-topology-budget`**
- *Juniper — Understanding Layer 3 Fabrics* — “…used in Ethernet Clos fabrics, independently of NVIDIA GPU hardware. Use the topology explanation, not the historical switch rates as current product recommendations.…”

**`d12-hazards-and-site-evidence`**
- *Energy Transfer — Q2 2026 investor presentation* — “…Primary search-extracted slide text reviewed; full PDF fetch returned HTTP 403. An agreement is not operational completion. A separate bullet about a completed 14-mile Abilene lateral is n…”
- *DOE — CHP Technologies: Gas Turbines* — “…pressor. Primary searchable PDF excerpt reviewed; full fetch returned HTTP 502. No generic pressure, efficiency or cost is adopted as an actual data-center turbine specification.…”
- *Applied Digital Achieves Ready for Service for Phase 1 at Polaris Forg* — “…llendale, North Dakota reached ready-for-service on October 27, 2025. Use as an actual phased handover example. Operator announcement of ready-for-service capacity, not measured draw or…”
- *Fermi — Q3 2025 Form 10-Q, Note 8* — “…ommenced in September 2025 after conditions were satisfied or waived. Do not describe the original commencement condition as currently unresolved.…”
- *Equinix statement — HO1 online but customer access flooded, August 28,* — “…l and staffed, surrounding roads closed, customer access unavailable. Use the attributed original statement. The article’s flood photo is a different identified street and is not used as…”
- *QTS — Suwanee campus* — “…plan image. Current page calls redundant campus conduits in progress. Do not infer completed end-to-end diversity from the January 2023 article.…”
- *ADA Infrastructure — Docklands campus planning announcement* — “…the proposed campus visualization. Historical planning announcement. Do not treat the image or planned capacity as completed construction or current operating power. Existing P144 suppo…”

**`d12-safety-and-control-boundaries`**
- *OSHA — 29 CFR 1910.36(b), number and separation of exit routes* — “…istance, occupant capacity, evacuation time or regulatory compliance. Do not infer that exactly two exits always suffice or that a shared segment is categorically prohibited.…”

**`d14-coordinating-control-and-work`**
- *Google DeepMind — Safety-first AI for autonomous data centre cooling a* — “…ic temperature limits in teaching interactions are original examples. Do not imply 30% lower whole-facility energy; the article compares cooling efficiency with a historical baseline.…”

**`d14-maintenance-and-service-reliability`**
- *Google Cloud — July 2022 europe-west2 cooling incident report* — “…ange initially avoided all three zones rather than the affected zone. Use the final July 29 summary, not the superseded July 21 preliminary timings. These are reported milestone endpoints…”

**`d03-interconnection-queues`**
- *Texas Legislature — SB 6 enrolled text, 89th Legislature* — “…om financial security, construction payments and electricity charges. Do not substitute unverified September 2026 implementation terms.…”
- *FERC — PJM large-load show-cause order, June 18, 2026* — “…r; preliminary proposed study reforms are not operating entitlements. Do not claim that load-related transmission requests can never share PJM's New Services Queue.…”


