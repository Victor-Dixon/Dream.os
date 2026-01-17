#!/usr/bin/env python3
"""
Targeted Discord Commander Import Fix
====================================

Fixes only the Discord commander absolute imports that are causing issues.
More conservative approach than the comprehensive fixer.

Author: Agent-3 (Infrastructure & DevOps Specialist)
"""

import os
import re
from pathlib import Path


def fix_discord_imports():
    """Fix specific problematic imports in Discord commander."""
    discord_root = Path('src/discord_commander')

    if not discord_root.exists():
        print("Discord commander directory not found")
        return

    fixes_applied = 0

    # Find all Python files in discord_commander
    for py_file in discord_root.rglob('*.py'):
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content

            # Fix specific incorrect imports
            content = content.replace(
                'from src.services.messaging_infrastructure import ConsolidatedMessagingService',
                'from ..services.messaging.service_adapters import ConsolidatedMessagingService'
            )

            content = content.replace(
                'from src.core.messaging_models_core import MessageCategory',
                'from ..core.messaging_models_core import MessageCategory'
            )

            content = content.replace(
                'from src.services.thea.thea_service import TheaService',
                'from ..services.thea.thea_service import TheaService'
            )

            content = content.replace(
                'from src.discord_commander.',
                'from ..'
            )

            # Only write if changed
            if content != original_content:
                with open(py_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ Fixed imports in {py_file.relative_to(discord_root)}")
                fixes_applied += 1

        except Exception as e:
            print(f"❌ Error processing {py_file}: {e}")

    print(f"\n📊 Discord Commander Import Fixes: {fixes_applied} files updated")

    # Test a key import
    try:
        import subprocess
        result = subprocess.run([
            'python', '-c',
            'import sys; sys.path.insert(0, "src"); from discord_commander.views.agent_messaging_view import AgentMessagingView; print("SUCCESS")'
        ], capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("✅ Discord commander imports working")
        else:
            print(f"❌ Discord commander imports still broken: {result.stderr}")
    except Exception as e:
        print(f"❌ Test failed: {e}")


if __name__ == '__main__':
    fix_discord_imports()