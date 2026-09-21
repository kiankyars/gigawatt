#!/usr/bin/env python3
"""Reader prose lint: measures the "audit voice" in course/expansion/*.json.

Report mode (default) prints a per-lesson scorecard and never fails.
`--check` exits 1 when a lesson exceeds the budgets below, so it can become a
CI gate once the rewrite has brought the corpus under them.

    python3 qa/reader/prose_lint.py                 # scorecard, worst first
    python3 qa/reader/prose_lint.py --list d03-service-and-siting
    python3 qa/reader/prose_lint.py --check         # enforce budgets

Budgets come from a human baseline (eight Wikipedia engineering articles,
43k words): 8% of sentences contain a negation, 9% of paragraphs end on one,
"establish" appears 2 times per 10k words. They are deliberately looser than
the baseline because teaching prose legitimately corrects misconceptions.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SOURCES = sorted((ROOT / "course" / "expansion").glob("*.json"))
SKIP = {"sample.json", "sample-presentation.json", "rack-energy-source-additions.proposed.json"}

BUDGET = {
    "para_end_neg": 0.20,   # share of paragraphs whose last sentence is a negation
    "neg_sentences": 0.14,  # share of sentences containing a negation
    "establish_10k": 5.0,   # "establish*" per 10,000 words
    "slide_refs": 0,        # sentences pointing at a slide/image the reader cannot see
    "residue": 0,           # review / fact-check notes left in teaching prose
}

SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9“\"‘'(\[$])")
WORD = re.compile(r"[A-Za-z0-9’'\-]+")
NEG = re.compile(
    r"\b((does|do|did)\s+not|doesn[’']t|cannot|can\s+not|can[’']t|must\s+not|should\s+not|need\s+not|"
    r"(is|are|was|were)\s+not|isn[’']t|aren[’']t|no\s+\w+|neither|nor|none|never|rather\s+than|instead\s+of|not)\b",
    re.I,
)
SLIDE = re.compile(
    r"\b(slides?|the presentation|opening presentation|th(e|is) deck|shown in the|appears? beside|"
    r"the (first|second|third) image|the (generated|manufacturer|original) (illustration|graphic|diagram|image|photograph|cutaway|figure)|"
    r"photograph shown|the animation|original image identifies)\b",
    re.I,
)
RESIDUE = re.compile(
    r"(not verified|was verified|no verified|as of this .{0,20}review|this review|rechecked|still future as of|"
    r"is not taught|not filled with|invented estimates?|not adopted|this replaces|older isolated|now compares|"
    r"omitted from the presentation|the course (does not|uses|labels|treats|keeps))",
    re.I,
)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in SENT.split(text.strip()) if s.strip()]


def lessons():
    for path in SOURCES:
        if path.name in SKIP:
            continue
        data = json.loads(path.read_text())
        for lesson in data if isinstance(data, list) else data.get("lessons", []):
            if isinstance(lesson, dict) and "sections" in lesson:
                yield lesson


def measure(lesson: dict) -> dict:
    paras = [p for s in lesson["sections"] for p in s.get("paragraphs", []) if isinstance(p, str)]
    sents = [s for p in paras for s in sentences(p)]
    words = sum(len(WORD.findall(p)) for p in paras) or 1
    text = " ".join(paras).lower()
    return {
        "id": lesson["id"],
        "words": words,
        "para_end_neg": sum(1 for p in paras if sentences(p) and NEG.search(sentences(p)[-1])) / max(len(paras), 1),
        "neg_sentences": sum(1 for s in sents if NEG.search(s)) / max(len(sents), 1),
        "establish_10k": len(re.findall(r"\bestablish\w*", text)) / words * 1e4,
        "slide_refs": [s for s in sents if SLIDE.search(s)],
        "residue": [s for s in sents if RESIDUE.search(s)],
        "para_end_list": [sentences(p)[-1] for p in paras if sentences(p) and NEG.search(sentences(p)[-1])],
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="exit 1 if any lesson exceeds a budget")
    ap.add_argument("--list", metavar="LESSON_ID", help="print every flagged sentence for one lesson")
    args = ap.parse_args()

    rows = sorted((measure(l) for l in lessons()), key=lambda r: -r["para_end_neg"])

    if args.list:
        row = next((r for r in rows if r["id"] == args.list), None)
        if row is None:
            print(f"unknown lesson: {args.list}", file=sys.stderr)
            return 2
        for label, key in (("PARAGRAPH ENDS ON A NEGATION", "para_end_list"), ("SLIDE REFERENCE", "slide_refs"), ("REVIEW RESIDUE", "residue")):
            print(f"\n== {label} ({len(row[key])})")
            for s in row[key]:
                print(f"  - {s}")
        return 0

    print(f"{'lesson':42s}{'words':>6s}{'¶end-neg':>10s}{'neg-sent':>10s}{'estab/10k':>11s}{'slide':>7s}{'residue':>9s}")
    failures = 0
    for r in rows:
        over = [
            r["para_end_neg"] > BUDGET["para_end_neg"],
            r["neg_sentences"] > BUDGET["neg_sentences"],
            r["establish_10k"] > BUDGET["establish_10k"],
            len(r["slide_refs"]) > BUDGET["slide_refs"],
            len(r["residue"]) > BUDGET["residue"],
        ]
        failures += any(over)
        flag = " *" if any(over) else ""
        print(
            f"{r['id']:42s}{r['words']:6d}{r['para_end_neg']:10.0%}{r['neg_sentences']:10.0%}"
            f"{r['establish_10k']:11.1f}{len(r['slide_refs']):7d}{len(r['residue']):9d}{flag}"
        )
    total = len(rows)
    print(f"\n{failures}/{total} lessons over budget (* = over). Budgets: {BUDGET}")
    return 1 if (args.check and failures) else 0


if __name__ == "__main__":
    raise SystemExit(main())
