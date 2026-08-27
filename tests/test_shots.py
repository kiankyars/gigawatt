from __future__ import annotations

import copy
import json
import math
import unittest

from gigawatt import shots


def planned_segments(course: dict) -> list[dict]:
    return [
        segment
        for act in course["acts"]
        for segment in act["segments"]
        if segment["camera"]["status"] == "planned"
    ]


def segment_by_id(course: dict, segment_id: str) -> dict:
    return next(
        segment
        for act in course["acts"]
        for segment in act["segments"]
        if segment["id"] == segment_id
    )


def walk_keys(value: object):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield key
            yield from walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_keys(nested)


class PlannedShotCompilerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        (
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
        ) = shots.load_inputs()
        cls.registry = shots.compile_registry(
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
            source_digest="test-digest",
        )

    def compile(
        self,
        *,
        course: dict | None = None,
        cameras: dict | None = None,
        master: dict | None = None,
        layout: dict | None = None,
        scene: dict | None = None,
    ) -> dict:
        return shots.compile_registry(
            course or self.course,
            cameras or self.cameras,
            master or self.master,
            layout or self.layout,
            scene or self.scene,
            source_digest="test-digest",
        )

    def test_registry_covers_exact_course_requests_in_order(self) -> None:
        planned = planned_segments(self.course)
        registry = self.registry
        self.assertEqual(
            {"schema_version", "source_digest", "planned_shot_count", "shots"},
            set(registry),
        )
        self.assertEqual(1, registry["schema_version"])
        self.assertEqual(21, registry["planned_shot_count"])
        self.assertEqual(21, len(registry["shots"]))
        self.assertEqual(
            [segment["camera"]["shot"] for segment in planned],
            [shot["id"] for shot in registry["shots"]],
        )
        self.assertEqual(
            [segment["id"] for segment in planned],
            [shot["segment_id"] for shot in registry["shots"]],
        )

        expected_fields = {
            "sequence",
            "id",
            "segment_id",
            "title",
            "status",
            "mode",
            "render_mode",
            "camera_anchor",
            "evidence_readiness",
            "focus_nodes",
            "focus_edges",
            "reveal_ids",
            "reveal_copy_ids",
            "frame",
        }
        for sequence, (segment, shot) in enumerate(
            zip(planned, registry["shots"], strict=True), start=1
        ):
            self.assertEqual(expected_fields, set(shot))
            self.assertEqual(sequence, shot["sequence"])
            self.assertEqual("planned", shot["status"])
            self.assertEqual(segment["node_ids"], shot["focus_nodes"])
            self.assertEqual(segment["edge_ids"], shot["focus_edges"])
            self.assertEqual(segment["camera"]["reveal_ids"], shot["reveal_ids"])
            self.assertEqual(
                segment["camera"]["reveal_copy_ids"], shot["reveal_copy_ids"]
            )

    def test_frames_are_finite_clamped_and_keep_anchor_context(self) -> None:
        camera_map = {camera["id"]: camera for camera in self.cameras["cameras"]}
        frame_width = float(self.layout["frame"]["w"])
        frame_height = float(self.layout["frame"]["h"])
        for shot in self.registry["shots"]:
            frame = shot["frame"]
            anchor = camera_map[shot["camera_anchor"]]
            if shot["render_mode"] == "2d":
                self.assertEqual("2d", frame["kind"])
                self.assertEqual(
                    [float(value) for value in anchor["viewBox"]],
                    frame["anchor_viewBox"],
                )
                x, y, width, height = frame["viewBox"]
                self.assertTrue(all(math.isfinite(value) for value in frame["viewBox"]))
                self.assertGreater(width, 0)
                self.assertGreater(height, 0)
                self.assertGreaterEqual(x, 0)
                self.assertGreaterEqual(y, 0)
                self.assertLessEqual(x + width, frame_width + 1e-9)
                self.assertLessEqual(y + height, frame_height + 1e-9)
                self.assertAlmostEqual(
                    frame_width / frame_height, width / height, places=5
                )
            else:
                self.assertEqual("3d", frame["kind"])
                self.assertEqual(
                    [float(value) for value in anchor["position"]],
                    frame["anchor_position"],
                )
                self.assertEqual(
                    [float(value) for value in anchor["target"]], frame["anchor_target"]
                )
                self.assertEqual([0, 1, 0], frame["up"])
                self.assertTrue(
                    all(
                        math.isfinite(value)
                        for value in [*frame["position"], *frame["target"]]
                    )
                )
                self.assertGreater(math.dist(frame["position"], frame["target"]), 0)

    def test_hidden_reveal_bundles_are_exact(self) -> None:
        node_map = {node["id"]: node for node in self.master["nodes"]}
        edge_map = {edge["id"]: edge for edge in self.master["edges"]}
        for shot in self.registry["shots"]:
            hidden_records = [
                node_map[node_id]
                for node_id in shot["focus_nodes"]
                if node_map[node_id].get("base_visible", True) is False
            ] + [
                edge_map[edge_id]
                for edge_id in shot["focus_edges"]
                if edge_map[edge_id].get("base_visible", True) is False
            ]
            expected_ids = {record["id"] for record in hidden_records}
            expected_copy = {
                copy_id
                for record in hidden_records
                for copy_id in record.get("reveal_copy_ids") or []
            }
            self.assertEqual(expected_ids, set(shot["reveal_ids"]))
            self.assertEqual(expected_copy, set(shot["reveal_copy_ids"]))

    def test_registry_has_no_pacing_or_scripting_fields(self) -> None:
        forbidden = {
            "autoplay",
            "beat",
            "beats",
            "cadence",
            "duration",
            "runtime",
            "script",
            "timing",
        }
        self.assertFalse(
            forbidden & {str(key).casefold() for key in walk_keys(self.registry)}
        )

    def test_generated_registry_and_manual_review_are_current(self) -> None:
        registry_json, html, digest = shots.build_artifacts()
        second_registry, second_html, second_digest = shots.build_artifacts()
        self.assertEqual(registry_json, second_registry)
        self.assertEqual(html, second_html)
        self.assertEqual(digest, second_digest)
        self.assertEqual(registry_json, shots.REGISTRY_PATH.read_text())
        self.assertEqual(html, shots.REVIEW_PATH.read_text())
        self.assertEqual(digest, json.loads(registry_json)["source_digest"])
        self.assertIn('id="previous"', html)
        self.assertIn('id="next"', html)
        self.assertIn('id="context-toggle"', html)
        self.assertIn('event.key === "ArrowLeft"', html)
        self.assertIn('event.key === "ArrowRight"', html)
        self.assertNotIn("setTimeout(", html)
        self.assertNotIn("setInterval(", html)
        self.assertNotIn("requestAnimationFrame(", html)

    def test_duplicate_or_missing_planned_requests_fail(self) -> None:
        duplicate = copy.deepcopy(self.course)
        planned = planned_segments(duplicate)
        planned[1]["camera"]["shot"] = planned[0]["camera"]["shot"]
        with self.assertRaisesRegex(shots.ShotError, "planned shot IDs must be unique"):
            self.compile(course=duplicate)

        missing = copy.deepcopy(self.course)
        segment_by_id(missing, "p0_gigawatt_not_workload")["camera"]["status"] = (
            "existing"
        )
        with self.assertRaisesRegex(shots.ShotError, "expected 21 planned"):
            self.compile(course=missing)

    def test_hidden_reveal_and_endpoint_drift_fail(self) -> None:
        reveal_drift = copy.deepcopy(self.course)
        segment_by_id(reveal_drift, "s05_ppa_not_wire")["camera"]["reveal_ids"] = []
        with self.assertRaisesRegex(shots.ShotError, "reveal_ids must exactly match"):
            self.compile(course=reveal_drift)

        copy_reveal_drift = copy.deepcopy(self.course)
        segment_by_id(copy_reveal_drift, "s05_ppa_not_wire")["camera"][
            "reveal_copy_ids"
        ] = []
        with self.assertRaisesRegex(
            shots.ShotError, "reveal_copy_ids must exactly match"
        ):
            self.compile(course=copy_reveal_drift)

        endpoint_drift = copy.deepcopy(self.course)
        segment_by_id(endpoint_drift, "s03_initial_grid_path")["node_ids"].remove(
            "initial_tie_138"
        )
        with self.assertRaisesRegex(shots.ShotError, "unfocused_endpoints"):
            self.compile(course=endpoint_drift)

    def test_mode_and_geometry_drift_fail(self) -> None:
        mode_drift = copy.deepcopy(self.course)
        segment_by_id(mode_drift, "s02_generator_terminal")["camera"]["mode"] = "2d"
        with self.assertRaisesRegex(shots.ShotError, "2D request requires"):
            self.compile(course=mode_drift)

        geometry_drift = copy.deepcopy(self.scene)
        del geometry_drift["nodes"]["die"]
        with self.assertRaisesRegex(shots.ShotError, "node geometry must cover"):
            self.compile(scene=geometry_drift)


if __name__ == "__main__":
    unittest.main()
