#!/usr/bin/env python3
"""
Check Status Monitor and Agent Statuses
Verifies status monitor is running and checks agent status staleness
"""

import json
from pathlib import Path
from datetime import datetime

AGENTS = ["Agent-1", "Agent-2", "Agent-3", "Agent-5", "Agent-6", "Agent-7", "Agent-8"]
WORKSPACE_ROOT = Path(__file__).parent.parent

def check_agent_statuses():
    """Check all agent status files for staleness."""
    now = datetime.now()
    stale_agents = []
    recent_agents = []
    
    print("=" * 60)
    print("📊 AGENT STATUS CHECK")
    print("=" * 60)
    print()
    
    for agent_id in AGENTS:
        status_file = WORKSPACE_ROOT / "agent_workspaces" / agent_id / "status.json"
        
        if not status_file.exists():
            print(f"❌ {agent_id}: status.json NOT FOUND")
            stale_agents.append((agent_id, "FILE_MISSING", None))
            continue
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                status = json.load(f)
            
            last_updated = status.get('last_updated', '')
            if not last_updated:
                print(f"⚠️  {agent_id}: No last_updated timestamp")
                stale_agents.append((agent_id, "NO_TIMESTAMP", None))
                continue
            
            try:
                dt = datetime.strptime(last_updated, '%Y-%m-%d %H:%M:%S')
                diff_hours = (now - dt).total_seconds() / 3600
                
                if diff_hours > 2:
                    print(f"🔴 {agent_id}: STALE ({diff_hours:.1f}h old) - Last: {last_updated}")
                    stale_agents.append((agent_id, "STALE", diff_hours))
                else:
                    print(f"✅ {agent_id}: RECENT ({diff_hours:.1f}h old) - Last: {last_updated}")
                    recent_agents.append((agent_id, diff_hours))
            except ValueError:
                print(f"⚠️  {agent_id}: Invalid timestamp format: {last_updated}")
                stale_agents.append((agent_id, "INVALID_TIMESTAMP", None))
        except Exception as e:
            print(f"❌ {agent_id}: Error reading status: {e}")
            stale_agents.append((agent_id, "ERROR", str(e)))
    
    print()
    print("=" * 60)
    print("📊 SUMMARY")
    print("=" * 60)
    print(f"✅ Recent agents: {len(recent_agents)}")
    print(f"🔴 Stale agents: {len(stale_agents)}")
    
    if stale_agents:
        print()
        print("🔴 STALE AGENTS:")
        for agent_id, reason, hours in stale_agents:
            if hours:
                print(f"   {agent_id}: {reason} ({hours:.1f}h old)")
            else:
                print(f"   {agent_id}: {reason}")
    
    return stale_agents, recent_agents

def check_discord_bot_status():
    """Check if Discord bot is running."""
    print()
    print("=" * 60)
    print("🤖 DISCORD BOT STATUS CHECK")
    print("=" * 60)
    print()
    
    # Check for running Python processes
    import subprocess
    try:
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        python_processes = [line for line in result.stdout.split('\n') if 'python.exe' in line.lower()]
        print(f"📊 Python processes running: {len(python_processes)}")
        
        # Check for discord bot specifically
        discord_bot_running = False
        for line in python_processes:
            if 'discord' in line.lower() or 'bot' in line.lower():
                discord_bot_running = True
                break
        
        if discord_bot_running:
            print("✅ Discord bot process detected")
        else:
            print("⚠️  Discord bot process not clearly identified")
            print("   (May be running but not identifiable by process name)")
        
    except Exception as e:
        print(f"⚠️  Could not check processes: {e}")
    
    print()
    print("💡 To verify status monitor:")
    print("   1. Check Discord: !monitor status")
    print("   2. Check logs: Look for 'Status change monitor started'")
    print("   3. Check bot startup: Should see monitor start message")

if __name__ == "__main__":
    stale, recent = check_agent_statuses()
    check_discord_bot_status()
    
    print()
    print("=" * 60)
    if stale:
        print(f"🚨 ACTION REQUIRED: {len(stale)} agents need status updates")
    else:
        print("✅ All agents have recent status updates")
    print("=" * 60)

