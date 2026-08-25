"""Style mocks — NOT the layout engine.

Two 16:9 frames to judge the visual direction of the master diagram:

  mock_wide.svg  — the full cutaway: one representative watt path from gas
                   turbine to atmosphere, symbols embedded in a site
                   cross-section. This is the "home" view the camera lives in.
  mock_zoom.svg  — one camera state (the electrical room segment), i.e. what
                   a viewer actually sees for most of the course.

Coordinates are hand-placed; the real layout engine will derive them from
master.yaml. Usage: uv run gigawatt-mock
"""

from pathlib import Path

from . import tokens
from .render import SYMS, S, journey_bar, lbl, note, place, tower, wire
from .svg import el, line, text

W, H = 1920, 1080


# The retired v0 mocks retain their original copy, but their palette aliases
# stay local so unsupported voltage claims cannot leak into the v1 manifests.
V = {
    "20kV": tokens.VOLTAGE["generator_terminal_mv"],
    "345kV": tokens.VOLTAGE["345kV"],
    "34.5kV": tokens.VOLTAGE["campus_mv"],
    "480V": tokens.VOLTAGE["facility_lv_ac"],
    "54V": tokens.VOLTAGE["rack_dc"],
    "0.8V": tokens.VOLTAGE["core_voltage"],
}
T = {
    "die": tokens.THERMAL["die_heat"],
    "liquid_hot": tokens.THERMAL["technology_return"],
    "liquid_warm": tokens.THERMAL["facility_return"],
    "air": tokens.THERMAL["air"],
}
GROUND = 830


