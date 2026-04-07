from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Iterable


CJK_RE = re.compile(r"[\u3400-\u9fff]")
WORD_RE = re.compile(r"[a-z0-9']+")
WHITESPACE_RE = re.compile(r"\s+")
TAG_RE = re.compile(r"<[^>]+>")
BLOCK_TAG_RE = re.compile(r"</?(?:p|div|section|article|li|ul|ol|h1|h2|h3|h4|h5|h6|blockquote|br|tr|table)[^>]*>", re.I)

GERMAN_HINTS = {
    "und",
    "der",
    "die",
    "das",
    "ein",
    "eine",
    "nicht",
    "mit",
    "von",
    "auf",
    "für",
}

EN_STOPWORDS = {
    "the",
    "and",
    "with",
    "that",
    "this",
    "from",
    "into",
    "about",
    "what",
    "when",
    "where",
    "would",
    "could",
    "should",
    "their",
    "there",
    "them",
    "they",
    "have",
    "how",
}


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def read_json(path: Path) -> object:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: object) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8").strip()
    if not text:
        return []
    return [json.loads(line) for line in text.splitlines()]


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    ensure_dir(path.parent)
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows), encoding="utf-8")


def collapse_whitespace(text: str) -> str:
    return WHITESPACE_RE.sub(" ", text).strip()


def normalize_text(text: str) -> str:
    lowered = text.lower()
    lowered = re.sub(r"[^\w\s\u3400-\u9fff]", " ", lowered)
    return collapse_whitespace(lowered)


def detect_language(text: str) -> str:
    if CJK_RE.search(text):
        return "zh"
    lowered = text.lower()
    german_hits = sum(1 for token in WORD_RE.findall(lowered) if token in GERMAN_HINTS)
    if any(ch in lowered for ch in "äöüß") or german_hits >= 2:
        return "de"
    return "en"


def extract_search_terms(text: str) -> list[str]:
    lowered = normalize_text(text)
    terms = []
    if CJK_RE.search(lowered):
        cjk_sequences = re.findall(r"[\u3400-\u9fff]{2,}", lowered)
        for seq in cjk_sequences:
            if len(seq) <= 4:
                terms.append(seq)
            else:
                for idx in range(0, len(seq) - 1):
                    terms.append(seq[idx : idx + 2])
    for word in WORD_RE.findall(lowered):
        if len(word) < 3 or word in EN_STOPWORDS:
            continue
        terms.append(word)
    deduped = []
    seen = set()
    for term in terms:
        if term not in seen:
            seen.add(term)
            deduped.append(term)
    return deduped[:48]


def chunk_text(text: str, max_chars: int = 1200) -> list[str]:
    paragraphs = [collapse_whitespace(part) for part in re.split(r"\n{2,}", text) if collapse_whitespace(part)]
    if not paragraphs:
        paragraphs = [collapse_whitespace(text)]
    chunks: list[str] = []
    current = ""
    for paragraph in paragraphs:
        if not current:
            current = paragraph
            continue
        if len(current) + len(paragraph) + 2 <= max_chars:
            current = f"{current}\n\n{paragraph}"
        else:
            chunks.append(current)
            current = paragraph
    if current:
        chunks.append(current)
    if not chunks and text.strip():
        chunks = [collapse_whitespace(text)]
    return chunks


def strip_html(html: str) -> str:
    html = BLOCK_TAG_RE.sub("\n", html)
    html = TAG_RE.sub(" ", html)
    return collapse_whitespace(html.replace("\xa0", " "))


def infer_period(text: str, title: str) -> str:
    haystack = f"{title} {text}".lower()
    if any(token in haystack for token in ["beer hall", "putsch", "1919", "1920", "1921", "1923"]):
        return "1919-1923"
    if any(token in haystack for token in ["weimar", "1924", "1925", "1928", "1930", "1932"]):
        return "1924-1932"
    if any(token in haystack for token in ["1933", "1934", "1935", "1936", "1937", "1938", "1939"]):
        return "1933-1939"
    if any(token in haystack for token in ["war", "1940", "1941", "1942", "1943", "1944", "1945", "bunker"]):
        return "1939-1945"
    return "broad"


def infer_themes(text: str, title: str) -> list[str]:
    haystack = f"{title} {text}".lower()
    theme_map = {
        "propaganda": ["propaganda", "myth", "charisma", "image", "spectacle", "群众", "宣传"],
        "biography": ["biography", "rise", "fall", "career", "生活", "崛起", "传记"],
        "ideology": ["ideology", "antisemit", "race", "lebensraum", "worldview", "意识形态"],
        "war": ["war", "army", "military", "bunker", "front", "战争", "军"],
        "sources": ["document", "archive", "speech", "letter", "quote", "档案", "演讲", "语录"],
    }
    themes = [name for name, keywords in theme_map.items() if any(token in haystack for token in keywords)]
    return themes or ["general"]

