#!/usr/bin/env python3
"""Dependency-free, heuristic GitHub Actions triage; NOT a YAML/security validator.
Usage: python3 workflow_triage.py .github/workflows --json
Exit codes: 0 = no hints, 1 = review hints, 2 = input/read error.
Only reads local inputs. Never executes workflow content or modifies files.
"""
import argparse
import json
import re
import sys
from pathlib import Path

USES = re.compile(r'^\s*(?:-\s*)?uses\s*:\s*[\"\']?([^\s\"\'#]+)')
WRITE_ALL = re.compile(r'^\s*permissions\s*:\s*[\"\']?write-all(?:[\"\']?\s*(?:#.*)?)$')
PERMISSIONS = re.compile(r'^\s*permissions\s*:')
TRIGGER = re.compile(r'\bpull_request_target\b')
FULL_SHA = re.compile(r'^[0-9a-fA-F]{40}$')
UNTRUSTED = re.compile(r'\$\{\{[^\n}]*github\.event\.(?:pull_request\.(?:title|body|head\.ref)|issue\.(?:title|body)|comment\.body)[^\n}]*\}\}')


def scan(text, label='<text>'):
    lines = text.splitlines()
    findings = []
    def add(rule, line, message):
        findings.append({'file': label, 'line': line, 'rule': rule, 'message': message})
    active = [(i, line) for i, line in enumerate(lines, 1)
              if line.strip() and not line.lstrip().startswith('#')]
    if not any(PERMISSIONS.match(line) for _, line in active):
        add('PERMISSIONS_REVIEW', 1, 'No permissions key recognized. Inspect effective repository/org defaults and declare least privilege. This does not prove write access.')
    for i, line in active:
        if WRITE_ALL.match(line):
            add('WRITE_ALL', i, 'Broad write-all token permissions recognized; scope permissions to individual jobs and required capabilities.')
        if TRIGGER.search(line.split('#', 1)[0]):
            add('TARGET_TRIGGER_REVIEW', i, 'pull_request_target reference recognized. Confirm it is a trigger and trace all untrusted inputs/code; this trigger alone is not a vulnerability.')
        match = USES.match(line)
        if match:
            ref = match.group(1)
            if ref.startswith('./'):
                pass
            elif ref.startswith('docker://'):
                if not re.search(r'@sha256:[0-9a-fA-F]{64}$', ref):
                    add('MUTABLE_IMAGE', i, 'Container action is not recognized as digest-pinned; review provenance and pin a verified digest.')
            else:
                _, sep, revision = ref.rpartition('@')
                if not sep or not FULL_SHA.fullmatch(revision):
                    add('MUTABLE_ACTION', i, 'External action is not recognized as pinned to a full commit SHA. Verify the intended upstream commit before pinning.')
        if UNTRUSTED.search(line):
            add('EVENT_INPUT_REVIEW', i, 'Direct event-input expression recognized. Inspect its context: interpolation into shell code can be dangerous; environment-variable use may be safe when handled correctly.')
    return findings


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('path', type=Path, help='Workflow file or directory; scans .yml and .yaml files recursively')
    parser.add_argument('--json', action='store_true', help='Print machine-readable findings')
    args = parser.parse_args()
    try:
        if args.path.is_symlink():
            raise ValueError('Symlink input is not supported')
        if args.path.is_file():
            files = [args.path]
        elif args.path.is_dir():
            files = sorted(p for p in args.path.rglob('*') if p.suffix.lower() in ('.yml', '.yaml') and p.is_file() and not p.is_symlink())
        else:
            raise ValueError('Input does not exist or is not a regular file/directory')
        if not files:
            raise ValueError('No workflow files found')
        findings = []
        for path in files:
            findings.extend(scan(path.read_text(encoding='utf-8'), str(path)))
    except (OSError, UnicodeError, ValueError) as exc:
        print('Input error: ' + str(exc), file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({'files_scanned': len(files), 'findings': findings, 'method': 'heuristic-text-review'}, indent=2))
    else:
        for finding in findings:
            print('{file}:{line}: {rule}: {message}'.format(**finding))
        print(str(len(files)) + ' file(s), ' + str(len(findings)) + ' review hint(s). No hints does NOT mean secure.')
    return 1 if findings else 0


if __name__ == '__main__':
    sys.exit(main())
