import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class SkillMatrixTests(unittest.TestCase):
    def test_repo_exposes_three_installable_skills(self) -> None:
        expected = [
            REPO_ROOT / "skills" / "hitler-quote-interview" / "SKILL.md",
            REPO_ROOT / "skills" / "hitler-quote-interview-source-attribution" / "SKILL.md",
            REPO_ROOT / "skills" / "hitler-quote-interview-local-corpus" / "SKILL.md",
        ]

        for path in expected:
            self.assertTrue(path.exists(), f"missing skill file: {path}")

    def test_default_skill_is_zero_setup(self) -> None:
        skill_text = (REPO_ROOT / "skills" / "hitler-quote-interview" / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("zero-setup", skill_text)
        self.assertIn("does not require a local corpus", skill_text)
        self.assertIn("references/dialogue-mode.md", skill_text)
        self.assertIn("Reconstructed answer:", skill_text)
        self.assertIn("复原回答：", skill_text)
        self.assertNotIn("Run the query helper first", skill_text)

    def test_default_skill_ships_dialogue_references(self) -> None:
        reference_dir = REPO_ROOT / "skills" / "hitler-quote-interview" / "references"
        dialogue_reference = reference_dir / "dialogue-mode.md"

        self.assertTrue((reference_dir / "overview.md").exists())
        self.assertTrue(dialogue_reference.exists())
        self.assertTrue((reference_dir / "rhetoric-guide.md").exists())
        self.assertTrue((reference_dir / "source-priority.md").exists())
        dialogue_text = dialogue_reference.read_text(encoding="utf-8")
        self.assertIn("conversation, not a briefing memo", dialogue_text)
        self.assertIn("复原回答：", dialogue_text)

    def test_local_corpus_skill_keeps_self_contained_scripts_and_references(self) -> None:
        skill_root = REPO_ROOT / "skills" / "hitler-quote-interview-local-corpus"

        self.assertTrue((skill_root / "scripts" / "query_corpus.py").exists())
        self.assertTrue((skill_root / "scripts" / "build_index.py").exists())
        self.assertTrue((skill_root / "scripts" / "ingest_books.py").exists())
        self.assertTrue((skill_root / "references" / "private_books.template.json").exists())
        self.assertTrue((skill_root / "references" / "setup-private-corpus.md").exists())


if __name__ == "__main__":
    unittest.main()
