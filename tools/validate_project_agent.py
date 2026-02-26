#!/usr/bin/env python3
import pathlib, sys
p = pathlib.Path(__file__).resolve().parents[1] / 'PROJECT_AGENT.md'
if not p.exists():
    print('FAIL: PROJECT_AGENT.md missing')
    sys.exit(1)
text = p.read_text(encoding='utf-8', errors='ignore')
required = ['## Execution Focus', '## Mandatory Validation', '## DevOps/Quality']
missing = [r for r in required if r not in text]
if missing:
    print('FAIL: missing sections:', ', '.join(missing))
    sys.exit(1)
print('OK:', p)
