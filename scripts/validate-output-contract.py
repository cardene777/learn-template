#!/usr/bin/env python3
from pathlib import Path
import re

SOURCE_ROOT = Path('contents')
OUTPUT_ROOT = Path('_site')
STATIC_PAGES = {
    'index.html',
    'commerce/index.html',
    'identity/index.html',
    'payments/index.html',
    'notes/index.html',
}
FRONT_RE = re.compile(r'^---\n(.*?)\n---(?:\n|$)', re.DOTALL)
SCALAR_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$', re.MULTILINE)


def front_matter(path: Path) -> dict[str, str]:
    text = path.read_text(encoding='utf-8')
    match = FRONT_RE.match(text)
    if not match:
        return {}
    data: dict[str, str] = {}
    for key, value in SCALAR_RE.findall(match.group(1)):
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key] = value
    return data


def output_path(permalink: str) -> str:
    clean = permalink.strip()
    if not clean.startswith('/'):
        raise RuntimeError(f'permalink must start with /: {permalink!r}')
    clean = clean.lstrip('/')
    if not clean:
        return 'index.html'
    if clean.endswith('/'):
        return clean + 'index.html'
    return clean


expected = set(STATIC_PAGES)
source_count = 0
errors: list[str] = []

for source in sorted(SOURCE_ROOT.rglob('*.md')):
    fm = front_matter(source)
    if not fm.get('id'):
        continue
    source_count += 1
    permalink = fm.get('permalink')
    if not permalink:
        errors.append(f'{source}: missing permalink')
        continue
    try:
        rendered = output_path(permalink)
    except RuntimeError as exc:
        errors.append(f'{source}: {exc}')
        continue
    if rendered in expected:
        errors.append(f'{source}: duplicate generated target {rendered}')
    expected.add(rendered)

actual = {
    path.relative_to(OUTPUT_ROOT).as_posix()
    for path in OUTPUT_ROOT.rglob('*.html')
}

missing = sorted(expected - actual)
unexpected = sorted(actual - expected)
if missing:
    errors.extend(f'missing generated HTML: {path}' for path in missing)
if unexpected:
    errors.extend(f'unexpected generated HTML: {path}' for path in unexpected)

if errors:
    raise RuntimeError('Generated output contract failed:\n- ' + '\n- '.join(errors))

print(
    f'Generated output contract OK: {len(actual)} HTML pages = '
    f'{source_count} content routes + {len(STATIC_PAGES)} static application routes.'
)
