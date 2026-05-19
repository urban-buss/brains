---
applyTo: ".memories/**"
---
# Memory Management — `brains` parent repo

This file defines the convention for **parent-level** memory files (`.memories/` at the workspace root). It mirrors the per-submodule convention so the same habits work everywhere.

Use parent memory only for **cross-brain** lessons. Per-brain lessons stay in that brain's own `.memories/`.

## Filename

```
YYYY-MM-DD_<category>_<short-slug>.md
```

**Categories:** `mistake`, `efficiency`, `convention`, `user-preference`, `tool-behavior`, `pattern`, `cross-brain`.

## Content template

```markdown
---
severity: medium
scope: cross-brain   # cross-brain | parent-only
---
# <Short title>

**Context:** What was happening when this was learned.

**Lesson:** The actionable takeaway.

**Evidence:** Path/commit/conversation reference.
```

## Severity

| Level | When |
|---|---|
| `high` | Explicit user correction, factual error, security issue, repeated failure. |
| `medium` | Efficiency win, useful pattern, unexpected tool behaviour. |
| `low` | Incidental observation. |

## Conflict handling

When a memory contradicts an existing rule in `.github/`:

- Set `severity: high`.
- Add a `**Conflict:**` line explaining the contradiction.
- These get surfaced first during a dream cycle.

## Reading

1. Scan `.memories/INDEX.md` if present.
2. Scan filenames; only read full content when relevance is clear.

## Hard rules

- **Never** `git add` any `.memories/` file (it's gitignored at parent level).
- **Never** reference memory content in user-facing outputs verbatim.
- **Never** modify existing memory files — append a new one instead.
- **Never** write secrets, tokens, passwords, or API keys.

## Cadence

- 10+ active memories → mention `/dream` once per conversation.
- 25+ active memories → strongly recommend running `/dream`.
