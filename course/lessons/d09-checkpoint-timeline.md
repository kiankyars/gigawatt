# Count preserved progress, lost progress and recovery

Generated reading view. Edit [`course/expansion/racks-compute-heat.json`](https://github.com/kiankyars/gigawatt/blob/main/course/expansion/racks-compute-heat.json), lesson `d09-checkpoint-timeline`, then run `uv run gigawatt-expand`.

**10. Storage, orchestration and recovery · Authored draft**

Compare explicit failure timelines and explain why asynchronous saving and replicated storage do not eliminate recovery design.

**Driving question:** When do more frequent checkpoints improve completed work, and when do they only add overhead?

## Draw four different kinds of time

A job timeline contains useful computation, checkpoint work, lost computation and recovery. Useful computation becomes lost only when a failure forces the job to return to an earlier saved state. Recovery includes more than reading bytes: detecting failure, obtaining resources, recreating the environment, restoring state and becoming ready to advance again can each consume time. Color those intervals separately. Otherwise a report can count recomputed work as new progress or describe storage transfer time as the entire outage.

Define the checkpoint interval carefully. It might mean wall-clock time between attempts, useful computation between completed checkpoints, or a number of application steps. These policies behave differently when checkpoint duration changes. The example below uses useful-computation time between checkpoints, pauses progress while saving, and declares a single failure at a fixed wall-clock instant. That makes every interval auditable. It does not assume that real failures arrive periodically or independently.

## A completed snapshot is a recovery point

The recovery point objective describes how much state or progress the service can afford to lose under its intended scenario. The recovery time objective describes how quickly the service should be restored. Checkpoint frequency influences the first, while scheduling, storage reads, initialization and operator response influence the second. Neither objective is guaranteed by a retention policy written on paper. A recovery exercise must demonstrate that the selected checkpoint is readable, coherent and compatible with the environment being restored.

Redundant storage and backup solve overlapping but different problems. Replication may preserve access after a device failure while also copying an accidental deletion. A retained backup may survive that deletion but take longer to restore. A model checkpoint may preserve training state but omit the software environment, dataset version or credentials required to continue safely. The recovery plan therefore includes a manifest of dependencies and a clear definition of valid progress, not only a directory full of large files.

## Asynchronous saving moves contention rather than abolishing it

Asynchronous checkpointing can allow computation to continue while saved state is written. PyTorch’s documented approach includes staging state and managing outstanding saves; its tutorial highlights additional host-memory pressure. The central invariant is that the saved version must remain coherent while the live application changes. Overlap can shorten the visible pause, but memory copies, CPU work, network traffic and storage writes still consume resources. If these interfere with input preparation or communication, normal steps can become slower.

Bound the number of outstanding saves. If a new checkpoint arrives faster than the backend can persist the previous one, queued state can accumulate and exhaust memory or storage. The newest attempted checkpoint is not necessarily the newest completed recovery point. Monitoring should expose both timestamps. Evaluate the whole job duration and recoverable progress under load, rather than quoting only the time until an asynchronous function returns. A fast return is an API behavior, not a durability measurement.

The current PyTorch tutorial makes the two completion events concrete. Its asynchronous-staging example waits for the device-to-host copy before the optimizer modifies model parameters, and tracks upload completion separately. A host-memory snapshot can therefore free the training loop to proceed while remaining vulnerable to losing that host. The teaching comparison stops the application during staging, then overlaps a background write with later steps; it does not assume that an immediate function return makes the checkpoint recoverable.

## Choose a policy with a failure model and a service goal

More frequent checkpoints generally reduce the maximum unsaved interval while increasing normal saving work. Their benefit depends on when failures occur, what scope is lost and how long restoration takes. A rare node fault that affects one small task differs from a shared storage outage that blocks an entire cluster. Use measured incidents where available and explicit scenarios where they are not. Compare policies across several failure positions and include a no-failure case so the cost of protection remains visible.

## Case study: Llama 3 needed routine recovery

The Llama 3 report describes 466 interruptions during a 54-day training snapshot: 47 planned and 419 unexpected. It reports more than 90% effective training time and only three incidents requiring significant manual intervention. Automated diagnosis, reduced startup time and shorter checkpoint operations helped preserve useful progress despite interruptions. Its flight recorder captures collective-operation information for diagnosing a stuck distributed job. These are measurements and operational observations from that run; neither interruption count nor effective training time is a hardware-availability guarantee. The detailed category table has inconsistent counts and percentages, so this lesson uses the internally consistent prose totals.

## Account for the energy spent recovering

The slides reuse the explicit failure-at-minute-35 timeline and assign the job 1 MW during computation, 0.8 MW during checkpoint pauses and 0.4 MW during restoration. Power is held constant within each stage, so its energy is power multiplied by duration. The 20-minute policy spends 1 MWh on the final 60 useful minutes, 13/60 MWh on computation that the failure discards, 0.8 × 4/60 MWh on saving and 0.4 × 5/60 MWh on restoration: about 1.303 MWh in total. The 40-minute policy spends about 1.643 MWh, including 35 minutes of discarded computation and two minutes saving. This account covers the stated job power; it is not a facility PUE or campus demand measurement.

## Worked example: Two policies face one failure at minute 35

- The job needs 60 minutes of useful computation. A valid initial checkpoint exists at zero progress.
- Policy A checkpoints after every 20 useful minutes; policy B after every 40. Each checkpoint pauses computation for 2 minutes.
- A single failure occurs at wall-clock minute 35 and restoration takes 5 minutes. No final checkpoint is required to count job completion.

1. Follow policy A to failure — Work 0–20; save 20–22; work 22–35 — A has preserved 20 useful minutes and loses the following 13.
2. Follow policy B to failure — Work 0–35; no completed new checkpoint — B loses all 35 attempted useful minutes and returns to zero.
3. Restore both jobs — Recovery 35–40 — The same five-minute restoration is assumed for both policies.
4. Finish policy A — Work 40–60; save 60–62; work 62–82 — Forty remaining useful minutes produce completion at minute 82.
5. Finish policy B — Work 40–80; save 80–82; work 82–102 — Sixty remaining useful minutes produce completion at minute 102.

**Result:** Policy A finishes 20 minutes earlier for this failure placement. Without a failure, A would incur one extra two-minute checkpoint before completing the same work.

**Model boundary:** This is an explicit scenario, not an estimate of failure probabilities or an optimal interval for a real cluster.

## The tradeoff

Choice: Shorten the interval between checkpoints.

Benefit: Reduce the amount of unsaved progress exposed to many failure timings.

Cost: Increase checkpoint traffic and pauses or asynchronous contention; more saved versions also consume retention capacity.

## When the situation changes

Trigger: Monitoring treats an initiated asynchronous save as a completed checkpoint.

Mechanism: After a fault, the service attempts to restore a version whose background write never reached a valid completion boundary.

Response: Track completion and verification separately from initiation, retain a previous valid state and exercise restart from the exact selected version.

## Apply the idea

Move the only failure to minute 55, keeping all policies unchanged. How much progress has each preserved, and when does each finish after the five-minute recovery?

<details>
<summary>Reveal the worked answer</summary>

Both have preserved 40 useful minutes. Both restart at minute 60 and complete the remaining 20 useful minutes at minute 80.

A loses 11 unsaved minutes while B loses 13, but A spent two additional minutes saving before failure. Their net preserved progress is identical at this failure instant. More frequent saving is not strictly better for every realized timeline.

</details>

**The idea to keep:** A checkpoint policy trades normal overhead against the amount of work that must be repeated after a specified failure.

## Sources and reading boundaries

- [Asynchronous Saving with Distributed Checkpoint](https://docs.pytorch.org/tutorials/recipes/distributed_async_checkpoint_recipe.html) — A coherent staging copy, background persistence and completion tracking are distinct; outstanding saves consume host memory. Read 2026-09-14. The current tutorial exposes separate staging and upload completion signals for asynchronous staging. API details depend on the framework version; teaching diagrams describe the state transitions, not a deployment recipe.
- [PyTorch Distributed Checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html) — Distributed state saving and loading require coordinated state and backend-specific handling. Read 2026-09-06. Public indexed API excerpts reviewed; the directly opened stable URL returned a redirect shell. Pin and review the selected framework release and storage writer before implementation; no complete API audit is claimed.
- [The Llama 3 Herd of Models — infrastructure and operational reliability](https://arxiv.org/html/2407.21783v3) — Dated 54-day interruption snapshot, effective training time, and automated diagnosis/recovery. Read 2026-09-14. Read sections 3.3.1 and 3.3.4; cross-checked PDF printed page 13. A 54-day snapshot, not a universal failure rate. Table 5 prints 148 faulty-GPU interruptions with 30.1%; rows total 441 although prose says 419 unexpected. Use coherent prose totals and do not recreate the category table.
