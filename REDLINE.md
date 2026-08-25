# Master diagram redline — disposition

Review date: 2026-08-25
Artifact: `diagram/master.svg`
Posture: IEEE/IEC-inspired conceptual one-line plus simplified thermal process
schematic; Abilene evidence overlay; not as-built and not for
design/construction.

## Release verdict

The original v0 drawing was not approved. The redline-corrected v1 is approved
to advance through course production within its stated conceptual scope. It is
not an as-built or design/construction artifact.

## Blocking redlines

1. **Lifecycle conflation — resolved.** Nodes and edges now carry `presence`,
   `lifecycle`, `as_of`, `fact_ids`, and `source_ids`. The validator rejects a
   lifecycle that the referenced facts cannot support. Solid means
   energized/confirmed; dotted means permitted without installation proof;
   dashed means future design; pale dashed means conceptual teaching topology.
2. **False single electrical path — resolved.** The master contains three
   separate origination branches: initial 138 kV grid service, expansion 345 kV
   grid service, and behind-the-meter generation. They terminate at an abstract,
   conceptual campus-MV distribution envelope; no shared as-built bus is
   asserted. A PPA is a hidden contractual overlay, not a local physical source.
3. **Incorrect thermal hydraulics — resolved.** Technology and facility supply
   and return paths are explicit. CRAH is a parallel residual-air branch.
   The Abilene design rejects heat through air-cooled chillers, and
   fill/treatment connects to the closed facility loop rather than to a cooling
   tower. Exact packages remain conceptual because as-built operation is not
   established.
4. **False package detail — resolved.** BESS and diesel retain complete
   conceptual package boundaries, while campus-MV distribution and 345 kV
   protection render as honest abstract envelopes. Independent inputs have
   independent ports; no unsourced breaker allocation or switch state is shown.
5. **Facts embedded in placement — resolved.** Rendered copy is keyed in
   `master.yaml` and factual placeholders resolve from `evidence/abilene.yaml`.
   `layout.yaml` contains geometry only. An unresolved fact can render only as
   an explicit unknown.

## Secondary redlines

- Journey order is declared in `master.yaml`; render order no longer depends on
  a color-token dictionary.
- The journey bar describes carrier/state, not voltage as a conserved quantity.
- `lifecycle`, `normal_state`, and `flow_direction` replace overloaded
  `variant` flags.
- Standards language is qualified as inspired/conceptual.
- Every rendered node, edge, and label has a stable SVG ID.
- Informational text uses a high-contrast muted token; faint color is reserved
  for guides and dimmed geometry.
- The atmosphere is the terminal sink, not a physically recirculating loop.

## Evidence dispositions

- Campus MV: 34.5 kV is limited to a Buildings 1–2 review design; campus-wide
  as-built voltage remains null.
- Gas generation: 360.5 MW permitted nameplate; commissioned MW remains null.
- Diesel: 62 units / 169.9 MW authorized; installed and operational counts
  remain null.
- Operations: at least two buildings energized; exact current count remains
  null. Workloads were live by 2025-07-22; exact start date remains null.
- Compute: the operating family is NVIDIA GB200; NVL72 remains a design
  reference. Installed GPU count remains null with `no evidence-backed
  estimate`.
- Rack power: nominal 50–51 VDC output is product-documented; Abilene AC input
  remains null, and the detailed shelf path is conceptual.
- Generator terminal: 11–13.8 kV is a model range only; site configuration
  remains null.
- Scope: the adjacent 900 MW, two-building Microsoft project is excluded.
- Cooling: direct-to-chip, closed-loop, non-evaporative design is evidenced;
  exact package operation and as-built topology are not.

## Acceptance checks

- YAML and source-reference validation.
- Exact 2D and 3D coverage of every master node and edge.
- Stable IDs for every rendered node, edge, and label.
- Deterministic SVG and HTML generation.
- Unit tests for branch separation, complete thermal supply/return, lifecycle
  posture, and fail-closed unknowns.
- 1920 × 1080 raster review of the 2D master and focused camera outputs.
- Browser runtime check of all six hybrid states.

Result on 2026-08-25: passed. The live player completed every 2D, overlay, and
3D transition without runtime errors; the final framing review found no cropped
or colliding required callouts.
