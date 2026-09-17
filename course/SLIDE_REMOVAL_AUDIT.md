# Audit of removed and relocated slides

Checked September 16, 2026 against the available user-message history, Git
changes, current scene definitions and image provenance. Slide numbers below
refer to the current course. Scene IDs remain the more stable references.
This workspace snapshot includes the concurrent Chapter 12 and 13 revisions;
those revisions are separate from the commit containing this report.

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
| 11 | `heat-path`, `branch-flow`, `coolant-interfaces` | These match Kian’s specific redundancy/unnecessary-content feedback. The CRAH/CDU distinction and four separate capture methods requested in that same review were added. The dictation-error speaker note remains removed. |
| 12 | `two-ceilings`, `reuse-interface` | Folded into `hot-hour` and `heat-reuse`; detailed calculations remain in the reader. No separate user request for either retired slide was found. |
| 13 | `delivery-paths`, `site-checks`, `handover-records` | Folded into the critical-path, factory-acceptance and release-decision slides. The approved revision excluded the previously requested additions listed below. |
| 14 | `diagnostic-observations`, `google-verification`, `control-delay`, `return-to-service`, `common-cause`, `overlap-outages`, `causal-evidence`, `diagnosis-check` | Combined with retained explanations or moved to reader detail. No separate request for these individual slides was found. The former DeepMind verification diagram is no longer displayed; thermal-budget and outage-overlap calculations remain reader material. |
| 16, this revision | `outage-timeline`, `weather-demand`, `density-choice`, `job-evidence`, `phase-handover` | Folded into the outage brief, weather-paths, density brief, job consequence and phase schedule respectively. All five cases and the Abilene image remain. |

“Retained in the reader” does not mean “still visible on a teaching slide.”
The rows above distinguish those outcomes.

## Explicit additions still present

- **Chapter 11:** CRAH/CDU at slide 4; separate capture methods at slides 2, 3,
  5 and 6.
- **Chapter 13:** EPC versus manufacturing strategy at slide 6; design release
  at slide 10; ownership of interfaces at slide 13; the fixed-20 MW rack-change
  exercise starts at slide 2 and continues through its electrical, hydraulic,
  spatial and schedule consequences.
- **Supplied Chapter 13 examples:** hardware-price meme at slide 3, Houdini at
  slide 8 and Compass at slide 12. The meme and two construction photographs
  are unchanged from HEAD.
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
