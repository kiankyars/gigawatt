"""Fail-closed validation for the evidence, 2D, 3D, and camera manifests."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable

import yaml

from . import layout as layout_pipeline
from . import scene as scene_pipeline
from . import tokens

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
EVIDENCE = ROOT / "evidence" / "abilene.yaml"

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


def _validate_evidence(evidence: dict[str, Any]) -> tuple[set[str], set[str]]:
    if evidence.get("schema_version") != 1:
        raise ValidationError("evidence schema_version must be 1")
    if evidence.get("accessed_as_of") != "2026-08-25":
        raise ValidationError("evidence accessed_as_of must be 2026-08-25")
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
    ):
        if facts[null_fact]["value"] is not None:
            raise ValidationError(f"{null_fact} must remain null until new primary evidence is added")
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
        layout_pipeline.resolve_copy(master, evidence, copy_id)
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
        if master["copy"][copy_id].get("base_visible", True) is False:
            continue
        if f'id="label-{copy_id}"' not in svg:
            raise ValidationError(f"master.svg missing stable label ID {copy_id}")


def _validate_camera_assets(cameras: dict[str, Any]) -> None:
    for camera in cameras.get("cameras") or []:
        if asset := camera.get("map_asset"):
            path = DIAGRAM / asset
            if not path.exists():
                raise ValidationError(f"camera {camera['id']}: missing generated map asset {asset}")


def validate_project() -> dict[str, Any]:
    master = _load_yaml_strict(DIAGRAM / "master.yaml")
    layout = _load_yaml_strict(DIAGRAM / "layout.yaml")
    evidence = _load_yaml_strict(EVIDENCE)
    scene = _load_yaml_strict(DIAGRAM / "scene.yaml")
    cameras = _load_yaml_strict(DIAGRAM / "cameras.yaml")

    source_ids, fact_ids = _validate_evidence(evidence)
    node_ids, edge_ids = _validate_master(master, evidence, source_ids)
    _validate_layout(master, layout, evidence)
    scene_pipeline.validate(master, scene, cameras)
    _validate_generated_svg(master, layout)
    _validate_camera_assets(cameras)

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
    }


def main() -> None:
    result = validate_project()
    print(
        "validated "
        f"{result['sources']} sources · {result['facts']} facts · "
        f"{result['nodes']} nodes · {result['edges']} edges · "
        f"{result['cameras']} cameras · hybrid {result['hybrid_digest']}"
    )


if __name__ == "__main__":
    main()
