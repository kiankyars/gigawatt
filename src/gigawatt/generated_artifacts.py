"""Pure regeneration and exact parity checks for deterministic course artifacts."""

from __future__ import annotations

import runpy
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

from . import course_runtime as course_runtime_pipeline
from . import layout as layout_pipeline
from . import mock as mock_pipeline
from . import scene as scene_pipeline
from . import sheet as sheet_pipeline
from . import shots as shots_pipeline

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
S10_GENERATOR = DIAGRAM / "generate_s10_two_rack_heat_paths.py"
PHASE1_GENERATOR = DIAGRAM / "generate_phase1_generation.py"
PHASE2_GENERATOR = DIAGRAM / "generate_phase2_transmission.py"
PHASE3_GENERATOR = DIAGRAM / "generate_phase3_campus.py"
PHASE4_GENERATOR = DIAGRAM / "generate_phase4_building.py"
PHASE5_GENERATOR = DIAGRAM / "generate_phase5_compute.py"
PHASE6_GENERATOR = DIAGRAM / "generate_phase6_heat.py"
COURSE_V2_GENERATOR = DIAGRAM / "generate_course_v2.py"

ACCEPTANCE_BASE_GENERATED_ARTIFACT_COMMANDS = {
    "diagram/symbols.svg": "uv run gigawatt-symbols",
    "diagram/master.svg": "uv run gigawatt-layout",
    "diagram/camera_system_orientation.svg": "uv run gigawatt-layout",
    "diagram/camera_watt_heat_handoff.svg": "uv run gigawatt-layout",
    "diagram/map_watt_heat_handoff.svg": "uv run gigawatt-layout",
    "diagram/mock_wide.svg": "uv run gigawatt-mock",
    "diagram/mock_zoom.svg": "uv run gigawatt-mock",
    "diagram/s10_two_rack_heat_paths.html": (
        "uv run python diagram/generate_s10_two_rack_heat_paths.py"
    ),
}
GENERATED_ARTIFACT_COMMANDS = {
    **ACCEPTANCE_BASE_GENERATED_ARTIFACT_COMMANDS,
    "diagram/phase1_generation.html": (
        "uv run python diagram/generate_phase1_generation.py"
    ),
    "diagram/phase2_transmission.html": (
        "uv run python diagram/generate_phase2_transmission.py"
    ),
    "diagram/phase3_campus.html": "uv run python diagram/generate_phase3_campus.py",
    "diagram/phase4_building.html": (
        "uv run python diagram/generate_phase4_building.py"
    ),
    "diagram/phase5_compute.html": "uv run python diagram/generate_phase5_compute.py",
    "diagram/phase6_heat.html": "uv run python diagram/generate_phase6_heat.py",
    "diagram/course_v2_runtime.json": "uv run python diagram/generate_course_v2.py",
    "diagram/course_v2.html": "uv run python diagram/generate_course_v2.py",
    "course/INSTRUCTOR_PACKET_V2.md": "uv run python diagram/generate_course_v2.py",
}
ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS = {
    **ACCEPTANCE_BASE_GENERATED_ARTIFACT_COMMANDS,
    "diagram/hybrid.html": "uv run gigawatt-scene",
    "diagram/planned_shots.json": "uv run gigawatt-shots",
    "diagram/planned_shots.html": "uv run gigawatt-shots",
    "diagram/course_runtime.json": "uv run gigawatt-course",
    "diagram/course.html": "uv run gigawatt-course",
    "course/INSTRUCTOR_PACKET.md": "uv run gigawatt-course",
}
CANDIDATE_COURSE_ARTIFACT_IDS = (
    "course/INSTRUCTOR_PACKET.md",
    "diagram/course.html",
    "diagram/course_runtime.json",
)


class GeneratedArtifactError(ValueError):
    """Raised when deterministic artifact construction or parity fails."""


def _layout_artifacts(
    master: Mapping[str, Any],
    layout: Mapping[str, Any],
    evidence: Mapping[str, Any],
    cameras: Mapping[str, Any],
) -> dict[str, str]:
    frame = layout["frame"]
    hud_scene, scene = layout_pipeline.compose(master, layout, evidence)
    artifacts = {
        "diagram/master.svg": layout_pipeline._svg(
            hud_scene,
            frame["w"],
            frame["h"],
            "master",
        )
    }
    for camera in cameras["cameras"]:
        if camera["mode"] not in {"2d", "overlay"}:
            continue
        artifacts[f"diagram/camera_{camera['id']}.svg"] = layout_pipeline.build_camera(
            scene,
            camera,
            frame,
            master["meta"]["journey_bar"],
            master,
        )
        if map_asset := camera.get("map_asset"):
            artifacts[f"diagram/{map_asset}"] = layout_pipeline._svg(
                layout_pipeline.filtered_camera_scene(scene, camera, master),
                frame["w"],
                frame["h"],
                f"map-{camera['id']}",
            )
    return artifacts


