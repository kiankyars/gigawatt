"""Build the complete untimed course player and instructor packet.

The course manifest owns order and pedagogy. The planned-shot compiler owns
derived provisional frames, reusable cameras own context, and evidence ledgers
own factual claims. This module packages those inputs without adding timing,
spoken scripts, or automatic advance.

Usage: uv run python -m gigawatt.course_runtime
"""

from __future__ import annotations

import hashlib
from collections.abc import Iterable
from pathlib import Path
from typing import Any

from . import layout as layout_pipeline
from . import scene as scene_pipeline
from . import shots, tokens

ROOT = Path(__file__).resolve().parents[2]
DIAGRAM = ROOT / "diagram"
COURSE_PATH = ROOT / "course" / "segments.yaml"
REGISTRY_PATH = DIAGRAM / "course_runtime.json"
PLAYER_PATH = DIAGRAM / "course.html"
PACKET_PATH = ROOT / "course" / "INSTRUCTOR_PACKET.md"

SCHEMA_VERSION = 1
EXPECTED_ACTS = 7
EXPECTED_SEGMENTS = 26
FORBIDDEN_RUNTIME_KEYS = {
    "autoplay",
    "beat",
    "beats",
    "cadence",
    "duration",
    "runtime",
    "script",
    "timing",
}

PROMOTION_GUARD_WARNINGS = {
    "announced_to_operational": "An announced structure or role does not prove current operation.",
    "anticipated_to_measured": "An anticipated value is not a measured operating result.",
    "capacity_basis_substitution": "Do not substitute one capacity, power, energy, or compute basis for another.",
    "conceptual_to_as_built": "Conceptual geometry is not an as-built connection or equipment configuration.",
    "contractual_to_physical": "A contract or commercial role does not establish physical power flow or asset control.",
    "design_ceiling_to_installed": "A design ceiling does not establish installed or operating quantity.",
    "design_to_as_built": "A design or engineering reference is not proof of the site's as-built condition.",
    "energy_power_time_basis": "Keep power rates and energy totals on one explicit, matching averaging interval.",
    "excluded_scope_addition": "Do not add explicitly excluded assets or capacity to the taught scope.",
    "facility_financing_to_component_allocation": "Do not allocate facility-level finance, acceptance, rent, or utilization terms to individual equipment; those terms remain undisclosed.",
    "future_design_to_operational": "A future design is not installed, commissioned, or operational.",
    "live_by_to_start_date": "A live-by disclosure is only an upper date bound, not an exact start date.",
    "market_example_to_site_schedule": "Market lead times and product availability examples do not establish Abilene's schedule or critical path.",
    "minimum_to_exact": "A confirmed minimum is not an exact current count.",
    "model_range_to_site_configuration": "A manufacturer range does not reveal the site's selected setting.",
    "named_role_to_asset_assignment": "Do not apply program, project, phase, or operating-part roles to every highlighted asset; their published scopes remain distinct.",
    "null_to_zero": "Unknown means not established by the cited evidence; it does not mean zero or absent.",
    "permitted_to_commissioned": "A permit does not prove equipment was commissioned.",
    "permitted_to_installed": "A permit does not prove equipment was installed.",
    "planned_to_operational": "A planned milestone or capacity is not operational evidence.",
    "power_to_compute_bridge": "Do not convert power to compute without matching hardware quantity, measured power, workload efficiency, and system boundaries.",
    "product_to_site_configuration": "A product specification does not establish the site's selected configuration or operating point.",
    "reverse_physical_flow": "Do not reverse supply, return, heat, or electrical direction while explaining the diagram.",
    "scenario_to_site_estimate": "A derived scenario is not a site estimate; missing site inputs must stop the calculation.",
    "single_path_conflation": "Do not identify distinct named, planned, conceptual, or energized paths as one completed physical path.",
    "site_scope_transfer": "A fact applies only to its stated scope; highlighted geometry does not transfer it to other assets or phases.",
    "substation_to_it_load": "Substation or feeder capacity does not establish current facility load or critical IT load.",
    "untyped_to_capacity": "An untyped delivery percentage does not establish MW, buildings, racks, accelerators, or workload capacity.",
}


