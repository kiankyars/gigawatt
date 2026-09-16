from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt.stage_site import (
    ROOT, SHARED_PRESENTATION_MODULES,
    public_path, published_text, published_url, stage,
)


def catalog(root, *decks):
    (root / "course").mkdir(parents=True, exist_ok=True)
    (root / "course/teaching-sequences.json").write_text(json.dumps({
        "presentations": [{"id": name, "chapters": [{"href": f"prototypes/{name}-format.html?teach=1"}]} for name in decks]
    }))


class SiteStagingTests(unittest.TestCase):
    def test_rebasing_preserves_delimiters_in_dynamic_reading_links(self):
        source = "course/prototypes/site-format.html"
        code = "link.href='../index.html#'+scene.reference; query='../index.html?'+params;"
        self.assertEqual(published_text(code, source), code)
        self.assertEqual(published_url("../index.html?#", source), "../index.html?#")

    def test_reader_and_current_presentations_have_one_canonical_path(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root, "siting")
            (root / "README.md").write_text("Course")
            (root / "course/prototypes").mkdir(parents=True)
            (root / "course/index.html").write_text('<title>Reader</title><a href="prototypes/siting-format.html?teach=1#fuel">Slides</a>')
            (root / "course/prototypes/siting-format.html").write_text('<title>Siting</title><a href="../index.html#d03-service-and-siting">Reading</a>')
            (root / "course/prototypes/presenter.html").write_text('<title>Presenter</title>')
            (root / "course/prototypes/case-studies.html").write_text('<title>Case studies</title>')
            (root / "course/domain-map.html").write_text('<title>Domain map</title>')
            original = root / "diagram/index.html"
            original.parent.mkdir()
            original.write_text("Retired introduction content")
            destination = stage(root)

            self.assertEqual(original.read_text(), "Retired introduction content")
            reader = (destination / "index.html").read_text()
            self.assertIn('<title>Reader</title>', reader)
            self.assertIn('href="slides/siting.html?teach=1#fuel"', reader)
            self.assertIn('href="../index.html#d03-service-and-siting"', (destination / "slides/siting.html").read_text())
            self.assertTrue((destination / "slides/presenter.html").exists())
            self.assertTrue((destination / "slides/case-studies.html").exists())
            self.assertTrue((destination / "domain-map.html").exists())
            for path in ("course", "diagram", "course.html", "v1.html", "STRATEGY.md"):
                self.assertFalse((destination / path).exists(), path)

    def test_module_imports_dynamic_assets_and_reader_links_are_rebased(self):
        cases = [
            ("course/index.html", "prototypes/orientation-format.html?teach=1#network-preview", "slides/overview.html?teach=1#network-preview"),
            ("course/prototypes/workload-format.html", "./workload-scenes.js", "./workload-scenes.js"),
            ("course/prototypes/workload-format.html", "siting-format.html?teach=1", "siting.html?teach=1"),
            ("course/prototypes/dc-distribution-format.html", "../assets/${figure.asset}", "../assets/${figure.asset}"),
            ("course/index.html", "../research/sources/P01.md", "research/sources/P01.md"),
            ("course/index.html", "https://example.com/course/index.html", "https://example.com/course/index.html"),
            ("course/index.html", "#d01-boundaries", "#d01-boundaries"),
        ]
        for source, url, expected in cases:
            with self.subTest(source=source, url=url):
                self.assertEqual(published_url(url, source), expected)
        content = '<img src="../assets/${figure.asset}"><script>import {x} from "./teaching-navigation.js";</script>'
        result = published_text(content, "course/prototypes/dc-distribution-format.html")
        self.assertIn('src="../assets/${figure.asset}"', result)
        self.assertIn('from "./teaching-navigation.js"', result)

    def test_embedded_json_is_rewritten_even_when_prose_contains_quotes(self):
        source = '<p>Do not assume a diagram’s arrow explains "everything".</p><script type="application/json">' + json.dumps({
            "prose": "Don't assume a generated image's typography is a circuit.",
            "href": "prototypes/workload-format.html?teach=1#next-brief",
        }) + '</script>'
        result = published_text(source, "course/index.html")
        self.assertIn('"href": "slides/workloads.html?teach=1#next-brief"', result)
        self.assertIn("Don't assume a generated image's typography", result)

    def test_source_index_and_project_readme_do_not_collide(self):
        self.assertEqual(str(public_path("README.md")), "README.md")
        self.assertEqual(str(public_path("course/README.md")), "SOURCE_INDEX.md")

    def test_only_cataloged_decks_publish_with_their_shared_modules(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root, "continuity", "rack-energy", "dc-distribution")
            (root / "README.md").write_text("Course")
            (root / "course/prototypes").mkdir(parents=True)
            (root / "course/web").mkdir()
            for deck in ("continuity", "rack-energy", "dc-distribution", "ups", "rack-power", "compute"):
                (root / f"course/prototypes/{deck}-format.html").write_text(f"<title>{deck}</title>")
            for name in ("teach.html", "sample.html", "sample-notes.html"):
                (root / "course" / name).write_text("<title>Retired presentation</title>")
            for name in SHARED_PRESENTATION_MODULES:
                (root / "course/web" / name).write_text("/* shared module */")
            (root / "course/prototypes/rack-energy-controller.js").write_text(
                "import {createElectricalVisuals} from '../web/electrical-renderer.js';"
            )
            destination = stage(root)
            for deck in ("continuity", "rack-energy", "dc-distribution"):
                self.assertIn(f"<title>{deck}</title>", (destination / "slides" / f"{deck}.html").read_text())
            for name in ("ups.html", "rack-power.html", "compute.html", "800v.html", "800v-explore.html", "800v-notes.html"):
                self.assertFalse((destination / "slides" / name).exists(), name)
            for name in ("teach.html", "sample.html", "sample-notes.html"):
                self.assertFalse((destination / name).exists(), name)
            for name in SHARED_PRESENTATION_MODULES:
                self.assertTrue((destination / "web" / name).is_file())
            self.assertFalse((destination / "course").exists())
            self.assertIn("'../web/electrical-renderer.js'", (destination / "slides/rack-energy-controller.js").read_text())

    def test_restaging_removes_retired_generated_routes(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root, "siting")
            (root / "README.md").write_text("Course")
            destination = stage(root)
            stale = destination / "course/index.html"
            stale.parent.mkdir()
            stale.write_text("Old reader redirect")
            (destination / "v1.html").write_text("Old introduction redirect")
            self.assertEqual(stage(root), destination)
            self.assertFalse(stale.exists())
            self.assertFalse((destination / "v1.html").exists())

    def test_staging_does_not_replace_an_unrelated_directory(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root)
            destination = root / "notes"
            destination.mkdir()
            note = destination / "keep.md"
            note.write_text("Keep this")
            with self.assertRaisesRegex(ValueError, "non-staged directory"):
                stage(root, destination)
            self.assertEqual(note.read_text(), "Keep this")

    def test_all_cataloged_decks_have_clean_paths(self):
        self.assertEqual(str(public_path("course/index.html")), "index.html")
        self.assertEqual(str(public_path("course/prototypes/site-format.html")), "slides/site-design.html")
        self.assertEqual(str(public_path("course/prototypes/procurement-cases-format.html")), "slides/procurement-cases.html")
        presentations = json.loads((ROOT / "course/teaching-sequences.json").read_text())["presentations"]
        for presentation in presentations:
            for chapter in presentation["chapters"]:
                source = "course/" + chapter["href"].split("?", 1)[0].split("#", 1)[0]
                target = str(public_path(source))
                self.assertTrue(target.startswith("slides/"))
                self.assertNotIn("prototypes", target)
                self.assertNotIn("-format", target)


if __name__ == "__main__":
    unittest.main()