def _s10_artifact() -> str:
    namespace = runpy.run_path(str(S10_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("S10 generator does not expose build()")
    rendered, _digest, _transformation_count = build()
    if not isinstance(rendered, str):
        raise GeneratedArtifactError("S10 generator build() did not return text")
    return rendered


def _phase1_artifact() -> str:
    namespace = runpy.run_path(str(PHASE1_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("Phase 1 generator does not expose build()")
    rendered, _digest, _state_count = build()
    if not isinstance(rendered, str):
        raise GeneratedArtifactError("Phase 1 generator build() did not return text")
    return rendered


def _phase2_artifact() -> str:
    namespace = runpy.run_path(str(PHASE2_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("Phase 2 generator does not expose build()")
    rendered, _digest, _state_count = build()
    if not isinstance(rendered, str):
        raise GeneratedArtifactError("Phase 2 generator build() did not return text")
    return rendered


def _phase3_artifact() -> str:
    namespace = runpy.run_path(str(PHASE3_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("Phase 3 generator does not expose build()")
    rendered, _digest, _state_count = build()
    if not isinstance(rendered, str):
        raise GeneratedArtifactError("Phase 3 generator build() did not return text")
    return rendered


def _phase4_artifact() -> str:
    namespace = runpy.run_path(str(PHASE4_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("Phase 4 generator does not expose build()")
    rendered, _digest, _state_count = build()
    if not isinstance(rendered, str):
        raise GeneratedArtifactError("Phase 4 generator build() did not return text")
    return rendered


def _phase5_artifact() -> str:
    namespace = runpy.run_path(str(PHASE5_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("Phase 5 generator does not expose build()")
    rendered, _digest, _state_count = build()
    if not isinstance(rendered, str):
        raise GeneratedArtifactError("Phase 5 generator build() did not return text")
    return rendered


def _phase6_artifact() -> str:
    namespace = runpy.run_path(str(PHASE6_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("Phase 6 generator does not expose build()")
    rendered, _digest, _state_count = build()
    if not isinstance(rendered, str):
        raise GeneratedArtifactError("Phase 6 generator build() did not return text")
    return rendered


def _course_v2_artifacts() -> dict[str, str]:
    namespace = runpy.run_path(str(COURSE_V2_GENERATOR))
    build = namespace.get("build")
    if not callable(build):
        raise GeneratedArtifactError("Course v2 generator does not expose build()")
    runtime, player, packet, _digest, _phase_count = build()
    artifacts = {
        "diagram/course_v2_runtime.json": runtime,
        "diagram/course_v2.html": player,
        "course/INSTRUCTOR_PACKET_V2.md": packet,
    }
    if not all(isinstance(rendered, str) for rendered in artifacts.values()):
        raise GeneratedArtifactError("Course v2 generator build() did not return text")
    return artifacts


def _build_acceptance_base_artifacts(
    master: Mapping[str, Any],
    layout: Mapping[str, Any],
    evidence: Mapping[str, Any],
    cameras: Mapping[str, Any],
) -> dict[str, str]:
    """Build the generated artifacts inherited by the frozen v1 acceptance set."""
    artifacts = {
        "diagram/symbols.svg": sheet_pipeline.build_sheet(),
        **_layout_artifacts(master, layout, evidence, cameras),
        "diagram/mock_wide.svg": mock_pipeline.build_wide(),
        "diagram/mock_zoom.svg": mock_pipeline.build_zoom(),
        "diagram/s10_two_rack_heat_paths.html": _s10_artifact(),
    }
    expected_paths = set(ACCEPTANCE_BASE_GENERATED_ARTIFACT_COMMANDS)
    if set(artifacts) != expected_paths:
        raise GeneratedArtifactError(
            "acceptance base artifact inventory drift: "
            f"missing={sorted(expected_paths - set(artifacts))} "
            f"extra={sorted(set(artifacts) - expected_paths)}"
        )
    return artifacts


def build_expected_artifacts(
    master: Mapping[str, Any],
    layout: Mapping[str, Any],
    evidence: Mapping[str, Any],
    cameras: Mapping[str, Any],
) -> dict[str, str]:
    """Build every deterministic artifact not owned by the other registries."""
    artifacts = {
        **_build_acceptance_base_artifacts(master, layout, evidence, cameras),
        "diagram/phase1_generation.html": _phase1_artifact(),
        "diagram/phase2_transmission.html": _phase2_artifact(),
        "diagram/phase3_campus.html": _phase3_artifact(),
        "diagram/phase4_building.html": _phase4_artifact(),
        "diagram/phase5_compute.html": _phase5_artifact(),
        "diagram/phase6_heat.html": _phase6_artifact(),
        **_course_v2_artifacts(),
    }
    expected_paths = set(GENERATED_ARTIFACT_COMMANDS)
    if set(artifacts) != expected_paths:
        raise GeneratedArtifactError(
            "generated artifact inventory drift: "
            f"missing={sorted(expected_paths - set(artifacts))} "
            f"extra={sorted(set(artifacts) - expected_paths)}"
        )
    return artifacts


def build_candidate_course_artifacts(
    runtime_registry: Mapping[str, Any],
) -> dict[str, str]:
    """Pure-build the three runtime artifacts for one modeled candidate."""

    course, cameras, master, layout, scene, ledgers, _visuals = (
        course_runtime_pipeline.load_inputs()
    )
    registry_json, player, instructor_packet = (
        course_runtime_pipeline.build_registry_artifacts(
            dict(runtime_registry),
            course,
            cameras,
            master,
            layout,
            scene,
            ledgers,
        )
    )
    artifacts = {
        "course/INSTRUCTOR_PACKET.md": instructor_packet,
        "diagram/course.html": player,
        "diagram/course_runtime.json": registry_json,
    }
    if tuple(sorted(artifacts)) != CANDIDATE_COURSE_ARTIFACT_IDS:
        raise GeneratedArtifactError("candidate course artifact inventory drift")
    return artifacts


def build_acceptance_materialized_artifacts() -> dict[str, str]:
    """Pure-build every non-self-referential artifact bound into acceptance."""
    course, cameras, master, layout, _scene, ledgers, _visuals = (
        course_runtime_pipeline.load_inputs()
    )
    evidence = ledgers[course["meta"]["master_evidence_ledger"]]
    shot_registry, shot_review, _shot_digest = shots_pipeline.build_artifacts()
    course_registry, course_player, instructor_packet, _course_digest = (
        course_runtime_pipeline.build_artifacts()
    )
    hybrid, _scene_digest = scene_pipeline.generate()
    artifacts = {
        **_build_acceptance_base_artifacts(master, layout, evidence, cameras),
        "diagram/hybrid.html": hybrid,
        "diagram/planned_shots.json": shot_registry,
        "diagram/planned_shots.html": shot_review,
        "diagram/course_runtime.json": course_registry,
        "diagram/course.html": course_player,
        "course/INSTRUCTOR_PACKET.md": instructor_packet,
    }
    expected_paths = set(ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS)
    if set(artifacts) != expected_paths:
        raise GeneratedArtifactError(
            "acceptance artifact inventory drift: "
            f"missing={sorted(expected_paths - set(artifacts))} "
            f"extra={sorted(set(artifacts) - expected_paths)}"
        )
    return artifacts


def assert_acceptance_current(
    artifacts: Mapping[str, str],
    *,
    read_bytes: Callable[[Path], bytes] | None = None,
) -> None:
    """Require literal retained-byte parity for the 14 materialized outputs."""
    reader = read_bytes or (lambda path: path.read_bytes())
    expected_paths = set(ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS)
    if set(artifacts) != expected_paths:
        raise GeneratedArtifactError("acceptance artifact parity input is incomplete")
    for relative_path, expected in artifacts.items():
        path = ROOT / relative_path
        try:
            actual = reader(path)
        except OSError as error:
            raise GeneratedArtifactError(
                f"{relative_path} is unavailable: {error}"
            ) from error
        if actual != expected.encode():
            command = ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS[relative_path]
            raise GeneratedArtifactError(f"{relative_path} is stale; run {command}")


def assert_current(
    artifacts: Mapping[str, str],
    *,
    read_text: Callable[[Path], str] | None = None,
) -> None:
    """Require exact bytes for every declared generated artifact."""
    reader = read_text or (lambda path: path.read_text())
    if set(artifacts) != set(GENERATED_ARTIFACT_COMMANDS):
        raise GeneratedArtifactError("generated artifact parity input is incomplete")
    for relative_path, expected in artifacts.items():
        path = ROOT / relative_path
        try:
            actual = reader(path)
        except OSError as error:
            raise GeneratedArtifactError(
                f"{relative_path} is unavailable: {error}"
            ) from error
        if actual != expected:
            command = GENERATED_ARTIFACT_COMMANDS[relative_path]
            raise GeneratedArtifactError(f"{relative_path} is stale; run {command}")
