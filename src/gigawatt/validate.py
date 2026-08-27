"""Fail-closed validation for the evidence, 2D, 3D, and camera manifests."""

from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any, Iterable

import yaml

from . import layout as layout_pipeline
from . import scene as scene_pipeline
from . import tokens

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
EVIDENCE = ROOT / "evidence" / "abilene.yaml"
COURSE = ROOT / "course" / "segments.yaml"

NODE_FIELDS = {
    "id",
    "label",
    "domain",
    "gate",
    "presence",
    "lifecycle",
    "as_of",
    "source_ids",
    "fact_ids",
}
EDGE_FIELDS = {
    "id",
    "from",
    "to",
    "carries",
    "presence",
    "lifecycle",
    "normal_state",
    "flow_direction",
    "source_ids",
    "fact_ids",
}
FACT_FIELDS = {"value", "unit", "scope", "basis", "lifecycle", "as_of", "source_ids", "posture"}
SOURCE_FIELDS = {"publisher", "title", "kind", "url", "publication_date", "review_date", "accessed_as_of", "date_note"}
LIFECYCLES = set(layout_pipeline.LIFECYCLE_STYLE)
FACT_POSTURES = {
    "anticipated_not_observed",
    "confirmed",
    "confirmed_minimum",
    "confirmed_model_spec",
    "design_not_as_built",
    "design_not_observed",
    "design_selected",
    "excluded_scope",
    "future_design",
    "live_by_not_start_date",
    "model_range_not_site_configured",
    "no_evidence_backed_estimate",
    "permitted_not_observed",
    "planned_not_operational",
    "reported_untyped",
    "unverified_null",
}
FACT_LIFECYCLES = {
    "anticipated_maintenance",
    "as_built_unknown",
    "commissioning_unknown",
    "constructed",
    "delivered_untyped",
    "deployed",
    "design_ceiling",
    "design_reference",
    "design_requirement",
    "energized",
    "future_design",
    "installation_unknown",
    "operating",
    "operation_unknown",
    "permitted",
    "planned",
    "product_documented",
    "review_design",
    "selected_design",
    "site_configuration_unknown",
    "topology_unknown",
}
OPERATIONAL_MASTER_LIFECYCLES = {"energized", "operational_confirmed"}
OPERATIONAL_FACT_LIFECYCLES = {"energized", "operating", "deployed"}
OPERATIONAL_ALLOWED_FACT_LIFECYCLES = OPERATIONAL_FACT_LIFECYCLES | {"constructed"}
EMPTY_FACT_IDS_ALLOWED = {"conceptual", "course_variant", "terminal"}
DESIGN_FACT_LIFECYCLES = {
    "anticipated_maintenance",
    "design_ceiling",
    "design_reference",
    "design_requirement",
    "future_design",
    "review_design",
    "selected_design",
}
NULL_POSTURES = {"no_evidence_backed_estimate", "unverified_null"}
COURSE_META_FIELDS = {
    "course_id",
    "inventory_scope",
    "status",
    "runtime_minutes",
    "relative_weight_total",
    "master",
    "cameras",
    "evidence_ledgers",
    "master_evidence_ledger",
    "sequence_rule",
}
ACT_FIELDS = {"id", "title", "learning_objective", "segments"}
SEGMENT_FIELDS = {
    "id",
    "title",
    "opening_question",
    "learning_objective",
    "weight",
    "depends_on",
    "camera",
    "node_ids",
    "edge_ids",
    "evidence",
    "transition",
}
SEGMENT_CAMERA_FIELDS = {
    "anchor",
    "shot",
    "mode",
    "status",
    "reveal_ids",
    "reveal_copy_ids",
}
SEGMENT_EVIDENCE_FIELDS = {
    "readiness",
    "claims",
    "promotion_guards",
    "blocking_research",
}
SEGMENT_CLAIM_FIELDS = {"id", "assertion", "binding", "fact_refs"}
SEGMENT_TRANSITION_FIELDS = {"to", "cue"}
SEGMENT_READINESS = {"evidence_ready", "research_required"}
SEGMENT_CAMERA_STATUS = {"existing", "planned"}
SEGMENT_ASSERTIONS = {
    "anticipated",
    "confirmed",
    "confirmed_minimum",
    "design_reference",
    "excluded_scope",
    "explicit_unknown",
    "future_design",
    "live_by",
    "no_evidence_backed_estimate",
    "permitted",
    "planned",
    "product_reference",
    "reported_untyped",
    "selected_design",
}
SEGMENT_CLAIM_BINDINGS = {"topology", "overlay"}
LEDGER_ID_PATTERN = re.compile(r"[a-z][a-z0-9_]*\Z")
ASSERTION_REQUIRED_GUARDS = {
    "anticipated": {"anticipated_to_measured"},
    "confirmed_minimum": {"minimum_to_exact"},
    "design_reference": {"design_to_as_built"},
    "excluded_scope": {"excluded_scope_addition"},
    "explicit_unknown": {"null_to_zero"},
    "future_design": {"future_design_to_operational"},
    "live_by": {"live_by_to_start_date"},
    "no_evidence_backed_estimate": {"null_to_zero"},
    "permitted": {"permitted_to_installed", "permitted_to_commissioned"},
    "planned": {"planned_to_operational"},
    "product_reference": {"product_to_site_configuration"},
    "reported_untyped": {"untyped_to_capacity"},
    "selected_design": {"design_to_as_built"},
}
BLOCKER_PLACEHOLDERS = {"research", "research required", "tbd", "todo", "unknown"}
PROMOTION_GUARDS = {
    "announced_to_operational",
    "anticipated_to_measured",
    "capacity_basis_substitution",
    "conceptual_to_as_built",
    "contractual_to_physical",
    "design_ceiling_to_installed",
    "design_to_as_built",
    "excluded_scope_addition",
    "future_design_to_operational",
    "live_by_to_start_date",
    "minimum_to_exact",
    "model_range_to_site_configuration",
    "null_to_zero",
    "permitted_to_commissioned",
    "permitted_to_installed",
    "planned_to_operational",
    "product_to_site_configuration",
    "reverse_physical_flow",
    "single_path_conflation",
    "site_scope_transfer",
    "substation_to_it_load",
    "untyped_to_capacity",
}


