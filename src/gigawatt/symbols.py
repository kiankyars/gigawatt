"""The GIGAWATT symbol library.

Electrical symbols follow IEEE 315 / ANSI one-line conventions; thermal symbols
follow simplified P&ID (ISA-5.1) conventions. Symbols are generic devices, not
course nodes — master.yaml nodes map onto them (e.g. vrm -> converter_dcdc).

Every symbol lives in a 64x64 local box with named ports on the boundary so the
layout engine can route edges without knowing geometry. Color is applied at
use-time via currentColor (voltage-keyed); fills are flat or none.
"""

from dataclasses import dataclass, field

from . import tokens
from .svg import circle, dc_bars, el, line, path, polygon, rect, sine, text

S = 64  # symbol cell size
M = S / 2  # midline


@dataclass(frozen=True)
class Symbol:
    id: str
    label: str
    standard: str
    body: str
    ports: dict[str, tuple[float, float]] = field(default_factory=dict)
    w: float = S
    h: float = S


_REGISTRY: dict[str, Symbol] = {}


def _sym(id: str, label: str, standard: str, body: str,
         ports: dict[str, tuple[float, float]]) -> Symbol:
    sym = Symbol(id=id, label=label, standard=standard, body=body, ports=ports)
    _REGISTRY[id] = sym
    return sym


# --------------------------------------------------------------------------
# Electrical — IEEE 315 / ANSI one-line
# --------------------------------------------------------------------------

_sym("source_grid", "Utility source", "IEEE 315 (AC source)",
     circle(M, 26, 15) + sine(M, 26, 16) + line(M, 41, M, S),
     ports={"out": (M, S)})

_sym("generator", "Generator", "IEEE 315 (rotating machine, G)",
     circle(M, M, 20) + text(M, M, "G", size=15, weight=600)
     + line(M, 0, M, 12) + line(M, 52, M, S),
     ports={"prime": (M, 0), "out": (M, S)})

_sym("turbine_gas", "Gas turbine", "Power SLD convention (prime mover)",
     polygon([(14, 22), (14, 42), (50, 54), (50, 10)])
     + line(0, M, 14, M) + line(50, M, S, M),
     ports={"fuel": (0, M), "shaft": (S, M)})

_sym("genset", "Engine genset", "IEEE 315 (G + prime mover)",
     rect(6, 22, 26, 20) + text(19, M, "D", size=11, weight=600)
     + line(32, M, 36, M) + circle(46, M, 10) + text(46, M, "G", size=10, weight=600)
     + line(46, 42, 46, S),
     ports={"out": (46, S)})

_sym("transformer_2w", "Transformer, 2-winding", "IEEE 315 (winding humps)",
     line(M, 0, M, 20)
     + path("M 14 26 A 6 6 0 0 1 26 26 A 6 6 0 0 1 38 26 A 6 6 0 0 1 50 26")
     + path("M 14 38 A 6 6 0 0 0 26 38 A 6 6 0 0 0 38 38 A 6 6 0 0 0 50 38")
     + line(M, 44, M, S),
     ports={"h": (M, 0), "x": (M, S)})

_sym("breaker", "Circuit breaker", "ANSI one-line (drawout square)",
     line(M, 0, M, 20) + rect(20, 20, 24, 24) + line(M, 44, M, S),
     ports={"in": (M, 0), "out": (M, S)})

_sym("disconnect", "Disconnect switch", "IEEE 315 (knife switch)",
     line(M, 0, M, 22) + circle(M, 24, 2) + line(M, 24, 47, 43)
     + circle(M, 44, 2) + line(M, 46, M, S),
     ports={"in": (M, 0), "out": (M, S)})

_sym("bus", "Bus", "One-line convention (heavy bar)",
     line(4, M, 60, M, w=tokens.STROKE_HEAVY),
     ports={"l": (0, M), "r": (S, M), "t": (M, 0), "b": (M, S)})

