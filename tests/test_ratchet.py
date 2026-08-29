import copy
import math
import unittest
from itertools import pairwise

from gigawatt import ratchet

SEGMENT_IDS = [f"s{index:02d}" for index in range(1, 27)]
VIEWPORT_IDS = list(ratchet.CANONICAL_VIEWPORT_IDS)
EVALUATION_IDS = [
    f"{segment_id}@{viewport_id}"
    for segment_id in SEGMENT_IDS
    for viewport_id in VIEWPORT_IDS
]
TRANSITION_IDS = [
    f"{predecessor_id}->{successor_id}"
    for predecessor_id, successor_id in pairwise(SEGMENT_IDS)
]
CURRENT_AUDIT_SUBJECT_SHA256 = "a" * 64


def score_inputs(
    *,
    severity: float = 2.0,
    teaching_importance: float = 3.0,
    affected_sections: int = 1,
    confidence: float = 0.5,
    repair_risk: float = 1.5,
) -> dict:
    return {
        "severity": severity,
        "teaching_importance": teaching_importance,
        "affected_sections": affected_sections,
        "confidence": confidence,
        "repair_risk": repair_risk,
    }


def finding(
    finding_id: str = "finding-layout",
    *,
    affected_segment_ids: list[str] | None = None,
    severity: float = 2.0,
) -> dict:
    affected_segment_ids = affected_segment_ids or [SEGMENT_IDS[0]]
    inputs = score_inputs(
        severity=severity,
        affected_sections=len(affected_segment_ids),
    )
    return {
        "finding_id": finding_id,
        "summary": "A concrete auditable defect",
        "affected_segment_ids": list(affected_segment_ids),
        **inputs,
        "priority_score": ratchet.priority_score(inputs),
        "evidence_ref": "artifact:independent-comparison-vector",
    }


def audit_report(role: str, auditor_id: str, *, findings: list[dict]) -> dict:
    return {
        "role": role,
        "auditor_id": auditor_id,
        "status": "complete",
        "evidence_ref": f"report:{role}",
        "segment_ids": list(SEGMENT_IDS),
        "viewport_ids": list(VIEWPORT_IDS),
        "evaluation_ids": list(EVALUATION_IDS),
        "transition_ids": list(TRANSITION_IDS),
        "findings": findings,
    }


def audit_round(sequence: int = 1) -> dict:
    visual_finding = finding()
    return {
        "round_id": f"round-{sequence}",
        "sequence": sequence,
        "audit_subject_sha256": CURRENT_AUDIT_SUBJECT_SHA256,
        "status": "complete",
        "loop_speed": "fast",
        "change_scopes": ["layout"],
        "research_trigger": None,
        "consultation_decisions": [],
        "audit_reports": [
            audit_report("visual_layout", "auditor-visual", findings=[visual_finding]),
            audit_report("pedagogy", "auditor-pedagogy", findings=[]),
            audit_report("adversarial_correctness", "auditor-adversarial", findings=[]),
        ],
        "selected_finding_id": visual_finding["finding_id"],
        "challenger_dispositions": [
            {
                "candidate_id": "candidate",
                "disposition": "rejected",
                "decision_ref": f"pareto:candidate:round-{sequence}",
            }
        ],
    }


def clean_audit_round(sequence: int = 1) -> dict:
    record = audit_round(sequence)
    for report in record["audit_reports"]:
        report["findings"] = []
    record["selected_finding_id"] = None
    return record


def required_protection_members() -> dict[str, list[str]]:
    return {
        "protected_dimensions": ["focus_occupancy"],
        "worst_decile_segments": ["s24"],
        "predecessors": ["s23"],
        "successors": ["s25"],
        "shared_consumers": ["focus_key"],
    }


def pareto_candidate() -> dict:
    members = required_protection_members()
    return {
        "candidate_id": "combined",
        "target": {
            "dimension_id": "annotation_claim_coverage",
            "direction": "increase",
            "champion_value": 0.4,
            "candidate_value": 0.6,
            "minimum_material_improvement": 0.1,
            "evidence_ref": "comparison:annotation",
        },
        "modeled_gate_evidence": {
            gate_id: {
                "status": "passed",
                "evidence_ref": f"modeled:{gate_id}",
            }
            for gate_id in ("target:annotation", "layout:occupancy_review")
        },
        "protection_evidence": {
            cohort: [
                {
                    "member_id": member_id,
                    "regressed": False,
                    "evidence_ref": f"protection:{cohort}:{member_id}",
                }
                for member_id in member_ids
            ]
            for cohort, member_ids in members.items()
        },
        "static_gate_evidence": {
            gate_id: {
                "status": "passed",
                "evidence_ref": f"gate:{gate_id}",
            }
            for gate_id in ratchet.STATIC_GATE_IDS
        },
        "live_gate_evidence": {
            gate_id: {
                "status": "passed",
                "evidence_ref": f"gate:{gate_id}",
            }
            for gate_id in ratchet.LIVE_GATE_IDS
        },
        "blind_reviews": [
            {
                "reviewer_id": "reviewer-a",
                "blind": True,
                "preference": "candidate",
                "evidence_ref": "review:a",
            },
            {
                "reviewer_id": "reviewer-b",
                "blind": True,
                "preference": "candidate",
                "evidence_ref": "review:b",
            },
            {
                "reviewer_id": "reviewer-c",
                "blind": True,
                "preference": "champion",
                "evidence_ref": "review:c",
            },
        ],
    }


