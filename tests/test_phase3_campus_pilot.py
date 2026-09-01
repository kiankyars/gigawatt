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

from gigawatt import campus_visual, teaching_visuals

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "course" / "pilots" / "phase3_campus.yaml"
GENERATOR = ROOT / "diagram" / "generate_phase3_campus.py"
OUTPUT = ROOT / "diagram" / "phase3_campus.html"


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


class Phase3CampusPilotTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.native = load_module("gigawatt_phase3_campus", GENERATOR)
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
        return campus_visual.compile_campus_distribution(
            deepcopy(self.manifest if manifest is None else manifest),
            deepcopy(self.ledgers if ledgers is None else ledgers),
            source_digest="0" * 64,
        )

    def test_manifest_is_manual_untimed_and_uses_five_coarse_states(self) -> None:
        self.assertEqual(
            {"mode": "manual", "advance": "instructor_controlled"},
            self.manifest["interaction"],
        )
        self.assertEqual(
            [
                "one_source_fanout",
                "feeder_fault_isolation",
                "abilene_unknown_merge",
                "separate_resilience_roles",
                "building_power_handoff",
            ],
            [state["id"] for state in self.manifest["states"]],
        )
        self.assertEqual(
            ["Fan-out", "Isolation", "Sources", "Roles", "Building"],
            [state["nav_label"] for state in self.manifest["states"]],
        )
        self.assertEqual([], teaching_visuals._forbidden_fields(self.manifest))
        for state in self.manifest["states"]:
            primary_layers = (
                state["show_generic_fanout"],
                state["show_feeder_fault_isolation"],
                bool(state["abilene_source_ids"]) or state["show_abilene_merge"],
                bool(state["resilience_role_ids"]),
                state["show_phase4_handoff"],
            )
            with self.subTest(state=state["id"]):
                self.assertEqual(1, sum(primary_layers))
        self.assertTrue(self.manifest["states"][1]["show_feeder_fault_isolation"])
        self.assertTrue(
            all("building_stage_ids" not in state for state in self.manifest["states"])
        )
        self.assertTrue(self.manifest["states"][-1]["show_phase4_handoff"])

    def test_every_claim_and_gap_guard_is_source_bound(self) -> None:
        payload = self.compile()
        content = {
            key: self.manifest[key]
            for key in (
                "generic_fanout",
                "feeder_fault_isolation",
                "abilene_source_boundary",
                "resilience_roles",
                "building_lifecycle",
                "phase4_handoff",
                "evidence_gaps",
            )
        }
        self.assertEqual(
            authored_refs(content),
            {fact["ref"] for fact in payload["evidence"]["facts"]},
        )
        self.assertEqual(48, len(payload["evidence"]["facts"]))
        self.assertEqual(29, len(payload["evidence"]["sources"]))
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
            "data-generic-fanout hidden",
            "data-feeder-fault-isolation hidden",
            'data-feeder-fault-stage-id="protection_detects"',
            'data-abilene-source-id="initial_grid"',
            'data-resilience-role-id="ups"',
            "data-phase4-handoff hidden",
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

    def test_svg_is_a_hybrid_with_purpose_built_state_visuals(self) -> None:
        payload = self.compile()
        rendered = campus_visual.render_campus_distribution(payload)
        required = (
            "GENERIC CAMPUS ORIENTATION · NOT ABILENE",
            'class="campus-ground"',
            'class="iso-building ',
            'class="orientation-compass"',
            "GENERIC FEEDER PROTECTION · CAUSAL SEQUENCE",
            "DISTURBANCE → DETECT → INTERRUPT → ISOLATE",
            'data-feeder-fault-stage-id="feeder_disturbance"',
            'data-feeder-fault-stage-id="protection_detects"',
            'data-feeder-fault-stage-id="protective_device_interrupts"',
            'data-feeder-fault-stage-id="faulted_branch_isolated"',
            "CONDITIONAL · NOT GUARANTEED",
            "Only if all three conditions hold.",
            "ABILENE EVIDENCE · THREE SEPARATE 2D LANES",
            "STOPS AT UNKNOWN MERGE",
            "NO SHARED BUS DRAWN",
            'class="role-diagram ups-diagram"',
            'class="role-diagram bess-diagram"',
            'class="role-diagram diesel-diagram"',
            "THREE INDEPENDENT REFERENCE DIAGRAMS · NOT A SEQUENCE",
            "NEXT · PHASE 4 · GENERIC FUNCTIONAL CHAIN",
            'class="handoff-cover" x="0" y="0" width="1600" height="900"',
            "Unit substation",
            "Switchgear",
            "Busway",
            "RACK POSITIONS",
        )
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, rendered)
        self.assertEqual(3, rendered.count('class="source-lane-card"'))
        self.assertEqual(4, rendered.count('class="fault-stage-card"'))
        self.assertEqual(3, rendered.count('class="remaining-condition-card"'))
        self.assertEqual(4, rendered.count('class="equipment-card"'))
        fanout = campus_visual._fanout_svg(payload["generic_fanout"])
        label_y = [
            float(value)
            for value in re.findall(
                r'class="iso-building-label centered"[^>]+y="([0-9.]+)"',
                fanout,
            )
        ]
        scope_y = float(
            re.search(r'class="scope-box"[^>]+y="([0-9.]+)"', fanout).group(1)
        )
        self.assertEqual(3, len(label_y))
        self.assertLess(max(label_y) + 18, scope_y)
        isolation = campus_visual._feeder_fault_isolation_svg(
            payload["feeder_fault_isolation"]
        )
        stage_boxes = [
            tuple(float(value) for value in match)
            for match in re.findall(
                r'class="fault-stage-card" x="([0-9.]+)" y="([0-9.]+)" width="([0-9.]+)" height="([0-9.]+)"',
                isolation,
            )
        ]
        self.assertEqual(4, len(stage_boxes))
        for x, y, width, height in stage_boxes:
            self.assertGreaterEqual(x, 42)
            self.assertGreaterEqual(y, 42)
            self.assertLessEqual(x + width, 1558)
            self.assertLessEqual(y + height, 858)
        outcome = re.search(
            r'class="conditional-outcome-card" x="([0-9.]+)" y="([0-9.]+)" width="([0-9.]+)" height="([0-9.]+)"',
            isolation,
        )
        self.assertIsNotNone(outcome)
        outcome_x, _, outcome_width, _ = (float(value) for value in outcome.groups())
        self.assertLessEqual(outcome_x + outcome_width, 1512)
        visible_markup = rendered.split(
            '<script id="pilot-data" type="application/json">', maxsplit=1
        )[0]
        self.assertNotIn("data-building-lifecycle", visible_markup)
        self.assertNotIn("data-building-stage-id", visible_markup)
        self.assertNotIn("DISCLOSURE LADDER", visible_markup)
        for state_svg in (
            fanout,
            isolation,
            campus_visual._source_boundary_svg(payload["abilene_source_boundary"]),
            campus_visual._roles_svg(payload["resilience_roles"]),
            campus_visual._handoff_svg(payload["phase4_handoff"]),
        ):
            self.assertNotIn("…", state_svg)

    def test_supported_viewports_use_readable_surfaces_and_full_nav(self) -> None:
        self.assertEqual(
            {
                "surface": "html",
                "profile": "course_landscape",
                "columns": 2,
                "minimum_text_px": 12,
                "scroll_axis": "vertical",
            },
            campus_visual.responsive_layout_contract(1280, 720),
        )
        tablet = campus_visual.responsive_layout_contract(1024, 768)
        short = campus_visual.responsive_layout_contract(844, 390)
        portrait = campus_visual.responsive_layout_contract(390, 844)
        standard = campus_visual.responsive_layout_contract(1440, 900)
        self.assertEqual(
            ("html", "tablet", 12),
            (tablet["surface"], tablet["profile"], tablet["minimum_text_px"]),
        )
        self.assertEqual(
            ("html", "short_landscape", 10),
            (short["surface"], short["profile"], short["minimum_text_px"]),
        )
        self.assertEqual(
            ("html", "portrait", 12),
            (portrait["surface"], portrait["profile"], portrait["minimum_text_px"]),
        )
        self.assertEqual("svg", standard["surface"])
        for dimensions in ((0, 720), (-1, 720), (1280, 0), (1280.0, 720)):
            with (
                self.subTest(dimensions=dimensions),
                self.assertRaisesRegex(
                    campus_visual.CampusVisualError,
                    "positive integers",
                ),
            ):
                campus_visual.responsive_layout_contract(*dimensions)

        rendered = campus_visual.render_campus_distribution(self.compile())
        self.assertIn("@media (max-width:1280px), (max-height:760px)", rendered)
        self.assertIn("font-size:12px", rendered)
        self.assertIn("font-size:10px", rendered)
        self.assertIn(
            ".state-nav-label { overflow:visible; text-overflow:clip; white-space:normal; }",
            rendered,
        )
        self.assertIn(".state-copy p { display:none; }", rendered)

    def test_responsive_html_is_payload_driven_and_matches_state_order(self) -> None:
        payload = self.compile()
        rendered = campus_visual.render_campus_distribution(payload)
        self.assertIn('class="responsive-visual"', rendered)
        self.assertIn(".responsive-visual { display:block", rendered)
        for source in payload["abilene_source_boundary"]["sources"]:
            self.assertEqual(
                2,
                rendered.count(f'data-abilene-source-id="{source["id"]}"'),
            )
        for role in payload["resilience_roles"]["roles"]:
            self.assertEqual(
                2,
                rendered.count(f'data-resilience-role-id="{role["id"]}"'),
            )
        for stage in payload["feeder_fault_isolation"]["stages"]:
            self.assertEqual(
                2,
                rendered.count(f'data-feeder-fault-stage-id="{stage["id"]}"'),
            )
        self.assertEqual(2, rendered.count("data-generic-fanout hidden"))
        self.assertEqual(2, rendered.count("data-feeder-fault-isolation hidden"))
        self.assertEqual(2, rendered.count("data-phase4-handoff hidden"))
        self.assertLess(
            rendered.index(
                '<section class="responsive-scene responsive-fault-isolation"'
            ),
            rendered.index(
                '<section class="responsive-scene responsive-source-boundary"'
            ),
        )

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
        rendered = campus_visual.render_campus_distribution(payload)
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
                Path(campus_visual.__file__).resolve(),
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

    def test_validator_rejects_bad_content_and_gap_fact_refs(self) -> None:
        bad_content = deepcopy(self.manifest)
        bad_content["generic_fanout"]["fact_refs"][0] = "outside:known_fact"
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "unregistered evidence ledger",
        ):
            self.compile(bad_content)

        bad_gap = deepcopy(self.manifest)
        bad_gap["evidence_gaps"][0]["related_fact_refs"][0] = (
            "generation_transmission:missing_fact"
        )
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "unknown fact reference",
        ):
            self.compile(bad_gap)

    def test_validator_rejects_pacing_layer_escape_and_completed_commissioning(
        self,
    ) -> None:
        paced = deepcopy(self.manifest)
        paced["states"][0]["duration_seconds"] = 30
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "pacing or scripting fields",
        ):
            self.compile(paced)

        escaped = deepcopy(self.manifest)
        escaped["states"][0]["resilience_role_ids"] = ["ups"]
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "exactly one primary teaching layer",
        ):
            self.compile(escaped)

        split_merge = deepcopy(self.manifest)
        split_merge["states"][2]["show_abilene_merge"] = False
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "must stay together",
        ):
            self.compile(split_merge)

        completed = deepcopy(self.manifest)
        completed["building_lifecycle"]["stages"][2]["title"] = "Commissioned"
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "remain explicitly unresolved",
        ):
            self.compile(completed)

    def test_fault_isolation_contract_fails_closed(self) -> None:
        reordered = deepcopy(self.manifest)
        reordered["feeder_fault_isolation"]["stages"][0]["id"] = (
            "unexpected_fault_stage"
        )
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "canonical order",
        ):
            self.compile(reordered)

        unbound = deepcopy(self.manifest)
        unbound["feeder_fault_isolation"]["stages"][0]["fact_refs"] = [
            "generation_transmission:substation_is_transform_protect_control_gate"
        ]
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "coordinated isolation evidence",
        ):
            self.compile(unbound)

        guaranteed = deepcopy(self.manifest)
        guaranteed["feeder_fault_isolation"]["remaining_service"]["title"] = (
            "Remaining building service is guaranteed"
        )
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "conditional, not guaranteed",
        ):
            self.compile(guaranteed)

        site_claim = deepcopy(self.manifest)
        site_claim["feeder_fault_isolation"]["boundary"]["body"] = (
            "A generic feeder sequence."
        )
        with self.assertRaisesRegex(
            campus_visual.CampusVisualError,
            "withhold Abilene topology",
        ):
            self.compile(site_claim)

    def test_schema_path_and_checked_in_output_fail_closed(self) -> None:
        for invalid in (True, 1.0, "1"):
            manifest = deepcopy(self.manifest)
            manifest["schema_version"] = invalid
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(
                    campus_visual.CampusVisualError,
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

        with TemporaryDirectory(prefix="gigawatt-phase3-yaml-") as directory:
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
