from __future__ import annotations

import math
import unittest
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from gigawatt import generated_artifacts, layout, validate


class EvidencePolicyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.evidence = validate._load_yaml_strict(validate.EVIDENCE)
        validate._validate_evidence(cls.evidence)

    def test_duplicate_yaml_keys_fail_preflight(self) -> None:
        with TemporaryDirectory(prefix="gigawatt-duplicate-yaml-") as directory:
            path = Path(directory) / "duplicate.yaml"
            path.write_text("facts:\n  repeated: 1\n  repeated: 2\n")
            with self.assertRaisesRegex(
                validate.ValidationError, "duplicate YAML key 'repeated'"
            ):
                validate._load_yaml_strict(path)

    def test_evidence_schema_rejects_unexpected_fields_at_every_level(self) -> None:
        source_id = next(iter(self.evidence["sources"]))
        fact_id = next(iter(self.evidence["facts"]))
        mutations = (
            ("root", lambda ledger: ledger.__setitem__("unexpected", True)),
            (
                "subject",
                lambda ledger: ledger["subject"].__setitem__("unexpected", True),
            ),
            (
                "evidence boundary",
                lambda ledger: ledger["evidence_boundary"].__setitem__(
                    "unexpected", True
                ),
            ),
            (
                "source",
                lambda ledger: ledger["sources"][source_id].__setitem__(
                    "unexpected", True
                ),
            ),
            (
                "fact",
                lambda ledger: ledger["facts"][fact_id].__setitem__("unexpected", True),
            ),
        )
        for level, mutate in mutations:
            ledger = deepcopy(self.evidence)
            mutate(ledger)
            with (
                self.subTest(level=level),
                self.assertRaisesRegex(validate.ValidationError, "extra=.*unexpected"),
            ):
                validate._validate_evidence_schema(ledger)

    def test_evidence_schema_rejects_missing_fields_at_every_level(self) -> None:
        source_id = next(iter(self.evidence["sources"]))
        fact_id = next(iter(self.evidence["facts"]))
        mutations = (
            ("root", lambda ledger: ledger.pop("evidence_boundary")),
            ("subject", lambda ledger: ledger["subject"].pop("id")),
            (
                "evidence boundary",
                lambda ledger: ledger["evidence_boundary"].pop("included_scope"),
            ),
            ("source", lambda ledger: ledger["sources"][source_id].pop("date_note")),
            ("fact", lambda ledger: ledger["facts"][fact_id].pop("unit")),
        )
        for level, mutate in mutations:
            ledger = deepcopy(self.evidence)
            mutate(ledger)
            with (
                self.subTest(level=level),
                self.assertRaisesRegex(validate.ValidationError, "missing="),
            ):
                validate._validate_evidence_schema(ledger)

    def test_evidence_schema_rejects_material_nested_type_mutations(self) -> None:
        source_id = next(iter(self.evidence["sources"]))
        fact_id = next(iter(self.evidence["facts"]))
        mutations = (
            (
                "source publisher",
                lambda ledger: ledger["sources"][source_id].__setitem__(
                    "publisher", {"name": "not scalar"}
                ),
                r"publisher: expected a non-empty string",
            ),
            (
                "mapping fact value",
                lambda ledger: ledger["facts"][fact_id].__setitem__(
                    "value", {"nested": "not scalar"}
                ),
                r"value: expected a scalar",
            ),
            (
                "subject value",
                lambda ledger: ledger["subject"].__setitem__("canonical_name", []),
                r"subject\.canonical_name: expected a non-empty string",
            ),
            (
                "evidence boundary value",
                lambda ledger: ledger["evidence_boundary"].__setitem__(
                    "included_scope", ["not scalar"]
                ),
                r"evidence_boundary\.included_scope: expected a non-empty string",
            ),
        )
        for field, mutate, message in mutations:
            ledger = deepcopy(self.evidence)
            mutate(ledger)
            with (
                self.subTest(field=field),
                self.assertRaisesRegex(validate.ValidationError, message),
            ):
                validate._validate_evidence_schema(ledger)

    def test_evidence_schema_version_requires_an_exact_integer(self) -> None:
        for invalid in (True, 1.0, "1"):
            ledger = deepcopy(self.evidence)
            ledger["schema_version"] = invalid
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(
                    validate.ValidationError, "schema_version must be 1"
                ),
            ):
                validate._validate_evidence_schema(ledger)

    def test_fact_unit_value_kind_contract_is_closed_and_exact(self) -> None:
        mutations = (
            (
                "numeric boolean",
                "gas_turbine_units_authorized",
                "value",
                True,
                "requires a finite number",
            ),
            (
                "numeric text",
                "gas_turbine_units_authorized",
                "value",
                "10",
                "requires a finite number",
            ),
            (
                "boolean integer",
                "adjacent_microsoft_scope_included",
                "value",
                0,
                "requires a boolean",
            ),
            (
                "text number",
                "rack_platform",
                "value",
                1,
                "requires a non-empty string",
            ),
            (
                "unknown unit",
                "rack_platform",
                "unit",
                "unclassified unit",
                "unknown fact unit",
            ),
        )
        for label, fact_id, field, value, message in mutations:
            ledger = deepcopy(self.evidence)
            ledger["facts"][fact_id][field] = value
            with (
                self.subTest(label=label),
                self.assertRaisesRegex(validate.ValidationError, message),
            ):
                validate._validate_evidence_schema(ledger, ledger_id="abilene")

    def test_immutable_ledger_context_contract_is_exact_and_complete(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        registered_contexts = {
            ledger_id: validate._ledger_context_digest(ledger)
            for ledger_id, ledger in ledgers.items()
        }
        self.assertEqual(7, len(validate.LEDGER_CONTEXT_CONTRACT))
        self.assertEqual(dict(validate.LEDGER_CONTEXT_CONTRACT), registered_contexts)
        with self.assertRaises(TypeError):
            validate.LEDGER_CONTEXT_CONTRACT["unexpected"] = "0" * 64

        missing = deepcopy(ledgers)
        missing.pop("thermal_engineering")
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable ledger context contract ledger mismatch: missing=",
        ):
            validate._validate_registered_ledger_context_contract(missing)

        extra = deepcopy(ledgers)
        extra["unexpected"] = deepcopy(extra["thermal_engineering"])
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable ledger context contract ledger mismatch: .*extra=",
        ):
            validate._validate_registered_ledger_context_contract(extra)

    def test_ledger_context_contract_rejects_every_root_leaf_mutation(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        mutation_count = 0

        for ledger_id, original in ledgers.items():
            schema_mutation = deepcopy(original)
            schema_mutation["schema_version"] = 2
            with (
                self.subTest(ledger_id=ledger_id, field="schema_version"),
                self.assertRaisesRegex(
                    validate.ValidationError, "schema_version must be 1"
                ),
            ):
                validate._validate_evidence_schema(schema_mutation, ledger_id=ledger_id)
            mutation_count += 1

            for field in sorted(original["subject"]):
                subject_mutation = deepcopy(original)
                subject_mutation["subject"][field] += " altered"
                with (
                    self.subTest(ledger_id=ledger_id, field=f"subject.{field}"),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable ledger context contract requires exact",
                    ),
                ):
                    validate._validate_evidence_schema(
                        subject_mutation, ledger_id=ledger_id
                    )
                mutation_count += 1

            accessed_mutation = deepcopy(original)
            accessed_mutation["accessed_as_of"] += " altered"
            with (
                self.subTest(ledger_id=ledger_id, field="accessed_as_of"),
                self.assertRaisesRegex(
                    validate.ValidationError,
                    "immutable ledger context contract requires exact",
                ),
            ):
                validate._validate_evidence_schema(
                    accessed_mutation, ledger_id=ledger_id
                )
            mutation_count += 1

            for field in sorted(original["evidence_boundary"]):
                boundary_mutation = deepcopy(original)
                boundary_mutation["evidence_boundary"][field] += " altered"
                with (
                    self.subTest(
                        ledger_id=ledger_id, field=f"evidence_boundary.{field}"
                    ),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable ledger context contract requires exact",
                    ),
                ):
                    validate._validate_evidence_schema(
                        boundary_mutation, ledger_id=ledger_id
                    )
                mutation_count += 1

        self.assertEqual(55, mutation_count)

    def test_immutable_fact_identity_contract_is_exact_and_complete(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        registered_ids = {
            f"{ledger_id}:{fact_id}"
            for ledger_id, ledger in ledgers.items()
            for fact_id in ledger["facts"]
        }
        self.assertEqual(184, len(validate.FACT_IDENTITY_CONTRACT))
        self.assertEqual(set(validate.FACT_IDENTITY_CONTRACT), registered_ids)
        with self.assertRaises(TypeError):
            validate.FACT_IDENTITY_CONTRACT["unexpected:fact"] = (None, "text")

    def test_immutable_fact_identity_contract_rejects_missing_and_extra_ids(
        self,
    ) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)

        missing = deepcopy(ledgers)
        missing["abilene"]["facts"].pop("installed_gpu_count")
        with self.assertRaisesRegex(
            validate.ValidationError,
            r"immutable registered fact identity contract mismatch: missing=.*installed_gpu_count",
        ):
            validate._validate_registered_fact_identity_contract(missing)

        extra = deepcopy(ledgers)
        extra["abilene"]["facts"]["unexpected_identity"] = deepcopy(
            extra["abilene"]["facts"]["installed_gpu_count"]
        )
        with self.assertRaisesRegex(
            validate.ValidationError,
            r"immutable registered fact identity contract mismatch: .*extra=.*unexpected_identity",
        ):
            validate._validate_registered_fact_identity_contract(extra)

    def test_immutable_fact_semantic_contract_is_exact_and_complete(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        registered_semantics = {
            f"{ledger_id}:{fact_id}": (
                fact["value"] is None,
                fact["posture"],
                fact["lifecycle"],
            )
            for ledger_id, ledger in ledgers.items()
            for fact_id, fact in ledger["facts"].items()
        }
        self.assertEqual(184, len(validate.FACT_SEMANTIC_CONTRACT))
        self.assertEqual(dict(validate.FACT_SEMANTIC_CONTRACT), registered_semantics)
        with self.assertRaises(TypeError):
            validate.FACT_SEMANTIC_CONTRACT["unexpected:fact"] = (
                True,
                "unverified_null",
                "operation_unknown",
            )

    def test_fact_semantic_contract_rejects_every_coordinated_mutation(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        fabricated_values = {"number": 1, "boolean": True, "text": "fabricated"}
        null_identity_count = 0

        for qualified_id, expected in sorted(validate.FACT_SEMANTIC_CONTRACT.items()):
            ledger_id, fact_id = qualified_id.split(":", 1)
            expected_null, expected_posture, expected_lifecycle = expected
            null_identity_count += expected_null

            posture_mutation = deepcopy(ledgers[ledger_id])
            posture_mutation["facts"][fact_id]["posture"] = (
                "no_evidence_backed_estimate"
                if expected_null and expected_posture == "unverified_null"
                else "unverified_null"
                if expected_null
                else "planned_not_operational"
                if expected_posture == "confirmed"
                else "confirmed"
            )
            with (
                self.subTest(qualified_id=qualified_id, mutation="posture"),
                self.assertRaisesRegex(
                    validate.ValidationError,
                    "immutable fact semantic contract requires",
                ),
            ):
                validate._validate_evidence_schema(
                    posture_mutation, ledger_id=ledger_id
                )

            lifecycle_mutation = deepcopy(ledgers[ledger_id])
            lifecycle_mutation["facts"][fact_id]["lifecycle"] = (
                "topology_unknown"
                if expected_null and expected_lifecycle == "operation_unknown"
                else "operation_unknown"
                if expected_null
                else "planned"
                if expected_lifecycle == "operating"
                else "operating"
            )
            with (
                self.subTest(qualified_id=qualified_id, mutation="lifecycle"),
                self.assertRaisesRegex(
                    validate.ValidationError,
                    "immutable fact semantic contract requires",
                ),
            ):
                validate._validate_evidence_schema(
                    lifecycle_mutation, ledger_id=ledger_id
                )

            coordinated_mutation = deepcopy(ledgers[ledger_id])
            fact = coordinated_mutation["facts"][fact_id]
            if expected_null:
                kind = validate.FACT_IDENTITY_CONTRACT[qualified_id][1]
                fact["value"] = fabricated_values[kind]
                fact["posture"] = "confirmed"
                fact["lifecycle"] = "operating"
            else:
                fact["value"] = None
                fact["posture"] = "unverified_null"
                fact["lifecycle"] = "operation_unknown"
            with (
                self.subTest(qualified_id=qualified_id, mutation="coordinated"),
                self.assertRaisesRegex(
                    validate.ValidationError,
                    "immutable fact semantic contract requires",
                ),
            ):
                validate._validate_evidence_schema(
                    coordinated_mutation, ledger_id=ledger_id
                )

        self.assertEqual(57, null_identity_count)

    def test_immutable_fact_payload_contract_is_exact_and_complete(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        registered_payloads = {
            f"{ledger_id}:{fact_id}": validate._fact_payload_digest(fact)
            for ledger_id, ledger in ledgers.items()
            for fact_id, fact in ledger["facts"].items()
        }
        self.assertEqual(184, len(validate.FACT_PAYLOAD_CONTRACT))
        self.assertEqual(dict(validate.FACT_PAYLOAD_CONTRACT), registered_payloads)
        with self.assertRaises(TypeError):
            validate.FACT_PAYLOAD_CONTRACT["unexpected:fact"] = "0" * 64

    def test_immutable_source_payload_contract_is_exact_and_complete(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        registered_payloads = {
            f"{ledger_id}:{source_id}": validate._source_payload_digest(source)
            for ledger_id, ledger in ledgers.items()
            for source_id, source in ledger["sources"].items()
        }
        self.assertEqual(71, len(validate.SOURCE_PAYLOAD_CONTRACT))
        self.assertEqual(dict(validate.SOURCE_PAYLOAD_CONTRACT), registered_payloads)
        with self.assertRaises(TypeError):
            validate.SOURCE_PAYLOAD_CONTRACT["unexpected:source"] = "0" * 64

        missing = deepcopy(ledgers["abilene"])
        missing["sources"].pop(next(iter(missing["sources"])))
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable source payload contract mismatch.*missing=",
        ):
            validate._validate_ledger_source_payload_contract("abilene", missing)

        extra = deepcopy(ledgers["abilene"])
        extra["sources"]["unexpected_source"] = deepcopy(
            next(iter(extra["sources"].values()))
        )
        with self.assertRaisesRegex(
            validate.ValidationError,
            "immutable source payload contract mismatch.*extra=",
        ):
            validate._validate_ledger_source_payload_contract("abilene", extra)

    def test_source_payload_contract_rejects_every_source_field_mutation(
        self,
    ) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        mutation_count = 0

        for qualified_id in sorted(validate.SOURCE_PAYLOAD_CONTRACT):
            ledger_id, source_id = qualified_id.split(":", 1)
            original = ledgers[ledger_id]["sources"][source_id]
            mutations = {
                "publisher": f"{original['publisher']} altered",
                "title": f"{original['title']} altered",
                "kind": f"{original['kind']}_altered",
                "url": f"{original['url']}#altered",
                "publication_date": (
                    f"{original['publication_date']} altered"
                    if original["publication_date"] is not None
                    else "2026-08-29"
                ),
                "review_date": (
                    f"{original['review_date']} altered"
                    if original["review_date"] is not None
                    else "2026-08-29"
                ),
                "accessed_as_of": f"{original['accessed_as_of']} altered",
                "date_note": f"{original['date_note']} altered",
            }
            self.assertEqual(set(validate.SOURCE_PAYLOAD_FIELDS), set(mutations))
            for field, replacement in mutations.items():
                mutated = deepcopy(ledgers[ledger_id])
                mutated["sources"][source_id][field] = replacement
                with (
                    self.subTest(qualified_id=qualified_id, field=field),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable source payload contract requires exact",
                    ),
                ):
                    validate._validate_evidence_schema(mutated, ledger_id=ledger_id)
                mutation_count += 1

        self.assertEqual(568, mutation_count)

    def test_fact_payload_contract_rejects_every_material_field_mutation(
        self,
    ) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        populated_value_mutations = 0
        protected_field_mutations = 0

        for qualified_id in sorted(validate.FACT_PAYLOAD_CONTRACT):
            ledger_id, fact_id = qualified_id.split(":", 1)
            original = ledgers[ledger_id]["facts"][fact_id]
            source_ids = list(ledgers[ledger_id]["sources"])
            material_mutations = {
                "scope": f"{original['scope']} altered",
                "basis": f"{original['basis']} altered",
                "as_of": f"{original['as_of']} altered",
                "source_ids": (
                    list(reversed(original["source_ids"]))
                    if len(original["source_ids"]) > 1
                    else [
                        next(
                            source_id
                            for source_id in source_ids
                            if source_id not in original["source_ids"]
                        )
                    ]
                ),
            }
            if original["value"] is not None:
                kind = validate.FACT_IDENTITY_CONTRACT[qualified_id][1]
                material_mutations["value"] = (
                    original["value"] + 1
                    if kind == "number"
                    else not original["value"]
                    if kind == "boolean"
                    else f"{original['value']} altered"
                )
                populated_value_mutations += 1

            for field, replacement in material_mutations.items():
                mutated = deepcopy(ledgers[ledger_id])
                mutated["facts"][fact_id][field] = replacement
                with (
                    self.subTest(qualified_id=qualified_id, field=field),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable fact payload contract requires exact",
                    ),
                ):
                    validate._validate_evidence_schema(mutated, ledger_id=ledger_id)
                protected_field_mutations += 1

        self.assertEqual(127, populated_value_mutations)
        self.assertEqual(863, protected_field_mutations)

    def test_immutable_course_claim_contract_is_exact_and_complete(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        snapshot = validate._course_claim_contract_snapshot(course)
        self.assertEqual(150, len(validate.COURSE_CLAIM_CONTRACT))
        self.assertEqual(dict(validate.COURSE_CLAIM_CONTRACT), snapshot)
        with self.assertRaises(TypeError):
            validate.COURSE_CLAIM_CONTRACT[("segment", "claim")] = "0" * 64

    def test_course_claim_contract_rejects_exhaustive_schema_compatible_mutations(
        self,
    ) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        claim_locations = [
            (act_index, segment_index, claim_index)
            for act_index, act in enumerate(course["acts"])
            for segment_index, segment in enumerate(act["segments"])
            for claim_index, _ in enumerate(segment["evidence"]["claims"])
        ]
        replacement_fact_ref = "abilene:installed_gpu_count"
        mutation_count = 0

        for act_index, segment_index, claim_index in claim_locations:
            original = course["acts"][act_index]["segments"][segment_index]["evidence"][
                "claims"
            ][claim_index]
            alternatives = {
                "assertion": (
                    "confirmed"
                    if original["assertion"] != "confirmed"
                    else "explicit_unknown"
                ),
                "binding": (
                    "overlay" if original["binding"] == "topology" else "topology"
                ),
                "fact_refs": (
                    list(reversed(original["fact_refs"]))
                    if len(original["fact_refs"]) > 1
                    else [
                        replacement_fact_ref
                        if original["fact_refs"][0] != replacement_fact_ref
                        else "abilene:operational_buildings_exact"
                    ]
                ),
            }
            for field, replacement in alternatives.items():
                mutated = deepcopy(course)
                mutated["acts"][act_index]["segments"][segment_index]["evidence"][
                    "claims"
                ][claim_index][field] = replacement
                with (
                    self.subTest(
                        key=(
                            mutated["acts"][act_index]["segments"][segment_index]["id"],
                            original["id"],
                        ),
                        field=field,
                    ),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable course claim contract mismatch",
                    ),
                ):
                    validate._validate_course_claim_contract(mutated)
                mutation_count += 1

        claim_swap_count = 0
        for act_index, act in enumerate(course["acts"]):
            for segment_index, segment in enumerate(act["segments"]):
                claims = segment["evidence"]["claims"]
                if len(claims) < 2:
                    continue
                mutated = deepcopy(course)
                first, second = mutated["acts"][act_index]["segments"][segment_index][
                    "evidence"
                ]["claims"][:2]
                first_payload = (
                    first["assertion"],
                    first["binding"],
                    first["fact_refs"],
                )
                second_payload = (
                    second["assertion"],
                    second["binding"],
                    second["fact_refs"],
                )
                first["assertion"], first["binding"], first["fact_refs"] = (
                    second_payload
                )
                second["assertion"], second["binding"], second["fact_refs"] = (
                    first_payload
                )
                with (
                    self.subTest(segment_id=segment["id"], mutation="claim_swap"),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable course claim contract mismatch",
                    ),
                ):
                    validate._validate_course_claim_contract(mutated)
                claim_swap_count += 1

        self.assertEqual(450, mutation_count)
        self.assertEqual(26, claim_swap_count)

    def test_reproduced_unknown_claim_promotions_fail_closed(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        master = validate._load_yaml_strict(validate.DIAGRAM / "master.yaml")
        cameras = validate._load_yaml_strict(validate.DIAGRAM / "cameras.yaml")
        ledgers = validate._load_course_evidence_ledgers(course)
        affected_segments = {
            "s01_fire_to_electricity",
            "s02_generator_terminal",
            "s07_building_power_train",
            "s08_rack_voltage_descent",
            "s19_fast_load_slow_grid",
            "s21_capital_ownership",
            "s22_capital_risk",
            "s24_megawatts_to_tokens",
        }
        vulnerable_claims = [
            (act_index, segment_index, claim_index)
            for act_index, act in enumerate(course["acts"])
            for segment_index, segment in enumerate(act["segments"])
            if segment["id"] in affected_segments
            for claim_index, claim in enumerate(segment["evidence"]["claims"])
            if claim["assertion"] in {"explicit_unknown", "no_evidence_backed_estimate"}
        ]
        fabricated_values = {"number": 1, "boolean": True, "text": "fabricated"}

        for act_index, segment_index, claim_index in vulnerable_claims:
            mutated_course = deepcopy(course)
            mutated_ledgers = deepcopy(ledgers)
            segment = mutated_course["acts"][act_index]["segments"][segment_index]
            claim = segment["evidence"]["claims"][claim_index]
            claim["assertion"] = "confirmed"
            for fact_ref in claim["fact_refs"]:
                ledger_id, fact_id = fact_ref.split(":", 1)
                fact = mutated_ledgers[ledger_id]["facts"][fact_id]
                fact["value"] = fabricated_values[
                    validate.FACT_IDENTITY_CONTRACT[fact_ref][1]
                ]
                fact["posture"] = "confirmed"
                fact["lifecycle"] = "operating"
            with (
                self.subTest(segment_id=segment["id"], claim_id=claim["id"]),
                self.assertRaisesRegex(
                    validate.ValidationError,
                    "immutable fact",
                ),
            ):
                validate._validate_course(
                    mutated_course,
                    master,
                    mutated_ledgers,
                    cameras,
                )

        self.assertEqual(17, len(vulnerable_claims))
        self.assertEqual(
            affected_segments,
            {
                course["acts"][act_index]["segments"][segment_index]["id"]
                for act_index, segment_index, _ in vulnerable_claims
            },
        )

    def test_numeric_fact_minimum_contract_is_exact_and_immutable(
        self,
    ) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        registered_numeric_ids = {
            f"{ledger_id}:{fact_id}"
            for ledger_id, ledger in ledgers.items()
            for fact_id in ledger["facts"]
            if validate.FACT_IDENTITY_CONTRACT[f"{ledger_id}:{fact_id}"][1] == "number"
        }
        self.assertEqual(47, len(registered_numeric_ids))
        self.assertEqual(
            set(validate.FACT_NUMERIC_MINIMUM_CONTRACT),
            registered_numeric_ids,
        )
        self.assertEqual({0}, set(validate.FACT_NUMERIC_MINIMUM_CONTRACT.values()))
        with self.assertRaises(TypeError):
            validate.FACT_NUMERIC_MINIMUM_CONTRACT["unexpected:fact"] = 0

    def test_all_numeric_facts_reject_negative_and_noncanonical_zero(
        self,
    ) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        self.assertEqual(47, len(validate.FACT_NUMERIC_MINIMUM_CONTRACT))
        populated_payload_rejections = 0
        null_count = 0
        for qualified_id in sorted(validate.FACT_NUMERIC_MINIMUM_CONTRACT):
            ledger_id, fact_id = qualified_id.split(":", 1)

            negative = deepcopy(ledgers[ledger_id])
            negative["facts"][fact_id]["value"] = -1
            negative["facts"][fact_id]["posture"] = "confirmed"
            negative["facts"][fact_id]["lifecycle"] = "operating"
            with (
                self.subTest(qualified_id=qualified_id, boundary="negative"),
                self.assertRaisesRegex(
                    validate.ValidationError,
                    r"numeric minimum contract requires value >= 0",
                ),
            ):
                validate._validate_evidence_schema(
                    negative,
                    ledger_id=ledger_id,
                )

            zero = deepcopy(ledgers[ledger_id])
            zero["facts"][fact_id]["value"] = 0
            if ledgers[ledger_id]["facts"][fact_id]["value"] is None:
                null_count += 1
                zero["facts"][fact_id]["posture"] = "confirmed"
                zero["facts"][fact_id]["lifecycle"] = "operating"
                with (
                    self.subTest(qualified_id=qualified_id, boundary="zero_null"),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable fact semantic contract requires",
                    ),
                ):
                    validate._validate_evidence_schema(zero, ledger_id=ledger_id)
            else:
                populated_payload_rejections += 1
                with (
                    self.subTest(qualified_id=qualified_id, boundary="zero_populated"),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable fact payload contract requires exact",
                    ),
                ):
                    validate._validate_evidence_schema(zero, ledger_id=ledger_id)
        self.assertEqual(22, populated_payload_rejections)
        self.assertEqual(25, null_count)

    def test_all_numeric_facts_reject_booleans_and_nonfinite_values(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        invalid_values = (True, math.nan, math.inf, -math.inf)
        for qualified_id in sorted(validate.FACT_NUMERIC_MINIMUM_CONTRACT):
            ledger_id, fact_id = qualified_id.split(":", 1)
            for invalid in invalid_values:
                mutated = deepcopy(ledgers[ledger_id])
                mutated["facts"][fact_id]["value"] = invalid
                with (
                    self.subTest(qualified_id=qualified_id, invalid=invalid),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "requires a finite number",
                    ),
                ):
                    validate._validate_evidence_schema(mutated, ledger_id=ledger_id)

    def test_coordinated_value_and_unit_mutations_fail_for_all_segments(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        master = validate._load_yaml_strict(validate.DIAGRAM / "master.yaml")
        cameras = validate._load_yaml_strict(validate.DIAGRAM / "cameras.yaml")
        ledgers = validate._load_course_evidence_ledgers(course)
        segments = {
            segment["id"]: segment
            for act in course["acts"]
            for segment in act["segments"]
        }
        probes = {
            "p0_gigawatt_not_workload": "abilene:planned_grid_interconnection_mw",
            "p1_read_the_machine": "abilene:grid_initial_service_operational_as_of",
            "s01_fire_to_electricity": "abilene:gas_turbine_units_authorized",
            "s02_generator_terminal": "abilene:gas_turbine_units_authorized",
            "s03_initial_grid_path": "abilene:grid_initial_source_line",
            "s04_expansion_grid_path": "abilene:grid_expansion_substation_voltage_kv",
            "s05_ppa_not_wire": "commercial_energy:crane_microsoft_ppa_contract",
            "s06_campus_mv_envelope": "abilene:campus_mv_reference_design_voltage_kv",
            "s07_building_power_train": (
                "electrical_engineering:unit_substation_coordinated_assembly_role"
            ),
            "s08_rack_voltage_descent": "abilene:rack_platform",
            "s09_watt_becomes_heat": "abilene:rack_platform",
            "s10_two_rack_heat_paths": ("abilene:rack_platform_nvl72_design_reference"),
            "s11_technology_loop": "abilene:cooling_direct_to_chip_design",
            "s12_cdu_boundary": "abilene:cooling_heat_rejection_posture",
            "s13_residual_air_branch": "abilene:rack_air_cooled_components",
            "s14_facility_heat_rejection": "abilene:cooling_heat_rejection_posture",
            "s15_water_accounting": (
                "abilene:cooling_initial_fill_gallons_per_building"
            ),
            "s16_close_atmosphere": "abilene:rack_platform",
            "s17_interconnection_schedule": ("abilene:planned_grid_interconnection_mw"),
            "s18_long_lead_equipment": "abilene:gas_turbine_units_authorized",
            "s19_fast_load_slow_grid": "abilene:bess_reference_design_status",
            "s20_build_sequence": "abilene:planned_grid_interconnection_mw",
            "s21_capital_ownership": (
                "commercial_compute:stargate_initial_equity_funders"
            ),
            "s22_capital_risk": (
                "commercial_compute:abilene_phase1_financing_structure"
            ),
            "s23_business_models": (
                "commercial_compute:abilene_2024_crusoe_owner_developer_announcement"
            ),
            "s24_megawatts_to_tokens": (
                "abilene:oracle_capacity_delivered_percent_untyped"
            ),
        }
        self.assertEqual(set(segments), set(probes))
        for segment_id, fact_ref in probes.items():
            self.assertTrue(
                any(
                    fact_ref in claim["fact_refs"]
                    for claim in segments[segment_id]["evidence"]["claims"]
                )
            )
            mutated = deepcopy(ledgers)
            ledger_id, fact_id = fact_ref.split(":", 1)
            mutated[ledger_id]["facts"][fact_id]["value"] = True
            mutated[ledger_id]["facts"][fact_id]["unit"] = "boolean"
            with (
                self.subTest(segment_id=segment_id, fact_ref=fact_ref),
                self.assertRaisesRegex(
                    validate.ValidationError,
                    "immutable fact identity requires",
                ),
            ):
                validate._validate_course(course, master, mutated, cameras)

    def test_all_registered_evidence_ledgers_satisfy_nested_schema(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        ledgers = validate._load_course_evidence_ledgers(course)
        self.assertEqual(set(course["meta"]["evidence_ledgers"]), set(ledgers))

    def test_installed_gpu_count_fails_closed(self) -> None:
        fact = self.evidence["facts"]["installed_gpu_count"]
        self.assertIsNone(fact["value"])
        self.assertEqual("no evidence-backed estimate", fact["basis"])

    def test_oracle_delivery_claim_separates_effective_and_access_dates(self) -> None:
        fact = self.evidence["facts"]["oracle_capacity_delivered_percent_untyped"]
        source = self.evidence["sources"]["oracle_abilene_portfolio"]
        self.assertEqual("2026-01", fact["as_of"])
        self.assertEqual("2026-08-25", source["accessed_as_of"])
        self.assertIn("current January 2026", source["date_note"])

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
        self.assertEqual(
            "selected_design", facts["cooling_heat_rejection_posture"]["lifecycle"]
        )
        self.assertNotIn(
            "direct-to-chip", facts["cooling_heat_rejection_posture"]["basis"]
        )
        self.assertEqual(
            "design_reference", facts["cooling_direct_to_chip_design"]["lifecycle"]
        )
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
            with (
                self.subTest(label=label),
                self.assertRaisesRegex(validate.ValidationError, "cannot support"),
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
        with self.assertRaisesRegex(
            validate.ValidationError, "source_ids must equal fact source union"
        ):
            validate._validate_fact_binding(record, facts, "probe")


class TopologyPostureTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.master = layout.load_yaml(validate.DIAGRAM / "master.yaml")

    def test_btm_step_up_path_stays_a_conceptual_teaching_reference(self) -> None:
        nodes = {node["id"]: node for node in self.master["nodes"]}
        edges = {edge["id"]: edge for edge in self.master["edges"]}
        for record in (
            nodes["gsu_transformer"],
            edges["btm_terminal_to_gsu"],
            edges["btm_gsu_to_mv"],
        ):
            self.assertEqual("teaching_reference", record["presence"])
            self.assertEqual("conceptual", record["lifecycle"])
            self.assertNotIn("gas_turbine_units_authorized", record["fact_ids"])

    def test_residual_air_connection_stays_a_conceptual_teaching_reference(
        self,
    ) -> None:
        edges = {edge["id"]: edge for edge in self.master["edges"]}
        record = edges["rack_air_load_to_crah"]
        self.assertEqual("teaching_reference", record["presence"])
        self.assertEqual("conceptual", record["lifecycle"])
        self.assertEqual([], record["source_ids"])
        self.assertEqual([], record["fact_ids"])


class MasterSchemaMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.master = validate._load_yaml_strict(validate.DIAGRAM / "master.yaml")
        cls.evidence = validate._load_yaml_strict(validate.EVIDENCE)
        cls.source_ids, _ = validate._validate_evidence(cls.evidence)

    def assert_master_rejected(self, master: dict, message: str) -> None:
        with self.assertRaisesRegex(validate.ValidationError, message):
            validate._validate_master(master, self.evidence, self.source_ids)

    def test_master_container_schemas_are_exact_and_typed(self) -> None:
        mutations = []

        extra_root = deepcopy(self.master)
        extra_root["unexpected"] = True
        mutations.append(
            ("extra root", extra_root, r"master: missing=.*extra=.*unexpected")
        )

        missing_root = deepcopy(self.master)
        missing_root["unexpected"] = missing_root.pop("reference_campus")
        mutations.append(
            (
                "missing plus extra root",
                missing_root,
                r"master: missing=.*reference_campus.*extra=.*unexpected",
            )
        )

        extra_meta = deepcopy(self.master)
        extra_meta["meta"]["unexpected"] = True
        mutations.append(
            ("extra meta", extra_meta, r"master\.meta: missing=.*extra=.*unexpected")
        )

        missing_posture = deepcopy(self.master)
        missing_posture["meta"].pop("diagram_posture")
        mutations.append(
            (
                "missing diagram posture",
                missing_posture,
                r"master\.meta: missing=.*diagram_posture",
            )
        )

        boolean_version = deepcopy(self.master)
        boolean_version["meta"]["version"] = True
        mutations.append(("boolean version", boolean_version, "must be the integer 1"))

        string_date = deepcopy(self.master)
        string_date["meta"]["reference_as_of"] = "2026-08-25"
        mutations.append(
            ("string reference date", string_date, "expected an exact date")
        )

        missing_scope = deepcopy(self.master)
        missing_scope["reference_campus"].pop("scope_boundary")
        mutations.append(
            (
                "missing scope boundary",
                missing_scope,
                r"reference_campus: missing=.*scope_boundary",
            )
        )

        extra_style = deepcopy(self.master)
        extra_style["status_styles"]["energized"]["unexpected"] = True
        mutations.append(
            (
                "extra status style",
                extra_style,
                r"status_styles\.energized: missing=.*extra=.*unexpected",
            )
        )

        for label, master, message in mutations:
            with self.subTest(label=label):
                self.assert_master_rejected(master, message)

    def test_master_copy_variants_are_exact_typed_and_exclusive(self) -> None:
        mutations = []

        extra_copy_field = deepcopy(self.master)
        extra_copy_field["copy"]["title"]["unexpected"] = True
        mutations.append(("extra field", extra_copy_field, "copy must use exactly"))

        boolean_text = deepcopy(self.master)
        boolean_text["copy"]["title"]["text"] = True
        mutations.append(("boolean text", boolean_text, "expected a non-empty string"))

        ambiguous = deepcopy(self.master)
        ambiguous["copy"]["title"]["template"] = "{gas_turbine_units_authorized}"
        ambiguous["copy"]["title"]["facts"] = ["gas_turbine_units_authorized"]
        mutations.append(("text plus template", ambiguous, "copy must use exactly"))

        boolean_fact_id = deepcopy(self.master)
        boolean_fact_id["copy"]["region_substations"]["facts"] = [True]
        mutations.append(
            ("boolean fact ID", boolean_fact_id, "expected a list of strings")
        )

        visible_hidden_copy = deepcopy(self.master)
        visible_hidden_copy["copy"]["nuclear_variant"]["base_visible"] = True
        mutations.append(("visible hidden copy", visible_hidden_copy, "must be false"))

        for label, master, message in mutations:
            with self.subTest(label=label):
                self.assert_master_rejected(master, message)

    def test_topology_presence_contract_is_exact_immutable_and_enforced(self) -> None:
        actual_contract = {
            f"{kind}:{record['id']}": record["presence"]
            for kind, records in (
                ("node", self.master["nodes"]),
                ("edge", self.master["edges"]),
            )
            for record in records
        }
        self.assertEqual(64, len(actual_contract))
        self.assertEqual(dict(validate.TOPOLOGY_PRESENCE_CONTRACT), actual_contract)
        with self.assertRaises(TypeError):
            validate.TOPOLOGY_PRESENCE_CONTRACT["node:unexpected"] = (
                "teaching_reference"
            )

        for kind, records in (
            ("node", self.master["nodes"]),
            ("edge", self.master["edges"]),
        ):
            for canonical_record in records:
                master = deepcopy(self.master)
                record = next(
                    item
                    for item in master[f"{kind}s"]
                    if item["id"] == canonical_record["id"]
                )
                record["presence"] = (
                    "site_evidenced"
                    if canonical_record["presence"] != "site_evidenced"
                    else "teaching_reference"
                )
                with (
                    self.subTest(kind=kind, record_id=record["id"]),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable presence contract requires",
                    ),
                ):
                    validate._validate_master(
                        master,
                        self.evidence,
                        self.source_ids,
                    )

    def test_topology_presence_contract_rejects_identity_drift(self) -> None:
        master = deepcopy(self.master)
        master["nodes"][0]["id"] = "unexpected_node"
        with self.assertRaisesRegex(
            validate.ValidationError,
            r"immutable topology presence contract mismatch: "
            r"missing=.*node:gas_turbine.*extra=.*node:unexpected_node",
        ):
            validate._validate_master(master, self.evidence, self.source_ids)

    def test_all_17_scope_ambiguous_records_reject_site_promotion(self) -> None:
        expected = {
            "teaching_reference": {
                "node": {"gsu_transformer", "campus_mv_distribution"},
                "edge": {
                    "btm_terminal_to_gsu",
                    "btm_gsu_to_mv",
                    "grid138_station_to_mv",
                    "grid345_lpt_to_mv",
                    "bess_to_mv",
                    "diesel_to_mv",
                },
            },
            "platform_evidenced": {
                "node": {
                    "power_shelf",
                    "rack_air_load",
                    "cold_plate",
                    "rack_manifold",
                },
                "edge": {
                    "busway_to_power_shelf",
                    "power_shelf_to_vrm",
                    "die_to_cold_plate_heat",
                    "cold_plate_to_manifold_return",
                    "manifold_to_cold_plate_supply",
                },
            },
        }
        actual = {
            presence: {
                kind: {
                    record["id"]
                    for record in self.master[f"{kind}s"]
                    if record["presence"] == presence
                    and record["lifecycle"]
                    in (
                        validate.NODE_PRESENCE_LIFECYCLES
                        if kind == "node"
                        else validate.EDGE_PRESENCE_LIFECYCLES
                    )["site_evidenced"]
                    and record["source_ids"]
                    and record["fact_ids"]
                }
                for kind in ("node", "edge")
            }
            for presence in ("teaching_reference", "platform_evidenced")
        }
        self.assertEqual(expected, actual)
        self.assertEqual(
            17,
            sum(
                len(record_ids)
                for by_kind in actual.values()
                for record_ids in by_kind.values()
            ),
        )

        for presence, by_kind in actual.items():
            for kind, record_ids in by_kind.items():
                for record_id in sorted(record_ids):
                    master = deepcopy(self.master)
                    record = next(
                        item for item in master[f"{kind}s"] if item["id"] == record_id
                    )
                    record["presence"] = "site_evidenced"
                    with (
                        self.subTest(
                            presence=presence,
                            kind=kind,
                            record_id=record_id,
                        ),
                        self.assertRaisesRegex(
                            validate.ValidationError,
                            "immutable presence contract requires",
                        ),
                    ):
                        validate._validate_master(
                            master,
                            self.evidence,
                            self.source_ids,
                        )

    def test_all_evidence_free_records_reject_site_evidenced_promotion(self) -> None:
        expected_nodes = {
            "nuclear_ppa",
            "unit_substation",
            "lv_switchgear",
            "ups",
            "busway",
            "vrm",
            "cdu",
            "crah",
            "atmosphere",
        }
        expected_edges = {
            "nuclear_ppa_overlay",
            "mv_to_unit_sub",
            "unit_sub_to_lv",
            "lv_to_ups",
            "ups_to_busway",
            "vrm_to_die",
            "manifold_to_cdu_return",
            "cdu_to_manifold_supply",
            "cdu_to_facility_return",
            "facility_to_cdu_supply",
            "rack_air_load_to_crah",
            "crah_to_facility_return",
            "facility_to_crah_supply",
        }
        actual_nodes = {
            record["id"]
            for record in self.master["nodes"]
            if not record["source_ids"] and not record["fact_ids"]
        }
        actual_edges = {
            record["id"]
            for record in self.master["edges"]
            if not record["source_ids"] and not record["fact_ids"]
        }
        self.assertEqual(expected_nodes, actual_nodes)
        self.assertEqual(expected_edges, actual_edges)
        self.assertEqual(22, len(actual_nodes | actual_edges))

        for kind, record_ids in (("nodes", actual_nodes), ("edges", actual_edges)):
            for record_id in sorted(record_ids):
                master = deepcopy(self.master)
                record = next(item for item in master[kind] if item["id"] == record_id)
                record["presence"] = "site_evidenced"
                with (
                    self.subTest(kind=kind, record_id=record_id),
                    self.assertRaisesRegex(
                        validate.ValidationError,
                        "immutable presence contract requires",
                    ),
                ):
                    validate._validate_master(
                        master,
                        self.evidence,
                        self.source_ids,
                    )

    def test_presence_lifecycle_state_flow_and_sink_combinations_are_closed(
        self,
    ) -> None:
        cases = []

        variant_flow = deepcopy(self.master)
        next(
            edge
            for edge in variant_flow["edges"]
            if edge["id"] == "nuclear_ppa_overlay"
        )["flow_direction"] = "forward"
        cases.append(
            ("variant physical flow", variant_flow, "course_variant edges require")
        )

        permitted_state = deepcopy(self.master)
        next(
            edge
            for edge in permitted_state["edges"]
            if edge["id"] == "btm_fuel_to_shaft"
        )["normal_state"] = "unknown"
        cases.append(
            ("permitted unknown state", permitted_state, "must occur together")
        )

        terminal_teaching = deepcopy(self.master)
        next(node for node in terminal_teaching["nodes"] if node["id"] == "atmosphere")[
            "presence"
        ] = "teaching_reference"
        cases.append(
            (
                "terminal teaching",
                terminal_teaching,
                "immutable presence contract requires",
            )
        )

        evidence_removed = deepcopy(self.master)
        gas_turbine = next(
            node for node in evidence_removed["nodes"] if node["id"] == "gas_turbine"
        )
        gas_turbine["source_ids"] = []
        gas_turbine["fact_ids"] = []
        cases.append(
            ("evidenced without owners", evidence_removed, "requires non-empty")
        )

        for label, master, message in cases:
            with self.subTest(label=label):
                self.assert_master_rejected(master, message)


class ProjectContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = validate.validate_project()
        cls.master = layout.load_yaml(validate.DIAGRAM / "master.yaml")
        cls.evidence = layout.load_yaml(validate.EVIDENCE)
        cls.source_ids, _ = validate._validate_evidence(cls.evidence)

    def test_full_contract(self) -> None:
        self.assertEqual(7, self.result["evidence_ledgers"])
        self.assertEqual(71, self.result["sources"])
        self.assertEqual(184, self.result["facts"])
        self.assertEqual(30, self.result["nodes"])
        self.assertEqual(34, self.result["edges"])
        self.assertEqual(6, self.result["cameras"])
        self.assertEqual(8, self.result["verified_generated_artifacts"])

    def test_central_validator_invokes_exact_generated_artifact_parity(self) -> None:
        with (
            patch.object(
                validate.generated_artifacts_pipeline,
                "assert_current",
                side_effect=generated_artifacts.GeneratedArtifactError(
                    "generated parity sentinel"
                ),
            ),
            self.assertRaisesRegex(
                validate.ValidationError, "generated parity sentinel"
            ),
        ):
            validate.validate_project()

    def test_every_master_record_has_evidence_bindings(self) -> None:
        for location in ("nodes", "edges"):
            for record in self.master[location]:
                self.assertIn("fact_ids", record)
                self.assertIsInstance(record["fact_ids"], list)

    def test_master_node_and_edge_fields_are_exact(self) -> None:
        mutations = []
        node_extra = deepcopy(self.master)
        node_extra["nodes"][0]["unexpected"] = True
        mutations.append(("node extra", node_extra))

        node_missing_extra = deepcopy(self.master)
        node_missing_extra["nodes"][0]["unexpected"] = node_missing_extra["nodes"][
            0
        ].pop("gate")
        mutations.append(("node missing plus extra", node_missing_extra))

        edge_extra = deepcopy(self.master)
        edge_extra["edges"][0]["unexpected"] = True
        mutations.append(("edge extra", edge_extra))

        edge_missing_extra = deepcopy(self.master)
        edge_missing_extra["edges"][0]["unexpected"] = edge_missing_extra["edges"][
            0
        ].pop("carries")
        mutations.append(("edge missing plus extra", edge_missing_extra))

        for label, master in mutations:
            with (
                self.subTest(label=label),
                self.assertRaisesRegex(
                    validate.ValidationError, r"missing=.*extra=.*unexpected"
                ),
            ):
                validate._validate_master(master, self.evidence, self.source_ids)

    def test_master_string_fields_require_exact_strings(self) -> None:
        for kind, fields in (
            (
                "nodes",
                ("id", "label", "domain", "gate", "presence", "lifecycle"),
            ),
            (
                "edges",
                (
                    "id",
                    "from",
                    "to",
                    "carries",
                    "presence",
                    "lifecycle",
                    "normal_state",
                    "flow_direction",
                ),
            ),
        ):
            for field in fields:
                master = deepcopy(self.master)
                master[kind][0][field] = True
                with (
                    self.subTest(kind=kind, field=field),
                    self.assertRaisesRegex(
                        validate.ValidationError, "expected a non-empty string"
                    ),
                ):
                    validate._validate_master(master, self.evidence, self.source_ids)

    def test_master_posture_enums_are_closed(self) -> None:
        mutations = (
            ("nodes", "presence", "as_built_operational", "unknown presence"),
            ("nodes", "lifecycle", "commissioned", "unknown lifecycle"),
            ("edges", "presence", "physical_sink", "unknown presence"),
            ("edges", "lifecycle", "commissioned", "unknown lifecycle"),
            ("edges", "normal_state", "normally_open", "unknown normal state"),
            ("edges", "flow_direction", "reverse", "unknown flow direction"),
        )
        for kind, field, value, message in mutations:
            master = deepcopy(self.master)
            master[kind][0][field] = value
            with (
                self.subTest(kind=kind, field=field),
                self.assertRaisesRegex(validate.ValidationError, message),
            ):
                validate._validate_master(master, self.evidence, self.source_ids)

    def test_master_optional_fields_have_exact_types(self) -> None:
        node_base_visible = deepcopy(self.master)
        node_base_visible["nodes"][0]["base_visible"] = 0
        edge_base_visible = deepcopy(self.master)
        edge_base_visible["edges"][0]["base_visible"] = 0
        node_reveal = deepcopy(self.master)
        node_reveal["nodes"][0]["reveal_copy_ids"] = [True]
        for label, master, message in (
            ("node base visibility", node_base_visible, "expected a boolean"),
            ("edge base visibility", edge_base_visible, "expected a boolean"),
            ("node reveal copy", node_reveal, "expected a list of strings"),
        ):
            with (
                self.subTest(label=label),
                self.assertRaisesRegex(validate.ValidationError, message),
            ):
                validate._validate_master(master, self.evidence, self.source_ids)

    def test_course_schema_version_requires_an_exact_integer(self) -> None:
        course = validate._load_yaml_strict(validate.COURSE)
        cameras = validate._load_yaml_strict(validate.DIAGRAM / "cameras.yaml")
        ledgers = validate._load_course_evidence_ledgers(course)
        for invalid in (True, 2.0, "2"):
            mutated = deepcopy(course)
            mutated["schema_version"] = invalid
            with (
                self.subTest(invalid=invalid),
                self.assertRaisesRegex(
                    validate.ValidationError, "course schema_version must be 2"
                ),
            ):
                validate._validate_course(mutated, self.master, ledgers, cameras)

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
        nuclear_ppa = next(
            node for node in master["nodes"] if node["id"] == "nuclear_ppa"
        )
        del nuclear_ppa["reveal_copy_ids"]
        source_ids, _ = validate._validate_evidence(self.evidence)
        with self.assertRaisesRegex(
            validate.ValidationError, "hidden master copy requires"
        ):
            validate._validate_master(master, self.evidence, source_ids)


if __name__ == "__main__":
    unittest.main()
