import copy
import hashlib
import json
import struct
import tempfile
import unittest
import zlib
from collections import Counter
from itertools import pairwise
from pathlib import Path
from unittest.mock import patch

from gigawatt import course_runtime, quality


def _png_chunk(chunk_type: bytes, payload: bytes) -> bytes:
    return (
        struct.pack(">I", len(payload))
        + chunk_type
        + payload
        + struct.pack(">I", zlib.crc32(chunk_type + payload) & 0xFFFFFFFF)
    )


def _occupancy_capture_png(width: int, height: int, marker: int) -> bytes:
    row = b"\x00" + bytes([marker % 256]) * width
    return b"".join(
        (
            b"\x89PNG\r\n\x1a\n",
            _png_chunk(
                b"IHDR",
                struct.pack(">IIBBBBB", width, height, 8, 0, 0, 0, 0),
            ),
            _png_chunk(b"IDAT", zlib.compress(row * height, level=9)),
            _png_chunk(b"IEND", b""),
        )
    )


def _acceptance_candidate(manifest: dict, candidate_id: str) -> dict:
    return next(
        record
        for record in manifest["acceptance"]["candidates"]
        if record["candidate_id"] == candidate_id
    )


def _occupancy_review_set(manifest: dict, candidate_id: str = "combined") -> dict:
    return next(
        record
        for record in manifest["occupancy_reviews"]
        if record["candidate_id"] == candidate_id
    )


def _copied_occupancy_reviews(
    manifest: dict, candidate_id: str = "combined"
) -> tuple[list[dict], dict]:
    review_sets = copy.deepcopy(manifest["occupancy_reviews"])
    return review_sets, _occupancy_review_set(
        {"occupancy_reviews": review_sets}, candidate_id
    )


def _resolve_gate(
    gate: dict,
    *,
    candidate_id: str,
    provenance_sha256: str,
    domain: str,
    evidence_id: str,
    evidence: dict,
    status: str,
) -> None:
    gate["status"] = status
    gate["evidence"] = evidence
    gate["evidence_ref"] = quality._acceptance_evidence_ref(
        candidate_id,
        provenance_sha256,
        domain,
        evidence_id,
        evidence,
    )
    gate["reason"] = f"Typed {evidence_id} evidence resolved {status}."


def _fully_resolved_acceptance_candidate(
    record: dict,
    current_state: dict,
    *,
    report_artifact_sha256_by_evidence_id: dict[str, str],
) -> dict:
    resolved = copy.deepcopy(record)
    candidate_id = resolved["candidate_id"]
    provenance = resolved["candidate_provenance_sha256"]
    common = {
        "candidate_id": candidate_id,
        "candidate_provenance_sha256": provenance,
        "candidate_current_state_sha256": current_state[
            "candidate_current_state_sha256"
        ],
        "validation_compiler_implementation_sha256": current_state[
            "validation_compiler_implementation_sha256"
        ],
    }
    report_sha256 = report_artifact_sha256_by_evidence_id.__getitem__
    static_evidence = {
        "validation": {
            **common,
            "command": "uv run gigawatt-validate",
            "exit_code": 0,
            "source_digest_sha256": current_state["candidate_source_digest_sha256"],
            "runtime_output_sha256": current_state["runtime_output_sha256"],
            "modeled_quality_output_sha256": current_state[
                "modeled_quality_output_sha256"
            ],
            "report_artifact_sha256": report_sha256("static:validation"),
        },
        "deterministic_generation": {
            **common,
            "command": "uv run gigawatt-quality",
            "seeds": list(quality.ACCEPTANCE_GENERATION_SEEDS),
            "artifact_count": current_state["generated_artifact_count"],
            "artifact_ids": current_state["generated_artifact_ids"],
            "mismatch_count": 0,
            "artifact_inventory_sha256": current_state[
                "generated_artifact_inventory_sha256"
            ],
            "artifact_set_sha256": current_state["generated_artifact_set_sha256"],
            "report_artifact_sha256": report_sha256("static:deterministic_generation"),
        },
        "evidence": {
            **common,
            "ledger_ids": current_state["evidence_ledger_ids"],
            "ledger_count": current_state["evidence_ledger_count"],
            "source_count": current_state["evidence_source_count"],
            "fact_count": current_state["evidence_fact_count"],
            "validation_error_count": 0,
            "evidence_inventory_sha256": current_state["evidence_inventory_sha256"],
            "report_artifact_sha256": report_sha256("static:evidence"),
        },
    }
    for gate_id, evidence in static_evidence.items():
        _resolve_gate(
            resolved["static_gate_evidence"][gate_id],
            candidate_id=candidate_id,
            provenance_sha256=provenance,
            domain="static",
            evidence_id=gate_id,
            evidence=evidence,
            status="passed",
        )

    browser_evidence = {
        **common,
        "viewport_ids": [viewport["id"] for viewport in quality.VIEWPORTS],
        "segment_count": course_runtime.EXPECTED_SEGMENTS,
        "evaluation_count": course_runtime.EXPECTED_SEGMENTS * len(quality.VIEWPORTS),
        "defect_count": 0,
        "artifact_sha256": report_sha256("live:browser"),
    }
    accessibility_evidence = {
        **common,
        "viewport_ids": [viewport["id"] for viewport in quality.VIEWPORTS],
        "segment_count": course_runtime.EXPECTED_SEGMENTS,
        "snapshot_count": course_runtime.EXPECTED_SEGMENTS * len(quality.VIEWPORTS),
        "violation_count": 0,
        "artifact_sha256": report_sha256("live:accessibility_snapshot"),
    }
    for gate_id, evidence in (
        ("browser", browser_evidence),
        ("accessibility_snapshot", accessibility_evidence),
    ):
        _resolve_gate(
            resolved["live_gate_evidence"][gate_id],
            candidate_id=candidate_id,
            provenance_sha256=provenance,
            domain="live",
            evidence_id=gate_id,
            evidence=evidence,
            status="passed",
        )

    for index, review in enumerate(resolved["blind_reviews"]):
        preference = "candidate" if index < 2 else "champion"
        evidence = {
            **common,
            "reviewer_id": review["reviewer_id"],
            "blind": True,
            "preference": preference,
            "comparison_artifact_sha256": report_sha256(
                f"blind_review:{review['reviewer_id']}"
            ),
        }
        review.update(
            {
                "preference": preference,
                "evidence": evidence,
                "evidence_ref": quality._acceptance_evidence_ref(
                    candidate_id,
                    provenance,
                    "blind_review",
                    review["reviewer_id"],
                    evidence,
                ),
                "reason": "Blind comparison completed.",
            }
        )

    prerequisite_evidence = {
        **common,
        "repair_scope_ids": list(quality.EXPECTED_PREREQUISITE_REPAIRS["scopes"]),
        "unresolved_repair_count": 0,
        "candidate_base_source_digest_sha256": current_state[
            "candidate_source_digest_sha256"
        ],
        "artifact_sha256": report_sha256("final:prerequisite_correctness_repairs"),
    }
    capture_evidence = {
        **common,
        "viewport_ids": [viewport["id"] for viewport in quality.VIEWPORTS],
        "expected_capture_count": course_runtime.EXPECTED_SEGMENTS
        * len(quality.VIEWPORTS),
        "reviewed_capture_count": course_runtime.EXPECTED_SEGMENTS
        * len(quality.VIEWPORTS),
        "capture_set_sha256": report_sha256(
            "final:historical_frozen_champion_viewport_captures"
        ),
    }
    for gate_id, evidence in (
        ("prerequisite_correctness_repairs", prerequisite_evidence),
        ("historical_frozen_champion_viewport_captures", capture_evidence),
    ):
        _resolve_gate(
            resolved["final_independent_gate_evidence"][gate_id],
            candidate_id=candidate_id,
            provenance_sha256=provenance,
            domain="final",
            evidence_id=gate_id,
            evidence=evidence,
            status="passed",
        )
    return resolved


def _acceptance_artifact_records(
    candidate_id: str,
    current_state: dict,
    artifact_sha256_by_evidence_id: dict[str, str],
    artifact_path_by_evidence_id: dict[str, str],
) -> list[dict]:
    return [
        {
            "candidate_id": candidate_id,
            "candidate_current_state_sha256": current_state[
                "candidate_current_state_sha256"
            ],
            "evidence_id": evidence_id,
            "artifact_path": artifact_path_by_evidence_id[evidence_id],
            "artifact_sha256": artifact_sha256_by_evidence_id[evidence_id],
        }
        for evidence_id in artifact_sha256_by_evidence_id
    ]


class ChangeOwnershipCoverageTests(unittest.TestCase):
    def raw_manifest(self) -> dict:
        return quality.scene_pipeline.load_yaml(quality.RATCHET_PATH)

    def test_undeclared_changed_source_fails_inverse_coverage(self) -> None:
        with (
            patch.object(
                quality.champion_pipeline,
                "changed_worktree_paths",
                return_value=("src/undeclared.py",),
            ),
            self.assertRaisesRegex(
                quality.QualityError,
                r"changed canonical source paths.*src/undeclared\.py",
            ),
        ):
            quality.load_ratchet_manifest()

    def test_generated_output_allowlist_is_ignored_but_master_yaml_is_source(
        self,
    ) -> None:
        raw_manifest = self.raw_manifest()
        with patch.object(
            quality.champion_pipeline,
            "changed_worktree_paths",
            return_value=tuple(sorted(quality.GENERATED_OUTPUT_PATH_ALLOWLIST)),
        ):
            self.assertEqual(quality.load_ratchet_manifest(), raw_manifest)

        self.assertNotIn(
            "diagram/master.yaml",
            quality.GENERATED_OUTPUT_PATH_ALLOWLIST,
        )
        broken = copy.deepcopy(raw_manifest)
        for change in broken["changes"]:
            if "diagram/master.yaml" in change["source_paths"]:
                change["source_paths"].remove("diagram/master.yaml")
        with (
            patch.object(quality.scene_pipeline, "load_yaml", return_value=broken),
            patch.object(
                quality.champion_pipeline,
                "changed_worktree_paths",
                return_value=("diagram/master.yaml",),
            ),
            self.assertRaisesRegex(
                quality.QualityError,
                r"changed canonical source paths.*diagram/master\.yaml",
            ),
        ):
            quality.load_ratchet_manifest()

    def test_actual_current_canonical_change_scope_is_declared(self) -> None:
        manifest = quality.load_ratchet_manifest()
        changed_paths = set(
            quality.champion_pipeline.changed_worktree_paths(
                quality.ROOT,
                manifest["frozen_champion"]["git_sha"],
            )
        )
        canonical_changed_paths = (
            changed_paths - quality.GENERATED_OUTPUT_PATH_ALLOWLIST
        )
        declared_source_paths = {
            source_path
            for change in manifest["changes"]
            for source_path in change["source_paths"]
        }
        self.assertEqual(canonical_changed_paths - declared_source_paths, set())
        self.assertLessEqual(
            {
                "README.md",
                "course/REDLINE.md",
                "diagram/master.yaml",
                "pyproject.toml",
                "tests/test_ratchet_docs.py",
            },
            canonical_changed_paths,
        )


class ThreeDimensionalLabelModelTests(unittest.TestCase):
    @staticmethod
    def _compile_quality_for_master(master: dict) -> dict:
        course, cameras, _master, layout, scene, ledgers, visuals = (
            course_runtime.load_inputs()
        )
        runtime = course_runtime.compile_registry(
            course,
            cameras,
            master,
            layout,
            scene,
            ledgers,
            visuals,
            source_digest="a" * 64,
        )
        return quality.compile_quality_registry(
            course,
            master,
            layout,
            scene,
            ledgers,
            runtime,
            source_digest="b" * 64,
            cameras=cameras,
            occupancy_reviews=quality.load_ratchet_manifest()["occupancy_reviews"],
        )

    def test_long_three_dimensional_label_model_bounds_full_nowrap_ink(self) -> None:
        _course, _cameras, master, _layout, _scene, _ledgers, _visuals = (
            course_runtime.load_inputs()
        )
        campus_distribution = next(
            node
            for node in master["nodes"]
            if node["id"] == "campus_mv_distribution"
        )
        self.assertEqual(
            "Abstract campus MV distribution envelope",
            campus_distribution["label"],
        )
        self.assertEqual(40, len(campus_distribution["label"]))
        expected_width = (
            sum(
                quality.THREE_LABEL_PRINTABLE_ASCII_ADVANCE_EM[character]
                for character in campus_distribution["label"]
            )
            * quality.THREE_LABEL_FONT_PX
            + quality.THREE_LABEL_BOX_CHROME_PX
        )
        self.assertAlmostEqual(259.4, expected_width)
        self.assertAlmostEqual(
            expected_width,
            quality._three_label_box_width(campus_distribution),
        )

        registry = self._compile_quality_for_master(master)
        affected_evaluations = []
        for segment in registry["segments"]:
            if segment["segment_id"] not in {
                "s02_generator_terminal",
                "s07_building_power_train",
            }:
                continue
            for evaluation in segment["quality_vector"]["viewport_evaluations"]:
                campus_boxes = [
                    item["box"]
                    for item in evaluation["selected_label_boxes"]
                    if item["id"] == "campus_mv_distribution"
                ]
                if not campus_boxes:
                    continue
                affected_evaluations.append(
                    (segment["segment_id"], evaluation["viewport_id"])
                )
                self.assertAlmostEqual(expected_width, campus_boxes[0]["width"])
                three = evaluation["three_dimensional"]
                self.assertEqual(0, three["residual_stage_clip_count"])
                self.assertEqual(0, three["residual_label_collision_count"])

        self.assertEqual(
            [
                ("s02_generator_terminal", "1920x1080"),
                ("s02_generator_terminal", "1440x900"),
                ("s02_generator_terminal", "1024x768"),
                ("s07_building_power_train", "1920x1080"),
                ("s07_building_power_train", "1440x900"),
                ("s07_building_power_train", "1024x768"),
            ],
            affected_evaluations,
        )

    def test_three_dimensional_label_table_covers_printable_ascii_exactly(
        self,
    ) -> None:
        self.assertEqual(
            {chr(code_point) for code_point in range(0x20, 0x7F)},
            set(quality.THREE_LABEL_PRINTABLE_ASCII_ADVANCE_EM),
        )

    def test_wide_glyph_label_is_suppressed_and_fallback_covered(self) -> None:
        _course, _cameras, master, _layout, _scene, _ledgers, _visuals = (
            course_runtime.load_inputs()
        )
        mutated_master = copy.deepcopy(master)
        campus_distribution = next(
            node
            for node in mutated_master["nodes"]
            if node["id"] == "campus_mv_distribution"
        )
        campus_distribution["label"] = "W" * 75
        self.assertGreater(
            quality._three_label_box_width(campus_distribution),
            862.0,
        )
        campus_distribution["label"] = "%" * 75
        self.assertGreater(
            quality._three_label_box_width(campus_distribution),
            970.0,
        )

        registry = self._compile_quality_for_master(mutated_master)
        segment = next(
            item
            for item in registry["segments"]
            if item["segment_id"] == "s02_generator_terminal"
        )
        evaluation = next(
            item
            for item in segment["quality_vector"]["viewport_evaluations"]
            if item["viewport_id"] == "1024x768"
        )
        selected_ids = {item["id"] for item in evaluation["selected_label_boxes"]}
        three = evaluation["three_dimensional"]
        self.assertNotIn("campus_mv_distribution", selected_ids)
        self.assertIn(
            "campus_mv_distribution", three["layout_suppressed_label_ids"]
        )
        self.assertIn("campus_mv_distribution", three["fixed_key_fallback_ids"])
        self.assertTrue(three["fixed_key_fallback_complete"])
        self.assertEqual(0, three["residual_stage_clip_count"])
        self.assertEqual(0, three["residual_label_collision_count"])

    def test_non_ascii_three_dimensional_label_fails_closed(self) -> None:
        _course, _cameras, master, _layout, _scene, _ledgers, _visuals = (
            course_runtime.load_inputs()
        )
        campus_distribution = next(
            node
            for node in master["nodes"]
            if node["id"] == "campus_mv_distribution"
        )
        for unsupported_label in ("\x1f", "\x7f", "\ufdfd"):
            with self.subTest(unsupported_label=repr(unsupported_label)):
                campus_distribution["label"] = unsupported_label
                with self.assertRaisesRegex(
                    quality.QualityError,
                    "3D spatial label 'campus_mv_distribution' must be a nonempty printable ASCII string",
                ):
                    self._compile_quality_for_master(master)

    def test_non_string_or_empty_three_dimensional_label_fails_closed(self) -> None:
        class SpoofedLabel(str):
            def __iter__(self):
                return iter("W")

        _course, _cameras, master, _layout, _scene, _ledgers, _visuals = (
            course_runtime.load_inputs()
        )
        campus_distribution = next(
            node
            for node in master["nodes"]
            if node["id"] == "campus_mv_distribution"
        )
        for invalid_label in (
            "",
            ["W", "W"],
            ("W",),
            7,
            None,
            SpoofedLabel("\ufdfd"),
        ):
            with self.subTest(invalid_label=repr(invalid_label)):
                campus_distribution["label"] = invalid_label
                with self.assertRaisesRegex(
                    quality.QualityError,
                    "3D spatial label 'campus_mv_distribution' must be a nonempty printable ASCII string",
                ):
                    self._compile_quality_for_master(master)


class QualityRegistryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.quality_json, cls.graph_json, cls.digest = quality.build_artifacts()
        cls.registry = json.loads(cls.quality_json)
        cls.graph = json.loads(cls.graph_json)
        cls.ratchet_manifest = quality.load_ratchet_manifest()
        (
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
            cls.ledgers,
            cls.visuals,
        ) = course_runtime.load_inputs()
        runtime_digest = course_runtime._source_digest(cls.course)
        cls.runtime = course_runtime.compile_registry(
            cls.course,
            cls.cameras,
            cls.master,
            cls.layout,
            cls.scene,
            cls.ledgers,
            cls.visuals,
            source_digest=runtime_digest,
        )
        cls.runtime_digest = runtime_digest

    def test_artifacts_are_deterministic_canonical_json(self) -> None:
        self.assertEqual(
            (self.quality_json, self.graph_json, self.digest),
            quality.build_artifacts(),
        )
        self.assertTrue(self.quality_json.endswith("\n"))

    def test_quality_compilation_preflights_webgl_numeric_domain(self) -> None:
        scene = copy.deepcopy(self.scene)
        box = next(
            primitive
            for structure in scene["structures"]
            for primitive in structure["primitives"]
            if primitive["shape"] == "box"
        )
        box["size"][0] = 1e39
        with self.assertRaisesRegex(
            quality.scene_pipeline.ManifestError, "WebGL Float32-safe bound"
        ):
            quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                scene,
                self.ledgers,
                self.runtime,
                source_digest=self.digest,
            )
        self.assertTrue(self.graph_json.endswith("\n"))
        self.assertEqual(
            self.quality_json,
            course_runtime.scene_pipeline.canonical_payload(self.registry) + "\n",
        )
        self.assertEqual(
            self.graph_json,
            course_runtime.scene_pipeline.canonical_payload(self.graph) + "\n",
        )

    def test_quality_compilation_rejects_blank_three_dimensional_anchor(self) -> None:
        cameras = copy.deepcopy(self.cameras)
        campus = next(
            camera
            for camera in cameras["cameras"]
            if camera["id"] == "campus_establishing"
        )
        campus["position"] = [1_000_000, 1_000_000, 1_000_000]
        with self.assertRaisesRegex(
            quality.scene_pipeline.ManifestError,
            "authored position-target distance.*OrbitControls range",
        ):
            quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.runtime,
                source_digest="blank-camera-anchor",
                cameras=cameras,
            )

    def test_quality_compilation_rejects_float32_collapsed_geometry(self) -> None:
        cases = []
        scene = copy.deepcopy(self.scene)
        box = next(
            primitive
            for structure in scene["structures"]
            for primitive in structure["primitives"]
            if primitive["shape"] == "box"
        )
        box["size"][0] = 1e-300
        cases.append(("dimension", scene, "Float32 quantization"))

        scene = copy.deepcopy(self.scene)
        edge = next(iter(scene["edges"].values()))
        edge["points"] = [edge["points"][0], edge["points"][0]]
        cases.append(("edge", scene, "total path.*Float32 quantization"))

        scene = copy.deepcopy(self.scene)
        scene["world"]["fog"] = {"near": 1e-300, "far": 2e-300}
        cases.append(("fog", scene, "interval.*Float32 quantization"))

        scene = copy.deepcopy(self.scene)
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

        scene = copy.deepcopy(self.scene)
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
                "GPU-matrix collapsed primitive volume",
                scene,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        scene = copy.deepcopy(self.scene)
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
                "repeated rotated primitive volume",
                scene,
                "rotation-aware transformed primitive geometry.*Float32 quantization",
            )
        )

        scene = copy.deepcopy(self.scene)
        edge = next(iter(scene["edges"].values()))
        base = 2**25 + 400
        edge["points"] = [
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

        for label, invalid_scene, message in cases:
            with (
                self.subTest(label=label),
                self.assertRaisesRegex(
                    quality.scene_pipeline.ManifestError,
                    message,
                ),
            ):
                quality.compile_quality_registry(
                    self.course,
                    self.master,
                    self.layout,
                    invalid_scene,
                    self.ledgers,
                    self.runtime,
                    source_digest=self.digest,
                )

    def test_current_audit_subject_is_noncircular_and_binds_every_input(self) -> None:
        materialized = quality._materialized_acceptance_artifact_state()
        baseline = quality._current_audit_subject_state(
            runtime_digest=self.runtime_digest,
            runtime_registry=self.runtime,
            ratchet_manifest=self.ratchet_manifest,
            materialized_artifact_state=materialized,
        )
        self.assertEqual(
            baseline["audit_subject_sha256"],
            self.registry["audit_program"]["saturation"][
                "current_audit_subject_sha256"
            ],
        )

        changed_runtime = copy.deepcopy(self.runtime)
        changed_runtime["segment_count"] += 1
        changed_ratchet = copy.deepcopy(self.ratchet_manifest)
        changed_ratchet["acceptance"]["modeled_eligibility_only"] = False
        changed_materialized = copy.deepcopy(materialized)
        changed_materialized[0]["output_sha256"] = "0" * 64
        input_mutations = (
            {"runtime_digest": "0" * 64},
            {"runtime_registry": changed_runtime},
            {"ratchet_manifest": changed_ratchet},
            {"materialized_artifact_state": changed_materialized},
        )
        defaults = {
            "runtime_digest": self.runtime_digest,
            "runtime_registry": self.runtime,
            "ratchet_manifest": self.ratchet_manifest,
            "materialized_artifact_state": materialized,
        }
        for mutation in input_mutations:
            with self.subTest(mutation=next(iter(mutation))):
                changed = quality._current_audit_subject_state(
                    **{**defaults, **mutation}
                )
                self.assertNotEqual(
                    baseline["audit_subject_sha256"],
                    changed["audit_subject_sha256"],
                )

        implementation = quality._validation_compiler_implementation_state()
        with patch.object(
            quality,
            "_validation_compiler_implementation_state",
            return_value={**implementation, "source_sha256": "0" * 64},
        ):
            changed = quality._current_audit_subject_state(**defaults)
        self.assertNotEqual(
            baseline["audit_subject_sha256"], changed["audit_subject_sha256"]
        )

        read_bytes = Path.read_bytes
        excluded = {
            quality.AUDITS_PATH.resolve(),
            quality.QUALITY_PATH.resolve(),
            quality.GRAPH_PATH.resolve(),
        }

        def reject_circular_reads(path: Path) -> bytes:
            if path.resolve() in excluded:
                raise AssertionError(f"circular audit-subject read: {path}")
            return read_bytes(path)

        with patch.object(Path, "read_bytes", reject_circular_reads):
            noncircular = quality._current_audit_subject_state(**defaults)
        self.assertEqual(baseline, noncircular)

        ratchet_path = quality.RATCHET_PATH.resolve()

        def change_ratchet_source(path: Path) -> bytes:
            payload = read_bytes(path)
            return payload + b"\n" if path.resolve() == ratchet_path else payload

        with patch.object(Path, "read_bytes", change_ratchet_source):
            changed_source = quality._current_audit_subject_state(**defaults)
        self.assertNotEqual(
            baseline["audit_subject_sha256"],
            changed_source["audit_subject_sha256"],
        )

    def test_audit_subject_materialized_inventory_fails_closed(self) -> None:
        materialized = quality._materialized_acceptance_artifact_state()
        mutations = []
        reordered = copy.deepcopy(materialized)
        reordered[:2] = reversed(reordered[:2])
        mutations.append(reordered)
        mutations.append(materialized[:-1])
        mutations.append([*materialized, copy.deepcopy(materialized[-1])])
        malformed = copy.deepcopy(materialized)
        malformed[0]["evidence_basis"] = "retained_bytes_only"
        mutations.append(malformed)
        malformed_digest = copy.deepcopy(materialized)
        malformed_digest[0]["output_sha256"] = "A" * 64
        mutations.append(malformed_digest)
        for invalid in mutations:
            with (
                self.subTest(invalid=invalid),
                self.assertRaises(quality.QualityError),
            ):
                quality._current_audit_subject_state(
                    runtime_digest=self.runtime_digest,
                    runtime_registry=self.runtime,
                    ratchet_manifest=self.ratchet_manifest,
                    materialized_artifact_state=invalid,
                )

    def test_build_computes_materialized_state_once_for_ratchet_and_saturation(
        self,
    ) -> None:
        materialized = quality._materialized_acceptance_artifact_state()
        with patch.object(
            quality,
            "_materialized_acceptance_artifact_state",
            return_value=materialized,
        ) as build_state:
            quality_json, _graph_json, _digest = quality.build_artifacts()
        self.assertEqual(build_state.call_count, 1)
        built = json.loads(quality_json)
        self.assertEqual(
            built["audit_program"]["saturation"]["current_audit_subject_sha256"],
            self.registry["audit_program"]["saturation"][
                "current_audit_subject_sha256"
            ],
        )

    def test_audit_policy_maps_reject_unknown_fields(self) -> None:
        manifest = quality.scene_pipeline.load_yaml(quality.AUDITS_PATH)
        for field in (
            "evidence_scope",
            "priority_policy",
            "loop_policy",
            "consultation_policy",
            "saturation_policy",
            "change_ownership_policy",
        ):
            with self.subTest(field=field):
                broken = copy.deepcopy(manifest)
                broken[field]["unexpected"] = True
                with (
                    patch.object(
                        quality.scene_pipeline,
                        "load_yaml",
                        return_value=broken,
                    ),
                    self.assertRaisesRegex(
                        quality.QualityError,
                        rf"{field} fields must be exact.*unknown=\['unexpected'\]",
                    ),
                ):
                    quality.load_audit_manifest(
                        [segment["segment_id"] for segment in self.runtime["segments"]]
                    )

    def test_audit_policy_truth_values_are_exact_and_fail_closed(self) -> None:
        manifest = quality.scene_pipeline.load_yaml(quality.AUDITS_PATH)
        segment_ids = [segment["segment_id"] for segment in self.runtime["segments"]]

        for policy_name, expected_policy in quality.EXPECTED_AUDIT_POLICIES.items():
            self.assertEqual(manifest[policy_name], expected_policy)
            for field_name, expected_value in expected_policy.items():
                with self.subTest(policy=policy_name, field=field_name):
                    broken = copy.deepcopy(manifest)
                    if type(expected_value) is bool:
                        adversarial_value = not expected_value
                    elif type(expected_value) is int:
                        adversarial_value = expected_value + 1
                    elif isinstance(expected_value, str):
                        adversarial_value = f"{expected_value} adversarial"
                    elif isinstance(expected_value, list):
                        adversarial_value = (
                            list(reversed(expected_value))
                            if len(expected_value) > 1
                            else [*expected_value, "adversarial"]
                        )
                    else:
                        self.fail(
                            f"missing adversarial mutation for {type(expected_value)}"
                        )
                    broken[policy_name][field_name] = adversarial_value
                    with (
                        patch.object(
                            quality.scene_pipeline,
                            "load_yaml",
                            return_value=broken,
                        ),
                        self.assertRaisesRegex(
                            quality.QualityError,
                            rf"{policy_name} values must exactly match",
                        ),
                    ):
                        quality.load_audit_manifest(segment_ids)

    def test_audit_policy_rejects_type_coercion_and_threshold_drift(self) -> None:
        manifest = quality.scene_pipeline.load_yaml(quality.AUDITS_PATH)
        segment_ids = [segment["segment_id"] for segment in self.runtime["segments"]]
        broken_schema = copy.deepcopy(manifest)
        broken_schema["schema_version"] = True
        with (
            patch.object(
                quality.scene_pipeline,
                "load_yaml",
                return_value=broken_schema,
            ),
            self.assertRaisesRegex(
                quality.QualityError,
                "schema_version must be 1",
            ),
        ):
            quality.load_audit_manifest(segment_ids)

        mutations = {
            "boolean_as_integer": (
                "priority_policy",
                "weighted_average_is_sufficient",
                0,
            ),
            "integer_as_boolean": (
                "saturation_policy",
                "required_consecutive_complete_rounds",
                True,
            ),
        }
        for mutation, (policy_name, field_name, adversarial_value) in mutations.items():
            with self.subTest(mutation=mutation):
                broken = copy.deepcopy(manifest)
                broken[policy_name][field_name] = adversarial_value
                with (
                    patch.object(
                        quality.scene_pipeline,
                        "load_yaml",
                        return_value=broken,
                    ),
                    self.assertRaisesRegex(
                        quality.QualityError,
                        rf"{policy_name} values must exactly match",
                    ),
                ):
                    quality.load_audit_manifest(segment_ids)

        for adversarial_threshold in (99.0, 100, True):
            with self.subTest(high_priority_threshold=adversarial_threshold):
                broken = copy.deepcopy(manifest)
                broken["high_priority_threshold"] = adversarial_threshold
                with (
                    patch.object(
                        quality.scene_pipeline,
                        "load_yaml",
                        return_value=broken,
                    ),
                    self.assertRaisesRegex(
                        quality.QualityError,
                        "high_priority_threshold must exactly match 100.0",
                    ),
                ):
                    quality.load_audit_manifest(segment_ids)

    def test_all_26_segments_have_non_aggregate_quality_vectors(self) -> None:
        self.assertEqual(self.registry["aggregation_policy"], "none")
        self.assertEqual(self.registry["segment_count"], 26)
        self.assertEqual(len(self.registry["segments"]), 26)
        self.assertEqual(
            [segment["segment_id"] for segment in self.registry["segments"]],
            [segment["segment_id"] for segment in self.runtime["segments"]],
        )
        expected_viewports = [viewport["id"] for viewport in quality.VIEWPORTS]
        for segment in self.registry["segments"]:
            vector = segment["quality_vector"]
            self.assertEqual(
                set(vector),
                {
                    "focus_density",
                    "annotation_coverage",
                    "overlay_position_candidates",
                    "viewport_evaluations",
                    "risk_flags",
                },
            )
            evaluations = vector["viewport_evaluations"]
            self.assertEqual(
                [evaluation["viewport_id"] for evaluation in evaluations],
                expected_viewports,
            )
            for evaluation in evaluations:
                self.assertIn("focus_density_per_megapixel", evaluation)
                self.assertIn("visible_label_count", evaluation)
                self.assertIn("selected_label_boxes", evaluation)
                self.assertIn("teaching_overlay", evaluation)
                self.assertEqual(evaluation["fixed_focus_key"]["font_px"], 10.0)
                self.assertEqual(
                    evaluation["fixed_boundary_note"]["copy_id"], "footnote"
                )
                self.assertTrue(evaluation["fixed_boundary_note"]["masthead_visible"])
                self.assertTrue(
                    evaluation["fixed_boundary_note"]["full_copy_accessible"]
                )
                self.assertIn("risk_flags", evaluation)
                if segment["render_mode"] == "2d":
                    self.assertEqual(
                        set(evaluation["two_dimensional"]),
                        {
                            "framed_label_ids",
                            "unclamped_label_bounds",
                            "unclamped_label_clipping_count",
                            "unclamped_label_clipping_ids",
                            "minimum_label_frame_margin_svg_units",
                            "required_label_frame_margin_svg_units",
                            "label_frame_margin_tolerance_svg_units",
                            "label_frame_margin_passed",
                            "estimated_label_pixels",
                            "label_stage_ratio",
                            "rendered_pixel_area",
                            "rendered_pixel_ratio_to_full_stage",
                            "legacy_rendered_pixel_area",
                            "legacy_rendered_pixel_ratio_to_full_stage",
                            "rendered_pixel_area_retention_ratio",
                            "max_candidate_rendered_pixel_area",
                            "max_render_area_candidate_selected",
                            "focus_occupancy",
                            "spatial_label_count",
                            "selected_spatial_label_count",
                            "protected_spatial_label_count",
                            "legend_visible_label_count",
                            "projected_base_font_px",
                            "minimum_spatial_font_px",
                            "spatial_font_gate_applied",
                            "spatial_labels_readable",
                            "fixed_focus_key",
                            "focused_geometry_strokes",
                        },
                    )
                else:
                    self.assertEqual(
                        set(evaluation["three_dimensional"]),
                        {
                            "projected_occupancy",
                            "projected_point_count",
                            "clipped_point_count",
                            "intended_label_count",
                            "projected_visible_label_count",
                            "selected_label_box_count",
                            "spatially_suppressed_label_count",
                            "layout_suppressed_label_ids",
                            "unprojected_label_ids",
                            "fixed_key_fallback_ids",
                            "fixed_key_fallback_missing_ids",
                            "fixed_key_fallback_complete",
                            "residual_label_collision_count",
                            "residual_stage_clip_count",
                            "lifecycle_chip_layout",
                        },
                    )

    def test_responsive_evaluation_matches_runtime_fitting_rules(self) -> None:
        runtime_by_segment = {
            segment["segment_id"]: segment for segment in self.runtime["segments"]
        }
        for segment in self.registry["segments"]:
            for evaluation in segment["quality_vector"]["viewport_evaluations"]:
                if "three_dimensional" in evaluation:
                    self.assertEqual(
                        evaluation["three_dimensional"]["clipped_point_count"], 0
                    )
                    self.assertNotIn("projected_clipping", evaluation["risk_flags"])
            if segment["render_mode"] == "2d":
                evaluation = next(
                    item
                    for item in segment["quality_vector"]["viewport_evaluations"]
                    if item["viewport_id"] == "1024x768"
                )
                visual_stage = evaluation["visual_stage"]
                _, _, view_width, view_height = runtime_by_segment[
                    segment["segment_id"]
                ]["frame"]["viewBox"]
                scale = min(
                    (visual_stage["width"] - 20) / view_width,
                    (visual_stage["height"] - 20) / view_height,
                )
                expected_rendered_area = view_width * scale * view_height * scale
                self.assertEqual(
                    evaluation["two_dimensional"]["rendered_pixel_area"],
                    quality._round(expected_rendered_area),
                )
                self.assertEqual(
                    evaluation["two_dimensional"]["rendered_pixel_ratio_to_full_stage"],
                    quality._round(
                        expected_rendered_area / evaluation["stage"]["pixel_count"]
                    ),
                )

        self.assertEqual(
            quality._stage_box(
                next(
                    viewport
                    for viewport in quality.VIEWPORTS
                    if viewport["id"] == "844x390"
                )
            ),
            {"x": 72, "y": 130, "width": 772, "height": 202, "pixel_count": 155944},
        )
        self.assertEqual(
            quality._stage_box(
                next(
                    viewport
                    for viewport in quality.VIEWPORTS
                    if viewport["id"] == "390x844"
                )
            ),
            {"x": 72, "y": 360, "width": 318, "height": 410, "pixel_count": 130380},
        )

    def test_annotated_3d_uses_maximum_physical_canvas_area(self) -> None:
        affected_ids = {
            "s01_fire_to_electricity",
            "s02_generator_terminal",
            "s08_rack_voltage_descent",
            "s15_water_accounting",
            "s16_close_atmosphere",
        }
        for segment in self.registry["segments"]:
            if segment["segment_id"] not in affected_ids:
                continue
            evaluation = next(
                item
                for item in segment["quality_vector"]["viewport_evaluations"]
                if item["viewport_id"] == "1024x768"
            )
            self.assertEqual(evaluation["visual_stage"]["width"], 738)
            self.assertEqual(evaluation["visual_stage"]["height"], 510)
            visual_stage = evaluation["open_visual_stage"]
            self.assertEqual(visual_stage["width"], 462)
            self.assertEqual(visual_stage["height"], 510)
            self.assertEqual(
                visual_stage["selected_standard_overlay_width_px"],
                240,
            )
            self.assertEqual(
                visual_stage["standard_overlay_width_candidates_px"],
                list(course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX),
            )
            self.assertEqual(
                visual_stage["physical_canvas_area"],
                visual_stage["max_candidate_physical_canvas_area"],
            )
            self.assertTrue(visual_stage["max_physical_canvas_area_candidate_selected"])
            self.assertTrue(visual_stage["widest_maximum_area_candidate_selected"])
            self.assertGreaterEqual(
                visual_stage["width"],
                quality.MIN_ANNOTATED_THREE_DIMENSIONAL_STANDARD_CANVAS_WIDTH_PX,
            )
            self.assertEqual(
                evaluation["teaching_overlay"]["selected_standard_width_px"],
                240,
            )

        gate = self.registry["visual_gates"][
            "annotated_three_dimensional_physical_composition"
        ]
        self.assertTrue(gate["passed"], gate["failures"])
        self.assertEqual(gate["segment_count"], 5)
        self.assertEqual(set(gate["segment_ids"]), affected_ids)
        self.assertEqual(gate["viewport_count"], 5)
        self.assertEqual(gate["evaluation_count"], 25)
        self.assertEqual(gate["standard_profile_evaluation_count"], 15)
        self.assertEqual(
            gate["minimum_observed_standard_profile_canvas_width_px"],
            462,
        )
        self.assertEqual(
            [item["evaluation_count"] for item in gate["viewport_summary"]],
            [5, 5, 5, 5, 5],
        )

    def test_annotated_3d_composition_gate_rejects_fixed_390px_dock(self) -> None:
        with patch.object(
            course_runtime,
            "TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX",
            (390,),
        ):
            adversarial = quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.runtime,
                source_digest="adversarial-fixed-390px-three-dimensional-dock",
                occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            )
        gate = adversarial["visual_gates"][
            "annotated_three_dimensional_physical_composition"
        ]
        self.assertFalse(gate["passed"])
        self.assertEqual(gate["failure_count"], 5)
        self.assertEqual(
            {failure["segment_id"] for failure in gate["failures"]},
            {
                "s01_fire_to_electricity",
                "s02_generator_terminal",
                "s08_rack_voltage_descent",
                "s15_water_accounting",
                "s16_close_atmosphere",
            },
        )
        self.assertTrue(
            all(
                failure["viewport_id"] == "1024x768"
                and failure["canvas_width"] == 312
                and failure["reasons"]
                == ["standard_profile_canvas_below_spatial_label_threshold"]
                for failure in gate["failures"]
            )
        )

    def test_physical_area_candidate_ties_choose_the_widest_overlay(self) -> None:
        selected = quality._widest_maximum_physical_area_candidate(
            [
                {"standard_width_px": 240, "physical_area": 100.0},
                {"standard_width_px": 280, "physical_area": 99.0},
                {"standard_width_px": 390, "physical_area": 100.0},
            ]
        )
        self.assertEqual(selected["standard_width_px"], 390)

    def test_unclamped_2d_label_bounds_are_inside_every_derived_frame(self) -> None:
        evaluations = [
            evaluation
            for segment in self.registry["segments"]
            for evaluation in segment["quality_vector"]["viewport_evaluations"]
            if "two_dimensional" in evaluation
        ]
        self.assertEqual(len(evaluations), 15 * len(quality.VIEWPORTS))
        for evaluation in evaluations:
            vector = evaluation["two_dimensional"]
            self.assertEqual(vector["unclamped_label_clipping_count"], 0)
            self.assertEqual(vector["unclamped_label_clipping_ids"], [])
            self.assertTrue(vector["label_frame_margin_passed"])
            self.assertGreaterEqual(
                vector["minimum_label_frame_margin_svg_units"]
                + vector["label_frame_margin_tolerance_svg_units"],
                vector["required_label_frame_margin_svg_units"],
            )
            self.assertTrue(
                all(
                    not record["clipped"] for record in vector["unclamped_label_bounds"]
                )
            )

        gate = self.registry["visual_gates"]["two_dimensional_label_clipping"]
        self.assertTrue(gate["passed"], gate["failures"])
        self.assertEqual(gate["evaluation_count"], len(evaluations))
        self.assertEqual(gate["failure_count"], 0)

        adversarial_runtime = copy.deepcopy(self.runtime)
        segment = next(
            item
            for item in adversarial_runtime["segments"]
            if item["segment_id"] == "s05_ppa_not_wire"
        )
        segment["frame"]["viewBox"][0] += 20.0
        segment["frame"]["viewBox"][2] -= 20.0
        adversarial = quality.compile_quality_registry(
            self.course,
            self.master,
            self.layout,
            self.scene,
            self.ledgers,
            adversarial_runtime,
            source_digest="adversarial-clipped-label-frame",
            occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
        )
        adversarial_gate = adversarial["visual_gates"]["two_dimensional_label_clipping"]
        self.assertFalse(adversarial_gate["passed"])
        self.assertEqual(adversarial_gate["failure_count"], len(quality.VIEWPORTS))
        self.assertTrue(
            all(
                failure["segment_id"] == "s05_ppa_not_wire"
                and failure["clipped_label_ids"] == ["nuclear_variant"]
                for failure in adversarial_gate["failures"]
            )
        )
        self.assertTrue(
            all(
                "label_clipping" in evaluation["risk_flags"]
                for evaluation in next(
                    item
                    for item in adversarial["segments"]
                    if item["segment_id"] == "s05_ppa_not_wire"
                )["quality_vector"]["viewport_evaluations"]
            )
        )

    def test_context_label_coverage_uses_every_runtime_visible_map_label(self) -> None:
        context_runtime = quality._modeled_runtime(
            self.runtime,
            self.ratchet_manifest["experiment_control"],
        )
        self.assertEqual(
            [segment["frame"] for segment in context_runtime["segments"]],
            [segment["frame"] for segment in self.runtime["segments"]],
        )
        context_registry = quality.compile_quality_registry(
            self.course,
            self.master,
            self.layout,
            self.scene,
            self.ledgers,
            context_runtime,
            source_digest="adversarial-context-label-coverage",
            occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            occupancy_candidate_id="experiment_control",
        )
        label_specs = quality._map_label_specs(
            self.course,
            self.master,
            self.layout,
            self.ledgers,
        )
        legend_ids = {
            copy_id for copy_id, spec in label_specs.items() if spec["legend"]
        }
        base_visible_spatial_ids = {
            copy_id
            for copy_id, spec in label_specs.items()
            if spec["base_visible"] and not spec["legend"]
        }
        runtime_by_id = {
            segment["segment_id"]: segment for segment in context_runtime["segments"]
        }
        for segment in context_registry["segments"]:
            if segment["render_mode"] != "2d":
                continue
            runtime_segment = runtime_by_id[segment["segment_id"]]
            expected_ids = sorted(
                base_visible_spatial_ids | set(runtime_segment["reveal_copy_ids"])
            )
            for evaluation in segment["quality_vector"]["viewport_evaluations"]:
                self.assertEqual(
                    evaluation["two_dimensional"]["framed_label_ids"],
                    expected_ids,
                )

        requested_legend_runtime = copy.deepcopy(context_runtime)
        legend_segment = next(
            segment
            for segment in requested_legend_runtime["segments"]
            if segment["segment_id"] == "p1_read_the_machine"
        )
        legend_segment["visual"]["show_legend"] = True
        requested_legend_registry = quality.compile_quality_registry(
            self.course,
            self.master,
            self.layout,
            self.scene,
            self.ledgers,
            requested_legend_runtime,
            source_digest="adversarial-context-requested-legend-coverage",
            occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            occupancy_candidate_id="experiment_control",
        )
        legend_evaluation = next(
            segment
            for segment in requested_legend_registry["segments"]
            if segment["segment_id"] == "p1_read_the_machine"
        )["quality_vector"]["viewport_evaluations"][0]
        self.assertEqual(
            set(legend_evaluation["two_dimensional"]["framed_label_ids"]),
            base_visible_spatial_ids | legend_ids,
        )

        expected_failure_segment_ids = {
            "p0_gigawatt_not_workload",
            "p1_read_the_machine",
            "s03_initial_grid_path",
            "s04_expansion_grid_path",
            "s05_ppa_not_wire",
            "s06_campus_mv_envelope",
            "s09_watt_becomes_heat",
            "s17_interconnection_schedule",
            "s18_long_lead_equipment",
            "s19_fast_load_slow_grid",
            "s20_build_sequence",
            "s22_capital_risk",
            "s23_business_models",
            "s24_megawatts_to_tokens",
        }
        context_gate = context_registry["visual_gates"][
            "two_dimensional_label_clipping"
        ]
        self.assertFalse(context_gate["passed"])
        self.assertEqual(context_gate["failure_count"], 70)
        self.assertEqual(
            Counter(failure["segment_id"] for failure in context_gate["failures"]),
            Counter({segment_id: 5 for segment_id in expected_failure_segment_ids}),
        )
        self.assertTrue(
            all(failure["clipped_label_ids"] for failure in context_gate["failures"])
        )

        self.assertTrue(
            self.registry["visual_gates"]["two_dimensional_label_clipping"]["passed"]
        )
        self.assertEqual(
            self.registry["visual_gates"]["two_dimensional_label_clipping"][
                "failure_count"
            ],
            0,
        )
        challengers = {
            challenger["id"]: challenger
            for challenger in self.registry["ratchet"]["challengers"]
        }
        for result in (
            self.registry["ratchet"]["experiment_control"],
            challengers["annotations_only"],
        ):
            gate = result["layout_gates"]["two_dimensional_label_clipping"]
            self.assertFalse(gate["passed"])
            self.assertEqual(gate["failure_count"], 70)
        for candidate_id in ("labels_only", "combined"):
            gate = challengers[candidate_id]["layout_gates"][
                "two_dimensional_label_clipping"
            ]
            self.assertTrue(gate["passed"])
            self.assertEqual(gate["failure_count"], 0)

    def test_ratchet_manifest_freezes_the_champion_and_enters_digest(self) -> None:
        self.assertEqual(
            self.ratchet_manifest["frozen_champion"], quality.EXPECTED_CHAMPION
        )
        self.assertEqual(
            self.ratchet_manifest["hypothesis"], quality.RATCHET_HYPOTHESIS
        )
        self.assertEqual(
            self.ratchet_manifest["experiment_control"],
            quality.EXPECTED_EXPERIMENT_CONTROL,
        )
        self.assertEqual(self.ratchet_manifest["variants"], quality.EXPECTED_VARIANTS)
        self.assertEqual(
            self.ratchet_manifest["prerequisite_repairs"],
            quality.EXPECTED_PREREQUISITE_REPAIRS,
        )
        self.assertTrue(self.ratchet_manifest["acceptance"]["modeled_eligibility_only"])
        self.assertEqual(
            self.registry["source_digest"],
            quality._quality_source_digest(self.runtime_digest, self.ratchet_manifest),
        )
        self.assertEqual(self.graph["source_digest"], self.registry["source_digest"])

    def test_ratchet_contract_rejects_python_scalar_type_coercion(self) -> None:
        mutations = []
        for invalid in (True, 1.0):
            mutations.append(
                (
                    f"schema_version_{invalid!r}",
                    lambda manifest, value=invalid: manifest.__setitem__(
                        "schema_version", value
                    ),
                    "schema_version must be 1",
                )
            )
        for invalid in (True, 75.0):
            mutations.append(
                (
                    f"champion_count_{invalid!r}",
                    lambda manifest, value=invalid: manifest[
                        "frozen_champion"
                    ].__setitem__("baseline_test_count", value),
                    "changed the frozen champion",
                )
            )
        mutations.append(
            (
                "champion_origin_non_string",
                lambda manifest: manifest["frozen_champion"].__setitem__(
                    "origin_sha", 0
                ),
                "changed the frozen champion",
            )
        )
        for field_name in (
            "frozen_champion_equivalent",
            "historical_viewport_captures_available",
        ):
            mutations.append(
                (
                    f"experiment_control_{field_name}",
                    lambda manifest, field=field_name: manifest[
                        "experiment_control"
                    ].__setitem__(field, 0),
                    "synthetic experiment control",
                )
            )
        for field_name, expected in quality.EXPECTED_PREREQUISITE_REPAIRS[
            "frozen_champion_invariant_delta"
        ].items():
            mutations.append(
                (
                    f"prerequisite_{field_name}",
                    lambda manifest, field=field_name, value=int(expected): manifest[
                        "prerequisite_repairs"
                    ]["frozen_champion_invariant_delta"].__setitem__(field, value),
                    "prerequisite repairs changed",
                )
            )
        for field_name, expected in quality.EXPECTED_HARD_CONSTRAINTS.items():
            if type(expected) is bool:
                mutations.append(
                    (
                        f"hard_constraint_{field_name}",
                        lambda manifest, field=field_name, value=int(expected): (
                            manifest["hard_constraints"].__setitem__(field, value)
                        ),
                        "hard_constraints",
                    )
                )
        mutations.append(
            (
                "variant_scalar_non_string",
                lambda manifest: manifest["variants"]["labels_only"].__setitem__(
                    "label_source", 0
                ),
                "isolated variants changed",
            )
        )
        for label, mutate, message in mutations:
            broken = copy.deepcopy(self.ratchet_manifest)
            mutate(broken)
            with (
                self.subTest(label=label),
                patch.object(quality.scene_pipeline, "load_yaml", return_value=broken),
                self.assertRaisesRegex(quality.QualityError, message),
            ):
                quality.load_ratchet_manifest()

    def test_hard_constraints_are_exact_and_fail_closed(self) -> None:
        self.assertEqual(
            self.ratchet_manifest["hard_constraints"],
            quality.EXPECTED_HARD_CONSTRAINTS,
        )
        broken = copy.deepcopy(self.ratchet_manifest)
        broken["hard_constraints"]["unknowns_remain_unknown"] = False
        with (
            patch.object(quality.scene_pipeline, "load_yaml", return_value=broken),
            self.assertRaisesRegex(quality.QualityError, "hard_constraints"),
        ):
            quality.load_ratchet_manifest()

    def test_challenger_registry_must_exactly_match_modeled_variants(self) -> None:
        self.assertEqual(
            [
                candidate["candidate_id"]
                for candidate in self.ratchet_manifest["challenger_changes"]
            ],
            list(quality.EXPECTED_VARIANTS),
        )
        mutations = {}

        extra = copy.deepcopy(self.ratchet_manifest)
        extra_candidate = copy.deepcopy(extra["challenger_changes"][-1])
        extra_candidate["candidate_id"] = "unmodeled_candidate"
        extra["challenger_changes"].append(extra_candidate)
        mutations["extra"] = extra

        missing = copy.deepcopy(self.ratchet_manifest)
        missing["challenger_changes"].pop()
        mutations["missing"] = missing

        reordered = copy.deepcopy(self.ratchet_manifest)
        reordered["challenger_changes"][:2] = reversed(
            reordered["challenger_changes"][:2]
        )
        mutations["reordered"] = reordered

        for mutation, broken in mutations.items():
            with (
                self.subTest(mutation=mutation),
                patch.object(quality.scene_pipeline, "load_yaml", return_value=broken),
                self.assertRaisesRegex(
                    quality.QualityError,
                    "challenger change registry must exactly match",
                ),
            ):
                quality.load_ratchet_manifest()

    def test_challenger_dispositions_require_exact_generated_pareto_set(self) -> None:
        comparison = self.registry["ratchet"]
        current = quality._current_challenger_dispositions(
            self.registry["audit_program"],
            self.ratchet_manifest,
            comparison,
        )
        self.assertEqual(
            [record["candidate_id"] for record in current],
            list(quality.EXPECTED_VARIANTS),
        )
        self.assertEqual(
            [record["disposition"] for record in current],
            ["pending", "rejected", "pending"],
        )

        mutations = {}
        missing = copy.deepcopy(comparison)
        missing["pareto"]["evaluations"].pop()
        mutations["missing"] = missing

        extra = copy.deepcopy(comparison)
        extra_evaluation = copy.deepcopy(extra["pareto"]["evaluations"][-1])
        extra_evaluation["candidate_id"] = "unmodeled_candidate"
        extra["pareto"]["evaluations"].append(extra_evaluation)
        mutations["extra"] = extra

        reordered = copy.deepcopy(comparison)
        reordered["pareto"]["evaluations"][:2] = reversed(
            reordered["pareto"]["evaluations"][:2]
        )
        mutations["reordered"] = reordered

        for mutation, broken in mutations.items():
            with (
                self.subTest(mutation=mutation),
                self.assertRaisesRegex(
                    quality.QualityError,
                    "generated Pareto candidates must exactly match",
                ),
            ):
                quality._current_challenger_dispositions(
                    self.registry["audit_program"],
                    self.ratchet_manifest,
                    broken,
                )

    def _pareto_from_acceptance_candidate(self, acceptance_candidate: dict) -> dict:
        evaluation = copy.deepcopy(
            next(
                item
                for item in self.registry["ratchet"]["pareto"]["evaluations"]
                if item["candidate_id"] == acceptance_candidate["candidate_id"]
            )
        )
        candidate = evaluation["input"]["candidate"]
        candidate["static_gate_evidence"] = quality._pareto_gate_records(
            acceptance_candidate["static_gate_evidence"],
            quality.ratchet.STATIC_GATE_IDS,
        )
        candidate["live_gate_evidence"] = quality._pareto_gate_records(
            acceptance_candidate["live_gate_evidence"],
            quality.ratchet.LIVE_GATE_IDS,
        )
        candidate["blind_reviews"] = quality._pareto_blind_reviews(
            acceptance_candidate["blind_reviews"]
        )
        for gate in candidate["modeled_gate_evidence"].values():
            if gate["status"] == "pending":
                gate.update(
                    {
                        "status": "passed",
                        "evidence_ref": "hypothetical:modeled-gate-resolution",
                    }
                )
        return quality._pareto_decision_against_experiment_control(
            candidate,
            required_protection_members=evaluation["input"][
                "required_protection_members"
            ],
            required_modeled_gate_ids=evaluation["input"]["required_modeled_gate_ids"],
        )

    def _candidate_current_state(self, candidate_id: str) -> dict:
        challenger = next(
            record
            for record in self.registry["ratchet"]["challengers"]
            if record["id"] == candidate_id
        )
        return challenger["final_acceptance_evaluation"]["candidate_current_state"]

    def _resolved_acceptance_fixture(
        self, candidate_id: str = "labels_only"
    ) -> tuple[Path, dict, list[dict], dict]:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        current_state = self._candidate_current_state(candidate_id)
        evidence_ids = [
            "static:validation",
            "static:deterministic_generation",
            "static:evidence",
            "live:browser",
            "live:accessibility_snapshot",
            *(
                f"blind_review:{reviewer_id}"
                for reviewer_id in quality.BLIND_REVIEWER_IDS
            ),
            "final:prerequisite_correctness_repairs",
            "final:historical_frozen_champion_viewport_captures",
        ]
        placeholder_sha256 = {evidence_id: "0" * 64 for evidence_id in evidence_ids}
        record = _fully_resolved_acceptance_candidate(
            _acceptance_candidate(self.ratchet_manifest, candidate_id),
            current_state,
            report_artifact_sha256_by_evidence_id=placeholder_sha256,
        )
        report_inputs = []
        for domain, gates, digest_field in (
            ("static", record["static_gate_evidence"], "report_artifact_sha256"),
            ("live", record["live_gate_evidence"], "artifact_sha256"),
            (
                "final",
                record["final_independent_gate_evidence"],
                None,
            ),
        ):
            for gate_id, gate in gates.items():
                report_inputs.append(
                    {
                        "evidence_id": f"{domain}:{gate_id}",
                        "domain": domain,
                        "ref_id": gate_id,
                        "wrapper": gate,
                        "evidence": gate["evidence"],
                        "digest_field": digest_field
                        or (
                            "artifact_sha256"
                            if gate_id == "prerequisite_correctness_repairs"
                            else "capture_set_sha256"
                        ),
                        "outcome": gate["status"],
                    }
                )
        for review in record["blind_reviews"]:
            report_inputs.append(
                {
                    "evidence_id": f"blind_review:{review['reviewer_id']}",
                    "domain": "blind_review",
                    "ref_id": review["reviewer_id"],
                    "wrapper": review,
                    "evidence": review["evidence"],
                    "digest_field": "comparison_artifact_sha256",
                    "outcome": review["preference"],
                }
            )

        artifact_sha256_by_evidence_id = {}
        artifact_path_by_evidence_id = {}
        for report_input in report_inputs:
            evidence_id = report_input["evidence_id"]
            evidence = report_input["evidence"]
            digest_field = report_input["digest_field"]
            report_evidence = copy.deepcopy(evidence)
            report_evidence.pop(digest_field)
            envelope = {
                "schema_version": quality.SCHEMA_VERSION,
                "candidate_id": candidate_id,
                "candidate_current_state_sha256": current_state[
                    "candidate_current_state_sha256"
                ],
                "evidence_id": evidence_id,
                "outcome": report_input["outcome"],
                "typed_evidence": report_evidence,
            }
            artifact_path = (
                f"course/acceptance_evidence/{evidence_id.replace(':', '_')}.json"
            )
            retained = root / artifact_path
            retained.parent.mkdir(parents=True, exist_ok=True)
            retained.write_text(
                quality.scene_pipeline.canonical_payload(envelope) + "\n"
            )
            artifact_sha256 = hashlib.sha256(retained.read_bytes()).hexdigest()
            evidence[digest_field] = artifact_sha256
            wrapper = report_input["wrapper"]
            wrapper["evidence_ref"] = quality._acceptance_evidence_ref(
                candidate_id,
                record["candidate_provenance_sha256"],
                report_input["domain"],
                report_input["ref_id"],
                evidence,
            )
            artifact_sha256_by_evidence_id[evidence_id] = artifact_sha256
            artifact_path_by_evidence_id[evidence_id] = artifact_path
        artifacts = _acceptance_artifact_records(
            candidate_id,
            current_state,
            artifact_sha256_by_evidence_id,
            artifact_path_by_evidence_id,
        )
        return root, record, artifacts, current_state

    def _resolved_occupancy_fixture(
        self,
        status: str,
        *,
        candidate_id: str = "combined",
    ) -> tuple[Path, list[dict], dict, dict]:
        decision = {
            "live_approved": "approved",
            "live_rejected": "rejected",
        }[status]
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        root = Path(directory.name)
        current_state = self._candidate_current_state(candidate_id)
        review_sets, review_set = _copied_occupancy_reviews(
            self.ratchet_manifest, candidate_id
        )
        captures = []
        for index, record in enumerate(review_set["reviews"]):
            modeled_sha256 = quality._occupancy_modeled_evaluation_sha256(
                candidate_id,
                current_state["candidate_current_state_sha256"],
                record,
            )
            viewport = next(
                viewport
                for viewport in quality.VIEWPORTS
                if viewport["id"] == record["viewport_id"]
            )
            capture_bytes = _occupancy_capture_png(
                viewport["width"], viewport["height"], index + 1
            )
            artifact_sha256 = hashlib.sha256(capture_bytes).hexdigest()
            capture = {
                "candidate_id": candidate_id,
                "candidate_current_state_sha256": current_state[
                    "candidate_current_state_sha256"
                ],
                "validation_compiler_implementation_sha256": current_state[
                    "validation_compiler_implementation_sha256"
                ],
                "segment_id": record["segment_id"],
                "viewport_id": record["viewport_id"],
                "modeled_evaluation_sha256": modeled_sha256,
                "artifact_path": "",
                "artifact_sha256": artifact_sha256,
            }
            artifact_path = quality._canonical_occupancy_capture_path(capture)
            capture["artifact_path"] = artifact_path
            retained = root / artifact_path
            retained.parent.mkdir(parents=True, exist_ok=True)
            retained.write_bytes(capture_bytes)
            reviewer_id = f"reviewer-{index + 1}"
            reviewed_at = "2026-08-29T12:00:00-07:00"
            record["status"] = status
            record["live_review"] = {
                "decision": decision,
                "reviewer_id": reviewer_id,
                "reviewed_at": reviewed_at,
                "candidate_current_state_sha256": current_state[
                    "candidate_current_state_sha256"
                ],
                "validation_compiler_implementation_sha256": current_state[
                    "validation_compiler_implementation_sha256"
                ],
                "modeled_evaluation_sha256": modeled_sha256,
                "artifact_sha256": artifact_sha256,
                "evidence_ref": quality._occupancy_live_evidence_ref(
                    candidate_id,
                    review_set["candidate_provenance_sha256"],
                    candidate_current_state_sha256=current_state[
                        "candidate_current_state_sha256"
                    ],
                    validation_compiler_implementation_sha256=current_state[
                        "validation_compiler_implementation_sha256"
                    ],
                    segment_id=record["segment_id"],
                    viewport_id=record["viewport_id"],
                    modeled_evaluation_sha256=modeled_sha256,
                    decision=decision,
                    reviewer_id=reviewer_id,
                    reviewed_at=reviewed_at,
                    artifact_sha256=artifact_sha256,
                ),
            }
            captures.append(capture)
        return (
            root,
            review_sets,
            {
                "schema_version": quality.OCCUPANCY_CAPTURE_SCHEMA_VERSION,
                "captures": captures,
            },
            current_state,
        )

    def _retained_path_patch(self, root: Path):
        return patch.object(
            quality,
            "_retained_evidence_path",
            side_effect=lambda value, _location: root.joinpath(*Path(value).parts),
        )

    def _rewrite_acceptance_report(
        self,
        root: Path,
        record: dict,
        artifacts: list[dict],
        *,
        evidence_id: str,
        domain: str,
        ref_id: str,
        wrapper: dict,
        digest_field: str,
        outcome: str,
    ) -> None:
        evidence = wrapper["evidence"]
        report_evidence = copy.deepcopy(evidence)
        report_evidence.pop(digest_field)
        envelope = {
            "schema_version": quality.SCHEMA_VERSION,
            "candidate_id": record["candidate_id"],
            "candidate_current_state_sha256": evidence[
                "candidate_current_state_sha256"
            ],
            "evidence_id": evidence_id,
            "outcome": outcome,
            "typed_evidence": report_evidence,
        }
        artifact = next(
            item for item in artifacts if item["evidence_id"] == evidence_id
        )
        retained = root / artifact["artifact_path"]
        retained.write_text(quality.scene_pipeline.canonical_payload(envelope) + "\n")
        artifact_sha256 = hashlib.sha256(retained.read_bytes()).hexdigest()
        artifact["artifact_sha256"] = artifact_sha256
        evidence[digest_field] = artifact_sha256
        wrapper["evidence_ref"] = quality._acceptance_evidence_ref(
            record["candidate_id"],
            record["candidate_provenance_sha256"],
            domain,
            ref_id,
            evidence,
        )

    def test_current_acceptance_evidence_remains_truthfully_pending(self) -> None:
        self.assertEqual(
            [
                record["candidate_id"]
                for record in self.ratchet_manifest["acceptance"]["candidates"]
            ],
            list(quality.EXPECTED_VARIANTS),
        )
        for record in self.ratchet_manifest["acceptance"]["candidates"]:
            gates = [
                *record["static_gate_evidence"].values(),
                *record["live_gate_evidence"].values(),
                *record["final_independent_gate_evidence"].values(),
            ]
            self.assertTrue(
                all(
                    gate["status"] == "pending"
                    and gate["evidence_ref"] is None
                    and gate["evidence"] is None
                    for gate in gates
                )
            )
            current_state = self._candidate_current_state(record["candidate_id"])
            self.assertEqual(current_state["generated_artifact_count"], 16)
            self.assertEqual(
                current_state["generated_artifact_ids"],
                list(quality.ACCEPTANCE_GENERATED_ARTIFACT_IDS),
            )
            self.assertIn(
                "diagram/symbols.svg", current_state["generated_artifact_ids"]
            )
            self.assertEqual(
                [
                    item["artifact_id"]
                    for item in current_state["generated_artifact_state"]
                ],
                current_state["generated_artifact_ids"],
            )
            self.assertEqual(
                Counter(
                    item["evidence_basis"]
                    for item in current_state["generated_artifact_state"]
                ),
                {
                    "pure_expected_output_and_retained_byte_parity": 11,
                    "candidate_specific_pure_expected_output": 3,
                    "non_circular_in_memory_expected_projection": 2,
                },
            )
            candidate_artifacts = {
                record["artifact_id"]: record
                for record in current_state["candidate_course_artifact_retained_parity"]
            }
            self.assertEqual(
                list(candidate_artifacts),
                list(quality.generated_artifacts.CANDIDATE_COURSE_ARTIFACT_IDS),
            )
            self.assertEqual(
                current_state["candidate_course_artifact_mismatch_ids"],
                [
                    artifact_id
                    for artifact_id, artifact in candidate_artifacts.items()
                    if not artifact["retained_byte_parity"]
                ],
            )
            self.assertEqual(
                current_state["candidate_course_artifacts_materialized"],
                record["candidate_id"] == "combined",
            )
            if record["candidate_id"] == "combined":
                self.assertTrue(
                    all(
                        artifact["expected_output_sha256"]
                        == artifact["retained_output_sha256"]
                        for artifact in candidate_artifacts.values()
                    )
                )
            else:
                self.assertTrue(current_state["candidate_course_artifact_mismatch_ids"])
                self.assertTrue(
                    all(
                        candidate_artifacts[artifact_id]["expected_output_sha256"]
                        != candidate_artifacts[artifact_id]["retained_output_sha256"]
                        for artifact_id in current_state[
                            "candidate_course_artifact_mismatch_ids"
                        ]
                    )
                )
            self.assertNotIn(
                "current_retained_bytes", json.dumps(current_state, sort_keys=True)
            )
            self.assertEqual(
                current_state["validation_compiler_source_count"],
                len(current_state["validation_compiler_source_ids"]),
            )
            self.assertEqual(
                current_state["validation_compiler_source_ids"],
                [
                    path.relative_to(quality.ROOT).as_posix()
                    for path in quality.VALIDATION_COMPILER_IMPLEMENTATION_PATHS
                ],
            )
            self.assertTrue(
                all(
                    review["preference"] == "pending"
                    and review["evidence_ref"] is None
                    and review["evidence"] is None
                    for review in record["blind_reviews"]
                )
            )

        for evaluation in self.registry["ratchet"]["pareto"]["evaluations"]:
            source = _acceptance_candidate(
                self.ratchet_manifest, evaluation["candidate_id"]
            )
            self.assertEqual(
                evaluation["input"]["acceptance_evidence"],
                source,
            )
            self.assertTrue(
                all(
                    gate["status"] == "pending"
                    for gate in evaluation["input"]["candidate"][
                        "static_gate_evidence"
                    ].values()
                )
            )

    def test_nonmaterialized_fully_resolved_candidate_cannot_be_accepted(self) -> None:
        root, resolved, artifacts, current_state = self._resolved_acceptance_fixture()
        hypothetical = copy.deepcopy(self.ratchet_manifest)
        source_record = _acceptance_candidate(hypothetical, "labels_only")
        source_record.clear()
        source_record.update(resolved)
        hypothetical["acceptance_artifacts"] = artifacts
        with (
            self._retained_path_patch(root),
            patch.object(
                quality.scene_pipeline,
                "load_yaml",
                return_value=hypothetical,
            ),
        ):
            loaded = quality.load_ratchet_manifest()
        loaded_record = _acceptance_candidate(loaded, "labels_only")
        pareto_result = self._pareto_from_acceptance_candidate(loaded_record)
        self.assertEqual(pareto_result["disposition"], "accepted")
        with self._retained_path_patch(root):
            result = quality._final_acceptance_evaluation(
                pareto_result,
                loaded_record,
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
            )
        self.assertEqual(result["status"], "pending")
        self.assertEqual(result["manifest_gate_status"], "passed")
        self.assertEqual(result["evidence_final_status"], "accepted")
        self.assertEqual(result["reasons"], ["candidate_artifacts:not_materialized"])
        self.assertEqual(result["candidate_artifact_materialization_status"], "pending")
        self.assertTrue(result["candidate_artifact_mismatch_ids"])
        self.assertFalse(result["promotion_eligible"])
        self.assertEqual(
            list(result["gate_evidence"]),
            list(quality.FINAL_ACCEPTANCE_GATE_IDS),
        )

    def test_materialized_combined_candidate_retains_valid_acceptance_path(
        self,
    ) -> None:
        root, resolved, artifacts, current_state = self._resolved_acceptance_fixture(
            "combined"
        )
        pareto_result = self._pareto_from_acceptance_candidate(resolved)
        self.assertEqual(pareto_result["disposition"], "accepted")
        with self._retained_path_patch(root):
            result = quality._final_acceptance_evaluation(
                pareto_result,
                resolved,
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
            )
        self.assertEqual(result["status"], "accepted")
        self.assertEqual(result["manifest_gate_status"], "passed")
        self.assertEqual(result["evidence_final_status"], "accepted")
        self.assertEqual(
            result["candidate_artifact_materialization_status"], "materialized"
        )
        self.assertEqual(result["candidate_artifact_mismatch_ids"], [])
        self.assertTrue(result["promotion_eligible"])
        self.assertEqual(result["reasons"], [])
        self.assertEqual(
            list(result["gate_evidence"]),
            list(quality.FINAL_ACCEPTANCE_GATE_IDS),
        )

    def test_acceptance_rejects_coordinated_fake_current_state_reports(self) -> None:
        mutations = (
            (
                "repeated_source_hashes",
                "validation",
                {
                    "source_digest_sha256": "1" * 64,
                    "runtime_output_sha256": "2" * 64,
                    "modeled_quality_output_sha256": "3" * 64,
                },
                "current compiler state",
            ),
            (
                "one_artifact",
                "deterministic_generation",
                {
                    "artifact_count": 1,
                    "artifact_ids": ["diagram/fake.txt"],
                    "artifact_inventory_sha256": "4" * 64,
                    "artifact_set_sha256": "5" * 64,
                },
                "current inventory",
            ),
            (
                "one_ledger_source_fact",
                "evidence",
                {
                    "ledger_ids": ["fake"],
                    "ledger_count": 1,
                    "source_count": 1,
                    "fact_count": 1,
                    "evidence_inventory_sha256": "6" * 64,
                },
                "current evidence inventory",
            ),
        )
        for label, gate_id, changed_fields, message in mutations:
            with self.subTest(label=label):
                root, record, artifacts, current_state = (
                    self._resolved_acceptance_fixture()
                )
                gate = record["static_gate_evidence"][gate_id]
                evidence = {**gate["evidence"], **changed_fields}
                _resolve_gate(
                    gate,
                    candidate_id=record["candidate_id"],
                    provenance_sha256=record["candidate_provenance_sha256"],
                    domain="static",
                    evidence_id=gate_id,
                    evidence=evidence,
                    status="passed",
                )
                self._rewrite_acceptance_report(
                    root,
                    record,
                    artifacts,
                    evidence_id=f"static:{gate_id}",
                    domain="static",
                    ref_id=gate_id,
                    wrapper=gate,
                    digest_field="report_artifact_sha256",
                    outcome="passed",
                )
                with (
                    self._retained_path_patch(root),
                    self.assertRaisesRegex(quality.QualityError, message),
                ):
                    quality._validate_candidate_acceptance_evidence(
                        record,
                        candidate_id=record["candidate_id"],
                        provenance_sha256=record["candidate_provenance_sha256"],
                        expected_current_state=current_state,
                        acceptance_artifacts=artifacts,
                        location="coordinated_fake",
                    )

    def test_acceptance_rejects_opaque_or_noncanonical_report_bytes(self) -> None:
        root, record, artifacts, current_state = self._resolved_acceptance_fixture()
        gate = record["static_gate_evidence"]["validation"]
        artifact = next(
            item for item in artifacts if item["evidence_id"] == "static:validation"
        )
        retained = root / artifact["artifact_path"]
        retained.write_bytes(b"")
        blank_sha256 = hashlib.sha256(b"").hexdigest()
        artifact["artifact_sha256"] = blank_sha256
        evidence = {**gate["evidence"], "report_artifact_sha256": blank_sha256}
        _resolve_gate(
            gate,
            candidate_id=record["candidate_id"],
            provenance_sha256=record["candidate_provenance_sha256"],
            domain="static",
            evidence_id="validation",
            evidence=evidence,
            status="passed",
        )
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(quality.QualityError, "not valid JSON"),
        ):
            quality._validate_candidate_acceptance_evidence(
                record,
                candidate_id=record["candidate_id"],
                provenance_sha256=record["candidate_provenance_sha256"],
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
                location="opaque_report",
            )

    def test_candidate_content_change_stales_acceptance_and_occupancy(self) -> None:
        modeled_quality = copy.deepcopy(self.registry)
        modeled_quality.pop("audit_program")
        modeled_quality.pop("ratchet")
        candidate_id = "combined"
        challenger = next(
            item
            for item in self.ratchet_manifest["challenger_changes"]
            if item["candidate_id"] == candidate_id
        )
        provenance = quality._candidate_acceptance_provenance(
            self.ratchet_manifest, challenger
        )
        baseline_state = quality._candidate_current_state(
            candidate_id=candidate_id,
            candidate_provenance_sha256=provenance,
            runtime_registry=self.runtime,
            quality_registry=modeled_quality,
            ledgers=self.ledgers,
        )
        self.assertEqual(
            baseline_state,
            self._candidate_current_state(candidate_id),
        )
        mutated_runtime = copy.deepcopy(self.runtime)
        mutated_runtime["segments"][0]["opening_question"] += " Content-only mutation."
        mutated_state = quality._candidate_current_state(
            candidate_id=candidate_id,
            candidate_provenance_sha256=provenance,
            runtime_registry=mutated_runtime,
            quality_registry=modeled_quality,
            ledgers=self.ledgers,
        )
        self.assertNotEqual(
            baseline_state["runtime_output_sha256"],
            mutated_state["runtime_output_sha256"],
        )
        self.assertEqual(
            baseline_state["modeled_quality_output_sha256"],
            mutated_state["modeled_quality_output_sha256"],
        )

        root, record, artifacts, _old_state = self._resolved_acceptance_fixture(
            candidate_id
        )
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(
                quality.QualityError, "current-state provenance is stale"
            ),
        ):
            quality._validate_candidate_acceptance_evidence(
                record,
                candidate_id=candidate_id,
                provenance_sha256=provenance,
                expected_current_state=mutated_state,
                acceptance_artifacts=artifacts,
                location="content_mutation",
            )

        capture_root, review_sets, captures, _capture_state = (
            self._resolved_occupancy_fixture("live_approved", candidate_id=candidate_id)
        )
        with self._retained_path_patch(capture_root):
            gate = quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                candidate_id=candidate_id,
                expected_current_state=mutated_state,
                capture_manifest=captures,
            )
        self.assertEqual(gate["status"], "failed")
        self.assertTrue(
            any(
                "candidate_current_state_is_stale" in record["reasons"]
                for record in gate["malformed_reviews"]
            )
        )
        self.assertTrue(
            any(
                "canonical_capture_manifest_entry_is_unconsumed" in record["reasons"]
                for record in gate["malformed_reviews"]
            )
        )

    def test_candidate_current_state_rejects_stale_materialized_output(self) -> None:
        target = (quality.ROOT / "diagram/course.html").resolve()
        read_bytes = Path.read_bytes

        def stale_reader(path: Path) -> bytes:
            payload = read_bytes(path)
            return (
                payload + b"\n<!-- stale -->\n" if path.resolve() == target else payload
            )

        with (
            patch.object(Path, "read_bytes", stale_reader),
            self.assertRaisesRegex(
                quality.QualityError, "^diagram/course.html is stale"
            ),
        ):
            quality._materialized_acceptance_artifact_state()

    def test_candidate_current_state_binds_compiler_implementation(self) -> None:
        modeled_quality = copy.deepcopy(self.registry)
        modeled_quality.pop("audit_program")
        modeled_quality.pop("ratchet")
        candidate_id = "combined"
        challenger = next(
            item
            for item in self.ratchet_manifest["challenger_changes"]
            if item["candidate_id"] == candidate_id
        )
        provenance = quality._candidate_acceptance_provenance(
            self.ratchet_manifest, challenger
        )
        materialized_state = quality._materialized_acceptance_artifact_state()
        baseline = quality._candidate_current_state(
            candidate_id=candidate_id,
            candidate_provenance_sha256=provenance,
            runtime_registry=self.runtime,
            quality_registry=modeled_quality,
            ledgers=self.ledgers,
            materialized_artifact_state=materialized_state,
        )
        implementation = quality._validation_compiler_implementation_state()
        changed_implementation = {
            **implementation,
            "source_sha256": (
                "0" * 64 if implementation["source_sha256"] != "0" * 64 else "1" * 64
            ),
        }
        with patch.object(
            quality,
            "_validation_compiler_implementation_state",
            return_value=changed_implementation,
        ):
            changed = quality._candidate_current_state(
                candidate_id=candidate_id,
                candidate_provenance_sha256=provenance,
                runtime_registry=self.runtime,
                quality_registry=modeled_quality,
                ledgers=self.ledgers,
                materialized_artifact_state=materialized_state,
            )
        self.assertNotEqual(
            baseline["validation_compiler_implementation_sha256"],
            changed["validation_compiler_implementation_sha256"],
        )
        self.assertNotEqual(
            baseline["candidate_current_state_sha256"],
            changed["candidate_current_state_sha256"],
        )
        for field in (
            "candidate_source_digest_sha256",
            "runtime_output_sha256",
            "modeled_quality_output_sha256",
            "generated_artifact_set_sha256",
            "evidence_inventory_sha256",
        ):
            self.assertEqual(baseline[field], changed[field])

        root, record, artifacts, _current_state = self._resolved_acceptance_fixture(
            candidate_id
        )
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(
                quality.QualityError, "current-state provenance is stale"
            ),
        ):
            quality._validate_candidate_acceptance_evidence(
                record,
                candidate_id=candidate_id,
                provenance_sha256=provenance,
                expected_current_state=changed,
                acceptance_artifacts=artifacts,
                location="compiler_implementation_change",
            )

        capture_root, review_sets, captures, _old_state = (
            self._resolved_occupancy_fixture("live_approved", candidate_id=candidate_id)
        )
        with self._retained_path_patch(capture_root):
            gate = quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                candidate_id=candidate_id,
                expected_current_state=changed,
                capture_manifest=captures,
            )
        self.assertEqual(gate["status"], "failed")
        self.assertTrue(
            any(
                "candidate_current_state_is_stale" in malformed["reasons"]
                for malformed in gate["malformed_reviews"]
            )
        )
        self.assertTrue(
            any(
                "compiler_implementation_is_stale" in malformed["reasons"]
                for malformed in gate["malformed_reviews"]
            )
        )

    def test_every_validation_compiler_source_changes_implementation_digest(
        self,
    ) -> None:
        baseline = quality._validation_compiler_implementation_state()
        read_bytes = Path.read_bytes
        for target in quality.VALIDATION_COMPILER_IMPLEMENTATION_PATHS:
            target = target.resolve()

            def changed_reader(path: Path, *, changed_target: Path = target) -> bytes:
                payload = read_bytes(path)
                return (
                    payload + b"\n# source-only mutation\n"
                    if path.resolve() == changed_target
                    else payload
                )

            with self.subTest(source=target.relative_to(quality.ROOT).as_posix()):
                with patch.object(Path, "read_bytes", changed_reader):
                    changed = quality._validation_compiler_implementation_state()
                self.assertEqual(changed["source_ids"], baseline["source_ids"])
                self.assertEqual(changed["source_count"], baseline["source_count"])
                self.assertNotEqual(changed["source_sha256"], baseline["source_sha256"])

    def test_typed_gate_failure_rejects_candidate(self) -> None:
        root, record, artifacts, current_state = self._resolved_acceptance_fixture()
        gate = record["static_gate_evidence"]["validation"]
        evidence = {**gate["evidence"], "exit_code": 1}
        _resolve_gate(
            gate,
            candidate_id=record["candidate_id"],
            provenance_sha256=record["candidate_provenance_sha256"],
            domain="static",
            evidence_id="validation",
            evidence=evidence,
            status="failed",
        )
        self._rewrite_acceptance_report(
            root,
            record,
            artifacts,
            evidence_id="static:validation",
            domain="static",
            ref_id="validation",
            wrapper=gate,
            digest_field="report_artifact_sha256",
            outcome="failed",
        )
        with self._retained_path_patch(root):
            quality._validate_candidate_acceptance_evidence(
                record,
                candidate_id=record["candidate_id"],
                provenance_sha256=record["candidate_provenance_sha256"],
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
                location="test_candidate",
            )
        pareto_result = self._pareto_from_acceptance_candidate(record)
        self.assertEqual(pareto_result["disposition"], "rejected")
        with self._retained_path_patch(root):
            result = quality._final_acceptance_evaluation(
                pareto_result,
                record,
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
            )
        self.assertEqual(result["status"], "rejected")
        self.assertIn("pareto:rejected", result["reasons"])

    def test_acceptance_candidate_identity_set_and_order_fail_closed(self) -> None:
        mutations = {}
        missing = copy.deepcopy(self.ratchet_manifest)
        missing["acceptance"]["candidates"].pop()
        mutations["missing"] = missing
        extra = copy.deepcopy(self.ratchet_manifest)
        extra["acceptance"]["candidates"].append(
            copy.deepcopy(extra["acceptance"]["candidates"][-1])
        )
        mutations["extra"] = extra
        reordered = copy.deepcopy(self.ratchet_manifest)
        reordered["acceptance"]["candidates"][:2] = reversed(
            reordered["acceptance"]["candidates"][:2]
        )
        mutations["reordered"] = reordered
        for label, manifest in mutations.items():
            with (
                self.subTest(label=label),
                patch.object(
                    quality.scene_pipeline, "load_yaml", return_value=manifest
                ),
                self.assertRaisesRegex(
                    quality.QualityError,
                    "acceptance candidate IDs must exactly match",
                ),
            ):
                quality.load_ratchet_manifest()

    def test_acceptance_refs_and_typed_evidence_fail_closed(self) -> None:
        root, base, artifacts, current_state = self._resolved_acceptance_fixture()
        mutations = []

        wrong_candidate = copy.deepcopy(base)
        wrong_candidate["static_gate_evidence"]["validation"]["evidence"][
            "candidate_id"
        ] = "combined"
        mutations.append(("candidate", wrong_candidate, "candidate binding"))

        wrong_provenance = copy.deepcopy(base)
        wrong_provenance["live_gate_evidence"]["browser"]["evidence"][
            "candidate_provenance_sha256"
        ] = "f" * 64
        mutations.append(("provenance", wrong_provenance, "provenance is stale"))

        wrong_domain = copy.deepcopy(base)
        gate = wrong_domain["static_gate_evidence"]["validation"]
        gate["evidence_ref"] = gate["evidence_ref"].replace(
            "/static/validation/", "/live/validation/"
        )
        mutations.append(("domain", wrong_domain, "malformed, stale, or misbound"))

        stale_ref = copy.deepcopy(base)
        stale_ref["static_gate_evidence"]["validation"]["evidence"][
            "source_digest_sha256"
        ] = "e" * 64
        mutations.append(("stale", stale_ref, "does not match current compiler state"))

        partial = copy.deepcopy(base)
        browser = partial["live_gate_evidence"]["browser"]
        browser_evidence = {**browser["evidence"], "evaluation_count": 129}
        _resolve_gate(
            browser,
            candidate_id=partial["candidate_id"],
            provenance_sha256=partial["candidate_provenance_sha256"],
            domain="live",
            evidence_id="browser",
            evidence=browser_evidence,
            status="passed",
        )
        mutations.append(("partial", partial, "evaluation_count is incomplete"))

        for label, record, message in mutations:
            with (
                self.subTest(label=label),
                self._retained_path_patch(root),
                self.assertRaisesRegex(quality.QualityError, message),
            ):
                quality._validate_candidate_acceptance_evidence(
                    record,
                    candidate_id=base["candidate_id"],
                    provenance_sha256=base["candidate_provenance_sha256"],
                    expected_current_state=current_state,
                    acceptance_artifacts=artifacts,
                    location="test_candidate",
                )

    def test_blind_review_identity_preference_and_count_fail_closed(self) -> None:
        base = copy.deepcopy(
            _acceptance_candidate(self.ratchet_manifest, "labels_only")
        )
        mutations = []
        missing = copy.deepcopy(base)
        missing["blind_reviews"].pop()
        mutations.append(missing)
        duplicate = copy.deepcopy(base)
        duplicate["blind_reviews"][1]["reviewer_id"] = "blind_reviewer_1"
        mutations.append(duplicate)
        reordered = copy.deepcopy(base)
        reordered["blind_reviews"][:2] = reversed(reordered["blind_reviews"][:2])
        mutations.append(reordered)
        invalid_preference = copy.deepcopy(base)
        invalid_preference["blind_reviews"][0]["preference"] = "preferred"
        mutations.append(invalid_preference)
        nonblind = copy.deepcopy(base)
        nonblind["blind_reviews"][0]["blind"] = False
        mutations.append(nonblind)
        for record in mutations:
            with self.assertRaises(quality.QualityError):
                quality._validate_candidate_acceptance_evidence(
                    record,
                    candidate_id=base["candidate_id"],
                    provenance_sha256=base["candidate_provenance_sha256"],
                    location="test_candidate",
                )

    def test_illegal_gate_status_and_evidence_combinations_fail_closed(self) -> None:
        base = copy.deepcopy(
            _acceptance_candidate(self.ratchet_manifest, "labels_only")
        )
        pending_with_ref = copy.deepcopy(base)
        pending_with_ref["static_gate_evidence"]["validation"]["evidence_ref"] = (
            "forged"
        )
        resolved_without_evidence = copy.deepcopy(base)
        resolved_without_evidence["static_gate_evidence"]["validation"]["status"] = (
            "passed"
        )
        root, outcome_mismatch, artifacts, current_state = (
            self._resolved_acceptance_fixture()
        )
        validation = outcome_mismatch["static_gate_evidence"]["validation"]
        failed_evidence = {**validation["evidence"], "exit_code": 1}
        _resolve_gate(
            validation,
            candidate_id=base["candidate_id"],
            provenance_sha256=base["candidate_provenance_sha256"],
            domain="static",
            evidence_id="validation",
            evidence=failed_evidence,
            status="passed",
        )
        for record in (
            pending_with_ref,
            resolved_without_evidence,
            outcome_mismatch,
        ):
            with (
                self._retained_path_patch(root),
                self.assertRaises(quality.QualityError),
            ):
                quality._validate_candidate_acceptance_evidence(
                    record,
                    candidate_id=base["candidate_id"],
                    provenance_sha256=base["candidate_provenance_sha256"],
                    expected_current_state=current_state,
                    acceptance_artifacts=artifacts,
                    location="test_candidate",
                )

    def test_final_acceptance_rejects_forged_or_cross_candidate_state(self) -> None:
        root, resolved, artifacts, current_state = self._resolved_acceptance_fixture()
        accepted_pareto = self._pareto_from_acceptance_candidate(resolved)

        forged_status = copy.deepcopy(resolved)
        forged_status["final_status"] = "accepted"
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(quality.QualityError, "fields must be exact"),
        ):
            quality._final_acceptance_evaluation(
                accepted_pareto,
                forged_status,
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
            )

        pending_evidence = _acceptance_candidate(self.ratchet_manifest, "labels_only")
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(
                quality.QualityError,
                "Pareto state must match supplied candidate evidence",
            ),
        ):
            quality._final_acceptance_evaluation(
                accepted_pareto,
                pending_evidence,
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
            )

        cross_candidate = copy.deepcopy(resolved)
        cross_candidate["candidate_id"] = "combined"
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(quality.QualityError, "candidate identity"),
        ):
            quality._final_acceptance_evaluation(
                accepted_pareto,
                cross_candidate,
                expected_current_state=current_state,
                acceptance_artifacts=artifacts,
            )

    def test_change_ownership_registry_rejects_adversarial_links(self) -> None:
        mutations = []

        owner_html = copy.deepcopy(self.ratchet_manifest)
        owner_html["change_owners"][0]["source_paths"].append("diagram/course.html")
        mutations.append(("owner_html", owner_html, "must not own generated HTML"))

        change_html = copy.deepcopy(self.ratchet_manifest)
        change_html["changes"][0]["source_paths"].append("diagram/course.html")
        mutations.append(
            ("change_html", change_html, "must not include generated HTML")
        )

        incompatible_path = copy.deepcopy(self.ratchet_manifest)
        focus_change = next(
            change
            for change in incompatible_path["changes"]
            if change["change_id"] == "CHANGE-FOCUS-LABELS"
        )
        focus_change["source_paths"] = ["course/segments.yaml"]
        mutations.append(
            (
                "incompatible_path",
                incompatible_path,
                "source paths must be compatible with linked owners",
            )
        )

        owner_mismatch = copy.deepcopy(self.ratchet_manifest)
        focus_change = next(
            change
            for change in owner_mismatch["changes"]
            if change["change_id"] == "CHANGE-FOCUS-LABELS"
        )
        focus_change["change_owner_ids"].append("OWNER-SEGMENT-AUTHORING")
        mutations.append(
            (
                "owner_mismatch",
                owner_mismatch,
                "change_owner_ids must exactly match finding owners",
            )
        )

        duplicate_finding = copy.deepcopy(self.ratchet_manifest)
        annotation_change = next(
            change
            for change in duplicate_finding["changes"]
            if change["change_id"] == "CHANGE-SEMANTIC-OVERLAYS"
        )
        annotation_change["finding_ids"].append("VIS-LABEL-01")
        mutations.append(
            (
                "duplicate_finding",
                duplicate_finding,
                "finding/change links must be exact and one-to-one",
            )
        )

        for mutation, broken, error_pattern in mutations:
            with (
                self.subTest(mutation=mutation),
                patch.object(quality.scene_pipeline, "load_yaml", return_value=broken),
                self.assertRaisesRegex(quality.QualityError, error_pattern),
            ):
                quality.load_ratchet_manifest()

    def test_isolated_challengers_use_their_intended_target_dimensions(self) -> None:
        ratchet = self.registry["ratchet"]
        self.assertEqual(
            ratchet["comparison_mode"], "modeled_on_corrected_candidate_base"
        )
        self.assertEqual(ratchet["hypothesis"], quality.RATCHET_HYPOTHESIS)
        self.assertEqual(
            ratchet["protected_sentinel_ids"],
            list(quality.PROTECTED_DENSE_SEGMENTS),
        )
        self.assertEqual(ratchet["acceptance"], self.ratchet_manifest["acceptance"])
        self.assertEqual(
            ratchet["prerequisite_repairs"],
            quality.EXPECTED_PREREQUISITE_REPAIRS,
        )
        self.assertEqual(len(ratchet["acceptance"]["candidates"]), 3)
        self.assertTrue(ratchet["acceptance"]["modeled_eligibility_only"])

        experiment_control = ratchet["experiment_control"]
        self.assertFalse(experiment_control["modeled_eligible"])
        self.assertEqual(experiment_control["role"], "experiment_control")
        self.assertEqual(experiment_control["pareto_disposition"], "not_applicable")
        self.assertEqual(experiment_control["final_acceptance"], "not_applicable")
        self.assertIsNone(experiment_control["final_acceptance_evaluation"])
        self.assertTrue(
            all(
                not gate["passed"]
                for gate in experiment_control["targeted_gates"].values()
            )
        )
        self.assertTrue(
            experiment_control["layout_gates"][
                "annotated_two_dimensional_physical_composition"
            ]["passed"]
        )
        control_three_composition = experiment_control["layout_gates"][
            "annotated_three_dimensional_physical_composition"
        ]
        self.assertTrue(control_three_composition["passed"])
        self.assertEqual(control_three_composition["evaluation_count"], 0)
        control_portrait = experiment_control["layout_gates"][
            "portrait_focus_key_complete_visibility"
        ]
        self.assertTrue(control_portrait["passed"])
        self.assertEqual(control_portrait["status"], "not_applicable")
        self.assertEqual(control_portrait["focus_policy_segment_count"], 0)
        self.assertEqual(
            control_portrait["not_applicable_segment_count"],
            course_runtime.EXPECTED_SEGMENTS,
        )
        control_clearance = experiment_control["layout_gates"][
            "teaching_overlay_stage_edge_clearance"
        ]
        self.assertTrue(control_clearance["passed"])
        self.assertEqual(control_clearance["status"], "not_applicable")
        self.assertEqual(control_clearance["annotated_segment_count"], 0)
        self.assertEqual(control_clearance["evaluation_count"], 0)
        challengers = {item["id"]: item for item in ratchet["challengers"]}
        for result in (experiment_control, *ratchet["challengers"]):
            for gate_id in (
                "overlay_residual_label_collision",
                "overlay_suppression_focus_key_coverage",
                "overlay_clipping",
                "two_dimensional_label_clipping",
                "three_dimensional_point_clipping",
            ):
                gate = result["layout_gates"][gate_id]
                self.assertEqual(gate["scope"], "all_segments_all_viewports")
                self.assertEqual(gate["segment_count"], 26)
                self.assertEqual(gate["viewport_count"], 5)
                self.assertEqual(gate["evaluation_count"], 130)
        expected_gates = {
            "labels_only": {
                "label_pressure": True,
                "dense_annotation_gap": False,
            },
            "annotations_only": {
                "label_pressure": False,
                "dense_annotation_gap": True,
            },
            "combined": {
                "label_pressure": True,
                "dense_annotation_gap": True,
            },
        }
        expected_non_regressions = {
            "labels_only": {"risk_flags": 0, "metrics": 0, "evaluations": 0},
            "annotations_only": {"risk_flags": 0, "metrics": 0, "evaluations": 0},
            "combined": {"risk_flags": 0, "metrics": 0, "evaluations": 0},
        }
        expected_target_gate_ids = {
            "labels_only": ["label_pressure"],
            "annotations_only": ["dense_annotation_gap"],
            "combined": ["label_pressure", "dense_annotation_gap"],
        }
        expected_pareto_dispositions = {
            "labels_only": "pending",
            "annotations_only": "rejected",
            "combined": "pending",
        }
        expected_final_acceptance = {
            "labels_only": "pending",
            "annotations_only": "rejected",
            "combined": "pending",
        }
        expected_modeled_statuses = {
            "labels_only": "pending",
            "annotations_only": "failed",
            "combined": "pending",
        }
        for variant_id, gates in expected_gates.items():
            challenger = challengers[variant_id]
            self.assertEqual(
                {
                    gate_id: gate["passed"]
                    for gate_id, gate in challenger["targeted_gates"].items()
                },
                gates,
            )
            self.assertEqual(
                challenger["target_gate_ids"],
                expected_target_gate_ids[variant_id],
            )
            self.assertTrue(
                all(
                    challenger["targeted_gates"][gate_id]["passed"]
                    for gate_id in challenger["target_gate_ids"]
                )
            )
            self.assertFalse(challenger["modeled_eligible"])
            self.assertEqual(
                challenger["modeled_gate_status"],
                expected_modeled_statuses[variant_id],
            )
            self.assertEqual(
                challenger["pareto_disposition"],
                expected_pareto_dispositions[variant_id],
            )
            self.assertEqual(
                challenger["final_acceptance"],
                expected_final_acceptance[variant_id],
            )
            final_evaluation = challenger["final_acceptance_evaluation"]
            self.assertEqual(
                set(final_evaluation),
                {
                    "candidate_id",
                    "candidate_provenance_sha256",
                    "candidate_current_state_sha256",
                    "candidate_current_state",
                    "status",
                    "pareto_disposition",
                    "manifest_gate_status",
                    "evidence_final_status",
                    "candidate_artifact_materialization_status",
                    "candidate_artifact_mismatch_ids",
                    "promotion_eligible",
                    "required_gate_ids",
                    "gate_evidence",
                    "reasons",
                },
            )
            self.assertEqual(final_evaluation["candidate_id"], variant_id)
            self.assertEqual(
                final_evaluation["pareto_disposition"],
                expected_pareto_dispositions[variant_id],
            )
            self.assertEqual(
                final_evaluation["status"],
                expected_final_acceptance[variant_id],
            )
            self.assertEqual(final_evaluation["manifest_gate_status"], "pending")
            self.assertEqual(final_evaluation["evidence_final_status"], "pending")
            self.assertEqual(
                final_evaluation["required_gate_ids"],
                list(quality.FINAL_ACCEPTANCE_GATE_IDS),
            )
            self.assertEqual(
                final_evaluation["gate_evidence"],
                quality._derived_final_gate_evidence(
                    _acceptance_candidate(self.ratchet_manifest, variant_id)
                ),
            )
            non_regression = challenger["layout_gates"][
                "all_section_risk_non_regression"
            ]
            self.assertEqual(
                non_regression["passed"],
                not any(expected_non_regressions[variant_id].values()),
            )
            self.assertEqual(
                {
                    "risk_flags": non_regression["risk_flag_regression_count"],
                    "metrics": non_regression["metric_regression_count"],
                    "evaluations": non_regression["regression_count"],
                },
                expected_non_regressions[variant_id],
            )
            self.assertTrue(
                challenger["layout_gates"][
                    "annotated_two_dimensional_physical_composition"
                ]["passed"]
            )
            self.assertTrue(
                challenger["layout_gates"][
                    "annotated_three_dimensional_physical_composition"
                ]["passed"]
            )
            self.assertTrue(challenger["invariants_unchanged_from_experiment_base"])
            self.assertEqual(
                challenger["invariant_digests"],
                ratchet["experiment_base_invariant_digests"],
            )
            portrait = challenger["layout_gates"][
                "portrait_focus_key_complete_visibility"
            ]
            if variant_id == "annotations_only":
                self.assertEqual(portrait["status"], "not_applicable")
                self.assertEqual(portrait["focus_policy_segment_count"], 0)
            else:
                self.assertEqual(portrait["status"], "passed")
                self.assertEqual(
                    portrait["focus_policy_segment_count"],
                    course_runtime.EXPECTED_SEGMENTS,
                )
            clearance = challenger["layout_gates"][
                "teaching_overlay_stage_edge_clearance"
            ]
            if variant_id == "labels_only":
                self.assertTrue(clearance["passed"])
                self.assertEqual(clearance["status"], "not_applicable")
                self.assertEqual(clearance["evaluation_count"], 0)
            else:
                self.assertTrue(clearance["passed"], clearance["failures"])
                self.assertEqual(clearance["status"], "passed")
                self.assertEqual(clearance["evaluation_count"], 80)

        combined = challengers["combined"]
        self.assertEqual(
            [
                gate_id
                for gate_id, gate in combined["layout_gates"].items()
                if not gate["passed"]
            ],
            ["occupancy_review"],
        )
        self.assertEqual(
            combined["layout_gates"]["occupancy_review"]["status"], "pending"
        )
        self.assertEqual(
            {
                record["metric_id"]
                for record in combined["layout_gates"][
                    "all_section_risk_non_regression"
                ]["metric_regressions"]
            },
            set(),
        )

    def test_course_objective_invariant_covers_every_act_objective(self) -> None:
        baseline = quality._invariant_digests(self.runtime)
        baseline_objectives = baseline["course_objectives"]
        act_ids = list(
            dict.fromkeys(segment["act_id"] for segment in self.runtime["segments"])
        )
        self.assertEqual(len(act_ids), course_runtime.EXPECTED_ACTS)

        for act_id in act_ids:
            with self.subTest(act_id=act_id):
                mutated = copy.deepcopy(self.runtime)
                matched = 0
                for segment in mutated["segments"]:
                    if segment["act_id"] == act_id:
                        segment["act_objective"] += " [objective mutation]"
                        matched += 1
                self.assertGreater(matched, 0)
                mutated_digests = quality._invariant_digests(mutated)
                self.assertNotEqual(
                    mutated_digests["course_objectives"],
                    baseline_objectives,
                )
                self.assertEqual(
                    {
                        key: value
                        for key, value in mutated_digests.items()
                        if key != "course_objectives"
                    },
                    {
                        key: value
                        for key, value in baseline.items()
                        if key != "course_objectives"
                    },
                )

    def test_course_objective_invariant_payload_has_exact_runtime_coverage(
        self,
    ) -> None:
        payload = quality._objective_invariant_payload(self.runtime["segments"])
        self.assertEqual(len(payload), course_runtime.EXPECTED_SEGMENTS)
        self.assertEqual(
            [record["segment_id"] for record in payload],
            [segment["segment_id"] for segment in self.runtime["segments"]],
        )
        self.assertEqual(
            len({record["act_id"] for record in payload}),
            course_runtime.EXPECTED_ACTS,
        )
        for index, record in enumerate(payload):
            self.assertEqual(
                set(record),
                {
                    "segment_id",
                    "act_id",
                    "act_objective",
                    "learning_objective",
                },
            )
            self.assertEqual(
                record,
                {field: self.runtime["segments"][index][field] for field in record},
            )

    def test_course_objective_invariant_covers_all_segment_objectives(self) -> None:
        baseline = quality._invariant_digests(self.runtime)
        baseline_objectives = baseline["course_objectives"]
        self.assertEqual(
            len(self.runtime["segments"]),
            course_runtime.EXPECTED_SEGMENTS,
        )

        for index, segment in enumerate(self.runtime["segments"]):
            with self.subTest(segment_id=segment["segment_id"]):
                mutated = copy.deepcopy(self.runtime)
                mutated["segments"][index]["learning_objective"] += (
                    " [objective mutation]"
                )
                mutated_digests = quality._invariant_digests(mutated)
                self.assertNotEqual(
                    mutated_digests["course_objectives"],
                    baseline_objectives,
                )
                self.assertEqual(
                    {
                        key: value
                        for key, value in mutated_digests.items()
                        if key != "course_objectives"
                    },
                    {
                        key: value
                        for key, value in baseline.items()
                        if key != "course_objectives"
                    },
                )

    def test_course_objective_invariant_rejects_type_coercion_and_empty_text(
        self,
    ) -> None:
        for field, invalid_value in (
            ("act_id", 1),
            ("act_objective", True),
            ("learning_objective", ["objective"]),
            ("learning_objective", "   "),
            ("learning_objective", None),
        ):
            with self.subTest(field=field, invalid_value=invalid_value):
                mutated = copy.deepcopy(self.runtime)
                mutated["segments"][0][field] = invalid_value
                with self.assertRaisesRegex(
                    quality.QualityError,
                    rf"segments\[0\]\.{field}=",
                ):
                    quality._invariant_digests(mutated)

    def test_current_challengers_preserve_course_objective_invariant(self) -> None:
        baseline = quality._invariant_digests(self.runtime)["course_objectives"]
        modeled_sources = [
            self.ratchet_manifest["experiment_control"],
            *(
                self.ratchet_manifest["variants"][variant_id]
                for variant_id in quality.EXPECTED_VARIANTS
            ),
        ]
        for visual_sources in modeled_sources:
            with self.subTest(visual_sources=visual_sources):
                modeled = quality._modeled_runtime(self.runtime, visual_sources)
                self.assertEqual(
                    quality._invariant_digests(modeled)["course_objectives"],
                    baseline,
                )

    def test_ratchet_preserves_each_sentinel_viewport_vector(self) -> None:
        ratchet = self.registry["ratchet"]
        results = [ratchet["experiment_control"], *ratchet["challengers"]]
        expected_viewports = [viewport["id"] for viewport in quality.VIEWPORTS]
        for result in results:
            self.assertEqual(
                [vector["segment_id"] for vector in result["vectors"]],
                list(quality.PROTECTED_DENSE_SEGMENTS),
            )
            for vector in result["vectors"]:
                self.assertEqual(
                    [item["viewport_id"] for item in vector["viewports"]],
                    expected_viewports,
                )
                for item in vector["viewports"]:
                    self.assertEqual(
                        set(item),
                        {
                            "viewport_id",
                            "label",
                            "annotation",
                            "overlay",
                            "projection",
                            "delta_from_experiment_control",
                        },
                    )
                    self.assertEqual(
                        set(item["label"]),
                        {
                            "visible_label_count",
                            "projected_base_font_px",
                            "fixed_focus_key_chip_count",
                            "fixed_focus_key_font_px",
                            "risk_flags",
                        },
                    )
                    self.assertEqual(
                        set(item["annotation"]),
                        {
                            "claim_coverage",
                            "covered_claim_count",
                            "claim_count",
                            "risk_flags",
                        },
                    )
                    self.assertEqual(set(item["projection"]), {"clipped_point_count"})

    def test_all_section_risk_non_regression_covers_26_by_5_dimensions(self) -> None:
        combined = next(
            item
            for item in self.registry["ratchet"]["challengers"]
            if item["id"] == "combined"
        )
        gate = combined["layout_gates"]["all_section_risk_non_regression"]
        self.assertTrue(gate["passed"])
        self.assertTrue(gate["taxonomy_complete"])
        self.assertEqual(gate["segment_count"], 26)
        self.assertEqual(gate["viewport_count"], 5)
        self.assertEqual(gate["evaluation_count"], 130)
        self.assertEqual(gate["dimension_ids"], list(quality.QUALITY_RISK_DIMENSIONS))
        self.assertEqual(
            gate["protected_metric_ids"],
            list(quality.PROTECTED_NONREGRESSION_METRICS),
        )
        self.assertEqual(gate["float_tolerance"], 0.000001)
        self.assertEqual(gate["risk_flag_regression_count"], 0)
        self.assertEqual(gate["metric_regression_count"], 0)
        self.assertEqual(gate["regression_count"], 0)
        self.assertEqual(
            Counter(record["metric_id"] for record in gate["metric_regressions"]),
            {},
        )
        self.assertTrue(
            all(
                len(record["dimensions"]) == len(quality.QUALITY_RISK_DIMENSIONS)
                for record in gate["evaluations"]
            )
        )
        self.assertEqual(
            {
                len(record["metrics"])
                for record in gate["evaluations"]
                if next(
                    segment
                    for segment in self.registry["segments"]
                    if segment["segment_id"] == record["segment_id"]
                )["render_mode"]
                == "2d"
            },
            {12},
        )
        self.assertEqual(
            {
                len(record["metrics"])
                for record in gate["evaluations"]
                if next(
                    segment
                    for segment in self.registry["segments"]
                    if segment["segment_id"] == record["segment_id"]
                )["render_mode"]
                == "3d"
            },
            {11},
        )

    def test_continuous_decline_without_new_risk_flag_fails(self) -> None:
        mutated = copy.deepcopy(self.registry)
        segment = next(
            item
            for item in mutated["segments"]
            if item["segment_id"] == "s05_ppa_not_wire"
        )
        evaluation = next(
            item
            for item in segment["quality_vector"]["viewport_evaluations"]
            if item["viewport_id"] == "1920x1080"
        )
        original_flags = copy.deepcopy(evaluation["risk_flags"])
        original = evaluation["two_dimensional"]["focus_occupancy"]
        evaluation["two_dimensional"]["focus_occupancy"] = quality._round(
            original - 0.001
        )
        self.assertGreater(
            evaluation["two_dimensional"]["focus_occupancy"],
            quality.MIN_FOCUS_OCCUPANCY,
        )
        self.assertEqual(evaluation["risk_flags"], original_flags)

        gate = quality._all_section_risk_non_regression(mutated, self.registry)
        self.assertFalse(gate["passed"])
        self.assertEqual(gate["risk_flag_regression_count"], 0)
        self.assertEqual(gate["metric_regression_count"], 1)
        self.assertEqual(gate["regression_count"], 1)
        self.assertEqual(
            gate["metric_regressions"],
            [
                {
                    "segment_id": "s05_ppa_not_wire",
                    "viewport_id": "1920x1080",
                    "metric_id": "two_dimensional.focus_occupancy",
                    "direction": "must_not_decrease",
                    "experiment_control_value": original,
                    "candidate_value": quality._round(original - 0.001),
                    "delta": -0.001,
                    "tolerance": quality.METRIC_REGRESSION_TOLERANCE,
                    "regressed": True,
                }
            ],
        )

        tolerated = copy.deepcopy(self.registry)
        tolerated_segment = next(
            item
            for item in tolerated["segments"]
            if item["segment_id"] == "s05_ppa_not_wire"
        )
        tolerated_evaluation = next(
            item
            for item in tolerated_segment["quality_vector"]["viewport_evaluations"]
            if item["viewport_id"] == "1920x1080"
        )
        tolerated_evaluation["two_dimensional"]["focus_occupancy"] -= (
            quality.METRIC_REGRESSION_TOLERANCE / 2
        )
        self.assertTrue(
            quality._all_section_risk_non_regression(tolerated, self.registry)["passed"]
        )

    def test_label_and_overlay_continuous_metrics_falsify_silent_regressions(
        self,
    ) -> None:
        def evaluation(registry: dict, segment_id: str, viewport_id: str) -> dict:
            segment = next(
                item
                for item in registry["segments"]
                if item["segment_id"] == segment_id
            )
            return next(
                item
                for item in segment["quality_vector"]["viewport_evaluations"]
                if item["viewport_id"] == viewport_id
            )

        visible = copy.deepcopy(self.registry)
        visible_evaluation = evaluation(visible, "s05_ppa_not_wire", "1920x1080")
        visible_evaluation["visible_label_count"] += 1
        visible_gate = quality._all_section_risk_non_regression(visible, self.registry)
        self.assertEqual(
            [item["metric_id"] for item in visible_gate["metric_regressions"]],
            ["visible_label_count"],
        )

        footprint = copy.deepcopy(self.registry)
        footprint_evaluation = evaluation(footprint, "s05_ppa_not_wire", "1920x1080")
        footprint_evaluation["two_dimensional"]["estimated_label_pixels"] += 1.0
        footprint_evaluation["two_dimensional"]["label_stage_ratio"] += 0.001
        footprint_gate = quality._all_section_risk_non_regression(
            footprint, self.registry
        )
        self.assertEqual(
            {item["metric_id"] for item in footprint_gate["metric_regressions"]},
            {
                "two_dimensional.estimated_label_pixels",
                "two_dimensional.label_stage_ratio",
            },
        )

        overlay = copy.deepcopy(self.registry)
        overlay_evaluation = evaluation(overlay, "s09_watt_becomes_heat", "1440x900")
        self.assertTrue(overlay_evaluation["teaching_overlay"]["present"])
        overlay_evaluation["teaching_overlay"]["height_stage_ratio"] += 0.001
        overlay_evaluation["teaching_overlay"]["area_stage_ratio"] += 0.001
        overlay_gate = quality._all_section_risk_non_regression(overlay, self.registry)
        self.assertEqual(
            {item["metric_id"] for item in overlay_gate["metric_regressions"]},
            {
                "teaching_overlay.height_stage_ratio",
                "teaching_overlay.area_stage_ratio",
            },
        )

        annotations = next(
            item
            for item in self.registry["ratchet"]["challengers"]
            if item["id"] == "annotations_only"
        )
        introduction_records = [
            metric
            for record in annotations["layout_gates"][
                "all_section_risk_non_regression"
            ]["evaluations"]
            for metric in record["metrics"]
            if metric["metric_id"]
            in {
                "teaching_overlay.height_stage_ratio",
                "teaching_overlay.area_stage_ratio",
            }
            and metric["experiment_control_value"] == 0
            and metric["candidate_value"] > 0
        ]
        self.assertTrue(introduction_records)
        self.assertTrue(all(not item["regressed"] for item in introduction_records))

    def test_unreviewed_occupancy_risk_fails_modeled_eligibility(self) -> None:
        mutated = copy.deepcopy(self.registry)
        segment = next(
            item
            for item in mutated["segments"]
            if item["segment_id"] == "s01_fire_to_electricity"
        )
        evaluation = segment["quality_vector"]["viewport_evaluations"][0]
        evaluation["risk_flags"] = sorted(
            {*evaluation["risk_flags"], "low_projected_occupancy"}
        )
        reviews = self.ratchet_manifest["occupancy_reviews"]
        mutated["visual_gates"]["occupancy_review"] = quality._occupancy_review_gate(
            mutated["segments"], reviews
        )
        self.assertFalse(mutated["visual_gates"]["occupancy_review"]["passed"])
        self.assertEqual(
            mutated["visual_gates"]["occupancy_review"]["status"], "failed"
        )
        self.assertIn(
            {
                "segment_id": "s01_fire_to_electricity",
                "viewport_id": "1920x1080",
                "risk_flags": ["low_projected_occupancy"],
                "metric_id": "three_dimensional.projected_occupancy",
                "observed_value": evaluation["three_dimensional"][
                    "projected_occupancy"
                ],
                "metric_available": True,
                "disposition": "requires_live_preference",
            },
            mutated["visual_gates"]["occupancy_review"]["missing_reviews"],
        )
        result = quality._ratchet_result(
            "mutated",
            {"label_source": "current", "annotation_source": "current"},
            mutated,
            self.registry,
            {},
        )
        self.assertFalse(result["modeled_eligible"])
        self.assertFalse(
            result["layout_gates"]["all_section_risk_non_regression"]["passed"]
        )

    def test_occupancy_reviews_bind_exact_generated_metric_and_value(self) -> None:
        review_sets, combined = _copied_occupancy_reviews(self.ratchet_manifest)
        combined["reviews"][0]["observed_value"] += 0.000001
        value_gate = quality._occupancy_review_gate(
            self.registry["segments"], review_sets
        )
        self.assertFalse(value_gate["passed"])
        self.assertIn(
            "observed_value_does_not_match_evaluation",
            value_gate["malformed_reviews"][0]["reasons"],
        )

        review_sets, combined = _copied_occupancy_reviews(self.ratchet_manifest)
        combined["reviews"][0]["metric_id"] = "two_dimensional.focus_occupancy"
        metric_gate = quality._occupancy_review_gate(
            self.registry["segments"], review_sets
        )
        self.assertFalse(metric_gate["passed"])
        self.assertIn(
            "metric_id_does_not_match_evaluation",
            metric_gate["malformed_reviews"][0]["reasons"],
        )

    def test_occupancy_review_resolution_schema_fails_closed(self) -> None:
        current_state = self._candidate_current_state("combined")

        def gate_for(mutator):
            review_sets, combined = _copied_occupancy_reviews(self.ratchet_manifest)
            mutator(combined["reviews"][0], combined)
            return quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest={
                    "schema_version": quality.OCCUPANCY_CAPTURE_SCHEMA_VERSION,
                    "captures": [],
                },
            )

        unknown_field = gate_for(
            lambda record, _review_set: record.__setitem__("unknown", None)
        )
        self.assertEqual(unknown_field["status"], "failed")
        self.assertEqual(
            unknown_field["malformed_reviews"][0]["reason"], "fields_not_exact"
        )

        invalid_status = gate_for(
            lambda record, _review_set: record.__setitem__("status", "approved")
        )
        self.assertIn(
            "status_is_invalid", invalid_status["malformed_reviews"][0]["reasons"]
        )

        stale_modeled_ref = gate_for(
            lambda record, _review_set: record.__setitem__(
                "modeled_evidence_ref", "diagram/course_quality.json#wrong"
            )
        )
        self.assertIn(
            "modeled_evidence_ref_does_not_match_evaluation",
            stale_modeled_ref["malformed_reviews"][0]["reasons"],
        )

        claimed_live = gate_for(
            lambda record, _review_set: record.__setitem__(
                "live_review", {"decision": "approved"}
            )
        )
        self.assertEqual(claimed_live["status"], "failed")
        self.assertIn(
            "unresolved_review_must_not_claim_live_provenance",
            claimed_live["malformed_reviews"][0]["reasons"],
        )

        for status in ("live_approved", "live_rejected"):
            with self.subTest(resolved_without_provenance=status):
                resolved_without_provenance = gate_for(
                    lambda record, _review_set, status=status: record.__setitem__(
                        "status", status
                    )
                )
                self.assertEqual(resolved_without_provenance["status"], "failed")
                self.assertIn(
                    "live_review_fields_not_exact",
                    resolved_without_provenance["malformed_reviews"][0]["reasons"],
                )

        def resolved_record(record, review_set, *, decision="approved"):
            record["status"] = "live_approved"
            artifact_sha256 = "a" * 64
            reviewed_at = "2026-08-29T12:00:00-07:00"
            reviewer_id = "reviewer-1"
            modeled_evaluation_sha256 = quality._occupancy_modeled_evaluation_sha256(
                review_set["candidate_id"],
                current_state["candidate_current_state_sha256"],
                record,
            )
            record["live_review"] = {
                "decision": decision,
                "reviewer_id": reviewer_id,
                "reviewed_at": reviewed_at,
                "candidate_current_state_sha256": current_state[
                    "candidate_current_state_sha256"
                ],
                "validation_compiler_implementation_sha256": current_state[
                    "validation_compiler_implementation_sha256"
                ],
                "modeled_evaluation_sha256": modeled_evaluation_sha256,
                "artifact_sha256": artifact_sha256,
                "evidence_ref": quality._occupancy_live_evidence_ref(
                    review_set["candidate_id"],
                    review_set["candidate_provenance_sha256"],
                    candidate_current_state_sha256=current_state[
                        "candidate_current_state_sha256"
                    ],
                    validation_compiler_implementation_sha256=current_state[
                        "validation_compiler_implementation_sha256"
                    ],
                    segment_id=record["segment_id"],
                    viewport_id=record["viewport_id"],
                    modeled_evaluation_sha256=modeled_evaluation_sha256,
                    decision="approved",
                    reviewer_id=reviewer_id,
                    reviewed_at=reviewed_at,
                    artifact_sha256=artifact_sha256,
                ),
            }

        def malformed_timestamp(record, review_set):
            resolved_record(record, review_set)
            record["live_review"]["reviewed_at"] = "2026-08-29"

        malformed_time = gate_for(malformed_timestamp)
        self.assertIn(
            "live_reviewed_at_must_be_rfc3339",
            malformed_time["malformed_reviews"][0]["reasons"],
        )

        for invalid_ref in (
            "live:occupancy-review/1",
            "./diagram/course_quality.json#ratchet/challengers/combined",
        ):
            with self.subTest(invalid_ref=invalid_ref):
                invalid_evidence = gate_for(
                    lambda record, review_set, invalid_ref=invalid_ref: (
                        resolved_record(record, review_set),
                        record["live_review"].__setitem__("evidence_ref", invalid_ref),
                    )
                )
                self.assertIn(
                    "live_evidence_ref_is_not_content_addressed",
                    invalid_evidence["malformed_reviews"][0]["reasons"],
                )

        artifact_tamper = gate_for(
            lambda record, review_set: (
                resolved_record(record, review_set),
                record["live_review"].__setitem__("artifact_sha256", "b" * 64),
            )
        )
        self.assertIn(
            "live_evidence_ref_is_not_content_addressed",
            artifact_tamper["malformed_reviews"][0]["reasons"],
        )

        def mismatched_rejection_decision(record, review_set):
            resolved_record(record, review_set, decision="rejected")

        mismatched_decision = gate_for(mismatched_rejection_decision)
        self.assertIn(
            "live_decision_does_not_match_status",
            mismatched_decision["malformed_reviews"][0]["reasons"],
        )

        def extra_identity(record, review_set):
            record["segment_id"] = "s01_fire_to_electricity"
            record["viewport_id"] = "390x844"
            record["modeled_evidence_ref"] = quality._occupancy_modeled_evidence_ref(
                review_set["candidate_id"],
                record["segment_id"],
                record["viewport_id"],
            )

        extra = gate_for(extra_identity)
        self.assertEqual(
            extra["extra_reviews"],
            [
                {
                    "segment_id": "s01_fire_to_electricity",
                    "viewport_id": "390x844",
                }
            ],
        )
        self.assertTrue(extra["missing_reviews"])
        self.assertTrue(extra["malformed_reviews"])

    def test_occupancy_review_resolution_aggregates_pending_passed_and_failed(
        self,
    ) -> None:
        unresolved = quality._occupancy_review_gate(
            self.registry["segments"], self.ratchet_manifest["occupancy_reviews"]
        )
        self.assertFalse(unresolved["passed"])
        self.assertEqual(unresolved["status"], "pending")
        self.assertEqual(unresolved["disposition"], "requires_live_preference")
        self.assertEqual(
            unresolved["resolution_counts"],
            {"live_approved": 0, "live_rejected": 0, "unresolved": 15},
        )
        self.assertTrue(
            all(review["live_review"] is None for review in unresolved["reviews"])
        )

        approved_root, approved_reviews, approved_captures, current_state = (
            self._resolved_occupancy_fixture("live_approved")
        )
        with self._retained_path_patch(approved_root):
            approved = quality._occupancy_review_gate(
                self.registry["segments"],
                approved_reviews,
                expected_current_state=current_state,
                capture_manifest=approved_captures,
            )
        self.assertTrue(approved["passed"])
        self.assertEqual(approved["status"], "passed")
        self.assertEqual(approved["disposition"], "live_approved")
        self.assertEqual(
            approved["resolution_counts"],
            {"live_approved": 15, "live_rejected": 0, "unresolved": 0},
        )

        mixed_reviews = copy.deepcopy(approved_reviews)
        mixed_record = _occupancy_review_set({"occupancy_reviews": mixed_reviews})[
            "reviews"
        ][0]
        mixed_record["status"] = "unresolved"
        mixed_record["live_review"] = None
        with self._retained_path_patch(approved_root):
            mixed = quality._occupancy_review_gate(
                self.registry["segments"],
                mixed_reviews,
                expected_current_state=current_state,
                capture_manifest=approved_captures,
            )
        self.assertFalse(mixed["passed"])
        self.assertEqual(mixed["status"], "failed")
        self.assertTrue(
            any(
                "canonical_capture_manifest_entry_is_unconsumed" in item["reasons"]
                for item in mixed["malformed_reviews"]
            )
        )

        mixed_captures = copy.deepcopy(approved_captures)
        mixed_captures["captures"] = [
            capture
            for capture in mixed_captures["captures"]
            if (
                capture["segment_id"],
                capture["viewport_id"],
            )
            != (mixed_record["segment_id"], mixed_record["viewport_id"])
        ]
        with self._retained_path_patch(approved_root):
            mixed_without_orphan = quality._occupancy_review_gate(
                self.registry["segments"],
                mixed_reviews,
                expected_current_state=current_state,
                capture_manifest=mixed_captures,
            )
        self.assertEqual(mixed_without_orphan["status"], "pending")
        self.assertEqual(mixed_without_orphan["malformed_reviews"], [])

        rejected_root, rejected_reviews, rejected_captures, rejected_state = (
            self._resolved_occupancy_fixture("live_rejected")
        )
        with self._retained_path_patch(rejected_root):
            rejected = quality._occupancy_review_gate(
                self.registry["segments"],
                rejected_reviews,
                expected_current_state=rejected_state,
                capture_manifest=rejected_captures,
            )
        self.assertFalse(rejected["passed"])
        self.assertEqual(rejected["status"], "failed")
        self.assertEqual(rejected["disposition"], "live_rejected")
        self.assertEqual(rejected["resolution_counts"]["live_rejected"], 15)

        for gate, expected_status in (
            (unresolved, "pending"),
            (approved, "passed"),
            (rejected, "failed"),
        ):
            with self.subTest(candidate_modeled_status=expected_status):
                registry = copy.deepcopy(self.registry)
                registry["visual_gates"]["occupancy_review"] = gate
                result = quality._ratchet_result(
                    "mutated",
                    {"label_source": "current", "annotation_source": "current"},
                    registry,
                    self.registry,
                    {},
                )
                self.assertEqual(
                    result["modeled_gate_evidence"]["layout:occupancy_review"][
                        "status"
                    ],
                    expected_status,
                )
                self.assertEqual(result["modeled_gate_status"], expected_status)

    def test_occupancy_capture_manifest_missing_stale_and_changed_bytes_fail(
        self,
    ) -> None:
        root, review_sets, captures, current_state = self._resolved_occupancy_fixture(
            "live_approved"
        )
        missing = copy.deepcopy(captures)
        missing["captures"].pop(0)
        with self._retained_path_patch(root):
            missing_gate = quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=missing,
            )
        self.assertEqual(missing_gate["status"], "failed")
        self.assertIn(
            "canonical_capture_manifest_entry_is_missing",
            missing_gate["malformed_reviews"][0]["reasons"],
        )

        stale = copy.deepcopy(captures)
        stale_source = root / stale["captures"][0]["artifact_path"]
        stale["captures"][0]["modeled_evaluation_sha256"] = "f" * 64
        stale["captures"][0]["artifact_path"] = (
            quality._canonical_occupancy_capture_path(stale["captures"][0])
        )
        stale_target = root / stale["captures"][0]["artifact_path"]
        stale_target.parent.mkdir(parents=True, exist_ok=True)
        stale_target.write_bytes(stale_source.read_bytes())
        with self._retained_path_patch(root):
            stale_gate = quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=stale,
            )
        self.assertEqual(stale_gate["status"], "failed")
        self.assertIn(
            "canonical_capture_manifest_entry_is_stale",
            stale_gate["malformed_reviews"][0]["reasons"],
        )

        changed_bytes = copy.deepcopy(captures)
        changed_path = root / changed_bytes["captures"][0]["artifact_path"]
        changed_path.write_bytes(b"changed capture bytes\n")
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(
                quality.QualityError, "does not match retained bytes"
            ),
        ):
            quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=changed_bytes,
            )

    def test_occupancy_capture_manifest_rejects_artifact_reuse_across_identities(
        self,
    ) -> None:
        root, review_sets, captures, current_state = self._resolved_occupancy_fixture(
            "live_approved"
        )
        reused_path = copy.deepcopy(captures)
        reused_path["captures"][1]["artifact_path"] = reused_path["captures"][0][
            "artifact_path"
        ]
        reused_path["captures"][1]["artifact_sha256"] = reused_path["captures"][0][
            "artifact_sha256"
        ]
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(quality.QualityError, "not canonical"),
        ):
            quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=reused_path,
            )

        reused_bytes = copy.deepcopy(captures)
        first_path = root / reused_bytes["captures"][0]["artifact_path"]
        second = reused_bytes["captures"][1]
        second["artifact_sha256"] = reused_bytes["captures"][0]["artifact_sha256"]
        second["artifact_path"] = quality._canonical_occupancy_capture_path(second)
        second_path = root / second["artifact_path"]
        second_path.parent.mkdir(parents=True, exist_ok=True)
        second_path.write_bytes(first_path.read_bytes())
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(
                quality.QualityError, "duplicates capture artifact bytes"
            ),
        ):
            quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=reused_bytes,
            )

    def test_occupancy_capture_manifest_requires_canonical_png_and_dimensions(
        self,
    ) -> None:
        root, review_sets, captures, current_state = self._resolved_occupancy_fixture(
            "live_approved"
        )

        text_capture = copy.deepcopy(captures)
        record = text_capture["captures"][0]
        text_bytes = b"not a png\n"
        record["artifact_sha256"] = hashlib.sha256(text_bytes).hexdigest()
        record["artifact_path"] = quality._canonical_occupancy_capture_path(record)
        text_path = root / record["artifact_path"]
        text_path.parent.mkdir(parents=True, exist_ok=True)
        text_path.write_bytes(text_bytes)
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(quality.QualityError, "must be a PNG capture"),
        ):
            quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=text_capture,
            )

        wrong_dimensions = copy.deepcopy(captures)
        record = wrong_dimensions["captures"][0]
        wrong_png = _occupancy_capture_png(1, 1, 211)
        record["artifact_sha256"] = hashlib.sha256(wrong_png).hexdigest()
        record["artifact_path"] = quality._canonical_occupancy_capture_path(record)
        wrong_path = root / record["artifact_path"]
        wrong_path.parent.mkdir(parents=True, exist_ok=True)
        wrong_path.write_bytes(wrong_png)
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(
                quality.QualityError, "dimensions must equal viewport"
            ),
        ):
            quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=wrong_dimensions,
            )

        noncanonical = copy.deepcopy(captures)
        noncanonical["captures"][0]["artifact_path"] = (
            "course/acceptance_evidence/occupancy/not-the-identity.png"
        )
        with (
            self._retained_path_patch(root),
            self.assertRaisesRegex(quality.QualityError, "not canonical"),
        ):
            quality._occupancy_review_gate(
                self.registry["segments"],
                review_sets,
                expected_current_state=current_state,
                capture_manifest=noncanonical,
            )

    def test_occupancy_review_sets_are_candidate_and_artifact_bound(self) -> None:
        review_sets = self.ratchet_manifest["occupancy_reviews"]
        self.assertEqual(
            [review_set["candidate_id"] for review_set in review_sets],
            list(quality.OCCUPANCY_REVIEW_CANDIDATE_IDS),
        )
        acceptance_provenance = {
            record["candidate_id"]: record["candidate_provenance_sha256"]
            for record in self.ratchet_manifest["acceptance"]["candidates"]
        }
        for candidate_id in quality.EXPECTED_VARIANTS:
            self.assertEqual(
                _occupancy_review_set(self.ratchet_manifest, candidate_id)[
                    "candidate_provenance_sha256"
                ],
                acceptance_provenance[candidate_id],
            )

        approved_sets, approved_labels = _copied_occupancy_reviews(
            self.ratchet_manifest, "labels_only"
        )
        labels_state = self._candidate_current_state("labels_only")
        for index, record in enumerate(approved_labels["reviews"]):
            artifact_sha256 = f"{index + 1:064x}"
            reviewer_id = f"reviewer-{index + 1}"
            reviewed_at = "2026-08-29T12:00:00-07:00"
            modeled_evaluation_sha256 = quality._occupancy_modeled_evaluation_sha256(
                "labels_only",
                labels_state["candidate_current_state_sha256"],
                record,
            )
            record["status"] = "live_approved"
            record["live_review"] = {
                "decision": "approved",
                "reviewer_id": reviewer_id,
                "reviewed_at": reviewed_at,
                "candidate_current_state_sha256": labels_state[
                    "candidate_current_state_sha256"
                ],
                "validation_compiler_implementation_sha256": labels_state[
                    "validation_compiler_implementation_sha256"
                ],
                "modeled_evaluation_sha256": modeled_evaluation_sha256,
                "artifact_sha256": artifact_sha256,
                "evidence_ref": quality._occupancy_live_evidence_ref(
                    "labels_only",
                    approved_labels["candidate_provenance_sha256"],
                    candidate_current_state_sha256=labels_state[
                        "candidate_current_state_sha256"
                    ],
                    validation_compiler_implementation_sha256=labels_state[
                        "validation_compiler_implementation_sha256"
                    ],
                    segment_id=record["segment_id"],
                    viewport_id=record["viewport_id"],
                    modeled_evaluation_sha256=modeled_evaluation_sha256,
                    decision="approved",
                    reviewer_id=reviewer_id,
                    reviewed_at=reviewed_at,
                    artifact_sha256=artifact_sha256,
                ),
            }
        labels_gate = quality._occupancy_review_gate(
            self.registry["segments"],
            approved_sets,
            candidate_id="labels_only",
            expected_current_state=labels_state,
            capture_manifest={
                "schema_version": quality.OCCUPANCY_CAPTURE_SCHEMA_VERSION,
                "captures": [],
            },
        )
        combined_gate = quality._occupancy_review_gate(
            self.registry["segments"],
            approved_sets,
            candidate_id="combined",
        )
        control_gate = quality._occupancy_review_gate(
            self.registry["segments"],
            approved_sets,
            candidate_id="experiment_control",
        )
        self.assertEqual(labels_gate["status"], "failed")
        self.assertTrue(
            all(
                "canonical_capture_manifest_entry_is_missing" in item["reasons"]
                for item in labels_gate["malformed_reviews"]
            )
        )
        self.assertEqual(combined_gate["status"], "pending")
        self.assertEqual(control_gate["status"], "pending")

        mismatched_registry = copy.deepcopy(self.registry)
        mismatched_registry["visual_gates"]["occupancy_review"] = labels_gate
        with self.assertRaisesRegex(
            quality.QualityError, "occupancy review candidate binding"
        ):
            quality._ratchet_result(
                "combined",
                self.ratchet_manifest["variants"]["combined"],
                mismatched_registry,
                self.registry,
                {},
            )

    def test_occupancy_manifest_rejects_stale_or_resolved_control_binding(self) -> None:
        stale = copy.deepcopy(self.ratchet_manifest)
        _occupancy_review_set(stale, "labels_only")["candidate_provenance_sha256"] = (
            "0" * 64
        )
        with (
            patch.object(quality.scene_pipeline, "load_yaml", return_value=stale),
            self.assertRaisesRegex(
                quality.QualityError, "candidate provenance is stale"
            ),
        ):
            quality.load_ratchet_manifest()

        resolved_control = copy.deepcopy(self.ratchet_manifest)
        control_record = _occupancy_review_set(resolved_control, "experiment_control")[
            "reviews"
        ][0]
        control_record["status"] = "live_approved"
        control_record["live_review"] = {}
        with (
            patch.object(
                quality.scene_pipeline, "load_yaml", return_value=resolved_control
            ),
            self.assertRaisesRegex(
                quality.QualityError,
                "experiment-control occupancy reviews must remain explicitly unresolved",
            ),
        ):
            quality.load_ratchet_manifest()

    def test_labels_only_cannot_accept_while_occupancy_review_is_pending(
        self,
    ) -> None:
        evaluation = copy.deepcopy(
            next(
                item
                for item in self.registry["ratchet"]["pareto"]["evaluations"]
                if item["candidate_id"] == "labels_only"
            )
        )
        candidate = evaluation["input"]["candidate"]
        for gate_group in ("static_gate_evidence", "live_gate_evidence"):
            for gate_id in candidate[gate_group]:
                candidate[gate_group][gate_id] = {
                    "status": "passed",
                    "evidence_ref": f"verified:{gate_id}",
                }
        for review in candidate["blind_reviews"]:
            review["preference"] = "candidate"
            review["evidence_ref"] = f"verified:{review['reviewer_id']}"

        decision = quality._pareto_decision_against_experiment_control(
            candidate,
            required_protection_members=evaluation["input"][
                "required_protection_members"
            ],
            required_modeled_gate_ids=evaluation["input"]["required_modeled_gate_ids"],
        )
        self.assertEqual(decision["disposition"], "pending")
        self.assertEqual(decision["modeled_gate_status"], "pending")
        self.assertIn(
            "modeled_gate_evidence:layout:occupancy_review:pending",
            decision["reasons"],
        )

    def test_each_candidate_has_a_nonvacuous_pareto_evaluation(self) -> None:
        evaluations = self.registry["ratchet"]["pareto"]["evaluations"]
        self.assertEqual(
            [evaluation["candidate_id"] for evaluation in evaluations],
            ["labels_only", "annotations_only", "combined"],
        )
        expected = {
            "labels_only": {
                "disposition": "pending",
                "dimension_id": "label_pressure_cleared",
                "delta": 1.0,
                "regression_counts": {
                    cohort: 0 for cohort in quality.ratchet.PROTECTION_COHORTS
                },
            },
            "annotations_only": {
                "disposition": "rejected",
                "dimension_id": "dense_annotation_gap_cleared",
                "delta": 1.0,
                "regression_counts": {
                    "protected_dimensions": 1,
                    "worst_decile_segments": 0,
                    "predecessors": 0,
                    "successors": 0,
                    "shared_consumers": 1,
                },
            },
            "combined": {
                "disposition": "pending",
                "dimension_id": ("label_pressure_and_dense_annotation_gap_cleared"),
                "delta": 2.0,
                "regression_counts": {
                    cohort: 0 for cohort in quality.ratchet.PROTECTION_COHORTS
                },
            },
        }
        for evaluation in evaluations:
            candidate_id = evaluation["candidate_id"]
            required = evaluation["input"]["required_protection_members"]
            self.assertEqual(set(required), set(quality.ratchet.PROTECTION_COHORTS))
            self.assertTrue(all(required[cohort] for cohort in required))
            ordered_ids = [
                segment["segment_id"] for segment in self.runtime["segments"]
            ]
            expected_pairs = list(pairwise(ordered_ids))
            self.assertEqual(
                evaluation["input"]["ordered_handoff_pairs"],
                [
                    {
                        "predecessor_id": predecessor,
                        "successor_id": successor,
                    }
                    for predecessor, successor in expected_pairs
                ],
            )
            self.assertEqual(len(required["predecessors"]), 25)
            self.assertEqual(len(required["successors"]), 25)
            self.assertEqual(
                required["predecessors"],
                [
                    f"handoff:{predecessor}->{successor}:predecessor"
                    for predecessor, successor in expected_pairs
                ],
            )
            self.assertEqual(
                required["successors"],
                [
                    f"handoff:{predecessor}->{successor}:successor"
                    for predecessor, successor in expected_pairs
                ],
            )
            self.assertEqual(
                required["worst_decile_segments"],
                self.registry["ratchet"]["experiment_control_worst_quality_decile"][
                    "segment_ids"
                ],
            )
            self.assertNotEqual(
                required["worst_decile_segments"],
                self.registry["worst_quality_decile"]["segment_ids"],
            )
            self.assertEqual(
                evaluation["input"]["candidate"]["candidate_id"], candidate_id
            )
            target = evaluation["input"]["candidate"]["target"]
            self.assertEqual(
                set(target),
                {
                    "dimension_id",
                    "direction",
                    "experiment_control_value",
                    "candidate_value",
                    "minimum_material_improvement",
                    "evidence_ref",
                },
            )
            self.assertNotIn("champion_value", target)
            required_modeled = evaluation["input"]["required_modeled_gate_ids"]
            self.assertEqual(
                set(required_modeled),
                set(evaluation["input"]["candidate"]["modeled_gate_evidence"]),
            )
            self.assertEqual(
                len(required_modeled),
                len(self.registry["ratchet"]["challengers"][0]["layout_gates"])
                + len(quality.RATCHET_TARGET_GATE_IDS[candidate_id]),
            )
            decision = evaluation["decision"]
            self.assertEqual(decision["candidate_id"], candidate_id)
            self.assertEqual(
                decision["disposition"], expected[candidate_id]["disposition"]
            )
            self.assertTrue(decision["material_improvement"]["passed"])
            self.assertEqual(
                decision["material_improvement"]["dimension_id"],
                expected[candidate_id]["dimension_id"],
            )
            self.assertEqual(
                decision["material_improvement"]["delta"],
                expected[candidate_id]["delta"],
            )
            self.assertEqual(
                decision["regression_free"],
                candidate_id in {"labels_only", "combined"},
            )
            self.assertEqual(
                decision["regression_counts"],
                expected[candidate_id]["regression_counts"],
            )
            self.assertEqual(decision["static_gate_status"], "pending")
            self.assertEqual(decision["live_gate_status"], "pending")
            self.assertEqual(decision["blind_review"]["status"], "pending")
            self.assertEqual(
                decision["modeled_gate_status"],
                {
                    "labels_only": "pending",
                    "annotations_only": "failed",
                    "combined": "pending",
                }[candidate_id],
            )

        synthetic_results = {
            "experiment_control": self.registry["ratchet"]["experiment_control"],
            "challengers": self.registry["ratchet"]["challengers"],
            "pareto": self.registry["ratchet"]["pareto"],
        }
        serialized = json.dumps(synthetic_results, sort_keys=True)
        self.assertNotIn('"champion_value"', serialized)
        self.assertNotIn('"delta_from_champion"', serialized)

        combined_evaluation = next(
            item for item in evaluations if item["candidate_id"] == "combined"
        )
        shared = {
            item["member_id"]: item["regressed"]
            for item in combined_evaluation["input"]["candidate"][
                "protection_evidence"
            ]["shared_consumers"]
        }
        self.assertEqual(
            shared,
            {
                "shared_consumer:course_runtime": False,
                "shared_consumer:teaching_overlay": False,
                "shared_consumer:focus_key_and_boundary": False,
            },
        )

    def test_audit_program_and_frozen_champion_are_truthfully_pending(self) -> None:
        audit_program = self.registry["audit_program"]
        self.assertEqual(audit_program["schema_version"], 1)
        self.assertEqual(len(audit_program["rounds"]), 21)

        segment_ids = [segment["segment_id"] for segment in self.registry["segments"]]
        duplicate_finding = copy.deepcopy(
            quality.load_audit_manifest(segment_ids=segment_ids)
        )
        round_15 = next(
            record
            for record in duplicate_finding["rounds"]
            if record["round_id"] == "static_round_15"
        )
        round_16 = next(
            record
            for record in duplicate_finding["rounds"]
            if record["round_id"] == "static_round_16"
        )
        round_16["audit_reports"][2]["findings"].append(
            copy.deepcopy(
                round_15["audit_reports"][2]["findings"][2]
            )
        )
        with (
            patch.object(
                quality.scene_pipeline,
                "load_yaml",
                return_value=duplicate_finding,
            ),
            self.assertRaisesRegex(
                quality.QualityError, "globally unique across rounds"
            ),
        ):
            quality.load_audit_manifest(segment_ids=segment_ids)
        self.assertEqual(audit_program["saturation"]["status"], "continue")
        self.assertFalse(audit_program["saturation"]["saturated"])
        dispositions = {
            item["candidate_id"]: item["disposition"]
            for item in audit_program["rounds"][-1]["challenger_dispositions"]
        }
        self.assertEqual(
            dispositions,
            {
                "labels_only": "pending",
                "annotations_only": "rejected",
                "combined": "pending",
            },
        )
        current_dispositions = {
            item["candidate_id"]: item["disposition"]
            for item in audit_program["saturation"]["current_challenger_dispositions"]
        }
        self.assertEqual(current_dispositions, dispositions)
        round_6 = next(
            round_record
            for round_record in audit_program["rounds"]
            if round_record["round_id"] == "static_round_6"
        )
        self.assertEqual(
            {
                item["candidate_id"]: item["disposition"]
                for item in round_6["challenger_dispositions"]
            },
            {
                "labels_only": "pending",
                "annotations_only": "rejected",
                "combined": "rejected",
            },
        )

        frozen = self.registry["frozen_champion"]
        self.assertTrue(frozen["static_verification"]["static_integrity_passed"])
        self.assertFalse(frozen["eligible_as_experiment_control"])
        self.assertEqual(
            frozen["static_verification"]["missing_live_evidence"],
            [
                "historical_per_viewport_frame_captures",
                "historical_per_viewport_quality_vectors",
            ],
        )

    def test_absolute_hard_layout_gates_reject_non_sentinel_defects(self) -> None:
        overlay_segment_id = next(
            segment["segment_id"]
            for segment in self.registry["segments"]
            if segment["segment_id"] not in quality.PROTECTED_DENSE_SEGMENTS
            and any(
                evaluation["teaching_overlay"]["present"]
                for evaluation in segment["quality_vector"]["viewport_evaluations"]
            )
        )
        three_dimensional_segment_id = next(
            segment["segment_id"]
            for segment in self.registry["segments"]
            if segment["segment_id"] not in quality.PROTECTED_DENSE_SEGMENTS
            and any(
                "three_dimensional" in evaluation
                for evaluation in segment["quality_vector"]["viewport_evaluations"]
            )
        )
        two_dimensional_segment_id = next(
            segment["segment_id"]
            for segment in self.registry["segments"]
            if segment["segment_id"] not in quality.PROTECTED_DENSE_SEGMENTS
            and any(
                "two_dimensional" in evaluation
                for evaluation in segment["quality_vector"]["viewport_evaluations"]
            )
        )
        cases = (
            (
                "overlay_residual_label_collision",
                overlay_segment_id,
                {
                    "residual_collision_count": 1,
                    "residual_collision_ids": ["adversarial_label"],
                },
            ),
            (
                "overlay_suppression_focus_key_coverage",
                overlay_segment_id,
                {
                    "suppressed_labels_covered_by_focus_key": False,
                    "suppressed_labels_missing_from_focus_key": ["adversarial_label"],
                },
            ),
            (
                "overlay_clipping",
                overlay_segment_id,
                {"viewport_clipped": True},
            ),
            (
                "two_dimensional_label_clipping",
                two_dimensional_segment_id,
                {
                    "unclamped_label_clipping_count": 1,
                    "unclamped_label_clipping_ids": ["adversarial_label"],
                    "minimum_label_frame_margin_svg_units": -1.0,
                    "label_frame_margin_passed": False,
                },
            ),
            (
                "three_dimensional_point_clipping",
                three_dimensional_segment_id,
                {"clipped_point_count": 1},
            ),
        )
        for gate_id, segment_id, defect in cases:
            with self.subTest(gate_id=gate_id, segment_id=segment_id):
                mutated = copy.deepcopy(self.registry)
                segment = next(
                    record
                    for record in mutated["segments"]
                    if record["segment_id"] == segment_id
                )
                evaluation = segment["quality_vector"]["viewport_evaluations"][0]
                if gate_id == "three_dimensional_point_clipping":
                    evaluation["three_dimensional"].update(defect)
                elif gate_id == "two_dimensional_label_clipping":
                    evaluation["two_dimensional"].update(defect)
                else:
                    evaluation["teaching_overlay"].update(defect)

                self.assertTrue(mutated["visual_gates"][gate_id]["passed"])
                result = quality._ratchet_result(
                    "mutated",
                    {"label_source": "current", "annotation_source": "current"},
                    mutated,
                    self.registry,
                    {},
                )
                gate = result["layout_gates"][gate_id]
                self.assertFalse(gate["passed"])
                self.assertEqual(gate["segment_count"], 26)
                self.assertEqual(gate["viewport_count"], 5)
                self.assertEqual(gate["evaluation_count"], 130)
                self.assertEqual(gate["failure_count"], 1)
                self.assertEqual(gate["failures"][0]["segment_id"], segment_id)
                self.assertEqual(
                    gate["failures"][0]["viewport_id"],
                    quality.VIEWPORTS[0]["id"],
                )
                self.assertEqual(result["modeled_gate_status"], "failed")

    def test_teaching_overlay_stage_edge_clearance_gate_fails_closed(self) -> None:
        gate_id = "teaching_overlay_stage_edge_clearance"
        expected_ids = self.registry["visual_gates"][gate_id][
            "expected_annotated_segment_ids"
        ]

        mutated = copy.deepcopy(self.registry)
        segment = next(
            record
            for record in mutated["segments"]
            if record["segment_id"] == "p1_read_the_machine"
        )
        evaluation = next(
            record
            for record in segment["quality_vector"]["viewport_evaluations"]
            if record["viewport_id"] == quality.SHORT_VIEWPORT_ID
        )
        evaluation["teaching_overlay"]["box"]["y"] -= 1.05
        self.assertTrue(mutated["visual_gates"][gate_id]["passed"])
        absolute = quality._absolute_hard_layout_gates(mutated)[gate_id]
        self.assertFalse(absolute["passed"])
        self.assertTrue(absolute["exact_coverage_passed"])
        self.assertEqual(absolute["minimum_observed_clearance_px"], 7.0)
        self.assertEqual(absolute["failure_count"], 1)
        self.assertEqual(
            absolute["failures"][0]["segment_id"],
            "p1_read_the_machine",
        )
        self.assertEqual(
            absolute["failures"][0]["viewport_id"],
            quality.SHORT_VIEWPORT_ID,
        )
        self.assertIn(
            "stage_edge_clearance_below_minimum",
            absolute["failures"][0]["failure_reasons"],
        )
        result = quality._ratchet_result(
            "mutated",
            {"label_source": "current", "annotation_source": "current"},
            mutated,
            self.registry,
            {},
        )
        self.assertFalse(result["layout_gates"][gate_id]["passed"])
        self.assertEqual(result["modeled_gate_status"], "failed")

        duplicate = copy.deepcopy(self.registry)
        segment = next(
            record
            for record in duplicate["segments"]
            if record["segment_id"] == "p1_read_the_machine"
        )
        segment["quality_vector"]["viewport_evaluations"].append(
            copy.deepcopy(segment["quality_vector"]["viewport_evaluations"][0])
        )
        duplicate_gate = quality._teaching_overlay_stage_edge_clearance_gate(
            duplicate["segments"],
            expected_annotated_segment_ids=expected_ids,
        )
        self.assertFalse(duplicate_gate["passed"])
        self.assertFalse(duplicate_gate["exact_coverage_passed"])
        self.assertIn(
            "viewport_sequence_mismatch",
            duplicate_gate["coverage_failure_reasons"],
        )
        self.assertIn(
            "duplicate_segment_viewport_evaluations",
            duplicate_gate["coverage_failure_reasons"],
        )
        self.assertGreater(duplicate_gate["failure_count"], 0)

        portrait = copy.deepcopy(self.registry)
        segment = next(
            record
            for record in portrait["segments"]
            if record["segment_id"] == "p1_read_the_machine"
        )
        evaluation = next(
            record
            for record in segment["quality_vector"]["viewport_evaluations"]
            if record["viewport_id"] == quality.PORTRAIT_VIEWPORT_ID
        )
        evaluation["teaching_overlay"]["interaction_mode"] = "toggle_overlay"
        portrait_gate = quality._teaching_overlay_stage_edge_clearance_gate(
            portrait["segments"],
            expected_annotated_segment_ids=expected_ids,
        )
        self.assertFalse(portrait_gate["passed"])
        self.assertTrue(portrait_gate["exact_coverage_passed"])
        self.assertEqual(portrait_gate["failure_count"], 1)
        self.assertIn(
            "portrait_drawer_mode_missing",
            portrait_gate["failures"][0]["failure_reasons"],
        )

    def test_short_overlay_spacing_mutation_recreates_round_9_defect(self) -> None:
        with patch.object(
            course_runtime,
            "SHORT_TEACHING_OVERLAY_ITEM_PADDING_BLOCK_PX",
            4,
        ):
            adversarial = quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.runtime,
                source_digest="adversarial-short-overlay-margin",
                occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            )
        gate = adversarial["visual_gates"]["teaching_overlay_stage_edge_clearance"]
        self.assertFalse(gate["passed"])
        self.assertTrue(gate["exact_coverage_passed"])
        self.assertTrue(gate["source_contract"]["passed"])
        self.assertLess(gate["minimum_observed_clearance_px"], 8.0)
        failure_pairs = {
            (failure["segment_id"], failure["viewport_id"])
            for failure in gate["failures"]
            if failure["segment_id"] is not None
        }
        self.assertLessEqual(
            {
                ("p1_read_the_machine", quality.SHORT_VIEWPORT_ID),
                ("s01_fire_to_electricity", quality.SHORT_VIEWPORT_ID),
            },
            failure_pairs,
        )
        self.assertTrue(
            all(
                "stage_edge_clearance_below_minimum" in failure["failure_reasons"]
                for failure in gate["failures"]
                if failure["segment_id"] is not None
            )
        )

    def test_visual_layout_gates_cover_every_modeled_viewport(self) -> None:
        self.assertEqual(len(quality.VIEWPORTS), 5)
        gates = self.registry["visual_gates"]
        self.assertTrue(
            gates["overlay_residual_label_collision"]["passed"],
            gates["overlay_residual_label_collision"]["failures"],
        )
        self.assertTrue(
            gates["overlay_suppression_focus_key_coverage"]["passed"],
            gates["overlay_suppression_focus_key_coverage"]["failures"],
        )
        self.assertTrue(
            gates["overlay_clipping"]["passed"],
            gates["overlay_clipping"]["failures"],
        )
        clearance = gates["teaching_overlay_stage_edge_clearance"]
        self.assertTrue(clearance["passed"], clearance["failures"])
        self.assertEqual(clearance["status"], "passed")
        self.assertEqual(clearance["scope"], "all_annotated_segments_all_viewports")
        self.assertEqual(clearance["annotated_segment_count"], 16)
        self.assertEqual(clearance["expected_annotated_segment_count"], 16)
        self.assertEqual(
            clearance["annotated_segment_ids"],
            clearance["expected_annotated_segment_ids"],
        )
        self.assertEqual(clearance["viewport_count"], 5)
        self.assertEqual(clearance["evaluation_count"], 80)
        self.assertEqual(clearance["expected_evaluation_count"], 80)
        self.assertEqual(clearance["applicable_nonportrait_evaluation_count"], 64)
        self.assertEqual(clearance["portrait_not_applicable_evaluation_count"], 16)
        self.assertEqual(
            clearance["portrait_policy"],
            "explicit_not_applicable_drawer",
        )
        self.assertTrue(clearance["exact_coverage_passed"])
        self.assertEqual(clearance["coverage_failure_reasons"], [])
        self.assertEqual(clearance["required_minimum_clearance_px"], 8.0)
        self.assertEqual(clearance["minimum_observed_clearance_px"], 8.0)
        self.assertEqual(clearance["minimum_observed_top_clearance_px"], 8.05)
        self.assertEqual(
            clearance["minimum_observed_short_top_clearance_px"],
            8.05,
        )
        portrait_records = [
            record
            for record in clearance["evaluations"]
            if record["viewport_id"] == quality.PORTRAIT_VIEWPORT_ID
        ]
        self.assertEqual(len(portrait_records), 16)
        self.assertTrue(
            all(
                not record["applicable"]
                and record["status"] == "not_applicable_portrait_drawer"
                and record["stage_edge_clearances_px"] is None
                and record["minimum_stage_edge_clearance_px"] is None
                and record["passed"]
                for record in portrait_records
            )
        )
        self.assertTrue(
            gates["two_dimensional_label_clipping"]["passed"],
            gates["two_dimensional_label_clipping"]["failures"],
        )
        for gate_id in (
            "overlay_stage_coverage",
            "annotated_two_dimensional_physical_composition",
            "annotated_three_dimensional_physical_composition",
            "compact_annotation_kind_cue",
            "focus_key_geometry_correspondence",
            "masthead_focus_key_visibility",
            "short_height_focus_key_complete_visibility",
            "tablet_focus_key_complete_visibility",
            "desktop_focus_key_complete_visibility",
            "responsive_focus_key_font_floor",
            "fixed_grammar_key",
            "portrait_teaching_drawer",
            "transport_slot_stability",
            "teaching_annotation_disclosure",
            "focused_geometry_stroke_and_dash_floor",
            "responsive_boundary_disclosure",
        ):
            self.assertTrue(gates[gate_id]["passed"], gates[gate_id]["failures"])
        self.assertTrue(
            gates["three_dimensional_point_clipping"]["passed"],
            gates["three_dimensional_point_clipping"]["failures"],
        )
        self.assertTrue(
            gates["three_dimensional_label_layout"]["passed"],
            gates["three_dimensional_label_layout"]["failures"],
        )
        self.assertTrue(gates["legend_scope"]["passed"])
        self.assertEqual(
            gates["legend_scope"]["requested_segment_ids"],
            [],
        )
        self.assertTrue(gates["legend_scope"]["no_request_is_valid"])
        occupancy = gates["occupancy_review"]
        self.assertFalse(occupancy["passed"], occupancy)
        self.assertEqual(occupancy["status"], "pending")
        self.assertTrue(occupancy["exact_coverage_required"])
        self.assertEqual(occupancy["detected_risk_evaluation_count"], 15)
        self.assertEqual(occupancy["reviewed_evaluation_count"], 15)
        self.assertEqual(occupancy["live_confirmation_status"], "pending")
        self.assertEqual(
            occupancy["resolution_counts"],
            {"live_approved": 0, "live_rejected": 0, "unresolved": 15},
        )
        self.assertEqual(occupancy["missing_reviews"], [])
        self.assertEqual(occupancy["extra_reviews"], [])
        self.assertEqual(occupancy["malformed_reviews"], [])

        composition_gate = gates["annotated_two_dimensional_physical_composition"]
        self.assertEqual(composition_gate["evaluation_count"], 55)
        self.assertEqual(
            composition_gate["metric"],
            "rendered_pixel_ratio_to_full_stage",
        )
        self.assertEqual(
            composition_gate["legacy_physical_defect_policies"],
            quality.LEGACY_PHYSICAL_DEFECT_POLICIES,
        )
        self.assertEqual(
            composition_gate["candidate_standard_overlay_widths_px"],
            list(course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX),
        )
        self.assertTrue(composition_gate["widest_width_wins_exact_area_ties"])
        self.assertEqual(composition_gate["legacy_defective_evaluation_count"], 19)
        self.assertTrue(composition_gate["requires_maximum_render_area_candidate"])
        self.assertTrue(composition_gate["requires_no_viewport_regression"])
        self.assertEqual(
            [item["viewport_id"] for item in composition_gate["viewport_summary"]],
            [viewport["id"] for viewport in quality.VIEWPORTS],
        )
        self.assertTrue(
            all(
                item["evaluation_count"] == 11 and item["minimum_gain_ratio"] >= 1.0
                for item in composition_gate["viewport_summary"]
            )
        )

        three_composition_gate = gates[
            "annotated_three_dimensional_physical_composition"
        ]
        self.assertEqual(three_composition_gate["segment_count"], 5)
        self.assertEqual(three_composition_gate["viewport_count"], 5)
        self.assertEqual(three_composition_gate["evaluation_count"], 25)
        self.assertEqual(
            three_composition_gate["candidate_standard_overlay_widths_px"],
            list(course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX),
        )
        self.assertTrue(three_composition_gate["widest_width_wins_exact_area_ties"])
        self.assertTrue(
            three_composition_gate["requires_maximum_physical_area_candidate"]
        )
        self.assertTrue(three_composition_gate["requires_no_viewport_regression"])
        self.assertEqual(
            three_composition_gate["minimum_observed_standard_profile_canvas_width_px"],
            462,
        )

        for segment in self.registry["segments"]:
            for evaluation in segment["quality_vector"]["viewport_evaluations"]:
                overlay = evaluation["teaching_overlay"]
                self.assertEqual(overlay["residual_collision_count"], 0)
                self.assertEqual(overlay["residual_collision_ids"], [])
                self.assertEqual(
                    overlay["spatial_suppressed_ids"],
                    overlay["raw_collision_ids"],
                )
                self.assertTrue(overlay["suppressed_labels_covered_by_focus_key"])
                self.assertFalse(overlay["viewport_clipped"])
                self.assertFalse(overlay["masthead_clipped"])
                self.assertFalse(overlay["transport_clipped"])
                self.assertFalse(overlay["stage_clipped"])
                self.assertTrue(overlay["within_stage_coverage"])
                if overlay["compact_kind_cue_required"]:
                    self.assertTrue(overlay["compact_kind_cue_preserved"])
                    self.assertEqual(overlay["compact_kind_cue_missing_css"], [])
                else:
                    self.assertIsNone(overlay["compact_kind_cue_preserved"])
                correspondence = evaluation["fixed_focus_key"][
                    "numbered_geometry_correspondence"
                ]
                self.assertTrue(correspondence["passed"], correspondence)
                self.assertEqual(correspondence["missing_marker_ids"], [])
                self.assertEqual(correspondence["anchor_covered_by_overlay_ids"], [])
                self.assertEqual(correspondence["leader_overlay_crossing_ids"], [])
                self.assertEqual(correspondence["visible_label_collision_ids"], [])
                self.assertEqual(
                    correspondence["leader_visible_label_crossing_ids"], []
                )
                self.assertEqual(correspondence["leader_marker_crossing_ids"], [])
                self.assertEqual(correspondence["marker_leader_crossing_ids"], [])
                self.assertEqual(correspondence["leader_leader_crossing_ids"], [])
                self.assertEqual(
                    correspondence["anchor_covered_by_prior_marker_ids"], []
                )
                self.assertEqual(correspondence["future_anchor_obstruction_ids"], [])
                expected_runtime_order = [
                    copy_id
                    for copy_id in evaluation["fixed_focus_key"]["chip_ids"]
                    if copy_id in set(correspondence["fallback_ids"])
                ]
                self.assertEqual(correspondence["fallback_ids"], expected_runtime_order)
                self.assertLessEqual(
                    correspondence["maximum_displacement_px"],
                    quality.MAX_FOCUS_MARKER_DISPLACEMENT_PX,
                )
                self.assertTrue(evaluation["header_flow"]["passed"])
                self.assertTrue(evaluation["header_flow"]["focus_key_visible"])
                boundary = evaluation["fixed_boundary_note"]
                self.assertGreaterEqual(boundary["font_px"], 10.0)
                self.assertEqual(
                    boundary["visible_clauses"],
                    ["source_gated", "teaching_reference_not_as_built"],
                )

                two_dimensional = evaluation.get("two_dimensional")
                if overlay["present"] and two_dimensional is not None:
                    visual_stage = evaluation["visual_stage"]
                    self.assertFalse(overlay["initially_visible"])
                    self.assertEqual(
                        visual_stage["fit_policy"],
                        "full_stage_no_initial_overlay",
                    )
                    if overlay["box"] is not None:
                        open_visual_stage = evaluation["open_visual_stage"]
                        self.assertEqual(
                            open_visual_stage["fit_policy"],
                            "max_render_area_full_available_pane",
                        )
                        self.assertFalse(
                            quality._boxes_intersect(
                                open_visual_stage,
                                overlay["box"],
                                gap=quality.TEACHING_DOCK_GAP_PX - 0.01,
                            )
                        )
                    else:
                        self.assertEqual(evaluation["viewport_id"], "390x844")
                    self.assertGreaterEqual(
                        two_dimensional["rendered_pixel_area"] + 0.01,
                        two_dimensional["legacy_rendered_pixel_area"],
                    )
                    self.assertGreaterEqual(
                        two_dimensional["rendered_pixel_ratio_to_full_stage"]
                        + 0.000001,
                        two_dimensional["legacy_rendered_pixel_ratio_to_full_stage"],
                    )
                    defect_policy = quality.LEGACY_PHYSICAL_DEFECT_POLICIES.get(
                        evaluation["viewport_id"]
                    )
                    if (
                        defect_policy
                        and two_dimensional["legacy_rendered_pixel_ratio_to_full_stage"]
                        < defect_policy["maximum_full_stage_ratio"]
                    ):
                        self.assertGreaterEqual(
                            two_dimensional["rendered_pixel_ratio_to_full_stage"]
                            + 0.000001,
                            two_dimensional["legacy_rendered_pixel_ratio_to_full_stage"]
                            * defect_policy["minimum_gain_ratio"],
                        )
                    self.assertTrue(
                        two_dimensional["max_render_area_candidate_selected"]
                    )
                    self.assertAlmostEqual(
                        two_dimensional["rendered_pixel_area"],
                        two_dimensional["max_candidate_rendered_pixel_area"],
                        delta=0.01,
                    )
                if "three_dimensional" in evaluation:
                    self.assertEqual(
                        evaluation["three_dimensional"]["clipped_point_count"], 0
                    )
                    self.assertEqual(
                        evaluation["three_dimensional"]["lifecycle_chip_layout"],
                        "hidden_spatially_visible_in_fixed_key",
                    )
                    self.assertEqual(
                        evaluation["three_dimensional"][
                            "fixed_key_fallback_missing_ids"
                        ],
                        [],
                    )
                    self.assertTrue(
                        evaluation["three_dimensional"]["fixed_key_fallback_complete"]
                    )
                    self.assertEqual(
                        evaluation["three_dimensional"][
                            "residual_label_collision_count"
                        ],
                        0,
                    )
                    self.assertEqual(
                        evaluation["three_dimensional"]["residual_stage_clip_count"],
                        0,
                    )

    def test_portrait_focus_key_contract_covers_all_focus_policy_segments(
        self,
    ) -> None:
        portrait_viewport = next(
            viewport
            for viewport in quality.VIEWPORTS
            if viewport["id"] == quality.PORTRAIT_VIEWPORT_ID
        )
        stage = quality._stage_box(portrait_viewport)
        self.assertEqual(stage["y"], course_runtime.PORTRAIT_MASTHEAD_HEIGHT_PX)
        self.assertEqual(
            stage["height"],
            int(portrait_viewport["height"])
            - course_runtime.PORTRAIT_MASTHEAD_HEIGHT_PX
            - course_runtime.PORTRAIT_TRANSPORT_HEIGHT_PX,
        )

        gate = self.registry["visual_gates"]["portrait_focus_key_complete_visibility"]
        self.assertTrue(gate["passed"], gate["failures"])
        self.assertEqual(gate["status"], "passed")
        self.assertEqual(
            gate["evidence_scope"],
            quality.PORTRAIT_FOCUS_KEY_EVIDENCE_SCOPE,
        )
        self.assertEqual(gate["viewport_id"], quality.PORTRAIT_VIEWPORT_ID)
        self.assertEqual(gate["segment_count"], course_runtime.EXPECTED_SEGMENTS)
        self.assertEqual(
            gate["focus_policy_segment_count"], course_runtime.EXPECTED_SEGMENTS
        )
        self.assertEqual(
            gate["evaluated_focus_policy_segment_count"],
            course_runtime.EXPECTED_SEGMENTS,
        )
        self.assertEqual(gate["not_applicable_segment_count"], 0)
        self.assertTrue(gate["exact_coverage_passed"])
        self.assertEqual(gate["failure_count"], 0)
        self.assertEqual(gate["failures"], [])

        runtime_by_id = {
            segment["segment_id"]: segment for segment in self.runtime["segments"]
        }
        evidence = self.ledgers[self.course["meta"]["master_evidence_ledger"]]
        for segment in self.registry["segments"]:
            portrait = next(
                evaluation
                for evaluation in segment["quality_vector"]["viewport_evaluations"]
                if evaluation["viewport_id"] == quality.PORTRAIT_VIEWPORT_ID
            )
            record = portrait["portrait_focus_key"]
            expected_entries = course_runtime.focus_key_entries(
                runtime_by_id[segment["segment_id"]],
                self.master,
                evidence,
            )
            self.assertTrue(record["applicable"])
            self.assertTrue(record["passed"], record)
            self.assertEqual(record["status"], "passed")
            self.assertEqual(record["entries"], expected_entries)
            self.assertEqual(record["entry_count"], len(expected_entries))
            self.assertFalse(
                record["estimate"]["focus_key"]["horizontal_paging_required"]
            )
            self.assertTrue(record["estimate"]["estimated_complete_key_fit"])
            self.assertTrue(portrait["header_flow"]["passed"])
            self.assertEqual(
                portrait["header_flow"]["measurement_scope"],
                "total_masthead_box",
            )
            self.assertEqual(
                portrait["header_flow"]["focus_key_height_px"],
                record["estimate"]["focus_key"]["estimated_height_px"],
            )

    def test_portrait_teaching_drawer_is_closed_by_default_and_exactly_covered(
        self,
    ) -> None:
        gate = self.registry["visual_gates"]["portrait_teaching_drawer"]
        self.assertTrue(gate["passed"], gate["failures"])
        self.assertEqual(gate["status"], "passed")
        self.assertEqual(
            gate["evidence_scope"],
            quality.PORTRAIT_TEACHING_DRAWER_EVIDENCE_SCOPE,
        )
        self.assertTrue(gate["closed_state_only"])
        self.assertEqual(gate["live_open_state_review"], "pending")
        self.assertEqual(gate["segment_count"], course_runtime.EXPECTED_SEGMENTS)
        self.assertEqual(gate["annotated_segment_count"], 16)
        self.assertEqual(gate["not_applicable_segment_count"], 10)
        self.assertEqual(gate["evaluation_count"], course_runtime.EXPECTED_SEGMENTS)
        self.assertEqual(gate["failure_count"], 0)
        self.assertEqual(gate["failures"], [])
        self.assertTrue(gate["source_contract"]["passed"])
        self.assertEqual(
            gate["source_contract"]["drawer_box"],
            {"x": 72, "y": 360, "width": 318, "height": 410},
        )

        runtime_by_id = {
            segment["segment_id"]: segment for segment in self.runtime["segments"]
        }
        covered = []
        for segment in self.registry["segments"]:
            portrait = next(
                evaluation
                for evaluation in segment["quality_vector"]["viewport_evaluations"]
                if evaluation["viewport_id"] == quality.PORTRAIT_VIEWPORT_ID
            )
            overlay = portrait["teaching_overlay"]
            annotated = (
                runtime_by_id[segment["segment_id"]]["visual"]["annotation"] is not None
            )
            self.assertFalse(overlay["initially_visible"])
            self.assertIsNone(overlay["box"])
            if annotated:
                covered.append(segment["segment_id"])
                self.assertTrue(overlay["present"])
                self.assertTrue(overlay["available_on_demand"])
                self.assertEqual(overlay["interaction_mode"], "portrait_toggle_drawer")
                self.assertTrue(overlay["drawer_contract"]["passed"])
            else:
                self.assertFalse(overlay["present"])
                self.assertFalse(overlay["available_on_demand"])
                self.assertEqual(overlay["interaction_mode"], "not_applicable")
        self.assertEqual(covered, gate["covered_segment_ids"])

    def test_round_6_responsive_gates_have_exact_static_coverage(self) -> None:
        gates = self.registry["visual_gates"]

        short = gates["short_height_focus_key_complete_visibility"]
        self.assertTrue(short["passed"], short["failures"])
        self.assertEqual(short["viewport_id"], "844x390")
        self.assertEqual(short["segment_count"], 26)
        self.assertEqual(short["evaluation_count"], 26)
        self.assertEqual(short["focus_policy_segment_count"], 26)
        self.assertTrue(short["exact_coverage_passed"])
        self.assertEqual(short["maximum_allowed_width_px"], 476.0)
        self.assertEqual(short["maximum_allowed_height_px"], 40.0)
        self.assertEqual(short["minimum_observed_font_px"], 10.0)
        self.assertEqual(short["minimum_observed_index_font_px"], 10.0)
        self.assertEqual(short["opening_question_font_px"], 10.0)
        self.assertEqual(short["required_masthead_safety_margin_px"], 8.0)
        self.assertGreaterEqual(
            short["minimum_observed_masthead_safety_margin_px"],
            short["required_masthead_safety_margin_px"],
        )

        tablet = gates["tablet_focus_key_complete_visibility"]
        self.assertTrue(tablet["passed"], tablet["failures"])
        self.assertEqual(tablet["viewport_id"], "1024x768")
        self.assertEqual(tablet["evaluation_count"], 26)
        self.assertEqual(tablet["maximum_allowed_height_px"], 44.0)
        self.assertEqual(tablet["minimum_observed_font_px"], 10.0)
        self.assertEqual(tablet["minimum_observed_index_font_px"], 10.0)

        desktop = gates["desktop_focus_key_complete_visibility"]
        self.assertTrue(desktop["passed"], desktop["failures"])
        self.assertEqual(desktop["viewport_ids"], ["1920x1080", "1440x900"])
        self.assertEqual(desktop["segment_count"], 26)
        self.assertEqual(desktop["viewport_count"], 2)
        self.assertEqual(desktop["evaluation_count"], 52)
        self.assertEqual(desktop["expected_evaluation_count"], 52)
        self.assertTrue(desktop["exact_coverage_passed"])
        self.assertFalse(desktop["horizontal_paging_required"])
        self.assertEqual(
            desktop["content_width_px_by_viewport"],
            {"1920x1080": 1372.0, "1440x900": 892.0},
        )
        self.assertEqual(desktop["maximum_allowed_height_px"], 41.0)
        self.assertEqual(desktop["minimum_observed_font_px"], 10.0)
        self.assertEqual(desktop["minimum_observed_index_font_px"], 10.0)

        typography = gates["responsive_focus_key_font_floor"]
        self.assertTrue(typography["passed"], typography["failures"])
        self.assertEqual(typography["scope"], "all_segments_all_viewports")
        self.assertEqual(typography["segment_count"], 26)
        self.assertEqual(typography["viewport_count"], 5)
        self.assertEqual(typography["evaluation_count"], 130)
        self.assertEqual(typography["expected_evaluation_count"], 130)
        self.assertTrue(typography["exact_coverage_passed"])
        self.assertEqual(typography["minimum_observed_text_font_px"], 10.0)
        self.assertEqual(typography["minimum_observed_index_font_px"], 10.0)
        self.assertEqual(
            typography["aria_label"],
            "Focus key: visual grammar and numbered topology labels",
        )

        stroke = gates["focused_geometry_stroke_and_dash_floor"]
        self.assertTrue(stroke["passed"], stroke["failures"])
        self.assertEqual(stroke["scope"], "all_two_dimensional_segments_all_viewports")
        self.assertEqual(stroke["segment_count"], 15)
        self.assertEqual(stroke["viewport_count"], 5)
        self.assertEqual(stroke["evaluation_count"], 75)
        self.assertEqual(stroke["expected_evaluation_count"], 75)
        self.assertEqual(stroke["minimum_observed_stroke_px"], 1.5)
        self.assertEqual(stroke["minimum_observed_dash_px"], 1.0)
        self.assertTrue(stroke["dashed_geometry_evaluation_count"])
        self.assertEqual(
            stroke["evidence_scope"],
            "deterministic_static_model_not_live_browser",
        )

        transport = gates["transport_slot_stability"]
        self.assertTrue(transport["passed"], transport["failures"])
        self.assertEqual(transport["segment_count"], 26)
        self.assertEqual(transport["viewport_count"], 5)
        self.assertEqual(transport["evaluation_count"], 130)
        self.assertEqual(
            transport["annotated_segment_count"]
            + transport["unannotated_segment_count"],
            26,
        )
        self.assertTrue(
            all(record["row_count"] == 1 for record in transport["evaluations"])
        )
        self.assertEqual(
            {
                record["observed_stage_bottom_inset_px"]
                for record in transport["evaluations"]
            },
            {58, 74},
        )

        grammar = gates["fixed_grammar_key"]
        self.assertTrue(grammar["passed"], grammar["failures"])
        self.assertEqual(grammar["grammar_entry_count"], 7)
        self.assertEqual(grammar["evaluation_count"], 5)
        self.assertTrue(grammar["projected_map_legend_suppressed"])

        disclosure = gates["teaching_annotation_disclosure"]
        self.assertTrue(disclosure["passed"], disclosure["failures"])
        self.assertEqual(disclosure["segment_count"], 26)
        self.assertEqual(disclosure["viewport_count"], 5)
        self.assertEqual(disclosure["evaluation_count"], 130)
        self.assertTrue(disclosure["closed_by_default"])
        self.assertEqual(
            disclosure["geometry_preservation_target"],
            "labels_only_full_stage",
        )
        self.assertTrue(
            all(
                not record["initially_visible"]
                and record["default_visual_geometry"] == "labels_only_full_stage"
                for record in disclosure["evaluations"]
            )
        )

    def test_round_6_fit_and_stroke_gates_fail_closed_under_mutation(self) -> None:
        with patch.dict(
            course_runtime._COMPACT_FOCUS_LABELS,
            {"mv_bus": "X" * 20},
        ):
            adversarial_key = quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.runtime,
                source_digest="adversarial-short-key-width",
                occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            )
        key_gate = adversarial_key["visual_gates"][
            "short_height_focus_key_complete_visibility"
        ]
        self.assertFalse(key_gate["passed"])
        self.assertTrue(
            any(
                "compact_label_width_exceeded" in failure["failure_reasons"]
                for failure in key_gate["failures"]
            )
        )
        desktop_key_gate = adversarial_key["visual_gates"][
            "desktop_focus_key_complete_visibility"
        ]
        self.assertFalse(desktop_key_gate["passed"])
        self.assertTrue(
            any(
                "compact_label_width_exceeded" in failure["failure_reasons"]
                for failure in desktop_key_gate["failures"]
            )
        )

        with patch.object(
            course_runtime,
            "DESKTOP_FOCUS_KEY_MAX_HEIGHT_PX",
            40.0,
        ):
            adversarial_desktop_height = quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.runtime,
                source_digest="adversarial-desktop-key-height",
                occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            )
        height_gate = adversarial_desktop_height["visual_gates"][
            "desktop_focus_key_complete_visibility"
        ]
        self.assertFalse(height_gate["passed"])
        self.assertTrue(
            any(
                "compact_key_height_exceeded" in failure["failure_reasons"]
                for failure in height_gate["failures"]
            )
        )

        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(
                "font-size: __FOCUS_KEY_INDEX_FONT_PX__px;",
                "font-size: 9px;",
                1,
            ),
        ):
            adversarial_typography = quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.runtime,
                source_digest="adversarial-focus-index-font",
                occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            )
        typography_gate = adversarial_typography["visual_gates"][
            "responsive_focus_key_font_floor"
        ]
        self.assertFalse(typography_gate["passed"])
        self.assertFalse(typography_gate["source_contract"]["passed"])
        self.assertEqual(typography_gate["failure_count"], 130)

        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(
                "vector-effect: non-scaling-stroke;",
                "vector-effect: none;",
                1,
            ),
        ):
            adversarial_stroke = quality.compile_quality_registry(
                self.course,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                self.runtime,
                source_digest="adversarial-scaling-strokes",
                occupancy_reviews=self.ratchet_manifest["occupancy_reviews"],
            )
        stroke_gate = adversarial_stroke["visual_gates"][
            "focused_geometry_stroke_and_dash_floor"
        ]
        self.assertFalse(stroke_gate["passed"])
        self.assertFalse(stroke_gate["source_contract"]["passed"])
        self.assertEqual(stroke_gate["failure_count"], 75)
        self.assertTrue(
            all(
                "focused_non_scaling_source_contract_failed"
                in failure["failure_reasons"]
                for failure in stroke_gate["failures"]
            )
        )

    def test_round_3_teaching_frame_repairs_are_claim_bound(self) -> None:
        runtime_by_id = {
            segment["segment_id"]: segment for segment in self.runtime["segments"]
        }
        expected = {
            "s01_fire_to_electricity": [
                ["turbine_generator_conversion_reference"],
                ["gas_authorization"],
                ["installed_turbine_presence"],
                [
                    "installed_turbine_configuration_unknown",
                    "operating_posture_unknown",
                ],
            ],
            "s02_generator_terminal": [
                ["model_voltage_range", "site_voltage_unknown"],
                ["campus_interface_design"],
                [
                    "campus_interface_unknown",
                    "site_generator_configuration_boundary",
                ],
            ],
            "s08_rack_voltage_descent": [
                ["rack_ac_unknown"],
                ["rack_dc_product_reference"],
                ["operating_rack_configuration_unknown"],
            ],
            "s15_water_accounting": [
                ["initial_fill_design"],
                ["anticipated_maintenance"],
                ["measured_operating_consumption_unknown"],
            ],
        }
        for segment_id, claim_groups in expected.items():
            with self.subTest(segment_id=segment_id):
                annotation = runtime_by_id[segment_id]["visual"]["annotation"]
                self.assertIsNotNone(annotation)
                self.assertEqual(
                    [item["claim_ids"] for item in annotation["items"]],
                    claim_groups,
                )
                portrait = next(
                    evaluation
                    for evaluation in next(
                        segment
                        for segment in self.registry["segments"]
                        if segment["segment_id"] == segment_id
                    )["quality_vector"]["viewport_evaluations"]
                    if evaluation["viewport_id"] == quality.PORTRAIT_VIEWPORT_ID
                )
                self.assertTrue(portrait["teaching_overlay"]["available_on_demand"])

    def test_marker_segment_intersection_detects_crossing_and_collinearity(
        self,
    ) -> None:
        self.assertTrue(
            quality._segments_intersect(
                (0.0, 0.0), (10.0, 10.0), (0.0, 10.0), (10.0, 0.0)
            )
        )
        self.assertTrue(
            quality._segments_intersect(
                (0.0, 0.0), (10.0, 0.0), (5.0, 0.0), (15.0, 0.0)
            )
        )
        self.assertFalse(
            quality._segments_intersect((0.0, 0.0), (4.0, 0.0), (5.0, 0.0), (10.0, 0.0))
        )

    def test_compact_kind_cue_gate_is_derived_from_runtime_css(self) -> None:
        contract = course_runtime.compact_kind_cue_contract("sequence", "short_height")
        self.assertTrue(contract["preserved"])
        required_token = contract["required_css"][1]
        with patch.object(
            course_runtime,
            "COURSE_CSS",
            course_runtime.COURSE_CSS.replace(required_token, ""),
        ):
            broken = course_runtime.compact_kind_cue_contract(
                "sequence", "short_height"
            )
        self.assertFalse(broken["preserved"])
        self.assertEqual(broken["missing_css"], [required_token])

        for profile in ("standard", "narrow", "short_height"):
            funnel = course_runtime.compact_kind_cue_contract("funnel", profile)
            parallel = course_runtime.compact_kind_cue_contract("parallel", profile)
            self.assertTrue(funnel["required"])
            self.assertTrue(funnel["preserved"])
            self.assertEqual(len(funnel["required_css"]), 5)
            self.assertTrue(parallel["required"])
            self.assertTrue(parallel["preserved"])

    def test_semantic_annotation_grid_matches_parallel_and_routes_css(self) -> None:
        runtime_by_id = {
            segment["segment_id"]: segment for segment in self.runtime["segments"]
        }
        annotations = {
            segment_id: runtime_by_id[segment_id]["visual"]["annotation"]
            for segment_id in (
                "s16_close_atmosphere",
                "s24_megawatts_to_tokens",
            )
        }
        self.assertEqual(annotations["s16_close_atmosphere"]["kind"], "parallel")
        self.assertEqual(annotations["s24_megawatts_to_tokens"]["kind"], "routes")

        expected = {
            "standard": {
                "parallel_widths": [350.0, 161.0, 161.0, 350.0],
                "parallel_height": 97.25,
                "routes_widths": [161.0, 161.0, 161.0, 161.0],
                "routes_height": 62.5,
            },
            "narrow": {
                "parallel_widths": [354.0, 166.0, 166.0, 354.0],
                "parallel_height": 83.5,
                "routes_widths": [166.0, 166.0, 166.0, 166.0],
                "routes_height": 54.0,
            },
            "short_height": {
                "parallel_widths": [358.0, 170.5, 170.5, 358.0],
                "parallel_height": 60.5,
                "routes_widths": [108.0, 108.0, 108.0, 108.0],
                "routes_height": 39.0,
            },
        }
        for profile, contract in expected.items():
            observed_widths: list[float] = []

            def one_line(
                _text: str,
                width: float,
                _font_size: float,
                widths: list[float] = observed_widths,
            ) -> int:
                widths.append(width)
                return 1

            with patch.object(quality, "_wrapped_line_count", side_effect=one_line):
                height = quality._teaching_grid_height(
                    annotations["s16_close_atmosphere"], 371.0, profile
                )
            self.assertEqual(observed_widths, contract["parallel_widths"])
            self.assertEqual(height, contract["parallel_height"])

            observed_widths.clear()
            with patch.object(quality, "_wrapped_line_count", side_effect=one_line):
                height = quality._teaching_grid_height(
                    annotations["s24_megawatts_to_tokens"], 371.0, profile
                )
            self.assertEqual(observed_widths, contract["routes_widths"])
            self.assertEqual(height, contract["routes_height"])

    def test_p1_swatch_prefix_is_modeled_in_every_responsive_profile(self) -> None:
        annotation = next(
            segment
            for segment in self.runtime["segments"]
            if segment["segment_id"] == "p1_read_the_machine"
        )["visual"]["annotation"]
        expected_text_widths = {
            "standard": 313.0,
            "narrow": 136.0,
            "short_height": 78.0,
        }
        for profile, expected_width in expected_text_widths.items():
            observed_widths: list[float] = []

            def one_line(
                _text: str,
                width: float,
                _font_size: float,
                widths: list[float] = observed_widths,
            ) -> int:
                widths.append(width)
                return 1

            with patch.object(quality, "_wrapped_line_count", side_effect=one_line):
                quality._teaching_grid_height(
                    annotation,
                    371.0,
                    profile,
                    "p1_read_the_machine",
                )
            self.assertEqual(observed_widths, [expected_width] * 4)

        p1 = next(
            segment
            for segment in self.registry["segments"]
            if segment["segment_id"] == "p1_read_the_machine"
        )
        overlays = {
            evaluation["viewport_id"]: evaluation["teaching_overlay"]
            for evaluation in p1["quality_vector"]["viewport_evaluations"]
        }
        self.assertEqual(overlays["844x390"]["box"]["height"], 185.95)
        self.assertEqual(
            overlays["844x390"]["stage_edge_clearances_px"],
            {"top": 8.05, "right": 374.0, "bottom": 8.0, "left": 8.0},
        )
        self.assertIsNone(overlays["390x844"]["box"])
        self.assertEqual(
            overlays["390x844"]["drawer_contract"]["drawer_box"]["height"],
            410,
        )

    def test_adaptive_overlay_width_uses_widest_maximum_area_choice(self) -> None:
        expected_1024_widths = {
            "p0_gigawatt_not_workload": 240,
            "p1_read_the_machine": 240,
            "s17_interconnection_schedule": 240,
            "s18_long_lead_equipment": 240,
            "s19_fast_load_slow_grid": 390,
            "s20_build_sequence": 240,
            "s21_capital_ownership": 240,
            "s22_capital_risk": 240,
            "s23_business_models": 240,
            "s24_megawatts_to_tokens": 240,
        }
        for segment in self.registry["segments"]:
            if segment["segment_id"] not in expected_1024_widths:
                continue
            evaluation = next(
                item
                for item in segment["quality_vector"]["viewport_evaluations"]
                if item["viewport_id"] == "1024x768"
            )
            visual_stage = evaluation["open_visual_stage"]
            self.assertEqual(
                visual_stage["selected_standard_overlay_width_px"],
                expected_1024_widths[segment["segment_id"]],
            )
            self.assertEqual(
                visual_stage["standard_overlay_width_candidates_px"],
                list(course_runtime.TEACHING_OVERLAY_STANDARD_WIDTH_CANDIDATES_PX),
            )
            self.assertEqual(
                evaluation["teaching_overlay"]["selected_standard_width_px"],
                expected_1024_widths[segment["segment_id"]],
            )

    def test_parallel_annotation_requires_four_semantic_items(self) -> None:
        invalid_visuals = copy.deepcopy(self.visuals)
        invalid_visuals["segments"]["s16_close_atmosphere"]["annotation"]["items"].pop()
        with self.assertRaisesRegex(
            course_runtime.CourseRuntimeError,
            "parallel requires exactly four items",
        ):
            course_runtime.compile_registry(
                self.course,
                self.cameras,
                self.master,
                self.layout,
                self.scene,
                self.ledgers,
                invalid_visuals,
                source_digest=self.runtime_digest,
            )

    def test_responsive_spatial_labels_fall_back_to_fixed_focus_key(self) -> None:
        target_ids = {"844x390", "390x844"}
        two_dimensional_segments = [
            segment
            for segment in self.registry["segments"]
            if segment["render_mode"] == "2d"
        ]
        self.assertEqual(len(two_dimensional_segments), 15)
        for segment in two_dimensional_segments:
            expected_chip_count = len(
                dict.fromkeys(
                    [
                        *next(
                            runtime_segment
                            for runtime_segment in self.runtime["segments"]
                            if runtime_segment["segment_id"] == segment["segment_id"]
                        )["visual"]["label_copy_ids"],
                        *next(
                            runtime_segment
                            for runtime_segment in self.runtime["segments"]
                            if runtime_segment["segment_id"] == segment["segment_id"]
                        )["reveal_copy_ids"],
                    ]
                )
            )
            for evaluation in segment["quality_vector"]["viewport_evaluations"]:
                if evaluation["viewport_id"] not in target_ids:
                    continue
                vector = evaluation["two_dimensional"]
                self.assertLess(
                    vector["projected_base_font_px"],
                    vector["minimum_spatial_font_px"],
                )
                self.assertEqual(vector["spatial_label_count"], 0)
                expected_legend_count = 0
                self.assertEqual(
                    vector["legend_visible_label_count"], expected_legend_count
                )
                if expected_legend_count:
                    self.assertGreater(vector["estimated_label_pixels"], 0)
                else:
                    self.assertEqual(vector["estimated_label_pixels"], 0)
                self.assertEqual(
                    evaluation["fixed_focus_key"]["chip_count"],
                    expected_chip_count,
                )
                self.assertEqual(
                    evaluation["fixed_focus_key"]["font_px"],
                    quality.FOCUS_KEY_FONT_PX,
                )
                correspondence = evaluation["fixed_focus_key"][
                    "numbered_geometry_correspondence"
                ]
                self.assertEqual(
                    correspondence["fallback_ids"], correspondence["marker_ids"]
                )
                self.assertEqual(correspondence["missing_marker_ids"], [])
                self.assertEqual(
                    correspondence["marker_count"],
                    expected_chip_count
                    - len(evaluation["fixed_focus_key"]["grammar_chip_ids"]),
                )
                self.assertTrue(correspondence["passed"])

    def test_short_wide_three_dimensional_labels_fall_back_to_fixed_key(
        self,
    ) -> None:
        labels_runtime = quality._modeled_runtime(
            self.runtime,
            {"label_source": "current", "annotation_source": "none"},
        )
        labels_quality = quality.compile_quality_registry(
            self.course,
            self.master,
            self.layout,
            self.scene,
            self.ledgers,
            labels_runtime,
            source_digest="test-digest",
        )
        segment = next(
            item
            for item in labels_quality["segments"]
            if item["segment_id"] == "s16_close_atmosphere"
        )
        evaluation = next(
            item
            for item in segment["quality_vector"]["viewport_evaluations"]
            if item["viewport_id"] == "844x390"
        )
        self.assertGreaterEqual(evaluation["visual_stage"]["width"], 400)
        self.assertLess(
            evaluation["visual_stage"]["height"],
            quality.shots.MIN_SPATIAL_LABEL_SURFACE_HEIGHT_PX,
        )
        three = evaluation["three_dimensional"]
        self.assertEqual(three["selected_label_box_count"], 0)
        self.assertEqual(
            three["layout_suppressed_label_ids"],
            sorted(evaluation["fixed_focus_key"]["chip_ids"]),
        )
        self.assertTrue(three["fixed_key_fallback_complete"])
        self.assertTrue(
            evaluation["fixed_focus_key"]["numbered_geometry_correspondence"]["passed"]
        )

    def test_protected_footnote_and_legend_contract_are_explicit(self) -> None:
        policy = self.registry["protected_copy_policy"]
        self.assertEqual(policy["map_copy_ids"], ["footnote"])
        self.assertEqual(policy["fixed_masthead_copy_id"], "footnote")
        self.assertTrue(policy["fixed_masthead_copy"])
        self.assertEqual(quality.PROTECTED_MAP_COPY_IDS, frozenset({"footnote"}))
        for segment in self.registry["segments"]:
            for evaluation in segment["quality_vector"]["viewport_evaluations"]:
                if "two_dimensional" in evaluation:
                    expected = 0
                    self.assertEqual(
                        evaluation["two_dimensional"]["legend_visible_label_count"],
                        expected,
                    )

    def test_dependency_graph_covers_every_required_stage(self) -> None:
        self.assertEqual(self.graph["dependency_path"], list(quality.GRAPH_STAGES))
        self.assertEqual(set(self.graph["stage_counts"]), set(quality.GRAPH_STAGES))
        self.assertTrue(all(self.graph["stage_counts"].values()))
        self.assertEqual(self.graph["stage_counts"]["segment"], 26)
        self.assertEqual(self.graph["stage_counts"]["shot"], 26)
        self.assertEqual(self.graph["stage_counts"]["frame"], 26)
        self.assertEqual(
            self.graph["stage_counts"]["evaluation"],
            26 * len(quality.VIEWPORTS),
        )
        self.assertEqual(
            set(self.graph["claim_node_types"]),
            {"topology_claim", "overlay_claim"},
        )
        frame_nodes = [node for node in self.graph["nodes"] if node["stage"] == "frame"]
        self.assertTrue(
            all(node["type"] == "provisional_frame_spec" for node in frame_nodes)
        )
        self.assertTrue(
            all(
                node["render_status"] == "pending_browser_capture"
                for node in frame_nodes
            )
        )
        self.assertTrue(all(node["capture_digest"] is None for node in frame_nodes))
        evaluation_nodes = [
            node for node in self.graph["nodes"] if node["stage"] == "evaluation"
        ]
        self.assertTrue(
            all(
                node["type"] == "modeled_viewport_evaluation"
                and node["evidence_status"] == "static_model_only"
                for node in evaluation_nodes
            )
        )
        self.assertEqual(
            {
                "frame_capture": "pending_browser_capture",
                "live_evaluation": "pending_browser_and_accessibility",
            },
            self.graph["completion_boundary"],
        )
        source_nodes = [
            node for node in self.graph["nodes"] if node["stage"] == "source"
        ]
        fact_nodes = [node for node in self.graph["nodes"] if node["stage"] == "fact"]
        self.assertTrue(
            all(
                {"publication_date", "review_date", "accessed_as_of", "date_note"}
                <= set(node)
                for node in source_nodes
            )
        )
        self.assertTrue(
            all({"value", "basis", "scope"} <= set(node) for node in fact_nodes)
        )

        node_stage = {node["id"]: node["stage"] for node in self.graph["nodes"]}
        allowed_stage_edges = {
            ("source", "fact"),
            ("fact", "topology"),
            ("topology", "segment"),
            ("segment", "segment"),
            ("segment", "shot"),
            ("shot", "frame"),
            ("frame", "evaluation"),
        }
        self.assertEqual(
            {
                (node_stage[edge["from"]], node_stage[edge["to"]])
                for edge in self.graph["edges"]
            },
            allowed_stage_edges,
        )
        transitions = [
            edge for edge in self.graph["edges"] if edge["type"] == "transitions_to"
        ]
        ordered_ids = [segment["segment_id"] for segment in self.runtime["segments"]]
        self.assertEqual(
            transitions,
            [
                {
                    "from": f"segment:{predecessor}",
                    "to": f"segment:{successor}",
                    "type": "transitions_to",
                }
                for predecessor, successor in pairwise(ordered_ids)
            ],
        )

    def test_claim_chain_evidence_and_full_inventory_resolve_in_graph(self) -> None:
        edges = {
            (edge["from"], edge["to"], edge["type"]) for edge in self.graph["edges"]
        }
        all_source_ids = {
            f"source:{ledger_id}:{source_id}"
            for ledger_id, ledger in self.ledgers.items()
            for source_id in ledger["sources"]
        }
        all_fact_ids = {
            f"fact:{ledger_id}:{fact_id}"
            for ledger_id, ledger in self.ledgers.items()
            for fact_id in ledger["facts"]
        }
        claim_fact_refs = {
            fact["ref"]
            for segment in self.runtime["segments"]
            for claim in segment["claims"]
            for fact in claim["facts"]
        }
        claim_fact_ids = {f"fact:{fact_ref}" for fact_ref in claim_fact_refs}
        claim_source_ids = set()
        for ledger_id, ledger in self.ledgers.items():
            for fact_id, fact in ledger["facts"].items():
                fact_ref = f"{ledger_id}:{fact_id}"
                if fact_ref not in claim_fact_refs:
                    continue
                fact_node = f"fact:{ledger_id}:{fact_id}"
                for source_id in fact["source_ids"]:
                    source_node = f"source:{ledger_id}:{source_id}"
                    claim_source_ids.add(source_node)
                    self.assertIn(
                        (
                            source_node,
                            fact_node,
                            "supports_fact",
                        ),
                        edges,
                    )

        graph_source_ids = {
            node["id"] for node in self.graph["nodes"] if node["stage"] == "source"
        }
        graph_fact_ids = {
            node["id"] for node in self.graph["nodes"] if node["stage"] == "fact"
        }
        self.assertEqual(graph_source_ids, claim_source_ids)
        self.assertEqual(graph_fact_ids, claim_fact_ids)
        self.assertEqual(self.graph["stage_counts"]["source"], len(claim_source_ids))
        self.assertEqual(self.graph["stage_counts"]["fact"], len(claim_fact_ids))

        inventory = self.graph["evidence_inventory"]
        self.assertEqual(
            set(inventory),
            {
                "policy",
                "total_source_count",
                "total_fact_count",
                "claim_chain_source_count",
                "claim_chain_fact_count",
                "inventory_only_source_ids",
                "inventory_only_fact_ids",
            },
        )
        self.assertEqual(inventory["policy"], quality.EVIDENCE_INVENTORY_POLICY)
        self.assertEqual(inventory["total_source_count"], len(all_source_ids))
        self.assertEqual(inventory["total_fact_count"], len(all_fact_ids))
        self.assertEqual(inventory["claim_chain_source_count"], len(claim_source_ids))
        self.assertEqual(inventory["claim_chain_fact_count"], len(claim_fact_ids))
        self.assertEqual(
            inventory["inventory_only_source_ids"],
            sorted(all_source_ids - claim_source_ids),
        )
        self.assertEqual(
            inventory["inventory_only_fact_ids"],
            sorted(all_fact_ids - claim_fact_ids),
        )

        for segment in self.runtime["segments"]:
            for claim in segment["claims"]:
                claim_node = f"topology:{segment['segment_id']}:{claim['id']}"
                for fact in claim["facts"]:
                    ledger_id, fact_id = fact["ref"].split(":", 1)
                    self.assertIn(
                        (
                            f"fact:{ledger_id}:{fact_id}",
                            claim_node,
                            "substantiates_topology",
                        ),
                        edges,
                    )

    def test_every_graph_node_is_on_a_complete_dependency_path(self) -> None:
        nodes = {node["id"]: node for node in self.graph["nodes"]}
        stage_index = {stage: index for index, stage in enumerate(quality.GRAPH_STAGES)}
        adjacency = {node_id: [] for node_id in nodes}
        reverse = {node_id: [] for node_id in nodes}
        for edge in self.graph["edges"]:
            source = edge["from"]
            target = edge["to"]
            if (
                stage_index[nodes[target]["stage"]]
                != stage_index[nodes[source]["stage"]] + 1
            ):
                continue
            adjacency[source].append(target)
            reverse[target].append(source)

        def closure(starts: set[str], graph: dict[str, list[str]]) -> set[str]:
            reached = set(starts)
            pending = list(starts)
            while pending:
                source = pending.pop()
                for target in graph[source]:
                    if target not in reached:
                        reached.add(target)
                        pending.append(target)
            return reached

        source_ids = {
            node_id for node_id, node in nodes.items() if node["stage"] == "source"
        }
        evaluation_ids = {
            node_id for node_id, node in nodes.items() if node["stage"] == "evaluation"
        }
        self.assertEqual(closure(source_ids, adjacency), set(nodes))
        self.assertEqual(closure(evaluation_ids, reverse), set(nodes))

    def test_topology_and_overlay_nodes_have_exact_physical_scope(self) -> None:
        nodes = {node["id"]: node for node in self.graph["nodes"]}
        multi_fact_claim_count = 0
        empty_overlay_fact_count = 0
        for segment in self.runtime["segments"]:
            for claim in segment["claims"]:
                multi_fact_claim_count += len(claim["facts"]) > 1
                node = nodes[f"topology:{segment['segment_id']}:{claim['id']}"]
                expected_nodes = sorted(
                    {
                        target["id"]
                        for fact in claim["facts"]
                        for target in fact["topology_targets"]
                        if target["kind"] == "node"
                    }
                )
                expected_edges = sorted(
                    {
                        target["id"]
                        for fact in claim["facts"]
                        for target in fact["topology_targets"]
                        if target["kind"] == "edge"
                    }
                )
                expected_targets = sorted(
                    {
                        (
                            target["kind"],
                            target["id"],
                            target["label"],
                            target["presence"],
                            target["lifecycle"],
                        )
                        for fact in claim["facts"]
                        for target in fact["topology_targets"]
                    }
                )
                actual_targets = sorted(
                    (
                        target["kind"],
                        target["id"],
                        target["label"],
                        target["presence"],
                        target["lifecycle"],
                    )
                    for target in node["topology_targets"]
                )
                self.assertEqual(expected_targets, actual_targets)
                expected_fact_topology_targets = {
                    fact["ref"]: [
                        {
                            "kind": target["kind"],
                            "id": target["id"],
                            "label": target["label"],
                            "presence": target["presence"],
                            "lifecycle": target["lifecycle"],
                        }
                        for target in fact["topology_targets"]
                    ]
                    for fact in claim["facts"]
                }
                self.assertEqual(
                    node["fact_topology_targets"],
                    expected_fact_topology_targets,
                )
                self.assertEqual(
                    set(node["fact_topology_targets"]),
                    set(node["fact_refs"]),
                )
                if claim["binding"] == "topology":
                    self.assertTrue(node["physically_bound"])
                    self.assertIsNone(node["overlay_scope"])
                    self.assertTrue(expected_nodes or expected_edges)
                else:
                    empty_overlay_fact_count += sum(
                        not fact["topology_targets"] for fact in claim["facts"]
                    )
                    self.assertFalse(node["physically_bound"])
                    self.assertEqual(expected_nodes, [])
                    self.assertEqual(expected_edges, [])
                    self.assertEqual(
                        node["overlay_scope"],
                        {
                            "kind": "segment_local",
                            "segment_id": segment["segment_id"],
                        },
                    )
        self.assertGreater(multi_fact_claim_count, 0)
        self.assertGreater(empty_overlay_fact_count, 0)

    def test_density_pressure_and_actual_worst_quality_deciles_are_explicit(
        self,
    ) -> None:
        protected = set(self.registry["protected_dense_segment_ids"])
        self.assertEqual(protected, set(quality.PROTECTED_DENSE_SEGMENTS))
        density_pressure = set(self.registry["density_pressure_decile"]["segment_ids"])
        self.assertEqual(
            density_pressure,
            {
                "s19_fast_load_slow_grid",
                "s21_capital_ownership",
                "s24_megawatts_to_tokens",
            },
        )
        self.assertLessEqual(density_pressure, protected)
        worst_quality = self.registry["worst_quality_decile"]
        self.assertEqual(
            set(worst_quality["segment_ids"]),
            {
                "s05_ppa_not_wire",
                "s07_building_power_train",
                "s09_watt_becomes_heat",
            },
        )
        self.assertEqual(
            worst_quality["metric"],
            "non_density_risk_occurrences_across_all_viewports",
        )
        by_id = {
            segment["segment_id"]: segment for segment in self.registry["segments"]
        }
        for segment_id in protected:
            segment = by_id[segment_id]
            self.assertTrue(segment["protected_dense_sentinel"])
            self.assertIn("dense_focus", segment["quality_vector"]["risk_flags"])

    def test_impact_cone_reaches_affected_viewport_evaluations(self) -> None:
        source_to_fact = next(
            edge
            for edge in self.graph["edges"]
            if edge["type"] == "supports_fact"
            and any(
                candidate["from"] == edge["to"]
                and candidate["type"] == "substantiates_topology"
                for candidate in self.graph["edges"]
            )
        )
        cone = quality.impact_cone(self.graph, source_to_fact["from"])
        self.assertIn(source_to_fact["to"], cone["by_stage"]["fact"])
        for stage in ("topology", "segment", "shot", "frame", "evaluation"):
            self.assertTrue(cone["by_stage"][stage], stage)
        self.assertEqual(cone, quality.impact_cone(self.graph, source_to_fact["from"]))
        with self.assertRaisesRegex(quality.QualityError, "unknown nodes"):
            quality.impact_cone(self.graph, "source:not:a-real-source")


if __name__ == "__main__":
    unittest.main()
