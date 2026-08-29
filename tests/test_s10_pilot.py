from __future__ import annotations

import importlib.util
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from gigawatt import scene, tokens, validate

ROOT = Path(__file__).resolve().parents[1]
PILOT = ROOT / "course" / "pilots" / "s10_two_rack_heat_paths.yaml"
NATIVE_GENERATOR = ROOT / "diagram" / "generate_s10_two_rack_heat_paths.py"
NATIVE_OUTPUT = ROOT / "diagram" / "s10_two_rack_heat_paths.html"
S10_NODES = {"die", "rack_air_load", "cold_plate", "rack_manifold"}
S10_EDGES = {
    "die_to_cold_plate_heat",
    "cold_plate_to_manifold_return",
    "manifold_to_cold_plate_supply",
}


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


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class S10PilotContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = validate._load_yaml_strict(validate.COURSE)
        cls.master = validate._load_yaml_strict(validate.DIAGRAM / "master.yaml")
        cls.scene = validate._load_yaml_strict(validate.DIAGRAM / "scene.yaml")
        cls.cameras = validate._load_yaml_strict(validate.DIAGRAM / "cameras.yaml")
        cls.pilot = validate._load_yaml_strict(PILOT)
        cls.segment = segment_by_id(cls.course, "s10_two_rack_heat_paths")
        cls.native = load_module("gigawatt_s10_native", NATIVE_GENERATOR)

    def test_s10_scope_and_evidence_boundary_are_exact(self) -> None:
        segment = self.segment
        self.assertEqual(S10_NODES, set(segment["node_ids"]))
        self.assertEqual(S10_EDGES, set(segment["edge_ids"]))
        self.assertEqual("data_hall_rack", segment["camera"]["anchor"])
        self.assertEqual("rack_cooling_split", segment["camera"]["shot"])
        self.assertEqual("3d", segment["camera"]["mode"])
        self.assertEqual([], segment["camera"]["reveal_ids"])
        self.assertEqual([], segment["camera"]["reveal_copy_ids"])

        evidence = segment["evidence"]
        self.assertEqual("evidence_ready", evidence["readiness"])
        self.assertEqual([], evidence["blocking_research"])
        self.assertEqual(
            {
                "design_to_as_built",
                "product_to_site_configuration",
                "conceptual_to_as_built",
            },
            set(evidence["promotion_guards"]),
        )
        self.assertEqual(
            [
                (
                    "rack_design_reference",
                    "design_reference",
                    [
                        "abilene:rack_platform_nvl72_design_reference",
                        "abilene:cooling_direct_to_chip_design",
                    ],
                ),
                (
                    "rack_component_split",
                    "product_reference",
                    [
                        "abilene:rack_air_cooled_components",
                        "abilene:rack_liquid_cooled_components",
                    ],
                ),
            ],
            [
                (claim["id"], claim["assertion"], claim["fact_refs"])
                for claim in evidence["claims"]
            ],
        )

    def test_transformations_are_coarse_untimed_manual_states(self) -> None:
        self.assertEqual(
            {
                "schema_version",
                "segment_id",
                "camera_anchor",
                "purpose",
                "transformations",
            },
            set(self.pilot),
        )
        self.assertEqual(self.segment["id"], self.pilot["segment_id"])
        self.assertEqual(self.segment["camera"]["anchor"], self.pilot["camera_anchor"])
        self.assertEqual(
            [
                "rack_context",
                "liquid_cooled_compute",
                "air_cooled_auxiliaries",
                "compare_paths",
            ],
            [transformation["id"] for transformation in self.pilot["transformations"]],
        )

        forbidden_prefixes = (
            "beat",
            "duration",
            "timing",
            "cadence",
            "script",
            "runtime",
            "autoplay",
        )
        forbidden_keys = sorted(
            key
            for key in walk_keys(self.pilot)
            if isinstance(key, str) and key.lower().startswith(forbidden_prefixes)
        )
        self.assertEqual([], forbidden_keys)

    def test_every_transformation_stays_inside_the_segment(self) -> None:
        master_edges = {edge["id"]: edge for edge in self.master["edges"]}
        covered_nodes: set[str] = set()
        covered_edges: set[str] = set()
        for transformation in self.pilot["transformations"]:
            self.assertEqual(
                {
                    "id",
                    "title",
                    "instruction",
                    "focus_nodes",
                    "focus_edges",
                    "pulse_edges",
                },
                set(transformation),
            )
            nodes = set(transformation["focus_nodes"])
            edges = set(transformation["focus_edges"])
            pulses = set(transformation["pulse_edges"])
            self.assertLessEqual(nodes, S10_NODES)
            self.assertLessEqual(edges, S10_EDGES)
            self.assertLessEqual(pulses, edges)
            for edge_id in edges:
                self.assertLessEqual(
                    {master_edges[edge_id]["from"], master_edges[edge_id]["to"]},
                    nodes,
                )
            covered_nodes.update(nodes)
            covered_edges.update(edges)

        self.assertEqual(S10_NODES, covered_nodes)
        self.assertEqual(S10_EDGES, covered_edges)

    def test_air_auxiliaries_stop_at_the_rack_boundary(self) -> None:
        air = next(
            transformation
            for transformation in self.pilot["transformations"]
            if transformation["id"] == "air_cooled_auxiliaries"
        )
        self.assertEqual(["rack_air_load"], air["focus_nodes"])
        self.assertEqual([], air["focus_edges"])
        self.assertEqual([], air["pulse_edges"])

        forbidden_nodes = {
            "cdu",
            "crah",
            "facility_loop",
            "air_cooled_chiller",
            "atmosphere",
        }
        forbidden_edges = {
            "rack_air_load_to_crah",
            "manifold_to_cdu_return",
            "cdu_to_manifold_supply",
        }
        all_nodes = {
            node_id
            for transformation in self.pilot["transformations"]
            for node_id in transformation["focus_nodes"]
        }
        all_edges = {
            edge_id
            for transformation in self.pilot["transformations"]
            for edge_id in transformation["focus_edges"]
        }
        self.assertFalse(all_nodes & forbidden_nodes)
        self.assertFalse(all_edges & forbidden_edges)

    def test_pilot_has_no_quantitative_heat_split_encoding(self) -> None:
        quantitative_keys = {
            "share",
            "ratio",
            "percent",
            "percentage",
            "fraction",
            "flow_rate",
            "temperature",
            "tdp",
            "load_magnitude",
        }
        self.assertFalse(
            quantitative_keys
            & {key.lower() for key in walk_keys(self.pilot) if isinstance(key, str)}
        )

    def test_native_output_is_deterministic_current_and_manual_only(self) -> None:
        first_html, first_digest, first_count = self.native.build()
        second_html, second_digest, second_count = self.native.build()
        self.assertEqual(
            (first_html, first_digest, first_count),
            (second_html, second_digest, second_count),
        )
        self.assertEqual(4, first_count)
        self.assertEqual(first_html, NATIVE_OUTPUT.read_text())
        self.assertIn('aria-label="Manual pilot transformations"', first_html)
        self.assertIn(
            'button.addEventListener("click", () => activate(index));', first_html
        )
        self.assertIn(
            'if (event.key === "ArrowRight") activate(current + 1);', first_html
        )
        for automatic_marker in (
            "setTimeout(",
            "setInterval(",
            "requestAnimationFrame(",
            "autoplay",
        ):
            with self.subTest(automatic_marker=automatic_marker):
                self.assertNotIn(automatic_marker, first_html)

    def test_native_schema_version_requires_an_exact_integer(self) -> None:
        for invalid in (True, 1.0, "1"):
            manifest = deepcopy(self.pilot)
            manifest["schema_version"] = invalid
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(
                    self.native.PilotError, "schema_version must be 1"
                ),
            ):
                self.native.validate_manifest(
                    manifest,
                    self.course,
                    self.master,
                    self.scene,
                    self.cameras,
                )

    def test_source_digest_covers_generator_and_transitive_rendering_code(
        self,
    ) -> None:
        declared = {path.resolve() for path in self.native.GENERATOR_DEPENDENCY_PATHS}
        expected = {
            NATIVE_GENERATOR.resolve(),
            Path(scene.__file__).resolve(),
            Path(tokens.__file__).resolve(),
            (ROOT / "pyproject.toml").resolve(),
            (ROOT / "uv.lock").resolve(),
            *{
                (ROOT / "diagram" / "vendor" / "three" / filename).resolve()
                for filename in (
                    "three.module.js",
                    "OrbitControls.js",
                    "CSS2DRenderer.js",
                    "LICENSE",
                )
            },
        }
        self.assertLessEqual(expected, declared)

        baseline = self.native._source_digest()
        original_read_bytes = Path.read_bytes

        def mutated_read_bytes(path: Path) -> bytes:
            payload = original_read_bytes(path)
            if path.resolve() == NATIVE_GENERATOR.resolve():
                return payload + b"\n# digest mutation probe\n"
            return payload

        with patch.object(Path, "read_bytes", mutated_read_bytes):
            mutated = self.native._source_digest()
        self.assertNotEqual(baseline, mutated)

    def test_native_validator_rejects_timing_and_scope_escape(self) -> None:
        timed = deepcopy(self.pilot)
        timed["transformations"][0]["duration_seconds"] = 30
        with self.assertRaisesRegex(self.native.PilotError, "fields must be exact"):
            self.native.validate_manifest(
                timed,
                self.course,
                self.master,
                self.scene,
                self.cameras,
            )

        escaped = deepcopy(self.pilot)
        escaped["transformations"][2]["focus_nodes"].append("crah")
        escaped["transformations"][2]["focus_edges"].append("rack_air_load_to_crah")
        with self.assertRaisesRegex(
            self.native.PilotError, "escapes canonical s10 scope"
        ):
            self.native.validate_manifest(
                escaped,
                self.course,
                self.master,
                self.scene,
                self.cameras,
            )


if __name__ == "__main__":
    unittest.main()
