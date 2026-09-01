from __future__ import annotations

import importlib.util
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

from gigawatt import building_visual, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase4_building.yaml"
GENERATOR = ROOT / "diagram" / "generate_phase4_building.py"
OUTPUT = ROOT / "diagram" / "phase4_building.html"


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


class Phase4BuildingPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = load_module("gigawatt_phase4_building", GENERATOR)
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
        return building_visual.compile_building_power_path(
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
            [
                "building_cutaway",
                "equipment_by_verb",
                "generic_ab_paths",
                "one_path_unavailable",
                "abilene_boundary",
                "rack_power_handoff",
            ],
            [state["id"] for state in self.manifest["states"]],
        )
        self.assertEqual(
            ["Spaces", "Functions", "A/B paths", "Isolation", "Abilene", "Rack"],
            [state["nav_label"] for state in self.manifest["states"]],
        )
        self.assertEqual([], teaching_visuals._forbidden_fields(self.manifest))
        self.assertTrue(self.manifest["states"][-1]["show_phase5_handoff"])
        final_copy = " ".join(
            (
                self.manifest["states"][-1]["title"],
                self.manifest["states"][-1]["instruction"],
            )
        )
        self.assertIn("Phase 4/5 boundary", final_copy)
        self.assertNotIn("Hand the carrier", final_copy)
        self.assertFalse(
            any(state["show_phase5_handoff"] for state in self.manifest["states"][:-1])
        )

    def test_every_authored_claim_and_gap_resolves_to_a_source_bound_fact(self) -> None:
        payload = self.compile()
        content_keys = (
            "spatial_building_zones",
            "functional_power_chain",
            "generic_protected_paths",
            "conditional_path_isolation",
            "abilene_mapping",
            "phase5_handoff",
            "evidence_gaps",
        )
        authored = {key: self.manifest[key] for key in content_keys}
        self.assertEqual(
            authored_fact_refs(authored),
            {fact["ref"] for fact in payload["evidence"]["facts"]},
        )
        self.assertEqual(25, len(payload["evidence"]["facts"]))
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
            'data-zone-id="campus_entry"',
            'data-chain-step-id="unit_substation"',
            'data-protected-path-id="path_a"',
            'data-isolation-path-state-id="isolated_path_a"',
            'data-abilene-known-id="first_phase_electrical_delivery"',
            'data-abilene-unknown-id="internal_power_train"',
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

    def test_visual_grammar_covers_the_six_distinct_teaching_jobs(self) -> None:
        rendered, _, _ = self.native.build()
        required = (
            "SPATIAL ORIENTATION · GENERIC CUTAWAY",
            "Campus entry",
            "Electrical space",
            "Data hall / IT space",
            "FUNCTIONAL GATES · CONCEPTUAL CARRIER FLOW",
            "FACILITY AC · DIRECTION OF TEACHING PATH",
            "GENERIC REFERENCE · A/B ARE TEACHING LABELS",
            "Compatible dual-input load",
            "Single-input load",
            "PATH A · UNAVAILABLE",
            "PATH B · REMAINS",
            "CONDITIONAL RACK RESULT",
            "Planned path removal",
            "Individual fault or path interruption",
            "ABILENE · EVIDENCE / UNKNOWN SPLIT",
            "GENERIC REFERENCE · NOT SITE-CONFIRMED",
            "Electrical equipment reached the site",
            "Building power train",
            "NEXT · PHASE 5 · STOP AT THE RACK-POWER BOUNDARY",
            "Mark the Phase 4/5 boundary at the rack position",
            "Rack position phase boundary",
            "Facility AC at",
            "Rack power shelf",
            "processor rails",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        self.assertNotIn("…", rendered)
        self.assertEqual(3, rendered.count('class="zone-front zone-'))
        self.assertGreaterEqual(rendered.count('class="chain-node"'), 6)

    def test_small_viewports_use_payload_html_and_declared_text_floors(self) -> None:
        short = building_visual.responsive_layout_contract(844, 390)
        portrait = building_visual.responsive_layout_contract(390, 844)
        tablet = building_visual.responsive_layout_contract(1024, 768)
        standard = building_visual.responsive_layout_contract(1280, 720)
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
        rendered = building_visual.render_building_power_path(self.compile())
        required = (
            'class="responsive-visual"',
            ".responsive-visual { display:block",
            ".visual-shell { display:none",
            "font-size:10px",
            "font-size:12px",
            "place-items:start stretch; overflow:auto",
            "@media (max-width:1100px) and (min-width:901px)",
            "@media (max-height:520px) and (orientation:landscape)",
            "@media (max-width:520px) and (orientation:portrait)",
            "overflow-x:hidden",
            "overflow-wrap:anywhere",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)

    def test_chain_badges_and_titles_have_disjoint_bounds(self) -> None:
        for index in range(len(building_visual.CHAIN_STEP_IDS)):
            geometry = building_visual.chain_step_geometry(index)
            badge = geometry["badge"]
            title = geometry["title"]
            intersects = not (
                badge[2] <= title[0]
                or title[2] <= badge[0]
                or badge[3] <= title[1]
                or title[3] <= badge[1]
            )
            with self.subTest(index=index):
                self.assertFalse(intersects)
                self.assertGreaterEqual(title[1] - badge[3], 10)

    def test_responsive_priority_matches_each_state_teaching_job(self) -> None:
        rendered = building_visual.render_building_power_path(self.compile())
        isolation_position = rendered.index(
            'class="responsive-layer responsive-isolation-layer"'
        )
        path_position = rendered.index('class="responsive-layer" data-path-layer')
        handoff_position = rendered.index('class="responsive-layer responsive-handoff"')
        abilene_position = rendered.index('class="responsive-layer" data-abilene-layer')
        self.assertLess(isolation_position, path_position)
        self.assertLess(handoff_position, abilene_position)
        self.assertIn("PATH A UNAVAILABLE · STATIC CONDITION", rendered)
        self.assertIn("Abilene unknown retained.", rendered)
        self.assertIn(
            'setLayer(".visual-shell [data-path-layer]", showPaths && !showIsolation)',
            rendered,
        )
        self.assertIn(
            'setLayer(".visual-shell [data-abilene-layer]", showAbilene && !state.show_phase5_handoff)',
            rendered,
        )

    def test_responsive_surface_is_generated_from_the_same_payload(self) -> None:
        rendered = building_visual.render_building_power_path(self.compile())
        for zone_id in building_visual.ZONE_IDS:
            self.assertEqual(2, rendered.count(f'data-zone-id="{zone_id}"'))
        for step_id in building_visual.CHAIN_STEP_IDS:
            self.assertEqual(2, rendered.count(f'data-chain-step-id="{step_id}"'))
            self.assertEqual(
                2,
                rendered.count(f'data-generic-chain-step-id="{step_id}"'),
            )
        for path_id in building_visual.PROTECTED_PATH_IDS:
            self.assertEqual(
                1,
                rendered.count(f'<g data-protected-path-id="{path_id}"'),
            )
            self.assertEqual(
                1,
                rendered.count(
                    f'class="responsive-card responsive-path" data-protected-path-id="{path_id}"'
                ),
            )
        for known_id in building_visual.ABILENE_KNOWN_IDS:
            self.assertEqual(2, rendered.count(f'data-abilene-known-id="{known_id}"'))
        for unknown_id in building_visual.ABILENE_UNKNOWN_IDS:
            self.assertEqual(
                2, rendered.count(f'data-abilene-unknown-id="{unknown_id}"')
            )

    def test_compiler_rejects_unregistered_or_unknown_claims(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["functional_power_chain"]["steps"][0]["fact_refs"] = [
            "not_registered:invented"
        ]
        with self.assertRaisesRegex(
            building_visual.BuildingVisualError,
            "unregistered evidence ledger",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["functional_power_chain"]["steps"][0]["fact_refs"] = [
            "building_power_reference:invented"
        ]
        with self.assertRaisesRegex(
            building_visual.BuildingVisualError,
            "unknown fact reference",
        ):
            self.compile(manifest)

    def test_compiler_rejects_pacing_and_schema_drift(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["states"][0]["duration_seconds"] = 30
        with self.assertRaisesRegex(
            building_visual.BuildingVisualError,
            "pacing or scripting fields",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["interaction"]["autoplay"] = False
        with self.assertRaisesRegex(
            building_visual.BuildingVisualError,
            "pacing or scripting fields",
        ):
            self.compile(manifest)

    def test_compiler_rejects_blank_or_misbound_state_transitions(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["states"][2]["protected_path_ids"] = []
        with self.assertRaisesRegex(
            building_visual.BuildingVisualError,
            "exactly one primary teaching layer",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["states"][3]["protected_path_ids"] = ["path_b"]
        with self.assertRaisesRegex(
            building_visual.BuildingVisualError,
            "isolation requires both generic protected paths",
        ):
            self.compile(manifest)
        manifest = deepcopy(self.manifest)
        manifest["states"][4]["abilene_unknown_ids"] = []
        with self.assertRaisesRegex(
            building_visual.BuildingVisualError,
            "preserve evidence and unknowns",
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
        self.assertIn(Path(building_visual.__file__).resolve(), captured_resolved)
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

    def test_svg_text_tspans_preserve_accessible_word_boundaries(self) -> None:
        rendered = building_visual.render_building_power_path(self.compile())
        self.assertNotRegex(rendered, r"</tspan><tspan")
        self.assertRegex(rendered, r"</tspan>\s+<tspan")


if __name__ == "__main__":
    unittest.main()
