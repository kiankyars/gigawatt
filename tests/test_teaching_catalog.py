from __future__ import annotations

import unittest
from copy import deepcopy
from html.parser import HTMLParser
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt import build_expanded as b


class TeachingCatalogTests(unittest.TestCase):
    def setUp(self):
        self.directory = TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.root = Path(self.directory.name)
        (self.root / "course/prototypes").mkdir(parents=True)
        (self.root / "course/prototypes/deck.html").write_text("<title>Deck</title>")
        self.domain_map = {
            "domains": [
                {"id": "D01", "title": "Boundaries"},
                {"id": "D02", "title": "Workloads"},
            ],
            "sequence": [{"domains": ["D01", "D02"]}],
        }
        self.lessons = [
            {"id": "boundaries", "domain": "D01"},
            {"id": "workload-brief", "domain": "D02"},
            {"id": "exercise", "domain": "capstone"},
        ]
        self.catalog = {
            "version": 1,
            "presentations": [
                {
                    "id": "workloads",
                    "title": "Workloads and requirements",
                    "chapters": [
                        {
                            "id": "D02",
                            "href": "prototypes/deck.html?teach=1#start",
                            "coverage": "chapter",
                        }
                    ],
                }
            ],
        }

    def resolve(self, catalog=None, domain_map=None):
        return b.teaching_chapters(
            self.catalog if catalog is None else catalog,
            self.domain_map if domain_map is None else domain_map,
            self.lessons,
            self.root,
        )

    def test_numbers_follow_the_curriculum_instead_of_domain_ids(self):
        chapters = self.resolve()
        self.assertEqual(
            [(c["id"], c["number"]) for c in chapters],
            [
                ("primer", 1),
                ("D01", 2),
                ("D02", 3),
                ("capstone", 4),
            ],
        )
        changed = deepcopy(self.domain_map)
        changed["sequence"][0]["domains"].reverse()
        reordered = self.resolve(domain_map=changed)
        self.assertEqual(reordered[1]["id"], "D02")
        self.assertEqual(reordered[1]["number"], 2)
        self.assertIn(
            '"workloads": "2. Workloads and requirements"',
            b.presentation_identities(reordered),
        )

    def test_placement_preserves_teaching_mode_fragment_and_scope(self):
        chapters = self.resolve()
        workload = next(c for c in chapters if c["id"] == "D02")
        self.assertEqual(workload["title"], "Workloads and requirements")
        self.assertEqual(workload["lesson_ids"], ["workload-brief"])
        self.assertEqual(
            workload["presentations"],
            [
                {
                    "id": "workloads",
                    "title": "Workloads and requirements",
                    "href": "prototypes/deck.html?teach=1#start",
                    "coverage": "chapter",
                }
            ],
        )
        self.assertEqual(chapters[0]["lesson_ids"], [])
        self.assertEqual(chapters[1]["presentations"], [])

    def test_a_shared_presentation_has_one_identity_and_number_range(self):
        self.catalog["presentations"][0]["chapters"].append(
            {
                "id": "D01",
                "href": "prototypes/deck.html?teach=1",
                "coverage": "selected",
            }
        )
        chapters = self.resolve()
        labels = b.presentation_identities(chapters)
        self.assertEqual(labels.count('"workloads"'), 1)
        self.assertIn("2–3. Workloads and requirements", labels)

    def test_missing_presentation_fails_before_a_broken_link_is_published(self):
        (self.root / "course/prototypes/deck.html").unlink()
        with self.assertRaisesRegex(b.ExpansionError, "missing teaching presentation"):
            self.resolve()

    def test_invalid_catalog_routes_and_duplicate_placements_fail(self):
        cases = []
        duplicate = deepcopy(self.catalog)
        duplicate["presentations"].append(deepcopy(duplicate["presentations"][0]))
        cases.append((duplicate, "Duplicate teaching presentation"))
        duplicate = deepcopy(self.catalog)
        duplicate["presentations"][0]["chapters"].append(
            deepcopy(duplicate["presentations"][0]["chapters"][0])
        )
        cases.append((duplicate, "duplicate presentation in chapter"))
        for field, value, message in [
            ("id", "D99", "unknown teaching chapter"),
            ("coverage", "complete", "coverage must be"),
            ("coverage", [], "coverage must be"),
            ("href", "https://example.com/deck.html", "local course presentation"),
            ("href", "../outside.html", "local course presentation"),
            ("href", "prototypes/deck.html#bad fragment", "local course presentation"),
        ]:
            changed = deepcopy(self.catalog)
            changed["presentations"][0]["chapters"][0][field] = value
            cases.append((changed, message))
        for catalog, message in cases:
            with (
                self.subTest(message=message),
                self.assertRaisesRegex(b.ExpansionError, message),
            ):
                self.resolve(catalog=catalog)

    def test_real_catalog_places_selected_topics_without_claiming_whole_chapters(self):
        course = b.load_course()
        chapters = {c["id"]: c for c in course["chapters"]}
        self.assertEqual(len(chapters), 17)
        self.assertEqual(chapters["D12"]["number"], 5)
        self.assertEqual(chapters["D13"]["number"], 14)
        self.assertEqual(chapters["capstone"]["number"], 17)
        self.assertEqual(
            len({p["id"] for c in chapters.values() for p in c["presentations"]}), 8
        )
        for did in ("D05", "D06", "D10", "D11"):
            with self.subTest(chapter=did):
                self.assertTrue(chapters[did]["presentations"])
                self.assertTrue(
                    all(
                        p["coverage"] == "selected"
                        for p in chapters[did]["presentations"]
                    )
                )
        self.assertEqual(
            chapters["D11"]["presentations"][0]["href"],
            "prototypes/cooling-format.html?teach=1#rejection",
        )
        self.assertEqual(chapters["D13"]["presentations"], [])
        self.assertEqual(chapters["D03"]["presentations"][0]["coverage"], "chapter")
        self.assertEqual(chapters["D03"]["presentations"][0]["href"], "prototypes/siting-format.html?teach=1")

    def test_numbered_markdown_uses_the_same_chapter_identity(self):
        course = b.load_course()
        lesson = next(l for l in course["lessons"] if l["domain"] == "D02")
        markdown = b.lesson_markdown(
            lesson, {s["id"]: s for s in course["sources"]}, chapters=course["chapters"]
        )
        self.assertIn("**3. Workloads and requirements · Authored draft**", markdown)

    def test_every_presentation_has_a_named_course_exit_in_its_header(self):
        class HeaderLinks(HTMLParser):
            def __init__(self):
                super().__init__()
                self.header = False
                self.current = None
                self.links = []

            def handle_starttag(self, tag, attrs):
                if tag == "header":
                    self.header = True
                if tag == "a" and self.header:
                    self.current = [dict(attrs).get("href", ""), ""]

            def handle_data(self, data):
                if self.current is not None:
                    self.current[1] += data

            def handle_endtag(self, tag):
                if tag == "a" and self.current is not None:
                    self.links.append(self.current)
                    self.current = None
                if tag == "header":
                    self.header = False

        root = Path(__file__).resolve().parents[1]
        course = b.load_course()
        paths = {
            p["href"].split("?")[0].split("#")[0]
            for c in course["chapters"] for p in c["presentations"]
        } | {"sample.html", "prototypes/case-studies.html"}
        for path in paths:
            with self.subTest(presentation=path):
                parser = HeaderLinks()
                parser.feed((root / "course" / path).read_text())
                self.assertTrue(any(
                    label.strip() == "← Back to course"
                    and href in {"index.html?view=slides", "../index.html?view=slides"}
                    for href, label in parser.links
                ), f"Missing explicit course exit in {path}")


if __name__ == "__main__":
    unittest.main()
