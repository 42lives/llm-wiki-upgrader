from __future__ import annotations

import argparse
from pathlib import Path

from .upgrader import build_checklist, upgrade_note


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="llm-wiki-upgrader", description="Upgrade rough LLM notes into wiki pages.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    upgrade = subparsers.add_parser("upgrade", help="Upgrade a Markdown note.")
    upgrade.add_argument("path", type=Path)

    checklist = subparsers.add_parser("checklist", help="Generate a publication checklist.")
    checklist.add_argument("path", type=Path)

    args = parser.parse_args(argv)

    if args.command == "upgrade":
        print(upgrade_note(args.path))
        return 0

    if args.command == "checklist":
        print(build_checklist(args.path))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2
