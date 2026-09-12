"""Stage the generated reader, assets and durable reference paths for Pages."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Keep shared links useful after retiring the original 22-lesson introduction.
# Its source remains in the repository for the curriculum's migration history.
INTRODUCTION_REDIRECTS = {
    "one-rack": "d01-boundaries",
    "power-and-energy": "d01-power-over-time",
    "sources-and-grid": "d03-power-and-procurement",
    "raise-voltage": "d03-voltage-and-distance",
    "substation-functions": "d04-read-the-power-train",
    "capacity-stages": "d03-service-and-siting",
    "building-power-train": "d04-read-the-power-train",
    "ride-through": "d05-storage-power-and-time",
    "redundant-paths": "d05-paths-and-transitions",
    "fault-domains": "d05-protection-and-fault-domains",
    "rack-conversion": "d06-conversion-ledger",
    "low-voltage-current": "d04-current-and-rating",
    "useful-compute": "d02-productive-utilization",
    "electrical-to-heat": "d10-local-thermal-paths",
    "liquid-heat-transport": "d10-flow-and-pressure",
    "heat-exchanger": "d10-cdu-interfaces",
    "residual-air": "d10-local-thermal-paths",
    "outdoor-rejection": "d11-heat-rejection",
    "facility-overhead": "d01-metrics-and-evidence",
    "capacity-bottleneck": "d15-capacity-ledger",
    "abilene-case": "d15-upgrade-and-evidence",
    "whole-system": "d01-boundaries",
}


def reader_redirect(reader_path):
    mapping = json.dumps(INTRODUCTION_REDIRECTS).replace("<", "\\u003c")
    return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>GIGAWATT — Data center course</title>
<script>let id;try{{id=decodeURIComponent(location.hash.slice(1));}}catch{{id="";}}
const lessons={mapping};
const hash=Object.hasOwn(lessons,id)?"#"+lessons[id]:location.hash;
location.replace("{reader_path}"+location.search+hash);</script>
<p><a href="{reader_path}">Open the GIGAWATT course.</a></p></html>"""


def stage(root=ROOT, destination=None):
    destination = destination or root / "_site"
    destination.mkdir(parents=True, exist_ok=True)
    paths = [Path("README.md")]
    for directory in ("course", "research"):
        paths.extend(p.relative_to(root) for p in (root / directory).glob("*.md"))
        paths.extend(p.relative_to(root) for p in (root / directory).glob("*.json"))
    paths.extend(p.relative_to(root) for p in (root / "course").glob("*.html"))
    paths.extend(
        p.relative_to(root)
        for p in (root / "course/prototypes").glob("*")
        if p.is_file() and p.suffix in {".html", ".js"}
    )
    for directory in ("course/assets", "course/lessons", "research/sources"):
        paths.extend(
            p.relative_to(root) for p in (root / directory).glob("*") if p.is_file()
        )
    paths.extend(
        p.relative_to(root)
        for p in (root / "course/assets/references").glob("*")
        if p.is_file()
    )
    for path in paths:
        target = destination / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / path, target)
    redirect = reader_redirect("course/index.html")
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
    retired_introduction = destination / "diagram/index.html"
    retired_introduction.parent.mkdir(parents=True, exist_ok=True)
    retired_introduction.write_text(
        reader_redirect("../course/index.html"), encoding="utf-8"
    )
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
