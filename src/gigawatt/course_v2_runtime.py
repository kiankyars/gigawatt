"""Strict unified runtime for the six-phase GIGAWATT v2 course.

The v2 player treats every phase renderer as a same-origin visual component.
This module validates the course spine, phase manifests, and embedded renderer
payloads before producing one deterministic registry, player, and instructor
packet.  The frozen v1 course remains a separate publication surface.
"""

from __future__ import annotations

import json
import re
from collections.abc import Mapping
from pathlib import Path, PurePosixPath
from typing import Any

from gigawatt import teaching_visuals as base

SCHEMA_VERSION = 1
PHASE_COUNT = 6
COURSE_PATH = Path("course/course_v2.yaml")
RUNTIME_PATH = Path("diagram/course_v2_runtime.json")
PLAYER_PATH = Path("diagram/course_v2.html")
PACKET_PATH = Path("course/INSTRUCTOR_PACKET_V2.md")
CAMERAS_PATH = Path("diagram/cameras.yaml")
COURSE_RUNTIME_PATH = Path("diagram/course_runtime.json")
PHASE_IDS = [
    "phase_1_generation",
    "phase_2_transmission",
    "phase_3_campus",
    "phase_4_building",
    "phase_5_compute",
    "phase_6_heat",
]
TOP_LEVEL_FIELDS = {
    "schema_version",
    "id",
    "title",
    "subtitle",
    "interaction",
    "journey",
    "spatial",
    "phases",
    "synthesis",
}
JOURNEY_FIELDS = {"id", "title", "anchor_question", "body", "phase_ids"}
SPATIAL_FIELDS = {"minimum_width_px", "state_views"}
SPATIAL_VIEW_FIELDS = {
    "artifact",
    "view_kind",
    "view_id",
    "title",
    "purpose",
    "boundary",
}
CAMERA_ROOT_FIELDS = {"meta", "vertical_slice", "cameras"}
COURSE_RUNTIME_FIELDS = {
    "act_count",
    "evidence_ready_count",
    "research_required_count",
    "schema_version",
    "segment_count",
    "segments",
    "source_digest",
}
PHASE_FIELDS = {
    "id",
    "number",
    "verb",
    "title",
    "question",
    "manifest",
    "artifact",
    "carrier_in",
    "carrier_out",
}
MANIFEST_PHASE_FIELDS = {"id", "number", "title", "anchor_question"}
SYNTHESIS_FIELDS = {"id", "title", "body", "lenses"}
LENS_FIELDS = {"id", "title", "question", "phase_readings"}
ARTIFACT_PAYLOAD_FIELDS = {
    "schema_version",
    "source_digest",
    "pilot",
    "canvas",
    "states",
    "evidence",
}
PILOT_REQUIRED_FIELDS = {
    "id",
    "title",
    "phase",
    "learning_objective",
    "interaction",
}
STATE_REQUIRED_FIELDS = {"id", "nav_label", "title", "instruction"}
EVIDENCE_FIELDS = {"ledger_ids", "facts", "sources"}
FACT_REQUIRED_FIELDS = {
    "ref",
    "value",
    "unit",
    "scope",
    "basis",
    "lifecycle",
    "as_of",
    "posture",
    "source_refs",
}
SOURCE_FIELDS = {
    "ref",
    "publisher",
    "title",
    "url",
    "accessed_as_of",
}
PILOT_DATA_PATTERN = re.compile(
    r'<script id="pilot-data" type="application/json">(?P<payload>.*?)</script>',
    re.DOTALL,
)
DIGEST_META_PATTERN = re.compile(
    r'<meta name="gigawatt-source-digest" content="(?P<digest>[0-9a-f]{64})">'
)


class CourseV2RuntimeError(base.TeachingVisualError):
    """Raised when the unified v2 course escapes its source contracts."""


def _exact(value: Any, fields: set[str], location: str) -> dict[str, Any]:
    try:
        return base._exact_fields(value, fields, location)
    except base.TeachingVisualError as error:
        raise CourseV2RuntimeError(str(error)) from error


def _text(value: Any, location: str, *, maximum: int = 300) -> str:
    try:
        return base._text(value, location, maximum=maximum)
    except base.TeachingVisualError as error:
        raise CourseV2RuntimeError(str(error)) from error


def _identifier(value: Any, location: str) -> str:
    try:
        return base._id(value, location)
    except base.TeachingVisualError as error:
        raise CourseV2RuntimeError(str(error)) from error


def _list(
    value: Any,
    location: str,
    *,
    minimum: int,
    maximum: int,
    item_limit: int = 160,
) -> list[str]:
    try:
        return base._unique_text_list(
            value,
            location,
            minimum=minimum,
            maximum=maximum,
            item_limit=item_limit,
        )
    except base.TeachingVisualError as error:
        raise CourseV2RuntimeError(str(error)) from error


def _relative_path(
    value: Any,
    location: str,
    *,
    prefix: str,
    suffix: str,
) -> str:
    normalized = _text(value, location, maximum=180)
    path = PurePosixPath(normalized)
    if (
        path.is_absolute()
        or ".." in path.parts
        or path.suffix != suffix
        or not normalized.startswith(prefix)
    ):
        raise CourseV2RuntimeError(
            f"{location}: expected a safe {suffix} path under {prefix}"
        )
    return normalized


def extract_pilot_payload(rendered: str, *, location: str) -> dict[str, Any]:
    """Extract and minimally validate one self-contained renderer payload."""
    if not isinstance(rendered, str) or not rendered.startswith("<!doctype html>"):
        raise CourseV2RuntimeError(f"{location}: expected self-contained HTML")
    match = PILOT_DATA_PATTERN.search(rendered)
    if match is None:
        raise CourseV2RuntimeError(f"{location}: missing embedded pilot-data JSON")
    try:
        payload = json.loads(match.group("payload"))
    except json.JSONDecodeError as error:
        raise CourseV2RuntimeError(
            f"{location}: invalid embedded pilot-data JSON: {error}"
        ) from error
    if not isinstance(payload, dict):
        raise CourseV2RuntimeError(f"{location}: embedded pilot data must be a mapping")
    required = ARTIFACT_PAYLOAD_FIELDS
    missing = required - set(payload)
    if missing:
        raise CourseV2RuntimeError(
            f"{location}: embedded pilot data missing {sorted(missing)}"
        )
    digest = base.validate_source_digest(payload["source_digest"])
    meta = DIGEST_META_PATTERN.search(rendered)
    if meta is None or meta.group("digest") != digest:
        raise CourseV2RuntimeError(
            f"{location}: source-digest meta must match embedded payload"
        )
    forbidden = base._forbidden_fields(payload)
    if forbidden:
        raise CourseV2RuntimeError(
            f"{location}: embedded payload contains pacing fields {forbidden}"
        )
    return payload


def _normalize_state(raw: Any, location: str) -> dict[str, str]:
    if not isinstance(raw, dict):
        raise CourseV2RuntimeError(f"{location}: expected a mapping")
    missing = STATE_REQUIRED_FIELDS - set(raw)
    if missing:
        raise CourseV2RuntimeError(f"{location}: missing {sorted(missing)}")
    return {
        "id": _identifier(raw["id"], f"{location}.id"),
        "nav_label": _text(raw["nav_label"], f"{location}.nav_label", maximum=24),
        "title": _text(raw["title"], f"{location}.title", maximum=180),
        "instruction": _text(
            raw["instruction"], f"{location}.instruction", maximum=600
        ),
    }


def _normalize_evidence(raw: Any, location: str) -> dict[str, Any]:
    evidence = _exact(raw, EVIDENCE_FIELDS, location)
    ledger_ids = _list(
        evidence["ledger_ids"],
        f"{location}.ledger_ids",
        minimum=1,
        maximum=12,
        item_limit=80,
    )
    if not isinstance(evidence["sources"], list) or not evidence["sources"]:
        raise CourseV2RuntimeError(f"{location}.sources must be a non-empty list")
    sources = []
    source_refs: set[str] = set()
    for index, raw_source in enumerate(evidence["sources"]):
        source_location = f"{location}.sources[{index}]"
        source = _exact(raw_source, SOURCE_FIELDS, source_location)
        ref = _text(source["ref"], f"{source_location}.ref", maximum=180)
        if ref.count(":") != 1:
            raise CourseV2RuntimeError(f"{source_location}.ref must be qualified")
        if ref in source_refs:
            raise CourseV2RuntimeError(f"{location}.sources refs must be unique")
        url = _text(source["url"], f"{source_location}.url", maximum=700)
        if not url.startswith(("https://", "http://")):
            raise CourseV2RuntimeError(f"{source_location}.url must be HTTP(S)")
        source_refs.add(ref)
        sources.append(
            {
                "ref": ref,
                "publisher": _text(
                    source["publisher"],
                    f"{source_location}.publisher",
                    maximum=220,
                ),
                "title": _text(
                    source["title"], f"{source_location}.title", maximum=500
                ),
                "url": url,
                "accessed_as_of": _text(
                    source["accessed_as_of"],
                    f"{source_location}.accessed_as_of",
                    maximum=40,
                ),
            }
        )
    if not isinstance(evidence["facts"], list) or not evidence["facts"]:
        raise CourseV2RuntimeError(f"{location}.facts must be a non-empty list")
    facts = []
    fact_refs: set[str] = set()
    for index, raw_fact in enumerate(evidence["facts"]):
        fact_location = f"{location}.facts[{index}]"
        fact = _exact(raw_fact, FACT_REQUIRED_FIELDS, fact_location)
        ref = _text(fact["ref"], f"{fact_location}.ref", maximum=180)
        if ref.count(":") != 1:
            raise CourseV2RuntimeError(f"{fact_location}.ref must be qualified")
        if ref in fact_refs:
            raise CourseV2RuntimeError(f"{location}.facts refs must be unique")
        bound_sources = _list(
            fact["source_refs"],
            f"{fact_location}.source_refs",
            minimum=1,
            maximum=12,
            item_limit=180,
        )
        unknown_sources = sorted(set(bound_sources) - source_refs)
        if unknown_sources:
            raise CourseV2RuntimeError(
                f"{fact_location}: unknown source refs {unknown_sources}"
            )
        fact_refs.add(ref)
        normalized = {"ref": ref, "value": fact["value"], "source_refs": bound_sources}
        if fact["unit"] is not None and not isinstance(fact["unit"], str):
            raise CourseV2RuntimeError(f"{fact_location}.unit must be text or null")
        normalized["unit"] = fact["unit"]
        for field in ("scope", "basis", "lifecycle", "as_of", "posture"):
            normalized[field] = _text(
                fact[field], f"{fact_location}.{field}", maximum=1400
            )
        facts.append(normalized)
    return {"ledger_ids": ledger_ids, "facts": facts, "sources": sources}


