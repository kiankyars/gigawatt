"""Capture permitted article text as a local, searchable Markdown library."""

from __future__ import annotations

import hashlib
import json
import re
import time
from datetime import UTC, datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit
from urllib.request import Request, urlopen

from gigawatt.research import (
    SA_HOSTS,
    ResearchError,
    atomic_write,
    candidate_sources,
    canonical_url,
    domain_ids,
    read_json,
    validate_catalog,
)

ARCHIVE = Path("research/articles")
VOID = {
    "area",
    "base",
    "br",
    "col",
    "embed",
    "hr",
    "img",
    "input",
    "link",
    "meta",
    "param",
    "source",
    "track",
    "wbr",
}
SKIP = {"script", "style", "nav", "form", "button", "noscript", "svg"}
FULL = {"public_article", "imported_full_article"}


class Node:
    def __init__(self, tag="", attrs=None):
        self.tag, self.attrs, self.children = tag, dict(attrs or []), []

    def walk(self):
        yield self
        for child in self.children:
            if isinstance(child, Node):
                yield from child.walk()


class Document(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("document")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs)
        self.stack[-1].children.append(node)
        if tag not in VOID:
            self.stack.append(node)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                break

    def handle_data(self, data):
        self.stack[-1].children.append(data)


def plain(node):
    return node if isinstance(node, str) else "".join(plain(c) for c in node.children)


def public_link(value, base):
    resolved = urljoin(base, value)
    return resolved if urlsplit(resolved).scheme in {"https", "http"} else ""


def markdown(node, base, list_depth=0):
    if isinstance(node, str):
        return re.sub(r"\s+", " ", node)
    tag, attrs = node.tag, node.attrs
    classes = set((attrs.get("class") or "").split())
    if classes & {"katex", "katex-display"}:
        tex = next(
            (
                plain(n)
                for n in node.walk()
                if n.tag == "annotation"
                and n.attrs.get("encoding") == "application/x-tex"
            ),
            None,
        )
        if tex:
            return (
                f"\n\n$$\n{tex}\n$$\n\n" if "katex-display" in classes else f"${tex}$"
            )
    if tag == "script" and (attrs.get("type") or "").startswith("math/tex"):
        return "$" + plain(node) + "$"
    if tag in SKIP or classes & {"subscribe-widget", "paywall", "button-wrapper"}:
        return ""
    if tag == "pre":
        content = plain(node).strip("\n")
        fence = "`" * max(
            3, max((len(m[0]) + 1 for m in re.finditer(r"`+", content)), default=3)
        )
        return f"\n\n{fence}\n{content}\n{fence}\n\n"
    if tag in {"ul", "ol"}:
        lines = []
        for i, child in enumerate(
            (c for c in node.children if isinstance(c, Node) and c.tag == "li"), 1
        ):
            body = "".join(
                markdown(c, base, list_depth + 1) for c in child.children
            ).strip()
            marker = f"{i}." if tag == "ol" else "-"
            lines.append(f"{'  ' * list_depth}{marker} {body}")
        return "\n\n" + "\n".join(lines) + "\n\n"
    if tag == "table":
        rows = []
        for row in node.walk():
            if row.tag == "tr":
                cells = [
                    re.sub(r"\s+", " ", markdown(c, base)).strip().replace("|", "\\|")
                    for c in row.children
                    if isinstance(c, Node) and c.tag in {"td", "th"}
                ]
                if cells:
                    rows.append(cells)
        if not rows:
            return ""
        width = max(map(len, rows))
        rows = [r + [""] * (width - len(r)) for r in rows]
        rows.insert(1, ["---"] * width)
        return "\n\n" + "\n".join("| " + " | ".join(r) + " |" for r in rows) + "\n\n"
    content = "".join(markdown(c, base, list_depth) for c in node.children)
    if re.fullmatch(r"h[1-6]", tag):
        return f"\n\n{'#' * int(tag[1])} {content.strip()}\n\n"
    if tag in {"p", "div", "section", "article", "figure", "figcaption"}:
        return "\n\n" + content.strip() + "\n\n"
    if tag == "blockquote":
        return (
            "\n\n"
            + "\n".join("> " + line for line in content.strip().splitlines())
            + "\n\n"
        )
    if tag == "br":
        return "  \n"
    if tag == "hr":
        return "\n\n---\n\n"
    if tag == "a":
        href = public_link(attrs.get("href", ""), base)
        return f"[{content.strip()}](<{href}>)" if href and content.strip() else content
    if tag == "img":
        src = public_link(attrs.get("src", ""), base) if attrs.get("src") else ""
        alt = (attrs.get("alt") or "Figure").replace("[", "(").replace("]", ")")
        return f"\n\n![{alt}](<{src}>)\n\n" if src else ""
    if tag in {"strong", "b"}:
        return f"**{content}**" if content.strip() else content
    if tag in {"em", "i"}:
        return f"*{content}*" if content.strip() else content
    if tag == "code":
        return "`` " + content + " ``"
    return content


