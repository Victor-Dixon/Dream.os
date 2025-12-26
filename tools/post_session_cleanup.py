#!/usr/bin/env python3
"""
Post Session Cleanup - Post devlog to Discord and update Swarm Brain
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from tools.categories.communication_tools import DiscordRouterPoster
from mcp_servers.swarm_brain_server import share_learning

def post_devlog_to_discord(devlog_path: str, agent_id: str = "Agent-3"):
    """Post devlog to Discord."""
    devlog_file = Path(devlog_path)
    if not devlog_file.exists():
        print(f"❌ Devlog file not found: {devlog_path}")
        return False
    
    devlog_content = devlog_file.read_text()
    
    # Extract title from devlog (first line after #)
    title = "Agent-3 Final Session Devlog"
    if devlog_content.startswith("#"):
        first_line = devlog_content.split("\n")[0]
        title = first_line.replace("#", "").strip()
    
    # Create summary message
    message = f"**Session Complete!**\n\n"
    message += f"📊 **Key Accomplishments:**\n"
    message += f"- Documentation sprawl audit (2,269 files)\n"
    message += f"- Duplicate consolidation plan (92 pairs)\n"
    message += f"- Website implementation coordination (Agent-7)\n"
    message += f"- V2 compliance documentation update (15 files)\n"
    message += f"- Workspace cleanup\n\n"
    message += f"🛠️ **Tools Created:** 5\n"
    message += f"📈 **Points Earned:** 175 pts\n\n"
    message += f"📄 Full devlog: `{devlog_file.name}`\n"
    
    poster = DiscordRouterPoster()
    result = poster.post_update(
        agent_id=agent_id,
        message=message,
        title=title,
        priority="normal"
    )
    
    if result["success"]:
        print(f"✅ Posted devlog to Discord: {title}")
        return True
    else:
        print(f"❌ Failed to post to Discord: {result.get('error')}")
        return False

def update_swarm_brain(swarm_brain_path: str, agent_id: str = "Agent-3"):
    """Update Swarm Brain with session knowledge."""
    swarm_brain_file = Path(swarm_brain_path)
    if not swarm_brain_file.exists():
        print(f"❌ Swarm Brain file not found: {swarm_brain_path}")
        return False
    
    content = swarm_brain_file.read_text()
    
    # Extract title
    title = "Agent-3 Session Knowledge - 2025-12-24"
    if content.startswith("#"):
        first_line = content.split("\n")[0]
        title = first_line.replace("#", "").strip()
    
    # Share learning to Swarm Brain
    result = share_learning(
        agent_id=agent_id,
        title=title,
        content=content,
        tags=["infrastructure", "devops", "documentation", "coordination", "deployment"]
    )
    
    if result.get("success"):
        print(f"✅ Updated Swarm Brain: {title}")
        print(f"   Entry ID: {result.get('entry_id')}")
        return True
    else:
        print(f"❌ Failed to update Swarm Brain: {result.get('error')}")
        return False

def main():
    """Main entry point."""
    agent_id = "Agent-3"
    devlog_path = "agent_workspaces/Agent-3/devlog_2025-12-24_final_session.md"
    swarm_brain_path = "agent_workspaces/Agent-3/swarm_brain_update_2025-12-24.md"
    
    print("🎯 Session Cleanup - Posting to Discord and Swarm Brain\n")
    
    # Post to Discord
    print("📢 Posting devlog to Discord...")
    discord_success = post_devlog_to_discord(devlog_path, agent_id)
    
    # Update Swarm Brain
    print("\n🧠 Updating Swarm Brain...")
    swarm_success = update_swarm_brain(swarm_brain_path, agent_id)
    
    # Summary
    print("\n" + "="*50)
    if discord_success and swarm_success:
        print("✅ Session cleanup complete!")
        print("   - Devlog posted to Discord")
        print("   - Swarm Brain updated")
    else:
        print("⚠️  Session cleanup completed with warnings:")
        if not discord_success:
            print("   - Discord posting failed")
        if not swarm_success:
            print("   - Swarm Brain update failed")
    print("="*50)

if __name__ == "__main__":
    main()

