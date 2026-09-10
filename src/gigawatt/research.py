"""Discover sources, build research notes, and maintain a local article archive."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import tempfile
import time
import xml.etree.ElementTree as ET
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[2]
START = "<!-- gigawatt-research:managed:start -->"
END = "<!-- gigawatt-research:managed:end -->"
DEFAULT_URL = "https://newsletter.semianalysis.com/sitemap.xml"
TRIAGE = {"unreviewed", "include", "exclude", "defer"}
REVIEW = {"candidate_not_reviewed", "public_excerpt_reviewed", "page_reviewed"}
SA_HOSTS = {"semianalysis.com", "www.semianalysis.com", "newsletter.semianalysis.com"}
KEYWORDS = {
    "D01": r"\b(power|energy|megawatt|gigawatt|pue)\b",
    "D02": r"\b(workload|training|inference|latency|tokens|batch)\b",
    "D03": r"\b(grid|utility|utilities|nuclear|gas|generation|interconnection|behind.the.meter|btm)\b",
    "D04": r"\b(electrical|substation|transformer|switchgear|distribution)\b",
    "D05": r"\b(ups|battery|batteries|generator|redundancy|backup|protection|bbu)\b",
    "D06": r"\b(800\s*v(?:dc)?|800vdc|54v|48v|busbar|rack power)\b",
    "D07": r"\b(gpu|accelerator|memory|hbm|ddr|blackwell|rubin|nvl|gb200|server|tpu)\b",
    "D08": r"\b(network|networking|interconnect|ethernet|infiniband|optics|photonic|nvlink)\b",
    "D09": r"\b(storage|checkpoint|checkpointing|orchestration|slurm)\b",
    "D10": r"\b(cooling|liquid|coldplate|cold plate|cdu)\b",
    "D11": r"\b(cooling|chiller|water|heat|weather)\b",
    "D12": r"\b(construction|campus|building|fire|site)\b",
    "D13": r"\b(construction|commissioning|supply chain|procurement|buildout|anatomy)\b",
    "D14": r"\b(reliability|outage|downtime|monitoring|control|failure|maintenance)\b",
    "D15": r"\b(cost|economics|capacity|utilization|efficiency|tco)\b",
}
BODY = """
## Claim-level notes

No claim-level notes have been recorded here. Catalog review status above describes
only its stated scope; it is not validation of every proposed teaching use.

## Questions and claims to verify

Record the claim, exact supporting location, what was actually read, the check
date, and any missing inputs or contradictory evidence.

## Teaching use

