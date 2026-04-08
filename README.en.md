<div align="center">

<h1>洗头佬.skill</h1>

<p><strong>A <code>skills.sh</code>-compatible historical research skill matrix</strong></p>

<p>Built for source-grounded, interview-style historical reconstructions.</p>
<p><strong>Zero-setup by default, with optional private-corpus augmentation when you need stronger citations.</strong></p>
<p><em>Speak like an interview. Cite like a historian.</em></p>

<p>
  <img alt="skills.sh compatible" src="https://img.shields.io/badge/skills.sh-compatible-111111?style=for-the-badge">
  <img alt="zero setup" src="https://img.shields.io/badge/zero--setup-default-0f766e?style=for-the-badge">
  <img alt="multi skill matrix" src="https://img.shields.io/badge/multi--skill-matrix-9a3412?style=for-the-badge">
  <img alt="archival interview mode" src="https://img.shields.io/badge/archival--interview-mode-1d4ed8?style=for-the-badge">
</p>

<p>
  <a href="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml"><img alt="Tests" src="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml/badge.svg"></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
</p>

<p><a href="./README.md">中文</a> · <a href="./README.en.md">English</a></p>

<p><code>Codex</code> · <code>Claude Code</code> · <code>OpenClaw</code> · <code>skills.sh</code> ecosystem</p>

<p><sub>Zero-setup by default. Evidence on demand. Local corpus when you need stronger depth.</sub></p>

</div>

---

> A historical research skill matrix. The default output is tuned to feel like an archival interview transcript rather than an encyclopedia summary or an uncontrolled persona roleplay.

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill hitler-quote-interview
```

| Dialogue-first | Zero-setup | Local evidence |
| --- | --- | --- |
| Feels closer to an archival interview than an essay | Works immediately after install | Bring in a private corpus only when you need stronger citations |

**Why it feels production-ready**

- install and use immediately, with no local service required
- default output is a single reconstructed dialogue turn, not a mini essay
- sources expand on demand instead of cluttering every reply
- deeper book-level evidence is available through the companion local-corpus skill

**What it feels like**

```text
Q: How did Hitler usually attack parliamentary democracy in the late Weimar years?
A: Reconstructed answer: He would usually frame parliament as weak, delayed, and symbolic of national division, then recast crisis as something only concentrated leadership could resolve.
```

```text
Q: I feel exhausted lately. What should I do?
A: Reconstructed answer: In his authoritarian public framing, he would likely have treated exhaustion as a failure of will and demanded that discipline and mission override personal strain.
```

`hitler-quote-interview` is a `skills.sh`-compatible historical research skill set for producing reconstructed answers that feel closer to an on-record historical interview than a generic explainer.

The repository now supports two usage modes:
- Zero-setup mode: install and use immediately, with no local service, database, or index process.
- Local-corpus augmentation: optionally run ingestion and retrieval scripts against your own private books for stronger chapter-level evidence.

## Use Cases

Use this project for questions such as:
- how his public rhetoric was structured, repeated, and staged
- how major biographers describe his rise, rule, and historical consequences
- whether a quote is reliable, misattributed, or better treated as paraphrase
- where to start with documentaries, films, and source-oriented historical guides

This skill does not impersonate Hitler or generate propaganda; it produces concise historical reconstructions grounded in the biographical and rhetorical record.

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
- prefer an interview-style reconstructed answer instead of an encyclopedia paragraph
- default to a single compact reconstructed answer
- expand into sources or historian comparison only when the user asks
- keep follow-up turns conversational rather than restarting from scratch

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
