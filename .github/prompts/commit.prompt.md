---
description: "Commit changes at the parent level with a conventional-commit message. Use when: 'commit', 'save changes' at parent root."
argument-hint: "Optional: scope or hint for the commit message"
agent: agent
---

You are committing at the **parent** `brains` repo level. The parent rarely contains source-code changes — most commits here are submodule pointer bumps or coordinator-tooling edits.

## Steps

1. **Inspect** the staged + unstaged changes:

   ```powershell
   git status
   git diff --staged
   git diff
   ```

2. **Refuse** if any of the following apply (and explain why):
   - A submodule shows `modified content` (dirty inner state) — commit inside the submodule first. See `prompts/pointer-bump.prompt.md`.
   - Paths under `.memories/`, `.proposals/`, or `.scratch/` are staged — these are gitignored and must not be committed.
   - Source files outside `.github/`, top-level docs, `.gitmodules`, or submodule pointers were edited — that work belongs inside a submodule.

3. **Choose the type** following Conventional Commits:

   | Situation | Type & scope |
   |---|---|
   | Only submodule pointers moved | `chore(<submodule>): bump to <short-sha>` (one per submodule) or `chore(submodules): bump <list>` if multiple |
   | Coordinator tooling under `.github/` | `chore(github): …` or `feat(github): …` |
   | Top-level docs / README | `docs: …` |
   | `.gitmodules` change (added/removed/retargeted submodule) | `chore(submodules): …` |

4. If a pointer bump is included, the message body should list the inbound submodule commit range:

   ```text
   chore(cellarbrain): bump to a1b2c3d

   Includes 4 commits from cellarbrain main:
   - feat(query): add cross-vintage view
   - fix(parser): handle empty CSV
   - test: extend smoke tests
   - chore: bump version to 0.3.1
   ```

   Use `prompts/pointer-bump.prompt.md` for the full guided flow.

5. **Stage** only what should be in this commit (don't blanket-stage). Then commit.

6. **Do not push** unless the user asks.

{{input}}
