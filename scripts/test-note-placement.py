#!/usr/bin/env python3
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]


def run(cwd: Path, *args: str, expect: int = 0):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    if result.returncode != expect:
        raise RuntimeError(
            f'Command failed ({result.returncode}, expected {expect}): {" ".join(args)}\n'
            f'stdout:\n{result.stdout}\nstderr:\n{result.stderr}'
        )
    return result


with tempfile.TemporaryDirectory(prefix='learn-placement-test-') as tmp:
    repo = Path(tmp)
    (repo / 'contents/payments/test').mkdir(parents=True)
    (repo / 'scripts').mkdir()
    shutil.copy2(ROOT / 'scripts/validate-directories.py', repo / 'scripts/validate-directories.py')
    shutil.copy2(ROOT / 'scripts/note-placement.py', repo / 'scripts/note-placement.py')

    (repo / 'contents/payments/test/research-directory.md').write_text(
        '''---
id: test-research
permalink: /payments/test/research/
title: Testリサーチ
description: placement test directory
type: Directory
order: 20
domainId: payments
domainName: Payments
collectionId: test
collectionName: Test
---
''', encoding='utf-8')
    (repo / 'contents/payments/test/note.md').write_text(
        '''---
id: test-note
permalink: /payments/test/note.html
title: Test Note
description: placement test note
type: Note
order: 10
domainId: payments
domainName: Payments
collectionId: test
collectionName: Test
---
body
''', encoding='utf-8')

    run(repo, 'git', 'init', '-q')
    run(repo, 'git', 'config', 'user.email', 'test@example.com')
    run(repo, 'git', 'config', 'user.name', 'placement-test')
    run(repo, 'git', 'add', '.')
    run(repo, 'git', 'commit', '-qm', 'initial')

    run(repo, sys.executable, 'scripts/note-placement.py', 'move', 'test-note', '--directory', 'test-research', '--lock')
    run(repo, 'git', 'add', '.')
    run(repo, 'git', 'commit', '-qm', 'move and lock')

    validator = run(repo, sys.executable, 'scripts/validate-directories.py')
    if 'test-note' not in validator.stdout or 'Active placement locks:' not in validator.stdout:
        raise RuntimeError('Validator did not report the active placement lock')

    note_path = repo / 'contents/payments/test/note.md'
    locked_text = note_path.read_text(encoding='utf-8')

    note_path.write_text(locked_text.replace('directoryId: test-research\n', ''), encoding='utf-8')
    run(repo, sys.executable, 'scripts/validate-directories.py', expect=1)
    run(repo, 'git', 'checkout', '--', str(note_path.relative_to(repo)))

    note_path.write_text(locked_text.replace('/payments/test/note.html', '/payments/test/moved.html'), encoding='utf-8')
    run(repo, sys.executable, 'scripts/validate-directories.py', expect=1)
    run(repo, 'git', 'checkout', '--', str(note_path.relative_to(repo)))

    run(repo, sys.executable, 'scripts/note-placement.py', 'unlock', 'test-note')
    unlocked_text = note_path.read_text(encoding='utf-8')
    note_path.write_text(unlocked_text.replace('directoryId: test-research\n', ''), encoding='utf-8')
    run(repo, sys.executable, 'scripts/validate-directories.py', expect=1)
    note_path.write_text(unlocked_text, encoding='utf-8')
    run(repo, 'git', 'add', '.')
    run(repo, 'git', 'commit', '-qm', 'unlock only')

    run(repo, sys.executable, 'scripts/note-placement.py', 'move', 'test-note', '--root', '--order', '30')
    run(repo, 'git', 'add', '.')
    run(repo, 'git', 'commit', '-qm', 'move after unlock')
    run(repo, sys.executable, 'scripts/validate-directories.py')

print('Note placement lock tests passed, including permalink protection.')
