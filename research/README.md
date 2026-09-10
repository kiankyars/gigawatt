# GIGAWATT research library

Use this library before repeating a web search. It connects the course's
[domain map](../course/DOMAIN_MAP.md) to a persistent source inventory and one
Markdown research note per curated source or selected discovery candidate. A local
article archive now stores searchable source text alongside those original notes.

[Browse the source index](INDEX.md) · [Curated search log](discovery-searches.md)
· [Editable catalog](../course/research-sources.json)

[Power-conversion research notes](power-conversion-notes.md): a concise synthesis
of Kian's SST, AC/HVDC and insulation questions, with networking context kept as
reference rather than additional teaching scope.

The library covers SemiAnalysis **and** primary sources from operators, vendors,
standards bodies, public agencies and original research. It separates discovery,
source review and verification of a specific claim. No publisher or archive is
the course's source of truth.

## Read and maintain the article archive

The three layers have distinct jobs:

- `research/discovery.json` indexes publisher metadata and relevance decisions.
- `research/articles/INDEX.md` indexes local article captures; each source has a
  Markdown file such as `research/articles/SA41.md`, with authors, date, URL,
  capture status, permission context and file hash. `manifest.json` records the
  capture inventory and failures. This folder is ignored by Git and excluded
  from Pages; it is the working text library for course research.
- `research/sources/SA41.md` contains original claim checks, curriculum connections
  and unresolved questions. These source notes remain public and separately reviewed.

Kian reported confirmation from SemiAnalysis's publishers on 2026-09-10 that the
course research use is permitted. That context is recorded in the local archive.
The original source text remains distinguishable from the course's explanations.

```sh
# Reuse existing captures; fetch missing curated SemiAnalysis articles.
uv run gigawatt-research archive sync

# Also capture mapped discovery candidates; their relevance remains unreviewed.
uv run gigawatt-research archive sync --include-candidates

# Refresh one article explicitly. A preview cannot replace a saved full article.
uv run gigawatt-research archive sync --source SA41 --refresh

# Import a complete publisher-provided or authorized local export.
uv run gigawatt-research archive import \
  --source SA41 --file /absolute/path/to/article.md --complete

# Verify saved bytes offline, then search article text without another web query.
uv run gigawatt-research archive check
rg -n -i 'behind.the.meter|islanding|fuel supply' research/articles/
```

The archive currently supports SemiAnalysis's article markup and common legacy
article-body containers, plus provided Markdown/text/HTML exports. It preserves
headings, paragraphs, lists, tables, code and source links. Figures remain links
to publisher assets; their image files are not downloaded. Unknown page structures,
login shells and short/non-article responses produce an explicit failure instead
of being stored as a complete article.

`public_article` means the publisher marked the captured article freely accessible;
`public_preview` means a paywall or paid-access signal was present.
`unverified_capture` means the body was extracted but completeness is not established.
`imported_full_article` records a supplied export declared complete with `--complete`;
`imported_text_unverified` preserves an export without that declaration. None of
these statuses means the technical claims were reviewed. HTML containing an explicit paywall cannot
be labeled complete by the importer; a provided full paid export can be declared
complete even when its metadata identifies a subscriber article. Failed requests retain earlier captures and
report a nonzero exit status; edited local files are preserved and flagged.

The public fetch does not use browser credentials. Publisher permission and
technical access are separate: importing an available full export fills a paid
article's missing portion. The linked BTM report is `SA41`; its public capture
is explicitly a preview. Its source note maps further work into existing domains.

On a fresh machine, record the permission context once with
`archive sync --permission-note "Publisher permission context"`; later runs reuse
that local record. `--source` can be repeated; `--timeout` and `--delay` bound
requests. The archive uses no LLM summaries or automatic lesson promotion.

## Run the pipeline

From the repository root:

```sh
# Discover public metadata. Defaults to the SemiAnalysis XML sitemap.
uv run gigawatt-research discover

# Include the public feed to enrich recent records with publisher titles.
uv run gigawatt-research discover \
  --url https://newsletter.semianalysis.com/sitemap.xml \
  --url https://newsletter.semianalysis.com/feed

# Generate/update local notes and the index, preserving human note bodies.
uv run gigawatt-research build --include-candidates

# Validate metadata, domain references and generated freshness without writing.
uv run gigawatt-research check --include-candidates

# Regenerate the domain atlas after changing curated source mappings.
uv run gigawatt-map
uv run gigawatt-map --check
```

