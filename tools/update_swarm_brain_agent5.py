#!/usr/bin/env python3
"""Update Swarm Brain with Agent-5 session knowledge"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from mcp_servers.swarm_brain_server import share_learning
    
    # Read swarm brain update file
    update_file = Path("agent_workspaces/Agent-5/swarm_brain_update_2025-12-26.md")
    if update_file.exists():
        content = update_file.read_text(encoding='utf-8')
        
        # Extract title
        title = "Agent-5 Session Knowledge - 2025-12-26"
        if content.startswith("#"):
            first_line = content.split("\n")[0]
            title = first_line.replace("#", "").strip()
        
        # Share learning
        result = share_learning(
            agent_id='Agent-5',
            title=title,
            content=content,
            tags=['analytics', 'validation', 'automation', 'task-management', 'environment-variables', 'ssot-compliance', 'devlog-standards', 'coordination', 'configuration-checking', 'integration']
        )
        
        if result.get('success'):
            print(f"✅ Swarm Brain updated: {title}")
            print(f"   Entry ID: {result.get('entry_id')}")
        else:
            print(f"❌ Failed to update Swarm Brain: {result.get('error')}")
    else:
        print(f"❌ Swarm Brain update file not found: {update_file}")
        
except ImportError as e:
    print(f"⚠️  Swarm Brain not available: {e}")
except Exception as e:
    print(f"❌ Error: {e}")

