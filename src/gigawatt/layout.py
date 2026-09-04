"""Compose the evidence-gated 2D master from semantic and placement manifests.

`master.yaml` owns topology and copy templates, `evidence/abilene.yaml` owns
facts and sources, and `layout.yaml` owns geometry. A rendered fact must resolve
through that chain; placement cannot carry prose or numbers.

Usage: uv run gigawatt-layout
"""

from __future__ import annotations

from dataclasses import dataclass, field
from itertools import pairwise
from pathlib import Path
from string import Formatter
from typing import Any

import yaml

from . import tokens
from .render import S, journey_bar, lbl, note, place, tower, wire
from .svg import el, line, text

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"

CARRIES_TONE = {
    "electricity@138kV": ("voltage", "138kV"),
    "electricity@345kV": ("voltage", "345kV"),
    "electricity@generator_terminal_mv": ("voltage", "generator_terminal_mv"),
    "electricity@campus_mv": ("voltage", "campus_mv"),
    "electricity@facility_lv_ac": ("voltage", "facility_lv_ac"),
    "electricity@rack_ac": ("voltage", "rack_ac"),
    "electricity@rack_dc": ("voltage", "rack_dc"),
    "electricity@core_voltage": ("voltage", "core_voltage"),
    "heat@solid": ("thermal", "die_heat"),
    "heat@technology_return": ("thermal", "technology_return"),
    "coolant@technology_supply": ("thermal", "technology_supply"),
    "heat@facility_return": ("thermal", "facility_return"),
    "coolant@facility_supply": ("thermal", "facility_supply"),
    "heat@air": ("thermal", "air"),
    "water@fill": ("thermal", "water"),
}

LIFECYCLE_STYLE = {
    "energized": (None, 1.0),
    "operational_confirmed": (None, 1.0),
    "terminal": (None, 1.0),
    "permitted": ("1 6", 0.92),
    "future_design": ("9 6", 0.82),
    "conceptual": ("7 6", 0.50),
    "course_variant": ("4 6", 0.42),
}


class DiagramError(ValueError):
    """Raised when semantic, evidence, or placement manifests drift."""


@dataclass
class Geom:
    body: str = ""
    ports: dict[str, tuple[float, float]] = field(default_factory=dict)


def load_yaml(path: Path) -> dict[str, Any]:
    data = yaml.safe_load(path.read_text())
    if not isinstance(data, dict):
        raise DiagramError(f"{path}: expected a mapping")
    return data


def tone_color(carries: str, explicit: str | None = None) -> str:
    if explicit:
        if explicit in tokens.VOLTAGE:
            return tokens.VOLTAGE[explicit]
        if explicit in tokens.THERMAL:
            return tokens.THERMAL[explicit]
        raise DiagramError(f"unknown explicit tone {explicit!r}")
    family_key = CARRIES_TONE.get(carries)
    if not family_key:
        return tokens.INK
    family, key = family_key
    return (tokens.VOLTAGE if family == "voltage" else tokens.THERMAL)[key]


def _fact_display(record: dict[str, Any]) -> str:
    value = record.get("value")
    if value is None:
        return "unverified"
    if isinstance(value, bool):
        return "yes" if value else "no"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def resolve_copy(
    master: dict[str, Any],
    evidence: dict[str, Any],
    copy_id: str,
    *,
    include_hidden: bool = False,
) -> str | None:
    try:
        spec = master["copy"][copy_id]
    except KeyError as exc:
        raise DiagramError(f"unknown copy ID {copy_id!r}") from exc
    if spec.get("base_visible", True) is False and not include_hidden:
        return None
    if "text" in spec:
        return str(spec["text"])
    template = spec.get("template")
    fact_ids = spec.get("facts") or []
    if not template or not fact_ids:
        raise DiagramError(f"copy {copy_id}: expected text or template + facts")
    placeholders = {name for _, name, _, _ in Formatter().parse(template) if name}
    if placeholders - set(fact_ids):
        raise DiagramError(
            f"copy {copy_id}: undeclared placeholders {sorted(placeholders - set(fact_ids))}"
        )
    facts = evidence.get("facts") or {}
    values: dict[str, str] = {}
    for fact_id in fact_ids:
        if fact_id not in facts:
            raise DiagramError(f"copy {copy_id}: missing fact {fact_id!r}")
        record = facts[fact_id]
        if record.get("value") is None and spec.get("posture") != "explicit_unknown":
            raise DiagramError(
                f"copy {copy_id}: unresolved fact {fact_id!r} is not an explicit unknown"
            )
        values[fact_id] = _fact_display(record)
    return template.format(**values)


