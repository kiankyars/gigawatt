"""Build the complete untimed course player and instructor packet.

The course manifest owns order and pedagogy. The planned-shot compiler owns
derived provisional frames, reusable cameras own context, and evidence ledgers
own factual claims. This module packages those inputs without adding timing,
spoken scripts, or automatic advance.

Usage: uv run python -m gigawatt.course_runtime
"""

from __future__ import annotations

from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Any

from . import layout as layout_pipeline
from . import scene as scene_pipeline
from . import shots, tokens

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
COURSE_PATH = ROOT / "course" / "segments.yaml"
VISUALS_PATH = ROOT / "course" / "visuals.yaml"
REGISTRY_PATH = DIAGRAM / "course_runtime.json"
PLAYER_PATH = DIAGRAM / "course.html"
PACKET_PATH = ROOT / "course" / "INSTRUCTOR_PACKET.md"

SCHEMA_VERSION = 1
EXPECTED_ACTS = 7
EXPECTED_SEGMENTS = 26
TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX = 390
TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX = (240, 280, 390)
TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX = 8
SHORT_TEACHING_OVERLAY_PADDING_BLOCK_PX = 5
SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX = 3
PORTRAIT_REFERENCE_VIEWPORT_WIDTH_PX = 390
PORTRAIT_REFERENCE_VIEWPORT_HEIGHT_PX = 844
PORTRAIT_RAIL_WIDTH_PX = 72
PORTRAIT_MASTHEAD_HORIZONTAL_PADDING_PX = 28
PORTRAIT_MASTHEAD_VERTICAL_PADDING_PX = 22
PORTRAIT_MASTHEAD_HEIGHT_PX = 360
PORTRAIT_MASTHEAD_SAFETY_MARGIN_PX = 24.0
PORTRAIT_TRANSPORT_HEIGHT_PX = 74
SHORT_TRANSPORT_HEIGHT_PX = 58
PORTRAIT_FOCUS_KEY_MAX_CHIPS = 12
PORTRAIT_FOCUS_KEY_COLUMNS = 2
PORTRAIT_FOCUS_KEY_GAP_PX = 5
PORTRAIT_FOCUS_KEY_FONT_PX = 10.0
PORTRAIT_FOCUS_KEY_LINE_HEIGHT = 1.15
PORTRAIT_FOCUS_KEY_MARGIN_TOP_PX = 6
PORTRAIT_ESTIMATED_GLYPH_WIDTH_RATIO = 0.60
SHORT_REFERENCE_VIEWPORT_WIDTH_PX = 844
SHORT_REFERENCE_VIEWPORT_HEIGHT_PX = 390
SHORT_MASTHEAD_HEIGHT_PX = 130
SHORT_MASTHEAD_SAFETY_MARGIN_PX = 8.0
SHORT_OPENING_QUESTION_FONT_PX = 10.0
SHORT_FOCUS_KEY_CONTENT_WIDTH_PX = 476.0
SHORT_FOCUS_KEY_MAX_CHIPS = 12
SHORT_FOCUS_KEY_COLUMNS = 5
SHORT_FOCUS_KEY_GAP_PX = 2
SHORT_FOCUS_KEY_FONT_PX = 10.0
SHORT_FOCUS_KEY_LINE_HEIGHT = 1.0
SHORT_FOCUS_KEY_MAX_HEIGHT_PX = 40.0
SHORT_ESTIMATED_GLYPH_WIDTH_RATIO = 0.60
TABLET_REFERENCE_VIEWPORT_WIDTH_PX = 1024
TABLET_REFERENCE_VIEWPORT_HEIGHT_PX = 768
TABLET_FOCUS_KEY_CONTENT_WIDTH_PX = 476.0
TABLET_FOCUS_KEY_MAX_CHIPS = 12
TABLET_FOCUS_KEY_COLUMNS = 5
TABLET_FOCUS_KEY_GAP_PX = 4
TABLET_FOCUS_KEY_FONT_PX = 10.0
TABLET_FOCUS_KEY_LINE_HEIGHT = 1.0
TABLET_FOCUS_KEY_MAX_HEIGHT_PX = 44.0
TABLET_ESTIMATED_GLYPH_WIDTH_RATIO = 0.60
DESKTOP_REFERENCE_VIEWPORTS = (
    {"id": "1920x1080", "width": 1920, "height": 1080},
    {"id": "1440x900", "width": 1440, "height": 900},
)
DESKTOP_RAIL_WIDTH_PX = 286
DESKTOP_MASTHEAD_HORIZONTAL_PADDING_PX = 48
DESKTOP_POSTURE_WIDTH_PX = 190
DESKTOP_MASTHEAD_COLUMN_GAP_PX = 24
DESKTOP_FOCUS_KEY_MAX_CHIPS = 12
DESKTOP_FOCUS_KEY_COLUMNS = 7
DESKTOP_FOCUS_KEY_GAP_PX = 5
DESKTOP_FOCUS_KEY_FONT_PX = 10.0
DESKTOP_FOCUS_KEY_LINE_HEIGHT = 1.15
DESKTOP_FOCUS_KEY_MAX_HEIGHT_PX = 41.0
DESKTOP_ESTIMATED_GLYPH_WIDTH_RATIO = 0.60
FOCUS_KEY_INDEX_FONT_FLOOR_PX = 10.0
FOCUSED_GEOMETRY_STROKE_FLOOR_PX = 1.5
FOCUSED_GEOMETRY_DASH_FLOOR_PX = 1.0

_PORTRAIT_MASTHEAD_BORDER_PX = 1.5
_PORTRAIT_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX = 6
_PORTRAIT_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX = 3
_PORTRAIT_FOCUS_KEY_CHIP_BORDER_PX = 1
_PORTRAIT_FOCUS_KEY_INDEX_WIDTH_PX = 14
_PORTRAIT_FOCUS_KEY_INDEX_GAP_PX = 4
_PORTRAIT_FOCUS_KEY_SWATCH_WIDTH_PX = 28
_SHORT_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX = 2
_SHORT_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX = 0
_SHORT_FOCUS_KEY_CHIP_BORDER_PX = 1
_SHORT_FOCUS_KEY_INDEX_WIDTH_PX = 10
_SHORT_FOCUS_KEY_INDEX_GAP_PX = 2
_SHORT_FOCUS_KEY_SWATCH_WIDTH_PX = 20
_TABLET_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX = 2
_TABLET_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX = 0
_TABLET_FOCUS_KEY_CHIP_BORDER_PX = 1
_TABLET_FOCUS_KEY_INDEX_WIDTH_PX = 10
_TABLET_FOCUS_KEY_INDEX_GAP_PX = 2
_TABLET_FOCUS_KEY_SWATCH_WIDTH_PX = 20
_DESKTOP_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX = 4
_DESKTOP_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX = 1
_DESKTOP_FOCUS_KEY_CHIP_BORDER_PX = 1
_DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX = 14
_DESKTOP_FOCUS_KEY_INDEX_GAP_PX = 4
_DESKTOP_FOCUS_KEY_SWATCH_WIDTH_PX = 28
_COMPACT_BOUNDARY_COPY = (
    "Source-gated Abilene facts · dashed equipment is a teaching reference, "
    "not as-built."
)

# These aliases are intentionally topology-ID keyed rather than derived from
# mutable prose. The exact authored label remains the accessible name; this
# compact visible copy is the stable orientation aid used in constrained keys.
_COMPACT_FOCUS_LABELS = {
    "air_cooled_chiller": "Chiller",
    "atmosphere": "Atmos.",
    "bess": "BESS",
    "busway": "Busway",
    "campus_mv_distribution": "MV dist.",
    "cdu": "CDU",
    "cold_plate": "Cold plt",
    "corridor_345": "345 path",
    "crah": "CRAH",
    "die": "Die",
    "die_turn": "W→heat",
    "diesel": "Diesel",
    "diesel_authorization": "62 units",
    "diesel_unknown": "Diesel ?",
    "facility_loop": "Fac loop",
    "fill_treatment": "Fill",
    "gas_permit": "360.5 MW",
    "gas_turbine": "Turbine",
    "gas_units": "10× gas",
    "generator": "Gen",
    "generator_terminal": "Gen term.",
    "gsu_transformer": "GSU",
    "hv_protection": "HV prot.",
    "legend_conceptual": "Concept",
    "legend_direction": "138 tie → station",
    "legend_energized": "Solid",
    "legend_future": "Dashed",
    "legend_permitted": "Dotted",
    "legend_posture": "Posture",
    "legend_title": "Carrier",
    "lv_switchgear": "LV gear",
    "manifold": "Manifold",
    "mv_bus": "MV bus",
    "mv_reference_design": "34.5 kV",
    "mv_unknown": "MV ?",
    "nuclear_variant": "Nuclear",
    "power_shelf": "Shelf",
    "rack_air_load": "Rack air",
    "rack_manifold": "Rack hdr",
    "region_buildings": "8 bldgs",
    "room_data_hall": "Hall",
    "room_electrical": "Elec.",
    "room_mechanical": "Mech.",
    "source_138": "138 src",
    "source_345": "345 src",
    "station_138": "138 kV",
    "station_345": "345 kV",
    "station_345_energized": "5 MPTs",
    "tie_138": "138 tie",
    "unit_sub": "Unit sub",
    "unit_substation": "Unit sub",
    "ups": "UPS",
    "vrm": "VRM",
    "zone_btm": "BTM",
    "zone_building": "Bldg",
    "zone_grid": "2 grid",
    "zone_mv": "MV env.",
    "zone_substations": "Stations",
}
_LEGEND_GRAMMAR_CUES = {
    "legend_title": "carrier",
    "legend_direction": "direction",
    "legend_posture": "posture",
    "legend_energized": "solid",
    "legend_permitted": "dotted",
    "legend_future": "dashed",
    "legend_conceptual": "conceptual",
}
_LEGEND_GRAMMAR_ACCESSIBLE_EXAMPLES = {
    "legend_direction": "initial 138 kV tie → initial 200 MW / 138 kV station",
}
FORBIDDEN_RUNTIME_KEYS = {
    "autoplay",
    "beat",
    "beats",
    "cadence",
    "duration",
    "runtime",
    "script",
    "timing",
}

PROMOTION_GUARD_WARNINGS = {
    "announced_to_operational": "An announced structure or role does not prove current operation.",
    "anticipated_to_measured": "An anticipated value is not a measured operating result.",
    "capacity_basis_substitution": "Do not substitute one capacity, power, energy, or compute basis for another.",
    "conceptual_to_as_built": "Conceptual geometry is not an as-built connection or equipment configuration.",
    "contractual_to_physical": "A contract or commercial role does not establish physical power flow or asset control.",
    "design_ceiling_to_installed": "A design ceiling does not establish installed or operating quantity.",
    "design_to_as_built": "A design or engineering reference is not proof of the site's as-built condition.",
    "energy_power_time_basis": "Keep power rates and energy totals on one explicit, matching averaging interval.",
    "excluded_scope_addition": "Do not add explicitly excluded assets or capacity to the taught scope.",
    "facility_financing_to_component_allocation": "Do not allocate facility-level finance, acceptance, rent, or utilization terms to individual equipment; those terms remain undisclosed.",
    "future_design_to_operational": "A future design is not installed, commissioned, or operational.",
    "live_by_to_start_date": "A live-by disclosure is only an upper date bound, not an exact start date.",
    "market_example_to_site_schedule": "Market lead times and product availability examples do not establish Abilene's schedule or critical path.",
    "minimum_to_exact": "A confirmed minimum is not an exact current count.",
    "model_range_to_site_configuration": "A manufacturer range does not reveal the site's selected setting.",
    "named_role_to_asset_assignment": "Do not apply program, project, phase, or operating-part roles to every highlighted asset; their published scopes remain distinct.",
    "null_to_zero": "Unknown means not established by the cited evidence; it does not mean zero or absent.",
    "permitted_to_commissioned": "A permit does not prove equipment was commissioned.",
    "permitted_to_installed": "A permit does not prove equipment was installed.",
    "planned_to_operational": "A planned milestone or capacity is not operational evidence.",
    "power_to_compute_bridge": "Do not convert power to compute without matching hardware quantity, measured power, workload efficiency, and system boundaries.",
    "product_to_site_configuration": "A product specification does not establish the site's selected configuration or operating point.",
    "reverse_physical_flow": "Do not reverse supply, return, heat, or electrical direction while explaining the diagram.",
    "scenario_to_site_estimate": "A derived scenario is not a site estimate; missing site inputs must stop the calculation.",
    "single_path_conflation": "Do not identify distinct named, planned, conceptual, or energized paths as one completed physical path.",
    "site_scope_transfer": "A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.",
    "substation_to_it_load": "Substation or feeder capacity does not establish current facility load or critical IT load.",
    "untyped_to_capacity": "An untyped delivery percentage does not establish MW, buildings, racks, accelerators, or workload capacity.",
}


class CourseRuntimeError(ValueError):
    """Raised when the production package drifts from a canonical input."""


def load_inputs() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    course = scene_pipeline.load_yaml(COURSE_PATH)
    cameras = scene_pipeline.load_yaml(DIAGRAM / "cameras.yaml")
    master = scene_pipeline.load_yaml(DIAGRAM / "master.yaml")
    layout = scene_pipeline.load_yaml(DIAGRAM / "layout.yaml")
    scene = scene_pipeline.load_yaml(DIAGRAM / "scene.yaml")
    ledgers = {
        ledger_id: scene_pipeline.load_yaml(ROOT / relative_path)
        for ledger_id, relative_path in course["meta"]["evidence_ledgers"].items()
    }
    visuals = scene_pipeline.load_yaml(VISUALS_PATH)
    return course, cameras, master, layout, scene, ledgers, visuals


def _source_digest(course: dict[str, Any]) -> str:
    paths = [
        Path(__file__).resolve(),
        *shots.GENERATOR_DEPENDENCY_PATHS,
        COURSE_PATH,
        VISUALS_PATH,
        DIAGRAM / "cameras.yaml",
        DIAGRAM / "master.yaml",
        DIAGRAM / "layout.yaml",
        DIAGRAM / "scene.yaml",
        *(
            ROOT / path
            for _, path in sorted(course["meta"]["evidence_ledgers"].items())
        ),
    ]
    return shots._digest_paths(paths)


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def compact_focus_label(item_id: str) -> str:
    """Return stable visible key copy while leaving full prose to accessibility."""
    if not isinstance(item_id, str) or not item_id:
        raise CourseRuntimeError("focus-key IDs must be non-empty strings")
    if item_id.startswith("legend_") and item_id not in _LEGEND_GRAMMAR_CUES:
        raise CourseRuntimeError(f"unknown fixed grammar key ID: {item_id}")
    return _COMPACT_FOCUS_LABELS.get(item_id, item_id.replace("_", " "))


def _focus_key_accessible_label(item_id: str, authored_label: str) -> str:
    """Keep authored copy intact while adding a concrete named grammar example."""
    example = _LEGEND_GRAMMAR_ACCESSIBLE_EXAMPLES.get(item_id)
    return (
        authored_label if example is None else f"{authored_label} · example: {example}"
    )


def focus_key_entries(
    segment: dict[str, Any],
    master: dict[str, Any],
    evidence: dict[str, Any],
) -> list[dict[str, str | int | bool | None]]:
    """Resolve the exact ordered marker-to-label key emitted by the player."""
    visual = segment["visual"]
    if visual["label_policy"] != "focus":
        return []
    if segment["render_mode"] == "2d":
        ids = list(
            dict.fromkeys([*visual["label_copy_ids"], *segment["reveal_copy_ids"]])
        )
        unknown_grammar_ids = sorted(
            item_id
            for item_id in ids
            if item_id.startswith("legend_") and item_id not in _LEGEND_GRAMMAR_CUES
        )
        if unknown_grammar_ids:
            raise CourseRuntimeError(
                f"segment {segment['segment_id']}: unknown fixed grammar key ID "
                f"{unknown_grammar_ids}"
            )
        labels = [
            layout_pipeline.resolve_copy(
                master,
                evidence,
                copy_id,
                include_hidden=True,
            )
            for copy_id in ids
        ]
    else:
        ids = list(dict.fromkeys(visual["label_node_ids"]))
        nodes = {node["id"]: node for node in master["nodes"]}
        labels = [
            (
                f"{nodes[node_id]['label']} · "
                f"{nodes[node_id]['presence'].replace('_', ' ')} · "
                f"{nodes[node_id]['lifecycle'].replace('_', ' ')}"
            )
            for node_id in ids
        ]
    if any(not isinstance(label, str) or not label.strip() for label in labels):
        raise CourseRuntimeError(
            f"segment {segment['segment_id']}: focus key contains unresolved copy"
        )
    entries: list[dict[str, str | int | bool | None]] = []
    geometry_number = 0
    for item_id, label in zip(ids, labels, strict=True):
        grammar_cue = _LEGEND_GRAMMAR_CUES.get(item_id)
        if item_id.startswith("legend_") and grammar_cue is None:
            raise CourseRuntimeError(
                f"segment {segment['segment_id']}: unknown fixed grammar key ID "
                f"{item_id}"
            )
        marker_required = grammar_cue is None
        if marker_required:
            geometry_number += 1
        entries.append(
            {
                "number": geometry_number if marker_required else None,
                "id": item_id,
                "label": label.strip(),
                "accessible_label": _focus_key_accessible_label(item_id, label.strip()),
                "compact_label": compact_focus_label(item_id),
                "key_role": "geometry" if marker_required else "grammar",
                "marker_required": marker_required,
                "swatch_cue": grammar_cue,
            }
        )
    return entries


def _normalized_grammar_cues(
    labels: Sequence[str], grammar_cues: Sequence[str | None] | None
) -> list[str | None]:
    cues = [None] * len(labels) if grammar_cues is None else list(grammar_cues)
    if len(cues) != len(labels):
        raise CourseRuntimeError("focus-key grammar cues must align with labels")
    unknown = sorted(
        {cue for cue in cues if cue and cue not in _LEGEND_GRAMMAR_CUES.values()}
    )
    if unknown:
        raise CourseRuntimeError(f"unknown focus-key grammar cues: {unknown}")
    return cues


