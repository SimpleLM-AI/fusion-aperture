#!/usr/bin/env python3
# Copyright (c) 2026 Fusion Aperture. SPDX-License-Identifier: CC-BY-NC-ND-4.0
"""Confirm SHA-256 of files listed in metadata/hashes.sha256."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "metadata" / "hashes.sha256"


def main() -> int:
    if not MANIFEST.is_file():
        print("missing", MANIFEST)
        return 1
    failed = 0
    checked = 0
    for raw in MANIFEST.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        digest, rel = line.split(None, 1)
        path = ROOT / rel
        checked += 1
        if not path.is_file():
            print("missing file", rel)
            failed += 1
            continue
        got = hashlib.sha256(path.read_bytes()).hexdigest()
        if got != digest:
            print("mismatch", rel)
            print("  expected", digest)
            print("  got     ", got)
            failed += 1
    print(f"checked {checked}, failed {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
