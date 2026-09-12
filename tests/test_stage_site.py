from __future__ import annotations

import json
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt.stage_site import INTRODUCTION_REDIRECTS, ROOT, stage


class SiteStagingTests(unittest.TestCase):
    def test_every_retired_introduction_lesson_has_a_current_destination(self):
        introduction = json.loads((ROOT / "course/lessons.json").read_text())
        course = json.loads((ROOT / "course/expanded-course.json").read_text())
        self.assertEqual(
            set(INTRODUCTION_REDIRECTS),
            {lesson["id"] for lesson in introduction["lessons"]},
        )
        self.assertLessEqual(
            set(INTRODUCTION_REDIRECTS.values()),
            {lesson["id"] for lesson in course["lessons"]},
        )

    def test_retired_introduction_is_replaced_in_public_artifact_only(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "README.md").write_text("Course")
            (root / "course").mkdir()
            (root / "course/index.html").write_text("Current reader")
            original = root / "diagram/index.html"
            original.parent.mkdir()
            original.write_text("Retired introduction content")
            destination = root / "_site"
            old_public = destination / "diagram/index.html"
            old_public.parent.mkdir(parents=True)
            old_public.write_text(original.read_text())

            stage(root, destination)

            self.assertEqual(original.read_text(), "Retired introduction content")
            self.assertEqual(
                (destination / "course/index.html").read_text(), "Current reader"
            )
            redirect = old_public.read_text()
            self.assertNotIn("Retired introduction content", redirect)
            self.assertIn('href="../course/index.html"', redirect)
            self.assertIn('"ride-through": "d05-storage-power-and-time"', redirect)
            for alias in (
                "index.html",
                "course.html",
                "v1.html",
                "phase1_generation.html",
            ):
                with self.subTest(alias=alias):
                    page = (destination / alias).read_text()
                    self.assertIn('href="course/index.html"', page)
                    self.assertNotIn("diagram/index.html", page)
                    self.assertIn("location.search+hash", page)


if __name__ == "__main__":
    unittest.main()
