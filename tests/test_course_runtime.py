from __future__ import annotations

import copy
import json
import math
import unittest
from unittest.mock import patch

from gigawatt import course_runtime, shots, validate
from gigawatt import layout as layout_pipeline
from gigawatt import scene as scene_pipeline


def walk_keys(value: object):
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            yield from walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from walk_keys(nested)


class CourseRuntimeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        (
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
            cls.ledgers,
            cls.visuals,
        ) = course_runtime.load_inputs()
        cls.registry = course_runtime.compile_registry(
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
            cls.ledgers,
            cls.visuals,
            source_digest="test-digest",
        )

    def test_registry_covers_the_canonical_course_exactly(self) -> None:
        manifest_segments = [
            segment for act in self.course["acts"] for segment in act["segments"]
        ]
        runtime_segments = self.registry["segments"]
        self.assertEqual(7, self.registry["act_count"])
        self.assertEqual(26, self.registry["segment_count"])
        self.assertEqual(
            [segment["id"] for segment in manifest_segments],
            [segment["segment_id"] for segment in runtime_segments],
        )
        self.assertEqual(
            list(range(1, 27)), [segment["sequence"] for segment in runtime_segments]
        )
        self.assertEqual(
            {"derived": 21, "existing": 5},
            {
                status: sum(segment["status"] == status for segment in runtime_segments)
                for status in ("derived", "existing")
            },
        )
        self.assertEqual(
            sum(
                segment["evidence"]["readiness"] == "evidence_ready"
                for segment in manifest_segments
            ),
            self.registry["evidence_ready_count"],
        )
        self.assertEqual(
            validate.PROMOTION_GUARDS,
            set(course_runtime.PROMOTION_GUARD_WARNINGS),
        )
        self.assertTrue(
            all(
                segment["promotion_guard_warnings"]
                for segment in self.registry["segments"]
            )
        )

    def test_course_runtime_rejects_blank_three_dimensional_anchor(self) -> None:
        cameras = copy.deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        campus["position"] = [1_000_000, 1_000_000, 1_000_000]
        with self.assertRaisesRegex(
            scene_pipeline.ManifestError,
            "authored position-target distance.*OrbitControls range",
        ):
            course_runtime.compile_registry(
                self.course,
                cameras,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.visuals,
                source_digest="blank-camera-anchor",
            )

    def test_compile_and_build_preflight_coordinated_unknown_promotion(self) -> None:
        course = copy.deepcopy(self.course)
        ledgers = copy.deepcopy(self.ledgers)
        gpu = ledgers["abilene"]["facts"]["installed_gpu_count"]
        gpu["value"] = 1
        gpu["posture"] = "confirmed"
        gpu["lifecycle"] = "operating"
        changed_claims = 0
        for act in course["acts"]:
            for segment in act["segments"]:
                for claim in segment["evidence"]["claims"]:
                    if "abilene:installed_gpu_count" in claim["fact_refs"]:
                        claim["assertion"] = "confirmed"
                        changed_claims += 1

        with (
            patch.object(course_runtime, "_compiled_visuals") as compile_visuals,
            self.assertRaisesRegex(validate.ValidationError, "immutable fact"),
        ):
            course_runtime.compile_registry(
                course,
                self.cameras,
                self.master,
                self.layout,
                self.scene,
                ledgers,
                self.visuals,
                source_digest="rejected-promotion",
            )
        compile_visuals.assert_not_called()

        loaded = (
            course,
            self.cameras,
            self.master,
            self.layout,
            self.scene,
            ledgers,
            self.visuals,
        )
        with (
            patch.object(course_runtime, "load_inputs", return_value=loaded),
            patch.object(course_runtime, "compile_registry") as compiler,
            patch.object(course_runtime, "_player_template") as player_template,
            patch.object(course_runtime, "build_instructor_packet") as packet_builder,
            self.assertRaisesRegex(validate.ValidationError, "immutable fact"),
        ):
            course_runtime.build_artifacts()

        self.assertEqual(3, changed_claims)
        compiler.assert_not_called()
        player_template.assert_not_called()
        packet_builder.assert_not_called()

    def test_compile_registry_preflights_authoritative_scene_contract(self) -> None:
        cases = []

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["world"]["fog"]["far"] = invalid_scene["world"]["fog"]["near"]
        cases.append(("fog", invalid_scene, self.cameras, r"fog\.far"))

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["structures"][0]["primitives"][0]["size"][0] = 0
        cases.append(("structure dimension", invalid_scene, self.cameras, "positive"))

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["structures"][0]["primitives"][0]["size"][0] = 1e39
        cases.append(
            (
                "Float32 structure dimension",
                invalid_scene,
                self.cameras,
                "WebGL Float32-safe bound",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["structures"][0]["primitives"][0]["size"][0] = 1e-300
        cases.append(
            (
                "Float32-collapsed structure dimension",
                invalid_scene,
                self.cameras,
                "positive dimension.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["world"]["fog"] = {"near": 1e-300, "far": 2e-300}
        cases.append(
            (
                "Float32-collapsed fog interval",
                invalid_scene,
                self.cameras,
                "interval.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["world"]["camera_up"] = [1e-300, 0, 0]
        cases.append(
            (
                "Float32-collapsed camera up",
                invalid_scene,
                self.cameras,
                "camera_up.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [2**30, 0, 0],
            [2**30 + 1, 0, 0],
        ]
        cases.append(
            (
                "Float32-collapsed edge path",
                invalid_scene,
                self.cameras,
                "total path.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        repeated_structure = next(
            structure
            for structure in invalid_scene["structures"]
            if "repeat" in structure
        )
        repeated_structure["repeat"] = {"count": 2, "step": [1e-300, 0, 0]}
        cases.append(
            (
                "Float32-collapsed repeat offset",
                invalid_scene,
                self.cameras,
                "repeat-derived offsets.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        primitive = invalid_scene["structures"][0]["primitives"][0]
        primitive["at"][0] = 2**30
        primitive["size"][0] = 1
        cases.append(
            (
                "Float32-collapsed authored extent",
                invalid_scene,
                self.cameras,
                "authored center and extent.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        primitive = invalid_scene["structures"][0]["primitives"][0]
        primitive["at"] = [0, 0, 2**30]
        primitive["size"] = [1, 10, 256]
        primitive["rotate"] = [0, 90, 0]
        cases.append(
            (
                "Float32-collapsed rotated primitive volume",
                invalid_scene,
                self.cameras,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        primitive = invalid_scene["structures"][0]["primitives"][0]
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
                "Float32 GPU-matrix collapsed primitive volume",
                invalid_scene,
                self.cameras,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        repeated_structure = next(
            structure
            for structure in invalid_scene["structures"]
            if "repeat" in structure
        )
        width = 2**-13
        repeated_structure["repeat"] = {
            "count": 6,
            "step": [-3 * width, -3 * width, -0.9 * width],
        }
        primitive = repeated_structure["primitives"][0]
        primitive["at"] = [
            1024.012939453125,
            1024.0150146484375,
            1024.0165771484376,
        ]
        primitive["size"] = [1.01 * width, 8 * width, 8 * width]
        primitive["rotate"] = [-60, -30, 0]
        cases.append(
            (
                "Float32-collapsed repeated rotated primitive volume",
                invalid_scene,
                self.cameras,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        base = 2**25 + 400
        invalid_scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [base, base, base],
            [base + 80, base + 80, base + 80],
        ]
        cases.append(
            (
                "Float32-collapsed edge tube cross-section",
                invalid_scene,
                self.cameras,
                "TubeGeometry cross-section rounding-error bound.*Float32 quantization",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["nodes"]["gas_turbine"]["at"][0] = 1e39
        cases.append(
            (
                "Float32 node position",
                invalid_scene,
                self.cameras,
                "WebGL Float32-safe bound",
            )
        )

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["nodes"]["generator"]["primitives"][0]["radius"] = 0
        cases.append(("node radius", invalid_scene, self.cameras, "positive"))

        invalid_cameras = copy.deepcopy(self.cameras)
        invalid_cameras["cameras"][0]["viewBox"][2] = 0
        cases.append(("viewBox", self.scene, invalid_cameras, r"viewBox\.width"))

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [index, 0, 0] for index in range(scene_pipeline.MAX_EDGE_POINTS + 1)
        ]
        cases.append(("edge points", invalid_scene, self.cameras, "edge point count"))

        invalid_scene = copy.deepcopy(self.scene)
        invalid_scene["structures"] = []
        cases.append(
            ("structural context", invalid_scene, self.cameras, "context layers")
        )

        invalid_cameras = copy.deepcopy(self.cameras)
        invalid_cameras["cameras"][1]["label_offsets"] = False
        cases.append(
            ("label offsets", self.scene, invalid_cameras, "must be a mapping")
        )

        invalid_scene = copy.deepcopy(self.scene)
        repeated_structure = next(
            structure
            for structure in invalid_scene["structures"]
            if "repeat" in structure
        )
        repeated_structure["repeat"]["count"] = 3
        repeated_structure["repeat"]["step"] = [
            float.fromhex("0x1.fffffffffffffp+1023"),
            0,
            0,
        ]
        cases.append(
            (
                "repeat-derived coordinate",
                invalid_scene,
                self.cameras,
                "repeat-derived offset",
            )
        )

        for label, scene, cameras, message in cases:
            with (
                self.subTest(label=label),
                patch.object(course_runtime, "_validate_course_inputs") as course_check,
                patch.object(course_runtime, "_compiled_visuals") as visual_compiler,
                self.assertRaisesRegex(scene_pipeline.ManifestError, message),
            ):
                course_runtime.compile_registry(
                    self.course,
                    cameras,
                    self.master,
                    self.layout,
                    scene,
                    self.ledgers,
                    self.visuals,
                    source_digest="invalid-scene",
                )
            course_check.assert_not_called()
            visual_compiler.assert_not_called()

    def test_build_artifacts_inherits_scene_resource_preflight(self) -> None:
        oversized_edge_scene = copy.deepcopy(self.scene)
        oversized_edge_scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [index, 0, 0] for index in range(10_000)
        ]

        repeat_overflow_scene = copy.deepcopy(self.scene)
        repeated_structure = next(
            structure
            for structure in repeat_overflow_scene["structures"]
            if "repeat" in structure
        )
        repeated_structure["repeat"]["count"] = 3
        repeated_structure["repeat"]["step"] = [
            float.fromhex("0x1.fffffffffffffp+1023"),
            0,
            0,
        ]

        float32_overflow_scene = copy.deepcopy(self.scene)
        float32_overflow_scene["structures"][0]["primitives"][0]["size"][0] = 1e39

        float32_position_scene = copy.deepcopy(self.scene)
        float32_position_scene["nodes"]["gas_turbine"]["at"][0] = 1e39

        float32_underflow_scene = copy.deepcopy(self.scene)
        float32_underflow_scene["structures"][0]["primitives"][0]["size"][0] = 1e-300

        float32_fog_scene = copy.deepcopy(self.scene)
        float32_fog_scene["world"]["fog"] = {"near": 1e-300, "far": 2e-300}

        float32_edge_scene = copy.deepcopy(self.scene)
        float32_edge_scene["edges"]["btm_fuel_to_shaft"]["points"] = [
            [2**30, 0, 0],
            [2**30 + 1, 0, 0],
        ]

        cases = (
            ("edge point budget", oversized_edge_scene, "edge point count"),
            (
                "repeat-derived coordinate",
                repeat_overflow_scene,
                "repeat-derived offset",
            ),
            (
                "Float32 structure dimension",
                float32_overflow_scene,
                "WebGL Float32-safe bound",
            ),
            (
                "Float32 node position",
                float32_position_scene,
                "WebGL Float32-safe bound",
            ),
            (
                "Float32-collapsed structure dimension",
                float32_underflow_scene,
                "positive dimension.*Float32 quantization",
            ),
            (
                "Float32-collapsed fog interval",
                float32_fog_scene,
                "interval.*Float32 quantization",
            ),
            (
                "Float32-collapsed edge path",
                float32_edge_scene,
                "total path.*Float32 quantization",
            ),
        )
        for label, invalid_scene, message in cases:
            loaded = (
                self.course,
                self.cameras,
                self.master,
                self.layout,
                invalid_scene,
                self.ledgers,
                self.visuals,
            )
            with (
                self.subTest(label=label),
                patch.object(course_runtime, "load_inputs", return_value=loaded),
                patch.object(course_runtime, "_player_template") as player_template,
                patch.object(
                    course_runtime, "build_instructor_packet"
                ) as packet_builder,
                self.assertRaisesRegex(scene_pipeline.ManifestError, message),
            ):
                course_runtime.build_artifacts()
            player_template.assert_not_called()
            packet_builder.assert_not_called()

    def test_compile_and_build_preflight_coordinated_ledger_context_rewrite(
        self,
    ) -> None:
        ledgers = copy.deepcopy(self.ledgers)
        for ledger in ledgers.values():
            for field, value in ledger["subject"].items():
                ledger["subject"][field] = f"{value} weakened"
            for field, value in ledger["evidence_boundary"].items():
                ledger["evidence_boundary"][field] = f"{value} weakened"

        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable ledger context contract requires exact",
        ):
            validate.validate_course_inputs(
                self.course,
                self.master,
                ledgers,
                self.cameras,
            )

        with (
            patch.object(course_runtime, "_compiled_visuals") as compile_visuals,
            self.assertRaisesRegex(
                validate.ValidationError,
                "immutable ledger context contract requires exact",
            ),
        ):
            course_runtime.compile_registry(
                self.course,
                self.cameras,
                self.master,
                self.layout,
                self.scene,
                ledgers,
                self.visuals,
                source_digest="rejected-ledger-context",
            )
        compile_visuals.assert_not_called()

        loaded = (
            self.course,
            self.cameras,
            self.master,
            self.layout,
            self.scene,
            ledgers,
            self.visuals,
        )
        with (
            patch.object(course_runtime, "load_inputs", return_value=loaded),
            patch.object(course_runtime, "compile_registry") as compiler,
            patch.object(course_runtime, "_player_template") as player_template,
            patch.object(course_runtime, "build_instructor_packet") as packet_builder,
            self.assertRaisesRegex(
                validate.ValidationError,
                "immutable ledger context contract requires exact",
            ),
        ):
            course_runtime.build_artifacts()

        compiler.assert_not_called()
        player_template.assert_not_called()
        packet_builder.assert_not_called()

    def test_runtime_contains_no_pacing_or_spoken_script_contract(self) -> None:
        forbidden = course_runtime.FORBIDDEN_RUNTIME_KEYS
        self.assertFalse(
            forbidden & {key.casefold() for key in walk_keys(self.registry)}
        )

    def test_dense_sentinels_have_claim_bound_visual_emphasis(self) -> None:
        sentinels = {
            "s16_close_atmosphere",
            "s19_fast_load_slow_grid",
            "s20_build_sequence",
            "s21_capital_ownership",
            "s24_megawatts_to_tokens",
        }
        runtime_by_id = {
            segment["segment_id"]: segment for segment in self.registry["segments"]
        }
        self.assertTrue(sentinels <= set(self.visuals["segments"]))
        self.assertTrue(
            all(
                segment["visual"]["label_policy"] == "focus"
                for segment in self.registry["segments"]
                if segment["render_mode"] == "2d"
            )
        )
        for segment_id in sentinels:
            visual = runtime_by_id[segment_id]["visual"]
            self.assertEqual("focus", visual["label_policy"])
            self.assertTrue(visual["annotation"]["items"])
            claim_ids = {claim["id"] for claim in runtime_by_id[segment_id]["claims"]}
            for item in visual["annotation"]["items"]:
                self.assertTrue(set(item["claim_ids"]) <= claim_ids)

        self.assertEqual(
            9,
            len(runtime_by_id["s16_close_atmosphere"]["visual"]["label_node_ids"]),
        )
        s16_annotation = runtime_by_id["s16_close_atmosphere"]["visual"]["annotation"]
        self.assertEqual("parallel", s16_annotation["kind"])
        self.assertIn("Parallel rack paths converge", s16_annotation["title"])
        self.assertTrue(
            any("Liquid path" in item["label"] for item in s16_annotation["items"])
        )
        self.assertTrue(
            any(
                "Residual-air path" in item["label"] for item in s16_annotation["items"]
            )
        )
        s20_items = runtime_by_id["s20_build_sequence"]["visual"]["annotation"]["items"]
        self.assertTrue(
            any("as of evidenced dates" in item["label"] for item in s20_items)
        )
        s09 = runtime_by_id["s09_watt_becomes_heat"]
        self.assertEqual(s09["visual"]["annotation"]["kind"], "sequence")
        self.assertEqual(
            s09["visual"]["annotation"]["title"],
            "Electrical endpoint, thermal source",
        )
        self.assertEqual(len(s09["visual"]["annotation"]["items"]), 2)
        self.assertTrue(
            any(
                "no heat split is inferred" in item["label"]
                for item in s09["visual"]["annotation"]["items"]
            )
        )
        s24_items = runtime_by_id["s24_megawatts_to_tokens"]["visual"]["annotation"][
            "items"
        ]
        self.assertEqual(
            s24_items,
            [
                {
                    "label": "Inference rate: W_facility×W_IT/W_facility×W_accel/W_IT×tokens/J=tokens/s",
                    "claim_ids": [
                        "facility_to_it_scenario_step",
                        "inference_published_boundaries",
                        "inference_scenario_step",
                        "complete_scenario_recipe",
                    ],
                },
                {
                    "label": "Energy yield: J_facility×J_IT/J_facility×J_accel/J_IT×tokens/J=tokens",
                    "claim_ids": [
                        "pue_accounting_boundary",
                        "facility_to_it_scenario_step",
                        "inference_scenario_step",
                        "complete_scenario_recipe",
                    ],
                },
                {
                    "label": (
                        "Training: active peak matmul FLOP/s × same-system measured "
                        "MFU ÷ model FLOP/token = tokens/s"
                    ),
                    "claim_ids": [
                        "training_published_method",
                        "training_scenario_step",
                        "complete_scenario_recipe",
                    ],
                },
                {
                    "label": "Missing site input means no Abilene estimate",
                    "claim_ids": [
                        "site_power_no_estimates",
                        "site_compute_no_estimates",
                        "site_workload_configuration_unknown",
                    ],
                },
            ],
        )
        self.assertEqual(
            [],
            runtime_by_id["s21_capital_ownership"]["visual"]["label_node_ids"],
        )
        s21 = runtime_by_id["s21_capital_ownership"]
        self.assertNotIn("nuclear_ppa", s21["focus_nodes"])
        self.assertEqual(s21["reveal_ids"], [])
        self.assertEqual(s21["reveal_copy_ids"], [])
        s21_copy = [item["label"] for item in s21["visual"]["annotation"]["items"]]
        self.assertTrue(any(label.startswith("Announcement:") for label in s21_copy))
        self.assertTrue(any(label.startswith("Contract:") for label in s21_copy))
        self.assertTrue(any("reported workloads" in label for label in s21_copy))
        s15 = runtime_by_id["s15_water_accounting"]["visual"]["annotation"]
        self.assertEqual(s15["kind"], "comparison")
        self.assertEqual(
            [item["claim_ids"] for item in s15["items"]],
            [
                ["initial_fill_design"],
                ["anticipated_maintenance"],
                ["measured_operating_consumption_unknown"],
            ],
        )
        legend_segments = {
            segment["segment_id"]
            for segment in self.registry["segments"]
            if segment["visual"]["show_legend"]
        }
        self.assertEqual(set(), legend_segments)
        self.assertEqual(
            "layers",
            runtime_by_id["p1_read_the_machine"]["visual"]["annotation"]["kind"],
        )
        self.assertTrue(
            all(
                segment["visual"]["label_policy"] == "focus"
                for segment in self.registry["segments"]
            )
        )
        s20 = runtime_by_id["s20_build_sequence"]["visual"]["annotation"]
        self.assertEqual(5, len(s20["items"]))
        self.assertEqual(
            {claim["id"] for claim in runtime_by_id["s20_build_sequence"]["claims"]},
            {claim_id for item in s20["items"] for claim_id in item["claim_ids"]},
        )

    def test_visual_emphasis_rejects_unbound_claims_and_scope_escape(self) -> None:
        invalid_claim = copy.deepcopy(self.visuals)
        invalid_claim["segments"]["s21_capital_ownership"]["annotation"]["items"][0][
            "claim_ids"
        ] = ["not_a_claim"]
        with self.assertRaisesRegex(
            course_runtime.CourseRuntimeError, "unknown claim IDs"
        ):
            course_runtime.compile_registry(
                self.course,
                self.cameras,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                invalid_claim,
                source_digest="test-digest",
            )

        scope_escape = copy.deepcopy(self.visuals)
        scope_escape["segments"]["s16_close_atmosphere"]["label_node_ids"].append(
            "gas_turbine"
        )
        with self.assertRaisesRegex(
            course_runtime.CourseRuntimeError, "inside segment focus"
        ):
            course_runtime.compile_registry(
                self.course,
                self.cameras,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                scope_escape,
                source_digest="test-digest",
            )

        cross_dimension = copy.deepcopy(self.visuals)
        cross_dimension["segments"]["s16_close_atmosphere"]["label_copy_ids"] = [
            "gas_units"
        ]
        with self.assertRaisesRegex(course_runtime.CourseRuntimeError, "3D emphasis"):
            course_runtime.compile_registry(
                self.course,
                self.cameras,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                cross_dimension,
                source_digest="test-digest",
            )

        invalid_routes = copy.deepcopy(self.visuals)
        invalid_routes["segments"]["s24_megawatts_to_tokens"]["annotation"]["items"][
            -2:
        ] = []
        with self.assertRaisesRegex(
            course_runtime.CourseRuntimeError, "routes requires three or four items"
        ):
            course_runtime.compile_registry(
                self.course,
                self.cameras,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                invalid_routes,
                source_digest="test-digest",
            )

    def test_planned_frames_match_the_planned_shot_compiler(self) -> None:
        visual_map = course_runtime._compiled_visuals(
            self.course,
            self.cameras,
            self.master,
            self.visuals,
        )
        resolved_label_copy_by_segment = course_runtime._resolved_2d_frame_label_copy(
            self.course,
            self.cameras,
            self.master,
            self.ledgers[self.course["meta"]["master_evidence_ledger"]],
            visual_map,
        )
        planned = shots.compile_registry(
            self.course,
            self.cameras,
            self.master,
            self.layout,
            self.scene,
            source_digest="test-digest",
            resolved_label_copy_by_segment=resolved_label_copy_by_segment,
        )
        planned_by_segment = {shot["segment_id"]: shot for shot in planned["shots"]}
        for segment in self.registry["segments"]:
            if segment["status"] == "derived":
                self.assertEqual(
                    planned_by_segment[segment["segment_id"]]["frame"],
                    segment["frame"],
                )

    def test_s09_compact_frame_is_fixed_key_only_and_preserves_standard_frame(
        self,
    ) -> None:
        segment = next(
            item
            for item in self.registry["segments"]
            if item["segment_id"] == "s09_watt_becomes_heat"
        )
        self.assertEqual(
            segment["frame"],
            {
                "kind": "2d",
                "viewBox": [1074.21, 644.0, 458.345, 257.819],
                "anchor_viewBox": [1000.0, 540.0, 650.0, 300.0],
                "compact_viewBox": [1239.791, 713.0, 170.098, 95.68],
            },
        )

        visuals = copy.deepcopy(self.visuals)
        del visuals["segments"]["s09_watt_becomes_heat"]
        context_registry = course_runtime.compile_registry(
            self.course,
            self.cameras,
            self.master,
            self.layout,
            self.scene,
            self.ledgers,
            visuals,
            source_digest="compact-disabled-without-focus-policy",
        )
        context_segment = next(
            item
            for item in context_registry["segments"]
            if item["segment_id"] == "s09_watt_becomes_heat"
        )
        self.assertEqual(context_segment["visual"]["label_policy"], "context")
        self.assertIn("compact_viewBox", context_segment["frame"])

    def test_visual_schema_version_requires_an_exact_integer(self) -> None:
        for invalid in (True, 1.0, "1"):
            visuals = copy.deepcopy(self.visuals)
            visuals["schema_version"] = invalid
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(
                    course_runtime.CourseRuntimeError,
                    "course visuals schema_version must be 1",
                ),
            ):
                course_runtime._compiled_visuals(
                    self.course,
                    self.cameras,
                    self.master,
                    visuals,
                )

    def test_all_two_dimensional_frames_fit_selected_copy_with_margin(self) -> None:
        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        frame_width = float(self.layout["frame"]["w"])
        frame_height = float(self.layout["frame"]["h"])
        affected_rendered_metrics = {
            ("s05_ppa_not_wire", "nuclear_variant"): (43.636, 320.364),
            ("s09_watt_becomes_heat", "die_turn"): (1101.574, 1276.0),
            ("s20_build_sequence", "station_138"): (381.583, 530.0),
            ("s20_build_sequence", "region_buildings"): (1186.028, 1513.972),
        }
        checked_metrics: set[tuple[str, str]] = set()

        for segment in self.registry["segments"]:
            if segment["render_mode"] != "2d":
                continue
            view_x, view_y, view_width, view_height = segment["frame"]["viewBox"]
            self.assertGreaterEqual(view_x, 0)
            self.assertGreaterEqual(view_y, 0)
            self.assertLessEqual(view_x + view_width, frame_width)
            self.assertLessEqual(view_y + view_height, frame_height)

            copy_ids = list(
                dict.fromkeys(
                    [
                        *segment["visual"]["label_copy_ids"],
                        *segment["reveal_copy_ids"],
                    ]
                )
            )
            copy_ids = [
                copy_id
                for copy_id in copy_ids
                if copy_id not in course_runtime._LEGEND_GRAMMAR_CUES
            ]
            resolved = {
                copy_id: layout_pipeline.resolve_copy(
                    self.master,
                    evidence,
                    copy_id,
                    include_hidden=True,
                )
                for copy_id in copy_ids
            }
            bounds = shots.two_dimensional_label_bounds(self.layout, resolved)
            margin = shots.TWO_DIMENSIONAL_LABEL_SAFETY_MARGIN
            for copy_id, record in bounds.items():
                x0, y0, x1, y1 = record["bbox"]
                self.assertLessEqual(view_x, x0 - margin + 0.001)
                self.assertLessEqual(view_y, y0 - margin + 0.001)
                self.assertGreaterEqual(view_x + view_width, x1 + margin - 0.001)
                self.assertGreaterEqual(view_y + view_height, y1 + margin - 0.001)

                metric_key = (segment["segment_id"], copy_id)
                if metric_key in affected_rendered_metrics:
                    actual_x0, actual_x1 = affected_rendered_metrics[metric_key]
                    self.assertLessEqual(view_x, actual_x0 - margin)
                    self.assertGreaterEqual(
                        view_x + view_width,
                        actual_x1 + margin,
                    )
                    checked_metrics.add(metric_key)

        self.assertEqual(set(affected_rendered_metrics), checked_metrics)

    def test_every_frame_is_finite_and_every_claim_is_resolved(self) -> None:
        for segment in self.registry["segments"]:
            frame = segment["frame"]
            geometry = (
                [
                    *frame["viewBox"],
                    *frame["anchor_viewBox"],
                    *frame.get("compact_viewBox", []),
                ]
                if frame["kind"] == "2d"
                else [
                    *frame["position"],
                    *frame["target"],
                    *frame["anchor_position"],
                    *frame["anchor_target"],
                ]
            )
            self.assertTrue(all(math.isfinite(float(value)) for value in geometry))
            self.assertTrue(segment["claims"] or segment["blocking_research"])
            for claim in segment["claims"]:
                self.assertTrue(claim["facts"])
                for fact in claim["facts"]:
                    self.assertTrue(fact["ref"])
                    self.assertTrue(fact["basis"])
                    self.assertTrue(fact["value"])
                    self.assertTrue(fact["scope"])
                    self.assertTrue(fact["sources"])
                    self.assertTrue(
                        all(source["accessed_as_of"] for source in fact["sources"])
                    )
                    self.assertTrue(
                        all(source["date_note"] for source in fact["sources"])
                    )
                    if claim["binding"] == "topology":
                        self.assertTrue(fact["topology_targets"])
                        self.assertTrue(
                            {target["id"] for target in fact["topology_targets"]}
                            <= {
                                *segment["focus_nodes"],
                                *segment["focus_edges"],
                            }
                        )
                    self.assertTrue(
                        all(
                            source["url"].startswith("https://")
                            for source in fact["sources"]
                        )
                    )
                self.assertIn("teaching reference", segment["boundary_note"])

    def test_player_injects_shared_short_surface_label_threshold(self) -> None:
        player = course_runtime._player_template()
        self.assertIn(
            f"mount.clientHeight < {shots.MIN_SPATIAL_LABEL_SURFACE_HEIGHT_PX}",
            player,
        )
        self.assertNotIn("__MIN_SPATIAL_LABEL_SURFACE_HEIGHT_PX__", player)

    def test_player_activates_compact_two_dimensional_frame_with_fixed_key(self) -> None:
        player = course_runtime._player_template()
        self.assertIn("function compact2dFrameActive(shot)", player)
        self.assertIn("function active2dView(shot)", player)
        self.assertIn("mapStage.clientWidth < 400", player)
        self.assertIn('if (shot.visual?.label_policy !== "focus") return false', player)
        self.assertIn(
            f"mapStage.clientHeight < {shots.MIN_SPATIAL_LABEL_SURFACE_HEIGHT_PX}",
            player,
        )
        self.assertIn(
            "const spatialLabelsReadable = !compactFrame && projectedBaseFont >= 10",
            player,
        )
        self.assertIn(
            'mapSvg.setAttribute("viewBox", active2dView(shot).join(" "))',
            player,
        )

    def test_player_inherits_depth_separated_focus_rendering(self) -> None:
        player = course_runtime._player_template()
        planned = shots.runtime_html_template()
        player_start = player.index("function renderDepthSeparatedFocus()")
        player_end = player.index("\n}\n", player_start) + 2
        planned_start = planned.index("function renderDepthSeparatedFocus()")
        planned_end = planned.index("\n}\n", planned_start) + 2

        self.assertEqual(
            planned[planned_start:planned_end],
            player[player_start:player_end],
        )
        self.assertIn("renderDepthSeparatedFocus();", player)
        self.assertLess(
            player.index("camera.layers.mask = cameraLayerMask;"),
            player.index("labelRenderer.render(scene, camera);"),
        )
        label_rule = player.split(".node-label {", 1)[1].split("}", 1)[0]
        self.assertNotIn("max-width", label_rule)
        self.assertIn("white-space: nowrap;", label_rule)

    def test_all_portrait_focus_keys_wrap_inside_the_declared_header_budget(
        self,
    ) -> None:
        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        nodes = {node["id"]: node for node in self.master["nodes"]}
        results = []
        for segment in self.registry["segments"]:
            entries = course_runtime.focus_key_entries(
                segment,
                self.master,
                evidence,
            )
            visual = segment["visual"]
            expected_ids = list(
                dict.fromkeys(
                    [*visual["label_copy_ids"], *segment["reveal_copy_ids"]]
                    if segment["render_mode"] == "2d"
                    else visual["label_node_ids"]
                )
            )
            if segment["render_mode"] == "2d":
                expected_labels = [
                    layout_pipeline.resolve_copy(
                        self.master,
                        evidence,
                        copy_id,
                        include_hidden=True,
                    )
                    for copy_id in expected_ids
                ]
            else:
                expected_labels = [
                    (
                        f"{nodes[node_id]['label']} · "
                        f"{nodes[node_id]['presence'].replace('_', ' ')} · "
                        f"{nodes[node_id]['lifecycle'].replace('_', ' ')}"
                    )
                    for node_id in expected_ids
                ]
            self.assertEqual(expected_ids, [entry["id"] for entry in entries])
            self.assertEqual(expected_labels, [entry["label"] for entry in entries])
            self.assertTrue(all(entry["compact_label"] for entry in entries))
            geometry = [entry for entry in entries if entry["marker_required"]]
            grammar = [entry for entry in entries if not entry["marker_required"]]
            self.assertEqual(
                list(range(1, len(geometry) + 1)),
                [entry["number"] for entry in geometry],
            )
            self.assertTrue(all(entry["number"] is None for entry in grammar))
            self.assertGreaterEqual(len(entries), 2)
            labels = [entry["compact_label"] for entry in entries]
            estimate = course_runtime.estimate_portrait_masthead_layout(
                segment,
                labels,
                grammar_cues=[entry["swatch_cue"] for entry in entries],
            )
            self.assertEqual(290, estimate["content_width_px"])
            self.assertFalse(estimate["focus_key"]["horizontal_paging_required"])
            self.assertTrue(estimate["focus_key"]["within_chip_budget"])
            self.assertEqual(
                "deterministic_static_estimate_not_live_browser",
                estimate["evidence_scope"],
            )
            self.assertTrue(estimate["estimated_complete_key_fit"])
            self.assertGreaterEqual(estimate["spare_height_px"], 0)
            results.append((segment["segment_id"], len(entries), estimate))

        self.assertEqual(course_runtime.EXPECTED_SEGMENTS, len(results))
        maximum_chips = max(results, key=lambda result: result[1])
        self.assertEqual("p1_read_the_machine", maximum_chips[0])
        self.assertEqual(
            course_runtime.PORTRAIT_FOCUS_KEY_MAX_CHIPS,
            maximum_chips[1],
        )
        worst = max(
            results,
            key=lambda result: result[2]["required_height_px"],
        )
        self.assertEqual("s24_megawatts_to_tokens", worst[0])
        self.assertEqual(11, worst[1])
        self.assertGreaterEqual(
            worst[2]["spare_height_px"],
            course_runtime.PORTRAIT_MASTHEAD_SAFETY_MARGIN_PX,
        )

    def test_portrait_focus_key_is_a_wrapping_semantic_list(self) -> None:
        player = course_runtime._player_template()
        self.assertIn(
            '<ol id="focus-key" role="list" tabindex="0" aria-label="Focus key: visual grammar and numbered topology labels" hidden></ol>',
            player,
        )
        self.assertIn('const chip = document.createElement("li")', player)
        self.assertIn('index.setAttribute("aria-hidden", "true")', player)
        self.assertIn(
            'chip.setAttribute("aria-label", `${markerNumber}. ${label}`)',
            player,
        )
        self.assertIn('chip.setAttribute("aria-label", label)', player)
        self.assertIn("copy.textContent = compactFocusLabel(id)", player)
        self.assertIn('copy.setAttribute("aria-hidden", "true")', player)
        self.assertIn("chip.title = label", player)
        self.assertIn(
            f":root {{ --head: {course_runtime.PORTRAIT_MASTHEAD_HEIGHT_PX}px; }}",
            player,
        )
        self.assertIn(
            f"grid-template-columns: repeat({course_runtime.PORTRAIT_FOCUS_KEY_COLUMNS}, minmax(0, 1fr));",
            player,
        )
        self.assertIn("overflow-x: visible;", player)
        self.assertIn("white-space: normal;", player)
        self.assertIn("overflow-wrap: anywhere;", player)
        self.assertNotIn("__PORTRAIT_", player)

    def test_all_short_height_focus_keys_fit_without_horizontal_paging(self) -> None:
        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        results = []
        for segment in self.registry["segments"]:
            entries = course_runtime.focus_key_entries(
                segment,
                self.master,
                evidence,
            )
            estimate = course_runtime.estimate_short_focus_key_layout(
                [str(entry["compact_label"]) for entry in entries],
                grammar_cues=[entry["swatch_cue"] for entry in entries],
            )
            self.assertEqual("844x390", estimate["viewport_id"])
            self.assertEqual(476.0, estimate["content_width_px"])
            self.assertFalse(estimate["horizontal_paging_required"])
            self.assertEqual(0.0, estimate["maximum_excess_width_px"])
            self.assertEqual(0.0, estimate["excess_height_px"])
            self.assertTrue(estimate["estimated_complete_key_fit"])
            results.append((segment["segment_id"], len(entries), estimate))

        self.assertEqual(course_runtime.EXPECTED_SEGMENTS, len(results))
        self.assertEqual(
            course_runtime.PORTRAIT_FOCUS_KEY_MAX_CHIPS,
            max(result[1] for result in results),
        )
        self.assertLessEqual(
            max(result[2]["estimated_height_px"] for result in results),
            course_runtime.SHORT_FOCUS_KEY_MAX_HEIGHT_PX,
        )

        too_wide = course_runtime.estimate_short_focus_key_layout(["X" * 20])
        self.assertFalse(too_wide["estimated_complete_key_fit"])
        self.assertGreater(too_wide["maximum_excess_width_px"], 0)
        too_tall = course_runtime.estimate_short_focus_key_layout(
            ["key"] * (course_runtime.SHORT_FOCUS_KEY_COLUMNS * 3 + 1)
        )
        self.assertFalse(too_tall["estimated_complete_key_fit"])
        self.assertGreater(too_tall["excess_height_px"], 0)

        player = course_runtime._player_template()
        self.assertIn(
            f"max-width: {int(course_runtime.SHORT_FOCUS_KEY_CONTENT_WIDTH_PX)}px;",
            player,
        )
        self.assertIn(
            f"grid-template-columns: repeat({course_runtime.SHORT_FOCUS_KEY_COLUMNS}, minmax(0, 1fr));",
            player,
        )
        self.assertNotIn("__SHORT_FOCUS_KEY_", player)

    def test_legend_key_entries_are_visible_grammar_not_marker_targets(self) -> None:
        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        p1 = next(
            segment
            for segment in self.registry["segments"]
            if segment["segment_id"] == "p1_read_the_machine"
        )
        entries = course_runtime.focus_key_entries(p1, self.master, evidence)
        grammar = [entry for entry in entries if entry["key_role"] == "grammar"]
        self.assertEqual(
            [
                "legend_title",
                "legend_direction",
                "legend_posture",
                "legend_energized",
                "legend_permitted",
                "legend_future",
                "legend_conceptual",
            ],
            [entry["id"] for entry in grammar],
        )
        self.assertTrue(all(not entry["marker_required"] for entry in grammar))
        self.assertTrue(all(entry["label"] for entry in grammar))
        self.assertTrue(all(entry["compact_label"] for entry in grammar))
        self.assertTrue(all(entry["number"] is None for entry in grammar))
        direction = next(
            entry for entry in grammar if entry["id"] == "legend_direction"
        )
        self.assertEqual(direction["compact_label"], "138 tie → station")
        self.assertIn(
            "initial 138 kV tie → initial 200 MW / 138 kV station",
            direction["accessible_label"],
        )
        grammar_contract = course_runtime.fixed_grammar_key_contract()
        self.assertTrue(
            grammar_contract["passed"], grammar_contract["missing_token_ids"]
        )
        self.assertEqual(grammar_contract["minimum_font_px"], 10.0)

        invalid = copy.deepcopy(p1)
        invalid["visual"]["label_copy_ids"][0] = "legend_unknown"
        with self.assertRaisesRegex(
            course_runtime.CourseRuntimeError, "unknown fixed grammar key ID"
        ):
            course_runtime.focus_key_entries(invalid, self.master, evidence)

    def test_all_tablet_focus_keys_fit_the_exact_wrapping_grid(self) -> None:
        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        for segment in self.registry["segments"]:
            entries = course_runtime.focus_key_entries(segment, self.master, evidence)
            estimate = course_runtime.estimate_tablet_focus_key_layout(
                [str(entry["compact_label"]) for entry in entries],
                grammar_cues=[entry["swatch_cue"] for entry in entries],
            )
            self.assertEqual(estimate["viewport_id"], "1024x768")
            self.assertEqual(estimate["font_px"], 10.0)
            self.assertEqual(estimate["index_font_px"], 10.0)
            self.assertEqual(estimate["maximum_excess_width_px"], 0.0)
            self.assertEqual(estimate["excess_height_px"], 0.0)
            self.assertTrue(estimate["estimated_complete_key_fit"], estimate)

    def test_all_desktop_focus_keys_fit_the_exact_wrapping_grid(self) -> None:
        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        evaluations = []
        for segment in self.registry["segments"]:
            entries = course_runtime.focus_key_entries(
                segment,
                self.master,
                evidence,
            )
            for viewport in course_runtime.DESKTOP_REFERENCE_VIEWPORTS:
                estimate = course_runtime.estimate_desktop_focus_key_layout(
                    [str(entry["compact_label"]) for entry in entries],
                    viewport_id=str(viewport["id"]),
                    grammar_cues=[entry["swatch_cue"] for entry in entries],
                )
                self.assertEqual(estimate["font_px"], 10.0)
                self.assertEqual(estimate["index_font_px"], 10.0)
                self.assertEqual(estimate["maximum_excess_width_px"], 0.0)
                self.assertEqual(estimate["excess_height_px"], 0.0)
                self.assertFalse(estimate["horizontal_paging_required"])
                self.assertTrue(estimate["estimated_complete_key_fit"], estimate)
                evaluations.append(estimate)

        self.assertEqual(52, len(evaluations))
        self.assertEqual(
            {"1920x1080": 1372.0, "1440x900": 892.0},
            {
                estimate["viewport_id"]: estimate["content_width_px"]
                for estimate in evaluations
            },
        )
        self.assertLessEqual(
            max(estimate["estimated_height_px"] for estimate in evaluations),
            course_runtime.DESKTOP_FOCUS_KEY_MAX_HEIGHT_PX,
        )

        too_wide = course_runtime.estimate_desktop_focus_key_layout(
            ["X" * 30],
            viewport_id="1440x900",
        )
        self.assertFalse(too_wide["estimated_complete_key_fit"])
        self.assertGreater(too_wide["maximum_excess_width_px"], 0.0)
        too_tall = course_runtime.estimate_desktop_focus_key_layout(
            ["key"] * (course_runtime.DESKTOP_FOCUS_KEY_COLUMNS * 2 + 1),
            viewport_id="1440x900",
        )
        self.assertFalse(too_tall["estimated_complete_key_fit"])
        self.assertGreater(too_tall["excess_height_px"], 0.0)

    def test_responsive_focus_key_typography_and_direction_span_fail_closed(
        self,
    ) -> None:
        contract = course_runtime.responsive_focus_key_contract()
        self.assertTrue(contract["passed"], contract["missing_token_ids"])
        self.assertEqual(contract["minimum_text_font_px"], 10.0)
        self.assertEqual(contract["minimum_index_font_px"], 10.0)
        self.assertEqual(contract["short_opening_question_font_px"], 10.0)
        self.assertEqual(
            contract["aria_label"],
            "Focus key: visual grammar and numbered topology labels",
        )
        self.assertEqual(
            contract["direction_column_span_by_profile"],
            {"desktop": 2, "tablet": 2, "short": 2, "portrait": 1},
        )

        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        p1 = next(
            segment
            for segment in self.registry["segments"]
            if segment["segment_id"] == "p1_read_the_machine"
        )
        entries = course_runtime.focus_key_entries(p1, self.master, evidence)
        portrait = course_runtime.estimate_portrait_focus_key_layout(
            [entry["compact_label"] for entry in entries],
            grammar_cues=[entry["swatch_cue"] for entry in entries],
        )
        self.assertEqual(portrait["column_spans"], [1] * len(entries))
        self.assertEqual(portrait["row_count"], 6)

        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(
                "font-size: __FOCUS_KEY_INDEX_FONT_PX__px;",
                "font-size: 9px;",
                1,
            ),
        ):
            reduced_index = course_runtime.responsive_focus_key_contract()
        self.assertFalse(reduced_index["passed"])
        self.assertIn("base_index_font", reduced_index["missing_token_ids"])

        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(
                "@media (min-width: 521px) {",
                "@media (min-width: 390px) {",
                1,
            ),
        ):
            portrait_span = course_runtime.responsive_focus_key_contract()
        self.assertFalse(portrait_span["passed"])
        self.assertIn("nonportrait_direction_span", portrait_span["missing_token_ids"])

    def test_portrait_transport_slots_do_not_shift_without_teaching(self) -> None:
        contract = course_runtime.portrait_transport_slot_contract()
        self.assertTrue(contract["passed"], contract["missing_token_ids"])
        self.assertEqual(contract["annotated_assignments"]["next"], 4)
        self.assertEqual(contract["unannotated_assignments"]["next"], 4)
        self.assertEqual(contract["unannotated_teaching_slot"], "reserved_hidden")

        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(
                "#next { grid-area: next; }",
                "#next { grid-area: evidence; }",
                1,
            ),
        ):
            broken = course_runtime.portrait_transport_slot_contract()
        self.assertFalse(broken["passed"])
        self.assertIn("next_area", broken["missing_token_ids"])

    def test_teaching_annotations_are_opt_in_at_every_viewport(self) -> None:
        contract = course_runtime.teaching_annotation_disclosure_contract()
        self.assertTrue(contract["passed"], contract["missing_token_ids"])
        self.assertTrue(contract["closed_by_default_all_viewports"])
        self.assertEqual(contract["annotation_content_order"], "authored_exact")
        self.assertEqual(contract["default_visual_geometry"], "labels_only_full_stage")

        player = course_runtime._player_template()
        self.assertIn(
            "teachingOpen = Boolean(open && shot.visual?.annotation);",
            player,
        )
        self.assertNotIn(
            "teachingOpen = Boolean(open && shot.visual?.annotation && portraitTeachingMode());",
            player,
        )
        self.assertIn("overlay.hidden = !annotationOpen;", player)

        with patch.object(
            course_runtime,
            "NOTES_JS",
            course_runtime.NOTES_JS.replace(
                "overlay.hidden = !annotationOpen;",
                "overlay.hidden = !hasAnnotation;",
                1,
            ),
        ):
            broken = course_runtime.teaching_annotation_disclosure_contract()
        self.assertFalse(broken["passed"])
        self.assertIn("closed_until_requested", broken["missing_token_ids"])

    def test_short_teaching_overlay_clearance_contract_fails_closed(self) -> None:
        contract = course_runtime.teaching_overlay_stage_edge_clearance_contract()
        self.assertTrue(contract["passed"], contract["missing_token_ids"])
        self.assertEqual(contract["minimum_stage_edge_clearance_px"], 8.0)
        self.assertEqual(contract["short_overlay_padding_block_px"], 5.0)
        self.assertEqual(contract["short_item_padding_block_px"], 3.0)
        self.assertEqual(contract["minimum_item_font_px"], 10.0)

        player = course_runtime._player_template()
        self.assertIn("bottom: calc(var(--transport) + 8px);", player)
        self.assertIn("left: calc(var(--rail) + 8px);", player)
        self.assertIn("right: 8px; left: auto;", player)
        self.assertIn("padding: 5px 8px;", player)
        self.assertIn("padding: 3px 5px;", player)
        self.assertNotIn("__TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX__", player)
        self.assertNotIn("__SHORT_TEACHING_OVERLAY_PADDING_BLOCK_PX__", player)
        self.assertNotIn(
            "__SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX__",
            player,
        )

        bottom_token = (
            "bottom: calc(var(--transport) + "
            "__TEACHING_OVERLAY_STAGE_EDGE_CLEARANCE_PX__px);"
        )
        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(
                bottom_token,
                "bottom: calc(var(--transport) + 1px);",
                1,
            ),
        ):
            broken = course_runtime.teaching_overlay_stage_edge_clearance_contract()
        self.assertFalse(broken["passed"])
        self.assertIn("short_bottom_clearance", broken["missing_token_ids"])

    def test_focused_map_strokes_are_non_scaling_and_fail_closed(self) -> None:
        contract = course_runtime.focused_geometry_stroke_contract()
        self.assertTrue(contract["passed"], contract["missing_token_ids"])
        self.assertEqual(contract["scaling_mode"], "non_scaling_stroke")
        self.assertEqual(contract["minimum_effective_stroke_px"], 1.5)
        self.assertEqual(contract["minimum_effective_dash_px"], 1.0)

        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(
                "vector-effect: non-scaling-stroke;",
                "vector-effect: none;",
                1,
            ),
        ):
            broken = course_runtime.focused_geometry_stroke_contract()
        self.assertFalse(broken["passed"])
        self.assertIn("non_scaling_stroke", broken["missing_token_ids"])

    def test_portrait_teaching_drawer_is_closed_accessible_and_full_stage(self) -> None:
        contract = course_runtime.portrait_teaching_drawer_contract()
        self.assertTrue(contract["passed"], contract["missing_token_ids"])
        self.assertEqual(
            "deterministic_source_contract_not_live_browser",
            contract["evidence_scope"],
        )
        self.assertTrue(contract["closed_by_default"])
        self.assertEqual("authored_exact", contract["annotation_content_order"])
        self.assertGreaterEqual(contract["minimum_item_font_px"], 10.0)
        self.assertEqual(
            {
                "x": course_runtime.PORTRAIT_RAIL_WIDTH_PX,
                "y": course_runtime.PORTRAIT_MASTHEAD_HEIGHT_PX,
                "width": 318,
                "height": (
                    course_runtime.PORTRAIT_REFERENCE_VIEWPORT_HEIGHT_PX
                    - course_runtime.PORTRAIT_MASTHEAD_HEIGHT_PX
                    - course_runtime.PORTRAIT_TRANSPORT_HEIGHT_PX
                ),
            },
            contract["drawer_box"],
        )
        self.assertEqual("hidden", contract["overflow_x"])
        self.assertEqual("auto", contract["overflow_y"])
        self.assertNotIn("drawer_single_column_items", contract["missing_token_ids"])
        self.assertNotIn("drawer_item_wrap", contract["missing_token_ids"])
        self.assertNotIn("fact_id_wrap", contract["missing_token_ids"])

        player = course_runtime._player_template()
        self.assertIn(
            '<button id="teaching-toggle" type="button" aria-controls="teaching-overlay" aria-expanded="false" hidden>',
            player,
        )
        self.assertIn(
            '<aside id="teaching-overlay" role="region"',
            player,
        )
        self.assertIn('aria-labelledby="teaching-title" hidden inert>', player)
        self.assertNotIn(
            '<aside id="teaching-overlay" role="region" aria-modal="true"',
            player,
        )
        self.assertIn("stage.inert = true;", player)
        self.assertIn('stage.setAttribute("aria-hidden", "true")', player)
        self.assertIn("overlay.inert = overlay.hidden;", player)
        self.assertIn('if (focusDrawer) $("teaching-close").focus()', player)
        self.assertIn("setTeachingOpen(false, { restoreFocus: true })", player)
        dock = player[player.index("function applyTeachingDock(shot)") :]
        drawer_guard = dock.index('if (overlay.dataset.mobileOpen === "true") return;')
        self.assertLess(drawer_guard, dock.index("bestMapPane("))

        selector = '#teaching-overlay[data-mobile-drawer="true"]:not([hidden])'
        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(selector, "#broken-drawer", 1),
        ):
            broken = course_runtime.portrait_teaching_drawer_contract()
        self.assertFalse(broken["passed"])
        self.assertIn("full_stage_drawer", broken["missing_token_ids"])

        required_repairs = {
            "drawer_single_column_items": (
                '#teaching-overlay[data-mobile-drawer="true"][data-kind="routes"] #teaching-items {'
                "\n      grid-template-columns: minmax(0, 1fr);"
            ),
            "drawer_item_wrap": (
                '#teaching-overlay[data-mobile-drawer="true"] #teaching-items li {'
                "\n      min-width: 0;\n      overflow-wrap: anywhere;"
            ),
            "fact_id_wrap": ".fact-details > p { overflow-wrap: anywhere; }",
        }
        for token_id, token in required_repairs.items():
            with (
                self.subTest(token_id=token_id),
                patch.object(
                    course_runtime,
                    "COURSE_CSS",
                    course_runtime.COURSE_CSS.replace(token, "/* removed repair */", 1),
                ),
            ):
                broken = course_runtime.portrait_teaching_drawer_contract()
            self.assertFalse(broken["passed"])
            self.assertIn(token_id, broken["missing_token_ids"])

    def test_standard_overlay_width_optimizer_covers_2d_and_3d(self) -> None:
        player = course_runtime._player_template()
        dock = player[player.index("function applyTeachingDock(shot)") :]
        dock = dock[: dock.index("function resizeVisualSurface(shot)")]
        self.assertIn("function bestMapPane", player)
        self.assertIn("function bestThreePane", player)
        self.assertIn("function widestMaximumPhysicalAreaCandidate", player)
        self.assertEqual(dock.count("for (const width of widths)"), 2)
        self.assertIn(
            "const widths = standardProfile ? standardTeachingOverlayWidths : [null];",
            dock,
        )
        self.assertIn(
            "const pane = bestThreePane(stageRect, overlay.getBoundingClientRect());",
            dock,
        )
        self.assertEqual(
            dock.count("widestMaximumPhysicalAreaCandidate(candidates)"),
            2,
        )

    def test_instructor_packet_annotation_parity_is_exact_and_section_isolated(
        self,
    ) -> None:
        def markdown_escape(value: str) -> str:
            return value.replace("|", "\\|")

        def packet_sections(packet: str) -> dict[str, str]:
            starts = []
            for segment in self.registry["segments"]:
                marker = (
                    f"### {segment['sequence']:02d}. {segment['title']} "
                    f"`{segment['segment_id']}`"
                )
                starts.append((segment["segment_id"], packet.index(marker)))
            return {
                segment_id: packet[start : starts[index + 1][1]]
                if index + 1 < len(starts)
                else packet[start:]
                for index, (segment_id, start) in enumerate(starts)
            }

        def annotation_block(annotation: dict[str, object]) -> str:
            lines = [
                "Presenter-facing teaching focus:",
                "",
                f"- Kind: `{annotation['kind']}`",
                f"- Title: {markdown_escape(annotation['title'])}",
                "",
            ]
            for index, item in enumerate(annotation["items"], start=1):
                claim_ids = ", ".join(f"`{claim_id}`" for claim_id in item["claim_ids"])
                lines.extend(
                    [
                        f"{index}. {markdown_escape(item['label'])}",
                        f"   - Claim IDs: {claim_ids}",
                    ]
                )
            return "\n".join(lines)

        packet = course_runtime.build_instructor_packet(self.registry)
        sections = packet_sections(packet)
        annotated_segments = [
            segment
            for segment in self.registry["segments"]
            if segment["visual"]["annotation"] is not None
        ]
        self.assertEqual(26, len(sections))
        self.assertEqual(16, len(annotated_segments))
        self.assertEqual(
            60,
            sum(
                len(segment["visual"]["annotation"]["items"])
                for segment in annotated_segments
            ),
        )
        self.assertEqual(
            106,
            sum(
                len(item["claim_ids"])
                for segment in annotated_segments
                for item in segment["visual"]["annotation"]["items"]
            ),
        )
        self.assertEqual(16, packet.count("Presenter-facing teaching focus:"))

        for segment in self.registry["segments"]:
            segment_id = segment["segment_id"]
            section = sections[segment_id]
            annotation = segment["visual"]["annotation"]
            if annotation is None:
                self.assertNotIn("Presenter-facing teaching focus:", section)
                continue

            expected_block = annotation_block(annotation)
            self.assertIn(expected_block, section)
            title_line = f"- Title: {markdown_escape(annotation['title'])}"
            for other_segment_id, other_section in sections.items():
                if other_segment_id != segment_id:
                    other_lines = other_section.splitlines()
                    self.assertNotIn(expected_block, other_section)
                    self.assertNotIn(title_line, other_lines)
                    for index, item in enumerate(annotation["items"], start=1):
                        label_line = f"{index}. {markdown_escape(item['label'])}"
                        self.assertNotIn(label_line, other_lines)

        escaped_registry = copy.deepcopy(self.registry)
        escaped_segment = next(
            segment
            for segment in escaped_registry["segments"]
            if segment["visual"]["annotation"] is not None
        )
        escaped_segment["visual"]["annotation"]["title"] = "Input | boundary"
        escaped_segment["visual"]["annotation"]["items"][0]["label"] = "Rate | yield"
        escaped_packet = course_runtime.build_instructor_packet(escaped_registry)
        escaped_section = packet_sections(escaped_packet)[escaped_segment["segment_id"]]
        self.assertIn("- Title: Input \\| boundary", escaped_section)
        self.assertIn("1. Rate \\| yield", escaped_section)
        self.assertNotIn("- Title: Input | boundary", escaped_section)
        self.assertNotIn("1. Rate | yield", escaped_section)

    def test_generated_player_and_packet_are_current_and_manual(self) -> None:
        registry_json, player, packet, digest = course_runtime.build_artifacts()
        second_registry, second_player, second_packet, second_digest = (
            course_runtime.build_artifacts()
        )
        self.assertEqual(
            (registry_json, player, packet, digest),
            (second_registry, second_player, second_packet, second_digest),
        )
        self.assertEqual(registry_json, course_runtime.REGISTRY_PATH.read_text())
        self.assertEqual(player, course_runtime.PLAYER_PATH.read_text())
        self.assertEqual(packet, course_runtime.PACKET_PATH.read_text())
        self.assertEqual(digest, json.loads(registry_json)["source_digest"])
        self.assertIn('id="previous"', player)
        self.assertIn('id="next"', player)
        self.assertNotIn('id="context-toggle"', player)
        self.assertNotIn('$("context-toggle").addEventListener', player)
        self.assertIn('id="evidence-toggle"', player)
        self.assertIn('id="teaching-overlay"', player)
        self.assertIn("function renderTeaching(shot)", player)
        self.assertIn("overlay.dataset.segmentId = shot.segment_id", player)
        self.assertIn('data-segment-id="p1_read_the_machine"', player)
        self.assertIn("shot.visual?.label_copy_ids", player)
        self.assertIn("shot.visual?.label_node_ids", player)
        self.assertIn("mapLegend?.contains(element)", player)
        self.assertIn(
            'mapLegend.style.display = legendRequest === false ? "none" : "inline"',
            player,
        )
        self.assertIn('const protectedCopy = new Set(["footnote"])', player)
        self.assertIn('id="boundary-note"', player)
        self.assertIn('id="boundary-full"', player)
        self.assertIn('id="boundary-compact"', player)
        self.assertIn("Source-gated Abilene facts", player)
        self.assertIn('$("boundary-note").title = shot.boundary_note', player)
        self.assertIn('id="focus-key"', player)
        self.assertIn('id="focus-markers"', player)
        self.assertIn("function renderFocusMarkers(shot)", player)
        self.assertIn('alignment: text.getAttribute("text-anchor") || "middle"', player)
        self.assertIn("const markerOffsetsByAlignment = {", player)
        self.assertIn(
            "markerOffsetsByAlignment[anchor.alignment] || markerOffsetsByAlignment.middle",
            player,
        )
        self.assertIn('index.className = "focus-index"', player)
        self.assertIn('marker.className = "focus-marker"', player)
        self.assertIn('leader.className = "focus-leader"', player)
        self.assertIn("function segmentIntersectsBox", player)
        self.assertIn("function segmentsIntersect", player)
        self.assertIn("Math.hypot(...offset) <= 48", player)
        self.assertIn("visibleLabelRects.every", player)
        self.assertIn("function applyTeachingDock", player)
        self.assertIn("function bestMapPane", player)
        self.assertIn("function bestThreePane", player)
        self.assertIn("function widestMaximumPhysicalAreaCandidate", player)
        self.assertIn(
            "candidate.physicalArea - chosen.physicalArea",
            player,
        )
        self.assertIn("function applyTeachingPane", player)
        self.assertIn("surface.dataset.teachingDock = pane.dock", player)
        self.assertIn("surface.dataset.teachingWidth = overlayWidth", player)
        self.assertIn("No fitted visual pane", player)
        self.assertIn(
            f"width: min({course_runtime.TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX}px,",
            player,
        )
        self.assertIn(
            f"const standardTeachingOverlayWidths = {json.dumps(list(course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX), separators=(',', ':'))};",
            player,
        )
        self.assertNotIn("__TEACHING_OVERLAY_STANDARD_DEFAULT_WIDTH_PX__", player)
        self.assertNotIn("__TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES__", player)
        self.assertIn(
            "grid-template-columns: 24px minmax(0, 1fr);",
            player,
        )
        self.assertIn(
            '#teaching-overlay[data-segment-id="p1_read_the_machine"] #teaching-items li::before { width: 22px; }',
            player,
        )
        self.assertIn(
            '#teaching-overlay[data-kind="funnel"] #teaching-items li:nth-child(5) { width: 60%; }',
            player,
        )
        self.assertIn(
            '#teaching-overlay[data-kind="parallel"] #teaching-items { grid-template-columns: repeat(2, minmax(0, 1fr)); }',
            player,
        )
        self.assertIn("mount.clientWidth < 400", player)
        self.assertIn(
            f"mount.clientHeight < {shots.MIN_SPATIAL_LABEL_SURFACE_HEIGHT_PX}",
            player,
        )
        self.assertNotIn("__MIN_SPATIAL_LABEL_SURFACE_HEIGHT_PX__", player)
        self.assertIn("function updateMapLabelLegibility(shot)", player)
        self.assertIn("projectedBaseFont >= 10", player)
        self.assertIn("function resolveTeachingCollisions(shot)", player)
        self.assertIn(
            'label.element.dataset.layoutSuppressed === "true"',
            player,
        )
        self.assertIn('element.dataset.overlaySuppressed = "true"', player)
        self.assertIn('entry.dataset.claimIds = item.claim_ids.join(" ")', player)
        self.assertIn('id="notes-panel"', player)
        self.assertIn('role="dialog" aria-modal="true"', player)
        self.assertIn('aria-controls="notes-panel"', player)
        self.assertIn('aria-expanded="false"', player)
        self.assertIn('aria-hidden="true" inert', player)
        self.assertIn('aria-label="Course navigation and evidence controls"', player)
        self.assertIn('id="state-status"', player)
        self.assertIn("function updateAccessibleState(shot)", player)
        self.assertIn("button.tabIndex = buttonIndex === current ? 0 : -1", player)
        self.assertIn("button.title = shot.title", player)
        self.assertIn('button.addEventListener("keydown", event => {', player)
        self.assertIn("shotList.children[targetIndex].focus()", player)
        self.assertIn("const titleSentence = /[.!?]$/.test(shot.title)", player)
        self.assertIn('shot.focus_edges.length === 1 ? "path" : "paths"', player)
        self.assertEqual(player.count("function countLabel(count, singular)"), 1)
        self.assertIn('countLabel(shot.focus_edges.length, "edge")', player)
        self.assertIn("function trapNotesFocus(event)", player)
        self.assertIn("element.inert = open", player)
        self.assertIn("panel.inert = !open", player)
        self.assertIn('$("notes-panel").scrollTop = 0', player)
        self.assertIn(
            'const restorePanelFocus = notesOpen && $("notes-panel").contains(document.activeElement);',
            player,
        )
        self.assertIn('if (restorePanelFocus) $("notes-close").focus();', player)
        self.assertIn("#three-mount .node-label small {", player)
        self.assertIn("#three-mount .node-label small {\n    display: none;", player)
        self.assertNotIn("#objective { display: none; }", player)
        self.assertIn("@media (max-height: 560px) and (min-width: 821px)", player)
        self.assertIn(
            '#three-mount .node-label[data-presence="teaching_reference"]', player
        )
        self.assertIn('notesSection("What the evidence supports")', player)
        self.assertIn(".fact-details > p { overflow-wrap: anywhere; }", player)
        self.assertIn(
            '#teaching-overlay[data-mobile-drawer="true"][data-kind="routes"] #teaching-items',
            player,
        )
        self.assertNotIn(
            '#teaching-overlay[data-mobile-drawer="true"] #teaching-items,',
            player,
        )
        self.assertNotRegex(
            player,
            r"(?s)#rail-heading h1\s*\{[^}]*display\s*:\s*none",
        )
        self.assertIn('"Evidence ready"', player)
        self.assertIn('"supported claim group"', player)
        self.assertIn(
            "const knownLimitCount = knownLimits.reduce(",
            player,
        )
        self.assertIn("notesDisclosure(`Known limits (${knownLimitCount})`", player)
        self.assertIn(
            "notesDisclosure(`Avoid overclaiming (${shot.promotion_guard_warnings.length})`",
            player,
        )
        self.assertIn(
            'new Set(["explicit_unknown", "no_evidence_backed_estimate"])', player
        )
        self.assertIn("Fact: ${fact.ref}", player)
        self.assertIn("Basis: ${fact.basis}", player)
        self.assertIn("Topology target: ${fact.topology_targets.map", player)
        self.assertIn("accessed ${source.accessed_as_of}", player)
        self.assertIn("Binding: segment-local, nonphysical teaching overlay", player)
        self.assertLess(
            player.index('notesSection("What the evidence supports")'),
            player.index("notesDisclosure(`Avoid overclaiming"),
        )
        self.assertLess(
            player.index("if (shot.blocking_research.length)"),
            player.index('notesSection("What the evidence supports")'),
        )
        self.assertNotIn('notesSection("Teaching territory")', player)
        self.assertIn('event.key === "ArrowLeft"', player)
        self.assertIn('event.key === "ArrowRight"', player)
        self.assertIn('event.target.closest?.("#focus-key, button, a")', player)
        self.assertLess(
            player.index(
                "if (notesOpen) {", player.index('addEventListener("keydown"')
            ),
            player.index(
                'event.key === "ArrowLeft"', player.index('addEventListener("keydown"')
            ),
        )
        self.assertNotIn("setTimeout(", player)
        self.assertNotIn("setInterval(", player)
        self.assertNotIn("requestAnimationFrame(", player)
        self.assertIn("not a spoken script", packet.casefold())
        self.assertIn("Red-line warnings:", packet)
        self.assertIn("scenario to site estimate", packet.casefold())
        self.assertIn("- Fact: `abilene:", packet)
        self.assertIn("- Basis:", packet)
        self.assertIn("- Topology target:", packet)
        self.assertIn("(accessed 2026-", packet)
        self.assertIn("- Binding: segment-local, nonphysical teaching overlay", packet)

    def test_embedded_json_is_script_safe(self) -> None:
        encoded = course_runtime._script_safe_payload({"title": "x</script>y"})
        self.assertNotIn("</script>", encoded)
        self.assertIn("<\\/script>", encoded)

    def test_semantic_units_are_qualified_not_concatenated(self) -> None:
        self.assertEqual(
            "A reserved slot can precede readiness (project-delivery relationship)",
            course_runtime._display_value(
                {
                    "value": "A reserved slot can precede readiness",
                    "unit": "project-delivery relationship",
                }
            ),
        )
        self.assertEqual(
            "36 months",
            course_runtime._display_value({"value": 36, "unit": "months"}),
        )

    def test_final_segment_has_a_close_not_an_invented_next_segment(self) -> None:
        self.assertIsNone(self.registry["segments"][-1]["transition"])
        self.assertIn("Close:", course_runtime.PACKET_PATH.read_text())


if __name__ == "__main__":
    unittest.main()
