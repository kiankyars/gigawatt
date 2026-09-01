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

from gigawatt import teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase1_generation.yaml"
GENERATOR = ROOT / "diagram" / "generate_phase1_generation.py"


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class Phase1GenerationPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = load_module("gigawatt_phase1_generation", GENERATOR)
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
        return teaching_visuals.compile_generation_landscape(
            deepcopy(self.manifest if manifest is None else manifest),
            deepcopy(self.ledgers if ledgers is None else ledgers),
            source_digest="0" * 64,
        )

    def test_manifest_is_manual_untimed_and_uses_coarse_exclusive_layers(self) -> None:
        self.assertEqual(
            {"mode": "manual", "advance": "instructor_controlled"},
            self.manifest["interaction"],
        )
        self.assertEqual(
            [
                "physical_families",
                "common_electrical_interface",
                "roles_are_not_technologies",
                "abilene_selection",
                "transmission_handoff",
            ],
            [state["id"] for state in self.manifest["states"]],
        )
        self.assertEqual(
            ["Sources", "Interface", "Roles", "Abilene", "Transmit"],
            [state["nav_label"] for state in self.manifest["states"]],
        )
        forbidden = teaching_visuals._forbidden_fields(self.manifest)
        self.assertEqual([], forbidden)

        for state in self.manifest["states"]:
            layers = (
                bool(state["family_ids"]),
                bool(state["distinction_ids"]),
                state["show_abilene_case"],
            )
            with self.subTest(state=state["id"]):
                self.assertEqual(1, sum(layers))
                if state["show_common_bus"]:
                    self.assertTrue(state["family_ids"])
                if state["show_handoff"]:
                    self.assertTrue(state["show_abilene_case"])
        self.assertTrue(self.manifest["states"][-1]["show_handoff"])

    def test_every_authored_claim_resolves_to_a_source_bound_fact(self) -> None:
        payload = self.compile()
        authored_refs = {
            ref
            for record in (
                *self.manifest["families"],
                *self.manifest["distinctions"],
                self.manifest["abilene_case"],
            )
            for ref in record["fact_refs"]
        }
        compiled_refs = {fact["ref"] for fact in payload["evidence"]["facts"]}
        self.assertEqual(authored_refs, compiled_refs)
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
        self.assertEqual(5, state_count)
        self.assertRegex(digest, r"^[0-9a-f]{64}$")

        required = (
            '<svg id="visual" role="img"',
            'aria-labelledby="visual-title visual-description"',
            'role="tablist"',
            'aria-live="polite"',
            'button.addEventListener("click", () => activate(index))',
            'document.querySelectorAll("[data-bus-link]")',
            'element.toggleAttribute("hidden", !selected.includes(id))',
            '.toggleAttribute("hidden", !state.show_abilene_case)',
            'event.key === "ArrowRight"',
            'event.key === "Home"',
            'event.key === "End"',
            "activate(0);",
            'id="pilot-data" type="application/json"',
            'class="state-nav-label">Sources</span>',
        )
        for marker in required:
            with self.subTest(required=marker):
                self.assertIn(marker, rendered)
        self.assertEqual(state_count, rendered.count('data-state-index="'))
        self.assertNotIn(".hidden =", rendered)
        self.assertIn("</tspan>\n<tspan", rendered)
        self.assertNotIn("</tspan><tspan", rendered)

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

    def test_role_state_uses_three_causal_pictograms(self) -> None:
        rendered, _, _ = self.native.build()
        storage = next(
            record
            for record in self.manifest["distinctions"]
            if record["id"] == "storage_not_primary_source"
        )
        self.assertEqual(
            [
                "generation_transmission:storage_is_charged_secondary_supply",
                "generation_transmission:storage_power_and_energy_are_distinct",
            ],
            storage["fact_refs"],
        )
        required = (
            "AC",
            "charge",
            "BESS",
            "discharge",
            "Batteries and pumped storage shift electricity through time",
            "Both time-shift energy rather than create a primary energy source.",
            "MW · rate",
            "MWh · energy",
            "PPA · contractual attributes",
            "physical electricity path",
            "Grid generation",
            "Shared grid",
            "Campus load",
            "Fuel",
            "Engine-generator",
            "Standby switch",
            "Load",
            'class="contract-arrow"',
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        self.assertEqual(3, rendered.count('<g class="causal-pictogram">'))

    def test_player_layout_is_viewport_bound_with_responsive_evidence_drawer(
        self,
    ) -> None:
        rendered, _, _ = self.native.build()
        required = (
            "height:100dvh",
            "overflow:hidden",
            ".visual-shell { width:100%; height:100%",
            "details[open] { max-height:min(34dvh,320px); overflow:auto",
            "@media (max-width:1100px) and (min-width:901px)",
            "@media (max-height:520px) and (orientation:landscape)",
            "@media (max-width:520px) and (orientation:portrait)",
            "details[open] { position:fixed; inset:10px",
            "overscroll-behavior:contain",
            "html { overflow:hidden; }",
            'history.scrollRestoration = "manual"',
            "function resetTeachingScroll()",
            'document.querySelector(".responsive-visual")',
            "window.scrollTo(0, 0)",
            "document.scrollingElement.scrollTop = 0",
            "container.scrollTop = 0",
            "resetTeachingScroll();",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        self.assertNotIn("aspect-ratio:16/9", rendered)

    def test_small_viewports_use_payload_driven_html_with_font_floors(self) -> None:
        short = teaching_visuals.responsive_layout_contract(844, 390)
        portrait = teaching_visuals.responsive_layout_contract(390, 844)
        standard = teaching_visuals.responsive_layout_contract(1440, 900)
        self.assertEqual(
            {
                "surface": "html",
                "profile": "short_landscape",
                "family_columns": 2,
                "minimum_text_px": 10,
                "scroll_axis": "vertical",
            },
            short,
        )
        self.assertEqual("html", portrait["surface"])
        self.assertEqual(1, portrait["family_columns"])
        self.assertGreaterEqual(portrait["minimum_text_px"], 12)
        self.assertEqual("vertical", portrait["scroll_axis"])
        self.assertEqual("svg", standard["surface"])

        payload = self.compile()
        for family in payload["families"]:
            geometry = teaching_visuals.short_landscape_family_geometry(
                family["compact_path"]
            )
            with self.subTest(family=family["id"]):
                self.assertGreaterEqual(geometry["minimum_text_px"], 10)
                self.assertLessEqual(
                    geometry["estimated_flow_width"], geometry["inner_width"]
                )

        rendered = teaching_visuals.render_generation_landscape(payload)
        self.assertIn('class="responsive-visual"', rendered)
        self.assertIn(".responsive-visual { display:block", rendered)
        self.assertIn(".visual-shell { display:none", rendered)
        self.assertIn("font-size:10px", rendered)
        self.assertIn("font-size:12px", rendered)
        self.assertIn("place-items:start stretch; overflow:auto", rendered)
        self.assertIn('class="compact-stage-label">Fuel / heat</span>', rendered)
        self.assertIn(
            'class="full-stage-label">Fuel, fission, or earth/sun heat</span>', rendered
        )

        for family in payload["families"]:
            self.assertEqual(
                2,
                rendered.count(f'data-family-id="{family["id"]}"'),
            )
        for distinction in payload["distinctions"]:
            self.assertEqual(
                2,
                rendered.count(f'data-distinction-id="{distinction["id"]}"'),
            )
        self.assertEqual(2, rendered.count("data-abilene-case hidden"))
        self.assertEqual(2, rendered.count("data-handoff hidden"))
        self.assertIn('document.querySelectorAll("[data-common-bus]")', rendered)
        self.assertIn('document.querySelectorAll("[data-abilene-case]")', rendered)

    def test_embedded_payload_is_script_safe_and_round_trips(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["title"] = "Safe </script><script>alert(1)</script> title"
        payload = self.compile(manifest)
        rendered = teaching_visuals.render_generation_landscape(payload)
        self.assertNotIn("</script><script>alert(1)</script>", rendered)
        match = re.search(
            r'<script id="pilot-data" type="application/json">(.*?)</script>',
            rendered,
            flags=re.DOTALL,
        )
        self.assertIsNotNone(match)
        embedded = json.loads(match.group(1))
        self.assertEqual(manifest["title"], embedded["pilot"]["title"])

    def test_source_digest_covers_renderer_manifest_and_registered_ledgers(
        self,
    ) -> None:
        declared = {path.resolve() for path in self.native.GENERATOR_DEPENDENCY_PATHS}
        self.assertLessEqual(
            {
                GENERATOR.resolve(),
                Path(teaching_visuals.__file__).resolve(),
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

    def test_validator_rejects_unregistered_or_unknown_fact_references(self) -> None:
        unregistered = deepcopy(self.manifest)
        unregistered["families"][0]["fact_refs"][0] = "outside:known_fact"
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "unregistered evidence ledger",
        ):
            self.compile(unregistered)

        unknown = deepcopy(self.manifest)
        ledger_id = next(iter(self.ledgers))
        unknown["families"][0]["fact_refs"][0] = f"{ledger_id}:missing_fact"
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "unknown fact reference",
        ):
            self.compile(unknown)

    def test_validator_rejects_missing_or_unknown_source_bindings(self) -> None:
        ledger_id, fact_id = self.manifest["families"][0]["fact_refs"][0].split(":", 1)
        missing = deepcopy(self.ledgers)
        missing[ledger_id]["facts"][fact_id]["source_ids"] = []
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "expected 1 to 12 entries",
        ):
            self.compile(ledgers=missing)

        unknown = deepcopy(self.ledgers)
        unknown[ledger_id]["facts"][fact_id]["source_ids"] = ["missing_source"]
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "unknown source IDs",
        ):
            self.compile(ledgers=unknown)

    def test_validator_rejects_pacing_fields_and_invalid_state_scope(self) -> None:
        paced = deepcopy(self.manifest)
        paced["states"][0]["duration_seconds"] = 30
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "pacing or scripting fields",
        ):
            self.compile(paced)

        escaped = deepcopy(self.manifest)
        escaped["states"][0]["family_ids"][0] = "invented_family"
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "unknown families",
        ):
            self.compile(escaped)

        incomplete = deepcopy(self.manifest)
        incomplete["states"][-1]["show_handoff"] = False
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "final pilot state must reveal",
        ):
            self.compile(incomplete)

    def test_evidence_paths_cannot_escape_the_registered_directory(self) -> None:
        manifest = deepcopy(self.manifest)
        first_id = next(iter(manifest["evidence_files"]))
        manifest["evidence_files"][first_id] = "../outside.yaml"
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "relative YAML path under evidence",
        ):
            teaching_visuals.registered_evidence_paths(manifest, root=ROOT)

    def test_schema_version_and_duplicate_yaml_keys_fail_closed(self) -> None:
        for invalid in (True, 1.0, "1"):
            manifest = deepcopy(self.manifest)
            manifest["schema_version"] = invalid
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(
                    teaching_visuals.TeachingVisualError,
                    "schema_version must be 1",
                ),
            ):
                self.compile(manifest)

        with TemporaryDirectory(prefix="gigawatt-phase1-yaml-") as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("schema_version: 1\nschema_version: 1\n")
            with self.assertRaisesRegex(
                teaching_visuals.TeachingVisualError,
                "duplicate YAML key",
            ):
                teaching_visuals.load_yaml(path)


if __name__ == "__main__":
    unittest.main()