class CourseRuntimeError(ValueError):
    """Raised when the production package drifts from a canonical input."""


def load_inputs() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    dict[str, dict[str, Any]],
]:
    course = scene_pipeline.load_yaml(COURSE_PATH)
    cameras = scene_pipeline.load_yaml(DIAGRAM / "cameras.yaml")
    master = scene_pipeline.load_yaml(DIAGRAM / "master.yaml")
    layout = scene_pipeline.load_yaml(DIAGRAM / "layout.yaml")
    scene = scene_pipeline.load_yaml(DIAGRAM / "scene.yaml")
    ledgers = {
        ledger_id: scene_pipeline.load_yaml(ROOT / relative_path)
        for ledger_id, relative_path in course["meta"]["evidence_ledgers"].items()
    }
    return course, cameras, master, layout, scene, ledgers


def _source_digest(course: dict[str, Any]) -> str:
    paths = [
        Path(__file__).resolve(),
        Path(shots.__file__).resolve(),
        Path(scene_pipeline.__file__).resolve(),
        Path(layout_pipeline.__file__).resolve(),
        Path(tokens.__file__).resolve(),
        COURSE_PATH,
        DIAGRAM / "cameras.yaml",
        DIAGRAM / "master.yaml",
        DIAGRAM / "layout.yaml",
        DIAGRAM / "scene.yaml",
        DIAGRAM / "vendor" / "three" / "three.module.js",
        DIAGRAM / "vendor" / "three" / "OrbitControls.js",
        DIAGRAM / "vendor" / "three" / "CSS2DRenderer.js",
        DIAGRAM / "vendor" / "three" / "LICENSE",
        *(
            ROOT / path
            for _, path in sorted(course["meta"]["evidence_ledgers"].items())
        ),
    ]
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.relative_to(ROOT).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _walk_keys(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key)
            yield from _walk_keys(nested)
    elif isinstance(value, list):
        for nested in value:
            yield from _walk_keys(nested)


def _display_value(fact: dict[str, Any]) -> str:
    value = fact["value"]
    if value is None:
        if fact["posture"] == "no_evidence_backed_estimate":
            return "No evidence-backed estimate"
        return "Unknown — not established by the cited evidence"
    if isinstance(value, bool):
        rendered = "Yes" if value else "No"
    else:
        rendered = str(value)
    unit = fact.get("unit")
    if not unit:
        return rendered
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return f"{rendered} {unit}"
    return f"{rendered} ({unit})"


def _script_safe_payload(payload: dict[str, Any]) -> str:
    return scene_pipeline.canonical_payload(payload).replace("</", "<\\/")


def _claim_card(
    claim: dict[str, Any], ledgers: dict[str, dict[str, Any]]
) -> dict[str, Any]:
    fact_cards: list[dict[str, Any]] = []
    for fact_ref in claim["fact_refs"]:
        ledger_id, fact_id = fact_ref.split(":", 1)
        ledger = ledgers[ledger_id]
        fact = ledger["facts"][fact_id]
        sources = []
        for source_id in fact["source_ids"]:
            source = ledger["sources"][source_id]
            sources.append(
                {
                    "id": source_id,
                    "publisher": source["publisher"],
                    "title": source["title"],
                    "url": source["url"],
                }
            )
        fact_cards.append(
            {
                "ref": fact_ref,
                "value": _display_value(fact),
                "scope": fact["scope"],
                "basis": fact["basis"],
                "lifecycle": fact["lifecycle"],
                "posture": fact["posture"],
                "as_of": fact["as_of"],
                "sources": sources,
            }
        )
    return {
        "id": claim["id"],
        "assertion": claim["assertion"],
        "binding": claim["binding"],
        "facts": fact_cards,
    }


