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

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
Refactored into modular generators package for maintainability
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from .generators import WorkResumeBuilder

logger = logging.getLogger(__name__)


class WorkResumeGenerator:
    """
    Generate comprehensive work resume from agent status and activity.

    This class provides a simplified interface to the modular resume generation system.
    """

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize with workspace root path.

        Args:
            workspace_root: Root directory for agent workspaces
        """
        self.builder = WorkResumeBuilder(workspace_root)

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
            include_recent_commits: Whether to include git commit history
            include_coordination: Whether to include coordination activity
            include_devlogs: Whether to include devlog entries
            days_back: Number of days to look back for data

        Returns:
            Complete work resume as formatted string
        """
        return self.builder.generate_work_resume(
            agent_id=agent_id,
            include_recent_commits=include_recent_commits,
            include_coordination=include_coordination,
            include_devlogs=include_devlogs,
            days_back=days_back,
        )

    def save_resume_to_file(self, agent_id: str, output_file: Optional[Path] = None) -> Path:
        """
        Generate and save work resume to file.

        Args:
            agent_id: Agent identifier
            output_file: Optional output file path

        Returns:
            Path to saved resume file
        """
        return self.builder.save_resume_to_file(agent_id, output_file)
    
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
        """Get recent git commits with actual git integration."""
        import subprocess
        import re
        from datetime import datetime, timedelta

        try:
            # Get git log with detailed format
            since_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
            cmd = [
                "git", "log",
                f"--since={since_date}",
                "--pretty=format:%H|%an|%ad|%s",
                "--date=short",
                "--no-merges"  # Exclude merge commits for cleaner output
            ]

            result = subprocess.run(cmd, capture_output=True, text=True, cwd=self.repo_root)
            if result.returncode != 0:
                logger.warning(f"Git log failed: {result.stderr}")
                return []

            commits = []
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue

                parts = line.split('|', 3)
                if len(parts) >= 4:
                    commits.append({
                        "hash": parts[0],
                        "author": parts[1],
                        "date": parts[2],
                        "message": parts[3]
                    })

            return commits[:20]  # Limit to 20 most recent commits

        except Exception as e:
            logger.error(f"Error getting git commits: {e}")
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
        """Get recent coordination activity with actual log integration."""
        import json
        from datetime import datetime, timedelta
        from pathlib import Path

        activities = []
        cutoff_date = datetime.now() - timedelta(days=days_back)

        try:
            # Check coordination cache
            cache_file = Path("coordination_cache.json")
            if cache_file.exists():
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)

                for entry in cache_data.get("coordinations", []):
                    # Check if entry is recent enough
                    if isinstance(entry.get("timestamp"), str):
                        try:
                            entry_date = datetime.fromisoformat(entry["timestamp"].replace('Z', '+00:00'))
                            if entry_date >= cutoff_date:
                                activities.append({
                                    "type": "coordination",
                                    "timestamp": entry_date.isoformat(),
                                    "description": entry.get("description", "Coordination activity"),
                                    "participants": entry.get("participants", []),
                                    "status": entry.get("status", "completed")
                                })
                        except (ValueError, AttributeError):
                            continue

            # Check A2A coordination status
            status_file = Path("a2a_coordination_status.json")
            if status_file.exists():
                with open(status_file, 'r', encoding='utf-8') as f:
                    status_data = json.load(f)

                for coord_id, coord_data in status_data.items():
                    if isinstance(coord_data.get("timestamp"), str):
                        try:
                            coord_date = datetime.fromisoformat(coord_data["timestamp"].replace('Z', '+00:00'))
                            if coord_date >= cutoff_date:
                                activities.append({
                                    "type": "a2a_coordination",
                                    "timestamp": coord_date.isoformat(),
                                    "description": coord_data.get("description", f"A2A coordination {coord_id}"),
                                    "participants": coord_data.get("participants", []),
                                    "status": coord_data.get("status", "active")
                                })
                        except (ValueError, AttributeError):
                            continue

            # Sort by timestamp (most recent first)
            activities.sort(key=lambda x: x["timestamp"], reverse=True)

            return activities[:15]  # Limit to 15 most recent activities

        except Exception as e:
            logger.error(f"Error getting coordination activity: {e}")
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


