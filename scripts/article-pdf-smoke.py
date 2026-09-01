#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import html
import re
import shutil
import socket
import subprocess
import sys
import time

ROOT = Path('_site')
ARTIFACTS = Path('_layout-smoke-artifacts')
PORT = 8767


def find_chrome() -> str:
    for name in ('google-chrome', 'google-chrome-stable', 'chromium', 'chromium-browser'):
        path = shutil.which(name)
        if path:
            return path
    raise RuntimeError('Chrome/Chromium is required for PDF smoke testing')


def require_tool(name: str) -> str:
    path = shutil.which(name)
    if not path:
        raise RuntimeError(f'{name} is required for PDF smoke testing')
    return path


def wait_for_server(port: int) -> None:
    deadline = time.time() + 10
    while time.time() < deadline:
        try:
            with socket.create_connection(('127.0.0.1', port), timeout=0.25):
                return
        except OSError:
            time.sleep(0.1)
    raise RuntimeError('Local _site server did not start')


def clean_text(value: str) -> str:
    value = re.sub(r'<script\b[^>]*>.*?</script>', ' ', value, flags=re.S | re.I)
    value = re.sub(r'<style\b[^>]*>.*?</style>', ' ', value, flags=re.S | re.I)
    value = re.sub(r'<[^>]+>', ' ', value)
    return re.sub(r'\s+', ' ', html.unescape(value)).strip()


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == 'index.html':
        return '/'
    if rel.endswith('/index.html'):
        return '/' + rel[:-len('index.html')]
    return '/' + rel


def validate_rendered_sources() -> tuple[int, str, str, str | None]:
    articles: list[tuple[Path, str]] = []
    preferred: tuple[Path, str, str, str] | None = None
    fallback: tuple[Path, str, str] | None = None

    for path in sorted(ROOT.rglob('*.html')):
        text = path.read_text(encoding='utf-8', errors='replace')
        if 'class="content"' not in text:
            continue
        articles.append((path, text))
        if 'id="article-pdf-export"' not in text:
            raise RuntimeError(f'PDF export button missing from article: {path}')

        title_match = re.search(r'<h1[^>]*>(.*?)</h1>', text, re.S | re.I)
        title = clean_text(title_match.group(1)) if title_match else ''
        if not title:
            continue
        if fallback is None:
            fallback = (path, text, title)

        details_match = re.search(r'<details\b[^>]*>(.*?)</details>', text, re.S | re.I)
        if not details_match:
            continue
        details_body = re.sub(r'<summary\b[^>]*>.*?</summary>', ' ', details_match.group(1), count=1, flags=re.S | re.I)
        details_text = clean_text(details_body)
        tokens = re.findall(r'[A-Za-z0-9_\-\u3040-\u30ff\u3400-\u9fff]{6,}', details_text)
        if tokens:
            preferred = (path, text, title, tokens[0])
            break

    if not articles:
        raise RuntimeError('No article pages found for PDF validation')
    if preferred:
        path, _text, title, details_token = preferred
        return len(articles), url_for(path), title, details_token
    if fallback:
        path, _text, title = fallback
        return len(articles), url_for(path), title, None
    raise RuntimeError('No article with a readable title was found for PDF validation')


def main() -> int:
    if not ROOT.exists():
        raise RuntimeError('_site does not exist; run npm run build first')

    article_count, target, title, details_token = validate_rendered_sources()
    chrome = find_chrome()
    pdftotext = require_tool('pdftotext')
    pdfinfo = require_tool('pdfinfo')
    pdftoppm = require_tool('pdftoppm')

    ARTIFACTS.mkdir(exist_ok=True)
    pdf_path = (ARTIFACTS / 'article-content-only.pdf').resolve()
    png_prefix = (ARTIFACTS / 'article-content-only-page1').resolve()
    pdf_path.unlink(missing_ok=True)

    server = subprocess.Popen(
        [sys.executable, '-m', 'http.server', str(PORT), '--bind', '127.0.0.1', '--directory', str(ROOT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    try:
        wait_for_server(PORT)
        result = subprocess.run(
            [
                chrome,
                '--headless=new',
                '--no-sandbox',
                '--disable-gpu',
                '--no-pdf-header-footer',
                '--virtual-time-budget=15000',
                f'--print-to-pdf={pdf_path}',
                f'http://127.0.0.1:{PORT}{target}',
            ],
            capture_output=True,
            text=True,
            timeout=45,
            check=False,
        )
        if result.returncode != 0 or not pdf_path.exists() or pdf_path.stat().st_size < 10_000:
            raise RuntimeError(f'Chrome PDF generation failed: rc={result.returncode}\n{result.stderr[-4000:]}')

        text_result = subprocess.run([pdftotext, str(pdf_path), '-'], capture_output=True, text=True, timeout=20, check=True)
        text = re.sub(r'\s+', ' ', text_result.stdout).strip()
        compact = re.sub(r'\s+', '', text_result.stdout)
        if title not in text:
            raise RuntimeError(f'PDF is missing article title: {title}')
        if details_token and details_token not in compact:
            raise RuntimeError(f'PDF is missing content from a closed details block: {details_token}')
        for forbidden in ['Libraryへ戻る', '状態確認中', '変更履歴', 'PDF出力']:
            if forbidden in text:
                raise RuntimeError(f'PDF contains UI that should be excluded: {forbidden}')

        info = subprocess.run([pdfinfo, str(pdf_path)], capture_output=True, text=True, timeout=20, check=True).stdout
        if 'A4' not in info:
            raise RuntimeError(f'PDF page size is not A4:\n{info}')

        subprocess.run(
            [pdftoppm, '-f', '1', '-singlefile', '-png', '-r', '150', str(pdf_path), str(png_prefix)],
            capture_output=True,
            text=True,
            timeout=30,
            check=True,
        )
        png_path = Path(f'{png_prefix}.png')
        if not png_path.exists() or png_path.stat().st_size < 10_000:
            raise RuntimeError('PDF first-page render was not produced')
    finally:
        server.terminate()
        try:
            server.wait(timeout=5)
        except subprocess.TimeoutExpired:
            server.kill()

    details_note = ' and includes closed-toggle content' if details_token else ''
    print(f'Article PDF smoke OK: {article_count} article pages expose PDF export; {target} is A4, content-only{details_note}.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
