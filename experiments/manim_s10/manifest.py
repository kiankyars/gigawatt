from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parents[2]
PILOT_PATH = REPO_ROOT / "course/pilots/s10_two_rack_heat_paths.yaml"
COURSE_PATH = REPO_ROOT / "course/segments.yaml"
MASTER_PATH = REPO_ROOT / "diagram/master.yaml"
SCENE_PATH = REPO_ROOT / "diagram/scene.yaml"
CAMERAS_PATH = REPO_ROOT / "diagram/cameras.yaml"
SOURCE_PATHS = (COURSE_PATH, PILOT_PATH, MASTER_PATH, SCENE_PATH, CAMERAS_PATH)

TOP_LEVEL_FIELDS = {
    "schema_version",
    "segment_id",
    "camera_anchor",
    "purpose",
    "transformations",
}
TRANSFORMATION_FIELDS = {
    "id",
    "title",
    "instruction",
    "focus_nodes",
    "focus_edges",
    "pulse_edges",
}


@dataclass(frozen=True)
class Transformation:
    id: str
    title: str
    instruction: str
    focus_nodes: tuple[str, ...]
    focus_edges: tuple[str, ...]
    pulse_edges: tuple[str, ...]


@dataclass(frozen=True)
class Pilot:
    schema_version: int
    segment_id: str
    camera_anchor: str
    purpose: str
    source_digest: str
    transformations: tuple[Transformation, ...]
    node_labels: dict[str, str]
    scene_nodes: dict[str, dict[str, Any]]
    scene_edges: dict[str, dict[str, Any]]

    def transformation(self, transformation_id: str) -> Transformation:
        for item in self.transformations:
            if item.id == transformation_id:
                return item
        available = ", ".join(item.id for item in self.transformations)
        raise ValueError(
            f"unknown transformation {transformation_id!r}; choose one of: {available}"
        )


def _load_mapping(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text())
    if not isinstance(value, dict):
        raise TypeError(f"{path.relative_to(REPO_ROOT)} must contain a mapping")
    return value


