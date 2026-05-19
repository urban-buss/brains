---
name: python-conventions
description: "Shared Python style guide for every brain. Loadable as a skill so any agent can pull it on demand. Mirrors `instructions/python.instructions.md`."
---

# Python conventions (shared across brains)

The authoritative copy of these rules lives in [`.github/instructions/python.instructions.md`](../../instructions/python.instructions.md) and is auto-applied to every `*.py` file in the workspace via `applyTo: "**/*.py"`.

Load this skill when you need the full style guide explicitly (e.g. when reviewing a new brain's first commit, or when asked "what's our Python style?").

## TL;DR

- `from __future__ import annotations` everywhere.
- `str | None`, `list`, `dict`, `tuple` — built-in generics, no `Optional`/`List`/`Dict`.
- `snake_case` for functions; `PascalCase` for classes; `_leading_underscore` for private.
- Parsers raise `ValueError` for required, return `None` for optional.
- No defensive code for impossible cases.
- Path traversal: `Path.is_relative_to()`. SQL: reject `INSERT/UPDATE/DELETE/DROP/CREATE/ALTER/TRUNCATE` if user-provided. HTTP: always set timeout.
- Tests next to every change. `tmp_path` for I/O. `pytest.raises` for failures.
- `ruff check` + `ruff format --check` is the gate.

## Submodule overrides

Each submodule may add project-specific rules in its own `.github/copilot-instructions.md`. On conflict, the submodule rule wins (it knows its domain better than the shared baseline).

## Note on duplication

The submodule-level style sections (in `cellarbrain/.github/copilot-instructions.md` and `recipebrain/.github/copilot-instructions.md`) currently restate most of the same rules. That duplication is intentional for now — submodules must remain standalone, since they're consumed individually as PyPI packages. The parent baseline is a *reference*, not a replacement. A `tools/sync-skills.py`-style mirror could be added later if drift becomes a real problem.
