"""Stage the generated reader, assets and durable reference paths for Pages."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def stage(root=ROOT, destination=None):
    destination = destination or root / "_site"
    destination.mkdir(parents=True, exist_ok=True)
    paths = [Path("README.md"), Path("diagram/index.html")]
    for directory in ("course", "research"):
        paths.extend(p.relative_to(root) for p in (root / directory).glob("*.md"))
        paths.extend(p.relative_to(root) for p in (root / directory).glob("*.json"))
    paths.extend(p.relative_to(root) for p in (root / "course").glob("*.html"))
    for directory in ("course/assets", "course/lessons", "research/sources"):
        paths.extend(
            p.relative_to(root) for p in (root / directory).glob("*") if p.is_file()
        )
    for path in paths:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / path, target)
    legacy = json.loads((root / "course/lessons.json").read_text())["lessons"]
    ids = json.dumps([l["id"] for l in legacy]).replace("<", "\\u003c")
    redirect = f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GIGAWATT — Data center course</title>
<script>let id;try{{id=decodeURIComponent(location.hash.slice(1));}}catch{{id="";}}
const legacy=new Set({ids});
location.replace((legacy.has(id)?"diagram/index.html":"course/index.html")+location.search+location.hash);</script>
<p><a href="course/index.html">Open the expanded GIGAWATT course.</a></p>
<p><a href="diagram/index.html">Open the interactive introduction.</a></p></html>"""
    aliases = (
        "index.html",
        "course.html",
        "course_v2.html",
        "v1.html",
        "hybrid.html",
        "phase1_generation.html",
        "phase2_transmission.html",
        "phase3_campus.html",
        "phase4_building.html",
        "phase5_compute.html",
        "phase6_heat.html",
    )
    for name in aliases:
        (destination / name).write_text(redirect, encoding="utf-8")
    retired_docs = {
        "STRATEGY.md": "course/COURSE_REVIEW.md",
        "course/COMPANION.md": "COURSE_REVIEW.md#companion-experience",
        "course/REVIEW_HELP.md": "PRESENTING.md",
        "course/expansion/AUTHORING.md": "../TEACHING_STANDARD.md",
    }
    for old_path, replacement in retired_docs.items():
        target = destination / old_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            f"# This document has moved\n\nRead the [consolidated guidance]({replacement}).\n",
            encoding="utf-8",
        )
    (destination / ".nojekyll").touch()
    return destination


if __name__ == "__main__":
    print(f"Staged course at {stage()}")
