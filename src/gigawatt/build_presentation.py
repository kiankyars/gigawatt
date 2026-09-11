"""Build a deliberately authored teaching sequence, separate from reading prose."""

from __future__ import annotations

import json
import re
from pathlib import Path

KINDS = {
    "intro",
    "dc-basics",
    "ac-basics",
    "three-phase",
    "voltage-basis",
    "copper",
    "current",
    "loss",
    "ac",
    "sidecar",
    "facility",
    "conversion-loss",
    "decision",
}
ROLES = {
    "problem",
    "comparison",
    "mechanism",
    "architecture",
    "balance",
    "counterexample",
    "transfer",
}
CONTRACT_FIELDS = (
    "driving_question",
    "fixed_boundary",
    "changed_variable",
    "primary_payoff",
    "misconception",
    "transfer_question",
)


def validate_presentation(data: dict) -> None:
    """Enforce teaching boundaries without imposing one lesson's scene order."""
    contract = data.get("learning_contract", {})
    for field in CONTRACT_FIELDS:
        if not isinstance(contract.get(field), str) or not contract[field].strip():
            raise ValueError(f"Missing learning contract: {field}")
    steps = data["steps"]
    if not steps or any(step["kind"] not in KINDS for step in steps):
        raise ValueError("Presentation requires supported visual kinds")
    roles = [step.get("pedagogical_role") for step in steps]
    if any(role not in ROLES for role in roles):
        raise ValueError("Each visual needs a declared teaching purpose")
    if roles[0] != "problem" or roles[-1] != "transfer":
        raise ValueError("Start with the problem and finish with changed-case transfer")
    if "mechanism" not in roles:
        raise ValueError("Explain the mechanism before assessing transfer")
    if len({step["id"] for step in steps}) != len(steps):
        raise ValueError("Duplicate presentation step IDs")
    for step in steps:
        if not re.fullmatch(r"[a-z0-9-]+", step["id"]):
            raise ValueError("Unsafe presentation step ID")
        for field, limit in (("headline", 18),):
            if not 0 < len(step[field].split()) <= limit:
                raise ValueError(
                    f"{step['id']}: audience {field} exceeds the text budget"
                )
        if not step.get("cue") or not step.get("notes") or not step.get("explanation"):
            raise ValueError(
                "Presenter reasoning and action cues must be authored separately"
            )
    if data["planned_duration_seconds"] != sum(s["duration_seconds"] for s in steps):
        raise ValueError("Planned duration must match the authored scene timings")
    for target in data.get("aliases", {}).values():
        if target not in {step["id"] for step in steps}:
            raise ValueError("Presentation alias points to a missing scene")


def presentation_outputs(root: Path, sample_id: str) -> dict[Path, str]:
    data = json.loads((root / "course/expansion/sample-presentation.json").read_text())
    if data["source_lesson_id"] != sample_id:
        raise ValueError("Presentation must refer to the authored sample")
    validate_presentation(data)
    web = root / "course/web"
    script = re.sub(
        r"^export ", "", (web / "reader-models.js").read_text(), flags=re.MULTILINE
    )
    script += "\n" + (web / "electrical-visuals.js").read_text()
    script += "\n" + (web / "presentation.js").read_text()
    replacements = {
        "__PRESENTATION_CSS__": (web / "presentation.css").read_text(),
        "__PRESENTATION_DATA__": json.dumps(
            data, ensure_ascii=False, separators=(",", ":")
        ).replace("<", "\\u003c"),
        "__PRESENTATION_SCRIPT__": re.sub(
            r"</script", r"<\\/script", script, flags=re.IGNORECASE
        ),
    }
    template = (web / "presentation.html").read_text()
    if any(template.count(marker) != 1 for marker in replacements):
        raise ValueError("Presentation template placeholders must occur exactly once")
    html = re.sub(
        r"__PRESENTATION_CSS__|__PRESENTATION_DATA__|__PRESENTATION_SCRIPT__",
        lambda match: replacements[match[0]],
        template,
    )
    if html.count("__PRESENTATION_MODE__") != 1:
        raise ValueError("Expected exactly one view placeholder")
    return {
        Path("course/sample.html"): html.replace("__PRESENTATION_MODE__", "student"),
        Path("course/teach.html"): html.replace("__PRESENTATION_MODE__", "teach"),
        Path("course/sample-notes.html"): html.replace(
            "__PRESENTATION_MODE__", "notes"
        ),
    }
