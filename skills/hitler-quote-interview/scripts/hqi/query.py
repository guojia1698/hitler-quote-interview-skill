from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .utils import detect_language, extract_search_terms, read_json, read_jsonl


TIER_SCORE = {"A": 3.0, "B": 2.0, "C": 1.0, "D": 0.5}
CONFIDENCE_SCORE = {"high": 1.5, "medium": 0.75, "low": 0.25}
SUPPLEMENTARY_TOKENS = ("notes", "endnotes", "bibliography", "references", "acknowledg", "glossary", "index")
FOOTNOTE_PATTERN = re.compile(r"\b\d{1,3}\s*[.)]")
BIOGRAPHY_AUTHORS = {
    "ian kershaw",
    "peter longerich",
    "volker ullrich",
    "john toland",
    "joachim fest",
}
RHETORIC_AUTHORS = {"ian kershaw", "ron rosenbaum", "laurence rees"}


def query_corpus(question: str, processed_dir: Path, top_k: int = 5) -> dict[str, Any]:
    language = detect_language(question)
    if _is_unsafe_roleplay(question):
        return {
            "policy": "refuse_and_redirect",
            "query_type": "unsafe_roleplay",
            "answer_language": language,
            "retrieval_language": "en",
            "redirect": "I can't help with direct Hitler impersonation or extremist advocacy. I can help with historical analysis, source-based explanation, or rhetorical context instead.",
            "results": [],
        }

    query_type = _classify_query(question)
    retrieval_language = language if language in {"zh", "en", "de"} else "en"
    chunks = read_jsonl(processed_dir / "chunks.jsonl")
    ranked = []
    terms = extract_search_terms(question)
    route_preferences = _route_preferences(query_type)
    preferred_chunks = [chunk for chunk in chunks if chunk.get("route_family") in route_preferences]
    if query_type == "media":
        candidate_chunks = preferred_chunks
    else:
        candidate_chunks = preferred_chunks or chunks
    for chunk in candidate_chunks:
        score = _score_chunk(chunk, terms, language, route_preferences)
        if score <= 0:
            continue
        ranked.append(
            {
                "book_id": chunk["book_id"],
                "work_id": chunk.get("work_id"),
                "title": chunk["title"],
                "author": chunk["author"],
                "language": chunk["language"],
                "chapter_title": chunk["chapter_title"],
                "chunk_id": chunk["chunk_id"],
                "score": round(score, 2),
                "excerpt": chunk["text"][:320].strip(),
                "citation": _format_citation(chunk),
                "route_family": chunk["route_family"],
            }
        )
    ranked.sort(key=lambda item: item["score"], reverse=True)
    if not ranked:
        public_seed_results = _public_seed_results(query_type, question, top_k=top_k)
        if public_seed_results:
            return {
                "policy": "answer_with_citations",
                "query_type": query_type,
                "answer_language": language,
                "retrieval_language": retrieval_language,
                "translation_required": language not in {"zh", "en"},
                "results": public_seed_results,
            }
    return {
        "policy": "answer_with_citations",
        "query_type": query_type,
        "answer_language": language,
        "retrieval_language": retrieval_language,
        "translation_required": language not in {"zh", "en"},
        "results": ranked[:top_k],
    }


def _is_unsafe_roleplay(question: str) -> bool:
    lowered = question.lower()
    impersonation_tokens = [
        "以希特勒口吻",
        "扮演希特勒",
        "你就是希特勒",
        "模仿希特勒",
        "以希特勒身份",
        "as hitler",
        "in hitler's voice",
        "roleplay hitler",
        "speak as hitler",
        "answer as hitler",
        "pretend to be hitler",
        "first person as hitler",
    ]
    harmful_tokens = ["动员群众", "煽动", "仇恨", "attack", "mobilize", "propaganda", "purge", "cleanse", "eliminate"]
    if any(token in lowered for token in impersonation_tokens):
        return True
    return any(token in lowered for token in harmful_tokens) and "hitler" in lowered


