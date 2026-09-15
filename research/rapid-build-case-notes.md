# Rapid construction cases — 15 September 2026

Implemented as two separate scenes in `course/prototypes/rapid-build-cases.js`, styled by `rapid-build-cases.css`. Suggested Chapter 5 placement: immediately after `colossus-service`, before `usable-land`. That sequence moves from reusing a factory to accelerating a new enclosure and assembling equipment off site, then returns to the constraints of the land itself.

Integration:

1. Import `rapidBuildScenes` into `site-scenes.js` and insert its two entries after `colossus-service`.
2. Import `renderRapidBuildCase` into `site-visuals.js` and include it in the existing renderer chain.
3. Link `rapid-build-cases.css` from `site-format.html`.
4. Keep both scene IDs stable: `meta-prometheus-tents` and `aws-houdini-prefab`.

## Sources and scope

- **Meta Engineering, 29 September 2025:** [Meta’s Infrastructure Evolution and the Advent of AI](https://engineering.fb.com/2025/09/29/data-infrastructure/metas-infrastructure-evolution-and-the-advent-of-ai/), “The Next Stage.” Direct operator confirmation that Prometheus uses weatherproof tents alongside conventional buildings and adjacent colocation. The embedded Prometheus photograph is the original image used here. Publication date is known; camera date is not stated.
- **SemiAnalysis, 29 July 2026:** [The Wild Wild West Of LEGO Datacenters](https://newsletter.semianalysis.com/p/the-wild-wild-west-of-lego-datacenters), “Purpose-Built Rapid-Deployment Shells” and “What Operators and Developers Are Modularizing Today / AWS.” This is the article recalled by the user. It distinguishes Meta’s fabric enclosures at New Albany from AWS’s Houdini factory-built data-hall skids and names Cupertino Electric as a partner. These are separate construction strategies; it does not establish an Amazon tent deployment.
- **Cupertino Electric, accessed 15 September 2026:** [Modular data centers](https://www.cei.com/core-markets/modular). Its own photo identifies the Edgerton, Wisconsin modular factory. This provides a real view of the partner’s production process, without claiming the pictured equipment belongs to AWS. The supplier describes factory integration and testing, then field installation and verification.

The scheduling explanation is the course’s inference from these workflows: enclosure or assembly savings leave civil works, utilities, interconnections and complete-system testing to coordinate. No numerical overall schedule saving is asserted. The article’s differing tent counts and narrowly scoped deployment-time claims are deliberately not used.

## Image record and checks

`course/assets/references/rapid-build-cases.provenance.json` records original URLs, attribution, scope and SHA-256 for the two unchanged publisher photographs. Both images were visually inspected. No AI image editing or browser installation was used.

The module is independent of shared player state; the two case studies introduce no buttons. Root integration and browser layout testing are still required before marking this course addition complete.
