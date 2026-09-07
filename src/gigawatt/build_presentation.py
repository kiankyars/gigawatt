"""Build a deliberately authored teaching sequence, separate from reading prose."""

from __future__ import annotations

import json
import re
from pathlib import Path

KINDS = ("intro", "current", "loss", "ac", "sidecar", "facility", "transfer")


def presentation_outputs(root: Path, sample_id: str) -> dict[Path, str]:
    data = json.loads((root / "course/expansion/sample-presentation.json").read_text())
    if data["source_lesson_id"] != sample_id:
        raise ValueError("Presentation must refer to the authored sample")
    steps = data["steps"]
    if tuple(step["kind"] for step in steps) != KINDS:
        raise ValueError(
            "Presentation requires the authored seven-step teaching sequence"
        )
    if len({step["id"] for step in steps}) != len(steps):
        raise ValueError("Duplicate presentation step IDs")
    for step in steps:
        if not re.fullmatch(r"[a-z0-9-]+", step["id"]):
            raise ValueError("Unsafe presentation step ID")
        for field, limit in (("headline", 10), ("caption", 18)):
            if not 0 < len(step[field].split()) <= limit:
                raise ValueError(
                    f"{step['id']}: audience {field} exceeds the text budget"
                )
        if not step.get("cue") or not step.get("notes"):
            raise ValueError(
                "Presenter reasoning and action cues must be authored separately"
            )
    web = root / "course/web"
    script = re.sub(
        r"^export ", "", (web / "reader-models.js").read_text(), flags=re.MULTILINE
    )
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
    return {Path("course/sample.html"): html, Path("course/sample-notes.html"): html}
