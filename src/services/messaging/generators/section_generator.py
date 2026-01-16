#!/usr/bin/env python3
"""
Work Resume Section Generator - Content Generation Infrastructure
===============================================================

<!-- SSOT Domain: messaging -->

Generates individual sections of work resumes with specialized formatting
for headers, current state, recent work, tasks, and activity summaries.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class WorkResumeSectionGenerator:
    """Generates individual sections of work resumes."""

    def generate_header(self, agent_id: str, status: Dict[str, Any]) -> str:
        """
        Generate resume header with agent information.

        Args:
            agent_id: Agent identifier
            status: Agent status data

        Returns:
            Formatted header section
        """
        agent_name = status.get('agent_name', f'Agent {agent_id}')
        last_updated = status.get('last_updated', 'Unknown')

        header = f"""# Work Resume: {agent_name} ({agent_id})

**Last Updated:** {last_updated}
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
        return header

    def generate_current_state(self, status: Dict[str, Any]) -> str:
        """
        Generate current state section.

        Args:
            status: Agent status data

        Returns:
            Formatted current state section
        """
        current_phase = status.get('current_phase', 'Unknown')
        mission = status.get('current_mission', 'No active mission')
        priority = status.get('mission_priority', 'Unknown')

        section = f"""## Current State

**Phase:** {current_phase}
**Mission:** {mission}
**Priority:** {priority}

"""
        return section

    def generate_recent_work(self, status: Dict[str, Any], days_back: int) -> str:
        """
        Generate recent work summary.

        Args:
            status: Agent status data
            days_back: Number of days to look back

        Returns:
            Formatted recent work section
        """
        current_tasks = status.get('current_tasks', [])
        completed_tasks = status.get('completed_tasks', [])
        achievements = status.get('achievements', [])

        section = f"""## Recent Work (Last {days_back} Days)

### Current Tasks
"""
        if current_tasks:
            for task in current_tasks:
                section += f"- {task}\n"
        else:
            section += "- No current tasks\n"

        section += "\n### Recently Completed\n"
        if completed_tasks:
            for task in completed_tasks[-5:]:  # Show last 5 completed tasks
                section += f"- ✅ {task}\n"
        else:
            section += "- No recently completed tasks\n"

        section += "\n### Key Achievements\n"
        if achievements:
            for achievement in achievements[-3:]:  # Show last 3 achievements
                section += f"- 🏆 {achievement}\n"
        else:
            section += "- No recent achievements\n"

        section += "\n"
        return section

    def generate_current_tasks(self, status: Dict[str, Any]) -> str:
        """
        Generate detailed current tasks section.

        Args:
            status: Agent status data

        Returns:
            Formatted current tasks section
        """
        current_tasks = status.get('current_tasks', [])

        section = "## Active Tasks\n\n"

        if current_tasks:
            for i, task in enumerate(current_tasks, 1):
                section += f"{i}. **{task}**\n"
        else:
            section += "*No active tasks*\n"

        section += "\n"
        return section

    def generate_next_actions(self, status: Dict[str, Any]) -> str:
        """
        Generate next actions section.

        Args:
            status: Agent status data

        Returns:
            Formatted next actions section
        """
        next_actions = status.get('next_actions', [])

        section = "## Next Actions\n\n"

        if next_actions:
            for action in next_actions:
                section += f"- {action}\n"
        else:
            section += "*No planned next actions*\n"

        section += "\n"
        return section

    def generate_commits_section(self, commits: List[Dict[str, Any]], agent_id: str) -> str:
        """
        Generate git commits section.

        Args:
            commits: List of commit data
            agent_id: Agent identifier

        Returns:
            Formatted commits section
        """
        section = "## Git Activity\n\n"

        if not commits:
            section += "*No recent commits found*\n\n"
            return section

        # Group commits by author (focus on agent's commits)
        agent_commits = [c for c in commits if agent_id.lower() in c.get('author', '').lower()]

        if agent_commits:
            section += f"### {agent_id}'s Commits ({len(agent_commits)})\n\n"
            for commit in agent_commits[:10]:  # Show last 10 commits
                message = commit.get('message', 'No message')[:80]
                date = commit.get('date', 'Unknown date')[:10]
                short_hash = commit.get('hash', '')[0:8]
                section += f"- `{short_hash}` - {message} ({date})\n"
        else:
            section += f"*No commits found for {agent_id}*\n"

        section += "\n"
        return section

    def generate_coordination_section(self, coordination: List[Dict[str, Any]]) -> str:
        """
        Generate coordination activity section.

        Args:
            coordination: List of coordination activities

        Returns:
            Formatted coordination section
        """
        section = "## Coordination Activity\n\n"

        if not coordination:
            section += "*No recent coordination activity*\n\n"
            return section

        for activity in coordination[:5]:  # Show last 5 activities
            activity_type = activity.get('type', 'Unknown')
            description = activity.get('description', 'No description')
            timestamp = activity.get('timestamp', 'Unknown time')

            section += f"- **{activity_type}**: {description} ({timestamp})\n"

        section += "\n"
        return section

    def generate_devlog_section(self, devlogs: List[Dict[str, Any]]) -> str:
        """
        Generate devlog activity section.

        Args:
            devlogs: List of devlog entries

        Returns:
            Formatted devlog section
        """
        section = "## Devlog Activity\n\n"

        if not devlogs:
            section += "*No recent devlog entries*\n\n"
            return section

        section += f"### Recent Devlogs ({len(devlogs)} entries)\n\n"

        for devlog in devlogs[:3]:  # Show last 3 devlogs
            filename = devlog.get('filename', 'Unknown file')
            modified = devlog.get('modified', 'Unknown date')[:10]
            content_preview = devlog.get('content', '')[:200].replace('\n', ' ').strip()

            section += f"#### {filename} ({modified})\n"
            section += f"{content_preview}...\n\n"

        return section

    def generate_footer(self, status: Dict[str, Any]) -> str:
        """
        Generate resume footer.

        Args:
            status: Agent status data

        Returns:
            Formatted footer section
        """
        footer = f"""---

*Work Resume generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*Status: {status.get('status', 'Unknown')}*

"""
        return footer