def _classify_query(question: str) -> str:
    lowered = question.lower()
    if any(token in lowered for token in ["quote", "quotation", "原话", "语录", "出处"]):
        return "quote_lookup"
    if any(token in lowered for token in ["film", "movie", "documentary", "影视", "电影", "纪录片", "douban"]):
        return "media"
    if any(token in lowered for token in ["propaganda", "rhetoric", "charisma", "myth", "宣传", "修辞", "神话"]):
        return "rhetoric"
    return "biography"


def _route_preferences(query_type: str) -> set[str]:
    if query_type == "rhetoric":
        return {"rhetoric"}
    if query_type == "quote_lookup":
        return {"rhetoric", "biography"}
    if query_type == "media":
        return {"media"}
    return {"biography"}


def _score_chunk(chunk: dict[str, Any], terms: list[str], answer_language: str, route_preferences: set[str]) -> float:
    haystack = f"{chunk.get('normalized_text', '')} {chunk.get('title', '').lower()} {chunk.get('chapter_title', '').lower()}"
    overlap = sum(1 for term in terms if term and term in haystack)
    score = overlap * 4.0
    if chunk.get("route_family") in route_preferences:
        score += 2.5
    else:
        score -= 7.0
    score += TIER_SCORE.get(chunk.get("tier", "B"), 0.5)
    score += CONFIDENCE_SCORE.get(chunk.get("confidence", "medium"), 0.25)
    if answer_language == chunk.get("language"):
        score += 2.0
    elif answer_language == "zh" and chunk.get("is_translation"):
        score += 1.5
    elif answer_language == "en" and not chunk.get("is_translation"):
        score += 1.0
    chapter_title = (chunk.get("chapter_title") or "").lower()
    if any(token in chapter_title for token in SUPPLEMENTARY_TOKENS):
        score -= 6.0
    author = (chunk.get("author") or "").lower()
    if route_preferences == {"biography"} and author in BIOGRAPHY_AUTHORS:
        score += 2.0
    if "rhetoric" in route_preferences and chunk.get("route_family") == "rhetoric" and author in RHETORIC_AUTHORS:
        score += 1.25
    score -= _reference_noise_penalty(chunk.get("text", ""))
    if overlap == 0 and chunk.get("route_family") not in route_preferences:
        score -= 10
    return score


def _format_citation(chunk: dict[str, Any]) -> str:
    base = f"{chunk['author']}, {chunk['title']}"
    if chunk.get("chapter_title"):
        base = f"{base}, {chunk['chapter_title']}"
    if chunk.get("page_range_optional"):
        base = f"{base}, pp. {chunk['page_range_optional']}"
    return base


def _reference_noise_penalty(text: str) -> float:
    hits = len(FOOTNOTE_PATTERN.findall(text))
    if hits < 4:
        return 0.0
    return min(8.0, 1.5 + hits * 0.55)


def _public_seed_results(query_type: str, question: str, top_k: int) -> list[dict[str, Any]]:
    skill_root = Path(__file__).resolve().parents[2]
    seed_path = skill_root / "references" / "public_sources.json"
    if not seed_path.exists():
        return []
    seeds = read_json(seed_path)
    if query_type == "media":
        eligible = [seed for seed in seeds if seed.get("source_type") == "media-catalog"]
    else:
        eligible = [seed for seed in seeds if seed.get("source_type") != "media-catalog"]
    if not eligible:
        return []
    terms = extract_search_terms(question)
    scored = []
    for seed in eligible:
        haystack = " ".join(
            [
                str(seed.get("title", "")).lower(),
                str(seed.get("notes", "")).lower(),
                str(seed.get("source_type", "")).lower(),
            ]
        )
        overlap = sum(1 for term in terms if term in haystack)
        score = 3.0 + overlap * 2.0
        if seed.get("source_type") == "media-catalog":
            score += 2.0
        scored.append(
            {
                "book_id": seed["source_id"],
                "work_id": seed["source_id"],
                "title": seed["title"],
                "author": seed["source_type"],
                "language": seed.get("language"),
                "chapter_title": seed.get("notes", "")[:80],
                "chunk_id": seed["source_id"],
                "score": round(score, 2),
                "excerpt": seed.get("notes", ""),
                "citation": seed["source_url"],
                "route_family": "media" if seed.get("source_type") == "media-catalog" else "reference",
            }
        )
    scored.sort(key=lambda item: item["score"], reverse=True)
    return scored[:top_k]