def build_wide() -> str:
    b: list[str] = []  # symbols + wires
    b.append(text(40, 42, "GIGAWATT — master cutaway, mock v0",
                  size=21, anchor="start", weight=700, fill=tokens.INK))
    b.append(note(40, 64, "style test, not layout-final · one representative "
                  "path; multiplicity is annotated, never drawn", anchor="start"))
    b.append(journey_bar(1080, 26))

    # ground + zones
    b.append(line(40, GROUND, 1880, GROUND, w=2))
    for x, s in ((190, "GENERATION YARD (BTM)"), (480, "345 kV CORRIDOR"),
                 (730, "CAMPUS SUBSTATION"), (900, "MV YARD"),
                 (1360, "DATA HALL BUILDING  ×8")):
        b.append(note(x, 858, s))

    # --- generation: fuel -> turbine -> generator -> GSU ---
    tb, tp = place("turbine_gas", 80, 700)
    gn, gp = place("generator", 170, 706)
    gsu, gsup = place("gsu" if "gsu" in SYMS else "transformer_2w", 262, 664)
    b += [tb, gn, gsu]
    b.append(wire(tokens.INK, (44, tp("fuel")[1]), tp("fuel"), w=tokens.STROKE))
    b.append(note(48, tp("fuel")[1] - 12, "natural gas", anchor="start"))
    sx, sy = tp("shaft")
    px, py = gp("prime")
    b.append(wire(tokens.INK, (sx, sy), (sx + 8, sy), (sx + 8, py - 14),
                  (px, py - 14), (px, py), w=tokens.STROKE, dash="5 4"))
    ox, oy = gp("out")
    hx, hy = gsup("x")
    b.append(wire(V["20kV"], (ox, oy), (ox, oy + 24), (hx, oy + 24), (hx, hy)))
    b.append(lbl(112, 790, "gas turbine ×10", size=10))
    b.append(note(112, 804, "360.5 MW · TCEQ 177263"))
    b.append(lbl(202, 795, "generator", size=10))
    b.append(lbl(294, 754, "GSU", size=10))

    # --- 345 kV corridor: GSU up to catenary, two towers, into substation ---
    tx, ty = gsup("h")
    b.append(wire(V["345kV"], (tx, ty), (tx, 420)))
    b.append(tower(410, GROUND, 396))
    b.append(tower(570, GROUND, 396))
    b.append(el("path", d=f"M {tx} 420 Q {(tx + 410) / 2} 452 410 420 "
                          f"Q 490 458 570 420 Q 635 450 700 420",
                fill="none", stroke=V["345kV"], stroke_width=tokens.STROKE_HEAVY,
                stroke_linecap="round"))
    b.append(lbl(490, 380, "345 kV corridor", size=10))
    b.append(note(490, 394, "AEP Abilene Northwest line"))

    # --- substation: disconnect -> breaker -> LPT ---
    b.append(el("rect", x=644, y=372, width=170, height=GROUND - 372,
                fill="none", stroke=tokens.FAINT, stroke_width=tokens.STROKE,
                stroke_dasharray="6 5"))
    b.append(lbl(729, 360, "substation · 1 GW · 345 kV greenfield", size=10))
    dsc, dscp = place("disconnect", 668, 438)
    brk, brkp = place("breaker", 668, 516)
    lpt, lptp = place("transformer_2w", 668, 594)
    b += [dsc, brk, lpt]
    b.append(wire(V["345kV"], (700, 420), dscp("in")))
    b.append(wire(V["345kV"], dscp("out"), brkp("in")))
    b.append(wire(V["345kV"], brkp("out"), lptp("h")))
    b.append(lbl(766, 632, "LPT", size=10, anchor="start"))
    b.append(note(766, 646, "345 → 34.5 kV", anchor="start"))

    # --- MV run to building, BESS + gensets tapping it ---
    mx, my = lptp("x")
    MV_Y = 712
    b.append(wire(V["34.5kV"], (mx, my), (mx, MV_Y), (980, MV_Y)))
    bess, bessp = place("battery_bess", 828, 642)
    gset, gsetp = place("genset", 898, 642)
    b += [bess, gset]
    bx, by = bessp("out")
    b.append(wire(V["34.5kV"], (bx, by), (bx, MV_Y), w=tokens.STROKE))
    gx, gy = gsetp("out")
    b.append(wire(V["34.5kV"], (gx, gy), (gx, MV_Y), w=tokens.STROKE))
    b.append(lbl(860, 630, "BESS", size=9.5))
    b.append(lbl(944, 630, "gensets", size=9.5))

    # --- building shell + partitions ---
    b.append(el("rect", x=980, y=360, width=760, height=GROUND - 360,
                fill="none", stroke=tokens.INK, stroke_width=2))
    for px_ in (1260, 1560):
        b.append(wire(tokens.FAINT, (px_, 360), (px_, GROUND),
                      w=tokens.STROKE, dash="6 5"))
    b.append(lbl(1360, 345, "×8 buildings · up to ~50,000 GPUs each", size=10))
    b.append(note(1118, 375, "ELECTRICAL ROOM"))
    b.append(note(1410, 375, "DATA HALL"))
    b.append(note(1650, 375, "MECHANICAL"))

    # --- electrical room: unit substation -> UPS -> busway ---
    usub, usubp = place("transformer_2w", 1030, 588)
    ups, upsp = place("ups", 1120, 646)
    b += [usub, ups]
    ux, uy = usubp("h")
    b.append(wire(V["34.5kV"], (980, MV_Y), (1000, MV_Y), (1000, uy - 16),
                  (ux, uy - 16), (ux, uy)))
    lx, ly = usubp("x")
    ix, iy = upsp("in")
    b.append(wire(V["480V"], (lx, ly), (lx, iy), (ix, iy)))
    ex, ey = upsp("out")
    BUS_Y = 540
    b.append(wire(V["480V"], (ex, ey), (ex + 24, ey), (ex + 24, BUS_Y),
                  (1470, BUS_Y)))
    b.append(lbl(1062, 576, "unit sub", size=9.5))
    b.append(note(1062, 566, "34.5 kV → 480 V"))
    b.append(lbl(1152, 730, "UPS", size=9.5))
    b.append(lbl(1330, 528, "busway (480 V)", size=9.5))

    # camera frame demo
    b.append(el("rect", x=988, y=548, width=264, height=200, fill="none",
                stroke=tokens.FAINT, stroke_width=1.2, stroke_dasharray="3 4"))
    b.append(note(992, 760, "camera — 'the electrical room' segment",
                  anchor="start"))

    # --- rack: shelf -> VRM -> die -> cold plate ---
    b.append(el("rect", x=1330, y=596, width=104, height=GROUND - 596 - 6,
                fill="none", stroke=tokens.INK, stroke_width=tokens.STROKE))
    b.append(lbl(1382, 588, "rack", size=9.5))
    shf, shfp = place("converter_rectifier", 1352, 606, s=0.62)
    vrm, vrmp = place("converter_dcdc", 1352, 664, s=0.62)
    die, diep = place("die_gpu", 1352, 716, s=0.62)
    b += [shf, vrm, die]
    ax, ay = shfp("ac")
    b.append(wire(V["480V"], (ax + 8, BUS_Y), (ax + 8, ay - 10), (ax, ay - 10),
                  (ax, ay), w=tokens.STROKE))
    dx, dy = shfp("dc")
    vx, vy = vrmp("in")
    b.append(wire(V["54V"], (dx, dy), (dx + 6, dy), (dx + 6, vy - 8),
                  (vx - 6, vy - 8), (vx - 6, vy), (vx, vy), w=tokens.STROKE))
    wx, wy = vrmp("out")
    px2, py2 = diep("power")
    b.append(wire(V["0.8V"], (wx, wy), (wx + 4, wy), (wx + 4, py2 - 6),
                  (px2, py2 - 6), (px2, py2), w=tokens.STROKE))
    b.append(note(1440, 640, "PSU shelf · 480 V → 54 V", anchor="start"))
    b.append(note(1440, 690, "VRM · 54 V → 0.8 V", anchor="start"))
    b.append(note(1440, 740, "GPU die — the turn:", anchor="start"))
    b.append(note(1440, 752, "the watt becomes heat", anchor="start"))

    # --- thermal return: die -> cold plate -> CDU -> roof -> atmosphere ---
    cp, cpp = place("cold_plate", 1352, 762, s=0.62)
    b.append(cp)
    hx2, hy2 = diep("heat")
    ch, cv = cpp("heat")
    b.append(wire(T["die"], (hx2, hy2), (ch, cv - 22 if cv - 22 > hy2 else cv)))
    cdu, cdup = place("cdu", 1600, 640)
    b.append(cdu)
    ox2, oy2 = cpp("liquid_out")
    ti, tj = cdup("tech_in")
    b.append(wire(T["liquid_hot"], (ox2, oy2), (1500, oy2), (1500, tj), (ti, tj)))
    fx, fy = cdup("fac_out")
    dc_, dcp_ = place("dry_cooler", 1580, 296)
    b.append(dc_)
    li, lj = dcp_("liquid_in")
    b.append(wire(T["liquid_warm"], (fx, fy), (1572, fy), (1572, lj), (li, lj)))
    atm, atmp = place("atmosphere", 1580, 192)
    b.append(atm)
    ai, aj = dcp_("air_out")
    mi, mj = atmp("in")
    b.append(wire(T["air"], (ai, aj), (ai, mj + 6), (mi, mj + 6), (mi, mj)))
    b.append(lbl(1632, 730, "CDU", size=9.5))
    b.append(note(1632, 744, "tech loop → facility loop"))
    b.append(lbl(1560, 270, "air-cooled chillers", size=9.5, anchor="end"))
    b.append(note(1560, 284, "zero-evaporation (Abilene)", anchor="end"))

    frame = el("rect", x=0, y=0, width=W, height=H, fill=tokens.PAPER)
    return el("svg", frame + "".join(b), xmlns="http://www.w3.org/2000/svg",
              width=W, height=H, viewBox=f"0 0 {W} {H}")


