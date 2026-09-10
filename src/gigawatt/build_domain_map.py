"""Validate the curriculum graph and generate its HTML and Markdown views."""

from __future__ import annotations

import argparse
import json
import re
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
PLACEHOLDERS = ("__DOMAIN_MAP_JSON__", "__RESEARCH_SOURCES_JSON__")
OUTPUTS = (Path("course/domain-map.html"), Path("course/DOMAIN_MAP.md"))


class DomainMapError(ValueError):
    """The curriculum graph or one of its declared references is invalid."""


def _unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        if key in result:
            raise DomainMapError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def _text(value: object, where: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise DomainMapError(f"{where} must be nonempty text")
    return value


def _records(value: object, where: str, *, empty: bool = False) -> list[dict]:
    if not isinstance(value, list) or (not empty and not value):
        raise DomainMapError(
            f"{where} must be a {'possibly empty' if empty else 'nonempty'} list"
        )
    if any(not isinstance(item, dict) for item in value):
        raise DomainMapError(f"{where} must contain objects")
    return value


def _strings(value: object, where: str, *, empty: bool = True) -> list[str]:
    if not isinstance(value, list) or (not empty and not value):
        raise DomainMapError(
            f"{where} must be a {'possibly empty' if empty else 'nonempty'} list"
        )
    for item in value:
        _text(item, where)
    if len(value) != len(set(value)):
        raise DomainMapError(f"{where} contains duplicate entries")
    return value


def _index(records: list[dict], where: str) -> dict[str, dict]:
    result = {}
    for item in records:
        identifier = _text(item.get("id"), f"{where}.id")
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", identifier):
            raise DomainMapError(f"{where}: unsafe ID {identifier!r}")
        if identifier in result:
            raise DomainMapError(f"Duplicate {where} ID: {identifier}")
        result[identifier] = item
    return result


def _refs(value: object, known: dict, where: str, *, empty: bool = True) -> list[str]:
    values = _strings(value, where, empty=empty)
    unknown = set(values) - known.keys()
    if unknown:
        raise DomainMapError(f"{where}: unknown reference(s) {sorted(unknown)}")
    return values


def validate_map(domain_map: object, research: object, lessons: object) -> dict:
    """Validate references and prerequisites; derive domain sources from the catalog."""
    if (
        not isinstance(domain_map, dict)
        or not isinstance(research, dict)
        or not isinstance(lessons, dict)
    ):
        raise DomainMapError(
            "The domain map, research catalog, and lessons must be objects"
        )
    result = deepcopy(domain_map)
    for key in (
        "title",
        "subtitle",
        "as_of",
        "status",
    ):
        _text(result.get(key), key)
    lanes = _index(_records(result.get("lanes"), "lanes"), "lane")
    domains = _index(_records(result.get("domains"), "domains"), "domain")
    sources = _index(_records(research.get("sources"), "sources", empty=True), "source")
    baseline = _index(_records(lessons.get("lessons"), "lessons"), "lesson")
    for lane in lanes.values():
        for key in ("title", "description"):
            _text(lane.get(key), f"{lane['id']}.{key}")
    for lesson in baseline.values():
        _text(lesson.get("title"), f"{lesson['id']}.title")
    objectives = {}
    for domain in domains.values():
        did = domain["id"]
        for key in (
            "title",
            "lane",
            "question",
            "purpose",
            "worked_example",
            "tradeoff",
            "failure",
        ):
            _text(domain.get(key), f"{did}.{key}")
        if domain["lane"] not in lanes:
            raise DomainMapError(f"{did}: unknown lane {domain['lane']}")
        _strings(domain.get("scope"), f"{did}.scope", empty=False)
        _refs(domain.get("prerequisites"), domains, f"{did}.prerequisites")
        if not isinstance(domain.get("visual"), dict):
            raise DomainMapError(f"{did}.visual must be an object")
        for key in ("title", "prediction", "interaction", "boundary"):
            _text(domain["visual"].get(key), f"{did}.visual.{key}")
        for objective in _records(domain.get("objectives"), f"{did}.objectives"):
            oid = _text(objective.get("id"), f"{did}.objective.id")
            if oid in objectives:
                raise DomainMapError(f"Duplicate objective ID: {oid}")
            objectives[oid] = objective
            for key in ("capability", "assessment"):
                _text(objective.get(key), f"{oid}.{key}")
            if objective.get("baseline_coverage") not in {"partial", "missing"}:
                raise DomainMapError(
                    f"{oid}: baseline coverage must be partial or missing"
                )
            _refs(
                objective.get("baseline_lessons"), baseline, f"{oid}.baseline_lessons"
            )
            if (
                objective["baseline_coverage"] == "partial"
                and not objective["baseline_lessons"]
            ):
                raise DomainMapError(f"{oid}: partial coverage needs a baseline lesson")
        domain["source_ids"] = []
    reused = {
        lid
        for objective in objectives.values()
        for lid in objective["baseline_lessons"]
    }
    if reused != set(baseline):
        raise DomainMapError(
            f"Baseline lessons without a migration decision: {sorted(set(baseline) - reused)}"
        )
    unused_lanes = set(lanes) - {domain["lane"] for domain in domains.values()}
    if unused_lanes:
        raise DomainMapError(f"Lanes without domains: {sorted(unused_lanes)}")
    for source in sources.values():
        sid = source["id"]
        for key in ("title", "publisher", "kind", "review_status", "use"):
            _text(source.get(key), f"{sid}.{key}")
        _text(source.get("caution") or source.get("limits"), f"{sid}.caution")
        url = _text(source.get("url"), f"{sid}.url")
        parsed = urlsplit(url)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.netloc
            or any(c.isspace() for c in url)
        ):
            raise DomainMapError(f"{sid}: source URL must be an absolute web URL")
        for did in _refs(source.get("domains"), domains, f"{sid}.domains"):
            domains[did]["source_ids"].append(sid)
    visited, visiting = set(), []

    def visit(did: str) -> None:
        if did in visiting:
            raise DomainMapError(f"Prerequisite cycle: {' -> '.join(visiting + [did])}")
        if did in visited:
            return
        visiting.append(did)
        for prerequisite in domains[did]["prerequisites"]:
            visit(prerequisite)
        visiting.pop()
        visited.add(did)

    for did in domains:
        visit(did)
    for collection, required in (
        ("paths", ("title", "purpose")),
        ("sequence", ("title", "outcome")),
        ("capstones", ("title", "brief", "deliverable", "assessment")),
    ):
        items = _index(_records(result.get(collection), collection), collection)
        for item in items.values():
            for key in required:
                _text(item.get(key), f"{item['id']}.{key}")
            _refs(item.get("domains"), domains, f"{item['id']}.domains", empty=False)
    ordered = [did for act in result["sequence"] for did in act["domains"]]
    if len(ordered) != len(set(ordered)) or set(ordered) != set(domains):
        raise DomainMapError("Teaching sequence must include every domain exactly once")
    positions = {did: i for i, did in enumerate(ordered)}
    for did, domain in domains.items():
        for prerequisite in domain["prerequisites"]:
            if positions[prerequisite] >= positions[did]:
                raise DomainMapError(
                    f"Teaching sequence places {did} before prerequisite {prerequisite}"
                )
    result["baseline_lessons"] = [
        {"id": lesson["id"], "title": lesson["title"]} for lesson in baseline.values()
    ]
    return result


