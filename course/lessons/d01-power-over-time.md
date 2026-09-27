# A megawatt is not a megawatt-hour

**2. Data center overview**

Integrate a stepped load profile, distinguish average and peak demand, and test what interval sampling hides.

**Driving question:** How can two facilities use equal energy but need different electrical capacity?

## Read the height and the area

Power tells you how quickly energy is transferred. One watt is one joule per second; a kilowatt is one thousand watts, and a megawatt is one thousand kilowatts. Energy includes duration. One megawatt-hour is the energy transferred by a constant one-megawatt rate for one hour. The hour is multiplied by the power, not divided into it. A battery described as one megawatt-hour does not necessarily have a one-megawatt output capability.

Draw time horizontally and power vertically. The height answers how much power the system must deliver at that moment. The area under the trace answers how much energy was delivered during an interval. A rectangular segment has width measured in hours and height measured in megawatts, so its area is measured in megawatt-hours. For a stepped trace, find each rectangle's area and add them. This is the same idea used by integration, without requiring calculus.

A capacity rating is a limit or capability stated under conditions. A measured load is what equipment actually draws. If a service is rated 12 MW, the most we can say from that number alone is that a specified capacity claim exists at that boundary. We cannot conclude that the site draws 12 MW continuously, that its cooling can remove the associated heat, or that IT is installed. Even multiplying 12 MW by a year only creates an energy ceiling under the added assumption of continuous full loading.

## Calculate a day, then change its shape

Take a facility whose live inference plus fixed facility support draws a steady 4 MW. An offline evaluation queue, a fixed set of prompts to run against a model checkpoint, is ready at 00:00 and due at 24:00, and it needs 48 megawatt-hours (MWh) of added energy. Run all its batches together and the queue adds 4 MW for 12 hours: the facility draws 8 MW for those 12 hours and 4 MW for the other 12. The two energy blocks are 96 and 48 MWh, 144 MWh in all. Spread that energy evenly across the day and the average is 144 divided by 24, or 6 MW. The peak is still 8 MW, so a 6 MW connection could not carry this trace.

Now stagger the batch starts and limit how many run at once, so the queue adds 2 MW for all 24 hours. The facility draws a flat 6 MW. Total energy is still 144 MWh and the queue still finishes by the deadline, but peak demand falls from 8 MW to 6 MW. Scheduling has changed the capacity the site needs while the work and its energy stay the same. Live inference keeps answering users as before; only the independent evaluation batches move. The comparison assumes spare compute is available all day and that the evaluations use the same energy and give the same results, whereas a real schedule change can alter GPU efficiency, idle power and cooling. In the lab below, 8 MW for 12 hours followed by 4 MW for 12 hours gives 144 MWh at a 6 MW average and an 8 MW peak; one 6 MW segment of 24 hours reproduces the staggered day.

Look at the headroom under a 6.5 MW supply limit. Running together, the 8 MW hours exceed it by 1.5 MW. Staggered, every hour leaves 0.5 MW of arithmetic margin. Neither number is a complete admission policy for a new workload: other equipment, redundancy requirements and fast excursions may bind first. An arithmetic margin at a meter is useful evidence about that meter, and the equipment downstream of it needs its own check.

## Measurement resolution changes the question

Suppose a displayed five-minute average is 8 MW. That display could come from a constant 8 MW draw. It could also come from one minute at 12 MW followed by four minutes at 7 MW: the energy-equivalent average is (12 + 4 × 7) divided by 5, also 8 MW. These traces are indistinguishable to the average yet impose different peak demands. When investigating a disturbance, collect measurements at a timescale capable of seeing the behavior in question.

The converse mistake is turning a brief spike into a full-day energy assumption. A one-minute excursion may matter to control and protection while adding little to the daily energy total. Quantify both before deciding what to change. A storage device might smooth a short peak if its power, usable energy, controls, and connection permit it. It cannot be selected merely by comparing the daily MWh with a capacity label.

There is also an operational tradeoff. Flattening a flexible training workload may reduce peaks but postpone completion. Flattening interactive demand by making people wait changes the service being delivered. A fair comparison therefore keeps the workload deadline or latency requirement beside the power trace. If the service requirement changes, acknowledge that change instead of reporting a pure electrical improvement.

When you read an energy bill, equipment rating, or monitoring graph, name four things before calculating: the electrical boundary, the units, the duration, and whether the value is a measurement or a rating. Those four labels determine which arithmetic is meaningful. They also prevent a monthly energy total from masquerading as a transient power model, or a large planned connection from masquerading as electricity already consumed.

## Worked example: Two schedules for one evaluation queue

- Live inference plus fixed support draws 4 MW all day.
- The evaluation queue needs 48 MWh, is ready at 00:00 and is due at 24:00.
- All loads are measured at the same facility input against a 6.5 MW supply limit.

1. Run together — 8 MW × 12 h + 4 MW × 12 h = 96 + 48 = 144 MWh — Area equals power multiplied by time; the queue adds 4 MW × 12 h = 48 MWh.
2. Average and peak — 144 / 24 = 6 MW average; 8 MW peak — Divide energy by the full duration to recover average power; the peak is the tallest segment.
3. Stagger — (4 + 2) MW × 24 h = 144 MWh — Spreading the same 48 MWh over 24 hours adds only 2 MW.
4. Supply check — 8 − 6.5 = 1.5 MW over; 6.5 − 6 = 0.5 MW spare — Only the staggered schedule fits under the 6.5 MW limit.

**Result:** Both schedules use 144 MWh and finish the queue on time; staggering lowers the peak from 8 MW to 6 MW, below the 6.5 MW limit.

**Model boundary:** Each segment is a constant average. The model shows neither subinterval peaks nor the changes in GPU efficiency, idle power or cooling that a real schedule change can cause.

## The tradeoff

Choice: Stagger the evaluation batches across the day instead of running them together.

Benefit: Peak demand falls from 8 MW to 6 MW while the queue’s 48 MWh and its deadline stay the same in the model.

Cost: Spare compute must be available all day, individual batches finish later, and real GPU efficiency, idle power and cooling can change with the schedule.

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

## Sources

- [EIA — Measuring electricity](https://www.eia.gov/energyexplained/electricity/measuring-electricity.php) — www.eia.gov · Reviewed 2026-09-06. kW and MW measure power; kWh and MWh include elapsed time.
- [OpenStax — Electrical Energy and Power](https://openstax.org/books/university-physics-volume-2/pages/9-5-electrical-energy-and-power) — openstax.org · Published 2016-10-06 · Reviewed 2026-09-06. Electrical power is a rate of energy transfer.
- [Google Cloud — Best practices for batch inference on GKE](https://docs.cloud.google.com/kubernetes-engine/docs/best-practices/machine-learning/inference/batch-inference) — Google Cloud · Reviewed 2026-09-12. Distinguishes scheduled, latency-tolerant batch inference from real-time serving and from request batching.
