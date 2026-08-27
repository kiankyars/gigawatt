from __future__ import annotations

import unittest
from copy import deepcopy

from gigawatt import validate


def segment_by_id(course: dict, segment_id: str) -> dict:
    return next(
        segment
        for act in course["acts"]
        for segment in act["segments"]
        if segment["id"] == segment_id
    )


class CourseInventoryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.course = validate._load_yaml_strict(validate.COURSE)
        cls.master = validate._load_yaml_strict(validate.DIAGRAM / "master.yaml")
        cls.ledgers = validate._load_course_evidence_ledgers(cls.course)
        cls.cameras = validate._load_yaml_strict(validate.DIAGRAM / "cameras.yaml")

    def validate(
        self,
        course: dict | None = None,
        ledgers: dict | None = None,
    ) -> dict[str, int]:
        return validate._validate_course(
            course or self.course,
            self.master,
            ledgers or self.ledgers,
            self.cameras,
        )

    def test_complete_course_contract(self) -> None:
        result = self.validate()
        self.assertEqual(7, result["acts"])
        self.assertEqual(26, result["segments"])
        self.assertEqual(26, result["evidence_ready_segments"])
        self.assertEqual(0, result["research_required_segments"])
        self.assertEqual(21, result["planned_shots"])
        self.assertIsNone(self.course["meta"]["runtime_minutes"])

    def test_every_visible_master_record_is_taught(self) -> None:
        segments = [
            segment
            for act in self.course["acts"]
            for segment in act["segments"]
        ]
        covered_nodes = {node_id for segment in segments for node_id in segment["node_ids"]}
        covered_edges = {edge_id for segment in segments for edge_id in segment["edge_ids"]}
        visible_nodes = {
            node["id"]
            for node in self.master["nodes"]
            if node.get("base_visible", True) is not False
        }
        visible_edges = {
            edge["id"]
            for edge in self.master["edges"]
            if edge.get("base_visible", True) is not False
        }
        self.assertEqual(set(), visible_nodes - covered_nodes)
        self.assertEqual(set(), visible_edges - covered_edges)

    def test_all_validated_camera_anchors_are_used(self) -> None:
        anchors = {
            segment["camera"]["anchor"]
            for act in self.course["acts"]
            for segment in act["segments"]
        }
        self.assertEqual(
            {camera["id"] for camera in self.cameras["cameras"]},
            anchors,
        )

    def test_physical_figure_eight_is_ordered_and_balanced(self) -> None:
        segments = [
            segment
            for act in self.course["acts"]
            for segment in act["segments"]
        ]
        ids = [segment["id"] for segment in segments]
        electrical = [segment_by_id(self.course, f"s{index:02d}_{suffix}") for index, suffix in (
            (1, "fire_to_electricity"),
            (2, "generator_terminal"),
            (3, "initial_grid_path"),
            (4, "expansion_grid_path"),
            (5, "ppa_not_wire"),
            (6, "campus_mv_envelope"),
            (7, "building_power_train"),
            (8, "rack_voltage_descent"),
        )]
        thermal = [segment_by_id(self.course, f"s{index:02d}_{suffix}") for index, suffix in (
            (9, "watt_becomes_heat"),
            (10, "two_rack_heat_paths"),
            (11, "technology_loop"),
            (12, "cdu_boundary"),
            (13, "residual_air_branch"),
            (14, "facility_heat_rejection"),
            (15, "water_accounting"),
            (16, "close_atmosphere"),
        )]
        self.assertLess(ids.index(electrical[-1]["id"]), ids.index(thermal[0]["id"]))
        self.assertLess(
            abs(
                sum(segment["weight"] for segment in electrical)
                - sum(segment["weight"] for segment in thermal)
            ),
            1.0,
        )

    def test_unknown_ids_and_incomplete_edges_fail(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s03_initial_grid_path")["node_ids"].append("not_a_node")
        with self.assertRaisesRegex(validate.ValidationError, "unknown_nodes"):
            self.validate(course)

        course = deepcopy(self.course)
        segment_by_id(course, "s03_initial_grid_path")["node_ids"].remove(
            "initial_tie_138"
        )
        with self.assertRaisesRegex(validate.ValidationError, "edge endpoints absent"):
            self.validate(course)

    def test_existing_camera_cannot_exceed_its_focus(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s08_rack_voltage_descent")["node_ids"].append("cdu")
        with self.assertRaisesRegex(validate.ValidationError, "focus exceeds"):
            self.validate(course)

    def test_transition_must_follow_canonical_order(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "p0_gigawatt_not_workload")["transition"]["to"] = (
            "s24_megawatts_to_tokens"
        )
        with self.assertRaisesRegex(validate.ValidationError, "transition must target"):
            self.validate(course)

    def test_redline_sensitive_readiness_is_explicit(self) -> None:
        self.assertEqual(
            "evidence_ready",
            segment_by_id(self.course, "s03_initial_grid_path")["evidence"]["readiness"],
        )
        thermal_close = segment_by_id(self.course, "s16_close_atmosphere")["evidence"]
        self.assertEqual("evidence_ready", thermal_close["readiness"])
        self.assertEqual([], thermal_close["blocking_research"])
        self.assertIn(
            "facility_interface_boundary",
            {claim["id"] for claim in thermal_close["claims"]},
        )

    def test_bound_fact_cannot_move_to_unrelated_topology(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s08_rack_voltage_descent")["evidence"]["claims"].append(
            {
                "id": "misplaced_gas_claim",
                "assertion": "permitted",
                "binding": "topology",
                "fact_refs": ["abilene:gas_permitted_nameplate_mw"],
            }
        )
        with self.assertRaisesRegex(validate.ValidationError, "not bound to selected topology"):
            self.validate(course)

    def test_claim_assertion_cannot_promote_permit_evidence(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s01_fire_to_electricity")["evidence"]["claims"][0][
            "assertion"
        ] = "confirmed"
        with self.assertRaisesRegex(validate.ValidationError, "cannot support assertion"):
            self.validate(course)

    def test_commercial_references_keep_contract_and_accounting_semantics(self) -> None:
        claims = segment_by_id(self.course, "s05_ppa_not_wire")["evidence"]["claims"]
        self.assertEqual(
            ["contract_reference", "accounting_reference"],
            [claim["assertion"] for claim in claims],
        )

        ledgers = deepcopy(self.ledgers)
        ledgers["commercial_energy"]["facts"]["crane_microsoft_ppa_contract"][
            "lifecycle"
        ] = "design_reference"
        with self.assertRaisesRegex(validate.ValidationError, "cannot support assertion"):
            self.validate(ledgers=ledgers)

    def test_derived_scenarios_are_not_promoted_to_published_methods(self) -> None:
        claims = segment_by_id(self.course, "s24_megawatts_to_tokens")["evidence"][
            "claims"
        ]
        by_id = {claim["id"]: claim for claim in claims}
        self.assertEqual("method_reference", by_id["pue_accounting_boundary"]["assertion"])
        self.assertEqual(
            "derived_scenario_reference",
            by_id["complete_scenario_recipe"]["assertion"],
        )

        course = deepcopy(self.course)
        mutable_claims = segment_by_id(course, "s24_megawatts_to_tokens")["evidence"][
            "claims"
        ]
        next(
            claim for claim in mutable_claims if claim["id"] == "complete_scenario_recipe"
        )["assertion"] = "method_reference"
        with self.assertRaisesRegex(validate.ValidationError, "cannot support assertion"):
            self.validate(course=course)

        course = deepcopy(self.course)
        segment_by_id(course, "s24_megawatts_to_tokens")["evidence"][
            "promotion_guards"
        ].remove("energy_power_time_basis")
        with self.assertRaisesRegex(validate.ValidationError, "missing assertion promotion guards"):
            self.validate(course=course)

    def test_scope_sensitive_summary_guards_are_explicit(self) -> None:
        s17 = segment_by_id(self.course, "s17_interconnection_schedule")
        s18 = segment_by_id(self.course, "s18_long_lead_equipment")
        s19 = segment_by_id(self.course, "s19_fast_load_slow_grid")
        s20 = segment_by_id(self.course, "s20_build_sequence")
        s21 = segment_by_id(self.course, "s21_capital_ownership")
        s22 = segment_by_id(self.course, "s22_capital_risk")

        self.assertIn("single_path_conflation", s17["evidence"]["promotion_guards"])
        self.assertIn(
            "market_example_to_site_schedule", s18["evidence"]["promotion_guards"]
        )
        self.assertNotIn("bess_to_mv", s19["edge_ids"])
        self.assertIn("substation_to_it_load", s20["evidence"]["promotion_guards"])
        self.assertIn(
            "named_role_to_asset_assignment", s21["evidence"]["promotion_guards"]
        )
        self.assertIn(
            "facility_financing_to_component_allocation",
            s22["evidence"]["promotion_guards"],
        )

        course = deepcopy(self.course)
        segment_by_id(course, "s05_ppa_not_wire")["evidence"]["promotion_guards"].remove(
            "contractual_to_physical"
        )
        with self.assertRaisesRegex(validate.ValidationError, "missing assertion promotion guards"):
            self.validate(course=course)

        ledgers = deepcopy(self.ledgers)
        ledgers["commercial_energy"]["facts"][
            "scope2_contractual_attributes_not_physical_flow"
        ]["posture"] = "design_not_observed"
        with self.assertRaisesRegex(validate.ValidationError, "cannot support assertion"):
            self.validate(ledgers=ledgers)

    def test_research_gate_and_schema_fail_closed(self) -> None:
        course = deepcopy(self.course)
        evidence = segment_by_id(course, "s17_interconnection_schedule")["evidence"]
        evidence["readiness"] = "research_required"
        evidence["blocking_research"] = []
        with self.assertRaisesRegex(validate.ValidationError, "needs blocking research"):
            self.validate(course)

        course = deepcopy(self.course)
        segment_by_id(course, "s03_initial_grid_path")["evidence"]["claims"][0][
            "source_ids"
        ] = ["mortenson_abilene_power_delivery"]
        with self.assertRaisesRegex(validate.ValidationError, r"extra=\['source_ids'\]"):
            self.validate(course)

    def test_dependencies_cannot_promote_a_summary(self) -> None:
        course = deepcopy(self.course)
        dependency = segment_by_id(course, "s12_cdu_boundary")["evidence"]
        dependency["readiness"] = "research_required"
        dependency["blocking_research"] = ["A new primary-source package is required."]
        with self.assertRaisesRegex(validate.ValidationError, "cannot depend on research-gated"):
            self.validate(course)

    def test_hidden_overlays_require_exact_reveal_intent(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s05_ppa_not_wire")["camera"]["reveal_ids"] = []
        with self.assertRaisesRegex(validate.ValidationError, "reveal_ids must exactly match"):
            self.validate(course)

        course = deepcopy(self.course)
        segment_by_id(course, "s05_ppa_not_wire")["camera"]["reveal_copy_ids"] = []
        with self.assertRaisesRegex(
            validate.ValidationError,
            "reveal_copy_ids must exactly match",
        ):
            self.validate(course)

    def test_hidden_ppa_reveal_bundle_is_complete(self) -> None:
        for segment_id in (
            "s05_ppa_not_wire",
            "s21_capital_ownership",
            "s23_business_models",
        ):
            camera = segment_by_id(self.course, segment_id)["camera"]
            self.assertEqual(["nuclear_variant"], camera["reveal_copy_ids"])

        svg = (validate.DIAGRAM / "master.svg").read_text()
        for svg_id in (
            "node-nuclear_ppa",
            "edge-nuclear_ppa_overlay",
            "label-nuclear_variant",
        ):
            with self.subTest(svg_id=svg_id):
                self.assertRegex(
                    svg,
                    rf'<g[^>]*id="{svg_id}"[^>]*display="none"',
                )

    def test_assertions_require_promotion_guards_and_real_blockers(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "p0_gigawatt_not_workload")["evidence"][
            "promotion_guards"
        ].remove("planned_to_operational")
        with self.assertRaisesRegex(validate.ValidationError, "missing assertion promotion guards"):
            self.validate(course)

        course = deepcopy(self.course)
        segment_by_id(course, "s17_interconnection_schedule")["evidence"][
            "blocking_research"
        ] = ["TBD"]
        with self.assertRaisesRegex(validate.ValidationError, "placeholders"):
            self.validate(course)

    def test_unbound_fact_requires_overlay_binding(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s15_water_accounting")["evidence"]["claims"].append(
            {
                "id": "unrelated_gpu_claim",
                "assertion": "no_evidence_backed_estimate",
                "binding": "topology",
                "fact_refs": ["abilene:installed_gpu_count"],
            }
        )
        with self.assertRaisesRegex(validate.ValidationError, "not bound to selected topology"):
            self.validate(course)

    def test_overlay_cannot_bypass_master_topology(self) -> None:
        course = deepcopy(self.course)
        claim = segment_by_id(course, "s03_initial_grid_path")["evidence"]["claims"][0]
        claim["binding"] = "overlay"
        with self.assertRaisesRegex(validate.ValidationError, "cannot bypass master topology"):
            self.validate(course)

    def test_qualified_refs_support_multiple_ledgers_without_collision(self) -> None:
        course = deepcopy(self.course)
        course["meta"]["evidence_ledgers"]["comparison"] = "evidence/comparison.yaml"
        ledgers = deepcopy(self.ledgers)
        ledgers["comparison"] = deepcopy(ledgers["abilene"])
        segment_by_id(course, "s23_business_models")["evidence"]["claims"].append(
            {
                "id": "comparison_platform",
                "assertion": "confirmed",
                "binding": "overlay",
                "fact_refs": ["comparison:rack_platform"],
            }
        )
        self.validate(course, ledgers)

        course = deepcopy(course)
        segment_by_id(course, "s23_business_models")["evidence"]["claims"][0][
            "binding"
        ] = "topology"
        with self.assertRaisesRegex(validate.ValidationError, "not bound to selected topology"):
            self.validate(course, ledgers)

    def test_ledger_registry_and_fact_refs_fail_closed(self) -> None:
        course = deepcopy(self.course)
        course["meta"]["evidence_ledgers"]["duplicate"] = "evidence/abilene.yaml"
        ledgers = {**self.ledgers, "duplicate": self.ledgers["abilene"]}
        with self.assertRaisesRegex(validate.ValidationError, "paths must be unique"):
            self.validate(course, ledgers)

        course = deepcopy(self.course)
        course["meta"]["evidence_ledgers"]["outside"] = "../outside.yaml"
        ledgers = {**self.ledgers, "outside": self.ledgers["abilene"]}
        with self.assertRaisesRegex(validate.ValidationError, "remain under evidence"):
            self.validate(course, ledgers)

        course = deepcopy(self.course)
        claim = segment_by_id(course, "p0_gigawatt_not_workload")["evidence"]["claims"][0]
        claim["fact_refs"] = ["unqualified_fact"]
        with self.assertRaisesRegex(validate.ValidationError, "malformed qualified"):
            self.validate(course)

    def test_lifecycle_and_no_estimate_assertions_fail_closed(self) -> None:
        ledgers = deepcopy(self.ledgers)
        ledgers["abilene"]["facts"]["buildings_energized_confirmed_min"][
            "lifecycle"
        ] = "planned"
        with self.assertRaisesRegex(validate.ValidationError, "cannot support assertion"):
            self.validate(ledgers=ledgers)

        ledgers = deepcopy(self.ledgers)
        ledgers["abilene"]["facts"]["installed_gpu_count"]["basis"] = "unknown"
        with self.assertRaisesRegex(validate.ValidationError, "cannot support assertion"):
            self.validate(ledgers=ledgers)

    def test_non_finite_weights_fail(self) -> None:
        course = deepcopy(self.course)
        course["meta"]["relative_weight_total"] = float("nan")
        segment_by_id(course, "p0_gigawatt_not_workload")["weight"] = float("nan")
        with self.assertRaisesRegex(validate.ValidationError, "finite"):
            self.validate(course)


if __name__ == "__main__":
    unittest.main()
