---
applyTo: "**"
---
# Brains — Copilot Workspace Instructions

## Project Overview

`brains` is a **parent aggregator repository**. It contains no application source code of its own — only Git submodules, shared coordinator tooling under `.github/`, and project-wide docs.

Each "brain" is a standalone Python project (CLI + MCP server, Python 3.11+, MIT license) living in its own submodule with its own `.github/`, `pyproject.toml`, tests, and release cadence.

| Submodule | Path | Purpose |
|-----------|------|---------|
| `cellarbrain` | `cellarbrain/` | Swiss wine-cellar manager (Vinocell CSV → Parquet + dossiers + MCP) |
| `recipebrain` | `recipebrain/` | Swiss recipe scraper + meal-planner (recipes + promotions + MCP) |

Cellarbrain and recipebrain compose at **runtime** via the MCP host — there is no Python-level coupling between them.

## Where work happens

**Almost all source-code work happens inside a submodule, not at the parent level.** When the user asks for a code change, infer which brain it belongs to and `cd` into that submodule. Use the submodule's own `.github/` (copilot-instructions, prompts, agents, skills) for project-specific guidance.

The parent repo's job is limited to:

- Tracking submodule pointers (commits) in `.gitmodules` + the tree.
- Coordinator workflows: dev setup, status, releases, cross-brain features.
- Shared docs and policies (this folder).

If you find yourself editing source files outside a submodule, stop and re-evaluate — it's almost always wrong.

## The dual-commit dance

When you change code inside a submodule, **two commits** are needed:

1. **Inside the submodule** — `cd <submodule> && git add ... && git commit`. This commit lives in the submodule's history.
2. **In the parent** — `cd .. && git add <submodule> && git commit -m "chore(<submodule>): bump to <short-sha>"`. This commit updates the parent's recorded pointer.

Skipping step 2 leaves the parent referencing the previous (now-stale) commit. Skipping step 1 stages a "dirty" submodule — never do this.

See [`instructions/submodule-workflow.instructions.md`](./instructions/submodule-workflow.instructions.md) for hard rules and `prompts/pointer-bump.prompt.md` for an automated helper.

## Pre-flight before bumping a pointer

A submodule pointer in the parent **must** reference a commit reachable from the submodule's `origin`. Otherwise collaborators (and CI) cannot fetch it.

Before committing a pointer bump:

```powershell
cd <submodule>
git fetch origin
git branch --contains HEAD --remote
# expect at least one origin/* branch
```

The helper `python .github/tools/check-submodule-pointers.py` automates this for every submodule.

## Pushing

- `git push` inside a submodule pushes to the submodule's own origin — fine when the submodule branch is intended for sharing (e.g. `main`).
- `git push` in the parent only pushes the parent. Use `--recurse-submodules=check` to be warned if a referenced submodule commit is missing on its remote.
- **Never** force-push either repo without explicit user confirmation.

## Cross-brain features (MCP interop)

When a feature spans both brains, it almost always runs through an MCP tool exposed by one brain and consumed by the other (canonical example: recipebrain's `cellar_pairing` calling cellarbrain). Use `prompts/cross-brain.prompt.md` to plan the work and the `skills/mcp-interop/` skill for the integration patterns.

## Coding Conventions

Per-submodule conventions live in each submodule's `.github/copilot-instructions.md`. The shared Python baseline is in [`instructions/python.instructions.md`](./instructions/python.instructions.md) — it applies workspace-wide. Submodule rules take precedence on conflict.

## Testing

Every brain has its own `tests/`. Run `pytest` inside the submodule. Use `python .github/tools/foreach.py -- pytest -q` from the parent to run all suites.

Never invent or skip tests as a workaround.

## Memory System

The workspace has a self-learning memory system for **cross-brain** lessons (`/memories/repo/` for repo-scoped facts, plus `.memories/` if adopted at parent level). Per-brain lessons stay in the submodule's own memory. See [`instructions/memory-management.instructions.md`](./instructions/memory-management.instructions.md).

### Git Safety

- **Never** commit `.memories/`. It's listed in `.gitignore` at parent level.
- Never write secrets/tokens to memory files.

## Common Tasks

### Bring a fresh clone up
```powershell
git submodule update --init --recursive
python .github/tools/foreach.py -- pip install -e ".[dev]"
python .github/tools/foreach.py -- pytest -q
```

### Update submodules to their tracked branch tips
```powershell
git submodule update --remote --merge
python .github/tools/check-submodule-pointers.py
# review the pointer-bump diff, then:
git add cellarbrain recipebrain
git commit -m "chore(submodules): bump to latest tracked branch"
```
See `prompts/submodule-update.prompt.md` for the guided flow.

### See state across all repos
```powershell
python .github/tools/foreach.py --include-parent -- git status -sb
```
Or use `prompts/status.prompt.md`.

### Add a new brain
Use `prompts/new-brain.prompt.md` — scaffolds a new submodule from the recipebrain template (Python + DuckDB/Parquet + MCP + dossiers).

## Prompts and agents

See [`AGENTS.md`](./AGENTS.md) for the index of parent-level agents and pointers into each submodule's agent catalogue.
