#!/usr/bin/env python3
"""
Work Resume Generator - Messaging Infrastructure
=================================================

<!-- SSOT Domain: integration -->

Generates comprehensive work resume summaries from agent status, devlogs, and activity.
This creates a detailed "resume" of work done that can be used for:
- Bringing agents up to speed after inactivity
- Tracking progress and accomplishments
- Providing context for coordination
- Status reporting and monitoring

V2 Compliance | Author: Agent-1 | Date: 2025-12-21
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


class WorkResumeGenerator:
    """Generate comprehensive work resume from agent status and activity."""
    
    def __init__(self, workspace_root: Optional[Path] = None):
        """Initialize with workspace root path."""
        if workspace_root is None:
            workspace_root = Path("agent_workspaces")
        self.workspace_root = Path(workspace_root)
    
    def generate_work_resume(
        self,
        agent_id: str,
        include_recent_commits: bool = True,
        include_coordination: bool = True,
        include_devlogs: bool = True,
        days_back: int = 7,
    ) -> str:
        """
        Generate comprehensive work resume for an agent.
        
        Args:
            agent_id: Agent identifier (e.g., "Agent-1")
            include_recent_commits: Include recent git commits
            include_coordination: Include coordination messages sent/received
            include_devlogs: Include devlog entries
            days_back: How many days back to look for activity
            
        Returns:
            Formatted work resume string
        """
        agent_workspace = self.workspace_root / agent_id
        
        # Load status.json
        status = self._load_status(agent_id)
        
        # Build resume sections
        sections = []
        
        # Header
        sections.append(self._generate_header(agent_id, status))
        
        # Current State
        sections.append(self._generate_current_state(status))
        
        # Recent Work Completed
        sections.append(self._generate_recent_work(status, days_back))
        
        # Current Tasks
        sections.append(self._generate_current_tasks(status))
        
        # Recent Commits (if enabled)
        if include_recent_commits:
            commits = self._get_recent_commits(days_back)
            if commits:
                sections.append(self._generate_commits_section(commits, agent_id))
        
        # Coordination Activity (if enabled)
        if include_coordination:
            coord = self._get_coordination_activity(agent_id, days_back)
            if coord:
                sections.append(self._generate_coordination_section(coord))
        
        # Devlog Summary (if enabled)
        if include_devlogs:
            devlogs = self._get_recent_devlogs(agent_id, days_back)
            if devlogs:
                sections.append(self._generate_devlog_section(devlogs))
        
        # Next Actions
        sections.append(self._generate_next_actions(status))
        
        # Footer
        sections.append(self._generate_footer(status))
        
        return "\n\n".join(sections)
    
    def _load_status(self, agent_id: str) -> Dict[str, Any]:
        """Load agent status.json."""
        status_file = self.workspace_root / agent_id / "status.json"
        if not status_file.exists():
            return {}
        
        try:
            with open(status_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.warning(f"Error loading {agent_id} status: {e}")
            return {}
    
    def _generate_header(self, agent_id: str, status: Dict[str, Any]) -> str:
        """Generate resume header."""
        agent_name = status.get("agent_name", f"{agent_id} Specialist")
        last_updated = status.get("last_updated", "Unknown")
        
        return f"""# 📋 WORK RESUME - {agent_id}

**Agent**: {agent_name}  
**Last Updated**: {last_updated}  
**Generated**: {datetime.now().isoformat()}  
**Purpose**: Comprehensive summary of work completed, current state, and next actions"""
    
    def _generate_current_state(self, status: Dict[str, Any]) -> str:
        """Generate current state section."""
        fsm_state = status.get("fsm_state", status.get("status", "UNKNOWN"))
        current_mission = status.get("current_mission", "Not specified")
        current_phase = status.get("current_phase", "Not specified")
        availability = status.get("availability", "Unknown")
        coordination_status = status.get("coordination_status", "Unknown")
        cycle_count = status.get("cycle_count", 0)
        points_earned = status.get("points_earned", 0)
        
        return f"""## 🔄 CURRENT STATE