class _Links(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.targets: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self.targets.extend(
                value for key, value in attrs if key == "href" and value
            )


def validate_template_links(template: str, root: Path) -> None:
    """Check static local document links without fetching any external resource."""
    parser = _Links()
    parser.feed(template)
    for target in parser.targets:
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc or not parsed.path:
            continue
        path = (root / "course" / unquote(parsed.path)).resolve()
        if not path.is_relative_to(root.resolve()):
            raise DomainMapError(f"Template link escapes the repository: {target}")
        if path in {(root / output).resolve() for output in OUTPUTS}:
            continue
        if not path.is_file():
            raise DomainMapError(f"Template link does not exist: {target}")


def _md(value: str) -> str:
    return (
        value.replace("\\", "\\\\")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("[", "\\[")
        .replace("]", "\\]")
    )


def render_markdown(domain_map: dict, research: dict) -> str:
    """Render the complete editable graph without inventing a second curriculum."""
    m = domain_map
    domains = {d["id"]: d for d in m["domains"]}
    lessons = {l["id"]: l["title"] for l in m["baseline_lessons"]}
    sources = {s["id"]: s for s in research["sources"]}
    lines = [
        f"# {_md(m['title'])}",
        "",
        "<!-- Generated from domain-map.json, research-sources.json and lessons.json. Edit those sources; run uv run gigawatt-map. -->",
        "",
        f"As of **{_md(m['as_of'])}**. {_md(m['status'])}",
        "",
        _md(m["subtitle"]),
        "",
        "[Interactive map](domain-map.html) · [Course review](COURSE_REVIEW.md) · [Source index](../research/INDEX.md) · [Research library](../research/README.md)",
        "",
        "## How to read this map",
        "",
        "The [filled-in course template](COURSE_REVIEW.md) owns audience, overall scope, exclusions, runtime and production priorities. This map owns the detailed objectives, prerequisites, teaching sequence and capstone briefs within that design.",
        "",
        "[Current authored coverage](EXPANDED_COURSE.md#objective-to-lesson-coverage) is generated from the lesson records. Presentation adaptation and review status are tracked in the course template.",
        "",
        "## Evidence and historical introduction coverage",
        "",
        "Source-to-domain mappings are derived from `research-sources.json` → `sources[].domains`. They identify research connections, not verified support for every objective.",
        "",
    ]
    for status, definition in m.get("baseline_coverage_definition", {}).items():
        lines.append(f"- **{_md(status)}:** {_md(definition)}")
    lines.extend(["", "## System lanes", ""])
    for lane in m["lanes"]:
        lines.extend([f"### {_md(lane['title'])}", "", _md(lane["description"]), ""])
        for domain in m["domains"]:
            if domain["lane"] == lane["id"]:
                lines.append(
                    f"- [{domain['id']} — {_md(domain['title'])}](#{domain['id'].lower()})"
                )
        lines.append("")
    lines.extend(
        [
            "## Proposed teaching sequence",
            "",
            "Domain IDs are stable references, not chapter numbers. This sequence respects prerequisites; runtime is not yet allocated.",
            "",
        ]
    )
    for act in m["sequence"]:
        route = " → ".join(f"[{did}](#{did.lower()})" for did in act["domains"])
        lines.extend(
            [
                f"### {act['id']} — {_md(act['title'])}",
                "",
                route,
                "",
                _md(act["outcome"]),
                "",
            ]
        )
    lines.extend(["## Domain teaching plans", ""])
    for domain in m["domains"]:
        did = domain["id"]
        lines.extend(
            [
                f'<a id="{did.lower()}"></a>',
                "",
                f"### {did} — {_md(domain['title'])}",
                "",
                f"**Central question:** {_md(domain['question'])}",
                "",
                _md(domain["purpose"]),
                "",
                "**Included scope:**",
                "",
            ]
        )
        lines.extend(f"- {_md(item)}" for item in domain["scope"])
        prerequisites = (
            ", ".join(
                f"[{p} — {_md(domains[p]['title'])}](#{p.lower()})"
                for p in domain["prerequisites"]
            )
            or "None in this map."
        )
        lines.extend(
            [
                "",
                f"**Prerequisites:** {prerequisites}",
                "",
                "**Learning objectives and assessments:**",
                "",
            ]
        )
        for objective in domain["objectives"]:
            baseline = (
                "; ".join(
                    f"`{lid}` — {_md(lessons[lid])}"
                    for lid in objective["baseline_lessons"]
                )
                or "No existing lesson mapped."
            )
            lines.extend(
                [
                    f"#### {objective['id']}",
                    "",
                    _md(objective["capability"]),
                    "",
                    f"**Assessment:** {_md(objective['assessment'])}",
                    "",
                    f"**Historical introduction coverage:** {objective['baseline_coverage']}. {baseline}",
                    "",
                ]
            )
        visual = domain["visual"]
        lines.extend(
            [
                f"**Visual plan: {_md(visual['title'])}**",
                "",
                f"- Prediction: {_md(visual['prediction'])}",
                f"- Interaction: {_md(visual['interaction'])}",
                f"- Model boundary: {_md(visual['boundary'])}",
                "",
                f"**Worked example:** {_md(domain['worked_example'])}",
                "",
                f"**Design tradeoff:** {_md(domain['tradeoff'])}",
                "",
                f"**Failure or maintenance scenario:** {_md(domain['failure'])}",
                "",
                "**Research connections:**",
                "",
            ]
        )
        for sid in domain["source_ids"]:
            source = sources[sid]
            lines.append(
                f"- [{sid} — {_md(source['title'])}]({source['url']}) · `{source['review_status']}` · [local note](../research/sources/{sid}.md)"
            )
        if not domain["source_ids"]:
            lines.append(
                "No source records mapped yet; this is an explicit research gap."
            )
        lines.append("")
    lines.extend(["## Paths through the system", ""])
    for path in m["paths"]:
        lines.extend(
            [
                f"### {_md(path['title'])}",
                "",
                " → ".join(f"[{did}](#{did.lower()})" for did in path["domains"]),
                "",
                _md(path["purpose"]),
                "",
            ]
        )
    lines.extend(["## Proposed capstones", ""])
    for capstone in m["capstones"]:
        lines.extend(
            [
                f"### {capstone['id']} — {_md(capstone['title'])}",
                "",
                _md(capstone["brief"]),
                "",
                "Domains: "
                + ", ".join(f"[{did}](#{did.lower()})" for did in capstone["domains"]),
                "",
                f"**Deliverable:** {_md(capstone['deliverable'])}",
                "",
                f"**Assessment:** {_md(capstone['assessment'])}",
                "",
            ]
        )
    lines.extend(
        [
            "## Historical introduction reuse",
            "",
            "Every lesson in the retained 22-lesson introduction has a reuse location. These historical mappings do not describe the current authored course or establish completion.",
            "",
            "| Introduction lesson | Objectives |",
            "| --- | --- |",
        ]
    )
    for lid, title in lessons.items():
        targets = [
            o["id"]
            for d in m["domains"]
            for o in d["objectives"]
            if lid in o["baseline_lessons"]
        ]
        lines.append(f"| `{lid}` — {_md(title)} | {', '.join(targets)} |")
    return "\n".join(lines).rstrip() + "\n"


def build(root: Path = ROOT) -> dict[Path, str]:
    try:
        loaded = [
            json.loads(
                (root / "course" / name).read_text(encoding="utf-8"),
                object_pairs_hook=_unique_object,
            )
            for name in ("domain-map.json", "research-sources.json", "lessons.json")
        ]
        template = (root / "course" / "web" / "domain-map.html").read_text(
            encoding="utf-8"
        )
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise DomainMapError(f"Cannot read domain-map source: {error}") from error
    domain_map, research, lessons = loaded
    domain_map = validate_map(domain_map, research, lessons)
    for placeholder in PLACEHOLDERS:
        if template.count(placeholder) != 1:
            raise DomainMapError(f"Template must contain {placeholder} exactly once")
    validate_template_links(template, root)
    values = {
        placeholder: json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        .replace("<", "\\u003c")
        .replace("\u2028", "\\u2028")
        .replace("\u2029", "\\u2029")
        for placeholder, value in zip(PLACEHOLDERS, (domain_map, research))
    }
    html = (
        re.sub(
            "|".join(map(re.escape, PLACEHOLDERS)),
            lambda match: values[match[0]],
            template,
        ).rstrip()
        + "\n"
    )
    return {OUTPUTS[0]: html, OUTPUTS[1]: render_markdown(domain_map, research)}


def write_or_check(root: Path, outputs: dict[Path, str], *, check: bool) -> None:
    if check:
        stale = [
            str(relative)
            for relative, content in outputs.items()
            if not (root / relative).is_file()
            or (root / relative).read_bytes() != content.encode("utf-8")
        ]
        if stale:
            raise DomainMapError(
                f"Generated domain-map files are stale: {', '.join(stale)}; run uv run gigawatt-map"
            )
        return
    for relative, content in outputs.items():
        destination = root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Validate references and require exact generated bytes",
    )
    args = parser.parse_args()
    try:
        outputs = build()
        write_or_check(ROOT, outputs, check=args.check)
        print(
            "Domain map validated; HTML and Markdown are current."
            if args.check
            else "Built course/domain-map.html and course/DOMAIN_MAP.md"
        )
    except (DomainMapError, OSError) as error:
        parser.exit(1, f"Domain map build failed: {error}\n")


if __name__ == "__main__":
    main()
