from __future__ import annotations

import json
import os
import posixpath
import re
import struct
import sys
import unittest
import zlib
from pathlib import Path, PurePosixPath
from tempfile import TemporaryDirectory
from unittest import mock
from urllib.parse import urljoin, urlsplit

from gigawatt.stage_site import (
    MIN_PSNR, PUBLISHED_FILES, REPOSITORY_URL, ROOT, SHARED_PRESENTATION_MODULES, has_alpha,
    image_references, public_path, published_files, published_text, published_url, stage, webp_encoder,
)


def catalog(root, *decks):
    (root / "course").mkdir(parents=True, exist_ok=True)
    (root / "course/teaching-sequences.json").write_text(json.dumps({
        "presentations": [{"id": name, "chapters": [{"href": f"prototypes/{name}-format.html?teach=1"}]} for name in decks]
    }))


def png(path, width=96, height=64, alpha=False):
    """Write a small gradient PNG without an imaging library."""
    channels = 4 if alpha else 3
    pixel = lambda x, y: (x * 2 % 256, y * 3 % 256, (x + y) % 256, 255)[:channels]
    rows = b"".join(b"\x00" + bytes(v for x in range(width) for v in pixel(x, y)) for y in range(height))
    chunk = lambda kind, data: (
        struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data) & 0xFFFFFFFF)
    )
    header = struct.pack(">IIBBBBB", width, height, 8, 6 if alpha else 2, 0, 0, 0)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header) + chunk(b"IDAT", zlib.compress(rows, 0)) + chunk(b"IEND", b""))
    return path


