"""Build the unified six-phase GIGAWATT v2 course surfaces.

Usage: uv run python diagram/generate_course_v2.py
"""

from __future__ import annotations

from pathlib import Path

from gigawatt import course_v2_runtime, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / course_v2_runtime.COURSE_PATH
RUNTIME = ROOT / course_v2_runtime.RUNTIME_PATH
PLAYER = ROOT / course_v2_runtime.PLAYER_PATH
PACKET = ROOT / course_v2_runtime.PACKET_PATH
GENERATOR_DEPENDENCY_PATHS = (
    ROOT / "pyproject.toml",
    ROOT / "uv.lock",
    Path(__file__).resolve(),
    Path(course_v2_runtime.__file__).resolve(),
    Path(teaching_visuals.__file__).resolve(),
)
SPATIAL_RUNTIME_DEPENDENCY_PATHS = (
    ROOT / course_v2_runtime.CAMERAS_PATH,
    ROOT / "diagram/master.svg",
    ROOT / "diagram/map_watt_heat_handoff.svg",
    ROOT / "diagram/vendor/three/three.module.js",
    ROOT / "diagram/vendor/three/OrbitControls.js",
    ROOT / "diagram/vendor/three/CSS2DRenderer.js",
    ROOT / "diagram/vendor/three/LICENSE",
)


def _phase_paths(spine: dict | None = None) -> tuple[Path, ...]:
    if spine is None:
        spine = teaching_visuals.load_yaml(COURSE)
    phases = spine.get("phases")
    if not isinstance(phases, list) or len(phases) != course_v2_runtime.PHASE_COUNT:
        raise course_v2_runtime.CourseV2RuntimeError(
            "course v2.phases must contain exactly six phases"
        )
    paths: list[Path] = []
    for index, phase in enumerate(phases):
        if not isinstance(phase, dict):
            raise course_v2_runtime.CourseV2RuntimeError(
                f"course v2.phases[{index}] must be a mapping"
            )
        manifest = course_v2_runtime._relative_path(
            phase.get("manifest"),
            f"course v2.phases[{index}].manifest",
            prefix="course/pilots/",
            suffix=".yaml",
        )
        artifact = course_v2_runtime._relative_path(
            phase.get("artifact"),
            f"course v2.phases[{index}].artifact",
            prefix="diagram/phase",
            suffix=".html",
        )
        paths.extend((ROOT / manifest, ROOT / artifact))
    return tuple(paths)


def _spatial_paths(spine: dict | None = None) -> tuple[Path, ...]:
    if spine is None:
        spine = teaching_visuals.load_yaml(COURSE)
    spatial = spine.get("spatial")
    if not isinstance(spatial, dict):
        raise course_v2_runtime.CourseV2RuntimeError(
            "course v2.spatial must be a mapping"
        )
    artifact = course_v2_runtime._relative_path(
        spatial.get("artifact"),
        "course v2.spatial.artifact",
        prefix="diagram/",
        suffix=".html",
    )
    return (ROOT / artifact, *SPATIAL_RUNTIME_DEPENDENCY_PATHS)


def _source_digest(spine: dict | None = None) -> str:
    if spine is None:
        spine = teaching_visuals.load_yaml(COURSE)
    return teaching_visuals.source_digest(
        ROOT,
        (
            *GENERATOR_DEPENDENCY_PATHS,
            COURSE,
            *_phase_paths(spine),
            *_spatial_paths(spine),
        ),
    )


def build() -> tuple[str, str, str, str, int]:
    spine = teaching_visuals.load_yaml(COURSE)
    digest = _source_digest(spine)
    registry = course_v2_runtime.load_and_compile(ROOT, source_digest=digest)
    runtime = course_v2_runtime.runtime_json(registry)
    player = course_v2_runtime.render_player(registry)
    packet = course_v2_runtime.render_instructor_packet(registry)
    return runtime, player, packet, digest, len(registry["phases"])


def main() -> None:
    runtime, player, packet, digest, phase_count = build()
    RUNTIME.write_text(runtime)
    PLAYER.write_text(player)
    PACKET.write_text(packet)
    print(
        f"built {RUNTIME.relative_to(ROOT)}, {PLAYER.relative_to(ROOT)}, and "
        f"{PACKET.relative_to(ROOT)} · {phase_count} phases · digest {digest}"
    )


if __name__ == "__main__":
    main()
