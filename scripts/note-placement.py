#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('contents')
SCALAR_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$')
LOCATION_FIELDS = ('directoryId', 'domainId', 'domainName', 'collectionId', 'collectionName', 'order')


def split_document(path: Path) -> tuple[list[str], list[str]]:
    lines = path.read_text(encoding='utf-8').splitlines()
    if not lines or lines[0] != '---':
        raise RuntimeError(f'Front matter is required: {path}')
    try:
        end = lines.index('---', 1)
    except ValueError:
        raise RuntimeError(f'Unclosed front matter: {path}')
    return lines[1:end], lines[end + 1:]


def parse_front(front: list[str]) -> dict[str, str]:
    data: dict[str, str] = {}
    for line in front:
        match = SCALAR_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key] = value
    return data


def is_true(value: str | None) -> bool:
    return (value or '').strip().lower() == 'true'


def format_value(value: str | int | bool) -> str:
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, int):
        return str(value)
    value = str(value)
    if re.fullmatch(r'[A-Za-z0-9_.-]+', value):
        return value
    return json.dumps(value, ensure_ascii=False)


def set_field(front: list[str], key: str, value: str | int | bool | None) -> None:
    index = None
    for i, line in enumerate(front):
        match = SCALAR_RE.match(line)
        if match and match.group(1) == key:
            index = i
            break

    if value is None:
        if index is not None:
            front.pop(index)
        return

    new_line = f'{key}: {format_value(value)}'
    if index is not None:
        front[index] = new_line
        return

    preferred_before = {
        'directoryId': ('domainId',),
        'placementLocked': ('domainId',),
        'order': ('chapter', 'directoryId', 'domainId'),
    }
    for anchor in preferred_before.get(key, ()):
        for i, line in enumerate(front):
            match = SCALAR_RE.match(line)
            if match and match.group(1) == anchor:
                front.insert(i, new_line)
                return
    front.append(new_line)


def write_document(path: Path, front: list[str], body: list[str]) -> None:
    path.write_text('\n'.join(['---', *front, '---', *body]) + '\n', encoding='utf-8')


def load_pages() -> list[tuple[Path, list[str], dict[str, str], list[str]]]:
    pages = []
    for path in ROOT.rglob('*.md'):
        try:
            front, body = split_document(path)
        except RuntimeError:
            continue
        fm = parse_front(front)
        if fm.get('id'):
            pages.append((path, front, fm, body))
    return pages


def find_note(pages, note_id: str):
    matches = [page for page in pages if page[2].get('id') == note_id and page[2].get('type') != 'Directory']
    if not matches:
        raise RuntimeError(f'Note not found: {note_id}')
    if len(matches) > 1:
        raise RuntimeError(f'Duplicate Note id: {note_id}')
    return matches[0]


def find_directory(pages, directory_id: str):
    matches = [page for page in pages if page[2].get('id') == directory_id and page[2].get('type') == 'Directory']
    if not matches:
        raise RuntimeError(f'Directory not found: {directory_id}')
    if len(matches) > 1:
        raise RuntimeError(f'Duplicate Directory id: {directory_id}')
    return matches[0]


def find_collection_reference(pages, domain_id: str, collection_id: str):
    matches = [
        page for page in pages
        if page[2].get('domainId') == domain_id
        and page[2].get('collectionId') == collection_id
        and page[2].get('domainName')
        and page[2].get('collectionName')
    ]
    if not matches:
        raise RuntimeError(
            f'No existing page can define target collection metadata: '
            f'domainId={domain_id}, collectionId={collection_id}'
        )
    return matches[0][2]


def next_order(pages, note_id: str, location: dict[str, str]) -> int:
    values: list[int] = []
    target_directory = location.get('directoryId') or ''
    for _, _, fm, _ in pages:
        if fm.get('id') == note_id:
            continue
        same = False
        if target_directory:
            same = (fm.get('directoryId') or '') == target_directory
        else:
            same = (
                not fm.get('directoryId')
                and fm.get('domainId') == location.get('domainId')
                and fm.get('collectionId') == location.get('collectionId')
            )
        if not same:
            continue
        try:
            values.append(int(fm.get('order', '')))
        except ValueError:
            pass
    return (max(values) + 10) if values else 10


def run_validator() -> None:
    result = subprocess.run([sys.executable, 'scripts/validate-directories.py'])
    if result.returncode:
        raise RuntimeError('Placement change was written, but validation failed. Fix or revert the change before committing.')


