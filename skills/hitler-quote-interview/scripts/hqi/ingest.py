from __future__ import annotations

import posixpath
import re
from pathlib import Path
from typing import Any
from xml.etree import ElementTree
from zipfile import ZipFile

from PyPDF2 import PdfReader

from .utils import (
    chunk_text,
    collapse_whitespace,
    ensure_dir,
    infer_period,
    infer_themes,
    read_json,
    strip_html,
    write_json,
    write_jsonl,
)


def ingest_books(config_path: Path, output_dir: Path) -> dict[str, int]:
    config = read_json(config_path)
    books = config.get("books", [])
    ensure_dir(output_dir)

    manifest_rows: list[dict[str, Any]] = []
    section_rows: list[dict[str, Any]] = []
    summary = {"books_processed": 0, "books_failed": 0, "sections_written": 0}

    for book in books:
        row = dict(book)
        source_path = Path(book["source_path"]).expanduser()
        row["source_path"] = str(source_path)
        row["source_name"] = source_path.name
        row["detected_title"] = None
        row["detected_author"] = None
        row["detected_language"] = None
        row["section_count"] = 0
        row["extracted_characters"] = 0
        row["page_count"] = None

        if not source_path.exists():
            row["ingest_status"] = "missing"
            row["confidence"] = "low"
            manifest_rows.append(row)
            summary["books_failed"] += 1
            continue

        try:
            file_format = str(book.get("format", source_path.suffix.lstrip("."))).lower()
            if file_format == "epub":
                metadata, sections = _parse_epub(source_path)
            elif file_format == "pdf":
                metadata, sections = _parse_pdf(source_path)
            else:
                raise ValueError(f"Unsupported format: {file_format}")
            row["detected_title"] = metadata.get("title")
            row["detected_author"] = metadata.get("author")
            row["detected_language"] = metadata.get("language")
            row["page_count"] = metadata.get("page_count")
            row["section_count"] = len(sections)
            row["extracted_characters"] = sum(len(item["text"]) for item in sections)
            row["ingest_status"] = "ok" if sections else "empty"
            row["confidence"] = metadata.get("confidence", "medium")
            manifest_rows.append(row)
            section_rows.extend(
                {
                    "book_id": row["book_id"],
                    "work_id": row.get("work_id"),
                    "title": row["title"],
                    "author": row["author"],
                    "language": row["language"],
                    "chapter_id": section["chapter_id"],
                    "chapter_title": section["chapter_title"],
                    "page_range_optional": section.get("page_range_optional"),
                    "text": section["text"],
                    "confidence": row["confidence"],
                    "tier": row.get("tier", "B"),
                    "themes": infer_themes(section["text"], section["chapter_title"]),
                    "period": infer_period(section["text"], section["chapter_title"]),
                }
                for section in sections
            )
            summary["books_processed"] += 1
        except Exception as exc:  # pragma: no cover - exercised by integration usage
            row["ingest_status"] = "error"
            row["confidence"] = "low"
            row["error"] = str(exc)
            manifest_rows.append(row)
            summary["books_failed"] += 1

    summary["sections_written"] = len(section_rows)
    write_json(output_dir / "books_manifest.json", manifest_rows)
    write_jsonl(output_dir / "sections.jsonl", section_rows)
    return summary


