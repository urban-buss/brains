#!/usr/bin/env python3
"""Run a command in every submodule (and optionally the parent repo).

Examples:
    python .github/tools/foreach.py -- pytest -q
    python .github/tools/foreach.py -- pip install -e ".[dev]"
    python .github/tools/foreach.py --include-parent -- git status -sb
    python .github/tools/foreach.py --only cellarbrain -- ruff check .

Exit code is the maximum (worst) exit code of any invocation, so the script
fails fast in CI when any submodule fails. Output from each run is streamed
with a header line, so logs stay readable.

Cross-platform: works on Windows PowerShell and POSIX shells. The command
after ``--`` is invoked via ``subprocess.run`` with ``shell=False`` and a
list of args (so quoting follows the shell that invoked this script).
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
    """Return ``[(name, abs_path), ...]`` parsed from ``.gitmodules``."""
    if not GITMODULES.is_file():
        return []
    parser = configparser.ConfigParser()
    parser.read(GITMODULES, encoding="utf-8")
    out: list[tuple[str, pathlib.Path]] = []
    for section in parser.sections():
        # Section name is e.g. 'submodule "cellarbrain"'.
        if not section.startswith("submodule "):
            continue
        name = section.split('"', 2)[1]
        rel = parser.get(section, "path", fallback=name)
        out.append((name, (REPO_ROOT / rel).resolve()))
    return sorted(out)


def run_one(label: str, cwd: pathlib.Path, command: list[str]) -> int:
    header = f"\n=== [{label}] {' '.join(command)} (cwd={cwd}) ==="
    print(header, flush=True)
    if not cwd.is_dir():
        print(f"  SKIP: {cwd} does not exist", flush=True)
        return 0
    proc = subprocess.run(command, cwd=cwd, shell=False)
    return proc.returncode


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(
        description="Run a command in every brains submodule.",
        usage="%(prog)s [--include-parent] [--only NAME ...] -- <command> [args...]",
    )
    p.add_argument(
        "--include-parent",
        action="store_true",
        help="Also run the command in the parent repo root.",
    )
    p.add_argument(
        "--only",
        action="append",
        default=[],
        metavar="NAME",
        help="Restrict to the named submodule(s). Repeatable.",
    )
    p.add_argument(
        "--continue-on-error",
        action="store_true",
        help="Run every target even if one fails (default: keep going, exit with worst code).",
    )

    if "--" not in argv:
        p.print_help(sys.stderr)
        return 2
    sep = argv.index("--")
    args = p.parse_args(argv[:sep])
    command = argv[sep + 1 :]
    if not command:
        print("ERROR: no command specified after --", file=sys.stderr)
        return 2

    targets: list[tuple[str, pathlib.Path]] = []
    if args.include_parent:
        targets.append(("brains", REPO_ROOT))
    for name, path in discover_submodules():
        if args.only and name not in args.only:
            continue
        targets.append((name, path))

    if not targets:
        print("ERROR: no targets to run against", file=sys.stderr)
        return 2

    worst = 0
    for name, path in targets:
        code = run_one(name, path, command)
        if code != 0:
            worst = max(worst, code)
            if not args.continue_on_error:
                # Keep going by default — we still want the full picture.
                continue
    print(f"\n=== done; worst exit code = {worst} ===")
    return worst


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
