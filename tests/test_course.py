from __future__ import annotations

import unittest
from copy import deepcopy
from types import MappingProxyType
from unittest.mock import patch

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
        cls.visuals = validate._load_yaml_strict(validate.COURSE_VISUALS)
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
            segment for act in self.course["acts"] for segment in act["segments"]
        ]
        covered_nodes = {
            node_id for segment in segments for node_id in segment["node_ids"]
        }
        covered_edges = {
            edge_id for segment in segments for edge_id in segment["edge_ids"]
        }
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
            segment for act in self.course["acts"] for segment in act["segments"]
        ]
        ids = [segment["id"] for segment in segments]
        electrical = [
            segment_by_id(self.course, f"s{index:02d}_{suffix}")
            for index, suffix in (
                (1, "fire_to_electricity"),
                (2, "generator_terminal"),
                (3, "initial_grid_path"),
                (4, "expansion_grid_path"),
                (5, "ppa_not_wire"),
                (6, "campus_mv_envelope"),
                (7, "building_power_train"),
                (8, "rack_voltage_descent"),
            )
        ]
        thermal = [
            segment_by_id(self.course, f"s{index:02d}_{suffix}")
            for index, suffix in (
                (9, "watt_becomes_heat"),
                (10, "two_rack_heat_paths"),
                (11, "technology_loop"),
                (12, "cdu_boundary"),
                (13, "residual_air_branch"),
                (14, "facility_heat_rejection"),
                (15, "water_accounting"),
                (16, "close_atmosphere"),
            )
        ]
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
            segment_by_id(self.course, "s03_initial_grid_path")["evidence"][
                "readiness"
            ],
        )
        thermal_close = segment_by_id(self.course, "s16_close_atmosphere")["evidence"]
        self.assertEqual("evidence_ready", thermal_close["readiness"])
        self.assertEqual([], thermal_close["blocking_research"])
        self.assertIn(
            "facility_interface_boundary",
            {claim["id"] for claim in thermal_close["claims"]},
        )

    def test_water_and_closing_handoff_preserve_the_teaching_boundary(self) -> None:
        water = segment_by_id(self.course, "s15_water_accounting")
        thermal_close = segment_by_id(self.course, "s16_close_atmosphere")
        measured_claim = next(
            claim
            for claim in water["evidence"]["claims"]
            if claim["id"] == "measured_operating_consumption_unknown"
        )
        self.assertEqual("explicit_unknown", measured_claim["assertion"])
        measured_fact = self.ledgers["abilene"]["facts"][
            "cooling_measured_operating_consumption_gallons"
        ]
        self.assertIsNone(measured_fact["value"])
        self.assertEqual("unverified_null", measured_fact["posture"])
        self.assertIn("measured consumption remains unknown", water["opening_question"])
        self.assertIn("fill_treatment", water["node_ids"])
        self.assertIn("fill_to_facility_loop", water["edge_ids"])
        self.assertNotIn("fill_treatment", thermal_close["node_ids"])
        self.assertNotIn("fill_to_facility_loop", thermal_close["edge_ids"])

        rack = segment_by_id(self.course, "s08_rack_voltage_descent")
        self.assertIn("deliberately unknown", rack["opening_question"])
        closing_cue = segment_by_id(self.course, "s23_business_models")["transition"][
            "cue"
        ]
        self.assertIn("no-estimate stop rule", closing_cue)
        self.assertNotIn("every physical and economic gate", closing_cue)

    def test_repeated_funnel_uses_one_five_stage_taxonomy(self) -> None:
        expected_stages = [
            "PLANNED",
            "CONSTRUCTED",
            "ENERGIZED",
            "LIVE",
            "UNKNOWN",
        ]
        self.assertEqual(
            [stage.lower() for stage in expected_stages],
            self.master["meta"]["gigawatts_to_tokens_funnel"],
        )

        for segment_id in ("p0_gigawatt_not_workload", "s20_build_sequence"):
            annotation = self.visuals["segments"][segment_id]["annotation"]
            self.assertEqual("funnel", annotation["kind"])
            self.assertEqual(
                expected_stages,
                [item["label"].split(" ", 1)[0] for item in annotation["items"]],
            )

        p0 = segment_by_id(self.course, "p0_gigawatt_not_workload")
        p0_claims = {claim["id"]: claim for claim in p0["evidence"]["claims"]}
        self.assertEqual(
            [
                "abilene:grid_initial_substation_capacity_mw",
                "abilene:grid_initial_substation_voltage_kv",
            ],
            p0_claims["initial_substation_rating"]["fact_refs"],
        )
        self.assertEqual(
            [
                "abilene:grid_expansion_substation_capacity_mw",
                "abilene:grid_expansion_substation_voltage_kv",
            ],
            p0_claims["expansion_substation_rating"]["fact_refs"],
        )
        self.assertIn(
            "PERMITTED is a separate authorization",
            self.visuals["segments"][p0["id"]]["annotation"]["title"],
        )
        constructed_item = self.visuals["segments"][p0["id"]]["annotation"]["items"][1]
        self.assertIn("PERMITTED", constructed_item["label"])
        self.assertIn("separate axis", constructed_item["label"])
        self.assertEqual(
            {
                "initial_substation_rating",
                "permitted_gas_layer",
                "permitted_diesel_layer",
            },
            set(constructed_item["claim_ids"]),
        )
        for claim_id in ("permitted_gas_layer", "permitted_diesel_layer"):
            self.assertEqual("permitted", p0_claims[claim_id]["assertion"])
            self.assertEqual("topology", p0_claims[claim_id]["binding"])
        self.assertTrue(
            {"permitted_to_installed", "permitted_to_commissioned"}
            <= set(p0["evidence"]["promotion_guards"])
        )

        s20 = segment_by_id(self.course, "s20_build_sequence")
        s20_claims = {claim["id"]: claim for claim in s20["evidence"]["claims"]}
        self.assertEqual(
            "Build sequence is a staged evidence boundary",
            s20["title"],
        )
        self.assertEqual(
            "Which delivery stages are evidenced, and where must inference stop?",
            s20["opening_question"],
        )
        self.assertNotIn("binding constraint", s20["title"].lower())
        self.assertNotIn("did", s20["opening_question"].lower())
        self.assertEqual(
            ["abilene_execution:campus_construction_start_month"],
            s20_claims["construction_start"]["fact_refs"],
        )
        self.assertEqual(
            ["abilene_execution:first_two_buildings_energized_by"],
            s20_claims["first_two_buildings_energized"]["fact_refs"],
        )
        self.assertEqual(
            ["abilene_execution:first_phase_operational_by"],
            s20_claims["first_phase_operational"]["fact_refs"],
        )
        self.assertEqual(
            "explicit_unknown",
            s20_claims["current_delivery_boundary"]["assertion"],
        )
        self.assertEqual(
            [
                "installed_gpu_no_estimate",
                "untyped_delivery_boundary",
                "current_delivery_boundary",
            ],
            self.visuals["segments"][s20["id"]]["annotation"]["items"][-1]["claim_ids"],
        )

    def test_p1_exposes_fixed_four_channel_grammar(self) -> None:
        visual = self.visuals["segments"]["p1_read_the_machine"]
        legend_ids = [
            "legend_title",
            "legend_direction",
            "legend_posture",
            "legend_energized",
            "legend_permitted",
            "legend_future",
            "legend_conceptual",
        ]
        self.assertFalse(visual["show_legend"])
        self.assertEqual(
            legend_ids
            + [
                "gas_permit",
                "station_138",
                "bess",
                "mv_unknown",
                "air_cooled_chiller",
            ],
            visual["label_copy_ids"],
        )

        self.assertEqual(
            {
                "legend_title": "COLOR = CARRIER · STROKE = LIFECYCLE",
                "legend_direction": "direction · named source→destination path order",
                "legend_posture": (
                    "evidence posture · claim copy / evidence drawer; not stroke"
                ),
                "legend_energized": "solid · energized lifecycle",
                "legend_permitted": "dotted · permitted lifecycle",
                "legend_future": "dashed · future-design lifecycle",
                "legend_conceptual": "pale dashed · conceptual lifecycle",
            },
            {copy_id: self.master["copy"][copy_id]["text"] for copy_id in legend_ids},
        )
        self.assertEqual(
            {
                "energized": "energized or operating lifecycle",
                "permitted": "permitted lifecycle",
                "future_design": "future-design lifecycle",
                "conceptual": "conceptual teaching lifecycle",
            },
            {
                style_id: self.master["status_styles"][style_id]["meaning"]
                for style_id in (
                    "energized",
                    "permitted",
                    "future_design",
                    "conceptual",
                )
            },
        )

        annotation = visual["annotation"]
        self.assertEqual("Four independent visual channels", annotation["title"])
        self.assertEqual(
            [
                "COLOR = carrier, independent of lifecycle",
                "DIRECTION = initial 138 kV tie → initial 200 MW / 138 kV station",
                "STROKE = energized, permitted, future-design, or conceptual lifecycle",
                "POSTURE = claim copy / evidence drawer, not stroke",
            ],
            [item["label"] for item in annotation["items"]],
        )
        self.assertEqual(
            [
                ["energized_example", "permitted_example", "selected_design_example"],
                ["energized_example"],
                [
                    "energized_example",
                    "permitted_example",
                    "future_example",
                    "unknown_example",
                    "selected_design_example",
                ],
                [
                    "energized_example",
                    "permitted_example",
                    "future_example",
                    "unknown_example",
                    "selected_design_example",
                ],
            ],
            [item["claim_ids"] for item in annotation["items"]],
        )
        claim_ids = {
            claim["id"]
            for claim in segment_by_id(self.course, "p1_read_the_machine")["evidence"][
                "claims"
            ]
        }
        self.assertTrue(
            all(
                item["claim_ids"] and set(item["claim_ids"]) <= claim_ids
                for item in annotation["items"]
            )
        )

    def test_thermal_to_schedule_handoff_names_scale_and_domain_change(self) -> None:
        cue = segment_by_id(self.course, "s16_close_atmosphere")["transition"]["cue"]
        self.assertEqual(
            "Zoom out from the thermal-return subsystem, then switch to the "
            "grid-interconnection schedule.",
            cue,
        )

    def test_measured_water_unknown_cannot_be_coordinately_promoted(self) -> None:
        course = deepcopy(self.course)
        ledgers = deepcopy(self.ledgers)
        fact = ledgers["abilene"]["facts"][
            "cooling_measured_operating_consumption_gallons"
        ]
        fact["value"] = 0
        fact["posture"] = "confirmed"
        fact["lifecycle"] = "operating"
        claim = next(
            claim
            for claim in segment_by_id(course, "s15_water_accounting")["evidence"][
                "claims"
            ]
            if claim["id"] == "measured_operating_consumption_unknown"
        )
        claim["assertion"] = "confirmed"
        self.assertFalse(validate._claim_assertion_matches("explicit_unknown", fact))
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable fact semantic contract|"
            "cooling_measured_operating_consumption_gallons must remain null",
        ):
            validate._validate_evidence(ledgers["abilene"])

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
        with self.assertRaisesRegex(
            validate.ValidationError, "not bound to selected topology"
        ):
            self.validate(course)

    def test_claim_assertion_cannot_promote_permit_evidence(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s01_fire_to_electricity")["evidence"]["claims"][0][
            "assertion"
        ] = "confirmed"
        with self.assertRaisesRegex(
            validate.ValidationError, "cannot support assertion"
        ):
            self.validate(course)

    def test_s01_permit_annotation_matches_bound_nameplate_evidence(self) -> None:
        segment = segment_by_id(self.course, "s01_fire_to_electricity")
        claim = next(
            claim
            for claim in segment["evidence"]["claims"]
            if claim["id"] == "gas_authorization"
        )
        facts = {
            fact_id: self.ledgers[ledger_id]["facts"][fact_id]
            for ref in claim["fact_refs"]
            for ledger_id, fact_id in [ref.split(":", 1)]
        }
        annotation_item = next(
            item
            for item in self.visuals["segments"][segment["id"]]["annotation"]["items"]
            if claim["id"] in item["claim_ids"]
        )

        self.assertEqual(10, facts["gas_turbine_units_authorized"]["value"])
        self.assertEqual(360.5, facts["gas_permitted_nameplate_mw"]["value"])
        self.assertEqual("permitted", claim["assertion"])
        self.assertEqual(
            {"permitted_not_observed"},
            {fact["posture"] for fact in facts.values()},
        )
        self.assertIn("Ten units", annotation_item["label"])
        self.assertIn("360.5 MW", annotation_item["label"])
        self.assertIn("permit scope", annotation_item["label"])
        self.assertNotIn("installed", annotation_item["label"].lower())
        self.assertNotIn("operating", annotation_item["label"].lower())

    def test_s01_conversion_objective_is_in_focus(self) -> None:
        segment = segment_by_id(self.course, "s01_fire_to_electricity")
        visual = self.visuals["segments"][segment["id"]]
        claims = {claim["id"]: claim for claim in segment["evidence"]["claims"]}

        self.assertEqual(
            ["gas_turbine", "generator", "gsu_transformer"],
            segment["node_ids"],
        )
        self.assertEqual(
            ["btm_fuel_to_shaft", "btm_terminal_to_gsu"],
            segment["edge_ids"],
        )
        self.assertEqual(segment["node_ids"], visual["label_node_ids"])
        conversion = visual["annotation"]["items"][0]
        self.assertEqual(
            "Generic conversion: combustion gas → shaft → "
            "generator-terminal electricity",
            conversion["label"],
        )
        self.assertEqual(
            ["turbine_generator_conversion_reference"],
            conversion["claim_ids"],
        )
        self.assertEqual(
            [
                "electrical_engineering:turbine_fluid_to_rotor_conversion",
                "electrical_engineering:generator_rotor_to_electricity_conversion",
            ],
            claims["turbine_generator_conversion_reference"]["fact_refs"],
        )
        self.assertEqual(
            "explicit_unknown",
            claims["installed_turbine_configuration_unknown"]["assertion"],
        )
        self.assertEqual(
            "explicit_unknown",
            claims["operating_posture_unknown"]["assertion"],
        )
        self.assertEqual(
            {
                "gas_authorization",
                "installed_turbine_presence",
                "installed_turbine_configuration_unknown",
                "operating_posture_unknown",
                "turbine_generator_conversion_reference",
            },
            {
                claim_id
                for item in visual["annotation"]["items"]
                for claim_id in item["claim_ids"]
            },
        )

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
        self.assertFalse(
            validate._claim_assertion_matches(
                "contract_reference",
                ledgers["commercial_energy"]["facts"]["crane_microsoft_ppa_contract"],
            )
        )
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable fact semantic contract|cannot support assertion",
        ):
            self.validate(ledgers=ledgers)

    def test_derived_scenarios_are_not_promoted_to_published_methods(self) -> None:
        claims = segment_by_id(self.course, "s24_megawatts_to_tokens")["evidence"][
            "claims"
        ]
        by_id = {claim["id"]: claim for claim in claims}
        self.assertEqual(
            "method_reference", by_id["pue_accounting_boundary"]["assertion"]
        )
        self.assertEqual(
            "derived_scenario_reference",
            by_id["complete_scenario_recipe"]["assertion"],
        )

        course = deepcopy(self.course)
        mutable_claims = segment_by_id(course, "s24_megawatts_to_tokens")["evidence"][
            "claims"
        ]
        next(
            claim
            for claim in mutable_claims
            if claim["id"] == "complete_scenario_recipe"
        )["assertion"] = "method_reference"
        with self.assertRaisesRegex(
            validate.ValidationError, "cannot support assertion"
        ):
            self.validate(course=course)

        course = deepcopy(self.course)
        segment_by_id(course, "s24_megawatts_to_tokens")["evidence"][
            "promotion_guards"
        ].remove("energy_power_time_basis")
        with self.assertRaisesRegex(
            validate.ValidationError, "missing assertion promotion guards"
        ):
            self.validate(course=course)

    def test_s24_annotation_separates_dimensional_routes_from_workloads(self) -> None:
        items = self.visuals["segments"]["s24_megawatts_to_tokens"]["annotation"][
            "items"
        ]
        inference_rate, energy_yield, training_rate, stop_rule = items

        self.assertEqual(
            "Inference rate: W_facility×W_IT/W_facility×W_accel/W_IT×tokens/J=tokens/s",
            inference_rate["label"],
        )
        self.assertEqual(
            [
                "facility_to_it_scenario_step",
                "inference_published_boundaries",
                "inference_scenario_step",
                "complete_scenario_recipe",
            ],
            inference_rate["claim_ids"],
        )
        self.assertEqual(
            "Energy yield: J_facility×J_IT/J_facility×J_accel/J_IT×tokens/J=tokens",
            energy_yield["label"],
        )
        self.assertEqual(
            [
                "pue_accounting_boundary",
                "facility_to_it_scenario_step",
                "inference_scenario_step",
                "complete_scenario_recipe",
            ],
            energy_yield["claim_ids"],
        )
        self.assertEqual(
            "Training: active peak matmul FLOP/s × same-system measured MFU ÷ "
            "model FLOP/token = tokens/s",
            training_rate["label"],
        )
        self.assertEqual(
            [
                "training_published_method",
                "training_scenario_step",
                "complete_scenario_recipe",
            ],
            training_rate["claim_ids"],
        )
        self.assertEqual(
            "Missing site input means no Abilene estimate",
            stop_rule["label"],
        )
        self.assertEqual(
            "Scenario unit cancellation; no Abilene values",
            self.visuals["segments"]["s24_megawatts_to_tokens"]["annotation"]["title"],
        )
        self.assertTrue(all(len(item["label"]) <= 96 for item in items))

    def test_s17_framing_starts_at_planned_public_boundary(self) -> None:
        segment = segment_by_id(self.course, "s17_interconnection_schedule")
        annotation = self.visuals["segments"][segment["id"]]["annotation"]
        claims = {claim["id"]: claim for claim in segment["evidence"]["claims"]}

        self.assertEqual(
            "Planned capacity becomes a utility delivery schedule",
            segment["title"],
        )
        self.assertEqual(
            "Which utility construction, energization, and equipment gates stand "
            "between planned capacity and service?",
            segment["opening_question"],
        )
        self.assertEqual(
            "Separate dated administrative, energization, and planned "
            "permanent-equipment gates.",
            segment["learning_objective"],
        )
        self.assertNotIn("queue", segment["title"].lower())
        self.assertNotIn("request", segment["opening_question"].lower())
        self.assertEqual(
            [
                {
                    "label": "PLANNED — 1.2 GW grid-interconnection boundary",
                    "claim_ids": ["planned_grid_boundary"],
                },
                {
                    "label": "CONFIRMED — initial utility gates energized 2023-06-30",
                    "claim_ids": ["initial_aep_delivery_gates"],
                },
                {
                    "label": (
                        "REPORTED — line schedule 2025-05-12→2025-11-21; "
                        "completion/energization unestablished"
                    ),
                    "claim_ids": ["expansion_line_schedule"],
                },
                {
                    "label": (
                        "PLANNED — permanent-transformer swaps expected by 2026-10-31"
                    ),
                    "claim_ids": ["expansion_permanent_transformer_schedule"],
                },
                {
                    "label": (
                        "UNKNOWN — customer queue/service agreement/capacity/load-ramp "
                        "administrative record"
                    ),
                    "claim_ids": ["private_interconnection_and_load_boundary"],
                },
            ],
            annotation["items"],
        )
        self.assertTrue(all(len(item["label"]) <= 96 for item in annotation["items"]))
        execution_facts = self.ledgers["abilene_execution"]["facts"]
        self.assertEqual(
            "2023-06-30",
            execution_facts["initial_aep_terminal_energized_date"]["value"],
        )
        self.assertEqual(
            "2023-06-30", execution_facts["initial_aep_poi_energized_date"]["value"]
        )
        self.assertEqual(
            "2025-05-12",
            execution_facts["expansion_345_line_start_date_as_reported"]["value"],
        )
        self.assertEqual(
            "2025-11-21",
            execution_facts["expansion_345_line_finish_date_as_reported"]["value"],
        )
        self.assertEqual(
            "2026-10-31",
            execution_facts["expansion_permanent_transformer_swaps_expected_by"][
                "value"
            ],
        )
        private_claim = claims["private_interconnection_and_load_boundary"]
        self.assertEqual("explicit_unknown", private_claim["assertion"])
        self.assertEqual(
            [
                "abilene_execution:site_specific_interconnection_queue_and_contract_record",
                "abilene_execution:contracted_grid_service_capacity_mw",
                "abilene_execution:current_total_facility_load_mw",
                "abilene_execution:current_critical_it_load_mw",
            ],
            private_claim["fact_refs"],
        )
        self.assertTrue(
            all(
                self.ledgers[ledger_id]["facts"][fact_id]["value"] is None
                for ref in private_claim["fact_refs"]
                for ledger_id, fact_id in [ref.split(":", 1)]
            )
        )
        self.assertEqual(
            {"unverified_null"},
            {
                self.ledgers[ledger_id]["facts"][fact_id]["posture"]
                for ref in private_claim["fact_refs"]
                for ledger_id, fact_id in [ref.split(":", 1)]
            },
        )

    def test_s18_s19_handoff_shows_scoped_time_examples(self) -> None:
        s18 = segment_by_id(self.course, "s18_long_lead_equipment")
        s19 = segment_by_id(self.course, "s19_fast_load_slow_grid")
        s18_items = self.visuals["segments"][s18["id"]]["annotation"]["items"]
        s19_item = self.visuals["segments"][s19["id"]]["annotation"]["items"][0]

        self.assertEqual(
            "Contrast scoped 36+ month equipment exposure with ~250 ms / <1 s "
            "external load behavior.",
            s18["transition"]["cue"],
        )
        self.assertEqual(
            {
                "label": (
                    "U.S. LPT market example: up to/over 36 months; not an "
                    "Abilene schedule"
                ),
                "claim_ids": ["transformer_delivery_exposure"],
            },
            s18_items[0],
        )
        self.assertEqual(
            {
                "label": (
                    "External GE portfolio: ~10 GW available for 2029 delivery; "
                    "not an Abilene schedule"
                ),
                "claim_ids": ["turbine_manufacturing_slot"],
            },
            s18_items[1],
        )
        self.assertEqual(
            {
                "label": (
                    "External cooling: XCA first shipped 2026-06; generic acceptance "
                    "sequence; not Abilene"
                ),
                "claim_ids": [
                    "cooling_product_availability_example",
                    "liquid_cooling_acceptance",
                ],
            },
            s18_items[2],
        )
        self.assertTrue(all(len(item["label"]) <= 96 for item in s18_items))
        self.assertEqual(
            {
                "label": (
                    "External NERC example: ~250 ms fastest ramp; transitions "
                    "<1 s; not Abilene"
                ),
                "claim_ids": ["synchronized_ai_load_dynamics"],
            },
            s19_item,
        )
        s18_claims = {claim["id"]: claim for claim in s18["evidence"]["claims"]}
        s19_claims = {claim["id"]: claim for claim in s19["evidence"]["claims"]}
        self.assertIn(
            "delivery_resilience:us_large_power_transformer_lead_time_2024",
            s18_claims["transformer_delivery_exposure"]["fact_refs"],
        )
        self.assertIn(
            "delivery_resilience:ge_gas_turbine_delivery_slot_exposure_2025",
            s18_claims["turbine_manufacturing_slot"]["fact_refs"],
        )
        self.assertIn(
            "delivery_resilience:uniflair_xca_initial_shipping_date",
            s18_claims["cooling_product_availability_example"]["fact_refs"],
        )
        self.assertTrue(
            {
                "delivery_resilience:ai_training_checkpoint_transition_duration",
                "delivery_resilience:ai_training_observed_ramp_rate",
            }
            <= set(s19_claims["synchronized_ai_load_dynamics"]["fact_refs"])
        )

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
        segment_by_id(course, "s05_ppa_not_wire")["evidence"][
            "promotion_guards"
        ].remove("contractual_to_physical")
        with self.assertRaisesRegex(
            validate.ValidationError, "missing assertion promotion guards"
        ):
            self.validate(course=course)

        ledgers = deepcopy(self.ledgers)
        ledgers["commercial_energy"]["facts"][
            "scope2_contractual_attributes_not_physical_flow"
        ]["posture"] = "design_not_observed"
        self.assertFalse(
            validate._claim_assertion_matches(
                "accounting_reference",
                ledgers["commercial_energy"]["facts"][
                    "scope2_contractual_attributes_not_physical_flow"
                ],
            )
        )
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable fact semantic contract|cannot support assertion",
        ):
            self.validate(ledgers=ledgers)

    def test_research_gate_and_schema_fail_closed(self) -> None:
        course = deepcopy(self.course)
        evidence = segment_by_id(course, "s17_interconnection_schedule")["evidence"]
        evidence["readiness"] = "research_required"
        evidence["blocking_research"] = []
        with self.assertRaisesRegex(
            validate.ValidationError, "needs blocking research"
        ):
            self.validate(course)

        course = deepcopy(self.course)
        segment_by_id(course, "s03_initial_grid_path")["evidence"]["claims"][0][
            "source_ids"
        ] = ["mortenson_abilene_power_delivery"]
        with self.assertRaisesRegex(
            validate.ValidationError, r"extra=\['source_ids'\]"
        ):
            self.validate(course)

    def test_dependencies_cannot_promote_a_summary(self) -> None:
        course = deepcopy(self.course)
        dependency = segment_by_id(course, "s12_cdu_boundary")["evidence"]
        dependency["readiness"] = "research_required"
        dependency["blocking_research"] = ["A new primary-source package is required."]
        with self.assertRaisesRegex(
            validate.ValidationError, "cannot depend on research-gated"
        ):
            self.validate(course)

    def test_hidden_overlays_require_exact_reveal_intent(self) -> None:
        course = deepcopy(self.course)
        segment_by_id(course, "s05_ppa_not_wire")["camera"]["reveal_ids"] = []
        with self.assertRaisesRegex(
            validate.ValidationError, "reveal_ids must exactly match"
        ):
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
            "s23_business_models",
        ):
            camera = segment_by_id(self.course, segment_id)["camera"]
            self.assertEqual(["nuclear_variant"], camera["reveal_copy_ids"])
        s21_camera = segment_by_id(self.course, "s21_capital_ownership")["camera"]
        self.assertEqual([], s21_camera["reveal_ids"])
        self.assertEqual([], s21_camera["reveal_copy_ids"])

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
        with self.assertRaisesRegex(
            validate.ValidationError, "missing assertion promotion guards"
        ):
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
        with self.assertRaisesRegex(
            validate.ValidationError, "not bound to selected topology"
        ):
            self.validate(course)

    def test_overlay_cannot_bypass_master_topology(self) -> None:
        course = deepcopy(self.course)
        claim = segment_by_id(course, "s03_initial_grid_path")["evidence"]["claims"][0]
        claim["binding"] = "overlay"
        with self.assertRaisesRegex(
            validate.ValidationError, "cannot bypass master topology"
        ):
            self.validate(course)

    def test_campus_mv_scope_does_not_rebind_gas_authorization(self) -> None:
        claim_ids = {
            claim["id"]
            for claim in segment_by_id(self.course, "s06_campus_mv_envelope")[
                "evidence"
            ]["claims"]
        }
        self.assertNotIn("gas_authorization", claim_ids)

    def test_overlay_ledger_must_match_the_act_scope(self) -> None:
        course = deepcopy(self.course)
        source_claim = deepcopy(
            segment_by_id(course, "s23_business_models")["evidence"]["claims"][0]
        )
        source_claim["id"] = "unrelated_commercial_overlay"
        target = segment_by_id(course, "s10_two_rack_heat_paths")
        target["evidence"]["claims"].append(source_claim)
        for guard in ("contractual_to_physical", "site_scope_transfer"):
            if guard not in target["evidence"]["promotion_guards"]:
                target["evidence"]["promotion_guards"].append(guard)
        with self.assertRaisesRegex(validate.ValidationError, "outside act scope"):
            self.validate(course)

    def test_qualified_refs_support_multiple_ledgers_without_collision(self) -> None:
        course = deepcopy(self.course)
        target = segment_by_id(course, "s02_generator_terminal")
        synthetic_claim = {
            "id": "execution_site_voltage_unknown",
            "assertion": "explicit_unknown",
            "binding": "overlay",
            "fact_refs": ["abilene_execution:generator_terminal_site_voltage_kv"],
        }
        target["evidence"]["claims"].append(synthetic_claim)
        extended_claim_contract = MappingProxyType(
            {
                **validate.COURSE_CLAIM_CONTRACT,
                (target["id"], synthetic_claim["id"]): validate._claim_payload_digest(
                    synthetic_claim
                ),
            }
        )
        with patch.object(
            validate,
            "COURSE_CLAIM_CONTRACT",
            extended_claim_contract,
        ):
            self.validate(course)

            course = deepcopy(course)
            segment_by_id(course, "s02_generator_terminal")["evidence"]["claims"][-1][
                "binding"
            ] = "topology"
            with self.assertRaisesRegex(
                validate.ValidationError, "not bound to selected topology"
            ):
                self.validate(course)

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
        claim = segment_by_id(course, "p0_gigawatt_not_workload")["evidence"]["claims"][
            0
        ]
        claim["fact_refs"] = ["unqualified_fact"]
        with self.assertRaisesRegex(validate.ValidationError, "malformed qualified"):
            self.validate(course)

    def test_lifecycle_and_no_estimate_assertions_fail_closed(self) -> None:
        ledgers = deepcopy(self.ledgers)
        ledgers["abilene"]["facts"]["buildings_energized_confirmed_min"][
            "lifecycle"
        ] = "planned"
        self.assertFalse(
            validate._claim_assertion_matches(
                "confirmed_minimum",
                ledgers["abilene"]["facts"]["buildings_energized_confirmed_min"],
            )
        )
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable fact semantic contract|cannot support assertion",
        ):
            self.validate(ledgers=ledgers)

        ledgers = deepcopy(self.ledgers)
        ledgers["abilene"]["facts"]["installed_gpu_count"]["basis"] = "unknown"
        self.assertFalse(
            validate._claim_assertion_matches(
                "no_evidence_backed_estimate",
                ledgers["abilene"]["facts"]["installed_gpu_count"],
            )
        )
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable fact payload contract|cannot support assertion",
        ):
            self.validate(ledgers=ledgers)

    def test_non_finite_weights_fail(self) -> None:
        course = deepcopy(self.course)
        course["meta"]["relative_weight_total"] = float("nan")
        segment_by_id(course, "p0_gigawatt_not_workload")["weight"] = float("nan")
        with self.assertRaisesRegex(validate.ValidationError, "finite"):
            self.validate(course)


if __name__ == "__main__":
    unittest.main()
