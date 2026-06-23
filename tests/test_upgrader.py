import unittest
from pathlib import Path

from llm_wiki_upgrader.upgrader import build_checklist, upgrade_note


class WikiUpgraderTest(unittest.TestCase):
    def test_upgrade_adds_required_sections(self) -> None:
        upgraded = upgrade_note(Path("examples/raw-note.md"))

        self.assertIn("## Summary", upgraded)
        self.assertIn("## Review Checklist", upgraded)
        self.assertIn("## Risks and Boundaries", upgraded)

    def test_checklist_mentions_privacy(self) -> None:
        checklist = build_checklist(Path("examples/raw-note.md"))

        self.assertIn("Privacy review", checklist)


if __name__ == "__main__":
    unittest.main()
