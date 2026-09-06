# Curated source discovery log

## 2026-09-06: broaden the data-center research library

This pass added **30 SemiAnalysis articles (SA11–SA40)** and **three primary sources (P13–P15)** to the existing 22-source seed. The curated catalog now contains **55 sources: 40 SemiAnalysis and 15 primary starting points**. These counts describe this dated pass; a later catalog may contain more. They do not describe every relevant article, completed full-text reviews, or verified course claims.

The aim was to find distinct contributions across the 15-domain map, especially load transients, on-site supply, networking, workloads, storage and orchestration, operations, construction, water and infrastructure economics. Sources were selected for a concrete research use, not to maximize the count. The domain-first curriculum determines what must be learned; articles supply leads, cases and claims to check.

## Method

1. Read the existing source IDs and domain map to preserve IDs and avoid duplicate URLs.
2. Run the bounded searches below and inspect the publisher sitemap index, annual lists for 2023–2026, and the top archive. Follow exact publisher article links; do not guess URL slugs.
3. Check the visible article title and publication date, then read the public introduction or selected preview sections. Record original research-use notes and source-specific cautions. Do not mark paid full text as reviewed.
4. Add the three primary references identified by the independent domain audit. Re-open each page and record the actual reading scope and version/date limits.
5. Validate unique IDs and URLs, the absence of overlap with the prior seed, date formats and valid domain mappings.

## Publisher indexes inspected

- https://newsletter.semianalysis.com/sitemap
- https://newsletter.semianalysis.com/sitemap/2023
- https://newsletter.semianalysis.com/sitemap/2024
- https://newsletter.semianalysis.com/sitemap/2025
- https://newsletter.semianalysis.com/sitemap/2026
- https://newsletter.semianalysis.com/archive?sort=top

The root pipeline work separately verified the public machine-readable sitemap (`https://newsletter.semianalysis.com/sitemap.xml`) and RSS feed (`https://newsletter.semianalysis.com/feed`). The curated pass above used annual HTML sitemaps; it did not itself enumerate and adjudicate every XML entry. The automated inventory and this curated review are separate evidence states.

## Search queries

Executed on 2026-09-06. These are a reproducible query trail, not a guarantee that a search engine will return the same ranking or complete set later.

- `site.newsletter.semianalysis.com/p/ "AI Training Load Fluctuations"`
- `site.newsletter.semianalysis.com/p/ "storage" "Datacenter"`
- `site.newsletter.semianalysis.com/p/ "Nvidia’s Optical Boogeyman"`
- `site.newsletter.semianalysis.com/p/ "datacenter" "power" "grid"`
- `site.newsletter.semianalysis.com/p/ ERCOT batch study`
- `site.newsletter.semianalysis.com/p/ optics networking optical boogeyman`
- `site.newsletter.semianalysis.com/p/ storage NAND flash SSD AI`
- `site.newsletter.semianalysis.com/p/ data center construction economics neocloud power`
- `site.newsletter.semianalysis.com/sitemap/2024`
- `site.newsletter.semianalysis.com/sitemap/2025`
- `site.newsletter.semianalysis.com/sitemap/2026`
- `site.newsletter.semianalysis.com/p/ "water" "cooling"`
- `site.newsletter.semianalysis.com/p/ "fire" "datacenter"`
- `site.newsletter.semianalysis.com/p/ "commissioning" "maintenance"`
- `site.newsletter.semianalysis.com/p/ "storage" "checkpointing"`
- `site.newsletter.semianalysis.com/p/ "BMS" "controls"`

The final gap searches for fire protection, commissioning/maintenance, checkpointing, and BMS/controls returned overlap with already selected material. No additional distinct page was selected after reaching the bounded 30-article supplement. This is not evidence that the publisher has no further coverage.

## What the broader pass changed

