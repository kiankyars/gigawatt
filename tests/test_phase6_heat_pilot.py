from __future__ import annotations

import importlib.util
import json
import re
import sys
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from gigawatt import heat_visual, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase6_heat.yaml"
GENERATOR = ROOT / "diagram" / "generate_phase6_heat.py"
OUTPUT = ROOT / "diagram" / "phase6_heat.html"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def authored_refs(value) -> set[str]:
    refs: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in {"fact_refs", "related_fact_refs"}:
                refs.update(nested)
            else:
                refs.update(authored_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(authored_refs(nested))
    return refs


class Phase6HeatPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = load_module("gigawatt_phase6_heat", GENERATOR)
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
        return heat_visual.compile_heat_return(
            deepcopy(self.manifest if manifest is None else manifest),
            deepcopy(self.ledgers if ledgers is None else ledgers),
            source_digest="0" * 64,
        )

    def test_manifest_is_manual_untimed_and_preserves_five_states(self) -> None:
        self.assertEqual(
            {"mode": "manual", "advance": "instructor_controlled"},
            self.manifest["interaction"],
        )
        self.assertEqual(
            [
                "die_to_cold_plate",
                "rack_to_facility_boundary",
                "parallel_residual_air",
                "facility_rejection_and_water",
                "whole_journey_closure",
            ],
            [state["id"] for state in self.manifest["states"]],
        )
        self.assertEqual(
            [
                "Cold plate",
                "Liquid loops",
                "Residual air",
                "Atmosphere",
                "Full journey",
            ],
            [state["nav_label"] for state in self.manifest["states"]],
        )
        self.assertEqual([], teaching_visuals._forbidden_fields(self.manifest))
        self.assertEqual(
            ["generate", "transmit", "campus", "building", "compute", "reject_heat"],
            self.manifest["states"][-1]["journey_stage_ids"],
        )
        self.assertTrue(
            all(
                not state["journey_stage_ids"] for state in self.manifest["states"][:-1]
            )
        )
        self.assertEqual(
            {"heat_obligation"},
            {
                view_id
                for state in self.manifest["states"]
                for view_id in state["energy_view_ids"]
            },
        )

    def test_exact_facility_stage_ids_reject_duplicate_list_records(self) -> None:
        self.assertEqual(
            ["facility_loop_transport", "air_cooled_terminal", "atmosphere_sink"],
            [stage["id"] for stage in self.manifest["facility_rejection"]["stages"]],
        )
        duplicate = deepcopy(self.manifest)
        duplicate["facility_rejection"]["stages"][2] = deepcopy(
            duplicate["facility_rejection"]["stages"][1]
        )
        with self.assertRaisesRegex(
            heat_visual.HeatVisualError,
            "incomplete or duplicate ID set",
        ):
            self.compile(duplicate)

    def test_every_claim_and_gap_guard_is_source_bound(self) -> None:
        payload = self.compile()
        content = {
            key: self.manifest[key]
            for key in (
                "energy_handoff",
                "liquid_path",
                "residual_air_path",
                "facility_rejection",
                "abilene_mapping",
                "journey_closure",
                "evidence_gaps",
            )
        }
        self.assertEqual(
            authored_refs(content),
            {fact["ref"] for fact in payload["evidence"]["facts"]},
        )
        self.assertEqual(43, len(payload["evidence"]["facts"]))
        self.assertEqual(22, len(payload["evidence"]["sources"]))
        source_refs = {source["ref"] for source in payload["evidence"]["sources"]}
        for fact in payload["evidence"]["facts"]:
            with self.subTest(fact=fact["ref"]):
                self.assertTrue(fact["source_refs"])
                self.assertLessEqual(set(fact["source_refs"]), source_refs)

    def test_output_is_deterministic_accessible_inline_and_manual_only(self) -> None:
        first = self.native.build()
        second = self.native.build()
        self.assertEqual(first, second)
        rendered, digest, state_count = first
        self.assertEqual(5, state_count)
        self.assertRegex(digest, r"^[0-9a-f]{64}$")
        required = (
            '<svg id="visual" role="img"',
            'aria-labelledby="visual-title visual-description"',
            'role="tablist"',
            'aria-live="polite"',
            'data-heat-scene-id="die_to_cold_plate"',
            'data-heat-scene-id="whole_journey_closure"',
            'button.addEventListener("click", () => activate(index))',
            'event.key === "ArrowRight"',
            'event.key === "Home"',
            'event.key === "End"',
            "activate(0);",
            'id="pilot-data" type="application/json"',
        )
        for marker in required:
            with self.subTest(required=marker):
                self.assertIn(marker, rendered)
        self.assertEqual(5, rendered.count('data-state-index="'))
        visible_markup = rendered.split(
            '<script id="pilot-data" type="application/json">', maxsplit=1
        )[0]
        self.assertNotIn(
            'data-heat-scene-id="electrical_to_compute_and_heat"', visible_markup
        )
        self.assertNotIn("TWO ACCOUNTING VIEWS · NOT TWO PIE SLICES", visible_markup)
        for forbidden in (
            '<script src="',
            "<link ",
            "@import",
            "fetch(",
            "setTimeout(",
            "setInterval(",
            "requestAnimationFrame(",
            "autoplay",
        ):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, rendered)

    def test_five_svg_states_are_causal_distinct_and_untruncated(self) -> None:
        payload = self.compile()
        state_functions = (
            heat_visual._cold_plate_svg,
            heat_visual._liquid_svg,
            heat_visual._air_svg,
            heat_visual._facility_svg,
            heat_visual._journey_svg,
        )
        rendered_states = [
            function(payload, state)
            for function, state in zip(state_functions, payload["states"])
        ]
        self.assertEqual(5, len({value for value in rendered_states}))
        for value in rendered_states:
            self.assertNotIn("…", value)

        rendered = heat_visual.render_heat_return(payload)
        required = (
            'class="cold-plate-cutaway"',
            "ACCOUNTING BOUNDARY",
            "Useful compute is a service, not an energy slice; no site heat fraction is inferred.",
            "TECHNOLOGY COOLING SYSTEM · IT SIDE",
            "FACILITY WATER SYSTEM · PLANT SIDE",
            "CONDITIONAL AT ABILENE",
            "HEAT ARROWS CONVERGE · FLUID CIRCUITS ARE NOT SHOWN MIXING",
            "FOUR SEPARATE WATER ACCOUNTS · NO CONFLATION",
            "FULL SIX-PHASE JOURNEY · CONCEPTUAL INDEX + EVIDENCE POSTURE",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        self.assertNotIn('class="pie-slice"', rendered)

    def test_water_accounts_cannot_conflate_evaporation_fill_or_unknown(self) -> None:
        payload = self.compile()
        accounts = {
            item["id"]: item for item in payload["facility_rejection"]["water_accounts"]
        }
        self.assertEqual(
            "No evaporative consumption in the selected Abilene design",
            accounts["rejection_process_water"]["display"],
        )
        self.assertIn(
            "1,000,000 gallons per building", accounts["initial_fill"]["display"]
        )
        self.assertIn(
            "50,000 gallons per building per year",
            accounts["anticipated_maintenance"]["display"],
        )
        self.assertEqual(
            "explicit_unknown_not_zero",
            accounts["measured_operating_water"]["accounting_posture"],
        )
        self.assertIn("not zero", accounts["measured_operating_water"]["boundary"])

    def test_journey_closure_is_a_real_six_phase_teaching_surface(self) -> None:
        payload = self.compile()
        journey = payload["journey_closure"]
        self.assertEqual(
            list(range(1, 7)), [stage["number"] for stage in journey["stages"]]
        )
        self.assertEqual(
            ["Generate", "Transmit", "Campus", "Building", "Compute", "Reject heat"],
            [stage["title"] for stage in journey["stages"]],
        )
        rendered = heat_visual._journey_svg(payload, payload["states"][-1])
        self.assertEqual(6, rendered.count('class="journey-stage"'))
        self.assertEqual(6, rendered.count('class="journey-icon'))
        self.assertIn("atmosphere", payload["journey_closure"]["body"].lower())
        self.assertIn(
            "not an Abilene as-built one-line", journey["closure_guard"]["body"]
        )

    def test_desktop_cards_stay_inside_panels_without_overlap(self) -> None:
        payload = self.compile()

        air = heat_visual._air_svg(payload, payload["states"][2])
        convergence = re.search(
            r'class="convergence-box" x="\d+" y="(\d+)" width="\d+" height="(\d+)"',
            air,
        )
        self.assertIsNotNone(convergence)
        convergence_bottom = int(convergence.group(1)) + int(convergence.group(2))
        evidence_cards = re.findall(
            r'class="(?:known|unknown)-summary" x="\d+" y="(\d+)" width="\d+" height="(\d+)"',
            air,
        )
        self.assertEqual(2, len(evidence_cards))
        for y, height in evidence_cards:
            with self.subTest(card=(y, height)):
                self.assertGreater(int(y), convergence_bottom)
                self.assertLessEqual(int(y) + int(height), 858)

        facility = heat_visual._facility_svg(payload, payload["states"][3])
        water_cards = re.findall(
            r'class="water-account[^\"]*"><rect x="(\d+)" y="\d+" width="(\d+)"',
            facility,
        )
        self.assertEqual(4, len(water_cards))
        for x, width in water_cards:
            with self.subTest(card=(x, width)):
                self.assertGreaterEqual(int(x), 42)
                self.assertLessEqual(int(x) + int(width), 1558)

        journey = heat_visual._journey_svg(payload, payload["states"][4])
        journey_cards = re.findall(
            r'class="journey-stage"><rect x="(\d+)" y="\d+" width="(\d+)"',
            journey,
        )
        self.assertEqual(6, len(journey_cards))
        for x, width in journey_cards:
            with self.subTest(card=(x, width)):
                self.assertGreaterEqual(int(x), 42)
                self.assertLessEqual(int(x) + int(width), 1558)

    def test_supported_viewports_are_readable_and_keep_full_nav_labels(self) -> None:
        expected = {
            (1280, 720): ("html", "course_landscape", 12),
            (1024, 768): ("html", "tablet", 12),
            (844, 390): ("html", "short_landscape", 10),
            (390, 844): ("html", "portrait", 12),
            (1440, 900): ("svg", "standard", 13),
        }
        for viewport, contract in expected.items():
            actual = heat_visual.responsive_layout_contract(*viewport)
            with self.subTest(viewport=viewport):
                self.assertEqual(
                    contract,
                    (actual["surface"], actual["profile"], actual["minimum_text_px"]),
                )
        for dimensions in ((0, 720), (-1, 720), (1280, 0), (1280.0, 720)):
            with (
                self.subTest(dimensions=dimensions),
                self.assertRaisesRegex(
                    heat_visual.HeatVisualError,
                    "positive integers",
                ),
            ):
                heat_visual.responsive_layout_contract(*dimensions)

        rendered = heat_visual.render_heat_return(self.compile())
        self.assertIn("@media (max-width:1280px), (max-height:760px)", rendered)
        self.assertIn("font-size:12px", rendered)
        self.assertIn("font-size:10px", rendered)
        self.assertIn(
            ".state-nav-label { overflow:visible; text-overflow:clip; white-space:normal; }",
            rendered,
        )
        self.assertIn("footer { grid-template-columns:1fr; gap:4px; }", rendered)
        self.assertIn(".state-copy p { display:none; }", rendered)

    def test_responsive_primary_content_is_first_and_payload_driven(self) -> None:
        payload = self.compile()
        rendered = heat_visual.render_heat_return(payload)
        self.assertIn('class="responsive-visual"', rendered)
        self.assertIn(".responsive-visual { display:block", rendered)
        for state in payload["states"]:
            self.assertEqual(
                2,
                rendered.count(f'data-heat-scene-id="{state["id"]}"'),
            )
        self.assertLess(
            rendered.index('<section class="responsive-scene responsive-journey"'),
            rendered.index('<section class="responsive-scene responsive-cold-plate"'),
        )
        visible_markup = rendered.split(
            '<script id="pilot-data" type="application/json">', maxsplit=1
        )[0]
        self.assertNotIn('class="responsive-scene responsive-energy"', visible_markup)

    def test_evidence_drawer_wraps_and_restores_scroll_when_closed(self) -> None:
        rendered, _, _ = self.native.build()
        required = (
            "overflow:auto; overflow-x:hidden",
            "overflow-wrap:anywhere; word-break:break-word",
            'const evidenceDrawer = document.querySelector("details");',
            'evidenceDrawer.addEventListener("toggle"',
            "if (!evidenceDrawer.open) resetTeachingScroll();",
            "document.scrollingElement.scrollTop = 0",
            "container.scrollTop = 0",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)

    def test_embedded_payload_is_script_safe_and_round_trips(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["title"] = "Safe </script><script>alert(1)</script> title"
        payload = self.compile(manifest)
        rendered = heat_visual.render_heat_return(payload)
        self.assertNotIn("</script><script>alert(1)</script>", rendered)
        match = re.search(
            r'<script id="pilot-data" type="application/json">(.*?)</script>',
            rendered,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        embedded = json.loads(match.group(1))
        self.assertEqual(manifest["title"], embedded["pilot"]["title"])

    def test_source_digest_covers_compilers_manifest_and_registered_ledgers(
        self,
    ) -> None:
        declared = {path.resolve() for path in self.native.GENERATOR_DEPENDENCY_PATHS}
        self.assertLessEqual(
            {
                GENERATOR.resolve(),
                Path(teaching_visuals.__file__).resolve(),
                Path(heat_visual.__file__).resolve(),
                (ROOT / "pyproject.toml").resolve(),
                (ROOT / "uv.lock").resolve(),
            },
            declared,
        )
        baseline = self.native._source_digest()
        original_read_bytes = Path.read_bytes
        probe = next(iter(self.evidence_paths.values())).resolve()

        def mutated_read_bytes(path: Path) -> bytes:
            value = original_read_bytes(path)
            if path.resolve() == probe:
                return value + b"\n# digest mutation probe\n"
            return value

        with patch.object(Path, "read_bytes", mutated_read_bytes):
            mutated = self.native._source_digest()
        self.assertNotEqual(baseline, mutated)

    def test_validator_rejects_bad_gap_refs_pacing_and_journey_escape(self) -> None:
        bad_gap = deepcopy(self.manifest)
        bad_gap["evidence_gaps"][0]["related_fact_refs"][0] = (
            "thermal_engineering:missing_fact"
        )
        with self.assertRaisesRegex(
            heat_visual.HeatVisualError,
            "unknown fact reference",
        ):
            self.compile(bad_gap)

        paced = deepcopy(self.manifest)
        paced["states"][0]["duration_seconds"] = 30
        with self.assertRaisesRegex(
            heat_visual.HeatVisualError,
            "pacing or scripting fields",
        ):
            self.compile(paced)

        escaped = deepcopy(self.manifest)
        escaped["states"][0]["journey_stage_ids"] = ["generate"]
        with self.assertRaisesRegex(
            heat_visual.HeatVisualError,
            "only the final state",
        ):
            self.compile(escaped)

        pie_fraction = deepcopy(self.manifest)
        pie_fraction["energy_handoff"]["allocation_guard"]["concise_boundary"] = (
            "Useful compute receives a fixed share of site power."
        )
        with self.assertRaisesRegex(
            heat_visual.HeatVisualError,
            "reject an energy slice and site heat fraction",
        ):
            self.compile(pie_fraction)

        repeated_handoff = deepcopy(self.manifest)
        repeated_handoff["states"][0]["energy_view_ids"].append("electrical_input")
        with self.assertRaisesRegex(
            heat_visual.HeatVisualError,
            "only the heat-obligation accounting view",
        ):
            self.compile(repeated_handoff)

    def test_schema_path_and_checked_in_output_fail_closed(self) -> None:
        for invalid in (True, 1.0, "1"):
            manifest = deepcopy(self.manifest)
            manifest["schema_version"] = invalid
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(
                    heat_visual.HeatVisualError,
                    "schema_version must be 1",
                ),
            ):
                self.compile(manifest)

        escaped = deepcopy(self.manifest)
        first_id = next(iter(escaped["evidence_files"]))
        escaped["evidence_files"][first_id] = "../outside.yaml"
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "relative YAML path under evidence",
        ):
            teaching_visuals.registered_evidence_paths(escaped, root=ROOT)

        with TemporaryDirectory(prefix="gigawatt-phase6-yaml-") as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("schema_version: 1\nschema_version: 1\n")
            with self.assertRaisesRegex(
                teaching_visuals.TeachingVisualError,
                "duplicate YAML key",
            ):
                teaching_visuals.load_yaml(path)

        rendered, digest, _ = self.native.build()
        self.assertTrue(OUTPUT.exists())
        self.assertEqual(rendered, OUTPUT.read_text())
        self.assertIn(
            f'<meta name="gigawatt-source-digest" content="{digest}">', rendered
        )


if __name__ == "__main__":
    unittest.main()