def _indexed_records(
    records: Any,
    *,
    location: str,
    id_field: str,
) -> tuple[list[str], dict[str, dict[str, Any]]]:
    if not isinstance(records, list) or not records:
        raise CourseV2RuntimeError(f"{location} must be a non-empty list")
    ids: list[str] = []
    indexed: dict[str, dict[str, Any]] = {}
    for index, record in enumerate(records):
        record_location = f"{location}[{index}]"
        if not isinstance(record, dict):
            raise CourseV2RuntimeError(f"{record_location} must be a mapping")
        record_id = _identifier(record.get(id_field), f"{record_location}.{id_field}")
        if record_id in indexed:
            raise CourseV2RuntimeError(f"{location}.{id_field} values must be unique")
        ids.append(record_id)
        indexed[record_id] = record
    return ids, indexed


def _normalize_spatial(
    raw: Any,
    cameras_raw: Any,
    course_runtime_raw: Any,
    phases: list[dict[str, Any]],
) -> dict[str, Any]:
    spatial = _exact(raw, SPATIAL_FIELDS, "course v2.spatial")
    minimum_width = spatial["minimum_width_px"]
    if type(minimum_width) is not int or minimum_width != 900:
        raise CourseV2RuntimeError(
            "course v2.spatial.minimum_width_px must be integer 900"
        )

    camera_root = _exact(cameras_raw, CAMERA_ROOT_FIELDS, "cameras.yaml")
    camera_ids, cameras = _indexed_records(
        camera_root["cameras"], location="cameras.yaml.cameras", id_field="id"
    )
    if camera_root["vertical_slice"] != camera_ids:
        raise CourseV2RuntimeError(
            "cameras.yaml.vertical_slice must match the camera inventory order"
        )

    course_runtime = _exact(
        course_runtime_raw, COURSE_RUNTIME_FIELDS, "course_runtime.json"
    )
    if (
        type(course_runtime["schema_version"]) is not int
        or course_runtime["schema_version"] != 1
    ):
        raise CourseV2RuntimeError(
            "course_runtime.json.schema_version must be integer 1"
        )
    base.validate_source_digest(course_runtime["source_digest"])
    segment_ids, segments = _indexed_records(
        course_runtime["segments"],
        location="course_runtime.json.segments",
        id_field="segment_id",
    )
    if type(course_runtime["segment_count"]) is not int or course_runtime[
        "segment_count"
    ] != len(segment_ids):
        raise CourseV2RuntimeError(
            "course_runtime.json.segment_count must match the segment inventory"
        )

    raw_state_views = spatial["state_views"]
    if not isinstance(raw_state_views, dict) or set(raw_state_views) != set(PHASE_IDS):
        raise CourseV2RuntimeError(
            "course v2.spatial.state_views must map exactly the six phase IDs"
        )

    phase_states = {
        phase["id"]: {state["id"]: state for state in phase["states"]}
        for phase in phases
    }
    artifact_kinds = {
        "segment": "diagram/course.html",
        "camera": "diagram/hybrid.html",
    }
    artifacts: set[str] = set()
    view_count = 0
    for phase_id in PHASE_IDS:
        raw_phase_views = raw_state_views[phase_id]
        phase_location = f"course v2.spatial.state_views.{phase_id}"
        if not isinstance(raw_phase_views, dict) or not raw_phase_views:
            raise CourseV2RuntimeError(f"{phase_location} must be a non-empty mapping")
        for state_id in raw_phase_views:
            _identifier(state_id, f"{phase_location}.state_id")
        unknown_states = sorted(set(raw_phase_views) - set(phase_states[phase_id]))
        if unknown_states:
            raise CourseV2RuntimeError(
                f"{phase_location} contains unknown state IDs {unknown_states}"
            )
        for state_id, raw_view in raw_phase_views.items():
            location = f"{phase_location}.{state_id}"
            view = _exact(raw_view, SPATIAL_VIEW_FIELDS, location)
            artifact = _relative_path(
                view["artifact"],
                f"{location}.artifact",
                prefix="diagram/",
                suffix=".html",
            )
            view_kind = _identifier(view["view_kind"], f"{location}.view_kind")
            if view_kind not in artifact_kinds:
                raise CourseV2RuntimeError(
                    f"{location}.view_kind must be 'segment' or 'camera'"
                )
            if artifact != artifact_kinds[view_kind]:
                raise CourseV2RuntimeError(
                    f"{location}: {view_kind!r} views must use "
                    f"{artifact_kinds[view_kind]!r}"
                )
            view_id = _identifier(view["view_id"], f"{location}.view_id")
            source = (
                segments.get(view_id)
                if view_kind == "segment"
                else cameras.get(view_id)
            )
            if source is None:
                inventory = (
                    "course_runtime.json" if view_kind == "segment" else "cameras.yaml"
                )
                raise CourseV2RuntimeError(
                    f"{location}.view_id {view_id!r} is not present in {inventory}"
                )
            source_mode = (
                source.get("render_mode")
                if view_kind == "segment"
                else source.get("mode")
            )
            if source_mode != "3d":
                raise CourseV2RuntimeError(
                    f"{location}.view_id {view_id!r} must reference a 3D {view_kind}"
                )
            if (
                view_kind == "segment"
                and source.get("evidence_readiness") != "evidence_ready"
            ):
                raise CourseV2RuntimeError(
                    f"{location}.view_id {view_id!r} must reference an evidence-ready segment"
                )
            source_title = _text(
                source.get("title"),
                f"{location}.source.title",
                maximum=180,
            )
            title = _text(view["title"], f"{location}.title", maximum=180)
            if title != source_title:
                raise CourseV2RuntimeError(
                    f"{location}.title must match the source view title {source_title!r}"
                )
            normalized_view = {
                "artifact": artifact,
                "view_kind": view_kind,
                "view_id": view_id,
                "view_index": (
                    segment_ids.index(view_id)
                    if view_kind == "segment"
                    else camera_ids.index(view_id)
                ),
                "title": title,
                "purpose": _text(view["purpose"], f"{location}.purpose", maximum=500),
                "boundary": _text(
                    view["boundary"], f"{location}.boundary", maximum=700
                ),
            }
            phase_states[phase_id][state_id]["spatial_view"] = normalized_view
            artifacts.add(artifact)
            view_count += 1
    return {
        "minimum_width_px": minimum_width,
        "state_view_count": view_count,
        "artifacts": sorted(artifacts),
    }


def _normalize_renderer_payload(
    payload: Mapping[str, Any],
    *,
    phase: Mapping[str, Any],
    manifest: Mapping[str, Any],
    location: str,
) -> dict[str, Any]:
    if type(payload["schema_version"]) is not int or payload["schema_version"] != 1:
        raise CourseV2RuntimeError(f"{location}.schema_version must be integer 1")
    pilot = payload["pilot"]
    if not isinstance(pilot, dict):
        raise CourseV2RuntimeError(f"{location}.pilot must be a mapping")
    missing = PILOT_REQUIRED_FIELDS - set(pilot)
    if missing:
        raise CourseV2RuntimeError(f"{location}.pilot missing {sorted(missing)}")
    base.validate_manual_interaction(
        pilot["interaction"], location=f"{location}.pilot.interaction"
    )
    pilot_phase = _exact(
        pilot["phase"], MANIFEST_PHASE_FIELDS, f"{location}.pilot.phase"
    )
    expected_phase = {
        "id": phase["id"],
        "number": phase["number"],
        "title": phase["title"],
        "anchor_question": phase["question"],
    }
    if pilot_phase != expected_phase:
        raise CourseV2RuntimeError(
            f"{location}: embedded phase contract does not match course spine"
        )
    if pilot["id"] != manifest["id"]:
        raise CourseV2RuntimeError(
            f"{location}: embedded pilot ID does not match manifest"
        )
    states_raw = payload["states"]
    if not isinstance(states_raw, list) or not 2 <= len(states_raw) <= 8:
        raise CourseV2RuntimeError(f"{location}.states must contain 2 to 8 states")
    states = [
        _normalize_state(record, f"{location}.states[{index}]")
        for index, record in enumerate(states_raw)
    ]
    ids = [state["id"] for state in states]
    nav_labels = [state["nav_label"] for state in states]
    if len(ids) != len(set(ids)) or len(nav_labels) != len(set(nav_labels)):
        raise CourseV2RuntimeError(
            f"{location}.states IDs and nav labels must be unique"
        )
    canvas = payload["canvas"]
    if not isinstance(canvas, dict) or not isinstance(canvas.get("kind"), str):
        raise CourseV2RuntimeError(f"{location}.canvas.kind must be text")
    return {
        "pilot_id": _identifier(pilot["id"], f"{location}.pilot.id"),
        "pilot_title": _text(pilot["title"], f"{location}.pilot.title", maximum=200),
        "learning_objective": _text(
            pilot["learning_objective"],
            f"{location}.pilot.learning_objective",
            maximum=700,
        ),
        "renderer_digest": base.validate_source_digest(payload["source_digest"]),
        "canvas_kind": _identifier(canvas["kind"], f"{location}.canvas.kind"),
        "states": states,
        "evidence": _normalize_evidence(payload["evidence"], f"{location}.evidence"),
    }