class PriorityContractTests(unittest.TestCase):
    def test_priority_score_uses_only_the_exact_formula(self) -> None:
        inputs = score_inputs(
            severity=4,
            teaching_importance=3,
            affected_sections=2,
            confidence=0.5,
            repair_risk=2,
        )
        self.assertEqual(ratchet.priority_score(inputs), 6.0)

    def test_priority_score_accepts_every_declared_domain_boundary(self) -> None:
        boundary_cases = (
            ("severity-minimum", {"severity": 1}, 1.0),
            ("severity-maximum", {"severity": 5}, 5.0),
            ("teaching-importance-minimum", {"teaching_importance": 1}, 1.0),
            ("teaching-importance-maximum", {"teaching_importance": 5}, 5.0),
            ("confidence-minimum", {"confidence": 0}, 0.0),
            ("confidence-maximum", {"confidence": 1}, 1.0),
            ("repair-risk-minimum", {"repair_risk": 1}, 1.0),
            ("repair-risk-above-minimum", {"repair_risk": 10}, 0.1),
        )

        for label, mutation, expected in boundary_cases:
            inputs = score_inputs(
                severity=1,
                teaching_importance=1,
                confidence=1,
                repair_risk=1,
            )
            inputs.update(mutation)
            with self.subTest(case=label):
                self.assertEqual(ratchet.priority_score(inputs), expected)

    def test_priority_score_rejects_each_domain_violation_independently(
        self,
    ) -> None:
        mutations = (
            ("severity-below", "severity", 0.999),
            ("severity-above", "severity", 5.001),
            ("severity-type", "severity", "1"),
            ("severity-bool", "severity", True),
            ("teaching-importance-below", "teaching_importance", 0.999),
            ("teaching-importance-above", "teaching_importance", 5.001),
            ("teaching-importance-type", "teaching_importance", "1"),
            ("teaching-importance-bool", "teaching_importance", True),
            ("confidence-below", "confidence", -0.001),
            ("confidence-above", "confidence", 1.001),
            ("confidence-type", "confidence", "0.5"),
            ("confidence-bool", "confidence", True),
            ("repair-risk-below", "repair_risk", 0.999),
            ("repair-risk-non-finite", "repair_risk", math.inf),
            ("repair-risk-type", "repair_risk", "1"),
            ("repair-risk-bool", "repair_risk", True),
        )

        for label, field, value in mutations:
            inputs = score_inputs()
            inputs[field] = value
            with (
                self.subTest(case=label),
                self.assertRaises(ratchet.RatchetContractError),
            ):
                ratchet.priority_score(inputs)

    def test_priority_score_fails_closed_on_invalid_numbers_and_schema(self) -> None:
        mutations = []
        for field, value in (
            ("severity", True),
            ("severity", math.nan),
            ("teaching_importance", math.inf),
            ("affected_sections", 0),
            ("confidence", 1.01),
            ("repair_risk", 0),
        ):
            record = score_inputs()
            record[field] = value
            mutations.append(record)
        missing = score_inputs()
        missing.pop("confidence")
        mutations.append(missing)
        unknown = score_inputs()
        unknown["weight"] = 1
        mutations.append(unknown)

        for mutation in mutations:
            with (
                self.subTest(mutation=mutation),
                self.assertRaises(ratchet.RatchetContractError),
            ):
                ratchet.priority_score(mutation)


