# Course verification

## Desktop browser preference — 2026-09-12

Use the built-in Codex browser for interactive and visual checks on this Mac.
Do not download or launch standalone Chrome for Testing or Playwright browser
binaries here. Existing browser test harnesses remain available for a separately
configured test environment; run local model and build checks without a browser.

## Chapter 6 overview sequence and image review — 2026-09-15

- **25 scenes.** Original overview is unchanged; focused repeats call the same
  renderer with an outline overlay. Across all three load choices and both
  layouts, removing that overlay and its accessible description recovers the
  original SVG exactly. Switchgear detail precedes the 480 V focus and expanded
  conductor drawing. Stable existing hashes retained.
- Native browser checks at **1280 × 720** and **390 × 844** covered the focus
  outlines, overview-to-detail navigation, Compass co-design layout, separate
  tap photograph and selected PF image. Images preserve their supplied bytes;
  no new image generation or standalone browser installation was needed.
- Also exercised and inspected the existing CT + CVT measurement view on desktop
  and phone, completing that specific previously blocked interaction check.
- Compared all four PF figures. Selected the two-column supplied comparison;
  independently verified 900/1125 kVA, 1083/1353 A and 90/112.5 percent at 480 V
  line-to-line. Rejected alternatives contain incorrect Q values and imply
  scalar addition of P and Q. Provenance records the selection and sources.
- **222 Node and 76 Python tests passed**, including rendering every scene in
  every offered control state and both layouts. Course, expanded-reader,
  domain-map, research, staging and whitespace checks passed.

## Chapter 7 review and Chapter 8 figures — 2026-09-15

- Chapter 5 now has **21** scenes, Chapter 7 **34**, and Chapter 8 **35**.
  The user-confirmed Chapter 6 single-line title edit is included.
- **222 Node tests and 76 Python tests passed.** Course, expanded reader,
  domain-map and research checks passed. The usable-window example now yields
  0.76 MWh, 7.6 minutes at 6 MW, and 7.24 minutes at 6.3 MW. Existing recovery
  models establish the 5 kJ deficit and the 50/100 ms cases.
- Built-in browser QA at **1280 × 720** and **390 × 844**: inspected the
  derivation, stored-energy circuit, quotation, both closing exercises, both
  construction photographs, supplied rack chart and stack recap, and the moved
  DC feeder. Corrected mathematical subscript wrapping and the new capacitor
  circuit during visual review. Phone diagrams scroll vertically as needed.
- Exercised both bypass answers, the cooling-control answer reveal, the three
  contact states and the merged shared-bus option. Confirmed the old Chapter 7
  `dc-feeder-protection` URL redirects to the Chapter 8 scene while retaining
  presentation mode. New images load from local assets. No standalone browser
  was installed or launched.
- An independent source-code review found no material arithmetic, circuit,
  state-wiring or redirect defects. Original supplied TIFF pixels were preserved
  during PNG conversion; provenance records attribution and source limitations.
- Sparks' current IT/nameplate and qualified discharge MW remain unknown. The
  dated reported 1 MW pilot comparison is not a claim of current autonomy.

## Chapter 6 final review — 2026-09-14

- **21 scenes.** Added `power-factor-explained` immediately before the existing
  `power-factor` scene. Existing hashes retain their destinations; former slides
  17–20 become 18–21. Image-led scenes retain accessible headings without a
  duplicate visible title above the supplied image.
- Confirmed Compass data-center use in Siemens's original announcement.
  Corrected the supplied NXAirS image's breaker, cable and earthing callouts
  against Siemens HA 1702 p. 12; an independent visual/source review found the
  revised endpoints defensible. Original supplied images are preserved.
- Built-in image edits also update the floor PDU caption and the supplied PF
  image's two definitions. Inspected output labels and unchanged comparison
  numbers; independently checked 1,083 A, 1,353 A and 112.5% rounded to 113%.
  Exact prompts, final asset paths, hashes and source scope are recorded in
  `assets/generated/distribution-final-review.provenance.json`.
- **222 Node and 76 Python tests passed.** Course, expanded reader, domain-map,
  research metadata, site staging and whitespace checks passed. Verified slide
  17 placement, all 21 scene IDs and every referenced image asset. The distribution render test
  exercises every scene, every offered control state and both layout variants.
- Fresh browser interaction/whole-page layout QA could not be performed. A
  browser inventory call succeeded, but no callable control surface was available
  afterward; the independent agent also found no CUA control tool. No standalone
  browser was installed or launched. This remains a verification follow-up,
  separate from Kian's conditional acceptance of the completed content edits.

## Chapter 6 Abilene voltages and instrument transformers — 2026-09-14

- Kept all 20 scenes and existing hashes. Updated the campus voltage reference
  to 345 kV / 34.5 kV, the corresponding 2 MW current to 33.5 A, and the reader.
  Rechecked Mortenson's expansion account and the Longhorn drawing's 34.5 kV
  feed label; retained their different evidence scopes. Historical 138 kV and
  unrelated 13.8 kV examples remain intact.
- Slide 5 explicitly labels the CT and adds an HV CT/CVT measurement view.
  Scaled current/voltage signals and the relay's trip command have distinct
  paths. Slide 6 uses “Air gap.” Sources cover instrument-transformer roles
  without asserting an installed Abilene model.
- Used the built-in image-generation tool to edit the transformer-location
  illustration's voltage/current labels. Visually inspected the result; exact
  prompt, revised hash and calculation are recorded in
  `assets/generated/distribution-figures.provenance.json`.
- Inspected desktop and 390-pixel-wide SVG renders of the campus path,
  CT/relay/breaker states, HV CT/CVT view and disconnector view. Corrected label
  overlap in the open-breaker and phone CVT diagrams. These are diagram renders,
  not browser screenshots or whole-page layout checks.
- **222 Node and 76 Python tests passed.** Course, expanded reader, domain-map,
  research metadata, site staging and whitespace checks passed. An independent
  review found no actionable diagram or instrument-transformer issues.
  Fresh interaction/layout QA of the new
  slide 5 view remains pending: the built-in browser-control tool was unavailable
  this turn. No standalone browser was installed or launched.

## Chapter 5 drainage, flood response and simpler check — 2026-09-14

- Removed the requested bottom subtitle from slide 5. Slide 19 now isolates
  the road/fiber conflict, removes the surface-rights condition and shaded site
  panels, and reveals replacement routes with a three-step construction order.
  The same 19 scene IDs and chapter continuation remain.
- Rechecked Equinix's November 2017 employee account: the Houston team really
  pumped water out while keeping power on. Its separate August 28 operating/
  access statement remains distinct. Clarified stormwater versus cooling-loop
  water in slide 4's notes without changing its approved visual.
- Built-in browser checked slides 4, 5, 10 and both states of 19 at **1280×720
  and 390×844**. No horizontal page overflow, out-of-bounds SVG text or text
  collisions. Both desktop and phone problem/reveal layouts received screenshot
  inspection. Corrected a replacement-fiber connection gap and moved the phone
  excavation labels clear of the existing routes.
- **222 Node and 76 Python tests passed.** Course, reader, domain-map, source
  metadata, staging and whitespace checks passed. No standalone browser ran.
  Latest requested edits are implemented; whole-chapter acceptance is pending.

## Chapter 4 final review and Chapter 3 opener — 2026-09-14

- Restored Chapter 3's original three-part opening text alongside the supplied
  image; the deck remains 17 slides. Chapter 4 remains 25 slides, with Abilene's
  delivery example immediately after CoreWeave, revised WHEN/WHAT wording,
  larger configuration diagrams, requested caption removals, GW units and
  generation/procurement headings. Chapter 4 is accepted per Kian's review.
- **222 Node and 76 Python tests passed.** Course, expanded reader, domain map,
  source metadata, staging and whitespace checks passed. Updated the legacy
  browser harness's stale slide count; did not launch its standalone browser.
- Built-in browser checked 15 changed/adjacent Siting scenes at **1280×720 and
  390×844**, plus the restored Workloads opener. No horizontal page overflow,
  out-of-bounds SVG text or text collisions. Verified reordered selector entries
  and header hiding on slides 7–10 followed by header restoration. Opening,
  configuration and procurement layouts received screenshot inspection.
- Independent source/diff review matched every item to its rendered scene.
  The fuel-efficiency question was withdrawn and its model remains unchanged.
  The xAI heading refers to the Colossus buildout; the existing Southaven source
  attribution remains visible. No new evidence about Colossus 1 is claimed.

## Chapter 3 final review and upcoming-slide window — 2026-09-14

- Chapter 3 now has **17 slides** and is accepted after Kian's requested edits.
  The old knowledge-check hash resolves to the retained closing slide. Added the
  supplied DeepSeek KV chart and the generated bus; simplified the specified
  labels, headings and subtitles. Prefix caching and conditional prefill/decode
  bottlenecks are explained in the reader. The Chapter 8 downward-step buffering
  gap is recorded in COURSE_REVIEW.md.
- **222 Node and 76 Python tests passed.** Course, expanded reader, domain map,
  research metadata, staging and whitespace checks passed. The seven presenter
  tests exercise initialization, message identity, live selectors, navigation,
  reconnect and the upcoming/end display through the actual modules.
- Built-in browser checked the eight changed/adjacent workload scenes at
  **1280×720 and 390×844**: no horizontal page overflow, out-of-bounds SVG text or
  text collisions. DeepSeek chart and bus layout received screenshot inspection
  at both widths. Closing navigation retains 17 selectable scenes.
- Presenter now contains **one full-area upcoming slide**, with no current-slide
  mirror. The unpublished local iframe fixture verified main slide 9 alongside
  upcoming slide 10, next/previous, selector navigation, the last-slide state,
  transition into Siting and disconnect/reconnect. The second-window layout was
  visually inspected. Native popup placement/recording capture remains outside
  what the built-in browser exposed for automation. One unlocated MutationObserver
  error appeared during fixture navigation/teardown, as in the preceding pass;
  no clean browser-console claim is made.

## Chapters 1–3 review and presenter window — 2026-09-14

- Primer has **22 slides**. Removed the entire two-terminal voltage subtitle, moved tap selection into Chapter 6, retained a simpler input-range example after converter introduction, and applied the phase/PSU, AC title, UPS and network wording requests. Chapter 2 clarifies Gemini 1.0 Ultra and OCS fault rerouting. Chapter 3 uses the supplied, uncropped Jensen Huang image and the requested metric/interactivity label edits through slide 6. Chapter 6 now has **20 slides**.
- **221 Node tests and 76 Python tests passed.** Course, expanded reader, domain map, source metadata, staging and whitespace checks passed. Presenter tests cover preview indices, message identity, live selectors, SVG link activation and scroll positions.
- Built-in browser checked all 22 primer scenes, Chapter 3 slides 1–6, the Chapter 2 TPU view and all three relocated tap states at **1280×720 and 390×844** during this review pass. No horizontal document overflow, SVG text collision, out-of-bounds text or failed loaded image was found. Updated content received screenshot inspection; the final subtitle removal was checked again on the rendered slide.
- The Presenter button opens a separate window; the original audience page contains no preview. The popup established its connection, but the built-in browser did not expose that native popup as an automatable tab. A local, unpublished iframe fixture supplied the opener relationship and exercised the production presenter modules: current/next rendering, navigation in both directions, interactive choices, answer reveal, end-of-chapter state, Workloads → Siting reconnection, disconnect/reconnect, and the Primer and Continuity selectors. Presenter layout received screenshot inspection in that fixture. Native popup window placement and recording capture were not independently tested.
- Two unlocated MutationObserver errors appeared during fixture navigation and teardown; the browser returned no source location, so their origin is unconfirmed. These are recorded rather than treated as a clean browser-console pass. The separate presenter follows the audience viewport and its current state; the next-slide preview starts at that slide's default state.

## Chapter 11 storage, orchestration and recovery — 2026-09-14