| Research gap | Useful additions | Why this matters |
| --- | --- | --- |
| Synchronous loads and grid response | SA11 | Connect workload behavior to electrical dynamics and continuity. |
| On-site supply and regional grid decisions | SA12, SA32, SA34 | Examine fuel, capacity markets, tariffs and regional assumptions separately. |
| Optical fabrics and protocols | SA13, SA15, SA16 | Distinguish rack scale-up, cluster scale-out and reconfigurable network designs. |
| Workload and cluster software demands | SA20–SA27, P13–P14 | Link performance, memory, scheduler placement and storage to the physical design. |
| Operational and tenant security | SA28, SA30 | Avoid incorrectly treating publication coverage as limited to equipment alone. |
| Modular construction and readiness | SA29, SA33, SA35–SA39 | Separate procurement, delivery, financing, power availability and operating capacity. |
| Water and thermal boundaries | SA31, P15 | Distinguish water-accounting boundaries from liquid-loop performance and rating conditions. |

## Reading and metadata limits

- SA11–SA40 are all `public_excerpt_reviewed`. The visible header and introduction or selected preview sections were read; complete paid articles and their underlying datasets/models were not reviewed.
- P13 is the current Slurm Topology Guide; selected topology and placement sections were read. Pin a release and validate examples before using implementation-specific behavior.
- P14 is the NVIDIA DGX SuperPOD H100 reference-architecture index only. Its linked technical chapters remain unread. It displays document RA-11333-001 V11, publication date 2023-09-22 and web update 2025-11-19.
- P15 is the OCP CDU white paper front matter, executive summary, contents and introduction only. Headers say August 2024; its version table says 11/01/2024. The catalog leaves the exact publication date null and preserves the inconsistency.
- SA25 uses the article H1 and annual sitemap title, “TPUv7: Google Takes a Swing at the King.” A search/browser wrapper exposes the alias “Google TPUv7: The 900lb Gorilla In the Room.” Preserve this alias when reconciling changed titles; deduplicate by URL.
- The original seed still contains one `candidate_not_reviewed` source, P11 (NFPA 75), whose substantive content was not available in the accessed page. All other records still retain their individual partial-reading cautions.

## Remaining coverage limits

- Bounded selection of 30 additions, not complete screening of all article relevance. Annual sitemaps reveal other candidates that remain unselected.
- The 2020–2022 sitemap entries were discovered from the sitemap index but not screened in this pass.
- Only selected public previews were reviewed; no subscriber login, full-text paid article inventory or underlying institutional models were accessed.
- Search results and sitemaps can omit, rename or move material. Index membership does not prove whole-corpus completeness or stable article titles.
- No domain has been certified complete. D12 life safety and D14 facility maintenance remain especially dependent on primary practitioner material even after broader publication coverage.
- Dedicated storage and operating-system sources beyond the sampled articles, regional electrical standards, and local environmental requirements need further discovery.
- Publication-led mappings are research leads. Inclusion does not verify a claim, endorse the article's framing or require use in the course.

Prioritize primary evidence for D02 measured training/inference/RL workload profiles; D09 storage behavior, checkpoint/recovery and versioned orchestration; D12 jurisdiction-specific electrical/fire/structural/accessibility requirements; and D14 facility controls, maintenance, incident response and failure data. Networking standards, utility tariffs and interconnection rules also need edition and jurisdiction tracking.

## Next discovery pass

1. Fetch and cache publisher sitemap metadata for all years from the index; deduplicate by canonical URL and preserve title aliases.
2. Screen every indexed article against domain objectives with include, contextual, excluded and unresolved dispositions.
3. Prioritize unreviewed public primary links cited by these articles, preserving separate records for original evidence.
4. Record paywalled access limitations and leave full-text review pending unless the user provides authorized material.
5. After the first complete screening, refresh only new or changed metadata while preserving editorial notes.

A complete initial discovery inventory means every enumerated metadata record receives an explicit relevance disposition. It does not mean every relevant article has been read, that sitemaps contain all historical material, or that a domain is pedagogically complete. Keep those completion measures separate.
