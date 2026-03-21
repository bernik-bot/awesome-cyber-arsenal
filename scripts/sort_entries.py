#!/usr/bin/env python3
import re
from pathlib import Path

README = Path("README.md")
TABLE_ROW_RE = re.compile(r"^\|\s*\[(.+?)\]")
TABLE_HEADER_RE = re.compile(r"^\|\s*Name\s*\|")
TABLE_SEP_RE = re.compile(r"^\|[-\s|]+\|$")


def sort_entries():
    content = README.read_text(encoding="utf-8")
    lines = content.splitlines()
    result: list[str] = []
    i = 0
    changed = False

    while i < len(lines):
        if TABLE_HEADER_RE.match(lines[i].strip()):
            result.append(lines[i])
            i += 1
            if i < len(lines) and TABLE_SEP_RE.match(lines[i].strip()):
                result.append(lines[i])
                i += 1

            rows: list[str] = []
            while i < len(lines) and TABLE_ROW_RE.match(lines[i].strip()):
                rows.append(lines[i])
                i += 1

            sorted_rows = sorted(
                rows,
                key=lambda r: (
                    TABLE_ROW_RE.match(r.strip()).group(1).lower()
                    if TABLE_ROW_RE.match(r.strip())
                    else ""
                ),
            )

            if sorted_rows != rows:
                changed = True

            result.extend(sorted_rows)
        else:
            result.append(lines[i])
            i += 1

    if changed:
        README.write_text("\n".join(result) + "\n", encoding="utf-8")
        print("Sorted entries alphabetically")
    else:
        print("Entries already sorted")


if __name__ == "__main__":
    sort_entries()