def source_digest() -> str:
    digest = hashlib.sha256()
    for path in SOURCE_PATHS:
        digest.update(path.relative_to(REPO_ROOT).as_posix().encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _require_exact_fields(
    value: dict[str, Any], expected: set[str], location: str
) -> None:
    actual = set(value)
    if actual != expected:
        missing = sorted(expected - actual)
        extra = sorted(actual - expected)
        raise ValueError(f"{location} field mismatch; missing={missing}, extra={extra}")


def _require_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{location} must be a non-empty string")
    return value


def _require_id_list(value: Any, location: str) -> tuple[str, ...]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise ValueError(f"{location} must be a list of non-empty ID strings")
    if len(value) != len(set(value)):
        raise ValueError(f"{location} must not contain duplicate IDs")
    return tuple(value)


def _canonical_segment(course: dict[str, Any], segment_id: str) -> dict[str, Any]:
    matches = [
        segment
        for act in course.get("acts", [])
        for segment in act.get("segments", [])
        if segment.get("id") == segment_id
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected one canonical segment {segment_id!r}, found {len(matches)}"
        )
    return matches[0]


def load_pilot() -> Pilot:
    pilot_data = _load_mapping(PILOT_PATH)
    course = _load_mapping(COURSE_PATH)
    master = _load_mapping(MASTER_PATH)
    scene = _load_mapping(SCENE_PATH)
    cameras = _load_mapping(CAMERAS_PATH)

    _require_exact_fields(pilot_data, TOP_LEVEL_FIELDS, "pilot")
    if pilot_data["schema_version"] != 1:
        raise ValueError("pilot.schema_version must equal 1")

    segment_id = _require_string(pilot_data["segment_id"], "pilot.segment_id")
    segment = _canonical_segment(course, segment_id)
    camera_anchor = _require_string(pilot_data["camera_anchor"], "pilot.camera_anchor")
    if camera_anchor != segment["camera"]["anchor"]:
        raise ValueError("pilot.camera_anchor does not match the canonical segment")
    camera_matches = [
        camera
        for camera in cameras.get("cameras", [])
        if camera.get("id") == camera_anchor
    ]
    if len(camera_matches) != 1 or camera_matches[0].get("mode") != "3d":
        raise ValueError("pilot.camera_anchor must resolve to one 3D camera")

    master_nodes = {node["id"]: node for node in master.get("nodes", [])}
    master_edges = {edge["id"]: edge for edge in master.get("edges", [])}
    scene_nodes = scene.get("nodes")
    scene_edges = scene.get("edges")
    if not isinstance(scene_nodes, dict) or not isinstance(scene_edges, dict):
        raise TypeError("diagram/scene.yaml must provide node and edge mappings")

    canonical_node_ids = tuple(segment["node_ids"])
    canonical_edge_ids = tuple(segment["edge_ids"])
    canonical_nodes = set(canonical_node_ids)
    canonical_edges = set(canonical_edge_ids)
    transformations_data = pilot_data["transformations"]
    if not isinstance(transformations_data, list) or not transformations_data:
        raise ValueError("pilot.transformations must be a non-empty list")

    transformations: list[Transformation] = []
    seen_ids: set[str] = set()
    covered_nodes: set[str] = set()
    covered_edges: set[str] = set()
    for index, item in enumerate(transformations_data):
        location = f"pilot.transformations[{index}]"
        if not isinstance(item, dict):
            raise TypeError(f"{location} must be a mapping")
        _require_exact_fields(item, TRANSFORMATION_FIELDS, location)

        transformation_id = _require_string(item["id"], f"{location}.id")
        if transformation_id in seen_ids:
            raise ValueError(f"duplicate transformation ID {transformation_id!r}")
        seen_ids.add(transformation_id)

        focus_nodes = _require_id_list(item["focus_nodes"], f"{location}.focus_nodes")
        focus_edges = _require_id_list(item["focus_edges"], f"{location}.focus_edges")
        pulse_edges = _require_id_list(item["pulse_edges"], f"{location}.pulse_edges")

        unknown_nodes = set(focus_nodes) - (set(master_nodes) & set(scene_nodes))
        unknown_edges = (set(focus_edges) | set(pulse_edges)) - (
            set(master_edges) & set(scene_edges)
        )
        if unknown_nodes:
            raise ValueError(
                f"{location} references unknown node IDs: {sorted(unknown_nodes)}"
            )
        if unknown_edges:
            raise ValueError(
                f"{location} references unknown edge IDs: {sorted(unknown_edges)}"
            )
        if set(focus_nodes) - canonical_nodes:
            raise ValueError(f"{location}.focus_nodes exceeds the canonical s10 scope")
        if set(focus_edges) - canonical_edges:
            raise ValueError(f"{location}.focus_edges exceeds the canonical s10 scope")
        if set(pulse_edges) - set(focus_edges):
            raise ValueError(f"{location}.pulse_edges must be a subset of focus_edges")
        if not focus_nodes and not focus_edges:
            raise ValueError(f"{location} must not be empty")
        hidden_nodes = {
            node_id
            for node_id in focus_nodes
            if master_nodes[node_id].get("base_visible", True) is False
        }
        hidden_edges = {
            edge_id
            for edge_id in focus_edges
            if master_edges[edge_id].get("base_visible", True) is False
        }
        if hidden_nodes or hidden_edges:
            raise ValueError(
                f"{location} references hidden items without a reveal contract"
            )
        focused_node_set = set(focus_nodes)
        missing_endpoints = {
            endpoint
            for edge_id in focus_edges
            for endpoint in (master_edges[edge_id]["from"], master_edges[edge_id]["to"])
            if endpoint not in focused_node_set
        }
        if missing_endpoints:
            raise ValueError(
                f"{location}.focus_edges has endpoints outside focus_nodes: "
                f"{sorted(missing_endpoints)}"
            )

        covered_nodes.update(focus_nodes)
        covered_edges.update(focus_edges)
        transformations.append(
            Transformation(
                id=transformation_id,
                title=_require_string(item["title"], f"{location}.title"),
                instruction=_require_string(
                    item["instruction"], f"{location}.instruction"
                ),
                focus_nodes=focus_nodes,
                focus_edges=focus_edges,
                pulse_edges=pulse_edges,
            )
        )

    if covered_nodes != canonical_nodes:
        raise ValueError(
            "pilot transformations must collectively cover the canonical s10 nodes"
        )
    if covered_edges != canonical_edges:
        raise ValueError(
            "pilot transformations must collectively cover the canonical s10 edges"
        )

    return Pilot(
        schema_version=pilot_data["schema_version"],
        segment_id=segment_id,
        camera_anchor=camera_anchor,
        purpose=_require_string(pilot_data["purpose"], "pilot.purpose"),
        source_digest=source_digest(),
        transformations=tuple(transformations),
        node_labels={
            node_id: master_nodes[node_id]["label"] for node_id in canonical_node_ids
        },
        scene_nodes={node_id: scene_nodes[node_id] for node_id in canonical_node_ids},
        scene_edges={edge_id: scene_edges[edge_id] for edge_id in canonical_edge_ids},
    )


if __name__ == "__main__":
    loaded = load_pilot()
    print(
        f"validated {loaded.segment_id}: {len(loaded.transformations)} transformations"
    )
    print(f"source_digest={loaded.source_digest}")
    for transformation in loaded.transformations:
        print(transformation.id)
