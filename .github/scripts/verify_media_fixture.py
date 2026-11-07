#!/usr/bin/env python3
"""Check the media ownership oracle and independently seeded failure paths."""

from pathlib import Path
import shutil
import tempfile

from verify_responsive_fixture import check


ROOT = Path(__file__).resolve().parents[2]
EXECUTABLE = ROOT / '.github/evals/executable'
FIXTURE = EXECUTABLE / 'fixtures/media-source-ownership'
ORACLE = EXECUTABLE / 'oracles/media-source-ownership/media_source_owner.dart'


def main() -> None:
    with tempfile.TemporaryDirectory(prefix='media-fixture-proof-') as directory:
        workspace = Path(directory) / 'player'
        shutil.copytree(FIXTURE, workspace)
        source = workspace / 'lib/media_source_owner.dart'
        command = ['dart', 'run', 'bin/verify.dart']
        check(workspace, ['dart', 'analyze', 'lib', 'bin'])
        check(workspace, command, fails_with='Stale source replaced latest')
        print('Seeded stale source: caught')
        shutil.copy2(ORACLE, source)
        check(workspace, ['dart', 'format', '--output=none', '--set-exit-if-changed', 'lib', 'bin'])
        check(workspace, ['dart', 'analyze', 'lib', 'bin'])
        check(workspace, command)
        print('Corrected fake-player owner: 6 scenarios passed')
        original = source.read_text(encoding='utf-8')
        mutations = [
            ('stale handle leak', '      await handle.close();\n      return;', '      return;', 'Stale successful handle was not released'),
            ('pending stop revival', '    _generation++;\n    final handle = current;', '    final handle = current;', 'Stopped owner revived from pending open'),
            ('replacement leak', '    await previous?.close();', '    if (previous == null) return;', 'Replaced active handle leaked'),
            ('concurrent stop ownership', '    current = null;\n    await handle?.close();', '    await handle?.close();\n    current = null;', 'Duplicate close'),
            ('failed close ownership', '    await handle?.close();', '    try {\n      await handle?.close();\n    } catch (_) {\n      current = handle;\n      rethrow;\n    }', 'Failed close left handle current'),
        ]
        for label, old, new, marker in mutations:
            if original.count(old) != 1:
                raise AssertionError(f'{label} mutation no longer matches the oracle')
            source.write_text(original.replace(old, new), encoding='utf-8')
            check(workspace, command, fails_with=marker)
            print(f'Seeded {label}: caught')


if __name__ == '__main__':
    main()
