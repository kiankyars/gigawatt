# Expanded lesson source

Each author owns one JSON file containing a `lessons` array and an optional
`sources` array for additional primary references. The first integration adapts
minor schema differences rather than discarding authored content.

Each lesson should have a stable `id`, `domain` (D01–D15), `title`, `question`,
`objectives` (existing objective IDs), `summary`, and `sections`: an ordered list
of `{heading, paragraphs}` with original explanatory prose. Include an explicit
worked example (`{title, givens, steps, result, boundary}`), tradeoff and failure
or limiting case, and transfer practice (`{question, answer, explanation}`).
Provide a `takeaway`, `source_ids`, and glossary terms where useful.

The generator normalizes source authoring into `course/expanded-course.json`,
readable Markdown lessons and an accessible HTML reader. This is an authored
draft, not a claim of external expert review, a tested recording, or a fixed
ten-hour runtime. Explain algebra and specialist terminology before using them.

Write three substantial lessons per domain, with every domain objective taught
and assessed. An example must be independently calculable; a failure must change
a stated condition; practice must apply the reasoning to a new case. Original
synthetic values must be labeled as such. No article-by-article paraphrase and
no wholesale reproduction of third-party prose or figures.
