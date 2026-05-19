---
description: "Sync the local working tree after pulling parent changes that include submodule pointer moves. Use when: 'sync', 'I just pulled', 'submodules out of date', 'catch up'."
agent: agent
---

A collaborator pulled new commits into the parent that move submodule pointers. This prompt brings the local checkout up to date safely.

## 1. Pull the parent

```powershell
git pull --ff-only
```

If this fails, stop and resolve the parent-level conflict first.

## 2. Update submodules to their recorded pointers

```powershell
git submodule update --init --recursive
```

This checks out every submodule at the **exact pointer** the parent now records (likely detached HEAD). It does **not** advance to branch tips.

## 3. Verify

```powershell
python .github/tools/foreach.py --include-parent -- git status -sb
python .github/tools/check-submodule-pointers.py --no-fetch
```

Every submodule should be clean and on the recorded pointer.

## 4. Reinstall editable packages if dependencies moved

If any submodule's `pyproject.toml` changed since the previous pull:

```powershell
python .github/tools/foreach.py -- pip install -e ".[dev]"
```

## 5. Notes

- After this prompt, submodules are typically in **detached HEAD** state — that's expected. To make new commits inside a submodule, check out (or create) a branch first.
- If you want to advance pointers further (to tracked-branch tips), that's a separate operation — use `prompts/submodule-update.prompt.md`.
