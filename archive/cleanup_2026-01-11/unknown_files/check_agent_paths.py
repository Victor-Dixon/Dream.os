#!/usr/bin/env python3
"""
Check Agent Paths - Verify inbox and devlog paths for all agents
"""

import os
from pathlib import Path

agents = ['Agent-1', 'Agent-2', 'Agent-3', 'Agent-4', 'Agent-5', 'Agent-6', 'Agent-7', 'Agent-8']
base_path = Path('agent_workspaces')

print('Agent Inbox/Devlog Path Verification:')
print('=' * 50)

all_good = True

for agent in agents:
    inbox_path = base_path / agent / 'inbox'
    devlog_path = base_path / agent / 'devlog.md'

    # Check inbox directory
    inbox_exists = inbox_path.exists()
    inbox_writable = False
    if inbox_exists:
        try:
            test_file = inbox_path / 'test_write.tmp'
            test_file.write_text('test')
            test_file.unlink()
            inbox_writable = True
        except Exception as e:
            print(f"  Inbox write test failed: {e}")
            inbox_writable = False
    else:
        all_good = False

    # Check devlog file
    devlog_exists = devlog_path.exists()
    devlog_writable = False
    if devlog_exists:
        try:
            with open(devlog_path, 'a') as f:
                f.write('')
            devlog_writable = True
        except Exception as e:
            print(f"  Devlog write test failed: {e}")
            devlog_writable = False
    else:
        # Try to create devlog
        try:
            devlog_path.parent.mkdir(parents=True, exist_ok=True)
            devlog_path.write_text('# Devlog\n\n')
            devlog_writable = True
            devlog_exists = True
            print(f"  Created devlog.md for {agent}")
        except Exception as e:
            print(f"  Devlog creation failed for {agent}: {e}")
            devlog_writable = False
            all_good = False

    status = "✅" if (inbox_exists and inbox_writable and devlog_exists and devlog_writable) else "❌"
    print(f'{agent}: {status}')
    print(f'  Inbox: {"✅" if inbox_exists else "❌"} exists, {"✅" if inbox_writable else "❌"} writable')
    print(f'  Devlog: {"✅" if devlog_exists else "❌"} exists, {"✅" if devlog_writable else "❌"} writable')
    print()

print(f'Overall Status: {"✅ ALL GOOD" if all_good else "❌ ISSUES FOUND"}')