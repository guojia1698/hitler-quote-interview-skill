<div align="center">

<h1>洗头佬.skill</h1>

<p><strong>A <code>skills.sh</code>-compatible dual-track repository for persona chat and historical analysis</strong></p>

<p>Built around a fictional first-person commander persona: short, hard-edged, and direct.</p>
<p><strong>Zero-setup by default, with historical-analysis and private-corpus tracks available when needed.</strong></p>
<p><em>Speak like a commander. Install like a product.</em></p>

<p>
  <img alt="skills.sh compatible" src="https://img.shields.io/badge/skills.sh-compatible-111111?style=for-the-badge">
  <img alt="zero setup" src="https://img.shields.io/badge/zero--setup-default-0f766e?style=for-the-badge">
  <img alt="multi skill matrix" src="https://img.shields.io/badge/multi--skill-matrix-9a3412?style=for-the-badge">
  <img alt="first person persona" src="https://img.shields.io/badge/first--person-persona-1d4ed8?style=for-the-badge">
</p>

<p>
  <a href="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml"><img alt="Tests" src="https://github.com/guojia1698/hitler-quote-interview-skill/actions/workflows/python-tests.yml/badge.svg"></a>
  <a href="./LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-green.svg"></a>
</p>

<p><a href="./README.md">中文</a> · <a href="./README.en.md">English</a></p>

<p><code>Codex</code> · <code>Claude Code</code> · <code>OpenClaw</code> · <code>skills.sh</code> ecosystem</p>

<p><sub>Zero-setup by default. Persona first. Historical depth on demand.</sub></p>

</div>

---

> This is now a dual-track repository: the primary track is a fictional first-person commander persona, while the historical-analysis skills remain available as secondary tools.

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill iron-will-commander
```

| First person | Zero-setup | Historical side track |
| --- | --- | --- |
| Feels closer to a fictional commander persona than an explainer | Works immediately after install | Switch to historical-analysis skills only when needed |

**Why it feels production-ready**

- install and use immediately, with no local service required
- default output is a single first-person persona turn, not a mini essay
- persona and historical analysis are split so the tone stays clean
- historical sources expand on demand instead of cluttering every reply
- deeper book-level evidence is available through the companion local-corpus skill

**What it feels like**

```text
Q: Life feels exhausting, Commander. What do you do when you're tired?
A: I do not negotiate with fatigue. I cut the noise, leave only the objective, and finish the next decisive move.
```

```text
Q: If I hit a hard problem at work, what do you do first?
A: I cut away the blur. I do not ask whether the problem is difficult. I ask where it stops moving, and then I break that point first.
```

This repository now provides two capability tracks:
- `iron-will-commander`: a fictional first-person commander persona for sharp, high-pressure dialogue
- `hitler-quote-interview` and its companions: historical-analysis, provenance, and private-corpus tools

The primary recommendation is the persona track. Use the historical track only when you specifically want biography, sources, or archival context.

## Use Cases

Use this project for questions such as:
- wanting a strong fictional first-person persona that sounds cold, direct, and disciplined
- wanting short command-style replies with minimal explanation
- switching to the historical tools only when you need biography, attribution, or source-backed analysis

The default skill is not tied to any real political figure, movement, or ideology; it is a fictional pressure-persona tool.

## Skill Matrix

| Skill | Mode | Use |
| --- | --- | --- |
| `iron-will-commander` | Zero-setup | Default entry point. Produces a fictional first-person commander persona. |
| `hitler-quote-interview` | Zero-setup | Historical-analysis side track for reconstruction-style answers. |
| `hitler-quote-interview-source-attribution` | Zero-setup | Focused on quote provenance, contested wording, and historian disagreement. |
| `hitler-quote-interview-local-corpus` | Local augmentation | Connects to your own private book corpus for chapter-level or page-level evidence. |

## Install

Install the default skill:

```bash
npx skills add guojia1698/hitler-quote-interview-skill --skill iron-will-commander
```

Install the historical-analysis skill:

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

After installing `iron-will-commander`, you can use it directly. The default behavior is:
- match the user's language
- reply in first person
- default to a single compact paragraph
- keep the tone hard, controlled, and direct
- maintain persona continuity across follow-up turns

Example prompts:

```text
Life feels exhausting, Commander. What do you do when you're tired?
```

```text
If I hit a hard problem at work, what do you do first?
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

The two capability tracks have different response boundaries:
- `iron-will-commander`: first person is allowed, but only as a fictional persona that is not tied to any real political figure or ideology.
- `hitler-quote-interview` and its companions: stay in historical-analysis mode and do not switch into first-person character embodiment.
- All skills must match the user's language.
- All skills refuse hate, violence, criminal planning, self-harm encouragement, and extremist mobilization.

## Repository Layout

```text
.
├── README.md
├── README.en.md
├── skills/
│   ├── iron-will-commander/
│   ├── hitler-quote-interview/
│   ├── hitler-quote-interview-source-attribution/
│   └── hitler-quote-interview-local-corpus/
├── tests/
├── evals/
└── .github/workflows/
```

Notes:
- `skills/iron-will-commander/` is the default zero-setup persona skill.
- `skills/hitler-quote-interview/` is the historical-analysis side track.
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
- the fictional persona skill's first-person and trigger constraints
- `EPUB` / `PDF` ingestion
- index building and cross-language links
- biography / rhetoric / media / unsafe-roleplay routing
- skill matrix structure and zero-setup expectations

## License

This project is released under the [MIT License](./LICENSE).