def _frame_for_segment(
    segment: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
) -> dict[str, Any]:
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    anchor = camera_map[segment["camera"]["anchor"]]
    render_mode = "3d" if anchor["mode"] == "3d" else "2d"
    if render_mode == "3d":
        return shots._derive_3d_frame(
            segment["node_ids"], segment["edge_ids"], anchor, scene
        )

    node_records, edge_records = shots._exact_geometry_coverage(master, layout, scene)
    del node_records
    geoms = layout_pipeline.build_geoms(layout, master, layout["frame"]["ground"])
    points: list[tuple[float, float]] = []
    for node_id in segment["node_ids"]:
        points.extend(shots._layout_node_points(node_id, layout))
    for edge_id in segment["edge_ids"]:
        points.extend(shots._layout_edge_points(edge_id, layout, edge_records, geoms))
    anchor_view = anchor.get("viewBox") or anchor.get("map_view")
    return {
        "kind": "2d",
        "viewBox": shots._fit_2d_view(points, layout["frame"]),
        "anchor_viewBox": [float(value) for value in anchor_view],
    }


def compile_registry(
    course: dict[str, Any],
    cameras: dict[str, Any],
    master: dict[str, Any],
    layout: dict[str, Any],
    scene: dict[str, Any],
    ledgers: dict[str, dict[str, Any]],
    *,
    source_digest: str,
) -> dict[str, Any]:
    """Compile all 26 segments into presenter-controlled course states."""
    if len(course.get("acts") or []) != EXPECTED_ACTS:
        raise CourseRuntimeError(
            f"expected {EXPECTED_ACTS} course acts, found {len(course.get('acts') or [])}"
        )

    planned_registry = shots.compile_registry(
        course,
        cameras,
        master,
        layout,
        scene,
        source_digest=source_digest,
    )
    planned_by_segment = {
        shot["segment_id"]: shot for shot in planned_registry["shots"]
    }
    camera_map = {camera["id"]: camera for camera in cameras["cameras"]}
    node_labels = {node["id"]: node["label"] for node in master["nodes"]}
    edge_labels = {
        edge["id"]: f"{node_labels[edge['from']]} → {node_labels[edge['to']]}"
        for edge in master["edges"]
    }

    compiled: list[dict[str, Any]] = []
    for act_sequence, act in enumerate(course["acts"], start=1):
        for segment in act["segments"]:
            request = segment["camera"]
            anchor = camera_map[request["anchor"]]
            if request["status"] == "planned":
                shot = planned_by_segment[segment["id"]]
                frame = shot["frame"]
                render_mode = shot["render_mode"]
            else:
                frame = _frame_for_segment(segment, cameras, master, layout, scene)
                render_mode = "3d" if anchor["mode"] == "3d" else "2d"

            compiled.append(
                {
                    "sequence": len(compiled) + 1,
                    "act_sequence": act_sequence,
                    "act_id": act["id"],
                    "act_title": act["title"],
                    "act_objective": act["learning_objective"],
                    "id": request["shot"],
                    "segment_id": segment["id"],
                    "title": segment["title"],
                    "opening_question": segment["opening_question"],
                    "learning_objective": segment["learning_objective"],
                    "status": (
                        "derived" if request["status"] == "planned" else "existing"
                    ),
                    "mode": request["mode"],
                    "render_mode": render_mode,
                    "camera_anchor": request["anchor"],
                    "evidence_readiness": segment["evidence"]["readiness"],
                    "focus_nodes": list(segment["node_ids"]),
                    "focus_node_labels": [
                        node_labels[node_id] for node_id in segment["node_ids"]
                    ],
                    "focus_edges": list(segment["edge_ids"]),
                    "focus_edge_labels": [
                        edge_labels[edge_id] for edge_id in segment["edge_ids"]
                    ],
                    "reveal_ids": list(request["reveal_ids"]),
                    "reveal_copy_ids": list(request["reveal_copy_ids"]),
                    "frame": frame,
                    "claims": [
                        _claim_card(claim, ledgers)
                        for claim in segment["evidence"]["claims"]
                    ],
                    "promotion_guards": list(segment["evidence"]["promotion_guards"]),
                    "promotion_guard_warnings": [
                        {
                            "id": guard,
                            "warning": PROMOTION_GUARD_WARNINGS[guard],
                        }
                        for guard in segment["evidence"]["promotion_guards"]
                    ],
                    "blocking_research": list(segment["evidence"]["blocking_research"]),
                    "depends_on": list(segment["depends_on"]),
                    "transition": (
                        dict(segment["transition"])
                        if segment["transition"] is not None
                        else None
                    ),
                }
            )

    if len(compiled) != EXPECTED_SEGMENTS:
        raise CourseRuntimeError(
            f"expected {EXPECTED_SEGMENTS} course segments, found {len(compiled)}"
        )
    readiness = [segment["evidence_readiness"] for segment in compiled]
    registry = {
        "schema_version": SCHEMA_VERSION,
        "source_digest": source_digest,
        "act_count": EXPECTED_ACTS,
        "segment_count": len(compiled),
        "evidence_ready_count": readiness.count("evidence_ready"),
        "research_required_count": readiness.count("research_required"),
        "segments": compiled,
    }
    forbidden = {
        key.casefold()
        for key in _walk_keys(registry)
        if key.casefold() in FORBIDDEN_RUNTIME_KEYS
    }
    if forbidden:
        raise CourseRuntimeError(
            f"course runtime contains timing or scripting fields: {sorted(forbidden)}"
        )
    return registry


