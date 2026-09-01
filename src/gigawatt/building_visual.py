"""Evidence-bound Phase 4 building-power teaching surface.

The manifest is deliberately stricter than a general diagram schema.  It owns
six instructor-selected teaching states and keeps generic building functions,
conditional A/B reasoning, and Abilene evidence in visibly different layers.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from gigawatt import teaching_visuals as base

SCHEMA_VERSION = 1
CANVAS_KIND = "building_power_path_v1"
CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 900
STATE_IDS = [
    "building_cutaway",
    "equipment_by_verb",
    "generic_ab_paths",
    "one_path_unavailable",
    "abilene_boundary",
    "rack_power_handoff",
]
ZONE_IDS = ["campus_entry", "electrical_space", "data_hall"]
CHAIN_STEP_IDS = [
    "campus_feeder",
    "unit_substation",
    "switchgear",
    "ups",
    "busway",
    "rack_position",
]
PROTECTED_PATH_IDS = ["path_a", "path_b"]
ISOLATION_STATE_IDS = ["isolated_path_a", "remaining_path_b", "rack_result"]
ABILENE_KNOWN_IDS = ["first_phase_electrical_delivery", "rack_family_delivery"]
ABILENE_UNKNOWN_IDS = ["campus_input", "internal_power_train"]

TOP_LEVEL_FIELDS = {
    "schema_version",
    "id",
    "title",
    "phase",
    "learning_objective",
    "evidence_files",
    "interaction",
    "canvas",
    "spatial_building_zones",
    "functional_power_chain",
    "generic_protected_paths",
    "conditional_path_isolation",
    "abilene_mapping",
    "phase5_handoff",
    "evidence_gaps",
    "states",
}
PHASE_FIELDS = {"id", "number", "title", "anchor_question"}
CANVAS_FIELDS = {"kind", "width", "height", "contract"}
CONTRACT_FIELDS = {
    "state_selection",
    "primary_layers",
    "evidence_binding",
    "geometry_owner",
    "handoff_requires",
}
SECTION_FIELDS = {"title", "body"}
ZONES_FIELDS = SECTION_FIELDS | {"zones", "cutaway_boundary"}
ZONE_FIELDS = {"id", "title", "contains", "boundary", "fact_refs"}
CHAIN_FIELDS = SECTION_FIELDS | {"steps", "chain_boundary"}
CHAIN_STEP_FIELDS = {"id", "title", "verb", "evidence_posture", "fact_refs"}
CHAIN_STEP_WITH_BOUNDARY_FIELDS = CHAIN_STEP_FIELDS | {"boundary"}
PATHS_FIELDS = SECTION_FIELDS | {
    "paths",
    "load_interfaces",
    "protected_path_boundary",
}
PATH_FIELDS = {"id", "title", "elements", "visual_posture", "fact_refs"}
ISOLATION_FIELDS = SECTION_FIELDS | {
    "path_states",
    "claim_split",
    "isolation_boundary",
}
ISOLATED_PATH_FIELDS = {
    "id",
    "title",
    "visual_posture",
    "causes",
    "boundary",
    "fact_refs",
}
REMAINING_PATH_FIELDS = {
    "id",
    "title",
    "visual_posture",
    "boundary",
    "fact_refs",
}
RACK_RESULT_FIELDS = {
    "id",
    "title",
    "visual_posture",
    "body",
    "fact_refs",
}
CARD_FIELDS = {"id", "title", "body", "fact_refs"}
BOUNDARY_FIELDS = CARD_FIELDS
CHAIN_BOUNDARY_FIELDS = {"id", "body", "fact_refs"}
ABILENE_FIELDS = SECTION_FIELDS | {"known", "unknown", "mapping_guard"}
HANDOFF_FIELDS = {"title", "body", "known", "unknown"}
HANDOFF_CARD_FIELDS = {"id", "body", "fact_refs"}
GAP_FIELDS = {"id", "gap", "renderer_guard", "related_fact_refs"}
STATE_FIELDS = {
    "id",
    "nav_label",
    "title",
    "instruction",
    "zone_ids",
    "chain_step_ids",
    "protected_path_ids",
    "isolation_path_state_ids",
    "abilene_known_ids",
    "abilene_unknown_ids",
    "show_phase5_handoff",
}


class BuildingVisualError(base.TeachingVisualError):
    """Raised when Phase 4 escapes its teaching or evidence contract."""


def responsive_layout_contract(
    viewport_width: int,
    viewport_height: int,
) -> dict[str, Any]:
    """Choose the SVG or readable payload-driven teaching surface."""
    if 901 <= viewport_width <= 1100:
        return {
            "surface": "html",
            "profile": "tablet",
            "columns": 2,
            "minimum_text_px": 12,
            "scroll_axis": "vertical",
        }
    return base.responsive_layout_contract(viewport_width, viewport_height)


def _exact(value: Any, fields: set[str], location: str) -> dict[str, Any]:
    try:
        return base._exact_fields(value, fields, location)
    except base.TeachingVisualError as error:
        raise BuildingVisualError(str(error)) from error


def _text(value: Any, location: str, *, maximum: int = 240) -> str:
    try:
        return base._text(value, location, maximum=maximum)
    except base.TeachingVisualError as error:
        raise BuildingVisualError(str(error)) from error


def _identifier(value: Any, location: str) -> str:
    try:
        return base._id(value, location)
    except base.TeachingVisualError as error:
        raise BuildingVisualError(str(error)) from error


def _list(
    value: Any,
    location: str,
    *,
    minimum: int,
    maximum: int,
    item_limit: int = 180,
) -> list[str]:
    try:
        return base._unique_text_list(
            value,
            location,
            minimum=minimum,
            maximum=maximum,
            item_limit=item_limit,
        )
    except base.TeachingVisualError as error:
        raise BuildingVisualError(str(error)) from error


def _refs(
    value: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[str]:
    try:
        return base._fact_refs(value, location, ledgers)
    except base.TeachingVisualError as error:
        raise BuildingVisualError(str(error)) from error


def _normalize_card(
    raw: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
    *,
    fields: set[str] = CARD_FIELDS,
) -> dict[str, Any]:
    value = _exact(raw, fields, location)
    result: dict[str, Any] = {
        "id": _identifier(value["id"], f"{location}.id"),
        "fact_refs": _refs(value["fact_refs"], f"{location}.fact_refs", ledgers),
    }
    for key in ("title", "body", "boundary", "gap", "renderer_guard"):
        if key in value:
            result[key] = _text(value[key], f"{location}.{key}", maximum=760)
    for key in ("visual_posture", "evidence_posture"):
        if key in value:
            result[key] = _identifier(value[key], f"{location}.{key}")
    return result


def _normalize_card_list(
    raw: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
    *,
    expected_ids: list[str],
    fields: set[str] = CARD_FIELDS,
) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(expected_ids):
        raise BuildingVisualError(
            f"{location} must contain exactly {len(expected_ids)} records"
        )
    records = [
        _normalize_card(item, f"{location}[{index}]", ledgers, fields=fields)
        for index, item in enumerate(raw)
    ]
    ids = [record["id"] for record in records]
    if ids != expected_ids:
        raise BuildingVisualError(
            f"{location} must remain in canonical order {expected_ids}"
        )
    return records


def _section_heading(value: Mapping[str, Any], location: str) -> dict[str, str]:
    return {
        "title": _text(value["title"], f"{location}.title", maximum=180),
        "body": _text(value["body"], f"{location}.body", maximum=760),
    }


def _normalize_zones(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.spatial_building_zones"
    value = _exact(raw, ZONES_FIELDS, location)
    if not isinstance(value["zones"], list) or len(value["zones"]) != len(ZONE_IDS):
        raise BuildingVisualError(f"{location}.zones must contain three zones")
    zones = []
    for index, raw_zone in enumerate(value["zones"]):
        zone_location = f"{location}.zones[{index}]"
        zone = _exact(raw_zone, ZONE_FIELDS, zone_location)
        zones.append(
            {
                "id": _identifier(zone["id"], f"{zone_location}.id"),
                "title": _text(zone["title"], f"{zone_location}.title", maximum=120),
                "contains": _list(
                    zone["contains"],
                    f"{zone_location}.contains",
                    minimum=2,
                    maximum=4,
                    item_limit=140,
                ),
                "boundary": _text(
                    zone["boundary"], f"{zone_location}.boundary", maximum=640
                ),
                "fact_refs": _refs(
                    zone["fact_refs"], f"{zone_location}.fact_refs", ledgers
                ),
            }
        )
    if [record["id"] for record in zones] != ZONE_IDS:
        raise BuildingVisualError(f"{location}.zones must remain in canonical order")
    boundary = _normalize_card(
        value["cutaway_boundary"],
        f"{location}.cutaway_boundary",
        ledgers,
        fields=BOUNDARY_FIELDS,
    )
    return {**_section_heading(value, location), "zones": zones, "boundary": boundary}


def _normalize_chain(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.functional_power_chain"
    value = _exact(raw, CHAIN_FIELDS, location)
    if not isinstance(value["steps"], list) or len(value["steps"]) != len(
        CHAIN_STEP_IDS
    ):
        raise BuildingVisualError(f"{location}.steps must contain six steps")
    steps = []
    for index, raw_step in enumerate(value["steps"]):
        step_location = f"{location}.steps[{index}]"
        fields = (
            CHAIN_STEP_WITH_BOUNDARY_FIELDS
            if raw_step.get("id") == "ups"
            else CHAIN_STEP_FIELDS
        )
        step = _exact(raw_step, fields, step_location)
        normalized = {
            "id": _identifier(step["id"], f"{step_location}.id"),
            "title": _text(step["title"], f"{step_location}.title", maximum=120),
            "verb": _text(step["verb"], f"{step_location}.verb", maximum=300),
            "evidence_posture": _identifier(
                step["evidence_posture"], f"{step_location}.evidence_posture"
            ),
            "fact_refs": _refs(
                step["fact_refs"], f"{step_location}.fact_refs", ledgers
            ),
        }
        if "boundary" in step:
            normalized["boundary"] = _text(
                step["boundary"], f"{step_location}.boundary", maximum=640
            )
        steps.append(normalized)
    if [record["id"] for record in steps] != CHAIN_STEP_IDS:
        raise BuildingVisualError(f"{location}.steps must remain in canonical order")
    boundary = _normalize_card(
        value["chain_boundary"],
        f"{location}.chain_boundary",
        ledgers,
        fields=CHAIN_BOUNDARY_FIELDS,
    )
    return {**_section_heading(value, location), "steps": steps, "boundary": boundary}


def _normalize_paths(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.generic_protected_paths"
    value = _exact(raw, PATHS_FIELDS, location)
    if not isinstance(value["paths"], list) or len(value["paths"]) != 2:
        raise BuildingVisualError(f"{location}.paths must contain Path A and Path B")
    paths = []
    for index, raw_path in enumerate(value["paths"]):
        path_location = f"{location}.paths[{index}]"
        path = _exact(raw_path, PATH_FIELDS, path_location)
        paths.append(
            {
                "id": _identifier(path["id"], f"{path_location}.id"),
                "title": _text(path["title"], f"{path_location}.title", maximum=80),
                "elements": _list(
                    path["elements"],
                    f"{path_location}.elements",
                    minimum=4,
                    maximum=4,
                    item_limit=150,
                ),
                "visual_posture": _identifier(
                    path["visual_posture"], f"{path_location}.visual_posture"
                ),
                "fact_refs": _refs(
                    path["fact_refs"], f"{path_location}.fact_refs", ledgers
                ),
            }
        )
    if [record["id"] for record in paths] != PROTECTED_PATH_IDS:
        raise BuildingVisualError(f"{location}.paths must remain Path A then Path B")
    load_interfaces = _normalize_card_list(
        value["load_interfaces"],
        f"{location}.load_interfaces",
        ledgers,
        expected_ids=["compatible_dual_input_load", "single_input_load"],
    )
    boundary = _normalize_card(
        value["protected_path_boundary"],
        f"{location}.protected_path_boundary",
        ledgers,
    )
    return {
        **_section_heading(value, location),
        "paths": paths,
        "load_interfaces": load_interfaces,
        "boundary": boundary,
    }


def _normalize_isolation(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.conditional_path_isolation"
    value = _exact(raw, ISOLATION_FIELDS, location)
    if not isinstance(value["path_states"], list) or len(value["path_states"]) != 3:
        raise BuildingVisualError(f"{location}.path_states must contain three states")
    fields_by_id = {
        "isolated_path_a": ISOLATED_PATH_FIELDS,
        "remaining_path_b": REMAINING_PATH_FIELDS,
        "rack_result": RACK_RESULT_FIELDS,
    }
    path_states = []
    for index, raw_state in enumerate(value["path_states"]):
        state_location = f"{location}.path_states[{index}]"
        state_id = raw_state.get("id") if isinstance(raw_state, dict) else None
        fields = fields_by_id.get(state_id)
        if fields is None:
            raise BuildingVisualError(f"{state_location}: unknown isolation state")
        state = _exact(raw_state, fields, state_location)
        normalized = _normalize_card(
            {key: nested for key, nested in state.items() if key != "causes"},
            state_location,
            ledgers,
            fields=fields - {"causes"},
        )
        if "causes" in state:
            normalized["causes"] = _list(
                state["causes"],
                f"{state_location}.causes",
                minimum=2,
                maximum=2,
                item_limit=120,
            )
        path_states.append(normalized)
    if [record["id"] for record in path_states] != ISOLATION_STATE_IDS:
        raise BuildingVisualError(
            f"{location}.path_states must remain in canonical order"
        )
    claim_split = _normalize_card_list(
        value["claim_split"],
        f"{location}.claim_split",
        ledgers,
        expected_ids=["planned_maintenance", "unplanned_fault"],
    )
    boundary = _normalize_card(
        value["isolation_boundary"],
        f"{location}.isolation_boundary",
        ledgers,
    )
    return {
        **_section_heading(value, location),
        "path_states": path_states,
        "claim_split": claim_split,
        "boundary": boundary,
    }


def _normalize_abilene(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.abilene_mapping"
    value = _exact(raw, ABILENE_FIELDS, location)
    known = _normalize_card_list(
        value["known"],
        f"{location}.known",
        ledgers,
        expected_ids=ABILENE_KNOWN_IDS,
    )
    unknown = _normalize_card_list(
        value["unknown"],
        f"{location}.unknown",
        ledgers,
        expected_ids=ABILENE_UNKNOWN_IDS,
    )
    guard = _normalize_card(
        value["mapping_guard"], f"{location}.mapping_guard", ledgers
    )
    return {
        **_section_heading(value, location),
        "known": known,
        "unknown": unknown,
        "guard": guard,
    }


def _normalize_handoff(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.phase5_handoff"
    value = _exact(raw, HANDOFF_FIELDS, location)
    known = _normalize_card_list(
        value["known"],
        f"{location}.known",
        ledgers,
        expected_ids=["product_and_design_reference", "rack_conversion_reference"],
        fields=HANDOFF_CARD_FIELDS,
    )
    unknown = _normalize_card_list(
        value["unknown"],
        f"{location}.unknown",
        ledgers,
        expected_ids=["site_rack_electrical_configuration"],
        fields=HANDOFF_CARD_FIELDS,
    )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=180),
        "body": _text(value["body"], f"{location}.body", maximum=760),
        "known": known,
        "unknown": unknown,
    }


def _normalize_gaps(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    location = "pilot manifest.evidence_gaps"
    if not isinstance(raw, list) or len(raw) != 2:
        raise BuildingVisualError(f"{location} must contain two renderer guards")
    gaps = []
    for index, raw_gap in enumerate(raw):
        gap_location = f"{location}[{index}]"
        value = _exact(raw_gap, GAP_FIELDS, gap_location)
        gaps.append(
            {
                "id": _identifier(value["id"], f"{gap_location}.id"),
                "gap": _text(value["gap"], f"{gap_location}.gap", maximum=760),
                "renderer_guard": _text(
                    value["renderer_guard"],
                    f"{gap_location}.renderer_guard",
                    maximum=520,
                ),
                "related_fact_refs": _refs(
                    value["related_fact_refs"],
                    f"{gap_location}.related_fact_refs",
                    ledgers,
                ),
            }
        )
    expected = [
        "generic_reference_is_not_coordination_design",
        "abilene_building_power_train_unpublished",
    ]
    if [record["id"] for record in gaps] != expected:
        raise BuildingVisualError(f"{location} must remain in canonical order")
    return gaps


def _state_ids(
    value: Any,
    location: str,
    allowed: list[str],
) -> list[str]:
    selected = _list(
        value,
        location,
        minimum=0,
        maximum=len(allowed),
        item_limit=80,
    )
    unknown = sorted(set(selected) - set(allowed))
    if unknown:
        raise BuildingVisualError(f"{location}: unknown IDs {unknown}")
    return selected


def _normalize_states(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(STATE_IDS):
        raise BuildingVisualError("pilot manifest.states must contain six states")
    states = []
    nav_labels: list[str] = []
    for index, raw_state in enumerate(raw):
        location = f"pilot manifest.states[{index}]"
        value = _exact(raw_state, STATE_FIELDS, location)
        state_id = _identifier(value["id"], f"{location}.id")
        selected = {
            "zone_ids": _state_ids(value["zone_ids"], f"{location}.zone_ids", ZONE_IDS),
            "chain_step_ids": _state_ids(
                value["chain_step_ids"], f"{location}.chain_step_ids", CHAIN_STEP_IDS
            ),
            "protected_path_ids": _state_ids(
                value["protected_path_ids"],
                f"{location}.protected_path_ids",
                PROTECTED_PATH_IDS,
            ),
            "isolation_path_state_ids": _state_ids(
                value["isolation_path_state_ids"],
                f"{location}.isolation_path_state_ids",
                ISOLATION_STATE_IDS,
            ),
            "abilene_known_ids": _state_ids(
                value["abilene_known_ids"],
                f"{location}.abilene_known_ids",
                ABILENE_KNOWN_IDS,
            ),
            "abilene_unknown_ids": _state_ids(
                value["abilene_unknown_ids"],
                f"{location}.abilene_unknown_ids",
                ABILENE_UNKNOWN_IDS,
            ),
        }
        if not isinstance(value["show_phase5_handoff"], bool):
            raise BuildingVisualError(f"{location}.show_phase5_handoff must be boolean")
        primary_layers = (
            bool(selected["zone_ids"]),
            bool(selected["protected_path_ids"]),
            bool(selected["abilene_known_ids"] or selected["abilene_unknown_ids"]),
            bool(
                selected["chain_step_ids"]
                and not (
                    selected["abilene_known_ids"] or selected["abilene_unknown_ids"]
                )
            ),
        )
        if sum(primary_layers) != 1:
            raise BuildingVisualError(
                f"{location}: state must select exactly one primary teaching layer"
            )
        if selected["isolation_path_state_ids"] and set(
            selected["protected_path_ids"]
        ) != set(PROTECTED_PATH_IDS):
            raise BuildingVisualError(
                f"{location}: isolation requires both generic protected paths"
            )
        if (selected["abilene_known_ids"] or selected["abilene_unknown_ids"]) and (
            not selected["abilene_known_ids"] or not selected["abilene_unknown_ids"]
        ):
            raise BuildingVisualError(
                f"{location}: Abilene states must preserve evidence and unknowns"
            )
        nav_label = _text(value["nav_label"], f"{location}.nav_label", maximum=24)
        nav_labels.append(nav_label)
        states.append(
            {
                "id": state_id,
                "nav_label": nav_label,
                "title": _text(value["title"], f"{location}.title", maximum=160),
                "instruction": _text(
                    value["instruction"], f"{location}.instruction", maximum=520
                ),
                **selected,
                "show_phase5_handoff": value["show_phase5_handoff"],
            }
        )
    if [state["id"] for state in states] != STATE_IDS:
        raise BuildingVisualError(
            f"pilot manifest states must remain in canonical order {STATE_IDS}"
        )
    if len(nav_labels) != len(set(nav_labels)):
        raise BuildingVisualError("pilot manifest state nav labels must be unique")
    expected_state_selections = [
        (ZONE_IDS, [], [], [], [], [], False),
        ([], CHAIN_STEP_IDS, [], [], [], [], False),
        ([], [], PROTECTED_PATH_IDS, [], [], [], False),
        ([], [], PROTECTED_PATH_IDS, ISOLATION_STATE_IDS, [], [], False),
        ([], CHAIN_STEP_IDS, [], [], ABILENE_KNOWN_IDS, ABILENE_UNKNOWN_IDS, False),
        (
            [],
            ["busway", "rack_position"],
            [],
            [],
            ["rack_family_delivery"],
            ["internal_power_train"],
            True,
        ),
    ]
    for state, expected in zip(states, expected_state_selections, strict=True):
        actual = (
            state["zone_ids"],
            state["chain_step_ids"],
            state["protected_path_ids"],
            state["isolation_path_state_ids"],
            state["abilene_known_ids"],
            state["abilene_unknown_ids"],
            state["show_phase5_handoff"],
        )
        if actual != expected:
            raise BuildingVisualError(
                f"pilot manifest.states.{state['id']} escaped its canonical selection"
            )
    return states


def _collect_fact_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {"fact_refs", "related_fact_refs"}:
                refs.update(nested)
            else:
                refs.update(_collect_fact_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(_collect_fact_refs(nested))
    return refs


def compile_building_power_path(
    manifest: dict[str, Any],
    evidence_ledgers: Mapping[str, dict[str, Any]],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Validate and normalize the Phase 4 teaching payload."""
    manifest = _exact(manifest, TOP_LEVEL_FIELDS, "pilot manifest")
    forbidden = base._forbidden_fields(manifest)
    if forbidden:
        raise BuildingVisualError(
            f"pilot manifest contains pacing or scripting fields: {forbidden}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise BuildingVisualError("pilot manifest schema_version must be 1")
    source_digest = base.validate_source_digest(source_digest)
    declared_ledgers, ledgers = base.validate_evidence_ledgers(
        manifest, evidence_ledgers
    )
    phase = _exact(manifest["phase"], PHASE_FIELDS, "pilot manifest.phase")
    if type(phase["number"]) is not int or phase["number"] != 4:
        raise BuildingVisualError("pilot manifest.phase.number must be integer 4")
    interaction = base.validate_manual_interaction(
        manifest["interaction"], location="pilot manifest.interaction"
    )
    canvas = _exact(manifest["canvas"], CANVAS_FIELDS, "pilot manifest.canvas")
    if canvas["kind"] != CANVAS_KIND:
        raise BuildingVisualError(f"pilot manifest.canvas.kind must be {CANVAS_KIND!r}")
    if canvas["width"] != CANVAS_WIDTH or canvas["height"] != CANVAS_HEIGHT:
        raise BuildingVisualError(
            f"pilot manifest.canvas must be {CANVAS_WIDTH} by {CANVAS_HEIGHT}"
        )
    contract = _exact(
        canvas["contract"], CONTRACT_FIELDS, "pilot manifest.canvas.contract"
    )
    expected_contract = {
        "state_selection": "exclusive_single_primary_layer",
        "primary_layers": [
            "spatial_building_zones",
            "functional_power_chain",
            "generic_protected_paths",
            "conditional_path_isolation",
            "abilene_mapping",
        ],
        "evidence_binding": "content_record_fact_refs",
        "geometry_owner": "building_power_path_renderer",
        "handoff_requires": "abilene_mapping",
    }
    if contract != expected_contract:
        raise BuildingVisualError(
            "pilot manifest.canvas.contract must match building_power_path_v1"
        )
    content = {
        "spatial_building_zones": _normalize_zones(
            manifest["spatial_building_zones"], ledgers
        ),
        "functional_power_chain": _normalize_chain(
            manifest["functional_power_chain"], ledgers
        ),
        "generic_protected_paths": _normalize_paths(
            manifest["generic_protected_paths"], ledgers
        ),
        "conditional_path_isolation": _normalize_isolation(
            manifest["conditional_path_isolation"], ledgers
        ),
        "abilene_mapping": _normalize_abilene(manifest["abilene_mapping"], ledgers),
        "phase5_handoff": _normalize_handoff(manifest["phase5_handoff"], ledgers),
        "evidence_gaps": _normalize_gaps(manifest["evidence_gaps"], ledgers),
    }
    states = _normalize_states(manifest["states"])
    evidence = base.compile_evidence_cards(
        _collect_fact_refs(content), ledgers, ledger_ids=declared_ledgers
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "pilot": {
            "id": _identifier(manifest["id"], "pilot manifest.id"),
            "title": _text(manifest["title"], "pilot manifest.title", maximum=160),
            "phase": {
                "id": _identifier(phase["id"], "pilot manifest.phase.id"),
                "number": 4,
                "title": _text(
                    phase["title"], "pilot manifest.phase.title", maximum=120
                ),
                "anchor_question": _text(
                    phase["anchor_question"],
                    "pilot manifest.phase.anchor_question",
                    maximum=240,
                ),
            },
            "learning_objective": _text(
                manifest["learning_objective"],
                "pilot manifest.learning_objective",
                maximum=520,
            ),
            "interaction": interaction,
        },
        "canvas": {
            "kind": CANVAS_KIND,
            "width": CANVAS_WIDTH,
            "height": CANVAS_HEIGHT,
            "contract": dict(contract),
        },
        **content,
        "states": states,
        "evidence": evidence,
    }
    compiled_forbidden = base._forbidden_fields(payload)
    if compiled_forbidden:
        raise BuildingVisualError(
            f"compiled teaching payload contains forbidden fields: {compiled_forbidden}"
        )
    return payload


def _escape(value: Any) -> str:
    return base._escape(value)


def _wrapped(
    text: str,
    *,
    x: float,
    y: float,
    width_chars: int,
    line_height: float,
    css_class: str,
    maximum_lines: int,
    center_lines: bool = False,
) -> str:
    return base._wrapped_svg_text(
        text,
        x=x,
        y=y,
        width_chars=width_chars,
        line_height=line_height,
        css_class=css_class,
        maximum_lines=maximum_lines,
        center_lines=center_lines,
    )


def _fact_description(record: Mapping[str, Any]) -> str:
    return "Evidence: " + ", ".join(record["fact_refs"])


def chain_step_geometry(index: int) -> dict[str, tuple[float, float, float, float]]:
    """Return non-overlapping badge and title bounds for one chain gate."""
    if index not in range(len(CHAIN_STEP_IDS)):
        raise BuildingVisualError("chain step geometry index must be 0 through 5")
    x = 45 + index * 255
    return {
        "node": (x, 315, x + 210, 560),
        "badge": (x + 88, 330, x + 122, 364),
        "title": (x + 20, 378, x + 190, 424),
        "verb": (x + 20, 438, x + 190, 518),
    }


def _zone_svg(record: Mapping[str, Any], index: int) -> str:
    x_values = (70, 535, 1000)
    x = x_values[index]
    top_y = 245
    width = 390
    depth = 78
    height = 350
    contains = "".join(
        f'<li role="listitem">{_escape(item)}</li>' for item in record["contains"]
    )
    return f"""
    <g data-zone-id="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <polygon class="zone-roof zone-{index}" points="{x},{top_y} {x + width},{top_y} {x + width + depth},{top_y - depth} {x + depth},{top_y - depth}"/>
      <polygon class="zone-side zone-{index}" points="{x + width},{top_y} {x + width + depth},{top_y - depth} {x + width + depth},{top_y + height - depth} {x + width},{top_y + height}"/>
      <rect class="zone-front zone-{index}" x="{x}" y="{top_y}" width="{width}" height="{height}"/>
      <text class="zone-index" x="{x + 24}" y="{top_y + 38}">0{index + 1}</text>
      <text class="zone-title" x="{x + 24}" y="{top_y + 79}">{_escape(record["title"])}</text>
      {_wrapped(" · ".join(record["contains"]), x=x + 24, y=top_y + 123, width_chars=34, line_height=28, css_class="zone-copy", maximum_lines=5)}
      {_wrapped(record["boundary"], x=x + 24, y=top_y + 270, width_chars=43, line_height=21, css_class="zone-boundary", maximum_lines=4)}
      <foreignObject x="-2000" y="-2000" width="1" height="1"><ul>{contains}</ul></foreignObject>
    </g>"""


def _zones_svg(record: Mapping[str, Any]) -> str:
    boundary = record["boundary"]
    return f"""
  <g data-zone-layer hidden>
    <text class="layer-kicker" x="70" y="68">SPATIAL ORIENTATION · GENERIC CUTAWAY</text>
    <text class="layer-title" x="70" y="113">{_escape(record["title"])}</text>
    {_wrapped(record["body"], x=70, y=150, width_chars=120, line_height=22, css_class="layer-body", maximum_lines=2)}
    {"".join(_zone_svg(zone, index) for index, zone in enumerate(record["zones"]))}
    <g class="boundary-strip" aria-label="{_escape(_fact_description(boundary))}">
      <rect x="70" y="755" width="1460" height="98" rx="8"/>
      <text class="boundary-title" x="94" y="790">{_escape(boundary["title"])}</text>
      {_wrapped(boundary["body"], x=94, y=820, width_chars=145, line_height=20, css_class="boundary-copy", maximum_lines=2)}
    </g>
  </g>"""


def _chain_step_svg(
    record: Mapping[str, Any], index: int, *, ghost: bool = False
) -> str:
    x = chain_step_geometry(index)["node"][0]
    attr = "data-generic-chain-step-id" if ghost else "data-chain-step-id"
    classes = "chain-node chain-ghost" if ghost else "chain-node"
    return f"""
    <g {attr}="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <rect class="{classes}" x="{x}" y="315" width="210" height="245" rx="12"/>
      <circle class="chain-number" cx="{x + 105}" cy="347" r="17"/>
      <text class="chain-number-label centered" x="{x + 105}" y="353">{index + 1}</text>
      {_wrapped(record["title"], x=x + 105, y=397, width_chars=20, line_height=22, css_class="chain-title centered", maximum_lines=2, center_lines=True)}
      {_wrapped(record["verb"], x=x + 20, y=445, width_chars=28, line_height=20, css_class="chain-verb", maximum_lines=4)}
      <text class="chain-posture centered" x="{x + 105}" y="538">{_escape(record["evidence_posture"].replace("_", " ").upper())}</text>
    </g>"""


def _chain_svg(record: Mapping[str, Any]) -> str:
    arrows = "".join(
        f'<path class="carrier-arrow" d="M {255 + index * 255} 438 H {295 + index * 255}"/>'
        for index in range(5)
    )
    boundary = record["boundary"]
    return f"""
  <g data-chain-layer hidden>
    <text class="layer-kicker" x="45" y="68">FUNCTIONAL GATES · CONCEPTUAL CARRIER FLOW</text>
    <text class="layer-title" x="45" y="113">{_escape(record["title"])}</text>
    {_wrapped(record["body"], x=45, y=150, width_chars=126, line_height=22, css_class="layer-body", maximum_lines=2)}
    <path class="carrier-line" d="M 80 438 H 1525"/>
    {arrows}
    {"".join(_chain_step_svg(step, index) for index, step in enumerate(record["steps"]))}
    <g class="carrier-label"><rect x="610" y="246" width="380" height="44" rx="22"/><text class="centered" x="800" y="274">FACILITY AC · DIRECTION OF TEACHING PATH</text></g>
    <g class="boundary-strip" aria-label="{_escape(_fact_description(boundary))}">
      <rect x="45" y="724" width="1510" height="118" rx="8"/>
      <text class="boundary-title" x="70" y="762">REFERENCE PATH ≠ REQUIRED TOPOLOGY</text>
      {_wrapped(boundary["body"], x=70, y=798, width_chars=148, line_height=21, css_class="boundary-copy", maximum_lines=2)}
    </g>
  </g>"""


def _protected_path_svg(record: Mapping[str, Any], index: int) -> str:
    y = 290 + index * 245
    css = "path-a" if record["id"] == "path_a" else "path-b"
    cards = []
    arrows = []
    for item_index, item in enumerate(record["elements"]):
        x = 125 + item_index * 265
        cards.append(
            f'<rect class="path-node {css}" x="{x}" y="{y}" width="205" height="96" rx="10"/>'
            + _wrapped(
                item,
                x=x + 102,
                y=y + 43,
                width_chars=25,
                line_height=22,
                css_class="path-node-label centered",
                maximum_lines=2,
                center_lines=True,
            )
        )
        if item_index < 3:
            arrows.append(
                f'<path class="path-arrow {css}" d="M {x + 205} {y + 48} H {x + 265}"/>'
            )
    return f"""
    <g data-protected-path-id="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <text class="path-title {css}" x="38" y="{y + 43}">{_escape(record["title"])}</text>
      {"".join(cards)}{"".join(arrows)}
      <path class="path-arrow {css}" d="M 1125 {y + 48} H 1160"/>
      <text class="path-posture" x="38" y="{y + 68}">GENERIC</text>
    </g>"""


def _paths_svg(record: Mapping[str, Any]) -> str:
    interfaces = record["load_interfaces"]
    boundary = record["boundary"]
    return f"""
  <g data-path-layer hidden>
    <text class="layer-kicker" x="55" y="62">GENERIC REFERENCE · A/B ARE TEACHING LABELS</text>
    <text class="layer-title" x="55" y="106">{_escape(record["title"])}</text>
    {_wrapped(record["body"], x=55, y=143, width_chars=126, line_height=22, css_class="layer-body", maximum_lines=3)}
    {"".join(_protected_path_svg(path, index) for index, path in enumerate(record["paths"]))}
    <g class="rack-interface" aria-label="{_escape(_fact_description(interfaces[0]))}; {_escape(_fact_description(interfaces[1]))}">
      <rect x="1160" y="238" width="380" height="432" rx="14"/>
      <text class="rack-kicker centered" x="1350" y="272">LOAD INTERFACES · CONDITIONS VISIBLE</text>
      <text class="rack-title" x="1190" y="314">{_escape(interfaces[0]["title"])}</text>
      {_wrapped(interfaces[0]["body"], x=1190, y=347, width_chars=44, line_height=19, css_class="rack-copy", maximum_lines=5)}
      <path class="rack-separator" d="M 1190 451 H 1510"/>
      <text class="rack-title" x="1190" y="486">{_escape(interfaces[1]["title"])}</text>
      {_wrapped(interfaces[1]["body"], x=1190, y=519, width_chars=44, line_height=19, css_class="rack-copy", maximum_lines=6)}
      <circle class="input-a" cx="1160" cy="338" r="10"/><circle class="input-b" cx="1160" cy="583" r="10"/>
    </g>
    <g class="boundary-strip" aria-label="{_escape(_fact_description(boundary))}">
      <rect x="55" y="716" width="1485" height="126" rx="8"/>
      <text class="boundary-title" x="80" y="754">{_escape(boundary["title"])}</text>
      {_wrapped(boundary["body"], x=80, y=790, width_chars=148, line_height=21, css_class="boundary-copy", maximum_lines=3)}
    </g>
  </g>"""


def _isolation_svg(record: Mapping[str, Any]) -> str:
    isolated, remaining, result = record["path_states"]
    planned, fault = record["claim_split"]
    boundary = record["boundary"]
    return f"""
  <g data-isolation-layer hidden>
    <text class="layer-kicker" x="55" y="52">CONDITIONAL ISOLATION · STATIC STATE</text>
    <text class="layer-title" x="55" y="94">{_escape(record["title"])}</text>
    {_wrapped(record["body"], x=55, y=128, width_chars=128, line_height=21, css_class="layer-body", maximum_lines=2)}
    <g class="claim-split" data-isolation-path-state-id="isolated_path_a">
      <rect x="55" y="176" width="705" height="132" rx="10"/>
      <text class="claim-title" x="82" y="215">{_escape(planned["title"])}</text>
      {_wrapped(planned["body"], x=82, y=250, width_chars=71, line_height=20, css_class="claim-copy", maximum_lines=3)}
      <rect x="840" y="176" width="705" height="132" rx="10"/>
      <text class="claim-title" x="867" y="215">{_escape(fault["title"])}</text>
      {_wrapped(fault["body"], x=867, y=250, width_chars=71, line_height=20, css_class="claim-copy", maximum_lines=3)}
    </g>
    <g data-isolation-path-state-id="isolated_path_a" aria-label="{_escape(_fact_description(isolated))}">
      <rect class="path-unavailable" x="55" y="350" width="1015" height="118" rx="13"/>
      <text class="isolation-path-title" x="85" y="389">PATH A · UNAVAILABLE</text>
      <path class="unavailable-strike" d="M 305 386 H 1018"/>
      <text class="isolation-path-copy" x="305" y="425">REMOVED FROM SERVICE · MAINTENANCE OR INTERRUPTION</text>
      <text class="isolation-path-guard" x="305" y="452">NO BREAKER, FAULT LOCATION, OR CLEARING SEQUENCE SHOWN</text>
    </g>
    <g data-isolation-path-state-id="remaining_path_b" aria-label="{_escape(_fact_description(remaining))}">
      <rect class="remaining-outline" x="55" y="500" width="1015" height="118" rx="13"/>
      <text class="remaining-path-title" x="85" y="539">PATH B · REMAINS</text>
      <path class="remaining-carrier" d="M 305 536 H 1018"/>
      <text class="remaining-path-copy" x="305" y="575">CONDITIONALLY AVAILABLE · CAPABILITY NOT PROVEN</text>
      <text class="isolation-path-guard" x="305" y="602">INDEPENDENCE, PROTECTION, AND HEALTH REQUIRE A SPECIFIC DESIGN</text>
    </g>
    <g data-isolation-path-state-id="rack_result" aria-label="{_escape(_fact_description(result))}">
      <rect class="rack-result-card" x="1120" y="350" width="425" height="268" rx="13"/>
      <text class="rack-result-kicker" x="1150" y="389">CONDITIONAL RACK RESULT</text>
      <text class="rack-result-title" x="1150" y="430">Still supplied only if:</text>
      <circle class="condition-dot" cx="1160" cy="470" r="6"/><text class="rack-result-copy" x="1180" y="476">the load accepts the surviving feed</text>
      <circle class="condition-dot" cx="1160" cy="511" r="6"/><text class="rack-result-copy" x="1180" y="517">the end-to-end Path B can carry it</text>
      <circle class="condition-dot unresolved" cx="1160" cy="566" r="6"/><text class="rack-result-copy" x="1180" y="572">otherwise the outcome is unresolved</text>
    </g>
    <g class="isolation-boundary" aria-label="{_escape(_fact_description(boundary))}">
      <rect x="165" y="688" width="1270" height="148" rx="9"/>
      <text class="boundary-title centered" x="800" y="730">{_escape(boundary["title"])}</text>
      {_wrapped(boundary["body"], x=800, y=768, width_chars=126, line_height=21, css_class="boundary-copy centered", maximum_lines=3, center_lines=True)}
    </g>
  </g>"""


def _abilene_card_svg(record: Mapping[str, Any], index: int, *, known: bool) -> str:
    x = 65 if known else 1040
    y = 225 + index * 245
    css = "known-card" if known else "unknown-card"
    attr = "data-abilene-known-id" if known else "data-abilene-unknown-id"
    status = "EVIDENCE" if known else "UNKNOWN"
    return f"""
    <g {attr}="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <rect class="abilene-card {css}" x="{x}" y="{y}" width="495" height="196" rx="12"/>
      <text class="abilene-status {css}" x="{x + 24}" y="{y + 34}">{status}</text>
      {_wrapped(record["title"], x=x + 24, y=y + 72, width_chars=43, line_height=24, css_class="abilene-title", maximum_lines=2)}
      {_wrapped(record["body"], x=x + 24, y=y + 125, width_chars=57, line_height=19, css_class="abilene-copy", maximum_lines=4)}
    </g>"""


def _abilene_svg(record: Mapping[str, Any], chain: Mapping[str, Any]) -> str:
    guard = record["guard"]
    ghost_steps = "".join(
        f"""<g data-generic-chain-step-id="{_escape(step["id"])}" aria-label="Generic reference: {_escape(step["title"])}">
          <rect class="ghost-node" x="{602 + index % 3 * 132}" y="{330 + index // 3 * 148}" width="112" height="104" rx="8"/>
          <text class="ghost-number centered" x="{658 + index % 3 * 132}" y="{362 + index // 3 * 148}">{index + 1}</text>
          {_wrapped(step["title"], x=658 + index % 3 * 132, y=392 + index // 3 * 148, width_chars=14, line_height=18, css_class="ghost-label centered", maximum_lines=2, center_lines=True)}
        </g>"""
        for index, step in enumerate(chain["steps"])
    )
    return f"""
  <g data-abilene-layer hidden>
    <text class="layer-kicker" x="55" y="58">ABILENE · EVIDENCE / UNKNOWN SPLIT</text>
    <text class="layer-title" x="55" y="102">{_escape(record["title"])}</text>
    {_wrapped(record["body"], x=55, y=139, width_chars=126, line_height=22, css_class="layer-body", maximum_lines=3)}
    <g class="generic-reference-chain">
      <rect x="565" y="202" width="470" height="510" rx="14"/>
      <text class="reference-label centered" x="800" y="238">GENERIC REFERENCE · NOT SITE-CONFIRMED</text>
      <path class="unknown-path" d="M 610 618 H 990"/>
      <text class="unknown-question centered" x="800" y="635">?</text>
      {ghost_steps}
    </g>
    {"".join(_abilene_card_svg(item, index, known=True) for index, item in enumerate(record["known"]))}
    {"".join(_abilene_card_svg(item, index, known=False) for index, item in enumerate(record["unknown"]))}
    <g class="mapping-guard" aria-label="{_escape(_fact_description(guard))}">
      <rect x="360" y="747" width="880" height="94" rx="10"/>
      <text class="boundary-title centered" x="800" y="781">{_escape(guard["title"])}</text>
      {_wrapped(guard["body"], x=800, y=813, width_chars=108, line_height=19, css_class="boundary-copy centered", maximum_lines=2, center_lines=True)}
    </g>
  </g>"""


def _handoff_svg(record: Mapping[str, Any]) -> str:
    known = record["known"]
    unknown = record["unknown"][0]
    return f"""
  <g data-handoff hidden>
    <rect class="handoff-backdrop" x="30" y="174" width="1540" height="590" rx="18"/>
    <text class="handoff-kicker" x="80" y="220">NEXT · PHASE 5 · STOP AT THE RACK-POWER BOUNDARY</text>
    <text class="handoff-title" x="80" y="268">{_escape(record["title"])}</text>
    {_wrapped(record["body"], x=80, y=306, width_chars=128, line_height=22, css_class="handoff-body", maximum_lines=3)}
    <g aria-label="{_escape(_fact_description(known[0]))}">
      <rect class="handoff-node handoff-known" x="85" y="425" width="290" height="155" rx="12"/>
      <text class="handoff-node-kicker" x="110" y="462">SITE / DESIGN REFERENCE</text>
      <text class="handoff-node-title" x="110" y="504">GB200 rack family</text>
      <text class="handoff-node-title" x="110" y="535">and NVL72 reference</text>
    </g>
    <path class="handoff-arrow" d="M 375 503 H 480"/>
    <g aria-label="Rack position phase boundary">
      <rect class="handoff-node rack-boundary-node" x="480" y="397" width="270" height="210" rx="12"/>
      <text class="handoff-node-kicker" x="505" y="438">PHASE 4 OUTPUT</text>
      <text class="handoff-node-title" x="505" y="488">Facility AC at</text>
      <text class="handoff-node-title" x="505" y="520">rack boundary</text>
      <text class="handoff-stop" x="505" y="568">STOP · SITE INPUT UNKNOWN</text>
    </g>
    <path class="handoff-arrow" d="M 750 503 H 855"/>
    <g aria-label="{_escape(_fact_description(known[1]))}">
      <rect class="handoff-node product-reference" x="855" y="397" width="270" height="210" rx="12"/>
      <text class="handoff-node-kicker" x="880" y="438">PRODUCT REFERENCE</text>
      <text class="handoff-node-title" x="880" y="488">Rack power shelf</text>
      <text class="handoff-node-title" x="880" y="520">nominal DC output</text>
      <text class="handoff-stop" x="880" y="568">NOT A SITE OPERATING POINT</text>
    </g>
    <path class="handoff-arrow handoff-unknown-arrow" d="M 1125 503 H 1230"/>
    <g aria-label="{_escape(_fact_description(unknown))}">
      <rect class="handoff-node handoff-unknown" x="1230" y="397" width="285" height="210" rx="12"/>
      <text class="handoff-node-kicker" x="1255" y="438">PHASE 5 QUESTION</text>
      <text class="handoff-node-title" x="1255" y="488">Rack DC toward</text>
      <text class="handoff-node-title" x="1255" y="520">processor rails</text>
      <text class="handoff-question" x="1255" y="570">SITE CONFIGURATION ?</text>
    </g>
  </g>"""


def _responsive_zone(record: Mapping[str, Any], index: int) -> str:
    items = "".join(f"<li>{_escape(item)}</li>" for item in record["contains"])
    return f"""<article class="responsive-card responsive-zone" data-zone-id="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <p class="responsive-kicker">Zone {index + 1:02d}</p><h3>{_escape(record["title"])}</h3>
      <ul>{items}</ul><p class="responsive-boundary">{_escape(record["boundary"])}</p></article>"""


def _responsive_chain_step(
    record: Mapping[str, Any], index: int, *, ghost: bool = False
) -> str:
    attr = "data-generic-chain-step-id" if ghost else "data-chain-step-id"
    return f"""<article class="responsive-card responsive-chain-step" {attr}="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <p class="responsive-kicker">Gate {index + 1:02d}</p><h3>{_escape(record["title"])}</h3>
      <p>{_escape(record["verb"])}</p></article>"""


def _responsive_path(record: Mapping[str, Any]) -> str:
    elements = '<span class="responsive-arrow">→</span>'.join(
        f"<span>{_escape(item)}</span>" for item in record["elements"]
    )
    return f"""<article class="responsive-card responsive-path" data-protected-path-id="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <p class="responsive-kicker">Generic teaching label</p><h3>{_escape(record["title"])}</h3>
      <div class="responsive-flow" role="img" aria-label="{_escape(" to ".join(record["elements"]))}">{elements}</div></article>"""


def _responsive_abilene_card(record: Mapping[str, Any], *, known: bool) -> str:
    attr = "data-abilene-known-id" if known else "data-abilene-unknown-id"
    label = "Evidence" if known else "Unknown"
    css = "responsive-known" if known else "responsive-unknown"
    return f"""<article class="responsive-card {css}" {attr}="{_escape(record["id"])}" aria-label="{_escape(_fact_description(record))}">
      <p class="responsive-kicker">{label}</p><h3>{_escape(record["title"])}</h3><p>{_escape(record["body"])}</p></article>"""


def _responsive_visual(payload: Mapping[str, Any]) -> str:
    zones = payload["spatial_building_zones"]
    chain = payload["functional_power_chain"]
    paths = payload["generic_protected_paths"]
    isolation = payload["conditional_path_isolation"]
    abilene = payload["abilene_mapping"]
    handoff = payload["phase5_handoff"]
    isolation_cards = "".join(
        f'<article class="responsive-card responsive-isolation" data-isolation-path-state-id="{_escape(record["id"])}"><h3>{_escape(record["title"])}</h3><p>{_escape(record.get("body", record.get("boundary", "")))}</p></article>'
        for record in isolation["path_states"]
    )
    handoff_known = handoff["known"]
    handoff_unknown = handoff["unknown"][0]
    return f"""
  <section class="responsive-visual" aria-label="Responsive building-power teaching surface">
    <section class="responsive-layer" data-zone-layer hidden>
      <p class="responsive-kicker">Spatial orientation · generic cutaway</p><h2>{_escape(zones["title"])}</h2>
      <div class="responsive-grid">{"".join(_responsive_zone(item, index) for index, item in enumerate(zones["zones"]))}</div>
      <p class="responsive-boundary">{_escape(zones["boundary"]["title"])}: {_escape(zones["boundary"]["body"])}</p>
    </section>
    <section class="responsive-layer" data-chain-layer hidden>
      <p class="responsive-kicker">Functional gates · facility AC</p><h2>{_escape(chain["title"])}</h2>
      <div class="responsive-chain">{"".join(_responsive_chain_step(item, index) for index, item in enumerate(chain["steps"]))}</div>
      <p class="responsive-boundary">{_escape(chain["boundary"]["body"])}</p>
    </section>
    <section class="responsive-layer responsive-isolation-layer" data-isolation-layer hidden>
      <p class="responsive-kicker">Static condition · no clearing sequence</p>
      <div class="responsive-grid">{isolation_cards}</div>
      <div class="responsive-claim-split"><article><h3>{_escape(isolation["claim_split"][0]["title"])}</h3><p>{_escape(isolation["claim_split"][0]["body"])}</p></article><article><h3>{_escape(isolation["claim_split"][1]["title"])}</h3><p>{_escape(isolation["claim_split"][1]["body"])}</p></article></div>
    </section>
    <section class="responsive-layer" data-path-layer hidden>
      <p class="responsive-kicker">Generic reference · not a site claim</p><h2>{_escape(paths["title"])}</h2>
      <div class="responsive-paths">{"".join(_responsive_path(item) for item in paths["paths"])}</div>
      <article class="responsive-card responsive-load"><h3>{_escape(paths["load_interfaces"][0]["title"])}</h3><p>{_escape(paths["load_interfaces"][0]["body"])}</p></article>
      <p class="responsive-boundary">{_escape(paths["boundary"]["title"])}: {_escape(paths["boundary"]["body"])}</p>
    </section>
    <section class="responsive-layer responsive-handoff" data-handoff hidden>
      <p class="responsive-kicker">Next · Phase 5</p><h2>{_escape(handoff["title"])}</h2>
      <div class="responsive-handoff-flow" role="img" aria-label="Facility AC at rack boundary to rack power shelf reference to processor-rail question">
        <article><strong>Phase 4 output</strong><span>Facility AC at rack boundary</span></article><span>→</span>
        <article><strong>Product reference</strong><span>Rack power shelf nominal DC output</span></article><span>→</span>
        <article><strong>Generic Phase 5 questions</strong><span>Board conversion ? · processor rails ?</span></article>
      </div>
      <p class="responsive-boundary"><strong>Abilene unknown retained.</strong> {_escape(handoff_unknown["body"])}</p>
      <span hidden>{_escape(handoff_known[0]["body"])} {_escape(handoff_known[1]["body"])}</span>
    </section>
    <section class="responsive-layer" data-abilene-layer hidden>
      <p class="responsive-kicker">Abilene · evidence / unknown split</p><h2>{_escape(abilene["title"])}</h2>
      <div class="responsive-abilene-grid">
        <div>{"".join(_responsive_abilene_card(item, known=True) for item in abilene["known"])}</div>
        <div class="responsive-generic-chain"><p class="responsive-kicker">Generic reference only</p>{"".join(_responsive_chain_step(item, index, ghost=True) for index, item in enumerate(chain["steps"]))}</div>
        <div>{"".join(_responsive_abilene_card(item, known=False) for item in abilene["unknown"])}</div>
      </div>
      <p class="responsive-boundary">{_escape(abilene["guard"]["title"])}: {_escape(abilene["guard"]["body"])}</p>
    </section>
  </section>"""


def render_building_power_path(payload: dict[str, Any]) -> str:
    """Render one compiled Phase 4 pilot as a self-contained HTML page."""
    if payload.get("canvas", {}).get("kind") != CANVAS_KIND:
        raise BuildingVisualError("render payload is not a building-power path")
    state_buttons = "".join(
        f'<button class="state-button" type="button" role="tab" '
        f'id="state-tab-{_escape(state["id"])}" aria-controls="visual" '
        f'aria-label="State {index + 1}: {_escape(state["title"])}" '
        f'title="{_escape(state["title"])}" aria-selected="false" '
        f'data-state-index="{index}"><span class="state-number">{index + 1:02d}</span>'
        f'<span class="state-nav-label">{_escape(state["nav_label"])}</span></button>'
        for index, state in enumerate(payload["states"])
    )
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).replace(
        "</", "<\\/"
    )
    evidence = base._evidence_html(payload)
    responsive = _responsive_visual(payload)
    phase = payload["pilot"]["phase"]
    rendered = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="gigawatt-source-digest" content="{_escape(payload["source_digest"])}">
