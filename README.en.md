# Hitler Quote Interview

[![Tests](https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml/badge.svg)](https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](./LICENSE)

[中文](./README.md) | English

`hitler-quote-interview` is a `skills.sh`-compatible historical research skill set for producing source-grounded answers about Adolf Hitler's rhetoric, propaganda, biography, quote attribution, and media portrayals.

The repository now supports two usage modes:
- Zero-setup mode: install and use immediately, with no local service, database, or index process.
- Local-corpus augmentation: optionally run ingestion and retrieval scripts against your own private books for stronger chapter-level evidence.

## Scope

Use this project for questions such as:
- how his public rhetoric was structured, repeated, and staged
- how major biographers describe his rise, rule, and historical consequences
- whether a quote is reliable, misattributed, or better treated as paraphrase
- where to start with documentaries, films, and source-oriented historical guides

This skill does not impersonate Hitler or generate propaganda; it produces evidence-backed historical reconstructions and states uncertainty when sources are thin or disputed.

## Skill Matrix

| Skill | Mode | Use |
| --- | --- | --- |
| `hitler-quote-interview` | Zero-setup | Default entry point. Produces interview-style historical reconstructions immediately after install. |
| `hitler-quote-interview-source-attribution` | Zero-setup | Focused on quote provenance, contested wording, and historian disagreement. |
| `hitler-quote-interview-local-corpus` | Local augmentation | Connects to your own private book corpus for chapter-level or page-level evidence. |

## Install

Install the default skill:

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview
```

Install the source-attribution skill:

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview-source-attribution
```

Install the local-corpus augmentation skill:

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview-local-corpus
```

The repository is intended for Codex, Claude Code, OpenClaw, and other agents that understand the `skills.sh` / `SKILL.md` convention.

## Quick Start

### 1. Zero-setup mode

After installing `hitler-quote-interview`, you can use it directly. The default behavior is:
- match the user's language
- answer briefly first, then cite sources or historians
- frame the answer as a reconstruction grounded in sources
- state uncertainty explicitly when the evidence is thin or disputed

Example prompts:

```text
请用中文概括一下，1930年代希特勒是如何通过宣传和政治仪式塑造个人形象的？
```

```text
Explain in English how major biographers describe Hitler's rise to power.
```

### 2. Source-attribution mode

If your main concern is provenance, disputed wording, or historian comparison, install `hitler-quote-interview-source-attribution`.

Example prompts:

```text
“某某语录”真的是希特勒说的吗？如果不可靠，请说明它更像是后人概括还是二手转述。
```

```text
Compare how Kershaw and Ullrich frame Hitler's political style.
```

### 3. Local-corpus augmentation

Only use `hitler-quote-interview-local-corpus` if you want retrieval over your own private books. It does not require a daemon, but it does run local scripts on demand.

1. Prepare a local config from [private_books.template.json](./skills/hitler-quote-interview-local-corpus/references/private_books.template.json).
2. Run ingestion to build `books_manifest.json` and `sections.jsonl`.
3. Run index building to create `chunks.jsonl`, `works_index.json`, and `cross_language_links.json`.
4. Query the processed corpus for candidate evidence blocks.

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/ingest_books.py \
  --config data/private_books/books.local.json \
  --output local-data/processed
```

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/build_index.py \
  --processed-dir local-data/processed
```

```bash
python3 skills/hitler-quote-interview-local-corpus/scripts/query_corpus.py \
  --question "How do historians describe Hitler's rise to power?" \
  --processed-dir local-data/processed \
  --top-k 5
```

See [setup-private-corpus.md](./skills/hitler-quote-interview-local-corpus/references/setup-private-corpus.md) for the detailed setup notes.

## Output Contract

All skills share the same response boundaries:
- match the user's language
- use historical reconstruction or historian framing instead of first-person impersonation
- keep quotations short and sourceable; prefer paraphrase when provenance is unclear
- refuse direct imitation, mobilization, hate, or ideological defense requests and redirect to historical analysis

## Repository Layout

```text
.
├── README.md
├── README.en.md
├── skills/
│   ├── hitler-quote-interview/
│   ├── hitler-quote-interview-source-attribution/
│   └── hitler-quote-interview-local-corpus/
├── tests/
├── evals/
└── .github/workflows/
```

Notes:
- `skills/hitler-quote-interview/` is the default zero-setup skill.
- `skills/hitler-quote-interview-source-attribution/` handles provenance and contested-source questions.
- `skills/hitler-quote-interview-local-corpus/` is the private-corpus retrieval layer.
- `tests/`, `evals/`, and `.github/workflows/` support verification and CI.

## Development

Local tooling expects `Python 3.10+`:

```bash
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
```

The test suite currently covers:
- `EPUB` / `PDF` ingestion
- index building and cross-language links
- biography / rhetoric / media / unsafe-roleplay routing
- skill matrix structure and zero-setup expectations

## License

This project is released under the [MIT License](./LICENSE).