def build_zoom() -> str:
    b: list[str] = []
    b.append(text(60, 70, "THE ELECTRICAL ROOM", size=34, anchor="start",
                  weight=700, fill=tokens.INK))
    b.append(text(60, 104, "34.5 kV enters the building; 480 V leaves this "
                  "room. Nothing downstream exists without it.",
                  size=15, anchor="start", fill=tokens.INK))
    b.append(journey_bar(1080, 40, active="480V"))

    SC = 2.6
    CHAIN_Y = 520

    usub, usubp = place("transformer_2w", 260, CHAIN_Y - S * SC / 2, s=SC, rot=-90)
    brk, brkp = place("breaker", 640, CHAIN_Y - S * SC / 2, s=SC, rot=-90)
    ups, upsp = place("ups", 1020, CHAIN_Y - S * SC / 2, s=SC)
    b += [usub, brk, ups]

    hx, hy = usubp("h")
    b.append(wire(V["34.5kV"], (60, hy), (hx, hy), w=4.5))
    b.append(lbl(64, hy - 24, "34.5 kV feeder — from the campus substation",
                 size=13, anchor="start"))
    xx, xy = usubp("x")
    bi, bj = brkp("in")
    b.append(wire(V["480V"], (xx, xy), (bi, bj), w=4.5))
    bo, bp_ = brkp("out")
    ui, uj = upsp("in")
    b.append(wire(V["480V"], (bo, bp_), (ui, uj), w=4.5))
    uo, up_ = upsp("out")
    b.append(wire(V["480V"], (uo, up_), (1860, up_), w=4.5))
    b.append(lbl(1856, up_ - 24, "busway → data hall", size=13, anchor="end"))

    def caption(cx: float, name: str, gate: str, vendors: str | None,
                mult: str | None) -> None:
        y = CHAIN_Y + S * SC / 2 + 46
        b.append(lbl(cx, y, name, size=17, weight=700))
        b.append(lbl(cx, y + 26, gate, size=13, weight=400))
        if vendors:
            b.append(note(cx, y + 50, vendors, size=11.5))
        if mult:
            b.append(note(cx, y + 70, mult, size=11.5))

    caption(260 + S * SC / 2, "Unit substation", "34.5 kV → 480 V",
            None, "one per lineup")
    caption(640 + S * SC / 2, "LV switchgear", "fault isolation — no "
            "energization without it", None, None)
    caption(1020 + S * SC / 2, "UPS (double conversion)",
            "bridges the seconds until gensets pick up",
            "Eaton · Vertiv · Schneider Electric",
            "×N lineups per building — VERIFY count")

    b.append(note(60, 1020, "mock v0 — one camera state of the master cutaway; "
                  "this is what a segment looks like on screen", anchor="start"))

    frame = el("rect", x=0, y=0, width=W, height=H, fill=tokens.PAPER)
    return el("svg", frame + "".join(b), xmlns="http://www.w3.org/2000/svg",
              width=W, height=H, viewBox=f"0 0 {W} {H}")


def main() -> None:
    out = Path(__file__).resolve().parents[2] / "diagram"
    (out / "mock_wide.svg").write_text(build_wide())
    print(f"wrote {out / 'mock_wide.svg'}")
    (out / "mock_zoom.svg").write_text(build_zoom())
    print(f"wrote {out / 'mock_zoom.svg'}")


if __name__ == "__main__":
    main()