- **25 scenes**, registered in the chapter directory and shared sequence. Chapter 10 leads to 11, then to the existing selected Chapter 12 cooling material. Three D09 reader lessons and the Google scheduling case handoff are updated. Chapters 1–10 slide content is unchanged.
- Cases use original Meta RSC and Google facility photographs, Meta’s Llama 3 paper, Google’s 2011 Gmail backup incident and its 2023 demand-response account. Publisher images were inspected and their saved bytes verified against provenance hashes. RSC phase-two targets are not presented as measured results; Llama 3 uses the internally consistent prose totals rather than its conflicting category table.
- **215 Node and 76 Python tests passed.** Course, expanded reader, domain map, research metadata, site staging and whitespace checks passed. Fourteen new model/deck tests cover checkpoint coherence, transfer constraints, asynchronous save queues, recovery placement, lost work, energy and scheduling deadlines. An independent review found no remaining substantive model or D09 coverage issue.
- Built-in browser checked all 25 scenes at **1280×720 and 390×844**, plus **64 control combinations and all eight answer/reveal combinations** across those sizes. No final horizontal overflow, SVG text collisions, out-of-bounds labels or failed loaded images; no desktop stage scrolling. Every desktop scene received screenshot inspection, with additional phone chart and exercise checks. The timeline labels and narrow chart typography were corrected during this pass.
- Clicked Chapter 10 → 11 → 12, Reading and Back to course. Fullscreen controls switched to “Exit full screen” and back; the browser’s read-only DOM proxy did not independently establish native fullscreen state. No console warnings/errors were returned. Checks used light appearance and the built-in browser only.

This records technical and visual verification. First author review remains pending.

## Chapter 6 follow-up — 2026-09-14

- **19 scenes**, including separate system-context isolation/surge views and a new busway introduction. Abilene's retired photograph hash redirects to the high-voltage campus path.
- Replaced the anatomy sketch with Siemens's original NXAirS sectional illustration. Generated a new overhead busway image and edited the PDU image with GPT image generation; both outputs visually inspected.
- **192 Node and 76 Python tests passed.** Course, expanded reader, domain map, research metadata and whitespace checks passed. Regression checks cover the high-voltage trace and two-hall breaker-failure outcome.
- Built-in browser checked every scene at **1280×720 and 390×844**: no horizontal document overflow, SVG text-to-text collision or failed loaded image; no desktop stage scrolling. Operated all 16 control choices with correct selected state and values. Circuit, conductor, manufacturer, isolation, phase-allocation and breaker-failure views received screenshot inspection. Light appearance checked.
- Phone diagrams reflow for the new circuit views. Large generated figures retain their existing contained horizontal-scroll presentation. Full-page browser captures proved unreliable for tall pages; viewport screenshots and live DOM geometry were used for the mobile conclusions.

## Chapters 4–5 review and shared navigation — 2026-09-14

- Chapter 4 has 25 scenes: the Southaven permit slide now includes a wider historical USGS aerial with coordinate-registered Census state boundary. The old schematic border hash resolves to this slide. MZX is identified as applicant and Trinity as consultant.
- Chapter 5 has 19 scenes: original SemiAnalysis BTM state chart beside Odessa, one QTS campus/topology comparison, simplified cooling and hot-swap labels, and a new live-campus expansion check. Getty remains reader background; the egress slide is removed. Retired hashes resolve to retained scenes.
- **192 Node and 76 Python tests passed.** Course, expanded reader, domain map, research metadata, staging and whitespace checks passed. Ruff was unavailable in the current environment; no lint pass is claimed.
- Built-in Codex browser verified all ten registered presentations’ final-slide links in curriculum order, including reader fallback after Chapter 9 and the combined 12–13 sequence. Chapter 5 → 6 was clicked; returning to the penultimate slide restores the ordinary next arrow.
- All 19 Chapter 5 scenes checked at 1280×720 and 390×844: no horizontal document/footer overflow or failed loaded image. Texas, QTS, cooling, Southaven and the new exercise received visual inspection. Both exercise states were operated. The geographic comparison was inspected at desktop and phone widths. Checks used light appearance; no separate browser binary was launched.
- Scope notes: QTS’s three-entry DC1 statement is available in indexed official PDF text; direct PDF requests returned 404. The actual campus plan remains embedded and the route diagram is a topology sketch. The SemiAnalysis chart ranks booked generating capacity, not data-center counts.

## Chapter 4 sites, capacity and generation — 2026-09-13

- Chapter 4 now has **26 scenes**. Added two genuine Polaris Forge 1 aerials
  from Applied Digital’s October 2025 presentation, retaining the original asset
  and showing photo areas through SVG viewports. Both photos are labeled as from
  that presentation; October 27 and November 24 remain separate service milestones.
- Corrected gas supplier/customer wording, Campus A/B label positions and Abilene
  capacity scope. 900 MW is a conditional calculation on the 1,200 MW plan;
  Oracle’s reported 75% does not establish current operating MW.
- Dania Beach explicitly teaches combined cycle and the 7HA.03 designation.
  Added the Tennessee/Mississippi siting relationship and attributed the
  historical permitting account; the reader records the subsequent removal plan.
- **72 Python and 142 Node tests passed.** Course, expanded reader, domain map,
  research metadata and staged-site checks passed. The existing browser harness
  was updated and syntax-checked without launching a standalone browser.
- Built-in Codex browser checked all six changed scenes at **1280×720,
  390×844 and 844×390**. A date/megawatt overlap was corrected and all eighteen
  resulting layouts passed text-collision, diagram-bound and horizontal-overflow
  checks. Representative desktop and phone screenshots were inspected. No console
  warnings or errors were observed. This pass used light appearance.

## Interactivity, transformer taps and instruction audit — 2026-09-13

The earlier 4,000-token/s exercise below passed arithmetic checks but missed the
requested teaching concept. That completion claim is withdrawn.

- Chapter 3 has **18 scenes**. Slide 3 teaches tokens/s/user and 50, 25 and
  12.5 ms token intervals. Slide 4 uses the original NVIDIA GB300/Qwen3.8 curve;
  threshold controls leave its per-GPU axis and printed benchmark conditions intact.
  The new service check-in asks what to change and remeasure when interactivity
  falls below the requirement. No exact supported-session count is inferred.
- Primer has **22 scenes**. The new transformer comparison shows 480 → 120 V,
  504 → 126 V at the same tap, and 504 → 120 V at the matched tap. P134 records
  Hammond Power Solutions' turns-ratio example; this is not automatic regulation.
- **72 Python and 142 Node tests passed.** Course, expanded reader, domain map,
  research metadata and site staging checks passed. Updated browser harnesses
  were syntax-checked without launching their standalone browser dependencies.
- Built-in Codex browser: all 18 workload scenes checked at **1280×720,
  390×844 and 844×390**, with no SVG text collisions, labels outside the diagram,
  or horizontal page overflow. All interactivity/threshold controls and both
  check-in states passed at those sizes. All three transformer states passed
  the same checks and displayed the expected input, tap, turns and output values.
- Representative desktop and phone visuals were inspected, including the original
  benchmark image. The chapter directory shows distinct rack-power deck names.
  No console warnings/errors were observed. Checks used light appearance.
- The feedback audit records incomplete teaching coverage and resolved dictation
  questions. An active check-in is now the default in every domain; a closing
  example requires a specific reason why no worthwhile active check can be made.

These checks do not establish spoken runtime, beginner comprehension or author
acceptance. Existing decks' complete check-in coverage remains a production task.

## Previous Chapter 3 revision — 2026-09-13

- Chapter 3 now has **16 slides**. The 4,000-output-token/s budget derives active
  sessions from streaming speed or streaming speed from active sessions, including
  milliseconds per token. All six control states agree with the arithmetic.
- Meta's model geometry and the ZeRO Adam ledger confirm the retained memory
  numbers. P129–P131 support the new Rubin-prefill → KV-cache handoff → Groq-LPX
  decode slide; the unchanged NVIDIA product render is stored with provenance.
- Runs now use 100 kW for 10 minutes versus 80 kW for 15 minutes. Staggering is
  fixed at 15-second intervals; the three retired ending scenes retain aliases.
- **72 Python tests and 142 Node tests passed.** Reader, domain-map and research
  generated files are current. The standalone workload browser harness was
  updated and syntax-checked; it was not launched.
- All 16 slides checked in the built-in Codex browser at **1280×720, 390×844 and
  844×390**. A desktop label overlap was corrected; all six service-control states
  then passed geometry checks. New LPX image, prefill comparison, energy table and
  fixed-offset trace were visually inspected. No console warnings/errors appeared.
- Repeated generic caveat footers were removed from the overview, primer, siting,
  generation, rack-power and cooling visuals. Their calculation inputs, source
  credits and named-project status remain. The teaching standard now records this
  rule for subsequent authoring. This pass used light appearance.

## Tiers, availability examples and directory — 2026-09-12

The four reliability scenes remain in the 22-slide selected UPS deck. Their
stable fragments are `tier-topology`, `tier-generation`, `availability-budget`
and `tier-investment`; the last two now show named examples and Fairwater Atlanta.

- **72 Python and 139 Node tests passed.** Checks cover the annual downtime math,
  claim boundaries, simultaneous comparisons and retained directory destinations.
- All four changed slides inspected in the native Codex browser at **1280×720,
  390×844 and 844×390**. No horizontal overflow; the actual Microsoft photograph
  loaded. Narrow screens scroll to the remaining content with the shared footer
  available. Desktop screenshots checked titles, diagrams, claim labels and sources.
- The device was in dark mode during this pass. A fullscreen attempt did not
  establish active DOM fullscreen; no new fullscreen or light-mode certification
  is claimed. Temporary viewport overrides were reset. No browser console errors
  were reported in the inspected sequence.
- The reader directory has chapter names and working destinations without interim
  status badges. Reliability Reading links now open the corresponding D05 reference.
- P120 and P121 record the Microsoft design claim and NTT DATA power SLA; P75
  distinguishes Crusoe Cloud from microgrid availability and their reporting windows.
  Reader, research and domain-map generated files are current. The standalone UPS
  browser harness was updated and syntax-checked, not run on this Mac.

This is a technical and visual pass; it does not close Kian's author review.

## Chapter 4 generation and Chapter 7 UPS — 2026-09-12

Current revision: Chapter 4 has 25 slides; the selected UPS sequence has 22.
One shared navigation component now adapts every presentation's original handlers.

- **72 Python tests and 136 Node tests passed.** New checks cover DC-link recharge energy and voltage, generator load-plus-charge state, conditional delivery economics, and the shared navigation contract. Existing three-phase transport and generation-cost conservation checks pass.
- Chapter 4's changed slides 15–25 checked in the native Codex browser at **1280×720, 390×844 and 844×390**. No final horizontal overflow, clipped SVG labels or measured text collisions. Fixed the portrait generated-image crop and labels crossing the procurement diagram's conductors.
- Visually inspected the actual Dania photograph, new GPT-generated delivery/startup/ramping figure, simultaneous cost curves, original Southaven application site/process figures, contract-fee comparison and delivery-premium calculation. The original source figures retain their credits and page links. Generated plant geometry is conceptual; the quantitative cost/current plots are computed in code.
- Independent UPS native pass checked revised slides 3–8 at the same three sizes, plus the 2N caption. Repeated all four generator states and both recovery-source selections; selection and diagram state agree. Fixed capacitor axes/metric overlaps and recovery diagram placement. No browser console errors in the checked UPS sequence.
- Shared navigation independently checked on workload, 800 V and UPS decks, including first/last disabled states, selector changes and UPS selector replacement after rendering. Sticky footer and 44px controls checked on narrow screens.
- Reader and source metadata synchronized; archived article content remains excluded from public staging. Chapter 4 has no reveal quiz; retired fragments resolve to the corresponding new scene. The standalone browser harness was updated and syntax-checked, **not executed**.
- Visual checks used the device's light appearance. No new dark-mode or native fullscreen certification is claimed for this pass. Viewport overrides were reset afterward.

## Chapters 3–5 and root publication — 2026-09-12

