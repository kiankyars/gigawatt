"""Build the evidence-bound Phase 5 rack-to-compute teaching pilot.

Usage: uv run python diagram/generate_phase5_compute.py
"""

from __future__ import annotations

from pathlib import Path

from gigawatt import compute_visual, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase5_compute.yaml"
OUTPUT = ROOT / "diagram" / "phase5_compute.html"
GENERATOR_DEPENDENCY_PATHS = (
    ROOT / "pyproject.toml",
    ROOT / "uv.lock",
    Path(__file__).resolve(),
    Path(compute_visual.__file__).resolve(),
    Path(teaching_visuals.__file__).resolve(),
)


def _evidence_paths(manifest: dict) -> dict[str, Path]:
    return teaching_visuals.registered_evidence_paths(manifest, root=ROOT)


def _source_digest(
    manifest: dict | None = None,
    evidence_paths: dict[str, Path] | None = None,
) -> str:
    if manifest is None:
        manifest = teaching_visuals.load_yaml(MANIFEST)
    if evidence_paths is None:
        evidence_paths = _evidence_paths(manifest)
    return teaching_visuals.source_digest(
        ROOT,
        (
            *GENERATOR_DEPENDENCY_PATHS,
            MANIFEST,
            *(evidence_paths[ledger_id] for ledger_id in sorted(evidence_paths)),
        ),
    )


def build() -> tuple[str, str, int]:
    manifest = teaching_visuals.load_yaml(MANIFEST)
    evidence_paths = _evidence_paths(manifest)
    ledgers = {
        ledger_id: teaching_visuals.load_yaml(path)
        for ledger_id, path in evidence_paths.items()
    }
    digest = _source_digest(manifest, evidence_paths)
    payload = compute_visual.compile_compute_power_descent(
        manifest,
        ledgers,
        source_digest=digest,
    )
    rendered = compute_visual.render_compute_power_descent(payload)
    return rendered, digest, len(payload["states"])


def main() -> None:
    rendered, digest, state_count = build()
    OUTPUT.write_text(rendered)
    print(
        f"built {OUTPUT.relative_to(ROOT)} · {state_count} manual states "
        f"· digest {digest}"
    )


if __name__ == "__main__":
    main()
