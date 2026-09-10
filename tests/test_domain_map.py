from __future__ import annotations

import json
import re
import shutil
import subprocess
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt import build_domain_map as atlas


def sources() -> tuple[dict, dict, dict]:
    return tuple(
        json.loads((atlas.ROOT / "course" / name).read_text())
        for name in ("domain-map.json", "research-sources.json", "lessons.json")
    )


class DomainMapTests(unittest.TestCase):
    def test_sources_have_one_mapping_authority(self):
        domain_map, research, lessons = sources()
        domain_map["domains"][0]["source_ids"] = ["stale-duplicate-map"]
        normalized = atlas.validate_map(domain_map, research, lessons)
        for domain in normalized["domains"]:
            self.assertEqual(
                domain["source_ids"],
                [
                    source["id"]
                    for source in research["sources"]
                    if domain["id"] in source["domains"]
                ],
            )
        self.assertEqual(
            domain_map["domains"][0]["source_ids"], ["stale-duplicate-map"]
        )
        self.assertEqual(
            normalized["baseline_lessons"],
            [{"id": l["id"], "title": l["title"]} for l in lessons["lessons"]],
        )

    def test_broken_curriculum_references_fail(self):
        mutations = {
            "duplicate domain": lambda m, r: m["domains"].append(
                deepcopy(m["domains"][0])
            ),
            "duplicate objective": lambda m, r: m["domains"][0]["objectives"].append(
                deepcopy(m["domains"][0]["objectives"][0])
            ),
            "unknown lane": lambda m, r: m["domains"][0].update(lane="unknown"),
            "unknown prerequisite": lambda m, r: m["domains"][0].update(
                prerequisites=["unknown"]
            ),
            "unknown lesson": lambda m, r: m["domains"][0]["objectives"][0].update(
                baseline_lessons=["unknown"]
            ),
            "unsupported completion": lambda m, r: m["domains"][0]["objectives"][
                0
            ].update(baseline_coverage="complete"),
            "empty assessment": lambda m, r: m["domains"][0]["objectives"][0].update(
                assessment=""
            ),
            "missing visual boundary": lambda m, r: m["domains"][0]["visual"].update(
                boundary=""
            ),
            "unknown source domain": lambda m, r: r["sources"][0].update(
                domains=["unknown"]
            ),
            "duplicate source": lambda m, r: r["sources"].append(
                deepcopy(r["sources"][0])
            ),
            "unsafe source ID": lambda m, r: r["sources"][0].update(id="../outside"),
            "executable URL": lambda m, r: r["sources"][0].update(
                url="javascript:alert(1)"
            ),
            "unknown path domain": lambda m, r: m["paths"][0].update(
                domains=["unknown"]
            ),
            "unknown capstone domain": lambda m, r: m["capstones"][0].update(
                domains=["unknown"]
            ),
            "incomplete sequence": lambda m, r: m["sequence"].pop(),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                domain_map, research, lessons = sources()
                mutate(domain_map, research)
                with self.assertRaises(atlas.DomainMapError):
                    atlas.validate_map(domain_map, research, lessons)

    def test_cycles_and_invalid_teaching_order_fail(self):
        domain_map, research, lessons = sources()
        domain_map["domains"][0]["prerequisites"] = [domain_map["domains"][1]["id"]]
        with self.assertRaisesRegex(atlas.DomainMapError, "Prerequisite cycle"):
            atlas.validate_map(domain_map, research, lessons)
        domain_map, research, lessons = sources()
        domain_map["sequence"][0]["domains"].reverse()
        with self.assertRaisesRegex(atlas.DomainMapError, "before prerequisite"):
            atlas.validate_map(domain_map, research, lessons)

    def test_markdown_preserves_every_teaching_contract(self):
        domain_map, research, lessons = sources()
        domain_map = atlas.validate_map(domain_map, research, lessons)
        markdown = atlas.render_markdown(domain_map, research)
        for domain in domain_map["domains"]:
            self.assertIn(f'<a id="{domain["id"].lower()}"></a>', markdown)
            for objective in domain["objectives"]:
                self.assertIn(f"#### {objective['id']}\n", markdown)
                self.assertIn(atlas._md(objective["assessment"]), markdown)
            for key in ("prediction", "interaction", "boundary"):
                self.assertIn(atlas._md(domain["visual"][key]), markdown)
        for capstone in domain_map["capstones"]:
            self.assertIn(atlas._md(capstone["assessment"]), markdown)

    def test_build_is_deterministic_and_embedded_text_stays_inert(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            web = root / "course" / "web"
            web.mkdir(parents=True)
            domain_map, research, lessons = sources()
            domain_map["title"] = (
                "</script><script>alert(1)</script> __RESEARCH_SOURCES_JSON__"
            )
            for name, value in zip(
                ("domain-map.json", "research-sources.json", "lessons.json"),
                (domain_map, research, lessons),
            ):
                (root / "course" / name).write_text(json.dumps(value))
            (web / "domain-map.html").write_text(
                "<script>const MAP=__DOMAIN_MAP_JSON__; const RESEARCH=__RESEARCH_SOURCES_JSON__;</script>"
            )
            outputs = atlas.build(root)
            self.assertEqual(outputs, atlas.build(root))
            html = outputs[atlas.OUTPUTS[0]]
            self.assertIn(r"\u003c/script>", html)
            self.assertNotIn("<script>alert(1)", html)
            self.assertIn("__RESEARCH_SOURCES_JSON__", html)
            self.assertEqual(html.count("</script>"), 1)
            (root / "course" / "domain-map.json").write_text(
                '{"title":"first","title":"second"}'
            )
            with self.assertRaisesRegex(atlas.DomainMapError, "Duplicate JSON key"):
                atlas.build(root)

    def test_declared_local_links_must_exist_and_stay_inside_repository(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "course").mkdir()
            (root / "course" / "REVIEW.md").write_text("Review")
            atlas.validate_template_links(
                '<a href="REVIEW.md">Review</a><a href="DOMAIN_MAP.md">Generated</a><a href="#overview">Map</a>',
                root,
            )
            for target in ("missing.md", "../../outside.md"):
                with (
                    self.subTest(target=target),
                    self.assertRaises(atlas.DomainMapError),
                ):
                    atlas.validate_template_links(f'<a href="{target}">Link</a>', root)

    def test_check_detects_stale_html_or_markdown_without_writing(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            outputs = {atlas.OUTPUTS[0]: "HTML\n", atlas.OUTPUTS[1]: "Markdown\n"}
            atlas.write_or_check(root, outputs, check=False)
            atlas.write_or_check(root, outputs, check=True)
            destination = root / atlas.OUTPUTS[1]
            destination.write_text("stale")
            with self.assertRaisesRegex(atlas.DomainMapError, "stale"):
                atlas.write_or_check(root, outputs, check=True)
            self.assertEqual(destination.read_text(), "stale")

    @unittest.skipUnless(
        shutil.which("node"), "Node is needed for JavaScript syntax validation"
    )
    def test_template_script_has_valid_syntax_with_real_data(self):
        domain_map, research, lessons = sources()
        template = (atlas.ROOT / "course" / "web" / "domain-map.html").read_text()
        script = re.search(r"<script>([\s\S]*?)</script>", template)[1]
        values = {
            atlas.PLACEHOLDERS[0]: json.dumps(
                atlas.validate_map(domain_map, research, lessons)
            ),
            atlas.PLACEHOLDERS[1]: json.dumps(research),
        }
        script = re.sub(
            "|".join(map(re.escape, atlas.PLACEHOLDERS)),
            lambda match: values[match[0]],
            script,
        )
        result = subprocess.run(
            ["node", "--check"],
            input=script,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