<title>GIGAWATT — {_escape(payload["pilot"]["title"])}</title>
<style>
  :root {{ --paper:#f7f6f1; --ink:#151716; --muted:#5e625f; --faint:#d4d4cd; --blue:#185f8f; --blue-soft:#e7f2f8; --green:#278a76; --green-soft:#e7f5f1; --amber:#aa6819; --amber-soft:#fff4e5; --red:#ad3028; --red-soft:#fbecea; --violet:#6f5aa8; }}
  * {{ box-sizing:border-box; }}
  [hidden] {{ display:none !important; }}
  html,body {{ width:100%; height:100%; min-height:0; margin:0; background:var(--paper); color:var(--ink); font-family:Inter,"Helvetica Neue",Arial,sans-serif; }}
  html {{ overflow:hidden; }}
  body {{ display:grid; grid-template-rows:auto minmax(0,1fr) auto; height:100dvh; min-height:0; overflow:hidden; }}
  header {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(300px,560px); gap:20px; padding:11px 20px 10px; border-bottom:1.5px solid var(--ink); }}
  .eyebrow,.phase-question,.state-number,.fact-ref,.layer-kicker,.responsive-kicker,.chain-posture,.abilene-status,.rack-kicker,.handoff-kicker,.handoff-node-kicker {{ text-transform:uppercase; letter-spacing:.08em; font-weight:760; }}
  .eyebrow,.phase-question,.state-number,.fact-ref,.responsive-kicker {{ font-size:11px; }}
  h1 {{ margin:3px 0; font-size:clamp(21px,2.2vw,34px); line-height:1.05; }}
  header p {{ margin:2px 0; line-height:1.3; }}
  .objective {{ align-self:end; color:var(--muted); font-size:13px; }}
  main {{ min-width:0; min-height:0; display:grid; place-items:center; overflow:hidden; padding:8px 14px; }}
  .visual-shell {{ width:100%; height:100%; min-width:0; min-height:0; max-width:1600px; max-height:900px; border:1.5px solid var(--ink); background:white; }}
  svg {{ display:block; width:100%; height:100%; }}
  .centered {{ text-anchor:middle; }}
  .layer-kicker {{ fill:var(--blue); font-size:14px; }}
  .layer-title {{ font-size:31px; font-weight:770; }}
  .layer-body {{ fill:var(--muted); font-size:15px; }}
  .zone-roof,.zone-side,.zone-front {{ stroke:var(--ink); stroke-width:2; }}
  .zone-roof {{ fill:#dcecf4; }} .zone-side {{ fill:#c4dae5; }} .zone-front {{ fill:#f9fcfd; }}
  .zone-1.zone-roof {{ fill:#e2f1ec; }} .zone-1.zone-side {{ fill:#cbe3da; }} .zone-1.zone-front {{ fill:#fbfdfc; }}
  .zone-2.zone-roof {{ fill:#eee9f8; }} .zone-2.zone-side {{ fill:#d9d0ef; }} .zone-2.zone-front {{ fill:#fdfcff; }}
  .zone-index {{ fill:var(--blue); font-size:14px; font-weight:770; letter-spacing:.08em; }}
  .zone-title {{ font-size:27px; font-weight:770; }} .zone-copy {{ font-size:18px; font-weight:650; }} .zone-boundary {{ fill:var(--muted); font-size:14px; }}
  .boundary-strip rect,.isolation-boundary rect,.mapping-guard rect {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.7; }}
  .boundary-title {{ font-size:17px; font-weight:760; }} .boundary-copy {{ fill:var(--muted); font-size:14px; }}
  .carrier-line {{ fill:none; stroke:var(--blue); stroke-width:6; }} .carrier-arrow,.path-arrow,.handoff-arrow {{ fill:none; stroke:var(--blue); stroke-width:4; marker-end:url(#arrow-blue); }}
  .chain-node {{ fill:white; stroke:var(--ink); stroke-width:2; }} .chain-number {{ fill:var(--blue); }} .chain-number-label {{ fill:white; font-size:13px; font-weight:780; }}
  .chain-title {{ font-size:20px; font-weight:760; }} .chain-verb {{ font-size:15px; }} .chain-posture {{ fill:var(--muted); font-size:9px; text-anchor:middle; }}
  .carrier-label rect {{ fill:var(--ink); }} .carrier-label text {{ fill:white; font-size:13px; font-weight:760; letter-spacing:.05em; }}
  .path-title {{ font-size:21px; font-weight:780; }} .path-title.path-a {{ fill:var(--blue); }} .path-title.path-b {{ fill:var(--green); }}
  .path-node {{ fill:white; stroke-width:2.5; }} .path-node.path-a {{ stroke:var(--blue); }} .path-node.path-b {{ stroke:var(--green); }}
  .path-arrow.path-a {{ stroke:var(--blue); marker-end:url(#arrow-blue); }} .path-arrow.path-b {{ stroke:var(--green); marker-end:url(#arrow-green); }}
  .path-node-label {{ font-size:15px; font-weight:710; }} .path-posture {{ fill:var(--muted); font-size:10px; font-weight:760; letter-spacing:.05em; }}
  .rack-interface rect {{ fill:var(--paper); stroke:var(--ink); stroke-width:2.5; }} .rack-kicker {{ fill:var(--muted); font-size:11px; }} .rack-title {{ font-size:19px; font-weight:770; }} .rack-copy {{ fill:var(--muted); font-size:13px; }} .rack-separator {{ fill:none; stroke:var(--faint); stroke-width:1.5; }}
  .input-a {{ fill:var(--blue); }} .input-b {{ fill:var(--green); }}
  .path-unavailable {{ fill:rgba(251,236,234,.86); stroke:var(--red); stroke-width:3; }} .unavailable-strike {{ fill:none; stroke:var(--red); stroke-width:5; stroke-dasharray:12 10; }}
  .isolation-label {{ fill:var(--red); }} .isolation-label-copy {{ fill:white; font-size:13px; font-weight:780; }}
  .remaining-outline {{ fill:rgba(231,245,241,.35); stroke:var(--green); stroke-width:4; }} .remaining-label {{ fill:var(--green); font-size:13px; font-weight:780; letter-spacing:.04em; }}
  .conditional-diamond {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:3; }} .conditional-mark {{ fill:var(--amber); font-size:24px; font-weight:800; }}
  .isolation-path-title,.remaining-path-title {{ font-size:22px; font-weight:800; }} .isolation-path-title {{ fill:var(--red); }} .remaining-path-title {{ fill:var(--green); }} .isolation-path-copy,.remaining-path-copy {{ font-size:14px; font-weight:780; letter-spacing:.04em; }} .isolation-path-guard {{ fill:var(--muted); font-size:11px; font-weight:730; letter-spacing:.03em; }} .remaining-carrier {{ fill:none; stroke:var(--green); stroke-width:6; marker-end:url(#arrow-green); }}
  .rack-result-card {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:2.5; }} .rack-result-kicker {{ fill:var(--amber); font-size:12px; font-weight:780; letter-spacing:.06em; }} .rack-result-title {{ font-size:21px; font-weight:780; }} .rack-result-copy {{ font-size:14px; }} .condition-dot {{ fill:var(--green); }} .condition-dot.unresolved {{ fill:var(--amber); }}
  .claim-split rect {{ fill:white; stroke:var(--ink); stroke-width:1.7; }} .claim-title {{ font-size:19px; font-weight:760; }} .claim-copy {{ fill:var(--muted); font-size:13px; }}
  .abilene-card {{ stroke-width:2.2; }} .abilene-card.known-card {{ fill:var(--green-soft); stroke:var(--green); }} .abilene-card.unknown-card {{ fill:var(--amber-soft); stroke:var(--amber); stroke-dasharray:8 6; }}
  .abilene-status {{ font-size:12px; }} .abilene-status.known-card {{ fill:var(--green); }} .abilene-status.unknown-card {{ fill:var(--amber); }}
  .abilene-title {{ font-size:19px; font-weight:760; }} .abilene-copy {{ fill:var(--muted); font-size:13px; }}
  .generic-reference-chain > rect {{ fill:#fafaf8; stroke:var(--faint); stroke-width:2; stroke-dasharray:7 6; }} .reference-label {{ fill:var(--muted); font-size:11px; font-weight:760; letter-spacing:.06em; }}
  .ghost-node {{ fill:white; stroke:var(--faint); stroke-width:1.5; }} .ghost-number {{ fill:var(--blue); font-size:14px; font-weight:800; }} .ghost-label {{ fill:var(--muted); font-size:13px; font-weight:720; }}
  .unknown-path {{ fill:none; stroke:var(--amber); stroke-width:5; stroke-dasharray:10 9; }} .unknown-question {{ fill:var(--amber); font-size:42px; font-weight:820; }}
  .handoff-backdrop {{ fill:#fbfcff; stroke:var(--ink); stroke-width:2.5; }} .handoff-kicker {{ fill:var(--blue); font-size:13px; }} .handoff-title {{ font-size:30px; font-weight:780; }} .handoff-body {{ fill:var(--muted); font-size:15px; }}
  .handoff-node {{ stroke-width:2.3; }} .handoff-known {{ fill:var(--green-soft); stroke:var(--green); }} .rack-boundary-node {{ fill:white; stroke:var(--ink); }} .product-reference {{ fill:var(--blue-soft); stroke:var(--blue); }} .handoff-unknown {{ fill:var(--amber-soft); stroke:var(--amber); stroke-dasharray:8 6; }}
  .handoff-node-kicker {{ fill:var(--muted); font-size:10px; }} .handoff-node-title {{ font-size:20px; font-weight:760; }} .handoff-stop,.handoff-question {{ fill:var(--red); font-size:10px; font-weight:780; letter-spacing:.04em; }} .handoff-question {{ fill:var(--amber); }} .handoff-unknown-arrow {{ stroke:var(--amber); stroke-dasharray:9 7; marker-end:url(#arrow-amber); }}
  footer {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(320px,570px); gap:10px 16px; min-height:0; max-height:48dvh; padding:9px 14px 10px; border-top:1.5px solid var(--ink); }}
  .state-nav {{ display:grid; grid-template-columns:repeat({len(payload["states"])},minmax(0,1fr)); gap:6px; }}
  .state-button {{ display:grid; grid-template-columns:auto 1fr; gap:7px; align-items:center; min-width:0; min-height:44px; padding:7px 8px; border:1.5px solid var(--ink); background:transparent; color:inherit; text-align:left; font:inherit; cursor:pointer; }}
  .state-nav-label {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }} .state-button[aria-selected="true"] {{ background:var(--ink); color:white; }}
  .state-copy {{ min-width:0; align-self:center; }} .state-copy h2 {{ margin:0 0 3px; font-size:16px; }} .state-copy p {{ margin:0; color:var(--muted); font-size:13px; line-height:1.3; }}
  details {{ grid-column:1/-1; min-width:0; min-height:0; border-top:1px solid var(--faint); padding-top:6px; }} details[open] {{ max-height:min(34dvh,320px); overflow:auto; overflow-x:hidden; overscroll-behavior:contain; }}
  summary {{ position:sticky; top:0; z-index:2; cursor:pointer; padding:3px 0; background:var(--paper); font-weight:700; }}
  .fact-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr)); gap:12px; margin-bottom:0; padding:0; list-style:none; }} .fact-card {{ min-width:0; border:1px solid var(--faint); padding:10px 12px; background:white; }}
  .fact-card p {{ margin:5px 0; line-height:1.35; }} .fact-ref,.fact-boundary,.fact-sources,a {{ overflow-wrap:anywhere; word-break:break-word; }} .fact-ref,.fact-boundary {{ color:var(--muted); font-size:11px; }} .fact-sources {{ font-size:12px; }} a {{ color:var(--blue); }}
  .visually-hidden {{ position:absolute !important; width:1px; height:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }}
  .responsive-visual {{ display:none; }} .responsive-layer {{ width:100%; }} .responsive-layer h2 {{ margin:2px 0 8px; font-size:18px; }}
  .responsive-card {{ min-width:0; padding:10px; border:1.5px solid var(--ink); border-radius:9px; background:white; }} .responsive-card h3,.responsive-layer h3 {{ margin:2px 0 5px; font-size:14px; }} .responsive-card p {{ margin:4px 0; line-height:1.35; }}
  .responsive-grid,.responsive-paths {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:7px; }} .responsive-zone ul {{ margin:6px 0; padding-left:18px; }}
  .responsive-boundary {{ margin:8px 0 0; padding:8px; border:1px solid var(--amber); border-radius:7px; background:var(--amber-soft); line-height:1.35; }}
  .responsive-chain {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:7px; }} .responsive-chain-step {{ position:relative; }}
  .responsive-flow {{ display:flex; align-items:stretch; gap:4px; overflow-wrap:anywhere; }} .responsive-flow > span:not(.responsive-arrow) {{ display:grid; place-items:center; flex:1 1 0; min-width:0; padding:7px 4px; border:1px solid var(--blue); border-radius:6px; text-align:center; }} .responsive-arrow {{ align-self:center; flex:0 0 auto; color:var(--blue); font-weight:800; }}
  .responsive-load {{ margin-top:7px; border-color:var(--violet); }} .responsive-isolation-layer {{ position:relative; }} .responsive-isolation {{ border-color:var(--red); }}
  .isolation-active .responsive-path[data-protected-path-id="path_a"] {{ opacity:.58; border-color:var(--red); background:var(--red-soft); text-decoration:line-through; }} .isolation-active .responsive-path[data-protected-path-id="path_a"]::before {{ content:"PATH A UNAVAILABLE · STATIC CONDITION"; display:block; margin-bottom:5px; color:var(--red); font-weight:800; letter-spacing:.05em; text-decoration:none; }}
  .isolation-active .responsive-path[data-protected-path-id="path_b"] {{ border-color:var(--green); background:var(--green-soft); }} .isolation-active .responsive-path[data-protected-path-id="path_b"]::before {{ content:"PATH B REMAINS · CONDITIONAL"; display:block; margin-bottom:5px; color:var(--green); font-weight:800; letter-spacing:.05em; }}
  .responsive-claim-split {{ display:grid; grid-template-columns:1fr 1fr; gap:7px; margin-top:7px; }} .responsive-claim-split article {{ padding:8px; border:1px solid var(--ink); border-radius:7px; background:white; }} .responsive-claim-split p {{ margin:3px 0; line-height:1.35; }}
  .responsive-abilene-grid {{ display:grid; grid-template-columns:1fr 1fr 1fr; gap:7px; }} .responsive-abilene-grid > div {{ display:grid; gap:7px; min-width:0; }} .responsive-known {{ border-color:var(--green); background:var(--green-soft); }} .responsive-unknown {{ border-color:var(--amber); border-style:dashed; background:var(--amber-soft); }} .responsive-generic-chain {{ padding:7px; border:1.5px dashed var(--faint); border-radius:8px; }}
  .responsive-handoff-flow {{ display:grid; grid-template-columns:1fr auto 1fr auto 1fr; gap:5px; align-items:stretch; }} .responsive-handoff-flow article {{ display:grid; gap:5px; min-width:0; padding:8px; border:1.5px solid var(--blue); border-radius:7px; background:white; }} .responsive-handoff-flow > span {{ align-self:center; color:var(--blue); font-weight:800; }}

  @media (max-width:1300px) {{
    .state-button {{ grid-template-columns:1fr; gap:2px; text-align:center; }} .state-nav-label {{ overflow:visible; text-overflow:clip; white-space:normal; }}
  }}

  @media (max-width:1100px) and (min-width:901px) {{
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:6px 10px; }} .visual-shell {{ display:none; }} .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:6px; font-size:12px; }}
    .responsive-chain {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .responsive-abilene-grid {{ grid-template-columns:1fr 1.15fr 1fr; }}
    footer {{ grid-template-columns:minmax(0,1fr) minmax(280px,420px); }} .state-button {{ min-height:40px; padding:5px 6px; }}
  }}
  @media (max-height:520px) and (orientation:landscape) {{
    header {{ grid-template-columns:1fr; padding:5px 12px 4px; }} header .objective,.phase-question {{ display:none; }} h1 {{ margin:0; font-size:19px; }} .eyebrow {{ margin:0; font-size:9px; }}
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:4px 8px; }} .visual-shell {{ display:none; }} .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:4px; font-size:10px; }}
    .responsive-layer h2 {{ margin:1px 0 5px; font-size:15px; }} .responsive-card {{ padding:6px; }} .responsive-card h3,.responsive-layer h3 {{ font-size:12px; }} .responsive-grid,.responsive-paths {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:5px; }}
    .responsive-chain {{ grid-template-columns:repeat(3,minmax(0,1fr)); gap:5px; }} .responsive-boundary {{ margin-top:5px; padding:5px; }} .responsive-abilene-grid {{ gap:5px; }} .responsive-abilene-grid > div {{ gap:5px; }} .responsive-flow > span:not(.responsive-arrow) {{ padding:5px 3px; }}
    footer {{ grid-template-columns:1fr; gap:4px; padding:4px 8px 5px; max-height:49dvh; }} .state-nav {{ gap:4px; }} .state-button {{ grid-template-columns:1fr; gap:0; min-height:32px; padding:3px 4px; text-align:center; font-size:10px; }} .state-number {{ display:none; }} .state-nav-label {{ overflow:visible; text-overflow:clip; white-space:normal; }} .state-copy h2 {{ font-size:12px; margin:0; }} .state-copy p {{ font-size:10px; line-height:1.2; }} details {{ padding-top:2px; }} details[open] {{ max-height:68dvh; }} summary {{ padding:1px 0; font-size:10px; }}
  }}
  @media (max-width:520px) and (orientation:portrait) {{
    header {{ grid-template-columns:1fr; gap:3px; padding:8px 10px 7px; }} h1 {{ font-size:21px; }} .objective {{ font-size:12px; }} .phase-question {{ font-size:10px; }}
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:6px; }} .visual-shell {{ display:none; }} .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:3px; font-size:12px; }}
    .responsive-layer h2 {{ font-size:18px; }} .responsive-grid,.responsive-paths,.responsive-chain,.responsive-abilene-grid,.responsive-claim-split {{ grid-template-columns:1fr; }} .responsive-flow,.responsive-handoff-flow {{ grid-template-columns:1fr; display:grid; }} .responsive-flow .responsive-arrow,.responsive-handoff-flow > span {{ transform:rotate(90deg); justify-self:center; }}
    .responsive-card {{ padding:9px; }} .responsive-card h3,.responsive-layer h3 {{ font-size:14px; }} .responsive-generic-chain {{ max-height:none; }}
    footer {{ grid-template-columns:1fr; gap:6px; padding:6px 8px 7px; max-height:50dvh; }} .state-nav {{ gap:3px; }} .state-button {{ grid-template-columns:1fr; gap:0; min-height:42px; padding:4px 2px; text-align:center; font-size:10px; }} .state-number {{ font-size:9px; }} .state-nav-label {{ overflow:visible; text-overflow:clip; white-space:normal; }} .state-copy h2 {{ font-size:14px; }} .state-copy p {{ font-size:12px; }} details[open] {{ max-height:70dvh; }}
  }}