def _place_symbol(spec: dict[str, Any], color: str = tokens.INK) -> tuple[str, Geom]:
    x, y = spec["at"]
    body, port = place(
        spec["symbol"], x, y, s=spec.get("s", 1.0), rot=spec.get("rot", 0), color=color
    )
    from .symbols import registry

    names = registry()[spec["symbol"]].ports
    return body, Geom(body, {name: port(name) for name in names})


def _place_stack(spec: dict[str, Any]) -> tuple[str, Geom]:
    x, y = spec["at"]
    gap = spec.get("gap", 14)
    color = tone_color(f"electricity@{spec.get('tone', '345kV')}")
    parts, ports = [], {}
    previous_out = None
    for index, symbol_id in enumerate(spec["symbols"]):
        body, port = place(symbol_id, x, y, color=color)
        parts.append(body)
        if index == 0:
            ports["in"] = port("in")
        if previous_out is not None:
            parts.append(wire(color, previous_out, port("in")))
        previous_out = port("out")
        y += S + gap
    ports["out"] = previous_out
    joined = "".join(parts)
    return joined, Geom(joined, ports)


def _place_corridor(spec: dict[str, Any], ground: float) -> tuple[str, Geom]:
    (x0, y0), (x1, y1) = spec["span"]
    color = tokens.VOLTAGE[spec.get("tone", "345kV")]
    parts = [tower(x, spec.get("ground", ground), spec["top"]) for x in spec["towers"]]
    points = [x0, *spec["towers"], x1]
    path_data = f"M {x0:.1f} {y0:.1f}"
    for left, right in pairwise(points):
        path_data += f" Q {(left + right) / 2:.1f} {y0 + 24:.1f} {right:.1f} {y1:.1f}"
    parts.append(
        el(
            "path",
            d=path_data,
            fill="none",
            stroke=color,
            stroke_width=tokens.STROKE_HEAVY,
            stroke_linecap="round",
        )
    )
    joined = "".join(parts)
    return joined, Geom(joined, {"w": (x0, y0), "e": (x1, y1)})


def _place_line_node(spec: dict[str, Any]) -> tuple[str, Geom]:
    points = [tuple(point) for point in spec["pts"]]
    body = wire(tokens.VOLTAGE[spec["tone"]], *points)
    return body, Geom(body, {name: tuple(point) for name, point in spec["ports"].items()})


def _place_dual_pipe(spec: dict[str, Any]) -> tuple[str, Geom]:
    supply = [tuple(point) for point in spec["supply_pts"]]
    returning = [tuple(point) for point in spec["return_pts"]]
    body = (
        wire(tokens.THERMAL["facility_supply"], *supply, w=tokens.STROKE)
        + wire(tokens.THERMAL["facility_return"], *returning, w=tokens.STROKE_HEAVY)
    )
    return body, Geom(body, {name: tuple(point) for name, point in spec["ports"].items()})


def _lifecycle_attrs(lifecycle: str, base_visible: bool = True) -> dict[str, Any]:
    dash, opacity = LIFECYCLE_STYLE.get(lifecycle, (None, 1.0))
    attrs: dict[str, Any] = {"data_lifecycle": lifecycle, "opacity": opacity}
    if dash:
        attrs["stroke_dasharray"] = dash
    if not base_visible:
        attrs["display"] = "none"
    return attrs


def build_geoms(layout: dict[str, Any], master: dict[str, Any], ground: float) -> dict[str, Geom]:
    node_meta = {node["id"]: node for node in master["nodes"]}
    geoms: dict[str, Geom] = {}
    for node_id, spec in layout["nodes"].items():
        kind = spec.get("kind")
        if kind == "stack":
            body, geom = _place_stack(spec)
        elif kind == "corridor":
            body, geom = _place_corridor(spec, ground)
        elif kind == "line_node":
            body, geom = _place_line_node(spec)
        elif kind == "dual_pipe":
            body, geom = _place_dual_pipe(spec)
        else:
            body, geom = _place_symbol(spec)
        meta = node_meta[node_id]
        geom.body = el(
            "g",
            body,
            id=f"node-{node_id}",
            data_presence=meta["presence"],
            **_lifecycle_attrs(meta["lifecycle"], meta.get("base_visible", True)),
        )
        geoms[node_id] = geom
    return geoms


