---
description: "Generate a clean parent-repo commit that records a submodule pointer move with the inbound commit range in the body. Use when: 'bump pointer', 'pointer bump', 'commit submodule update'."
argument-hint: "Optional: submodule name (cellarbrain or recipebrain). If omitted, bumps every modified submodule."
agent: agent
---

You are recording a **submodule pointer bump** in the parent repo.

## Pre-flight (refuse if any fails)

1. Working tree at parent level: only submodule pointer changes may be staged or unstaged.
   ```powershell
   git status --porcelain
   ```
   Anything beyond `M cellarbrain` / `M recipebrain` lines requires a separate commit.

2. Each affected submodule must have a **clean** working tree:
   ```powershell
   cd <submodule>; git status --porcelain
   ```
   If non-empty → stop, ask the user to commit inside the submodule first.

3. Each new pointer commit must be reachable from the submodule's `origin`:
   ```powershell
   python .github/tools/check-submodule-pointers.py
   ```
   If any pointer is local-only, stop and ask whether to push it first (`git push origin <branch>` inside the submodule). Get explicit user approval before pushing.

## Build the commit message

For each affected submodule:

1. Read the old pointer commit (parent's view) and the new HEAD inside the submodule:
   ```powershell
   git ls-tree HEAD <submodule>        # old SHA in parent index
   cd <submodule>; git rev-parse HEAD  # new SHA
   ```

2. Collect the inbound commit list (oldest → newest):
   ```powershell
   cd <submodule>
   git log --pretty=format:"- %s" <old-sha>..<new-sha>
   ```

3. Compose the message:

   - **Single submodule moved** →
     ```
     chore(<submodule>): bump to <new-short-sha>

     Includes N commits from <submodule> <branch>:
     - <subject 1>
     - <subject 2>
     …
     ```

   - **Multiple submodules moved** → one commit per submodule (preferred), or a combined commit titled `chore(submodules): bump <names>` with a body grouped by submodule.

4. Stage **only** the submodule pointer files and commit:
   ```powershell
   git add <submodule>
   git commit -F <message-file>
   ```

## Post-conditions

- `git status` is clean.
- `git log -1` shows the new pointer-bump commit.
- Do **not** push unless the user asks.

{{input}}
