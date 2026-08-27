"""Build the instructor-controlled native pilot for s10.

The pilot manifest owns only coarse transformations. The course manifest owns
the segment scope, while the master and scene manifests continue to own
semantics and placement.

Usage: uv run python diagram/generate_s10_two_rack_heat_paths.py
"""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from gigawatt.scene import build_payload, canonical_payload, load_yaml

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "course" / "segments.yaml"
MANIFEST = ROOT / "course" / "pilots" / "s10_two_rack_heat_paths.yaml"
MASTER = ROOT / "diagram" / "master.yaml"
SCENE = ROOT / "diagram" / "scene.yaml"
CAMERAS = ROOT / "diagram" / "cameras.yaml"
OUTPUT = ROOT / "diagram" / "s10_two_rack_heat_paths.html"

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
PILOT_LABEL_POSITIONS = {
    "rack_air_load": [640, 88, -42],
    "rack_manifold": [650, 150, 46],
}


class PilotError(ValueError):
    """Raised when the pilot drifts beyond its canonical course scope."""


def _segment(course: dict[str, Any], segment_id: str) -> dict[str, Any]:
    matches = [
        segment
        for act in course.get("acts") or []
        for segment in act.get("segments") or []
        if segment.get("id") == segment_id
    ]
    if len(matches) != 1:
        raise PilotError(
            f"course/segments.yaml: expected one segment {segment_id!r}, "
            f"found {len(matches)}"
        )
    return matches[0]


def _id_list(value: Any, location: str) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise PilotError(f"{location}: expected a list of IDs")
    if len(value) != len(set(value)):
        raise PilotError(f"{location}: IDs must be unique")
    return value


