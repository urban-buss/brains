---
description: "Catch up local_* branches in all submodules with origin/main — merge, resolve conflicts, harmonize, and run CI. Use when: 'catch up local branch', 'merge main into local', 'local branch behind main', 'sync local with main', 'update local branch'."
agent: agent
---

Bring every submodule's currently checked-out `local_*` branch up to date with `origin/main`. Resolve merge conflicts intelligently, identify follow-up harmonization work, and validate with the CI pipeline.

---

## Phase 1 — Assess divergence

For each submodule in `.gitmodules`:

```powershell
cd <submodule>
git fetch origin
git branch --show-current          # must be a local_* branch
git log --oneline HEAD..origin/main | Measure-Object -Line   # commits behind
git log --oneline origin/main..HEAD | Measure-Object -Line   # commits ahead
cd ..
```

Produce a summary table:

| Submodule | Local branch | Behind main | Ahead of main | Action needed? |
|-----------|--------------|-------------|---------------|----------------|

If a submodule is **not** on a `local_*` branch, warn the user and skip it.
If a submodule is already up to date (0 behind), note it and skip to Phase 4.

---

## Phase 2 — Merge origin/main into each local branch

For every submodule that is behind:

```powershell
cd <submodule>
git merge origin/main --no-edit
```

### If merge succeeds (no conflicts)

Log the merge commit and continue to Phase 3.

### If merge conflicts occur

**Do not blindly accept either side.** Follow this conflict-resolution protocol:

1. List conflicted files:
   ```powershell
   git diff --name-only --diff-filter=U
   ```

2. For each conflicted file, understand context by examining:
   - The incoming changes from main:
     ```powershell
     git log --oneline --follow -p origin/main -- <file> | Select-Object -First 80
     ```
   - The local branch's changes:
     ```powershell
     git log --oneline --follow -p HEAD -- <file> | Select-Object -First 80
     ```
   - The conflict markers in the working tree.

3. Resolve each conflict by:
   - Understanding the **intent** of both sides (not just the text diff).
   - Preserving both sets of functionality where they don't contradict.
   - Preferring the upstream pattern if the local change was a precursor to the same fix.
   - Adding comments (`# merged from main: ...`) only if the resolution is non-obvious.

4. Stage resolved files and complete the merge:
   ```powershell
   git add <resolved-files>
   git commit --no-edit
   ```

> **Delegate option**: If the conflict set is large (>5 files), delegate per-file resolution to a subagent with the full diff context and resolution instructions, then review the result.

---

## Phase 3 — Harmonization analysis

After merging, analyze whether the incoming changes from main require follow-up adjustments on the local branch. Common cases:

- **API changes**: A function signature changed on main → local callers need updating.
- **Config/schema drift**: New required fields in `pyproject.toml`, config TOML, or data schemas.
- **Import moves**: Modules renamed or relocated on main → local imports stale.
- **New patterns**: Main adopted a new utility/helper that the local branch should use instead of its ad-hoc version.
- **Test coverage**: New features merged from main lack test coverage for local-branch interactions.

### Steps

1. Review the merge diff (what came in from main):
   ```powershell
   cd <submodule>
   git diff HEAD~1..HEAD --stat
   git log --oneline MERGE_HEAD~5..MERGE_HEAD  # recent main commits
   ```

2. Search for inconsistencies:
   - Grep for deprecated names/patterns that main removed but local still uses.
   - Check that imports resolve correctly.
   - Look for duplicated logic (local implemented something main also now provides).

3. If harmonization changes are needed:
   - Plan them as discrete commits with clear messages.
   - **Delegate** implementation to a subagent if the change set is non-trivial (>3 files or requires deep domain understanding). Provide the subagent with:
     - The list of changes needed and why.
     - Relevant file paths and context.
     - The coding conventions (reference the submodule's `.github/copilot-instructions.md`).
   - Commit each harmonization change separately inside the submodule.

---

## Phase 4 — Run CI pipeline

For every submodule where Phase 2 or Phase 3 produced commits:

```powershell
cd <submodule>
pip install -e ".[dev]"
pytest -q
```

### If tests pass

Report success and move to the next submodule.

### If tests fail

1. Capture the failure output.
2. Diagnose root cause (merge artifact? missing import? schema mismatch?).
3. **Delegate** the fix to a subagent with:
   - The pytest output (traceback + assertion).
   - The recently merged/harmonized files.
   - Instructions to fix and commit inside the submodule.
4. Re-run `pytest -q` to confirm the fix.
5. Repeat until green.

---

## Phase 5 — Final report

Produce a summary:

| Submodule | Branch | Merged? | Conflicts? | Harmonized? | CI status |
|-----------|--------|---------|------------|-------------|-----------|

For each submodule that had work:
- List merge commits (SHAs + subjects).
- List harmonization commits if any.
- List fix commits if CI required repairs.
- Note if anything remains unresolved or needs user attention.

---

## Safety rules

- **Never force-push** any branch.
- **Never commit to main** — all work stays on the `local_*` branch.
- If a merge is catastrophically conflicted (>20 files, or entire modules diverged), abort (`git merge --abort`) and ask the user how to proceed.
- Follow the submodule-workflow instructions: commits stay inside the submodule; pointer bumps happen separately in the parent if needed.
- Do **not** automatically bump parent pointers — that's a separate operation the user can trigger with `pointer-bump.prompt.md` when ready.