</style>
</head>
<body>
<header>
  <div><p class="eyebrow">Phase {phase["number"]} · {_escape(phase["title"])}</p><h1>{_escape(payload["pilot"]["title"])}</h1><p class="phase-question">{_escape(phase["anchor_question"])}</p></div>
  <p class="objective">{_escape(payload["pilot"]["learning_objective"])}</p>
</header>
<main>
  <section class="visual-shell" aria-label="Instructor-controlled building-power teaching surface">
    <svg id="visual" role="img" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" aria-labelledby="visual-title visual-description">
      <title id="visual-title">Building-power path teaching surface</title>
      <desc id="visual-description">Six manually selected views explain physical zones, functional gates, generic A and B paths, conditional isolation, Abilene evidence boundaries, and the rack handoff.</desc>
      <defs>
        <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#185f8f"/></marker>
        <marker id="arrow-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#278a76"/></marker>
        <marker id="arrow-amber" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#aa6819"/></marker>
      </defs>
{_zones_svg(payload["spatial_building_zones"])}
{_chain_svg(payload["functional_power_chain"])}
{_paths_svg(payload["generic_protected_paths"])}
{_isolation_svg(payload["conditional_path_isolation"])}
{_abilene_svg(payload["abilene_mapping"], payload["functional_power_chain"])}
{_handoff_svg(payload["phase5_handoff"])}
    </svg>
  </section>
{responsive}
</main>
<footer>
  <nav class="state-nav" role="tablist" aria-label="Manual Phase 4 teaching states">{state_buttons}</nav>
  <section class="state-copy" aria-labelledby="state-title"><h2 id="state-title"></h2><p id="state-instruction"></p></section>
  <p id="state-status" class="visually-hidden" aria-live="polite"></p>
  <details id="evidence-drawer"><summary><span class="evidence-label">Evidence</span><span class="evidence-count"> used in this pilot · {len(payload["evidence"]["facts"])} facts · {len(payload["evidence"]["sources"])} sources</span></summary><ul class="fact-list">{evidence}</ul></details>
