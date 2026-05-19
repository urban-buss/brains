---
description: "Show git status across the parent repo and every submodule. Use when: 'status', 'where am I', 'what changed', 'overall state'."
agent: agent
---

Print a compact health report covering the parent repo and every submodule.

## Steps

1. **Parent state**:

   ```powershell
   git status -sb
   git log -1 --pretty=format:"%h %s (%ar)"
   ```

2. **Submodule state** — for each entry in `.gitmodules`:

   ```powershell
   cd <submodule>
   git status -sb
   git log -1 --pretty=format:"%h %s (%ar)"
   cd ..
   ```

   Or simply:

   ```powershell
   python .github/tools/foreach.py --include-parent -- git status -sb
   ```

3. **Pointer hygiene**:

   ```powershell
   python .github/tools/check-submodule-pointers.py
   ```

   Flag any pointer that is local-only on the user's machine.

4. **Summarise** as a single table:

   | Repo | Branch | Ahead/Behind | Dirty? | Pointer pushed? |
   |------|--------|--------------|--------|-----------------|
   | brains (parent) | … | … | … | n/a |
   | cellarbrain | … | … | … | … |
   | recipebrain | … | … | … | … |

5. Call out anything that needs attention (dirty submodules, unpushed pointers, detached HEADs that aren't expected).

Do **not** stage or commit anything. This prompt is read-only.

{{input}}
