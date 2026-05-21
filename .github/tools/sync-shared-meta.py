#!/usr/bin/env python3
"""Mirror canonical meta-files from `.github/_shared/` into every submodule.

Run from the parent root:

    python .github/tools/sync-shared-meta.py            # write mirrors
    python .github/tools/sync-shared-meta.py --check    # diff only, non-zero on drift

Substitutes `{{package_name}}`, `{{Package_Name}}`, and `{{cli}}` per submodule
(read from each submodule's `pyproject.toml`).
"""

from __future__ import annotations

import argparse
import difflib
import sys
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
SHARED_DIR = REPO_ROOT / ".github" / "_shared"

MARKDOWN_BANNER = (
    "<!-- GENERATED FROM .github/_shared/{rel} -->\n"
    "<!-- DO NOT EDIT — run `python .github/tools/sync-shared-meta.py` "
    "at the parent root. -->\n"
)

PYTHON_BANNER = (
    "# GENERATED FROM .github/_shared/{rel}\n"
    "# DO NOT EDIT — run `python .github/tools/sync-shared-meta.py` "
    "at the parent root.\n"
)


def discover_submodules(root: Path) -> list[Path]:
    """Return submodule directories declared in `.gitmodules`."""
    gitmodules = root / ".gitmodules"
    if not gitmodules.is_file():
        return []
    paths: list[Path] = []
    for line in gitmodules.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("path = "):
            rel = line.removeprefix("path = ").strip()
            paths.append(root / rel)
    return paths


def read_template_vars(submodule: Path) -> dict[str, str]:
    """Resolve template variables from a submodule's `pyproject.toml`."""
    pyproject = submodule / "pyproject.toml"
    if not pyproject.is_file():
        raise FileNotFoundError(f"missing pyproject.toml: {pyproject}")
    data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
    project = data.get("project", {})
    name = project.get("name")
    if not name:
        raise ValueError(f"no [project] name in {pyproject}")
    scripts = project.get("scripts", {}) or {}
    cli = next(iter(scripts), name)
    return {
        "package_name": name,
        "Package_Name": name.capitalize(),
        "cli": cli,
    }


def substitute(text: str, vars_: dict[str, str]) -> str:
    for key, value in vars_.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def insert_banner(text: str, rel: str) -> str:
    """Insert a GENERATED banner appropriate for the file type."""
    rel_posix = rel.replace("\\", "/")
    if rel_posix.endswith(".py"):
        banner = PYTHON_BANNER.format(rel=rel_posix)
        # Preserve shebang on line 1.
        if text.startswith("#!"):
            shebang, _, rest = text.partition("\n")
            return f"{shebang}\n{banner}\n{rest.lstrip()}"
        return banner + "\n" + text
    banner = MARKDOWN_BANNER.format(rel=rel_posix)
    if text.startswith("---\n"):
        end = text.find("\n---\n", 4)
        if end != -1:
            head = text[: end + len("\n---\n")]
            tail = text[end + len("\n---\n") :]
            return f"{head}\n{banner}\n{tail.lstrip()}"
    return banner + "\n" + text


def iter_shared_files(shared: Path):
    for path in sorted(shared.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(shared)
        if rel.parts[0] == "README.md" or rel.name == "README.md":
            continue
        yield path, rel


def render(source: Path, rel: Path, vars_: dict[str, str]) -> str:
    raw = source.read_text(encoding="utf-8")
    body = substitute(raw, vars_)
    return insert_banner(body, str(rel))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Diff against committed mirrors instead of writing.",
    )
    args = parser.parse_args()

    if not SHARED_DIR.is_dir():
        print(f"ERROR: missing {SHARED_DIR}", file=sys.stderr)
        return 1

    submodules = discover_submodules(REPO_ROOT)
    if not submodules:
        print("ERROR: no submodules found in .gitmodules", file=sys.stderr)
        return 1

    drift = False
    written = 0
    for submodule in submodules:
        if not submodule.is_dir():
            print(f"skip (missing): {submodule.name}")
            continue
        try:
            vars_ = read_template_vars(submodule)
        except (FileNotFoundError, ValueError) as exc:
            print(f"skip {submodule.name}: {exc}")
            continue

        for source, rel in iter_shared_files(SHARED_DIR):
            target = submodule / ".github" / rel
            rendered = render(source, rel, vars_)

            if args.check:
                if not target.is_file():
                    print(f"DRIFT (missing): {target.relative_to(REPO_ROOT)}")
                    drift = True
                    continue
                actual = target.read_text(encoding="utf-8")
                if actual != rendered:
                    print(f"DRIFT: {target.relative_to(REPO_ROOT)}")
                    diff = difflib.unified_diff(
                        actual.splitlines(keepends=True),
                        rendered.splitlines(keepends=True),
                        fromfile=str(target.relative_to(REPO_ROOT)),
                        tofile=f"_shared/{rel}",
                        n=2,
                    )
                    sys.stdout.writelines(diff)
                    drift = True
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(rendered, encoding="utf-8")
                written += 1

    if args.check:
        if drift:
            print("\nMirrors are out of sync. Run `python .github/tools/sync-shared-meta.py`.")
            return 1
        print("All mirrors in sync.")
        return 0

    print(f"Wrote {written} mirrored files across {len(submodules)} submodule(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
