# `_shared/` — canonical mirrored meta-files

This folder holds the **canonical** versions of meta-files that are mirrored
into every brain (submodule) via `tools/sync-shared-meta.py`.

Edit files here, then run:

```powershell
python .github/tools/sync-shared-meta.py
```

…from the parent root. The generator writes one byte-identical (modulo
template substitution) copy into each submodule's `.github/` at the **same
relative path** (so `_shared/instructions/foo.md` lands at
`<submodule>/.github/instructions/foo.md`).

## Template variables

Files may contain `{{var}}` placeholders that the generator substitutes
per-submodule from `pyproject.toml`:

| Placeholder | Source | Example |
|---|---|---|
| `{{package_name}}` | `[project] name` | `cellarbrain` |
| `{{Package_Name}}` | titlecase of the above | `Cellarbrain` |
| `{{cli}}` | first key in `[project.scripts]`, or `{{package_name}}` | `cellarbrain` |

## Generated-file banner

Each mirrored file gets a banner inserted **after** the YAML frontmatter so
Copilot's `applyTo` still parses cleanly:

```markdown
<!-- GENERATED FROM brains/.github/_shared/<path> -->
<!-- DO NOT EDIT — run `python .github/tools/sync-shared-meta.py` at the parent root. -->
```

## Drift check

CI runs `tools/check-meta-drift.py`, which re-renders into a temp dir and
diffs against the committed mirrors in each submodule. Any mismatch fails CI.

## Brain-specific addenda

Don't edit a mirrored file inside a submodule. If a brain needs to extend a
shared rule, add a sibling file with a clear suffix (for example
`memory-management.cellarbrain.instructions.md`) and reference it from
`copilot-instructions.md`.
