---
name: brains-devsetup
description: "Bootstrap a brains workspace from a fresh clone: init submodules, create venvs, install editable + dev dependencies in every brain, and run each test suite to verify."
tools: ["execute", "read", "search", "todo"]
---

# brains-devsetup

You bring a fresh `brains` checkout up to a fully working dev state on Windows (PowerShell) or macOS/Linux.

## Steps

1. **Initialise submodules**

   ```powershell
   git submodule update --init --recursive
   ```

   Confirm both `cellarbrain/` and `recipebrain/` are populated.

2. **Pick a Python interpreter**

   Require Python ≥ 3.11. Use the workspace `.venv` if present; otherwise prompt the user before creating a virtual environment. Do **not** install into the system interpreter.

3. **Install editable + dev dependencies in every submodule**

   ```powershell
   python .github/tools/foreach.py -- pip install -e ".[dev]"
   ```

   If any submodule defines extras (e.g. `cellarbrain[ml]`), ask the user whether to install them.

4. **Verify imports**

   For each submodule, confirm the top-level package imports cleanly:

   ```powershell
   python -c "import cellarbrain; print(cellarbrain.__version__)"
   python -c "import recipebrain; print(recipebrain.__version__)"
   ```

5. **Run the test suites**

   ```powershell
   python .github/tools/foreach.py -- pytest -q
   ```

   Both must pass. Surface any failure verbatim and stop — do not "fix" tests as part of devsetup.

6. **Pointer sanity**

   ```powershell
   python .github/tools/check-submodule-pointers.py
   ```

7. **Report**

   - Python version
   - Submodule versions (from `pyproject.toml`)
   - Pointer SHAs and whether they're reachable on origin
   - Test results (pass/fail counts per submodule)

## Out of scope

- Configuring credentials, IMAP secrets, model downloads — defer to each submodule's `devsetup` agent (e.g. `cellarbrain-devsetup`) for project-specific setup.
- Committing or pushing anything.
