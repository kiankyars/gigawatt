"""Shared frame-drawing helpers: symbol placement, wiring, labels, journey bar."""

import math

from . import tokens
from .svg import el, line, text
from .symbols import registry

S = 64
SYMS = registry()


def place(sid: str, x: float, y: float, s: float = 1.0, rot: float = 0,
          color: str = tokens.INK):
    """Place a symbol; returns (svg, port) where port(name) -> abs coords."""
    sym = SYMS[sid]
    tf = f"translate({x},{y}) scale({s})"
    if rot:
        tf += f" rotate({rot},{S / 2},{S / 2})"
    body = el("g", sym.body, transform=tf, color=color)

    def port(name: str) -> tuple[float, float]:
        px, py = sym.ports[name]
        if rot:
            a = math.radians(rot)
            cx = cy = S / 2
            px, py = (cx + (px - cx) * math.cos(a) - (py - cy) * math.sin(a),
                      cy + (px - cx) * math.sin(a) + (py - cy) * math.cos(a))
        return (x + px * s, y + py * s)

    return body, port


def wire(color: str, *pts: tuple[float, float], w: float = tokens.STROKE_HEAVY,
         dash: str | None = None) -> str:
    d = "M " + " L ".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    attrs: dict[str, object] = dict(d=d, fill="none", stroke=color,
                                    stroke_width=w, stroke_linecap="round",
                                    stroke_linejoin="round")
    if dash:
        attrs["stroke_dasharray"] = dash
    return el("path", **attrs)


def lbl(x: float, y: float, s: str, size: float = 12.5, weight: int = 600,
        fill: str = tokens.INK, anchor: str = "middle") -> str:
    return text(x, y, s, size=size, weight=weight, fill=fill, anchor=anchor)


def note(x: float, y: float, s: str, size: float = 10.5,
         anchor: str = "middle") -> str:
    return text(x, y, s, size=size, fill=tokens.MUTED_TEXT, anchor=anchor)


def journey_bar(x: float, y: float, journey: dict | None = None,
                active: str | None = None) -> str:
    """Render the ordered carrier/state journey declared by the master."""
    out: list[str] = []
    journey = journey or {
        "electrical": ["source_branches", "campus_mv", "facility_lv_ac", "rack_dc", "core_voltage"],
        "thermal": ["die_heat", "technology_return", "facility_return", "atmosphere"],
    }
    sw, gap = 72, 6
    for name in journey["electrical"]:
        color = tokens.VOLTAGE[name]
        dim = active is not None and name != active
        out.append(el("rect", x=x, y=y, width=sw, height=16, fill=color,
                      fill_opacity=0.22 if dim else 1.0))
        out.append(text(x + sw / 2, y + 29, tokens.JOURNEY_LABEL[name], size=8.5,
                        fill=tokens.MUTED_TEXT if dim else tokens.INK))
        x += sw + gap
    x += 14
    for name in journey["thermal"]:
        color = tokens.THERMAL[name]
        dim = active is not None and name != active
        out.append(el("rect", x=x, y=y, width=sw * 0.7, height=16, fill=color,
                      fill_opacity=0.22 if dim else 1.0))
        out.append(text(x + sw * 0.35, y + 29, tokens.JOURNEY_LABEL[name], size=8.5,
                        fill=tokens.MUTED_TEXT if dim else tokens.INK))
        x += sw * 0.7 + gap
    return "".join(out)


def tower(x: float, ground: float, top: float) -> str:
    """Minimal lattice transmission tower glyph."""
    arm = 26
    return (line(x, ground, x, top)
            + line(x - arm, top, x + arm, top)
            + line(x - arm * 0.6, top + 24, x + arm * 0.6, top + 24)
            + line(x - 10, ground, x, ground - 40) + line(x + 10, ground, x, ground - 40)
            + line(x - arm, top, x - arm, top + 8)
            + line(x + arm, top, x + arm, top + 8))