`build` and `check` run offline. Omit `--include-candidates` to build an index of
curated sources only. Candidate notes already on disk are not deleted. Use the
same option for build and check so the expected index agrees.

Discovery is an explicit refresh, not a background monitor. It reads only
sitemap/RSS/Atom metadata, discards feed body fields, and follows bounded
same-publisher sitemap indexes. It does not follow article links or extract
article prose. The default limit is four metadata documents, with a one-second
delay between requests and a 20-second request timeout; flags can change those
bounds. A failed request or exhausted document limit saves the successful
metadata and reports a partial/failed run with a nonzero exit code. An empty or
failed refresh never erases previous records or decisions.

## Which file owns what

| File                                 | Role                                                                                           | Edit policy                                                                                                            |
| ------------------------------------ | ---------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| `course/research-sources.json`       | Curated source identity, review scope, dates, original use/caution notes and domain mappings   | Edit after reviewing the relevant material. Keep stable source IDs.                                                    |
| `research/discovery.json`            | Durable metadata inventory, URL aliases, keyword suggestions, triage decisions and run history | Discovery refreshes metadata. Edit `triage`, `domains` and `notes` to record decisions; later refreshes preserve them. |
| `research/sources/SAxx.md`, `Pxx.md` | One local note for each curated source                                                         | The marked metadata region is generated. Write original claim checks and teaching notes below it.                      |
| `research/sources/DISC_*.md`         | Notes for candidates with domain suggestions or explicit domain assignments                    | These are unreviewed leads. A deterministic URL-based ID avoids repeated files for the same URL.                       |
| `research/INDEX.md`                  | Navigable index across the generated source notes                                              | The marked index region is generated; the body below it is preserved.                                                  |
| `research/discovery-searches.md`     | Human-readable search trail and scope limits                                                   | Record queries, indexes inspected, what was actually read and remaining gaps.                                          |

The generator refuses to overwrite a note without its expected managed-region
markers. It prepares outputs before writing, preserves everything after the
end marker byte-for-byte, and does not delete notes for retired or excluded
sources. Review removal and migration explicitly when the catalog changes.

## Add sources from any publisher

For a reviewed source, add a record to `course/research-sources.json` using the
existing schema and a unique ID. Give it actual review scope, dates where known,
one or more domain IDs, an original explanation of its use and specific limits.
Run the note and atlas builders afterward.

For search-agent results or an external metadata collection, import a JSON list
or an object containing a `sources` or `items` list. A record needs a real URL
and title; domain tags and a triage decision are optional:

```json
[
  {
    "url": "https://blogs.nvidia.com/blog/800-vdc-power-architecture-ai-factory/",
    "title": "Why Scaling AI Compute Performance Requires a New Power Architecture",
    "publisher": "NVIDIA",
    "published_on": "2026-08-11",
    "domains": ["D04", "D06"],
    "triage": "include",
    "notes": "An identified primary vendor announcement; review deployment claims separately."
  }
]
```

```sh
uv run gigawatt-research discover --import /absolute/path/to/source-metadata.json
```

Imports whitelist metadata fields and do not copy arbitrary article-body fields.
Importing a record never promotes it to reviewed source evidence. Existing
decisions take precedence when a later import or discovery observes the same URL.
Known same-path SemiAnalysis host aliases and tracking parameters are normalized;
meaningful query parameters and distinct dated historical routes are retained.

## From discovery to teaching

1. **Discover.** Save the search results or publisher metadata once. The XML
   sitemap provides broad discovery; the feed enriches recent titles. Follow
   [the search log](discovery-searches.md) when a publisher index misses a subject.
2. **Triage.** Review the candidate against the learner's objective. Set `triage`
   to `include`, `exclude` or `defer`, assign deliberate `domains`, and record a
   reason in `notes`. Unreviewed keyword suggestions are not editorial decisions.
3. **Read.** Inspect the accessible source and its original references. Record
   whether the reading was a page, preview, abstract or selected sections. Leave
   inaccessible paid material unreviewed.
4. **Curate.** Add a stable source record with original use/caution notes. Add
   claim-level checks below its Markdown metadata block, including exact source
   locations, contradictory evidence and remaining questions.
