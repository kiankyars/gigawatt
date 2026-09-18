# Audit of removed and relocated slides

Checked September 16, 2026 against the available user-message history, Git
changes, current scene definitions and image provenance. Slide numbers below
refer to the current course. Scene IDs remain the more stable references.
This workspace snapshot includes the concurrent Chapter 12 and 13 revisions;
those revisions are separate from the commit containing this report.

**Latest update — 18 September 2026:** the Chapter 16 replacement below
supersedes the September 16 five-case retention decision. Earlier numbered
records remain historical.

**Yes: some slides originally requested or supplied by Kian were later removed
as standalone slides. The concrete cases below have later user instructions
approving their replacement, merger or relocation. No contradictory removal
was found in the histories inspected.** This is a bounded audit, not proof
about every historical task. A Git author name alone does not establish that
Kian personally created a slide.

## Requested material that later changed form

| Original addition | Later user instruction | Current result |
| --- | --- | --- |
| Chapter 9 AC/DC comparison image, formerly `dc-architecture-changes` | September 16, 16:22 PT: “I prefer slide 13 over slide 11, to be honest.” The preceding correction explicitly identified those two slides. | Removed in `e5972ea`; the preferred three-column `ocp-power-architectures` comparison remains. The original `dc-hall-before-after.png` is still stored. |
| Chapter 8 capacitor/BBU/generator/BESS hierarchy, formerly `rack-transfer` | September 16, 14:56 PT: “Also please merge the two diagrams that you mentioned.” | Merged into `energy-locality` (“Where backup power connects”), retaining all requested sources and their connection points. |
| Separate converter-heat calculation | September 16, 15:37 PT: “Sounds good regarding replacing slide 7 calculation with one high-level before-and-after comparison.” | Replaced in the later DC revision. The subsequent image/comparison choice is recorded above. |
| Standalone Compute chapter, with a protected opening image and meme | September 15: “Go ahead and make that migration,” then an explicit request to preserve the image and meme by moving them. | Chapter retired with authorization. Both protected visuals remain in Networking. |
| Former storage chapter’s five protected examples | September 16, 17:10 PT: “I like those four slides you want to keep and I like the Lama example too. Please keep that and move it to the respective spot.” Later: “Continue with the migration.” | Meta storage tiers remains in Chapter 10; Google demand response, its deadline exercise, Gmail and Llama remain in Chapter 14. |

## Recent simplification cuts

| Chapter | Standalone scenes removed | What happened to their teaching content |
| --- | --- | --- |
| 11 | `heat-path`, `branch-flow`, `coolant-interfaces` | These match Kian’s specific redundancy/unnecessary-content feedback. The CRAH/CDU distinction and four capture methods remain. On September 17, `capture-coldplates` and `crah-cdu` were combined into `capture-options` at the author’s request. GB300 rack coolant entry was added; rear-door cooling remains a separate mechanism. The dictation-error speaker note remains removed. |
| 12 | `two-ceilings`, `reuse-interface` | Folded into `hot-hour` and `heat-reuse`; detailed calculations remain in the reader. No separate user request for either retired slide was found. |
| 13 | `delivery-paths`, `site-checks`, `handover-records` | Folded into the critical-path, factory-acceptance and release-decision slides. The approved revision excluded the previously requested additions listed below. |
| 14 | `diagnostic-observations`, `google-verification`, `control-delay`, `return-to-service`, `common-cause`, `overlap-outages`, `causal-evidence`, `diagnosis-check` | Combined with retained explanations or moved to reader detail. No separate request for these individual slides was found. The former DeepMind verification diagram is no longer displayed; thermal-budget and outage-overlap calculations remain reader material. |
| 16, this revision | `outage-timeline`, `weather-demand`, `density-choice`, `job-evidence`, `phase-handover` | Folded into the outage brief, weather-paths, density brief, job consequence and phase schedule respectively. All five cases and the Abilene image remain. |

“Retained in the reader” does not mean “still visible on a teaching slide.”
The rows above distinguish those outcomes.

## Explicit additions still present

- **Chapter 11:** stacked CRAH/CDU and air/cold-plate comparison at slide 2; GB300 coolant entry at slide 3; rear-door cooling at slide 4 and immersion at slide 5.
- **Chapter 13:** the 20 MW case is now slides 3–7, immediately connecting the changed rack layout to electrical, hydraulic and support consequences. A separate schedule case occupies slides 8–9. Prefabrication occupies slides 10–13; OCP interface specifications are slide 14. The commissioning sequence follows.
- **Supplied Chapter 13 examples:** hardware-price meme is slide 2, Houdini slide 12 and Siemens–Compass slide 13. The original meme and both construction photographs remain unchanged.
- **Explicit September 17 cuts:** generic manufacturing-release and shipping checklists, interactive package approvals, and both factory-week arithmetic exercises are removed from the active deck. Their engineering detail remains in the reader and old scene links redirect. This follows the latest author request and supersedes the earlier request to retain them as standalone slides.
- **Protected storage/recovery examples:** Meta RSC in Chapter 10; Chapter 14
  Google demand response slide 9, deadline slide 10, Gmail slide 15 and Llama
  slide 17.
- The supplied rack-input, conversion, VRM, recharge, power-stack, Microsoft,
  leaf–spine and optics visuals still have active teaching uses.

## Evidence trail

