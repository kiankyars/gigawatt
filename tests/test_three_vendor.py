from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from gigawatt import shots

ROOT = Path(__file__).resolve().parents[1]
VENDOR = ROOT / "diagram" / "vendor" / "three"
EXPECTED_SHA256 = {
    "three.module.js": (
        "ce1fa418de16a19495a9f72495580e3015d7745c296d3ce0485897f902ddedfb"
    ),
    "OrbitControls.js": (
        "80efaadea4f8a636a65fb0bd08bfef62f3d93a0bb94e2e7500f23176c5c07f4e"
    ),
    "CSS2DRenderer.js": (
        "7de0bb70e3c1d6da58416353ed7140a7a7743ece99d73b56eb62bc2dd79bfed5"
    ),
    "LICENSE": "4c40a1ef62450b857c3b2aaf294936304cd552d965fbcd9d32d4c5bcf4ba4454",
}
LOCAL_IMPORT_MAP = (
    '{"imports":{"three":"./vendor/three/three.module.js",'
    '"three/addons/controls/OrbitControls.js":"./vendor/three/OrbitControls.js",'
    '"three/addons/renderers/CSS2DRenderer.js":'
    '"./vendor/three/CSS2DRenderer.js"}}'
)


class ThreeVendorTests(unittest.TestCase):
    def test_vendor_matches_three_0_170_0_package_files(self) -> None:
        self.assertEqual(set(EXPECTED_SHA256), {path.name for path in VENDOR.iterdir()})
        for filename, expected in EXPECTED_SHA256.items():
            with self.subTest(filename=filename):
                actual = hashlib.sha256((VENDOR / filename).read_bytes()).hexdigest()
                self.assertEqual(expected, actual)
        self.assertIn(
            "const REVISION = '170';", (VENDOR / "three.module.js").read_text()
        )

    def test_all_template_owners_use_only_local_three_imports(self) -> None:
        owners = (
            ROOT / "src" / "gigawatt" / "shots.py",
            ROOT / "src" / "gigawatt" / "scene.py",
            ROOT / "diagram" / "generate_s10_two_rack_heat_paths.py",
        )
        for owner in owners:
            with self.subTest(owner=owner.relative_to(ROOT)):
                source = owner.read_text()
                self.assertIn(LOCAL_IMPORT_MAP, source)
                self.assertNotIn("https://unpkg.com/three", source)

        for artifact in (ROOT / "diagram").glob("*.html"):
            with self.subTest(artifact=artifact.relative_to(ROOT)):
                self.assertNotIn("https://unpkg.com/three", artifact.read_text())

    def test_shot_payload_is_script_safe_and_round_trips(self) -> None:
        payload = {"copy": "</script><script>alert('unexpected')</script>"}
        encoded = shots._script_safe_payload(payload)
        self.assertNotIn("</script>", encoded.casefold())
        self.assertIn("<\\/script>", encoded)
        self.assertEqual(payload, json.loads(encoded))

    def test_shot_template_surfaces_startup_failures(self) -> None:
        template = shots.REVIEW_HTML
        self.assertIn("window.__gigawattStartupError = error =>", template)
        self.assertIn('window.addEventListener("error", onError, true);', template)
        self.assertIn(
            'window.addEventListener("unhandledrejection", onRejection);', template
        )
        self.assertIn('overlay.dataset.state = "error";', template)
        self.assertIn('overlay.setAttribute("role", "alert");', template)
        self.assertIn("window.__gigawattReady();", template)
        self.assertLess(
            template.index("window.__gigawattStartupError"),
            template.index('<script type="importmap">'),
        )


if __name__ == "__main__":
    unittest.main()
