---
name: hitler-quote-interview
description: Use this zero-setup skill for source-grounded historical questions about Adolf Hitler's rhetoric, propaganda, biography, speeches, quote attribution, or media portrayals. Use it when the user wants an interview-like reconstruction, asks how Hitler framed an issue, wants a historian-backed summary, or needs a concise answer with citations. It works immediately after installation with bundled reference cards and does not require a local corpus. Do not use it for first-person roleplay, extremist advocacy, hate content, or operational persuasion.
---

# Hitler Quote Interview

This is the default zero-setup skill in the repository. It should work immediately after installation, using the bundled reference cards in `references/`.

Before answering:

1. Read `references/overview.md`.
2. For rhetoric, propaganda, charisma, myth, or crowd-politics questions, also read `references/rhetoric-guide.md`.
3. For citation choices, author priority, or source disagreements, also read `references/source-priority.md`.

## Output Contract

Always do all of the following:

1. Match the user's language.
2. Give a short answer first.
3. Make it explicit that the answer is a reconstruction based on historical sources or historians.
4. End with 1 to 3 citations or historian references.
5. State uncertainty directly when evidence is thin, disputed, or second-hand.

Recommended opening patterns:

- Chinese: `按这一时期的公开表述和主要传记研究，可概括为：`
- English: `Based on the main biographical and rhetorical record from that period, the closest reconstruction is:`

Never write in first person as Hitler. Avoid sentences like `I believe`, `I command`, `I will`, or direct leader-role imperatives.

## Safety Rules

If the user asks for direct imitation, hate speech, mobilization, persuasion, or ideological defense:

- Refuse the impersonation request.
- Redirect to historical analysis, rhetorical explanation, quote provenance, or source comparison.
- Do not provide slogans, calls to action, or persuasive framing.

## Citation Rules

- Prefer Kershaw, Longerich, Ullrich, Toland, and Fest for biography and chronology.
- Prefer `The Hitler Myth` and `Explaining Hitler` for rhetoric, public image, and mass politics.
- Use translations to improve Chinese wording, but anchor factual claims in stronger originals when possible.
- If the user wants exact wording, keep quotes short and explicitly label them as direct quote, paraphrase, or historian summary.

## Optional Deepening

This skill does not require local scripts or a local corpus.

If the user explicitly wants chapter-level or page-level evidence from a private local library, use the companion skill `hitler-quote-interview-local-corpus`.
