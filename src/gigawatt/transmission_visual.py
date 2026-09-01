"""Evidence-bound Phase 2 transmission teaching surface.

The module validates a strict, purpose-built transmission manifest and renders
six coarse states that change only in response to instructor input.  It reuses
the Phase 1 YAML, evidence-ledger, source-digest, and evidence-card contracts.
"""

from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from gigawatt import teaching_visuals as base

SCHEMA_VERSION = 1
CANVAS_KIND = "transmission_landscape_v1"
CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 900
SHORT_LANDSCAPE_MAX_HEIGHT = 520
SHORT_LANDSCAPE_MIN_TEXT_PX = 10
PORTRAIT_MAX_WIDTH = 520
PORTRAIT_MIN_TEXT_PX = 12

PRINCIPLE_IDS = {
    "voltage_transfer",
    "meshed_ac_network",
    "continuous_system_balance",
}
PROCESS_LANE_IDS = {"generator_interconnection", "ercot_large_load_integration"}
ABILENE_PATH_IDS = {"initial_138", "expansion_345"}
STATE_IDS = [
    "why_voltage_rises",
    "network_and_balance",
    "substation_gate",
    "generator_vs_large_load",
    "abilene_grid_paths",
    "campus_distribution_handoff",
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
    "transmission_principles",
    "substation_anatomy",
    "interconnection_processes",
    "abilene_case",
    "phase3_handoff",
    "states",
}
CANVAS_FIELDS = {"kind", "width", "height", "contract"}
CONTRACT_FIELDS = {
    "state_selection",
    "primary_layers",
    "evidence_binding",
    "geometry_owner",
    "handoff_requires",
}
PHASE_FIELDS = {"id", "number", "title", "anchor_question"}
VOLTAGE_FIELDS = {"id", "title", "body", "comparison", "fact_refs"}
PRINCIPLE_FIELDS = {"id", "title", "body", "visual", "fact_refs"}
COMPARISON_FIELDS = {"fixed", "lower_voltage", "higher_voltage", "relation"}
COMPARISON_SIDE_FIELDS = {"voltage", "current", "conductor_loss"}
MESH_VISUAL_FIELDS = {
    "source_labels",
    "network_labels",
    "load_labels",
    "path_posture",
}
BALANCE_VISUAL_FIELDS = {
    "operator_label",
    "supply_label",
    "demand_label",
    "relation",
}
SUBSTATION_FIELDS = {"title", "body", "functions", "boundary", "fact_refs"}
PROCESS_FIELDS = {"title", "lanes", "case_boundary"}
GENERATOR_LANE_FIELDS = {
    "id",
    "title",
    "subject",
    "gate",
    "body",
    "gates",
    "boundary",
    "fact_refs",
}
LOAD_LANE_FIELDS = GENERATOR_LANE_FIELDS | {"status_note"}
STATUS_NOTE_FIELDS = {"label", "body", "fact_refs"}
BOUNDARY_FIELDS = {"title", "body", "fact_refs"}
ABILENE_FIELDS = {"title", "paths", "boundary"}
PATH_FIELDS = {"id", "title", "steps", "status", "fact_refs"}
HANDOFF_FIELDS = {"title", "body", "fact_refs"}
STATE_FIELDS = {
    "id",
    "nav_label",
    "title",
    "instruction",
    "principle_ids",
    "show_substation",
    "process_lane_ids",
    "abilene_path_ids",
    "show_handoff",
}


class TransmissionVisualError(base.TeachingVisualError):
    """Raised when Phase 2 escapes its teaching or evidence contract."""


def responsive_layout_contract(
    viewport_width: int,
    viewport_height: int,
) -> dict[str, Any]:
    """Select an SVG or readable payload-driven teaching surface."""
    if 901 <= viewport_width <= 1100:
        return {
            "surface": "html",
            "profile": "tablet",
            "family_columns": 2,
            "minimum_text_px": 12,
            "scroll_axis": "vertical",
        }
    return base.responsive_layout_contract(viewport_width, viewport_height)


def _exact(value: Any, fields: set[str], location: str) -> dict[str, Any]:
    try:
        return base._exact_fields(value, fields, location)
    except base.TeachingVisualError as error:
        raise TransmissionVisualError(str(error)) from error


def _text(value: Any, location: str, *, maximum: int = 240) -> str:
    try:
        return base._text(value, location, maximum=maximum)
    except base.TeachingVisualError as error:
        raise TransmissionVisualError(str(error)) from error


def _identifier(value: Any, location: str) -> str:
    try:
        return base._id(value, location)
    except base.TeachingVisualError as error:
        raise TransmissionVisualError(str(error)) from error


