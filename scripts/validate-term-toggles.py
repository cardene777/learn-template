#!/usr/bin/env python3
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
CONTENTS = ROOT / 'contents'
errors: list[str] = []
notes = 0
details_blocks = 0

css = (ROOT / 'assets' / 'article-overrides.css').read_text(encoding='utf-8')
for selector in ('.content details', '.content details > summary'):
    if selector not in css:
        errors.append(f'article-overrides.css missing automatic details style: {selector}')

compiler = ROOT / 'scripts' / 'prepare-astro.mjs'
if not compiler.exists():
    errors.append('scripts/prepare-astro.mjs is required')
else:
    compiler_text = compiler.read_text(encoding='utf-8')
    for required in ('DETAIL_RE', 'details-definition', 'marked.parse'):
        if required not in compiler_text:
            errors.append(f'prepare-astro.mjs missing details compiler contract: {required}')

DETAIL_RE = re.compile(r'<details>\s*\n<summary>(?P<summary>[^\n<>]+)</summary>\s*\n(?P<body>[\s\S]*?)\n</details>')

for path in sorted(CONTENTS.rglob('*.md')):
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---') or text.count('---') < 2:
        continue
    front = text.split('---', 2)[1]
    if 'type: Note' not in front:
        continue
    notes += 1
    rel = path.relative_to(ROOT)

    if '<details class=' in text or '<details style=' in text or '<details id=' in text:
        errors.append(f'{rel}: details must not carry source styling/id attributes')
    if 'markdown=' in text:
        errors.append(f'{rel}: markdown attributes must not be written in source')
    if text.count('<details>') != text.count('</details>'):
        errors.append(f'{rel}: unbalanced details tags')
    if text.count('<summary>') != text.count('</summary>'):
        errors.append(f'{rel}: unbalanced summary tags')

    raw_details_count = text.count('<details>')
    matches = list(DETAIL_RE.finditer(text))
    details_blocks += len(matches)
    if len(matches) != raw_details_count:
        errors.append(f'{rel}: details blocks must use simple <details> + one-line <summary> source syntax')
    for match in matches:
        summary = match.group('summary').strip()
        body = match.group('body').strip()
        if not summary:
            errors.append(f'{rel}: details summary is empty')
        if not body:
            errors.append(f'{rel}: details body is empty for {summary!r}')

if details_blocks == 0:
    errors.append('at least one Note must exercise the details compiler contract')

if errors:
    print('Term toggle validation failed:', file=sys.stderr)
    for error in errors:
        print(f'- {error}', file=sys.stderr)
    raise SystemExit(1)

print(f'Term toggle source validation OK: {notes} Notes checked / {details_blocks} simple details blocks; Astro details compiler is present.')