def extract_article(html, url):
    """Extract the exposed article body; never infer access to hidden paid text."""
    parser = Document()
    parser.feed(html)
    nodes = list(parser.root.walk())
    metadata = {
        n.attrs.get("property", n.attrs.get("name")): n.attrs.get("content")
        for n in nodes
        if n.tag == "meta"
    }
    structured = []
    for n in nodes:
        if n.tag == "script" and n.attrs.get("type") == "application/ld+json":
            try:
                value = json.loads(plain(n))
                structured.extend(value if isinstance(value, list) else [value])
            except (ValueError, TypeError):
                continue
    news = next(
        (
            s
            for s in structured
            if isinstance(s, dict)
            and s.get("@type") in {"NewsArticle", "Article", "BlogPosting"}
        ),
        {},
    )
    body = next(
        (
            n
            for n in nodes
            if {"body", "markup"} <= set((n.attrs.get("class") or "").split())
        ),
        None,
    )
    if body is None:
        body = next(
            (
                n
                for n in nodes
                if set((n.attrs.get("class") or "").split())
                & {"entry-content", "post-content", "post-body"}
            ),
            None,
        )
    if body is None:
        raise ResearchError(
            "No supported article body found; login/error shells are not articles"
        )
    text = (
        re.sub(r"\n[ \t]*\n(?:[ \t]*\n)+", "\n\n", markdown(body, url)).strip() + "\n"
    )
    if len(plain(body).split()) < 30:
        raise ResearchError("Exposed article body is too short to archive reliably")
    paywall = any(
        n.attrs.get("data-testid") == "paywall"
        or "paywall" in (n.attrs.get("class") or "").split()
        for n in nodes
    )
    status = (
        "public_preview"
        if paywall or news.get("isAccessibleForFree") is False
        else "public_article"
        if news.get("isAccessibleForFree") is True
        else "unverified_capture"
    )
    authors = news.get("author", [])
    authors = authors if isinstance(authors, list) else [authors]
    return {
        "title": (news.get("headline") or metadata.get("og:title") or "").strip(),
        "published_on": news.get("datePublished"),
        "authors": [
            a.get("name", "") if isinstance(a, dict) else str(a) for a in authors
        ],
        "access_status": status,
        "paywall_detected": paywall,
        "word_count": len(plain(body).split()),
        "markdown": text,
        "response_sha256": hashlib.sha256(html.encode()).hexdigest(),
    }


