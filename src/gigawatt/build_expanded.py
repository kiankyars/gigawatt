"""Build the expanded course reader and Markdown from authored lesson records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
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
)
IMAGES = (
    "campus-cutaway.png",
    "rack-anatomy.png",
    "cooling-cutaway.png",
    "power-equipment.png",
    "network-equipment.png",
)


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


def normalize(raw, catalog_by_url, known_objectives):
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
            if not re.fullmatch(r"references/[a-z0-9-]+\.(?:png|jpeg|jpg|svg)", asset):
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
        value = lesson.get(key)
        if isinstance(value, dict):
            value = [
                f"{name.replace('_', ' ').capitalize()}: {text(v, key)}"
                for name, v in value.items()
            ]
        lesson[key] = paragraphs(value, key)
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
        lesson["source_notes"].append(
            {
                "id": identifier,
                "claim": text(source.get("claim"), "source.claim"),
                "reviewed_on": text(source.get("reviewed_on"), "source.reviewed_on"),
                "limits": text(source.get("limits"), "source.limits"),
            }
        )
    lesson["word_count"] = len(
        flatten(
            {
                k: lesson[k]
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


def attach_domain_checkins(raw, lessons, sequence):
    """Validate one optional boundary exercise per domain and resolve its links."""
    if not isinstance(raw, dict) or raw.get("version") != 1:
        raise ExpansionError("Domain check-ins: expected version 1")
    records = raw.get("checkins")
    if not isinstance(records, list):
        raise ExpansionError("Domain check-ins: expected a list of checkins")
    fields = {
        "domain",
        "title",
        "scenario",
        "prompt",
        "answer",
        "explanation",
        "next_domain",
        "bridge",
    }
    by_domain = {}
    for record in records:
        if not isinstance(record, dict) or set(record) != fields:
            raise ExpansionError("Domain check-in: missing or unexpected fields")
        checkin = deepcopy(record)
        for key in fields - {"explanation"}:
            text(checkin[key], f"domain check-in.{key}")
        if not isinstance(checkin["explanation"], list) or not checkin["explanation"]:
            raise ExpansionError("Domain check-in: expected explanatory paragraphs")
        checkin["explanation"] = paragraphs(
            checkin["explanation"], "domain check-in.explanation"
        )
        domain = checkin["domain"]
        if domain in by_domain:
            raise ExpansionError(f"Duplicate domain check-in: {domain}")
        by_domain[domain] = checkin
    if set(by_domain) != set(sequence):
        raise ExpansionError("Domain check-ins must cover every domain exactly once")
    first = {
        domain: next(l for l in lessons if l["domain"] == domain)
        for domain in sequence + ["capstone"]
    }
    last = {l["domain"]: l for l in lessons}
    for domain, next_domain in zip(sequence, sequence[1:] + ["capstone"], strict=True):
        checkin = by_domain[domain]
        if checkin["next_domain"] != next_domain:
            raise ExpansionError(
                f"{domain}: check-in bridge must follow course sequence"
            )
        checkin["next_lesson"] = first[next_domain]["id"]
        checkin["next_title"] = first[next_domain]["title"]
        last[domain]["domain_checkin"] = checkin


def teaching_chapters(raw, domain_map, lessons, root=ROOT):
    """Resolve available teaching sequences against the single curriculum order.

    Coverage describes the scope of a presentation, not its review or rehearsal
    status. A chapter without a presentation still has its authored reading.
    """
    if not isinstance(raw, dict) or set(raw) != {"version", "presentations"}:
        raise ExpansionError("Teaching catalog: missing or unexpected fields")
    if raw["version"] != 1 or not isinstance(raw["presentations"], list):
        raise ExpansionError("Teaching catalog: expected version 1 and presentations")
    domains = {d["id"]: d for d in domain_map["domains"]}
    sequence = [did for act in domain_map["sequence"] for did in act["domains"]]
    if len(sequence) != len(set(sequence)) or set(sequence) != set(domains):
        raise ExpansionError(
            "Teaching chapters: sequence must contain every domain once"
        )
    titles = {
        **{did: domain["title"] for did, domain in domains.items()},
        "primer": "Primer",
        "D01": "Data center overview",
        "D02": "Workloads and requirements",
        "capstone": "Put the system together",
    }
    chapters = [
        {
            "id": did,
            "number": number,
            "title": titles[did],
            "lesson_ids": [l["id"] for l in lessons if l["domain"] == did],
            "presentations": [],
        }
        for number, did in enumerate(["primer", *sequence, "capstone"], 1)
    ]
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
            item["numbers"].append(chapter["number"])
    labels = {}
    for pid, item in presentations.items():
        numbers = item["numbers"]
        if len(numbers) > 1 and numbers == list(range(numbers[0], numbers[-1] + 1)):
            ordinal = f"{numbers[0]}–{numbers[-1]}"
        else:
            ordinal = ", ".join(str(number) for number in numbers)
        labels[pid] = f"{ordinal}. {item['title']}"
    return (
        "// Generated from teaching-sequences.json and domain-map.json.\n"
        "// Run uv run gigawatt-expand; chapter numbering follows the curriculum order.\n"
        "export const presentationLabels = Object.freeze("
        + json.dumps(labels, ensure_ascii=False, indent=2).replace("<", "\\u003c")
        + ");\n"
    )


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
    lessons = [normalize(l, by_url, known) for l in raw_lessons]
    ids = [l["id"] for l in lessons]
    if len(ids) != len(set(ids)):
        raise ExpansionError("Duplicate authored lesson IDs")
    if known - {
        o for l in lessons if l["domain"] != "capstone" for o in l["objectives"]
    }:
        raise ExpansionError("Some domain objectives have no authored lesson")
    sequence = [did for act in domain_map["sequence"] for did in act["domains"]]
    order = {did: i for i, did in enumerate(sequence + ["capstone"])}
    if any(l["domain"] not in order for l in lessons):
        raise ExpansionError("Unknown lesson domain")
    lessons.sort(key=lambda l: order[l["domain"]])
    expected_capstones = {c["id"] for c in domain_map["capstones"]}
    authored_capstones = [
        l.get("capstone_id") for l in lessons if l["domain"] == "capstone"
    ]
    if set(authored_capstones) != expected_capstones:
        raise ExpansionError(
            "Authored capstones must cover the domain map's capstone IDs"
        )
    attach_domain_checkins(
        read(root / "course/domain-checkins.json"), lessons, sequence
    )
    glossary, seen_terms = [], set()
    for l in lessons:
        for term in l.get("terms", []):
            if not isinstance(term, dict):
                raise ExpansionError(f"{l['id']}: glossary terms must be records")
            name = text(term.get("term"), "term")
            definition = text(term.get("definition"), "definition")
            if name.lower() not in seen_terms:
                glossary.append(
                    {"term": name, "definition": definition, "lesson": l["id"]}
                )
                seen_terms.add(name.lower())
    glossary.sort(key=lambda g: g["term"].lower())
    used = {s for l in lessons for s in l["source_ids"]}
    return {
        "title": "GIGAWATT",
        "status": "Authored draft — external expert and learner reviews pending",
        "as_of": domain_map["as_of"],
        "domains": sorted(domain_map["domains"], key=lambda d: order[d["id"]]),
        "chapters": teaching_chapters(
            read(root / "course/teaching-sequences.json"), domain_map, lessons, root
        ),
        "lessons": lessons,
        "sources": [s for s in catalog if s["id"] in used],
        "glossary": glossary,
    }


def lesson_markdown(
    l, sources, *, include_source=True, asset_prefix="assets/", domains=(), chapters=()
):
    topics = {d["id"]: d for d in domains}
    topic_title = topics.get(l["domain"], {}).get("title", "Integrated practice")
    chapter = next((c for c in chapters if c["id"] == l["domain"]), None)
    if chapter:
        topic_title = f"{chapter['number']}. {chapter['title']}"
    lines = [
        f"# {l['title']}",
        "",
        f"**{topic_title} · Authored draft**",
        "",
        l["summary"],
        "",
        f"**Driving question:** {l['question']}",
        "",
    ]
    if include_source:
        path = l.get("source_path", "course/expansion/sample.json")
        lines[2:2] = [
            f"Generated reading view. Edit [`{path}`](https://github.com/kiankyars/gigawatt/blob/main/{path}), lesson `{l['id']}`, then run `uv run gigawatt-expand`.",
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
            "## The tradeoff",
            "",
        ]
    )
    lines.extend([p + "\n" for p in l["tradeoff"]])
    lines.extend(
        [
            "## When the situation changes",
            "",
            *[p + "\n" for p in l["failure"]],
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
            "## Sources and reading boundaries",
            "",
        ]
    )
    for note in l["source_notes"]:
        s = sources[note["id"]]
        lines.extend(
            [
                f"- [{s['title']}]({s['url']}) — {note['claim']} Read {note['reviewed_on']}. {note['limits']}"
            ]
        )
    if checkin := l.get("domain_checkin"):
        next_domain = (
            "the integrated cases"
            if checkin["next_domain"] == "capstone"
            else topics.get(checkin["next_domain"], {}).get(
                "title", checkin["next_title"]
            )
        )
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
                f"Continue in **{next_domain}**: {checkin['next_title']}.",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


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
    )
    sample_data = {
        **data,
        "chapters": [
            {**chapter, "lesson_ids": [sample["id"]]}
            for chapter in data["chapters"]
            if chapter["id"] == sample["domain"]
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
        chapters=data["chapters"],
    )
    outputs.update(presentation_outputs(root, sample["id"]))
    index = [
        "# GIGAWATT — From watts to useful compute",
        "",
        data["status"] + ". Updated " + data["as_of"] + ".",
        "",
        "The course is organized around mechanisms, solved examples, tradeoffs and changed-scenario practice. Runtime follows teaching and rehearsal; no ten-hour duration is asserted.",
        "",
        "Generated from the lesson records in `course/expansion/` and boundary exercises in `course/domain-checkins.json` with `uv run gigawatt-expand`. This is a reading view; the [filled-in course template](COURSE_REVIEW.md) owns course design and production decisions.",
        "",
        "Each topic ends with a check-in: pause, make a prediction, compare the reasoning, and connect it to the next problem. These check-ins carry no score and do not block progression.",
        "",
        "[Open the visual reader](index.html) · [Domain map](DOMAIN_MAP.md) · [Dry-run guide](PRESENTING.md)",
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
    for chapter in data["chapters"]:
        index.extend([f"### {chapter['number']}. {chapter['title']}", ""])
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
            f"- [{l['title']}](lessons/{l['id']}.md) — {l['question']}"
            for l in data["lessons"]
            if l["id"] in chapter["lesson_ids"]
        )
        index.append("")
    index.extend(
        [
            "",
            "## Objective-to-lesson coverage",
            "",
            "Every entry below is authored and has practice; this is not evidence of learner mastery or external engineering review.",
            "",
            "| Objective | Authored lessons |",
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
                lesson_markdown(
                    l,
                    sources,
                    include_source=False,
                    domains=data["domains"],
                    chapters=data["chapters"],
                ).replace("# ", "## ", 1)
                for l in data["lessons"]
            ],
        ]
    )
    outputs[Path("course/EXPANDED_COURSE.md")] = "\n".join(index)
    manifest = {
        "as_of": data["as_of"],
        "lessons": len(data["lessons"]),
        "words": sum(l["word_count"] for l in data["lessons"]),
        "objectives": sum(len(d["objectives"]) for d in data["domains"]),
        "capstones": sum(l["domain"] == "capstone" for l in data["lessons"]),
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
