"""Build the master-ID-driven hybrid 2D/3D teaching substrate.

`master.yaml` owns topology and facts. `scene.yaml` owns spatial placement,
`cameras.yaml` owns views, and this module only validates and compiles them into
one deterministic browser player.

Usage: uv run python -m gigawatt.scene
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import struct
from copy import deepcopy
from datetime import date, datetime
from fractions import Fraction
from itertools import pairwise
from pathlib import Path
from typing import Any

import yaml

from . import tokens

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
ALLOWED_MODES = {"2d", "3d", "overlay"}
ALLOWED_SHAPES = {"box", "cylinder"}
CANONICAL_CAMERA_IDS = (
    "system_orientation",
    "campus_establishing",
    "electrical_room",
    "data_hall_rack",
    "watt_heat_handoff",
    "thermal_return",
)
CANONICAL_STRUCTURE_IDS = (
    "campus-pad",
    "data-hall-shell",
    "electrical-room-partition",
    "rack-row-context",
)
MAX_REPEAT_COUNT = 256
MAX_EXPANDED_PRIMITIVES = 2_048
MIN_EDGE_POINTS = 2
MAX_EDGE_POINTS = 32
MAX_TOTAL_EDGE_POINTS = 512
MIN_EDGE_TUBE_SEGMENTS = 12
EDGE_TUBE_SEGMENTS_PER_POINT = 10
MAX_TOTAL_EDGE_TUBE_SEGMENTS = 5_120
FLOAT32_MAX = float.fromhex("0x1.fffffep+127")
FLOAT32_MIN_NORMAL = float.fromhex("0x1p-126")
FLOAT32_MIN_SUBNORMAL = float.fromhex("0x1p-149")
WEBGL_FLOAT32_HEADROOM = 16
MAX_WEBGL_MAGNITUDE = FLOAT32_MAX / WEBGL_FLOAT32_HEADROOM
EDGE_TUBE_RADIUS = tokens.STROKE_HEAVY * 0.72
EDGE_TUBE_RADIAL_SEGMENTS = 8
PULSE_RADIUS = 6.2
MIN_VISIBLE_FOCUS_OPACITY = 1 / 255
MIN_HYBRID_FOCUSED_EDGE_OPACITY = 0.42
HYBRID_CONFIRMED_EDGE_OPACITY = 0.96
EDGE_FLOW_MARKER_RADIUS = 5.2
EDGE_FLOW_MARKER_HEIGHT = 14.0
EDGE_FOCUS_ENVELOPE_RADIUS = max(
    EDGE_TUBE_RADIUS,
    PULSE_RADIUS,
    math.hypot(EDGE_FLOW_MARKER_RADIUS, EDGE_FLOW_MARKER_HEIGHT / 2),
)
THREE_CAMERA_VERTICAL_FOV_DEGREES = 40.0
THREE_CAMERA_NEAR = 1.0
THREE_CAMERA_FAR = 5_000.0
THREE_CAMERA_MIN_DISTANCE = 90.0
THREE_HYBRID_CAMERA_MAX_DISTANCE = 3_200.0
THREE_REVIEW_CAMERA_MAX_DISTANCE = 3_600.0
THREE_CAMERA_MIN_POLAR_ANGLE_FRACTION = 0.0
THREE_CAMERA_MAX_POLAR_ANGLE_FRACTION = 0.49
CAMERA_CONTROL_ANGLE_MARGIN_RADIANS = 1e-6
CAMERA_VISIBILITY_NUMERIC_MARGIN = 1.0
CAMERA_FLOAT32_OPERATION_COUNT = 32
CAMERA_FLOAT32_GAMMA = (
    CAMERA_FLOAT32_OPERATION_COUNT
    * 2**-24
    / (1 - CAMERA_FLOAT32_OPERATION_COUNT * 2**-24)
)
CAMERA_FOCUS_COVERAGE_POLICY = (
    ("1920x1080", 1920, 1080, 1, 1),
    ("1440x900", 1440, 900, 1, 1),
    # The planned-shot canvas at 1024x768 excludes its 286px rail and its
    # 112px/74px header and transport.  It is narrower than the full viewport.
    ("1024x768", 738, 582, 1, 1),
    ("844x390", 844, 390, 1, 1),
    ("390x844", 390, 844, 1, 3),
)
SCENE_ROOT_FIELDS = {"meta", "world", "structures", "nodes", "edges"}
SCENE_META_FIELDS = {"version", "master", "units", "coverage"}
SCENE_WORLD_FIELDS = {"camera_up", "ground", "fog"}
SCENE_GROUND_FIELDS = {"size", "at", "fill"}
SCENE_FOG_FIELDS = {"near", "far"}
SCENE_STRUCTURE_REQUIRED_FIELDS = {"id", "primitives"}
SCENE_STRUCTURE_OPTIONAL_FIELDS = {"repeat"}
SCENE_REPEAT_FIELDS = {"count", "step"}
SCENE_NODE_FIELDS = {"at", "label_at", "primitives"}
SCENE_EDGE_REQUIRED_FIELDS = {"points"}
SCENE_EDGE_OPTIONAL_FIELDS = {"tone"}
PRIMITIVE_COMMON_REQUIRED_FIELDS = {"shape", "at", "fill"}
PRIMITIVE_OPTIONAL_FIELDS = {"rotate", "opacity"}
PRIMITIVE_REQUIRED_FIELDS_BY_SHAPE = {
    "box": {"size"},
    "cylinder": {"radius", "height"},
}
CAMERA_ROOT_FIELDS = {"meta", "vertical_slice", "cameras"}
CAMERA_META_FIELDS = {"version", "master", "scene"}
CAMERA_COMMON_FIELDS = {
    "id",
    "mode",
    "title",
    "subtitle",
    "viewBox",
    "well",
    "focus_nodes",
    "focus_edges",
}
CAMERA_OPTIONAL_FIELDS_BY_MODE = {
    "2d": {"compact_viewBox", "focus_labels"},
    "3d": {"label_offsets", "label_nodes", "pulse_edges"},
    "overlay": {"compact_viewBox", "focus_labels"},
}
CAMERA_REQUIRED_FIELDS_BY_MODE = {
    "2d": {"map_view"},
    "3d": {"position", "target"},
    "overlay": {"map_view", "map_asset", "annotation"},
}
CAMERA_ANNOTATION_FIELDS = {"node", "fields"}


class ManifestError(ValueError):
    """Raised when a scene or camera reference drifts from the master."""


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects silent mapping-key replacement."""


