"""
Discord Poster Module
=====================

Handles Discord posting with chunking and file uploads.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-30
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

from pathlib import Path
from typing import Dict, List, Any, Optional

# Try to import Discord posting functionality
try:
    from tools.categories.communication_tools import DiscordRouterPoster
    DISCORD_AVAILABLE = True
except ImportError:
    DISCORD_AVAILABLE = False
    DiscordRouterPoster = None


def post_summary(
    date_str: str,
    active_agents: int,
    total_completed: int,
    total_achievements: int,
    report_path: Path,
    agent_id: str = "Agent-4"
) -> bool:
    """
    Post summary message to Discord.
    
    Args:
        date_str: Date string for the report
        active_agents: Number of active agents
        total_completed: Total completed tasks
        total_achievements: Total achievements
        report_path: Path to full report file
        agent_id: Target agent channel (default: Agent-4)
    
    Returns:
        True if successful, False otherwise
    """
    if not DISCORD_AVAILABLE:
        print("⚠️  Discord posting not available - DiscordRouterPoster not found")
        return False
    
    try:
        poster = DiscordRouterPoster(agent_id=agent_id)
        
        summary_msg = f"""**Cycle Accomplishments Report**
**Date:** {date_str}
**Agents:** {active_agents}
**Tasks:** {total_completed} | **Achievements:** {total_achievements}

*Full report generated at: `reports/{report_path.name}`*"""
        
        poster.post_update(
            agent_id=agent_id,
            message=summary_msg,
            title="📊 Cycle Report Summary",
            priority="normal"
        )
        
        return True
    except Exception as e:
        print(f"❌ Error posting summary to Discord: {e}")
        return False


def post_agent_details(
    agents_data: List[Dict[str, Any]],
    agent_id: str = "Agent-4",
    max_chunk_size: int = 1600
) -> bool:
    """
    Post per-agent details to Discord (chunked for readability).
    
    Args:
        agents_data: List of agent status dicts
        agent_id: Target agent channel (default: Agent-4)
        max_chunk_size: Maximum characters per chunk
    
    Returns:
        True if successful, False otherwise
    """
    if not DISCORD_AVAILABLE:
        return False
    
    try:
        poster = DiscordRouterPoster(agent_id=agent_id)
        
        for data in agents_data:
            agent_id_str = data.get("agent_id", "Unknown")
            agent_name = data.get("agent_name", "Unknown")
            
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
                    
                    if len(agent_msg) + len(task_str) > max_chunk_size:
                        poster.post_update(
                            agent_id=agent_id,
                            message=agent_msg,
                            title=f"📄 {agent_id_str}: {agent_name}",
                            priority="normal"
                        )
                        agent_msg = f"**{agent_id_str} (Continued):**\n"
                    
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
                    
                    if len(agent_msg) + len(ach_str) > max_chunk_size:
                        poster.post_update(
                            agent_id=agent_id,
                            message=agent_msg,
                            title=f"📄 {agent_id_str}: {agent_name}",
                            priority="normal"
                        )
                        agent_msg = f"**{agent_id_str} (Continued):**\n"
                    
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
                    
                    if len(agent_msg) + len(task_str) > max_chunk_size:
                        poster.post_update(
                            agent_id=agent_id,
                            message=agent_msg,
                            title=f"📄 {agent_id_str}: {agent_name}",
                            priority="normal"
                        )
                        agent_msg = f"**{agent_id_str} (Continued):**\n"
                    
                    agent_msg += task_str
            
            # Post remaining content
            if agent_msg.strip():
                poster.post_update(
                    agent_id=agent_id,
                    message=agent_msg,
                    title=f"📄 {agent_id_str}: {agent_name}",
                    priority="normal"
                )
        
        return True
    except Exception as e:
        print(f"❌ Error posting agent details to Discord: {e}")
        return False


def post_full_report_file(
    report_path: Path,
    agent_id: str = "Agent-4"
) -> bool:
    """
    Upload full report file to Discord.
    
    Args:
        report_path: Path to report file
        agent_id: Target agent channel (default: Agent-4)
    
    Returns:
        True if successful, False otherwise
    """
    if not DISCORD_AVAILABLE:
        return False
    
    try:
        poster = DiscordRouterPoster(agent_id=agent_id)
        
        poster.post_update(
            agent_id=agent_id,
            message="📎 **Full Cycle Accomplishments Report (Attached)**",
            title="📊 Full Report Download",
            priority="normal",
            file_path=str(report_path)
        )
        
        return True
    except Exception as e:
        print(f"❌ Error uploading report file to Discord: {e}")
        return False


def post_to_discord(
    agents_data: List[Dict[str, Any]],
    date_str: str,
    active_agents: int,
    total_completed: int,
    total_achievements: int,
    report_path: Path,
    agent_id: str = "Agent-4",
    include_details: bool = True,
    include_file: bool = True
) -> bool:
    """
    Post complete cycle report to Discord (summary + details + file).
    
    Args:
        agents_data: List of agent status dicts
        date_str: Date string for the report
        active_agents: Number of active agents
        total_completed: Total completed tasks
        total_achievements: Total achievements
        report_path: Path to full report file
        agent_id: Target agent channel (default: Agent-4)
        include_details: Whether to post per-agent details
        include_file: Whether to upload full report file
    
    Returns:
        True if at least one post succeeded, False otherwise
    """
    if not DISCORD_AVAILABLE:
        print("⚠️  Discord posting not available - DiscordRouterPoster not found")
        return False
    
    success_count = 0
    
    # 1. Post Summary
    if post_summary(date_str, active_agents, total_completed, total_achievements, report_path, agent_id):
        success_count += 1
    
    # 2. Post Agent Details (chunked)
    if include_details:
        if post_agent_details(agents_data, agent_id):
            success_count += 1
    
    # 3. Upload Full Report File
    if include_file:
        if post_full_report_file(report_path, agent_id):
            success_count += 1
    
    return success_count > 0

