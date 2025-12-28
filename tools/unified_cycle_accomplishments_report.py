#!/usr/bin/env python3
import json
import os
import datetime
from pathlib import Path
import glob
import sys

# Add project root to path to allow imports from src/tools
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

try:
    from tools.categories.communication_tools import DiscordRouterPoster
    DISCORD_AVAILABLE = True
except ImportError as e:
    print(f"⚠️  Could not import DiscordRouterPoster. Discord posting will be skipped.")
    print(f"   Error details: {e}")
    DISCORD_AVAILABLE = False
except Exception as e:
    print(f"⚠️  Unexpected error importing DiscordRouterPoster: {e}")
    import traceback
    traceback.print_exc()
    DISCORD_AVAILABLE = False

def generate_report():
    workspace_root = Path("/workspace")
    agent_workspaces = workspace_root / "agent_workspaces"
    
    agents_data = []
    
    total_completed_tasks = 0
    total_achievements = 0
    active_agents = 0
    
    print("Collecting data from agent workspaces...")
    
    # Process Agent 1-8
    for i in range(1, 9):
        agent_id = f"Agent-{i}"
        status_file = agent_workspaces / agent_id / "status.json"
        
        if status_file.exists():
            try:
                with open(status_file, 'r') as f:
                    data = json.load(f)
                    
                agents_data.append(data)
                
                # Count stats
                completed = data.get("completed_tasks", [])
                total_completed_tasks += len(completed)
                
                # Achievements might be in 'achievements'
                achievements = data.get("achievements", [])
                total_achievements += len(achievements)
                
                status = data.get("status", "")
                if "ACTIVE" in status:
                    active_agents += 1
                    
            except Exception as e:
                print(f"Error reading {status_file}: {e}")
        else:
            print(f"Warning: Status file not found for {agent_id}")
                
    # Generate Markdown
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    date_str = datetime.datetime.now().strftime("%Y-%m-%d")
    filename_ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    report_content = f"""# Cycle Accomplishments Report

**Generated:** {timestamp}
**Date:** {date_str}
**Agents:** {active_agents}

---

## Summary

**Total Agents:** {active_agents}
**Total Completed Tasks:** {total_completed_tasks}
**Total Achievements:** {total_achievements}

---
"""

    for data in agents_data:
        agent_id = data.get("agent_id", "Unknown")
        agent_name = data.get("agent_name", "Unknown")
        status = data.get("status", "Unknown")
        last_updated = data.get("last_updated", "Unknown")
        priority = data.get("mission_priority", data.get("priority", "Normal"))
        
        report_content += f"\n## {agent_id}: {agent_name}\n\n"
        report_content += f"**Status:** {status}  \n"
        report_content += f"**Priority:** {priority}  \n"
        report_content += f"**Last Updated:** {last_updated}\n\n"
        
        # Current Mission
        current_mission = data.get("current_mission", "No mission set.")
        report_content += f"### Current Mission\n{current_mission}\n\n"
        
        # Completed Tasks
        completed = data.get("completed_tasks", [])
        if isinstance(completed, list) and completed:
            report_content += f"### Completed Tasks ({len(completed)})\n"
            for task in completed[-20:]: # Last 20
                 # Task can be string or dict
                if isinstance(task, str):
                    report_content += f"- {task}\n"
                elif isinstance(task, dict):
                    task_desc = task.get("task", "Unknown Task")
                    details = task.get("details", "")
                    if details:
                        report_content += f"- {task_desc}: {details}\n"
                    else:
                        report_content += f"- {task_desc}\n"
            report_content += "\n"

        # Recent completions (sometimes used instead of completed_tasks for objects)
        recent = data.get("recent_completions", [])
        if recent and not completed: # Fallback if completed_tasks is empty but recent exists
             report_content += f"### Recent Completions ({len(recent)})\n"
             for task in recent[-20:]:
                if isinstance(task, dict):
                    task_desc = task.get("task", "Unknown Task")
                    details = task.get("details", "")
                    if details:
                         report_content += f"- {task_desc}: {details}\n"
                    else:
                         report_content += f"- {task_desc}\n"
                elif isinstance(task, str):
                    report_content += f"- {task}\n"
             report_content += "\n"


        # Achievements
        achievements = data.get("achievements", [])
        if achievements:
            report_content += f"### Achievements ({len(achievements)})\n"
            for ach in achievements[-15:]:
                if isinstance(ach, str):
                    report_content += f"- {ach}\n"
                elif isinstance(ach, dict):
                     # Extract title or description
                     title = ach.get("title", ach.get("description", str(ach)))
                     report_content += f"- {title}\n"
            report_content += "\n"
            
        # Active Tasks
        active = data.get("current_tasks", [])
        if active:
            report_content += f"### Active Tasks ({len(active)})\n"
            for task in active[-10:]:
                if isinstance(task, str):
                    report_content += f"- {task}\n"
                elif isinstance(task, dict):
                    task_desc = task.get("task", "Unknown Task")
                    report_content += f"- {task_desc}\n"
            report_content += "\n"
            
        report_content += "---\n"
        
    report_content += """
## Report Metadata

**Generated By:** Unified Cycle Accomplishments Report Generator
**Protocol:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0
**Format:** Markdown
"""

    report_dir = workspace_root / "reports"
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / f"cycle_accomplishments_{filename_ts}.md"
    
    try:
        with open(report_path, 'w') as f:
            f.write(report_content)
        print(f"Report generated: {report_path}")
        
        # Post to Discord
        if DISCORD_AVAILABLE:
            print("Posting report to Discord (chunked)...")
            try:
                poster = DiscordRouterPoster(agent_id="Agent-4")
                
                # 1. Post Summary
                summary_msg = f"""**Cycle Accomplishments Report**
**Date:** {date_str}
**Agents:** {active_agents}
**Tasks:** {total_completed_tasks} | **Achievements:** {total_achievements}

*Full report generated at: `reports/{report_path.name}`*
"""
                poster.post_update(
                    agent_id="Agent-4", 
                    message=summary_msg, 
                    title="📊 Cycle Report Summary", 
                    priority="normal"
                )

                # 2. Post per-agent details
                for data in agents_data:
                    agent_id = data.get("agent_id", "Unknown")
                    agent_name = data.get("agent_name", "Unknown")
                    
                    # Construct Agent Message
                    # We need to manually chunk to avoid truncation in DiscordRouterPoster (limit ~1800 chars total)
                    # Safe limit for message body: 1600 chars
                    MAX_CHUNK_SIZE = 1600
                    
                    # Header stats
                    status = data.get("status", "Unknown")
                    priority = data.get("mission_priority", data.get("priority", "Normal"))
                    current_mission = data.get("current_mission", "No mission set.")
                    
                    # Start first chunk
                    agent_msg = f"**Status:** {status} | **Priority:** {priority}\n"
                    agent_msg += f"**Mission:** {current_mission}\n\n"
                    
                    # Completed Tasks
                    completed = data.get("completed_tasks", [])
                    if completed:
                        agent_msg += f"**Completed ({len(completed)}):**\n"
                        for task in completed: 
                            task_str = ""
                            if isinstance(task, str):
                                task_str = f"- {task}\n"
                            elif isinstance(task, dict):
                                task_desc = task.get("task", "Unknown")
                                details = task.get("details", "")
                                if details:
                                    task_str = f"- {task_desc}: {details}\n"
                                else:
                                    task_str = f"- {task_desc}\n"
                            
                            # Check length
                            if len(agent_msg) + len(task_str) > MAX_CHUNK_SIZE:
                                # Post current chunk
                                poster.post_update(agent_id="Agent-4", message=agent_msg, title=f"📄 {agent_id}: {agent_name}", priority="normal")
                                agent_msg = f"**{agent_id} (Continued):**\n"
                            
                            agent_msg += task_str
                        agent_msg += "\n"

                    # Achievements
                    achievements = data.get("achievements", [])
                    if achievements:
                        agent_msg += f"**Achievements ({len(achievements)}):**\n"
                        for ach in achievements:
                            ach_str = ""
                            if isinstance(ach, str):
                                ach_str = f"- {ach}\n"
                            elif isinstance(ach, dict):
                                title = ach.get("title", ach.get("description", str(ach)))
                                ach_str = f"- {title}\n"
                            
                            if len(agent_msg) + len(ach_str) > MAX_CHUNK_SIZE:
                                poster.post_update(agent_id="Agent-4", message=agent_msg, title=f"📄 {agent_id}: {agent_name}", priority="normal")
                                agent_msg = f"**{agent_id} (Continued):**\n"
                            
                            agent_msg += ach_str
                            
                    # Active Tasks
                    active = data.get("current_tasks", [])
                    if active:
                         agent_msg += f"**Active Tasks ({len(active)}):**\n"
                         for task in active[:10]:
                            task_str = ""
                            if isinstance(task, str):
                                task_str = f"- {task}\n"
                            elif isinstance(task, dict):
                                task_desc = task.get("task", "Unknown Task")
                                task_str = f"- {task_desc}\n"
                            
                            if len(agent_msg) + len(task_str) > MAX_CHUNK_SIZE:
                                poster.post_update(agent_id="Agent-4", message=agent_msg, title=f"📄 {agent_id}: {agent_name}", priority="normal")
                                agent_msg = f"**{agent_id} (Continued):**\n"
                            
                            agent_msg += task_str
                    
                    # Post final chunk for this agent
                    if agent_msg:
                        poster.post_update(agent_id="Agent-4", message=agent_msg, title=f"📄 {agent_id}: {agent_name}", priority="normal")

            except Exception as e:
                print(f"⚠️ Error posting to Discord: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("ℹ️ Discord posting skipped (module not available)")
            
    except Exception as e:
        print(f"Error writing report: {e}")

if __name__ == "__main__":
    generate_report()