def _construct_unique_mapping(
    loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False
) -> dict[Any, Any]:
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            mark = key_node.start_mark
            raise ManifestError(
                f"{mark.name}:{mark.line + 1}:{mark.column + 1}: "
                "unhashable YAML mapping key"
            ) from exc
        if duplicate:
            mark = key_node.start_mark
            raise ManifestError(
                f"{mark.name}:{mark.line + 1}:{mark.column + 1}: "
                f"duplicate YAML key {key!r}"
            )
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        with path.open() as stream:
            data = yaml.load(stream, Loader=_UniqueKeyLoader)
    except ManifestError:
        raise
    except (OSError, yaml.YAMLError) as exc:
        raise ManifestError(f"{path}: invalid YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise ManifestError(f"{path.name}: expected a mapping")
    return data


def palette() -> dict[str, str]:
    """Expose the Python design tokens under renderer-neutral names."""
    values = {
        "ink": tokens.INK,
        "paper": tokens.PAPER,
        "faint": tokens.FAINT,
        "muted": tokens.MUTED_TEXT,
    }
    values.update({f"voltage:{name}": color for name, color in tokens.VOLTAGE.items()})
    values.update({f"thermal:{name}": color for name, color in tokens.THERMAL.items()})
    return values


def edge_key(edge: dict[str, Any]) -> str:
    return edge.get("id") or f"{edge['from']}->{edge['to']}"


def _is_finite_number(value: Any) -> bool:
    if type(value) not in {int, float}:
        return False
    try:
        return math.isfinite(float(value))
    except OverflowError:
        return False


def _finite_number(value: Any, location: str) -> None:
    if not _is_finite_number(value):
        raise ManifestError(f"{location}: expected a finite number")


def _is_webgl_safe_number(value: Any) -> bool:
    return _is_finite_number(value) and abs(float(value)) <= MAX_WEBGL_MAGNITUDE


def _webgl_safe_number(value: Any, location: str) -> None:
    if not _is_webgl_safe_number(value):
        raise ManifestError(
            f"{location}: expected a finite number with magnitude no greater than "
            f"the WebGL Float32-safe bound {MAX_WEBGL_MAGNITUDE!r}"
        )


def _webgl_float32(value: float) -> float:
    """Return the value WebGL receives after IEEE-754 Float32 conversion."""
    return struct.unpack(">f", struct.pack(">f", float(value)))[0]


def _webgl_float32_vector(value: list[int | float]) -> tuple[float, ...]:
    return tuple(_webgl_float32(item) for item in value)


def _derived_webgl_safe_number(value: Any, location: str) -> None:
    if not _is_webgl_safe_number(value):
        raise ManifestError(
            f"{location}: derived magnitude must not exceed the WebGL "
            f"Float32-safe bound {MAX_WEBGL_MAGNITUDE!r}"
        )


def _positive_number(value: Any, location: str) -> None:
    _webgl_safe_number(value, location)
    if value <= 0:
        raise ManifestError(f"{location}: expected a positive number")
    if _webgl_float32(value) <= 0:
        raise ManifestError(
            f"{location}: positive dimension must remain positive after WebGL "
            "Float32 quantization"
        )


def _unit_interval_number(value: Any, location: str) -> None:
    _finite_number(value, location)
    if not 0 <= value <= 1:
        raise ManifestError(f"{location}: expected a number from 0 through 1")


def _numeric_vector(value: Any, length: int, location: str) -> None:
    if not isinstance(value, list) or len(value) != length:
        raise ManifestError(f"{location}: expected {length} finite numeric coordinates")
    for index, item in enumerate(value):
        _webgl_safe_number(item, f"{location}[{index}]")


def _rectangle(value: Any, location: str) -> None:
    _numeric_vector(value, 4, location)
    for index, dimension in ((2, "width"), (3, "height")):
        _positive_number(value[index], f"{location}.{dimension}")


def _triplet(value: Any, location: str) -> None:
    _numeric_vector(value, 3, location)


def _positive_vector(value: Any, length: int, location: str) -> None:
    _numeric_vector(value, length, location)
    for index, item in enumerate(value):
        _positive_number(item, f"{location}[{index}]")


def _schema_keys(
    value: Any,
    required: set[str],
    optional: set[str],
    location: str,
) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManifestError(f"{location}: expected a mapping")
    keys = set(value)
    missing = required - keys
    extra = keys - required - optional
    if missing or extra:
        raise ManifestError(
            f"{location}: fields must be exact; "
            f"missing={sorted(missing)} extra={sorted(extra, key=repr)}"
        )
    return value


def _exact_keys(value: Any, expected: set[str], location: str) -> dict[str, Any]:
    return _schema_keys(value, expected, set(), location)


def _nonempty_string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{location}: expected a non-empty string")
    return value


def _id_list(value: Any, location: str) -> list[str]:
    if not isinstance(value, list) or any(
        not isinstance(item, str) or not item for item in value
    ):
        raise ManifestError(f"{location}: expected a list of non-empty IDs")
    if len(value) != len(set(value)):
        raise ManifestError(f"{location}: IDs must be unique")
    return value


def _validate_camera_manifest_schema(cameras: Any) -> list[dict[str, Any]]:
    root = _exact_keys(cameras, CAMERA_ROOT_FIELDS, "cameras.yaml")
    meta = _exact_keys(root["meta"], CAMERA_META_FIELDS, "cameras.meta")
    if type(meta["version"]) is not int or meta["version"] != 1:
        raise ManifestError("cameras.meta.version must be integer 1")
    if meta["master"] != "master.yaml" or meta["scene"] != "scene.yaml":
        raise ManifestError(
            "cameras.meta must reference master.yaml and scene.yaml exactly"
        )

    sequence_value = root["vertical_slice"]
    if not isinstance(sequence_value, list) or len(sequence_value) != len(
        CANONICAL_CAMERA_IDS
    ):
        raise ManifestError(
            "cameras.vertical_slice must contain exactly the six canonical camera IDs"
        )
    sequence = _id_list(sequence_value, "cameras.vertical_slice")
    if tuple(sequence) != CANONICAL_CAMERA_IDS:
        raise ManifestError(
            "cameras.vertical_slice must match the canonical camera ID order exactly"
        )

    camera_list = root["cameras"]
    if not isinstance(camera_list, list) or len(camera_list) != len(
        CANONICAL_CAMERA_IDS
    ):
        raise ManifestError(
            "cameras.yaml.cameras must contain exactly the six canonical cameras"
        )
    for index, camera in enumerate(camera_list):
        location = f"cameras.cameras[{index}]"
        if not isinstance(camera, dict):
            raise ManifestError(f"{location}: expected a mapping")
        mode = camera.get("mode")
        if not isinstance(mode, str) or mode not in ALLOWED_MODES:
            raise ManifestError(f"{location}.mode: unsupported mode {mode!r}")
        expected = (
            CAMERA_COMMON_FIELDS
            | CAMERA_REQUIRED_FIELDS_BY_MODE[mode]
            | CAMERA_OPTIONAL_FIELDS_BY_MODE[mode]
        )
        required = CAMERA_COMMON_FIELDS | CAMERA_REQUIRED_FIELDS_BY_MODE[mode]
        missing = required - set(camera)
        extra = set(camera) - expected
        if missing or extra:
            raise ManifestError(
                f"{location}: fields must be exact for {mode}; "
                f"missing={sorted(missing)} extra={sorted(extra)}"
            )
        for field in ("id", "title", "subtitle"):
            _nonempty_string(camera[field], f"{location}.{field}")
        if camera["id"] != CANONICAL_CAMERA_IDS[index]:
            raise ManifestError(
                f"{location}.id must be {CANONICAL_CAMERA_IDS[index]!r}"
            )
        _id_list(camera["focus_nodes"], f"{location}.focus_nodes")
        _id_list(camera["focus_edges"], f"{location}.focus_edges")
        if "focus_labels" in camera:
            _id_list(camera["focus_labels"], f"{location}.focus_labels")
        if "label_nodes" in camera:
            _id_list(camera["label_nodes"], f"{location}.label_nodes")
        if "label_offsets" in camera and not isinstance(camera["label_offsets"], dict):
            raise ManifestError(f"{location}.label_offsets must be a mapping")
        if "pulse_edges" in camera:
            pulse_edges = _id_list(camera["pulse_edges"], f"{location}.pulse_edges")
            if not set(pulse_edges) <= set(camera["focus_edges"]):
                raise ManifestError(
                    f"{location}.pulse_edges must be a subset of focus_edges"
                )
        if "map_asset" in camera:
            map_asset = _nonempty_string(camera["map_asset"], f"{location}.map_asset")
            if Path(map_asset).name != map_asset or not map_asset.endswith(".svg"):
                raise ManifestError(
                    f"{location}.map_asset must be a local SVG filename"
                )
        if "annotation" in camera:
            annotation = _exact_keys(
                camera["annotation"],
                CAMERA_ANNOTATION_FIELDS,
                f"{location}.annotation",
            )
            _nonempty_string(annotation["node"], f"{location}.annotation.node")
            annotation_fields = _id_list(
                annotation["fields"], f"{location}.annotation.fields"
            )
            if not annotation_fields:
                raise ManifestError(f"{location}.annotation.fields must be non-empty")

    return camera_list


def _primitive_list(value: Any, location: str) -> list[dict[str, Any]]:
    if not isinstance(value, list) or not value:
        raise ManifestError(f"{location}: primitives must be a non-empty list")
    return value


def _validate_primitive_schema(primitive: Any, location: str) -> None:
    if not isinstance(primitive, dict):
        raise ManifestError(f"{location}: expected a mapping")
    shape = primitive.get("shape")
    if not isinstance(shape, str) or shape not in ALLOWED_SHAPES:
        raise ManifestError(f"{location}: unsupported shape {shape!r}")
    required = (
        PRIMITIVE_COMMON_REQUIRED_FIELDS | PRIMITIVE_REQUIRED_FIELDS_BY_SHAPE[shape]
    )
    _schema_keys(primitive, required, PRIMITIVE_OPTIONAL_FIELDS, location)


def edge_tube_segment_count(point_count: int) -> int:
    return max(MIN_EDGE_TUBE_SEGMENTS, point_count * EDGE_TUBE_SEGMENTS_PER_POINT)


def _validate_scene_manifest_schema(scene: Any) -> dict[str, Any]:
    root = _exact_keys(scene, SCENE_ROOT_FIELDS, "scene.yaml")
    meta = _exact_keys(root["meta"], SCENE_META_FIELDS, "scene.meta")
    if type(meta["version"]) is not int or meta["version"] != 1:
        raise ManifestError("scene.meta.version must be integer 1")
    if meta["master"] != "master.yaml":
        raise ManifestError("scene.meta.master must reference master.yaml exactly")
    _nonempty_string(meta["units"], "scene.meta.units")
    if not isinstance(meta["coverage"], str) or meta["coverage"] not in {
        "exact",
        "subset",
    }:
        raise ManifestError("scene.meta.coverage must be exact or subset")

    world = _exact_keys(root["world"], SCENE_WORLD_FIELDS, "scene.world")
    _exact_keys(world["ground"], SCENE_GROUND_FIELDS, "scene.world.ground")
    _exact_keys(world["fog"], SCENE_FOG_FIELDS, "scene.world.fog")

    structures = root["structures"]
    if not isinstance(structures, list) or len(structures) != len(
        CANONICAL_STRUCTURE_IDS
    ):
        raise ManifestError(
            "scene.structures must contain exactly the four canonical context layers"
        )
    structure_ids: list[str] = []
    structure_primitives: list[tuple[str, list[dict[str, Any]], int]] = []
    for index, structure_value in enumerate(structures):
        location = f"scene.structures[{index}]"
        structure = _schema_keys(
            structure_value,
            SCENE_STRUCTURE_REQUIRED_FIELDS,
            SCENE_STRUCTURE_OPTIONAL_FIELDS,
            location,
        )
        structure_id = _nonempty_string(structure["id"], f"{location}.id")
        if structure_id != CANONICAL_STRUCTURE_IDS[index]:
            raise ManifestError(
                f"{location}.id must be {CANONICAL_STRUCTURE_IDS[index]!r}"
            )
        structure_ids.append(structure_id)
        primitives = _primitive_list(structure["primitives"], location)
        repeat_count = 1
        if "repeat" in structure:
            repeat = _exact_keys(
                structure["repeat"],
                SCENE_REPEAT_FIELDS,
                f"{location}.repeat",
            )
            repeat_count = repeat["count"]
            if (
                type(repeat_count) is not int
                or repeat_count < 1
                or repeat_count > MAX_REPEAT_COUNT
            ):
                raise ManifestError(
                    f"{location}.repeat.count: invalid; expected an integer from "
                    f"1 through {MAX_REPEAT_COUNT}"
                )
        structure_primitives.append((location, primitives, repeat_count))
    if len(structure_ids) != len(set(structure_ids)):
        raise ManifestError("scene.structures: IDs must be unique")

    nodes = root["nodes"]
    if not isinstance(nodes, dict):
        raise ManifestError("scene.nodes: expected an ID-keyed mapping")
    node_primitives: list[tuple[str, list[dict[str, Any]]]] = []
    for node_id, node_value in nodes.items():
        if not isinstance(node_id, str) or not node_id:
            raise ManifestError("scene.nodes: IDs must be non-empty strings")
        location = f"scene.nodes.{node_id}"
        node = _exact_keys(node_value, SCENE_NODE_FIELDS, location)
        node_primitives.append(
            (location, _primitive_list(node["primitives"], location))
        )

    edges = root["edges"]
    if not isinstance(edges, dict):
        raise ManifestError("scene.edges: expected an ID-keyed mapping")
    edge_point_counts: list[int] = []
    for edge_id, edge_value in edges.items():
        if not isinstance(edge_id, str) or not edge_id:
            raise ManifestError("scene.edges: IDs must be non-empty strings")
        edge = _schema_keys(
            edge_value,
            SCENE_EDGE_REQUIRED_FIELDS,
            SCENE_EDGE_OPTIONAL_FIELDS,
            f"scene.edges.{edge_id}",
        )
        points = edge["points"]
        if not isinstance(points, list):
            raise ManifestError(f"scene.edges.{edge_id}.points: expected a list")
        point_count = len(points)
        if point_count < MIN_EDGE_POINTS or point_count > MAX_EDGE_POINTS:
            raise ManifestError(
                f"scene.edges.{edge_id}.points: edge point count must be from "
                f"{MIN_EDGE_POINTS} through {MAX_EDGE_POINTS}; count={point_count}"
            )
        edge_point_counts.append(point_count)

    total_edge_points = sum(edge_point_counts)
    if total_edge_points > MAX_TOTAL_EDGE_POINTS:
        raise ManifestError(
            "scene.edges: total edge point budget exceeded; "
            f"count={total_edge_points} limit={MAX_TOTAL_EDGE_POINTS}"
        )
    total_edge_tube_segments = sum(
        edge_tube_segment_count(point_count) for point_count in edge_point_counts
    )
    if total_edge_tube_segments > MAX_TOTAL_EDGE_TUBE_SEGMENTS:
        raise ManifestError(
            "scene.edges: total TubeGeometry segment budget exceeded; "
            f"count={total_edge_tube_segments} "
            f"limit={MAX_TOTAL_EDGE_TUBE_SEGMENTS}"
        )

    expanded_primitive_count = sum(
        len(primitives) * repeat_count
        for _, primitives, repeat_count in structure_primitives
    ) + sum(len(primitives) for _, primitives in node_primitives)
    if expanded_primitive_count > MAX_EXPANDED_PRIMITIVES:
        raise ManifestError(
            "scene: expanded primitive budget exceeded; "
            f"count={expanded_primitive_count} limit={MAX_EXPANDED_PRIMITIVES}"
        )

    for location, primitives, _ in structure_primitives:
        for index, primitive in enumerate(primitives):
            _validate_primitive_schema(primitive, f"{location}.primitives[{index}]")
    for location, primitives in node_primitives:
        for index, primitive in enumerate(primitives):
            _validate_primitive_schema(primitive, f"{location}.primitives[{index}]")
    return root


def _validate_primitives(primitives: Any, location: str, token_names: set[str]) -> None:
    primitives = _primitive_list(primitives, location)
    for index, primitive in enumerate(primitives):
        here = f"{location}.primitives[{index}]"
        shape = primitive.get("shape")
        _triplet(primitive.get("at"), f"{here}.at")
        if shape == "box":
            _positive_vector(primitive.get("size"), 3, f"{here}.size")
        else:
            _positive_number(primitive.get("radius"), f"{here}.radius")
            _positive_number(primitive.get("height"), f"{here}.height")
        if primitive.get("fill") not in token_names:
            raise ManifestError(
                f"{here}.fill: unknown shared token {primitive.get('fill')!r}"
            )
        if "rotate" in primitive:
            _triplet(primitive["rotate"], f"{here}.rotate")
        if "opacity" in primitive:
            _unit_interval_number(primitive["opacity"], f"{here}.opacity")


def _primitive_bounding_radius(primitive: dict[str, Any]) -> float:
    if primitive["shape"] == "box":
        return math.hypot(*(float(value) / 2 for value in primitive["size"]))
    return math.hypot(float(primitive["radius"]), float(primitive["height"]) / 2)


def _primitive_axis_extents(primitive: dict[str, Any]) -> tuple[float, float, float]:
    if primitive["shape"] == "box":
        size = primitive["size"]
        return float(size[0]) / 2, float(size[1]) / 2, float(size[2]) / 2
    radius = float(primitive["radius"])
    return radius, float(primitive["height"]) / 2, radius


def _primitive_rotation_matrix(
    rotate: list[int | float],
) -> tuple[tuple[float, float, float], ...]:
    x, y, z = (math.radians(float(value)) / 2 for value in rotate)
    cos_x, sin_x = math.cos(x), math.sin(x)
    cos_y, sin_y = math.cos(y), math.sin(y)
    cos_z, sin_z = math.cos(z), math.sin(z)
    quaternion_x = sin_x * cos_y * cos_z + cos_x * sin_y * sin_z
    quaternion_y = cos_x * sin_y * cos_z - sin_x * cos_y * sin_z
    quaternion_z = cos_x * cos_y * sin_z + sin_x * sin_y * cos_z
    quaternion_w = cos_x * cos_y * cos_z - sin_x * sin_y * sin_z
    x2 = quaternion_x + quaternion_x
    y2 = quaternion_y + quaternion_y
    z2 = quaternion_z + quaternion_z
    xx = quaternion_x * x2
    xy = quaternion_x * y2
    xz = quaternion_x * z2
    yy = quaternion_y * y2
    yz = quaternion_y * z2
    zz = quaternion_z * z2
    wx = quaternion_w * x2
    wy = quaternion_w * y2
    wz = quaternion_w * z2
    return (
        (1 - (yy + zz), xy - wz, xz + wy),
        (xy + wz, 1 - (xx + zz), yz - wx),
        (xz - wy, yz + wx, 1 - (xx + yy)),
    )


def _primitive_local_float32_vertices(
    primitive: dict[str, Any],
) -> tuple[tuple[float, float, float], ...]:
    if primitive["shape"] == "box":
        half_extents = tuple(
            _webgl_float32(float(value) / 2) for value in primitive["size"]
        )
        return tuple(
            tuple(
                extent if corner & (1 << axis) else -extent
                for axis, extent in enumerate(half_extents)
            )
            for corner in range(8)
        )

    radius = float(primitive["radius"])
    half_height = _webgl_float32(float(primitive["height"]) / 2)
    return tuple(
        (
            _webgl_float32(radius * math.sin(segment * math.tau / 16)),
            half_height if upper else -half_height,
            _webgl_float32(radius * math.cos(segment * math.tau / 16)),
        )
        for upper in (False, True)
        for segment in range(16)
    )


def _float32_affine_rank(points: tuple[tuple[float, float, float], ...]) -> int:
    anchor = tuple(Fraction(value) for value in points[0])
    basis: list[tuple[Fraction, Fraction, Fraction]] = []
    for point in points[1:]:
        vector = tuple(
            Fraction(value) - anchor[index] for index, value in enumerate(point)
        )
        if vector == (0, 0, 0):
            continue
        if not basis:
            basis.append(vector)
            continue
        cross = (
            basis[0][1] * vector[2] - basis[0][2] * vector[1],
            basis[0][2] * vector[0] - basis[0][0] * vector[2],
            basis[0][0] * vector[1] - basis[0][1] * vector[0],
        )
        if len(basis) == 1:
            if cross != (0, 0, 0):
                basis.append(vector)
            continue
        if sum(cross[index] * basis[1][index] for index in range(3)) != 0:
            return 3
    return len(basis)


def _primitive_gpu_float32_vertices(
    primitive: dict[str, Any],
    center: tuple[float, float, float],
) -> tuple[tuple[float, float, float], ...]:
    rotate = primitive.get("rotate", [0, 0, 0])
    matrix = tuple(
        tuple(_webgl_float32(value) for value in row)
        for row in _primitive_rotation_matrix(rotate)
    )
    translation = tuple(_webgl_float32(value) for value in center)
    return tuple(
        tuple(
            _webgl_float32_transform_coordinate(
                matrix[world_axis], vertex, translation[world_axis]
            )
            for world_axis in range(3)
        )
        for vertex in _primitive_local_float32_vertices(primitive)
    )


def _rotated_primitive_gpu_float32_vertices(
    primitive: dict[str, Any],
    center: tuple[float, float, float],
) -> tuple[tuple[float, float, float], ...]:
    return _primitive_gpu_float32_vertices(primitive, center)


def _webgl_float32_transform_coordinate(
    matrix_row: tuple[float, float, float],
    vertex: tuple[float, float, float],
    translation: float,
) -> float:
    value = translation
    for coefficient, coordinate in zip(matrix_row, vertex, strict=True):
        value = _webgl_float32(value + _webgl_float32(coefficient * coordinate))
    return value


def _camera_focus_points(
    scene: dict[str, Any], camera: dict[str, Any]
) -> tuple[tuple[str, tuple[float, float, float], float, float | None], ...]:
    camera_id = camera["id"]
    points: list[
        tuple[str, tuple[float, float, float], float, float | None]
    ] = []
    geometry_witness_count = 0
    for node_id in camera["focus_nodes"]:
        node = scene["nodes"].get(node_id)
        if node is None:
            raise ManifestError(
                f"camera {camera_id}: focus node {node_id!r} has no scene geometry"
            )
        for primitive_index, primitive in enumerate(node["primitives"]):
            if _webgl_float32(float(primitive.get("opacity", 1))) < _webgl_float32(
                MIN_VISIBLE_FOCUS_OPACITY
            ):
                continue
            center = tuple(
                float(node["at"][axis]) + float(primitive["at"][axis])
                for axis in range(3)
            )
            vertices = _primitive_gpu_float32_vertices(primitive, center)
            points.extend(
                (
                    (
                        f"node:{node_id}.primitive[{primitive_index}]"
                        f".vertex[{vertex_index}]"
                    ),
                        vertex,
                        0.0,
                        _webgl_float32(float(primitive.get("opacity", 1))),
                    )
                for vertex_index, vertex in enumerate(vertices)
            )
            geometry_witness_count += len(vertices)

    rendered_label_nodes = camera.get("label_nodes", camera["focus_nodes"])
    for node_id in rendered_label_nodes:
        node = scene["nodes"].get(node_id)
        if node is None:
            raise ManifestError(
                f"camera {camera_id}: label node {node_id!r} has no scene geometry"
            )
        points.append(
            (
                f"label:{node_id}",
                tuple(_webgl_float32(value) for value in node["label_at"]),
                0.0,
                None,
            )
        )

    for edge_id in camera["focus_edges"]:
        edge = scene["edges"].get(edge_id)
        if edge is None:
            raise ManifestError(
                f"camera {camera_id}: focus edge {edge_id!r} has no scene geometry"
            )
        points.extend(
            (
                f"edge:{edge_id}[{point_index}]",
                tuple(_webgl_float32(value) for value in point),
                EDGE_FOCUS_ENVELOPE_RADIUS,
                MIN_HYBRID_FOCUSED_EDGE_OPACITY,
            )
            for point_index, point in enumerate(edge["points"])
        )
        geometry_witness_count += len(edge["points"])
    if not geometry_witness_count:
        raise ManifestError(
            f"camera {camera_id}: 3D anchor must retain at least one rendered "
            "focus-geometry witness"
        )
    return tuple(points)


def _camera_float32_view_rows(
    camera: dict[str, Any], camera_up: list[int | float]
) -> tuple[tuple[tuple[float, float, float], float], ...]:
    camera_id = camera["id"]
    position = tuple(float(value) for value in camera["position"])
    target = tuple(float(value) for value in camera["target"])
    quantized_position = tuple(_webgl_float32(value) for value in position)
    quantized_target = tuple(_webgl_float32(value) for value in target)
    quantized_direction = tuple(
        _webgl_float32(quantized_target[index] - quantized_position[index])
        for index in range(3)
    )
    if quantized_direction == (0.0, 0.0, 0.0):
        raise ManifestError(
            f"camera {camera_id}: position-target direction must remain nonzero "
            "after WebGL Float32 quantization"
        )

    backward = tuple(position[index] - target[index] for index in range(3))
    backward_length = math.sqrt(sum(value * value for value in backward))
    if not math.isfinite(backward_length) or backward_length == 0:
        raise ManifestError(f"camera {camera_id}: invalid 3D direction")
    maximum_distance = min(
        THREE_HYBRID_CAMERA_MAX_DISTANCE, THREE_REVIEW_CAMERA_MAX_DISTANCE
    )
    if not (
        THREE_CAMERA_MIN_DISTANCE + CAMERA_VISIBILITY_NUMERIC_MARGIN
        < backward_length
        < maximum_distance - CAMERA_VISIBILITY_NUMERIC_MARGIN
    ):
        raise ManifestError(
            f"camera {camera_id}: authored position-target distance must remain "
            "strictly inside every renderer OrbitControls range; "
            f"distance={backward_length!r} "
            f"minimum={THREE_CAMERA_MIN_DISTANCE!r} maximum={maximum_distance!r}"
        )
    backward_inverse_length = 1 / backward_length
    backward = tuple(value * backward_inverse_length for value in backward)
    up = tuple(float(value) for value in camera_up)
    up_length = math.sqrt(sum(value * value for value in up))
    if not math.isfinite(up_length) or up_length == 0:
        raise ManifestError(f"camera {camera_id}: camera up must be nonzero")
    up_inverse_length = 1 / up_length
    up = tuple(value * up_inverse_length for value in up)
    polar_angle = math.acos(
        max(-1.0, min(1.0, sum(backward[index] * up[index] for index in range(3))))
    )
    minimum_polar_angle = math.pi * THREE_CAMERA_MIN_POLAR_ANGLE_FRACTION
    maximum_polar_angle = math.pi * THREE_CAMERA_MAX_POLAR_ANGLE_FRACTION
    if not (
        minimum_polar_angle + CAMERA_CONTROL_ANGLE_MARGIN_RADIANS
        < polar_angle
        < maximum_polar_angle - CAMERA_CONTROL_ANGLE_MARGIN_RADIANS
    ):
        raise ManifestError(
            f"camera {camera_id}: authored position-target polar angle must remain "
            "strictly inside every renderer OrbitControls range; "
            f"angle={polar_angle!r} maximum={maximum_polar_angle!r}"
        )
    right = (
        up[1] * backward[2] - up[2] * backward[1],
        up[2] * backward[0] - up[0] * backward[2],
        up[0] * backward[1] - up[1] * backward[0],
    )
    right_length = math.sqrt(sum(value * value for value in right))
    if not math.isfinite(right_length) or right_length == 0:
        raise ManifestError(
            f"camera {camera_id}: position-target direction must remain "
            "nonparallel to camera up"
        )
    right_inverse_length = 1 / right_length
    right = tuple(value * right_inverse_length for value in right)
    resolved_up = (
        backward[1] * right[2] - backward[2] * right[1],
        backward[2] * right[0] - backward[0] * right[2],
        backward[0] * right[1] - backward[1] * right[0],
    )
    rows = []
    for basis in (right, resolved_up, backward):
        quantized_basis = tuple(_webgl_float32(value) for value in basis)
        translation = _webgl_float32(
            -sum(basis[index] * position[index] for index in range(3))
        )
        rows.append((quantized_basis, translation))
    return tuple(rows)


def _camera_float32_view_coordinate(
    row: tuple[float, float, float],
    point: tuple[float, float, float],
    translation: float,
    envelope_radius: float,
) -> tuple[float, float]:
    terms = tuple(
        coefficient * coordinate
        for coefficient, coordinate in zip(row, point, strict=True)
    )
    coordinate = math.fsum((*terms, translation))
    magnitude_sum = math.fsum((*(abs(term) for term in terms), abs(translation)))
    rounding_error = (
        CAMERA_FLOAT32_GAMMA * magnitude_sum
        + CAMERA_FLOAT32_OPERATION_COUNT * FLOAT32_MIN_SUBNORMAL
    )
    envelope_extent = envelope_radius * math.sqrt(
        sum(coefficient * coefficient for coefficient in row)
    )
    return coordinate, rounding_error + envelope_extent


def _webgl_float32_smoothstep(edge0: float, edge1: float, value: float) -> float:
    lower = _webgl_float32(edge0)
    upper = _webgl_float32(edge1)
    coordinate = _webgl_float32(value)
    interval = _webgl_float32(upper - lower)
    ratio = _webgl_float32(_webgl_float32(coordinate - lower) / interval)
    ratio = min(1.0, max(0.0, ratio))
    squared = _webgl_float32(ratio * ratio)
    falloff = _webgl_float32(3.0 - _webgl_float32(2.0 * ratio))
    return _webgl_float32(squared * falloff)


def _camera_focus_visibility(
    scene: dict[str, Any], camera: dict[str, Any]
) -> dict[str, Any]:
    """Model authored focus-point visibility through Three's Float32 view state."""
    points = _camera_focus_points(scene, camera)
    rows = _camera_float32_view_rows(camera, scene["world"]["camera_up"])
    view_points = {}
    for point_id, point, envelope_radius, opacity in points:
        coordinates_and_errors = tuple(
            _camera_float32_view_coordinate(row, point, translation, envelope_radius)
            for row, translation in rows
        )
        view_points[point_id] = (
            tuple(record[0] for record in coordinates_and_errors),
            tuple(record[1] for record in coordinates_and_errors),
            opacity,
        )
    camera_near = _webgl_float32(THREE_CAMERA_NEAR)
    camera_far = _webgl_float32(THREE_CAMERA_FAR)
    fog_far = _webgl_float32(float(scene["world"]["fog"]["far"]))
    depth_visible = {
        point_id
        for point_id, (view_point, error, _) in view_points.items()
        if -view_point[2] - error[2] > camera_near + CAMERA_VISIBILITY_NUMERIC_MARGIN
        and -view_point[2] + error[2] < camera_far - CAMERA_VISIBILITY_NUMERIC_MARGIN
        and -view_point[2] + error[2] < fog_far - CAMERA_VISIBILITY_NUMERIC_MARGIN
    }
    fog_near = _webgl_float32(float(scene["world"]["fog"]["near"]))
    minimum_effective_opacity = _webgl_float32(MIN_VISIBLE_FOCUS_OPACITY)
    effective_geometry_witness_ids = []
    for point_id, (view_point, error, opacity) in view_points.items():
        if opacity is None or point_id not in depth_visible:
            continue
        conservative_depth = (
            -view_point[2] + error[2] + CAMERA_VISIBILITY_NUMERIC_MARGIN
        )
        fog_factor = _webgl_float32_smoothstep(
            fog_near, fog_far, conservative_depth
        )
        fog_attenuation = _webgl_float32(1.0 - fog_factor)
        effective_opacity = _webgl_float32(
            _webgl_float32(opacity) * fog_attenuation
        )
        if effective_opacity >= minimum_effective_opacity:
            effective_geometry_witness_ids.append(point_id)
    viewport_coverage = []
    vertical_tangent = math.tan(math.radians(THREE_CAMERA_VERTICAL_FOV_DEGREES / 2))
    vertical_scale = _webgl_float32(1 / vertical_tangent)
    for (
        viewport_id,
        width,
        height,
        minimum_numerator,
        minimum_denominator,
    ) in CAMERA_FOCUS_COVERAGE_POLICY:
        aspect = width / height
        horizontal_scale = _webgl_float32(1 / (vertical_tangent * aspect))
        visible = []
        for point_id, (view_point, error, _) in view_points.items():
            view_x, view_y, view_z = view_point
            depth = -view_z
            depth_lower = depth - error[2] - CAMERA_VISIBILITY_NUMERIC_MARGIN
            clip_x = horizontal_scale * view_x
            clip_y = vertical_scale * view_y
            clip_x_error = (
                abs(horizontal_scale) * error[0]
                + CAMERA_FLOAT32_GAMMA
                * abs(horizontal_scale)
                * (abs(view_x) + error[0])
                + CAMERA_FLOAT32_OPERATION_COUNT * FLOAT32_MIN_SUBNORMAL
            )
            clip_y_error = (
                abs(vertical_scale) * error[1]
                + CAMERA_FLOAT32_GAMMA
                * abs(vertical_scale)
                * (abs(view_y) + error[1])
                + CAMERA_FLOAT32_OPERATION_COUNT * FLOAT32_MIN_SUBNORMAL
            )
            if (
                point_id in depth_visible
                and abs(clip_x) + clip_x_error < depth_lower
                and abs(clip_y) + clip_y_error < depth_lower
            ):
                visible.append(point_id)
        viewport_coverage.append(
            {
                "viewport_id": viewport_id,
                "surface_width": width,
                "surface_height": height,
                "point_count": len(points),
                "visible_point_count": len(visible),
                "minimum_numerator": minimum_numerator,
                "minimum_denominator": minimum_denominator,
            }
        )
    return {
        "point_count": len(points),
        "depth_visible_point_count": len(depth_visible),
        "depth_invisible_point_ids": sorted(set(view_points) - depth_visible),
        "effective_geometry_witness_count": len(effective_geometry_witness_ids),
        "effective_geometry_witness_point_ids": effective_geometry_witness_ids,
        "viewport_coverage": viewport_coverage,
    }


def _validate_camera_focus_visibility(
    scene: dict[str, Any], camera: dict[str, Any]
) -> None:
    coverage = _camera_focus_visibility(scene, camera)
    camera_id = camera["id"]
    if coverage["depth_visible_point_count"] != coverage["point_count"]:
        raise ManifestError(
            f"camera {camera_id}: 3D anchor focus geometry must remain inside "
            "PerspectiveCamera near/far and scene fog visibility; "
            f"invisible_points={coverage['depth_invisible_point_ids']}"
        )
    for viewport in coverage["viewport_coverage"]:
        if (
            viewport["visible_point_count"] * viewport["minimum_denominator"]
            < viewport["point_count"] * viewport["minimum_numerator"]
        ):
            raise ManifestError(
                f"camera {camera_id}: 3D anchor focus geometry coverage at "
                f"{viewport['viewport_id']} must be at least "
                f"{viewport['minimum_numerator']}/{viewport['minimum_denominator']}; "
                f"visible={viewport['visible_point_count']} "
                f"declared={viewport['point_count']}"
            )
    if not coverage["effective_geometry_witness_count"]:
        raise ManifestError(
            f"camera {camera_id}: 3D anchor must retain rendered focus geometry "
            "with effective post-fog opacity of at least one 8-bit step"
        )


def _validate_rotated_primitive_float32_volume(
    primitive: dict[str, Any],
    center: tuple[float, float, float],
    location: str,
) -> None:
    if "rotate" not in primitive:
        return
    if (
        _float32_affine_rank(_rotated_primitive_gpu_float32_vertices(primitive, center))
        < 3
    ):
        raise ManifestError(
            f"{location}: rotation-aware transformed primitive geometry must "
            "retain nonzero volume after WebGL Float32 quantization"
        )


def _validate_float32_extent(center: float, extent: float, location: str) -> None:
    low = center - extent
    high = center + extent
    _derived_webgl_safe_number(low, f"{location}.minimum")
    _derived_webgl_safe_number(high, f"{location}.maximum")
    quantized_low = _webgl_float32(low)
    quantized_center = _webgl_float32(center)
    quantized_high = _webgl_float32(high)
    if not quantized_low < quantized_center < quantized_high:
        raise ManifestError(
            f"{location}: authored center and extent must remain distinguishable "
            "after WebGL Float32 quantization"
        )


def _float32_rounding_error_bound(lower: float, upper: float) -> float:
    magnitude = max(abs(lower), abs(upper))
    if magnitude < FLOAT32_MIN_NORMAL:
        return FLOAT32_MIN_SUBNORMAL / 2
    _, exponent = math.frexp(magnitude)
    return math.ldexp(1.0, exponent - 25)


def _edge_tube_cross_section_rounding_error_bound(
    points: list[list[int | float]],
) -> float:
    axis_errors = []
    for coordinate_index in range(3):
        coordinates = [float(point[coordinate_index]) for point in points]
        axis_errors.append(
            _float32_rounding_error_bound(
                min(coordinates) - EDGE_TUBE_RADIUS,
                max(coordinates) + EDGE_TUBE_RADIUS,
            )
        )
    # Eight radial segments include both diameter pairs, +/-N and +/-B. Their
    # combined perturbation is bounded by this Frobenius-norm factor.
    return math.sqrt(2) * math.hypot(*axis_errors)


def _validate_primitive_world_bounds(
    primitives: list[dict[str, Any]],
    base: list[int | float],
    offset: list[int | float],
    location: str,
) -> None:
    for primitive_index, primitive in enumerate(primitives):
        bounding_radius = _primitive_bounding_radius(primitive)
        axis_extents = _primitive_axis_extents(primitive)
        center = tuple(
            float(base[coordinate_index])
            + float(primitive["at"][coordinate_index])
            + float(offset[coordinate_index])
            for coordinate_index in range(3)
        )
        for coordinate_index in range(3):
            _derived_webgl_safe_number(
                abs(center[coordinate_index]) + bounding_radius,
                f"{location}.primitives[{primitive_index}].world_extent"
                f"[{coordinate_index}]",
            )
            _validate_float32_extent(
                center[coordinate_index],
                axis_extents[coordinate_index],
                f"{location}.primitives[{primitive_index}].world_extent"
                f"[{coordinate_index}]",
            )
        _validate_rotated_primitive_float32_volume(
            primitive,
            center,
            f"{location}.primitives[{primitive_index}].world_extent",
        )


def _validate_repeat_derived_coordinates(
    structure: dict[str, Any], location: str
) -> list[list[float]]:
    repeat = structure["repeat"]
    step = repeat["step"]
    try:
        _triplet(step, f"{location}.repeat.step")
    except ManifestError as exc:
        raise ManifestError(
            f"{location}.repeat.step: maximum repeat-derived offset must stay "
            "within the WebGL Float32-safe numeric domain"
        ) from exc
    final_repeat_index = repeat["count"] - 1
    final_offset = []
    for coordinate_index, coordinate in enumerate(step):
        derived = float(coordinate) * final_repeat_index
        if not _is_webgl_safe_number(derived):
            raise ManifestError(
                f"{location}.repeat.step[{coordinate_index}]: maximum "
                "repeat-derived offset must stay within the WebGL "
                "Float32-safe numeric domain"
            )
        final_offset.append(derived)

    offsets = [[0.0, 0.0, 0.0]]
    previous_offset = _webgl_float32_vector(offsets[0])
    for repeat_index in range(1, repeat["count"]):
        offset = [float(coordinate) * repeat_index for coordinate in step]
        quantized_offset = _webgl_float32_vector(offset)
        if quantized_offset == previous_offset:
            raise ManifestError(
                f"{location}.repeat.step: adjacent repeat-derived offsets must "
                "remain distinguishable after WebGL Float32 quantization; "
                f"repeat_index={repeat_index}"
            )
        offsets.append(offset)
        previous_offset = quantized_offset

    for primitive_index, primitive in enumerate(structure["primitives"]):
        for coordinate_index, (coordinate, offset) in enumerate(
            zip(primitive["at"], final_offset, strict=True)
        ):
            derived = float(coordinate) + offset
            if not _is_webgl_safe_number(derived):
                raise ManifestError(
                    f"{location}.primitives[{primitive_index}].at"
                    f"[{coordinate_index}]: maximum repeat-derived primitive "
                    "position must stay within the WebGL Float32-safe "
                    "numeric domain"
                )
        previous_position = _webgl_float32_vector(primitive["at"])
        for repeat_index in range(1, repeat["count"]):
            position = [
                float(coordinate) + float(step[index]) * repeat_index
                for index, coordinate in enumerate(primitive["at"])
            ]
            quantized_position = _webgl_float32_vector(position)
            if quantized_position == previous_position:
                raise ManifestError(
                    f"{location}.primitives[{primitive_index}].at: adjacent "
                    "repeat-derived primitive positions must remain "
                    "distinguishable after WebGL Float32 quantization; "
                    f"repeat_index={repeat_index}"
                )
            previous_position = quantized_position
    return offsets


def validate_camera_focus_labels(
    master: dict[str, Any], camera: dict[str, Any]
) -> list[str] | None:
    """Return a camera's safe copy focus, rejecting hidden-label bypasses."""
    cid = camera.get("id", "<unknown>")
    value = camera.get("focus_labels")
    if value is None:
        return None
    if not isinstance(value, list) or any(
        not isinstance(copy_id, str) for copy_id in value
    ):
        raise ManifestError(f"camera {cid}: focus_labels must be a list of copy IDs")
    if len(value) != len(set(value)):
        raise ManifestError(f"camera {cid}: focus_labels must be unique")

    master_copy = master.get("copy") or {}
    known_copy_ids = set(master_copy)
    hidden_copy_ids = {
        copy_id
        for copy_id, spec in master_copy.items()
        if spec.get("base_visible", True) is False
    }
    unknown_focus_labels = sorted(set(value) - known_copy_ids)
    hidden_focus_labels = sorted(set(value) & hidden_copy_ids)
    if unknown_focus_labels or hidden_focus_labels:
        raise ManifestError(
            f"camera {cid}: unknown_focus_labels={unknown_focus_labels} "
            f"hidden_focus_labels={hidden_focus_labels}"
        )
    return value


def _validate_webgl_numeric_fields(scene: dict[str, Any]) -> None:
    token_names = set(palette())
    world = scene["world"]
    camera_up = world.get("camera_up")
    _triplet(camera_up, "scene.world.camera_up")
    if _webgl_float32_vector(camera_up) == (0.0, 0.0, 0.0):
        raise ManifestError(
            "scene.world.camera_up: vector must remain nonzero after WebGL "
            "Float32 quantization"
        )
    fog = world["fog"]
    fog_near = fog.get("near")
    fog_far = fog.get("far")
    _webgl_safe_number(fog_near, "scene.world.fog.near")
    _webgl_safe_number(fog_far, "scene.world.fog.far")
    if fog_near < 0:
        raise ManifestError("scene.world.fog.near: expected a non-negative number")
    if fog_far <= fog_near:
        raise ManifestError("scene.world.fog.far: expected a number greater than near")
    if _webgl_float32(fog_far) <= _webgl_float32(fog_near):
        raise ManifestError(
            "scene.world.fog.far: interval must remain strictly ordered after "
            "WebGL Float32 quantization"
        )
    ground = world["ground"]
    if ground.get("fill") not in token_names:
        raise ManifestError("scene.world.ground.fill must reference a shared token")
    _positive_vector(ground.get("size"), 2, "scene.world.ground.size")
    _triplet(ground.get("at"), "scene.world.ground.at")
    ground_extent = math.hypot(*(float(value) / 2 for value in ground["size"]))
    for coordinate_index, coordinate in enumerate(ground["at"]):
        _derived_webgl_safe_number(
            abs(float(coordinate)) + ground_extent,
            f"scene.world.ground.world_extent[{coordinate_index}]",
        )
    for size_index, coordinate_index in enumerate((0, 2)):
        _validate_float32_extent(
            float(ground["at"][coordinate_index]),
            float(ground["size"][size_index]) / 2,
            f"scene.world.ground.world_extent[{coordinate_index}]",
        )

    for node_id, spec in scene["nodes"].items():
        _triplet(spec.get("at"), f"scene.nodes.{node_id}.at")
        _triplet(spec.get("label_at"), f"scene.nodes.{node_id}.label_at")
        _validate_primitives(
            spec.get("primitives"), f"scene.nodes.{node_id}", token_names
        )
        _validate_primitive_world_bounds(
            spec["primitives"],
            spec["at"],
            [0, 0, 0],
            f"scene.nodes.{node_id}",
        )

    for structure in scene["structures"]:
        sid = structure["id"]
        _validate_primitives(
            structure.get("primitives"), f"scene.structures.{sid}", token_names
        )
        offsets: list[list[int | float]] = [[0, 0, 0]]
        if "repeat" in structure:
            offsets = _validate_repeat_derived_coordinates(
                structure, f"scene.structures.{sid}"
            )
        for offset in offsets:
            _validate_primitive_world_bounds(
                structure["primitives"],
                [0, 0, 0],
                offset,
                f"scene.structures.{sid}",
            )

    for key, spec in scene["edges"].items():
        points = spec.get("points")
        if not isinstance(points, list) or len(points) < 2:
            raise ManifestError(
                f"scene.edges.{key}.points: expected at least two points"
            )
        quantized_points = []
        for index, point in enumerate(points):
            _triplet(point, f"scene.edges.{key}.points[{index}]")
            quantized_points.append(_webgl_float32_vector(point))
            for coordinate_index, coordinate in enumerate(point):
                _derived_webgl_safe_number(
                    abs(float(coordinate)) + EDGE_FOCUS_ENVELOPE_RADIUS,
                    f"scene.edges.{key}.points[{index}]"
                    f".world_extent[{coordinate_index}]",
                )
        if len(set(quantized_points)) == 1:
            raise ManifestError(
                f"scene.edges.{key}.points: total path must remain non-degenerate "
                "after WebGL Float32 quantization"
            )
        for segment_index, (start, end) in enumerate(pairwise(quantized_points)):
            if start == end:
                raise ManifestError(
                    f"scene.edges.{key}.points: every path segment must remain "
                    "nonzero after WebGL Float32 quantization; "
                    f"segment_index={segment_index}"
                )
        cross_section_error_bound = _edge_tube_cross_section_rounding_error_bound(
            points
        )
        if not cross_section_error_bound < EDGE_TUBE_RADIUS:
            raise ManifestError(
                f"scene.edges.{key}.points: TubeGeometry cross-section "
                "rounding-error bound must stay below its radius after WebGL "
                "Float32 quantization; "
                f"bound={cross_section_error_bound!r} radius={EDGE_TUBE_RADIUS!r}"
            )
        if "tone" in spec and spec["tone"] not in token_names:
            raise ManifestError(f"scene.edges.{key}.tone: unknown shared token")


def validate_webgl_numeric_domain(scene: dict[str, Any]) -> None:
    """Fail closed before scene numbers reach Float32 WebGL geometry or state."""
    scene = _validate_scene_manifest_schema(scene)
    _validate_webgl_numeric_fields(scene)


def validate(
    master: dict[str, Any], scene: dict[str, Any], cameras: dict[str, Any]
) -> None:
    """Fail closed on drift between semantic, spatial, and camera manifests."""
    scene = _validate_scene_manifest_schema(scene)
    _validate_webgl_numeric_fields(scene)
    camera_list = _validate_camera_manifest_schema(cameras)
    master_nodes = {node["id"] for node in master.get("nodes") or []}
    master_edge_records = {edge_key(edge): edge for edge in master.get("edges") or []}
    master_edges = set(master_edge_records)
    hidden_master_edges = {
        key
        for key, edge in master_edge_records.items()
        if edge.get("base_visible", True) is False
    }
    hidden_master_nodes = {
        node["id"]
        for node in master["nodes"]
        if node.get("base_visible", True) is False
    }
    if not master_nodes or not master_edges:
        raise ManifestError("master.yaml: nodes and edges must be non-empty")

    scene_nodes = set((scene.get("nodes") or {}).keys())
    scene_edges = set((scene.get("edges") or {}).keys())
    if scene.get("meta", {}).get("coverage") == "exact":
        missing_nodes = sorted(master_nodes - scene_nodes)
        extra_nodes = sorted(scene_nodes - master_nodes)
        missing_edges = sorted(master_edges - scene_edges)
        extra_edges = sorted(scene_edges - master_edges)
        if missing_nodes or extra_nodes or missing_edges or extra_edges:
            raise ManifestError(
                "scene/master coverage mismatch: "
                f"missing_nodes={missing_nodes} extra_nodes={extra_nodes} "
                f"missing_edges={missing_edges} extra_edges={extra_edges}"
            )
    elif not scene_nodes <= master_nodes or not scene_edges <= master_edges:
        raise ManifestError("scene contains node or edge IDs absent from master.yaml")

    camera_ids = [camera.get("id") for camera in camera_list]
    if not camera_ids or len(camera_ids) != len(set(camera_ids)):
        raise ManifestError("cameras.yaml: camera IDs must be present and unique")
    for camera in camera_list:
        cid = camera["id"]
        mode = camera.get("mode")
        if mode not in ALLOWED_MODES:
            raise ManifestError(f"camera {cid}: unsupported mode {mode!r}")
        _rectangle(camera.get("viewBox"), f"camera {cid}.viewBox")
        _rectangle(camera.get("well"), f"camera {cid}.well")
        validate_camera_focus_labels(master, camera)
        focus_nodes = set(camera["focus_nodes"])
        unknown_nodes = sorted(focus_nodes - master_nodes)
        hidden_focus_nodes = sorted(
            focus_nodes & hidden_master_nodes if mode == "3d" else set()
        )
        label_nodes_value = camera.get("label_nodes")
        if label_nodes_value is not None and not (
            isinstance(label_nodes_value, list)
            and all(isinstance(node_id, str) for node_id in label_nodes_value)
        ):
            raise ManifestError(f"camera {cid}: label_nodes must be a list of node IDs")
        label_nodes = set(label_nodes_value or [])
        unknown_label_nodes = sorted(label_nodes - master_nodes)
        nonfocus_label_nodes = sorted(label_nodes - focus_nodes)
        label_offsets = camera.get("label_offsets", {})
        invalid_label_offsets = sorted(
            (
                node_id
                for node_id, offset in label_offsets.items()
                if node_id not in focus_nodes
                or not isinstance(offset, list)
                or len(offset) != 2
                or any(not _is_webgl_safe_number(value) for value in offset)
            ),
            key=repr,
        )
        camera_edges = set(camera["focus_edges"]) | set(camera.get("pulse_edges") or [])
        unknown_edges = sorted(camera_edges - master_edges)
        hidden_camera_edges = sorted(camera_edges & hidden_master_edges)
        nonfocus_edge_endpoints = {
            edge_id: sorted(
                {
                    master_edge_records[edge_id]["from"],
                    master_edge_records[edge_id]["to"],
                }
                - focus_nodes
            )
            for edge_id in sorted(set(camera["focus_edges"]) & master_edges)
            if {
                master_edge_records[edge_id]["from"],
                master_edge_records[edge_id]["to"],
            }
            - focus_nodes
        }
        if (
            unknown_nodes
            or hidden_focus_nodes
            or unknown_label_nodes
            or nonfocus_label_nodes
            or invalid_label_offsets
            or unknown_edges
            or hidden_camera_edges
            or nonfocus_edge_endpoints
        ):
            raise ManifestError(
                f"camera {cid}: unknown_nodes={unknown_nodes} "
                f"hidden_focus_nodes={hidden_focus_nodes} "
                f"unknown_label_nodes={unknown_label_nodes} "
                f"nonfocus_label_nodes={nonfocus_label_nodes} "
                f"invalid_label_offsets={invalid_label_offsets} "
                f"unknown_edges={unknown_edges} hidden_edges={hidden_camera_edges} "
                f"nonfocus_edge_endpoints={nonfocus_edge_endpoints}"
            )
        if mode == "3d":
            _triplet(camera.get("position"), f"camera {cid}.position")
            _triplet(camera.get("target"), f"camera {cid}.target")
            _validate_camera_focus_visibility(scene, camera)
        else:
            _rectangle(camera.get("map_view"), f"camera {cid}.map_view")
            if "compact_viewBox" in camera:
                _rectangle(
                    camera["compact_viewBox"],
                    f"camera {cid}.compact_viewBox",
                )
        if annotation := camera.get("annotation"):
            if annotation.get("node") not in master_nodes:
                raise ManifestError(f"camera {cid}: annotation node is not in master")
            if annotation["node"] not in focus_nodes:
                raise ManifestError(
                    f"camera {cid}: annotation node must be in focus_nodes"
                )
            annotated_node = next(
                node for node in master["nodes"] if node["id"] == annotation["node"]
            )
            unknown_annotation_fields = sorted(
                set(annotation["fields"]) - set(annotated_node)
            )
            if unknown_annotation_fields:
                raise ManifestError(
                    f"camera {cid}: unknown annotation fields "
                    f"{unknown_annotation_fields}"
                )

    present_modes = {camera["mode"] for camera in camera_list}
    if present_modes != ALLOWED_MODES:
        raise ManifestError(
            f"cameras.yaml: vertical slice must exercise {sorted(ALLOWED_MODES)}"
        )


def _normalise_voltage(value: str) -> str:
    normalised = re.sub(r"[^0-9a-z.]", "", value.lower())
    return re.sub(r"(?:ac|dc)$", "", normalised)


def token_for_edge(carries: str, explicit: str | None = None) -> str:
    """Map a semantic carry to a shared token without a voltage claim table."""
    token_names = palette()
    if explicit:
        if explicit not in token_names:
            raise ManifestError(f"unknown edge tone {explicit!r}")
        return explicit
    if carries.startswith("electricity@"):
        semantic_token = carries.split("@", 1)[1]
        if semantic_token in tokens.VOLTAGE:
            return f"voltage:{semantic_token}"
        carried = _normalise_voltage(semantic_token)
        for name in tokens.VOLTAGE:
            if _normalise_voltage(name) == carried:
                return f"voltage:{name}"
        return "ink"
    if "@" in carries:
        medium, state = carries.split("@", 1)
        if medium in {"heat", "coolant"} and state in tokens.THERMAL:
            return f"thermal:{state}"
        if medium == "heat" and state == "solid" and "die_heat" in tokens.THERMAL:
            return "thermal:die_heat"
    if carries.startswith("water"):
        return "thermal:water"
    return "ink"


def _annotation(camera: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> None:
    annotation = camera.get("annotation")
    if not annotation:
        return
    node_id = annotation["node"]
    node = nodes[node_id]
    items = []
    for field in annotation["fields"]:
        value = node.get(field)
        if value is None or value == "":
            continue
        if isinstance(value, list):
            value = ", ".join(str(item) for item in value)
        items.append(
            {
                "field": field,
                "label": field.replace("_", " ").title(),
                "value": str(value),
            }
        )
    camera["annotation"] = {"node": node_id, "items": items}


def build_payload(
    master: dict[str, Any], scene: dict[str, Any], cameras: dict[str, Any]
) -> dict[str, Any]:
    validate(master, scene, cameras)
    master_nodes = {node["id"]: node for node in master["nodes"]}
    master_edges = {edge_key(edge): edge for edge in master["edges"]}

    scene_nodes = []
    for node_id, placement in scene["nodes"].items():
        semantic = master_nodes[node_id]
        scene_nodes.append(
            {
                "id": node_id,
                "label": semantic["label"],
                "domain": semantic.get("domain"),
                "gate": semantic.get("gate"),
                "presence": semantic.get("presence"),
                "lifecycle": semantic.get("lifecycle"),
                "as_of": semantic.get("as_of"),
                "source_ids": semantic.get("source_ids") or [],
                "base_visible": semantic.get("base_visible", True),
                "at_reference": semantic.get("at_reference"),
                "vendors": semantic.get("vendors") or [],
                "position": placement["at"],
                "label_position": placement["label_at"],
                "primitives": placement["primitives"],
            }
        )

    scene_edges = []
    for key, placement in scene["edges"].items():
        semantic = master_edges[key]
        scene_edges.append(
            {
                "id": key,
                "from": semantic["from"],
                "to": semantic["to"],
                "carries": semantic["carries"],
                "presence": semantic.get("presence"),
                "lifecycle": semantic.get("lifecycle"),
                "flow_direction": semantic.get("flow_direction"),
                "normal_state": semantic.get("normal_state"),
                "source_ids": semantic.get("source_ids") or [],
                "base_visible": semantic.get("base_visible", True),
                "points": placement["points"],
                "token": token_for_edge(semantic["carries"], placement.get("tone")),
            }
        )

    camera_list = deepcopy(cameras["cameras"])
    for camera in camera_list:
        _annotation(camera, master_nodes)

    return {
        "meta": {
            "title": "GIGAWATT — hybrid vertical slice",
            "reference_campus": master.get("reference_campus", {}).get("name"),
            "master_version": master.get("meta", {}).get("version"),
        },
        "palette": palette(),
        "font": tokens.FONT,
        "stroke": {"standard": tokens.STROKE, "heavy": tokens.STROKE_HEAVY},
        "world": scene["world"],
        "structures": scene.get("structures") or [],
        "nodes": scene_nodes,
        "edges": scene_edges,
        "cameras": camera_list,
        "vertical_slice": cameras["vertical_slice"],
    }


def canonical_payload(payload: dict[str, Any]) -> str:
    def serialise(value: Any) -> str:
        if isinstance(value, (date, datetime)):
            return value.isoformat()
        raise TypeError(f"cannot serialise {type(value).__name__}")

    try:
        return json.dumps(
            payload,
            allow_nan=False,
            default=serialise,
            ensure_ascii=False,
            separators=(",", ":"),
            sort_keys=True,
        )
    except (TypeError, ValueError) as error:
        raise ManifestError(f"payload serialization failed: {error}") from error


HTML = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>GIGAWATT — hybrid vertical slice</title>
<style>
  :root {
    --paper: __PAPER__;
    --ink: __INK__;
    --faint: __FAINT__;
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
  button { font: inherit; color: inherit; }
  #app { position: relative; width: 100%; height: 100%; background: var(--paper); }
  #three-mount, #map-stage { position: absolute; inset: 0; }
  #three-mount canvas { display: block; width: 100%; height: 100%; }
  #labels { position: absolute; inset: 0; pointer-events: none; }
  #map-stage {
    display: none;
    padding: 118px 36px 94px;
    background: var(--paper);
  }
  #map-svg { width: 100%; height: 100%; display: block; }
  #masthead {
    position: absolute;
    z-index: 8;
    top: 0;
    left: 0;
    right: 0;
    min-height: 94px;
    padding: 21px 28px 16px;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 24px;
    background: color-mix(in srgb, var(--paper) 94%, transparent);
    border-bottom: var(--rule) solid var(--ink);
  }
  #title { margin: 0; font-size: 19px; line-height: 1.15; font-weight: 700; }
  #state-title { margin: 5px 0 0; font-size: 13px; line-height: 1.25; font-weight: 700; }
  #state-subtitle { margin: 3px 0 0; max-width: 760px; font-size: 11px; line-height: 1.3; }
  #mode {
    align-self: start;
    min-width: 62px;
    padding: 5px 7px;
    border: var(--rule) solid var(--ink);
    text-align: center;
    font-size: 10px;
    font-weight: 700;
    letter-spacing: .08em;
    text-transform: uppercase;
  }
  .node-label {
    padding: 3px 6px;
    color: var(--ink);
    background: color-mix(in srgb, var(--paper) 88%, transparent);
    border: 1px solid var(--ink);
    font-size: 10px;
    line-height: 1.15;
    font-weight: 650;
    white-space: nowrap;
  }
  .node-label small {
    display: block;
    margin-top: 2px;
    color: var(--ink);
    font-size: 8px;
    font-weight: 450;
    letter-spacing: .04em;
    text-transform: uppercase;
  }
  #annotation {
    position: absolute;
    z-index: 7;
    display: none;
    right: 42px;
    top: 132px;
    width: min(390px, calc(100vw - 84px));
    padding: 15px 17px 16px;
    background: color-mix(in srgb, var(--paper) 96%, transparent);
    border: var(--rule) solid var(--ink);
  }
  #annotation-source {
    margin: 0 0 10px;
    font-size: 9px;
    letter-spacing: .08em;
    text-transform: uppercase;
  }
  .annotation-row { padding: 8px 0; border-top: 1px solid var(--faint); }
  .annotation-key { display: block; margin-bottom: 3px; font-size: 9px; font-weight: 700; text-transform: uppercase; }
  .annotation-value { display: block; font-size: 11px; line-height: 1.35; }
  #transport {
    position: absolute;
    z-index: 9;
    left: 0;
    right: 0;
    bottom: 0;
    min-height: 72px;
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 12px;
    align-items: center;
    padding: 12px 18px;
    background: color-mix(in srgb, var(--paper) 95%, transparent);
    border-top: var(--rule) solid var(--ink);
  }
  .arrow {
    width: 38px;
    height: 34px;
    border: var(--rule) solid var(--ink);
    background: transparent;
    cursor: pointer;
  }
  .arrow:disabled { color: var(--faint); border-color: var(--faint); cursor: default; }
  #steps { display: flex; justify-content: center; gap: 5px; min-width: 0; }
  .step {
    position: relative;
    width: min(128px, 15vw);
    min-width: 32px;
    height: 34px;
    overflow: hidden;
    padding: 0 8px;
    border: 0;
    border-bottom: 3px solid var(--faint);
    background: transparent;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 9px;
    cursor: pointer;
  }
  .step[aria-current="step"] { border-bottom-color: var(--ink); font-weight: 700; }
  #loading {
    position: absolute;
    z-index: 20;
    inset: 0;
    display: grid;
    place-items: center;
    background: var(--paper);
    font-size: 12px;
  }
  @media (max-width: 720px) {
    #masthead { padding: 15px 17px 12px; min-height: 88px; }
    #title { font-size: 16px; }
    #state-subtitle { max-width: 76vw; }
    #map-stage { padding: 100px 10px 80px; }
    #transport { padding-inline: 9px; gap: 5px; }
    .step { width: 28px; padding: 0; color: transparent; }
    .step::after { content: attr(data-number); color: var(--ink); }
    #annotation { top: 105px; right: 14px; width: calc(100vw - 28px); }
  }
  @media (prefers-reduced-motion: reduce) {
    *, *::before, *::after { scroll-behavior: auto !important; }
  }
