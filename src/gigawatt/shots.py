"""Compile the untimed planned-shot registry and manual review surface.

The course manifest owns shot requests and semantic scope. Reusable cameras own
context, the layout owns 2D geometry, and the scene owns 3D placement. This
module derives review geometry without promoting planned shots to existing.

Usage: uv run python -m gigawatt.shots
"""

from __future__ import annotations

import hashlib
import math
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from . import layout as layout_pipeline
from . import scene as scene_pipeline
from . import tokens
from .render import S

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
COURSE_PATH = ROOT / "course" / "segments.yaml"
CAMERAS_PATH = DIAGRAM / "cameras.yaml"
MASTER_PATH = DIAGRAM / "master.yaml"
LAYOUT_PATH = DIAGRAM / "layout.yaml"
SCENE_PATH = DIAGRAM / "scene.yaml"
REGISTRY_PATH = DIAGRAM / "planned_shots.json"
REVIEW_PATH = DIAGRAM / "planned_shots.html"

SCHEMA_VERSION = 1
EXPECTED_PLANNED_SHOTS = 21
ALLOWED_MODES = {"2d", "3d", "overlay"}
FORBIDDEN_REGISTRY_KEYS = {
    "autoplay",
    "beat",
    "beats",
    "cadence",
    "duration",
    "runtime",
    "script",
    "timing",
}


class ShotError(ValueError):
    """Raised when a planned shot drifts from its canonical owners."""


def load_inputs() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
]:
    return (
        scene_pipeline.load_yaml(COURSE_PATH),
        scene_pipeline.load_yaml(CAMERAS_PATH),
        scene_pipeline.load_yaml(MASTER_PATH),
        scene_pipeline.load_yaml(LAYOUT_PATH),
        scene_pipeline.load_yaml(SCENE_PATH),
    )


def _source_digest(master: dict[str, Any]) -> str:
    evidence_path = ROOT / master["meta"]["evidence_file"]
    digest = hashlib.sha256()
    for path in (
        COURSE_PATH,
        CAMERAS_PATH,
        MASTER_PATH,
        LAYOUT_PATH,
        SCENE_PATH,
        evidence_path,
    ):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _script_safe_payload(payload: dict[str, Any]) -> str:
    return scene_pipeline.canonical_payload(payload).replace("</", "<\\/")


