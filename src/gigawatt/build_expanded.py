"""Build the expanded course reader and Markdown from authored lesson records."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import posixpath
import re
import sys
from copy import deepcopy
from pathlib import Path
from urllib.parse import urlsplit

from gigawatt.build_presentation import presentation_outputs
from gigawatt.research import canonical_url

ROOT = Path(__file__).resolve().parents[2]
PARTS = (
    "foundations-power.json",
    "racks-compute-heat.json",
    "heat-delivery-operations.json",
    "capstones.json",
    "grid-queues.json",
)
IMAGES = (
    "campus-cutaway.png",
    "rack-anatomy.png",
    "cooling-cutaway.png",
    "power-equipment.png",
    "network-equipment.png",
)
# While False, a repeated glossary term (case-insensitive) only prints a warning and
# the first definition in reading order is kept. Set True once the duplicates are merged.
FAIL_ON_DUPLICATE_TERMS = True


class ExpansionError(ValueError):
    """A teaching contract or generated artifact is incomplete."""


def read(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ExpansionError(f"{label}: expected nonempty text")
    return value


def paragraphs(value, label):
    values = value if isinstance(value, list) else [value]
    return [text(v, label) for v in values]


def flatten(value):
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return " ".join(flatten(v) for v in value)
    if isinstance(value, dict):
        return " ".join(flatten(v) for v in value.values())
    return ""


def reader_lab_types(root=ROOT):
    """The lab types course/web/reader.js renders, read from its `type === "..."` branches.

    A lesson may name only these, or "none" to hide its lab, so it cannot ask for a lab
    the reader would silently leave blank.
    """
    source = (root / "course/web/reader.js").read_text(encoding="utf-8")
    types = frozenset(re.findall(r'\btype === "([a-z][a-z0-9-]*)"', source))
    if not types:
        raise ExpansionError("No lab types found in course/web/reader.js")
    return types


def validate_lab(lesson, lab_types):
    """Check the optional lab and practice fields that pass through to the reader unchanged."""
    lid = lesson["id"]
    if "lab" in lesson:
        lab = lesson["lab"]
        if not isinstance(lab, str) or (lab != "none" and lab not in lab_types):
            raise ExpansionError(
                f"{lid}: lab must be one of {', '.join(sorted(lab_types))} or none"
            )
    if "lab_params" in lesson:
        params = lesson["lab_params"]
        if lesson.get("lab") in (None, "none"):
            raise ExpansionError(f"{lid}: lab_params needs an explicit lab type")
        if not isinstance(params, dict) or not params:
            raise ExpansionError(f"{lid}: lab_params must be a nonempty object")
        for key, value in params.items():
            if not re.fullmatch(r"[a-z][a-z0-9-]*", key):
                raise ExpansionError(f"{lid}: unsafe lab_params key: {key}")
            number = isinstance(value, (int, float)) and not isinstance(value, bool)
            if not (
                (number and math.isfinite(value))
                or (isinstance(value, str) and value.strip())
            ):
                raise ExpansionError(
                    f"{lid}: lab_params.{key} must be a finite number or nonempty text"
                )
    if "optional" in lesson and not isinstance(lesson["optional"], bool):
        raise ExpansionError(f"{lid}: optional must be true or false")


def normalize(raw, catalog_by_url, known_objectives, lab_types=None):
    lesson = deepcopy(raw)
    for key in ("id", "domain", "title", "question", "summary", "takeaway"):
        text(lesson.get(key), f"lesson.{key}")
    if not re.fullmatch(r"[a-z0-9][a-z0-9-]+", lesson["id"]):
        raise ExpansionError(f"Unsafe lesson ID: {lesson['id']}")
    objectives = lesson.get("objectives")
    if (
        not isinstance(objectives, list)
        or not objectives
        or len(set(objectives)) != len(objectives)
        or not set(objectives) <= known_objectives
    ):
        raise ExpansionError(f"{lesson['id']}: invalid objective references")
    if lesson["domain"] != "capstone" and any(
        not o.startswith(lesson["domain"] + ".") for o in objectives
    ):
        raise ExpansionError(f"{lesson['id']}: objective outside its domain")
    if not isinstance(lesson.get("sections"), list) or len(lesson["sections"]) < 2:
        raise ExpansionError(
            f"{lesson['id']}: a lesson needs developed explanatory sections"
        )
    for section in lesson["sections"]:
        text(section.get("heading"), "section.heading")
        section["paragraphs"] = paragraphs(
            section.get("paragraphs"), "section.paragraphs"
        )
        for figure in section.get("figures", []):
            asset = text(figure.get("asset"), "figure.asset")
            if not re.fullmatch(r"references/[a-z0-9-]+\.(?:png|jpeg|jpg|svg|webp)", asset):
                raise ExpansionError(f"Unsafe reference figure path: {asset}")
            for field in ("alt", "caption", "source_title"):
                text(figure.get(field), f"figure.{field}")
            url = canonical_url(text(figure.get("source_url"), "figure.source_url"))
            if url not in catalog_by_url:
                raise ExpansionError(
                    f"{lesson['id']}: figure source not in library: {url}"
                )
    example = lesson.get("example", lesson.get("worked_example"))
    if not isinstance(example, dict):
        raise ExpansionError(f"{lesson['id']}: missing worked example")
    steps = example.get("steps")
    if not isinstance(steps, list) or len(steps) < 2:
        raise ExpansionError(f"{lesson['id']}: example needs intermediate reasoning")
    lesson["worked_example"] = {
        "title": text(example.get("title"), "example.title"),
        "givens": paragraphs(
            example.get("assumptions", example.get("givens")), "example.givens"
        ),
        "steps": [
            " — ".join(
                text(s[k], f"step.{k}")
                for k in ("label", "expression", "explanation")
                if k in s
            )
            if isinstance(s, dict)
            else text(s, "step")
            for s in steps
        ],
        "result": text(example.get("result"), "example.result"),
        "boundary": text(example.get("boundary"), "example.boundary"),
    }
    for key in ("tradeoff", "failure"):
        # Optional slots: a lesson keeps them only where they carry teaching content.
        if key not in lesson:
            continue
        value = lesson[key]
        if isinstance(value, dict):
            if not value:
                raise ExpansionError(f"{lesson['id']}: {key} needs content when present")
            value = [
                f"{name.replace('_', ' ').capitalize()}: {text(v, key)}"
                for name, v in value.items()
            ]
        if isinstance(value, list) and not value:
            raise ExpansionError(f"{lesson['id']}: {key} needs content when present")
        lesson[key] = paragraphs(value, key)
    validate_lab(lesson, reader_lab_types() if lab_types is None else lab_types)
    p = lesson.get("practice")
    if not isinstance(p, dict):
        raise ExpansionError(f"{lesson['id']}: missing transfer practice")
    lesson["practice"] = {
        "question": text(p.get("question"), "practice.question"),
        "answer": text(p.get("answer"), "practice.answer"),
        "explanation": paragraphs(
            p.get("reasoning", p.get("explanation")), "practice.explanation"
        ),
    }
    source_records = lesson.get("sources")
    if not isinstance(source_records, list) or not source_records:
        raise ExpansionError(f"{lesson['id']}: missing source reading records")
    lesson["source_ids"], lesson["source_notes"] = [], []
    for source in source_records:
        url = canonical_url(text(source.get("url"), "source.url"))
        if url not in catalog_by_url:
            raise ExpansionError(f"{lesson['id']}: source not yet in library: {url}")
        identifier = catalog_by_url[url]["id"]
        if identifier not in lesson["source_ids"]:
            lesson["source_ids"].append(identifier)
        reviewed_on = text(source.get("reviewed_on"), "source.reviewed_on")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", reviewed_on):
            raise ExpansionError(
                f"{lesson['id']}: source.reviewed_on must be a YYYY-MM-DD date"
            )
        lesson["source_notes"].append(
            {
                "id": identifier,
                "claim": text(source.get("claim"), "source.claim"),
                "reviewed_on": reviewed_on,
                "limits": text(source.get("limits"), "source.limits"),
            }
        )
    lesson["word_count"] = len(
        flatten(
            {
                k: lesson.get(k)
                for k in (
                    "title",
                    "summary",
                    "sections",
                    "worked_example",
                    "tradeoff",
                    "failure",
                    "practice",
                    "takeaway",
                )
            }
        ).split()
    )
    for key in ("example", "sources"):
        lesson.pop(key, None)
    return lesson


def chapter_label(chapter):
    """The name learners see: "5. Physical site, buildings and safety" or a case study's title."""
    return (
        f"{chapter['number']}. {chapter['title']}"
        if "number" in chapter
        else chapter["title"]
    )


