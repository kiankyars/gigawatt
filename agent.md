The symbol library is built and rendered. Here's the redline sheet:

GIGAWATT symbol library redline sheet v0

What exists now:

uv project (pyproject.toml, src/gigawatt/) — stdlib only, no dependencies. uv run gigawatt-symbols regenerates the sheet.
tokens.py — the entire aesthetic in one file: one typeface, two line weights, the voltage-keyed scale (500 kV → 0.8 V) plus the thermal scale, flat fills only.
symbols.py — 27 symbols: IEEE 315 / ANSI one-line for electrical (generator, winding-hump transformer, drawout breaker, battery/BESS, IEC converter boxes, double-conversion UPS), simplified P&ID for thermal (pump, HX, CDU package, cooling tower, CRAH). Symbols are generic devices with named connection ports — master.yaml nodes will map onto them (e.g. vrm → converter_dcdc), and the layout engine routes edges via ports without knowing geometry.
diagram/symbols.svg — the contact sheet, which is your redline artifact per the anti-slop contract.
Worth a human pass on the sheet before layout work starts: the gas-turbine trapezoid and cold-plate serpentine are the two custom glyphs I'd scrutinize most, and whether Inter is the typeface you want is a taste call I've made provisionally.

The reference campus is pinned: **Abilene (Lancium / Crusoe / Oracle — Stargate)**, per the recommendation from [Campus scout](a024e0b8-6efa-47c6-8303-b98f6dad8764). It was the only candidate satisfying all four criteria simultaneously: typed 1.2 GW grid connection, the deepest evidence package in the atlas (curated record + municipal permitting + two satellite-change retains + a Jun 2024 → Jun 2026 chronology), a real generation story (ERCOT direct tie, 200 MW + 1 GW substation ladder, GE Vernova turbines on site), and enough construction dates to hang the diagram on.

Changes made: `diagram/master.yaml` now carries a `reference_campus` block with atlas source paths, dated facts, and an `open_verifies` list; the gas-turbine node is annotated with the on-site GE Vernova units; `STRATEGY.md` records the decision and keeps Project Jupiter (2.45 GW behind-the-meter fuel cells) in reserve as the BTM contrast case for the capital-stack read.

One consequence worth your attention: **ERCOT has no 500 kV — its transmission tops out at 345 kV.** The journey bar's top rung and the `500kV` color token will need re-pinning once the actual interconnection voltage at Abilene is verified. I've listed that first in `open_verifies` rather than silently renaming tokens, since it needs a dated source before it renders.