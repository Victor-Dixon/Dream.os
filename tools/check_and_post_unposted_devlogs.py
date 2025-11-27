#!/usr/bin/env python3
"""
Check and Post Unposted Devlogs to Discord
===========================================

Scans devlogs directory and posts any unposted devlogs to Discord.
Tracks posted devlogs to avoid duplicates.

⚠️ NOTE: This script uses devlog_poster.py (SSOT) internally.
All devlog posting should go through devlog_poster.py.

Routing Rules:
- Agents (1-3, 5-8): Always post to their own devlog channels
- Captain (Agent-4): Regular posts → own channel, Major updates → captain channel

Author: Agent-7 (Web Development Specialist)
Date: 2025-11-26
"""

import os
import json
import sys
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv
import requests

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

load_dotenv()


def get_agent_webhook(agent_id: str) -> str | None:
    """Get Discord webhook URL for agent."""
    # Try multiple naming conventions
    webhook = (
        os.getenv(f"DISCORD_WEBHOOK_{agent_id.replace('-', '_')}")
        or os.getenv(f"DISCORD_{agent_id.replace('-', '_')}_WEBHOOK")
        or os.getenv("DISCORD_WEBHOOK_URL")  # Fallback to general
    )
    return webhook


def get_posted_devlogs() -> set[str]:
    """Get set of already posted devlog filenames."""
    log_file = Path("logs/devlog_posts.json")
    if not log_file.exists():
        return set()
    
    try:
        with open(log_file, 'r') as f:
            data = json.load(f)
        return {entry.get("filename", "") for entry in data if entry.get("filename")}
    except (json.JSONDecodeError, Exception):
        return set()


def log_devlog_post(agent_id: str, filename: str, success: bool) -> None:
    """Log devlog post attempt."""
    log_file = Path("logs/devlog_posts.json")
    log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing logs
    if log_file.exists():
        try:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        except (json.JSONDecodeError, Exception):
            logs = []
    else:
        logs = []
    
    # Add new log entry
    logs.append({
        "agent_id": agent_id,
        "filename": filename,
        "posted_at": datetime.now().isoformat(),
        "success": success,
    })
    
    # Save logs
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)


def extract_agent_from_filename(filename: str) -> str | None:
    """Extract agent ID from devlog filename."""
    filename_lower = filename.lower()
    
    # Try patterns: agent2_, agent-2_, Agent-2_, etc.
    for agent_num in range(1, 9):
        patterns = [
            f"agent{agent_num}_",
            f"agent-{agent_num}_",
            f"Agent-{agent_num}_",
            f"Agent{agent_num}_",
        ]
        for pattern in patterns:
            if pattern.lower() in filename_lower:
                return f"Agent-{agent_num}"
    
    return None


def post_devlog_to_discord(agent_id: str, file_path: Path, webhook_url: str) -> bool:
    """Post devlog to Discord."""
    try:
        content = file_path.read_text(encoding='utf-8')
        
        # Discord message limit: 2000 chars
        if len(content) > 1900:
            preview = content[:1900] + "\n\n*(Full devlog available in Swarm Brain)*"
        else:
            preview = content
        
        # Create embed
        embed = {
            "title": f"📋 Devlog: {file_path.stem}",
            "description": preview,
            "color": 0x3498DB,  # Blue
            "fields": [
                {"name": "Agent", "value": agent_id, "inline": True},
                {"name": "File", "value": file_path.name, "inline": True},
                {"name": "Timestamp", "value": datetime.now().strftime("%Y-%m-%d %H:%M"), "inline": True},
            ],
            "footer": {"text": "Swarm Brain Devlog System"},
        }
        
        payload = {
            "embeds": [embed],
            "username": f"{agent_id} Devlog Bot"
        }
        
        response = requests.post(webhook_url, json=payload, timeout=10)
        
        if response.status_code in [200, 204]:
            return True
        else:
            print(f"❌ Discord API error: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error posting devlog: {e}")
        return False


def main():
    """Main execution."""
    print("🔍 Checking for Unposted Devlogs...")
    print("=" * 60)
    
    # Get posted devlogs
    posted = get_posted_devlogs()
    print(f"✅ Found {len(posted)} already posted devlogs")
    
    # Scan devlogs directory
    devlogs_dir = Path("devlogs")
    if not devlogs_dir.exists():
        print(f"❌ Devlogs directory not found: {devlogs_dir}")
        return
    
    # Find unposted devlogs
    unposted = []
    for devlog_file in devlogs_dir.glob("*.md"):
        if devlog_file.name not in posted:
            agent_id = extract_agent_from_filename(devlog_file.name)
            if agent_id:
                unposted.append((agent_id, devlog_file))
    
    print(f"\n📋 Found {len(unposted)} unposted devlogs")
    
    if not unposted:
        print("✅ All devlogs already posted!")
        return
    
    # Post unposted devlogs
    print("\n📤 Posting unposted devlogs...")
    success_count = 0
    fail_count = 0
    
    for agent_id, file_path in unposted:
        print(f"\n📝 Processing: {file_path.name} ({agent_id})")
        
        # Get webhook
        webhook_url = get_agent_webhook(agent_id)
        if not webhook_url:
            print(f"⚠️ No webhook configured for {agent_id} - skipping")
            log_devlog_post(agent_id, file_path.name, False)
            fail_count += 1
            continue
        
        # Post to Discord using devlog_poster.py (SSOT)
        devlog_poster_path = Path(__file__).parent / "devlog_poster.py"
        import subprocess
        cmd = [sys.executable, str(devlog_poster_path),
               "--agent", agent_id,
               "--file", str(file_path)]
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            success = result.returncode == 0
            if result.stdout:
                print(result.stdout)
        except subprocess.CalledProcessError:
            success = False
        except Exception as e:
            print(f"⚠️ Error calling devlog_poster.py: {e}")
            # Fallback to direct posting
            success = post_devlog_to_discord(agent_id, file_path, webhook_url)
        
        if success:
            print(f"✅ Posted to Discord: {file_path.name}")
            success_count += 1
        else:
            print(f"❌ Failed to post: {file_path.name}")
            fail_count += 1
        
        # Log attempt
        log_devlog_post(agent_id, file_path.name, success)
    
    print("\n" + "=" * 60)
    print(f"📊 SUMMARY:")
    print(f"   Total unposted: {len(unposted)}")
    print(f"   Successfully posted: {success_count}")
    print(f"   Failed: {fail_count}")
    print("\n🐝 WE. ARE. SWARM. ⚡🔥")


if __name__ == "__main__":
    main()