</style>
</head>
<body>
<main id="app" aria-label="Hybrid 2D and 3D view of the GIGAWATT master diagram">
  <section id="three-mount" aria-label="Three-dimensional campus view"></section>
  <section id="map-stage" aria-label="Two-dimensional engineering map">
    <svg id="map-svg" viewBox="0 0 1920 1080" preserveAspectRatio="xMidYMid meet" role="img" aria-label="Master engineering diagram">
      <image id="map-image" href="master.svg" x="0" y="0" width="1920" height="1080"></image>
    </svg>
  </section>
  <header id="masthead">
    <div>
      <h1 id="title"></h1>
      <p id="state-title"></p>
      <p id="state-subtitle"></p>
    </div>
    <div id="mode"></div>
  </header>
  <aside id="annotation" aria-live="polite">
    <p id="annotation-source"></p>
    <div id="annotation-rows"></div>
  </aside>
  <nav id="transport" aria-label="Vertical slice camera states">
    <button class="arrow" id="previous" type="button" aria-label="Previous camera state">←</button>
    <div id="steps"></div>
    <button class="arrow" id="next" type="button" aria-label="Next camera state">→</button>
  </nav>
  <div id="loading">Loading the scene…</div>
</main>
<script id="scene-data" type="application/json">__DATA__</script>
<script type="importmap">
{"imports":{"three":"./vendor/three/three.module.js","three/addons/controls/OrbitControls.js":"./vendor/three/OrbitControls.js","three/addons/renderers/CSS2DRenderer.js":"./vendor/three/CSS2DRenderer.js"}}
</script>
<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";

