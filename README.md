# GIGAWATT

A long-form, diagram-heavy course on how a watt moves from generation to
a GPU's transistors and back out as heat — and who builds, owns, finances, and
bottlenecks each step.

**Follow one watt:** generation → interconnection → substation → transformer →
switchgear → UPS/BESS → busway → rack → PSU → VRM → die → cold plate → CDU →
chilled water → cooling → atmosphere.

**Reference campus:** Abilene (Lancium / Crusoe / Oracle — Stargate).

Status: master-diagram stage. The 2D one-line (`diagram/master.svg`) is the
engineering map. The three.js scene (`diagram/mock_3d.html`) is the
establishing shot and the spatial zooms (electrical room, rack). See `STRATEGY.md`.

```
uv run gigawatt-symbols   # symbol library contact sheet
uv run gigawatt-layout    # compose master.svg from YAML
uv run gigawatt-mock      # leftover 2D style-test frames
python3 -m http.server --directory diagram   # then open mock_3d.html
```