Connect verified claims to an objective, mechanism, worked example, tradeoff,
failure or limiting case, or transfer question. Topic presence is not mastery.
"""


class ResearchError(ValueError):
    """Invalid input or unsafe replacement of human research material."""


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ResearchError(f"Cannot read {path}: {exc}") from exc


def canonical_url(value: str) -> str:
    """Normalize explicit same-path publisher aliases, not guessed slug migrations."""
    if not isinstance(value, str):
        raise ResearchError("A URL must be a string")
    parts = urlsplit(value.strip())
    if (
        parts.scheme not in {"http", "https"}
        or not parts.hostname
        or parts.username
        or parts.password
        or any(c.isspace() for c in value)
    ):
        raise ResearchError(f"Invalid public HTTP(S) URL: {value!r}")
    try:
        port = parts.port
    except ValueError as exc:
        raise ResearchError(f"Invalid URL port: {value!r}") from exc
    host = parts.hostname.lower()
    path = parts.path or "/"
    scheme = parts.scheme
    if host in SA_HOSTS:
        # /p/ is the newsletter route; dated historical routes remain on the main host.
        if path.startswith("/p/"):
            host = "newsletter.semianalysis.com"
        elif host == "www.semianalysis.com":
            host = "semianalysis.com"
        scheme = "https"
        path = path.rstrip("/") or "/"
    if ":" in host:
        host = f"[{host}]"
    netloc = host
    if port and (scheme, port) not in {("https", 443), ("http", 80)}:
        netloc += f":{port}"
    query = urlencode(
        sorted(
            (key, val)
            for key, val in parse_qsl(parts.query, keep_blank_values=True)
            if not key.lower().startswith("utm_")
            and key.lower() not in {"fbclid", "gclid"}
            and not (
                parts.hostname.lower() in SA_HOSTS
                and key.lower()
                in {
                    "s",
                    "r",
                    "triedredirect",
                    "publication_id",
                    "post_id",
                    "isfreemail",
                }
            )
        )
    )
    return urlunsplit((scheme, netloc, path, query, ""))


def domain_ids(domain_map: dict) -> set[str]:
    if not isinstance(domain_map, dict) or not isinstance(
        domain_map.get("domains"), list
    ):
        raise ResearchError("Domain map must contain a domains list")
    result = set()
    for domain in domain_map["domains"]:
        identifier = domain.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(r"D\d{2,}", identifier):
            raise ResearchError(f"Invalid domain ID: {identifier!r}")
        if identifier in result:
            raise ResearchError(f"Duplicate domain ID: {identifier}")
        result.add(identifier)
    return result


def validate_domains(values, known: set[str], label: str) -> list[str]:
    if not isinstance(values, list) or any(not isinstance(v, str) for v in values):
        raise ResearchError(f"{label}: domains must be a list of IDs")
    if len(values) != len(set(values)) or not set(values) <= known:
        raise ResearchError(f"{label}: duplicate or unknown domain IDs: {values}")
    return values


def validate_catalog(catalog: dict, domain_map: dict) -> list[dict]:
    known = domain_ids(domain_map)
    if not isinstance(catalog, dict) or not isinstance(catalog.get("sources"), list):
        raise ResearchError("Catalog must contain a sources list")
    sources, ids, urls = [], set(), set()
    for original in catalog["sources"]:
        source = dict(original)
        identifier = source.get("id")
        if not isinstance(identifier, str) or not re.fullmatch(
            r"[A-Za-z][A-Za-z0-9_-]*", identifier
        ):
            raise ResearchError(f"Invalid source ID: {identifier!r}")
        if identifier in ids:
            raise ResearchError(f"Duplicate source ID: {identifier}")
        for key in ("title", "publisher", "kind", "review_status", "use", "caution"):
            if not isinstance(source.get(key), str) or not source[key].strip():
                raise ResearchError(f"{identifier}: missing {key}")
        if source["review_status"] not in REVIEW:
            raise ResearchError(f"{identifier}: unknown review status")
        if source["review_status"] != "candidate_not_reviewed" and not source.get(
            "reviewed_on"
        ):
            raise ResearchError(f"{identifier}: reviewed content needs reviewed_on")
        source["url"] = canonical_url(source.get("url"))
        if source["url"] in urls:
            raise ResearchError(
                f"Duplicate source URL after alias normalization: {source['url']}"
            )
        validate_domains(source.get("domains"), known, identifier)
        ids.add(identifier)
        urls.add(source["url"])
        sources.append(source)
    for domain in domain_map["domains"]:
        for identifier in domain.get("source_ids", []):
            if identifier not in ids:
                raise ResearchError(
                    f"{domain['id']}: unknown mapped source {identifier}"
                )
    return sources


def candidate_id(url: str) -> str:
    return "DISC_" + hashlib.sha256(url.encode()).hexdigest()[:16]


def validate_inventory(inventory: dict, known: set[str]) -> None:
    if not isinstance(inventory, dict) or not isinstance(inventory.get("items"), list):
        raise ResearchError("Discovery inventory must contain an items list")
    seen = set()
    for item in inventory["items"]:
        url = canonical_url(item.get("url"))
        if item["url"] != url:
            raise ResearchError(f"Discovery URL is not canonical: {item['url']}")
        if url in seen:
            raise ResearchError(f"Duplicate discovery URL: {url}")
        seen.add(url)
        if item.get("triage") not in TRIAGE:
            raise ResearchError(f"{url}: invalid triage state")
        validate_domains(item.get("suggested_domains", []), known, url)
        validate_domains(item.get("domains", []), known, url)
        if not isinstance(item.get("title"), str) or not item["title"].strip():
            raise ResearchError(f"{url}: missing title")


def candidate_sources(
    inventory: dict, known: set[str], curated_urls: set[str]
) -> list[dict]:
    validate_inventory(inventory, known)
    result = []
    for item in inventory["items"]:
        domains = item.get("domains", [])
        if not domains and item["triage"] == "unreviewed":
            domains = item.get("suggested_domains", [])
        if item["url"] in curated_urls or item["triage"] == "exclude" or not domains:
            continue
        result.append(
            {
                "id": candidate_id(item["url"]),
                "title": item["title"],
                "url": item["url"],
                "publisher": item.get("publisher") or urlsplit(item["url"]).hostname,
                "kind": "discovery_candidate",
                "review_status": "candidate_not_reviewed",
                "published_on": item.get("published_on"),
                "domains": domains,
                "triage": item["triage"],
                "use": "Candidate for research; domain suggestions are keyword triage only.",
                "caution": (
                    "Metadata only. No article links were followed and no article content was reviewed. "
                    "A URL-derived title and sitemap last-modified date are not verified "
                    "article title and publication date."
                ),
                "title_origin": item.get("title_origin", "unknown"),
                "discovered_via": item.get("discovered_via", []),
                "first_seen": item.get("first_seen"),
                "last_seen": item.get("last_seen"),
            }
        )
    return result


def md(value) -> str:
    return (
        str(value)
        .replace("\n", " ")
        .replace("|", "\\|")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def source_metadata(source: dict) -> str:
    lines = [f"# {md(source['id'])} — {md(source['title'])}", ""]
    for key in (
        "url",
        "publisher",
        "kind",
        "review_status",
        "reviewed_on",
        "published_on",
        "updated_on",
        "domains",
        "use",
        "caution",
        "triage",
        "title_origin",
        "discovered_via",
        "first_seen",
        "last_seen",
    ):
        value = source.get(key)
        if value is not None:
            if key == "domains":
                value = ", ".join(
                    f"[{d}](../../course/DOMAIN_MAP.md#{d.lower()})" for d in value
                )
            elif key == "url":
                value = f"[Original source]({value})"
            elif isinstance(value, list):
                value = ", ".join(value)
            lines.append(f"- **{key.replace('_', ' ').capitalize()}:** {md(value)}")
    fingerprint = hashlib.sha256(
        json.dumps(source, ensure_ascii=False, sort_keys=True).encode()
    ).hexdigest()
    lines.extend(["", f"Catalog metadata fingerprint: {fingerprint}"])
    return "\n".join(lines)


def managed_text(path: Path, metadata: str, initial_body: str = BODY) -> str:
    prefix = f"{START}\n{metadata}\n{END}"
    if not path.exists():
        return prefix + "\n" + initial_body
    text = path.read_text(encoding="utf-8")
    if (
        not text.startswith(START + "\n")
        or text.count(START) != 1
        or text.count(END) != 1
    ):
        raise ResearchError(f"Refusing to replace unmanaged or malformed note: {path}")
    return prefix + text.split(END, 1)[1]


def atomic_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        mode="w", encoding="utf-8", dir=path.parent, delete=False
    ) as f:
        temporary = Path(f.name)
        f.write(text)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def build_notes(
    root: Path, include_candidates: bool = False, check: bool = False
) -> list[Path]:
    domain_map = read_json(root / "course/domain-map.json")
    catalog = read_json(root / "course/research-sources.json")
    sources = validate_catalog(catalog, domain_map)
    inventory_path = root / "research/discovery.json"
    if inventory_path.exists():
        inventory = read_json(inventory_path)
        validate_inventory(inventory, domain_ids(domain_map))
    else:
        inventory = {"items": []}
    if include_candidates:
        sources += candidate_sources(
            inventory, domain_ids(domain_map), {s["url"] for s in sources}
        )
    ids = [s["id"] for s in sources]
    if len(ids) != len(set(ids)):
        raise ResearchError("Candidate ID conflicts with a curated source ID")
    sources.sort(key=lambda s: s["id"])
    outputs = {}
    for source in sources:
        path = root / "research/sources" / f"{source['id']}.md"
        outputs[path] = managed_text(path, source_metadata(source))
    index = [
        "# Research source index",
        "",
        "Generated from the curated catalog"
        + (" and eligible discovery candidates." if include_candidates else "."),
        f"Candidate notes included: {'yes' if include_candidates else 'no'}.",
        "",
        "Review labels retain their catalog scope. Metadata discovery does not read articles.",
        "Keyword domain suggestions are triage, not a completeness or authority claim.",
        "",
        "| Source | Publisher | Domains | Content review |",
        "| --- | --- | --- | --- |",
    ]
    for source in sources:
        index.append(
            f"| [{md(source['id'])} — {md(source['title'])}](sources/{source['id']}.md)"
            f" | {md(source['publisher'])} | {', '.join(source['domains'])}"
            f" | {source['review_status']} |"
        )
    index_path = root / "research/INDEX.md"
    outputs[index_path] = managed_text(
        index_path, "\n".join(index), "\n## Research notes\n"
    )
    stale = [
        path
        for path, text in outputs.items()
        if not path.exists() or path.read_text(encoding="utf-8") != text
    ]
    if check and stale:
        raise ResearchError(
            "Missing or stale generated metadata: " + ", ".join(str(p) for p in stale)
        )
    if not check:
        for path in stale:
            atomic_write(path, outputs[path])
    return stale


def suggest_domains(title: str, known: set[str]) -> list[str]:
    text = re.sub(r"[-_/]", " ", title.lower())
    return sorted(
        d for d, pattern in KEYWORDS.items() if d in known and re.search(pattern, text)
    )


def slug_title(url: str) -> str:
    slug = urlsplit(url).path.rstrip("/").split("/")[-1]
    return slug.replace("-", " ").replace("_", " ") or urlsplit(url).hostname


def tag(element: ET.Element) -> str:
    return element.tag.rsplit("}", 1)[-1]


def child_text(element: ET.Element, name: str) -> str | None:
    for child in element:
        if tag(child) == name:
            return "".join(child.itertext()).strip() or None
    return None


def parse_metadata(data: bytes, origin: str) -> tuple[list[dict], list[str]]:
    """Read XML metadata fields only; ignore descriptions and encoded article content."""
    if b"<!DOCTYPE" in data.upper() or b"<!ENTITY" in data.upper():
        raise ResearchError("XML document types and entities are not accepted")
    try:
        document = ET.fromstring(data)
    except ET.ParseError as exc:
        raise ResearchError(f"Invalid metadata XML from {origin}: {exc}") from exc
    kind = tag(document)
    records, children = [], []
    if kind == "sitemapindex":
        for node in document:
            url = child_text(node, "loc")
            if url:
                children.append(url)
    elif kind == "urlset":
        for node in document:
            url = child_text(node, "loc")
            if url:
                records.append(
                    {
                        "url": url,
                        "title": slug_title(url),
                        "title_origin": "url_slug",
                        "sitemap_last_modified": child_text(node, "lastmod"),
                    }
                )
    elif kind in {"rss", "feed", "RDF"}:
        for node in document.iter():
            if tag(node) not in {"item", "entry"}:
                continue
            url = child_text(node, "link")
            if not url:
                for link in node:
                    if (
                        tag(link) == "link"
                        and link.get("rel", "alternate") == "alternate"
                    ):
                        url = link.get("href")
                        if url:
                            break
            if not url:
                continue
            title = child_text(node, "title")
            records.append(
                {
                    "url": url,
                    "title": title or slug_title(url),
                    "title_origin": "feed_title" if title else "url_slug",
                    "published_on": child_text(node, "pubDate")
                    or child_text(node, "published"),
                }
            )
    else:
        raise ResearchError(
            f"Unsupported metadata format {kind!r}; use sitemap, RSS, Atom or JSON import"
        )
    return records, children


def fetch_metadata(url: str, timeout: float, max_bytes: int = 4_000_000) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": "GIGAWATT-course-research/0.1 (public metadata; no article-body crawler)",
            "Accept": "application/xml, text/xml, application/rss+xml, application/atom+xml",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        data = response.read(max_bytes + 1)
    if len(data) > max_bytes:
        raise ResearchError(f"Metadata document exceeds {max_bytes} bytes: {url}")
    return data


def load_import(path: Path, known: set[str]) -> list[dict]:
    data = read_json(path)
    records = data.get("items", data.get("sources")) if isinstance(data, dict) else data
    if not isinstance(records, list):
        raise ResearchError("Metadata import must be a list or contain items/sources")
    result = []
    for record in records:
        if not isinstance(record, dict):
            raise ResearchError("Every imported metadata record must be an object")
        record = dict(record)
        record["url"] = canonical_url(record.get("url"))
        if not isinstance(record.get("title"), str) or not record["title"].strip():
            raise ResearchError(f"{record['url']}: imported metadata needs a title")
        validate_domains(record.get("domains", []), known, record["url"])
        if record.get("triage", "unreviewed") not in TRIAGE:
            raise ResearchError(f"{record['url']}: invalid imported triage state")
        record["title_origin"] = "manual_metadata"
        # Keep only metadata and decisions; never copy arbitrary full-text fields.
        allowed = {
            "url",
            "title",
            "title_origin",
            "publisher",
            "published_on",
            "domains",
            "triage",
            "notes",
        }
        result.append({key: value for key, value in record.items() if key in allowed})
    return result


def merge_records(
    previous: dict, records: list[dict], known: set[str], now: str
) -> list[dict]:
    validate_inventory(previous, known)
    merged = {item["url"]: dict(item) for item in previous["items"]}
    for incoming in records:
        url = canonical_url(incoming["url"])
        old = merged.get(url)
        title = incoming.get("title") or slug_title(url)
        origin = incoming.get("title_origin", "url_slug")
        if (
            old
            and old.get("title_origin") in {"feed_title", "manual_metadata"}
            and origin == "url_slug"
        ):
            title, origin = old["title"], old["title_origin"]
        item = dict(old or {})
        item.update(
            {
                "url": url,
                "title": title,
                "title_origin": origin,
                "publisher": incoming.get("publisher")
                or item.get("publisher")
                or (
                    "SemiAnalysis"
                    if urlsplit(url).hostname in SA_HOSTS
                    else urlsplit(url).hostname
                ),
                "suggested_domains": suggest_domains(title, known),
                "first_seen": item.get("first_seen", now),
                "last_seen": now,
            }
        )
        for key in ("published_on", "sitemap_last_modified"):
            if incoming.get(key):
                item[key] = incoming[key]
        vias = set(item.get("discovered_via", []))
        if incoming.get("via"):
            vias.add(incoming["via"])
        item["discovered_via"] = sorted(vias)
        # Existing decisions are authoritative, including explicit empty domain lists.
        for key, default in (("triage", "unreviewed"), ("domains", []), ("notes", "")):
            item[key] = old.get(key, default) if old else incoming.get(key, default)
        merged[url] = item
    result = sorted(merged.values(), key=lambda item: item["url"])
    validate_inventory({"items": result}, known)
    return result


def discover(
    root: Path,
    urls: list[str],
    imports: list[Path],
    max_documents: int = 4,
    timeout: float = 20,
    delay: float = 1,
    fetcher=fetch_metadata,
    now: str | None = None,
) -> dict:
    if max_documents < 1 or max_documents > 50 or timeout <= 0 or delay < 0:
        raise ResearchError(
            "Use 1–50 documents, a positive timeout and a nonnegative delay"
        )
    known = domain_ids(read_json(root / "course/domain-map.json"))
    path = root / "research/discovery.json"
    previous = read_json(path) if path.exists() else {"items": [], "runs": []}
    validate_inventory(previous, known)
    now = now or datetime.now(UTC).isoformat(timespec="seconds")
    records, errors, successes = [], [], []
    for import_path in imports:
        imported = load_import(import_path, known)
        records.extend(
            dict(item, via=f"import:{import_path.name}") for item in imported
        )
        successes.append(f"import:{import_path.name}")
    queue = list(dict.fromkeys(canonical_url(url) for url in urls))
    visited = set()
    while queue and len(visited) < max_documents:
        url = queue.pop(0)
        if url in visited:
            continue
        if visited and delay:
            time.sleep(delay)
        visited.add(url)
        try:
            data = fetcher(url, timeout)
            items, children = parse_metadata(data, url)
            normalized_items = [
                dict(item, url=canonical_url(item["url"]), via=url) for item in items
            ]
            records.extend(normalized_items)
            successes.append(url)
            for child in children:
                normalized = canonical_url(child)
                child_host, origin_host = (
                    urlsplit(normalized).hostname,
                    urlsplit(url).hostname,
                )
                if (
                    child_host != origin_host
                    and not {child_host, origin_host} <= SA_HOSTS
                ):
                    errors.append(
                        {
                            "url": normalized,
                            "error": "Cross-host sitemap child was not fetched",
                        }
                    )
                    continue
                if normalized not in visited and normalized not in queue:
                    queue.append(normalized)
        except (OSError, ValueError) as exc:
            errors.append({"url": url, "error": str(exc)})
    status = "partial" if errors or queue else "completed"
    if not successes:
        status = "failed"
    run = {
        "at": now,
        "status": status,
        "documents_succeeded": successes,
        "documents_failed": errors,
        "unvisited_due_to_bound": queue,
        "metadata_records_observed": len(records),
        "article_links_followed": 0,
        "limits": {
            "max_documents": max_documents,
            "timeout_seconds": timeout,
            "delay_seconds": delay,
        },
        "scope_note": (
            "Completed means requested metadata documents were processed within the bound, "
            "not an exhaustive relevant corpus. Titles/URL keywords only suggest triage. "
            "No source-content review or publication-date verification is implied."
        ),
    }
    result = {
        "schema_version": 1,
        "scope": "Public metadata and manual imports; article links are not followed. Feed body fields are discarded.",
        "runs": previous.get("runs", []) + [run],
        "items": merge_records(previous, records, known, now),
    }
    atomic_write(path, json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    return run


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="Repository root")
    subcommands = parser.add_subparsers(dest="command", required=True)
    for command in ("build", "check"):
        sub = subcommands.add_parser(command)
        sub.add_argument("--include-candidates", action="store_true")
    sub = subcommands.add_parser("discover")
    sub.add_argument(
        "--url",
        action="append",
        default=[],
        help="Public sitemap/RSS/Atom URL; repeatable",
    )
    sub.add_argument("--import", dest="imports", action="append", type=Path, default=[])
    sub.add_argument("--max-documents", type=int, default=4)
    sub.add_argument("--timeout", type=float, default=20)
    sub.add_argument("--delay", type=float, default=1)
    archive = subcommands.add_parser(
        "archive", help="Local permitted article captures and exports"
    )
    actions = archive.add_subparsers(dest="archive_action", required=True)
    sync = actions.add_parser(
        "sync", help="Capture public article bodies; label previews explicitly"
    )
    sync.add_argument("--source", action="append", dest="source_ids")
    sync.add_argument("--include-candidates", action="store_true")
    sync.add_argument("--refresh", action="store_true")
    sync.add_argument("--timeout", type=float, default=20)
    sync.add_argument("--delay", type=float, default=1)
    sync.add_argument(
        "--permission-note",
        help="Publisher permission context; saved locally for later runs",
    )
    imp = actions.add_parser(
        "import", help="Import a provided Markdown, text or HTML article export"
    )
    imp.add_argument("--source", required=True)
    imp.add_argument("--file", type=Path, required=True)
    imp.add_argument(
        "--complete",
        action="store_true",
        help="The supplied export contains the complete article",
    )
    imp.add_argument("--permission-note")
    actions.add_parser(
        "check", help="Verify captured file hashes without network access"
    )
    args = parser.parse_args(argv)
    try:
        if args.command == "archive":
            from gigawatt import article_archive

            if args.archive_action == "check":
                print(
                    f"Verified {article_archive.check(args.root)} local article captures."
                )
                return 0
            if args.archive_action == "import":
                status = article_archive.import_article(
                    args.root,
                    args.source,
                    args.file,
                    complete=args.complete,
                    permission_note=args.permission_note,
                )
                print(f"{args.source}: {status}")
                return 0
            if args.timeout <= 0 or args.delay < 0:
                raise ResearchError("Timeout must be positive and delay nonnegative")
            results = article_archive.sync(
                args.root,
                args.source_ids,
                include_candidates=args.include_candidates,
                refresh=args.refresh,
                timeout=args.timeout,
                delay=args.delay,
                permission_note=args.permission_note,
            )
            counts = {
                status: sum(s == status for _, s in results) for _, status in results
            }
            print(
                f"Archive: {len(results)} selected sources; {json.dumps(counts, sort_keys=True)}"
            )
            return 1 if counts.get("fetch_failed") else 0
        if args.command in {"build", "check"}:
            changed = build_notes(
                args.root, args.include_candidates, args.command == "check"
            )
            print(
                "Research metadata is current."
                if args.command == "check"
                else f"Updated {len(changed)} research notes/index files; human note bodies preserved."
            )
            return 0
        urls = args.url or ([] if args.imports else [DEFAULT_URL])
        run = discover(
            args.root, urls, args.imports, args.max_documents, args.timeout, args.delay
        )
        print(
            f"Discovery {run['status']}: {run['metadata_records_observed']} metadata records observed; "
            "0 article links followed; body fields discarded. Inventory and prior decisions saved."
        )
        for error in run["documents_failed"]:
            print(f"  {error['url']}: {error['error']}", file=sys.stderr)
        if run["unvisited_due_to_bound"]:
            print(
                f"  {len(run['unvisited_due_to_bound'])} metadata documents left by request bound.",
                file=sys.stderr,
            )
        return 0 if run["status"] == "completed" else 1
    except (ValueError, OSError) as exc:
        print(f"Research error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
