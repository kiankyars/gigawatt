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

    def test_one_domain_can_split_into_contiguous_chapters_with_distinct_reading(self):
        self.lessons.append({"id": "workload-detail", "domain": "D02"})
        self.catalog["chapter_splits"] = {"D02": [
            {"id": "D02", "title": "Workload goals", "lesson_ids": ["workload-brief"]},
            {"id": "D02-detail", "title": "Workload mechanisms", "lesson_ids": ["workload-detail"]},
        ]}
        self.catalog["presentations"][0]["chapters"][0]["id"] = "D02-detail"
        chapters = self.resolve()
        self.assertEqual([(c["number"], c["id"]) for c in chapters][-3:],
                         [(3, "D02"), (4, "D02-detail"), (5, "capstone")])
        self.assertEqual(chapters[3]["domain"], "D02")
        self.assertEqual(chapters[3]["lesson_ids"], ["workload-detail"])
        self.assertEqual(chapters[3]["presentations"][0]["id"], "workloads")
        self.assertIn('"workloads": "4. Workloads and requirements"', b.presentation_identities(chapters))
        for ids in (["workload-brief"], ["unknown"], []):
            bad = deepcopy(self.catalog)
            bad["chapter_splits"]["D02"][1]["lesson_ids"] = ids
            with self.subTest(ids=ids), self.assertRaises(b.ExpansionError):
                self.resolve(catalog=bad)

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

    def test_handoff_uses_next_chapter_reading_and_preserves_presentation_entry(self):
        chapters = self.resolve()
        route = b.presentation_routes(chapters)[0]
        self.assertEqual(route["path"], "deck.html")
        self.assertEqual(route["next"], {
            "number": 4,
            "title": "Putting an AI Factory Together",
            "href": "../index.html#exercise",
            "kind": "reading",
        })
        chapters[1]["presentations"] = [{"id": "previous", "href": "prototypes/previous.html"}]
        previous = b.presentation_routes(chapters)[0]
        self.assertEqual(previous["next"]["href"], "deck.html?teach=1#start")
        self.assertEqual(previous["next"]["number"], 3)

    def test_shared_deck_handoff_starts_after_last_covered_chapter(self):
        chapters = self.resolve()
        chapters[1]["presentations"] = deepcopy(chapters[2]["presentations"])
        routes = b.presentation_routes(chapters)
        self.assertEqual(len(routes), 1)
        self.assertEqual(routes[0]["next"]["number"], 4)
        chapters[-1]["presentations"] = deepcopy(chapters[2]["presentations"])
        self.assertIsNone(b.presentation_routes(chapters)[0]["next"])

    def test_handoff_paths_are_rebased_by_site_staging(self):
        from gigawatt.stage_site import published_text

        generated = b.presentation_identities(b.load_course()["chapters"])
        staged = published_text(generated, "course/prototypes/teaching-navigation.js")
        self.assertIn('"path": "siting.html"', staged)
        self.assertIn('"href": "site-design.html?teach=1"', staged)
        self.assertNotIn("-format.html", staged)

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

    def test_real_catalog_has_one_complete_deck_for_every_chapter(self):
        course = b.load_course()
        chapters = {c["id"]: c for c in course["chapters"]}
        self.assertEqual(len(chapters), 16)
        self.assertEqual(chapters["D12"]["number"], 5)
        self.assertEqual(chapters["D13"]["number"], 13)
        self.assertEqual(chapters["capstone"]["number"], 16)
        self.assertEqual(
            len({p["id"] for c in chapters.values() for p in c["presentations"]}), 16
        )
        for did in chapters:
            with self.subTest(chapter=did):
                self.assertTrue(chapters[did]["presentations"])
                self.assertTrue(
                    all(
                        p["coverage"] == "chapter"
                        for p in chapters[did]["presentations"]
                    )
                )
        self.assertEqual(
            chapters["D11"]["presentations"][0]["href"],
            "prototypes/heat-rejection-format.html?teach=1",
        )
        self.assertEqual(chapters["D13"]["presentations"], [{
            "id": "procurement-cases",
            "title": "EPC",
            "href": "prototypes/procurement-cases-format.html?teach=1",
            "coverage": "chapter",
        }])
        self.assertEqual(chapters["D04"]["presentations"][0]["href"], "prototypes/distribution-format.html?teach=1")
        self.assertEqual(chapters["D04"]["presentations"][0]["coverage"], "chapter")
        self.assertEqual(chapters["D03"]["presentations"][0]["coverage"], "chapter")
        self.assertEqual(chapters["D03"]["presentations"][0]["href"], "prototypes/siting-format.html?teach=1")
        for did, deck in (("D05", "continuity"), ("D06", "rack-energy"), ("D06-DC", "dc-distribution"), ("D14", "operations")):
            with self.subTest(chapter=did):
                self.assertEqual(len(chapters[did]["presentations"]), 1)
                presentation = chapters[did]["presentations"][0]
                self.assertEqual(presentation["id"], deck)
                self.assertEqual(presentation["coverage"], "chapter")
                self.assertEqual(presentation["href"], f"prototypes/{deck}-format.html?teach=1")

    def test_numbered_markdown_uses_the_same_chapter_identity(self):
        course = b.load_course()
        lesson = next(l for l in course["lessons"] if l["domain"] == "D02")
        markdown = b.lesson_markdown(
            lesson, {s["id"]: s for s in course["sources"]}, chapters=course["chapters"]
        )
        self.assertIn("**3. Workloads and requirements · Authored draft**", markdown)

    def test_compute_and_storage_are_further_reading_and_chapter_numbers_remain_contiguous(self):
        course = b.load_course()
        chapters = course["chapters"]
        self.assertEqual([c["number"] for c in chapters], list(range(1, 17)))
        self.assertNotIn("D07", [c["id"] for c in chapters])
        reference = course["references"][0]
        self.assertEqual(reference["id"], "D07")
        self.assertNotIn("number", reference)
        self.assertEqual(set(reference["lesson_ids"]), {
            "d07-data-path", "d07-bottleneck-model", "d07-rack-as-system",
        })
        self.assertEqual(reference["presentations"], [])
        self.assertEqual([l["id"] for l in course["lessons"] if l["domain"] == "D07"], reference["lesson_ids"])
        storage = next(r for r in course["references"] if r["id"] == "D09")
        self.assertNotIn("number", storage)
        self.assertEqual(len(storage["lesson_ids"]), 3)
        self.assertEqual(storage["presentations"], [])
        self.assertNotIn("D09", [c["id"] for c in chapters])
        self.assertNotIn("storage-format.html", b.presentation_identities(chapters))
        rack_check = next(l["domain_checkin"] for l in course["lessons"] if l["id"] == "d06-eight-hundred-volt-architectures")
        self.assertEqual(rack_check["next_domain"], "D08")
        self.assertNotIn("compute-format.html", b.presentation_identities(chapters))

    def test_rack_split_preserves_reading_ownership_and_places_checkin_after_dc(self):
        course = b.load_course()
        chapters = {c["id"]: c for c in course["chapters"]}
        self.assertEqual(chapters["D06"]["number"], 8)
        self.assertEqual(chapters["D06"]["lesson_ids"], ["d06-conversion-ledger", "d06-rack-migration"])
        self.assertEqual(chapters["D06-DC"]["number"], 9)
        self.assertEqual(chapters["D06-DC"]["lesson_ids"], ["d06-eight-hundred-volt-architectures"])
        lessons = [l for l in course["lessons"] if l["domain"] == "D06"]
        self.assertEqual([l["id"] for l in lessons], chapters["D06"]["lesson_ids"] + chapters["D06-DC"]["lesson_ids"])
        self.assertFalse(any("domain_checkin" in l for l in lessons[:-1]))
        self.assertIn("domain_checkin", lessons[-1])
        markdown = b.lesson_markdown(lessons[-1], {s["id"]: s for s in course["sources"]}, chapters=course["chapters"])
        self.assertIn("**9. 800 V DC distribution · Authored draft**", markdown)

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
