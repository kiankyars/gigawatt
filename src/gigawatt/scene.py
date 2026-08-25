"""Build the master-ID-driven hybrid 2D/3D teaching substrate.

`master.yaml` owns topology and facts. `scene.yaml` owns spatial placement,
`cameras.yaml` owns views, and this module only validates and compiles them into
one deterministic browser player.

Usage: uv run python -m gigawatt.scene
"""

from __future__ import annotations

import hashlib
import json
import re
from copy import deepcopy
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml

from . import tokens

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
ALLOWED_MODES = {"2d", "3d", "overlay"}
ALLOWED_SHAPES = {"box", "cylinder"}


class ManifestError(ValueError):
    """Raised when a scene or camera reference drifts from the master."""


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text())
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


def _triplet(value: Any, location: str) -> None:
    if not (
        isinstance(value, list)
        and len(value) == 3
        and all(isinstance(v, (int, float)) for v in value)
    ):
        raise ManifestError(f"{location}: expected three numeric coordinates")


def _validate_primitives(
    primitives: Any, location: str, token_names: set[str]
) -> None:
    if not isinstance(primitives, list) or not primitives:
        raise ManifestError(f"{location}: primitives must be a non-empty list")
    for index, primitive in enumerate(primitives):
        here = f"{location}.primitives[{index}]"
        if not isinstance(primitive, dict):
            raise ManifestError(f"{here}: expected a mapping")
        shape = primitive.get("shape")
        if shape not in ALLOWED_SHAPES:
            raise ManifestError(f"{here}: unsupported shape {shape!r}")
        _triplet(primitive.get("at"), f"{here}.at")
        if shape == "box":
            _triplet(primitive.get("size"), f"{here}.size")
        else:
            if not isinstance(primitive.get("radius"), (int, float)):
                raise ManifestError(f"{here}.radius: expected a number")
            if not isinstance(primitive.get("height"), (int, float)):
                raise ManifestError(f"{here}.height: expected a number")
        if primitive.get("fill") not in token_names:
            raise ManifestError(
                f"{here}.fill: unknown shared token {primitive.get('fill')!r}"
            )
        if "rotate" in primitive:
            _triplet(primitive["rotate"], f"{here}.rotate")


