from __future__ import annotations

import json
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


def build_publish_review(path: Path, output_format: str = "markdown") -> str:
    upgraded = upgrade_note(path)
    findings = review_publication_readiness(upgraded)
    summary = {
        "status": "ready" if not findings else "needs review",
        "findings": len(findings),
        "sections": len([title for title in SECTION_TITLES if f"## {title}" in upgraded]),
    }
    report = {
        "summary": summary,
        "findings": findings,
        "checklist": [
            "Confirm every claim is sourced, tested, or marked as an assumption.",
            "Remove private names, emails, account IDs, tokens, and private workflow details.",
            "Replace copied source text with summaries unless redistribution is allowed.",
            "Keep risks and boundaries visible before publishing.",
            "Add source notes and license context for public wiki pages.",
        ],
        "privacy_boundary": "This review runs locally and does not upload note content.",
    }
    if output_format == "json":
        return json.dumps(report, indent=2, ensure_ascii=False) + "\n"
    return render_publish_review_markdown(report)


def batch_upgrade(path: Path) -> str:
    root = path.expanduser().resolve()
    files = sorted(root.glob("*.md")) if root.is_dir() else [root]
    lines = ["# Batch Wiki Upgrade", "", f"Source: `{root}`", "", f"Files: {len(files)}", ""]
    for file_path in files:
        upgraded = upgrade_note(file_path)
        lines.extend([f"## {file_path.name}", "", upgraded.rstrip(), ""])
    if not files:
        lines.append("No Markdown files found.")
    return "\n".join(lines).rstrip() + "\n"


def review_publication_readiness(text: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    lower = text.lower()
    for title in SECTION_TITLES:
        if f"## {title}" not in text:
            findings.append({"severity": "medium", "message": f"Missing section: {title}"})
    if "source notes" not in lower:
        findings.append({"severity": "medium", "message": "Missing source notes section"})
    if "private" not in lower and "privacy" not in lower:
        findings.append({"severity": "medium", "message": "Missing privacy boundary language"})
    if "copyright" not in lower and "license" not in lower:
        findings.append({"severity": "low", "message": "Missing copyright or license review language"})
    if "assumption" not in lower and "verified" not in lower and "review" not in lower:
        findings.append({"severity": "low", "message": "Missing claim review boundary language"})
    return findings


def render_publish_review_markdown(report: dict[str, object]) -> str:
    summary = report["summary"]
    lines = [
        "# Wiki Publication Review",
        "",
        f"Status: {summary['status']}",
        f"Findings: {summary['findings']}",
        f"Sections present: {summary['sections']}/{len(SECTION_TITLES)}",
        "",
        "## Findings",
        "",
    ]
    findings = report["findings"]
    if not findings:
        lines.append("No publication readiness findings.")
    for finding in findings:
        lines.append(f"- [{finding['severity']}] {finding['message']}")
    lines.extend(["", "## Checklist", ""])
    for item in report["checklist"]:
        lines.append(f"- [ ] {item}")
    lines.extend(["", "## Privacy Boundary", "", str(report["privacy_boundary"])])
    return "\n".join(lines).rstrip() + "\n"


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
