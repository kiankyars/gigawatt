"""Read-only verification for a frozen course champion stored in Git."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]


class ChampionVerificationError(ValueError):
    """Raised when the frozen champion cannot be verified from repository data."""


def _full_hex_digest(value: Any, *, length: int, location: str) -> str:
    if type(value) is not str or re.fullmatch(rf"[0-9a-f]{{{length}}}", value) is None:
        raise ChampionVerificationError(
            f"{location} must be a full {length}-character lowercase hexadecimal digest"
        )
    return value


def _validate_champion_schema(champion: Any) -> dict[str, Any]:
    if type(champion) is not dict:
        raise ChampionVerificationError("champion must be a mapping")
    required = {
        "git_sha",
        "origin_sha",
        "source_tree_aggregate_sha256",
        "baseline_test_count",
        "baseline_runtime_source_digest",
        "artifact_sha256",
    }
    actual = set(champion)
    missing = sorted(required - actual)
    unknown = sorted(actual - required)
    if missing or unknown:
        raise ChampionVerificationError(
            f"champion fields must be exact; missing={missing} unknown={unknown}"
        )

    _full_hex_digest(champion["git_sha"], length=40, location="champion.git_sha")
    _full_hex_digest(champion["origin_sha"], length=40, location="champion.origin_sha")
    _full_hex_digest(
        champion["source_tree_aggregate_sha256"],
        length=64,
        location="champion.source_tree_aggregate_sha256",
    )
    _full_hex_digest(
        champion["baseline_runtime_source_digest"],
        length=64,
        location="champion.baseline_runtime_source_digest",
    )
    baseline_test_count = champion["baseline_test_count"]
    if type(baseline_test_count) is not int or baseline_test_count < 1:
        raise ChampionVerificationError(
            "champion.baseline_test_count must be a positive integer"
        )

    artifacts = champion["artifact_sha256"]
    if type(artifacts) is not dict or not artifacts:
        raise ChampionVerificationError(
            "champion.artifact_sha256 must be a non-empty mapping"
        )
    for file_name, expected_digest in artifacts.items():
        if type(file_name) is not str or not file_name:
            raise ChampionVerificationError(
                "champion.artifact_sha256 keys must be non-empty strings"
            )
        _full_hex_digest(
            expected_digest,
            length=64,
            location=f"champion.artifact_sha256[{file_name!r}]",
        )
    return champion


def _git(repo: Path, *arguments: str) -> bytes:
    try:
        completed = subprocess.run(
            ["git", "-C", str(repo), *arguments],
            check=True,
            capture_output=True,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        detail = getattr(error, "stderr", b"")
        message = detail.decode(errors="replace").strip()
        raise ChampionVerificationError(
            f"git {' '.join(arguments)} failed: {message or error}"
        ) from error
    return completed.stdout


def _blob(repo: Path, git_sha: str, file_name: str) -> bytes:
    return _git(repo, "show", f"{git_sha}:{file_name}")


def tree_aggregate_sha256(repo: Path, git_sha: str) -> str:
    """Reproduce the frozen baseline's tracked-file aggregate at ``git_sha``."""
    raw_names = _git(repo, "ls-tree", "-r", "--name-only", "-z", git_sha)
    file_names = sorted(name for name in raw_names.split(b"\0") if name)
    aggregate = hashlib.sha256()
    for raw_name in file_names:
        file_name = raw_name.decode("utf-8")
        blob_digest = hashlib.sha256(_blob(repo, git_sha, file_name)).hexdigest()
        aggregate.update(f"{blob_digest}  {file_name}\n".encode())
    return aggregate.hexdigest()


def changed_worktree_paths(repo: Path, git_sha: str) -> tuple[str, ...]:
    """Return paths whose current bytes differ from a frozen Git snapshot."""

    tracked = _git(
        repo,
        "diff",
        "--name-only",
        "--no-renames",
        "-z",
        git_sha,
        "--",
    )
    untracked = _git(repo, "ls-files", "--others", "--exclude-standard", "-z")
    return tuple(
        sorted(
            {
                raw_path.decode("utf-8")
                for raw_path in (*tracked.split(b"\0"), *untracked.split(b"\0"))
                if raw_path
            }
        )
    )


