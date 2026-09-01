"""Compile deterministic course-quality and dependency-graph registries.

The quality registry measures every authored course segment without combining
the dimensions into a single score.  The dependency graph keeps the ownership
chain from primary evidence through each viewport evaluation inspectable, so a
defect can be traced to its owner and its downstream impact cone.

Usage: uv run python -m gigawatt.quality
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import struct
import zlib
from collections import Counter, defaultdict, deque
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime
from itertools import pairwise
from pathlib import Path, PurePosixPath
from typing import Any

from . import champion as champion_pipeline
from . import course_runtime, generated_artifacts, ratchet, shots, tokens
from . import layout as layout_pipeline
from . import scene as scene_pipeline

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
QUALITY_PATH = DIAGRAM / "course_quality.json"
GRAPH_PATH = DIAGRAM / "course_dependency_graph.json"
RATCHET_PATH = ROOT / "course" / "quality_ratchet.yaml"
AUDITS_PATH = ROOT / "course" / "quality_audits.yaml"
GENERATED_OUTPUT_PATH_ALLOWLIST = frozenset(
    {
        "course/INSTRUCTOR_PACKET.md",
        "course/INSTRUCTOR_PACKET_V2.md",
        "diagram/camera_system_orientation.svg",
        "diagram/camera_watt_heat_handoff.svg",
        "diagram/course.html",
        "diagram/course_v2.html",
        "diagram/course_v2_runtime.json",
        "diagram/course_dependency_graph.json",
        "diagram/course_quality.json",
        "diagram/course_runtime.json",
        "diagram/hybrid.html",
        "diagram/map_watt_heat_handoff.svg",
        "diagram/master.svg",
        "diagram/mock_wide.svg",
        "diagram/mock_zoom.svg",
        "diagram/phase1_generation.html",
        "diagram/phase2_transmission.html",
        "diagram/phase3_campus.html",
        "diagram/phase4_building.html",
        "diagram/phase5_compute.html",
        "diagram/phase6_heat.html",
        "diagram/planned_shots.html",
        "diagram/planned_shots.json",
        "diagram/s10_two_rack_heat_paths.html",
    }
)
ACCEPTANCE_GENERATED_ARTIFACT_IDS = tuple(
    sorted(
        set(generated_artifacts.ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS)
        | {
            "diagram/course_dependency_graph.json",
            "diagram/course_quality.json",
        }
    )
)
VALIDATION_COMPILER_IMPLEMENTATION_PATHS = tuple(
    sorted(
        [
            *(ROOT / "src" / "gigawatt").glob("*.py"),
            DIAGRAM / "generate_phase1_generation.py",
            DIAGRAM / "generate_phase2_transmission.py",
            DIAGRAM / "generate_phase3_campus.py",
            DIAGRAM / "generate_phase4_building.py",
            DIAGRAM / "generate_phase5_compute.py",
            DIAGRAM / "generate_phase6_heat.py",
            DIAGRAM / "generate_course_v2.py",
            DIAGRAM / "generate_s10_two_rack_heat_paths.py",
        ],
        key=lambda path: path.relative_to(ROOT).as_posix(),
    )
)

SCHEMA_VERSION = 1
OCCUPANCY_CAPTURE_SCHEMA_VERSION = 2
VIEWPORTS = (
    {"id": "1920x1080", "width": 1920, "height": 1080},
    {"id": "1440x900", "width": 1440, "height": 900},
    {"id": "1024x768", "width": 1024, "height": 768},
    {"id": "844x390", "width": 844, "height": 390},
    {"id": "390x844", "width": 390, "height": 844},
)
PORTRAIT_VIEWPORT_ID = "390x844"
SHORT_VIEWPORT_ID = "844x390"
TABLET_VIEWPORT_ID = "1024x768"
DESKTOP_VIEWPORT_IDS = ("1920x1080", "1440x900")
PORTRAIT_FOCUS_KEY_EVIDENCE_SCOPE = "deterministic_static_estimate_not_live_browser"
SHORT_FOCUS_KEY_EVIDENCE_SCOPE = "deterministic_static_estimate_not_live_browser"
TABLET_FOCUS_KEY_EVIDENCE_SCOPE = "deterministic_static_estimate_not_live_browser"
DESKTOP_FOCUS_KEY_EVIDENCE_SCOPE = "deterministic_static_estimate_not_live_browser"
PORTRAIT_TEACHING_DRAWER_EVIDENCE_SCOPE = (
    "deterministic_source_contract_not_live_browser"
)
GRAPH_STAGES = (
    "source",
    "fact",
    "topology",
    "segment",
    "shot",
    "frame",
    "evaluation",
)
EVIDENCE_INVENTORY_POLICY = (
    "graph nodes include only sources and facts referenced by course claims; "
    "inventory-only IDs preserve full-ledger transparency without implying "
    "course impact"
)
CLAIM_NODE_TYPES = {"topology": "topology_claim", "overlay": "overlay_claim"}

OCCUPANCY_RISK_FLAGS = frozenset({"low_focus_occupancy", "low_projected_occupancy"})
OCCUPANCY_METRIC_BY_RISK_FLAG = {
    "low_focus_occupancy": "two_dimensional.focus_occupancy",
    "low_projected_occupancy": "three_dimensional.projected_occupancy",
}
OCCUPANCY_REVIEW_STATUSES = frozenset({"unresolved", "live_approved", "live_rejected"})
OCCUPANCY_LIVE_DECISION_BY_STATUS = {
    "unresolved": None,
    "live_approved": "approved",
    "live_rejected": "rejected",
}
OCCUPANCY_LIVE_REVIEW_FIELDS = frozenset(
    {
        "decision",
        "reviewer_id",
        "reviewed_at",
        "candidate_current_state_sha256",
        "validation_compiler_implementation_sha256",
        "modeled_evaluation_sha256",
        "artifact_sha256",
        "evidence_ref",
    }
)
QUALITY_RISK_DIMENSIONS = {
    "density_pressure": frozenset({"dense_focus"}),
    "label_pressure": frozenset(
        {"visible_label_pressure", "label_area_pressure", "label_clipping"}
    ),
    "occupancy": OCCUPANCY_RISK_FLAGS,
    "annotation": frozenset({"dense_annotation_coverage_gap"}),
    "overlay": frozenset(
        {
            "overlay_residual_label_collision",
            "overlay_suppression_focus_key_gap",
            "overlay_viewport_clipping",
            "overlay_masthead_clipping",
            "overlay_transport_clipping",
            "overlay_stage_clipping",
            "overlay_stage_edge_clearance",
            "overlay_stage_dominance",
        }
    ),
    "geometry_projection": frozenset(
        {
            "focus_key_geometry_correspondence_gap",
            "projected_clipping",
        }
    ),
}
METRIC_REGRESSION_TOLERANCE = 0.000001
LABEL_FRAME_MARGIN_TOLERANCE = 0.001
PROTECTED_NONREGRESSION_METRICS = {
    "annotation.claim_coverage": "must_not_decrease",
    "visible_label_count": "must_not_increase",
    "teaching_overlay.residual_collision_count": "must_not_increase",
    "teaching_overlay.stage_clipped": "must_not_increase",
    "teaching_overlay.height_stage_ratio": "must_not_increase_after_presence",
    "teaching_overlay.area_stage_ratio": "must_not_increase_after_presence",
    "fixed_focus_key.numbered_geometry_correspondence.passed": "must_not_decrease",
    "two_dimensional.focus_occupancy": "must_not_decrease",
    "two_dimensional.rendered_pixel_ratio_to_full_stage": "must_not_decrease",
    "two_dimensional.projected_base_font_px": "must_not_decrease",
    "two_dimensional.estimated_label_pixels": "must_not_increase",
    "two_dimensional.label_stage_ratio": "must_not_increase",
    "three_dimensional.projected_occupancy": "must_not_decrease",
    "three_dimensional.clipped_point_count": "must_not_increase",
    "three_dimensional.residual_label_collision_count": "must_not_increase",
    "three_dimensional.residual_stage_clip_count": "must_not_increase",
}
TEACHING_OVERLAY_CONSUMER_METRICS = frozenset(
    {
        "teaching_overlay.residual_collision_count",
        "teaching_overlay.stage_clipped",
        "teaching_overlay.height_stage_ratio",
        "teaching_overlay.area_stage_ratio",
        "two_dimensional.focus_occupancy",
        "two_dimensional.rendered_pixel_ratio_to_full_stage",
        "two_dimensional.projected_base_font_px",
        "two_dimensional.estimated_label_pixels",
        "two_dimensional.label_stage_ratio",
        "three_dimensional.projected_occupancy",
    }
)

# These are protected because the course-quality brief names them as the first
# dense frames to ratchet.  The computed focus-density lower decile is reported
# separately and may change as the authored topology changes.
PROTECTED_DENSE_SEGMENTS = (
    "s16_close_atmosphere",
    "s19_fast_load_slow_grid",
    "s20_build_sequence",
    "s21_capital_ownership",
    "s24_megawatts_to_tokens",
)

DENSE_FOCUS_MIN_ITEMS = 19
MAX_VISIBLE_LABELS = 16
MAX_LABEL_STAGE_RATIO = 0.16
MIN_FOCUS_OCCUPANCY = 0.08
MIN_PROJECTED_OCCUPANCY = 0.08
MIN_DENSE_ANNOTATION_CLAIM_COVERAGE = 0.25
MAX_OVERLAY_STAGE_HEIGHT_RATIO = 0.50
MAX_OVERLAY_STAGE_AREA_RATIO = 0.50
MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX = 8.0
TEACHING_DOCK_GAP_PX = 12.0
MAX_FOCUS_MARKER_DISPLACEMENT_PX = 48.0
FOCUS_MARKER_SIZE_PX = 20.0
FOCUS_MARKER_STEP_PX = 22.0

MAP_HORIZONTAL_PADDING = 44
MAP_VERTICAL_PADDING = 36
MAP_BASE_FONT_PX = 10.5
MIN_SPATIAL_LABEL_FONT_PX = 10.0
MIN_FOCUSED_GEOMETRY_STROKE_PX = course_runtime.FOCUSED_GEOMETRY_STROKE_FLOOR_PX
MIN_FOCUSED_GEOMETRY_DASH_PX = course_runtime.FOCUSED_GEOMETRY_DASH_FLOOR_PX
MIN_ANNOTATED_THREE_DIMENSIONAL_STANDARD_CANVAS_WIDTH_PX = 400.0
FOCUS_KEY_FONT_PX = 10.0
THREE_LABEL_FONT_PX = 10.0
THREE_LABEL_BOX_CHROME_PX = 16.0
THREE_LABEL_PRINTABLE_ASCII_ADVANCE_GROUPS = (
    (0.35, "'"),
    (0.36, " il"),
    (0.38, ",."),
    (0.42, "!:;j"),
    (0.44, "f"),
    (0.47, "t"),
    (0.49, "-"),
    (0.51, "r"),
    (0.56, "()I[]|"),
    (0.60, '"Jc'),
    (0.61, "sz"),
    (0.63, "?"),
    (0.65, "L"),
    (0.66, "Fv"),
    (0.67, "y"),
    (0.68, "aex"),
    (0.69, "k"),
    (0.70, "/ET\\o"),
    (0.71, "Zbdgpq"),
    (0.72, "S"),
    (0.73, "$*0123456789_`hnu{}"),
    (0.75, "PY"),
    (0.76, "C"),
    (0.78, "BVX"),
    (0.79, "AK"),
    (0.80, "R"),
    (0.83, "GU"),
    (0.84, "D"),
    (0.85, "H"),
    (0.86, "NOQ"),
    (0.88, "#&+<=>^~"),
    (0.96, "M"),
    (0.99, "w"),
    (1.03, "@"),
    (1.07, "m"),
    (1.14, "W"),
    (1.29, "%"),
)
THREE_LABEL_PRINTABLE_ASCII_ADVANCE_EM = {
    character: advance
    for advance, characters in THREE_LABEL_PRINTABLE_ASCII_ADVANCE_GROUPS
    for character in characters
}
CAMERA_FOV_DEGREES = scene_pipeline.THREE_CAMERA_VERTICAL_FOV_DEGREES
CAMERA_NEAR = scene_pipeline.THREE_CAMERA_NEAR
CAMERA_FAR = scene_pipeline.THREE_CAMERA_FAR
ALLOWED_LEGEND_SEGMENT_IDS = {"p1_read_the_machine"}
PROTECTED_MAP_COPY_IDS = frozenset(shots.PROTECTED_MAP_COPY_IDS)
LEGACY_TEACHING_OVERLAY_STANDARD_WIDTH_PX = 390.0
LEGACY_PHYSICAL_DEFECT_POLICIES = {
    "1440x900": {
        "maximum_full_stage_ratio": 0.40,
        "minimum_gain_ratio": 1.15,
    },
    "1024x768": {
        "maximum_full_stage_ratio": 0.30,
        "minimum_gain_ratio": 1.10,
    },
}

RATCHET_HYPOTHESIS = (
    "Relative to the corrected experiment control, combining focused labels with "
    "claim-bound semantic overlays removes label pressure and dense-annotation "
    "gaps without changing facts, topology, order, or frames."
)
EXPECTED_CHAMPION = {
    "git_sha": "0856a93b78181bec3945168632d141595575800c",
    "origin_sha": "0856a93b78181bec3945168632d141595575800c",
    "source_tree_aggregate_sha256": (
        "f95a3887fb294005b9201485a69121c95bef9c4dcce2e5c4ba737e60e90d9e8b"
    ),
    "baseline_test_count": 349,
    "baseline_runtime_source_digest": (
        "407277f9e170254051393046bcfb6f43caa25ce09a665d3d7020ac764f127d04"
    ),
    "artifact_sha256": {
        "diagram/course.html": (
            "d174f41e5439a72a88fee844a6b629d4bf6c3cb036333321f02ba0f8503a25bb"
        ),
        "diagram/course_runtime.json": (
            "25b7564075e58ee69563b5abd75148ac933ffec65554887c0972024e8504802d"
        ),
        "diagram/planned_shots.html": (
            "ebab25664a01e723c501c7df7d283584d3118aba2493081a89a0e1e821a67ac4"
        ),
        "diagram/planned_shots.json": (
            "33ad49f945e89f69e3e909a3687b14d40855ea175380a686e51b38d5b7aab39b"
        ),
        "course/INSTRUCTOR_PACKET.md": (
            "9b651b42cc1c8f7803b4b3cefdd7e076504d43540515a62895682f832c4aea34"
        ),
    },
}
EXPECTED_EXPERIMENT_CONTROL = {
    "control_id": "corrected_current_worktree_context_control",
    "provenance": "synthetic model on the corrected current worktree",
    "frozen_champion_equivalent": False,
    "historical_viewport_captures_available": False,
    "visual_overrides": {},
    "label_source": "champion_context",
    "annotation_source": "none",
}
EXPECTED_HARD_CONSTRAINTS = {
    "evidence_and_topology_remain_correct": True,
    "unknowns_remain_unknown": True,
    "forbidden_motion_patterns": ["autoplay", "micro_beats", "generic_zoom"],
    "accessibility_must_pass": True,
    "deterministic_generation_must_pass": True,
    "forbidden_render_defects": ["clipping", "collisions", "illegible_labels"],
}
EXPECTED_VARIANTS = {
    "labels_only": {"label_source": "current", "annotation_source": "none"},
    "annotations_only": {
        "label_source": "champion_context",
        "annotation_source": "current",
    },
    "combined": {"label_source": "current", "annotation_source": "current"},
}
OCCUPANCY_REVIEW_CANDIDATE_IDS = ("experiment_control", *EXPECTED_VARIANTS)
RATCHET_TARGET_GATE_IDS = {
    "labels_only": ("label_pressure",),
    "annotations_only": ("dense_annotation_gap",),
    "combined": ("label_pressure", "dense_annotation_gap"),
}
FINAL_ACCEPTANCE_GATE_IDS = (
    "prerequisite_correctness_repairs",
    "historical_frozen_champion_viewport_captures",
    "browser",
    "accessibility_snapshot",
    "blind_review",
)
FINAL_ACCEPTANCE_STATUSES = frozenset({"accepted", "rejected", "pending"})
FINAL_ACCEPTANCE_GATE_STATUSES = frozenset({"passed", "failed", "pending"})
BLIND_REVIEWER_IDS = (
    "blind_reviewer_1",
    "blind_reviewer_2",
    "blind_reviewer_3",
)
ACCEPTANCE_EVIDENCE_SCHEME = "course-quality-evidence"
ACCEPTANCE_INDEPENDENT_GATE_IDS = (
    "prerequisite_correctness_repairs",
    "historical_frozen_champion_viewport_captures",
)
ACCEPTANCE_GENERATION_SEEDS = (1, 7, 777)
ACCEPTANCE_EVIDENCE_DIRECTORY = PurePosixPath("course/acceptance_evidence")
EXPECTED_PREREQUISITE_REPAIRS = {
    "status": "separate_correctness_candidate",
    "rationale": (
        "Evidence, topology, accessibility, and frame-derivation defects found "
        "during the audit must not be attributed to the visual hypothesis."
    ),
    "frozen_champion_invariant_delta": {
        "facts_unchanged": False,
        "topology_unchanged": False,
        "claim_set_unchanged": False,
        "derived_frames_unchanged": False,
        "course_order_unchanged": True,
        "course_objectives_unchanged": True,
    },
    "scopes": [
        "effective-versus-access date correction",
        "conceptual topology posture and exact owner correction",
        "claim locality and source disclosure",
        "accessibility and keyboard repair",
        "rotated geometry bounds and complete generator dependency digest",
    ],
}
EXPECTED_AUDIT_POLICIES = {
    "evidence_scope": {
        "audit_basis": "current worktree source, generated DOM, and static quality model",
        "browser_rendering": "unavailable_pending",
        "historical_frozen_champion_viewport_captures": "unavailable_pending",
        "accessibility_snapshot": "unavailable_pending",
        "blind_review": "unavailable_pending",
        "interpretation": (
            "A complete static audit round is not live-browser proof and cannot "
            "promote a challenger."
        ),
    },
    "priority_policy": {
        "formula": (
            "severity * teaching_importance * affected_sections * confidence / "
            "repair_risk"
        ),
        "selection_rule": (
            "Select a highest exact priority score; ties are admissible."
        ),
        "optimization_target": "worst sections and lower decile, not the average",
        "weighted_average_is_sufficient": False,
        "density_alone_is_a_defect": False,
    },
    "loop_policy": {
        "fast": [
            "layout",
            "label_hierarchy",
            "framing",
            "annotation",
            "authored_transformation",
            "navigation",
            "accessibility",
        ],
        "slow": ["primary_source_research"],
        "slow_trigger": (
            "Use the slow loop only when a pedagogical problem genuinely traces to "
            "missing evidence; ambiguous evidence remains null or explicitly limited."
        ),
    },
    "consultation_policy": {
        "autonomous_reversible_scopes": [
            "layout",
            "label_hierarchy",
            "framing",
            "annotation",
            "authored_transformation",
            "navigation",
            "accessibility",
        ],
        "consultation_required_scopes": [
            "course_thesis",
            "course_order",
            "course_objectives",
            "visual_language",
            "substantive_material_removal",
            "evidence_boundary_weakening",
            "pareto_incomparable_aesthetic",
            "private_as_built_evidence",
            "presenter_comfort",
            "learner_retention",
        ],
    },
    "saturation_policy": {
        "required_consecutive_complete_rounds": 2,
        "required_independent_roles": [
            "visual_layout",
            "pedagogy",
            "adversarial_correctness",
        ],
        "required_segment_count_per_role": 26,
        "stop_only_when": [
            "two consecutive complete audits produce no admissible improvement",
            "no high-priority finding remains",
            "all 26 sections pass global review",
        ],
        "pending_candidate_or_admissible_change_prevents_saturation": True,
        "final_acceptance_gates_remain_separate": True,
        "universal_learner_retention_guaranteed": False,
    },
    "change_ownership_policy": {
        "generated_html_is_never_a_change_owner": True,
        "finding_links_required": True,
        "change_owner_links_required": True,
        "canonical_change_registry": "course/quality_ratchet.yaml#changes",
    },
}
EXPECTED_AUDIT_HIGH_PRIORITY_THRESHOLD = 100.0


class QualityError(ValueError):
    """Raised when the quality model cannot resolve a canonical owner."""


def _unique_nonempty_strings(value: Any) -> bool:
    return (
        isinstance(value, list)
        and bool(value)
        and all(isinstance(item, str) and item for item in value)
        and len(value) == len(set(value))
    )


def _matches_exact_contract_value(actual: Any, expected: Any) -> bool:
    """Compare policy values without Python's bool/int equality coercion."""
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(
            _matches_exact_contract_value(actual[key], expected_value)
            for key, expected_value in expected.items()
        )
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(
            _matches_exact_contract_value(actual_item, expected_item)
            for actual_item, expected_item in zip(actual, expected, strict=True)
        )
    return actual == expected


def _sha256_string(value: Any, location: str) -> str:
    if (
        not isinstance(value, str)
        or len(value) != 64
        or value != value.lower()
        or any(character not in "0123456789abcdef" for character in value)
    ):
        raise QualityError(f"{location} must be a lowercase SHA-256 digest")
    return value


def _integer_at_least(value: Any, minimum: int, location: str) -> int:
    if type(value) is not int or value < minimum:
        raise QualityError(f"{location} must be an integer >= {minimum}")
    return value


def _candidate_acceptance_provenance(
    manifest: dict[str, Any], challenger: dict[str, Any]
) -> str:
    """Bind evidence to the exact non-circular candidate declaration."""

    candidate_id = challenger["candidate_id"]
    payload = {
        "schema_version": manifest["schema_version"],
        "hard_constraints": manifest["hard_constraints"],
        "frozen_champion": manifest["frozen_champion"],
        "experiment_control": manifest["experiment_control"],
        "hypothesis_id": manifest["hypothesis_id"],
        "hypothesis": manifest["hypothesis"],
        "prerequisite_repairs": manifest["prerequisite_repairs"],
        "variant": manifest["variants"][candidate_id],
        "challenger_change": challenger,
    }
    return hashlib.sha256(
        scene_pipeline.canonical_payload(payload).encode()
    ).hexdigest()


def _experiment_control_occupancy_provenance(manifest: dict[str, Any]) -> str:
    """Bind control reviews to the exact synthetic-control declaration."""

    payload = {
        "schema_version": manifest["schema_version"],
        "hard_constraints": manifest["hard_constraints"],
        "frozen_champion": manifest["frozen_champion"],
        "experiment_control": manifest["experiment_control"],
        "hypothesis_id": manifest["hypothesis_id"],
        "hypothesis": manifest["hypothesis"],
        "prerequisite_repairs": manifest["prerequisite_repairs"],
        "variant": manifest["experiment_control"],
        "challenger_change": {
            "candidate_id": "experiment_control",
            "role": "experiment_control",
        },
    }
    return hashlib.sha256(
        scene_pipeline.canonical_payload(payload).encode()
    ).hexdigest()


def _canonical_sha256(value: Any) -> str:
    return hashlib.sha256(scene_pipeline.canonical_payload(value).encode()).hexdigest()


def _validation_compiler_implementation_state() -> dict[str, Any]:
    source_ids = [
        path.relative_to(ROOT).as_posix()
        for path in VALIDATION_COMPILER_IMPLEMENTATION_PATHS
    ]
    return {
        "source_ids": source_ids,
        "source_count": len(source_ids),
        "source_sha256": shots._digest_paths(VALIDATION_COMPILER_IMPLEMENTATION_PATHS),
    }


def _materialized_acceptance_artifact_state() -> list[dict[str, str]]:
    try:
        expected = generated_artifacts.build_acceptance_materialized_artifacts()
        generated_artifacts.assert_acceptance_current(expected)
    except generated_artifacts.GeneratedArtifactError as error:
        raise QualityError(str(error)) from error
    expected_ids = set(generated_artifacts.ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS)
    if set(expected) != expected_ids or not expected_ids < set(
        ACCEPTANCE_GENERATED_ARTIFACT_IDS
    ):
        raise QualityError("materialized acceptance artifact inventory is invalid")
    state = []
    for artifact_id in sorted(expected):
        expected_bytes = expected[artifact_id].encode()
        state.append(
            {
                "artifact_id": artifact_id,
                "evidence_basis": "pure_expected_output_and_retained_byte_parity",
                "output_sha256": hashlib.sha256(expected_bytes).hexdigest(),
            }
        )
    return state


def _validated_materialized_acceptance_artifact_state(
    value: Sequence[dict[str, str]],
) -> list[dict[str, str]]:
    if isinstance(value, (str, bytes)) or not isinstance(value, Sequence):
        raise QualityError("materialized acceptance artifact state must be a sequence")
    records = copy.deepcopy(list(value))
    expected_ids = sorted(generated_artifacts.ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS)
    if [
        record.get("artifact_id") for record in records if isinstance(record, dict)
    ] != expected_ids or len(records) != len(expected_ids):
        raise QualityError(
            "materialized acceptance artifact state must have exact ordered inventory"
        )
    for index, record in enumerate(records):
        if (
            not isinstance(record, dict)
            or set(record) != {"artifact_id", "evidence_basis", "output_sha256"}
            or record["evidence_basis"]
            != "pure_expected_output_and_retained_byte_parity"
        ):
            raise QualityError(
                f"materialized acceptance artifact state[{index}] is invalid"
            )
        _sha256_string(
            record["output_sha256"],
            f"materialized artifact {record['artifact_id']} output_sha256",
        )
    return records


def _current_audit_subject_state(
    *,
    runtime_digest: str,
    runtime_registry: dict[str, Any],
    ratchet_manifest: dict[str, Any],
    materialized_artifact_state: Sequence[dict[str, str]],
) -> dict[str, Any]:
    """Bind clean audit rounds to current inputs without ingesting audit history."""

    materialized_state = _validated_materialized_acceptance_artifact_state(
        materialized_artifact_state
    )
    compiler_implementation = _validation_compiler_implementation_state()
    payload = {
        "schema_version": SCHEMA_VERSION,
        "runtime_source_sha256": _sha256_string(
            runtime_digest, "current audit subject runtime source digest"
        ),
        "runtime_output_sha256": _canonical_sha256(runtime_registry),
        "validation_compiler_implementation_sha256": _sha256_string(
            compiler_implementation["source_sha256"],
            "current audit subject compiler implementation digest",
        ),
        "ratchet_manifest_payload_sha256": _canonical_sha256(ratchet_manifest),
        "ratchet_manifest_source_sha256": hashlib.sha256(
            RATCHET_PATH.read_bytes()
        ).hexdigest(),
        "materialized_artifact_set_sha256": _canonical_sha256(
            [
                {
                    "artifact_id": record["artifact_id"],
                    "output_sha256": record["output_sha256"],
                }
                for record in materialized_state
            ]
        ),
    }
    return {**payload, "audit_subject_sha256": _canonical_sha256(payload)}


def _candidate_current_state(
    *,
    candidate_id: str,
    candidate_provenance_sha256: str,
    runtime_registry: dict[str, Any],
    quality_registry: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
    materialized_artifact_state: Sequence[dict[str, str]] | None = None,
) -> dict[str, Any]:
    """Derive the non-circular compiler state to which evidence must bind.

    The modeled quality digest deliberately excludes its source digest and the
    occupancy-review ingestion surface.  Both contain ratchet evidence records;
    including either would make the evidence provenance depend on itself.
    """

    runtime_output_sha256 = _canonical_sha256(runtime_registry)
    modeled_quality = copy.deepcopy(quality_registry)
    modeled_quality.pop("source_digest", None)
    visual_gates = modeled_quality.get("visual_gates")
    if isinstance(visual_gates, dict):
        visual_gates.pop("occupancy_review", None)
    modeled_quality_output_sha256 = _canonical_sha256(modeled_quality)

    candidate_source_digest_sha256 = _sha256_string(
        runtime_registry.get("source_digest"),
        f"current state source digest for {candidate_id}",
    )
    compiler_implementation = _validation_compiler_implementation_state()
    artifact_ids = list(ACCEPTANCE_GENERATED_ARTIFACT_IDS)
    artifact_inventory_sha256 = _canonical_sha256(artifact_ids)
    expected_output_bytes = {
        "diagram/course_quality.json": (
            scene_pipeline.canonical_payload(modeled_quality) + "\n"
        ).encode(),
    }
    try:
        candidate_course_artifacts = (
            generated_artifacts.build_candidate_course_artifacts(runtime_registry)
        )
    except (
        course_runtime.CourseRuntimeError,
        generated_artifacts.GeneratedArtifactError,
    ) as error:
        raise QualityError(
            f"candidate {candidate_id!r} course artifacts could not be built: {error}"
        ) from error
    candidate_course_artifact_ids = list(
        generated_artifacts.CANDIDATE_COURSE_ARTIFACT_IDS
    )
    if set(candidate_course_artifacts) != set(candidate_course_artifact_ids):
        raise QualityError("candidate course artifact inventory is invalid")
    candidate_course_output_sha256 = {
        artifact_id: hashlib.sha256(
            candidate_course_artifacts[artifact_id].encode()
        ).hexdigest()
        for artifact_id in candidate_course_artifact_ids
    }
    candidate_graph = compile_dependency_graph(
        ledgers, runtime_registry, quality_registry
    )
    candidate_graph.pop("source_digest", None)
    expected_output_bytes["diagram/course_dependency_graph.json"] = (
        scene_pipeline.canonical_payload(candidate_graph) + "\n"
    ).encode()
    materialized_state = _validated_materialized_acceptance_artifact_state(
        _materialized_acceptance_artifact_state()
        if materialized_artifact_state is None
        else materialized_artifact_state
    )
    materialized_by_id = {
        record["artifact_id"]: record for record in materialized_state
    }
    artifact_state = []
    candidate_course_artifact_retained_parity = []
    for artifact_id in artifact_ids:
        if artifact_id in candidate_course_output_sha256:
            retained_output_sha256 = materialized_by_id[artifact_id]["output_sha256"]
            output_sha256 = candidate_course_output_sha256[artifact_id]
            retained_byte_parity = output_sha256 == retained_output_sha256
            parity_record = {
                "artifact_id": artifact_id,
                "expected_output_sha256": output_sha256,
                "retained_output_sha256": retained_output_sha256,
                "retained_byte_parity": retained_byte_parity,
            }
            candidate_course_artifact_retained_parity.append(parity_record)
            artifact_state.append(
                {
                    "artifact_id": artifact_id,
                    "evidence_basis": "candidate_specific_pure_expected_output",
                    "output_sha256": output_sha256,
                    "retained_output_sha256": retained_output_sha256,
                    "retained_byte_parity": retained_byte_parity,
                }
            )
            continue
        if artifact_id in materialized_by_id:
            artifact_state.append(materialized_by_id[artifact_id])
            continue
        if artifact_id not in expected_output_bytes:
            raise QualityError(
                f"acceptance artifact {artifact_id!r} lacks an expected-output owner"
            )
        artifact_state.append(
            {
                "artifact_id": artifact_id,
                "evidence_basis": "non_circular_in_memory_expected_projection",
                "output_sha256": hashlib.sha256(
                    expected_output_bytes[artifact_id]
                ).hexdigest(),
            }
        )
    candidate_course_artifact_mismatch_ids = [
        record["artifact_id"]
        for record in candidate_course_artifact_retained_parity
        if not record["retained_byte_parity"]
    ]
    artifact_set_sha256 = _canonical_sha256(artifact_state)

    ledger_ids = sorted(ledgers)
    evidence_inventory = []
    source_count = 0
    fact_count = 0
    for ledger_id in ledger_ids:
        ledger = ledgers[ledger_id]
        sources = ledger.get("sources")
        facts = ledger.get("facts")
        if not isinstance(sources, dict) or not isinstance(facts, dict):
            raise QualityError(
                f"current evidence ledger {ledger_id!r} lacks source/fact mappings"
            )
        source_count += len(sources)
        fact_count += len(facts)
        evidence_inventory.append(
            {
                "ledger_id": ledger_id,
                "source_payload_sha256": {
                    source_id: _canonical_sha256(source)
                    for source_id, source in sorted(sources.items())
                },
                "fact_payload_sha256": {
                    fact_id: _canonical_sha256(fact)
                    for fact_id, fact in sorted(facts.items())
                },
            }
        )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": candidate_id,
        "candidate_provenance_sha256": _sha256_string(
            candidate_provenance_sha256,
            f"candidate provenance for {candidate_id}",
        ),
        "candidate_source_digest_sha256": candidate_source_digest_sha256,
        "validation_compiler_source_ids": compiler_implementation["source_ids"],
        "validation_compiler_source_count": compiler_implementation["source_count"],
        "validation_compiler_implementation_sha256": compiler_implementation[
            "source_sha256"
        ],
        "runtime_output_sha256": runtime_output_sha256,
        "modeled_quality_output_sha256": modeled_quality_output_sha256,
        "generated_artifact_ids": artifact_ids,
        "generated_artifact_count": len(artifact_ids),
        "generated_artifact_inventory_sha256": artifact_inventory_sha256,
        "generated_artifact_state": artifact_state,
        "generated_artifact_set_sha256": artifact_set_sha256,
        "candidate_course_artifact_ids": candidate_course_artifact_ids,
        "candidate_course_artifact_count": len(candidate_course_artifact_ids),
        "candidate_course_artifact_retained_parity": (
            candidate_course_artifact_retained_parity
        ),
        "candidate_course_artifact_mismatch_ids": (
            candidate_course_artifact_mismatch_ids
        ),
        "candidate_course_artifacts_materialized": not (
            candidate_course_artifact_mismatch_ids
        ),
        "evidence_ledger_ids": ledger_ids,
        "evidence_ledger_count": len(ledger_ids),
        "evidence_source_count": source_count,
        "evidence_fact_count": fact_count,
        "evidence_inventory_sha256": _canonical_sha256(evidence_inventory),
    }
    return {**payload, "candidate_current_state_sha256": _canonical_sha256(payload)}


def _retained_evidence_path(value: Any, location: str) -> Path:
    if not isinstance(value, str) or not value:
        raise QualityError(f"{location} must be a non-empty relative path")
    relative = PurePosixPath(value)
    if (
        relative.is_absolute()
        or ".." in relative.parts
        or relative.parts[: len(ACCEPTANCE_EVIDENCE_DIRECTORY.parts)]
        != ACCEPTANCE_EVIDENCE_DIRECTORY.parts
    ):
        raise QualityError(
            f"{location} must remain under {ACCEPTANCE_EVIDENCE_DIRECTORY}"
        )
    return _retained_evidence_root().joinpath(
        *relative.parts[len(ACCEPTANCE_EVIDENCE_DIRECTORY.parts) :]
    )


def _retained_evidence_root() -> Path:
    return ROOT.joinpath(*ACCEPTANCE_EVIDENCE_DIRECTORY.parts)


def _canonical_acceptance_report_path(artifact_sha256: str) -> str:
    digest = _sha256_string(
        artifact_sha256,
        "acceptance report artifact_sha256",
    )
    return f"{ACCEPTANCE_EVIDENCE_DIRECTORY}/reports/{digest}.json"


def _retained_artifact_bytes(value: Any, location: str) -> bytes:
    path = _retained_evidence_path(value, location)
    root = _retained_evidence_root()
    try:
        if root.is_symlink() or path.is_symlink():
            raise QualityError(f"{location} must not be a symbolic link")
        relative_to_root = path.relative_to(root)
        current = root
        for part in relative_to_root.parts[:-1]:
            current /= part
            if current.is_symlink():
                raise QualityError(
                    f"{location} must not traverse a symbolic-link directory"
                )
        if not path.is_file():
            raise QualityError(f"{location} must be a regular file")
        return path.read_bytes()
    except OSError as error:
        raise QualityError(f"{location} is unavailable: {error}") from error


def _retained_artifact_sha256(value: Any, location: str) -> str:
    return hashlib.sha256(_retained_artifact_bytes(value, location)).hexdigest()


def _validate_acceptance_artifacts(value: Any) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        raise QualityError("acceptance_artifacts must be a list")
    expected_fields = {
        "candidate_id",
        "candidate_current_state_sha256",
        "evidence_id",
        "artifact_path",
        "artifact_sha256",
    }
    allowed_evidence_ids = {
        "static:validation",
        "static:deterministic_generation",
        "static:evidence",
        "final:prerequisite_correctness_repairs",
        "final:historical_frozen_champion_viewport_captures",
        "live:browser",
        "live:accessibility_snapshot",
        *(f"blind_review:{reviewer_id}" for reviewer_id in BLIND_REVIEWER_IDS),
    }
    seen: set[tuple[str, str]] = set()
    seen_paths: set[str] = set()
    for index, artifact in enumerate(value):
        location = f"acceptance_artifacts[{index}]"
        if not isinstance(artifact, dict) or set(artifact) != expected_fields:
            raise QualityError(f"{location} fields must be exact")
        candidate_id = artifact["candidate_id"]
        evidence_id = artifact["evidence_id"]
        if (
            candidate_id not in EXPECTED_VARIANTS
            or evidence_id not in allowed_evidence_ids
        ):
            raise QualityError(f"{location} candidate/evidence identity is invalid")
        identity = (candidate_id, evidence_id)
        if identity in seen:
            raise QualityError(f"{location} duplicates a retained evidence identity")
        seen.add(identity)
        _sha256_string(
            artifact["candidate_current_state_sha256"],
            f"{location}.candidate_current_state_sha256",
        )
        declared_sha256 = _sha256_string(
            artifact["artifact_sha256"], f"{location}.artifact_sha256"
        )
        expected_path = _canonical_acceptance_report_path(declared_sha256)
        if artifact["artifact_path"] != expected_path:
            raise QualityError(f"{location}.artifact_path is not canonical")
        if artifact["artifact_path"] in seen_paths:
            raise QualityError(f"{location} duplicates a retained artifact path")
        seen_paths.add(artifact["artifact_path"])
        actual_sha256 = _retained_artifact_sha256(
            artifact["artifact_path"], f"{location}.artifact_path"
        )
        if declared_sha256 != actual_sha256:
            raise QualityError(
                f"{location}.artifact_sha256 does not match retained bytes"
            )
    return value


def _validate_retained_evidence_inventory(
    acceptance_artifacts: Sequence[dict[str, Any]],
    capture_manifest: dict[str, Any],
) -> set[str]:
    acceptance_paths = [
        artifact["artifact_path"] for artifact in acceptance_artifacts
    ]
    capture_paths = [
        capture["artifact_path"] for capture in capture_manifest["captures"]
    ]
    referenced_paths = set(acceptance_paths) | set(capture_paths)
    if len(referenced_paths) != len(acceptance_paths) + len(capture_paths):
        raise QualityError(
            "retained acceptance evidence paths must be globally unique"
        )

    root = _retained_evidence_root()
    actual_paths: set[str] = set()
    if root.exists() or root.is_symlink():
        if root.is_symlink() or not root.is_dir():
            raise QualityError(
                f"{ACCEPTANCE_EVIDENCE_DIRECTORY} must be a regular directory"
            )
        for path in root.rglob("*"):
            relative = path.relative_to(root)
            retained_path = (
                ACCEPTANCE_EVIDENCE_DIRECTORY.joinpath(*relative.parts).as_posix()
            )
            if path.is_symlink():
                raise QualityError(
                    "retained acceptance evidence inventory must not contain "
                    f"symbolic links; path={retained_path!r}"
                )
            if path.is_dir():
                continue
            if not path.is_file():
                raise QualityError(
                    "retained acceptance evidence inventory must contain only "
                    f"regular files; path={retained_path!r}"
                )
            actual_paths.add(retained_path)
    if actual_paths != referenced_paths:
        raise QualityError(
            "retained acceptance evidence inventory must exactly match referenced "
            "artifacts; "
            f"missing={sorted(referenced_paths - actual_paths)} "
            f"extra={sorted(actual_paths - referenced_paths)}"
        )
    return referenced_paths


def _occupancy_capture_identity_sha256(capture: dict[str, Any]) -> str:
    viewport = next(
        viewport for viewport in VIEWPORTS if viewport["id"] == capture["viewport_id"]
    )
    return _canonical_sha256(
        {
            "capture_schema_version": OCCUPANCY_CAPTURE_SCHEMA_VERSION,
            "candidate_id": capture["candidate_id"],
            "candidate_current_state_sha256": capture["candidate_current_state_sha256"],
            "validation_compiler_implementation_sha256": capture[
                "validation_compiler_implementation_sha256"
            ],
            "segment_id": capture["segment_id"],
            "viewport_id": capture["viewport_id"],
            "modeled_evaluation_sha256": capture["modeled_evaluation_sha256"],
            "artifact_sha256": capture["artifact_sha256"],
            "media_type": "image/png",
            "width_px": viewport["width"],
            "height_px": viewport["height"],
        }
    )


def _canonical_occupancy_capture_path(capture: dict[str, Any]) -> str:
    return (
        "course/acceptance_evidence/occupancy/"
        f"{_occupancy_capture_identity_sha256(capture)}.png"
    )


def _validate_occupancy_capture_png(
    payload: bytes,
    *,
    viewport_id: str,
    location: str,
) -> None:
    signature = b"\x89PNG\r\n\x1a\n"
    if not payload.startswith(signature):
        raise QualityError(f"{location} must be a PNG capture")
    viewport = next(viewport for viewport in VIEWPORTS if viewport["id"] == viewport_id)
    offset = len(signature)
    chunk_index = 0
    ihdr: tuple[int, int, int, int, int, int, int] | None = None
    idat = bytearray()
    saw_iend = False
    while offset < len(payload):
        if len(payload) - offset < 12:
            raise QualityError(f"{location} PNG chunk is truncated")
        length = struct.unpack(">I", payload[offset : offset + 4])[0]
        chunk_type = payload[offset + 4 : offset + 8]
        data_start = offset + 8
        data_end = data_start + length
        crc_end = data_end + 4
        if crc_end > len(payload):
            raise QualityError(f"{location} PNG chunk is truncated")
        chunk_data = payload[data_start:data_end]
        declared_crc = struct.unpack(">I", payload[data_end:crc_end])[0]
        actual_crc = zlib.crc32(chunk_type + chunk_data) & 0xFFFFFFFF
        if declared_crc != actual_crc:
            raise QualityError(f"{location} PNG chunk CRC is invalid")
        if chunk_type == b"IHDR":
            if chunk_index != 0 or ihdr is not None or length != 13:
                raise QualityError(f"{location} PNG IHDR is invalid")
            ihdr = struct.unpack(">IIBBBBB", chunk_data)
        elif chunk_type == b"IDAT":
            if ihdr is None or saw_iend:
                raise QualityError(f"{location} PNG IDAT ordering is invalid")
            idat.extend(chunk_data)
        elif chunk_type == b"IEND":
            if length != 0 or ihdr is None or not idat:
                raise QualityError(f"{location} PNG IEND is invalid")
            saw_iend = True
            offset = crc_end
            if offset != len(payload):
                raise QualityError(f"{location} PNG has trailing bytes")
            break
        elif chunk_type[:1].isupper():
            raise QualityError(f"{location} PNG has an unsupported critical chunk")
        offset = crc_end
        chunk_index += 1
    if ihdr is None or not saw_iend:
        raise QualityError(f"{location} PNG structure is incomplete")
    width, height, bit_depth, color_type, compression, filtering, interlace = ihdr
    if (width, height) != (viewport["width"], viewport["height"]):
        raise QualityError(
            f"{location} PNG dimensions must equal viewport {viewport_id}"
        )
    channels_by_color_type = {0: 1, 2: 3, 4: 2, 6: 4}
    if (
        bit_depth != 8
        or color_type not in channels_by_color_type
        or compression != 0
        or filtering != 0
        or interlace != 0
    ):
        raise QualityError(f"{location} PNG encoding is not canonical")
    row_size = width * channels_by_color_type[color_type]
    expected_size = height * (row_size + 1)
    decompressor = zlib.decompressobj()
    try:
        decoded = decompressor.decompress(bytes(idat), expected_size + 1)
    except zlib.error as error:
        raise QualityError(f"{location} PNG image data is invalid") from error
    if decompressor.unconsumed_tail or len(decoded) > expected_size:
        raise QualityError(f"{location} PNG image data exceeds its dimensions")
    try:
        decoded += decompressor.flush()
    except zlib.error as error:
        raise QualityError(f"{location} PNG image data is invalid") from error
    if (
        not decompressor.eof
        or decompressor.unused_data
        or len(decoded) != expected_size
    ):
        raise QualityError(f"{location} PNG image data does not match its dimensions")
    if any(decoded[row * (row_size + 1)] > 4 for row in range(height)):
        raise QualityError(f"{location} PNG row filter is invalid")


def _validate_occupancy_capture_manifest(value: Any) -> dict[str, Any]:
    if (
        not isinstance(value, dict)
        or set(value) != {"schema_version", "captures"}
        or value["schema_version"] != OCCUPANCY_CAPTURE_SCHEMA_VERSION
        or type(value["schema_version"]) is not int
        or not isinstance(value["captures"], list)
    ):
        raise QualityError("occupancy_capture_manifest fields must be exact")
    expected_fields = {
        "candidate_id",
        "candidate_current_state_sha256",
        "validation_compiler_implementation_sha256",
        "segment_id",
        "viewport_id",
        "modeled_evaluation_sha256",
        "artifact_path",
        "artifact_sha256",
    }
    seen: set[tuple[str, str, str]] = set()
    seen_paths: set[str] = set()
    seen_digests: set[str] = set()
    for index, capture in enumerate(value["captures"]):
        location = f"occupancy_capture_manifest.captures[{index}]"
        if not isinstance(capture, dict) or set(capture) != expected_fields:
            raise QualityError(f"{location} fields must be exact")
        candidate_id = capture["candidate_id"]
        segment_id = capture["segment_id"]
        viewport_id = capture["viewport_id"]
        identity = (candidate_id, segment_id, viewport_id)
        if (
            candidate_id not in EXPECTED_VARIANTS
            or not isinstance(segment_id, str)
            or not segment_id
            or viewport_id not in {viewport["id"] for viewport in VIEWPORTS}
        ):
            raise QualityError(f"{location} candidate/evaluation identity is invalid")
        if identity in seen:
            raise QualityError(f"{location} duplicates a capture identity")
        seen.add(identity)
        for field in (
            "candidate_current_state_sha256",
            "validation_compiler_implementation_sha256",
            "modeled_evaluation_sha256",
            "artifact_sha256",
        ):
            _sha256_string(capture[field], f"{location}.{field}")
        expected_path = _canonical_occupancy_capture_path(capture)
        if capture["artifact_path"] != expected_path:
            raise QualityError(f"{location}.artifact_path is not canonical")
        if capture["artifact_path"] in seen_paths:
            raise QualityError(f"{location} duplicates a capture artifact path")
        if capture["artifact_sha256"] in seen_digests:
            raise QualityError(f"{location} duplicates capture artifact bytes")
        seen_paths.add(capture["artifact_path"])
        seen_digests.add(capture["artifact_sha256"])
        payload = _retained_artifact_bytes(
            capture["artifact_path"], f"{location}.artifact_path"
        )
        actual_sha256 = hashlib.sha256(payload).hexdigest()
        if capture["artifact_sha256"] != actual_sha256:
            raise QualityError(
                f"{location}.artifact_sha256 does not match retained bytes"
            )
        _validate_occupancy_capture_png(
            payload,
            viewport_id=viewport_id,
            location=f"{location}.artifact_path",
        )
    return value


def _require_retained_acceptance_artifact(
    artifacts: Sequence[dict[str, Any]],
    *,
    candidate_id: str,
    candidate_current_state_sha256: str,
    evidence_id: str,
    artifact_sha256: str,
    typed_evidence: dict[str, Any],
    artifact_digest_field: str,
    outcome: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> None:
    matches = [
        artifact
        for artifact in artifacts
        if artifact["candidate_id"] == candidate_id
        and artifact["evidence_id"] == evidence_id
    ]
    if len(matches) != 1:
        raise QualityError(
            f"{location} requires exactly one retained artifact for {evidence_id!r}"
        )
    artifact = matches[0]
    if artifact["candidate_current_state_sha256"] != candidate_current_state_sha256:
        raise QualityError(
            f"{location} retained artifact current-state binding is stale"
        )
    if (
        expected_current_state is not None
        and artifact["candidate_current_state_sha256"]
        != expected_current_state["candidate_current_state_sha256"]
    ):
        raise QualityError(
            f"{location} retained artifact does not match current compiler state"
        )
    if artifact["artifact_sha256"] != artifact_sha256:
        raise QualityError(
            f"{location} evidence digest does not match retained artifact"
        )
    actual_sha256 = _retained_artifact_sha256(
        artifact["artifact_path"], f"{location}.retained_artifact_path"
    )
    if actual_sha256 != artifact_sha256:
        raise QualityError(f"{location} retained artifact bytes are stale")
    report_evidence = copy.deepcopy(typed_evidence)
    if report_evidence.pop(artifact_digest_field, None) != artifact_sha256:
        raise QualityError(f"{location} report digest field is invalid")
    expected_envelope = {
        "schema_version": SCHEMA_VERSION,
        "candidate_id": candidate_id,
        "candidate_current_state_sha256": candidate_current_state_sha256,
        "evidence_id": evidence_id,
        "outcome": outcome,
        "typed_evidence": report_evidence,
    }
    report_path = _retained_evidence_path(
        artifact["artifact_path"], f"{location}.retained_artifact_path"
    )
    try:
        report_bytes = report_path.read_bytes()
        report = json.loads(report_bytes)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise QualityError(
            f"{location} retained report is not valid JSON: {error}"
        ) from error
    if not _matches_exact_contract_value(report, expected_envelope):
        raise QualityError(f"{location} retained report envelope is stale or misbound")
    canonical_report = (
        scene_pipeline.canonical_payload(expected_envelope) + "\n"
    ).encode()
    if report_bytes != canonical_report:
        raise QualityError(f"{location} retained report bytes are not canonical")


def _acceptance_evidence_ref(
    candidate_id: str,
    provenance_sha256: str,
    domain: str,
    evidence_id: str,
    evidence: dict[str, Any],
) -> str:
    """Return a content-addressed ref bound to candidate, provenance, and domain."""

    evidence_sha256 = hashlib.sha256(
        scene_pipeline.canonical_payload(evidence).encode()
    ).hexdigest()
    return (
        f"{ACCEPTANCE_EVIDENCE_SCHEME}://{candidate_id}/"
        f"{provenance_sha256}/{domain}/{evidence_id}/{evidence_sha256}"
    )


def _acceptance_evidence_common(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    expected_fields: set[str],
    location: str,
) -> dict[str, Any]:
    common_fields = {
        "candidate_id",
        "candidate_provenance_sha256",
        "candidate_current_state_sha256",
        "validation_compiler_implementation_sha256",
    }
    if (
        not isinstance(evidence, dict)
        or set(evidence) != expected_fields | common_fields
    ):
        actual_fields = set(evidence) if isinstance(evidence, dict) else set()
        raise QualityError(
            f"{location} evidence fields must be exact; "
            f"missing={sorted(expected_fields | common_fields - actual_fields)} "
            f"unknown={sorted(actual_fields - (expected_fields | common_fields))}"
        )
    if evidence["candidate_id"] != candidate_id:
        raise QualityError(f"{location} evidence candidate binding is invalid")
    if evidence["candidate_provenance_sha256"] != provenance_sha256:
        raise QualityError(f"{location} evidence provenance is stale")
    current_state_sha256 = _sha256_string(
        evidence["candidate_current_state_sha256"],
        f"{location}.candidate_current_state_sha256",
    )
    implementation_sha256 = _sha256_string(
        evidence["validation_compiler_implementation_sha256"],
        f"{location}.validation_compiler_implementation_sha256",
    )
    if (
        expected_current_state is not None
        and current_state_sha256
        != expected_current_state["candidate_current_state_sha256"]
    ):
        raise QualityError(f"{location} evidence current-state provenance is stale")
    if (
        expected_current_state is not None
        and implementation_sha256
        != expected_current_state["validation_compiler_implementation_sha256"]
    ):
        raise QualityError(f"{location} evidence compiler implementation is stale")
    return evidence


def _validate_gate_record(
    value: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    domain: str,
    evidence_id: str,
    evidence_validator: Any,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> dict[str, Any]:
    expected_fields = {"status", "evidence_ref", "evidence", "reason"}
    if not isinstance(value, dict) or set(value) != expected_fields:
        raise QualityError(f"{location} fields must be exact")
    status = value["status"]
    if not isinstance(status, str) or status not in FINAL_ACCEPTANCE_GATE_STATUSES:
        raise QualityError(f"{location}.status is invalid")
    reason = value["reason"]
    if not isinstance(reason, str) or not reason.strip():
        raise QualityError(f"{location}.reason must be a non-empty string")
    evidence_ref = value["evidence_ref"]
    evidence = value["evidence"]
    if status == "pending":
        if evidence_ref is not None or evidence is not None:
            raise QualityError(
                f"{location} pending status requires null evidence and evidence_ref"
            )
        return value
    if not isinstance(evidence, dict):
        raise QualityError(f"{location} resolved status requires typed evidence")
    derived_status = evidence_validator(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        location=f"{location}.evidence",
    )
    if status != derived_status:
        raise QualityError(f"{location}.status must match its typed evidence outcome")
    expected_ref = _acceptance_evidence_ref(
        candidate_id,
        provenance_sha256,
        domain,
        evidence_id,
        evidence,
    )
    if evidence_ref != expected_ref:
        raise QualityError(f"{location}.evidence_ref is malformed, stale, or misbound")
    return value


def _validate_validation_evidence(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> str:
    evidence = _acceptance_evidence_common(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        expected_fields={
            "command",
            "exit_code",
            "source_digest_sha256",
            "runtime_output_sha256",
            "modeled_quality_output_sha256",
            "report_artifact_sha256",
        },
        location=location,
    )
    if evidence["command"] != "uv run gigawatt-validate":
        raise QualityError(f"{location}.command is not canonical")
    exit_code = _integer_at_least(evidence["exit_code"], 0, f"{location}.exit_code")
    exact_fields = {
        "source_digest_sha256": "candidate_source_digest_sha256",
        "runtime_output_sha256": "runtime_output_sha256",
        "modeled_quality_output_sha256": "modeled_quality_output_sha256",
    }
    for field, state_field in exact_fields.items():
        value = _sha256_string(evidence[field], f"{location}.{field}")
        if (
            expected_current_state is not None
            and value != expected_current_state[state_field]
        ):
            raise QualityError(
                f"{location}.{field} does not match current compiler state"
            )
    _sha256_string(
        evidence["report_artifact_sha256"],
        f"{location}.report_artifact_sha256",
    )
    return "passed" if exit_code == 0 else "failed"


def _validate_deterministic_generation_evidence(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> str:
    evidence = _acceptance_evidence_common(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        expected_fields={
            "command",
            "seeds",
            "artifact_count",
            "artifact_ids",
            "mismatch_count",
            "artifact_inventory_sha256",
            "artifact_set_sha256",
            "report_artifact_sha256",
        },
        location=location,
    )
    if evidence["command"] != "uv run gigawatt-quality":
        raise QualityError(f"{location}.command is not canonical")
    if not _matches_exact_contract_value(
        evidence["seeds"], list(ACCEPTANCE_GENERATION_SEEDS)
    ):
        raise QualityError(f"{location}.seeds must be the canonical generation seeds")
    artifact_count = _integer_at_least(
        evidence["artifact_count"], 1, f"{location}.artifact_count"
    )
    if not _unique_nonempty_strings(evidence["artifact_ids"]):
        raise QualityError(f"{location}.artifact_ids must be unique non-empty strings")
    mismatch_count = _integer_at_least(
        evidence["mismatch_count"], 0, f"{location}.mismatch_count"
    )
    if mismatch_count > artifact_count:
        raise QualityError(f"{location}.mismatch_count exceeds artifact_count")
    inventory_sha256 = _sha256_string(
        evidence["artifact_inventory_sha256"],
        f"{location}.artifact_inventory_sha256",
    )
    artifact_set_sha256 = _sha256_string(
        evidence["artifact_set_sha256"], f"{location}.artifact_set_sha256"
    )
    _sha256_string(
        evidence["report_artifact_sha256"],
        f"{location}.report_artifact_sha256",
    )
    if expected_current_state is not None:
        expected_artifact_ids = expected_current_state["generated_artifact_ids"]
        if evidence["artifact_ids"] != expected_artifact_ids:
            raise QualityError(
                f"{location}.artifact_ids do not match current inventory"
            )
        if artifact_count != expected_current_state["generated_artifact_count"]:
            raise QualityError(
                f"{location}.artifact_count does not match current inventory"
            )
        if (
            inventory_sha256
            != expected_current_state["generated_artifact_inventory_sha256"]
        ):
            raise QualityError(
                f"{location}.artifact_inventory_sha256 does not match current inventory"
            )
        if (
            artifact_set_sha256
            != expected_current_state["generated_artifact_set_sha256"]
        ):
            raise QualityError(f"{location}.artifact_set_sha256 is stale")
    return "passed" if mismatch_count == 0 else "failed"


def _validate_evidence_gate_evidence(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> str:
    evidence = _acceptance_evidence_common(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        expected_fields={
            "ledger_ids",
            "ledger_count",
            "source_count",
            "fact_count",
            "validation_error_count",
            "evidence_inventory_sha256",
            "report_artifact_sha256",
        },
        location=location,
    )
    if not _unique_nonempty_strings(evidence["ledger_ids"]):
        raise QualityError(f"{location}.ledger_ids must be unique non-empty strings")
    ledger_count = _integer_at_least(
        evidence["ledger_count"], 1, f"{location}.ledger_count"
    )
    source_count = _integer_at_least(
        evidence["source_count"], 1, f"{location}.source_count"
    )
    fact_count = _integer_at_least(evidence["fact_count"], 1, f"{location}.fact_count")
    error_count = _integer_at_least(
        evidence["validation_error_count"],
        0,
        f"{location}.validation_error_count",
    )
    inventory_sha256 = _sha256_string(
        evidence["evidence_inventory_sha256"],
        f"{location}.evidence_inventory_sha256",
    )
    _sha256_string(
        evidence["report_artifact_sha256"],
        f"{location}.report_artifact_sha256",
    )
    if expected_current_state is not None:
        exact_values = {
            "ledger_ids": expected_current_state["evidence_ledger_ids"],
            "ledger_count": expected_current_state["evidence_ledger_count"],
            "source_count": expected_current_state["evidence_source_count"],
            "fact_count": expected_current_state["evidence_fact_count"],
            "evidence_inventory_sha256": expected_current_state[
                "evidence_inventory_sha256"
            ],
        }
        actual_values = {
            "ledger_ids": evidence["ledger_ids"],
            "ledger_count": ledger_count,
            "source_count": source_count,
            "fact_count": fact_count,
            "evidence_inventory_sha256": inventory_sha256,
        }
        for field, expected in exact_values.items():
            if not _matches_exact_contract_value(actual_values[field], expected):
                raise QualityError(
                    f"{location}.{field} does not match current evidence inventory"
                )
    return "passed" if error_count == 0 else "failed"


def _validate_browser_evidence(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> str:
    evidence = _acceptance_evidence_common(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        expected_fields={
            "viewport_ids",
            "segment_count",
            "evaluation_count",
            "defect_count",
            "artifact_sha256",
            "report_artifact_sha256",
        },
        location=location,
    )
    if not _matches_exact_contract_value(
        evidence["viewport_ids"], [viewport["id"] for viewport in VIEWPORTS]
    ):
        raise QualityError(f"{location}.viewport_ids must be exact and ordered")
    if (
        _integer_at_least(evidence["segment_count"], 0, f"{location}.segment_count")
        != course_runtime.EXPECTED_SEGMENTS
    ):
        raise QualityError(f"{location}.segment_count is incomplete")
    if _integer_at_least(
        evidence["evaluation_count"], 0, f"{location}.evaluation_count"
    ) != course_runtime.EXPECTED_SEGMENTS * len(VIEWPORTS):
        raise QualityError(f"{location}.evaluation_count is incomplete")
    defect_count = _integer_at_least(
        evidence["defect_count"], 0, f"{location}.defect_count"
    )
    _sha256_string(evidence["artifact_sha256"], f"{location}.artifact_sha256")
    _sha256_string(
        evidence["report_artifact_sha256"],
        f"{location}.report_artifact_sha256",
    )
    return "passed" if defect_count == 0 else "failed"


def _validate_accessibility_evidence(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> str:
    evidence = _acceptance_evidence_common(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        expected_fields={
            "viewport_ids",
            "segment_count",
            "snapshot_count",
            "violation_count",
            "artifact_sha256",
            "report_artifact_sha256",
        },
        location=location,
    )
    if not _matches_exact_contract_value(
        evidence["viewport_ids"], [viewport["id"] for viewport in VIEWPORTS]
    ):
        raise QualityError(f"{location}.viewport_ids must be exact and ordered")
    if (
        _integer_at_least(evidence["segment_count"], 0, f"{location}.segment_count")
        != course_runtime.EXPECTED_SEGMENTS
    ):
        raise QualityError(f"{location}.segment_count is incomplete")
    if _integer_at_least(
        evidence["snapshot_count"], 0, f"{location}.snapshot_count"
    ) != course_runtime.EXPECTED_SEGMENTS * len(VIEWPORTS):
        raise QualityError(f"{location}.snapshot_count is incomplete")
    violation_count = _integer_at_least(
        evidence["violation_count"], 0, f"{location}.violation_count"
    )
    _sha256_string(evidence["artifact_sha256"], f"{location}.artifact_sha256")
    _sha256_string(
        evidence["report_artifact_sha256"],
        f"{location}.report_artifact_sha256",
    )
    return "passed" if violation_count == 0 else "failed"


def _validate_prerequisite_evidence(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> str:
    evidence = _acceptance_evidence_common(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        expected_fields={
            "repair_scope_ids",
            "unresolved_repair_count",
            "candidate_base_source_digest_sha256",
            "artifact_sha256",
            "report_artifact_sha256",
        },
        location=location,
    )
    if not _matches_exact_contract_value(
        evidence["repair_scope_ids"], EXPECTED_PREREQUISITE_REPAIRS["scopes"]
    ):
        raise QualityError(f"{location}.repair_scope_ids must be exact and ordered")
    unresolved = _integer_at_least(
        evidence["unresolved_repair_count"],
        0,
        f"{location}.unresolved_repair_count",
    )
    if unresolved > len(EXPECTED_PREREQUISITE_REPAIRS["scopes"]):
        raise QualityError(
            f"{location}.unresolved_repair_count exceeds the declared scope"
        )
    base_source_sha256 = _sha256_string(
        evidence["candidate_base_source_digest_sha256"],
        f"{location}.candidate_base_source_digest_sha256",
    )
    _sha256_string(evidence["artifact_sha256"], f"{location}.artifact_sha256")
    _sha256_string(
        evidence["report_artifact_sha256"],
        f"{location}.report_artifact_sha256",
    )
    if (
        expected_current_state is not None
        and base_source_sha256
        != expected_current_state["candidate_source_digest_sha256"]
    ):
        raise QualityError(f"{location}.candidate_base_source_digest_sha256 is stale")
    return "passed" if unresolved == 0 else "failed"


def _validate_historical_capture_evidence(
    evidence: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> str:
    evidence = _acceptance_evidence_common(
        evidence,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        expected_fields={
            "viewport_ids",
            "expected_capture_count",
            "reviewed_capture_count",
            "capture_set_sha256",
            "report_artifact_sha256",
        },
        location=location,
    )
    if not _matches_exact_contract_value(
        evidence["viewport_ids"], [viewport["id"] for viewport in VIEWPORTS]
    ):
        raise QualityError(f"{location}.viewport_ids must be exact and ordered")
    required_count = course_runtime.EXPECTED_SEGMENTS * len(VIEWPORTS)
    if (
        _integer_at_least(
            evidence["expected_capture_count"],
            0,
            f"{location}.expected_capture_count",
        )
        != required_count
    ):
        raise QualityError(f"{location}.expected_capture_count is not canonical")
    reviewed_count = _integer_at_least(
        evidence["reviewed_capture_count"],
        0,
        f"{location}.reviewed_capture_count",
    )
    if reviewed_count > required_count:
        raise QualityError(f"{location}.reviewed_capture_count is out of range")
    _sha256_string(evidence["capture_set_sha256"], f"{location}.capture_set_sha256")
    _sha256_string(
        evidence["report_artifact_sha256"],
        f"{location}.report_artifact_sha256",
    )
    return "passed" if reviewed_count == required_count else "failed"


def _validate_blind_reviews(
    value: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None,
    location: str,
) -> list[dict[str, Any]]:
    if not isinstance(value, list) or len(value) != len(BLIND_REVIEWER_IDS):
        raise QualityError(f"{location} must contain exactly three reviews")
    actual_reviewer_ids = []
    for index, review in enumerate(value):
        item_location = f"{location}[{index}]"
        expected_fields = {
            "reviewer_id",
            "blind",
            "preference",
            "evidence_ref",
            "evidence",
            "reason",
        }
        if not isinstance(review, dict) or set(review) != expected_fields:
            raise QualityError(f"{item_location} fields must be exact")
        reviewer_id = review["reviewer_id"]
        actual_reviewer_ids.append(reviewer_id)
        if review["blind"] is not True:
            raise QualityError(f"{item_location}.blind must be true")
        preference = review["preference"]
        if (
            not isinstance(preference, str)
            or preference not in ratchet.REVIEW_PREFERENCES
        ):
            raise QualityError(f"{item_location}.preference is invalid")
        reason = review["reason"]
        if not isinstance(reason, str) or not reason.strip():
            raise QualityError(f"{item_location}.reason must be a non-empty string")
        evidence_ref = review["evidence_ref"]
        evidence = review["evidence"]
        if preference == "pending":
            if evidence_ref is not None or evidence is not None:
                raise QualityError(
                    f"{item_location} pending preference requires null evidence and evidence_ref"
                )
            continue
        evidence = _acceptance_evidence_common(
            evidence,
            candidate_id=candidate_id,
            provenance_sha256=provenance_sha256,
            expected_current_state=expected_current_state,
            expected_fields={
                "reviewer_id",
                "blind",
                "preference",
                "comparison_artifact_sha256",
                "report_artifact_sha256",
            },
            location=f"{item_location}.evidence",
        )
        if (
            evidence["reviewer_id"] != reviewer_id
            or evidence["blind"] is not True
            or evidence["preference"] != preference
        ):
            raise QualityError(
                f"{item_location} fields must match its typed reviewer evidence"
            )
        _sha256_string(
            evidence["comparison_artifact_sha256"],
            f"{item_location}.evidence.comparison_artifact_sha256",
        )
        _sha256_string(
            evidence["report_artifact_sha256"],
            f"{item_location}.evidence.report_artifact_sha256",
        )
        expected_ref = _acceptance_evidence_ref(
            candidate_id,
            provenance_sha256,
            "blind_review",
            reviewer_id,
            evidence,
        )
        if evidence_ref != expected_ref:
            raise QualityError(
                f"{item_location}.evidence_ref is malformed, stale, or misbound"
            )
    if actual_reviewer_ids != list(BLIND_REVIEWER_IDS):
        raise QualityError(f"{location} reviewer IDs must be exact and ordered")
    return value


def _validate_candidate_acceptance_evidence(
    value: Any,
    *,
    candidate_id: str,
    provenance_sha256: str,
    expected_current_state: dict[str, Any] | None = None,
    acceptance_artifacts: Sequence[dict[str, Any]] = (),
    location: str,
) -> dict[str, Any]:
    expected_fields = {
        "candidate_id",
        "candidate_provenance_sha256",
        "static_gate_evidence",
        "live_gate_evidence",
        "blind_reviews",
        "final_independent_gate_evidence",
    }
    if not isinstance(value, dict) or set(value) != expected_fields:
        raise QualityError(f"{location} fields must be exact")
    if value["candidate_id"] != candidate_id:
        raise QualityError(f"{location}.candidate_id does not match its registry entry")
    if value["candidate_provenance_sha256"] != provenance_sha256:
        raise QualityError(f"{location}.candidate_provenance_sha256 is stale")

    static_gates = value["static_gate_evidence"]
    if not isinstance(static_gates, dict) or set(static_gates) != set(
        ratchet.STATIC_GATE_IDS
    ):
        raise QualityError(
            f"{location}.static_gate_evidence must be complete and exact"
        )
    static_validators = {
        "validation": _validate_validation_evidence,
        "deterministic_generation": _validate_deterministic_generation_evidence,
        "evidence": _validate_evidence_gate_evidence,
    }
    for gate_id in ratchet.STATIC_GATE_IDS:
        _validate_gate_record(
            static_gates[gate_id],
            candidate_id=candidate_id,
            provenance_sha256=provenance_sha256,
            domain="static",
            evidence_id=gate_id,
            evidence_validator=static_validators[gate_id],
            expected_current_state=expected_current_state,
            location=f"{location}.static_gate_evidence.{gate_id}",
        )
        gate = static_gates[gate_id]
        if gate["status"] != "pending":
            evidence = gate["evidence"]
            _require_retained_acceptance_artifact(
                acceptance_artifacts,
                candidate_id=candidate_id,
                candidate_current_state_sha256=evidence[
                    "candidate_current_state_sha256"
                ],
                evidence_id=f"static:{gate_id}",
                artifact_sha256=evidence["report_artifact_sha256"],
                typed_evidence=evidence,
                artifact_digest_field="report_artifact_sha256",
                outcome=gate["status"],
                expected_current_state=expected_current_state,
                location=f"{location}.static_gate_evidence.{gate_id}",
            )

    live_gates = value["live_gate_evidence"]
    if not isinstance(live_gates, dict) or set(live_gates) != set(
        ratchet.LIVE_GATE_IDS
    ):
        raise QualityError(f"{location}.live_gate_evidence must be complete and exact")
    live_validators = {
        "browser": _validate_browser_evidence,
        "accessibility_snapshot": _validate_accessibility_evidence,
    }
    for gate_id in ratchet.LIVE_GATE_IDS:
        _validate_gate_record(
            live_gates[gate_id],
            candidate_id=candidate_id,
            provenance_sha256=provenance_sha256,
            domain="live",
            evidence_id=gate_id,
            evidence_validator=live_validators[gate_id],
            expected_current_state=expected_current_state,
            location=f"{location}.live_gate_evidence.{gate_id}",
        )
        gate = live_gates[gate_id]
        if gate["status"] != "pending":
            evidence = gate["evidence"]
            _require_retained_acceptance_artifact(
                acceptance_artifacts,
                candidate_id=candidate_id,
                candidate_current_state_sha256=evidence[
                    "candidate_current_state_sha256"
                ],
                evidence_id=f"live:{gate_id}",
                artifact_sha256=evidence["report_artifact_sha256"],
                typed_evidence=evidence,
                artifact_digest_field="report_artifact_sha256",
                outcome=gate["status"],
                expected_current_state=expected_current_state,
                location=f"{location}.live_gate_evidence.{gate_id}",
            )

    _validate_blind_reviews(
        value["blind_reviews"],
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        location=f"{location}.blind_reviews",
    )
    for index, review in enumerate(value["blind_reviews"]):
        if review["preference"] == "pending":
            continue
        evidence = review["evidence"]
        _require_retained_acceptance_artifact(
            acceptance_artifacts,
            candidate_id=candidate_id,
            candidate_current_state_sha256=evidence["candidate_current_state_sha256"],
            evidence_id=f"blind_review:{review['reviewer_id']}",
            artifact_sha256=evidence["report_artifact_sha256"],
            typed_evidence=evidence,
            artifact_digest_field="report_artifact_sha256",
            outcome=review["preference"],
            expected_current_state=expected_current_state,
            location=f"{location}.blind_reviews[{index}]",
        )

    independent_gates = value["final_independent_gate_evidence"]
    if not isinstance(independent_gates, dict) or set(independent_gates) != set(
        ACCEPTANCE_INDEPENDENT_GATE_IDS
    ):
        raise QualityError(
            f"{location}.final_independent_gate_evidence must be complete and exact"
        )
    independent_validators = {
        "prerequisite_correctness_repairs": _validate_prerequisite_evidence,
        "historical_frozen_champion_viewport_captures": (
            _validate_historical_capture_evidence
        ),
    }
    for gate_id in ACCEPTANCE_INDEPENDENT_GATE_IDS:
        _validate_gate_record(
            independent_gates[gate_id],
            candidate_id=candidate_id,
            provenance_sha256=provenance_sha256,
            domain="final",
            evidence_id=gate_id,
            evidence_validator=independent_validators[gate_id],
            expected_current_state=expected_current_state,
            location=(f"{location}.final_independent_gate_evidence.{gate_id}"),
        )
        gate = independent_gates[gate_id]
        if gate["status"] != "pending":
            evidence = gate["evidence"]
            _require_retained_acceptance_artifact(
                acceptance_artifacts,
                candidate_id=candidate_id,
                candidate_current_state_sha256=evidence[
                    "candidate_current_state_sha256"
                ],
                evidence_id=f"final:{gate_id}",
                artifact_sha256=evidence["report_artifact_sha256"],
                typed_evidence=evidence,
                artifact_digest_field="report_artifact_sha256",
                outcome=gate["status"],
                expected_current_state=expected_current_state,
                location=(f"{location}.final_independent_gate_evidence.{gate_id}"),
            )
    return value


def _required_acceptance_artifact_identities(
    acceptance_candidates: Sequence[dict[str, Any]],
) -> set[tuple[str, str]]:
    required: set[tuple[str, str]] = set()
    for candidate in acceptance_candidates:
        candidate_id = candidate["candidate_id"]
        for domain, gates in (
            ("static", candidate["static_gate_evidence"]),
            ("live", candidate["live_gate_evidence"]),
            ("final", candidate["final_independent_gate_evidence"]),
        ):
            required.update(
                (candidate_id, f"{domain}:{gate_id}")
                for gate_id, gate in gates.items()
                if gate["status"] != "pending"
            )
        required.update(
            (candidate_id, f"blind_review:{review['reviewer_id']}")
            for review in candidate["blind_reviews"]
            if review["preference"] != "pending"
        )
    return required


def _validate_acceptance_artifact_consumption(
    acceptance_candidates: Sequence[dict[str, Any]],
    acceptance_artifacts: Sequence[dict[str, Any]],
) -> None:
    required_artifact_identities = _required_acceptance_artifact_identities(
        acceptance_candidates
    )
    actual_artifact_identities = {
        (artifact["candidate_id"], artifact["evidence_id"])
        for artifact in acceptance_artifacts
    }
    if actual_artifact_identities != required_artifact_identities:
        raise QualityError(
            "acceptance_artifacts identities must exactly match resolved evidence; "
            f"missing={sorted(required_artifact_identities - actual_artifact_identities)} "
            f"extra={sorted(actual_artifact_identities - required_artifact_identities)}"
        )


def load_ratchet_manifest() -> dict[str, Any]:
    manifest = scene_pipeline.load_yaml(RATCHET_PATH)
    required_fields = {
        "schema_version",
        "hard_constraints",
        "frozen_champion",
        "experiment_control",
        "hypothesis_id",
        "hypothesis",
        "prerequisite_repairs",
        "variants",
        "change_owners",
        "finding_owners",
        "changes",
        "challenger_changes",
        "acceptance_artifacts",
        "occupancy_capture_manifest",
        "occupancy_reviews",
        "acceptance",
    }
    actual_fields = set(manifest or {})
    if (
        not isinstance(manifest, dict)
        or not required_fields <= actual_fields
        or actual_fields - required_fields
    ):
        raise QualityError(
            "course quality ratchet fields must be exact; "
            f"missing={sorted(required_fields - actual_fields)} "
            f"unknown={sorted(actual_fields - required_fields)}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise QualityError("course quality ratchet schema_version must be 1")
    if not _matches_exact_contract_value(
        manifest["frozen_champion"], EXPECTED_CHAMPION
    ):
        raise QualityError("course quality ratchet changed the frozen champion")
    if not _matches_exact_contract_value(
        manifest["experiment_control"], EXPECTED_EXPERIMENT_CONTROL
    ):
        raise QualityError(
            "course quality ratchet must identify the synthetic experiment control"
        )
    if manifest["hypothesis_id"] != "HYP-FOCUS-OVERLAY-01":
        raise QualityError("course quality ratchet hypothesis_id is not canonical")
    if manifest["hypothesis"] != RATCHET_HYPOTHESIS:
        raise QualityError("course quality ratchet hypothesis changed")
    if not _matches_exact_contract_value(
        manifest["prerequisite_repairs"], EXPECTED_PREREQUISITE_REPAIRS
    ):
        raise QualityError("course quality ratchet prerequisite repairs changed")
    if not _matches_exact_contract_value(manifest["variants"], EXPECTED_VARIANTS):
        raise QualityError("course quality ratchet isolated variants changed")
    hard_constraints = manifest["hard_constraints"]
    if not _matches_exact_contract_value(hard_constraints, EXPECTED_HARD_CONSTRAINTS):
        raise QualityError(
            "course quality ratchet hard_constraints must exactly preserve the "
            "evidence, unknown, motion, accessibility, determinism, and render gates"
        )

    acceptance_artifacts = _validate_acceptance_artifacts(
        manifest["acceptance_artifacts"]
    )
    occupancy_capture_manifest = _validate_occupancy_capture_manifest(
        manifest["occupancy_capture_manifest"]
    )
    retained_evidence_paths = _validate_retained_evidence_inventory(
        acceptance_artifacts,
        occupancy_capture_manifest,
    )

    change_owners = manifest["change_owners"]
    if not isinstance(change_owners, list) or not change_owners:
        raise QualityError("course quality ratchet change_owners must be non-empty")
    owner_ids: set[str] = set()
    owner_source_paths: dict[str, set[str]] = {}
    for index, owner in enumerate(change_owners):
        if not isinstance(owner, dict) or set(owner) != {
            "change_owner_id",
            "source_paths",
            "responsibilities",
        }:
            raise QualityError(f"change_owners[{index}] fields must be exact")
        owner_id = owner["change_owner_id"]
        if not isinstance(owner_id, str) or not owner_id or owner_id in owner_ids:
            raise QualityError(f"change_owners[{index}] has an invalid or duplicate ID")
        owner_ids.add(owner_id)
        for field in ("source_paths", "responsibilities"):
            values = owner[field]
            if not _unique_nonempty_strings(values):
                raise QualityError(
                    f"change_owners[{index}].{field} must be unique non-empty strings"
                )
        source_paths = owner["source_paths"]
        generated_html_paths = sorted(
            path for path in source_paths if Path(path).suffix.lower() == ".html"
        )
        if generated_html_paths:
            raise QualityError(
                f"change_owners[{index}].source_paths must not own generated HTML; "
                f"paths={generated_html_paths}"
            )
        owner_source_paths[owner_id] = set(source_paths)

    finding_owners = manifest["finding_owners"]
    if not isinstance(finding_owners, dict) or not finding_owners:
        raise QualityError("course quality ratchet finding_owners must be non-empty")
    for finding_id, finding_owner_ids in finding_owners.items():
        if (
            not isinstance(finding_id, str)
            or not finding_id
            or not _unique_nonempty_strings(finding_owner_ids)
            or not set(finding_owner_ids) <= owner_ids
        ):
            raise QualityError(f"finding_owners[{finding_id!r}] is invalid")

    changes = manifest["changes"]
    if not isinstance(changes, list) or not changes:
        raise QualityError("course quality ratchet changes must be non-empty")
    changes_by_id: dict[str, dict[str, Any]] = {}
    finding_change_counts: Counter[str] = Counter()
    for index, change in enumerate(changes):
        if not isinstance(change, dict) or set(change) != {
            "change_id",
            "finding_ids",
            "change_owner_ids",
            "source_paths",
            "description",
        }:
            raise QualityError(f"changes[{index}] fields must be exact")
        change_id = change["change_id"]
        if (
            not isinstance(change_id, str)
            or not change_id
            or change_id in changes_by_id
        ):
            raise QualityError(f"changes[{index}] has an invalid or duplicate ID")
        finding_ids = change["finding_ids"]
        change_owner_ids = change["change_owner_ids"]
        source_paths = change["source_paths"]
        if (
            not _unique_nonempty_strings(finding_ids)
            or not set(finding_ids) <= set(finding_owners)
            or not _unique_nonempty_strings(change_owner_ids)
            or not set(change_owner_ids) <= owner_ids
            or not _unique_nonempty_strings(source_paths)
            or not isinstance(change["description"], str)
            or not change["description"]
        ):
            raise QualityError(f"changes[{index}] has unresolved ownership links")
        generated_html_paths = sorted(
            path for path in source_paths if Path(path).suffix.lower() == ".html"
        )
        if generated_html_paths:
            raise QualityError(
                f"changes[{index}].source_paths must not include generated HTML; "
                f"paths={generated_html_paths}"
            )
        expected_owner_ids = {
            owner_id
            for finding_id in finding_ids
            for owner_id in finding_owners[finding_id]
        }
        if set(change_owner_ids) != expected_owner_ids:
            raise QualityError(
                f"changes[{index}] change_owner_ids must exactly match finding owners; "
                f"missing={sorted(expected_owner_ids - set(change_owner_ids))} "
                f"extra={sorted(set(change_owner_ids) - expected_owner_ids)}"
            )
        linked_owner_paths = set().union(
            *(owner_source_paths[owner_id] for owner_id in change_owner_ids)
        )
        incompatible_paths = sorted(set(source_paths) - linked_owner_paths)
        owners_without_change_paths = sorted(
            owner_id
            for owner_id in change_owner_ids
            if set(source_paths).isdisjoint(owner_source_paths[owner_id])
        )
        if incompatible_paths or owners_without_change_paths:
            raise QualityError(
                f"changes[{index}] source paths must be compatible with linked owners; "
                f"incompatible_paths={incompatible_paths} "
                f"owners_without_change_paths={owners_without_change_paths}"
            )
        finding_change_counts.update(finding_ids)
        changes_by_id[change_id] = change
    missing_change_findings = sorted(set(finding_owners) - set(finding_change_counts))
    multiply_linked_findings = sorted(
        finding_id for finding_id, count in finding_change_counts.items() if count != 1
    )
    if missing_change_findings or multiply_linked_findings:
        raise QualityError(
            "finding/change links must be exact and one-to-one; "
            f"missing={missing_change_findings} "
            f"multiply_linked={multiply_linked_findings}"
        )

    declared_source_paths = {
        source_path
        for change in changes_by_id.values()
        for source_path in change["source_paths"]
    }
    try:
        changed_paths = set(
            champion_pipeline.changed_worktree_paths(
                ROOT,
                manifest["frozen_champion"]["git_sha"],
            )
        )
    except champion_pipeline.ChampionVerificationError as error:
        raise QualityError(
            "course quality ratchet could not compare the current worktree to "
            "the frozen champion"
        ) from error
    changed_source_paths = (
        changed_paths - GENERATED_OUTPUT_PATH_ALLOWLIST - retained_evidence_paths
    )
    undeclared_changed_source_paths = sorted(
        changed_source_paths - declared_source_paths
    )
    if undeclared_changed_source_paths:
        raise QualityError(
            "changed canonical source paths must be declared by compatible "
            "change owners; "
            f"undeclared={undeclared_changed_source_paths}"
        )

    challenger_changes = manifest["challenger_changes"]
    if not isinstance(challenger_changes, list) or not challenger_changes:
        raise QualityError(
            "course quality ratchet challenger_changes must be non-empty"
        )
    candidate_ids: set[str] = set()
    for index, candidate in enumerate(challenger_changes):
        if not isinstance(candidate, dict) or set(candidate) != {
            "candidate_id",
            "hypothesis_id",
            "change_ids",
            "finding_ids",
            "change_owner_ids",
        }:
            raise QualityError(f"challenger_changes[{index}] fields must be exact")
        candidate_id = candidate["candidate_id"]
        if (
            not isinstance(candidate_id, str)
            or not candidate_id
            or candidate_id in candidate_ids
        ):
            raise QualityError(
                f"challenger_changes[{index}] has an invalid or duplicate candidate ID"
            )
        candidate_ids.add(candidate_id)
        change_ids = candidate["change_ids"]
        finding_ids = candidate["finding_ids"]
        candidate_owner_ids = candidate["change_owner_ids"]
        if (
            not _unique_nonempty_strings(change_ids)
            or not set(change_ids) <= set(changes_by_id)
            or not _unique_nonempty_strings(finding_ids)
            or not set(finding_ids) <= set(finding_owners)
            or not _unique_nonempty_strings(candidate_owner_ids)
            or not set(candidate_owner_ids) <= owner_ids
            or candidate["hypothesis_id"] != manifest["hypothesis_id"]
        ):
            raise QualityError(
                f"challenger_changes[{index}] has unresolved candidate links"
            )
        linked_findings = {
            finding_id
            for change_id in change_ids
            for finding_id in changes_by_id[change_id]["finding_ids"]
        }
        linked_owners = {
            owner_id
            for change_id in change_ids
            for owner_id in changes_by_id[change_id]["change_owner_ids"]
        }
        if (
            set(finding_ids) != linked_findings
            or set(candidate_owner_ids) != linked_owners
        ):
            raise QualityError(
                f"challenger_changes[{index}] must exactly match its change links"
            )
    declared_candidate_ids = [
        candidate["candidate_id"] for candidate in challenger_changes
    ]
    expected_candidate_ids = list(EXPECTED_VARIANTS)
    if declared_candidate_ids != expected_candidate_ids:
        raise QualityError(
            "challenger change registry must exactly match the isolated variants; "
            f"expected={expected_candidate_ids} actual={declared_candidate_ids}"
        )

    occupancy_reviews = manifest["occupancy_reviews"]
    if not isinstance(occupancy_reviews, list) or len(occupancy_reviews) != len(
        OCCUPANCY_REVIEW_CANDIDATE_IDS
    ):
        raise QualityError(
            "course quality ratchet occupancy_reviews must contain one ordered "
            "candidate-scoped review set per control and challenger"
        )
    occupancy_candidate_ids = [
        review_set.get("candidate_id") if isinstance(review_set, dict) else None
        for review_set in occupancy_reviews
    ]
    if occupancy_candidate_ids != list(OCCUPANCY_REVIEW_CANDIDATE_IDS):
        raise QualityError(
            "occupancy review candidate IDs must be exact and ordered; "
            f"expected={list(OCCUPANCY_REVIEW_CANDIDATE_IDS)} "
            f"actual={occupancy_candidate_ids}"
        )
    challenger_by_id = {
        challenger["candidate_id"]: challenger for challenger in challenger_changes
    }
    expected_occupancy_provenance = {
        "experiment_control": _experiment_control_occupancy_provenance(manifest),
        **{
            candidate_id: _candidate_acceptance_provenance(
                manifest, challenger_by_id[candidate_id]
            )
            for candidate_id in EXPECTED_VARIANTS
        },
    }
    for index, review_set in enumerate(occupancy_reviews):
        location = f"occupancy_reviews[{index}]"
        if not isinstance(review_set, dict) or set(review_set) != {
            "candidate_id",
            "candidate_provenance_sha256",
            "reviews",
        }:
            raise QualityError(f"{location} fields must be exact")
        candidate_id = review_set["candidate_id"]
        provenance_sha256 = _sha256_string(
            review_set["candidate_provenance_sha256"],
            f"{location}.candidate_provenance_sha256",
        )
        if provenance_sha256 != expected_occupancy_provenance[candidate_id]:
            raise QualityError(f"{location} candidate provenance is stale")
        reviews = review_set["reviews"]
        if not isinstance(reviews, list):
            raise QualityError(f"{location}.reviews must be a list")
        if candidate_id == "experiment_control":
            for review_index, review in enumerate(reviews):
                if (
                    not isinstance(review, dict)
                    or review.get("status") != "unresolved"
                    or review.get("live_review") is not None
                ):
                    raise QualityError(
                        "experiment-control occupancy reviews must remain explicitly "
                        f"unresolved with null live evidence; index={review_index}"
                    )
    acceptance = manifest["acceptance"]
    if (
        not isinstance(acceptance, dict)
        or set(acceptance) != {"modeled_eligibility_only", "candidates"}
        or acceptance["modeled_eligibility_only"] is not True
    ):
        raise QualityError("course quality ratchet acceptance fields must be exact")
    acceptance_candidates = acceptance["candidates"]
    if not isinstance(acceptance_candidates, list):
        raise QualityError(
            "course quality ratchet acceptance.candidates must be an ordered list"
        )
    acceptance_candidate_ids = [
        record.get("candidate_id") if isinstance(record, dict) else None
        for record in acceptance_candidates
    ]
    if acceptance_candidate_ids != declared_candidate_ids:
        raise QualityError(
            "acceptance candidate IDs must exactly match the challenger registry in "
            f"order; expected={declared_candidate_ids} "
            f"actual={acceptance_candidate_ids}"
        )
    for index, (challenger, evidence_record) in enumerate(
        zip(challenger_changes, acceptance_candidates, strict=True)
    ):
        candidate_id = challenger["candidate_id"]
        provenance_sha256 = _candidate_acceptance_provenance(manifest, challenger)
        _validate_candidate_acceptance_evidence(
            evidence_record,
            candidate_id=candidate_id,
            provenance_sha256=provenance_sha256,
            acceptance_artifacts=acceptance_artifacts,
            location=f"acceptance.candidates[{index}]",
        )
    _validate_acceptance_artifact_consumption(
        acceptance_candidates,
        acceptance_artifacts,
    )
    return manifest


def load_audit_manifest(
    segment_ids: Sequence[str],
) -> dict[str, Any]:
    """Load and validate audit rounds before current decisions are available."""
    manifest = scene_pipeline.load_yaml(AUDITS_PATH)
    expected_fields = {
        "schema_version",
        "evidence_scope",
        "priority_policy",
        "loop_policy",
        "consultation_policy",
        "saturation_policy",
        "change_ownership_policy",
        "high_priority_threshold",
        "rounds",
    }
    if not isinstance(manifest, dict) or set(manifest) != expected_fields:
        raise QualityError(
            "course quality audits fields must be exact; "
            f"missing={sorted(expected_fields - set(manifest or {}))} "
            f"unknown={sorted(set(manifest or {}) - expected_fields)}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise QualityError("course quality audits schema_version must be 1")
    for field, expected_policy in EXPECTED_AUDIT_POLICIES.items():
        policy = manifest[field]
        expected_policy_fields = set(expected_policy)
        if not isinstance(policy, dict) or set(policy) != expected_policy_fields:
            actual_fields = set(policy) if isinstance(policy, dict) else set()
            raise QualityError(
                f"course quality audits {field} fields must be exact; "
                f"missing={sorted(expected_policy_fields - actual_fields)} "
                f"unknown={sorted(actual_fields - expected_policy_fields)}"
            )
        if not _matches_exact_contract_value(policy, expected_policy):
            raise QualityError(
                f"course quality audits {field} values must exactly match the "
                "canonical policy"
            )
    threshold = manifest["high_priority_threshold"]
    if not _matches_exact_contract_value(
        threshold, EXPECTED_AUDIT_HIGH_PRIORITY_THRESHOLD
    ):
        raise QualityError(
            "course quality audits high_priority_threshold must exactly match "
            f"{EXPECTED_AUDIT_HIGH_PRIORITY_THRESHOLD}"
        )
    rounds = manifest["rounds"]
    if not isinstance(rounds, list):
        raise QualityError("course quality audits rounds must be a list")
    try:
        validated_rounds = [
            ratchet.validate_audit_round(record, segment_ids=segment_ids)
            for record in rounds
        ]
        ratchet.validate_audit_finding_identity(validated_rounds)
    except ratchet.RatchetContractError as error:
        raise QualityError(f"invalid course quality audit manifest: {error}") from error
    validated_manifest = copy.deepcopy(manifest)
    validated_manifest["rounds"] = validated_rounds
    return validated_manifest


def _validate_audit_change_links(
    audit_manifest: dict[str, Any], ratchet_manifest: dict[str, Any]
) -> None:
    audit_finding_id_list = [
        finding["finding_id"]
        for round_record in audit_manifest["rounds"]
        for report in round_record["audit_reports"]
        for finding in report["findings"]
    ]
    if len(audit_finding_id_list) != len(set(audit_finding_id_list)):
        raise QualityError("audit finding IDs must be globally unique across rounds")
    audit_finding_ids = set(audit_finding_id_list)
    owned_finding_ids = set(ratchet_manifest["finding_owners"])
    if audit_finding_ids != owned_finding_ids:
        raise QualityError(
            "audit findings and finding-owner registry must match exactly; "
            f"unowned={sorted(audit_finding_ids - owned_finding_ids)} "
            f"unaudited={sorted(owned_finding_ids - audit_finding_ids)}"
        )
    declared_candidate_ids = {
        record["candidate_id"] for record in ratchet_manifest["challenger_changes"]
    }
    for round_record in audit_manifest["rounds"]:
        disposition_ids = {
            record["candidate_id"] for record in round_record["challenger_dispositions"]
        }
        if disposition_ids != declared_candidate_ids:
            raise QualityError(
                f"audit round {round_record['round_id']} candidate dispositions "
                "must match the challenger change registry exactly"
            )


def _current_challenger_dispositions(
    audit_manifest: dict[str, Any],
    ratchet_manifest: dict[str, Any],
    ratchet_comparison: dict[str, Any],
) -> list[dict[str, str]]:
    """Bind saturation to current Pareto decisions, not historical labels."""

    declared_candidate_ids = [
        candidate["candidate_id"]
        for candidate in ratchet_manifest["challenger_changes"]
    ]
    evaluations = ratchet_comparison["pareto"]["evaluations"]
    generated_candidate_ids = [evaluation["candidate_id"] for evaluation in evaluations]
    if generated_candidate_ids != declared_candidate_ids:
        raise QualityError(
            "generated Pareto candidates must exactly match the challenger registry; "
            f"declared={declared_candidate_ids} generated={generated_candidate_ids}"
        )
    mismatched_decision_ids = [
        evaluation["candidate_id"]
        for evaluation in evaluations
        if evaluation["decision"]["candidate_id"] != evaluation["candidate_id"]
    ]
    if mismatched_decision_ids:
        raise QualityError(
            "generated Pareto decision IDs must match their candidate IDs; "
            f"candidates={mismatched_decision_ids}"
        )
    return [
        {
            "candidate_id": evaluation["candidate_id"],
            "disposition": evaluation["decision"]["disposition"],
            "decision_ref": (
                "diagram/course_quality.json#ratchet/pareto/evaluations/"
                f"{evaluation['candidate_id']}/decision"
            ),
        }
        for evaluation in evaluations
    ]


def _quality_source_digest(
    runtime_digest: str,
    ratchet_manifest: dict[str, Any],
    audit_manifest: dict[str, Any] | None = None,
) -> str:
    if audit_manifest is None:
        audit_manifest = scene_pipeline.load_yaml(AUDITS_PATH)
    digest = hashlib.sha256()
    digest.update(b"course_runtime\0")
    digest.update(runtime_digest.encode())
    digest.update(b"\0course/quality_ratchet.yaml\0")
    digest.update(scene_pipeline.canonical_payload(ratchet_manifest).encode())
    digest.update(b"\0course/quality_ratchet.yaml:source_bytes\0")
    digest.update(RATCHET_PATH.read_bytes())
    digest.update(b"\0course/quality_audits.yaml\0")
    digest.update(scene_pipeline.canonical_payload(audit_manifest).encode())
    digest.update(b"\0course/quality_audits.yaml:source_bytes\0")
    digest.update(AUDITS_PATH.read_bytes())
    digest.update(b"\0champion_contract\0")
    digest.update(Path(champion_pipeline.__file__).read_bytes())
    digest.update(b"\0ratchet_contract\0")
    digest.update(Path(ratchet.__file__).read_bytes())
    digest.update(b"\0quality_compiler\0")
    digest.update(Path(__file__).read_bytes())
    return digest.hexdigest()


def _round(value: float) -> float:
    return round(value, 6)


def _widest_maximum_physical_area_candidate(
    candidates: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    if not candidates:
        raise QualityError("no fitted teaching-overlay candidate")
    chosen = candidates[0]
    for candidate in candidates[1:]:
        area_delta = candidate["physical_area"] - chosen["physical_area"]
        if area_delta > 1e-6 or (
            abs(area_delta) <= 1e-6
            and candidate["standard_width_px"] > chosen["standard_width_px"]
        ):
            chosen = candidate
    return chosen


def _node_id(stage: str, *parts: str) -> str:
    return ":".join((stage, *parts))


def _stage_box(viewport: dict[str, int | str]) -> dict[str, int]:
    width = int(viewport["width"])
    height = int(viewport["height"])
    if width <= 820:
        rail = course_runtime.PORTRAIT_RAIL_WIDTH_PX
        head = 156
        if width <= 520:
            head = course_runtime.PORTRAIT_MASTHEAD_HEIGHT_PX
    elif width <= 1100:
        rail = 286
        head = 184
    else:
        rail = 286
        head = 196
    transport = course_runtime.PORTRAIT_TRANSPORT_HEIGHT_PX
    if height <= 560 and width >= 821:
        rail = 72
        head = course_runtime.SHORT_MASTHEAD_HEIGHT_PX
        transport = 58
    stage_width = width - rail
    stage_height = height - head - transport
    if stage_width <= 0 or stage_height <= 0:
        raise QualityError(f"viewport {width}x{height} leaves no course stage")
    return {
        "x": rail,
        "y": head,
        "width": stage_width,
        "height": stage_height,
        "pixel_count": stage_width * stage_height,
    }


def _bbox_2d(points: Iterable[tuple[float, float]]) -> tuple[float, ...]:
    values = list(points)
    if not values:
        raise QualityError("cannot measure an empty 2D focus")
    xs = [point[0] for point in values]
    ys = [point[1] for point in values]
    return min(xs), min(ys), max(xs), max(ys)


def _intersect_2d(
    left: tuple[float, float, float, float],
    right: tuple[float, float, float, float],
) -> tuple[float, float]:
    x0 = max(left[0], right[0])
    y0 = max(left[1], right[1])
    x1 = min(left[2], right[2])
    y1 = min(left[3], right[3])
    return max(0.0, x1 - x0), max(0.0, y1 - y0)


def _box(x: float, y: float, width: float, height: float) -> dict[str, float]:
    return {
        "x": _round(x),
        "y": _round(y),
        "width": _round(width),
        "height": _round(height),
    }


def _box_bounds(box: dict[str, float]) -> tuple[float, float, float, float]:
    return (
        float(box["x"]),
        float(box["y"]),
        float(box["x"]) + float(box["width"]),
        float(box["y"]) + float(box["height"]),
    )


def _boxes_intersect(
    left: dict[str, float], right: dict[str, float], *, gap: float = 0.0
) -> bool:
    left_x0, left_y0, left_x1, left_y1 = _box_bounds(left)
    right_x0, right_y0, right_x1, right_y1 = _box_bounds(right)
    return not (
        left_x1 + gap <= right_x0
        or left_x0 >= right_x1 + gap
        or left_y1 + gap <= right_y0
        or left_y0 >= right_y1 + gap
    )


def _box_is_contained(
    inner: dict[str, float], outer: dict[str, float], *, tolerance: float = 0.01
) -> bool:
    inner_x0, inner_y0, inner_x1, inner_y1 = _box_bounds(inner)
    outer_x0, outer_y0, outer_x1, outer_y1 = _box_bounds(outer)
    return (
        inner_x0 >= outer_x0 - tolerance
        and inner_y0 >= outer_y0 - tolerance
        and inner_x1 <= outer_x1 + tolerance
        and inner_y1 <= outer_y1 + tolerance
    )


def _stage_edge_clearances(
    stage: dict[str, float | int], overlay: dict[str, float]
) -> dict[str, float]:
    stage_x0, stage_y0, stage_x1, stage_y1 = _box_bounds(stage)
    overlay_x0, overlay_y0, overlay_x1, overlay_y1 = _box_bounds(overlay)
    return {
        "top": _round(overlay_y0 - stage_y0),
        "right": _round(stage_x1 - overlay_x1),
        "bottom": _round(stage_y1 - overlay_y1),
        "left": _round(overlay_x0 - stage_x0),
    }


def _segment_intersects_box(
    start: tuple[float, float],
    end: tuple[float, float],
    box: dict[str, float],
    *,
    gap: float = 0.0,
) -> bool:
    """Return whether a closed line segment intersects an expanded box."""
    x0, y0, x1, y1 = _box_bounds(box)
    bounds = ((x0 - gap, x1 + gap), (y0 - gap, y1 + gap))
    near = 0.0
    far = 1.0
    for origin, delta, (minimum, maximum) in zip(
        start,
        (end[0] - start[0], end[1] - start[1]),
        bounds,
        strict=True,
    ):
        if abs(delta) < 1e-9:
            if origin < minimum or origin > maximum:
                return False
            continue
        first = (minimum - origin) / delta
        second = (maximum - origin) / delta
        entry = min(first, second)
        exit_ = max(first, second)
        near = max(near, entry)
        far = min(far, exit_)
        if near > far:
            return False
    return far >= 0.0 and near <= 1.0


def _segments_intersect(
    left_start: tuple[float, float],
    left_end: tuple[float, float],
    right_start: tuple[float, float],
    right_end: tuple[float, float],
) -> bool:
    """Return whether two closed line segments intersect."""
    epsilon = 1e-9

    def orientation(
        start: tuple[float, float],
        end: tuple[float, float],
        point: tuple[float, float],
    ) -> float:
        return (end[0] - start[0]) * (point[1] - start[1]) - (end[1] - start[1]) * (
            point[0] - start[0]
        )

    def on_segment(
        start: tuple[float, float],
        end: tuple[float, float],
        point: tuple[float, float],
    ) -> bool:
        return (
            min(start[0], end[0]) - epsilon
            <= point[0]
            <= max(start[0], end[0]) + epsilon
            and min(start[1], end[1]) - epsilon
            <= point[1]
            <= max(start[1], end[1]) + epsilon
        )

    left_right_start = orientation(left_start, left_end, right_start)
    left_right_end = orientation(left_start, left_end, right_end)
    right_left_start = orientation(right_start, right_end, left_start)
    right_left_end = orientation(right_start, right_end, left_end)

    def straddles(first: float, second: float) -> bool:
        return (first > epsilon and second < -epsilon) or (
            first < -epsilon and second > epsilon
        )

    if straddles(left_right_start, left_right_end) and straddles(
        right_left_start, right_left_end
    ):
        return True
    return (
        (
            abs(left_right_start) <= epsilon
            and on_segment(left_start, left_end, right_start)
        )
        or (
            abs(left_right_end) <= epsilon
            and on_segment(left_start, left_end, right_end)
        )
        or (
            abs(right_left_start) <= epsilon
            and on_segment(right_start, right_end, left_start)
        )
        or (
            abs(right_left_end) <= epsilon
            and on_segment(right_start, right_end, left_end)
        )
    )


def _legacy_visual_stage_box(
    stage: dict[str, int], overlay: dict[str, Any]
) -> dict[str, int]:
    """Return the original non-overlapping pane used before responsive fitting."""
    if not overlay.get("initially_visible", overlay["present"]):
        return dict(stage)
    overlay_box = overlay["box"]
    if overlay_box["width"] >= stage["width"] * 0.72:
        x = float(stage["x"])
        y = float(stage["y"])
        width = float(stage["width"])
        height = overlay_box["y"] - TEACHING_DOCK_GAP_PX - y
        dock = "bottom"
    else:
        stage_center = stage["x"] + stage["width"] / 2.0
        overlay_center = overlay_box["x"] + overlay_box["width"] / 2.0
        y = float(stage["y"])
        height = float(stage["height"])
        if overlay_center <= stage_center:
            x = overlay_box["x"] + overlay_box["width"] + TEACHING_DOCK_GAP_PX
            width = stage["x"] + stage["width"] - x
            dock = "left"
        else:
            x = float(stage["x"])
            width = overlay_box["x"] - TEACHING_DOCK_GAP_PX - x
            dock = "right"
    if width <= 0 or height <= 0:
        raise QualityError("teaching dock leaves no visual stage")
    return {
        "x": round(x),
        "y": round(y),
        "width": round(width),
        "height": round(height),
        "pixel_count": round(width) * round(height),
        "dock": dock,
    }


def _frame_render_metrics(
    box: dict[str, float],
    view_width: float,
    view_height: float,
    horizontal_padding: float,
    vertical_padding: float,
) -> dict[str, float] | None:
    """Fit an unchanged canonical viewBox inside a candidate visual pane."""
    inner_width = float(box["width"]) - horizontal_padding
    inner_height = float(box["height"]) - vertical_padding
    if inner_width <= 0 or inner_height <= 0:
        return None
    scale = min(inner_width / view_width, inner_height / view_height)
    rendered_width = view_width * scale
    rendered_height = view_height * scale
    return {
        "scale": scale,
        "rendered_width": rendered_width,
        "rendered_height": rendered_height,
        "rendered_pixel_area": rendered_width * rendered_height,
    }


def _visual_stage_candidates(
    stage: dict[str, int],
    overlay: dict[str, Any],
    view_width: float,
    view_height: float,
    horizontal_padding: float,
    vertical_padding: float,
) -> list[dict[str, Any]]:
    """Return runtime-order side and above-overlay canonical-frame fits."""
    overlay_box = overlay["box"]
    stage_right = float(stage["x"] + stage["width"])
    stage_center = float(stage["x"]) + float(stage["width"]) / 2.0
    overlay_center = float(overlay_box["x"]) + float(overlay_box["width"]) / 2.0
    if overlay_center <= stage_center:
        side_x = (
            float(overlay_box["x"]) + float(overlay_box["width"]) + TEACHING_DOCK_GAP_PX
        )
        side = {
            "x": side_x,
            "y": float(stage["y"]),
            "width": stage_right - side_x,
            "height": float(stage["height"]),
            "dock": "left",
        }
    else:
        side = {
            "x": float(stage["x"]),
            "y": float(stage["y"]),
            "width": float(overlay_box["x"]) - TEACHING_DOCK_GAP_PX - float(stage["x"]),
            "height": float(stage["height"]),
            "dock": "right",
        }
    candidates = [
        side,
        {
            "x": float(stage["x"]),
            "y": float(stage["y"]),
            "width": float(stage["width"]),
            "height": float(overlay_box["y"])
            - TEACHING_DOCK_GAP_PX
            - float(stage["y"]),
            "dock": "bottom",
        },
    ]
    fitted = []
    for candidate in candidates:
        metrics = _frame_render_metrics(
            candidate,
            view_width,
            view_height,
            horizontal_padding,
            vertical_padding,
        )
        if metrics is not None:
            fitted.append({**candidate, **metrics})
    return fitted


def _visual_stage_box(
    stage: dict[str, int],
    overlay: dict[str, Any],
    *,
    view_box: Sequence[float] | None = None,
    horizontal_padding: float = 0.0,
    vertical_padding: float = 0.0,
    legacy_overlay: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Fit the largest canonical frame that clears an authored teaching overlay.

    Two-dimensional annotated scenes compare the overlay-opposite side pane with
    the pane above the overlay.  The winner is the pane that renders the largest
    unchanged canonical viewBox.  The full winning pane remains available to
    focus labels and markers; physical rendered pixels, not the pane's local
    denominator, decide whether the composition improved.
    """
    if not overlay.get("initially_visible", overlay["present"]):
        if view_box is None:
            return dict(stage)
        _, _, view_width, view_height = (float(value) for value in view_box)
        metrics = _frame_render_metrics(
            stage,
            view_width,
            view_height,
            horizontal_padding,
            vertical_padding,
        )
        if metrics is None:
            raise QualityError("full visual stage leaves no fitted frame")
        rendered_pixel_area = metrics["rendered_pixel_area"]
        full_stage_pixels = float(stage["pixel_count"])
        return {
            **stage,
            "dock": "none",
            "fit_policy": "full_stage_no_initial_overlay",
            "rendered_pixel_area": _round(rendered_pixel_area),
            "rendered_pixel_ratio_to_full_stage": _round(
                rendered_pixel_area / full_stage_pixels
            ),
            "legacy_rendered_pixel_area": _round(rendered_pixel_area),
            "legacy_rendered_pixel_ratio_to_full_stage": _round(
                rendered_pixel_area / full_stage_pixels
            ),
            "rendered_pixel_area_retention_ratio": 1.0,
            "max_candidate_rendered_pixel_area": _round(rendered_pixel_area),
            "max_render_area_candidate_selected": True,
            "candidate_rendered_frames": [
                {
                    "dock": "none",
                    "available_box": {
                        key: _round(stage[key]) for key in ("x", "y", "width", "height")
                    },
                    "rendered_width": _round(metrics["rendered_width"]),
                    "rendered_height": _round(metrics["rendered_height"]),
                    "rendered_pixel_area": _round(rendered_pixel_area),
                }
            ],
            "legacy_visual_stage": {
                **stage,
                "dock": "none",
                "fit_policy": "full_stage_no_initial_overlay",
            },
        }
    if view_box is None:
        return _legacy_visual_stage_box(stage, overlay)

    _, _, view_width, view_height = (float(value) for value in view_box)
    fitted_candidates = _visual_stage_candidates(
        stage,
        overlay,
        view_width,
        view_height,
        horizontal_padding,
        vertical_padding,
    )
    if not fitted_candidates:
        raise QualityError("teaching overlay leaves no fitted visual pane")

    chosen = max(
        fitted_candidates,
        key=lambda candidate: candidate["rendered_pixel_area"],
    )
    legacy_candidates = _visual_stage_candidates(
        stage,
        legacy_overlay or overlay,
        view_width,
        view_height,
        horizontal_padding,
        vertical_padding,
    )
    if not legacy_candidates:
        raise QualityError("legacy teaching dock leaves no fitted visual frame")
    legacy_chosen = max(
        legacy_candidates,
        key=lambda candidate: candidate["rendered_pixel_area"],
    )
    rendered_pixel_area = chosen["rendered_pixel_area"]
    legacy_rendered_pixel_area = legacy_chosen["rendered_pixel_area"]
    full_stage_pixels = float(stage["pixel_count"])
    return {
        "x": _round(chosen["x"]),
        "y": _round(chosen["y"]),
        "width": _round(chosen["width"]),
        "height": _round(chosen["height"]),
        "pixel_count": _round(chosen["width"] * chosen["height"]),
        "dock": chosen["dock"],
        "fit_policy": "max_render_area_full_available_pane",
        "rendered_pixel_area": _round(rendered_pixel_area),
        "rendered_pixel_ratio_to_full_stage": _round(
            rendered_pixel_area / full_stage_pixels
        ),
        "legacy_rendered_pixel_area": _round(legacy_rendered_pixel_area),
        "legacy_rendered_pixel_ratio_to_full_stage": _round(
            legacy_rendered_pixel_area / full_stage_pixels
        ),
        "rendered_pixel_area_retention_ratio": _round(
            rendered_pixel_area / legacy_rendered_pixel_area
        ),
        "max_candidate_rendered_pixel_area": _round(
            max(candidate["rendered_pixel_area"] for candidate in fitted_candidates)
        ),
        "max_render_area_candidate_selected": True,
        "candidate_rendered_frames": [
            {
                "dock": candidate["dock"],
                "available_box": {
                    "x": _round(candidate["x"]),
                    "y": _round(candidate["y"]),
                    "width": _round(candidate["width"]),
                    "height": _round(candidate["height"]),
                },
                "rendered_width": _round(candidate["rendered_width"]),
                "rendered_height": _round(candidate["rendered_height"]),
                "rendered_pixel_area": _round(candidate["rendered_pixel_area"]),
            }
            for candidate in fitted_candidates
        ],
        "legacy_visual_stage": {
            "x": _round(legacy_chosen["x"]),
            "y": _round(legacy_chosen["y"]),
            "width": _round(legacy_chosen["width"]),
            "height": _round(legacy_chosen["height"]),
            "pixel_count": _round(legacy_chosen["width"] * legacy_chosen["height"]),
            "dock": legacy_chosen["dock"],
            "fit_policy": "max_render_area_full_available_pane",
        },
    }


def _wrapped_line_count(text: str, width: float, font_size: float) -> int:
    """Estimate browser word wrapping using the course's compact sans face."""
    if width <= 0:
        return max(1, len(text))
    glyph_width = font_size * 0.54
    line_width = 0.0
    lines = 1
    for word in text.split():
        word_width = len(word) * glyph_width
        separator = glyph_width if line_width else 0.0
        if line_width and line_width + separator + word_width > width:
            lines += 1
            line_width = word_width
        else:
            line_width += separator + word_width
    return lines


def _teaching_grid_height(
    annotation: dict[str, Any],
    content_width: float,
    profile: str,
    segment_id: str | None = None,
) -> float:
    items = annotation["items"]
    kind = annotation["kind"]
    if profile == "short_height":
        gap = 4.0
        font_size = 10.0
        line_height = font_size * 1.15
        padding_x = 5.0
        padding_y = float(course_runtime.SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX)
        maximum_columns = max(1, math.floor((content_width + gap) / (90.0 + gap)))
        columns = min(len(items), maximum_columns)
        if kind == "parallel":
            columns = 2
        sequence_prefix = 0.0
        routes_last_spans = False
    elif profile == "narrow":
        gap = 5.0
        font_size = 10.0
        line_height = font_size * 1.25
        padding_x = 7.0
        padding_y = 6.0
        columns = 2
        sequence_prefix = 25.0 if kind == "sequence" else 0.0
        routes_last_spans = kind == "routes"
    else:
        gap = 7.0
        font_size = 11.0
        line_height = font_size * 1.25
        padding_x = 9.0
        padding_y = 7.0
        columns = 2 if kind in {"comparison", "parallel", "routes"} else 1
        sequence_prefix = 25.0 if kind == "sequence" else 0.0
        routes_last_spans = kind == "routes"

    column_width = (content_width - gap * (columns - 1)) / columns

    def item_height(index: int, item: dict[str, Any], width: float) -> float:
        if kind == "funnel":
            if profile in {"narrow", "short_height"} and index < 5:
                width *= (1.0, 0.96, 0.92, 0.88, 0.84)[index]
            elif index < 5:
                width *= (1.0, 0.9, 0.8, 0.7, 0.6)[index]
        p1_swatch_prefix = 0.0
        if segment_id == "p1_read_the_machine":
            p1_swatch_prefix = 37.0 if profile == "standard" else 30.0
        text_width = max(
            1.0,
            width - 2 * padding_x - 3.0 - sequence_prefix - p1_swatch_prefix,
        )
        lines = _wrapped_line_count(item["label"], text_width, font_size)
        return lines * line_height + 2 * padding_y

    rows: list[float] = []
    if kind == "parallel":
        rows.append(item_height(0, items[0], content_width))
        rows.append(
            max(
                item_height(index, item, column_width)
                for index, item in enumerate(items[1:3], start=1)
            )
        )
        rows.append(item_height(3, items[3], content_width))
    elif routes_last_spans and len(items) % columns == 1 and len(items) > 1:
        regular = items[:-1]
        for offset in range(0, len(regular), columns):
            rows.append(
                max(
                    item_height(offset + index, item, column_width)
                    for index, item in enumerate(regular[offset : offset + columns])
                )
            )
        rows.append(item_height(len(items) - 1, items[-1], content_width))
    else:
        for offset in range(0, len(items), columns):
            rows.append(
                max(
                    item_height(offset + index, item, column_width)
                    for index, item in enumerate(items[offset : offset + columns])
                )
            )
    return sum(rows) + gap * max(0, len(rows) - 1)


def _portrait_focus_key_evaluation(
    segment: dict[str, Any],
    master: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Resolve and model the complete portrait key without claiming a live audit."""
    if segment["visual"]["label_policy"] != "focus":
        return {
            "applicable": False,
            "passed": True,
            "status": "not_applicable",
            "evidence_scope": PORTRAIT_FOCUS_KEY_EVIDENCE_SCOPE,
            "segment_id": segment["segment_id"],
            "viewport_id": PORTRAIT_VIEWPORT_ID,
            "entry_count": 0,
            "entries": [],
            "estimate": None,
            "failure_reasons": [],
        }

    entries = course_runtime.focus_key_entries(segment, master, evidence)
    estimate = course_runtime.estimate_portrait_masthead_layout(
        segment,
        [entry["compact_label"] for entry in entries],
        grammar_cues=[entry["swatch_cue"] for entry in entries],
    )
    if estimate["evidence_scope"] != PORTRAIT_FOCUS_KEY_EVIDENCE_SCOPE:
        raise QualityError("portrait focus-key evidence scope drifted")
    reasons = []
    if not entries:
        reasons.append("empty_focus_key")
    if not estimate["focus_key"]["within_chip_budget"]:
        reasons.append("focus_key_chip_budget_exceeded")
    if estimate["focus_key"]["horizontal_paging_required"]:
        reasons.append("horizontal_paging_required")
    if estimate["required_height_px"] > estimate["budget_height_px"]:
        reasons.append("insufficient_portrait_header_budget")
    if not estimate["safety_margin_passed"]:
        reasons.append("portrait_header_safety_margin_failed")
    if not estimate["estimated_complete_key_fit"] and not reasons:
        reasons.append("portrait_focus_key_fit_failed")
    return {
        "applicable": True,
        "passed": not reasons,
        "status": "passed" if not reasons else "failed",
        "evidence_scope": PORTRAIT_FOCUS_KEY_EVIDENCE_SCOPE,
        "segment_id": segment["segment_id"],
        "viewport_id": PORTRAIT_VIEWPORT_ID,
        "entry_count": len(entries),
        "entries": entries,
        "estimate": estimate,
        "failure_reasons": reasons,
    }


def _short_focus_key_evaluation(
    segment: dict[str, Any],
    master: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Model the complete compact key at the protected 844x390 viewport."""
    entries = course_runtime.focus_key_entries(segment, master, evidence)
    if segment["visual"]["label_policy"] != "focus":
        return {
            "applicable": False,
            "passed": True,
            "status": "not_applicable",
            "evidence_scope": SHORT_FOCUS_KEY_EVIDENCE_SCOPE,
            "segment_id": segment["segment_id"],
            "viewport_id": SHORT_VIEWPORT_ID,
            "entry_count": 0,
            "entries": [],
            "estimate": None,
            "failure_reasons": [],
        }
    estimate = course_runtime.estimate_short_focus_key_layout(
        [str(entry["compact_label"]) for entry in entries],
        grammar_cues=[entry["swatch_cue"] for entry in entries],
    )
    reasons = []
    if not entries:
        reasons.append("empty_focus_key")
    if not estimate["within_chip_budget"]:
        reasons.append("focus_key_chip_budget_exceeded")
    if estimate["maximum_excess_width_px"] > 0:
        reasons.append("compact_label_width_exceeded")
    if estimate["excess_height_px"] > 0:
        reasons.append("compact_key_height_exceeded")
    if estimate["font_px"] < MIN_SPATIAL_LABEL_FONT_PX:
        reasons.append("compact_key_font_below_floor")
    if estimate["index_font_px"] < MIN_SPATIAL_LABEL_FONT_PX:
        reasons.append("compact_key_index_font_below_floor")
    if estimate["horizontal_paging_required"]:
        reasons.append("horizontal_paging_required")
    if not estimate["estimated_complete_key_fit"] and not reasons:
        reasons.append("short_focus_key_fit_failed")
    return {
        "applicable": True,
        "passed": not reasons,
        "status": "passed" if not reasons else "failed",
        "evidence_scope": SHORT_FOCUS_KEY_EVIDENCE_SCOPE,
        "segment_id": segment["segment_id"],
        "viewport_id": SHORT_VIEWPORT_ID,
        "entry_count": len(entries),
        "entries": entries,
        "estimate": estimate,
        "failure_reasons": reasons,
    }


def _tablet_focus_key_evaluation(
    segment: dict[str, Any],
    master: dict[str, Any],
    evidence: dict[str, Any],
) -> dict[str, Any]:
    """Model the complete compact key at the protected 1024x768 viewport."""
    entries = course_runtime.focus_key_entries(segment, master, evidence)
    if segment["visual"]["label_policy"] != "focus":
        return {
            "applicable": False,
            "passed": True,
            "status": "not_applicable",
            "evidence_scope": TABLET_FOCUS_KEY_EVIDENCE_SCOPE,
            "segment_id": segment["segment_id"],
            "viewport_id": TABLET_VIEWPORT_ID,
            "entry_count": 0,
            "entries": [],
            "estimate": None,
            "failure_reasons": [],
        }
    estimate = course_runtime.estimate_tablet_focus_key_layout(
        [str(entry["compact_label"]) for entry in entries],
        grammar_cues=[entry["swatch_cue"] for entry in entries],
    )
    reasons = []
    if not entries:
        reasons.append("empty_focus_key")
    if not estimate["within_chip_budget"]:
        reasons.append("focus_key_chip_budget_exceeded")
    if estimate["maximum_excess_width_px"] > 0:
        reasons.append("compact_label_width_exceeded")
    if estimate["excess_height_px"] > 0:
        reasons.append("compact_key_height_exceeded")
    if estimate["font_px"] < MIN_SPATIAL_LABEL_FONT_PX:
        reasons.append("compact_key_font_below_floor")
    if estimate["index_font_px"] < MIN_SPATIAL_LABEL_FONT_PX:
        reasons.append("compact_key_index_font_below_floor")
    if estimate["horizontal_paging_required"]:
        reasons.append("horizontal_paging_required")
    if not estimate["estimated_complete_key_fit"] and not reasons:
        reasons.append("tablet_focus_key_fit_failed")
    return {
        "applicable": True,
        "passed": not reasons,
        "status": "passed" if not reasons else "failed",
        "evidence_scope": TABLET_FOCUS_KEY_EVIDENCE_SCOPE,
        "segment_id": segment["segment_id"],
        "viewport_id": TABLET_VIEWPORT_ID,
        "entry_count": len(entries),
        "entries": entries,
        "estimate": estimate,
        "failure_reasons": reasons,
    }


def _desktop_focus_key_evaluation(
    segment: dict[str, Any],
    master: dict[str, Any],
    evidence: dict[str, Any],
    viewport_id: str,
) -> dict[str, Any]:
    """Model the complete wrapped key at one canonical desktop viewport."""
    if viewport_id not in DESKTOP_VIEWPORT_IDS:
        raise QualityError(f"unsupported desktop focus-key viewport: {viewport_id}")
    entries = course_runtime.focus_key_entries(segment, master, evidence)
    if segment["visual"]["label_policy"] != "focus":
        return {
            "applicable": False,
            "passed": True,
            "status": "not_applicable",
            "evidence_scope": DESKTOP_FOCUS_KEY_EVIDENCE_SCOPE,
            "segment_id": segment["segment_id"],
            "viewport_id": viewport_id,
            "entry_count": 0,
            "entries": [],
            "estimate": None,
            "failure_reasons": [],
        }
    estimate = course_runtime.estimate_desktop_focus_key_layout(
        [str(entry["compact_label"]) for entry in entries],
        viewport_id=viewport_id,
        grammar_cues=[entry["swatch_cue"] for entry in entries],
    )
    reasons = []
    if not entries:
        reasons.append("empty_focus_key")
    if not estimate["within_chip_budget"]:
        reasons.append("focus_key_chip_budget_exceeded")
    if estimate["maximum_excess_width_px"] > 0:
        reasons.append("compact_label_width_exceeded")
    if estimate["excess_height_px"] > 0:
        reasons.append("compact_key_height_exceeded")
    if estimate["font_px"] < MIN_SPATIAL_LABEL_FONT_PX:
        reasons.append("compact_key_font_below_floor")
    if estimate["index_font_px"] < MIN_SPATIAL_LABEL_FONT_PX:
        reasons.append("compact_key_index_font_below_floor")
    if estimate["horizontal_paging_required"]:
        reasons.append("horizontal_paging_required")
    if not estimate["estimated_complete_key_fit"] and not reasons:
        reasons.append("desktop_focus_key_fit_failed")
    return {
        "applicable": True,
        "passed": not reasons,
        "status": "passed" if not reasons else "failed",
        "evidence_scope": DESKTOP_FOCUS_KEY_EVIDENCE_SCOPE,
        "segment_id": segment["segment_id"],
        "viewport_id": viewport_id,
        "entry_count": len(entries),
        "entries": entries,
        "estimate": estimate,
        "failure_reasons": reasons,
    }


def _header_flow_evaluation(
    segment: dict[str, Any],
    viewport: dict[str, int | str],
    stage: dict[str, int],
    focus_key_entries: Sequence[dict[str, Any]],
    portrait_focus_key: dict[str, Any] | None = None,
    short_focus_key: dict[str, Any] | None = None,
    tablet_focus_key: dict[str, Any] | None = None,
    desktop_focus_key: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Model the fixed masthead stack that must retain the focus key."""
    width = int(viewport["width"])
    height = int(viewport["height"])
    focus_key_applicable = segment["visual"]["label_policy"] == "focus"
    if width <= 520:
        if portrait_focus_key is None:
            raise QualityError("portrait header flow requires its focus-key evaluation")
        estimate = (
            portrait_focus_key["estimate"]
            if focus_key_applicable
            else course_runtime.estimate_portrait_masthead_layout(segment, [])
        )
        passed = estimate["required_height_px"] <= estimate["budget_height_px"]
        if focus_key_applicable:
            passed = passed and portrait_focus_key["passed"]
        overflow = max(
            0.0,
            estimate["required_height_px"] - estimate["budget_height_px"],
        )
        return {
            "passed": passed,
            "measurement_scope": "total_masthead_box",
            "evidence_scope": PORTRAIT_FOCUS_KEY_EVIDENCE_SCOPE,
            "content_width_px": estimate["content_width_px"],
            "required_height_px": estimate["required_height_px"],
            "available_height_px": estimate["budget_height_px"],
            "overflow_px": _round(overflow),
            "focus_key_applicable": focus_key_applicable,
            "focus_key_visible": passed if focus_key_applicable else None,
            "focus_key_height_px": (
                estimate["focus_key"]["estimated_height_px"]
                if focus_key_applicable
                else 0.0
            ),
            "reason": None
            if passed
            else (
                portrait_focus_key["failure_reasons"]
                if focus_key_applicable
                else ["fixed_masthead_overflow"]
            ),
        }

    compact = width <= 1100
    short_height = height <= 560 and width >= 821
    if width <= 820:
        horizontal_padding = 28.0
        vertical_padding = 22.0
        posture_width = 0.0
        column_gap = 0.0
    elif short_height:
        horizontal_padding = 20.0
        vertical_padding = 12.0
        posture_width = 190.0
        column_gap = 24.0
    elif compact:
        horizontal_padding = 48.0
        vertical_padding = 33.0
        posture_width = 0.0
        column_gap = 0.0
    else:
        horizontal_padding = 48.0
        vertical_padding = 33.0
        posture_width = 190.0
        column_gap = 24.0
    content_width = stage["width"] - horizontal_padding - posture_width - column_gap
    if content_width <= 0:
        return {
            "passed": False,
            "content_width_px": _round(content_width),
            "required_height_px": None,
            "available_height_px": None,
            "overflow_px": None,
            "focus_key_applicable": focus_key_applicable,
            "focus_key_visible": False,
            "focus_key_height_px": None,
            "reason": "no_masthead_content_width",
        }

    def line_height(text: str, font: float, ratio: float) -> float:
        return _wrapped_line_count(text, content_width, font) * font * ratio

    eyebrow = (
        f"Act {segment['act_sequence']} · {segment['act_title']} · "
        f"{segment['sequence']:02d} / {course_runtime.EXPECTED_SEGMENTS}"
    )
    boundary = (
        "Source-gated Abilene facts · dashed equipment is a teaching reference, "
        "not as-built."
        if compact
        else segment["boundary_note"]
    )
    if short_height:
        required = line_height(eyebrow, 9.0, 1.2)
        required += 2.0 + line_height(segment["title"], 16.0, 1.1)
        required += 2.0 + line_height(
            segment["opening_question"],
            course_runtime.SHORT_OPENING_QUESTION_FONT_PX,
            1.25,
        )
        required += 2.0 + line_height(boundary, 10.0, 1.1)
        if short_focus_key is None:
            raise QualityError("short header flow requires its focus-key evaluation")
        focus_key_height = (
            short_focus_key["estimate"]["estimated_height_px"]
            if focus_key_applicable
            else 0.0
        )
        if focus_key_applicable:
            required += 2.0 + focus_key_height
    else:
        required = line_height(eyebrow, 9.0, 1.2)
        required += 5.0 + line_height(segment["title"], 20.0, 1.1)
        required += 5.0 + line_height(segment["opening_question"], 11.0, 1.25)
        if not compact:
            required += 4.0 + line_height(segment["learning_objective"], 9.0, 1.25)
        required += 4.0 + line_height(boundary, 10.0, 1.2)
        required += 5.0 + 10.0 * 1.25
        if viewport["id"] == TABLET_VIEWPORT_ID:
            if tablet_focus_key is None:
                raise QualityError(
                    "tablet header flow requires its focus-key evaluation"
                )
            focus_key_height = (
                tablet_focus_key["estimate"]["estimated_height_px"]
                if focus_key_applicable
                else 0.0
            )
        elif viewport["id"] in DESKTOP_VIEWPORT_IDS:
            if desktop_focus_key is None:
                raise QualityError(
                    "desktop header flow requires its focus-key evaluation"
                )
            focus_key_height = (
                desktop_focus_key["estimate"]["estimated_height_px"]
                if focus_key_applicable
                else 0.0
            )
        else:
            focus_key_height = 21.5 if focus_key_applicable else 0.0
        if focus_key_applicable:
            required += 6.0 + focus_key_height
    available = stage["y"] - vertical_padding - 1.5
    overflow = max(0.0, required - available)
    spare_height = available - required
    required_safety_margin = (
        course_runtime.SHORT_MASTHEAD_SAFETY_MARGIN_PX if short_height else 0.0
    )
    missing_key = focus_key_applicable and not focus_key_entries
    short_key_failed = bool(
        short_height and focus_key_applicable and not short_focus_key["passed"]
    )
    tablet_key_failed = bool(
        viewport["id"] == TABLET_VIEWPORT_ID
        and focus_key_applicable
        and not tablet_focus_key["passed"]
    )
    desktop_key_failed = bool(
        viewport["id"] in DESKTOP_VIEWPORT_IDS
        and focus_key_applicable
        and not desktop_focus_key["passed"]
    )
    safety_margin_failed = spare_height < required_safety_margin
    passed = (
        overflow == 0.0
        and not missing_key
        and not short_key_failed
        and not tablet_key_failed
        and not desktop_key_failed
        and not safety_margin_failed
    )
    return {
        "passed": passed,
        "measurement_scope": "masthead_content_box",
        "evidence_scope": "deterministic_static_estimate_not_live_browser",
        "content_width_px": _round(content_width),
        "required_height_px": _round(required),
        "available_height_px": _round(available),
        "overflow_px": _round(overflow),
        "spare_height_px": _round(spare_height),
        "required_safety_margin_px": required_safety_margin,
        "safety_margin_passed": not safety_margin_failed,
        "opening_question_font_px": (
            course_runtime.SHORT_OPENING_QUESTION_FONT_PX if short_height else 11.0
        ),
        "focus_key_applicable": focus_key_applicable,
        "focus_key_visible": passed if focus_key_applicable else None,
        "focus_key_height_px": focus_key_height,
        "reason": None
        if passed
        else (
            "empty_focus_key"
            if missing_key
            else (
                short_focus_key["failure_reasons"]
                if short_key_failed
                else (
                    tablet_focus_key["failure_reasons"]
                    if tablet_key_failed
                    else (
                        desktop_focus_key["failure_reasons"]
                        if desktop_key_failed
                        else (
                            "short_masthead_safety_margin_failed"
                            if safety_margin_failed
                            else "fixed_masthead_overflow"
                        )
                    )
                )
            )
        ),
    }


def _teaching_overlay_box(
    annotation: dict[str, Any],
    viewport: dict[str, int | str],
    stage: dict[str, int],
    *,
    standard_width_px: float = (
        course_runtime.TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX
    ),
    segment_id: str | None = None,
) -> tuple[dict[str, float], str]:
    width = int(viewport["width"])
    height = int(viewport["height"])
    rail = stage["x"]
    head = stage["y"]
    transport = height - stage["y"] - stage["height"]
    border = 1.5

    if height <= 560 and width >= 821:
        profile = "short_height"
        overlay_width = min(390.0, (width - rail) * 0.52)
        right_aligned = annotation["position"] == "right" or annotation[
            "position"
        ].endswith("-right")
        stage_edge_clearance = float(
            course_runtime.TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
        )
        x = (
            width - stage_edge_clearance - overlay_width
            if right_aligned
            else rail + stage_edge_clearance
        )
        bottom_gap = stage_edge_clearance
        overlay_padding_block = float(
            course_runtime.SHORT_TEACHING_OVERLAY_PADDING_BLOCK_PX
        )
        padding = (
            overlay_padding_block,
            8.0,
            overlay_padding_block,
            8.0,
        )
        kicker_font = 9.0
        title_font = 11.0
        title_margins = (2.0, 5.0)
    elif width <= 820:
        profile = "narrow"
        overlay_width = width - rail - 28.0
        x = rail + 14.0
        bottom_gap = 14.0
        padding = (9.0, 12.0, 10.0, 12.0)
        kicker_font = 9.0
        title_font = 13.0
        title_margins = (3.0, 5.0)
    else:
        profile = "standard"
        overlay_width = min(standard_width_px, width - rail - 48.0)
        right_aligned = annotation["position"] == "right" or annotation[
            "position"
        ].endswith("-right")
        x = width - 24.0 - overlay_width if right_aligned else rail + 24.0
        bottom_gap = 22.0
        padding = (14.0, 16.0, 15.0, 16.0)
        kicker_font = 9.0
        title_font = 15.0
        title_margins = (5.0, 10.0)

    padding_top, padding_right, padding_bottom, padding_left = padding
    content_width = overlay_width - padding_left - padding_right - 2 * border
    kicker_height = kicker_font * 1.2
    title_lines = _wrapped_line_count(annotation["title"], content_width, title_font)
    title_height = title_lines * title_font * 1.15
    items_height = _teaching_grid_height(
        annotation,
        content_width,
        profile,
        segment_id,
    )
    overlay_height = (
        2 * border
        + padding_top
        + kicker_height
        + title_margins[0]
        + title_height
        + title_margins[1]
        + items_height
        + padding_bottom
    )

    top_aligned = profile == "standard" and annotation["position"].startswith("top-")
    if top_aligned:
        y = head + 22.0
    else:
        y = height - transport - bottom_gap - overlay_height
    return _box(x, y, overlay_width, overlay_height), profile


def _teaching_overlay_evaluation(
    segment: dict[str, Any],
    viewport: dict[str, int | str],
    stage: dict[str, int],
    selected_label_boxes: list[dict[str, Any]],
    focus_key_ids: Sequence[str],
    *,
    standard_width_px: float = (
        course_runtime.TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX
    ),
) -> dict[str, Any]:
    annotation = segment["visual"]["annotation"]
    if annotation is None:
        return {
            "present": False,
            "initially_visible": False,
            "interaction_mode": "not_applicable",
            "available_on_demand": False,
            "drawer_contract": None,
            "kind": None,
            "position": None,
            "responsive_profile": None,
            "box": None,
            "stage_edge_clearance_applicable": False,
            "stage_edge_clearances_px": None,
            "minimum_stage_edge_clearance_px": None,
            "stage_edge_clearance_passed": None,
            "height_stage_ratio": 0.0,
            "width_stage_ratio": 0.0,
            "area_stage_ratio": 0.0,
            "within_stage_coverage": True,
            "compact_kind_cue": "not_applicable",
            "compact_kind_cue_required": False,
            "compact_kind_cue_required_css": [],
            "compact_kind_cue_missing_css": [],
            "compact_kind_cue_preserved": None,
            "raw_collision_count": 0,
            "raw_collision_ids": [],
            "spatial_suppressed_count": 0,
            "spatial_suppressed_ids": [],
            "residual_collision_count": 0,
            "residual_collision_ids": [],
            "suppressed_labels_missing_from_focus_key": [],
            "suppressed_labels_covered_by_focus_key": True,
            "viewport_clipped": False,
            "masthead_clipped": False,
            "transport_clipped": False,
            "stage_clipped": False,
            "candidate_positions": [],
            "zero_residual_collision_candidate_positions": [],
            "risk_flags": [],
        }

    if viewport["id"] == PORTRAIT_VIEWPORT_ID:
        drawer_contract = course_runtime.portrait_teaching_drawer_contract()
        cue_contract = course_runtime.compact_kind_cue_contract(
            annotation["kind"], "narrow"
        )
        candidate_positions = [
            {
                "position": position,
                "status": "not_applicable_portrait_drawer",
                "responsive_profile": "portrait_drawer",
                "box": None,
                "raw_collision_count": 0,
                "raw_collision_ids": [],
                "spatial_suppressed_count": 0,
                "spatial_suppressed_ids": [],
                "residual_collision_count": 0,
                "residual_collision_ids": [],
                "suppressed_labels_missing_from_focus_key": [],
                "suppressed_labels_covered_by_focus_key": True,
                "viewport_clipped": False,
                "masthead_clipped": False,
                "transport_clipped": False,
                "stage_clipped": False,
                "passed": True,
            }
            for position in ("left", "right", "top-left", "top-right")
        ]
        return {
            "present": True,
            "initially_visible": False,
            "interaction_mode": "portrait_toggle_drawer",
            "available_on_demand": drawer_contract["passed"],
            "drawer_contract": drawer_contract,
            "kind": annotation["kind"],
            "position": annotation["position"],
            "responsive_profile": "portrait_drawer",
            "box": None,
            "stage_edge_clearance_applicable": False,
            "stage_edge_clearances_px": None,
            "minimum_stage_edge_clearance_px": None,
            "stage_edge_clearance_passed": None,
            "height_stage_ratio": 0.0,
            "width_stage_ratio": 0.0,
            "area_stage_ratio": 0.0,
            "within_stage_coverage": True,
            "compact_kind_cue": cue_contract["cue"],
            "compact_kind_cue_required": cue_contract["required"],
            "compact_kind_cue_required_css": cue_contract["required_css"],
            "compact_kind_cue_missing_css": cue_contract["missing_css"],
            "compact_kind_cue_preserved": cue_contract["preserved"],
            "raw_collision_count": 0,
            "raw_collision_ids": [],
            "spatial_suppressed_count": 0,
            "spatial_suppressed_ids": [],
            "residual_collision_count": 0,
            "residual_collision_ids": [],
            "suppressed_labels_missing_from_focus_key": [],
            "suppressed_labels_covered_by_focus_key": True,
            "viewport_clipped": False,
            "masthead_clipped": False,
            "transport_clipped": False,
            "stage_clipped": False,
            "candidate_positions": candidate_positions,
            "zero_residual_collision_candidate_positions": [
                candidate["position"] for candidate in candidate_positions
            ],
            "risk_flags": [],
        }

    viewport_box = _box(
        0.0,
        0.0,
        float(viewport["width"]),
        float(viewport["height"]),
    )
    stage_box = _box(
        float(stage["x"]),
        float(stage["y"]),
        float(stage["width"]),
        float(stage["height"]),
    )
    masthead_box = _box(
        float(stage["x"]),
        0.0,
        float(stage["width"]),
        float(stage["y"]),
    )
    transport_y = stage["y"] + stage["height"]
    transport_box = _box(
        float(stage["x"]),
        float(transport_y),
        float(stage["width"]),
        float(viewport["height"]) - transport_y,
    )

    def evaluate_position(position: str) -> dict[str, Any]:
        candidate_annotation = {**annotation, "position": position}
        candidate_box, candidate_profile = _teaching_overlay_box(
            candidate_annotation,
            viewport,
            stage,
            standard_width_px=standard_width_px,
            segment_id=segment["segment_id"],
        )
        raw_collision_ids = sorted(
            item["id"]
            for item in selected_label_boxes
            if _boxes_intersect(candidate_box, item["box"], gap=4.0)
        )
        spatial_suppressed_ids = raw_collision_ids
        residual_collision_ids: list[str] = []
        missing_from_focus_key = sorted(
            set(spatial_suppressed_ids) - set(focus_key_ids)
        )
        candidate_viewport_clipped = not _box_is_contained(candidate_box, viewport_box)
        candidate_masthead_clipped = _boxes_intersect(candidate_box, masthead_box)
        candidate_transport_clipped = _boxes_intersect(candidate_box, transport_box)
        candidate_stage_clipped = not _box_is_contained(candidate_box, stage_box)
        candidate_edge_clearances = _stage_edge_clearances(stage_box, candidate_box)
        candidate_minimum_clearance = min(candidate_edge_clearances.values())
        candidate_clearance_passed = (
            candidate_minimum_clearance >= MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
        )
        return {
            "position": position,
            "responsive_profile": candidate_profile,
            "box": candidate_box,
            "raw_collision_count": len(raw_collision_ids),
            "raw_collision_ids": raw_collision_ids,
            "spatial_suppressed_count": len(spatial_suppressed_ids),
            "spatial_suppressed_ids": spatial_suppressed_ids,
            "residual_collision_count": len(residual_collision_ids),
            "residual_collision_ids": residual_collision_ids,
            "suppressed_labels_missing_from_focus_key": missing_from_focus_key,
            "suppressed_labels_covered_by_focus_key": not missing_from_focus_key,
            "viewport_clipped": candidate_viewport_clipped,
            "masthead_clipped": candidate_masthead_clipped,
            "transport_clipped": candidate_transport_clipped,
            "stage_clipped": candidate_stage_clipped,
            "stage_edge_clearances_px": candidate_edge_clearances,
            "minimum_stage_edge_clearance_px": candidate_minimum_clearance,
            "stage_edge_clearance_passed": candidate_clearance_passed,
            "passed": (
                not residual_collision_ids
                and not missing_from_focus_key
                and not candidate_stage_clipped
                and candidate_clearance_passed
            ),
        }

    candidate_positions = [
        evaluate_position(position)
        for position in ("left", "right", "top-left", "top-right")
    ]
    current = next(
        candidate
        for candidate in candidate_positions
        if candidate["position"] == annotation["position"]
    )
    overlay_box = current["box"]
    profile = current["responsive_profile"]
    raw_collision_ids = current["raw_collision_ids"]
    spatial_suppressed_ids = current["spatial_suppressed_ids"]
    residual_collision_ids = current["residual_collision_ids"]
    missing_from_focus_key = current["suppressed_labels_missing_from_focus_key"]
    viewport_clipped = current["viewport_clipped"]
    masthead_clipped = current["masthead_clipped"]
    transport_clipped = current["transport_clipped"]
    stage_clipped = current["stage_clipped"]
    stage_edge_clearances = current["stage_edge_clearances_px"]
    minimum_stage_edge_clearance = current["minimum_stage_edge_clearance_px"]
    stage_edge_clearance_passed = current["stage_edge_clearance_passed"]
    height_stage_ratio = _round(overlay_box["height"] / stage["height"])
    width_stage_ratio = _round(overlay_box["width"] / stage["width"])
    area_stage_ratio = _round(height_stage_ratio * width_stage_ratio)
    within_stage_coverage = area_stage_ratio <= MAX_OVERLAY_STAGE_AREA_RATIO and (
        width_stage_ratio < 0.8 or height_stage_ratio <= MAX_OVERLAY_STAGE_HEIGHT_RATIO
    )
    cue_contract = course_runtime.compact_kind_cue_contract(annotation["kind"], profile)
    risk_flags = []
    if residual_collision_ids:
        risk_flags.append("overlay_residual_label_collision")
    if missing_from_focus_key:
        risk_flags.append("overlay_suppression_focus_key_gap")
    if viewport_clipped:
        risk_flags.append("overlay_viewport_clipping")
    if masthead_clipped:
        risk_flags.append("overlay_masthead_clipping")
    if transport_clipped:
        risk_flags.append("overlay_transport_clipping")
    if stage_clipped and not (masthead_clipped or transport_clipped):
        risk_flags.append("overlay_stage_clipping")
    if not stage_edge_clearance_passed:
        risk_flags.append("overlay_stage_edge_clearance")
    if not within_stage_coverage:
        risk_flags.append("overlay_stage_dominance")
    return {
        "present": True,
        "initially_visible": False,
        "interaction_mode": "toggle_overlay",
        "available_on_demand": True,
        "drawer_contract": None,
        "kind": annotation["kind"],
        "position": annotation["position"],
        "responsive_profile": profile,
        "box": overlay_box,
        "stage_edge_clearance_applicable": True,
        "stage_edge_clearances_px": stage_edge_clearances,
        "minimum_stage_edge_clearance_px": minimum_stage_edge_clearance,
        "stage_edge_clearance_passed": stage_edge_clearance_passed,
        "height_stage_ratio": height_stage_ratio,
        "width_stage_ratio": width_stage_ratio,
        "area_stage_ratio": area_stage_ratio,
        "within_stage_coverage": within_stage_coverage,
        "compact_kind_cue": cue_contract["cue"],
        "compact_kind_cue_required": cue_contract["required"],
        "compact_kind_cue_required_css": cue_contract["required_css"],
        "compact_kind_cue_missing_css": cue_contract["missing_css"],
        "compact_kind_cue_preserved": cue_contract["preserved"],
        "raw_collision_count": len(raw_collision_ids),
        "raw_collision_ids": raw_collision_ids,
        "spatial_suppressed_count": len(spatial_suppressed_ids),
        "spatial_suppressed_ids": spatial_suppressed_ids,
        "residual_collision_count": len(residual_collision_ids),
        "residual_collision_ids": residual_collision_ids,
        "suppressed_labels_missing_from_focus_key": missing_from_focus_key,
        "suppressed_labels_covered_by_focus_key": not missing_from_focus_key,
        "viewport_clipped": viewport_clipped,
        "masthead_clipped": masthead_clipped,
        "transport_clipped": transport_clipped,
        "stage_clipped": stage_clipped,
        "candidate_positions": candidate_positions,
        "zero_residual_collision_candidate_positions": [
            candidate["position"]
            for candidate in candidate_positions
            if candidate["passed"]
        ],
        "risk_flags": sorted(risk_flags),
    }


def _teaching_overlay_stage_edge_clearance_gate(
    segments: Sequence[dict[str, Any]],
    *,
    expected_annotated_segment_ids: Sequence[str] | None = None,
) -> dict[str, Any]:
    """Require exact modeled stage-edge clearance for every authored annotation."""
    source_contract = course_runtime.teaching_overlay_stage_edge_clearance_contract()
    source_contract_passed = (
        source_contract["passed"]
        and source_contract["minimum_stage_edge_clearance_px"]
        == MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
        and source_contract["minimum_item_font_px"] >= MIN_SPATIAL_LABEL_FONT_PX
    )
    annotated_segments = [
        segment
        for segment in segments
        if segment["quality_vector"]["annotation_coverage"]["item_count"] > 0
    ]
    annotated_segment_ids = [segment["segment_id"] for segment in annotated_segments]
    required_annotated_segment_ids = (
        annotated_segment_ids
        if expected_annotated_segment_ids is None
        else list(expected_annotated_segment_ids)
    )
    required_annotated_segment_count = len(required_annotated_segment_ids)
    segments_by_id = {segment["segment_id"]: segment for segment in segments}
    expected_viewport_ids = [str(viewport["id"]) for viewport in VIEWPORTS]
    expected_pairs = {
        (segment_id, viewport_id)
        for segment_id in required_annotated_segment_ids
        for viewport_id in expected_viewport_ids
    }
    observed_pairs: list[tuple[str, str]] = []
    records = []
    evaluation_failures = []
    observed_nonportrait_clearances = []
    observed_nonportrait_top_clearances = []
    observed_short_top_clearances = []
    viewport_sequence_mismatch_ids = []

    for segment_id in required_annotated_segment_ids:
        segment = segments_by_id.get(segment_id)
        evaluations = (
            [] if segment is None else segment["quality_vector"]["viewport_evaluations"]
        )
        viewport_ids = [str(evaluation["viewport_id"]) for evaluation in evaluations]
        if viewport_ids != expected_viewport_ids:
            viewport_sequence_mismatch_ids.append(segment_id)
        observed_pairs.extend((segment_id, viewport_id) for viewport_id in viewport_ids)
        evaluations_by_viewport = {
            str(evaluation["viewport_id"]): evaluation for evaluation in evaluations
        }
        for viewport_id in expected_viewport_ids:
            evaluation = evaluations_by_viewport.get(viewport_id)
            reasons = []
            applicable = viewport_id != PORTRAIT_VIEWPORT_ID
            edge_clearances = None
            minimum_clearance = None
            overlay = None if evaluation is None else evaluation.get("teaching_overlay")
            if evaluation is None:
                reasons.append("annotated_viewport_evaluation_missing")
            if not isinstance(overlay, dict):
                reasons.append("teaching_overlay_missing")
            elif not overlay.get("present"):
                reasons.append("authored_annotation_overlay_missing")
            elif not applicable:
                if overlay.get("interaction_mode") != "portrait_toggle_drawer":
                    reasons.append("portrait_drawer_mode_missing")
                if overlay.get("responsive_profile") != "portrait_drawer":
                    reasons.append("portrait_drawer_profile_missing")
                if overlay.get("box") is not None:
                    reasons.append("portrait_drawer_must_not_use_overlay_box")
                if overlay.get("stage_edge_clearance_applicable") is not False:
                    reasons.append("portrait_clearance_must_be_not_applicable")
                if overlay.get("stage_edge_clearance_passed") is not None:
                    reasons.append("portrait_clearance_result_must_be_null")
            else:
                box = overlay.get("box")
                stage = None if evaluation is None else evaluation.get("stage")
                if not isinstance(box, dict) or not isinstance(stage, dict):
                    reasons.append("nonportrait_overlay_box_or_stage_missing")
                else:
                    edge_clearances = _stage_edge_clearances(stage, box)
                    minimum_clearance = min(edge_clearances.values())
                    observed_nonportrait_clearances.append(minimum_clearance)
                    observed_nonportrait_top_clearances.append(edge_clearances["top"])
                    if viewport_id == SHORT_VIEWPORT_ID:
                        observed_short_top_clearances.append(edge_clearances["top"])
                    if overlay.get("stage_edge_clearance_applicable") is not True:
                        reasons.append("nonportrait_clearance_not_applicable")
                    if overlay.get("stage_edge_clearances_px") != edge_clearances:
                        reasons.append("modeled_edge_clearances_drifted")
                    if overlay.get("minimum_stage_edge_clearance_px") != (
                        minimum_clearance
                    ):
                        reasons.append("modeled_minimum_clearance_drifted")
                    if minimum_clearance < (
                        MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
                    ):
                        reasons.append("stage_edge_clearance_below_minimum")
                    if overlay.get("stage_edge_clearance_passed") != (
                        minimum_clearance
                        >= MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
                    ):
                        reasons.append("modeled_clearance_result_drifted")
            record = {
                "segment_id": segment_id,
                "viewport_id": viewport_id,
                "applicable": applicable,
                "status": (
                    "failed"
                    if reasons
                    else ("passed" if applicable else "not_applicable_portrait_drawer")
                ),
                "required_minimum_clearance_px": (
                    MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
                ),
                "stage_edge_clearances_px": edge_clearances,
                "minimum_stage_edge_clearance_px": minimum_clearance,
                "failure_reasons": reasons,
                "passed": not reasons,
            }
            records.append(record)
            if reasons:
                evaluation_failures.append(record)

    observed_pair_set = set(observed_pairs)
    coverage_failure_reasons = []
    if not source_contract_passed:
        coverage_failure_reasons.append("stage_edge_clearance_source_contract_failed")
    if annotated_segment_ids != required_annotated_segment_ids:
        coverage_failure_reasons.append("annotated_segment_ids_mismatch")
    if len(required_annotated_segment_ids) != len(set(required_annotated_segment_ids)):
        coverage_failure_reasons.append("duplicate_expected_annotated_segment_ids")
    if viewport_sequence_mismatch_ids:
        coverage_failure_reasons.append("viewport_sequence_mismatch")
    if len(observed_pairs) != len(observed_pair_set):
        coverage_failure_reasons.append("duplicate_segment_viewport_evaluations")
    if observed_pair_set != expected_pairs:
        coverage_failure_reasons.append("segment_viewport_pair_coverage_mismatch")
    if len(records) != required_annotated_segment_count * len(VIEWPORTS):
        coverage_failure_reasons.append("evaluation_count_mismatch")
    exact_coverage_passed = not coverage_failure_reasons
    coverage_failures = (
        []
        if not coverage_failure_reasons
        else [
            {
                "segment_id": None,
                "viewport_id": None,
                "failure_reasons": coverage_failure_reasons,
            }
        ]
    )
    failures = [*evaluation_failures, *coverage_failures]
    passed = exact_coverage_passed and not evaluation_failures
    return {
        "passed": passed,
        "status": (
            "not_applicable"
            if not annotated_segment_ids and passed
            else ("passed" if passed else "failed")
        ),
        "evidence_scope": "deterministic_static_model_not_live_browser",
        "scope": "all_annotated_segments_all_viewports",
        "required_minimum_clearance_px": (MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX),
        "annotated_segment_count": len(annotated_segment_ids),
        "expected_annotated_segment_count": required_annotated_segment_count,
        "annotated_segment_ids": annotated_segment_ids,
        "expected_annotated_segment_ids": required_annotated_segment_ids,
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": len(records),
        "expected_evaluation_count": required_annotated_segment_count * len(VIEWPORTS),
        "applicable_nonportrait_evaluation_count": sum(
            record["applicable"] for record in records
        ),
        "portrait_not_applicable_evaluation_count": sum(
            not record["applicable"] for record in records
        ),
        "portrait_policy": "explicit_not_applicable_drawer",
        "exact_coverage_required": True,
        "exact_coverage_passed": exact_coverage_passed,
        "coverage_failure_reasons": coverage_failure_reasons,
        "viewport_sequence_mismatch_segment_ids": viewport_sequence_mismatch_ids,
        "minimum_observed_clearance_px": min(
            observed_nonportrait_clearances,
            default=None,
        ),
        "minimum_observed_top_clearance_px": min(
            observed_nonportrait_top_clearances,
            default=None,
        ),
        "minimum_observed_short_top_clearance_px": min(
            observed_short_top_clearances,
            default=None,
        ),
        "source_contract": source_contract,
        "evaluations": records,
        "failure_count": len(failures),
        "failures": failures,
    }


def _opened_teaching_overlay(overlay: dict[str, Any]) -> dict[str, Any]:
    """Return the same authored overlay in its user-requested open state."""
    return {
        **overlay,
        "initially_visible": overlay["present"] and overlay["box"] is not None,
    }


def _map_label_specs(
    course: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
) -> dict[str, dict[str, Any]]:
    evidence = ledgers[course["meta"]["master_evidence_ledger"]]
    labels: dict[str, dict[str, Any]] = {}
    resolved_copy: dict[str, str] = {}

    def add(
        copy_id: str,
        at: Sequence[float],
        *,
        size: float,
        anchor: str = "middle",
        legend: bool = False,
    ) -> None:
        if copy_id in labels:
            raise QualityError(f"duplicate rendered map label {copy_id!r}")
        text = layout_pipeline.resolve_copy(
            master, evidence, copy_id, include_hidden=True
        )
        if text is None:
            raise QualityError(f"map label {copy_id!r} has no resolvable copy")
        width = max(size * 1.5, len(text) * size * 0.56)
        height = size * 1.25
        x, y = (float(value) for value in at)
        if anchor == "start":
            x0, x1 = x, x + width
        elif anchor == "end":
            x0, x1 = x - width, x
        elif anchor == "middle":
            x0, x1 = x - width / 2, x + width / 2
        else:
            raise QualityError(f"map label {copy_id!r}: unsupported anchor {anchor!r}")
        labels[copy_id] = {
            "at": (x, y),
            "anchor": anchor,
            "bbox": (x0, y - height, x1, y),
            "base_visible": master["copy"][copy_id].get("base_visible", True),
            "legend": legend,
        }
        resolved_copy[copy_id] = text

    ground = float(layout["frame"]["ground"])
    for zone in layout.get("zones") or []:
        add(zone["copy_id"], (zone["x"], ground + 28), size=10.5)
    for region in layout.get("regions") or []:
        if "copy_id" in region:
            add(region["copy_id"], region["label_at"], size=11.0)
    for label in layout.get("room_labels") or []:
        add(
            label["id"],
            label["at"],
            size=float(label.get("size", 10.5)),
            anchor=label.get("anchor", "middle"),
        )
    for label in layout.get("labels") or []:
        default_size = 10.5 if label.get("kind", "label") == "note" else 12.5
        add(
            label["id"],
            label["at"],
            size=float(label.get("size", default_size)),
            anchor=label.get("anchor", "middle"),
        )
    legend = layout.get("legend")
    if legend:
        x, y = legend["at"]
        add(
            legend["title_id"],
            (x, y),
            size=12.5,
            anchor="start",
            legend=True,
        )
        for index, entry in enumerate(legend["entries"]):
            add(
                entry["id"],
                (x + 54, y + 24 + index * 22),
                size=10.5,
                anchor="start",
                legend=True,
            )
    unclamped_bounds = shots.two_dimensional_label_bounds(layout, resolved_copy)
    if set(unclamped_bounds) != set(labels):
        raise QualityError("rendered 2D label bounds must cover every map label")
    for copy_id, spec in labels.items():
        spec["unclamped_bbox"] = unclamped_bounds[copy_id]["bbox"]
    return labels


def _focus_points_2d(
    segment: dict[str, Any],
    layout: dict[str, Any],
    edge_records: dict[str, dict[str, Any]],
    geoms: dict[str, layout_pipeline.Geom],
) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for node_id in segment["focus_nodes"]:
        points.extend(shots._layout_node_points(node_id, layout))
    for edge_id in segment["focus_edges"]:
        points.extend(shots._layout_edge_points(edge_id, layout, edge_records, geoms))
    return points


def _focus_marker_offsets(alignment: str) -> list[tuple[float, float]]:
    if alignment not in {"start", "middle", "end"}:
        raise QualityError(f"unsupported focus-marker anchor alignment {alignment!r}")
    step = FOCUS_MARKER_STEP_PX
    offsets = [
        (x * step, y * step)
        for x in range(-2, 3)
        for y in range(-2, 3)
        if math.hypot(x * step, y * step) <= MAX_FOCUS_MARKER_DISPLACEMENT_PX
    ]
    offsets.sort(
        key=lambda item: (
            item[0] ** 2 + item[1] ** 2,
            item[1],
            abs(item[0]),
            -item[0] if alignment == "start" else item[0],
        )
    )
    return offsets


def _place_numbered_focus_markers(
    anchor_by_id: dict[str, tuple[float, float]],
    fallback_ids: Sequence[str],
    stage: dict[str, int],
    overlay_box: dict[str, float] | None,
    visible_label_boxes: Sequence[dict[str, Any]] = (),
    alignment_by_id: Mapping[str, str] | None = None,
) -> dict[str, Any]:
    marker_size = FOCUS_MARKER_SIZE_PX
    alignment_by_id = alignment_by_id or {}
    stage_inset = _box(
        stage["x"] + 5.0,
        stage["y"] + 5.0,
        stage["width"] - 10.0,
        stage["height"] - 10.0,
    )
    placed_boxes: list[dict[str, float]] = []
    placed_leaders: list[tuple[tuple[float, float], tuple[float, float], str]] = []
    marker_ids: list[str] = []
    missing_ids: list[str] = []
    displaced_ids: list[str] = []
    anchor_covered_ids: list[str] = []
    leader_overlay_crossing_ids: list[str] = []
    visible_label_collision_ids: list[str] = []
    leader_visible_label_crossing_ids: list[str] = []
    leader_marker_crossing_ids: list[str] = []
    marker_leader_crossing_ids: list[str] = []
    leader_leader_crossing_ids: list[str] = []
    anchor_covered_by_prior_marker_ids: list[str] = []
    future_anchor_obstruction_ids: list[str] = []
    over_maximum_displacement_ids: list[str] = []
    placement_records: list[dict[str, Any]] = []
    for index, copy_id in enumerate(fallback_ids):
        anchor = anchor_by_id.get(copy_id)
        if anchor is None:
            missing_ids.append(copy_id)
            continue
        anchor_box = _box(anchor[0], anchor[1], 0.0, 0.0)
        if any(_boxes_intersect(anchor_box, box, gap=1.0) for box in placed_boxes):
            anchor_covered_by_prior_marker_ids.append(copy_id)
        if overlay_box is not None and _boxes_intersect(anchor_box, overlay_box):
            anchor_covered_ids.append(copy_id)
        future_anchors = [
            (future_id, anchor_by_id[future_id])
            for future_id in fallback_ids[index + 1 :]
            if future_id in anchor_by_id
        ]
        selected: tuple[dict[str, float], float, float] | None = None
        for dx, dy in _focus_marker_offsets(alignment_by_id.get(copy_id, "middle")):
            x = anchor[0] + dx
            y = anchor[1] + dy
            box = _box(
                x - marker_size / 2, y - marker_size / 2, marker_size, marker_size
            )
            if not _box_is_contained(box, stage_inset):
                continue
            if overlay_box is not None and _boxes_intersect(box, overlay_box, gap=4.0):
                continue
            if overlay_box is not None and _segment_intersects_box(
                anchor, (x, y), overlay_box, gap=1.0
            ):
                continue
            if any(
                _boxes_intersect(box, item["box"], gap=3.0)
                or _segment_intersects_box(anchor, (x, y), item["box"], gap=1.0)
                for item in visible_label_boxes
            ):
                continue
            if any(
                _boxes_intersect(box, _box(future[0], future[1], 0.0, 0.0), gap=2.0)
                or _segment_intersects_box(
                    anchor,
                    (x, y),
                    _box(future[0], future[1], 0.0, 0.0),
                    gap=2.0,
                )
                for _, future in future_anchors
            ):
                continue
            if any(
                _boxes_intersect(box, other, gap=2.0)
                or _segment_intersects_box(anchor, (x, y), other, gap=1.0)
                for other in placed_boxes
            ):
                continue
            if any(
                _segment_intersects_box(start, end, box, gap=1.0)
                or (
                    math.hypot(dx, dy) > 1.0
                    and _segments_intersect(anchor, (x, y), start, end)
                )
                for start, end, _ in placed_leaders
            ):
                continue
            selected = (box, dx, dy)
            break
        if selected is None:
            missing_ids.append(copy_id)
            continue
        box, dx, dy = selected
        placed_boxes.append(box)
        marker_ids.append(copy_id)
        displacement = math.hypot(dx, dy)
        prior_leaders = list(placed_leaders)
        if displacement:
            displaced_ids.append(copy_id)
        if displacement > MAX_FOCUS_MARKER_DISPLACEMENT_PX:
            over_maximum_displacement_ids.append(copy_id)
        if overlay_box is not None and _segment_intersects_box(
            anchor,
            (anchor[0] + dx, anchor[1] + dy),
            overlay_box,
            gap=1.0,
        ):
            leader_overlay_crossing_ids.append(copy_id)
        collides_with = sorted(
            item["id"]
            for item in visible_label_boxes
            if _boxes_intersect(box, item["box"], gap=3.0)
        )
        if collides_with:
            visible_label_collision_ids.append(copy_id)
        leader_visible_collisions = sorted(
            item["id"]
            for item in visible_label_boxes
            if _segment_intersects_box(
                anchor,
                (anchor[0] + dx, anchor[1] + dy),
                item["box"],
                gap=1.0,
            )
        )
        if leader_visible_collisions:
            leader_visible_label_crossing_ids.append(copy_id)
        prior_marker_crossings = [
            marker_id
            for marker_id, marker_box in zip(marker_ids[:-1], placed_boxes[:-1])
            if _segment_intersects_box(
                anchor,
                (anchor[0] + dx, anchor[1] + dy),
                marker_box,
                gap=1.0,
            )
        ]
        if prior_marker_crossings:
            leader_marker_crossing_ids.append(copy_id)
        prior_leader_crossings = [
            leader_id
            for start, end, leader_id in prior_leaders
            if _segment_intersects_box(start, end, box, gap=1.0)
        ]
        if prior_leader_crossings:
            marker_leader_crossing_ids.append(copy_id)
        leader_leader_crossings = [
            leader_id
            for start, end, leader_id in prior_leaders
            if displacement
            and _segments_intersect(
                anchor,
                (anchor[0] + dx, anchor[1] + dy),
                start,
                end,
            )
        ]
        if leader_leader_crossings:
            leader_leader_crossing_ids.append(copy_id)
        if displacement:
            placed_leaders.append((anchor, (anchor[0] + dx, anchor[1] + dy), copy_id))
        obstructed_future_ids = sorted(
            future_id
            for future_id, future in future_anchors
            if _boxes_intersect(box, _box(future[0], future[1], 0.0, 0.0), gap=2.0)
            or _segment_intersects_box(
                anchor,
                (anchor[0] + dx, anchor[1] + dy),
                _box(future[0], future[1], 0.0, 0.0),
                gap=2.0,
            )
        )
        if obstructed_future_ids:
            future_anchor_obstruction_ids.append(copy_id)
        placement_records.append(
            {
                "id": copy_id,
                "anchor": {"x": _round(anchor[0]), "y": _round(anchor[1])},
                "marker": {
                    "x": _round(anchor[0] + dx),
                    "y": _round(anchor[1] + dy),
                },
                "displacement_px": _round(displacement),
                "visible_label_collision_ids": collides_with,
                "leader_visible_label_collision_ids": leader_visible_collisions,
                "leader_prior_marker_collision_ids": prior_marker_crossings,
                "marker_prior_leader_collision_ids": prior_leader_crossings,
                "leader_prior_leader_collision_ids": leader_leader_crossings,
                "obstructed_future_anchor_ids": obstructed_future_ids,
            }
        )
    maximum_displacement = max(
        (record["displacement_px"] for record in placement_records), default=0.0
    )
    return {
        "fallback_ids": list(fallback_ids),
        "marker_ids": marker_ids,
        "missing_marker_ids": missing_ids,
        "displaced_marker_ids": displaced_ids,
        "marker_count": len(marker_ids),
        "marker_size_px": marker_size,
        "leader_count": len(displaced_ids),
        "maximum_allowed_displacement_px": MAX_FOCUS_MARKER_DISPLACEMENT_PX,
        "maximum_displacement_px": maximum_displacement,
        "anchor_covered_by_overlay_ids": sorted(anchor_covered_ids),
        "leader_overlay_crossing_ids": sorted(leader_overlay_crossing_ids),
        "visible_label_collision_ids": sorted(visible_label_collision_ids),
        "leader_visible_label_crossing_ids": sorted(leader_visible_label_crossing_ids),
        "leader_marker_crossing_ids": sorted(leader_marker_crossing_ids),
        "marker_leader_crossing_ids": sorted(marker_leader_crossing_ids),
        "leader_leader_crossing_ids": sorted(leader_leader_crossing_ids),
        "anchor_covered_by_prior_marker_ids": sorted(
            anchor_covered_by_prior_marker_ids
        ),
        "future_anchor_obstruction_ids": sorted(future_anchor_obstruction_ids),
        "over_maximum_displacement_ids": sorted(over_maximum_displacement_ids),
        "placements": placement_records,
        "passed": not (
            missing_ids
            or anchor_covered_ids
            or leader_overlay_crossing_ids
            or visible_label_collision_ids
            or leader_visible_label_crossing_ids
            or leader_marker_crossing_ids
            or marker_leader_crossing_ids
            or leader_leader_crossing_ids
            or anchor_covered_by_prior_marker_ids
            or future_anchor_obstruction_ids
            or over_maximum_displacement_ids
        ),
    }


def _focused_geometry_stroke_evaluation(
    segment: dict[str, Any],
    viewport: dict[str, int | str],
    layout: dict[str, Any],
    master: dict[str, Any],
    scale: float,
    source_contract: dict[str, Any],
) -> dict[str, Any]:
    """Model focused map strokes after the runtime's responsive SVG transform."""
    node_by_id = {node["id"]: node for node in master["nodes"]}
    edge_by_id = {edge["id"]: edge for edge in master["edges"]}
    records = []
    missing_geometry_ids = []

    def add_record(
        geometry_id: str,
        geometry_kind: str,
        lifecycle: str,
        authored_stroke_px: float,
    ) -> None:
        dash_text = layout_pipeline.LIFECYCLE_STYLE.get(lifecycle, (None, 1.0))[0]
        dash_values = (
            [] if dash_text is None else [float(value) for value in dash_text.split()]
        )
        non_scaling = source_contract["passed"]
        effective_stroke = (
            authored_stroke_px if non_scaling else authored_stroke_px * scale
        )
        effective_dash = [
            value if non_scaling else value * scale for value in dash_values
        ]
        minimum_dash = min(effective_dash, default=None)
        stroke_passed = effective_stroke + 0.000001 >= MIN_FOCUSED_GEOMETRY_STROKE_PX
        dash_passed = minimum_dash is None or (
            minimum_dash + 0.000001 >= MIN_FOCUSED_GEOMETRY_DASH_PX
        )
        records.append(
            {
                "id": geometry_id,
                "kind": geometry_kind,
                "lifecycle": lifecycle,
                "authored_stroke_px": _round(authored_stroke_px),
                "effective_stroke_px": _round(effective_stroke),
                "dash_pattern": dash_text or "solid",
                "effective_dash_pattern_px": [
                    _round(value) for value in effective_dash
                ],
                "minimum_effective_dash_px": (
                    None if minimum_dash is None else _round(minimum_dash)
                ),
                "stroke_floor_passed": stroke_passed,
                "dash_floor_passed": dash_passed,
                "passed": stroke_passed and dash_passed,
            }
        )

    for node_id in segment["focus_nodes"]:
        node = node_by_id.get(node_id)
        if node is None or node_id not in layout["nodes"]:
            missing_geometry_ids.append(node_id)
            continue
        add_record(node_id, "node", node["lifecycle"], float(tokens.STROKE))
    for edge_id in segment["focus_edges"]:
        edge = edge_by_id.get(edge_id)
        edge_layout = layout["edges"].get(edge_id)
        if edge is None or edge_layout is None:
            missing_geometry_ids.append(edge_id)
            continue
        authored_stroke = (
            tokens.STROKE if edge_layout.get("w") == "thin" else tokens.STROKE_HEAVY
        )
        add_record(edge_id, "edge", edge["lifecycle"], float(authored_stroke))

    failure_reasons = []
    if not source_contract["passed"]:
        failure_reasons.append("focused_non_scaling_source_contract_failed")
    if missing_geometry_ids:
        failure_reasons.append("focused_geometry_missing_from_layout")
    if not records:
        failure_reasons.append("empty_focused_geometry")
    if any(not record["stroke_floor_passed"] for record in records):
        failure_reasons.append("effective_stroke_floor_failed")
    if any(not record["dash_floor_passed"] for record in records):
        failure_reasons.append("effective_dash_floor_failed")
    return {
        "passed": not failure_reasons,
        "evidence_scope": "deterministic_static_model_not_live_browser",
        "segment_id": segment["segment_id"],
        "viewport_id": viewport["id"],
        "scale_without_non_scaling_stroke": _round(scale),
        "non_scaling_stroke_applied": source_contract["passed"],
        "minimum_required_stroke_px": MIN_FOCUSED_GEOMETRY_STROKE_PX,
        "minimum_required_dash_px": MIN_FOCUSED_GEOMETRY_DASH_PX,
        "focused_node_count": len(segment["focus_nodes"]),
        "focused_edge_count": len(segment["focus_edges"]),
        "geometry_count": len(records),
        "dashed_geometry_count": sum(
            record["dash_pattern"] != "solid" for record in records
        ),
        "minimum_effective_stroke_px": min(
            (record["effective_stroke_px"] for record in records),
            default=None,
        ),
        "minimum_effective_dash_px": min(
            (
                record["minimum_effective_dash_px"]
                for record in records
                if record["minimum_effective_dash_px"] is not None
            ),
            default=None,
        ),
        "missing_geometry_ids": sorted(missing_geometry_ids),
        "records": records,
        "failure_reasons": failure_reasons,
    }


def _map_evaluation(
    segment: dict[str, Any],
    viewport: dict[str, int | str],
    stage: dict[str, int],
    layout: dict[str, Any],
    master: dict[str, Any],
    label_specs: dict[str, dict[str, Any]],
    focus_points: list[tuple[float, float]],
    focused_stroke_contract: dict[str, Any],
) -> dict[str, Any]:
    compact_view = segment["frame"].get("compact_viewBox")
    compact_frame_active = (
        compact_view is not None
        and segment["visual"]["label_policy"] == "focus"
        and shots.spatial_labels_require_fixed_key(
            stage["width"], stage["height"]
        )
    )
    active_view = compact_view if compact_frame_active else segment["frame"]["viewBox"]
    view_x, view_y, view_width, view_height = (
        float(value) for value in active_view
    )
    view_bbox = (view_x, view_y, view_x + view_width, view_y + view_height)
    label_view_x, label_view_y, label_view_width, label_view_height = (
        float(value) for value in segment["frame"]["viewBox"]
    )
    label_view_bbox = (
        label_view_x,
        label_view_y,
        label_view_x + label_view_width,
        label_view_y + label_view_height,
    )
    visual = segment["visual"]
    reveal_copy_ids = set(segment["reveal_copy_ids"])
    selected_copy_ids = set(visual["label_copy_ids"]) | reveal_copy_ids
    grammar_copy_ids = {
        copy_id
        for copy_id in selected_copy_ids
        if copy_id in course_runtime._LEGEND_GRAMMAR_CUES
    }
    rendered_selected_copy_ids = selected_copy_ids - grammar_copy_ids
    if visual["label_policy"] == "focus":
        framed_label_ids = sorted(rendered_selected_copy_ids)
    else:
        framed_label_id_set = {
            copy_id for copy_id, spec in label_specs.items() if spec["base_visible"]
        } | reveal_copy_ids
        legend_ids = {
            copy_id for copy_id, spec in label_specs.items() if spec["legend"]
        }
        framed_label_id_set -= legend_ids
        if visual["show_legend"]:
            framed_label_id_set |= legend_ids
        framed_label_ids = sorted(framed_label_id_set)
    unclamped_label_records = []
    unclamped_label_clipping_ids = []
    for copy_id in framed_label_ids:
        if copy_id not in label_specs:
            raise QualityError(
                f"segment {segment['segment_id']}: unknown rendered label {copy_id!r}"
            )
        x0, y0, x1, y1 = label_specs[copy_id]["unclamped_bbox"]
        margins = {
            "left": _round(x0 - label_view_bbox[0]),
            "top": _round(y0 - label_view_bbox[1]),
            "right": _round(label_view_bbox[2] - x1),
            "bottom": _round(label_view_bbox[3] - y1),
        }
        minimum_margin = min(margins.values())
        clipped = minimum_margin < -LABEL_FRAME_MARGIN_TOLERANCE
        if clipped:
            unclamped_label_clipping_ids.append(copy_id)
        unclamped_label_records.append(
            {
                "id": copy_id,
                "bbox": [_round(value) for value in (x0, y0, x1, y1)],
                "frame_margins": margins,
                "minimum_frame_margin_svg_units": minimum_margin,
                "clipped": clipped,
            }
        )
    minimum_label_frame_margin = min(
        (
            record["minimum_frame_margin_svg_units"]
            for record in unclamped_label_records
        ),
        default=None,
    )
    label_frame_margin_passed = (
        minimum_label_frame_margin is None
        or minimum_label_frame_margin + LABEL_FRAME_MARGIN_TOLERANCE
        >= shots.TWO_DIMENSIONAL_LABEL_SAFETY_MARGIN
    )
    all_focus_key_ids = []
    focus_key_ids = []
    if visual["label_policy"] == "focus":
        all_focus_key_ids = list(
            dict.fromkeys([*visual["label_copy_ids"], *segment["reveal_copy_ids"]])
        )
        focus_key_ids = [
            copy_id
            for copy_id in all_focus_key_ids
            if copy_id not in grammar_copy_ids
            and copy_id in label_specs
            and not label_specs[copy_id]["legend"]
        ]
    if int(viewport["width"]) <= 1100:
        horizontal_padding = vertical_padding = 20
    else:
        horizontal_padding = MAP_HORIZONTAL_PADDING
        vertical_padding = MAP_VERTICAL_PADDING
    standard_profile = int(viewport["width"]) >= 821 and int(viewport["height"]) >= 561
    standard_widths = (
        course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX
        if standard_profile and segment["visual"]["annotation"] is not None
        else (course_runtime.TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX,)
    )
    legacy_preliminary_overlay = _opened_teaching_overlay(
        _teaching_overlay_evaluation(
            segment,
            viewport,
            stage,
            [],
            focus_key_ids,
            standard_width_px=LEGACY_TEACHING_OVERLAY_STANDARD_WIDTH_PX,
        )
    )
    width_candidates = []
    for standard_width_px in standard_widths:
        candidate_overlay = _teaching_overlay_evaluation(
            segment,
            viewport,
            stage,
            [],
            focus_key_ids,
            standard_width_px=standard_width_px,
        )
        candidate_stage = _visual_stage_box(
            stage,
            _opened_teaching_overlay(candidate_overlay),
            view_box=active_view,
            horizontal_padding=horizontal_padding,
            vertical_padding=vertical_padding,
            legacy_overlay=legacy_preliminary_overlay,
        )
        width_candidates.append(
            {
                "standard_width_px": standard_width_px,
                "overlay": candidate_overlay,
                "visual_stage": candidate_stage,
                "rendered_pixel_area": candidate_stage.get("rendered_pixel_area", 0.0),
                "physical_area": candidate_stage.get("rendered_pixel_area", 0.0),
            }
        )
    chosen_width = _widest_maximum_physical_area_candidate(width_candidates)
    selected_standard_width_px = chosen_width["standard_width_px"]
    open_visual_stage = chosen_width["visual_stage"]
    open_visual_stage["selected_standard_overlay_width_px"] = selected_standard_width_px
    open_visual_stage["standard_overlay_width_candidates_px"] = list(standard_widths)
    open_visual_stage["standard_overlay_width_candidate_evaluations"] = [
        {
            "standard_width_px": candidate["standard_width_px"],
            "rendered_pixel_area": _round(candidate["rendered_pixel_area"]),
            "dock": candidate["visual_stage"].get("dock"),
        }
        for candidate in width_candidates
    ]
    if open_visual_stage.get("rendered_pixel_area") is not None:
        open_visual_stage["max_candidate_rendered_pixel_area"] = _round(
            max(candidate["rendered_pixel_area"] for candidate in width_candidates)
        )
        open_visual_stage["max_render_area_candidate_selected"] = True
    visual_stage = _visual_stage_box(
        stage,
        chosen_width["overlay"],
        view_box=active_view,
        horizontal_padding=horizontal_padding,
        vertical_padding=vertical_padding,
    )
    inner_width = max(1, visual_stage["width"] - horizontal_padding)
    inner_height = max(1, visual_stage["height"] - vertical_padding)
    scale = min(inner_width / view_width, inner_height / view_height)
    focused_geometry_strokes = _focused_geometry_stroke_evaluation(
        segment,
        viewport,
        layout,
        master,
        scale,
        focused_stroke_contract,
    )
    rendered_width = view_width * scale
    rendered_height = view_height * scale
    rendered_x = (
        visual_stage["x"] + horizontal_padding / 2 + (inner_width - rendered_width) / 2
    )
    rendered_y = (
        visual_stage["y"] + vertical_padding / 2 + (inner_height - rendered_height) / 2
    )
    focus_width, focus_height = _intersect_2d(_bbox_2d(focus_points), view_bbox)
    focus_pixels = focus_width * focus_height * scale * scale
    focus_occupancy = focus_pixels / float(visual_stage["pixel_count"])

    if visual["label_policy"] == "focus":
        allowed = rendered_selected_copy_ids | set(PROTECTED_MAP_COPY_IDS)
    else:
        allowed = {
            copy_id for copy_id, spec in label_specs.items() if spec["base_visible"]
        } | reveal_copy_ids
    legend_ids = {copy_id for copy_id, spec in label_specs.items() if spec["legend"]}
    allowed -= legend_ids
    if visual["show_legend"]:
        allowed |= legend_ids

    projected_base_font_px = MAP_BASE_FONT_PX * scale
    spatial_font_gate_applied = visual["label_policy"] == "focus"
    spatial_labels_readable = (
        not compact_frame_active
        and (
            not spatial_font_gate_applied
            or projected_base_font_px >= MIN_SPATIAL_LABEL_FONT_PX
        )
    )
    visible_label_count = 0
    selected_spatial_label_count = 0
    protected_spatial_label_count = 0
    legend_visible_label_count = 0
    estimated_label_pixels = 0.0
    selected_label_boxes: list[dict[str, Any]] = []
    marker_anchors: dict[str, tuple[float, float]] = {}
    for copy_id in sorted(allowed):
        if copy_id not in label_specs:
            raise QualityError(
                f"segment {segment['segment_id']}: unknown rendered label {copy_id!r}"
            )
        spec = label_specs[copy_id]
        if not spec["base_visible"] and copy_id not in reveal_copy_ids:
            continue
        if not spec["legend"] and copy_id in rendered_selected_copy_ids:
            marker_anchors[copy_id] = (
                rendered_x + (spec["at"][0] - view_x) * scale,
                rendered_y + (spec["at"][1] - view_y) * scale,
            )
        label_x0 = max(spec["bbox"][0], view_bbox[0])
        label_y0 = max(spec["bbox"][1], view_bbox[1])
        label_x1 = min(spec["bbox"][2], view_bbox[2])
        label_y1 = min(spec["bbox"][3], view_bbox[3])
        label_width = max(0.0, label_x1 - label_x0)
        label_height = max(0.0, label_y1 - label_y0)
        if not spec["legend"] and not spatial_labels_readable:
            continue
        if label_width > 0 and label_height > 0:
            visible_label_count += 1
            estimated_label_pixels += label_width * label_height * scale * scale
            if spec["legend"]:
                legend_visible_label_count += 1
            elif copy_id in rendered_selected_copy_ids:
                selected_spatial_label_count += 1
                selected_label_boxes.append(
                    {
                        "id": copy_id,
                        "box": _box(
                            rendered_x + (label_x0 - view_x) * scale,
                            rendered_y + (label_y0 - view_y) * scale,
                            label_width * scale,
                            label_height * scale,
                        ),
                    }
                )
            elif copy_id in PROTECTED_MAP_COPY_IDS:
                protected_spatial_label_count += 1

    overlay = _teaching_overlay_evaluation(
        segment,
        viewport,
        stage,
        selected_label_boxes,
        focus_key_ids,
        standard_width_px=selected_standard_width_px,
    )
    overlay["selected_standard_width_px"] = selected_standard_width_px
    suppressed_ids = (
        set(overlay["spatial_suppressed_ids"])
        if overlay["initially_visible"]
        else set()
    )
    for item in selected_label_boxes:
        item["spatially_suppressed_by_overlay"] = item["id"] in suppressed_ids
    suppressed_label_pixels = sum(
        item["box"]["width"] * item["box"]["height"]
        for item in selected_label_boxes
        if item["id"] in suppressed_ids
    )
    visible_label_count = max(0, visible_label_count - len(suppressed_ids))
    selected_spatial_label_count = max(
        0, selected_spatial_label_count - len(suppressed_ids)
    )
    estimated_label_pixels = max(0.0, estimated_label_pixels - suppressed_label_pixels)
    fallback_ids = (
        focus_key_ids
        if visual["label_policy"] == "focus" and not spatial_labels_readable
        else [copy_id for copy_id in focus_key_ids if copy_id in suppressed_ids]
    )
    visible_label_obstacles = [
        item for item in selected_label_boxes if item["id"] not in suppressed_ids
    ]
    geometry_correspondence = _place_numbered_focus_markers(
        marker_anchors,
        fallback_ids,
        visual_stage,
        overlay["box"] if overlay["initially_visible"] else None,
        visible_label_obstacles,
        {
            copy_id: label_specs[copy_id]["anchor"]
            for copy_id in fallback_ids
            if copy_id in label_specs
        },
    )

    focus_items = len(segment["focus_nodes"]) + len(segment["focus_edges"])
    density = focus_items / (visual_stage["pixel_count"] / 1_000_000)
    label_stage_ratio = estimated_label_pixels / float(visual_stage["pixel_count"])
    risk_flags = []
    if focus_items >= DENSE_FOCUS_MIN_ITEMS:
        risk_flags.append("dense_focus")
    if visible_label_count > MAX_VISIBLE_LABELS:
        risk_flags.append("visible_label_pressure")
    if label_stage_ratio > MAX_LABEL_STAGE_RATIO:
        risk_flags.append("label_area_pressure")
    if unclamped_label_clipping_ids:
        risk_flags.append("label_clipping")
    if focus_occupancy < MIN_FOCUS_OCCUPANCY:
        risk_flags.append("low_focus_occupancy")
    if not geometry_correspondence["passed"]:
        risk_flags.append("focus_key_geometry_correspondence_gap")
    if overlay["initially_visible"]:
        risk_flags.extend(overlay["risk_flags"])

    focus_key = {
        "chip_count": len(all_focus_key_ids),
        "chip_ids": all_focus_key_ids,
        "marker_eligible_chip_ids": focus_key_ids,
        "grammar_chip_ids": sorted(set(all_focus_key_ids) - set(focus_key_ids)),
        "font_px": FOCUS_KEY_FONT_PX,
        "numbered_geometry_correspondence": geometry_correspondence,
    }

    return {
        "viewport_id": viewport["id"],
        "viewport": {
            "width": int(viewport["width"]),
            "height": int(viewport["height"]),
        },
        "stage": stage,
        "visual_stage": visual_stage,
        "open_visual_stage": open_visual_stage,
        "focus_density_per_megapixel": _round(density),
        "visible_label_count": visible_label_count,
        "selected_label_boxes": selected_label_boxes,
        "teaching_overlay": overlay,
        "fixed_focus_key": focus_key,
        "fixed_boundary_note": {
            "copy_id": "footnote",
            "masthead_visible": True,
            "full_copy_accessible": True,
            "font_px": 10.0,
            "responsive_style": "full_exact"
            if int(viewport["width"]) > 1100
            else "compact_two_clause_visible_duplicate",
            "visible_clauses": ["source_gated", "teaching_reference_not_as_built"],
        },
        "two_dimensional": {
            "framed_label_ids": framed_label_ids,
            "unclamped_label_bounds": unclamped_label_records,
            "unclamped_label_clipping_count": len(unclamped_label_clipping_ids),
            "unclamped_label_clipping_ids": unclamped_label_clipping_ids,
            "minimum_label_frame_margin_svg_units": minimum_label_frame_margin,
            "required_label_frame_margin_svg_units": (
                shots.TWO_DIMENSIONAL_LABEL_SAFETY_MARGIN
            ),
            "label_frame_margin_tolerance_svg_units": (LABEL_FRAME_MARGIN_TOLERANCE),
            "label_frame_margin_passed": label_frame_margin_passed,
            "estimated_label_pixels": round(estimated_label_pixels),
            "label_stage_ratio": _round(label_stage_ratio),
            "rendered_pixel_area": _round(rendered_width * rendered_height),
            "rendered_pixel_ratio_to_full_stage": _round(
                rendered_width * rendered_height / float(stage["pixel_count"])
            ),
            "legacy_rendered_pixel_area": visual_stage.get(
                "legacy_rendered_pixel_area",
                _round(rendered_width * rendered_height),
            ),
            "legacy_rendered_pixel_ratio_to_full_stage": visual_stage.get(
                "legacy_rendered_pixel_ratio_to_full_stage",
                _round(rendered_width * rendered_height / float(stage["pixel_count"])),
            ),
            "rendered_pixel_area_retention_ratio": visual_stage.get(
                "rendered_pixel_area_retention_ratio", 1.0
            ),
            "max_candidate_rendered_pixel_area": visual_stage.get(
                "max_candidate_rendered_pixel_area",
                _round(rendered_width * rendered_height),
            ),
            "max_render_area_candidate_selected": visual_stage.get(
                "max_render_area_candidate_selected", True
            ),
            "focus_occupancy": _round(focus_occupancy),
            "spatial_label_count": visible_label_count - legend_visible_label_count,
            "selected_spatial_label_count": selected_spatial_label_count,
            "protected_spatial_label_count": protected_spatial_label_count,
            "legend_visible_label_count": legend_visible_label_count,
            "projected_base_font_px": _round(projected_base_font_px),
            "minimum_spatial_font_px": MIN_SPATIAL_LABEL_FONT_PX,
            "spatial_font_gate_applied": spatial_font_gate_applied,
            "spatial_labels_readable": spatial_labels_readable,
            "fixed_focus_key": focus_key,
            "focused_geometry_strokes": focused_geometry_strokes,
        },
        "risk_flags": sorted(risk_flags),
    }


def _subtract(left: Sequence[float], right: Sequence[float]) -> tuple[float, ...]:
    return tuple(float(a) - float(b) for a, b in zip(left, right, strict=True))


def _dot(left: Sequence[float], right: Sequence[float]) -> float:
    return sum(a * b for a, b in zip(left, right, strict=True))


def _cross(left: Sequence[float], right: Sequence[float]) -> tuple[float, ...]:
    return (
        left[1] * right[2] - left[2] * right[1],
        left[2] * right[0] - left[0] * right[2],
        left[0] * right[1] - left[1] * right[0],
    )


def _normalise(vector: Sequence[float]) -> tuple[float, ...]:
    length = math.sqrt(_dot(vector, vector))
    if not math.isfinite(length) or length <= 0:
        raise QualityError("cannot project with a zero-length camera vector")
    return tuple(value / length for value in vector)


def _project_point(
    point: Sequence[float],
    *,
    position: Sequence[float],
    right: Sequence[float],
    up: Sequence[float],
    forward: Sequence[float],
    aspect: float,
) -> tuple[float, float, bool] | None:
    relative = _subtract(point, position)
    depth = _dot(relative, forward)
    if depth <= CAMERA_NEAR or depth >= CAMERA_FAR:
        return None
    tangent = math.tan(math.radians(CAMERA_FOV_DEGREES) / 2)
    x = _dot(relative, right) / (depth * tangent * aspect)
    y = _dot(relative, up) / (depth * tangent)
    return x, y, abs(x) <= 1 and abs(y) <= 1


def _camera_basis(
    frame: dict[str, Any], aspect: float
) -> tuple[tuple[float, ...], ...]:
    authored_position = tuple(float(value) for value in frame["position"])
    target = tuple(float(value) for value in frame["target"])
    requested_up = tuple(float(value) for value in frame["up"])
    direction = _normalise(_subtract(authored_position, target))
    distance = shots._responsive_3d_distance(
        frame, aspect, vertical_fov_degrees=CAMERA_FOV_DEGREES
    )
    position = tuple(target[index] + direction[index] * distance for index in range(3))
    forward = _normalise(_subtract(target, position))
    right = _normalise(_cross(forward, requested_up))
    up = _normalise(_cross(right, forward))
    return position, right, up, forward


def _focus_points_3d(
    segment: dict[str, Any], scene: dict[str, Any]
) -> list[tuple[float, float, float]]:
    points: list[tuple[float, float, float]] = []
    for node_id in segment["focus_nodes"]:
        points.extend(shots._scene_node_points(node_id, scene))
    for edge_id in segment["focus_edges"]:
        points.extend(tuple(point) for point in scene["edges"][edge_id]["points"])
    return points


def _three_label_box_width(node: dict[str, Any]) -> float:
    label = node["label"]
    if type(label) is not str or not label:
        raise QualityError(
            f"3D spatial label {node['id']!r} must be a nonempty printable ASCII string"
        )
    try:
        label_width = (
            sum(
                THREE_LABEL_PRINTABLE_ASCII_ADVANCE_EM[character] for character in label
            )
            * THREE_LABEL_FONT_PX
        )
    except KeyError as error:
        raise QualityError(
            f"3D spatial label {node['id']!r} must be a nonempty printable ASCII string"
        ) from error
    return label_width + THREE_LABEL_BOX_CHROME_PX


def _place_three_label_boxes(
    labels: list[dict[str, Any]], stage: dict[str, int]
) -> tuple[list[dict[str, Any]], list[str]]:
    ordered = sorted(
        labels,
        key=lambda item: (
            item["box"]["x"],
            item["box"]["y"],
            item["id"],
        ),
    )
    offsets = [0.0]
    for step in range(1, len(ordered) + 1):
        offsets.extend((-40.0 * step, 40.0 * step))
    stage_top = float(stage["y"])
    stage_bottom = stage_top + float(stage["height"])
    stage_left = float(stage["x"])
    stage_right = stage_left + float(stage["width"])
    placed_boxes: list[dict[str, float]] = []
    placed: list[dict[str, Any]] = []
    suppressed_ids: list[str] = []
    for item in ordered:
        original = item["box"]
        selected_offset: float | None = None
        for offset in offsets:
            shifted = _box(
                original["x"],
                original["y"] + offset,
                original["width"],
                original["height"],
            )
            shifted_top = shifted["y"]
            shifted_bottom = shifted_top + shifted["height"]
            shifted_left = shifted["x"]
            shifted_right = shifted_left + shifted["width"]
            if (
                shifted_left < stage_left + 6.0
                or shifted_right > stage_right - 6.0
                or shifted_top < stage_top + 6.0
                or shifted_bottom > stage_bottom - 6.0
            ):
                continue
            if all(
                not _boxes_intersect(shifted, other, gap=5.0) for other in placed_boxes
            ):
                selected_offset = offset
                break
        if selected_offset is None:
            suppressed_ids.append(item["id"])
            continue
        final_box = _box(
            original["x"],
            original["y"] + selected_offset,
            original["width"],
            original["height"],
        )
        placed_boxes.append(final_box)
        placed.append(
            {
                "id": item["id"],
                "box": final_box,
                "vertical_collision_offset_px": _round(selected_offset),
            }
        )
    return sorted(placed, key=lambda item: item["id"]), sorted(suppressed_ids)


def _three_evaluation(
    segment: dict[str, Any],
    viewport: dict[str, int | str],
    stage: dict[str, int],
    node_records: dict[str, dict[str, Any]],
    scene: dict[str, Any],
    focus_points: list[tuple[float, float, float]],
) -> dict[str, Any]:
    visual = segment["visual"]
    focus_key_ids = [
        node_id
        for node_id in dict.fromkeys(visual["label_node_ids"])
        if node_id in node_records
    ]
    selected_standard_width_px = (
        course_runtime.TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX
    )
    preliminary_overlay = _teaching_overlay_evaluation(
        segment,
        viewport,
        stage,
        [],
        focus_key_ids,
        standard_width_px=selected_standard_width_px,
    )
    visual_stage = _visual_stage_box(stage, preliminary_overlay)
    open_visual_stage = dict(visual_stage)
    if visual["annotation"] is not None:
        standard_profile = (
            int(viewport["width"]) >= 821 and int(viewport["height"]) >= 561
        )
        standard_widths = (
            course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX
            if standard_profile
            else (course_runtime.TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX,)
        )
        legacy_overlay = _teaching_overlay_evaluation(
            segment,
            viewport,
            stage,
            [],
            focus_key_ids,
            standard_width_px=LEGACY_TEACHING_OVERLAY_STANDARD_WIDTH_PX,
        )
        legacy_stage = _visual_stage_box(
            stage,
            _opened_teaching_overlay(legacy_overlay),
        )
        width_candidates = []
        for standard_width_px in standard_widths:
            candidate_overlay = _teaching_overlay_evaluation(
                segment,
                viewport,
                stage,
                [],
                focus_key_ids,
                standard_width_px=standard_width_px,
            )
            candidate_stage = _visual_stage_box(
                stage,
                _opened_teaching_overlay(candidate_overlay),
            )
            physical_area = float(candidate_stage["pixel_count"])
            width_candidates.append(
                {
                    "standard_width_px": standard_width_px,
                    "overlay": candidate_overlay,
                    "visual_stage": candidate_stage,
                    "physical_area": physical_area,
                }
            )
        chosen_width = _widest_maximum_physical_area_candidate(width_candidates)
        selected_standard_width_px = chosen_width["standard_width_px"]
        preliminary_overlay = chosen_width["overlay"]
        open_visual_stage = chosen_width["visual_stage"]
        maximum_physical_area = max(
            candidate["physical_area"] for candidate in width_candidates
        )
        maximum_area_widths = [
            candidate["standard_width_px"]
            for candidate in width_candidates
            if abs(candidate["physical_area"] - maximum_physical_area) <= 1e-6
        ]
        open_visual_stage["selected_standard_overlay_width_px"] = (
            selected_standard_width_px
        )
        open_visual_stage["standard_overlay_width_candidates_px"] = list(
            standard_widths
        )
        open_visual_stage["standard_overlay_width_candidate_evaluations"] = [
            {
                "standard_width_px": candidate["standard_width_px"],
                "physical_canvas_area": _round(candidate["physical_area"]),
                "canvas_width": candidate["visual_stage"]["width"],
                "canvas_height": candidate["visual_stage"]["height"],
                "dock": candidate["visual_stage"].get("dock"),
            }
            for candidate in width_candidates
        ]
        open_visual_stage["physical_canvas_area"] = _round(
            chosen_width["physical_area"]
        )
        open_visual_stage["legacy_physical_canvas_area"] = _round(
            legacy_stage["pixel_count"]
        )
        open_visual_stage["physical_canvas_area_retention_ratio"] = _round(
            chosen_width["physical_area"] / legacy_stage["pixel_count"]
        )
        open_visual_stage["max_candidate_physical_canvas_area"] = _round(
            maximum_physical_area
        )
        open_visual_stage["max_physical_canvas_area_candidate_selected"] = (
            abs(chosen_width["physical_area"] - maximum_physical_area) <= 1e-6
        )
        open_visual_stage["widest_maximum_area_candidate_selected"] = (
            selected_standard_width_px == max(maximum_area_widths)
        )
        open_visual_stage["standard_profile"] = standard_profile
    aspect = visual_stage["width"] / visual_stage["height"]
    position, right, up, forward = _camera_basis(segment["frame"], aspect)
    projected: list[tuple[float, float]] = []
    clipped_point_count = 0
    for point in focus_points:
        result = _project_point(
            point,
            position=position,
            right=right,
            up=up,
            forward=forward,
            aspect=aspect,
        )
        if result is None:
            clipped_point_count += 1
            continue
        x, y, inside = result
        if not inside:
            clipped_point_count += 1
        projected.append((min(1.0, max(-1.0, x)), min(1.0, max(-1.0, y))))

    if projected:
        xs = [point[0] for point in projected]
        ys = [point[1] for point in projected]
        projected_occupancy = (max(xs) - min(xs)) / 2 * (max(ys) - min(ys)) / 2
    else:
        projected_occupancy = 0.0

    if visual["label_policy"] == "focus":
        label_node_ids = list(visual["label_node_ids"])
    else:
        label_node_ids = list(segment["focus_nodes"])
    reveals = set(segment["reveal_ids"])
    visible_label_count = 0
    intended_label_count = 0
    intended_label_ids: list[str] = []
    projected_label_ids: list[str] = []
    unplaced_label_boxes: list[dict[str, Any]] = []
    for node_id in label_node_ids:
        node = scene["nodes"][node_id]
        if not node.get("base_visible", True) and node_id not in reveals:
            continue
        intended_label_count += 1
        intended_label_ids.append(node_id)
        result = _project_point(
            node["label_at"],
            position=position,
            right=right,
            up=up,
            forward=forward,
            aspect=aspect,
        )
        if result is not None and result[2]:
            visible_label_count += 1
            projected_label_ids.append(node_id)
            x, y, _ = result
            label_width = _three_label_box_width(node_records[node_id])
            label_height = 21.5
            center_x = visual_stage["x"] + (x + 1.0) / 2.0 * visual_stage["width"]
            center_y = visual_stage["y"] + (1.0 - y) / 2.0 * visual_stage["height"]
            unplaced_label_boxes.append(
                {
                    "id": node_id,
                    "box": _box(
                        center_x - label_width / 2.0,
                        center_y - label_height / 2.0,
                        label_width,
                        label_height,
                    ),
                }
            )

    projected_visible_label_count = visible_label_count
    if shots.spatial_labels_require_fixed_key(
        visual_stage["width"], visual_stage["height"]
    ):
        selected_label_boxes = []
        layout_suppressed_ids = sorted(item["id"] for item in unplaced_label_boxes)
    else:
        selected_label_boxes, layout_suppressed_ids = _place_three_label_boxes(
            unplaced_label_boxes, visual_stage
        )
    overlay = _teaching_overlay_evaluation(
        segment,
        viewport,
        stage,
        selected_label_boxes,
        focus_key_ids,
        standard_width_px=selected_standard_width_px,
    )
    overlay["selected_standard_width_px"] = selected_standard_width_px
    suppressed_ids = (
        set(overlay["spatial_suppressed_ids"])
        if overlay["initially_visible"]
        else set()
    )
    for item in selected_label_boxes:
        item["spatially_suppressed_by_overlay"] = item["id"] in suppressed_ids
    visible_label_count = max(0, len(selected_label_boxes) - len(suppressed_ids))
    unprojected_label_ids = sorted(set(intended_label_ids) - set(projected_label_ids))
    fallback_id_set = (
        set(unprojected_label_ids) | set(layout_suppressed_ids) | suppressed_ids
    )
    fallback_ids = [node_id for node_id in focus_key_ids if node_id in fallback_id_set]
    fallback_missing_ids = sorted(fallback_id_set - set(focus_key_ids))
    marker_anchors = {
        item["id"]: (
            item["box"]["x"] + item["box"]["width"] / 2.0,
            item["box"]["y"] + item["box"]["height"] / 2.0,
        )
        for item in unplaced_label_boxes
    }
    visible_label_obstacles = [
        item for item in selected_label_boxes if item["id"] not in suppressed_ids
    ]
    geometry_correspondence = _place_numbered_focus_markers(
        marker_anchors,
        fallback_ids,
        visual_stage,
        overlay["box"] if overlay["initially_visible"] else None,
        visible_label_obstacles,
    )

    focus_items = len(segment["focus_nodes"]) + len(segment["focus_edges"])
    density = focus_items / (visual_stage["pixel_count"] / 1_000_000)
    risk_flags = []
    if focus_items >= DENSE_FOCUS_MIN_ITEMS:
        risk_flags.append("dense_focus")
    if visible_label_count > MAX_VISIBLE_LABELS:
        risk_flags.append("visible_label_pressure")
    if fallback_missing_ids:
        risk_flags.append("label_clipping")
    if not geometry_correspondence["passed"]:
        risk_flags.append("focus_key_geometry_correspondence_gap")
    if clipped_point_count:
        risk_flags.append("projected_clipping")
    if projected_occupancy < MIN_PROJECTED_OCCUPANCY:
        risk_flags.append("low_projected_occupancy")
    if overlay["initially_visible"]:
        risk_flags.extend(overlay["risk_flags"])

    return {
        "viewport_id": viewport["id"],
        "viewport": {
            "width": int(viewport["width"]),
            "height": int(viewport["height"]),
        },
        "stage": stage,
        "visual_stage": visual_stage,
        "open_visual_stage": open_visual_stage,
        "focus_density_per_megapixel": _round(density),
        "visible_label_count": visible_label_count,
        "selected_label_boxes": selected_label_boxes,
        "teaching_overlay": overlay,
        "fixed_focus_key": {
            "chip_count": len(focus_key_ids),
            "chip_ids": focus_key_ids,
            "font_px": FOCUS_KEY_FONT_PX,
            "numbered_geometry_correspondence": geometry_correspondence,
        },
        "fixed_boundary_note": {
            "copy_id": "footnote",
            "masthead_visible": True,
            "full_copy_accessible": True,
            "font_px": 10.0,
            "responsive_style": "full_exact"
            if int(viewport["width"]) > 1100
            else "compact_two_clause_visible_duplicate",
            "visible_clauses": ["source_gated", "teaching_reference_not_as_built"],
        },
        "three_dimensional": {
            "projected_occupancy": _round(projected_occupancy),
            "projected_point_count": len(focus_points),
            "clipped_point_count": clipped_point_count,
            "intended_label_count": intended_label_count,
            "projected_visible_label_count": projected_visible_label_count,
            "selected_label_box_count": len(selected_label_boxes),
            "spatially_suppressed_label_count": len(suppressed_ids),
            "layout_suppressed_label_ids": layout_suppressed_ids,
            "unprojected_label_ids": unprojected_label_ids,
            "fixed_key_fallback_ids": fallback_ids,
            "fixed_key_fallback_missing_ids": fallback_missing_ids,
            "fixed_key_fallback_complete": not fallback_missing_ids,
            "residual_label_collision_count": 0,
            "residual_stage_clip_count": 0,
            "lifecycle_chip_layout": "hidden_spatially_visible_in_fixed_key",
        },
        "risk_flags": sorted(risk_flags),
    }


def _annotation_coverage(segment: dict[str, Any]) -> dict[str, Any]:
    claim_ids = {claim["id"] for claim in segment["claims"]}
    annotation = segment["visual"]["annotation"]
    items = [] if annotation is None else annotation["items"]
    referenced_claims = {claim_id for item in items for claim_id in item["claim_ids"]}
    unknown = referenced_claims - claim_ids
    if unknown:
        raise QualityError(
            f"segment {segment['segment_id']}: annotation references unknown claims "
            f"{sorted(unknown)}"
        )
    item_count = len(items)
    items_with_claim_refs = sum(bool(item["claim_ids"]) for item in items)
    claim_count = len(claim_ids)
    return {
        "item_count": item_count,
        "items_with_claim_refs": items_with_claim_refs,
        "item_coverage": _round(items_with_claim_refs / item_count)
        if item_count
        else 0.0,
        "claim_count": claim_count,
        "covered_claim_count": len(referenced_claims),
        "claim_coverage": _round(len(referenced_claims) / claim_count)
        if claim_count
        else 0.0,
    }


def _occupancy_risk_records(compiled: Sequence[dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    for segment in compiled:
        for evaluation in segment["quality_vector"]["viewport_evaluations"]:
            risk_flags = sorted(
                OCCUPANCY_RISK_FLAGS.intersection(evaluation["risk_flags"])
            )
            if risk_flags:
                if len(risk_flags) != 1:
                    raise QualityError(
                        "an occupancy-risk evaluation must map to exactly one metric; "
                        f"segment_id={segment['segment_id']!r}, "
                        f"viewport_id={evaluation['viewport_id']!r}, "
                        f"risk_flags={risk_flags!r}"
                    )
                metric_id = OCCUPANCY_METRIC_BY_RISK_FLAG[risk_flags[0]]
                dimension, metric = metric_id.split(".", 1)
                dimension_metrics = evaluation.get(dimension)
                observed_value = (
                    dimension_metrics.get(metric)
                    if isinstance(dimension_metrics, dict)
                    else None
                )
                records.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "risk_flags": risk_flags,
                        "metric_id": metric_id,
                        "observed_value": observed_value,
                        "metric_available": observed_value is not None,
                        "disposition": "requires_live_preference",
                    }
                )
    return records


def _occupancy_modeled_evidence_ref(
    candidate_id: str, segment_id: str, viewport_id: str
) -> str:
    anchor = (
        "ratchet/experiment_control"
        if candidate_id == "experiment_control"
        else f"ratchet/challengers/{candidate_id}"
    )
    return (
        f"diagram/course_quality.json#{anchor}/layout_gates/occupancy_review/"
        f"evaluations/{segment_id}/{viewport_id}"
    )


def _occupancy_live_evidence_ref(
    candidate_id: str,
    provenance_sha256: str,
    *,
    candidate_current_state_sha256: str,
    validation_compiler_implementation_sha256: str,
    segment_id: str,
    viewport_id: str,
    modeled_evaluation_sha256: str,
    decision: str,
    reviewer_id: str,
    reviewed_at: str,
    artifact_sha256: str,
) -> str:
    evidence = {
        "candidate_id": candidate_id,
        "candidate_provenance_sha256": provenance_sha256,
        "candidate_current_state_sha256": candidate_current_state_sha256,
        "validation_compiler_implementation_sha256": validation_compiler_implementation_sha256,
        "segment_id": segment_id,
        "viewport_id": viewport_id,
        "modeled_evaluation_sha256": modeled_evaluation_sha256,
        "decision": decision,
        "reviewer_id": reviewer_id,
        "reviewed_at": reviewed_at,
        "artifact_sha256": artifact_sha256,
    }
    return _acceptance_evidence_ref(
        candidate_id,
        provenance_sha256,
        "live",
        f"occupancy_review:{segment_id}:{viewport_id}",
        evidence,
    )


def _occupancy_modeled_evaluation_sha256(
    candidate_id: str,
    candidate_current_state_sha256: str,
    evaluation: dict[str, Any],
) -> str:
    return _canonical_sha256(
        {
            "candidate_id": candidate_id,
            "candidate_current_state_sha256": candidate_current_state_sha256,
            "segment_id": evaluation["segment_id"],
            "viewport_id": evaluation["viewport_id"],
            "risk_flags": evaluation["risk_flags"],
            "metric_id": evaluation["metric_id"],
            "observed_value": evaluation["observed_value"],
        }
    )


def _occupancy_review_gate(
    compiled: Sequence[dict[str, Any]],
    occupancy_reviews: Sequence[dict[str, Any]] | None,
    *,
    candidate_id: str = "combined",
    expected_current_state: dict[str, Any] | None = None,
    capture_manifest: dict[str, Any] | None = None,
) -> dict[str, Any]:
    detected = _occupancy_risk_records(compiled)
    expected_by_key = {
        (record["segment_id"], record["viewport_id"]): record for record in detected
    }
    provenance_sha256 = None
    captures: list[dict[str, Any]] = []
    if capture_manifest is not None:
        captures = _validate_occupancy_capture_manifest(capture_manifest)["captures"]
    reviews: list[Any] = []
    if occupancy_reviews is not None:
        if isinstance(occupancy_reviews, (str, bytes)) or not isinstance(
            occupancy_reviews, Sequence
        ):
            raise QualityError("occupancy review sets must be a sequence")
        matching_sets = [
            review_set
            for review_set in occupancy_reviews
            if isinstance(review_set, dict)
            and review_set.get("candidate_id") == candidate_id
        ]
        if len(matching_sets) != 1:
            raise QualityError(
                "occupancy reviews must contain exactly one set for "
                f"candidate_id={candidate_id!r}"
            )
        review_set = matching_sets[0]
        if set(review_set) != {
            "candidate_id",
            "candidate_provenance_sha256",
            "reviews",
        }:
            raise QualityError("occupancy review set fields must be exact")
        provenance_sha256 = _sha256_string(
            review_set["candidate_provenance_sha256"],
            f"occupancy review provenance for {candidate_id}",
        )
        if not isinstance(review_set["reviews"], list):
            raise QualityError("occupancy review set reviews must be a list")
        reviews = list(review_set["reviews"])
    review_by_key: dict[tuple[str, str], dict[str, Any]] = {}
    seen_review_keys: set[tuple[Any, Any]] = set()
    malformed = []
    expected_fields = {
        "segment_id",
        "viewport_id",
        "risk_flags",
        "status",
        "metric_id",
        "observed_value",
        "rationale",
        "modeled_evidence_ref",
        "live_review",
    }
    for index, record in enumerate(reviews):
        if not isinstance(record, dict) or set(record) != expected_fields:
            malformed.append({"index": index, "reason": "fields_not_exact"})
            continue
        segment_id = record["segment_id"]
        viewport_id = record["viewport_id"]
        key = (segment_id, viewport_id)
        reasons = []
        valid_identity = (
            isinstance(segment_id, str)
            and bool(segment_id)
            and isinstance(viewport_id, str)
            and bool(viewport_id)
        )
        if not valid_identity:
            reasons.append("invalid_evaluation_identity")
        elif key in seen_review_keys:
            reasons.append("duplicate_evaluation_review")
        if valid_identity:
            seen_review_keys.add(key)
        if isinstance(segment_id, str) and isinstance(viewport_id, str):
            expected_modeled_evidence_ref = _occupancy_modeled_evidence_ref(
                candidate_id, segment_id, viewport_id
            )
        else:
            expected_modeled_evidence_ref = None
        status = record["status"]
        if type(status) is not str or status not in OCCUPANCY_REVIEW_STATUSES:
            reasons.append("status_is_invalid")
        for field in ("rationale", "modeled_evidence_ref"):
            if not isinstance(record[field], str) or not record[field].strip():
                reasons.append(f"{field}_must_be_non_empty")
        if record["modeled_evidence_ref"] != expected_modeled_evidence_ref:
            reasons.append("modeled_evidence_ref_does_not_match_evaluation")
        live_review = record["live_review"]
        if status == "unresolved":
            if live_review is not None:
                reasons.append("unresolved_review_must_not_claim_live_provenance")
        elif status in OCCUPANCY_REVIEW_STATUSES:
            if not isinstance(live_review, dict) or set(live_review) != set(
                OCCUPANCY_LIVE_REVIEW_FIELDS
            ):
                reasons.append("live_review_fields_not_exact")
            else:
                expected_decision = OCCUPANCY_LIVE_DECISION_BY_STATUS[status]
                if live_review["decision"] != expected_decision:
                    reasons.append("live_decision_does_not_match_status")
                for field in ("reviewer_id", "reviewed_at", "evidence_ref"):
                    value = live_review[field]
                    if type(value) is not str or not value.strip():
                        reasons.append(f"live_{field}_must_be_non_empty")
                artifact_sha256 = live_review["artifact_sha256"]
                try:
                    _sha256_string(
                        artifact_sha256,
                        "occupancy live_review.artifact_sha256",
                    )
                except QualityError:
                    reasons.append("live_artifact_sha256_must_be_sha256")
                reviewed_at = live_review["reviewed_at"]
                candidate_current_state_sha256 = live_review[
                    "candidate_current_state_sha256"
                ]
                validation_compiler_implementation_sha256 = live_review[
                    "validation_compiler_implementation_sha256"
                ]
                modeled_evaluation_sha256 = live_review["modeled_evaluation_sha256"]
                for field, digest in (
                    ("candidate_current_state_sha256", candidate_current_state_sha256),
                    (
                        "validation_compiler_implementation_sha256",
                        validation_compiler_implementation_sha256,
                    ),
                    ("modeled_evaluation_sha256", modeled_evaluation_sha256),
                ):
                    try:
                        _sha256_string(digest, f"occupancy live_review.{field}")
                    except QualityError:
                        reasons.append(f"live_{field}_must_be_sha256")
                timestamp_valid = False
                if isinstance(reviewed_at, str) and reviewed_at.strip():
                    normalized = (
                        f"{reviewed_at[:-1]}+00:00"
                        if reviewed_at.endswith("Z")
                        else reviewed_at
                    )
                    try:
                        timestamp = datetime.fromisoformat(normalized)
                    except ValueError:
                        timestamp = None
                    timestamp_valid = (
                        timestamp is not None
                        and timestamp.tzinfo is not None
                        and "T" in reviewed_at
                    )
                    if not timestamp_valid:
                        reasons.append("live_reviewed_at_must_be_rfc3339")
                if (
                    provenance_sha256 is not None
                    and live_review["decision"] == expected_decision
                    and isinstance(live_review["reviewer_id"], str)
                    and bool(live_review["reviewer_id"].strip())
                    and timestamp_valid
                    and isinstance(artifact_sha256, str)
                    and len(artifact_sha256) == 64
                    and artifact_sha256 == artifact_sha256.lower()
                    and all(
                        character in "0123456789abcdef" for character in artifact_sha256
                    )
                    and isinstance(candidate_current_state_sha256, str)
                    and len(candidate_current_state_sha256) == 64
                    and isinstance(validation_compiler_implementation_sha256, str)
                    and len(validation_compiler_implementation_sha256) == 64
                    and isinstance(modeled_evaluation_sha256, str)
                    and len(modeled_evaluation_sha256) == 64
                ):
                    expected_evaluation = expected_by_key.get(key)
                    if expected_current_state is None:
                        reasons.append("current_candidate_state_is_unavailable")
                        expected_modeled_sha256 = None
                    else:
                        expected_state_sha256 = expected_current_state[
                            "candidate_current_state_sha256"
                        ]
                        if candidate_current_state_sha256 != expected_state_sha256:
                            reasons.append("candidate_current_state_is_stale")
                        if (
                            validation_compiler_implementation_sha256
                            != expected_current_state[
                                "validation_compiler_implementation_sha256"
                            ]
                        ):
                            reasons.append("compiler_implementation_is_stale")
                        expected_modeled_sha256 = (
                            _occupancy_modeled_evaluation_sha256(
                                candidate_id,
                                expected_state_sha256,
                                expected_evaluation,
                            )
                            if expected_evaluation is not None
                            else None
                        )
                        if modeled_evaluation_sha256 != expected_modeled_sha256:
                            reasons.append("modeled_evaluation_digest_is_stale")
                    matching_captures = [
                        capture
                        for capture in captures
                        if capture["candidate_id"] == candidate_id
                        and capture["segment_id"] == segment_id
                        and capture["viewport_id"] == viewport_id
                    ]
                    if len(matching_captures) != 1:
                        reasons.append("canonical_capture_manifest_entry_is_missing")
                    else:
                        capture = matching_captures[0]
                        capture_bindings = {
                            "candidate_current_state_sha256": candidate_current_state_sha256,
                            "validation_compiler_implementation_sha256": validation_compiler_implementation_sha256,
                            "modeled_evaluation_sha256": modeled_evaluation_sha256,
                            "artifact_sha256": artifact_sha256,
                        }
                        if any(
                            capture[field] != expected
                            for field, expected in capture_bindings.items()
                        ):
                            reasons.append("canonical_capture_manifest_entry_is_stale")
                    expected_live_evidence_ref = _occupancy_live_evidence_ref(
                        candidate_id,
                        provenance_sha256,
                        candidate_current_state_sha256=candidate_current_state_sha256,
                        validation_compiler_implementation_sha256=validation_compiler_implementation_sha256,
                        segment_id=segment_id,
                        viewport_id=viewport_id,
                        modeled_evaluation_sha256=modeled_evaluation_sha256,
                        decision=expected_decision,
                        reviewer_id=live_review["reviewer_id"],
                        reviewed_at=reviewed_at,
                        artifact_sha256=artifact_sha256,
                    )
                    if live_review["evidence_ref"] != expected_live_evidence_ref:
                        reasons.append("live_evidence_ref_is_not_content_addressed")
        elif live_review is not None:
            reasons.append("invalid_status_must_not_claim_live_provenance")
        if candidate_id == "experiment_control" and (
            status != "unresolved" or live_review is not None
        ):
            reasons.append("experiment_control_must_remain_unresolved")
        risk_flags = record["risk_flags"]
        if (
            not isinstance(risk_flags, list)
            or not all(isinstance(flag, str) for flag in risk_flags)
            or len(risk_flags) != len(set(risk_flags))
        ):
            reasons.append("risk_flags_must_be_unique_strings")
        elif sorted(risk_flags) != (
            expected_by_key.get(key, {}).get("risk_flags") if valid_identity else None
        ):
            reasons.append("risk_flags_do_not_match_evaluation")
        expected = expected_by_key.get(key, {}) if valid_identity else {}
        if record["metric_id"] != expected.get("metric_id"):
            reasons.append("metric_id_does_not_match_evaluation")
        observed_value = record["observed_value"]
        if (
            isinstance(observed_value, bool)
            or not isinstance(observed_value, (int, float))
            or not math.isfinite(float(observed_value))
        ):
            reasons.append("observed_value_must_be_finite_number")
        elif observed_value != expected.get("observed_value"):
            reasons.append("observed_value_does_not_match_evaluation")
        if reasons:
            malformed.append({"index": index, "key": list(key), "reasons": reasons})
        else:
            review_by_key[key] = copy.deepcopy(record)

    missing = [
        record for key, record in expected_by_key.items() if key not in review_by_key
    ]
    extra = [
        {
            "segment_id": segment_id,
            "viewport_id": viewport_id,
        }
        for segment_id, viewport_id in sorted(seen_review_keys)
        if (segment_id, viewport_id) not in expected_by_key
    ]
    resolved_capture_keys = {
        key
        for key, record in review_by_key.items()
        if key in expected_by_key
        and record["status"] in {"live_approved", "live_rejected"}
    }
    malformed.extend(
        {
            "index": index,
            "key": [capture["segment_id"], capture["viewport_id"]],
            "reasons": ["canonical_capture_manifest_entry_is_unconsumed"],
        }
        for index, capture in enumerate(captures)
        if capture["candidate_id"] == candidate_id
        and (capture["segment_id"], capture["viewport_id"]) not in resolved_capture_keys
    )
    valid_reviews = [
        review_by_key[key] for key in sorted(review_by_key) if key in expected_by_key
    ]
    resolution_counts = {
        status: sum(record["status"] == status for record in valid_reviews)
        for status in sorted(OCCUPANCY_REVIEW_STATUSES)
    }
    invalid_coverage = bool(missing or extra or malformed)
    if invalid_coverage or resolution_counts["live_rejected"]:
        status = "failed"
    elif resolution_counts["unresolved"]:
        status = "pending"
    else:
        status = "passed"
    disposition = {
        "failed": "live_rejected"
        if not invalid_coverage and resolution_counts["live_rejected"]
        else "invalid_review_coverage",
        "pending": "requires_live_preference",
        "passed": "live_approved" if detected else "not_required",
    }[status]
    return {
        "passed": status == "passed",
        "status": status,
        "candidate_id": candidate_id,
        "candidate_provenance_sha256": provenance_sha256,
        "risk_flags": sorted(OCCUPANCY_RISK_FLAGS),
        "exact_coverage_required": True,
        "live_confirmation_status": status,
        "disposition": disposition,
        "detected_risk_evaluation_count": len(detected),
        "reviewed_evaluation_count": len(review_by_key),
        "resolution_counts": resolution_counts,
        "detected_risk_evaluations": detected,
        "reviews": valid_reviews,
        "missing_reviews": missing,
        "extra_reviews": extra,
        "malformed_reviews": malformed,
    }


def _quality_risk_score(segment: dict[str, Any]) -> int:
    """Count observed defect risks, excluding density as a neutral characteristic."""
    evaluation_flags = [
        flag
        for evaluation in segment["quality_vector"]["viewport_evaluations"]
        for flag in evaluation["risk_flags"]
        if flag != "dense_focus"
    ]
    segment_only_flags = set(segment["quality_vector"]["risk_flags"]) - {
        flag
        for evaluation in segment["quality_vector"]["viewport_evaluations"]
        for flag in evaluation["risk_flags"]
    }
    return len(evaluation_flags) + len(segment_only_flags - {"dense_focus"})


def _validate_quality_camera_inputs(
    master: dict[str, Any],
    scene: dict[str, Any],
    cameras: dict[str, Any],
    runtime_registry: dict[str, Any],
) -> None:
    scene_pipeline.validate(master, scene, cameras)
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    expected_up = [float(value) for value in scene["world"]["camera_up"]]
    for segment in runtime_registry["segments"]:
        if segment["render_mode"] != "3d":
            continue
        anchor_id = segment["camera_anchor"]
        anchor = camera_map.get(anchor_id)
        if anchor is None or anchor["mode"] != "3d":
            raise QualityError(
                f"segment {segment['segment_id']}: invalid 3D camera anchor "
                f"{anchor_id!r}"
            )
        frame = segment["frame"]
        expected = {
            "anchor_position": [float(value) for value in anchor["position"]],
            "anchor_target": [float(value) for value in anchor["target"]],
            "up": expected_up,
        }
        mismatched = sorted(
            field for field, value in expected.items() if frame.get(field) != value
        )
        if mismatched:
            raise QualityError(
                f"segment {segment['segment_id']}: runtime 3D camera anchor "
                f"binding mismatch fields={mismatched}"
            )


def compile_quality_registry(
    course: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
    runtime_registry: dict[str, Any],
    *,
    source_digest: str,
    cameras: dict[str, Any] | None = None,
    occupancy_reviews: Sequence[dict[str, Any]] | None = None,
    occupancy_candidate_id: str = "combined",
) -> dict[str, Any]:
    """Measure every segment at the protected course viewports."""
    if cameras is None:
        cameras = scene_pipeline.load_yaml(shots.CAMERAS_PATH)
    _validate_quality_camera_inputs(master, scene, cameras, runtime_registry)
    segments = runtime_registry["segments"]
    if len(segments) != course_runtime.EXPECTED_SEGMENTS:
        raise QualityError(
            f"expected {course_runtime.EXPECTED_SEGMENTS} segments, "
            f"found {len(segments)}"
        )
    segment_ids = {segment["segment_id"] for segment in segments}
    missing_sentinels = set(PROTECTED_DENSE_SEGMENTS) - segment_ids
    if missing_sentinels:
        raise QualityError(
            f"protected dense segments are missing: {sorted(missing_sentinels)}"
        )

    node_records, edge_records = shots._exact_geometry_coverage(master, layout, scene)
    geoms = layout_pipeline.build_geoms(layout, master, layout["frame"]["ground"])
    label_specs = _map_label_specs(course, master, layout, ledgers)
    if PROTECTED_MAP_COPY_IDS != frozenset({"footnote"}):
        raise QualityError("runtime protected map copy must remain exactly footnote")
    missing_protected_copy = set(PROTECTED_MAP_COPY_IDS) - set(label_specs)
    if missing_protected_copy:
        raise QualityError(
            f"protected map copy is not rendered: {sorted(missing_protected_copy)}"
        )
    legend_request_ids = sorted(
        segment["segment_id"]
        for segment in segments
        if segment["visual"]["show_legend"]
    )
    unauthorized_legend_ids = sorted(
        set(legend_request_ids) - ALLOWED_LEGEND_SEGMENT_IDS
    )
    if unauthorized_legend_ids:
        raise QualityError(
            "map legend may only be requested by p1_read_the_machine; found "
            f"{unauthorized_legend_ids}"
        )
    master_evidence = ledgers[course["meta"]["master_evidence_ledger"]]
    boundary_note = layout_pipeline.resolve_copy(
        master,
        master_evidence,
        "footnote",
        include_hidden=True,
    )
    if not isinstance(boundary_note, str) or not boundary_note:
        raise QualityError("protected footnote must resolve to fixed boundary copy")

    compiled = []
    portrait_focus_key_records = []
    short_focus_key_records = []
    tablet_focus_key_records = []
    desktop_focus_key_records = []
    focused_stroke_contract = course_runtime.focused_geometry_stroke_contract()
    for segment in segments:
        focus_items = len(segment["focus_nodes"]) + len(segment["focus_edges"])
        annotation = _annotation_coverage(segment)
        portrait_focus_key = _portrait_focus_key_evaluation(
            segment,
            master,
            master_evidence,
        )
        portrait_focus_key_records.append(portrait_focus_key)
        focus_key_entries = portrait_focus_key["entries"]
        short_focus_key = _short_focus_key_evaluation(
            segment,
            master,
            master_evidence,
        )
        short_focus_key_records.append(short_focus_key)
        tablet_focus_key = _tablet_focus_key_evaluation(
            segment,
            master,
            master_evidence,
        )
        tablet_focus_key_records.append(tablet_focus_key)
        desktop_focus_keys = {
            viewport_id: _desktop_focus_key_evaluation(
                segment,
                master,
                master_evidence,
                viewport_id,
            )
            for viewport_id in DESKTOP_VIEWPORT_IDS
        }
        desktop_focus_key_records.extend(desktop_focus_keys.values())
        evaluations = []
        if segment["frame"]["kind"] == "2d":
            focus_points_2d = _focus_points_2d(segment, layout, edge_records, geoms)
            for viewport in VIEWPORTS:
                stage = _stage_box(viewport)
                evaluations.append(
                    _map_evaluation(
                        segment,
                        viewport,
                        stage,
                        layout,
                        master,
                        label_specs,
                        focus_points_2d,
                        focused_stroke_contract,
                    )
                )
        elif segment["frame"]["kind"] == "3d":
            focus_points_3d = _focus_points_3d(segment, scene)
            for viewport in VIEWPORTS:
                stage = _stage_box(viewport)
                evaluations.append(
                    _three_evaluation(
                        segment,
                        viewport,
                        stage,
                        node_records,
                        scene,
                        focus_points_3d,
                    )
                )
        else:
            raise QualityError(
                f"segment {segment['segment_id']}: unsupported frame kind "
                f"{segment['frame']['kind']!r}"
            )
        for viewport, evaluation in zip(VIEWPORTS, evaluations, strict=True):
            if viewport["id"] == PORTRAIT_VIEWPORT_ID:
                evaluation["portrait_focus_key"] = portrait_focus_key
            if viewport["id"] == SHORT_VIEWPORT_ID:
                evaluation["short_focus_key"] = short_focus_key
            if viewport["id"] == TABLET_VIEWPORT_ID:
                evaluation["tablet_focus_key"] = tablet_focus_key
            if viewport["id"] in DESKTOP_VIEWPORT_IDS:
                evaluation["desktop_focus_key"] = desktop_focus_keys[viewport["id"]]
            evaluation["header_flow"] = _header_flow_evaluation(
                segment,
                viewport,
                evaluation["stage"],
                focus_key_entries,
                portrait_focus_key if viewport["id"] == PORTRAIT_VIEWPORT_ID else None,
                short_focus_key if viewport["id"] == SHORT_VIEWPORT_ID else None,
                tablet_focus_key if viewport["id"] == TABLET_VIEWPORT_ID else None,
                desktop_focus_keys.get(viewport["id"]),
            )

        risk_flags = {
            flag for evaluation in evaluations for flag in evaluation["risk_flags"]
        }
        if (
            focus_items >= DENSE_FOCUS_MIN_ITEMS
            and annotation["claim_coverage"] < MIN_DENSE_ANNOTATION_CLAIM_COVERAGE
        ):
            risk_flags.add("dense_annotation_coverage_gap")
        overlay_position_candidates = []
        if segment["visual"]["annotation"] is not None:
            for position in ("left", "right", "top-left", "top-right"):
                failures = []
                for evaluation in evaluations:
                    candidate = next(
                        item
                        for item in evaluation["teaching_overlay"][
                            "candidate_positions"
                        ]
                        if item["position"] == position
                    )
                    if not candidate["passed"]:
                        failures.append(
                            {
                                "viewport_id": evaluation["viewport_id"],
                                "raw_collision_ids": candidate["raw_collision_ids"],
                                "residual_collision_ids": candidate[
                                    "residual_collision_ids"
                                ],
                                "suppressed_labels_missing_from_focus_key": (
                                    candidate[
                                        "suppressed_labels_missing_from_focus_key"
                                    ]
                                ),
                                "stage_clipped": candidate["stage_clipped"],
                            }
                        )
                overlay_position_candidates.append(
                    {
                        "position": position,
                        "passed_all_viewports": not failures,
                        "failures": failures,
                    }
                )
        compiled.append(
            {
                "sequence": segment["sequence"],
                "segment_id": segment["segment_id"],
                "shot_id": segment["id"],
                "mode": segment["mode"],
                "render_mode": segment["render_mode"],
                "protected_dense_sentinel": segment["segment_id"]
                in PROTECTED_DENSE_SEGMENTS,
                "quality_vector": {
                    "focus_density": {
                        "focus_node_count": len(segment["focus_nodes"]),
                        "focus_edge_count": len(segment["focus_edges"]),
                        "semantic_item_count": focus_items,
                    },
                    "annotation_coverage": annotation,
                    "overlay_position_candidates": overlay_position_candidates,
                    "viewport_evaluations": evaluations,
                    "risk_flags": sorted(risk_flags),
                },
            }
        )

    expected_portrait_focus_ids = {
        segment["segment_id"]
        for segment in segments
        if segment["visual"]["label_policy"] == "focus"
    }
    evaluated_portrait_focus_ids = {
        record["segment_id"]
        for record in portrait_focus_key_records
        if record["applicable"]
    }
    missing_portrait_focus_ids = sorted(
        expected_portrait_focus_ids - evaluated_portrait_focus_ids
    )
    extra_portrait_focus_ids = sorted(
        evaluated_portrait_focus_ids - expected_portrait_focus_ids
    )
    portrait_focus_key_failures = [
        {
            "segment_id": record["segment_id"],
            "entry_count": record["entry_count"],
            "failure_reasons": record["failure_reasons"],
            "estimate": record["estimate"],
        }
        for record in portrait_focus_key_records
        if record["applicable"] and not record["passed"]
    ]
    portrait_exact_coverage = (
        len(portrait_focus_key_records) == len(segments)
        and not missing_portrait_focus_ids
        and not extra_portrait_focus_ids
    )
    portrait_focus_key_passed = (
        portrait_exact_coverage and not portrait_focus_key_failures
    )
    portrait_focus_key_gate = {
        "passed": portrait_focus_key_passed,
        "status": (
            "not_applicable"
            if not expected_portrait_focus_ids and portrait_focus_key_passed
            else ("passed" if portrait_focus_key_passed else "failed")
        ),
        "evidence_scope": PORTRAIT_FOCUS_KEY_EVIDENCE_SCOPE,
        "viewport_id": PORTRAIT_VIEWPORT_ID,
        "segment_count": len(segments),
        "focus_policy_segment_count": len(expected_portrait_focus_ids),
        "evaluated_focus_policy_segment_count": len(evaluated_portrait_focus_ids),
        "not_applicable_segment_count": len(segments)
        - len(expected_portrait_focus_ids),
        "exact_coverage_required": True,
        "exact_coverage_passed": portrait_exact_coverage,
        "covered_segment_ids": sorted(evaluated_portrait_focus_ids),
        "missing_segment_ids": missing_portrait_focus_ids,
        "extra_segment_ids": extra_portrait_focus_ids,
        "required_safety_margin_px": (
            course_runtime.PORTRAIT_MASTHEAD_SAFETY_MARGIN_PX
        ),
        "minimum_observed_safety_margin_px": min(
            (
                record["estimate"]["spare_height_px"]
                for record in portrait_focus_key_records
                if record["applicable"]
            ),
            default=None,
        ),
        "failure_count": len(portrait_focus_key_failures),
        "failures": portrait_focus_key_failures,
    }

    expected_short_focus_ids = expected_portrait_focus_ids
    evaluated_short_focus_ids = {
        record["segment_id"]
        for record in short_focus_key_records
        if record["applicable"]
    }
    missing_short_focus_ids = sorted(
        expected_short_focus_ids - evaluated_short_focus_ids
    )
    extra_short_focus_ids = sorted(evaluated_short_focus_ids - expected_short_focus_ids)
    short_focus_key_failures = [
        {
            "segment_id": record["segment_id"],
            "entry_count": record["entry_count"],
            "failure_reasons": record["failure_reasons"],
            "estimate": record["estimate"],
        }
        for record in short_focus_key_records
        if record["applicable"] and not record["passed"]
    ]
    short_exact_coverage = (
        len(short_focus_key_records) == len(segments)
        and not missing_short_focus_ids
        and not extra_short_focus_ids
    )
    short_header_records = [
        {
            "segment_id": segment["segment_id"],
            "header_flow": next(
                evaluation["header_flow"]
                for evaluation in segment["quality_vector"]["viewport_evaluations"]
                if evaluation["viewport_id"] == SHORT_VIEWPORT_ID
            ),
        }
        for segment in compiled
    ]
    short_masthead_failures = [
        {
            **record,
            "failure_reasons": [
                reason
                for reason, failed in (
                    (
                        "short_opening_question_font_below_floor",
                        record["header_flow"]["opening_question_font_px"] < 10.0,
                    ),
                    (
                        "short_masthead_safety_margin_failed",
                        not record["header_flow"]["safety_margin_passed"],
                    ),
                )
                if failed
            ],
        }
        for record in short_header_records
        if record["header_flow"]["opening_question_font_px"] < 10.0
        or not record["header_flow"]["safety_margin_passed"]
    ]
    short_failures = [*short_focus_key_failures, *short_masthead_failures]
    short_focus_key_passed = short_exact_coverage and not short_failures
    short_focus_key_gate = {
        "passed": short_focus_key_passed,
        "status": (
            "not_applicable"
            if not expected_short_focus_ids and short_focus_key_passed
            else ("passed" if short_focus_key_passed else "failed")
        ),
        "evidence_scope": SHORT_FOCUS_KEY_EVIDENCE_SCOPE,
        "viewport_id": SHORT_VIEWPORT_ID,
        "segment_count": len(segments),
        "evaluation_count": len(short_focus_key_records),
        "focus_policy_segment_count": len(expected_short_focus_ids),
        "evaluated_focus_policy_segment_count": len(evaluated_short_focus_ids),
        "not_applicable_segment_count": len(segments) - len(expected_short_focus_ids),
        "exact_coverage_required": True,
        "exact_coverage_passed": short_exact_coverage,
        "covered_segment_ids": sorted(evaluated_short_focus_ids),
        "missing_segment_ids": missing_short_focus_ids,
        "extra_segment_ids": extra_short_focus_ids,
        "maximum_allowed_width_px": course_runtime.SHORT_FOCUS_KEY_CONTENT_WIDTH_PX,
        "maximum_allowed_height_px": course_runtime.SHORT_FOCUS_KEY_MAX_HEIGHT_PX,
        "minimum_required_font_px": MIN_SPATIAL_LABEL_FONT_PX,
        "opening_question_font_px": course_runtime.SHORT_OPENING_QUESTION_FONT_PX,
        "required_masthead_safety_margin_px": (
            course_runtime.SHORT_MASTHEAD_SAFETY_MARGIN_PX
        ),
        "minimum_observed_masthead_safety_margin_px": min(
            record["header_flow"]["spare_height_px"] for record in short_header_records
        ),
        "minimum_observed_font_px": min(
            (
                record["estimate"]["font_px"]
                for record in short_focus_key_records
                if record["applicable"]
            ),
            default=None,
        ),
        "minimum_observed_index_font_px": min(
            (
                record["estimate"]["index_font_px"]
                for record in short_focus_key_records
                if record["applicable"]
            ),
            default=None,
        ),
        "failure_count": len(short_failures),
        "failures": short_failures,
    }

    expected_tablet_focus_ids = expected_portrait_focus_ids
    evaluated_tablet_focus_ids = {
        record["segment_id"]
        for record in tablet_focus_key_records
        if record["applicable"]
    }
    missing_tablet_focus_ids = sorted(
        expected_tablet_focus_ids - evaluated_tablet_focus_ids
    )
    extra_tablet_focus_ids = sorted(
        evaluated_tablet_focus_ids - expected_tablet_focus_ids
    )
    tablet_focus_key_failures = [
        {
            "segment_id": record["segment_id"],
            "entry_count": record["entry_count"],
            "failure_reasons": record["failure_reasons"],
            "estimate": record["estimate"],
        }
        for record in tablet_focus_key_records
        if record["applicable"] and not record["passed"]
    ]
    tablet_exact_coverage = (
        len(tablet_focus_key_records) == len(segments)
        and not missing_tablet_focus_ids
        and not extra_tablet_focus_ids
    )
    tablet_focus_key_passed = tablet_exact_coverage and not tablet_focus_key_failures
    tablet_focus_key_gate = {
        "passed": tablet_focus_key_passed,
        "status": (
            "not_applicable"
            if not expected_tablet_focus_ids and tablet_focus_key_passed
            else ("passed" if tablet_focus_key_passed else "failed")
        ),
        "evidence_scope": TABLET_FOCUS_KEY_EVIDENCE_SCOPE,
        "viewport_id": TABLET_VIEWPORT_ID,
        "segment_count": len(segments),
        "evaluation_count": len(tablet_focus_key_records),
        "focus_policy_segment_count": len(expected_tablet_focus_ids),
        "evaluated_focus_policy_segment_count": len(evaluated_tablet_focus_ids),
        "not_applicable_segment_count": len(segments) - len(expected_tablet_focus_ids),
        "exact_coverage_required": True,
        "exact_coverage_passed": tablet_exact_coverage,
        "covered_segment_ids": sorted(evaluated_tablet_focus_ids),
        "missing_segment_ids": missing_tablet_focus_ids,
        "extra_segment_ids": extra_tablet_focus_ids,
        "maximum_allowed_width_px": course_runtime.TABLET_FOCUS_KEY_CONTENT_WIDTH_PX,
        "maximum_allowed_height_px": course_runtime.TABLET_FOCUS_KEY_MAX_HEIGHT_PX,
        "minimum_required_font_px": MIN_SPATIAL_LABEL_FONT_PX,
        "minimum_observed_font_px": min(
            (
                record["estimate"]["font_px"]
                for record in tablet_focus_key_records
                if record["applicable"]
            ),
            default=None,
        ),
        "minimum_observed_index_font_px": min(
            (
                record["estimate"]["index_font_px"]
                for record in tablet_focus_key_records
                if record["applicable"]
            ),
            default=None,
        ),
        "failure_count": len(tablet_focus_key_failures),
        "failures": tablet_focus_key_failures,
    }

    responsive_key_source_contract = course_runtime.responsive_focus_key_contract()
    expected_desktop_pairs = {
        (segment["segment_id"], viewport_id)
        for segment in segments
        for viewport_id in DESKTOP_VIEWPORT_IDS
    }
    observed_desktop_pairs = {
        (record["segment_id"], record["viewport_id"])
        for record in desktop_focus_key_records
    }
    desktop_focus_key_failures = [
        {
            "segment_id": record["segment_id"],
            "viewport_id": record["viewport_id"],
            "entry_count": record["entry_count"],
            "failure_reasons": record["failure_reasons"],
            "estimate": record["estimate"],
        }
        for record in desktop_focus_key_records
        if record["applicable"] and not record["passed"]
    ]
    if not responsive_key_source_contract["passed"]:
        desktop_focus_key_failures.append(
            {
                "segment_id": None,
                "viewport_id": None,
                "entry_count": None,
                "failure_reasons": ["responsive_focus_key_source_contract_failed"],
                "source_contract": responsive_key_source_contract,
            }
        )
    desktop_exact_coverage = observed_desktop_pairs == expected_desktop_pairs
    desktop_focus_key_passed = desktop_exact_coverage and not desktop_focus_key_failures
    desktop_focus_key_gate = {
        "passed": desktop_focus_key_passed,
        "status": "passed" if desktop_focus_key_passed else "failed",
        "evidence_scope": DESKTOP_FOCUS_KEY_EVIDENCE_SCOPE,
        "viewport_ids": list(DESKTOP_VIEWPORT_IDS),
        "segment_count": len(segments),
        "viewport_count": len(DESKTOP_VIEWPORT_IDS),
        "evaluation_count": len(desktop_focus_key_records),
        "expected_evaluation_count": len(segments) * len(DESKTOP_VIEWPORT_IDS),
        "focus_policy_evaluation_count": sum(
            record["applicable"] for record in desktop_focus_key_records
        ),
        "exact_coverage_required": True,
        "exact_coverage_passed": desktop_exact_coverage,
        "missing_evaluations": [
            {"segment_id": segment_id, "viewport_id": viewport_id}
            for segment_id, viewport_id in sorted(
                expected_desktop_pairs - observed_desktop_pairs
            )
        ],
        "extra_evaluations": [
            {"segment_id": segment_id, "viewport_id": viewport_id}
            for segment_id, viewport_id in sorted(
                observed_desktop_pairs - expected_desktop_pairs
            )
        ],
        "content_width_px_by_viewport": {
            viewport_id: course_runtime.desktop_focus_key_content_width(
                next(
                    int(viewport["width"])
                    for viewport in VIEWPORTS
                    if viewport["id"] == viewport_id
                )
            )
            for viewport_id in DESKTOP_VIEWPORT_IDS
        },
        "maximum_allowed_height_px": course_runtime.DESKTOP_FOCUS_KEY_MAX_HEIGHT_PX,
        "minimum_required_font_px": MIN_SPATIAL_LABEL_FONT_PX,
        "minimum_observed_font_px": min(
            (
                record["estimate"]["font_px"]
                for record in desktop_focus_key_records
                if record["applicable"]
            ),
            default=None,
        ),
        "minimum_observed_index_font_px": min(
            (
                record["estimate"]["index_font_px"]
                for record in desktop_focus_key_records
                if record["applicable"]
            ),
            default=None,
        ),
        "horizontal_paging_required": any(
            record["estimate"]["horizontal_paging_required"]
            for record in desktop_focus_key_records
            if record["applicable"]
        ),
        "source_contract": responsive_key_source_contract,
        "evaluations": desktop_focus_key_records,
        "failure_count": len(desktop_focus_key_failures),
        "failures": desktop_focus_key_failures,
    }

    typography_records = []
    for segment in segments:
        for viewport in VIEWPORTS:
            viewport_id = str(viewport["id"])
            profile = responsive_key_source_contract["profile_font_px"][viewport_id]
            reasons = []
            if not responsive_key_source_contract["passed"]:
                reasons.append("responsive_focus_key_source_contract_failed")
            if profile["text"] < course_runtime.FOCUS_KEY_INDEX_FONT_FLOOR_PX:
                reasons.append("focus_key_text_font_below_floor")
            if profile["index"] < course_runtime.FOCUS_KEY_INDEX_FONT_FLOOR_PX:
                reasons.append("focus_key_index_font_below_floor")
            typography_records.append(
                {
                    "segment_id": segment["segment_id"],
                    "viewport_id": viewport_id,
                    "text_font_px": profile["text"],
                    "index_font_px": profile["index"],
                    "minimum_font_px": course_runtime.FOCUS_KEY_INDEX_FONT_FLOOR_PX,
                    "failure_reasons": reasons,
                    "passed": not reasons,
                }
            )
    expected_typography_pairs = {
        (segment["segment_id"], str(viewport["id"]))
        for segment in segments
        for viewport in VIEWPORTS
    }
    observed_typography_pairs = {
        (record["segment_id"], record["viewport_id"]) for record in typography_records
    }
    typography_failures = [
        record for record in typography_records if not record["passed"]
    ]
    typography_exact_coverage = observed_typography_pairs == expected_typography_pairs
    responsive_focus_key_font_gate = {
        "passed": typography_exact_coverage and not typography_failures,
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "scope": "all_segments_all_viewports",
        "segment_count": len(segments),
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": len(typography_records),
        "expected_evaluation_count": len(segments) * len(VIEWPORTS),
        "exact_coverage_required": True,
        "exact_coverage_passed": typography_exact_coverage,
        "minimum_required_font_px": course_runtime.FOCUS_KEY_INDEX_FONT_FLOOR_PX,
        "minimum_observed_text_font_px": min(
            record["text_font_px"] for record in typography_records
        ),
        "minimum_observed_index_font_px": min(
            record["index_font_px"] for record in typography_records
        ),
        "aria_label": responsive_key_source_contract["aria_label"],
        "source_contract": responsive_key_source_contract,
        "evaluations": typography_records,
        "failure_count": len(typography_failures),
        "failures": typography_failures,
    }

    grammar_source_contract = course_runtime.fixed_grammar_key_contract()
    p1_matches = [
        segment
        for segment in segments
        if segment["segment_id"] == "p1_read_the_machine"
    ]
    grammar_reasons = []
    grammar_entries: list[dict[str, Any]] = []
    geometry_entries: list[dict[str, Any]] = []
    if len(p1_matches) != 1:
        grammar_reasons.append("p1_segment_not_exactly_once")
    else:
        p1 = p1_matches[0]
        if p1["visual"]["show_legend"]:
            grammar_reasons.append("projected_map_legend_must_be_suppressed")
        p1_entries = course_runtime.focus_key_entries(p1, master, master_evidence)
        grammar_entries = [
            entry for entry in p1_entries if entry["key_role"] == "grammar"
        ]
        geometry_entries = [
            entry for entry in p1_entries if entry["key_role"] == "geometry"
        ]
        expected_grammar_ids = list(course_runtime._LEGEND_GRAMMAR_CUES)
        if [entry["id"] for entry in grammar_entries] != expected_grammar_ids:
            grammar_reasons.append("fixed_grammar_id_order_mismatch")
        if any(
            entry["number"] is not None or entry["marker_required"]
            for entry in grammar_entries
        ):
            grammar_reasons.append("grammar_rows_must_be_unnumbered_unanchored")
        if [entry["number"] for entry in geometry_entries] != list(
            range(1, len(geometry_entries) + 1)
        ):
            grammar_reasons.append("geometry_row_numbering_not_contiguous")
        if [entry["swatch_cue"] for entry in grammar_entries] != list(
            course_runtime._LEGEND_GRAMMAR_CUES.values()
        ):
            grammar_reasons.append("fixed_grammar_cue_order_mismatch")
        direction_entry = next(
            (entry for entry in grammar_entries if entry["id"] == "legend_direction"),
            None,
        )
        if direction_entry is None:
            grammar_reasons.append("named_direction_row_missing")
        else:
            if direction_entry["compact_label"] != "138 tie → station":
                grammar_reasons.append("named_direction_visible_copy_mismatch")
            if "initial 138 kV tie → initial 200 MW / 138 kV station" not in str(
                direction_entry["accessible_label"]
            ):
                grammar_reasons.append("named_direction_accessible_copy_missing")
    if not grammar_source_contract["passed"]:
        grammar_reasons.append("fixed_grammar_source_contract_failed")
    grammar_profile_by_viewport = {
        "1920x1080": "standard",
        "1440x900": "standard",
        TABLET_VIEWPORT_ID: "tablet",
        SHORT_VIEWPORT_ID: "short",
        PORTRAIT_VIEWPORT_ID: "portrait",
    }
    grammar_viewport_records = []
    for viewport in VIEWPORTS:
        profile_id = grammar_profile_by_viewport[str(viewport["id"])]
        font_px = grammar_source_contract["profile_font_px"][profile_id]
        record_reasons = list(grammar_reasons)
        if font_px < 10.0:
            record_reasons.append("fixed_grammar_font_below_floor")
        grammar_viewport_records.append(
            {
                "viewport_id": viewport["id"],
                "profile_id": profile_id,
                "grammar_entry_count": len(grammar_entries),
                "geometry_entry_count": len(geometry_entries),
                "font_px": font_px,
                "minimum_font_px": 10.0,
                "failure_reasons": record_reasons,
                "passed": not record_reasons,
            }
        )
    grammar_failures = [
        record for record in grammar_viewport_records if not record["passed"]
    ]
    fixed_grammar_key_gate = {
        "passed": not grammar_failures,
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "segment_id": "p1_read_the_machine",
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": len(grammar_viewport_records),
        "grammar_ids": [entry["id"] for entry in grammar_entries],
        "grammar_cues": [entry["swatch_cue"] for entry in grammar_entries],
        "grammar_entry_count": len(grammar_entries),
        "geometry_entry_count": len(geometry_entries),
        "projected_map_legend_suppressed": (
            len(p1_matches) == 1 and not p1_matches[0]["visual"]["show_legend"]
        ),
        "source_contract": grammar_source_contract,
        "evaluations": grammar_viewport_records,
        "failure_count": len(grammar_failures),
        "failures": grammar_failures,
    }

    portrait_drawer_contract = course_runtime.portrait_teaching_drawer_contract()
    expected_portrait_drawer_ids = {
        segment["segment_id"]
        for segment in segments
        if segment["visual"]["annotation"] is not None
    }
    portrait_drawer_records = []
    portrait_drawer_failures = []
    for segment in compiled:
        evaluation = next(
            record
            for record in segment["quality_vector"]["viewport_evaluations"]
            if record["viewport_id"] == PORTRAIT_VIEWPORT_ID
        )
        overlay = evaluation["teaching_overlay"]
        expected = segment["segment_id"] in expected_portrait_drawer_ids
        reasons = []
        if expected:
            if not overlay["present"]:
                reasons.append("authored_annotation_missing")
            if overlay["initially_visible"]:
                reasons.append("drawer_not_closed_by_default")
            if overlay["interaction_mode"] != "portrait_toggle_drawer":
                reasons.append("portrait_drawer_mode_missing")
            if not overlay["available_on_demand"]:
                reasons.append("portrait_drawer_unavailable")
            if overlay["box"] is not None:
                reasons.append("closed_drawer_participates_in_geometry")
        elif (
            overlay["present"]
            or overlay["initially_visible"]
            or overlay["interaction_mode"] != "not_applicable"
            or overlay["available_on_demand"]
        ):
            reasons.append("unannotated_segment_drawer_not_not_applicable")
        record = {
            "segment_id": segment["segment_id"],
            "status": "passed" if not reasons else "failed",
            "expected": expected,
            "initially_visible": overlay["initially_visible"],
            "interaction_mode": overlay["interaction_mode"],
            "available_on_demand": overlay["available_on_demand"],
            "failure_reasons": reasons,
        }
        portrait_drawer_records.append(record)
        if reasons:
            portrait_drawer_failures.append(record)
    portrait_drawer_covered_ids = {
        record["segment_id"]
        for record in portrait_drawer_records
        if record["expected"] and record["status"] == "passed"
    }
    portrait_drawer_missing_ids = sorted(
        expected_portrait_drawer_ids - portrait_drawer_covered_ids
    )
    portrait_teaching_drawer_gate = {
        "passed": (
            portrait_drawer_contract["passed"]
            and not portrait_drawer_failures
            and not portrait_drawer_missing_ids
            and len(portrait_drawer_records) == len(segments)
        ),
        "status": "passed"
        if (
            portrait_drawer_contract["passed"]
            and not portrait_drawer_failures
            and not portrait_drawer_missing_ids
            and len(portrait_drawer_records) == len(segments)
        )
        else "failed",
        "evidence_scope": PORTRAIT_TEACHING_DRAWER_EVIDENCE_SCOPE,
        "viewport_id": PORTRAIT_VIEWPORT_ID,
        "closed_state_only": True,
        "live_open_state_review": "pending",
        "segment_count": len(segments),
        "annotated_segment_count": len(expected_portrait_drawer_ids),
        "not_applicable_segment_count": len(segments)
        - len(expected_portrait_drawer_ids),
        "covered_segment_ids": sorted(portrait_drawer_covered_ids),
        "missing_segment_ids": portrait_drawer_missing_ids,
        "source_contract": portrait_drawer_contract,
        "evaluation_count": len(portrait_drawer_records),
        "evaluations": portrait_drawer_records,
        "failure_count": len(portrait_drawer_failures),
        "failures": portrait_drawer_failures,
    }

    transport_contract = course_runtime.transport_slot_contract()
    transport_profile_by_viewport = {
        viewport_id: {"profile_id": profile_id, **profile}
        for profile_id, profile in transport_contract["profiles"].items()
        for viewport_id in profile["viewport_ids"]
    }
    transport_records = []
    for segment in segments:
        annotated = segment["visual"]["annotation"] is not None
        for viewport in VIEWPORTS:
            viewport_id = str(viewport["id"])
            profile = transport_profile_by_viewport.get(viewport_id)
            stage = _stage_box(viewport)
            observed_inset = int(viewport["height"]) - stage["y"] - stage["height"]
            reasons = []
            if profile is None:
                reasons.append("transport_profile_missing")
                expected_inset = None
                areas = []
            else:
                expected_inset = profile["height_px"]
                areas = list(profile["areas"])
                if profile["row_count"] != 1:
                    reasons.append("transport_not_single_row")
                if observed_inset != expected_inset:
                    reasons.append("transport_stage_inset_mismatch")
            if not transport_contract["passed"]:
                reasons.append("transport_source_contract_failed")
            nonportrait = viewport_id != PORTRAIT_VIEWPORT_ID
            expected_areas = (
                ["previous", "note", "teaching", "evidence", "next"]
                if nonportrait
                else ["previous", "teaching", "evidence", "next"]
            )
            if areas != expected_areas:
                reasons.append("semantic_area_order_mismatch")
            assignments = {
                area: index for index, area in enumerate(expected_areas, start=1)
            }
            transport_records.append(
                {
                    "segment_id": segment["segment_id"],
                    "viewport_id": viewport_id,
                    "profile_id": None if profile is None else profile["profile_id"],
                    "annotated": annotated,
                    "teaching_slot_state": (
                        "available" if annotated else "reserved_hidden"
                    ),
                    "row_count": None if profile is None else profile["row_count"],
                    "semantic_area_order": areas,
                    "semantic_assignments": assignments,
                    "nonportrait_five_child_contract": (
                        len(areas) == 5 if nonportrait else None
                    ),
                    "observed_stage_bottom_inset_px": observed_inset,
                    "expected_stage_bottom_inset_px": expected_inset,
                    "failure_reasons": reasons,
                    "passed": not reasons,
                }
            )
    transport_failures = [
        record for record in transport_records if not record["passed"]
    ]
    expected_transport_evaluations = course_runtime.EXPECTED_SEGMENTS * len(VIEWPORTS)
    transport_gate = {
        "passed": (
            transport_contract["passed"]
            and len(transport_records) == expected_transport_evaluations
            and not transport_failures
        ),
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "scope": "all_segments_all_viewports",
        "segment_count": len(segments),
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": len(transport_records),
        "expected_evaluation_count": expected_transport_evaluations,
        "annotated_segment_count": sum(
            segment["visual"]["annotation"] is not None for segment in segments
        ),
        "unannotated_segment_count": sum(
            segment["visual"]["annotation"] is None for segment in segments
        ),
        "annotated_evaluation_count": sum(
            record["annotated"] for record in transport_records
        ),
        "unannotated_evaluation_count": sum(
            not record["annotated"] for record in transport_records
        ),
        "standard_stage_bottom_inset_px": (course_runtime.PORTRAIT_TRANSPORT_HEIGHT_PX),
        "short_stage_bottom_inset_px": course_runtime.SHORT_TRANSPORT_HEIGHT_PX,
        "single_row_required": True,
        "hidden_teaching_slot_required": "reserved",
        "source_contract": transport_contract,
        "evaluations": transport_records,
        "failure_count": len(transport_failures),
        "failures": transport_failures,
    }

    disclosure_contract = course_runtime.teaching_annotation_disclosure_contract()
    teaching_disclosure_records = []
    compiled_by_id = {segment["segment_id"]: segment for segment in compiled}
    for segment in segments:
        annotated = segment["visual"]["annotation"] is not None
        quality_segment = compiled_by_id[segment["segment_id"]]
        for evaluation in quality_segment["quality_vector"]["viewport_evaluations"]:
            overlay = evaluation["teaching_overlay"]
            geometry_preserved = (
                evaluation["visual_stage"].get("dock", "none") == "none"
            )
            passed = (
                disclosure_contract["passed"]
                and not overlay["initially_visible"]
                and overlay["available_on_demand"] is annotated
                and geometry_preserved
            )
            teaching_disclosure_records.append(
                {
                    "segment_id": segment["segment_id"],
                    "viewport_id": evaluation["viewport_id"],
                    "annotated": annotated,
                    "initially_visible": overlay["initially_visible"],
                    "available_on_demand": overlay["available_on_demand"],
                    "default_visual_geometry": (
                        "labels_only_full_stage"
                        if geometry_preserved
                        else "overlay_reduced_stage"
                    ),
                    "passed": passed,
                }
            )
    teaching_disclosure_failures = [
        record for record in teaching_disclosure_records if not record["passed"]
    ]
    teaching_disclosure_gate = {
        "passed": (
            disclosure_contract["passed"]
            and len(teaching_disclosure_records)
            == course_runtime.EXPECTED_SEGMENTS * len(VIEWPORTS)
            and not teaching_disclosure_failures
        ),
        "evidence_scope": "deterministic_source_contract_not_live_browser",
        "scope": "all_segments_all_viewports_default_state",
        "segment_count": len(segments),
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": len(teaching_disclosure_records),
        "annotated_evaluation_count": sum(
            record["annotated"] for record in teaching_disclosure_records
        ),
        "closed_by_default": True,
        "geometry_preservation_target": "labels_only_full_stage",
        "source_contract": disclosure_contract,
        "evaluations": teaching_disclosure_records,
        "failure_count": len(teaching_disclosure_failures),
        "failures": teaching_disclosure_failures,
    }

    two_dimensional_segment_ids = {
        segment["segment_id"] for segment in segments if segment["render_mode"] == "2d"
    }
    focused_stroke_records = [
        evaluation["two_dimensional"]["focused_geometry_strokes"]
        for segment in compiled
        if segment["render_mode"] == "2d"
        for evaluation in segment["quality_vector"]["viewport_evaluations"]
    ]
    focused_stroke_failures = [
        record for record in focused_stroke_records if not record["passed"]
    ]
    focused_stroke_covered_segments = {
        record["segment_id"] for record in focused_stroke_records
    }
    expected_focused_stroke_evaluations = len(two_dimensional_segment_ids) * len(
        VIEWPORTS
    )
    focused_geometry_stroke_gate = {
        "passed": (
            focused_stroke_contract["passed"]
            and focused_stroke_covered_segments == two_dimensional_segment_ids
            and len(focused_stroke_records) == expected_focused_stroke_evaluations
            and not focused_stroke_failures
        ),
        "evidence_scope": "deterministic_static_model_not_live_browser",
        "scope": "all_two_dimensional_segments_all_viewports",
        "segment_count": len(two_dimensional_segment_ids),
        "segment_ids": sorted(two_dimensional_segment_ids),
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": len(focused_stroke_records),
        "expected_evaluation_count": expected_focused_stroke_evaluations,
        "minimum_required_stroke_px": MIN_FOCUSED_GEOMETRY_STROKE_PX,
        "minimum_required_dash_px": MIN_FOCUSED_GEOMETRY_DASH_PX,
        "minimum_observed_stroke_px": min(
            (
                record["minimum_effective_stroke_px"]
                for record in focused_stroke_records
                if record["minimum_effective_stroke_px"] is not None
            ),
            default=None,
        ),
        "minimum_observed_dash_px": min(
            (
                record["minimum_effective_dash_px"]
                for record in focused_stroke_records
                if record["minimum_effective_dash_px"] is not None
            ),
            default=None,
        ),
        "dashed_geometry_evaluation_count": sum(
            record["dashed_geometry_count"] > 0 for record in focused_stroke_records
        ),
        "source_contract": focused_stroke_contract,
        "failure_count": len(focused_stroke_failures),
        "failures": focused_stroke_failures,
    }

    decile_size = math.ceil(len(compiled) * 0.10)
    density_ranked = sorted(
        compiled,
        key=lambda item: (
            -item["quality_vector"]["focus_density"]["semantic_item_count"],
            item["sequence"],
        ),
    )
    density_cutoff = density_ranked[decile_size - 1]["quality_vector"]["focus_density"][
        "semantic_item_count"
    ]
    density_pressure_decile = sorted(
        item["segment_id"]
        for item in density_ranked
        if item["quality_vector"]["focus_density"]["semantic_item_count"]
        >= density_cutoff
    )
    risk_ranked = sorted(
        compiled,
        key=lambda item: (-_quality_risk_score(item), item["sequence"]),
    )
    risk_cutoff = _quality_risk_score(risk_ranked[decile_size - 1])
    worst_quality_decile = sorted(
        item["segment_id"]
        for item in risk_ranked
        if _quality_risk_score(item) >= risk_cutoff
    )
    residual_collision_failures = []
    suppression_coverage_failures = []
    clipping_failures = []
    overlay_dominance_failures = []
    compact_kind_cue_failures = []
    geometry_correspondence_failures = []
    header_flow_failures = []
    boundary_disclosure_failures = []
    projected_point_failures = []
    three_label_layout_failures = []
    two_dimensional_label_frame_failures = []
    two_dimensional_label_frame_margins = []
    two_dimensional_evaluation_count = 0
    annotated_2d_composition_failures = []
    annotated_2d_composition_records = []
    annotated_2d_evaluation_count = 0
    annotated_3d_composition_failures = []
    annotated_3d_composition_records = []
    annotated_3d_segment_ids: set[str] = set()
    for segment in compiled:
        for evaluation in segment["quality_vector"]["viewport_evaluations"]:
            overlay = evaluation["teaching_overlay"]
            two_dimensional = evaluation.get("two_dimensional")
            if two_dimensional is not None:
                two_dimensional_evaluation_count += 1
                minimum_margin = two_dimensional["minimum_label_frame_margin_svg_units"]
                if minimum_margin is not None:
                    two_dimensional_label_frame_margins.append(minimum_margin)
                if (
                    two_dimensional["unclamped_label_clipping_count"]
                    or not two_dimensional["label_frame_margin_passed"]
                ):
                    two_dimensional_label_frame_failures.append(
                        {
                            "segment_id": segment["segment_id"],
                            "viewport_id": evaluation["viewport_id"],
                            "clipped_label_ids": two_dimensional[
                                "unclamped_label_clipping_ids"
                            ],
                            "minimum_label_frame_margin_svg_units": minimum_margin,
                            "required_label_frame_margin_svg_units": (
                                two_dimensional["required_label_frame_margin_svg_units"]
                            ),
                        }
                    )
            if overlay["present"] and two_dimensional is not None:
                annotated_2d_evaluation_count += 1
                open_visual_stage = evaluation["open_visual_stage"]
                rendered_area = open_visual_stage["rendered_pixel_area"]
                legacy_area = open_visual_stage["legacy_rendered_pixel_area"]
                rendered_ratio = open_visual_stage["rendered_pixel_ratio_to_full_stage"]
                legacy_ratio = open_visual_stage[
                    "legacy_rendered_pixel_ratio_to_full_stage"
                ]
                max_candidate_area = open_visual_stage[
                    "max_candidate_rendered_pixel_area"
                ]
                defect_policy = LEGACY_PHYSICAL_DEFECT_POLICIES.get(
                    evaluation["viewport_id"]
                )
                legacy_defective = bool(
                    defect_policy
                    and legacy_ratio < defect_policy["maximum_full_stage_ratio"]
                )
                required_gain_ratio = (
                    defect_policy["minimum_gain_ratio"]
                    if legacy_defective and defect_policy is not None
                    else 1.0
                )
                reasons = []
                annotated_2d_composition_records.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "rendered_pixel_ratio_to_full_stage": rendered_ratio,
                        "legacy_rendered_pixel_ratio_to_full_stage": legacy_ratio,
                        "gain_ratio": _round(rendered_ratio / legacy_ratio),
                        "legacy_defective": legacy_defective,
                        "required_gain_ratio": required_gain_ratio,
                    }
                )
                if rendered_ratio + 0.000001 < legacy_ratio:
                    reasons.append("full_stage_rendered_pixel_ratio_regressed")
                if legacy_defective and rendered_ratio + 0.000001 < (
                    legacy_ratio * required_gain_ratio
                ):
                    reasons.append("legacy_physical_defect_material_gain_missing")
                if (
                    not open_visual_stage["max_render_area_candidate_selected"]
                    or abs(rendered_area - max_candidate_area) > 0.01
                ):
                    reasons.append("maximum_render_area_candidate_not_selected")
                if reasons:
                    annotated_2d_composition_failures.append(
                        {
                            "segment_id": segment["segment_id"],
                            "viewport_id": evaluation["viewport_id"],
                            "reasons": reasons,
                            "rendered_pixel_area": rendered_area,
                            "rendered_pixel_ratio_to_full_stage": rendered_ratio,
                            "legacy_rendered_pixel_area": legacy_area,
                            "legacy_rendered_pixel_ratio_to_full_stage": legacy_ratio,
                            "rendered_ratio_gain": _round(
                                rendered_ratio / legacy_ratio
                            ),
                            "legacy_defective": legacy_defective,
                            "required_gain_ratio": required_gain_ratio,
                            "max_candidate_rendered_pixel_area": max_candidate_area,
                        }
                    )
            if overlay["residual_collision_count"]:
                residual_collision_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "label_ids": overlay["residual_collision_ids"],
                    }
                )
            if not overlay["suppressed_labels_covered_by_focus_key"]:
                suppression_coverage_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "label_ids": overlay[
                            "suppressed_labels_missing_from_focus_key"
                        ],
                    }
                )
            if overlay["stage_clipped"]:
                clipping_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "viewport_clipped": overlay["viewport_clipped"],
                        "masthead_clipped": overlay["masthead_clipped"],
                        "transport_clipped": overlay["transport_clipped"],
                    }
                )
            if not overlay["within_stage_coverage"]:
                overlay_dominance_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "height_stage_ratio": overlay["height_stage_ratio"],
                        "width_stage_ratio": overlay["width_stage_ratio"],
                        "area_stage_ratio": overlay["area_stage_ratio"],
                    }
                )
            if (
                overlay["compact_kind_cue_required"]
                and overlay["compact_kind_cue_preserved"] is not True
            ):
                compact_kind_cue_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "kind": overlay["kind"],
                        "missing_css": overlay["compact_kind_cue_missing_css"],
                    }
                )
            correspondence = evaluation["fixed_focus_key"].get(
                "numbered_geometry_correspondence"
            )
            if correspondence is not None and not correspondence["passed"]:
                geometry_correspondence_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "missing_marker_ids": correspondence["missing_marker_ids"],
                        "anchor_covered_by_overlay_ids": correspondence[
                            "anchor_covered_by_overlay_ids"
                        ],
                        "leader_overlay_crossing_ids": correspondence[
                            "leader_overlay_crossing_ids"
                        ],
                        "visible_label_collision_ids": correspondence[
                            "visible_label_collision_ids"
                        ],
                        "leader_visible_label_crossing_ids": correspondence[
                            "leader_visible_label_crossing_ids"
                        ],
                        "leader_marker_crossing_ids": correspondence[
                            "leader_marker_crossing_ids"
                        ],
                        "marker_leader_crossing_ids": correspondence[
                            "marker_leader_crossing_ids"
                        ],
                        "leader_leader_crossing_ids": correspondence[
                            "leader_leader_crossing_ids"
                        ],
                        "anchor_covered_by_prior_marker_ids": correspondence[
                            "anchor_covered_by_prior_marker_ids"
                        ],
                        "future_anchor_obstruction_ids": correspondence[
                            "future_anchor_obstruction_ids"
                        ],
                        "over_maximum_displacement_ids": correspondence[
                            "over_maximum_displacement_ids"
                        ],
                    }
                )
            if not evaluation["header_flow"]["passed"]:
                header_flow_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "header_flow": evaluation["header_flow"],
                    }
                )
            boundary = evaluation["fixed_boundary_note"]
            if (
                boundary["font_px"] < 10.0
                or not boundary["full_copy_accessible"]
                or boundary["visible_clauses"]
                != ["source_gated", "teaching_reference_not_as_built"]
            ):
                boundary_disclosure_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "boundary": boundary,
                    }
                )
            three = evaluation.get("three_dimensional")
            if three is not None and overlay["present"]:
                annotated_3d_segment_ids.add(segment["segment_id"])
                visual_stage = evaluation["open_visual_stage"]
                physical_area = visual_stage["physical_canvas_area"]
                legacy_area = visual_stage["legacy_physical_canvas_area"]
                max_candidate_area = visual_stage["max_candidate_physical_canvas_area"]
                standard_profile = visual_stage["standard_profile"]
                reasons = []
                if physical_area + 0.000001 < legacy_area:
                    reasons.append("physical_canvas_area_regressed")
                if (
                    not visual_stage["max_physical_canvas_area_candidate_selected"]
                    or abs(physical_area - max_candidate_area) > 0.01
                ):
                    reasons.append("maximum_physical_area_candidate_not_selected")
                if not visual_stage["widest_maximum_area_candidate_selected"]:
                    reasons.append("widest_exact_area_tie_not_selected")
                if (
                    standard_profile
                    and visual_stage["width"]
                    < MIN_ANNOTATED_THREE_DIMENSIONAL_STANDARD_CANVAS_WIDTH_PX
                ):
                    reasons.append(
                        "standard_profile_canvas_below_spatial_label_threshold"
                    )
                record = {
                    "segment_id": segment["segment_id"],
                    "viewport_id": evaluation["viewport_id"],
                    "standard_profile": standard_profile,
                    "canvas_width": visual_stage["width"],
                    "canvas_height": visual_stage["height"],
                    "physical_canvas_area": physical_area,
                    "legacy_physical_canvas_area": legacy_area,
                    "physical_canvas_area_gain_ratio": visual_stage[
                        "physical_canvas_area_retention_ratio"
                    ],
                    "max_candidate_physical_canvas_area": max_candidate_area,
                    "selected_standard_overlay_width_px": visual_stage[
                        "selected_standard_overlay_width_px"
                    ],
                    "candidate_standard_overlay_widths_px": visual_stage[
                        "standard_overlay_width_candidates_px"
                    ],
                }
                annotated_3d_composition_records.append(record)
                if reasons:
                    annotated_3d_composition_failures.append(
                        {**record, "reasons": reasons}
                    )
            if three is not None and three["clipped_point_count"]:
                projected_point_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "clipped_point_count": three["clipped_point_count"],
                    }
                )
            if three is not None and (
                three["residual_label_collision_count"]
                or three["residual_stage_clip_count"]
                or not three["fixed_key_fallback_complete"]
            ):
                three_label_layout_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "residual_label_collision_count": three[
                            "residual_label_collision_count"
                        ],
                        "residual_stage_clip_count": three["residual_stage_clip_count"],
                        "fallback_missing_ids": three["fixed_key_fallback_missing_ids"],
                    }
                )
    occupancy_review = _occupancy_review_gate(
        compiled,
        occupancy_reviews,
        candidate_id=occupancy_candidate_id,
    )
    teaching_overlay_stage_edge_clearance = _teaching_overlay_stage_edge_clearance_gate(
        compiled,
        expected_annotated_segment_ids=[
            segment["segment_id"]
            for segment in segments
            if segment["visual"]["annotation"] is not None
        ],
    )
    visual_gates = {
        "two_dimensional_label_clipping": {
            "passed": not two_dimensional_label_frame_failures,
            "scope": "all_two_dimensional_segments_all_viewports",
            "evaluation_count": two_dimensional_evaluation_count,
            "maximum_allowed_clipped_labels": 0,
            "minimum_required_frame_margin_svg_units": (
                shots.TWO_DIMENSIONAL_LABEL_SAFETY_MARGIN
            ),
            "margin_tolerance_svg_units": LABEL_FRAME_MARGIN_TOLERANCE,
            "minimum_observed_frame_margin_svg_units": min(
                two_dimensional_label_frame_margins,
                default=None,
            ),
            "failure_count": len(two_dimensional_label_frame_failures),
            "failures": two_dimensional_label_frame_failures,
        },
        "overlay_residual_label_collision": {
            "passed": not residual_collision_failures,
            "failure_count": len(residual_collision_failures),
            "failures": residual_collision_failures,
        },
        "overlay_suppression_focus_key_coverage": {
            "passed": not suppression_coverage_failures,
            "failure_count": len(suppression_coverage_failures),
            "failures": suppression_coverage_failures,
        },
        "overlay_clipping": {
            "passed": not clipping_failures,
            "failure_count": len(clipping_failures),
            "failures": clipping_failures,
        },
        "teaching_overlay_stage_edge_clearance": (
            teaching_overlay_stage_edge_clearance
        ),
        "overlay_stage_coverage": {
            "passed": not overlay_dominance_failures,
            "maximum_full_width_height_ratio": MAX_OVERLAY_STAGE_HEIGHT_RATIO,
            "maximum_area_ratio": MAX_OVERLAY_STAGE_AREA_RATIO,
            "failure_count": len(overlay_dominance_failures),
            "failures": overlay_dominance_failures,
        },
        "annotated_two_dimensional_physical_composition": {
            "passed": not annotated_2d_composition_failures,
            "metric": "rendered_pixel_ratio_to_full_stage",
            "legacy_standard_overlay_width_px": (
                LEGACY_TEACHING_OVERLAY_STANDARD_WIDTH_PX
            ),
            "candidate_standard_overlay_widths_px": list(
                course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX
            ),
            "widest_width_wins_exact_area_ties": True,
            "legacy_physical_defect_policies": LEGACY_PHYSICAL_DEFECT_POLICIES,
            "legacy_defective_evaluation_count": sum(
                record["legacy_defective"]
                for record in annotated_2d_composition_records
            ),
            "requires_maximum_render_area_candidate": True,
            "requires_no_viewport_regression": True,
            "evaluation_count": annotated_2d_evaluation_count,
            "viewport_summary": [
                {
                    "viewport_id": viewport["id"],
                    "evaluation_count": len(records),
                    "legacy_defective_evaluation_count": sum(
                        record["legacy_defective"] for record in records
                    ),
                    "minimum_rendered_pixel_ratio_to_full_stage": min(
                        record["rendered_pixel_ratio_to_full_stage"]
                        for record in records
                    ),
                    "minimum_legacy_rendered_pixel_ratio_to_full_stage": min(
                        record["legacy_rendered_pixel_ratio_to_full_stage"]
                        for record in records
                    ),
                    "minimum_gain_ratio": min(
                        record["gain_ratio"] for record in records
                    ),
                    "maximum_gain_ratio": max(
                        record["gain_ratio"] for record in records
                    ),
                }
                for viewport in VIEWPORTS
                if (
                    records := [
                        record
                        for record in annotated_2d_composition_records
                        if record["viewport_id"] == viewport["id"]
                    ]
                )
            ],
            "failure_count": len(annotated_2d_composition_failures),
            "failures": annotated_2d_composition_failures,
        },
        "annotated_three_dimensional_physical_composition": {
            "passed": not annotated_3d_composition_failures,
            "scope": "all_annotated_three_dimensional_segments_all_viewports",
            "metric": "physical_canvas_pixel_area",
            "legacy_standard_overlay_width_px": (
                LEGACY_TEACHING_OVERLAY_STANDARD_WIDTH_PX
            ),
            "candidate_standard_overlay_widths_px": list(
                course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX
            ),
            "widest_width_wins_exact_area_ties": True,
            "requires_maximum_physical_area_candidate": True,
            "requires_no_viewport_regression": True,
            "minimum_standard_profile_canvas_width_px": (
                MIN_ANNOTATED_THREE_DIMENSIONAL_STANDARD_CANVAS_WIDTH_PX
            ),
            "segment_count": len(annotated_3d_segment_ids),
            "segment_ids": sorted(annotated_3d_segment_ids),
            "viewport_count": len(VIEWPORTS),
            "evaluation_count": len(annotated_3d_composition_records),
            "standard_profile_evaluation_count": sum(
                record["standard_profile"]
                for record in annotated_3d_composition_records
            ),
            "minimum_observed_standard_profile_canvas_width_px": min(
                (
                    record["canvas_width"]
                    for record in annotated_3d_composition_records
                    if record["standard_profile"]
                ),
                default=None,
            ),
            "viewport_summary": [
                {
                    "viewport_id": viewport["id"],
                    "evaluation_count": len(records),
                    "minimum_canvas_width": min(
                        record["canvas_width"] for record in records
                    ),
                    "minimum_physical_canvas_area": min(
                        record["physical_canvas_area"] for record in records
                    ),
                    "minimum_legacy_physical_canvas_area": min(
                        record["legacy_physical_canvas_area"] for record in records
                    ),
                    "minimum_gain_ratio": min(
                        record["physical_canvas_area_gain_ratio"] for record in records
                    ),
                    "maximum_gain_ratio": max(
                        record["physical_canvas_area_gain_ratio"] for record in records
                    ),
                }
                for viewport in VIEWPORTS
                if (
                    records := [
                        record
                        for record in annotated_3d_composition_records
                        if record["viewport_id"] == viewport["id"]
                    ]
                )
            ],
            "failure_count": len(annotated_3d_composition_failures),
            "failures": annotated_3d_composition_failures,
        },
        "compact_annotation_kind_cue": {
            "passed": not compact_kind_cue_failures,
            "failure_count": len(compact_kind_cue_failures),
            "failures": compact_kind_cue_failures,
        },
        "focus_key_geometry_correspondence": {
            "passed": not geometry_correspondence_failures,
            "maximum_marker_displacement_px": MAX_FOCUS_MARKER_DISPLACEMENT_PX,
            "requires_visible_anchor": True,
            "requires_clear_leader_path": True,
            "avoids_visible_labels": True,
            "failure_count": len(geometry_correspondence_failures),
            "failures": geometry_correspondence_failures,
        },
        "masthead_focus_key_visibility": {
            "passed": not header_flow_failures,
            "failure_count": len(header_flow_failures),
            "failures": header_flow_failures,
        },
        "short_height_focus_key_complete_visibility": short_focus_key_gate,
        "tablet_focus_key_complete_visibility": tablet_focus_key_gate,
        "desktop_focus_key_complete_visibility": desktop_focus_key_gate,
        "portrait_focus_key_complete_visibility": portrait_focus_key_gate,
        "responsive_focus_key_font_floor": responsive_focus_key_font_gate,
        "fixed_grammar_key": fixed_grammar_key_gate,
        "portrait_teaching_drawer": portrait_teaching_drawer_gate,
        "transport_slot_stability": transport_gate,
        "portrait_transport_slot_stability": transport_gate,
        "teaching_annotation_disclosure": teaching_disclosure_gate,
        "focused_geometry_stroke_and_dash_floor": focused_geometry_stroke_gate,
        "responsive_boundary_disclosure": {
            "passed": not boundary_disclosure_failures,
            "minimum_font_px": 10.0,
            "required_visible_clauses": [
                "source_gated",
                "teaching_reference_not_as_built",
            ],
            "failure_count": len(boundary_disclosure_failures),
            "failures": boundary_disclosure_failures,
        },
        "legend_scope": {
            "passed": not unauthorized_legend_ids,
            "allowed_segment_ids": sorted(ALLOWED_LEGEND_SEGMENT_IDS),
            "requested_segment_ids": legend_request_ids,
            "no_request_is_valid": True,
        },
        "three_dimensional_point_clipping": {
            "passed": not projected_point_failures,
            "failure_count": len(projected_point_failures),
            "failures": projected_point_failures,
        },
        "three_dimensional_label_layout": {
            "passed": not three_label_layout_failures,
            "failure_count": len(three_label_layout_failures),
            "failures": three_label_layout_failures,
        },
        "occupancy_review": occupancy_review,
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "aggregation_policy": "none",
        "segment_count": len(compiled),
        "viewport_count": len(VIEWPORTS),
        "viewports": list(VIEWPORTS),
        "protected_copy_policy": {
            "map_copy_ids": sorted(PROTECTED_MAP_COPY_IDS),
            "fixed_masthead_copy_id": "footnote",
            "fixed_masthead_copy": boundary_note,
        },
        "visual_gates": visual_gates,
        "protected_dense_segment_ids": list(PROTECTED_DENSE_SEGMENTS),
        "density_pressure_decile": {
            "requested_size": decile_size,
            "boundary_semantic_item_count": density_cutoff,
            "tie_policy": "include_all_at_boundary",
            "segment_ids": density_pressure_decile,
        },
        "worst_quality_decile": {
            "requested_size": decile_size,
            "metric": "non_density_risk_occurrences_across_all_viewports",
            "boundary_risk_occurrence_count": risk_cutoff,
            "tie_policy": "include_all_at_boundary",
            "segment_ids": worst_quality_decile,
            "risk_occurrence_count_by_segment": {
                item["segment_id"]: _quality_risk_score(item) for item in risk_ranked
            },
        },
        "risk_thresholds": {
            "dense_focus_min_items": DENSE_FOCUS_MIN_ITEMS,
            "max_visible_labels": MAX_VISIBLE_LABELS,
            "max_label_stage_ratio": MAX_LABEL_STAGE_RATIO,
            "max_overlay_stage_height_ratio": MAX_OVERLAY_STAGE_HEIGHT_RATIO,
            "max_overlay_stage_area_ratio": MAX_OVERLAY_STAGE_AREA_RATIO,
            "min_teaching_overlay_stage_edge_clearance_px": (
                MIN_TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX
            ),
            "legacy_physical_defect_policies": LEGACY_PHYSICAL_DEFECT_POLICIES,
            "min_focus_occupancy": MIN_FOCUS_OCCUPANCY,
            "min_projected_occupancy": MIN_PROJECTED_OCCUPANCY,
            "min_dense_annotation_claim_coverage": (
                MIN_DENSE_ANNOTATION_CLAIM_COVERAGE
            ),
        },
        "segments": compiled,
    }


def _payload_digest(value: Any) -> str:
    return hashlib.sha256(scene_pipeline.canonical_payload(value).encode()).hexdigest()


def _objective_invariant_payload(
    segments: list[dict[str, Any]],
) -> list[dict[str, str]]:
    payload = []
    for index, segment in enumerate(segments):
        objective_record = {}
        for field in (
            "segment_id",
            "act_id",
            "act_objective",
            "learning_objective",
        ):
            value = segment.get(field)
            if type(value) is not str or not value.strip():
                raise QualityError(
                    "protected course objective fields must be non-empty strings; "
                    f"segments[{index}].{field}={value!r}"
                )
            objective_record[field] = value
        payload.append(objective_record)
    return payload


def _invariant_digests(runtime_registry: dict[str, Any]) -> dict[str, str]:
    segments = runtime_registry["segments"]
    return {
        "course_objectives": _payload_digest(_objective_invariant_payload(segments)),
        "facts": _payload_digest(
            [
                {
                    "segment_id": segment["segment_id"],
                    "claims": segment["claims"],
                }
                for segment in segments
            ]
        ),
        "topology": _payload_digest(
            [
                {
                    "segment_id": segment["segment_id"],
                    "focus_nodes": segment["focus_nodes"],
                    "focus_edges": segment["focus_edges"],
                    "reveal_ids": segment["reveal_ids"],
                    "reveal_copy_ids": segment["reveal_copy_ids"],
                }
                for segment in segments
            ]
        ),
        "order": _payload_digest(
            [
                {
                    "sequence": segment["sequence"],
                    "segment_id": segment["segment_id"],
                    "depends_on": segment["depends_on"],
                    "transition": segment["transition"],
                }
                for segment in segments
            ]
        ),
        "frames": _payload_digest(
            [
                {
                    "segment_id": segment["segment_id"],
                    "shot_id": segment["id"],
                    "status": segment["status"],
                    "mode": segment["mode"],
                    "render_mode": segment["render_mode"],
                    "camera_anchor": segment["camera_anchor"],
                    "frame": segment["frame"],
                }
                for segment in segments
            ]
        ),
    }


def _all_section_risk_non_regression(
    registry: dict[str, Any], experiment_control: dict[str, Any]
) -> dict[str, Any]:
    """Compare discrete risks and protected metrics for all segment viewports."""
    candidate_by_id = {
        segment["segment_id"]: segment for segment in registry["segments"]
    }
    control_by_id = {
        segment["segment_id"]: segment for segment in experiment_control["segments"]
    }
    if set(candidate_by_id) != set(control_by_id):
        raise QualityError("risk non-regression requires identical segment sets")
    known_flags = frozenset().union(*QUALITY_RISK_DIMENSIONS.values())
    records = []
    unknown_flags: set[str] = set()
    metric_regressions = []

    def metric_record(
        metric_id: str,
        experiment_control_value: float | bool,
        candidate_value: float | bool,
        *,
        experiment_control_present: bool | None = None,
        candidate_present: bool | None = None,
    ) -> dict[str, Any]:
        direction = PROTECTED_NONREGRESSION_METRICS[metric_id]
        uses_float_tolerance = isinstance(
            experiment_control_value, float
        ) or isinstance(candidate_value, float)
        tolerance = METRIC_REGRESSION_TOLERANCE if uses_float_tolerance else 0.0
        delta = float(candidate_value) - float(experiment_control_value)
        if direction == "must_not_decrease":
            regressed = delta < -tolerance
        elif direction == "must_not_increase":
            regressed = delta > tolerance
        elif direction == "must_not_increase_after_presence":
            if experiment_control_present is None or candidate_present is None:
                raise QualityError(
                    f"protected metric {metric_id!r} requires presence evidence"
                )
            target_introduced = not experiment_control_present and candidate_present
            regressed = not target_introduced and delta > tolerance
        else:
            raise QualityError(f"unsupported protected metric direction {direction!r}")
        return {
            "metric_id": metric_id,
            "direction": direction,
            "experiment_control_value": experiment_control_value,
            "candidate_value": candidate_value,
            "delta": _round(delta),
            "tolerance": tolerance,
            "regressed": regressed,
        }

    for segment_id, candidate in candidate_by_id.items():
        control = control_by_id[segment_id]
        if candidate["render_mode"] != control["render_mode"]:
            raise QualityError(
                f"risk non-regression cannot compare unlike render modes for {segment_id}"
            )
        candidate_evaluations = {
            item["viewport_id"]: item
            for item in candidate["quality_vector"]["viewport_evaluations"]
        }
        control_evaluations = {
            item["viewport_id"]: item
            for item in control["quality_vector"]["viewport_evaluations"]
        }
        if set(candidate_evaluations) != set(control_evaluations):
            raise QualityError(
                f"risk non-regression requires identical viewports for {segment_id}"
            )
        candidate_evaluation_union = {
            flag
            for evaluation in candidate_evaluations.values()
            for flag in evaluation["risk_flags"]
        }
        control_evaluation_union = {
            flag
            for evaluation in control_evaluations.values()
            for flag in evaluation["risk_flags"]
        }
        candidate_segment_only = (
            set(candidate["quality_vector"]["risk_flags"]) - candidate_evaluation_union
        )
        control_segment_only = (
            set(control["quality_vector"]["risk_flags"]) - control_evaluation_union
        )
        candidate_annotation_coverage = candidate["quality_vector"][
            "annotation_coverage"
        ]["claim_coverage"]
        control_annotation_coverage = control["quality_vector"]["annotation_coverage"][
            "claim_coverage"
        ]
        for viewport in VIEWPORTS:
            viewport_id = viewport["id"]
            candidate_evaluation = candidate_evaluations[viewport_id]
            control_evaluation = control_evaluations[viewport_id]
            candidate_flags = (
                set(candidate_evaluation["risk_flags"]) | candidate_segment_only
            )
            control_flags = set(control_evaluation["risk_flags"]) | control_segment_only
            unknown_flags.update((candidate_flags | control_flags) - known_flags)
            dimensions = []
            added_flags = []
            for dimension_id, dimension_flags in QUALITY_RISK_DIMENSIONS.items():
                candidate_dimension = sorted(candidate_flags & dimension_flags)
                control_dimension = sorted(control_flags & dimension_flags)
                added = sorted(set(candidate_dimension) - set(control_dimension))
                added_flags.extend(added)
                dimensions.append(
                    {
                        "dimension_id": dimension_id,
                        "experiment_control_risk_flags": control_dimension,
                        "candidate_risk_flags": candidate_dimension,
                        "added_risk_flags": added,
                        "regressed": bool(added),
                    }
                )
            metrics = [
                metric_record(
                    "annotation.claim_coverage",
                    control_annotation_coverage,
                    candidate_annotation_coverage,
                ),
                metric_record(
                    "visible_label_count",
                    control_evaluation["visible_label_count"],
                    candidate_evaluation["visible_label_count"],
                ),
                metric_record(
                    "teaching_overlay.residual_collision_count",
                    control_evaluation["teaching_overlay"]["residual_collision_count"],
                    candidate_evaluation["teaching_overlay"][
                        "residual_collision_count"
                    ],
                ),
                metric_record(
                    "teaching_overlay.stage_clipped",
                    control_evaluation["teaching_overlay"]["stage_clipped"],
                    candidate_evaluation["teaching_overlay"]["stage_clipped"],
                ),
                metric_record(
                    "teaching_overlay.height_stage_ratio",
                    control_evaluation["teaching_overlay"]["height_stage_ratio"],
                    candidate_evaluation["teaching_overlay"]["height_stage_ratio"],
                    experiment_control_present=control_evaluation["teaching_overlay"][
                        "present"
                    ],
                    candidate_present=candidate_evaluation["teaching_overlay"][
                        "present"
                    ],
                ),
                metric_record(
                    "teaching_overlay.area_stage_ratio",
                    control_evaluation["teaching_overlay"]["area_stage_ratio"],
                    candidate_evaluation["teaching_overlay"]["area_stage_ratio"],
                    experiment_control_present=control_evaluation["teaching_overlay"][
                        "present"
                    ],
                    candidate_present=candidate_evaluation["teaching_overlay"][
                        "present"
                    ],
                ),
                metric_record(
                    "fixed_focus_key.numbered_geometry_correspondence.passed",
                    control_evaluation["fixed_focus_key"][
                        "numbered_geometry_correspondence"
                    ]["passed"],
                    candidate_evaluation["fixed_focus_key"][
                        "numbered_geometry_correspondence"
                    ]["passed"],
                ),
            ]
            if candidate["render_mode"] == "2d":
                candidate_render = candidate_evaluation.get("two_dimensional")
                control_render = control_evaluation.get("two_dimensional")
                if candidate_render is None or control_render is None:
                    raise QualityError(
                        f"risk non-regression requires two-dimensional metrics for "
                        f"{segment_id}:{viewport_id}"
                    )
                for metric_name in (
                    "focus_occupancy",
                    "rendered_pixel_ratio_to_full_stage",
                    "projected_base_font_px",
                    "estimated_label_pixels",
                    "label_stage_ratio",
                ):
                    metrics.append(
                        metric_record(
                            f"two_dimensional.{metric_name}",
                            control_render[metric_name],
                            candidate_render[metric_name],
                        )
                    )
            elif candidate["render_mode"] == "3d":
                candidate_render = candidate_evaluation.get("three_dimensional")
                control_render = control_evaluation.get("three_dimensional")
                if candidate_render is None or control_render is None:
                    raise QualityError(
                        f"risk non-regression requires three-dimensional metrics for "
                        f"{segment_id}:{viewport_id}"
                    )
                for metric_name in (
                    "projected_occupancy",
                    "clipped_point_count",
                    "residual_label_collision_count",
                    "residual_stage_clip_count",
                ):
                    metrics.append(
                        metric_record(
                            f"three_dimensional.{metric_name}",
                            control_render[metric_name],
                            candidate_render[metric_name],
                        )
                    )
            else:
                raise QualityError(
                    f"risk non-regression does not support render mode "
                    f"{candidate['render_mode']!r}"
                )
            evaluation_metric_regressions = [
                metric for metric in metrics if metric["regressed"]
            ]
            metric_regressions.extend(
                {
                    "segment_id": segment_id,
                    "viewport_id": viewport_id,
                    **metric,
                }
                for metric in evaluation_metric_regressions
            )
            records.append(
                {
                    "segment_id": segment_id,
                    "viewport_id": viewport_id,
                    "dimensions": dimensions,
                    "metrics": metrics,
                    "added_risk_flags": sorted(added_flags),
                    "metric_regression_ids": [
                        metric["metric_id"] for metric in evaluation_metric_regressions
                    ],
                    "regressed": bool(added_flags or evaluation_metric_regressions),
                }
            )
    expected_count = course_runtime.EXPECTED_SEGMENTS * len(VIEWPORTS)
    if len(records) != expected_count:
        raise QualityError(
            f"risk non-regression expected {expected_count} evaluations, "
            f"found {len(records)}"
        )
    regressions = [record for record in records if record["regressed"]]
    return {
        "passed": not regressions and not unknown_flags,
        "comparison": "candidate_vs_corrected_experiment_control",
        "segment_count": len(candidate_by_id),
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": len(records),
        "dimension_ids": list(QUALITY_RISK_DIMENSIONS),
        "protected_metric_ids": list(PROTECTED_NONREGRESSION_METRICS),
        "float_tolerance": METRIC_REGRESSION_TOLERANCE,
        "taxonomy_complete": not unknown_flags,
        "unknown_risk_flags": sorted(unknown_flags),
        "risk_flag_regression_count": sum(
            len(record["added_risk_flags"]) for record in records
        ),
        "metric_regression_count": len(metric_regressions),
        "metric_regressions": metric_regressions,
        "regression_count": len(regressions),
        "regressions": regressions,
        "evaluations": records,
    }


def _modeled_runtime(
    runtime_registry: dict[str, Any], visual_sources: dict[str, str]
) -> dict[str, Any]:
    modeled = copy.deepcopy(runtime_registry)
    for segment in modeled["segments"]:
        current_visual = segment["visual"]
        if visual_sources["label_source"] == "current":
            visual = {
                "label_policy": current_visual["label_policy"],
                "show_legend": current_visual["show_legend"],
                "label_node_ids": list(current_visual["label_node_ids"]),
                "label_copy_ids": list(current_visual["label_copy_ids"]),
            }
        elif visual_sources["label_source"] == "champion_context":
            visual = {
                "label_policy": "context",
                "show_legend": False,
                "label_node_ids": [],
                "label_copy_ids": [],
            }
        else:
            raise QualityError(
                f"unsupported ratchet label source {visual_sources['label_source']!r}"
            )
        if visual_sources["annotation_source"] == "current":
            visual["annotation"] = copy.deepcopy(current_visual["annotation"])
        elif visual_sources["annotation_source"] == "none":
            visual["annotation"] = None
        else:
            raise QualityError(
                "unsupported ratchet annotation source "
                f"{visual_sources['annotation_source']!r}"
            )
        segment["visual"] = visual
    return modeled


def _absolute_hard_layout_gates(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Evaluate render defects over every segment at every modeled viewport."""

    segments = registry["segments"]
    expected_viewport_ids = [viewport["id"] for viewport in VIEWPORTS]
    if len(segments) != course_runtime.EXPECTED_SEGMENTS:
        raise QualityError(
            "absolute layout gates require exactly "
            f"{course_runtime.EXPECTED_SEGMENTS} segments"
        )
    segment_ids = [segment["segment_id"] for segment in segments]
    if len(segment_ids) != len(set(segment_ids)):
        raise QualityError("absolute layout gates require unique segment IDs")

    residual_collision_failures = []
    suppression_coverage_failures = []
    clipping_failures = []
    two_dimensional_label_frame_failures = []
    projected_point_failures = []
    evaluation_count = 0
    two_dimensional_evaluation_count = 0
    three_dimensional_evaluation_count = 0
    for segment in segments:
        evaluations = segment["quality_vector"]["viewport_evaluations"]
        viewport_ids = [evaluation["viewport_id"] for evaluation in evaluations]
        if viewport_ids != expected_viewport_ids:
            raise QualityError(
                "absolute layout gates require each segment to have the exact "
                f"modeled viewport sequence; segment_id={segment['segment_id']!r}"
            )
        for evaluation in evaluations:
            evaluation_count += 1
            overlay = evaluation["teaching_overlay"]
            if overlay["residual_collision_count"] or overlay["residual_collision_ids"]:
                residual_collision_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "residual_collision_count": overlay["residual_collision_count"],
                        "label_ids": overlay["residual_collision_ids"],
                    }
                )
            if (
                not overlay["suppressed_labels_covered_by_focus_key"]
                or overlay["suppressed_labels_missing_from_focus_key"]
            ):
                suppression_coverage_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        "label_ids": overlay[
                            "suppressed_labels_missing_from_focus_key"
                        ],
                    }
                )
            clipping = {
                "viewport_clipped": overlay["viewport_clipped"],
                "masthead_clipped": overlay["masthead_clipped"],
                "transport_clipped": overlay["transport_clipped"],
                "stage_clipped": overlay["stage_clipped"],
            }
            if any(clipping.values()):
                clipping_failures.append(
                    {
                        "segment_id": segment["segment_id"],
                        "viewport_id": evaluation["viewport_id"],
                        **clipping,
                    }
                )
            two_dimensional = evaluation.get("two_dimensional")
            if two_dimensional is not None:
                two_dimensional_evaluation_count += 1
                if (
                    two_dimensional["unclamped_label_clipping_count"]
                    or not two_dimensional["label_frame_margin_passed"]
                ):
                    two_dimensional_label_frame_failures.append(
                        {
                            "segment_id": segment["segment_id"],
                            "viewport_id": evaluation["viewport_id"],
                            "clipped_label_ids": two_dimensional[
                                "unclamped_label_clipping_ids"
                            ],
                            "minimum_label_frame_margin_svg_units": (
                                two_dimensional["minimum_label_frame_margin_svg_units"]
                            ),
                            "required_label_frame_margin_svg_units": (
                                two_dimensional["required_label_frame_margin_svg_units"]
                            ),
                        }
                    )
            three_dimensional = evaluation.get("three_dimensional")
            if three_dimensional is not None:
                three_dimensional_evaluation_count += 1
                if three_dimensional["clipped_point_count"]:
                    projected_point_failures.append(
                        {
                            "segment_id": segment["segment_id"],
                            "viewport_id": evaluation["viewport_id"],
                            "clipped_point_count": three_dimensional[
                                "clipped_point_count"
                            ],
                        }
                    )

    expected_evaluation_count = course_runtime.EXPECTED_SEGMENTS * len(VIEWPORTS)
    if evaluation_count != expected_evaluation_count:
        raise QualityError(
            "absolute layout gates require exactly "
            f"{expected_evaluation_count} segment-viewport evaluations"
        )
    coverage = {
        "scope": "all_segments_all_viewports",
        "segment_count": len(segments),
        "viewport_count": len(VIEWPORTS),
        "evaluation_count": evaluation_count,
    }

    def gate(failures: list[dict[str, Any]], **policy: Any) -> dict[str, Any]:
        return {
            "passed": not failures,
            **coverage,
            **policy,
            "failure_count": len(failures),
            "failures": failures,
        }

    teaching_overlay_stage_edge_clearance = _teaching_overlay_stage_edge_clearance_gate(
        segments
    )
    return {
        "overlay_residual_label_collision": gate(
            residual_collision_failures,
            maximum_allowed=0,
        ),
        "overlay_suppression_focus_key_coverage": gate(
            suppression_coverage_failures,
            required="all_suppressed_labels",
        ),
        "overlay_clipping": gate(
            clipping_failures,
            maximum_allowed=0,
        ),
        "teaching_overlay_stage_edge_clearance": (
            teaching_overlay_stage_edge_clearance
        ),
        "two_dimensional_label_clipping": gate(
            two_dimensional_label_frame_failures,
            maximum_allowed_clipped_labels=0,
            minimum_required_frame_margin_svg_units=(
                shots.TWO_DIMENSIONAL_LABEL_SAFETY_MARGIN
            ),
            margin_tolerance_svg_units=LABEL_FRAME_MARGIN_TOLERANCE,
            two_dimensional_evaluation_count=two_dimensional_evaluation_count,
        ),
        "three_dimensional_point_clipping": gate(
            projected_point_failures,
            maximum_allowed=0,
            three_dimensional_evaluation_count=(three_dimensional_evaluation_count),
        ),
    }


def _ratchet_result(
    result_id: str,
    visual_sources: dict[str, str],
    registry: dict[str, Any],
    experiment_control_registry: dict[str, Any],
    invariant_digests: dict[str, str],
    *,
    is_champion: bool = False,
) -> dict[str, Any]:
    by_segment = {segment["segment_id"]: segment for segment in registry["segments"]}
    experiment_control_by_segment = {
        segment["segment_id"]: segment
        for segment in experiment_control_registry["segments"]
    }
    label_gate_passed = True
    annotation_gate_passed = True
    risk_non_regression = _all_section_risk_non_regression(
        registry, experiment_control_registry
    )
    segment_vectors = []
    label_risk_types = {
        "visible_label_pressure",
        "label_area_pressure",
        "label_clipping",
    }
    for segment_id in PROTECTED_DENSE_SEGMENTS:
        segment = by_segment[segment_id]
        experiment_control = experiment_control_by_segment[segment_id]
        annotation = segment["quality_vector"]["annotation_coverage"]
        experiment_control_annotation = experiment_control["quality_vector"][
            "annotation_coverage"
        ]
        annotation_flags = []
        if annotation["claim_coverage"] < MIN_DENSE_ANNOTATION_CLAIM_COVERAGE:
            annotation_flags.append("dense_annotation_coverage_gap")
            annotation_gate_passed = False
        experiment_control_evaluations = {
            evaluation["viewport_id"]: evaluation
            for evaluation in experiment_control["quality_vector"][
                "viewport_evaluations"
            ]
        }
        viewport_vectors = []
        for evaluation in segment["quality_vector"]["viewport_evaluations"]:
            experiment_control_evaluation = experiment_control_evaluations[
                evaluation["viewport_id"]
            ]
            two_dimensional = evaluation.get("two_dimensional")
            if two_dimensional is None:
                projected_base_font_px = None
            else:
                projected_base_font_px = two_dimensional["projected_base_font_px"]
            focus_key_chip_count = evaluation["fixed_focus_key"]["chip_count"]
            focus_key_font_px = evaluation["fixed_focus_key"]["font_px"]
            label_flags = sorted(
                label_risk_types.intersection(evaluation["risk_flags"])
            )
            if label_flags:
                label_gate_passed = False
            overlay = evaluation["teaching_overlay"]
            three_dimensional = evaluation.get("three_dimensional")
            clipped_point_count = (
                0
                if three_dimensional is None
                else three_dimensional["clipped_point_count"]
            )
            experiment_control_overlay = experiment_control_evaluation[
                "teaching_overlay"
            ]
            viewport_vectors.append(
                {
                    "viewport_id": evaluation["viewport_id"],
                    "label": {
                        "visible_label_count": evaluation["visible_label_count"],
                        "projected_base_font_px": projected_base_font_px,
                        "fixed_focus_key_chip_count": focus_key_chip_count,
                        "fixed_focus_key_font_px": focus_key_font_px,
                        "risk_flags": label_flags,
                    },
                    "annotation": {
                        "claim_coverage": annotation["claim_coverage"],
                        "covered_claim_count": annotation["covered_claim_count"],
                        "claim_count": annotation["claim_count"],
                        "risk_flags": annotation_flags,
                    },
                    "overlay": {
                        "present": overlay["present"],
                        "height_stage_ratio": overlay["height_stage_ratio"],
                        "width_stage_ratio": overlay["width_stage_ratio"],
                        "area_stage_ratio": overlay["area_stage_ratio"],
                        "within_stage_coverage": overlay["within_stage_coverage"],
                        "compact_kind_cue": overlay["compact_kind_cue"],
                        "compact_kind_cue_preserved": overlay[
                            "compact_kind_cue_preserved"
                        ],
                        "raw_collision_count": overlay["raw_collision_count"],
                        "raw_collision_ids": overlay["raw_collision_ids"],
                        "spatial_suppressed_count": overlay["spatial_suppressed_count"],
                        "spatial_suppressed_ids": overlay["spatial_suppressed_ids"],
                        "residual_collision_count": overlay["residual_collision_count"],
                        "residual_collision_ids": overlay["residual_collision_ids"],
                        "suppressed_labels_covered_by_focus_key": overlay[
                            "suppressed_labels_covered_by_focus_key"
                        ],
                        "viewport_clipped": overlay["viewport_clipped"],
                        "masthead_clipped": overlay["masthead_clipped"],
                        "transport_clipped": overlay["transport_clipped"],
                        "stage_clipped": overlay["stage_clipped"],
                        "risk_flags": overlay["risk_flags"],
                    },
                    "projection": {
                        "clipped_point_count": clipped_point_count,
                    },
                    "delta_from_experiment_control": {
                        "visible_label_count": evaluation["visible_label_count"]
                        - experiment_control_evaluation["visible_label_count"],
                        "annotation_claim_coverage": _round(
                            annotation["claim_coverage"]
                            - experiment_control_annotation["claim_coverage"]
                        ),
                        "overlay_raw_collision_count": (
                            overlay["raw_collision_count"]
                            - experiment_control_overlay["raw_collision_count"]
                        ),
                        "overlay_residual_collision_count": (
                            overlay["residual_collision_count"]
                            - experiment_control_overlay["residual_collision_count"]
                        ),
                    },
                }
            )
        segment_vectors.append(
            {"segment_id": segment_id, "viewports": viewport_vectors}
        )

    targeted_gates = {
        "label_pressure": {
            "passed": label_gate_passed,
            "failure_flags": [
                "visible_label_pressure",
                "label_area_pressure",
                "label_clipping",
            ],
        },
        "dense_annotation_gap": {
            "passed": annotation_gate_passed,
            "minimum_claim_coverage": MIN_DENSE_ANNOTATION_CLAIM_COVERAGE,
            "failure_flag": "dense_annotation_coverage_gap",
        },
    }
    absolute_layout_gates = _absolute_hard_layout_gates(registry)
    occupancy_review = registry["visual_gates"]["occupancy_review"]
    if (
        result_id in OCCUPANCY_REVIEW_CANDIDATE_IDS
        and occupancy_review["candidate_id"] != result_id
    ):
        raise QualityError(
            "occupancy review candidate binding does not match ratchet result; "
            f"expected={result_id!r} actual={occupancy_review['candidate_id']!r}"
        )
    layout_gates = {
        "overlay_residual_label_collision": absolute_layout_gates[
            "overlay_residual_label_collision"
        ],
        "overlay_suppression_focus_key_coverage": absolute_layout_gates[
            "overlay_suppression_focus_key_coverage"
        ],
        "overlay_clipping": absolute_layout_gates["overlay_clipping"],
        "teaching_overlay_stage_edge_clearance": absolute_layout_gates[
            "teaching_overlay_stage_edge_clearance"
        ],
        "two_dimensional_label_clipping": absolute_layout_gates[
            "two_dimensional_label_clipping"
        ],
        "overlay_stage_coverage": registry["visual_gates"]["overlay_stage_coverage"],
        "annotated_two_dimensional_physical_composition": registry["visual_gates"][
            "annotated_two_dimensional_physical_composition"
        ],
        "annotated_three_dimensional_physical_composition": registry["visual_gates"][
            "annotated_three_dimensional_physical_composition"
        ],
        "compact_annotation_kind_cue": registry["visual_gates"][
            "compact_annotation_kind_cue"
        ],
        "focus_key_geometry_correspondence": registry["visual_gates"][
            "focus_key_geometry_correspondence"
        ],
        "masthead_focus_key_visibility": registry["visual_gates"][
            "masthead_focus_key_visibility"
        ],
        "short_height_focus_key_complete_visibility": registry["visual_gates"][
            "short_height_focus_key_complete_visibility"
        ],
        "tablet_focus_key_complete_visibility": registry["visual_gates"][
            "tablet_focus_key_complete_visibility"
        ],
        "desktop_focus_key_complete_visibility": registry["visual_gates"][
            "desktop_focus_key_complete_visibility"
        ],
        "portrait_focus_key_complete_visibility": registry["visual_gates"][
            "portrait_focus_key_complete_visibility"
        ],
        "responsive_focus_key_font_floor": registry["visual_gates"][
            "responsive_focus_key_font_floor"
        ],
        "fixed_grammar_key": registry["visual_gates"]["fixed_grammar_key"],
        "portrait_teaching_drawer": registry["visual_gates"][
            "portrait_teaching_drawer"
        ],
        "transport_slot_stability": registry["visual_gates"][
            "transport_slot_stability"
        ],
        "teaching_annotation_disclosure": registry["visual_gates"][
            "teaching_annotation_disclosure"
        ],
        "focused_geometry_stroke_and_dash_floor": registry["visual_gates"][
            "focused_geometry_stroke_and_dash_floor"
        ],
        "responsive_boundary_disclosure": registry["visual_gates"][
            "responsive_boundary_disclosure"
        ],
        "three_dimensional_point_clipping": absolute_layout_gates[
            "three_dimensional_point_clipping"
        ],
        "three_dimensional_label_layout": registry["visual_gates"][
            "three_dimensional_label_layout"
        ],
        "legend_scope": registry["visual_gates"]["legend_scope"],
        "occupancy_review": occupancy_review,
        "all_section_risk_non_regression": risk_non_regression,
    }
    target_gate_ids = RATCHET_TARGET_GATE_IDS.get(result_id, tuple(targeted_gates))
    candidate_anchor = (
        "ratchet/experiment_control"
        if is_champion
        else f"ratchet/challengers/{result_id}"
    )
    modeled_gate_evidence = {
        f"target:{gate_id}": {
            "status": "passed" if targeted_gates[gate_id]["passed"] else "failed",
            "evidence_ref": (
                f"diagram/course_quality.json#{candidate_anchor}/"
                f"targeted_gates/{gate_id}"
            ),
        }
        for gate_id in target_gate_ids
    }
    for gate_id, gate in layout_gates.items():
        status = (
            gate["status"]
            if gate_id == "occupancy_review"
            else ("passed" if gate["passed"] else "failed")
        )
        modeled_gate_evidence[f"layout:{gate_id}"] = {
            "status": status,
            "evidence_ref": None
            if status == "pending"
            else (
                f"diagram/course_quality.json#{candidate_anchor}/layout_gates/{gate_id}"
            ),
        }
    modeled_gate_statuses = {
        record["status"] for record in modeled_gate_evidence.values()
    }
    if "failed" in modeled_gate_statuses:
        modeled_gate_status = "failed"
    elif "pending" in modeled_gate_statuses:
        modeled_gate_status = "pending"
    else:
        modeled_gate_status = "passed"
    return {
        "id": result_id,
        "role": "experiment_control" if is_champion else "challenger",
        "visual_sources": visual_sources,
        "invariant_digests": invariant_digests,
        "invariants_unchanged_from_experiment_base": True,
        "target_gate_ids": list(target_gate_ids),
        "targeted_gates": targeted_gates,
        "layout_gates": layout_gates,
        "modeled_gate_evidence": modeled_gate_evidence,
        "modeled_gate_status": modeled_gate_status,
        "modeled_eligible": modeled_gate_status == "passed",
        "pareto_disposition": "not_evaluated",
        "final_acceptance": "not_evaluated",
        "final_acceptance_evaluation": None,
        "vectors": segment_vectors,
    }


def _pareto_decision_against_experiment_control(
    candidate: dict[str, Any],
    *,
    required_protection_members: dict[str, Sequence[str]],
    required_modeled_gate_ids: Sequence[str],
) -> dict[str, Any]:
    """Adapt the synthetic-control schema to the pure Pareto contract."""

    contract_candidate = copy.deepcopy(candidate)
    target = contract_candidate.get("target")
    if not isinstance(target, dict) or set(target) != {
        "dimension_id",
        "direction",
        "experiment_control_value",
        "candidate_value",
        "minimum_material_improvement",
        "evidence_ref",
    }:
        raise QualityError(
            "synthetic Pareto target must use the exact experiment-control schema"
        )
    target["champion_value"] = target.pop("experiment_control_value")
    try:
        return ratchet.pareto_decision(
            contract_candidate,
            required_protection_members=required_protection_members,
            required_modeled_gate_ids=required_modeled_gate_ids,
        )
    except ratchet.RatchetContractError as error:
        raise QualityError("synthetic Pareto candidate is invalid") from error


def _gate_group_status(gates: dict[str, dict[str, Any]]) -> str:
    statuses = {record["status"] for record in gates.values()}
    if "failed" in statuses:
        return "failed"
    if "pending" in statuses:
        return "pending"
    return "passed"


def _pareto_gate_records(
    gates: dict[str, dict[str, Any]], gate_ids: Sequence[str]
) -> dict[str, dict[str, Any]]:
    return {
        gate_id: {
            "status": gates[gate_id]["status"],
            "evidence_ref": gates[gate_id]["evidence_ref"],
        }
        for gate_id in gate_ids
    }


def _pareto_blind_reviews(
    reviews: Sequence[dict[str, Any]],
) -> list[dict[str, Any]]:
    return [
        {
            "reviewer_id": review["reviewer_id"],
            "blind": review["blind"],
            "preference": review["preference"],
            "evidence_ref": review["evidence_ref"],
        }
        for review in reviews
    ]


def _derived_blind_review_gate(
    acceptance_candidate: dict[str, Any],
) -> dict[str, Any]:
    candidate_id = acceptance_candidate["candidate_id"]
    provenance_sha256 = acceptance_candidate["candidate_provenance_sha256"]
    reviews = acceptance_candidate["blind_reviews"]
    preferences = [review["preference"] for review in reviews]
    candidate_preferences = preferences.count("candidate")
    pending_reviews = preferences.count("pending")
    if candidate_preferences >= 2:
        status = "passed"
    elif candidate_preferences + pending_reviews >= 2:
        status = "pending"
    else:
        status = "failed"
    if status == "pending":
        evidence = None
        evidence_ref = None
    else:
        evidence = {
            "candidate_id": candidate_id,
            "candidate_provenance_sha256": provenance_sha256,
            "reviewer_ids": [review["reviewer_id"] for review in reviews],
            "preferences": preferences,
            "review_evidence_refs": [review["evidence_ref"] for review in reviews],
            "required_preferences": 2,
            "candidate_preferences": candidate_preferences,
        }
        evidence_ref = _acceptance_evidence_ref(
            candidate_id,
            provenance_sha256,
            "final",
            "blind_review",
            evidence,
        )
    return {
        "status": status,
        "evidence_ref": evidence_ref,
        "evidence": evidence,
        "reason": (
            "At least two blind reviewers prefer the candidate."
            if status == "passed"
            else (
                "Blind review remains unresolved."
                if status == "pending"
                else "Fewer than two blind reviewers can prefer the candidate."
            )
        ),
    }


def _derived_final_gate_evidence(
    acceptance_candidate: dict[str, Any],
) -> dict[str, dict[str, Any]]:
    independent = acceptance_candidate["final_independent_gate_evidence"]
    live = acceptance_candidate["live_gate_evidence"]
    return {
        "prerequisite_correctness_repairs": copy.deepcopy(
            independent["prerequisite_correctness_repairs"]
        ),
        "historical_frozen_champion_viewport_captures": copy.deepcopy(
            independent["historical_frozen_champion_viewport_captures"]
        ),
        "browser": copy.deepcopy(live["browser"]),
        "accessibility_snapshot": copy.deepcopy(live["accessibility_snapshot"]),
        "blind_review": _derived_blind_review_gate(acceptance_candidate),
    }


def _final_acceptance_evaluation(
    pareto_result: dict[str, Any],
    acceptance_candidate: dict[str, Any],
    *,
    expected_current_state: dict[str, Any],
    acceptance_artifacts: Sequence[dict[str, Any]],
) -> dict[str, Any]:
    """Derive final acceptance from Pareto and candidate-bound typed evidence."""

    try:
        pareto_result = ratchet.validate_pareto_result(pareto_result)
    except ratchet.RatchetContractError as error:
        raise QualityError(
            "final acceptance requires a coherent Pareto result"
        ) from error
    candidate_id = pareto_result["candidate_id"]
    if not isinstance(acceptance_candidate, dict):
        raise QualityError("final acceptance candidate evidence must be a mapping")
    evidence_candidate_id = acceptance_candidate.get("candidate_id")
    if evidence_candidate_id != candidate_id:
        raise QualityError(
            "final acceptance evidence must match the Pareto candidate identity"
        )
    provenance_sha256 = _sha256_string(
        acceptance_candidate.get("candidate_provenance_sha256"),
        "final acceptance candidate provenance",
    )
    _validate_candidate_acceptance_evidence(
        acceptance_candidate,
        candidate_id=candidate_id,
        provenance_sha256=provenance_sha256,
        expected_current_state=expected_current_state,
        acceptance_artifacts=acceptance_artifacts,
        location="final_acceptance_candidate",
    )

    static_gate_status = _gate_group_status(
        acceptance_candidate["static_gate_evidence"]
    )
    live_gate_status = _gate_group_status(acceptance_candidate["live_gate_evidence"])
    blind_review_gate = _derived_blind_review_gate(acceptance_candidate)
    if (
        pareto_result["static_gate_status"] != static_gate_status
        or pareto_result["live_gate_status"] != live_gate_status
        or pareto_result["blind_review"]["status"] != blind_review_gate["status"]
    ):
        raise QualityError(
            "final acceptance Pareto state must match supplied candidate evidence"
        )

    gates = _derived_final_gate_evidence(acceptance_candidate)
    if list(gates) != list(FINAL_ACCEPTANCE_GATE_IDS):
        raise QualityError("final acceptance gates must be complete and ordered")
    gate_status = _gate_group_status(gates)
    evidence_final_status = {
        "passed": "accepted",
        "failed": "rejected",
        "pending": "pending",
    }[gate_status]
    candidate_artifacts_materialized = expected_current_state[
        "candidate_course_artifacts_materialized"
    ]
    if not isinstance(candidate_artifacts_materialized, bool):
        raise QualityError("candidate artifact materialization state must be boolean")
    pareto_disposition = pareto_result["disposition"]
    if pareto_disposition == "rejected" or gate_status == "failed":
        status = "rejected"
    elif (
        pareto_disposition == "pending"
        or gate_status == "pending"
        or not candidate_artifacts_materialized
    ):
        status = "pending"
    else:
        status = "accepted"
    reasons = [
        f"acceptance_gate:{gate_id}:{gate['status']}"
        for gate_id, gate in gates.items()
        if gate["status"] != "passed"
    ]
    if pareto_disposition != "accepted":
        reasons.insert(0, f"pareto:{pareto_disposition}")
    if not candidate_artifacts_materialized:
        reasons.append("candidate_artifacts:not_materialized")
    return {
        "candidate_id": candidate_id,
        "candidate_provenance_sha256": provenance_sha256,
        "candidate_current_state_sha256": expected_current_state[
            "candidate_current_state_sha256"
        ],
        "candidate_current_state": copy.deepcopy(expected_current_state),
        "status": status,
        "pareto_disposition": pareto_disposition,
        "manifest_gate_status": gate_status,
        "evidence_final_status": evidence_final_status,
        "candidate_artifact_materialization_status": (
            "materialized" if candidate_artifacts_materialized else "pending"
        ),
        "candidate_artifact_mismatch_ids": copy.deepcopy(
            expected_current_state["candidate_course_artifact_mismatch_ids"]
        ),
        "promotion_eligible": status == "accepted",
        "required_gate_ids": list(FINAL_ACCEPTANCE_GATE_IDS),
        "gate_evidence": gates,
        "reasons": reasons,
    }


def _pareto_candidate(
    runtime_registry: dict[str, Any],
    experiment_control_quality: dict[str, Any],
    experiment_control_result: dict[str, Any],
    candidate_result: dict[str, Any],
    acceptance_evidence: dict[str, Any],
) -> dict[str, Any]:
    candidate_id = candidate_result["id"]
    if acceptance_evidence["candidate_id"] != candidate_id:
        raise QualityError("Pareto evidence input does not match the candidate")
    try:
        target_gate_ids = RATCHET_TARGET_GATE_IDS[candidate_id]
    except KeyError as error:
        raise QualityError(f"unsupported Pareto candidate {candidate_id!r}") from error
    risk_gate = candidate_result["layout_gates"]["all_section_risk_non_regression"]
    regressions_by_segment = Counter(
        record["segment_id"] for record in risk_gate["regressions"]
    )
    ordered_segment_ids = [
        segment["segment_id"] for segment in runtime_registry["segments"]
    ]
    handoff_pairs = list(pairwise(ordered_segment_ids))
    if len(handoff_pairs) != course_runtime.EXPECTED_SEGMENTS - 1:
        raise QualityError("Pareto continuity requires exactly 25 ordered handoffs")
    predecessor_ids = [
        f"handoff:{predecessor_id}->{successor_id}:predecessor"
        for predecessor_id, successor_id in handoff_pairs
    ]
    successor_ids = [
        f"handoff:{predecessor_id}->{successor_id}:successor"
        for predecessor_id, successor_id in handoff_pairs
    ]
    worst_decile_ids = experiment_control_quality["worst_quality_decile"]["segment_ids"]

    invariant_member_ids = [
        f"invariant:{name}" for name in sorted(candidate_result["invariant_digests"])
    ]
    layout_member_ids = [
        f"layout_gate:{gate_id}" for gate_id in sorted(candidate_result["layout_gates"])
    ]
    protected_dimension_ids = invariant_member_ids + layout_member_ids
    shared_consumer_ids = [
        "shared_consumer:course_runtime",
        "shared_consumer:teaching_overlay",
        "shared_consumer:focus_key_and_boundary",
    ]
    required_members = {
        "protected_dimensions": protected_dimension_ids,
        "worst_decile_segments": list(worst_decile_ids),
        "predecessors": predecessor_ids,
        "successors": successor_ids,
        "shared_consumers": shared_consumer_ids,
    }

    def evidence(member_id: str, regressed: bool, anchor: str) -> dict[str, Any]:
        return {
            "member_id": member_id,
            "regressed": regressed,
            "evidence_ref": f"diagram/course_quality.json#{anchor}",
        }

    candidate_anchor = f"ratchet/challengers/{candidate_id}"

    protected_evidence = []
    invariant_regressed = (
        candidate_result["invariant_digests"]
        != experiment_control_result["invariant_digests"]
    )
    for member_id in invariant_member_ids:
        protected_evidence.append(
            evidence(member_id, invariant_regressed, f"{candidate_anchor}/invariants")
        )
    for member_id in layout_member_ids:
        gate_id = member_id.removeprefix("layout_gate:")
        candidate_passed = candidate_result["layout_gates"][gate_id]["passed"]
        control_passed = experiment_control_result["layout_gates"][gate_id]["passed"]
        protected_evidence.append(
            evidence(
                member_id,
                control_passed and not candidate_passed,
                f"{candidate_anchor}/layout_gates/{gate_id}",
            )
        )

    overlay_gate_ids = {
        "overlay_residual_label_collision",
        "overlay_suppression_focus_key_coverage",
        "overlay_clipping",
        "teaching_overlay_stage_edge_clearance",
        "overlay_stage_coverage",
        "annotated_three_dimensional_physical_composition",
        "compact_annotation_kind_cue",
    }
    focus_key_gate_ids = {
        "focus_key_geometry_correspondence",
        "masthead_focus_key_visibility",
        "short_height_focus_key_complete_visibility",
        "tablet_focus_key_complete_visibility",
        "desktop_focus_key_complete_visibility",
        "portrait_focus_key_complete_visibility",
        "responsive_focus_key_font_floor",
        "responsive_boundary_disclosure",
    }
    metric_regression_ids = {
        record["metric_id"] for record in risk_gate["metric_regressions"]
    }

    def layout_gate_regressed(gate_id: str) -> bool:
        return (
            experiment_control_result["layout_gates"][gate_id]["passed"]
            and not candidate_result["layout_gates"][gate_id]["passed"]
        )

    shared_regressions = {
        "shared_consumer:course_runtime": invariant_regressed,
        "shared_consumer:teaching_overlay": any(
            metric_id in TEACHING_OVERLAY_CONSUMER_METRICS
            for metric_id in metric_regression_ids
        )
        or any(layout_gate_regressed(gate_id) for gate_id in overlay_gate_ids),
        "shared_consumer:focus_key_and_boundary": any(
            metric_id.startswith("fixed_focus_key.")
            for metric_id in metric_regression_ids
        )
        or any(layout_gate_regressed(gate_id) for gate_id in focus_key_gate_ids),
    }
    candidate = {
        "candidate_id": candidate_id,
        "target": {
            "dimension_id": f"{'_and_'.join(target_gate_ids)}_cleared",
            "direction": "increase",
            "experiment_control_value": sum(
                experiment_control_result["targeted_gates"][gate_id]["passed"]
                for gate_id in target_gate_ids
            ),
            "candidate_value": sum(
                candidate_result["targeted_gates"][gate_id]["passed"]
                for gate_id in target_gate_ids
            ),
            "minimum_material_improvement": 1,
            "evidence_ref": (
                f"diagram/course_quality.json#{candidate_anchor}/targeted_gates"
            ),
        },
        "protection_evidence": {
            "protected_dimensions": protected_evidence,
            "worst_decile_segments": [
                evidence(
                    segment_id,
                    bool(regressions_by_segment[segment_id]),
                    f"ratchet/experiment_control/worst_quality_decile/{segment_id}",
                )
                for segment_id in worst_decile_ids
            ],
            "predecessors": [
                evidence(
                    member_id,
                    bool(regressions_by_segment[predecessor_id]),
                    (
                        f"{candidate_anchor}/handoffs/"
                        f"{predecessor_id}-to-{successor_id}/predecessor"
                    ),
                )
                for member_id, (predecessor_id, successor_id) in zip(
                    predecessor_ids, handoff_pairs, strict=True
                )
            ],
            "successors": [
                evidence(
                    member_id,
                    bool(regressions_by_segment[successor_id]),
                    (
                        f"{candidate_anchor}/handoffs/"
                        f"{predecessor_id}-to-{successor_id}/successor"
                    ),
                )
                for member_id, (predecessor_id, successor_id) in zip(
                    successor_ids, handoff_pairs, strict=True
                )
            ],
            "shared_consumers": [
                evidence(
                    member_id,
                    shared_regressions[member_id],
                    (
                        f"{candidate_anchor}/shared_consumers/"
                        f"{member_id.removeprefix('shared_consumer:')}"
                    ),
                )
                for member_id in shared_consumer_ids
            ],
        },
        "modeled_gate_evidence": copy.deepcopy(
            candidate_result["modeled_gate_evidence"]
        ),
        "static_gate_evidence": _pareto_gate_records(
            acceptance_evidence["static_gate_evidence"],
            ratchet.STATIC_GATE_IDS,
        ),
        "live_gate_evidence": _pareto_gate_records(
            acceptance_evidence["live_gate_evidence"],
            ratchet.LIVE_GATE_IDS,
        ),
        "blind_reviews": _pareto_blind_reviews(acceptance_evidence["blind_reviews"]),
    }
    decision = _pareto_decision_against_experiment_control(
        candidate,
        required_protection_members=required_members,
        required_modeled_gate_ids=list(candidate_result["modeled_gate_evidence"]),
    )
    return {
        "candidate_id": candidate_id,
        "input": {
            "ordered_handoff_pairs": [
                {
                    "predecessor_id": predecessor_id,
                    "successor_id": successor_id,
                }
                for predecessor_id, successor_id in handoff_pairs
            ],
            "required_protection_members": required_members,
            "required_modeled_gate_ids": list(
                candidate_result["modeled_gate_evidence"]
            ),
            "acceptance_evidence": copy.deepcopy(acceptance_evidence),
            "candidate": candidate,
        },
        "decision": decision,
    }


def compile_ratchet_comparison(
    course: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
    runtime_registry: dict[str, Any],
    quality_registry: dict[str, Any],
    ratchet_manifest: dict[str, Any],
    *,
    source_digest: str,
    materialized_artifact_state: Sequence[dict[str, str]],
) -> dict[str, Any]:
    """Compare isolated visual variants without making an acceptance decision."""
    materialized_artifact_state = _validated_materialized_acceptance_artifact_state(
        materialized_artifact_state
    )
    base_invariants = _invariant_digests(runtime_registry)
    experiment_control_runtime = _modeled_runtime(
        runtime_registry, ratchet_manifest["experiment_control"]
    )
    experiment_control_invariants = _invariant_digests(experiment_control_runtime)
    if experiment_control_invariants != base_invariants:
        raise QualityError("experiment control changed protected course invariants")
    experiment_control_quality = compile_quality_registry(
        course,
        master,
        layout,
        scene,
        ledgers,
        experiment_control_runtime,
        source_digest=source_digest,
        occupancy_reviews=ratchet_manifest["occupancy_reviews"],
        occupancy_candidate_id="experiment_control",
    )
    experiment_control_state = _candidate_current_state(
        candidate_id="experiment_control",
        candidate_provenance_sha256=_experiment_control_occupancy_provenance(
            ratchet_manifest
        ),
        runtime_registry=experiment_control_runtime,
        quality_registry=experiment_control_quality,
        ledgers=ledgers,
        materialized_artifact_state=materialized_artifact_state,
    )
    experiment_control_quality["visual_gates"]["occupancy_review"] = (
        _occupancy_review_gate(
            experiment_control_quality["segments"],
            ratchet_manifest["occupancy_reviews"],
            candidate_id="experiment_control",
            expected_current_state=experiment_control_state,
            capture_manifest=ratchet_manifest["occupancy_capture_manifest"],
        )
    )
    experiment_control_result = _ratchet_result(
        "experiment_control",
        ratchet_manifest["experiment_control"],
        experiment_control_quality,
        experiment_control_quality,
        base_invariants,
        is_champion=True,
    )

    acceptance_by_candidate = {
        record["candidate_id"]: record
        for record in ratchet_manifest["acceptance"]["candidates"]
    }
    challenger_by_id = {
        record["candidate_id"]: record
        for record in ratchet_manifest["challenger_changes"]
    }
    candidate_current_states = {}
    challengers = []
    for variant_id in EXPECTED_VARIANTS:
        visual_sources = ratchet_manifest["variants"][variant_id]
        variant_runtime = _modeled_runtime(runtime_registry, visual_sources)
        variant_invariants = _invariant_digests(variant_runtime)
        if variant_invariants != base_invariants:
            raise QualityError(
                f"ratchet variant {variant_id} changed protected course invariants"
            )
        if variant_id == "combined":
            variant_quality = quality_registry
        else:
            variant_quality = compile_quality_registry(
                course,
                master,
                layout,
                scene,
                ledgers,
                variant_runtime,
                source_digest=source_digest,
                occupancy_reviews=ratchet_manifest["occupancy_reviews"],
                occupancy_candidate_id=variant_id,
            )
        candidate_provenance_sha256 = _candidate_acceptance_provenance(
            ratchet_manifest, challenger_by_id[variant_id]
        )
        current_state = _candidate_current_state(
            candidate_id=variant_id,
            candidate_provenance_sha256=candidate_provenance_sha256,
            runtime_registry=variant_runtime,
            quality_registry=variant_quality,
            ledgers=ledgers,
            materialized_artifact_state=materialized_artifact_state,
        )
        candidate_current_states[variant_id] = current_state
        variant_quality["visual_gates"]["occupancy_review"] = _occupancy_review_gate(
            variant_quality["segments"],
            ratchet_manifest["occupancy_reviews"],
            candidate_id=variant_id,
            expected_current_state=current_state,
            capture_manifest=ratchet_manifest["occupancy_capture_manifest"],
        )
        _validate_candidate_acceptance_evidence(
            acceptance_by_candidate[variant_id],
            candidate_id=variant_id,
            provenance_sha256=candidate_provenance_sha256,
            expected_current_state=current_state,
            acceptance_artifacts=ratchet_manifest["acceptance_artifacts"],
            location=f"acceptance.candidates.{variant_id}",
        )
        challengers.append(
            _ratchet_result(
                variant_id,
                visual_sources,
                variant_quality,
                experiment_control_quality,
                variant_invariants,
            )
        )

    pareto_evaluations = [
        _pareto_candidate(
            runtime_registry,
            experiment_control_quality,
            experiment_control_result,
            challenger,
            acceptance_by_candidate[challenger["id"]],
        )
        for challenger in challengers
    ]
    pareto_by_candidate = {
        evaluation["candidate_id"]: evaluation["decision"]
        for evaluation in pareto_evaluations
    }
    experiment_control_result["pareto_disposition"] = "not_applicable"
    experiment_control_result["final_acceptance"] = "not_applicable"
    experiment_control_result["final_acceptance_evaluation"] = None
    for challenger in challengers:
        pareto_result = pareto_by_candidate[challenger["id"]]
        acceptance_evaluation = _final_acceptance_evaluation(
            pareto_result,
            acceptance_by_candidate[challenger["id"]],
            expected_current_state=candidate_current_states[challenger["id"]],
            acceptance_artifacts=ratchet_manifest["acceptance_artifacts"],
        )
        challenger["pareto_disposition"] = pareto_result["disposition"]
        challenger["final_acceptance"] = acceptance_evaluation["status"]
        challenger["final_acceptance_evaluation"] = acceptance_evaluation

    return {
        "schema_version": ratchet_manifest["schema_version"],
        "comparison_mode": "modeled_on_corrected_candidate_base",
        "frozen_champion_metadata": ratchet_manifest["frozen_champion"],
        "hard_constraints": ratchet_manifest["hard_constraints"],
        "hypothesis_id": ratchet_manifest["hypothesis_id"],
        "hypothesis": ratchet_manifest["hypothesis"],
        "prerequisite_repairs": ratchet_manifest["prerequisite_repairs"],
        "change_owners": ratchet_manifest["change_owners"],
        "finding_owners": ratchet_manifest["finding_owners"],
        "changes": ratchet_manifest["changes"],
        "challenger_changes": ratchet_manifest["challenger_changes"],
        "protected_sentinel_ids": list(PROTECTED_DENSE_SEGMENTS),
        "viewport_ids": [viewport["id"] for viewport in VIEWPORTS],
        "non_aggregation_policy": "preserve_each_sentinel_viewport_vector",
        "experiment_base_invariant_digests": base_invariants,
        "experiment_control": experiment_control_result,
        "experiment_control_worst_quality_decile": experiment_control_quality[
            "worst_quality_decile"
        ],
        "challengers": challengers,
        "pareto": {"evaluations": pareto_evaluations},
        "acceptance": ratchet_manifest["acceptance"],
    }


def compile_dependency_graph(
    ledgers: dict[str, dict[str, Any]],
    runtime_registry: dict[str, Any],
    quality_registry: dict[str, Any],
) -> dict[str, Any]:
    """Build the typed evidence-to-evaluation ownership graph."""
    nodes: dict[str, dict[str, Any]] = {}
    edges: set[tuple[str, str, str]] = set()

    def add_node(node: dict[str, Any]) -> None:
        node_id = node["id"]
        if node_id in nodes and nodes[node_id] != node:
            raise QualityError(f"conflicting graph node {node_id!r}")
        nodes[node_id] = node

    def add_edge(source: str, target: str, relationship: str) -> None:
        edges.add((source, target, relationship))

    claim_fact_refs = {
        fact["ref"]
        for segment in runtime_registry["segments"]
        for claim in segment["claims"]
        for fact in claim["facts"]
    }
    all_source_node_ids: set[str] = set()
    all_fact_node_ids: set[str] = set()
    claim_source_node_ids: set[str] = set()
    known_fact_refs: set[str] = set()
    for ledger_id, ledger in sorted(ledgers.items()):
        for source_id, source in sorted(ledger["sources"].items()):
            if not str(source["kind"]).startswith("primary_"):
                raise QualityError(
                    f"source {ledger_id}:{source_id} is not typed as primary"
                )
            all_source_node_ids.add(_node_id("source", ledger_id, source_id))
        for fact_id, fact in sorted(ledger["facts"].items()):
            fact_ref = f"{ledger_id}:{fact_id}"
            known_fact_refs.add(fact_ref)
            all_fact_node_ids.add(_node_id("fact", ledger_id, fact_id))
            for source_id in fact["source_ids"]:
                if source_id not in ledger["sources"]:
                    raise QualityError(
                        f"fact {fact_ref} references unknown source {source_id!r}"
                    )
                if fact_ref in claim_fact_refs:
                    claim_source_node_ids.add(_node_id("source", ledger_id, source_id))

    unknown_claim_fact_refs = claim_fact_refs - known_fact_refs
    if unknown_claim_fact_refs:
        raise QualityError(
            f"course claims reference unknown facts: {sorted(unknown_claim_fact_refs)}"
        )

    for ledger_id, ledger in sorted(ledgers.items()):
        for source_id, source in sorted(ledger["sources"].items()):
            graph_id = _node_id("source", ledger_id, source_id)
            if graph_id not in claim_source_node_ids:
                continue
            add_node(
                {
                    "id": graph_id,
                    "stage": "source",
                    "type": "primary_source",
                    "ref": f"{ledger_id}:{source_id}",
                    "publisher": source["publisher"],
                    "title": source["title"],
                    "kind": source["kind"],
                    "url": source["url"],
                    "publication_date": source.get("publication_date"),
                    "review_date": source.get("review_date"),
                    "accessed_as_of": source.get("accessed_as_of"),
                    "date_note": source.get("date_note"),
                }
            )
        for fact_id, fact in sorted(ledger["facts"].items()):
            fact_ref = f"{ledger_id}:{fact_id}"
            if fact_ref not in claim_fact_refs:
                continue
            graph_id = _node_id("fact", ledger_id, fact_id)
            add_node(
                {
                    "id": graph_id,
                    "stage": "fact",
                    "type": "evidence_fact",
                    "ref": fact_ref,
                    "value": fact["value"],
                    "basis": fact["basis"],
                    "scope": fact["scope"],
                    "lifecycle": fact["lifecycle"],
                    "posture": fact["posture"],
                    "as_of": fact["as_of"],
                }
            )
            for source_id in fact["source_ids"]:
                add_edge(
                    _node_id("source", ledger_id, source_id),
                    graph_id,
                    "supports_fact",
                )

    quality_by_segment = {
        segment["segment_id"]: segment for segment in quality_registry["segments"]
    }
    segment_node_ids: dict[str, str] = {}
    for segment in runtime_registry["segments"]:
        segment_id = segment["segment_id"]
        segment_node_id = _node_id("segment", segment_id)
        segment_node_ids[segment_id] = segment_node_id
        add_node(
            {
                "id": segment_node_id,
                "stage": "segment",
                "type": "course_segment",
                "segment_id": segment_id,
                "sequence": segment["sequence"],
                "title": segment["title"],
            }
        )
        for claim in segment["claims"]:
            binding = claim["binding"]
            if binding not in CLAIM_NODE_TYPES:
                raise QualityError(
                    f"segment {segment_id}: unsupported claim binding {binding!r}"
                )
            target_ids: dict[str, set[str]] = {"node": set(), "edge": set()}
            target_records: dict[tuple[str, str], dict[str, Any]] = {}
            fact_topology_targets: dict[str, list[dict[str, Any]]] = {}
            for fact in claim["facts"]:
                targets = fact.get("topology_targets")
                if not isinstance(targets, list):
                    raise QualityError(
                        f"claim {segment_id}:{claim['id']} fact {fact['ref']}: "
                        "topology_targets must be a list"
                    )
                if binding == "topology" and not targets:
                    raise QualityError(
                        f"topology claim {segment_id}:{claim['id']} fact "
                        f"{fact['ref']} has no selected physical target"
                    )
                if binding == "overlay" and targets:
                    raise QualityError(
                        f"overlay claim {segment_id}:{claim['id']} fact "
                        f"{fact['ref']} leaked physical targets"
                    )
                fact_target_records = []
                for target in targets:
                    kind = target.get("kind")
                    target_id = target.get("id")
                    if kind not in target_ids or not isinstance(target_id, str):
                        raise QualityError(
                            f"claim {segment_id}:{claim['id']} fact {fact['ref']}: "
                            f"invalid topology target {target!r}"
                        )
                    target_ids[kind].add(target_id)
                    target_record = {
                        "kind": kind,
                        "id": target_id,
                        "label": target["label"],
                        "presence": target["presence"],
                        "lifecycle": target["lifecycle"],
                    }
                    target_records[(kind, target_id)] = target_record
                    fact_target_records.append(target_record)
                if fact["ref"] in fact_topology_targets:
                    raise QualityError(
                        f"claim {segment_id}:{claim['id']} repeats fact {fact['ref']!r}"
                    )
                fact_topology_targets[fact["ref"]] = fact_target_records
            if target_ids["node"] - set(segment["focus_nodes"]):
                raise QualityError(
                    f"topology claim {segment_id}:{claim['id']} targets nodes "
                    "outside the selected segment focus"
                )
            if target_ids["edge"] - set(segment["focus_edges"]):
                raise QualityError(
                    f"topology claim {segment_id}:{claim['id']} targets edges "
                    "outside the selected segment focus"
                )

            claim_node_id = _node_id("topology", segment_id, claim["id"])
            add_node(
                {
                    "id": claim_node_id,
                    "stage": "topology",
                    "type": CLAIM_NODE_TYPES[binding],
                    "claim_id": claim["id"],
                    "segment_id": segment_id,
                    "assertion": claim["assertion"],
                    "binding": binding,
                    "fact_refs": [fact["ref"] for fact in claim["facts"]],
                    "physically_bound": binding == "topology",
                    "topology_targets": [
                        target_records[key] for key in sorted(target_records)
                    ],
                    "fact_topology_targets": fact_topology_targets,
                    "overlay_scope": {
                        "kind": "segment_local",
                        "segment_id": segment_id,
                    }
                    if binding == "overlay"
                    else None,
                }
            )
            add_edge(claim_node_id, segment_node_id, "binds_segment")
            for fact in claim["facts"]:
                fact_node_id = _node_id("fact", *fact["ref"].split(":", 1))
                if fact_node_id not in nodes:
                    raise QualityError(
                        f"claim {segment_id}:{claim['id']} references unknown fact "
                        f"{fact['ref']!r}"
                    )
                add_edge(fact_node_id, claim_node_id, "substantiates_topology")

        shot_node_id = _node_id("shot", segment_id, segment["id"])
        add_node(
            {
                "id": shot_node_id,
                "stage": "shot",
                "type": "camera_shot",
                "shot_id": segment["id"],
                "segment_id": segment_id,
                "camera_anchor": segment["camera_anchor"],
                "mode": segment["mode"],
            }
        )
        add_edge(segment_node_id, shot_node_id, "requests_shot")

        frame_node_id = _node_id("frame", segment_id)
        add_node(
            {
                "id": frame_node_id,
                "stage": "frame",
                "type": "provisional_frame_spec",
                "segment_id": segment_id,
                "render_mode": segment["render_mode"],
                "frame": segment["frame"],
                "render_status": "pending_browser_capture",
                "capture_digest": None,
            }
        )
        add_edge(shot_node_id, frame_node_id, "specifies_frame")

        quality_segment = quality_by_segment.get(segment_id)
        if quality_segment is None:
            raise QualityError(f"segment {segment_id}: missing quality vector")
        for evaluation in quality_segment["quality_vector"]["viewport_evaluations"]:
            evaluation_node_id = _node_id(
                "evaluation", segment_id, evaluation["viewport_id"]
            )
            add_node(
                {
                    "id": evaluation_node_id,
                    "stage": "evaluation",
                    "type": "modeled_viewport_evaluation",
                    "segment_id": segment_id,
                    "viewport_id": evaluation["viewport_id"],
                    "risk_flags": evaluation["risk_flags"],
                    "evidence_status": "static_model_only",
                }
            )
            add_edge(frame_node_id, evaluation_node_id, "modeled_at")

    for segment in runtime_registry["segments"]:
        target = segment_node_ids[segment["segment_id"]]
        for dependency in segment["depends_on"]:
            source = segment_node_ids.get(dependency)
            if source is None:
                raise QualityError(
                    f"segment {segment['segment_id']}: unknown dependency "
                    f"{dependency!r}"
                )
            add_edge(source, target, "teaching_dependency")

    for predecessor, successor in pairwise(runtime_registry["segments"]):
        add_edge(
            segment_node_ids[predecessor["segment_id"]],
            segment_node_ids[successor["segment_id"]],
            "transitions_to",
        )

    node_list = sorted(nodes.values(), key=lambda node: node["id"])
    edge_list = [
        {"from": source, "to": target, "type": relationship}
        for source, target, relationship in sorted(edges)
    ]
    stage_counts = Counter(node["stage"] for node in node_list)
    type_counts = Counter(node["type"] for node in node_list)
    claim_fact_node_ids = {
        _node_id("fact", *fact_ref.split(":", 1)) for fact_ref in claim_fact_refs
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "source_digest": quality_registry["source_digest"],
        "dependency_path": list(GRAPH_STAGES),
        "completion_boundary": {
            "frame_capture": "pending_browser_capture",
            "live_evaluation": "pending_browser_and_accessibility",
        },
        "claim_node_types": sorted(CLAIM_NODE_TYPES.values()),
        "evidence_inventory": {
            "policy": EVIDENCE_INVENTORY_POLICY,
            "total_source_count": len(all_source_node_ids),
            "total_fact_count": len(all_fact_node_ids),
            "claim_chain_source_count": len(claim_source_node_ids),
            "claim_chain_fact_count": len(claim_fact_node_ids),
            "inventory_only_source_ids": sorted(
                all_source_node_ids - claim_source_node_ids
            ),
            "inventory_only_fact_ids": sorted(all_fact_node_ids - claim_fact_node_ids),
        },
        "node_count": len(node_list),
        "edge_count": len(edge_list),
        "stage_counts": {stage: stage_counts.get(stage, 0) for stage in GRAPH_STAGES},
        "node_type_counts": dict(sorted(type_counts.items())),
        "nodes": node_list,
        "edges": edge_list,
    }


def impact_cone(
    graph: dict[str, Any], start_node_ids: str | Iterable[str]
) -> dict[str, Any]:
    """Return the deterministic downstream cone for one or more graph nodes."""
    starts = (
        [start_node_ids] if isinstance(start_node_ids, str) else list(start_node_ids)
    )
    starts = sorted(set(starts))
    known_nodes = {node["id"]: node for node in graph["nodes"]}
    unknown = set(starts) - set(known_nodes)
    if unknown:
        raise QualityError(f"impact cone starts from unknown nodes: {sorted(unknown)}")

    adjacency: dict[str, list[str]] = defaultdict(list)
    for edge in graph["edges"]:
        adjacency[edge["from"]].append(edge["to"])
    for targets in adjacency.values():
        targets.sort()

    distances = {node_id: 0 for node_id in starts}
    queue = deque(starts)
    while queue:
        source = queue.popleft()
        for target in adjacency.get(source, []):
            distance = distances[source] + 1
            if target not in distances or distance < distances[target]:
                distances[target] = distance
                queue.append(target)

    ordered = sorted(distances, key=lambda node_id: (distances[node_id], node_id))
    by_stage = {
        stage: [
            node_id for node_id in ordered if known_nodes[node_id]["stage"] == stage
        ]
        for stage in GRAPH_STAGES
    }
    return {
        "start_node_ids": starts,
        "node_ids": ordered,
        "distance_by_node_id": {node_id: distances[node_id] for node_id in ordered},
        "by_stage": by_stage,
        "maximum_distance": max(distances.values(), default=0),
    }


def build_artifacts() -> tuple[str, str, str]:
    course, cameras, master, layout, scene, ledgers, visuals = (
        course_runtime.load_inputs()
    )
    ratchet_manifest = load_ratchet_manifest()
    champion_verification = champion_pipeline.require_frozen_champion(
        ratchet_manifest["frozen_champion"],
        observe_mutable_provenance=False,
    )
    runtime_digest = course_runtime._source_digest(course)
    runtime_registry = course_runtime.compile_registry(
        course,
        cameras,
        master,
        layout,
        scene,
        ledgers,
        visuals,
        source_digest=runtime_digest,
    )
    materialized_artifact_state = _materialized_acceptance_artifact_state()
    current_audit_subject = _current_audit_subject_state(
        runtime_digest=runtime_digest,
        runtime_registry=runtime_registry,
        ratchet_manifest=ratchet_manifest,
        materialized_artifact_state=materialized_artifact_state,
    )
    segment_ids = [segment["segment_id"] for segment in runtime_registry["segments"]]
    audit_manifest = load_audit_manifest(segment_ids)
    _validate_audit_change_links(audit_manifest, ratchet_manifest)
    source_digest = _quality_source_digest(
        runtime_digest, ratchet_manifest, audit_manifest
    )
    quality_registry = compile_quality_registry(
        course,
        master,
        layout,
        scene,
        ledgers,
        runtime_registry,
        source_digest=source_digest,
        cameras=cameras,
        occupancy_reviews=ratchet_manifest["occupancy_reviews"],
    )
    quality_registry["frozen_champion"] = {
        "metadata": ratchet_manifest["frozen_champion"],
        "static_verification": champion_verification,
        "eligible_as_experiment_control": False,
        "eligibility_reason": (
            "historical viewport captures and quality vectors are unavailable"
        ),
    }
    ratchet_comparison = compile_ratchet_comparison(
        course,
        master,
        layout,
        scene,
        ledgers,
        runtime_registry,
        quality_registry,
        ratchet_manifest,
        source_digest=source_digest,
        materialized_artifact_state=materialized_artifact_state,
    )
    current_dispositions = _current_challenger_dispositions(
        audit_manifest,
        ratchet_manifest,
        ratchet_comparison,
    )
    try:
        reconciled_rounds = ratchet.reconcile_audit_round_dispositions(
            audit_manifest["rounds"],
            segment_ids=segment_ids,
            current_challenger_dispositions=current_dispositions,
        )
        saturation = ratchet.evaluate_saturation(
            audit_manifest["rounds"],
            segment_ids=segment_ids,
            high_priority_threshold=audit_manifest["high_priority_threshold"],
            current_challenger_dispositions=current_dispositions,
            current_audit_subject_sha256=current_audit_subject["audit_subject_sha256"],
        )
    except ratchet.RatchetContractError as error:
        raise QualityError(
            f"invalid current challenger disposition reconciliation: {error}"
        ) from error
    quality_registry["audit_program"] = {
        **audit_manifest,
        "rounds": reconciled_rounds,
        "saturation": saturation,
    }
    quality_registry["ratchet"] = ratchet_comparison
    graph = compile_dependency_graph(ledgers, runtime_registry, quality_registry)
    quality_json = scene_pipeline.canonical_payload(quality_registry) + "\n"
    graph_json = scene_pipeline.canonical_payload(graph) + "\n"
    return quality_json, graph_json, source_digest


def _acceptance_report_spec(
    evidence_id: str,
) -> tuple[str, str, str, Any]:
    specs = {
        "static:validation": (
            "static",
            "validation",
            "report_artifact_sha256",
            _validate_validation_evidence,
        ),
        "static:deterministic_generation": (
            "static",
            "deterministic_generation",
            "report_artifact_sha256",
            _validate_deterministic_generation_evidence,
        ),
        "static:evidence": (
            "static",
            "evidence",
            "report_artifact_sha256",
            _validate_evidence_gate_evidence,
        ),
        "live:browser": (
            "live",
            "browser",
            "report_artifact_sha256",
            _validate_browser_evidence,
        ),
        "live:accessibility_snapshot": (
            "live",
            "accessibility_snapshot",
            "report_artifact_sha256",
            _validate_accessibility_evidence,
        ),
        "final:prerequisite_correctness_repairs": (
            "final",
            "prerequisite_correctness_repairs",
            "report_artifact_sha256",
            _validate_prerequisite_evidence,
        ),
        "final:historical_frozen_champion_viewport_captures": (
            "final",
            "historical_frozen_champion_viewport_captures",
            "report_artifact_sha256",
            _validate_historical_capture_evidence,
        ),
    }
    if evidence_id in specs:
        return specs[evidence_id]
    prefix = "blind_review:"
    if evidence_id.startswith(prefix):
        reviewer_id = evidence_id.removeprefix(prefix)
        if reviewer_id in BLIND_REVIEWER_IDS:
            return (
                "blind_review",
                reviewer_id,
                "report_artifact_sha256",
                None,
            )
    raise QualityError(f"unsupported acceptance evidence_id {evidence_id!r}")


def _write_content_addressed_evidence(
    repository_root: Path,
    artifact_path: str,
    payload: bytes,
) -> Path:
    root = repository_root.resolve()
    if not root.is_dir():
        raise QualityError("acceptance repository root must be an existing directory")
    relative = PurePosixPath(artifact_path)
    if relative.is_absolute() or ".." in relative.parts:
        raise QualityError("acceptance artifact path must be repository-relative")
    parent = root
    for part in relative.parts[:-1]:
        parent /= part
        if parent.exists() or parent.is_symlink():
            if parent.is_symlink() or not parent.is_dir():
                raise QualityError(
                    "acceptance artifact path must not traverse a non-directory or "
                    "symbolic link"
                )
        else:
            try:
                parent.mkdir()
            except OSError as error:
                raise QualityError(
                    f"acceptance artifact directory could not be created: {error}"
                ) from error
    target = root.joinpath(*relative.parts)
    if target.exists() or target.is_symlink():
        if target.is_symlink() or not target.is_file():
            raise QualityError(
                "acceptance artifact target must be a regular non-symbolic-link file"
            )
        try:
            retained = target.read_bytes()
        except OSError as error:
            raise QualityError(
                f"acceptance artifact target could not be read: {error}"
            ) from error
        if retained != payload:
            raise QualityError(
                "content-addressed acceptance artifact already exists with different bytes"
            )
        return target
    try:
        with target.open("xb") as destination:
            destination.write(payload)
    except OSError as error:
        raise QualityError(
            f"acceptance artifact could not be materialized: {error}"
        ) from error
    return target


def materialize_acceptance_report(
    value: Any,
    *,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    expected_fields = {
        "schema_version",
        "candidate_id",
        "candidate_current_state_sha256",
        "evidence_id",
        "outcome",
        "typed_evidence",
    }
    if not isinstance(value, dict) or set(value) != expected_fields:
        raise QualityError("acceptance report input fields must be exact")
    if type(value["schema_version"]) is not int or value["schema_version"] != SCHEMA_VERSION:
        raise QualityError("acceptance report schema_version is invalid")
    candidate_id = value["candidate_id"]
    if candidate_id not in EXPECTED_VARIANTS:
        raise QualityError("acceptance report candidate_id is invalid")
    current_state_sha256 = _sha256_string(
        value["candidate_current_state_sha256"],
        "acceptance report candidate_current_state_sha256",
    )
    evidence_id = value["evidence_id"]
    if not isinstance(evidence_id, str):
        raise QualityError("acceptance report evidence_id must be a string")
    domain, ref_id, digest_field, validator = _acceptance_report_spec(evidence_id)
    outcome = value["outcome"]
    if not isinstance(outcome, str) or outcome == "pending":
        raise QualityError("acceptance report outcome must be explicitly resolved")
    report_evidence = value["typed_evidence"]
    if not isinstance(report_evidence, dict):
        raise QualityError("acceptance report typed_evidence must be a mapping")
    if digest_field in report_evidence:
        raise QualityError(
            f"acceptance report typed_evidence must omit self-digest field {digest_field!r}"
        )
    if report_evidence.get("candidate_id") != candidate_id:
        raise QualityError("acceptance report candidate binding is inconsistent")
    if report_evidence.get("candidate_current_state_sha256") != current_state_sha256:
        raise QualityError("acceptance report current-state binding is inconsistent")
    provenance_sha256 = _sha256_string(
        report_evidence.get("candidate_provenance_sha256"),
        "acceptance report candidate_provenance_sha256",
    )
    evidence = copy.deepcopy(report_evidence)
    evidence[digest_field] = "0" * 64
    if domain == "blind_review":
        evidence = _acceptance_evidence_common(
            evidence,
            candidate_id=candidate_id,
            provenance_sha256=provenance_sha256,
            expected_current_state=None,
            expected_fields={
                "reviewer_id",
                "blind",
                "preference",
                "comparison_artifact_sha256",
                "report_artifact_sha256",
            },
            location="acceptance report typed_evidence",
        )
        if (
            evidence["reviewer_id"] != ref_id
            or evidence["blind"] is not True
            or evidence["preference"] != outcome
            or outcome not in ratchet.REVIEW_PREFERENCES - {"pending"}
        ):
            raise QualityError("acceptance report blind-review outcome is inconsistent")
    else:
        derived_outcome = validator(
            evidence,
            candidate_id=candidate_id,
            provenance_sha256=provenance_sha256,
            expected_current_state=None,
            location="acceptance report typed_evidence",
        )
        if outcome != derived_outcome:
            raise QualityError(
                "acceptance report outcome does not match its typed evidence"
            )

    envelope = copy.deepcopy(value)
    report_bytes = (scene_pipeline.canonical_payload(envelope) + "\n").encode()
    artifact_sha256 = hashlib.sha256(report_bytes).hexdigest()
    artifact_path = _canonical_acceptance_report_path(artifact_sha256)
    _write_content_addressed_evidence(
        repository_root,
        artifact_path,
        report_bytes,
    )
    evidence[digest_field] = artifact_sha256
    evidence_ref = _acceptance_evidence_ref(
        candidate_id,
        provenance_sha256,
        domain,
        ref_id,
        evidence,
    )
    resolution_field = "preference" if domain == "blind_review" else "status"
    return {
        "schema_version": SCHEMA_VERSION,
        "acceptance_artifact": {
            "candidate_id": candidate_id,
            "candidate_current_state_sha256": current_state_sha256,
            "evidence_id": evidence_id,
            "artifact_path": artifact_path,
            "artifact_sha256": artifact_sha256,
        },
        "manifest_patch": {
            resolution_field: outcome,
            "evidence_ref": evidence_ref,
            "evidence": evidence,
        },
    }


def _rfc3339_timestamp(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip() or "T" not in value:
        raise QualityError(f"{location} must be an RFC3339 timestamp")
    normalized = f"{value[:-1]}+00:00" if value.endswith("Z") else value
    try:
        timestamp = datetime.fromisoformat(normalized)
    except ValueError as error:
        raise QualityError(f"{location} must be an RFC3339 timestamp") from error
    if timestamp.tzinfo is None:
        raise QualityError(f"{location} must include a timezone")
    return value


def materialize_occupancy_evidence(
    value: Any,
    capture_bytes: bytes,
    *,
    repository_root: Path = ROOT,
) -> dict[str, Any]:
    expected_fields = {
        "schema_version",
        "candidate_id",
        "candidate_provenance_sha256",
        "candidate_current_state_sha256",
        "validation_compiler_implementation_sha256",
        "evaluation",
        "decision",
        "reviewer_id",
        "reviewed_at",
        "rationale",
    }
    if not isinstance(value, dict) or set(value) != expected_fields:
        raise QualityError("occupancy evidence input fields must be exact")
    if type(value["schema_version"]) is not int or value["schema_version"] != SCHEMA_VERSION:
        raise QualityError("occupancy evidence schema_version is invalid")
    candidate_id = value["candidate_id"]
    if candidate_id not in EXPECTED_VARIANTS:
        raise QualityError("occupancy evidence requires a challenger candidate_id")
    provenance_sha256 = _sha256_string(
        value["candidate_provenance_sha256"],
        "occupancy evidence candidate_provenance_sha256",
    )
    current_state_sha256 = _sha256_string(
        value["candidate_current_state_sha256"],
        "occupancy evidence candidate_current_state_sha256",
    )
    compiler_sha256 = _sha256_string(
        value["validation_compiler_implementation_sha256"],
        "occupancy evidence validation_compiler_implementation_sha256",
    )
    evaluation = value["evaluation"]
    evaluation_fields = {
        "segment_id",
        "viewport_id",
        "risk_flags",
        "metric_id",
        "observed_value",
    }
    if not isinstance(evaluation, dict) or set(evaluation) != evaluation_fields:
        raise QualityError("occupancy evidence evaluation fields must be exact")
    segment_id = evaluation["segment_id"]
    viewport_id = evaluation["viewport_id"]
    if not isinstance(segment_id, str) or not segment_id:
        raise QualityError("occupancy evidence segment_id must be non-empty")
    if viewport_id not in {viewport["id"] for viewport in VIEWPORTS}:
        raise QualityError("occupancy evidence viewport_id is invalid")
    risk_flags = evaluation["risk_flags"]
    if (
        not isinstance(risk_flags, list)
        or len(risk_flags) != 1
        or risk_flags[0] not in OCCUPANCY_RISK_FLAGS
    ):
        raise QualityError("occupancy evidence must identify exactly one occupancy risk")
    if evaluation["metric_id"] != OCCUPANCY_METRIC_BY_RISK_FLAG[risk_flags[0]]:
        raise QualityError("occupancy evidence metric_id does not match its risk")
    observed_value = evaluation["observed_value"]
    if (
        isinstance(observed_value, bool)
        or not isinstance(observed_value, (int, float))
        or not math.isfinite(float(observed_value))
    ):
        raise QualityError("occupancy evidence observed_value must be finite")
    decision = value["decision"]
    if decision not in {"approved", "rejected"}:
        raise QualityError("occupancy evidence decision must be approved or rejected")
    reviewer_id = value["reviewer_id"]
    rationale = value["rationale"]
    if not isinstance(reviewer_id, str) or not reviewer_id.strip():
        raise QualityError("occupancy evidence reviewer_id must be non-empty")
    if not isinstance(rationale, str) or not rationale.strip():
        raise QualityError("occupancy evidence rationale must be non-empty")
    reviewed_at = _rfc3339_timestamp(
        value["reviewed_at"],
        "occupancy evidence reviewed_at",
    )
    if not isinstance(capture_bytes, bytes):
        raise QualityError("occupancy capture must be bytes")
    _validate_occupancy_capture_png(
        capture_bytes,
        viewport_id=viewport_id,
        location="occupancy capture",
    )
    artifact_sha256 = hashlib.sha256(capture_bytes).hexdigest()
    modeled_evaluation_sha256 = _occupancy_modeled_evaluation_sha256(
        candidate_id,
        current_state_sha256,
        evaluation,
    )
    capture = {
        "candidate_id": candidate_id,
        "candidate_current_state_sha256": current_state_sha256,
        "validation_compiler_implementation_sha256": compiler_sha256,
        "segment_id": segment_id,
        "viewport_id": viewport_id,
        "modeled_evaluation_sha256": modeled_evaluation_sha256,
        "artifact_path": "",
        "artifact_sha256": artifact_sha256,
    }
    capture["artifact_path"] = _canonical_occupancy_capture_path(capture)
    _write_content_addressed_evidence(
        repository_root,
        capture["artifact_path"],
        capture_bytes,
    )
    live_review = {
        "decision": decision,
        "reviewer_id": reviewer_id,
        "reviewed_at": reviewed_at,
        "candidate_current_state_sha256": current_state_sha256,
        "validation_compiler_implementation_sha256": compiler_sha256,
        "modeled_evaluation_sha256": modeled_evaluation_sha256,
        "artifact_sha256": artifact_sha256,
        "evidence_ref": _occupancy_live_evidence_ref(
            candidate_id,
            provenance_sha256,
            candidate_current_state_sha256=current_state_sha256,
            validation_compiler_implementation_sha256=compiler_sha256,
            segment_id=segment_id,
            viewport_id=viewport_id,
            modeled_evaluation_sha256=modeled_evaluation_sha256,
            decision=decision,
            reviewer_id=reviewer_id,
            reviewed_at=reviewed_at,
            artifact_sha256=artifact_sha256,
        ),
    }
    return {
        "schema_version": SCHEMA_VERSION,
        "capture": capture,
        "occupancy_review": {
            **copy.deepcopy(evaluation),
            "status": f"live_{decision}",
            "rationale": rationale,
            "modeled_evidence_ref": _occupancy_modeled_evidence_ref(
                candidate_id,
                segment_id,
                viewport_id,
            ),
            "live_review": live_review,
        },
    }


def _load_acceptance_cli_input(path: Path) -> Any:
    try:
        return json.loads(path.read_bytes())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise QualityError(f"acceptance input is not valid JSON: {error}") from error


def acceptance_main() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        prog="gigawatt-acceptance",
        description=(
            "Materialize canonical acceptance evidence from explicit reviewed inputs."
        ),
    )
    parser.add_argument(
        "--repository-root",
        type=Path,
        default=ROOT,
        help=argparse.SUPPRESS,
    )
    commands = parser.add_subparsers(dest="command", required=True)
    report = commands.add_parser("report")
    report.add_argument("--input", type=Path, required=True)
    occupancy = commands.add_parser("occupancy")
    occupancy.add_argument("--input", type=Path, required=True)
    occupancy.add_argument("--capture", type=Path, required=True)
    arguments = parser.parse_args()
    try:
        value = _load_acceptance_cli_input(arguments.input)
        if arguments.command == "report":
            result = materialize_acceptance_report(
                value,
                repository_root=arguments.repository_root,
            )
        else:
            try:
                capture_bytes = arguments.capture.read_bytes()
            except OSError as error:
                raise QualityError(
                    f"occupancy capture is unavailable: {error}"
                ) from error
            result = materialize_occupancy_evidence(
                value,
                capture_bytes,
                repository_root=arguments.repository_root,
            )
    except QualityError as error:
        parser.error(str(error))
    print(scene_pipeline.canonical_payload(result))


def main() -> None:
    quality_json, graph_json, digest = build_artifacts()
    QUALITY_PATH.write_text(quality_json)
    GRAPH_PATH.write_text(graph_json)
    print(
        f"built {QUALITY_PATH.relative_to(ROOT)} and "
        f"{GRAPH_PATH.relative_to(ROOT)} · "
        f"{course_runtime.EXPECTED_SEGMENTS} segments × {len(VIEWPORTS)} viewports "
        f"· digest {digest}"
    )


if __name__ == "__main__":
    main()
