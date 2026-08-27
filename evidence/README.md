# Evidence ledger

The registered ledgers separate evidence scopes instead of pooling unlike
claims:

- `abilene.yaml` is the fact boundary for the original eight-building Abilene
  reference campus and remains the master-diagram ledger.
- `commercial_energy.yaml` holds named contract comparisons and authoritative
  accounting boundaries.
- `electrical_engineering.yaml` holds generic conversion, protection,
  distribution, and point-of-load references.
- `thermal_engineering.yaml` holds generic heat-transfer, liquid-loop,
  air-path, and facility-loop references.

`sources` uses stable IDs for primary records. `facts` is a flat mapping so
renderers can resolve a qualified fact reference without interpreting nested
prose.

Every fact carries:

- `value` and `unit`
- `scope` and `basis`
- `lifecycle` and `as_of`
- `source_ids` and `posture`

`null` means the cited evidence does not establish a value. It never means zero.
Planned interconnection, permitted generation, energized infrastructure,
commissioned power, current load, and IT load are distinct and non-additive.

## Postures

- `confirmed`: directly stated by a primary source for the stated scope.
- `confirmed_contract`: directly stated contract terms for the named comparison
  scope, not a physical delivery-path claim.
- `authoritative_guidance`: a standard or guidance boundary, not a site design
  or operating claim.
- `confirmed_minimum`: a primary-source lower bound; the exact total is unknown.
- `planned_not_operational`: a planned rating, not delivered or operating power.
- `permitted_not_observed`: authorized equipment or nameplate, not proof of
  installation, commissioning, or operation.
- `design_not_as_built`: review/design evidence, not an as-built condition.
- `design_not_observed`: a design ceiling or reference, not installed or
  operating equipment.
- `design_selected`: a project-specific selected design, not proof that the
  system was installed, commissioned, or operating.
- `anticipated_not_observed`: a forward-looking operating or maintenance value,
  not measured consumption.
- `confirmed_model_spec`: a manufacturer specification for the identified model.
- `model_range_not_site_configured`: a manufacturer range without the site's
  selected configuration.
- `live_by_not_start_date`: operation existed by the cited disclosure date; the
  exact start date remains unknown.
- `reported_untyped`: reported value whose denominator or capacity basis is not
  supplied and cannot support derived operational claims.
- `unverified_null`: the evidence is insufficient, so the canonical value stays
  `null`.
- `no_evidence_backed_estimate`: no supported numerical estimate exists; the
  fact's `basis` carries the literal output `no evidence-backed estimate`.
- `future_design`: shown as future in design material, not operational.
- `excluded_scope`: recorded only to prevent accidental inclusion or addition.

## Master bindings

Every master node and edge carries `fact_ids`. Its `source_ids` must exactly
match the union of the referenced facts' sources. Energized or operational
geometry may use only non-null evidence with an operating lifecycle; design,
planned, product-documentation, permit, and unknown facts cannot be promoted to
solid operational geometry. Permitted and future-design geometry must include a
fact at the matching lifecycle. Conceptual, terminal, and course-variant records
may use empty `fact_ids` and `source_ids`.

The project validator rejects duplicate YAML mapping keys before loading any
manifest, so a later duplicate cannot silently replace an earlier evidence or
topology record.

## Boundary

The initial 200 MW / 138 kV path and the separate 1 GW / 345 kV expansion path
belong to the original reference campus but are not interchangeable topology.
The adjacent two-building, 900 MW Microsoft expansion is explicitly excluded.
Its buildings and power must not be folded into the original eight-building
campus facts.
