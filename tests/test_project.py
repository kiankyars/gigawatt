from __future__ import annotations

import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory

from gigawatt import layout, validate


class EvidencePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = validate._load_yaml_strict(validate.EVIDENCE)
        validate._validate_evidence(cls.evidence)

    def test_duplicate_yaml_keys_fail_preflight(self) -> None:
        with TemporaryDirectory(prefix="gigawatt-duplicate-yaml-") as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("facts:\n  repeated: 1\n  repeated: 2\n")
            with self.assertRaisesRegex(validate.ValidationError, "duplicate YAML key 'repeated'"):
                validate._load_yaml_strict(path)

    def test_installed_gpu_count_fails_closed(self) -> None:
        fact = self.evidence["facts"]["installed_gpu_count"]
        self.assertIsNone(fact["value"])
        self.assertEqual("no evidence-backed estimate", fact["basis"])

    def test_operating_and_design_rack_platforms_are_separate(self) -> None:
        facts = self.evidence["facts"]
        operating = facts["rack_platform"]
        design = facts["rack_platform_nvl72_design_reference"]
        self.assertEqual("NVIDIA GB200", operating["value"])
        self.assertEqual("deployed", operating["lifecycle"])
        self.assertEqual("NVIDIA GB200 NVL72", design["value"])
        self.assertEqual("design_reference", design["lifecycle"])
        self.assertEqual("design_not_observed", design["posture"])

    def test_cooling_values_remain_design_or_anticipated(self) -> None:
        facts = self.evidence["facts"]
        self.assertEqual("selected_design", facts["cooling_heat_rejection_posture"]["lifecycle"])
        self.assertNotIn("direct-to-chip", facts["cooling_heat_rejection_posture"]["basis"])
        self.assertEqual("design_reference", facts["cooling_direct_to_chip_design"]["lifecycle"])
        self.assertEqual(
            "anticipated_not_observed",
            facts["cooling_annual_maintenance_gallons_per_building"]["posture"],
        )

    def test_design_product_null_and_permit_facts_cannot_be_promoted(self) -> None:
        facts = self.evidence["facts"]
        cases = {
            "thermal design": "cooling_direct_to_chip_design",
            "rack product": "rack_power_shelf_output_vdc",
            "rack air product": "rack_air_cooled_components",
            "rack liquid product": "rack_liquid_cooled_components",
            "campus MV null": "campus_lpt_secondary_as_built_voltage_kv",
            "gas permit": "gas_permitted_nameplate_mw",
            "diesel permit": "diesel_permitted_nameplate_mw",
        }
        for label, fact_id in cases.items():
            fact = facts[fact_id]
            record = {
                "id": f"promotion_probe_{fact_id}",
                "lifecycle": "operational_confirmed",
                "fact_ids": [fact_id],
                "source_ids": list(fact["source_ids"]),
            }
            with self.subTest(label=label), self.assertRaisesRegex(
                validate.ValidationError, "cannot support"
            ):
                validate._validate_fact_binding(record, facts, "probe")

    def test_master_sources_must_equal_referenced_fact_sources(self) -> None:
        facts = self.evidence["facts"]
        record = {
            "id": "source_mismatch_probe",
            "lifecycle": "conceptual",
            "fact_ids": ["rack_air_cooled_components"],
            "source_ids": [],
        }
        with self.assertRaisesRegex(validate.ValidationError, "source_ids must equal fact source union"):
            validate._validate_fact_binding(record, facts, "probe")


class ProjectContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = validate.validate_project()
        cls.master = layout.load_yaml(validate.DIAGRAM / "master.yaml")
        cls.evidence = layout.load_yaml(validate.EVIDENCE)

    def test_full_contract(self) -> None:
        self.assertEqual(7, self.result["evidence_ledgers"])
        self.assertEqual(71, self.result["sources"])
        self.assertEqual(183, self.result["facts"])
        self.assertEqual(30, self.result["nodes"])
        self.assertEqual(34, self.result["edges"])
        self.assertEqual(6, self.result["cameras"])

    def test_every_master_record_has_evidence_bindings(self) -> None:
        for location in ("nodes", "edges"):
            for record in self.master[location]:
                self.assertIn("fact_ids", record)
                self.assertIsInstance(record["fact_ids"], list)

    def test_permits_do_not_become_operations(self) -> None:
        nodes = {node["id"]: node for node in self.master["nodes"]}
        facts = self.evidence["facts"]
        self.assertEqual("permitted", nodes["gas_turbine"]["lifecycle"])
        self.assertEqual("permitted", nodes["diesel_backup_package"]["lifecycle"])
        self.assertIsNone(facts["gas_commissioned_mw"]["value"])
        self.assertIsNone(facts["diesel_units_installed"]["value"])
        self.assertIsNone(facts["campus_source_merge_as_built_topology"]["value"])
        self.assertIsNone(facts["bess_campus_connection_as_built_topology"]["value"])
        self.assertIsNone(facts["diesel_campus_connection_as_built_topology"]["value"])

    def test_thermal_fill_is_not_heat_rejection_makeup(self) -> None:
        edges = {edge["id"]: edge for edge in self.master["edges"]}
        self.assertEqual("facility_loop", edges["fill_to_facility_loop"]["to"])
        self.assertEqual("air_cooled_chiller", edges["chiller_to_atmosphere"]["from"])
        self.assertEqual("atmosphere", edges["chiller_to_atmosphere"]["to"])

    def test_hidden_copy_requires_a_hidden_reveal_owner(self) -> None:
        master = deepcopy(self.master)
        nuclear_ppa = next(node for node in master["nodes"] if node["id"] == "nuclear_ppa")
        del nuclear_ppa["reveal_copy_ids"]
        source_ids, _ = validate._validate_evidence(self.evidence)
        with self.assertRaisesRegex(validate.ValidationError, "hidden master copy requires"):
            validate._validate_master(master, self.evidence, source_ids)


if __name__ == "__main__":
    unittest.main()
