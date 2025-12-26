#!/usr/bin/env python3
"""Post session cleanup summary to Discord."""

import sys
from pathlib import Path

project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.categories.communication_tools import DiscordRouterPoster

poster = DiscordRouterPoster()

message = """📝 **Agent-5 Session Cleanup Complete**

✅ Passdown updated
✅ Devlog created  
✅ Swarm Brain updated
✅ Tool created (session_cleanup_manager.py)

**Session Summary**: 
- Workspace cleanup (55+ messages archived)
- Tool consolidation analysis (121 tools, 10 V2 violations)
- Coordination activation (2 active coordinations)
- V2 compliance standard update (300→400 lines)

Ready for next session! 🐝"""

result = poster.post_update(
    agent_id='Agent-5',
    message=message,
    title='Agent-5 Session Cleanup Complete',
    priority='normal'
)

if result.get('success'):
    print('✅ Posted to Discord')
else:
    print(f'❌ Failed: {result.get("error")}')

