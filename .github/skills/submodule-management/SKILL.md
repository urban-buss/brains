---
name: submodule-management
description: "Safe Git workflows for the submodule layer: updating, pinning, verifying pointers, and recovering from common foot-guns. Load when working with .gitmodules or when status is confusing."
---

# Submodule management

The most error-prone moments in this workspace involve Git submodules. This skill is the checklist + recovery guide.

## Mental model

- The **parent repo** records, for each submodule, a single fixed commit SHA — the "pointer".
- The **submodule's own repo** has its own history, branches, and remotes.
- `git submodule update` reads pointers and checks out the submodule at exactly those SHAs (usually detached HEAD).
- `git submodule update --remote` fast-forwards each submodule to the tip of the branch named in `.gitmodules` — i.e. it **changes** the pointer.

## Daily commands

| Goal | Command |
|---|---|
| Bring a fresh clone up | `git submodule update --init --recursive` |
| Sync after `git pull` moved pointers | `git submodule update --init --recursive` (same command) |
| Advance every submodule to tracked-branch tip | `git submodule update --remote --merge --recursive` |
| Run a command in every submodule | `python .github/tools/foreach.py -- <cmd>` |
| Verify pointers are reachable on origin | `python .github/tools/check-submodule-pointers.py` |
| Snapshot of versions and SHAs | `python .github/tools/snapshot-versions.py` |

## Safe pointer bump (the dual-commit dance)

1. `cd <submodule>` — make your edits inside the submodule.
2. `git add … && git commit` inside the submodule.
3. (If sharing) `git push` inside the submodule.
4. `cd ..` — back to parent.
5. `git add <submodule>` — stages the new SHA.
6. `git commit -m "chore(<submodule>): bump to <short-sha>"` — records the pointer move in the parent.

Or run `prompts/pointer-bump.prompt.md` which automates the message body with the inbound commit range.

## Recovery

### "My submodule shows `(modified content)` but I didn't touch it"

The submodule's working tree differs from the recorded pointer. Either:
- The submodule has uncommitted changes inside — `cd <submodule>; git status` reveals them.
- Or you reset/checked out the submodule manually — `git submodule update --init --recursive` re-pins it.

### "I committed a pointer bump but `check-submodule-pointers.py` says it's local-only"

You forgot to push the submodule. From inside the submodule, `git push origin <branch>`. Then the existing parent commit is fine — no need to amend.

### "Parent says `modified: <submodule> (new commits)` and I want to discard"

To restore the submodule to the parent's recorded pointer:
```powershell
git submodule update --init --recursive
```

To **keep** the new commits (record them as a bump):
```powershell
git add <submodule>
```
…then use `prompts/pointer-bump.prompt.md`.

### "Detached HEAD inside a submodule — can I commit there?"

Not directly. Create a branch first:
```powershell
cd <submodule>
git switch -c my-feature
# now commit as usual
```

### "I want to change which branch the submodule tracks"

Edit `.gitmodules`:
```ini
[submodule "cellarbrain"]
    path = cellarbrain
    url = https://github.com/urban-buss/cellarbrain.git
    branch = some-other-branch    # ← change this
```
Then `git submodule sync` and `git submodule update --remote`. Commit `.gitmodules` + the (possibly moved) pointer together.

## Anti-patterns to refuse

- `git push --force` in either repo without explicit user approval.
- Bumping a pointer to a commit that is not yet on the submodule's `origin`.
- Editing source files of a brain from the parent root.
- Committing a pointer bump while the submodule is dirty.
- `git add -f .memories/` / `.proposals/` / `.scratch/`.

## Related

- `instructions/submodule-workflow.instructions.md` — the hard-rule version, auto-applied.
- `prompts/pointer-bump.prompt.md`, `prompts/submodule-update.prompt.md`, `prompts/submodule-sync.prompt.md`.
- `workflows/submodule-sanity.yml` — CI check that runs on every PR.
