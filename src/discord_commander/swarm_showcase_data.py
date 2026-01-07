"""
Swarm Showcase Data Loader - Agent Cellphone V2
==============================================

SSOT Domain: swarm

Data loading and processing for swarm showcase displays.

Features:
- Agent status data aggregation
- Roadmap data processing
- Task and directive tracking
- Performance metrics collection

V2 Compliant: Yes (<300 lines)
Author: Agent-1 (Integration & Core Systems Specialist)
Date: 2026-01-07
"""

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class SwarmShowcaseData:
    """
    Loads and processes data for swarm showcase displays.
    """

    def __init__(self):
        self.agent_workspaces = Path("agent_workspaces")
        self.master_task_log = Path("MASTER_TASK_LOG.md")
        self._agent_statuses = None
        self._roadmap_data = None

    def get_all_agent_statuses(self) -> List[Dict[str, Any]]:
        """Get status data for all agents."""
        if self._agent_statuses is not None:
            return self._agent_statuses

        statuses = []
        if self.agent_workspaces.exists():
            for agent_dir in self.agent_workspaces.iterdir():
                if agent_dir.is_dir() and agent_dir.name.startswith("Agent-"):
                    status_file = agent_dir / "status.json"
                    if status_file.exists():
                        try:
                            with open(status_file, 'r', encoding='utf-8') as f:
                                status_data = json.load(f)
                                status_data['agent_id'] = agent_dir.name
                                statuses.append(status_data)
                        except Exception as e:
                            logger.warning(f"Failed to load status for {agent_dir.name}: {e}")

        self._agent_statuses = statuses
        return statuses

    def get_roadmap_data(self) -> Dict[str, Any]:
        """Get roadmap and integration data."""
        if self._roadmap_data is not None:
            return self._roadmap_data

        roadmap = {
            "phases": [
                {
                    "name": "Phase 1: Foundation",
                    "status": "completed",
                    "description": "Core infrastructure and agent framework",
                    "completion": 100
                },
                {
                    "name": "Phase 2: Integration",
                    "status": "completed",
                    "description": "Service integration and API connections",
                    "completion": 100
                },
                {
                    "name": "Phase 3: Expansion",
                    "status": "in_progress",
                    "description": "Advanced features and scaling",
                    "completion": 85
                },
                {
                    "name": "Phase 4: Optimization",
                    "status": "planned",
                    "description": "Performance tuning and automation",
                    "completion": 0
                }
            ],
            "current_focus": "Enterprise-grade infrastructure deployment",
            "next_milestone": "Complete Revenue Engine production validation"
        }

        self._roadmap_data = roadmap
        return roadmap

    def get_task_data(self) -> Dict[str, Any]:
        """Get current tasks and directives from MASTER_TASK_LOG."""
        tasks = {
            "active": [],
            "completed_today": [],
            "blocked": [],
            "total_active": 0,
            "total_completed": 0
        }

        if self.master_task_log.exists():
            try:
                content = self.master_task_log.read_text(encoding='utf-8')
                # Simple parsing - could be enhanced
                lines = content.split('\n')
                current_section = None

                for line in lines:
                    line = line.strip()
                    if line.startswith('## '):
                        section = line[3:].lower()
                        if 'this week' in section:
                            current_section = 'active'
                        elif 'completed' in section:
                            current_section = 'completed'
                        elif 'waiting' in section:
                            current_section = 'blocked'
                        else:
                            current_section = None
                    elif line.startswith('- [') and current_section:
                        task = line[2:].strip()
                        if current_section == 'active':
                            tasks['active'].append(task)
                        elif current_section == 'completed':
                            tasks['completed_today'].append(task)

                tasks['total_active'] = len(tasks['active'])
                tasks['total_completed'] = len(tasks['completed_today'])

            except Exception as e:
                logger.warning(f"Failed to parse task log: {e}")

        return tasks

    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate performance metrics across all agents."""
        statuses = self.get_all_agent_statuses()

        metrics = {
            "total_agents": len(statuses),
            "active_agents": 0,
            "completed_tasks_today": 0,
            "success_rate": 0,
            "average_completion": 0
        }

        total_completion = 0
        for status in statuses:
            if status.get('status') == 'ACTIVE_AGENT_MODE':
                metrics['active_agents'] += 1

            completed = len(status.get('completed_tasks', []))
            metrics['completed_tasks_today'] += completed
            total_completion += completed

        if metrics['total_agents'] > 0:
            metrics['average_completion'] = total_completion / metrics['total_agents']
            metrics['success_rate'] = (metrics['active_agents'] / metrics['total_agents']) * 100

        return metrics

    def get_agent_excellence_data(self) -> List[Dict[str, Any]]:
        """Get data for agent excellence showcase."""
        statuses = self.get_all_agent_statuses()

        excellence_data = []
        for status in statuses:
            agent_data = {
                "agent_id": status.get('agent_id', 'Unknown'),
                "name": status.get('agent_name', 'Unknown Agent'),
                "status": status.get('status', 'Unknown'),
                "current_mission": status.get('current_mission', 'No active mission'),
                "completed_tasks": len(status.get('completed_tasks', [])),
                "active_tasks": len(status.get('current_tasks', [])),
                "achievements": status.get('achievements', []),
                "priority": status.get('mission_priority', 'Normal')
            }
            excellence_data.append(agent_data)

        # Sort by completed tasks (descending)
        excellence_data.sort(key=lambda x: x['completed_tasks'], reverse=True)
        return excellence_data

    def get_overview_data(self) -> Dict[str, Any]:
        """Get comprehensive overview data."""
        return {
            "agent_statuses": self.get_all_agent_statuses(),
            "roadmap": self.get_roadmap_data(),
            "tasks": self.get_task_data(),
            "performance": self.get_performance_metrics(),
            "timestamp": datetime.now().isoformat(),
            "system_health": "operational"
        }

    def refresh_data(self):
        """Refresh all cached data."""
        self._agent_statuses = None
        self._roadmap_data = None
        logger.info("Swarm showcase data refreshed")