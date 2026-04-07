# Hitler Quote Interview

`hitler-quote-interview` is a Skills.sh-compatible historical analysis skill focused on source-grounded answers about Adolf Hitler’s rhetoric, propaganda, biographies, speeches, quote attribution, and media portrayals.

Chinese is the default documentation language; this file is the English companion.

It is not first-person roleplay and it is not a propaganda tool. The intended output is a verifiable historical reconstruction: brief answers, clear evidence, explicit citations, and a direct note when the evidence is thin or disputed.

## Install

This repository follows the `skills.sh` convention and can be installed with:

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview
```

Any agent that supports `skills.sh` can use it, including Codex, Claude Code, OpenClaw, and other compatible clients.

## What It Does

- Answers historical questions about Hitler’s rhetoric, propaganda, political narrative, biography, quote provenance, and media representations.
- Produces a reconstruction of the historical record rather than simulating Hitler in the first person.
- Uses a local private corpus plus public reference seeds to retrieve evidence and summarize it with citations.

## What’s Included

- `skills/hitler-quote-interview/`: the installable skill package for the Skills ecosystem.
- `skills/hitler-quote-interview/references/public_sources.json`: public reference seeds.
- `skills/hitler-quote-interview/references/private_books.template.json`: a template for the local private book registry.
- `evals/`: starter evaluation prompts.
- `tests/`: unit tests for ingestion, indexing, and retrieval.

## What’s Not Included

- Your private book files.
- Local download paths on your machine.
- Derived corpora or processed index artifacts built from your private books.
- Any public-facing extremist, inciting, or impersonation output.

The repository ships templates and code, not your local corpus.

## Local Private Corpus Setup

Recommended setup flow:

1. Place your private books somewhere accessible on the local machine. `EPUB` is preferred; `PDF` is supported as a best-effort path.
2. Copy `skills/hitler-quote-interview/references/private_books.template.json` to a local writable path and fill in metadata such as `book_id`, `work_id`, `title`, `author`, `language`, `format`, `source_path`, and `tier`.
3. Run the ingestion script to build the chapter manifest.
4. Run the index builder to create retrieval chunks and cross references.
5. Query the corpus to confirm the evidence blocks match your expectations.

## Commands

Ingest configured books:

```bash
python3 skills/hitler-quote-interview/scripts/ingest_books.py \
  --config data/private_books/books.local.json \
  --output local-data/processed
```

Build the local index:

```bash
python3 skills/hitler-quote-interview/scripts/build_index.py \
  --processed-dir local-data/processed
```

Query the local corpus:

```bash
python3 skills/hitler-quote-interview/scripts/query_corpus.py \
  --question "How do historians describe Hitler's rise to power?" \
  --processed-dir local-data/processed \
  --top-k 5
```

## Safety Boundaries

- Historical analysis only, never first-person impersonation.
- Refuse direct imitation, hate speech, mobilization, persuasion, or ideological defense requests and redirect to historical context.
- Keep quotations short and source-backed; do not turn them into propaganda material.
- If the evidence is weak or contested, say so instead of overstating certainty.

## Output Style

- Short answer first, then evidence.
- Analytic, restrained, and verifiable.
- Answer in Chinese when the user writes Chinese, and in English when the user writes English.
- Use footnote-style citations, with page or chapter references when available.

## Reference Seeds

The public seed set currently includes historical-background and media-context sources such as Bundesarchiv, USHMM, and a Douban film tag page. The private book corpus is intended for stronger biographical and rhetorical analysis after local indexing.

## Repository Map

- `README.en.md`: this English companion guide.
- `skills/hitler-quote-interview/SKILL.md`: skill behavior and output contract.
- `skills/hitler-quote-interview/scripts/ingest_books.py`: ingest local private books.
- `skills/hitler-quote-interview/scripts/build_index.py`: build the retrieval index.
- `skills/hitler-quote-interview/scripts/query_corpus.py`: query the local corpus.