def _parse_epub(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    with ZipFile(path) as archive:
        opf_path = _find_opf_path(archive)
        opf_dir = posixpath.dirname(opf_path)
        package = ElementTree.fromstring(archive.read(opf_path))
        ns = {"opf": "http://www.idpf.org/2007/opf", "dc": "http://purl.org/dc/elements/1.1/"}

        title = _text_or_none(package.find(".//dc:title", ns))
        author = _text_or_none(package.find(".//dc:creator", ns))
        language = _text_or_none(package.find(".//dc:language", ns))

        manifest_map: dict[str, dict[str, str]] = {}
        for item in package.findall(".//opf:manifest/opf:item", ns):
            manifest_map[item.attrib["id"]] = {
                "href": posixpath.normpath(posixpath.join(opf_dir, item.attrib["href"])),
                "media_type": item.attrib.get("media-type", ""),
            }

        toc_labels = _parse_toc_labels(archive, manifest_map, package, ns)
        sections: list[dict[str, Any]] = []
        spine_items = package.findall(".//opf:spine/opf:itemref", ns)
        for chapter_idx, itemref in enumerate(spine_items, start=1):
            entry = manifest_map.get(itemref.attrib["idref"])
            if not entry or "html" not in entry["media_type"]:
                continue
            html = archive.read(entry["href"]).decode("utf-8", errors="ignore")
            chapter_title = _extract_heading(html) or toc_labels.get(entry["href"]) or f"Chapter {chapter_idx}"
            text = strip_html(html)
            if _should_skip_section(entry["href"], chapter_title, text):
                continue
            sections.append(
                {
                    "chapter_id": f"{Path(entry['href']).stem}-{chapter_idx}",
                    "chapter_title": chapter_title,
                    "text": text,
                }
            )
    confidence = "high" if sum(len(item["text"]) for item in sections) > 2000 else "medium"
    return {"title": title, "author": author, "language": language, "confidence": confidence}, sections


def _find_opf_path(archive: ZipFile) -> str:
    container = ElementTree.fromstring(archive.read("META-INF/container.xml"))
    namespace = {"c": "urn:oasis:names:tc:opendocument:xmlns:container"}
    rootfile = container.find(".//c:rootfile", namespace)
    if rootfile is None:
        raise ValueError("EPUB missing rootfile")
    return rootfile.attrib["full-path"]


def _parse_toc_labels(
    archive: ZipFile,
    manifest_map: dict[str, dict[str, str]],
    package: ElementTree.Element,
    ns: dict[str, str],
) -> dict[str, str]:
    labels: dict[str, str] = {}
    spine = package.find(".//opf:spine", ns)
    if spine is None:
        return labels
    toc_id = spine.attrib.get("toc")
    if not toc_id or toc_id not in manifest_map:
        return labels
    toc_path = manifest_map[toc_id]["href"]
    try:
        tree = ElementTree.fromstring(archive.read(toc_path))
    except Exception:
        return labels
    for point in tree.findall(".//{http://www.daisy.org/z3986/2005/ncx/}navPoint"):
        label = point.find(".//{http://www.daisy.org/z3986/2005/ncx/}text")
        content = point.find(".//{http://www.daisy.org/z3986/2005/ncx/}content")
        if label is None or content is None:
            continue
        src = content.attrib.get("src", "")
        href = posixpath.normpath(posixpath.join(posixpath.dirname(toc_path), src.split("#", 1)[0]))
        labels[href] = collapse_whitespace(label.text or "")
    return labels


def _extract_heading(html: str) -> str | None:
    for tag in ("h1", "h2", "title"):
        match = re.search(rf"<{tag}[^>]*>(.*?)</{tag}>", html, flags=re.I | re.S)
        if match:
            heading = strip_html(match.group(1))
            if heading:
                return heading
    return None


def _should_skip_section(href: str, chapter_title: str, text: str) -> bool:
    haystack = f"{href} {chapter_title}".lower()
    basename = Path(href).stem.lower()
    direct_noise_tokens = (
        "contents",
        "copyright",
        "title",
        "cover",
        "toc",
        "navigation",
        "endnotes",
        "notes",
        "bibliography",
        "acknowledg",
        "glossary",
        "references",
    )
    explicit_index_labels = {"index", "name index", "subject index"}
    if len(text) < 60:
        return True
    if any(token in haystack for token in direct_noise_tokens):
        return True
    if basename in explicit_index_labels or chapter_title.strip().lower() in explicit_index_labels:
        return True
    return False


def _parse_pdf(path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    reader = PdfReader(str(path))
    metadata = reader.metadata or {}
    title = getattr(metadata, "title", None) or metadata.get("/Title")
    author = getattr(metadata, "author", None) or metadata.get("/Author")
    sections: list[dict[str, Any]] = []
    pending_text: list[str] = []
    start_page = 1
    for index, page in enumerate(reader.pages, start=1):
        page_text = collapse_whitespace(page.extract_text() or "")
        if not page_text:
            continue
        if not pending_text:
            start_page = index
        pending_text.append(page_text)
        combined = " ".join(pending_text)
        if len(combined) >= 1200 or index == len(reader.pages):
            sections.append(
                {
                    "chapter_id": f"pages-{start_page}-{index}",
                    "chapter_title": f"Pages {start_page}-{index}",
                    "page_range_optional": f"{start_page}-{index}",
                    "text": combined,
                }
            )
            pending_text = []
    total_chars = sum(len(item["text"]) for item in sections)
    confidence = "medium" if total_chars >= 4000 else "low"
    return {
        "title": title,
        "author": author,
        "language": None,
        "page_count": len(reader.pages),
        "confidence": confidence,
    }, sections


def _text_or_none(element: ElementTree.Element | None) -> str | None:
    if element is None or element.text is None:
        return None
    text = collapse_whitespace(element.text)
    return text or None