def _unique_strings(value: Any, location: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise ShotError(f"{location}: expected a list of non-empty IDs")
    if len(value) != len(set(value)):
        raise ShotError(f"{location}: IDs must be unique")
    return value


def _exact_geometry_coverage(
    master: dict[str, Any], layout: dict[str, Any], scene: dict[str, Any]
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    node_records = {node["id"]: node for node in master.get("nodes") or []}
    edge_records = {edge["id"]: edge for edge in master.get("edges") or []}
    if len(node_records) != len(master.get("nodes") or []):
        raise ShotError("master node IDs must be unique")
    if len(edge_records) != len(master.get("edges") or []):
        raise ShotError("master edge IDs must be unique")

    node_ids = set(node_records)
    edge_ids = set(edge_records)
    layout_nodes = set((layout.get("nodes") or {}).keys())
    layout_edges = set((layout.get("edges") or {}).keys())
    scene_nodes = set((scene.get("nodes") or {}).keys())
    scene_edges = set((scene.get("edges") or {}).keys())
    if node_ids != layout_nodes or node_ids != scene_nodes:
        raise ShotError(
            "node geometry must cover the semantic master exactly: "
            f"layout_missing={sorted(node_ids - layout_nodes)} "
            f"layout_extra={sorted(layout_nodes - node_ids)} "
            f"scene_missing={sorted(node_ids - scene_nodes)} "
            f"scene_extra={sorted(scene_nodes - node_ids)}"
        )
    if edge_ids != layout_edges or edge_ids != scene_edges:
        raise ShotError(
            "edge geometry must cover the semantic master exactly: "
            f"layout_missing={sorted(edge_ids - layout_edges)} "
            f"layout_extra={sorted(layout_edges - edge_ids)} "
            f"scene_missing={sorted(edge_ids - scene_edges)} "
            f"scene_extra={sorted(scene_edges - edge_ids)}"
        )
    return node_records, edge_records


def _layout_node_points(
    node_id: str, layout: dict[str, Any]
) -> list[tuple[float, float]]:
    spec = layout["nodes"][node_id]
    kind = spec.get("kind")
    if kind == "corridor":
        (_, span_y0), (_, span_y1) = spec["span"]
        ground = spec.get("ground", layout["frame"]["ground"])
        points = [tuple(spec["span"][0]), tuple(spec["span"][1])]
        points.extend((float(x), float(spec["top"])) for x in spec["towers"])
        points.extend((float(x), float(ground)) for x in spec["towers"])
        points.extend(
            [
                (float(spec["span"][0][0]), float(span_y0)),
                (float(spec["span"][1][0]), float(span_y1)),
            ]
        )
        return points
    if kind == "line_node":
        return [tuple(point) for point in spec["pts"]]
    if kind == "dual_pipe":
        return [
            *(tuple(point) for point in spec["supply_pts"]),
            *(tuple(point) for point in spec["return_pts"]),
        ]

    x, y = spec["at"]
    scale = float(spec.get("s", 1.0))
    if kind == "stack":
        height = len(spec["symbols"]) * S + max(0, len(spec["symbols"]) - 1) * float(
            spec.get("gap", 14)
        )
        width = S
    else:
        width = height = S * scale
    return [
        (float(x), float(y)),
        (float(x + width), float(y)),
        (float(x), float(y + height)),
        (float(x + width), float(y + height)),
    ]


def _layout_edge_points(
    edge_id: str,
    layout: dict[str, Any],
    edge_records: dict[str, dict[str, Any]],
    geoms: dict[str, layout_pipeline.Geom],
) -> list[tuple[float, float]]:
    spec = layout["edges"][edge_id]
    record = edge_records[edge_id]
    source, target = record["from"], record["to"]
    from_port, to_port = spec["ports"]
    start = (
        tuple(spec["from_at"])
        if spec.get("from_at") is not None
        else geoms[source].ports[from_port]
    )
    end = (
        tuple(spec["to_at"])
        if spec.get("to_at") is not None
        else geoms[target].ports[to_port]
    )
    return [start, *(tuple(point) for point in spec.get("via") or []), end]


def _fit_2d_view(
    points: Iterable[tuple[float, float]], frame: dict[str, Any]
) -> list[float]:
    point_list = list(points)
    if not point_list:
        raise ShotError("cannot frame a 2D shot without geometry")
    xs = [point[0] for point in point_list]
    ys = [point[1] for point in point_list]
    raw_width = max(xs) - min(xs)
    raw_height = max(ys) - min(ys)
    padding = max(72.0, max(raw_width, raw_height) * 0.12)
    width = max(360.0, raw_width + 2 * padding)
    height = max(202.5, raw_height + 2 * padding)
    aspect = float(frame["w"]) / float(frame["h"])
    if width / height < aspect:
        width = height * aspect
    else:
        height = width / aspect

    frame_width = float(frame["w"])
    frame_height = float(frame["h"])
    if width > frame_width:
        width = frame_width
        height = width / aspect
    if height > frame_height:
        height = frame_height
        width = height * aspect

    center_x = (min(xs) + max(xs)) / 2
    center_y = (min(ys) + max(ys)) / 2
    x = min(max(0.0, center_x - width / 2), frame_width - width)
    y = min(max(0.0, center_y - height / 2), frame_height - height)
    return [round(value, 3) for value in (x, y, width, height)]


def _scene_node_points(
    node_id: str, scene: dict[str, Any]
) -> list[tuple[float, float, float]]:
    spec = scene["nodes"][node_id]
    origin = [float(value) for value in spec["at"]]
    points: list[tuple[float, float, float]] = [tuple(origin), tuple(spec["label_at"])]
    for primitive in spec["primitives"]:
        center = [origin[index] + float(primitive["at"][index]) for index in range(3)]
        if primitive["shape"] == "box":
            half = [float(value) / 2 for value in primitive["size"]]
        else:
            radius = float(primitive["radius"])
            half = [radius, float(primitive["height"]) / 2, radius]
        for signs in (
            (-1, -1, -1),
            (-1, -1, 1),
            (-1, 1, -1),
            (-1, 1, 1),
            (1, -1, -1),
            (1, -1, 1),
            (1, 1, -1),
            (1, 1, 1),
        ):
            points.append(
                tuple(center[index] + signs[index] * half[index] for index in range(3))
            )
    return points


def _derive_3d_frame(
    node_ids: list[str],
    edge_ids: list[str],
    anchor: dict[str, Any],
    scene: dict[str, Any],
) -> dict[str, Any]:
    points: list[tuple[float, float, float]] = []
    for node_id in node_ids:
        points.extend(_scene_node_points(node_id, scene))
    for edge_id in edge_ids:
        points.extend(tuple(point) for point in scene["edges"][edge_id]["points"])
    if not points:
        raise ShotError("cannot frame a 3D shot without geometry")

    axes = list(zip(*points))
    minimum = [min(axis) for axis in axes]
    maximum = [max(axis) for axis in axes]
    target = [(minimum[index] + maximum[index]) / 2 for index in range(3)]
    radius = max(math.dist(target, point) for point in points)
    anchor_position = [float(value) for value in anchor["position"]]
    anchor_target = [float(value) for value in anchor["target"]]
    direction = [anchor_position[index] - anchor_target[index] for index in range(3)]
    anchor_distance = math.sqrt(sum(value * value for value in direction))
    if not math.isfinite(anchor_distance) or anchor_distance <= 0:
        raise ShotError(f"camera {anchor['id']}: invalid 3D direction")
    direction = [value / anchor_distance for value in direction]
    distance = max(
        180.0,
        anchor_distance * 0.55,
        radius / math.sin(math.radians(20.0)) * 1.22,
    )
    position = [target[index] + direction[index] * distance for index in range(3)]
    values = [*target, *position]
    if any(not math.isfinite(value) for value in values):
        raise ShotError(f"camera {anchor['id']}: derived non-finite 3D frame")
    return {
        "kind": "3d",
        "position": [round(value, 3) for value in position],
        "target": [round(value, 3) for value in target],
        "up": [0, 1, 0],
        "anchor_position": anchor_position,
        "anchor_target": anchor_target,
    }


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def compile_registry(
    course: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Compile every planned course request into conservative review geometry."""
    node_records, edge_records = _exact_geometry_coverage(master, layout, scene)
    copy_records = master.get("copy") or {}
    hidden_nodes = {
        node_id
        for node_id, record in node_records.items()
        if record.get("base_visible", True) is False
    }
    hidden_edges = {
        edge_id
        for edge_id, record in edge_records.items()
        if record.get("base_visible", True) is False
    }
    hidden_copy = {
        copy_id
        for copy_id, record in copy_records.items()
        if record.get("base_visible", True) is False
    }

    camera_list = cameras.get("cameras") or []
    camera_ids = [camera.get("id") for camera in camera_list]
    if not camera_ids or len(camera_ids) != len(set(camera_ids)):
        raise ShotError("reusable camera IDs must be present and unique")
    camera_map = {camera["id"]: camera for camera in camera_list}

    segments = [
        segment
        for act in course.get("acts") or []
        for segment in act.get("segments") or []
    ]
    planned = [
        segment
        for segment in segments
        if segment.get("camera", {}).get("status") == "planned"
    ]
    if len(planned) != EXPECTED_PLANNED_SHOTS:
        raise ShotError(
            f"expected {EXPECTED_PLANNED_SHOTS} planned course requests, found {len(planned)}"
        )
    shot_ids = [segment["camera"]["shot"] for segment in planned]
    if len(shot_ids) != len(set(shot_ids)):
        raise ShotError("planned shot IDs must be unique")
    collisions = sorted(set(shot_ids) & set(camera_map))
    if collisions:
        raise ShotError(f"planned shot IDs collide with reusable cameras: {collisions}")

    geoms = layout_pipeline.build_geoms(layout, master, layout["frame"]["ground"])
    compiled: list[dict[str, Any]] = []
    for sequence, segment in enumerate(planned, start=1):
        request = segment["camera"]
        segment_id = segment["id"]
        mode = request.get("mode")
        if mode not in ALLOWED_MODES:
            raise ShotError(f"segment {segment_id}: unsupported shot mode {mode!r}")
        anchor_id = request.get("anchor")
        if anchor_id not in camera_map:
            raise ShotError(
                f"segment {segment_id}: unknown camera anchor {anchor_id!r}"
            )
        anchor = camera_map[anchor_id]
        anchor_mode = anchor.get("mode")
        render_mode = "3d" if anchor_mode == "3d" else "2d"
        if mode == "3d" and render_mode != "3d":
            raise ShotError(f"segment {segment_id}: 3D request requires a 3D anchor")
        if mode == "2d" and render_mode != "2d":
            raise ShotError(
                f"segment {segment_id}: 2D request requires a 2D/map anchor"
            )
        if render_mode == "3d":
            for field in ("position", "target"):
                value = anchor.get(field)
                if not (
                    isinstance(value, list)
                    and len(value) == 3
                    and all(
                        isinstance(item, (int, float))
                        and not isinstance(item, bool)
                        and math.isfinite(float(item))
                        for item in value
                    )
                ):
                    raise ShotError(f"camera {anchor_id}.{field}: invalid 3D geometry")
        else:
            anchor_view = anchor.get("viewBox") or anchor.get("map_view")
            if not (
                isinstance(anchor_view, list)
                and len(anchor_view) == 4
                and all(isinstance(item, (int, float)) for item in anchor_view)
            ):
                raise ShotError(f"camera {anchor_id}: invalid 2D geometry")

        node_ids = _unique_strings(
            segment.get("node_ids"), f"segment {segment_id}.node_ids"
        )
        edge_ids = _unique_strings(
            segment.get("edge_ids"), f"segment {segment_id}.edge_ids"
        )
        unknown_nodes = sorted(set(node_ids) - set(node_records))
        unknown_edges = sorted(set(edge_ids) - set(edge_records))
        missing_endpoints = sorted(
            {
                endpoint
                for edge_id in set(edge_ids) & set(edge_records)
                for endpoint in (
                    edge_records[edge_id]["from"],
                    edge_records[edge_id]["to"],
                )
            }
            - set(node_ids)
        )
        if unknown_nodes or unknown_edges or missing_endpoints:
            raise ShotError(
                f"segment {segment_id}: invalid semantic focus "
                f"nodes={unknown_nodes} edges={unknown_edges} "
                f"unfocused_endpoints={missing_endpoints}"
            )

        reveal_ids = set(
            _unique_strings(
                request.get("reveal_ids"), f"segment {segment_id}.reveal_ids"
            )
        )
        reveal_copy_ids = set(
            _unique_strings(
                request.get("reveal_copy_ids"),
                f"segment {segment_id}.reveal_copy_ids",
            )
        )
        expected_reveals = (set(node_ids) & hidden_nodes) | (
            set(edge_ids) & hidden_edges
        )
        hidden_selected_records = [
            *(node_records[node_id] for node_id in set(node_ids) & hidden_nodes),
            *(edge_records[edge_id] for edge_id in set(edge_ids) & hidden_edges),
        ]
        expected_copy_reveals = {
            copy_id
            for record in hidden_selected_records
            for copy_id in record.get("reveal_copy_ids") or []
        }
        if reveal_ids != expected_reveals:
            raise ShotError(
                f"segment {segment_id}: reveal_ids must exactly match hidden focus "
                f"{sorted(expected_reveals)}"
            )
        if reveal_copy_ids != expected_copy_reveals:
            raise ShotError(
                f"segment {segment_id}: reveal_copy_ids must exactly match hidden copy "
                f"{sorted(expected_copy_reveals)}"
            )
        if reveal_copy_ids - hidden_copy:
            raise ShotError(
                f"segment {segment_id}: reveal copy is not base-hidden "
                f"{sorted(reveal_copy_ids - hidden_copy)}"
            )

        if render_mode == "2d":
            points: list[tuple[float, float]] = []
            for node_id in node_ids:
                points.extend(_layout_node_points(node_id, layout))
            for edge_id in edge_ids:
                points.extend(_layout_edge_points(edge_id, layout, edge_records, geoms))
            frame = {
                "kind": "2d",
                "viewBox": _fit_2d_view(points, layout["frame"]),
                "anchor_viewBox": [
                    float(value)
                    for value in (anchor.get("viewBox") or anchor.get("map_view"))
                ],
            }
        else:
            frame = _derive_3d_frame(node_ids, edge_ids, anchor, scene)

        compiled.append(
            {
                "sequence": sequence,
                "id": request["shot"],
                "segment_id": segment_id,
                "title": segment["title"],
                "status": "planned",
                "mode": mode,
                "render_mode": render_mode,
                "camera_anchor": anchor_id,
                "evidence_readiness": segment["evidence"]["readiness"],
                "focus_nodes": node_ids,
                "focus_edges": edge_ids,
                "reveal_ids": list(request["reveal_ids"]),
                "reveal_copy_ids": list(request["reveal_copy_ids"]),
                "frame": frame,
            }
        )

    registry = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "planned_shot_count": len(compiled),
        "shots": compiled,
    }
    forbidden = {
        key.casefold()
        for key in _walk_keys(registry)
        if key.casefold() in FORBIDDEN_REGISTRY_KEYS
    }
    if forbidden:
        raise ShotError(
            f"registry contains timing or scripting fields: {sorted(forbidden)}"
        )
    return registry


REVIEW_HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="gigawatt-source-digest" content="__DIGEST__">
<title>GIGAWATT — planned shot review</title>
<style>
  :root {
    --paper: __PAPER__;
    --ink: __INK__;
    --faint: __FAINT__;
    --muted: __MUTED__;
    --rail: 286px;
    --head: 112px;
    --transport: 74px;
    --rule: 1.5px;
  }
  * { box-sizing: border-box; }
  html, body { width: 100%; height: 100%; }
  body {
    margin: 0;
    overflow: hidden;
    color: var(--ink);
    background: var(--paper);
    font-family: __FONT__;
  }
  button { color: inherit; font: inherit; }
  #shot-rail {
    position: absolute;
    z-index: 12;
    inset: 0 auto 0 0;
    width: var(--rail);
    display: grid;
    grid-template-rows: auto minmax(0, 1fr);
    background: var(--paper);
    border-right: var(--rule) solid var(--ink);
  }
  #rail-heading { padding: 18px 18px 14px; border-bottom: 1px solid var(--faint); }
  #rail-heading p { margin: 0; color: var(--muted); font-size: 9px; letter-spacing: .08em; text-transform: uppercase; }
  #rail-heading h1 { margin: 5px 0 0; font-size: 17px; line-height: 1.15; }
  #shot-list { overflow-y: auto; padding: 8px 0 18px; }
  .shot-button {
    width: 100%;
    padding: 10px 16px 11px;
    display: grid;
    grid-template-columns: 26px minmax(0, 1fr);
    gap: 8px;
    border: 0;
    border-left: 4px solid transparent;
    background: transparent;
    text-align: left;
    cursor: pointer;
  }
  .shot-button:hover { background: color-mix(in srgb, var(--faint) 26%, transparent); }
  .shot-button[aria-current="step"] { border-left-color: var(--ink); background: color-mix(in srgb, var(--faint) 38%, transparent); }
  .shot-number { padding-top: 1px; color: var(--muted); font-size: 9px; font-variant-numeric: tabular-nums; }
  .shot-name { display: block; font-size: 10px; font-weight: 700; line-height: 1.25; }
  .segment-name { display: block; margin-top: 3px; color: var(--muted); font-size: 8px; line-height: 1.2; }
  #masthead {
    position: absolute;
    z-index: 10;
    top: 0;
    right: 0;
    left: var(--rail);
    min-height: var(--head);
    padding: 18px 24px 15px;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 24px;
    background: color-mix(in srgb, var(--paper) 95%, transparent);
    border-bottom: var(--rule) solid var(--ink);
  }
  #eyebrow, #shot-id { margin: 0; color: var(--muted); font-size: 9px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
  #title { margin: 5px 0 0; font-size: 20px; line-height: 1.1; }
  #scope-summary, #scope-ids { margin: 5px 0 0; font-size: 10px; line-height: 1.25; }
  #scope-ids { max-width: 760px; overflow: hidden; color: var(--muted); text-overflow: ellipsis; white-space: nowrap; }
  #posture {
    align-self: start;
    min-width: 190px;
    padding: 9px 11px;
    border: var(--rule) solid var(--ink);
    background: var(--paper);
  }
  #mode { margin: 5px 0 0; font-size: 10px; font-weight: 700; text-transform: uppercase; }
  #reveal-summary { margin: 5px 0 0; color: var(--muted); font-size: 9px; line-height: 1.25; }
  #stage {
    position: absolute;
    inset: var(--head) 0 var(--transport) var(--rail);
    background: var(--paper);
  }
  #three-mount, #map-stage { position: absolute; inset: 0; }
  #three-mount canvas { display: block; width: 100%; height: 100%; }
  #labels { position: absolute; inset: 0; pointer-events: none; }
  #map-stage { padding: 18px 22px; }
  #map-svg { width: 100%; height: 100%; display: block; }
  .node-label {
    max-width: 205px;
    padding: 4px 7px;
    color: var(--ink);
    background: color-mix(in srgb, var(--paper) 91%, transparent);
    border: 1px solid var(--ink);
    font-size: 10px;
    font-weight: 700;
    line-height: 1.15;
    white-space: nowrap;
  }
  .node-label small {
    display: block;
    margin-top: 2px;
    color: var(--muted);
    font-size: 8px;
    font-weight: 500;
    letter-spacing: .035em;
    text-transform: uppercase;
  }
  #transport {
    position: absolute;
    z-index: 11;
    right: 0;
    bottom: 0;
    left: var(--rail);
    min-height: var(--transport);
    padding: 12px 18px;
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto auto;
    gap: 10px;
    align-items: center;
    background: color-mix(in srgb, var(--paper) 96%, transparent);
    border-top: var(--rule) solid var(--ink);
  }
  .arrow, #context-toggle {
    height: 38px;
    border: var(--rule) solid var(--ink);
    background: transparent;
    cursor: pointer;
  }
  .arrow { width: 44px; }
  #context-toggle { min-width: 132px; padding: 0 12px; font-size: 9px; font-weight: 700; text-transform: uppercase; }
  .arrow:disabled { color: var(--faint); border-color: var(--faint); cursor: default; }
  #manual-note { margin: 0; text-align: center; color: var(--muted); font-size: 9px; letter-spacing: .04em; text-transform: uppercase; }
  #loading {
    position: absolute;
    z-index: 30;
    inset: 0;
    display: grid;
    place-items: center;
    background: var(--paper);
    font-size: 12px;
  }
  #loading[data-state="error"] {
    padding: 32px;
    text-align: center;
    white-space: pre-line;
  }
  @media (max-width: 820px) {
    :root { --rail: 72px; --head: 126px; }
    #rail-heading h1 { display: none; }
    #rail-heading { padding-inline: 8px; }
    .shot-button { grid-template-columns: 1fr; padding-inline: 8px; }
    .shot-number { text-align: center; }
    .shot-name, .segment-name { display: none; }
    #masthead { padding: 14px 15px 12px; grid-template-columns: 1fr; gap: 7px; }
    #posture { display: none; }
    #scope-ids { max-width: 72vw; }
    #transport { padding-inline: 8px; }
    #context-toggle { min-width: 100px; }
  }
</style>
</head>
<body>
<aside id="shot-rail" aria-label="Planned shot registry">
  <header id="rail-heading">
    <p>Course production</p>
    <h1>21 planned shots</h1>
  </header>
  <nav id="shot-list" aria-label="Planned shots"></nav>
</aside>
<header id="masthead">
  <div>
    <p id="eyebrow"></p>
    <h2 id="title"></h2>
    <p id="scope-summary"></p>
    <p id="scope-ids"></p>
  </div>
  <aside id="posture">
    <p id="shot-id"></p>
    <p id="mode"></p>
    <p id="reveal-summary"></p>
  </aside>
</header>
<main id="stage" aria-label="Manual planned-shot review surface">
  <section id="three-mount" aria-label="Three-dimensional shot geometry"></section>
  <section id="map-stage" aria-label="Two-dimensional shot geometry">
    <svg id="map-svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Focused engineering map">__MAP_SCENE__</svg>
  </section>
</main>
<nav id="transport" aria-label="Manual review controls">
  <button class="arrow" id="previous" type="button" aria-label="Previous planned shot">←</button>
  <p id="manual-note">Manual review · select every change</p>
  <button id="context-toggle" type="button">Show anchor</button>
  <button class="arrow" id="next" type="button" aria-label="Next planned shot">→</button>
</nav>
<div id="loading">Loading the planned-shot registry…</div>
<script id="review-data" type="application/json">__DATA__</script>
<script>
(() => {
  const overlay = document.getElementById("loading");
  const onError = event => window.__gigawattStartupError(event.error || event.message);
  const onRejection = event => window.__gigawattStartupError(event.reason);
  window.__gigawattStartupError = error => {
    const detail = error instanceof Error ? error.message : String(error || "Unknown startup error");
    overlay.dataset.state = "error";
    overlay.setAttribute("role", "alert");
    overlay.textContent = `Unable to start this course view.\n${detail}`;
  };
  window.__gigawattReady = () => {
    window.removeEventListener("error", onError, true);
    window.removeEventListener("unhandledrejection", onRejection);
    overlay.remove();
  };
  window.addEventListener("error", onError, true);
  window.addEventListener("unhandledrejection", onRejection);
})();
</script>
<script type="importmap">
{"imports":{"three":"./vendor/three/three.module.js","three/addons/controls/OrbitControls.js":"./vendor/three/OrbitControls.js","three/addons/renderers/CSS2DRenderer.js":"./vendor/three/CSS2DRenderer.js"}}
</script>
<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";

try {
const data = JSON.parse(document.getElementById("review-data").textContent);
const $ = id => document.getElementById(id);
const shots = data.registry.shots;
const stage = $("stage");
const mount = $("three-mount");
const mapStage = $("map-stage");
const mapSvg = $("map-svg");
const hiddenNodes = new Set(data.hidden.nodes);
const hiddenEdges = new Set(data.hidden.edges);
const hiddenCopy = new Set(data.hidden.copy);

const scene = new THREE.Scene();
scene.background = new THREE.Color(data.scene.palette.paper);
scene.fog = new THREE.Fog(data.scene.palette.paper, data.scene.world.fog.near, data.scene.world.fog.far);
const camera = new THREE.PerspectiveCamera(40, stage.clientWidth / stage.clientHeight, 1, 5000);
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(stage.clientWidth, stage.clientHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
mount.appendChild(renderer.domElement);
const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(stage.clientWidth, stage.clientHeight);
labelRenderer.domElement.id = "labels";
mount.appendChild(labelRenderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.minDistance = 90;
controls.maxDistance = 3600;
controls.maxPolarAngle = Math.PI * 0.49;

scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d8cf, 1.45));
const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
keyLight.position.set(700, 1100, 650);
scene.add(keyLight);

function material(spec, context = false) {
  const opacity = context ? Math.min(spec.opacity ?? 1, 0.2) : (spec.opacity ?? 1);
  const value = new THREE.MeshLambertMaterial({
    color: data.scene.palette[spec.fill],
    flatShading: true,
    opacity,
    transparent: opacity < 1
  });
  value.userData.baseOpacity = opacity;
  return value;
}

function primitiveMesh(spec, context = false) {
  let geometry;
  if (spec.shape === "box") geometry = new THREE.BoxGeometry(...spec.size);
  else if (spec.shape === "cylinder") geometry = new THREE.CylinderGeometry(spec.radius, spec.radius, spec.height, 16);
  else throw new Error(`Unsupported shape: ${spec.shape}`);
  const mesh = new THREE.Mesh(geometry, material(spec, context));
  mesh.position.set(...spec.at);
  if (spec.rotate) mesh.rotation.set(...spec.rotate.map(THREE.MathUtils.degToRad));
  return mesh;
}

function addPrimitives(parent, primitives, offset = [0, 0, 0], context = false) {
  const materials = [];
  for (const spec of primitives) {
    const mesh = primitiveMesh(spec, context);
    mesh.position.add(new THREE.Vector3(...offset));
    parent.add(mesh);
    materials.push(mesh.material);
  }
  return materials;
}

const ground = data.scene.world.ground;
const groundMesh = new THREE.Mesh(
  new THREE.PlaneGeometry(...ground.size),
  material({ fill: ground.fill, opacity: 0.2 }, true)
);
groundMesh.rotation.x = -Math.PI / 2;
groundMesh.position.set(...ground.at);
scene.add(groundMesh);
for (const structure of data.scene.structures) {
  const group = new THREE.Group();
  scene.add(group);
  if (structure.repeat) {
    for (let index = 0; index < structure.repeat.count; index += 1) {
      addPrimitives(group, structure.primitives, structure.repeat.step.map(value => value * index), true);
    }
  } else {
    addPrimitives(group, structure.primitives, [0, 0, 0], true);
  }
}

const nodeObjects = new Map();
const nodeLabels = new Map();
for (const node of data.scene.nodes) {
  const group = new THREE.Group();
  group.position.set(...node.position);
  group.userData.materials = addPrimitives(group, node.primitives);
  group.userData.baseVisible = node.base_visible;
  scene.add(group);

  const element = document.createElement("div");
  element.className = "node-label";
  element.textContent = node.label;
  const posture = document.createElement("small");
  posture.textContent = `${node.presence.replaceAll("_", " ")} · ${node.lifecycle.replaceAll("_", " ")}`;
  element.appendChild(posture);
  const label = new CSS2DObject(element);
  label.position.set(...node.label_position);
  label.visible = false;
  scene.add(label);
  group.userData.label = label;
  nodeObjects.set(node.id, group);
  nodeLabels.set(node.id, node.label);
}

function segmentedCurve(points) {
  const curve = new THREE.CurvePath();
  for (let index = 1; index < points.length; index += 1) {
    curve.add(new THREE.LineCurve3(new THREE.Vector3(...points[index - 1]), new THREE.Vector3(...points[index])));
  }
  return curve;
}

const edgeObjects = new Map();
for (const edge of data.scene.edges) {
  const curve = segmentedCurve(edge.points);
  const edgeMaterial = new THREE.MeshBasicMaterial({
    color: data.scene.palette[edge.token],
    opacity: 0.025,
    transparent: true
  });
  const mesh = new THREE.Mesh(
    new THREE.TubeGeometry(curve, Math.max(12, edge.points.length * 10), data.scene.stroke.heavy * 0.72, 8, false),
    edgeMaterial
  );
  scene.add(mesh);
  const marker = new THREE.Mesh(
    new THREE.ConeGeometry(5.2, 14, 10),
    new THREE.MeshBasicMaterial({ color: data.scene.palette[edge.token] })
  );
  const markerPosition = curve.getPoint(0.64);
  const markerDirection = curve.getTangent(0.64).normalize();
  marker.position.copy(markerPosition);
  marker.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), markerDirection);
  marker.visible = false;
  scene.add(marker);
  edgeObjects.set(edge.id, { mesh, marker, baseVisible: edge.base_visible, flowDirection: edge.flow_direction });
}

const mapNodes = [...mapSvg.querySelectorAll('[id^="node-"]')];
const mapEdges = [...mapSvg.querySelectorAll('[id^="edge-"]')];
const mapLabels = [...mapSvg.querySelectorAll('[id^="label-"]')];
const mapLegend = mapSvg.querySelector("#status-legend");

function render3d() {
  for (const object of nodeObjects.values()) {
    object.userData.label.element.style.marginTop = "0px";
  }
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);

  const stageRect = stage.getBoundingClientRect();
  const labels = [...nodeObjects.values()]
    .map(object => object.userData.label)
    .filter(label => label.visible)
    .map(label => ({ label, rect: label.element.getBoundingClientRect() }))
    .sort((left, right) => left.rect.x - right.rect.x || left.rect.y - right.rect.y);
  const placed = [];
  const offsets = [0];
  for (let step = 1; step <= labels.length; step += 1) {
    offsets.push(-40 * step, 40 * step);
  }
  for (const item of labels) {
    const offset = offsets.find(candidate => {
      const shifted = {
        left: item.rect.left,
        right: item.rect.right,
        top: item.rect.top + candidate,
        bottom: item.rect.bottom + candidate
      };
      if (shifted.top < stageRect.top + 6 || shifted.bottom > stageRect.bottom - 6) return false;
      return placed.every(other =>
        shifted.right + 5 <= other.left ||
        shifted.left >= other.right + 5 ||
        shifted.bottom + 5 <= other.top ||
        shifted.top >= other.bottom + 5
      );
    }) ?? 0;
    item.label.element.style.marginTop = `${offset}px`;
    placed.push({
      left: item.rect.left,
      right: item.rect.right,
      top: item.rect.top + offset,
      bottom: item.rect.bottom + offset
    });
  }
}

function applyMapFocus(shot) {
  const focusNodes = new Set(shot.focus_nodes);
  const focusEdges = new Set(shot.focus_edges);
  const reveals = new Set(shot.reveal_ids);
  const copyReveals = new Set(shot.reveal_copy_ids);
  for (const element of mapNodes) {
    const id = element.id.slice(5);
    const visible = !hiddenNodes.has(id) || reveals.has(id);
    element.style.display = visible ? "inline" : "none";
    element.style.opacity = focusNodes.has(id) ? "1" : ".08";
  }
  for (const element of mapEdges) {
    const id = element.id.slice(5);
    const visible = !hiddenEdges.has(id) || reveals.has(id);
    element.style.display = visible ? "inline" : "none";
    element.style.opacity = focusEdges.has(id) ? "1" : ".06";
  }
  for (const element of mapLabels) {
    const id = element.id.slice(6);
    const visible = !hiddenCopy.has(id) || copyReveals.has(id);
    element.style.display = visible ? "inline" : "none";
    element.style.opacity = copyReveals.has(id) ? "1" : ".20";
  }
  if (mapLegend) mapLegend.style.opacity = ".20";
}

function apply3dFocus(shot) {
  const focusNodes = new Set(shot.focus_nodes);
  const focusEdges = new Set(shot.focus_edges);
  const reveals = new Set(shot.reveal_ids);
  for (const [id, object] of nodeObjects) {
    const visible = object.userData.baseVisible || reveals.has(id);
    const selected = visible && focusNodes.has(id);
    object.visible = visible;
    for (const item of object.userData.materials) {
      item.opacity = item.userData.baseOpacity * (selected ? 1 : 0.035);
      item.transparent = item.opacity < 1;
    }
    object.userData.label.visible = selected;
  }
  for (const [id, object] of edgeObjects) {
    const visible = object.baseVisible || reveals.has(id);
    const selected = visible && focusEdges.has(id);
    object.mesh.visible = visible;
    object.mesh.material.opacity = selected ? .96 : .025;
    object.marker.visible = selected && object.flowDirection !== "none";
  }
}

let current = 0;
let showingAnchor = false;

function setFrame(shot) {
  if (shot.frame.kind === "2d") {
    const view = showingAnchor ? shot.frame.anchor_viewBox : shot.frame.viewBox;
    mapSvg.setAttribute("viewBox", view.join(" "));
    return;
  }
  const position = showingAnchor ? shot.frame.anchor_position : shot.frame.position;
  const target = showingAnchor ? shot.frame.anchor_target : shot.frame.target;
  camera.position.set(...position);
  camera.up.set(...shot.frame.up);
  controls.target.set(...target);
  controls.update();
  render3d();
}

function activate(index) {
  current = Math.max(0, Math.min(shots.length - 1, index));
  showingAnchor = false;
  const shot = shots[current];
  const is3d = shot.render_mode === "3d";
  mount.style.display = is3d ? "block" : "none";
  mapStage.style.display = is3d ? "none" : "block";
  if (is3d) apply3dFocus(shot);
  else applyMapFocus(shot);
  setFrame(shot);

  $("eyebrow").textContent = `${String(shot.sequence).padStart(2, "0")} / ${shots.length} · ${shot.segment_id}`;
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
  $("context-toggle").textContent = "Show anchor";
  document.querySelectorAll(".shot-button").forEach((button, buttonIndex) => {
    if (buttonIndex === current) {
      button.setAttribute("aria-current", "step");
      button.scrollIntoView({ block: "nearest" });
    } else {
      button.removeAttribute("aria-current");
    }
  });
  $("previous").disabled = current === 0;
  $("next").disabled = current === shots.length - 1;
}

const shotList = $("shot-list");
shots.forEach((shot, index) => {
  const button = document.createElement("button");
  button.className = "shot-button";
  button.type = "button";
  const number = document.createElement("span");
  number.className = "shot-number";
  number.textContent = String(shot.sequence).padStart(2, "0");
  const labels = document.createElement("span");
  const name = document.createElement("span");
  name.className = "shot-name";
  name.textContent = shot.id;
  const segment = document.createElement("span");
  segment.className = "segment-name";
  segment.textContent = shot.segment_id;
  labels.append(name, segment);
  button.append(number, labels);
  button.addEventListener("click", () => activate(index));
  shotList.appendChild(button);
});

$("previous").addEventListener("click", () => activate(current - 1));
$("next").addEventListener("click", () => activate(current + 1));
$("context-toggle").addEventListener("click", () => {
  showingAnchor = !showingAnchor;
  $("context-toggle").textContent = showingAnchor ? "Show shot" : "Show anchor";
  setFrame(shots[current]);
});
addEventListener("keydown", event => {
  if (event.key === "ArrowLeft") activate(current - 1);
  if (event.key === "ArrowRight") activate(current + 1);
});
controls.addEventListener("change", render3d);
addEventListener("resize", () => {
  camera.aspect = stage.clientWidth / stage.clientHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(stage.clientWidth, stage.clientHeight);
  labelRenderer.setSize(stage.clientWidth, stage.clientHeight);
  render3d();
});

activate(0);
window.__gigawattReady();
} catch (error) {
  window.__gigawattStartupError(error);
  throw error;
}
</script>
</body>
</html>
"""


def build_artifacts() -> tuple[str, str, str]:
    course, cameras, master, layout, scene = load_inputs()
    digest = _source_digest(master)
    registry = compile_registry(
        course,
        cameras,
        master,
        layout,
        scene,
        source_digest=digest,
    )
    registry_json = scene_pipeline.canonical_payload(registry) + "\n"

    evidence = scene_pipeline.load_yaml(ROOT / master["meta"]["evidence_file"])
    _, map_scene = layout_pipeline.compose(master, layout, evidence)
    shared = scene_pipeline.build_payload(master, scene, cameras)
    review_payload = {
        "registry": registry,
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
    html = (
        REVIEW_HTML.replace("__DATA__", _script_safe_payload(review_payload))
        .replace("__MAP_SCENE__", map_scene)
        .replace("__DIGEST__", digest)
        .replace("__PAPER__", tokens.PAPER)
        .replace("__INK__", tokens.INK)
        .replace("__FAINT__", tokens.FAINT)
        .replace("__MUTED__", tokens.MUTED_TEXT)
        .replace("__FONT__", tokens.FONT)
    )
    return registry_json, html, digest


def main() -> None:
    registry_json, html, digest = build_artifacts()
    REGISTRY_PATH.write_text(registry_json)
    REVIEW_PATH.write_text(html)
    print(
        f"built {REGISTRY_PATH.relative_to(ROOT)} and {REVIEW_PATH.relative_to(ROOT)} "
        f"· {EXPECTED_PLANNED_SHOTS} manual shots · digest {digest}"
    )


if __name__ == "__main__":
    main()
