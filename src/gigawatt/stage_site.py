"""Stage the current reader, presentations and assets for Pages."""

from __future__ import annotations

import json
import posixpath
import re
import shutil
from pathlib import Path, PurePosixPath
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]

# Editable files remain grouped by curriculum concern; publication has one root.
SLIDE_NAMES = {
    "terminology-format": "primer",
    "orientation-format": "overview",
    "workload-format": "workloads",
    "siting-format": "siting",
    "site-format": "site-design",
    "distribution-format": "distribution",
    "continuity-format": "continuity",
    "rack-energy-format": "rack-energy",
    "networking-format": "networking",
    "storage-format": "storage",
    "cooling-format": "cooling",
}
SHARED_PRESENTATION_MODULES = (
    "electrical-renderer.js", "presentation-renderers.js",
    "reader-models.js", "presentation.css",
)
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


def stage(root=ROOT, destination=None):
    destination = destination or root / "_site"
    catalog = json.loads((root / "course/teaching-sequences.json").read_text())
    presentation_html = {
        Path("course") / urlsplit(chapter["href"]).path
        for presentation in catalog["presentations"]
        for chapter in presentation["chapters"]
    }
    presentation_html.update({
        Path("course/prototypes/presenter.html"),
        Path("course/prototypes/case-studies.html"),
    })
    # Rebuild our generated directory so retired routes cannot survive a later stage.
    if destination.exists() and any(destination.iterdir()):
        if not (destination / ".nojekyll").is_file():
            raise ValueError(f"Refusing to replace a non-staged directory: {destination}")
        shutil.rmtree(destination)
    destination.mkdir(parents=True, exist_ok=True)
    paths = {Path("README.md")}
    for directory in ("course", "research"):
        paths.update(p.relative_to(root) for p in (root / directory).glob("*.md"))
        paths.update(p.relative_to(root) for p in (root / directory).glob("*.json"))
    paths.update(Path("course") / name for name in ("index.html", "domain-map.html", "sample-reading.html"))
    paths.update(
        p.relative_to(root) for p in (root / "course/prototypes").glob("*")
        if p.is_file() and (p.suffix in {".js", ".css"} or p.relative_to(root) in presentation_html)
    )
    paths.update(Path("course/web") / name for name in SHARED_PRESENTATION_MODULES)
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
    (destination / ".nojekyll").touch()
    return destination


if __name__ == "__main__":
    print(f"Staged course at {stage()}")
