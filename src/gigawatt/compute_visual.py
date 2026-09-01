"""Evidence-bound Phase 5 rack-to-compute teaching surface.

This compiler deliberately accepts one narrow manifest.  It keeps product
documentation, generic electrical mechanisms, and Abilene operating evidence
separate while exposing six coarse, instructor-selected teaching states.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from gigawatt import teaching_visuals as base

SCHEMA_VERSION = 1
CANVAS_KIND = "compute_power_descent_v1"
CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 900

STATE_IDS = [
    "orient_inside_rack",
    "facility_ac_to_rack_dc",
    "board_point_of_load",
    "useful_compute_and_upstream_demand",
    "abilene_compute_boundary",
    "heat_carrier_handoff",
]
ORIENTATION_LAYER_IDS = ["data_hall_boundary", "rack_envelope", "board_and_die"]
RACK_CONVERSION_STEP_IDS = ["facility_ac_input", "rack_power_shelf", "rack_dc_bus"]
POINT_OF_LOAD_STEP_IDS = [
    "intermediate_bus",
    "multiphase_vrm",
    "processor_rails",
    "active_processor",
]
FORWARD_ALLOCATION_IDS = [
    "facility_power",
    "it_power",
    "accelerator_power",
    "active_compute",
    "useful_output",
]
UPSTREAM_DEMAND_IDS = ["synchronized_work", "aggregation_path", "grid_facing_load"]
ABILENE_KNOWN_IDS = ["platform_family", "rack_delivery", "live_compute"]
ABILENE_UNKNOWN_IDS = [
    "rack_and_rail_configuration",
    "power_allocation",
    "workload_and_output",
    "site_demand_waveform",
]
HANDOFF_CARRIER_IDS = [
    "useful_compute_output",
    "processor_heat",
    "liquid_and_air_split",
]
GAP_IDS = [
    "abilene_internal_rack_power_path",
    "abilene_power_to_useful_compute_measurement",
    "abilene_correlated_demand_trace",
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
    "rack_orientation",
    "rack_power_conversion",
    "processor_point_of_load",
    "compute_demand_loop",
    "abilene_mapping",
    "phase6_handoff",
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
ORIENTATION_FIELDS = SECTION_FIELDS | {"layers", "orientation_boundary"}
ORIENTATION_LAYER_FIELDS = {"id", "title", "contains", "carrier", "fact_refs"}
ORIENTATION_LAYER_BOUNDARY_FIELDS = ORIENTATION_LAYER_FIELDS | {"boundary"}
POWER_CONVERSION_FIELDS = SECTION_FIELDS | {"steps", "conversion_boundary"}
POWER_STEP_FIELDS = {"id", "title", "verb", "value_posture", "fact_refs"}
POWER_STEP_BOUNDARY_FIELDS = POWER_STEP_FIELDS | {"boundary"}
POINT_OF_LOAD_FIELDS = SECTION_FIELDS | {"steps", "point_of_load_boundary"}
DEMAND_LOOP_FIELDS = SECTION_FIELDS | {
    "forward_allocation",
    "upstream_demand",
    "demand_boundary",
}
CARD_FIELDS = {"id", "title", "body", "fact_refs"}
BOUNDARY_FIELDS = {"id", "body", "fact_refs"}
TITLED_BOUNDARY_FIELDS = CARD_FIELDS
FORWARD_FIELDS = {"id", "title", "boundary", "fact_refs"}
UPSTREAM_FIELDS = CARD_FIELDS
ABILENE_FIELDS = {"title", "known", "unknown", "mapping_guard"}
HANDOFF_FIELDS = SECTION_FIELDS | {"carriers"}
HANDOFF_CARRIER_FIELDS = {"id", "title", "carrier", "boundary", "fact_refs"}
GAP_FIELDS = {"id", "gap", "renderer_guard", "related_fact_refs"}
STATE_FIELDS = {
    "id",
    "nav_label",
    "title",
    "instruction",
    "orientation_layer_ids",
    "rack_conversion_step_ids",
    "point_of_load_step_ids",
    "show_compute_demand_loop",
    "abilene_known_ids",
    "abilene_unknown_ids",
    "show_phase6_handoff",
}


class ComputeVisualError(base.TeachingVisualError):
    """Raised when Phase 5 escapes its teaching or evidence contract."""


def responsive_layout_contract(
    viewport_width: int,
    viewport_height: int,
) -> dict[str, Any]:
    """Choose the desktop SVG or the payload-derived readable HTML surface."""
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
        raise ComputeVisualError(str(error)) from error


def _text(value: Any, location: str, *, maximum: int = 240) -> str:
    try:
        return base._text(value, location, maximum=maximum)
    except base.TeachingVisualError as error:
        raise ComputeVisualError(str(error)) from error


def _identifier(value: Any, location: str) -> str:
    try:
        return base._id(value, location)
    except base.TeachingVisualError as error:
        raise ComputeVisualError(str(error)) from error


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
        raise ComputeVisualError(str(error)) from error


def _refs(
    value: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[str]:
    try:
        return base._fact_refs(value, location, ledgers)
    except base.TeachingVisualError as error:
        raise ComputeVisualError(str(error)) from error


def _record(
    raw: Any,
    fields: set[str],
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
    *,
    list_fields: set[str] | None = None,
    identifier_fields: set[str] | None = None,
) -> dict[str, Any]:
    value = _exact(raw, fields, location)
    list_fields = list_fields or set()
    identifier_fields = identifier_fields or set()
    normalized: dict[str, Any] = {}
    for key in value:
        item_location = f"{location}.{key}"
        if key == "id":
            normalized[key] = _identifier(value[key], item_location)
        elif key in {"fact_refs", "related_fact_refs"}:
            normalized[key] = _refs(value[key], item_location, ledgers)
        elif key in list_fields:
            normalized[key] = _list(
                value[key], item_location, minimum=1, maximum=8, item_limit=180
            )
        elif key in identifier_fields:
            normalized[key] = _identifier(value[key], item_location)
        else:
            normalized[key] = _text(value[key], item_location, maximum=1000)
    return normalized


def _records(
    raw: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
    *,
    expected_ids: list[str],
    fields: set[str] | None = None,
    fields_by_id: Mapping[str, set[str]] | None = None,
    list_fields: set[str] | None = None,
    identifier_fields: set[str] | None = None,
) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(expected_ids):
        raise ComputeVisualError(
            f"{location} must contain exactly {len(expected_ids)} records"
        )
    normalized = []
    for index, raw_record in enumerate(raw):
        record_location = f"{location}[{index}]"
        record_id = raw_record.get("id") if isinstance(raw_record, dict) else None
        record_fields = fields_by_id.get(record_id) if fields_by_id else fields
        if record_fields is None:
            raise ComputeVisualError(f"{record_location}: unknown record ID")
        normalized.append(
            _record(
                raw_record,
                record_fields,
                record_location,
                ledgers,
                list_fields=list_fields,
                identifier_fields=identifier_fields,
            )
        )
    ids = [record["id"] for record in normalized]
    if ids != expected_ids:
        raise ComputeVisualError(
            f"{location} must remain in canonical order {expected_ids}"
        )
    return normalized


def _heading(value: Mapping[str, Any], location: str) -> dict[str, str]:
    return {
        "title": _text(value["title"], f"{location}.title", maximum=180),
        "body": _text(value["body"], f"{location}.body", maximum=1000),
    }


def _normalize_orientation(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.rack_orientation"
    value = _exact(raw, ORIENTATION_FIELDS, location)
    fields_by_id = {
        "data_hall_boundary": ORIENTATION_LAYER_FIELDS,
        "rack_envelope": ORIENTATION_LAYER_BOUNDARY_FIELDS,
        "board_and_die": ORIENTATION_LAYER_BOUNDARY_FIELDS,
    }
    layers = _records(
        value["layers"],
        f"{location}.layers",
        ledgers,
        expected_ids=ORIENTATION_LAYER_IDS,
        fields_by_id=fields_by_id,
        list_fields={"contains"},
    )
    boundary = _record(
        value["orientation_boundary"],
        TITLED_BOUNDARY_FIELDS,
        f"{location}.orientation_boundary",
        ledgers,
    )
    return {**_heading(value, location), "layers": layers, "boundary": boundary}


def _normalize_conversion(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.rack_power_conversion"
    value = _exact(raw, POWER_CONVERSION_FIELDS, location)
    fields_by_id = {
        "facility_ac_input": POWER_STEP_BOUNDARY_FIELDS,
        "rack_power_shelf": POWER_STEP_FIELDS,
        "rack_dc_bus": POWER_STEP_FIELDS,
    }
    steps = _records(
        value["steps"],
        f"{location}.steps",
        ledgers,
        expected_ids=RACK_CONVERSION_STEP_IDS,
        fields_by_id=fields_by_id,
        identifier_fields={"value_posture"},
    )
    boundary = _record(
        value["conversion_boundary"],
        BOUNDARY_FIELDS,
        f"{location}.conversion_boundary",
        ledgers,
    )
    return {**_heading(value, location), "steps": steps, "boundary": boundary}


def _normalize_point_of_load(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.processor_point_of_load"
    value = _exact(raw, POINT_OF_LOAD_FIELDS, location)
    fields_by_id = {
        "intermediate_bus": POWER_STEP_FIELDS,
        "multiphase_vrm": POWER_STEP_FIELDS,
        "processor_rails": POWER_STEP_FIELDS,
        "active_processor": POWER_STEP_BOUNDARY_FIELDS,
    }
    steps = _records(
        value["steps"],
        f"{location}.steps",
        ledgers,
        expected_ids=POINT_OF_LOAD_STEP_IDS,
        fields_by_id=fields_by_id,
        identifier_fields={"value_posture"},
    )
    boundary = _record(
        value["point_of_load_boundary"],
        BOUNDARY_FIELDS,
        f"{location}.point_of_load_boundary",
        ledgers,
    )
    return {**_heading(value, location), "steps": steps, "boundary": boundary}


def _normalize_demand_loop(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.compute_demand_loop"
    value = _exact(raw, DEMAND_LOOP_FIELDS, location)
    forward = _records(
        value["forward_allocation"],
        f"{location}.forward_allocation",
        ledgers,
        expected_ids=FORWARD_ALLOCATION_IDS,
        fields=FORWARD_FIELDS,
    )
    upstream = _records(
        value["upstream_demand"],
        f"{location}.upstream_demand",
        ledgers,
        expected_ids=UPSTREAM_DEMAND_IDS,
        fields=UPSTREAM_FIELDS,
    )
    boundary = _record(
        value["demand_boundary"],
        BOUNDARY_FIELDS,
        f"{location}.demand_boundary",
        ledgers,
    )
    return {
        **_heading(value, location),
        "forward_allocation": forward,
        "upstream_demand": upstream,
        "boundary": boundary,
    }


def _normalize_abilene(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.abilene_mapping"
    value = _exact(raw, ABILENE_FIELDS, location)
    known = _records(
        value["known"],
        f"{location}.known",
        ledgers,
        expected_ids=ABILENE_KNOWN_IDS,
        fields=CARD_FIELDS,
    )
    unknown = _records(
        value["unknown"],
        f"{location}.unknown",
        ledgers,
        expected_ids=ABILENE_UNKNOWN_IDS,
        fields=CARD_FIELDS,
    )
    guard = _record(
        value["mapping_guard"],
        BOUNDARY_FIELDS,
        f"{location}.mapping_guard",
        ledgers,
    )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=180),
        "known": known,
        "unknown": unknown,
        "guard": guard,
    }


def _normalize_handoff(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.phase6_handoff"
    value = _exact(raw, HANDOFF_FIELDS, location)
    carriers = _records(
        value["carriers"],
        f"{location}.carriers",
        ledgers,
        expected_ids=HANDOFF_CARRIER_IDS,
        fields=HANDOFF_CARRIER_FIELDS,
    )
    return {**_heading(value, location), "carriers": carriers}


def _normalize_gaps(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    return _records(
        raw,
        "pilot manifest.evidence_gaps",
        ledgers,
        expected_ids=GAP_IDS,
        fields=GAP_FIELDS,
    )


def _state_ids(value: Any, location: str, allowed: list[str]) -> list[str]:
    selected = _list(
        value,
        location,
        minimum=0,
        maximum=len(allowed),
        item_limit=80,
    )
    unknown = sorted(set(selected) - set(allowed))
    if unknown:
        raise ComputeVisualError(f"{location}: unknown IDs {unknown}")
    return selected


def _normalize_states(raw: Any) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(STATE_IDS):
        raise ComputeVisualError("pilot manifest.states must contain six states")
    states: list[dict[str, Any]] = []
    nav_labels: list[str] = []
    for index, raw_state in enumerate(raw):
        location = f"pilot manifest.states[{index}]"
        value = _exact(raw_state, STATE_FIELDS, location)
        selected = {
            "orientation_layer_ids": _state_ids(
                value["orientation_layer_ids"],
                f"{location}.orientation_layer_ids",
                ORIENTATION_LAYER_IDS,
            ),
            "rack_conversion_step_ids": _state_ids(
                value["rack_conversion_step_ids"],
                f"{location}.rack_conversion_step_ids",
                RACK_CONVERSION_STEP_IDS,
            ),
            "point_of_load_step_ids": _state_ids(
                value["point_of_load_step_ids"],
                f"{location}.point_of_load_step_ids",
                POINT_OF_LOAD_STEP_IDS,
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
        for flag in ("show_compute_demand_loop", "show_phase6_handoff"):
            if not isinstance(value[flag], bool):
                raise ComputeVisualError(f"{location}.{flag} must be boolean")
        state = {
            "id": _identifier(value["id"], f"{location}.id"),
            "nav_label": _text(value["nav_label"], f"{location}.nav_label", maximum=28),
            "title": _text(value["title"], f"{location}.title", maximum=180),
            "instruction": _text(
                value["instruction"], f"{location}.instruction", maximum=620
            ),
            **selected,
            "show_compute_demand_loop": value["show_compute_demand_loop"],
            "show_phase6_handoff": value["show_phase6_handoff"],
        }
        states.append(state)
        nav_labels.append(state["nav_label"])
    if [state["id"] for state in states] != STATE_IDS:
        raise ComputeVisualError(
            f"pilot manifest states must remain in canonical order {STATE_IDS}"
        )
    if len(nav_labels) != len(set(nav_labels)):
        raise ComputeVisualError("pilot manifest state nav labels must be unique")

    expected = [
        (ORIENTATION_LAYER_IDS, [], [], False, [], [], False),
        (["rack_envelope"], RACK_CONVERSION_STEP_IDS, [], False, [], [], False),
        (
            ["board_and_die"],
            ["rack_dc_bus"],
            POINT_OF_LOAD_STEP_IDS,
            False,
            [],
            [],
            False,
        ),
        ([], [], ["active_processor"], True, [], [], False),
        (
            ["rack_envelope", "board_and_die"],
            RACK_CONVERSION_STEP_IDS,
            ["multiphase_vrm", "processor_rails", "active_processor"],
            False,
            ABILENE_KNOWN_IDS,
            ABILENE_UNKNOWN_IDS,
            False,
        ),
        (
            ["board_and_die"],
            [],
            ["active_processor"],
            False,
            ["platform_family", "live_compute"],
            ["rack_and_rail_configuration"],
            True,
        ),
    ]
    for state, canonical in zip(states, expected, strict=True):
        actual = (
            state["orientation_layer_ids"],
            state["rack_conversion_step_ids"],
            state["point_of_load_step_ids"],
            state["show_compute_demand_loop"],
            state["abilene_known_ids"],
            state["abilene_unknown_ids"],
            state["show_phase6_handoff"],
        )
        if actual != canonical:
            raise ComputeVisualError(
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


def compile_compute_power_descent(
    manifest: dict[str, Any],
    evidence_ledgers: Mapping[str, dict[str, Any]],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Validate and normalize the Phase 5 teaching payload."""
    manifest = _exact(manifest, TOP_LEVEL_FIELDS, "pilot manifest")
    forbidden = base._forbidden_fields(manifest)
    if forbidden:
        raise ComputeVisualError(
            f"pilot manifest contains pacing or scripting fields: {forbidden}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise ComputeVisualError("pilot manifest schema_version must be 1")
    try:
        source_digest = base.validate_source_digest(source_digest)
        declared_ledgers, ledgers = base.validate_evidence_ledgers(
            manifest, evidence_ledgers
        )
    except base.TeachingVisualError as error:
        raise ComputeVisualError(str(error)) from error

    phase = _exact(manifest["phase"], PHASE_FIELDS, "pilot manifest.phase")
    if type(phase["number"]) is not int or phase["number"] != 5:
        raise ComputeVisualError("pilot manifest.phase.number must be integer 5")
    try:
        interaction = base.validate_manual_interaction(
            manifest["interaction"], location="pilot manifest.interaction"
        )
    except base.TeachingVisualError as error:
        raise ComputeVisualError(str(error)) from error

    canvas = _exact(manifest["canvas"], CANVAS_FIELDS, "pilot manifest.canvas")
    if canvas["kind"] != CANVAS_KIND:
        raise ComputeVisualError(f"pilot manifest.canvas.kind must be {CANVAS_KIND!r}")
    if canvas["width"] != CANVAS_WIDTH or canvas["height"] != CANVAS_HEIGHT:
        raise ComputeVisualError(
            f"pilot manifest.canvas must be {CANVAS_WIDTH} by {CANVAS_HEIGHT}"
        )
    contract = _exact(
        canvas["contract"], CONTRACT_FIELDS, "pilot manifest.canvas.contract"
    )
    expected_contract = {
        "state_selection": "exclusive_single_primary_layer",
        "primary_layers": [
            "rack_orientation",
            "rack_power_conversion",
            "processor_point_of_load",
            "compute_demand_loop",
            "abilene_mapping",
        ],
        "evidence_binding": "content_record_fact_refs",
        "geometry_owner": "compute_power_descent_renderer",
        "handoff_requires": "abilene_mapping",
    }
    if contract != expected_contract:
        raise ComputeVisualError(
            "pilot manifest.canvas.contract must match compute_power_descent_v1"
        )

    content = {
        "rack_orientation": _normalize_orientation(
            manifest["rack_orientation"], ledgers
        ),
        "rack_power_conversion": _normalize_conversion(
            manifest["rack_power_conversion"], ledgers
        ),
        "processor_point_of_load": _normalize_point_of_load(
            manifest["processor_point_of_load"], ledgers
        ),
        "compute_demand_loop": _normalize_demand_loop(
            manifest["compute_demand_loop"], ledgers
        ),
        "abilene_mapping": _normalize_abilene(manifest["abilene_mapping"], ledgers),
        "phase6_handoff": _normalize_handoff(manifest["phase6_handoff"], ledgers),
        "evidence_gaps": _normalize_gaps(manifest["evidence_gaps"], ledgers),
    }
    states = _normalize_states(manifest["states"])
    try:
        evidence = base.compile_evidence_cards(
            _collect_fact_refs(content), ledgers, ledger_ids=declared_ledgers
        )
    except base.TeachingVisualError as error:
        raise ComputeVisualError(str(error)) from error

    payload = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "pilot": {
            "id": _identifier(manifest["id"], "pilot manifest.id"),
            "title": _text(manifest["title"], "pilot manifest.title", maximum=180),
            "phase": {
                "id": _identifier(phase["id"], "pilot manifest.phase.id"),
                "number": 5,
                "title": _text(
                    phase["title"], "pilot manifest.phase.title", maximum=140
                ),
                "anchor_question": _text(
                    phase["anchor_question"],
                    "pilot manifest.phase.anchor_question",
                    maximum=320,
                ),
            },
            "learning_objective": _text(
                manifest["learning_objective"],
                "pilot manifest.learning_objective",
                maximum=720,
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
        raise ComputeVisualError(
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


def orientation_geometry() -> dict[str, tuple[int, int, int, int]]:
    """Return the state-1 extents used to keep every object in the viewBox."""
    return {
        "hall": (65, 115, 675, 620),
        "rack": (785, 40, 1025, 650),
        "board": (1170, 160, 1530, 550),
        "boundary": (55, 660, 1545, 765),
    }


def svg_geometry_contract() -> dict[str, dict[str, tuple[int, int, int, int]]]:
    """Publish conservative bounds for every desktop state's visible objects."""
    return {
        "orient_inside_rack": orientation_geometry(),
        "facility_ac_to_rack_dc": {
            "ac_input": (55, 170, 435, 500),
            "power_shelf": (590, 170, 970, 500),
            "dc_bus": (1125, 170, 1505, 500),
            "product_boundary": (520, 535, 1080, 607),
            "evidence_boundary": (55, 625, 1545, 730),
        },
        "board_point_of_load": {
            "steps": (55, 180, 1530, 465),
            "rail_callout": (820, 505, 1500, 610),
            "evidence_boundary": (55, 625, 1545, 730),
        },
        "useful_compute_and_upstream_demand": {
            "forward_allocation": (55, 205, 1523, 390),
            "upstream_demand": (75, 470, 1525, 600),
            "evidence_boundary": (55, 630, 1545, 735),
        },
        "abilene_compute_boundary": {
            "known_and_unknown": (55, 150, 1545, 603),
            "evidence_boundary": (55, 625, 1545, 730),
        },
        "heat_carrier_handoff": {
            "processor": (70, 165, 420, 415),
            "useful_output": (540, 145, 1500, 335),
            "processor_heat": (70, 500, 520, 650),
            "thermal_split": (590, 405, 1500, 650),
        },
    }


def _boundary_svg(record: Mapping[str, Any], *, y: int) -> str:
    return (
        f'<g class="boundary-strip" transform="translate(55 {y})">'
        '<rect width="1490" height="105" rx="10"/>'
        f'<text class="boundary-kicker" x="22" y="27">EVIDENCE BOUNDARY</text>'
        + _wrapped(
            record["body"],
            x=22,
            y=52,
            width_chars=150,
            line_height=19,
            css_class="boundary-copy",
            maximum_lines=3,
        )
        + f"<desc>{_escape(_fact_description(record))}</desc></g>"
    )


def _orientation_svg(record: Mapping[str, Any]) -> str:
    layers = {layer["id"]: layer for layer in record["layers"]}
    hall = layers["data_hall_boundary"]
    rack = layers["rack_envelope"]
    board = layers["board_and_die"]
    return f"""
<g data-orientation-layer hidden>
  <text class="layer-kicker" x="55" y="50">2D / 3D ORIENTATION · NESTED SYSTEM, NOT AN AS-BUILT DRAWING</text>
  <text class="layer-title" x="55" y="88">{_escape(record["title"])}</text>
  <g data-orientation-layer-id="data_hall_boundary" hidden>
    <g class="hall-cutaway" transform="translate(65 115)">
      <polygon class="hall-top" points="0,70 330,0 610,90 280,162"/>
      <polygon class="hall-side" points="280,162 610,90 610,430 280,505"/>
      <polygon class="hall-front" points="0,70 280,162 280,505 0,410"/>
      <path class="facility-ac" d="M 42 310 H 136 V 238 H 250"/>
      <text class="carrier-label" x="36" y="346">FACILITY AC</text>
      <text class="object-kicker" x="22" y="34">DATA HALL BOUNDARY</text>
      <text class="object-title" x="22" y="66">{_escape(hall["title"])}</text>
      <text class="object-copy" x="22" y="392">busway / distribution → tap-off → rack position</text>
    </g>
    <desc>{_escape(_fact_description(hall))}</desc>
  </g>
  <path class="descent-link" d="M 650 365 C 720 365 720 365 785 365"/>
  <g data-orientation-layer-id="rack_envelope" hidden>
    <g class="rack-iso" transform="translate(795 40)">
      <polygon class="rack-top" points="0,52 104,14 220,55 115,94"/>
      <polygon class="rack-side" points="115,94 220,55 220,520 115,560"/>
      <polygon class="rack-front" points="0,52 115,94 115,560 0,518"/>
      <rect class="shelf-band" x="13" y="124" width="89" height="62" rx="4"/>
      <rect class="dc-band" x="13" y="204" width="89" height="30" rx="4"/>
      <rect class="tray-band" x="13" y="250" width="89" height="72" rx="4"/>
      <rect class="tray-band" x="13" y="336" width="89" height="72" rx="4"/>
      <rect class="tray-band" x="13" y="422" width="89" height="72" rx="4"/>
      <text class="object-kicker" x="0" y="-18">RACK ENVELOPE</text>
      <text class="small-label" x="57" y="160">power shelf</text>
      <text class="small-label" x="57" y="226">DC bus</text>
      <text class="small-label" x="57" y="294">trays</text>
      <g class="rack-carrier-band" transform="translate(-10 580)">
        <rect width="240" height="30" rx="6"/>
        <text x="120" y="20">AC IN · DC AFTER CONVERSION</text>
      </g>
    </g>
    <desc>{_escape(_fact_description(rack))}</desc>
  </g>
  <path class="descent-link" d="M 1038 365 C 1100 365 1100 365 1160 365"/>
  <g data-orientation-layer-id="board_and_die" hidden>
    <g class="board-close" transform="translate(1170 160)">
      <rect class="board" width="360" height="390" rx="18"/>
      <rect class="bus-chip" x="24" y="52" width="95" height="60" rx="8"/>
      <g class="vrm-phases">
        <rect x="142" y="45" width="34" height="74" rx="5"/>
        <rect x="184" y="45" width="34" height="74" rx="5"/>
        <rect x="226" y="45" width="34" height="74" rx="5"/>
        <rect x="268" y="45" width="34" height="74" rx="5"/>
      </g>
      <path class="board-power" d="M 119 82 H 138 M 305 82 H 326 V 206"/>
      <rect class="processor" x="112" y="172" width="180" height="152" rx="12"/>
      <path class="die-grid" d="M 142 205 H 262 M 142 240 H 262 M 142 275 H 262 M 172 193 V 306 M 212 193 V 306 M 252 193 V 306"/>
      <text class="object-kicker" x="0" y="-25">BOARD / PROCESSOR BOUNDARY</text>
      <text class="small-label" x="38" y="88">DC bus</text>
      <text class="small-label" x="160" y="139">multiphase regulation</text>
      <text class="processor-label" x="202" y="346">PROCESSOR</text>
      <text class="carrier-label" x="16" y="374">PROGRESSIVELY LOWER-VOLTAGE DC</text>
    </g>
    <desc>{_escape(_fact_description(board))}</desc>
  </g>
  {_boundary_svg(record["boundary"], y=660)}
</g>
"""


def _conversion_step_svg(
    step: Mapping[str, Any],
    *,
    x: int,
    css_class: str,
) -> str:
    if "boundary" in step:
        boundary = step["boundary"]
    else:
        boundary = {
            "rack_power_shelf": (
                "Product documentation supports this conversion boundary; "
                "it does not establish site operation."
            ),
            "rack_dc_bus": (
                "Nominal product output only; no rack-count or facility-load "
                "inference follows."
            ),
        }[step["id"]]
    return (
        f'<g data-rack-conversion-step-id="{_escape(step["id"])}" hidden '
        f'transform="translate({x} 170)">'
        f'<rect class="conversion-node {css_class}" width="380" height="330" rx="16"/>'
        f'<text class="node-posture" x="26" y="40">{_escape(step["value_posture"].replace("_", " ").upper())}</text>'
        + _wrapped(
            step["title"],
            x=26,
            y=82,
            width_chars=30,
            line_height=30,
            css_class="node-title",
            maximum_lines=2,
        )
        + _wrapped(
            step["verb"],
            x=26,
            y=158,
            width_chars=43,
            line_height=22,
            css_class="node-copy",
            maximum_lines=3,
        )
        + _wrapped(
            boundary,
            x=26,
            y=247,
            width_chars=46,
            line_height=18,
            css_class="node-boundary",
            maximum_lines=4,
        )
        + f"<desc>{_escape(_fact_description(step))}</desc></g>"
    )


def _conversion_svg(record: Mapping[str, Any]) -> str:
    steps = record["steps"]
    return f"""
<g data-rack-conversion-layer hidden>
  <text class="layer-kicker" x="55" y="50">CARRIER BOUNDARY · FACILITY AC → PRODUCT CONVERSION → NOMINAL RACK DC</text>
  <text class="layer-title" x="55" y="88">{_escape(record["title"])}</text>
  <path class="conversion-arrow ac-arrow" d="M 435 335 H 560"/>
  <path class="conversion-arrow dc-arrow" d="M 970 335 H 1095"/>
  {_conversion_step_svg(steps[0], x=55, css_class="ac-node")}
  {_conversion_step_svg(steps[1], x=590, css_class="shelf-node")}
  {_conversion_step_svg(steps[2], x=1125, css_class="dc-node")}
  <g class="carrier-pill ac-pill" transform="translate(456 284)"><rect width="86" height="42" rx="21"/><text x="43" y="27">AC</text></g>
  <g class="carrier-pill dc-pill" transform="translate(991 284)"><rect width="86" height="42" rx="21"/><text x="43" y="27">DC</text></g>
  <g class="explicit-boundary" transform="translate(520 535)">
    <rect width="560" height="72" rx="10"/>
    <text x="280" y="28">DOCUMENTED PRODUCT BOUNDARY</text>
    <text class="boundary-emphasis" x="280" y="53">nominal rack DC ≠ Abilene measurement</text>
  </g>
  {_boundary_svg(record["boundary"], y=625)}
</g>
"""


def _point_step_svg(step: Mapping[str, Any], *, x: int, index: int) -> str:
    css = ["intermediate", "vrm", "rails", "processor-step"][index]
    return (
        f'<g data-point-of-load-step-id="{_escape(step["id"])}" hidden '
        f'transform="translate({x} 180)">'
        f'<rect class="point-node {css}" width="320" height="285" rx="15"/>'
        f'<text class="node-index" x="25" y="40">0{index + 1}</text>'
        + _wrapped(
            step["title"],
            x=25,
            y=83,
            width_chars=28,
            line_height=29,
            css_class="node-title",
            maximum_lines=2,
        )
        + _wrapped(
            step["verb"],
            x=25,
            y=157,
            width_chars=37,
            line_height=21,
            css_class="node-copy",
            maximum_lines=4,
        )
        + f'<text class="node-posture bottom-posture" x="25" y="260">{_escape(step["value_posture"].replace("_", " ").upper())}</text>'
        + f"<desc>{_escape(_fact_description(step))}</desc></g>"
    )


def _point_of_load_svg(record: Mapping[str, Any]) -> str:
    steps = record["steps"]
    nodes = "".join(
        _point_step_svg(step, x=55 + index * 385, index=index)
        for index, step in enumerate(steps)
    )
    arrows = "".join(
        f'<path class="point-arrow" d="M {375 + index * 385} 322 H {425 + index * 385}"/>'
        for index in range(3)
    )
    return f"""
<g data-point-of-load-layer hidden>
  <text class="layer-kicker" x="55" y="50">BOARD POWER DESCENT · GENERIC FUNCTION, NO UNIVERSAL RAIL VALUE</text>
  <text class="layer-title" x="55" y="88">{_escape(record["title"])}</text>
  <g class="trend-band" transform="translate(55 150)">
    <path d="M 0 22 H 1470"/>
    <text x="0" y="8">INTERMEDIATE DC</text>
    <text class="trend-center" x="735" y="8">VOLTAGE STEPS DOWN · CURRENT CAPABILITY RISES</text>
    <text class="trend-end" x="1470" y="8">PRECISE PROCESSOR RAILS</text>
  </g>
  {arrows}{nodes}
  <g class="rail-callout" transform="translate(820 505)">
    <rect width="680" height="105" rx="11"/>
    <text x="24" y="34">LOW VOLTAGE · HIGH CURRENT</text>
    <text class="rail-copy" x="24" y="66">Precise point-of-load function, intentionally without a numerical rail.</text>
    <text class="rail-copy" x="24" y="88">Rack DC is not the processor core voltage.</text>
  </g>
  {_boundary_svg(record["boundary"], y=625)}
</g>
"""


def _demand_svg(record: Mapping[str, Any]) -> str:
    forward = record["forward_allocation"]
    upstream = record["upstream_demand"]
    forward_summaries = {
        "facility_power": "Includes IT equipment and non-IT facility loads.",
        "it_power": "Needs matching metering or a boundary-consistent PUE relationship.",
        "accelerator_power": "Needs a measured share or matching inventory and power evidence.",
        "active_compute": "Needs model, workload, software, utilization, and measurement context.",
        "useful_output": "Needs workload-specific measurement or a fully qualified scenario.",
    }
    upstream_summaries = {
        "synchronized_work": "Parallel work can correlate processor-level demand.",
        "aggregation_path": "Demand aggregates through board, rack, building, and campus.",
        "grid_facing_load": "Fast power-electronic load changes can challenge grid response.",
    }
    forward_nodes = []
    for index, step in enumerate(forward):
        x = 55 + index * 302
        forward_nodes.append(
            f'<g class="allocation-node" transform="translate({x} 205)">'
            '<rect width="260" height="185" rx="12"/>'
            f'<text class="node-index" x="20" y="36">0{index + 1}</text>'
            + _wrapped(
                step["title"],
                x=20,
                y=75,
                width_chars=26,
                line_height=25,
                css_class="allocation-title",
                maximum_lines=2,
            )
            + _wrapped(
                forward_summaries[step["id"]],
                x=20,
                y=131,
                width_chars=36,
                line_height=16,
                css_class="allocation-copy",
                maximum_lines=4,
            )
            + f"<desc>{_escape(_fact_description(step))}</desc></g>"
        )
    demand_cards = []
    for index, step in enumerate(upstream):
        x = 75 + index * 505
        demand_cards.append(
            f'<g class="demand-node" transform="translate({x} 470)">'
            '<rect width="440" height="130" rx="12"/>'
            f'<text class="demand-direction" x="22" y="32">DEMAND VIEW · STEP {index + 1}</text>'
            + _wrapped(
                step["title"],
                x=22,
                y=66,
                width_chars=42,
                line_height=23,
                css_class="demand-title",
                maximum_lines=2,
            )
            + _wrapped(
                upstream_summaries[step["id"]],
                x=22,
                y=107,
                width_chars=58,
                line_height=16,
                css_class="demand-copy",
                maximum_lines=3,
            )
            + f"<desc>{_escape(_fact_description(step))}</desc></g>"
        )
    forward_arrows = "".join(
        f'<path class="useful-arrow" d="M {315 + index * 302} 297 H {347 + index * 302}"/>'
        for index in range(4)
    )
    upstream_arrows = "".join(
        f'<path class="demand-arrow" d="M {515 + index * 505} 535 H {558 + index * 505}"/>'
        for index in range(2)
    )
    return f"""
<g data-compute-demand-layer hidden>
  <text class="layer-kicker" x="55" y="50">TWO READINGS · USEFUL OUTPUT FORWARD / CORRELATED DEMAND UPSTREAM</text>
  <text class="layer-title" x="55" y="88">{_escape(record["title"])}</text>
  <g class="lane-label useful-label" transform="translate(55 140)"><rect width="415" height="40" rx="20"/><text x="207" y="26">FORWARD ALLOCATION · ELECTRICITY → WORK</text></g>
  {forward_arrows}{"".join(forward_nodes)}
  <path class="turn-arrow" d="M 1432 400 C 1432 430 1370 432 1300 432"/>
  <g class="lane-label demand-label" transform="translate(55 414)"><rect width="620" height="40" rx="20"/><text x="310" y="26">UPSTREAM DEMAND SIGNATURE · NOT REVERSE ELECTRICAL FLOW</text></g>
  {upstream_arrows}{"".join(demand_cards)}
  {_boundary_svg(record["boundary"], y=630)}
</g>
"""


def _abilene_card_svg(
    record: Mapping[str, Any],
    *,
    x: int,
    y: int,
    known: bool,
) -> str:
    data_name = "abilene-known-id" if known else "abilene-unknown-id"
    css = "known-card" if known else "unknown-card"
    status = "SUPPORTED" if known else "UNRESOLVED"
    summaries = {
        "platform_family": (
            "GB200 is supported for Phase 1; NVL72 remains a design reference, "
            "not an installed count."
        ),
        "rack_delivery": (
            "First GB200 racks arrived in June 2025; delivered and operating "
            "counts are undisclosed."
        ),
        "live_compute": (
            "Early training and inference are confirmed; the exact first-live "
            "date is unresolved."
        ),
        "rack_and_rail_configuration": (
            "Rack variant and count, populated trays, shelf input, power "
            "configuration, and processor rail are unknown."
        ),
        "power_allocation": (
            "Facility and IT power, PUE, accelerator count and share, usable "
            "power, and utilization are unknown."
        ),
        "workload_and_output": (
            "Model, workload, training utilization, inference batching, and "
            "measured token throughput are unknown."
        ),
        "site_demand_waveform": (
            "No site trace establishes synchronized-demand magnitude, ramp, "
            "recurrence, or grid response."
        ),
    }
    return (
        f'<g data-{data_name}="{_escape(record["id"])}" hidden '
        f'class="abilene-card {css}" transform="translate({x} {y})">'
        '<rect width="700" height="108" rx="12"/>'
        f'<text class="abilene-status {css}" x="22" y="24">{status}</text>'
        + _wrapped(
            record["title"],
            x=22,
            y=50,
            width_chars=60,
            line_height=20,
            css_class="abilene-title",
            maximum_lines=2,
        )
        + _wrapped(
            summaries[record["id"]],
            x=22,
            y=82,
            width_chars=94,
            line_height=14,
            css_class="abilene-copy",
            maximum_lines=2,
        )
        + f"<desc>{_escape(_fact_description(record))}</desc></g>"
    )


def _abilene_svg(record: Mapping[str, Any]) -> str:
    known = "".join(
        _abilene_card_svg(item, x=55, y=150 + index * 115, known=True)
        for index, item in enumerate(record["known"])
    )
    unknown = "".join(
        _abilene_card_svg(item, x=845, y=150 + index * 115, known=False)
        for index, item in enumerate(record["unknown"])
    )
    return f"""
<g data-abilene-layer hidden>
  <text class="layer-kicker" x="55" y="50">ABILENE · PLATFORM AND ACTIVITY EVIDENCE ≠ OPERATING POWER MODEL</text>
  <text class="layer-title" x="55" y="88">{_escape(record["title"])}</text>
  <text class="column-title known-column" x="55" y="138">WHAT THE RECORD SUPPORTS</text>
  <text class="column-title unknown-column" x="845" y="138">WHAT REMAINS UNKNOWN</text>
  {known}{unknown}
  {_boundary_svg(record["guard"], y=625)}
</g>
"""


def _handoff_svg(record: Mapping[str, Any]) -> str:
    carriers = {item["id"]: item for item in record["carriers"]}
    useful = carriers["useful_compute_output"]
    heat = carriers["processor_heat"]
    split = carriers["liquid_and_air_split"]
    useful_boundary = (
        "Activity is confirmed; model, utilization, throughput, and a numerical "
        "useful-compute fraction are not."
    )
    heat_boundary = (
        "Generic energy balance, not a per-die fraction or measured Abilene load."
    )
    split_boundary = (
        "Product cooling roles are documented; Abilene as-built cooling "
        "interfaces remain unknown."
    )
    return f"""
<g data-phase6-handoff hidden>
  <text class="layer-kicker" x="55" y="50">PHASE BOUNDARY · COMPUTATION IS DESIRED; HEAT CREATES THE COOLING OBLIGATION</text>
  <text class="layer-title" x="55" y="88">{_escape(record["title"])}</text>
  <g class="handoff-processor" transform="translate(70 165)">
    <rect width="350" height="250" rx="20"/>
    <path class="die-grid" d="M 55 88 H 295 M 55 138 H 295 M 55 188 H 295 M 115 58 V 212 M 175 58 V 212 M 235 58 V 212"/>
    <text class="processor-kicker" x="175" y="34">ACTIVE PROCESSOR</text>
    <text class="processor-label" x="175" y="232">ELECTRICAL INPUT</text>
  </g>
  <path class="useful-branch" d="M 420 270 H 520"/>
  <g data-handoff-carrier-id="useful_compute_output" class="handoff-output useful-output" transform="translate(540 145)">
    <rect width="960" height="190" rx="16"/>
    <text class="handoff-status" x="28" y="34">DESIRED OUTPUT</text>
    <text class="handoff-title" x="28" y="72">{_escape(useful["title"])}</text>
    <text class="handoff-carrier" x="28" y="105">{_escape(useful["carrier"])}</text>
    {_wrapped(useful_boundary, x=28, y=140, width_chars=122, line_height=18, css_class="handoff-copy", maximum_lines=2)}
    <desc>{_escape(_fact_description(useful))}</desc>
  </g>
  <path class="heat-branch" d="M 245 415 V 485"/>
  <g data-handoff-carrier-id="processor_heat" class="heat-node" transform="translate(70 500)">
    <rect width="450" height="150" rx="15"/>
    <text class="handoff-status" x="24" y="31">THERMAL OBLIGATION</text>
    <text class="handoff-title" x="24" y="64">{_escape(heat["title"])}</text>
    <text class="handoff-carrier" x="24" y="92">{_escape(heat["carrier"])}</text>
    {_wrapped(heat_boundary, x=24, y=119, width_chars=54, line_height=16, css_class="handoff-copy", maximum_lines=2)}
    <desc>{_escape(_fact_description(heat))}</desc>
  </g>
  <path class="thermal-arrow" d="M 520 575 H 575"/>
  <g data-handoff-carrier-id="liquid_and_air_split" class="thermal-split" transform="translate(590 405)">
    <rect width="910" height="245" rx="16"/>
    <text class="handoff-status" x="28" y="32">NEXT · PHASE 6</text>
    <text class="handoff-title" x="28" y="66">{_escape(split["title"])}</text>
    <g class="thermal-path liquid-path" transform="translate(28 86)"><rect width="405" height="62" rx="9"/><text x="202" y="38">LIQUID-COOLED PROCESSOR PATH</text></g>
    <g class="thermal-path air-path" transform="translate(461 86)"><rect width="405" height="62" rx="9"/><text x="202" y="38">RESIDUAL AIR-COOLED RACK PATH</text></g>
    {_wrapped(split_boundary, x=28, y=184, width_chars=114, line_height=18, css_class="handoff-copy", maximum_lines=2)}
    <desc>{_escape(_fact_description(split))}</desc>
  </g>
</g>
"""


def _responsive_card(
    record: Mapping[str, Any],
    *,
    data_name: str,
    css_class: str = "",
    initially_hidden: bool = True,
) -> str:
    paragraphs = []
    for key in ("carrier", "verb", "body", "boundary"):
        if key in record:
            paragraphs.append(
                f'<p class="responsive-{_escape(key)}">{_escape(record[key])}</p>'
            )
    if "contains" in record:
        paragraphs.append(
            '<ul class="responsive-contains">'
            + "".join(f"<li>{_escape(item)}</li>" for item in record["contains"])
            + "</ul>"
        )
    posture = ""
    if "value_posture" in record:
        posture = (
            '<p class="responsive-posture">'
            + _escape(record["value_posture"].replace("_", " ").upper())
            + "</p>"
        )
    return (
        f'<article class="responsive-card {css_class}" '
        f'data-{data_name}="{_escape(record["id"])}"'
        + (" hidden" if initially_hidden else "")
        + ">"
        f"<h3>{_escape(record.get('title', record['id']))}</h3>"
        + posture
        + "".join(paragraphs)
        + f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        + "</article>"
    )


def _responsive_boundary(record: Mapping[str, Any]) -> str:
    title = record.get("title", "Evidence boundary")
    return (
        '<aside class="responsive-boundary">'
        f"<strong>{_escape(title)}</strong><p>{_escape(record['body'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</aside>"
    )


def _responsive_orientation(record: Mapping[str, Any]) -> str:
    cards = "".join(
        _responsive_card(
            layer,
            data_name="orientation-layer-id",
            css_class=f"orientation-{_escape(layer['id'])}",
        )
        for layer in record["layers"]
    )
    return (
        '<section class="responsive-layer responsive-orientation" '
        "data-responsive-orientation-layer hidden>"
        '<p class="responsive-kicker">2D / 3D nested orientation · not as-built</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-nested-path">'
        + cards
        + "</div>"
        + _responsive_boundary(record["boundary"])
        + "</section>"
    )


def _responsive_conversion(record: Mapping[str, Any]) -> str:
    parts = []
    for index, step in enumerate(record["steps"]):
        if index:
            carrier = "AC" if index == 1 else "DC"
            parts.append(
                f'<span class="responsive-arrow" aria-hidden="true">→ <b>{carrier}</b> →</span>'
            )
        parts.append(
            _responsive_card(
                step,
                data_name="rack-conversion-step-id",
                css_class=f"conversion-{_escape(step['id'])}",
            )
        )
    return (
        '<section class="responsive-layer" data-responsive-rack-conversion-layer hidden>'
        '<p class="responsive-kicker">Facility AC → conversion → documented nominal rack DC</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-flow conversion-flow">' + "".join(parts) + "</div>"
        '<p class="responsive-explicit-boundary"><strong>Documented product boundary:</strong> nominal rack DC is not an Abilene measurement.</p>'
        + _responsive_boundary(record["boundary"])
        + "</section>"
    )


def _responsive_point_of_load(record: Mapping[str, Any]) -> str:
    parts = []
    for index, step in enumerate(record["steps"]):
        if index:
            parts.append('<span class="responsive-arrow" aria-hidden="true">→</span>')
        parts.append(
            _responsive_card(
                step,
                data_name="point-of-load-step-id",
                css_class=f"point-{_escape(step['id'])}",
            )
        )
    return (
        '<section class="responsive-layer" data-responsive-point-of-load-layer hidden>'
        '<p class="responsive-kicker">Generic board power descent · no universal rail value</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<p class="responsive-trend"><strong>Voltage steps down</strong><span>current capability rises</span></p>'
        '<div class="responsive-flow point-flow">' + "".join(parts) + "</div>"
        '<p class="responsive-explicit-boundary"><strong>Low voltage · high current:</strong> rack DC is not processor core voltage.</p>'
        + _responsive_boundary(record["boundary"])
        + "</section>"
    )


def _responsive_demand(record: Mapping[str, Any]) -> str:
    forward = "".join(
        _responsive_card(
            item,
            data_name="forward-allocation-id",
            initially_hidden=False,
        )
        for item in record["forward_allocation"]
    )
    upstream = "".join(
        _responsive_card(
            item,
            data_name="upstream-demand-id",
            css_class="demand-card",
            initially_hidden=False,
        )
        for item in record["upstream_demand"]
    )
    return (
        '<section class="responsive-layer" data-responsive-compute-demand-layer hidden>'
        '<p class="responsive-kicker">Two readings · linked, not interchangeable</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<h3 class="lane-heading useful-heading">Forward allocation · electricity → useful work</h3>'
        '<div class="responsive-demand-grid forward-grid">' + forward + "</div>"
        '<h3 class="lane-heading demand-heading">Upstream demand signature · not reverse electrical flow</h3>'
        '<div class="responsive-demand-grid upstream-grid">'
        + upstream
        + "</div>"
        + _responsive_boundary(record["boundary"])
        + "</section>"
    )


def _responsive_abilene(record: Mapping[str, Any]) -> str:
    known = "".join(
        _responsive_card(
            item, data_name="abilene-known-id", css_class="responsive-known"
        )
        for item in record["known"]
    )
    unknown = "".join(
        _responsive_card(
            item, data_name="abilene-unknown-id", css_class="responsive-unknown"
        )
        for item in record["unknown"]
    )
    return (
        '<section class="responsive-layer" data-responsive-abilene-layer hidden>'
        '<p class="responsive-kicker">Abilene · evidence / unknown split</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-abilene-grid">'
        '<div><h3 class="known-heading">What the record supports</h3>'
        + known
        + '</div><div><h3 class="unknown-heading">What remains unknown</h3>'
        + unknown
        + "</div></div>"
        + _responsive_boundary(record["guard"])
        + "</section>"
    )


def _responsive_handoff(record: Mapping[str, Any]) -> str:
    carriers = {item["id"]: item for item in record["carriers"]}
    useful = _responsive_card(
        carriers["useful_compute_output"],
        data_name="handoff-carrier-id",
        css_class="responsive-useful",
        initially_hidden=False,
    )
    heat = _responsive_card(
        carriers["processor_heat"],
        data_name="handoff-carrier-id",
        css_class="responsive-heat",
        initially_hidden=False,
    )
    split = _responsive_card(
        carriers["liquid_and_air_split"],
        data_name="handoff-carrier-id",
        css_class="responsive-thermal-split",
        initially_hidden=False,
    )
    return (
        '<section class="responsive-layer responsive-handoff" '
        "data-responsive-phase6-handoff hidden>"
        '<p class="responsive-kicker">Phase boundary · cooling obligation begins</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-processor">ACTIVE PROCESSOR · electrical input</div>'
        '<div class="responsive-output-split"><div><span class="split-label">Desired output</span>'
        + useful
        + '</div><div><span class="split-label">Thermal obligation</span>'
        + heat
        + '<span class="responsive-arrow vertical-arrow" aria-hidden="true">↓</span>'
        + split
        + '<div class="responsive-thermal-paths"><span>Liquid-cooled processor path</span><span>Residual air-cooled rack path</span></div>'
        + "</div></div></section>"
    )


def _responsive_visual(payload: Mapping[str, Any]) -> str:
    return (
        '<section class="responsive-visual" aria-label="Responsive rack-to-compute teaching surface">'
        + _responsive_orientation(payload["rack_orientation"])
        + _responsive_conversion(payload["rack_power_conversion"])
        + _responsive_point_of_load(payload["processor_point_of_load"])
        + _responsive_demand(payload["compute_demand_loop"])
        + _responsive_abilene(payload["abilene_mapping"])
        + _responsive_handoff(payload["phase6_handoff"])
        + "</section>"
    )


def render_compute_power_descent(payload: dict[str, Any]) -> str:
    """Render the compiled Phase 5 payload as one self-contained HTML page."""
    if payload.get("canvas", {}).get("kind") != CANVAS_KIND:
        raise ComputeVisualError("render payload is not a compute power descent")
    state_buttons = "".join(
        f'<button class="state-button" type="button" role="tab" '
        f'id="state-tab-{_escape(state["id"])}" aria-controls="visual" '
        f'aria-label="State {index + 1}: {_escape(state["title"])}" '
        f'title="{_escape(state["title"])}" aria-selected="false" '
        f'data-state-index="{index}">'
        f'<span class="state-number">{index + 1:02d}</span>'
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
  :root {{ --paper:#fafaf7; --ink:#171918; --muted:#5e625f; --faint:#d8dad5; --blue:#185f8f; --blue-soft:#eaf3f9; --green:#278a76; --green-soft:#e7f5f1; --amber:#aa6819; --amber-soft:#fff5e5; --red:#b23a32; --red-soft:#fbefed; --violet:#6250a8; --violet-soft:#f1eefb; }}
  * {{ box-sizing:border-box; }} [hidden] {{ display:none !important; }}
  html,body {{ width:100%; height:100%; min-height:0; margin:0; background:var(--paper); color:var(--ink); font-family:Inter,"Helvetica Neue",Arial,sans-serif; }}
  html {{ overflow:hidden; }} body {{ display:grid; grid-template-rows:auto minmax(0,1fr) auto; height:100dvh; min-height:0; overflow:hidden; }}
  header {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(300px,570px); gap:22px; padding:10px 20px 9px; border-bottom:1.5px solid var(--ink); }}
  .eyebrow,.phase-question,.state-number,.layer-kicker,.object-kicker,.node-posture,.boundary-kicker,.abilene-status,.column-title,.handoff-status,.responsive-kicker,.responsive-posture,.split-label {{ text-transform:uppercase; letter-spacing:.075em; font-size:11px; font-weight:760; }}
  h1 {{ margin:3px 0; font-size:clamp(21px,2.2vw,34px); line-height:1.05; }} header p {{ margin:2px 0; line-height:1.3; }} .objective {{ align-self:end; color:var(--muted); font-size:13px; }}
  main {{ min-width:0; min-height:0; display:grid; place-items:center; overflow:hidden; padding:7px 13px; }} .visual-shell {{ width:100%; height:100%; max-width:1600px; max-height:900px; border:1.5px solid var(--ink); background:white; }} svg {{ display:block; width:100%; height:100%; }}
  .layer-kicker {{ fill:var(--blue); }} .layer-title {{ font-size:31px; font-weight:790; }} .object-kicker {{ fill:var(--muted); }} .object-title {{ font-size:23px; font-weight:760; }} .object-copy {{ fill:var(--muted); font-size:14px; }} .small-label {{ fill:var(--muted); font-size:12px; font-weight:720; text-anchor:middle; }}
  .hall-top,.rack-top {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:2; }} .hall-front,.rack-front {{ fill:#fff; stroke:var(--ink); stroke-width:2; }} .hall-side,.rack-side {{ fill:#edf0ed; stroke:var(--ink); stroke-width:2; }} .facility-ac {{ fill:none; stroke:var(--blue); stroke-width:8; marker-end:url(#arrow-blue); }} .carrier-label {{ fill:var(--blue); font-size:12px; font-weight:780; letter-spacing:.05em; }}
  .shelf-band {{ fill:var(--blue-soft); stroke:var(--blue); }} .dc-band {{ fill:var(--green-soft); stroke:var(--green); }} .tray-band {{ fill:#fff; stroke:var(--faint); }} .rack-carrier-band rect {{ fill:var(--ink); }} .rack-carrier-band text {{ fill:white; font-size:11px; font-weight:780; letter-spacing:.045em; text-anchor:middle; }} .descent-link {{ fill:none; stroke:var(--violet); stroke-width:5; stroke-dasharray:10 8; marker-end:url(#arrow-violet); }}
  .board {{ fill:#eff6ef; stroke:#3b7045; stroke-width:3; }} .bus-chip {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:2; }} .vrm-phases rect {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:2; }} .board-power {{ fill:none; stroke:var(--blue); stroke-width:5; marker-end:url(#arrow-blue); }} .processor {{ fill:var(--violet-soft); stroke:var(--violet); stroke-width:3; }} .die-grid {{ fill:none; stroke:var(--violet); stroke-width:2; opacity:.55; }} .processor-label,.processor-kicker {{ fill:var(--violet); font-size:13px; font-weight:780; text-anchor:middle; }}
  .boundary-strip rect {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.8; }} .boundary-kicker {{ fill:var(--amber); }} .boundary-copy {{ fill:var(--muted); font-size:14px; }}
  .conversion-node,.point-node,.allocation-node rect,.demand-node rect {{ fill:#fff; stroke:var(--ink); stroke-width:2.2; }} .ac-node {{ fill:var(--blue-soft); stroke:var(--blue); }} .shelf-node {{ fill:var(--violet-soft); stroke:var(--violet); }} .dc-node {{ fill:var(--green-soft); stroke:var(--green); }} .node-title {{ font-size:25px; font-weight:780; }} .node-copy {{ fill:var(--ink); font-size:16px; }} .node-boundary {{ fill:var(--muted); font-size:13px; }} .node-posture {{ fill:var(--muted); }} .bottom-posture {{ font-size:9px; }}
  .conversion-arrow,.point-arrow,.useful-arrow,.demand-arrow,.turn-arrow,.useful-branch,.heat-branch,.thermal-arrow {{ fill:none; stroke-width:5; marker-end:url(#arrow-blue); }} .ac-arrow {{ stroke:var(--blue); }} .dc-arrow {{ stroke:var(--green); marker-end:url(#arrow-green); }} .carrier-pill text {{ fill:white; font-size:15px; font-weight:800; text-anchor:middle; }} .ac-pill rect {{ fill:var(--blue); }} .dc-pill rect {{ fill:var(--green); }}
  .explicit-boundary rect,.rail-callout rect {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:2; }} .explicit-boundary text {{ fill:var(--amber); font-size:14px; font-weight:780; text-anchor:middle; }} .explicit-boundary .boundary-emphasis {{ fill:var(--ink); font-size:18px; }}
  .trend-band path {{ stroke:var(--blue); stroke-width:4; marker-end:url(#arrow-blue); }} .trend-band text {{ fill:var(--blue); font-size:12px; font-weight:780; }} .trend-center {{ text-anchor:middle; }} .trend-end {{ text-anchor:end; }} .node-index {{ fill:var(--blue); font-size:15px; font-weight:800; }} .point-node.vrm {{ fill:var(--amber-soft); stroke:var(--amber); }} .point-node.rails {{ fill:var(--green-soft); stroke:var(--green); }} .point-node.processor-step {{ fill:var(--violet-soft); stroke:var(--violet); }} .point-arrow {{ stroke:var(--blue); }} .rail-callout text {{ fill:var(--amber); font-size:15px; font-weight:780; }} .rail-callout .rail-copy {{ fill:var(--muted); font-size:14px; font-weight:500; }}
  .lane-label rect {{ fill:var(--blue); }} .lane-label.demand-label rect {{ fill:var(--violet); }} .lane-label text {{ fill:white; font-size:12px; font-weight:780; text-anchor:middle; }} .allocation-title,.demand-title {{ font-size:18px; font-weight:760; }} .allocation-copy,.demand-copy {{ fill:var(--muted); font-size:12px; }} .useful-arrow {{ stroke:var(--blue); }} .turn-arrow {{ stroke:var(--violet); }} .demand-arrow {{ stroke:var(--violet); marker-end:url(#arrow-violet); }} .demand-node rect {{ fill:var(--violet-soft); stroke:var(--violet); }} .demand-direction {{ fill:var(--violet); font-size:10px; font-weight:780; }}
  .abilene-card rect {{ stroke-width:2; }} .abilene-card.known-card rect {{ fill:var(--green-soft); stroke:var(--green); }} .abilene-card.unknown-card rect {{ fill:var(--amber-soft); stroke:var(--amber); stroke-dasharray:8 6; }} .known-column,.abilene-status.known-card {{ fill:var(--green); }} .unknown-column,.abilene-status.unknown-card {{ fill:var(--amber); }} .abilene-title {{ font-size:18px; font-weight:760; }} .abilene-copy {{ fill:var(--muted); font-size:12px; }}
  .handoff-processor rect {{ fill:var(--violet-soft); stroke:var(--violet); stroke-width:3; }} .useful-branch {{ stroke:var(--green); marker-end:url(#arrow-green); }} .heat-branch,.thermal-arrow {{ stroke:var(--red); marker-end:url(#arrow-red); }} .air-arrow {{ stroke:var(--amber); marker-end:url(#arrow-amber); }} .handoff-output rect,.heat-node rect,.thermal-split > rect {{ stroke-width:2.5; }} .useful-output rect {{ fill:var(--green-soft); stroke:var(--green); }} .heat-node rect {{ fill:var(--red-soft); stroke:var(--red); }} .thermal-split > rect {{ fill:var(--amber-soft); stroke:var(--amber); }} .handoff-status {{ fill:var(--muted); }} .handoff-title {{ font-size:24px; font-weight:780; }} .handoff-carrier {{ fill:var(--muted); font-size:15px; }} .handoff-copy {{ fill:var(--muted); font-size:13px; }} .thermal-path rect {{ stroke-width:2; }} .liquid-path rect {{ fill:var(--blue-soft); stroke:var(--blue); }} .air-path rect {{ fill:white; stroke:var(--amber); }} .thermal-path text {{ font-size:11px; font-weight:780; text-anchor:middle; }}
  footer {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(330px,600px); gap:9px 16px; max-height:49dvh; padding:8px 14px 9px; border-top:1.5px solid var(--ink); }} .state-nav {{ display:grid; grid-template-columns:repeat({len(payload["states"])},minmax(0,1fr)); gap:5px; }} .state-button {{ display:grid; grid-template-columns:auto 1fr; gap:6px; align-items:center; min-width:0; min-height:44px; padding:6px 7px; border:1.5px solid var(--ink); background:transparent; color:inherit; text-align:left; font:inherit; cursor:pointer; }} .state-nav-label {{ overflow:visible; text-overflow:clip; white-space:normal; line-height:1.1; }} .state-button[aria-selected="true"] {{ background:var(--ink); color:white; }} .state-copy {{ min-width:0; align-self:center; }} .state-copy h2 {{ margin:0 0 3px; font-size:16px; }} .state-copy p {{ margin:0; color:var(--muted); font-size:13px; line-height:1.25; }}
  details {{ grid-column:1/-1; min-width:0; border-top:1px solid var(--faint); padding-top:5px; }} details[open] {{ max-height:min(35dvh,330px); overflow:auto; overflow-x:hidden; overscroll-behavior:contain; }} summary {{ position:sticky; top:0; z-index:3; padding:3px 0; background:var(--paper); cursor:pointer; font-weight:700; }} .fact-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr)); gap:10px; margin-bottom:0; padding:0; list-style:none; }} .fact-card {{ min-width:0; padding:9px 11px; border:1px solid var(--faint); background:white; }} .fact-card p {{ margin:5px 0; line-height:1.35; }} .fact-ref,.fact-boundary,.fact-sources,a {{ overflow-wrap:anywhere; word-break:break-word; }} .fact-ref,.fact-boundary {{ color:var(--muted); font-size:11px; }} .fact-sources {{ font-size:12px; }} a {{ color:var(--blue); }}
  .visually-hidden {{ position:absolute !important; width:1px; height:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }} .responsive-visual {{ display:none; }} .responsive-layer {{ width:100%; }} .responsive-layer h2 {{ margin:2px 0 9px; font-size:19px; }} .responsive-card {{ min-width:0; padding:10px; border:1.5px solid var(--ink); border-radius:9px; background:white; overflow-wrap:anywhere; }} .responsive-card h3 {{ margin:1px 0 5px; font-size:14px; line-height:1.2; }} .responsive-card p {{ margin:4px 0; line-height:1.35; }} .responsive-posture,.responsive-kicker {{ color:var(--blue); }} .responsive-carrier {{ color:var(--blue); font-weight:700; }} .responsive-boundary,.responsive-explicit-boundary {{ margin:8px 0 0; padding:8px; border:1px solid var(--amber); border-radius:7px; background:var(--amber-soft); line-height:1.35; overflow-wrap:anywhere; }} .responsive-boundary p {{ margin:4px 0 0; }}
  .responsive-nested-path {{ display:grid; grid-template-columns:1.2fr 1fr 1fr; gap:7px; align-items:stretch; }} .responsive-nested-path article {{ position:relative; }} .orientation-data_hall_boundary {{ border-color:var(--blue); }} .orientation-rack_envelope {{ border-color:var(--violet); }} .orientation-board_and_die {{ border-color:var(--green); }} .responsive-contains {{ margin:6px 0; padding-left:18px; }} .responsive-flow {{ display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:5px; align-items:stretch; }} .conversion-flow {{ grid-template-columns:1fr auto 1fr auto 1fr; }} .point-flow {{ grid-template-columns:1fr auto 1fr auto 1fr auto 1fr; }} .responsive-arrow {{ align-self:center; color:var(--blue); font-weight:800; text-align:center; }} .responsive-trend {{ display:flex; justify-content:space-between; gap:10px; padding:7px; border-bottom:3px solid var(--blue); color:var(--blue); }}
  .responsive-demand-grid {{ display:grid; gap:6px; }} .forward-grid {{ grid-template-columns:repeat(5,minmax(0,1fr)); }} .upstream-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .lane-heading {{ margin:8px 0 5px; padding:6px 8px; border-radius:6px; color:white; font-size:13px; }} .useful-heading {{ background:var(--blue); }} .demand-heading {{ background:var(--violet); }} .demand-card {{ border-color:var(--violet); background:var(--violet-soft); }}
  .responsive-abilene-grid {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }} .responsive-abilene-grid > div {{ display:grid; gap:7px; min-width:0; }} .responsive-abilene-grid > div > h3 {{ margin:0; }} .known-heading {{ color:var(--green); }} .unknown-heading {{ color:var(--amber); }} .responsive-known {{ border-color:var(--green); background:var(--green-soft); }} .responsive-unknown {{ border-color:var(--amber); border-style:dashed; background:var(--amber-soft); }}
  .responsive-processor {{ margin:8px auto; max-width:360px; padding:26px 12px; border:2px solid var(--violet); border-radius:10px; background:var(--violet-soft); color:var(--violet); text-align:center; font-weight:800; }} .responsive-output-split {{ display:grid; grid-template-columns:1fr 1fr; gap:8px; }} .responsive-output-split > div {{ min-width:0; }} .split-label {{ display:block; margin-bottom:5px; }} .responsive-useful {{ border-color:var(--green); background:var(--green-soft); }} .responsive-heat {{ border-color:var(--red); background:var(--red-soft); }} .responsive-thermal-split {{ border-color:var(--amber); background:var(--amber-soft); }} .vertical-arrow {{ display:block; padding:3px; color:var(--red); }} .responsive-thermal-paths {{ display:grid; grid-template-columns:1fr 1fr; gap:5px; margin-top:5px; }} .responsive-thermal-paths span {{ padding:7px; border:1px solid var(--blue); border-radius:6px; text-align:center; font-weight:700; }} .responsive-thermal-paths span + span {{ border-color:var(--amber); }}
  @media (max-width:1300px) {{ .state-button {{ grid-template-columns:1fr; gap:1px; text-align:center; }} }}
  @media (max-width:1100px) and (min-width:901px) {{ main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:6px 10px; }} .visual-shell {{ display:none; }} .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:5px; font-size:12px; }} .responsive-card {{ font-size:12px; }} footer {{ grid-template-columns:minmax(0,1fr) minmax(290px,430px); }} .state-button {{ min-height:42px; padding:4px; font-size:11px; }} }}
  @media (max-height:520px) and (orientation:landscape) {{ header {{ grid-template-columns:1fr; padding:4px 10px 3px; }} header .objective,.phase-question {{ display:none; }} h1 {{ margin:0; font-size:18px; }} .eyebrow {{ margin:0; font-size:9px; }} main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:3px 7px; }} .visual-shell {{ display:none; }} .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:3px; font-size:10px; }} .responsive-layer h2 {{ margin:1px 0 5px; font-size:15px; }} .responsive-card {{ padding:6px; font-size:10px; }} .responsive-card h3 {{ font-size:12px; }} .responsive-boundary,.responsive-explicit-boundary {{ margin-top:5px; padding:5px; }} footer {{ grid-template-columns:1fr; gap:3px; padding:3px 7px 4px; max-height:51dvh; }} .state-nav {{ gap:3px; }} .state-button {{ grid-template-columns:1fr; min-height:31px; padding:2px 3px; font-size:10px; }} .state-number {{ display:none; }} .state-copy h2 {{ margin:0; font-size:12px; }} .state-copy p {{ font-size:10px; line-height:1.2; }} details {{ padding-top:1px; }} details[open] {{ max-height:72dvh; }} summary {{ padding:1px 0; font-size:10px; }} }}
  @media (max-width:520px) and (orientation:portrait) {{ header {{ grid-template-columns:1fr; gap:3px; padding:7px 9px 6px; }} h1 {{ font-size:20px; }} .objective {{ font-size:12px; }} .phase-question {{ font-size:10px; }} main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; padding:5px; }} .visual-shell {{ display:none; }} .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:3px; font-size:12px; }} .responsive-layer h2 {{ font-size:18px; }} .responsive-card {{ padding:9px; font-size:12px; }} .responsive-card h3 {{ font-size:14px; }} .responsive-nested-path,.responsive-abilene-grid,.responsive-output-split,.responsive-demand-grid,.responsive-flow,.responsive-thermal-paths {{ grid-template-columns:1fr; }} .responsive-arrow {{ padding:2px; }} .responsive-trend {{ flex-direction:column; }} footer {{ grid-template-columns:1fr; gap:5px; padding:5px 7px 6px; max-height:52dvh; }} .state-nav {{ grid-template-columns:repeat(3,minmax(0,1fr)); gap:3px; }} .state-button {{ grid-template-columns:1fr; min-height:42px; padding:3px 2px; font-size:10px; }} .state-number {{ font-size:9px; }} .state-copy h2 {{ font-size:14px; }} .state-copy p {{ font-size:12px; }} details[open] {{ max-height:74dvh; }} }}
</style>
</head>
<body>
<header>
  <div><p class="eyebrow">Phase {phase["number"]} · {_escape(phase["title"])}</p><h1>{_escape(payload["pilot"]["title"])}</h1><p class="phase-question">{_escape(phase["anchor_question"])}</p></div>
  <p class="objective">{_escape(payload["pilot"]["learning_objective"])}</p>
</header>
<main>
  <section class="visual-shell" aria-label="Instructor-controlled rack-to-compute teaching surface">
    <svg id="visual" role="img" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" aria-labelledby="visual-title visual-description">
      <title id="visual-title">Rack-to-compute power descent</title>
      <desc id="visual-description">Six manually selected views explain nested rack orientation, facility AC to nominal rack DC conversion, point-of-load descent, useful output and correlated demand, Abilene evidence boundaries, and the heat handoff.</desc>
      <defs>
        <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#185f8f"/></marker>
        <marker id="arrow-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#278a76"/></marker>
        <marker id="arrow-violet" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#6250a8"/></marker>
        <marker id="arrow-red" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#b23a32"/></marker>
        <marker id="arrow-amber" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#aa6819"/></marker>
      </defs>
{_orientation_svg(payload["rack_orientation"])}
{_conversion_svg(payload["rack_power_conversion"])}
{_point_of_load_svg(payload["processor_point_of_load"])}
{_demand_svg(payload["compute_demand_loop"])}
{_abilene_svg(payload["abilene_mapping"])}
{_handoff_svg(payload["phase6_handoff"])}
    </svg>
  </section>
{responsive}
</main>
<footer>
  <nav class="state-nav" role="tablist" aria-label="Manual Phase 5 teaching states">{state_buttons}</nav>
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
  const showHandoff = state.show_phase6_handoff;
  const showAbilene = !showHandoff && (state.abilene_known_ids.length > 0 || state.abilene_unknown_ids.length > 0);
  const showDemand = !showHandoff && !showAbilene && state.show_compute_demand_loop;
  const showPoint = !showHandoff && !showAbilene && !showDemand && state.point_of_load_step_ids.length > 0;
  const showConversion = !showHandoff && !showAbilene && !showDemand && !showPoint && state.rack_conversion_step_ids.length > 0;
  const showOrientation = !showHandoff && !showAbilene && !showDemand && !showPoint && !showConversion && state.orientation_layer_ids.length > 0;
  setLayer("[data-orientation-layer], [data-responsive-orientation-layer]", showOrientation);
  setLayer("[data-rack-conversion-layer], [data-responsive-rack-conversion-layer]", showConversion);
  setLayer("[data-point-of-load-layer], [data-responsive-point-of-load-layer]", showPoint);
  setLayer("[data-compute-demand-layer], [data-responsive-compute-demand-layer]", showDemand);
  setLayer("[data-abilene-layer], [data-responsive-abilene-layer]", showAbilene);
  setLayer("[data-phase6-handoff], [data-responsive-phase6-handoff]", showHandoff);
  setVisible("[data-orientation-layer-id]", state.orientation_layer_ids, "orientationLayerId");
  setVisible("[data-rack-conversion-step-id]", state.rack_conversion_step_ids, "rackConversionStepId");
  setVisible("[data-point-of-load-step-id]", state.point_of_load_step_ids, "pointOfLoadStepId");
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