def attach_checkins(raw, lessons, chapters):
    """Validate one check-in per chapter and point it at the next lesson in course order.

    Every chapter with reading ends with a check-in, except the final optional exercises.
    A check-in names the chapter it closes and the chapter that follows it; the builder
    resolves the continue target from the chapter order, so split chapters and unnumbered
    case studies are never skipped. The attached record carries ``chapter``, ``domain``,
    ``next_chapter``, ``next_lesson``, ``next_title`` and ``next_label`` (the next
    chapter's display name). ``next_domain`` repeats ``next_chapter``: the reader resolves
    it as a chapter ID, which equals the domain ID except for split and case-study chapters.
    """
    if not isinstance(raw, dict) or raw.get("version") != 1:
        raise ExpansionError("Chapter check-ins: expected version 1")
    records = raw.get("checkins")
    if not isinstance(records, list):
        raise ExpansionError("Chapter check-ins: expected a list of checkins")
    fields = {
        "chapter",
        "title",
        "scenario",
        "prompt",
        "answer",
        "explanation",
        "next_chapter",
        "bridge",
    }
    by_chapter = {}
    for record in records:
        if not isinstance(record, dict) or set(record) != fields:
            raise ExpansionError("Chapter check-in: missing or unexpected fields")
        checkin = deepcopy(record)
        for key in fields - {"explanation"}:
            text(checkin[key], f"chapter check-in.{key}")
        if not isinstance(checkin["explanation"], list) or not checkin["explanation"]:
            raise ExpansionError("Chapter check-in: expected explanatory paragraphs")
        checkin["explanation"] = paragraphs(
            checkin["explanation"], "chapter check-in.explanation"
        )
        if checkin["chapter"] in by_chapter:
            raise ExpansionError(f"Duplicate chapter check-in: {checkin['chapter']}")
        by_chapter[checkin["chapter"]] = checkin
    closing = [c for c in chapters if c["lesson_ids"] and c["domain"] != "capstone"]
    if set(by_chapter) != {c["id"] for c in closing}:
        raise ExpansionError(
            "Chapter check-ins must cover every chapter with reading exactly once"
        )
    by_id = {l["id"]: l for l in lessons}
    order = [lid for chapter in chapters for lid in chapter["lesson_ids"]]
    chapter_of = {lid: chapter for chapter in chapters for lid in chapter["lesson_ids"]}
    for chapter in closing:
        checkin = by_chapter[chapter["id"]]
        last = chapter["lesson_ids"][-1]
        position = order.index(last)
        if position + 1 >= len(order):
            raise ExpansionError(f"{chapter['id']}: check-in has no following lesson")
        following = by_id[order[position + 1]]
        next_chapter = chapter_of[following["id"]]
        if checkin["next_chapter"] != next_chapter["id"]:
            raise ExpansionError(
                f"{chapter['id']}: check-in bridge must follow course sequence"
                f" (expected {next_chapter['id']})"
            )
        checkin.update(
            {
                "domain": chapter["domain"],
                "next_domain": next_chapter["id"],
                "next_lesson": following["id"],
                "next_title": following["title"],
                "next_label": chapter_label(next_chapter),
            }
        )
        by_id[last]["domain_checkin"] = checkin