def _must_replace(text: str, old: str, new: str) -> str:
    if old not in text:
        raise CourseRuntimeError(f"course player template drift: {old[:80]!r}")
    return text.replace(old, new)


COURSE_CSS = r"""
  :root { --head: 148px; --notes: 430px; }
  #masthead { height: var(--head); min-height: var(--head); overflow: hidden; }
  #opening-question { margin: 5px 0 0; font-size: 11px; font-weight: 700; line-height: 1.25; }
  #objective { margin: 4px 0 0; color: var(--muted); font-size: 9px; line-height: 1.25; }
  #scope-summary { color: var(--muted); }
  #transport { grid-template-columns: auto minmax(0, 1fr) auto auto auto; }
  #evidence-toggle {
    min-width: 128px;
    height: 38px;
    padding: 0 12px;
    border: var(--rule) solid var(--ink);
    background: transparent;
    cursor: pointer;
    font-size: 9px;
    font-weight: 700;
    text-transform: uppercase;
  }
  #notes-panel {
    position: absolute;
    z-index: 24;
    top: var(--head);
    right: 0;
    bottom: var(--transport);
    width: min(var(--notes), calc(100vw - var(--rail)));
    padding: 19px 20px 28px;
    overflow-y: auto;
    background: color-mix(in srgb, var(--paper) 98%, transparent);
    border-left: var(--rule) solid var(--ink);
    transform: translateX(100%);
    transition: transform 160ms ease-out;
  }
  #notes-panel[data-open="true"] { transform: translateX(0); }
  #notes-close {
    float: right;
    width: 34px;
    height: 30px;
    border: 1px solid var(--ink);
    background: transparent;
    cursor: pointer;
  }
  #notes-kicker { margin: 0; color: var(--muted); font-size: 9px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
  #notes-title { margin: 6px 44px 15px 0; font-size: 18px; line-height: 1.15; }
  .notes-section { margin-top: 18px; padding-top: 13px; border-top: 1px solid var(--faint); }
  .notes-section h3 { margin: 0 0 8px; font-size: 10px; letter-spacing: .06em; text-transform: uppercase; }
  .notes-section p, .notes-section li { font-size: 10px; line-height: 1.45; }
  .notes-section ul { margin: 0; padding-left: 18px; }
  .notes-section li + li { margin-top: 8px; }
  .guard-list strong { display: block; margin-bottom: 2px; font-size: 9px; text-transform: uppercase; }
  .claim-card { margin-top: 11px; padding: 11px; border: 1px solid var(--faint); }
  .claim-card h4 { margin: 0 0 7px; font-size: 10px; }
  .claim-card p { margin: 5px 0 0; }
  .fact-value { font-weight: 700; }
  .source-list { margin-top: 6px !important; color: var(--muted); }
  .source-list a { color: inherit; }
  .ready { border-left: 5px solid #2f6f4e !important; }
  .gated { border-left: 5px solid #9c5f20 !important; }
  @media (max-width: 1100px) and (min-width: 821px) {
    :root { --head: 166px; }
    #objective { display: none; }
  }
  @media (max-width: 820px) {
    :root { --head: 156px; }
    #objective { display: none; }
    #evidence-toggle { min-width: 92px; }
    #notes-panel { width: calc(100vw - var(--rail)); }
  }
"""


