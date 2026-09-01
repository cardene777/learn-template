from pathlib import Path
import re

ROOT = Path('_site')
ARTICLE_HEADER_RE = re.compile(r'<header\s+class="article-library-header".*?</header>', re.DOTALL)
LIBRARY_HEADER_RE = re.compile(r'<header\s+class="library-header".*?</header>', re.DOTALL)


def assert_common_nav(path: Path, text: str) -> None:
    required = ['>Home</a>', '>コマース</a>', '>アイデンティティ</a>', '>決済</a>']
    missing = [item for item in required if item not in text]
    if missing:
        raise RuntimeError(f'Global header nav missing in {path}: {missing}')


def validate_article(path: Path, text: str) -> None:
    headers = ARTICLE_HEADER_RE.findall(text)
    if len(headers) != 1:
        raise RuntimeError(f'Article global header count must be 1: {path} (count={len(headers)})')
    assert_common_nav(path, headers[0])
    for required in ['article-library-header-search', 'article-library-deploy-status']:
        if required not in headers[0]:
            raise RuntimeError(f'Article header contract missing ({required}): {path}')


def validate_library(path: Path, text: str) -> None:
    headers = LIBRARY_HEADER_RE.findall(text)
    if len(headers) != 1:
        raise RuntimeError(f'Library global header count must be 1: {path} (count={len(headers)})')
    assert_common_nav(path, headers[0])
    for required in ['library-header-search', 'library-deploy-status']:
        if required not in headers[0]:
            raise RuntimeError(f'Library header contract missing ({required}): {path}')


article_count = 0
library_count = 0
for path in ROOT.rglob('*.html'):
    text = path.read_text(encoding='utf-8')
    rel = path.relative_to(ROOT).as_posix()
    if 'class="content"' in text:
        validate_article(path, text)
        article_count += 1
        continue
    if 'class="library-body"' in text or 'directory-main' in text or rel in {'index.html', 'commerce/index.html', 'identity/index.html', 'payments/index.html'}:
        validate_library(path, text)
        library_count += 1

if article_count == 0:
    raise RuntimeError('No article pages were validated')
if library_count < 4:
    raise RuntimeError(f'Too few library pages validated: {library_count}')

print(f'Global header validation OK: {article_count} article pages, {library_count} library/directory pages. Validation does not rewrite generated HTML.')