def compile_course_v2(
    spine: dict[str, Any],
    manifests: Mapping[str, dict[str, Any]],
    renderer_payloads: Mapping[str, dict[str, Any]],
    cameras: dict[str, Any],
    course_runtime: dict[str, Any],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Compile a strict six-phase registry from one course spine."""
    spine = _exact(spine, TOP_LEVEL_FIELDS, "course v2")
    forbidden = base._forbidden_fields(spine)
    if forbidden:
        raise CourseV2RuntimeError(
            f"course v2 contains pacing or scripting fields: {forbidden}"
        )
    if type(spine["schema_version"]) is not int or spine["schema_version"] != 1:
        raise CourseV2RuntimeError("course v2 schema_version must be integer 1")
    source_digest = base.validate_source_digest(source_digest)
    interaction = base.validate_manual_interaction(
        spine["interaction"], location="course v2.interaction"
    )
    journey_raw = _exact(spine["journey"], JOURNEY_FIELDS, "course v2.journey")
    journey_phase_ids = _list(
        journey_raw["phase_ids"],
        "course v2.journey.phase_ids",
        minimum=PHASE_COUNT,
        maximum=PHASE_COUNT,
        item_limit=80,
    )
    if journey_phase_ids != PHASE_IDS:
        raise CourseV2RuntimeError(
            f"course v2 journey phases must remain in canonical order {PHASE_IDS}"
        )
    phases_raw = spine["phases"]
    if not isinstance(phases_raw, list) or len(phases_raw) != PHASE_COUNT:
        raise CourseV2RuntimeError("course v2.phases must contain exactly six phases")
    if set(manifests) != set(PHASE_IDS) or set(renderer_payloads) != set(PHASE_IDS):
        raise CourseV2RuntimeError(
            "loaded manifests and renderer payloads must exactly match six phase IDs"
        )
    phases = []
    for index, raw_phase in enumerate(phases_raw):
        location = f"course v2.phases[{index}]"
        phase = _exact(raw_phase, PHASE_FIELDS, location)
        phase_id = _identifier(phase["id"], f"{location}.id")
        if phase_id != PHASE_IDS[index]:
            raise CourseV2RuntimeError(f"{location}.id must be {PHASE_IDS[index]!r}")
        if type(phase["number"]) is not int or phase["number"] != index + 1:
            raise CourseV2RuntimeError(f"{location}.number must be integer {index + 1}")
        normalized_phase = {
            "id": phase_id,
            "number": index + 1,
            "verb": _text(phase["verb"], f"{location}.verb", maximum=32),
            "title": _text(phase["title"], f"{location}.title", maximum=140),
            "question": _text(phase["question"], f"{location}.question", maximum=320),
            "manifest": _relative_path(
                phase["manifest"],
                f"{location}.manifest",
                prefix="course/pilots/",
                suffix=".yaml",
            ),
            "artifact": _relative_path(
                phase["artifact"],
                f"{location}.artifact",
                prefix="diagram/phase",
                suffix=".html",
            ),
            "carrier_in": _text(
                phase["carrier_in"], f"{location}.carrier_in", maximum=140
            ),
            "carrier_out": _text(
                phase["carrier_out"], f"{location}.carrier_out", maximum=140
            ),
        }
        manifest = manifests[phase_id]
        if not isinstance(manifest, dict):
            raise CourseV2RuntimeError(f"{location}: loaded manifest must be a mapping")
        manifest_phase = _exact(
            manifest.get("phase"),
            MANIFEST_PHASE_FIELDS,
            f"{location}.loaded_manifest.phase",
        )
        expected_manifest_phase = {
            "id": phase_id,
            "number": index + 1,
            "title": normalized_phase["title"],
            "anchor_question": normalized_phase["question"],
        }
        if manifest_phase != expected_manifest_phase:
            raise CourseV2RuntimeError(
                f"{location}: phase manifest does not match course spine"
            )
        base.validate_manual_interaction(
            manifest.get("interaction"),
            location=f"{location}.loaded_manifest.interaction",
        )
        manifest_forbidden = base._forbidden_fields(manifest)
        if manifest_forbidden:
            raise CourseV2RuntimeError(
                f"{location}: phase manifest contains pacing fields {manifest_forbidden}"
            )
        renderer = _normalize_renderer_payload(
            renderer_payloads[phase_id],
            phase=normalized_phase,
            manifest=manifest,
            location=f"{location}.renderer",
        )
        phases.append({**normalized_phase, **renderer})
    synthesis_raw = _exact(spine["synthesis"], SYNTHESIS_FIELDS, "course v2.synthesis")
    lenses_raw = synthesis_raw["lenses"]
    if not isinstance(lenses_raw, list) or len(lenses_raw) != 3:
        raise CourseV2RuntimeError(
            "course v2.synthesis.lenses must contain three lenses"
        )
    lenses = []
    for index, raw_lens in enumerate(lenses_raw):
        location = f"course v2.synthesis.lenses[{index}]"
        lens = _exact(raw_lens, LENS_FIELDS, location)
        readings = lens["phase_readings"]
        if not isinstance(readings, dict) or set(readings) != set(PHASE_IDS):
            raise CourseV2RuntimeError(
                f"{location}.phase_readings must map exactly the six phase IDs"
            )
        lenses.append(
            {
                "id": _identifier(lens["id"], f"{location}.id"),
                "title": _text(lens["title"], f"{location}.title", maximum=140),
                "question": _text(
                    lens["question"], f"{location}.question", maximum=360
                ),
                "phase_readings": {
                    phase_id: _text(
                        readings[phase_id],
                        f"{location}.phase_readings.{phase_id}",
                        maximum=480,
                    )
                    for phase_id in PHASE_IDS
                },
            }
        )
    expected_lens_ids = ["delivery_constraint", "ownership_and_risk", "usable_compute"]
    if [lens["id"] for lens in lenses] != expected_lens_ids:
        raise CourseV2RuntimeError(
            f"course v2 synthesis lenses must remain {expected_lens_ids}"
        )
    spatial = _normalize_spatial(spine["spatial"], cameras, course_runtime, phases)
    registry = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "course": {
            "id": _identifier(spine["id"], "course v2.id"),
            "title": _text(spine["title"], "course v2.title", maximum=100),
            "subtitle": _text(spine["subtitle"], "course v2.subtitle", maximum=260),
            "interaction": interaction,
        },
        "journey": {
            "id": _identifier(journey_raw["id"], "course v2.journey.id"),
            "title": _text(
                journey_raw["title"], "course v2.journey.title", maximum=180
            ),
            "anchor_question": _text(
                journey_raw["anchor_question"],
                "course v2.journey.anchor_question",
                maximum=520,
            ),
            "body": _text(journey_raw["body"], "course v2.journey.body", maximum=760),
            "phase_ids": journey_phase_ids,
        },
        "spatial": spatial,
        "phases": phases,
        "synthesis": {
            "id": _identifier(synthesis_raw["id"], "course v2.synthesis.id"),
            "title": _text(
                synthesis_raw["title"],
                "course v2.synthesis.title",
                maximum=180,
            ),
            "body": _text(
                synthesis_raw["body"],
                "course v2.synthesis.body",
                maximum=700,
            ),
            "lenses": lenses,
        },
    }
    compiled_forbidden = base._forbidden_fields(registry)
    if compiled_forbidden:
        raise CourseV2RuntimeError(
            f"compiled course v2 contains pacing fields {compiled_forbidden}"
        )
    return registry


def load_and_compile(
    root: Path,
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Load the spine, six manifests, and six materialized phase renderers."""
    root = root.resolve()
    spine = base.load_yaml(root / COURSE_PATH)
    cameras = base.load_yaml(root / CAMERAS_PATH)
    try:
        course_runtime = json.loads((root / COURSE_RUNTIME_PATH).read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise CourseV2RuntimeError(
            f"could not load {COURSE_RUNTIME_PATH.as_posix()}: {error}"
        ) from error
    phases = spine.get("phases")
    if not isinstance(phases, list):
        raise CourseV2RuntimeError("course v2.phases must be a list")
    manifests: dict[str, dict[str, Any]] = {}
    renderer_payloads: dict[str, dict[str, Any]] = {}
    for index, raw_phase in enumerate(phases):
        if not isinstance(raw_phase, dict):
            raise CourseV2RuntimeError(f"course v2.phases[{index}] must be a mapping")
        phase_id = raw_phase.get("id")
        if not isinstance(phase_id, str):
            raise CourseV2RuntimeError(f"course v2.phases[{index}].id must be text")
        manifest_path = _relative_path(
            raw_phase.get("manifest"),
            f"course v2.phases[{index}].manifest",
            prefix="course/pilots/",
            suffix=".yaml",
        )
        artifact_path = _relative_path(
            raw_phase.get("artifact"),
            f"course v2.phases[{index}].artifact",
            prefix="diagram/phase",
            suffix=".html",
        )
        manifests[phase_id] = base.load_yaml(root / manifest_path)
        try:
            rendered = (root / artifact_path).read_text()
        except OSError as error:
            raise CourseV2RuntimeError(
                f"could not load phase artifact {artifact_path}: {error}"
            ) from error
        renderer_payloads[phase_id] = extract_pilot_payload(
            rendered, location=f"phase artifact {artifact_path}"
        )
    return compile_course_v2(
        spine,
        manifests,
        renderer_payloads,
        cameras,
        course_runtime,
        source_digest=source_digest,
    )


def runtime_json(registry: Mapping[str, Any]) -> str:
    """Serialize one registry deterministically."""
    return json.dumps(registry, indent=2, sort_keys=True) + "\n"


def _escape(value: Any) -> str:
    return base._escape(value)


def _phase_compass(registry: Mapping[str, Any]) -> str:
    return "".join(
        f'<button class="phase-button" type="button" role="tab" '
        f'id="phase-tab-{_escape(phase["id"])}" aria-selected="false" '
        f'aria-controls="phase-view" '
        f'aria-label="Phase {phase["number"]}: {_escape(phase["title"])}" '
        f'title="Phase {phase["number"]}: {_escape(phase["title"])}" '
        f'data-phase-index="{index}"><span class="phase-number">'
        f'{phase["number"]:02d}</span><span class="phase-verb">'
        f"{_escape(phase['verb'])}</span></button>"
        for index, phase in enumerate(registry["phases"])
    )


def _journey_cards(registry: Mapping[str, Any]) -> str:
    cards = []
    for index, phase in enumerate(registry["phases"]):
        title = (
            ""
            if phase["verb"].casefold() == phase["title"].casefold()
            else f'<span class="journey-title">{_escape(phase["title"])}</span>'
        )
        cards.append(
            f'<button class="journey-card" type="button" data-open-phase="{index}" '
            f'aria-label="Open Phase {phase["number"]}: {_escape(phase["title"])}">'
            f'<span class="journey-number">{phase["number"]:02d}</span>'
            f"<strong>{_escape(phase['verb'])}</strong>"
            f"{title}"
            f'<p class="journey-question">{_escape(phase["question"])}</p>'
            f"<small>{_escape(phase['carrier_in'])} → {_escape(phase['carrier_out'])}</small>"
            "</button>"
        )
    return "".join(cards)


def _synthesis_matrix(registry: Mapping[str, Any]) -> str:
    lenses = registry["synthesis"]["lenses"]
    headings = "".join(
        f'<th scope="col"><span class="lens-number">0{index + 1}</span>'
        f"{_escape(lens['title'])}</th>"
        for index, lens in enumerate(lenses)
    )
    rows = []
    for phase in registry["phases"]:
        readings = "".join(
            f'<td data-lens-label="{_escape(lens["title"])}">'
            f'<span class="mobile-lens-label">{_escape(lens["title"])}</span>'
            f"<p>{_escape(lens['phase_readings'][phase['id']])}</p></td>"
            for lens in lenses
        )
        rows.append(
            f'<tr data-synthesis-phase="{_escape(phase["id"])}">'
            f'<th scope="row"><span class="journey-number">{phase["number"]:02d}</span>'
            f"<strong>{_escape(phase['verb'])}</strong>"
            f"<span>{_escape(phase['title'])}</span></th>{readings}</tr>"
        )
    return (
        '<div class="synthesis-matrix-wrap"><table class="synthesis-matrix">'
        f'<thead><tr><th scope="col">Phase</th>{headings}</tr></thead>'
        f"<tbody>{''.join(rows)}</tbody></table></div>"
    )


def _evidence_sections(registry: Mapping[str, Any]) -> str:
    sections = []
    for index, phase in enumerate(registry["phases"]):
        facts = base._evidence_html({"evidence": phase["evidence"]})
        sections.append(
            f'<section class="phase-evidence" data-evidence-phase-index="{index}" '
            f'hidden aria-label="Phase {phase["number"]} evidence">'
            f'<ul class="fact-list">{facts}</ul></section>'
        )
    return "".join(sections)


def render_player(registry: dict[str, Any]) -> str:
    """Render the unified manual v2 player as one self-contained shell."""
    if len(registry.get("phases", [])) != PHASE_COUNT:
        raise CourseV2RuntimeError("player registry must contain six phases")
    serialized = json.dumps(registry, sort_keys=True, separators=(",", ":")).replace(
        "</", "<\\/"
    )
    compass = _phase_compass(registry)
    journey_cards = _journey_cards(registry)
    synthesis_matrix = _synthesis_matrix(registry)
    evidence_sections = _evidence_sections(registry)
    course = registry["course"]
    journey = registry["journey"]
    synthesis = registry["synthesis"]
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="gigawatt-source-digest" content="{_escape(registry["source_digest"])}">
<title>{_escape(course["title"])} — six-phase course</title>
<style>
  :root {{ --paper:#f7f6f1; --white:#fff; --ink:#151716; --muted:#5d625f; --faint:#d2d3cc; --blue:#185f8f; --blue-soft:#e7f2f8; --green:#278a76; --green-soft:#e7f5f1; --amber:#aa6819; --amber-soft:#fff4e5; --evidence-clearance:64px; }}
  * {{ box-sizing:border-box; }} [hidden] {{ display:none !important; }}
  html,body {{ width:100%; height:100%; min-width:0; min-height:0; margin:0; overflow:hidden; background:var(--paper); color:var(--ink); font-family:Inter,"Helvetica Neue",Arial,sans-serif; }}
  body {{ display:grid; grid-template-rows:auto minmax(0,1fr) auto; height:100dvh; }}
  button {{ color:inherit; font:inherit; }} button:focus-visible,a:focus-visible,summary:focus-visible {{ outline:3px solid var(--blue); outline-offset:2px; }}
  header {{ min-width:0; display:grid; grid-template-columns:minmax(210px,.54fr) minmax(0,1.46fr); gap:14px; align-items:end; padding:8px 14px 9px; border-bottom:1.5px solid var(--ink); background:var(--paper); }}
  .brand-kicker,.phase-number,.state-number,.journey-number,.lens-number,.view-kicker,.carrier-label,.fact-ref {{ text-transform:uppercase; letter-spacing:.08em; font-weight:780; }}
  .brand-kicker {{ margin:0; color:var(--blue); font-size:10px; }} .brand h1 {{ margin:1px 0; font-size:24px; line-height:1; }} .brand-subtitle {{ margin:3px 0 0; color:var(--muted); font-size:11px; line-height:1.25; }}
  .phase-compass {{ min-width:0; display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:5px; }}
  .phase-button {{ min-width:0; min-height:43px; display:grid; grid-template-columns:auto 1fr; gap:6px; align-items:center; padding:5px 7px; border:1.5px solid var(--ink); background:transparent; cursor:pointer; }} .phase-button[aria-selected="true"] {{ background:var(--ink); color:white; }} .phase-number {{ font-size:9px; }} .phase-verb {{ min-width:0; font-size:12px; font-weight:720; overflow-wrap:anywhere; }}
  main {{ min-width:0; min-height:0; position:relative; overflow:hidden; }}
  .opening-view,.synthesis-view {{ width:100%; height:100%; overflow:auto; overscroll-behavior:contain; padding:clamp(14px,2.3vw,34px); }} .opening-inner,.synthesis-inner {{ max-width:1500px; margin:0 auto; }}
  .view-kicker {{ margin:0 0 8px; color:var(--blue); font-size:11px; }} .opening-view h2,.synthesis-view h2 {{ margin:0; font-size:clamp(26px,4vw,56px); line-height:1.02; }} .view-question {{ max-width:1120px; margin:12px 0 8px; font-size:clamp(16px,2vw,27px); font-weight:670; line-height:1.24; }} .view-body {{ max-width:1080px; margin:8px 0 18px; color:var(--muted); font-size:14px; line-height:1.45; }}
  .journey-grid {{ display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:8px; }} .journey-card {{ min-width:0; min-height:240px; display:flex; flex-direction:column; align-items:flex-start; gap:7px; padding:14px; border:1.5px solid var(--ink); background:var(--white); text-align:left; cursor:pointer; }} .journey-card:hover {{ background:var(--blue-soft); }} .journey-number {{ color:var(--blue); font-size:11px; }} .journey-card strong {{ font-size:20px; }} .journey-title {{ font-size:14px; font-weight:680; }} .journey-question {{ margin:1px 0; color:var(--ink); font-size:12px; font-weight:620; line-height:1.32; overflow-wrap:anywhere; }} .journey-card small {{ margin-top:auto; color:var(--muted); font-size:11px; line-height:1.35; overflow-wrap:anywhere; }}
  .phase-view {{ width:100%; height:100%; min-height:0; display:grid; grid-template-rows:auto minmax(0,1fr); overflow:hidden; }} .phase-context {{ min-width:0; display:grid; grid-template-columns:minmax(0,1fr) auto; gap:12px; align-items:center; padding:6px 14px; border-bottom:1px solid var(--faint); background:var(--white); }} .phase-heading {{ min-width:0; }} .phase-heading h2 {{ margin:0; font-size:18px; }} .phase-question {{ margin:2px 0 0; color:var(--muted); font-size:12px; line-height:1.25; }} .phase-tools {{ display:flex; align-items:center; gap:8px; margin-top:5px; }} .spatial-toggle {{ min-height:31px; padding:4px 8px; border:1.5px solid var(--blue); background:var(--blue-soft); color:var(--blue); cursor:pointer; font-size:10px; font-weight:760; }} .spatial-toggle[aria-pressed="true"] {{ background:var(--blue); color:white; }}
  .carrier-handoff {{ display:grid; grid-template-columns:minmax(95px,1fr) auto minmax(95px,1fr); gap:7px; align-items:center; min-width:300px; max-width:520px; }} .carrier-node {{ min-width:0; padding:6px 8px; border:1px solid var(--blue); border-radius:6px; background:var(--blue-soft); font-size:11px; font-weight:680; text-align:center; overflow-wrap:anywhere; }} .carrier-arrow {{ color:var(--blue); font-weight:850; }} .carrier-label {{ display:block; color:var(--muted); font-size:8px; }}
  .phase-frame-wrap {{ min-width:0; min-height:0; position:relative; padding:6px 10px; overflow:hidden; }} #phase-frame,#spatial-frame {{ display:block; width:100%; height:100%; min-width:0; min-height:0; border:1.5px solid var(--ink); background:var(--white); }} .spatial-panel {{ position:absolute; z-index:5; top:18px; right:22px; width:min(440px,calc(100% - 44px)); padding:11px 13px; border:1.5px solid var(--ink); background:color-mix(in srgb,var(--paper) 95%,transparent); box-shadow:0 4px 16px #15171624; pointer-events:none; }} .spatial-panel p {{ margin:3px 0; font-size:11px; line-height:1.35; }} .spatial-panel h3 {{ margin:2px 0 5px; font-size:17px; }} .spatial-panel .spatial-kicker {{ color:var(--blue); font-size:9px; font-weight:780; letter-spacing:.08em; text-transform:uppercase; }} .spatial-panel .spatial-boundary {{ color:var(--muted); font-size:10px; }} .frame-error {{ position:absolute; z-index:8; inset:12px; display:grid; place-items:center; padding:20px; border:2px solid var(--amber); background:var(--amber-soft); text-align:center; }}
  .synthesis-matrix-wrap {{ width:100%; min-width:0; margin-top:20px; overflow-x:hidden; }} .synthesis-matrix {{ width:100%; table-layout:fixed; border-collapse:collapse; background:var(--white); }} .synthesis-matrix th,.synthesis-matrix td {{ min-width:0; padding:10px 11px; border:1px solid var(--ink); vertical-align:top; overflow-wrap:anywhere; }} .synthesis-matrix thead th {{ background:var(--ink); color:white; font-size:13px; line-height:1.25; text-align:left; }} .synthesis-matrix thead th:first-child {{ width:15%; }} .synthesis-matrix tbody th {{ background:var(--blue-soft); text-align:left; }} .synthesis-matrix tbody th strong,.synthesis-matrix tbody th > span:last-child {{ display:block; }} .synthesis-matrix tbody th strong {{ margin:4px 0 2px; font-size:15px; }} .synthesis-matrix tbody th > span:last-child {{ color:var(--muted); font-size:11px; line-height:1.3; }} .synthesis-matrix td p {{ margin:0; font-size:12px; line-height:1.4; }} .lens-number {{ display:block; margin-bottom:4px; color:var(--blue); font-size:9px; }} .synthesis-matrix thead .lens-number {{ color:#9fd0e8; }} .mobile-lens-label {{ display:none; }}
  footer {{ min-width:0; min-height:0; max-height:54dvh; display:grid; grid-template-columns:auto minmax(0,1fr) auto minmax(280px,500px); gap:6px 10px; align-items:center; padding:7px 10px 8px; border-top:1.5px solid var(--ink); background:var(--paper); }}
  .course-step {{ min-width:54px; min-height:42px; padding:5px 7px; border:1.5px solid var(--ink); background:transparent; cursor:pointer; font-size:11px; font-weight:720; }} .course-step:disabled {{ color:#999; border-color:var(--faint); cursor:default; }}
  .state-nav {{ min-width:0; display:grid; grid-template-columns:repeat(6,minmax(0,1fr)); gap:4px; }} .state-button {{ min-width:0; min-height:42px; display:grid; grid-template-columns:auto 1fr; gap:5px; align-items:center; padding:5px 6px; border:1.5px solid var(--ink); background:transparent; text-align:left; cursor:pointer; }} .state-button[aria-selected="true"] {{ background:var(--ink); color:white; }} .state-button:disabled {{ color:#8a8d8b; border-color:var(--faint); background:#efeee9; cursor:default; }} .state-number {{ font-size:9px; }} .state-nav-label {{ min-width:0; font-size:11px; font-weight:680; overflow-wrap:anywhere; }}
  .state-copy {{ min-width:0; align-self:center; }} .state-copy h3 {{ margin:0 0 2px; font-size:14px; }} .state-copy p {{ margin:0; color:var(--muted); font-size:11px; line-height:1.25; }} .course-position {{ min-width:0; color:var(--muted); font-size:12px; text-align:center; }}
  details {{ position:fixed; z-index:30; right:10px; bottom:var(--evidence-clearance); width:min(520px,calc(100vw - 20px)); min-width:0; min-height:0; border:1.5px solid var(--ink); background:var(--paper); box-shadow:0 5px 18px #15171620; }} details[open] {{ right:10px; bottom:10px; width:min(780px,calc(100vw - 20px)); max-height:min(62dvh,560px); overflow:auto; overflow-x:hidden; overscroll-behavior:contain; box-shadow:0 12px 38px #15171638; }} summary {{ position:sticky; top:0; z-index:3; padding:7px 9px; background:var(--paper); cursor:pointer; font-size:12px; font-weight:720; }}
  .fact-list {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr)); gap:8px; margin:0; padding:4px 8px 8px; list-style:none; }} .fact-card {{ min-width:0; padding:8px 10px; border:1px solid var(--faint); background:var(--white); }} .fact-card p {{ margin:4px 0; font-size:11px; line-height:1.35; }} .fact-ref,.fact-boundary,.fact-sources,a {{ overflow-wrap:anywhere; word-break:break-word; }} .fact-ref,.fact-boundary {{ color:var(--muted); font-size:9px !important; }} a {{ color:var(--blue); }}
  .visually-hidden {{ position:absolute !important; width:1px; height:1px; overflow:hidden; clip:rect(1px,1px,1px,1px); white-space:nowrap; }}
  @media (max-width:1300px) {{ .phase-button,.state-button {{ grid-template-columns:1fr; gap:1px; text-align:center; }} .journey-grid {{ grid-template-columns:repeat(3,minmax(0,1fr)); }} .journey-card {{ min-height:150px; }} }}
  @media (max-width:899px) {{ .spatial-toggle,.spatial-panel {{ display:none !important; }} }}
  @media (max-width:1100px) {{ :root {{ --evidence-clearance:96px; }} header {{ grid-template-columns:190px minmax(0,1fr); }} .brand-subtitle {{ display:none; }} .phase-context {{ grid-template-columns:1fr; gap:4px; }} .carrier-handoff {{ width:100%; max-width:none; }} footer {{ grid-template-columns:auto minmax(0,1fr) auto; }} .state-copy {{ grid-column:1/-1; }} }}
  @media (max-height:520px) and (orientation:landscape) {{ :root {{ --evidence-clearance:44px; }} }}
  @media (max-height:520px) and (orientation:landscape) {{ header {{ grid-template-columns:145px minmax(0,1fr); gap:7px; padding:4px 7px; }} .brand h1 {{ font-size:18px; }} .brand-kicker {{ font-size:8px; }} .phase-button {{ min-height:31px; padding:2px 3px; }} .phase-number {{ display:none; }} .phase-verb {{ font-size:9px; }} .phase-context {{ grid-template-columns:minmax(0,1fr) minmax(300px,.9fr); padding:3px 8px; }} .phase-heading h2 {{ font-size:13px; }} .phase-question {{ font-size:9px; }} .carrier-handoff {{ min-width:0; }} .carrier-node {{ padding:3px 5px; font-size:9px; }} .phase-frame-wrap {{ padding:3px 6px; }} .opening-view,.synthesis-view {{ padding:8px; }} .opening-view h2,.synthesis-view h2 {{ font-size:23px; }} .view-question {{ margin:5px 0; font-size:13px; }} .view-body {{ margin:4px 0 7px; font-size:10px; }} .journey-grid {{ grid-template-columns:repeat(6,minmax(0,1fr)); gap:4px; }} .journey-card {{ min-height:105px; gap:3px; padding:6px; }} .journey-card strong {{ font-size:13px; }} .journey-card > span:not(.journey-number) {{ font-size:9px; }} .journey-card small {{ font-size:8px; }} .lens-grid {{ gap:6px; margin-top:8px; }} .lens-card {{ min-height:115px; padding:8px; }} .lens-card h3 {{ margin:4px 0; font-size:15px; }} .lens-card p {{ font-size:9px; }} footer {{ grid-template-columns:auto minmax(0,1fr) auto minmax(260px,.8fr); gap:3px 6px; padding:3px 6px 4px; max-height:60dvh; }} .course-step {{ min-width:42px; min-height:31px; padding:2px 4px; font-size:9px; }} .state-button {{ min-height:31px; padding:2px 3px; }} .state-number {{ display:none; }} .state-nav-label {{ font-size:9px; }} .state-copy {{ grid-column:auto; }} .state-copy h3 {{ font-size:10px; }} .state-copy p {{ font-size:9px; line-height:1.15; }} details {{ padding-top:1px; }} details[open] {{ max-height:75dvh; }} summary {{ padding:1px 0; font-size:9px; }} }}
  @media (max-width:520px) and (orientation:portrait) {{ header {{ grid-template-columns:1fr; gap:6px; padding:7px 7px 6px; }} .brand {{ display:flex; gap:7px; align-items:baseline; }} .brand h1 {{ font-size:20px; }} .brand-kicker {{ font-size:8px; }} .phase-compass {{ gap:3px; }} .phase-button {{ min-height:38px; padding:3px 2px; }} .phase-number {{ font-size:8px; }} .phase-verb {{ font-size:9px; }} .phase-context {{ padding:5px 7px; }} .phase-heading h2 {{ font-size:15px; }} .phase-question {{ font-size:10px; }} .carrier-handoff {{ min-width:0; gap:4px; }} .carrier-node {{ padding:4px; font-size:9px; }} .phase-frame-wrap {{ padding:4px; }} .opening-view,.synthesis-view {{ padding:12px 8px; }} .opening-view h2,.synthesis-view h2 {{ font-size:27px; }} .view-question {{ font-size:15px; }} .view-body {{ font-size:12px; }} .journey-grid,.lens-grid {{ grid-template-columns:1fr; }} .journey-card,.lens-card {{ min-height:0; }} footer {{ grid-template-columns:auto minmax(0,1fr) auto; gap:5px; padding:5px 6px 6px; max-height:58dvh; }} .course-step {{ min-width:42px; min-height:39px; padding:3px; font-size:9px; }} .state-nav {{ gap:3px; }} .state-button {{ min-height:39px; padding:3px 1px; }} .state-number {{ font-size:8px; }} .state-nav-label {{ font-size:9px; }} .state-copy {{ grid-column:1/-1; }} .state-copy h3 {{ font-size:12px; }} .state-copy p {{ font-size:10px; }} details[open] {{ max-height:72dvh; }} }}
  @media (max-height:520px) and (orientation:landscape) {{ details {{ padding-top:0; }} details[open] {{ max-height:82dvh; }} summary {{ padding:4px 6px; }} }}
  @media (max-height:520px) and (orientation:landscape) {{ .journey-question {{ font-size:9px; line-height:1.2; }} .synthesis-matrix-wrap {{ margin-top:6px; }} .synthesis-matrix th,.synthesis-matrix td {{ padding:4px; }} .synthesis-matrix thead th {{ font-size:9px; }} .synthesis-matrix tbody th strong {{ font-size:10px; }} .synthesis-matrix tbody th > span:last-child {{ font-size:8px; }} .synthesis-matrix td p {{ font-size:9px; line-height:1.2; }} }}
  @media (max-width:520px) and (orientation:portrait) {{ :root {{ --evidence-clearance:94px; }} details[open] {{ max-height:78dvh; }} .synthesis-matrix-wrap {{ margin-top:12px; }} .synthesis-matrix,.synthesis-matrix tbody,.synthesis-matrix tr,.synthesis-matrix th,.synthesis-matrix td {{ display:block; width:100%; }} .synthesis-matrix thead {{ display:none; }} .synthesis-matrix tr {{ margin-bottom:10px; border:1.5px solid var(--ink); }} .synthesis-matrix tbody th,.synthesis-matrix td {{ border:0; }} .synthesis-matrix tbody th {{ padding:9px; border-bottom:1px solid var(--ink); }} .synthesis-matrix td {{ padding:9px; border-bottom:1px solid var(--faint); }} .synthesis-matrix td:last-child {{ border-bottom:0; }} .mobile-lens-label {{ display:block; margin-bottom:4px; color:var(--blue); font-size:10px; font-weight:760; text-transform:uppercase; letter-spacing:.04em; }} .synthesis-matrix td p {{ font-size:12px; }} }}
</style>
</head>
<body>
<header>
  <div class="brand"><p class="brand-kicker">Six-phase course · manual</p><h1>{_escape(course["title"])}</h1><p class="brand-subtitle">{_escape(course["subtitle"])}</p></div>
  <nav class="phase-compass" role="tablist" aria-label="Six-phase course compass">{compass}</nav>
</header>
<main>
  <section id="opening-view" class="opening-view" aria-labelledby="opening-title">
    <div class="opening-inner"><p class="view-kicker">Opening journey</p><h2 id="opening-title">{_escape(journey["title"])}</h2><p class="view-question">{_escape(journey["anchor_question"])}</p><p class="view-body">{_escape(journey["body"])}</p><div class="journey-grid">{journey_cards}</div></div>
  </section>
  <section id="phase-view" class="phase-view" hidden aria-labelledby="current-phase-title">
    <div class="phase-context"><div class="phase-heading"><h2 id="current-phase-title"></h2><p id="current-phase-question" class="phase-question"></p><div class="phase-tools"><button id="spatial-toggle" class="spatial-toggle" type="button" aria-controls="phase-frame-wrap" aria-pressed="false" hidden>Open 2D explanation</button></div></div><div class="carrier-handoff" role="img" aria-label="Current phase system boundary; this is not a traced electron path"><div class="carrier-node"><span class="carrier-label">Phase input</span><span id="carrier-in"></span></div><span class="carrier-arrow" aria-hidden="true">→</span><div class="carrier-node"><span class="carrier-label">Phase output</span><span id="carrier-out"></span></div></div></div>
    <div id="phase-frame-wrap" class="phase-frame-wrap" data-spatial-mode="false"><aside id="spatial-panel" class="spatial-panel" hidden aria-labelledby="spatial-title"><p class="spatial-kicker">3D system view · conceptual</p><h3 id="spatial-title"></h3><p id="spatial-purpose"></p><p id="spatial-boundary" class="spatial-boundary"></p></aside><iframe id="phase-frame" title="Phase 2D explanation"></iframe><iframe id="spatial-frame" title="State-bound 3D system view" tabindex="-1" hidden></iframe><p id="frame-error" class="frame-error" hidden></p></div>
  </section>
  <section id="synthesis-view" class="synthesis-view" hidden aria-labelledby="synthesis-title"><div class="synthesis-inner"><p class="view-kicker">Closing synthesis</p><h2 id="synthesis-title">{_escape(synthesis["title"])}</h2><p class="view-body">{_escape(synthesis["body"])}</p>{synthesis_matrix}</div></section>
</main>
<footer>
  <button id="course-prev" class="course-step" type="button" aria-label="Previous course view">Back</button>
  <nav id="state-nav" class="state-nav" role="tablist" aria-label="Manual teaching states"></nav>
  <button id="course-next" class="course-step" type="button" aria-label="Next course view">Next</button>
  <section id="state-copy" class="state-copy" aria-labelledby="state-title"><h3 id="state-title"></h3><p id="state-instruction"></p></section>
  <p id="state-status" class="visually-hidden" aria-live="polite"></p>
  <details id="evidence-drawer" data-layout-mode="overlay" hidden><summary><span id="evidence-summary">Evidence</span></summary>{evidence_sections}</details>
</footer>
<script id="course-data" type="application/json">{serialized}</script>
<script>
"use strict";
if ("scrollRestoration" in history) history.scrollRestoration = "manual";
const course = JSON.parse(document.getElementById("course-data").textContent);
const openingView = document.getElementById("opening-view");
const phaseView = document.getElementById("phase-view");
const synthesisView = document.getElementById("synthesis-view");
const teachingFrame = document.getElementById("phase-frame");
const spatialFrame = document.getElementById("spatial-frame");
const frameWrap = document.getElementById("phase-frame-wrap");
const frameError = document.getElementById("frame-error");
const spatialToggle = document.getElementById("spatial-toggle");
const spatialPanel = document.getElementById("spatial-panel");
const spatialTitle = document.getElementById("spatial-title");
const spatialPurpose = document.getElementById("spatial-purpose");
const spatialBoundary = document.getElementById("spatial-boundary");
const spatialQuery = matchMedia("(min-width: {registry["spatial"]["minimum_width_px"]}px)");
const phaseButtons = [...document.querySelectorAll("[data-phase-index]")];
const stateNav = document.getElementById("state-nav");
const stateCopy = document.getElementById("state-copy");
const evidenceDrawer = document.getElementById("evidence-drawer");
const previousButton = document.getElementById("course-prev");
const nextButton = document.getElementById("course-next");
let mode = "opening";
let currentPhase = 0;
let currentState = 0;
let spatialMode = false;

function resetScroll() {{
  window.scrollTo(0, 0);
  if (document.scrollingElement) {{ document.scrollingElement.scrollTop = 0; document.scrollingElement.scrollLeft = 0; }}
  [document.querySelector("main"), openingView, synthesisView, evidenceDrawer].forEach(element => {{
    if (!element) return; element.scrollTop = 0; element.scrollLeft = 0;
  }});
  [teachingFrame, spatialFrame].forEach(frame => {{
    try {{
      frame.contentWindow.scrollTo(0, 0);
      if (frame.contentDocument.scrollingElement) frame.contentDocument.scrollingElement.scrollTop = 0;
      const childMain = frame.contentDocument.querySelector("main");
      if (childMain) {{ childMain.scrollTop = 0; childMain.scrollLeft = 0; }}
    }} catch (error) {{ /* same-origin frame may still be loading */ }}
  }});
}}

function selectCompass(index) {{
  const fallbackIndex = mode === "synthesis" ? course.phases.length - 1 : 0;
  phaseButtons.forEach((button, buttonIndex) => {{
    const selected = mode === "phase" && buttonIndex === index;
    const keyboardTarget = selected || (mode !== "phase" && buttonIndex === fallbackIndex);
    button.setAttribute("aria-selected", String(selected)); button.tabIndex = keyboardTarget ? 0 : -1;
  }});
}}

function showEvidence(index) {{
  document.querySelectorAll("[data-evidence-phase-index]").forEach(section => {{
    section.toggleAttribute("hidden", Number(section.dataset.evidencePhaseIndex) !== index);
  }});
  const phase = course.phases[index];
  document.getElementById("evidence-summary").textContent = `Evidence · Phase ${{phase.number}} · ${{phase.evidence.facts.length}} facts · ${{phase.evidence.sources.length}} sources`;
  evidenceDrawer.hidden = false;
}}

function currentSpatialView() {{
  if (mode !== "phase") return null;
  return course.phases[currentPhase].states[currentState].spatial_view || null;
}}

function syncSpatialControl() {{
  const available = Boolean(currentSpatialView()) && spatialQuery.matches;
  spatialToggle.hidden = !available;
  spatialToggle.disabled = !available;
  spatialToggle.setAttribute("aria-pressed", String(spatialMode && available));
  spatialToggle.textContent = spatialMode && available ? "Open 2D explanation" : "Return to 3D system view";
}}

function buildStateNav() {{
  const phase = course.phases[currentPhase];
  stateNav.replaceChildren();
  stateNav.style.gridTemplateColumns = `repeat(${{phase.states.length}}, minmax(0, 1fr))`;
  phase.states.forEach((state, index) => {{
    const button = document.createElement("button"); button.type = "button"; button.className = "state-button"; button.setAttribute("role", "tab");
    button.dataset.stateIndex = String(index); button.setAttribute("aria-controls", "phase-frame-wrap"); button.setAttribute("aria-label", `State ${{index + 1}}: ${{state.title}}`); button.title = state.title;
    const number = document.createElement("span"); number.className = "state-number"; number.textContent = String(index + 1).padStart(2, "0");
    const label = document.createElement("span"); label.className = "state-nav-label"; label.textContent = state.nav_label;
    button.append(number, label); button.addEventListener("click", () => activateState(index)); stateNav.append(button);
  }});
}}

function activateState(index, focusButton = false) {{
  const phase = course.phases[currentPhase]; currentState = Math.max(0, Math.min(phase.states.length - 1, index)); const state = phase.states[currentState];
  [...stateNav.querySelectorAll("[data-state-index]")].forEach((button, buttonIndex) => {{ const selected = buttonIndex === currentState; button.setAttribute("aria-selected", String(selected)); button.tabIndex = selected ? 0 : -1; }});
  document.getElementById("state-title").textContent = state.title; document.getElementById("state-instruction").textContent = state.instruction;
  document.getElementById("state-status").textContent = `Phase ${{phase.number}}, state ${{currentState + 1}} of ${{phase.states.length}}: ${{state.title}}. ${{state.instruction}}`;
  if (currentSpatialView() && spatialQuery.matches) showSpatial(); else showTeaching();
  resetScroll(); if (focusButton) stateNav.querySelector(`[data-state-index="${{currentState}}"]`).focus();
}}

function bindChildNavigation(child) {{
  if (child.documentElement.dataset.courseV2OuterKeys === "bound") return;
  child.documentElement.dataset.courseV2OuterKeys = "bound";
  child.addEventListener("keydown", event => {{
    if (!["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End", "Escape"].includes(event.key)) return;
    event.preventDefault(); event.stopImmediatePropagation();
    if (event.key !== "Escape") return;
    if (evidenceDrawer.open) {{ evidenceDrawer.open = false; resetScroll(); return; }}
    if (spatialMode) {{ showTeaching(true); return; }}
    stateNav.querySelector(`[data-state-index="${{currentState}}"]`)?.focus();
  }}, true);
}}

function prepareTeachingFrame() {{
  if (mode !== "phase") return;
  const phase = course.phases[currentPhase];
  const artifact = phase.artifact.replace("diagram/", "");
  if (teachingFrame.dataset.artifact !== artifact) return;
  try {{ if (!teachingFrame.contentWindow.location.pathname.endsWith(`/${{artifact}}`)) return; }} catch (error) {{ return; }}
  try {{
    const child = teachingFrame.contentDocument; const digest = child.querySelector('meta[name="gigawatt-source-digest"]')?.content;
    if (digest !== phase.renderer_digest) throw new Error("renderer digest mismatch");
    let style = child.getElementById("course-v2-component-style"); if (!style) {{ style = child.createElement("style"); style.id = "course-v2-component-style"; child.head.append(style); }}
    style.textContent = "html,body{{width:100%!important;height:100%!important;min-height:0!important;overflow:hidden!important}}body{{display:block!important}}header,footer{{display:none!important}}main{{width:100%!important;height:100dvh!important;min-height:0!important;padding:4px!important}}@media (min-width:1281px){{main{{place-items:center!important;overflow:hidden!important}}.visual-shell{{display:block!important}}.responsive-visual{{display:none!important}}}}";
    bindChildNavigation(child);
    if (typeof teachingFrame.contentWindow.activate !== "function") throw new Error("phase activate function unavailable");
    teachingFrame.contentWindow.activate(currentState);
    teachingFrame.title = `Phase ${{phase.number}}: ${{phase.title}} 2D explanation`;
    if (!spatialMode) frameError.hidden = true;
  }} catch (error) {{ if (!spatialMode) {{ frameError.hidden = false; frameError.textContent = "The phase visual failed its same-origin source check."; }} }}
}}

function prepareSpatialFrame() {{
  const phase = course.phases[currentPhase]; const view = currentSpatialView();
  if (!view || !spatialQuery.matches || !spatialMode) return;
  const artifact = view.artifact.replace("diagram/", "");
  if (spatialFrame.dataset.artifact !== artifact) return;
  try {{ if (!spatialFrame.contentWindow.location.pathname.endsWith(`/${{artifact}}`)) return; }} catch (error) {{ return; }}
  try {{
    const child = spatialFrame.contentDocument;
    let style = child.getElementById("course-v2-spatial-style"); if (!style) {{ style = child.createElement("style"); style.id = "course-v2-spatial-style"; child.head.append(style); }}
    let control;
    if (view.view_kind === "segment") {{
      style.textContent = ":root{{--rail:0px!important;--head:0px!important;--transport:0px!important}}#shot-rail,#masthead,#transport{{display:none!important}}#stage{{inset:0!important}}";
      const data = JSON.parse(child.getElementById("review-data").textContent);
      const segment = data.registry.segments[view.view_index];
      if (!segment || segment.segment_id !== view.view_id || segment.title !== view.title || segment.render_mode !== "3d") throw new Error("spatial segment contract mismatch");
      const shots = [...child.querySelectorAll("#shot-list > .shot-button")]; control = shots[view.view_index];
      if (shots.length !== data.registry.segments.length || !control || control.title !== view.title || !child.getElementById("teaching-overlay")) throw new Error("spatial segment control mismatch");
      control.click();
      if (control.getAttribute("aria-current") !== "step" || child.getElementById("shot-id").textContent !== view.view_id || !child.getElementById("mode").textContent.includes("3d")) throw new Error("spatial segment activation postcondition failed");
    }} else if (view.view_kind === "camera") {{
      style.textContent = "#masthead,#transport{{display:none!important}}";
      const scene = JSON.parse(child.getElementById("scene-data").textContent);
      const camera = scene.cameras[view.view_index];
      if (!camera || scene.vertical_slice[view.view_index] !== view.view_id || camera.id !== view.view_id || camera.mode !== "3d" || camera.title !== view.title) throw new Error("spatial camera contract mismatch");
      const steps = [...child.querySelectorAll("#steps > .step")]; control = steps[view.view_index];
      if (steps.length !== scene.cameras.length || !control || control.textContent.trim() !== view.title) throw new Error("spatial camera control mismatch");
      control.click();
      if (control.getAttribute("aria-current") !== "step" || child.getElementById("mode").textContent !== "3d" || child.getElementById("state-title").textContent !== view.title) throw new Error("spatial camera activation postcondition failed");
    }} else {{
      throw new Error("unsupported spatial view kind");
    }}
    bindChildNavigation(child);
    frameError.hidden = true; spatialFrame.title = `3D system view · Phase ${{phase.number}} · ${{view.title}}`;
    document.getElementById("state-status").textContent = `Phase ${{phase.number}} 3D system view: ${{view.title}}. ${{view.purpose}}`;
    resetScroll();
  }} catch (error) {{ frameError.hidden = false; frameError.textContent = "The 3D system view failed its same-origin view check."; }}
}}

function showSpatial() {{
  const view = currentSpatialView();
  if (!view || !spatialQuery.matches) return;
  spatialMode = true; frameError.hidden = true; frameWrap.dataset.spatialMode = "true"; teachingFrame.hidden = true; spatialFrame.hidden = false; spatialFrame.tabIndex = -1;
  spatialTitle.textContent = view.title; spatialPurpose.textContent = view.purpose; spatialBoundary.textContent = view.boundary; spatialPanel.hidden = false; syncSpatialControl(); prepareTeachingFrame();
  const artifact = view.artifact.replace("diagram/", "");
  if (spatialFrame.dataset.artifact !== artifact) {{ spatialFrame.dataset.artifact = artifact; spatialFrame.src = artifact; }} else {{ prepareSpatialFrame(); }}
}}

function showTeaching(focusToggle = false) {{
  if (mode !== "phase") return;
  spatialMode = false; frameError.hidden = true; frameWrap.dataset.spatialMode = "false"; teachingFrame.hidden = false; teachingFrame.removeAttribute("tabindex"); spatialFrame.hidden = true; spatialPanel.hidden = true; syncSpatialControl();
  const phase = course.phases[currentPhase]; const artifact = phase.artifact.replace("diagram/", "");
  if (teachingFrame.dataset.artifact !== artifact) {{ teachingFrame.dataset.artifact = artifact; teachingFrame.src = artifact; }} else {{ prepareTeachingFrame(); }}
  if (focusToggle) {{ const target = !spatialToggle.hidden ? spatialToggle : stateNav.querySelector(`[data-state-index="${{currentState}}"]`); if (target) target.focus(); }}
}}

function showOpening() {{
  mode = "opening"; spatialMode = false; teachingFrame.removeAttribute("tabindex"); spatialPanel.hidden = true; frameWrap.dataset.spatialMode = "false"; openingView.hidden = false; phaseView.hidden = true; synthesisView.hidden = true; stateNav.replaceChildren();
  stateCopy.hidden = true; evidenceDrawer.open = false; evidenceDrawer.hidden = true; previousButton.disabled = true; nextButton.disabled = false; nextButton.textContent = "Start";
  document.getElementById("state-status").textContent = "Opening journey"; selectCompass(-1); syncSpatialControl(); resetScroll();
}}

function showPhase(index) {{
  mode = "phase"; spatialMode = false; teachingFrame.removeAttribute("tabindex"); spatialPanel.hidden = true; frameWrap.dataset.spatialMode = "false"; currentPhase = Math.max(0, Math.min(course.phases.length - 1, index)); currentState = 0; const phase = course.phases[currentPhase];
  openingView.hidden = true; phaseView.hidden = false; synthesisView.hidden = true; stateCopy.hidden = false; evidenceDrawer.open = false;
  document.getElementById("current-phase-title").textContent = `Phase ${{phase.number}} · ${{phase.title}}`; document.getElementById("current-phase-question").textContent = phase.question;
  document.getElementById("carrier-in").textContent = phase.carrier_in; document.getElementById("carrier-out").textContent = phase.carrier_out;
  previousButton.disabled = false; previousButton.textContent = currentPhase === 0 ? "Opening" : "Previous phase"; nextButton.disabled = false; nextButton.textContent = currentPhase === course.phases.length - 1 ? "Synthesis" : "Next phase";
  selectCompass(currentPhase); buildStateNav(); showEvidence(currentPhase);
  const artifact = phase.artifact.replace("diagram/", ""); if (teachingFrame.dataset.artifact !== artifact) {{ teachingFrame.dataset.artifact = artifact; teachingFrame.src = artifact; }}
  activateState(0);
}}

function showSynthesis() {{
  mode = "synthesis"; spatialMode = false; teachingFrame.removeAttribute("tabindex"); spatialPanel.hidden = true; frameWrap.dataset.spatialMode = "false"; openingView.hidden = true; phaseView.hidden = true; synthesisView.hidden = false; stateNav.replaceChildren(); stateCopy.hidden = true;
  evidenceDrawer.open = false; evidenceDrawer.hidden = true; previousButton.disabled = false; previousButton.textContent = "Phase 6"; nextButton.disabled = true; nextButton.textContent = "Complete";
  document.getElementById("state-status").textContent = "Closing synthesis"; selectCompass(-1); syncSpatialControl(); resetScroll();
}}

phaseButtons.forEach((button, index) => button.addEventListener("click", () => showPhase(index)));
document.querySelectorAll("[data-open-phase]").forEach(button => button.addEventListener("click", () => showPhase(Number(button.dataset.openPhase))));
document.querySelector(".phase-compass").addEventListener("keydown", event => {{
  let target = null; if (event.key === "ArrowRight" || event.key === "ArrowDown") target = currentPhase + 1; if (event.key === "ArrowLeft" || event.key === "ArrowUp") target = currentPhase - 1; if (event.key === "Home") target = 0; if (event.key === "End") target = course.phases.length - 1;
  if (target !== null) {{ event.preventDefault(); showPhase(Math.max(0, Math.min(course.phases.length - 1, target))); phaseButtons[currentPhase].focus(); }}
}});
stateNav.addEventListener("keydown", event => {{
  let target = null; const states = course.phases[currentPhase].states; if (event.key === "ArrowRight" || event.key === "ArrowDown") target = currentState + 1; if (event.key === "ArrowLeft" || event.key === "ArrowUp") target = currentState - 1; if (event.key === "Home") target = 0; if (event.key === "End") target = states.length - 1;
  if (target !== null) {{ event.preventDefault(); activateState(target, true); }}
}});
previousButton.addEventListener("click", () => {{ if (mode === "synthesis") showPhase(course.phases.length - 1); else if (mode === "phase" && currentPhase === 0) showOpening(); else if (mode === "phase") showPhase(currentPhase - 1); }});
nextButton.addEventListener("click", () => {{ if (mode === "opening") showPhase(0); else if (mode === "phase" && currentPhase === course.phases.length - 1) showSynthesis(); else if (mode === "phase") showPhase(currentPhase + 1); }});
spatialToggle.addEventListener("click", () => {{ if (spatialMode) showTeaching(false); else showSpatial(); }});
spatialQuery.addEventListener("change", event => {{
  if (mode !== "phase") {{ syncSpatialControl(); return; }}
  if (event.matches && currentSpatialView()) showSpatial(); else if (spatialMode) showTeaching(true); else syncSpatialControl();
}});
teachingFrame.addEventListener("load", prepareTeachingFrame);
spatialFrame.addEventListener("load", prepareSpatialFrame);
evidenceDrawer.addEventListener("toggle", () => {{ if (!evidenceDrawer.open) resetScroll(); }});
document.addEventListener("keydown", event => {{ if (event.key !== "Escape") return; if (evidenceDrawer.open) {{ evidenceDrawer.open = false; resetScroll(); return; }} if (spatialMode) showTeaching(true); }});
showOpening();
</script>
</body>
</html>
"""


def render_instructor_packet(registry: Mapping[str, Any]) -> str:
    """Render the manual v2 instructor packet from the same registry."""
    course = registry["course"]
    journey = registry["journey"]
    lines = [
        f"# {course['title']} v2 Instructor Packet",
        "",
        course["subtitle"],
        "",
        "This is teaching territory, not a spoken script. The instructor controls every advance and decides when the current explanation is complete.",
        "",
        "## Run and test",
        "",
        "```sh",
        "python3 -m http.server --directory diagram 8000",
        "```",
        "",
        "Open `http://localhost:8000/course_v2.html`. Use the six-phase compass to move between engineering problems and the state rail to change the current teaching visual. At 900 px and wider, mapped states open on their state-bound 3D system view; use `Open 2D explanation` for causal and evidence detail, then `Return to 3D system view` when useful. The outer evidence drawer contains the fact-level basis, scope, posture, date boundary, and primary-source links for the active phase.",
        "",
        f"Machine registry source digest: `{registry['source_digest']}`",
        "",
        "## Opening journey",
        "",
        f"**{journey['title']}**",
        "",
        journey["anchor_question"],
        "",
        journey["body"],
        "",
    ]
    for phase in registry["phases"]:
        lines.extend(
            [
                f"## Phase {phase['number']}: {phase['title']}",
                "",
                f"**Anchor question:** {phase['question']}",
                "",
                f"**Phase boundary:** {phase['carrier_in']} → {phase['carrier_out']}",
                "",
                f"**Learning objective:** {phase['learning_objective']}",
                "",
            ]
        )
        lines.extend(["### Manual teaching states", ""])
        for index, state in enumerate(phase["states"]):
            lines.extend(
                [
                    f"{index + 1}. **{state['nav_label']} — {state['title']}**",
                    f"   {state['instruction']}",
                ]
            )
            spatial_view = state.get("spatial_view")
            if spatial_view is not None:
                lines.extend(
                    [
                        f"   **3D system view:** {spatial_view['title']} — {spatial_view['purpose']}",
                        f"   **Spatial boundary:** {spatial_view['boundary']}",
                    ]
                )
        publishers = sorted(
            {source["publisher"] for source in phase["evidence"]["sources"]}
        )
        lines.extend(
            [
                "",
                "### Evidence boundary",
                "",
                f"{len(phase['evidence']['facts'])} bound facts from {len(phase['evidence']['sources'])} sources.",
                "",
                "Publishers: " + "; ".join(publishers),
                "",
            ]
        )
    synthesis = registry["synthesis"]
    lines.extend(
        [
            "## Closing synthesis",
            "",
            f"**{synthesis['title']}**",
            "",
            synthesis["body"],
            "",
        ]
    )
    for lens in synthesis["lenses"]:
        lines.extend([f"### {lens['title']}", "", lens["question"], ""])
        for phase in registry["phases"]:
            lines.append(
                f"- **Phase {phase['number']} · {phase['verb']}:** "
                f"{lens['phase_readings'][phase['id']]}"
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"
