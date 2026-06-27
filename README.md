# LLM Wiki Upgrader

Local-first tools for turning rough LLM notes into a cleaner, reviewable wiki structure.

This project is for working professionals and AI-assisted builders who collect useful LLM notes, prompts, commands, and workflows but need a safer way to publish or maintain them.

## Features

- Convert loose Markdown notes into a standard wiki page format
- Add consistent sections: Summary, Use Cases, Workflow, Review Checklist, Risks
- Extract action items into a maintainer checklist
- Detect missing source notes and weak review language
- Review publication readiness with Markdown or JSON output
- Run locally with no network calls or external dependencies

## Usage

```bash
python3 -m llm_wiki_upgrader upgrade examples/raw-note.md
python3 -m llm_wiki_upgrader checklist examples/raw-note.md
python3 -m llm_wiki_upgrader publish-review examples/raw-note.md --format markdown
python3 -m llm_wiki_upgrader publish-review examples/raw-note.md --format json
```

## Wiki Style

The generated structure is intentionally simple:

```markdown
# Title

## Summary

## Use Cases

## Workflow

## Review Checklist

## Risks and Boundaries

## Source Notes
```

## Why This Exists

LLM output often starts as messy notes. Before those notes become a public wiki, team guide, or open-source documentation, they need structure, review boundaries, and clear risk language.

LLM Wiki Upgrader helps turn draft AI notes into something a maintainer can review.

## Publication Review

`publish-review` checks whether a wiki note has the review boundaries needed before publication:

- required wiki sections,
- source notes,
- privacy boundary language,
- copyright or license review language,
- claim review language,
- reusable publication checklist.

The command runs locally and does not upload note content.

## License

MIT
