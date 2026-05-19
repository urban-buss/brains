---
description: "Update every submodule to the tip of its tracked branch, run pre-flight checks, and prepare a clean pointer-bump commit. Use when: 'update submodules', 'sync submodules', 'pull submodules', 'bump submodules'."
agent: agent
---

Bring every submodule pointer up to the tip of its tracked branch, with full safety checks.

## 1. Verify clean parent state

```powershell
git status --porcelain
```

If anything beyond submodule pointer changes is staged or modified at parent level, stop and ask the user to commit or stash first.

## 2. Verify each submodule is clean

```powershell
python .github/tools/foreach.py -- git status --porcelain
```

If any submodule has uncommitted changes, **stop**. Resolve inside the submodule first.

## 3. Update all submodules to their tracked branch tips

```powershell
git submodule update --remote --merge --recursive
```

For each submodule, this fast-forwards the working tree to the branch named in `.gitmodules` (default: `main`).

## 4. Verify pointers exist on origin

```powershell
python .github/tools/check-submodule-pointers.py
```

If any submodule's new HEAD is local-only, stop. Ask the user whether to push it from the submodule first.

## 5. Run the test suites (optional but recommended)

```powershell
python .github/tools/foreach.py -- pytest -q
```

If any suite fails, surface the failure and stop — do not commit a pointer bump that points to a known-broken commit.

## 6. Hand off to `pointer-bump.prompt.md`

Invoke the `pointer-bump` workflow to compose the per-submodule commit messages with the inbound commit ranges and create the commits. Do **not** push automatically.

## 7. Report

- Which submodules moved (old SHA → new SHA, # of commits).
- Which submodules were already at tip (no-op).
- Whether `check-submodule-pointers.py` passed.
- Whether the test suites passed.
