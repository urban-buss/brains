# Brains — Agents Index

This file lists the **parent-level** agents that coordinate work across both brains. For each brain's own specialists, see the submodule's `.github/AGENTS.md`.

## Parent-level (this repo)

| Agent | Purpose | Tools |
|-------|---------|-------|
| **brains-coordinator** | Plans and routes cross-brain work; dispatches to submodule agents. | `read`, `search`, `execute`, `todo` |
| **brains-devsetup** | Bootstraps a fresh clone: submodules, venvs, editable installs, test suites. | `execute`, `read`, `search`, `todo` |
| **brains-explorer** | Read-only Q&A across both codebases plus parent docs. | `read`, `search`, `todo` |
| **brains-release** | Cascades coordinated releases and the combined parent pointer-bump commit. | `execute`, `read`, `search`, `todo` |

## Per-brain (in submodules)

| Submodule | Catalogue |
|-----------|-----------|
| cellarbrain | [`cellarbrain/.github/AGENTS.md`](../cellarbrain/.github/AGENTS.md) — devsetup, smoketest, qa, research, market, price-tracker, shopscanner, shopresearch, search-tester, explorer, trainer, tracked, the `cellarbrain` sommelier itself. |
| recipebrain | [`recipebrain/.github/agents/`](../recipebrain/.github/agents/) — recipe & promotion specialists (catalogue forthcoming). |

## Prompts at parent level

| Prompt | Use it for |
|--------|------------|
| `status.prompt.md` | Compact health report across parent + every submodule. |
| `commit.prompt.md` | Parent-flavoured conventional commits. |
| `pointer-bump.prompt.md` | Compose a clean pointer-bump commit with the inbound commit range. |
| `submodule-update.prompt.md` | Pull each submodule's tracked branch tip with full safety checks. |
| `submodule-sync.prompt.md` | Catch up after pulling parent changes that move pointers. |
| `cross-brain.prompt.md` | Plan/implement a feature that spans both brains via MCP. |
| `release-all.prompt.md` | Cascade a coordinated release. |
| `new-brain.prompt.md` | Scaffold a new `<x>brain` submodule from the recipebrain template. |
| `commit.prompt.md` | Conventional commits, parent-flavoured. |
| `dream.prompt.md` | Consolidate cross-brain `.memories/` into permanent rules. |

## Instructions at parent level

| File | Scope | Purpose |
|------|-------|---------|
| `copilot-instructions.md` | `**` | Workspace overview, dual-commit dance, memory system. |
| `instructions/submodule-workflow.instructions.md` | `**` | Hard rules for submodule safety. |
| `instructions/python.instructions.md` | `**/*.py` | Shared Python baseline (style, typing, imports, docstrings). |
| `instructions/memory-management.instructions.md` | `.memories/**` | Memory file conventions (mirrors per-submodule rules). |

## Skills at parent level

| Skill | Purpose |
|-------|---------|
| `skills/submodule-management/` | Safe Git workflows for the submodule layer. |
| `skills/mcp-interop/` | How cellarbrain ↔ recipebrain compose at runtime via MCP. |
| `skills/python-conventions/` | Shared Python style guide; loadable on demand. |

## Tools at parent level

| Tool | Purpose |
|------|---------|
| `tools/foreach.py` | Run a command in every submodule (and optionally the parent). |
| `tools/check-submodule-pointers.py` | Verify every pointer is reachable on origin. |
| `tools/snapshot-versions.py` | Manifest of `{submodule: version, commit, branch}`. |