</footer>
<script id="pilot-data" type="application/json">{serialized}</script>
<script>
"use strict";
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
const pilot = JSON.parse(document.getElementById("pilot-data").textContent);
const buttons = [...document.querySelectorAll("[data-state-index]")];
const evidenceDrawer = document.getElementById("evidence-drawer");
let current = 0;

function setVisible(selector, selected, dataKey) {{
  document.querySelectorAll(selector).forEach(element => {{
    element.toggleAttribute("hidden", !selected.includes(element.dataset[dataKey]));
  }});
}}

function setLayer(selector, visible) {{
  document.querySelectorAll(selector).forEach(element => {{
    element.toggleAttribute("hidden", !visible);
  }});
}}

function resetTeachingScroll() {{
  window.scrollTo(0, 0);
  if (document.scrollingElement) {{
    document.scrollingElement.scrollTop = 0;
    document.scrollingElement.scrollLeft = 0;
  }}
  [document.querySelector("main"), document.querySelector(".responsive-visual")]
    .forEach(container => {{
      if (!container) return;
      container.scrollTop = 0;
      container.scrollLeft = 0;
    }});
}}

function activate(index, focusButton = false) {{
  current = Math.max(0, Math.min(pilot.states.length - 1, index));
  const state = pilot.states[current];
  const showZones = state.zone_ids.length > 0;
  const showPaths = state.protected_path_ids.length > 0;
  const showIsolation = state.isolation_path_state_ids.length > 0;
  const showAbilene = state.abilene_known_ids.length > 0 || state.abilene_unknown_ids.length > 0;
  const showChain = state.chain_step_ids.length > 0 && !showAbilene;
  document.body.classList.toggle("isolation-active", showIsolation);
  setLayer("[data-zone-layer]", showZones);
  setLayer("[data-chain-layer]", showChain);
  setLayer(".visual-shell [data-path-layer]", showPaths && !showIsolation);
  setLayer(".responsive-visual [data-path-layer]", showPaths);
  setLayer("[data-isolation-layer]", showIsolation);
  setLayer(".visual-shell [data-abilene-layer]", showAbilene && !state.show_phase5_handoff);
  setLayer(".responsive-visual [data-abilene-layer]", showAbilene);
  setLayer("[data-handoff]", state.show_phase5_handoff);
  setVisible("[data-zone-id]", state.zone_ids, "zoneId");
  setVisible("[data-chain-step-id]", state.chain_step_ids, "chainStepId");
  setVisible("[data-generic-chain-step-id]", state.chain_step_ids, "genericChainStepId");
  setVisible("[data-protected-path-id]", state.protected_path_ids, "protectedPathId");
  setVisible("[data-isolation-path-state-id]", state.isolation_path_state_ids, "isolationPathStateId");
  setVisible("[data-abilene-known-id]", state.abilene_known_ids, "abileneKnownId");
  setVisible("[data-abilene-unknown-id]", state.abilene_unknown_ids, "abileneUnknownId");
  buttons.forEach((button, buttonIndex) => {{
    const selected = buttonIndex === current;
    button.setAttribute("aria-selected", String(selected));
    button.tabIndex = selected ? 0 : -1;
  }});
  document.getElementById("state-title").textContent = state.title;
  document.getElementById("state-instruction").textContent = state.instruction;
  document.getElementById("state-status").textContent = `State ${{current + 1}} of ${{pilot.states.length}}: ${{state.title}}. ${{state.instruction}}`;
  resetTeachingScroll();
  if (focusButton) buttons[current].focus();
}}

buttons.forEach((button, index) => button.addEventListener("click", () => activate(index)));
document.querySelector(".state-nav").addEventListener("keydown", event => {{
  let target = null;
  if (event.key === "ArrowRight" || event.key === "ArrowDown") target = current + 1;
  if (event.key === "ArrowLeft" || event.key === "ArrowUp") target = current - 1;
  if (event.key === "Home") target = 0;
  if (event.key === "End") target = pilot.states.length - 1;
  if (target !== null) {{ event.preventDefault(); activate(target, true); }}
}});
evidenceDrawer.addEventListener("toggle", () => {{
  if (!evidenceDrawer.open) resetTeachingScroll();
}});
activate(0);
</script>
</body>
</html>
"""
    return "\n".join(line.rstrip() for line in rendered.splitlines()) + "\n"
