#!/usr/bin/env python3
"""Fail if any tracked content contains U+2014."""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
EM_DASH = "\u2014"
EXCLUDED_DIRS = {".git"}


def should_skip(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return path.is_symlink() or any(part in EXCLUDED_DIRS for part in rel.parts)


def read_text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None
    except OSError as exc:
        print(f"warning: could not read {path}: {exc}", file=sys.stderr)
        return None


def main() -> int:
    violations: list[tuple[str, int, int, str]] = []

    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or should_skip(path):
            continue

        text = read_text(path)
        if text is None:
            continue

        rel = path.relative_to(ROOT).as_posix()
        for line_number, line in enumerate(text.splitlines(), start=1):
            column = line.find(EM_DASH)
            while column != -1:
                violations.append((rel, line_number, column + 1, line.strip()))
                column = line.find(EM_DASH, column + 1)

    if not violations:
        print("No em dash characters found.")
        return 0

    print("Em dash characters (U+2014) are not allowed.")
    print("Use a comma, colon, parentheses, or a plain hyphen instead.")
    for rel, line_number, column, snippet in violations:
        print(f"::error file={rel},line={line_number},col={column}::Em dash (U+2014) found")
        print(f"{rel}:{line_number}:{column}: {snippet}")

    return 1


if __name__ == "__main__":
    raise SystemExit(main())