NOTES_HTML = r"""
<aside id="notes-panel" data-open="false" aria-label="Instructor evidence packet" aria-hidden="true" inert>
  <button id="notes-close" type="button" aria-label="Close instructor evidence">×</button>
  <p id="notes-kicker"></p>
  <h2 id="notes-title"></h2>
  <div id="notes-body"></div>
</aside>
"""


NOTES_JS = r"""
function notesSection(title) {
  const section = document.createElement("section");
  section.className = "notes-section";
  const heading = document.createElement("h3");
  heading.textContent = title;
  section.appendChild(heading);
  return section;
}

function paragraph(text, className = "") {
  const value = document.createElement("p");
  value.textContent = text;
  if (className) value.className = className;
  return value;
}

function renderNotes(shot) {
  const restorePanelFocus = notesOpen && $("notes-panel").contains(document.activeElement);
  $("notes-panel").scrollTop = 0;
  $("notes-kicker").textContent = `Act ${shot.act_sequence} · ${shot.act_title}`;
  $("notes-title").textContent = shot.title;
  const body = $("notes-body");
  body.replaceChildren();

  const territory = notesSection("Teaching territory");
  territory.append(
    paragraph(`Question: ${shot.opening_question}`),
    paragraph(`Objective: ${shot.learning_objective}`),
    paragraph(`Available transformations: focused ${shot.render_mode.toUpperCase()} frame, reusable context, and this evidence view. Advance only when useful.`)
  );
  body.appendChild(territory);

  const guards = notesSection("Red-line warnings");
  guards.classList.add("gated", "guard-list");
  const guardList = document.createElement("ul");
  for (const guard of shot.promotion_guard_warnings) {
    const item = document.createElement("li");
    const label = document.createElement("strong");
    label.textContent = guard.id.replaceAll("_", " ");
    item.append(label, document.createTextNode(guard.warning));
    guardList.appendChild(item);
  }
  guards.appendChild(guardList);
  body.appendChild(guards);

  const evidence = notesSection("Validated claims");
  evidence.classList.add(shot.evidence_readiness === "evidence_ready" ? "ready" : "gated");
  evidence.appendChild(paragraph(shot.evidence_readiness.replaceAll("_", " ").toUpperCase()));
  for (const claim of shot.claims) {
    const card = document.createElement("article");
    card.className = "claim-card";
    const heading = document.createElement("h4");
    heading.textContent = `${claim.id.replaceAll("_", " ")} · ${claim.assertion.replaceAll("_", " ")}`;
    card.appendChild(heading);
    for (const fact of claim.facts) {
      card.append(
        paragraph(fact.value, "fact-value"),
        paragraph(`Scope: ${fact.scope}`),
        paragraph(`Boundary: ${fact.posture.replaceAll("_", " ")} · ${fact.lifecycle.replaceAll("_", " ")} · as of ${fact.as_of}`)
      );
      const sources = document.createElement("p");
      sources.className = "source-list";
      sources.append("Source: ");
      fact.sources.forEach((source, index) => {
        if (index) sources.append(" · ");
        const link = document.createElement("a");
        link.href = source.url;
        link.target = "_blank";
        link.rel = "noreferrer";
        link.textContent = `${source.publisher} — ${source.title}`;
        sources.appendChild(link);
      });
      card.appendChild(sources);
    }
    evidence.appendChild(card);
  }
  body.appendChild(evidence);

  if (shot.blocking_research.length) {
    const blockers = notesSection("Explicit evidence boundary");
    blockers.classList.add("gated");
    const list = document.createElement("ul");
    for (const blocker of shot.blocking_research) {
      const item = document.createElement("li");
      item.textContent = blocker;
      list.appendChild(item);
    }
    blockers.appendChild(list);
    body.appendChild(blockers);
  }

  const handoff = notesSection(shot.transition ? "Handoff" : "Close");
  handoff.appendChild(paragraph(
    shot.transition
      ? shot.transition.cue
      : "Return to the opening question and state which conversions are evidenced, assumed, or still unknown."
  ));
  body.appendChild(handoff);
  if (restorePanelFocus) $("notes-close").focus();
}

function setNotesOpen(open) {
  const panel = $("notes-panel");
  const toggle = $("evidence-toggle");
  notesOpen = open;
  panel.inert = !open;
  panel.dataset.open = String(open);
  panel.setAttribute("aria-hidden", String(!open));
  toggle.setAttribute("aria-expanded", String(open));
  toggle.textContent = open ? "Hide evidence" : "Show evidence";
  if (open) {
    $("notes-close").focus();
  } else if (panel.contains(document.activeElement)) {
    toggle.focus();
  }
}
"""