class AuditRoundContractTests(unittest.TestCase):
    def test_valid_round_has_exact_independent_26_by_3_coverage(self) -> None:
        record = audit_round()
        original = copy.deepcopy(record)
        validated = ratchet.validate_audit_round(record, segment_ids=SEGMENT_IDS)
        self.assertEqual(validated, record)
        self.assertEqual(record, original)
        self.assertEqual(
            {
                (report["role"], segment_id)
                for report in validated["audit_reports"]
                for segment_id in report["segment_ids"]
            },
            {
                (role, segment_id)
                for role in ratchet.AUDIT_ROLES
                for segment_id in SEGMENT_IDS
            },
        )
        self.assertEqual(
            len({report["auditor_id"] for report in validated["audit_reports"]}),
            3,
        )
        for report in validated["audit_reports"]:
            self.assertEqual(report["segment_ids"], SEGMENT_IDS)
            self.assertEqual(report["viewport_ids"], VIEWPORT_IDS)
            self.assertEqual(report["evaluation_ids"], EVALUATION_IDS)
            self.assertEqual(report["transition_ids"], TRANSITION_IDS)
        self.assertEqual(len(EVALUATION_IDS), 130)
        self.assertEqual(len(TRANSITION_IDS), 25)

    def test_finding_evidence_cannot_self_reference_the_finding(self) -> None:
        for evidence_ref in (
            "audit:finding-layout",
            "course/quality_audits.yaml#round-1/finding-layout",
            "artifact.json?finding=finding-layout&round=1",
        ):
            record = audit_round()
            record["audit_reports"][0]["findings"][0]["evidence_ref"] = evidence_ref
            with (
                self.subTest(evidence_ref=evidence_ref),
                self.assertRaisesRegex(
                    ratchet.RatchetContractError, "must not self-reference"
                ),
            ):
                ratchet.validate_audit_round(record, segment_ids=SEGMENT_IDS)

    def test_round_rejects_coverage_independence_and_schema_mutations(self) -> None:
        mutations: list[dict] = []

        missing_segment = audit_round()
        missing_segment["audit_reports"][0]["segment_ids"].pop()
        mutations.append(missing_segment)

        duplicate_segment = audit_round()
        duplicate_segment["audit_reports"][0]["segment_ids"][-1] = SEGMENT_IDS[0]
        mutations.append(duplicate_segment)

        reordered_segments = audit_round()
        reordered_segments["audit_reports"][0]["segment_ids"][0:2] = reversed(
            reordered_segments["audit_reports"][0]["segment_ids"][0:2]
        )
        mutations.append(reordered_segments)

        for coverage_field, extra_id in (
            ("viewport_ids", "1280x720"),
            ("evaluation_ids", "s99@1280x720"),
            ("transition_ids", "s26->s27"),
        ):
            missing = audit_round()
            missing["audit_reports"][0][coverage_field].pop()
            mutations.append(missing)

            extra = audit_round()
            extra["audit_reports"][0][coverage_field].append(extra_id)
            mutations.append(extra)

            duplicate = audit_round()
            duplicate["audit_reports"][0][coverage_field][-1] = duplicate[
                "audit_reports"
            ][0][coverage_field][0]
            mutations.append(duplicate)

            reordered = audit_round()
            reordered["audit_reports"][0][coverage_field][0:2] = reversed(
                reordered["audit_reports"][0][coverage_field][0:2]
            )
            mutations.append(reordered)

        reused_auditor = audit_round()
        reused_auditor["audit_reports"][1]["auditor_id"] = "auditor-visual"
        mutations.append(reused_auditor)

        duplicate_role = audit_round()
        duplicate_role["audit_reports"][1]["role"] = "visual_layout"
        mutations.append(duplicate_role)

        unknown_role = audit_round()
        unknown_role["audit_reports"][1]["role"] = "copy_edit"
        mutations.append(unknown_role)

        unknown_field = audit_round()
        unknown_field["average_score"] = 1
        mutations.append(unknown_field)

        forged_score = audit_round()
        forged_score["audit_reports"][0]["findings"][0]["priority_score"] += 0.01
        mutations.append(forged_score)

        forged_count = audit_round()
        forged_count["audit_reports"][0]["findings"][0]["affected_sections"] = 2
        mutations.append(forged_count)

        pending_report = audit_round()
        pending_report["audit_reports"][0]["status"] = "pending"
        pending_report["audit_reports"][0]["evidence_ref"] = None
        mutations.append(pending_report)

        complete_without_evidence = audit_round()
        complete_without_evidence["audit_reports"][0]["evidence_ref"] = None
        mutations.append(complete_without_evidence)

        for mutation in mutations:
            with (
                self.subTest(mutation=mutation),
                self.assertRaises(ratchet.RatchetContractError),
            ):
                ratchet.validate_audit_round(mutation, segment_ids=SEGMENT_IDS)

    def test_round_must_select_a_highest_priority_finding(self) -> None:
        record = audit_round()
        higher = finding("finding-higher", severity=5)
        record["audit_reports"][1]["findings"].append(higher)
        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "highest-priority finding"
        ):
            ratchet.validate_audit_round(record, segment_ids=SEGMENT_IDS)
        record["selected_finding_id"] = higher["finding_id"]
        ratchet.validate_audit_round(record, segment_ids=SEGMENT_IDS)

    def test_fast_and_slow_loop_constraints_are_fail_closed(self) -> None:
        fast = audit_round()
        fast["change_scopes"] = ["primary_source_research"]
        with self.assertRaisesRegex(ratchet.RatchetContractError, "invalid for fast"):
            ratchet.validate_audit_round(fast, segment_ids=SEGMENT_IDS)

        fast = audit_round()
        fast["research_trigger"] = {
            "finding_id": "finding-layout",
            "pedagogical_problem": "Missing source",
            "missing_evidence_owner_ids": ["fact:x"],
            "primary_sources_only": True,
            "ambiguity_policy": "preserve_null_or_explicit_limit",
        }
        with self.assertRaisesRegex(ratchet.RatchetContractError, "fast audit"):
            ratchet.validate_audit_round(fast, segment_ids=SEGMENT_IDS)

        slow = audit_round()
        slow["loop_speed"] = "slow"
        slow["change_scopes"] = ["primary_source_research"]
        slow["research_trigger"] = {
            "finding_id": "finding-layout",
            "pedagogical_problem": "The claim owner lacks primary evidence",
            "missing_evidence_owner_ids": ["fact:ledger:missing"],
            "primary_sources_only": True,
            "ambiguity_policy": "preserve_null_or_explicit_limit",
        }
        ratchet.validate_audit_round(slow, segment_ids=SEGMENT_IDS)

        mutations = []
        missing_trigger = copy.deepcopy(slow)
        missing_trigger["research_trigger"] = None
        mutations.append(missing_trigger)
        unknown_finding = copy.deepcopy(slow)
        unknown_finding["research_trigger"]["finding_id"] = "finding:unknown"
        mutations.append(unknown_finding)
        secondary_sources = copy.deepcopy(slow)
        secondary_sources["research_trigger"]["primary_sources_only"] = False
        mutations.append(secondary_sources)
        promoted_ambiguity = copy.deepcopy(slow)
        promoted_ambiguity["research_trigger"]["ambiguity_policy"] = "estimate"
        mutations.append(promoted_ambiguity)
        mixed_speed = copy.deepcopy(slow)
        mixed_speed["change_scopes"].append("layout")
        mutations.append(mixed_speed)
        for mutation in mutations:
            with (
                self.subTest(mutation=mutation),
                self.assertRaises(ratchet.RatchetContractError),
            ):
                ratchet.validate_audit_round(mutation, segment_ids=SEGMENT_IDS)

    def test_restricted_changes_require_exact_authorization(self) -> None:
        record = audit_round()
        record["change_scopes"].append("course_order")
        with self.assertRaisesRegex(ratchet.RatchetContractError, "authorized"):
            ratchet.validate_audit_round(record, segment_ids=SEGMENT_IDS)

        record["consultation_decisions"] = [
            {
                "decision_id": "decision-order",
                "scope": "course_order",
                "disposition": "authorized",
                "decision_maker_id": "course-owner",
                "authorization_ref": "user-message:42",
            }
        ]
        ratchet.validate_audit_round(record, segment_ids=SEGMENT_IDS)

        missing_ref = copy.deepcopy(record)
        missing_ref["consultation_decisions"][0]["authorization_ref"] = None
        with self.assertRaisesRegex(ratchet.RatchetContractError, "authorization_ref"):
            ratchet.validate_audit_round(missing_ref, segment_ids=SEGMENT_IDS)

        pending_with_ref = copy.deepcopy(record["consultation_decisions"][0])
        pending_with_ref["disposition"] = "pending"
        with self.assertRaisesRegex(ratchet.RatchetContractError, "null"):
            ratchet.validate_consultation_decision(pending_with_ref)

    def test_challenger_dispositions_are_strict_records(self) -> None:
        unknown = audit_round()
        unknown["challenger_dispositions"][0]["disposition"] = "preferred"
        with self.assertRaises(ratchet.RatchetContractError):
            ratchet.validate_audit_round(unknown, segment_ids=SEGMENT_IDS)

        duplicate = audit_round()
        duplicate["challenger_dispositions"].append(
            copy.deepcopy(duplicate["challenger_dispositions"][0])
        )
        with self.assertRaisesRegex(ratchet.RatchetContractError, "duplicate"):
            ratchet.validate_audit_round(duplicate, segment_ids=SEGMENT_IDS)


