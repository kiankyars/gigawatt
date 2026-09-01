from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest import mock

from gigawatt import course_v2_runtime, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
COURSE = ROOT / "course" / "course_v2.yaml"
GENERATOR = ROOT / "diagram" / "generate_course_v2.py"
RUNTIME = ROOT / "diagram" / "course_v2_runtime.json"
PLAYER = ROOT / "diagram" / "course_v2.html"
PACKET = ROOT / "course" / "INSTRUCTOR_PACKET_V2.md"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class CourseV2RuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = load_module("gigawatt_course_v2_generator", GENERATOR)
        cls.spine = teaching_visuals.load_yaml(COURSE)
        cls.cameras = teaching_visuals.load_yaml(ROOT / course_v2_runtime.CAMERAS_PATH)
        cls.manifests: dict[str, dict] = {}
        cls.payloads: dict[str, dict] = {}
        for phase in cls.spine["phases"]:
            phase_id = phase["id"]
            cls.manifests[phase_id] = teaching_visuals.load_yaml(
                ROOT / phase["manifest"]
            )
            rendered = (ROOT / phase["artifact"]).read_text()
            cls.payloads[phase_id] = course_v2_runtime.extract_pilot_payload(
                rendered,
                location=phase["artifact"],
            )

    def compile(
        self,
        *,
        spine: dict | None = None,
        manifests: dict[str, dict] | None = None,
        payloads: dict[str, dict] | None = None,
        cameras: dict | None = None,
    ) -> dict:
        return course_v2_runtime.compile_course_v2(
            deepcopy(self.spine if spine is None else spine),
            deepcopy(self.manifests if manifests is None else manifests),
            deepcopy(self.payloads if payloads is None else payloads),
            deepcopy(self.cameras if cameras is None else cameras),
            source_digest="0" * 64,
        )

    def test_real_registry_is_six_phase_manual_and_evidence_bound(self) -> None:
        registry = self.compile()
        self.assertEqual(
            {"mode": "manual", "advance": "instructor_controlled"},
            registry["course"]["interaction"],
        )
        self.assertEqual(
            course_v2_runtime.PHASE_IDS,
            [phase["id"] for phase in registry["phases"]],
        )
        self.assertEqual(
            [1, 2, 3, 4, 5, 6],
            [phase["number"] for phase in registry["phases"]],
        )
        self.assertEqual(
            "One system journey, six engineering problems", registry["journey"]["title"]
        )
        self.assertIn("does not trace one electron", registry["journey"]["body"])
        self.assertEqual(
            "generator terminals and bulk-grid sources",
            registry["phases"][1]["carrier_in"],
        )
        self.assertEqual(
            "grid service and a separately evidenced onsite source",
            registry["phases"][2]["carrier_in"],
        )
        self.assertNotIn("one carrier", json.dumps(registry).lower())
        self.assertNotIn("same physical path", json.dumps(registry).lower())
        self.assertEqual(
            [5, 6, 5, 6, 6, 5], [len(p["states"]) for p in registry["phases"]]
        )
        self.assertEqual(
            207, sum(len(p["evidence"]["facts"]) for p in registry["phases"])
        )
        self.assertEqual("diagram/hybrid.html", registry["spatial"]["artifact"])
        self.assertEqual(900, registry["spatial"]["minimum_width_px"])
        self.assertEqual(
            {
                "phase_4_building": ("electrical_room", 2),
                "phase_5_compute": ("data_hall_rack", 3),
                "phase_6_heat": ("thermal_return", 5),
            },
            {
                phase_id: (anchor["camera_id"], anchor["camera_index"])
                for phase_id, anchor in registry["spatial"]["anchors"].items()
            },
        )
        self.assertNotIn("campus_establishing", registry["spatial"]["anchors"])
        for phase in registry["phases"]:
            with self.subTest(phase=phase["id"]):
                self.assertRegex(phase["renderer_digest"], r"^[0-9a-f]{64}$")
                self.assertTrue(phase["evidence"]["facts"])
                source_refs = {source["ref"] for source in phase["evidence"]["sources"]}
                for fact in phase["evidence"]["facts"]:
                    self.assertLessEqual(set(fact["source_refs"]), source_refs)
        self.assertEqual([], teaching_visuals._forbidden_fields(registry))

    def test_compiler_rejects_spine_manifest_and_renderer_drift(self) -> None:
        timed = deepcopy(self.spine)
        timed["journey"]["duration_seconds"] = 20
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "unexpected fields|pacing",
        ):
            self.compile(spine=timed)

        wrong_question = deepcopy(self.spine)
        wrong_question["phases"][2]["question"] = "A different question"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "manifest does not match",
        ):
            self.compile(spine=wrong_question)

        wrong_payload = deepcopy(self.payloads)
        wrong_payload["phase_4_building"]["pilot"]["phase"]["number"] = 5
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "embedded phase contract",
        ):
            self.compile(payloads=wrong_payload)

        unbound = deepcopy(self.payloads)
        unbound["phase_1_generation"]["evidence"]["facts"][0]["source_refs"] = [
            "generation_transmission:missing_source"
        ]
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "unknown source refs",
        ):
            self.compile(payloads=unbound)

        incomplete_synthesis = deepcopy(self.spine)
        incomplete_synthesis["synthesis"]["lenses"][0]["phase_readings"].pop(
            "phase_6_heat"
        )
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must map exactly the six phase IDs",
        ):
            self.compile(spine=incomplete_synthesis)

    def test_compiler_rejects_spatial_anchor_and_camera_drift(self) -> None:
        wrong_artifact = deepcopy(self.spine)
        wrong_artifact["spatial"]["artifact"] = "diagram/course.html"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must be 'diagram/hybrid.html'",
        ):
            self.compile(spine=wrong_artifact)

        for width in (899, 901):
            with self.subTest(width=width):
                changed = deepcopy(self.spine)
                changed["spatial"]["minimum_width_px"] = width
                with self.assertRaisesRegex(
                    course_v2_runtime.CourseV2RuntimeError,
                    "must be integer 900",
                ):
                    self.compile(spine=changed)

        wrong_anchor = deepcopy(self.spine)
        wrong_anchor["spatial"]["anchors"]["phase_4_building"]["camera_id"] = (
            "campus_establishing"
        )
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must be 'electrical_room'",
        ):
            self.compile(spine=wrong_anchor)

        missing_anchor = deepcopy(self.spine)
        missing_anchor["spatial"]["anchors"].pop("phase_6_heat")
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must map exactly Building, Compute, and Heat",
        ):
            self.compile(spine=missing_anchor)

        reordered = deepcopy(self.cameras)
        reordered["cameras"][2], reordered["cameras"][3] = (
            reordered["cameras"][3],
            reordered["cameras"][2],
        )
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "canonical six-camera order",
        ):
            self.compile(cameras=reordered)

        not_spatial = deepcopy(self.cameras)
        not_spatial["cameras"][2]["mode"] = "2d"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must remain a 3D camera",
        ):
            self.compile(cameras=not_spatial)

        weakened = deepcopy(self.spine)
        weakened["spatial"]["boundary"] = "A spatial view."
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must preserve the conceptual",
        ):
            self.compile(spine=weakened)

    def test_artifact_extractor_rejects_digest_mismatch_and_external_shells(
        self,
    ) -> None:
        artifact = (ROOT / self.spine["phases"][0]["artifact"]).read_text()
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "source-digest meta",
        ):
            course_v2_runtime.extract_pilot_payload(
                artifact.replace(
                    '<meta name="gigawatt-source-digest" content="',
                    '<meta name="gigawatt-source-digest" content="f',
                    1,
                ),
                location="changed artifact",
            )
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "self-contained HTML",
        ):
            course_v2_runtime.extract_pilot_payload(
                "<html><script src='phase.js'></script></html>",
                location="external artifact",
            )

    def test_generator_is_deterministic_and_materialized_outputs_match(self) -> None:
        first = self.native.build()
        second = self.native.build()
        self.assertEqual(first, second)
        runtime, player, packet, digest, phase_count = first
        self.assertEqual(6, phase_count)
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        self.assertEqual(runtime, RUNTIME.read_text())
        self.assertEqual(player, PLAYER.read_text())
        self.assertEqual(packet, PACKET.read_text())
        parsed = json.loads(runtime)
        self.assertEqual(digest, parsed["source_digest"])
        embedded = re.search(
            r'<script id="course-data" type="application/json">(.*?)</script>',
            player,
            re.DOTALL,
        )
        self.assertIsNotNone(embedded)
        self.assertEqual(parsed, json.loads(embedded.group(1)))

    def test_player_owns_manual_phase_state_and_evidence_navigation(self) -> None:
        _, player, _, _, _ = self.native.build()
        required = (
            'class="phase-compass" role="tablist"',
            'id="opening-view"',
            'id="phase-view"',
            'id="synthesis-view"',
            'class="synthesis-matrix"',
            'data-synthesis-phase="phase_1_generation"',
            'id="phase-frame"',
            'id="spatial-toggle"',
            'id="spatial-panel"',
            "3D spatial anchor",
            "Return to 2D teaching",
            'id="state-nav" class="state-nav" role="tablist"',
            'id="evidence-drawer" data-layout-mode="overlay"',
            'data-evidence-phase-index="0"',
            "frame.contentWindow.activate(currentState)",
            "header,footer{display:none!important}",
            "@media (min-width:1281px){main{place-items:center!important;overflow:hidden!important}.visual-shell{display:block!important}.responsive-visual{display:none!important}}",
            "renderer digest mismatch",
            'const spatialQuery = matchMedia("(min-width: 900px)")',
            "course.spatial.anchors[course.phases[currentPhase].id]",
            'course.spatial.artifact.replace("diagram/", "")',
            'child.querySelectorAll("#steps > .step")',
            "scene.vertical_slice[anchor.camera_index]",
            'camera.mode !== "3d"',
            'step.getAttribute("aria-current") !== "step"',
            'child.getElementById("mode").textContent !== "3d"',
            'style.textContent = "#masthead,#transport{display:none!important}"',
            "event.stopImmediatePropagation()",
            "showTeaching(true)",
            "frame.tabIndex = -1",
            '"Previous phase"',
            '"Next phase"',
            '"Synthesis"',
            'event.key === "ArrowRight"',
            'event.key === "Home"',
            'event.key === "End"',
            'event.key === "Escape"',
            'history.scrollRestoration = "manual"',
            "window.scrollTo(0, 0)",
            "document.scrollingElement.scrollTop = 0",
            'section.toggleAttribute("hidden"',
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, player)
        self.assertEqual(6, player.count('class="phase-button"'))
        self.assertEqual(6, player.count('class="phase-evidence"'))
        self.assertEqual(6, player.count("data-synthesis-phase="))
        self.assertEqual(18, player.count('class="mobile-lens-label"'))
        self.assertEqual(
            1,
            player.count('document.querySelectorAll("[data-open-phase]").forEach'),
        )
        self.assertGreaterEqual(player.count('frame.removeAttribute("tabindex")'), 4)
        embedded = re.search(
            r'<script id="course-data" type="application/json">(.*?)</script>',
            player,
            re.DOTALL,
        )
        self.assertIsNotNone(embedded)
        embedded_course = json.loads(embedded.group(1))
        self.assertNotIn(
            "campus_establishing",
            {
                anchor["camera_id"]
                for anchor in embedded_course["spatial"]["anchors"].values()
            },
        )
        for phase in self.spine["phases"]:
            self.assertIn(
                f'<p class="journey-question">{phase["question"]}</p>', player
            )
        self.assertIn(
            '<strong>Reject heat</strong><p class="journey-question">How does heat get from silicon back to the atmosphere?</p>',
            player,
        )
        self.assertNotIn(
            '<strong>Reject heat</strong><span class="journey-title">Reject heat</span>',
            player,
        )
        self.assertNotIn("…", player)
        forbidden = (
            '<script src="',
            "<link ",
            "@import",
            "fetch(",
            "setTimeout(",
            "setInterval(",
            "requestAnimationFrame(",
            "autoplay",
            "text-overflow",
        )
        for marker in forbidden:
            with self.subTest(forbidden=marker):
                self.assertNotIn(marker, player)

    def test_player_declares_responsive_full_label_surfaces(self) -> None:
        _, player, _, _, _ = self.native.build()
        required = (
            "width:100%; height:100%; min-width:0; min-height:0",
            "height:100dvh",
            "overflow:hidden",
            "overflow-wrap:anywhere",
            "@media (max-width:1300px)",
            "@media (max-width:899px)",
            "@media (max-height:520px) and (orientation:landscape)",
            "@media (max-width:520px) and (orientation:portrait)",
            ".journey-grid,.lens-grid { grid-template-columns:1fr; }",
            ".synthesis-matrix thead { display:none; }",
            ".synthesis-matrix,.synthesis-matrix tbody,.synthesis-matrix tr,.synthesis-matrix th,.synthesis-matrix td { display:block; width:100%; }",
            "details[open] { max-height:72dvh; }",
            "details { position:fixed; z-index:30;",
            "details[open] { right:10px; bottom:10px;",
            "--evidence-clearance:64px",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, player)

    def test_instructor_packet_matches_registry_without_prescribed_pacing(self) -> None:
        registry = self.compile()
        packet = course_v2_runtime.render_instructor_packet(registry)
        for phase in registry["phases"]:
            self.assertIn(f"## Phase {phase['number']}: {phase['title']}", packet)
            self.assertIn(
                f"**Phase boundary:** {phase['carrier_in']} → {phase['carrier_out']}",
                packet,
            )
            for state in phase["states"]:
                self.assertIn(state["nav_label"], packet)
                self.assertIn(state["instruction"], packet)
            anchor = registry["spatial"]["anchors"].get(phase["id"])
            if anchor is None:
                self.assertNotIn(
                    f"**3D spatial anchor (900 px and wider):** {phase['title']}",
                    packet,
                )
            else:
                self.assertIn(
                    f"**3D spatial anchor (900 px and wider):** {anchor['camera_title']} — {anchor['purpose']}",
                    packet,
                )
        self.assertEqual(3, packet.count("**Spatial boundary:**"))
        self.assertIn(registry["spatial"]["boundary"], packet)
        for lens in registry["synthesis"]["lenses"]:
            self.assertIn(lens["title"], packet)
            self.assertIn(lens["question"], packet)
            for phase in registry["phases"]:
                self.assertIn(lens["phase_readings"][phase["id"]], packet)
        self.assertNotRegex(packet.lower(), r"\b(minutes?|seconds?|cadence|autoplay)\b")

    def test_source_digest_closes_over_phase_and_spatial_dependencies(self) -> None:
        phase_paths = {
            path.relative_to(ROOT).as_posix() for path in self.native._phase_paths()
        }
        expected_phases = {
            value
            for phase in self.spine["phases"]
            for value in (phase["manifest"], phase["artifact"])
        }
        self.assertEqual(expected_phases, phase_paths)
        spatial_paths = {
            path.relative_to(ROOT).as_posix() for path in self.native._spatial_paths()
        }
        expected_spatial = {
            "diagram/hybrid.html",
            "diagram/cameras.yaml",
            "diagram/master.svg",
            "diagram/map_watt_heat_handoff.svg",
            "diagram/vendor/three/three.module.js",
            "diagram/vendor/three/OrbitControls.js",
            "diagram/vendor/three/CSS2DRenderer.js",
            "diagram/vendor/three/LICENSE",
        }
        self.assertEqual(expected_spatial, spatial_paths)
        for path in (*self.native._phase_paths(), *self.native._spatial_paths()):
            self.assertTrue(path.is_file(), path)
        self.assertEqual(self.native._source_digest(), self.native.build()[3])

        baseline = self.native._source_digest()
        original_read_bytes = Path.read_bytes
        for target in self.native._spatial_paths():
            with self.subTest(target=target.relative_to(ROOT)):

                def changed(path: Path, *, _target: Path = target) -> bytes:
                    payload = original_read_bytes(path)
                    return (
                        payload + b"tamper"
                        if path.resolve() == _target.resolve()
                        else payload
                    )

                with mock.patch.object(Path, "read_bytes", changed):
                    self.assertNotEqual(baseline, self.native._source_digest())


if __name__ == "__main__":
    unittest.main()