def _player_template() -> str:
    html = shots.REVIEW_HTML
    replacements = (
        ("GIGAWATT — planned shot review", "GIGAWATT — complete course"),
        ("Planned shot registry", "Complete course sequence"),
        ("<p>Course production</p>", "<p>Untimed course runtime</p>"),
        ("<h1>21 planned shots</h1>", "<h1>26 course segments</h1>"),
        ('aria-label="Planned shots"', 'aria-label="Course segments"'),
        (
            'aria-label="Manual planned-shot review surface"',
            'aria-label="Presenter-controlled course surface"',
        ),
        ('aria-label="Previous planned shot"', 'aria-label="Previous course segment"'),
        ('aria-label="Next planned shot"', 'aria-label="Next course segment"'),
        (
            "Manual review · select every change",
            "Untimed · presenter advances every transformation",
        ),
        ("Loading the planned-shot registry…", "Loading the complete course…"),
        ("const shots = data.registry.shots;", "const shots = data.registry.segments;"),
        ("Show anchor", "Show context"),
        ("Show shot", "Show focus"),
    )
    for old, new in replacements:
        html = _must_replace(html, old, new)
    html = _must_replace(
        html,
        "</style>",
        f"{COURSE_CSS}\n</style>",
    )
    html = _must_replace(
        html,
        '<p id="scope-summary"></p>\n    <p id="scope-ids"></p>',
        '<p id="opening-question"></p>\n    <p id="objective"></p>\n    <p id="scope-summary"></p>\n    <p id="scope-ids"></p>',
    )
    html = _must_replace(
        html,
        '<button id="context-toggle" type="button">Show context</button>',
        '<button id="evidence-toggle" type="button" aria-controls="notes-panel" aria-expanded="false">Show evidence</button>\n  <button id="context-toggle" type="button">Show context</button>',
    )
    html = _must_replace(
        html,
        '<div id="loading">Loading the complete course…</div>',
        f'{NOTES_HTML}\n<div id="loading">Loading the complete course…</div>',
    )
    html = _must_replace(
        html,
        "let current = 0;\nlet showingAnchor = false;",
        f"{NOTES_JS}\n\nlet current = 0;\nlet showingAnchor = false;\nlet notesOpen = false;",
    )
    old_header = r"""  $("eyebrow").textContent = `${String(shot.sequence).padStart(2, "0")} / ${shots.length} · ${shot.segment_id}`;
  $("title").textContent = shot.title;
  $("scope-summary").textContent = `${shot.focus_nodes.length} nodes · ${shot.focus_edges.length} edges · ${shot.evidence_readiness.replaceAll("_", " ")}`;
  const readableNodes = shot.focus_nodes.map(id => nodeLabels.get(id) || id);
  $("scope-ids").textContent = readableNodes.join(" · ");
  $("scope-ids").title = shot.focus_nodes.join(", ");
  $("shot-id").textContent = shot.id;
  $("mode").textContent = `${shot.mode} · ${shot.render_mode} context · ${shot.camera_anchor}`;
  const revealCount = shot.reveal_ids.length + shot.reveal_copy_ids.length;
  $("reveal-summary").textContent = revealCount
    ? `${shot.reveal_ids.length} hidden geometry + ${shot.reveal_copy_ids.length} hidden copy revealed`
    : "No hidden reveal";
  $("context-toggle").textContent = "Show context";"""
    new_header = r"""  $("eyebrow").textContent = `Act ${shot.act_sequence} · ${shot.act_title} · ${String(shot.sequence).padStart(2, "0")} / ${shots.length}`;
  $("title").textContent = shot.title;
  $("opening-question").textContent = shot.opening_question;
  $("objective").textContent = shot.learning_objective;
  $("scope-summary").textContent = `${shot.focus_nodes.length} nodes · ${shot.focus_edges.length} edges · ${shot.evidence_readiness.replaceAll("_", " ")}`;
  $("scope-ids").textContent = shot.focus_node_labels.join(" · ");
  $("scope-ids").title = shot.focus_nodes.join(", ");
  $("shot-id").textContent = shot.segment_id;
  $("mode").textContent = `${shot.mode} · ${shot.render_mode} · ${shot.camera_anchor}`;
  const revealCount = shot.reveal_ids.length + shot.reveal_copy_ids.length;
  $("reveal-summary").textContent = revealCount
    ? `${revealCount} explicit hidden reveals · ${shot.status}`
    : `${shot.status} view · no hidden reveal`;
  $("posture").classList.toggle("ready", shot.evidence_readiness === "evidence_ready");
  $("posture").classList.toggle("gated", shot.evidence_readiness !== "evidence_ready");
  $("context-toggle").textContent = "Show context";
  renderNotes(shot);"""
    html = _must_replace(html, old_header, new_header)
    old_rail = r"""  name.className = "shot-name";
  name.textContent = shot.id;
  const segment = document.createElement("span");
  segment.className = "segment-name";
  segment.textContent = shot.segment_id;"""
    new_rail = r"""  name.className = "shot-name";
  name.textContent = shot.title;
  const segment = document.createElement("span");
  segment.className = "segment-name";
  segment.textContent = `Act ${shot.act_sequence} · ${shot.segment_id}`;"""
    html = _must_replace(html, old_rail, new_rail)
    html = _must_replace(
        html,
        '$("context-toggle").addEventListener("click", () => {',
        '$("evidence-toggle").addEventListener("click", () => setNotesOpen(!notesOpen));\n$("notes-close").addEventListener("click", () => setNotesOpen(false));\n$("context-toggle").addEventListener("click", () => {',
    )
    html = _must_replace(
        html,
        '  if (event.key === "ArrowRight") activate(current + 1);\n});',
        '  if (event.key === "ArrowRight") activate(current + 1);\n  if (event.key.toLowerCase() === "e") setNotesOpen(!notesOpen);\n  if (event.key === "Escape") setNotesOpen(false);\n});',
    )
    return html