def teaching_chapters(raw, domain_map, lessons, root=ROOT):
    """Resolve available teaching sequences against the single curriculum order.

    Coverage describes the scope of a presentation, not its review or rehearsal
    status. A chapter without a presentation still has its authored reading.
    """
    if (not isinstance(raw, dict) or not {"version", "presentations"} <= set(raw)
            or set(raw) - {"version", "presentations", "chapter_splits", "additional_chapters"}):
        raise ExpansionError("Teaching catalog: missing or unexpected fields")
    if raw["version"] != 1 or not isinstance(raw["presentations"], list):
        raise ExpansionError("Teaching catalog: expected version 1 and presentations")
    domains = {d["id"]: d for d in domain_map["domains"]}
    sequence = [did for act in domain_map["sequence"] for did in act["domains"]]
    all_domains = sequence + domain_map.get("reference_domains", [])
    if len(all_domains) != len(set(all_domains)) or set(all_domains) != set(domains):
        raise ExpansionError(
            "Teaching chapters: sequence and further reading must contain every domain once"
        )
    titles = {
        **{did: domain["title"] for did, domain in domains.items()},
        "primer": "Primer",
        "D01": "Data center overview",
        "D02": "Workloads and requirements",
        "capstone": "Putting an AI Factory Together",
    }
    splits = raw.get("chapter_splits", {})
    if not isinstance(splits, dict) or set(splits) - set(sequence):
        raise ExpansionError("Teaching chapter splits: expected domains from the curriculum")
    additions = raw.get("additional_chapters", [])
    if not isinstance(additions, list):
        raise ExpansionError("Additional chapters: expected a list")
    lesson_domains = {lesson["id"]: lesson["domain"] for lesson in lessons}
    additional_lessons = set()
    for part in additions:
        if (not isinstance(part, dict)
                or set(part) != {"id", "domain", "title", "lesson_ids"}
                or part["domain"] not in sequence):
            raise ExpansionError("Additional chapters: invalid fields or domain")
        ids = part["lesson_ids"]
        if (not isinstance(ids, list) or not ids
                or any(not isinstance(lid, str) for lid in ids)
                or len(ids) != len(set(ids))
                or additional_lessons.intersection(ids)
                or any(lesson_domains.get(lid) != part["domain"] for lid in ids)):
            raise ExpansionError("Additional chapters: lessons must exist in their domain and occur once")
        additional_lessons.update(ids)
    chapters = []
    chapter_ids = set()
    for did in ["primer", *sequence, "capstone"]:
        lesson_ids = [l["id"] for l in lessons if l["domain"] == did and l["id"] not in additional_lessons]
        parts = splits.get(did, [{"id": did, "title": titles[did], "lesson_ids": lesson_ids}])
        if did in splits:
            if not isinstance(parts, list) or len(parts) < 2:
                raise ExpansionError(f"{did}: a chapter split needs at least two parts")
            assigned = []
            for part in parts:
                if not isinstance(part, dict) or set(part) != {"id", "title", "lesson_ids"}:
                    raise ExpansionError(f"{did}: invalid chapter split fields")
                if (not isinstance(part["lesson_ids"], list) or not part["lesson_ids"]
                        or any(not isinstance(lid, str) for lid in part["lesson_ids"])):
                    raise ExpansionError(f"{did}: chapter split needs lesson IDs")
                assigned.extend(part["lesson_ids"])
            if len(assigned) != len(set(assigned)) or set(assigned) != set(lesson_ids):
                raise ExpansionError(f"{did}: split chapters must partition the domain lessons exactly once")
            if parts[0]["id"] != did:
                raise ExpansionError(f"{did}: first split chapter must preserve the domain ID")
        for part in parts:
            identifier = text(part["id"], "chapter.id")
            if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", identifier):
                raise ExpansionError(f"Unsafe chapter ID: {identifier}")
            if identifier in chapter_ids or (identifier != did and identifier in domains):
                raise ExpansionError(f"Duplicate or conflicting chapter ID: {identifier}")
            chapter_ids.add(identifier)
            chapters.append({
                "id": identifier,
                "domain": did,
                "number": len(chapters) + 1,
                "title": text(part["title"], "chapter.title"),
                "lesson_ids": part["lesson_ids"],
                "presentations": [],
            })
    for part in additions:
        identifier = text(part["id"], "chapter.id")
        if not re.fullmatch(r"[A-Za-z][A-Za-z0-9-]*", identifier):
            raise ExpansionError(f"Unsafe chapter ID: {identifier}")
        if identifier in chapter_ids or identifier in domains:
            raise ExpansionError(f"Duplicate or conflicting chapter ID: {identifier}")
        chapter_ids.add(identifier)
        # Case studies are unnumbered and follow their domain, so recorded chapter numbers never move.
        after = max(i for i, chapter in enumerate(chapters) if chapter["domain"] == part["domain"])
        chapters.insert(after + 1, {**part, "presentations": [], "additional": True})
    by_id = {chapter["id"]: chapter for chapter in chapters}
    seen = set()
    for presentation in raw["presentations"]:
        if not isinstance(presentation, dict) or set(presentation) != {
            "id",
            "title",
            "chapters",
        }:
            raise ExpansionError("Teaching presentation: missing or unexpected fields")
        pid = text(presentation["id"], "teaching presentation.id")
        if not re.fullmatch(r"[a-z][a-z0-9-]*", pid):
            raise ExpansionError(f"Unsafe teaching presentation ID: {pid}")
        if pid in seen:
            raise ExpansionError(f"Duplicate teaching presentation: {pid}")
        seen.add(pid)
        title = text(presentation["title"], "teaching presentation.title")
        placements = presentation["chapters"]
        if not isinstance(placements, list) or not placements:
            raise ExpansionError(f"{pid}: expected at least one chapter placement")
        placed = set()
        for placement in placements:
            if not isinstance(placement, dict) or set(placement) != {
                "id",
                "href",
                "coverage",
            }:
                raise ExpansionError(f"{pid}: invalid chapter placement fields")
            did = text(placement["id"], f"{pid}.chapter.id")
            if did not in by_id:
                raise ExpansionError(f"{pid}: unknown teaching chapter: {did}")
            if did in placed:
                raise ExpansionError(f"{pid}: duplicate presentation in chapter: {did}")
            placed.add(did)
            if not isinstance(placement["coverage"], str) or placement[
                "coverage"
            ] not in {"chapter", "selected"}:
                raise ExpansionError(f"{pid}: coverage must be chapter or selected")
            href = text(placement["href"], f"{pid}.href")
            route = urlsplit(href)
            if (
                route.scheme
                or route.netloc
                or not re.fullmatch(r"(?:[a-z0-9-]+/)*[a-z0-9-]+\.html", route.path)
                or (route.fragment and not re.fullmatch(r"[a-z0-9-]+", route.fragment))
            ):
                raise ExpansionError(
                    f"{pid}: expected a local course presentation href"
                )
            if not (root / "course" / route.path).is_file():
                raise ExpansionError(
                    f"{pid}: missing teaching presentation: {route.path}"
                )
            by_id[did]["presentations"].append(
                {
                    "id": pid,
                    "title": title,
                    "href": href,
                    "coverage": placement["coverage"],
                }
            )
    return chapters


