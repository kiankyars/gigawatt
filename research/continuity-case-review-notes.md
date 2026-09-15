# Chapter 7 case review

Reviewed 15 September 2026. This pass changes only the isolated quote module, its CSS, and this note. Existing continuity files, reader, catalogue, trackers, generated output, and source registry remain for the integrating agent.

## Sparks: use a load denominator, with its date and boundary

**The reviewed Crusoe and Redwood publications do not establish a current, commissioned IT nameplate or total-site load for the Sparks deployment.** Do not substitute the solar rating for either load. A historical 1 MW pilot figure is available through a published interview with a Crusoe employee, but its electrical boundary is unspecified in that transcript.

| Quantity | Supported meaning | Consequence for runtime |
| --- | --- | --- |
| 12 MW | Solar-array rating explicitly identified by Redwood and Crusoe | Not a data-center load denominator |
| 63 MWh | Published repurposed-battery storage capacity | Not established as usable AC energy at the load after reserve and conversion losses |
| 1 MW | July 2025 host-published interview describes the initial Crusoe deployment at this scale | Historical reported pilot scale; transcript does not say IT versus total load or provide a nameplate |
| 20 MW | Crusoe’s March 2026 expansion statement | Electrical boundary and commissioning status are not established; not a verified runtime denominator |
| Battery discharge MW | No separately qualified output rating found in the reviewed primary material | Power sufficiency must be established separately from stored energy |

### Primary evidence

1. [Redwood: Introduction to Redwood Energy](https://www.redwoodmaterials.com/resources/unlocking-affordable-energy-storage-at-scale-an-introduction-to-redwood-energy/), 2 April 2026, section “Proven at Scale: The Crusoe Project.” Explicitly identifies a 12 MW solar array, 63 MWh battery storage, four modular data centers, and an expansion to 24. It gives neither IT nor total-site electrical load. The earlier registry entry P169 reviewed only an indexed excerpt; this pass read the full page.

2. [Crusoe: partnership expansion](https://www.crusoe.ai/resources/newsroom/crusoe-and-redwood-materials-expand-strategic-partnership-scaling-to-7x-the-original-ai-infrastructure-density), 24 March 2026, existing P75. Cully Cavness says: “By expanding our work with Redwood Energy to 20 megawatts”. The release pairs this with an announced expansion from four to 24 modular data centers, nearly sevenfold compute capacity, and calls the prior microgrid 12 MW / 63 MWh. It does not define the 20 MW boundary as IT, total load, PV, or battery output. Do not divide 63 MWh by 20 MW as a verified site-runtime calculation, or reverse-engineer an original load from the approximate compute multiplier.

3. [Redwood: Data Center Energy Storage](https://www.redwoodmaterials.com/resources/data-center-energy-storage-solving-speed-to-power-for-ai-factories/), “Proven at Scale” section. Describes 12 MW of solar supplying multiple megawatts of modular data centers. The phrase distinguishes generation from the compute installation, but supplies no exact load denominator.

4. [Luca Pedretti: published Crusoe interview transcript](https://lucapedretti850786.substack.com/p/c0b), 27 July 2025. The host attributes this statement to Forrest Carroll, Crusoe Energy & Infrastructure Development: “This 1 MW deployment scales to 5 MW”. The [official Pexapark podcast catalogue](https://pexapark.com/podcast/) independently identifies Episode 19, the same topic, host and guest, dated 24 July 2025. The written interview is primary participant testimony, not an equipment specification. Audio was not checked; do not call this a verified verbatim audio transcript. It does not explicitly label the 1 MW as IT versus total load.

### Integration recommendation

Replace the existing 63/12 example with a clearly dated **reported 1 MW pilot-scale comparison** only if that evidence boundary is acceptable: 63 MWh / 1 MW = 63 hours = 2.625 days. Label this an ideal energy-to-reported-load ratio. If 1 MW is IT load, cooling and electrical overhead raise the battery-fed load; usable energy, initial charge, reserves and conversion losses also change duration. The relationship is `runtime = usable delivered battery energy / total battery-fed load`, subject to adequate battery output power. This is not 63 hours of measured or guaranteed autonomy.

If a verified current nameplate is required, retain the symbolic relationship and report the missing load instead. No GPU count, GPU power rating, module count, or solar rating was used to invent a load.

Discovery-only corroboration: [Latitude Media](https://www.latitudemedia.com/news/crusoe-and-redwood-materials-are-powering-a-data-center-with-old-ev-batteries/) describes a one-MW initial proof of concept; [Axios](https://www.axios.com/pro/pro-rata-premium/2025/06/27/ai-reno-vation) explicitly calls the initial installation 1 MW of IT capacity. These are secondary reports, so neither upgrades the primary evidence to a current verified nameplate.

## Microsoft quotation: separate slide after Fairwater

The complete user-supplied passage matches the two paragraphs under “High-availability, low-cost power” in [Microsoft’s Fairwater article](https://blogs.microsoft.com/blog/2025/11/12/infinite-scale-the-architecture-behind-the-azure-ai-superfactory/), by Scott Guthrie, 12 November 2025 (existing source P120). Its wording and punctuation are preserved in `microsoftPowerManagementQuote.text`; there are no omissions or paraphrases inside the quotation.

The article introduces Fairwater Atlanta and describes Fairwater design innovations. The quotation immediately follows the Atlanta-specific availability paragraph. It supports attribution as **Microsoft describing power-management solutions in the Fairwater design discussion**. It does not establish that all three measures were commissioned at Atlanta or deployed throughout the Azure fleet. The renderer uses the article title and author/date attribution without adding either claim.

The supplied phrase “without utilizing excess power” remains part of Microsoft’s quotation. It is not converted into a separate engineering claim of lossless energy storage.

Integration interface:

- Import `microsoftPowerManagementQuote` and `renderMicrosoftPowerManagementQuote` from `continuity-case-review.js`.
- Add the metadata object as a scene immediately after `tier-investment`, before `service-check`.
- For scene `power-management-quote`, call `renderMicrosoftPowerManagementQuote({ compact })`.
- Load `continuity-case-review.css` after the main continuity stylesheet. It uses the existing palette variables and scopes every selector to the new quote figure.
- Run the established deck visual checks after integration. This isolated module has not been rendered in the full slide layout.