class SiteStagingTests(unittest.TestCase):
    def test_rebasing_preserves_delimiters_in_dynamic_reading_links(self):
        source = "course/prototypes/site-format.html"
        code = "link.href='../index.html#'+scene.reference; query='../index.html?'+params;"
        expected = "link.href='../read.html#'+scene.reference; query='../read.html?'+params;"
        self.assertEqual(published_text(code, source), expected)
        self.assertEqual(published_url("../index.html?#", source), "../read.html?#")

    def test_homepage_reader_and_current_presentations_have_distinct_canonical_paths(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root, "siting")
            (root / "README.md").write_text("Course")
            (root / "course/prototypes").mkdir(parents=True)
            (root / "course/homepage.html").write_text('<title>Homepage</title><a href="index.html#d03-service-and-siting">Read</a><script src="home/main.js"></script>')
            (root / "course/index.html").write_text('<title>Reader</title><a href="homepage.html">Home</a><a href="prototypes/siting-format.html?teach=1#fuel">Slides</a>')
            (root / "course/prototypes/siting-format.html").write_text('<title>Siting</title><a href="../index.html#d03-service-and-siting">Reading</a>')
            (root / "course/prototypes/presenter.html").write_text('<title>Presenter</title>')
            (root / "course/prototypes/case-studies.html").write_text('<title>Case studies</title>')
            (root / "course/domain-map.html").write_text('<title>Domain map</title>')
            original = root / "diagram/index.html"
            original.parent.mkdir()
            original.write_text("Retired introduction content")
            destination = stage(root)

            self.assertEqual(original.read_text(), "Retired introduction content")
            homepage = (destination / "index.html").read_text()
            self.assertIn('<title>Homepage</title>', homepage)
            self.assertIn('href="read.html#d03-service-and-siting"', homepage)
            self.assertIn('src="home/main.js"', homepage)
            reader = (destination / "read.html").read_text()
            self.assertIn('<title>Reader</title>', reader)
            self.assertIn('href="index.html"', reader)
            self.assertIn('href="slides/siting.html?teach=1#fuel"', reader)
            self.assertIn('href="../read.html#d03-service-and-siting"', (destination / "slides/siting.html").read_text())
            self.assertTrue((destination / "slides/presenter.html").exists())
            self.assertTrue((destination / "slides/case-studies.html").exists())
            self.assertTrue((destination / "domain-map.html").exists())
            for path in ("course", "diagram", "course.html", "homepage.html", "v1.html", "STRATEGY.md"):
                self.assertFalse((destination / path).exists(), path)

    def test_homepage_assets_publish_recursively_with_rebased_links(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root)
            (root / "course/home/vendor").mkdir(parents=True)
            (root / "course/home/main.js").write_text(
                "import {scene} from './vendor/scene.js'; const reading='../index.html#d01-boundaries';"
            )
            (root / "course/home/vendor/scene.js").write_text("export const scene = 'campus';")
            (root / "course/home/main.css").write_text("body { color: #123; }")
            (root / "course/home/vendor/data.bin").write_bytes(bytes([0, 128, 255]))
            destination = stage(root)
            self.assertEqual(
                (destination / "home/main.js").read_text(),
                "import {scene} from './vendor/scene.js'; const reading='../read.html#d01-boundaries';",
            )
            self.assertEqual((destination / "home/vendor/scene.js").read_text(), "export const scene = 'campus';")
            self.assertEqual((destination / "home/main.css").read_text(), "body { color: #123; }")
            self.assertEqual((destination / "home/vendor/data.bin").read_bytes(), bytes([0, 128, 255]))

    def test_module_imports_dynamic_assets_and_reader_links_are_rebased(self):
        cases = [
            ("course/homepage.html", "index.html#d01-boundaries", "read.html#d01-boundaries"),
            ("course/homepage.html", "prototypes/terminology-format.html?teach=1", "slides/primer.html?teach=1"),
            ("course/homepage.html", "home/main.js", "home/main.js"),
            ("course/index.html", "homepage.html", "index.html"),
            ("course/index.html", "prototypes/orientation-format.html?teach=1#network-preview", "slides/overview.html?teach=1#network-preview"),
            ("course/prototypes/workload-format.html", "./workload-scenes.js", "./workload-scenes.js"),
            ("course/prototypes/workload-format.html", "siting-format.html?teach=1", "siting.html?teach=1"),
            ("course/prototypes/workload-format.html", "../index.html#d02-workloads", "../read.html#d02-workloads"),
            ("course/prototypes/workload-format.html", "../homepage.html", "../index.html"),
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
            for deck in ("continuity", "rack-energy", "dc-distribution", "ups", "rack-power", "compute", "storage"):
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

    def test_a_stage_that_stopped_partway_is_replaced(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root)
            with mock.patch("gigawatt.stage_site.convert_images", side_effect=RuntimeError("interrupted")):
                with self.assertRaisesRegex(RuntimeError, "interrupted"):
                    stage(root)
            destination = stage(root)
            self.assertTrue((destination / ".nojekyll").is_file())
            self.assertTrue((destination / "teaching-sequences.json").is_file())

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
        self.assertEqual(str(public_path("course/homepage.html")), "index.html")
        self.assertEqual(str(public_path("course/index.html")), "read.html")
        self.assertEqual(str(public_path("course/home/vendor/scene.js")), "home/vendor/scene.js")
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

    def test_markdown_code_spans_keep_repository_paths(self):
        source = (
            "Editable inputs remain grouped in `course/`; the sequences in `course/prototypes/` "
            "are source files, and `read.html` is generated. See [the reader](index.html) and "
            "[slides](prototypes/siting-format.html?teach=1#fuel).\n\n```sh\nopen course/index.html\n```\n"
        )
        staged = published_text(source, "course/README.md")
        self.assertIn("grouped in `course/`", staged)
        self.assertIn("sequences in `course/prototypes/` are", staged)
        self.assertIn("`read.html` is generated", staged)
        self.assertIn("open course/index.html", staged)
        self.assertIn("[the reader](read.html)", staged)
        self.assertIn("[slides](slides/siting.html?teach=1#fuel)", staged)

    def test_prototypes_folder_publishes_as_slides(self):
        self.assertEqual(str(public_path("course/prototypes")), "slides")
        self.assertEqual(published_url("prototypes/", "course/SLIDE_REMOVAL_AUDIT.md"), "slides/")
        self.assertEqual(published_url("../prototypes/", "course/lessons/d01-boundaries.md"), "../slides/")
        self.assertEqual(published_text("[decks](prototypes/)", "course/COURSE_REVIEW.md"), "[decks](slides/)")

    def test_only_listed_documents_publish_and_other_links_point_to_the_repository(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root, "siting")
            (root / "README.md").write_text("[Course review](course/COURSE_REVIEW.md)")
            (root / "course/prototypes").mkdir(parents=True)
            (root / "course/prototypes/siting-format.html").write_text("<title>Siting</title>")
            (root / "course/COURSE_REVIEW.md").write_text(
                "[Tests](TESTING.md#desktop) [Prompt](CHAPTER_16_CLOSING_IMAGE_PROMPT.md) "
                "[Map](DOMAIN_MAP.md) [Builder](../src/gigawatt/stage_site.py) "
                "[Retired](prototypes/ups-format.html#tier-topology) [Missing](GONE.md) `TESTING.md` "
                "[Diagram](../diagram/index.html#top) [Audit](../qa/reader/) [Repository](../) [Decks](prototypes/)"
            )
            (root / "diagram").mkdir()
            (root / "diagram/index.html").write_text("<title>Diagram</title>")
            (root / "qa/reader").mkdir(parents=True)
            (root / "qa/reader/READER_AUDIT.md").write_text("Audit")
            for name in ("DOMAIN_MAP.md", "TESTING.md", "CHAPTER_16_CLOSING_IMAGE_PROMPT.md", "SCRATCH.md", "lessons.json"):
                (root / "course" / name).write_text(name)
            (root / "course/prototypes/ups-format.html").write_text("<title>Retired</title>")
            (root / "src/gigawatt").mkdir(parents=True)
            (root / "src/gigawatt/stage_site.py").write_text("")
            (root / "research").mkdir()
            for name in ("README.md", "INDEX.md", "memo-2026-09-20.md", "discovery.json"):
                (root / "research" / name).write_text(name)
            (root / "course/sample-reading.html").write_text("<title>One lesson</title>")
            destination = stage(root)

            for name in ("COURSE_REVIEW.md", "DOMAIN_MAP.md", "teaching-sequences.json",
                         "research/README.md", "research/INDEX.md", "slides/siting.html"):
                self.assertTrue((destination / name).is_file(), name)
            for name in ("README.md", "TESTING.md", "CHAPTER_16_CLOSING_IMAGE_PROMPT.md", "SCRATCH.md", "lessons.json",
                         "research/memo-2026-09-20.md", "research/discovery.json", "sample-reading.html",
                         "slides/ups.html"):
                self.assertFalse((destination / name).exists(), name)
            review = (destination / "COURSE_REVIEW.md").read_text()
            self.assertIn(f"[Tests]({REPOSITORY_URL}blob/main/course/TESTING.md#desktop)", review)
            self.assertIn(f"[Prompt]({REPOSITORY_URL}blob/main/course/CHAPTER_16_CLOSING_IMAGE_PROMPT.md)", review)
            self.assertIn(f"[Builder]({REPOSITORY_URL}blob/main/src/gigawatt/stage_site.py)", review)
            self.assertIn("[Map](DOMAIN_MAP.md)", review)
            # Retired pages keep their site address and reach the 404 page; unknown files stay as written.
            self.assertIn("[Retired](slides/ups.html#tier-topology)", review)
            self.assertIn("[Missing](GONE.md)", review)
            self.assertIn("`TESTING.md`", review)
            # Pages and folders outside course/ are never published, so they link to GitHub.
            self.assertIn(f"[Diagram]({REPOSITORY_URL}blob/main/diagram/index.html#top)", review)
            self.assertIn(f"[Audit]({REPOSITORY_URL}tree/main/qa/reader)", review)
            self.assertIn(f"[Repository]({REPOSITORY_URL}tree/main/)", review)
            self.assertIn("[Decks](slides/)", review)

    def test_every_listed_document_exists(self):
        for name in PUBLISHED_FILES:
            self.assertTrue((ROOT / name).is_file(), name)

    def test_every_listed_document_is_linked_from_a_published_page(self):
        """Crawl links from the entry pages so an orphaned document cannot stay on the list."""
        published = {PurePosixPath(path.as_posix()) for path in published_files(ROOT)}
        link = re.compile(r"""\]\(([^\s)]+)\)|(?:href|src)=["']([^"'<>]+)["']""")
        queue = [PurePosixPath(p) for p in ("course/homepage.html", "course/index.html", "course/404.html")]
        reached = set()
        while queue:
            page = queue.pop()
            if page in reached:
                continue
            reached.add(page)
            if page.suffix not in {".html", ".md"}:
                continue
            for match in link.finditer((ROOT / page).read_text(encoding="utf-8")):
                route = urlsplit(match[1] or match[2])
                if route.scheme or route.netloc or not route.path or route.path.startswith("/") or "${" in route.path:
                    continue
                target = PurePosixPath(posixpath.normpath(str(page.parent / route.path)))
                if target in published:
                    queue.append(target)
        for name in PUBLISHED_FILES:
            self.assertIn(PurePosixPath(name), reached, f"{name} is published but no published page links to it")

    def test_not_found_page_publishes_at_the_root_with_absolute_links(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            catalog(root)
            page = '<a href="/gigawatt/">Course homepage</a><a href="/gigawatt/read.html">Course reader</a>'
            (root / "course/404.html").write_text(page)
            destination = stage(root)
            self.assertEqual((destination / "404.html").read_text(), page)
        page = (ROOT / "course/404.html").read_text()
        self.assertIn('href="/gigawatt/"', page)
        self.assertIn('href="/gigawatt/read.html"', page)
        self.assertNotIn("http-equiv", page.lower())

    def test_homepage_chapters_resolve_to_published_slides(self):
        presentations = json.loads((ROOT / "course/teaching-sequences.json").read_text())["presentations"]
        staged = json.loads(published_text((ROOT / "course/teaching-sequences.json").read_text(), "course/teaching-sequences.json"))
        self.assertEqual(len(staged["presentations"]), 17)
        home = (ROOT / "course/home/home.js").read_text()
        self.assertIn("new URL(href,catalog)", home)
        self.assertNotIn("-format.html':", home)
        for source, published in zip(presentations, staged["presentations"]):
            href = urljoin("https://example.test/gigawatt/teaching-sequences.json", published["chapters"][0]["href"])
            original = "course/" + urlsplit(source["chapters"][0]["href"]).path
            self.assertEqual(urlsplit(href).path, "/gigawatt/" + str(public_path(original)), source["id"])
            self.assertRegex(urlsplit(href).path, r"^/gigawatt/slides/[a-z0-9-]+\.html$")

    def test_png_transparency_is_detected(self):
        with TemporaryDirectory() as tmp:
            self.assertTrue(has_alpha(png(Path(tmp) / "alpha.png", alpha=True)))
            self.assertFalse(has_alpha(png(Path(tmp) / "opaque.png")))


class ImageConversionTests(unittest.TestCase):
    def require_encoder(self):
        """Skip without a WebP encoder, unless GIGAWATT_REQUIRE_WEBP=1 (as in CI) makes that a failure."""
        if webp_encoder():
            return
        if os.environ.get("GIGAWATT_REQUIRE_WEBP") == "1":
            self.fail("GIGAWATT_REQUIRE_WEBP=1, but neither cwebp nor Pillow with WebP support is installed")
        self.skipTest("needs cwebp or Pillow with WebP support")

    def site(self, root):
        catalog(root, "distribution")
        (root / "README.md").write_text("Course")
        assets = root / "course/assets"
        png(assets / "references/figure.png")
        png(assets / "generated/scene-a.png")
        png(assets / "generated/scene-b.png", width=8, height=8)
        png(assets / "icon.png", width=4, height=4, alpha=True)
        (assets / "references/figure.provenance.json").write_text('{"file": "figure.png"}')
        (root / "course/prototypes").mkdir()
        (root / "course/prototypes/distribution-format.html").write_text(
            '<img src="../assets/references/figure.png"><img src="../assets/icon.png">'
        )
        (root / "course/prototypes/distribution-visuals.js").write_text(
            'const art=file=>`<img src="../assets/generated/${file}.png">`;const figure={file:"references/figure.png"};'
            'const remote="https://cdn.example.com/img/figure.png";'
        )
        (root / "course/prototypes/deck.css").write_text(".hero{background:url(../assets/references/figure.png)}")
        (root / "course/README.md").write_text(
            "[Figure](assets/references/figure.png) and `course/assets/references/figure.png`, `figure.png`, "
            "[Remote](https://example.com/references/figure.png)"
        )
        (root / "course/domain-map.html").write_text('<script>const r={"asset":"course/assets/references/figure.png"}</script>')

    def test_large_images_publish_as_webp_and_references_follow(self):
        self.require_encoder()
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.site(root)
            original = (root / "course/assets/references/figure.png").read_bytes()
            conversions = []
            destination = stage(root, convert_over=10_000, conversions=conversions)
            self.assertEqual(
                sorted(c.source for c in conversions),
                ["assets/generated/scene-a.png", "assets/generated/scene-b.png", "assets/references/figure.png"],
            )
            for conversion in conversions:
                self.assertGreaterEqual(conversion.psnr, MIN_PSNR, conversion.source)
                self.assertEqual((destination / conversion.target).stat().st_size, conversion.after)
            figure = next(c for c in conversions if c.source == "assets/references/figure.png")
            self.assertLess(figure.after, figure.before)

            figure = destination / "assets/references/figure.webp"
            self.assertEqual(figure.read_bytes()[:4] + figure.read_bytes()[8:12], b"RIFFWEBP")
            self.assertFalse((destination / "assets/references/figure.png").exists())
            self.assertEqual((root / "course/assets/references/figure.png").read_bytes(), original)
            # Small images stay as they are, except in a folder whose names are built at run time.
            self.assertTrue((destination / "assets/icon.png").exists())
            self.assertTrue((destination / "assets/generated/scene-a.webp").exists())
            self.assertTrue((destination / "assets/generated/scene-b.webp").exists())
            self.assertEqual(list((destination / "assets/generated").glob("*.png")), [])

            self.assertIn('src="../assets/references/figure.webp"', (destination / "slides/distribution.html").read_text())
            self.assertIn('src="../assets/icon.png"', (destination / "slides/distribution.html").read_text())
            visuals = (destination / "slides/distribution-visuals.js").read_text()
            self.assertIn('src="../assets/generated/${file}.webp"', visuals)
            self.assertIn('file:"references/figure.webp"', visuals)
            self.assertIn('remote="https://cdn.example.com/img/figure.png"', visuals)
            self.assertIn("url(../assets/references/figure.webp)", (destination / "slides/deck.css").read_text())
            index = (destination / "SOURCE_INDEX.md").read_text()
            self.assertIn("[Figure](assets/references/figure.webp)", index)
            self.assertIn("`course/assets/references/figure.png`, `figure.png`", index)
            self.assertIn("[Remote](https://example.com/references/figure.png)", index)
            self.assertIn('"course/assets/references/figure.png"', (destination / "domain-map.html").read_text())
            self.assertEqual((destination / "assets/references/figure.provenance.json").read_text(), '{"file": "figure.png"}')

    def test_renaming_leaves_remote_urls_and_repository_paths_alone(self):
        """Renaming needs no encoder, so this runs on every machine."""
        with TemporaryDirectory() as tmp:
            site = Path(tmp)
            (site / "slides").mkdir()
            script = site / "slides/deck.js"
            script.write_text(
                'a="../assets/campus-cutaway.png";b="https://cdn.example.com/img/campus-cutaway.png";'
                'c="//cdn.example.com/campus-cutaway.png";d="course/assets/campus-cutaway.png";'
                "e=`https://example.com\n../assets/campus-cutaway.png`;"
            )
            notes = site / "notes.md"
            notes.write_text(
                "[Local](assets/campus-cutaway.png) [Remote](https://example.com/assets/campus-cutaway.png) "
                "`assets/campus-cutaway.png`"
            )
            image_references(site, {"assets/campus-cutaway.png": "assets/campus-cutaway.webp"}, set())
            self.assertEqual(
                script.read_text(),
                'a="../assets/campus-cutaway.webp";b="https://cdn.example.com/img/campus-cutaway.png";'
                'c="//cdn.example.com/campus-cutaway.png";d="course/assets/campus-cutaway.png";'
                "e=`https://example.com\n../assets/campus-cutaway.webp`;",
            )
            self.assertEqual(
                notes.read_text(),
                "[Local](assets/campus-cutaway.webp) [Remote](https://example.com/assets/campus-cutaway.png) "
                "`assets/campus-cutaway.png`",
            )

    def test_staging_fails_loudly_without_an_encoder(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.site(root)
            with mock.patch("gigawatt.stage_site.shutil.which", return_value=None), \
                    mock.patch.dict(sys.modules, {"PIL": None}):
                self.assertIsNone(webp_encoder())
                with self.assertRaisesRegex(RuntimeError, "neither cwebp nor Pillow"):
                    stage(root, convert_over=10_000)


if __name__ == "__main__":
    unittest.main()