The dated quotations above were checked against original user messages, not
assistant descriptions of what the user wanted.

- Main task `01a0a716-2551-76f0-9b71-9189174661ef`, local rollout
  `rollout-2026-09-15T15-00-41-01a0a716-2551-76f0-9b71-9189174661ef.jsonl`:
  lines 3972 (merge), 5035 (replace calculation), 5282/5363 (supplied image),
  5595/5625 (preferred comparison), 6633/6888 (protected cases and migration).
  Other explicit cuts appear at 2644 and 7797.
- Parent task `01a0a715-4f29-75f3-bcc0-a8238d6b07dc`, read through task history:
  user items `01a0a6c1-aa3f-7ac0-b959-1e0c8a05650c` (backup hierarchy),
  `01a0a707-d187-7bf0-a7cc-f4884c957af9` and
  `01a0a70a-3ecc-77c2-93a9-2c18680538d2` (Compute migration and protected images).
- Archived September 12 task `01a096e7-dc1d-7eb2-9c44-b493c2c4a4a5`, rollout
  ending `01a09728-dcd9-7262-8fbd-aa454160ace3.jsonl`: line 352 (D13 topics
  and fixed-20 MW exercise), 8372/8710/9259 (separate construction examples),
  9629 (supplied memes).
- Current [scene and image sources](prototypes/),
  [DC image provenance](assets/references/rack-energy-review-figures.provenance.json),
  and Git changes establish what survives. Current local changes were compared
  with HEAD; uncommitted work in other chapters was preserved.

## Chapter 14 review — September 17, 2026

The standalone same-temperature timestamp, command/acknowledgment and wrong-row mapping slides are removed. Their relevant concepts remain in complete row measurements, startup traces and the Chapter 13 commissioning example. Google cooling and demand response, Cloudflare, Gmail, London and Llama 3 remain; context expands the chapter to 21 slides. Meta's original maintenance diagram is added. Previous scene links redirect to the corresponding current topic.

## Chapter 15 commercial-model rebuild — 17 September 2026

Removed the repeated spare-power/accepted-path constraint exercises, ownership-versus-contract NPV toy model, cost-per-accepted-result invoice, artificial upgrade-delay comparison, adjacent Microsoft-campus detour and closing evidence quiz. Replaced them with GPU capacity versus API billing, bare metal and managed software, on-demand/interruptible/committed products, contract tenor, historical rental prices, billable occupancy, contract financing, energy-cost allocation and Abilene targets versus delivery. The D15 reader and domain objectives now match this scope. Earlier physical capacity constraints remain in their engineering chapters and the five integrated cases.

## Chapter 16 Abilene finale — 18 September 2026

Kian authorized the proposed replacement: one connected Abilene case instead
of five independent hypothetical cases. **Putting an AI Factory Together** has
nine slides connecting the course's engineering and commercial decisions.
This is a new presentation awaiting author review; Chapters 1–13 remain accepted.

| Retired presentation material | Disposition |
| --- | --- |
| Separate outage, weather, retrofit, network and phased-opening cases | Removed from the finale. The C01–C05 reader exercises and numerical models remain optional practice; relevant mechanisms are already taught in their engineering chapters. |
| Hot-weather rack-count comparison | Removed. Its supported-load comparison could be mistaken for a change in installed GPU inventory. |
| Auxiliary-power saving versus cooling-capacity exercise | Removed from the finale because it repeats the local-versus-site constraint reasoning in Chapter 14. |
| `phase-choice` rack matching and `phase-schedule` arithmetic | Removed from the presentation rather than replacing them with another elementary selection task. |
| Abilene photograph and useful system connections | Reused as appropriate in the connected Abilene case; actual site facts remain separate from explanatory engineering relationships. |

The existing `integrated-cases` deck route is retained. Old fragments redirect
into the new sequence. Keeping the original reader exercises does not mean
they remain part of the final presentation.

Chapter 11's device-temperature controls were replaced with both cases visible together. No physical mechanism was removed. Supplied control-layer and prefabrication images replace their respective diagrams without changing scene destinations.

**Chapter 11 image placement follow-up:** merged the standalone coolant-entry mechanism into cold-plate hardware and moved the NVIDIA rear view beside the RDHX discussion. The photograph remains identified as coolant manifolds. The old entry hash resolves to cold plates. A subsequent supplied immersion photograph follows the immersion explanation, bringing the sequence to sixteen slides.

## Chapters 11–13 local review — 17 September 2026

- Chapter 12 removes `weather-bins`, `water-metrics`, and `heat-rejection-check` from the active deck. Corresponding reader/model detail remains. Their old fragments resolve to the current hot-weather, tower-water and operating-dependency scenes.
- Chapter 13 removes the empty opening and the schedule brief/comparison. EPC responsibilities is the opening; the supplied prefab figure and both actual package cases remain.
- Chapter 13 `controls-interface` and `integrated-tests` become one Chapter 11 `cooling-response` scene immediately after `cooling-derating`. Old links point to that new location. The destination is Chapter 11 because it contains the cooling-loss example the author named.
- Chapter 13 removes the closing `release-decision` pattern-matching quiz. Shared rack readiness remains under a literal title. The phase-boundary scene reuses the earlier CoreWeave delivery case and photographs rather than adding another generic diagram.
- The supplied OCP rack figure is added after the retained coupling example; no user-provided image or named prefab case is removed.
