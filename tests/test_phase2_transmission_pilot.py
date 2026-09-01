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

from gigawatt import teaching_visuals, transmission_visual

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase2_transmission.yaml"
GENERATOR = ROOT / "diagram" / "generate_phase2_transmission.py"
OUTPUT = ROOT / "diagram" / "phase2_transmission.html"


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
            if key == "fact_refs":
                refs.update(nested)
            else:
                refs.update(authored_fact_refs(nested))
    elif isinstance(value, list):
        for nested in value:
            refs.update(authored_fact_refs(nested))
    return refs


class Phase2TransmissionPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = load_module("gigawatt_phase2_transmission", GENERATOR)
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
        return transmission_visual.compile_transmission_landscape(
            deepcopy(self.manifest if manifest is None else manifest),
            deepcopy(self.ledgers if ledgers is None else ledgers),
            source_digest="0" * 64,
        )

    def test_manifest_is_manual_untimed_and_uses_six_coarse_states(self) -> None:
        self.assertEqual(
            {"mode": "manual", "advance": "instructor_controlled"},
            self.manifest["interaction"],
        )
        self.assertEqual(
            [
                "why_voltage_rises",
                "network_and_balance",
                "substation_gate",
                "generator_vs_large_load",
                "abilene_grid_paths",
                "campus_distribution_handoff",
            ],
            [state["id"] for state in self.manifest["states"]],
        )
        self.assertEqual(
            ["Voltage", "Network", "Substation", "Gates", "Abilene", "Campus"],
            [state["nav_label"] for state in self.manifest["states"]],
        )
        self.assertEqual([], teaching_visuals._forbidden_fields(self.manifest))

        for state in self.manifest["states"]:
            primary_layers = (
                bool(state["principle_ids"]),
                state["show_substation"],
                bool(state["process_lane_ids"]),
                bool(state["abilene_path_ids"]),
            )
            with self.subTest(state=state["id"]):
                self.assertEqual(1, sum(primary_layers))
                if state["show_handoff"]:
                    self.assertEqual(
                        {"initial_138", "expansion_345"},
                        set(state["abilene_path_ids"]),
                    )
        self.assertTrue(self.manifest["states"][-1]["show_handoff"])

    def test_every_authored_claim_resolves_to_a_source_bound_fact(self) -> None:
        payload = self.compile()
        content = {
            key: self.manifest[key]
            for key in (
                "transmission_principles",
                "substation_anatomy",
                "interconnection_processes",
                "abilene_case",
                "phase3_handoff",
            )
        }
        self.assertEqual(
            authored_fact_refs(content),
            {fact["ref"] for fact in payload["evidence"]["facts"]},
        )
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
            'data-principle-id="voltage_transfer"',
            "data-substation hidden",
            'data-process-lane-id="generator_interconnection"',
            'data-abilene-path-id="initial_138"',
            'button.addEventListener("click", () => activate(index))',
            'event.key === "ArrowRight"',
            'event.key === "Home"',
            'event.key === "End"',
            "activate(0);",
            'evidenceDrawer.addEventListener("toggle"',
            "if (!evidenceDrawer.open) resetTeachingScroll();",
            'id="pilot-data" type="application/json"',
            'class="state-nav-label">Voltage</span>',
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

    def test_six_states_render_purpose_built_explanatory_visuals(self) -> None:
        rendered, _, _ = self.native.build()
        required = (
            "Same transferred power",
            "P fixed · loss ∝ I²R",
            "INTERCONNECTED AC NETWORK",
            "Generator A",
            "Transmission node 2",
            "Balancing authority",
            "EXPLODED FUNCTIONAL ENVELOPE",
            'class="balance-title centered"',
            'class="substation-boundary-copy centered"',
            "Transform voltage",
            "Feed outgoing circuits",
            "Valid request with required project data and readiness items",
            "System-wide steady-state and stability screening",
            "Current public posture through 2026-08-21",
            "2026-07-11",
            "2026-08-20",
            "Initial path — 200 MW / 138 kV station",
            "Expansion path — 1 GW / 345 kV substation",
            "NO MERGE DRAWN",
            "NEXT · PHASE 3",
            "GENERIC PHASE 3 QUESTIONS · NOT ABILENE TOPOLOGY",
            "How does power fan out to buildings?",
            "NO MERGE ASSUMED",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        self.assertEqual(7, rendered.count('class="function-card"'))
        self.assertEqual(10, rendered.count('class="gate-card"'))
        mesh = transmission_visual._mesh_svg(
            self.compile()["transmission_principles"][1]
        )
        self.assertNotIn("…", mesh)
        substation = transmission_visual._substation_svg(
            self.compile()["substation_anatomy"]
        )
        card_y = [
            float(value)
            for value in re.findall(
                r'class="function-card"[^>]+ y="([0-9.]+)"', substation
            )
        ]
        self.assertEqual(7, len(card_y))
        self.assertGreaterEqual(min(card_y), 200)
        handoff = transmission_visual._handoff_svg(
            self.compile()["phase3_handoff"], self.compile()["abilene_case"]
        )
        self.assertEqual(3, handoff.count('class="handoff-question-node"'))
        self.assertNotIn("…", handoff)

    def test_small_viewports_use_payload_html_and_declared_text_floors(self) -> None:
        short = transmission_visual.responsive_layout_contract(844, 390)
        portrait = transmission_visual.responsive_layout_contract(390, 844)
        tablet = transmission_visual.responsive_layout_contract(1024, 768)
        standard = transmission_visual.responsive_layout_contract(1440, 900)
        self.assertEqual("html", short["surface"])
        self.assertEqual("short_landscape", short["profile"])
        self.assertGreaterEqual(short["minimum_text_px"], 10)
        self.assertEqual("html", portrait["surface"])
        self.assertEqual("portrait", portrait["profile"])
        self.assertGreaterEqual(portrait["minimum_text_px"], 12)
        self.assertEqual("html", tablet["surface"])
        self.assertEqual("tablet", tablet["profile"])
        self.assertGreaterEqual(tablet["minimum_text_px"], 12)
        self.assertEqual("vertical", tablet["scroll_axis"])
        self.assertEqual("svg", standard["surface"])

        rendered = transmission_visual.render_transmission_landscape(self.compile())
        required = (
            'class="responsive-visual"',
            ".responsive-visual { display:block",
            ".visual-shell { display:none",
            "font-size:10px",
            "font-size:12px",
            "place-items:start stretch; overflow:auto",
            ".objective { display:none; }",
            "@media (max-width:1100px) and (min-width:901px)",
            "@media (max-width:1300px) and (min-width:1101px)",
            ".state-nav-label { overflow:visible; text-overflow:clip; white-space:normal; }",
            ".fact-ref,.fact-boundary { overflow-wrap:anywhere; word-break:break-word;",
            ".responsive-visual { display:block; width:100%; height:auto; min-height:100%; padding:6px; font-size:12px; }",
            ".responsive-path-flow { flex-direction:column; align-items:stretch; }",
            'class="responsive-handoff-diagram"',
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        for principle in self.compile()["transmission_principles"]:
            self.assertEqual(
                2,
                rendered.count(f'data-principle-id="{principle["id"]}"'),
            )
        for lane in self.compile()["interconnection_processes"]["lanes"]:
            self.assertEqual(
                2,
                rendered.count(f'data-process-lane-id="{lane["id"]}"'),
            )
        for path in self.compile()["abilene_case"]["paths"]:
            self.assertEqual(
                2,
                rendered.count(f'data-abilene-path-id="{path["id"]}"'),
            )
        self.assertEqual(2, rendered.count("data-substation hidden"))
        self.assertEqual(2, rendered.count("data-abilene-case hidden"))
        self.assertEqual(2, rendered.count("data-handoff hidden"))
        self.assertLess(
            rendered.index('<div class="responsive-handoff"'),
            rendered.index('<section class="responsive-abilene"'),
        )

    def test_embedded_payload_is_script_safe_and_round_trips(self) -> None:
        manifest = deepcopy(self.manifest)
        manifest["title"] = "Safe </script><script>alert(1)</script> title"
        payload = self.compile(manifest)
        rendered = transmission_visual.render_transmission_landscape(payload)
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
                Path(transmission_visual.__file__).resolve(),
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

    def test_validator_rejects_bad_fact_and_source_bindings(self) -> None:
        unregistered = deepcopy(self.manifest)
        unregistered["transmission_principles"][0]["fact_refs"][0] = (
            "outside:known_fact"
        )
        with self.assertRaisesRegex(
            transmission_visual.TransmissionVisualError,
            "unregistered evidence ledger",
        ):
            self.compile(unregistered)

        unknown = deepcopy(self.manifest)
        ledger_id = next(iter(self.ledgers))
        unknown["transmission_principles"][0]["fact_refs"][0] = (
            f"{ledger_id}:missing_fact"
        )
        with self.assertRaisesRegex(
            transmission_visual.TransmissionVisualError,
            "unknown fact reference",
        ):
            self.compile(unknown)

        ref = self.manifest["transmission_principles"][0]["fact_refs"][0]
        ledger_id, fact_id = ref.split(":", 1)
        missing = deepcopy(self.ledgers)
        missing[ledger_id]["facts"][fact_id]["source_ids"] = []
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "expected 1 to 12 entries",
        ):
            self.compile(ledgers=missing)

        unknown_source = deepcopy(self.ledgers)
        unknown_source[ledger_id]["facts"][fact_id]["source_ids"] = ["missing_source"]
        with self.assertRaisesRegex(
            teaching_visuals.TeachingVisualError,
            "unknown source IDs",
        ):
            self.compile(ledgers=unknown_source)

    def test_validator_rejects_pacing_layer_escape_and_bad_handoff(self) -> None:
        paced = deepcopy(self.manifest)
        paced["states"][0]["duration_seconds"] = 30
        with self.assertRaisesRegex(
            transmission_visual.TransmissionVisualError,
            "pacing or scripting fields",
        ):
            self.compile(paced)

        escaped = deepcopy(self.manifest)
        escaped["states"][0]["principle_ids"][0] = "invented_principle"
        with self.assertRaisesRegex(
            transmission_visual.TransmissionVisualError,
            "unknown principles",
        ):
            self.compile(escaped)

        multiple = deepcopy(self.manifest)
        multiple["states"][0]["show_substation"] = True
        with self.assertRaisesRegex(
            transmission_visual.TransmissionVisualError,
            "exactly one primary teaching layer",
        ):
            self.compile(multiple)

        incomplete = deepcopy(self.manifest)
        incomplete["states"][-1]["show_handoff"] = False
        with self.assertRaisesRegex(
            transmission_visual.TransmissionVisualError,
            "only the final pilot state may reveal",
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
                    transmission_visual.TransmissionVisualError,
                    "schema_version must be 1",
                ),
            ):
                self.compile(manifest)

        with TemporaryDirectory(prefix="gigawatt-phase2-yaml-") as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("schema_version: 1\nschema_version: 1\n")
            with self.assertRaisesRegex(
                teaching_visuals.TeachingVisualError,
                "duplicate YAML key",
            ):
                teaching_visuals.load_yaml(path)

    def test_checked_in_output_matches_deterministic_build(self) -> None:
        rendered, digest, _ = self.native.build()
        self.assertTrue(OUTPUT.exists())
        self.assertEqual(rendered, OUTPUT.read_text())
        self.assertIn(
            f'<meta name="gigawatt-source-digest" content="{digest}">', rendered
        )


if __name__ == "__main__":
    unittest.main()
