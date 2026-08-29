from __future__ import annotations

import json
import math
import shutil
import struct
import subprocess
import unittest
from copy import deepcopy
from itertools import pairwise
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from gigawatt import layout as layout_pipeline
from gigawatt import scene as scene_pipeline


class ScenePipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.master = scene_pipeline.load_yaml(scene_pipeline.DIAGRAM / "master.yaml")
        cls.scene = scene_pipeline.load_yaml(scene_pipeline.DIAGRAM / "scene.yaml")
        cls.cameras = scene_pipeline.load_yaml(scene_pipeline.DIAGRAM / "cameras.yaml")

    def test_manifests_cover_master_exactly(self) -> None:
        scene_pipeline.validate_webgl_numeric_domain(self.scene)
        scene_pipeline.validate(self.master, self.scene, self.cameras)
        self.assertEqual(
            {node["id"] for node in self.master["nodes"]},
            set(self.scene["nodes"]),
        )
        self.assertEqual(
            {edge["id"] for edge in self.master["edges"]},
            set(self.scene["edges"]),
        )

    def test_loader_rejects_duplicate_mapping_keys_at_nested_depth(self) -> None:
        with TemporaryDirectory(prefix="gigawatt-scene-yaml-") as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("outer:\n  inner:\n    repeated: 1\n    repeated: 2\n")
            with self.assertRaisesRegex(
                scene_pipeline.ManifestError, "duplicate YAML key 'repeated'"
            ):
                scene_pipeline.load_yaml(path)

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
        changed_payload = scene_pipeline.build_payload(
            changed, self.scene, self.cameras
        )
        self.assertEqual(
            "Changed only in semantic master", changed_payload["nodes"][0]["label"]
        )

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

    def test_camera_focus_labels_cannot_reveal_hidden_or_unknown_copy(self) -> None:
        cases = (
            ("nuclear_variant", "hidden_focus_labels"),
            ("not_master_copy", "unknown_focus_labels"),
        )
        for copy_id, message in cases:
            cameras = deepcopy(self.cameras)
            cameras["cameras"][0]["focus_labels"] = [copy_id]
            with self.subTest(copy_id=copy_id):
                with self.assertRaisesRegex(scene_pipeline.ManifestError, message):
                    scene_pipeline.validate(self.master, self.scene, cameras)
                with self.assertRaisesRegex(scene_pipeline.ManifestError, message):
                    layout_pipeline.filtered_camera_scene(
                        "<g/>",
                        cameras["cameras"][0],
                        self.master,
                    )

    def test_camera_focus_labels_must_be_unique_strings(self) -> None:
        for focus_labels in (["region_rack", "region_rack"], ["region_rack", 7]):
            cameras = deepcopy(self.cameras)
            cameras["cameras"][0]["focus_labels"] = focus_labels
            with (
                self.subTest(focus_labels=focus_labels),
                self.assertRaisesRegex(scene_pipeline.ManifestError, "focus_labels"),
            ):
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
            for first, second in pairwise(path_edges):
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
            camera
            for camera in self.cameras["cameras"]
            if camera["id"] == "thermal_return"
        )
        self.assertEqual(semantic_thermal, set(thermal_camera["focus_edges"]))

        edges = {edge["id"]: edge for edge in self.master["edges"]}
        pulse = [edges[edge_id] for edge_id in thermal_camera["pulse_edges"]]
        self.assertEqual("die", pulse[0]["from"])
        self.assertEqual("atmosphere", pulse[-1]["to"])
        for first, second in pairwise(pulse):
            self.assertEqual(first["to"], second["from"])

    def test_vertical_slice_uses_all_three_view_modes(self) -> None:
        cameras = self.cameras["cameras"]
        self.assertEqual(
            self.cameras["vertical_slice"], [camera["id"] for camera in cameras]
        )
        self.assertEqual(
            {"2d", "3d", "overlay"}, {camera["mode"] for camera in cameras}
        )

    def test_camera_count_ids_and_order_are_exact_before_record_validation(
        self,
    ) -> None:
        self.assertEqual(
            scene_pipeline.CANONICAL_CAMERA_IDS,
            tuple(self.cameras["vertical_slice"]),
        )
        self.assertEqual(
            scene_pipeline.CANONICAL_CAMERA_IDS,
            tuple(camera["id"] for camera in self.cameras["cameras"]),
        )

        mutations = []
        empty = deepcopy(self.cameras)
        empty["vertical_slice"] = []
        empty["cameras"] = []
        mutations.append(("empty", empty))

        reordered = deepcopy(self.cameras)
        reordered["vertical_slice"][:2] = reversed(reordered["vertical_slice"][:2])
        reordered["cameras"][:2] = reversed(reordered["cameras"][:2])
        mutations.append(("reordered", reordered))

        renamed = deepcopy(self.cameras)
        renamed["vertical_slice"][0] = "renamed_camera"
        renamed["cameras"][0]["id"] = "renamed_camera"
        mutations.append(("renamed", renamed))

        appended = deepcopy(self.cameras)
        for index in range(1_000):
            camera = deepcopy(self.cameras["cameras"][0])
            camera["id"] = f"extra_camera_{index}"
            appended["cameras"].append(camera)
            appended["vertical_slice"].append(camera["id"])
        mutations.append(("1,000 appended", appended))

        for label, cameras in mutations:
            with (
                self.subTest(label=label),
                patch.object(scene_pipeline, "_id_list") as id_list_validator,
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "canonical camera"
                ),
            ):
                scene_pipeline.validate(self.master, self.scene, cameras)
            if label in {"empty", "1,000 appended"}:
                id_list_validator.assert_not_called()

    def test_camera_manifest_schema_is_exact_and_mode_specific(self) -> None:
        rename_cases = [
            (index, field, f"{field}z")
            for index in range(len(self.cameras["cameras"]))
            for field in ("focus_nodes", "focus_edges")
        ] + [
            (4, "map_asset", "map_assets"),
            (5, "pulse_edges", "pulse_edgez"),
        ]
        for index, source, replacement in rename_cases:
            cameras = deepcopy(self.cameras)
            cameras["cameras"][index][replacement] = cameras["cameras"][index].pop(
                source
            )
            with (
                self.subTest(source=source, replacement=replacement),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "fields must be exact"
                ),
            ):
                scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["unknown"] = True
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "fields must be exact"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["meta"]["unknown"] = True
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "fields must be exact"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][1]["map_view"] = [0, 0, 1, 1]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "fields must be exact for 3d"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_camera_manifest_schema_rejects_coercion_and_incomplete_ownership(
        self,
    ) -> None:
        cameras = deepcopy(self.cameras)
        cameras["meta"]["version"] = True
        with self.assertRaisesRegex(scene_pipeline.ManifestError, "integer 1"):
            scene_pipeline.validate(self.master, self.scene, cameras)

        mutations = (
            (0, "focus_nodes", [True]),
            (
                0,
                "focus_edges",
                ["grid138_source_to_tie", "grid138_source_to_tie"],
            ),
            (4, "map_asset", "../map.svg"),
            (5, "pulse_edges", ["grid138_source_to_tie"]),
        )
        for index, field, value in mutations:
            cameras = deepcopy(self.cameras)
            cameras["cameras"][index][field] = value
            with (
                self.subTest(field=field, value=value),
                self.assertRaises(scene_pipeline.ManifestError),
            ):
                scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][4]["annotation"]["extra"] = "ignored"
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "fields must be exact"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][4]["annotation"]["fields"] = ["not_a_node_field"]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "unknown annotation fields"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_camera_label_offsets_reject_falsey_nonmappings_and_mixed_keys(
        self,
    ) -> None:
        for value in (False, [], "", None):
            cameras = deepcopy(self.cameras)
            cameras["cameras"][1]["label_offsets"] = value
            with (
                self.subTest(value=value),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "label_offsets must be a mapping"
                ),
            ):
                scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][1]["label_offsets"] = {
            "not_a_focus_node": [0, 0],
            7: [0, 0],
            ("tuple",): [0, 0],
        }
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "invalid_label_offsets"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_camera_rectangles_require_positive_extents_but_allow_coordinates(
        self,
    ) -> None:
        rectangles = [
            (index, field)
            for index, camera in enumerate(self.cameras["cameras"])
            for field in ("viewBox", "well", "map_view", "compact_viewBox")
            if field in camera
        ]
        self.assertEqual(15, len(rectangles))

        rejected_probes = 0
        for index, field in rectangles:
            for dimension_index, dimension in ((2, "width"), (3, "height")):
                for invalid in (0, -1):
                    cameras = deepcopy(self.cameras)
                    cameras["cameras"][index][field][dimension_index] = invalid
                    rejected_probes += 1
                    with (
                        self.subTest(
                            camera=cameras["cameras"][index]["id"],
                            field=field,
                            dimension=dimension,
                            invalid=invalid,
                        ),
                        self.assertRaisesRegex(
                            scene_pipeline.ManifestError,
                            rf"{field}\.{dimension}: expected a positive number",
                        ),
                    ):
                        scene_pipeline.validate(self.master, self.scene, cameras)
        self.assertEqual(60, rejected_probes)

        allowed_coordinate_probes = 0
        for index, field in rectangles:
            for coordinate_index, coordinate in ((0, -1), (1, 0)):
                cameras = deepcopy(self.cameras)
                cameras["cameras"][index][field][coordinate_index] = coordinate
                scene_pipeline.validate(self.master, self.scene, cameras)
                allowed_coordinate_probes += 1
        self.assertEqual(30, allowed_coordinate_probes)

    def test_camera_focus_edges_and_annotations_are_owned_by_focus_nodes(
        self,
    ) -> None:
        master_edges = {edge["id"]: edge for edge in self.master["edges"]}
        edge_ownership_probes = 0
        for index, camera in enumerate(self.cameras["cameras"]):
            if not camera["focus_edges"]:
                continue
            edge = master_edges[camera["focus_edges"][0]]
            cameras = deepcopy(self.cameras)
            cameras["cameras"][index]["focus_nodes"].remove(edge["from"])
            edge_ownership_probes += 1
            with (
                self.subTest(camera=camera["id"], edge=edge["id"]),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "nonfocus_edge_endpoints"
                ),
            ):
                scene_pipeline.validate(self.master, self.scene, cameras)
        self.assertEqual(5, edge_ownership_probes)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][4]["annotation"] = {
            "node": "ups",
            "fields": ["label"],
        }
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "annotation node must be in focus_nodes"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][4]["annotation"]["fields"] = []
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "annotation.fields must be non-empty"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_three_dimensional_camera_anchor_focus_visibility_is_exact(self) -> None:
        expected = {
            "campus_establishing": (514, 508, [514, 514, 514, 514, 209]),
            "electrical_room": (43, 39, [43, 43, 43, 43, 33]),
            "data_hall_rack": (162, 156, [162, 162, 162, 162, 86]),
            "thermal_return": (288, 278, [288, 288, 288, 288, 160]),
        }
        self.assertEqual(
            scene_pipeline.CAMERA_FOCUS_COVERAGE_POLICY,
            (
                ("1920x1080", 1920, 1080, 1, 1),
                ("1440x900", 1440, 900, 1, 1),
                ("1024x768", 738, 582, 1, 1),
                ("844x390", 844, 390, 1, 1),
                ("390x844", 390, 844, 1, 3),
            ),
        )
        observed_points = 0
        observed_geometry_witnesses = 0
        for camera in self.cameras["cameras"]:
            if camera["mode"] != "3d":
                continue
            with self.subTest(camera=camera["id"]):
                coverage = scene_pipeline._camera_focus_visibility(self.scene, camera)
                point_count, effective_count, visible_counts = expected[camera["id"]]
                observed_points += point_count
                observed_geometry_witnesses += effective_count
                self.assertEqual(point_count, coverage["point_count"])
                self.assertEqual(point_count, coverage["depth_visible_point_count"])
                self.assertEqual(
                    effective_count, coverage["effective_geometry_witness_count"]
                )
                self.assertEqual([], coverage["depth_invisible_point_ids"])
                self.assertEqual(
                    visible_counts,
                    [
                        viewport["visible_point_count"]
                        for viewport in coverage["viewport_coverage"]
                    ],
                )
        self.assertEqual(1_007, observed_points)
        self.assertEqual(981, observed_geometry_witnesses)

    def test_camera_anchor_visibility_rejects_blank_node_and_edge_geometry(
        self,
    ) -> None:
        cameras = deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        campus["position"] = [1_000_000, 1_000_000, 1_000_000]
        for gateway in (
            lambda: scene_pipeline.validate(self.master, self.scene, cameras),
            lambda: scene_pipeline.build_payload(self.master, self.scene, cameras),
        ):
            with self.assertRaisesRegex(
                scene_pipeline.ManifestError,
                "authored position-target distance.*OrbitControls range",
            ):
                gateway()

        cameras = deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        campus["position"] = [786, 970, 1_288]
        campus["target"] = [-396, 507, -188]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "focus geometry coverage at 1024x768.*visible=498 declared=514",
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

        scene = deepcopy(self.scene)
        primitive = scene["nodes"]["campus_mv_distribution"]["primitives"][0]
        primitive["at"] = [1_000_000] * 3
        scene["nodes"]["campus_mv_distribution"]["label_at"] = [1_000_000] * 3
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "focus geometry.*node:campus_mv_distribution.*primitive",
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

        scene = deepcopy(self.scene)
        scene["nodes"]["gas_turbine"]["at"] = [1_000_000] * 3
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "3D anchor focus geometry.*node:gas_turbine",
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

        master = deepcopy(self.master)
        next(node for node in master["nodes"] if node["id"] == "gas_turbine")[
            "base_visible"
        ] = False
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            r"hidden_focus_nodes=\['gas_turbine'\]",
        ):
            scene_pipeline.validate(master, self.scene, self.cameras)

        minimum_opacity = scene_pipeline._webgl_float32(
            scene_pipeline.MIN_VISIBLE_FOCUS_OPACITY
        )
        minimum_opacity_bits = struct.unpack(
            ">I", struct.pack(">f", minimum_opacity)
        )[0]
        immediately_below_minimum = struct.unpack(
            ">f", struct.pack(">I", minimum_opacity_bits - 1)
        )[0]
        self.assertEqual(
            minimum_opacity,
            scene_pipeline._webgl_float32(scene_pipeline.MIN_VISIBLE_FOCUS_OPACITY),
        )
        for opacity in (0, 2**-149, immediately_below_minimum):
            cameras = deepcopy(self.cameras)
            campus = next(
                camera
                for camera in cameras["cameras"]
                if camera["id"] == "campus_establishing"
            )
            campus["focus_nodes"] = ["campus_mv_distribution"]
            campus["focus_edges"] = []
            campus["label_nodes"] = []
            campus["label_offsets"] = {}
            scene = deepcopy(self.scene)
            scene["nodes"]["campus_mv_distribution"]["primitives"][0][
                "opacity"
            ] = opacity
            with (
                self.subTest(opacity=opacity),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    "at least one rendered focus-geometry witness",
                ),
            ):
                scene_pipeline.validate(self.master, scene, cameras)

        scene["nodes"]["campus_mv_distribution"]["primitives"][0][
            "opacity"
        ] = minimum_opacity
        scene["world"]["fog"]["near"] = 3_500
        scene_pipeline.validate(self.master, scene, cameras)

        cameras = deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        campus["focus_nodes"] = ["campus_mv_distribution"]
        campus["focus_edges"] = []
        campus["label_nodes"] = ["campus_mv_distribution"]
        campus["label_offsets"] = {
            "campus_mv_distribution": [1_000_000, 1_000_000]
        }
        scene = deepcopy(self.scene)
        scene["nodes"]["campus_mv_distribution"]["primitives"][0]["opacity"] = 0
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "at least one rendered focus-geometry witness",
        ):
            scene_pipeline.validate(self.master, scene, cameras)

        cameras = deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        direction = [0, math.cos(1.5), math.sin(1.5)]
        campus["position"] = [0, 0, 0]
        campus["target"] = [-3_198 * value for value in direction]
        campus["focus_nodes"] = ["campus_mv_distribution"]
        campus["focus_edges"] = []
        campus["label_nodes"] = []
        campus["label_offsets"] = {}
        scene = deepcopy(self.scene)
        center = [-3_597 * value for value in direction]
        scene["nodes"]["campus_mv_distribution"] = {
            "at": center,
            "label_at": center,
            "primitives": [
                {
                    "shape": "box",
                    "size": [1, 1, 1],
                    "at": [0, 0, 0],
                    "fill": "ink",
                    "opacity": 1,
                }
            ],
        }
        coverage = scene_pipeline._camera_focus_visibility(scene, campus)
        self.assertEqual(8, coverage["depth_visible_point_count"])
        self.assertEqual(0, coverage["effective_geometry_witness_count"])
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "effective post-fog opacity.*8-bit step",
        ):
            scene_pipeline.validate(self.master, scene, cameras)

        scene = deepcopy(self.scene)
        scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [1_000_000, 1_000_000, 1_000_000],
            [1_000_080, 1_000_000, 1_000_000],
        ]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "3D anchor focus geometry.*edge:btm_fuel_to_shaft",
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

        scene = deepcopy(self.scene)
        scene["world"]["fog"] = {"near": 0, "far": 1_000}
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "3D anchor focus geometry.*fog visibility",
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

    def test_camera_direction_must_survive_float32_quantization(self) -> None:
        cameras = deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        campus["position"] = [2**30, 2**30, 2**30]
        campus["target"] = [2**30 + 1, 2**30 + 1, 2**30 + 1]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "position-target direction.*Float32 quantization",
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_camera_distance_matches_both_renderer_control_ranges(self) -> None:
        for distance, message in (
            (scene_pipeline.THREE_CAMERA_MIN_DISTANCE - 1, "minimum=90.0"),
            (scene_pipeline.THREE_HYBRID_CAMERA_MAX_DISTANCE + 1, "maximum=3200.0"),
        ):
            cameras = deepcopy(self.cameras)
            camera = next(
                item for item in cameras["cameras"] if item["id"] == "electrical_room"
            )
            camera["position"] = [camera["target"][0] + distance, *camera["target"][1:]]
            with (
                self.subTest(distance=distance),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    f"OrbitControls range.*{message}",
                ),
            ):
                scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        campus["position"] = [-224.109, -1_432.85, 782.087]
        campus["target"] = [-611.697, -20.177, -33.824]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "polar angle.*OrbitControls range",
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

        html = scene_pipeline.render_html(
            scene_pipeline.build_payload(self.master, self.scene, self.cameras)
        )
        self.assertIn("new THREE.PerspectiveCamera(\n  40,", html)
        self.assertIn("  1,\n  5000\n);", html)
        self.assertIn("controls.minDistance = 90;", html)
        self.assertIn("controls.maxDistance = 3200;", html)
        self.assertIn("controls.minPolarAngle = Math.PI * 0;", html)
        self.assertIn("controls.maxPolarAngle = Math.PI * 0.49;", html)
        self.assertIn("camera.up.set(...data.world.camera_up).normalize();", html)
        self.assertIn("new THREE.SphereGeometry(6.2, 14, 14)", html)
        self.assertNotIn("__THREE_", html)
        self.assertNotIn("__MIN_HYBRID_", html)
        self.assertNotIn("__HYBRID_CONFIRMED_", html)

    def test_hybrid_focus_render_clears_context_depth_and_restores_state(
        self,
    ) -> None:
        scene = deepcopy(self.scene)
        campus_pad = next(
            structure
            for structure in scene["structures"]
            if structure["id"] == "campus-pad"
        )
        campus_pad["primitives"][0] = {
            "shape": "box",
            "size": [10_000, 10_000, 10],
            "at": [0, 0, 750],
            "fill": "ink",
            "opacity": 1,
        }
        scene_pipeline.validate(self.master, scene, self.cameras)
        html = scene_pipeline.render_html(
            scene_pipeline.build_payload(self.master, scene, self.cameras)
        )

        start = html.index("function renderDepthSeparatedFocus()")
        end = html.index("\n}\n", start) + 2
        render_contract = html[start:end]
        ordered = (
            "renderer.autoClear = true;",
            "camera.layers.set(CONTEXT_LAYER);",
            "renderer.render(scene, camera);",
            "renderer.clearDepth();",
            "scene.background = null;",
            "renderer.autoClear = false;",
            "camera.layers.set(FOCUS_LAYER);",
            "renderer.render(scene, camera);",
            "scene.background = background;",
            "renderer.autoClear = autoClear;",
            "camera.layers.mask = cameraLayerMask;",
        )
        positions = []
        cursor = 0
        for fragment in ordered:
            position = render_contract.index(fragment, cursor)
            positions.append(position)
            cursor = position + len(fragment)
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(2, render_contract.count("renderer.render(scene, camera);"))
        self.assertEqual(1, render_contract.count("renderer.clearDepth();"))
        self.assertIn(
            "object.traverse(child => child.layers.set(layer));",
            html,
        )
        self.assertIn(
            "setLayerRecursively(object, selected ? FOCUS_LAYER : CONTEXT_LAYER);",
            html,
        )
        self.assertIn("hemisphereLight.layers.enable(FOCUS_LAYER);", html)
        self.assertIn("keyLight.layers.enable(FOCUS_LAYER);", html)
        self.assertIn("pulse.layers.set(FOCUS_LAYER);", html)
        self.assertLess(
            html.index("camera.layers.mask = cameraLayerMask;"),
            html.index("labelRenderer.render(scene, camera);"),
        )

        label_rule = html.split(".node-label {", 1)[1].split("}", 1)[0]
        self.assertNotIn("max-width", label_rule)
        self.assertIn("white-space: nowrap;", label_rule)

    def test_camera_label_nodes_are_known_focus_nodes(self) -> None:
        payload = scene_pipeline.build_payload(self.master, self.scene, self.cameras)
        campus = next(
            camera
            for camera in payload["cameras"]
            if camera["id"] == "campus_establishing"
        )
        self.assertTrue(set(campus["label_nodes"]) <= set(campus["focus_nodes"]))
        self.assertIn(
            "const labelFocus = new Set(state.label_nodes || []);",
            scene_pipeline.render_html(payload),
        )

        thermal = next(
            camera for camera in payload["cameras"] if camera["id"] == "thermal_return"
        )
        self.assertTrue(set(thermal["label_offsets"]) <= set(thermal["focus_nodes"]))
        self.assertIn("state.label_offsets?.[id]", scene_pipeline.render_html(payload))

        cameras = deepcopy(self.cameras)
        cameras["cameras"][1]["label_nodes"] = ["not_a_master_node"]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "unknown_label_nodes"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

        cameras = deepcopy(self.cameras)
        cameras["cameras"][1]["label_nodes"] = ["unit_substation"]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "nonfocus_label_nodes"
        ):
            scene_pipeline.validate(self.master, self.scene, cameras)

    def test_scene_schema_rejects_missing_and_extra_fields_exhaustively(
        self,
    ) -> None:
        records: list[tuple[tuple, set[str]]] = [
            ((), scene_pipeline.SCENE_ROOT_FIELDS),
            (("meta",), scene_pipeline.SCENE_META_FIELDS),
            (("world",), scene_pipeline.SCENE_WORLD_FIELDS),
            (("world", "ground"), scene_pipeline.SCENE_GROUND_FIELDS),
            (("world", "fog"), scene_pipeline.SCENE_FOG_FIELDS),
        ]
        for structure_index, structure in enumerate(self.scene["structures"]):
            records.append(
                (
                    ("structures", structure_index),
                    scene_pipeline.SCENE_STRUCTURE_REQUIRED_FIELDS,
                )
            )
            if "repeat" in structure:
                records.append(
                    (
                        ("structures", structure_index, "repeat"),
                        scene_pipeline.SCENE_REPEAT_FIELDS,
                    )
                )
            for primitive_index, primitive in enumerate(structure["primitives"]):
                records.append(
                    (
                        ("structures", structure_index, "primitives", primitive_index),
                        scene_pipeline.PRIMITIVE_COMMON_REQUIRED_FIELDS
                        | scene_pipeline.PRIMITIVE_REQUIRED_FIELDS_BY_SHAPE[
                            primitive["shape"]
                        ],
                    )
                )
        for node_id, node in self.scene["nodes"].items():
            records.append((("nodes", node_id), scene_pipeline.SCENE_NODE_FIELDS))
            for primitive_index, primitive in enumerate(node["primitives"]):
                records.append(
                    (
                        ("nodes", node_id, "primitives", primitive_index),
                        scene_pipeline.PRIMITIVE_COMMON_REQUIRED_FIELDS
                        | scene_pipeline.PRIMITIVE_REQUIRED_FIELDS_BY_SHAPE[
                            primitive["shape"]
                        ],
                    )
                )
        records.extend(
            (("edges", edge_id), scene_pipeline.SCENE_EDGE_REQUIRED_FIELDS)
            for edge_id in self.scene["edges"]
        )
        self.assertEqual(129, len(records))

        def record_at(scene, path):
            target = scene
            for key in path:
                target = target[key]
            return target

        missing_field_probes = 0
        for path, required_fields in records:
            for field in required_fields:
                scene = deepcopy(self.scene)
                record_at(scene, path).pop(field)
                missing_field_probes += 1
                with (
                    self.subTest(mutation="missing", path=path, field=field),
                    self.assertRaises(scene_pipeline.ManifestError),
                ):
                    scene_pipeline.validate(self.master, scene, self.cameras)
        self.assertEqual(389, missing_field_probes)

        for path, _ in records:
            scene = deepcopy(self.scene)
            record_at(scene, path)["unexpected_field"] = True
            with (
                self.subTest(mutation="extra", path=path),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "fields must be exact"
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

    def test_scene_structure_context_ids_and_order_are_exact(self) -> None:
        self.assertEqual(
            scene_pipeline.CANONICAL_STRUCTURE_IDS,
            tuple(structure["id"] for structure in self.scene["structures"]),
        )

        mutations = []
        empty = deepcopy(self.scene)
        empty["structures"] = []
        mutations.append(("empty", empty))

        missing = deepcopy(self.scene)
        missing["structures"].pop()
        mutations.append(("missing", missing))

        reordered = deepcopy(self.scene)
        reordered["structures"][:2] = reversed(reordered["structures"][:2])
        mutations.append(("reordered", reordered))

        renamed = deepcopy(self.scene)
        renamed["structures"][0]["id"] = "renamed-context"
        mutations.append(("renamed", renamed))

        appended = deepcopy(self.scene)
        appended["structures"].append(deepcopy(appended["structures"][0]))
        mutations.append(("appended", appended))

        for label, scene in mutations:
            with (
                self.subTest(label=label),
                patch.object(scene_pipeline, "_validate_primitive_schema") as validator,
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    r"canonical context layers|\.id must be",
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)
            validator.assert_not_called()

        for coverage in (None, [], {}, "typo"):
            scene = deepcopy(self.scene)
            scene["meta"]["coverage"] = coverage
            with (
                self.subTest(coverage=coverage),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "coverage must be exact or subset"
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

    def test_primitive_schema_rejects_typo_and_cross_shape_fields_exhaustively(
        self,
    ) -> None:
        primitive_paths = [
            ("structures", structure_index, "primitives", primitive_index)
            for structure_index, structure in enumerate(self.scene["structures"])
            for primitive_index in range(len(structure["primitives"]))
        ] + [
            ("nodes", node_id, "primitives", primitive_index)
            for node_id, node in self.scene["nodes"].items()
            for primitive_index in range(len(node["primitives"]))
        ]
        self.assertEqual(55, len(primitive_paths))

        cross_shape_probes = 0
        for path in primitive_paths:
            scene = deepcopy(self.scene)
            primitive = scene
            for key in path:
                primitive = primitive[key]
            if primitive["shape"] == "box":
                primitive["radius"] = 1
            else:
                primitive["size"] = [1, 1, 1]
            cross_shape_probes += 1
            with (
                self.subTest(path=path, shape=primitive["shape"]),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "fields must be exact"
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)
        self.assertEqual(55, cross_shape_probes)

        scene = deepcopy(self.scene)
        primitive = scene["structures"][0]["primitives"][0]
        primitive["opacitiy"] = primitive.pop("opacity")
        with self.assertRaisesRegex(scene_pipeline.ManifestError, "opacitiy"):
            scene_pipeline.validate(self.master, scene, self.cameras)

        for shape in (None, [], {}):
            scene = deepcopy(self.scene)
            scene["structures"][0]["primitives"][0]["shape"] = shape
            with (
                self.subTest(shape=shape),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "unsupported shape"
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

    def test_repeat_schema_is_exact_and_never_truthiness_bypassed(self) -> None:
        repeat_index = next(
            index
            for index, structure in enumerate(self.scene["structures"])
            if "repeat" in structure
        )
        invalid_payloads = (
            None,
            False,
            True,
            "",
            "repeat",
            [],
            [1],
            {},
            {"count": 6},
            {"step": [0, 0, 58]},
            {"count": 6, "step": [0, 0, 58], "extra": 1},
        )
        for payload in invalid_payloads:
            scene = deepcopy(self.scene)
            scene["structures"][repeat_index]["repeat"] = payload
            with (
                self.subTest(payload=payload),
                self.assertRaisesRegex(scene_pipeline.ManifestError, "repeat"),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)
        self.assertEqual(11, len(invalid_payloads))

        for count in (None, False, True, 0, -1, 1.0, "1", 10**400):
            scene = deepcopy(self.scene)
            scene["structures"][repeat_index]["repeat"]["count"] = count
            with (
                self.subTest(count=count),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, r"repeat\.count: invalid"
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

        invalid_steps = (
            None,
            False,
            "",
            [],
            {},
            [0, 0],
            [0, 0, 0, 0],
            [0, False, 0],
            [0, math.nan, 0],
        )
        for step in invalid_steps:
            scene = deepcopy(self.scene)
            scene["structures"][repeat_index]["repeat"]["step"] = step
            with (
                self.subTest(step=step),
                self.assertRaisesRegex(scene_pipeline.ManifestError, r"repeat\.step"),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

        scene = deepcopy(self.scene)
        scene["structures"][repeat_index]["repeat"] = {
            "count": 1,
            "step": [0, 0, 0],
        }
        scene_pipeline.validate(self.master, scene, self.cameras)

    def test_repeat_count_and_expanded_primitive_budget_are_bounded(self) -> None:
        repeat_index = next(
            index
            for index, structure in enumerate(self.scene["structures"])
            if "repeat" in structure
        )
        current_expanded = sum(
            len(structure["primitives"]) * structure.get("repeat", {}).get("count", 1)
            for structure in self.scene["structures"]
        ) + sum(len(node["primitives"]) for node in self.scene["nodes"].values())
        self.assertEqual(60, current_expanded)

        scene = deepcopy(self.scene)
        scene["structures"][repeat_index]["repeat"]["count"] = (
            scene_pipeline.MAX_REPEAT_COUNT
        )
        scene_pipeline.validate(self.master, scene, self.cameras)

        for count in (scene_pipeline.MAX_REPEAT_COUNT + 1, 10**308):
            scene = deepcopy(self.scene)
            scene["structures"][repeat_index]["repeat"]["count"] = count
            with (
                self.subTest(count=count),
                patch.object(scene_pipeline, "_validate_primitive_schema") as validator,
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    rf"1 through {scene_pipeline.MAX_REPEAT_COUNT}",
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)
            validator.assert_not_called()

        scene = deepcopy(self.scene)
        structure = scene["structures"][repeat_index]
        structure["repeat"]["count"] = scene_pipeline.MAX_REPEAT_COUNT
        structure["primitives"] *= 8
        with (
            patch.object(scene_pipeline, "_validate_primitive_schema") as validator,
            self.assertRaisesRegex(
                scene_pipeline.ManifestError, "expanded primitive budget exceeded"
            ),
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)
        validator.assert_not_called()

    def test_repeat_derived_coordinates_stay_in_webgl_float32_safe_range(
        self,
    ) -> None:
        repeat_index = next(
            index
            for index, structure in enumerate(self.scene["structures"])
            if "repeat" in structure
        )
        individually_safe = scene_pipeline.MAX_WEBGL_MAGNITUDE * 0.75

        scene = deepcopy(self.scene)
        repeat = scene["structures"][repeat_index]["repeat"]
        repeat["count"] = 3
        repeat["step"] = [individually_safe, 0, 0]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "repeat-derived offset"
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

        scene = deepcopy(self.scene)
        structure = scene["structures"][repeat_index]
        structure["repeat"] = {
            "count": 2,
            "step": [individually_safe, 0, 0],
        }
        structure["primitives"][0]["at"][0] = individually_safe
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError, "repeat-derived primitive position"
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

    def test_edge_point_and_tube_segment_budgets_are_bounded_before_walks(
        self,
    ) -> None:
        edge_ids = list(self.scene["edges"])
        first_edge = edge_ids[0]
        current_point_count = sum(
            len(edge["points"]) for edge in self.scene["edges"].values()
        )
        current_tube_segments = sum(
            scene_pipeline.edge_tube_segment_count(len(edge["points"]))
            for edge in self.scene["edges"].values()
        )
        self.assertEqual(93, current_point_count)
        self.assertEqual(930, current_tube_segments)
        self.assertEqual(
            (12, 10, 8),
            (
                scene_pipeline.MIN_EDGE_TUBE_SEGMENTS,
                scene_pipeline.EDGE_TUBE_SEGMENTS_PER_POINT,
                scene_pipeline.EDGE_TUBE_RADIAL_SEGMENTS,
            ),
        )
        rendered = scene_pipeline.render_html(
            scene_pipeline.build_payload(self.master, self.scene, self.cameras)
        )
        self.assertIn("radius, 8, false", rendered)
        self.assertNotIn("__EDGE_TUBE_RADIAL_SEGMENTS__", rendered)
        self.assertEqual(
            scene_pipeline.MAX_TOTAL_EDGE_TUBE_SEGMENTS,
            scene_pipeline.MAX_TOTAL_EDGE_POINTS
            * scene_pipeline.EDGE_TUBE_SEGMENTS_PER_POINT,
        )

        def points(count):
            return [[index, 0, 0] for index in range(count)]

        scene = deepcopy(self.scene)
        scene["edges"][first_edge]["points"] = points(scene_pipeline.MAX_EDGE_POINTS)
        scene_pipeline.validate_webgl_numeric_domain(scene)

        class HugeReportedPointList(list):
            def __len__(self) -> int:
                return 10_000_000

        oversized_lists = (
            points(scene_pipeline.MAX_EDGE_POINTS + 1),
            points(10_000),
            HugeReportedPointList(points(2)),
        )
        for edge_points in oversized_lists:
            scene = deepcopy(self.scene)
            scene["edges"][first_edge]["points"] = edge_points
            with (
                self.subTest(reported_count=len(edge_points)),
                patch.object(scene_pipeline, "_validate_primitive_schema") as validator,
                patch.object(scene_pipeline, "_triplet") as point_validator,
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "edge point count"
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)
            validator.assert_not_called()
            point_validator.assert_not_called()

        def scene_with_total_points(total):
            scene = deepcopy(self.scene)
            base, remainder = divmod(total, len(edge_ids))
            for index, edge_id in enumerate(edge_ids):
                count = base + (index < remainder)
                scene["edges"][edge_id]["points"] = points(count)
            return scene

        boundary = scene_with_total_points(scene_pipeline.MAX_TOTAL_EDGE_POINTS)
        self.assertLessEqual(
            max(len(edge["points"]) for edge in boundary["edges"].values()),
            scene_pipeline.MAX_EDGE_POINTS,
        )
        scene_pipeline.validate_webgl_numeric_domain(boundary)

        over_budget = scene_with_total_points(scene_pipeline.MAX_TOTAL_EDGE_POINTS + 1)
        with (
            patch.object(scene_pipeline, "_validate_primitive_schema") as validator,
            patch.object(scene_pipeline, "_triplet") as point_validator,
            self.assertRaisesRegex(
                scene_pipeline.ManifestError, "total edge point budget exceeded"
            ),
        ):
            scene_pipeline.validate(self.master, over_budget, self.cameras)
        validator.assert_not_called()
        point_validator.assert_not_called()

    def test_browser_number_range_is_closed_exhaustively(self) -> None:
        maximum_finite_float = float.fromhex("0x1.fffffffffffffp+1023")
        self.assertEqual(float.fromhex("0x1.fffffep+127"), scene_pipeline.FLOAT32_MAX)
        self.assertEqual(
            scene_pipeline.FLOAT32_MAX / scene_pipeline.WEBGL_FLOAT32_HEADROOM,
            scene_pipeline.MAX_WEBGL_MAGNITUDE,
        )
        self.assertLess(scene_pipeline.MAX_WEBGL_MAGNITUDE, scene_pipeline.FLOAT32_MAX)
        for valid in (
            0,
            -0.0,
            scene_pipeline.MAX_WEBGL_MAGNITUDE,
            -scene_pipeline.MAX_WEBGL_MAGNITUDE,
        ):
            with self.subTest(webgl_safe=valid):
                self.assertTrue(scene_pipeline._is_webgl_safe_number(valid))
        for invalid in (
            1e39,
            -1e39,
            scene_pipeline.MAX_WEBGL_MAGNITUDE * 2,
            -scene_pipeline.MAX_WEBGL_MAGNITUDE * 2,
        ):
            with self.subTest(webgl_unsafe=invalid):
                self.assertFalse(scene_pipeline._is_webgl_safe_number(invalid))

        for valid in (0, -0.0, 10**308, -(10**308), maximum_finite_float):
            with self.subTest(valid=valid):
                self.assertTrue(scene_pipeline._is_finite_number(valid))
        for invalid in (
            True,
            False,
            math.nan,
            math.inf,
            -math.inf,
            10**400,
            -(10**400),
        ):
            with self.subTest(invalid=invalid):
                self.assertFalse(scene_pipeline._is_finite_number(invalid))

        scene_paths = []
        for field in ("size", "at"):
            scene_paths.extend(
                ("world", "ground", field, index)
                for index in range(len(self.scene["world"]["ground"][field]))
            )
        scene_paths.extend(("world", "fog", field) for field in ("near", "far"))
        scene_paths.extend(
            ("world", "camera_up", index)
            for index in range(len(self.scene["world"]["camera_up"]))
        )

        primitive_records = []
        for structure_index, structure in enumerate(self.scene["structures"]):
            primitive_records.extend(
                (
                    ("structures", structure_index, "primitives", primitive_index),
                    primitive,
                )
                for primitive_index, primitive in enumerate(structure["primitives"])
            )
            if "repeat" in structure:
                scene_paths.extend(
                    ("structures", structure_index, "repeat", "step", index)
                    for index in range(len(structure["repeat"]["step"]))
                )
        for node_id, node in self.scene["nodes"].items():
            for field in ("at", "label_at"):
                scene_paths.extend(
                    ("nodes", node_id, field, index)
                    for index in range(len(node[field]))
                )
            primitive_records.extend(
                (
                    ("nodes", node_id, "primitives", primitive_index),
                    primitive,
                )
                for primitive_index, primitive in enumerate(node["primitives"])
            )

        for path, primitive in primitive_records:
            scene_paths.extend(
                (*path, "at", index) for index in range(len(primitive["at"]))
            )
            if primitive["shape"] == "box":
                scene_paths.extend(
                    (*path, "size", index) for index in range(len(primitive["size"]))
                )
            else:
                scene_paths.extend((*path, field) for field in ("radius", "height"))
            if "rotate" in primitive:
                scene_paths.extend(
                    (*path, "rotate", index)
                    for index in range(len(primitive["rotate"]))
                )
            if "opacity" in primitive:
                scene_paths.append((*path, "opacity"))

        for edge_id, edge in self.scene["edges"].items():
            scene_paths.extend(
                ("edges", edge_id, "points", point_index, coordinate_index)
                for point_index, point in enumerate(edge["points"])
                for coordinate_index in range(len(point))
            )

        camera_paths = []
        for camera_index, camera in enumerate(self.cameras["cameras"]):
            for field in ("viewBox", "well", "map_view", "position", "target"):
                if field in camera:
                    camera_paths.extend(
                        ("cameras", camera_index, field, coordinate_index)
                        for coordinate_index in range(len(camera[field]))
                    )
            for node_id, offset in camera.get("label_offsets", {}).items():
                camera_paths.extend(
                    (
                        "cameras",
                        camera_index,
                        "label_offsets",
                        node_id,
                        coordinate_index,
                    )
                    for coordinate_index in range(len(offset))
                )

        self.assertEqual(840, len(scene_paths))
        self.assertEqual(108, len(camera_paths))

        def replace(container, path, value) -> None:
            target = container
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value

        rejected_probes = 0
        for huge_integer in (10**400, -(10**400)):
            for path in scene_paths:
                scene = deepcopy(self.scene)
                replace(scene, path, huge_integer)
                rejected_probes += 1
                with (
                    self.subTest(manifest="scene", path=path, sign=huge_integer > 0),
                    self.assertRaises(scene_pipeline.ManifestError),
                ):
                    scene_pipeline.validate(self.master, scene, self.cameras)
            for path in camera_paths:
                cameras = deepcopy(self.cameras)
                replace(cameras, path, huge_integer)
                rejected_probes += 1
                with (
                    self.subTest(manifest="cameras", path=path, sign=huge_integer > 0),
                    self.assertRaises(scene_pipeline.ManifestError),
                ):
                    scene_pipeline.validate(self.master, self.scene, cameras)
        self.assertEqual(1896, rejected_probes)

        float32_overflow_probes = 0
        for path in scene_paths:
            scene = deepcopy(self.scene)
            replace(scene, path, 1e39)
            float32_overflow_probes += 1
            with (
                self.subTest(manifest="scene", path=path, value="1e39"),
                self.assertRaises(scene_pipeline.ManifestError),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)
        for path in camera_paths:
            cameras = deepcopy(self.cameras)
            replace(cameras, path, 1e39)
            float32_overflow_probes += 1
            with (
                self.subTest(manifest="cameras", path=path, value="1e39"),
                self.assertRaises(scene_pipeline.ManifestError),
            ):
                scene_pipeline.validate(self.master, self.scene, cameras)
        self.assertEqual(948, float32_overflow_probes)

    def test_build_payload_rejects_float32_geometry_overflow(self) -> None:
        cases = []

        scene = deepcopy(self.scene)
        scene["structures"][0]["primitives"][0]["size"][0] = 1e39
        cases.append(("box dimension", scene, "WebGL Float32-safe bound"))

        scene = deepcopy(self.scene)
        scene["nodes"]["gas_turbine"]["at"][0] = 1e39
        cases.append(("node position", scene, "WebGL Float32-safe bound"))

        scene = deepcopy(self.scene)
        repeated = next(
            structure for structure in scene["structures"] if "repeat" in structure
        )
        repeated["repeat"]["count"] = 3
        repeated["repeat"]["step"] = [
            scene_pipeline.MAX_WEBGL_MAGNITUDE * 0.75,
            0,
            0,
        ]
        cases.append(("repeat-derived position", scene, "repeat-derived offset"))

        for label, invalid_scene, message in cases:
            for gateway in (
                scene_pipeline.validate_webgl_numeric_domain,
                lambda candidate: scene_pipeline.validate(
                    self.master, candidate, self.cameras
                ),
                lambda candidate: scene_pipeline.build_payload(
                    self.master, candidate, self.cameras
                ),
            ):
                with (
                    self.subTest(label=label, gateway=gateway),
                    self.assertRaisesRegex(scene_pipeline.ManifestError, message),
                ):
                    gateway(invalid_scene)

    def test_float32_collapsed_dimensions_are_rejected_exhaustively(self) -> None:
        dimension_paths = []
        for structure_index, structure in enumerate(self.scene["structures"]):
            for primitive_index, primitive in enumerate(structure["primitives"]):
                path = ("structures", structure_index, "primitives", primitive_index)
                if primitive["shape"] == "box":
                    dimension_paths.extend((*path, "size", index) for index in range(3))
                else:
                    dimension_paths.extend(
                        (*path, field) for field in ("radius", "height")
                    )
        for node_id, node in self.scene["nodes"].items():
            for primitive_index, primitive in enumerate(node["primitives"]):
                path = ("nodes", node_id, "primitives", primitive_index)
                if primitive["shape"] == "box":
                    dimension_paths.extend((*path, "size", index) for index in range(3))
                else:
                    dimension_paths.extend(
                        (*path, field) for field in ("radius", "height")
                    )
        dimension_paths.extend(("world", "ground", "size", index) for index in range(2))
        self.assertEqual(149, len(dimension_paths))

        for path in dimension_paths:
            scene = deepcopy(self.scene)
            target = scene
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = 1e-300
            with (
                self.subTest(path=path),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "positive.*Float32 quantization"
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

    def test_authored_geometry_extents_remain_float32_distinguishable_exhaustively(
        self,
    ) -> None:
        probes = []
        for structure_index, structure in enumerate(self.scene["structures"]):
            for primitive_index, primitive in enumerate(structure["primitives"]):
                path = ("structures", structure_index, "primitives", primitive_index)
                if primitive["shape"] == "box":
                    probes.extend((path, "size", axis, axis) for axis in range(3))
                else:
                    probes.extend(
                        (
                            (path, "radius", None, 0),
                            (path, "height", None, 1),
                        )
                    )
        for node_id, node in self.scene["nodes"].items():
            for primitive_index, primitive in enumerate(node["primitives"]):
                path = ("nodes", node_id, "primitives", primitive_index)
                if primitive["shape"] == "box":
                    probes.extend((path, "size", axis, axis) for axis in range(3))
                else:
                    probes.extend(
                        (
                            (path, "radius", None, 0),
                            (path, "height", None, 1),
                        )
                    )
        self.assertEqual(147, len(probes))

        authored_scale = 2**30
        for path, dimension_field, dimension_index, coordinate_index in probes:
            scene = deepcopy(self.scene)
            primitive = scene
            for key in path:
                primitive = primitive[key]
            if path[0] == "structures" and "repeat" in scene["structures"][path[1]]:
                scene["structures"][path[1]]["repeat"] = {
                    "count": 1,
                    "step": [0, 0, 0],
                }
            primitive["at"][coordinate_index] = authored_scale
            if dimension_index is None:
                primitive[dimension_field] = 1
            else:
                primitive[dimension_field][dimension_index] = 1
            with (
                self.subTest(path=path, dimension=dimension_field),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    "authored center and extent.*Float32 quantization",
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

        for size_index, coordinate_index in enumerate((0, 2)):
            scene = deepcopy(self.scene)
            scene["world"]["ground"]["at"][coordinate_index] = authored_scale
            scene["world"]["ground"]["size"][size_index] = 1
            with (
                self.subTest(path="ground", axis=coordinate_index),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    "authored center and extent.*Float32 quantization",
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

    def test_rotated_primitive_geometry_retains_float32_volume_exhaustively(
        self,
    ) -> None:
        box_paths = []
        for structure_index, structure in enumerate(self.scene["structures"]):
            box_paths.extend(
                ("structures", structure_index, "primitives", primitive_index)
                for primitive_index, primitive in enumerate(structure["primitives"])
                if primitive["shape"] == "box"
            )
        for node_id, node in self.scene["nodes"].items():
            box_paths.extend(
                ("nodes", node_id, "primitives", primitive_index)
                for primitive_index, primitive in enumerate(node["primitives"])
                if primitive["shape"] == "box"
            )
        self.assertEqual(37, len(box_paths))

        authored_scale = 2**30
        box_mutations = (
            ("local x", [1, 10, 256], [0, 90, 0], [0, 0, authored_scale]),
            ("local y", [10, 1, 256], [90, 0, 0], [0, 0, authored_scale]),
            ("local z", [256, 10, 1], [0, 90, 0], [authored_scale, 0, 0]),
        )
        box_probes = 0
        for path in box_paths:
            for thin_axis, size, rotate, center in box_mutations:
                scene = deepcopy(self.scene)
                primitive = scene
                for key in path:
                    primitive = primitive[key]
                base = [0, 0, 0]
                if path[0] == "nodes":
                    base = scene["nodes"][path[1]]["at"]
                elif "repeat" in scene["structures"][path[1]]:
                    scene["structures"][path[1]]["repeat"] = {
                        "count": 1,
                        "step": [0, 0, 0],
                    }
                primitive["at"] = [
                    float(value) - float(base[index])
                    for index, value in enumerate(center)
                ]
                primitive["size"] = size
                primitive["rotate"] = rotate
                box_probes += 1
                with (
                    self.subTest(path=path, thin_axis=thin_axis),
                    self.assertRaisesRegex(
                        scene_pipeline.ManifestError,
                        "rotation-aware transformed primitive geometry.*"
                        "Float32 quantization",
                    ),
                ):
                    scene_pipeline.validate(self.master, scene, self.cameras)
        self.assertEqual(111, box_probes)

        cylinder_paths = []
        for structure_index, structure in enumerate(self.scene["structures"]):
            cylinder_paths.extend(
                ("structures", structure_index, "primitives", primitive_index)
                for primitive_index, primitive in enumerate(structure["primitives"])
                if primitive["shape"] == "cylinder"
            )
        for node_id, node in self.scene["nodes"].items():
            cylinder_paths.extend(
                ("nodes", node_id, "primitives", primitive_index)
                for primitive_index, primitive in enumerate(node["primitives"])
                if primitive["shape"] == "cylinder"
            )
        self.assertEqual(18, len(cylinder_paths))

        for path in cylinder_paths:
            scene = deepcopy(self.scene)
            primitive = scene
            for key in path:
                primitive = primitive[key]
            base = [0, 0, 0]
            if path[0] == "nodes":
                base = scene["nodes"][path[1]]["at"]
            elif "repeat" in scene["structures"][path[1]]:
                scene["structures"][path[1]]["repeat"] = {
                    "count": 1,
                    "step": [0, 0, 0],
                }
            primitive["at"] = [
                -float(base[0]),
                -float(base[1]),
                authored_scale - float(base[2]),
            ]
            primitive["radius"] = 128
            primitive["height"] = 1
            primitive["rotate"] = [90, 0, 0]
            with (
                self.subTest(path=path, thin_axis="cylinder height"),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    "rotation-aware transformed primitive geometry.*"
                    "Float32 quantization",
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

    def test_every_edge_retains_sound_float32_tube_cross_section(self) -> None:
        base = 2**25 + 400
        points = [[base, base, base], [base + 80, base + 80, base + 80]]
        self.assertLess(
            scene_pipeline._webgl_float32(base - scene_pipeline.EDGE_TUBE_RADIUS),
            scene_pipeline._webgl_float32(base),
        )
        self.assertGreater(
            scene_pipeline._webgl_float32(base + scene_pipeline.EDGE_TUBE_RADIUS),
            scene_pipeline._webgl_float32(base),
        )
        self.assertGreaterEqual(
            scene_pipeline._edge_tube_cross_section_rounding_error_bound(points),
            scene_pipeline.EDGE_TUBE_RADIUS,
        )

        canonical_bounds = [
            scene_pipeline._edge_tube_cross_section_rounding_error_bound(edge["points"])
            for edge in self.scene["edges"].values()
        ]
        self.assertTrue(
            all(bound < scene_pipeline.EDGE_TUBE_RADIUS for bound in canonical_bounds)
        )
        self.assertGreater(
            min(scene_pipeline.EDGE_TUBE_RADIUS / bound for bound in canonical_bounds),
            24_000,
        )

        edge_probes = 0
        for edge_id in self.scene["edges"]:
            scene = deepcopy(self.scene)
            scene["edges"][edge_id]["points"] = points
            edge_probes += 1
            with (
                self.subTest(edge=edge_id),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    "TubeGeometry cross-section rounding-error bound.*"
                    "Float32 quantization",
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)
        self.assertEqual(34, edge_probes)

    def test_rotated_primitive_uses_float32_gpu_matrix_semantics(self) -> None:
        scene = deepcopy(self.scene)
        primitive = scene["structures"][0]["primitives"][0]
        primitive["at"] = [
            1024.1536073483026,
            1024.8170099900176,
            1025.117256280513,
        ]
        primitive["size"] = [
            0.0018179010284972768,
            0.00013933693226819645,
            0.004424568176824122,
        ]
        primitive["rotate"] = [
            113.38577503924103,
            93.41804158058227,
            -70.68951634408539,
        ]
        center = tuple(float(value) for value in primitive["at"])
        matrix = scene_pipeline._primitive_rotation_matrix(primitive["rotate"])
        final_round_only_vertices = tuple(
            tuple(
                scene_pipeline._webgl_float32(
                    center[world_axis]
                    + sum(
                        matrix[world_axis][local_axis] * vertex[local_axis]
                        for local_axis in range(3)
                    )
                )
                for world_axis in range(3)
            )
            for vertex in scene_pipeline._primitive_local_float32_vertices(primitive)
        )
        gpu_vertices = scene_pipeline._rotated_primitive_gpu_float32_vertices(
            primitive, center
        )
        self.assertEqual(
            3, scene_pipeline._float32_affine_rank(final_round_only_vertices)
        )
        self.assertEqual(8, len(set(final_round_only_vertices)))
        self.assertEqual(2, scene_pipeline._float32_affine_rank(gpu_vertices))
        self.assertEqual(4, len(set(gpu_vertices)))
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "rotation-aware transformed primitive geometry.*Float32 quantization",
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

    def test_repeat_validation_checks_every_phase_sensitive_rotated_instance(
        self,
    ) -> None:
        with patch.object(
            scene_pipeline,
            "_validate_primitive_world_bounds",
            wraps=scene_pipeline._validate_primitive_world_bounds,
        ) as bounds_validator:
            scene_pipeline.validate(self.master, self.scene, self.cameras)
        repeat_calls = [
            call
            for call in bounds_validator.call_args_list
            if call.args[3] == "scene.structures.rack-row-context"
        ]
        self.assertEqual(6, len(repeat_calls))
        self.assertEqual(
            [[0.0, 0.0, 58.0 * index] for index in range(6)],
            [call.args[2] for call in repeat_calls],
        )

        scene = deepcopy(self.scene)
        structure = next(
            structure for structure in scene["structures"] if "repeat" in structure
        )
        width = 2**-13
        step = [-3 * width, -3 * width, -0.9 * width]
        structure["repeat"] = {"count": 6, "step": step}
        primitive = structure["primitives"][0]
        primitive["at"] = [
            1024.012939453125,
            1024.0150146484375,
            1024.0165771484376,
        ]
        primitive["size"] = [1.01 * width, 8 * width, 8 * width]
        primitive["rotate"] = [-60, -30, 0]

        matrix = scene_pipeline._primitive_rotation_matrix(primitive["rotate"])
        local_vertices = scene_pipeline._primitive_local_float32_vertices(primitive)
        final_round_only_ranks = []
        gpu_ranks = []
        valid_instances = []
        for repeat_index in range(structure["repeat"]["count"]):
            offset = [value * repeat_index for value in step]
            center = tuple(
                float(primitive["at"][axis]) + offset[axis] for axis in range(3)
            )
            final_round_only_vertices = tuple(
                tuple(
                    scene_pipeline._webgl_float32(
                        center[world_axis]
                        + sum(
                            matrix[world_axis][local_axis] * vertex[local_axis]
                            for local_axis in range(3)
                        )
                    )
                    for world_axis in range(3)
                )
                for vertex in local_vertices
            )
            final_round_only_ranks.append(
                scene_pipeline._float32_affine_rank(final_round_only_vertices)
            )
            gpu_ranks.append(
                scene_pipeline._float32_affine_rank(
                    scene_pipeline._rotated_primitive_gpu_float32_vertices(
                        primitive, center
                    )
                )
            )
            try:
                scene_pipeline._validate_primitive_world_bounds(
                    [primitive], [0, 0, 0], offset, "phase-sensitive-repeat"
                )
            except scene_pipeline.ManifestError as error:
                self.assertRegex(
                    str(error),
                    "rotation-aware transformed primitive geometry.*"
                    "Float32 quantization",
                )
                valid_instances.append(False)
            else:
                valid_instances.append(True)
        self.assertEqual([3, 2, 2, 2, 3, 3], final_round_only_ranks)
        self.assertEqual([2, 2, 2, 2, 2, 2], gpu_ranks)
        self.assertEqual([False] * 6, valid_instances)

        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "rotation-aware transformed primitive geometry.*Float32 quantization",
        ):
            scene_pipeline.validate(self.master, scene, self.cameras)

    @unittest.skipUnless(shutil.which("node"), "Node.js is required")
    def test_bundled_three_confirms_camera_anchor_visibility_evidence(self) -> None:
        campus = next(
            camera
            for camera in self.cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        blank = deepcopy(campus)
        blank["position"] = [1_000_000, 1_000_000, 1_000_000]
        points = [
            list(point)
            for _, point, _, _ in scene_pipeline._camera_focus_points(
                self.scene, campus
            )
        ]
        payload = json.dumps(
            {
                "points": points,
                "up": self.scene["world"]["camera_up"],
                "fogFar": self.scene["world"]["fog"]["far"],
                "fov": scene_pipeline.THREE_CAMERA_VERTICAL_FOV_DEGREES,
                "near": scene_pipeline.THREE_CAMERA_NEAR,
                "far": scene_pipeline.THREE_CAMERA_FAR,
                "aspects": [16 / 9, 738 / 582],
                "cameras": [campus, blank],
            }
        )
        script = """
import * as THREE from './diagram/vendor/three/three.module.js';
const data = JSON.parse(process.argv[2]);
const counts = data.cameras.map(spec => data.aspects.map(aspect => {
    const camera = new THREE.PerspectiveCamera(
      data.fov,
      aspect,
      data.near,
      data.far
    );
    camera.position.set(...spec.position);
    camera.up.set(...data.up).normalize();
    camera.lookAt(...spec.target);
    camera.updateMatrixWorld(true);
    const projectionView = new THREE.Matrix4().multiplyMatrices(
      camera.projectionMatrix,
      camera.matrixWorldInverse
    );
    const frustum = new THREE.Frustum().setFromProjectionMatrix(projectionView);
    return data.points.filter(raw => {
      const point = new THREE.Vector3(...raw);
      const viewPoint = point.clone().applyMatrix4(camera.matrixWorldInverse);
      return frustum.containsPoint(point) && -viewPoint.z < data.fogFar;
    }).length;
  }));
console.log(JSON.stringify(counts));
"""
        result = subprocess.run(
            [shutil.which("node") or "node", "--input-type=module", "-", payload],
            cwd=scene_pipeline.ROOT,
            input=script,
            text=True,
            capture_output=True,
            check=True,
        )
        self.assertEqual([[514, 514], [0, 0]], json.loads(result.stdout))
        self.assertEqual(
            514,
            scene_pipeline._camera_focus_visibility(self.scene, campus)[
                "viewport_coverage"
            ][0]["visible_point_count"],
        )
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "authored position-target distance.*OrbitControls range",
        ):
            scene_pipeline._camera_focus_visibility(self.scene, blank)

    @unittest.skipUnless(shutil.which("node"), "Node.js is required")
    def test_bundled_three_confirms_float32_geometry_collapse_evidence(self) -> None:
        script = """
import * as THREE from './diagram/vendor/three/three.module.js';
const scale = 2 ** 30;
const edgeBase = 2 ** 25 + 400;
const radius = Number(process.argv[2]);
const curve = new THREE.CurvePath();
curve.add(new THREE.LineCurve3(
  new THREE.Vector3(edgeBase, edgeBase, edgeBase),
  new THREE.Vector3(edgeBase + 80, edgeBase + 80, edgeBase + 80)
));
const tube = new THREE.TubeGeometry(curve, 20, radius, 8, false);
const tubePositions = tube.getAttribute('position');
const tubeIndices = tube.getIndex();
const a = new THREE.Vector3();
const b = new THREE.Vector3();
const c = new THREE.Vector3();
const ab = new THREE.Vector3();
const ac = new THREE.Vector3();
let tubeMaxTriangleArea = 0;
let tubeNonzeroTriangles = 0;
for (let index = 0; index < tubeIndices.count; index += 3) {
  a.fromBufferAttribute(tubePositions, tubeIndices.getX(index));
  b.fromBufferAttribute(tubePositions, tubeIndices.getX(index + 1));
  c.fromBufferAttribute(tubePositions, tubeIndices.getX(index + 2));
  const area = ab.subVectors(b, a).cross(ac.subVectors(c, a)).length() / 2;
  tubeMaxTriangleArea = Math.max(tubeMaxTriangleArea, area);
  if (area > 0) tubeNonzeroTriangles += 1;
}

const box = new THREE.BoxGeometry(1, 10, 256);
const boxTransform = new THREE.Matrix4().compose(
  new THREE.Vector3(0, 0, scale),
  new THREE.Quaternion().setFromEuler(new THREE.Euler(0, Math.PI / 2, 0)),
  new THREE.Vector3(1, 1, 1)
);
box.applyMatrix4(boxTransform);
const boxPositions = box.getAttribute('position');
const boxIndices = box.getIndex();
let boxSignedVolumeTimesSix = 0;
for (let index = 0; index < boxIndices.count; index += 3) {
  a.fromBufferAttribute(boxPositions, boxIndices.getX(index));
  b.fromBufferAttribute(boxPositions, boxIndices.getX(index + 1));
  c.fromBufferAttribute(boxPositions, boxIndices.getX(index + 2));
  boxSignedVolumeTimesSix += a.dot(ab.crossVectors(b, c));
}

const gpuBox = new THREE.BoxGeometry(
  0.0018179010284972768,
  0.00013933693226819645,
  0.004424568176824122
);
const gpuMesh = new THREE.Mesh(gpuBox);
gpuMesh.position.set(
  1024.1536073483026,
  1024.8170099900176,
  1025.117256280513
);
gpuMesh.rotation.set(...[
  113.38577503924103,
  93.41804158058227,
  -70.68951634408539
].map(THREE.MathUtils.degToRad));
gpuMesh.updateMatrix();
const gpuMatrix = new Float32Array(gpuMesh.matrix.elements);
const gpuPositions = gpuBox.getAttribute('position');
const gpuBoxVertices = Array.from({ length: gpuPositions.count }, (_, index) => {
  const local = [
    gpuPositions.getX(index),
    gpuPositions.getY(index),
    gpuPositions.getZ(index)
  ];
  return [0, 1, 2].map(worldAxis => {
    let value = gpuMatrix[12 + worldAxis];
    for (let localAxis = 0; localAxis < 3; localAxis += 1) {
      const product = Math.fround(
        gpuMatrix[localAxis * 4 + worldAxis] * local[localAxis]
      );
      value = Math.fround(value + product);
    }
    return value;
  });
});
const gpuBoxUniqueVertices = [...new Map(
  gpuBoxVertices.map(vertex => [JSON.stringify(vertex), vertex])
).values()];
console.log(JSON.stringify({
  tube_max_triangle_area: tubeMaxTriangleArea,
  tube_nonzero_triangles: tubeNonzeroTriangles,
  tube_triangle_count: tubeIndices.count / 3,
  tube_ring_unique_counts: Array.from({ length: 21 }, (_, ring) => new Set(
    Array.from({ length: 9 }, (_, radial) => {
      const index = ring * 9 + radial;
      return `${tubePositions.getX(index)},${tubePositions.getY(index)},${tubePositions.getZ(index)}`;
    })
  ).size),
  box_unique_z: new Set(
    Array.from({ length: boxPositions.count }, (_, index) => boxPositions.getZ(index))
  ).size,
  box_volume: Math.abs(boxSignedVolumeTimesSix) / 6,
  gpu_box_vertices: gpuBoxUniqueVertices
}));
"""
        result = subprocess.run(
            [
                shutil.which("node") or "node",
                "--input-type=module",
                "-",
                str(scene_pipeline.EDGE_TUBE_RADIUS),
            ],
            cwd=scene_pipeline.ROOT,
            input=script,
            text=True,
            capture_output=True,
            check=True,
        )
        evidence = json.loads(result.stdout)
        gpu_box_vertices = {
            tuple(vertex) for vertex in evidence.pop("gpu_box_vertices")
        }
        gpu_primitive = {
            "shape": "box",
            "at": [
                1024.1536073483026,
                1024.8170099900176,
                1025.117256280513,
            ],
            "size": [
                0.0018179010284972768,
                0.00013933693226819645,
                0.004424568176824122,
            ],
            "rotate": [
                113.38577503924103,
                93.41804158058227,
                -70.68951634408539,
            ],
        }
        expected_gpu_vertices = set(
            scene_pipeline._rotated_primitive_gpu_float32_vertices(
                gpu_primitive, tuple(gpu_primitive["at"])
            )
        )
        self.assertEqual(expected_gpu_vertices, gpu_box_vertices)
        self.assertEqual(4, len(gpu_box_vertices))
        self.assertEqual(
            2,
            scene_pipeline._float32_affine_rank(tuple(gpu_box_vertices)),
        )
        self.assertEqual(
            {
                "tube_max_triangle_area": 0,
                "tube_nonzero_triangles": 0,
                "tube_triangle_count": 320,
                "tube_ring_unique_counts": [1] * 21,
                "box_unique_z": 1,
                "box_volume": 0,
            },
            evidence,
        )

    def test_every_edge_segment_survives_float32_quantization(self) -> None:
        authored_scale = 2**30
        self.assertNotEqual(float(authored_scale), float(authored_scale + 1))
        self.assertEqual(
            scene_pipeline._webgl_float32(authored_scale),
            scene_pipeline._webgl_float32(authored_scale + 1),
        )

        segment_probes = 0
        for edge_id, edge in self.scene["edges"].items():
            for segment_index in range(len(edge["points"]) - 1):
                scene = deepcopy(self.scene)
                points = scene["edges"][edge_id]["points"]
                points[segment_index] = [authored_scale, 0, 0]
                points[segment_index + 1] = [authored_scale + 1, 0, 0]
                segment_probes += 1
                with (
                    self.subTest(edge=edge_id, segment=segment_index),
                    self.assertRaisesRegex(
                        scene_pipeline.ManifestError, "Float32 quantization"
                    ),
                ):
                    scene_pipeline.validate(self.master, scene, self.cameras)
        self.assertEqual(59, segment_probes)

    def test_float32_representability_reaches_every_scene_gateway(self) -> None:
        cases = []

        scene = deepcopy(self.scene)
        scene["structures"][0]["primitives"][0]["size"][0] = 1e-300
        cases.append(("box dimension", scene, "positive.*Float32 quantization"))

        scene = deepcopy(self.scene)
        scene["nodes"]["generator"]["primitives"][0]["radius"] = 1e-300
        cases.append(("cylinder radius", scene, "positive.*Float32 quantization"))

        scene = deepcopy(self.scene)
        scene["world"]["ground"]["size"][0] = 1e-300
        cases.append(("ground dimension", scene, "positive.*Float32 quantization"))

        scene = deepcopy(self.scene)
        scene["world"]["fog"] = {"near": 1e-300, "far": 2e-300}
        cases.append(("fog interval", scene, "interval.*Float32 quantization"))

        for camera_up in ([0, 0, 0], [1e-300, 0, 0]):
            scene = deepcopy(self.scene)
            scene["world"]["camera_up"] = camera_up
            cases.append(("camera up", scene, "camera_up.*Float32 quantization"))

        scene = deepcopy(self.scene)
        repeated = next(
            structure for structure in scene["structures"] if "repeat" in structure
        )
        repeated["repeat"] = {"count": 2, "step": [1e-300, 0, 0]}
        cases.append(
            ("repeat offset", scene, "repeat-derived offsets.*Float32 quantization")
        )

        scene = deepcopy(self.scene)
        repeated = next(
            structure for structure in scene["structures"] if "repeat" in structure
        )
        repeated["repeat"] = {"count": 2, "step": [1, 0, 0]}
        repeated["primitives"][0]["at"][0] = 2**30
        cases.append(
            (
                "repeat world position",
                scene,
                "repeat-derived primitive positions.*Float32 quantization",
            )
        )

        scene = deepcopy(self.scene)
        scene["structures"][0]["primitives"][0]["at"][0] = 2**30
        scene["structures"][0]["primitives"][0]["size"][0] = 1
        cases.append(
            (
                "authored world extent",
                scene,
                "authored center and extent.*Float32 quantization",
            )
        )

        scene = deepcopy(self.scene)
        primitive = scene["structures"][0]["primitives"][0]
        primitive["at"] = [0, 0, 2**30]
        primitive["size"] = [1, 10, 256]
        primitive["rotate"] = [0, 90, 0]
        cases.append(
            (
                "rotated primitive volume",
                scene,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        scene = deepcopy(self.scene)
        primitive = scene["structures"][0]["primitives"][0]
        primitive["at"] = [
            1024.1536073483026,
            1024.8170099900176,
            1025.117256280513,
        ]
        primitive["size"] = [
            0.0018179010284972768,
            0.00013933693226819645,
            0.004424568176824122,
        ]
        primitive["rotate"] = [
            113.38577503924103,
            93.41804158058227,
            -70.68951634408539,
        ]
        cases.append(
            (
                "GPU Float32 matrix primitive volume",
                scene,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        scene = deepcopy(self.scene)
        repeated = next(
            structure for structure in scene["structures"] if "repeat" in structure
        )
        width = 2**-13
        repeated["repeat"] = {
            "count": 6,
            "step": [-3 * width, -3 * width, -0.9 * width],
        }
        primitive = repeated["primitives"][0]
        primitive["at"] = [
            1024.012939453125,
            1024.0150146484375,
            1024.0165771484376,
        ]
        primitive["size"] = [1.01 * width, 8 * width, 8 * width]
        primitive["rotate"] = [-60, -30, 0]
        cases.append(
            (
                "phase-sensitive repeated primitive volume",
                scene,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        scene = deepcopy(self.scene)
        base = 2**25 + 400
        scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [base, base, base],
            [base + 80, base + 80, base + 80],
        ]
        cases.append(
            (
                "edge tube cross-section",
                scene,
                "TubeGeometry cross-section rounding-error bound.*Float32 quantization",
            )
        )

        scene = deepcopy(self.scene)
        scene["edges"]["btm_fuel_to_shaft"]["points"] = [[0, 0, 0], [0, 0, 0]]
        cases.append(("total edge path", scene, "total path.*Float32 quantization"))

        scene = deepcopy(self.scene)
        scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [0, 0, 0],
            [1e-300, 0, 0],
            [1, 0, 0],
        ]
        cases.append(("edge segment", scene, "path segment.*Float32 quantization"))

        gateways = (
            scene_pipeline.validate_webgl_numeric_domain,
            lambda candidate: scene_pipeline.validate(
                self.master, candidate, self.cameras
            ),
            lambda candidate: scene_pipeline.build_payload(
                self.master, candidate, self.cameras
            ),
        )
        for label, invalid_scene, message in cases:
            for gateway in gateways:
                with (
                    self.subTest(label=label, gateway=gateway),
                    self.assertRaisesRegex(scene_pipeline.ManifestError, message),
                ):
                    gateway(invalid_scene)

    def test_geometry_rejects_boolean_and_nonfinite_numeric_mutations(self) -> None:
        scene_paths = (
            ("camera up", ("world", "camera_up", 0)),
            ("fog near", ("world", "fog", "near")),
            ("fog far", ("world", "fog", "far")),
            ("ground size", ("world", "ground", "size", 0)),
            ("ground coordinate", ("world", "ground", "at", 0)),
            (
                "structure coordinate",
                ("structures", 0, "primitives", 0, "at", 0),
            ),
            ("box size", ("structures", 0, "primitives", 0, "size", 0)),
            ("primitive opacity", ("structures", 0, "primitives", 0, "opacity")),
            ("repeat count", ("structures", 3, "repeat", "count")),
            ("repeat step", ("structures", 3, "repeat", "step", 0)),
            ("node coordinate", ("nodes", "gas_turbine", "at", 0)),
            ("label coordinate", ("nodes", "gas_turbine", "label_at", 0)),
            (
                "cylinder radius",
                ("nodes", "generator", "primitives", 0, "radius"),
            ),
            (
                "cylinder height",
                ("nodes", "generator", "primitives", 0, "height"),
            ),
            (
                "primitive rotation",
                ("nodes", "generator", "primitives", 0, "rotate", 0),
            ),
            ("edge coordinate", ("edges", "btm_fuel_to_shaft", "points", 0, 0)),
        )
        camera_paths = (
            ("camera view box", ("cameras", 0, "viewBox", 0)),
            ("camera well", ("cameras", 0, "well", 0)),
            ("map view", ("cameras", 0, "map_view", 0)),
            ("camera position", ("cameras", 1, "position", 0)),
            ("camera target", ("cameras", 1, "target", 0)),
            (
                "camera label offset",
                ("cameras", 1, "label_offsets", "utility_source_138", 0),
            ),
        )

        def replace(container, path, value) -> None:
            target = container
            for key in path[:-1]:
                target = target[key]
            target[path[-1]] = value

        invalid_values = (True, math.nan, math.inf, -math.inf)
        for label, path in scene_paths:
            for invalid in invalid_values:
                scene = deepcopy(self.scene)
                replace(scene, path, invalid)
                with (
                    self.subTest(field=label, invalid=invalid),
                    self.assertRaises(scene_pipeline.ManifestError),
                ):
                    scene_pipeline.validate(self.master, scene, self.cameras)
        for label, path in camera_paths:
            for invalid in invalid_values:
                cameras = deepcopy(self.cameras)
                replace(cameras, path, invalid)
                with (
                    self.subTest(field=label, invalid=invalid),
                    self.assertRaises(scene_pipeline.ManifestError),
                ):
                    scene_pipeline.validate(self.master, self.scene, cameras)

    def test_physical_geometry_dimensions_are_positive_exhaustively(self) -> None:
        primitives = []
        for structure_index, structure in enumerate(self.scene["structures"]):
            primitives.extend(
                (
                    ("structures", structure_index, "primitives", primitive_index),
                    primitive,
                )
                for primitive_index, primitive in enumerate(structure["primitives"])
            )
        for node_id, node in self.scene["nodes"].items():
            primitives.extend(
                (
                    ("nodes", node_id, "primitives", primitive_index),
                    primitive,
                )
                for primitive_index, primitive in enumerate(node["primitives"])
            )

        def replace(path, field, index, value) -> dict:
            scene = deepcopy(self.scene)
            target = scene
            for key in path:
                target = target[key]
            if index is None:
                target[field] = value
            else:
                target[field][index] = value
            return scene

        box_dimension_probes = 0
        cylinder_dimension_probes = 0
        for path, primitive in primitives:
            if primitive["shape"] == "box":
                for dimension_index in range(3):
                    for invalid in (0, -1):
                        scene = replace(path, "size", dimension_index, invalid)
                        box_dimension_probes += 1
                        with (
                            self.subTest(
                                path=path,
                                field="size",
                                index=dimension_index,
                                invalid=invalid,
                            ),
                            self.assertRaisesRegex(
                                scene_pipeline.ManifestError,
                                "expected a positive number",
                            ),
                        ):
                            scene_pipeline.validate(self.master, scene, self.cameras)
            else:
                for field in ("radius", "height"):
                    for invalid in (0, -1):
                        scene = replace(path, field, None, invalid)
                        cylinder_dimension_probes += 1
                        with (
                            self.subTest(path=path, field=field, invalid=invalid),
                            self.assertRaisesRegex(
                                scene_pipeline.ManifestError,
                                "expected a positive number",
                            ),
                        ):
                            scene_pipeline.validate(self.master, scene, self.cameras)

        ground_extent_probes = 0
        for extent_index in range(2):
            for invalid in (0, -1):
                scene = deepcopy(self.scene)
                scene["world"]["ground"]["size"][extent_index] = invalid
                ground_extent_probes += 1
                with (
                    self.subTest(
                        field="ground.size",
                        index=extent_index,
                        invalid=invalid,
                    ),
                    self.assertRaisesRegex(
                        scene_pipeline.ManifestError, "expected a positive number"
                    ),
                ):
                    scene_pipeline.validate(self.master, scene, self.cameras)

        self.assertEqual(222, box_dimension_probes)
        self.assertEqual(72, cylinder_dimension_probes)
        self.assertEqual(4, ground_extent_probes)

    def test_fog_domain_requires_nonnegative_near_and_strictly_greater_far(
        self,
    ) -> None:
        invalid_intervals = (
            (-1, 3600, "near"),
            (1900, -1, "far"),
            (1900, 1900, "far"),
            (1901, 1900, "far"),
        )
        for near, far, invalid_field in invalid_intervals:
            scene = deepcopy(self.scene)
            scene["world"]["fog"] = {"near": near, "far": far}
            with (
                self.subTest(near=near, far=far),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError,
                    rf"fog\.{invalid_field}",
                ),
            ):
                scene_pipeline.validate(self.master, scene, self.cameras)

        scene = deepcopy(self.scene)
        scene["world"]["fog"] = {"near": 0, "far": 1}
        scene_pipeline.validate_webgl_numeric_domain(scene)

    def test_primitive_opacity_is_closed_unit_interval_exhaustively(self) -> None:
        opacity_paths = []
        for structure_index, structure in enumerate(self.scene["structures"]):
            opacity_paths.extend(
                ("structures", structure_index, "primitives", primitive_index)
                for primitive_index, primitive in enumerate(structure["primitives"])
                if "opacity" in primitive
            )
        for node_id, node in self.scene["nodes"].items():
            opacity_paths.extend(
                ("nodes", node_id, "primitives", primitive_index)
                for primitive_index, primitive in enumerate(node["primitives"])
                if "opacity" in primitive
            )
        self.assertEqual(41, len(opacity_paths))

        invalid_values = (-0.01, 1.01, True, False, math.nan, math.inf, -math.inf)
        rejected_probes = 0
        for path in opacity_paths:
            for invalid in invalid_values:
                scene = deepcopy(self.scene)
                target = scene
                for key in path:
                    target = target[key]
                target["opacity"] = invalid
                rejected_probes += 1
                with (
                    self.subTest(path=path, invalid=invalid),
                    self.assertRaises(scene_pipeline.ManifestError),
                ):
                    scene_pipeline.validate(self.master, scene, self.cameras)
        self.assertEqual(287, rejected_probes)

        accepted_boundary_probes = 0
        for path in opacity_paths:
            for boundary in (0, 1):
                scene = deepcopy(self.scene)
                target = scene
                for key in path:
                    target = target[key]
                target["opacity"] = boundary
                scene_pipeline.validate(self.master, scene, self.cameras)
                accepted_boundary_probes += 1
        self.assertEqual(82, accepted_boundary_probes)

    def test_canonical_payload_wraps_serialization_failures(self) -> None:
        for value in (math.nan, math.inf, -math.inf, object()):
            with (
                self.subTest(value=repr(value)),
                self.assertRaisesRegex(
                    scene_pipeline.ManifestError, "payload serialization failed"
                ),
            ):
                scene_pipeline.canonical_payload({"value": value})

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
