#!/usr/bin/env python3
"""CI wrapper around `sync-shared-meta.py --check`.

Exits non-zero if any submodule's mirrored meta-file disagrees with the
canonical source under `.github/_shared/`. Intended for use in
`submodule-sanity.yml`.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent.parent
GENERATOR = REPO_ROOT / ".github" / "tools" / "sync-shared-meta.py"


def main() -> int:
    if not GENERATOR.is_file():
        print(f"ERROR: missing {GENERATOR}", file=sys.stderr)
        return 1
    result = subprocess.run(
        [sys.executable, str(GENERATOR), "--check"],
        cwd=REPO_ROOT,
    )
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
