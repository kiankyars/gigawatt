from __future__ import annotations

import io
import json
import unittest
from contextlib import redirect_stderr
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from gigawatt import build_expanded as b
from gigawatt.build_presentation import validate_presentation
from gigawatt.research import canonical_url


class ExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = b.load_course()
        # A lesson without lab fields, so each test can add its own.
        cls.raw = {
            k: v
            for k, v in b.read(b.ROOT / "course/expansion/foundations-power.json")[0].items()
            if k not in ("lab", "lab_params")
        }
        cls.catalog = {
            canonical_url(s["url"]): s
            for s in b.read(b.ROOT / "course/research-sources.json")["sources"]
        }
        cls.objectives = {
            o["id"] for d in cls.course["domains"] for o in d["objectives"]
        }

    def test_every_objective_has_authored_teaching_and_transfer_practice(self):
        covered = {
            o
            for l in self.course["lessons"]
            if l["domain"] != "capstone"
            for o in l["objectives"]
        }
        self.assertEqual(covered, self.objectives)
        capstone_ids = [
            l["capstone_id"]
            for l in self.course["lessons"]
            if l["domain"] == "capstone" and "capstone_id" in l
        ]
        expected = {c["id"] for c in b.read(b.ROOT / "course/domain-map.json")["capstones"]}
        self.assertEqual(sorted(capstone_ids), sorted(expected))
        manifest = b.read(b.ROOT / "course/expansion-manifest.json")
        self.assertEqual(manifest["capstones"], len(expected))

    def test_merging_lessons_preserves_objective_coverage_without_a_lesson_quota(self):
        original_read = b.read
        part = original_read(b.ROOT / "course/expansion/foundations-power.json")
        domain_lessons = [l for l in part if l["domain"] == "D01"]
        merged = deepcopy(domain_lessons[0])
        merged["objectives"] = sorted(
            {o for l in domain_lessons for o in l["objectives"]}
        )
        changed = [merged] + [l for l in part if l["domain"] != "D01"]

        def read(path):
            return (
                changed
                if path.name == "foundations-power.json"
                else original_read(path)
            )

        with patch.object(b, "read", side_effect=read):
            course = b.load_course()
            self.assertEqual(sum(l["domain"] == "D01" for l in course["lessons"]), 1)
            changed.remove(merged)
            with self.assertRaisesRegex(b.ExpansionError, "no authored lesson"):
                b.load_course()

    def test_capstone_identity_comes_from_the_map_not_a_fixed_count(self):
        original_read = b.read
        exercises = [
            l for l in original_read(b.ROOT / "course/expansion/capstones.json") if "capstone_id" in l
        ]
        unknown = deepcopy(exercises)
        unknown[0]["capstone_id"] = "C99"
        repeated = deepcopy(exercises)
        repeated.append({**deepcopy(repeated[-1]), "id": "c99-repeated-exercise"})
        for changed in (unknown, repeated, exercises[1:]):

            def read(path, changed=changed):
                return changed if path.name == "capstones.json" else original_read(path)

            with (
                self.subTest(lessons=[l["id"] for l in changed]),
                patch.object(b, "read", side_effect=read),
                self.assertRaisesRegex(b.ExpansionError, "capstone IDs"),
            ):
                b.load_course()

    def test_chapter_16_can_hold_companion_reading_without_a_capstone_id(self):
        original_read = b.read
        exercises = [
            l for l in original_read(b.ROOT / "course/expansion/capstones.json") if "capstone_id" in l
        ]
        companion = {
            **deepcopy(exercises[0]),
            "id": "c00-companion-reading",
            "title": "A companion case for the exercises",
        }
        companion.pop("capstone_id")
        companion.pop("optional", None)
        companion["terms"] = []
        changed = [companion, *exercises]

        def read(path):
            return changed if path.name == "capstones.json" else original_read(path)

        with patch.object(b, "read", side_effect=read):
            course = b.load_course()
        capstone = next(c for c in course["chapters"] if c["domain"] == "capstone")
        self.assertEqual(capstone["lesson_ids"], [l["id"] for l in changed])
        lessons = {l["id"]: l for l in course["lessons"]}
        self.assertNotIn("domain_checkin", lessons[companion["id"]])
        economics = next(c for c in course["chapters"] if c["id"] == "D15")
        handoff = lessons[economics["lesson_ids"][-1]]["domain_checkin"]
        self.assertEqual(handoff["next_lesson"], companion["id"])
        self.assertEqual(handoff["next_label"], b.chapter_label(capstone))
        markdown = b.lesson_markdown(
            lessons[economics["lesson_ids"][-1]],
            {s["id"]: s for s in course["sources"]},
            chapters=course["chapters"],
        )
        self.assertIn(
            f"Continue in **{b.chapter_label(capstone)}**: A companion case for the exercises.\n",
            markdown,
        )
        self.assertEqual(
            sum(l["domain"] == "capstone" and "capstone_id" in l for l in course["lessons"]),
            len(exercises),
        )

    def test_every_chapter_with_reading_ends_with_one_checkin(self):
        chapters = self.course["chapters"]
        lessons = {l["id"]: l for l in self.course["lessons"]}
        order = [lid for chapter in chapters for lid in chapter["lesson_ids"]]
        chapter_of = {lid: c for c in chapters for lid in c["lesson_ids"]}
        closing = [c for c in chapters if c["lesson_ids"] and c["domain"] != "capstone"]
        self.assertEqual(sum("domain_checkin" in l for l in lessons.values()), len(closing))
        self.assertEqual(len(closing), 15)
        for chapter in chapters:
            with self.subTest(chapter=chapter["id"]):
                ids = chapter["lesson_ids"]
                self.assertTrue(all("domain_checkin" not in lessons[lid] for lid in ids[:-1]))
                if chapter not in closing:
                    self.assertTrue(all("domain_checkin" not in lessons[lid] for lid in ids))
                    continue
                checkin = lessons[ids[-1]]["domain_checkin"]
                following = lessons[order[order.index(ids[-1]) + 1]]
                next_chapter = chapter_of[following["id"]]
                self.assertEqual(checkin["chapter"], chapter["id"])
                self.assertEqual(checkin["domain"], chapter["domain"])
                self.assertEqual(checkin["next_lesson"], following["id"])
                self.assertEqual(checkin["next_title"], following["title"])
                self.assertEqual(checkin["next_chapter"], next_chapter["id"])
                self.assertEqual(checkin["next_domain"], next_chapter["id"])
                self.assertEqual(checkin["next_label"], b.chapter_label(next_chapter))
        for reference in self.course["references"]:
            self.assertTrue(all("domain_checkin" not in lessons[lid] for lid in reference["lesson_ids"]))

    def test_chapter_4_checkin_continues_into_the_case_study(self):
        lessons = {l["id"]: l for l in self.course["lessons"]}
        siting = next(c for c in self.course["chapters"] if c["id"] == "D03")
        checkin = lessons[siting["lesson_ids"][-1]]["domain_checkin"]
        self.assertEqual(checkin["next_lesson"], "d03-interconnection-queues")
        self.assertEqual(checkin["next_chapter"], "grid-queues")
        self.assertEqual(checkin["next_label"], "Case study — ERCOT and PJM: the race to connect")
        self.assertIn("ERCOT", checkin["bridge"])
        self.assertIn("PJM", checkin["bridge"])
        case = lessons["d03-interconnection-queues"]["domain_checkin"]
        self.assertEqual(case["chapter"], "grid-queues")
        self.assertEqual(case["next_label"], "5. Physical site, buildings and safety")
        sources = {s["id"]: s for s in self.course["sources"]}
        markdown = b.lesson_markdown(lessons[siting["lesson_ids"][-1]], sources, chapters=self.course["chapters"])
        self.assertIn("Continue in **Case study — ERCOT and PJM: the race to connect**.", markdown)

    def test_handoffs_name_the_next_chapter_and_end_with_one_period(self):
        chapters = {c["id"]: c for c in self.course["chapters"]}
        lessons = {l["id"]: l for l in self.course["lessons"]}
        sources = {s["id"]: s for s in self.course["sources"]}
        # Whatever lesson opens the next chapter, the handoff names that chapter as the
        # reader's directory does and ends the lesson title with exactly one period.
        opening = {
            chapter_id: lessons[chapters[chapter_id]["lesson_ids"][0]]["title"].rstrip(".")
            for chapter_id in ("D06", "D06-DC", "capstone")
        }
        expected = {
            "D05": f"Continue in **8. Rack power and buffering**: {opening['D06']}.\n",
            "D06": f"Continue in **9. 800 V DC distribution**: {opening['D06-DC']}.\n",
            "D15": f"Continue in **16. Putting an AI Factory Together**: {opening['capstone']}.\n",
        }
        self.assertTrue(lessons[chapters["capstone"]["lesson_ids"][0]]["title"].strip())
        for chapter in self.course["chapters"]:
            closing = chapter["lesson_ids"] and lessons[chapter["lesson_ids"][-1]]
            if not closing or "domain_checkin" not in closing:
                continue
            with self.subTest(chapter=chapter["id"]):
                markdown = b.lesson_markdown(closing, sources, chapters=self.course["chapters"])
                handoff = markdown.rstrip("\n").rsplit("\n", 1)[1]
                self.assertTrue(handoff.startswith(f"Continue in **{closing['domain_checkin']['next_label']}**"))
                self.assertTrue(handoff.endswith(".") and not handoff.endswith(".."))
                if chapter["id"] in expected:
                    self.assertTrue(markdown.endswith(expected[chapter["id"]]))
                self.assertNotIn("the integrated cases", markdown)

    def test_manuscript_names_the_chapters_that_end_with_a_checkin(self):
        summary = b.checkin_summary(self.course["chapters"], self.course["lessons"])
        self.assertTrue(
            summary.startswith(
                "Chapters 2 to 15 and the case study after Chapter 4 each end with a check-in:"
            )
        )
        self.assertTrue(summary.endswith("These check-ins carry no score and do not block progression."))
        manuscript = (b.ROOT / "course/EXPANDED_COURSE.md").read_text(encoding="utf-8")
        self.assertIn(f"\n\n{summary}\n\n", manuscript)

        def course(*layout):
            """Chapters from ("3", True) for numbered or ("case", True) for unnumbered."""
            chapters, lessons = [], []
            for i, (number, closes) in enumerate(layout):
                chapter = {"id": f"c{i}", "lesson_ids": [f"l{i}"]}
                if number != "case":
                    chapter["number"] = int(number)
                chapters.append(chapter)
                lessons.append({"id": f"l{i}", **({"domain_checkin": {}} if closes else {})})
            return chapters, lessons

        cases = {
            "Chapter 2 ends with a check-in": (("1", False), ("2", True), ("3", False)),
            "Chapters 2 and 3 each end with a check-in": (("2", True), ("3", True)),
            "Chapters 2, 4 and 5 each end with a check-in": (
                ("2", True), ("3", False), ("4", True), ("5", True),
            ),
            "Chapters 2 to 4 each end with a check-in": (("2", True), ("3", True), ("4", True)),
            "Chapter 2 and the opening case study each end with a check-in": (
                ("case", True), ("1", False), ("2", True),
            ),
            "The opening case study and the case study after Chapter 1 each end with a check-in": (
                ("case", True), ("1", False), ("case", True),
            ),
            "The opening case study ends with a check-in": (("case", True), ("1", False)),
        }
        for expected, layout in cases.items():
            with self.subTest(layout=layout):
                summary = b.checkin_summary(*course(*layout))
                self.assertTrue(summary.startswith(expected + ":"), summary)
                single = expected.endswith(" ends with a check-in")
                self.assertTrue(
                    summary.endswith(
                        "This check-in carries no score and does not block progression."
                        if single
                        else "These check-ins carry no score and do not block progression."
                    )
                )
        chapters, lessons = course(("1", False), ("2", False))
        chapters.append({"id": "empty", "number": 3, "lesson_ids": []})
        self.assertEqual(b.checkin_summary(chapters, lessons), "")

    def test_manuscript_nests_each_lesson_under_its_title(self):
        manuscript = (b.ROOT / "course/EXPANDED_COURSE.md").read_text(encoding="utf-8")
        body = manuscript.split("\n## Full course text\n", 1)[1]
        self.assertEqual(
            [line[3:] for line in body.splitlines() if line.startswith("## ")],
            [l["title"] for l in self.course["lessons"]],
        )
        self.assertNotIn("\n# ", body)
        self.assertEqual(body.count("\n### Sources\n"), len(self.course["lessons"]))
        for lesson in self.course["lessons"]:
            with self.subTest(lesson=lesson["id"]):
                self.assertIn(f"\n### {lesson['sections'][0]['heading']}\n", body)

    def test_checkins_follow_teaching_order_and_survive_lesson_merges(self):
        raw = b.read(b.ROOT / "course/domain-checkins.json")
        original = deepcopy(raw)
        lessons = deepcopy(self.course["lessons"])
        chapters = deepcopy(self.course["chapters"])
        first_d01 = next(l for l in lessons if l["domain"] == "D01")
        lessons = [l for l in lessons if l["domain"] != "D01" or l is first_d01]
        for chapter in chapters:
            if chapter["id"] == "D01":
                chapter["lesson_ids"] = [first_d01["id"]]
        for lesson in lessons:
            lesson.pop("domain_checkin", None)
        b.attach_checkins(raw, lessons, chapters)
        self.assertEqual(raw, original)
        self.assertEqual(first_d01["domain_checkin"]["next_chapter"], "D02")
        bridges = {
            l["domain_checkin"]["chapter"]: l["domain_checkin"]["next_chapter"]
            for l in lessons
            if "domain_checkin" in l
        }
        self.assertEqual(bridges["D03"], "grid-queues")
        self.assertEqual(bridges["grid-queues"], "D12")
        self.assertEqual(bridges["D12"], "D04")
        self.assertEqual(bridges["D06"], "D06-DC")
        self.assertEqual(bridges["D06-DC"], "D08")
        self.assertEqual(bridges["D11"], "D13")
        self.assertEqual(bridges["D15"], "capstone")

    def test_checkins_attach_to_the_last_lesson_after_a_chapter_reorder(self):
        original_read = b.read
        current = {c["id"]: c["lesson_ids"] for c in self.course["chapters"]}
        # Reverse two chapters' reading order; the check-ins must follow the new last lessons.
        wanted = {domain: list(reversed(current[domain])) for domain in ("D03", "D12")}

        def read(path):
            data = original_read(path)
            if path.name in {"foundations-power.json", "heat-delivery-operations.json"}:
                items = data["lessons"] if isinstance(data, dict) else data
                for domain, ids in wanted.items():
                    rank = {lid: i for i, lid in enumerate(ids)}
                    slots = [i for i, l in enumerate(items) if l["domain"] == domain]
                    ordered = sorted((items[i] for i in slots), key=lambda l: rank[l["id"]])
                    for i, lesson in zip(slots, ordered, strict=True):
                        items[i] = lesson
            return data

        with patch.object(b, "read", side_effect=read):
            course = b.load_course()
        chapters = {c["id"]: c for c in course["chapters"]}
        lessons = {l["id"]: l for l in course["lessons"]}
        for domain, ids in wanted.items():
            self.assertEqual(chapters[domain]["lesson_ids"], ids)
            self.assertTrue(all("domain_checkin" not in lessons[lid] for lid in ids[:-1]))
            self.assertEqual(lessons[ids[-1]]["domain_checkin"]["chapter"], domain)
        self.assertEqual(lessons[wanted["D03"][-1]]["domain_checkin"]["next_lesson"], "d03-interconnection-queues")
        self.assertEqual(lessons["d03-interconnection-queues"]["domain_checkin"]["next_lesson"], wanted["D12"][0])
        self.assertEqual(lessons[wanted["D12"][-1]]["domain_checkin"]["next_chapter"], "D04")

    def test_incomplete_duplicate_or_misrouted_checkins_fail(self):
        raw = b.read(b.ROOT / "course/domain-checkins.json")
        chapters = self.course["chapters"]
        missing = deepcopy(raw)
        missing["checkins"].pop()
        duplicate = deepcopy(raw)
        duplicate["checkins"].append(deepcopy(duplicate["checkins"][0]))
        unknown = deepcopy(raw)
        unknown["checkins"][0]["chapter"] = "D99"
        misrouted = deepcopy(raw)
        next(c for c in misrouted["checkins"] if c["chapter"] == "D03")[
            "next_chapter"
        ] = "D12"
        for record, message in [
            (missing, "cover every chapter"),
            (duplicate, "Duplicate chapter check-in"),
            (unknown, "cover every chapter"),
            (misrouted, "follow course sequence"),
        ]:
            with (
                self.subTest(message=message),
                self.assertRaisesRegex(b.ExpansionError, message),
            ):
                b.attach_checkins(record, deepcopy(self.course["lessons"]), chapters)

    def test_checkins_require_a_scenario_prediction_reasoning_and_bridge(self):
        raw = b.read(b.ROOT / "course/domain-checkins.json")
        chapters = self.course["chapters"]
        for field in ("title", "scenario", "prompt", "answer", "explanation", "bridge"):
            changed = deepcopy(raw)
            changed["checkins"][0][field] = [] if field == "explanation" else ""
            with self.subTest(field=field), self.assertRaises(b.ExpansionError):
                b.attach_checkins(changed, deepcopy(self.course["lessons"]), chapters)
        changed = deepcopy(raw)
        changed["checkins"][0]["promtp"] = changed["checkins"][0].pop("prompt")
        with self.assertRaisesRegex(b.ExpansionError, "missing or unexpected fields"):
            b.attach_checkins(changed, deepcopy(self.course["lessons"]), chapters)

    def test_markdown_includes_checkin_with_hidden_reasoning(self):
        sources = {s["id"]: s for s in self.course["sources"]}
        for lesson in self.course["lessons"]:
            markdown = b.lesson_markdown(lesson, sources)
            if checkin := lesson.get("domain_checkin"):
                with self.subTest(lesson=lesson["id"]):
                    boundary_text = markdown.split("## Check your understanding: ", 1)[
                        1
                    ]
                    self.assertIn("Pause and make a prediction", boundary_text)
                    self.assertIn(checkin["scenario"], boundary_text)
                    self.assertIn(checkin["prompt"], boundary_text)
                    reveal = boundary_text.split("<details>", 1)[1].split(
                        "</details>", 1
                    )[0]
                    self.assertIn(checkin["answer"], reveal)
                    for explanation in checkin["explanation"]:
                        self.assertIn(explanation, reveal)
                    after = boundary_text.split("</details>", 1)[1]
                    self.assertIn(checkin["bridge"], after)
                    self.assertIn(f"Continue in **{checkin['next_label']}**", after)
            else:
                self.assertNotIn("## Check your understanding: ", markdown)

    def test_normalization_preserves_worked_steps_and_specific_source_limits(self):
        l = b.normalize(self.raw, self.catalog, self.objectives)
        for original, rendered in zip(
            self.raw["example"]["steps"], l["worked_example"]["steps"], strict=True
        ):
            for value in original.values():
                self.assertIn(value, rendered)
        self.assertEqual(
            l["source_notes"][0]["limits"], self.raw["sources"][0]["limits"]
        )
        self.assertEqual(
            l["practice"]["explanation"][0], self.raw["practice"]["reasoning"]
        )

    def test_tradeoff_and_failure_are_optional_but_not_empty(self):
        lesson = deepcopy(self.raw)
        lesson.pop("tradeoff")
        lesson.pop("failure")
        normalized = b.normalize(lesson, self.catalog, self.objectives)
        self.assertNotIn("tradeoff", normalized)
        self.assertNotIn("failure", normalized)
        sources = {s["id"]: s for s in self.catalog.values()}
        markdown = b.lesson_markdown(normalized, sources)
        self.assertNotIn("## The tradeoff", markdown)
        self.assertNotIn("## When the situation changes", markdown)
        self.assertIn("## Apply the idea", markdown)
        kept = b.normalize(deepcopy(self.raw), self.catalog, self.objectives)
        self.assertIn("## The tradeoff", b.lesson_markdown(kept, sources))
        for key in ("tradeoff", "failure"):
            for empty in ("", [], {}):
                lesson = deepcopy(self.raw)
                lesson[key] = empty
                with self.subTest(key=key, empty=empty), self.assertRaises(b.ExpansionError):
                    b.normalize(lesson, self.catalog, self.objectives)

    def test_lab_fields_pass_through_and_optional_lessons_are_labelled(self):
        lesson = deepcopy(self.raw)
        lesson.update({"lab": "heat", "lab_params": {"duty": 120, "delta": 8.5, "mode": "ac"}, "optional": True})
        normalized = b.normalize(lesson, self.catalog, self.objectives)
        self.assertEqual(normalized["lab"], "heat")
        self.assertEqual(normalized["lab_params"], {"duty": 120, "delta": 8.5, "mode": "ac"})
        self.assertIs(normalized["optional"], True)
        sources = {s["id"]: s for s in self.catalog.values()}
        markdown = b.lesson_markdown(normalized, sources, chapters=self.course["chapters"])
        self.assertIn("· Optional practice**", markdown.split("\n\n", 3)[1])
        hidden = deepcopy(self.raw)
        hidden["lab"] = "none"
        self.assertEqual(b.normalize(hidden, self.catalog, self.objectives)["lab"], "none")
        plain = b.lesson_markdown(b.normalize(deepcopy(self.raw), self.catalog, self.objectives), sources)
        self.assertNotIn("Optional practice", plain)
        for fields, message in [
            ({"lab": "thermal"}, "lab must be one of"),
            ({"lab": 3}, "lab must be one of"),
            ({"lab_params": {"duty": 1}}, "explicit lab type"),
            ({"lab": "none", "lab_params": {"duty": 1}}, "explicit lab type"),
            ({"lab": "heat", "lab_params": {}}, "nonempty object"),
            ({"lab": "heat", "lab_params": [1]}, "nonempty object"),
            ({"lab": "heat", "lab_params": {"Duty": 1}}, "unsafe lab_params key"),
            ({"lab": "heat", "lab_params": {"duty": True}}, "finite number"),
            ({"lab": "heat", "lab_params": {"duty": float("nan")}}, "finite number"),
            ({"lab": "heat", "lab_params": {"duty": None}}, "finite number"),
            ({"optional": "yes"}, "optional must be"),
        ]:
            lesson = deepcopy(self.raw)
            lesson.update(fields)
            with self.subTest(fields=fields), self.assertRaisesRegex(b.ExpansionError, message):
                b.normalize(lesson, self.catalog, self.objectives)

    def test_lab_types_come_from_the_labs_the_reader_renders(self):
        reader = (b.ROOT / "course/web/reader.js").read_text()
        lab_types = b.reader_lab_types()
        self.assertTrue(lab_types)
        for lab in lab_types:
            self.assertIn(f'type === "{lab}"', reader)
        for lesson in self.course["lessons"]:
            if "lab" in lesson:
                self.assertIn(lesson["lab"], lab_types | {"none"})
        lesson = deepcopy(self.raw)
        lesson["lab"] = "energy"
        with self.assertRaisesRegex(b.ExpansionError, "lab must be one of heat or none"):
            b.normalize(lesson, self.catalog, self.objectives, frozenset({"heat"}))
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "course/web").mkdir(parents=True)
            (root / "course/web/reader.js").write_text("const labs = {};")
            with self.assertRaisesRegex(b.ExpansionError, "No lab types"):
                b.reader_lab_types(root)

    def test_markdown_is_a_learner_page_with_a_catalog_bibliography(self):
        sources = {s["id"]: s for s in self.course["sources"]}
        for lesson in self.course["lessons"]:
            with self.subTest(lesson=lesson["id"]):
                markdown = b.lesson_markdown(lesson, sources, chapters=self.course["chapters"])
                self.assertNotIn("Generated reading view", markdown)
                self.assertNotIn("Authored draft", markdown)
                self.assertNotIn("gigawatt-expand", markdown)
                bibliography = markdown.split("\n## Sources\n\n", 1)[1].split("\n\n## ", 1)[0]
                entries = [line for line in bibliography.splitlines() if line]
                self.assertEqual(len(entries), len(lesson["source_notes"]))
                for note, entry in zip(lesson["source_notes"], entries, strict=True):
                    source = sources[note["id"]]
                    details = [source["publisher"]]
                    if source.get("published_on"):
                        details.append(f"Published {source['published_on']}")
                    if source.get("reviewed_on"):
                        details.append(f"Reviewed {source['reviewed_on']}")
                    claim = note["claim"].strip()
                    claim += "" if claim[-1] in ".?!" else "."
                    self.assertEqual(
                        entry,
                        f"- [{source['title']}]({source['url']}) — {' · '.join(details)}. {claim}",
                    )
                    self.assertNotIn(note["limits"], entry)

    def test_bibliography_ends_a_claim_with_one_period(self):
        lesson = deepcopy(self.raw)
        lesson["sources"] = lesson["sources"][:1]
        claim = lesson["sources"][0]["claim"].strip().rstrip(".?!")
        sources = {s["id"]: s for s in self.catalog.values()}
        for written in (claim, f"{claim}.", f"  {claim}  "):
            lesson["sources"][0]["claim"] = written
            normalized = b.normalize(lesson, self.catalog, self.objectives)
            markdown = b.lesson_markdown(normalized, sources)
            entry = markdown.split("\n## Sources\n\n", 1)[1].splitlines()[0]
            with self.subTest(claim=written):
                self.assertTrue(entry.endswith(f". {claim}."))
                self.assertFalse(entry.endswith(".."))
        record = next(iter(sources.values()))
        undated = {k: v for k, v in record.items() if k not in ("published_on", "reviewed_on")}
        self.assertEqual(
            b.bibliography_entry(undated, {"claim": "Asks a question?"}),
            f"- [{record['title']}]({record['url']}) — {record['publisher']}. Asks a question?",
        )

    def test_duplicate_glossary_terms_warn_now_and_can_fail_the_build(self):
        lessons = [
            {"id": "first", "terms": [{"term": "Approach temperature", "definition": "Tower meaning."}]},
            {"id": "second", "terms": [{"term": "approach  Temperature", "definition": "CDU meaning."}]},
            {"id": "third", "terms": [{"term": "Critical path", "definition": "Schedule meaning."}]},
        ]
        stderr = io.StringIO()
        with patch.object(b, "FAIL_ON_DUPLICATE_TERMS", False), redirect_stderr(stderr):
            glossary = b.glossary_entries(lessons)
        self.assertEqual([g["term"] for g in glossary], ["Approach temperature", "Critical path"])
        self.assertEqual(glossary[0]["lesson"], "first")
        self.assertIn("Approach temperature (first, second)", stderr.getvalue())
        with (
            patch.object(b, "FAIL_ON_DUPLICATE_TERMS", True),
            self.assertRaisesRegex(b.ExpansionError, r"Approach temperature \(first, second\)"),
        ):
            b.glossary_entries(lessons)
        with patch.object(b, "FAIL_ON_DUPLICATE_TERMS", True):
            self.assertEqual(len(b.glossary_entries(lessons[:1] + lessons[2:])), 2)

    def test_manuscript_date_and_source_dates_come_from_the_catalog(self):
        catalog = {s["id"]: s for s in b.read(b.ROOT / "course/research-sources.json")["sources"]}
        cited = {sid for l in self.course["lessons"] for sid in l["source_ids"]}
        self.assertEqual({s["id"] for s in self.course["sources"]}, cited)
        read_on = [n["reviewed_on"] for l in self.course["lessons"] for n in l["source_notes"]]
        self.assertEqual(
            self.course["updated_on"],
            max([self.course["as_of"]] + [catalog[sid]["reviewed_on"] for sid in cited] + read_on),
        )
        self.assertGreaterEqual(self.course["updated_on"], max(read_on))
        manuscript = (b.ROOT / "course/EXPANDED_COURSE.md").read_text(encoding="utf-8")
        self.assertIn(f"\n\nUpdated {self.course['updated_on']}.\n\n", manuscript)
        self.assertNotIn("Authored draft", manuscript)
        self.assertNotIn("reviews pending", manuscript)
        undated = deepcopy(self.raw)
        undated["sources"][0]["reviewed_on"] = "26 September 2026"
        with self.assertRaisesRegex(b.ExpansionError, "YYYY-MM-DD"):
            b.normalize(undated, self.catalog, self.objectives)
        for source in self.course["sources"]:
            self.assertEqual(source.get("published_on"), catalog[source["id"]].get("published_on"))
        self.assertTrue(any(s.get("published_on") for s in self.course["sources"]))

    def test_unknown_objectives_and_uncatalogued_evidence_fail(self):
        l = deepcopy(self.raw)
        l["objectives"].append("D99.1")
        with self.assertRaises(b.ExpansionError):
            b.normalize(l, self.catalog, self.objectives)
        l = deepcopy(self.raw)
        l["sources"][0]["url"] = "https://example.org/unreviewed"
        with self.assertRaisesRegex(b.ExpansionError, "not yet in library"):
            b.normalize(l, self.catalog, self.objectives)

    def test_missing_solution_or_boundary_cannot_pass_as_a_lesson(self):
        for container, field in [("practice", "answer"), ("example", "boundary")]:
            l = deepcopy(self.raw)
            l[container][field] = ""
            with self.assertRaises(b.ExpansionError):
                b.normalize(l, self.catalog, self.objectives)

    def test_glossary_links_resolve_to_authored_lessons(self):
        known = {l["id"] for l in self.course["lessons"]}
        self.assertTrue(all(g["lesson"] in known for g in self.course["glossary"]))
        terms = [g["term"].lower() for g in self.course["glossary"]]
        self.assertEqual(len(terms), len(set(terms)))

    def test_presentation_and_reading_are_distinct_generated_surfaces(self):
        audience = (b.ROOT / "course/sample.html").read_text()
        reference = (b.ROOT / "course/sample-reading.html").read_text()
        self.assertIn('id="presentation-data"', audience)
        self.assertIn('data-view="student"', audience)
        self.assertIn('data-view="teach"', (b.ROOT / "course/teach.html").read_text())
        self.assertIn(
            'data-view="notes"', (b.ROOT / "course/sample-notes.html").read_text()
        )
        self.assertNotIn('id="expanded-data"', audience)
        self.assertIn('id="expanded-data"', reference)
        self.assertTrue((b.ROOT / "course/sample-notes.html").is_file())
        data = b.read(b.ROOT / "course/expansion/sample-presentation.json")
        self.assertEqual(data["source_lesson_id"], "sample-800v")
        self.assertEqual(
            [s["kind"] for s in data["steps"][1:5]],
            ["dc-basics", "ac-basics", "three-phase", "voltage-basis"],
        )
        for step in data["steps"]:
            self.assertLessEqual(len(step["headline"].split()), 18)
            self.assertNotIn("caption", step)
            self.assertTrue(step["notes"] and step["cue"] and step["explanation"])

    def test_presentation_contract_requires_a_problem_mechanism_and_relevant_ending(
        self,
    ):
        data = b.read(b.ROOT / "course/expansion/sample-presentation.json")
        validate_presentation(data)
        for field in ("fixed_boundary", "primary_payoff", "closing_question"):
            changed = deepcopy(data)
            changed["learning_contract"][field] = ""
            with self.assertRaisesRegex(ValueError, "learning contract"):
                validate_presentation(changed)
        changed = deepcopy(data)
        changed["steps"][-1]["pedagogical_role"] = "balance"
        validate_presentation(changed)
        changed["steps"][0]["pedagogical_role"] = "balance"
        with self.assertRaisesRegex(ValueError, "Start with the problem"):
            validate_presentation(changed)

    def test_presentation_contract_allows_authored_sequence_lengths(self):
        data = b.read(b.ROOT / "course/expansion/sample-presentation.json")
        data["steps"] = [
            data["steps"][0],
            next(s for s in data["steps"] if s["pedagogical_role"] == "mechanism"),
            data["steps"][-1],
        ]
        data["planned_duration_seconds"] = sum(
            s["duration_seconds"] for s in data["steps"]
        )
        validate_presentation(data)

    def test_generated_reader_is_current_and_data_is_inert(self):
        _, stale = b.build(check=True)
        self.assertEqual(stale, [])
        html = (b.ROOT / "course/index.html").read_text()
        self.assertIn('type="application/json"', html)
        self.assertNotIn("__EXPANDED_COURSE__", html)
        payload = html.split('<script id="expanded-data" type="application/json">')[
            1
        ].split("</script>")[0]
        self.assertEqual(
            len(json.loads(payload)["lessons"]), len(self.course["lessons"])
        )

    def test_reference_figures_keep_sources_and_relative_asset_links(self):
        lesson = next(
            l for l in self.course["lessons"] if l["id"] == "d04-conversion-placement"
        )
        figures = [f for s in lesson["sections"] for f in s.get("figures", [])]
        self.assertEqual(len(figures), 2)
        sources = {s["id"]: s for s in self.course["sources"]}
        markdown = b.lesson_markdown(lesson, sources, asset_prefix="../assets/")
        for figure in figures:
            self.assertIn(f"../assets/{figure['asset']}", markdown)
            self.assertIn(figure["source_url"], markdown)
            self.assertTrue((b.ROOT / "course/assets" / figure["asset"]).is_file())
        for asset in ("references/aisle-photo.webp", "references/aisle-photo.jpeg"):
            changed = deepcopy(self.raw)
            changed["sections"][0]["figures"] = [dict(figures[0], asset=asset)]
            normalized = b.normalize(changed, self.catalog, self.objectives)
            self.assertEqual(normalized["sections"][0]["figures"][0]["asset"], asset)
        for asset in ("../../private.png", "references/aisle-photo.gif", "references/Aisle.webp"):
            changed = deepcopy(self.raw)
            changed["sections"][0]["figures"] = [dict(figures[0], asset=asset)]
            with self.subTest(asset=asset), self.assertRaisesRegex(b.ExpansionError, "Unsafe reference figure path"):
                b.normalize(changed, self.catalog, self.objectives)

    def test_sample_embeds_every_cited_catalog_record(self):
        html = (b.ROOT / "course/sample-reading.html").read_text()
        payload = json.loads(
            html.split('<script id="expanded-data" type="application/json">')[1].split(
                "</script>"
            )[0]
        )
        cited = set(payload["lessons"][0]["source_ids"])
        self.assertEqual(cited, {s["id"] for s in payload["sources"]})
        self.assertNotIn("domain_checkin", payload["lessons"][0])


if __name__ == "__main__":
    unittest.main()
