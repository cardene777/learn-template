#!/usr/bin/env python3
"""Validate generated HTML slide SVG geometry.

This validator is intentionally strict for template authoring.
It checks nodes against regions and checks text against its owner node.
"""
from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from xml.etree import ElementTree as ET

CONTENT = (80.0, 315.0, 1440.0, 505.0)

@dataclass(frozen=True)
class Box:
    x: float
    y: float
    w: float
    h: float

    @property
    def right(self) -> float:
        return self.x + self.w

    @property
    def bottom(self) -> float:
        return self.y + self.h

    def contains(self, other: "Box", pad: float = 0.0) -> bool:
        return (
            other.x >= self.x + pad and
            other.y >= self.y + pad and
            other.right <= self.right - pad and
            other.bottom <= self.bottom - pad
        )


def nsless(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def num(el: ET.Element, attr: str) -> float:
    value = el.attrib.get(attr)
    if value is None:
        raise ValueError(f"missing {attr}")
    return float(value)


def approx_width(text: str, size: float) -> float:
    width = 0.0
    for ch in text:
        if ch.isspace():
            width += size * 0.32
        elif ord(ch) < 128:
            width += size * 0.58
        else:
            width += size * 0.95
    return width


def extract_font_size(cls: str | None) -> float:
    if cls is None:
        return 16.0
    if "Title" in cls:
        return 22.0
    if "Sub" in cls:
        return 15.0
    if "Mono" in cls:
        return 12.0
    if "caption" in cls:
        return 13.0
    return 16.0


def parse_path_points(d: str) -> tuple[tuple[float, float], tuple[float, float]]:
    nums = [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", d)]
    if len(nums) < 4:
        raise ValueError(f"invalid path {d}")
    return (nums[0], nums[1]), (nums[-2], nums[-1])


def anchor(box: Box, name: str) -> tuple[float, float]:
    if name == "left":
        return box.x, box.y + box.h / 2
    if name == "right":
        return box.right, box.y + box.h / 2
    if name == "top":
        return box.x + box.w / 2, box.y
    if name == "bottom":
        return box.x + box.w / 2, box.bottom
    raise ValueError(f"unknown anchor {name}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html")
    args = parser.parse_args()
    raw = Path(args.html).read_text(encoding="utf-8")

    errors: list[str] = []
    if "、" in raw:
        errors.append("Japanese comma found")

    svgs = re.findall(r"<svg[\s\S]*?</svg>", raw)
    if not svgs:
        errors.append("No SVG found")
        print("FAIL")
        print("\n".join(errors))
        return 1

    for si, svg in enumerate(svgs):
        root = ET.fromstring(svg)
        nodes: dict[str, Box] = {}
        zones: dict[str, Box] = {"content": Box(*CONTENT)}

        for el in root.iter():
            if nsless(el.tag) != "rect":
                continue
            box = Box(num(el, "x"), num(el, "y"), num(el, "width"), num(el, "height"))
            zone_name = el.attrib.get("data-zone")
            node_name = el.attrib.get("data-node")
            if zone_name:
                zones[zone_name] = box
            if node_name:
                nodes[node_name] = box
                zone_ref = el.attrib.get("data-zone-ref", "content")
                if zone_ref in zones and not zones[zone_ref].contains(box, 0):
                    errors.append(f"svg{si}:{node_name} outside zone {zone_ref}")

        for el in root.iter():
            if nsless(el.tag) != "text":
                continue
            owner = el.attrib.get("data-fit")
            if not owner or owner not in nodes:
                continue
            text = "".join(el.itertext()).strip()
            x = float(el.attrib.get("x", "0"))
            y = float(el.attrib.get("y", "0"))
            size = extract_font_size(el.attrib.get("class"))
            width = approx_width(text, size)
            height = size * 1.25
            # text x is left aligned in authored templates
            box = Box(x, y - height, width, height)
            if not nodes[owner].contains(box, 10):
                errors.append(f"svg{si}:text '{text}' outside node {owner}")

        for el in root.iter():
            if nsless(el.tag) != "path":
                continue
            f = el.attrib.get("data-from")
            t = el.attrib.get("data-to")
            if not f or not t:
                continue
            if f not in nodes or t not in nodes:
                errors.append(f"svg{si}:arrow references missing node")
                continue
            expected_start = anchor(nodes[f], el.attrib.get("data-from-anchor", "right"))
            expected_end = anchor(nodes[t], el.attrib.get("data-to-anchor", "left"))
            actual_start, actual_end = parse_path_points(el.attrib.get("d", ""))
            for label, a, b in [("start", actual_start, expected_start), ("end", actual_end, expected_end)]:
                if abs(a[0] - b[0]) > 0.1 or abs(a[1] - b[1]) > 0.1:
                    errors.append(f"svg{si}:arrow {f}->{t} {label} mismatch")

    if errors:
        print("FAIL")
        print("\n".join(errors))
        return 1
    print("PASS")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
