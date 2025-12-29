#!/usr/bin/env python3
"""
<!-- SSOT Domain: core -->

Progress Monitor Stage - Monitor Agent Progress
==============================================

Stage 1: Monitor agent status and calculate progress.
"""

import json
from pathlib import Path
from typing import Dict, Optional

from ..core.models import PipelineAgent


def read_agent_status(agent_id: str, workspace_path: Path) -> Optional[Dict]:
    """Read agent's status.json file."""
    status_file = workspace_path / agent_id / "status.json"

    if not status_file.exists():
        return None

    try:
        with open(status_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"⚠️ Error reading {agent_id} status: {e}")
        return None


def calculate_progress(
    agent_id: str,
    agent: PipelineAgent,
    workspace_path: Path
) -> float:
    """
    Calculate agent's progress percentage.

    Looks for:
    1. Completed repos in completed_tasks
    2. Current repo in current_tasks
    3. repos_XX_YY_mission in status

    Returns: 0.0 to 100.0
    """
    status = read_agent_status(agent_id, workspace_path)
    if not status:
        return 0.0

    start_repo, end_repo = agent.repos_assigned
    total_repos = end_repo - start_repo + 1

    # Check completed_tasks for repo completion signals
    completed = 0
    completed_tasks = status.get('completed_tasks', [])

    for task in completed_tasks:
        task_str = str(task).lower()
        # Look for "repo #XX" or "repos XX-YY complete"
        for repo_num in range(start_repo, end_repo + 1):
            if f'repo #{repo_num}' in task_str or f'repo {repo_num}' in task_str:
                completed += 1
                break

    # Check current_tasks for in-progress repos
    current_tasks = status.get('current_tasks', [])
    current = 0

    for task in current_tasks:
        task_str = str(task).lower()
        for repo_num in range(start_repo, end_repo + 1):
            if f'repo #{repo_num}' in task_str or f'repo {repo_num}' in task_str:
                current = repo_num - start_repo + 1
                break

    # Calculate progress
    if completed > 0:
        agent.current_repo = completed
        return (completed / total_repos) * 100.0
    elif current > 0:
        agent.current_repo = current
        return (current / total_repos) * 100.0
    else:
        # Check mission-specific fields
        mission_key = f"repos_{start_repo}_{end_repo}_mission"
        if mission_key in status:
            mission_data = status[mission_key]
            repos_done = mission_data.get('repos_analyzed', 0)
            agent.current_repo = repos_done
            return (repos_done / total_repos) * 100.0

    return 0.0