def fetch_article(url, timeout=20):
    request = Request(
        url,
        headers={
            "User-Agent": "GIGAWATT-research/0.2 (permitted local article archive)",
            "Accept": "text/html",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        if urlsplit(response.url).hostname not in SA_HOSTS:
            raise ResearchError("Article redirected outside the selected publisher")
        content = response.read(10_000_001)
        if len(content) > 10_000_000:
            raise ResearchError("Article response exceeds 10 MB")
        return content.decode(response.headers.get_content_charset() or "utf-8")


def selected_sources(root, ids=None, include_candidates=False):
    m = read_json(root / "course/domain-map.json")
    catalog = validate_catalog(read_json(root / "course/research-sources.json"), m)
    sources = list(catalog)
    if include_candidates and (root / "research/discovery.json").exists():
        sources += candidate_sources(
            read_json(root / "research/discovery.json"),
            domain_ids(m),
            {s["url"] for s in catalog},
        )
    if ids:
        unknown = set(ids) - {s["id"] for s in sources}
        if unknown:
            raise ResearchError(f"Unknown source IDs: {sorted(unknown)}")
    return [
        s
        for s in sources
        if (not ids or s["id"] in ids)
        and urlsplit(s["url"]).hostname in SA_HOSTS
        and s.get("triage") not in {"exclude", "defer"}
    ]


def load_manifest(root):
    path = root / ARCHIVE / "manifest.json"
    return read_json(path) if path.exists() else {"schema_version": 1, "records": {}}


def permission_context(root, note):
    manifest = load_manifest(root)
    note = note or manifest.get("permission_basis")
    if not note or not note.strip():
        raise ResearchError(
            "Record the publisher permission context once with --permission-note"
        )
    if manifest.get("permission_basis") != note:
        manifest["permission_basis"] = note
        save_manifest(root, manifest)
    return note


def check(root):
    records = load_manifest(root)["records"]
    count = 0
    for sid, record in records.items():
        if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", sid):
            raise ResearchError("Unsafe source ID in archive manifest")
        if record.get("file_sha256"):
            path = root / ARCHIVE / f"{sid}.md"
            if (
                not path.exists()
                or hashlib.sha256(path.read_bytes()).hexdigest()
                != record["file_sha256"]
            ):
                raise ResearchError(f"{sid}: missing or modified archive capture")
            count += 1
    return count


def save_manifest(root, manifest):
    atomic_write(
        root / ARCHIVE / "manifest.json",
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
    )
    lines = [
        "# Local article archive",
        "",
        "Generated capture index. Source notes and course design remain separate. Captured text is not a completed source review. Figures remain links to publisher assets.",
        "",
        "| Article | Domains | Selection | Capture | Words |",
        "| --- | --- | --- | --- | --- |",
    ]
    for sid, r in sorted(
        manifest["records"].items(),
        key=lambda item: (item[0].startswith("DISC_"), item[0]),
    ):
        label = r.get("title", sid).replace("|", "\\|")
        link = (
            f"[{sid} — {label}]({sid}.md)"
            if r.get("file_sha256")
            else f"{sid} — {label}"
        )
        selection = r.get(
            "selection", "discovery candidate" if sid.startswith("DISC_") else "curated"
        )
        status = r.get("access_status", "fetch_failed") + (
            "; last refresh failed" if r.get("last_attempt_error") else ""
        )
        lines.append(
            f"| {link} | {', '.join(r.get('domains', []))} | {selection} | {status} | {r.get('word_count', '—')} |"
        )
    atomic_write(root / ARCHIVE / "INDEX.md", "\n".join(lines) + "\n")


def store_capture(root, source, article, permission_note, *, explicit_import=False):
    manifest = load_manifest(root)
    sid = source["id"]
    previous = manifest["records"].get(sid, {})
    path = root / ARCHIVE / f"{sid}.md"
    if path.exists() and not explicit_import:
        if hashlib.sha256(path.read_bytes()).hexdigest() != previous.get("file_sha256"):
            raise ResearchError(f"{sid}: local article was edited; preserving it")
        if (
            previous.get("access_status") in FULL
            and article["access_status"] not in FULL
        ):
            return "preserved_full_capture"
    body = article.pop("markdown")
    record = {
        **article,
        "id": sid,
        "url": canonical_url(source["url"]),
        "title": article.get("title") or source["title"],
        "domains": source["domains"],
        "selection": "discovery candidate"
        if source.get("kind") == "discovery_candidate"
        else "curated",
        "captured_on": datetime.now(UTC).isoformat(),
        "permission_basis": permission_note,
    }
    content = (
        "---\n"
        + "\n".join(
            f"{key}: {json.dumps(value, ensure_ascii=False)}"
            for key, value in record.items()
        )
        + "\n---\n\n"
        + f"# {record['title']}\n\n"
        + f"[Publisher original]({record['url']}) · [Research note](../sources/{sid}.md) · Capture: **{record['access_status']}**. This is source text, not the course's explanation or a verification verdict.\n\n"
        + body
    )
    record["file_sha256"] = hashlib.sha256(content.encode()).hexdigest()
    atomic_write(path, content)
    manifest["records"][sid] = record
    save_manifest(root, manifest)
    return record["access_status"]


def sync(
    root,
    ids=None,
    *,
    include_candidates=False,
    refresh=False,
    timeout=20,
    delay=1,
    permission_note,
    fetch=fetch_article,
):
    sources = selected_sources(root, ids, include_candidates)
    if not sources:
        raise ResearchError("No selected SemiAnalysis sources to archive")
    permission_note = permission_context(root, permission_note)
    results = []
    for i, source in enumerate(sources):
        sid = source["id"]
        manifest = load_manifest(root)
        previous = manifest["records"].get(sid, {})
        if previous.get("file_sha256") and not refresh:
            path = root / ARCHIVE / f"{sid}.md"
            if (
                path.exists()
                and hashlib.sha256(path.read_bytes()).hexdigest()
                == previous["file_sha256"]
            ):
                results.append((sid, "cached"))
                continue
        try:
            captured = extract_article(fetch(source["url"], timeout), source["url"])
            status = store_capture(root, source, captured, permission_note)
        except (ResearchError, OSError, ValueError) as exc:
            status = "fetch_failed"
            manifest = load_manifest(root)
            record = manifest["records"].setdefault(
                sid,
                {
                    "title": source["title"],
                    "url": source["url"],
                    "domains": source["domains"],
                },
            )
            record["last_attempt_error"] = str(exc)
            record["last_attempt_on"] = datetime.now(UTC).isoformat()
            save_manifest(root, manifest)
            print(f"{sid}: {status}: {exc}", flush=True)
        else:
            print(f"{sid}: {status}", flush=True)
        results.append((sid, status))
        if i < len(sources) - 1 and delay:
            time.sleep(delay)
    return results


def import_article(root, source_id, path, *, complete=False, permission_note):
    sources = selected_sources(root, [source_id], include_candidates=True)
    if not sources:
        raise ResearchError("The selected source is not a SemiAnalysis record")
    source = sources[0]
    permission_note = permission_context(root, permission_note)
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".html", ".htm"}:
        article = extract_article(text, source["url"])
        if complete and article["paywall_detected"]:
            raise ResearchError(
                "This HTML contains a paywall/preview signal; it cannot be labeled complete"
            )
    else:
        if not text.strip():
            raise ResearchError("Imported article is empty")
        article = {
            "title": source["title"],
            "authors": [],
            "published_on": source.get("published_on"),
            "markdown": text,
            "word_count": len(text.split()),
            "response_sha256": hashlib.sha256(text.encode()).hexdigest(),
        }
    article["access_status"] = (
        "imported_full_article" if complete else "imported_text_unverified"
    )
    return store_capture(root, source, article, permission_note, explicit_import=True)
