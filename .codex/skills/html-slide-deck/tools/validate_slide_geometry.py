#!/usr/bin/env python3
"""Validate geometry metadata in html-slide-deck templates.

This validator intentionally checks deterministic metadata rather than visual guesswork.
Templates should annotate diagram nodes and arrows with data attributes.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET


@dataclass(frozen=True)
class Box:
    id: str
    x: float
    y: float
    w: float
    h: float

    @property
    def left(self) -> tuple[float, float]:
        return self.x, self.y + self.h / 2

    @property
    def right(self) -> tuple[float, float]:
        return self.x + self.w, self.y + self.h / 2

    @property
    def top(self) -> tuple[float, float]:
        return self.x + self.w / 2, self.y

    @property
    def bottom(self) -> tuple[float, float]:
        return self.x + self.w / 2, self.y + self.h


def _float(value: str | None, default: float = 0) -> float:
    try:
        return float(value or default)
    except ValueError:
        return default


def _strip_html_to_svg(source: str) -> str:
    match = re.search(r"<svg\b.*?</svg>", source, re.S)
    if not match:
        raise ValueError("svg element not found")
    svg = match.group(0)
    svg = re.sub(r"<foreignObject\b.*?</foreignObject>", "", svg, flags=re.S)
    return svg


def _endpoint_from_path(d: str) -> tuple[tuple[float, float], tuple[float, float]]:
    nums = [float(n) for n in re.findall(r"-?\d+(?:\.\d+)?", d)]
    if len(nums) < 4:
        raise ValueError(f"invalid path data: {d}")
    return (nums[0], nums[1]), (nums[-2], nums[-1])


def validate(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if "、" in re.sub(r"<script\b.*?</script>", "", source, flags=re.S):
        errors.append("Japanese comma found")

    root = ET.fromstring(_strip_html_to_svg(source))
    ns = "{http://www.w3.org/2000/svg}"
    boxes: dict[str, Box] = {}

    for rect in root.iter(f"{ns}rect"):
        box_id = rect.attrib.get("data-node")
        if not box_id:
            continue
        boxes[box_id] = Box(
            box_id,
            _float(rect.attrib.get("x")),
            _float(rect.attrib.get("y")),
            _float(rect.attrib.get("width")),
            _float(rect.attrib.get("height")),
        )

    region = Box("content", 80, 315, 1440, 505)
    for box in boxes.values():
        if box.x < region.x or box.y < region.y or box.x + box.w > region.x + region.w or box.y + box.h > region.y + region.h:
            errors.append(f"node out of content region: {box.id}")

    for path_el in root.iter(f"{ns}path"):
        from_id = path_el.attrib.get("data-from")
        to_id = path_el.attrib.get("data-to")
        if not from_id or not to_id:
            continue
        if from_id not in boxes or to_id not in boxes:
            errors.append(f"arrow references unknown node: {from_id}->{to_id}")
            continue
        start, end = _endpoint_from_path(path_el.attrib.get("d", ""))
        expected_start = getattr(boxes[from_id], path_el.attrib.get("data-from-anchor", "right"))
        expected_end = getattr(boxes[to_id], path_el.attrib.get("data-to-anchor", "left"))
        if abs(start[0] - expected_start[0]) > 1 or abs(start[1] - expected_start[1]) > 1:
            errors.append(f"arrow start mismatch: {from_id}->{to_id}")
        if abs(end[0] - expected_end[0]) > 1 or abs(end[1] - expected_end[1]) > 1:
            errors.append(f"arrow end mismatch: {from_id}->{to_id}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    failed = False
    for item in args.files:
        errors = validate(Path(item))
        if errors:
            failed = True
            print(f"FAIL {item}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"PASS {item}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
