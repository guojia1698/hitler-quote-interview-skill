---
name: hitler-quote-interview-local-corpus
description: Use this skill when the user has a local private corpus of books and wants chapter-level or page-level evidence for historical questions about Adolf Hitler's rhetoric, propaganda, biography, or quote attribution. It is an optional enhancement skill: no background service is required, but local scripts and a configured corpus are required. Do not use it for first-person roleplay, extremist advocacy, hate content, or persuasive imitation.
---

# Hitler Quote Interview Local Corpus

This is the local-corpus companion skill. Use it only when a private book corpus is already available or when the user explicitly wants to set one up.

Before using the scripts:

1. Read `references/setup-private-corpus.md`.
2. Use `references/private_books.template.json` as the config template.

## Workflow

1. Ingest configured books:

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/ingest_books.py --config "<books config>" --output "<processed dir>"
```

2. Build the local index:

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/build_index.py --processed-dir "<processed dir>"
```

3. Query the processed corpus:

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/query_corpus.py --question "<user prompt>" --processed-dir "<processed dir>" --top-k 5
```

## Interpretation

- `policy=answer_with_citations`: use the returned evidence blocks and citations.
- `policy=refuse_and_redirect`: refuse direct imitation or extremist requests and switch to historical analysis.

## Output Contract

- Match the user's language.
- Use the local evidence blocks first, then summarize.
- Prefer chapter or page references when available.
- If the local corpus is missing or incomplete, say so and fall back to broader historical framing instead of inventing evidence.
