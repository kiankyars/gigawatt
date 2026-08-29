"""Pure, fail-closed contracts for course quality ratchet records."""

from __future__ import annotations

import copy
import math
import re
from collections.abc import Mapping, Sequence
from decimal import Decimal, InvalidOperation
from itertools import pairwise
from typing import Any

EXPECTED_SEGMENT_COUNT = 26
CANONICAL_VIEWPORT_IDS = (
    "1920x1080",
    "1440x900",
    "1024x768",
    "844x390",
    "390x844",
)
EXPECTED_EVALUATION_COUNT = EXPECTED_SEGMENT_COUNT * len(CANONICAL_VIEWPORT_IDS)
EXPECTED_TRANSITION_COUNT = EXPECTED_SEGMENT_COUNT - 1
AUDIT_ROLES = (
    "visual_layout",
    "pedagogy",
    "adversarial_correctness",
)
ROUND_STATUSES = frozenset({"complete", "incomplete"})
REPORT_STATUSES = frozenset({"complete", "pending"})
LOOP_SPEEDS = frozenset({"fast", "slow"})
DISPOSITIONS = frozenset({"accepted", "rejected", "pending"})

FAST_CHANGE_SCOPES = frozenset(
    {
        "layout",
        "label_hierarchy",
        "framing",
        "annotation",
        "authored_transformation",
        "navigation",
        "accessibility",
    }
)
SLOW_CHANGE_SCOPES = frozenset({"primary_source_research"})
RESTRICTED_CHANGE_SCOPES = frozenset(
    {
        "course_thesis",
        "course_order",
        "course_objectives",
        "visual_language",
        "substantive_material_removal",
        "evidence_boundary_weakening",
        "pareto_incomparable_aesthetic",
        "private_as_built_evidence",
        "presenter_comfort",
        "learner_retention",
    }
)
CONSULTATION_DISPOSITIONS = frozenset({"authorized", "rejected", "pending"})

PROTECTION_COHORTS = (
    "protected_dimensions",
    "worst_decile_segments",
    "predecessors",
    "successors",
    "shared_consumers",
)
STATIC_GATE_IDS = ("validation", "deterministic_generation", "evidence")
LIVE_GATE_IDS = ("browser", "accessibility_snapshot")
GATE_STATUSES = frozenset({"passed", "failed", "pending"})
REVIEW_PREFERENCES = frozenset({"candidate", "champion", "tie", "pending"})

_PRIORITY_FIELDS = frozenset(
    {
        "severity",
        "teaching_importance",
        "affected_sections",
        "confidence",
        "repair_risk",
    }
)
_FINDING_FIELDS = _PRIORITY_FIELDS | frozenset(
    {
        "finding_id",
        "summary",
        "affected_segment_ids",
        "priority_score",
        "evidence_ref",
    }
)
_REPORT_FIELDS = frozenset(
    {
        "role",
        "auditor_id",
        "status",
        "evidence_ref",
        "segment_ids",
        "viewport_ids",
        "evaluation_ids",
        "transition_ids",
        "findings",
    }
)
_ROUND_FIELDS = frozenset(
    {
        "round_id",
        "sequence",
        "status",
        "loop_speed",
        "change_scopes",
        "research_trigger",
        "consultation_decisions",
        "audit_reports",
        "selected_finding_id",
        "challenger_dispositions",
    }
)
_OPTIONAL_ROUND_FIELDS = frozenset({"audit_subject_sha256"})
_SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")


class RatchetContractError(ValueError):
    """Raised when ratchet data is incomplete, ambiguous, or internally false."""