class ValidationError(ValueError):
    """Raised when any project contract is violated."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silent mapping-key replacement."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            mark = key_node.start_mark
            raise ValidationError(
                f"{mark.name}:{mark.line + 1}:{mark.column + 1}: unhashable YAML mapping key"
            ) from exc
        if duplicate:
            mark = key_node.start_mark
            raise ValidationError(
                f"{mark.name}:{mark.line + 1}:{mark.column + 1}: duplicate YAML key {key!r}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def _load_yaml_strict(path: Path) -> dict[str, Any]:
    try:
        with path.open() as stream:
            data = yaml.load(stream, Loader=_UniqueKeyLoader)
    except ValidationError:
        raise
    except (OSError, yaml.YAMLError) as exc:
        raise ValidationError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ValidationError(f"{path}: expected a mapping")
    return data


def _unique(items: Iterable[str], location: str) -> set[str]:
    values = list(items)
    if len(values) != len(set(values)):
        raise ValidationError(f"{location}: IDs must be unique")
    return set(values)


def _exact_fields(record: dict[str, Any], fields: set[str], location: str) -> None:
    missing = fields - set(record)
    extra = set(record) - fields
    if missing or extra:
        raise ValidationError(
            f"{location}: missing={sorted(missing)} extra={sorted(extra)}"
        )


def _nonempty_string(value: Any, location: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValidationError(f"{location}: expected a non-empty string")


def _string_list(value: Any, location: str, *, allow_empty: bool = True) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise ValidationError(f"{location}: expected a list of strings")
    if not allow_empty and not value:
        raise ValidationError(f"{location}: expected a non-empty list")
    return _unique(value, location)


def _course_ledger_registry(
    meta: dict[str, Any], *, require_existing: bool = False
) -> dict[str, Path]:
    registry = meta.get("evidence_ledgers")
    if not isinstance(registry, dict) or not registry:
        raise ValidationError("course.meta.evidence_ledgers must be a non-empty mapping")

    evidence_root = (ROOT / "evidence").resolve()
    paths: dict[str, Path] = {}
    for ledger_id, raw_path in registry.items():
        if not isinstance(ledger_id, str) or not LEDGER_ID_PATTERN.fullmatch(ledger_id):
            raise ValidationError(
                f"course evidence ledger ID {ledger_id!r} must match {LEDGER_ID_PATTERN.pattern!r}"
            )
        _nonempty_string(raw_path, f"course.meta.evidence_ledgers.{ledger_id}")
        relative_path = Path(raw_path)
        if relative_path.is_absolute() or relative_path.suffix not in {".yaml", ".yml"}:
            raise ValidationError(
                f"course evidence ledger {ledger_id}: path must be a relative YAML file under evidence/"
            )
        resolved = (ROOT / relative_path).resolve()
        if resolved.parent != evidence_root and evidence_root not in resolved.parents:
            raise ValidationError(
                f"course evidence ledger {ledger_id}: path must remain under evidence/"
            )
        if require_existing and not resolved.is_file():
            raise ValidationError(
                f"course evidence ledger {ledger_id}: file does not exist: {raw_path}"
            )
        paths[ledger_id] = resolved

    if len(set(paths.values())) != len(paths):
        raise ValidationError("course evidence ledger paths must be unique")
    master_ledger = meta.get("master_evidence_ledger")
    if master_ledger not in paths:
        raise ValidationError(
            "course.meta.master_evidence_ledger must name a registered evidence ledger"
        )
    return paths


def _load_course_evidence_ledgers(course: dict[str, Any]) -> dict[str, dict[str, Any]]:
    meta = course.get("meta")
    if not isinstance(meta, dict):
        raise ValidationError("course.meta: expected a mapping")
    paths = _course_ledger_registry(meta, require_existing=True)
    ledgers = {ledger_id: _load_yaml_strict(path) for ledger_id, path in paths.items()}
    for ledger_id, ledger in ledgers.items():
        _validate_evidence_schema(ledger, f"evidence ledger {ledger_id}")
    return ledgers


def _resolve_fact_ref(
    fact_ref: str,
    ledgers: dict[str, dict[str, Any]],
    location: str,
) -> tuple[str, str, dict[str, Any]]:
    if not isinstance(fact_ref, str) or fact_ref.count(":") != 1:
        raise ValidationError(f"{location}: malformed qualified fact reference {fact_ref!r}")
    ledger_id, fact_id = fact_ref.split(":", 1)
    if not LEDGER_ID_PATTERN.fullmatch(ledger_id) or not LEDGER_ID_PATTERN.fullmatch(fact_id):
        raise ValidationError(f"{location}: malformed qualified fact reference {fact_ref!r}")
    if ledger_id not in ledgers:
        raise ValidationError(f"{location}: unknown evidence ledger {ledger_id!r}")
    facts = ledgers[ledger_id].get("facts") or {}
    if fact_id not in facts:
        raise ValidationError(f"{location}: unknown fact {fact_ref!r}")
    return ledger_id, fact_id, facts[fact_id]


def _source_refs(records: Iterable[dict[str, Any]], source_ids: set[str], location: str) -> None:
    for record in records:
        unknown = set(record.get("source_ids") or []) - source_ids
        if unknown:
            raise ValidationError(f"{location} {record.get('id', '<record>')}: unknown sources {sorted(unknown)}")


def _validate_fact_binding(
    record: dict[str, Any], facts: dict[str, dict[str, Any]], location: str
) -> None:
    record_id = record.get("id", "<record>")
    fact_ids = record.get("fact_ids")
    if not isinstance(fact_ids, list) or any(not isinstance(fact_id, str) for fact_id in fact_ids):
        raise ValidationError(f"{location} {record_id}: fact_ids must be a list of strings")
    _unique(fact_ids, f"{location} {record_id}.fact_ids")

    lifecycle = record["lifecycle"]
    if not fact_ids and lifecycle not in EMPTY_FACT_IDS_ALLOWED:
        raise ValidationError(
            f"{location} {record_id}: lifecycle {lifecycle!r} requires at least one fact_id"
        )

    unknown = set(fact_ids) - set(facts)
    if unknown:
        raise ValidationError(f"{location} {record_id}: unknown facts {sorted(unknown)}")

    referenced = [facts[fact_id] for fact_id in fact_ids]
    expected_sources = {
        source_id for fact in referenced for source_id in fact.get("source_ids") or []
    }
    source_list = record.get("source_ids")
    if not isinstance(source_list, list) or any(
        not isinstance(source_id, str) for source_id in source_list
    ):
        raise ValidationError(f"{location} {record_id}: source_ids must be a list of strings")
    _unique(source_list, f"{location} {record_id}.source_ids")
    actual_sources = set(source_list)
    if actual_sources != expected_sources:
        raise ValidationError(
            f"{location} {record_id}: source_ids must equal fact source union; "
            f"expected {sorted(expected_sources)}, got {sorted(actual_sources)}"
        )

    if lifecycle in OPERATIONAL_MASTER_LIFECYCLES:
        incompatible = [
            fact_id
            for fact_id, fact in zip(fact_ids, referenced)
            if fact.get("value") is None
            or fact.get("lifecycle") not in OPERATIONAL_ALLOWED_FACT_LIFECYCLES
        ]
        if incompatible:
            raise ValidationError(
                f"{location} {record_id}: facts {incompatible} cannot support "
                f"{lifecycle}; operational geometry cannot use null, design, "
                "product, permit, planned, or unknown evidence"
            )
        if not any(
            fact.get("lifecycle") in OPERATIONAL_FACT_LIFECYCLES for fact in referenced
        ):
            raise ValidationError(
                f"{location} {record_id}: {lifecycle} requires at least one "
                f"{sorted(OPERATIONAL_FACT_LIFECYCLES)} fact"
            )

    if lifecycle == "permitted" and not any(
        fact.get("lifecycle") == "permitted" for fact in referenced
    ):
        raise ValidationError(
            f"{location} {record_id}: permitted geometry requires a permitted fact"
        )

    if lifecycle == "future_design" and not any(
        fact.get("lifecycle") in DESIGN_FACT_LIFECYCLES for fact in referenced
    ):
        raise ValidationError(
            f"{location} {record_id}: future_design geometry requires a design fact"
        )


def _copy_ids(layout: dict[str, Any]) -> list[str]:
    ids = [layout["title_id"], layout["subtitle_id"]]
    ids.extend(zone["copy_id"] for zone in layout.get("zones") or [])
    ids.extend(region["copy_id"] for region in layout.get("regions") or [] if "copy_id" in region)
    ids.extend(item["id"] for item in layout.get("room_labels") or [])
    ids.extend(item["id"] for item in layout.get("labels") or [])
    legend = layout.get("legend") or {}
    if legend:
        ids.append(legend["title_id"])
        ids.extend(item["id"] for item in legend.get("entries") or [])
    return ids


def _validate_evidence_schema(
    evidence: dict[str, Any], location: str = "evidence"
) -> tuple[set[str], set[str]]:
    if evidence.get("schema_version") != 1:
        raise ValidationError(f"{location}: schema_version must be 1")
    _nonempty_string(evidence.get("accessed_as_of"), f"{location}.accessed_as_of")
    sources = evidence.get("sources") or {}
    facts = evidence.get("facts") or {}
    source_ids = _unique(sources, "evidence.sources")
    fact_ids = _unique(facts, "evidence.facts")
    for source_id, source in sources.items():
        missing = SOURCE_FIELDS - set(source)
        if missing:
            raise ValidationError(f"source {source_id}: missing {sorted(missing)}")
        if not str(source["url"]).startswith("https://"):
            raise ValidationError(f"source {source_id}: expected an HTTPS primary-source URL")
        if source["accessed_as_of"] != evidence["accessed_as_of"]:
            raise ValidationError(
                f"source {source_id}: accessed_as_of must match the evidence ledger"
            )
    for fact_id, fact in facts.items():
        missing = FACT_FIELDS - set(fact)
        if missing:
            raise ValidationError(f"fact {fact_id}: missing {sorted(missing)}")
        if fact["lifecycle"] not in FACT_LIFECYCLES:
            raise ValidationError(f"fact {fact_id}: unknown lifecycle {fact['lifecycle']!r}")
        if fact["posture"] not in FACT_POSTURES:
            raise ValidationError(f"fact {fact_id}: unknown posture {fact['posture']!r}")
        if not isinstance(fact["scope"], str) or not fact["scope"].strip():
            raise ValidationError(f"fact {fact_id}: scope must be a non-empty string")
        if not isinstance(fact["basis"], str) or not fact["basis"].strip():
            raise ValidationError(f"fact {fact_id}: basis must be a non-empty string")
        if not isinstance(fact["as_of"], str):
            raise ValidationError(f"fact {fact_id}: as_of must be a quoted string")
        if not isinstance(fact["source_ids"], list) or not fact["source_ids"]:
            raise ValidationError(f"fact {fact_id}: source_ids must be a non-empty list")
        _unique(fact["source_ids"], f"fact {fact_id}.source_ids")
        unknown = set(fact["source_ids"]) - source_ids
        if unknown:
            raise ValidationError(f"fact {fact_id}: unknown sources {sorted(unknown)}")
        if fact["value"] is None and fact["posture"] not in NULL_POSTURES:
            raise ValidationError(
                f"fact {fact_id}: null value requires one of {sorted(NULL_POSTURES)}"
            )
        if fact["value"] is not None and fact["posture"] in NULL_POSTURES:
            raise ValidationError(f"fact {fact_id}: null posture requires a null value")
    return source_ids, fact_ids


def _validate_abilene_evidence(evidence: dict[str, Any]) -> None:
    if evidence.get("accessed_as_of") != "2026-08-25":
        raise ValidationError("Abilene evidence accessed_as_of must be 2026-08-25")
    facts = evidence["facts"]
    gpu = facts["installed_gpu_count"]
    if gpu["value"] is not None or gpu["basis"] != "no evidence-backed estimate":
        raise ValidationError("installed_gpu_count must fail closed with literal no evidence-backed estimate")
    if facts["adjacent_microsoft_scope_included"]["value"] is not False:
        raise ValidationError("adjacent Microsoft scope must remain excluded")
    for null_fact in (
        "campus_lpt_secondary_as_built_voltage_kv",
        "grid_expansion_upstream_line",
        "gas_commissioned_mw",
        "diesel_units_installed",
        "diesel_operational_units",
        "operational_buildings_exact",
        "exact_workload_start_date",
        "rack_power_shelf_ac_input_voltage_v",
        "generator_terminal_site_voltage_kv",
        "bess_operational_status",
        "campus_source_merge_as_built_topology",
        "bess_campus_connection_as_built_topology",
        "diesel_campus_connection_as_built_topology",
    ):
        if facts[null_fact]["value"] is not None:
            raise ValidationError(f"{null_fact} must remain null until new primary evidence is added")


def _validate_evidence(evidence: dict[str, Any]) -> tuple[set[str], set[str]]:
    source_ids, fact_ids = _validate_evidence_schema(evidence)
    _validate_abilene_evidence(evidence)
    return source_ids, fact_ids


def _validate_master(
    master: dict[str, Any], evidence: dict[str, Any], source_ids: set[str]
) -> tuple[set[str], set[str]]:
    nodes = master.get("nodes") or []
    edges = master.get("edges") or []
    facts = evidence.get("facts") or {}
    node_ids = _unique((node["id"] for node in nodes), "master.nodes")
    edge_ids = _unique((edge["id"] for edge in edges), "master.edges")
    for node in nodes:
        missing = NODE_FIELDS - set(node)
        if missing:
            raise ValidationError(f"node {node.get('id')}: missing {sorted(missing)}")
        if node["lifecycle"] not in LIFECYCLES:
            raise ValidationError(f"node {node['id']}: unknown lifecycle {node['lifecycle']!r}")
        _validate_fact_binding(node, facts, "node")
    for edge in edges:
        missing = EDGE_FIELDS - set(edge)
        if missing:
            raise ValidationError(f"edge {edge.get('id')}: missing {sorted(missing)}")
        if edge["from"] not in node_ids or edge["to"] not in node_ids:
            raise ValidationError(f"edge {edge['id']}: endpoint absent from master nodes")
        if edge["lifecycle"] not in LIFECYCLES:
            raise ValidationError(f"edge {edge['id']}: unknown lifecycle {edge['lifecycle']!r}")
        if "variant" in edge:
            raise ValidationError(f"edge {edge['id']}: use lifecycle/normal_state/flow_direction, not variant")
        _validate_fact_binding(edge, facts, "edge")
    _source_refs(nodes, source_ids, "node")
    _source_refs(edges, source_ids, "edge")

    copy = master.get("copy")
    if not isinstance(copy, dict) or not copy:
        raise ValidationError("master.copy must be a non-empty mapping")
    copy_ids = set(copy)
    hidden_copy_ids = {
        copy_id
        for copy_id, spec in copy.items()
        if spec.get("base_visible", True) is False
    }
    owned_hidden_copy_ids: set[str] = set()
    for kind, records in (("node", nodes), ("edge", edges)):
        for record in records:
            location = f"{kind} {record['id']}.reveal_copy_ids"
            reveal_copy_ids = _string_list(record.get("reveal_copy_ids", []), location)
            if reveal_copy_ids and record.get("base_visible", True) is not False:
                raise ValidationError(
                    f"{kind} {record['id']}: only hidden records may own reveal copy"
                )
            unknown_copy_ids = reveal_copy_ids - copy_ids
            if unknown_copy_ids:
                raise ValidationError(
                    f"{kind} {record['id']}: unknown reveal copy IDs "
                    f"{sorted(unknown_copy_ids)}"
                )
            visible_copy_ids = reveal_copy_ids - hidden_copy_ids
            if visible_copy_ids:
                raise ValidationError(
                    f"{kind} {record['id']}: reveal copy must be base-hidden "
                    f"{sorted(visible_copy_ids)}"
                )
            owned_hidden_copy_ids.update(reveal_copy_ids)
    orphaned_hidden_copy_ids = hidden_copy_ids - owned_hidden_copy_ids
    if orphaned_hidden_copy_ids:
        raise ValidationError(
            "hidden master copy requires a hidden node/edge reveal owner: "
            f"{sorted(orphaned_hidden_copy_ids)}"
        )

    journeys = master["meta"]["journey_bar"]
    unknown_electrical = set(journeys["electrical"]) - set(tokens.VOLTAGE)
    unknown_thermal = set(journeys["thermal"]) - set(tokens.THERMAL)
    if unknown_electrical or unknown_thermal:
        raise ValidationError(
            f"journey token drift: electrical={sorted(unknown_electrical)} thermal={sorted(unknown_thermal)}"
        )

    node_map = {node["id"]: node for node in nodes}
    if node_map["bess_package"]["lifecycle"] != "future_design":
        raise ValidationError("BESS must remain future_design")
    if node_map["diesel_backup_package"]["lifecycle"] != "permitted":
        raise ValidationError("diesel backup must remain permitted, not operational")
    if "cooling_tower" in node_ids:
        raise ValidationError("Abilene base topology cannot contain a cooling tower")
    edge_map = {edge["id"]: edge for edge in edges}
    if edge_map["fill_to_facility_loop"]["to"] != "facility_loop":
        raise ValidationError("fill/treatment must connect to the closed facility loop")
    if edge_map["nuclear_ppa_overlay"]["carries"] != "contractual_attribute":
        raise ValidationError("PPA must remain a contractual overlay, not a physical energy source")

    serialised = str(master)
    for unsupported in ("20kV", "54VDC", "480 V", "345 kV -> 34.5 kV"):
        if unsupported in serialised:
            raise ValidationError(f"unsupported exact voltage leaked into master: {unsupported}")
    return node_ids, edge_ids


def _validate_layout(
    master: dict[str, Any], layout: dict[str, Any], evidence: dict[str, Any]
) -> None:
    layout_pipeline._assert_coverage(master, layout)
    copy_ids = _copy_ids(layout)
    _unique(copy_ids, "rendered copy")
    for copy_id in copy_ids:
        layout_pipeline.resolve_copy(master, evidence, copy_id, include_hidden=True)
    hidden_copy_ids = {
        copy_id
        for copy_id, spec in master["copy"].items()
        if spec.get("base_visible", True) is False
    }
    missing_hidden_copy_ids = hidden_copy_ids - set(copy_ids)
    if missing_hidden_copy_ids:
        raise ValidationError(
            "layout missing base-hidden master copy: "
            f"{sorted(missing_hidden_copy_ids)}"
        )
    for section in ("zones", "regions", "labels", "room_labels"):
        for spec in layout.get(section) or []:
            forbidden = {"text", "title", "subtitle", "label"} & set(spec)
            if forbidden:
                raise ValidationError(f"layout.{section}: semantic copy leaked into placement: {sorted(forbidden)}")


def _validate_generated_svg(master: dict[str, Any], layout: dict[str, Any]) -> None:
    svg = (DIAGRAM / "master.svg").read_text()
    for node in master["nodes"]:
        if f'id="node-{node["id"]}"' not in svg:
            raise ValidationError(f"master.svg missing stable node ID {node['id']}")
    for edge in master["edges"]:
        if f'id="edge-{edge["id"]}"' not in svg:
            raise ValidationError(f"master.svg missing stable edge ID {edge['id']}")
    for copy_id in _copy_ids(layout):
        if f'id="label-{copy_id}"' not in svg:
            raise ValidationError(f"master.svg missing stable label ID {copy_id}")


def _validate_camera_assets(cameras: dict[str, Any]) -> None:
    for camera in cameras.get("cameras") or []:
        if asset := camera.get("map_asset"):
            path = DIAGRAM / asset
            if not path.exists():
                raise ValidationError(f"camera {camera['id']}: missing generated map asset {asset}")


def _claim_assertion_matches(assertion: str, fact: dict[str, Any]) -> bool:
    posture = fact["posture"]
    lifecycle = fact["lifecycle"]
    value = fact["value"]
    if assertion == "explicit_unknown":
        return value is None and posture == "unverified_null" and lifecycle in {
            "as_built_unknown",
            "commissioning_unknown",
            "installation_unknown",
            "operation_unknown",
            "site_configuration_unknown",
            "topology_unknown",
        }
    if assertion == "no_evidence_backed_estimate":
        return (
            value is None
            and posture == "no_evidence_backed_estimate"
            and lifecycle == "operation_unknown"
            and fact["basis"] == "no evidence-backed estimate"
        )
    if value is None:
        return False
    if assertion == "confirmed":
        return posture == "confirmed" and lifecycle in OPERATIONAL_ALLOWED_FACT_LIFECYCLES
    if assertion == "confirmed_minimum":
        return posture == "confirmed_minimum" and lifecycle in OPERATIONAL_FACT_LIFECYCLES
    if assertion == "planned":
        return lifecycle == "planned" and posture == "planned_not_operational"
    if assertion == "permitted":
        return lifecycle == "permitted" and posture == "permitted_not_observed"
    if assertion == "future_design":
        return lifecycle == "future_design" and posture == "future_design"
    if assertion == "design_reference":
        return lifecycle in {"design_reference", "review_design"} and posture in {
            "design_not_as_built",
            "design_not_observed",
        }
    if assertion == "selected_design":
        return lifecycle in {"design_requirement", "selected_design"} and posture == "design_selected"
    if assertion == "product_reference":
        return lifecycle == "product_documented" and posture in {
            "confirmed_model_spec",
            "model_range_not_site_configured",
        }
    if assertion == "anticipated":
        return lifecycle == "anticipated_maintenance" and posture == "anticipated_not_observed"
    if assertion == "live_by":
        return lifecycle == "operating" and posture == "live_by_not_start_date"
    if assertion == "reported_untyped":
        return lifecycle == "delivered_untyped" and posture == "reported_untyped"
    if assertion == "excluded_scope":
        return lifecycle == "planned" and posture == "excluded_scope"
    return False


def _validate_course(
    course: dict[str, Any],
    master: dict[str, Any],
    evidence_ledgers: dict[str, dict[str, Any]],
    cameras: dict[str, Any],
) -> dict[str, int]:
    if course.get("schema_version") != 2:
        raise ValidationError("course schema_version must be 2")
    if set(course) != {"schema_version", "meta", "acts"}:
        raise ValidationError("course root must contain only schema_version, meta, and acts")

    meta = course.get("meta")
    if not isinstance(meta, dict):
        raise ValidationError("course.meta: expected a mapping")
    _exact_fields(meta, COURSE_META_FIELDS, "course.meta")
    if meta["course_id"] != "gigawatt":
        raise ValidationError("course.meta.course_id must be gigawatt")
    if meta["inventory_scope"] != "complete_course":
        raise ValidationError("course inventory_scope must be complete_course")
    if meta["runtime_minutes"] is not None:
        raise ValidationError("course runtime remains unset until editorial review")
    for field, expected in (
        ("master", "diagram/master.yaml"),
        ("cameras", "diagram/cameras.yaml"),
    ):
        if meta[field] != expected:
            raise ValidationError(f"course.meta.{field} must reference {expected}")
    ledger_paths = _course_ledger_registry(meta)
    if set(evidence_ledgers) != set(ledger_paths):
        raise ValidationError(
            "course evidence ledger payloads must exactly match the registered ledger IDs"
        )
    for ledger_id, ledger in evidence_ledgers.items():
        _validate_evidence_schema(ledger, f"evidence ledger {ledger_id}")
    master_ledger_id = meta["master_evidence_ledger"]
    if Path(master["meta"]["evidence_file"]) != ledger_paths[master_ledger_id].relative_to(ROOT):
        raise ValidationError(
            "course master evidence ledger must point to master.meta.evidence_file"
        )
    _nonempty_string(meta["status"], "course.meta.status")
    _nonempty_string(meta["sequence_rule"], "course.meta.sequence_rule")
    relative_weight_total = meta["relative_weight_total"]
    if (
        isinstance(relative_weight_total, bool)
        or not isinstance(relative_weight_total, (int, float))
        or not math.isfinite(float(relative_weight_total))
    ):
        raise ValidationError("course.meta.relative_weight_total must be finite numeric")

    master_nodes = {node["id"]: node for node in master["nodes"]}
    master_edges = {edge["id"]: edge for edge in master["edges"]}
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    globally_bound_fact_refs = {
        f"{master_ledger_id}:{fact_id}"
        for record in [*master["nodes"], *master["edges"]]
        for fact_id in record.get("fact_ids") or []
    }

    acts = course.get("acts")
    if not isinstance(acts, list) or not acts:
        raise ValidationError("course.acts must be a non-empty list")
    act_ids: list[str] = []
    segment_ids: list[str] = []
    segments: list[dict[str, Any]] = []
    planned_shots: list[str] = []
    covered_nodes: set[str] = set()
    covered_edges: set[str] = set()
    total_weight = 0.0
    readiness_counts = {readiness: 0 for readiness in SEGMENT_READINESS}

    for act_index, act in enumerate(acts):
        location = f"course.acts[{act_index}]"
        if not isinstance(act, dict):
            raise ValidationError(f"{location}: expected a mapping")
        _exact_fields(act, ACT_FIELDS, location)
        _nonempty_string(act["id"], f"{location}.id")
        _nonempty_string(act["title"], f"{location}.title")
        _nonempty_string(act["learning_objective"], f"{location}.learning_objective")
        act_ids.append(act["id"])
        if not isinstance(act["segments"], list) or not act["segments"]:
            raise ValidationError(f"{location}.segments must be a non-empty list")

        for segment_index, segment in enumerate(act["segments"]):
            segment_location = f"{location}.segments[{segment_index}]"
            if not isinstance(segment, dict):
                raise ValidationError(f"{segment_location}: expected a mapping")
            _exact_fields(segment, SEGMENT_FIELDS, segment_location)
            for field in ("id", "title", "opening_question", "learning_objective"):
                _nonempty_string(segment[field], f"{segment_location}.{field}")
            segment_ids.append(segment["id"])
            segments.append(segment)

            weight = segment["weight"]
            if (
                isinstance(weight, bool)
                or not isinstance(weight, (int, float))
                or not math.isfinite(float(weight))
                or weight <= 0
            ):
                raise ValidationError(f"{segment_location}.weight must be positive and finite")
            total_weight += float(weight)
            _string_list(segment["depends_on"], f"{segment_location}.depends_on")

            camera = segment["camera"]
            if not isinstance(camera, dict):
                raise ValidationError(f"{segment_location}.camera: expected a mapping")
            _exact_fields(camera, SEGMENT_CAMERA_FIELDS, f"{segment_location}.camera")
            anchor_id = camera["anchor"]
            _nonempty_string(anchor_id, f"{segment_location}.camera.anchor")
            if anchor_id not in camera_map:
                raise ValidationError(f"segment {segment['id']}: unknown camera anchor {anchor_id!r}")
            _nonempty_string(camera["mode"], f"{segment_location}.camera.mode")
            if camera["mode"] not in scene_pipeline.ALLOWED_MODES:
                raise ValidationError(f"segment {segment['id']}: invalid camera mode {camera['mode']!r}")
            _nonempty_string(camera["status"], f"{segment_location}.camera.status")
            if camera["status"] not in SEGMENT_CAMERA_STATUS:
                raise ValidationError(f"segment {segment['id']}: invalid camera status {camera['status']!r}")
            _nonempty_string(camera["shot"], f"{segment_location}.camera.shot")
            reveal_ids = _string_list(
                camera["reveal_ids"], f"{segment_location}.camera.reveal_ids"
            )
            reveal_copy_ids = _string_list(
                camera["reveal_copy_ids"],
                f"{segment_location}.camera.reveal_copy_ids",
            )

            node_ids = segment["node_ids"]
            edge_ids = segment["edge_ids"]
            selected_nodes = _string_list(
                node_ids,
                f"segment {segment['id']}.node_ids",
                allow_empty=False,
            )
            selected_edges = _string_list(
                edge_ids,
                f"segment {segment['id']}.edge_ids",
            )
            unknown_nodes = selected_nodes - set(master_nodes)
            unknown_edges = selected_edges - set(master_edges)
            if unknown_nodes or unknown_edges:
                raise ValidationError(
                    f"segment {segment['id']}: unknown_nodes={sorted(unknown_nodes)} "
                    f"unknown_edges={sorted(unknown_edges)}"
                )
            incomplete_edges = sorted(
                edge_id
                for edge_id in selected_edges
                if {
                    master_edges[edge_id]["from"],
                    master_edges[edge_id]["to"],
                }
                - selected_nodes
            )
            if incomplete_edges:
                raise ValidationError(
                    f"segment {segment['id']}: edge endpoints absent for {incomplete_edges}"
                )

            hidden_selected = {
                node_id
                for node_id in selected_nodes
                if master_nodes[node_id].get("base_visible", True) is False
            } | {
                edge_id
                for edge_id in selected_edges
                if master_edges[edge_id].get("base_visible", True) is False
            }
            hidden_selected_records = [
                master_nodes[node_id]
                for node_id in selected_nodes
                if node_id in hidden_selected
            ] + [
                master_edges[edge_id]
                for edge_id in selected_edges
                if edge_id in hidden_selected
            ]
            expected_reveal_copy_ids = {
                copy_id
                for record in hidden_selected_records
                for copy_id in record.get("reveal_copy_ids", [])
            }

            if camera["status"] == "existing":
                if reveal_ids or reveal_copy_ids:
                    raise ValidationError(
                        f"segment {segment['id']}: existing camera cannot request hidden reveals"
                    )
                anchor = camera_map[anchor_id]
                if camera["shot"] != anchor_id or camera["mode"] != anchor["mode"]:
                    raise ValidationError(
                        f"segment {segment['id']}: existing shot must equal its anchor and mode"
                    )
                anchor_nodes = set(anchor.get("focus_nodes") or [])
                anchor_edges = set(anchor.get("focus_edges") or [])
                if (anchor_nodes and not selected_nodes <= anchor_nodes) or (
                    anchor_edges and not selected_edges <= anchor_edges
                ):
                    raise ValidationError(
                        f"segment {segment['id']}: focus exceeds existing camera {anchor_id}"
                    )
                if hidden_selected:
                    raise ValidationError(
                        f"segment {segment['id']}: existing camera cannot reveal hidden "
                        f"IDs={sorted(hidden_selected)}"
                    )
            else:
                if camera["shot"] == anchor_id:
                    raise ValidationError(
                        f"segment {segment['id']}: planned shot must have a new shot ID"
                    )
                if reveal_ids != hidden_selected:
                    raise ValidationError(
                        f"segment {segment['id']}: planned reveal_ids must exactly match "
                        f"selected hidden IDs {sorted(hidden_selected)}"
                    )
                if reveal_copy_ids != expected_reveal_copy_ids:
                    raise ValidationError(
                        f"segment {segment['id']}: planned reveal_copy_ids must exactly "
                        "match selected hidden copy IDs "
                        f"{sorted(expected_reveal_copy_ids)}"
                    )
                planned_shots.append(camera["shot"])

            segment_evidence = segment["evidence"]
            if not isinstance(segment_evidence, dict):
                raise ValidationError(f"{segment_location}.evidence: expected a mapping")
            _exact_fields(
                segment_evidence,
                SEGMENT_EVIDENCE_FIELDS,
                f"{segment_location}.evidence",
            )
            readiness = segment_evidence["readiness"]
            _nonempty_string(readiness, f"{segment_location}.evidence.readiness")
            if readiness not in SEGMENT_READINESS:
                raise ValidationError(f"segment {segment['id']}: invalid readiness {readiness!r}")
            readiness_counts[readiness] += 1

            claims = segment_evidence["claims"]
            blockers = segment_evidence["blocking_research"]
            guards = segment_evidence["promotion_guards"]
            if not isinstance(claims, list):
                raise ValidationError(f"segment {segment['id']}: claims must be a list")
            if not isinstance(blockers, list) or any(
                not isinstance(item, str) or not item.strip() for item in blockers
            ):
                raise ValidationError(
                    f"segment {segment['id']}: blocking_research must be a string list"
                )
            invalid_blockers = [
                item
                for item in blockers
                if len(item.strip()) < 20
                or item.strip().casefold().rstrip(".?!") in BLOCKER_PLACEHOLDERS
                or item.strip()[-1] not in ".?!"
            ]
            if invalid_blockers:
                raise ValidationError(
                    f"segment {segment['id']}: blocking_research contains placeholders "
                    f"or underspecified items {invalid_blockers}"
                )
            guard_set = _string_list(
                guards,
                f"segment {segment['id']}.promotion_guards",
                allow_empty=False,
            )
            unknown_guards = guard_set - PROMOTION_GUARDS
            if unknown_guards:
                raise ValidationError(
                    f"segment {segment['id']}: unknown promotion guards {sorted(unknown_guards)}"
                )
            if readiness == "evidence_ready" and (blockers or not claims):
                raise ValidationError(
                    f"segment {segment['id']}: evidence_ready requires claims and no blockers"
                )
            if readiness == "research_required" and not blockers:
                raise ValidationError(
                    f"segment {segment['id']}: research_required needs blocking research"
                )

            selected_fact_refs = {
                f"{master_ledger_id}:{fact_id}"
                for record_id in selected_nodes
                for fact_id in master_nodes[record_id].get("fact_ids") or []
            } | {
                f"{master_ledger_id}:{fact_id}"
                for record_id in selected_edges
                for fact_id in master_edges[record_id].get("fact_ids") or []
            }
            claim_ids: list[str] = []
            claimed_fact_refs: list[str] = []
            required_guards: set[str] = set()
            for claim_index, claim in enumerate(claims):
                claim_location = f"{segment_location}.evidence.claims[{claim_index}]"
                if not isinstance(claim, dict):
                    raise ValidationError(f"{claim_location}: expected a mapping")
                _exact_fields(claim, SEGMENT_CLAIM_FIELDS, claim_location)
                _nonempty_string(claim["id"], f"{claim_location}.id")
                claim_ids.append(claim["id"])
                assertion = claim["assertion"]
                _nonempty_string(assertion, f"{claim_location}.assertion")
                if assertion not in SEGMENT_ASSERTIONS:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: invalid assertion {assertion!r}"
                    )
                binding = claim["binding"]
                _nonempty_string(binding, f"{claim_location}.binding")
                if binding not in SEGMENT_CLAIM_BINDINGS:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: invalid binding {binding!r}"
                    )
                fact_refs = claim["fact_refs"]
                _string_list(
                    fact_refs,
                    f"{claim_location}.fact_refs",
                    allow_empty=False,
                )
                claimed_fact_refs.extend(fact_refs)
                resolved = [
                    _resolve_fact_ref(fact_ref, evidence_ledgers, claim_location)
                    for fact_ref in fact_refs
                ]
                if binding == "topology":
                    misplaced = sorted(set(fact_refs) - selected_fact_refs)
                    if misplaced:
                        raise ValidationError(
                            f"segment {segment['id']} claim {claim['id']}: topology facts "
                            f"are not bound to selected topology {misplaced}"
                        )
                else:
                    master_bound = sorted(set(fact_refs) & globally_bound_fact_refs)
                    if master_bound:
                        raise ValidationError(
                            f"segment {segment['id']} claim {claim['id']}: overlay cannot "
                            f"bypass master topology binding {master_bound}"
                        )
                    if any(ledger_id != master_ledger_id for ledger_id, _, _ in resolved) and (
                        "site_scope_transfer" not in guard_set
                    ):
                        raise ValidationError(
                            f"segment {segment['id']} claim {claim['id']}: external-ledger "
                            "overlay requires site_scope_transfer"
                        )

                incompatible = sorted(
                    fact_ref
                    for fact_ref, (_, _, fact) in zip(fact_refs, resolved)
                    if not _claim_assertion_matches(assertion, fact)
                )
                if incompatible:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: facts {incompatible} "
                        f"cannot support assertion {assertion!r}"
                    )

                numeric_scopes_by_unit: dict[str, set[str]] = {}
                for _, _, fact in resolved:
                    value = fact["value"]
                    unit = fact["unit"]
                    if isinstance(value, (int, float)) and not isinstance(value, bool) and unit:
                        numeric_scopes_by_unit.setdefault(str(unit), set()).add(fact["scope"])
                additive_scope_collisions = {
                    unit: scopes
                    for unit, scopes in numeric_scopes_by_unit.items()
                    if len(scopes) > 1
                }
                if additive_scope_collisions:
                    raise ValidationError(
                        f"segment {segment['id']} claim {claim['id']}: one claim cannot "
                        f"combine same-unit numeric facts across scopes {additive_scope_collisions}"
                    )
                required_guards.update(ASSERTION_REQUIRED_GUARDS.get(assertion, set()))
            _unique(claim_ids, f"segment {segment['id']}.claim IDs")
            _unique(claimed_fact_refs, f"segment {segment['id']}.claimed fact references")
            missing_guards = required_guards - guard_set
            if missing_guards:
                raise ValidationError(
                    f"segment {segment['id']}: missing assertion promotion guards "
                    f"{sorted(missing_guards)}"
                )

            covered_nodes.update(selected_nodes)
            covered_edges.update(selected_edges)

    _unique(act_ids, "course act IDs")
    _unique(segment_ids, "course segment IDs")
    _unique(planned_shots, "course planned shot IDs")
    segment_index = {segment_id: index for index, segment_id in enumerate(segment_ids)}
    segment_readiness = {
        segment["id"]: segment["evidence"]["readiness"] for segment in segments
    }
    for index, segment in enumerate(segments):
        dependencies = set(segment["depends_on"])
        unavailable = sorted(
            dependency
            for dependency in dependencies
            if dependency not in segment_index or segment_index[dependency] >= index
        )
        if unavailable:
            raise ValidationError(
                f"segment {segment['id']}: dependencies must name earlier segments {unavailable}"
            )
        gated_dependencies = sorted(
            dependency
            for dependency in dependencies
            if segment_readiness[dependency] != "evidence_ready"
        )
        if segment_readiness[segment["id"]] == "evidence_ready" and gated_dependencies:
            raise ValidationError(
                f"segment {segment['id']}: evidence_ready cannot depend on research-gated "
                f"segments {gated_dependencies}"
            )
    shot_collisions = sorted(set(planned_shots) & set(camera_map))
    if shot_collisions:
        raise ValidationError(
            f"course planned shot IDs collide with existing cameras: {shot_collisions}"
        )
    if not math.isclose(
        total_weight,
        float(meta["relative_weight_total"]),
        rel_tol=0.0,
        abs_tol=1e-9,
    ):
        raise ValidationError(
            f"course relative weight mismatch: declared {meta['relative_weight_total']}, "
            f"computed {total_weight}"
        )

    for index, segment in enumerate(segments):
        transition = segment["transition"]
        if index == len(segments) - 1:
            if transition is not None:
                raise ValidationError("final course segment transition must be null")
            continue
        if not isinstance(transition, dict):
            raise ValidationError(f"segment {segment['id']}: transition must be a mapping")
        _exact_fields(transition, SEGMENT_TRANSITION_FIELDS, f"segment {segment['id']}.transition")
        _nonempty_string(transition["cue"], f"segment {segment['id']}.transition.cue")
        expected = segments[index + 1]["id"]
        if transition["to"] != expected:
            raise ValidationError(
                f"segment {segment['id']}: transition must target next segment {expected!r}"
            )

    visible_nodes = {
        node_id
        for node_id, node in master_nodes.items()
        if node.get("base_visible", True) is not False
    }
    visible_edges = {
        edge_id
        for edge_id, edge in master_edges.items()
        if edge.get("base_visible", True) is not False
    }
    missing_nodes = sorted(visible_nodes - covered_nodes)
    missing_edges = sorted(visible_edges - covered_edges)
    if missing_nodes or missing_edges:
        raise ValidationError(
            "complete course coverage mismatch: "
            f"missing_nodes={missing_nodes} missing_edges={missing_edges}"
        )

    return {
        "acts": len(acts),
        "segments": len(segments),
        "evidence_ready_segments": readiness_counts["evidence_ready"],
        "research_required_segments": readiness_counts["research_required"],
        "planned_shots": len(planned_shots),
    }


def validate_project() -> dict[str, Any]:
    master = _load_yaml_strict(DIAGRAM / "master.yaml")
    layout = _load_yaml_strict(DIAGRAM / "layout.yaml")
    evidence = _load_yaml_strict(EVIDENCE)
    scene = _load_yaml_strict(DIAGRAM / "scene.yaml")
    cameras = _load_yaml_strict(DIAGRAM / "cameras.yaml")
    course = _load_yaml_strict(COURSE)
    course_ledgers = _load_course_evidence_ledgers(course)

    source_ids, fact_ids = _validate_evidence(evidence)
    node_ids, edge_ids = _validate_master(master, evidence, source_ids)
    _validate_layout(master, layout, evidence)
    scene_pipeline.validate(master, scene, cameras)
    _validate_generated_svg(master, layout)
    _validate_camera_assets(cameras)
    course_result = _validate_course(course, master, course_ledgers, cameras)

    html, digest = scene_pipeline.generate()
    if html != (DIAGRAM / "hybrid.html").read_text():
        raise ValidationError("hybrid.html is stale; run gigawatt-scene")
    return {
        "sources": len(source_ids),
        "facts": len(fact_ids),
        "nodes": len(node_ids),
        "edges": len(edge_ids),
        "cameras": len(cameras["cameras"]),
        "hybrid_digest": digest,
        **course_result,
    }


def main() -> None:
    result = validate_project()
    print(
        "validated "
        f"{result['sources']} sources · {result['facts']} facts · "
        f"{result['nodes']} nodes · {result['edges']} edges · "
        f"{result['cameras']} cameras · {result['acts']} acts · "
        f"{result['segments']} segments "
        f"({result['evidence_ready_segments']} evidence-ready / "
        f"{result['research_required_segments']} research-gated) · "
        f"{result['planned_shots']} planned shots · hybrid {result['hybrid_digest']}"
    )


if __name__ == "__main__":
    main()
