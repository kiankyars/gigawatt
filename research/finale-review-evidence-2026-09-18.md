# Chapter 16 review: equipment, cooling cost and capital

Primary sources checked September 18, 2026. Scope: the original Oracle/OpenAI Abilene campus, not the adjacent Microsoft project.

## Air-cooled chillers: what the maintenance claim actually says

[Crusoe's August 5, 2025 inside look](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center) explicitly describes increased lifecycle and maintenance costs for its closed-loop, non-evaporative system at this scale. Crusoe says it accepted the additional expense to conserve water. The source does not quantify the costs, identify a tendered alternative, or establish a general rule for every air-cooled chiller.

The user's general intuition is supported by [Trane's air/water chiller comparison](https://www.trane.com/commercial/north-america/canada/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html): air-cooled systems avoid cooling-tower water treatment, tower maintenance, and associated equipment; Trane lists lower maintenance as a general advantage. Water-cooled systems can have lower compressor energy use and greater unit capacity. Actual campus lifecycle expense depends on the complete installation.

Recommended slide treatment: **Conserve water; accept higher overall cost.** Keep the maintenance distinction in presenter notes. Do not teach that air-cooled chillers inherently have higher maintenance costs, and do not assert the opposite for Abilene's particular system without its cost data.

## Who finances, builds, operates, leases and uses the campus

- [Crusoe's October 15, 2024 financing announcement](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) describes a fully funded forward takeout, with Blue Owl-managed funds and Primary Digital Infrastructure jointly sponsoring the initial 206 MW project. Crusoe designs, builds and operates the data center. The project is long-term leased to a hyperscale tenant; the original announcement did not name the tenant.
- [May 21, 2025 expansion announcement](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture) describes Crusoe, Blue Owl-managed funds and Primary Digital Infrastructure jointly sponsoring the six additional buildings within a $15 billion venture. This is project financing, not a GPU bill or a measure of profit.
- [Crusoe's September 30, 2025 live-campus announcement](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live) identifies the long-term Oracle collaboration and operation on Oracle Cloud Infrastructure. [OpenAI's July 22, 2025 announcement](https://openai.com/index/stargate-advances-with-partnership-with-oracle/) identifies OpenAI's early training and inference workloads and Oracle's delivery of GB200 racks.

Teach the roles as **capital partners + Crusoe development/operations → Oracle cloud infrastructure → OpenAI workloads**. Do not say Crusoe merely leases the building from someone else to avoid all building liability: neither that description nor the claimed liability purpose is established by these sources. Capital recycling is supported by the original financing announcement; total removal of contractual or operating responsibility is not.

## A concrete manufacturing connection to Abilene

A fresh [Crusoe announcement dated September 14, 2026](https://www.crusoe.ai/resources/newsroom/crusoe-opens-second-tulsa-factory-ai-infrastructure) says its Tulsa operations supplied **more than 2,500 switchboards** to the flagship Abilene Stargate site. It lists medium-voltage switchgear, low-voltage switchboards, electrical enclosures, industrial controls and copper busbar among the factories' products. The 2,500 figure refers to switchboards, not every listed product type and not 2,500 complete electrical rooms.

The [2025 Impact Report](https://media.ffycdn.net/us/crusoe/PL5TuZz5apXB9pVsd3H1.pdf), printed page 16, independently ties Abilene to in-house switchgear manufacture and prefabricated electrical skids. Page 10 covers the manufacturing arm. The report was downloaded, its text extracted, and both pages visually inspected. No report screenshot is used in the slides.

## Photographs ready for the course

| Asset | What it shows | Suitable caption |
| --- | --- | --- |
| `course/assets/references/finale-review-abilene-construction.jpg` | Genuine Oracle media-kit aerial: built roofs, exposed structural frames, ongoing roads and equipment work at Abilene | Abilene campus under construction · Oracle |
| `course/assets/references/finale-review-tulsa-assembly.webp` | Genuine Crusoe photograph of assembly cells at its second Tulsa manufacturing facility, published September 14, 2026 | Crusoe's Tulsa assembly floor · September 2026 |

The assembly photo is a documented example of Crusoe's production process. The pictured individual enclosures are not specifically identified as the units shipped to Abilene, and the newly opened factory must not be presented as the factory that completed the first 2025 buildings. Pair its caption with the separately sourced cumulative Tulsa delivery figure. Both photographs are publisher originals downloaded unchanged; details and hashes are in `course/assets/references/finale-review-provenance.json`.

## Follow-up review: named customer and limits of the cost comparison

[Crusoe, June 9, 2026](https://www.crusoe.ai/resources/newsroom/crusoes-contracted-ai-infrastructure-capacity-approaches-5-gigawatts-across-data-centers-and-cloud) explicitly identifies the 1.2 GW Abilene campus as purpose built for Oracle among its projects contracted to hyperscale clients. This resolves the teaching identity: Oracle is the hyperscaler, Crusoe develops and operates the campus, and OpenAI uses Oracle compute. It does not disclose an exact legal lease entity or contract term.

The cooling article's comparison with evaporative towers is contextual, not a published project cost model. It supplies no priced alternative, cost breakdown, water tariff or forecast. The slide therefore attributes Crusoe's water-management priority through a short quotation and removes the generic “higher overall cost” bar and repeated plumbing diagram. All three preceding cooling options remain unselected.
