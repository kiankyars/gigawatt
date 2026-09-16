from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt.stage_site import (
    INTRODUCTION_REDIRECTS, PRESENTATION_REDIRECTS, ROOT, SHARED_PRESENTATION_MODULES,
    public_path, published_text, published_url, stage,
)


class SiteStagingTests(unittest.TestCase):
    def test_rebasing_preserves_delimiters_in_dynamic_reading_links(self):
        source = "course/prototypes/site-format.html"
        code = "link.href='../index.html#'+scene.reference; query='../index.html?'+params;"
        self.assertEqual(published_text(code, source), code)
        self.assertEqual(published_url("../index.html?#", source), "../index.html?#")

    def test_every_retired_introduction_lesson_has_a_current_destination(self):
        introduction = json.loads((ROOT / "course/lessons.json").read_text())
        course = json.loads((ROOT / "course/expanded-course.json").read_text())
        self.assertEqual(set(INTRODUCTION_REDIRECTS), {lesson["id"] for lesson in introduction["lessons"]})
        self.assertLessEqual(set(INTRODUCTION_REDIRECTS.values()), {lesson["id"] for lesson in course["lessons"]})

    def test_reader_is_root_and_shared_deep_links_keep_query_and_fragment(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Course")
            (root / "course/prototypes").mkdir(parents=True)
            (root / "course/index.html").write_text('<title>Reader</title><a href="prototypes/siting-format.html?teach=1#fuel">Slides</a>')
            (root / "course/prototypes/siting-format.html").write_text('<title>Siting</title><a href="../index.html#d03-service-and-siting">Reading</a>')
            original = root / "diagram/index.html"
            original.parent.mkdir()
            original.write_text("Retired introduction content")
            destination = stage(root)

            self.assertEqual(original.read_text(), "Retired introduction content")
            reader = (destination / "index.html").read_text()
            self.assertIn('<title>Reader</title>', reader)
            self.assertIn('href="slides/siting.html?teach=1#fuel"', reader)
            self.assertIn('href="../index.html#d03-service-and-siting"', (destination / "slides/siting.html").read_text())
            for path, target in {
                "course/index.html": "../index.html",
                "course/prototypes/siting-format.html": "../../slides/siting.html",
                "diagram/index.html": "../index.html",
                "course.html": "index.html",
                "v1.html": "index.html",
            }.items():
                with self.subTest(path=path):
                    redirect = (destination / path).read_text()
                    self.assertIn(f'href="{target}"', redirect)
                    self.assertIn("location.search+hash", redirect)
            self.assertIn('"ride-through": "d05-storage-power-and-time"', (destination / "diagram/index.html").read_text())
            self.assertIn("const lessons={};", (destination / "course/prototypes/siting-format.html").read_text())

    def test_module_imports_dynamic_assets_and_reader_links_are_rebased(self):
        cases = [
            ("course/index.html", "prototypes/orientation-format.html?teach=1#network-preview", "slides/overview.html?teach=1#network-preview"),
            ("course/teach.html", "./prototypes/teaching-navigation.js", "./teaching-navigation.js"),
            ("course/teach.html", "assets/slide-chrome.css", "../assets/slide-chrome.css"),
            ("course/prototypes/workload-format.html", "./workload-scenes.js", "./workload-scenes.js"),
            ("course/prototypes/workload-format.html", "siting-format.html?teach=1", "siting.html?teach=1"),
            ("course/prototypes/rack-power-format.html", "../teach.html", "800v.html"),
            ("course/index.html", "../research/sources/P01.md", "research/sources/P01.md"),
            ("course/teach.html", "assets/${figure.asset}", "../assets/${figure.asset}"),
            ("course/index.html", "https://example.com/course/index.html", "https://example.com/course/index.html"),
            ("course/index.html", "#d01-boundaries", "#d01-boundaries"),
        ]
        for source, url, expected in cases:
            with self.subTest(source=source, url=url):
                self.assertEqual(published_url(url, source), expected)
        content = '<img src="assets/${figure.asset}"><script>import {x} from "./prototypes/teaching-navigation.js";</script>'
        result = published_text(content, "course/teach.html")
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

    def test_consolidated_decks_keep_old_urls_and_shared_module_imports(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Course")
            (root / "course/prototypes").mkdir(parents=True)
            (root / "course/web").mkdir()
            for deck in ("continuity", "rack-energy", "dc-distribution", "ups", "rack-power"):
                (root / f"course/prototypes/{deck}-format.html").write_text(f"<title>{deck}</title>")
            (root / "course/teach.html").write_text("<title>Legacy 800 V</title>")
            for name in SHARED_PRESENTATION_MODULES:
                (root / "course/web" / name).write_text("/* shared module */")
            (root / "course/prototypes/rack-energy-controller.js").write_text(
                "import {createElectricalVisuals} from '../web/electrical-renderer.js';"
            )
            destination = stage(root)
            for old, current in PRESENTATION_REDIRECTS.items():
                with self.subTest(old=old):
                    redirect = (destination / "slides" / old).read_text()
                    self.assertIn(f'href="{current}"', redirect)
                    self.assertIn("location.search+hash", redirect)
                    self.assertIn("const lessons={};", redirect)
            self.assertIn("<title>continuity</title>", (destination / "slides/continuity.html").read_text())
            self.assertIn("<title>rack-energy</title>", (destination / "slides/rack-energy.html").read_text())
            for name in SHARED_PRESENTATION_MODULES:
                self.assertTrue((destination / "web" / name).is_file())
                self.assertTrue((destination / "course/web" / name).is_file())
            self.assertIn("'../web/electrical-renderer.js'", (destination / "slides/rack-energy-controller.js").read_text())
            self.assertIn('href="../../slides/ups.html"', (destination / "course/prototypes/ups-format.html").read_text())

    def test_all_published_decks_have_clean_paths(self):
        self.assertEqual(str(public_path("course/index.html")), "index.html")
        self.assertEqual(str(public_path("course/teach.html")), "slides/800v.html")
        self.assertEqual(str(public_path("course/prototypes/site-format.html")), "slides/site-design.html")
        self.assertEqual(str(public_path("course/prototypes/procurement-cases-format.html")), "slides/procurement-cases.html")
        for source in (ROOT / "course/prototypes").glob("*.html"):
            target = str(public_path(source.relative_to(ROOT)))
            self.assertTrue(target.startswith("slides/"))
            self.assertNotIn("prototypes", target)
            self.assertNotIn("-format", target)

    def test_houdini_case_redirect_is_rebased_for_the_published_slide_location(self):
        source = "course/prototypes/site-scenes.js"
        code = (ROOT / source).read_text()
        published = published_text(code, source)
        self.assertIn('new URL("./procurement-cases.html", moduleHref)', published)
        self.assertIn('destination.search = current.search;', published)
        self.assertIn('destination.hash = current.hash;', published)

    def test_moved_chapter_eight_fragments_target_a_published_deck(self):
        for filename in ("continuity-main.js", "distribution-player.js"):
            with self.subTest(filename=filename):
                source = f"course/prototypes/{filename}"
                published = published_text((ROOT / source).read_text(), source)
                self.assertIn('location.replace("rack-energy.html" + location.search', published)
                self.assertNotIn('rack-energy-format.html', published)
        self.assertEqual(public_path("course/prototypes/rack-energy-format.html").name, "rack-energy.html")

    def test_compute_redirect_destinations_rebase_to_live_slide_paths(self):
        source = "course/prototypes/compute-migration.js"
        published = published_text((ROOT / source).read_text(), source)
        for destination in (
            "networking.html#networking-purpose", "networking.html#consumer-hardware-meme",
            "workloads.html#operand-reuse", "rack-energy.html#rack-hardware-anatomy",
            "storage.html#tray-repair", "../index.html#d07-bottleneck-model",
        ):
            self.assertIn(destination, published)
        self.assertNotIn("-format.html", published)


if __name__ == "__main__":
    unittest.main()