The preceding revision added three built-in GPT ImageGen figures, rebuilds Chapter 4
as 23 slides, adds Chapter 5 as 22 slides, and replaces Chapter 3's final visual.
The course is named From Watts to Tokens. The reader publishes at the root and
slide decks at `/slides/`, with old query/hash links preserved.

- **72 Python tests and 125 Node tests passed.** New staging checks cover dynamic
  Reading links, root paths, preserved deep links, recursive image assets and
  exclusion of local article archives. Four new Chapter 5 model checks cover
  physical loads, fiber failure and shared controls.
- Native Codex browser: Chapter 4's 23 slides checked at 1280×720, 390×844 and
  844×390 (**69 layouts**); **39 control/reveal states**, with repeated selection,
  were checked across those sizes. No final measured SVG-label collisions,
  out-of-bounds text or document-width overflow in these checks.
- Independent Chapter 5 native pass checked all 22 slides at the same three sizes
  and seven control groups, including repeated selection/restoration. Corrected
  the narrow captions, borehole label and route geometry found in that pass.
- Inspected actual GPT configuration/handoff figures and GE/Siemens diagrams;
  inspected the actual Lenovo rack and tray and Oracle aerial in rendered slides.
  Oracle embeds require the page's `no-referrer` policy. Its photographs remain
  publisher-hosted; no image was rehosted to solve the browser problem.
- Chapter 3's final visual checked at desktop, phone portrait and landscape;
  phone crops isolate each object and keep the trace labels inside its monitor.
  Diagram overlays are schematic, not fabricated telemetry.
- Shared navigation checked across eight existing deck routes plus Chapter 5;
  Reading follows the selected lesson, Chapter 4 reaches Chapter 5, and legacy
  URLs retain teaching mode and the selected slide. The reader's filter toggle
  is removed. Styled chapter links remain keyboard-accessible anchors.
- Native visual checks used the device's light appearance. Fullscreen preserves
  that appearance. Dark-mode styles were retained; this pass does not claim a
  new visual check of every dark-mode state.

The three standalone browser harnesses were updated for current navigation and
syntax-checked; they were **not executed** or used to launch another browser.
Native measurements and selected screenshots are the actual browser evidence.
Passing checks does not claim final author acceptance or beginner comprehension.

### Source-date reconciliation

Abilene's active slide, D03 reading and standalone case ledger use Oracle's
September 2026 status. The aerial remains dated 15 July 2026. The August Energy
Transfer update and the May Crusoe impact report provide separate fuel-route and
bridge-to-backup evidence. No September satellite capture was established.

Keep actual historical dates: Applied Digital's October/November 2025 releases;
March 10 substation energization; Wolfspeed's March 5 device announcement; OCP's
March 30 v1.0 paper; and Sparks' March operating-period report. Targeted September
searches did not establish a replacement OCP revision or a new Sparks measurement
period. SA32's March analysis remains dated research, not a current tariff quote.
No blanket publication-date substitution or complete new source-corpus audit is
claimed.

## Navigation, generation, reliability and rack power — 2026-09-12

The review adds eight generation/dispatch scenes to Section 4 (26 total), four
Tier/availability scenes to the UPS sequence (21 total), and an eleven-scene
selected rack-power presentation. The overview gains clearer PSU terminology
and a selectable NVIDIA GB300 rear figure showing its local DC busbar.

All build, expanded-artifact, domain-map and research freshness checks passed,
as did **67 Python tests and 117 Node tests**. The new tests independently check
availability allowances, equal-output fuel balances, every hourly dispatch
balance, the annual-cost crossover, local rail current/drop/loss, source-ramp
energy, BBU surviving capacity, recharge and finite multiphase ripple. A new
catalog-wide test requires an explicit Back to course header exit.

Built-in-browser checks covered:

- All existing deck header exits plus the student 800 V route; the new rack
  sequence also returned successfully to the reader's Slides available catalog.
- All eight generation scenes and controls: **60 scene/control states** across
  the actual 927 × 745 desktop viewport, 390 × 844 and 844 × 390. No measured SVG
  text collisions, out-of-bounds labels or page-width overflow. The hide/reveal
  control was checked in both states; its changed label required an adaptive
  test locator, not an application fix.
- All four reliability scenes at 1280 × 720, 390 × 844 and 844 × 390, including
  maintenance/fault, three availability targets and the customer-requirement
  toggle. An initial clipped card border was corrected and rechecked.
- All eleven rack-power scenes and controls at desktop and phone size
  (26 states each). The phone pass found overlapping BBU footnotes; after their
  correction, all three BBU states were rechecked at 390 × 844 and 844 × 390
  with no collisions or overflow.
- Visual inspection of the real GB300 rear figure and Dania Beach photograph,
  the gas shaft and separate steam/water loop, and the rack-to-die and Tier
  diagrams. Manufacturer images loaded from their credited publishers.

Temporary viewport overrides were reset. These checks used the current light
device setting; no new dark-mode browser sweep or standalone browser run is
claimed. New layouts inherit the existing device-theme variables. The source
notes distinguish full/subsection review from Uptime's indexed public passages
(direct requests returned 403). Numerical teaching scenarios are not product
ratings, commissioned behavior or a demonstration of learner comprehension.

## Overview photograph and Section 4 draft — 2026-09-12

Overview slide 2 opens on Google's credited New Albany server-aisle photograph.
The alternate floor plan preserves the white/gray-space explanation and all
thirteen overview scenes. The remote image loaded successfully; its content was
visually inspected in the built-in browser.

The new siting presentation has eighteen scenes and is registered under Section 4.
The final built-in-browser pass covered 150 scene/control/reveal states at
390 × 844, 1440 × 900 and 844 × 390, with no measured label collisions or labels
outside the displayed SVG. It included the three corrected spacing issues found
in the initial browser sweep. The final reader link opened the actual D03
prediction exercise and its Section 5 transition. Temporary viewport overrides
were reset. Native final checks used the device's light setting; preliminary
standalone checks covered both themes before the browser preference above was
noticed. No further standalone browser launches were used afterward.

All generated-artifact and research checks passed, as did 66 Python tests and
105 Node tests. The new model tests independently check readiness, signed power
balance, storage energy/power limits, fuel-limited duration and three-phase power
conservation. `tests/browser_siting.cjs` is retained for a separately configured
browser test environment; its full final revision was not rerun on this Mac.

Abilene claims retain Crusoe's 27 March 2026 reporting date. The Southaven/MiniHard
case retains SemiAnalysis's 7 August 2026 attribution; the 200 MW / 34.5 kV / 161 kV
calculations are hypothetical. These checks establish neither learner pacing
nor a real site's commissioned behavior. Section 4 remains an authored draft.

## Automated checks

```sh
uv run gigawatt-build
uv run gigawatt-build --check
uv run python -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/math.test.mjs
git diff --check
```

The builder checks chapter/lesson relationships, source URL shape, renderer IDs,
check answer bounds, local module assembly, and exact generated bytes. The math
tests check the numerical models. These checks do not verify a source's contents
or establish visual quality.

## Browser walkthrough

Serve `diagram/` locally and use the generated `index.html`. Inspect every lesson
at a desktop size, then sample each distinct layout at tablet, narrow portrait,
and short landscape sizes. Include 200% browser zoom.

- Read the title, diagram labels, units, assumptions, and takeaway without
  relying on notes to rescue the explanation.
- Use every interactive control at its endpoints and typical values. Predict
  the direction of the result and compare it to the displayed explanation.
- Navigate chapters and lessons, reload a deep link, and use the back/forward
  controls. Confirm the displayed content and active lesson stay consistent.
- Answer each knowledge check incorrectly and correctly; verify the feedback
  explains the result and does not only name the answer.
- Open and close notes and sources. Confirm links resolve to the intended
  primary evidence and changing lessons does not leave stale content visible.
- Traverse controls by keyboard. Check focus visibility, labels, slider values,
  dialog behavior if present, and the availability of textual explanations.
- Enable reduced motion and inspect narrow and short viewports for clipping,
  overlapping controls, unreadable labels, or horizontal page scrolling.
- Check the console and network panel for errors. Disconnect the network and
  confirm the course remains usable apart from external source links.

For a material diagram change, retain a few representative screenshots and
record which sizes and states were inspected. Recheck a changed numerical or
site-specific claim against its source before release.

## Publication

The Pages workflow validates the generated page and tests before staging the
single course page and small redirects for previously published course and
phase URLs. After deployment, inspect the published page, follow an old course
link, and verify that the content matches the intended commit. Do not reuse a
previous version's browser review as evidence for changed visuals.

## Rebuild verification — 2026-09-04

The rebuilt course was inspected in the browser across all 22 lessons at desktop
and 390 × 844 portrait sizes. No horizontal page overflow, text outside SVG
bounds, or browser console warnings/errors were observed. The capacity lab was
also checked at 1024 × 768 and 844 × 390. Seven quantitative diagrams have a
separate compact composition for phones; the other illustrations scale.

All 14 interactive views were exercised, including every slider's endpoints,
equipment selection, utility interruption, path loss, and feeder isolation.
The capacity lab produced the expected 600 → 700 → 400 rack-equivalent sequence.
All four checks were answered incorrectly and correctly; the feedback explained
the mechanism. Notes, source dialogs, Escape, arrow navigation, browser history,
reload/deep links, skip-link focus, and fullscreen presentation were exercised.

Seven Python build tests and six Node numerical tests passed, along with bundled
JavaScript syntax, deterministic artifact checking, Ruff, and whitespace checks.
This records the inspected scope, not a certification or a claim that learner
outcomes have been measured. A real teaching session remains the test of pacing
and comprehension.

## Expansion planning verification — 2026-09-06

The domain atlas and research pipeline are implemented planning tools. The
expanded lessons, final teaching visuals, learner trials and recording are
still pending; none of the new course review gates was closed by these checks.

- 28 Python tests and six numerical JavaScript tests passed. These include the
  domain graph and teaching-order checks, source mapping consistency, safe
  embedding, discovery failure handling, metadata deduplication, preservation
  of editorial decisions and exact human note bodies, and stale-output checks.
- The existing course, new HTML/Markdown map and research notes passed their
  offline freshness checks. A repeated research build changed zero files.
- Local Markdown links across the planning and research documents resolved,
  including exact filename case. Ruff and whitespace checks passed.
- The atlas overview and D06 detail were inspected in the in-app browser at
  desktop size and 390 × 844 portrait. The D06 view showed five objectives,
  three prerequisite highlights and eight source connections. No horizontal
  page overflow was measured at the sampled phone state. This is a sampled
  planning-interface review, not the full course browser walkthrough above.

The Pages workflow now checks the map and research outputs as well as the
existing course. The new atlas is available as a local preview and repository
artifact; this change does not add it to the public Pages site.

## Authored expansion verification — 2026-09-06

The expanded reader contains **50 authored lessons**, including five integrated
cases, with **65 mapped objectives**, roughly **51,000 words**, 137 glossary
terms, five GPT ImageGen illustrations and eight types of numerical model.
These are implementation counts. At this initial expansion check, external
engineering review, learner feedback, recording and export checks were pending.
Kian subsequently identified text crowding and an unclear recording workflow;
see the presentation revision below and [PRESENTING.md](PRESENTING.md).

- **34 Python tests and 14 JavaScript numerical tests passed.** Checks include
  complete objective mapping, worked-answer and source-boundary preservation,
  generated freshness, DC current/loss ratios, water heat transport, bits/bytes,
  roofline ceilings, separate backup power/energy constraints, checkpoint
  approximations and whole-rack capacity limits.
- **100 lesson viewport states passed** in headless Chromium through Playwright:
  all 50 lessons at 1440 × 1000 and 390 × 844. Every image loaded, every lesson
  had its explanatory sections and worked steps, every practice answer opened,
  and no horizontal page overflow or browser errors were observed.
- All eight model types were exercised at slider endpoints. Search match/empty
  states, glossary-to-lesson links, three electrical architecture selections,
  the sample page, mobile contents/Escape, reduced-motion context, and the
  sample at 1024 × 768 and 844 × 390 were checked.
