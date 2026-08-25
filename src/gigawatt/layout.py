"""Compose the master diagram from master.yaml + layout.yaml.

Topology and facts live in master.yaml. Placement lives in layout.yaml.
This module is the only thing that draws — no one-off coordinates.

Usage: uv run gigawatt-layout
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml

from . import tokens
from .render import S, journey_bar, lbl, note, place, tower, wire
from .svg import el, line, rect, text

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"

CARRIES_VOLTAGE = {
    "electricity@20kV": "20kV",
    "electricity@345kV": "345kV",
    "electricity@34.5kV": "34.5kV",
    "electricity@480V": "480V",
    "electricity@54VDC": "54V",
    "electricity@0.8V": "0.8V",
}
CARRIES_THERMAL = {
    "heat": "die",
    "heat@liquid": "liquid_hot",
    "heat@air": "air",
    "water": "water",
}


@dataclass
class Geom:
    body: str = ""
    ports: dict[str, tuple[float, float]] = field(default_factory=dict)


def load_yaml(name: str) -> dict:
    return yaml.safe_load((DIAGRAM / name).read_text())


def tone_color(carries: str, tone: str | None) -> str:
    if tone:
        return tokens.VOLTAGE.get(tone) or tokens.THERMAL[tone]
    if carries in CARRIES_VOLTAGE:
        return tokens.VOLTAGE[CARRIES_VOLTAGE[carries]]
    if carries in CARRIES_THERMAL:
        return tokens.THERMAL[CARRIES_THERMAL[carries]]
    return tokens.INK  # shaft power, unlabeled


def _place_symbol(spec: dict, color: str = tokens.INK) -> tuple[str, Geom]:
    x, y = spec["at"]
    body, port = place(spec["symbol"], x, y, s=spec.get("s", 1.0),
                       rot=spec.get("rot", 0), color=color)
    from .symbols import registry
    names = registry()[spec["symbol"]].ports
    return body, Geom(body, {n: port(n) for n in names})


def _place_stack(spec: dict) -> tuple[str, Geom]:
    x, y = spec["at"]
    gap = spec.get("gap", 14)
    parts, ports = [], {}
    prev_out = None
    for i, sid in enumerate(spec["symbols"]):
        body, port = place(sid, x, y)
        parts.append(body)
        if i == 0:
            ports["in"] = port("in")
        if prev_out is not None:
            parts.append(wire(tokens.VOLTAGE["345kV"], prev_out, port("in")))
        prev_out = port("out")
        y += S + gap
    ports["out"] = prev_out
    return "".join(parts), Geom("".join(parts), ports)


def _place_corridor(spec: dict, ground: float) -> tuple[str, Geom]:
    (x0, y0), (x1, y1) = spec["span"]
    parts = [tower(x, ground, spec["top"]) for x in spec["towers"]]
    xs = [x0, *spec["towers"], x1]
    d = f"M {x0:.1f} {y0:.1f}"
    for a, b in zip(xs, xs[1:]):
        mx, my = (a + b) / 2, y0 + 32
        d += f" Q {mx:.1f} {my:.1f} {b:.1f} {y1:.1f}"
    parts.append(el("path", d=d, fill="none", stroke=tokens.VOLTAGE["345kV"],
                    stroke_width=tokens.STROKE_HEAVY, stroke_linecap="round"))
    ports = {"w": (x0, y0), "e": (x1, y1)}
    return "".join(parts), Geom("".join(parts), ports)


def _place_pipe(spec: dict) -> tuple[str, Geom]:
    pts = [tuple(p) for p in spec["pts"]]
    body = wire(tokens.THERMAL["liquid_warm"], *pts)
    ports = {n: tuple(p) for n, p in spec["ports"].items()}
    return body, Geom(body, ports)


def build_geoms(layout: dict, ground: float) -> dict[str, Geom]:
    geoms: dict[str, Geom] = {}
    for nid, spec in layout["nodes"].items():
        kind = spec.get("kind")
        if kind == "stack":
            body, geom = _place_stack(spec)
        elif kind == "corridor":
            body, geom = _place_corridor(spec, ground)
        elif kind == "pipe":
            body, geom = _place_pipe(spec)
        else:
            body, geom = _place_symbol(spec)
        geom.body = el("g", body, id=f"node-{nid}")
        geoms[nid] = geom
    return geoms


def _edge_index(master: dict) -> dict[str, dict]:
    return {f"{e['from']}->{e['to']}": e for e in master["edges"]}


def _pt(nid: str, port: str | None, geom: Geom, override) -> tuple[float, float]:
    if override is not None:
        return tuple(override)
    if port is None:
        raise ValueError(f"{nid}: edge missing port")
    if port not in geom.ports:
        raise KeyError(f"{nid} has no port '{port}' (have {list(geom.ports)})")
    return geom.ports[port]


def build_edges(layout: dict, master: dict, geoms: dict[str, Geom]) -> str:
    facts = _edge_index(master)
    out = []
    for key, spec in layout["edges"].items():
        meta = facts[key]
        color = tone_color(meta["carries"], spec.get("tone"))
        w = tokens.STROKE if spec.get("w") == "thin" else tokens.STROKE_HEAVY
        dash = "5 4" if meta.get("variant") else None
        src, dst = key.split("->")
        a = _pt(src, spec["ports"][0], geoms[src], spec.get("from_at"))
        b = _pt(dst, spec["ports"][1], geoms[dst], spec.get("to_at"))
        via = [tuple(p) for p in spec.get("via") or []]
        out.append(el("g", wire(color, a, *via, b, w=w, dash=dash),
                      id=f"edge-{src}-{dst}"))
    return "".join(out)


def build_site(layout: dict) -> str:
    f = layout["frame"]
    w, ground = f["w"], f["ground"]
    b = [line(40, ground, w - 40, ground, w=2)]
    for z in layout["zones"]:
        b.append(note(z["x"], ground + 28, z["label"]))
    for r in layout["regions"]:
        style = r.get("style", "solid")
        dash = "6 5" if style == "dashed" else None
        sw = 2 if style == "heavy" else tokens.STROKE
        if "rect" in r:
            x, y, rw, rh = r["rect"]
            b.append(rect(x, y, rw, rh, sw=sw, dash=dash))
        if "line" in r:
            (x1, y1), (x2, y2) = r["line"]
            b.append(wire(tokens.FAINT, (x1, y1), (x2, y2), w=tokens.STROKE,
                          dash=dash))
        if "label" in r:
            lx, ly = r["label_at"]
            b.append(lbl(lx, ly, r["label"], size=10))
    for lab in layout.get("room_labels", []):
        b.append(note(*lab["at"], lab["text"]))
    for lab in layout["labels"]:
        kind = lab.get("kind")
        fn = note if kind == "note" else lbl
        kwargs = dict(anchor=lab.get("anchor", "middle"))
        if "size" in lab:
            kwargs["size"] = lab["size"]
        b.append(fn(*lab["at"], lab["text"], **kwargs))
    for g in layout.get("guides", []):
        pts = [tuple(p) for p in g["pts"]]
        b.append(wire(tokens.INK, *pts, w=tokens.STROKE, dash=g.get("dash")))
    return "".join(b)


def _svg(inner: str, w: float, h: float, sid: str) -> str:
    return el("svg", inner, xmlns="http://www.w3.org/2000/svg",
              width=w, height=h, viewBox=f"0 0 {w} {h}", id=sid)


def compose(master: dict, layout: dict) -> tuple[str, str]:
    missing = [n["id"] for n in master["nodes"] if n["id"] not in layout["nodes"]]
    extra = [k for k in layout["nodes"] if k not in {n["id"] for n in master["nodes"]}]
    if missing or extra:
        raise SystemExit(f"layout/master node mismatch: missing={missing} extra={extra}")
    geoms = build_geoms(layout, layout["frame"]["ground"])
    scene = el("g",
               build_site(layout)
               + build_edges(layout, master, geoms)
               + "".join(g.body for g in geoms.values()),
               color=tokens.INK)
    f = layout["frame"]
    hud = (el("rect", x=0, y=0, width=f["w"], height=f["h"], fill=tokens.PAPER)
           + text(40, 42, layout["title"], size=18, anchor="start", weight=700,
                  fill=tokens.INK)
           + note(40, 64, layout["subtitle"], anchor="start")
           + journey_bar(1080, 26))
    return hud + scene, scene


def build_camera(scene: str, cam: dict, frame: dict) -> str:
    """Zoom well over the same scene markup — not a separately drawn chain."""
    w, h = frame["w"], frame["h"]
    vx, vy, vw, vh = cam["viewBox"]
    wx, wy, ww, wh = cam.get("well") or [80, 140, round(vw / vh * 720), 720]
    hud = (
        el("rect", x=0, y=0, width=w, height=h, fill=tokens.PAPER)
        + text(60, 70, cam["title"], size=34, anchor="start", weight=700,
               fill=tokens.INK)
        + text(60, 104, cam.get("subtitle", ""), size=15, anchor="start",
               fill=tokens.INK)
        + journey_bar(1080, 40, active=cam.get("active"))
        + note(60, 1020,
               "camera state of the master diagram — not a separate slide",
               anchor="start")
    )
    well = el("svg", scene, x=wx, y=wy, width=ww, height=wh,
              viewBox=f"{vx} {vy} {vw} {vh}", overflow="hidden")
    return _svg(hud + well, w, h, f"camera-{cam['id']}")


def main() -> None:
    master = load_yaml("master.yaml")
    layout = load_yaml("layout.yaml")
    w, h = layout["frame"]["w"], layout["frame"]["h"]
    hud_scene, scene = compose(master, layout)
    out = DIAGRAM / "master.svg"
    out.write_text(_svg(hud_scene, w, h, "master"))
    print(f"wrote {out}")
    cam_file = DIAGRAM / "cameras.yaml"
    if cam_file.exists():
        for cam in load_yaml("cameras.yaml").get("cameras") or []:
            path = DIAGRAM / f"camera_{cam['id']}.svg"
            path.write_text(build_camera(scene, cam, layout["frame"]))
            print(f"wrote {path}")


if __name__ == "__main__":
    main()
