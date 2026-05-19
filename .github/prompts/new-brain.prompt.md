---
description: "Scaffold a new <x>brain submodule from the recipebrain template (Python + DuckDB/Parquet + MCP + dossiers). Use when: 'new brain', 'add brain', 'scaffold brain', 'create a new brain'."
argument-hint: "Name of the new brain (e.g. 'cookbrain', 'fitnessbrain'). Must end with 'brain'."
agent: agent
---

You are scaffolding a new "<name>brain" submodule that follows the same architecture as `cellarbrain` and `recipebrain`: Python 3.11+, DuckDB + Parquet, MCP server, per-entity Markdown dossiers, MIT license.

## 0. Pre-flight

- Working tree at parent level must be clean.
- Name must end with `brain` (e.g. `cookbrain`, `fitnessbrain`, `studybrain`).
- A remote repository must already exist (or be agreed) at e.g. `https://github.com/<owner>/<name>brain`. **Ask the user** for the remote URL before doing anything irreversible.

## 1. Confirm with the user

Before creating anything, confirm:

- Final brain name and remote URL.
- Whether to template from `recipebrain` (default, lightest scaffold) or `cellarbrain` (full ML/sommelier-style scaffold).
- Whether to add it now or open a tracking issue first.

## 2. Create the submodule

```powershell
git submodule add <remote-url> <name>brain
```

This creates `.gitmodules` entry + an empty (or existing) submodule directory.

## 3. Seed the project skeleton

Copy the **template brain's** structure as a starting point, then clear domain content:

| Keep verbatim | Adapt | Remove |
|---|---|---|
| `pyproject.toml` structure, `LICENSE`, `CHANGELOG.md` skeleton | Package name, CLI name, entry points, docs index | Domain-specific code, parsers, fixtures |
| `.github/copilot-instructions.md` structure, prompts, workflows | Project overview, knowledge-base table | Domain agents (price-tracker, shopscanner, etc.) |
| `tests/conftest.py` patterns | Sample fixtures | Real test data |
| `setup.py` (if present) | Path references | Domain entries |

Suggested source tree:

```
<name>brain/
├── pyproject.toml
├── README.md
├── LICENSE
├── CHANGELOG.md
├── <name>brain.toml          # main config
├── .github/
│   ├── copilot-instructions.md
│   ├── AGENTS.md
│   ├── workflows/{ci,publish}.yml
│   ├── instructions/
│   ├── prompts/
│   └── tools/sync-skills.py
├── docs/
│   ├── index.md
│   ├── 01-vision-and-usecases.md
│   ├── 02-requirements.md
│   ├── 03-data-sources.md
│   ├── 04-entity-model.md
│   ├── 05-mcp-tools.md
│   └── 06-architecture.md
├── src/<name>brain/
│   ├── __init__.py
│   ├── cli.py
│   ├── settings.py
│   ├── writer.py             # Parquet SCHEMAS
│   ├── query.py              # DuckDB read layer
│   ├── mcp_server.py
│   └── migrations/
└── tests/
    ├── conftest.py
    └── test_smoke.py
```

## 4. Wire CI / packaging

- Make sure `pyproject.toml` declares Python `>=3.11`, includes a `[dev]` extra, and exposes a CLI entry point (`[project.scripts] <name>brain = "<name>brain.cli:main"`).
- Copy the submodule's own `.github/workflows/ci.yml` (lint + matrix pytest).
- The parent's `.github/workflows/ci.yml` already discovers submodules via the matrix — add the new name to the matrix list.

## 5. First commits

Inside the new submodule:

1. Initial commit with the skeleton.
2. Push to the new origin's `main`.

In the parent:

3. Stage and commit `.gitmodules` + the new pointer using `prompts/pointer-bump.prompt.md`.

## 6. Update parent docs

- Add the new brain to `README.md`'s submodule table.
- Add it to `.github/copilot-instructions.md`'s submodule table.
- Add it to `.github/workflows/ci.yml` and `.github/workflows/lint.yml` matrix lists.
- Add it to `.github/AGENTS.md` per-brain section.

## 7. Hand off to domain work

Once the skeleton is green:

- Run `agents/brains-devsetup.agent.md` to verify the full workspace still installs and tests.
- Open the new submodule and begin domain implementation there; do **not** add domain code from the parent root.

Topic / brain name:

{{input}}