def _mapping(value: Any, location: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise RatchetContractError(f"{location} must be a mapping")
    return value


def _exact_keys(
    value: Mapping[str, Any], expected: set[str] | frozenset[str], location: str
) -> None:
    actual = set(value)
    if actual != set(expected):
        missing = sorted(set(expected) - actual)
        unknown = sorted(actual - set(expected))
        raise RatchetContractError(
            f"{location} fields must be exact; missing={missing} unknown={unknown}"
        )


def _exact_keys_with_optional(
    value: Mapping[str, Any],
    required: set[str] | frozenset[str],
    optional: set[str] | frozenset[str],
    location: str,
) -> None:
    actual = set(value)
    missing = sorted(set(required) - actual)
    unknown = sorted(actual - (set(required) | set(optional)))
    if missing or unknown:
        raise RatchetContractError(
            f"{location} fields must be exact; missing={missing} unknown={unknown}"
        )


def _list(value: Any, location: str) -> list[Any]:
    if not isinstance(value, list):
        raise RatchetContractError(f"{location} must be a list")
    return value


def _string(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise RatchetContractError(f"{location} must be a non-empty string")
    return value


def _sha256(value: Any, location: str) -> str:
    if not isinstance(value, str) or _SHA256_PATTERN.fullmatch(value) is None:
        raise RatchetContractError(f"{location} must be a lowercase SHA-256 digest")
    return value


def _references_finding_id(evidence_ref: str, finding_id: str) -> bool:
    return (
        re.search(
            rf"(?<![A-Za-z0-9_-]){re.escape(finding_id)}(?![A-Za-z0-9_-])",
            evidence_ref,
        )
        is not None
    )


def _boolean(value: Any, location: str) -> bool:
    if not isinstance(value, bool):
        raise RatchetContractError(f"{location} must be a boolean")
    return value


def _integer(value: Any, location: str, *, positive: bool = False) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RatchetContractError(f"{location} must be an integer")
    if positive and value <= 0:
        raise RatchetContractError(f"{location} must be positive")
    return value


def _decimal(value: Any, location: str) -> Decimal:
    if isinstance(value, bool) or not isinstance(value, (int, float, Decimal)):
        raise RatchetContractError(f"{location} must be a finite number")
    try:
        result = Decimal(str(value))
    except (InvalidOperation, ValueError) as exc:
        raise RatchetContractError(f"{location} must be a finite number") from exc
    if not result.is_finite():
        raise RatchetContractError(f"{location} must be a finite number")
    return result


def _positive_decimal(value: Any, location: str) -> Decimal:
    result = _decimal(value, location)
    if result <= 0:
        raise RatchetContractError(f"{location} must be positive")
    return result


def _unique_strings(
    value: Any, location: str, *, allow_empty: bool = True
) -> list[str]:
    records = _list(value, location)
    if not allow_empty and not records:
        raise RatchetContractError(f"{location} must not be empty")
    strings = [
        _string(item, f"{location}[{index}]") for index, item in enumerate(records)
    ]
    if len(strings) != len(set(strings)):
        raise RatchetContractError(f"{location} must not contain duplicate IDs")
    return strings


def _segment_ids(segment_ids: Sequence[str]) -> tuple[str, ...]:
    if isinstance(segment_ids, (str, bytes)) or not isinstance(segment_ids, Sequence):
        raise RatchetContractError("segment_ids must be a sequence")
    values = [
        _string(segment_id, f"segment_ids[{index}]")
        for index, segment_id in enumerate(segment_ids)
    ]
    if len(values) != EXPECTED_SEGMENT_COUNT:
        raise RatchetContractError(
            f"segment_ids must contain exactly {EXPECTED_SEGMENT_COUNT} IDs"
        )
    if len(values) != len(set(values)):
        raise RatchetContractError("segment_ids must not contain duplicates")
    return tuple(values)


def canonical_evaluation_ids(segment_ids: Sequence[str]) -> tuple[str, ...]:
    """Return the canonical segment-major audit evaluation IDs."""

    expected_segments = _segment_ids(segment_ids)
    return tuple(
        f"{segment_id}@{viewport_id}"
        for segment_id in expected_segments
        for viewport_id in CANONICAL_VIEWPORT_IDS
    )


def canonical_transition_ids(segment_ids: Sequence[str]) -> tuple[str, ...]:
    """Return the canonical ordered predecessor-to-successor audit IDs."""

    expected_segments = _segment_ids(segment_ids)
    return tuple(
        f"{predecessor_id}->{successor_id}"
        for predecessor_id, successor_id in pairwise(expected_segments)
    )


def _validate_exact_ordered_ids(
    value: Any,
    *,
    expected: Sequence[str],
    location: str,
) -> list[str]:
    actual = _unique_strings(value, location, allow_empty=False)
    if actual != list(expected):
        raise RatchetContractError(
            f"{location} must exactly match canonical IDs in canonical order"
        )
    return actual


def priority_score(score_inputs: Mapping[str, Any]) -> float:
    """Return the unrounded contract priority score for exact score inputs."""

    score_inputs = _mapping(score_inputs, "priority")
    _exact_keys(score_inputs, _PRIORITY_FIELDS, "priority")
    severity = _decimal(score_inputs["severity"], "priority.severity")
    if not Decimal(1) <= severity <= Decimal(5):
        raise RatchetContractError(
            "priority.severity must be between 1 and 5 inclusive"
        )
    teaching_importance = _decimal(
        score_inputs["teaching_importance"], "priority.teaching_importance"
    )
    if not Decimal(1) <= teaching_importance <= Decimal(5):
        raise RatchetContractError(
            "priority.teaching_importance must be between 1 and 5 inclusive"
        )
    affected_sections = _integer(
        score_inputs["affected_sections"],
        "priority.affected_sections",
        positive=True,
    )
    confidence = _decimal(score_inputs["confidence"], "priority.confidence")
    if not Decimal(0) <= confidence <= Decimal(1):
        raise RatchetContractError(
            "priority.confidence must be between 0 and 1 inclusive"
        )
    repair_risk = _decimal(score_inputs["repair_risk"], "priority.repair_risk")
    if repair_risk < 1:
        raise RatchetContractError("priority.repair_risk must be at least 1")
    score = (
        severity
        * teaching_importance
        * Decimal(affected_sections)
        * confidence
        / repair_risk
    )
    result = float(score)
    if not math.isfinite(result):
        raise RatchetContractError("priority score must be finite")
    return result


def _validate_finding(
    finding: Any, *, segment_ids: tuple[str, ...], location: str
) -> Mapping[str, Any]:
    finding = _mapping(finding, location)
    _exact_keys(finding, _FINDING_FIELDS, location)
    finding_id = _string(finding["finding_id"], f"{location}.finding_id")
    _string(finding["summary"], f"{location}.summary")
    evidence_ref = _string(finding["evidence_ref"], f"{location}.evidence_ref")
    if _references_finding_id(evidence_ref, finding_id):
        raise RatchetContractError(
            f"{location}.evidence_ref must not self-reference finding {finding_id!r}"
        )
    affected = _unique_strings(
        finding["affected_segment_ids"],
        f"{location}.affected_segment_ids",
        allow_empty=False,
    )
    unknown = set(affected) - set(segment_ids)
    if unknown:
        raise RatchetContractError(
            f"{location}.affected_segment_ids contains unknown IDs {sorted(unknown)}"
        )
    affected_sections = _integer(
        finding["affected_sections"],
        f"{location}.affected_sections",
        positive=True,
    )
    if affected_sections != len(affected):
        raise RatchetContractError(
            f"{location}.affected_sections must equal the unique affected segment count"
        )
    score_inputs = {field: finding[field] for field in _PRIORITY_FIELDS}
    expected_score = priority_score(score_inputs)
    actual_score = float(
        _decimal(finding["priority_score"], f"{location}.priority_score")
    )
    if actual_score != expected_score:
        raise RatchetContractError(
            f"{location}.priority_score must equal the exact priority formula"
        )
    return finding


def validate_consultation_decision(decision: Mapping[str, Any]) -> dict[str, Any]:
    """Validate one decision at a user-owned preference boundary."""

    decision = _mapping(decision, "consultation_decision")
    expected = {
        "decision_id",
        "scope",
        "disposition",
        "decision_maker_id",
        "authorization_ref",
    }
    _exact_keys(decision, expected, "consultation_decision")
    _string(decision["decision_id"], "consultation_decision.decision_id")
    scope = _string(decision["scope"], "consultation_decision.scope")
    if scope not in RESTRICTED_CHANGE_SCOPES:
        raise RatchetContractError(
            f"consultation_decision.scope is not restricted: {scope!r}"
        )
    disposition = _string(decision["disposition"], "consultation_decision.disposition")
    if disposition not in CONSULTATION_DISPOSITIONS:
        raise RatchetContractError(
            f"unsupported consultation disposition {disposition!r}"
        )
    _string(decision["decision_maker_id"], "consultation_decision.decision_maker_id")
    authorization_ref = decision["authorization_ref"]
    if disposition == "authorized":
        _string(authorization_ref, "consultation_decision.authorization_ref")
    elif authorization_ref is not None:
        raise RatchetContractError(
            "non-authorized consultation decisions must have a null authorization_ref"
        )
    return copy.deepcopy(dict(decision))


def _validate_research_trigger(
    trigger: Any, *, finding_ids: set[str], location: str
) -> None:
    trigger = _mapping(trigger, location)
    expected = {
        "finding_id",
        "pedagogical_problem",
        "missing_evidence_owner_ids",
        "primary_sources_only",
        "ambiguity_policy",
    }
    _exact_keys(trigger, expected, location)
    finding_id = _string(trigger["finding_id"], f"{location}.finding_id")
    if finding_id not in finding_ids:
        raise RatchetContractError(
            f"{location}.finding_id must reference a finding in the same round"
        )
    _string(trigger["pedagogical_problem"], f"{location}.pedagogical_problem")
    _unique_strings(
        trigger["missing_evidence_owner_ids"],
        f"{location}.missing_evidence_owner_ids",
        allow_empty=False,
    )
    if (
        _boolean(trigger["primary_sources_only"], f"{location}.primary_sources_only")
        is not True
    ):
        raise RatchetContractError(f"{location}.primary_sources_only must be true")
    if trigger["ambiguity_policy"] != "preserve_null_or_explicit_limit":
        raise RatchetContractError(
            f"{location}.ambiguity_policy must preserve nulls or explicit limits"
        )


def _validate_challenger_dispositions(value: Any, location: str) -> None:
    records = _list(value, location)
    candidate_ids: list[str] = []
    for index, record in enumerate(records):
        item_location = f"{location}[{index}]"
        record = _mapping(record, item_location)
        _exact_keys(
            record,
            {"candidate_id", "disposition", "decision_ref"},
            item_location,
        )
        candidate_ids.append(
            _string(record["candidate_id"], f"{item_location}.candidate_id")
        )
        disposition = _string(record["disposition"], f"{item_location}.disposition")
        if disposition not in DISPOSITIONS:
            raise RatchetContractError(
                f"unsupported challenger disposition {disposition!r}"
            )
        _string(record["decision_ref"], f"{item_location}.decision_ref")
    if len(candidate_ids) != len(set(candidate_ids)):
        raise RatchetContractError(f"{location} contains duplicate candidate IDs")


def reconcile_audit_round_dispositions(
    rounds: Sequence[Mapping[str, Any]],
    *,
    segment_ids: Sequence[str],
    current_challenger_dispositions: Sequence[Mapping[str, Any]],
) -> list[dict[str, Any]]:
    """Validate candidate identity while preserving historical dispositions."""

    expected_segments = _segment_ids(segment_ids)
    if isinstance(rounds, (str, bytes)) or not isinstance(rounds, Sequence):
        raise RatchetContractError("rounds must be a sequence")
    if isinstance(current_challenger_dispositions, (str, bytes)) or not isinstance(
        current_challenger_dispositions, Sequence
    ):
        raise RatchetContractError("current_challenger_dispositions must be a sequence")
    current = list(current_challenger_dispositions)
    _validate_challenger_dispositions(current, "current_challenger_dispositions")
    current_ids = {record["candidate_id"] for record in current}
    if not current_ids:
        raise RatchetContractError("current_challenger_dispositions must not be empty")

    reconciled = []
    for value in rounds:
        record = validate_audit_round(value, segment_ids=expected_segments)
        historical_ids = {
            item["candidate_id"] for item in record["challenger_dispositions"]
        }
        if historical_ids != current_ids:
            raise RatchetContractError(
                f"audit round {record['round_id']} challenger IDs must exactly match "
                "the current generated decisions"
            )
        reconciled.append(record)
    validate_audit_finding_identity(reconciled)
    return reconciled


def validate_audit_finding_identity(
    rounds: Sequence[Mapping[str, Any]],
) -> None:
    """Require each issue identity to occur once across the full audit history."""

    occurrences: dict[str, list[str]] = {}
    for round_record in rounds:
        round_id = str(round_record["round_id"])
        for report in round_record["audit_reports"]:
            for finding in report["findings"]:
                occurrences.setdefault(finding["finding_id"], []).append(round_id)
    duplicates = {
        finding_id: round_ids
        for finding_id, round_ids in occurrences.items()
        if len(round_ids) != 1
    }
    if duplicates:
        details = ", ".join(
            f"{finding_id!r} in {round_ids!r}"
            for finding_id, round_ids in sorted(duplicates.items())
        )
        raise RatchetContractError(
            f"audit finding IDs must be globally unique across rounds; {details}"
        )


def validate_audit_round(
    round_record: Mapping[str, Any], *, segment_ids: Sequence[str]
) -> dict[str, Any]:
    """Validate a complete audit-round record without mutating caller data."""

    expected_segments = _segment_ids(segment_ids)
    expected_evaluations = canonical_evaluation_ids(expected_segments)
    expected_transitions = canonical_transition_ids(expected_segments)
    round_record = _mapping(round_record, "audit_round")
    _exact_keys_with_optional(
        round_record,
        _ROUND_FIELDS,
        _OPTIONAL_ROUND_FIELDS,
        "audit_round",
    )
    _string(round_record["round_id"], "audit_round.round_id")
    if "audit_subject_sha256" in round_record:
        _sha256(
            round_record["audit_subject_sha256"],
            "audit_round.audit_subject_sha256",
        )
    _integer(round_record["sequence"], "audit_round.sequence", positive=True)
    status = _string(round_record["status"], "audit_round.status")
    if status not in ROUND_STATUSES:
        raise RatchetContractError(f"unsupported audit round status {status!r}")
    loop_speed = _string(round_record["loop_speed"], "audit_round.loop_speed")
    if loop_speed not in LOOP_SPEEDS:
        raise RatchetContractError(f"unsupported loop speed {loop_speed!r}")

    reports = _list(round_record["audit_reports"], "audit_round.audit_reports")
    if len(reports) != len(AUDIT_ROLES):
        raise RatchetContractError(
            f"audit_round.audit_reports must contain exactly {len(AUDIT_ROLES)} reports"
        )
    roles: list[str] = []
    auditor_ids: list[str] = []
    report_statuses: list[str] = []
    finding_ids: set[str] = set()
    findings: list[Mapping[str, Any]] = []
    for index, report_value in enumerate(reports):
        location = f"audit_round.audit_reports[{index}]"
        report = _mapping(report_value, location)
        _exact_keys(report, _REPORT_FIELDS, location)
        role = _string(report["role"], f"{location}.role")
        if role not in AUDIT_ROLES:
            raise RatchetContractError(f"unsupported audit role {role!r}")
        roles.append(role)
        auditor_ids.append(_string(report["auditor_id"], f"{location}.auditor_id"))
        report_status = _string(report["status"], f"{location}.status")
        if report_status not in REPORT_STATUSES:
            raise RatchetContractError(
                f"unsupported audit report status {report_status!r}"
            )
        report_statuses.append(report_status)
        evidence_ref = report["evidence_ref"]
        if report_status == "complete":
            _string(evidence_ref, f"{location}.evidence_ref")
        elif evidence_ref is not None:
            raise RatchetContractError(
                f"{location}.evidence_ref must be null while the report is pending"
            )
        _validate_exact_ordered_ids(
            report["segment_ids"],
            expected=expected_segments,
            location=f"{location}.segment_ids",
        )
        _validate_exact_ordered_ids(
            report["viewport_ids"],
            expected=CANONICAL_VIEWPORT_IDS,
            location=f"{location}.viewport_ids",
        )
        _validate_exact_ordered_ids(
            report["evaluation_ids"],
            expected=expected_evaluations,
            location=f"{location}.evaluation_ids",
        )
        _validate_exact_ordered_ids(
            report["transition_ids"],
            expected=expected_transitions,
            location=f"{location}.transition_ids",
        )
        report_findings = _list(report["findings"], f"{location}.findings")
        for finding_index, finding_value in enumerate(report_findings):
            finding_location = f"{location}.findings[{finding_index}]"
            finding = _validate_finding(
                finding_value,
                segment_ids=expected_segments,
                location=finding_location,
            )
            finding_id = finding["finding_id"]
            if finding_id in finding_ids:
                raise RatchetContractError(f"duplicate audit finding ID {finding_id!r}")
            finding_ids.add(finding_id)
            findings.append(finding)
    if set(roles) != set(AUDIT_ROLES) or len(roles) != len(set(roles)):
        raise RatchetContractError(
            "audit_round.audit_reports must contain each required role exactly once"
        )
    if len(auditor_ids) != len(set(auditor_ids)):
        raise RatchetContractError(
            "audit roles must be performed by independent auditor IDs"
        )
    reports_complete = all(item == "complete" for item in report_statuses)
    if (status == "complete") != reports_complete:
        raise RatchetContractError(
            "audit round status must be complete exactly when all role reports are complete"
        )

    selected_finding_id = round_record["selected_finding_id"]
    if not findings:
        if selected_finding_id is not None:
            raise RatchetContractError(
                "audit_round.selected_finding_id must be null when there are no findings"
            )
    else:
        selected_finding_id = _string(
            selected_finding_id, "audit_round.selected_finding_id"
        )
        by_id = {finding["finding_id"]: finding for finding in findings}
        if selected_finding_id not in by_id:
            raise RatchetContractError(
                "audit_round.selected_finding_id must reference a round finding"
            )
        maximum = max(float(finding["priority_score"]) for finding in findings)
        if float(by_id[selected_finding_id]["priority_score"]) != maximum:
            raise RatchetContractError(
                "audit_round.selected_finding_id must select a highest-priority finding"
            )

    scopes = _unique_strings(round_record["change_scopes"], "audit_round.change_scopes")
    decisions_value = _list(
        round_record["consultation_decisions"],
        "audit_round.consultation_decisions",
    )
    decisions = [validate_consultation_decision(item) for item in decisions_value]
    decision_ids = [item["decision_id"] for item in decisions]
    decision_scopes = [item["scope"] for item in decisions]
    if len(decision_ids) != len(set(decision_ids)):
        raise RatchetContractError(
            "audit_round.consultation_decisions contains duplicate decision IDs"
        )
    if len(decision_scopes) != len(set(decision_scopes)):
        raise RatchetContractError(
            "audit_round.consultation_decisions contains duplicate scopes"
        )
    authorized_scopes = {
        item["scope"] for item in decisions if item["disposition"] == "authorized"
    }
    restricted_changes = set(scopes) & RESTRICTED_CHANGE_SCOPES
    if not restricted_changes <= authorized_scopes:
        raise RatchetContractError(
            "restricted change scopes require matching authorized consultation decisions"
        )

    allowed_scopes = (
        FAST_CHANGE_SCOPES if loop_speed == "fast" else SLOW_CHANGE_SCOPES
    ) | RESTRICTED_CHANGE_SCOPES
    unknown_scopes = set(scopes) - allowed_scopes
    if unknown_scopes:
        raise RatchetContractError(
            f"audit_round.change_scopes are invalid for {loop_speed} loop: "
            f"{sorted(unknown_scopes)}"
        )
    trigger = round_record["research_trigger"]
    if loop_speed == "fast":
        if trigger is not None:
            raise RatchetContractError(
                "fast audit rounds must not carry a primary-source research trigger"
            )
    else:
        if "primary_source_research" not in scopes:
            raise RatchetContractError(
                "slow audit rounds must include primary_source_research"
            )
        _validate_research_trigger(
            trigger,
            finding_ids=finding_ids,
            location="audit_round.research_trigger",
        )

    _validate_challenger_dispositions(
        round_record["challenger_dispositions"],
        "audit_round.challenger_dispositions",
    )
    return copy.deepcopy(dict(round_record))


def _validate_gate_group(
    value: Any, *, gate_ids: tuple[str, ...], location: str
) -> tuple[str, list[str]]:
    evidence = _mapping(value, location)
    _exact_keys(evidence, set(gate_ids), location)
    statuses: list[str] = []
    reasons: list[str] = []
    for gate_id in gate_ids:
        gate_location = f"{location}.{gate_id}"
        record = _mapping(evidence[gate_id], gate_location)
        _exact_keys(record, {"status", "evidence_ref"}, gate_location)
        status = _string(record["status"], f"{gate_location}.status")
        if status not in GATE_STATUSES:
            raise RatchetContractError(f"unsupported gate status {status!r}")
        statuses.append(status)
        evidence_ref = record["evidence_ref"]
        if status in {"passed", "failed"}:
            _string(evidence_ref, f"{gate_location}.evidence_ref")
        elif evidence_ref is not None:
            raise RatchetContractError(
                f"{gate_location}.evidence_ref must be null while pending"
            )
        if status != "passed":
            reasons.append(f"{location}:{gate_id}:{status}")
    if "failed" in statuses:
        return "failed", reasons
    if "pending" in statuses:
        return "pending", reasons
    return "passed", reasons


def _required_protection_members(
    value: Mapping[str, Sequence[str]],
) -> dict[str, tuple[str, ...]]:
    value = _mapping(value, "required_protection_members")
    _exact_keys(value, set(PROTECTION_COHORTS), "required_protection_members")
    result: dict[str, tuple[str, ...]] = {}
    for cohort in PROTECTION_COHORTS:
        members = value[cohort]
        if isinstance(members, (str, bytes)) or not isinstance(members, Sequence):
            raise RatchetContractError(
                f"required_protection_members.{cohort} must be a sequence"
            )
        normalized = [
            _string(item, f"required_protection_members.{cohort}[{index}]")
            for index, item in enumerate(members)
        ]
        if not normalized:
            raise RatchetContractError(
                f"required_protection_members.{cohort} must not be empty"
            )
        if len(normalized) != len(set(normalized)):
            raise RatchetContractError(
                f"required_protection_members.{cohort} contains duplicate IDs"
            )
        result[cohort] = tuple(normalized)
    return result


def pareto_decision(
    candidate: Mapping[str, Any],
    *,
    required_protection_members: Mapping[str, Sequence[str]],
    required_modeled_gate_ids: Sequence[str],
) -> dict[str, Any]:
    """Derive accepted, rejected, or pending from a complete Pareto record."""

    expected_members = _required_protection_members(required_protection_members)
    candidate = _mapping(candidate, "pareto_candidate")
    expected_fields = {
        "candidate_id",
        "target",
        "modeled_gate_evidence",
        "protection_evidence",
        "static_gate_evidence",
        "live_gate_evidence",
        "blind_reviews",
    }
    _exact_keys(candidate, expected_fields, "pareto_candidate")
    candidate_id = _string(candidate["candidate_id"], "pareto_candidate.candidate_id")

    target = _mapping(candidate["target"], "pareto_candidate.target")
    _exact_keys(
        target,
        {
            "dimension_id",
            "direction",
            "champion_value",
            "candidate_value",
            "minimum_material_improvement",
            "evidence_ref",
        },
        "pareto_candidate.target",
    )
    dimension_id = _string(
        target["dimension_id"], "pareto_candidate.target.dimension_id"
    )
    direction = _string(target["direction"], "pareto_candidate.target.direction")
    if direction not in {"increase", "decrease"}:
        raise RatchetContractError(f"unsupported target direction {direction!r}")
    champion_value = _decimal(
        target["champion_value"], "pareto_candidate.target.champion_value"
    )
    candidate_value = _decimal(
        target["candidate_value"], "pareto_candidate.target.candidate_value"
    )
    minimum = _positive_decimal(
        target["minimum_material_improvement"],
        "pareto_candidate.target.minimum_material_improvement",
    )
    _string(target["evidence_ref"], "pareto_candidate.target.evidence_ref")
    delta = (
        candidate_value - champion_value
        if direction == "increase"
        else champion_value - candidate_value
    )
    material_passed = delta >= minimum

    if isinstance(required_modeled_gate_ids, (str, bytes)) or not isinstance(
        required_modeled_gate_ids, Sequence
    ):
        raise RatchetContractError("required_modeled_gate_ids must be a sequence")
    modeled_gate_ids = [
        _string(item, f"required_modeled_gate_ids[{index}]")
        for index, item in enumerate(required_modeled_gate_ids)
    ]
    if not modeled_gate_ids:
        raise RatchetContractError("required_modeled_gate_ids must not be empty")
    if len(modeled_gate_ids) != len(set(modeled_gate_ids)):
        raise RatchetContractError(
            "required_modeled_gate_ids must not contain duplicate IDs"
        )
    modeled_status, modeled_reasons = _validate_gate_group(
        candidate["modeled_gate_evidence"],
        gate_ids=tuple(modeled_gate_ids),
        location="modeled_gate_evidence",
    )

    protection = _mapping(
        candidate["protection_evidence"], "pareto_candidate.protection_evidence"
    )
    _exact_keys(
        protection, set(PROTECTION_COHORTS), "pareto_candidate.protection_evidence"
    )
    regression_counts: dict[str, int] = {}
    for cohort in PROTECTION_COHORTS:
        records = _list(
            protection[cohort], f"pareto_candidate.protection_evidence.{cohort}"
        )
        seen: list[str] = []
        regression_count = 0
        for index, value in enumerate(records):
            location = f"pareto_candidate.protection_evidence.{cohort}[{index}]"
            record = _mapping(value, location)
            _exact_keys(record, {"member_id", "regressed", "evidence_ref"}, location)
            seen.append(_string(record["member_id"], f"{location}.member_id"))
            if _boolean(record["regressed"], f"{location}.regressed"):
                regression_count += 1
            _string(record["evidence_ref"], f"{location}.evidence_ref")
        if len(seen) != len(set(seen)):
            raise RatchetContractError(
                f"pareto_candidate.protection_evidence.{cohort} has duplicate members"
            )
        if set(seen) != set(expected_members[cohort]) or len(seen) != len(
            expected_members[cohort]
        ):
            raise RatchetContractError(
                f"pareto_candidate.protection_evidence.{cohort} must cover every "
                "required member exactly"
            )
        regression_counts[cohort] = regression_count
    regression_free = not any(regression_counts.values())

    static_status, static_reasons = _validate_gate_group(
        candidate["static_gate_evidence"],
        gate_ids=STATIC_GATE_IDS,
        location="static_gate_evidence",
    )
    live_status, live_reasons = _validate_gate_group(
        candidate["live_gate_evidence"],
        gate_ids=LIVE_GATE_IDS,
        location="live_gate_evidence",
    )

    reviews = _list(candidate["blind_reviews"], "pareto_candidate.blind_reviews")
    if len(reviews) != 3:
        raise RatchetContractError(
            "pareto_candidate.blind_reviews must contain exactly three reviews"
        )
    reviewer_ids: list[str] = []
    preferences: list[str] = []
    all_blind = True
    for index, value in enumerate(reviews):
        location = f"pareto_candidate.blind_reviews[{index}]"
        review = _mapping(value, location)
        _exact_keys(
            review,
            {"reviewer_id", "blind", "preference", "evidence_ref"},
            location,
        )
        reviewer_ids.append(_string(review["reviewer_id"], f"{location}.reviewer_id"))
        all_blind = _boolean(review["blind"], f"{location}.blind") and all_blind
        preference = _string(review["preference"], f"{location}.preference")
        if preference not in REVIEW_PREFERENCES:
            raise RatchetContractError(f"unsupported review preference {preference!r}")
        preferences.append(preference)
        evidence_ref = review["evidence_ref"]
        if preference == "pending":
            if evidence_ref is not None:
                raise RatchetContractError(
                    f"{location}.evidence_ref must be null while pending"
                )
        else:
            _string(evidence_ref, f"{location}.evidence_ref")
    if len(reviewer_ids) != len(set(reviewer_ids)):
        raise RatchetContractError(
            "blind review requires three independent reviewer IDs"
        )
    candidate_preferences = preferences.count("candidate")
    pending_reviews = preferences.count("pending")
    if not all_blind or candidate_preferences + pending_reviews < 2:
        review_status = "failed"
    elif pending_reviews:
        review_status = "pending"
    elif candidate_preferences >= 2:
        review_status = "passed"
    else:
        review_status = "failed"

    rejection_reasons: list[str] = []
    pending_reasons: list[str] = []
    if not material_passed:
        rejection_reasons.append("target_not_materially_improved")
    if modeled_status == "failed":
        rejection_reasons.extend(
            reason for reason in modeled_reasons if reason.endswith(":failed")
        )
    elif modeled_status == "pending":
        pending_reasons.extend(
            reason for reason in modeled_reasons if reason.endswith(":pending")
        )
    for cohort in PROTECTION_COHORTS:
        if regression_counts[cohort]:
            rejection_reasons.append(f"regression:{cohort}")
    for status, reasons in (
        (static_status, static_reasons),
        (live_status, live_reasons),
    ):
        if status == "failed":
            rejection_reasons.extend(
                reason for reason in reasons if reason.endswith(":failed")
            )
        elif status == "pending":
            pending_reasons.extend(
                reason for reason in reasons if reason.endswith(":pending")
            )
    if review_status == "failed":
        rejection_reasons.append(
            "blind_review_protocol_failed"
            if not all_blind
            else "blind_preference_threshold_failed"
        )
    elif review_status == "pending":
        pending_reasons.append("blind_review:pending")

    if rejection_reasons:
        disposition = "rejected"
        reasons = rejection_reasons + pending_reasons
    elif pending_reasons:
        disposition = "pending"
        reasons = pending_reasons
    else:
        disposition = "accepted"
        reasons = []
    return {
        "candidate_id": candidate_id,
        "disposition": disposition,
        "material_improvement": {
            "dimension_id": dimension_id,
            "direction": direction,
            "delta": float(delta),
            "minimum_required": float(minimum),
            "passed": material_passed,
        },
        "regression_free": regression_free,
        "regression_counts": regression_counts,
        "modeled_gate_status": modeled_status,
        "static_gate_status": static_status,
        "live_gate_status": live_status,
        "blind_review": {
            "status": review_status,
            "candidate_preferences": candidate_preferences,
            "reviewer_count": len(reviews),
            "required_preferences": 2,
        },
        "reasons": reasons,
    }


def validate_pareto_result(result: Mapping[str, Any]) -> dict[str, Any]:
    """Validate that a serialized Pareto result agrees with its own evidence."""

    location = "pareto_result"
    result = _mapping(result, location)
    _exact_keys(
        result,
        {
            "candidate_id",
            "disposition",
            "material_improvement",
            "regression_free",
            "regression_counts",
            "modeled_gate_status",
            "static_gate_status",
            "live_gate_status",
            "blind_review",
            "reasons",
        },
        location,
    )
    _string(result["candidate_id"], f"{location}.candidate_id")
    disposition = _string(result["disposition"], f"{location}.disposition")
    if disposition not in DISPOSITIONS:
        raise RatchetContractError(f"unsupported Pareto disposition {disposition!r}")

    material = _mapping(
        result["material_improvement"], f"{location}.material_improvement"
    )
    _exact_keys(
        material,
        {"dimension_id", "direction", "delta", "minimum_required", "passed"},
        f"{location}.material_improvement",
    )
    _string(
        material["dimension_id"],
        f"{location}.material_improvement.dimension_id",
    )
    direction = _string(
        material["direction"], f"{location}.material_improvement.direction"
    )
    if direction not in {"increase", "decrease"}:
        raise RatchetContractError(
            f"unsupported Pareto material direction {direction!r}"
        )
    delta = _decimal(material["delta"], f"{location}.material_improvement.delta")
    minimum = _positive_decimal(
        material["minimum_required"],
        f"{location}.material_improvement.minimum_required",
    )
    material_passed = _boolean(
        material["passed"], f"{location}.material_improvement.passed"
    )
    if material_passed != (delta >= minimum):
        raise RatchetContractError(
            "pareto_result.material_improvement.passed must match its delta and minimum"
        )

    regression_counts = _mapping(
        result["regression_counts"], f"{location}.regression_counts"
    )
    _exact_keys(
        regression_counts,
        set(PROTECTION_COHORTS),
        f"{location}.regression_counts",
    )
    normalized_counts: dict[str, int] = {}
    for cohort in PROTECTION_COHORTS:
        count = _integer(
            regression_counts[cohort],
            f"{location}.regression_counts.{cohort}",
        )
        if count < 0:
            raise RatchetContractError(
                f"{location}.regression_counts.{cohort} must be non-negative"
            )
        normalized_counts[cohort] = count
    regression_free = _boolean(result["regression_free"], f"{location}.regression_free")
    if regression_free != (not any(normalized_counts.values())):
        raise RatchetContractError(
            "pareto_result.regression_free must match its regression counts"
        )

    gate_statuses = []
    for field in ("modeled_gate_status", "static_gate_status", "live_gate_status"):
        status = _string(result[field], f"{location}.{field}")
        if status not in GATE_STATUSES:
            raise RatchetContractError(f"unsupported Pareto {field} {status!r}")
        gate_statuses.append(status)

    blind_review = _mapping(result["blind_review"], f"{location}.blind_review")
    _exact_keys(
        blind_review,
        {"status", "candidate_preferences", "reviewer_count", "required_preferences"},
        f"{location}.blind_review",
    )
    review_status = _string(blind_review["status"], f"{location}.blind_review.status")
    if review_status not in GATE_STATUSES:
        raise RatchetContractError(
            f"unsupported Pareto blind-review status {review_status!r}"
        )
    reviewer_count = _integer(
        blind_review["reviewer_count"],
        f"{location}.blind_review.reviewer_count",
        positive=True,
    )
    required_preferences = _integer(
        blind_review["required_preferences"],
        f"{location}.blind_review.required_preferences",
        positive=True,
    )
    candidate_preferences = _integer(
        blind_review["candidate_preferences"],
        f"{location}.blind_review.candidate_preferences",
    )
    if reviewer_count != 3 or required_preferences != 2:
        raise RatchetContractError("Pareto blind review must require two of three")
    if not 0 <= candidate_preferences <= reviewer_count:
        raise RatchetContractError(
            "pareto_result.blind_review.candidate_preferences is out of range"
        )
    if review_status == "passed" and candidate_preferences < required_preferences:
        raise RatchetContractError(
            "passed Pareto blind review must meet the preference threshold"
        )

    reasons = _unique_strings(result["reasons"], f"{location}.reasons")
    rejection = (
        not material_passed
        or not regression_free
        or "failed" in gate_statuses
        or review_status == "failed"
    )
    pending = "pending" in gate_statuses or review_status == "pending"
    expected_disposition = (
        "rejected" if rejection else ("pending" if pending else "accepted")
    )
    if disposition != expected_disposition:
        raise RatchetContractError(
            "pareto_result.disposition must match its material, regression, gate, "
            "and blind-review evidence"
        )
    if (disposition == "accepted") != (not reasons):
        raise RatchetContractError(
            "accepted Pareto results must have no reasons and unresolved results "
            "must explain their disposition"
        )
    return copy.deepcopy(dict(result))


def evaluate_saturation(
    rounds: Sequence[Mapping[str, Any]],
    *,
    segment_ids: Sequence[str],
    high_priority_threshold: float,
    current_challenger_dispositions: Sequence[Mapping[str, Any]],
    current_audit_subject_sha256: str,
) -> dict[str, Any]:
    """Derive saturation from the two most recent consecutive audit rounds."""

    expected_segments = _segment_ids(segment_ids)
    threshold = _positive_decimal(high_priority_threshold, "high_priority_threshold")
    current_subject = _sha256(
        current_audit_subject_sha256,
        "current_audit_subject_sha256",
    )
    if isinstance(rounds, (str, bytes)) or not isinstance(rounds, Sequence):
        raise RatchetContractError("rounds must be a sequence")
    if isinstance(current_challenger_dispositions, (str, bytes)) or not isinstance(
        current_challenger_dispositions, Sequence
    ):
        raise RatchetContractError("current_challenger_dispositions must be a sequence")
    current = list(current_challenger_dispositions)
    _validate_challenger_dispositions(current, "current_challenger_dispositions")
    validated = reconcile_audit_round_dispositions(
        rounds,
        segment_ids=expected_segments,
        current_challenger_dispositions=current,
    )
    current_dispositions = {item["disposition"] for item in current}
    round_ids = [record["round_id"] for record in validated]
    if len(round_ids) != len(set(round_ids)):
        raise RatchetContractError("rounds must not contain duplicate round IDs")
    sequences = [record["sequence"] for record in validated]
    if any(current <= previous for previous, current in pairwise(sequences)):
        raise RatchetContractError("round sequences must be strictly increasing")

    finding_ids_by_round: dict[str, list[str]] = {}
    high_finding_ids_by_round: dict[str, list[str]] = {}
    for record in validated:
        round_id = record["round_id"]
        round_findings = [
            finding
            for report in record["audit_reports"]
            for finding in report["findings"]
        ]
        finding_ids_by_round[round_id] = [
            finding["finding_id"] for finding in round_findings
        ]
        high_finding_ids_by_round[round_id] = [
            finding["finding_id"]
            for finding in round_findings
            if _decimal(
                finding["priority_score"],
                f"round {round_id} finding priority_score",
            )
            >= threshold
        ]

    reasons: list[str] = []
    qualifying_round_ids: list[str] = []
    terminal = validated[-2:]
    high_finding_ids = [
        finding_id
        for record in terminal
        for finding_id in high_finding_ids_by_round[record["round_id"]]
    ]
    required_coverage = EXPECTED_SEGMENT_COUNT * len(AUDIT_ROLES)
    if len(validated) < 2:
        reasons.append("fewer_than_two_rounds")
    else:
        if terminal[1]["sequence"] != terminal[0]["sequence"] + 1:
            reasons.append("terminal_rounds_not_sequence_consecutive")
    for record in terminal:
        round_id = record["round_id"]
        round_qualifies = True
        if record["status"] != "complete":
            reasons.append(f"round_not_complete:{round_id}")
            round_qualifies = False
        if current_dispositions - {"rejected"}:
            reasons.append(f"admissible_or_pending_improvement:{round_id}")
            round_qualifies = False
        if finding_ids_by_round[round_id]:
            reasons.append(f"findings_remain:{round_id}")
            round_qualifies = False
        audit_subject = record.get("audit_subject_sha256")
        if audit_subject is None:
            reasons.append(f"audit_subject_sha256_missing:{round_id}")
            round_qualifies = False
        elif audit_subject != current_subject:
            reasons.append(f"audit_subject_sha256_mismatch:{round_id}")
            round_qualifies = False
        if round_qualifies:
            qualifying_round_ids.append(round_id)
    if high_finding_ids:
        reasons.append("high_priority_findings_remain")

    saturated = not reasons and len(qualifying_round_ids) == 2
    return {
        "status": "saturated" if saturated else "continue",
        "saturated": saturated,
        "qualifying_round_ids": qualifying_round_ids if saturated else [],
        "required_consecutive_rounds": 2,
        "required_role_segment_coverage_per_round": required_coverage,
        "required_viewport_coverage_per_report": len(CANONICAL_VIEWPORT_IDS),
        "required_evaluation_coverage_per_report": EXPECTED_EVALUATION_COUNT,
        "required_transition_coverage_per_report": EXPECTED_TRANSITION_COUNT,
        "high_priority_threshold": float(threshold),
        "current_audit_subject_sha256": current_subject,
        "current_challenger_dispositions": copy.deepcopy(current),
        "high_finding_ids": sorted(set(high_finding_ids)),
        "reasons": reasons,
    }
