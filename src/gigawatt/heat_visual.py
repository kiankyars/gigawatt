"""Evidence-bound Phase 6 heat-rejection teaching surface."""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from gigawatt import teaching_visuals as base

SCHEMA_VERSION = 1
CANVAS_KIND = "heat_return_v1"
CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 900

ENERGY_IDS = {"electrical_input", "useful_compute_service", "heat_obligation"}
LIQUID_IDS = {
    "die_heat_source",
    "cold_plate_heat_exchange",
    "rack_manifold_distribution",
    "technology_loop_return",
    "conditional_cdu_boundary",
    "facility_loop_entry",
}
AIR_IDS = {
    "air_cooled_auxiliaries",
    "warm_air_return",
    "conditional_air_handler",
    "facility_loop_merge",
}
FACILITY_IDS = {
    "facility_loop_transport",
    "air_cooled_terminal",
    "atmosphere_sink",
}
WATER_IDS = {
    "rejection_process_water",
    "initial_fill",
    "anticipated_maintenance",
    "measured_operating_water",
}
KNOWN_IDS = {
    "selected_direct_liquid_design",
    "selected_facility_loop",
    "selected_air_cooled_terminal",
    "disclosed_water_categories",
}
UNKNOWN_IDS = {
    "cdu_presence_and_configuration",
    "cooling_interfaces",
    "residual_air_equipment",
    "loop_setpoints_and_measurements",
    "measured_site_water",
}
JOURNEY_IDS = [
    "generate",
    "transmit",
    "campus",
    "building",
    "compute",
    "reject_heat",
]
STATE_IDS = [
    "rack_cooling_split",
    "technology_loop",
    "cdu_boundary",
    "parallel_residual_air",
    "facility_heat_rejection",
    "water_accounting",
    "whole_journey_closure",
]
STATE_SELECTOR_INVARIANTS = {
    "rack_cooling_split": {
        "energy_view_ids": ("heat_obligation",),
        "liquid_stage_ids": (
            "die_heat_source",
            "cold_plate_heat_exchange",
            "rack_manifold_distribution",
        ),
        "residual_air_stage_ids": (
            "air_cooled_auxiliaries",
            "warm_air_return",
        ),
        "facility_stage_ids": (),
        "water_account_ids": (),
        "abilene_known_ids": ("selected_direct_liquid_design",),
        "abilene_unknown_ids": (
            "residual_air_equipment",
            "loop_setpoints_and_measurements",
        ),
        "journey_stage_ids": (),
    },
    "technology_loop": {
        "energy_view_ids": (),
        "liquid_stage_ids": (
            "cold_plate_heat_exchange",
            "rack_manifold_distribution",
            "technology_loop_return",
        ),
        "residual_air_stage_ids": (),
        "facility_stage_ids": (),
        "water_account_ids": (),
        "abilene_known_ids": ("selected_direct_liquid_design",),
        "abilene_unknown_ids": (
            "cooling_interfaces",
            "loop_setpoints_and_measurements",
        ),
        "journey_stage_ids": (),
    },
    "cdu_boundary": {
        "energy_view_ids": (),
        "liquid_stage_ids": (
            "rack_manifold_distribution",
            "technology_loop_return",
            "conditional_cdu_boundary",
            "facility_loop_entry",
        ),
        "residual_air_stage_ids": (),
        "facility_stage_ids": (),
        "water_account_ids": (),
        "abilene_known_ids": (
            "selected_direct_liquid_design",
            "selected_facility_loop",
        ),
        "abilene_unknown_ids": (
            "cdu_presence_and_configuration",
            "cooling_interfaces",
            "loop_setpoints_and_measurements",
        ),
        "journey_stage_ids": (),
    },
    "parallel_residual_air": {
        "energy_view_ids": (),
        "liquid_stage_ids": (
            "cold_plate_heat_exchange",
            "rack_manifold_distribution",
            "technology_loop_return",
            "conditional_cdu_boundary",
            "facility_loop_entry",
        ),
        "residual_air_stage_ids": (
            "air_cooled_auxiliaries",
            "warm_air_return",
            "conditional_air_handler",
            "facility_loop_merge",
        ),
        "facility_stage_ids": (),
        "water_account_ids": (),
        "abilene_known_ids": (
            "selected_direct_liquid_design",
            "selected_facility_loop",
        ),
        "abilene_unknown_ids": (
            "cdu_presence_and_configuration",
            "cooling_interfaces",
            "residual_air_equipment",
            "loop_setpoints_and_measurements",
        ),
        "journey_stage_ids": (),
    },
    "facility_heat_rejection": {
        "energy_view_ids": (),
        "liquid_stage_ids": ("facility_loop_entry",),
        "residual_air_stage_ids": ("facility_loop_merge",),
        "facility_stage_ids": (
            "facility_loop_transport",
            "air_cooled_terminal",
            "atmosphere_sink",
        ),
        "water_account_ids": (),
        "abilene_known_ids": (
            "selected_facility_loop",
            "selected_air_cooled_terminal",
        ),
        "abilene_unknown_ids": (
            "cooling_interfaces",
            "residual_air_equipment",
            "loop_setpoints_and_measurements",
        ),
        "journey_stage_ids": (),
    },
    "water_accounting": {
        "energy_view_ids": (),
        "liquid_stage_ids": (),
        "residual_air_stage_ids": (),
        "facility_stage_ids": ("air_cooled_terminal",),
        "water_account_ids": (
            "rejection_process_water",
            "initial_fill",
            "anticipated_maintenance",
            "measured_operating_water",
        ),
        "abilene_known_ids": (
            "selected_air_cooled_terminal",
            "disclosed_water_categories",
        ),
        "abilene_unknown_ids": ("measured_site_water",),
        "journey_stage_ids": (),
    },
    "whole_journey_closure": {
        "energy_view_ids": (),
        "liquid_stage_ids": (
            "die_heat_source",
            "cold_plate_heat_exchange",
            "rack_manifold_distribution",
            "technology_loop_return",
            "conditional_cdu_boundary",
            "facility_loop_entry",
        ),
        "residual_air_stage_ids": (
            "air_cooled_auxiliaries",
            "warm_air_return",
            "conditional_air_handler",
            "facility_loop_merge",
        ),
        "facility_stage_ids": (
            "facility_loop_transport",
            "air_cooled_terminal",
            "atmosphere_sink",
        ),
        "water_account_ids": (
            "rejection_process_water",
            "measured_operating_water",
        ),
        "abilene_known_ids": (
            "selected_direct_liquid_design",
            "selected_facility_loop",
            "selected_air_cooled_terminal",
        ),
        "abilene_unknown_ids": (
            "cdu_presence_and_configuration",
            "cooling_interfaces",
            "residual_air_equipment",
            "loop_setpoints_and_measurements",
            "measured_site_water",
        ),
        "journey_stage_ids": tuple(JOURNEY_IDS),
    },
}
CONDITIONAL_STAGE_IDS = {
    "liquid-stage": {"conditional_cdu_boundary"},
    "air-stage": {"conditional_air_handler", "facility_loop_merge"},
}
PRIMARY_LAYERS = [
    "residual_air_path",
    "liquid_path",
    "liquid_path",
    "residual_air_path",
    "facility_rejection",
    "abilene_mapping",
    "journey_closure",
]
GAP_IDS = {
    "abilene_cdu_and_interface_topology",
    "abilene_residual_air_path",
    "abilene_thermal_operating_point",
    "abilene_measured_water_account",
}

TOP_LEVEL_FIELDS = {
    "schema_version",
    "id",
    "title",
    "phase",
    "learning_objective",
    "evidence_files",
    "interaction",
    "canvas",
    "energy_handoff",
    "liquid_path",
    "residual_air_path",
    "facility_rejection",
    "abilene_mapping",
    "journey_closure",
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
    "closure_requires",
}
ENERGY_FIELDS = {"title", "body", "views", "allocation_guard"}
VIEW_FIELDS = {"id", "title", "carrier", "boundary", "fact_refs"}
GUARD_FIELDS = {"id", "body", "fact_refs"}
ENERGY_GUARD_FIELDS = GUARD_FIELDS | {"concise_boundary"}
PATH_FIELDS = {"title", "body", "stages"}
STAGE_FIELDS = {"id", "title", "verb", "carrier", "boundary", "fact_refs"}
CONDITIONAL_STAGE_FIELDS = STAGE_FIELDS | {"render_posture"}
FACILITY_FIELDS = {"title", "body", "stages", "water_accounts"}
FACILITY_STAGE_FIELDS = STAGE_FIELDS | {"evidence_posture"}
WATER_FIELDS = {
    "id",
    "title",
    "display",
    "accounting_posture",
    "boundary",
    "fact_refs",
}
MAPPING_FIELDS = {"title", "known", "unknown", "validation_boundary"}
KNOWN_FIELDS = {"id", "title", "body", "evidence_posture", "fact_refs"}
UNKNOWN_FIELDS = {"id", "title", "body", "fact_refs"}
JOURNEY_FIELDS = {"title", "body", "stages", "closure_guard"}
JOURNEY_STAGE_FIELDS = {
    "id",
    "number",
    "title",
    "carrier",
    "abilene_posture",
    "fact_refs",
}
GAP_FIELDS = {
    "id",
    "gap",
    "renderer_guard",
    "related_state_ids",
    "related_fact_refs",
}
STATE_FIELDS = {
    "id",
    "nav_label",
    "title",
    "instruction",
    "energy_view_ids",
    "liquid_stage_ids",
    "residual_air_stage_ids",
    "facility_stage_ids",
    "water_account_ids",
    "abilene_known_ids",
    "abilene_unknown_ids",
    "journey_stage_ids",
}


class HeatVisualError(base.TeachingVisualError):
    """Raised when Phase 6 escapes its teaching or evidence contract."""


def _validate_compiled_state_selectors(states: Any, *, location: str) -> None:
    if not isinstance(states, list) or len(states) != len(STATE_IDS):
        raise HeatVisualError(
            f"{location} must contain exactly {len(STATE_IDS)} states"
        )
    for index, state_id in enumerate(STATE_IDS):
        state = states[index]
        state_location = f"{location}[{index}]"
        if not isinstance(state, Mapping) or state.get("id") != state_id:
            raise HeatVisualError(f"{state_location}.id must remain {state_id!r}")
        for field, expected_values in STATE_SELECTOR_INVARIANTS[state_id].items():
            expected = list(expected_values)
            if state.get(field) != expected:
                raise HeatVisualError(
                    f"{state_location}.{field} must exactly match the "
                    f"{state_id} selector invariant {expected}"
                )


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
        raise HeatVisualError("viewport dimensions must be positive integers")
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
        "columns": 6,
        "minimum_text_px": 13,
        "scroll_axis": "none",
    }


def _exact(value: Any, fields: set[str], location: str) -> dict[str, Any]:
    try:
        return base._exact_fields(value, fields, location)
    except base.TeachingVisualError as error:
        raise HeatVisualError(str(error)) from error


def _text(value: Any, location: str, *, maximum: int = 240) -> str:
    try:
        return base._text(value, location, maximum=maximum)
    except base.TeachingVisualError as error:
        raise HeatVisualError(str(error)) from error


def _identifier(value: Any, location: str) -> str:
    try:
        return base._id(value, location)
    except base.TeachingVisualError as error:
        raise HeatVisualError(str(error)) from error


def _list(
    value: Any,
    location: str,
    *,
    minimum: int,
    maximum: int,
    item_limit: int = 80,
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
        raise HeatVisualError(str(error)) from error


def _refs(
    value: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[str]:
    try:
        return base._fact_refs(value, location, ledgers)
    except base.TeachingVisualError as error:
        raise HeatVisualError(str(error)) from error


def _records(
    raw: Any,
    *,
    location: str,
    expected_ids: set[str],
    ledgers: Mapping[str, dict[str, Any]],
    kind: str,
) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(expected_ids):
        raise HeatVisualError(
            f"{location} must contain exactly {len(expected_ids)} {kind} records"
        )
    records: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_record in enumerate(raw):
        record_location = f"{location}[{index}]"
        fields = VIEW_FIELDS if kind == "energy-view" else STAGE_FIELDS
        if isinstance(raw_record, dict) and (
            "render_posture" in raw_record or "evidence_posture" in raw_record
        ):
            fields = (
                CONDITIONAL_STAGE_FIELDS
                if "render_posture" in raw_record
                else FACILITY_STAGE_FIELDS
            )
        record = _exact(raw_record, fields, record_location)
        record_id = _identifier(record["id"], f"{record_location}.id")
        ids.append(record_id)
        normalized = {
            "id": record_id,
            "title": _text(record["title"], f"{record_location}.title", maximum=140),
            "boundary": _text(
                record["boundary"], f"{record_location}.boundary", maximum=620
            ),
            "fact_refs": _refs(
                record["fact_refs"], f"{record_location}.fact_refs", ledgers
            ),
        }
        if kind == "energy-view":
            normalized["carrier"] = _text(
                record["carrier"], f"{record_location}.carrier", maximum=180
            )
        else:
            normalized["verb"] = _text(
                record["verb"], f"{record_location}.verb", maximum=190
            )
            normalized["carrier"] = _text(
                record["carrier"], f"{record_location}.carrier", maximum=160
            )
            if "render_posture" in record:
                posture = _identifier(
                    record["render_posture"],
                    f"{record_location}.render_posture",
                )
                if posture != "generic_reference_unresolved_at_abilene":
                    raise HeatVisualError(
                        f"{record_location}.render_posture must remain conditional"
                    )
                normalized["render_posture"] = posture
            if "evidence_posture" in record:
                normalized["evidence_posture"] = _identifier(
                    record["evidence_posture"],
                    f"{record_location}.evidence_posture",
                )
        records.append(normalized)
    if len(ids) != len(set(ids)) or set(ids) != expected_ids:
        raise HeatVisualError(f"{location} contains an incomplete or duplicate ID set")
    return records


def _normalize_energy(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.energy_handoff"
    value = _exact(raw, ENERGY_FIELDS, location)
    guard_location = f"{location}.allocation_guard"
    guard = _exact(value["allocation_guard"], ENERGY_GUARD_FIELDS, guard_location)
    concise_boundary = _text(
        guard["concise_boundary"],
        f"{guard_location}.concise_boundary",
        maximum=180,
    )
    if "not an energy slice" not in concise_boundary.casefold() or (
        "no site heat fraction" not in concise_boundary.casefold()
    ):
        raise HeatVisualError(
            "energy handoff concise boundary must reject an energy slice and site heat fraction"
        )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=170),
        "body": _text(value["body"], f"{location}.body", maximum=680),
        "views": _records(
            value["views"],
            location=f"{location}.views",
            expected_ids=ENERGY_IDS,
            ledgers=ledgers,
            kind="energy-view",
        ),
        "allocation_guard": {
            "id": _identifier(guard["id"], f"{guard_location}.id"),
            "body": _text(guard["body"], f"{guard_location}.body", maximum=620),
            "concise_boundary": concise_boundary,
            "fact_refs": _refs(
                guard["fact_refs"], f"{guard_location}.fact_refs", ledgers
            ),
        },
    }


def _normalize_path(
    raw: Any,
    *,
    location: str,
    expected_ids: set[str],
    ledgers: Mapping[str, dict[str, Any]],
    kind: str,
) -> dict[str, Any]:
    value = _exact(raw, PATH_FIELDS, location)
    stages = _records(
        value["stages"],
        location=f"{location}.stages",
        expected_ids=expected_ids,
        ledgers=ledgers,
        kind=kind,
    )
    expected_conditional_ids = CONDITIONAL_STAGE_IDS.get(kind, set())
    actual_conditional_ids = {
        stage["id"] for stage in stages if "render_posture" in stage
    }
    if actual_conditional_ids != expected_conditional_ids:
        raise HeatVisualError(
            f"{location}.stages must mark exactly {sorted(expected_conditional_ids)} "
            "as generic references unresolved at Abilene"
        )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=170),
        "body": _text(value["body"], f"{location}.body", maximum=680),
        "stages": stages,
    }


