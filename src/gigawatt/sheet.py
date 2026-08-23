"""Contact sheet: every symbol + all design tokens on one SVG for human redline.

Usage: uv run gigawatt-symbols  ->  writes diagram/symbols.svg
"""

from pathlib import Path

from . import tokens
from .svg import el, line, text
from .symbols import Symbol, registry

CELL_W, CELL_H = 150, 128
COLS = 6
PAD = 36
SCALE = 1.15

ELECTRICAL = ["source_grid", "generator", "turbine_gas", "genset",
              "transformer_2w", "breaker", "disconnect", "bus", "battery_bess",
              "converter_rectifier", "converter_inverter", "converter_dcdc",
              "ups", "die_gpu"]
THERMAL = ["pump", "heat_exchanger", "valve", "cold_plate", "manifold", "cdu",
           "chiller", "fan", "crah", "cooling_tower", "dry_cooler", "tank",
           "atmosphere"]


def _cell(sym: Symbol, x: float, y: float) -> str:
    ox = x + (CELL_W - sym.w * SCALE) / 2
    ports = "".join(
        line(px - 3, py, px + 3, py) + line(px, py - 3, px, py + 3)
        for px, py in sym.ports.values())
    return (
        el("g", sym.body, transform=f"translate({ox},{y}) scale({SCALE})",
           color=tokens.INK)
        + el("g", ports, transform=f"translate({ox},{y}) scale({SCALE})",
             color=tokens.FAINT)
        + text(x + CELL_W / 2, y + sym.h * SCALE + 12, sym.label,
               size=10.5, weight=600, fill=tokens.INK)
        + text(x + CELL_W / 2, y + sym.h * SCALE + 25, sym.standard,
               size=8, fill=tokens.FAINT)
        + text(x + CELL_W / 2, y + sym.h * SCALE + 37, sym.id,
               size=8, fill=tokens.FAINT)
    )


def _section(title: str, ids: list[str], y: float, out: list[str]) -> float:
    syms = registry()
    out.append(text(PAD, y, title.upper(), size=13, anchor="start", weight=700,
                    fill=tokens.INK))
    out.append(line(PAD, y + 10, PAD + COLS * CELL_W, y + 10))
    y += 24
    for i, sid in enumerate(ids):
        cx = PAD + (i % COLS) * CELL_W
        cy = y + (i // COLS) * CELL_H
        out.append(_cell(syms[sid], cx, cy))
    rows = (len(ids) + COLS - 1) // COLS
    return y + rows * CELL_H + 20


def _swatches(y: float, out: list[str]) -> float:
    out.append(text(PAD, y, "TOKENS", size=13, anchor="start", weight=700,
                    fill=tokens.INK))
    out.append(line(PAD, y + 10, PAD + COLS * CELL_W, y + 10))
    y += 30
    x = PAD
    for name, color in {**tokens.VOLTAGE, **tokens.THERMAL}.items():
        out.append(el("rect", x=x, y=y, width=52, height=22, fill=color))
        out.append(text(x + 26, y + 34, name, size=9, fill=tokens.INK))
        x += 64
    y += 58
    out.append(line(PAD, y, PAD + 130, y, w=tokens.STROKE))
    out.append(text(PAD + 150, y, f"standard {tokens.STROKE}", size=9,
                    anchor="start", fill=tokens.INK))
    out.append(line(PAD + 280, y, PAD + 410, y, w=tokens.STROKE_HEAVY))
    out.append(text(PAD + 430, y, f"heavy {tokens.STROKE_HEAVY} (bus / lit path)",
                    size=9, anchor="start", fill=tokens.INK))
    out.append(text(PAD + 620, y, f"type: {tokens.FONT.split(',')[0]}",
                    size=11, anchor="start", fill=tokens.INK))
    return y + 34


def build_sheet() -> str:
    body: list[str] = []
    body.append(text(PAD, 30, "GIGAWATT symbol library — redline sheet v0",
                     size=17, anchor="start", weight=700, fill=tokens.INK))
    body.append(text(PAD, 48, "IEEE 315 / ANSI one-line + simplified P&ID. "
                     "Crosshairs mark connection ports (review aid only).",
                     size=10, anchor="start", fill=tokens.FAINT))
    y = _swatches(78, body)
    y = _section("Electrical — one-line", ELECTRICAL, y, body)
    y = _section("Thermal — P&ID", THERMAL, y, body)
    w = PAD * 2 + COLS * CELL_W
    return el("svg", el("rect", x=0, y=0, width=w, height=y, fill=tokens.PAPER)
              + "".join(body),
              xmlns="http://www.w3.org/2000/svg", width=w, height=y,
              viewBox=f"0 0 {w} {y}")


def main() -> None:
    out = Path(__file__).resolve().parents[2] / "diagram" / "symbols.svg"
    out.write_text(build_sheet())
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
