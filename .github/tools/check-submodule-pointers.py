#!/usr/bin/env python3
"""Verify every submodule pointer in the parent repo is reachable on origin.

For each submodule listed in ``.gitmodules``:
  1. Read the recorded pointer commit from the parent index.
  2. ``git fetch origin`` inside the submodule (quiet).
  3. Confirm the pointer commit is reachable from at least one ``origin/*``
     branch (``git branch -r --contains <sha>``).

Exits non-zero if any pointer is local-only, missing, or unfetchable. Suitable
for use in CI (``submodule-sanity.yml``) and as a pre-flight before
``prompts/pointer-bump.prompt.md``.

Usage:
    python .github/tools/check-submodule-pointers.py
    python .github/tools/check-submodule-pointers.py --no-fetch  # offline
"""

from __future__ import annotations

import argparse
import configparser
import pathlib
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
GITMODULES = REPO_ROOT / ".gitmodules"


def discover_submodules() -> list[tuple[str, pathlib.Path]]:
    if not GITMODULES.is_file():
        return []
    parser = configparser.ConfigParser()
    parser.read(GITMODULES, encoding="utf-8")
    out: list[tuple[str, pathlib.Path]] = []
    for section in parser.sections():
        if not section.startswith("submodule "):
            continue
        name = section.split('"', 2)[1]
        rel = parser.get(section, "path", fallback=name)
        out.append((name, (REPO_ROOT / rel).resolve()))
    return sorted(out)


def pointer_sha(name: str, path: pathlib.Path) -> str | None:
    """Return the SHA the parent records for the submodule, or None."""
    rel = path.relative_to(REPO_ROOT).as_posix()
    proc = subprocess.run(
        ["git", "ls-tree", "HEAD", rel],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if proc.returncode != 0 or not proc.stdout.strip():
        return None
    # Format: "<mode> commit <sha>\t<path>"
    parts = proc.stdout.split()
    if len(parts) < 3 or parts[1] != "commit":
        return None
    return parts[2]


def check_one(name: str, path: pathlib.Path, *, fetch: bool) -> tuple[bool, str]:
    if not (path / ".git").exists() and not (path / ".git").is_file():
        return False, f"{name}: submodule not initialised ({path})"

    sha = pointer_sha(name, path)
    if sha is None:
        return False, f"{name}: could not read parent pointer"

    if fetch:
        proc = subprocess.run(
            ["git", "fetch", "--quiet", "origin"],
            cwd=path,
            capture_output=True,
            text=True,
            check=False,
        )
        if proc.returncode != 0:
            return False, f"{name}: git fetch failed: {proc.stderr.strip()}"

    proc = subprocess.run(
        ["git", "branch", "-r", "--contains", sha],
        cwd=path,
        capture_output=True,
        text=True,
        check=False,
    )
    branches = [
        line.strip().lstrip("* ").strip()
        for line in proc.stdout.splitlines()
        if line.strip()
    ]
    branches = [b for b in branches if b.startswith("origin/")]
    if not branches:
        return False, (
            f"{name}: pointer {sha[:12]} is NOT reachable from any origin/* branch. "
            "Push the commit to origin, or move the pointer back."
        )
    return True, f"{name}: pointer {sha[:12]} reachable from {', '.join(branches[:3])}"


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument(
        "--no-fetch",
        action="store_true",
        help="Skip 'git fetch origin' in each submodule (use cached refs).",
    )
    args = p.parse_args(argv)

    submodules = discover_submodules()
    if not submodules:
        print("No submodules found.", file=sys.stderr)
        return 0

    worst_ok = True
    for name, path in submodules:
        ok, msg = check_one(name, path, fetch=not args.no_fetch)
        marker = "OK " if ok else "FAIL"
        print(f"[{marker}] {msg}")
        worst_ok = worst_ok and ok
    return 0 if worst_ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