- Desktop course, mobile sample and mobile model screenshots were visually
  inspected. Chart labels use responsive HTML text rather than small lettering
  inside a scaled SVG. The illustrations carry no authoritative measurements.
- Local document links resolved in both the repository and staged site. Root
  navigation and historical introductory lesson hashes were checked separately.
- Generated course, sample, map and research-note freshness passed, as did
  Ruff and whitespace checks. The current `qa/expansion/browser-report.json`
  records the browser scope; screenshots sit alongside it.

The checkpoint interaction refuses its first-order estimate above its declared
10% checkpoint-overhead teaching cutoff. It remains an approximation, not an
exact availability or restart model. The DC architecture choices select
representative bus voltages; hypothetical slider changes do not validate real
component compatibility.

To repeat the browser check, make Playwright and its Chromium browser available,
serve the repository root, then run `node tests/browser_reader.cjs`. An optional
first argument selects the course base URL and a second the screenshot/report
folder. The first run used the bundled Codex Node packages through `NODE_PATH`;
the test itself does not depend on a Codex browser session.

Publication now stages the expanded reader, sample, illustrations, compact
introduction, domain atlas, and reference documents. The site is explicitly an
authored draft. Prior introductory release checks remain historical evidence
for their stated version, not external sign-off on this expansion.

## Presentation revision after first feedback — 2026-09-06

Kian identified text crowding and an unclear recording workflow. The sample now
has a visual presentation, a separate synchronized notes window, and a preserved
reading page. This addresses the delivery-format issue; the revised teaching
sequence still awaits learner rehearsal and specialist review.

- **35 Python tests and 14 JavaScript numerical tests passed.** Generated
  presentation and reading surfaces are distinct, with separately authored notes
  and limited headline/caption text. Both use the existing tested DC model.
- **50 presentation layout states passed** in headless Chromium: all seven
  visuals, with before/after answer states where applicable, at 1920 × 1080,
  1280 × 720, 1024 × 768, 390 × 844, and 844 × 390. No horizontal overflow or
  clipped equipment labels was found. The desktop recording sizes need no page
  scrolling. Phone architecture diagrams stack vertically and may scroll.
- Current and loss answers remain hidden until revealed. The default current,
  slider endpoints, loss ratio and changed-load answer were checked. The fixed
  resistance assumption and conductor-loss denominator stay on screen.
- Separate-window navigation, answer visibility and voltage synchronization
  passed in both directions. Notes remain outside the visible audience surface.
  Keyboard advancement after reveal, slider keyboard input, fullscreen entry and
  exit, and the preserved reading page were exercised.
- The prior reader regression check also passed: 100 lesson viewport states,
  eight model types, search, glossary and practice. The old reading sample is
  now `sample-reading.html`; the existing `sample.html` link opens the visual
  presentation, including when its former `#sample-800v` hash is supplied.
- Desktop introduction, current, loss and architecture screenshots, the mobile
  architecture layout and the presenter console were visually inspected.
  Browser report and screenshots: `qa/presentation/`.

Repeat with `node tests/browser_presentation.cjs` while serving the repository
root and providing Playwright through `NODE_PATH` or a local installation. The
optional first argument is the course base URL; the second is the report folder.
The checks use a fresh browser context and do not inspect a personal profile.
They do not establish an actual recording duration, captured audio quality,
video-export legibility or learner comprehension.

## Dry-run and energy-balance revision — 2026-09-08

The default student visual sample is now `sample.html`; the explicit teaching
endpoint is `teach.html`. The notes window contains narration, cues and the
sequence without a recording-setup block. The production plan begins with an
unrecorded teaching dry run. This revision follows direct feedback about those
surfaces and the misleading feeder-demand drawing.

- **35 Python tests and 17 JavaScript numerical tests passed.** New checks close
  both electrical power and one-hour energy balances, include the sending-end
  voltage required by the stated receiving-end voltage, and verify a whole-path
  AC/DC advantage, reversal and break-even point. Invalid loss, resistance and
  duration inputs are rejected.
- **120 visual layout states passed:** eight steps plus four answer reveals,
  student and teaching modes, at 1920 × 1080, 1280 × 720, 1024 × 768,
  390 × 844 and 844 × 390. Forty additional student explanation expansions
  were checked. The initial phone footer overflow was fixed; no remaining
  horizontal overflow or clipped equipment labels was found.
- Student mode hides instructor controls and ignores P/F teaching shortcuts.
  Teaching fullscreen and the separate notes window work. Step changes,
  reveals, DC voltage and the final conversion-loss slider synchronize.
- The legacy `#feeder-transfer` link opens the final AC/DC loss comparison.
  The physically impossible request no longer appears as an operating flow.
  The written sample preserves the assumptions and the changed-case solution.
- Independent arithmetic review confirmed the 1 mΩ receiving-end DC comparison:
  104.340278 versus 100.015625 kW segment input for equal 100 kW delivered.
  The source voltage covers conductor drop. The separate whole-path budgets
  give AC 105 kW, DC 103.1 kW at default losses, and DC 106.1 kW when its
  conversion loss rises to 6 kW. All losses are explicitly hypothetical;
  no real-product efficiency advantage is inferred.
- The new desktop energy ledgers and phone student view were visually inspected.
  Report and screenshots are in `qa/presentation/`. The obsolete feeder
  screenshot was removed; Git history preserves the earlier version.

Rack-unit coverage was also added to `d06-rack-migration` using identified Eaton
and OCP sources, with access/revision limitations recorded. Its worked allocation
uses 32 of 42U; independent fit and service constraints remain explicit. The
course now indexes 140 glossary terms and 59 lesson source records.

These checks verify the artifact and calculations. They do not establish that
Kian has completed the revised dry run, that learners understand the explanation,
or that the course has received specialist engineering review.

## Corrected 480 V AC / 800 V DC comparison — 2026-09-08

Kian clarified that the sample's reference was 480 V three-phase AC. The earlier
48 V DC premise is superseded for this sample. The eight steps now distinguish
per-conductor current, conductor count, total conductor heat, and complete-path
input energy. The reading calculator uses the same AC/DC conductor model.

- 36 Python tests and 21 JavaScript numerical tests passed. The sample builder
  now includes catalog sources used only by the sample, with a regression check
  that every cited record is embedded in its reading page.
- 120 presentation layout states and 40 student explanation expansions passed
  across both audience modes and five viewports. Notes synchronization, keyboard
  controls, old-hash routing, converter-loss changes and the reader AC/DC controls
  passed. Desktop and phone current/ledger renders were visually inspected.
- At 100 kW feeder receiving power, 480 V AC line-to-line RMS at PF 1 requires
  120.281 A per line; 800 V DC requires 125 A per conductor. With 10 mΩ per
  conductor, total heat is 0.434028 versus 0.3125 kW. The 28% reduction applies
  to conductor heat, and gives 0.121528 kWh less input over one hour.
- The final model instead fixes a 100 kW useful DC load. Assumed downstream
  converter losses enter feeder demand before conductor heat is calculated.
  With AC conversion loss 4 kW downstream, AC input is 104.469444 kW. With DC
  conversion loss 1 kW upstream plus 2 kW downstream, DC input is 103.325125 kW.
  Raising total DC conversion loss to 6 kW produces 106.344531 kW input. The
  crossover at approximately 4.137 kW is bracketed by the 4.1/4.2 kW controls.
- An independent physics audit confirmed conservation and converter placement.
  Conversion losses remain explicit teaching assumptions. This is neither an
  equipment performance measurement nor a whole-facility efficiency estimate.
- Source catalog, domain map, generated pages, Python formatting/lint, JavaScript
  syntax and whitespace checks passed. Local site staging succeeded.

The earlier test records above describe earlier iterations. Current report and
screenshots are in `qa/presentation/`. Comprehension and spoken delivery still
require Kian's unrecorded rehearsal.

## Copper, space and course-wide teaching standard — 2026-09-09

The sample now has ten scenes. A copper comparison precedes current and heating;
the architecture sequence marks released rack space and relocated conversion;
a changed-load exercise follows the complete-path energy counterexample.

- 38 Python tests and 22 JavaScript numerical tests passed. The new numerical
  check confirms 200 kW at 800 V gives 250 A and 1.25 kW conductor heat at
  10 mΩ per conductor. The model does not establish equipment capacity.
- 160 browser layout states and 50 student explanation expansions passed.
  All five solid copper bars have equal rendered width and height, with three
  in the AC bundle and two in DC. The revealed material reduction is 33.3%
  under the visible geometry assumptions.
- The final question hides its calculated current/heat and capacity conclusion
  until reveal. Its answer synchronizes to the separate notes window. Existing
  current, loss, complete-path reversal, sliders, keyboard, fullscreen, student
  mode separation and legacy hash checks remain covered.
- Desktop and phone copper, capacity, sidecar and power-room diagrams were
  visually inspected. No overflow or clipped labels was found, including the
  ten-step mobile navigation. Report and captures remain in `qa/presentation/`.
- The builder now validates a learning contract, teaching roles, timing totals
  and aliases without a fixed sequence length. The course template now tracks
  adaptation work across all domains; it does not claim those presentations exist.

Rehearsal allocations were subsequently increased to allow explanation and
predictions; approximately fifteen minutes is a provisional allowance, not a
measured duration. Learner comprehension and spoken delivery remain unverified
until the revised dry run. The other 50 reading lessons and the persistent
functional BOM remain pending adaptation.


## Ownership consolidation and terminology — 2026-09-10

The filled-in course template now owns scope, companion commitments and production
status. The domain map owns objectives and sequence; its renamed
`baseline_coverage` / `baseline_lessons` fields explicitly refer to the retained
introduction. Four overlapping guidance files were retired after consolidation;
the site builder preserves their published paths as replacement links.

- All generated-output checks, 40 Python tests and 22 JavaScript numerical tests
  passed. Regression checks allow a domain's lessons to merge while retaining
  objective coverage, reject an uncovered objective, and validate capstone IDs
  against the map instead of a hardcoded lesson count.
- The reader passed 100 desktop/phone lesson states, search, glossary, practice
  and its eight numerical models. After the final terminology/practice edits,
  the three affected lessons passed six additional staged-site viewport states.
- The domain map passed nine selected-domain states at 1440, 768 and 390 pixels,
  including historical-coverage labels, BTM search, coverage filtering and no
  horizontal overflow or page errors. The phone layout was visually inspected.
- 1,196 local Markdown link targets resolved. All four retired published paths
  resolved to the consolidated guidance in the staged site. Ruff and whitespace
  checks passed; generated builds were current.

D01/D12 white/grey-space explanations and D03 behind-the-meter supply now include
original application questions and scoped primary citations. The D03 arithmetic
keeps the customer bus fixed: 8 MW load = 6 MW local + 2 MW grid; with a supported
island, 4 MWh of usable storage at a 2 MW deficit lasts two hours. These are
synthetic assumptions, not site capability evidence. External technical review,
learner rehearsal and full-course presentation adaptation remain pending.


## Local article archive — 2026-09-10

The source pipeline now has explicit archive sync, import and offline integrity
commands. Publisher permission context is recorded locally. Metadata discovery,
article capture, source review and curriculum changes remain distinct operations.

- 51 Python tests passed, including 11 archive tests for structured extraction,
  mathematical source text, preview detection, complete provided exports,
  caching, failed refreshes, manual-edit preservation, source identity and
  exclusion from the public site. Existing generated-course checks still pass.
- The refreshed discovery inventory has 336 URLs. The bounded archive contains
  97 selected SemiAnalysis captures: 41 curated sources and 56 discovery
  candidates, with 16 publisher-marked public articles and 81 public previews.
  Both capture passes completed without a request failure. This is not a claim
  of an exhaustive relevant corpus or completed reading.
- All 97 file hashes verified. A subsequent sync returned 97 cache hits without
  fetching article bodies again. The new BTM report, SA41, remains labeled a
  public preview; importing a complete authorized export is supported.
