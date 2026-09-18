# Abilene finale: claim ledger

Reviewed against live primary sources on September 18, 2026. Scope is the original Crusoe-built Oracle/OpenAI Abilene campus, not the adjacent Microsoft development. This note supports Chapter 16's connected synthesis rather than a reconstruction of confidential as-built details.

## Customer, equipment and phases

- [OpenAI, July 22, 2025](https://openai.com/index/stargate-advances-with-partnership-with-oracle/): Oracle started delivering GB200 racks in June 2025; OpenAI had begun early training and inference at Abilene by the July announcement.
- [Crusoe, September 30, 2025](https://www.crusoe.ai/resources/newsroom/crusoe-announces-flagship-abilene-data-center-is-live): construction began June 2024; the first two buildings were energized within a year; first phase running on OCI. The planned eight-building campus supports an integrated network fabric.
- [Crusoe, March 18, 2025](https://www.crusoe.ai/resources/newsroom/crusoe-expands-ai-data-center-campus-in-abilene-to-1-2-gigawatts): initial two buildings and 200+ MW; six-building expansion; eight buildings and 1.2 GW total plan. The release's wording about 50,000 GB200 NVL72s per building confuses racks with GPUs and is not suitable for quantitative teaching.
- [Oracle, current data-center locations](https://www.oracle.com/data-centers/): Abilene section says 75% of total capacity delivered as of September 2026, with remaining delivery in subsequent quarters. Capacity basis is not defined. Do not turn this into a claimed 900 MW operating load.

## Power and cooling choices

- [Crusoe 2025 Impact Report](https://media.ffycdn.net/us/crusoe/PL5TuZz5apXB9pVsd3H1.pdf), printed page 16: 350 MW onsite gas plant with long-term backup role. Printed page 19 explicitly describes Abilene's temporary gas bridge power. It does not establish that the 350 MW plant backs up all 1.2 GW. Report downloaded and text extracted directly for this review.
- [Energy Transfer, February 17, 2026, page 1](https://ir.energytransfer.com/node/52241/pdf): natural-gas deliveries to Oracle near Abilene began January 2026. The reported roughly 900 MMcf/day is aggregated across three Oracle projects, not Abilene alone.
- [Crusoe, August 5, 2025](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center): facility water recirculates in a closed loop and air-cooled chillers reject heat. The company says it chose higher lifecycle and maintenance expenditure to conserve water. It estimates approximately 50,000 gallons per building annually for maintenance and water quality, separate from initial fill; therefore no evaporation for heat rejection does not mean zero site water use.
- [Trane, Air vs. Water Cooled Chillers](https://www.trane.com/commercial/north-america/canada/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html), October 2019, Energy efficiency paragraph: ambient dry-bulb determines air-cooled refrigerant condensing temperature; reduced condensing temperature/pressure reduces compressor work. This supports the general hot-weather mechanism at fixed cooling duty and setpoints, not measured Abilene power, COP, capacity loss, or a particular equipment selection.
- [Crusoe, July 18, 2024](https://www.crusoe.ai/resources/newsroom/crusoe-200mw-ai-data-center): early design announcement supports direct-to-chip or rear-door heat exchangers with air-cooling flexibility. This does not establish a commissioned residual-air arrangement or prove the complete absence of CRAHs.

## Delivery and financing

- Impact Report page 16 describes Abilene's in-house electrical equipment and switchgear, factory fabrication and prefabricated electrical skids. These practices connect equipment procurement to phase delivery without inventing a saved-weeks calculation.
- [Crusoe, October 15, 2024](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture): first-phase $3.4B venture, 206 MW, two buildings, fully leased long-term to an unnamed Fortune 100 hyperscaler. It describes a funded forward takeout; it does not disclose a GPU purchase total or the tenant's cloud contract economics.
- [Crusoe, May 21, 2025](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-and-primary-digital-infrastructure-enter-joint-venture): second phase of a $15B joint venture involving Crusoe, Blue Owl funds and Primary Digital Infrastructure, funding expansion to eight buildings. $15B is not a stated GPU bill, pure debt principal or incremental amount to add to the earlier $3.4B.

## Visuals

Original Oracle imagery and a full-resolution frame from its Abilene media kit are recorded in [finale-abilene-provenance.json](../course/assets/references/finale-abilene-provenance.json). The 3840×2160 rack-aisle frame with coolant hoses is suitable for a large image. The frame does not establish exact hardware models or loop topology by inspection alone.

## Exclusions

No actual Abilene tariff, revenue, utilization, measured PUE, thermal derating curve, tokens per second, detailed redundancy arrangement or proprietary electrical single-line was established. A synthesis diagram may connect functional systems but should not purport to be a construction drawing. No adjacent Microsoft-campus capacity or gas-development figures should be merged into this story.
