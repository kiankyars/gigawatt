"""Build the expanded course reader and Markdown from authored lesson records."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path

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


def load_course(root=ROOT):
    domain_map = read(root / "course/domain-map.json")
    catalog = read(root / "course/research-sources.json")["sources"]
    known = {o["id"] for d in domain_map["domains"] for o in d["objectives"]}
    by_url = {canonical_url(s["url"]): s for s in catalog}
    raw_lessons = []
    for name in PARTS:
        part = read(root / "course/expansion" / name)
        raw_lessons.extend(part["lessons"] if isinstance(part, dict) else part)
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
    for d in domain_map["domains"]:
        if sum(l["domain"] == d["id"] for l in lessons) < 3:
            raise ExpansionError(f"{d['id']}: domain expansion incomplete")
    if sum(l["domain"] == "capstone" for l in lessons) != 5:
        raise ExpansionError("Expected the five integrated capstones")
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
        "as_of": "2026-09-08",
        "domains": sorted(domain_map["domains"], key=lambda d: order[d["id"]]),
        "lessons": lessons,
        "sources": [s for s in catalog if s["id"] in used],
        "glossary": glossary,
    }


def lesson_markdown(l, sources):
    lines = [
        f"# {l['title']}",
        "",
        f"**{l['domain']} · Authored draft · Objectives:** {', '.join(l['objectives'])}",
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
    sources = {s["id"]: s for s in data["sources"]}
    outputs = {
        Path("course/index.html"): html,
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
        sample, {s["id"]: s for s in sample_data["sources"]}
    )
    outputs.update(presentation_outputs(root, sample["id"]))
    index = [
        "# GIGAWATT — From watts to useful compute",
        "",
        data["status"] + ". Updated " + data["as_of"] + ".",
        "",
        "The course is organized around mechanisms, solved examples, tradeoffs and changed-scenario practice. Runtime follows teaching and rehearsal; no ten-hour duration is asserted.",
        "",
        "[Open the visual reader](index.html) · [Domain map](DOMAIN_MAP.md) · [Review help](REVIEW_HELP.md)",
        "",
        "## Learning path",
        "",
    ]
    for l in data["lessons"]:
        outputs[Path("course/lessons") / (l["id"] + ".md")] = lesson_markdown(
            l, sources
        )
        index.append(
            f"- **{l['domain']}** [{l['title']}](lessons/{l['id']}.md) — {l['question']}"
        )
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
            index.append(f"| {o['id']} | {links} |")
    index.extend(
        [
            "",
            "## Full course text",
            "",
            *[
                lesson_markdown(l, sources).replace("# ", "## ", 1)
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