- The actual `research/articles/` folder is Git-ignored and absent from the
  staged Pages artifact. Public original research notes, the source catalog,
  domain mappings, code and workflow documentation remain publishable outputs.

The archive retains publisher figure links instead of downloading images.
Captured source prose does not become lesson prose or technical-review evidence.


## AC/DC foundations — 2026-09-10

The 800 V sample now has fourteen scenes, including a closed DC loop, single-phase
AC reversal, balanced three-phase current/power and line-to-line voltage. All keep
100 kW average received power explicit. The provisional rehearsal allocation is
now about 23 minutes. D05 had no presenter sequence at that checkpoint; see the
UPS prototype update below.

- 51 Python and 31 numerical JavaScript tests passed. Nine new waveform tests
  check RMS/cycle averages, polarity reversal, balanced power/current sums,
  voltage subtraction, alternate inputs and invalid values.
- The existing presentation browser check passed 200 layout/reveal states.
  `tests/browser_electrical.cjs` additionally checks 20 primer layouts, title/visual
  separation, the fixed energy reference, cycle controls, phase balance, keyboard
  access and synchronized presenter notes. Screenshots were visually inspected.
- New primary source notes P18/P19 support the introductory electrical identities.
  Ideal resistive examples explain the quantities; they are not rack-input
  waveforms, equipment ratings or measured architecture efficiencies.

## UPS, bypass and redundancy prototype — 2026-09-10

The local `course/prototypes/ups-format.html` now has fifteen scenes. The new
bypass and redundancy diagrams are code-rendered; the campus image remains an
orientation aid. Notes are optional through `?rehearse=1`.

- 52 Python tests passed, with research, domain-map and generated-course checks
  current. The SST chart is included in D06 with a forecast caption and source;
  its SHA-256 matches the supplied image. Reader checks passed 100 lesson/viewport
  states and confirmed the image loads.
- `node --test tests/ups-bypass.test.mjs tests/ups-redundancy.test.mjs` passed
  20 tests. These trace rendered bypass connections, check source loss and
  maintenance isolation, and independently check surviving module/path capacity.
- `node tests/browser_ups.cjs` (with Playwright available) passed 60 layouts
  across 1440×900, 1280×720, 390×844 and 844×390, plus source, fault, maintenance,
  bus and load-growth interactions. SVG exclusivity, keyboard navigation and
  optional note synchronization passed. Representative screenshots were inspected;
  short landscape layouts scroll instead of clipping the controls.

These checks establish the stated teaching-model behavior, not equipment-specific
transfer performance, a switching procedure or completed learner review of D05.

## Automatic device themes — 2026-09-10

The reader, sample/teaching/notes views, UPS prototype, domain map and introduction
follow `prefers-color-scheme` with CSS. Checked 48 light → dark → light states
across eight pages and desktop/mobile layouts: preference changes apply without
navigation, preserve the current scene and source images, and keep printing light.
The full reader check also passed 100 lesson/viewport states in dark mode.
UPS checks passed all 60 scene layouts in each theme; sample controls and note
synchronization still pass. Representative screenshots were visually inspected.
All 52 Python tests and generated-output checks pass. Changes remain local.


## Learner-review revision — 2026-09-11

Both teaching sequences now use one explanatory headline and omit competing
bottom subtitles. The UPS sequence embeds the named product photograph and
identifies the separate UPS battery. The 800 V sequence has thirteen scenes;
its converter-loss example uses an explicitly illustrative 98% efficiency,
and the final current calculation shows the 100 → 200 kW load change directly.

- 52 Python and 51 JavaScript tests passed, including waveform identities,
  conductor losses, bypass connectivity and surviving capacity. Generated
  course, research and domain-map checks passed; Ruff and whitespace checks passed.
- The updated presentation check passed 180 layout/reveal states across teaching
  and student modes at five viewport sizes, with no desktop presentation scroll,
  horizontal overflow or clipped labels. It checks the converter energy balance,
  current/heat arithmetic, old deep-link aliases, keyboard controls and note sync.
- The electrical-primer check passed 20 layouts plus current reversal, balanced
  total power, voltage measurement and synchronized controls. DC now uses a closed
  circuit and equation; the voltmeter connects to two explicitly live phases.
- UPS checks passed 60 layouts and 12 introductory light/dark views, product-image
  loading, bypass source changes, 14 redundancy cases and optional note sync.
- Desktop and mobile screenshots were visually inspected, including the meter,
  converter heat branch and final current comparison in light and dark modes.

These checks verify the implemented teaching models and presentation behavior.
They do not establish measured equipment efficiencies or learning outcomes.

## Generator handoff and architecture ending — 2026-09-11

The UPS sequence now has sixteen slides, with a three-state utility / battery
bridge / accepted-generator diagram before bypass. Navigation uses short labels;
the full teaching sentence appears only in the headline. The 800 V sequence now
has twelve slides and ends with conversion placement. The unrelated load-doubling
slide and matching written exercise are removed; its old hash opens upstream
conversion. A changed-case ending is no longer mandatory in the authoring schema.

- 52 Python and 51 JavaScript tests passed, along with all generated-output,
  research, map, lint and whitespace checks.
- Presentation checks passed 160 layout/reveal states and verified the revised
  ending, historical links, controls and note synchronization.
- UPS checks passed 64 slide layouts, 12 introductory theme views, short-label
  menu fit, the existing 14 redundancy cases and bypass controls. Twelve further
  generator states covered three sources/stages, two viewports and both themes:
  only the selected source contact closes; startup uses the battery/DC link;
  the generator feeds the rectifier; inverter output remains supplied.
- The new diagram was checked independently for path continuity and source
  isolation. Desktop/mobile screenshots were inspected; compact labels were
  moved inside component boxes to avoid intersecting the wires. The staged site
  includes the generator diagram module.

## AC foundations and adoption dates — 2026-09-11

The twelve-slide sample now motivates balanced three-phase AC with the power
pulses of an explicitly resistive single-phase teaching load. The voltage slide
adds a synchronized three-pair waveform view; the copper geometry is shown
without a reveal, conductor heat includes its equations, and the converter
example explicitly isolates one 480 V AC-to-800 V DC supply. Architecture dates
are attributed to the May 2026 SemiAnalysis forecast, with the baseline and
combined Phases 1–2 distinguished from Phase 3.

- All 52 Python and 51 JavaScript tests passed. Course, expansion, domain-map
  and research metadata checks passed, along with Ruff and whitespace checks.
- The presentation harness passed 150 layout/reveal states, including controls,
  student explanations, historical links and synchronized notes.
- The electrical harness passed 20 primer and five phase-pair layouts. Sampling
  a complete cycle independently recovered 480 V RMS for each pair and verified
  that signed instantaneous pair differences sum to zero. Current reversal,
  balanced power, keyboard controls and notes synchronization passed.
- An additional 24 desktop/mobile light/dark layouts passed overflow and overlap
  checks. Representative waveform, heat, converter and architecture screenshots
  were visually inspected.

These are ideal teaching models and dated adoption forecasts, not measured
converter performance, universal deployment dates or equipment-specific designs.

## DC-link buffering and step-down context — 2026-09-11

Slide 9 now identifies conventional MV-to-480-V AC step-down and isolation before
its AC/DC supply boundary. Reader text distinguishes the 415 V AC input in
SemiAnalysis Phase 3 and rejects a universal 10 kV rectification ceiling. Normal
and battery UPS views identify DC-link capacitor buffering; D05 includes the
hypothetical 0.20 F, 800→700 V, 1 MW capacitor-only hold-up calculation.

All 52 Python and 51 JavaScript tests passed, with generated-output, catalog,
map, lint and whitespace checks. Presentation checks passed 150 states and now
check that the converter equation clears the navigation. UPS checks passed 64
layouts, 12 introductory theme views, bypass/redundancy interactions and notes
synchronization. Eight targeted converter/storage views passed in light and dark
at desktop/mobile sizes. Representative converter and UPS screenshots were
inspected. Independent arithmetic gives 15 kJ usable, 15 ms hold-up and 49 kJ
remaining below the selected voltage threshold; these are not UPS specifications.

## Capacitor support, conversion placement and parcel selection — 2026-09-11

The UPS prototype now directly compares capacitor-only endurance with an assumed
battery-power ramp. Four numerical tests check the 15 ms cutoff, simultaneous
contributions, 5 kJ deficit, 768.1 V result and energy conservation. These are
hypothetical inputs, not measured UPS timing. The 800 V sample opens slide 9 with
conventional step-down and controlled rectification; conversion heat is optional.
D12 replaces generic downtime arithmetic with an interactive two-parcel screen.

Validation passed: 52 Python tests, 55 JavaScript tests, generated-artifact and
research checks, Ruff and whitespace checks. Browser coverage includes 150 sample
layout states plus its new step-down view, 68 UPS layouts, 16 theme views,
scenario controls and existing notes/keyboard behavior. The parcel comparison
was checked in light/dark at 1440 and 390 pixels, including keyboard selection,
area/date arithmetic and navigation back to ordinary lessons. Representative
screenshots were inspected. The parcel lesson is a reader draft, not a completed
presenter sequence or an assessed real site.

## Generalizing the reviewed sequences — 2026-09-11

Slide 9 now has one supply-path headline and three component blocks. Its optional
loss view explicitly names the electronic AC/DC converter; the upstream transformer
is outside that calculation. The teaching standard and playbook carry the reviewed
approach into new sections. The first adaptation is eight cooling scenes spanning
selected D10/D11 concepts, with separate fluid loops and visible heat transfers.

Validation passed: 52 Python tests, 59 JavaScript numerical tests, generated-file
and research checks, Ruff and whitespace checks. The 800 V browser harness passed
150 states. Cooling passed 64 layouts (four viewport sizes in light/dark), flow
selection, facility-flow stop/restore, heat tracing, keyboard navigation, source
dialog and student/teaching-mode separation. Representative desktop and phone
screenshots were visually inspected. The calculation diagram is an open selected
cold-plate path, not a closed loop with an omitted heat sink. Small-screen navigation
follows the content so it cannot cover the diagram. The reader and optional model
notes retain source limits; the new sequence remains a draft for a dry run.

## Cooling diagram repair and terminology coverage — 2026-09-11

The rack heat label is now centered inside a source block that fits within one
server tray. Heat arrows begin outside that label and at the outdoor coil rather
than beside the fan. Duplicate cold-plate labeling and an unexplained layer were
removed; the reduced-flow comparison explicitly labels temperature rise.

Cooling browser checks pass 64 layouts in two themes and four viewport sizes,
including object/label containment and heat-arrow origins. Flow-restored and
trace-revealed states are also checked and captured. Desktop and phone views were
visually inspected. Twelve targeted D10/D11 reader layouts passed terminology,
worked-temperature and overflow checks. All 52 Python and 59 JavaScript tests,
generated-artifact checks, source checks, Ruff and whitespace checks passed.

D10 distinguishes rack capture and room-air equipment; D11 now directly teaches
dry/wet/hybrid rejection, air-/water-cooled chillers, dry bulb, wet bulb and named
approach temperatures. The synthetic 84 kW comparison has independently checked
45°C, 35°C and 41°C technology-supply outcomes, including the chosen separating
exchanger. These expanded reader lessons are not completed presenter sequences.

## Cooling presenter expansion and CoolIT example — 2026-09-11

The presenter now contains eleven scenes with selectable capture, plant and
weather states. It directly teaches CRAH and CDU roles, air/liquid capture,
sensible-heat balance, loop rise versus approach, real CHx2000 hardware, dry/wet
rejection, dry/wet bulb, hybrid/chiller/economizer modes and loss of facility flow.
The former water-warms and flow-doubling scenes are consolidated into the
substantive air/water volume-flow comparison; their historical links still work.

