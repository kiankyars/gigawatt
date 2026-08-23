"""Minimal SVG string builders. No drawing library — the diagram is composed."""

from . import tokens


def el(tag: str, body: str | None = None, **attrs: object) -> str:
    rendered = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in attrs.items())
    if body is None:
        return f"<{tag} {rendered}/>"
    return f"<{tag} {rendered}>{body}</{tag}>"


def line(x1: float, y1: float, x2: float, y2: float, w: float = tokens.STROKE) -> str:
    return el("line", x1=x1, y1=y1, x2=x2, y2=y2,
              stroke="currentColor", stroke_width=w, stroke_linecap="round")


def circle(cx: float, cy: float, r: float, fill: str = "none",
           w: float = tokens.STROKE) -> str:
    return el("circle", cx=cx, cy=cy, r=r, fill=fill,
              stroke="currentColor", stroke_width=w)


def rect(x: float, y: float, w: float, h: float, fill: str = "none",
         sw: float = tokens.STROKE, dash: str | None = None) -> str:
    attrs: dict[str, object] = dict(x=x, y=y, width=w, height=h, fill=fill,
                                    stroke="currentColor", stroke_width=sw)
    if dash:
        attrs["stroke_dasharray"] = dash
    return el("rect", **attrs)


def path(d: str, fill: str = "none", w: float = tokens.STROKE) -> str:
    return el("path", d=d, fill=fill, stroke="currentColor",
              stroke_width=w, stroke_linecap="round", stroke_linejoin="round")


def polygon(points: list[tuple[float, float]], fill: str = "none",
            w: float = tokens.STROKE) -> str:
    pts = " ".join(f"{x},{y}" for x, y in points)
    return el("polygon", points=pts, fill=fill, stroke="currentColor",
              stroke_width=w, stroke_linejoin="round")


def text(x: float, y: float, s: str, size: float = tokens.FONT_SIZE,
         anchor: str = "middle", weight: int = 400, fill: str = "currentColor") -> str:
    s = s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return el("text", s, x=x, y=y, font_family=tokens.FONT, font_size=size,
              font_weight=weight, text_anchor=anchor,
              dominant_baseline="central", fill=fill)


def sine(cx: float, cy: float, w: float) -> str:
    """AC tilde glyph, drawn (not typeset) so it scales with the symbol."""
    h = w / 3
    return path(f"M {cx - w / 2} {cy} Q {cx - w / 4} {cy - h} {cx} {cy} "
                f"Q {cx + w / 4} {cy + h} {cx + w / 2} {cy}")


def dc_bars(cx: float, cy: float, w: float) -> str:
    """DC glyph: solid bar over dashed bar."""
    solid = line(cx - w / 2, cy - 2.5, cx + w / 2, cy - 2.5)
    dashed = el("line", x1=cx - w / 2, y1=cy + 2.5, x2=cx + w / 2, y2=cy + 2.5,
                stroke="currentColor", stroke_width=tokens.STROKE,
                stroke_dasharray="3 2.5")
    return solid + dashed
