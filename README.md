# GIGAWATT

**From watts to racks. Then all the way back to the air.**

An interactive course about the physical systems that make a data center work.
Start with a rack's two obligations: deliver electrical power and remove heat.
Then follow the grid connection, electrical distribution, continuity of service,
rack power conversion, useful computation, and the return of heat to the atmosphere.

The course uses purpose-built SVG diagrams, interactive engineering scenarios,
short explanations, retrieval questions, and expandable notes with primary sources.
Each interaction changes a relationship the learner can explain: voltage and
current, energy and runtime, capacity after a failure, heat and flow, or facility
power and IT load. The instructor or learner controls the pace.

## Run it

```sh
uv run gigawatt-build
python3 -m http.server --directory diagram 8000
```

Open [the local course](http://localhost:8000). `diagram/index.html` is the single
generated teaching page; it contains its own styles, code, diagrams, and content.
It can also be opened directly as a local file. Source links require a network
connection, but the course itself does not.

## Edit and verify

- `course/lessons.json` owns the chapter order, explanations, checks, notes, and sources.
- `course/web/index.html` and `course/web/course.css` own the page and visual system.
- `course/web/diagrams.js` owns the explanatory diagrams and their interactions.
- `course/web/math.js` owns the engineering calculations.
- `course/web/course.js` owns navigation, lesson state, notes, and knowledge checks.
- `src/gigawatt/build_course.py` validates and assembles the self-contained page.

After editing, regenerate and run:

```sh
uv run gigawatt-build
uv run gigawatt-build --check
uv run python -m unittest discover -s tests -p 'test_*.py' -v
node --test tests/math.test.mjs
git diff --check
```

Use `course/TESTING.md` for the browser walkthrough. A successful build checks
content relationships and artifact freshness; visual and teaching quality require
actually using the course.

GitHub Pages validates these checks and publishes `diagram/index.html` when
`main` changes. Previously published course and phase URLs redirect to the same
course. The production course is [GIGAWATT](https://kiankyars.github.io/gigawatt/).

## Scope and evidence

The core is data center engineering. Generation technologies, commercial
structures, and project history appear only when they explain a physical
constraint. The Abilene example is a bounded application of the course, with
dated evidence and explicit unknowns. Teaching scenarios are labeled assumptions
and do not estimate a site's installed equipment or operating performance.

`evidence/` retains the earlier source ledgers, and `diagram/master.yaml`,
`diagram/layout.yaml`, and `diagram/master.svg` retain the researched engineering
map. They are reference material, separate from the active lesson source. Their
dated site claims need rechecking before reuse. The small reference symbol and
map generators remain available as `gigawatt-symbols` and `gigawatt-layout`.

Earlier course players, alternate curricula, 3D pilots, and champion/challenger
experiments have been retired. Their history remains in Git.