- 168 browser scene/state layouts passed across four viewports and both themes,
  with object-label containment, SVG bounds, keyboard controls, restored-flow
  states, photo loading and student/teaching separation. Representative desktop
  and phone diagrams were inspected. Mode-specific headlines replace generic
  statements; repeated bottom summaries were trimmed.
- All 52 Python and 60 JavaScript tests passed, alongside generated-course,
  source/map, Ruff, staging and whitespace checks. The added transport test
  independently closes 100 kW at a 10 K rise for 8,291.87 L/s modeled air and
  2.39234 L/s water. Separate 84 kW CDU and outdoor examples retain their inputs.
- CoolIT product photographs and current primary specifications were checked.
  2 MW at 5 K approach and 2,125 L/min at 35 psi remain separately listed points;
  no combined efficiency or universal rack compatibility is inferred. Photographs
  load from the manufacturer, with attribution and a cabinet/internal toggle.

The presentation is implemented for a new dry run. Full-domain completeness,
spoken delivery and learner comprehension are not established by these checks.

## Opening teaching section — 2026-09-11

`course/prototypes/orientation-format.html` directly teaches eight selected D01
scenes: three facility paths, white/grey space, rack and facility boundaries,
heat accounting, equal energy/different peaks, averaging and useful-work metrics.
`orientation-model.js` supplies the shared ledger, profile and efficiency models;
eight numerical tests check conservation, double counting, intervals and invalid
inputs. The examples are original assumptions, not measured site or product data.

`node tests/browser_orientation.cjs` passed 128 scene/state layouts at 1440, 1280,
844 and 390 pixels in light/dark mode. It checks label containment, text overlap,
desktop fit, selected controls, restoration, numerical results, mouse, touch,
keyboard, the source dialog and the teaching-only full-screen button. Screenshots
were inspected, including narrow heat paths and both demand profiles. Fifty-two
Python tests and 74 JavaScript tests passed; generated reader, map and research
checks are current. The sequence is ready for a dry run; broader D01 evidence
evaluation stays in the reference and D02 presentation remains to be authored.

## Opening revision — 2026-09-12

The opening now has six scenes. White/gray space remains on slide 2; the CDU
relocation exercise, heat-accounting scene and separate averaging scene were
removed. The GB300 example uses NVIDIA's published full-rack requirement and
product image; its hypothetical operating ledger is labeled separately. The
remaining comparisons distinguish supply nameplate from demand, stagger a
deadline-bound LLM evaluation queue and reduce facility overhead at fixed IT
energy and workload.

All 88 orientation scene/state layouts passed at four viewport sizes in both
themes, including image decoding, label containment, control selection,
restoration, input methods and old-link redirects. Eight actual-fullscreen cases
passed across orientation, UPS, cooling and 800 V DC, including device-theme
changes while full screen. Representative desktop and phone views were inspected.
All 52 Python and 75 JavaScript tests passed. Generated reader, map and research
checks are current. D08's written lesson now explains the campus-to-carrier
handoff; its teaching presentation remains unbuilt.

## Broader opening tour — 2026-09-12

The opening now contains thirteen slides. Seven new diagrams preview generation,
transmission, campus power, backup, chip-to-cluster scale, network roles and the
liquid heat path. Each links to its existing deeper lesson. White/gray space
remains on slide 2. The liquid-path preview keeps its coolant circuits separate;
its optional explanation identifies the remaining room-air cooling requirement.

All 144 scene/state layouts passed at four viewport sizes in both themes, with
label containment, overlap, navigation, legacy links and existing numerical
comparisons checked. Desktop and phone diagrams were visually inspected,
including coolant connections, network close-up lines and first-use terms.
Eight full-screen checks across the four teaching sets passed. All 52 Python
and 75 JavaScript tests passed; generated artifacts, source metadata, the thirteen
lesson links and site staging checks passed. No additional recorded runtime or
whole-domain completion is claimed.

## D00 primer and D02 workload presentation — 2026-09-12

D00 adds 18 optional first-exposure scenes with a planned 1,200-second pacing
outline. D02 adds 19 scenes across the three workload lessons. D01 remains
unchanged. Runtime and learner comprehension require an aloud dry run.

- All 52 Python and 94 JavaScript tests passed, including 19 new workload tests
  for memory partitions, complete energy/output accounts, FIFO batching,
  independent job phases and acceptance boundaries.
- Before the desktop browser preference below, D00 passed both themes, four
  viewports, its interactive states, keyboard/dialog behavior and D01 handoff.
  D02 passed 320 scene/state layout checks, numerical comparisons, control
  restoration, keyboard/touch navigation, reveals, dialogs and fullscreen.
- Generated course, domain map and research metadata freshness checks passed.
  Screenshots were inspected for desktop/mobile legibility and diagram meaning.
  Final D02 navigation and arrow changes passed static checks; their last
  interactive inspection remains pending in the built-in browser.

## Domain checks and cases — 2026-09-12

D00 now has 16 substantive scenes and 1,110 seconds of provisional cues; this
supersedes the earlier 18-scene/1,200-second version. Opening and closing roadmap
slides were removed. Historical hashes still resolve to circuit and PUE.

The reader includes 15 domain-end scenarios and answer reveals. Case treatments
cover original Colossus reuse, the attributed SemiAnalysis equipment lead-time
workaround, Crusoe/Redwood solar and batteries, Abilene cooling, and Google's
flexible demand. The original Abilene campus is the recurring reference; the
adjacent Microsoft project stays distinct. D02 hands off to the first D03 lesson.

57 Python tests and 94 existing JavaScript model tests passed, as did exact
freshness checks for the reader, domain map, source library and historical course.
The case models and new visual walkthrough are checked separately below.

Case-study checks passed for the 200 MW three-phase current values (3.347 kA at
34.5 kV; 0.717 kA at 161 kV), ideal battery durations (21 and 10.5 hours), invalid
denominators, nine unique scene IDs, source keys and reader destinations. All
three new presentation shells pass JavaScript syntax checks. A first overly
precise hand-rounded expected-current value in the ad hoc check was corrected;
the implementation formula was unchanged. Final new case layouts and the small
D00 opening/PUE changes still need a built-in-browser visual walkthrough; earlier
standalone browser checks do not cover these changes.

## D13 modular-delivery exercise — 2026-09-12

Two reader lessons and the D13 check-in now use the same synthetic 20 MW phase.
Reviewed the electrical and coolant calculations, local support-load assumption,
parallel schedule and release ownership. At 480 V balanced three phase/PF 1,
100/200 kW require 120.3/240.6 A. At cp 4.18 and 10 K, water flow is 2.39/4.78 kg/s.
The stipulated quadratic branch model raises 20 kPa to 80 kPa, above 60 kPa
available. These are explicit teaching assumptions, not equipment selections.

Independent site work finishes week 8; factory assembly 6 weeks plus transport 1
joins it before 2 weeks of connections and 2 of acceptance. Approval at weeks
0/3/5 gives completion at weeks 12/14/16. The site-built comparison is week 16.
Source review dates are preserved; no new external review is claimed. The reader
now displays the authored visual captions so numerical assumptions remain visible
next to its summary diagrams.


## Primer, workload copy and feedback verification — 2026-09-12

This revision supersedes the earlier primer scene counts and the direct workload-to-supply handoff recorded above. The Primer has 19 scenes and 1,205 seconds of planned cues. It has no optional label, skip link, course-forward reference or reassurance outro. New examples cover AC waveforms, power factor, standby versus online UPS, model loading, payload completion and cold-plate heat transfer. Author-only provenance is in PRIMER_EVIDENCE.md.

All 19 workload scenes were edited for concise headings and diagrams. Repeated eyebrow, SVG subtitle banners, stage boundary paragraph and narrative recaps were removed. Detailed assumptions remain in the Explanation dialog; essential assumptions and units remain beside the quantities.

Verification on the reviewed source:

- 57 Python tests and 94 JavaScript model tests pass. Generated historical course, expanded reader, domain map and research metadata are current; Python lint and diff checks pass.
- Primer static checks cover 19 scenes, every control/diagram state, new arithmetic and UPS paths, legacy hashes and zero reference/chapter pointers. Workload static checks cover 82 scene/state/layout combinations and parse generated SVG as XML.
- The built-in Codex browser checked all 19 default scenes in each presentation at 1280 × 720 and 390 × 844 for SVG text bounds, collisions and horizontal page overflow. Three workload timeline label collisions were fixed and rechecked. Representative desktop and mobile screenshots were inspected and retained in the task.
- Additional interactions checked AC polarity, UPS interruption, 1,000 Mb/s payload timing, two/four training devices, answer reveal and Explanation open/close. These checks sample controls; they are not a fresh exhaustive browser run of every state, theme, zoom and screen size.
- Both final presentation actions were clicked and landed on their respective reader check-ins with focus and scroll placement. Answer reveal and continuation to the next topic worked. The land lesson visibly offers the greenfield/brownfield comparison and original Colossus case beside its introduction.
- Descriptive topic names replace visible domain codes in current course interfaces and guidance. Stable internal IDs and historical verification entries remain.

No standalone browser or browser installer was launched for this review. The planned timing still needs an aloud dry run and learner feedback. FEEDBACK_AUDIT.md tracks every user request and publication status.

Publication verification: commit `8aa6549a1a72db6f693c4a71c9dccacdfc63ed69` deployed successfully in Pages run `34720114864`. Sixteen live files matched local bytes, including both revised presentation shells and changed modules, reader, domain map, course data, case module, land/delivery lessons and author records. The course map also rendered descriptive topic names without visible domain-code labels or horizontal overflow at desktop size.


## Numbered chapters and presentation directory — 2026-09-12

The reader now has one numbered chapter directory, an All chapters / Slides available filter, expandable readings and direct presentation links. The presentation catalog is teaching-sequences.json; numbers follow the curriculum sequence, starting with the Primer and ending with the integrated cases. Six distinct decks appear in seven chapter placements because cooling spans two chapters. UPS, 800 V and cooling are marked as selected topics. The duplicate footer menu and historical-introduction link are removed. Author resources are collapsed separately.

The four production follow-ups are unchecked in COURSE_REVIEW.md; TEACHING_STANDARD.md records the required chapter/case handoffs. The previous long feedback audit is replaced with the confirmed decisions and links to those owners.

Verification:

- 66 Python tests and 94 JavaScript model tests pass. Seven catalog tests cover derived numbering, shared-deck placement, missing files, invalid routes, duplicates, selected-topic scope and numbered manuscript labels. Two staging tests verify retirement and durable redirects. All generated-course, domain-map and research freshness checks pass.
- The built-in browser opened all seven sidebar presentation links at 1280 × 720 and 390 × 844, including the heat-rejection deep link. Shared numbered titles loaded and no horizontal overflow was observed. Desktop and mobile screenshots of the new sidebar were inspected.
- Checked the slides filter, title search, empty results, all-chapter reading search, numbered reading navigation and the mobile drawer. The selected view persists in the URL. Readings close the mobile drawer after navigation.
- The 800 V deck and presenter notes render after the script's module conversion; navigating to its circuit scene works. Its sample reader retains chapter number 8.
- The staged historical introduction redirects an Abilene hash to the corresponding current lesson and preserves the slides filter. A root legacy lesson hash also resolves to the current reader. Separate JavaScript checks exercised all 22 old hashes, root/diagram paths, malformed/current/unknown hashes and query parameters (52 redirect executions).
- No browser console warnings or errors were observed. Testing used the built-in browser; no standalone browser was launched or downloaded.

These checks verify navigation and existing presentation startup, not completion of the four production follow-ups or rehearsal of the course.

## Primer continuity and simpler slide navigation — 2026-09-12

Power factor now compares voltage/current waveforms before introducing the ratio
in author notes. Slides 14–19 follow a compute server from model loading through
network transfer, GPU heat and cooling to a separate whole-facility PUE account.
The network endpoints and illustrative transfer boundary are explicit. The
unexplained PUE bottom caption is removed.

The Primer has no rehearsal cues, prescribed slide times or Explanation panel.
Supporting prose is in PRIMER_NOTES.md. Primer and UPS have visible Back to course
links; workloads has one course exit and its final check-in, with the redundant
overview and reading links removed.