def _provenance_state(
    repo: Path, declared_origin_sha: Any
) -> dict[str, dict[str, Any]]:
    tracking_ref = "refs/remotes/origin/main"
    try:
        observed_sha = _git(repo, "rev-parse", tracking_ref).decode().strip()
    except ChampionVerificationError as error:
        origin_main = {
            "status": "unavailable",
            "observation_kind": "local_remote_tracking_ref",
            "ref": tracking_ref,
            "declared_frozen_sha": declared_origin_sha,
            "observed_sha": None,
            "matches_declared_frozen_sha": None,
            "integrity_relevant": False,
            "detail": str(error),
        }
    else:
        matches = observed_sha == declared_origin_sha
        origin_main = {
            "status": (
                "matches_frozen_declaration"
                if matches
                else "differs_from_frozen_declaration"
            ),
            "observation_kind": "local_remote_tracking_ref",
            "ref": tracking_ref,
            "declared_frozen_sha": declared_origin_sha,
            "observed_sha": observed_sha,
            "matches_declared_frozen_sha": matches,
            "integrity_relevant": False,
            "detail": (
                "A local remote-tracking ref is mutable and is not live remote "
                "verification."
            ),
        }
    return {
        "origin_main_tracking_ref": origin_main,
        "live_remote": {
            "status": "not_checked",
            "integrity_relevant": False,
            "detail": "No network fetch or remote query was performed.",
        },
    }


def verify_frozen_champion(
    champion: dict[str, Any], *, repo: Path = ROOT
) -> dict[str, Any]:
    """Return fail-closed, reproducible checks for the frozen Git snapshot."""
    champion = _validate_champion_schema(champion)
    git_sha = champion["git_sha"]

    checks: list[dict[str, Any]] = []

    def record(check_id: str, expected: Any, actual: Any) -> None:
        checks.append(
            {
                "id": check_id,
                "expected": expected,
                "actual": actual,
                "passed": actual == expected,
            }
        )

    resolved_commit = _git(repo, "rev-parse", f"{git_sha}^{{commit}}").decode().strip()
    record("git_commit", git_sha, resolved_commit)
    record(
        "tracked_tree_aggregate",
        champion["source_tree_aggregate_sha256"],
        tree_aggregate_sha256(repo, git_sha),
    )

    artifacts = champion["artifact_sha256"]
    for file_name, expected_digest in sorted(artifacts.items()):
        record(
            f"artifact:{file_name}",
            expected_digest,
            hashlib.sha256(_blob(repo, git_sha, file_name)).hexdigest(),
        )

    runtime = json.loads(_blob(repo, git_sha, "diagram/course_runtime.json"))
    record(
        "runtime_source_digest",
        champion["baseline_runtime_source_digest"],
        runtime.get("source_digest"),
    )
    record("runtime_segment_count", 26, len(runtime.get("segments", [])))
    record("declared_baseline_test_count", 349, champion["baseline_test_count"])

    failures = [check for check in checks if not check["passed"]]
    return {
        "static_integrity_passed": not failures,
        "checks": checks,
        "failures": failures,
        "provenance_state": _provenance_state(repo, champion["origin_sha"]),
        "historical_test_reproduction": {
            "command": "uv run python -m unittest discover -s tests -v",
            "git_sha": git_sha,
            "expected_test_count": champion["baseline_test_count"],
            "status": "requires_external_execution",
        },
        "missing_live_evidence": [
            "historical_per_viewport_frame_captures",
            "historical_per_viewport_quality_vectors",
        ],
    }


def require_frozen_champion(
    champion: dict[str, Any], *, repo: Path = ROOT
) -> dict[str, Any]:
    result = verify_frozen_champion(champion, repo=repo)
    if not result["static_integrity_passed"]:
        failed_ids = [failure["id"] for failure in result["failures"]]
        raise ChampionVerificationError(
            f"frozen champion verification failed: {failed_ids}"
        )
    return result