def _text_list(
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
        raise TransmissionVisualError(str(error)) from error


def _refs(
    value: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[str]:
    try:
        return base._fact_refs(value, location, ledgers)
    except base.TeachingVisualError as error:
        raise TransmissionVisualError(str(error)) from error


def _normalize_boundary(
    raw: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    value = _exact(raw, BOUNDARY_FIELDS, location)
    return {
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "body": _text(value["body"], f"{location}.body", maximum=600),
        "fact_refs": _refs(value["fact_refs"], f"{location}.fact_refs", ledgers),
    }


def _normalize_principles(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != 3:
        raise TransmissionVisualError(
            "pilot manifest.transmission_principles must contain exactly three principles"
        )
    principles: list[dict[str, Any]] = []
    ids: list[str] = []
    for index, record in enumerate(raw):
        location = f"pilot manifest.transmission_principles[{index}]"
        if not isinstance(record, dict):
            raise TransmissionVisualError(f"{location}: expected a mapping")
        principle_id = _identifier(record.get("id"), f"{location}.id")
        fields = (
            VOLTAGE_FIELDS if principle_id == "voltage_transfer" else PRINCIPLE_FIELDS
        )
        value = _exact(record, fields, location)
        normalized: dict[str, Any] = {
            "id": principle_id,
            "title": _text(value["title"], f"{location}.title", maximum=140),
            "body": _text(value["body"], f"{location}.body", maximum=520),
            "fact_refs": _refs(value["fact_refs"], f"{location}.fact_refs", ledgers),
        }
        if principle_id == "voltage_transfer":
            comparison = _exact(
                value["comparison"], COMPARISON_FIELDS, f"{location}.comparison"
            )
            normalized["comparison"] = {
                "fixed": _text(
                    comparison["fixed"], f"{location}.comparison.fixed", maximum=80
                ),
                "lower_voltage": {
                    field: _text(
                        _exact(
                            comparison["lower_voltage"],
                            COMPARISON_SIDE_FIELDS,
                            f"{location}.comparison.lower_voltage",
                        )[field],
                        f"{location}.comparison.lower_voltage.{field}",
                        maximum=100,
                    )
                    for field in sorted(COMPARISON_SIDE_FIELDS)
                },
                "higher_voltage": {
                    field: _text(
                        _exact(
                            comparison["higher_voltage"],
                            COMPARISON_SIDE_FIELDS,
                            f"{location}.comparison.higher_voltage",
                        )[field],
                        f"{location}.comparison.higher_voltage.{field}",
                        maximum=100,
                    )
                    for field in sorted(COMPARISON_SIDE_FIELDS)
                },
                "relation": _text(
                    comparison["relation"],
                    f"{location}.comparison.relation",
                    maximum=140,
                ),
            }
        elif principle_id == "meshed_ac_network":
            visual = _exact(value["visual"], MESH_VISUAL_FIELDS, f"{location}.visual")
            normalized["visual"] = {
                "source_labels": _text_list(
                    visual["source_labels"],
                    f"{location}.visual.source_labels",
                    minimum=2,
                    maximum=5,
                    item_limit=70,
                ),
                "network_labels": _text_list(
                    visual["network_labels"],
                    f"{location}.visual.network_labels",
                    minimum=3,
                    maximum=6,
                    item_limit=70,
                ),
                "load_labels": _text_list(
                    visual["load_labels"],
                    f"{location}.visual.load_labels",
                    minimum=2,
                    maximum=5,
                    item_limit=70,
                ),
                "path_posture": _identifier(
                    visual["path_posture"], f"{location}.visual.path_posture"
                ),
            }
        else:
            visual = _exact(
                value["visual"], BALANCE_VISUAL_FIELDS, f"{location}.visual"
            )
            normalized["visual"] = {
                field: _text(visual[field], f"{location}.visual.{field}", maximum=100)
                for field in sorted(BALANCE_VISUAL_FIELDS)
            }
        ids.append(principle_id)
        principles.append(normalized)
    if len(ids) != len(set(ids)) or set(ids) != PRINCIPLE_IDS:
        raise TransmissionVisualError(
            "pilot manifest principles must be the voltage, mesh, and balance set"
        )
    return principles


def _normalize_substation(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.substation_anatomy"
    value = _exact(raw, SUBSTATION_FIELDS, location)
    return {
        "title": _text(value["title"], f"{location}.title", maximum=150),
        "body": _text(value["body"], f"{location}.body", maximum=500),
        "functions": _text_list(
            value["functions"],
            f"{location}.functions",
            minimum=7,
            maximum=7,
            item_limit=90,
        ),
        "boundary": _text(value["boundary"], f"{location}.boundary", maximum=500),
        "fact_refs": _refs(value["fact_refs"], f"{location}.fact_refs", ledgers),
    }


def _normalize_processes(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.interconnection_processes"
    value = _exact(raw, PROCESS_FIELDS, location)
    if not isinstance(value["lanes"], list) or len(value["lanes"]) != 2:
        raise TransmissionVisualError(
            f"{location}.lanes must contain exactly two lanes"
        )
    lanes: list[dict[str, Any]] = []
    lane_ids: list[str] = []
    for index, raw_lane in enumerate(value["lanes"]):
        lane_location = f"{location}.lanes[{index}]"
        if not isinstance(raw_lane, dict):
            raise TransmissionVisualError(f"{lane_location}: expected a mapping")
        lane_id = _identifier(raw_lane.get("id"), f"{lane_location}.id")
        fields = (
            LOAD_LANE_FIELDS
            if lane_id == "ercot_large_load_integration"
            else GENERATOR_LANE_FIELDS
        )
        lane = _exact(raw_lane, fields, lane_location)
        normalized: dict[str, Any] = {
            "id": lane_id,
            "title": _text(lane["title"], f"{lane_location}.title", maximum=120),
            "subject": _text(lane["subject"], f"{lane_location}.subject", maximum=150),
            "gate": _text(lane["gate"], f"{lane_location}.gate", maximum=180),
            "body": _text(lane["body"], f"{lane_location}.body", maximum=520),
            "gates": _text_list(
                lane["gates"],
                f"{lane_location}.gates",
                minimum=4,
                maximum=7,
                item_limit=220,
            ),
            "boundary": _text(
                lane["boundary"], f"{lane_location}.boundary", maximum=420
            ),
            "fact_refs": _refs(
                lane["fact_refs"], f"{lane_location}.fact_refs", ledgers
            ),
        }
        if lane_id == "ercot_large_load_integration":
            status_location = f"{lane_location}.status_note"
            status = _exact(lane["status_note"], STATUS_NOTE_FIELDS, status_location)
            normalized["status_note"] = {
                "label": _text(
                    status["label"], f"{status_location}.label", maximum=120
                ),
                "body": _text(status["body"], f"{status_location}.body", maximum=720),
                "fact_refs": _refs(
                    status["fact_refs"], f"{status_location}.fact_refs", ledgers
                ),
            }
        lane_ids.append(lane_id)
        lanes.append(normalized)
    if len(lane_ids) != len(set(lane_ids)) or set(lane_ids) != PROCESS_LANE_IDS:
        raise TransmissionVisualError(
            "pilot manifest process lanes must be generator interconnection and ERCOT large load"
        )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "lanes": lanes,
        "case_boundary": _normalize_boundary(
            value["case_boundary"], f"{location}.case_boundary", ledgers
        ),
    }


def _normalize_abilene(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.abilene_case"
    value = _exact(raw, ABILENE_FIELDS, location)
    if not isinstance(value["paths"], list) or len(value["paths"]) != 2:
        raise TransmissionVisualError(
            f"{location}.paths must contain exactly two paths"
        )
    paths: list[dict[str, Any]] = []
    path_ids: list[str] = []
    for index, raw_path in enumerate(value["paths"]):
        path_location = f"{location}.paths[{index}]"
        path = _exact(raw_path, PATH_FIELDS, path_location)
        path_id = _identifier(path["id"], f"{path_location}.id")
        path_ids.append(path_id)
        paths.append(
            {
                "id": path_id,
                "title": _text(path["title"], f"{path_location}.title", maximum=130),
                "steps": _text_list(
                    path["steps"],
                    f"{path_location}.steps",
                    minimum=3,
                    maximum=6,
                    item_limit=150,
                ),
                "status": _text(path["status"], f"{path_location}.status", maximum=520),
                "fact_refs": _refs(
                    path["fact_refs"], f"{path_location}.fact_refs", ledgers
                ),
            }
        )
    if len(path_ids) != len(set(path_ids)) or set(path_ids) != ABILENE_PATH_IDS:
        raise TransmissionVisualError(
            "pilot manifest Abilene paths must be the initial 138 kV and expansion 345 kV paths"
        )
    return {
        "title": _text(value["title"], f"{location}.title", maximum=160),
        "paths": paths,
        "boundary": _normalize_boundary(
            value["boundary"], f"{location}.boundary", ledgers
        ),
    }


def _normalize_handoff(
    raw: Any,
    ledgers: Mapping[str, dict[str, Any]],
) -> dict[str, Any]:
    location = "pilot manifest.phase3_handoff"
    value = _exact(raw, HANDOFF_FIELDS, location)
    return {
        "title": _text(value["title"], f"{location}.title", maximum=150),
        "body": _text(value["body"], f"{location}.body", maximum=520),
        "fact_refs": _refs(value["fact_refs"], f"{location}.fact_refs", ledgers),
    }


def _normalize_states(
    raw: Any,
    *,
    principle_ids: set[str],
    process_lane_ids: set[str],
    abilene_path_ids: set[str],
) -> list[dict[str, Any]]:
    if not isinstance(raw, list) or len(raw) != len(STATE_IDS):
        raise TransmissionVisualError(
            f"pilot manifest.states must contain exactly {len(STATE_IDS)} states"
        )
    states: list[dict[str, Any]] = []
    ids: list[str] = []
    nav_labels: list[str] = []
    used_principles: set[str] = set()
    used_lanes: set[str] = set()
    used_paths: set[str] = set()
    for index, raw_state in enumerate(raw):
        location = f"pilot manifest.states[{index}]"
        state = _exact(raw_state, STATE_FIELDS, location)
        state_id = _identifier(state["id"], f"{location}.id")
        selected_principles = _text_list(
            state["principle_ids"],
            f"{location}.principle_ids",
            minimum=0,
            maximum=len(principle_ids),
            item_limit=80,
        )
        selected_lanes = _text_list(
            state["process_lane_ids"],
            f"{location}.process_lane_ids",
            minimum=0,
            maximum=len(process_lane_ids),
            item_limit=80,
        )
        selected_paths = _text_list(
            state["abilene_path_ids"],
            f"{location}.abilene_path_ids",
            minimum=0,
            maximum=len(abilene_path_ids),
            item_limit=80,
        )
        unknown_principles = sorted(set(selected_principles) - principle_ids)
        unknown_lanes = sorted(set(selected_lanes) - process_lane_ids)
        unknown_paths = sorted(set(selected_paths) - abilene_path_ids)
        if unknown_principles or unknown_lanes or unknown_paths:
            raise TransmissionVisualError(
                f"{location}: unknown principles={unknown_principles} "
                f"process_lanes={unknown_lanes} paths={unknown_paths}"
            )
        for flag in ("show_substation", "show_handoff"):
            if not isinstance(state[flag], bool):
                raise TransmissionVisualError(f"{location}.{flag} must be boolean")
        primary_layers = (
            bool(selected_principles),
            state["show_substation"],
            bool(selected_lanes),
            bool(selected_paths),
        )
        if sum(primary_layers) != 1:
            raise TransmissionVisualError(
                f"{location}: state must select exactly one primary teaching layer"
            )
        if state["show_handoff"] and set(selected_paths) != abilene_path_ids:
            raise TransmissionVisualError(
                f"{location}: handoff must retain both separate Abilene paths"
            )
        nav_label = _text(state["nav_label"], f"{location}.nav_label", maximum=24)
        ids.append(state_id)
        nav_labels.append(nav_label)
        used_principles.update(selected_principles)
        used_lanes.update(selected_lanes)
        used_paths.update(selected_paths)
        states.append(
            {
                "id": state_id,
                "nav_label": nav_label,
                "title": _text(state["title"], f"{location}.title", maximum=140),
                "instruction": _text(
                    state["instruction"], f"{location}.instruction", maximum=480
                ),
                "principle_ids": selected_principles,
                "show_substation": state["show_substation"],
                "process_lane_ids": selected_lanes,
                "abilene_path_ids": selected_paths,
                "show_handoff": state["show_handoff"],
            }
        )
    if ids != STATE_IDS:
        raise TransmissionVisualError(
            f"pilot manifest states must remain in canonical order {STATE_IDS}"
        )
    if len(nav_labels) != len(set(nav_labels)):
        raise TransmissionVisualError("pilot manifest state nav labels must be unique")
    if used_principles != principle_ids or used_lanes != process_lane_ids:
        raise TransmissionVisualError(
            "pilot states must use every authored principle and process lane"
        )
    if used_paths != abilene_path_ids:
        raise TransmissionVisualError("pilot states must use both Abilene paths")
    if not states[-1]["show_handoff"] or any(
        state["show_handoff"] for state in states[:-1]
    ):
        raise TransmissionVisualError(
            "only the final pilot state may reveal the Phase 3 handoff"
        )
    return states


def _collect_fact_refs(value: Any) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "fact_refs":
                refs.update(nested)
            else:
                refs.update(_collect_fact_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(_collect_fact_refs(nested))
    return refs


def compile_transmission_landscape(
    manifest: dict[str, Any],
    evidence_ledgers: Mapping[str, dict[str, Any]],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Validate and normalize the Phase 2 transmission teaching payload."""
    manifest = _exact(manifest, TOP_LEVEL_FIELDS, "pilot manifest")
    forbidden = base._forbidden_fields(manifest)
    if forbidden:
        raise TransmissionVisualError(
            f"pilot manifest contains pacing or scripting fields: {forbidden}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise TransmissionVisualError("pilot manifest schema_version must be 1")
    source_digest = base.validate_source_digest(source_digest)
    declared_ledgers, ledgers = base.validate_evidence_ledgers(
        manifest, evidence_ledgers
    )

    phase = _exact(manifest["phase"], PHASE_FIELDS, "pilot manifest.phase")
    if type(phase["number"]) is not int or phase["number"] != 2:
        raise TransmissionVisualError("pilot manifest.phase.number must be integer 2")
    interaction = base.validate_manual_interaction(
        manifest["interaction"], location="pilot manifest.interaction"
    )
    canvas = _exact(manifest["canvas"], CANVAS_FIELDS, "pilot manifest.canvas")
    if canvas["kind"] != CANVAS_KIND:
        raise TransmissionVisualError(
            f"pilot manifest.canvas.kind must be {CANVAS_KIND!r}"
        )
    if canvas["width"] != CANVAS_WIDTH or canvas["height"] != CANVAS_HEIGHT:
        raise TransmissionVisualError(
            f"pilot manifest.canvas must be {CANVAS_WIDTH} by {CANVAS_HEIGHT}"
        )
    contract = _exact(
        canvas["contract"], CONTRACT_FIELDS, "pilot manifest.canvas.contract"
    )
    expected_contract = {
        "state_selection": "exclusive_single_primary_layer",
        "primary_layers": [
            "transmission_principles",
            "substation_anatomy",
            "interconnection_processes",
            "abilene_case",
        ],
        "evidence_binding": "content_record_fact_refs",
        "geometry_owner": "transmission_landscape_renderer",
        "handoff_requires": "abilene_case",
    }
    if contract != expected_contract:
        raise TransmissionVisualError(
            "pilot manifest.canvas.contract must match transmission_landscape_v1"
        )

    principles = _normalize_principles(manifest["transmission_principles"], ledgers)
    substation = _normalize_substation(manifest["substation_anatomy"], ledgers)
    processes = _normalize_processes(manifest["interconnection_processes"], ledgers)
    abilene = _normalize_abilene(manifest["abilene_case"], ledgers)
    handoff = _normalize_handoff(manifest["phase3_handoff"], ledgers)
    states = _normalize_states(
        manifest["states"],
        principle_ids={record["id"] for record in principles},
        process_lane_ids={record["id"] for record in processes["lanes"]},
        abilene_path_ids={record["id"] for record in abilene["paths"]},
    )

    content = {
        "transmission_principles": principles,
        "substation_anatomy": substation,
        "interconnection_processes": processes,
        "abilene_case": abilene,
        "phase3_handoff": handoff,
    }
    evidence = base.compile_evidence_cards(
        _collect_fact_refs(content),
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
                "number": 2,
                "title": _text(
                    phase["title"], "pilot manifest.phase.title", maximum=100
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
                maximum=440,
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
        raise TransmissionVisualError(
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


def _voltage_svg(record: Mapping[str, Any]) -> str:
    comparison = record["comparison"]
    sides = (
        ("lower_voltage", 70, "LOWER VOLTAGE", "voltage-low", 13, 5),
        ("higher_voltage", 850, "HIGHER VOLTAGE", "voltage-high", 5, 2),
    )
    panels = []
    for side_id, x, heading, css_class, line_width, heat_count in sides:
        side = comparison[side_id]
        heat = "".join(
            f'<circle class="heat-dot" cx="{x + 250 + index * 38}" cy="395" r="8"/>'
            for index in range(heat_count)
        )
        panels.append(
            f'<g class="voltage-panel {css_class}">'
            f'<rect class="teaching-panel" x="{x}" y="118" width="680" height="640" rx="18"/>'
            f'<text class="panel-kicker" x="{x + 34}" y="164">{heading}</text>'
            f'<rect class="power-node" x="{x + 52}" y="294" width="150" height="92" rx="12"/>'
            f'<text class="node-label centered" x="{x + 127}" y="338">SOURCE</text>'
            f'<text class="node-detail centered" x="{x + 127}" y="363">fixed power</text>'
            f'<path class="power-conductor" style="stroke-width:{line_width}px" d="M {x + 202} 340 H {x + 478}"/>'
            f"{heat}"
            f'<rect class="power-node" x="{x + 478}" y="294" width="150" height="92" rx="12"/>'
            f'<text class="node-label centered" x="{x + 553}" y="338">LOAD</text>'
            f'<text class="node-detail centered" x="{x + 553}" y="363">same power</text>'
            f'<rect class="metric-card" x="{x + 48}" y="470" width="180" height="104" rx="10"/>'
            + _wrapped(
                str(side["voltage"]),
                x=x + 138,
                y=522,
                width_chars=18,
                line_height=20,
                css_class="metric-label centered",
                maximum_lines=2,
                center_lines=True,
            )
            + f'<rect class="metric-card" x="{x + 250}" y="470" width="180" height="104" rx="10"/>'
            + _wrapped(
                str(side["current"]),
                x=x + 340,
                y=522,
                width_chars=18,
                line_height=20,
                css_class="metric-label centered",
                maximum_lines=2,
                center_lines=True,
            )
            + f'<rect class="metric-card" x="{x + 452}" y="470" width="180" height="104" rx="10"/>'
            + _wrapped(
                str(side["conductor_loss"]),
                x=x + 542,
                y=512,
                width_chars=18,
                line_height=20,
                css_class="metric-label centered",
                maximum_lines=3,
                center_lines=True,
            )
            + f'<text class="equation centered" x="{x + 340}" y="674">P fixed · loss ∝ I²R</text>'
            + "</g>"
        )
    return (
        '<g data-principle-id="voltage_transfer" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record))}</desc>"
        f'<rect class="fixed-power-pill" x="585" y="42" width="430" height="54" rx="27"/>'
        f'<text class="fixed-power-label centered" x="800" y="76">{_escape(comparison["fixed"])}</text>'
        + "".join(panels)
        + '<rect class="relation-box" x="310" y="790" width="980" height="72" rx="12"/>'
        + f'<text class="relation-label centered" x="800" y="835">{_escape(comparison["relation"])}</text>'
        + "</g>"
    )


def _mesh_svg(record: Mapping[str, Any]) -> str:
    visual = record["visual"]
    sources = [(135, 210), (135, 420), (135, 630)]
    network = [(485, 180), (680, 360), (485, 610)]
    loads = [(1030, 270), (1030, 560)]
    lines = (
        (215, 210, 445, 180),
        (215, 210, 640, 360),
        (215, 420, 445, 180),
        (215, 420, 640, 360),
        (215, 420, 445, 610),
        (215, 630, 640, 360),
        (215, 630, 445, 610),
        (525, 180, 640, 360),
        (525, 610, 640, 360),
        (720, 360, 990, 270),
        (720, 360, 990, 560),
        (525, 180, 990, 270),
        (525, 610, 990, 560),
    )
    edges = "".join(
        f'<path class="mesh-edge" d="M {x1} {y1} L {x2} {y2}"/>'
        for x1, y1, x2, y2 in lines
    )

    def nodes(
        labels: list[str], coordinates: list[tuple[int, int]], css_class: str
    ) -> str:
        return "".join(
            f'<g><rect class="mesh-node {css_class}" x="{x - 80}" y="{y - 36}" width="160" height="72" rx="12"/>'
            + _wrapped(
                label,
                x=x,
                y=y + 5,
                width_chars=18,
                line_height=17,
                css_class="mesh-label centered",
                maximum_lines=2,
                center_lines=True,
            )
            + "</g>"
            for label, (x, y) in zip(labels, coordinates)
        )

    return (
        '<g data-principle-id="meshed_ac_network" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record))}</desc>"
        '<rect class="teaching-panel" x="42" y="42" width="1120" height="816" rx="18"/>'
        '<text class="panel-kicker" x="78" y="92">INTERCONNECTED AC NETWORK</text>'
        + _wrapped(
            str(record["title"]),
            x=78,
            y=132,
            width_chars=62,
            line_height=27,
            css_class="panel-title",
            maximum_lines=2,
        )
        + edges
        + nodes(list(visual["source_labels"]), sources, "source-node")
        + nodes(list(visual["network_labels"]), network, "network-node")
        + nodes(list(visual["load_labels"]), loads, "load-node")
        + '<rect class="network-boundary" x="100" y="724" width="1000" height="106" rx="10"/>'
        + _wrapped(
            str(record["body"]),
            x=130,
            y=758,
            width_chars=108,
            line_height=21,
            css_class="network-boundary-copy",
            maximum_lines=3,
        )
        + "</g>"
    )


def _balance_svg(record: Mapping[str, Any]) -> str:
    visual = record["visual"]
    return (
        '<g data-principle-id="continuous_system_balance" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record))}</desc>"
        '<rect class="balance-panel" x="1188" y="94" width="370" height="712" rx="18"/>'
        '<text class="panel-kicker centered" x="1373" y="146">SYSTEM OPERATION</text>'
        + _wrapped(
            str(record["title"]),
            x=1373,
            y=205,
            width_chars=29,
            line_height=26,
            css_class="balance-title centered",
            maximum_lines=3,
            center_lines=True,
        )
        + '<rect class="balance-node supply-node" x="1243" y="292" width="260" height="82" rx="12"/>'
        + f'<text class="node-label centered" x="1373" y="340">{_escape(visual["supply_label"])}</text>'
        + '<path class="balance-arrow" d="M 1373 384 V 440"/>'
        + '<rect class="operator-node" x="1243" y="445" width="260" height="92" rx="12"/>'
        + _wrapped(
            str(visual["operator_label"]),
            x=1373,
            y=494,
            width_chars=24,
            line_height=20,
            css_class="operator-label centered",
            maximum_lines=2,
            center_lines=True,
        )
        + '<path class="balance-arrow" d="M 1373 547 V 603"/>'
        + '<rect class="balance-node demand-node" x="1243" y="608" width="260" height="82" rx="12"/>'
        + f'<text class="node-label centered" x="1373" y="656">{_escape(visual["demand_label"])}</text>'
        + f'<text class="balance-relation centered" x="1373" y="746">{_escape(visual["relation"])}</text>'
        + "</g>"
    )


def _substation_svg(record: Mapping[str, Any]) -> str:
    functions = list(record["functions"])
    centers = [170, 380, 590, 800, 1010, 1220, 1430]
    cards = []
    for index, (label, x) in enumerate(zip(functions, centers)):
        y = 260 if index % 2 == 0 else 625
        line_y = 410
        card_y = y - 60
        connector_end = card_y + 120 if y < line_y else card_y
        cards.append(
            f'<path class="function-connector" d="M {x} {line_y} V {connector_end}"/>'
            f'<rect class="function-card" x="{x - 90}" y="{card_y}" width="180" height="120" rx="12"/>'
            f'<circle class="function-number" cx="{x}" cy="{card_y + 27}" r="16"/>'
            f'<text class="function-number-label centered" x="{x}" y="{card_y + 33}">{index + 1}</text>'
            + _wrapped(
                label,
                x=x,
                y=card_y + 78,
                width_chars=18,
                line_height=19,
                css_class="function-label centered",
                maximum_lines=3,
                center_lines=True,
            )
        )
    return (
        "<g data-substation hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record))}</desc>"
        '<rect class="teaching-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="panel-kicker" x="82" y="94">EXPLODED FUNCTIONAL ENVELOPE</text>'
        + _wrapped(
            str(record["title"]),
            x=82,
            y=136,
            width_chars=82,
            line_height=28,
            css_class="panel-title",
            maximum_lines=2,
        )
        + '<text class="line-label" x="82" y="386">INCOMING TRANSMISSION</text>'
        + '<path class="station-line" d="M 82 410 H 1518"/>'
        + '<path class="station-break" d="M 740 390 L 780 430 M 780 390 L 740 430"/>'
        + '<circle class="transformer-coil" cx="930" cy="410" r="30"/>'
        + '<circle class="transformer-coil" cx="980" cy="410" r="30"/>'
        + '<text class="line-label" x="1325" y="386">OUTGOING DELIVERY</text>'
        + "".join(cards)
        + '<rect class="boundary-box" x="240" y="758" width="1120" height="78" rx="10"/>'
        + _wrapped(
            str(record["boundary"]),
            x=800,
            y=802,
            width_chars=104,
            line_height=20,
            css_class="substation-boundary-copy centered",
            maximum_lines=2,
            center_lines=True,
        )
        + "</g>"
    )


def _process_lane_svg(record: Mapping[str, Any], *, x: int) -> str:
    gates = list(record["gates"])
    card_width = 650
    card_height = 60
    start_y = 225
    gap = 10
    gate_parts = []
    for index, gate in enumerate(gates):
        y = start_y + index * (card_height + gap)
        if index:
            gate_parts.append(
                f'<path class="gate-arrow" d="M {x + card_width / 2} {y - gap} V {y - 3}"/>'
            )
        gate_parts.append(
            f'<rect class="gate-card" x="{x}" y="{y}" width="{card_width}" height="{card_height}" rx="9"/>'
            f'<circle class="gate-number" cx="{x + 28}" cy="{y + 30}" r="16"/>'
            f'<text class="gate-number-label centered" x="{x + 28}" y="{y + 36}">{index + 1}</text>'
            + _wrapped(
                gate,
                x=x + 58,
                y=y + 28,
                width_chars=73,
                line_height=16,
                css_class="gate-label",
                maximum_lines=3,
                center_lines=True,
            )
        )
    end_y = start_y + len(gates) * (card_height + gap)
    footer_y = max(610, end_y + 4)
    if "status_note" in record:
        status = record["status_note"]
        footer = (
            f'<rect class="status-box" x="{x}" y="{footer_y}" width="{card_width}" height="132" rx="10"/>'
            f'<text class="status-label" x="{x + 20}" y="{footer_y + 27}">{_escape(status["label"])}</text>'
            + _wrapped(
                str(status["body"]),
                x=x + 20,
                y=footer_y + 54,
                width_chars=78,
                line_height=16,
                css_class="status-copy",
                maximum_lines=5,
            )
        )
    else:
        footer = (
            f'<rect class="lane-boundary-box" x="{x}" y="{footer_y}" width="{card_width}" height="104" rx="10"/>'
            '<text class="boundary-kicker" '
            f'x="{x + 20}" y="{footer_y + 27}">SCOPE BOUNDARY</text>'
            + _wrapped(
                str(record["boundary"]),
                x=x + 20,
                y=footer_y + 53,
                width_chars=78,
                line_height=17,
                css_class="lane-boundary-copy",
                maximum_lines=3,
            )
        )
    return (
        f'<g data-process-lane-id="{_escape(record["id"])}" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record))}</desc>"
        f'<rect class="process-lane" x="{x - 22}" y="80" width="694" height="690" rx="16"/>'
        f'<text class="lane-title" x="{x}" y="122">{_escape(record["title"])}</text>'
        f'<text class="lane-subject" x="{x}" y="151">{_escape(record["subject"])}</text>'
        + _wrapped(
            str(record["gate"]),
            x=x,
            y=183,
            width_chars=72,
            line_height=19,
            css_class="lane-gate",
            maximum_lines=2,
        )
        + "".join(gate_parts)
        + footer
        + "</g>"
    )


def _process_svg(record: Mapping[str, Any]) -> str:
    lanes = list(record["lanes"])
    boundary = record["case_boundary"]
    return (
        "<g data-processes hidden>"
        f"<title>{_escape(record['title'])}</title>"
        '<text class="process-title centered" x="800" y="52">'
        f"{_escape(record['title'])}</text>"
        + _process_lane_svg(lanes[0], x=70)
        + _process_lane_svg(lanes[1], x=880)
        + "<g data-process-boundary hidden>"
        + '<rect class="boundary-box" x="180" y="794" width="1240" height="72" rx="10"/>'
        + f'<text class="boundary-kicker" x="210" y="821">{_escape(boundary["title"])}</text>'
        + _wrapped(
            str(boundary["body"]),
            x=210,
            y=847,
            width_chars=132,
            line_height=17,
            css_class="boundary-copy",
            maximum_lines=2,
        )
        + "</g></g>"
    )


def _abilene_path_svg(record: Mapping[str, Any], *, y: int, css_class: str) -> str:
    steps = list(record["steps"])
    x0 = 70
    usable = 1160
    gap = 22
    box_width = (usable - gap * (len(steps) - 1)) / len(steps)
    center_y = y + 70
    parts = []
    for index, step in enumerate(steps):
        x = x0 + index * (box_width + gap)
        if index:
            parts.append(
                f'<path class="case-path-arrow {css_class}" d="M {x - gap} {center_y} H {x - 4}"/>'
            )
        parts.append(
            f'<rect class="case-path-step {css_class}" x="{x:.2f}" y="{y + 24}" width="{box_width:.2f}" height="92" rx="10"/>'
            + _wrapped(
                step,
                x=x + box_width / 2,
                y=center_y + 5,
                width_chars=max(12, int(box_width / 9)),
                line_height=18,
                css_class="case-path-label centered",
                maximum_lines=4,
                center_lines=True,
            )
        )
    parts.append(
        f'<path class="case-path-arrow {css_class}" d="M {x0 + usable} {center_y} H 1320"/>'
    )
    return (
        f'<g data-abilene-path-id="{_escape(record["id"])}" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['status'])} {_escape(_fact_description(record))}</desc>"
        f'<text class="case-path-title" x="70" y="{y}">{_escape(record["title"])}</text>'
        + "".join(parts)
        + f'<rect class="path-status" x="70" y="{y + 132}" width="1160" height="62" rx="9"/>'
        + _wrapped(
            str(record["status"]),
            x=92,
            y=y + 158,
            width_chars=122,
            line_height=17,
            css_class="path-status-copy",
            maximum_lines=2,
        )
        + "</g>"
    )


def _abilene_svg(record: Mapping[str, Any]) -> str:
    paths = {path["id"]: path for path in record["paths"]}
    boundary = record["boundary"]
    return (
        "<g data-abilene-case hidden>"
        f"<title>{_escape(record['title'])}</title>"
        '<rect class="teaching-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="panel-kicker" x="72" y="88">ABILENE APPLICATION · PATHS REMAIN SEPARATE</text>'
        + _wrapped(
            str(record["title"]),
            x=72,
            y=126,
            width_chars=76,
            line_height=27,
            css_class="panel-title",
            maximum_lines=2,
        )
        + '<rect class="campus-boundary" x="1320" y="156" width="190" height="454" rx="12"/>'
        + '<text class="boundary-vertical centered" x="1415" y="255">CAMPUS</text>'
        + '<text class="boundary-vertical centered" x="1415" y="288">ELECTRICAL</text>'
        + '<text class="boundary-vertical centered" x="1415" y="321">BOUNDARY</text>'
        + '<text class="boundary-stop centered" x="1415" y="400">PATH 1 STOPS</text>'
        + '<text class="boundary-stop centered" x="1415" y="495">PATH 2 STOPS</text>'
        + '<text class="boundary-stop centered" x="1415" y="565">NO MERGE DRAWN</text>'
        + _abilene_path_svg(paths["initial_138"], y=178, css_class="initial-path")
        + _abilene_path_svg(paths["expansion_345"], y=418, css_class="expansion-path")
        + '<rect class="boundary-box" x="72" y="660" width="1438" height="112" rx="10"/>'
        + f'<text class="boundary-kicker" x="102" y="692">{_escape(boundary["title"])}</text>'
        + _wrapped(
            str(boundary["body"]),
            x=102,
            y=723,
            width_chars=145,
            line_height=20,
            css_class="boundary-copy",
            maximum_lines=3,
        )
        + "</g>"
    )


def _handoff_svg(
    record: Mapping[str, Any],
    abilene_case: Mapping[str, Any],
) -> str:
    paths = {path["id"]: path for path in abilene_case["paths"]}
    questions = (
        "How does power fan out to buildings?",
        "Which resilience layer protects each load?",
        "What campus voltages and switching exist?",
    )
    question_cards = []
    for index, (question, y) in enumerate(zip(questions, (285, 455, 625))):
        question_cards.append(
            f'<circle class="handoff-question-node" cx="875" cy="{y}" r="34"/>'
            f'<text class="handoff-question-mark centered" x="875" y="{y + 10}">?</text>'
            f'<path class="handoff-fan-line" d="M 915 {y} H 1018"/>'
            f'<path class="generic-building" d="M 1030 {y + 48} V {y - 48} '
            f'L 1070 {y - 82} L 1110 {y - 48} V {y + 48} Z"/>'
            f'<rect class="generic-building-card" x="1132" y="{y - 58}" width="350" height="116" rx="12"/>'
            f'<text class="generic-building-number" x="1160" y="{y - 25}">QUESTION {index + 1}</text>'
            + _wrapped(
                question,
                x=1160,
                y=y + 8,
                width_chars=36,
                line_height=21,
                css_class="generic-question-title",
                maximum_lines=2,
            )
        )
    return (
        "<g data-handoff hidden>"
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record))}</desc>"
        '<rect class="handoff-panel" x="42" y="42" width="1516" height="816" rx="18"/>'
        '<text class="handoff-kicker" x="82" y="90">NEXT · PHASE 3</text>'
        + _wrapped(
            str(record["title"]),
            x=82,
            y=132,
            width_chars=76,
            line_height=29,
            css_class="handoff-title",
            maximum_lines=2,
        )
        + '<text class="handoff-side-label" x="82" y="204">EVIDENCED GRID PATHS STOP</text>'
        + '<rect class="handoff-source-card" x="82" y="232" width="420" height="126" rx="12"/>'
        + _wrapped(
            str(paths["initial_138"]["title"]),
            x=112,
            y=282,
            width_chars=39,
            line_height=23,
            css_class="handoff-source-title",
            maximum_lines=2,
        )
        + '<path class="handoff-stop-line" d="M 502 295 H 590"/>'
        + '<rect class="handoff-source-card" x="82" y="482" width="420" height="126" rx="12"/>'
        + _wrapped(
            str(paths["expansion_345"]["title"]),
            x=112,
            y=532,
            width_chars=39,
            line_height=23,
            css_class="handoff-source-title",
            maximum_lines=2,
        )
        + '<path class="handoff-stop-line" d="M 502 545 H 590"/>'
        + '<rect class="handoff-campus-boundary" x="590" y="190" width="200" height="548" rx="14"/>'
        + '<text class="handoff-boundary-label centered" x="690" y="350">UNRESOLVED</text>'
        + '<text class="handoff-boundary-label centered" x="690" y="384">CAMPUS</text>'
        + '<text class="handoff-boundary-label centered" x="690" y="418">BOUNDARY</text>'
        + '<text class="handoff-boundary-stop centered" x="690" y="480">PATHS STOP HERE</text>'
        + '<text class="handoff-boundary-stop centered" x="690" y="512">NO MERGE ASSUMED</text>'
        + '<text class="handoff-side-label" x="842" y="204">GENERIC PHASE 3 QUESTIONS · NOT ABILENE TOPOLOGY</text>'
        + "".join(question_cards)
        + '<rect class="handoff-scope" x="842" y="718" width="640" height="116" rx="10"/>'
        + _wrapped(
            str(record["body"]),
            x=862,
            y=748,
            width_chars=72,
            line_height=18,
            css_class="handoff-scope-copy",
            maximum_lines=4,
        )
        + "</g>"
    )


def _responsive_voltage(record: Mapping[str, Any]) -> str:
    comparison = record["comparison"]
    sides = []
    for side_id, heading in (
        ("lower_voltage", "Lower voltage"),
        ("higher_voltage", "Higher voltage"),
    ):
        side = comparison[side_id]
        sides.append(
            '<div class="responsive-voltage-side">'
            f"<strong>{_escape(heading)}</strong>"
            '<div class="responsive-power-flow" role="img" '
            f'aria-label="{_escape(heading)} fixed-power transfer">'
            '<span class="responsive-node">Source</span>'
            '<span class="responsive-line" aria-hidden="true">→</span>'
            '<span class="responsive-node">Load</span>'
            "</div><ul>"
            f"<li>{_escape(side['voltage'])}</li>"
            f"<li>{_escape(side['current'])}</li>"
            f"<li>{_escape(side['conductor_loss'])}</li>"
            "</ul></div>"
        )
    return (
        '<article class="responsive-card responsive-voltage" '
        'data-principle-id="voltage_transfer" hidden>'
        f'<p class="responsive-kicker">{_escape(comparison["fixed"])}</p>'
        f"<h3>{_escape(record['title'])}</h3>"
        '<div class="responsive-voltage-grid">'
        + "".join(sides)
        + '</div><p class="responsive-relation">'
        f"{_escape(comparison['relation'])} · P fixed · loss ∝ I²R</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_mesh(record: Mapping[str, Any]) -> str:
    visual = record["visual"]
    return (
        '<article class="responsive-card responsive-mesh" '
        'data-principle-id="meshed_ac_network" hidden>'
        '<p class="responsive-kicker">Interconnected AC network</p>'
        f"<h3>{_escape(record['title'])}</h3>"
        '<div class="responsive-network" role="img" aria-label="Multiple possible paths from generators through transmission nodes to loads">'
        "<div><strong>Sources</strong><span>"
        + _escape(" · ".join(visual["source_labels"]))
        + '</span></div><div class="network-center"><strong>Meshed network</strong><span>'
        + _escape(" · ".join(visual["network_labels"]))
        + "</span></div><div><strong>Loads</strong><span>"
        + _escape(" · ".join(visual["load_labels"]))
        + "</span></div></div>"
        f'<p class="responsive-body">{_escape(record["body"])}</p>'
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_balance(record: Mapping[str, Any]) -> str:
    visual = record["visual"]
    return (
        '<article class="responsive-card responsive-balance" '
        'data-principle-id="continuous_system_balance" hidden>'
        '<p class="responsive-kicker">System operation</p>'
        f"<h3>{_escape(record['title'])}</h3>"
        '<div class="responsive-balance-flow" role="img" '
        'aria-label="Aggregate generation coordinated by the balancing authority with aggregate load">'
        f'<span class="responsive-node">{_escape(visual["supply_label"])}</span>'
        '<span aria-hidden="true">↕</span>'
        f'<span class="responsive-node operator-responsive-node">{_escape(visual["operator_label"])}</span>'
        '<span aria-hidden="true">↕</span>'
        f'<span class="responsive-node">{_escape(visual["demand_label"])}</span>'
        "</div>"
        f'<p class="responsive-body">{_escape(record["body"])}</p>'
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_substation(record: Mapping[str, Any]) -> str:
    functions = "".join(
        f"<li><span>{index + 1}</span>{_escape(label)}</li>"
        for index, label in enumerate(record["functions"])
    )
    return (
        '<article class="responsive-card responsive-substation" data-substation hidden>'
        '<p class="responsive-kicker">Exploded functional envelope</p>'
        f"<h3>{_escape(record['title'])}</h3>"
        f'<p class="responsive-body">{_escape(record["body"])}</p>'
        f'<ol class="responsive-function-grid">{functions}</ol>'
        '<div class="responsive-boundary"><strong>Generic boundary</strong>'
        f"<p>{_escape(record['boundary'])}</p></div>"
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_process_lane(record: Mapping[str, Any]) -> str:
    gates = "".join(f"<li>{_escape(gate)}</li>" for gate in record["gates"])
    status = ""
    if "status_note" in record:
        note = record["status_note"]
        status = (
            '<div class="responsive-status">'
            f"<strong>{_escape(note['label'])}</strong>"
            f"<p>{_escape(note['body'])}</p>"
            f'<span class="visually-hidden">{_escape(_fact_description(note))}</span>'
            "</div>"
        )
    return (
        '<article class="responsive-card responsive-process-lane" '
        f'data-process-lane-id="{_escape(record["id"])}" hidden>'
        f"<h3>{_escape(record['title'])}</h3>"
        f'<p class="responsive-subject">{_escape(record["subject"])}</p>'
        f'<p class="responsive-gate">{_escape(record["gate"])}</p>'
        f'<ol class="responsive-gates">{gates}</ol>'
        + status
        + '<div class="responsive-boundary"><strong>Scope boundary</strong>'
        f"<p>{_escape(record['boundary'])}</p></div>"
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_processes(record: Mapping[str, Any]) -> str:
    boundary = record["case_boundary"]
    lanes = "".join(_responsive_process_lane(lane) for lane in record["lanes"])
    return (
        '<section class="responsive-processes" data-processes hidden>'
        f'<h2 class="visually-hidden">{_escape(record["title"])}</h2>'
        '<div class="responsive-process-grid">'
        + lanes
        + '</div><div class="responsive-boundary responsive-process-boundary" data-process-boundary hidden>'
        f"<strong>{_escape(boundary['title'])}</strong>"
        f"<p>{_escape(boundary['body'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(boundary))}</span>'
        "</div></section>"
    )


def _responsive_path(record: Mapping[str, Any]) -> str:
    stages = []
    for index, step in enumerate(record["steps"]):
        if index:
            stages.append('<span class="responsive-arrow" aria-hidden="true">→</span>')
        stages.append(f'<span class="responsive-stage">{_escape(step)}</span>')
    return (
        '<article class="responsive-card responsive-path" '
        f'data-abilene-path-id="{_escape(record["id"])}" hidden>'
        f"<h3>{_escape(record['title'])}</h3>"
        '<div class="responsive-path-flow" role="img" '
        f'aria-label="{_escape(" to ".join(record["steps"]))}">'
        + "".join(stages)
        + '<span class="responsive-stop">STOP AT CAMPUS BOUNDARY</span></div>'
        f'<p class="responsive-status-copy">{_escape(record["status"])}</p>'
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</article>"
    )


def _responsive_abilene(record: Mapping[str, Any]) -> str:
    boundary = record["boundary"]
    return (
        '<section class="responsive-abilene" data-abilene-case hidden>'
        '<p class="responsive-kicker">Abilene application · paths remain separate</p>'
        f"<h2>{_escape(record['title'])}</h2>"
        '<div class="responsive-path-grid">'
        + "".join(_responsive_path(path) for path in record["paths"])
        + '</div><div class="responsive-boundary">'
        f"<strong>{_escape(boundary['title'])}</strong>"
        f"<p>{_escape(boundary['body'])}</p>"
        f'<span class="visually-hidden">{_escape(_fact_description(boundary))}</span>'
        "</div></section>"
    )


def _responsive_handoff(
    record: Mapping[str, Any],
    abilene_case: Mapping[str, Any],
) -> str:
    paths = {path["id"]: path for path in abilene_case["paths"]}
    return (
        '<div class="responsive-handoff" data-handoff hidden>'
        "<span>Next · Phase 3</span>"
        f"<strong>{_escape(record['title'])} →</strong>"
        f"<p>{_escape(record['body'])}</p>"
        '<div class="responsive-handoff-diagram" role="img" '
        'aria-label="Two evidenced grid paths stop at an unresolved campus boundary; generic question-marked building distribution begins on the other side">'
        '<div class="responsive-handoff-inbound">'
        f"<span>{_escape(paths['initial_138']['title'])} <b>STOP</b></span>"
        f"<span>{_escape(paths['expansion_345']['title'])} <b>STOP</b></span>"
        '</div><div class="responsive-campus-boundary">UNRESOLVED CAMPUS BOUNDARY<br><b>NO MERGE ASSUMED</b></div>'
        '<ul class="responsive-phase3-questions">'
        "<li><b>?</b> How does power fan out to buildings?</li>"
        "<li><b>?</b> Which resilience layer protects each load?</li>"
        "<li><b>?</b> What campus voltages and switching exist?</li>"
        "</ul></div>"
        "<small>Generic questions · not Abilene as-built topology</small>"
        f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        "</div>"
    )


def _responsive_visual(payload: Mapping[str, Any]) -> str:
    principles = {record["id"]: record for record in payload["transmission_principles"]}
    return (
        '<section class="responsive-visual" aria-label="Responsive transmission teaching surface">'
        + _responsive_voltage(principles["voltage_transfer"])
        + '<div class="responsive-network-grid">'
        + _responsive_mesh(principles["meshed_ac_network"])
        + _responsive_balance(principles["continuous_system_balance"])
        + "</div>"
        + _responsive_substation(payload["substation_anatomy"])
        + _responsive_processes(payload["interconnection_processes"])
        + _responsive_handoff(payload["phase3_handoff"], payload["abilene_case"])
        + _responsive_abilene(payload["abilene_case"])
        + "</section>"
    )


def render_transmission_landscape(payload: dict[str, Any]) -> str:
    """Render one compiled Phase 2 pilot as a self-contained HTML page."""
    if payload.get("canvas", {}).get("kind") != CANVAS_KIND:
        raise TransmissionVisualError("render payload is not a transmission landscape")
    principles = {record["id"]: record for record in payload["transmission_principles"]}
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
  header {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(300px,560px); gap:20px; padding:11px 20px 10px; border-bottom:1.5px solid var(--ink); }}
  .eyebrow,.phase-question,.state-number,.fact-ref,.panel-kicker,.boundary-kicker,.handoff-kicker,.responsive-kicker,.status-label {{ text-transform:uppercase; letter-spacing:.08em; font-size:11px; font-weight:750; }}
  h1 {{ margin:3px 0; font-size:clamp(21px,2.2vw,34px); line-height:1.05; }}
  header p {{ margin:2px 0; line-height:1.3; }}
  .objective {{ align-self:end; color:var(--muted); font-size:13px; }}
  main {{ min-width:0; min-height:0; display:grid; place-items:center; overflow:hidden; padding:8px 14px; }}
  .visual-shell {{ width:100%; height:100%; min-width:0; min-height:0; max-width:1600px; max-height:900px; border:1.5px solid var(--ink); background:white; }}
  svg {{ display:block; width:100%; height:100%; }}
  .centered {{ text-anchor:middle; }}
  .teaching-panel,.process-lane {{ fill:#fff; stroke:var(--ink); stroke-width:2; }}
  .panel-title,.process-title {{ font-size:26px; font-weight:760; }}
  .balance-title {{ font-size:22px; font-weight:760; }}
  .panel-kicker {{ fill:var(--blue); }}
  .fixed-power-pill {{ fill:var(--ink); }}
  .fixed-power-label {{ fill:white; font-size:18px; font-weight:750; letter-spacing:.05em; }}
  .power-node,.metric-card {{ fill:#fff; stroke:var(--blue); stroke-width:2; }}
  .voltage-low .power-conductor {{ stroke:var(--red); }}
  .voltage-high .power-conductor {{ stroke:var(--blue); }}
  .power-conductor {{ fill:none; marker-end:url(#arrow-blue); }}
  .voltage-low .power-conductor {{ marker-end:url(#arrow-red); }}
  .heat-dot {{ fill:var(--red); opacity:.75; }}
  .node-label,.metric-label {{ font-size:17px; font-weight:720; }}
  .node-detail {{ font-size:13px; fill:var(--muted); }}
  .panel-kicker {{ font-size:14px; }}
  .equation {{ font-size:24px; font-weight:750; fill:var(--muted); }}
  .relation-box {{ fill:var(--blue); }}
  .relation-label {{ fill:white; font-size:23px; font-weight:760; }}
  .mesh-edge {{ fill:none; stroke:var(--blue); stroke-width:3; opacity:.45; }}
  .mesh-node {{ stroke-width:2; }}
  .source-node {{ fill:var(--green-soft); stroke:var(--green); }}
  .network-node {{ fill:var(--blue-soft); stroke:var(--blue); }}
  .load-node {{ fill:var(--amber-soft); stroke:var(--amber); }}
  .mesh-label {{ font-size:14px; font-weight:700; }}
  .network-boundary {{ fill:var(--paper); stroke:var(--faint); stroke-width:1.5; }}
  .network-boundary-copy {{ font-size:15px; fill:var(--muted); }}
  .balance-panel {{ fill:var(--paper); stroke:var(--blue); stroke-width:2; }}
  .balance-node {{ fill:white; stroke:var(--blue); stroke-width:2; }}
  .operator-node {{ fill:var(--ink); stroke:var(--ink); }}
  .operator-label {{ fill:white; font-size:18px; font-weight:740; }}
  .balance-arrow {{ fill:none; stroke:var(--blue); stroke-width:3; marker-end:url(#arrow-blue); }}
  .balance-relation {{ fill:var(--blue); font-size:18px; font-weight:740; }}
  .station-line {{ fill:none; stroke:var(--blue); stroke-width:8; }}
  .station-break {{ fill:none; stroke:var(--amber); stroke-width:5; }}
  .transformer-coil {{ fill:none; stroke:var(--blue); stroke-width:4; }}
  .line-label {{ font-size:13px; font-weight:740; fill:var(--muted); letter-spacing:.05em; }}
  .function-connector {{ fill:none; stroke:var(--faint); stroke-width:2; }}
  .function-card {{ fill:var(--paper); stroke:var(--ink); stroke-width:1.7; }}
  .function-number {{ fill:var(--blue); }}
  .function-number-label {{ fill:white; font-size:12px; font-weight:760; }}
  .function-label {{ font-size:15px; font-weight:700; }}
  .lane-title {{ font-size:23px; font-weight:760; }}
  .lane-subject {{ font-size:13px; font-weight:700; fill:var(--blue); }}
  .lane-gate {{ font-size:15px; fill:var(--muted); }}
  .gate-card {{ fill:var(--paper); stroke:var(--blue); stroke-width:1.7; }}
  .gate-number {{ fill:var(--blue); }}
  .gate-number-label {{ fill:white; font-size:12px; font-weight:760; }}
  .gate-label {{ font-size:13px; font-weight:650; }}
  .gate-arrow {{ fill:none; stroke:var(--blue); stroke-width:2.4; marker-end:url(#arrow-blue-small); }}
  .status-box {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:2; }}
  .status-label,.boundary-kicker {{ fill:var(--amber); }}
  .status-copy,.lane-boundary-copy,.boundary-copy {{ font-size:13px; fill:var(--muted); }}
  .substation-boundary-copy {{ font-size:16px; fill:var(--muted); }}
  .lane-boundary-box,.boundary-box {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.7; }}
  .case-path-title {{ font-size:19px; font-weight:760; }}
  .case-path-step {{ fill:white; stroke-width:2.2; }}
  .case-path-step.initial-path {{ stroke:var(--blue); }}
  .case-path-step.expansion-path {{ stroke:var(--green); }}
  .case-path-arrow {{ fill:none; stroke-width:3.2; }}
  .case-path-arrow.initial-path {{ stroke:var(--blue); marker-end:url(#arrow-blue); }}
  .case-path-arrow.expansion-path {{ stroke:var(--green); marker-end:url(#arrow-green); }}
  .case-path-label {{ font-size:14px; font-weight:700; }}
  .path-status {{ fill:var(--paper); stroke:var(--faint); stroke-width:1.4; }}
  .path-status-copy {{ font-size:13px; fill:var(--muted); }}
  .campus-boundary {{ fill:var(--ink); stroke:var(--ink); }}
  .boundary-vertical {{ fill:white; font-size:19px; font-weight:780; letter-spacing:.05em; }}
  .boundary-stop {{ fill:#d9d9d4; font-size:11px; font-weight:720; letter-spacing:.05em; }}
  .handoff-panel {{ fill:white; stroke:var(--ink); stroke-width:2; }}
  .handoff-kicker {{ fill:var(--blue); }}
  .handoff-title {{ fill:var(--ink); font-size:28px; font-weight:760; }}
  .handoff-side-label {{ fill:var(--muted); font-size:13px; font-weight:760; letter-spacing:.06em; }}
  .handoff-source-card {{ fill:var(--paper); stroke:var(--blue); stroke-width:2; }}
  .handoff-source-title {{ font-size:18px; font-weight:730; }}
  .handoff-stop-line {{ fill:none; stroke:var(--red); stroke-width:5; }}
  .handoff-campus-boundary {{ fill:var(--ink); stroke:var(--ink); }}
  .handoff-boundary-label {{ fill:white; font-size:25px; font-weight:780; letter-spacing:.04em; }}
  .handoff-boundary-stop {{ fill:#d9d9d4; font-size:12px; font-weight:740; letter-spacing:.04em; }}
  .handoff-question-node {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:2.5; }}
  .handoff-question-mark {{ fill:var(--amber); font-size:31px; font-weight:800; }}
  .handoff-fan-line {{ fill:none; stroke:var(--amber); stroke-width:3; stroke-dasharray:8 7; }}
  .generic-building {{ fill:var(--blue-soft); stroke:var(--blue); stroke-width:2; }}
  .generic-building-card {{ fill:var(--paper); stroke:var(--faint); stroke-width:1.7; }}
  .generic-building-number {{ fill:var(--blue); font-size:11px; font-weight:760; letter-spacing:.06em; }}
  .generic-question-title {{ font-size:17px; font-weight:720; }}
  .handoff-scope {{ fill:var(--amber-soft); stroke:var(--amber); stroke-width:1.5; }}
  .handoff-scope-copy {{ fill:var(--muted); font-size:13px; }}
  footer {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(320px,570px); gap:10px 16px; min-height:0; max-height:48dvh; padding:9px 14px 10px; border-top:1.5px solid var(--ink); }}
  .state-nav {{ display:grid; grid-template-columns:repeat({len(payload["states"])},minmax(0,1fr)); gap:6px; }}
  .state-button {{ display:grid; grid-template-columns:auto 1fr; gap:7px; align-items:center; min-width:0; min-height:44px; padding:7px 8px; border:1.5px solid var(--ink); background:transparent; color:inherit; text-align:left; font:inherit; cursor:pointer; }}
  .state-nav-label {{ overflow:visible; text-overflow:clip; white-space:normal; }}
  .state-button[aria-selected="true"] {{ background:var(--ink); color:white; }}
  .state-copy {{ min-width:0; align-self:center; }}
  .state-copy h2 {{ margin:0 0 3px; font-size:16px; }}
  .state-copy p {{ margin:0; color:var(--muted); font-size:13px; line-height:1.3; }}
  details {{ grid-column:1/-1; min-height:0; border-top:1px solid var(--faint); padding-top:6px; }}
  details[open] {{ max-height:min(34dvh,320px); overflow:auto; overscroll-behavior:contain; }}
  summary {{ position:sticky; top:0; z-index:2; cursor:pointer; padding:3px 0; background:var(--paper); font-weight:700; }}
  .fact-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:12px; margin-bottom:0; padding:0; list-style:none; }}
  .fact-card {{ min-width:0; border:1px solid var(--faint); padding:10px 12px; background:white; }}
  .fact-card p {{ margin:5px 0; line-height:1.35; }}
  .fact-ref,.fact-boundary {{ overflow-wrap:anywhere; word-break:break-word; color:var(--muted); font-size:11px; }}
  .fact-sources {{ min-width:0; overflow-wrap:anywhere; word-break:break-word; font-size:12px; }}
  a {{ overflow-wrap:anywhere; word-break:break-word; color:var(--blue); }}
  .visually-hidden {{ position:absolute !important; width:1px; height:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }}
  .responsive-visual {{ display:none; }}
  .responsive-card {{ min-width:0; border:1.5px solid var(--ink); border-radius:9px; background:white; }}
  .responsive-card h3,.responsive-abilene h2 {{ margin:0; line-height:1.15; }}
  .responsive-card p,.responsive-abilene p {{ margin:0; }}
  .responsive-kicker {{ color:var(--blue); }}
  .responsive-voltage-grid,.responsive-network-grid,.responsive-process-grid,.responsive-path-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); }}
  .responsive-voltage-side {{ border:1px solid var(--faint); border-radius:7px; }}
  .responsive-power-flow,.responsive-path-flow {{ display:flex; align-items:center; }}
  .responsive-node,.responsive-stage,.responsive-stop {{ display:inline-grid; place-items:center; min-width:0; border:1.5px solid var(--blue); border-radius:6px; background:white; text-align:center; font-weight:700; line-height:1.1; }}
  .responsive-line,.responsive-arrow {{ flex:0 0 auto; color:var(--blue); font-weight:800; }}
  .responsive-relation {{ border-radius:7px; background:var(--blue); color:white; font-weight:740; text-align:center; }}
  .responsive-network {{ display:grid; grid-template-columns:1fr 1.2fr 1fr; align-items:center; }}
  .responsive-network > div {{ display:grid; border:1px solid var(--faint); border-radius:7px; text-align:center; }}
  .responsive-network .network-center {{ border-color:var(--blue); background:var(--blue-soft); }}
  .responsive-network span {{ color:var(--muted); }}
  .responsive-balance-flow {{ display:flex; align-items:center; justify-content:center; }}
  .operator-responsive-node {{ background:var(--ink); color:white; border-color:var(--ink); }}
  .responsive-function-grid,.responsive-gates {{ margin:0; padding:0; list-style:none; }}
  .responsive-function-grid {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); }}
  .responsive-function-grid li,.responsive-gates li {{ border:1px solid var(--faint); border-radius:6px; background:var(--paper); }}
  .responsive-function-grid span {{ display:inline-grid; place-items:center; border-radius:50%; background:var(--blue); color:white; font-weight:750; }}
  .responsive-gates {{ counter-reset:gate; display:grid; }}
  .responsive-gates li {{ counter-increment:gate; display:grid; grid-template-columns:auto 1fr; align-items:center; }}
  .responsive-gates li::before {{ content:counter(gate); display:inline-grid; place-items:center; border-radius:50%; background:var(--blue); color:white; font-weight:750; }}
  .responsive-subject,.responsive-gate {{ color:var(--muted); }}
  .responsive-status {{ border:1.5px solid var(--amber); border-radius:7px; background:var(--amber-soft); }}
  .responsive-status strong,.responsive-boundary strong {{ color:var(--amber); }}
  .responsive-boundary {{ border:1.5px solid var(--amber); border-radius:7px; background:var(--amber-soft); }}
  .responsive-stop {{ border-color:var(--ink); background:var(--ink); color:white; }}
  .responsive-status-copy {{ color:var(--muted); }}
  .responsive-handoff {{ border:1.5px solid var(--ink); border-radius:8px; background:white; color:var(--ink); }}
  .responsive-handoff > span:first-child {{ color:var(--blue); text-transform:uppercase; letter-spacing:.06em; font-weight:760; }}
  .responsive-handoff > p {{ color:var(--muted); }}
  .responsive-handoff-diagram {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(150px,.55fr) minmax(0,1fr); align-items:stretch; }}
  .responsive-handoff-inbound,.responsive-phase3-questions {{ display:grid; gap:6px; margin:0; padding:0; list-style:none; }}
  .responsive-handoff-inbound span,.responsive-phase3-questions li {{ display:grid; align-items:center; border:1px solid var(--faint); border-radius:6px; background:var(--paper); }}
  .responsive-handoff-inbound b {{ color:var(--red); }}
  .responsive-campus-boundary {{ display:grid; place-items:center; padding:8px; background:var(--ink); color:white; text-align:center; font-weight:760; }}
  .responsive-campus-boundary b {{ color:#d9d9d4; }}
  .responsive-phase3-questions b {{ color:var(--amber); font-size:1.4em; }}
  .responsive-handoff small {{ display:block; color:var(--amber); font-weight:740; }}
  @media (max-width:1300px) and (min-width:1101px) {{
    .state-nav {{ gap:4px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; padding:4px; text-align:center; font-size:11px; }}
  }}
  @media (max-width:1100px) and (min-width:901px) {{
    .state-nav {{ gap:4px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; padding:4px; text-align:center; font-size:11px; }}
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; }}
    .visual-shell {{ display:none; }}
    .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:6px; font-size:12px; }}
    .responsive-card,.responsive-abilene,.responsive-handoff {{ padding:10px; }}
    .responsive-card h3,.responsive-abilene h2 {{ margin-bottom:6px; font-size:17px; }}
    .responsive-body,.responsive-subject,.responsive-gate,.responsive-status-copy {{ margin-bottom:7px !important; color:var(--muted); font-size:12px; line-height:1.4; }}
    .responsive-voltage-grid,.responsive-network-grid,.responsive-process-grid,.responsive-path-grid {{ gap:10px; }}
    .responsive-voltage-side,.responsive-network > div,.responsive-status,.responsive-boundary {{ padding:8px; font-size:12px; }}
    .responsive-power-flow,.responsive-path-flow,.responsive-balance-flow {{ gap:5px; margin-top:6px; }}
    .responsive-path-flow {{ flex-direction:column; align-items:stretch; }}
    .responsive-path .responsive-arrow {{ align-self:center; transform:rotate(90deg); }}
    .responsive-path .responsive-stop {{ flex:1 1 auto; }}
    .responsive-node,.responsive-stage,.responsive-stop {{ min-height:36px; padding:6px; font-size:12px; }}
    .responsive-relation {{ margin-top:7px !important; padding:7px; font-size:12px; }}
    .responsive-network {{ gap:6px; }}
    .responsive-function-grid {{ gap:5px; }}
    .responsive-function-grid li {{ display:flex; align-items:center; gap:5px; padding:6px; font-size:12px; }}
    .responsive-function-grid span {{ flex:0 0 22px; height:22px; }}
    .responsive-gates {{ gap:5px; margin-top:6px; }}
    .responsive-gates li {{ grid-template-columns:24px 1fr; gap:6px; min-height:38px; padding:6px; font-size:12px; line-height:1.3; }}
    .responsive-gates li::before {{ width:22px; height:22px; }}
    .responsive-status,.responsive-boundary {{ margin-top:8px; line-height:1.4; }}
    .responsive-handoff-diagram {{ gap:8px; margin-top:8px; }}
    .responsive-handoff-inbound span,.responsive-phase3-questions li {{ min-height:48px; padding:7px; font-size:12px; }}
    .responsive-handoff small {{ margin-top:7px; font-size:12px; }}
  }}
  @media (max-width:900px) {{
    header {{ grid-template-columns:1fr; gap:2px; padding:8px 10px 7px; }}
    .objective {{ font-size:11px; }}
    main {{ padding:6px; }}
    footer {{ grid-template-columns:1fr; gap:5px; padding:6px 8px 7px; }}
    .state-nav {{ gap:4px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; min-height:44px; padding:4px; text-align:center; font-size:11px; }}
    .state-copy h2 {{ font-size:14px; }}
    .state-copy p {{ display:-webkit-box; overflow:hidden; -webkit-box-orient:vertical; -webkit-line-clamp:2; font-size:11px; }}
    details[open] {{ position:fixed; inset:10px; z-index:10; max-height:none; padding:10px; overflow:auto; border:1.5px solid var(--ink); background:var(--paper); }}
  }}
  @media (max-height:{SHORT_LANDSCAPE_MAX_HEIGHT}px) and (orientation:landscape) {{
    header {{ grid-template-columns:minmax(0,1fr) minmax(250px,450px); gap:10px; padding:4px 10px; }}
    h1 {{ margin:1px 0; font-size:18px; }}
    .eyebrow,.phase-question {{ font-size:9px; }}
    .objective {{ display:none; }}
    main {{ padding:3px 7px; }}
    footer {{ grid-template-columns:minmax(0,1fr) minmax(250px,390px) auto; gap:6px; padding:4px 7px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; min-height:34px; padding:3px 4px; text-align:center; font-size:10px; }}
    .state-copy h2 {{ font-size:12px; }}
    .state-copy p {{ display:none; }}
    details {{ grid-column:auto; align-self:center; border-top:0; padding-top:0; font-size:10px; }}
    .evidence-count {{ display:none; }}
    .visual-shell {{ display:none; }}
    .responsive-visual {{ display:block; width:100%; height:100%; min-height:0; overflow:auto; padding:2px; }}
    .responsive-card {{ padding:5px; }}
    .responsive-card h3,.responsive-abilene h2 {{ margin-bottom:3px; font-size:12px; }}
    .responsive-body {{ display:none; }}
    .responsive-voltage-grid,.responsive-network-grid,.responsive-process-grid,.responsive-path-grid {{ gap:5px; }}
    .responsive-voltage-side {{ padding:4px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-voltage-side ul {{ display:flex; gap:5px; margin:4px 0 0; padding:0; list-style:none; }}
    .responsive-power-flow,.responsive-path-flow {{ gap:2px; margin-top:4px; }}
    .responsive-node,.responsive-stage,.responsive-stop {{ flex:1 1 0; min-height:26px; padding:2px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-relation {{ margin-top:4px !important; padding:4px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-network {{ gap:3px; }}
    .responsive-network > div {{ gap:2px; padding:4px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-balance-flow {{ gap:4px; margin-top:5px; }}
    .responsive-function-grid {{ grid-template-columns:repeat(4,minmax(0,1fr)); gap:3px; }}
    .responsive-function-grid li {{ display:flex; align-items:center; gap:3px; padding:3px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-function-grid span {{ flex:0 0 18px; height:18px; }}
    .responsive-process-lane {{ max-height:100%; }}
    .responsive-subject,.responsive-gate {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-gates {{ gap:2px; margin-top:4px; }}
    .responsive-gates li {{ grid-template-columns:18px 1fr; gap:3px; min-height:24px; padding:2px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-gates li::before {{ width:16px; height:16px; }}
    .responsive-status,.responsive-boundary {{ margin-top:4px; padding:4px 6px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-status p,.responsive-boundary p,.responsive-status-copy {{ display:-webkit-box; overflow:hidden; -webkit-box-orient:vertical; -webkit-line-clamp:2; }}
    .responsive-path {{ padding:5px; }}
    .responsive-path-flow {{ flex-direction:column; align-items:stretch; }}
    .responsive-path .responsive-arrow {{ align-self:center; transform:rotate(90deg); }}
    .responsive-path .responsive-stage {{ font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-path .responsive-stop {{ flex:1 1 auto; }}
    .responsive-status-copy {{ margin-top:4px !important; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-handoff {{ display:block; margin-top:4px; padding:5px 8px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-handoff > p {{ display:none; }}
    .responsive-handoff-diagram {{ grid-template-columns:1fr 94px 1fr; gap:3px; margin-top:4px; }}
    .responsive-handoff-inbound,.responsive-phase3-questions {{ gap:2px; }}
    .responsive-handoff-inbound span,.responsive-phase3-questions li {{ min-height:32px; padding:3px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-campus-boundary {{ padding:3px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-handoff small {{ margin-top:3px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
  }}
  @media (max-width:{PORTRAIT_MAX_WIDTH}px) and (orientation:portrait) {{
    header {{ padding:7px 8px 6px; }}
    h1 {{ font-size:20px; }}
    .state-number {{ font-size:9px; }}
    .state-nav-label {{ font-size:10px; }}
    .state-copy p {{ display:none; }}
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; }}
    .visual-shell {{ display:none; }}
    .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:3px; }}
    .responsive-card {{ padding:10px; }}
    .responsive-card h3,.responsive-abilene h2 {{ margin-bottom:5px; font-size:16px; }}
    .responsive-body,.responsive-subject,.responsive-gate,.responsive-status-copy {{ margin-bottom:8px !important; color:var(--muted); font-size:{PORTRAIT_MIN_TEXT_PX}px; line-height:1.35; }}
    .responsive-voltage-grid,.responsive-network-grid,.responsive-process-grid,.responsive-path-grid {{ grid-template-columns:1fr; gap:8px; }}
    .responsive-voltage-side {{ padding:8px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-power-flow,.responsive-path-flow,.responsive-balance-flow {{ flex-direction:column; align-items:stretch; gap:4px; }}
    .responsive-node,.responsive-stage,.responsive-stop {{ min-height:34px; padding:5px 7px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-line,.responsive-arrow {{ align-self:center; transform:rotate(90deg); }}
    .responsive-relation {{ margin-top:8px !important; padding:7px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-network {{ grid-template-columns:1fr; gap:5px; }}
    .responsive-network > div {{ gap:3px; padding:7px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-function-grid {{ grid-template-columns:1fr; gap:5px; }}
    .responsive-function-grid li {{ display:flex; align-items:center; gap:6px; padding:6px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-function-grid span {{ flex:0 0 22px; height:22px; }}
    .responsive-gates {{ gap:5px; }}
    .responsive-gates li {{ grid-template-columns:24px 1fr; gap:6px; padding:6px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-gates li::before {{ width:22px; height:22px; }}
    .responsive-status,.responsive-boundary {{ margin-top:8px; padding:8px; font-size:{PORTRAIT_MIN_TEXT_PX}px; line-height:1.35; }}
    .responsive-path {{ padding:10px; }}
    .responsive-handoff {{ display:grid; gap:4px; margin-top:8px; padding:10px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-handoff-diagram {{ grid-template-columns:1fr; gap:5px; }}
    .responsive-handoff-inbound span,.responsive-phase3-questions li {{ min-height:42px; padding:7px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-campus-boundary {{ min-height:84px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
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
  <section class="visual-shell" aria-label="Instructor-controlled transmission teaching surface">
    <svg id="visual" role="img" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" aria-labelledby="visual-title visual-description">
      <title id="visual-title">Transmission and interconnection landscape</title>
      <desc id="visual-description">Six manually selected causal views explain voltage, the meshed and balanced grid, substations, separate connection processes, Abilene service paths, and the campus handoff.</desc>
      <defs>
        <marker id="arrow-blue" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#175d8d"/></marker>
        <marker id="arrow-blue-small" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#175d8d"/></marker>
        <marker id="arrow-red" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#b3261e"/></marker>
        <marker id="arrow-green" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#2f9e8f"/></marker>
        <marker id="arrow-white" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#ffffff"/></marker>
      </defs>
      {_voltage_svg(principles["voltage_transfer"])}
      {_mesh_svg(principles["meshed_ac_network"])}
      {_balance_svg(principles["continuous_system_balance"])}
      {_substation_svg(payload["substation_anatomy"])}
      {_process_svg(payload["interconnection_processes"])}
      {_abilene_svg(payload["abilene_case"])}
      {_handoff_svg(payload["phase3_handoff"], payload["abilene_case"])}
    </svg>
  </section>
  {responsive}
</main>
<footer>
  <nav class="state-nav" role="tablist" aria-label="Manual Phase 2 teaching states">{state_buttons}</nav>
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
  setVisible("[data-principle-id]", state.principle_ids, "principleId");
  document.querySelectorAll("[data-substation]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_substation);
  }});
  setVisible("[data-process-lane-id]", state.process_lane_ids, "processLaneId");
  const showProcesses = state.process_lane_ids.length > 0;
  document.querySelectorAll("[data-processes]").forEach(element => {{
    element.toggleAttribute("hidden", !showProcesses);
  }});
  document.querySelectorAll("[data-process-boundary]").forEach(element => {{
    element.toggleAttribute("hidden", !showProcesses);
  }});
  setVisible("[data-abilene-path-id]", state.abilene_path_ids, "abilenePathId");
  const showAbilene = state.abilene_path_ids.length > 0;
  document.querySelectorAll("[data-abilene-case]").forEach(element => {{
    element.toggleAttribute("hidden", !showAbilene);
  }});
  document.querySelectorAll("[data-handoff]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_handoff);
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
