#!/usr/bin/env python3
from pathlib import Path
import re

ROOT = Path('contents')
SCALAR_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$')
REQUIRED_NOTE = ('id','permalink','title','description','type','order','domainId','domainName')


def parse(path: Path) -> dict[str,str]:
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0] != '---':
        return {}
    try:
        end = lines.index('---', 1)
    except ValueError:
        raise RuntimeError(f'Unclosed front matter: {path}')
    out = {}
    for line in lines[1:end]:
        m = SCALAR_RE.match(line)
        if not m:
            continue
        key, value = m.groups()
        value = value.strip().strip('"').strip("'")
        out[key] = value
    return out


def is_true_false_or_empty(value: str | None) -> bool:
    return not value or value.lower() in {'true','false'}


errors=[]
ids={}
permalinks={}
count=0
root_count=0
collection_count=0
for path in ROOT.rglob('*.md'):
    fm=parse(path)
    if not fm.get('id'):
        continue
    if fm.get('type') == 'Directory':
        continue
    count += 1

    for field in REQUIRED_NOTE:
        if not fm.get(field):
            errors.append(f'{path}: missing required Note field {field}')

    if fm.get('type') and fm.get('type') != 'Note':
        errors.append(f'{path}: type must be Note, got {fm.get("type")!r}')

    domain_id = fm.get('domainId')
    if len(path.parts) < 3:
        errors.append(f'{path}: Note source must stay under contents/<domain>/...')
    elif domain_id and path.parts[1] != domain_id:
        errors.append(f'{path}: source domain {path.parts[1]!r} does not match domainId {domain_id!r}')

    permalink = fm.get('permalink')
    if permalink and domain_id and not permalink.startswith(f'/{domain_id}/'):
        errors.append(f'{path}: permalink {permalink!r} must stay under /{domain_id}/')

    collection_id = fm.get('collectionId')
    collection_name = fm.get('collectionName')
    if bool(collection_id) != bool(collection_name):
        errors.append(f'{path}: collectionId and collectionName must either both exist or both be omitted')

    if fm.get('directoryId') and not collection_id:
        errors.append(f'{path}: Directory member Note must keep collectionId / collectionName')

    if collection_id:
        collection_count += 1
    else:
        root_count += 1

    try:
        int(fm.get('order',''))
    except ValueError:
        errors.append(f'{path}: order must be an integer, got {fm.get("order")!r}')

    if not is_true_false_or_empty(fm.get('placementLocked')):
        errors.append(f'{path}: placementLocked must be true or false')

    note_id=fm.get('id')
    if note_id:
        if note_id in ids:
            errors.append(f'Duplicate Note id {note_id}: {ids[note_id]} and {path}')
        ids[note_id]=path

    if permalink:
        if permalink in permalinks:
            errors.append(f'Duplicate permalink {permalink}: {permalinks[permalink]} and {path}')
        permalinks[permalink]=path

if errors:
    raise RuntimeError('Content metadata validation failed:\n- ' + '\n- '.join(errors))
print(f'Content metadata OK: {count} Notes checked ({root_count} domain-root, {collection_count} collection-scoped).')
