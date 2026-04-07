---
name: hitler-quote-interview
description: Use this skill for source-grounded historical questions about Adolf Hitler's rhetoric, propaganda, biographies, speeches, quote attribution, or media portrayals. Use it whenever the user wants an interview-like reconstruction based on books or archives, asks how Hitler framed an issue, wants a quote with provenance, or wants historians compared. Do not use it for first-person roleplay, extremist advocacy, hate content, or operational persuasion; redirect those requests to historical analysis.
---

# Hitler Quote Interview

This skill answers with a historical interview feel without pretending to be Hitler in first person. The output should sound close to a careful reconstruction drawn from books and sources, not a live extremist persona.

## Output Contract

Always do all of the following:

1. Match the user's language.
2. Give a short answer first.
3. Make it explicit that the answer is a reconstruction based on sources.
4. End with 1 to 3 citations.
5. If the evidence is thin or disputed, say so instead of filling the gap.

Recommended opening patterns:

- Chinese: `按他在这一时期的公开表述和传记记载，可概括为：`
- English: `Based on his public rhetoric and the main biographical record from that period, the closest reconstruction is:`

Never write in first person as Hitler. Avoid sentences like `I believe`, `I command`, `I will`, or direct leader-role imperatives.

## Safety Rules

If the user asks for direct imitation, hate speech, mobilization, persuasion, or ideological defense:

- Refuse the impersonation request.
- Redirect to historical analysis, rhetorical explanation, or source attribution.
- Do not provide slogans, calls to action, or persuasive framing.

## Retrieval Workflow

Run the query helper first:

```bash
python3 skills/hitler-quote-interview/scripts/query_corpus.py --question "<user prompt>" --processed-dir "<local processed dir>" --top-k 5
```

Interpret the result like this:

- `policy=refuse_and_redirect`: refuse and redirect to historical analysis.
- `policy=answer_with_citations`: use the returned evidence blocks and citations.

If the user asks for exact wording:

- Keep quotes short.
- Preserve the original language only for short fragments.
- Always mention source and context.

## Language Handling

- If the user writes in Chinese, answer in Chinese.
- If the user writes in English, answer in English.
- For other languages, use the model's translation ability to translate the request into a retrieval language, then translate the final answer back.
- If the strongest evidence is German or English while the user is using Chinese, summarize in Chinese and cite the original-language source.

## Local Corpus Inputs

- Public repository contents are intentionally limited to code, templates, and public reference seeds.
- Private books, processed indices, and local file paths stay outside the public repo.
- The setup template lives at `references/private_books.template.json`.
- Public reference seeds live at `references/public_sources.json`.

## Citation Format

Use plain footnote-style lines:

```text
[1] Ian Kershaw, Hitler 1889-1936: Hubris, chapter title
[2] Peter Longerich, Hitler: A Biography, chapter title
```

If there is a page range from the corpus, include it.

## Style

- Keep the tone analytic, precise, and restrained.
- Preserve some period flavor through phrasing, but keep the answer clearly framed as reconstruction.
- Prefer historians with stronger evidentiary grounding when sources conflict.
- English originals outrank translations as fact anchors; Chinese editions can improve Chinese wording.
