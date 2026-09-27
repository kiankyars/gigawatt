"""The prose lint's --gate mode blocks the Pages deploy, so its pass and fail paths are tested here."""

from __future__ import annotations

import contextlib
import importlib.util
import io
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("prose_lint", ROOT / "qa/reader/prose_lint.py")
prose_lint = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(prose_lint)


def lesson(lesson_id, *paragraphs):
    return {"id": lesson_id, "sections": [{"paragraphs": list(paragraphs)}]}


CLEAN = lesson("clean", "Transformers step the voltage down. Cables carry the current to the racks.")
# Every paragraph ends on a negation, far over the voice budgets, with no slide reference or residue.
NEGATIVE = lesson("negative", "The breaker does not trip.", "The feeder is not overloaded.")
SLIDE_REF = lesson("slide-ref", "The slide shows the transformer. Cables carry the current.")
RESIDUE = lesson("residue", "This review rechecked the transformer rating. Cables carry the current.")


def run(lessons, *arguments):
    """Run main() on these lessons and return its exit code and printed output."""
    output = io.StringIO()
    with mock.patch.object(prose_lint, "lessons", return_value=iter(lessons)), \
            mock.patch("sys.argv", ["prose_lint.py", *arguments]), \
            contextlib.redirect_stdout(output), contextlib.redirect_stderr(io.StringIO()):
        return prose_lint.main(), output.getvalue()


class ProseLintGateTests(unittest.TestCase):
    def test_list_measures_are_compared_by_count(self):
        clean, slide = prose_lint.measure(CLEAN), prose_lint.measure(SLIDE_REF)
        self.assertEqual(len(slide["slide_refs"]), 1)
        self.assertFalse(prose_lint.over_budget(clean)["slide_refs"])
        self.assertTrue(prose_lint.over_budget(slide)["slide_refs"])
        self.assertFalse(prose_lint.over_budget(slide)["residue"])

    def test_gate_fails_on_a_slide_reference_or_review_residue(self):
        code, output = run([CLEAN, SLIDE_REF], "--gate", "slide_refs")
        self.assertEqual(code, 1)
        self.assertIn("slide-ref: over the slide_refs budget", output)
        self.assertIn("The slide shows the transformer.", output)
        self.assertEqual(run([CLEAN, RESIDUE], "--gate", "slide_refs,residue")[0], 1)

    def test_gate_passes_a_clean_corpus_and_ignores_ungated_budgets(self):
        code, output = run([CLEAN], "--gate", "establish_10k")
        self.assertEqual(code, 0)
        self.assertIn("0/1 lessons over the gated budgets", output)
        # The negation ratios are far over budget, but only the named budgets gate.
        self.assertEqual(run([CLEAN, NEGATIVE], "--gate", "slide_refs,residue")[0], 0)
        self.assertEqual(run([CLEAN, NEGATIVE], "--gate", "para_end_neg")[0], 1)

    def test_unknown_or_empty_gate_is_a_usage_error(self):
        for value in ("bogus", "slide_refs,bogus", ","):
            with self.subTest(value=value), self.assertRaises(SystemExit) as stop:
                run([CLEAN], "--gate", value)
            self.assertEqual(stop.exception.code, 2)

    def test_report_mode_never_fails_and_check_mode_does(self):
        self.assertEqual(run([CLEAN, NEGATIVE])[0], 0)
        self.assertEqual(run([CLEAN, NEGATIVE], "--check")[0], 1)
        self.assertEqual(run([CLEAN], "--check")[0], 0)


if __name__ == "__main__":
    unittest.main()
