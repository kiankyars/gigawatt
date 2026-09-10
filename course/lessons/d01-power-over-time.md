# A megawatt is not a megawatt-hour

Generated reading view. Edit [`course/expansion/foundations-power.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/foundations-power.json), lesson `d01-power-over-time`, then run `uv run gigawatt-expand`.

**D01 · Authored draft · Objectives:** D01.2, D01.3

Integrate a stepped load profile, distinguish average and peak demand, and test what interval sampling hides.

**Driving question:** How can two facilities use equal energy but need different electrical capacity?

## Read the height and the area

Power tells you how quickly energy is transferred. One watt is one joule per second; a kilowatt is one thousand watts, and a megawatt is one thousand kilowatts. Energy includes duration. One megawatt-hour is the energy transferred by a constant one-megawatt rate for one hour. The hour is multiplied by the power, not divided into it. A battery described as one megawatt-hour does not necessarily have a one-megawatt output capability.

Draw time horizontally and power vertically. The height answers how much power the system must deliver at that moment. The area under the trace answers how much energy was delivered during an interval. A rectangular segment has width measured in hours and height measured in megawatts, so its area is measured in megawatt-hours. For a stepped trace, find each rectangle's area and add them. This is the same idea used by integration, without requiring calculus.

A capacity rating is a limit or capability stated under conditions. A measured load is what equipment actually draws. If a service is rated 12 MW, the most we can say from that number alone is that a specified capacity claim exists at that boundary. We cannot conclude that the site draws 12 MW continuously, that its cooling can remove the associated heat, or that IT is installed. Even multiplying 12 MW by a year only creates an energy ceiling under the added assumption of continuous full loading.

## Calculate a day, then change its shape

Consider a synthetic 24-hour facility trace: 6 MW for eight hours, 10 MW for twelve hours, and 4 MW for four hours. The three energy blocks are 48, 120, and 16 MWh. Together they total 184 MWh. To find the average power, spread that energy evenly across the same 24 hours: 184 divided by 24 is about 7.67 MW. The maximum stated segment is still 10 MW. The average has not made a 7.67 MW connection sufficient for the original trace.

Now imagine moving flexible work so the facility consumes exactly 7.67 MW all day. The total energy remains 184 MWh in this ideal thought experiment, while peak demand falls. That illustrates why scheduling can affect infrastructure capacity even when work and energy remain unchanged. A real rescheduling change might alter cooling efficiency, queue delay, job completion time, and total energy. We held those effects fixed to isolate the shape of demand; the calculation does not promise they are absent.

Look at the headroom under a 12 MW service rating. During the 10 MW segment, the arithmetic difference is 2 MW. During the 4 MW segment it is 8 MW. Neither number is a complete admission policy for a new workload. Other equipment, redundancy requirements, and fast excursions may bind first. An arithmetic margin at a meter is useful evidence, but it is not transferable capacity everywhere downstream of that meter.

## Measurement resolution changes the question

Suppose a displayed five-minute average is 8 MW. That display could come from a constant 8 MW draw. It could also come from one minute at 12 MW followed by four minutes at 7 MW: the energy-equivalent average is (12 + 4 × 7) divided by 5, also 8 MW. These traces are indistinguishable to the average yet impose different peak demands. When investigating a disturbance, collect measurements at a timescale capable of seeing the behavior in question.

The converse mistake is turning a brief spike into a full-day energy assumption. A one-minute excursion may matter to control and protection while adding little to the daily energy total. Quantify both before deciding what to change. A storage device might smooth a short peak if its power, usable energy, controls, and connection permit it. It cannot be selected merely by comparing the daily MWh with a capacity label.

There is also an operational tradeoff. Flattening a flexible training workload may reduce peaks but postpone completion. Flattening interactive demand by making people wait changes the service being delivered. A fair comparison therefore keeps the workload deadline or latency requirement beside the power trace. If the service requirement changes, acknowledge that change instead of reporting a pure electrical improvement.

When you read an energy bill, equipment rating, or monitoring graph, name four things before calculating: the electrical boundary, the units, the duration, and whether the value is a measurement or a rating. Those four labels determine which arithmetic is meaningful. They also prevent a monthly energy total from masquerading as a transient power model, or a large planned connection from masquerading as electricity already consumed.

## Worked example: A three-level daily load

- The three constant segments cover a full day without overlap.
- All loads are measured at the same facility input.

1. First segment — 6 MW × 8 h = 48 MWh — Area equals power multiplied by time.
2. Second segment — 10 MW × 12 h = 120 MWh — A higher plateau contributes more energy per hour.
3. Third segment — 4 MW × 4 h = 16 MWh — Add the last interval, not its power alone.
4. Daily total and average — 48 + 120 + 16 = 184 MWh; 184 / 24 = 7.67 MW — Divide energy by the full duration to recover average power.

**Result:** Average demand is 7.67 MW, while the stated peak is 10 MW.

**Model boundary:** These segment averages do not establish subinterval peaks or equipment transient response.

## The tradeoff

Choice: Shift flexible work from the 10 MW interval to quieter intervals.

Benefit: The peak may fall while the same daily energy and work are preserved in the simplified model.

Cost: Jobs may finish later, and actual energy efficiency can change with scheduling and weather.

## When the situation changes

Trigger: Use a five-minute average to assess a one-minute limit violation.

Mechanism: Averaging can hide the peak that challenged the electrical system.

Response: Compare the relevant time-resolved trace with the applicable limit and measurement boundary.

## Apply the idea

A 2 MW excursion lasts 90 seconds. How much extra energy is it, and does that determine the storage output rating?

<details>
<summary>Reveal the worked answer</summary>

Extra energy is 0.05 MWh, or 50 kWh; the output power must separately support the 2 MW excursion.

Ninety seconds is 90/3,600 = 0.025 hours. Multiplying by 2 MW gives 0.05 MWh. Energy alone says nothing about whether an inverter can deliver 2 MW.

</details>

**The idea to keep:** Capacity constrains a rate; energy adds that rate across time.

## Sources and reading boundaries

- [EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) — kW and MW measure power; kWh and MWh include elapsed time. Read 2026-09-06. Read the public unit definitions. All traces, durations, averages, and practice values are original.
- [OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) — Electrical power is a rate of energy transfer. Read 2026-09-06. Read the power definition and equations; the source is not a data-center telemetry or transient specification.
