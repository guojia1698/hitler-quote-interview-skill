import json
import tempfile
import unittest
from pathlib import Path

from tests._skill_bootstrap import SKILL_ROOT  # noqa: F401


class BuildIndexTests(unittest.TestCase):
    def test_build_index_creates_chunks_works_and_cross_language_links(self) -> None:
        from scripts.hqi.index import build_index

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            processed_dir = root / "processed"
            processed_dir.mkdir(parents=True, exist_ok=True)

            manifest = [
                {
                    "book_id": "toland-en",
                    "work_id": "toland-definitive-biography",
                    "title": "Adolf Hitler: The Definitive Biography",
                    "author": "John Toland",
                    "language": "en",
                    "tier": "A",
                    "is_translation": False,
                    "ingest_status": "ok",
                    "confidence": "high",
                },
                {
                    "book_id": "toland-zh",
                    "work_id": "toland-definitive-biography",
                    "title": "希特勒传：从乞丐到元首",
                    "author": "John Toland",
                    "language": "zh",
                    "tier": "C",
                    "is_translation": True,
                    "ingest_status": "ok",
                    "confidence": "medium",
                },
            ]
            sections = [
                {
                    "book_id": "toland-en",
                    "work_id": "toland-definitive-biography",
                    "language": "en",
                    "chapter_id": "c1",
                    "chapter_title": "Rise",
                    "text": "Hitler built a movement through propaganda and political theater.",
                    "confidence": "high",
                    "tier": "A",
                },
                {
                    "book_id": "toland-zh",
                    "work_id": "toland-definitive-biography",
                    "language": "zh",
                    "chapter_id": "c1",
                    "chapter_title": "崛起",
                    "text": "希特勒通过宣传、仪式和戏剧化政治来塑造群众动员。",
                    "confidence": "medium",
                    "tier": "C",
                },
            ]
            (processed_dir / "books_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
            (processed_dir / "sections.jsonl").write_text(
                "\n".join(json.dumps(item, ensure_ascii=False) for item in sections),
                encoding="utf-8",
            )

            summary = build_index(processed_dir)

            chunks = [json.loads(line) for line in (processed_dir / "chunks.jsonl").read_text(encoding="utf-8").splitlines()]
            works_index = json.loads((processed_dir / "works_index.json").read_text(encoding="utf-8"))
            links = json.loads((processed_dir / "cross_language_links.json").read_text(encoding="utf-8"))

            self.assertEqual(summary["chunks_written"], 2)
            self.assertEqual(chunks[0]["route_family"], "biography")
            self.assertEqual(works_index["toland-definitive-biography"]["languages"], ["en", "zh"])
            self.assertEqual(links[0]["work_id"], "toland-definitive-biography")
            self.assertEqual(set(links[0]["languages"]), {"en", "zh"})


if __name__ == "__main__":
    unittest.main()
