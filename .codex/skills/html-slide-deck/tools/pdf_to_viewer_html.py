#!/usr/bin/env python3
"""Convert a PDF into a self-contained PDF-viewer-style HTML slide deck.

The converter is intentionally image-based.
It preserves the source PDF layout exactly and places rendered pages inside the
shared thumbnail-sidebar viewer template.

Usage:
  python tools/pdf_to_viewer_html.py input.pdf output.html --title "Deck Title" --dpi 160

Dependencies:
  - PyMuPDF package name: pymupdf
"""

from __future__ import annotations

import argparse
import base64
import html
from pathlib import Path
from typing import Iterable, Sequence

try:
    import fitz  # PyMuPDF
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "PyMuPDF is required. Install it with `pip install pymupdf`."
    ) from exc


def encode_png(data: bytes) -> str:
    return "data:image/png;base64," + base64.b64encode(data).decode("ascii")


def render_pdf_pages(pdf_path: Path, dpi: int) -> list[str]:
    doc = fitz.open(pdf_path)
    scale = dpi / 72
    matrix = fitz.Matrix(scale, scale)
    images: list[str] = []

    for page in doc:
        pix = page.get_pixmap(matrix=matrix, alpha=False)
        images.append(encode_png(pix.tobytes("png")))

    return images


def read_titles(path: Path | None, total: int) -> list[str]:
    if path is None:
        return [f"Slide {i:02d}" for i in range(1, total + 1)]
    if not path.exists():
        raise SystemExit(f"Titles file not found: {path}")
    titles = [line.strip() for line in path.read_text(encoding="utf-8").splitlines()]
    titles = [title for title in titles if title]
    if len(titles) < total:
        titles.extend(f"Slide {i:02d}" for i in range(len(titles) + 1, total + 1))
    return titles[:total]


def build_items(images: Iterable[str], titles: Sequence[str]) -> tuple[str, str, int]:
    thumbnails: list[str] = []
    pages: list[str] = []
    image_list = list(images)
    total = len(image_list)

    for index, src in enumerate(image_list, start=1):
        page_id = f"page-{index:02d}"
        no = f"{index:02d}"
        title = titles[index - 1] if index - 1 < len(titles) else f"Slide {no}"
        safe_title = html.escape(title)

        thumbnails.append(
            f'''    <a class="thumb" href="#{page_id}">
      <span class="thumb-number">{no}</span>
      <span class="thumb-frame"><img src="{src}" alt="Page {no} thumbnail" /></span>
    </a>'''
        )

        pages.append(
            f'''    <section id="{page_id}" class="page">
      <div class="page-head"><span class="page-title">{safe_title}</span><span class="page-no">{no} / {total:02d}</span></div>
      <div class="page-card"><img src="{src}" alt="{safe_title}" loading="lazy" /></div>
    </section>'''
        )

    return "\n".join(thumbnails), "\n".join(pages), total


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--title", default=None)
    parser.add_argument("--titles-file", type=Path, default=None)
    parser.add_argument("--dpi", type=int, default=160)
    parser.add_argument(
        "--template",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "templates" / "pdf-viewer-slide-deck.html",
    )
    args = parser.parse_args()

    if not args.pdf.exists():
        raise SystemExit(f"PDF not found: {args.pdf}")
    if not args.template.exists():
        raise SystemExit(f"Template not found: {args.template}")

    deck_title = args.title or args.pdf.stem
    template = args.template.read_text(encoding="utf-8")
    images = render_pdf_pages(args.pdf, args.dpi)
    titles = read_titles(args.titles_file, len(images))
    thumbnails, pages, total = build_items(images, titles)

    html_output = (
        template
        .replace("{{DECK_TITLE}}", html.escape(deck_title))
        .replace("{{PAGE_COUNT}}", str(total))
        .replace("{{THUMBNAILS}}", thumbnails)
        .replace("{{PAGES}}", pages)
    )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html_output, encoding="utf-8")


if __name__ == "__main__":
    main()