def location_text(fm: dict[str, str]) -> str:
    parent = fm.get('directoryId') or '<category root>'
    return (
        f'parent={parent}, domain={fm.get("domainId")}, '
        f'collection={fm.get("collectionId")}, order={fm.get("order")}'
    )


def command_status(args) -> None:
    pages = load_pages()
    _, _, fm, _ = find_note(pages, args.id)
    print(f'{args.id}: {location_text(fm)}, placementLocked={str(is_true(fm.get("placementLocked"))).lower()}')


def command_lock(args) -> None:
    pages = load_pages()
    path, front, fm, body = find_note(pages, args.id)
    if is_true(fm.get('placementLocked')):
        print(f'{args.id} is already placement-locked.')
        return
    set_field(front, 'placementLocked', True)
    write_document(path, front, body)
    run_validator()
    print(f'Locked {args.id} at {location_text(parse_front(front))}')


def command_unlock(args) -> None:
    pages = load_pages()
    path, front, fm, body = find_note(pages, args.id)
    if not is_true(fm.get('placementLocked')):
        print(f'{args.id} is already unlocked.')
        return
    set_field(front, 'placementLocked', False)
    write_document(path, front, body)
    run_validator()
    print(
        f'Unlocked {args.id} without moving it. Commit this unlock first; '
        f'the placement validator intentionally rejects unlock+move in one commit.'
    )


def command_move(args) -> None:
    pages = load_pages()
    path, front, fm, body = find_note(pages, args.id)
    if is_true(fm.get('placementLocked')):
        raise RuntimeError(
            f'{args.id} is placement-locked. Run `python3 scripts/note-placement.py unlock {args.id}`, '
            f'commit that unlock, then move it in a later commit.'
        )

    target = dict(fm)
    if args.directory:
        _, _, directory, _ = find_directory(pages, args.directory)
        target['directoryId'] = args.directory
        for field in ('domainId', 'domainName', 'collectionId', 'collectionName'):
            if not directory.get(field):
                raise RuntimeError(f'Target Directory {args.directory} is missing {field}')
            target[field] = directory[field]
    else:
        target.pop('directoryId', None)
        target_domain = args.domain or fm.get('domainId')
        target_collection = args.collection or fm.get('collectionId')
        if not target_domain or not target_collection:
            raise RuntimeError('Root placement needs domainId and collectionId metadata')
        reference = find_collection_reference(pages, target_domain, target_collection)
        target['domainId'] = target_domain
        target['domainName'] = reference['domainName']
        target['collectionId'] = target_collection
        target['collectionName'] = reference['collectionName']

    target_order = args.order if args.order is not None else next_order(pages, args.id, target)
    target['order'] = str(target_order)

    if args.directory:
        set_field(front, 'directoryId', target['directoryId'])
    else:
        set_field(front, 'directoryId', None)

    for field in ('domainId', 'domainName', 'collectionId', 'collectionName'):
        set_field(front, field, target[field])
    set_field(front, 'order', target_order)
    if args.lock:
        set_field(front, 'placementLocked', True)

    write_document(path, front, body)
    run_validator()
    updated = parse_front(front)
    print(f'Moved {args.id}: {location_text(updated)}')
    if args.lock:
        print('The new placement is locked in the same commit.')


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description='Move Learn notes between category roots and nested Directories, or lock/unlock their placement.'
    )
    sub = parser.add_subparsers(dest='command', required=True)

    status = sub.add_parser('status', help='Show the current placement and lock state.')
    status.add_argument('id')
    status.set_defaults(func=command_status)

    lock = sub.add_parser('lock', help='Lock the current placement.')
    lock.add_argument('id')
    lock.set_defaults(func=command_lock)

    unlock = sub.add_parser('unlock', help='Unlock placement without moving. Commit this separately before a move.')
    unlock.add_argument('id')
    unlock.set_defaults(func=command_unlock)

    move = sub.add_parser('move', help='Move an unlocked Note.')
    move.add_argument('id')
    target = move.add_mutually_exclusive_group(required=True)
    target.add_argument('--directory', help='Target Directory id, including nested Directories.')
    target.add_argument('--root', action='store_true', help='Move to a category/collection root.')
    move.add_argument('--domain', help='Target domainId for --root. Defaults to the current domain.')
    move.add_argument('--collection', help='Target collectionId for --root. Defaults to the current collection.')
    move.add_argument('--order', type=int, help='Display order. Defaults to the end of the target location.')
    move.add_argument('--lock', action='store_true', help='Lock the new placement immediately.')
    move.set_defaults(func=command_move)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        args.func(args)
        return 0
    except RuntimeError as exc:
        print(f'error: {exc}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
