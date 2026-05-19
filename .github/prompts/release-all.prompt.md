---
description: "Cascade a coordinated release across every submodule, then bump the parent pointers in lockstep. Use when: 'release all', 'cut a coordinated release', 'release both brains'."
argument-hint: "Optional: bump type (patch/minor/major) applied to each submodule"
agent: agent
---

Release every brain together. Each submodule remains autonomous (its own version, CHANGELOG, tag), but the parent records a single, coordinated pointer-bump commit so collaborators can clone one matching set.

## 1. Pre-flight (parent)

- Working tree clean at parent level (`git status --porcelain` empty).
- On the parent branch you want to release from (usually `main`).
- All submodules clean inside (`python .github/tools/foreach.py -- git status --porcelain`).

Stop on any failure.

## 2. Release each submodule

For **each** submodule (process them sequentially, not in parallel):

1. `cd <submodule>`
2. Run the submodule's own release workflow — typically `prompts/release.prompt.md` inside that submodule. Follow whatever it instructs (version bump, CHANGELOG update, branch creation, squash commit).
3. **Stop and ask the user** before pushing the submodule branch or creating tags. Push only when the user confirms.
4. Note the new release SHA / tag for the parent commit message.
5. `cd ..`

If any submodule's release fails (tests, lint, build), stop the entire cascade — do not partially release.

## 3. Bump parent pointers

Once every submodule has its release commit on its `origin`:

```powershell
git submodule update --remote --merge
python .github/tools/check-submodule-pointers.py
```

Both submodules' new HEADs must be reachable on origin before continuing.

## 4. Commit the coordinated bump

Use `prompts/pointer-bump.prompt.md` but produce a **single combined** commit at parent level:

```
chore(submodules): coordinated release — cellarbrain vX.Y.Z, recipebrain vA.B.C

cellarbrain vX.Y.Z (<old>..<new>):
  - <highlights>

recipebrain vA.B.C (<old>..<new>):
  - <highlights>
```

## 5. Tag the parent (optional)

If the user wants a parent-level marker:

```powershell
git tag -a coord-YYYY-MM-DD -m "Coordinated release: cellarbrain vX.Y.Z + recipebrain vA.B.C"
```

Ask before tagging — coordinated tags at parent level are an opt-in convention.

## 6. Final state

- Each submodule has its release commit, CHANGELOG entry, and (if confirmed) its tag, all pushed.
- The parent has one combined pointer-bump commit.
- Nothing is force-pushed.

{{input}}