def _normalize_facility(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.facility_rejection"
    value = _exact(raw, FACILITY_FIELDS, location)
    stages = _records(
        value["stages"],
        location=f"{location}.stages",
        expected_ids=FACILITY_IDS,
        ledgers=ledgers,
        kind="facility-stage",
    )
    if (
        not isinstance(value["water_accounts"], list)
        or len(value["water_accounts"]) != 4
    ):
        raise HeatVisualError(
            f"{location}.water_accounts must contain exactly four accounts"
        )
    accounts: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_account in enumerate(value["water_accounts"]):
        account_location = f"{location}.water_accounts[{index}]"
        account = _exact(raw_account, WATER_FIELDS, account_location)
        account_id = _identifier(account["id"], f"{account_location}.id")
        ids.append(account_id)
        accounts.append(
            {
                "id": account_id,
                "title": _text(
                    account["title"], f"{account_location}.title", maximum=110
                ),
                "display": _text(
                    account["display"], f"{account_location}.display", maximum=220
                ),
                "accounting_posture": _identifier(
                    account["accounting_posture"],
                    f"{account_location}.accounting_posture",
                ),
                "boundary": _text(
                    account["boundary"],
                    f"{account_location}.boundary",
                    maximum=440,
                ),
                "fact_refs": _refs(
                    account["fact_refs"],
                    f"{account_location}.fact_refs",
                    ledgers,
                ),
            }
        )
    if len(ids) != len(set(ids)) or set(ids) != WATER_IDS:
        raise HeatVisualError("water accounts must remain separate and complete")
    measured = next(
        item for item in accounts if item["id"] == "measured_operating_water"
    )
    if measured["accounting_posture"] != "explicit_unknown_not_zero":
        raise HeatVisualError("measured operating water must remain unknown, not zero")
    return {
        "title": _text(value["title"], f"{location}.title", maximum=170),
        "body": _text(value["body"], f"{location}.body", maximum=680),
        "stages": stages,
        "water_accounts": accounts,
    }


def _normalize_mapping(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.abilene_mapping"
    value = _exact(raw, MAPPING_FIELDS, location)

    def normalize_items(
        raw_items: Any,
        *,
        fields: set[str],
        expected_ids: set[str],
        item_kind: str,
    ) -> list[dict[str, Any]]:
        if not isinstance(raw_items, list) or len(raw_items) != len(expected_ids):
            raise HeatVisualError(
                f"{location}.{item_kind} must contain {len(expected_ids)} records"
            )
        items: list[dict[str, Any]] = []
        ids: list[str] = []
        for index, raw_item in enumerate(raw_items):
            item_location = f"{location}.{item_kind}[{index}]"
            item = _exact(raw_item, fields, item_location)
            item_id = _identifier(item["id"], f"{item_location}.id")
            ids.append(item_id)
            normalized = {
                "id": item_id,
                "title": _text(item["title"], f"{item_location}.title", maximum=120),
                "body": _text(item["body"], f"{item_location}.body", maximum=560),
                "fact_refs": _refs(
                    item["fact_refs"], f"{item_location}.fact_refs", ledgers
                ),
            }
            if "evidence_posture" in item:
                normalized["evidence_posture"] = _identifier(
                    item["evidence_posture"],
                    f"{item_location}.evidence_posture",
                )
            items.append(normalized)
        if len(ids) != len(set(ids)) or set(ids) != expected_ids:
            raise HeatVisualError(f"{location}.{item_kind} ID set is incomplete")
        return items

    validation_location = f"{location}.validation_boundary"
    validation = _exact(value["validation_boundary"], GUARD_FIELDS, validation_location)
    return {
        "title": _text(value["title"], f"{location}.title", maximum=180),
        "known": normalize_items(
            value["known"],
            fields=KNOWN_FIELDS,
            expected_ids=KNOWN_IDS,
            item_kind="known",
        ),
        "unknown": normalize_items(
            value["unknown"],
            fields=UNKNOWN_FIELDS,
            expected_ids=UNKNOWN_IDS,
            item_kind="unknown",
        ),
        "validation_boundary": {
            "id": _identifier(validation["id"], f"{validation_location}.id"),
            "body": _text(
                validation["body"], f"{validation_location}.body", maximum=620
            ),
            "fact_refs": _refs(
                validation["fact_refs"],
                f"{validation_location}.fact_refs",
                ledgers,
            ),
        },
    }


def _normalize_journey(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.journey_closure"
    value = _exact(raw, JOURNEY_FIELDS, location)
    if not isinstance(value["stages"], list) or len(value["stages"]) != 6:
        raise HeatVisualError(f"{location}.stages must contain exactly six phases")
    stages: list[dict[str, Any]] = []
    ids: list[str] = []
    numbers: list[int] = []
    for index, raw_stage in enumerate(value["stages"]):
        stage_location = f"{location}.stages[{index}]"
        stage = _exact(raw_stage, JOURNEY_STAGE_FIELDS, stage_location)
        stage_id = _identifier(stage["id"], f"{stage_location}.id")
        if type(stage["number"]) is not int:
            raise HeatVisualError(f"{stage_location}.number must be an integer")
        ids.append(stage_id)
        numbers.append(stage["number"])
        stages.append(
            {
                "id": stage_id,
                "number": stage["number"],
                "title": _text(stage["title"], f"{stage_location}.title", maximum=80),
                "carrier": _text(
                    stage["carrier"], f"{stage_location}.carrier", maximum=200
                ),
                "abilene_posture": _text(
                    stage["abilene_posture"],
                    f"{stage_location}.abilene_posture",
                    maximum=260,
                ),
                "fact_refs": _refs(
                    stage["fact_refs"], f"{stage_location}.fact_refs", ledgers
                ),
            }
        )
    if ids != JOURNEY_IDS or numbers != list(range(1, 7)):
        raise HeatVisualError("journey closure must preserve phases 1 through 6")
    guard_location = f"{location}.closure_guard"
    guard = _exact(value["closure_guard"], GUARD_FIELDS, guard_location)
    return {
        "title": _text(value["title"], f"{location}.title", maximum=170),
        "body": _text(value["body"], f"{location}.body", maximum=680),
        "stages": stages,
        "closure_guard": {
            "id": _identifier(guard["id"], f"{guard_location}.id"),
            "body": _text(guard["body"], f"{guard_location}.body", maximum=620),
            "fact_refs": _refs(
                guard["fact_refs"], f"{guard_location}.fact_refs", ledgers
            ),
        },
    }


def _normalize_gaps(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    location = "pilot manifest.evidence_gaps"
    if not isinstance(raw, list) or len(raw) != 4:
        raise HeatVisualError(f"{location} must contain exactly four guards")
    gaps: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, raw_gap in enumerate(raw):
        gap_location = f"{location}[{index}]"
        gap = _exact(raw_gap, GAP_FIELDS, gap_location)
        gap_id = _identifier(gap["id"], f"{gap_location}.id")
        ids.append(gap_id)
        state_ids = _list(
            gap["related_state_ids"],
            f"{gap_location}.related_state_ids",
            minimum=1,
            maximum=6,
        )
        unknown_states = sorted(set(state_ids) - set(STATE_IDS))
        if unknown_states:
            raise HeatVisualError(
                f"{gap_location}.related_state_ids contains unknown states {unknown_states}"
            )
        gaps.append(
            {
                "id": gap_id,
                "gap": _text(gap["gap"], f"{gap_location}.gap", maximum=620),
                "renderer_guard": _text(
                    gap["renderer_guard"],
                    f"{gap_location}.renderer_guard",
                    maximum=620,
                ),
                "related_state_ids": state_ids,
                "related_fact_refs": _refs(
                    gap["related_fact_refs"],
                    f"{gap_location}.related_fact_refs",
                    ledgers,
                ),
            }
        )
    if len(ids) != len(set(ids)) or set(ids) != GAP_IDS:
        raise HeatVisualError("heat evidence-gap guard set is incomplete")
    return gaps


def _normalize_states(
    raw: Any,
    *,
    id_sets: Mapping[str, set[str]],
) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(STATE_IDS):
        raise HeatVisualError(
            f"pilot manifest.states must contain exactly {len(STATE_IDS)} states"
        )
    selector_fields = {
        "energy_view_ids": "energy",
        "liquid_stage_ids": "liquid",
        "residual_air_stage_ids": "air",
        "facility_stage_ids": "facility",
        "water_account_ids": "water",
        "abilene_known_ids": "known",
        "abilene_unknown_ids": "unknown",
        "journey_stage_ids": "journey",
    }
    states: list[dict[str, Any]] = []
    ids: list[str] = []
    nav_labels: list[str] = []
    used = {namespace: set() for namespace in id_sets}
    for index, raw_state in enumerate(raw):
        location = f"pilot manifest.states[{index}]"
        state = _exact(raw_state, STATE_FIELDS, location)
        state_id = _identifier(state["id"], f"{location}.id")
        normalized: dict[str, Any] = {
            "id": state_id,
            "nav_label": _text(state["nav_label"], f"{location}.nav_label", maximum=28),
            "title": _text(state["title"], f"{location}.title", maximum=160),
            "instruction": _text(
                state["instruction"], f"{location}.instruction", maximum=520
            ),
            "primary_layer": PRIMARY_LAYERS[index],
        }
        for field, namespace in selector_fields.items():
            selected = _list(
                state[field],
                f"{location}.{field}",
                minimum=0,
                maximum=len(id_sets[namespace]),
            )
            unknown = sorted(set(selected) - id_sets[namespace])
            if unknown:
                raise HeatVisualError(
                    f"{location}.{field} contains unknown IDs {unknown}"
                )
            normalized[field] = selected
            used[namespace].update(selected)
        expected_selectors = STATE_SELECTOR_INVARIANTS.get(state_id)
        if expected_selectors is not None:
            for field in selector_fields:
                expected = list(expected_selectors[field])
                if normalized[field] != expected:
                    raise HeatVisualError(
                        f"{location}.{field} must exactly match the "
                        f"{state_id} selector invariant {expected}"
                    )
        ids.append(state_id)
        nav_labels.append(normalized["nav_label"])
        states.append(normalized)
    if ids != STATE_IDS:
        raise HeatVisualError(
            f"pilot states must remain in canonical order {STATE_IDS}"
        )
    if len(nav_labels) != len(set(nav_labels)):
        raise HeatVisualError("pilot state nav labels must be unique")
    for namespace, expected in id_sets.items():
        if namespace == "energy":
            if used[namespace] != {"heat_obligation"}:
                raise HeatVisualError(
                    "Phase 6 states may retain only the heat-obligation accounting view"
                )
            continue
        if used[namespace] != expected:
            raise HeatVisualError(
                f"pilot states must use every authored {namespace} record"
            )
    if states[-1]["journey_stage_ids"] != JOURNEY_IDS or any(
        state["journey_stage_ids"] for state in states[:-1]
    ):
        raise HeatVisualError(
            "only the final state may reveal the complete six-phase journey"
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


def compile_heat_return(
    manifest: dict[str, Any],
    evidence_ledgers: Mapping[str, dict[str, Any]],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Validate and normalize the Phase 6 heat-rejection payload."""
    manifest = _exact(manifest, TOP_LEVEL_FIELDS, "pilot manifest")
    forbidden = base._forbidden_fields(manifest)
    if forbidden:
        raise HeatVisualError(
            f"pilot manifest contains pacing or scripting fields: {forbidden}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise HeatVisualError("pilot manifest schema_version must be 1")
    source_digest = base.validate_source_digest(source_digest)
    declared_ledgers, ledgers = base.validate_evidence_ledgers(
        manifest, evidence_ledgers
    )
    interaction = base.validate_manual_interaction(
        manifest["interaction"], location="pilot manifest.interaction"
    )
    phase = _exact(manifest["phase"], PHASE_FIELDS, "pilot manifest.phase")
    if type(phase["number"]) is not int or phase["number"] != 6:
        raise HeatVisualError("pilot manifest.phase.number must be integer 6")
    canvas = _exact(manifest["canvas"], CANVAS_FIELDS, "pilot manifest.canvas")
    if canvas["kind"] != CANVAS_KIND:
        raise HeatVisualError(f"pilot manifest.canvas.kind must be {CANVAS_KIND!r}")
    if canvas["width"] != CANVAS_WIDTH or canvas["height"] != CANVAS_HEIGHT:
        raise HeatVisualError(
            f"pilot manifest.canvas must be {CANVAS_WIDTH} by {CANVAS_HEIGHT}"
        )
    contract = _exact(
        canvas["contract"], CONTRACT_FIELDS, "pilot manifest.canvas.contract"
    )
    expected_contract = {
        "state_selection": "exclusive_single_primary_layer",
        "primary_layers": [
            "liquid_path",
            "residual_air_path",
            "facility_rejection",
            "abilene_mapping",
            "journey_closure",
        ],
        "evidence_binding": "content_record_fact_refs",
        "geometry_owner": "heat_return_renderer",
        "closure_requires": "journey_closure",
    }
    if contract != expected_contract:
        raise HeatVisualError(
            "pilot manifest.canvas.contract must match heat_return_v1"
        )
    energy = _normalize_energy(manifest["energy_handoff"], ledgers)
    liquid = _normalize_path(
        manifest["liquid_path"],
        location="pilot manifest.liquid_path",
        expected_ids=LIQUID_IDS,
        ledgers=ledgers,
        kind="liquid-stage",
    )
    air = _normalize_path(
        manifest["residual_air_path"],
        location="pilot manifest.residual_air_path",
        expected_ids=AIR_IDS,
        ledgers=ledgers,
        kind="air-stage",
    )
    facility = _normalize_facility(manifest["facility_rejection"], ledgers)
    mapping = _normalize_mapping(manifest["abilene_mapping"], ledgers)
    journey = _normalize_journey(manifest["journey_closure"], ledgers)
    gaps = _normalize_gaps(manifest["evidence_gaps"], ledgers)
    id_sets = {
        "energy": {item["id"] for item in energy["views"]},
        "liquid": {item["id"] for item in liquid["stages"]},
        "air": {item["id"] for item in air["stages"]},
        "facility": {item["id"] for item in facility["stages"]},
        "water": {item["id"] for item in facility["water_accounts"]},
        "known": {item["id"] for item in mapping["known"]},
        "unknown": {item["id"] for item in mapping["unknown"]},
        "journey": {item["id"] for item in journey["stages"]},
    }
    states = _normalize_states(manifest["states"], id_sets=id_sets)
    content = {
        "energy_handoff": energy,
        "liquid_path": liquid,
        "residual_air_path": air,
        "facility_rejection": facility,
        "abilene_mapping": mapping,
        "journey_closure": journey,
        "evidence_gaps": gaps,
    }
    evidence = base.compile_evidence_cards(
        _collect_refs(content), ledgers, ledger_ids=declared_ledgers
    )
    payload = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "pilot": {
            "id": _identifier(manifest["id"], "pilot manifest.id"),
            "title": _text(manifest["title"], "pilot manifest.title", maximum=150),
            "phase": {
                "id": _identifier(phase["id"], "pilot manifest.phase.id"),
                "number": 6,
                "title": _text(
                    phase["title"], "pilot manifest.phase.title", maximum=90
                ),
                "anchor_question": _text(
                    phase["anchor_question"],
                    "pilot manifest.phase.anchor_question",
                    maximum=220,
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
        raise HeatVisualError(
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


def _by_id(records: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {record["id"]: record for record in records}


def _mapping_summary(
    payload: Mapping[str, Any],
    state: Mapping[str, Any],
    *,
    y: int,
) -> str:
    mapping = payload["abilene_mapping"]
    known = _by_id(mapping["known"])
    unknown = _by_id(mapping["unknown"])
    known_titles = [known[item_id]["title"] for item_id in state["abilene_known_ids"]]
    unknown_titles = [
        unknown[item_id]["title"] for item_id in state["abilene_unknown_ids"]
    ]
    if not known_titles and not unknown_titles:
        return ""
    return (
        '<g class="mapping-summary">'
        f'<rect class="known-summary" x="90" y="{y}" width="700" height="86" rx="10"/>'
        f'<text class="mapping-kicker" x="116" y="{y + 28}">ABILENE EVIDENCE SUPPORTS</text>'
        + _wrapped(
            " · ".join(known_titles) if known_titles else "No selected site claim",
            x=116,
            y=y + 57,
            width_chars=74,
            line_height=18,
            css_class="mapping-copy",
            maximum_lines=2,
        )
        + f'<rect class="unknown-summary" x="810" y="{y}" width="700" height="86" rx="10"/>'
        f'<text class="mapping-kicker unknown-kicker" x="836" y="{y + 28}">PUBLIC EVIDENCE DOES NOT ESTABLISH</text>'
        + _wrapped(
            " · ".join(unknown_titles) if unknown_titles else "No additional unknown",
            x=836,
            y=y + 57,
            width_chars=74,
            line_height=18,
            css_class="mapping-copy",
            maximum_lines=2,
        )
        + "</g>"
    )


def _energy_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    record = payload["energy_handoff"]
    views = _by_id(record["views"])
    electrical = views["electrical_input"]
    compute = views["useful_compute_service"]
    heat = views["heat_obligation"]
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record['allocation_guard']))}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">TWO ACCOUNTING VIEWS · NOT TWO PIE SLICES</text>'
        + _wrapped(
            str(record["title"]),
            x=78,
            y=132,
            width_chars=84,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<rect class="energy-input-card" x="90" y="300" width="390" height="250" rx="18"/>'
        + '<path class="electric-bolt" d="M 238 340 L 190 435 H 250 L 220 520 L 330 402 H 270 L 305 340 Z"/>'
        + _wrapped(
            str(electrical["title"]),
            x=285,
            y=590,
            width_chars=34,
            line_height=22,
            css_class="energy-card-title centered",
            maximum_lines=2,
            center_lines=True,
        )
        + f'<text class="carrier-label centered" x="285" y="645">{_escape(electrical["carrier"])}</text>'
        + '<path class="service-arrow" d="M 480 390 C 610 390 610 280 735 280"/>'
        + '<path class="heat-arrow" d="M 480 470 C 610 470 610 610 735 610"/>'
        + '<rect class="view-card service-view" x="735" y="180" width="760" height="250" rx="18"/>'
        + '<text class="view-kicker" x="770" y="222">DESIRED SERVICE VIEW · NOT AN ENERGY FRACTION</text>'
        + f'<text class="view-title" x="770" y="272">{_escape(compute["title"])}</text>'
        + _wrapped(
            str(compute["carrier"]),
            x=770,
            y=315,
            width_chars=67,
            line_height=23,
            css_class="view-carrier",
            maximum_lines=2,
        )
        + '<g class="compute-pictogram"><rect x="1250" y="250" width="150" height="110" rx="12"/>'
        + '<path d="M 1275 278 H 1375 M 1275 306 H 1375 M 1275 334 H 1340"/>'
        + '<circle cx="1368" cy="334" r="9"/></g>'
        + '<rect class="view-card thermal-view" x="735" y="500" width="760" height="250" rx="18"/>'
        + '<text class="view-kicker heat-kicker" x="770" y="542">THERMAL OBLIGATION · NO UNIVERSAL PERCENTAGE</text>'
        + f'<text class="view-title" x="770" y="592">{_escape(heat["title"])}</text>'
        + _wrapped(
            str(heat["carrier"]),
            x=770,
            y=635,
            width_chars=67,
            line_height=23,
            css_class="view-carrier",
            maximum_lines=2,
        )
        + '<g class="heat-pictogram"><path d="M 1280 690 C 1245 650 1325 630 1285 590 M 1340 690 C 1305 650 1385 630 1345 590 M 1400 690 C 1365 650 1445 630 1405 590"/></g>'
        + '<rect class="guard-box" x="90" y="770" width="1405" height="65" rx="10"/>'
        + _wrapped(
            str(record["allocation_guard"]["body"]),
            x=120,
            y=800,
            width_chars=145,
            line_height=18,
            css_class="guard-copy",
            maximum_lines=2,
        )
        + "</g>"
    )


def _cold_plate_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    liquid = _by_id(payload["liquid_path"]["stages"])
    die = liquid["die_heat_source"]
    cold = liquid["cold_plate_heat_exchange"]
    accounting_guard = payload["energy_handoff"]["allocation_guard"]
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(die['boundary'])} {_escape(cold['boundary'])} {_escape(_fact_description(accounting_guard))}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">PHYSICAL INTERFACE · NO SITE OPERATING VALUES</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<g class="cold-plate-cutaway">'
        + '<rect class="board" x="150" y="630" width="900" height="54" rx="8"/>'
        + '<rect class="component-die" x="370" y="510" width="460" height="120" rx="10"/>'
        + '<path class="die-grid" d="M 420 540 H 780 M 420 570 H 780 M 420 600 H 780 M 500 520 V 620 M 600 520 V 620 M 700 520 V 620"/>'
        + '<rect class="thermal-interface" x="330" y="485" width="540" height="25" rx="5"/>'
        + '<rect class="cold-plate" x="300" y="300" width="600" height="185" rx="18"/>'
        + '<path class="coolant-channel" d="M 350 352 H 470 C 520 352 520 422 570 422 H 650 C 700 422 700 352 750 352 H 850"/>'
        + '<path class="coolant-supply" d="M 190 352 H 350"/>'
        + '<path class="coolant-return" d="M 850 352 H 1010"/>'
        + '<path class="component-heat" d="M 455 500 V 448 M 600 500 V 448 M 745 500 V 448"/>'
        + '<text class="cutaway-label" x="930" y="340">TCS SUPPLY</text>'
        + '<text class="cutaway-label" x="930" y="382">WARMED RETURN</text>'
        + f'<text class="cutaway-title centered" x="600" y="275">{_escape(cold["title"])}</text>'
        + f'<text class="cutaway-title centered" x="600" y="735">{_escape(die["title"])}</text>'
        + "</g>"
        + '<rect class="verb-card" x="1090" y="230" width="420" height="420" rx="16"/>'
        + '<text class="verb-kicker" x="1120" y="275">HEAT HANDOFF</text>'
        + _wrapped(
            str(die["verb"]),
            x=1120,
            y=322,
            width_chars=39,
            line_height=22,
            css_class="verb-copy",
            maximum_lines=3,
        )
        + '<path class="verb-arrow" d="M 1295 365 V 420"/>'
        + _wrapped(
            str(cold["verb"]),
            x=1120,
            y=468,
            width_chars=39,
            line_height=22,
            css_class="verb-copy",
            maximum_lines=3,
        )
        + '<rect class="guard-box" x="1120" y="535" width="360" height="105" rx="9"/>'
        + '<text class="guard-label" x="1140" y="562">ACCOUNTING BOUNDARY</text>'
        + _wrapped(
            str(accounting_guard["concise_boundary"]),
            x=1140,
            y=590,
            width_chars=39,
            line_height=18,
            css_class="guard-copy",
            maximum_lines=3,
        )
        + _mapping_summary(payload, state, y=742)
        + "</g>"
    )


def _rack_split_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    liquid = _by_id(payload["liquid_path"]["stages"])
    air = _by_id(payload["residual_air_path"]["stages"])
    heat = _by_id(payload["energy_handoff"]["views"])["heat_obligation"]
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(heat['boundary'])} {_escape(payload['residual_air_path']['body'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">ONE RACK · TWO THERMAL OBLIGATIONS · NO AUTHORED HEAT FRACTION</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<g class="rack-shell"><rect x="90" y="205" width="390" height="490" rx="18"/>'
        '<text class="lane-label" x="120" y="245">RACK EQUIPMENT BOUNDARY</text>'
        '<rect class="component-die" x="145" y="290" width="280" height="92" rx="10"/>'
        f'<text class="rack-split-title centered" x="285" y="345">{_escape(liquid["die_heat_source"]["title"])}</text>'
        '<rect class="cold-plate" x="145" y="405" width="280" height="92" rx="10"/>'
        f'<text class="rack-split-title centered" x="285" y="460">{_escape(liquid["cold_plate_heat_exchange"]["title"])}</text>'
        '<path class="component-heat" d="M 220 405 V 382 M 285 405 V 382 M 350 405 V 382"/>'
        '<rect class="air-aux-card" x="145" y="545" width="280" height="92" rx="10"/>'
        + _wrapped(
            str(air["air_cooled_auxiliaries"]["title"]),
            x=285,
            y=590,
            width_chars=28,
            line_height=19,
            css_class="rack-split-title centered",
            maximum_lines=2,
            center_lines=True,
        )
        + "</g>"
        '<path class="rack-liquid-branch" d="M 480 450 C 555 450 545 315 630 315"/>'
        '<path class="rack-air-branch" d="M 480 590 C 555 590 545 585 630 585"/>'
        '<rect class="parallel-lane liquid-lane" x="630" y="205" width="840" height="225" rx="16"/>'
        '<text class="lane-label" x="660" y="245">LIQUID BRANCH · COMPONENT → COLD PLATE → RACK MANIFOLD</text>'
        + _wrapped(
            " → ".join(
                liquid[item_id]["title"] for item_id in state["liquid_stage_ids"]
            ),
            x=1050,
            y=330,
            width_chars=72,
            line_height=23,
            css_class="parallel-path-copy centered",
            maximum_lines=3,
            center_lines=True,
        )
        + '<path class="liquid-heat-arrow" d="M 700 385 H 1400"/>'
        '<rect class="parallel-lane air-lane" x="630" y="475" width="840" height="225" rx="16"/>'
        '<text class="lane-label air-label" x="660" y="515">RESIDUAL-AIR BRANCH · AUXILIARIES → ROOM AIR</text>'
        + _wrapped(
            " → ".join(
                air[item_id]["title"] for item_id in state["residual_air_stage_ids"]
            ),
            x=1050,
            y=600,
            width_chars=72,
            line_height=23,
            css_class="parallel-path-copy centered",
            maximum_lines=3,
            center_lines=True,
        )
        + '<path class="air-flow-arrow" d="M 700 655 H 1400"/>'
        + _mapping_summary(payload, state, y=752)
        + "</g>"
    )


def _technology_loop_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    stages = _by_id(payload["liquid_path"]["stages"])
    order = state["liquid_stage_ids"]
    x_positions = [140, 610, 1080]
    if len(order) != len(x_positions):
        raise HeatVisualError(
            "technology_loop liquid_stage_ids must match its three desktop positions"
        )
    cards: list[str] = []
    for index, stage_id in enumerate(order):
        x = x_positions[index]
        stage = stages[stage_id]
        cards.append(
            f'<g class="loop-stage"><rect x="{x}" y="250" width="360" height="280" rx="16"/>'
            + _wrapped(
                str(stage["title"]),
                x=x + 180,
                y=310,
                width_chars=38,
                line_height=22,
                css_class="loop-stage-title centered",
                maximum_lines=2,
                center_lines=True,
            )
            + f'<circle class="loop-stage-icon" cx="{x + 180}" cy="400" r="48"/>'
            + f'<text class="loop-stage-number centered" x="{x + 180}" y="414">{index + 1}</text>'
            + _wrapped(
                str(stage["verb"]),
                x=x + 180,
                y=485,
                width_chars=40,
                line_height=18,
                css_class="loop-stage-verb centered",
                maximum_lines=3,
                center_lines=True,
            )
            + "</g>"
        )
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(payload['liquid_path']['body'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">TECHNOLOGY COOLING SYSTEM · SUPPLY AND RETURN ARE DISTINCT</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + "".join(cards)
        + '<path class="technology-supply" d="M 1360 585 H 320"/>'
        '<text class="loop-line-label" x="1080" y="575">COOLED SUPPLY · TOWARD COLD PLATES</text>'
        '<path class="technology-return" d="M 320 665 H 1360"/>'
        '<text class="loop-line-label" x="340" y="655">WARMED RETURN · HEAT MOVES TOWARD THE LOOP BOUNDARY</text>'
        '<rect class="guard-box" x="450" y="700" width="700" height="46" rx="10"/>'
        '<text class="convergence-label centered" x="800" y="729">NO SITE COOLANT · FLOW · PRESSURE · TEMPERATURE · SETPOINT</text>'
        + _mapping_summary(payload, state, y=758)
        + "</g>"
    )


def _cdu_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    stages = _by_id(payload["liquid_path"]["stages"])
    manifold = stages["rack_manifold_distribution"]
    technology = stages["technology_loop_return"]
    cdu = stages["conditional_cdu_boundary"]
    facility = stages["facility_loop_entry"]
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(cdu['boundary'])} {_escape(facility['boundary'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">CONDITIONAL LIQUID-TO-LIQUID BOUNDARY · HEAT CROSSES · COOLANTS DO NOT</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<rect class="loop-zone technology-zone" x="75" y="190" width="680" height="500" rx="18"/>'
        '<text class="zone-label" x="105" y="228">TECHNOLOGY COOLING SYSTEM · IT SIDE</text>'
        '<rect class="loop-zone facility-zone" x="845" y="190" width="680" height="500" rx="18"/>'
        '<text class="zone-label facility-label" x="875" y="228">FACILITY WATER SYSTEM · PLANT SIDE</text>'
        '<g class="cdu-side-stage"><rect x="125" y="300" width="250" height="230" rx="15"/>'
        + _wrapped(
            str(manifold["title"]),
            x=250,
            y=360,
            width_chars=27,
            line_height=22,
            css_class="loop-stage-title centered",
            maximum_lines=2,
            center_lines=True,
        )
        + _wrapped(
            str(technology["carrier"]),
            x=250,
            y=450,
            width_chars=27,
            line_height=19,
            css_class="loop-stage-verb centered",
            maximum_lines=3,
            center_lines=True,
        )
        + "</g>"
        '<g class="conditional-stage cdu-boundary"><rect x="635" y="260" width="330" height="340" rx="18"/>'
        '<text class="conditional-label centered" x="800" y="300">CONDITIONAL AT ABILENE</text>'
        + _wrapped(
            str(cdu["title"]),
            x=800,
            y=360,
            width_chars=34,
            line_height=23,
            css_class="loop-stage-title centered",
            maximum_lines=3,
            center_lines=True,
        )
        + '<path class="heat-exchanger" d="M 735 425 L 865 505 M 735 505 L 865 425"/>'
        '<text class="cdu-transfer-label centered" x="800" y="555">HEAT EXCHANGE · NO COOLANT MIXING</text>'
        "</g>"
        '<g class="cdu-side-stage facility-side"><rect x="1225" y="300" width="250" height="230" rx="15"/>'
        + _wrapped(
            str(facility["title"]),
            x=1350,
            y=360,
            width_chars=27,
            line_height=22,
            css_class="loop-stage-title centered",
            maximum_lines=2,
            center_lines=True,
        )
        + _wrapped(
            str(facility["carrier"]),
            x=1350,
            y=450,
            width_chars=27,
            line_height=19,
            css_class="loop-stage-verb centered",
            maximum_lines=3,
            center_lines=True,
        )
        + "</g>"
        '<path class="technology-return" d="M 375 390 H 635"/>'
        '<path class="facility-return" d="M 965 390 H 1225"/>'
        '<path class="technology-supply" d="M 635 540 H 375"/>'
        '<path class="facility-supply" d="M 1225 540 H 965"/>'
        '<text class="loop-line-label" x="415" y="380">WARMED TCS RETURN</text>'
        '<text class="loop-line-label" x="1000" y="380">HEAT TO FACILITY LOOP</text>'
        + _mapping_summary(payload, state, y=752)
        + "</g>"
    )


def _liquid_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    stages = _by_id(payload["liquid_path"]["stages"])
    order = state["liquid_stage_ids"]
    x_positions = [85, 335, 585, 875, 1175]
    if len(order) > len(x_positions):
        raise HeatVisualError("liquid path exceeds its desktop position inventory")
    cards = []
    for index, stage_id in enumerate(order):
        x = x_positions[index]
        stage = stages[stage_id]
        conditional = stage_id == "conditional_cdu_boundary"
        css_class = " conditional-stage" if conditional else ""
        if index:
            cards.append(
                f'<path class="heat-flow-arrow" d="M {x - 42} 420 H {x - 10}"/>'
            )
        cards.append(
            f'<g class="loop-stage{css_class}"><rect x="{x}" y="245" width="210" height="350" rx="15"/>'
            + (
                f'<text class="conditional-label" x="{x + 20}" y="278">CONDITIONAL AT ABILENE</text>'
                if conditional
                else ""
            )
            + _wrapped(
                str(stage["title"]),
                x=x + 105,
                y=330 if conditional else 295,
                width_chars=22,
                line_height=21,
                css_class="loop-stage-title centered",
                maximum_lines=3,
                center_lines=True,
            )
            + f'<circle class="loop-stage-icon" cx="{x + 105}" cy="410" r="46"/>'
            + (
                f'<text class="conditional-question centered" x="{x + 105}" y="425">?</text>'
                if conditional
                else f'<text class="loop-stage-number centered" x="{x + 105}" y="423">{index + 1}</text>'
            )
            + _wrapped(
                str(stage["verb"]),
                x=x + 105,
                y=515,
                width_chars=23,
                line_height=18,
                css_class="loop-stage-verb centered",
                maximum_lines=4,
                center_lines=True,
            )
            + "</g>"
        )
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(payload['liquid_path']['body'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">HEAT DIRECTION ACROSS TWO DISTINCT COOLANT LOOPS</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<rect class="loop-zone technology-zone" x="70" y="190" width="1000" height="465" rx="18"/>'
        + '<text class="zone-label" x="95" y="225">TECHNOLOGY COOLING SYSTEM · IT SIDE</text>'
        + '<rect class="loop-zone facility-zone" x="1090" y="190" width="440" height="465" rx="18"/>'
        + '<text class="zone-label facility-label" x="1115" y="225">FACILITY WATER SYSTEM · PLANT SIDE</text>'
        + "".join(cards)
        + '<path class="supply-return supply-line" d="M 1400 675 H 220"/>'
        + '<path class="supply-return return-line" d="M 220 710 H 1400"/>'
        + '<text class="loop-line-label" x="230" y="670">SUPPLY · FLOW DIRECTION GENERIC</text>'
        + '<text class="loop-line-label" x="1110" y="735">WARMED RETURN · HEAT MOVES TOWARD PLANT</text>'
        + _mapping_summary(payload, state, y=758)
        + "</g>"
    )


def _air_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    liquid = _by_id(payload["liquid_path"]["stages"])
    air = _by_id(payload["residual_air_path"]["stages"])
    liquid_titles = [liquid[item_id]["title"] for item_id in state["liquid_stage_ids"]]
    air_order = state["residual_air_stage_ids"]
    air_cards = []
    for index, stage_id in enumerate(air_order):
        stage = air[stage_id]
        x = 170 + index * 325
        conditional = "render_posture" in stage
        if index:
            air_cards.append(
                f'<path class="air-flow-arrow" d="M {x - 52} 575 H {x - 15}"/>'
            )
        air_cards.append(
            f'<g class="air-stage{" conditional-stage" if conditional else ""}"><rect x="{x}" y="475" width="260" height="190" rx="14"/>'
            + (
                f'<text class="conditional-label" x="{x + 18}" y="503">GENERIC · UNRESOLVED AT ABILENE</text>'
                if conditional
                else ""
            )
            + _wrapped(
                str(stage["title"]),
                x=x + 130,
                y=545 if conditional else 525,
                width_chars=28,
                line_height=20,
                css_class="air-stage-title centered",
                maximum_lines=3,
                center_lines=True,
            )
            + _wrapped(
                str(stage["verb"]),
                x=x + 130,
                y=620,
                width_chars=29,
                line_height=17,
                css_class="air-stage-verb centered",
                maximum_lines=3,
                center_lines=True,
            )
            + "</g>"
        )
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(payload['residual_air_path']['body'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">PARALLEL HEAT-REMOVAL OBLIGATIONS · NOT MIXED COOLANT</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<rect class="parallel-lane liquid-lane" x="95" y="195" width="1410" height="190" rx="16"/>'
        + '<text class="lane-label" x="125" y="230">LIQUID PATH · PROCESSORS / HIGH-POWER COMPONENTS</text>'
        + _wrapped(
            " → ".join(liquid_titles),
            x=800,
            y=300,
            width_chars=125,
            line_height=23,
            css_class="parallel-path-copy centered",
            maximum_lines=3,
            center_lines=True,
        )
        + '<path class="liquid-heat-arrow" d="M 180 350 H 1410"/>'
        + '<rect class="parallel-lane air-lane" x="95" y="430" width="1410" height="275" rx="16"/>'
        + '<text class="lane-label air-label" x="125" y="465">RESIDUAL AIR PATH · AUXILIARIES / ROOM AIR</text>'
        + "".join(air_cards)
        + '<rect class="convergence-box" x="515" y="712" width="570" height="45" rx="10"/>'
        + '<text class="convergence-label centered" x="800" y="741">HEAT ARROWS CONVERGE · FLUID CIRCUITS ARE NOT SHOWN MIXING</text>'
        + _mapping_summary(payload, state, y=766)
        + "</g>"
    )


def _facility_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    facility = payload["facility_rejection"]
    stages = _by_id(facility["stages"])
    accounts = _by_id(facility["water_accounts"])
    stage_order = state["facility_stage_ids"]
    stage_cards = []
    for index, stage_id in enumerate(stage_order):
        stage = stages[stage_id]
        x = 120 + index * 500
        if index:
            stage_cards.append(
                f'<path class="facility-arrow" d="M {x - 70} 300 H {x - 18}"/>'
            )
        icon = ""
        if stage_id == "facility_loop_transport":
            icon = f'<path class="loop-coil" d="M {x + 65} 340 C {x + 25} 300 {x + 205} 300 {x + 165} 340 C {x + 125} 380 {x + 305} 380 {x + 265} 340"/>'
        elif stage_id == "air_cooled_terminal":
            icon = "".join(
                f'<g class="fan"><circle cx="{x + 90 + n * 95}" cy="340" r="38"/><path d="M {x + 90 + n * 95} 310 V 370 M {x + 60 + n * 95} 340 H {x + 120 + n * 95}"/></g>'
                for n in range(3)
            )
        else:
            icon = f'<path class="atmosphere-waves" d="M {x + 80} 380 C {x + 20} 330 {x + 150} 300 {x + 90} 245 M {x + 180} 380 C {x + 120} 330 {x + 250} 300 {x + 190} 245 M {x + 280} 380 C {x + 220} 330 {x + 350} 300 {x + 290} 245"/>'
        stage_cards.append(
            f'<g class="facility-stage"><rect x="{x}" y="205" width="390" height="265" rx="16"/>'
            + _wrapped(
                str(stage["title"]),
                x=x + 195,
                y=255,
                width_chars=39,
                line_height=22,
                css_class="facility-stage-title centered",
                maximum_lines=2,
                center_lines=True,
            )
            + icon
            + _wrapped(
                str(stage["verb"]),
                x=x + 195,
                y=430,
                width_chars=40,
                line_height=18,
                css_class="facility-stage-verb centered",
                maximum_lines=3,
                center_lines=True,
            )
            + "</g>"
        )
    account_cards = []
    for index, account_id in enumerate(state["water_account_ids"]):
        account = accounts[account_id]
        x = 70 + index * 370
        unknown = account_id == "measured_operating_water"
        account_cards.append(
            f'<g class="water-account{" unknown-water" if unknown else ""}"><rect x="{x}" y="535" width="350" height="245" rx="14"/>'
            f'<text class="water-account-number" x="{x + 24}" y="570">0{index + 1}</text>'
            + _wrapped(
                str(account["title"]),
                x=x + 175,
                y=615,
                width_chars=34,
                line_height=20,
                css_class="water-account-title centered",
                maximum_lines=2,
                center_lines=True,
            )
            + _wrapped(
                str(account["display"]),
                x=x + 175,
                y=680,
                width_chars=36,
                line_height=19,
                css_class="water-account-display centered",
                maximum_lines=4,
                center_lines=True,
            )
            + _wrapped(
                str(account["boundary"]),
                x=x + 175,
                y=748,
                width_chars=39,
                line_height=16,
                css_class="water-account-boundary centered",
                maximum_lines=3,
                center_lines=True,
            )
            + "</g>"
        )
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(facility['body'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">SELECTED TERMINAL DESIGN · NOT OPERATING TELEMETRY</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + "".join(stage_cards)
        + '<text class="water-section-title" x="70" y="515">FOUR SEPARATE WATER ACCOUNTS · NO CONFLATION</text>'
        + "".join(account_cards)
        + "</g>"
    )


def _facility_rejection_svg(
    payload: Mapping[str, Any], state: Mapping[str, Any]
) -> str:
    facility = payload["facility_rejection"]
    stages = _by_id(facility["stages"])
    air = _by_id(payload["residual_air_path"]["stages"])
    air_handoff = air[state["residual_air_stage_ids"][0]]
    x_positions = [120, 605, 1090]
    stage_order = state["facility_stage_ids"]
    if len(stage_order) != len(x_positions):
        raise HeatVisualError(
            "facility_heat_rejection facility_stage_ids must match its three desktop positions"
        )
    cards: list[str] = []
    for index, stage_id in enumerate(stage_order):
        x = x_positions[index]
        stage = stages[stage_id]
        if index:
            cards.append(
                f'<path class="facility-arrow" d="M {x - 85} 420 H {x - 20}"/>'
            )
        if stage_id == "facility_loop_transport":
            icon = (
                f'<path class="loop-coil" d="M {x + 85} 405 C {x + 35} 355 '
                f"{x + 205} 355 {x + 155} 405 C {x + 105} 455 "
                f'{x + 275} 455 {x + 225} 405"/>'
            )
        elif stage_id == "air_cooled_terminal":
            icon = "".join(
                f'<g class="fan"><circle cx="{x + 95 + n * 92}" cy="410" r="38"/>'
                f'<path d="M {x + 95 + n * 92} 380 V 440 M {x + 65 + n * 92} 410 H {x + 125 + n * 92}"/></g>'
                for n in range(3)
            )
        else:
            icon = (
                f'<path class="atmosphere-waves" d="M {x + 95} 455 C {x + 35} 405 '
                f"{x + 165} 375 {x + 105} 320 M {x + 195} 455 C {x + 135} 405 "
                f"{x + 265} 375 {x + 205} 320 M {x + 295} 455 C {x + 235} 405 "
                f'{x + 365} 375 {x + 305} 320"/>'
            )
        cards.append(
            f'<g class="facility-stage"><rect x="{x}" y="235" width="390" height="390" rx="16"/>'
            + _wrapped(
                str(stage["title"]),
                x=x + 195,
                y=300,
                width_chars=39,
                line_height=23,
                css_class="facility-stage-title centered",
                maximum_lines=2,
                center_lines=True,
            )
            + icon
            + _wrapped(
                str(stage["verb"]),
                x=x + 195,
                y=555,
                width_chars=42,
                line_height=19,
                css_class="facility-stage-verb centered",
                maximum_lines=3,
                center_lines=True,
            )
            + f"<desc>{_escape(stage['boundary'])} {_escape(_fact_description(stage))}</desc></g>"
        )
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(facility['body'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">FACILITY HEAT PATH · SELECTED TERMINAL DESIGN · NOT OPERATING TELEMETRY</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<rect class="generic-handoff-box" x="120" y="185" width="1360" height="38" rx="9"/>'
        '<text class="generic-handoff-label centered" x="800" y="210">RESIDUAL-AIR → FACILITY-WATER / TERMINAL HANDOFF IS GENERIC AND CONDITIONAL · NOT AN ABILENE CONNECTION</text>'
        f"<desc>{_escape(air_handoff['boundary'])}</desc>"
        + '<path class="facility-heat-ribbon" d="M 185 420 H 1415"/>'
        + "".join(cards)
        + '<rect class="guard-box" x="300" y="680" width="1000" height="58" rx="10"/>'
        '<text class="convergence-label centered" x="800" y="716">DESIGN SELECTION ≠ INSTALLATION ≠ COMMISSIONING ≠ CURRENT OPERATION</text>'
        + _mapping_summary(payload, state, y=752)
        + "</g>"
    )


def _water_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    facility = payload["facility_rejection"]
    accounts = _by_id(facility["water_accounts"])
    cards: list[str] = []
    for index, account_id in enumerate(state["water_account_ids"]):
        account = accounts[account_id]
        x = 70 + index * 370
        unknown = account_id == "measured_operating_water"
        cards.append(
            f'<g class="water-account{" unknown-water" if unknown else ""}"><rect x="{x}" y="255" width="350" height="430" rx="16"/>'
            f'<text class="water-account-number" x="{x + 24}" y="292">0{index + 1}</text>'
            + _wrapped(
                str(account["title"]),
                x=x + 175,
                y=355,
                width_chars=34,
                line_height=22,
                css_class="water-account-title centered",
                maximum_lines=3,
                center_lines=True,
            )
            + _wrapped(
                str(account["display"]),
                x=x + 175,
                y=470,
                width_chars=36,
                line_height=20,
                css_class="water-account-display centered",
                maximum_lines=5,
                center_lines=True,
            )
            + '<line class="water-card-divider" '
            f'x1="{x + 30}" y1="535" x2="{x + 320}" y2="535"/>'
            + _wrapped(
                str(account["boundary"]),
                x=x + 175,
                y=585,
                width_chars=39,
                line_height=17,
                css_class="water-account-boundary centered",
                maximum_lines=5,
                center_lines=True,
            )
            + f"<desc>{_escape(_fact_description(account))}</desc></g>"
        )
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(facility['body'])}</desc>"
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">FOUR WATER ACCOUNTS · DIFFERENT BASES · NEVER SUBSTITUTE OR SUM</text>'
        + _wrapped(
            str(state["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<rect class="water-context" x="970" y="95" width="540" height="95" rx="12"/>'
        '<text class="mapping-kicker" x="995" y="128">SELECTED ABILENE TERMINAL</text>'
        '<text class="mapping-copy" x="995" y="160">Air-cooled chillers · no evaporative use in that process</text>'
        + "".join(cards)
        + '<rect class="guard-box" x="230" y="720" width="1140" height="90" rx="10"/>'
        '<text class="guard-label" x="260" y="752">ACCOUNTING GUARD</text>'
        + _wrapped(
            "Initial fill is not annual use. Anticipated maintenance is not measured consumption. Unknown is not zero. No campus total is inferred.",
            x=260,
            y=782,
            width_chars=115,
            line_height=18,
            css_class="guard-copy",
            maximum_lines=2,
        )
        + "</g>"
    )


def _journey_icon(stage_id: str, *, x: int, y: int) -> str:
    if stage_id == "generate":
        return f'<g class="journey-icon"><circle cx="{x}" cy="{y}" r="42"/><path d="M {x - 14} {y - 25} L {x + 5} {y - 4} L {x - 2} {y + 26} L {x + 20} {y - 2} L {x} {y - 2} Z"/></g>'
    if stage_id == "transmit":
        return f'<g class="journey-icon"><path d="M {x} {y - 48} L {x - 42} {y + 48} M {x} {y - 48} L {x + 42} {y + 48} M {x - 28} {y - 10} H {x + 28} M {x - 38} {y + 20} H {x + 38}"/></g>'
    if stage_id == "campus":
        return f'<g class="journey-icon"><path d="M {x - 55} {y + 38} V {y - 25} H {x - 10} V {y + 38} M {x + 5} {y + 38} V {y - 45} H {x + 55} V {y + 38}"/></g>'
    if stage_id == "building":
        return f'<g class="journey-icon"><rect x="{x - 55}" y="{y - 48}" width="110" height="96"/><path d="M {x - 30} {y - 20} H {x + 30} M {x - 30} {y + 5} H {x + 30} M {x - 30} {y + 30} H {x + 30}"/></g>'
    if stage_id == "compute":
        return f'<g class="journey-icon"><rect x="{x - 48}" y="{y - 48}" width="96" height="96" rx="8"/><path d="M {x - 25} {y - 22} H {x + 25} V {y + 22} H {x - 25} Z M {x - 62} {y - 25} H {x - 48} M {x - 62} {y} H {x - 48} M {x - 62} {y + 25} H {x - 48} M {x + 48} {y - 25} H {x + 62} M {x + 48} {y} H {x + 62} M {x + 48} {y + 25} H {x + 62}"/></g>'
    return f'<g class="journey-icon heat-closure-icon"><circle cx="{x}" cy="{y + 20}" r="42"/><path d="M {x - 45} {y - 5} C {x - 85} {y - 45} {x - 5} {y - 60} {x - 42} {y - 95} M {x} {y - 5} C {x - 40} {y - 45} {x + 40} {y - 60} {x + 3} {y - 95} M {x + 45} {y - 5} C {x + 5} {y - 45} {x + 85} {y - 60} {x + 48} {y - 95}"/></g>'


def _journey_svg(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    journey = payload["journey_closure"]
    cards = []
    for index, stage in enumerate(journey["stages"]):
        x = 52 + index * 255
        if index:
            cards.append(f'<path class="journey-arrow" d="M {x - 34} 430 H {x - 8}"/>')
        cards.append(
            f'<g class="journey-stage"><rect x="{x}" y="175" width="230" height="560" rx="16"/>'
            f'<circle class="journey-number" cx="{x + 34}" cy="215" r="22"/>'
            f'<text class="journey-number-label centered" x="{x + 34}" y="223">{stage["number"]}</text>'
            f'<text class="journey-title" x="{x + 68}" y="223">{_escape(stage["title"])}</text>'
            + _journey_icon(str(stage["id"]), x=x + 115, y=340)
            + '<text class="journey-section-label" '
            f'x="{x + 18}" y="462">CARRIER / FUNCTION</text>'
            + _wrapped(
                str(stage["carrier"]),
                x=x + 115,
                y=510,
                width_chars=24,
                line_height=18,
                css_class="journey-copy centered",
                maximum_lines=5,
                center_lines=True,
            )
            + '<text class="journey-section-label posture-label" '
            f'x="{x + 18}" y="595">ABILENE POSTURE</text>'
            + _wrapped(
                str(stage["abilene_posture"]),
                x=x + 115,
                y=655,
                width_chars=24,
                line_height=17,
                css_class="journey-posture centered",
                maximum_lines=6,
                center_lines=True,
            )
            + f"<desc>{_escape(_fact_description(stage))}</desc></g>"
        )
    return (
        f'<g data-heat-scene-id="{_escape(state["id"])}" hidden>'
        f"<title>{_escape(state['title'])}</title>"
        f"<desc>{_escape(journey['body'])} {_escape(_fact_description(journey['closure_guard']))}</desc>"
        '<rect class="journey-cover" x="0" y="0" width="1600" height="900"/>'
        '<rect class="heat-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="scene-kicker" x="78" y="88">FULL SIX-PHASE JOURNEY · CONCEPTUAL INDEX + EVIDENCE POSTURE</text>'
        + _wrapped(
            str(journey["title"]),
            x=78,
            y=132,
            width_chars=82,
            line_height=29,
            css_class="scene-title",
            maximum_lines=2,
        )
        + '<path class="journey-ribbon" d="M 95 430 H 1505"/>'
        + "".join(cards)
        + '<rect class="guard-box" x="100" y="770" width="1400" height="66" rx="10"/>'
        + _wrapped(
            str(journey["closure_guard"]["body"]),
            x=130,
            y=800,
            width_chars=145,
            line_height=18,
            css_class="guard-copy",
            maximum_lines=2,
        )
        + "</g>"
    )


def _responsive_mapping(
    payload: Mapping[str, Any],
    state: Mapping[str, Any],
) -> str:
    mapping = payload["abilene_mapping"]
    known = _by_id(mapping["known"])
    unknown = _by_id(mapping["unknown"])
    known_items = "".join(
        f"<li>{_escape(known[item_id]['title'])}</li>"
        for item_id in state["abilene_known_ids"]
    )
    unknown_items = "".join(
        f"<li>{_escape(unknown[item_id]['title'])}</li>"
        for item_id in state["abilene_unknown_ids"]
    )
    if not known_items and not unknown_items:
        return ""
    return (
        '<div class="responsive-mapping">'
        '<section class="mapping-known"><strong>Abilene evidence supports</strong>'
        f"<ul>{known_items or '<li>No selected site claim</li>'}</ul></section>"
        '<section class="mapping-unknown"><strong>Public evidence does not establish</strong>'
        f"<ul>{unknown_items or '<li>No additional unknown</li>'}</ul></section>"
        "</div>"
    )


def _responsive_flow_glyph(index: int, count: int) -> str:
    if index >= count - 1:
        return ""
    return (
        '<span class="responsive-flow-glyph" aria-hidden="true" '
        'data-flow-direction="forward">→</span>'
    )


def _responsive_inline_flow(titles: list[str]) -> str:
    items: list[str] = []
    for index, title in enumerate(titles):
        items.append(f'<span class="responsive-path-chip">{_escape(title)}</span>')
        if index < len(titles) - 1:
            items.append(
                '<b class="responsive-inline-arrow" aria-hidden="true" '
                'data-flow-direction="forward">→</b>'
            )
    return "".join(items)


def _responsive_energy(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    record = payload["energy_handoff"]
    views = _by_id(record["views"])
    return (
        f'<section class="responsive-scene responsive-energy" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Two accounting views · not two pie slices</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-energy-layout">'
        '<article class="responsive-energy-input"><span class="bolt" aria-hidden="true">ϟ</span>'
        f"<h3>{_escape(views['electrical_input']['title'])}</h3>"
        f"<p>{_escape(views['electrical_input']['carrier'])}</p></article>"
        '<div class="responsive-view-stack">'
        '<article class="responsive-view service"><strong>Desired service view · not an energy fraction</strong>'
        f"<h3>{_escape(views['useful_compute_service']['title'])}</h3>"
        f"<p>{_escape(views['useful_compute_service']['carrier'])}</p>"
        f"<small>{_escape(views['useful_compute_service']['boundary'])}</small></article>"
        '<article class="responsive-view thermal"><strong>Thermal obligation · no universal percentage</strong>'
        f"<h3>{_escape(views['heat_obligation']['title'])}</h3>"
        f"<p>{_escape(views['heat_obligation']['carrier'])}</p>"
        f"<small>{_escape(views['heat_obligation']['boundary'])}</small></article>"
        '</div></div><div class="responsive-guard">'
        f"{_escape(record['allocation_guard']['body'])}</div>"
        "</section>"
    )


def _responsive_cold_plate(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    stages = _by_id(payload["liquid_path"]["stages"])
    die = stages["die_heat_source"]
    cold = stages["cold_plate_heat_exchange"]
    accounting_guard = payload["energy_handoff"]["allocation_guard"]
    return (
        f'<section class="responsive-scene responsive-cold-plate" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Physical interface · no site operating values</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        '<div class="responsive-cutaway" role="img" '
        'aria-label="Component heat crosses a thermal interface into cold-plate coolant channels">'
        '<div class="responsive-coolant"><span>Technology coolant supply</span><i></i><span>Warmed return</span></div>'
        f'<div class="responsive-plate"><strong>{_escape(cold["title"])}</strong><span class="channel"></span></div>'
        '<b class="heat-up">↑ heat ↑</b>'
        f'<div class="responsive-die">{_escape(die["title"])}</div></div>'
        '<div class="responsive-verb-grid"><article><strong>1 · Heat source</strong>'
        f"<p>{_escape(die['verb'])}</p></article><article><strong>2 · Heat exchange</strong>"
        f"<p>{_escape(cold['verb'])}</p></article></div>"
        '<div class="responsive-guard"><strong>Accounting boundary</strong><br>'
        f"{_escape(accounting_guard['concise_boundary'])}"
        f'<span class="visually-hidden"> {_escape(_fact_description(accounting_guard))}</span></div>'
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_rack_split(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    liquid = _by_id(payload["liquid_path"]["stages"])
    air = _by_id(payload["residual_air_path"]["stages"])
    liquid_cards = _responsive_inline_flow(
        [liquid[item_id]["title"] for item_id in state["liquid_stage_ids"]]
    )
    air_cards = _responsive_inline_flow(
        [air[item_id]["title"] for item_id in state["residual_air_stage_ids"]]
    )
    return (
        f'<section class="responsive-scene responsive-rack-split" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">One rack · two thermal obligations · no authored heat fraction</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        '<div class="responsive-rack-branches">'
        '<article class="responsive-parallel-lane liquid"><strong>Liquid branch · high-power components</strong>'
        f"<div>{liquid_cards}</div></article>"
        '<article class="responsive-parallel-lane air"><strong>Residual-air branch · auxiliaries and room air</strong>'
        f"<div>{air_cards}</div></article></div>"
        '<div class="responsive-guard">Product component allocation does not establish a site heat split, airflow layout, or operating point.</div>'
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_technology_loop(
    payload: Mapping[str, Any], state: Mapping[str, Any]
) -> str:
    stages = _by_id(payload["liquid_path"]["stages"])
    order = state["liquid_stage_ids"]
    cards = "".join(
        '<article class="responsive-loop-stage">'
        f"<h3>{_escape(stages[item_id]['title'])}</h3>"
        f"<p>{_escape(stages[item_id]['verb'])}</p>"
        f"<small>{_escape(stages[item_id]['carrier'])}</small>"
        f"{_responsive_flow_glyph(index, len(order))}</article>"
        for index, item_id in enumerate(order)
    )
    return (
        f'<section class="responsive-scene responsive-technology-loop" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Technology Cooling System · two directional paths</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        f'<div class="responsive-stage-flow technology-stages">{cards}</div>'
        '<div class="responsive-supply-return"><span>← Cooled supply toward cold plates</span>'
        "<span>Warmed return / heat direction →</span></div>"
        '<div class="responsive-guard">No site coolant, flow, pressure, temperature, routing, or setpoint is authored.</div>'
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_cdu(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    stages = _by_id(payload["liquid_path"]["stages"])
    cdu = stages["conditional_cdu_boundary"]
    return (
        f'<section class="responsive-scene responsive-cdu" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Conditional liquid-to-liquid boundary</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        '<div class="responsive-cdu-zones">'
        '<article class="responsive-cdu-side"><strong>Technology Cooling System · IT side</strong>'
        f"<h3>{_escape(stages['rack_manifold_distribution']['title'])}</h3>"
        f"<p>{_escape(stages['technology_loop_return']['carrier'])}</p></article>"
        '<article class="responsive-cdu-boundary"><span class="conditional-chip">Conditional at Abilene</span>'
        f"<h3>{_escape(cdu['title'])}</h3><strong>Heat exchange · no coolant mixing</strong>"
        '<span class="responsive-transfer-glyph" aria-hidden="true" data-flow-direction="heat-transfer">⇢</span>'
        f"<p>{_escape(cdu['boundary'])}</p></article>"
        '<article class="responsive-cdu-side facility"><strong>Facility Water System · plant side</strong>'
        f"<h3>{_escape(stages['facility_loop_entry']['title'])}</h3>"
        f"<p>{_escape(stages['facility_loop_entry']['carrier'])}</p></article></div>"
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_liquid(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    stages = _by_id(payload["liquid_path"]["stages"])
    cards = "".join(
        '<article class="responsive-loop-stage'
        + (" conditional" if item_id == "conditional_cdu_boundary" else "")
        + '">'
        + (
            '<span class="conditional-chip">Conditional at Abilene</span>'
            if item_id == "conditional_cdu_boundary"
            else ""
        )
        + f"<h3>{_escape(stages[item_id]['title'])}</h3>"
        + f"<p>{_escape(stages[item_id]['verb'])}</p>"
        + f"<small>{_escape(stages[item_id]['carrier'])}</small></article>"
        for item_id in state["liquid_stage_ids"]
    )
    return (
        f'<section class="responsive-scene responsive-liquid" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Two distinct coolant loops</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        '<div class="responsive-loop-zones"><strong>Technology Cooling System · IT side</strong>'
        "<strong>Facility Water System · plant side</strong></div>"
        f'<div class="responsive-stage-flow">{cards}</div>'
        '<div class="responsive-supply-return"><span>← Generic supply direction</span>'
        "<span>Warmed return / heat direction →</span></div>"
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_air(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    liquid = _by_id(payload["liquid_path"]["stages"])
    air = _by_id(payload["residual_air_path"]["stages"])
    liquid_cards = _responsive_inline_flow(
        [liquid[item_id]["title"] for item_id in state["liquid_stage_ids"]]
    )
    air_order = state["residual_air_stage_ids"]
    air_cards = "".join(
        '<article class="responsive-air-stage'
        + (" conditional" if "render_posture" in air[item_id] else "")
        + '">'
        + (
            '<span class="conditional-chip">Generic · unresolved at Abilene</span>'
            if "render_posture" in air[item_id]
            else ""
        )
        + f"<h3>{_escape(air[item_id]['title'])}</h3>"
        + f"<p>{_escape(air[item_id]['verb'])}</p>"
        + f"<small>{_escape(air[item_id]['boundary'])}</small>"
        + _responsive_flow_glyph(index, len(air_order))
        + "</article>"
        for index, item_id in enumerate(air_order)
    )
    return (
        f'<section class="responsive-scene responsive-air" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Parallel heat-removal obligations</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        '<article class="responsive-parallel-lane liquid"><strong>Liquid path · processors / high-power components</strong>'
        f"<div>{liquid_cards}</div></article>"
        '<article class="responsive-parallel-lane air"><strong>Residual-air path · auxiliary components / room air</strong>'
        f'<div class="responsive-air-flow">{air_cards}</div></article>'
        '<div class="responsive-convergence">Heat arrows converge · fluid circuits are not shown mixing</div>'
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_facility(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    facility = payload["facility_rejection"]
    stages = _by_id(facility["stages"])
    accounts = _by_id(facility["water_accounts"])
    stage_cards = "".join(
        f'<article class="responsive-facility-stage"><span>0{index + 1}</span>'
        f"<h3>{_escape(stages[item_id]['title'])}</h3>"
        f"<p>{_escape(stages[item_id]['verb'])}</p>"
        f"<small>{_escape(stages[item_id]['boundary'])}</small></article>"
        for index, item_id in enumerate(state["facility_stage_ids"])
    )
    account_cards = "".join(
        '<article class="responsive-water-account'
        + (" unknown" if item_id == "measured_operating_water" else "")
        + f'"><span>0{index + 1}</span><h3>{_escape(accounts[item_id]["title"])}</h3>'
        + f"<strong>{_escape(accounts[item_id]['display'])}</strong>"
        + f"<p>{_escape(accounts[item_id]['boundary'])}</p></article>"
        for index, item_id in enumerate(state["water_account_ids"])
    )
    return (
        f'<section class="responsive-scene responsive-facility" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Selected terminal design · not telemetry</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        f'<div class="responsive-facility-flow">{stage_cards}</div>'
        '<h3 class="water-heading">Four separate water accounts · no conflation</h3>'
        f'<div class="responsive-water-grid">{account_cards}</div>'
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_facility_rejection(
    payload: Mapping[str, Any], state: Mapping[str, Any]
) -> str:
    facility = payload["facility_rejection"]
    stages = _by_id(facility["stages"])
    air = _by_id(payload["residual_air_path"]["stages"])
    air_handoff = air[state["residual_air_stage_ids"][0]]
    stage_order = state["facility_stage_ids"]
    stage_cards = "".join(
        f'<article class="responsive-facility-stage"><span>0{index + 1}</span>'
        f"<h3>{_escape(stages[item_id]['title'])}</h3>"
        f"<p>{_escape(stages[item_id]['verb'])}</p>"
        f"<small>{_escape(stages[item_id]['boundary'])}</small>"
        f"{_responsive_flow_glyph(index, len(stage_order))}</article>"
        for index, item_id in enumerate(stage_order)
    )
    return (
        f'<section class="responsive-scene responsive-facility-rejection" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Facility heat path · selected terminal design · not telemetry</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        '<div class="responsive-generic-handoff"><span class="conditional-chip">Generic conditional handoff · not an Abilene connection</span>'
        f"<strong>{_escape(air_handoff['title'])}</strong>"
        f"<p>{_escape(air_handoff['boundary'])}</p></div>"
        f'<div class="responsive-facility-flow">{stage_cards}</div>'
        '<div class="responsive-guard">Design selection is not installation, commissioning, or current operation.</div>'
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _responsive_water(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    facility = payload["facility_rejection"]
    accounts = _by_id(facility["water_accounts"])
    cards = "".join(
        '<article class="responsive-water-account'
        + (" unknown" if item_id == "measured_operating_water" else "")
        + f'"><span>0{index + 1}</span><h3>{_escape(accounts[item_id]["title"])}</h3>'
        + f"<strong>{_escape(accounts[item_id]['display'])}</strong>"
        + f"<p>{_escape(accounts[item_id]['boundary'])}</p></article>"
        for index, item_id in enumerate(state["water_account_ids"])
    )
    return (
        f'<section class="responsive-scene responsive-water-accounting" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Four water accounts · different bases · no substitution</p>'
        f"<h2>{_escape(state['title'])}</h2>"
        '<div class="responsive-water-context"><strong>Selected Abilene terminal</strong>'
        "<p>Air-cooled chillers; no evaporative use in that heat-rejection process.</p></div>"
        f'<div class="responsive-water-grid">{cards}</div>'
        '<div class="responsive-guard">Initial fill is not annual use. Anticipated maintenance is not measured consumption. Unknown is not zero. No campus total is inferred.</div>'
        + _responsive_mapping(payload, state)
        + "</section>"
    )


def _journey_icon_text(stage_id: str) -> str:
    return {
        "generate": "ϟ",
        "transmit": "⌁",
        "campus": "▦",
        "building": "▤",
        "compute": "▣",
        "reject_heat": "≋",
    }[stage_id]


def _responsive_journey(payload: Mapping[str, Any], state: Mapping[str, Any]) -> str:
    journey = payload["journey_closure"]
    stages = journey["stages"]
    cards = "".join(
        f'<article class="responsive-journey-stage"><span class="journey-icon-text">{_journey_icon_text(str(stage["id"]))}</span>'
        f"<b>{stage['number']}</b><h3>{_escape(stage['title'])}</h3>"
        "<strong>Carrier / function</strong>"
        f"<p>{_escape(stage['carrier'])}</p><strong>Abilene posture</strong>"
        f"<p>{_escape(stage['abilene_posture'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(stage))}</span>'
        f"{_responsive_flow_glyph(index, len(stages))}</article>"
        for index, stage in enumerate(stages)
    )
    return (
        f'<section class="responsive-scene responsive-journey" data-heat-scene-id="{_escape(state["id"])}" hidden>'
        '<p class="responsive-kicker">Full six-phase journey · conceptual index + evidence posture</p>'
        f"<h2>{_escape(journey['title'])}</h2>"
        f'<p class="journey-intro">{_escape(journey["body"])}</p>'
        f'<div class="responsive-journey-grid">{cards}</div>'
        '<div class="responsive-guard">'
        f"{_escape(journey['closure_guard']['body'])}</div></section>"
    )


def _responsive_visual(payload: Mapping[str, Any]) -> str:
    states = {state["id"]: state for state in payload["states"]}
    return (
        '<section class="responsive-visual" aria-label="Responsive heat-rejection teaching surface">'
        + _responsive_journey(payload, states["whole_journey_closure"])
        + _responsive_rack_split(payload, states["rack_cooling_split"])
        + _responsive_technology_loop(payload, states["technology_loop"])
        + _responsive_cdu(payload, states["cdu_boundary"])
        + _responsive_air(payload, states["parallel_residual_air"])
        + _responsive_facility_rejection(payload, states["facility_heat_rejection"])
        + _responsive_water(payload, states["water_accounting"])
        + "</section>"
    )


def render_heat_return(payload: dict[str, Any]) -> str:
    """Render one compiled Phase 6 pilot as a self-contained HTML page."""
    if payload.get("canvas", {}).get("kind") != CANVAS_KIND:
        raise HeatVisualError("render payload is not a heat-return surface")
    _validate_compiled_state_selectors(
        payload.get("states"), location="render payload.states"
    )
    states = {state["id"]: state for state in payload["states"]}
    buttons = "".join(
        f'<button class="state-button" type="button" '
        f'id="state-selector-{_escape(state["id"])}" aria-pressed="false" '
        f'aria-label="State {index + 1}: {_escape(state["title"])}" '
        f'title="{_escape(state["title"])}" '
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
  :root {{ --paper:#fafaf7; --ink:#1a1a1a; --muted:#5f5f59; --faint:#d4d4cd; --blue:#175d8d; --blue-soft:#eaf3f8; --cyan:#158ca0; --cyan-soft:#e8f7f9; --green:#2f9e8f; --green-soft:#e9f7f4; --amber:#b76e18; --amber-soft:#fff7ed; --red:#b3261e; --red-soft:#fceceb; }}
  * {{ box-sizing:border-box; }}
  [hidden] {{ display:none !important; }}
  html,body {{ width:100%; height:100%; min-height:0; margin:0; background:var(--paper); color:var(--ink); font-family:Inter,"Helvetica Neue",Arial,sans-serif; }}
  html {{ overflow:hidden; }}
  body {{ display:grid; grid-template-rows:auto minmax(0,1fr) auto; height:100dvh; min-height:0; overflow:hidden; }}
  header {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(330px,590px); gap:20px; padding:11px 20px 10px; border-bottom:1.5px solid var(--ink); }}
  .eyebrow,.phase-question,.state-number,.scene-kicker,.responsive-kicker,.fact-ref,.view-kicker,.verb-kicker,.mapping-kicker,.conditional-label,.zone-label,.lane-label,.water-section-title,.journey-section-label,.responsive-view strong,.responsive-mapping strong,.conditional-chip {{ text-transform:uppercase; letter-spacing:.07em; font-size:13px; font-weight:760; }}
  h1 {{ margin:3px 0; font-size:clamp(21px,2.2vw,34px); line-height:1.05; }}
  header p {{ margin:2px 0; line-height:1.3; }}
  .objective {{ align-self:end; color:var(--muted); font-size:13px; }}
  main {{ min-width:0; min-height:0; display:grid; place-items:center; overflow:hidden; padding:8px 14px; }}
  .visual-shell {{ width:100%; height:100%; min-width:0; min-height:0; max-width:1600px; max-height:900px; border:1.5px solid var(--ink); background:white; }}
  svg {{ display:block; width:100%; height:100%; }}
  .centered {{ text-anchor:middle; }}
  .heat-panel {{ fill:white; stroke:var(--ink); stroke-width:2; }}
  .journey-cover {{ fill:white; }}
  .scene-kicker {{ fill:var(--blue); font-size:13px; }}
  .scene-title {{ font-size:27px; font-weight:770; }}
  .energy-input-card,.view-card,.verb-card,.loop-stage > rect,.air-stage > rect,.facility-stage > rect,.water-account > rect,.journey-stage > rect {{ fill:white; stroke:var(--ink); stroke-width:2; }}
  .electric-bolt {{ fill:var(--blue); }}
  .energy-card-title,.view-title,.cutaway-title,.loop-stage-title,.air-stage-title,.facility-stage-title,.water-account-title,.journey-title {{ font-weight:760; }}
  .energy-card-title {{ font-size:20px; }}
  .carrier-label {{ fill:var(--muted); font-size:13px; }}
  .arrowhead-blue {{ fill:var(--blue); }}
  .arrowhead-cyan {{ fill:var(--cyan); }}
  .arrowhead-amber {{ fill:var(--amber); }}
  .arrowhead-red {{ fill:var(--red); }}
  .service-arrow {{ fill:none; stroke:var(--blue); stroke-width:5; marker-end:url(#arrow-blue); }}
  .heat-arrow {{ fill:none; stroke:var(--red); stroke-width:5; marker-end:url(#arrow-red); }}
  .service-view {{ fill:var(--blue-soft); stroke:var(--blue); }}
  .thermal-view {{ fill:var(--red-soft); stroke:var(--red); }}
  .view-kicker {{ fill:var(--blue); }}
  .heat-kicker {{ fill:var(--red); }}
  .view-title {{ font-size:23px; }}
  .view-carrier {{ fill:var(--muted); font-size:16px; }}
  .compute-pictogram rect {{ fill:white; stroke:var(--blue); stroke-width:2; }}
  .compute-pictogram path {{ fill:none; stroke:var(--blue); stroke-width:3; }}
  .compute-pictogram circle {{ fill:var(--green); }}
  .heat-pictogram path {{ fill:none; stroke:var(--red); stroke-width:6; }}
  .guard-box {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.6; }}
  .guard-copy {{ fill:var(--muted); font-size:13px; }}
  .guard-label {{ fill:var(--amber); font-size:13px; font-weight:760; }}
  .board {{ fill:#d9d9d4; stroke:var(--ink); stroke-width:2; }}
  .component-die {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:3; }}
  .die-grid {{ fill:none; stroke:var(--blue); stroke-width:2; opacity:.55; }}
  .thermal-interface {{ fill:var(--amber); }}
  .cold-plate {{ fill:var(--cyan-soft); stroke:var(--cyan); stroke-width:3; }}
  .coolant-channel,.coolant-supply,.coolant-return {{ fill:none; stroke:var(--cyan); stroke-width:12; }}
  .coolant-return {{ stroke:var(--red); }}
  .component-heat {{ fill:none; stroke:var(--red); stroke-width:5; marker-end:url(#arrow-red); }}
  .cutaway-label {{ fill:var(--muted); font-size:13px; font-weight:700; }}
  .cutaway-title {{ font-size:19px; }}
  .rack-shell > rect {{ fill:#f8f8f5; stroke:var(--ink); stroke-width:2; }}
  .air-aux-card {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:2; }}
  .rack-split-title {{ font-size:16px; font-weight:760; }}
  .rack-liquid-branch {{ fill:none; stroke:var(--cyan); stroke-width:5; marker-end:url(#arrow-cyan); }}
  .rack-air-branch {{ fill:none; stroke:var(--amber); stroke-width:5; marker-end:url(#arrow-amber); }}
  .verb-kicker {{ fill:var(--blue); }}
  .verb-copy {{ font-size:17px; font-weight:700; }}
  .verb-arrow {{ fill:none; stroke:var(--red); stroke-width:4; marker-end:url(#arrow-red); }}
  .known-summary {{ fill:var(--green-soft); stroke:var(--green); stroke-width:1.6; }}
  .unknown-summary {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.6; }}
  .mapping-kicker {{ fill:var(--green); }}
  .unknown-kicker {{ fill:var(--amber); }}
  .mapping-copy {{ fill:var(--muted); font-size:13px; }}
  .loop-zone {{ fill:#f8fcfd; stroke:var(--cyan); stroke-width:2; }}
  .facility-zone {{ fill:#f7faf5; stroke:var(--green); }}
  .zone-label {{ fill:var(--cyan); }}
  .facility-label {{ fill:var(--green); }}
  .loop-stage > rect {{ fill:white; stroke:var(--cyan); }}
  .conditional-stage > rect {{ fill:var(--amber-soft); stroke:var(--amber); stroke-dasharray:8 6; }}
  .conditional-label {{ fill:var(--amber); }}
  .loop-stage-title {{ font-size:17px; }}
  .loop-stage-icon {{ fill:var(--cyan-soft); stroke:var(--cyan); stroke-width:2; }}
  .loop-stage-number,.conditional-question {{ fill:var(--cyan); font-size:29px; font-weight:800; }}
  .conditional-question {{ fill:var(--amber); }}
  .loop-stage-verb {{ fill:var(--muted); font-size:13px; }}
  .heat-flow-arrow,.air-flow-arrow,.facility-arrow,.journey-arrow {{ fill:none; stroke:var(--red); stroke-width:4; marker-end:url(#arrow-red); }}
  .supply-return {{ fill:none; stroke-width:4; }}
  .supply-line {{ stroke:var(--cyan); marker-end:url(#arrow-cyan); }}
  .return-line {{ stroke:var(--red); marker-end:url(#arrow-red); }}
  .technology-supply,.facility-supply {{ fill:none; stroke:var(--cyan); stroke-width:6; marker-end:url(#arrow-cyan); }}
  .technology-return,.facility-return {{ fill:none; stroke:var(--red); stroke-width:6; marker-end:url(#arrow-red); }}
  .loop-line-label {{ fill:var(--muted); font-size:13px; font-weight:700; }}
  .cdu-side-stage > rect {{ fill:white; stroke:var(--cyan); stroke-width:2; }}
  .facility-side > rect {{ stroke:var(--green); }}
  .heat-exchanger {{ fill:none; stroke:var(--amber); stroke-width:12; }}
  .cdu-transfer-label {{ fill:var(--amber); font-size:13px; font-weight:760; }}
  .parallel-lane {{ fill:#f8fcfd; stroke:var(--cyan); stroke-width:2; }}
  .air-lane {{ fill:#fffaf5; stroke:var(--amber); }}
  .lane-label {{ fill:var(--cyan); }}
  .air-label {{ fill:var(--amber); }}
  .parallel-path-copy {{ fill:var(--muted); font-size:16px; font-weight:700; }}
  .liquid-heat-arrow {{ fill:none; stroke:var(--red); stroke-width:5; marker-end:url(#arrow-red); }}
  .air-stage > rect {{ stroke:var(--amber); }}
  .air-stage-title {{ font-size:16px; }}
  .air-stage-verb {{ fill:var(--muted); font-size:13px; }}
  .convergence-box {{ fill:var(--ink); }}
  .convergence-label {{ fill:white; font-size:13px; font-weight:740; }}
  .facility-stage > rect {{ stroke:var(--green); }}
  .facility-stage-title {{ font-size:19px; }}
  .facility-stage-verb {{ fill:var(--muted); font-size:13px; }}
  .loop-coil {{ fill:none; stroke:var(--green); stroke-width:10; }}
  .fan circle {{ fill:var(--green-soft); stroke:var(--green); stroke-width:2; }}
  .fan path {{ fill:none; stroke:var(--green); stroke-width:3; }}
  .atmosphere-waves {{ fill:none; stroke:var(--red); stroke-width:6; }}
  .facility-heat-ribbon {{ fill:none; stroke:var(--red); stroke-width:8; marker-end:url(#arrow-red); }}
  .generic-handoff-box {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.6; stroke-dasharray:7 5; }}
  .generic-handoff-label {{ fill:var(--amber); font-size:13px; font-weight:760; }}
  .water-section-title {{ fill:var(--blue); }}
  .water-account > rect {{ fill:var(--blue-soft); stroke:var(--blue); }}
  .unknown-water > rect {{ fill:var(--amber-soft); stroke:var(--amber); }}
  .water-account-number {{ fill:var(--blue); font-size:13px; font-weight:760; }}
  .unknown-water .water-account-number {{ fill:var(--amber); }}
  .water-account-title {{ font-size:17px; }}
  .water-account-display {{ font-size:14px; font-weight:720; }}
  .water-account-boundary {{ fill:var(--muted); font-size:13px; }}
  .water-card-divider {{ stroke:var(--faint); stroke-width:1.5; }}
  .water-context {{ fill:var(--green-soft); stroke:var(--green); stroke-width:1.6; }}
  .journey-ribbon {{ fill:none; stroke:var(--blue); stroke-width:10; marker-end:url(#arrow-blue); }}
  .journey-stage > rect {{ fill:white; stroke:var(--blue); }}
  .journey-stage:last-of-type > rect {{ fill:var(--red-soft); stroke:var(--red); }}
  .journey-number {{ fill:var(--blue); }}
  .journey-number-label {{ fill:white; font-size:16px; font-weight:800; }}
  .journey-title {{ font-size:18px; }}
  .journey-icon circle,.journey-icon rect {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:3; }}
  .journey-icon path {{ fill:none; stroke:var(--blue); stroke-width:4; }}
  .heat-closure-icon circle {{ fill:var(--red-soft); stroke:var(--red); }}
  .heat-closure-icon path {{ stroke:var(--red); }}
  .journey-section-label {{ fill:var(--blue); }}
  .posture-label {{ fill:var(--amber); }}
  .journey-copy {{ font-size:13px; font-weight:680; }}
  .journey-posture {{ fill:var(--muted); font-size:13px; }}
  footer {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(340px,590px); gap:10px 16px; min-height:0; max-height:48dvh; padding:9px 14px 10px; border-top:1.5px solid var(--ink); }}
  .state-nav {{ display:grid; grid-template-columns:repeat({len(payload["states"])},minmax(0,1fr)); gap:6px; }}
  .state-button {{ display:grid; grid-template-columns:auto 1fr; gap:7px; align-items:center; min-width:0; min-height:44px; padding:7px 8px; border:1.5px solid var(--ink); background:transparent; color:inherit; text-align:left; font:inherit; cursor:pointer; }}
  .state-nav-label {{ overflow:visible; text-overflow:clip; white-space:normal; }}
  .state-button[aria-pressed="true"] {{ background:var(--ink); color:white; }}
  .state-copy {{ min-width:0; align-self:center; }}
  .state-copy h2 {{ margin:0 0 3px; font-size:16px; }}
  .state-copy p {{ margin:0; color:var(--muted); font-size:13px; line-height:1.3; }}
  details {{ grid-column:1/-1; min-width:0; min-height:0; border-top:1px solid var(--faint); padding-top:6px; }}
  details[open] {{ max-height:min(34dvh,320px); overflow:auto; overflow-x:hidden; overscroll-behavior:contain; }}
  summary {{ position:sticky; top:0; z-index:2; cursor:pointer; padding:3px 0; background:var(--paper); font-weight:700; }}
  .fact-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr)); gap:12px; min-width:0; margin-bottom:0; padding:0; list-style:none; }}
  .fact-card {{ min-width:0; border:1px solid var(--faint); padding:10px 12px; background:white; }}
  .fact-card p {{ margin:5px 0; line-height:1.35; }}
  .fact-ref,.fact-boundary {{ overflow-wrap:anywhere; word-break:break-word; color:var(--muted); font-size:13px; }}
  .fact-sources {{ min-width:0; overflow-wrap:anywhere; word-break:break-word; font-size:13px; }}
  a {{ overflow-wrap:anywhere; word-break:break-word; color:var(--blue); }}
  .visually-hidden {{ position:absolute !important; width:1px; height:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }}
  .responsive-visual {{ display:none; }}
  .responsive-scene {{ min-width:0; border:1.5px solid var(--ink); border-radius:10px; background:white; }}
  .responsive-scene h2,.responsive-scene h3,.responsive-scene p,.responsive-scene ul {{ margin:0; }}
  .responsive-kicker,.conditional-chip {{ color:var(--blue); text-transform:uppercase; letter-spacing:.06em; font-weight:760; }}
  .responsive-energy-layout {{ display:grid; grid-template-columns:minmax(180px,.7fr) minmax(0,1.5fr); }}
  .responsive-energy-input,.responsive-view,.responsive-verb-grid article,.responsive-loop-stage,.responsive-air-stage,.responsive-facility-stage,.responsive-water-account,.responsive-journey-stage {{ position:relative; min-width:0; border:1px solid var(--faint); border-radius:8px; background:var(--paper); }}
  .responsive-energy-input {{ display:grid; place-items:center; text-align:center; }}
  .bolt {{ color:var(--blue); font-size:48px; }}
  .responsive-view-stack {{ display:grid; }}
  .responsive-view.service {{ border-color:var(--blue); background:var(--blue-soft); }}
  .responsive-view.thermal {{ border-color:var(--red); background:var(--red-soft); }}
  .responsive-view.thermal > strong {{ color:var(--red); }}
  .responsive-view small,.responsive-facility-stage small {{ display:block; color:var(--muted); }}
  .responsive-guard {{ border:1px solid var(--amber); border-radius:8px; background:var(--amber-soft); color:var(--muted); }}
  .responsive-cutaway {{ display:grid; place-items:center; }}
  .responsive-coolant {{ display:flex; justify-content:space-between; width:100%; color:var(--cyan); font-weight:700; }}
  .responsive-coolant i {{ flex:1; margin:0 8px; border-top:6px solid var(--cyan); }}
  .responsive-plate {{ display:grid; place-items:center; width:min(560px,90%); border:2px solid var(--cyan); border-radius:10px; background:var(--cyan-soft); }}
  .channel {{ width:75%; border-top:8px solid var(--cyan); border-radius:50%; }}
  .heat-up {{ color:var(--red); }}
  .responsive-die {{ width:min(440px,75%); border:2px solid var(--blue); border-radius:8px; background:var(--blue-soft); text-align:center; font-weight:730; }}
  .responsive-verb-grid,.responsive-mapping,.responsive-loop-zones,.responsive-stage-flow,.responsive-air-flow,.responsive-facility-flow,.responsive-water-grid,.responsive-journey-grid {{ display:grid; }}
  .responsive-verb-grid,.responsive-mapping,.responsive-loop-zones {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
  .mapping-known,.mapping-unknown {{ min-width:0; border:1px solid var(--green); border-radius:8px; background:var(--green-soft); }}
  .mapping-unknown {{ border-color:var(--amber); background:var(--amber-soft); }}
  .mapping-known strong {{ color:var(--green); }}
  .mapping-unknown strong {{ color:var(--amber); }}
  .responsive-stage-flow {{ grid-template-columns:repeat(5,minmax(0,1fr)); }}
  .responsive-stage-flow.technology-stages {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
  .responsive-loop-zones strong {{ border:1px solid var(--cyan); border-radius:7px; background:var(--cyan-soft); text-align:center; }}
  .responsive-loop-zones strong:last-child {{ border-color:var(--green); background:var(--green-soft); }}
  .responsive-loop-stage {{ border-color:var(--cyan); }}
  .responsive-loop-stage.conditional,.responsive-air-stage.conditional {{ border-color:var(--amber); border-style:dashed; background:var(--amber-soft); }}
  .responsive-rack-branches,.responsive-cdu-zones {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:8px; }}
  .responsive-cdu-zones {{ grid-template-columns:minmax(0,1fr) minmax(0,1.2fr) minmax(0,1fr); }}
  .responsive-cdu-side,.responsive-cdu-boundary,.responsive-water-context {{ position:relative; min-width:0; padding:9px; border:1px solid var(--cyan); border-radius:8px; background:var(--cyan-soft); }}
  .responsive-cdu-side.facility,.responsive-water-context {{ border-color:var(--green); background:var(--green-soft); }}
  .responsive-cdu-boundary {{ border-color:var(--amber); border-style:dashed; background:var(--amber-soft); }}
  .conditional-chip {{ display:block; color:var(--amber); }}
  .responsive-transfer-glyph {{ display:block; margin:7px 0; color:var(--red); font-size:28px; font-weight:800; text-align:center; }}
  .responsive-supply-return {{ display:flex; justify-content:space-between; color:var(--muted); font-weight:700; }}
  .responsive-parallel-lane {{ border:1px solid var(--cyan); border-radius:8px; background:var(--cyan-soft); }}
  .responsive-parallel-lane.air {{ border-color:var(--amber); background:var(--amber-soft); }}
  .responsive-parallel-lane > div {{ display:flex; flex-wrap:wrap; align-items:center; }}
  .responsive-path-chip {{ border:1px solid currentColor; border-radius:999px; }}
  .responsive-inline-arrow,.responsive-flow-glyph {{ color:var(--red); font-size:20px; font-weight:850; line-height:1; }}
  .responsive-flow-glyph {{ display:block; margin-top:7px; text-align:right; }}
  .responsive-air-flow {{ grid-template-columns:repeat(4,minmax(0,1fr)); }}
  .responsive-convergence {{ border-radius:8px; background:var(--ink); color:white; text-align:center; font-weight:720; }}
  .responsive-facility-flow {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
  .responsive-water-grid {{ grid-template-columns:repeat(4,minmax(0,1fr)); }}
  .responsive-facility-stage {{ border-color:var(--green); }}
  .responsive-generic-handoff {{ margin-top:9px; padding:9px; border:1px dashed var(--amber); border-radius:8px; background:var(--amber-soft); }}
  .responsive-generic-handoff strong {{ display:block; margin:4px 0; }}
  .responsive-facility-stage > span,.responsive-water-account > span {{ color:var(--blue); font-weight:760; }}
  .responsive-water-account {{ border-color:var(--blue); background:var(--blue-soft); }}
  .responsive-water-account.unknown {{ border-color:var(--amber); background:var(--amber-soft); }}
  .responsive-water-account.unknown > span {{ color:var(--amber); }}
  .water-heading {{ color:var(--blue); text-transform:uppercase; letter-spacing:.05em; }}
  .journey-intro {{ color:var(--muted); }}
  .responsive-journey-grid {{ grid-template-columns:repeat(6,minmax(0,1fr)); }}
  .responsive-journey-stage {{ border-color:var(--blue); }}
  .responsive-journey-stage:last-child {{ border-color:var(--red); background:var(--red-soft); }}
  .journey-icon-text {{ display:grid; place-items:center; color:var(--blue); font-size:38px; }}
  .responsive-journey-stage:last-child .journey-icon-text {{ color:var(--red); }}
  .responsive-journey-stage > b {{ display:grid; place-items:center; width:28px; height:28px; border-radius:50%; background:var(--blue); color:white; }}
  .responsive-journey-stage > strong {{ display:block; color:var(--blue); text-transform:uppercase; letter-spacing:.05em; font-size:12px; }}
  @media (max-width:1280px), (max-height:760px) {{
    header {{ grid-template-columns:minmax(0,1fr) minmax(300px,520px); gap:10px; padding:7px 12px; }}
    h1 {{ font-size:22px; }}
    .objective {{ font-size:12px; }}
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:6px; }}
    footer {{ padding:6px 9px 7px; }}
    .state-nav {{ gap:4px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; padding:4px; text-align:center; font-size:12px; }}
    .visual-shell {{ display:none; }}
    .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:4px; font-size:12px; }}
    .responsive-scene {{ padding:11px; }}
    .responsive-scene h2 {{ margin-bottom:8px; font-size:19px; }}
    .responsive-scene h3 {{ margin-bottom:5px; font-size:15px; }}
    .responsive-kicker {{ margin-bottom:4px !important; font-size:12px; }}
    .responsive-energy-layout,.responsive-view-stack,.responsive-verb-grid,.responsive-mapping,.responsive-loop-zones,.responsive-stage-flow,.responsive-air-flow,.responsive-facility-flow,.responsive-water-grid,.responsive-journey-grid {{ gap:8px; }}
    .responsive-energy-input,.responsive-view,.responsive-verb-grid article,.responsive-loop-stage,.responsive-air-stage,.responsive-facility-stage,.responsive-water-account,.responsive-journey-stage,.mapping-known,.mapping-unknown {{ padding:8px; font-size:12px; line-height:1.4; }}
    .responsive-guard,.responsive-mapping,.responsive-cutaway,.responsive-verb-grid,.responsive-loop-zones,.responsive-stage-flow,.responsive-supply-return,.responsive-parallel-lane,.responsive-rack-branches,.responsive-cdu-zones,.responsive-water-context,.responsive-convergence,.responsive-facility-flow,.water-heading,.responsive-water-grid,.journey-intro,.responsive-journey-grid {{ margin-top:9px; }}
    .responsive-guard,.responsive-parallel-lane,.responsive-convergence {{ padding:8px; font-size:12px; line-height:1.4; }}
    .responsive-view-stack {{ gap:8px; }}
    .responsive-view small,.responsive-loop-stage small,.responsive-air-stage small,.responsive-facility-stage small {{ display:block; margin-top:5px; font-size:12px; line-height:1.35; color:var(--muted); }}
    .responsive-cutaway {{ gap:7px; padding:10px; }}
    .responsive-plate,.responsive-die {{ padding:12px; }}
    .responsive-verb-grid article {{ border-color:var(--faint); }}
    .mapping-known,.mapping-unknown {{ padding:8px; }}
    .mapping-known ul,.mapping-unknown ul {{ padding-left:18px; }}
    .responsive-loop-zones strong {{ padding:7px; }}
    .responsive-loop-stage small {{ display:block; margin-top:5px; color:var(--muted); }}
    .responsive-supply-return {{ padding:7px; }}
    .responsive-parallel-lane > div {{ gap:5px; margin-top:6px; }}
    .responsive-path-chip {{ padding:4px 6px; }}
    .responsive-air-stage p,.responsive-facility-stage p,.responsive-water-account p,.responsive-journey-stage p {{ font-size:12px; line-height:1.4; }}
    .responsive-convergence {{ margin-bottom:9px; }}
    .water-heading {{ font-size:13px; }}
    .responsive-journey-stage {{ position:relative; }}
    .responsive-journey-stage > b {{ position:absolute; top:8px; right:8px; }}
  }}
  @media (max-width:1100px) {{
    header {{ grid-template-columns:1fr; gap:2px; }}
    footer {{ grid-template-columns:1fr; gap:4px; }}
    .responsive-stage-flow {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
    .responsive-stage-flow.technology-stages {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
    .responsive-loop-stage:last-child {{ grid-column:1/-1; }}
    .responsive-air-flow,.responsive-water-grid,.responsive-journey-grid {{ grid-template-columns:repeat(2,minmax(0,1fr)); }}
    .responsive-facility-flow {{ grid-template-columns:repeat(3,minmax(0,1fr)); }}
    details[open] {{ position:fixed; inset:10px; z-index:10; max-height:none; padding:10px; overflow:auto; overflow-x:hidden; border:1.5px solid var(--ink); background:var(--paper); }}
  }}
  @media (max-height:520px) and (orientation:landscape) {{
    header {{ grid-template-columns:1fr; padding:3px 8px; }}
    h1 {{ margin:1px 0; font-size:17px; }}
    .eyebrow,.phase-question {{ font-size:10px; }}
    .objective {{ display:none; }}
    main {{ padding:3px 6px; }}
    footer {{ grid-template-columns:minmax(0,1fr) minmax(210px,320px) auto; gap:5px; padding:3px 6px; }}
    .state-button {{ grid-template-columns:1fr; gap:0; min-height:34px; padding:2px 3px; text-align:center; font-size:10px; }}
    .state-copy h2 {{ font-size:11px; }}
    .state-copy p {{ display:none; }}
    details {{ grid-column:auto; align-self:center; border-top:0; padding-top:0; font-size:10px; }}
    .evidence-count {{ display:none; }}
    .responsive-visual {{ padding:2px; font-size:10px; }}
    .responsive-scene {{ padding:7px; }}
    .responsive-scene h2 {{ margin-bottom:4px; font-size:14px; }}
    .responsive-scene h3 {{ margin-bottom:3px; font-size:12px; }}
    .responsive-energy-layout {{ grid-template-columns:140px 1fr; }}
    .responsive-stage-flow,.responsive-air-flow,.responsive-water-grid,.responsive-journey-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); gap:5px; }}
    .responsive-loop-stage:last-child {{ grid-column:auto; }}
    .responsive-energy-input,.responsive-view,.responsive-verb-grid article,.responsive-loop-stage,.responsive-air-stage,.responsive-facility-stage,.responsive-water-account,.responsive-journey-stage,.mapping-known,.mapping-unknown {{ padding:5px; font-size:10px; }}
    .responsive-view small,.responsive-loop-stage small,.responsive-air-stage small,.responsive-facility-stage small {{ font-size:10px; }}
    .journey-icon-text {{ font-size:28px; }}
  }}
  @media (max-width:520px) and (orientation:portrait) {{
    header {{ padding:6px 8px; }}
    h1 {{ font-size:19px; }}
    .objective {{ display:none; }}
    footer {{ grid-template-columns:1fr; gap:4px; padding:5px 7px; }}
    .state-button {{ min-height:44px; padding:3px 2px; font-size:12px; }}
    .state-number {{ font-size:12px; }}
    .state-copy h2 {{ font-size:13px; }}
    .state-copy p {{ display:none; }}
    .responsive-visual {{ padding:2px; font-size:12px; }}
    .responsive-scene {{ padding:9px; }}
    .responsive-energy-layout,.responsive-verb-grid,.responsive-mapping,.responsive-loop-zones,.responsive-stage-flow,.responsive-stage-flow.technology-stages,.responsive-rack-branches,.responsive-cdu-zones,.responsive-air-flow,.responsive-facility-flow,.responsive-water-grid,.responsive-journey-grid {{ grid-template-columns:1fr; }}
    .responsive-loop-stage:last-child {{ grid-column:auto; }}
    .responsive-supply-return {{ display:grid; gap:4px; }}
    .responsive-coolant {{ display:grid; gap:5px; text-align:center; }}
    .responsive-coolant i {{ min-height:6px; }}
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
  <section class="visual-shell" aria-label="Instructor-controlled heat-rejection teaching surface">
    <svg id="visual" role="img" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" aria-labelledby="visual-title visual-description">
      <defs>
        <marker id="arrow-blue" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path class="arrowhead-blue" d="M 0 0 L 10 5 L 0 10 z"/></marker>
        <marker id="arrow-cyan" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path class="arrowhead-cyan" d="M 0 0 L 10 5 L 0 10 z"/></marker>
        <marker id="arrow-amber" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path class="arrowhead-amber" d="M 0 0 L 10 5 L 0 10 z"/></marker>
        <marker id="arrow-red" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="4" markerHeight="4" orient="auto"><path class="arrowhead-red" d="M 0 0 L 10 5 L 0 10 z"/></marker>
      </defs>
      <title id="visual-title">Heat return from silicon to atmosphere</title>
      <desc id="visual-description">Seven manually selected causal views separate the rack heat split, technology loop, conditional CDU boundary, residual-air branch, facility heat rejection, water accounting, and complete six-phase journey.</desc>
      {_rack_split_svg(payload, states["rack_cooling_split"])}
      {_technology_loop_svg(payload, states["technology_loop"])}
      {_cdu_svg(payload, states["cdu_boundary"])}
      {_air_svg(payload, states["parallel_residual_air"])}
      {_facility_rejection_svg(payload, states["facility_heat_rejection"])}
      {_water_svg(payload, states["water_accounting"])}
      {_journey_svg(payload, states["whole_journey_closure"])}
    </svg>
  </section>
  {responsive}
</main>
<footer>
  <nav class="state-nav" aria-label="Manual Phase 6 teaching-state selectors">{buttons}</nav>
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
  document.querySelectorAll("[data-heat-scene-id]").forEach(element => {{
    element.toggleAttribute("hidden", element.dataset.heatSceneId !== state.id);
  }});
  buttons.forEach((button, buttonIndex) => {{
    const selected = buttonIndex === current;
    button.setAttribute("aria-pressed", String(selected));
    if (selected) button.setAttribute("aria-current", "step");
    else button.removeAttribute("aria-current");
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
