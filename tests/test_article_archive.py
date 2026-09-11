from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt import article_archive as a
from gigawatt import research as r
from gigawatt.stage_site import stage

URL = "https://newsletter.semianalysis.com/p/test-power"
PERMISSION = "Publisher permission reported by the course author for local research."
BODY = """<h2>One electrical boundary</h2><p>Our original example has eight units of load,
six units of local generation and two units of grid import. The missing supply
must be replaced when grid support disappears; location alone proves no island capability.</p>
<ul><li>Grid connected</li><li>Supported island</li></ul>
<table><tr><th>Source</th><th>MW</th></tr><tr><td>Grid</td><td>2</td></tr></table>
<p>Read <a href="/reference">the reference</a>.</p><img src="/figure.png" alt>
<pre>power = local + grid\nprint(power)</pre>
<div class="subscribe-widget">UNWANTED SUBSCRIPTION CTA</div>"""


def html(*, paid=False, paywall=False):
    metadata = {
        "@type": "NewsArticle",
        "headline": "An original test article",
        "isAccessibleForFree": not paid,
        "author": [{"name": "Example Author"}],
        "datePublished": "2026-09-10",
    }
    return (
        '<html><nav>UNWANTED NAVIGATION</nav><script type="application/ld+json">'
        + json.dumps(metadata)
        + '</script><div class="body markup">'
        + BODY
        + "</div>"
        + ('<div data-testid="paywall">Subscribe for the rest</div>' if paywall else "")
        + "<footer>UNWANTED FOOTER</footer></html>"
    )


class ArticleArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root / "course").mkdir()
        (self.root / "course/domain-map.json").write_text(
            json.dumps({"domains": [{"id": "D03"}]})
        )
        self.source = {
            "id": "SA01",
            "url": URL,
            "title": "An original test article",
            "publisher": "SemiAnalysis",
            "kind": "analysis",
            "review_status": "candidate_not_reviewed",
            "domains": ["D03"],
            "use": "Evaluate supply boundaries.",
            "caution": "Not reviewed.",
        }
        (self.root / "course/research-sources.json").write_text(
            json.dumps({"sources": [self.source]})
        )

    def test_extract_preserves_structure_citations_and_code_without_page_chrome(self):
        result = a.extract_article(html(), URL)
        self.assertEqual(result["access_status"], "public_article")
        self.assertEqual(result["authors"], ["Example Author"])
        text = result["markdown"]
        self.assertIn("## One electrical boundary", text)
        self.assertIn("- Supported island", text)
        self.assertIn("| Source | MW |\n| --- | --- |\n| Grid | 2 |", text)
        self.assertIn(
            "[the reference](<https://newsletter.semianalysis.com/reference>)", text
        )
        self.assertIn(
            "![Figure](<https://newsletter.semianalysis.com/figure.png>)", text
        )
        self.assertIn("power = local + grid\nprint(power)", text)
        self.assertNotIn("UNWANTED", text)

    def test_paid_metadata_or_paywall_stays_partial_and_shells_fail(self):
        for kwargs in [
            {"paid": True},
            {"paywall": True},
            {"paid": True, "paywall": True},
        ]:
            self.assertEqual(
                a.extract_article(html(**kwargs), URL)["access_status"],
                "public_preview",
            )
        with self.assertRaisesRegex(r.ResearchError, "No supported article body"):
            a.extract_article("<html><p>Sign in to continue</p></html>", URL)
        with self.assertRaisesRegex(r.ResearchError, "too short"):
            a.extract_article('<div class="body markup">Subscribe</div>', URL)

    def test_sync_caches_and_never_promotes_catalog_review(self):
        calls = []

        def fetch(url, timeout):
            calls.append(url)
            return html(paid=True, paywall=True)

        self.assertEqual(
            a.sync(self.root, permission_note=PERMISSION, delay=0, fetch=fetch),
            [("SA01", "public_preview")],
        )
        snapshot = (self.root / a.ARCHIVE / "SA01.md").read_bytes()
        self.assertEqual(
            a.sync(self.root, permission_note=None, delay=0, fetch=fetch),
            [("SA01", "cached")],
        )
        self.assertEqual(calls, [URL])
        self.assertEqual(a.check(self.root), 1)
        self.assertEqual((self.root / a.ARCHIVE / "SA01.md").read_bytes(), snapshot)
        self.assertEqual(
            r.read_json(self.root / "course/research-sources.json")["sources"][0][
                "review_status"
            ],
            "candidate_not_reviewed",
        )

    def test_failed_refresh_and_preview_do_not_replace_imported_full_text(self):
        exported = self.root / "export.md"
        exported.write_text(
            "# Full provided article\n\nOriginal complete test export with its full argument."
        )
        a.import_article(
            self.root, "SA01", exported, complete=True, permission_note=PERMISSION
        )
        target = self.root / a.ARCHIVE / "SA01.md"
        original = target.read_bytes()
        self.assertEqual(
            a.sync(
                self.root,
                refresh=True,
                permission_note=None,
                delay=0,
                fetch=lambda *args: html(paid=True),
            ),
            [("SA01", "preserved_full_capture")],
        )

        def failure(*args):
            raise OSError("Synthetic network outage")

        self.assertEqual(
            a.sync(
                self.root, refresh=True, permission_note=None, delay=0, fetch=failure
            ),
            [("SA01", "fetch_failed")],
        )
        self.assertEqual(target.read_bytes(), original)
        record = a.load_manifest(self.root)["records"]["SA01"]
        self.assertEqual(record["access_status"], "imported_full_article")
        self.assertIn("network outage", record["last_attempt_error"])
        self.assertEqual(a.check(self.root), 1)

    def test_local_edits_are_preserved_and_detected(self):
        a.sync(
            self.root, permission_note=PERMISSION, delay=0, fetch=lambda *args: html()
        )
        target = self.root / a.ARCHIVE / "SA01.md"
        edited = target.read_text() + "\nA user addition.\n"
        target.write_text(edited)
        result = a.sync(
            self.root,
            refresh=True,
            permission_note=None,
            delay=0,
            fetch=lambda *args: html(),
        )
        self.assertEqual(result, [("SA01", "fetch_failed")])
        self.assertEqual(target.read_text(), edited)
        with self.assertRaisesRegex(r.ResearchError, "modified archive"):
            a.check(self.root)

    def test_imported_preview_cannot_be_labeled_complete(self):
        export = self.root / "export.html"
        export.write_text(html(paid=True, paywall=True))
        with self.assertRaisesRegex(r.ResearchError, "cannot be labeled complete"):
            a.import_article(
                self.root, "SA01", export, complete=True, permission_note=PERMISSION
            )
        self.assertFalse((self.root / a.ARCHIVE / "SA01.md").exists())

    def test_provided_full_paid_html_is_accepted_when_no_paywall_is_present(self):
        export = self.root / "full-export.html"
        export.write_text(html(paid=True, paywall=False))
        status = a.import_article(
            self.root, "SA01", export, complete=True, permission_note=PERMISSION
        )
        self.assertEqual(status, "imported_full_article")

    def test_math_source_is_preserved_without_duplicate_visual_markup(self):
        formula = '<span class="katex"><math><annotation encoding="application/x-tex">I^2 R</annotation></math><span class="katex-html">DUPLICATE FORMULA</span></span>'
        result = a.extract_article(html().replace("</h2>", "</h2>" + formula), URL)
        self.assertIn("$I^2 R$", result["markdown"])
        self.assertNotIn("DUPLICATE FORMULA", result["markdown"])

    def test_site_staging_keeps_local_article_text_out_of_the_public_artifact(self):
        (self.root / "README.md").write_text("Public course")
        (self.root / "diagram").mkdir()
        (self.root / "diagram/index.html").write_text("Introduction")
        (self.root / "course/lessons.json").write_text('{"lessons": []}')
        private = self.root / a.ARCHIVE
        private.mkdir(parents=True)
        (private / "SA01.md").write_text("PRIVATE SOURCE TEXT")
        (self.root / "research/README.md").write_text("Public research workflow")
        prototype = self.root / "course/prototypes"
        prototype.mkdir()
        teaching_files = {
            "ups-format.html": '<script type="module" src="./ups-bypass.js"></script>',
            "ups-bypass.js": 'export { renderRedundancy } from "./ups-redundancy.js";',
            "ups-redundancy.js": "export function renderRedundancy() {}",
        }
        for name, content in teaching_files.items():
            (prototype / name).write_text(content)
        destination = stage(self.root)
        self.assertTrue((destination / "research/README.md").exists())
        self.assertFalse((destination / a.ARCHIVE).exists())
        for name, content in teaching_files.items():
            self.assertEqual(
                (destination / "course/prototypes" / name).read_text(), content
            )

    def test_email_tracking_does_not_create_a_second_article_identity(self):
        tracked = (
            URL
            + "?utm_source=email&publication_id=1&post_id=2&isFreemail=true&r=user&triedRedirect=true"
        )
        self.assertEqual(r.canonical_url(tracked), URL)
        self.assertNotEqual(r.canonical_url(URL + "?section=two"), URL)

    def test_archive_checks_use_recorded_bytes_and_confine_paths(self):
        a.sync(
            self.root, permission_note=PERMISSION, delay=0, fetch=lambda *args: html()
        )
        manifest = a.load_manifest(self.root)
        data = (self.root / a.ARCHIVE / "SA01.md").read_bytes()
        self.assertEqual(
            manifest["records"]["SA01"]["file_sha256"], hashlib.sha256(data).hexdigest()
        )
        manifest["records"]["../../outside"] = {}
        a.save_manifest(self.root, manifest)
        with self.assertRaisesRegex(r.ResearchError, "Unsafe source ID"):
            a.check(self.root)


if __name__ == "__main__":
    unittest.main()
