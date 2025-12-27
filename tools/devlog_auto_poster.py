#!/usr/bin/env python3
"""
Devlog Auto-Poster Tool

Automated devlog posting scheduler that monitors agent workspaces and posts devlogs
to Discord when created.

Usage:
    python tools/devlog_auto_poster.py [--agent Agent-X] [--watch] [--interval SECONDS] [--once]
    
Examples:
    # Post all unposted devlogs for all agents
    python tools/devlog_auto_poster.py --once
    
    # Monitor Agent-1's devlogs and auto-post new ones
    python tools/devlog_auto_poster.py --agent Agent-1 --watch --interval 60
    
    # Post unposted devlogs for Agent-7
    python tools/devlog_auto_poster.py --agent Agent-7 --once
"""

import os
import sys
import json
import time
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set, Optional
from dotenv import load_dotenv

# Add project root to path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

# Load .env
env_path = project_root / ".env"
load_dotenv(dotenv_path=env_path)

# Import devlog poster
try:
    from tools.devlog_poster import post_devlog
    DEVLOG_POSTER_AVAILABLE = True
except ImportError:
    DEVLOG_POSTER_AVAILABLE = False
    print("⚠️  devlog_poster.py not available - install dependencies")


class DevlogAutoPoster:
    """Monitors agent workspaces and auto-posts devlogs to Discord."""
    
    def __init__(self, agent_id: Optional[str] = None):
        """Initialize auto-poster.
        
        Args:
            agent_id: Optional agent ID to monitor (if None, monitors all agents)
        """
        self.agent_id = agent_id
        self.project_root = project_root
        self.workspaces_dir = project_root / "agent_workspaces"
        self.state_file = project_root / "tools" / ".devlog_auto_poster_state.json"
        self.posted_devlogs: Set[str] = self._load_state()
    
    def _load_state(self) -> Set[str]:
        """Load state of posted devlogs from file.
        
        Returns:
            Set of posted devlog file paths
        """
        if self.state_file.exists():
            try:
                with open(self.state_file, 'r') as f:
                    data = json.load(f)
                    return set(data.get("posted_devlogs", []))
            except Exception as e:
                print(f"⚠️  Failed to load state: {e}")
        return set()
    
    def _save_state(self):
        """Save state of posted devlogs to file."""
        try:
            data = {
                "posted_devlogs": list(self.posted_devlogs),
                "last_updated": datetime.now().isoformat()
            }
            with open(self.state_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"⚠️  Failed to save state: {e}")
    
    def _get_agent_workspaces(self) -> List[Path]:
        """Get list of agent workspace directories to monitor.
        
        Returns:
            List of agent workspace paths
        """
        if self.agent_id:
            # Single agent
            agent_dir = self.workspaces_dir / self.agent_id
            if agent_dir.exists():
                return [agent_dir]
            return []
        else:
            # All agents
            workspaces = []
            for item in self.workspaces_dir.iterdir():
                if item.is_dir() and item.name.startswith("Agent-"):
                    workspaces.append(item)
            return workspaces
    
    def _find_devlogs(self, workspace_dir: Path) -> List[Path]:
        """Find all devlog markdown files in workspace.
        
        Args:
            workspace_dir: Agent workspace directory
        
        Returns:
            List of devlog file paths
        """
        devlogs = []
        
        # Check devlogs/ directory
        devlogs_dir = workspace_dir / "devlogs"
        if devlogs_dir.exists():
            for file in devlogs_dir.glob("*.md"):
                devlogs.append(file)
        
        # Also check root of workspace for devlog files
        for file in workspace_dir.glob("DEVLOG*.md"):
            devlogs.append(file)
        for file in workspace_dir.glob("devlog*.md"):
            devlogs.append(file)
        
        return sorted(devlogs, key=lambda p: p.stat().st_mtime, reverse=True)
    
    def _get_agent_id_from_path(self, devlog_path: Path) -> Optional[str]:
        """Extract agent ID from devlog file path.
        
        Args:
            devlog_path: Path to devlog file
        
        Returns:
            Agent ID (e.g., "Agent-1") or None
        """
        # Try to extract from path: agent_workspaces/Agent-X/...
        parts = devlog_path.parts
        for part in parts:
            if part.startswith("Agent-"):
                return part
        return None
    
    def _is_devlog_posted(self, devlog_path: Path) -> bool:
        """Check if devlog has been posted.
        
        Args:
            devlog_path: Path to devlog file
        
        Returns:
            True if already posted
        """
        # Use absolute path as key
        key = str(devlog_path.resolve())
        return key in self.posted_devlogs
    
    def _mark_devlog_posted(self, devlog_path: Path):
        """Mark devlog as posted.
        
        Args:
            devlog_path: Path to devlog file
        """
        key = str(devlog_path.resolve())
        self.posted_devlogs.add(key)
        self._save_state()
    
    def _post_devlog(self, devlog_path: Path, agent_id: str) -> bool:
        """Post devlog to Discord.
        
        Args:
            devlog_path: Path to devlog file
            agent_id: Agent ID
        
        Returns:
            True if successful
        """
        if not DEVLOG_POSTER_AVAILABLE:
            print(f"❌ Devlog poster not available - cannot post {devlog_path.name}")
            return False
        
        try:
            success = post_devlog(
                agent_id=agent_id,
                devlog_path=str(devlog_path),
                title=None  # Auto-extract from file
            )
            
            if success:
                self._mark_devlog_posted(devlog_path)
                print(f"✅ Posted devlog: {devlog_path.name} (Agent: {agent_id})")
            else:
                print(f"❌ Failed to post devlog: {devlog_path.name} (Agent: {agent_id})")
            
            return success
            
        except Exception as e:
            print(f"❌ Error posting devlog {devlog_path.name}: {e}")
            return False
    
    def check_and_post(self) -> Dict[str, int]:
        """Check for unposted devlogs and post them.
        
        Returns:
            Dict with stats: {"checked": N, "posted": N, "skipped": N}
        """
        stats = {"checked": 0, "posted": 0, "skipped": 0}
        
        workspaces = self._get_agent_workspaces()
        
        for workspace_dir in workspaces:
            agent_id = workspace_dir.name
            devlogs = self._find_devlogs(workspace_dir)
            
            for devlog_path in devlogs:
                stats["checked"] += 1
                
                # Check if already posted
                if self._is_devlog_posted(devlog_path):
                    stats["skipped"] += 1
                    continue
                
                # Post devlog
                if self._post_devlog(devlog_path, agent_id):
                    stats["posted"] += 1
                else:
                    stats["skipped"] += 1
        
        return stats
    
    def watch(self, interval: int = 60):
        """Watch for new devlogs and auto-post them.
        
        Args:
            interval: Check interval in seconds (default: 60)
        """
        print(f"👀 Watching for new devlogs (interval: {interval}s)")
        if self.agent_id:
            print(f"   Monitoring: {self.agent_id}")
        else:
            print(f"   Monitoring: All agents")
        print(f"   Press Ctrl+C to stop\n")
        
        try:
            while True:
                stats = self.check_and_post()
                
                if stats["posted"] > 0:
                    print(f"📤 Posted {stats['posted']} new devlog(s)")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n\n👋 Stopping devlog auto-poster")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Automated devlog posting scheduler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Post all unposted devlogs for all agents (one-time)
  python tools/devlog_auto_poster.py --once
  
  # Monitor Agent-1's devlogs and auto-post new ones every 60 seconds
  python tools/devlog_auto_poster.py --agent Agent-1 --watch --interval 60
  
  # Post unposted devlogs for Agent-7 (one-time)
  python tools/devlog_auto_poster.py --agent Agent-7 --once
        """
    )
    
    parser.add_argument(
        "--agent",
        type=str,
        help="Agent ID to monitor (e.g., Agent-1). If not specified, monitors all agents."
    )
    parser.add_argument(
        "--watch",
        action="store_true",
        help="Watch mode - continuously monitor for new devlogs"
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=60,
        help="Check interval in seconds for watch mode (default: 60)"
    )
    parser.add_argument(
        "--once",
        action="store_true",
        help="One-time check - post all unposted devlogs and exit"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if not args.watch and not args.once:
        parser.error("Must specify either --watch or --once")
    
    if not DEVLOG_POSTER_AVAILABLE:
        print("❌ Devlog poster not available - install dependencies")
        sys.exit(1)
    
    # Initialize auto-poster
    poster = DevlogAutoPoster(agent_id=args.agent)
    
    # Run
    if args.once:
        print("🔍 Checking for unposted devlogs...\n")
        stats = poster.check_and_post()
        
        print("\n" + "="*60)
        print("Devlog Auto-Poster Results")
        print("="*60)
        print(f"Checked: {stats['checked']} devlogs")
        print(f"Posted: {stats['posted']} new devlog(s)")
        print(f"Skipped: {stats['skipped']} (already posted)")
        print("="*60 + "\n")
        
    elif args.watch:
        poster.watch(interval=args.interval)


if __name__ == "__main__":
    main()

