from pathlib import Path
import re
import subprocess

ROOT = Path('contents')
SCALAR_RE = re.compile(r'^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*?)\s*$')
LOCK_FIELDS = ('directoryId', 'domainId', 'domainName', 'collectionId', 'collectionName', 'order', 'permalink')


def parse_front_matter_text(text: str, source: str = '<text>') -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0] != '---':
        return {}
    try:
        end = lines.index('---', 1)
    except ValueError:
        raise RuntimeError(f'Unclosed front matter: {source}')
    data: dict[str, str] = {}
    for line in lines[1:end]:
        match = SCALAR_RE.match(line)
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        data[key] = value
    return data


def parse_front_matter(path: Path) -> dict[str, str]:
    return parse_front_matter_text(path.read_text(encoding='utf-8'), str(path))


def is_true(value: str | None) -> bool:
    return (value or '').strip().lower() == 'true'


def git_output(*args: str) -> str | None:
    try:
        return subprocess.check_output(['git', *args], text=True, stderr=subprocess.DEVNULL).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def placement_baseline() -> str | None:
    status = git_output('status', '--porcelain', '--', 'contents')
    if status:
        return 'HEAD'
    return git_output('rev-parse', 'HEAD^')


def load_pages_from_ref(ref: str) -> list[tuple[str, dict[str, str]]]:
    listing = git_output('ls-tree', '-r', '--name-only', ref, '--', 'contents')
    if listing is None:
        return []
    pages: list[tuple[str, dict[str, str]]] = []
    for raw_path in listing.splitlines():
        if not raw_path.endswith('.md'):
            continue
        text = git_output('show', f'{ref}:{raw_path}')
        if text is None:
            continue
        fm = parse_front_matter_text(text, f'{ref}:{raw_path}')
        if fm.get('id'):
            pages.append((raw_path, fm))
    return pages


pages: list[tuple[Path, dict[str, str]]] = []
for path in ROOT.rglob('*.md'):
    fm = parse_front_matter(path)
    if fm.get('id'):
        pages.append((path, fm))

errors: list[str] = []
directories: dict[str, tuple[Path, dict[str, str]]] = {}

for path, fm in pages:
    locked_value = fm.get('placementLocked')
    if locked_value and locked_value.lower() not in {'true', 'false'}:
        errors.append(f'{path}: placementLocked must be true or false, got {locked_value!r}')

    if fm.get('layout'):
        errors.append(f'{path}: legacy Jekyll layout front matter is not allowed under Astro')

    if fm.get('type') != 'Directory':
        continue
    directory_id = fm['id']
    if directory_id in directories:
        errors.append(f'Duplicate Directory id {directory_id}: {directories[directory_id][0]} and {path}')
        continue
    directories[directory_id] = (path, fm)
    for field in ('permalink', 'title', 'description', 'domainId', 'collectionId', 'collectionName'):
        if not fm.get(field):
            errors.append(f'Directory {directory_id} is missing {field}: {path}')
    permalink = fm.get('permalink') or ''
    if not (permalink.startswith('/') and permalink.endswith('/')):
        errors.append(f'Directory {directory_id} permalink must start and end with /: {path}')

member_counts = {directory_id: 0 for directory_id in directories}
for path, fm in pages:
    directory_id = fm.get('directoryId')
    if not directory_id:
        continue
    target = directories.get(directory_id)
    if not target:
        errors.append(f'Unknown directoryId {directory_id}: {path}')
        continue
    member_counts[directory_id] += 1
    _, directory = target
    for field in ('domainId', 'collectionId', 'collectionName'):
        if fm.get(field) != directory.get(field):
            errors.append(f'{path}: {field}={fm.get(field)!r} does not match Directory {directory_id} {field}={directory.get(field)!r}')

for directory_id, (path, fm) in directories.items():
    parent_id = fm.get('directoryId')
    if parent_id == directory_id:
        errors.append(f'Directory {directory_id} cannot contain itself: {path}')
        continue
    seen = {directory_id}
    current = parent_id
    while current:
        if current in seen:
            errors.append(f'Directory cycle detected at {directory_id}: {path}')
            break
        seen.add(current)
        parent = directories.get(current)
        if not parent:
            break
        current = parent[1].get('directoryId')

baseline = placement_baseline()
locked_checked = 0
if baseline:
    previous_pages = load_pages_from_ref(baseline)
    current_by_id: dict[str, list[tuple[Path, dict[str, str]]]] = {}
    for item in pages:
        current_by_id.setdefault(item[1]['id'], []).append(item)

    for previous_path, previous in previous_pages:
        if previous.get('type') == 'Directory' or not is_true(previous.get('placementLocked')):
            continue
        locked_checked += 1
        note_id = previous['id']
        matches = current_by_id.get(note_id, [])
        if not matches:
            errors.append(f'Locked Note {note_id} was removed or its id changed. Unlock it in a separate commit before removing/renaming it: {previous_path}')
            continue
        if len(matches) != 1:
            errors.append(f'Locked Note {note_id} resolves to multiple current files')
            continue

        current_path, current = matches[0]
        changed = [field for field in LOCK_FIELDS if (previous.get(field) or '') != (current.get(field) or '')]
        if changed:
            details = ', '.join(f'{field}: {previous.get(field)!r} -> {current.get(field)!r}' for field in changed)
            errors.append(
                f'Placement lock violation for {note_id}: {details}. First commit placementLocked: false without moving the Note, then move it in a later commit. Current file: {current_path}'
            )

if errors:
    raise RuntimeError('Directory/placement validation failed:\n- ' + '\n- '.join(errors))

note_count = sum(1 for _, fm in pages if fm.get('directoryId') and fm.get('type') != 'Directory')
nested_count = sum(1 for _, fm in pages if fm.get('directoryId') and fm.get('type') == 'Directory')
locked_notes = sorted(
    ((fm['id'], path, fm) for path, fm in pages if fm.get('type') != 'Directory' and is_true(fm.get('placementLocked'))),
    key=lambda item: item[0],
)
print(f'Validated {len(directories)} directories, {nested_count} nested directories, {note_count} directory member notes, and {len(locked_notes)} placement-locked notes.')
if baseline:
    print(f'Placement lock baseline: {baseline} ({locked_checked} previously locked notes checked).')
if locked_notes:
    print('Active placement locks:')
    for note_id, path, fm in locked_notes:
        parent = fm.get('directoryId') or '<category root>'
        print(f'  🔒 {note_id}: parent={parent}, order={fm.get("order")}, permalink={fm.get("permalink")}, source={path}')
else:
    print('Active placement locks: none. Lock feature is enabled; no Note currently has placementLocked: true.')
for directory_id, count in sorted(member_counts.items()):
    print(f'  {directory_id}: {count} children')
