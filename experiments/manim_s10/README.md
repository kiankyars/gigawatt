# ManimCE s10 renderer experiment

Status: **rejected spike; not a production course path**.

The rendered comparison failed the project's visual quality bar. It read as
generic vector animation, while reaching the intended explanatory quality would
require bespoke design and choreography that does not justify maintaining a
second renderer. These files remain only to preserve the evaluation record and
are excluded from the active course validation path.

This isolated experiment renders one transformation from
`course/pilots/s10_two_rack_heat_paths.yaml` per invocation. It consumes the
manifest's canonical node and edge IDs and reads geometry and labels from the
existing master and scene files.

The loader rejects extra manifest fields, unknown IDs, IDs outside the
canonical s10 scope, and pulse edges that are not also focused. It does not add
Manim to the project dependencies. `uv` supplies ManimCE and PyYAML in a
temporary environment.

On macOS, Pycairo may build locally. The verified setup uses Homebrew's Cairo
and package-discovery helper:

```sh
brew install cairo pkgconf
```

Validation and every rendered frame expose the same SHA-256 source digest as
the native pilot. The digest covers, in order, the course inventory, pilot
manifest, semantic master, 3D scene, and cameras using each repository-relative
path, a NUL byte, the raw file bytes, and a trailing NUL byte.

Validate the shared manifest:

```sh
uv run python experiments/manim_s10/manifest.py
```

Render one independent low-quality clip:

```sh
GIGAWATT_TRANSFORMATION_ID=liquid_cooled_compute \
  uv run --isolated --with 'manim==0.21.0' --with 'PyYAML>=6.0.3' \
  manim render -ql --disable_caching \
  --media_dir experiments/manim_s10/media \
  -o liquid_cooled_compute \
  experiments/manim_s10/scene.py TransformationClip
```

Valid transformation IDs are printed by the validation command. Each output
is self-contained so a player or instructor can select it manually. Generated
media is intentionally ignored by Git. The motion needed to express a
transition inside an individual clip is renderer mechanics only; it never
defines or implies course pacing.