def _edge_index(master: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {edge["id"]: edge for edge in master["edges"]}


def _pt(node_id: str, port: str | None, geom: Geom, override: Any) -> tuple[float, float]:
    if override is not None:
        return tuple(override)
    if port is None:
        raise DiagramError(f"{node_id}: edge missing port")
    if port not in geom.ports:
        raise DiagramError(f"{node_id}: unknown port {port!r}; have {sorted(geom.ports)}")
    return geom.ports[port]


def build_edges(layout: dict[str, Any], master: dict[str, Any], geoms: dict[str, Geom]) -> str:
    edge_meta = _edge_index(master)
    out = []
    for edge_id, spec in layout["edges"].items():
        meta = edge_meta[edge_id]
        source, target = meta["from"], meta["to"]
        a = _pt(source, spec["ports"][0], geoms[source], spec.get("from_at"))
        b = _pt(target, spec["ports"][1], geoms[target], spec.get("to_at"))
        via = [tuple(point) for point in spec.get("via") or []]
        width = tokens.STROKE if spec.get("w") == "thin" else tokens.STROKE_HEAVY
        dash, _ = LIFECYCLE_STYLE.get(meta["lifecycle"], (None, 1.0))
        body = wire(tone_color(meta["carries"], spec.get("tone")), a, *via, b, w=width, dash=dash)
        out.append(
            el(
                "g",
                body,
                id=f"edge-{edge_id}",
                data_from=source,
                data_to=target,
                data_presence=meta["presence"],
                data_lifecycle=meta["lifecycle"],
                data_normal_state=meta["normal_state"],
                data_flow_direction=meta["flow_direction"],
                opacity=LIFECYCLE_STYLE.get(meta["lifecycle"], (None, 1.0))[1],
                display="none" if meta.get("base_visible", True) is False else "inline",
            )
        )
    return "".join(out)


def _render_copy(
    master: dict[str, Any], evidence: dict[str, Any], spec: dict[str, Any],
    *, default_kind: str = "label"
) -> str:
    copy_id = spec["id"]
    rendered = resolve_copy(master, evidence, copy_id, include_hidden=True)
    if rendered is None:
        return ""
    fn = note if spec.get("kind", default_kind) == "note" else lbl
    kwargs: dict[str, Any] = {"anchor": spec.get("anchor", "middle")}
    if "size" in spec:
        kwargs["size"] = spec["size"]
    return el(
        "g",
        fn(*spec["at"], rendered, **kwargs),
        id=f"label-{copy_id}",
        display="none"
        if master["copy"][copy_id].get("base_visible", True) is False
        else "inline",
    )


def _legend(layout: dict[str, Any], master: dict[str, Any], evidence: dict[str, Any]) -> str:
    spec = layout.get("legend")
    if not spec:
        return ""
    x, y = spec["at"]
    parts = [
        el(
            "g",
            lbl(x, y, resolve_copy(master, evidence, spec["title_id"]) or "", anchor="start"),
            id=f"label-{spec['title_id']}",
        )
    ]
    for index, entry in enumerate(spec["entries"]):
        line_y = y + 24 + index * 22
        dash, opacity = LIFECYCLE_STYLE[entry["lifecycle"]]
        parts.append(
            el("g", wire(tokens.INK, (x, line_y), (x + 42, line_y), w=2, dash=dash), opacity=opacity)
        )
        label_spec = {"id": entry["id"], "at": [x + 54, line_y], "kind": "note", "anchor": "start", "size": 10.5}
        parts.append(_render_copy(master, evidence, label_spec))
    return el("g", "".join(parts), id="status-legend")


def build_site(
    layout: dict[str, Any], master: dict[str, Any], evidence: dict[str, Any], layer: str
) -> str:
    if layer not in {"background", "annotations"}:
        raise DiagramError(f"unknown site layer {layer!r}")
    frame = layout["frame"]
    width, ground = frame["w"], frame["ground"]
    body = [line(40, ground, width - 40, ground, w=2)] if layer == "background" else []
    if layer == "annotations":
        for zone in layout["zones"]:
            rendered = resolve_copy(master, evidence, zone["copy_id"])
            body.append(
                el(
                    "g",
                    note(zone["x"], ground + 28, rendered or "", size=10.5),
                    id=f"label-{zone['copy_id']}",
                )
            )
    for region in layout["regions"]:
        style = region.get("style", "evidence")
        dash = "7 6" if style == "conceptual" else None
        color = tokens.FAINT_GUIDE if style == "conceptual" else tokens.INK
        if layer == "background" and "rect" in region:
            x, y, region_width, region_height = region["rect"]
            body.append(
                el(
                    "rect",
                    x=x,
                    y=y,
                    width=region_width,
                    height=region_height,
                    fill="none",
                    stroke=color,
                    stroke_width=2 if style == "evidence" else tokens.STROKE,
                    stroke_dasharray=dash or "none",
                )
            )
        if layer == "background" and "line" in region:
            (x1, y1), (x2, y2) = region["line"]
            body.append(wire(color, (x1, y1), (x2, y2), w=tokens.STROKE, dash=dash))
        if layer == "annotations" and "copy_id" in region:
            copy_id = region["copy_id"]
            rendered = resolve_copy(master, evidence, copy_id)
            body.append(
                el(
                    "g",
                    lbl(*region["label_at"], rendered or "", size=11),
                    id=f"label-{copy_id}",
                )
            )
    if layer == "annotations":
        for room in layout.get("room_labels", []):
            body.append(_render_copy(master, evidence, room, default_kind="note"))
        for label_spec in layout["labels"]:
            body.append(_render_copy(master, evidence, label_spec))
        body.append(_legend(layout, master, evidence))
    else:
        for guide in layout.get("guides", []):
            points = [tuple(point) for point in guide["pts"]]
            body.append(wire(tokens.INK, *points, w=tokens.STROKE, dash=guide.get("dash")))
    return "".join(body)


def _svg(inner: str, width: float, height: float, svg_id: str) -> str:
    return el(
        "svg",
        inner,
        xmlns="http://www.w3.org/2000/svg",
        width=width,
        height=height,
        viewBox=f"0 0 {width} {height}",
        id=svg_id,
    )


def _assert_coverage(master: dict[str, Any], layout: dict[str, Any]) -> None:
    master_nodes = {node["id"] for node in master["nodes"]}
    layout_nodes = set(layout["nodes"])
    master_edges = {edge["id"] for edge in master["edges"]}
    layout_edges = set(layout["edges"])
    if master_nodes != layout_nodes or master_edges != layout_edges:
        raise DiagramError(
            "layout/master coverage mismatch: "
            f"missing_nodes={sorted(master_nodes - layout_nodes)} "
            f"extra_nodes={sorted(layout_nodes - master_nodes)} "
            f"missing_edges={sorted(master_edges - layout_edges)} "
            f"extra_edges={sorted(layout_edges - master_edges)}"
        )


def compose(
    master: dict[str, Any], layout: dict[str, Any], evidence: dict[str, Any]
) -> tuple[str, str]:
    _assert_coverage(master, layout)
    geoms = build_geoms(layout, master, layout["frame"]["ground"])
    scene = el(
        "g",
        build_site(layout, master, evidence, "background")
        + build_edges(layout, master, geoms)
        + "".join(geom.body for geom in geoms.values())
        + build_site(layout, master, evidence, "annotations"),
        color=tokens.INK,
        id="master-scene",
    )
    frame = layout["frame"]
    title_copy = resolve_copy(master, evidence, layout["title_id"]) or ""
    subtitle_copy = resolve_copy(master, evidence, layout["subtitle_id"]) or ""
    hud = (
        el("rect", x=0, y=0, width=frame["w"], height=frame["h"], fill=tokens.PAPER)
        + el(
            "g",
            text(40, 42, title_copy, size=18, anchor="start", weight=700, fill=tokens.INK),
            id=f"label-{layout['title_id']}",
        )
        + el(
            "g",
            note(40, 64, subtitle_copy, size=10.5, anchor="start"),
            id=f"label-{layout['subtitle_id']}",
        )
        + journey_bar(1040, 26, journey=master["meta"]["journey_bar"])
    )
    return hud + scene, scene


def main() -> None:
    master = load_yaml(DIAGRAM / "master.yaml")
    layout = load_yaml(DIAGRAM / "layout.yaml")
    evidence_path = ROOT / master["meta"]["evidence_file"]
    evidence = load_yaml(evidence_path)
    frame = layout["frame"]
    hud_scene, _scene = compose(master, layout, evidence)
    output = DIAGRAM / "master.svg"
    output.write_text(_svg(hud_scene, frame["w"], frame["h"], "master"))
    print(f"wrote {output}")


if __name__ == "__main__":
    main()
