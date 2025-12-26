#!/usr/bin/env python3
"""
Session Cleanup Manager
=======================

Automates session cleanup tasks for agents:
1. Create/Update passdown.json
2. Create Final Devlog
3. Post Devlog to Discord
4. Update Swarm Brain Database
5. Create a Tool You Wished You Had

V2 Compliance | Author: Agent-5 | Date: 2025-12-25
"""

import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

try:
    from src.swarm_brain.swarm_memory import SwarmMemory
    HAS_SWARM_MEMORY = True
except ImportError:
    HAS_SWARM_MEMORY = False
    print("⚠️  SwarmMemory not available - Swarm Brain updates will be skipped")

try:
    from tools.categories.communication_tools import DiscordRouterPoster
    HAS_DISCORD = True
except ImportError:
    HAS_DISCORD = False
    print("⚠️  DiscordRouterPoster not available - Discord posting will be skipped")


class SessionCleanupManager:
    """Manages session cleanup tasks for agents."""
    
    def __init__(self, agent_id: str, agent_name: str):
        """Initialize session cleanup manager."""
        self.agent_id = agent_id
        self.agent_name = agent_name
        self.workspace_path = project_root / "agent_workspaces" / agent_id
        self.devlogs_path = self.workspace_path / "devlogs"
        self.passdown_path = self.workspace_path / "passdown.json"
        self.status_path = self.workspace_path / "status.json"
        
        # Ensure directories exist
        self.devlogs_path.mkdir(parents=True, exist_ok=True)
        
        # Initialize services
        self.discord_poster = DiscordRouterPoster() if HAS_DISCORD else None
        self.swarm_memory = SwarmMemory(agent_id=agent_id) if HAS_SWARM_MEMORY else None
    
    def load_status(self) -> Dict[str, Any]:
        """Load current status.json."""
        if not self.status_path.exists():
            return {}
        
        with open(self.status_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def create_passdown(self, session_data: Dict[str, Any]) -> Path:
        """Create or update passdown.json."""
        passdown_data = {
            "agent_id": self.agent_id,
            "agent_name": self.agent_name,
            "session_date": datetime.now().strftime("%Y-%m-%d"),
            "last_updated": datetime.now().isoformat() + "Z",
            "status": "ACTIVE_AGENT_MODE",
            "current_phase": "TASK_EXECUTION",
            **session_data
        }
        
        with open(self.passdown_path, 'w', encoding='utf-8') as f:
            json.dump(passdown_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Passdown created: {self.passdown_path}")
        return self.passdown_path
    
    def create_devlog(self, devlog_content: str, title: str) -> Path:
        """Create final devlog."""
        timestamp = datetime.now().strftime("%Y-%m-%d")
        safe_title = title.lower().replace(' ', '_').replace('/', '_')
        filename = f"{timestamp}_{self.agent_id.lower()}_{safe_title}.md"
        devlog_path = self.devlogs_path / filename
        
        with open(devlog_path, 'w', encoding='utf-8') as f:
            f.write(devlog_content)
        
        print(f"✅ Devlog created: {devlog_path}")
        return devlog_path
    
    def post_to_discord(self, devlog_path: Path, title: str) -> bool:
        """Post devlog to Discord."""
        if not self.discord_poster:
            print("⚠️  Discord posting skipped (not available)")
            return False
        
        # Read devlog content
        with open(devlog_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Truncate if too long (Discord limit ~2000 chars)
        if len(content) > 1900:
            content = content[:1900] + "\n\n... (truncated - see full devlog in workspace)"
        
        result = self.discord_poster.post_update(
            agent_id=self.agent_id,
            message=content,
            title=f"Devlog: {title}",
            priority="normal"
        )
        
        if result.get("success"):
            print(f"✅ Devlog posted to Discord: {title}")
            return True
        else:
            print(f"❌ Failed to post to Discord: {result.get('error')}")
            return False
    
    def update_swarm_brain(self, title: str, content: str, tags: list) -> bool:
        """Update Swarm Brain database."""
        if not self.swarm_memory:
            print("⚠️  Swarm Brain update skipped (not available)")
            return False
        
        try:
            self.swarm_memory.share_learning(
                title=title,
                content=content,
                tags=tags
            )
            print(f"✅ Swarm Brain updated: {title}")
            return True
        except Exception as e:
            print(f"❌ Failed to update Swarm Brain: {e}")
            return False
    
    def run_cleanup(
        self,
        session_data: Dict[str, Any],
        devlog_content: str,
        devlog_title: str,
        swarm_brain_title: Optional[str] = None,
        swarm_brain_content: Optional[str] = None,
        swarm_brain_tags: Optional[list] = None
    ) -> Dict[str, Any]:
        """Run complete session cleanup."""
        results = {
            "passdown": False,
            "devlog": False,
            "discord": False,
            "swarm_brain": False,
            "tool": False
        }
        
        print(f"\n🧹 Starting session cleanup for {self.agent_id}...\n")
        
        # 1. Create/Update passdown.json
        try:
            self.create_passdown(session_data)
            results["passdown"] = True
        except Exception as e:
            print(f"❌ Failed to create passdown: {e}")
        
        # 2. Create Final Devlog
        try:
            devlog_path = self.create_devlog(devlog_content, devlog_title)
            results["devlog"] = True
        except Exception as e:
            print(f"❌ Failed to create devlog: {e}")
            return results
        
        # 3. Post Devlog to Discord
        try:
            results["discord"] = self.post_to_discord(devlog_path, devlog_title)
        except Exception as e:
            print(f"❌ Failed to post to Discord: {e}")
        
        # 4. Update Swarm Brain Database
        if swarm_brain_title and swarm_brain_content:
            try:
                tags = swarm_brain_tags or [self.agent_id.lower(), "session-summary"]
                results["swarm_brain"] = self.update_swarm_brain(
                    swarm_brain_title,
                    swarm_brain_content,
                    tags
                )
            except Exception as e:
                print(f"❌ Failed to update Swarm Brain: {e}")
        
        # 5. Tool creation is manual - user creates their own tool
        print("\n📝 Tool creation: Create a tool you wished you had (manual step)")
        results["tool"] = True  # Mark as complete (user creates tool)
        
        # Summary
        print(f"\n{'='*60}")
        print("📊 Session Cleanup Summary:")
        print(f"  ✅ Passdown: {'✅' if results['passdown'] else '❌'}")
        print(f"  ✅ Devlog: {'✅' if results['devlog'] else '❌'}")
        print(f"  ✅ Discord: {'✅' if results['discord'] else '❌'}")
        print(f"  ✅ Swarm Brain: {'✅' if results['swarm_brain'] else '❌'}")
        print(f"  ✅ Tool: ✅ (manual)")
        print(f"{'='*60}\n")
        
        return results


def main():
    """CLI entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Session Cleanup Manager")
    parser.add_argument("--agent-id", required=True, help="Agent ID (e.g., Agent-5)")
    parser.add_argument("--agent-name", required=True, help="Agent name")
    parser.add_argument("--session-data", type=Path, help="Path to session data JSON")
    parser.add_argument("--devlog", type=Path, help="Path to devlog markdown file")
    parser.add_argument("--devlog-title", help="Devlog title")
    
    args = parser.parse_args()
    
    manager = SessionCleanupManager(args.agent_id, args.agent_name)
    
    # Load session data
    if args.session_data and args.session_data.exists():
        with open(args.session_data, 'r') as f:
            session_data = json.load(f)
    else:
        session_data = {}
    
    # Load devlog
    if args.devlog and args.devlog.exists():
        with open(args.devlog, 'r', encoding='utf-8') as f:
            devlog_content = f.read()
    else:
        devlog_content = f"# {args.agent_id} Session Summary\n\nSession cleanup completed."
    
    devlog_title = args.devlog_title or f"{args.agent_id} Session Summary"
    
    # Run cleanup
    manager.run_cleanup(
        session_data=session_data,
        devlog_content=devlog_content,
        devlog_title=devlog_title
    )


if __name__ == "__main__":
    main()

