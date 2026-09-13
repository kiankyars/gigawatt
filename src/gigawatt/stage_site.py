"""Stage the generated reader, assets and durable reference paths for Pages."""

from __future__ import annotations

import json
import posixpath
import re
import shutil
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

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


# Editable files remain grouped by curriculum concern; publication has one root.
SLIDE_NAMES = {
    "terminology-format": "primer",
    "orientation-format": "overview",
    "workload-format": "workloads",
    "siting-format": "siting",
    "site-format": "site-design",
    "ups-format": "ups",
    "rack-power-format": "rack-power",
    "cooling-format": "cooling",
}
ROOT_PRESENTATIONS = {
    "teach.html": "800v.html",
    "sample.html": "800v-explore.html",
    "sample-notes.html": "800v-notes.html",
}
TEXT_SUFFIXES = {".html", ".js", ".css", ".json", ".md"}
QUOTED_URL = re.compile(
    r"([\"'`])((?:\.\.?/|course/|prototypes/|assets/|lessons/|research/|web/|"
    r"[a-zA-Z0-9_-]+\.(?:html|js|css|json|md|png|webp|jpg|svg))[^\"'`\n<>]*?)\1"
)
MARKDOWN_URL = re.compile(r"(?<=\]\()([^\s)]+)(?=\))")


def public_path(source):
    """Map a repository source path to its stable location in the published site."""
    source = PurePosixPath(source)
    parts = source.parts
    if parts[:2] == ("course", "prototypes"):
        name = source.name
        if source.suffix == ".html":
            name = SLIDE_NAMES.get(source.stem, source.stem.removesuffix("-format")) + ".html"
        return PurePosixPath("slides", *parts[2:-1], name)
    if source == PurePosixPath("course/README.md"):
        return PurePosixPath("SOURCE_INDEX.md")
    if parts[:1] == ("course",):
        if len(parts) == 2 and source.name in ROOT_PRESENTATIONS:
            return PurePosixPath("slides", ROOT_PRESENTATIONS[source.name])
        return PurePosixPath(*parts[1:])
    return source


def published_url(value, source):
    """Rebase local links and module imports when their containing file moves."""
    if not value or value[0] in "#?" or any(c in value for c in "\n\r\t"):
        return value
    try:
        route = urlsplit(value)
    except ValueError:
        return value
    if route.scheme or route.netloc or route.path.startswith("/"):
        return value
    if not (route.path.startswith(("./", "../", "course/", "prototypes/", "assets/", "lessons/", "research/", "web/"))
            or re.fullmatch(r"[a-zA-Z0-9_-]+\.(?:html|js|css|json|md|png|webp|jpg|svg)", route.path)):
        return value
    source = PurePosixPath(source)
    original = PurePosixPath(posixpath.normpath(str(source.parent / route.path)))
    target = public_path(original)
    relative = posixpath.relpath(str(target), str(public_path(source).parent))
    if route.path.endswith("/") and not relative.endswith("/"):
        relative += "/"
    if value.startswith("./") and not relative.startswith("."):
        relative = "./" + relative
    # Empty delimiters can be prefixes for a JavaScript URL concatenation.
    if "?" in value.split("#", 1)[0]:
        relative += "?" + route.query
    if "#" in value:
        relative += "#" + route.fragment
    return relative


def published_text(content, source):
    content = QUOTED_URL.sub(
        lambda match: match[1] + published_url(match[2], source) + match[1], content
    )
    if PurePosixPath(source).suffix == ".md":
        content = MARKDOWN_URL.sub(lambda match: published_url(match[1], source), content)
    return content


def reader_redirect(reader_path, *, introduction=True):
    mapping = json.dumps(INTRODUCTION_REDIRECTS if introduction else {}).replace("<", "\\u003c")
    destination = json.dumps(reader_path).replace("<", "\\u003c")
    return f"""<!doctype html><html lang="en"><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>From Watts to Tokens — Data center course</title>
<script>let id;try{{id=decodeURIComponent(location.hash.slice(1));}}catch{{id="";}}
const lessons={mapping};
const hash=Object.hasOwn(lessons,id)?"#"+lessons[id]:location.hash;
location.replace({destination}+location.search+hash);</script>
<p><a href="{reader_path}">Open From Watts to Tokens.</a></p></html>"""


def stage(root=ROOT, destination=None):
    destination = destination or root / "_site"
    destination.mkdir(parents=True, exist_ok=True)
    paths = {Path("README.md")}
    for directory in ("course", "research"):
        paths.update(p.relative_to(root) for p in (root / directory).glob("*.md"))
        paths.update(p.relative_to(root) for p in (root / directory).glob("*.json"))
    paths.update(p.relative_to(root) for p in (root / "course").glob("*.html"))
    paths.update(
        p.relative_to(root) for p in (root / "course/prototypes").glob("*")
        if p.is_file() and p.suffix in {".html", ".js", ".css"}
    )
    for directory in ("course/lessons", "research/sources"):
        paths.update(p.relative_to(root) for p in (root / directory).glob("*") if p.is_file())
    paths.update(
        p.relative_to(root) for p in (root / "course/assets").rglob("*") if p.is_file()
    )
    for path in sorted(paths):
        if not (root / path).is_file():
            continue
        canonical = Path(public_path(path))
        target = destination / canonical
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix in TEXT_SUFFIXES:
            target.write_text(published_text((root / path).read_text(), path), encoding="utf-8")
        else:
            shutil.copyfile(root / path, target)
        if canonical != path:
            legacy = destination / path
            legacy.parent.mkdir(parents=True, exist_ok=True)
            if path.suffix == ".html":
                relative = posixpath.relpath(str(canonical), str(path.parent))
                legacy.write_text(reader_redirect(relative, introduction=False), encoding="utf-8")
            else:
                # Old research links and imported assets remain durable too.
                shutil.copyfile(root / path, legacy)
    aliases = (
        "course.html", "course_v2.html", "v1.html", "hybrid.html",
        "phase1_generation.html", "phase2_transmission.html", "phase3_campus.html",
        "phase4_building.html", "phase5_compute.html", "phase6_heat.html",
    )
    for name in aliases:
        (destination / name).write_text(reader_redirect("index.html"), encoding="utf-8")
    retired_introduction = destination / "diagram/index.html"
    retired_introduction.parent.mkdir(parents=True, exist_ok=True)
    retired_introduction.write_text(reader_redirect("../index.html"), encoding="utf-8")
    retired_docs = {
        "STRATEGY.md": "COURSE_REVIEW.md",
        "course/COMPANION.md": "../COURSE_REVIEW.md#companion-experience",
        "course/REVIEW_HELP.md": "../PRESENTING.md",
        "course/expansion/AUTHORING.md": "../../TEACHING_STANDARD.md",
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
