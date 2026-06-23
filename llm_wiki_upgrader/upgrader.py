from __future__ import annotations

from pathlib import Path

SECTION_TITLES = [
    "Summary",
    "Use Cases",
    "Workflow",
    "Review Checklist",
    "Risks and Boundaries",
    "Source Notes",
]


def upgrade_note(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore").strip()
    title = _title_from(text, path)
    body = _strip_title(text)
    bullets = _extract_bullets(body)

    lines = [
        f"# {title}",
        "",
        "## Summary",
        "",
        _first_paragraph(body) or "Summarize the note before publishing.",
        "",
        "## Use Cases",
        "",
        *_section_items(bullets[:3], fallback="- Add concrete use cases."),
        "",
        "## Workflow",
        "",
        *_section_items(bullets[3:6], fallback="- Convert the rough note into reviewed steps."),
        "",
        "## Review Checklist",
        "",
        "- Confirm claims are sourced or marked as assumptions.",
        "- Remove private data, secrets, and account-specific details.",
        "- Verify instructions before publishing.",
        "",
        "## Risks and Boundaries",
        "",
        "- Do not present LLM output as verified fact without review.",
        "- Do not copy copyrighted source text into the wiki.",
        "- Keep private workflow details out of public examples.",
        "",
        "## Source Notes",
        "",
        "```text",
        body or "(empty)",
        "```",
    ]
    return "\n".join(lines).rstrip() + "\n"


def build_checklist(path: Path) -> str:
    upgraded = upgrade_note(path)
    missing = [title for title in SECTION_TITLES if f"## {title}" not in upgraded]
    lines = ["# Wiki Review Checklist", "", "- Structure: " + ("complete" if not missing else "missing " + ", ".join(missing))]
    lines.extend(
        [
            "- Source review: confirm borrowed material is summarized, not copied.",
            "- Privacy review: remove personal data, secrets, and private account details.",
            "- Actionability review: each workflow step should be testable or reviewable.",
            "- Publication review: add license/source notes before sharing publicly.",
        ]
    )
    return "\n".join(lines) + "\n"


def _title_from(text: str, path: Path) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def _strip_title(text: str) -> str:
    lines = text.splitlines()
    if lines and lines[0].startswith("# "):
        return "\n".join(lines[1:]).strip()
    return text


def _extract_bullets(text: str) -> list[str]:
    bullets = []
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            bullets.append("- " + stripped[2:].strip())
    return bullets


def _first_paragraph(text: str) -> str:
    for block in text.split("\n\n"):
        cleaned = " ".join(line.strip() for line in block.splitlines() if line.strip() and not line.strip().startswith(("-", "*", "#")))
        if cleaned:
            return cleaned
    return ""


def _section_items(items: list[str], fallback: str) -> list[str]:
    return items if items else [fallback]
