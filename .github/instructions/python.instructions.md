---
applyTo: "**/*.py"
---
# Shared Python Style — `brains` workspace

This is the **baseline** Python style every brain inherits. Each submodule's own `.github/copilot-instructions.md` may add project-specific rules; on conflict, the submodule rule wins.

## Imports & headers

- `from __future__ import annotations` at the top of **every** module.
- Order: stdlib → third-party → local. One blank line between groups.
- Module-level docstring explains the purpose in 1–3 lines before any imports.

## Type hints

- Built-in generics: `list[int]`, `dict[str, int]`, `tuple[str, ...]`. Never `List`, `Dict`, `Tuple` from `typing`.
- Union syntax: `str | None`, never `Optional[str]`.
- Re-usable aliases live near the top of the module:
  ```python
  Lookup = dict[str, int]              # display_value → id
  CompositeLookup = dict[tuple, int]   # composite_key → id
  ```

## Naming

- Functions, methods, modules, locals: `snake_case`.
- Classes: `PascalCase`.
- Private helpers and module-internal symbols: `_leading_underscore`.
- Constants: `UPPER_SNAKE_CASE`.

## Docstrings

- Public functions and classes have a one-line summary; add `Args:` / `Returns:` blocks only when not obvious.
- Parsers include an `Examples:` block in the docstring showing input → output.
- Do **not** add docstrings to code you didn't change (per workspace policy).

## Error handling

- Parsers: return `None` for *optional* missing fields, raise `ValueError` for *required* ones.
- Query layers: project-specific exception (`QueryError`, `DataStaleError`).
- Dossier/file ops: project-specific exception (`WineNotFoundError`, `RecipeNotFoundError`, `ProtectedSectionError`).
- **No defensive error handling** for scenarios that cannot occur. Only validate at system boundaries.

## Security invariants (universal)

- Use `pathlib.Path.is_relative_to()` for any path traversal check.
- SQL validation must reject `INSERT`/`UPDATE`/`DELETE`/`DROP`/`CREATE`/`ALTER`/`TRUNCATE` if user-provided.
- Never `eval()` or `exec()` user input.
- Never disable TLS verification.
- Always set HTTP timeouts (default: 30s).
- Secrets live in `<project>.local.toml` (gitignored), never in main config.

## Testing (pytest)

- One test file per source module: `tests/test_<module>.py`.
- Group related tests in classes (`class TestFoobyAdapter:`).
- Shared fixtures in `tests/conftest.py`.
- Use `tmp_path` for all file I/O; never write to real `output/` directories.
- `pytest.raises(ValueError)` for expected failures.
- `@pytest.mark.parametrize` for data-driven cases; direct assertions for one-offs.
- **Every code change includes test updates.** No exceptions.

## Linting & formatting

- `ruff check .` and `ruff format --check .` are the canonical gate.
- Match the existing project's `pyproject.toml` config — do not introduce new linters at parent level.

## Things to avoid

- Over-engineering. Implement only what's requested or clearly necessary.
- Adding type annotations or docstrings to code you didn't change.
- Creating helpers for one-time operations.
- Bypassing tests with skip markers as a workaround.
