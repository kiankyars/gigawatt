from __future__ import annotations

import hashlib
import unittest
from unittest import mock

from gigawatt import course_runtime, generated_artifacts, quality, scene


class GeneratedArtifactClosureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = generated_artifacts.ROOT
        cls.master = scene.load_yaml(root / "diagram/master.yaml")
        cls.layout = scene.load_yaml(root / "diagram/layout.yaml")
        cls.evidence = scene.load_yaml(root / "evidence/abilene.yaml")
        cls.cameras = scene.load_yaml(root / "diagram/cameras.yaml")
        cls.artifacts = generated_artifacts.build_expected_artifacts(
            cls.master,
            cls.layout,
            cls.evidence,
            cls.cameras,
        )
        cls.acceptance_artifacts = (
            generated_artifacts.build_acceptance_materialized_artifacts()
        )
        course, cameras, master, layout, scene_data, ledgers, visuals = (
            course_runtime.load_inputs()
        )
        runtime = course_runtime.compile_registry(
            course,
            cameras,
            master,
            layout,
            scene_data,
            ledgers,
            visuals,
            source_digest=course_runtime._source_digest(course),
        )
        cls.runtime = runtime
        cls.candidate_course_artifacts = {
            candidate_id: generated_artifacts.build_candidate_course_artifacts(
                quality._modeled_runtime(runtime, visual_sources)
            )
            for candidate_id, visual_sources in quality.EXPECTED_VARIANTS.items()
        }

    def test_exact_inventory_and_current_bytes(self) -> None:
        self.assertEqual(
            set(self.artifacts),
            set(generated_artifacts.GENERATED_ARTIFACT_COMMANDS),
        )
        self.assertEqual(len(self.artifacts), 17)
        self.assertIn("diagram/phase1_generation.html", self.artifacts)
        self.assertIn("diagram/phase2_transmission.html", self.artifacts)
        self.assertIn("diagram/phase3_campus.html", self.artifacts)
        self.assertIn("diagram/phase4_building.html", self.artifacts)
        self.assertIn("diagram/phase5_compute.html", self.artifacts)
        self.assertIn("diagram/phase6_heat.html", self.artifacts)
        self.assertIn("diagram/course_v2_runtime.json", self.artifacts)
        self.assertIn("diagram/course_v2.html", self.artifacts)
        self.assertIn("course/INSTRUCTOR_PACKET_V2.md", self.artifacts)
        generated_artifacts.assert_current(self.artifacts)

    def test_every_artifact_tamper_fails_closed(self) -> None:
        for relative_path in self.artifacts:
            with self.subTest(relative_path=relative_path):

                def tampered_reader(path, *, target=relative_path):
                    text = path.read_text()
                    if path == generated_artifacts.ROOT / target:
                        return text + "\n<!-- tampered -->\n"
                    return text

                with self.assertRaisesRegex(
                    generated_artifacts.GeneratedArtifactError,
                    f"^{relative_path} is stale",
                ):
                    generated_artifacts.assert_current(
                        self.artifacts,
                        read_text=tampered_reader,
                    )

    def test_acceptance_artifact_inventory_and_current_bytes_are_exact(self) -> None:
        self.assertEqual(
            set(self.acceptance_artifacts),
            set(generated_artifacts.ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS),
        )
        self.assertEqual(len(self.acceptance_artifacts), 14)
        self.assertIn("diagram/s10_two_rack_heat_paths.html", self.acceptance_artifacts)
        self.assertNotIn("diagram/phase1_generation.html", self.acceptance_artifacts)
        self.assertNotIn("diagram/phase2_transmission.html", self.acceptance_artifacts)
        self.assertNotIn("diagram/phase3_campus.html", self.acceptance_artifacts)
        self.assertNotIn("diagram/phase4_building.html", self.acceptance_artifacts)
        self.assertNotIn("diagram/phase5_compute.html", self.acceptance_artifacts)
        self.assertNotIn("diagram/phase6_heat.html", self.acceptance_artifacts)
        self.assertNotIn("diagram/course_v2_runtime.json", self.acceptance_artifacts)
        self.assertNotIn("diagram/course_v2.html", self.acceptance_artifacts)
        self.assertNotIn("course/INSTRUCTOR_PACKET_V2.md", self.acceptance_artifacts)
        generated_artifacts.assert_acceptance_current(self.acceptance_artifacts)

    def test_every_acceptance_artifact_tamper_fails_closed(self) -> None:
        for relative_path in self.acceptance_artifacts:
            with self.subTest(relative_path=relative_path):

                def tampered_reader(path, *, target=relative_path):
                    payload = path.read_bytes()
                    return (
                        payload + b"\n<!-- tampered -->\n"
                        if path == generated_artifacts.ROOT / target
                        else payload
                    )

                with self.assertRaisesRegex(
                    generated_artifacts.GeneratedArtifactError,
                    f"^{relative_path} is stale",
                ):
                    generated_artifacts.assert_acceptance_current(
                        self.acceptance_artifacts,
                        read_bytes=tampered_reader,
                    )

    def test_acceptance_artifact_inventory_drift_fails_closed(self) -> None:
        missing = dict(self.acceptance_artifacts)
        missing.pop(next(iter(missing)))
        with self.assertRaisesRegex(
            generated_artifacts.GeneratedArtifactError,
            "parity input is incomplete",
        ):
            generated_artifacts.assert_acceptance_current(missing)

        extra = {**self.acceptance_artifacts, "diagram/undeclared.html": ""}
        with self.assertRaisesRegex(
            generated_artifacts.GeneratedArtifactError,
            "parity input is incomplete",
        ):
            generated_artifacts.assert_acceptance_current(extra)

    def test_candidate_course_artifacts_are_exact_and_deterministic(self) -> None:
        retained_sha256 = {
            artifact_id: hashlib.sha256(
                self.acceptance_artifacts[artifact_id].encode()
            ).hexdigest()
            for artifact_id in generated_artifacts.CANDIDATE_COURSE_ARTIFACT_IDS
        }
        for candidate_id, artifacts in self.candidate_course_artifacts.items():
            with self.subTest(candidate_id=candidate_id):
                self.assertEqual(
                    tuple(sorted(artifacts)),
                    generated_artifacts.CANDIDATE_COURSE_ARTIFACT_IDS,
                )
                self.assertEqual(
                    artifacts,
                    generated_artifacts.build_candidate_course_artifacts(
                        quality._modeled_runtime(
                            self.runtime,
                            quality.EXPECTED_VARIANTS[candidate_id],
                        )
                    ),
                )
                candidate_sha256 = {
                    artifact_id: hashlib.sha256(payload.encode()).hexdigest()
                    for artifact_id, payload in artifacts.items()
                }
                if candidate_id == "combined":
                    self.assertEqual(candidate_sha256, retained_sha256)
                else:
                    self.assertNotEqual(candidate_sha256, retained_sha256)

    def test_pages_workflow_publishes_v2_with_frozen_v1_comparison(self) -> None:
        workflow = scene.load_yaml(
            generated_artifacts.ROOT / ".github/workflows/pages.yml"
        )
        self.assertEqual(
            workflow["permissions"],
            {
                "contents": "read",
                "pages": "write",
                "id-token": "write",
            },
        )
        deploy = workflow["jobs"]["deploy"]
        self.assertEqual(
            deploy["environment"],
            {
                "name": "github-pages",
                "url": "${{ steps.deployment.outputs.page_url }}",
            },
        )
        stage = next(
            step for step in deploy["steps"] if step["name"] == "Stage the course site"
        )
        self.assertEqual(
            stage["run"].splitlines(),
            [
                "mkdir -p _site/vendor",
                "cp diagram/course_v2.html _site/index.html",
                "cp diagram/phase1_generation.html _site/",
                "cp diagram/phase2_transmission.html _site/",
                "cp diagram/phase3_campus.html _site/",
                "cp diagram/phase4_building.html _site/",
                "cp diagram/phase5_compute.html _site/",
                "cp diagram/phase6_heat.html _site/",
                "cp diagram/hybrid.html _site/",
                "cp diagram/master.svg _site/",
                "cp diagram/map_watt_heat_handoff.svg _site/",
                "cp diagram/course.html _site/v1.html",
                "cp -R diagram/vendor/three _site/vendor/three",
                "touch _site/.nojekyll",
            ],
        )
        actions = {
            step["name"]: step["uses"]
            for step in deploy["steps"]
            if "uses" in step
        }
        self.assertEqual(
            actions,
            {
                "Check out repository": "actions/checkout@v6",
                "Configure GitHub Pages": "actions/configure-pages@v5",
                "Upload GitHub Pages artifact": "actions/upload-pages-artifact@v4",
                "Deploy GitHub Pages": "actions/deploy-pages@v4",
            },
        )
        upload = next(
            step
            for step in deploy["steps"]
            if step["name"] == "Upload GitHub Pages artifact"
        )
        self.assertEqual(upload["with"], {"path": "_site"})

    def test_pages_workflow_closes_over_v2_phase_dependencies(self) -> None:
        workflow = scene.load_yaml(
            generated_artifacts.ROOT / ".github/workflows/pages.yml"
        )
        deploy = workflow["jobs"]["deploy"]
        stage = next(
            step for step in deploy["steps"] if step["name"] == "Stage the course site"
        )
        staged_phase_commands = {
            line
            for line in stage["run"].splitlines()
            if line.startswith("cp diagram/phase")
        }
        course_v2 = scene.load_yaml(generated_artifacts.ROOT / "course/course_v2.yaml")
        expected_phase_commands = {
            f"cp {phase['artifact']} _site/" for phase in course_v2["phases"]
        }
        self.assertEqual(staged_phase_commands, expected_phase_commands)
        self.assertEqual(6, len(staged_phase_commands))
        staged_spatial_commands = {
            line
            for line in stage["run"].splitlines()
            if line
            in {
                "cp diagram/hybrid.html _site/",
                "cp diagram/master.svg _site/",
                "cp diagram/map_watt_heat_handoff.svg _site/",
                "cp -R diagram/vendor/three _site/vendor/three",
            }
        }
        self.assertEqual(
            {
                "cp diagram/hybrid.html _site/",
                "cp diagram/master.svg _site/",
                "cp diagram/map_watt_heat_handoff.svg _site/",
                "cp -R diagram/vendor/three _site/vendor/three",
            },
            staged_spatial_commands,
        )
        for dependency in (
            "diagram/hybrid.html",
            "diagram/master.svg",
            "diagram/map_watt_heat_handoff.svg",
            "diagram/vendor/three/three.module.js",
            "diagram/vendor/three/OrbitControls.js",
            "diagram/vendor/three/CSS2DRenderer.js",
            "diagram/vendor/three/LICENSE",
        ):
            with self.subTest(dependency=dependency):
                self.assertTrue((generated_artifacts.ROOT / dependency).is_file())


class AcceptanceMaterializationIsolationTests(unittest.TestCase):
    def test_frozen_acceptance_build_does_not_invoke_v2_generators(self) -> None:
        with mock.patch.object(
            generated_artifacts,
            "_phase1_artifact",
            side_effect=AssertionError("v2 generator entered frozen acceptance"),
        ):
            artifacts = generated_artifacts.build_acceptance_materialized_artifacts()
        self.assertEqual(
            set(artifacts),
            set(generated_artifacts.ACCEPTANCE_MATERIALIZED_ARTIFACT_COMMANDS),
        )


if __name__ == "__main__":
    unittest.main()
