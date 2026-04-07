import json
import tempfile
import unittest
from pathlib import Path
from zipfile import ZipFile

from tests._skill_bootstrap import SKILL_ROOT  # noqa: F401


def build_minimal_epub(path: Path, title: str = "Sample Book", language: str = "en") -> None:
    container_xml = """<?xml version="1.0" encoding="UTF-8"?>
<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">
  <rootfiles>
    <rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
  </rootfiles>
</container>
"""
    content_opf = f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" version="2.0" unique-identifier="BookId">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:title>{title}</dc:title>
    <dc:creator>Example Author</dc:creator>
    <dc:language>{language}</dc:language>
  </metadata>
  <manifest>
    <item id="ncx" href="toc.ncx" media-type="application/x-dtbncx+xml"/>
    <item id="chapter1" href="chapter1.xhtml" media-type="application/xhtml+xml"/>
    <item id="chapter2" href="chapter2.xhtml" media-type="application/xhtml+xml"/>
  </manifest>
  <spine toc="ncx">
    <itemref idref="chapter1"/>
    <itemref idref="chapter2"/>
  </spine>
</package>
"""
    toc_ncx = """<?xml version="1.0" encoding="UTF-8"?>
<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">
  <navMap>
    <navPoint id="navpoint-1" playOrder="1">
      <navLabel><text>Chapter One</text></navLabel>
      <content src="chapter1.xhtml"/>
    </navPoint>
    <navPoint id="navpoint-2" playOrder="2">
      <navLabel><text>Chapter Two</text></navLabel>
      <content src="chapter2.xhtml"/>
    </navPoint>
  </navMap>
</ncx>
"""
    chapter1 = """<html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Chapter One</h1>
<p>Hitler used propaganda, spectacle, and repetition to shape mass politics.</p>
</body></html>"""
    chapter2 = """<html xmlns="http://www.w3.org/1999/xhtml"><body><h1>Chapter Two</h1>
<p>Biographers compare how different historians describe his rise to power.</p>
</body></html>"""
    with ZipFile(path, "w") as epub:
        epub.writestr("mimetype", "application/epub+zip")
        epub.writestr("META-INF/container.xml", container_xml)
        epub.writestr("OEBPS/content.opf", content_opf)
        epub.writestr("OEBPS/toc.ncx", toc_ncx)
        epub.writestr("OEBPS/chapter1.xhtml", chapter1)
        epub.writestr("OEBPS/chapter2.xhtml", chapter2)


class IngestBooksTests(unittest.TestCase):
    def test_ingest_books_writes_manifest_and_sections_for_epub(self) -> None:
        from scripts.hqi.ingest import ingest_books

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source_epub = root / "sample.epub"
            build_minimal_epub(source_epub)

            config_path = root / "books.json"
            config_path.write_text(
                json.dumps(
                    {
                        "books": [
                            {
                                "book_id": "sample-book",
                                "work_id": "sample-work",
                                "title": "Sample Book",
                                "author": "Example Author",
                                "language": "en",
                                "format": "epub",
                                "source_path": str(source_epub),
                                "tier": "A",
                            }
                        ]
                    },
                    ensure_ascii=False,
                    indent=2,
                ),
                encoding="utf-8",
            )

            output_dir = root / "processed"
            result = ingest_books(config_path, output_dir)

            manifest = json.loads((output_dir / "books_manifest.json").read_text(encoding="utf-8"))
            sections = [json.loads(line) for line in (output_dir / "sections.jsonl").read_text(encoding="utf-8").splitlines()]

            self.assertEqual(result["books_processed"], 1)
            self.assertEqual(manifest[0]["book_id"], "sample-book")
            self.assertEqual(manifest[0]["ingest_status"], "ok")
            self.assertEqual(manifest[0]["detected_title"], "Sample Book")
            self.assertEqual(len(sections), 2)
            self.assertEqual(sections[0]["chapter_title"], "Chapter One")
            self.assertIn("propaganda", sections[0]["text"].lower())

    def test_ingest_books_marks_missing_source_as_failed(self) -> None:
        from scripts.hqi.ingest import ingest_books

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            config_path = root / "books.json"
            config_path.write_text(
                json.dumps(
                    {
                        "books": [
                            {
                                "book_id": "missing-book",
                                "work_id": "missing-work",
                                "title": "Missing Book",
                                "author": "Unknown",
                                "language": "en",
                                "format": "epub",
                                "source_path": str(root / "missing.epub"),
                                "tier": "A",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )

            output_dir = root / "processed"
            result = ingest_books(config_path, output_dir)
            manifest = json.loads((output_dir / "books_manifest.json").read_text(encoding="utf-8"))

            self.assertEqual(result["books_failed"], 1)
            self.assertEqual(manifest[0]["ingest_status"], "missing")
            self.assertEqual(manifest[0]["confidence"], "low")

    def test_index_split_href_is_not_treated_as_noise(self) -> None:
        from scripts.hqi.ingest import _should_skip_section

        should_skip = _should_skip_section(
            "OEBPS/index_split_005-7.xhtml",
            "Chapter One",
            "This chapter describes Hitler's rise and political movement in prose form.",
        )

        self.assertFalse(should_skip)


if __name__ == "__main__":
    unittest.main()
