from __future__ import annotations

import json
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt import research as r

NOW = "2026-09-06T12:00:00+00:00"
ARTICLE = "https://newsletter.semianalysis.com/p/800vdc-rack-power"
SITEMAP = b"""<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
<url><loc>https://semianalysis.com/p/800vdc-rack-power/</loc><lastmod>2026-08-01</lastmod></url>
<url><loc>https://newsletter.semianalysis.com/p/800vdc-rack-power?utm_source=rss</loc></url>
</urlset>"""
FEED = b"""<rss version="2.0"><channel><item>
<title>800 VDC rack power and grid connection</title>
<link>https://newsletter.semianalysis.com/p/800vdc-rack-power</link>
<pubDate>Tue, 01 Sep 2026 00:00:00 GMT</pubDate>
<description>DO NOT ARCHIVE THIS ARTICLE BODY</description>
</item></channel></rss>"""


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "course").mkdir()
        self.map = {
            "domains": [
                {"id": "D03", "title": "Grid", "source_ids": ["P01"]},
                {"id": "D06", "title": "Rack power", "source_ids": ["P01"]},
            ]
        }
        self.catalog = {
            "sources": [
                {
                    "id": "P01",
                    "title": "A primary manual",
                    "url": "https://example.org/manual",
                    "publisher": "Example",
                    "kind": "primary",
                    "review_status": "candidate_not_reviewed",
                    "domains": ["D03", "D06"],
                    "use": "Verify the interface.",
                    "caution": "Not yet read.",
                }
            ]
        }
        self.write("course/domain-map.json", self.map)
        self.write("course/research-sources.json", self.catalog)

    def write(self, name, value):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value), encoding="utf-8")
        return path

    def test_build_is_idempotent_and_preserves_exact_human_body(self):
        self.assertEqual(len(r.build_notes(self.root)), 2)
        self.assertEqual(r.build_notes(self.root), [])
        note = self.root / "research/sources/P01.md"
        human = "\n\n## My evidence\nα = 17.\n\nKeep exact whitespace.  \n"
        note.write_text(note.read_text().split(r.END)[0] + r.END + human)
        self.catalog["sources"][0]["title"] = "Revised primary manual"
        self.write("course/research-sources.json", self.catalog)
        with self.assertRaisesRegex(r.ResearchError, "stale"):
            r.build_notes(self.root, check=True)
        r.build_notes(self.root)
        self.assertEqual(note.read_text().split(r.END)[1], human)
        self.assertIn("Revised primary manual", note.read_text())
        self.assertEqual(r.build_notes(self.root), [])
        self.assertEqual(r.build_notes(self.root, check=True), [])

    def test_unmanaged_note_refuses_write_before_any_output_changes(self):
        path = self.root / "research/sources/P01.md"
        path.parent.mkdir(parents=True)
        path.write_text("My unstructured source notes")
        with self.assertRaisesRegex(r.ResearchError, "Refusing"):
            r.build_notes(self.root)
        self.assertEqual(path.read_text(), "My unstructured source notes")
        self.assertFalse((self.root / "research/INDEX.md").exists())

    def test_catalog_rejects_unknown_ids_and_normalized_duplicates(self):
        bad = deepcopy(self.catalog)
        bad["sources"][0]["domains"] = ["D99"]
        with self.assertRaisesRegex(r.ResearchError, "unknown domain"):
            r.validate_catalog(bad, self.map)
        bad = deepcopy(self.catalog)
        bad["sources"][0]["url"] = ARTICLE
        duplicate = dict(
            bad["sources"][0], id="P02", url=ARTICLE.replace("newsletter.", "")
        )
        bad["sources"].append(duplicate)
        with self.assertRaisesRegex(r.ResearchError, "Duplicate source URL"):
            r.validate_catalog(bad, self.map)
        bad = deepcopy(self.map)
        bad["domains"][0]["source_ids"] = ["MISSING"]
        with self.assertRaisesRegex(r.ResearchError, "unknown mapped source"):
            r.validate_catalog(self.catalog, bad)

    def test_alias_deduping_preserves_decisions_across_repeat_discovery(self):
        run = r.discover(
            self.root,
            [r.DEFAULT_URL],
            [],
            delay=0,
            fetcher=lambda *args: SITEMAP,
            now=NOW,
        )
        self.assertEqual(run["status"], "completed")
        path = self.root / "research/discovery.json"
        inventory = r.read_json(path)
        self.assertEqual(len(inventory["items"]), 1)
        item = inventory["items"][0]
        self.assertEqual(item["url"], ARTICLE)
        self.assertEqual(item["suggested_domains"], ["D06"])
        self.assertNotIn("published_on", item)
        item.update(triage="defer", domains=["D03"], notes="Keep this expert question.")
        self.write("research/discovery.json", inventory)
        r.discover(
            self.root, [r.DEFAULT_URL], [], delay=0, fetcher=lambda *args: FEED, now=NOW
        )
        updated = r.read_json(path)["items"][0]
        self.assertEqual(
            (updated["triage"], updated["domains"], updated["notes"]),
            ("defer", ["D03"], "Keep this expert question."),
        )
        self.assertEqual(updated["title_origin"], "feed_title")
        self.assertNotIn("DO NOT ARCHIVE", path.read_text())
        self.assertEqual(updated["first_seen"], NOW)
        self.assertEqual(len(r.read_json(path)["items"]), 1)

    def test_all_network_failure_records_failure_without_erasing_inventory(self):
        r.discover(
            self.root,
            [r.DEFAULT_URL],
            [],
            delay=0,
            fetcher=lambda *args: SITEMAP,
            now=NOW,
        )
        prior = r.read_json(self.root / "research/discovery.json")["items"]

        def failed(*args):
            raise TimeoutError("timed out")

        run = r.discover(
            self.root, [r.DEFAULT_URL], [], delay=0, fetcher=failed, now=NOW
        )
        self.assertEqual(run["status"], "failed")
        self.assertEqual(len(run["documents_failed"]), 1)
        self.assertEqual(
            r.read_json(self.root / "research/discovery.json")["items"], prior
        )

    def test_partial_discovery_retains_good_results_and_reports_bounds(self):
        index = b"""<sitemapindex>
        <sitemap><loc>https://example.org/one.xml</loc></sitemap>
        <sitemap><loc>https://example.org/two.xml</loc></sitemap>
        </sitemapindex>"""
        fixtures = {
            "https://example.org/index.xml": index,
            "https://example.org/one.xml": SITEMAP,
        }

        def fetch(url, timeout):
            if url.endswith("two.xml"):
                raise OSError("Unavailable")
            return fixtures[url]

        run = r.discover(
            self.root,
            ["https://example.org/index.xml"],
            [],
            max_documents=2,
            delay=0,
            fetcher=fetch,
            now=NOW,
        )
        self.assertEqual(run["status"], "partial")
        self.assertEqual(run["unvisited_due_to_bound"], ["https://example.org/two.xml"])
        self.assertEqual(
            len(r.read_json(self.root / "research/discovery.json")["items"]), 1
        )
        run = r.discover(
            self.root,
            ["https://example.org/index.xml"],
            [],
            max_documents=3,
            delay=0,
            fetcher=fetch,
            now=NOW,
        )
        self.assertEqual(run["status"], "partial")
        self.assertEqual(len(run["documents_failed"]), 1)

    def test_cross_host_sitemap_child_is_not_fetched(self):
        calls = []

        def fetch(url, timeout):
            calls.append(url)
            return b"<sitemapindex><sitemap><loc>http://127.0.0.1/private.xml</loc></sitemap></sitemapindex>"

        run = r.discover(
            self.root,
            ["https://example.org/index.xml"],
            [],
            delay=0,
            fetcher=fetch,
            now=NOW,
        )
        self.assertEqual(calls, ["https://example.org/index.xml"])
        self.assertEqual(run["status"], "partial")

    def test_candidate_notes_are_unreviewed_and_curated_aliases_not_duplicated(self):
        r.discover(
            self.root,
            [r.DEFAULT_URL],
            [],
            delay=0,
            fetcher=lambda *args: SITEMAP,
            now=NOW,
        )
        r.build_notes(self.root, include_candidates=True)
        candidate = self.root / "research/sources" / f"{r.candidate_id(ARTICLE)}.md"
        self.assertIn("candidate_not_reviewed", candidate.read_text())
        self.assertIn("Metadata only", candidate.read_text())
        self.assertEqual(r.build_notes(self.root, include_candidates=True), [])
        r.build_notes(self.root, include_candidates=True, check=True)
        self.catalog["sources"][0]["url"] = ARTICLE.replace("newsletter.", "")
        self.write("course/research-sources.json", self.catalog)
        r.build_notes(self.root, include_candidates=True)
        index = (self.root / "research/INDEX.md").read_text()
        self.assertNotIn("DISC_", index)
        self.assertTrue(candidate.exists(), "Never silently delete a user's old notes")

    def test_import_is_publisher_neutral_rejects_bad_domains_and_ignores_body(self):
        imported = self.write(
            "manual.json",
            [
                {
                    "url": "https://other.example/power",
                    "title": "Grid power",
                    "publisher": "Other publisher",
                    "triage": "include",
                    "domains": ["D03"],
                    "body": "FULL ARTICLE MUST NOT BE COPIED",
                }
            ],
        )
        run = r.discover(
            self.root,
            [],
            [imported],
            delay=0,
            now=NOW,
            fetcher=lambda *args: self.fail("Imports should not call the network"),
        )
        self.assertEqual(run["status"], "completed")
        path = self.root / "research/discovery.json"
        self.assertNotIn("FULL ARTICLE", path.read_text())
        item = r.read_json(path)["items"][0]
        self.assertEqual(item["publisher"], "Other publisher")
        self.assertEqual(item["triage"], "include")
        imported.write_text(
            json.dumps(
                [
                    {
                        "url": "https://other.example/invalid",
                        "title": "Invalid",
                        "domains": ["D99"],
                    }
                ]
            )
        )
        previous = path.read_bytes()
        with self.assertRaisesRegex(r.ResearchError, "unknown domain"):
            r.discover(self.root, [], [imported], delay=0, now=NOW)
        self.assertEqual(path.read_bytes(), previous)

    def test_malformed_metadata_fails_without_review_or_records(self):
        for data in [
            b"<not-valid",
            b"<html><body>Article page</body></html>",
            b'<!DOCTYPE x [<!ENTITY y "oops">]><urlset/>',
        ]:
            with self.subTest(data=data):
                run = r.discover(
                    self.root,
                    [r.DEFAULT_URL],
                    [],
                    delay=0,
                    fetcher=lambda *args, data=data: data,
                    now=NOW,
                )
                self.assertEqual(run["status"], "failed")
                self.assertEqual(run["metadata_records_observed"], 0)
        self.assertEqual(
            r.read_json(self.root / "research/discovery.json")["items"], []
        )

    def test_atom_metadata_and_canonicalization_keep_meaningful_query(self):
        data = b"""<feed xmlns="http://www.w3.org/2005/Atom"><entry>
        <title>Grid systems</title><link rel="alternate" href="https://example.org/?r=reference"/>
        <published>2026-09-01T00:00:00Z</published><content>Not saved</content>
        </entry></feed>"""
        records, children = r.parse_metadata(data, "https://example.org/feed")
        self.assertEqual(records[0]["url"], "https://example.org/?r=reference")
        self.assertEqual(children, [])
        self.assertEqual(r.canonical_url(records[0]["url"]), records[0]["url"])
        self.assertEqual(r.canonical_url(r.DEFAULT_URL), r.DEFAULT_URL)
        for url in (
            "https://newsletter.semianalysis.com/archive",
            "https://newsletter.semianalysis.com/feed",
        ):
            self.assertEqual(r.canonical_url(url), url)

    def test_explicit_empty_mapping_does_not_reinstate_keyword_suggestions(self):
        r.discover(
            self.root,
            [r.DEFAULT_URL],
            [],
            delay=0,
            fetcher=lambda *args: SITEMAP,
            now=NOW,
        )
        inventory = r.read_json(self.root / "research/discovery.json")
        item = inventory["items"][0]
        item.update(triage="defer", domains=[], notes="Outside the chosen scope.")
        self.assertEqual(r.candidate_sources(inventory, {"D03", "D06"}, set()), [])

    def test_check_catches_hand_edited_invalid_inventory_mapping(self):
        r.discover(
            self.root,
            [r.DEFAULT_URL],
            [],
            delay=0,
            fetcher=lambda *args: SITEMAP,
            now=NOW,
        )
        r.build_notes(self.root)
        inventory = r.read_json(self.root / "research/discovery.json")
        inventory["items"][0]["domains"] = ["D99"]
        self.write("research/discovery.json", inventory)
        with self.assertRaisesRegex(r.ResearchError, "unknown domain"):
            r.build_notes(self.root, check=True)


if __name__ == "__main__":
    unittest.main()
