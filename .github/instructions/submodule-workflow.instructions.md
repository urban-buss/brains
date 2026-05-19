---
applyTo: "**"
---
# Submodule Workflow — Hard Rules

These rules apply to **any** Copilot session at the `brains` parent root. They protect against the most common foot-guns in a submodule-heavy workspace.

## 1. Source edits go inside submodules

Application source code (`*.py`, `pyproject.toml`, tests, docs of a brain) lives **inside** `cellarbrain/` or `recipebrain/`. Always `cd` into the relevant submodule before editing such files.

The only files that legitimately change at parent level:

- `.gitmodules`
- The submodule pointers themselves (created automatically by `git add <submodule>`)
- Anything under `.github/`, `.proposals/`, `.scratch/`, `.memories/`
- Top-level docs (`README.md`, `LICENSE` if added)
- `brains.code-workspace`

If a request seems to require editing source files at parent level, stop and ask.

## 2. Two commits, in this order

Changing code in a submodule requires:

1. Commit **inside** the submodule (`cd <submodule> && git commit`).
2. Commit the pointer bump **in the parent** (`git add <submodule> && git commit`).

Never do step 2 without step 1. Never leave step 1 without step 2.

## 3. Never stage a dirty submodule

If `git status` at parent level shows `modified: <submodule> (modified content)`, the submodule has uncommitted changes inside it. Refuse to commit the parent pointer until the inner state is clean and committed.

## 4. Pointer must exist on origin

Before committing a parent pointer bump, the referenced submodule commit **must** be reachable from the submodule's `origin` (any remote branch). Otherwise the parent will reference an unfetchable commit.

Verify with:

```powershell
cd <submodule>
git fetch origin
git branch -r --contains HEAD
# must list at least one origin/* branch
```

Or run `python .github/tools/check-submodule-pointers.py` from the parent.

If the commit only exists locally, push it first (`git push origin <branch>`) **and only if the user has approved pushing** that branch.

## 5. Pushing rules

- Never `git push --force` either repo without explicit user confirmation.
- Never push a submodule branch the user hasn't explicitly intended to share.
- When pushing the parent, prefer `git push --recurse-submodules=check` to be warned about missing-on-remote pointers.

## 6. Never edit a submodule's tracked branch in `.gitmodules` casually

Switching the `branch =` value in `.gitmodules` changes how `git submodule update --remote` behaves for every collaborator. Confirm with the user before touching it.

## 7. Refuse to commit `.memories/`, `.proposals/`, `.scratch/`

These are local-only working folders (already in `.gitignore`). Refuse any `git add` (including `-f`) that targets them.

## 8. Never bypass safety checks

No `--no-verify`, no `git reset --hard` without confirmation, no `git clean -fdx` without confirmation.

## 9. Detached HEAD inside a submodule is normal

After `git submodule update`, the submodule will be on a detached HEAD at the pointer commit. To make new commits, check out (or create) a branch inside the submodule first.