- **FSM State**: {fsm_state}
- **Current Mission**: {current_mission}
- **Current Phase**: {current_phase}
- **Availability**: {availability}
- **Coordination Status**: {coordination_status}
- **Cycle Count**: {cycle_count}
- **Points Earned**: {points_earned}"""
    
    def _generate_recent_work(self, status: Dict[str, Any], days_back: int) -> str:
        """Generate recent work completed section."""
        completed = status.get("completed_tasks", [])
        recent_completions = status.get("recent_completions", [])
        
        # Combine and filter by date if possible
        all_completed = completed + recent_completions
        
        if not all_completed:
            return "## ✅ RECENT WORK COMPLETED\n\nNo completed tasks recorded."
        
        # Format completed tasks
        items = []
        for item in all_completed[:20]:  # Limit to 20 most recent
            if isinstance(item, dict):
                task = item.get("task", "Unknown task")
                completed_date = item.get("completed", "Unknown date")
                details = item.get("details", "")
                if details:
                    items.append(f"- **{task}** ({completed_date}): {details}")
                else:
                    items.append(f"- **{task}** ({completed_date})")
            else:
                items.append(f"- {item}")
        
        return f"""## ✅ RECENT WORK COMPLETED

{chr(10).join(items)}"""
    
    def _generate_current_tasks(self, status: Dict[str, Any]) -> str:
        """Generate current tasks section."""
        tasks = status.get("current_tasks", [])
        
        if not tasks:
            return "## 📋 CURRENT TASKS\n\nNo active tasks."
        
        items = []
        for task in tasks:
            if isinstance(task, dict):
                task_name = task.get("task", "Unknown task")
                task_status = task.get("status", "Unknown")
                started = task.get("started", "")
                coordination_with = task.get("coordination_with", "")
                next_action = task.get("next", "")
                
                item = f"- **{task_name}**"
                item += f"\n  - Status: {task_status}"
                if started:
                    item += f"\n  - Started: {started}"
                if coordination_with:
                    coord_str = coordination_with if isinstance(coordination_with, str) else ", ".join(coordination_with)
                    item += f"\n  - Coordination: {coord_str}"
                if next_action:
                    item += f"\n  - Next: {next_action}"
                items.append(item)
            else:
                items.append(f"- {task}")
        
        return f"""## 📋 CURRENT TASKS

{chr(10).join(items)}"""
    
    def _generate_next_actions(self, status: Dict[str, Any]) -> str:
        """Generate next actions section."""
        next_priorities = status.get("next_priorities", [])
        
        if not next_priorities:
            # Try to extract from current_tasks
            tasks = status.get("current_tasks", [])
            if tasks and isinstance(tasks[0], dict):
                next_action = tasks[0].get("next", "")
                if next_action:
                    return f"""## 🎯 NEXT ACTIONS

{next_action}"""
            return "## 🎯 NEXT ACTIONS\n\nNo specific next actions defined."
        
        items = "\n".join([f"- {priority}" for priority in next_priorities])
        return f"""## 🎯 NEXT ACTIONS

{items}"""
    
    def _get_recent_commits(self, days_back: int) -> List[Dict[str, Any]]:
        """Get recent git commits (placeholder - would need git integration)."""
        # TODO: Integrate with git to get recent commits
        # This would use something like: git log --since="{days_back} days ago" --pretty=format:"%H|%an|%ad|%s"
        return []
    
    def _generate_commits_section(self, commits: List[Dict[str, Any]], agent_id: str) -> str:
        """Generate commits section."""
        items = []
        for commit in commits[:10]:  # Limit to 10 most recent
            hash_short = commit.get("hash", "")[:8]
            author = commit.get("author", "")
            date = commit.get("date", "")
            message = commit.get("message", "")
            items.append(f"- `{hash_short}` ({date}): {message}")
        
        return f"""## 📦 RECENT COMMITS

