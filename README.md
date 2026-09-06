# GIGAWATT

**From watts to racks, useful compute, and operation.**

GIGAWATT is being expanded into a reference course on modern AI data-center
infrastructure. Start with the [domain atlas](course/domain-map.html),
[domain map](course/DOMAIN_MAP.md), [course review](course/COURSE_REVIEW.md),
[companion design](course/COMPANION.md), and [research library](research/README.md).
These describe the proposed expansion; the existing player remains a 22-lesson
electrical-and-thermal introduction.

The current interactive introduction explains the physical systems that make a
data center work.
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

- `course/COURSE_REVIEW.md` owns the expanded learner contract and production review.
- `course/domain-map.json` owns the proposed domains, capabilities and assessments.
- `course/research-sources.json` owns the curated research source catalog.
- `course/lessons.json` owns the current player's chapter order, explanations,
  checks, notes, and sources.
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

Build the planning atlas and Markdown coverage map with `uv run gigawatt-map`;
use `uv run gigawatt-map --check` to validate references, prerequisite order and
generated outputs. The research library documents its separate discovery and
note-building commands. Serve the repository root to browse the planning atlas
at `/course/domain-map.html`; serving only `diagram/` exposes the current player.

GitHub Pages validates these checks and publishes `diagram/index.html` when
`main` changes. Previously published course and phase URLs redirect to the same
course. The production course is [GIGAWATT](https://kiankyars.github.io/gigawatt/).

## Scope and evidence

The expanded scope includes power, compute/memory, networking, storage, cooling,
physical design, delivery, operations and system economics. The domain map
sets the depth and explicit exclusions. The existing Abilene example is a
bounded application of the introduction, with
dated evidence and explicit unknowns. Teaching scenarios are labeled assumptions
and do not estimate a site's installed equipment or operating performance.

`evidence/` retains the earlier source ledgers, and `diagram/master.yaml`,
`diagram/layout.yaml`, and `diagram/master.svg` retain the researched engineering
map. They are reference material, separate from the active lesson source. Their
dated site claims need rechecking before reuse. The small reference symbol and
map generators remain available as `gigawatt-symbols` and `gigawatt-layout`.

Earlier course players, alternate curricula, 3D pilots, and champion/challenger
experiments have been retired. Their history remains in Git.
