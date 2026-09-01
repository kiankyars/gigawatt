"""Build the evidence-bound Phase 3 campus distribution teaching pilot.

Usage: uv run python diagram/generate_phase3_campus.py
"""

from __future__ import annotations

from pathlib import Path

from gigawatt import campus_visual, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase3_campus.yaml"
OUTPUT = ROOT / "diagram" / "phase3_campus.html"
GENERATOR_DEPENDENCY_PATHS = (
    ROOT / "pyproject.toml",
    ROOT / "uv.lock",
    Path(__file__).resolve(),
    Path(teaching_visuals.__file__).resolve(),
    Path(campus_visual.__file__).resolve(),
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
    payload = campus_visual.compile_campus_distribution(
        manifest,
        ledgers,
        source_digest=digest,
    )
    rendered = campus_visual.render_campus_distribution(payload)
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
