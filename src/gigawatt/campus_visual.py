"""Evidence-bound Phase 3 campus distribution teaching surface."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from gigawatt import teaching_visuals as base

SCHEMA_VERSION = 1
CANVAS_KIND = "campus_distribution_v1"
CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 900

SOURCE_IDS = {"initial_grid", "expansion_grid", "onsite_gas"}
ROLE_IDS = {"ups", "bess", "diesel"}
STAGE_IDS = ["constructed", "energized", "commissioned", "live"]
FAULT_STAGE_IDS = [
    "feeder_disturbance",
    "protection_detects",
    "protective_device_interrupts",
    "faulted_branch_isolated",
]
FAULT_STAGE_POSTURES = {
    "feeder_disturbance": "faulted_branch",
    "protection_detects": "detection_reference",
    "protective_device_interrupts": "open_protective_device",
    "faulted_branch_isolated": "isolated_branch_with_conditional_peers",
}
REMAINING_SERVICE_CONDITION_IDS = [
    "independent_source_and_path",
    "selective_device_coordination",
    "remaining_path_can_carry_load",
]
EQUIPMENT_IDS = ["unit_substation", "switchgear", "ups", "busway"]
GAP_IDS = {
    "dedicated_generic_campus_mv_fanout_reference",
    "building_specific_commissioning_record",
}
STATE_IDS = [
    "one_source_fanout",
    "feeder_fault_isolation",
    "abilene_unknown_merge",
    "separate_resilience_roles",
    "building_power_handoff",
]

TOP_LEVEL_FIELDS = {
    "schema_version",
    "id",
    "title",
    "phase",
    "learning_objective",
    "evidence_files",
    "interaction",
    "canvas",
    "generic_fanout",
    "feeder_fault_isolation",
    "abilene_source_boundary",
    "resilience_roles",
    "building_lifecycle",
    "phase4_handoff",
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
FANOUT_FIELDS = {
    "id",
    "title",
    "body",
    "topology",
    "protection_note",
    "boundary",
    "fact_refs",
}
TOPOLOGY_FIELDS = {
    "source",
    "distribution_node",
    "building_feeders",
    "relation",
}
FAULT_ISOLATION_FIELDS = {
    "title",
    "body",
    "stages",
    "remaining_service",
    "boundary",
}
FAULT_STAGE_FIELDS = {
    "id",
    "title",
    "action",
    "visual_posture",
    "boundary",
    "fact_refs",
}
REMAINING_SERVICE_FIELDS = {
    "id",
    "title",
    "body",
    "conditions",
    "visual_posture",
    "fact_refs",
}
REMAINING_SERVICE_CONDITION_FIELDS = {"id", "text"}
SOURCE_BOUNDARY_FIELDS = {"title", "body", "sources", "merge"}
SOURCE_FIELDS = {
    "id",
    "title",
    "evidence_posture",
    "edge_posture",
    "boundary",
    "fact_refs",
}
MERGE_FIELDS = {
    "id",
    "title",
    "known",
    "unknown",
    "render_posture",
    "fact_refs",
}
ROLES_FIELDS = {"title", "body", "roles", "comparison_boundary"}
ROLE_FIELDS = {
    "id",
    "title",
    "function",
    "architectural_position",
    "role_note",
    "abilene_boundary",
    "fact_refs",
}
BOUNDARY_FIELDS = {"id", "title", "body", "fact_refs"}
LIFECYCLE_FIELDS = {"title", "body", "stages", "campus_scope_boundary"}
STAGE_FIELDS = {
    "id",
    "title",
    "known",
    "boundary",
    "evidence_posture",
    "fact_refs",
}
HANDOFF_FIELDS = {"title", "body", "equipment_verbs", "site_boundary"}
EQUIPMENT_FIELDS = {"id", "equipment", "verb", "fact_refs"}
SITE_BOUNDARY_FIELDS = {"id", "body", "fact_refs"}
GAP_FIELDS = {"id", "gap", "renderer_guard", "related_fact_refs"}
STATE_FIELDS = {
    "id",
    "nav_label",
    "title",
    "instruction",
    "show_generic_fanout",
    "show_feeder_fault_isolation",
    "abilene_source_ids",
    "show_abilene_merge",
    "resilience_role_ids",
    "show_phase4_handoff",
}


class CampusVisualError(base.TeachingVisualError):
    """Raised when Phase 3 escapes its teaching or evidence contract."""


def responsive_layout_contract(
    viewport_width: int,
    viewport_height: int,
) -> dict[str, Any]:
    """Select a readable surface for the supported course viewports."""
    if (
        type(viewport_width) is not int
        or type(viewport_height) is not int
        or viewport_width <= 0
        or viewport_height <= 0
    ):
        raise CampusVisualError("viewport dimensions must be positive integers")
    if viewport_width <= 520 and viewport_height >= viewport_width:
        return {
            "surface": "html",
            "profile": "portrait",
            "columns": 1,
            "minimum_text_px": 12,
            "scroll_axis": "vertical",
        }
    if viewport_width <= 1100:
        return {
            "surface": "html",
            "profile": "tablet" if viewport_height > 520 else "short_landscape",
            "columns": 2,
            "minimum_text_px": 12 if viewport_height > 520 else 10,
            "scroll_axis": "vertical",
        }
    if viewport_width <= 1280 or viewport_height <= 760:
        return {
            "surface": "html",
            "profile": "course_landscape",
            "columns": 2,
            "minimum_text_px": 12,
            "scroll_axis": "vertical",
        }
    return {
        "surface": "svg",
        "profile": "standard",
        "columns": 4,
        "minimum_text_px": 13,
        "scroll_axis": "none",
    }


def _exact(value: Any, fields: set[str], location: str) -> dict[str, Any]:
    try:
        return base._exact_fields(value, fields, location)
    except base.TeachingVisualError as error:
        raise CampusVisualError(str(error)) from error


def _text(value: Any, location: str, *, maximum: int = 240) -> str:
    try:
        return base._text(value, location, maximum=maximum)
    except base.TeachingVisualError as error:
        raise CampusVisualError(str(error)) from error


def _identifier(value: Any, location: str) -> str:
    try:
        return base._id(value, location)
    except base.TeachingVisualError as error:
        raise CampusVisualError(str(error)) from error


def _list(
    value: Any,
    location: str,
    *,
    minimum: int,
    maximum: int,
    item_limit: int = 160,
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
        raise CampusVisualError(str(error)) from error


def _refs(
    value: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[str]:
    try:
        return base._fact_refs(value, location, ledgers)
    except base.TeachingVisualError as error:
        raise CampusVisualError(str(error)) from error


def _normalize_fanout(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.generic_fanout"
    value = _exact(raw, FANOUT_FIELDS, location)
    topology = _exact(value["topology"], TOPOLOGY_FIELDS, f"{location}.topology")
    return {
        "id": _identifier(value["id"], f"{location}.id"),
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "body": _text(value["body"], f"{location}.body", maximum=620),
        "topology": {
            "source": _text(
                topology["source"], f"{location}.topology.source", maximum=100
            ),
            "distribution_node": _text(
                topology["distribution_node"],
                f"{location}.topology.distribution_node",
                maximum=100,
            ),
            "building_feeders": _list(
                topology["building_feeders"],
                f"{location}.topology.building_feeders",
                minimum=3,
                maximum=3,
                item_limit=80,
            ),
            "relation": _text(
                topology["relation"], f"{location}.topology.relation", maximum=180
            ),
        },
        "protection_note": _text(
            value["protection_note"],
            f"{location}.protection_note",
            maximum=620,
        ),
        "boundary": _text(value["boundary"], f"{location}.boundary", maximum=620),
        "fact_refs": _refs(value["fact_refs"], f"{location}.fact_refs", ledgers),
    }


def _normalize_feeder_fault_isolation(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.feeder_fault_isolation"
    value = _exact(raw, FAULT_ISOLATION_FIELDS, location)
    if not isinstance(value["stages"], list) or len(value["stages"]) != len(
        FAULT_STAGE_IDS
    ):
        raise CampusVisualError(
            f"{location}.stages must contain exactly {len(FAULT_STAGE_IDS)} stages"
        )

    stages: list[dict[str, Any]] = []
    stage_ids: list[str] = []
    coordination_ref = (
        "building_power_reference:"
        "selective_fault_isolation_requires_system_coordination"
    )
    for index, raw_stage in enumerate(value["stages"]):
        stage_location = f"{location}.stages[{index}]"
        stage = _exact(raw_stage, FAULT_STAGE_FIELDS, stage_location)
        stage_id = _identifier(stage["id"], f"{stage_location}.id")
        stage_ids.append(stage_id)
        visual_posture = _identifier(
            stage["visual_posture"], f"{stage_location}.visual_posture"
        )
        refs = _refs(stage["fact_refs"], f"{stage_location}.fact_refs", ledgers)
        if coordination_ref not in refs:
            raise CampusVisualError(
                f"{stage_location} must remain bound to coordinated isolation evidence"
            )
        stages.append(
            {
                "id": stage_id,
                "title": _text(stage["title"], f"{stage_location}.title", maximum=100),
                "action": _text(
                    stage["action"], f"{stage_location}.action", maximum=440
                ),
                "visual_posture": visual_posture,
                "boundary": _text(
                    stage["boundary"],
                    f"{stage_location}.boundary",
                    maximum=300,
                ),
                "fact_refs": refs,
            }
        )
    if stage_ids != FAULT_STAGE_IDS:
        raise CampusVisualError(
            "pilot fault-isolation stages must remain in canonical order "
            f"{FAULT_STAGE_IDS}"
        )
    for stage in stages:
        if stage["visual_posture"] != FAULT_STAGE_POSTURES[stage["id"]]:
            raise CampusVisualError(
                f"pilot fault-isolation stage {stage['id']!r} has the wrong visual posture"
            )

    remaining_location = f"{location}.remaining_service"
    remaining = _exact(
        value["remaining_service"],
        REMAINING_SERVICE_FIELDS,
        remaining_location,
    )
    if not isinstance(remaining["conditions"], list) or len(
        remaining["conditions"]
    ) != len(REMAINING_SERVICE_CONDITION_IDS):
        raise CampusVisualError(
            f"{remaining_location}.conditions must contain exactly three conditions"
        )
    conditions: list[dict[str, str]] = []
    condition_ids: list[str] = []
    for index, raw_condition in enumerate(remaining["conditions"]):
        condition_location = f"{remaining_location}.conditions[{index}]"
        condition = _exact(
            raw_condition,
            REMAINING_SERVICE_CONDITION_FIELDS,
            condition_location,
        )
        condition_id = _identifier(condition["id"], f"{condition_location}.id")
        condition_ids.append(condition_id)
        conditions.append(
            {
                "id": condition_id,
                "text": _text(
                    condition["text"], f"{condition_location}.text", maximum=180
                ),
            }
        )
    if condition_ids != REMAINING_SERVICE_CONDITION_IDS:
        raise CampusVisualError(
            "pilot remaining-service conditions must remain in canonical order "
            f"{REMAINING_SERVICE_CONDITION_IDS}"
        )
    remaining_id = _identifier(remaining["id"], f"{remaining_location}.id")
    remaining_posture = _identifier(
        remaining["visual_posture"],
        f"{remaining_location}.visual_posture",
    )
    if remaining_id != "conditional_remaining_service" or remaining_posture != (
        "conditional_not_guaranteed"
    ):
        raise CampusVisualError(
            "remaining service must stay explicitly conditional and not guaranteed"
        )
    remaining_title = _text(
        remaining["title"], f"{remaining_location}.title", maximum=140
    )
    if "conditional" not in remaining_title.casefold() or "not guaranteed" not in (
        remaining_title.casefold()
    ):
        raise CampusVisualError(
            "remaining-service title must state conditional, not guaranteed"
        )
    remaining_refs = _refs(
        remaining["fact_refs"], f"{remaining_location}.fact_refs", ledgers
    )
    continuity_ref = "building_power_reference:dual_path_continuity_conditions"
    if not {coordination_ref, continuity_ref}.issubset(remaining_refs):
        raise CampusVisualError(
            "remaining service must bind coordination and continuity-condition evidence"
        )

    boundary_location = f"{location}.boundary"
    boundary = _exact(value["boundary"], BOUNDARY_FIELDS, boundary_location)
    boundary_id = _identifier(boundary["id"], f"{boundary_location}.id")
    boundary_body = _text(boundary["body"], f"{boundary_location}.body", maximum=560)
    if boundary_id != "generic_sequence_not_site_guarantee" or not all(
        phrase in boundary_body.casefold()
        for phrase in ("abilene", "automatic restoration", "uninterrupted service")
    ):
        raise CampusVisualError(
            "fault-isolation boundary must withhold Abilene topology, automatic "
            "restoration, and uninterrupted service"
        )

    return {
        "title": _text(value["title"], f"{location}.title", maximum=170),
        "body": _text(value["body"], f"{location}.body", maximum=620),
        "stages": stages,
        "remaining_service": {
            "id": remaining_id,
            "title": remaining_title,
            "body": _text(remaining["body"], f"{remaining_location}.body", maximum=620),
            "conditions": conditions,
            "visual_posture": remaining_posture,
            "fact_refs": remaining_refs,
        },
        "boundary": {
            "id": boundary_id,
            "title": _text(
                boundary["title"], f"{boundary_location}.title", maximum=150
            ),
            "body": boundary_body,
            "fact_refs": _refs(
                boundary["fact_refs"], f"{boundary_location}.fact_refs", ledgers
            ),
        },
    }


def _normalize_source_boundary(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.abilene_source_boundary"
    value = _exact(raw, SOURCE_BOUNDARY_FIELDS, location)
    if not isinstance(value["sources"], list) or len(value["sources"]) != 3:
        raise CampusVisualError(f"{location}.sources must contain exactly three lanes")
    sources: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_source in enumerate(value["sources"]):
        source_location = f"{location}.sources[{index}]"
        source = _exact(raw_source, SOURCE_FIELDS, source_location)
        source_id = _identifier(source["id"], f"{source_location}.id")
        ids.append(source_id)
        edge_posture = _identifier(
            source["edge_posture"], f"{source_location}.edge_posture"
        )
        if edge_posture != "stop_at_unknown_merge":
            raise CampusVisualError(
                f"{source_location}.edge_posture must stop at unknown merge"
            )
        sources.append(
            {
                "id": source_id,
                "title": _text(
                    source["title"], f"{source_location}.title", maximum=130
                ),
                "evidence_posture": _text(
                    source["evidence_posture"],
                    f"{source_location}.evidence_posture",
                    maximum=220,
                ),
                "edge_posture": edge_posture,
                "boundary": _text(
                    source["boundary"],
                    f"{source_location}.boundary",
                    maximum=440,
                ),
                "fact_refs": _refs(
                    source["fact_refs"], f"{source_location}.fact_refs", ledgers
                ),
            }
        )
    if len(ids) != len(set(ids)) or set(ids) != SOURCE_IDS:
        raise CampusVisualError(
            "pilot source lanes must be initial grid, expansion grid, and onsite gas"
        )
    merge_location = f"{location}.merge"
    merge = _exact(value["merge"], MERGE_FIELDS, merge_location)
    render_posture = _identifier(
        merge["render_posture"], f"{merge_location}.render_posture"
    )
    if render_posture != "unresolved_boundary":
        raise CampusVisualError(
            f"{merge_location}.render_posture must be unresolved_boundary"
        )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "body": _text(value["body"], f"{location}.body", maximum=620),
        "sources": sources,
        "merge": {
            "id": _identifier(merge["id"], f"{merge_location}.id"),
            "title": _text(merge["title"], f"{merge_location}.title", maximum=130),
            "known": _text(merge["known"], f"{merge_location}.known", maximum=480),
            "unknown": _text(
                merge["unknown"], f"{merge_location}.unknown", maximum=620
            ),
            "render_posture": render_posture,
            "fact_refs": _refs(
                merge["fact_refs"], f"{merge_location}.fact_refs", ledgers
            ),
        },
    }


def _normalize_roles(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.resilience_roles"
    value = _exact(raw, ROLES_FIELDS, location)
    if not isinstance(value["roles"], list) or len(value["roles"]) != 3:
        raise CampusVisualError(f"{location}.roles must contain exactly three roles")
    roles: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_role in enumerate(value["roles"]):
        role_location = f"{location}.roles[{index}]"
        role = _exact(raw_role, ROLE_FIELDS, role_location)
        role_id = _identifier(role["id"], f"{role_location}.id")
        ids.append(role_id)
        roles.append(
            {
                "id": role_id,
                "title": _text(role["title"], f"{role_location}.title", maximum=100),
                "function": _text(
                    role["function"], f"{role_location}.function", maximum=190
                ),
                "architectural_position": _text(
                    role["architectural_position"],
                    f"{role_location}.architectural_position",
                    maximum=160,
                ),
                "role_note": _text(
                    role["role_note"], f"{role_location}.role_note", maximum=620
                ),
                "abilene_boundary": _text(
                    role["abilene_boundary"],
                    f"{role_location}.abilene_boundary",
                    maximum=620,
                ),
                "fact_refs": _refs(
                    role["fact_refs"], f"{role_location}.fact_refs", ledgers
                ),
            }
        )
    if len(ids) != len(set(ids)) or set(ids) != ROLE_IDS:
        raise CampusVisualError("pilot roles must be UPS, BESS, and diesel")
    boundary_location = f"{location}.comparison_boundary"
    boundary = _exact(value["comparison_boundary"], BOUNDARY_FIELDS, boundary_location)
    return {
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "body": _text(value["body"], f"{location}.body", maximum=620),
        "roles": roles,
        "comparison_boundary": {
            "id": _identifier(boundary["id"], f"{boundary_location}.id"),
            "title": _text(
                boundary["title"], f"{boundary_location}.title", maximum=130
            ),
            "body": _text(boundary["body"], f"{boundary_location}.body", maximum=560),
            "fact_refs": _refs(
                boundary["fact_refs"], f"{boundary_location}.fact_refs", ledgers
            ),
        },
    }


def _normalize_lifecycle(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.building_lifecycle"
    value = _exact(raw, LIFECYCLE_FIELDS, location)
    if not isinstance(value["stages"], list) or len(value["stages"]) != 4:
        raise CampusVisualError(f"{location}.stages must contain exactly four stages")
    stages: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_stage in enumerate(value["stages"]):
        stage_location = f"{location}.stages[{index}]"
        stage = _exact(raw_stage, STAGE_FIELDS, stage_location)
        stage_id = _identifier(stage["id"], f"{stage_location}.id")
        ids.append(stage_id)
        stages.append(
            {
                "id": stage_id,
                "title": _text(stage["title"], f"{stage_location}.title", maximum=90),
                "known": _text(stage["known"], f"{stage_location}.known", maximum=620),
                "boundary": _text(
                    stage["boundary"], f"{stage_location}.boundary", maximum=560
                ),
                "evidence_posture": _identifier(
                    stage["evidence_posture"],
                    f"{stage_location}.evidence_posture",
                ),
                "fact_refs": _refs(
                    stage["fact_refs"], f"{stage_location}.fact_refs", ledgers
                ),
            }
        )
    if ids != STAGE_IDS:
        raise CampusVisualError(
            f"pilot lifecycle stages must remain in canonical order {STAGE_IDS}"
        )
    commissioned = stages[2]
    if "?" not in commissioned["title"] or commissioned["evidence_posture"] != (
        "operational_milestone_with_commissioning_gap"
    ):
        raise CampusVisualError(
            "Commissioned must remain explicitly unresolved in the lifecycle ladder"
        )
    boundary_location = f"{location}.campus_scope_boundary"
    boundary = _exact(
        value["campus_scope_boundary"], BOUNDARY_FIELDS, boundary_location
    )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "body": _text(value["body"], f"{location}.body", maximum=620),
        "stages": stages,
        "campus_scope_boundary": {
            "id": _identifier(boundary["id"], f"{boundary_location}.id"),
            "title": _text(
                boundary["title"], f"{boundary_location}.title", maximum=130
            ),
            "body": _text(boundary["body"], f"{boundary_location}.body", maximum=560),
            "fact_refs": _refs(
                boundary["fact_refs"], f"{boundary_location}.fact_refs", ledgers
            ),
        },
    }


def _normalize_handoff(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.phase4_handoff"
    value = _exact(raw, HANDOFF_FIELDS, location)
    if not isinstance(value["equipment_verbs"], list) or len(
        value["equipment_verbs"]
    ) != len(EQUIPMENT_IDS):
        raise CampusVisualError(
            f"{location}.equipment_verbs must contain exactly four functions"
        )
    equipment_verbs: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_equipment in enumerate(value["equipment_verbs"]):
        equipment_location = f"{location}.equipment_verbs[{index}]"
        equipment = _exact(raw_equipment, EQUIPMENT_FIELDS, equipment_location)
        equipment_id = _identifier(equipment["id"], f"{equipment_location}.id")
        ids.append(equipment_id)
        equipment_verbs.append(
            {
                "id": equipment_id,
                "equipment": _text(
                    equipment["equipment"],
                    f"{equipment_location}.equipment",
                    maximum=90,
                ),
                "verb": _text(
                    equipment["verb"],
                    f"{equipment_location}.verb",
                    maximum=220,
                ),
                "fact_refs": _refs(
                    equipment["fact_refs"],
                    f"{equipment_location}.fact_refs",
                    ledgers,
                ),
            }
        )
    if ids != EQUIPMENT_IDS:
        raise CampusVisualError(
            f"pilot handoff equipment must remain in canonical order {EQUIPMENT_IDS}"
        )
    boundary_location = f"{location}.site_boundary"
    boundary = _exact(value["site_boundary"], SITE_BOUNDARY_FIELDS, boundary_location)
    return {
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "body": _text(value["body"], f"{location}.body", maximum=620),
        "equipment_verbs": equipment_verbs,
        "site_boundary": {
            "id": _identifier(boundary["id"], f"{boundary_location}.id"),
            "body": _text(boundary["body"], f"{boundary_location}.body", maximum=520),
            "fact_refs": _refs(
                boundary["fact_refs"], f"{boundary_location}.fact_refs", ledgers
            ),
        },
    }


def _normalize_gaps(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    location = "pilot manifest.evidence_gaps"
    if not isinstance(raw, list) or len(raw) != 2:
        raise CampusVisualError(f"{location} must contain exactly two guards")
    gaps: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_gap in enumerate(raw):
        gap_location = f"{location}[{index}]"
        gap = _exact(raw_gap, GAP_FIELDS, gap_location)
        gap_id = _identifier(gap["id"], f"{gap_location}.id")
        ids.append(gap_id)
        gaps.append(
            {
                "id": gap_id,
                "gap": _text(gap["gap"], f"{gap_location}.gap", maximum=620),
                "renderer_guard": _text(
                    gap["renderer_guard"],
                    f"{gap_location}.renderer_guard",
                    maximum=520,
                ),
                "related_fact_refs": _refs(
                    gap["related_fact_refs"],
                    f"{gap_location}.related_fact_refs",
                    ledgers,
                ),
            }
        )
    if len(ids) != len(set(ids)) or set(ids) != GAP_IDS:
        raise CampusVisualError("pilot evidence-gap guard set is incomplete")
    return gaps


def _normalize_states(
    raw: Any,
    *,
    source_ids: set[str],
    role_ids: set[str],
) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(STATE_IDS):
        raise CampusVisualError(
            f"pilot manifest.states must contain exactly {len(STATE_IDS)} states"
        )
    states: list[dict[str, Any]] = []
    ids: list[str] = []
    nav_labels: list[str] = []
    used_sources: set[str] = set()
    used_roles: set[str] = set()
    feeder_fault_state_count = 0
    for index, raw_state in enumerate(raw):
        location = f"pilot manifest.states[{index}]"
        state = _exact(raw_state, STATE_FIELDS, location)
        state_id = _identifier(state["id"], f"{location}.id")
        selected_sources = _list(
            state["abilene_source_ids"],
            f"{location}.abilene_source_ids",
            minimum=0,
            maximum=3,
            item_limit=60,
        )
        selected_roles = _list(
            state["resilience_role_ids"],
            f"{location}.resilience_role_ids",
            minimum=0,
            maximum=3,
            item_limit=60,
        )
        unknown_sources = sorted(set(selected_sources) - source_ids)
        unknown_roles = sorted(set(selected_roles) - role_ids)
        if unknown_sources or unknown_roles:
            raise CampusVisualError(
                f"{location}: unknown sources={unknown_sources} roles={unknown_roles}"
            )
        for flag in (
            "show_generic_fanout",
            "show_feeder_fault_isolation",
            "show_abilene_merge",
            "show_phase4_handoff",
        ):
            if not isinstance(state[flag], bool):
                raise CampusVisualError(f"{location}.{flag} must be boolean")
        primary_layers = (
            state["show_generic_fanout"],
            state["show_feeder_fault_isolation"],
            bool(selected_sources),
            bool(selected_roles),
            state["show_phase4_handoff"],
        )
        if sum(primary_layers) != 1:
            raise CampusVisualError(
                f"{location}: state must select exactly one primary teaching layer"
            )
        if state["show_abilene_merge"] != bool(selected_sources):
            raise CampusVisualError(
                f"{location}: Abilene source lanes and unresolved merge must stay together"
            )
        nav_label = _text(state["nav_label"], f"{location}.nav_label", maximum=24)
        ids.append(state_id)
        nav_labels.append(nav_label)
        used_sources.update(selected_sources)
        used_roles.update(selected_roles)
        feeder_fault_state_count += int(state["show_feeder_fault_isolation"])
        states.append(
            {
                "id": state_id,
                "nav_label": nav_label,
                "title": _text(state["title"], f"{location}.title", maximum=150),
                "instruction": _text(
                    state["instruction"], f"{location}.instruction", maximum=520
                ),
                "show_generic_fanout": state["show_generic_fanout"],
                "show_feeder_fault_isolation": state["show_feeder_fault_isolation"],
                "abilene_source_ids": selected_sources,
                "show_abilene_merge": state["show_abilene_merge"],
                "resilience_role_ids": selected_roles,
                "show_phase4_handoff": state["show_phase4_handoff"],
            }
        )
    if ids != STATE_IDS:
        raise CampusVisualError(
            f"pilot manifest states must remain in canonical order {STATE_IDS}"
        )
    if len(nav_labels) != len(set(nav_labels)):
        raise CampusVisualError("pilot manifest state nav labels must be unique")
    if used_sources != source_ids or used_roles != role_ids:
        raise CampusVisualError(
            "pilot states must use every authored source and resilience role"
        )
    if feeder_fault_state_count != 1 or not states[1]["show_feeder_fault_isolation"]:
        raise CampusVisualError(
            "exactly the second pilot state must teach feeder-fault isolation"
        )
    if not states[-1]["show_phase4_handoff"] or any(
        state["show_phase4_handoff"] for state in states[:-1]
    ):
        raise CampusVisualError(
            "only the final pilot state may reveal the Phase 4 handoff"
        )
    return states


def _collect_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {"fact_refs", "related_fact_refs"}:
                refs.update(nested)
            else:
                refs.update(_collect_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(_collect_refs(nested))
    return refs


def compile_campus_distribution(
    manifest: dict[str, Any],
    evidence_ledgers: Mapping[str, dict[str, Any]],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Validate and normalize the Phase 3 campus teaching payload."""
    manifest = _exact(manifest, TOP_LEVEL_FIELDS, "pilot manifest")
    forbidden = base._forbidden_fields(manifest)
    if forbidden:
        raise CampusVisualError(
            f"pilot manifest contains pacing or scripting fields: {forbidden}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise CampusVisualError("pilot manifest schema_version must be 1")
    source_digest = base.validate_source_digest(source_digest)
    declared_ledgers, ledgers = base.validate_evidence_ledgers(
        manifest, evidence_ledgers
    )
    interaction = base.validate_manual_interaction(
        manifest["interaction"], location="pilot manifest.interaction"
    )
    phase = _exact(manifest["phase"], PHASE_FIELDS, "pilot manifest.phase")
    if type(phase["number"]) is not int or phase["number"] != 3:
        raise CampusVisualError("pilot manifest.phase.number must be integer 3")
    canvas = _exact(manifest["canvas"], CANVAS_FIELDS, "pilot manifest.canvas")
    if canvas["kind"] != CANVAS_KIND:
        raise CampusVisualError(f"pilot manifest.canvas.kind must be {CANVAS_KIND!r}")
    if canvas["width"] != CANVAS_WIDTH or canvas["height"] != CANVAS_HEIGHT:
        raise CampusVisualError(
            f"pilot manifest.canvas must be {CANVAS_WIDTH} by {CANVAS_HEIGHT}"
        )
    contract = _exact(
        canvas["contract"], CONTRACT_FIELDS, "pilot manifest.canvas.contract"
    )
    expected_contract = {
        "state_selection": "exclusive_single_primary_layer",
        "primary_layers": [
            "generic_fanout",
            "feeder_fault_isolation",
            "abilene_source_boundary",
            "resilience_roles",
            "phase4_handoff",
        ],
        "evidence_binding": "content_record_fact_refs",
        "geometry_owner": "campus_distribution_renderer",
        "handoff_requires": "feeder_fault_isolation",
    }
    if contract != expected_contract:
        raise CampusVisualError(
            "pilot manifest.canvas.contract must match campus_distribution_v1"
        )

    fanout = _normalize_fanout(manifest["generic_fanout"], ledgers)
    feeder_fault_isolation = _normalize_feeder_fault_isolation(
        manifest["feeder_fault_isolation"], ledgers
    )
    source_boundary = _normalize_source_boundary(
        manifest["abilene_source_boundary"], ledgers
    )
    roles = _normalize_roles(manifest["resilience_roles"], ledgers)
    lifecycle = _normalize_lifecycle(manifest["building_lifecycle"], ledgers)
    handoff = _normalize_handoff(manifest["phase4_handoff"], ledgers)
    gaps = _normalize_gaps(manifest["evidence_gaps"], ledgers)
    states = _normalize_states(
        manifest["states"],
        source_ids={source["id"] for source in source_boundary["sources"]},
        role_ids={role["id"] for role in roles["roles"]},
    )
    content = {
        "generic_fanout": fanout,
        "feeder_fault_isolation": feeder_fault_isolation,
        "abilene_source_boundary": source_boundary,
        "resilience_roles": roles,
        "building_lifecycle": lifecycle,
        "phase4_handoff": handoff,
        "evidence_gaps": gaps,
    }
    evidence = base.compile_evidence_cards(
        _collect_refs(content),
        ledgers,
        ledger_ids=declared_ledgers,
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "pilot": {
            "id": _identifier(manifest["id"], "pilot manifest.id"),
            "title": _text(manifest["title"], "pilot manifest.title", maximum=140),
            "phase": {
                "id": _identifier(phase["id"], "pilot manifest.phase.id"),
                "number": 3,
                "title": _text(
                    phase["title"], "pilot manifest.phase.title", maximum=100
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
                maximum=480,
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
        raise CampusVisualError(
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
    refs = record.get("fact_refs", record.get("related_fact_refs", []))
    return "Evidence: " + ", ".join(refs)


def _iso_building(
    *,
    x: int,
    y: int,
    width: int,
    height: int,
    depth: int,
    label: str,
    css_class: str = "",
) -> str:
    right = x + width
    bottom = y + height
    return (
        f'<g class="iso-building {css_class}">'
        f'<polygon class="iso-building-front" points="{x},{y} {right},{y} {right},{bottom} {x},{bottom}"/>'
        f'<polygon class="iso-building-side" points="{right},{y} {right + depth},{y - depth // 2} '
        f'{right + depth},{bottom - depth // 2} {right},{bottom}"/>'
        f'<polygon class="iso-building-top" points="{x},{y} {x + depth},{y - depth // 2} '
        f'{right + depth},{y - depth // 2} {right},{y}"/>'
        f'<path class="iso-window" d="M {x + 24} {y + 36} H {right - 24} '
        f'M {x + 24} {y + 70} H {right - 24} M {x + 24} {y + 104} H {right - 24}"/>'
        f'<text class="iso-building-label centered" x="{x + width / 2}" y="{bottom + 24}">{_escape(label)}</text>'
        "</g>"
    )


def _fanout_svg(record: Mapping[str, Any]) -> str:
    topology = record["topology"]
    feeders = list(topology["building_feeders"])
    buildings = (
        _iso_building(
            x=965,
            y=250,
            width=210,
            height=150,
            depth=70,
            label=feeders[0],
            css_class="building-a",
        ),
        _iso_building(
            x=1180,
            y=470,
            width=210,
            height=150,
            depth=70,
            label=feeders[1],
            css_class="building-b",
        ),
        _iso_building(
            x=760,
            y=480,
            width=210,
            height=150,
            depth=70,
            label=feeders[2],
            css_class="building-c",
        ),
    )
    return (
        "<g data-generic-fanout hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(record['protection_note'])} {_escape(_fact_description(record))}</desc>"
        '<rect class="campus-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="76" y="88">GENERIC CAMPUS ORIENTATION · NOT ABILENE</text>'
        + _wrapped(
            str(record["title"]),
            x=76,
            y=132,
            width_chars=78,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<polygon class="campus-ground" points="270,310 940,190 1450,440 790,780"/>'
        + '<path class="campus-grid" d="M 420 285 L 1080 650 M 610 250 L 1250 570 M 810 220 L 1390 490 M 330 390 L 960 260 M 480 500 L 1140 350 M 650 610 L 1300 460"/>'
        + '<rect class="source-boundary-card" x="90" y="380" width="250" height="142" rx="14"/>'
        + _wrapped(
            str(topology["source"]),
            x=215,
            y=438,
            width_chars=24,
            line_height=22,
            css_class="source-boundary-title centered",
            maximum_lines=3,
            center_lines=True,
        )
        + '<path class="fanout-feeder incoming-feeder" d="M 340 451 L 515 425"/>'
        + '<polygon class="iso-gate-top" points="515,390 585,365 710,405 640,432"/>'
        + '<polygon class="iso-gate-front" points="515,390 640,432 640,535 515,492"/>'
        + '<polygon class="iso-gate-side" points="640,432 710,405 710,508 640,535"/>'
        + _wrapped(
            str(topology["distribution_node"]),
            x=612,
            y=558,
            width_chars=27,
            line_height=20,
            css_class="distribution-label centered",
            maximum_lines=2,
            center_lines=True,
        )
        + '<path class="fanout-bus" d="M 700 465 L 1050 408"/>'
        + '<path class="fanout-feeder" d="M 870 438 L 1010 355"/>'
        + '<path class="fanout-feeder" d="M 1010 415 L 1210 520"/>'
        + '<path class="fanout-feeder" d="M 780 453 L 835 515"/>'
        + "".join(buildings)
        + '<g class="orientation-compass"><circle cx="1450" cy="155" r="45"/>'
        + '<path d="M 1450 188 V 125 M 1450 125 L 1438 143 M 1450 125 L 1462 143"/>'
        + '<text class="compass-label centered" x="1450" y="114">N</text></g>'
        + f'<text class="relation-label" x="80" y="692">{_escape(topology["relation"])}</text>'
        + '<rect class="scope-box" x="80" y="742" width="1440" height="86" rx="10"/>'
        + _wrapped(
            str(record["boundary"]),
            x=108,
            y=778,
            width_chars=146,
            line_height=20,
            css_class="scope-copy",
            maximum_lines=3,
        )
        + "</g>"
    )


def _fault_stage_icon(stage_id: str, *, x: int, y: int) -> str:
    if stage_id == "feeder_disturbance":
        return (
            f'<g class="fault-icon disturbance-icon" aria-hidden="true">'
            f'<path class="fault-source-line" d="M {x} {y} H {x + 82}"/>'
            f'<circle class="fault-node" cx="{x + 96}" cy="{y}" r="14"/>'
            f'<path class="fault-normal-branch" d="M {x + 110} {y} H {x + 230} M {x + 145} {y} V {y - 42} H {x + 230}"/>'
            f'<path class="faulted-branch" d="M {x + 145} {y} V {y + 48} H {x + 220}"/>'
            f'<path class="fault-bolt" d="M {x + 226} {y + 20} L {x + 207} {y + 55} H {x + 225} L {x + 210} {y + 88} L {x + 250} {y + 44} H {x + 229} Z"/>'
            "</g>"
        )
    if stage_id == "protection_detects":
        return (
            f'<g class="fault-icon detect-icon" aria-hidden="true">'
            f'<path class="fault-source-line" d="M {x} {y} H {x + 250}"/>'
            f'<circle class="detection-ring" cx="{x + 124}" cy="{y}" r="48"/>'
            f'<circle class="detection-core" cx="{x + 124}" cy="{y}" r="19"/>'
            f'<path class="detection-wave" d="M {x + 75} {y - 57} Q {x + 124} {y - 88} {x + 173} {y - 57} M {x + 72} {y + 57} Q {x + 124} {y + 88} {x + 176} {y + 57}"/>'
            f'<text class="fault-icon-label centered" x="{x + 124}" y="{y + 5}">DETECT</text>'
            "</g>"
        )
    if stage_id == "protective_device_interrupts":
        return (
            f'<g class="fault-icon interrupt-icon" aria-hidden="true">'
            f'<path class="fault-source-line" d="M {x} {y} H {x + 93} M {x + 165} {y} H {x + 250}"/>'
            f'<circle class="breaker-contact" cx="{x + 101}" cy="{y}" r="8"/>'
            f'<circle class="breaker-contact" cx="{x + 157}" cy="{y}" r="8"/>'
            f'<path class="open-breaker" d="M {x + 108} {y - 4} L {x + 148} {y - 40}"/>'
            f'<path class="interrupt-stop" d="M {x + 129} {y + 30} V {y + 76}"/>'
            "</g>"
        )
    return (
        f'<g class="fault-icon isolate-icon" aria-hidden="true">'
        f'<circle class="fault-node" cx="{x + 56}" cy="{y}" r="14"/>'
        f'<path class="fault-normal-branch conditional-branch" d="M {x + 70} {y} H {x + 142} V {y - 48} H {x + 238} M {x + 142} {y} V {y + 48} H {x + 238}"/>'
        f'<text class="conditional-question centered" x="{x + 250}" y="{y - 41}">?</text>'
        f'<text class="conditional-question centered" x="{x + 250}" y="{y + 55}">?</text>'
        f'<path class="faulted-branch" d="M {x + 70} {y} H {x + 116}"/>'
        f'<path class="isolation-bars" d="M {x + 124} {y - 26} V {y + 26} M {x + 140} {y - 26} V {y + 26}"/>'
        f'<path class="faulted-branch isolated-tail" d="M {x + 148} {y} H {x + 222}"/>'
        f'<text class="fault-icon-label centered" x="{x + 185}" y="{y + 35}">ISOLATED</text>'
        "</g>"
    )


def _fault_stage_svg(record: Mapping[str, Any], *, x: int, index: int) -> str:
    return (
        f'<g data-feeder-fault-stage-id="{_escape(record["id"])}">'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['action'])} {_escape(record['boundary'])} {_escape(_fact_description(record))}</desc>"
        f'<rect class="fault-stage-card" x="{x}" y="190" width="330" height="320" rx="14"/>'
        f'<circle class="fault-stage-number" cx="{x + 28}" cy="220" r="16"/>'
        f'<text class="fault-stage-number-label centered" x="{x + 28}" y="226">{index + 1}</text>'
        + _wrapped(
            str(record["title"]),
            x=x + 56,
            y=217,
            width_chars=28,
            line_height=20,
            css_class="fault-stage-title",
            maximum_lines=2,
        )
        + _fault_stage_icon(str(record["id"]), x=x + 38, y=320)
        + _wrapped(
            str(record["action"]),
            x=x + 24,
            y=413,
            width_chars=39,
            line_height=17,
            css_class="fault-stage-action",
            maximum_lines=4,
        )
        + _wrapped(
            str(record["boundary"]),
            x=x + 24,
            y=482,
            width_chars=42,
            line_height=14,
            css_class="fault-stage-boundary",
            maximum_lines=2,
        )
        + "</g>"
    )


def _feeder_fault_isolation_svg(record: Mapping[str, Any]) -> str:
    stages = list(record["stages"])
    remaining = record["remaining_service"]
    boundary = record["boundary"]
    stage_x = (72, 442, 812, 1182)
    conditions = []
    condition_x = (92, 386, 680)
    for index, (condition, x) in enumerate(
        zip(remaining["conditions"], condition_x, strict=True)
    ):
        conditions.append(
            f'<g data-remaining-service-condition-id="{_escape(condition["id"])}">'
            f'<rect class="remaining-condition-card" x="{x}" y="608" width="274" height="82" rx="9"/>'
            f'<circle class="remaining-condition-number" cx="{x + 25}" cy="633" r="14"/>'
            f'<text class="remaining-condition-number-label centered" x="{x + 25}" y="638">{index + 1}</text>'
            + _wrapped(
                str(condition["text"]),
                x=x + 49,
                y=630,
                width_chars=29,
                line_height=16,
                css_class="remaining-condition-copy",
                maximum_lines=3,
            )
            + "</g>"
        )
    return (
        "<g data-feeder-fault-isolation hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(remaining['body'])} {_escape(_fact_description(boundary))}</desc>"
        '<rect class="campus-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="76" y="86">GENERIC FEEDER PROTECTION · CAUSAL SEQUENCE</text>'
        + _wrapped(
            str(record["title"]),
            x=76,
            y=126,
            width_chars=78,
            line_height=27,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<text class="fault-sequence-label centered" x="800" y="173">DISTURBANCE → DETECT → INTERRUPT → ISOLATE</text>'
        + "".join(
            _fault_stage_svg(stage, x=x, index=index)
            for index, (stage, x) in enumerate(zip(stages, stage_x, strict=True))
        )
        + '<path class="fault-stage-arrow" d="M 408 350 H 432 M 778 350 H 802 M 1148 350 H 1172"/>'
        + '<rect class="remaining-service-panel" x="72" y="548" width="1440" height="172" rx="14"/>'
        + f'<text class="remaining-service-title" x="96" y="582">{_escape(remaining["title"])}</text>'
        + "".join(conditions)
        + '<path class="remaining-condition-arrow" d="M 960 649 H 986"/>'
        + '<rect class="conditional-outcome-card" x="996" y="608" width="496" height="82" rx="9"/>'
        + '<text class="conditional-outcome-kicker" x="1020" y="634">OTHER BUILDINGS</text>'
        + '<text class="conditional-outcome-title" x="1020" y="659">CONDITIONAL · NOT GUARANTEED</text>'
        + '<text class="conditional-outcome-copy" x="1020" y="681">Only if all three conditions hold.</text>'
        + '<rect class="fault-boundary-card" x="72" y="744" width="1440" height="86" rx="10"/>'
        + f'<text class="fault-boundary-title" x="98" y="774">{_escape(boundary["title"])}</text>'
        + _wrapped(
            str(boundary["body"]),
            x=98,
            y=804,
            width_chars=146,
            line_height=18,
            css_class="fault-boundary-copy",
            maximum_lines=2,
        )
        + "</g>"
    )


def _source_lane_svg(record: Mapping[str, Any], *, y: int) -> str:
    return (
        f'<g data-abilene-source-id="{_escape(record["id"])}" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['evidence_posture'])} {_escape(record['boundary'])} {_escape(_fact_description(record))}</desc>"
        f'<rect class="source-lane-card" x="72" y="{y}" width="650" height="164" rx="14"/>'
        f'<text class="source-lane-title" x="100" y="{y + 38}">{_escape(record["title"])}</text>'
        + _wrapped(
            str(record["evidence_posture"]),
            x=100,
            y=y + 71,
            width_chars=67,
            line_height=19,
            css_class="source-lane-posture",
            maximum_lines=2,
        )
        + _wrapped(
            str(record["boundary"]),
            x=100,
            y=y + 119,
            width_chars=67,
            line_height=18,
            css_class="source-lane-boundary",
            maximum_lines=3,
        )
        + f'<path class="source-stop-line" d="M 722 {y + 82} H 958"/>'
        + f'<path class="source-stop-bar" d="M 958 {y + 58} V {y + 106}"/>'
        + f'<text class="source-stop-label centered" x="840" y="{y + 66}">STOPS AT UNKNOWN MERGE</text>'
        + "</g>"
    )


def _source_boundary_svg(record: Mapping[str, Any]) -> str:
    sources = list(record["sources"])
    merge = record["merge"]
    return (
        "<g data-abilene-boundary hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(merge))}</desc>"
        '<rect class="campus-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="76" y="86">ABILENE EVIDENCE · THREE SEPARATE 2D LANES</text>'
        + _wrapped(
            str(record["title"]),
            x=76,
            y=126,
            width_chars=76,
            line_height=27,
            css_class="scene-title",
            maximum_lines=2,
        )
        + _source_lane_svg(sources[0], y=170)
        + _source_lane_svg(sources[1], y=378)
        + _source_lane_svg(sources[2], y=586)
        + '<rect class="unknown-boundary" x="975" y="150" width="190" height="620" rx="16"/>'
        + '<text class="unknown-boundary-label centered" x="1070" y="330">UNRESOLVED</text>'
        + '<text class="unknown-boundary-label centered" x="1070" y="365">CAMPUS</text>'
        + '<text class="unknown-boundary-label centered" x="1070" y="400">MERGE</text>'
        + '<text class="unknown-question centered" x="1070" y="495">?</text>'
        + '<text class="unknown-boundary-stop centered" x="1070" y="555">NO SHARED BUS DRAWN</text>'
        + "<g data-abilene-merge hidden>"
        + '<rect class="merge-evidence-card" x="1192" y="150" width="328" height="620" rx="16"/>'
        + f'<text class="merge-title" x="1220" y="194">{_escape(merge["title"])}</text>'
        + '<text class="merge-section-label" x="1220" y="238">KNOWN REVIEW LABEL</text>'
        + _wrapped(
            str(merge["known"]),
            x=1220,
            y=273,
            width_chars=34,
            line_height=19,
            css_class="merge-known",
            maximum_lines=6,
        )
        + '<text class="merge-section-label unknown-label" x="1220" y="405">NOT ESTABLISHED</text>'
        + _wrapped(
            str(merge["unknown"]),
            x=1220,
            y=440,
            width_chars=34,
            line_height=19,
            css_class="merge-unknown",
            maximum_lines=9,
        )
        + "</g></g>"
    )


def _role_pictogram(role_id: str, *, x: int, y: int) -> str:
    if role_id == "ups":
        return (
            f'<g class="role-diagram ups-diagram">'
            f'<rect class="diagram-node" x="{x}" y="{y}" width="92" height="64" rx="9"/>'
            f'<text class="diagram-label centered" x="{x + 46}" y="{y + 38}">SOURCE</text>'
            f'<path class="diagram-link" d="M {x + 92} {y + 32} H {x + 136}"/>'
            f'<rect class="ups-icon" x="{x + 136}" y="{y - 10}" width="112" height="84" rx="10"/>'
            f'<path class="battery-bars" d="M {x + 158} {y + 49} V {y + 18} M {x + 180} {y + 49} V {y + 10} M {x + 202} {y + 49} V {y + 27} M {x + 224} {y + 49} V {y + 3}"/>'
            f'<text class="diagram-label centered" x="{x + 192}" y="{y + 68}">UPS</text>'
            f'<path class="diagram-link" d="M {x + 248} {y + 32} H {x + 292}"/>'
            f'<rect class="critical-load" x="{x + 292}" y="{y}" width="92" height="64" rx="9"/>'
            f'<text class="diagram-label centered" x="{x + 338}" y="{y + 28}">CRITICAL</text>'
            f'<text class="diagram-label centered" x="{x + 338}" y="{y + 46}">LOAD</text></g>'
        )
    if role_id == "bess":
        return (
            f'<g class="role-diagram bess-diagram">'
            f'<path class="site-bus" d="M {x} {y + 22} H {x + 384}"/>'
            f'<rect class="diagram-node" x="{x}" y="{y - 10}" width="92" height="64" rx="9"/>'
            f'<text class="diagram-label centered" x="{x + 46}" y="{y + 28}">SOURCE</text>'
            f'<rect class="diagram-node" x="{x + 292}" y="{y - 10}" width="92" height="64" rx="9"/>'
            f'<text class="diagram-label centered" x="{x + 338}" y="{y + 28}">SITE LOAD</text>'
            f'<path class="parallel-branch" d="M {x + 192} {y + 22} V {y + 90}"/>'
            f'<rect class="bess-icon" x="{x + 132}" y="{y + 90}" width="120" height="72" rx="10"/>'
            f'<path class="battery-outline" d="M {x + 156} {y + 113} H {x + 225} V {y + 143} H {x + 156} Z M {x + 225} {y + 122} H {x + 234} V {y + 134} H {x + 225}"/>'
            f'<text class="diagram-label centered" x="{x + 192}" y="{y + 181}">PARALLEL BESS</text></g>'
        )
    return (
        f'<g class="role-diagram diesel-diagram">'
        f'<rect class="diagram-node" x="{x + 292}" y="{y}" width="92" height="64" rx="9"/>'
        f'<text class="diagram-label centered" x="{x + 338}" y="{y + 38}">LOAD</text>'
        f'<rect class="transfer-gate" x="{x + 160}" y="{y}" width="96" height="64" rx="9"/>'
        f'<text class="diagram-label centered" x="{x + 208}" y="{y + 28}">TRANSFER</text>'
        f'<text class="diagram-label centered" x="{x + 208}" y="{y + 46}">GATE</text>'
        f'<path class="diagram-link" d="M {x + 256} {y + 32} H {x + 292}"/>'
        f'<circle class="diesel-icon" cx="{x + 70}" cy="{y + 124}" r="54"/>'
        f'<text class="diesel-letter centered" x="{x + 70}" y="{y + 136}">G</text>'
        f'<path class="standby-branch" d="M {x + 124} {y + 124} H {x + 208} V {y + 64}"/>'
        f'<text class="diagram-label" x="{x + 142}" y="{y + 151}">STANDBY BRANCH</text></g>'
    )


def _role_svg(record: Mapping[str, Any], *, x: int) -> str:
    return (
        f'<g data-resilience-role-id="{_escape(record["id"])}" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['role_note'])} {_escape(record['abilene_boundary'])} {_escape(_fact_description(record))}</desc>"
        f'<rect class="role-card" x="{x}" y="180" width="470" height="568" rx="16"/>'
        f'<text class="role-title" x="{x + 28}" y="222">{_escape(record["title"])}</text>'
        + _wrapped(
            str(record["function"]),
            x=x + 28,
            y=258,
            width_chars=46,
            line_height=20,
            css_class="role-function",
            maximum_lines=3,
        )
        + _role_pictogram(str(record["id"]), x=x + 42, y=332)
        + '<text class="role-section-label" '
        f'x="{x + 28}" y="548">ARCHITECTURAL POSITION</text>'
        + _wrapped(
            str(record["architectural_position"]),
            x=x + 28,
            y=578,
            width_chars=48,
            line_height=19,
            css_class="role-position",
            maximum_lines=3,
        )
        + '<rect class="role-boundary" '
        f'x="{x + 24}" y="620" width="422" height="112" rx="10"/>'
        + _wrapped(
            str(record["abilene_boundary"]),
            x=x + 44,
            y=647,
            width_chars=48,
            line_height=16,
            css_class="role-boundary-copy",
            maximum_lines=5,
        )
        + "</g>"
    )


def _roles_svg(record: Mapping[str, Any]) -> str:
    roles = list(record["roles"])
    boundary = record["comparison_boundary"]
    return (
        "<g data-resilience-roles hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(boundary))}</desc>"
        '<rect class="campus-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="76" y="84">THREE INDEPENDENT REFERENCE DIAGRAMS · NOT A SEQUENCE</text>'
        + _wrapped(
            str(record["title"]),
            x=76,
            y=124,
            width_chars=78,
            line_height=27,
            css_class="scene-title",
            maximum_lines=2,
        )
        + _role_svg(roles[0], x=50)
        + _role_svg(roles[1], x=565)
        + _role_svg(roles[2], x=1080)
        + '<rect class="scope-box" x="180" y="768" width="1240" height="82" rx="10"/>'
        + f'<text class="scope-title" x="210" y="796">{_escape(boundary["title"])}</text>'
        + _wrapped(
            str(boundary["body"]),
            x=210,
            y=821,
            width_chars=133,
            line_height=17,
            css_class="scope-copy",
            maximum_lines=2,
        )
        + "</g>"
    )


def _stage_svg(record: Mapping[str, Any], *, x: int, index: int) -> str:
    posture_labels = {
        "constructed": "SCOPE EVIDENCE",
        "energized": "MINIMUM + BY-DATE",
        "commissioned": "UNRESOLVED",
        "live": "LIVE-BY EVIDENCE",
    }
    unresolved = record["id"] == "commissioned"
    css_class = " lifecycle-unresolved" if unresolved else ""
    badge = "?" if unresolved else str(index + 1)
    boundary_copy = str(record["boundary"]).split(". ", 1)[0].rstrip(".") + "."
    return (
        f'<g data-building-stage-id="{_escape(record["id"])}" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['known'])} {_escape(record['boundary'])} {_escape(_fact_description(record))}</desc>"
        f'<rect class="lifecycle-card{css_class}" x="{x}" y="170" width="340" height="452" rx="16"/>'
        f'<circle class="stage-number{css_class}" cx="{x + 42}" cy="214" r="24"/>'
        f'<text class="stage-number-label centered" x="{x + 42}" y="222">{badge}</text>'
        f'<text class="stage-title" x="{x + 78}" y="221">{_escape(record["title"])}</text>'
        f'<text class="stage-posture" x="{x + 28}" y="270">{posture_labels[record["id"]]}</text>'
        + '<text class="stage-section-label" '
        f'x="{x + 28}" y="310">PUBLIC EVIDENCE</text>'
        + _wrapped(
            str(record["known"]),
            x=x + 28,
            y=338,
            width_chars=34,
            line_height=18,
            css_class="stage-known",
            maximum_lines=8,
        )
        + '<text class="stage-section-label boundary-label" '
        f'x="{x + 28}" y="500">BOUNDARY</text>'
        + _wrapped(
            boundary_copy,
            x=x + 28,
            y=528,
            width_chars=34,
            line_height=18,
            css_class="stage-boundary",
            maximum_lines=5,
        )
        + "</g>"
    )


def _lifecycle_svg(record: Mapping[str, Any]) -> str:
    stages = list(record["stages"])
    scope = record["campus_scope_boundary"]
    building_icons = []
    for index in range(8):
        x = 320 + index * 116
        css_class = " confirmed-minimum" if index < 2 else " planned-only"
        label = str(index + 1) if index < 2 else "?"
        building_icons.append(
            f'<g class="lifecycle-building{css_class}">'
            f'<path d="M {x} 718 V 665 H {x + 70} V 718 Z M {x + 12} 680 H {x + 24} M {x + 35} 680 H {x + 47} M {x + 12} 697 H {x + 24} M {x + 35} 697 H {x + 47}"/>'
            f'<text class="lifecycle-building-label centered" x="{x + 35}" y="742">{label}</text></g>'
        )
    return (
        "<g data-building-lifecycle hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(scope))}</desc>"
        '<rect class="campus-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="76" y="84">DISCLOSURE LADDER · NOT ONE COMPLETION BADGE</text>'
        + _wrapped(
            str(record["title"]),
            x=76,
            y=124,
            width_chars=78,
            line_height=27,
            css_class="scene-title",
            maximum_lines=2,
        )
        + _stage_svg(stages[0], x=70, index=0)
        + _stage_svg(stages[1], x=455, index=1)
        + _stage_svg(stages[2], x=840, index=2)
        + _stage_svg(stages[3], x=1225, index=3)
        + '<path class="lifecycle-arrow" d="M 410 396 H 445 M 795 396 H 830 M 1180 396 H 1215"/>'
        + '<text class="building-strip-label" x="80" y="650">PLANNED CAMPUS · CURRENT OPERATIONAL COUNT NOT DISCLOSED</text>'
        + "".join(building_icons)
        + '<text class="confirmed-label" x="320" y="770">AT LEAST TWO ENERGIZED · REMAINING BUILDING STATE UNRESOLVED</text>'
        + '<rect class="scope-box" x="80" y="792" width="1440" height="48" rx="10"/>'
        + f'<text class="scope-title" x="110" y="823">{_escape(scope["title"])}</text>'
        + "</g>"
    )


def _equipment_icon(equipment_id: str, *, x: int, y: int) -> str:
    if equipment_id == "unit_substation":
        return (
            f'<g><circle class="equipment-coil" cx="{x + 60}" cy="{y}" r="28"/>'
            f'<circle class="equipment-coil" cx="{x + 104}" cy="{y}" r="28"/>'
            f'<path class="equipment-switch" d="M {x} {y} H {x + 25} M {x + 25} {y} L {x + 50} {y - 20}"/></g>'
        )
    if equipment_id == "switchgear":
        return (
            f'<g><rect class="gear-cabinet" x="{x + 8}" y="{y - 42}" width="150" height="84" rx="5"/>'
            f'<path class="gear-divider" d="M {x + 58} {y - 42} V {y + 42} M {x + 108} {y - 42} V {y + 42}"/>'
            f'<circle class="gear-indicator" cx="{x + 32}" cy="{y - 15}" r="5"/><circle class="gear-indicator" cx="{x + 82}" cy="{y - 15}" r="5"/><circle class="gear-indicator" cx="{x + 132}" cy="{y - 15}" r="5"/></g>'
        )
    if equipment_id == "ups":
        return (
            f'<g><rect class="ups-icon" x="{x + 22}" y="{y - 45}" width="120" height="90" rx="8"/>'
            f'<path class="battery-bars" d="M {x + 48} {y + 18} V {y - 15} M {x + 72} {y + 18} V {y - 25} M {x + 96} {y + 18} V {y - 5} M {x + 120} {y + 18} V {y - 34}"/></g>'
        )
    return (
        f'<g><path class="busway-rail" d="M {x + 5} {y - 20} H {x + 155} V {y + 20} H {x + 5} Z"/>'
        f'<path class="busway-plugs" d="M {x + 38} {y + 20} V {y + 45} M {x + 82} {y + 20} V {y + 45} M {x + 126} {y + 20} V {y + 45}"/></g>'
    )


def _handoff_svg(record: Mapping[str, Any]) -> str:
    equipment = list(record["equipment_verbs"])
    cards = []
    for index, item in enumerate(equipment):
        x = 520 + index * 250
        if index:
            cards.append(
                f'<path class="equipment-arrow" d="M {x - 36} 430 H {x - 8}"/>'
            )
        cards.append(
            f'<g class="equipment-card" data-handoff-equipment-id="{_escape(item["id"])}">'
            f'<rect x="{x}" y="280" width="220" height="330" rx="15"/>'
            f'<text class="equipment-number" x="{x + 22}" y="316">0{index + 1}</text>'
            f'<text class="equipment-title centered" x="{x + 110}" y="355">{_escape(item["equipment"])}</text>'
            + _equipment_icon(str(item["id"]), x=x + 28, y=430)
            + _wrapped(
                str(item["verb"]),
                x=x + 110,
                y=530,
                width_chars=23,
                line_height=18,
                css_class="equipment-verb centered",
                maximum_lines=5,
                center_lines=True,
            )
            + f"<desc>{_escape(_fact_description(item))}</desc></g>"
        )
    return (
        "<g data-phase4-handoff hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record['site_boundary']))}</desc>"
        '<rect class="handoff-cover" x="0" y="0" width="1600" height="900"/>'
        '<rect class="campus-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="76" y="84">NEXT · PHASE 4 · GENERIC FUNCTIONAL CHAIN</text>'
        + _wrapped(
            str(record["title"]),
            x=76,
            y=126,
            width_chars=78,
            line_height=28,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<g class="handoff-building">'
        + '<polygon class="handoff-building-front" points="82,300 390,300 390,650 82,650"/>'
        + '<polygon class="handoff-building-side" points="390,300 470,260 470,610 390,650"/>'
        + '<polygon class="handoff-building-top" points="82,300 162,260 470,260 390,300"/>'
        + '<path class="handoff-building-cut" d="M 130 350 H 350 V 610 H 130 Z M 170 390 H 310 M 170 450 H 310 M 170 510 H 310"/>'
        + '<text class="handoff-building-label centered" x="270" y="694">ONE GENERIC BUILDING</text>'
        + "</g>"
        + '<path class="campus-feeder-arrow" d="M 52 475 H 130"/>'
        + '<text class="campus-feeder-label" x="70" y="452">CAMPUS FEEDER</text>'
        + '<g class="handoff-protection-note">'
        + '<rect x="82" y="720" width="400" height="64" rx="10"/>'
        + '<text class="handoff-protection-title centered" x="282" y="746">PROTECTION BOUNDARY PRESERVED</text>'
        + '<text class="handoff-protection-copy centered" x="282" y="768">Actual Abilene scheme remains unknown</text></g>'
        + "".join(cards)
        + '<path class="rack-arrow" d="M 1490 430 H 1530"/>'
        + '<text class="rack-label centered" x="1510" y="408">RACK POSITIONS</text>'
        + '<rect class="scope-box" x="520" y="680" width="1010" height="126" rx="10"/>'
        + '<text class="scope-title" x="548" y="714">GENERIC FUNCTIONS · NOT AN ABILENE ONE-LINE</text>'
        + _wrapped(
            str(record["site_boundary"]["body"]),
            x=548,
            y=748,
            width_chars=105,
            line_height=20,
            css_class="scope-copy",
            maximum_lines=3,
        )
        + "</g>"
    )


def _responsive_fanout(record: Mapping[str, Any]) -> str:
    topology = record["topology"]
    buildings = "".join(
        '<div class="responsive-building"><span class="building-roof" '
        'aria-hidden="true"></span>'
        f"<strong>{_escape(feeder)}</strong></div>"
        for feeder in topology["building_feeders"]
    )
    return (
        '<article class="responsive-scene responsive-fanout" data-generic-fanout hidden>'
        '<p class="responsive-kicker">Generic orientation · not Abilene</p>'
        f"<h3>{_escape(record['title'])}</h3>"
        '<div class="responsive-campus-map" role="img" '
        'aria-label="One upstream source reaches a conceptual distribution node with three separate building feeders">'
        '<div class="responsive-source">'
        f'{_escape(topology["source"])}</div><span class="map-arrow">→</span>'
        '<div class="responsive-distribution-node">'
        f"{_escape(topology['distribution_node'])}<small>transform · protect · control · deliver</small></div>"
        '<span class="fanout-marker">↗ → ↘</span>'
        f'<div class="responsive-building-grid">{buildings}</div></div>'
        f'<p class="responsive-relation">{_escape(topology["relation"])}</p>'
        '<div class="responsive-scope"><strong>Abstract topology only</strong>'
        f"<p>{_escape(record['boundary'])}</p></div>"
        f'<span class="visually-hidden">{_escape(record["protection_note"])} {_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_fault_stage(record: Mapping[str, Any], index: int) -> str:
    symbols = {
        "feeder_disturbance": "FAULT",
        "protection_detects": "DETECT",
        "protective_device_interrupts": "OPEN",
        "faulted_branch_isolated": "ISOLATE",
    }
    arrow = (
        '<span class="responsive-stage-arrow" aria-hidden="true">→</span>'
        if index < len(FAULT_STAGE_IDS) - 1
        else ""
    )
    return (
        '<article class="responsive-fault-stage" '
        f'data-feeder-fault-stage-id="{_escape(record["id"])}">'
        f'<span class="responsive-fault-number">0{index + 1}</span>'
        f'<span class="responsive-fault-symbol {_escape(record["visual_posture"])}" aria-hidden="true">{symbols[record["id"]]}</span>'
        f"<h3>{_escape(record['title'])}</h3>"
        f"<p>{_escape(record['action'])}</p>"
        '<div class="responsive-fault-boundary"><strong>Boundary</strong>'
        f"<p>{_escape(record['boundary'])}</p></div>"
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        + arrow
        + "</article>"
    )


def _responsive_feeder_fault_isolation(record: Mapping[str, Any]) -> str:
    remaining = record["remaining_service"]
    boundary = record["boundary"]
    conditions = "".join(
        '<div class="responsive-remaining-condition" '
        f'data-remaining-service-condition-id="{_escape(condition["id"])}">'
        f"<span>{index + 1}</span><p>{_escape(condition['text'])}</p></div>"
        for index, condition in enumerate(remaining["conditions"])
    )
    return (
        '<section class="responsive-scene responsive-fault-isolation" '
        "data-feeder-fault-isolation hidden>"
        '<p class="responsive-kicker">Generic feeder protection · causal sequence</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<p class="responsive-fault-sequence">DISTURBANCE → DETECT → INTERRUPT → ISOLATE</p>'
        '<div class="responsive-fault-flow">'
        + "".join(
            _responsive_fault_stage(stage, index)
            for index, stage in enumerate(record["stages"])
        )
        + '</div><section class="responsive-remaining-service">'
        f"<h3>{_escape(remaining['title'])}</h3>"
        f"<p>{_escape(remaining['body'])}</p>"
        f'<div class="responsive-condition-grid">{conditions}</div>'
        '<strong class="responsive-conditional-result">OTHER BUILDINGS: CONDITIONAL · NOT GUARANTEED</strong>'
        f'<span class="visually-hidden">{_escape(_fact_description(remaining))}</span>'
        '</section><div class="responsive-scope responsive-isolation-scope">'
        f"<strong>{_escape(boundary['title'])}</strong><p>{_escape(boundary['body'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(boundary))}</span>'
        "</div></section>"
    )


def _responsive_source_lane(record: Mapping[str, Any]) -> str:
    return (
        '<article class="responsive-source-lane" '
        f'data-abilene-source-id="{_escape(record["id"])}" hidden>'
        f"<h3>{_escape(record['title'])}</h3>"
        f'<p class="responsive-posture">{_escape(record["evidence_posture"])}</p>'
        '<div class="responsive-stop-line" aria-hidden="true"><span></span><b>STOP</b></div>'
        f'<p class="responsive-boundary-copy">{_escape(record["boundary"])}</p>'
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_source_boundary(record: Mapping[str, Any]) -> str:
    merge = record["merge"]
    return (
        '<section class="responsive-scene responsive-source-boundary" '
        "data-abilene-boundary hidden>"
        '<p class="responsive-kicker">Three separate 2D lanes</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-source-grid">'
        + "".join(_responsive_source_lane(source) for source in record["sources"])
        + '</div><div class="responsive-merge" data-abilene-merge hidden>'
        '<div class="responsive-merge-stop"><b>?</b><strong>Unresolved campus merge</strong><span>No shared bus drawn</span></div>'
        '<div class="responsive-merge-evidence">'
        "<strong>Known review label</strong>"
        f"<p>{_escape(merge['known'])}</p><strong>Not established</strong>"
        f"<p>{_escape(merge['unknown'])}</p></div>"
        f'<span class="visually-hidden">{_escape(_fact_description(merge))}</span>'
        "</div></section>"
    )


def _responsive_role_diagram(role_id: str) -> str:
    if role_id == "ups":
        return (
            '<div class="responsive-role-diagram series-role" role="img" '
            'aria-label="UPS shown in series between source and critical load">'
            '<span>Source</span><b>→</b><span class="role-emphasis">UPS</span><b>→</b><span>Critical load</span></div>'
        )
    if role_id == "bess":
        return (
            '<div class="responsive-role-diagram parallel-role" role="img" '
            'aria-label="BESS shown as a parallel site-level resource">'
            "<div><span>Source</span><i></i><span>Site load</span></div>"
            '<b>↕</b><span class="role-emphasis">Parallel BESS</span></div>'
        )
    return (
        '<div class="responsive-role-diagram standby-role" role="img" '
        'aria-label="Diesel generator shown on a separate standby branch">'
        "<div><span>Transfer gate</span><b>→</b><span>Load</span></div>"
        '<div><span class="role-emphasis">Diesel G</span><b>┄ standby branch ┄↗</b></div></div>'
    )


def _responsive_role(record: Mapping[str, Any]) -> str:
    return (
        '<article class="responsive-role" '
        f'data-resilience-role-id="{_escape(record["id"])}" hidden>'
        f"<h3>{_escape(record['title'])}</h3>"
        f'<p class="responsive-function">{_escape(record["function"])}</p>'
        + _responsive_role_diagram(str(record["id"]))
        + '<strong class="responsive-section-label">Architectural position</strong>'
        f"<p>{_escape(record['architectural_position'])}</p>"
        '<div class="responsive-scope"><strong>Abilene boundary</strong>'
        f"<p>{_escape(record['abilene_boundary'])}</p></div>"
        f'<span class="visually-hidden">{_escape(record["role_note"])} {_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_roles(record: Mapping[str, Any]) -> str:
    boundary = record["comparison_boundary"]
    return (
        '<section class="responsive-scene responsive-roles" data-resilience-roles hidden>'
        '<p class="responsive-kicker">Independent references · not a sequence</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-role-grid">'
        + "".join(_responsive_role(role) for role in record["roles"])
        + '</div><div class="responsive-scope comparison-scope">'
        f"<strong>{_escape(boundary['title'])}</strong><p>{_escape(boundary['body'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(boundary))}</span>'
        "</div></section>"
    )


def _responsive_stage(record: Mapping[str, Any], index: int) -> str:
    labels = {
        "constructed": "Scope evidence",
        "energized": "Minimum + by-date",
        "commissioned": "Unresolved",
        "live": "Live-by evidence",
    }
    badge = "?" if record["id"] == "commissioned" else str(index + 1)
    css_class = " unresolved-stage" if record["id"] == "commissioned" else ""
    return (
        f'<article class="responsive-stage-card{css_class}" '
        f'data-building-stage-id="{_escape(record["id"])}" hidden>'
        f'<span class="responsive-stage-number">{badge}</span>'
        f"<h3>{_escape(record['title'])}</h3>"
        f'<strong class="responsive-stage-posture">{labels[record["id"]]}</strong>'
        '<span class="responsive-section-label">Public evidence</span>'
        f"<p>{_escape(record['known'])}</p>"
        '<span class="responsive-section-label">Boundary</span>'
        f"<p>{_escape(record['boundary'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_lifecycle(record: Mapping[str, Any]) -> str:
    scope = record["campus_scope_boundary"]
    buildings = "".join(
        '<span class="confirmed-building">✓</span>' if index < 2 else "<span>?</span>"
        for index in range(8)
    )
    return (
        '<section class="responsive-scene responsive-lifecycle" '
        "data-building-lifecycle hidden>"
        '<p class="responsive-kicker">Disclosure ladder · not one completion badge</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-stage-grid">'
        + "".join(
            _responsive_stage(stage, index)
            for index, stage in enumerate(record["stages"])
        )
        + '</div><div class="responsive-building-strip" role="img" '
        'aria-label="Eight planned buildings; at least two energized; exact current operational count not disclosed">'
        f"{buildings}<strong>At least two energized · remaining current state unresolved</strong></div>"
        '<div class="responsive-scope">'
        f"<strong>{_escape(scope['title'])}</strong><p>{_escape(scope['body'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(scope))}</span>'
        "</div></section>"
    )


def _responsive_handoff(record: Mapping[str, Any]) -> str:
    equipment = "".join(
        '<article class="responsive-equipment-card" '
        f'data-handoff-equipment-id="{_escape(item["id"])}">'
        f"<span>0{index + 1}</span><h3>{_escape(item['equipment'])}</h3>"
        f"<p>{_escape(item['verb'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(item))}</span></article>'
        for index, item in enumerate(record["equipment_verbs"])
    )
    return (
        '<section class="responsive-scene responsive-handoff" data-phase4-handoff hidden>'
        '<p class="responsive-kicker">Next · Phase 4 · generic functional chain</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-building-entry">'
        '<div class="responsive-cutaway-building" aria-hidden="true"><span></span><span></span><span></span></div>'
        "<div><strong>One generic building</strong>"
        "<p>Campus feeder enters a functional chain; product, rating, route, and switching remain unresolved.</p>"
        '<div class="responsive-protection-handoff">Protection boundary preserved · actual Abilene scheme unknown</div></div></div>'
        '<div class="responsive-equipment-chain">'
        + equipment
        + '<strong class="rack-destination">Rack positions →</strong></div>'
        '<div class="responsive-scope"><strong>Generic functions · not an Abilene one-line</strong>'
        f"<p>{_escape(record['site_boundary']['body'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(record["site_boundary"]))}</span>'
        "</div></section>"
    )


def _responsive_visual(payload: Mapping[str, Any]) -> str:
    return (
        '<section class="responsive-visual" aria-label="Responsive campus distribution teaching surface">'
        + _responsive_fanout(payload["generic_fanout"])
        + _responsive_feeder_fault_isolation(payload["feeder_fault_isolation"])
        + _responsive_source_boundary(payload["abilene_source_boundary"])
        + _responsive_roles(payload["resilience_roles"])
        + _responsive_handoff(payload["phase4_handoff"])
        + "</section>"
    )


def render_campus_distribution(payload: dict[str, Any]) -> str:
    """Render one compiled Phase 3 pilot as a self-contained HTML page."""
    if payload.get("canvas", {}).get("kind") != CANVAS_KIND:
        raise CampusVisualError("render payload is not a campus distribution surface")
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
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="gigawatt-source-digest" content="{_escape(payload["source_digest"])}">
<title>GIGAWATT — {_escape(payload["pilot"]["title"])}</title>
<style>
  :root {{ --paper:#fafaf7; --ink:#1a1a1a; --muted:#5f5f59; --faint:#d4d4cd; --blue:#175d8d; --blue-soft:#eaf3f8; --green:#2f9e8f; --green-soft:#e9f7f4; --amber:#b76e18; --amber-soft:#fff7ed; --red:#b3261e; --red-soft:#fceceb; }}
  * {{ box-sizing:border-box; }}
  [hidden] {{ display:none !important; }}
  html,body {{ width:100%; height:100%; min-height:0; margin:0; background:var(--paper); color:var(--ink); font-family:Inter,"Helvetica Neue",Arial,sans-serif; }}
  html {{ overflow:hidden; }}
  body {{ display:grid; grid-template-rows:auto minmax(0,1fr) auto; height:100dvh; min-height:0; overflow:hidden; }}
  header {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(320px,570px); gap:20px; padding:11px 20px 10px; border-bottom:1.5px solid var(--ink); }}
  .eyebrow,.phase-question,.state-number,.scene-kicker,.responsive-kicker,.fact-ref,.scope-title,.role-section-label,.stage-section-label,.merge-section-label,.equipment-number {{ text-transform:uppercase; letter-spacing:.075em; font-size:11px; font-weight:760; }}
  h1 {{ margin:3px 0; font-size:clamp(21px,2.2vw,34px); line-height:1.05; }}
  header p {{ margin:2px 0; line-height:1.3; }}
  .objective {{ align-self:end; color:var(--muted); font-size:13px; }}
  main {{ min-width:0; min-height:0; display:grid; place-items:center; overflow:hidden; padding:8px 14px; }}
  .visual-shell {{ width:100%; height:100%; min-width:0; min-height:0; max-width:1600px; max-height:900px; border:1.5px solid var(--ink); background:white; }}
  svg {{ display:block; width:100%; height:100%; }}
  .centered {{ text-anchor:middle; }}
  .campus-panel {{ fill:white; stroke:var(--ink); stroke-width:2; }}
  .scene-kicker {{ fill:var(--blue); font-size:13px; }}
  .scene-title {{ font-size:27px; font-weight:770; }}
  .campus-ground {{ fill:#f3f3ef; stroke:var(--faint); stroke-width:2; }}
  .campus-grid {{ fill:none; stroke:#deded7; stroke-width:1.5; }}
  .source-boundary-card,.source-lane-card,.role-card,.lifecycle-card {{ fill:white; stroke:var(--ink); stroke-width:2; }}
  .source-boundary-title,.distribution-label {{ font-size:17px; font-weight:730; }}
  .fanout-feeder {{ fill:none; stroke:var(--blue); stroke-width:4; }}
  .incoming-feeder {{ stroke-width:7; }}
  .fanout-bus {{ fill:none; stroke:var(--blue); stroke-width:10; }}
  .iso-gate-top,.iso-building-top {{ fill:#d7eaf3; stroke:var(--blue); stroke-width:2; }}
  .iso-gate-front,.iso-building-front {{ fill:#eaf3f8; stroke:var(--blue); stroke-width:2; }}
  .iso-gate-side,.iso-building-side {{ fill:#bfdbe9; stroke:var(--blue); stroke-width:2; }}
  .iso-window {{ fill:none; stroke:var(--blue); stroke-width:3; opacity:.55; }}
  .iso-building-label {{ font-size:14px; font-weight:730; }}
  .orientation-compass circle {{ fill:white; stroke:var(--ink); stroke-width:1.5; }}
  .orientation-compass path {{ fill:none; stroke:var(--ink); stroke-width:2; }}
  .compass-label {{ font-size:15px; font-weight:780; }}
  .relation-label {{ fill:var(--blue); font-size:17px; font-weight:740; }}
  .fault-sequence-label {{ fill:var(--blue); font-size:15px; font-weight:790; letter-spacing:.07em; }}
  .fault-stage-card {{ fill:white; stroke:var(--ink); stroke-width:2; }}
  .fault-stage-number {{ fill:var(--blue); }}
  .fault-stage-number-label,.remaining-condition-number-label {{ fill:white; font-size:13px; font-weight:800; }}
  .fault-stage-title {{ font-size:17px; font-weight:770; }}
  .fault-stage-action {{ fill:var(--muted); font-size:13px; }}
  .fault-stage-boundary {{ fill:var(--amber); font-size:11px; font-weight:680; }}
  .fault-stage-arrow,.remaining-condition-arrow {{ fill:none; stroke:var(--blue); stroke-width:4; }}
  .fault-source-line,.fault-normal-branch,.detection-wave,.open-breaker {{ fill:none; stroke:var(--blue); stroke-width:4; }}
  .fault-node,.breaker-contact {{ fill:white; stroke:var(--blue); stroke-width:4; }}
  .faulted-branch,.interrupt-stop,.isolation-bars {{ fill:none; stroke:var(--red); stroke-width:5; }}
  .fault-bolt {{ fill:var(--red); }}
  .detection-ring {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:4; }}
  .detection-core {{ fill:white; stroke:var(--blue); stroke-width:3; }}
  .fault-icon-label {{ fill:var(--blue); font-size:11px; font-weight:800; letter-spacing:.04em; }}
  .isolate-icon .fault-icon-label {{ fill:var(--red); }}
  .conditional-branch {{ stroke-dasharray:8 5; }}
  .conditional-question {{ fill:var(--amber); font-size:28px; font-weight:800; }}
  .isolated-tail {{ stroke-dasharray:5 5; opacity:.7; }}
  .remaining-service-panel {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:2; }}
  .remaining-service-title {{ fill:var(--blue); font-size:18px; font-weight:780; }}
  .remaining-condition-card {{ fill:white; stroke:var(--blue); stroke-width:1.5; }}
  .remaining-condition-number {{ fill:var(--blue); }}
  .remaining-condition-copy {{ font-size:12px; font-weight:690; }}
  .conditional-outcome-card {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:2; }}
  .conditional-outcome-kicker {{ fill:var(--amber); font-size:11px; font-weight:780; letter-spacing:.06em; }}
  .conditional-outcome-title {{ font-size:17px; font-weight:800; }}
  .conditional-outcome-copy {{ fill:var(--muted); font-size:12px; }}
  .fault-boundary-card {{ fill:var(--ink); stroke:var(--ink); stroke-width:2; }}
  .fault-boundary-title {{ fill:white; font-size:15px; font-weight:760; }}
  .fault-boundary-copy {{ fill:#d9d9d4; font-size:13px; }}
  .scope-box,.role-boundary {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.6; }}
  .scope-title {{ fill:var(--amber); }}
  .scope-copy,.source-lane-boundary,.role-boundary-copy,.stage-boundary {{ fill:var(--muted); font-size:13px; }}
  .source-lane-title {{ font-size:20px; font-weight:760; }}
  .source-lane-posture {{ fill:var(--blue); font-size:14px; font-weight:700; }}
  .source-stop-line {{ fill:none; stroke:var(--blue); stroke-width:5; }}
  .source-stop-bar {{ fill:none; stroke:var(--red); stroke-width:7; }}
  .source-stop-label {{ fill:var(--red); font-size:11px; font-weight:780; letter-spacing:.04em; }}
  .unknown-boundary {{ fill:var(--ink); stroke:var(--ink); }}
  .unknown-boundary-label {{ fill:white; font-size:23px; font-weight:780; letter-spacing:.04em; }}
  .unknown-question {{ fill:var(--amber); font-size:80px; font-weight:800; }}
  .unknown-boundary-stop {{ fill:#d9d9d4; font-size:11px; font-weight:740; }}
  .merge-evidence-card {{ fill:var(--paper); stroke:var(--faint); stroke-width:2; }}
  .merge-title {{ font-size:18px; font-weight:760; }}
  .merge-section-label {{ fill:var(--blue); }}
  .unknown-label {{ fill:var(--amber); }}
  .merge-known,.merge-unknown {{ font-size:14px; fill:var(--muted); }}
  .role-title {{ font-size:25px; font-weight:770; }}
  .role-function {{ fill:var(--muted); font-size:15px; }}
  .role-section-label {{ fill:var(--blue); }}
  .role-position {{ font-size:15px; font-weight:700; }}
  .diagram-node,.critical-load,.transfer-gate {{ fill:white; stroke:var(--blue); stroke-width:2; }}
  .diagram-link,.site-bus,.parallel-branch {{ fill:none; stroke:var(--blue); stroke-width:3; }}
  .diagram-label {{ font-size:11px; font-weight:760; }}
  .ups-icon,.bess-icon {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:2; }}
  .battery-bars,.battery-outline {{ fill:none; stroke:var(--blue); stroke-width:3; }}
  .diesel-icon {{ fill:var(--green-soft); stroke:var(--green); stroke-width:3; }}
  .diesel-letter {{ fill:var(--green); font-size:34px; font-weight:800; }}
  .standby-branch {{ fill:none; stroke:var(--green); stroke-width:3; stroke-dasharray:8 6; }}
  .lifecycle-card.lifecycle-unresolved {{ fill:var(--amber-soft); stroke:var(--amber); }}
  .stage-number {{ fill:var(--blue); }}
  .stage-number.lifecycle-unresolved {{ fill:var(--amber); }}
  .stage-number-label {{ fill:white; font-size:18px; font-weight:800; }}
  .stage-title {{ font-size:21px; font-weight:760; }}
  .stage-posture {{ fill:var(--blue); font-size:11px; font-weight:760; letter-spacing:.05em; }}
  .lifecycle-unresolved + .stage-number-label,.lifecycle-unresolved .stage-posture {{ fill:var(--amber); }}
  .stage-section-label {{ fill:var(--blue); }}
  .boundary-label {{ fill:var(--amber); }}
  .stage-known {{ font-size:13px; }}
  .lifecycle-arrow {{ fill:none; stroke:var(--blue); stroke-width:3; }}
  .building-strip-label,.confirmed-label {{ fill:var(--muted); font-size:12px; font-weight:730; letter-spacing:.04em; }}
  .lifecycle-building path {{ fill:none; stroke:var(--faint); stroke-width:2; }}
  .lifecycle-building.confirmed-minimum path {{ fill:var(--blue-soft); stroke:var(--blue); }}
  .lifecycle-building-label {{ font-size:12px; font-weight:760; fill:var(--muted); }}
  .handoff-building-front {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:2; }}
  .handoff-cover {{ fill:white; }}
  .handoff-building-side {{ fill:#bfdbe9; stroke:var(--blue); stroke-width:2; }}
  .handoff-building-top {{ fill:#d7eaf3; stroke:var(--blue); stroke-width:2; }}
  .handoff-building-cut {{ fill:white; stroke:var(--blue); stroke-width:2; }}
  .handoff-building-label {{ font-size:15px; font-weight:760; }}
  .handoff-protection-note rect {{ fill:var(--ink); }}
  .handoff-protection-title {{ fill:white; font-size:11px; font-weight:780; letter-spacing:.05em; }}
  .handoff-protection-copy {{ fill:#d9d9d4; font-size:12px; }}
  .campus-feeder-arrow,.equipment-arrow,.rack-arrow {{ fill:none; stroke:var(--blue); stroke-width:4; }}
  .campus-feeder-label,.rack-label {{ fill:var(--blue); font-size:11px; font-weight:760; }}
  .equipment-card > rect {{ fill:white; stroke:var(--ink); stroke-width:2; }}
  .equipment-number {{ fill:var(--blue); }}
  .equipment-title {{ font-size:20px; font-weight:760; }}
  .equipment-verb {{ font-size:13px; fill:var(--muted); }}
  .equipment-coil,.equipment-switch,.gear-divider,.busway-rail,.busway-plugs {{ fill:none; stroke:var(--blue); stroke-width:3; }}
  .gear-cabinet {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:2; }}
  .gear-indicator {{ fill:var(--green); }}
  .lifecycle-pills rect {{ fill:var(--blue); }}
  .lifecycle-pills .unresolved-pill {{ fill:var(--amber); }}
  .lifecycle-pills text {{ fill:white; text-anchor:middle; font-size:10px; font-weight:760; }}
  footer {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(330px,570px); gap:10px 16px; min-height:0; max-height:48dvh; padding:9px 14px 10px; border-top:1.5px solid var(--ink); }}
  .state-nav {{ display:grid; grid-template-columns:repeat({len(payload["states"])},minmax(0,1fr)); gap:6px; }}
  .state-button {{ display:grid; grid-template-columns:auto 1fr; gap:7px; align-items:center; min-width:0; min-height:44px; padding:7px 8px; border:1.5px solid var(--ink); background:transparent; color:inherit; text-align:left; font:inherit; cursor:pointer; }}
  .state-nav-label {{ overflow:visible; text-overflow:clip; white-space:normal; }}
  .state-button[aria-selected="true"] {{ background:var(--ink); color:white; }}
  .state-copy {{ min-width:0; align-self:center; }}
  .state-copy h2 {{ margin:0 0 3px; font-size:16px; }}
  .state-copy p {{ margin:0; color:var(--muted); font-size:13px; line-height:1.3; }}
  details {{ grid-column:1/-1; min-width:0; min-height:0; border-top:1px solid var(--faint); padding-top:6px; }}
  details[open] {{ max-height:min(34dvh,320px); overflow:auto; overflow-x:hidden; overscroll-behavior:contain; }}
  summary {{ position:sticky; top:0; z-index:2; cursor:pointer; padding:3px 0; background:var(--paper); font-weight:700; }}
  .fact-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr)); gap:12px; min-width:0; margin-bottom:0; padding:0; list-style:none; }}
  .fact-card {{ min-width:0; border:1px solid var(--faint); padding:10px 12px; background:white; }}
  .fact-card p {{ margin:5px 0; line-height:1.35; }}
  .fact-ref,.fact-boundary {{ overflow-wrap:anywhere; word-break:break-word; color:var(--muted); font-size:11px; }}
  .fact-sources {{ min-width:0; overflow-wrap:anywhere; word-break:break-word; font-size:12px; }}
  a {{ overflow-wrap:anywhere; word-break:break-word; color:var(--blue); }}
  .visually-hidden {{ position:absolute !important; width:1px; height:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }}
  .responsive-visual {{ display:none; }}
  .responsive-scene {{ min-width:0; border:1.5px solid var(--ink); border-radius:10px; background:white; }}
  .responsive-scene h2,.responsive-scene h3,.responsive-scene p {{ margin:0; }}
  .responsive-kicker,.responsive-section-label,.responsive-stage-posture {{ color:var(--blue); text-transform:uppercase; letter-spacing:.06em; font-weight:760; }}
  .responsive-campus-map {{ display:grid; grid-template-columns:minmax(0,.8fr) auto minmax(0,1fr) auto minmax(0,1.4fr); align-items:center; }}
  .responsive-source,.responsive-distribution-node,.responsive-building,.responsive-source-lane,.responsive-role,.responsive-stage-card,.responsive-equipment-card {{ min-width:0; border:1px solid var(--faint); border-radius:8px; background:var(--paper); }}
  .responsive-source,.responsive-distribution-node {{ display:grid; place-items:center; text-align:center; font-weight:730; }}
  .responsive-distribution-node {{ border-color:var(--blue); background:var(--blue-soft); }}
  .responsive-distribution-node small {{ color:var(--muted); font-weight:500; }}
  .responsive-building-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); }}
  .responsive-building {{ position:relative; display:grid; place-items:end center; min-height:78px; text-align:center; }}
  .building-roof {{ position:absolute; top:9px; width:52%; height:34px; transform:skewY(-10deg); border:1.5px solid var(--blue); background:var(--blue-soft); }}
  .map-arrow,.fanout-marker {{ color:var(--blue); font-weight:800; }}
  .responsive-relation {{ color:var(--blue); font-weight:740; text-align:center; }}
  .responsive-fault-sequence {{ color:var(--blue); font-weight:800; letter-spacing:.055em; text-align:center; }}
  .responsive-fault-flow {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); }}
  .responsive-fault-stage {{ position:relative; min-width:0; border:1px solid var(--faint); border-radius:8px; background:var(--paper); }}
  .responsive-fault-number {{ color:var(--blue); font-size:11px; font-weight:800; }}
  .responsive-fault-symbol {{ display:grid; place-items:center; min-height:54px; border:1.5px solid var(--blue); border-radius:7px; background:var(--blue-soft); color:var(--blue); font-weight:820; letter-spacing:.04em; }}
  .responsive-fault-symbol.faulted_branch,.responsive-fault-symbol.open_protective_device,.responsive-fault-symbol.isolated_branch_with_conditional_peers {{ border-color:var(--red); background:var(--red-soft); color:var(--red); }}
  .responsive-stage-arrow {{ position:absolute; top:46%; right:-15px; z-index:2; color:var(--blue); font-size:24px; font-weight:800; }}
  .responsive-fault-boundary {{ border-top:1px solid var(--amber); color:var(--muted); }}
  .responsive-fault-boundary strong {{ color:var(--amber); text-transform:uppercase; letter-spacing:.05em; font-size:10px; }}
  .responsive-remaining-service {{ border:1.5px solid var(--blue); border-radius:8px; background:var(--blue-soft); }}
  .responsive-remaining-service h3 {{ color:var(--blue); }}
  .responsive-condition-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); }}
  .responsive-remaining-condition {{ display:grid; grid-template-columns:auto 1fr; align-items:start; min-width:0; border:1px solid var(--blue); border-radius:7px; background:white; }}
  .responsive-remaining-condition > span {{ display:grid; place-items:center; width:25px; height:25px; border-radius:50%; background:var(--blue); color:white; font-weight:800; }}
  .responsive-conditional-result {{ display:block; border-radius:7px; background:var(--ink); color:white; text-align:center; }}
  .responsive-scope {{ min-width:0; border:1px solid var(--amber); border-radius:8px; background:var(--amber-soft); }}
  .responsive-scope strong {{ color:var(--amber); }}
  .responsive-scope.responsive-isolation-scope {{ border-color:var(--red); background:var(--red-soft); }}
  .responsive-scope.responsive-isolation-scope strong {{ color:var(--red); }}
  .responsive-source-grid,.responsive-role-grid,.responsive-stage-grid,.responsive-equipment-chain {{ display:grid; }}
  .responsive-source-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
  .responsive-source-lane h3,.responsive-role h3,.responsive-stage-card h3,.responsive-equipment-card h3 {{ margin:0; }}
  .responsive-posture,.responsive-function {{ color:var(--blue); font-weight:680; }}
  .responsive-stop-line {{ display:flex; align-items:center; }}
  .responsive-stop-line span {{ flex:1; border-top:3px solid var(--blue); }}
  .responsive-stop-line b {{ border-left:5px solid var(--red); padding-left:7px; color:var(--red); }}
  .responsive-boundary-copy {{ color:var(--muted); }}
  .responsive-merge {{ display:grid; grid-template-columns:minmax(180px,.45fr) minmax(0,1fr); }}
  .responsive-merge-stop {{ display:grid; place-items:center; background:var(--ink); color:white; text-align:center; }}
  .responsive-merge-stop b {{ color:var(--amber); font-size:42px; }}
  .responsive-merge-stop span {{ color:#d9d9d4; }}
  .responsive-merge-evidence {{ min-width:0; }}
  .responsive-merge-evidence strong {{ color:var(--blue); }}
  .responsive-role-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
  .responsive-role-diagram {{ display:grid; place-items:center; border:1px solid var(--faint); border-radius:7px; background:white; }}
  .series-role {{ grid-template-columns:1fr auto 1fr auto 1fr; }}
  .parallel-role > div,.standby-role > div {{ display:flex; align-items:center; justify-content:center; width:100%; }}
  .parallel-role i {{ flex:1; border-top:2px solid var(--blue); }}
  .role-emphasis {{ border:1.5px solid var(--blue); border-radius:6px; background:var(--blue-soft); }}
  .responsive-stage-grid {{ grid-template-columns:repeat(4,minmax(0,1fr)); }}
  .responsive-stage-card {{ position:relative; }}
  .responsive-stage-number {{ display:grid; place-items:center; width:30px; height:30px; border-radius:50%; background:var(--blue); color:white; font-weight:800; }}
  .unresolved-stage {{ border-color:var(--amber); background:var(--amber-soft); }}
  .unresolved-stage .responsive-stage-number {{ background:var(--amber); }}
  .responsive-building-strip {{ display:grid; grid-template-columns:repeat(8,32px) minmax(0,1fr); align-items:center; }}
  .responsive-building-strip > span {{ display:grid; place-items:center; width:28px; height:36px; border:1px solid var(--faint); background:var(--paper); }}
  .responsive-building-strip .confirmed-building {{ border-color:var(--blue); background:var(--blue-soft); color:var(--blue); }}
  .responsive-building-entry {{ display:grid; grid-template-columns:180px minmax(0,1fr); align-items:center; }}
  .responsive-cutaway-building {{ display:grid; grid-template-rows:repeat(3,1fr); min-height:130px; transform:skewY(-3deg); border:2px solid var(--blue); background:var(--blue-soft); }}
  .responsive-cutaway-building span {{ border-bottom:1px solid var(--blue); }}
  .responsive-protection-handoff {{ border-radius:7px; background:var(--ink); color:white; font-weight:700; }}
  .responsive-lifecycle-pills {{ display:flex; flex-wrap:wrap; }}
  .responsive-lifecycle-pills span {{ border-radius:999px; background:var(--blue); color:white; }}
  .responsive-lifecycle-pills .unresolved {{ background:var(--amber); }}
  .responsive-equipment-chain {{ grid-template-columns:repeat(4,minmax(0,1fr)) auto; align-items:stretch; }}
  .responsive-equipment-card > span:first-child {{ color:var(--blue); font-weight:760; }}
  .rack-destination {{ display:grid; place-items:center; color:var(--blue); }}
  @media (max-width:1280px), (max-height:760px) {{
    header {{ grid-template-columns:minmax(0,1fr) minmax(280px,500px); gap:10px; padding:7px 12px; }}
    h1 {{ font-size:22px; }}
    .objective {{ font-size:11px; }}
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:6px; }}
    footer {{ padding:6px 9px 7px; }}
    .state-nav {{ gap:4px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; padding:4px; text-align:center; font-size:11px; }}
    .visual-shell {{ display:none; }}
    .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:4px; font-size:12px; }}
    .responsive-scene {{ padding:11px; }}
    .responsive-scene h2 {{ margin-bottom:8px; font-size:19px; }}
    .responsive-scene h3 {{ margin-bottom:5px; font-size:15px; }}
    .responsive-kicker {{ margin-bottom:4px !important; font-size:11px; }}
    .responsive-campus-map,.responsive-fault-flow,.responsive-condition-grid,.responsive-source-grid,.responsive-role-grid,.responsive-stage-grid,.responsive-equipment-chain {{ gap:8px; }}
    .responsive-source,.responsive-distribution-node,.responsive-building,.responsive-fault-stage,.responsive-source-lane,.responsive-role,.responsive-stage-card,.responsive-equipment-card {{ padding:8px; font-size:12px; line-height:1.35; }}
    .responsive-distribution-node small {{ margin-top:4px; font-size:11px; }}
    .responsive-building-grid {{ gap:5px; }}
    .responsive-building strong {{ margin-top:42px; font-size:11px; }}
    .responsive-relation,.responsive-fault-sequence,.responsive-remaining-service,.responsive-scope,.responsive-merge,.responsive-role-diagram,.responsive-building-strip,.responsive-building-entry {{ margin-top:8px; }}
    .responsive-relation,.responsive-remaining-service,.responsive-scope,.responsive-merge-evidence,.responsive-merge-stop,.responsive-role-diagram,.responsive-building-strip,.responsive-building-entry {{ padding:8px; font-size:12px; line-height:1.4; }}
    .responsive-fault-symbol {{ margin:6px 0; padding:6px; }}
    .responsive-fault-boundary {{ margin-top:7px; padding-top:6px; }}
    .responsive-condition-grid {{ margin-top:8px; }}
    .responsive-remaining-condition {{ gap:7px; padding:7px; }}
    .responsive-remaining-condition p {{ font-size:12px; line-height:1.35; }}
    .responsive-conditional-result,.responsive-protection-handoff {{ margin-top:8px; padding:7px; }}
    .responsive-stop-line {{ margin:8px 0; }}
    .responsive-boundary-copy,.responsive-role p,.responsive-stage-card p,.responsive-equipment-card p {{ font-size:12px; line-height:1.4; }}
    .responsive-role-diagram {{ min-height:108px; gap:5px; }}
    .role-emphasis,.responsive-lifecycle-pills span {{ padding:5px 7px; }}
    .responsive-section-label,.responsive-stage-posture {{ display:block; margin-top:7px; font-size:10px; }}
    .responsive-stage-number {{ margin-bottom:5px; }}
    .responsive-building-strip {{ gap:4px; }}
    .responsive-building-strip strong {{ margin-left:8px; }}
    .responsive-building-entry {{ gap:12px; }}
    .responsive-lifecycle-pills {{ gap:5px; margin-top:8px; }}
    .responsive-equipment-chain {{ margin-top:10px; }}
  }}
  @media (max-width:1100px) {{
    header {{ grid-template-columns:1fr; gap:2px; }}
    .responsive-fault-flow,.responsive-source-grid,.responsive-role-grid,.responsive-stage-grid,.responsive-equipment-chain {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
    .responsive-stage-arrow {{ display:none; }}
    .responsive-source-lane:last-child,.rack-destination {{ grid-column:1/-1; }}
    .responsive-building-strip {{ grid-template-columns:repeat(8,28px); }}
    .responsive-building-strip strong {{ grid-column:1/-1; margin:5px 0 0; }}
    details[open] {{ position:fixed; inset:10px; z-index:10; max-height:none; padding:10px; overflow:auto; overflow-x:hidden; border:1.5px solid var(--ink); background:var(--paper); }}
  }}
  @media (max-height:520px) and (orientation:landscape) {{
    header {{ grid-template-columns:1fr; padding:3px 8px; }}
    h1 {{ margin:1px 0; font-size:17px; }}
    .eyebrow,.phase-question {{ font-size:9px; }}
    .objective {{ display:none; }}
    main {{ padding:3px 6px; }}
    footer {{ grid-template-columns:minmax(0,1fr) minmax(220px,330px) auto; gap:5px; padding:3px 6px; }}
    .state-button {{ grid-template-columns:1fr; gap:0; min-height:34px; padding:2px 3px; text-align:center; font-size:10px; }}
    .state-copy h2 {{ font-size:11px; }}
    .state-copy p {{ display:none; }}
    details {{ grid-column:auto; align-self:center; border-top:0; padding-top:0; font-size:10px; }}
    .evidence-count {{ display:none; }}
    .responsive-visual {{ padding:2px; font-size:10px; }}
    .responsive-scene {{ padding:7px; }}
    .responsive-scene h2 {{ margin-bottom:4px; font-size:14px; }}
    .responsive-scene h3 {{ margin-bottom:3px; font-size:12px; }}
    .responsive-campus-map {{ grid-template-columns:1fr auto 1fr; gap:4px; }}
    .fanout-marker,.responsive-building-grid {{ grid-column:1/-1; }}
    .responsive-fault-flow,.responsive-source-grid,.responsive-role-grid,.responsive-stage-grid,.responsive-equipment-chain {{ grid-template-columns:repeat(2,minmax(0,1fr)); gap:5px; }}
    .responsive-source,.responsive-distribution-node,.responsive-building,.responsive-fault-stage,.responsive-source-lane,.responsive-role,.responsive-stage-card,.responsive-equipment-card {{ padding:5px; font-size:10px; }}
    .responsive-role-diagram {{ min-height:82px; padding:4px; font-size:10px; }}
    .responsive-remaining-service,.responsive-scope,.responsive-merge-evidence,.responsive-merge-stop,.responsive-building-strip,.responsive-building-entry {{ padding:5px; font-size:10px; }}
    .responsive-building-entry {{ grid-template-columns:110px 1fr; }}
    .responsive-cutaway-building {{ min-height:90px; }}
  }}
  @media (max-width:520px) and (orientation:portrait) {{
    header {{ padding:6px 8px; }}
    h1 {{ font-size:19px; }}
    .objective {{ display:none; }}
    footer {{ grid-template-columns:1fr; gap:4px; padding:5px 7px; }}
    .state-button {{ min-height:42px; padding:3px 2px; font-size:10px; }}
    .state-number {{ font-size:9px; }}
    .state-copy h2 {{ font-size:13px; }}
    .state-copy p {{ display:none; }}
    .responsive-visual {{ padding:2px; font-size:12px; }}
    .responsive-scene {{ padding:9px; }}
    .responsive-campus-map,.responsive-fault-flow,.responsive-condition-grid,.responsive-source-grid,.responsive-role-grid,.responsive-stage-grid,.responsive-equipment-chain,.responsive-merge,.responsive-building-entry {{ grid-template-columns:1fr; }}
    .responsive-campus-map {{ gap:5px; }}
    .map-arrow {{ transform:rotate(90deg); text-align:center; }}
    .fanout-marker {{ text-align:center; }}
    .responsive-building-grid {{ gap:5px; }}
    .responsive-source-lane:last-child,.rack-destination {{ grid-column:auto; }}
    .responsive-role-diagram {{ min-height:105px; }}
    .responsive-building-strip {{ grid-template-columns:repeat(4,28px); }}
    .responsive-building-strip strong {{ grid-column:1/-1; }}
    .responsive-cutaway-building {{ min-height:110px; }}
  }}
</style>
</head>
<body>
<header>
  <div>
    <p class="eyebrow">Phase {phase["number"]} · {_escape(phase["title"])}</p>
    <h1>{_escape(payload["pilot"]["title"])}</h1>
    <p class="phase-question">{_escape(phase["anchor_question"])}</p>
  </div>
  <p class="objective">{_escape(payload["pilot"]["learning_objective"])}</p>
</header>
<main>
  <section class="visual-shell" aria-label="Instructor-controlled campus distribution teaching surface">
    <svg id="visual" role="img" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" aria-labelledby="visual-title visual-description">
      <title id="visual-title">Campus distribution and resilience landscape</title>
      <desc id="visual-description">Five manually selected views explain a generic isometric fan-out, conditional feeder-fault isolation, separate Abilene source boundaries, distinct resilience roles, and the functional path into one building. Abilene lifecycle disclosures remain backstage in the evidence payload.</desc>
      {_fanout_svg(payload["generic_fanout"])}
      {_feeder_fault_isolation_svg(payload["feeder_fault_isolation"])}
      {_source_boundary_svg(payload["abilene_source_boundary"])}
      {_roles_svg(payload["resilience_roles"])}
      {_handoff_svg(payload["phase4_handoff"])}
    </svg>
  </section>
  {responsive}
</main>
<footer>
  <nav class="state-nav" role="tablist" aria-label="Manual Phase 3 teaching states">{state_buttons}</nav>
  <section class="state-copy" aria-labelledby="state-title"><h2 id="state-title"></h2><p id="state-instruction"></p></section>
  <p id="state-status" class="visually-hidden" aria-live="polite"></p>
  <details><summary><span class="evidence-label">Evidence</span><span class="evidence-count"> used in this pilot · {len(payload["evidence"]["facts"])} facts · {len(payload["evidence"]["sources"])} sources</span></summary><ul class="fact-list">{evidence}</ul></details>
</footer>
<script id="pilot-data" type="application/json">{serialized}</script>
<script>
"use strict";
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
const pilot = JSON.parse(document.getElementById("pilot-data").textContent);
const buttons = [...document.querySelectorAll("[data-state-index]")];
const evidenceDrawer = document.querySelector("details");
let current = 0;

function setVisible(selector, selected, dataKey) {{
  document.querySelectorAll(selector).forEach(element => {{
    element.toggleAttribute("hidden", !selected.includes(element.dataset[dataKey]));
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
  document.querySelectorAll("[data-generic-fanout]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_generic_fanout);
  }});
  document.querySelectorAll("[data-feeder-fault-isolation]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_feeder_fault_isolation);
  }});
  setVisible("[data-abilene-source-id]", state.abilene_source_ids, "abileneSourceId");
  document.querySelectorAll("[data-abilene-boundary]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_abilene_merge);
  }});
  document.querySelectorAll("[data-abilene-merge]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_abilene_merge);
  }});
  setVisible("[data-resilience-role-id]", state.resilience_role_ids, "resilienceRoleId");
  document.querySelectorAll("[data-resilience-roles]").forEach(element => {{
    element.toggleAttribute("hidden", state.resilience_role_ids.length === 0);
  }});
  document.querySelectorAll("[data-phase4-handoff]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_phase4_handoff);
  }});
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
evidenceDrawer.addEventListener("toggle", () => {{
  if (!evidenceDrawer.open) resetTeachingScroll();
}});
document.querySelector(".state-nav").addEventListener("keydown", event => {{
  let target = null;
  if (event.key === "ArrowRight" || event.key === "ArrowDown") target = current + 1;
  if (event.key === "ArrowLeft" || event.key === "ArrowUp") target = current - 1;
  if (event.key === "Home") target = 0;
  if (event.key === "End") target = pilot.states.length - 1;
  if (target !== null) {{ event.preventDefault(); activate(target, true); }}
}});
activate(0);
</script>
</body>
</html>
"""