const data = JSON.parse(document.getElementById("scene-data").textContent);
const $ = id => document.getElementById(id);
const mount = $("three-mount");
const mapStage = $("map-stage");
const mapSvg = $("map-svg");
const mapImage = $("map-image");
const annotation = $("annotation");
const scene = new THREE.Scene();
const CONTEXT_LAYER = 0;
const FOCUS_LAYER = 1;
scene.background = new THREE.Color(data.palette.paper);
scene.fog = new THREE.Fog(data.palette.paper, data.world.fog.near, data.world.fog.far);

const camera = new THREE.PerspectiveCamera(
  __THREE_CAMERA_VERTICAL_FOV_DEGREES__,
  innerWidth / innerHeight,
  __THREE_CAMERA_NEAR__,
  __THREE_CAMERA_FAR__
);
camera.up.set(...data.world.camera_up).normalize();
const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: false });
renderer.setSize(innerWidth, innerHeight);
renderer.setPixelRatio(Math.min(devicePixelRatio, 2));
renderer.outputColorSpace = THREE.SRGBColorSpace;
mount.appendChild(renderer.domElement);

const labelRenderer = new CSS2DRenderer();
labelRenderer.setSize(innerWidth, innerHeight);
labelRenderer.domElement.id = "labels";
mount.appendChild(labelRenderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.08;
controls.minPolarAngle = Math.PI * __THREE_CAMERA_MIN_POLAR_ANGLE_FRACTION__;
controls.maxPolarAngle = Math.PI * __THREE_CAMERA_MAX_POLAR_ANGLE_FRACTION__;
controls.minDistance = __THREE_CAMERA_MIN_DISTANCE__;
controls.maxDistance = __THREE_HYBRID_CAMERA_MAX_DISTANCE__;
const initial3d = data.cameras.find(state => state.mode === "3d");
if (initial3d) {
  camera.position.set(...initial3d.position);
  controls.target.set(...initial3d.target);
  controls.update();
}

const hemisphereLight = new THREE.HemisphereLight(0xffffff, 0xd8d8cf, 1.45);
hemisphereLight.layers.enable(FOCUS_LAYER);
scene.add(hemisphereLight);
const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
keyLight.position.set(700, 1100, 650);
keyLight.layers.enable(FOCUS_LAYER);
scene.add(keyLight);

const ground = data.world.ground;
const groundMaterial = new THREE.MeshLambertMaterial({ color: data.palette[ground.fill], flatShading: true });
const groundMesh = new THREE.Mesh(new THREE.PlaneGeometry(...ground.size), groundMaterial);
groundMesh.rotation.x = -Math.PI / 2;
groundMesh.position.set(...ground.at);
groundMesh.layers.set(CONTEXT_LAYER);
scene.add(groundMesh);

function setLayerRecursively(object, layer) {
  object.traverse(child => child.layers.set(layer));
}

function material(spec) {
  const opacity = spec.opacity ?? 1;
  const value = new THREE.MeshLambertMaterial({
    color: data.palette[spec.fill],
    flatShading: true,
    opacity,
    transparent: opacity < 1
  });
  value.userData.baseOpacity = opacity;
  return value;
}

function primitiveMesh(spec) {
  let geometry;
  if (spec.shape === "box") {
    geometry = new THREE.BoxGeometry(...spec.size);
  } else if (spec.shape === "cylinder") {
    geometry = new THREE.CylinderGeometry(spec.radius, spec.radius, spec.height, 16);
  } else {
    throw new Error(`Unsupported shape: ${spec.shape}`);
  }
  const mesh = new THREE.Mesh(geometry, material(spec));
  mesh.position.set(...spec.at);
  if (spec.rotate) mesh.rotation.set(...spec.rotate.map(THREE.MathUtils.degToRad));
  mesh.layers.set(CONTEXT_LAYER);
  return mesh;
}

function addPrimitives(parent, primitives, offset = [0, 0, 0]) {
  const materials = [];
  for (const spec of primitives) {
    const mesh = primitiveMesh(spec);
    mesh.position.add(new THREE.Vector3(...offset));
    parent.add(mesh);
    materials.push(mesh.material);
  }
  return materials;
}

for (const structure of data.structures) {
  const group = new THREE.Group();
  scene.add(group);
  if (structure.repeat) {
    for (let i = 0; i < structure.repeat.count; i += 1) {
      addPrimitives(group, structure.primitives, structure.repeat.step.map(value => value * i));
    }
  } else {
    addPrimitives(group, structure.primitives);
  }
}

const nodeObjects = new Map();
for (const node of data.nodes) {
  const group = new THREE.Group();
  group.position.set(...node.position);
  group.userData.materials = addPrimitives(group, node.primitives);
  group.userData.baseVisible = node.base_visible;
  group.visible = node.base_visible;
  scene.add(group);

  const labelElement = document.createElement("div");
  labelElement.className = "node-label";
  labelElement.textContent = node.label;
  if (node.lifecycle) {
    const lifecycle = document.createElement("small");
    lifecycle.textContent = node.lifecycle.replaceAll("_", " ");
    labelElement.appendChild(lifecycle);
  }
  const label = new CSS2DObject(labelElement);
  label.position.set(...node.label_position);
  label.visible = node.base_visible;
  scene.add(label);
  group.userData.labelElement = labelElement;
  group.userData.labelObject = label;
  nodeObjects.set(node.id, group);
}

function segmentedCurve(points) {
  const curve = new THREE.CurvePath();
  for (let i = 1; i < points.length; i += 1) {
    curve.add(new THREE.LineCurve3(new THREE.Vector3(...points[i - 1]), new THREE.Vector3(...points[i])));
  }
  return curve;
}

const edgeObjects = new Map();
for (const edge of data.edges) {
  if (!edge.base_visible) continue;
  const curve = segmentedCurve(edge.points);
  const confirmed = ["energized", "operational_confirmed", "terminal"].includes(edge.lifecycle);
  const baseOpacity = edge.base_visible && confirmed
    ? __HYBRID_CONFIRMED_EDGE_OPACITY__
    : __MIN_HYBRID_FOCUSED_EDGE_OPACITY__;
  const edgeMaterial = new THREE.MeshBasicMaterial({
    color: data.palette[edge.token],
    opacity: baseOpacity,
    transparent: baseOpacity < 1
  });
  edgeMaterial.userData.baseOpacity = baseOpacity;
  const radius = data.stroke.heavy * 0.72;
  const geometry = new THREE.TubeGeometry(curve, Math.max(12, edge.points.length * 10), radius, __EDGE_TUBE_RADIAL_SEGMENTS__, false);
  const mesh = new THREE.Mesh(geometry, edgeMaterial);
  mesh.layers.set(CONTEXT_LAYER);
  scene.add(mesh);
  edgeObjects.set(edge.id, { mesh, curve, token: edge.token });
}

const pulse = new THREE.Mesh(
  new THREE.SphereGeometry(__PULSE_RADIUS__, 14, 14),
  new THREE.MeshBasicMaterial({ color: data.palette.ink })
);
pulse.layers.set(FOCUS_LAYER);
scene.add(pulse);
let activePulseEdges = [];

function setFocus(state) {
  const nodeFocus = new Set(state.focus_nodes || []);
  const labelFocus = new Set(state.label_nodes || []);
  const hasLabelFocus = Array.isArray(state.label_nodes);
  const edgeFocus = new Set(state.focus_edges || []);
  const hasFocus = nodeFocus.size > 0 || edgeFocus.size > 0;
  for (const [id, object] of nodeObjects) {
    const selected = object.userData.baseVisible && (!hasFocus || nodeFocus.has(id));
    setLayerRecursively(object, selected ? FOCUS_LAYER : CONTEXT_LAYER);
    for (const item of object.userData.materials) {
      item.opacity = item.userData.baseOpacity * (selected ? 1 : 0.11);
      item.transparent = item.opacity < 1;
    }
    object.userData.labelObject.visible = selected && (!hasLabelFocus || labelFocus.has(id));
    const [offsetX, offsetY] = state.label_offsets?.[id] || [0, 0];
    object.userData.labelElement.style.marginLeft = `${offsetX}px`;
    object.userData.labelElement.style.marginTop = `${offsetY}px`;
  }
  for (const [id, object] of edgeObjects) {
    const selected = !hasFocus || edgeFocus.has(id);
    object.mesh.layers.set(selected ? FOCUS_LAYER : CONTEXT_LAYER);
    object.mesh.material.opacity = object.mesh.material.userData.baseOpacity * (selected ? 1 : 0.09);
    object.mesh.material.transparent = object.mesh.material.opacity < 1;
  }
  const pulseIds = state.pulse_edges || [...edgeFocus];
  activePulseEdges = pulseIds.map(id => edgeObjects.get(id)).filter(Boolean);
  pulse.visible = activePulseEdges.length > 0;
}

function renderDepthSeparatedFocus() {
  const background = scene.background;
  const autoClear = renderer.autoClear;
  const cameraLayerMask = camera.layers.mask;
  try {
    renderer.autoClear = true;
    camera.layers.set(CONTEXT_LAYER);
    renderer.render(scene, camera);
    renderer.clearDepth();
    scene.background = null;
    renderer.autoClear = false;
    camera.layers.set(FOCUS_LAYER);
    renderer.render(scene, camera);
  } finally {
    scene.background = background;
    renderer.autoClear = autoClear;
    camera.layers.mask = cameraLayerMask;
  }
}

function renderAnnotation(state) {
  const spec = state.annotation;
  if (!spec) {
    annotation.style.display = "none";
    return;
  }
  $("annotation-source").textContent = `master.yaml · node ${spec.node}`;
  const rows = $("annotation-rows");
  rows.replaceChildren();
  for (const item of spec.items) {
    const row = document.createElement("div");
    row.className = "annotation-row";
    const key = document.createElement("span");
    key.className = "annotation-key";
    key.textContent = item.label;
    const value = document.createElement("span");
    value.className = "annotation-value";
    value.textContent = item.value;
    row.append(key, value);
    rows.appendChild(row);
  }
  annotation.style.display = "block";
}

let cameraTween = null;
function moveCamera(state, immediate) {
  const destination = new THREE.Vector3(...state.position);
  const target = new THREE.Vector3(...state.target);
  if (immediate || matchMedia("(prefers-reduced-motion: reduce)").matches) {
    camera.position.copy(destination);
    controls.target.copy(target);
    controls.update();
    cameraTween = null;
    return;
  }
  cameraTween = {
    started: performance.now(),
    duration: 900,
    fromPosition: camera.position.clone(),
    toPosition: destination,
    fromTarget: controls.target.clone(),
    toTarget: target
  };
}

let current = 0;
function activate(index, immediate = false) {
  current = Math.max(0, Math.min(data.cameras.length - 1, index));
  const state = data.cameras[current];
  const is3d = state.mode === "3d";
  mount.style.display = is3d ? "block" : "none";
  mapStage.style.display = is3d ? "none" : "block";
  if (!is3d) {
    mapSvg.setAttribute("viewBox", state.map_view.join(" "));
    mapImage.setAttribute("href", state.map_asset || "master.svg");
  }
  $("state-title").textContent = state.title;
  $("state-subtitle").textContent = state.subtitle || "";
  $("mode").textContent = state.mode;
  renderAnnotation(state);
  if (is3d) {
    setFocus(state);
    moveCamera(state, immediate);
  } else {
    pulse.visible = false;
  }
  document.querySelectorAll(".step").forEach((button, buttonIndex) => {
    if (buttonIndex === current) button.setAttribute("aria-current", "step");
    else button.removeAttribute("aria-current");
  });
  $("previous").disabled = current === 0;
  $("next").disabled = current === data.cameras.length - 1;
}

$("title").textContent = data.meta.title;
const steps = $("steps");
data.cameras.forEach((state, index) => {
  const button = document.createElement("button");
  button.className = "step";
  button.type = "button";
  button.dataset.number = String(index + 1);
  button.textContent = state.title;
  button.addEventListener("click", () => activate(index));
  steps.appendChild(button);
});
$("previous").addEventListener("click", () => activate(current - 1));
$("next").addEventListener("click", () => activate(current + 1));
addEventListener("keydown", event => {
  if (event.key === "ArrowLeft") activate(current - 1);
  if (event.key === "ArrowRight") activate(current + 1);
});

const clockStart = performance.now();
function tick(now) {
  if (cameraTween) {
    const raw = Math.min(1, (now - cameraTween.started) / cameraTween.duration);
    const eased = raw < 0.5 ? 4 * raw * raw * raw : 1 - Math.pow(-2 * raw + 2, 3) / 2;
    camera.position.lerpVectors(cameraTween.fromPosition, cameraTween.toPosition, eased);
    controls.target.lerpVectors(cameraTween.fromTarget, cameraTween.toTarget, eased);
    if (raw === 1) cameraTween = null;
  }
  if (activePulseEdges.length) {
    const phase = ((now - clockStart) / 6000) % 1;
    const scaled = phase * activePulseEdges.length;
    const active = activePulseEdges[Math.min(activePulseEdges.length - 1, Math.floor(scaled))];
    pulse.position.copy(active.curve.getPoint(scaled % 1));
    pulse.material.color.set(data.palette[active.token]);
  }
  controls.update();
  renderDepthSeparatedFocus();
  labelRenderer.render(scene, camera);
  requestAnimationFrame(tick);
}

addEventListener("resize", () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
  labelRenderer.setSize(innerWidth, innerHeight);
});