def presentation_identities(chapters):
    """Build small shared labels so decks never maintain their own chapter numbers."""
    presentations = {}
    for chapter in chapters:
        for presentation in chapter["presentations"]:
            item = presentations.setdefault(
                presentation["id"], {"title": presentation["title"], "numbers": []}
            )
            if "number" in chapter:
                item["numbers"].append(chapter["number"])
    labels = {}
    for pid, item in presentations.items():
        numbers = item["numbers"]
        if len(numbers) > 1 and numbers == list(range(numbers[0], numbers[-1] + 1)):
            ordinal = f"{numbers[0]}–{numbers[-1]}"
        else:
            ordinal = ", ".join(str(number) for number in numbers)
        labels[pid] = f"{ordinal}. {item['title']}" if numbers else item["title"]
    return (
        "// Generated from teaching-sequences.json and domain-map.json.\n"
        "// Run uv run gigawatt-expand; chapter numbering follows the curriculum order.\n"
        "export const presentationLabels = Object.freeze("
        + json.dumps(labels, ensure_ascii=False, indent=2).replace("<", "\\u003c")
        + ");\n"
        + "export const presentationRoutes = Object.freeze("
        + json.dumps(
            presentation_routes(chapters), ensure_ascii=False, indent=2
        ).replace("<", "\\u003c")
        + ");\n"
    )


