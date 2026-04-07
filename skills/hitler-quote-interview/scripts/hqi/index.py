from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from .utils import chunk_text, infer_period, infer_themes, normalize_text, read_json, read_jsonl, write_json, write_jsonl


def build_index(processed_dir: Path, chunk_size: int = 1200) -> dict[str, int]:
    manifest = read_json(processed_dir / "books_manifest.json")
    sections = read_jsonl(processed_dir / "sections.jsonl")
    manifest_by_book = {row["book_id"]: row for row in manifest}

    chunks: list[dict[str, Any]] = []
    works: dict[str, dict[str, Any]] = {}
    work_languages: dict[str, set[str]] = defaultdict(set)
    work_books: dict[str, list[str]] = defaultdict(list)

    for section in sections:
        manifest_row = manifest_by_book.get(section["book_id"])
        if not manifest_row or manifest_row.get("ingest_status") != "ok":
            continue
        work_id = section.get("work_id") or manifest_row.get("work_id") or section["book_id"]
        work = works.setdefault(
            work_id,
            {
                "work_id": work_id,
                "primary_title": manifest_row["title"],
                "authors": [],
                "languages": [],
                "books": [],
                "tiers": [],
                "route_family": _route_family(manifest_row),
            },
        )
        if manifest_row["author"] not in work["authors"]:
            work["authors"].append(manifest_row["author"])
        if manifest_row["book_id"] not in work["books"]:
            work["books"].append(manifest_row["book_id"])
        if manifest_row.get("tier") and manifest_row["tier"] not in work["tiers"]:
            work["tiers"].append(manifest_row["tier"])
        work_languages[work_id].add(manifest_row["language"])
        work_books[work_id].append(manifest_row["book_id"])

        section_chunks = chunk_text(section["text"], max_chars=chunk_size)
        for index, chunk in enumerate(section_chunks, start=1):
            chunks.append(
                {
                    "book_id": section["book_id"],
                    "work_id": work_id,
                    "title": manifest_row["title"],
                    "author": manifest_row["author"],
                    "language": manifest_row["language"],
                    "route_family": _route_family(manifest_row),
                    "tier": manifest_row.get("tier", "B"),
                    "is_translation": bool(manifest_row.get("is_translation")),
                    "chapter_id": section["chapter_id"],
                    "chapter_title": section["chapter_title"],
                    "page_range_optional": section.get("page_range_optional"),
                    "chunk_id": f"{section['book_id']}:{section['chapter_id']}:{index}",
                    "text": chunk,
                    "normalized_text": normalize_text(chunk),
                    "themes": section.get("themes") or infer_themes(chunk, section["chapter_title"]),
                    "period": section.get("period") or infer_period(chunk, section["chapter_title"]),
                    "confidence": section.get("confidence", manifest_row.get("confidence", "medium")),
                }
            )

    for work_id, languages in work_languages.items():
        works[work_id]["languages"] = sorted(languages)

    cross_language_links = [
        {
            "work_id": work_id,
            "languages": sorted(languages),
            "book_ids": sorted(set(work_books[work_id])),
        }
        for work_id, languages in work_languages.items()
        if len(languages) > 1
    ]

    write_jsonl(processed_dir / "chunks.jsonl", chunks)
    write_json(processed_dir / "works_index.json", works)
    write_json(processed_dir / "cross_language_links.json", cross_language_links)
    return {"chunks_written": len(chunks), "works_indexed": len(works), "links_written": len(cross_language_links)}


def _route_family(manifest_row: dict[str, Any]) -> str:
    if manifest_row.get("route_family"):
        return manifest_row["route_family"]
    title = manifest_row.get("title", "").lower()
    if any(token in title for token in ("myth", "explaining", "charisma", "propaganda")):
        return "rhetoric"
    if any(token in title for token in ("film", "movie", "documentary")):
        return "media"
    return "biography"
