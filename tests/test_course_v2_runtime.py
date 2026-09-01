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
        cls.course_runtime = json.loads(
            (ROOT / course_v2_runtime.COURSE_RUNTIME_PATH).read_text()
        )
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
        course_runtime: dict | None = None,
    ) -> dict:
        return course_v2_runtime.compile_course_v2(
            deepcopy(self.spine if spine is None else spine),
            deepcopy(self.manifests if manifests is None else manifests),
            deepcopy(self.payloads if payloads is None else payloads),
            deepcopy(self.cameras if cameras is None else cameras),
            deepcopy(self.course_runtime if course_runtime is None else course_runtime),
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
            [5, 6, 5, 6, 6, 7], [len(p["states"]) for p in registry["phases"]]
        )
        self.assertEqual(
            207, sum(len(p["evidence"]["facts"]) for p in registry["phases"])
        )
        self.assertEqual(900, registry["spatial"]["minimum_width_px"])
        self.assertEqual(13, registry["spatial"]["state_view_count"])
        self.assertEqual(
            ["diagram/course.html", "diagram/hybrid.html"],
            registry["spatial"]["artifacts"],
        )
        expected_spatial_views = {
            ("phase_1_generation", "abilene_selection"): (
                "segment",
                "s01_fire_to_electricity",
            ),
            ("phase_1_generation", "transmission_handoff"): (
                "segment",
                "s02_generator_terminal",
            ),
            ("phase_2_transmission", "abilene_grid_paths"): (
                "camera",
                "campus_establishing",
            ),
            ("phase_3_campus", "abilene_unknown_merge"): (
                "camera",
                "campus_establishing",
            ),
            ("phase_4_building", "equipment_by_verb"): (
                "segment",
                "s07_building_power_train",
            ),
            ("phase_5_compute", "orient_inside_rack"): (
                "segment",
                "s08_rack_voltage_descent",
            ),
            ("phase_6_heat", "rack_cooling_split"): (
                "segment",
                "s10_two_rack_heat_paths",
            ),
            ("phase_6_heat", "technology_loop"): (
                "segment",
                "s11_technology_loop",
            ),
            ("phase_6_heat", "cdu_boundary"): ("segment", "s12_cdu_boundary"),
            ("phase_6_heat", "parallel_residual_air"): (
                "segment",
                "s13_residual_air_branch",
            ),
            ("phase_6_heat", "facility_heat_rejection"): (
                "segment",
                "s14_facility_heat_rejection",
            ),
            ("phase_6_heat", "water_accounting"): (
                "segment",
                "s15_water_accounting",
            ),
            ("phase_6_heat", "whole_journey_closure"): (
                "segment",
                "s16_close_atmosphere",
            ),
        }
        actual_spatial_views = {}
        for phase in registry["phases"]:
            with self.subTest(phase=phase["id"]):
                self.assertRegex(phase["renderer_digest"], r"^[0-9a-f]{64}$")
                self.assertTrue(phase["evidence"]["facts"])
                source_refs = {source["ref"] for source in phase["evidence"]["sources"]}
                for fact in phase["evidence"]["facts"]:
                    self.assertLessEqual(set(fact["source_refs"]), source_refs)
                for state in phase["states"]:
                    view = state.get("spatial_view")
                    if view is None:
                        continue
                    actual_spatial_views[(phase["id"], state["id"])] = (
                        view["view_kind"],
                        view["view_id"],
                    )
                    self.assertTrue(view["title"])
                    self.assertTrue(view["purpose"])
                    self.assertTrue(view["boundary"])
                    self.assertIsInstance(view["view_index"], int)
        self.assertEqual(expected_spatial_views, actual_spatial_views)
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

    def test_compiler_rejects_spatial_view_and_source_drift(self) -> None:
        for width in (899, 901):
            with self.subTest(width=width):
                changed = deepcopy(self.spine)
                changed["spatial"]["minimum_width_px"] = width
                with self.assertRaisesRegex(
                    course_v2_runtime.CourseV2RuntimeError,
                    "must be integer 900",
                ):
                    self.compile(spine=changed)

        missing_phase = deepcopy(self.spine)
        missing_phase["spatial"]["state_views"].pop("phase_6_heat")
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must map exactly the six phase IDs",
        ):
            self.compile(spine=missing_phase)

        empty_phase = deepcopy(self.spine)
        empty_phase["spatial"]["state_views"]["phase_4_building"] = {}
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must be a non-empty mapping",
        ):
            self.compile(spine=empty_phase)

        unknown_state = deepcopy(self.spine)
        unknown_state["spatial"]["state_views"]["phase_1_generation"]["not_a_state"] = (
            unknown_state["spatial"]["state_views"]["phase_1_generation"].pop(
                "abilene_selection"
            )
        )
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "unknown state IDs",
        ):
            self.compile(spine=unknown_state)

        unexpected = deepcopy(self.spine)
        unexpected["spatial"]["state_views"]["phase_1_generation"]["abilene_selection"][
            "camera_id"
        ] = "campus_establishing"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "fields must be exact",
        ):
            self.compile(spine=unexpected)

        wrong_pair = deepcopy(self.spine)
        wrong_pair["spatial"]["state_views"]["phase_1_generation"]["abilene_selection"][
            "artifact"
        ] = "diagram/hybrid.html"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "segment.*views must use 'diagram/course.html'",
        ):
            self.compile(spine=wrong_pair)

        unknown_segment = deepcopy(self.spine)
        unknown_segment["spatial"]["state_views"]["phase_1_generation"][
            "abilene_selection"
        ]["view_id"] = "missing_segment"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "not present in course_runtime.json",
        ):
            self.compile(spine=unknown_segment)

        two_dimensional_segment = deepcopy(self.spine)
        two_dimensional_segment["spatial"]["state_views"]["phase_1_generation"][
            "abilene_selection"
        ]["view_id"] = "p0_gigawatt_not_workload"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must reference a 3D segment",
        ):
            self.compile(spine=two_dimensional_segment)

        research_required_segment = deepcopy(self.course_runtime)
        next(
            segment
            for segment in research_required_segment["segments"]
            if segment["segment_id"] == "s01_fire_to_electricity"
        )["evidence_readiness"] = "research_required"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must reference an evidence-ready segment",
        ):
            self.compile(course_runtime=research_required_segment)

        title_drift = deepcopy(self.spine)
        title_drift["spatial"]["state_views"]["phase_1_generation"][
            "abilene_selection"
        ]["title"] = "A renamed view"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must match the source view title",
        ):
            self.compile(spine=title_drift)

        unknown_camera = deepcopy(self.spine)
        unknown_camera["spatial"]["state_views"]["phase_2_transmission"][
            "abilene_grid_paths"
        ]["view_id"] = "missing_camera"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "not present in cameras.yaml",
        ):
            self.compile(spine=unknown_camera)

        not_spatial = deepcopy(self.cameras)
        next(
            camera
            for camera in not_spatial["cameras"]
            if camera["id"] == "campus_establishing"
        )["mode"] = "2d"
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must reference a 3D camera",
        ):
            self.compile(cameras=not_spatial)

        reordered = deepcopy(self.cameras)
        reordered["vertical_slice"][1], reordered["vertical_slice"][2] = (
            reordered["vertical_slice"][2],
            reordered["vertical_slice"][1],
        )
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "must match the camera inventory order",
        ):
            self.compile(cameras=reordered)

        duplicate_segments = deepcopy(self.course_runtime)
        duplicate_segments["segments"][1]["segment_id"] = duplicate_segments[
            "segments"
        ][0]["segment_id"]
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "segment_id values must be unique",
        ):
            self.compile(course_runtime=duplicate_segments)

        wrong_count = deepcopy(self.course_runtime)
        wrong_count["segment_count"] += 1
        with self.assertRaisesRegex(
            course_v2_runtime.CourseV2RuntimeError,
            "segment_count must match",
        ):
            self.compile(course_runtime=wrong_count)

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
            'id="spatial-frame"',
            'id="spatial-toggle"',
            'id="spatial-panel"',
            "Open 2D explanation",
            "Return to 3D system view",
            'id="state-nav" class="state-nav" role="tablist"',
            'id="evidence-drawer" data-layout-mode="overlay"',
            'data-evidence-phase-index="0"',
            "teachingFrame.contentWindow.activate(currentState)",
            "header,footer{display:none!important}",
            "@media (min-width:1281px){main{place-items:center!important;overflow:hidden!important}.visual-shell{display:block!important}.responsive-visual{display:none!important}}",
            "renderer digest mismatch",
            'const spatialQuery = matchMedia("(min-width: 900px)")',
            "function currentSpatialView()",
            "course.phases[currentPhase].states[currentState].spatial_view",
            'view.artifact.replace("diagram/", "")',
            'child.getElementById("review-data")',
            'child.querySelectorAll("#shot-list > .shot-button")',
            'segment.render_mode !== "3d"',
            'child.getElementById("teaching-overlay")',
            'child.querySelectorAll("#steps > .step")',
            "scene.vertical_slice[view.view_index]",
            'camera.mode !== "3d"',
            'control.getAttribute("aria-current") !== "step"',
            'style.textContent = "#masthead,#transport{display:none!important}"',
            "#shot-rail,#masthead,#transport{display:none!important}",
            "#stage{inset:0!important}",
            "function bindChildNavigation(child)",
            "event.stopImmediatePropagation()",
            "showTeaching(true)",
            "spatialFrame.tabIndex = -1",
            "if (spatialFrame.dataset.artifact !== artifact)",
            "spatialFrame.contentWindow.location.pathname.endsWith",
            "teachingFrame.contentWindow.location.pathname.endsWith",
            'teachingFrame.addEventListener("load", prepareTeachingFrame)',
            'spatialFrame.addEventListener("load", prepareSpatialFrame)',
            "if (currentSpatialView() && spatialQuery.matches) showSpatial(); else showTeaching();",
            'spatialToggle.setAttribute("aria-pressed", String(spatialMode && available))',
            "if (!spatialMode) frameError.hidden = true",
            "if (!spatialMode) { frameError.hidden = false",
            '"Previous phase"',
            '"Next phase"',
            '"Synthesis"',
            'event.key === "ArrowRight"',
            'event.key === "Home"',
            'event.key === "End"',
            'event.key !== "Escape"',
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
        self.assertGreaterEqual(
            player.count('teachingFrame.removeAttribute("tabindex")'), 4
        )
        self.assertEqual(1, player.count('id="spatial-frame"'))
        self.assertEqual(1, player.count("spatialFrame.src = artifact"))
        embedded = re.search(
            r'<script id="course-data" type="application/json">(.*?)</script>',
            player,
            re.DOTALL,
        )
        self.assertIsNotNone(embedded)
        embedded_course = json.loads(embedded.group(1))
        self.assertEqual(
            13,
            sum(
                "spatial_view" in state
                for phase in embedded_course["phases"]
                for state in phase["states"]
            ),
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
            "setStateControlsDisabled",
            "if (spatialMode) return",
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
            'document.documentElement.style.setProperty("--evidence-clearance", `${clearance}px`);',
            "new ResizeObserver(updateEvidenceClearance).observe(courseFooter);",
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
                spatial_view = state.get("spatial_view")
                if spatial_view is not None:
                    self.assertIn(
                        f"**3D system view:** {spatial_view['title']} — {spatial_view['purpose']}",
                        packet,
                    )
                    self.assertIn(
                        f"**Spatial boundary:** {spatial_view['boundary']}", packet
                    )
        self.assertEqual(13, packet.count("**Spatial boundary:**"))
        self.assertIn("`Open 2D explanation`", packet)
        self.assertIn("`Return to 3D system view`", packet)
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
            "diagram/course.html",
            "diagram/course_runtime.json",
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