def presentation_routes(chapters):
    """Derive chapter handoffs, relative to the generated navigation module."""
    presentations = {}
    for index, chapter in enumerate(chapters):
        for presentation in chapter["presentations"]:
            item = presentations.setdefault(presentation["id"], {"paths": set()})
            item["paths"].add(urlsplit(presentation["href"]).path)
            item["last_chapter"] = index
    routes = []
    for item in presentations.values():
        next_index = item["last_chapter"] + 1
        destination = None
        if next_index < len(chapters):
            chapter = chapters[next_index]
            if chapter["presentations"]:
                href = chapter["presentations"][0]["href"]
                kind = "slides"
            else:
                href = "index.html"
                if chapter["lesson_ids"]:
                    href += "#" + chapter["lesson_ids"][0]
                kind = "reading"
            destination = {
                **({"number": chapter["number"]} if "number" in chapter else {}),
                "title": chapter["title"],
                "href": posixpath.relpath(href, "prototypes"),
                "kind": kind,
            }
        for path in sorted(item["paths"]):
            routes.append({"path": posixpath.relpath(path, "prototypes"), "next": destination})
    return routes


def load_course(root=ROOT):
    domain_map = read(root / "course/domain-map.json")
    catalog = read(root / "course/research-sources.json")["sources"]
    known = {o["id"] for d in domain_map["domains"] for o in d["objectives"]}
    by_url = {canonical_url(s["url"]): s for s in catalog}
    raw_lessons = []
    for name in PARTS:
        part = read(root / "course/expansion" / name)
        raw_lessons.extend(
            {**lesson, "source_path": f"course/expansion/{name}"}
            for lesson in (part["lessons"] if isinstance(part, dict) else part)
        )
    lab_types = reader_lab_types(root)
    lessons = [normalize(l, by_url, known, lab_types) for l in raw_lessons]
    ids = [l["id"] for l in lessons]
    if len(ids) != len(set(ids)):
        raise ExpansionError("Duplicate authored lesson IDs")
    if known - {
        o for l in lessons if l["domain"] != "capstone" for o in l["objectives"]
    }:
        raise ExpansionError("Some domain objectives have no authored lesson")
    sequence = [did for act in domain_map["sequence"] for did in act["domains"]]
    references = domain_map.get("reference_domains", [])
    order = {did: i for i, did in enumerate(sequence + ["capstone"] + references)}
    if any(l["domain"] not in order for l in lessons):
        raise ExpansionError("Unknown lesson domain")
    lessons.sort(key=lambda l: order[l["domain"]])
    # Chapter 16 may also hold companion reading, such as the Abilene case, that is not
    # one of the domain map's capstone exercises; only lessons with a capstone_id count.
    expected_capstones = {c["id"] for c in domain_map["capstones"]}
    authored_capstones = [
        l["capstone_id"]
        for l in lessons
        if l["domain"] == "capstone" and l.get("capstone_id") is not None
    ]
    if (
        len(authored_capstones) != len(set(authored_capstones))
        or set(authored_capstones) != expected_capstones
    ):
        raise ExpansionError(
            "Authored capstones must cover the domain map's capstone IDs once each"
        )
    chapters = teaching_chapters(
        read(root / "course/teaching-sequences.json"), domain_map, lessons, root
    )
    reading_ids = [lid for chapter in chapters for lid in chapter["lesson_ids"]]
    reading_ids.extend(l["id"] for l in lessons if l["domain"] in references)
    reading_order = {lid: i for i, lid in enumerate(reading_ids)}
    lessons.sort(key=lambda lesson: reading_order[lesson["id"]])
    attach_checkins(read(root / "course/domain-checkins.json"), lessons, chapters)
    glossary = glossary_entries(lessons)
    used = {s for l in lessons for s in l["source_ids"]}
    sources = [s for s in catalog if s["id"] in used]
    return {
        "title": "From Watts to Tokens",
        "status": "Authored draft — external expert and learner reviews pending",
        "as_of": domain_map["as_of"],
        # The newest reading of a cited source, in the catalog or in a lesson's own
        # source notes, dates the reading content.
        "updated_on": max(
            [domain_map["as_of"]]
            + [s["reviewed_on"] for s in sources if s.get("reviewed_on")]
            + [n["reviewed_on"] for l in lessons for n in l["source_notes"]]
        ),
        "domains": sorted(domain_map["domains"], key=lambda d: order[d["id"]]),
        "chapters": chapters,
        "references": [
            {
                "id": did,
                "title": next(d["title"] for d in domain_map["domains"] if d["id"] == did),
                "lesson_ids": [l["id"] for l in lessons if l["domain"] == did],
                "presentations": [],
            }
            for did in references
        ],
        "lessons": lessons,
        "sources": sources,
        "glossary": glossary,
    }


