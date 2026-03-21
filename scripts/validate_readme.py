#!/usr/bin/env python3
import re
import sys
from pathlib import Path

README = Path("README.md")

VALID_MATURITY = {"🟢", "🟡", "🔴"}
VALID_EXTRAS = {"⭐"}
MAX_DESC_LEN = 120
TABLE_ROW_RE = re.compile(
    r"^\|\s*\[(.+?)\]\((.+?)\)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*\[.+?\]\((.+?)\)\s*\|$"
)


def validate():
    content = README.read_text(encoding="utf-8")
    lines = content.splitlines()
    errors: list[str] = []
    table_rows = 0

    for i, line in enumerate(lines, 1):
        if not line.startswith("|") or line.startswith("| Name") or line.startswith("|---"):
            continue

        match = TABLE_ROW_RE.match(line.strip())
        if not match:
            if "|" in line and "[" in line:
                errors.append(f"Line {i}: Malformed table row")
            continue

        table_rows += 1
        name, homepage, desc, maturity_raw, link = match.groups()

        maturity_tokens = set(maturity_raw.strip().split())
        maturity_badge = maturity_tokens & VALID_MATURITY
        unknown_tokens = maturity_tokens - VALID_MATURITY - VALID_EXTRAS

        if not maturity_badge:
            errors.append(f"Line {i} [{name}]: Missing maturity badge")
        if unknown_tokens:
            errors.append(f"Line {i} [{name}]: Unknown badge(s): {unknown_tokens}")

        if len(desc) > MAX_DESC_LEN:
            errors.append(
                f"Line {i} [{name}]: Description too long ({len(desc)} > {MAX_DESC_LEN})"
            )

        if not homepage.startswith("http"):
            errors.append(f"Line {i} [{name}]: Invalid homepage URL: {homepage}")
        if not link.startswith("http"):
            errors.append(f"Line {i} [{name}]: Invalid link URL: {link}")

    if errors:
        print(f"Found {len(errors)} error(s):\n")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)

    print(f"Validated {table_rows} entries with no errors")


if __name__ == "__main__":
    validate()
