from __future__ import annotations

import argparse
from pathlib import Path

from .upgrader import batch_upgrade, build_checklist, build_publish_review, upgrade_note


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="llm-wiki-upgrader", description="Upgrade rough LLM notes into wiki pages.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upgrade = subparsers.add_parser("upgrade", help="Upgrade a Markdown note.")
    upgrade.add_argument("path", type=Path)

    checklist = subparsers.add_parser("checklist", help="Generate a publication checklist.")
    checklist.add_argument("path", type=Path)

    publish_review = subparsers.add_parser("publish-review", help="Review wiki publication readiness.")
    publish_review.add_argument("path", type=Path)
    publish_review.add_argument("--format", choices=["markdown", "json"], default="markdown")

    batch = subparsers.add_parser("batch-upgrade", help="Upgrade all Markdown notes in a folder.")
    batch.add_argument("path", type=Path)

    args = parser.parse_args(argv)

    if args.command == "upgrade":
        print(upgrade_note(args.path))
        return 0

    if args.command == "checklist":
        print(build_checklist(args.path))
        return 0

    if args.command == "publish-review":
        print(build_publish_review(args.path, args.format))
        return 0

    if args.command == "batch-upgrade":
        print(batch_upgrade(args.path))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
