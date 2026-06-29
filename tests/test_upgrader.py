import unittest
from pathlib import Path

from llm_wiki_upgrader.upgrader import batch_upgrade, build_checklist, build_publish_review, upgrade_note


class WikiUpgraderTest(unittest.TestCase):
    def test_upgrade_adds_required_sections(self) -> None:
        upgraded = upgrade_note(Path("examples/raw-note.md"))

        self.assertIn("## Summary", upgraded)
        self.assertIn("## Review Checklist", upgraded)
        self.assertIn("## Risks and Boundaries", upgraded)

    def test_checklist_mentions_privacy(self) -> None:
        checklist = build_checklist(Path("examples/raw-note.md"))

        self.assertIn("Privacy review", checklist)

    def test_publish_review_outputs_status_and_checklist(self) -> None:
        markdown = build_publish_review(Path("examples/raw-note.md"))
        json_output = build_publish_review(Path("examples/raw-note.md"), "json")

        self.assertIn("# Wiki Publication Review", markdown)
        self.assertIn("Status:", markdown)
        self.assertIn("Checklist", markdown)
        self.assertIn('"privacy_boundary"', json_output)

    def test_batch_upgrade_combines_markdown_notes(self) -> None:
        batch = batch_upgrade(Path("examples"))

        self.assertIn("# Batch Wiki Upgrade", batch)
        self.assertIn("raw-note.md", batch)


if __name__ == "__main__":
    unittest.main()