class ParetoContractTests(unittest.TestCase):
    def evaluate(self, candidate: dict) -> dict:
        return ratchet.pareto_decision(
            candidate,
            required_protection_members=required_protection_members(),
            required_modeled_gate_ids=[
                "target:annotation",
                "layout:occupancy_review",
            ],
        )

    def test_acceptance_requires_material_improvement_and_every_protection(
        self,
    ) -> None:
        candidate = pareto_candidate()
        original = copy.deepcopy(candidate)
        decision = self.evaluate(candidate)
        self.assertEqual(candidate, original)
        self.assertEqual(decision["disposition"], "accepted")
        self.assertEqual(decision["material_improvement"]["delta"], 0.2)
        self.assertTrue(decision["material_improvement"]["passed"])
        self.assertTrue(decision["regression_free"])
        self.assertEqual(
            decision["regression_counts"],
            {cohort: 0 for cohort in ratchet.PROTECTION_COHORTS},
        )
        self.assertEqual(decision["static_gate_status"], "passed")
        self.assertEqual(decision["live_gate_status"], "passed")
        self.assertEqual(decision["blind_review"]["candidate_preferences"], 2)

    def test_material_threshold_is_inclusive_and_directional(self) -> None:
        exact = pareto_candidate()
        exact["target"]["champion_value"] = 0.4
        exact["target"]["candidate_value"] = 0.5
        exact["target"]["minimum_material_improvement"] = 0.1
        self.assertEqual(self.evaluate(exact)["disposition"], "accepted")

        below = copy.deepcopy(exact)
        below["target"]["candidate_value"] = 0.499
        self.assertEqual(self.evaluate(below)["disposition"], "rejected")

        decrease = copy.deepcopy(exact)
        decrease["target"]["direction"] = "decrease"
        decrease["target"]["champion_value"] = 0.5
        decrease["target"]["candidate_value"] = 0.4
        self.assertEqual(self.evaluate(decrease)["disposition"], "accepted")

    def test_every_protection_cohort_rejects_one_regression(self) -> None:
        for cohort in ratchet.PROTECTION_COHORTS:
            candidate = pareto_candidate()
            candidate["protection_evidence"][cohort][0]["regressed"] = True
            with self.subTest(cohort=cohort):
                decision = self.evaluate(candidate)
                self.assertEqual(decision["disposition"], "rejected")
                self.assertIn(f"regression:{cohort}", decision["reasons"])

    def test_protection_coverage_cannot_be_vacuous_or_duplicated(self) -> None:
        missing = pareto_candidate()
        missing["protection_evidence"]["shared_consumers"] = []
        with self.assertRaisesRegex(ratchet.RatchetContractError, "every required"):
            self.evaluate(missing)

        duplicate = pareto_candidate()
        duplicate["protection_evidence"]["predecessors"].append(
            copy.deepcopy(duplicate["protection_evidence"]["predecessors"][0])
        )
        with self.assertRaisesRegex(ratchet.RatchetContractError, "duplicate"):
            self.evaluate(duplicate)

        missing_required_cohort = required_protection_members()
        missing_required_cohort.pop("successors")
        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "fields must be exact"
        ):
            ratchet.pareto_decision(
                pareto_candidate(),
                required_protection_members=missing_required_cohort,
                required_modeled_gate_ids=[
                    "target:annotation",
                    "layout:occupancy_review",
                ],
            )

        for cohort in ratchet.PROTECTION_COHORTS:
            empty_required_cohort = required_protection_members()
            empty_required_cohort[cohort] = []
            with (
                self.subTest(empty_required_cohort=cohort),
                self.assertRaisesRegex(
                    ratchet.RatchetContractError, "must not be empty"
                ),
            ):
                ratchet.pareto_decision(
                    pareto_candidate(),
                    required_protection_members=empty_required_cohort,
                    required_modeled_gate_ids=[
                        "target:annotation",
                        "layout:occupancy_review",
                    ],
                )

    def test_static_and_live_gate_evidence_drive_rejected_and_pending(self) -> None:
        failed = pareto_candidate()
        failed["static_gate_evidence"]["evidence"] = {
            "status": "failed",
            "evidence_ref": "failure:evidence",
        }
        self.assertEqual(self.evaluate(failed)["disposition"], "rejected")

        pending = pareto_candidate()
        pending["live_gate_evidence"]["browser"] = {
            "status": "pending",
            "evidence_ref": None,
        }
        decision = self.evaluate(pending)
        self.assertEqual(decision["disposition"], "pending")
        self.assertEqual(decision["live_gate_status"], "pending")

        rejected_dominates = copy.deepcopy(pending)
        rejected_dominates["target"]["candidate_value"] = 0.4
        self.assertEqual(self.evaluate(rejected_dominates)["disposition"], "rejected")

        passed_without_evidence = pareto_candidate()
        passed_without_evidence["live_gate_evidence"]["browser"]["evidence_ref"] = None
        with self.assertRaisesRegex(ratchet.RatchetContractError, "evidence_ref"):
            self.evaluate(passed_without_evidence)

        missing_gate = pareto_candidate()
        missing_gate["static_gate_evidence"].pop("validation")
        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "fields must be exact"
        ):
            self.evaluate(missing_gate)

    def test_absolute_modeled_gates_cannot_be_bypassed_by_relative_protection(
        self,
    ) -> None:
        pending = pareto_candidate()
        pending["modeled_gate_evidence"]["layout:occupancy_review"] = {
            "status": "pending",
            "evidence_ref": None,
        }
        decision = self.evaluate(pending)
        self.assertEqual(decision["disposition"], "pending")
        self.assertEqual(decision["modeled_gate_status"], "pending")

        failed = pareto_candidate()
        failed["modeled_gate_evidence"]["layout:occupancy_review"] = {
            "status": "failed",
            "evidence_ref": "modeled:occupancy-failure",
        }
        decision = self.evaluate(failed)
        self.assertEqual(decision["disposition"], "rejected")
        self.assertEqual(decision["modeled_gate_status"], "failed")

        missing = pareto_candidate()
        missing["modeled_gate_evidence"].pop("layout:occupancy_review")
        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "fields must be exact"
        ):
            self.evaluate(missing)

    def test_blind_review_requires_three_independent_blind_votes_and_two_preferences(
        self,
    ) -> None:
        insufficient = pareto_candidate()
        insufficient["blind_reviews"][1]["preference"] = "champion"
        self.assertEqual(self.evaluate(insufficient)["disposition"], "rejected")

        pending = pareto_candidate()
        pending["blind_reviews"][1]["preference"] = "pending"
        pending["blind_reviews"][1]["evidence_ref"] = None
        self.assertEqual(self.evaluate(pending)["disposition"], "pending")

        impossible = copy.deepcopy(pending)
        impossible["blind_reviews"][0]["preference"] = "champion"
        self.assertEqual(self.evaluate(impossible)["disposition"], "rejected")

        nonblind = pareto_candidate()
        nonblind["blind_reviews"][0]["blind"] = False
        self.assertEqual(self.evaluate(nonblind)["disposition"], "rejected")

        duplicate = pareto_candidate()
        duplicate["blind_reviews"][1]["reviewer_id"] = "reviewer-a"
        with self.assertRaisesRegex(ratchet.RatchetContractError, "independent"):
            self.evaluate(duplicate)

    def test_pareto_schema_rejects_unknown_fields_and_bool_numbers(self) -> None:
        unknown = pareto_candidate()
        unknown["weighted_average"] = 10
        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "fields must be exact"
        ):
            self.evaluate(unknown)

        forged_number = pareto_candidate()
        forged_number["target"]["candidate_value"] = True
        with self.assertRaisesRegex(ratchet.RatchetContractError, "finite number"):
            self.evaluate(forged_number)

    def test_serialized_pareto_result_must_match_its_coupled_evidence(self) -> None:
        accepted = self.evaluate(pareto_candidate())
        self.assertEqual(
            ratchet.validate_pareto_result(accepted),
            accepted,
        )

        mutations = []

        no_material_improvement = copy.deepcopy(accepted)
        no_material_improvement["material_improvement"]["delta"] = 0.0
        no_material_improvement["material_improvement"]["passed"] = False
        mutations.append(no_material_improvement)

        regressed = copy.deepcopy(accepted)
        regressed["regression_counts"]["shared_consumers"] = 1
        regressed["regression_free"] = False
        mutations.append(regressed)

        for field in (
            "modeled_gate_status",
            "static_gate_status",
            "live_gate_status",
        ):
            pending = copy.deepcopy(accepted)
            pending[field] = "pending"
            mutations.append(pending)

        blind_pending = copy.deepcopy(accepted)
        blind_pending["blind_review"]["status"] = "pending"
        mutations.append(blind_pending)

        accepted_with_reason = copy.deepcopy(accepted)
        accepted_with_reason["reasons"] = ["forged"]
        mutations.append(accepted_with_reason)

        for mutated in mutations:
            with (
                self.subTest(mutated=mutated),
                self.assertRaises(ratchet.RatchetContractError),
            ):
                ratchet.validate_pareto_result(mutated)

        bool_count = copy.deepcopy(accepted)
        bool_count["regression_counts"]["predecessors"] = False
        with self.assertRaisesRegex(ratchet.RatchetContractError, "integer"):
            ratchet.validate_pareto_result(bool_count)