_sym("battery_bess", "BESS", "IEEE 315 battery, enclosed",
     rect(10, 10, 44, 44, dash="4 3")
     + line(M, 0, M, 22)
     + line(20, 26, 44, 26) + line(26, 31, 38, 31, w=tokens.STROKE_HEAVY)
     + line(20, 37, 44, 37) + line(26, 42, 38, 42, w=tokens.STROKE_HEAVY)
     + line(M, 42, M, S),
     ports={"dc": (M, 0), "out": (M, S)})

_sym("converter_rectifier", "Rectifier (AC-DC)", "IEC 617 converter box",
     line(0, M, 12, M) + rect(12, 18, 40, 28) + line(12, 46, 52, 18)
     + sine(22, 25, 10) + dc_bars(42, 39, 10) + line(52, M, S, M),
     ports={"ac": (0, M), "dc": (S, M)})

_sym("converter_inverter", "Inverter (DC-AC)", "IEC 617 converter box",
     line(0, M, 12, M) + rect(12, 18, 40, 28) + line(12, 46, 52, 18)
     + dc_bars(22, 25, 10) + sine(42, 39, 10) + line(52, M, S, M),
     ports={"dc": (0, M), "ac": (S, M)})

_sym("converter_dcdc", "DC-DC converter", "IEC 617 converter box",
     line(0, M, 12, M) + rect(12, 18, 40, 28) + line(12, 46, 52, 18)
     + dc_bars(22, 25, 10) + dc_bars(42, 39, 10) + line(52, M, S, M),
     ports={"in": (0, M), "out": (S, M)})

_sym("ups", "UPS, double conversion", "Rectifier + inverter, enclosed",
     rect(4, 14, 56, 36)
     + rect(9, 21, 20, 22) + line(9, 43, 29, 21) + sine(15, 26, 8) + dc_bars(24, 38, 8)
     + line(29, 32, 35, 32)
     + rect(35, 21, 20, 22) + line(35, 43, 55, 21) + dc_bars(41, 26, 8) + sine(50, 38, 8)
     + line(0, 32, 4, 32) + line(60, 32, S, 32),
     ports={"in": (0, 32), "out": (S, 32)})

_sym("die_gpu", "GPU die", "Custom (package + die)",
     rect(16, 16, 32, 32)
     + rect(26, 26, 12, 12, fill="currentColor", sw=0)
     + line(M, 0, M, 16)
     + "".join(line(48, y, 54, y) for y in (22, 32, 42))
     + "".join(line(10, y, 16, y) for y in (22, 32, 42))
     + line(M, 48, M, S),
     ports={"power": (M, 0), "heat": (M, S)})

# --------------------------------------------------------------------------
# Thermal — simplified P&ID (ISA-5.1)
# --------------------------------------------------------------------------

_sym("pump", "Pump", "ISA-5.1 (centrifugal)",
     circle(M, M, 18) + polygon([(24, 22), (24, 42), (48, 32)])
     + line(0, M, 14, M) + line(50, M, S, M),
     ports={"suction": (0, M), "discharge": (S, M)})

_sym("heat_exchanger", "Heat exchanger", "ISA-5.1 (shell and tube, simplified)",
     circle(M, M, 18)
     + path("M 14 32 L 21 24 L 29 40 L 37 24 L 45 40 L 50 32")
     + line(0, M, 14, M) + line(50, M, S, M)
     + line(M, 0, M, 14) + line(M, 50, M, S),
     ports={"a_in": (0, M), "a_out": (S, M), "b_in": (M, 0), "b_out": (M, S)})

_sym("valve", "Valve", "ISA-5.1 (gate)",
     polygon([(20, 24), (20, 40), (32, 32)]) + polygon([(44, 24), (44, 40), (32, 32)])
     + line(0, M, 20, M) + line(44, M, S, M),
     ports={"in": (0, M), "out": (S, M)})

_sym("cold_plate", "Cold plate", "Custom (serpentine channel)",
     rect(10, 20, 44, 24)
     + path("M 10 26 H 46 M 46 26 V 32 H 18 M 18 32 V 38 H 54")
     + line(0, 26, 10, 26) + line(54, 38, S, 38) + line(M, 44, M, S),
     ports={"liquid_in": (0, 26), "liquid_out": (S, 38), "heat": (M, S)})

