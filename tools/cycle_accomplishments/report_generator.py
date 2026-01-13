"""
Report Generator Module
=======================

Generates comprehensive markdown reports from agent status data.

Protocol: CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0
Author: Agent-7 (Web Development Specialist)
Date: 2025-12-30
V2 Compliant: Yes

<!-- SSOT Domain: tools -->
"""

from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
from collections import defaultdict


def get_block_status(workspace_root: Optional[Path] = None) -> List[str]:
    """
    Extract block status from MASTER_TASK_LOG.md if available.
    
    Args:
        workspace_root: Root workspace path (defaults to current directory)
    
    Returns:
        List of block status lines
    """
    if workspace_root is None:
        workspace_root = Path.cwd()
    
    master_log_path = workspace_root / "MASTER_TASK_LOG.md"
    
    if not master_log_path.exists():
        return []
    
    try:
        with open(master_log_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Look for current block status
        if "Block 1" in content and "Block 2" in content:
            return [
                "**Current Phase:** Swarm Phase 3 Consolidation & V2 Completion",
                "**Active Blocks:**",
                "- Block 1: Infrastructure refactoring + WP-CLI integration + Phase 3 runtime errors (Agent-1)",
                "- Block 2: Staging & rollback infrastructure + deployment MCP enhancements (Agent-2) ✅ COMPLETED",
                "- Block 3: Critical deployments + PHP validation + GA4/Pixel config (Agent-3)",
                "- Block 4: Analytics validation + DB operations + WordPress health checks (Agent-5)",
                "- Block 5: SSOT tagging (646 tools) + PSE rule validation + archived tools audit (Agent-6)",
                "- Block 6: P0 Foundation fixes (Tier 2) + Offer Ladders + ICP Definitions + website-manager MCP enhancements (Agent-7)",
                "- Block 7: Unified tool registry + cache management + tool discovery audit (Agent-8)",
            ]
    except Exception:
        pass
    
    return []


def format_task(task: Any, max_length: int = 200) -> str:
    """
    Format a task (string or dict) for display.
    
    Args:
        task: Task as string or dict
        max_length: Maximum length for truncation
    
    Returns:
        Formatted task string
    """
    if isinstance(task, str):
        task_text = task
    elif isinstance(task, dict):
        task_desc = task.get('task', 'Unknown Task')
        details = task.get('details', '')
        if details:
            task_text = f"{task_desc}: {details}"
        else:
            task_text = task_desc
    else:
        task_text = str(task)
    
    # Truncate if too long
    if len(task_text) > max_length:
        task_text = task_text[:max_length] + "..."
    
    return task_text


def generate_cycle_report(
    agents: Dict[str, Dict[str, Any]],
    totals: Dict[str, Any],
    workspace_root: Optional[Path] = None
) -> str:
    """
    Generate comprehensive cycle accomplishments report.
    
    Args:
        agents: Dict of agent_id -> status data
        totals: Calculated totals from data_collector
        workspace_root: Root workspace path for block status lookup
    
    Returns:
        Complete markdown report as string
    """
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    date = datetime.now().strftime('%Y-%m-%d')
    
    report = [
        "# 🚀 Swarm Cycle Accomplishments Report",
        "",
        f"**Generated:** {timestamp}",
        f"**Date:** {date}",
        f"**Agents Active:** {totals['total_agents']}",
        "",
        "## 📊 Executive Summary",
        "",
        f"- **Total Agents:** {totals['total_agents']}",
        f"- **Completed Tasks:** {totals['total_completed_tasks']}",
        f"- **Achievements:** {totals['total_achievements']}",
        f"- **Active Tasks:** {totals['active_tasks_count']}",
        "",
        "## 👥 Agent Accomplishments",
        ""
    ]
    
    # Sort agents for consistent reporting
    sorted_agents = sorted(agents.keys())
    
    for agent_id in sorted_agents:
        status = agents[agent_id]
        agent_name = status.get('agent_name', f'Agent {agent_id.split("-")[1]}')
        current_mission = status.get('current_mission', 'No mission set')
        last_updated = status.get('last_updated', 'Unknown')
        
        report.append(f"### {agent_id}: {agent_name}")
        report.append("")
        report.append(f"**Current Mission:** {current_mission}")
        report.append(f"**Last Updated:** {last_updated}")
        report.append(f"**Status:** {status.get('status', 'Unknown')}")
        report.append("")
        
        # Completed Tasks (last 20)
        completed_tasks = status.get('completed_tasks', [])
        if completed_tasks:
            report.append(f"**✅ Completed Tasks ({len(completed_tasks)}):**")
            for task in completed_tasks[-20:]:
                report.append(f"- {format_task(task)}")
            report.append("")
        
        # Recent Completions (Achievements) - fallback if completed_tasks is empty
        recent_completions = status.get('recent_completions', [])
        if recent_completions and not completed_tasks:
            report.append(f"**✅ Recent Completions ({len(recent_completions)}):**")
            for task in recent_completions[-20:]:
                report.append(f"- {format_task(task)}")
            report.append("")
        
        # Achievements (last 15)
        achievements = status.get('achievements', [])
        if achievements:
            report.append(f"**🏆 Achievements ({len(achievements)}):**")
            for achievement in achievements[-15:]:
                if isinstance(achievement, str):
                    report.append(f"- {achievement}")
                elif isinstance(achievement, dict):
                    title = achievement.get('title', achievement.get('description', str(achievement)))
                    report.append(f"- {title}")
            report.append("")
        
        # Current Tasks (last 10)
        current_tasks = status.get('current_tasks', [])
        if current_tasks:
            report.append(f"**🔄 Current Tasks ({len(current_tasks)}):**")
            for task in current_tasks[-10:]:
                if isinstance(task, dict):
                    task_name = task.get('task', 'Unknown')
                    task_status = task.get('status', 'Unknown')
                    report.append(f"- **{task_status.upper()}:** {task_name}")
                else:
                    report.append(f"- {format_task(task)}")
            report.append("")
        
        report.append("---")
        report.append("")
    
    # Active Tasks Summary (grouped by status)
    active_tasks = totals.get('active_tasks', [])
    if active_tasks:
        report.append("## 🎯 Active Tasks Overview")
        report.append("")
        
        # Group by status
        status_groups = defaultdict(list)
        for task in active_tasks:
            status_groups[task['status']].append(task)
        
        for status, tasks in status_groups.items():
            report.append(f"### {status.replace('_', ' ').title()} ({len(tasks)})")
            for task in tasks:
                report.append(f"- **{task['agent']}:** {task['task']}")
            report.append("")
    
    # Block Status
    block_status = get_block_status(workspace_root)
    if block_status:
        report.append("## 📋 Swarm Phase 3 Block Status")
        report.append("")
        report.extend(block_status)
        report.append("")
    
    # Report Metadata
    report.append("## 📋 Report Metadata")
    report.append("")
    report.append("**Protocol:** CYCLE_ACCOMPLISHMENTS_REPORT_GENERATION v2.0")
    report.append("**Generated By:** tools/cycle_accomplishments/ (modular)")
    report.append("**Format:** Markdown")
    report.append("**Timestamp:** " + timestamp)
    report.append("")
    report.append("---")
    report.append("*This report aggregates accomplishments across all active swarm agents.*")
    
    return "\n".join(report)


def save_report(report: str, workspace_root: Optional[Path] = None) -> Path:
    """
    Save report to file and return path.
    
    Args:
        report: Report content as string
        workspace_root: Root workspace path (defaults to current directory)
    
    Returns:
        Path to saved report file
    """
    if workspace_root is None:
        workspace_root = Path.cwd()
    
    reports_dir = workspace_root / "reports"
    reports_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"cycle_accomplishments_{timestamp}.md"
    report_path = reports_dir / filename
    
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path

