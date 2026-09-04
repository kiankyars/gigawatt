# Course source

`lessons.json` is the active curriculum. It contains the title, chapter list, and
ordered lessons. Each lesson specifies a stable ID, chapter, visual ID, short
explanation, takeaway, longer notes, and sources. Optional checks include a
question, options, a zero-based answer index, and an explanation.

`web/` contains the HTML template, CSS, native SVG visuals, engineering math,
and navigation code. The visual registry in `diagrams.js` is the authority for
the visual IDs used by lessons. `gigawatt-build` embeds all of these inputs into
`../diagram/index.html`; edit the inputs and regenerate the page.

```sh
uv run gigawatt-build
uv run gigawatt-build --check
```

The core journey is rack requirements, grid delivery, electrical continuity,
silicon, cooling, and whole-system limits. Lessons build one physical model.
Keep examples and questions useful to that journey, with explicit numerical
assumptions and a clear separation between generic principles and dated site
claims.

The source ledgers under `../evidence/` are retained research references. They
do not automatically establish a lesson's correctness or current project state;
inspect and cite the underlying source when reusing a claim.

`TESTING.md` covers release checks and the visual walkthrough. Retired players
and experimental curricula remain available through Git history.