_sym("manifold", "Manifold", "Custom (header bar + taps)",
     rect(27, 6, 8, 52, fill="currentColor", sw=0)
     + "".join(line(35, y, 54, y) for y in (14, 28, 42, 56))
     + line(0, 10, 27, 10),
     ports={"main": (0, 10), "t1": (S, 14), "t2": (S, 28), "t3": (S, 42), "t4": (S, 56)})

_sym("cdu", "CDU", "Package unit (HX + pump)",
     rect(4, 10, 56, 44)
     + circle(24, 32, 11) + path("M 15 32 L 20 26 L 26 38 L 32 28")
     + circle(45, 32, 8) + polygon([(41, 27), (41, 37), (52, 32)])
     + line(0, 22, 4, 22) + line(0, 42, 4, 42)
     + line(60, 22, S, 22) + line(60, 42, S, 42),
     ports={"tech_in": (S, 22), "tech_out": (S, 42),
            "fac_in": (0, 22), "fac_out": (0, 42)})

_sym("chiller", "Chiller", "Package unit (evap / cond circuits)",
     rect(4, 14, 56, 36)
     + circle(21, 32, 9) + circle(43, 32, 9)
     + line(28, 26, 36, 26) + line(28, 38, 36, 38)
     + line(0, 32, 4, 32) + line(60, 32, S, 32),
     ports={"evap": (0, 32), "cond": (S, 32)})

_sym("fan", "Fan", "ISA-5.1 (axial)",
     circle(M, M, 14)
     + path(f"M {M} 18 Q 40 26 {M} {M} Q 24 38 {M} 46"),
     ports={"in": (M, S), "out": (M, 0)})

_sym("crah", "CRAH / fan wall", "Package unit (coil + fan)",
     rect(8, 10, 48, 44)
     + path("M 12 20 L 20 14 L 28 26 L 36 14 L 44 26 L 52 20")
     + circle(32, 42, 9) + path("M 32 34 Q 37 39 32 42 Q 27 45 32 50")
     + line(0, 32, 8, 32) + line(56, 32, S, 32),
     ports={"liquid_in": (0, 32), "liquid_out": (S, 32), "air": (M, 0)})

_sym("cooling_tower", "Cooling tower", "P&ID convention (cell + fan)",
     polygon([(14, 56), (50, 56), (44, 22), (20, 22)])
     + circle(M, 14, 8) + path(f"M {M} 8 Q 36 11 {M} 14 Q 28 17 {M} 20")
     + "".join(line(19 + i, y, 45 - i, y) for i, y in ((0, 50), (1, 44), (2, 38)))
     + line(0, 34, 17, 34) + line(M, 56, M, S),
     ports={"water_in": (0, 34), "water_out": (M, S), "air_out": (M, 0)})

_sym("dry_cooler", "Dry cooler", "P&ID convention (coil + fans)",
     rect(6, 22, 52, 26)
     + circle(21, 35, 8) + path("M 21 28 Q 26 32 21 35 Q 16 38 21 42")
     + circle(43, 35, 8) + path("M 43 28 Q 48 32 43 35 Q 38 38 43 42")
     + line(0, 35, 6, 35) + line(58, 35, S, 35),
     ports={"liquid_in": (0, 35), "liquid_out": (S, 35), "air_out": (M, 0)})

_sym("tank", "Tank (makeup water)", "P&ID convention (vessel)",
     path("M 20 20 A 12 5 0 0 1 44 20 L 44 48 A 12 5 0 0 1 20 48 Z")
     + el("ellipse", cx=32, cy=20, rx=12, ry=5, fill="none",
          stroke="currentColor", stroke_width=tokens.STROKE)
     + line(M, 53, M, S),
     ports={"out": (M, S)})

_sym("atmosphere", "Atmosphere", "Custom (terminal sink)",
     path("M 14 46 Q 23 38 32 46 Q 41 54 50 46")
     + path("M 14 32 Q 23 24 32 32 Q 41 40 50 32")
     + path("M 14 18 Q 23 10 32 18 Q 41 26 50 18")
     + line(M, 54, M, S),
     ports={"in": (M, S)})


def registry() -> dict[str, Symbol]:
    return dict(_REGISTRY)
