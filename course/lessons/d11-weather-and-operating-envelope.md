# The weather changes two constraints at once

**D11 · Authored draft · Objectives:** D11.1, D11.3, D11.5

Use an explicitly synthetic operating table to connect ambient conditions, cooling input and a fixed site power ceiling.

**Driving question:** How can hotter weather reduce usable IT capacity even before the cooler reaches its thermal limit?

## A rating is a point, not a universal capacity

A cooler cannot be described adequately by one large number on its label. The heat transfer depends on the fluid temperatures and flows, the outside air, and the operating configuration. A dry heat exchanger approaches the temperature of the air that receives its heat. An evaporative process also depends on the air’s moisture condition. Dry-bulb temperature measures ordinary air temperature; wet-bulb conditions help characterize the opportunity for evaporative cooling. Neither variable alone describes every plant.

A required coolant supply temperature establishes another part of the task. An architecture that can supply a warmer loop may have an opportunity unavailable to equipment demanding colder water. Heat exchangers add approach temperatures, and loads change return temperatures. Before claiming that a location has free cooling below a particular outdoor temperature, identify which loop, mode, exchanger and IT inlet limit are being discussed. The threshold belongs to that arrangement and operating envelope.

Performance tables make these dependencies explicit. A real table needs a source, revision, equipment configuration, load fraction, entering conditions and definition of included auxiliaries. A table without those labels can make two machines look comparable when they are answering different questions. The numbers below are deliberately invented teaching inputs. They illustrate the reasoning to apply to a validated table; they are not measurements, weather statistics or a proposed product curve.

## Two ceilings must survive the same hot hour

Consider a site with 10 MW of available electrical input. Its non-cooling overhead is 0.4 MW. In our synthetic model, cooling input equals IT heat divided by a stated plant COP; that ratio includes every cooling electrical load used in this exercise. We assume IT heat equals IT power at the modeled evaporator boundary. The site inequality is therefore PIT + PIT/COP + 0.4 ≤ 10 MW. This accounting avoids applying a yearly efficiency average to a particular hour.

In the cool condition the plant COP is eight and available thermal duty is 9 MW. In the hot condition the plant COP is four and thermal duty is 8.5 MW. At a proposed 8 MW IT load, the hot plant can remove the heat, but it consumes 2 MW doing so. The complete site then requires 10.4 MW. Thermal capacity alone says yes; the electrical balance says no. Reducing the IT load to 7.68 MW satisfies the hot electrical limit before the thermal ceiling is reached.

The result is a coupled constraint, not a penalty that can be assigned twice. First calculate feasible IT power from the electrical balance, then compare that result with available thermal duty and every other relevant ceiling. If a real performance curve changes COP with load, this simple division is no longer exact. Solve the electrical and thermal conditions together using the supplied load-dependent values rather than holding a favorable COP constant while changing its operating point.

## A useful weather model retains timing

An annual climate average hides the duration and coincidence of demanding conditions. A plant may face high ambient temperature when workloads are also heavy, or water restrictions may eliminate a mode assumed available by the energy calculation. For an estimate, divide a supplied time trace into operating bins and integrate the corresponding input. If switching, hysteresis or thermal storage matters, preserve the sequence instead of treating bins as interchangeable hours.

For a twelve-hour cool period followed by twelve hot hours, the synthetic site can sustain 8 MW IT in the cool bin and 7.68 MW in the hot bin. That is a capacity-limited dispatch assumption, not measured application demand. The resulting IT energy is 188.16 MWh; cooling uses 35.04 MWh; non-cooling overhead adds 9.6 MWh. Their sum is 232.8 MWh. The reduction in IT work cannot be quantified without a workload model.

An economizer, thermal store or higher supply temperature might alter this result. Each proposal must say which equation or constraint it changes and what additional resource it consumes. A heat-reuse customer is similarly conditional: it must accept the available temperature and heat at the required times. A receiving building that needs little summer heat does not remove the obligation to reject a summer data-center load.

## Worked example: A complete hot-hour power balance

- All values are synthetic, with constant COP within each declared bin.
- Site limit 10 MW; non-cooling overhead 0.4 MW. Cool COP 8 and thermal limit 9 MW; hot COP 4 and thermal limit 8.5 MW.
- IT power becomes the modeled cooling duty; cooling input includes all plant auxiliaries.

1. Proposed hot load — 8 + 8/4 + 0.4 = 10.4 MW — Eight megawatts fits the thermal envelope but exceeds the site electrical limit.
2. Electrical IT ceiling — PIT ≤ (10 − 0.4)/(1 + 1/4) = 7.68 MW — Rearrange the full power budget instead of subtracting a cooling load calculated at a different IT load.
3. Check thermal ceiling — min(7.68, 8.5) = 7.68 MW — The electrical budget is binding for this hot condition.

**Result:** The feasible hot-bin IT ceiling is 7.68 MW in this model.

**Model boundary:** No real climate, product curve or control stability is represented. Other site constraints may reduce the feasible load further.

## The tradeoff

Choice: Retain compressor capacity for unfavorable outdoor conditions.

Benefit: It can widen the temperature envelope in which the required cooling duty is achievable.

Cost: Its electricity, capital, maintenance and rejection duty must be included, even if it operates infrequently.

## When the situation changes

Trigger: An annual PUE is used to authorize a high-load hot-weather operating point.

Mechanism: The average conceals a higher cooling demand during the constrained hour.

Response: Reconcile time-aligned load, ambient and equipment performance, then compare feasible operating responses within validated limits.

## Apply the idea

A revised synthetic hot mode has COP 5 but only 7.5 MW thermal capacity. What now limits IT under the same 10 MW site limit and 0.4 MW overhead?

<details>
<summary>Reveal the worked answer</summary>

The electrical ceiling is 9.6/1.2 = 8 MW, but thermal capacity limits IT to 7.5 MW.

Better COP frees electrical headroom, but it does not repair the separate heat-removal ceiling. At 7.5 MW IT, site input is 7.5 + 1.5 + 0.4 = 9.4 MW. The unused 0.6 MW cannot support additional IT without increasing the thermal capability or changing the stated conditions.

</details>

**The idea to keep:** Cooling availability and cooling electricity are separate functions of operating conditions. Check both at the same load and time.

## Sources and reading boundaries

- [ASHRAE Handbook, Chapter 20: Data Centers and Telecommunication Facilities](https://handbook.ashrae.org/Handbooks/A23/SI/A23_Ch20/a23_ch20_si.aspx) — Selected discussion supports the dependence of cooling choices on environmental and system conditions. Read 2026-09-06. No equipment curve or universal economizer threshold is taken from this chapter; all operating-bin numbers are original hypothetical inputs.
- [Best Practices Guide for Energy-Efficient Data Center Design](https://www.energy.gov/cmei/femp/articles/best-practices-guide-energy-efficient-data-center-design) — The overview identifies environmental conditions, cooling and heat recovery as connected design subjects. Read 2026-09-06. Landing-page scope reviewed; no claim to have audited every linked design recommendation. Synthetic energy calculations are independent.