- All 66 Python tests and 94 JavaScript tests pass. Generated course, expanded
  reader, domain map, research metadata, site staging and whitespace checks pass.
- Primer static checks pass for all nineteen scenes and every control state.
  Independent integration of the actual desktop/mobile SVG traces verifies
  equal RMS voltage and average power, with 25% greater RMS current at PF 0.8.
  Network timing checks give 6.41/0.65 ms for an 8 MB chunk at 10/100 Gb/s,
  including the fixed illustrative 10 µs first-bit latency.
- The built-in browser checked the seven revised diagrams at 1280 × 720 and
  390 × 844 in the active light theme for text collisions, SVG bounds and page
  overflow. Representative power-factor, memory, heat, network and PUE views
  were visually inspected. Revised final network/PUE labels were rechecked.
- Checked both network rates and selection restoration, Primer exit from the
  first slide, entering/leaving fullscreen, UPS exit at mobile width, and the
  workload opening and end check-in. No browser warnings or errors were found.
- The legacy workload browser script has no static mode and could not load its
  absent Playwright dependency. Its browser checks were performed through the
  built-in browser instead; no browser package was installed or launched.

These checks do not establish spoken runtime, learner comprehension or a new
exhaustive review of every theme and pre-existing slide state.

## Primer watts, polarity and three-phase power — 2026-09-12

Applied the primer revisions in sequence: clarified power as energy transferred
per second, moved the resistor heat label below all four heat arrows, replaced
the initial DC trace with a constant level, and tied AC polarity to labeled
resistor terminals and conventional-current direction. Removed the ripple
caption. New voltage-variation and three-phase-total-power scenes bring the
primer to 21 slides. Author notes and current slide-count guidance are updated.

- All 66 Python and 94 JavaScript tests pass, along with generated-artifact,
  research, staging and whitespace checks.
- Primer static checks cover 21 scenes and every control state. They verify the
  DC baseline, voltage scaling, three power contributions and their sum. All
  361 samples of the actual rendered phase-power curves sum to the flat 30 kW
  trace within SVG rounding tolerance, in desktop and compact layouts.
- The built-in browser checked all 26 changed scene/control/viewport cases at
  1280 × 720 and 390 × 844. A compact AC/DC time/terminal-label overlap was fixed
  and all three AC states were rechecked. The watts, resistor heating, polarity,
  voltage variation and three-phase-power diagrams were visually inspected.
- The new power example explicitly assumes balanced sinusoidal voltage with
  equal resistive loads. Its straight trace is total instantaneous power, not
  voltage or the largest individual phase. Voltage-variation values are
  illustrative levels, not equipment operating limits; transformer tap/rating
  qualifications are retained in the author notes and evidence.

Browser checks used the active light theme and the built-in browser. Spoken
runtime and beginner comprehension remain for the planned teaching review.


## Overview and workload review — 2026-09-12

Chapter 2 retains 13 slides and adds a Google TPU v4 photo/OCS/ICI example,
qualified multi-data-center training context, coolant terminology and a revised
capacity headline. Chapter 3 is rebuilt as 18 slides: named GB300 NVL72 service,
Llama 3.1 70B state and KV accounting, visible training/inference comparisons,
continuous batching, same-work energy, production H100 telemetry, conditional
scheduling and a workload-to-supply brief. The old threshold quizzes are removed;
retired hashes resolve to the corresponding taught content. Three D02 reader
lessons and nine source records were updated alongside the presentation.

Verification:

- 67 Python tests and 121 JavaScript tests pass. New checks cover the named
  KV geometry, binary capacity, complete-request allocation, same-work energy,
  continuous slot membership and rendering all retained slide/control states.
- Generated introduction, expanded reader, domain map and research checks pass.
  Site staging and whitespace checks pass. Browser harnesses were updated for
  the new scenes; they were not run in a standalone browser.
- The built-in Codex browser checked all 18 workload default scenes at
  1280 × 720, 390 × 844 and 844 × 390 for SVG text bounds, text collisions
  and horizontal page overflow. One narrow ending-label overflow was corrected
  and rechecked. The training-state labels were clarified after independent
  technical review and rechecked at all three sizes.
- Exercised all six workload button choices at desktop and phone width: selection
  state follows the selected option; scheduling changes peak 480 → 340 kW at
  unchanged cycle energy, dependency changes the waiting paths, and transition
  duration changes the rate 160 → 1,600 kW/s.
- Inspected representative intro, memory, batching, production-trace and TPU
  screenshots. The actual publisher-hosted H100 figure and TPU photograph loaded.
  Checked Explanation open/close, the retired acceptance-envelope hash and the
  final link into Section 4. No browser warnings or errors were observed.
- The overview's changed views were checked in twelve scene/state/viewport cases
  across the same three sizes, including the TPU toggle, selected state and image.
  Independent source review keeps pod ICI distinct from inter-cluster networking,
  rounded model quantities distinct from throughput, and simulation distinct
  from production telemetry.

These browser checks used the active light theme; they do not establish a new
exhaustive theme/zoom/accessibility review, spoken runtime or author acceptance.
The chapter tracker records the revised material as ready for author review.

## Chapter 5 rebuild — 2026-09-12

Chapter 5 now has 20 scenes. Five requested/spatial figures were generated with
GPT ImageGen and visually inspected. Colossus 1 uses its actual official aerial;
Lenovo specifications distinguish the approximately 1,580 kg rack and 29 kg tray.
Source notes P122–P128 and the D12 reader record the cooling, fiber and case-study
boundaries. The mineral-rights case retains the Texas RRC qualifications in the
reading. It is not a finding about Abilene title.

Validation completed for this revision:

- **72 Python tests** and **140 JavaScript tests** passed. The site tests exercise
  rendering across declared states and resolve retired hashes to retained scenes.
- Course, expanded reader, domain map and research metadata checks all passed;
  generated outputs are current and `git diff --check` is clean.
- A local staged-site **headless Chromium** sweep checked 20 scenes at
  1440×900, 1280×720 and 390×844 in light and dark appearance: **120 states**,
  with no script errors, broken images, horizontal overflow, desktop footer
  intrusion or overlapping visible SVG text. Screenshots were captured for
  every scene at 1440 and 390 pixels; the changed physical mechanisms and
  representative narrow/dark versions were inspected visually.
- Run/stop selection and the state of both cooling trains were checked in all
  six viewport/theme combinations. Fullscreen retained the selected device
  theme in both appearances. The retired sidecar hash reaches tray service;
  the former recap hash maps to the final control-dependency scene.
- Visual review corrected a route crossing a wall, overlapping room labels,
  incomplete DC-link connections, tiny mobile diagram labels and dark-theme
  soil-label contrast. The generated tray image has no manufacturer label.