def _estimated_wrapped_line_count(
    text: str,
    width_px: float,
    font_px: float,
) -> int:
    """Conservatively model word wrapping with the CSS anywhere fallback."""
    if width_px <= 0 or font_px <= 0:
        raise CourseRuntimeError("wrapped text requires positive width and font size")
    glyph_width = font_px * PORTRAIT_ESTIMATED_GLYPH_WIDTH_RATIO
    maximum_glyphs = max(1, int(width_px // glyph_width))
    words = text.split()
    if not words:
        return 1
    lines = 1
    line_glyphs = 0
    for word in words:
        remaining = len(word)
        if line_glyphs and line_glyphs + 1 + remaining <= maximum_glyphs:
            line_glyphs += 1 + remaining
            continue
        if line_glyphs:
            lines += 1
            line_glyphs = 0
        while remaining > maximum_glyphs:
            lines += 1
            remaining -= maximum_glyphs
        line_glyphs = remaining
    return lines


def estimate_portrait_focus_key_layout(
    labels: Sequence[str],
    *,
    grammar_cues: Sequence[str | None] | None = None,
    content_width_px: float = (
        PORTRAIT_REFERENCE_VIEWPORT_WIDTH_PX
        - PORTRAIT_RAIL_WIDTH_PX
        - PORTRAIT_MASTHEAD_HORIZONTAL_PADDING_PX
    ),
) -> dict[str, Any]:
    """Model the deterministic two-column portrait key without DOM measurement."""
    if any(not isinstance(label, str) or not label.strip() for label in labels):
        raise CourseRuntimeError("portrait focus-key labels must be non-empty strings")
    cues = _normalized_grammar_cues(labels, grammar_cues)
    cell_width = (
        content_width_px - PORTRAIT_FOCUS_KEY_GAP_PX * (PORTRAIT_FOCUS_KEY_COLUMNS - 1)
    ) / PORTRAIT_FOCUS_KEY_COLUMNS
    fixed_chrome = (
        2 * _PORTRAIT_FOCUS_KEY_CHIP_BORDER_PX
        + 2 * _PORTRAIT_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX
        + _PORTRAIT_FOCUS_KEY_INDEX_GAP_PX
    )
    text_widths = [
        cell_width
        - fixed_chrome
        - (
            _PORTRAIT_FOCUS_KEY_SWATCH_WIDTH_PX
            if cue
            else _PORTRAIT_FOCUS_KEY_INDEX_WIDTH_PX
        )
        for cue in cues
    ]
    item_heights = [
        max(
            _PORTRAIT_FOCUS_KEY_INDEX_WIDTH_PX,
            _estimated_wrapped_line_count(
                label,
                text_width,
                PORTRAIT_FOCUS_KEY_FONT_PX,
            )
            * PORTRAIT_FOCUS_KEY_FONT_PX
            * PORTRAIT_FOCUS_KEY_LINE_HEIGHT,
        )
        + 2 * _PORTRAIT_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX
        + 2 * _PORTRAIT_FOCUS_KEY_CHIP_BORDER_PX
        for label, text_width in zip(labels, text_widths, strict=True)
    ]
    row_heights = [
        max(item_heights[offset : offset + PORTRAIT_FOCUS_KEY_COLUMNS])
        for offset in range(0, len(item_heights), PORTRAIT_FOCUS_KEY_COLUMNS)
    ]
    estimated_height = sum(row_heights) + PORTRAIT_FOCUS_KEY_GAP_PX * max(
        0, len(row_heights) - 1
    )
    within_chip_budget = len(labels) <= PORTRAIT_FOCUS_KEY_MAX_CHIPS
    return {
        "chip_count": len(labels),
        "maximum_chip_count": PORTRAIT_FOCUS_KEY_MAX_CHIPS,
        "within_chip_budget": within_chip_budget,
        "columns": PORTRAIT_FOCUS_KEY_COLUMNS,
        "column_spans": [1] * len(labels),
        "row_count": len(row_heights),
        "row_heights_px": [round(height, 3) for height in row_heights],
        "content_width_px": round(content_width_px, 3),
        "cell_width_px": round(cell_width, 3),
        "text_widths_px": [round(width, 3) for width in text_widths],
        "minimum_text_width_px": round(min(text_widths, default=cell_width), 3),
        "font_px": PORTRAIT_FOCUS_KEY_FONT_PX,
        "index_font_px": FOCUS_KEY_INDEX_FONT_FLOOR_PX,
        "line_height": PORTRAIT_FOCUS_KEY_LINE_HEIGHT,
        "estimated_glyph_width_ratio": PORTRAIT_ESTIMATED_GLYPH_WIDTH_RATIO,
        "estimated_height_px": round(estimated_height, 3),
        "layout_mode": "wrapped_grid",
        "overflow_wrap": "anywhere",
        "horizontal_paging_required": False,
        "grammar_cue_count": sum(cue is not None for cue in cues),
        "estimated_complete_key_fit": within_chip_budget,
    }


def _estimate_compact_focus_key_layout(
    compact_labels: Sequence[str],
    *,
    grammar_cues: Sequence[str | None] | None,
    viewport_id: str,
    content_width_px: float,
    maximum_chip_count: int,
    columns: int,
    gap_px: float,
    font_px: float,
    line_height: float,
    maximum_height_px: float,
    glyph_width_ratio: float,
    chip_horizontal_padding_px: float,
    chip_vertical_padding_px: float,
    chip_border_px: float,
    index_width_px: float,
    index_gap_px: float,
    swatch_width_px: float,
    layout_mode: str,
) -> dict[str, Any]:
    """Model a complete compact key using the same constants as runtime CSS."""
    if any(not isinstance(label, str) or not label.strip() for label in compact_labels):
        raise CourseRuntimeError("compact focus-key labels must be non-empty strings")
    if content_width_px <= 0:
        raise CourseRuntimeError("compact focus-key content width must be positive")
    cues = _normalized_grammar_cues(compact_labels, grammar_cues)
    cell_width = (content_width_px - gap_px * (columns - 1)) / columns
    column_spans = [2 if cue == "direction" else 1 for cue in cues]
    fixed_chrome = 2 * chip_border_px + 2 * chip_horizontal_padding_px + index_gap_px
    text_widths = [
        cell_width * span
        + gap_px * (span - 1)
        - fixed_chrome
        - (swatch_width_px if cue else index_width_px)
        for cue, span in zip(cues, column_spans, strict=True)
    ]
    estimated_widths = [
        len(label) * font_px * glyph_width_ratio for label in compact_labels
    ]
    excess_widths = [
        max(0.0, width - text_width)
        for width, text_width in zip(estimated_widths, text_widths, strict=True)
    ]
    row_count = 0
    occupied_columns = 0
    for span in column_spans:
        if occupied_columns == 0:
            row_count += 1
        if occupied_columns + span > columns:
            row_count += 1
            occupied_columns = 0
        occupied_columns += span
        if occupied_columns == columns:
            occupied_columns = 0
    chip_height = (
        max(index_width_px, font_px * line_height)
        + 2 * chip_vertical_padding_px
        + 2 * chip_border_px
    )
    estimated_height = row_count * chip_height + max(0, row_count - 1) * gap_px
    excess_height = max(0.0, estimated_height - maximum_height_px)
    within_chip_budget = len(compact_labels) <= maximum_chip_count
    fits = within_chip_budget and not any(excess_widths) and excess_height == 0.0
    return {
        "viewport_id": viewport_id,
        "chip_count": len(compact_labels),
        "maximum_chip_count": maximum_chip_count,
        "within_chip_budget": within_chip_budget,
        "columns": columns,
        "column_spans": column_spans,
        "row_count": row_count,
        "content_width_px": round(content_width_px, 3),
        "cell_width_px": round(cell_width, 3),
        "text_widths_px": [round(width, 3) for width in text_widths],
        "minimum_text_width_px": round(min(text_widths, default=cell_width), 3),
        "font_px": font_px,
        "index_font_px": font_px,
        "line_height": line_height,
        "estimated_glyph_width_ratio": glyph_width_ratio,
        "estimated_label_widths_px": [round(width, 3) for width in estimated_widths],
        "excess_widths_px": [round(width, 3) for width in excess_widths],
        "maximum_excess_width_px": round(max(excess_widths, default=0.0), 3),
        "estimated_height_px": round(estimated_height, 3),
        "maximum_height_px": maximum_height_px,
        "excess_height_px": round(excess_height, 3),
        "layout_mode": layout_mode,
        "horizontal_paging_required": False,
        "grammar_cue_count": sum(cue is not None for cue in cues),
        "estimated_complete_key_fit": fits,
    }


def estimate_short_focus_key_layout(
    compact_labels: Sequence[str],
    *,
    grammar_cues: Sequence[str | None] | None = None,
    content_width_px: float = SHORT_FOCUS_KEY_CONTENT_WIDTH_PX,
) -> dict[str, Any]:
    """Model the complete 844x390 key against its conservative first column."""
    return _estimate_compact_focus_key_layout(
        compact_labels,
        grammar_cues=grammar_cues,
        viewport_id=(
            f"{SHORT_REFERENCE_VIEWPORT_WIDTH_PX}x{SHORT_REFERENCE_VIEWPORT_HEIGHT_PX}"
        ),
        content_width_px=content_width_px,
        maximum_chip_count=SHORT_FOCUS_KEY_MAX_CHIPS,
        columns=SHORT_FOCUS_KEY_COLUMNS,
        gap_px=SHORT_FOCUS_KEY_GAP_PX,
        font_px=SHORT_FOCUS_KEY_FONT_PX,
        line_height=SHORT_FOCUS_KEY_LINE_HEIGHT,
        maximum_height_px=SHORT_FOCUS_KEY_MAX_HEIGHT_PX,
        glyph_width_ratio=SHORT_ESTIMATED_GLYPH_WIDTH_RATIO,
        chip_horizontal_padding_px=_SHORT_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX,
        chip_vertical_padding_px=_SHORT_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX,
        chip_border_px=_SHORT_FOCUS_KEY_CHIP_BORDER_PX,
        index_width_px=_SHORT_FOCUS_KEY_INDEX_WIDTH_PX,
        index_gap_px=_SHORT_FOCUS_KEY_INDEX_GAP_PX,
        swatch_width_px=_SHORT_FOCUS_KEY_SWATCH_WIDTH_PX,
        layout_mode="fixed_five_column_spanning_grid",
    )


def estimate_tablet_focus_key_layout(
    compact_labels: Sequence[str],
    *,
    grammar_cues: Sequence[str | None] | None = None,
    content_width_px: float = TABLET_FOCUS_KEY_CONTENT_WIDTH_PX,
) -> dict[str, Any]:
    """Model the complete 1024x768 key against its real first column."""
    return _estimate_compact_focus_key_layout(
        compact_labels,
        grammar_cues=grammar_cues,
        viewport_id=(
            f"{TABLET_REFERENCE_VIEWPORT_WIDTH_PX}x"
            f"{TABLET_REFERENCE_VIEWPORT_HEIGHT_PX}"
        ),
        content_width_px=content_width_px,
        maximum_chip_count=TABLET_FOCUS_KEY_MAX_CHIPS,
        columns=TABLET_FOCUS_KEY_COLUMNS,
        gap_px=TABLET_FOCUS_KEY_GAP_PX,
        font_px=TABLET_FOCUS_KEY_FONT_PX,
        line_height=TABLET_FOCUS_KEY_LINE_HEIGHT,
        maximum_height_px=TABLET_FOCUS_KEY_MAX_HEIGHT_PX,
        glyph_width_ratio=TABLET_ESTIMATED_GLYPH_WIDTH_RATIO,
        chip_horizontal_padding_px=_TABLET_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX,
        chip_vertical_padding_px=_TABLET_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX,
        chip_border_px=_TABLET_FOCUS_KEY_CHIP_BORDER_PX,
        index_width_px=_TABLET_FOCUS_KEY_INDEX_WIDTH_PX,
        index_gap_px=_TABLET_FOCUS_KEY_INDEX_GAP_PX,
        swatch_width_px=_TABLET_FOCUS_KEY_SWATCH_WIDTH_PX,
        layout_mode="fixed_five_column_spanning_grid",
    )


def desktop_focus_key_content_width(viewport_width_px: int) -> float:
    """Return the actual first masthead-column width in a desktop profile."""
    supported_widths = {
        int(viewport["width"]) for viewport in DESKTOP_REFERENCE_VIEWPORTS
    }
    if viewport_width_px not in supported_widths:
        raise CourseRuntimeError(
            f"unsupported desktop focus-key viewport width: {viewport_width_px}"
        )
    return float(
        viewport_width_px
        - DESKTOP_RAIL_WIDTH_PX
        - DESKTOP_MASTHEAD_HORIZONTAL_PADDING_PX
        - DESKTOP_POSTURE_WIDTH_PX
        - DESKTOP_MASTHEAD_COLUMN_GAP_PX
    )


def estimate_desktop_focus_key_layout(
    compact_labels: Sequence[str],
    *,
    viewport_id: str,
    grammar_cues: Sequence[str | None] | None = None,
) -> dict[str, Any]:
    """Model the complete non-scrolling key at a canonical desktop viewport."""
    viewport_by_id = {
        str(viewport["id"]): viewport for viewport in DESKTOP_REFERENCE_VIEWPORTS
    }
    if viewport_id not in viewport_by_id:
        raise CourseRuntimeError(
            f"unsupported desktop focus-key viewport: {viewport_id!r}"
        )
    viewport_width = int(viewport_by_id[viewport_id]["width"])
    return _estimate_compact_focus_key_layout(
        compact_labels,
        grammar_cues=grammar_cues,
        viewport_id=viewport_id,
        content_width_px=desktop_focus_key_content_width(viewport_width),
        maximum_chip_count=DESKTOP_FOCUS_KEY_MAX_CHIPS,
        columns=DESKTOP_FOCUS_KEY_COLUMNS,
        gap_px=DESKTOP_FOCUS_KEY_GAP_PX,
        font_px=DESKTOP_FOCUS_KEY_FONT_PX,
        line_height=DESKTOP_FOCUS_KEY_LINE_HEIGHT,
        maximum_height_px=DESKTOP_FOCUS_KEY_MAX_HEIGHT_PX,
        glyph_width_ratio=DESKTOP_ESTIMATED_GLYPH_WIDTH_RATIO,
        chip_horizontal_padding_px=_DESKTOP_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX,
        chip_vertical_padding_px=_DESKTOP_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX,
        chip_border_px=_DESKTOP_FOCUS_KEY_CHIP_BORDER_PX,
        index_width_px=_DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX,
        index_gap_px=_DESKTOP_FOCUS_KEY_INDEX_GAP_PX,
        swatch_width_px=_DESKTOP_FOCUS_KEY_SWATCH_WIDTH_PX,
        layout_mode="fixed_seven_column_wrapped_grid",
    )


def estimate_portrait_masthead_layout(
    segment: dict[str, Any],
    labels: Sequence[str],
    *,
    grammar_cues: Sequence[str | None] | None = None,
) -> dict[str, Any]:
    """Estimate the complete 390px portrait masthead against its fixed budget."""
    content_width = (
        PORTRAIT_REFERENCE_VIEWPORT_WIDTH_PX
        - PORTRAIT_RAIL_WIDTH_PX
        - PORTRAIT_MASTHEAD_HORIZONTAL_PADDING_PX
    )

    def line_height(text: str, font_px: float, ratio: float) -> float:
        return (
            _estimated_wrapped_line_count(text, content_width, font_px)
            * font_px
            * ratio
        )

    eyebrow = (
        f"Act {segment['act_sequence']} · {segment['act_title']} · "
        f"{segment['sequence']:02d} / {EXPECTED_SEGMENTS}"
    )
    flow_height = line_height(eyebrow, 9.0, 1.2)
    flow_height += 5.0 + line_height(segment["title"], 20.0, 1.1)
    flow_height += 5.0 + line_height(segment["opening_question"], 11.0, 1.25)
    flow_height += 4.0 + line_height(_COMPACT_BOUNDARY_COPY, 10.0, 1.2)
    flow_height += 5.0 + 10.0 * 1.25
    focus_key = estimate_portrait_focus_key_layout(
        labels,
        grammar_cues=grammar_cues,
    )
    if labels:
        flow_height += (
            PORTRAIT_FOCUS_KEY_MARGIN_TOP_PX + focus_key["estimated_height_px"]
        )
    required_height = (
        PORTRAIT_MASTHEAD_VERTICAL_PADDING_PX
        + _PORTRAIT_MASTHEAD_BORDER_PX
        + flow_height
    )
    spare_height = PORTRAIT_MASTHEAD_HEIGHT_PX - required_height
    fits = (
        focus_key["within_chip_budget"]
        and spare_height >= PORTRAIT_MASTHEAD_SAFETY_MARGIN_PX
    )
    return {
        "evidence_scope": "deterministic_static_estimate_not_live_browser",
        "viewport_width_px": PORTRAIT_REFERENCE_VIEWPORT_WIDTH_PX,
        "content_width_px": content_width,
        "budget_height_px": PORTRAIT_MASTHEAD_HEIGHT_PX,
        "required_safety_margin_px": PORTRAIT_MASTHEAD_SAFETY_MARGIN_PX,
        "required_height_px": round(required_height, 3),
        "spare_height_px": round(spare_height, 3),
        "safety_margin_passed": spare_height >= PORTRAIT_MASTHEAD_SAFETY_MARGIN_PX,
        "focus_key": focus_key,
        "estimated_complete_key_fit": fits,
    }


def _compiled_visuals(
    course: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    visuals: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    """Validate claim-bound presentation emphasis without changing semantics."""
    if set(visuals) != {"schema_version", "segments"}:
        raise CourseRuntimeError(
            "course visuals must contain exactly schema_version and segments"
        )
    if (
        type(visuals["schema_version"]) is not int
        or visuals["schema_version"] != 1
        or not isinstance(visuals["segments"], dict)
    ):
        raise CourseRuntimeError("course visuals schema_version must be 1")

    course_segments = {
        segment["id"]: segment for act in course["acts"] for segment in act["segments"]
    }
    unknown_segments = set(visuals["segments"]) - set(course_segments)
    if unknown_segments:
        raise CourseRuntimeError(
            f"course visuals reference unknown segments: {sorted(unknown_segments)}"
        )

    known_nodes = {node["id"] for node in master["nodes"]}
    known_copy = set(master["copy"])
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    compiled: dict[str, dict[str, Any]] = {}
    for segment_id, visual in visuals["segments"].items():
        location = f"course visuals segment {segment_id}"
        if not isinstance(visual, dict) or set(visual) != {
            "label_policy",
            "show_legend",
            "label_node_ids",
            "label_copy_ids",
            "annotation",
        }:
            raise CourseRuntimeError(f"{location}: invalid fields")
        if visual["label_policy"] != "focus":
            raise CourseRuntimeError(f"{location}: label_policy must be focus")
        if not isinstance(visual["show_legend"], bool):
            raise CourseRuntimeError(f"{location}.show_legend must be boolean")
        label_node_ids = visual["label_node_ids"]
        label_copy_ids = visual["label_copy_ids"]
        for field, values in (
            ("label_node_ids", label_node_ids),
            ("label_copy_ids", label_copy_ids),
        ):
            if (
                not isinstance(values, list)
                or any(not isinstance(value, str) or not value for value in values)
                or len(values) != len(set(values))
            ):
                raise CourseRuntimeError(f"{location}.{field}: expected unique IDs")

        segment = course_segments[segment_id]
        if set(label_node_ids) - set(segment["node_ids"]):
            raise CourseRuntimeError(
                f"{location}: label nodes must stay inside segment focus"
            )
        if set(label_node_ids) - known_nodes:
            raise CourseRuntimeError(f"{location}: unknown label node IDs")
        if set(label_copy_ids) - known_copy:
            raise CourseRuntimeError(f"{location}: unknown label copy IDs")
        render_mode = camera_map[segment["camera"]["anchor"]]["mode"]
        if render_mode == "3d" and label_copy_ids:
            raise CourseRuntimeError(
                f"{location}: 3D emphasis cannot contain 2D label copy IDs"
            )
        if render_mode != "3d" and label_node_ids:
            raise CourseRuntimeError(
                f"{location}: 2D emphasis cannot contain 3D label node IDs"
            )
        if render_mode == "3d" and visual["show_legend"]:
            raise CourseRuntimeError(
                f"{location}: 3D emphasis cannot show the map legend"
            )
        hidden_copy = {
            copy_id
            for copy_id, record in master["copy"].items()
            if record.get("base_visible", True) is False
        }
        if set(label_copy_ids) & hidden_copy:
            raise CourseRuntimeError(
                f"{location}: base-hidden copy must use the existing reveal contract"
            )

        annotation = visual["annotation"]
        if annotation is None:
            normalized_annotation = None
        elif not isinstance(annotation, dict) or set(annotation) != {
            "kind",
            "position",
            "title",
            "items",
        }:
            raise CourseRuntimeError(f"{location}.annotation: invalid fields")
        else:
            if annotation["kind"] not in {
                "comparison",
                "funnel",
                "layers",
                "parallel",
                "routes",
                "sequence",
            }:
                raise CourseRuntimeError(f"{location}.annotation.kind is invalid")
            if annotation["position"] not in {
                "left",
                "right",
                "top-left",
                "top-right",
            }:
                raise CourseRuntimeError(
                    f"{location}.annotation.position must be left or right"
                )
            if (
                not isinstance(annotation["title"], str)
                or not annotation["title"].strip()
            ):
                raise CourseRuntimeError(
                    f"{location}.annotation.title must be non-empty"
                )
            items = annotation["items"]
            if not isinstance(items, list) or not 2 <= len(items) <= 5:
                raise CourseRuntimeError(
                    f"{location}.annotation.items must contain two to five items"
                )
            if annotation["kind"] == "routes" and len(items) not in {3, 4}:
                raise CourseRuntimeError(
                    f"{location}.annotation.items: routes requires three or four items"
                )
            if annotation["kind"] == "funnel" and len(items) < 3:
                raise CourseRuntimeError(
                    f"{location}.annotation.items: funnel requires at least three items"
                )
            if annotation["kind"] == "parallel" and len(items) != 4:
                raise CourseRuntimeError(
                    f"{location}.annotation.items: parallel requires exactly four items"
                )
            claim_ids = {claim["id"] for claim in segment["evidence"]["claims"]}
            normalized_items = []
            for index, item in enumerate(items):
                item_location = f"{location}.annotation.items[{index}]"
                if not isinstance(item, dict) or set(item) != {"label", "claim_ids"}:
                    raise CourseRuntimeError(f"{item_location}: invalid fields")
                label = item["label"]
                refs = item["claim_ids"]
                if not isinstance(label, str) or not label.strip() or len(label) > 96:
                    raise CourseRuntimeError(
                        f"{item_location}.label must be 1 to 96 characters"
                    )
                if (
                    not isinstance(refs, list)
                    or not refs
                    or any(not isinstance(ref, str) or not ref for ref in refs)
                    or len(refs) != len(set(refs))
                ):
                    raise CourseRuntimeError(
                        f"{item_location}.claim_ids must be non-empty unique IDs"
                    )
                unknown_claims = set(refs) - claim_ids
                if unknown_claims:
                    raise CourseRuntimeError(
                        f"{item_location}: unknown claim IDs {sorted(unknown_claims)}"
                    )
                normalized_items.append({"label": label, "claim_ids": list(refs)})

            normalized_annotation = {
                "kind": annotation["kind"],
                "position": annotation["position"],
                "title": annotation["title"],
                "items": normalized_items,
            }

        compiled[segment_id] = {
            "label_policy": "focus",
            "show_legend": visual["show_legend"],
            "label_node_ids": list(label_node_ids),
            "label_copy_ids": list(label_copy_ids),
            "annotation": normalized_annotation,
        }

    forbidden = {
        key.casefold()
        for key in _walk_keys(compiled)
        if key.casefold() in FORBIDDEN_RUNTIME_KEYS
    }
    if forbidden:
        raise CourseRuntimeError(
            f"course visuals contain timing or scripting fields: {sorted(forbidden)}"
        )
    return compiled


def _display_value(fact: dict[str, Any]) -> str:
    value = fact["value"]
    if value is None:
        if fact["posture"] == "no_evidence_backed_estimate":
            return "No evidence-backed estimate"
        return "Unknown — not established by the cited evidence"
    if isinstance(value, bool):
        rendered = "Yes" if value else "No"
    else:
        rendered = str(value)
    unit = fact.get("unit")
    if not unit:
        return rendered
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{rendered} {unit}"
    return f"{rendered} ({unit})"


def _script_safe_payload(payload: dict[str, Any]) -> str:
    return scene_pipeline.canonical_payload(payload).replace("</", "<\\/")


def _claim_card(
    claim: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
    topology_targets: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    fact_cards: list[dict[str, Any]] = []
    for fact_ref in claim["fact_refs"]:
        ledger_id, fact_id = fact_ref.split(":", 1)
        ledger = ledgers[ledger_id]
        fact = ledger["facts"][fact_id]
        sources = []
        for source_id in fact["source_ids"]:
            source = ledger["sources"][source_id]
            sources.append(
                {
                    "id": source_id,
                    "publisher": source["publisher"],
                    "title": source["title"],
                    "url": source["url"],
                    "publication_date": source["publication_date"],
                    "review_date": source["review_date"],
                    "accessed_as_of": source["accessed_as_of"],
                    "date_note": source["date_note"],
                }
            )
        fact_cards.append(
            {
                "ref": fact_ref,
                "value": _display_value(fact),
                "scope": fact["scope"],
                "basis": fact["basis"],
                "lifecycle": fact["lifecycle"],
                "posture": fact["posture"],
                "as_of": fact["as_of"],
                "sources": sources,
                "topology_targets": list(topology_targets.get(fact_ref, [])),
            }
        )
        if claim["binding"] == "topology" and not fact_cards[-1]["topology_targets"]:
            raise CourseRuntimeError(
                f"topology claim {claim['id']} fact {fact_ref} has no selected owner"
            )
    return {
        "id": claim["id"],
        "assertion": claim["assertion"],
        "binding": claim["binding"],
        "facts": fact_cards,
    }


def _selected_fact_targets(
    segment: dict[str, Any], master: dict[str, Any], master_ledger_id: str
) -> dict[str, list[dict[str, Any]]]:
    """Resolve each master-ledger fact to its exact selected topology owners."""
    node_map = {node["id"]: node for node in master["nodes"]}
    edge_map = {edge["id"]: edge for edge in master["edges"]}
    targets: dict[str, list[dict[str, Any]]] = {}
    for node_id in segment["node_ids"]:
        node = node_map[node_id]
        target = {
            "kind": "node",
            "id": node_id,
            "label": node["label"],
            "presence": node["presence"],
            "lifecycle": node["lifecycle"],
        }
        for fact_id in node.get("fact_ids") or []:
            targets.setdefault(f"{master_ledger_id}:{fact_id}", []).append(target)
    for edge_id in segment["edge_ids"]:
        edge = edge_map[edge_id]
        target = {
            "kind": "edge",
            "id": edge_id,
            "label": f"{node_map[edge['from']]['label']} → {node_map[edge['to']]['label']}",
            "presence": edge["presence"],
            "lifecycle": edge["lifecycle"],
        }
        for fact_id in edge.get("fact_ids") or []:
            targets.setdefault(f"{master_ledger_id}:{fact_id}", []).append(target)
    return targets


def _frame_for_segment(
    segment: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
    *,
    resolved_label_copy: dict[str, str] | None = None,
) -> dict[str, Any]:
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    anchor = camera_map[segment["camera"]["anchor"]]
    render_mode = "3d" if anchor["mode"] == "3d" else "2d"
    if render_mode == "3d":
        return shots._derive_3d_frame(
            segment["node_ids"], segment["edge_ids"], anchor, scene
        )

    return shots._derive_2d_frame(
        segment["node_ids"],
        segment["edge_ids"],
        anchor,
        master,
        layout,
        scene,
        resolved_label_copy=resolved_label_copy,
    )


def _resolved_2d_frame_label_copy(
    course: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    evidence: dict[str, Any],
    visual_map: dict[str, dict[str, Any]],
) -> dict[str, dict[str, str]]:
    """Bind 2D frame labels to exact visual selection and ledger-resolved copy."""
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    resolved_by_segment: dict[str, dict[str, str]] = {}
    for act in course["acts"]:
        for segment in act["segments"]:
            if camera_map[segment["camera"]["anchor"]]["mode"] == "3d":
                continue
            visual = visual_map.get(segment["id"])
            selected_copy_ids = visual["label_copy_ids"] if visual else []
            unknown_grammar_ids = sorted(
                copy_id
                for copy_id in selected_copy_ids
                if copy_id.startswith("legend_") and copy_id not in _LEGEND_GRAMMAR_CUES
            )
            if unknown_grammar_ids:
                raise CourseRuntimeError(
                    f"segment {segment['id']}: unknown fixed grammar key IDs "
                    f"{unknown_grammar_ids}"
                )
            frame_copy_ids = [
                copy_id
                for copy_id in selected_copy_ids
                if copy_id not in _LEGEND_GRAMMAR_CUES
            ]
            copy_ids = list(
                dict.fromkeys([*frame_copy_ids, *segment["camera"]["reveal_copy_ids"]])
            )
            resolved: dict[str, str] = {}
            for copy_id in copy_ids:
                rendered = layout_pipeline.resolve_copy(
                    master,
                    evidence,
                    copy_id,
                    include_hidden=True,
                )
                if not isinstance(rendered, str) or not rendered:
                    raise CourseRuntimeError(
                        f"segment {segment['id']}: 2D frame copy {copy_id!r} "
                        "did not resolve to text"
                    )
                resolved[copy_id] = rendered
            resolved_by_segment[segment["id"]] = resolved
    return resolved_by_segment


def _validate_course_inputs(
    course: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
) -> None:
    from . import validate as validate_pipeline

    validate_pipeline.validate_course_inputs(course, master, ledgers, cameras)


def compile_registry(
    course: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
    visuals: dict[str, Any],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Compile all 26 segments into presenter-controlled course states."""
    scene_pipeline.validate(master, scene, cameras)
    _validate_course_inputs(course, cameras, master, ledgers)
    if len(course.get("acts") or []) != EXPECTED_ACTS:
        raise CourseRuntimeError(
            f"expected {EXPECTED_ACTS} course acts, found {len(course.get('acts') or [])}"
        )

    visual_map = _compiled_visuals(course, cameras, master, visuals)
    master_evidence = ledgers[course["meta"]["master_evidence_ledger"]]
    resolved_label_copy_by_segment = _resolved_2d_frame_label_copy(
        course,
        cameras,
        master,
        master_evidence,
        visual_map,
    )
    planned_registry = shots.compile_registry(
        course,
        cameras,
        master,
        layout,
        scene,
        source_digest=source_digest,
        resolved_label_copy_by_segment=resolved_label_copy_by_segment,
    )
    planned_by_segment = {
        shot["segment_id"]: shot for shot in planned_registry["shots"]
    }
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    node_labels = {node["id"]: node["label"] for node in master["nodes"]}
    edge_labels = {
        edge["id"]: f"{node_labels[edge['from']]} → {node_labels[edge['to']]}"
        for edge in master["edges"]
    }

    compiled: list[dict[str, Any]] = []
    master_ledger_id = course["meta"]["master_evidence_ledger"]
    boundary_note = layout_pipeline.resolve_copy(
        master,
        ledgers[master_ledger_id],
        "footnote",
        include_hidden=True,
    )
    if not isinstance(boundary_note, str) or not boundary_note:
        raise CourseRuntimeError(
            "master footnote must resolve to protected boundary copy"
        )
    for act_sequence, act in enumerate(course["acts"], start=1):
        for segment in act["segments"]:
            request = segment["camera"]
            anchor = camera_map[request["anchor"]]
            if request["status"] == "planned":
                shot = planned_by_segment[segment["id"]]
                frame = shot["frame"]
                render_mode = shot["render_mode"]
            else:
                frame = _frame_for_segment(
                    segment,
                    cameras,
                    master,
                    layout,
                    scene,
                    resolved_label_copy=resolved_label_copy_by_segment.get(
                        segment["id"]
                    ),
                )
                render_mode = "3d" if anchor["mode"] == "3d" else "2d"

            topology_targets = _selected_fact_targets(segment, master, master_ledger_id)
            compiled.append(
                {
                    "sequence": len(compiled) + 1,
                    "act_sequence": act_sequence,
                    "act_id": act["id"],
                    "act_title": act["title"],
                    "act_objective": act["learning_objective"],
                    "act_evidence_ledgers": list(act["evidence_ledgers"]),
                    "id": request["shot"],
                    "segment_id": segment["id"],
                    "title": segment["title"],
                    "opening_question": segment["opening_question"],
                    "learning_objective": segment["learning_objective"],
                    "boundary_note": boundary_note,
                    "status": (
                        "derived" if request["status"] == "planned" else "existing"
                    ),
                    "mode": request["mode"],
                    "render_mode": render_mode,
                    "camera_anchor": request["anchor"],
                    "evidence_readiness": segment["evidence"]["readiness"],
                    "focus_nodes": list(segment["node_ids"]),
                    "focus_node_labels": [
                        node_labels[node_id] for node_id in segment["node_ids"]
                    ],
                    "focus_edges": list(segment["edge_ids"]),
                    "focus_edge_labels": [
                        edge_labels[edge_id] for edge_id in segment["edge_ids"]
                    ],
                    "reveal_ids": list(request["reveal_ids"]),
                    "reveal_copy_ids": list(request["reveal_copy_ids"]),
                    "frame": frame,
                    "claims": [
                        _claim_card(claim, ledgers, topology_targets)
                        for claim in segment["evidence"]["claims"]
                    ],
                    "promotion_guards": list(segment["evidence"]["promotion_guards"]),
                    "promotion_guard_warnings": [
                        {
                            "id": guard,
                            "warning": PROMOTION_GUARD_WARNINGS[guard],
                        }
                        for guard in segment["evidence"]["promotion_guards"]
                    ],
                    "blocking_research": list(segment["evidence"]["blocking_research"]),
                    "visual": visual_map.get(
                        segment["id"],
                        {
                            "label_policy": "context",
                            "show_legend": False,
                            "label_node_ids": [],
                            "label_copy_ids": [],
                            "annotation": None,
                        },
                    ),
                    "depends_on": list(segment["depends_on"]),
                    "transition": (
                        dict(segment["transition"])
                        if segment["transition"] is not None
                        else None
                    ),
                }
            )

    if len(compiled) != EXPECTED_SEGMENTS:
        raise CourseRuntimeError(
            f"expected {EXPECTED_SEGMENTS} course segments, found {len(compiled)}"
        )
    readiness = [segment["evidence_readiness"] for segment in compiled]
    registry = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "act_count": EXPECTED_ACTS,
        "segment_count": len(compiled),
        "evidence_ready_count": readiness.count("evidence_ready"),
        "research_required_count": readiness.count("research_required"),
        "segments": compiled,
    }
    forbidden = {
        key.casefold()
        for key in _walk_keys(registry)
        if key.casefold() in FORBIDDEN_RUNTIME_KEYS
    }
    if forbidden:
        raise CourseRuntimeError(
            f"course runtime contains timing or scripting fields: {sorted(forbidden)}"
        )
    return registry


def _must_replace(text: str, old: str, new: str) -> str:
    if old not in text:
        raise CourseRuntimeError(f"course player template drift: {old[:80]!r}")
    return text.replace(old, new)


COURSE_CSS = r"""
  :root { --head: 196px; --notes: 430px; }
  #masthead { height: var(--head); min-height: var(--head); overflow: hidden; }
  #opening-question { margin: 5px 0 0; font-size: 11px; font-weight: 700; line-height: 1.25; }
  #objective { margin: 4px 0 0; color: var(--muted); font-size: 9px; line-height: 1.25; }
  #boundary-note { margin: 4px 0 0; color: var(--muted); font-size: 10px; line-height: 1.2; }
  #boundary-compact { display: none; }
  #scope-summary { color: var(--muted); }
  #focus-key {
    margin: 6px 0 0;
    max-width: min(920px, calc(100vw - var(--rail) - 250px));
    display: flex;
    gap: 5px;
    list-style: none;
    overflow-x: auto;
    padding: 0 0 2px;
    scrollbar-width: thin;
  }
  #focus-key[hidden] { display: none; }
  .focus-chip {
    flex: 0 0 auto;
    padding: 3px 6px;
    border: 1px solid var(--faint);
    background: var(--paper);
    font-size: 10px;
    font-weight: 650;
    line-height: 1.15;
    white-space: nowrap;
  }
  .focus-index {
    display: inline-grid;
    width: 14px;
    height: 14px;
    margin-right: 4px;
    place-items: center;
    border-radius: 50%;
    background: var(--ink);
    color: var(--paper);
    font-size: __FOCUS_KEY_INDEX_FONT_PX__px;
    font-variant-numeric: tabular-nums;
    line-height: 1;
  }
  .focus-copy { min-width: 0; }
  .focus-chip[data-key-role="grammar"] {
    display: grid;
    grid-template-columns: 28px minmax(0, 1fr);
    column-gap: 4px;
    align-items: center;
  }
  @media (min-width: 521px) {
    .focus-chip[data-label-id="legend_direction"] { grid-column: span 2; }
  }
  .focus-swatch {
    position: relative;
    width: 24px;
    height: 12px;
    align-self: center;
  }
  .focus-swatch::before {
    position: absolute;
    top: 50%;
    right: 0;
    left: 0;
    border-top: 2px solid var(--ink);
    content: "";
    transform: translateY(-50%);
  }
  .focus-swatch[data-cue="carrier"]::before {
    height: 4px;
    border: 0;
    background: linear-gradient(90deg, #143f70 0 25%, #2f9e8f 25% 50%, #d3552c 50% 75%, #b3261e 75%);
  }
  .focus-swatch[data-cue="direction"]::after {
    position: absolute;
    top: 50%;
    right: 0;
    width: 6px;
    height: 6px;
    border-top: 2px solid var(--ink);
    border-right: 2px solid var(--ink);
    content: "";
    transform: translateY(-50%) rotate(45deg);
  }
  .focus-swatch[data-cue="posture"] {
    display: grid;
    place-items: center;
    border: 1px solid var(--ink);
    font-size: 10px;
    font-weight: 700;
    line-height: 1;
  }
  .focus-swatch[data-cue="posture"]::before { position: static; border: 0; content: "Aa"; transform: none; }
  .focus-swatch[data-cue="solid"]::before { border-top-style: solid; }
  .focus-swatch[data-cue="dotted"]::before { border-top-style: dotted; }
  .focus-swatch[data-cue="dashed"]::before { border-top-style: dashed; }
  .focus-swatch[data-cue="conceptual"]::before { border-top-style: dashed; opacity: .45; }
  #focus-markers {
    position: absolute;
    z-index: 10;
    inset: 0;
    overflow: hidden;
    pointer-events: none;
  }
  .focus-marker {
    position: absolute;
    width: 20px;
    height: 20px;
    display: grid;
    place-items: center;
    transform: translate(-50%, -50%);
    border: 1px solid var(--ink);
    border-radius: 50%;
    background: var(--paper);
    color: var(--ink);
    box-shadow: 0 0 0 2px color-mix(in srgb, var(--paper) 82%, transparent);
    font-size: 10px;
    font-weight: 800;
    font-variant-numeric: tabular-nums;
    line-height: 1;
  }
  .focus-leader {
    position: absolute;
    height: 1px;
    transform-origin: 0 50%;
    background: var(--ink);
    opacity: .72;
  }
  #transport {
    grid-template-columns: auto minmax(0, 1fr) minmax(128px, auto) minmax(128px, auto) auto;
    grid-template-areas: "previous note teaching evidence next";
  }
  #previous { grid-area: previous; }
  #manual-note { grid-area: note; }
  #teaching-toggle { grid-area: teaching; }
  #evidence-toggle { grid-area: evidence; }
  #next { grid-area: next; }
  #map-svg [data-focus-state="focused"] [stroke-width],
  #map-svg [data-focus-state="focused"] [stroke-dasharray] {
    vector-effect: non-scaling-stroke;
  }
  #three-mount .node-label small {
    display: none;
  }
  #three-mount .node-label[data-presence="teaching_reference"] { border-style: dashed; }
  #teaching-overlay {
    position: absolute;
    z-index: 9;
    bottom: calc(var(--transport) + 22px);
    left: calc(var(--rail) + 24px);
    width: min(__TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX__px, calc(100vw - var(--rail) - 48px));
    padding: 14px 16px 15px;
    background: var(--paper);
    border: var(--rule) solid var(--ink);
    box-shadow: 8px 8px 0 color-mix(in srgb, var(--faint) 70%, transparent);
    pointer-events: none;
  }
  #teaching-overlay[hidden] { display: none; }
  #teaching-overlay[data-position="right"],
  #teaching-overlay[data-position$="-right"] { right: 24px; left: auto; }
  #teaching-overlay[data-position^="top-"] {
    top: calc(var(--head) + 22px);
    bottom: auto;
  }
  #teaching-kicker { margin: 0; color: var(--muted); font-size: 9px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
  #teaching-title { margin: 5px 0 10px; font-size: 15px; line-height: 1.15; }
  #teaching-items { margin: 0; padding: 0; display: grid; gap: 7px; list-style: none; }
  #teaching-items li { padding: 7px 9px; background: color-mix(in srgb, var(--paper) 88%, transparent); border-left: 3px solid var(--ink); font-size: 11px; font-weight: 650; line-height: 1.25; }
  #teaching-overlay[data-kind="comparison"] #teaching-items,
  #teaching-overlay[data-kind="routes"] #teaching-items { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  #teaching-overlay[data-kind="parallel"] #teaching-items { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  #teaching-overlay[data-kind="parallel"] #teaching-items li:first-child,
  #teaching-overlay[data-kind="parallel"] #teaching-items li:last-child { grid-column: 1 / -1; }
  #teaching-overlay[data-kind="routes"] #teaching-items li:last-child { grid-column: 1 / -1; border-left-color: #9c5f20; }
  #teaching-overlay[data-kind="sequence"] #teaching-items { counter-reset: teaching-step; }
  #teaching-overlay[data-kind="sequence"] #teaching-items li { counter-increment: teaching-step; display: grid; grid-template-columns: 18px minmax(0, 1fr); gap: 7px; }
  #teaching-overlay[data-kind="sequence"] #teaching-items li::before { content: counter(teaching-step); color: var(--muted); font-size: 9px; font-variant-numeric: tabular-nums; }
  #teaching-overlay[data-kind="funnel"] #teaching-items li { margin-inline: auto; }
  #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(1) { width: 100%; }
  #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(2) { width: 90%; }
  #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(3) { width: 80%; }
  #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(4) { width: 70%; }
  #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(5) { width: 60%; }
  #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li {
    display: grid;
    grid-template-columns: 30px minmax(0, 1fr);
    gap: 7px;
    align-items: center;
  }
  #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li::before {
    content: "";
    width: 28px;
    border-top: 2px solid var(--ink);
  }
  #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li:nth-child(2)::before { border-top-style: dotted; }
  #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li:nth-child(3)::before { border-top-style: dashed; }
  #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li:nth-child(4)::before { border-color: var(--faint); border-top-style: dashed; }
  #teaching-toggle { display: none; }
  #teaching-toggle:not([hidden]) { display: inline-grid; place-items: center; }
  #evidence-toggle,
  #teaching-toggle {
    min-width: 128px;
    height: 38px;
    padding: 0 12px;
    border: var(--rule) solid var(--ink);
    background: transparent;
    cursor: pointer;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
  }
  #teaching-close { display: none; }
  #notes-panel {
    position: absolute;
    z-index: 24;
    top: var(--head);
    right: 0;
    bottom: var(--transport);
    width: min(var(--notes), calc(100vw - var(--rail)));
    padding: 19px 20px 28px;
    overflow-y: auto;
    background: color-mix(in srgb, var(--paper) 98%, transparent);
    border-left: var(--rule) solid var(--ink);
    transform: translateX(100%);
    transition: transform 160ms ease-out;
  }
  #notes-panel[data-open="true"] { transform: translateX(0); }
  #notes-close {
    float: right;
    width: 34px;
    height: 30px;
    border: 1px solid var(--ink);
    background: transparent;
    cursor: pointer;
  }
  #notes-kicker { margin: 0; color: var(--muted); font-size: 9px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
  #notes-title { margin: 6px 44px 15px 0; font-size: 18px; line-height: 1.15; }
  .evidence-summary { margin: 0; padding: 10px 11px; border: 1px solid var(--faint); font-size: 10px; font-weight: 700; line-height: 1.35; }
  .notes-section { margin-top: 18px; padding-top: 13px; border-top: 1px solid var(--faint); }
  .notes-section h3 { margin: 0 0 8px; font-size: 10px; letter-spacing: .06em; text-transform: uppercase; }
  .notes-section p, .notes-section li { font-size: 10px; line-height: 1.45; }
  .notes-section ul { margin: 0; padding-left: 18px; }
  .notes-section li + li { margin-top: 8px; }
  .disclosure > summary { cursor: pointer; font-size: 10px; font-weight: 700; letter-spacing: .04em; text-transform: uppercase; }
  .disclosure[open] > summary { margin-bottom: 10px; }
  .guard-list strong { display: block; margin-bottom: 2px; font-size: 9px; text-transform: uppercase; }
  .claim-card { margin-top: 11px; padding: 11px; border: 1px solid var(--faint); }
  .claim-card h4 { margin: 0 0 7px; font-size: 10px; }
  .claim-card p { margin: 5px 0 0; }
  .fact-value { font-weight: 700; }
  .fact-details { margin-top: 7px; }
  .fact-details > summary { cursor: pointer; color: var(--muted); font-size: 9px; }
  .source-list { margin-top: 6px !important; color: var(--muted); }
  .source-list a { color: inherit; }
  .ready { border-left: 5px solid #2f6f4e !important; }
  .gated { border-left: 5px solid #9c5f20 !important; }
  @media (min-width: 1101px) {
    #scope-summary {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    #focus-key {
      width: 100%;
      max-width: none;
      display: grid;
      grid-template-columns: repeat(__DESKTOP_FOCUS_KEY_COLUMNS__, minmax(0, 1fr));
      gap: __DESKTOP_FOCUS_KEY_GAP_PX__px;
      overflow-x: visible;
      padding-bottom: 0;
      scrollbar-width: auto;
    }
    .focus-chip {
      min-width: 0;
      display: grid;
      grid-template-columns: __DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX__px minmax(0, 1fr);
      column-gap: __DESKTOP_FOCUS_KEY_INDEX_GAP_PX__px;
      align-items: center;
      padding: __DESKTOP_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX__px __DESKTOP_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX__px;
      font-size: __DESKTOP_FOCUS_KEY_FONT_PX__px;
      line-height: __DESKTOP_FOCUS_KEY_LINE_HEIGHT__;
      white-space: nowrap;
    }
    .focus-index {
      width: __DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX__px;
      height: __DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX__px;
      margin-right: 0;
      font-size: __FOCUS_KEY_INDEX_FONT_PX__px;
    }
    .focus-chip[data-key-role="grammar"] {
      grid-template-columns: __DESKTOP_FOCUS_KEY_SWATCH_WIDTH_PX__px minmax(0, 1fr);
      column-gap: __DESKTOP_FOCUS_KEY_INDEX_GAP_PX__px;
    }
    .focus-chip[data-key-role="grammar"] .focus-swatch { width: __DESKTOP_FOCUS_KEY_SWATCH_WIDTH_PX__px; }
  }
  @media (max-width: 1100px) {
    #map-stage { padding: 10px; }
    #objective,
    #scope-ids {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    #boundary-full {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    #boundary-compact {
      display: block;
      max-width: 100%;
      white-space: normal;
    }
  }
  @media (max-width: 1100px) and (min-width: 821px) {
    :root { --head: 184px; }
    #masthead { grid-template-columns: minmax(0, 1fr); }
    #posture { display: none; }
  }
  @media (max-width: 1100px) and (min-width: 821px) and (min-height: 561px) {
    #focus-key {
      width: min(100%, __TABLET_FOCUS_KEY_CONTENT_WIDTH_PX__px);
      max-width: __TABLET_FOCUS_KEY_CONTENT_WIDTH_PX__px;
      display: grid;
      grid-template-columns: repeat(__TABLET_FOCUS_KEY_COLUMNS__, minmax(0, 1fr));
      gap: __TABLET_FOCUS_KEY_GAP_PX__px;
      overflow-x: visible;
      padding-bottom: 0;
      scrollbar-width: auto;
    }
    .focus-chip {
      min-width: 0;
      display: grid;
      grid-template-columns: __TABLET_FOCUS_KEY_INDEX_WIDTH_PX__px minmax(0, 1fr);
      column-gap: __TABLET_FOCUS_KEY_INDEX_GAP_PX__px;
      align-items: center;
      padding: 0 __TABLET_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX__px;
      font-size: __TABLET_FOCUS_KEY_FONT_PX__px;
      line-height: __TABLET_FOCUS_KEY_LINE_HEIGHT__;
      white-space: nowrap;
    }
    .focus-index {
      width: __TABLET_FOCUS_KEY_INDEX_WIDTH_PX__px;
      height: __TABLET_FOCUS_KEY_INDEX_WIDTH_PX__px;
      margin-right: 0;
      font-size: __TABLET_FOCUS_KEY_FONT_PX__px;
    }
    .focus-chip[data-key-role="grammar"] {
      grid-template-columns: __TABLET_FOCUS_KEY_SWATCH_WIDTH_PX__px minmax(0, 1fr);
      column-gap: __TABLET_FOCUS_KEY_INDEX_GAP_PX__px;
    }
    .focus-chip[data-key-role="grammar"] .focus-swatch { width: __TABLET_FOCUS_KEY_SWATCH_WIDTH_PX__px; }
  }
  @media (max-width: 820px) {
    :root { --head: 156px; }
    #masthead { grid-template-columns: minmax(0, 1fr); padding: 12px 14px 10px; }
    #posture { display: none; }
    #evidence-toggle { min-width: 92px; }
    #focus-key { max-width: calc(100vw - var(--rail) - 30px); }
    #notes-panel { width: calc(100vw - var(--rail)); }
    #teaching-overlay,
    #teaching-overlay[data-position="right"],
    #teaching-overlay[data-position$="-right"],
    #teaching-overlay[data-position^="top-"] {
      top: auto;
      right: auto;
      bottom: calc(var(--transport) + 14px);
      left: calc(var(--rail) + 14px);
      width: calc(100vw - var(--rail) - 28px);
      padding: 9px 12px 10px;
      box-shadow: 5px 5px 0 color-mix(in srgb, var(--faint) 70%, transparent);
    }
    #teaching-title { margin: 3px 0 5px; font-size: 13px; }
    #teaching-items { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 5px; }
    #teaching-items li { padding: 6px 7px; font-size: 10px; }
    #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li {
      grid-template-columns: 24px minmax(0, 1fr);
      gap: 6px;
    }
    #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li::before { width: 22px; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(1) { width: 100%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(2) { width: 96%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(3) { width: 92%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(4) { width: 88%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(5) { width: 84%; }
  }
  @media (max-width: 520px) {
    :root { --head: __PORTRAIT_MASTHEAD_HEIGHT_PX__px; }
    #eyebrow { line-height: 1.2; }
    #transport {
      grid-template-columns: auto minmax(0, 1fr) minmax(0, 1fr) auto;
      grid-template-areas: "previous teaching evidence next";
    }
    #previous { grid-area: previous; }
    #teaching-toggle { grid-area: teaching; }
    #evidence-toggle { grid-area: evidence; }
    #next { grid-area: next; }
    #manual-note {
      position: absolute;
      width: 1px;
      height: 1px;
      padding: 0;
      margin: -1px;
      overflow: hidden;
      clip: rect(0, 0, 0, 0);
      white-space: nowrap;
      border: 0;
    }
    #evidence-toggle,
    #teaching-toggle { min-width: 0; padding-inline: 6px; }
    #teaching-toggle:not([hidden]) { display: inline-grid; place-items: center; }
    #focus-key {
      max-width: none;
      display: grid;
      grid-template-columns: repeat(__PORTRAIT_FOCUS_KEY_COLUMNS__, minmax(0, 1fr));
      gap: __PORTRAIT_FOCUS_KEY_GAP_PX__px;
      overflow-x: visible;
      padding-bottom: 0;
      scrollbar-width: auto;
    }
    .focus-chip {
      min-width: 0;
      display: grid;
      grid-template-columns: 14px minmax(0, 1fr);
      column-gap: 4px;
      align-items: start;
      white-space: normal;
      overflow-wrap: anywhere;
    }
    .focus-index { margin-right: 0; }
    .focus-chip[data-key-role="grammar"] {
      grid-template-columns: __PORTRAIT_FOCUS_KEY_SWATCH_WIDTH_PX__px minmax(0, 1fr);
    }
    .focus-chip[data-key-role="grammar"] .focus-swatch { width: __PORTRAIT_FOCUS_KEY_SWATCH_WIDTH_PX__px; }
    #stage[data-teaching-open="true"] #three-mount,
    #stage[data-teaching-open="true"] #map-stage,
    #stage[data-teaching-open="true"] #focus-markers { visibility: hidden; }
    #teaching-overlay[data-mobile-drawer="true"]:not([hidden]) {
      z-index: 20;
      top: var(--head);
      right: 0;
      bottom: var(--transport);
      left: var(--rail);
      width: auto;
      padding: 12px 14px 18px;
      overflow-x: hidden;
      overflow-y: auto;
      box-shadow: none;
      pointer-events: auto;
    }
    #teaching-overlay[data-mobile-drawer="true"]:not([hidden]) #teaching-close {
      display: block;
      float: right;
      width: 34px;
      height: 30px;
      border: 1px solid var(--ink);
      background: var(--paper);
      cursor: pointer;
    }
  }
  @media (max-height: 560px) and (min-width: 821px) {
    :root { --rail: 72px; --head: __SHORT_MASTHEAD_HEIGHT_PX__px; --transport: 58px; }
    #rail-heading h1 { display: none; }
    #rail-heading { padding-inline: 8px; }
    .shot-button { grid-template-columns: 1fr; padding-inline: 8px; }
    .shot-number { text-align: center; }
    .shot-name, .segment-name { display: none; }
    #masthead { padding: 6px 10px; }
    #title { margin-top: 2px; font-size: 16px; }
    #opening-question { margin-top: 2px; font-size: __SHORT_OPENING_QUESTION_FONT_PX__px; }
    #boundary-note { margin-top: 2px; line-height: 1.1; }
    #scope-summary,
    #scope-ids { position: absolute; width: 1px; height: 1px; overflow: hidden; clip: rect(0, 0, 0, 0); }
    #focus-key {
      width: min(100%, __SHORT_FOCUS_KEY_CONTENT_WIDTH_PX__px);
      max-width: __SHORT_FOCUS_KEY_CONTENT_WIDTH_PX__px;
      margin-top: 2px;
      display: grid;
      grid-template-columns: repeat(__SHORT_FOCUS_KEY_COLUMNS__, minmax(0, 1fr));
      gap: __SHORT_FOCUS_KEY_GAP_PX__px;
      overflow-x: visible;
      padding-bottom: 0;
      scrollbar-width: auto;
    }
    .focus-chip {
      min-width: 0;
      display: grid;
      grid-template-columns: __SHORT_FOCUS_KEY_INDEX_WIDTH_PX__px minmax(0, 1fr);
      column-gap: __SHORT_FOCUS_KEY_INDEX_GAP_PX__px;
      align-items: center;
      padding: 0 __SHORT_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX__px;
      font-size: __SHORT_FOCUS_KEY_FONT_PX__px;
      line-height: __SHORT_FOCUS_KEY_LINE_HEIGHT__;
      white-space: nowrap;
    }
    .focus-index {
      width: __SHORT_FOCUS_KEY_INDEX_WIDTH_PX__px;
      height: __SHORT_FOCUS_KEY_INDEX_WIDTH_PX__px;
      margin-right: 0;
      font-size: __SHORT_FOCUS_KEY_FONT_PX__px;
    }
    .focus-chip[data-key-role="grammar"] {
      grid-template-columns: __SHORT_FOCUS_KEY_SWATCH_WIDTH_PX__px minmax(0, 1fr);
      column-gap: __SHORT_FOCUS_KEY_INDEX_GAP_PX__px;
    }
    .focus-chip[data-key-role="grammar"] .focus-swatch { width: __SHORT_FOCUS_KEY_SWATCH_WIDTH_PX__px; }
    #transport { min-height: var(--transport); padding-block: 7px; }
    #teaching-overlay,
    #teaching-overlay[data-position^="top-"] {
      top: auto;
      right: auto;
      bottom: calc(var(--transport) + __TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX__px);
      left: calc(var(--rail) + __TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX__px);
      width: min(390px, calc((100vw - var(--rail)) * .52));
      padding: __SHORT_TEACHING_OVERLAY_PADDING_BLOCK_PX__px 8px;
      box-shadow: 4px 4px 0 color-mix(in srgb, var(--faint) 70%, transparent);
    }
    #teaching-overlay[data-position="right"],
    #teaching-overlay[data-position$="-right"] { right: __TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX__px; left: auto; }
    #teaching-kicker { font-size: 9px; }
    #teaching-title { margin: 2px 0 5px; font-size: 11px; }
    #teaching-items,
    #teaching-overlay[data-kind="comparison"] #teaching-items,
    #teaching-overlay[data-kind="parallel"] #teaching-items,
    #teaching-overlay[data-kind="routes"] #teaching-items {
      grid-template-columns: repeat(auto-fit, minmax(90px, 1fr));
      gap: 4px;
    }
    #teaching-items li,
    #teaching-overlay[data-kind="sequence"] #teaching-items li,
    #teaching-overlay[data-kind="funnel"] #teaching-items li {
      width: 100%;
      margin: 0;
      padding: __SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX__px 5px;
      display: block;
      font-size: 10px;
      line-height: 1.15;
    }
    #teaching-overlay[data-kind="sequence"] #teaching-items li { position: relative; padding-right: 19px; }
    #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li {
      display: grid;
      grid-template-columns: 24px minmax(0, 1fr);
      gap: 6px;
    }
    #teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li::before { width: 22px; }
    #teaching-overlay[data-kind="sequence"] #teaching-items li::before {
      position: absolute;
      top: 3px;
      right: 3px;
      width: 13px;
      height: 13px;
      display: grid;
      place-items: center;
      border: 1px solid var(--muted);
      border-radius: 50%;
      content: counter(teaching-step);
      font-size: 9px;
      line-height: 1;
    }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(1) { width: 100%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(2) { width: 96%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(3) { width: 92%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(4) { width: 88%; }
    #teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(5) { width: 84%; }
    #teaching-overlay[data-kind="routes"] #teaching-items li:last-child { grid-column: auto; }
    #teaching-overlay[data-kind="parallel"] #teaching-items {
      grid-template-columns: repeat(2, minmax(90px, 1fr));
    }
    #teaching-overlay[data-kind="parallel"] #teaching-items li:first-child,
    #teaching-overlay[data-kind="parallel"] #teaching-items li:last-child { grid-column: 1 / -1; }
  }
"""


ANNOTATION_KIND_CUE_CONTRACT = {
    "sequence": {
        "cue": "number_badges",
        "profiles": {
            "short_height": (
                '#teaching-overlay[data-kind="sequence"] #teaching-items { counter-reset: teaching-step; }',
                '#teaching-overlay[data-kind="sequence"] #teaching-items li { position: relative; padding-right: 19px; }',
                "content: counter(teaching-step);",
            ),
        },
    },
    "funnel": {
        "cue": "stepped_widths",
        "profiles": {
            profile: tuple(
                f'#teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child({index}) {{ width: {width}%; }}'
                for index, width in enumerate(widths, start=1)
            )
            for profile, widths in {
                "standard": (100, 90, 80, 70, 60),
                "narrow": (100, 96, 92, 88, 84),
                "short_height": (100, 96, 92, 88, 84),
            }.items()
        },
    },
    "parallel": {
        "cue": "split_parallel_converge",
        "profiles": {
            "standard": (
                '#teaching-overlay[data-kind="parallel"] #teaching-items { grid-template-columns: repeat(2, minmax(0, 1fr)); }',
                '#teaching-overlay[data-kind="parallel"] #teaching-items li:first-child,',
                '#teaching-overlay[data-kind="parallel"] #teaching-items li:last-child { grid-column: 1 / -1; }',
            ),
            "narrow": (
                '#teaching-overlay[data-kind="parallel"] #teaching-items { grid-template-columns: repeat(2, minmax(0, 1fr)); }',
                '#teaching-overlay[data-kind="parallel"] #teaching-items li:first-child,',
                '#teaching-overlay[data-kind="parallel"] #teaching-items li:last-child { grid-column: 1 / -1; }',
            ),
            "short_height": (
                '#teaching-overlay[data-kind="parallel"] #teaching-items {\n      grid-template-columns: repeat(2, minmax(90px, 1fr));',
                '#teaching-overlay[data-kind="parallel"] #teaching-items li:first-child,',
                '#teaching-overlay[data-kind="parallel"] #teaching-items li:last-child { grid-column: 1 / -1; }',
            ),
        },
    },
}


def compact_kind_cue_contract(kind: str, profile: str | None) -> dict[str, Any]:
    """Return whether runtime CSS preserves an annotation's structural cue."""
    contract = ANNOTATION_KIND_CUE_CONTRACT.get(kind)
    required_css = None if contract is None else contract["profiles"].get(profile)
    if required_css is None:
        return {
            "required": False,
            "cue": "not_applicable",
            "required_css": [],
            "missing_css": [],
            "preserved": None,
        }
    required_css = list(required_css)
    missing_css = [token for token in required_css if token not in COURSE_CSS]
    return {
        "required": True,
        "cue": contract["cue"],
        "required_css": required_css,
        "missing_css": missing_css,
        "preserved": not missing_css,
    }


NOTES_HTML = r"""
<aside id="teaching-overlay" role="region" data-position="left" data-mobile-drawer="true" aria-labelledby="teaching-title" hidden inert>
  <button id="teaching-close" type="button" aria-label="Close teaching focus">×</button>
  <p id="teaching-kicker">Teaching focus</p>
  <h3 id="teaching-title"></h3>
  <ol id="teaching-items"></ol>
</aside>
<aside id="notes-panel" role="dialog" aria-modal="true" data-open="false" aria-labelledby="notes-title" aria-hidden="true" inert>
  <button id="notes-close" type="button" aria-label="Close instructor evidence">×</button>
  <p id="notes-kicker"></p>
  <h2 id="notes-title"></h2>
  <div id="notes-body"></div>
</aside>
"""


NOTES_JS = r"""
const compactFocusLabels = __COMPACT_FOCUS_LABELS__;
const legendGrammarCues = __LEGEND_GRAMMAR_CUES__;
const focusKeyCopyById = data.focus_key_copy || {};

function compactFocusLabel(id) {
  return compactFocusLabels[id] || id.replaceAll("_", " ");
}

function notesSection(title) {
  const section = document.createElement("section");
  section.className = "notes-section";
  const heading = document.createElement("h3");
  heading.textContent = title;
  section.appendChild(heading);
  return section;
}

function paragraph(text, className = "") {
  const value = document.createElement("p");
  value.textContent = text;
  if (className) value.className = className;
  return value;
}

function countLabel(count, singular) {
  return `${count} ${count === 1 ? singular : `${singular}s`}`;
}

function markerBoxesOverlap(left, right, gap = 3) {
  return !(
    left.right + gap <= right.left ||
    left.left >= right.right + gap ||
    left.bottom + gap <= right.top ||
    left.top >= right.bottom + gap
  );
}

function focusMarkerOffsets() {
  const offsets = [];
  for (let x = -2; x <= 2; x += 1) {
    for (let y = -2; y <= 2; y += 1) {
      const offset = [x * 22, y * 22];
      if (Math.hypot(...offset) <= 48) offsets.push(offset);
    }
  }
  return offsets.sort((left, right) => {
    const leftDistance = left[0] ** 2 + left[1] ** 2;
    const rightDistance = right[0] ** 2 + right[1] ** 2;
    return leftDistance - rightDistance || left[1] - right[1] || Math.abs(left[0]) - Math.abs(right[0]) || left[0] - right[0];
  });
}

const markerOffsets = focusMarkerOffsets();

function segmentIntersectsBox(start, end, box, gap = 0) {
  const bounds = {
    left: box.left - gap,
    right: box.right + gap,
    top: box.top - gap,
    bottom: box.bottom + gap
  };
  let near = 0;
  let far = 1;
  const dx = end.x - start.x;
  const dy = end.y - start.y;
  for (const [origin, delta, minimum, maximum] of [
    [start.x, dx, bounds.left, bounds.right],
    [start.y, dy, bounds.top, bounds.bottom]
  ]) {
    if (Math.abs(delta) < 1e-9) {
      if (origin < minimum || origin > maximum) return false;
      continue;
    }
    const first = (minimum - origin) / delta;
    const second = (maximum - origin) / delta;
    const entry = Math.min(first, second);
    const exit = Math.max(first, second);
    near = Math.max(near, entry);
    far = Math.min(far, exit);
    if (near > far) return false;
  }
  return far >= 0 && near <= 1;
}

function segmentsIntersect(leftStart, leftEnd, rightStart, rightEnd) {
  const epsilon = 1e-9;
  const orientation = (start, end, point) =>
    (end.x - start.x) * (point.y - start.y) -
    (end.y - start.y) * (point.x - start.x);
  const onSegment = (start, end, point) =>
    point.x >= Math.min(start.x, end.x) - epsilon &&
    point.x <= Math.max(start.x, end.x) + epsilon &&
    point.y >= Math.min(start.y, end.y) - epsilon &&
    point.y <= Math.max(start.y, end.y) + epsilon;
  const leftRightStart = orientation(leftStart, leftEnd, rightStart);
  const leftRightEnd = orientation(leftStart, leftEnd, rightEnd);
  const rightLeftStart = orientation(rightStart, rightEnd, leftStart);
  const rightLeftEnd = orientation(rightStart, rightEnd, leftEnd);
  const straddles = (first, second) =>
    (first > epsilon && second < -epsilon) ||
    (first < -epsilon && second > epsilon);
  if (
    straddles(leftRightStart, leftRightEnd) &&
    straddles(rightLeftStart, rightLeftEnd)
  ) return true;
  return (
    (Math.abs(leftRightStart) <= epsilon && onSegment(leftStart, leftEnd, rightStart)) ||
    (Math.abs(leftRightEnd) <= epsilon && onSegment(leftStart, leftEnd, rightEnd)) ||
    (Math.abs(rightLeftStart) <= epsilon && onSegment(rightStart, rightEnd, leftStart)) ||
    (Math.abs(rightLeftEnd) <= epsilon && onSegment(rightStart, rightEnd, leftEnd))
  );
}

const standardTeachingOverlayWidths = __TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES__;

function bestMapPane(stageRect, overlayRect, viewWidth, viewHeight, horizontalPadding, verticalPadding) {
  const gap = 12;
  const overlayOnLeft = (overlayRect.left + overlayRect.right) / 2 <= (stageRect.left + stageRect.right) / 2;
  const sideCandidate = overlayOnLeft
    ? {
        dock: "left",
        left: overlayRect.right + gap,
        top: stageRect.top,
        width: stageRect.right - overlayRect.right - gap,
        height: stageRect.height
      }
    : {
        dock: "right",
        left: stageRect.left,
        top: stageRect.top,
        width: overlayRect.left - stageRect.left - gap,
        height: stageRect.height
      };
  const candidates = [sideCandidate, {
    dock: "bottom",
    left: stageRect.left,
    top: stageRect.top,
    width: stageRect.width,
    height: overlayRect.top - stageRect.top - gap
  }];
  let chosen = null;
  for (const candidate of candidates) {
    const innerWidth = candidate.width - horizontalPadding;
    const innerHeight = candidate.height - verticalPadding;
    if (innerWidth <= 0 || innerHeight <= 0) continue;
    const scale = Math.min(innerWidth / viewWidth, innerHeight / viewHeight);
    const renderedArea = viewWidth * scale * viewHeight * scale;
    const fitted = { ...candidate, renderedArea };
    if (!chosen || fitted.renderedArea > chosen.renderedArea) chosen = fitted;
  }
  return chosen;
}

function bestThreePane(stageRect, overlayRect) {
  const gap = 12;
  const overlayOnLeft = (overlayRect.left + overlayRect.right) / 2 <= (stageRect.left + stageRect.right) / 2;
  let pane;
  if (overlayRect.width >= stageRect.width * .72) {
    pane = {
      dock: "bottom",
      left: stageRect.left,
      top: stageRect.top,
      width: stageRect.width,
      height: overlayRect.top - stageRect.top - gap
    };
  } else if (overlayOnLeft) {
    pane = {
      dock: "left",
      left: overlayRect.right + gap,
      top: stageRect.top,
      width: stageRect.right - overlayRect.right - gap,
      height: stageRect.height
    };
  } else {
    pane = {
      dock: "right",
      left: stageRect.left,
      top: stageRect.top,
      width: overlayRect.left - stageRect.left - gap,
      height: stageRect.height
    };
  }
  if (pane.width <= 0 || pane.height <= 0) return null;
  return { ...pane, physicalArea: pane.width * pane.height };
}

function widestMaximumPhysicalAreaCandidate(candidates) {
  let chosen = null;
  for (const candidate of candidates) {
    const areaDelta = chosen ? candidate.physicalArea - chosen.physicalArea : Infinity;
    const widerTie = chosen && Math.abs(areaDelta) <= 1e-6 &&
      (candidate.overlayWidth ?? -1) > (chosen.overlayWidth ?? -1);
    if (!chosen || areaDelta > 1e-6 || widerTie) chosen = candidate;
  }
  return chosen;
}

function applyTeachingPane(stageRect, pane, overlayWidth) {
  const top = pane.top - stageRect.top;
  const right = stageRect.right - pane.left - pane.width;
  const bottom = stageRect.bottom - pane.top - pane.height;
  const left = pane.left - stageRect.left;
  for (const surface of [mount, mapStage]) {
    surface.style.inset = `${top}px ${right}px ${bottom}px ${left}px`;
    surface.dataset.teachingDock = pane.dock;
    surface.dataset.teachingWidth = overlayWidth ?? "responsive";
  }
}

function applyTeachingDock(shot) {
  const overlay = $("teaching-overlay");
  overlay.style.width = "";
  for (const surface of [mount, mapStage]) {
    surface.style.inset = "0px";
    delete surface.dataset.teachingDock;
    delete surface.dataset.teachingWidth;
  }
  if (overlay.dataset.mobileOpen === "true") return;
  if (!shot.visual?.annotation || overlay.hidden) return;
  const stageRect = stage.getBoundingClientRect();
  const standardProfile = matchMedia("(min-width: 821px) and (min-height: 561px)").matches;
  const widths = standardProfile ? standardTeachingOverlayWidths : [null];
  if (shot.render_mode === "2d") {
    const [, , viewWidth, viewHeight] = shot.frame.viewBox;
    const style = getComputedStyle(mapStage);
    const horizontalPadding = Number.parseFloat(style.paddingLeft) + Number.parseFloat(style.paddingRight);
    const verticalPadding = Number.parseFloat(style.paddingTop) + Number.parseFloat(style.paddingBottom);
    const candidates = [];
    for (const width of widths) {
      overlay.style.width = width === null ? "" : `${width}px`;
      const pane = bestMapPane(
        stageRect,
        overlay.getBoundingClientRect(),
        viewWidth,
        viewHeight,
        horizontalPadding,
        verticalPadding
      );
      if (!pane) continue;
      candidates.push({ ...pane, overlayWidth: width, physicalArea: pane.renderedArea });
    }
    const chosen = widestMaximumPhysicalAreaCandidate(candidates);
    if (!chosen) throw new Error(`No fitted visual pane for ${shot.segment_id}`);
    overlay.style.width = chosen.overlayWidth === null ? "" : `${chosen.overlayWidth}px`;
    applyTeachingPane(stageRect, chosen, chosen.overlayWidth);
    return;
  }
  const candidates = [];
  for (const width of widths) {
    overlay.style.width = width === null ? "" : `${width}px`;
    const pane = bestThreePane(stageRect, overlay.getBoundingClientRect());
    if (!pane) continue;
    candidates.push({ ...pane, overlayWidth: width });
  }
  const chosen = widestMaximumPhysicalAreaCandidate(candidates);
  if (!chosen) throw new Error(`No fitted visual pane for ${shot.segment_id}`);
  overlay.style.width = chosen.overlayWidth === null ? "" : `${chosen.overlayWidth}px`;
  applyTeachingPane(stageRect, chosen, chosen.overlayWidth);
}

function resizeVisualSurface(shot) {
  const rect = mount.getBoundingClientRect();
  if (rect.width <= 0 || rect.height <= 0) return;
  camera.aspect = rect.width / rect.height;
  camera.updateProjectionMatrix();
  renderer.setSize(rect.width, rect.height);
  labelRenderer.setSize(rect.width, rect.height);
  if (shot.render_mode === "3d") setFrame(shot);
}

function mapFocusAnchor(id) {
  const label = mapLabelById.get(id);
  const text = label?.querySelector("text");
  const transform = mapSvg.getScreenCTM();
  if (!label || !text || !transform || label.dataset.focusVisible !== "true" || label.style.display !== "none") return null;
  const point = mapSvg.createSVGPoint();
  point.x = Number(text.getAttribute("x"));
  point.y = Number(text.getAttribute("y"));
  const projected = point.matrixTransform(transform);
  return Number.isFinite(projected.x) && Number.isFinite(projected.y)
    ? { x: projected.x, y: projected.y }
    : null;
}

function threeFocusAnchor(id, stageRect) {
  const object = nodeObjects.get(id);
  const label = object?.userData.label;
  if (!label?.visible || label.element.style.visibility !== "hidden") return null;
  const projected = label.position.clone().project(camera);
  if (!Number.isFinite(projected.x) || !Number.isFinite(projected.y) || projected.z < -1 || projected.z > 1) return null;
  return {
    x: stageRect.left + (projected.x * .5 + .5) * stageRect.width,
    y: stageRect.top + (-projected.y * .5 + .5) * stageRect.height
  };
}

function renderFocusMarkers(shot) {
  const layer = $("focus-markers");
  layer.replaceChildren();
  if (shot.visual?.label_policy !== "focus") return;
  const stageRect = stage.getBoundingClientRect();
  const visualRect = (shot.render_mode === "2d" ? mapStage : mount).getBoundingClientRect();
  const overlay = $("teaching-overlay");
  const overlayRect = overlay && !overlay.hidden ? overlay.getBoundingClientRect() : null;
  const visibleLabelRects = shot.render_mode === "2d"
    ? mapLabels
        .filter(element => element.style.display !== "none" && !mapLegend?.contains(element))
        .map(element => element.getBoundingClientRect())
    : [...nodeObjects.values()]
        .map(object => object.userData.label)
        .filter(label => label.visible && label.element.style.visibility !== "hidden")
        .map(label => label.element.getBoundingClientRect());
  const placed = [];
  const placedLeaders = [];
  const chips = [...$("focus-key").querySelectorAll('.focus-chip[data-marker-number]')];
  const entries = chips.map(chip => {
    const id = chip.dataset.labelId;
    return {
      id,
      markerNumber: chip.dataset.markerNumber,
      anchor: shot.render_mode === "2d"
        ? mapFocusAnchor(id)
        : threeFocusAnchor(id, visualRect)
    };
  });
  for (const [entryIndex, entry] of entries.entries()) {
    const { id, markerNumber, anchor } = entry;
    if (!anchor) continue;
    const futureAnchors = entries
      .slice(entryIndex + 1)
      .filter(item => item.anchor)
      .map(item => ({
        left: item.anchor.x,
        right: item.anchor.x,
        top: item.anchor.y,
        bottom: item.anchor.y
      }));
    const markerSize = 20;
    const candidate = markerOffsets
      .map(([dx, dy]) => ({
        x: anchor.x + dx,
        y: anchor.y + dy,
        box: {
          left: anchor.x + dx - markerSize / 2,
          right: anchor.x + dx + markerSize / 2,
          top: anchor.y + dy - markerSize / 2,
          bottom: anchor.y + dy + markerSize / 2
        }
      }))
      .find(item =>
        item.box.left >= visualRect.left + 5 &&
        item.box.right <= visualRect.right - 5 &&
        item.box.top >= visualRect.top + 5 &&
        item.box.bottom <= visualRect.bottom - 5 &&
        (!overlayRect || !markerBoxesOverlap(item.box, overlayRect, 4)) &&
        (!overlayRect || !segmentIntersectsBox(anchor, item, overlayRect, 1)) &&
        visibleLabelRects.every(box =>
          !markerBoxesOverlap(item.box, box, 3) &&
          !segmentIntersectsBox(anchor, item, box, 1)
        ) &&
        futureAnchors.every(box =>
          !markerBoxesOverlap(item.box, box, 2) &&
          !segmentIntersectsBox(anchor, item, box, 2)
        ) &&
        placed.every(box =>
          !markerBoxesOverlap(item.box, box, 2) &&
          !segmentIntersectsBox(anchor, item, box, 1)
        ) &&
        placedLeaders.every(leader =>
          !segmentIntersectsBox(leader.start, leader.end, item.box, 1) &&
          (
            Math.hypot(item.x - anchor.x, item.y - anchor.y) <= 1 ||
            !segmentsIntersect(anchor, item, leader.start, leader.end)
          )
        )
      );
    if (!candidate) continue;
    placed.push(candidate.box);
    const distance = Math.hypot(candidate.x - anchor.x, candidate.y - anchor.y);
    if (distance > 1) {
      const leader = document.createElement("span");
      leader.className = "focus-leader";
      leader.style.left = `${anchor.x - stageRect.left}px`;
      leader.style.top = `${anchor.y - stageRect.top}px`;
      leader.style.width = `${distance}px`;
      leader.style.transform = `rotate(${Math.atan2(candidate.y - anchor.y, candidate.x - anchor.x)}rad)`;
      layer.appendChild(leader);
      placedLeaders.push({ start: anchor, end: candidate });
    }
    const marker = document.createElement("span");
    marker.className = "focus-marker";
    marker.dataset.labelId = id;
    marker.style.left = `${candidate.x - stageRect.left}px`;
    marker.style.top = `${candidate.y - stageRect.top}px`;
    marker.textContent = markerNumber;
    layer.appendChild(marker);
  }
}

function portraitTeachingMode() {
  return matchMedia("(max-width: 520px)").matches;
}

function syncTeachingVisibility(shot, { focusDrawer = false, restoreFocus = false } = {}) {
  const overlay = $("teaching-overlay");
  const toggle = $("teaching-toggle");
  const hasAnnotation = Boolean(shot.visual?.annotation);
  const portrait = portraitTeachingMode();
  const annotationOpen = hasAnnotation && teachingOpen;
  const portraitDrawerOpen = annotationOpen && portrait;
  toggle.hidden = !hasAnnotation;
  toggle.setAttribute("aria-expanded", String(annotationOpen));
  toggle.textContent = annotationOpen ? "Hide teaching" : "Teaching";
  overlay.hidden = !annotationOpen;
  overlay.inert = overlay.hidden;
  overlay.dataset.mobileOpen = String(portraitDrawerOpen);
  stage.dataset.teachingOpen = String(portraitDrawerOpen);
  if (portraitDrawerOpen) {
    stage.inert = true;
    stage.setAttribute("aria-hidden", "true");
    if (focusDrawer) $("teaching-close").focus();
  } else if (!notesOpen) {
    stage.inert = false;
    stage.removeAttribute("aria-hidden");
  }
  if (restoreFocus && !toggle.hidden) toggle.focus();
}

function setTeachingOpen(open, { restoreFocus = false } = {}) {
  const shot = shots[current];
  teachingOpen = Boolean(open && shot.visual?.annotation);
  syncTeachingVisibility(shot, {
    focusDrawer: teachingOpen && portraitTeachingMode(),
    restoreFocus
  });
  applyTeachingDock(shot);
  resizeVisualSurface(shot);
  resolveTeachingCollisions(shot);
}

function renderTeaching(shot) {
  const overlay = $("teaching-overlay");
  const annotation = shot.visual?.annotation;
  teachingOpen = false;
  if (!annotation) {
    syncTeachingVisibility(shot);
    applyTeachingDock(shot);
    resizeVisualSurface(shot);
    resolveTeachingCollisions(shot);
    return;
  }
  overlay.dataset.position = annotation.position;
  overlay.dataset.kind = annotation.kind;
  overlay.dataset.segmentId = shot.segment_id;
  $("teaching-title").textContent = annotation.title;
  const items = $("teaching-items");
  items.replaceChildren();
  for (const item of annotation.items) {
    const entry = document.createElement("li");
    entry.textContent = item.label;
    entry.dataset.claimIds = item.claim_ids.join(" ");
    items.appendChild(entry);
  }
  syncTeachingVisibility(shot);
  applyTeachingDock(shot);
  resizeVisualSurface(shot);
  resolveTeachingCollisions(shot);
}

function notesDisclosure(title, className = "") {
  const disclosure = document.createElement("details");
  disclosure.className = `notes-section disclosure ${className}`.trim();
  const summary = document.createElement("summary");
  summary.textContent = title;
  disclosure.appendChild(summary);
  return disclosure;
}

function appendClaimCard(section, claim) {
  const card = document.createElement("article");
  card.className = "claim-card";
  const heading = document.createElement("h4");
  heading.textContent = `${claim.id.replaceAll("_", " ")} · ${claim.assertion.replaceAll("_", " ")}`;
  card.appendChild(heading);
  card.appendChild(paragraph(
    claim.binding === "overlay"
      ? "Binding: segment-local, nonphysical teaching overlay"
      : "Binding: selected topology ownership"
  ));
  for (const fact of claim.facts) {
    card.appendChild(paragraph(fact.value, "fact-value"));
    const details = document.createElement("details");
    details.className = "fact-details";
    const summary = document.createElement("summary");
    summary.textContent = "Fact, ownership, boundary, and sources";
    details.append(
      summary,
      paragraph(`Fact: ${fact.ref}`),
      paragraph(`Basis: ${fact.basis}`),
      paragraph(`Scope: ${fact.scope}`),
      paragraph(`Boundary: ${fact.posture.replaceAll("_", " ")} · ${fact.lifecycle.replaceAll("_", " ")} · as of ${fact.as_of}`)
    );
    if (fact.topology_targets.length) {
      details.appendChild(paragraph(`Topology target: ${fact.topology_targets.map(target => `${target.kind} ${target.id} (${target.label}; ${target.presence.replaceAll("_", " ")} · ${target.lifecycle.replaceAll("_", " ")})`).join(" · ")}`));
    }
    const sources = document.createElement("p");
    sources.className = "source-list";
    sources.append("Source: ");
    fact.sources.forEach((source, index) => {
      if (index) sources.append(" · ");
      const link = document.createElement("a");
      link.href = source.url;
      link.target = "_blank";
      link.rel = "noreferrer";
      link.textContent = `${source.publisher} — ${source.title}`;
      sources.appendChild(link);
      sources.append(` (accessed ${source.accessed_as_of}; ${source.date_note})`);
    });
    details.appendChild(sources);
    card.appendChild(details);
  }
  section.appendChild(card);
}

function renderNotes(shot) {
  const restorePanelFocus = notesOpen && $("notes-panel").contains(document.activeElement);
  $("notes-panel").scrollTop = 0;
  $("notes-kicker").textContent = `Act ${shot.act_sequence} · ${shot.act_title}`;
  $("notes-title").textContent = shot.title;
  const body = $("notes-body");
  body.replaceChildren();

  const limitAssertions = new Set(["explicit_unknown", "no_evidence_backed_estimate"]);
  const supportedClaims = shot.claims.filter(claim => !limitAssertions.has(claim.assertion));
  const knownLimits = shot.claims.filter(claim => limitAssertions.has(claim.assertion));
  const knownLimitCount = knownLimits.reduce((count, claim) => count + claim.facts.length, 0);
  const ready = shot.evidence_readiness === "evidence_ready";
  const summary = paragraph(
    `${ready ? "Evidence ready" : "Evidence review needed"} · ${countLabel(supportedClaims.length, "supported claim group")} · ${countLabel(knownLimitCount, "known limit")}`,
    `evidence-summary ${ready ? "ready" : "gated"}`
  );
  body.appendChild(summary);

  if (shot.blocking_research.length) {
    const blockers = notesSection(`Open research (${shot.blocking_research.length})`);
    blockers.classList.add("gated");
    const list = document.createElement("ul");
    for (const blocker of shot.blocking_research) {
      const item = document.createElement("li");
      item.textContent = blocker;
      list.appendChild(item);
    }
    blockers.appendChild(list);
    body.appendChild(blockers);
  }

  const evidence = notesSection("What the evidence supports");
  for (const claim of supportedClaims) appendClaimCard(evidence, claim);
  body.appendChild(evidence);

  if (knownLimits.length) {
    const limits = notesDisclosure(`Known limits (${knownLimitCount})`, "known-limits");
    for (const claim of knownLimits) appendClaimCard(limits, claim);
    body.appendChild(limits);
  }

  const guards = notesDisclosure(`Avoid overclaiming (${shot.promotion_guard_warnings.length})`, "guard-list");
  const guardList = document.createElement("ul");
  for (const guard of shot.promotion_guard_warnings) {
    const item = document.createElement("li");
    const label = document.createElement("strong");
    label.textContent = guard.id.replaceAll("_", " ");
    item.append(label, document.createTextNode(guard.warning));
    guardList.appendChild(item);
  }
  guards.appendChild(guardList);
  body.appendChild(guards);

  if (restorePanelFocus) $("notes-close").focus();
}

function setNotesOpen(open) {
  const panel = $("notes-panel");
  const toggle = $("evidence-toggle");
  const wasOpen = notesOpen;
  if (open && teachingOpen) setTeachingOpen(false);
  notesOpen = open;
  for (const id of ["shot-rail", "masthead", "stage", "transport", "teaching-overlay"]) {
    const element = $(id);
    element.inert = open;
    if (open) element.setAttribute("aria-hidden", "true");
    else element.removeAttribute("aria-hidden");
  }
  panel.inert = !open;
  panel.dataset.open = String(open);
  panel.setAttribute("aria-hidden", String(!open));
  toggle.setAttribute("aria-expanded", String(open));
  toggle.textContent = open ? "Hide evidence" : "Show evidence";
  if (open) {
    $("notes-close").focus();
  } else {
    syncTeachingVisibility(shots[current]);
    if (wasOpen) toggle.focus();
  }
}

function trapNotesFocus(event) {
  const panel = $("notes-panel");
  const focusable = [...panel.querySelectorAll('button, a[href], summary, [tabindex]:not([tabindex="-1"])')]
    .filter(element => !element.hidden && element.getAttribute("aria-hidden") !== "true");
  if (!focusable.length) return;
  const first = focusable[0];
  const last = focusable[focusable.length - 1];
  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  } else if (!panel.contains(document.activeElement)) {
    event.preventDefault();
    first.focus();
  }
}
"""


def _player_template() -> str:
    html = shots.runtime_html_template()
    course_css = (
        COURSE_CSS.replace(
            "__TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX__",
            str(TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX),
        )
        .replace(
            "__TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX__",
            str(TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX),
        )
        .replace(
            "__SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX__",
            str(SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX),
        )
        .replace(
            "__SHORT_TEACHING_OVERLAY_PADDING_BLOCK_PX__",
            str(SHORT_TEACHING_OVERLAY_PADDING_BLOCK_PX),
        )
    )
    course_css = (
        course_css.replace(
            "__FOCUS_KEY_INDEX_FONT_PX__",
            str(FOCUS_KEY_INDEX_FONT_FLOOR_PX),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_COLUMNS__",
            str(DESKTOP_FOCUS_KEY_COLUMNS),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_GAP_PX__",
            str(DESKTOP_FOCUS_KEY_GAP_PX),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX__",
            str(_DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_INDEX_GAP_PX__",
            str(_DESKTOP_FOCUS_KEY_INDEX_GAP_PX),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX__",
            str(_DESKTOP_FOCUS_KEY_CHIP_VERTICAL_PADDING_PX),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX__",
            str(_DESKTOP_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_FONT_PX__",
            str(DESKTOP_FOCUS_KEY_FONT_PX),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_LINE_HEIGHT__",
            str(DESKTOP_FOCUS_KEY_LINE_HEIGHT),
        )
        .replace(
            "__DESKTOP_FOCUS_KEY_SWATCH_WIDTH_PX__",
            str(_DESKTOP_FOCUS_KEY_SWATCH_WIDTH_PX),
        )
        .replace(
            "__PORTRAIT_MASTHEAD_HEIGHT_PX__",
            str(PORTRAIT_MASTHEAD_HEIGHT_PX),
        )
        .replace(
            "__PORTRAIT_FOCUS_KEY_COLUMNS__",
            str(PORTRAIT_FOCUS_KEY_COLUMNS),
        )
        .replace(
            "__PORTRAIT_FOCUS_KEY_GAP_PX__",
            str(PORTRAIT_FOCUS_KEY_GAP_PX),
        )
        .replace(
            "__PORTRAIT_FOCUS_KEY_SWATCH_WIDTH_PX__",
            str(_PORTRAIT_FOCUS_KEY_SWATCH_WIDTH_PX),
        )
        .replace(
            "__TABLET_FOCUS_KEY_CONTENT_WIDTH_PX__",
            str(int(TABLET_FOCUS_KEY_CONTENT_WIDTH_PX)),
        )
        .replace(
            "__TABLET_FOCUS_KEY_COLUMNS__",
            str(TABLET_FOCUS_KEY_COLUMNS),
        )
        .replace(
            "__TABLET_FOCUS_KEY_GAP_PX__",
            str(TABLET_FOCUS_KEY_GAP_PX),
        )
        .replace(
            "__TABLET_FOCUS_KEY_INDEX_WIDTH_PX__",
            str(_TABLET_FOCUS_KEY_INDEX_WIDTH_PX),
        )
        .replace(
            "__TABLET_FOCUS_KEY_INDEX_GAP_PX__",
            str(_TABLET_FOCUS_KEY_INDEX_GAP_PX),
        )
        .replace(
            "__TABLET_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX__",
            str(_TABLET_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX),
        )
        .replace(
            "__TABLET_FOCUS_KEY_FONT_PX__",
            str(TABLET_FOCUS_KEY_FONT_PX),
        )
        .replace(
            "__TABLET_FOCUS_KEY_LINE_HEIGHT__",
            str(TABLET_FOCUS_KEY_LINE_HEIGHT),
        )
        .replace(
            "__TABLET_FOCUS_KEY_SWATCH_WIDTH_PX__",
            str(_TABLET_FOCUS_KEY_SWATCH_WIDTH_PX),
        )
        .replace(
            "__SHORT_MASTHEAD_HEIGHT_PX__",
            str(SHORT_MASTHEAD_HEIGHT_PX),
        )
        .replace(
            "__SHORT_OPENING_QUESTION_FONT_PX__",
            str(SHORT_OPENING_QUESTION_FONT_PX),
        )
        .replace(
            "__SHORT_FOCUS_KEY_CONTENT_WIDTH_PX__",
            str(int(SHORT_FOCUS_KEY_CONTENT_WIDTH_PX)),
        )
        .replace(
            "__SHORT_FOCUS_KEY_COLUMNS__",
            str(SHORT_FOCUS_KEY_COLUMNS),
        )
        .replace(
            "__SHORT_FOCUS_KEY_GAP_PX__",
            str(SHORT_FOCUS_KEY_GAP_PX),
        )
        .replace(
            "__SHORT_FOCUS_KEY_INDEX_WIDTH_PX__",
            str(_SHORT_FOCUS_KEY_INDEX_WIDTH_PX),
        )
        .replace(
            "__SHORT_FOCUS_KEY_INDEX_GAP_PX__",
            str(_SHORT_FOCUS_KEY_INDEX_GAP_PX),
        )
        .replace(
            "__SHORT_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX__",
            str(_SHORT_FOCUS_KEY_CHIP_HORIZONTAL_PADDING_PX),
        )
        .replace(
            "__SHORT_FOCUS_KEY_FONT_PX__",
            str(SHORT_FOCUS_KEY_FONT_PX),
        )
        .replace(
            "__SHORT_FOCUS_KEY_LINE_HEIGHT__",
            str(SHORT_FOCUS_KEY_LINE_HEIGHT),
        )
        .replace(
            "__SHORT_FOCUS_KEY_SWATCH_WIDTH_PX__",
            str(_SHORT_FOCUS_KEY_SWATCH_WIDTH_PX),
        )
    )
    notes_js = (
        NOTES_JS.replace(
            "__TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES__",
            scene_pipeline.canonical_payload(
                list(TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX)
            ),
        )
        .replace(
            "__COMPACT_FOCUS_LABELS__",
            scene_pipeline.canonical_payload(_COMPACT_FOCUS_LABELS),
        )
        .replace(
            "__LEGEND_GRAMMAR_CUES__",
            scene_pipeline.canonical_payload(_LEGEND_GRAMMAR_CUES),
        )
    )
    replacements = (
        ("GIGAWATT — planned shot review", "GIGAWATT — complete course"),
        ("Planned shot registry", "Complete course sequence"),
        ("<p>Course production</p>", "<p>Untimed course runtime</p>"),
        ("<h1>21 planned shots</h1>", "<h1>26 course segments</h1>"),
        ('aria-label="Planned shots"', 'aria-label="Course segments"'),
        (
            'aria-label="Manual planned-shot review surface"',
            'aria-label="Presenter-controlled course surface"',
        ),
        (
            'aria-label="Manual review controls"',
            'aria-label="Course navigation and evidence controls"',
        ),
        ('aria-label="Previous planned shot"', 'aria-label="Previous course segment"'),
        ('aria-label="Next planned shot"', 'aria-label="Next course segment"'),
        (
            "Manual review · select every change",
            "Untimed · presenter advances between course sections",
        ),
        ("Loading the planned-shot registry…", "Loading the complete course…"),
        ("const shots = data.registry.shots;", "const shots = data.registry.segments;"),
    )
    for old, new in replacements:
        html = _must_replace(html, old, new)
    html = _must_replace(
        html,
        "</style>",
        f"{course_css}\n</style>",
    )
    html = _must_replace(
        html,
        '<p id="scope-summary"></p>\n    <p id="scope-ids"></p>',
        '<p id="opening-question"></p>\n    <p id="objective"></p>\n    <p id="boundary-note"><span id="boundary-full"></span><span id="boundary-compact" aria-hidden="true">Source-gated Abilene facts · dashed equipment is a teaching reference, not as-built.</span></p>\n    <p id="scope-summary"></p>\n    <p id="scope-ids"></p>',
    )
    html = _must_replace(
        html,
        '<div id="focus-key" tabindex="0" aria-label="Readable labels for focused topology" hidden></div>',
        '<ol id="focus-key" role="list" tabindex="0" aria-label="Focus key: visual grammar and numbered topology labels" hidden></ol>',
    )
    html = _must_replace(
        html,
        '    <svg id="map-svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Focused engineering map">__MAP_SCENE__</svg>\n  </section>\n</main>',
        '    <svg id="map-svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Focused engineering map">__MAP_SCENE__</svg>\n  </section>\n  <div id="focus-markers" aria-hidden="true"></div>\n</main>',
    )
    html = _must_replace(
        html,
        '<button id="context-toggle" type="button">Show anchor</button>',
        '<button id="teaching-toggle" type="button" aria-controls="teaching-overlay" aria-expanded="false" hidden>Teaching</button>\n  <button id="evidence-toggle" type="button" aria-controls="notes-panel" aria-expanded="false">Show evidence</button>',
    )
    html = _must_replace(
        html,
        '<div id="loading">Loading the complete course…</div>',
        f'{NOTES_HTML}\n<div id="loading">Loading the complete course…</div>',
    )
    html = _must_replace(
        html,
        "let current = 0;\nlet showingAnchor = false;",
        f"{notes_js}\n\nlet current = 0;\nlet notesOpen = false;\nlet teachingOpen = false;",
    )
    html = _must_replace(
        html,
        """    const label = shot.render_mode === "2d"
      ? mapLabelById.get(id)?.textContent.trim()
      : `${nodeLabels.get(id)} · ${nodePostures.get(id)}`;""",
        """    const label = shot.render_mode === "2d"
      ? (focusKeyCopyById[id] || mapLabelById.get(id)?.textContent.trim())
      : `${nodeLabels.get(id)} · ${nodePostures.get(id)}`;""",
    )
    html = _must_replace(
        html,
        """    const chip = document.createElement("span");
    chip.className = "focus-chip";
    chip.dataset.labelId = id;
    chip.textContent = label;
    key.appendChild(chip);""",
        """    const chip = document.createElement("li");
    chip.className = "focus-chip";
    chip.dataset.labelId = id;
    const grammarCue = legendGrammarCues[id];
    const grammarId = id.startsWith("legend_");
    if (grammarId && !grammarCue) throw new Error(`Unknown fixed grammar key ID: ${id}`);
    chip.dataset.keyRole = grammarCue ? "grammar" : "geometry";
    const copy = document.createElement("span");
    copy.className = "focus-copy";
    copy.textContent = compactFocusLabel(id);
    copy.setAttribute("aria-hidden", "true");
    chip.title = label;
    if (grammarCue) {
      const swatch = document.createElement("span");
      swatch.className = "focus-swatch";
      swatch.dataset.cue = grammarCue;
      swatch.setAttribute("aria-hidden", "true");
      chip.setAttribute("aria-label", label);
      chip.append(swatch, copy);
    } else {
      const markerNumber = key.querySelectorAll('[data-key-role="geometry"]').length + 1;
      chip.dataset.markerNumber = String(markerNumber);
      const index = document.createElement("span");
      index.className = "focus-index";
      index.textContent = String(markerNumber);
      index.setAttribute("aria-hidden", "true");
      chip.setAttribute("aria-label", `${markerNumber}. ${label}`);
      chip.append(index, copy);
    }
    key.appendChild(chip);""",
    )
    html = _must_replace(
        html,
        "  if (!overlay || overlay.hidden) return;",
        "  if (!overlay || overlay.hidden) {\n    renderFocusMarkers(shot);\n    return;\n  }",
    )
    html = _must_replace(
        html,
        '    element.style.opacity = focusNodes.has(id) ? "1" : ".08";',
        '    element.dataset.focusState = focusNodes.has(id) ? "focused" : "context";\n'
        '    element.style.opacity = focusNodes.has(id) ? "1" : ".08";',
    )
    html = _must_replace(
        html,
        '    element.style.opacity = focusEdges.has(id) ? "1" : ".06";',
        '    element.dataset.focusState = focusEdges.has(id) ? "focused" : "context";\n'
        '    element.style.opacity = focusEdges.has(id) ? "1" : ".06";',
    )
    html = _must_replace(
        html,
        """    if (shot.render_mode === "2d") element.style.display = "none";
    else element.style.visibility = "hidden";
  }
}""",
        """    if (shot.render_mode === "2d") element.style.display = "none";
    else element.style.visibility = "hidden";
  }
  renderFocusMarkers(shot);
}""",
    )
    html = _must_replace(
        html,
        r"""function setFrame(shot) {
  if (shot.frame.kind === "2d") {
    const view = showingAnchor ? shot.frame.anchor_viewBox : shot.frame.viewBox;
    mapSvg.setAttribute("viewBox", view.join(" "));
    return;
  }
  const position = showingAnchor ? shot.frame.anchor_position : responsive3dPosition(shot.frame);
  const target = showingAnchor ? shot.frame.anchor_target : shot.frame.target;
  camera.position.set(...position);
  camera.up.set(...shot.frame.up).normalize();
  controls.target.set(...target);
  controls.update();
  render3d();
}""",
        r"""function setFrame(shot) {
  if (shot.frame.kind === "2d") {
    mapSvg.setAttribute("viewBox", shot.frame.viewBox.join(" "));
    return;
  }
  camera.position.set(...responsive3dPosition(shot.frame));
  camera.up.set(...shot.frame.up).normalize();
  controls.target.set(...shot.frame.target);
  controls.update();
  render3d();
}""",
    )
    html = _must_replace(
        html,
        "  showingAnchor = false;\n  const shot = shots[current];",
        "  const shot = shots[current];",
    )
    old_header = r"""  $("eyebrow").textContent = `${String(shot.sequence).padStart(2, "0")} / ${shots.length} · ${shot.segment_id}`;
  $("title").textContent = shot.title;
  $("scope-summary").textContent = `${shot.focus_nodes.length} nodes · ${shot.focus_edges.length} edges · ${shot.evidence_readiness.replaceAll("_", " ")}`;
  const readableNodes = shot.focus_nodes.map(id => nodeLabels.get(id) || id);
  $("scope-ids").textContent = readableNodes.join(" · ");
  $("scope-ids").title = shot.focus_nodes.join(", ");
  $("shot-id").textContent = shot.id;
  $("mode").textContent = `${shot.mode} · ${shot.render_mode} context · ${shot.camera_anchor}`;
  const revealCount = shot.reveal_ids.length + shot.reveal_copy_ids.length;
  $("reveal-summary").textContent = revealCount
    ? `${shot.reveal_ids.length} hidden geometry + ${shot.reveal_copy_ids.length} hidden copy revealed`
    : "No hidden reveal";
  $("context-toggle").textContent = "Show anchor";"""
    new_header = r"""  $("eyebrow").textContent = `Act ${shot.act_sequence} · ${shot.act_title} · ${String(shot.sequence).padStart(2, "0")} / ${shots.length}`;
  $("title").textContent = shot.title;
  $("opening-question").textContent = shot.opening_question;
  $("objective").textContent = shot.learning_objective;
  $("boundary-full").textContent = shot.boundary_note;
  $("boundary-note").title = shot.boundary_note;
  $("scope-summary").textContent = `${shot.focus_nodes.length} nodes · ${shot.focus_edges.length} edges · ${shot.evidence_readiness.replaceAll("_", " ")}`;
  $("scope-ids").textContent = shot.focus_node_labels.join(" · ");
  $("scope-ids").title = shot.focus_nodes.join(", ");
  $("shot-id").textContent = shot.segment_id;
  $("mode").textContent = `${shot.mode} · ${shot.render_mode} · ${shot.camera_anchor}`;
  const revealCount = shot.reveal_ids.length + shot.reveal_copy_ids.length;
  $("reveal-summary").textContent = revealCount
    ? `${revealCount} explicit hidden reveals · ${shot.status}`
    : `${shot.status} view · no hidden reveal`;
  $("posture").classList.toggle("ready", shot.evidence_readiness === "evidence_ready");
  $("posture").classList.toggle("gated", shot.evidence_readiness !== "evidence_ready");
  renderTeaching(shot);
  renderNotes(shot);"""
    html = _must_replace(html, old_header, new_header)
    old_rail = r"""  name.className = "shot-name";
  name.textContent = shot.id;
  const segment = document.createElement("span");
  segment.className = "segment-name";
  segment.textContent = shot.segment_id;"""
    new_rail = r"""  name.className = "shot-name";
  name.textContent = shot.title;
  const segment = document.createElement("span");
  segment.className = "segment-name";
  segment.textContent = `Act ${shot.act_sequence} · ${shot.segment_id}`;"""
    html = _must_replace(html, old_rail, new_rail)
    html = _must_replace(
        html,
        """$("context-toggle").addEventListener("click", () => {
  showingAnchor = !showingAnchor;
  $("context-toggle").textContent = showingAnchor ? "Show shot" : "Show anchor";
  setFrame(shots[current]);
});""",
        '$("teaching-toggle").addEventListener("click", () => setTeachingOpen(!teachingOpen));\n$("teaching-close").addEventListener("click", () => setTeachingOpen(false, { restoreFocus: true }));\n$("evidence-toggle").addEventListener("click", () => setNotesOpen(!notesOpen));\n$("notes-close").addEventListener("click", () => setNotesOpen(false));',
    )
    html = _must_replace(
        html,
        """addEventListener("keydown", event => {
  if (event.target.closest?.("#focus-key, button, a")) return;
  if (event.key === "ArrowLeft") activate(current - 1);
  if (event.key === "ArrowRight") activate(current + 1);
});""",
        """addEventListener("keydown", event => {
  if (notesOpen) {
    if (event.key === "Escape") {
      event.preventDefault();
      setNotesOpen(false);
    } else if (event.key === "Tab") {
      trapNotesFocus(event);
    }
    return;
  }
  if (teachingOpen && event.key === "Escape") {
    event.preventDefault();
    setTeachingOpen(false, { restoreFocus: true });
    return;
  }
  if (event.target.closest?.("#focus-key, button, a")) return;
  if (event.key === "ArrowLeft") activate(current - 1);
  if (event.key === "ArrowRight") activate(current + 1);
  if (event.key.toLowerCase() === "e") setNotesOpen(true);
});""",
    )
    html = _must_replace(
        html,
        """addEventListener("resize", () => {
  camera.aspect = mount.clientWidth / mount.clientHeight;""",
        """addEventListener("resize", () => {
  syncTeachingVisibility(shots[current]);
  applyTeachingDock(shots[current]);
  camera.aspect = mount.clientWidth / mount.clientHeight;""",
    )
    return html


def portrait_teaching_drawer_contract() -> dict[str, Any]:
    """Verify the deterministic source contract for the portrait teaching drawer."""
    html = _player_template()
    required_tokens = {
        "native_toggle": '<button id="teaching-toggle" type="button" aria-controls="teaching-overlay" aria-expanded="false" hidden>',
        "labelled_region": '<aside id="teaching-overlay" role="region"',
        "closed_hidden_inert": 'aria-labelledby="teaching-title" hidden inert>',
        "full_stage_drawer": (
            '#teaching-overlay[data-mobile-drawer="true"]:not([hidden]) {'
            "\n      z-index: 20;"
        ),
        "drawer_stage_inset": "top: var(--head);\n      right: 0;\n      bottom: var(--transport);\n      left: var(--rail);",
        "drawer_scroll": "overflow-x: hidden;\n      overflow-y: auto;",
        "stage_hidden_while_open": '#stage[data-teaching-open="true"] #three-mount',
        "portrait_drawer_not_docked": (
            'if (overlay.dataset.mobileOpen === "true") return;'
        ),
        "expanded_state": (
            'toggle.setAttribute("aria-expanded", String(annotationOpen));'
        ),
        "closed_state": "overlay.hidden = !annotationOpen;",
        "closed_inert_state": "overlay.inert = overlay.hidden;",
        "drawer_focus": 'if (focusDrawer) $("teaching-close").focus();',
        "escape_close": 'if (teachingOpen && event.key === "Escape")',
        "restore_opener_focus": "setTeachingOpen(false, { restoreFocus: true })",
        "segment_reset": "teachingOpen = false;",
    }
    missing_tokens = [
        token_id for token_id, token in required_tokens.items() if token not in html
    ]
    drawer_width = PORTRAIT_REFERENCE_VIEWPORT_WIDTH_PX - PORTRAIT_RAIL_WIDTH_PX
    drawer_height = (
        PORTRAIT_REFERENCE_VIEWPORT_HEIGHT_PX
        - PORTRAIT_MASTHEAD_HEIGHT_PX
        - PORTRAIT_TRANSPORT_HEIGHT_PX
    )
    return {
        "passed": not missing_tokens,
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "closed_by_default": True,
        "annotation_content_order": "authored_exact",
        "minimum_item_font_px": 10.0,
        "drawer_box": {
            "x": PORTRAIT_RAIL_WIDTH_PX,
            "y": PORTRAIT_MASTHEAD_HEIGHT_PX,
            "width": drawer_width,
            "height": drawer_height,
        },
        "overflow_x": "hidden",
        "overflow_y": "auto",
        "required_token_ids": list(required_tokens),
        "missing_token_ids": missing_tokens,
    }


def teaching_overlay_stage_edge_clearance_contract() -> dict[str, Any]:
    """Verify short overlays use the same modeled clearance and compact spacing."""
    html = _player_template()
    clearance = TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
    overlay_padding_block = SHORT_TEACHING_OVERLAY_PADDING_BLOCK_PX
    padding_block = SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX
    required_tokens = {
        "short_profile": "@media (max-height: 560px) and (min-width: 821px)",
        "short_bottom_clearance": (f"bottom: calc(var(--transport) + {clearance}px);"),
        "short_left_clearance": f"left: calc(var(--rail) + {clearance}px);",
        "short_right_clearance": f"right: {clearance}px; left: auto;",
        "compact_overlay_padding": f"padding: {overlay_padding_block}px 8px;",
        "compact_item_padding": f"padding: {padding_block}px 5px;",
        "item_font_floor": "font-size: 10px;\n      line-height: 1.15;",
    }
    missing_tokens = [
        token_id for token_id, token in required_tokens.items() if token not in html
    ]
    return {
        "passed": not missing_tokens,
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "minimum_stage_edge_clearance_px": float(clearance),
        "short_overlay_padding_block_px": float(overlay_padding_block),
        "short_item_padding_block_px": float(padding_block),
        "minimum_item_font_px": 10.0,
        "required_token_ids": list(required_tokens),
        "missing_token_ids": missing_tokens,
    }


def teaching_annotation_disclosure_contract() -> dict[str, Any]:
    """Verify annotations are exact, accessible, and opt-in at every viewport."""
    html = _player_template()
    required_tokens = {
        "all_viewport_toggle": (
            "#teaching-toggle:not([hidden]) { display: inline-grid; "
            "place-items: center; }"
        ),
        "toggle_accessible_name": (
            '<button id="teaching-toggle" type="button" '
            'aria-controls="teaching-overlay" aria-expanded="false" hidden>'
        ),
        "labelled_region": '<aside id="teaching-overlay" role="region"',
        "closed_markup": 'aria-labelledby="teaching-title" hidden inert>',
        "default_state_reset": "teachingOpen = false;",
        "closed_until_requested": "overlay.hidden = !annotationOpen;",
        "closed_inert": "overlay.inert = overlay.hidden;",
        "all_viewport_open_state": (
            "teachingOpen = Boolean(open && shot.visual?.annotation);"
        ),
        "exact_title": ('$("teaching-title").textContent = annotation.title;'),
        "exact_item_copy": "entry.textContent = item.label;",
        "claim_binding": 'entry.dataset.claimIds = item.claim_ids.join(" ");',
        "closed_stage_geometry": (
            "if (!shot.visual?.annotation || overlay.hidden) return;"
        ),
        "escape_close": 'if (teachingOpen && event.key === "Escape")',
        "evidence_exclusion": ("if (open && teachingOpen) setTeachingOpen(false);"),
    }
    missing_tokens = [
        token_id for token_id, token in required_tokens.items() if token not in html
    ]
    return {
        "passed": not missing_tokens,
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "closed_by_default_all_viewports": True,
        "default_visual_geometry": "labels_only_full_stage",
        "annotation_content_order": "authored_exact",
        "required_token_ids": list(required_tokens),
        "missing_token_ids": missing_tokens,
    }


def transport_slot_contract() -> dict[str, Any]:
    """Verify every responsive transport keeps one explicit semantic row."""
    html = _player_template()
    required_tokens = {
        "all_viewport_areas": (
            'grid-template-areas: "previous note teaching evidence next";'
        ),
        "all_viewport_columns": (
            "grid-template-columns: auto minmax(0, 1fr) minmax(128px, auto) "
            "minmax(128px, auto) auto;"
        ),
        "note_area": "#manual-note { grid-area: note; }",
        "portrait_areas": ('grid-template-areas: "previous teaching evidence next";'),
        "previous_area": "#previous { grid-area: previous; }",
        "teaching_area": "#teaching-toggle { grid-area: teaching; }",
        "evidence_area": "#evidence-toggle { grid-area: evidence; }",
        "next_area": "#next { grid-area: next; }",
        "hidden_teaching": "toggle.hidden = !hasAnnotation;",
    }
    missing_tokens = [
        token_id for token_id, token in required_tokens.items() if token not in html
    ]
    for token_id in ("previous_area", "teaching_area", "evidence_area", "next_area"):
        if html.count(required_tokens[token_id]) < 2 and token_id not in missing_tokens:
            missing_tokens.append(token_id)
    profiles = {
        "standard": {
            "viewport_ids": ["1920x1080", "1440x900", "1024x768"],
            "row_count": 1,
            "height_px": PORTRAIT_TRANSPORT_HEIGHT_PX,
            "areas": ["previous", "note", "teaching", "evidence", "next"],
        },
        "short": {
            "viewport_ids": ["844x390"],
            "row_count": 1,
            "height_px": SHORT_TRANSPORT_HEIGHT_PX,
            "areas": ["previous", "note", "teaching", "evidence", "next"],
        },
        "portrait": {
            "viewport_ids": ["390x844"],
            "row_count": 1,
            "height_px": PORTRAIT_TRANSPORT_HEIGHT_PX,
            "areas": ["previous", "teaching", "evidence", "next"],
            "note": "visually_hidden",
        },
    }
    return {
        "passed": not missing_tokens,
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "viewport_ids": [
            "1920x1080",
            "1440x900",
            "1024x768",
            "844x390",
            "390x844",
        ],
        "profiles": profiles,
        "annotated_row_count": 1,
        "unannotated_row_count": 1,
        "hidden_teaching_slot": "reserved",
        "required_token_ids": list(required_tokens),
        "missing_token_ids": missing_tokens,
    }


def responsive_focus_key_contract() -> dict[str, Any]:
    """Verify responsive key typography, semantics, and profile-specific spans."""
    html = _player_template()
    required_tokens = {
        "truthful_mixed_key_name": (
            'aria-label="Focus key: visual grammar and numbered topology labels"'
        ),
        "base_index_font": (
            f"color: var(--paper);\n    font-size: {FOCUS_KEY_INDEX_FONT_FLOOR_PX}px;"
            "\n    font-variant-numeric: tabular-nums;"
        ),
        "nonportrait_direction_span": (
            "@media (min-width: 521px) {\n"
            '    .focus-chip[data-label-id="legend_direction"] '
            "{ grid-column: span 2; }\n  }"
        ),
        "portrait_single_column_direction": ".focus-index { margin-right: 0; }",
        "desktop_wrapped_grid": (
            f"grid-template-columns: repeat({DESKTOP_FOCUS_KEY_COLUMNS}, "
            "minmax(0, 1fr));"
        ),
        "desktop_no_horizontal_paging": (
            f"grid-template-columns: repeat({DESKTOP_FOCUS_KEY_COLUMNS}, "
            "minmax(0, 1fr));\n"
            f"      gap: {DESKTOP_FOCUS_KEY_GAP_PX}px;\n"
            "      overflow-x: visible;\n"
            "      padding-bottom: 0;"
        ),
        "desktop_index_font": (
            f"height: {_DESKTOP_FOCUS_KEY_INDEX_WIDTH_PX}px;\n"
            "      margin-right: 0;\n"
            f"      font-size: {FOCUS_KEY_INDEX_FONT_FLOOR_PX}px;"
        ),
        "short_question_font": (
            "#opening-question { margin-top: 2px; "
            f"font-size: {SHORT_OPENING_QUESTION_FONT_PX}px; }}"
        ),
        "short_lower_value_metadata_hidden": (
            "#scope-summary,\n    #scope-ids { position: absolute; width: 1px;"
        ),
    }
    missing_tokens = [
        token_id for token_id, token in required_tokens.items() if token not in html
    ]
    direction_span_rule_count = html.count(
        '.focus-chip[data-label-id="legend_direction"] { grid-column: span 2; }'
    )
    profile_font_px = {
        "1920x1080": {
            "text": DESKTOP_FOCUS_KEY_FONT_PX,
            "index": FOCUS_KEY_INDEX_FONT_FLOOR_PX,
        },
        "1440x900": {
            "text": DESKTOP_FOCUS_KEY_FONT_PX,
            "index": FOCUS_KEY_INDEX_FONT_FLOOR_PX,
        },
        "1024x768": {
            "text": TABLET_FOCUS_KEY_FONT_PX,
            "index": TABLET_FOCUS_KEY_FONT_PX,
        },
        "844x390": {
            "text": SHORT_FOCUS_KEY_FONT_PX,
            "index": SHORT_FOCUS_KEY_FONT_PX,
        },
        "390x844": {
            "text": PORTRAIT_FOCUS_KEY_FONT_PX,
            "index": FOCUS_KEY_INDEX_FONT_FLOOR_PX,
        },
    }
    minimum_text_font = min(profile["text"] for profile in profile_font_px.values())
    minimum_index_font = min(profile["index"] for profile in profile_font_px.values())
    return {
        "passed": (
            not missing_tokens
            and direction_span_rule_count == 1
            and minimum_text_font >= FOCUS_KEY_INDEX_FONT_FLOOR_PX
            and minimum_index_font >= FOCUS_KEY_INDEX_FONT_FLOOR_PX
            and SHORT_OPENING_QUESTION_FONT_PX >= 10.0
        ),
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "aria_label": "Focus key: visual grammar and numbered topology labels",
        "profile_font_px": profile_font_px,
        "minimum_text_font_px": minimum_text_font,
        "minimum_index_font_px": minimum_index_font,
        "required_minimum_font_px": FOCUS_KEY_INDEX_FONT_FLOOR_PX,
        "short_opening_question_font_px": SHORT_OPENING_QUESTION_FONT_PX,
        "direction_column_span_by_profile": {
            "desktop": 2,
            "tablet": 2,
            "short": 2,
            "portrait": 1,
        },
        "direction_span_rule_count": direction_span_rule_count,
        "required_token_ids": list(required_tokens),
        "missing_token_ids": missing_tokens,
    }


def fixed_grammar_key_contract() -> dict[str, Any]:
    """Verify fixed grammar rows are unnumbered, accessible, and visibly distinct."""
    html = _player_template()
    required_tokens = {
        "independent_copy_source": "const focusKeyCopyById = data.focus_key_copy || {};",
        "independent_copy_lookup": (
            "focusKeyCopyById[id] || mapLabelById.get(id)?.textContent.trim()"
        ),
        "unknown_id_fails_closed": (
            "if (grammarId && !grammarCue) throw new Error(`Unknown fixed grammar key ID: ${id}`);"
        ),
        "grammar_role": 'chip.dataset.keyRole = grammarCue ? "grammar" : "geometry";',
        "unnumbered_swatch": "swatch.dataset.cue = grammarCue;",
        "geometry_only_numbering": (
            "key.querySelectorAll('[data-key-role=\"geometry\"]').length + 1"
        ),
        "carrier_cue": '.focus-swatch[data-cue="carrier"]::before',
        "direction_cue": '.focus-swatch[data-cue="direction"]::after',
        "posture_cue": '.focus-swatch[data-cue="posture"]::before',
        "solid_cue": '.focus-swatch[data-cue="solid"]::before',
        "dotted_cue": '.focus-swatch[data-cue="dotted"]::before',
        "dashed_cue": '.focus-swatch[data-cue="dashed"]::before',
        "conceptual_cue": '.focus-swatch[data-cue="conceptual"]::before',
    }
    missing_tokens = [
        token_id for token_id, token in required_tokens.items() if token not in html
    ]
    profile_fonts = {
        "standard": 10.0,
        "tablet": TABLET_FOCUS_KEY_FONT_PX,
        "short": SHORT_FOCUS_KEY_FONT_PX,
        "portrait": PORTRAIT_FOCUS_KEY_FONT_PX,
    }
    minimum_font = min(profile_fonts.values())
    cue_values = list(_LEGEND_GRAMMAR_CUES.values())
    return {
        "passed": (
            not missing_tokens
            and len(cue_values) == len(set(cue_values))
            and minimum_font >= 10.0
        ),
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "grammar_ids": list(_LEGEND_GRAMMAR_CUES),
        "grammar_cues": dict(_LEGEND_GRAMMAR_CUES),
        "cue_count": len(cue_values),
        "cues_visibly_distinct": len(cue_values) == len(set(cue_values)),
        "numbering": "geometry_rows_only",
        "anchoring": "geometry_rows_only",
        "full_accessible_copy_source": "authored_master_copy_plus_named_direction_example",
        "profile_font_px": profile_fonts,
        "minimum_font_px": minimum_font,
        "required_minimum_font_px": 10.0,
        "required_token_ids": list(required_tokens),
        "missing_token_ids": missing_tokens,
    }


def portrait_transport_slot_contract() -> dict[str, Any]:
    """Backward-compatible portrait view of the all-viewport slot contract."""
    contract = transport_slot_contract()
    assignments = {"previous": 1, "teaching": 2, "evidence": 3, "next": 4}
    return {
        **contract,
        "viewport_id": (
            f"{PORTRAIT_REFERENCE_VIEWPORT_WIDTH_PX}x"
            f"{PORTRAIT_REFERENCE_VIEWPORT_HEIGHT_PX}"
        ),
        "column_count": 4,
        "annotated_assignments": assignments,
        "unannotated_assignments": assignments,
        "unannotated_teaching_slot": "reserved_hidden",
    }


def focused_geometry_stroke_contract() -> dict[str, Any]:
    """Verify focused SVG groups receive non-scaling stroke and dash treatment."""
    html = _player_template()
    required_tokens = {
        "focused_node_state": (
            'element.dataset.focusState = focusNodes.has(id) ? "focused" : "context";'
        ),
        "focused_edge_state": (
            'element.dataset.focusState = focusEdges.has(id) ? "focused" : "context";'
        ),
        "stroke_selector": ('#map-svg [data-focus-state="focused"] [stroke-width],'),
        "dash_selector": ('#map-svg [data-focus-state="focused"] [stroke-dasharray] {'),
        "non_scaling_stroke": "vector-effect: non-scaling-stroke;",
    }
    missing_tokens = [
        token_id for token_id, token in required_tokens.items() if token not in html
    ]
    return {
        "passed": not missing_tokens,
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "application": "focused_nodes_and_edges",
        "scaling_mode": "non_scaling_stroke",
        "minimum_effective_stroke_px": FOCUSED_GEOMETRY_STROKE_FLOOR_PX,
        "minimum_effective_dash_px": FOCUSED_GEOMETRY_DASH_FLOOR_PX,
        "required_token_ids": list(required_tokens),
        "missing_token_ids": missing_tokens,
    }


def _markdown_escape(value: str) -> str:
    return value.replace("|", "\\|")


def build_instructor_packet(registry: dict[str, Any]) -> str:
    lines = [
        "# GIGAWATT instructor packet",
        "",
        "This packet is teaching territory, not a spoken script. It assigns no",
        "durations, cadence, or automatic visual changes. The presenter decides how",
        "long to remain in each segment and may open the evidence view when the",
        "explanation benefits.",
        "",
        "## Run and test",
        "",
        "```sh",
        "python3 -m http.server --directory diagram 8000",
        "```",
        "",
        "Open `http://localhost:8000/course.html`. Use the segment rail or left/right",
        "arrow keys to move through the course. `Show evidence` (or the E key) opens",
        "the sourced claims, known limits, claim boundaries, and",
        "primary-source links. No state advances on its own.",
        "",
        "For a first editorial pass, check whether each opening question naturally",
        "invites the explanation, whether the focused frame remains useful,",
        "whether the evidence boundary is sayable in your own words, and whether the",
        "handoff makes the next segment feel inevitable. Record notes by segment ID.",
        "",
    ]
    current_act: str | None = None
    for segment in registry["segments"]:
        if segment["act_id"] != current_act:
            current_act = segment["act_id"]
            lines.extend(
                [
                    f"## Act {segment['act_sequence']}: {segment['act_title']}",
                    "",
                    segment["act_objective"],
                    "",
                ]
            )
        readiness = segment["evidence_readiness"].replace("_", " ")
        lines.extend(
            [
                f"### {segment['sequence']:02d}. {segment['title']} `{segment['segment_id']}`",
                "",
                f"- Opening question: {segment['opening_question']}",
                f"- Teaching objective: {segment['learning_objective']}",
                f"- Visual focus: {', '.join(segment['focus_node_labels'])}",
                f"- Visual state: focused {segment['render_mode'].upper()} view; evidence panel on demand.",
                f"- Evidence posture: **{readiness}**",
                "",
            ]
        )
        annotation = segment["visual"]["annotation"]
        if annotation is not None:
            lines.extend(
                [
                    "Presenter-facing teaching focus:",
                    "",
                    f"- Kind: `{annotation['kind']}`",
                    f"- Title: {_markdown_escape(annotation['title'])}",
                    "",
                ]
            )
            for index, item in enumerate(annotation["items"], start=1):
                claim_ids = ", ".join(f"`{claim_id}`" for claim_id in item["claim_ids"])
                lines.extend(
                    [
                        f"{index}. {_markdown_escape(item['label'])}",
                        f"   - Claim IDs: {claim_ids}",
                    ]
                )
            lines.append("")
        lines.extend(["Validated claim territory:", ""])
        for claim in segment["claims"]:
            assertion = claim["assertion"].replace("_", " ")
            lines.append(f"- **{claim['id'].replace('_', ' ')} — {assertion}.**")
            binding = (
                "segment-local, nonphysical teaching overlay"
                if claim["binding"] == "overlay"
                else "selected topology ownership"
            )
            lines.append(f"  - Binding: {binding}")
            for fact in claim["facts"]:
                sources = ", ".join(
                    f"[{source['publisher']} — {_markdown_escape(source['title'])}]({source['url']}) "
                    f"(accessed {source['accessed_as_of']}; {_markdown_escape(source['date_note'])})"
                    for source in fact["sources"]
                )
                lines.extend(
                    [
                        f"  - {_markdown_escape(fact['value'])}",
                        f"  - Fact: `{fact['ref']}`",
                        f"  - Basis: {_markdown_escape(fact['basis'])}",
                        f"  - Scope: {_markdown_escape(fact['scope'])}",
                        f"  - Boundary: `{fact['posture']}` / `{fact['lifecycle']}` / as of {fact['as_of']}",
                    ]
                )
                if fact["topology_targets"]:
                    targets = "; ".join(
                        f"{target['kind']} `{target['id']}` ({_markdown_escape(target['label'])}; "
                        f"`{target['presence']}` / `{target['lifecycle']}`)"
                        for target in fact["topology_targets"]
                    )
                    lines.append(f"  - Topology target: {targets}")
                lines.append(f"  - Sources: {sources}")
        lines.extend(["", "Red-line warnings:", ""])
        for guard in segment["promotion_guard_warnings"]:
            lines.append(
                f"- **{guard['id'].replace('_', ' ')}.** {_markdown_escape(guard['warning'])}"
            )
        if segment["blocking_research"]:
            lines.extend(["", "Explicit evidence boundary:", ""])
            lines.extend(f"- {item}" for item in segment["blocking_research"])
        if segment["transition"]:
            lines.extend(["", f"Handoff: {segment['transition']['cue']}", ""])
        else:
            lines.extend(
                [
                    "",
                    "Close: Return to the opening question and state which conversions are evidenced, assumed, or still unknown.",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def build_registry_artifacts(
    registry: dict[str, Any],
    course: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
) -> tuple[str, str, str]:
    """Render exact course artifacts for an already compiled runtime registry."""

    digest = registry.get("source_digest")
    if not isinstance(digest, str) or len(digest) != 64:
        raise CourseRuntimeError("compiled runtime source_digest must be SHA-256")
    registry_json = scene_pipeline.canonical_payload(registry) + "\n"

    master_evidence = ledgers[course["meta"]["master_evidence_ledger"]]
    _, map_scene = layout_pipeline.compose(master, layout, master_evidence)
    shared = scene_pipeline.build_payload(master, scene, cameras)
    focus_key_copy = {}
    for copy_id in _LEGEND_GRAMMAR_CUES:
        authored = layout_pipeline.resolve_copy(
            master,
            master_evidence,
            copy_id,
            include_hidden=True,
        )
        if not isinstance(authored, str) or not authored.strip():
            raise CourseRuntimeError(
                f"fixed grammar key {copy_id!r} must resolve to authored copy"
            )
        focus_key_copy[copy_id] = _focus_key_accessible_label(copy_id, authored.strip())
    player_payload = {
        "registry": registry,
        "focus_key_copy": focus_key_copy,
        "scene": {
            "palette": shared["palette"],
            "stroke": shared["stroke"],
            "world": shared["world"],
            "structures": shared["structures"],
            "nodes": shared["nodes"],
            "edges": shared["edges"],
        },
        "hidden": {
            "nodes": sorted(
                node["id"]
                for node in master["nodes"]
                if node.get("base_visible", True) is False
            ),
            "edges": sorted(
                edge["id"]
                for edge in master["edges"]
                if edge.get("base_visible", True) is False
            ),
            "copy": sorted(
                copy_id
                for copy_id, record in master["copy"].items()
                if record.get("base_visible", True) is False
            ),
        },
    }
    player = (
        _player_template()
        .replace("__DATA__", _script_safe_payload(player_payload))
        .replace("__MAP_SCENE__", map_scene)
        .replace("__DIGEST__", digest)
        .replace("__PAPER__", tokens.PAPER)
        .replace("__INK__", tokens.INK)
        .replace("__FAINT__", tokens.FAINT)
        .replace("__MUTED__", tokens.MUTED_TEXT)
        .replace("__FONT__", tokens.FONT)
    )
    packet = build_instructor_packet(registry)
    return registry_json, player, packet


def build_artifacts() -> tuple[str, str, str, str]:
    course, cameras, master, layout, scene, ledgers, visuals = load_inputs()
    _validate_course_inputs(course, cameras, master, ledgers)
    digest = _source_digest(course)
    registry = compile_registry(
        course,
        cameras,
        master,
        layout,
        scene,
        ledgers,
        visuals,
        source_digest=digest,
    )
    registry_json, player, packet = build_registry_artifacts(
        registry,
        course,
        cameras,
        master,
        layout,
        scene,
        ledgers,
    )
    return registry_json, player, packet, digest


def main() -> None:
    registry, player, packet, digest = build_artifacts()
    REGISTRY_PATH.write_text(registry)
    PLAYER_PATH.write_text(player)
    PACKET_PATH.write_text(packet)
    print(
        f"built {REGISTRY_PATH.relative_to(ROOT)}, {PLAYER_PATH.relative_to(ROOT)}, "
        f"and {PACKET_PATH.relative_to(ROOT)} · {EXPECTED_SEGMENTS} manual segments "
        f"· digest {digest}"
    )


if __name__ == "__main__":
    main()
