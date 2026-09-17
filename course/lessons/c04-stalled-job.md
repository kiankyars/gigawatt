# The powered cluster that keeps waiting

Generated reading view. Edit [`course/expansion/capstones.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/capstones.json), lesson `c04-stalled-job`, then run `uv run gigawatt-expand`.

**16. Put the system together · Authored draft**

Trace a payload from sender through fabric to receiver, compare two upgrades, and test the predicted gain against end-to-end progress.

**Driving question:** Which physical segment limits communication, and would upgrading it shorten the complete job cycle?

## Name what the job is waiting for

A hypothetical distributed job repeats a serial cycle: 60 seconds of useful compute, a communication phase, and 10 seconds of other fixed work. The supplied application trace shows no overlap. The same work completes each cycle. Every device remains allocated throughout, including the waiting time; allocation therefore does not establish useful progress. Keep the compute duration and the other work fixed while testing the communication path.

The communication phase moves one supplied 800 GB payload through a sender, a fabric bottleneck and a receiver. Their achieved payload-rate limits are 80, 40 and 80 GB/s respectively. The path is limited to 40 GB/s, so the transfer takes 20 seconds. These decimal payload units and effective rate limits are original scenario inputs. They are not advertised port speeds or measurements of a named platform. A real collective may add rounds, shared traffic and synchronization; the single-payload model applies only to the declared transfer here.

## Make a falsifiable improvement prediction

Proposal E doubles the sender rate limit from 80 to 160 GB/s while the 40 GB/s fabric bottleneck and 80 GB/s receiver remain unchanged. Proposal F doubles the fabric bottleneck to 80 GB/s, keeping both endpoints unchanged. Predict the achieved path rate, the communication interval and the complete cycle for each proposal before inspecting the result. Improving the sender leaves a slower segment downstream; improving the fabric releases the binding constraint in this supplied path.

After the change, measure the same payload across the complete path and align that measurement with the application trace. An end-to-end rate of 40 GB/s still predicts a 20-second communication phase and a 90-second cycle. A rate of 80 GB/s predicts 10 seconds and an 80-second cycle. If those intervals do not match, investigate another bottleneck, changed synchronization, a different payload or a broken no-overlap assumption. Verify correct output as well as completion time. A link negotiating its new speed does not by itself establish the payload rate or useful job throughput.

## Worked example: Compare an endpoint upgrade with a bottleneck upgrade

- Original serial cycle: 60 s useful compute, one 800 GB communication phase, then 10 s other fixed work; no overlap.
- Achieved payload-rate limits: sender 80 GB/s, fabric bottleneck 40 GB/s, receiver 80 GB/s.
- E doubles only the sender limit; F doubles only the fabric bottleneck. Work per cycle stays fixed.

1. Baseline path rate is min(80, 40, 80) = 40 GB/s. Communication takes 800/40 = 20 s.
2. The complete baseline cycle is 60 + 20 + 10 = 90 s. Useful-compute share is 60/90 = 66.7%.
3. E gives min(160, 40, 80) = 40 GB/s. Communication and the 90 s complete cycle are unchanged.
4. F gives min(80, 80, 80) = 80 GB/s. Communication takes 10 s, and the complete cycle takes 80 s.
5. With fixed work per cycle, F produces 90/80 = 1.125 times baseline cycle throughput: a 12.5% gain. Doubling one phase rate does not double useful job throughput.

**Result:** The fabric intervention saves ten seconds per cycle; the sender intervention saves none on this path. Verify the changed end-to-end rate, phase time and correct output.

**Model boundary:** All payloads, achieved rate limits and phase times are original teaching inputs. The model excludes overlap, collective algorithm details, startup and failure recovery. No rack-power rating, advertised FLOPS or generic utilization counter is converted into useful output.

## The tradeoff

Choice: Upgrade the fabric segment that limits the measured path.

Benefit: The predicted ten-second cycle reduction is tied to a specific physical bottleneck and an observable transfer.

Cost: Acquisition, installation disruption, topology changes and future sharing still affect value; the larger speed improvement is not automatically the better investment.

## When the situation changes

Trigger: The new link reports its higher speed, but the complete job cycle remains at 90 seconds.

Mechanism: The achieved payload rate may still be limited by another segment, shared traffic or synchronization; the negotiated link rate is not the end-to-end rate.

Response: Measure the same payload at the path endpoints, align the compute and communication intervals, and check the changed configuration and correct output against the prediction.

## Apply the idea

After the fabric upgrade, a receiver-side limit of 50 GB/s is discovered. The sender and fabric can each deliver 80 GB/s. With the same payload and serial phases, what are the new communication and cycle times? Which path segment should be investigated next?

<details>
<summary>Reveal the worked answer</summary>

The path rate is min(80, 80, 50) = 50 GB/s. Communication takes 800/50 = 16 s, and the complete cycle takes 60 + 16 + 10 = 86 s. The receiver side is now binding.

The bottleneck moves when one segment improves. The cycle-throughput gain is 90/86, about 1.047 times baseline; further sender or fabric upgrades cannot remove the supplied receiver limit.

</details>

**The idea to keep:** A job's critical path is a time budget. Improve the segment that governs completion and measure whether the expected gain appears.

## Sources and reading boundaries

- [NVIDIA DGX SuperPOD — Network Fabrics](https://docs.nvidia.com/dgx-superpod/reference-architecture-scalable-infrastructure-h100/latest/network-fabrics.html) — Physical compute-fabric context: endpoint connections, switches and inter-switch paths. All payloads, achieved rates, timings and interventions in the case are original teaching inputs. Read 2026-09-16. The reference architecture motivates tracing a complete physical path. The case does not reproduce its topology, device ratings, measured performance or scheduling behavior.
