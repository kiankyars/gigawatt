# Course clarification questions and answers

Compiled 18 September 2026 from the 17–18 September review conversations and the current course. Repeated questions are combined. This covers conceptual questions from Chapters 11–16; requests to move pictures, remove captions or change formatting are tracked separately in [FEEDBACK_AUDIT.md](FEEDBACK_AUDIT.md). Links use slide names because slide numbers changed during editing.

## The 30°C coolant and overheating chip — Chapter 14

### 1. How can the water still arrive at 30°C while the chip overheats?

The incoming water temperature is only one part of cooling. The water must also reach the cold plate at sufficient flow, and heat must cross the chip-to-water thermal path. Reduced flow can mean warmer water along that path and a greater thermal resistance. The chip then needs to become hotter to transfer the same heat into the water.

The course compares these two stabilized states:

| Measurement | Before | After |
|---|---:|---:|
| Water entering the row | 30°C | 30°C |
| Water flow | 100 kg/s | 50 kg/s |
| Water returning from the row | 35°C | 40°C |
| Heat carried away | 2.09 MW | 2.09 MW |
| Hottest measured chip | 70°C | 85°C |
| Assumed chip limit | 80°C | 80°C |

**Heat removal can equal heat generation at an unsafe temperature.** The after-state fails because the measured chip temperature exceeds its limit. The water balance does not calculate the 85°C chip temperature; that is another supplied measurement in the example. [Current slide](https://kiankyars.github.io/gigawatt/slides/operations.html?teach=1#heat-balance)

### 2. If half the water warms by twice as much, isn't that perfectly fine?

It can be. Half the flow and twice the temperature rise carry the same heat:

`100 × 4.18 × 5 = 50 × 4.18 × 10 = 2,090 kW`.

If all chip, coolant and equipment temperatures remain acceptable, lower flow alone is not a failure. Your objection to the original slide was correct: the heat balance alone did not establish a problem. The chip-temperature measurement supplies the missing condition.

### 3. Shouldn't we initially keep the same temperature rise and remove only half the heat?

Yes—as a simplified snapshot immediately after the flow reduction, before temperatures have adjusted. At 50 kg/s and the old 5°C rise, the water carries only 1.045 MW while the row still produces 2.09 MW. The difference accumulates as heat in the equipment and coolant, raising temperatures. The later 10°C water rise restores the full heat-removal rate, but the equipment has reached a hotter state.

The plotted transition illustrates this sequence; it does not specify a settling time or thermal mass.

### 4. Is this the same energy being removed over a longer time?

Not at the final equilibrium. Both final states remove **2.09 megajoules every second**. During the transition, less heat leaves than is generated, so some additional energy stays stored in the warmer equipment. Once removal catches up, temperature stops increasing; it does not automatically return to its earlier value.

### 5. Why do we show 30°C and 40°C at the same time? Is the row disconnected?

They are different measurement locations: **30°C enters; 40°C returns**. Upstream cooling maintains the inlet temperature. Measured nonzero flow rules out a completely disconnected branch, but does not identify what reduced the flow. The example establishes a local cooling problem, not a particular faulty valve or pump.

## Heat transfer and coolant equipment — Chapter 11

### 6. What are heat rate and sensible heat? What does the equation mean?

Heat rate is energy transferred per second, measured in watts. Sensible heating changes temperature without a phase change: here, water becomes warmer while remaining liquid.

`Heat rate = mass flow × specific heat capacity × water temperature rise`

or `Q̇ = ṁ cp ΔT`.

The steady-flow sensible-heat balance describes how a flowing liquid carries heat without continued heat accumulation inside the component. It is the relevant heat-balance equation here, rather than a formula for every heat-transfer mechanism.

### 7. What are heat flux and thermal resistance?

**Heat flux** is heat rate per unit area. A 400 W chip over 4 cm² gives 100 W/cm²; the same power over 1 cm² gives 400 W/cm². The total heat is unchanged, but more concentrated.

**Thermal resistance** is the temperature difference required per watt through a specified path, in °C/W:

`Tchip − Tcoolant = heat rate × thermal resistance`.

Area, materials, contact quality, cold-plate design and flow affect that path. Heat flux alone does not determine chip temperature.

### 8. Should the 400 W calculation say ΔT? Is it a temperature decrease?

Yes, it should say **ΔT = 400 W × thermal resistance**. It is the temperature difference between the chip and local coolant, not a decrease over time. Add coolant temperature to obtain chip temperature. With 35°C coolant, the course's two thermal resistances give 35 + 32 = 67°C and 35 + 48 = 83°C. [Current slide](https://kiankyars.github.io/gigawatt/slides/cooling.html?teach=1#device-temperature)

### 9. Are CRAH, CDU and chiller different devices? Is CoolIT's 2 MW unit a compressor?

| Device | Function |
|---|---|
| CRAH: computer room air handler | Fans pass room air over a chilled-water coil. |
| Liquid-to-liquid CDU: coolant distribution unit | Pumps and regulates rack coolant; an exchanger transfers heat into separate facility water. |
| Chiller | Uses refrigeration, including a compressor, to cool a liquid. |

The **CoolIT CHx2000 is a CDU**, not a refrigeration compressor. Its listed 2 MW at 5°C approach is a heat-transfer rating. Its 2,125 L/min at 35 psi is a separately specified hydraulic point. [Manufacturer](https://www.coolitsystems.com/cdu-product/chx2000/)

### 10. Can a liquid-cooled rack still need air cooling? Is air cooling actually dead?

Yes, a liquid-cooled rack can still release heat from components outside the cold plates into air. That air heat needs a path out: a rear-door exchanger, room-air equipment or another suitable arrangement. The provocative opening title does not mean air cooling has disappeared from data centers. [GB300 cooling example](https://lenovopress.lenovo.com/lp2357-lenovo-nvidia-gb300-nvl72-rack-scale-ai#cooling)

### 11. Is the GB300 rear-manifold diagram a rear-door heat exchanger? Is it facility water or technology coolant?

The NVIDIA rear view shows **manifolds and connections feeding cold plates**. It is not itself a rear-door exhaust-air coil. In the liquid-to-liquid CDU arrangement, technology coolant runs between the CDU and cold plates; facility water stays on the other side of the exchanger.

An RDHX is a separate air-to-liquid heat exchanger. Depending on the design, it can receive suitable facility water or a separately conditioned loop. It does not universally require exactly the same plumbing as the cold plates.

### 12. If an RDHX catches the remaining heat, is the room-air capacity example still relevant?

Only for heat that escapes capture. If cold plates collect 85 kW of a 100 kW rack's heat, 15 kW remains in air. A suitable RDHX can transfer that remaining 15 kW into liquid, freeing the corresponding room-air cooling capacity. The heat still has to leave the site.

### 13. Did we establish that Abilene has no CRAHs?

No campus-wide absence claim was established. Crusoe documents recirculating facility water and air-cooled chillers; that does not identify every residual-air cooling device in every hall. The CRAH/CDU comparison is a generic arrangement, not an Abilene floor plan. The pasted explanation did not supply sufficient evidence to establish its stronger claims. [Crusoe's design description](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)

### 14. What distinguishes single-phase from two-phase immersion?

In single-phase immersion, the electrically insulating liquid remains liquid and carries heat to an exchanger. In two-phase immersion, it boils at the hot hardware, condenses at a cooled surface and returns to the bath. These terms describe the coolant's phase behavior, not the number of water loops.

## Pump pressure, flow and approach — Chapters 11 and 13

### 15. Is the pump chart used in industry? What determines the operating point?

Yes. The pump curve shows the pressure difference a pump can supply at different flows at a fixed speed. The circuit curve shows the pressure difference required to move those flows through the circuit. Their **intersection determines steady flow**. The course's numbers illustrate this standard method; they are not a named CDU's measured curve. [KSB operating point](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/operating-point-1117036)

### 16. Why is there another rising line?

It is an alternative circuit with more resistance—for example, a partly closed valve. It intersects the same pump curve at a lower flow. The current example moves from 2 L/s at 120 kPa to about 1.41 L/s at 140 kPa. One pump curve plus two alternative circuit curves demonstrates both how flow is selected and how a restriction changes it.

### 17. Why does the circuit require more pressure at higher flow? Why call it a pressure drop?

Faster flow through unchanged pipes, fittings and cold plates produces greater frictional losses. In the turbulent-flow approximation used in the example, `Δp ∝ flow²`: twice the flow requires approximately four times the pressure difference. The pump provides a pressure **rise**; the circuit consumes it as a pressure **drop**. They describe opposite sides of the same circulation requirement. [KSB system curve](https://www.ksb.com/en-global/centrifugal-pump-lexicon/article/system-characteristic-curve-1116274)

### 18. Does 80 kPa at the CDU need to become 20 kPa at the rack?

No. **20 kPa is the inlet-to-outlet pressure difference needed across the branch at the original flow; 80 kPa is the difference needed at double flow.** They are two operating cases, not two absolute pressures at different locations. A 60 kPa available differential would be insufficient for the second case.

### 19. What was the “myth”? Isn't faster fluid at lower pressure?

The misleading generalization was “faster flow always means lower pressure.” On the fixed-speed pump curve, more flow typically corresponds to less pressure rise available. Through a fixed resistant circuit, more flow requires a larger pressure difference. A local velocity/static-pressure relationship does not replace this pump-and-circuit balance. “Concrete myth” was not the name of a separate course concept.

### 20. What is approach temperature, and is lower better?

At the CDU, the illustrated approach is **rack-coolant supply minus incoming facility-water temperature**: 35 − 30 = 5°C. It differs from one fluid's supply-to-return rise. A smaller approach lets the rack coolant get closer to the facility-water temperature. That is thermally useful, although achieving it can require a larger exchanger or different flows and costs. A 5°C temperature difference is also 5 K.

### 21. Does cooling have redundancy? Can computing slow down after a failure?

Yes. Spare pumps/CDUs and independent cooling paths can protect against different failures. An extra CDU does not fix a shared failed pipe or common power source. If available cooling falls, suitable controls can reduce power, move work or stop it. The response must be supported and tested; automatic chip throttling is not proof that every loss-of-cooling event can be handled indefinitely. [Course example](https://kiankyars.github.io/gigawatt/slides/cooling.html?teach=1#lost-flow)

## Outdoor heat rejection — Chapter 12

### 22. Are dry bulb/wet bulb the same thing as dry cooling/wet cooling?

No. **Dry bulb** is ordinary air temperature. **Wet bulb** is the temperature of a wetted, ventilated sensor cooled by evaporation; it is lower in unsaturated air and equal at saturation. These are air measurements. A dry cooler approaches dry-bulb temperature; evaporative equipment can exploit the lower wet bulb. [National Weather Service](https://www.weather.gov/source/zhu/ZHU_Training_Page/definitions/dry_wet_bulb_definition/dry_wet_bulb.html)

### 23. How does water evaporate in a cooling tower? Through perforated pipes?

In the open tower shown, nozzles or a distribution deck spread water over fill, creating films and droplets. Moving air contacts that exposed water; some evaporates, cooling the remainder, which collects and recirculates. Evaporation is not happening through holes in a sealed coil.

Evaporation leaves minerals behind. **Blowdown** removes concentrated water. **Makeup water** replaces losses; “makeup” describes its purpose, not whether it is drinking water or treated wastewater. [DOE cooling-tower guide](https://www.energy.gov/cmei/femp/best-management-practice-10-cooling-tower-management)

### 24. Is adiabatic assist just another cooling tower?

Both exploit evaporation, but in the illustrated adiabatic cooler, wetted pads cool the **incoming air before it reaches a sealed coolant coil**. The process coolant stays inside the coil. In the open tower, the circulating tower water itself contacts air. Adiabatic assistance can improve dry cooling without opening the process loop, but consumes water while active. [Manufacturer example](https://www.evapco.com/products/closed-circuit-coolers-air-cooled/eaw-da-double-stack-adiabatic-cooler?page=1)

### 25. Does “45°C exceeds the 35°C limit” mean the chips must be at 35°C?

No. The example stipulates a maximum **rack-coolant inlet** of 35°C. The dry route gives 35°C outdoor air + 5°C cooler approach + 5°C CDU approach = 45°C coolant entering the rack. That misses the coolant requirement. Chip temperature is a separate, higher temperature. [Current dry-cooler slide](https://kiankyars.github.io/gigawatt/slides/heat-rejection.html?teach=1#approach-outdoors)

### 26. Can a closed rack loop use a wet tower? Could open tower water go all the way to the CDU?

Yes, a closed rack loop can transfer heat through exchangers into a separate open tower loop. “Closed loop” applies to a particular circuit, not automatically the entire facility.

Direct tower-water service to a suitable CDU or exchanger is possible if its materials, filtration, treatment and water-quality requirements permit. It cannot be assumed interchangeable with a clean closed facility-water loop. A chiller's sealed refrigerant circuit is separate again. The course's direct dry/wet comparison does not contain refrigeration.

### 27. Which slide had the “continuity mistake”?

It was the **closed-loop water slide**—formerly Chapter 12 slide 14, then slide 9, now slide 10. After being moved, it unexpectedly switched to an air-cooled arrangement and introduced a chiller, breaking the narrative from the preceding wet-tower diagram. It now starts with the wet-tower route and preserves that direct heat-exchanger arrangement. “Continuity” meant narrative consistency here. [Current slide](https://kiankyars.github.io/gigawatt/slides/heat-rejection.html?teach=1#closed-loop-water)

### 28. How can the chiller release more heat than it collected?

The compressor consumes electricity that also becomes heat. **10 MW collected from the load + 2 MW of compressor electricity = 12 MW rejected at the condenser.** Pumps and fans are outside that particular balance. No energy is being created.

### 29. Without a chiller, would we remove less than the 10 MW?

Not necessarily. Direct outdoor cooling can remove the whole 10 MW when outdoor conditions, temperature differences and equipment capacity permit. Refrigeration is needed when direct cooling cannot meet the required coolant temperature or duty. Without the compressor, its extra 2 MW is also absent.

### 30. Are we assuming COP 8 when cool and COP 4 when hot?

Yes, in that example. `COP = cooling heat removed / cooling electricity`. Removing 8 MW needs 1 MW electricity at COP 8 and 2 MW at COP 4. Those are teaching operating points, not a universal weather rule. Higher outdoor temperatures generally increase compressor work in an air-cooled chiller. Economizer operation can bypass the compressor when conditions permit; pumps and fans still need power. [Trane](https://www.trane.com/commercial/north-america/canada/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html)

### 31. Does the heat-reuse slide say the data center runs only six hours?

No. It produces 4 MW of heat all day. The **neighboring heat customer** needs 2 MW for six hours, or is closed that day. The customer's schedule changes; the data center's does not. Heat without a customer still needs an outdoor rejection path.

### 32. Is dry cooling dependent only on electricity, and wet cooling on water too?

For the operating-resource comparison, yes: non-evaporative dry rejection needs electricity; wet towers also need continuing makeup water. Adiabatic assistance consumes water when used. Initial filling, maintenance and the dependence of cooling performance on weather are separate considerations.

## Delivery and commissioning — Chapter 13

### 33. Is EPC the proper name? What is prefabrication achieving?

EPC means **engineering, procurement and construction**. Commissioning is an activity, not the expansion of the letter C. Prefabrication assembles and tests equipment in a factory while site construction proceeds, moving work and troubleshooting earlier. It is a delivery strategy within the project, not a replacement for EPC.

### 34. Does factory testing simply shorten on-site acceptance testing?

That is the central benefit being taught. Internal wiring, piping and control logic can be checked before shipment. Field connections, interactions with installed equipment and integrated responses still need on-site tests. We do not claim a universal number of weeks saved.

### 35. What did “accepted path” or “accepted system” mean?

It meant a complete, tested combination of **power, cooling and networking serving the same racks**, rather than unrelated totals elsewhere on the site. “Accepted” referred to commissioning against agreed requirements. It was not a special kind of wire or a billing unit, and the vague phrase was poor teaching language.

### 36. Is the new-phase example the first 50 MW in October and another 50 MW in November?

Yes. Applied Digital delivered phases of Polaris Forge 1 in Ellendale for CoreWeave: [50 MW on 27 October 2025](https://ir.applieddigital.com/news-events/press-releases/detail/133/applied-digital-achieves-ready-for-service-for-phase-1-at), followed by [another 50 MW on 24 November](https://ir.applieddigital.com/news-events/press-releases/detail/137/applied-digital-completes-phase-ii-ready-for-service-at). The design lesson is connecting the next phase while keeping the first operating. The announcements establish the milestones, not a published switching topology. The pictures came from an investor presentation, which explained their earlier screenshot-like framing.

## Controls and operating incidents — Chapter 14

### 37. What are the three control layers? Which does the next example emphasize?

Local equipment controls hold quantities such as pump pressure or flow. Plant controls start, stop and coordinate cooling equipment. Workload scheduling decides when and where computing runs. The example about starting more cooling before admitting another job emphasizes **plant controls coordinating with the scheduler**.

### 38. Was Google's AI cooling system giving advice or controlling equipment?

The 2016 version advised operators. The 2018 system directly controlled cooling under human supervision and with an override. The four stages are sensor readings → predicted outcomes → constrained action selection → independent local checks and action. Its performance graph concerns cooling energy per unit of cooling, not the same percentage reduction in all facility electricity. [Google DeepMind](https://deepmind.google/blog/safety-first-ai-for-autonomous-data-centre-cooling-and-industrial-control/)

### 39. Is the 1 MW buffer real? How do operators choose cooling reserve?

The slide's **1 MW headroom and three-minute startup are assumptions**. There is no universal 1 MW or fixed-percentage rule. Margin depends on credible load changes, equipment startup time, local coolant delivery, weather and required failure tolerance.

Three different protections matter: spare heat-removal capacity in MW, redundancy after a failure, and stored thermal energy that buys time. A manufacturer's staging sequence uses 80% or 90% loading thresholds for specified chiller configurations; these are control thresholds, not a universal data-center reserve. [Johnson Controls](https://docs.johnsoncontrols.com/bas/r/Metasys/en-US/Chilled-Water-Plant-for-Guideline-36-Application-Note/1.0/Chiller-sequence-of-operations/Chiller-and-waterside-economizer-staging-determination-5.20.1-15/Stage-Up-Part-Load-Ratio-SPLRUP)

For a concrete thermal-storage example, Intel described two 24,000-US-gallon chilled-water tanks designed for twelve minutes of cooling, with pumps and fans on backed-up power. [Intel report](https://www.intel.com/content/dam/doc/white-paper/intel-it-thermal-storage-system-provides-emergency-data-center-cooling-paper.pdf)

### 40. Is Google actually postponing jobs, or was that invented?

Google documented demand response that shifts eligible nonurgent work, including YouTube processing and Google Translate updates, while maintaining live services. The course's 4 MW job, three hours of work and specific timetable are an illustration, not Google's disclosed measurements. Shifting the illustrated job changes demand during the event without changing its 12 MWh of work energy. [Google's account](https://cloud.google.com/blog/products/infrastructure/using-demand-response-to-reduce-data-center-power-consumption)

### 41. What was Cloudflare's single point of failure? What do dashboard, API and analytics mean?

The dashboard is the customer management interface; the API lets software perform management tasks; analytics supplies usage and traffic information. Their service design spanned sites, but necessary Kafka/ClickHouse dependencies remained at one Portland facility. Losing that facility therefore disabled services that appeared distributed. Earlier tests had not removed the entire facility and its dependencies. The lesson is testing the actual scope of a failure. [Cloudflare's report](https://blog.cloudflare.com/post-mortem-on-cloudflare-control-plane-and-analytics-outage/)

### 42. Was Gmail's problem that a broken replica reinfected a repaired copy?

That was not the documented account. A software update affected several live copies; an earlier offline tape backup preserved data. The lesson concerns correlated software failures across replicas versus an independent recovery copy. It is useful storage context, but we moved it out of the main operations presentation. [Google's account](https://gmail.googleblog.com/2011/02/gmail-back-soon-for-everyone.html)

### 43. Did Google supply London incident pictures? Why did recovery take longer than cooling repairs?

The cited final incident report supplied a timeline and explanation, not incident photographs. It describes extreme heat combined with failures of redundant cooling. Repairing cooling made restart possible; sequencing services and reconciling system state took longer. The report identifies another 14 hours 15 minutes from cooling repair to initial service restoration. The quotation is now [in the published deck](https://kiankyars.github.io/gigawatt/slides/operations.html?teach=1#london-cooling-quote). [Google report](https://status.cloud.google.com/incidents/fmEL9i2fArADKawkZAa2)

### 44. What is the point of Meta's maintenance groups and cost curve?

Taking a larger group offline removes more capacity at once; making groups very small creates more maintenance interruptions. The curve illustrates the trade-off. It does not supply a universal optimum group size. [Meta's original diagrams](https://engineering.fb.com/2024/06/12/production-engineering/maintaining-large-scale-ai-capacity-meta/)

### 45. Does the final operations knowledge check actually have an answer?

Yes: **the healthy Row C cannot take another 2.50 MW at its current flow**. It has 2.09 MW of local water-side headroom, despite 3 MW spare at the central plant and electrical supply. The proposed total 4.59 MW requires about 110 kg/s for the specified 30°C inlet and 40°C maximum return. More proven local flow or placing some work elsewhere resolves that water-balance constraint. This replaces the earlier exercise whose chips were already too hot. [Current question and explanation](https://kiankyars.github.io/gigawatt/slides/operations.html?teach=1#operating-decision)

## GPU economics and the finale — Chapters 15–16

### 46. Does bare metal mean there is no managed software?

No. Bare metal describes physical hardware access without a hypervisor layer. Managed describes who operates software. Kubernetes, Slurm or an inference service can be managed on bare-metal machines. CoreWeave explicitly runs Kubernetes directly on bare metal. [CoreWeave](https://www.coreweave.com/products/bare-metal)

### 47. What does Spot mean? Why offer one-, three- or five-year contracts?

Spot refers to short-term capacity at the current price. Cloud Spot products such as AWS's also permit the provider to reclaim capacity; a short-term price quote alone does not establish that contractual right. AWS adjusts its Spot prices gradually, so “instantaneous price” is too strong. [AWS](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-spot-instances.html)

Longer commitments give the provider more predictable revenue and the customer capacity assurance, often in exchange for different pricing or payment terms. Shorter exposure permits repricing but risks vacancies. Longer does not automatically mean a lower quote for every product and market. We did not find a publicly accessible, matched one-/three-/five-year series to reproduce, so did not invent one. [SemiAnalysis index](https://gpu-index.semianalysis.com/)

### 48. Is a cloud provider paid per training result? What did the lab's “internal cost” mean?

GPU-capacity agreements can charge for reserved capacity or GPU-hours; model APIs can charge for tokens. A lab can separately calculate its internal cost per training run or token. That internal accounting may include the cloud invoice, labor and other allocated costs. It does not imply the infrastructure provider invoices each successful training result, and “internal cost” did not mean only salaries. [CoreWeave product examples](https://www.coreweave.com/products/dedicated-inference)

### 49. What is electricity cost pass-through? Does a price rise reduce profitability?

Pass-through means the contract lets the provider charge the specified electricity expense to the customer. With a fixed all-in rental price, an unhedged electricity-price rise instead squeezes the provider's margin. The outcome depends on the agreement and hedging, rather than every electricity increase having the same effect on every data center.

### 50. Are unrented GPUs switched off? Is billable occupancy the same as utilization?

Not necessarily. Unrented hardware can remain powered at idle; operators choose their power policy. Paid hardware can also be temporarily idle, so rented hours are not the same as GPU compute utilization.

The corrected example includes both: 80 rented hours at a 1 kW site-power allocation, plus 20 unrented hours at 0.2 kW, consume 84 kWh. Dividing by 80 paid hours gives **1.05 kWh per billed GPU-hour**. These powers are teaching assumptions, including allocated site overhead, rather than a GPU specification. [Current example](https://kiankyars.github.io/gigawatt/slides/capacity.html?teach=1#gpu-hour-cost)

### 51. What does NVIDIA's backstop cover?

The discussed arrangements support revenue by committing to purchase specified cloud capacity under contractual conditions. They are not unconditional guarantees of every provider's debts or profits. They can improve financing confidence while leaving delivery and operating risks. CoreWeave's initial $6.3 billion agreement and NVIDIA's later aggregate program disclosures describe different scopes and dates. [CoreWeave filing](https://www.sec.gov/Archives/edgar/data/1769628/000176962825000047/crwv-20250909.htm), [NVIDIA filing](https://www.sec.gov/Archives/edgar/data/1045810/000104581026000075/nvda-20260726.htm)

### 52. Does hot weather mean the installed GPU inventory shrinks?

No. It can reduce the IT load that the cooling and electrical systems can sustainably support, or increase cooling electricity at the same IT load. The hardware remains installed. The underlying distinction remains in Chapter 12. The finale’s separate hot-weather comparison was removed during the latest review because it repeated that lesson.

### 53. What is Chapter 16's purpose now? Which chapters are approved?

The former finale contained five separate engineering exercises. We agreed those repeated earlier material without providing a satisfying conclusion. The replacement follows **one real AI factory—Abilene—to connect workload, power, cooling, construction, financing and expansion**. The useful earlier exercises remain optional reading. [Abilene finale](https://kiankyars.github.io/gigawatt/slides/integrated-cases.html?teach=1#abilene-factory)

Your approval covers the reviewed material in Chapters **1–13**. The subsequently authorized power triangle in Chapter 6, Clemente/VRM additions in Chapter 8 and Toronto additions in Chapter 12 await your review; unchanged material remains accepted. Chapters **14–16** remain awaiting your acceptance. The persistent record is [COURSE_REVIEW.md](COURSE_REVIEW.md).

### 54. Have we taught the power triangle?

Yes. Following your authorization, **Chapter 6 slide 24** now draws the triangle immediately after the beer analogy: **900 kW real power**, **675 kvar reactive power**, **1,125 kVA apparent power**, and **PF = 0.8**. This corrects the impression that real and reactive power add arithmetically. The example assumes sinusoidal waveforms; harmonic distortion can also reduce true power factor. [Slide](https://kiankyars.github.io/gigawatt/slides/distribution.html?teach=1#power-triangle) · [Schneider explanation](https://www.electrical-installation.org/enwiki/Definition_of_reactive_power)

### 55. Is the hyperscaler at Abilene Crusoe, Oracle or OpenAI?

**Oracle.** Crusoe builds and operates the physical campus; Oracle supplies GPU cloud capacity; OpenAI runs training and inference on it. Campus financing involves Crusoe, Blue Owl and Primary Digital. The slide now names these roles instead of leaving “hyperscaler” unexplained. Crusoe explicitly calls Abilene purpose built for Oracle in its [June 2026 announcement](https://www.crusoe.ai/resources/newsroom/crusoes-contracted-ai-infrastructure-capacity-approaches-5-gigawatts-across-data-centers-and-cloud).

### 56. Why accept higher cooling costs in water-constrained Texas?

Crusoe says it chose the non-evaporative design to conserve water. Its discussion contrasts that choice with evaporative towers, but publishes no quantified comparison or water-price assumptions. We should not pretend to know its cost model. [Crusoe](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)

A wet tower can reduce compressor electricity by enabling lower condensing temperatures, but needs makeup water, treatment and tower upkeep. Air-cooled chillers avoid that evaporative demand and tower maintenance, while often using more compressor electricity. Future water prices and supply restrictions could make the air-cooled choice more attractive financially; the published evidence does not establish the lifetime winner. **Air-cooled does not universally mean higher maintenance.** [Trane comparison](https://www.trane.com/commercial/north-america/canada/en/about-us/newsroom/blogs/air-vs-water-cooled-chillers.html)

### 57. What do Blue Owl and Primary Digital get from Abilene?

Their involvement concerns the **physical data-center project**. Blue Owl-managed funds supply institutional capital. Primary Digital helps sponsor and structure the deal; the first-phase legal announcement also identifies its facilitating/advisory role. The commercial attraction is a facility backed by a long-term tenant lease: rental cash flow and property value support investment returns. Crusoe contributes development and operating capability while recycling capital into further projects. The announcements do not disclose each party's ownership share, cash contribution, fees or target return. [Crusoe](https://www.crusoe.ai/resources/newsroom/crusoe-blue-owl-capital-primary-digital-joint-venture) · [Kirkland transaction account](https://www.kirkland.com/news/press-release/2025/01/kirkland-ellis-advises-bo-funds-on-jv-and-financing-for-development-of-adc)

### 58. Does the cooling claim establish greenwashing?

The finale poses this as a discussion question. The design avoids evaporative water consumption, but Crusoe's article does not supply enough cost information to assess its claimed financial sacrifice. Water savings and commercial benefits can coexist. On-site gas creates a separate emissions question; it does not itself make the water-saving claim false. [Crusoe’s stated rationale](https://www.crusoe.ai/resources/blog/an-inside-look-at-the-abilene-ai-data-center)