class SaturationContractTests(unittest.TestCase):
    def evaluate(
        self,
        rounds: list[dict],
        *,
        threshold: float = 5.0,
        current_disposition: str = "rejected",
    ) -> dict:
        return ratchet.evaluate_saturation(
            rounds,
            segment_ids=SEGMENT_IDS,
            high_priority_threshold=threshold,
            current_challenger_dispositions=[
                {
                    "candidate_id": "candidate",
                    "disposition": current_disposition,
                    "decision_ref": "pareto:candidate:current",
                }
            ],
            current_audit_subject_sha256=CURRENT_AUDIT_SUBJECT_SHA256,
        )

    def test_two_consecutive_complete_clean_rounds_saturate(self) -> None:
        result = self.evaluate([clean_audit_round(1), clean_audit_round(2)])
        self.assertTrue(result["saturated"])
        self.assertEqual(result["status"], "saturated")
        self.assertEqual(result["qualifying_round_ids"], ["round-1", "round-2"])
        self.assertEqual(result["required_role_segment_coverage_per_round"], 78)
        self.assertEqual(result["required_viewport_coverage_per_report"], 5)
        self.assertEqual(result["required_evaluation_coverage_per_report"], 130)
        self.assertEqual(result["required_transition_coverage_per_report"], 25)
        self.assertEqual(
            result["current_audit_subject_sha256"],
            CURRENT_AUDIT_SUBJECT_SHA256,
        )
        self.assertEqual(result["reasons"], [])

    def test_terminal_rounds_must_bind_the_current_audit_subject(self) -> None:
        legacy = [clean_audit_round(1), clean_audit_round(2)]
        legacy[0].pop("audit_subject_sha256")
        result = self.evaluate(legacy)
        self.assertFalse(result["saturated"])
        self.assertEqual(
            result["reasons"],
            ["audit_subject_sha256_missing:round-1"],
        )

        stale = [clean_audit_round(1), clean_audit_round(2)]
        for record in stale:
            record["audit_subject_sha256"] = "b" * 64
        result = self.evaluate(stale)
        self.assertFalse(result["saturated"])
        self.assertEqual(
            result["reasons"],
            [
                "audit_subject_sha256_mismatch:round-1",
                "audit_subject_sha256_mismatch:round-2",
            ],
        )

        mixed = [clean_audit_round(1), clean_audit_round(2)]
        mixed[1]["audit_subject_sha256"] = "b" * 64
        result = self.evaluate(mixed)
        self.assertFalse(result["saturated"])
        self.assertEqual(
            result["reasons"],
            ["audit_subject_sha256_mismatch:round-2"],
        )

        current = self.evaluate([clean_audit_round(1), clean_audit_round(2)])
        self.assertTrue(current["saturated"])
        self.assertEqual(current["reasons"], [])

    def test_audit_subject_digests_are_strict_lowercase_sha256(self) -> None:
        malformed_values = (
            None,
            "",
            "a" * 63,
            "a" * 65,
            "A" * 64,
            "g" * 64,
            f"{'a' * 64}\n",
        )
        for value in malformed_values:
            record = clean_audit_round(1)
            record["audit_subject_sha256"] = value
            with (
                self.subTest(round_digest=value),
                self.assertRaisesRegex(
                    ratchet.RatchetContractError,
                    "lowercase SHA-256 digest",
                ),
            ):
                ratchet.validate_audit_round(record, segment_ids=SEGMENT_IDS)

            with (
                self.subTest(current_digest=value),
                self.assertRaisesRegex(
                    ratchet.RatchetContractError,
                    "lowercase SHA-256 digest",
                ),
            ):
                ratchet.evaluate_saturation(
                    [clean_audit_round(1), clean_audit_round(2)],
                    segment_ids=SEGMENT_IDS,
                    high_priority_threshold=5.0,
                    current_challenger_dispositions=[
                        {
                            "candidate_id": "candidate",
                            "disposition": "rejected",
                            "decision_ref": "pareto:candidate:current",
                        }
                    ],
                    current_audit_subject_sha256=value,
                )

    def test_current_audit_subject_digest_is_a_required_argument(self) -> None:
        with self.assertRaisesRegex(TypeError, "current_audit_subject_sha256"):
            ratchet.evaluate_saturation(
                [clean_audit_round(1), clean_audit_round(2)],
                segment_ids=SEGMENT_IDS,
                high_priority_threshold=5.0,
                current_challenger_dispositions=[
                    {
                        "candidate_id": "candidate",
                        "disposition": "rejected",
                        "decision_ref": "pareto:candidate:current",
                    }
                ],
            )

    def test_single_round_reports_high_findings_without_saturating(self) -> None:
        high = audit_round(1)
        high_finding = high["audit_reports"][0]["findings"][0]
        high_finding.update(
            {
                "severity": 5,
                "teaching_importance": 5,
                "confidence": 1,
                "repair_risk": 1,
            }
        )
        high_finding["priority_score"] = ratchet.priority_score(
            {field: high_finding[field] for field in ratchet._PRIORITY_FIELDS}
        )

        result = self.evaluate([high])
        self.assertFalse(result["saturated"])
        self.assertEqual(result["status"], "continue")
        self.assertEqual(result["high_finding_ids"], ["finding-layout"])
        self.assertEqual(
            result["reasons"],
            [
                "fewer_than_two_rounds",
                "findings_remain:round-1",
                "high_priority_findings_remain",
            ],
        )

        history = [high, clean_audit_round(2), clean_audit_round(3)]
        terminally_clean = self.evaluate(history)
        self.assertTrue(terminally_clean["saturated"])
        self.assertEqual(terminally_clean["high_finding_ids"], [])

    def test_saturation_uses_only_the_two_latest_sequence_consecutive_rounds(
        self,
    ) -> None:
        nonconsecutive = [clean_audit_round(1), clean_audit_round(3)]
        result = self.evaluate(nonconsecutive)
        self.assertFalse(result["saturated"])
        self.assertIn("terminal_rounds_not_sequence_consecutive", result["reasons"])

        one_round = self.evaluate([clean_audit_round(1)])
        self.assertFalse(one_round["saturated"])
        self.assertEqual(one_round["reasons"], ["fewer_than_two_rounds"])

        older_clean = [
            clean_audit_round(1),
            clean_audit_round(2),
            clean_audit_round(3),
        ]
        older_clean[-1]["challenger_dispositions"][0]["disposition"] = "pending"
        self.assertTrue(self.evaluate(older_clean)["saturated"])

    def test_incomplete_high_or_admissible_round_blocks_saturation(self) -> None:
        incomplete = clean_audit_round(2)
        incomplete["status"] = "incomplete"
        incomplete["audit_reports"][0]["status"] = "pending"
        incomplete["audit_reports"][0]["evidence_ref"] = None
        self.assertFalse(self.evaluate([clean_audit_round(1), incomplete])["saturated"])

        for disposition in ("pending", "accepted"):
            with self.subTest(disposition=disposition):
                result = self.evaluate(
                    [clean_audit_round(1), clean_audit_round(2)],
                    current_disposition=disposition,
                )
                self.assertFalse(result["saturated"])
                self.assertIn(
                    "admissible_or_pending_improvement:round-2", result["reasons"]
                )

        high = audit_round(2)
        high_finding = high["audit_reports"][0]["findings"][0]
        high_finding.update(
            {
                "severity": 5,
                "teaching_importance": 5,
                "confidence": 1,
                "repair_risk": 1,
            }
        )
        high_finding["priority_score"] = ratchet.priority_score(
            {field: high_finding[field] for field in ratchet._PRIORITY_FIELDS}
        )
        result = self.evaluate([clean_audit_round(1), high])
        self.assertFalse(result["saturated"])
        self.assertEqual(result["high_finding_ids"], ["finding-layout"])
        self.assertIn("findings_remain:round-2", result["reasons"])
        self.assertIn("high_priority_findings_remain", result["reasons"])

    def test_any_terminal_finding_blocks_regardless_of_priority_threshold(self) -> None:
        low = audit_round(2)
        result = self.evaluate(
            [clean_audit_round(1), low],
            threshold=1_000_000.0,
        )

        self.assertFalse(result["saturated"])
        self.assertEqual(result["qualifying_round_ids"], [])
        self.assertEqual(result["high_finding_ids"], [])
        self.assertIn("findings_remain:round-2", result["reasons"])
        self.assertNotIn("high_priority_findings_remain", result["reasons"])

    def test_saturation_uses_current_decisions_without_rewriting_history(self) -> None:
        rounds = [clean_audit_round(1), clean_audit_round(2)]
        original = copy.deepcopy(rounds)
        self.assertTrue(self.evaluate(rounds)["saturated"])

        result = self.evaluate(rounds, current_disposition="pending")
        self.assertFalse(result["saturated"])
        self.assertIn(
            "admissible_or_pending_improvement:round-2",
            result["reasons"],
        )
        self.assertEqual(
            result["current_challenger_dispositions"][0]["disposition"],
            "pending",
        )
        self.assertEqual(rounds, original)

        current = [
            {
                "candidate_id": "candidate",
                "disposition": "pending",
                "decision_ref": "pareto:candidate:current",
            }
        ]
        historical = ratchet.reconcile_audit_round_dispositions(
            rounds,
            segment_ids=SEGMENT_IDS,
            current_challenger_dispositions=current,
        )
        self.assertEqual(historical, original)
        self.assertEqual(
            historical[-1]["challenger_dispositions"][0]["disposition"],
            "rejected",
        )
        historical[-1]["challenger_dispositions"][0]["disposition"] = "accepted"
        self.assertEqual(rounds, original)

    def test_saturation_rejects_invalid_history_and_coverage(self) -> None:
        duplicate_sequence = [clean_audit_round(1), clean_audit_round(1)]
        duplicate_sequence[1]["round_id"] = "different-id"
        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "strictly increasing"
        ):
            self.evaluate(duplicate_sequence)

        duplicate_finding = [audit_round(1), audit_round(2)]
        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "globally unique across rounds"
        ):
            self.evaluate(duplicate_finding)

        missing_coverage = clean_audit_round(2)
        missing_coverage["audit_reports"][2]["segment_ids"].pop()
        with self.assertRaisesRegex(ratchet.RatchetContractError, "canonical"):
            self.evaluate([clean_audit_round(1), missing_coverage])

        unknown = clean_audit_round(2)
        unknown["saturated"] = True
        with self.assertRaisesRegex(ratchet.RatchetContractError, "unknown"):
            self.evaluate([clean_audit_round(1), unknown])

        with self.assertRaisesRegex(
            ratchet.RatchetContractError, "current generated decisions"
        ):
            ratchet.evaluate_saturation(
                [clean_audit_round(1)],
                segment_ids=SEGMENT_IDS,
                high_priority_threshold=5.0,
                current_challenger_dispositions=[
                    {
                        "candidate_id": "different-candidate",
                        "disposition": "rejected",
                        "decision_ref": "pareto:different-candidate",
                    }
                ],
                current_audit_subject_sha256=CURRENT_AUDIT_SUBJECT_SHA256,
            )

        with self.assertRaisesRegex(
            ratchet.RatchetContractError,
            "current_challenger_dispositions must be a sequence",
        ):
            ratchet.evaluate_saturation(
                [clean_audit_round(1)],
                segment_ids=SEGMENT_IDS,
                high_priority_threshold=5.0,
                current_challenger_dispositions=None,
                current_audit_subject_sha256=CURRENT_AUDIT_SUBJECT_SHA256,
            )


if __name__ == "__main__":
    unittest.main()