def _markdown_escape(value: str) -> str:
    return value.replace("|", "\\|")


def build_instructor_packet(registry: dict[str, Any]) -> str:
    lines = [
        "# GIGAWATT instructor packet",
        "",
        "This packet is teaching territory, not a spoken script. It assigns no",
        "durations, cadence, or automatic visual changes. The presenter decides how",
        "long to remain in each segment and may switch among focus, context, and",
        "evidence views only when the explanation benefits.",
        "",
        "## Run and test",
        "",
        "```sh",
        "python3 -m http.server --directory diagram 8000",
        "```",
        "",
        "Open `http://localhost:8000/course.html`. Use the segment rail or left/right",
        "arrow keys to move through the course. `Show context` widens to the reusable",
        "camera, while `Show evidence` (or the E key) opens the claim boundary and",
        "primary-source links. No state advances on its own.",
        "",
        "For a first editorial pass, check whether each opening question naturally",
        "invites the explanation, whether focus/context is enough visual movement,",
        "whether the evidence boundary is sayable in your own words, and whether the",
        "handoff makes the next segment feel inevitable. Record notes by segment ID.",
        "",
    ]
    current_act: str | None = None
    for segment in registry["segments"]:
        if segment["act_id"] != current_act:
            current_act = segment["act_id"]
            lines.extend(
                [
                    f"## Act {segment['act_sequence']}: {segment['act_title']}",
                    "",
                    segment["act_objective"],
                    "",
                ]
            )
        readiness = segment["evidence_readiness"].replace("_", " ")
        lines.extend(
            [
                f"### {segment['sequence']:02d}. {segment['title']} `{segment['segment_id']}`",
                "",
                f"- Opening question: {segment['opening_question']}",
                f"- Teaching objective: {segment['learning_objective']}",
                f"- Visual focus: {', '.join(segment['focus_node_labels'])}",
                f"- Available transformation: focused {segment['render_mode'].upper()} view ↔ `{segment['camera_anchor']}` context; evidence panel on demand.",
                f"- Evidence posture: **{readiness}**",
                "",
                "Validated claim territory:",
                "",
            ]
        )
        for claim in segment["claims"]:
            assertion = claim["assertion"].replace("_", " ")
            lines.append(f"- **{claim['id'].replace('_', ' ')} — {assertion}.**")
            for fact in claim["facts"]:
                sources = ", ".join(
                    f"[{source['publisher']} — {_markdown_escape(source['title'])}]({source['url']})"
                    for source in fact["sources"]
                )
                lines.extend(
                    [
                        f"  - {_markdown_escape(fact['value'])}",
                        f"  - Scope: {_markdown_escape(fact['scope'])}",
                        f"  - Boundary: `{fact['posture']}` / `{fact['lifecycle']}` / as of {fact['as_of']}",
                        f"  - Sources: {sources}",
                    ]
                )
        lines.extend(["", "Red-line warnings:", ""])
        for guard in segment["promotion_guard_warnings"]:
            lines.append(
                f"- **{guard['id'].replace('_', ' ')}.** {_markdown_escape(guard['warning'])}"
            )
        if segment["blocking_research"]:
            lines.extend(["", "Explicit evidence boundary:", ""])
            lines.extend(f"- {item}" for item in segment["blocking_research"])
        if segment["transition"]:
            lines.extend(["", f"Handoff: {segment['transition']['cue']}", ""])
        else:
            lines.extend(
                [
                    "",
                    "Close: Return to the opening question and state which conversions are evidenced, assumed, or still unknown.",
                    "",
                ]
            )
    return "\n".join(lines).rstrip() + "\n"


