#!/usr/bin/env python3
"""Emit a manifest of {submodule: version, commit, branch} for every brain.

Useful for release notes, the README badge block, and reproducible installs.

Usage:
    python .github/tools/snapshot-versions.py            # Markdown table (default)
    python .github/tools/snapshot-versions.py --json     # machine-readable JSON
    python .github/tools/snapshot-versions.py --out manifest.json --json
"""

from __future__ import annotations

import argparse
import configparser
import json
import pathlib
import re
import subprocess
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent.parent
GITMODULES = REPO_ROOT / ".gitmodules"

VERSION_RE = re.compile(r'^\s*version\s*=\s*"([^"]+)"', re.MULTILINE)


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


def read_version(path: pathlib.Path) -> str | None:
    pyproject = path / "pyproject.toml"
    if not pyproject.is_file():
        return None
    match = VERSION_RE.search(pyproject.read_text(encoding="utf-8"))
    return match.group(1) if match else None


def git(cwd: pathlib.Path, *args: str) -> str:
    proc = subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=False
    )
    return proc.stdout.strip()


def snapshot_one(name: str, path: pathlib.Path) -> dict[str, str | None]:
    if not path.is_dir():
        return {"name": name, "error": "submodule path missing"}
    commit = git(path, "rev-parse", "HEAD") or None
    short = commit[:12] if commit else None
    branch = git(path, "rev-parse", "--abbrev-ref", "HEAD") or None
    if branch == "HEAD":
        branch = "(detached)"
    return {
        "name": name,
        "version": read_version(path),
        "commit": commit,
        "short": short,
        "branch": branch,
    }


def render_markdown(rows: list[dict[str, str | None]]) -> str:
    lines = [
        "| Submodule | Version | Commit | Branch |",
        "|-----------|---------|--------|--------|",
    ]
    for row in rows:
        if row.get("error"):
            lines.append(f"| {row['name']} | — | — | _{row['error']}_ |")
            continue
        lines.append(
            f"| {row['name']} | {row.get('version') or '—'} | "
            f"`{row.get('short') or '—'}` | {row.get('branch') or '—'} |"
        )
    return "\n".join(lines) + "\n"


def main(argv: list[str]) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown.")
    p.add_argument(
        "--out", type=pathlib.Path, help="Write output to this file instead of stdout."
    )
    args = p.parse_args(argv)

    rows = [snapshot_one(name, path) for name, path in discover_submodules()]

    if args.json:
        payload = json.dumps(rows, indent=2)
    else:
        payload = render_markdown(rows)

    if args.out:
        args.out.write_text(payload, encoding="utf-8")
        print(f"Wrote {args.out}")
    else:
        sys.stdout.write(payload)
        if not payload.endswith("\n"):
            sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