activate(0, true);
$("loading").remove();
requestAnimationFrame(tick);
</script>
</body>
</html>
"""


def render_html(payload: dict[str, Any]) -> str:
    encoded = canonical_payload(payload).replace("</", "<\\/")
    return (
        HTML.replace("__PAPER__", tokens.PAPER)
        .replace("__INK__", tokens.INK)
        .replace("__FAINT__", tokens.FAINT)
        .replace("__FONT__", tokens.FONT)
        .replace("__EDGE_TUBE_RADIAL_SEGMENTS__", str(EDGE_TUBE_RADIAL_SEGMENTS))
        .replace("__PULSE_RADIUS__", f"{PULSE_RADIUS:g}")
        .replace(
            "__MIN_HYBRID_FOCUSED_EDGE_OPACITY__",
            f"{MIN_HYBRID_FOCUSED_EDGE_OPACITY:g}",
        )
        .replace(
            "__HYBRID_CONFIRMED_EDGE_OPACITY__",
            f"{HYBRID_CONFIRMED_EDGE_OPACITY:g}",
        )
        .replace(
            "__THREE_CAMERA_VERTICAL_FOV_DEGREES__",
            f"{THREE_CAMERA_VERTICAL_FOV_DEGREES:g}",
        )
        .replace("__THREE_CAMERA_NEAR__", f"{THREE_CAMERA_NEAR:g}")
        .replace("__THREE_CAMERA_FAR__", f"{THREE_CAMERA_FAR:g}")
        .replace("__THREE_CAMERA_MIN_DISTANCE__", f"{THREE_CAMERA_MIN_DISTANCE:g}")
        .replace(
            "__THREE_HYBRID_CAMERA_MAX_DISTANCE__",
            f"{THREE_HYBRID_CAMERA_MAX_DISTANCE:g}",
        )
        .replace(
            "__THREE_CAMERA_MIN_POLAR_ANGLE_FRACTION__",
            f"{THREE_CAMERA_MIN_POLAR_ANGLE_FRACTION:g}",
        )
        .replace(
            "__THREE_CAMERA_MAX_POLAR_ANGLE_FRACTION__",
            f"{THREE_CAMERA_MAX_POLAR_ANGLE_FRACTION:g}",
        )
        .replace("__DATA__", encoded)
    )


def generate(
    master_path: Path = DIAGRAM / "master.yaml",
    scene_path: Path = DIAGRAM / "scene.yaml",
    cameras_path: Path = DIAGRAM / "cameras.yaml",
) -> tuple[str, str]:
    payload = build_payload(
        load_yaml(master_path), load_yaml(scene_path), load_yaml(cameras_path)
    )
    html = render_html(payload)
    digest = hashlib.sha256(canonical_payload(payload).encode()).hexdigest()
    return html, digest


def main() -> None:
    html, digest = generate()
    output = DIAGRAM / "hybrid.html"
    output.write_text(html)
    print(f"wrote {output} (source sha256 {digest})")


if __name__ == "__main__":
    main()
