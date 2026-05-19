---
description: "Consolidate cross-brain memories from .memories/ into permanent rules under .github/. Run periodically when 10+ memories accumulate."
agent: agent
---

# Dream Cycle (parent level)

You are running a **dream cycle** for the `brains` parent repo — consolidating cross-brain lessons from `.memories/` (parent root) into permanent rules under `.github/`.

Per-brain memories live in each submodule's own `.memories/` and have their own dream prompts; do not touch them from here.

## Process

### 1. Gather

Read every file in `.memories/` (skip `_archive/` and `INDEX.md`). Parse the `severity` frontmatter from each. Filter to `scope: cross-brain` or `scope: parent-only`. If `.memories/` is empty or only contains `.gitkeep`, report "No memories to process" and stop.

### 2. Conflicts first

Surface any memory containing a `**Conflict:**` line. For each, present:
- **Update rule** — modify the parent `.github/` file.
- **Discard lesson** — archive the memory.
- **Keep both** — add a nuanced note to the rule acknowledging the exception.

Wait for user input before proceeding.

### 3. Cluster

Group remaining memories by theme (e.g. "pointer bumps", "MCP interop", "release cascade"). Weight by severity.

### 4. Evaluate

- Any `severity: high` → act immediately.
- 2+ `severity: medium` on the same theme → act.
- 3+ `severity: low` on the same theme → act.
- Below threshold → defer.

### 5. Propose

Present a **dream plan** to the user:
- Which parent `.github/` files will be modified.
- What rules/guidelines will be added or refined.
- Which memories will be archived.
- Which memories will be deferred.

**Wait for user approval before changing anything.**

### 6. Apply

Edit `.github/` files minimally — append to sections instead of rewriting. Preserve existing voice and formatting.

### 7. Archive

Move processed memories to `.memories/_archive/`. Create the directory if needed. Verify it is still covered by `.gitignore`.

### 8. Update INDEX

Regenerate `.memories/INDEX.md` with deferred memories grouped by theme.

### 9. Report

Summarise what was added/modified, what was archived, what was deferred, and remind the user that all `.github/` changes are revertible via `git checkout`.

## Hard rules

- Never `git add` anything in `.memories/`.
- Never reference memory content verbatim in user-facing output.
- Never write secrets into rules or memories.
