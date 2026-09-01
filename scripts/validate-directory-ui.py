#!/usr/bin/env python3
from __future__ import annotations

from html import unescape
from pathlib import Path
import re
import sys

SITE = Path("_site")
errors: list[str] = []
checked = 0

for path in sorted(SITE.rglob("*.html")):
    raw = path.read_text(encoding="utf-8", errors="replace")
    if "directory-main" not in raw:
        continue
    checked += 1
    visible = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    visible = re.sub(r"(?s)<[^>]+>", " ", visible)
    visible = unescape(re.sub(r"\s+", " ", visible))
    if re.search(r"\bDIRECTORY\b|\bDirectory\b", visible):
        errors.append(f"{path}: visible Directory type wording remains")

if errors:
    print("Directory UI validation failed:", file=sys.stderr)
    for error in errors:
        print(f"- {error}", file=sys.stderr)
    raise SystemExit(1)

if checked == 0:
    print("Directory UI validation OK: no Directory pages exist in this repository.")
else:
    print(f"Directory UI validation OK: {checked} rendered directory pages contain no visible Directory type labels.")