def validate(
    master: dict[str, Any], scene: dict[str, Any], cameras: dict[str, Any]
) -> None:
    """Fail closed on drift between semantic, spatial, and camera manifests."""
    master_nodes = {node["id"] for node in master.get("nodes") or []}
    master_edge_records = {
        edge_key(edge): edge for edge in master.get("edges") or []
    }
    master_edges = set(master_edge_records)
    hidden_master_edges = {
        key
        for key, edge in master_edge_records.items()
        if edge.get("base_visible", True) is False
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

    token_names = set(palette())
    ground = scene.get("world", {}).get("ground") or {}
    if ground.get("fill") not in token_names:
        raise ManifestError("scene.world.ground.fill must reference a shared token")
    if not (
        isinstance(ground.get("size"), list)
        and len(ground["size"]) == 2
        and all(isinstance(v, (int, float)) for v in ground["size"])
    ):
        raise ManifestError("scene.world.ground.size: expected two numeric values")
    _triplet(ground.get("at"), "scene.world.ground.at")

    for node_id, spec in (scene.get("nodes") or {}).items():
        _triplet(spec.get("at"), f"scene.nodes.{node_id}.at")
        _triplet(spec.get("label_at"), f"scene.nodes.{node_id}.label_at")
        _validate_primitives(spec.get("primitives"), f"scene.nodes.{node_id}", token_names)

    for structure in scene.get("structures") or []:
        sid = structure.get("id", "<unknown>")
        _validate_primitives(
            structure.get("primitives"), f"scene.structures.{sid}", token_names
        )
        if repeat := structure.get("repeat"):
            if not isinstance(repeat.get("count"), int) or repeat["count"] < 1:
                raise ManifestError(f"scene.structures.{sid}.repeat.count: invalid")
            _triplet(repeat.get("step"), f"scene.structures.{sid}.repeat.step")

    for key, spec in (scene.get("edges") or {}).items():
        points = spec.get("points")
        if not isinstance(points, list) or len(points) < 2:
            raise ManifestError(f"scene.edges.{key}.points: expected at least two points")
        for index, point in enumerate(points):
            _triplet(point, f"scene.edges.{key}.points[{index}]")
        if "tone" in spec and spec["tone"] not in token_names:
            raise ManifestError(f"scene.edges.{key}.tone: unknown shared token")

    camera_list = cameras.get("cameras") or []
    camera_ids = [camera.get("id") for camera in camera_list]
    if not camera_ids or len(camera_ids) != len(set(camera_ids)):
        raise ManifestError("cameras.yaml: camera IDs must be present and unique")
    for camera in camera_list:
        cid = camera["id"]
        mode = camera.get("mode")
        if mode not in ALLOWED_MODES:
            raise ManifestError(f"camera {cid}: unsupported mode {mode!r}")
        focus_nodes = set(camera.get("focus_nodes") or [])
        unknown_nodes = sorted(focus_nodes - master_nodes)
        label_nodes_value = camera.get("label_nodes")
        if label_nodes_value is not None and not (
            isinstance(label_nodes_value, list)
            and all(isinstance(node_id, str) for node_id in label_nodes_value)
        ):
            raise ManifestError(f"camera {cid}: label_nodes must be a list of node IDs")
        label_nodes = set(label_nodes_value or [])
        unknown_label_nodes = sorted(label_nodes - master_nodes)
        nonfocus_label_nodes = sorted(label_nodes - focus_nodes)
        camera_edges = set(camera.get("focus_edges") or []) | set(
            camera.get("pulse_edges") or []
        )
        unknown_edges = sorted(camera_edges - master_edges)
        hidden_camera_edges = sorted(camera_edges & hidden_master_edges)
        if (
            unknown_nodes
            or unknown_label_nodes
            or nonfocus_label_nodes
            or unknown_edges
            or hidden_camera_edges
        ):
            raise ManifestError(
                f"camera {cid}: unknown_nodes={unknown_nodes} "
                f"unknown_label_nodes={unknown_label_nodes} "
                f"nonfocus_label_nodes={nonfocus_label_nodes} "
                f"unknown_edges={unknown_edges} hidden_edges={hidden_camera_edges}"
            )
        if mode == "3d":
            _triplet(camera.get("position"), f"camera {cid}.position")
            _triplet(camera.get("target"), f"camera {cid}.target")
        else:
            view = camera.get("map_view")
            if not (
                isinstance(view, list)
                and len(view) == 4
                and all(isinstance(v, (int, float)) for v in view)
            ):
                raise ManifestError(f"camera {cid}.map_view: expected four numbers")
        if annotation := camera.get("annotation"):
            if annotation.get("node") not in master_nodes:
                raise ManifestError(f"camera {cid}: annotation node is not in master")
            if not isinstance(annotation.get("fields"), list):
                raise ManifestError(f"camera {cid}: annotation fields must be a list")

    sequence = cameras.get("vertical_slice") or []
    if sequence != camera_ids:
        raise ManifestError(
            "cameras.yaml: vertical_slice must enumerate camera states in file order"
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

    return json.dumps(
        payload,
        default=serialise,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )


HTML = r'''<!doctype html>
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
    max-width: 190px;
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
{"imports":{"three":"https://unpkg.com/three@0.170.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.170.0/examples/jsm/"}}
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
scene.background = new THREE.Color(data.palette.paper);
scene.fog = new THREE.Fog(data.palette.paper, data.world.fog.near, data.world.fog.far);

const camera = new THREE.PerspectiveCamera(40, innerWidth / innerHeight, 1, 5000);
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
controls.maxPolarAngle = Math.PI * 0.49;
controls.minDistance = 90;
controls.maxDistance = 3200;
const initial3d = data.cameras.find(state => state.mode === "3d");
if (initial3d) {
  camera.position.set(...initial3d.position);
  controls.target.set(...initial3d.target);
  controls.update();
}

scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d8cf, 1.45));
const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
keyLight.position.set(700, 1100, 650);
scene.add(keyLight);

const ground = data.world.ground;
const groundMaterial = new THREE.MeshLambertMaterial({ color: data.palette[ground.fill], flatShading: true });
const groundMesh = new THREE.Mesh(new THREE.PlaneGeometry(...ground.size), groundMaterial);
groundMesh.rotation.x = -Math.PI / 2;
groundMesh.position.set(...ground.at);
scene.add(groundMesh);

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
  const baseOpacity = edge.base_visible && confirmed ? 0.96 : 0.42;
  const edgeMaterial = new THREE.MeshBasicMaterial({
    color: data.palette[edge.token],
    opacity: baseOpacity,
    transparent: baseOpacity < 1
  });
  edgeMaterial.userData.baseOpacity = baseOpacity;
  const radius = data.stroke.heavy * 0.72;
  const geometry = new THREE.TubeGeometry(curve, Math.max(12, edge.points.length * 10), radius, 8, false);
  const mesh = new THREE.Mesh(geometry, edgeMaterial);
  scene.add(mesh);
  edgeObjects.set(edge.id, { mesh, curve, token: edge.token });
}

const pulse = new THREE.Mesh(
  new THREE.SphereGeometry(6.2, 14, 14),
  new THREE.MeshBasicMaterial({ color: data.palette.ink })
);
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
    for (const item of object.userData.materials) {
      item.opacity = item.userData.baseOpacity * (selected ? 1 : 0.11);
      item.transparent = item.opacity < 1;
    }
    object.userData.labelObject.visible = selected && (!hasLabelFocus || labelFocus.has(id));
  }
  for (const [id, object] of edgeObjects) {
    const selected = !hasFocus || edgeFocus.has(id);
    object.mesh.material.opacity = object.mesh.material.userData.baseOpacity * (selected ? 1 : 0.09);
    object.mesh.material.transparent = object.mesh.material.opacity < 1;
  }
  const pulseIds = state.pulse_edges || [...edgeFocus];
  activePulseEdges = pulseIds.map(id => edgeObjects.get(id)).filter(Boolean);
  pulse.visible = activePulseEdges.length > 0;
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
  renderer.render(scene, camera);
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
'''


def render_html(payload: dict[str, Any]) -> str:
    encoded = canonical_payload(payload).replace("</", "<\\/")
    return (
        HTML.replace("__PAPER__", tokens.PAPER)
        .replace("__INK__", tokens.INK)
        .replace("__FAINT__", tokens.FAINT)
        .replace("__FONT__", tokens.FONT)
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
