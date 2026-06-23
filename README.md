# LLM Wiki Upgrader

Local-first tools for turning rough LLM notes into a cleaner, reviewable wiki structure.

This project is for working professionals and AI-assisted builders who collect useful LLM notes, prompts, commands, and workflows but need a safer way to publish or maintain them.

## Features

- Convert loose Markdown notes into a standard wiki page format
- Add consistent sections: Summary, Use Cases, Workflow, Review Checklist, Risks
- Extract action items into a maintainer checklist
- Detect missing source notes and weak review language
- Run locally with no network calls or external dependencies

## Usage

```bash
python3 -m llm_wiki_upgrader upgrade examples/raw-note.md
python3 -m llm_wiki_upgrader checklist examples/raw-note.md
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

## License

MIT
