#!/usr/bin/env python3
"""Create PR for DigitalDreamscape merge."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))
from tools.merge_prs_via_api import get_github_token, create_pr

token = get_github_token()
pr = create_pr(
    token,
    'Dadudekc',
    'DreamVault',
    'Merge DigitalDreamscape into DreamVault',
    '''Repository Consolidation Merge

**Source**: DigitalDreamscape
**Target**: DreamVault

This merge is part of Batch 2 repository consolidation.

**Executed by**: Agent-1 (Integration & Core Systems Specialist)
**Method**: Simple git clone to D:/Temp
**Branch**: merge-DigitalDreamscape-20251130''',
    'merge-DigitalDreamscape-20251130',
    'master'  # Try master instead of main
)

if pr:
    print(f"✅ PR created: {pr.get('html_url')}")
else:
    print("❌ PR creation failed")