5. **Teach.** Connect an objective to a mechanism, worked example, comparison,
   failure or limiting case, and a transfer assessment. Attach exact citations
   to the claims and visual boundaries used in the lesson.
6. **Refresh.** Re-run discovery for new metadata; check time-sensitive claims
   before recording. Preserve the source snapshot associated with the video.

**Anti-pattern: the encyclopedic survey.** An included article does not earn a
chapter, and mentioning a topic does not satisfy an objective. Multiple sources
can inform one lesson; one source can inform several domains. Record duplicates,
case-only uses and exclusions rather than forcing every source into the script.

## Honest coverage and access states

- `candidate_not_reviewed`: substantive content has not been reviewed.
- `public_excerpt_reviewed`: only the stated accessible preview, abstract or
  indexed excerpt was reviewed; this does not imply access to the full work.
- `page_reviewed`: the identified page was inspected, within the limits in its
  caution field; linked documents and chapters require separate review.

A completed discovery run means its requested metadata documents were processed
within the bound. It does **not** mean every relevant article exists in that
index, every candidate was classified, or every source claim was verified.
Sitemap last-modified dates are not publication dates; URL slugs are not verified
titles. The inventory records their origin so later work can correct them.

Use the curated selection and discovery queue together. Keywords can miss an
article with an unexpected title, and can match a semiconductor or financial
article outside our scope. The current domain map is a planning baseline; none
of its objectives is certified complete by the research pipeline.

## Content and reuse

The public library contains original research notes, citations and course material.
The local article archive retains publisher text under the permission context
reported by Kian, with provenance and access limits. It is not staged for public
redistribution. Capture does not certify technical claims or add a curriculum
requirement; course design remains in the filled-in template.

The purpose is to preserve useful research so future authoring starts with the
saved text, known source, its limits and the next unresolved question.

## Initial run — 2026-09-06

The public sitemap and feed refresh completed at 22:19 UTC. It recorded 352
metadata observations, deduplicated to **332 URLs**, including **330 article
URLs**. The curated catalog now holds **56 sources: 40 SemiAnalysis and 16
primary references**. The generated library contains **111 source notes**:
56 curated records and 55 additional unreviewed discovery candidates, plus the
index. A curated record can still be limited to a preview or an unreviewed lead;
consult its individual status. These are discovery and planning counts, not a
claim of exhaustive coverage or completed claim verification.

Offline freshness checks passed, and a second build changed zero files while
preserving the added claim notes. The isolated tests cover alias deduplication,
manual decisions, malformed or failed discovery, metadata-only imports,
generated freshness and preservation of human research bodies.

## Lesson expansion — 2026-09-06

The library now contains 101 curated source records, including the requested
[NVIDIA NVL72 component reference](sources/P17.md) and 44 additional primary
references used in the authored lessons. There are 57 distinct primary source
connections in the 50-lesson manuscript. Each lesson preserves its specific
claim, reading date and access limit. These counts do not promote previews,
abstracts or indexes to full-document reviews. `E*.md` records are additional
primary references with stable URL-derived IDs.

## Rack-format review — 2026-09-08

Two primary mechanical-format references were added after finding a rack-unit
teaching gap: Eaton's rack basics (indexed excerpts reviewed; direct page blocked)
and OCP Open Rack V3 Base Specification rev. 1.0 (selected mechanical sections
reviewed). The current catalog contains 103 curated records, and 59 source
records support the authored lessons. The new notes preserve the specific
access and revision limits.

## AC/DC sample correction — 2026-09-08

The catalog now contains 105 curated records. The added Schneider Electric
PM2200 calculation page supports balanced three-phase power arithmetic in the
480 V AC / 800 V DC teaching sample. An NVIDIA OCP announcement explicitly
identifies 415 or 480 V three-phase AC as relevant distribution baselines. These
notes distinguish those references from measured savings: converter losses are
teaching assumptions and conductor losses are original calculations. The main
50-lesson manuscript still uses 59 source records; sample-specific evidence is
included in the sample's own reference list.

## UPS redundancy coverage audit — 2026-09-08

[The coverage review](redundancy-coverage-review.md) finds developed N+1 material
but missing N+2, 2(N+1), bypass and load-interface teaching, plus incomplete 2N
assessment. It proposes a bounded presenter sequence and changed-load exercise.
Four primary references were added with specific page, revision and access
limits. The catalog now contains 109 curated records. These additions do not
mark the missing lesson content or presentation as complete.