def glossary_entries(lessons):
    """Collect glossary terms in reading order and report terms defined more than once."""
    glossary, first_use, duplicates = [], {}, {}
    for l in lessons:
        for term in l.get("terms", []):
            if not isinstance(term, dict):
                raise ExpansionError(f"{l['id']}: glossary terms must be records")
            name = text(term.get("term"), "term")
            definition = text(term.get("definition"), "definition")
            key = " ".join(name.lower().split())
            if key in first_use:
                duplicates.setdefault(key, [first_use[key]]).append((name, l["id"]))
                continue
            first_use[key] = (name, l["id"])
            glossary.append({"term": name, "definition": definition, "lesson": l["id"]})
    if duplicates:
        listing = "; ".join(
            f"{uses[0][0]} ({', '.join(lesson for _, lesson in uses)})"
            for uses in duplicates.values()
        )
        if FAIL_ON_DUPLICATE_TERMS:
            raise ExpansionError(f"Duplicate glossary terms: {listing}")
        print(
            f"Warning: {len(duplicates)} glossary terms are defined more than once;"
            f" the first definition is kept: {listing}",
            file=sys.stderr,
        )
    glossary.sort(key=lambda g: g["term"].lower())
    return glossary


def lesson_markdown(l, sources, *, asset_prefix="assets/", domains=(), chapters=()):
    topics = {d["id"]: d for d in domains}
    topic_title = topics.get(l["domain"], {}).get("title", "Integrated practice")
    chapter = next((c for c in chapters if l["id"] in c["lesson_ids"]), None)
    if chapter:
        topic_title = chapter_label(chapter)
    if l.get("optional"):
        topic_title += " · Optional practice"
    lines = [
        f"# {l['title']}",
        "",
        f"**{topic_title}**",
        "",
        l["summary"],
        "",
        f"**Driving question:** {l['question']}",
        "",
    ]
    for section in l["sections"]:
        lines.extend([f"## {section['heading']}", ""])
        for p in section["paragraphs"]:
            lines.extend([p, ""])
        for figure in section.get("figures", []):
            lines.extend(
                [
                    f"![{figure['alt']}]({asset_prefix}{figure['asset']})",
                    "",
                    f"{figure['caption']} [{figure['source_title']}]({figure['source_url']})",
                    "",
                ]
            )
    w = l["worked_example"]
    lines.extend(
        [
            f"## Worked example: {w['title']}",
            "",
            *[f"- {s}" for s in w["givens"]],
            "",
            *[f"{i}. {s}" for i, s in enumerate(w["steps"], 1)],
            "",
            f"**Result:** {w['result']}",
            "",
            f"**Model boundary:** {w['boundary']}",
            "",
        ]
    )
    for key, heading in (("tradeoff", "The tradeoff"), ("failure", "When the situation changes")):
        if l.get(key):
            lines.extend([f"## {heading}", "", *[p + "\n" for p in l[key]]])
    lines.extend(
        [
            "## Apply the idea",
            "",
            l["practice"]["question"],
            "",
            "<details>",
            "<summary>Reveal the worked answer</summary>",
            "",
            l["practice"]["answer"],
            "",
            *[p + "\n" for p in l["practice"]["explanation"]],
            "</details>",
            "",
            f"**The idea to keep:** {l['takeaway']}",
            "",
            "## Sources",
            "",
        ]
    )
    lines.extend(bibliography_entry(sources[note["id"]], note) for note in l["source_notes"])
    if checkin := l.get("domain_checkin"):
        next_title = checkin["next_title"].rstrip().rstrip(".")
        destination = f"**{checkin['next_label']}**"
        if next_title not in checkin["next_label"]:
            destination += f": {next_title}"
        lines.extend(
            [
                "",
                f"## Check your understanding: {checkin['title']}",
                "",
                "Pause and make a prediction, then compare your reasoning.",
                "",
                checkin["scenario"],
                "",
                f"**Pause and predict:** {checkin['prompt']}",
                "",
                "<details>",
                "<summary>Compare your reasoning</summary>",
                "",
                checkin["answer"],
                "",
                *[p + "\n" for p in checkin["explanation"]],
                "</details>",
                "",
                f"**The next problem:** {checkin['bridge']}",
                "",
                f"Continue in {destination}.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def bibliography_entry(source, note):
    """One bibliography line: title, publisher, dates from the catalog, and the lesson's claim."""
    details = [source["publisher"]]
    if source.get("published_on"):
        details.append(f"Published {source['published_on']}")
    if source.get("reviewed_on"):
        details.append(f"Reviewed {source['reviewed_on']}")
    claim = note["claim"].strip()
    if claim[-1] not in ".?!":
        claim += "."
    return f"- [{source['title']}]({source['url']}) — {' · '.join(details)}. {claim}"


def join_words(items):
    """Join names as prose: "A", "A and B", "A, B and C"."""
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + f" and {items[-1]}"


def checkin_summary(chapters, lessons):
    """Say which chapters end with a check-in, from the attached records.

    Returns "" when no chapter has a check-in, so the manuscript says nothing about them.
    """
    by_id = {l["id"]: l for l in lessons}
    numbers, cases, previous = [], [], None
    for chapter in chapters:
        ids = chapter["lesson_ids"]
        closes = bool(ids) and "domain_checkin" in by_id[ids[-1]]
        if "number" in chapter:
            previous = chapter["number"]
            if closes:
                numbers.append(previous)
        elif closes:
            cases.append(
                "the opening case study"
                if previous is None
                else f"the case study after Chapter {previous}"
            )
    count = len(numbers) + len(cases)
    if not count:
        return ""
    parts = []
    if len(numbers) == 1:
        parts.append(f"Chapter {numbers[0]}")
    elif len(numbers) > 2 and numbers == list(range(numbers[0], numbers[-1] + 1)):
        parts.append(f"Chapters {numbers[0]} to {numbers[-1]}")
    elif numbers:
        parts.append("Chapters " + join_words([str(n) for n in numbers]))
    subject = join_words(parts + cases)
    one = count == 1
    return (
        f"{subject[0].upper()}{subject[1:]} {'ends' if one else 'each end'} with a check-in:"
        " pause, make a prediction, compare your reasoning, then connect it to the next"
        f" problem. {'This check-in carries' if one else 'These check-ins carry'} no score"
        f" and {'does' if one else 'do'} not block progression."
    )


def build(root=ROOT, check=False):
    data = load_course(root)
    web = root / "course/web"
    template = (web / "reader.html").read_text()
    css = (web / "reader.css").read_text()
    models = (web / "reader-models.js").read_text()
    script = (
        re.sub(r"^export ", "", models, flags=re.MULTILINE)
        + "\n"
        + (web / "reader.js").read_text()
    )
    if re.search(r"</style\b", css, re.IGNORECASE):
        raise ExpansionError("Unsafe closing CSS tag")
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace(
        "<", "\\u003c"
    )
    replacements = {
        "__READER_CSS__": css,
        "__EXPANDED_COURSE__": payload,
        "__READER_SCRIPT__": re.sub(
            r"</script", r"<\\/script", script, flags=re.IGNORECASE
        ),
    }
    for placeholder in replacements:
        if template.count(placeholder) != 1:
            raise ExpansionError(f"Expected one {placeholder}")
    html = re.sub(
        r"__READER_CSS__|__EXPANDED_COURSE__|__READER_SCRIPT__",
        lambda m: replacements[m[0]],
        template,
    )
    for name in IMAGES:
        if not (root / "course/assets" / name).is_file():
            raise ExpansionError(f"Missing teaching illustration: {name}")
    for lesson in data["lessons"]:
        for section in lesson["sections"]:
            for figure in section.get("figures", []):
                if not (root / "course/assets" / figure["asset"]).is_file():
                    raise ExpansionError(f"Missing source figure: {figure['asset']}")
    sources = {s["id"]: s for s in data["sources"]}
    outputs = {
        Path("course/index.html"): html,
        Path("course/prototypes/teaching-navigation.js"): presentation_identities(
            data["chapters"]
        ),
        Path("course/expanded-course.json"): json.dumps(
            data, ensure_ascii=False, indent=2
        )
        + "\n",
    }
    catalog = read(root / "course/research-sources.json")["sources"]
    sample = normalize(
        read(root / "course/expansion/sample.json"),
        {canonical_url(s["url"]): s for s in catalog},
        {o["id"] for d in data["domains"] for o in d["objectives"]},
        reader_lab_types(root),
    )
    sample_data = {
        **data,
        "references": [],
        "chapters": [
            {**chapter, "lesson_ids": [sample["id"]]}
            for chapter in data["chapters"]
            if "d06-eight-hundred-volt-architectures" in chapter["lesson_ids"]
        ],
        "lessons": [sample],
        "sources": [s for s in catalog if s["id"] in sample["source_ids"]],
        "glossary": [{**term, "lesson": sample["id"]} for term in sample["terms"]],
    }
    sample_replacements = {
        **replacements,
        "__EXPANDED_COURSE__": json.dumps(
            sample_data, ensure_ascii=False, separators=(",", ":")
        ).replace("<", "\\u003c"),
    }
    outputs[Path("course/sample-reading.html")] = re.sub(
        r"__READER_CSS__|__EXPANDED_COURSE__|__READER_SCRIPT__",
        lambda m: sample_replacements[m[0]],
        template,
    )
    outputs[Path("course/SAMPLE.md")] = lesson_markdown(
        sample,
        {s["id"]: s for s in sample_data["sources"]},
        domains=data["domains"],
        chapters=sample_data["chapters"],
    )
    outputs.update(presentation_outputs(root, sample["id"]))
    checkin_note = checkin_summary(data["chapters"], data["lessons"])
    index = [
        "# From Watts to Tokens — A visual course on AI data centers",
        "",
        # The review status stays in the data and the manifest; learners see only the date.
        "Updated " + data["updated_on"] + ".",
        "",
        "Each lesson explains a mechanism, works a numerical example and ends with practice on a changed scenario.",
        "",
        *([checkin_note, ""] if checkin_note else []),
        "[Open the visual reader](index.html) · [Domain map](DOMAIN_MAP.md)",
        "",
        "## Learning path",
        "",
    ]
    for l in data["lessons"]:
        outputs[Path("course/lessons") / (l["id"] + ".md")] = lesson_markdown(
            l,
            sources,
            asset_prefix="../assets/",
            domains=data["domains"],
            chapters=data["chapters"],
        )
    for chapter in [*data["chapters"], *data["references"]]:
        index.extend([f"### {chapter_label(chapter)}", ""])
        for presentation in chapter["presentations"]:
            scope = (
                "Selected-topic slides"
                if presentation["coverage"] == "selected"
                else "Slides"
            )
            index.append(
                f"- {scope}: [{presentation['title']}]({presentation['href']})"
            )
        index.extend(
            f"- {'Optional practice: ' if l.get('optional') else ''}"
            f"[{l['title']}](lessons/{l['id']}.md) — {l['question']}"
            for l in data["lessons"]
            if l["id"] in chapter["lesson_ids"]
        )
        index.append("")
    index.extend(
        [
            "",
            "## Objective-to-lesson coverage",
            "",
            "Each course objective links to the lessons that teach it. Every lesson ends with a practice question.",
            "",
            "| Objective | Lessons |",
            "| --- | --- |",
        ]
    )
    for d in data["domains"]:
        for o in d["objectives"]:
            links = ", ".join(
                f"[{l['title']}](lessons/{l['id']}.md)"
                for l in data["lessons"]
                if o["id"] in l["objectives"]
            )
            index.append(f"| {o['capability']} | {links} |")
    index.extend(
        [
            "",
            "## Full course text",
            "",
            *[
                # Nest each lesson under the manuscript: its title becomes a level-2
                # heading and its sections level 3, so a lesson's start stays visible.
                re.sub(
                    r"(?m)^(#{1,5}) ",
                    r"#\1 ",
                    lesson_markdown(
                        l,
                        sources,
                        domains=data["domains"],
                        chapters=data["chapters"],
                    ),
                )
                for l in data["lessons"]
            ],
        ]
    )
    outputs[Path("course/EXPANDED_COURSE.md")] = "\n".join(index)
    manifest = {
        "as_of": data["as_of"],
        "updated_on": data["updated_on"],
        "lessons": len(data["lessons"]),
        "words": sum(l["word_count"] for l in data["lessons"]),
        "objectives": sum(len(d["objectives"]) for d in data["domains"]),
        "capstones": sum(
            l["domain"] == "capstone" and l.get("capstone_id") is not None
            for l in data["lessons"]
        ),
        "domain_checkins": sum("domain_checkin" in l for l in data["lessons"]),
        "glossary_terms": len(data["glossary"]),
        "source_records": len(data["sources"]),
        "image_sha256": {
            name: hashlib.sha256(
                (root / "course/assets" / name).read_bytes()
            ).hexdigest()
            for name in IMAGES
        },
        "review_state": data["status"],
    }
    outputs[Path("course/expansion-manifest.json")] = (
        json.dumps(manifest, indent=2) + "\n"
    )
    stale = [
        str(path)
        for path, content in outputs.items()
        if not (root / path).is_file() or (root / path).read_text() != content
    ]
    if check and stale:
        raise ExpansionError("Stale expansion outputs: " + ", ".join(stale))
    if not check:
        for path, content in outputs.items():
            (root / path).parent.mkdir(parents=True, exist_ok=True)
            if str(path) in stale:
                (root / path).write_text(content, encoding="utf-8")
    return manifest, stale


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        manifest, changed = build(check=args.check)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(1, f"Expansion build failed: {exc}\n")
    print(
        f"Expanded course: {manifest['lessons']} lessons, {manifest['objectives']} mapped objectives, {manifest['capstones']} capstones; {len(changed)} stale/updated files."
    )


if __name__ == "__main__":
    main()
