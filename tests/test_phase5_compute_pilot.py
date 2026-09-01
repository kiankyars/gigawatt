from __future__ import annotations

import importlib.util
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from gigawatt import compute_visual, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase5_compute.yaml"
GENERATOR = ROOT / "diagram" / "generate_phase5_compute.py"
OUTPUT = ROOT / "diagram" / "phase5_compute.html"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def authored_fact_refs(value) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {"fact_refs", "related_fact_refs"}:
                refs.update(nested)
            else:
                refs.update(authored_fact_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(authored_fact_refs(nested))
    return refs


class Phase5ComputePilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = load_module("gigawatt_phase5_compute", GENERATOR)
        cls.manifest = teaching_visuals.load_yaml(MANIFEST)
        cls.evidence_paths = teaching_visuals.registered_evidence_paths(
            cls.manifest,
            root=ROOT,
        )
        cls.ledgers = {
            ledger_id: teaching_visuals.load_yaml(path)
            for ledger_id, path in cls.evidence_paths.items()
        }

    def compile(
        self,
        manifest: dict | None = None,
        ledgers: dict | None = None,
    ) -> dict:
        return compute_visual.compile_compute_power_descent(
            deepcopy(self.manifest if manifest is None else manifest),
            deepcopy(self.ledgers if ledgers is None else ledgers),
            source_digest="0" * 64,
        )

    def test_manifest_is_manual_and_uses_six_coarse_states(self) -> None:
        self.assertEqual(
            {"mode": "manual", "advance": "instructor_controlled"},
            self.manifest["interaction"],
        )
        self.assertEqual(
            compute_visual.STATE_IDS, [s["id"] for s in self.manifest["states"]]
        )
        self.assertEqual(
            ["Rack", "Rack power", "Processor rails", "Compute", "Abilene", "Heat"],
            [state["nav_label"] for state in self.manifest["states"]],
        )
        self.assertEqual([], teaching_visuals._forbidden_fields(self.manifest))
        self.assertTrue(self.manifest["states"][-1]["show_phase6_handoff"])
        final_copy = " ".join(
            (
                self.manifest["states"][-1]["title"],
                self.manifest["states"][-1]["instruction"],
            )
        )
        self.assertIn("thermal-obligation boundary", final_copy)
        self.assertNotIn("physical carrier", final_copy)
        self.assertFalse(
            any(state["show_phase6_handoff"] for state in self.manifest["states"][:-1])
        )

    def test_every_authored_claim_and_gap_resolves_to_evidence(self) -> None:
        payload = self.compile()
        content_keys = (
            "rack_orientation",
            "rack_power_conversion",
            "processor_point_of_load",
            "compute_demand_loop",
            "abilene_mapping",
            "phase6_handoff",
            "evidence_gaps",
        )
        authored = {key: self.manifest[key] for key in content_keys}
        self.assertEqual(
            authored_fact_refs(authored),
            {fact["ref"] for fact in payload["evidence"]["facts"]},
        )
        self.assertEqual(43, len(payload["evidence"]["facts"]))
        source_refs = {source["ref"] for source in payload["evidence"]["sources"]}
        self.assertTrue(source_refs)
        for fact in payload["evidence"]["facts"]:
            with self.subTest(fact=fact["ref"]):
                self.assertTrue(fact["source_refs"])
                self.assertLessEqual(set(fact["source_refs"]), source_refs)

    def test_output_is_deterministic_inline_accessible_and_manual_only(self) -> None:
        first = self.native.build()
        second = self.native.build()
        self.assertEqual(first, second)
        rendered, digest, state_count = first
        self.assertEqual(6, state_count)
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        required = (
            '<svg id="visual" role="img"',
            'aria-labelledby="visual-title visual-description"',
            'role="tablist"',
            'aria-live="polite"',
            'data-orientation-layer-id="data_hall_boundary"',
            'data-rack-conversion-step-id="facility_ac_input"',
            'data-point-of-load-step-id="multiphase_vrm"',
            "data-compute-demand-layer",
            'data-abilene-known-id="platform_family"',
            'data-abilene-unknown-id="rack_and_rail_configuration"',
            "data-phase6-handoff",
            'element.toggleAttribute("hidden", !visible)',
            'button.addEventListener("click", () => activate(index))',
            'event.key === "ArrowRight"',
            'event.key === "Home"',
            'event.key === "End"',
            'history.scrollRestoration = "manual"',
            "window.scrollTo(0, 0)",
            "activate(0);",
            'id="pilot-data" type="application/json"',
        )
        for marker in required:
            with self.subTest(required=marker):
                self.assertIn(marker, rendered)
        self.assertEqual(state_count, rendered.count('data-state-index="'))
        forbidden = (
            '<script src="',
            "<link ",
            "@import",
            "fetch(",
            "setTimeout(",
            "setInterval(",
            "requestAnimationFrame(",
            "autoplay",
        )
        for marker in forbidden:
            with self.subTest(forbidden=marker):
                self.assertNotIn(marker, rendered)

    def test_visual_grammar_covers_all_six_teaching_jobs(self) -> None:
        rendered, _, _ = self.native.build()
        required = (
            "2D / 3D ORIENTATION",
            "DATA HALL BOUNDARY",
            "RACK ENVELOPE",
            'class="rack-carrier-band"',
            "BOARD / PROCESSOR BOUNDARY",
            "FACILITY AC → PRODUCT CONVERSION → NOMINAL RACK DC",
            "DOCUMENTED PRODUCT BOUNDARY",
            "nominal rack DC ≠ Abilene measurement",
            "BOARD POWER DESCENT",
            "VOLTAGE STEPS DOWN · CURRENT CAPABILITY RISES",
            "LOW VOLTAGE · HIGH CURRENT",
            "FORWARD ALLOCATION · ELECTRICITY → WORK",
            "UPSTREAM DEMAND SIGNATURE · NOT REVERSE ELECTRICAL FLOW",
            "WHAT THE RECORD SUPPORTS",
            "WHAT REMAINS UNKNOWN",
            "PHASE BOUNDARY · COMPUTATION IS DESIRED; HEAT CREATES THE COOLING OBLIGATION",
            "DESIRED OUTPUT",
            "THERMAL OBLIGATION",
            "LIQUID-COOLED PROCESSOR PATH",
            "RESIDUAL AIR-COOLED RACK PATH",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        self.assertNotIn("…", rendered)
        self.assertNotIn("PRIMARY PHYSICAL HANDOFF", rendered)
        self.assertNotIn("PHYSICAL OUTPUT", rendered)
        self.assertEqual(1, rendered.count('<path class="thermal-arrow"'))
        self.assertNotIn('class="thermal-arrow air-arrow"', rendered)

    def test_every_desktop_state_stays_inside_the_svg_viewbox(self) -> None:
        geometry = compute_visual.svg_geometry_contract()
        self.assertEqual(set(compute_visual.STATE_IDS), set(geometry))
        for state_id, objects in geometry.items():
            with self.subTest(state=state_id):
                self.assertTrue(objects)
            for object_id, (left, top, right, bottom) in objects.items():
                with self.subTest(state=state_id, object=object_id):
                    self.assertGreaterEqual(left, 0)
                    self.assertGreaterEqual(top, 0)
                    self.assertGreater(right, left)
                    self.assertGreater(bottom, top)
                    self.assertLessEqual(right, compute_visual.CANVAS_WIDTH)
                    self.assertLessEqual(bottom, compute_visual.CANVAS_HEIGHT)
                    self.assertLessEqual(bottom, 765)
        boundary_states = {
            "orient_inside_rack": ("rack", "boundary"),
            "facility_ac_to_rack_dc": (
                "product_boundary",
                "evidence_boundary",
            ),
            "board_point_of_load": ("rail_callout", "evidence_boundary"),
            "useful_compute_and_upstream_demand": (
                "upstream_demand",
                "evidence_boundary",
            ),
            "abilene_compute_boundary": (
                "known_and_unknown",
                "evidence_boundary",
            ),
        }
        for state_id, (upper_id, lower_id) in boundary_states.items():
            upper = geometry[state_id][upper_id]
            lower = geometry[state_id][lower_id]
            self.assertLess(upper[3], lower[1], state_id)

    def test_small_viewports_use_payload_html_and_text_floors(self) -> None:
        short = compute_visual.responsive_layout_contract(844, 390)
        portrait = compute_visual.responsive_layout_contract(390, 844)
        tablet = compute_visual.responsive_layout_contract(1024, 768)
        standard = compute_visual.responsive_layout_contract(1280, 720)
        self.assertEqual(
            ("html", "short_landscape"), (short["surface"], short["profile"])
        )
        self.assertGreaterEqual(short["minimum_text_px"], 10)
        self.assertEqual(
            ("html", "portrait"), (portrait["surface"], portrait["profile"])
        )
        self.assertGreaterEqual(portrait["minimum_text_px"], 12)
        self.assertEqual(("html", "tablet"), (tablet["surface"], tablet["profile"]))
        self.assertGreaterEqual(tablet["minimum_text_px"], 12)
        self.assertEqual("vertical", tablet["scroll_axis"])
        self.assertEqual("svg", standard["surface"])
        rendered = compute_visual.render_compute_power_descent(self.compile())
        required = (
            'class="responsive-visual"',
            ".responsive-visual { display:none",
            ".visual-shell { display:none",
            "font-size:10px",
            "font-size:12px",
            "place-items:start stretch; overflow:auto",
            "@media (max-width:1100px) and (min-width:901px)",
            "@media (max-height:520px) and (orientation:landscape)",
            "@media (max-width:520px) and (orientation:portrait)",
            "overflow-x:hidden",
            "overflow-wrap:anywhere",
            ".state-nav-label { overflow:visible; text-overflow:clip; white-space:normal",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)

    def test_responsive_surface_is_derived_from_the_same_payload(self) -> None:
        rendered = compute_visual.render_compute_power_descent(self.compile())
        for record_id in compute_visual.ORIENTATION_LAYER_IDS:
            self.assertEqual(
                2, rendered.count(f'data-orientation-layer-id="{record_id}"')
            )
        for record_id in compute_visual.RACK_CONVERSION_STEP_IDS:
            self.assertEqual(
                2, rendered.count(f'data-rack-conversion-step-id="{record_id}"')
            )
        for record_id in compute_visual.POINT_OF_LOAD_STEP_IDS:
            self.assertEqual(
                2, rendered.count(f'data-point-of-load-step-id="{record_id}"')
            )
        for record_id in compute_visual.ABILENE_KNOWN_IDS:
            self.assertEqual(2, rendered.count(f'data-abilene-known-id="{record_id}"'))
        for record_id in compute_visual.ABILENE_UNKNOWN_IDS:
            self.assertEqual(
                2, rendered.count(f'data-abilene-unknown-id="{record_id}"')
            )
        for record_id in compute_visual.HANDOFF_CARRIER_IDS:
            self.assertEqual(
                2, rendered.count(f'data-handoff-carrier-id="{record_id}"')
            )

    def test_compiler_rejects_unregistered_or_unknown_claims(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["rack_orientation"]["layers"][0]["fact_refs"] = [
            "not_registered:invented"
        ]
        with self.assertRaisesRegex(
            compute_visual.ComputeVisualError,
            "unregistered evidence ledger",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["rack_orientation"]["layers"][0]["fact_refs"] = [
            "electrical_engineering:invented"
        ]
        with self.assertRaisesRegex(
            compute_visual.ComputeVisualError,
            "unknown fact reference",
        ):
            self.compile(manifest)

    def test_compiler_rejects_pacing_and_schema_drift(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["states"][0]["duration_seconds"] = 30
        with self.assertRaisesRegex(
            compute_visual.ComputeVisualError,
            "pacing or scripting fields",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["interaction"]["autoplay"] = False
        with self.assertRaisesRegex(
            compute_visual.ComputeVisualError,
            "pacing or scripting fields",
        ):
            self.compile(manifest)

    def test_compiler_rejects_blank_or_misbound_transitions(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["states"][0]["orientation_layer_ids"] = []
        with self.assertRaisesRegex(
            compute_visual.ComputeVisualError,
            "escaped its canonical selection",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["states"][3]["show_compute_demand_loop"] = False
        with self.assertRaisesRegex(
            compute_visual.ComputeVisualError,
            "escaped its canonical selection",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["states"][4]["abilene_unknown_ids"] = []
        with self.assertRaisesRegex(
            compute_visual.ComputeVisualError,
            "escaped its canonical selection",
        ):
            self.compile(manifest)

    def test_source_digest_binds_manifest_renderer_and_every_ledger(self) -> None:
        baseline = self.native._source_digest()
        original = teaching_visuals.source_digest
        captured: list[Path] = []

        def capture(root: Path, paths):
            materialized = list(paths)
            captured.extend(materialized)
            return original(root, materialized)

        with patch.object(teaching_visuals, "source_digest", side_effect=capture):
            self.native._source_digest()
        captured_resolved = {path.resolve() for path in captured}
        self.assertIn(MANIFEST.resolve(), captured_resolved)
        self.assertIn(GENERATOR.resolve(), captured_resolved)
        self.assertIn(Path(compute_visual.__file__).resolve(), captured_resolved)
        self.assertIn(Path(teaching_visuals.__file__).resolve(), captured_resolved)
        self.assertLessEqual(
            {path.resolve() for path in self.evidence_paths.values()},
            captured_resolved,
        )
        self.assertRegex(baseline, r"^[0-9a-f]{64}$")

    def test_generated_output_matches_the_pure_builder(self) -> None:
        rendered, _, _ = self.native.build()
        self.assertTrue(OUTPUT.is_file())
        self.assertEqual(rendered, OUTPUT.read_text())
        self.assertRegex(
            rendered,
            r'<meta name="gigawatt-source-digest" content="[0-9a-f]{64}">',
        )

    def test_script_payload_escapes_html_end_tags(self) -> None:
        payload = self.compile()
        payload["pilot"]["title"] = "safe </script> payload"
        rendered = compute_visual.render_compute_power_descent(payload)
        self.assertIn("safe <\\/script> payload", rendered)
        self.assertNotIn('"title":"safe </script> payload"', rendered)

    def test_svg_text_tspans_preserve_accessible_word_boundaries(self) -> None:
        rendered = compute_visual.render_compute_power_descent(self.compile())
        self.assertNotRegex(rendered, r"</tspan><tspan")
        self.assertRegex(rendered, r"</tspan>\s+<tspan")


if __name__ == "__main__":
    unittest.main()
