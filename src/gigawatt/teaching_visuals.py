"""Deterministic, evidence-bound teaching visuals for coarse manual states.

This module deliberately does not know about the Abilene master diagram.  It
renders explanatory canvases whose statements bind directly to qualified facts
in registered evidence ledgers.  The generated HTML is self-contained and its
states change only in response to instructor input.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import textwrap
from collections.abc import Iterable, Mapping
from pathlib import Path, PurePosixPath
from typing import Any

import yaml

SCHEMA_VERSION = 1
CANVAS_KIND = "generation_landscape_v1"
CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 900
MIN_STATES = 2
MAX_STATES = 8
SHORT_LANDSCAPE_MAX_HEIGHT = 520
SHORT_LANDSCAPE_MIN_TEXT_PX = 10
PORTRAIT_MAX_WIDTH = 520
PORTRAIT_MIN_TEXT_PX = 12
COMPACT_FAMILY_PATHS = {
    "heat_turbine": ["Fuel / heat", "hot fluid", "turbine", "generator", "AC"],
    "moving_fluid": ["Water / air", "rotor", "generator", "AC"],
    "solar_pv": ["Photons", "PV cell", "DC", "inverter", "AC"],
    "fuel_cell": ["Fuel", "fuel-cell stack", "DC", "conditioning", "AC"],
}
REQUIRED_FAMILY_IDS = set(COMPACT_FAMILY_PATHS)
REQUIRED_DISTINCTION_IDS = {
    "storage_not_primary_source",
    "ppa_not_physical_generator",
    "standby_is_a_role",
}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
LEDGER_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")

TOP_LEVEL_FIELDS = {
    "schema_version",
    "id",
    "title",
    "phase",
    "learning_objective",
    "evidence_files",
    "interaction",
    "canvas",
    "families",
    "distinctions",
    "abilene_case",
    "states",
}
PHASE_FIELDS = {"id", "number", "title", "anchor_question"}
INTERACTION_FIELDS = {"mode", "advance"}
CANVAS_FIELDS = {"kind", "width", "height"}
FAMILY_FIELDS = {"id", "title", "examples", "path", "fact_refs"}
DISTINCTION_FIELDS = {"id", "title", "body", "fact_refs"}
ABILENE_CASE_FIELDS = {"title", "path", "fact_refs", "boundary"}
STATE_FIELDS = {
    "id",
    "title",
    "nav_label",
    "instruction",
    "family_ids",
    "distinction_ids",
    "show_common_bus",
    "show_abilene_case",
    "show_handoff",
}
LEDGER_FIELDS = {
    "schema_version",
    "subject",
    "accessed_as_of",
    "evidence_boundary",
    "sources",
    "facts",
}
SOURCE_REQUIRED_FIELDS = {"publisher", "title", "url", "accessed_as_of"}
FACT_REQUIRED_FIELDS = {
    "value",
    "unit",
    "scope",
    "basis",
    "lifecycle",
    "as_of",
    "source_ids",
    "posture",
}
FORBIDDEN_FIELD_PARTS = {
    "autoplay",
    "beat",
    "beats",
    "cadence",
    "duration",
    "runtime",
    "script",
    "timing",
}


class TeachingVisualError(ValueError):
    """Raised when a teaching visual escapes its authored evidence contract."""


def responsive_layout_contract(
    viewport_width: int,
    viewport_height: int,
) -> dict[str, Any]:
    """Return the deterministic alternate-surface contract for a viewport."""
    if viewport_width <= 0 or viewport_height <= 0:
        raise TeachingVisualError("responsive viewport dimensions must be positive")
    if (
        viewport_height <= SHORT_LANDSCAPE_MAX_HEIGHT
        and viewport_width > viewport_height
    ):
        return {
            "surface": "html",
            "profile": "short_landscape",
            "family_columns": 2,
            "minimum_text_px": SHORT_LANDSCAPE_MIN_TEXT_PX,
            "scroll_axis": "vertical",
        }
    if viewport_width <= PORTRAIT_MAX_WIDTH and viewport_height >= viewport_width:
        return {
            "surface": "html",
            "profile": "portrait",
            "family_columns": 1,
            "minimum_text_px": PORTRAIT_MIN_TEXT_PX,
            "scroll_axis": "vertical",
        }
    return {
        "surface": "svg",
        "profile": "standard",
        "family_columns": 1,
        "minimum_text_px": None,
        "scroll_axis": None,
    }


def short_landscape_family_geometry(
    compact_path: list[str],
    *,
    viewport_width: int = 844,
) -> dict[str, float]:
    """Estimate compact-flow width without relying on a browser renderer."""
    if not compact_path:
        raise TeachingVisualError("compact family path must not be empty")
    usable_width = viewport_width - 14
    card_width = (usable_width - 6) / 2
    inner_width = card_width - 12
    stage_width = sum(max(24.0, len(label) * 5.2 + 8.0) for label in compact_path)
    arrow_width = max(0, len(compact_path) - 1) * 8.0
    return {
        "card_width": card_width,
        "inner_width": inner_width,
        "estimated_flow_width": stage_width + arrow_width,
        "minimum_text_px": float(SHORT_LANDSCAPE_MIN_TEXT_PX),
    }


class _UniqueKeyLoader(yaml.SafeLoader):
    pass


def _construct_unique_mapping(
    loader: _UniqueKeyLoader,
    node: yaml.nodes.MappingNode,
    deep: bool = False,
) -> dict[Any, Any]:
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in mapping:
            raise TeachingVisualError(f"duplicate YAML key {key!r}")
        mapping[key] = loader.construct_object(value_node, deep=deep)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
    _construct_unique_mapping,
)


def load_yaml(path: Path) -> dict[str, Any]:
    """Load one strict YAML mapping with duplicate keys rejected."""
    try:
        value = yaml.load(path.read_text(), Loader=_UniqueKeyLoader)
    except (OSError, yaml.YAMLError) as error:
        raise TeachingVisualError(f"could not load {path}: {error}") from error
    if not isinstance(value, dict):
        raise TeachingVisualError(f"{path}: expected a top-level mapping")
    return value


def _exact_fields(value: Any, expected: set[str], location: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise TeachingVisualError(f"{location}: expected a mapping")
    actual = set(value)
    if actual != expected:
        raise TeachingVisualError(
            f"{location}: fields must be exact; "
            f"missing={sorted(expected - actual)} extra={sorted(actual - expected)}"
        )
    return value


def _text(value: Any, location: str, *, maximum: int = 240) -> str:
    if not isinstance(value, str) or not value.strip():
        raise TeachingVisualError(f"{location}: expected non-empty text")
    normalized = " ".join(value.split())
    if len(normalized) > maximum:
        raise TeachingVisualError(
            f"{location}: text exceeds the {maximum}-character limit"
        )
    return normalized


def _id(value: Any, location: str) -> str:
    result = _text(value, location, maximum=80)
    if not ID_PATTERN.fullmatch(result):
        raise TeachingVisualError(
            f"{location}: expected lowercase snake_case identifier"
        )
    return result


def _unique_text_list(
    value: Any,
    location: str,
    *,
    minimum: int = 0,
    maximum: int = 8,
    item_limit: int = 100,
    unique: bool = True,
) -> list[str]:
    if not isinstance(value, list):
        raise TeachingVisualError(f"{location}: expected a list")
    if not minimum <= len(value) <= maximum:
        raise TeachingVisualError(
            f"{location}: expected {minimum} to {maximum} entries"
        )
    normalized = [
        _text(item, f"{location}[{index}]", maximum=item_limit)
        for index, item in enumerate(value)
    ]
    if unique and len(normalized) != len(set(normalized)):
        raise TeachingVisualError(f"{location}: entries must be unique")
    return normalized


def _evidence_registry(value: Any) -> dict[str, str]:
    if not isinstance(value, dict) or not value:
        raise TeachingVisualError("evidence_files: expected a non-empty mapping")
    normalized: dict[str, str] = {}
    for ledger_id, path in value.items():
        if not isinstance(ledger_id, str) or not LEDGER_ID_PATTERN.fullmatch(ledger_id):
            raise TeachingVisualError(
                f"evidence_files key {ledger_id!r}: expected lowercase snake_case"
            )
        normalized[ledger_id] = _text(path, f"evidence_files.{ledger_id}", maximum=180)
    if len(normalized.values()) != len(set(normalized.values())):
        raise TeachingVisualError("evidence_files paths must be unique")
    return normalized


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def _forbidden_fields(value: Any) -> list[str]:
    forbidden = []
    for key in _walk_keys(value):
        normalized = key.casefold().replace("-", "_")
        parts = set(normalized.split("_"))
        if normalized in FORBIDDEN_FIELD_PARTS or parts & FORBIDDEN_FIELD_PARTS:
            forbidden.append(key)
    return sorted(set(forbidden))


def registered_evidence_paths(
    manifest: Mapping[str, Any],
    *,
    root: Path,
) -> dict[str, Path]:
    """Resolve the manifest's evidence registry without permitting traversal."""
    raw = _evidence_registry(manifest.get("evidence_files"))
    evidence_root = (root / "evidence").resolve()
    resolved: dict[str, Path] = {}
    seen_paths: set[Path] = set()
    for ledger_id, value in raw.items():
        relative = value
        posix = PurePosixPath(relative)
        if posix.is_absolute() or posix.suffix != ".yaml" or ".." in posix.parts:
            raise TeachingVisualError(
                f"evidence_files.{ledger_id}: expected a relative YAML path under evidence/"
            )
        path = (root / Path(*posix.parts)).resolve()
        if not path.is_relative_to(evidence_root):
            raise TeachingVisualError(
                f"evidence_files.{ledger_id}: path must remain under evidence/"
            )
        if path in seen_paths:
            raise TeachingVisualError("evidence_files paths must be unique")
        seen_paths.add(path)
        resolved[ledger_id] = path
    return resolved


