# Feedback verification

Updated **12 September 2026**. This is a request-by-request record of the course
changes, including work that still needs review or publication. It does not claim
that the entire course has finished presentation slides.

The detailed primer feedback was supplied after the author clarified that the
original message had not been sent. It is now part of the implementation
checklist below. The later naming request is applied as **Primer** and descriptive
topic names in the public interface; existing internal IDs and URLs remain stable.

**Status key:**

- **Implemented in source:** the stated content or behavior is present in the
  local files inspected for this audit. This does not establish visual quality or
  that the current revision is on the website.
- **Review pending:** an assigned editor is revising it, or the requested result
  still needs an independent check.
- **Previously published:** an earlier version was committed and pushed. The
  publication section distinguishes that version from this revision.
- **Recorded verification:** the earlier task recorded the result; any fresh
  check and its limits are stated separately.

## Primer

| Request | Status and implementation | Review location |
| --- | --- | --- |
| Keep the primer separate from the historical 22-lesson introduction. | **Implemented in source.** The primer is a separate visual sequence before the main course. The retained 22-lesson introduction remains a historical resource. | [Primer](prototypes/terminology-format.html?teach=1); [course source index](README.md#retained-introduction-and-research) |
| Preserve the existing overview instead of turning it into the primer. | **Implemented in source.** The overview retains its thirteen authored scenes. Navigation labels and a check-in link have been updated around that content. | [Data center overview](prototypes/orientation-format.html?teach=1) |
| Aim for about 20 minutes of useful first exposure. | **Implemented in source; rehearsal pending.** The inspected primer has nineteen scenes with planned cues totaling 1,205 seconds, about 20 minutes. Those cues are not a measured teaching runtime. The teaching goal is that a beginner can recognize some of an expert conversation. | [Scene content](prototypes/terminology-scenes.js); [teaching standard](TEACHING_STANDARD.md) |
| Remove a redundant introduction slide. | **Implemented in source.** The sequence starts with a working circuit. The old welcome link resolves to that scene without adding a separate slide. | [Current needs a complete loop](prototypes/terminology-format.html?teach=1#circuit) |
| Replace confusing domain-code labels with topic names; call the opening Primer and remove the optional label. | **Implemented and checked.** The primer, navigation, accessibility labels and current course guidance use **Primer** and descriptive topic names. Objective descriptions replace codes in the reader. Internal IDs and archived verification logs retain their technical identifiers. | [Primer shell](prototypes/terminology-format.html); [reader navigation](https://github.com/kiankyars/gigawatt/blob/main/course/web/reader.js) |
| Remove “Skip to D01.” | **Implemented and checked in the built-in browser.** The skip route is absent from the inspected primer files. | [Primer shell](prototypes/terminology-format.html) |
| Remove references to later chapters and promises that a term will be explained later. | **Implemented and verified by the source sweep.** The inspected scene explanations stay within the primer. This applies to visible copy, diagrams, explanations and navigation, not only the main heading. | [Scene content](prototypes/terminology-scenes.js); [diagrams](prototypes/terminology-visuals.js); [electrical diagrams](prototypes/terminology-electricity.js) |
| Explain AC in terms of voltage changing polarity. | **Implemented and checked in the built-in browser.** The AC heading says that voltage changes polarity. Its explanation distinguishes voltage polarity from current direction and shows current reversal for a resistor. | [AC voltage changes polarity](prototypes/terminology-format.html?teach=1#ac-dc) |
| Add a follow-up showing non-sinusoidal AC: square, sawtooth and triangle or zigzag. | **Implemented and checked in the built-in browser.** A separate scene compares all four waveform shapes and distinguishes these examples from normally sinusoidal utility supply. | [AC waveform shapes](prototypes/terminology-format.html?teach=1#ac-shapes) |
| Say that three-phase is the predominant AC distribution used in data centers. | **Implemented and checked in the built-in browser.** The scene states this directly, while retaining the distinction that individual loads can use single-phase AC or DC. | [Three-phase AC](prototypes/terminology-format.html?teach=1#three-phase) |
| Give power factor its own motivated follow-up. | **Implemented and checked in the built-in browser.** Two 8 kW loads require 8 kVA at power factor 1 and 10 kVA at 0.8. The point is additional current capacity at fixed voltage, rather than an unexplained term attached to three-phase AC. The explanation distinguishes power factor from efficiency. | [Power factor](prototypes/terminology-format.html?teach=1#power-factor) |
| Preserve transformer, rectifier, inverter and power supply material. | **Implemented in source.** Their separate functions remain in one converter scene. | [Conversion equipment](prototypes/terminology-format.html?teach=1#conversion) |
| Preserve the UPS introduction. | **Implemented in source.** It still locates the rectifier, DC link, inverter, battery and upstream generator by their roles. | [UPS, battery and generator](prototypes/terminology-format.html?teach=1#backup) |
| Follow UPS with offline versus online operation and familiar applications. | **Implemented and checked in the built-in browser.** The new comparison changes both supply paths during an interruption. It connects standby systems to desktop computers and online double-conversion systems to critical data-center and sensitive medical loads. Application examples are not a claim that all medical equipment requires one topology. | [Offline and online UPS](prototypes/terminology-format.html?teach=1#ups-types) |
| Remove the N+1 line promising a later surviving-service test. | **Implemented in source.** That cross-reference is absent. The useful N+1 definition remains with its simple capacity example. | [Load, rating and redundancy](prototypes/terminology-format.html?teach=1#capacity) |
| Use ordinary English, especially for load versus rating. | **Implemented and reviewed.** The capacity heading now says “A 100 kW load needs two 50 kW modules.” All primer headlines use plain English without semicolon constructions, and repeated diagram recaps have been reduced. | [Scene headings](prototypes/terminology-scenes.js) |
| Make memory versus storage useful, or remove it. | **Implemented and checked in the built-in browser.** A saved model moves from storage into RAM and GPU working memory before execution. The example supplies a reason for naming the different locations. It is one common loading path, not the only possible architecture. | [Loading a saved model](prototypes/terminology-format.html?teach=1#memory-storage) |
| Make bandwidth and latency useful, or remove the weak treatment. | **Implemented and checked in the built-in browser.** An 8 MB payload uses either a 100 or 1,000 Mb/s link while first-bit travel remains 20 ms. The comparison shows which part of the completion time changes. | [Bandwidth and latency](prototypes/terminology-format.html?teach=1#network) |
| Improve heat-transfer rate versus temperature with a cold-plate example. | **Implemented and checked in the built-in browser.** A chip, cold plate and warming coolant carry distinct temperature labels and a 500 W heat-transfer arrow. Temperatures and energy per second refer to the same physical path. | [Heat and temperature](prototypes/terminology-format.html?teach=1#heat-temperature) |
| Keep the cooling/cold-plate mechanism. | **Implemented in source.** A separate scene follows coolant through a cold plate and CDU, with heat crossing between two fluid loops. | [Cooling path](prototypes/terminology-format.html?teach=1#cooling) |
| Remove the final reassurance quotation and empty closing slide. | **Implemented in source.** The sequence ends with a substantive PUE example. The old closing link resolves to that scene. The reassurance quotation is absent. | [PUE](prototypes/terminology-format.html?teach=1#pue) |

## Cases and recurring campus

| Request | Status and implementation | Review location |
| --- | --- | --- |
| Confirm Abilene as the recurring real campus. | **Implemented in source and previously published.** The original Crusoe-built Stargate campus in Abilene, Texas is the reference. The adjacent Microsoft development is a separate project. Illustrative calculations do not become claimed Abilene measurements. This is a recurring teaching reference; it is not yet a complete interactive as-built campus model. | [Authoring rule](TEACHING_STANDARD.md#abilene-and-the-recurring-case-studies); [Abilene capacity case](prototypes/case-studies.html?teach=1#abilene-ledger) |
| Explicitly teach greenfield versus brownfield. | **Implemented in source; discoverability changes awaiting publication.** The land lesson now names the comparison in its summary and a dedicated section, and its glossary uses redevelopment terminology consistently. Relevant case-slide links appear beside the lesson introduction. | [Land lesson](index.html#d12-hazards-and-site-evidence); [land comparison slides](prototypes/case-studies.html?teach=1#land) |
| Use original Colossus as the brownfield case. | **Implemented in source and previously published.** The case identifies the reused Electrolux factory in Memphis, Tennessee. A historical utility split, 8 MW from the existing substation plus 142 MW from a new one, shows why reusing a building does not remove the need for new services. No unsupported matched cost saving or contamination designation is claimed. | [Original Colossus](prototypes/case-studies.html?teach=1#colossus); [written case](lessons/d12-hazards-and-site-evidence.md) |
| Teach the SemiAnalysis account of using medium voltage because high-voltage equipment could not be procured quickly enough. | **Implemented in source and previously published.** The case attributes the procurement explanation to the reviewed SemiAnalysis passage in its Southaven/MiniHard discussion. It shows the reported route from generation through MV distribution and MV/LV transformers, and separately teaches the current tradeoff. It does not relocate that evidence to original Colossus or claim all xAI equipment is exclusively MV. | [Procurement case](prototypes/case-studies.html?teach=1#procurement); [current comparison](prototypes/case-studies.html?teach=1#current); [source record SA42](../research/sources/SA42.md) |
| Teach Crusoe's solar-powered data-center example. | **Implemented in source and previously published.** The case is Crusoe/Redwood in Sparks, Nevada, with reported 12 MW solar and 63 MWh battery ratings. It teaches power versus energy, ideal runtime and the role of grid backup. Availability is not misrepresented as solar energy share or proof of uninterrupted solar-only operation. | [Solar and batteries](prototypes/case-studies.html?teach=1#sparks); [availability](prototypes/case-studies.html?teach=1#availability) |
| Add other compelling cases and teach their consequences. | **Implemented in source and previously published.** Further cases cover Abilene's cooling path, Google's deferral of eligible work and Abilene capacity milestones. Each has a prediction, answer and explanation. These are short authored case slides and linked reader treatments; they have not yet been woven into every future full chapter presentation. | [Abilene cooling](prototypes/case-studies.html?teach=1#abilene-cooling); [Google scheduling](prototypes/case-studies.html?teach=1#demand-response); [capacity milestones](prototypes/case-studies.html?teach=1#abilene-ledger) |

## Check-ins, workload slides and delivery exercise

| Request | Status and implementation | Review location |
| --- | --- | --- |
| Add an active check-in after each domain. | **Implemented in source and previously published in the reader.** There are fifteen check-ins, each on its domain's final reading lesson, with a prediction prompt, answer reveal and transition. Responses are local to the page. The links below identify every check-in. Full slide adaptations for the remaining domains are not yet complete. | [Check-in source](domain-checkins.json); [reader implementation](https://github.com/kiankyars/gigawatt/blob/main/course/web/reader.js) |
| Make check-ins reachable from the actual overview and workload presentations. | **Implemented in source; publication pending.** Their final actions lead directly to the corresponding check-in. Both final actions were clicked in the built-in browser and focused the correct rendered check-in. Revealing an answer and continuing to the next topic were also checked. | [Overview check-in](index.html?checkin=1#d01-metrics-and-evidence); [workload check-in](index.html?checkin=1#d02-phases-and-envelopes) |
| Create the next workload teaching section with separate agents. | **Previously published.** The delegation history confirms separate teaching and model agents configured as GPT-6 Astra with Ultra reasoning. Nineteen authored scenes cover workload requirements, memory, useful output, latency, batching and demand over time, with shared calculations and longer reading explanations. This sequence still needs an aloud dry run and learner review. | [Workloads and requirements](prototypes/workload-format.html?teach=1); [scene source](prototypes/workload-scenes.js) |
| Carry the earlier minimal-text visual feedback into the workload slides; remove excessive subtitles. | **Implemented and independently reviewed; publication pending.** A dedicated editor revised all nineteen scenes, removed the course eyebrow, displayed boundary paragraph, SVG subtitle banners and narrative recaps, and simplified every headline. Definitions and longer explanations remain in the Explanation dialog. All 82 scene/state/layout combinations passed static rendering and SVG XML checks. The built-in browser review covered all nineteen default scenes at desktop and mobile sizes; three chart-label collisions were corrected and rechecked. | [Workload presentation](prototypes/workload-format.html?teach=1); [visual source](prototypes/workload-visuals.js) |
| Strengthen the delivery lesson with a concrete site-built versus prefabricated/modular comparison. | **Implemented in source and previously published.** The delegation history confirms the requested GPT-6 Astra agent with Ultra reasoning. The reading lesson separates EPC responsibilities from manufacturing strategy; identifies factory and site work; explains parallel schedules, design freezes, transport and module-interface ownership. The stipulated comparison completes at week 16 for site assembly and week 12 for prefabrication with approved inputs. | [Delivery dependencies](index.html#d13-delivery-dependencies); [written lesson](lessons/d13-delivery-dependencies.md) |
| Keep 20 MW fixed while 200 × 100 kW racks become 100 × 200 kW just before fabrication. Require electrical, hydraulic, spatial and scheduling reasoning. | **Implemented in source and previously published.** The linked exercise includes revised branch current, coolant flow and pressure, local support loads, interface locations, transport and resource dates. It identifies what may proceed, the affected holds, responsible owners and evidence for release. The examples are original engineering exercises, not an actual site's approved design. | [Interface exercise](index.html#d13-interface-contracts); [written lesson](lessons/d13-interface-contracts.md); [delivery check-in](index.html?checkin=1#d13-commissioning-complete-paths) |
| Extend scheduling and interface teaching rather than relying on aggregate arithmetic. | **Implemented in source and previously published.** With revised approvals at week 3, the stipulated modular finish moves to week 14; at week 5 it moves to week 16. Package releases, factory slots, delivery and site acceptance remain distinct. These additions are in the reader and check-in, not a new complete delivery slide deck. | [Dependency exercise](lessons/d13-delivery-dependencies.md); [acceptance lesson](lessons/d13-commissioning-complete-paths.md) |

### All fifteen domain check-ins

These links open the check-in directly in the current reader implementation. The
order follows the teaching sequence, which places physical siting after supply.

| Topic | Check-in |
| --- | --- |
| Data center overview | [What does the meter establish?](index.html?checkin=1#d01-metrics-and-evidence) |
| Workloads and requirements | [Same hardware, different service](index.html?checkin=1#d02-phases-and-envelopes) |
| Siting, grid connection and supply | [Can this phase open?](index.html?checkin=1#d03-service-and-siting) |
| Physical site, buildings and safety | [It fits until replacement day](index.html?checkin=1#d12-safety-and-control-boundaries) |
| Campus and building power distribution | [Which rating stops the load?](index.html?checkin=1#d04-conversion-placement) |
| Continuity, storage and protection | [Maintenance, then another loss](index.html?checkin=1#d05-protection-and-fault-domains) |
| Rack power and the 800 V DC transition | [Did moving the converter save energy?](index.html?checkin=1#d06-rack-migration) |
| Compute, memory and the rack | [Compute check-in](index.html?checkin=1#d07-rack-as-system) |
| Networking and interconnects | [Network check-in](index.html?checkin=1#d08-copper-light-service) |
| Storage, orchestration and recovery | [Service acceptance check-in](index.html?checkin=1#d09-service-acceptance) |
| Chip and rack heat capture | [Cooling-interface check-in](index.html?checkin=1#d10-cdu-interfaces) |
| Heat rejection, climate and water | [Heat and water check-in](index.html?checkin=1#d11-water-and-heat-reuse) |
| Design, procurement and commissioning | [Delivery and interfaces check-in](index.html?checkin=1#d13-commissioning-complete-paths) |
| Controls, operations and reliability | [Operations check-in](index.html?checkin=1#d14-maintenance-and-service-reliability) |
| Capacity, cost and system decisions | [System decision check-in](index.html?checkin=1#d15-upgrade-and-evidence) |

## Browser cleanup and publication

| Request | Status and verification limits |
| --- | --- |
| Investigate the Chrome for Testing pop-ups and remove the testing browser. | **Recorded verification, with a limited fresh check.** The earlier investigation attributed the notifications to the testing browser and its helper, recorded removal of the cached browser/profile/downloads and both notification registrations, and reported no remaining matching processes. This audit found no Chrome for Testing application at the standard application locations, no matching process, and no browser executable in the inspected Playwright cache. The remaining cache contains FFmpeg and package-link metadata. This is not a new comprehensive malware scan or a fresh inspection of all System Settings entries. |
| Use the built-in browser for further visual testing. | **Implemented as a project rule.** [Testing instructions](TESTING.md#desktop-browser-preference--2026-09-12) prohibit downloading or launching standalone Chrome for Testing or Playwright browser binaries on this Mac. The current review used the built-in browser for both nineteen-scene presentations, explanations, representative controls, case discoverability and presentation-to-check-in navigation. No standalone browser was launched for this revision. |
| Push changes so the material can be read on the website. | **Earlier material published; this revision pending.** Commit `f278c6b` published the primer, workload sequence, cases and check-ins. Commit `f2cd565` published the delivery exercise. Current primer edits, workload copy cleanup, topic-name changes and discoverability changes must still be committed, pushed and checked against the live website. |
| Provide written verification of every suggestion. | **This record.** Pending items remain visible until the corresponding review or publication actually succeeds. Source presence, automated checks, rendered inspection and teaching rehearsal are different kinds of evidence. |

Public review endpoints are the [Primer](https://kiankyars.github.io/gigawatt/course/prototypes/terminology-format.html?teach=1),
[Workloads and requirements](https://kiankyars.github.io/gigawatt/course/prototypes/workload-format.html?teach=1),
[case-study slides](https://kiankyars.github.io/gigawatt/course/prototypes/case-studies.html?teach=1)
and [reading companion](https://kiankyars.github.io/gigawatt/course/index.html).
Until the current revision is deployed and checked, these may show the previously
published content rather than the local changes described above.

### Verification for this revision

- The primer has nineteen scenes and 1,205 seconds of planned cues. Static checks cover every diagram/control state, arithmetic, UPS paths, sequence, aliases and the absence of chapter/reference pointers.
- All 57 Python tests and 94 JavaScript model tests pass. Historical course, expanded reader, domain map and research metadata freshness checks pass. The expanded course has 50 lessons, 65 objectives and five capstones.
- The built-in browser review covered all nineteen default scenes of each revised presentation at 1280 × 720 and 390 × 844. It checked SVG text bounds and collisions, horizontal overflow and representative screenshots. Additional interactions covered AC polarity, UPS interruption, network speed, training device count, answer reveal and both Explanation dialogs. Both presentation check-in actions were followed successfully.
- **Publication pending:** commit and push this reviewed revision, confirm the exact Pages deployment, and compare the deployed files before updating this record.
- **Teaching validation remains:** rehearse the sequences aloud and obtain learner feedback. Planned cues and software checks do not establish teaching time or comprehension. Full authored slide decks for the remaining course topics are separate ongoing work.
