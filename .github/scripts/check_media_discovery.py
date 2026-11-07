#!/usr/bin/env python3
"""Smoke-test local media installation; opt in to a native implicit Codex read."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


ROOT = Path(__file__).resolve().parents[2]
SKILLS = [
    'flutter-media', 'flutter-networking', 'flutter-platform-integration',
    'flutter-app-workflow', 'dart-concurrency', 'flutter-testing',
]
PROMPT = (
    'Plan a focused fix for a Flutter video player that uses its existing SDK. '
    'Opening source A is slow; source B becomes ready first; then A returns '
    'after the user has left the page. A successful open creates an owned player '
    'controller. Explain source ownership, resource cleanup, and verification '
    'without changing packages or writing code. There is no live media or target '
    'device in this project. Read local guidance if relevant; do not use the '
    'network, operate hardware, or modify files.'
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='invoke Codex once with a prompt that names no skill')
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    result: dict = {'source': 'local checkout', 'installed_skills': SKILLS, 'native_execution': False}
    with tempfile.TemporaryDirectory(prefix='flutter-media-discovery-') as directory:
        workspace = Path(directory)
        command = [
            shutil.which('node'), str(ROOT / 'node_modules/skills/bin/cli.mjs'),
            'add', str(ROOT), '--skill', *SKILLS, '--agent', 'codex', '--yes',
        ]
        install = subprocess.run(command, cwd=workspace, text=True, capture_output=True, timeout=120, check=True)
        result['installation'] = {'command': command, 'stdout': install.stdout, 'stderr': install.stderr}
        installed = workspace / '.agents/skills/flutter-media/SKILL.md'
        source = ROOT / 'skills/flutter-media/SKILL.md'
        if not installed.is_file() or installed.read_bytes() != source.read_bytes():
            raise RuntimeError('Installed media entrypoint does not match the checkout')
        result['installed_entrypoint_sha256'] = hashlib.sha256(installed.read_bytes()).hexdigest()
        result['default_implicit_policy'] = not (installed.parent / 'agents/openai.yaml').exists()
        if args.execute:
            response = workspace / 'response.txt'
            command = [
                shutil.which('codex'), 'exec', '--ephemeral', '--skip-git-repo-check',
                '--ignore-user-config', '--ignore-rules', '--sandbox', 'read-only',
                '--cd', str(workspace), '--json', '--output-last-message', str(response), '-',
            ]
            completed = subprocess.run(command, input=PROMPT, cwd=workspace, text=True, capture_output=True, timeout=180, check=True)
            result.update({
                'native_execution': True, 'prompt': PROMPT, 'command': command,
                'agent_version': subprocess.check_output([shutil.which('codex'), '--version'], text=True).strip(),
                'model': None, 'response': response.read_text(encoding='utf-8'),
                'events': [json.loads(line) for line in completed.stdout.splitlines() if line.strip()],
                'stderr': completed.stderr,
            })
            result['instruction_read_evidence'] = [
                {'command': item['command'], 'exit_code': item['exit_code']}
                for event in result['events']
                for item in [event.get('item', {})]
                if item.get('type') == 'command_execution'
                and item.get('exit_code') == 0
                and 'flutter-media/SKILL.md' in item.get('command', '')
                and 'name: flutter-media' in item.get('aggregated_output', '')
            ]
    result['passed'] = not args.execute or bool(result['instruction_read_evidence'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(f'Installed media skill matches checkout; native execution={args.execute}. Wrote {args.output}')
    return 0 if result['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