def validate_manifest(
    manifest: dict[str, Any],
    course: dict[str, Any],
    master: dict[str, Any],
    scene: dict[str, Any],
    cameras: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    """Validate the manual transformations against every canonical owner."""
    actual_top_level = set(manifest)
    if actual_top_level != TOP_LEVEL_FIELDS:
        raise PilotError(
            "pilot manifest top-level fields must be exact: "
            f"missing={sorted(TOP_LEVEL_FIELDS - actual_top_level)} "
            f"extra={sorted(actual_top_level - TOP_LEVEL_FIELDS)}"
        )
    if manifest["schema_version"] != 1:
        raise PilotError("pilot manifest schema_version must be 1")
    if not isinstance(manifest["purpose"], str) or not manifest["purpose"].strip():
        raise PilotError("pilot manifest purpose must be non-empty")

    segment = _segment(course, manifest["segment_id"])
    if manifest["camera_anchor"] != segment.get("camera", {}).get("anchor"):
        raise PilotError(
            "pilot camera_anchor must equal the canonical segment camera anchor"
        )

    camera_matches = [
        camera
        for camera in cameras.get("cameras") or []
        if camera.get("id") == manifest["camera_anchor"]
    ]
    if len(camera_matches) != 1 or camera_matches[0].get("mode") != "3d":
        raise PilotError("pilot camera_anchor must resolve to one 3D camera")
    camera = camera_matches[0]

    canonical_nodes = set(_id_list(segment.get("node_ids"), "canonical node_ids"))
    canonical_edges = set(_id_list(segment.get("edge_ids"), "canonical edge_ids"))
    master_nodes = {node["id"]: node for node in master.get("nodes") or []}
    master_edges = {
        edge.get("id") or f"{edge['from']}->{edge['to']}": edge
        for edge in master.get("edges") or []
    }
    scene_nodes = set((scene.get("nodes") or {}).keys())
    scene_edges = set((scene.get("edges") or {}).keys())

    if not canonical_nodes or not canonical_edges:
        raise PilotError("canonical s10 node and edge scopes must be non-empty")
    missing_nodes = sorted(canonical_nodes - set(master_nodes) | canonical_nodes - scene_nodes)
    missing_edges = sorted(canonical_edges - set(master_edges) | canonical_edges - scene_edges)
    if missing_nodes or missing_edges:
        raise PilotError(
            f"canonical s10 scope is absent from master/scene: "
            f"nodes={missing_nodes} edges={missing_edges}"
        )
    hidden_nodes = sorted(
        node_id
        for node_id in canonical_nodes
        if master_nodes[node_id].get("base_visible", True) is False
    )
    hidden_edges = sorted(
        edge_id
        for edge_id in canonical_edges
        if master_edges[edge_id].get("base_visible", True) is False
    )
    if hidden_nodes or hidden_edges:
        raise PilotError(
            f"s10 pilot cannot bypass hidden items: nodes={hidden_nodes} "
            f"edges={hidden_edges}"
        )

    transformations = manifest["transformations"]
    if not isinstance(transformations, list) or not transformations:
        raise PilotError("pilot transformations must be a non-empty list")
    ids = [item.get("id") for item in transformations if isinstance(item, dict)]
    if len(ids) != len(transformations) or any(
        not isinstance(item, str) or not item for item in ids
    ):
        raise PilotError("every transformation must have a non-empty ID")
    if len(ids) != len(set(ids)):
        raise PilotError("transformation IDs must be unique")

    covered_nodes: set[str] = set()
    covered_edges: set[str] = set()
    for index, transformation in enumerate(transformations):
        location = f"transformations[{index}]"
        actual_fields = set(transformation)
        if actual_fields != TRANSFORMATION_FIELDS:
            raise PilotError(
                f"{location} fields must be exact: "
                f"missing={sorted(TRANSFORMATION_FIELDS - actual_fields)} "
                f"extra={sorted(actual_fields - TRANSFORMATION_FIELDS)}"
            )
        for field in ("title", "instruction"):
            if not isinstance(transformation[field], str) or not transformation[field].strip():
                raise PilotError(f"{location}.{field}: expected non-empty text")
        focus_nodes = set(_id_list(transformation["focus_nodes"], f"{location}.focus_nodes"))
        focus_edges = set(_id_list(transformation["focus_edges"], f"{location}.focus_edges"))
        pulse_edges = set(_id_list(transformation["pulse_edges"], f"{location}.pulse_edges"))
        outside_nodes = sorted(focus_nodes - canonical_nodes)
        outside_edges = sorted(focus_edges - canonical_edges)
        outside_pulses = sorted(pulse_edges - focus_edges)
        scoped_focus_edges = focus_edges & canonical_edges
        unfocused_endpoints = sorted(
            {
                endpoint
                for edge_id in scoped_focus_edges
                for endpoint in (
                    master_edges[edge_id]["from"],
                    master_edges[edge_id]["to"],
                )
            }
            - focus_nodes
        )
        if outside_nodes or outside_edges or outside_pulses or unfocused_endpoints:
            raise PilotError(
                f"{location} escapes canonical s10 scope: nodes={outside_nodes} "
                f"edges={outside_edges} pulse_not_focused={outside_pulses} "
                f"unfocused_endpoints={unfocused_endpoints}"
            )
        if not focus_nodes and not focus_edges:
            raise PilotError(f"{location}: a transformation cannot be empty")
        covered_nodes.update(focus_nodes)
        covered_edges.update(focus_edges)

    if covered_nodes != canonical_nodes or covered_edges != canonical_edges:
        raise PilotError(
            "transformations must cover the exact canonical s10 scope: "
            f"missing_nodes={sorted(canonical_nodes - covered_nodes)} "
            f"extra_nodes={sorted(covered_nodes - canonical_nodes)} "
            f"missing_edges={sorted(canonical_edges - covered_edges)} "
            f"extra_edges={sorted(covered_edges - canonical_edges)}"
        )

    return segment, camera


def _source_digest() -> str:
    digest = hashlib.sha256()
    for path in (COURSE, MANIFEST, MASTER, SCENE, CAMERAS):
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def build() -> tuple[str, str, int]:
    course = load_yaml(COURSE)
    manifest = load_yaml(MANIFEST)
    master = load_yaml(MASTER)
    scene = load_yaml(SCENE)
    cameras = load_yaml(CAMERAS)
    segment, camera = validate_manifest(manifest, course, master, scene, cameras)

    shared = build_payload(master, scene, cameras)
    assertions = sorted(
        {
            claim["assertion"]
            for claim in segment.get("evidence", {}).get("claims") or []
        }
    )
    digest = _source_digest()
    payload = {
        "meta": {
            "title": segment["title"],
            "segment_id": segment["id"],
            "purpose": manifest["purpose"],
            "camera_anchor": manifest["camera_anchor"],
            "evidence_readiness": segment["evidence"]["readiness"],
            "assertions": assertions,
            "promotion_guards": segment["evidence"]["promotion_guards"],
            "source_digest": digest,
        },
        "palette": shared["palette"],
        "font": shared["font"],
        "stroke": shared["stroke"],
        "world": shared["world"],
        "structures": shared["structures"],
        "nodes": shared["nodes"],
        "edges": shared["edges"],
        "camera": camera,
        "label_positions": PILOT_LABEL_POSITIONS,
        "transformations": manifest["transformations"],
    }
    rendered = (
        HTML.replace("__DATA__", canonical_payload(payload))
        .replace("__PAPER__", shared["palette"]["paper"])
        .replace("__INK__", shared["palette"]["ink"])
        .replace("__FAINT__", shared["palette"]["faint"])
        .replace("__MUTED__", shared["palette"]["muted"])
        .replace("__FONT__", shared["font"])
        .replace("__DIGEST__", digest)
        .replace("__SUPPLY__", shared["palette"]["thermal:technology_supply"])
        .replace("__RETURN__", shared["palette"]["thermal:technology_return"])
        .replace("__HEAT__", shared["palette"]["thermal:die_heat"])
        .replace("__AIR__", shared["palette"]["thermal:air"])
    )
    return rendered, digest, len(manifest["transformations"])


HTML = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="gigawatt-source-digest" content="__DIGEST__">
<title>GIGAWATT — s10 native comparison pilot</title>
<style>
  :root {
    --paper: __PAPER__;
    --ink: __INK__;
    --faint: __FAINT__;
    --muted: __MUTED__;
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
  #app, #three-mount { position: absolute; inset: 0; }
  #three-mount canvas { display: block; width: 100%; height: 100%; }
  #labels { position: absolute; inset: 0; pointer-events: none; }
  #masthead {
    position: absolute;
    z-index: 8;
    top: 0;
    right: 0;
    left: 0;
    min-height: 112px;
    padding: 20px 28px 16px;
    display: grid;
    grid-template-columns: minmax(0, 1fr) auto;
    gap: 24px;
    background: color-mix(in srgb, var(--paper) 95%, transparent);
    border-bottom: var(--rule) solid var(--ink);
  }
  #eyebrow, #evidence-boundary {
    margin: 0;
    color: var(--muted);
    font-size: 9px;
    font-weight: 700;
    letter-spacing: .09em;
    text-transform: uppercase;
  }
  #title { margin: 5px 0 0; font-size: 20px; line-height: 1.1; }
  #transformation-title { margin: 6px 0 0; font-size: 13px; line-height: 1.2; }
  #instruction {
    margin: 3px 0 0;
    max-width: 820px;
    font-size: 11px;
    line-height: 1.35;
  }
  #evidence {
    align-self: start;
    max-width: 330px;
    padding: 10px 12px;
    border: var(--rule) solid var(--ink);
    background: var(--paper);
  }
  #evidence-posture { margin: 4px 0 0; font-size: 10px; line-height: 1.35; }
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
  #legend {
    position: absolute;
    z-index: 7;
    top: 132px;
    right: 28px;
    min-width: 196px;
    padding: 11px 13px;
    background: color-mix(in srgb, var(--paper) 93%, transparent);
    border: 1px solid var(--ink);
    font-size: 9px;
  }
  .legend-row { display: flex; gap: 8px; align-items: center; margin: 5px 0; }
  .swatch { width: 22px; height: 4px; background: var(--color); }
  #scope {
    position: absolute;
    z-index: 7;
    left: 28px;
    bottom: 88px;
    margin: 0;
    padding: 7px 9px;
    color: var(--muted);
    background: color-mix(in srgb, var(--paper) 91%, transparent);
    border: 1px solid var(--faint);
    font-size: 9px;
  }
  #transport {
    position: absolute;
    z-index: 9;
    right: 0;
    bottom: 0;
    left: 0;
    min-height: 72px;
    padding: 12px 18px;
    display: grid;
    grid-template-columns: auto minmax(0, 1fr) auto;
    gap: 12px;
    align-items: center;
    background: color-mix(in srgb, var(--paper) 95%, transparent);
    border-top: var(--rule) solid var(--ink);
  }
  .arrow {
    width: 42px;
    height: 36px;
    border: var(--rule) solid var(--ink);
    background: transparent;
    cursor: pointer;
  }
  .arrow:disabled { color: var(--faint); border-color: var(--faint); cursor: default; }
  #steps { display: flex; justify-content: center; gap: 6px; min-width: 0; }
  .step {
    width: min(190px, 20vw);
    min-width: 42px;
    height: 38px;
    overflow: hidden;
    padding: 0 10px;
    border: 0;
    border-bottom: 3px solid var(--faint);
    background: transparent;
    text-overflow: ellipsis;
    white-space: nowrap;
    font-size: 10px;
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
  @media (max-width: 760px) {
    #masthead { min-height: 126px; padding: 15px 16px 12px; grid-template-columns: 1fr; gap: 8px; }
    #evidence { display: none; }
    #legend { top: 138px; right: 12px; }
    #scope { left: 12px; }
    #transport { padding-inline: 8px; gap: 5px; }
    .step { width: 34px; padding: 0; color: transparent; }
    .step::after { content: attr(data-number); color: var(--ink); }
  }
</style>
</head>
<body>
<main id="app" aria-label="Instructor-controlled comparison of two rack cooling paths">
  <section id="three-mount" aria-label="Three-dimensional rack cooling comparison"></section>
  <header id="masthead">
    <div>
      <p id="eyebrow"></p>
      <h1 id="title"></h1>
      <p id="transformation-title"></p>
      <p id="instruction"></p>
    </div>
    <aside id="evidence">
      <p id="evidence-boundary">Evidence boundary</p>
      <p id="evidence-posture"></p>
    </aside>
  </header>
  <aside id="legend" aria-label="Carrier legend">
    <div class="legend-row"><span class="swatch" style="--color: __SUPPLY__"></span>Technology supply</div>
    <div class="legend-row"><span class="swatch" style="--color: __RETURN__"></span>Technology return</div>
    <div class="legend-row"><span class="swatch" style="--color: __HEAT__"></span>Die heat</div>
    <div class="legend-row"><span class="swatch" style="--color: __AIR__"></span>Air-cooled auxiliaries</div>
  </aside>
  <p id="scope">Canonical s10 scope · 4 nodes · 3 edges · air branch stops at the rack package</p>
  <nav id="transport" aria-label="Manual pilot transformations">
    <button class="arrow" id="previous" type="button" aria-label="Previous transformation">←</button>
    <div id="steps"></div>
    <button class="arrow" id="next" type="button" aria-label="Next transformation">→</button>
  </nav>
  <div id="loading">Loading the native pilot…</div>
</main>
<script id="pilot-data" type="application/json">__DATA__</script>
<script type="importmap">
{"imports":{"three":"https://unpkg.com/three@0.170.0/build/three.module.js","three/addons/":"https://unpkg.com/three@0.170.0/examples/jsm/"}}
</script>
<script type="module">
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { CSS2DRenderer, CSS2DObject } from "three/addons/renderers/CSS2DRenderer.js";

const data = JSON.parse(document.getElementById("pilot-data").textContent);
const $ = id => document.getElementById(id);
const mount = $("three-mount");
const scene = new THREE.Scene();
scene.background = new THREE.Color(data.palette.paper);
scene.fog = new THREE.Fog(data.palette.paper, data.world.fog.near, data.world.fog.far);

const camera = new THREE.PerspectiveCamera(40, innerWidth / innerHeight, 1, 5000);
camera.position.set(...data.camera.position);
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
controls.target.set(...data.camera.target);
controls.minDistance = 90;
controls.maxDistance = 1600;
controls.maxPolarAngle = Math.PI * 0.49;
controls.update();

scene.add(new THREE.HemisphereLight(0xffffff, 0xd8d8cf, 1.45));
const keyLight = new THREE.DirectionalLight(0xffffff, 1.5);
keyLight.position.set(700, 1100, 650);
scene.add(keyLight);

function material(spec, context = false) {
  const opacity = context ? Math.min(spec.opacity ?? 1, 0.2) : (spec.opacity ?? 1);
  const value = new THREE.MeshLambertMaterial({
    color: data.palette[spec.fill],
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

const ground = data.world.ground;
const groundMaterial = material({ fill: ground.fill, opacity: 0.2 }, true);
const groundMesh = new THREE.Mesh(new THREE.PlaneGeometry(...ground.size), groundMaterial);
groundMesh.rotation.x = -Math.PI / 2;
groundMesh.position.set(...ground.at);
scene.add(groundMesh);

for (const structure of data.structures) {
  const group = new THREE.Group();
  scene.add(group);
  if (structure.repeat) {
    for (let i = 0; i < structure.repeat.count; i += 1) {
      addPrimitives(group, structure.primitives, structure.repeat.step.map(value => value * i), true);
    }
  } else {
    addPrimitives(group, structure.primitives, [0, 0, 0], true);
  }
}

const nodeObjects = new Map();
for (const node of data.nodes) {
  if (!node.base_visible) continue;
  const group = new THREE.Group();
  group.position.set(...node.position);
  group.userData.materials = addPrimitives(group, node.primitives);
  scene.add(group);

  const element = document.createElement("div");
  element.className = "node-label";
  element.textContent = node.label;
  const label = new CSS2DObject(element);
  label.position.set(...(data.label_positions[node.id] || node.label_position));
  label.visible = false;
  scene.add(label);
  group.userData.label = label;
  group.userData.labelElement = element;
  nodeObjects.set(node.id, group);
}

function segmentedCurve(points) {
  const curve = new THREE.CurvePath();
  for (let index = 1; index < points.length; index += 1) {
    curve.add(new THREE.LineCurve3(new THREE.Vector3(...points[index - 1]), new THREE.Vector3(...points[index])));
  }
  return curve;
}

const edgeObjects = new Map();
for (const edge of data.edges) {
  if (!edge.base_visible) continue;
  const curve = segmentedCurve(edge.points);
  const edgeMaterial = new THREE.MeshBasicMaterial({
    color: data.palette[edge.token],
    opacity: 0.035,
    transparent: true
  });
  const mesh = new THREE.Mesh(
    new THREE.TubeGeometry(curve, Math.max(12, edge.points.length * 10), data.stroke.heavy * 0.72, 8, false),
    edgeMaterial
  );
  scene.add(mesh);

  const marker = new THREE.Mesh(
    new THREE.ConeGeometry(5.2, 14, 10),
    new THREE.MeshBasicMaterial({ color: data.palette[edge.token] })
  );
  const markerPosition = curve.getPoint(0.64);
  const markerDirection = curve.getTangent(0.64).normalize();
  marker.position.copy(markerPosition);
  marker.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), markerDirection);
  marker.visible = false;
  scene.add(marker);
  edgeObjects.set(edge.id, { mesh, marker });
}

function render() {
  renderer.render(scene, camera);
  labelRenderer.render(scene, camera);
}

let current = 0;
function activate(index) {
  current = Math.max(0, Math.min(data.transformations.length - 1, index));
  const transformation = data.transformations[current];
  const focusNodes = new Set(transformation.focus_nodes);
  const focusEdges = new Set(transformation.focus_edges);
  const pulseEdges = new Set(transformation.pulse_edges);

  for (const [id, object] of nodeObjects) {
    const selected = focusNodes.has(id);
    for (const item of object.userData.materials) {
      item.opacity = item.userData.baseOpacity * (selected ? 1 : 0.008);
      item.transparent = item.opacity < 1;
      item.needsUpdate = true;
    }
    object.userData.label.visible = selected;
    const [offsetX, offsetY] = data.camera.label_offsets?.[id] || [0, 0];
    object.userData.labelElement.style.marginLeft = `${offsetX}px`;
    object.userData.labelElement.style.marginTop = `${offsetY}px`;
  }
  for (const [id, object] of edgeObjects) {
    object.mesh.material.opacity = focusEdges.has(id) ? 0.96 : 0.006;
    object.marker.visible = pulseEdges.has(id);
  }

  $("transformation-title").textContent = transformation.title;
  $("instruction").textContent = transformation.instruction;
  document.querySelectorAll(".step").forEach((button, buttonIndex) => {
    if (buttonIndex === current) button.setAttribute("aria-current", "step");
    else button.removeAttribute("aria-current");
  });
  $("previous").disabled = current === 0;
  $("next").disabled = current === data.transformations.length - 1;
  render();
}

$("eyebrow").textContent = `${data.meta.segment_id} · native comparison pilot · manual control`;
$("title").textContent = data.meta.title;
$("evidence-posture").textContent = `${data.meta.assertions.map(value => value.replaceAll("_", " ")).join(" + ")} · not an as-built claim`;

const steps = $("steps");
data.transformations.forEach((transformation, index) => {
  const button = document.createElement("button");
  button.className = "step";
  button.type = "button";
  button.dataset.number = String(index + 1);
  button.textContent = transformation.title;
  button.addEventListener("click", () => activate(index));
  steps.appendChild(button);
});
$("previous").addEventListener("click", () => activate(current - 1));
$("next").addEventListener("click", () => activate(current + 1));
addEventListener("keydown", event => {
  if (event.key === "ArrowLeft") activate(current - 1);
  if (event.key === "ArrowRight") activate(current + 1);
});
controls.addEventListener("change", render);
addEventListener("resize", () => {
  camera.aspect = innerWidth / innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(innerWidth, innerHeight);
  labelRenderer.setSize(innerWidth, innerHeight);
  render();
});

activate(0);
$("loading").remove();
</script>
</body>
</html>
'''


def main() -> None:
    rendered, digest, transformation_count = build()
    OUTPUT.write_text(rendered)
    print(
        f"built {OUTPUT.relative_to(ROOT)} · {transformation_count} transformations "
        f"· digest {digest}"
    )


if __name__ == "__main__":
    main()
