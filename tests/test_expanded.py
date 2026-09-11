from __future__ import annotations

import json
import unittest
from copy import deepcopy
from unittest.mock import patch

from gigawatt import build_expanded as b
from gigawatt.build_presentation import validate_presentation
from gigawatt.research import canonical_url


class ExpansionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.course = b.load_course()
        cls.raw = b.read(b.ROOT / "course/expansion/foundations-power.json")[0]
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
        self.assertEqual(
            {
                l["capstone_id"]
                for l in self.course["lessons"]
                if l["domain"] == "capstone"
            },
            {c["id"] for c in b.read(b.ROOT / "course/domain-map.json")["capstones"]},
        )

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
        changed = original_read(b.ROOT / "course/expansion/capstones.json")
        changed[0]["capstone_id"] = "C99"

        def read(path):
            return changed if path.name == "capstones.json" else original_read(path)

        with (
            patch.object(b, "read", side_effect=read),
            self.assertRaisesRegex(b.ExpansionError, "capstone IDs"),
        ):
            b.load_course()

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

    def test_presentation_contract_requires_a_problem_mechanism_and_transfer(self):
        data = b.read(b.ROOT / "course/expansion/sample-presentation.json")
        validate_presentation(data)
        for field in ("fixed_boundary", "primary_payoff", "transfer_question"):
            changed = deepcopy(data)
            changed["learning_contract"][field] = ""
            with self.assertRaisesRegex(ValueError, "learning contract"):
                validate_presentation(changed)
        changed = deepcopy(data)
        changed["steps"][-1]["pedagogical_role"] = "balance"
        with self.assertRaisesRegex(ValueError, "changed-case transfer"):
            validate_presentation(changed)

    def test_presentation_contract_allows_authored_sequence_lengths(self):
        data = b.read(b.ROOT / "course/expansion/sample-presentation.json")
        data["steps"] = [
            data["steps"][0],
            next(s for s in data["steps"] if s["pedagogical_role"] == "mechanism"),
            data["steps"][-1],
        ]
        data["aliases"] = {}
        data["planned_duration_seconds"] = sum(
            s["duration_seconds"] for s in data["steps"]
        )
        validate_presentation(data)
        data["aliases"] = {"old-scene": "missing-scene"}
        with self.assertRaisesRegex(ValueError, "missing scene"):
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
        lesson = next(l for l in self.course["lessons"] if l["id"] == "d04-conversion-placement")
        figures = [f for s in lesson["sections"] for f in s.get("figures", [])]
        self.assertEqual(len(figures), 2)
        sources = {s["id"]: s for s in self.course["sources"]}
        markdown = b.lesson_markdown(lesson, sources, asset_prefix="../assets/")
        for figure in figures:
            self.assertIn(f"../assets/{figure['asset']}", markdown)
            self.assertIn(figure["source_url"], markdown)
            self.assertTrue((b.ROOT / "course/assets" / figure["asset"]).is_file())
        changed = deepcopy(self.raw)
        changed["sections"][0]["figures"] = [dict(figures[0], asset="../../private.png")]
        with self.assertRaisesRegex(b.ExpansionError, "Unsafe reference figure path"):
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


if __name__ == "__main__":
    unittest.main()