{chr(10).join(items)}"""
    
    def _get_coordination_activity(self, agent_id: str, days_back: int) -> List[Dict[str, Any]]:
        """Get recent coordination activity (placeholder - would need message queue/log integration)."""
        # TODO: Integrate with message queue/log to get recent A2A messages
        return []
    
    def _generate_coordination_section(self, coord: List[Dict[str, Any]]) -> str:
        """Generate coordination activity section."""
        items = []
        for activity in coord[:10]:  # Limit to 10 most recent
            direction = activity.get("direction", "")  # "sent" or "received"
            target = activity.get("target", "")
            message_id = activity.get("message_id", "")
            timestamp = activity.get("timestamp", "")
            items.append(f"- {direction.upper()} to/from {target} ({timestamp}): {message_id[:8]}")
        
        return f"""## 🤝 COORDINATION ACTIVITY

{chr(10).join(items)}"""
    
    def _get_recent_devlogs(self, agent_id: str, days_back: int) -> List[Dict[str, Any]]:
        """Get recent devlog entries."""
        devlog_dir = self.workspace_root / agent_id / "devlogs"
        if not devlog_dir.exists():
            return []
        
        devlogs = []
        cutoff_date = datetime.now() - timedelta(days=days_back)
        
        for devlog_file in sorted(devlog_dir.glob("*.md"), key=lambda p: p.stat().st_mtime, reverse=True):
            try:
                # Get file modification time
                mtime = datetime.fromtimestamp(devlog_file.stat().st_mtime)
                if mtime < cutoff_date:
                    continue
                
                # Read first few lines for summary
                with open(devlog_file, 'r', encoding='utf-8') as f:
                    content = f.read()[:500]  # First 500 chars
                    lines = content.split('\n')[:5]  # First 5 lines
                    summary = '\n'.join(lines)
                
                devlogs.append({
                    "file": devlog_file.name,
                    "date": mtime.isoformat(),
                    "summary": summary
                })
            except Exception as e:
                logger.warning(f"Error reading devlog {devlog_file}: {e}")
                continue
        
        return devlogs[:5]  # Limit to 5 most recent
    
    def _generate_devlog_section(self, devlogs: List[Dict[str, Any]]) -> str:
        """Generate devlog summary section."""
        items = []
        for devlog in devlogs:
            file_name = devlog.get("file", "")
            date = devlog.get("date", "")[:10]  # Just the date part
            summary = devlog.get("summary", "")[:200]  # First 200 chars
            items.append(f"- **{file_name}** ({date}):\n  {summary}...")
        
        return f"""## 📝 RECENT DEVLOG ENTRIES

{chr(10).join(items)}"""
    
    def _generate_footer(self, status: Dict[str, Any]) -> str:
        """Generate resume footer."""
        return f"""---

**RESUME GENERATED**: {datetime.now().isoformat()}  
**Use Case**: This resume provides comprehensive context for:
- Bringing agents back up to speed after inactivity
- Coordinating with other agents (shows what you've been working on)
- Status reporting and progress tracking
- Identifying next actions and priorities

**Next Steps**: Review current tasks, execute next actions, update status.json with progress"""
    
    def save_resume_to_file(self, agent_id: str, output_file: Optional[Path] = None) -> Path:
        """Generate and save work resume to file."""
        resume = self.generate_work_resume(agent_id)
        
        if output_file is None:
            output_file = self.workspace_root / agent_id / f"WORK_RESUME_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(resume)
        
        logger.info(f"✅ Work resume saved to {output_file}")
        return output_file


def generate_work_resume(
    agent_id: str,
    workspace_root: Optional[Path] = None,
    **kwargs
) -> str:
    """Convenience function to generate work resume."""
    generator = WorkResumeGenerator(workspace_root=workspace_root)
    return generator.generate_work_resume(agent_id, **kwargs)