Temporary screenshots and sweep results are in `/tmp/chapter5-final/`. These
checks establish rendering and the explicitly described teaching relationships,
not construction accuracy or author acceptance. The next author pass starts at
[slide 14](prototypes/site-format.html?teach=1#service-envelope).

## PSU and BBU product photographs — 2026-09-13

- Added `psu-hardware` and `bbu-hardware` before the existing mechanism scenes;
  the rack-to-chip deck now contains 13 slides. Existing model inputs and controls
  are unchanged.
- Four manufacturer images inspected directly; original bytes retained with
  source URLs, dimensions and SHA-256 records. The viewport crops whitespace only.
- In-app browser: both photo slides inspected at 1280 × 720 and 390 × 844.
  Two images per slide, readable labels, no horizontal overflow; mobile content
  remains vertically scrollable. Browser error/warning log was empty.
- All 72 Python and 142 Node tests passed, including the rack-power models.
  Research/reader generation and site staging passed. Publication identified a
  stale domain-map source listing; it was regenerated and all workflow checks passed locally.
  `git diff --check` passed. This is a scoped photo integration check, not a new
  whole-course visual or author-acceptance claim.

## Chapter 5 cases and service boundaries — 2026-09-13

- Twenty scenes. The original opening three scenes, rack/tray comparison and
  service-envelope scene retain their content. Retired scene hashes resolve to
  relevant retained scenes, including the new replacement check-in.
- Added TCDC/Getty legal context, ADA Docklands groundworks, Equinix HO1 Harvey
  access, QTS Suwanee introduction, Rogers Toronto acoustics and Lenovo PSU
  hot-swap. Four new source images/figures have recorded SHA-256 provenance.
- The six site tests pass: every scene and declared control state renders in
  both layouts; the check-in separates qualified remaining supply capacity,
  compute-tray power-off and the complete handling/floor-load route.
- Built-in Codex browser inspected ten changed scenes at 1280×720, 390×844 and
  844×390. All four new images loaded; no horizontal overflow or SVG text beyond
  its viewport. The revealed check-in worked. A landscape check-in heading
  collision found by screenshot inspection was corrected with natural page
  height; its title and content now occupy separate vertical areas. Browser
  error log was empty. No external testing browser was installed or launched.
- Case photography and the desktop foundation, Getty and check-in layouts were
  visually inspected. Evidence review added Getty's feasible low-pump alternative
  and the surface owner's own-alternatives condition to the legal notes.
- This is implementation and layout verification, not measured learner outcomes
  or author acceptance. The exact mineral-caused-delay and flooded-bridge examples
  remain unverified as recorded in FEEDBACK_AUDIT.md.

## Chapter 6 distribution — 2026-09-13

- Separate GPT-6 Astra / Ultra agent authored 30 scenes covering D04.1–D04.4,
  three primary-source equipment/site cases, five actual photographs and an
  extension decision that checks service and IT-branch capacity separately.
- Twelve dedicated Node tests pass, covering kW/kVA/current and heat balances,
  reserve, phase limits, branch-current sums, open paths, invalid inputs, all
  scenes/control states, source assets and each check-in outcome.
- Agent used only the built-in Codex browser. All 30 scenes were checked at
  1280×720, 390×844 and 844×390: no horizontal overflow, stage clipping or SVG
  text outside its bounds; every image loaded. All 30 control selections,
  check-in reveal, scrolling, Back to course, Reading, keyboard navigation and
  full-screen enter/exit were exercised. Dark palette spot checks used a local
  wrapper with the production CSS variables. Viewport reset afterwards.
- Review fixes: losses leave equipment as a heat branch; the fifth rack crosses
  the busway limit; building branches visibly join their bus; labels avoid wires;
  repeated meta-commentary and extra chapter links are removed.
- Case assets were inspected by both author and integrator. Source records
  distinguish the Compass factory image, Fujitsu's unspecified north-London site,
  the 2012 Green installation and the dated Abilene aerial. Oracle was deduplicated
  to P102. Generated images were optional; actual photos and code diagrams were
  used for this chapter.
- Integration adds the Chapter 6 directory entry, public `/slides/distribution.html`
  route, reader case sections and source/provenance records. Full checks: 72 Python
  tests and 155 Node tests pass; course, expanded-reader, domain-map and research
  freshness checks pass.

## Chapters 7 and 8 integration — 2026-09-13

- Chapter 7 is a separate 26-scene D05 deck at `continuity-format.html`.
  It reuses the reviewed UPS, bypass, capacitor, generator, redundancy and
  reliability renderers. Added storage power/energy comparison, the real Sparks
  storage site, fault isolation, grounding, AC/DC interruption and the
  whole-service check-in. Fairwater retains its own `tier-investment` scene.
- Chapter 8 is one 32-scene D06 deck at `rack-energy-format.html`: the retained
  rack-to-chip and 800 V sequences share navigation and rendering functions.
  Both named PSU/BBU photo scenes remain. Added inlet-power accounting, physical
  scale context and a retrofit decision with a power/date reversal.
- One historical Zurich-West scene moves the unique 2012 case into Chapter 8:
  1 MW DC, 380 V distribution, transformer plus rectifier in the central unit.
  ABB's 400 V open-circuit specification is distinguished from its diagram label.
  P153/P154 and the existing photo are reused; no generic loss/heat slide is
  duplicated. `green-dc` and `green-path` are aliases in Chapter 8.
- Actual built-in GPT ImageGen produced the Chapter 7 electrical-room context and
  Chapter 8 rack/board/package illustration. Exact prompts and provenance are
  retained beside the assets and in `rack-energy-source-additions.proposed.json`.
  These images provide physical context, not product or circuit evidence.
- P157 registers Redwood's Sparks aerial/context; P158 registers Schneider's
  conceptual TN return path (indexed public text reviewed; direct page unavailable).
  The local NVIDIA rack figure uses existing P64. P159 registers the independently
  researched controls-transformer operating limits and unchanged product photo for
  the concurrent Chapter 6 revision; its teaching integration is reviewed separately.
- 69 scoped Node tests pass, including shared navigation, retained UPS mechanisms,
  capacitor energy balance, storage/service models, every legacy scene/alias,
  rack power, retrofit constraints and shared renderers. All 73 Python tests pass.
  Course, expanded-reader, domain-map and research checks pass; research generation
  includes discovery candidates as required by the publication workflow.
- The catalog has one Chapter 7 and one Chapter 8 entry. Site staging includes the
  four shared web modules. Nine old URL redirect chains were executed in Node:
  query strings, fragments and scene destinations remain intact. Seven canonical
  and legacy routes return HTTP 200; a static import/link/asset traversal finds no
  missing dependencies from the two staged entrypoints.
- Prior native Codex browser inspection covered all 26 Chapter 7 scenes at
  1280×720 and 390×844, and all 31 pre-Zurich Chapter 8 scenes at desktop size,
  with narrow follow-ups and both manufacturer photo scenes. Controls, reveals,
  keyboard focus and scroll reachability were exercised. Dark checks used a
  temporary local fixture activating the production dark palette, not an OS
  appearance change. Source still follows device appearance and reduced motion.
- **Remaining visual check:** native browser access was unavailable during final
  integration (the child reported a locked Mac; the integrator found no browser).
  The new Zurich slide and final public redirect/navigation paths therefore have
  no new browser pass. Native fullscreen state is also unconfirmed. No external
  or headless browser was used as a substitute. This is implementation evidence,
  not author acceptance or a whole-course visual pass.


## Chapter 6 review revision — 2026-09-13

- Reworked the 30-scene deck into 18 scenes. Added switchgear anatomy, separate
  relay and breaker actions, isolation versus surge protection, and a failed
  interruption diagnosis. Consolidated the power-factor, tap-off and growth
  examples. Chapter 8 receives the unique historical DC case; old links survive.
- Four built-in GPT images are included with provenance. Actual in-app-browser
  screenshots checked the opening, transformer-location comparison, PDU/PSU
  comparison and continuity handoff. They are conceptual illustrations.
- All 18 scenes received DOM geometry checks at 1280×720 and 390×844. Desktop
  stages fit without vertical clipping; SVG labels stay in the SVG viewport.
  Narrow horizontal overflow was corrected by allowing the main grid item to
  shrink; wide figures scroll within their own region. All image assets loaded.
- All 17 state buttons and the diagnosis reveal were exercised with the native
  in-app browser and their pressed/expanded states verified. Visual inspection
  corrected a sensor-label collision and breaker-terminal connections. Navigation
  uses short labels and the shared footer. New actual OS-dark/fullscreen checks
  were not performed in this revision.
- Primer now includes a 23rd scene: the Schneider Phaseo ABL6TS25B controls
  transformer, its real photograph and published operating input ranges. The
  mobile slide was visually inspected; the 23-scene static test passes.
- 73 Python tests pass. Distribution rendering/model checks and generation,
  expanded-reader, domain-map, research freshness and diff checks pass. The
  previous full Node run passed 168 tests; a concurrent Chapter 5 edit temporarily
  broke its own text assertion, outside this scoped release.
- This records implementation checks, not author acceptance.


## Chapter 5 context and ending revision — 2026-09-13

- Added two context scenes, giving 22 total. Both liked engineering cases are
  preserved. ADA’s proposed-campus rendering precedes groundworks; the NWS-hosted
  TxDOT Houston flood photograph and Harvey timeline precede HO1’s operating case.
- Replaced static fire-room illustration with a causal exit-route comparison.
  Tested all six layout/incident combinations and checked corridor/door geometry.
  The final replacement exercise contains two cards; answers replace questions.
- Corrected three missing media-query braces in the existing page stylesheet.
  All 22 scenes received native in-app-browser geometry checks at 1280×720 and
  390×844: no horizontal page overflow or desktop stage overflow. Image loading
  completed on the repeated pass. New context images, egress incident and concise
  reasoning were visually inspected; all egress/answer selections were exercised.
- 170 Node tests and 73 Python tests pass. Three new source records preserve
  historical dates, image credits and the limited OSHA indexed-text review.
  Reading, research metadata and site staging were regenerated. No new actual
  OS-dark or native-fullscreen claim is made; author acceptance remains pending.
- Chapter 6 revision 5195f94 was published separately; its Pages deployment
  succeeded and its live scene/equipment/transformer modules matched that commit.

## Chapter 7 review revision — 2026-09-14

- Thirty active scenes retain the former hashes. New: `capacitor-energy`,
  `battery-ramp`, `dc-feeder-protection`, `tier-overview`.
- Numerical tests derive 64 kJ initial, 49 kJ remaining, 15 kJ usable; 5 kJ
  ramp deficit and 768.1146 V; recovery at 50/100 ms and other supplied durations.
  Shared-bus tests distinguish closed upstream contacts during the fault from
  clearing, with no supported load group in either state.
- Built-in Codex browser: all thirty default scenes at 1280×720 and 390×844
  (60 geometry checks), no horizontal overflow, desktop stage overflow, missing
  loaded images or rendered SVG text outside its viewport. Actual screenshots
  reviewed for equipment, capacitor derivation/recovery, grounding, DC feeder,
  pyramid and the knowledge-check reveal in the active dark device theme.
- Headless Chromium: 151 scene/control/layout cases across light/dark and
  1280×720 / 390×844. All action buttons exercised on desktop, plus repaired
  control supply and generator/recovery states. No page errors, pressed-state
  failures or clipping. The test measures transformed text in screen coordinates
  so the existing rotated maintenance-bypass label is assessed correctly.
- Energy subagent separately checked 20 light/dark compact/desktop render states.
  No new native fullscreen or OS-theme-switch check is claimed.
- 175 Node tests and 73 Python tests passed. Course, expanded reader, domain map,
  research metadata (including discovery candidates), staging and whitespace
  checks passed. P168–P171 registered; prior source entries preserved.
- `/tmp/ch7-full-qa.json` records the complete automated scene/control findings;
  `/tmp/ch7-energy-qa/findings.json` records the independent energy render checks.

## Chapter 9 compute, memory and the rack — 2026-09-14

- Added `compute-format.html` with **21 scenes**, the existing shared navigation,
  device-based light/dark colors, direct Reading links and no source/notes popup.
- Source and model work were delegated independently. Three D07 reader lessons
  now support the exact chapter mechanisms; P172–P176 add current NVIDIA hardware,
  coherent-memory, failure-recovery and health-check references. Existing relevant
  entries retain their IDs and receive scoped review updates.
- **187 JavaScript tests and 73 Python tests passed.** Twelve new numerical tests
  cover memory-read timing, overlapped compute/HBM bounds, the roofline knee,
  concentrated versus dispersed failures and reduced-service prerequisites. The
  catalog test now expects the tenth registered presentation.
- All **21 scenes at the native desktop viewport and all 21 at 390×844** were
  inspected through the built-in Codex browser. No page-width overflow or SVG
  text outside the drawing area; no desktop page-height overflow. Actual screenshots
  checked the manufacturer figures, HBM leaders, transfer boundaries, roofline,
  matrix shapes, fault layouts and the closing comparison.
- Exercised all **11 parameter choices** and all **three diagnosis answers** in
  the native browser. Selected buttons match state; the four-GPU choice survives
  leaving and returning; keyboard next works. Enter/exit fullscreen preserves the
  light device palette. Temporary viewport override restored afterward.
- Earlier automated light/dark render checks covered 1440×900, 1280×720 and
  390×844 (210 scene/control states, no page errors, image failures or clipping).
  Final geometry and interaction verification was performed in the native browser.
- The visual pass fixed a log-axis/straight-line roofline error, moved NVSwitch
  outside the accelerator enclosure, made a four-element vector match the
  four-column weight tile, and attached the interposer leader to its actual layer.
  Narrow diagrams use separate readable compositions.
- `gigawatt.build_course --check`, `gigawatt-expand --check`, `gigawatt-map --check`,
  `gigawatt-research check --include-candidates` and `git diff --check` pass.
- These are implementation/source/browser checks. Kian's first Chapter 9 dry run
  and feedback are still pending in the existing course review tracker.


## Chapter 7 capacitance without calculus — 2026-09-14

- Chapter 7 now has 31 scenes. New `capacitance` introduces charge and the
  meaning of farads; `capacitor-energy` replaces differentials with a numerical
  voltage–charge triangle and explicit algebraic substitution. Existing hashes
  and hold-up, battery-ramp and recovery models remain intact.
- OpenStax College Physics 2e §19.7 was reviewed directly. The reader and P171
  source note use its algebraic derivation. The average is over charge, and
  charge on either plate is distinguished from the capacitor's net charge.
- Built-in browser: inspected desktop screenshots of both revised diagrams and
  the following hold-up slide. Geometry checks passed for the four capacitance,
  energy, hold-up and ramp scenes at 1280×720, with no page overflow or SVG text
  outside the drawing. Both new compact diagrams passed width and SVG-text
  bounds at 390×844. No browser warnings/errors. Mobile screenshot capture did
  not match the browser's reported geometry, so no clean mobile screenshot claim
  is made. Temporary viewport override was restored.
- 192 JavaScript tests and 76 Python tests passed. Course, expansion, domain map,
  research metadata and whitespace checks passed. No new OS-theme or native
  fullscreen check was performed.
- The existing chapter tracker was refreshed; author feedback and final
  acceptance remain separate. Chapter 10 is being authored independently.

- Published capacitor revision: `0af3caf19270b0fd8efbd27f817df206fe9d8ff0`.
  Pages run `34891342550` succeeded; live `continuity-energy.js` and
  `continuity-scenes.js` bytes match the locally staged revision.


## Chapter 10 networking and interconnects — 2026-09-14

- 22 scenes use the shared header, footer, selector and automatic chapter
  continuation. Chapter 9 now opens Chapter 10; Chapter 10 continues to the
  Chapter 11 reader until that presentation exists.
- Independent source review supplied actual NVIDIA adapter/switch figures and
  Google's OCS figure. New source records P182–P187 and the three D08 reader
  lessons support the hardware, media, ring and fabric examples. Existing
  Meta/Google/NCCL IDs were reused. GPT ImageGen created the spatial opening.
- Built-in browser: all 22 default scenes checked at 1280×720 and 390×844.
  No horizontal overflow, broken loaded image or SVG text outside its viewBox.
  Actual desktop screenshots inspected all 22 scenes. Found and corrected
  overlapping server/tally labels, disconnected endpoint cables in the fabric
  diagram, and a carrier slide that exceeded the desktop viewport by 10 px.
  Rechecked the corrected layouts. Compact versions reflow rather than scaling
  the full desktop composition.
- All 13 parameter choices exercised; pressed states match the selected
  condition. Diagnosis selection and reveal exercised. Native fullscreen enter
  and exit work; no OS-dark change was made during this pass. Temporary
  responsive viewport override was restored. No browser warnings/errors.
- 200 JavaScript tests and 76 Python tests passed. New numerical tests cover
  one-direction fabric capacity, bytes/bits conversion, ring phase endpoints,
  overlap and propagation; navigation tests cover the newly built handoff.
- Technical checks establish the authored draft's implementation state. Kian's
  first Chapter 10 review remains pending in COURSE_REVIEW.md.
