from __future__ import annotations

import unittest
from copy import deepcopy

from gigawatt import scene as scene_pipeline


class ScenePipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.master = scene_pipeline.load_yaml(scene_pipeline.DIAGRAM / "master.yaml")
        cls.scene = scene_pipeline.load_yaml(scene_pipeline.DIAGRAM / "scene.yaml")
        cls.cameras = scene_pipeline.load_yaml(scene_pipeline.DIAGRAM / "cameras.yaml")

    def test_manifests_cover_master_exactly(self) -> None:
        scene_pipeline.validate(self.master, self.scene, self.cameras)
        self.assertEqual(
            {node["id"] for node in self.master["nodes"]},
            set(self.scene["nodes"]),
        )
        self.assertEqual(
            {edge["id"] for edge in self.master["edges"]},
            set(self.scene["edges"]),
        )

    def test_scene_contains_placement_not_semantic_copy(self) -> None:
        forbidden_node_keys = {"label", "domain", "gate", "lifecycle", "source_ids"}
        forbidden_edge_keys = {
            "from",
            "to",
            "carries",
            "lifecycle",
            "source_ids",
        }
        for spec in self.scene["nodes"].values():
            self.assertFalse(forbidden_node_keys & set(spec))
        for spec in self.scene["edges"].values():
            self.assertFalse(forbidden_edge_keys & set(spec))

    def test_payload_derives_labels_and_carries_from_master(self) -> None:
        payload = scene_pipeline.build_payload(self.master, self.scene, self.cameras)
        payload_nodes = {node["id"]: node for node in payload["nodes"]}
        payload_edges = {edge["id"]: edge for edge in payload["edges"]}
        for node in self.master["nodes"]:
            self.assertEqual(node["label"], payload_nodes[node["id"]]["label"])
        for edge in self.master["edges"]:
            self.assertEqual(edge["carries"], payload_edges[edge["id"]]["carries"])

        changed = deepcopy(self.master)
        changed["nodes"][0]["label"] = "Changed only in semantic master"
        changed_payload = scene_pipeline.build_payload(changed, self.scene, self.cameras)
        self.assertEqual("Changed only in semantic master", changed_payload["nodes"][0]["label"])

    def test_shared_palette_is_the_only_scene_palette(self) -> None:
        payload = scene_pipeline.build_payload(self.master, self.scene, self.cameras)
        self.assertEqual(scene_pipeline.palette(), payload["palette"])
        token_names = set(payload["palette"])
        for node in self.scene["nodes"].values():
            for primitive in node["primitives"]:
                self.assertIn(primitive["fill"], token_names)
        for edge in payload["edges"]:
            self.assertIn(edge["token"], token_names)

    def test_canonical_ac_and_dc_tokens_remain_distinct(self) -> None:
        self.assertEqual(
            "voltage:rack_ac",
            scene_pipeline.token_for_edge("electricity@rack_ac"),
        )
        self.assertEqual(
            "voltage:rack_dc",
            scene_pipeline.token_for_edge("electricity@rack_dc"),
        )

    def test_hidden_edges_are_not_constructed_or_camera_selectable(self) -> None:
        payload = scene_pipeline.build_payload(self.master, self.scene, self.cameras)
        hidden = [edge for edge in payload["edges"] if not edge["base_visible"]]
        self.assertTrue(hidden)
        html = scene_pipeline.render_html(payload)
        self.assertIn("if (!edge.base_visible) continue;", html)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][0]["focus_edges"] = [hidden[0]["id"]]
        with self.assertRaisesRegex(scene_pipeline.ManifestError, "hidden_edges"):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_grid_and_btm_paths_are_three_distinct_branches(self) -> None:
        edges = {edge["id"]: edge for edge in self.master["edges"]}
        branch_paths = (
            ("btm_fuel_to_shaft", "btm_terminal_to_gsu", "btm_gsu_to_mv"),
            (
                "grid138_source_to_tie",
                "grid138_tie_to_station",
                "grid138_station_to_mv",
            ),
            (
                "grid345_source_to_corridor",
                "grid345_corridor_to_hv",
                "grid345_hv_to_lpt",
                "grid345_lpt_to_mv",
            ),
        )
        starts = []
        for path in branch_paths:
            path_edges = [edges[edge_id] for edge_id in path]
            starts.append(path_edges[0]["from"])
            for first, second in zip(path_edges, path_edges[1:]):
                self.assertEqual(first["to"], second["from"])
            self.assertEqual("campus_mv_distribution", path_edges[-1]["to"])
        self.assertEqual(len(starts), len(set(starts)))
        self.assertNotIn(
            ("gsu_transformer", "transmission_corridor_345"),
            {(edge["from"], edge["to"]) for edge in edges.values()},
        )

    def test_thermal_camera_shows_full_supply_return_graph(self) -> None:
        semantic_thermal = {
            edge["id"]
            for edge in self.master["edges"]
            if edge["carries"].split("@", 1)[0] in {"heat", "coolant", "water"}
        }
        thermal_camera = next(
            camera for camera in self.cameras["cameras"] if camera["id"] == "thermal_return"
        )
        self.assertEqual(semantic_thermal, set(thermal_camera["focus_edges"]))

        edges = {edge["id"]: edge for edge in self.master["edges"]}
        pulse = [edges[edge_id] for edge_id in thermal_camera["pulse_edges"]]
        self.assertEqual("die", pulse[0]["from"])
        self.assertEqual("atmosphere", pulse[-1]["to"])
        for first, second in zip(pulse, pulse[1:]):
            self.assertEqual(first["to"], second["from"])

    def test_vertical_slice_uses_all_three_view_modes(self) -> None:
        cameras = self.cameras["cameras"]
        self.assertEqual(
            self.cameras["vertical_slice"], [camera["id"] for camera in cameras]
        )
        self.assertEqual({"2d", "3d", "overlay"}, {camera["mode"] for camera in cameras})

    def test_camera_label_nodes_are_known_focus_nodes(self) -> None:
        payload = scene_pipeline.build_payload(self.master, self.scene, self.cameras)
        campus = next(
            camera
            for camera in payload["cameras"]
            if camera["id"] == "campus_establishing"
        )
        self.assertTrue(set(campus["label_nodes"]) <= set(campus["focus_nodes"]))
        self.assertIn("const labelFocus = new Set(state.label_nodes || []);", scene_pipeline.render_html(payload))

        cameras = deepcopy(self.cameras)
        cameras["cameras"][1]["label_nodes"] = ["not_a_master_node"]
        with self.assertRaisesRegex(scene_pipeline.ManifestError, "unknown_label_nodes"):
            scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][1]["label_nodes"] = ["unit_substation"]
        with self.assertRaisesRegex(scene_pipeline.ManifestError, "nonfocus_label_nodes"):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_generated_player_is_deterministic_and_current(self) -> None:
        first_html, first_digest = scene_pipeline.generate()
        second_html, second_digest = scene_pipeline.generate()
        self.assertEqual(first_digest, second_digest)
        self.assertEqual(first_html, second_html)
        self.assertEqual(
            first_html,
            (scene_pipeline.DIAGRAM / "hybrid.html").read_text(),
        )


if __name__ == "__main__":
    unittest.main()
