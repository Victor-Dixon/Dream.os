#!/usr/bin/env python3
"""Post Agent-2 devlog summary to Discord."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.categories.communication_tools import DiscordRouterPoster

poster = DiscordRouterPoster()

message = """📝 **Agent-2 Session Cleanup Complete**

✅ Passdown updated
✅ Devlog created  
✅ Swarm Brain updated
✅ Tool created (a2a_coordination_validator.py)

**Session Summary**: 
- A2A coordination system debugging (template application, sender identification)
- 2026 revenue engine website fixes Phase 1 architecture validation
- WordPress specifications created (Custom Post Types, Custom Fields, templates)
- 2 architecture reviews marked complete

Ready for next session! 🐝"""

result = poster.post_update(
    agent_id='Agent-2',
    message=message,
    title='Agent-2 Session Cleanup Complete',
    priority='normal'
)

if result.get('success'):
    print('✅ Posted to Discord')
else:
    print(f'❌ Failed: {result.get("error")}')