def source_digest(root: Path, paths: Iterable[Path]) -> str:
    """Hash a deterministic, root-relative set of teaching-pilot inputs."""
    root = root.resolve()
    digest = hashlib.sha256()
    seen: set[Path] = set()
    for candidate in paths:
        path = candidate.resolve()
        if path in seen:
            continue
        if not path.is_relative_to(root):
            raise TeachingVisualError(f"digest path must remain under {root}: {path}")
        seen.add(path)
        digest.update(path.relative_to(root).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _validate_ledger(ledger_id: str, ledger: Any) -> dict[str, Any]:
    location = f"evidence ledger {ledger_id}"
    ledger = _exact_fields(ledger, LEDGER_FIELDS, location)
    if type(ledger["schema_version"]) is not int or ledger["schema_version"] != 1:
        raise TeachingVisualError(f"{location}.schema_version must be 1")
    _text(ledger["accessed_as_of"], f"{location}.accessed_as_of", maximum=40)
    if not isinstance(ledger["subject"], dict) or not ledger["subject"]:
        raise TeachingVisualError(f"{location}.subject: expected a non-empty mapping")
    if (
        not isinstance(ledger["evidence_boundary"], dict)
        or not ledger["evidence_boundary"]
    ):
        raise TeachingVisualError(
            f"{location}.evidence_boundary: expected a non-empty mapping"
        )
    sources = ledger["sources"]
    facts = ledger["facts"]
    if not isinstance(sources, dict) or not sources:
        raise TeachingVisualError(f"{location}.sources: expected a non-empty mapping")
    if not isinstance(facts, dict) or not facts:
        raise TeachingVisualError(f"{location}.facts: expected a non-empty mapping")

    for source_id, source in sources.items():
        _id(source_id, f"{location}.sources key")
        if not isinstance(source, dict):
            raise TeachingVisualError(
                f"{location}.sources.{source_id}: expected mapping"
            )
        missing = SOURCE_REQUIRED_FIELDS - set(source)
        if missing:
            raise TeachingVisualError(
                f"{location}.sources.{source_id}: missing {sorted(missing)}"
            )
        for field in SOURCE_REQUIRED_FIELDS:
            _text(source[field], f"{location}.sources.{source_id}.{field}", maximum=500)
        if not str(source["url"]).startswith(("https://", "http://")):
            raise TeachingVisualError(
                f"{location}.sources.{source_id}.url must be HTTP(S)"
            )

    for fact_id, fact in facts.items():
        _id(fact_id, f"{location}.facts key")
        if not isinstance(fact, dict):
            raise TeachingVisualError(f"{location}.facts.{fact_id}: expected mapping")
        missing = FACT_REQUIRED_FIELDS - set(fact)
        if missing:
            raise TeachingVisualError(
                f"{location}.facts.{fact_id}: missing {sorted(missing)}"
            )
        for field in ("scope", "basis", "lifecycle", "as_of", "posture"):
            _text(fact[field], f"{location}.facts.{fact_id}.{field}", maximum=1200)
        source_ids = _unique_text_list(
            fact["source_ids"],
            f"{location}.facts.{fact_id}.source_ids",
            minimum=1,
            maximum=12,
            item_limit=80,
        )
        unknown = sorted(set(source_ids) - set(sources))
        if unknown:
            raise TeachingVisualError(
                f"{location}.facts.{fact_id}: unknown source IDs {unknown}"
            )
    return ledger


def _fact_refs(
    value: Any,
    location: str,
    ledgers: Mapping[str, dict[str, Any]],
) -> list[str]:
    refs = _unique_text_list(
        value,
        location,
        minimum=1,
        maximum=12,
        item_limit=160,
    )
    for ref in refs:
        if ref.count(":") != 1:
            raise TeachingVisualError(f"{location}: unqualified fact reference {ref!r}")
        ledger_id, fact_id = ref.split(":", 1)
        if ledger_id not in ledgers:
            raise TeachingVisualError(
                f"{location}: unregistered evidence ledger {ledger_id!r}"
            )
        if fact_id not in ledgers[ledger_id]["facts"]:
            raise TeachingVisualError(f"{location}: unknown fact reference {ref!r}")
    return refs


def validate_source_digest(value: Any) -> str:
    """Validate the lowercase SHA-256 value embedded in a teaching payload."""
    if not isinstance(value, str) or not re.fullmatch(r"[0-9a-f]{64}", value):
        raise TeachingVisualError("source_digest must be a lowercase SHA-256 digest")
    return value


def validate_manual_interaction(value: Any, *, location: str) -> dict[str, str]:
    """Validate the shared manual, instructor-controlled interaction contract."""
    interaction = _exact_fields(value, INTERACTION_FIELDS, location)
    expected = {"mode": "manual", "advance": "instructor_controlled"}
    if interaction != expected:
        raise TeachingVisualError(
            f"{location} must be manual and instructor_controlled"
        )
    return dict(interaction)


def validate_evidence_ledgers(
    manifest: Mapping[str, Any],
    evidence_ledgers: Mapping[str, dict[str, Any]],
) -> tuple[dict[str, str], dict[str, dict[str, Any]]]:
    """Validate the exact evidence registry and every source-bound ledger."""
    declared_ledgers = _evidence_registry(manifest.get("evidence_files"))
    if set(evidence_ledgers) != set(declared_ledgers):
        raise TeachingVisualError(
            "loaded evidence ledgers must exactly match evidence_files; "
            f"missing={sorted(set(declared_ledgers) - set(evidence_ledgers))} "
            f"extra={sorted(set(evidence_ledgers) - set(declared_ledgers))}"
        )
    ledgers = {
        ledger_id: _validate_ledger(ledger_id, ledger)
        for ledger_id, ledger in evidence_ledgers.items()
    }
    return declared_ledgers, ledgers


def compile_evidence_cards(
    fact_refs: Iterable[str],
    ledgers: Mapping[str, dict[str, Any]],
    *,
    ledger_ids: Iterable[str],
) -> dict[str, Any]:
    """Build the shared fact/source payload for an evidence-bound visual."""
    fact_cards = []
    used_source_refs: set[str] = set()
    for ref in sorted(set(fact_refs)):
        if ref.count(":") != 1:
            raise TeachingVisualError(f"unqualified fact reference {ref!r}")
        ledger_id, fact_id = ref.split(":", 1)
        if ledger_id not in ledgers:
            raise TeachingVisualError(
                f"unregistered evidence ledger {ledger_id!r} in compiled facts"
            )
        if fact_id not in ledgers[ledger_id]["facts"]:
            raise TeachingVisualError(f"unknown fact reference {ref!r}")
        fact = ledgers[ledger_id]["facts"][fact_id]
        source_refs = [f"{ledger_id}:{source_id}" for source_id in fact["source_ids"]]
        used_source_refs.update(source_refs)
        fact_cards.append(
            {
                "ref": ref,
                "value": fact["value"],
                "unit": fact["unit"],
                "scope": fact["scope"],
                "basis": fact["basis"],
                "lifecycle": fact["lifecycle"],
                "as_of": fact["as_of"],
                "posture": fact["posture"],
                "source_refs": source_refs,
            }
        )
    source_cards = []
    for ref in sorted(used_source_refs):
        ledger_id, source_id = ref.split(":", 1)
        source = ledgers[ledger_id]["sources"][source_id]
        source_cards.append(
            {
                "ref": ref,
                "publisher": source["publisher"],
                "title": source["title"],
                "url": source["url"],
                "accessed_as_of": source["accessed_as_of"],
            }
        )
    return {
        "ledger_ids": list(ledger_ids),
        "facts": fact_cards,
        "sources": source_cards,
    }


def compile_generation_landscape(
    manifest: dict[str, Any],
    evidence_ledgers: Mapping[str, dict[str, Any]],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Validate and normalize the generation-landscape teaching payload."""
    manifest = _exact_fields(manifest, TOP_LEVEL_FIELDS, "pilot manifest")
    forbidden = _forbidden_fields(manifest)
    if forbidden:
        raise TeachingVisualError(
            f"pilot manifest contains pacing or scripting fields: {forbidden}"
        )
    if type(manifest["schema_version"]) is not int or manifest["schema_version"] != 1:
        raise TeachingVisualError("pilot manifest schema_version must be 1")
    pilot_id = _id(manifest["id"], "pilot manifest.id")
    title = _text(manifest["title"], "pilot manifest.title", maximum=120)
    objective = _text(
        manifest["learning_objective"],
        "pilot manifest.learning_objective",
        maximum=360,
    )
    source_digest = validate_source_digest(source_digest)

    declared_ledgers, ledgers = validate_evidence_ledgers(manifest, evidence_ledgers)

    phase = _exact_fields(manifest["phase"], PHASE_FIELDS, "pilot manifest.phase")
    phase_id = _id(phase["id"], "pilot manifest.phase.id")
    if type(phase["number"]) is not int or phase["number"] != 1:
        raise TeachingVisualError("pilot manifest.phase.number must be integer 1")
    phase_title = _text(phase["title"], "pilot manifest.phase.title", maximum=100)
    anchor_question = _text(
        phase["anchor_question"],
        "pilot manifest.phase.anchor_question",
        maximum=220,
    )

    interaction = validate_manual_interaction(
        manifest["interaction"], location="pilot manifest.interaction"
    )
    canvas = _exact_fields(manifest["canvas"], CANVAS_FIELDS, "pilot manifest.canvas")
    if canvas["kind"] != CANVAS_KIND:
        raise TeachingVisualError(f"pilot manifest.canvas.kind must be {CANVAS_KIND!r}")
    if canvas["width"] != CANVAS_WIDTH or canvas["height"] != CANVAS_HEIGHT:
        raise TeachingVisualError(
            f"pilot manifest.canvas must be {CANVAS_WIDTH} by {CANVAS_HEIGHT}"
        )

    raw_families = manifest["families"]
    if not isinstance(raw_families, list) or len(raw_families) != 4:
        raise TeachingVisualError(
            "pilot manifest.families must contain exactly four families"
        )
    families = []
    family_ids = []
    for index, raw in enumerate(raw_families):
        location = f"pilot manifest.families[{index}]"
        family = _exact_fields(raw, FAMILY_FIELDS, location)
        family_id = _id(family["id"], f"{location}.id")
        family_ids.append(family_id)
        families.append(
            {
                "id": family_id,
                "title": _text(family["title"], f"{location}.title", maximum=100),
                "examples": _unique_text_list(
                    family["examples"],
                    f"{location}.examples",
                    minimum=1,
                    maximum=8,
                    item_limit=60,
                ),
                "path": _unique_text_list(
                    family["path"],
                    f"{location}.path",
                    minimum=2,
                    maximum=6,
                    item_limit=70,
                    unique=False,
                ),
                "compact_path": list(COMPACT_FAMILY_PATHS.get(family_id, [])),
                "fact_refs": _fact_refs(
                    family["fact_refs"], f"{location}.fact_refs", ledgers
                ),
            }
        )
    if len(family_ids) != len(set(family_ids)):
        raise TeachingVisualError("pilot manifest family IDs must be unique")
    if set(family_ids) != REQUIRED_FAMILY_IDS:
        raise TeachingVisualError(
            "pilot manifest families must be the thermal, moving-fluid, "
            "photovoltaic, and fuel-cell teaching set"
        )
    for family in families:
        if len(family["path"]) != len(family["compact_path"]):
            raise TeachingVisualError(
                f"pilot manifest family {family['id']!r} path must contain "
                f"{len(family['compact_path'])} stages for the compact layout"
            )

    raw_distinctions = manifest["distinctions"]
    if not isinstance(raw_distinctions, list) or not 2 <= len(raw_distinctions) <= 6:
        raise TeachingVisualError(
            "pilot manifest.distinctions must contain two to six distinctions"
        )
    distinctions = []
    distinction_ids = []
    for index, raw in enumerate(raw_distinctions):
        location = f"pilot manifest.distinctions[{index}]"
        distinction = _exact_fields(raw, DISTINCTION_FIELDS, location)
        distinction_id = _id(distinction["id"], f"{location}.id")
        distinction_ids.append(distinction_id)
        distinctions.append(
            {
                "id": distinction_id,
                "title": _text(distinction["title"], f"{location}.title", maximum=100),
                "body": _text(distinction["body"], f"{location}.body", maximum=360),
                "fact_refs": _fact_refs(
                    distinction["fact_refs"], f"{location}.fact_refs", ledgers
                ),
            }
        )
    if len(distinction_ids) != len(set(distinction_ids)):
        raise TeachingVisualError("pilot manifest distinction IDs must be unique")
    if set(distinction_ids) != REQUIRED_DISTINCTION_IDS:
        raise TeachingVisualError(
            "pilot manifest distinctions must be the storage, PPA, and standby "
            "teaching set"
        )

    raw_case = _exact_fields(
        manifest["abilene_case"], ABILENE_CASE_FIELDS, "pilot manifest.abilene_case"
    )
    abilene_case = {
        "title": _text(
            raw_case["title"], "pilot manifest.abilene_case.title", maximum=120
        ),
        "path": _unique_text_list(
            raw_case["path"],
            "pilot manifest.abilene_case.path",
            minimum=2,
            maximum=7,
            item_limit=80,
            unique=False,
        ),
        "fact_refs": _fact_refs(
            raw_case["fact_refs"], "pilot manifest.abilene_case.fact_refs", ledgers
        ),
        "boundary": _text(
            raw_case["boundary"],
            "pilot manifest.abilene_case.boundary",
            maximum=500,
        ),
    }

    raw_states = manifest["states"]
    if (
        not isinstance(raw_states, list)
        or not MIN_STATES <= len(raw_states) <= MAX_STATES
    ):
        raise TeachingVisualError(
            f"pilot manifest.states must contain {MIN_STATES} to {MAX_STATES} states"
        )
    states = []
    state_ids = []
    nav_labels = []
    used_families: set[str] = set()
    used_distinctions: set[str] = set()
    for index, raw in enumerate(raw_states):
        location = f"pilot manifest.states[{index}]"
        state = _exact_fields(raw, STATE_FIELDS, location)
        state_id = _id(state["id"], f"{location}.id")
        state_ids.append(state_id)
        nav_label = _text(state["nav_label"], f"{location}.nav_label", maximum=24)
        nav_labels.append(nav_label)
        selected_families = _unique_text_list(
            state["family_ids"],
            f"{location}.family_ids",
            minimum=0,
            maximum=len(families),
            item_limit=80,
        )
        selected_distinctions = _unique_text_list(
            state["distinction_ids"],
            f"{location}.distinction_ids",
            minimum=0,
            maximum=len(distinctions),
            item_limit=80,
        )
        unknown_families = sorted(set(selected_families) - set(family_ids))
        unknown_distinctions = sorted(set(selected_distinctions) - set(distinction_ids))
        if unknown_families or unknown_distinctions:
            raise TeachingVisualError(
                f"{location}: unknown families={unknown_families} "
                f"distinctions={unknown_distinctions}"
            )
        flags = {}
        for field in ("show_common_bus", "show_abilene_case", "show_handoff"):
            if not isinstance(state[field], bool):
                raise TeachingVisualError(f"{location}.{field} must be boolean")
            flags[field] = state[field]
        if (
            not selected_families
            and not selected_distinctions
            and not any(flags.values())
        ):
            raise TeachingVisualError(f"{location}: state must reveal teaching content")
        used_families.update(selected_families)
        used_distinctions.update(selected_distinctions)
        states.append(
            {
                "id": state_id,
                "title": _text(state["title"], f"{location}.title", maximum=120),
                "nav_label": nav_label,
                "instruction": _text(
                    state["instruction"], f"{location}.instruction", maximum=420
                ),
                "family_ids": selected_families,
                "distinction_ids": selected_distinctions,
                **flags,
            }
        )
    if len(state_ids) != len(set(state_ids)):
        raise TeachingVisualError("pilot manifest state IDs must be unique")
    if len(nav_labels) != len(set(nav_labels)):
        raise TeachingVisualError("pilot manifest state nav labels must be unique")
    if used_families != set(family_ids) or used_distinctions != set(distinction_ids):
        raise TeachingVisualError(
            "pilot states must use every authored family and distinction; "
            f"missing_families={sorted(set(family_ids) - used_families)} "
            f"missing_distinctions={sorted(set(distinction_ids) - used_distinctions)}"
        )
    if not states[-1]["show_handoff"]:
        raise TeachingVisualError("final pilot state must reveal the Phase 2 handoff")

    used_fact_refs = {
        ref
        for record in [*families, *distinctions, abilene_case]
        for ref in record["fact_refs"]
    }
    evidence = compile_evidence_cards(
        used_fact_refs,
        ledgers,
        ledger_ids=declared_ledgers,
    )

    payload = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "pilot": {
            "id": pilot_id,
            "title": title,
            "phase": {
                "id": phase_id,
                "number": 1,
                "title": phase_title,
                "anchor_question": anchor_question,
            },
            "learning_objective": objective,
            "interaction": interaction,
        },
        "canvas": {
            "kind": CANVAS_KIND,
            "width": CANVAS_WIDTH,
            "height": CANVAS_HEIGHT,
        },
        "families": families,
        "distinctions": distinctions,
        "abilene_case": abilene_case,
        "states": states,
        "evidence": evidence,
    }
    compiled_forbidden = _forbidden_fields(payload)
    if compiled_forbidden:
        raise TeachingVisualError(
            f"compiled teaching payload contains forbidden fields: {compiled_forbidden}"
        )
    return payload


def _escape(value: Any) -> str:
    return html.escape(str(value), quote=True)


def _wrapped_svg_text(
    text: str,
    *,
    x: float,
    y: float,
    width_chars: int,
    line_height: float,
    css_class: str,
    maximum_lines: int,
    center_lines: bool = False,
) -> str:
    lines = textwrap.wrap(text, width=width_chars, break_long_words=False) or [""]
    if len(lines) > maximum_lines:
        lines = lines[:maximum_lines]
        lines[-1] = lines[-1].rstrip(" .") + "…"
    first_y = y
    if center_lines:
        first_y -= (len(lines) - 1) * line_height / 2
    tspans = "\n".join(
        f'<tspan x="{x}" dy="{0 if index == 0 else line_height}">{_escape(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'<text class="{css_class}" x="{x}" y="{first_y}">{tspans}</text>'


def _fact_description(record: Mapping[str, Any]) -> str:
    return "Evidence: " + ", ".join(record["fact_refs"])


def _family_svg(record: Mapping[str, Any], index: int) -> str:
    x = 46
    y = 54 + index * 196
    height = 166
    path = list(record["path"])
    path_x = 410.0
    path_width = 770.0
    gap = 22.0
    box_width = (path_width - gap * (len(path) - 1)) / len(path)
    path_parts = []
    center_y = y + 100
    for stage_index, stage in enumerate(path):
        box_x = path_x + stage_index * (box_width + gap)
        if stage_index:
            previous_right = box_x - gap
            path_parts.append(
                f'<path class="flow-arrow" d="M {previous_right:.2f} {center_y:.2f} H {box_x - 5:.2f}"/>'
            )
        path_parts.append(
            f'<rect class="stage-box" x="{box_x:.2f}" y="{center_y - 31:.2f}" '
            f'width="{box_width:.2f}" height="62" rx="8"/>'
        )
        path_parts.append(
            _wrapped_svg_text(
                str(stage),
                x=box_x + box_width / 2,
                y=center_y + 5,
                width_chars=max(8, int(box_width / 10)),
                line_height=14,
                css_class="stage-label centered",
                maximum_lines=4,
                center_lines=True,
            )
        )
    return (
        f'<g class="family" data-family-id="{_escape(record["id"])}" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(_fact_description(record))}</desc>"
        f'<rect class="family-card" x="{x}" y="{y}" width="1170" height="{height}" rx="12"/>'
        f'<text class="family-title" x="72" y="{y + 45}">{_escape(record["title"])}</text>'
        + _wrapped_svg_text(
            ", ".join(record["examples"]),
            x=72,
            y=y + 78,
            width_chars=40,
            line_height=20,
            css_class="family-examples",
            maximum_lines=3,
        )
        + "".join(path_parts)
        + f'<path class="bus-link" data-bus-link hidden d="M 1216 {center_y} H 1310"/>'
        + "</g>"
    )


def _common_bus_svg() -> str:
    return """
<g id="common-bus" data-common-bus hidden>
  <title>Common electrical interface</title>
  <desc>Different physical conversion paths converge on a usable electrical interface.</desc>
  <line class="common-bus" x1="1320" y1="80" x2="1320" y2="790"/>
  <rect class="bus-label-box" x="1360" y="300" width="196" height="220" rx="12"/>
  <text class="bus-title centered" x="1458" y="352">COMMON</text>
  <text class="bus-title centered" x="1458" y="383">ELECTRICAL</text>
  <text class="bus-title centered" x="1458" y="414">INTERFACE</text>
  <text class="bus-detail centered" x="1458" y="458">generator or inverter</text>
  <text class="bus-detail centered" x="1458" y="484">then voltage conversion</text>
</g>
""".strip()


def _mini_node(
    x: float,
    y: float,
    width: float,
    label: str,
    *,
    css_class: str = "mini-node",
) -> str:
    return (
        f'<rect class="{css_class}" x="{x}" y="{y - 22}" '
        f'width="{width}" height="44" rx="8"/>'
        + _wrapped_svg_text(
            label,
            x=x + width / 2,
            y=y + 5,
            width_chars=max(6, int((width - 12) / 8)),
            line_height=14,
            css_class="mini-label centered",
            maximum_lines=2,
            center_lines=True,
        )
    )


def _mini_arrow(start: float, end: float, y: float) -> str:
    return f'<path class="mini-arrow" d="M {start} {y} H {end}"/>'


def _storage_pictogram(x: float, y: float) -> str:
    center_y = y + 225
    stages = (
        (x + 30, 62, "AC"),
        (x + 142, 90, "charge"),
        (x + 282, 86, "BESS"),
        (x + 418, 102, "discharge"),
        (x + 590, 62, "AC"),
    )
    parts = []
    for index, (node_x, width, label) in enumerate(stages):
        if index:
            previous_x, previous_width, _ = stages[index - 1]
            parts.append(_mini_arrow(previous_x + previous_width, node_x - 6, center_y))
        parts.append(_mini_node(node_x, center_y, width, label))
    parts.extend(
        (
            f'<rect class="mini-badge" x="{x + 244}" y="{y + 153}" width="78" height="27" rx="13.5"/>',
            f'<text class="mini-badge-label centered" x="{x + 283}" y="{y + 171}">MW · rate</text>',
            f'<rect class="mini-badge" x="{x + 330}" y="{y + 153}" width="104" height="27" rx="13.5"/>',
            f'<text class="mini-badge-label centered" x="{x + 382}" y="{y + 171}">MWh · energy</text>',
        )
    )
    return '<g class="causal-pictogram">' + "".join(parts) + "</g>"


def _ppa_pictogram(x: float, y: float) -> str:
    contract_y = y + 195
    physical_y = y + 258
    return (
        '<g class="causal-pictogram">'
        + _mini_node(x + 65, contract_y, 110, "Buyer", css_class="contract-node")
        + f'<path class="contract-arrow" d="M {x + 175} {contract_y} H {x + 469}"/>'
        + f'<text class="contract-label centered" x="{x + 322}" y="{contract_y - 13}">PPA · contractual attributes</text>'
        + _mini_node(
            x + 475,
            contract_y,
            170,
            "Generator attributes",
            css_class="contract-node",
        )
        + _mini_node(x + 45, physical_y, 150, "Grid generation")
        + _mini_arrow(x + 195, x + 264, physical_y)
        + _mini_node(x + 270, physical_y, 130, "Shared grid")
        + _mini_arrow(x + 400, x + 494, physical_y)
        + _mini_node(x + 500, physical_y, 145, "Campus load")
        + f'<text class="physical-label centered" x="{x + 347.5}" y="{physical_y - 31}">physical electricity path</text>'
        + "</g>"
    )


def _standby_pictogram(x: float, y: float) -> str:
    center_y = y + 225
    stages = (
        (x + 35, 80, "Fuel", "mini-node"),
        (x + 155, 160, "Engine-generator", "mini-node"),
        (x + 365, 140, "Standby switch", "standby-node"),
        (x + 555, 100, "Load", "mini-node"),
    )
    parts = []
    for index, (node_x, width, label, css_class) in enumerate(stages):
        if index:
            previous_x, previous_width, _, _ = stages[index - 1]
            parts.append(_mini_arrow(previous_x + previous_width, node_x - 6, center_y))
        parts.append(_mini_node(node_x, center_y, width, label, css_class=css_class))
    return '<g class="causal-pictogram">' + "".join(parts) + "</g>"


def _distinction_pictogram(record_id: str, x: float, y: float) -> str:
    if record_id == "storage_not_primary_source":
        return _storage_pictogram(x, y)
    if record_id == "ppa_not_physical_generator":
        return _ppa_pictogram(x, y)
    if record_id == "standby_is_a_role":
        return _standby_pictogram(x, y)
    raise TeachingVisualError(f"unsupported distinction pictogram {record_id!r}")


def _distinction_svg(record: Mapping[str, Any], index: int, total: int) -> str:
    column = index % 2
    row = index // 2
    x = 70 + column * 765
    if total % 2 == 1 and index == total - 1:
        x = 452.5
    y = 85 + row * 345
    return (
        f'<g class="distinction" data-distinction-id="{_escape(record["id"])}" hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(record['body'])} {_escape(_fact_description(record))}</desc>"
        f'<rect class="distinction-card" x="{x}" y="{y}" width="695" height="300" rx="14"/>'
        f'<text class="distinction-title" x="{x + 28}" y="{y + 46}">{_escape(record["title"])}</text>'
        + _wrapped_svg_text(
            str(record["body"]),
            x=x + 28,
            y=y + 84,
            width_chars=72,
            line_height=22,
            css_class="distinction-body",
            maximum_lines=3,
        )
        + _distinction_pictogram(str(record["id"]), x, y)
        + "</g>"
    )


def _case_svg(record: Mapping[str, Any]) -> str:
    path = list(record["path"])
    x0 = 130.0
    usable = 1340.0
    gap = 28.0
    box_width = (usable - gap * (len(path) - 1)) / len(path)
    parts = []
    for index, stage in enumerate(path):
        x = x0 + index * (box_width + gap)
        if index:
            parts.append(
                f'<path class="case-arrow" d="M {x - gap:.2f} 380 H {x - 5:.2f}"/>'
            )
        parts.append(
            f'<rect class="case-stage" x="{x:.2f}" y="315" width="{box_width:.2f}" height="130" rx="12"/>'
        )
        parts.append(
            _wrapped_svg_text(
                str(stage),
                x=x + box_width / 2,
                y=366,
                width_chars=max(10, int(box_width / 9)),
                line_height=24,
                css_class="case-stage-label centered",
                maximum_lines=3,
            )
        )
    return (
        '<g id="abilene-case" data-abilene-case hidden>'
        f"<title>{_escape(record['title'])}</title>"
        f"<desc>{_escape(_fact_description(record))}</desc>"
        '<rect class="case-panel" x="72" y="72" width="1456" height="684" rx="18"/>'
        f'<text class="case-kicker" x="120" y="132">ABILENE APPLICATION</text>'
        f'<text class="case-title" x="120" y="184">{_escape(record["title"])}</text>'
        + "".join(parts)
        + '<rect class="boundary-box" x="120" y="520" width="1360" height="170" rx="12"/>'
        + '<text class="boundary-kicker" x="150" y="558">EVIDENCE BOUNDARY</text>'
        + _wrapped_svg_text(
            str(record["boundary"]),
            x=150,
            y=600,
            width_chars=135,
            line_height=27,
            css_class="boundary-copy",
            maximum_lines=3,
        )
        + "</g>"
    )


def _handoff_svg() -> str:
    return """
<g id="phase-handoff" data-handoff hidden>
  <rect class="handoff-box" x="1015" y="772" width="513" height="100" rx="12"/>
  <text class="handoff-kicker" x="1042" y="806">NEXT · PHASE 2</text>
  <text class="handoff-title" x="1042" y="841">Why raise voltage and transmit?</text>
  <path class="handoff-arrow" d="M 1450 825 H 1494"/>
</g>
""".strip()


def _evidence_html(payload: Mapping[str, Any]) -> str:
    source_by_ref = {record["ref"]: record for record in payload["evidence"]["sources"]}
    fact_rows = []
    for fact in payload["evidence"]["facts"]:
        links = ", ".join(
            f'<a href="{_escape(source_by_ref[ref]["url"])}" target="_blank" rel="noreferrer">'
            f"{_escape(source_by_ref[ref]['publisher'])} · {_escape(source_by_ref[ref]['title'])}</a>"
            for ref in fact["source_refs"]
        )
        value = "unknown" if fact["value"] is None else str(fact["value"])
        if fact["unit"]:
            value = f"{value} {fact['unit']}"
        fact_rows.append(
            '<li class="fact-card">'
            f'<p class="fact-ref">{_escape(fact["ref"])}</p>'
            f"<p><strong>{_escape(value)}</strong></p>"
            f"<p>{_escape(fact['basis'])}</p>"
            f'<p class="fact-boundary">{_escape(fact["scope"])} · '
            f"{_escape(fact['posture'])} · as of {_escape(fact['as_of'])}</p>"
            f'<p class="fact-sources">{links}</p>'
            "</li>"
        )
    return "".join(fact_rows)


def _responsive_flow_html(
    full_path: list[str],
    *,
    compact_path: list[str] | None = None,
) -> str:
    compact = compact_path or full_path
    parts = []
    for index, (full_label, compact_label) in enumerate(zip(full_path, compact)):
        if index:
            parts.append('<span class="responsive-arrow" aria-hidden="true">→</span>')
        parts.append(
            f'<span class="responsive-stage" title="{_escape(full_label)}">'
            f'<span class="full-stage-label">{_escape(full_label)}</span>'
            f'<span class="compact-stage-label">{_escape(compact_label)}</span>'
            "</span>"
        )
    return (
        f'<div class="responsive-flow" role="img" '
        f'aria-label="{_escape(" to ".join(full_path))}">' + "".join(parts) + "</div>"
    )


def _responsive_family_html(record: Mapping[str, Any]) -> str:
    return (
        f'<article class="responsive-card responsive-family" '
        f'data-family-id="{_escape(record["id"])}" hidden>'
        f"<h3>{_escape(record['title'])}</h3>"
        f'<p class="responsive-examples">{_escape(", ".join(record["examples"]))}</p>'
        + _responsive_flow_html(
            list(record["path"]), compact_path=list(record["compact_path"])
        )
        + f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        + "</article>"
    )


def _responsive_node(label: str, *, css_class: str = "") -> str:
    class_name = "responsive-node" + (f" {css_class}" if css_class else "")
    return f'<span class="{class_name}">{_escape(label)}</span>'


def _responsive_causal_row(labels: list[str], *, aria_label: str) -> str:
    parts = []
    for index, label in enumerate(labels):
        if index:
            parts.append('<span class="responsive-arrow" aria-hidden="true">→</span>')
        parts.append(_responsive_node(label))
    return (
        f'<div class="responsive-causal-row" role="img" '
        f'aria-label="{_escape(aria_label)}">' + "".join(parts) + "</div>"
    )


def _responsive_distinction_diagram(record_id: str) -> str:
    if record_id == "storage_not_primary_source":
        return (
            '<div class="responsive-badges"><span>MW · rate</span><span>MWh · energy</span></div>'
            + _responsive_causal_row(
                ["AC", "charge", "BESS", "discharge", "AC"],
                aria_label="AC to charge to BESS to discharge to AC",
            )
        )
    if record_id == "ppa_not_physical_generator":
        return (
            '<div class="responsive-contract-lane" role="img" '
            'aria-label="Buyer linked by a PPA for contractual attributes to generator attributes">'
            + _responsive_node("Buyer", css_class="contract-responsive-node")
            + '<span class="responsive-contract-link" aria-hidden="true">PPA · attributes ⇢</span>'
            + _responsive_node(
                "Generator attributes", css_class="contract-responsive-node"
            )
            + "</div>"
            + '<p class="responsive-lane-label">Separate physical electricity path</p>'
            + _responsive_causal_row(
                ["Grid generation", "Shared grid", "Campus load"],
                aria_label="Grid generation to shared grid to campus load",
            )
        )
    if record_id == "standby_is_a_role":
        return _responsive_causal_row(
            ["Fuel", "Engine-generator", "Standby switch", "Load"],
            aria_label="Fuel to engine-generator to standby switch to load",
        )
    raise TeachingVisualError(f"unsupported responsive distinction {record_id!r}")


def _responsive_distinction_html(record: Mapping[str, Any]) -> str:
    return (
        f'<article class="responsive-card responsive-distinction" '
        f'data-distinction-id="{_escape(record["id"])}" hidden>'
        f"<h3>{_escape(record['title'])}</h3>"
        f'<p class="responsive-body">{_escape(record["body"])}</p>'
        + _responsive_distinction_diagram(str(record["id"]))
        + f'<span class="visually-hidden">{_escape(_fact_description(record))}</span>'
        + "</article>"
    )


def _responsive_visual_html(payload: Mapping[str, Any]) -> str:
    families = "".join(
        _responsive_family_html(record) for record in payload["families"]
    )
    distinctions = "".join(
        _responsive_distinction_html(record) for record in payload["distinctions"]
    )
    case = payload["abilene_case"]
    return (
        '<section class="responsive-visual" aria-label="Responsive generation teaching diagram">'
        '<div class="responsive-families">'
        + families
        + '<div class="responsive-common-bus" data-common-bus hidden>'
        "<strong>Common electrical interface</strong>"
        "<span>generator or inverter → voltage conversion</span>"
        "</div></div>"
        '<div class="responsive-distinctions">' + distinctions + "</div>"
        '<article class="responsive-card responsive-case" data-abilene-case hidden>'
        '<p class="responsive-kicker">Abilene application</p>'
        f"<h3>{_escape(case['title'])}</h3>"
        + _responsive_flow_html(list(case["path"]))
        + '<div class="responsive-boundary"><strong>Evidence boundary</strong>'
        f"<p>{_escape(case['boundary'])}</p></div>"
        "</article>"
        '<div class="responsive-handoff" data-handoff hidden>'
        "<span>Next · Phase 2</span><strong>Why raise voltage and transmit? →</strong>"
        "</div>"
        "</section>"
    )


def render_generation_landscape(payload: dict[str, Any]) -> str:
    """Render one compiled generation landscape as a self-contained HTML page."""
    if payload.get("canvas", {}).get("kind") != CANVAS_KIND:
        raise TeachingVisualError("render payload is not a generation landscape")
    families = "".join(
        _family_svg(record, index) for index, record in enumerate(payload["families"])
    )
    distinctions = "".join(
        _distinction_svg(record, index, len(payload["distinctions"]))
        for index, record in enumerate(payload["distinctions"])
    )
    state_buttons = "".join(
        f'<button class="state-button" type="button" role="tab" '
        f'id="state-tab-{_escape(state["id"])}" aria-controls="visual" '
        f'aria-label="State {index + 1}: {_escape(state["title"])}" '
        f'title="{_escape(state["title"])}" aria-selected="false" '
        f'data-state-index="{index}">'
        f'<span class="state-number">{index + 1:02d}</span>'
        f'<span class="state-nav-label">{_escape(state["nav_label"])}</span></button>'
        for index, state in enumerate(payload["states"])
    )
    serialized = json.dumps(payload, sort_keys=True, separators=(",", ":")).replace(
        "</", "<\\/"
    )
    evidence = _evidence_html(payload)
    responsive_visual = _responsive_visual_html(payload)
    phase = payload["pilot"]["phase"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="gigawatt-source-digest" content="{_escape(payload["source_digest"])}">
<title>GIGAWATT — {_escape(payload["pilot"]["title"])}</title>
<style>
  :root {{ --paper:#fafaf7; --ink:#1a1a1a; --muted:#5f5f59; --faint:#d4d4cd; --blue:#175d8d; --green:#2f9e8f; --amber:#b76e18; --red:#b3261e; }}
  * {{ box-sizing:border-box; }}
  [hidden] {{ display:none !important; }}
  html,body {{ width:100%; height:100%; min-height:0; margin:0; background:var(--paper); color:var(--ink); font-family:Inter,"Helvetica Neue",Arial,sans-serif; }}
  html {{ overflow:hidden; }}
  body {{ display:grid; grid-template-rows:auto minmax(0,1fr) auto; height:100dvh; min-height:0; overflow:hidden; }}
  header {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(280px,520px); gap:20px; min-height:0; padding:11px 20px 10px; border-bottom:1.5px solid var(--ink); }}
  .eyebrow,.phase-question,.state-number,.fact-ref,.boundary-kicker,.case-kicker,.handoff-kicker {{ text-transform:uppercase; letter-spacing:.08em; font-size:11px; font-weight:700; }}
  h1 {{ margin:3px 0; font-size:clamp(21px,2.2vw,34px); line-height:1.05; }}
  header p {{ margin:2px 0; line-height:1.3; }}
  .objective {{ color:var(--muted); font-size:13px; align-self:end; }}
  main {{ min-width:0; min-height:0; display:grid; place-items:center; overflow:hidden; padding:8px 14px; }}
  .visual-shell {{ width:100%; height:100%; min-width:0; min-height:0; max-width:1600px; max-height:900px; border:1.5px solid var(--ink); background:white; }}
  svg {{ display:block; width:100%; height:100%; }}
  .family-card,.distinction-card,.case-panel {{ fill:#fff; stroke:var(--ink); stroke-width:2; }}
  .family-title,.distinction-title,.case-title {{ font-size:24px; font-weight:700; }}
  .family-examples,.distinction-body,.boundary-copy {{ font-size:17px; fill:var(--muted); }}
  .stage-box {{ fill:var(--paper); stroke:var(--blue); stroke-width:2; }}
  .stage-label {{ font-size:15px; font-weight:650; }}
  .case-stage-label {{ font-size:16px; font-weight:650; }}
  .centered {{ text-anchor:middle; }}
  .flow-arrow,.bus-link,.case-arrow,.handoff-arrow {{ fill:none; stroke:var(--blue); stroke-width:4; marker-end:url(#arrow); }}
  .common-bus {{ stroke:var(--blue); stroke-width:10; }}
  .bus-label-box {{ fill:var(--paper); stroke:var(--blue); stroke-width:2; }}
  .bus-title {{ font-size:22px; font-weight:800; fill:var(--blue); }}
  .bus-detail {{ font-size:14px; fill:var(--muted); }}
  .distinction-card {{ fill:var(--paper); }}
  .mini-node {{ fill:white; stroke:var(--blue); stroke-width:2; }}
  .standby-node {{ fill:#fff7ed; stroke:var(--amber); stroke-width:2; }}
  .contract-node {{ fill:#fff7ed; stroke:var(--amber); stroke-width:2; }}
  .mini-label {{ font-size:13px; font-weight:700; }}
  .mini-arrow {{ fill:none; stroke:var(--blue); stroke-width:2.5; marker-end:url(#arrow-small); }}
  .contract-arrow {{ fill:none; stroke:var(--amber); stroke-width:2.5; stroke-dasharray:8 6; marker-end:url(#arrow-small-amber); }}
  .contract-label,.physical-label {{ font-size:12px; font-weight:700; letter-spacing:.03em; }}
  .contract-label {{ fill:var(--amber); }}
  .physical-label {{ fill:var(--blue); }}
  .mini-badge {{ fill:var(--blue); }}
  .mini-badge-label {{ fill:white; font-size:11px; font-weight:700; }}
  .case-panel {{ stroke:var(--blue); stroke-width:3; }}
  .case-kicker {{ fill:var(--blue); }}
  .case-stage {{ fill:var(--paper); stroke:var(--blue); stroke-width:2.5; }}
  .boundary-box {{ fill:#fff7ed; stroke:var(--amber); stroke-width:2; }}
  .boundary-kicker {{ fill:var(--amber); }}
  .handoff-box {{ fill:var(--ink); stroke:var(--ink); }}
  .handoff-kicker,.handoff-title {{ fill:white; }}
  .handoff-title {{ font-size:21px; font-weight:700; }}
  .handoff-arrow {{ stroke:white; marker-end:url(#arrow-white); }}
  footer {{ display:grid; grid-template-columns:minmax(0,1fr) minmax(300px,540px); gap:10px 16px; min-height:0; max-height:48dvh; padding:9px 14px 10px; border-top:1.5px solid var(--ink); }}
  .state-nav {{ display:grid; grid-template-columns:repeat({len(payload["states"])},minmax(0,1fr)); gap:6px; }}
  .state-button {{ display:grid; grid-template-columns:auto 1fr; gap:7px; align-items:center; min-width:0; min-height:44px; padding:7px 8px; border:1.5px solid var(--ink); background:transparent; color:inherit; text-align:left; font:inherit; cursor:pointer; }}
  .state-nav-label {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }}
  .state-button[aria-selected="true"] {{ background:var(--ink); color:white; }}
  .state-copy {{ min-width:0; align-self:center; }}
  .state-copy h2 {{ margin:0 0 3px; font-size:16px; }}
  .state-copy p {{ margin:0; color:var(--muted); font-size:13px; line-height:1.3; }}
  details {{ grid-column:1/-1; min-height:0; border-top:1px solid var(--faint); padding-top:6px; }}
  details[open] {{ max-height:min(34dvh,320px); overflow:auto; overscroll-behavior:contain; }}
  summary {{ position:sticky; top:0; z-index:1; cursor:pointer; padding:3px 0; background:var(--paper); font-weight:700; }}
  .fact-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:12px; margin-bottom:0; padding:0; list-style:none; }}
  .fact-card {{ border:1px solid var(--faint); padding:10px 12px; background:white; }}
  .fact-card p {{ margin:5px 0; line-height:1.35; }}
  .fact-ref,.fact-boundary {{ color:var(--muted); font-size:11px; overflow-wrap:anywhere; }}
  .fact-sources {{ font-size:12px; }}
  a {{ color:var(--blue); overflow-wrap:anywhere; }}
  .visually-hidden {{ position:absolute !important; width:1px; height:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }}
  .responsive-visual {{ display:none; }}
  .responsive-card {{ min-width:0; border:1.5px solid var(--ink); border-radius:9px; background:white; }}
  .responsive-card h3 {{ margin:0; line-height:1.15; }}
  .responsive-card p {{ margin:0; }}
  .responsive-flow,.responsive-causal-row,.responsive-contract-lane {{ display:flex; align-items:center; }}
  .responsive-stage,.responsive-node {{ display:inline-grid; place-items:center; min-width:0; border:1.5px solid var(--blue); border-radius:6px; background:white; text-align:center; font-weight:700; line-height:1.1; }}
  .responsive-arrow {{ flex:0 0 auto; color:var(--blue); font-weight:800; }}
  .compact-stage-label {{ display:none; }}
  .responsive-badges {{ display:flex; justify-content:center; gap:5px; }}
  .responsive-badges span {{ border-radius:999px; background:var(--blue); color:white; font-weight:700; }}
  .contract-responsive-node {{ border-color:var(--amber); background:#fff7ed; }}
  .responsive-contract-link {{ color:var(--amber); text-align:center; font-weight:700; }}
  .responsive-lane-label {{ color:var(--blue); text-align:center; font-weight:700; }}
  .responsive-common-bus {{ grid-column:1/-1; align-items:center; justify-content:center; border:1.5px solid var(--blue); border-radius:7px; color:var(--blue); text-align:center; }}
  .responsive-common-bus span {{ color:var(--muted); }}
  .responsive-boundary {{ border:1.5px solid var(--amber); border-radius:7px; background:#fff7ed; }}
  .responsive-boundary strong,.responsive-kicker {{ color:var(--amber); text-transform:uppercase; letter-spacing:.06em; }}
  .responsive-handoff {{ align-items:center; justify-content:space-between; border-radius:8px; background:var(--ink); color:white; }}
  @media (max-width:1100px) and (min-width:901px) {{
    .state-nav {{ gap:4px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; padding:4px; text-align:center; font-size:11px; }}
  }}
  @media (max-width:900px) {{
    header {{ grid-template-columns:1fr; gap:2px; padding:8px 10px 7px; }}
    .objective {{ font-size:11px; }}
    main {{ padding:6px; }}
    footer {{ grid-template-columns:1fr; gap:5px; padding:6px 8px 7px; }}
    .state-nav {{ grid-template-columns:repeat({len(payload["states"])},minmax(0,1fr)); gap:4px; }}
    .state-button {{ grid-template-columns:1fr; gap:1px; min-height:44px; padding:4px; text-align:center; font-size:11px; }}
    .state-copy h2 {{ font-size:14px; }}
    .state-copy p {{ display:-webkit-box; overflow:hidden; -webkit-box-orient:vertical; -webkit-line-clamp:2; font-size:11px; }}
    details[open] {{ position:fixed; inset:10px; z-index:10; max-height:none; padding:10px; overflow:auto; border:1.5px solid var(--ink); background:var(--paper); }}
  }}
  @media (max-height:{SHORT_LANDSCAPE_MAX_HEIGHT}px) and (orientation:landscape) {{
    header {{ grid-template-columns:minmax(0,1fr) minmax(230px,420px); gap:10px; padding:4px 10px; }}
    h1 {{ margin:1px 0; font-size:18px; }}
    .eyebrow,.phase-question {{ font-size:9px; }}
    .objective {{ display:none; }}
    main {{ padding:3px 7px; }}
    footer {{ grid-template-columns:minmax(0,1fr) minmax(250px,390px) auto; gap:6px; padding:4px 7px; }}
    .state-button {{ grid-template-columns:auto 1fr; min-height:34px; padding:3px 4px; text-align:left; font-size:10px; }}
    .state-copy h2 {{ font-size:12px; }}
    .state-copy p {{ display:block; overflow:visible; -webkit-line-clamp:unset; font-size:10px; }}
    details {{ grid-column:auto; align-self:center; border-top:0; padding-top:0; font-size:10px; }}
    .evidence-count {{ display:none; }}
    .visual-shell {{ display:none; }}
    .responsive-visual {{ display:block; width:100%; height:100%; min-height:0; overflow:auto; padding:2px; }}
    .responsive-families {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:4px 6px; }}
    .responsive-distinctions {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:6px; }}
    .responsive-card {{ padding:5px; }}
    .responsive-card h3 {{ margin-bottom:3px; font-size:12px; }}
    .responsive-examples {{ overflow:hidden; text-overflow:ellipsis; white-space:nowrap; color:var(--muted); font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-body {{ display:none; }}
    .responsive-flow,.responsive-causal-row {{ gap:2px; margin-top:5px; }}
    .responsive-stage,.responsive-node {{ flex:1 1 0; min-height:26px; padding:2px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-arrow {{ font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .full-stage-label {{ display:none; }}
    .compact-stage-label {{ display:inline; }}
    .responsive-common-bus {{ display:flex; gap:8px; min-height:24px; padding:3px 6px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-distinction {{ min-height:102px; }}
    .responsive-distinction h3 {{ min-height:28px; }}
    .responsive-badges {{ margin:2px 0; }}
    .responsive-badges span {{ padding:2px 5px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-contract-lane {{ gap:3px; }}
    .responsive-contract-lane .responsive-node {{ flex:1 1 0; }}
    .responsive-contract-link {{ flex:1 1 0; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-lane-label {{ margin:2px 0 !important; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-case h3 {{ font-size:13px; }}
    .responsive-kicker {{ margin-bottom:2px !important; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-boundary {{ margin-top:5px; padding:4px 6px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
    .responsive-boundary p {{ display:-webkit-box; overflow:hidden; -webkit-box-orient:vertical; -webkit-line-clamp:2; }}
    .responsive-handoff {{ display:flex; margin-top:4px; padding:5px 8px; font-size:{SHORT_LANDSCAPE_MIN_TEXT_PX}px; }}
  }}
  @media (max-width:{PORTRAIT_MAX_WIDTH}px) and (orientation:portrait) {{
    header {{ padding:7px 8px 6px; }}
    h1 {{ font-size:20px; }}
    .state-number {{ font-size:9px; }}
    .state-nav-label {{ font-size:10px; }}
    main {{ place-items:start stretch; overflow:auto; overscroll-behavior:contain; }}
    .visual-shell {{ display:none; }}
    .responsive-visual {{ display:block; width:100%; height:auto; min-height:100%; padding:3px; }}
    .responsive-families,.responsive-distinctions {{ display:grid; grid-template-columns:1fr; gap:8px; }}
    .responsive-card {{ padding:10px; }}
    .responsive-card h3 {{ margin-bottom:5px; font-size:16px; }}
    .responsive-examples,.responsive-body {{ margin-bottom:8px !important; color:var(--muted); font-size:{PORTRAIT_MIN_TEXT_PX}px; line-height:1.35; }}
    .responsive-flow,.responsive-causal-row,.responsive-contract-lane {{ flex-direction:column; align-items:stretch; gap:4px; }}
    .responsive-stage,.responsive-node {{ min-height:34px; padding:5px 7px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-arrow {{ align-self:center; font-size:16px; line-height:1; transform:rotate(90deg); }}
    .full-stage-label {{ display:inline; }}
    .compact-stage-label {{ display:none; }}
    .responsive-common-bus {{ display:grid; gap:2px; min-height:52px; margin-top:8px; padding:7px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-badges {{ margin:5px 0; }}
    .responsive-badges span {{ padding:4px 8px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-contract-link {{ padding:4px; border-top:1.5px dashed var(--amber); border-bottom:1.5px dashed var(--amber); font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-lane-label {{ margin:8px 0 4px !important; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-kicker {{ margin-bottom:4px !important; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
    .responsive-boundary {{ margin-top:8px; padding:8px; font-size:{PORTRAIT_MIN_TEXT_PX}px; line-height:1.35; }}
    .responsive-handoff {{ display:grid; gap:3px; margin-top:8px; padding:10px; font-size:{PORTRAIT_MIN_TEXT_PX}px; }}
  }}
</style>
</head>
<body>
<header>
  <div>
    <p class="eyebrow">Phase {phase["number"]} · {_escape(phase["title"])}</p>
    <h1>{_escape(payload["pilot"]["title"])}</h1>
    <p class="phase-question">{_escape(phase["anchor_question"])}</p>
  </div>
  <p class="objective">{_escape(payload["pilot"]["learning_objective"])}</p>
</header>
<main>
  <section class="visual-shell" aria-label="Instructor-controlled generation teaching diagram">
    <svg id="visual" role="img" viewBox="0 0 {CANVAS_WIDTH} {CANVAS_HEIGHT}" aria-labelledby="visual-title visual-description">
      <title id="visual-title">Generation conversion landscape</title>
      <desc id="visual-description">A manually selected sequence comparing generation conversion families, commercial and physical distinctions, and the Abilene application.</desc>
      <defs>
        <marker id="arrow" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#175d8d"/></marker>
        <marker id="arrow-white" markerWidth="8" markerHeight="8" refX="7" refY="4" orient="auto"><path d="M0,0 L8,4 L0,8 Z" fill="#ffffff"/></marker>
        <marker id="arrow-small" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#175d8d"/></marker>
        <marker id="arrow-small-amber" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#b76e18"/></marker>
      </defs>
      {families}
      {_common_bus_svg()}
      {distinctions}
      {_case_svg(payload["abilene_case"])}
      {_handoff_svg()}
    </svg>
  </section>
  {responsive_visual}
</main>
<footer>
  <nav class="state-nav" role="tablist" aria-label="Manual Phase 1 teaching states">{state_buttons}</nav>
  <section class="state-copy" aria-labelledby="state-title"><h2 id="state-title"></h2><p id="state-instruction"></p></section>
  <p id="state-status" class="visually-hidden" aria-live="polite"></p>
  <details><summary><span class="evidence-label">Evidence</span><span class="evidence-count"> used in this pilot · {len(payload["evidence"]["facts"])} facts · {len(payload["evidence"]["sources"])} sources</span></summary><ul class="fact-list">{evidence}</ul></details>
</footer>
<script id="pilot-data" type="application/json">{serialized}</script>
<script>
"use strict";
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
const pilot = JSON.parse(document.getElementById("pilot-data").textContent);
const buttons = [...document.querySelectorAll("[data-state-index]")];
let current = 0;

function setVisible(selector, selected) {{
  document.querySelectorAll(selector).forEach(element => {{
    const id = element.dataset.familyId || element.dataset.distinctionId;
    element.toggleAttribute("hidden", !selected.includes(id));
  }});
}}

function resetTeachingScroll() {{
  window.scrollTo(0, 0);
  if (document.scrollingElement) {{
    document.scrollingElement.scrollTop = 0;
    document.scrollingElement.scrollLeft = 0;
  }}
  [document.querySelector("main"), document.querySelector(".responsive-visual")]
    .forEach(container => {{
      container.scrollTop = 0;
      container.scrollLeft = 0;
    }});
}}

function activate(index, focusButton = false) {{
  current = Math.max(0, Math.min(pilot.states.length - 1, index));
  const state = pilot.states[current];
  setVisible("[data-family-id]", state.family_ids);
  setVisible("[data-distinction-id]", state.distinction_ids);
  document.querySelectorAll("[data-bus-link]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_common_bus);
  }});
  document.querySelectorAll("[data-common-bus]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_common_bus);
  }});
  document.querySelectorAll("[data-abilene-case]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_abilene_case);
  }});
  document.querySelectorAll("[data-handoff]").forEach(element => {{
    element.toggleAttribute("hidden", !state.show_handoff);
  }});
  buttons.forEach((button, buttonIndex) => {{
    const selected = buttonIndex === current;
    button.setAttribute("aria-selected", String(selected));
    button.tabIndex = selected ? 0 : -1;
  }});
  document.getElementById("state-title").textContent = state.title;
  document.getElementById("state-instruction").textContent = state.instruction;
  document.getElementById("state-status").textContent = `State ${{current + 1}} of ${{pilot.states.length}}: ${{state.title}}. ${{state.instruction}}`;
  resetTeachingScroll();
  if (focusButton) buttons[current].focus();
}}

buttons.forEach((button, index) => button.addEventListener("click", () => activate(index)));
document.querySelector(".state-nav").addEventListener("keydown", event => {{
  let target = null;
  if (event.key === "ArrowRight" || event.key === "ArrowDown") target = current + 1;
  if (event.key === "ArrowLeft" || event.key === "ArrowUp") target = current - 1;
  if (event.key === "Home") target = 0;
  if (event.key === "End") target = pilot.states.length - 1;
  if (target !== null) {{ event.preventDefault(); activate(target, true); }}
}});
const evidenceDrawer = document.querySelector("details");
evidenceDrawer.addEventListener("toggle", () => {{
  if (!evidenceDrawer.open) resetTeachingScroll();
}});
activate(0);
</script>
</body>
</html>
"""
