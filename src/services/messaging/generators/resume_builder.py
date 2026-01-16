#!/usr/bin/env python3
"""
Work Resume Builder - Orchestration Infrastructure
==================================================

<!-- SSOT Domain: messaging -->

Orchestrates the work resume generation process by coordinating data collection
and section generation into a cohesive resume document.

V2 Compliance | Author: Agent-1 | Date: 2026-01-16
"""

import logging
from pathlib import Path
from typing import Any, Dict, Optional

from .data_collector import WorkResumeDataCollector
from .section_generator import WorkResumeSectionGenerator

logger = logging.getLogger(__name__)


class WorkResumeBuilder:
    """Orchestrates work resume generation from multiple data sources."""

    def __init__(self, workspace_root: Optional[Path] = None):
        """
        Initialize resume builder.

        Args:
            workspace_root: Root directory for agent workspaces
        """
        self.data_collector = WorkResumeDataCollector(workspace_root)
        self.section_generator = WorkResumeSectionGenerator()

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
        # Collect all data
        data = self.data_collector.collect_agent_data(agent_id, days_back)

        # Extract data components
        status = data['status']
        commits = data['commits'] if include_recent_commits else []
        coordination = data['coordination'] if include_coordination else []
        devlogs = data['devlogs'] if include_devlogs else []

        # Build resume sections
        resume_parts = []

        # Header
        resume_parts.append(self.section_generator.generate_header(agent_id, status))

        # Current state
        resume_parts.append(self.section_generator.generate_current_state(status))

        # Recent work summary
        resume_parts.append(self.section_generator.generate_recent_work(status, days_back))

        # Detailed current tasks
        resume_parts.append(self.section_generator.generate_current_tasks(status))

        # Next actions
        resume_parts.append(self.section_generator.generate_next_actions(status))

        # Git activity
        if include_recent_commits:
            resume_parts.append(self.section_generator.generate_commits_section(commits, agent_id))

        # Coordination activity
        if include_coordination:
            resume_parts.append(self.section_generator.generate_coordination_section(coordination))

        # Devlog activity
        if include_devlogs:
            resume_parts.append(self.section_generator.generate_devlog_section(devlogs))

        # Footer
        resume_parts.append(self.section_generator.generate_footer(status))

        # Combine all sections
        return ''.join(resume_parts)

    def save_resume_to_file(self, agent_id: str, output_file: Optional[Path] = None) -> Path:
        """
        Generate and save work resume to file.

        Args:
            agent_id: Agent identifier
            output_file: Optional output file path

        Returns:
            Path to saved resume file
        """
        if output_file is None:
            output_file = Path(f"work_resume_{agent_id}_{Path.cwd().name}.md")

        resume_content = self.generate_work_resume(agent_id)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(resume_content)

        logger.info(f"Work resume saved to {output_file}")
        return output_file