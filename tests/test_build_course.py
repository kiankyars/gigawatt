from __future__ import annotations

import json
import shutil
import subprocess
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt import build_course


def example_course() -> dict:
    return {
        "title": "GIGAWATT",
        "subtitle": "From watts to racks",
        "chapters": [{"id": "power", "title": "Power", "kicker": "01"}],
        "lessons": [
            {
                "id": "rack",
                "chapter": "power",
                "title": "Supply the rack",
                "eyebrow": "One system",
                "body": "A load needs power.",
                "visual": "rack",
                "takeaway": "Capacity has a boundary.",
                "notes": ["This is a teaching scenario."],
                "sources": [{"title": "Source", "url": "https://example.org/source"}],
                "check": {
                    "question": "Which boundary?",
                    "options": ["Site", "IT"],
                    "answer": 1,
                    "explanation": "The stated boundary is IT.",
                },
            }
        ],
    }


class CourseBuildTests(unittest.TestCase):
    def test_valid_content_and_optional_check(self):
        source = example_course()
        self.assertIs(build_course.validate_course(source, {"rack"}), source)
        del source["lessons"][0]["check"]
        build_course.validate_course(source, {"rack"})

    def test_broken_relationships_are_rejected(self):
        mutations = {
            "duplicate chapter": lambda c: c["chapters"].append(
                deepcopy(c["chapters"][0])
            ),
            "duplicate lesson": lambda c: c["lessons"].append(
                deepcopy(c["lessons"][0])
            ),
            "unknown chapter": lambda c: c["lessons"][0].update(chapter="missing"),
            "unknown visual": lambda c: c["lessons"][0].update(visual="missing"),
            "empty chapter": lambda c: c["chapters"].append(
                {"id": "empty", "title": "Empty", "kicker": "02"}
            ),
            "invalid source": lambda c: c["lessons"][0]["sources"][0].update(
                url="javascript:alert(1)"
            ),
            "missing source": lambda c: c["lessons"][0].update(sources=[]),
            "invalid answer": lambda c: c["lessons"][0]["check"].update(answer=2),
            "boolean answer": lambda c: c["lessons"][0]["check"].update(answer=True),
            "empty option": lambda c: c["lessons"][0]["check"].update(
                options=["A", ""]
            ),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                source = example_course()
                mutate(source)
                with self.assertRaises(build_course.CourseError):
                    build_course.validate_course(source, {"rack"})

    def test_visual_registry_has_one_owner(self):
        self.assertEqual(
            build_course.declared_visual_ids('export const VISUAL_IDS = ["rack"];'),
            {"rack"},
        )
        for code in (
            "",
            'const VISUAL_IDS = ["rack", "rack"];',
            "const VISUAL_IDS = [1];",
        ):
            with self.subTest(code=code), self.assertRaises(build_course.CourseError):
                build_course.declared_visual_ids(code)

    def test_bundle_strips_supported_module_edges(self):
        scripts = {
            "math.js": "export function current(p, v) { return p / v; }",
            "diagrams.js": 'import {\n current\n} from "./math.js";\nexport const VISUAL_IDS = ["rack"];',
            "course.js": 'import { VISUAL_IDS } from "./diagrams.js";\nconsole.log(VISUAL_IDS);',
        }
        result = build_course.bundle_scripts(scripts)
        self.assertNotIn("import ", result)
        self.assertNotIn("export ", result)
        self.assertLess(
            result.index("function current"), result.index("const VISUAL_IDS")
        )
        scripts["course.js"] = 'import x from "https://example.org/external.js";'
        with self.assertRaisesRegex(build_course.CourseError, "unsupported"):
            build_course.bundle_scripts(scripts)

    def test_build_is_deterministic_and_keeps_embedded_text_inert(self):
        with TemporaryDirectory() as directory:
            root = Path(directory)
            web = root / "course" / "web"
            web.mkdir(parents=True)
            source = example_course()
            source["lessons"][0]["body"] = (
                "</script><script>alert(1)</script> __COURSE_CSS__"
            )
            (root / "course" / "lessons.json").write_text(json.dumps(source))
            (web / "index.html").write_text(
                '<style>__COURSE_CSS__</style><script type="application/json" id="course-data">__COURSE_DATA__</script><script type="module">__COURSE_SCRIPT__</script>'
            )
            (web / "course.css").write_text("body { color: black; }")
            (web / "math.js").write_text("export const zero = 0;")
            (web / "diagrams.js").write_text('export const VISUAL_IDS = ["rack"];')
            (web / "course.js").write_text("document.title = 'GIGAWATT';")
            result = build_course.build(root)
            self.assertEqual(result, build_course.build(root))
            self.assertIn(r"\u003c/script>", result)
            self.assertIn("__COURSE_CSS__", result)
            self.assertNotIn("<script>alert(1)", result)
            (root / "course" / "lessons.json").write_text('{"title":"A","title":"B"}')
            with self.assertRaisesRegex(build_course.CourseError, "Duplicate JSON key"):
                build_course.build(root)

    def test_committed_page_matches_current_sources(self):
        self.assertEqual(
            (build_course.ROOT / "diagram" / "index.html").read_bytes(),
            build_course.build().encode("utf-8"),
        )

    @unittest.skipUnless(
        shutil.which("node"), "Node is needed for JavaScript syntax validation"
    )
    def test_bundled_javascript_has_valid_module_syntax(self):
        web = build_course.ROOT / "course" / "web"
        scripts = {name: (web / name).read_text() for name in build_course.ASSETS}
        result = subprocess.run(
            ["node", "--input-type=module", "--check"],
            input=build_course.bundle_scripts(scripts),
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