def build_artifacts() -> tuple[str, str, str, str]:
    course, cameras, master, layout, scene, ledgers = load_inputs()
    digest = _source_digest(course)
    registry = compile_registry(
        course,
        cameras,
        master,
        layout,
        scene,
        ledgers,
        source_digest=digest,
    )
    registry_json = scene_pipeline.canonical_payload(registry) + "\n"

    master_evidence = ledgers[course["meta"]["master_evidence_ledger"]]
    _, map_scene = layout_pipeline.compose(master, layout, master_evidence)
    shared = scene_pipeline.build_payload(master, scene, cameras)
    player_payload = {
        "registry": registry,
        "scene": {
            "palette": shared["palette"],
            "stroke": shared["stroke"],
            "world": shared["world"],
            "structures": shared["structures"],
            "nodes": shared["nodes"],
            "edges": shared["edges"],
        },
        "hidden": {
            "nodes": sorted(
                node["id"]
                for node in master["nodes"]
                if node.get("base_visible", True) is False
            ),
            "edges": sorted(
                edge["id"]
                for edge in master["edges"]
                if edge.get("base_visible", True) is False
            ),
            "copy": sorted(
                copy_id
                for copy_id, record in master["copy"].items()
                if record.get("base_visible", True) is False
            ),
        },
    }
    player = (
        _player_template()
        .replace("__DATA__", _script_safe_payload(player_payload))
        .replace("__MAP_SCENE__", map_scene)
        .replace("__DIGEST__", digest)
        .replace("__PAPER__", tokens.PAPER)
        .replace("__INK__", tokens.INK)
        .replace("__FAINT__", tokens.FAINT)
        .replace("__MUTED__", tokens.MUTED_TEXT)
        .replace("__FONT__", tokens.FONT)
    )
    packet = build_instructor_packet(registry)
    return registry_json, player, packet, digest


def main() -> None:
    registry, player, packet, digest = build_artifacts()
    REGISTRY_PATH.write_text(registry)
    PLAYER_PATH.write_text(player)
    PACKET_PATH.write_text(packet)
    print(
        f"built {REGISTRY_PATH.relative_to(ROOT)}, {PLAYER_PATH.relative_to(ROOT)}, "
        f"and {PACKET_PATH.relative_to(ROOT)} · {EXPECTED_SEGMENTS} manual segments "
        f"· digest {digest}"
    )


if __name__ == "__main__":
    main()
